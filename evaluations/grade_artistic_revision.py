"""Independent retained-art successor checks; semantic/visual judgment stays explicit.

This checks saved records and decoded capture pixels, not a caller's pass summary.
It deliberately does not execute a consumer-supplied checker or renderer.
"""

from __future__ import annotations

import argparse
import json
import tomllib
from itertools import pairwise
from pathlib import Path
from typing import Any, cast

from PIL import Image, ImageChops, ImageColor

from evaluations.grade_named_codex_role import named_route_checks, rows, trace_facts
from evaluations.host_trials import sha, write_json
from pixl import candidate_review, codec, families, graph, job_history, plar

WORK = "work/artistic-revision"
INPUTS = "work/artistic-revision-inputs"
OLD_JOB = "authoring-01.working.join-01"
CONSUMERS = {"statusCell", "compactStatus"}
SCALES = {1, 3}
STATES = {"idle", "running", "succeeded", "failed", "paused"}


def read(path: Path):
    return json.loads(path.read_bytes())


def confined(root: Path, name: str) -> Path:
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes consumer: {name}")
    return path


def referenced(root: Path, item) -> Path:
    if isinstance(item, str):
        return confined(root, item)
    path = confined(root, item["path"])
    if sha(path) != item["sha256"]:
        raise ValueError(f"Referenced bytes changed: {item['path']}")
    return path


def renamed(text: str) -> str:
    """Only the announced new destination names change the retained literal text."""
    return text.replace("src/queue-view-successor.ts", "src/queue-view-artistic.ts").replace(
        "renderer-successor/", "renderer-artistic/")


def pixel_difference(left: Image.Image, right: Image.Image) -> float:
    extrema = cast(tuple[tuple[float, float], ...], ImageChops.difference(left, right).convert("RGB").getextrema())
    return max(high for _, high in extrema)


def criteria_errors(document, baseline, correction, proposal, mapping, root: Path,
                    approved_changes: dict | None = None) -> list[str]:
    errors = []
    originals = correction["retained_comparison"]["original_20"]
    expected_originals = {r["id"]: r["record_sha256"] for r in originals}
    supplied_originals = mapping.get("original_20", [])
    if len(expected_originals) != 20 or len(supplied_originals) != 20 or {
        r["id"]: r["record_sha256"] for r in supplied_originals
    } != expected_originals:
        errors.append("original20 mapping differs from retained reconciliation")
    for ident, digest in expected_originals.items():
        if ident not in baseline.records or codec.record_hash(baseline.records[ident]) != digest:
            errors.append(f"original20 baseline mismatch: {ident}")
        if ident not in document.records or codec.record_hash(document.records[ident]) != digest:
            errors.append(f"original20 changed: {ident}")
    expected = {r["id"]: r for r in correction["corrected_criteria"]}
    adopted = mapping.get("corrected_29", [])
    if len(expected) != 29 or len(adopted) != 29 or {r["source_id"] for r in adopted} != set(expected):
        return errors + ["corrected29 membership differs from retained reconciliation"]
    if len({r["record_id"] for r in adopted}) != 29:
        errors.append("corrected29 does not bind 29 distinct saved criteria")
    old_proposal = {r["id"]: r for r in proposal["criteria"]}
    source_index = {**proposal["sources"], **correction["sources"]}
    for row in adopted:
        ident, original = row["record_id"], expected[row["source_id"]]
        literal = original["corrected_check"]
        if literal == "(unchanged)":
            literal = original["original_check"]
        # A separate evaluator can approve an exact, evidence-bound descriptive
        # rederivation. The native caller's assertion is insufficient by itself.
        if row.get("check") not in (literal, renamed(literal)):
            approved = (approved_changes or {}).get(row["source_id"], {})
            if not (approved.get("record_id") == ident and approved.get("before") in (literal, renamed(literal))
                    and approved.get("after") == row.get("check")):
                errors.append(f"semantic review required for exact revised literal: {ident}")
        for field in ("authority_label_for_record", "clauses", "expert_clauses", "carries",
                      "sources_added", "evidence_route"):
            if row.get(field) != original.get(field):
                errors.append(f"corrected authority/lineage changed: {ident}.{field}")
        record = document.records.get(ident)
        if record is None or record.kind != "Q" or ident in baseline.records:
            errors.append(f"successor criterion is not new saved Q: {ident}")
            continue
        q = record.fields
        if q["ck"] != row.get("check") or (q["dm"].value, q["md"].value) != (original["domain"], original["mode"]):
            errors.append(f"saved check or route differs: {ident}")
        actual_sources = set()
        actual_source_paths = set()
        for ref in q["so"]:
            source = document.records[ref.id]
            if source.kind != "S":
                errors.append(f"not a source: {ref.id}")
                continue
            data = source.fields
            path = confined(root, data["ur"])
            if not path.is_file() or sha(path) != data["dg"]:
                errors.append(f"source bytes differ: {ref.id}")
                continue
            count = len(path.read_text(encoding="utf-8").splitlines())
            bounds = data["ln"]
            if len(bounds) != 2 or not 1 <= bounds[0] <= bounds[1] <= count:
                errors.append(f"invalid file-local source bounds: {ref.id}")
            actual_sources.add(data["dg"])
            actual_source_paths.add((data["ur"], data["dg"]))
        required = old_proposal[row["source_id"]]["sources"] + original.get("sources_added", [])
        for source in required:
            digest = source.get("sha256", source_index[source["id"]]["sha256"])
            if digest not in actual_sources:
                old_path = source_index[source["id"]].get("path", "")
                new_path = renamed(old_path)
                new_file = confined(root, new_path) if new_path else None
                # Source facts for the expressly adapted destination must bind
                # its actual new bytes. Owner/caller sources have no such rename.
                rebound = (new_path != old_path and new_file is not None and new_file.is_file()
                           and (new_path, sha(new_file)) in actual_source_paths)
                if not rebound:
                    errors.append(f"retained source not bound: {ident}:{source['id']}")
    return errors


def semantic_changes(path: Path | None, root: Path, mapping_path: Path, correction_path: Path) -> dict:
    """Load only an evaluator-supplied, exact-hash approval; never discover one from caller output."""
    if path is None:
        return {}
    review = read(path)
    if (review.get("version") != 1 or review.get("mapping_sha256") != sha(mapping_path)
            or review.get("reconciliation_sha256") != sha(correction_path)):
        raise ValueError("Independent semantic review does not bind the current mapping/reconciliation")
    decisions = {}
    for row in review["decisions"]:
        if (row["source_id"] in decisions or row.get("approved") is not True or not row.get("reason")
                or not row.get("evidence") or not row.get("record_id") or not row.get("before") or not row.get("after")):
            raise ValueError("Incomplete or duplicate independent semantic decision")
        for item in row["evidence"]:
            if not isinstance(item, dict) or not item.get("sha256"):
                raise ValueError("Semantic decision evidence must bind exact file bytes")
            referenced(root, item)
        decisions[row["source_id"]] = row
    return decisions


def job_errors(document, baseline, root: Path) -> list[str]:
    old, current = baseline.records[OLD_JOB], document.records[OLD_JOB]
    errors = []
    for field in ("ah", "tk", "tl", "op", "xs", "ri"):
        if current.fields[field] != old.fields[field]:
            errors.append(f"prepared job immutable field changed: {field}")
    def journal(record, doc):
        artifact = doc.records[record.fields["jr"].id]
        path = confined(root, artifact.fields["ur"])
        if sha(path) != artifact.fields["dg"]:
            raise ValueError("Job journal identity differs")
        return job_history.validate(read(path))
    before, after = journal(old, baseline), journal(current, document)
    if after["intent"] != before["intent"] or after["intent_sha256"] != before["intent_sha256"]:
        errors.append("prepared job intent changed")
    if after["events"][:len(before["events"])] != before["events"]:
        errors.append("prepared job events are not append-only")
    appended = after["events"][len(before["events"]):]
    if (before["state"] != "prepared" or current.fields["si"].value != "failed"
            or after["state"] != "failed" or after["remote_id"] is not None
            or len(appended) != 1 or appended[0]["event"] != "failed"
            or appended[0]["remote_id"] is not None or appended[0]["artifact"] is not None):
        errors.append("pending job is not locally abandoned without dispatch or remote identity")
    return errors


def image_error(root: Path, capture: Path, item: dict, display: dict, *, screenshot=None) -> str | None:
    """Independently decode the retained source crop, composite and nearest scale."""
    try:
        path = referenced(capture, item["image"])
        with Image.open(path) as opened:
            actual = opened.convert("RGBA")
        descriptor = item["descriptor"]
        source = confined(root, descriptor["path"])
        if item.get("asset", {}).get("sha256", sha(source)) != sha(source):
            return "asset hash differs"
        width, height = display["cell"]
        scale = item["scale"]
        if actual.size != (width * scale, height * scale):
            return "canvas size differs"
        # SVG Start is preserved byte-for-byte and screen placement is checked;
        # PNG members permit an independent full pixel-compositing calculation.
        if source.suffix.lower() == ".png":
            with Image.open(source) as opened:
                image = opened.convert("RGBA")
            if image.size != (width * descriptor["frames"], height):
                return "source geometry differs"
            frame = item["frame"]
            if not isinstance(frame, int) or not 0 <= frame < descriptor["frames"]:
                return "invalid frame index"
            crop = image.crop((frame * width, 0, (frame + 1) * width, height))
            panel = Image.new("RGBA", crop.size, (*ImageColor.getrgb(display["background"]), 255))
            expected = Image.alpha_composite(panel, crop).resize(actual.size, Image.Resampling.NEAREST)
            if pixel_difference(expected, actual) > 1:
                return "source/composite/canvas pixels differ"
        if screenshot is not None:
            b = item["bounds"]
            if any(b[k] != round(b[k]) for k in ("x", "y", "width", "height")):
                return "fractional destination bounds"
            x, y, w, h = (int(b[k]) for k in ("x", "y", "width", "height"))
            if (w, h) != actual.size or x < 0 or y < 0 or x + w > screenshot.width or y + h > screenshot.height:
                return "destination outside screenshot"
            region = screenshot.crop((x, y, x + w, y + h))
            if pixel_difference(region, actual) > 1:
                return "canvas absent from destination screenshot"
    except (OSError, ValueError, KeyError, TypeError) as error:
        return str(error)
    return None


def observed_live_rows(report: dict) -> tuple[list[dict], list[str]]:
    """Join raw RAF samples to the same phase's independently identified live cells.

    The native fixture records timing/pixels in ``playback`` and descriptors once
    in ``live``; static event-driven observations are retained in ``stateLive``.
    No deterministic timeline is used and no absent sample is reconstructed.
    """
    rows, errors = [], []
    # stateLive captures each backend event before the timed Working run starts;
    # its isolated running snapshot belongs to that event, not the later epoch.
    static_rows = [r for r in report.get("stateLive", []) if r.get("state") != "running"]
    for source in [*report.get("playback", []), *static_rows]:
        row = dict(source)
        if "descriptor" not in row:
            matches = [cell for cell in report.get("live", []) if all(
                cell.get(key) == row.get(key) for key in ("consumer", "state", "scale"))]
            if len(matches) != 1 or row.get("motion") != report["motion"]:
                errors.append("raw playback sample has no unique same-preference live descriptor")
                continue
            row["descriptor"] = matches[0]["descriptor"]
            if "asset" in matches[0]:
                row["asset"] = matches[0]["asset"]
        rows.append(row)
    return rows, errors


def timing_error(sample: dict, motion: str) -> str | None:
    """Use the actual paint time when separately retained, not a later capture boundary."""
    if "paintElapsed" in sample or "paintAt" in sample:
        try:
            paint, at = sample["paintElapsed"], sample["paintAt"]
            elapsed, captured = sample["elapsed"], sample["at"]
            if any(not isinstance(v, (int, float)) for v in (paint, at, elapsed, captured)):
                return "paint/capture timestamps are not numeric"
            # Animated paints use the RAF clock relative to the live epoch.
            # A stationary cell is initially painted before select() starts
            # that epoch, so its zero-time construction paint has its own clock.
            bad_origin = motion == "normal" and abs((at - paint) - (captured - elapsed)) > .01
            if paint < 0 or at > captured or paint > elapsed or bad_origin:
                return "paint/capture timestamps do not preserve their shared origin/order"
            expected = int(paint // 100) % 4 if motion == "normal" else sample["descriptor"]["holdFrame"]
            if sample["frame"] != expected:
                return "observed frame contradicts owner 100ms paint timing"
        except (KeyError, TypeError):
            return "incomplete paint/capture timestamps"
    elif (motion == "normal" and sample["frame"] != int(sample["elapsed"] // 100) % 4
          and 25 < sample["elapsed"] % 100 < 75):
        return "observed frame contradicts owner 100ms timing"
    return None


def capture_errors(root: Path, path: Path) -> tuple[list[str], dict]:
    render, capture = read(path), path.parent
    errors = []
    served = render.get("served_files", {})
    if "consumer/src/queue-view-artistic.ts" not in served:
        errors.append("new destination module was not served")
    for name, digest in served.items():
        group, relative = name.split("/", 1)
        base = root if group == "consumer" else root / "renderer-artistic"
        file = confined(base, relative)
        if not file.is_file() or sha(file) != digest:
            errors.append(f"served source differs: {name}")
    phases = render.get("phases", [])
    sessions = {p["report"]["sessionId"] for p in phases}
    if len(sessions) != 1:
        errors.append("capture phases do not share one page session")
    facts: dict[str, Any] = {"phases": [], "initially_reduced": False, "switch_cycle": False}
    names = [p["name"] for p in phases]
    facts["switch_cycle"] = all(n in names for n in ("normal-start", "reduced", "normal-restored"))
    for phase in phases:
        report, name = phase["report"], phase["name"]
        motion = report["motion"]
        facts["phases"].append({"name": name, "motion": motion})
        if name == "as-launched" and motion == "reduced" and report.get("mediaMatches") is True:
            facts["initially_reduced"] = True
        expected_motion = {"normal-start": "normal", "reduced": "reduced", "normal-restored": "normal"}.get(name)
        if expected_motion and motion != expected_motion:
            errors.append(f"{name}: incorrect preference")
        if report.get("errors") or report.get("missing") or report.get("devicePixelRatio") != 1:
            errors.append(f"{name}: browser errors, missing art or unexpected pixel ratio")
        if (report["display"].get("frameMs") != 100 or report["display"].get("cell") != [16, 16]
                or report["display"].get("filter") != "nearest"):
            errors.append(f"{name}: owner timing, geometry or sampling changed")
        screenshot_path = referenced(capture, phase["screenshot"])
        with Image.open(screenshot_path) as image:
            screenshot = image.convert("RGBA")
        views = report.get("views", [])
        coverage = {(r["consumer"], r["state"], r["scale"]) for r in views}
        required = {(c, s, z) for c in CONSUMERS for s in STATES for z in SCALES}
        if coverage != required:
            errors.append(f"{name}: missing or unexpected consumer/state/scale destination")
        for item in views:
            label = f"{name}:{item['consumer']}:{item['state']}:{item['scale']}x"
            if error := image_error(root, capture, item, report["display"], screenshot=screenshot):
                errors.append(f"{label}: {error}")
            d = item["descriptor"]
            animate = item["state"] == "running" and motion == "normal"
            if d.get("animate") is not animate or d.get("motion") != motion:
                errors.append(f"{label}: descriptor does not honor preference")
            if not animate and item["frame"] != d.get("holdFrame"):
                errors.append(f"{label}: stationary cell does not hold its declared frame")
        playback, row_errors = observed_live_rows(report)
        errors.extend(f"{name}: {error}" for error in row_errors)
        for consumer in CONSUMERS:
            for scale in SCALES:
                samples = [s for s in playback if s.get("consumer") == consumer and s.get("scale") == scale
                           and s.get("state") == "running"]
                label = f"{name}:{consumer}:{scale}x live playback"
                elapsed: list[Any] = [s.get("elapsed") for s in samples]
                frames = [s.get("frame") for s in samples]
                if (len(samples) < 2 or any(not isinstance(t, (int, float)) for t in elapsed)
                        or any(b <= a for a, b in pairwise(elapsed))):
                    errors.append(f"{label}: no increasing wall-clock observations")
                    continue
                if motion == "normal":
                    wraps = sum(a == 3 and b == 0 for a, b in pairwise(frames))
                    if set(frames) != {0, 1, 2, 3} or wraps < 1 or elapsed[-1] - elapsed[0] < 400:
                        errors.append(f"{label}: no full observed four-frame loop and wrap")
                elif len(set(frames)) != 1 or elapsed[-1] - elapsed[0] < 400:
                    errors.append(f"{label}: held cell not observed across a full loop duration")
                for sample in samples:
                    if error := timing_error(sample, motion):
                        errors.append(f"{label}: {error}")
                    if error := image_error(root, capture, sample, report["display"]):
                        errors.append(f"{label}: {error}")
                for state in ("failed", "paused"):
                    static = [s for s in playback if s.get("consumer") == consumer and s.get("scale") == scale
                              and s.get("state") == state]
                    if not static:
                        errors.append(f"{name}:{consumer}:{scale}x: missing live {state} observation")
                    for sample in static:
                        descriptor = sample["descriptor"]
                        if (descriptor.get("animate") is not False or descriptor.get("motion") != motion
                                or sample["frame"] != descriptor.get("holdFrame")):
                            errors.append(f"{name}:{consumer}:{state}:{scale}x: static live state changed")
                        if error := image_error(root, capture, sample, report["display"]):
                            errors.append(f"{name}:{consumer}:{state}:{scale}x: {error}")
        if name in {"reduced", "normal-restored"}:
            events = [e for e in report.get("preferenceEvents", []) if e["to"] == motion]
            if not events or events[-1].get("sessionId") != report["sessionId"]:
                errors.append(f"{name}: no in-session media change event")
            else:
                repainted = events[-1].get("repainted", [])
                if not required <= {(r["consumer"], r["state"], r["scale"]) for r in repainted}:
                    errors.append(f"{name}: switch did not repaint all destination cells")
                for r in repainted:
                    animate = r["state"] == "running" and motion == "normal"
                    if r.get("animate") is not animate or not animate and r.get("frame") != r.get("holdFrame"):
                        errors.append(f"{name}: changed preference does not preserve static/held cells")
    return errors, facts


def plan_errors(document, plan_id: str, required_q: set[str]) -> list[str]:
    marker = document.records[plan_id]
    if marker.fields.get("mt", {}).get("binding") != "pixl.production.plan/1":
        return ["reported plan is not an authored production plan"]
    errors: list[str] = []
    planned_q: set[str] = set()
    delivery_outputs: list[str] = []
    for task_id in marker.fields["mt"]["tasks"]:
        task = document.records[task_id]
        if task.fields["st"].value != "done":
            errors.append(f"successor task unfinished: {task_id}")
        for ref in task.fields["op"]:
            output = document.records[ref.id]
            planned_q.update(q.id for q in output.fields["rq"])
            if "mb" in output.fields:
                delivery_outputs.append(ref.id)
                current = families.describe(document, ref.id)
                # This API also describes eligibility to create another snapshot.
                # A completed delivery deliberately cannot create one until reopened;
                # that sole state guard is not a defect in its existing acceptance.
                done_guard = f"family_state: {current['task']} is done; snapshots require an open or active task"
                snapshot_problems = [reason for reason in current["snapshot_blockers"] if reason != done_guard]
                if (current["state"] != "done" or not current["candidate"] or current["blockers"]
                        or snapshot_problems or current["pending_jobs"]
                        or not all(m["accepted"] for m in current["members"])):
                    errors.append(f"successor collective delivery is not accepted: {ref.id}")
    if planned_q != required_q or len(delivery_outputs) != 1:
        errors.append("authored plan does not contain exactly the corrected29 and one collective delivery")
    return errors


def historical_record_errors(document, baseline, plan_id: str, root: Path) -> list[str]:
    """Permit only the real successor's appended confirmed destination index entry."""
    marker = document.records[plan_id]
    destinations: set[str] = set()
    for task_id in marker.fields["mt"]["tasks"]:
        for output_ref in document.records[task_id].fields["op"]:
            output = document.records[output_ref.id]
            if "mb" in output.fields:
                destinations.update(ref.id for ref in output.fields.get("ds", []))
    errors = []
    for ident, old in baseline.records.items():
        current = document.records.get(ident)
        if current is not None and codec.record_hash(old) == codec.record_hash(current):
            continue
        if ident == OLD_JOB:
            continue  # Its immutable fields and append-only journal have a separate check.
        allowed = False
        if old.kind == "P" and current is not None and current.kind == "P":
            before, after = old.fields.get("in", []), current.fields.get("in", [])
            additions = after[len(before):]
            allowed = (after[:len(before)] == before and bool(additions)
                       and len({r.id for r in after}) == len(after)
                       and {k: v for k, v in old.fields.items() if k != "in"}
                       == {k: v for k, v in current.fields.items() if k != "in"})
            for ref in additions:
                choice = document.records.get(ref.id)
                allowed = allowed and (ref.id not in baseline.records and ref.id in destinations
                    and choice is not None and choice.kind == "I"
                    and choice.fields.get("pr") == codec.Ref(ident)
                    and choice.fields.get("st") == codec.Symbol("confirmed"))
                if choice is not None:
                    values = choice.fields.get("vl", {})
                    allowed = allowed and (values.get("module") == "src/queue-view-artistic.ts"
                        and values.get("fixture") == "renderer-artistic/"
                        and (root / "src/queue-view-artistic.ts").is_file()
                        and (root / "renderer-artistic/view.mjs").is_file())
        if not allowed:
            errors.append(ident)
    return errors


def completion_observation(continuation: dict) -> tuple[bool, dict]:
    """A native terminal event cannot establish an unobserved process return code."""
    evidence = {key: continuation.get(key) for key in ("status", "returncode", "interruption_reason")}
    passed = (evidence["status"] == "finished" and evidence["returncode"] == 0
              and evidence["interruption_reason"] is None)
    return passed, evidence


def outcome_status(checks: list[dict]) -> str:
    failed = [c["check"] for c in checks if not c["pass"]]
    if not failed:
        return "pass"
    if failed == ["native_attempt_completed"]:
        return "partial"
    return "fail"


def _grade(attempt: Path, consumer: Path | None = None, semantic_review: Path | None = None,
           continuation_path: Path | None = None) -> dict:
    attempt = attempt.resolve()
    launch, identity = read(attempt / "launch.json"), read(attempt / "identity.json")
    consumer = (consumer or Path(launch["cwd"])).resolve()
    checks = []

    def check(name, condition, evidence=None):
        checks.append({"check": name, "pass": bool(condition), "evidence": evidence})

    def guarded(name, operation):
        try:
            errors = operation()
            check(name, not errors, errors)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            check(name, False, str(error))

    result = read(consumer / WORK / "CALLER-RESULT.json")
    state = referenced(consumer, result["state_path"])
    document = codec.parse(state.read_bytes())
    baseline = codec.parse((consumer / INPUTS / "baseline/state.px").read_bytes())
    correction_path = consumer / "work/continuation/SPECIALIST-ROUND2.json"
    correction = read(correction_path)
    proposal = read(consumer / "work/focused-successor/specialist-proposal.json")
    mapping_path = referenced(consumer, result.get("criteria_mapping", WORK + "/adopted-criteria.json"))
    mapping = read(mapping_path)
    approved_changes = semantic_changes(semantic_review, consumer, mapping_path, correction_path)
    guarded("valid_saved_production_graph", lambda: graph.validate(document, consumer) and [])
    changed = historical_record_errors(document, baseline, result["plan_id"], consumer)
    check("historical_records_preserved_with_exact_additive_destination", not changed, changed)
    allowed = {state.relative_to(consumer).as_posix(), result["plar_path"]}
    drift = [name for name, digest in identity.get("inputs", {}).items()
             if name not in allowed and (not (consumer / name).is_file() or sha(consumer / name) != digest)]
    check("retained_inputs_art_sources_and_failures_preserved", not drift, drift)
    guarded("original20_and_corrected29_literal_authority_and_sources", lambda: criteria_errors(
        document, baseline, correction, proposal, mapping, consumer, approved_changes))
    guarded("pending_request_abandoned_locally_with_history", lambda: job_errors(document, baseline, consumer))
    required_q = {r["record_id"] for r in mapping.get("corrected_29", [])}
    guarded("successor_plan_and_collective_delivery_completed", lambda: plan_errors(document, result["plan_id"], required_q))
    candidates, reviews = result.get("candidate_ids", []), result.get("review_ids", [])
    reviewed = set()
    review_errors = []
    for ident in reviews:
        record = document.records[ident]
        if ident in baseline.records or record.fields.get("mt", {}).get("candidate_review") != 1:
            review_errors.append(f"not a fresh explicit review: {ident}")
            continue
        path = confined(consumer, record.fields["ur"])
        if sha(path) != record.fields["dg"]:
            review_errors.append(f"review bytes changed: {ident}")
            continue
        saved = read(path)
        if saved["candidate"] not in candidates:
            review_errors.append(f"review candidate not declared: {ident}")
        for item in saved["files"]:
            referenced(path.parent, item)
        for verdict in saved["observation"]["verdicts"]:
            if verdict["status"] == "pass":
                reviewed.add(verdict["criterion"])
    for ident in candidates:
        context = candidate_review.context(document, consumer, ident)
        if not context["current_acceptance"]["all_required_pass"] or not context["current_acceptance"]["task_complete"]:
            review_errors.append(f"current candidate not accepted: {ident}")
    check("fresh_reviews_cover_all29_current_criteria", bool(reviews) and bool(candidates)
          and required_q <= reviewed and not review_errors, {"errors": review_errors, "unreviewed": sorted(required_q - reviewed)})
    capture_facts = []
    for item in result.get("renderer_evidence", []):
        def verify_capture(item=item):
            errors, facts = capture_errors(consumer, referenced(consumer, item))
            capture_facts.append(facts)
            return errors
        guarded("independent_destination_capture:" + item["path"], verify_capture)
    check("both_switch_cycle_and_initial_reduced_observed", any(f["switch_cycle"] for f in capture_facts)
          and any(f["initially_reduced"] for f in capture_facts), capture_facts)
    def handoff_errors():
        path = referenced(consumer, result["handoff"])
        saved = read(path)
        selected = plar.read(consumer, path=result["plar_path"], asset_id="queue.working")
        expected = {"path": result["plar_path"], "hash": selected["hash"],
                    "current": selected["production"]["selection_current"]}
        valid = (path.stem == sha(path) and saved.get("asset_id") == "queue.working"
                 and saved.get("requirements_hash") == selected["requirements_hash"]
                 and saved.get("selection") == expected
                 and saved.get("resume") == selected["production"]["continuation"]
                 and saved.get("next") == selected["production"]["continuation"]["action"])
        return [] if valid else ["handoff differs from current public PLAR continuation"]
    guarded("exact_current_handoff", handoff_errors)
    role_path = consumer / ".codex/agents/pixl.toml"
    selected_continuation = continuation_path or attempt / "continuation.json"
    continuation = read(selected_continuation)
    role = tomllib.loads(role_path.read_text(encoding="utf-8"))
    facts = trace_facts([rows(p) for p in sorted(attempt.glob("native-*.jsonl"))],
                        continuation.get("session_id"), role["developer_instructions"])
    for name, passed, evidence in named_route_checks(facts):
        if name != "same_child_completed_after_followup":
            check(name, passed, evidence)
    completed, completion_evidence = completion_observation(continuation)
    check("native_attempt_completed", completed, completion_evidence)
    return {"version": 1, "status": outcome_status(checks),
            "checks": checks, "passed": sum(c["pass"] for c in checks), "total": len(checks),
            "task_outcome_status": "pass" if all(c["pass"] for c in checks if c["check"] != "native_attempt_completed") else "fail",
            "native_host_completion_status": "pass" if completed else "unverified_or_interrupted",
            "continuation_evidence": {"path": str(selected_continuation), "sha256": sha(selected_continuation),
                                      "explicit_override": continuation_path is not None},
            "independent_semantic_review": {"path": str(semantic_review), "sha256": sha(semantic_review),
                                            "approved_source_ids": sorted(approved_changes)} if semantic_review else None,
            "scope": "Independent saved-state, authority mapping, provenance, native-role and destination pixel checks. Visual meanings and aesthetic judgments require the separately retained human/model inspection; M1/M2 and broader quality remain open."}


def grade(attempt: Path, consumer: Path | None = None, semantic_review: Path | None = None,
          continuation_path: Path | None = None) -> dict:
    try:
        return _grade(attempt, consumer, semantic_review, continuation_path)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        return {"version": 1, "status": "fail", "passed": 0, "total": 1,
                "checks": [{"check": "required_evidence_readable", "pass": False,
                            "evidence": f"{type(error).__name__}: {error}"}],
                "scope": "Incomplete or invalid evidence; no production acceptance inferred."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attempt", type=Path)
    parser.add_argument("--consumer", type=Path)
    parser.add_argument("--semantic-review", type=Path,
                        help="Independent evaluator's exact mapping-bound descriptive rederivation decisions")
    parser.add_argument("--continuation", type=Path,
                        help="Explicit additive recovery record; original continuation remains unchanged")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    outcome = grade(args.attempt, args.consumer, args.semantic_review, args.continuation)
    write_json(args.output, outcome)
    print(json.dumps({k: outcome[k] for k in ("status", "passed", "total")}))
    raise SystemExit(0 if outcome["status"] == "pass" else 1)
