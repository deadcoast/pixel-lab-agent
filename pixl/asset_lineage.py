"""Bounded, read-only provenance views over existing artifact and job identities.

Public callers validate the rooted graph first. This projection also verifies
the files it reads and the durable job projections it exposes. Request intent
and caller observations never authenticate execution by a remote service.
"""

import json
from collections import deque
from itertools import islice
from urllib.parse import urlsplit

from . import graph, jobs
from .codec import PixlError

LIMITS = {"jobs": 32, "depth": 4, "same_bytes": 16, "workflow_inputs": 16,
          "events_per_job": 32, "source_requests_per_job": 8,
          "source_matches": 32, "simulation_nodes": 512}
_GENERATE = {"create_image_pro", "create_image_pro_flash", "create_image_pixflux",
             "create_image_bitforge", "create_character", "create_isometric_tile",
             "create_topdown_tileset", "create_sidescroller_tileset"}


def _operation(request):
    tool, arguments = request["tool"], request["arguments"]
    if tool in _GENERATE:
        return "generation_request", {}
    if tool in {"animate_image", "animate_character"}:
        return "animation_request", {}
    argv = arguments.get("argv")
    if tool == "pixelart_workbench" and isinstance(argv, list) and argv[:1] == ["edit"]:
        try:
            value = json.loads(argv[argv.index("--changes") + 1])
            if isinstance(value, list) and value and all(
                isinstance(row, dict) and row.get("operation") == "patch_pixels"
                for row in value
            ):
                return "deterministic_edit_request", {
                    "operations": ["patch_pixels"],
                    "patch_count": sum(len(row.get("pixels", [])) for row in value
                                       if isinstance(row.get("pixels", []), list)),
                }
        except (ValueError, IndexError, TypeError):
            pass
        return "provider_edit_request", {}
    if tool in {"edit_image", "edit_image_pro", "edit_image_pro_flash"}:
        return "provider_edit_request", {}
    return "unknown", {}


def _references(request):
    """Interpret only explicit source fields; never prompts or arbitrary IDs."""
    arguments = request["arguments"]
    argv = arguments.get("argv")
    if (request["tool"] == "pixelart_workbench" and isinstance(argv, list)
            and len(argv) >= 2 and argv[0] == "edit" and isinstance(argv[1], str)):
        yield "edit_source", argv[1], "/intent/request/arguments/argv/1"
    for key in ("first_frame_url", "last_frame_url", "image_url"):
        if isinstance(arguments.get(key), str):
            yield key, arguments[key], f"/intent/request/arguments/{key}"
    style = arguments.get("style_image")
    if isinstance(style, dict) and isinstance(style.get("url"), str):
        yield "style_reference", style["url"], "/intent/request/arguments/style_image/url"


def _remote_identity(locator):
    if locator.startswith("upload:"):
        return None
    if locator.startswith("job:"):
        return locator[4:] or None
    try:
        url = urlsplit(locator)
    except ValueError:
        return None
    if url.scheme:
        parts = url.path.split("/")
        if (url.scheme == "https" and url.netloc == "api.pixellab.ai"
                and not url.query and not url.fragment and len(parts) == 5
                and parts[:3] == ["", "mcp", "images"] and parts[4] == "download"):
            return parts[3] or None
        return None
    return locator if locator and "/" not in locator and "\\" not in locator else None


def _simulation_claims(request, events):
    """Only evidence assertions count; schema and request parameters do not."""
    pending = deque()
    result = []
    truncated = False
    remaining = LIMITS["simulation_nodes"]

    def enqueue(value, path, depth, claim=False):
        nonlocal remaining, truncated
        if remaining:
            pending.append((value, path, depth, claim))
            remaining -= 1
        else:
            truncated = True

    for key in ("authorization", "discovery"):
        enqueue(request.get(key, {}).get("evidence", {}), f"/intent/request/{key}/evidence", 0)
    for index, event in enumerate(events[:remaining]):
        enqueue(event["evidence"], f"/events/{index}/evidence", 0)
    truncated |= len(events) > LIMITS["simulation_nodes"] - 2
    while pending:
        value, path, depth, claim = pending.popleft()
        if depth > 8:
            truncated = True
            continue
        if claim and type(value) is bool:
            result.append({"locator": path, "value": value})
            continue
        if isinstance(value, dict):
            truncated |= len(value) > remaining
            for key, child in islice(value.items(), remaining):
                pointer = path + "/" + key.replace("~", "~0").replace("/", "~1")
                enqueue(child, pointer, depth + 1, key in {"simulated", "provider_simulated"})
        elif isinstance(value, list):
            truncated |= len(value) > remaining
            for index, child in enumerate(value[:remaining]):
                enqueue(child, path + f"/{index}", depth + 1)
    return result, truncated


def describe(doc, root, candidate_id):
    """Describe retained evidence, not acceptance or a complete production DAG."""
    candidate = doc.records.get(candidate_id)
    if candidate is None or candidate.kind != "X":
        raise PixlError("lineage_candidate", "select an existing artifact")
    truncated = False
    journal_cache = {}

    def retained_journal(record):
        nonlocal truncated
        if record.id not in journal_cache:
            if len(journal_cache) >= LIMITS["jobs"]:
                truncated = True
                return None
            journal_cache[record.id] = jobs._get(doc, record.id, root)
        return journal_cache[record.id]

    def bounded(value, depth=0):
        nonlocal truncated
        if isinstance(value, str) and len(value) > 512:
            truncated = True
            return value[:512] + "…"
        if isinstance(value, (dict, list)):
            if depth >= 4:
                truncated = True
                return {"omitted": "read exact retained journal locator"}
            if len(value) > 12:
                truncated = True
            if isinstance(value, dict):
                return {key: bounded(child, depth + 1)
                        for key, child in list(value.items())[:12]}
            return [bounded(child, depth + 1) for child in value[:12]]
        return value

    def artifact_row(record):
        nonlocal truncated
        path = graph.confined(root, record.fields["ur"])
        try:
            actual_hash = graph.file_hash(path)
        except OSError as error:
            raise PixlError("lineage_file", record.id) from error
        if actual_hash != record.fields["dg"]:
            raise PixlError("file_hash", record.id)
        direct_jobs = importers.get(record.id, [])
        truncated |= len(direct_jobs) > LIMITS["jobs"]
        return {"candidate": record.id, "uri": record.fields["ur"],
                "sha256": record.fields["dg"],
                "output": record.fields["of"].id if "of" in record.fields else None,
                "jobs": direct_jobs[:LIMITS["jobs"]]}

    all_jobs = sorted((r for r in doc.records.values() if r.kind == "J"),
                      key=lambda r: r.id)
    importers = {}
    for record in all_jobs:
        for ref in record.fields.get("xs", []):
            importers.setdefault(ref.id, []).append(record.id)
    selected = artifact_row(candidate)
    equivalents = [r for r in sorted(doc.records.values(), key=lambda r: r.id)
                   if r.kind == "X" and r.id != candidate_id and "of" in r.fields
                   and r.fields["dg"] == candidate.fields["dg"]]
    truncated |= len(equivalents) > LIMITS["same_bytes"]
    same_bytes = [artifact_row(r) for r in equivalents[:LIMITS["same_bytes"]]]
    inputs = []
    if "of" in candidate.fields:
        output = doc.records[candidate.fields["of"].id]
        task = doc.records[output.fields["tk"].id]
        refs = task.fields.get("ip", [])
        truncated |= len(refs) > LIMITS["workflow_inputs"]
        inputs = [artifact_row(doc.records[r.id]) for r in refs[:LIMITS["workflow_inputs"]]]
    queue = deque((id_, 0) for row in [selected, *same_bytes, *inputs] for id_ in row["jobs"])
    seen = set()
    rows = []
    while queue:
        id_, depth = queue.popleft()
        if id_ in seen:
            continue
        if len(rows) >= LIMITS["jobs"] or depth > LIMITS["depth"]:
            truncated = True
            continue
        seen.add(id_)
        record = doc.records[id_]
        if "jr" not in record.fields:
            continue
        journal = retained_journal(record)
        if journal is None:
            continue
        request = journal["intent"]["request"]
        retained = doc.records[record.fields["jr"].id]
        operation, details = _operation(request)
        claims, claims_truncated = _simulation_claims(request, journal["events"])
        truncated |= claims_truncated
        values = {claim["value"] for claim in claims}
        simulated = next(iter(values)) if len(values) == 1 and not claims_truncated else None
        sources = []
        references = list(_references(request))
        truncated |= len(references) > LIMITS["source_requests_per_job"]
        for role, locator, pointer in references[:LIMITS["source_requests_per_job"]]:
            remote = _remote_identity(locator)
            matches = [r for r in all_jobs if remote is not None and r.fields["ri"] == remote]
            # Provider IDs are scoped to the recorded provider, not globally unique.
            matched = []
            matches_truncated = len(matches) > LIMITS["source_matches"]
            for other in matches[:LIMITS["source_matches"]]:
                if "jr" in other.fields:
                    other_journal = retained_journal(other)
                    if other_journal is None:
                        matches_truncated = True
                        continue
                    other_request = other_journal["intent"]["request"]
                    if other_request["provider"] == request["provider"]:
                        matched.append(other)
            matched_candidates = [ref.id for r in matched for ref in r.fields.get("xs", [])]
            matches_truncated |= len(matched_candidates) > LIMITS["source_matches"]
            truncated |= matches_truncated
            sources.append({"role": role, "locator": bounded(locator), "journal_locator": pointer,
                            "relationship": "recorded_request_reference",
                            "matching_jobs": [r.id for r in matched],
                            "matching_candidates": matched_candidates[:LIMITS["source_matches"]],
                            "resolution": "truncated" if matches_truncated else "unresolved" if not matched else "unique" if len(matched) == 1 else "ambiguous"})
            queue.extend((other.id, depth + 1) for other in matched)
        events = journal["events"]
        truncated |= len(events) > LIMITS["events_per_job"]
        observed, imported = [], []
        for index, event in enumerate(events[:LIMITS["events_per_job"]]):
            event_row = {"sequence": event["sequence"], "event": event["event"],
                         "locator": f"/events/{index}", "evidence": bounded(event["evidence"])}
            if event["event"] == "imported":
                event_row["artifact"] = event["artifact"]
                imported.append(event_row)
            elif event["event"] != "dispatch":
                observed.append(event_row)
        rows.append({"id": id_, "tool": request["tool"], "provider": request["provider"],
                     "remote_id": journal["remote_id"], "state": journal["state"],
                     "operation": operation, "operation_details": details, "simulated": simulated,
                     "simulation_claims": bounded(claims), "simulation_conflict": len(values) > 1,
                     "simulation_scan_truncated": claims_truncated,
                     "remote_verified": False,
                     "journal": {"artifact": retained.id, "uri": retained.fields["ur"],
                                 "sha256": retained.fields["dg"]},
                     "imports": imported, "observations": observed, "source_requests": sources})
    return {"candidate": candidate_id, "sha256": candidate.fields["dg"], "artifact": selected,
            "provenance_status": "recorded_provider_import" if selected["jobs"] else
            "same_bytes_as_recorded_import" if any(r["jobs"] for r in same_bytes) else "unrecorded",
            "remote_verified": False, "jobs": rows, "same_bytes": same_bytes,
            "workflow_inputs": inputs, "truncated": truncated, "limits": dict(LIMITS),
            "limitations": [
                "Job identities and local journal bytes are verified; provider observations are caller-reported, not remotely authenticated.",
                "Operations describe recorded request intent, not successful generation, artistic quality or acceptance.",
                "Matching remote IDs expose request references, not proof that every imported byte came from that source.",
                "Same bytes means equivalence, not a parent, reuse direction or common origin.",
                "Workflow inputs and style references are context, not pixel derivation. Unresolved uploads and absent links remain unknown.",
                "The projection is bounded; use retained journal paths and JSON pointers for full evidence. It is not a complete lineage ledger.",
            ]}
