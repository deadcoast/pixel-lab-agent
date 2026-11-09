"""Exact connected-plan evidence for the existing independent caller review."""

import json
from pathlib import Path

from . import codec, graph, jobs, plar, platform, production_plan, retention, store
from .codec import PixlError
from .request_review import source_evidence


def handoff(folder, root, plan, job=None):
    """Arguments for pixl_request_review, not an assertion that review passed."""
    result = {
        "packet": (Path(folder) / "state.px").relative_to(root).as_posix(),
        "plan": plan,
    }
    if job:
        result["job"] = job
    return result


def _source(root, record):
    fields = record.fields
    path = retention.resolve(root, fields["ur"], fields["dg"])
    # The existing retention resolver confines both declared and retained paths.
    evidence = source_evidence(
        path.parent,
        {"path": path.name, "lines": fields["ln"]},
        fields["dg"],
    )
    return {
        **evidence,
        "id": record.id,
        "path": fields["ur"],
        "record_sha256": codec.record_hash(record),
        "source_class": fields["au"].value,
    }


def _coverage(root, path, scope_hash, rows):
    """Check identity/coverage only. Nonempty prose is not semantic correctness."""
    value = json.loads(graph.confined(root, path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise PixlError("request_review", "comparison must be an object")
    expected = {row["id"]: row["record_sha256"] for row in rows}
    comparisons = value.get("criterion_comparisons", [])
    if not isinstance(comparisons, list):
        raise PixlError("request_review", "criterion_comparisons must be a list")
    seen, duplicates, incomplete, changed, unexpected = set(), [], [], [], []
    fields = (
        "source_obligation",
        "authority_basis",
        "scope",
        "literal_delta",
        "discriminating_alternative",
        "disposition",
    )
    for row in comparisons:
        if not isinstance(row, dict) or not isinstance(row.get("criterion"), str):
            raise PixlError("request_review", "comparison needs an exact criterion ID")
        ident = row["criterion"]
        if ident in seen:
            duplicates.append(ident)
        seen.add(ident)
        if ident not in expected:
            unexpected.append(ident)
        elif row.get("record_sha256") != expected[ident]:
            changed.append(ident)
        missing = [
            key
            for key in fields
            if not isinstance(row.get(key), str) or not row[key].strip()
        ]
        if missing:
            incomplete.append({"criterion": ident, "missing": missing})
    missing = sorted(set(expected) - seen)
    current = value.get("review_scope_sha256") == scope_hash
    return {
        "path": path,
        "sha256": graph.file_hash(graph.confined(root, path)),
        "expected": len(expected),
        "observed": len(comparisons),
        "missing": missing,
        "duplicates": duplicates,
        "unexpected": unexpected,
        "changed_identities": changed,
        "incomplete": incomplete,
        "scope_current": current,
        "complete": current
        and not any((missing, duplicates, unexpected, changed, incomplete)),
        "semantic_verdict": "not_assessed",
    }


def report(root, state, plan_id, job=None, comparison=None):
    root = Path(root).resolve()
    state_path = graph.confined(root, state)
    doc = store.load(state_path.parent)
    production_plan._require(
        state_path.name == "state.px", "review needs store state.px"
    )
    marker = production_plan._record(doc, plan_id, "X")
    production_plan._require(
        marker.fields.get("mt", {}).get("binding") == "pixl.production.plan/1",
        "review needs a connected production plan",
    )
    snapshot_path = graph.confined(root, marker.fields["ur"])
    production_plan._require(
        graph.file_hash(snapshot_path) == marker.fields["dg"], "plan snapshot changed"
    )
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    plan = snapshot["plan"]
    production_plan._validate(plan, production_plan.SCHEMA)
    production_plan._require(plan_id == plan["id"] + ".plan", "plan identity mismatch")
    diagnostics, rows, sources, controls = [], [], {}, []
    try:
        production_plan._current_plan(doc, marker)
    except PixlError as error:
        diagnostics.append({"status": "changed_plan_context", "reason": str(error)})
    for stage in [*plan["stages"], {"id": "delivery", **plan["delivery"]}]:
        task_id, output_id = production_plan._ids(plan, stage["id"])
        output = production_plan._record(doc, output_id, "F")
        controls.append(
            {
                "output": output_id,
                "task": task_id,
                "record_sha256": codec.record_hash(output),
                "fields": codec.to_data(output.fields),
                "contract": codec.to_data(doc.records[stage["contract"]].fields)
                if "contract" in stage
                else None,
                "inputs": [
                    {"id": ref.id, "fields": codec.to_data(doc.records[ref.id].fields)}
                    for ref in doc.records[task_id].fields["ip"]
                    if "of" in doc.records[ref.id].fields
                ],
            }
        )
        for criterion in stage["criteria"]:
            ident = plan["id"] + "." + stage["id"] + ".q." + criterion["id"]
            current = doc.records.get(ident)
            expected = marker.fields["mt"]["scope"][ident]
            status = (
                "current"
                if current and codec.record_hash(current) == expected
                else "changed"
            )
            if status != "current":
                diagnostics.append({"criterion": ident, "status": "changed_criterion"})
            for source_id in criterion["sources"]:
                if source_id in sources:
                    continue
                record = production_plan._record(doc, source_id, "S")
                try:
                    evidence = _source(root, record)
                except (OSError, PixlError) as error:
                    evidence = {
                        "id": source_id,
                        "status": "unavailable",
                        "reason": str(error),
                        "record_sha256": codec.record_hash(record),
                    }
                if codec.record_hash(record) != marker.fields["mt"]["scope"].get(
                    source_id
                ):
                    evidence["record_status"] = "changed"
                    diagnostics.append(
                        {"source": source_id, "status": "changed_source_record"}
                    )
                if evidence["status"] != "resolved":
                    diagnostics.append(
                        {"source": source_id, "status": evidence["status"]}
                    )
                sources[source_id] = evidence
            rows.append(
                {
                    **criterion,
                    "id": ident,
                    "stage": stage["id"],
                    "output": output_id,
                    "record_sha256": expected,
                    "record_status": status,
                    "current_record_sha256": codec.record_hash(current)
                    if current
                    else None,
                    "authority": "unclassified",
                    "comparison": "unperformed",
                }
            )
    selections = []
    for stage in plan["stages"]:
        if "selection" not in stage:
            continue
        selection = stage["selection"]
        try:
            current = plar.read(
                root, selection["path"], selection["asset"], include_production=False
            )
            item = {
                **selection,
                "current_requirements_hash": current["requirements_hash"],
                "current_requirements": plar._requirements(current["asset"]),
            }
            if current["requirements_hash"] != selection["requirements_hash"]:
                diagnostics.append(
                    {"asset": selection["asset"], "status": "changed_selection"}
                )
        except (OSError, PixlError) as error:
            item = {**selection, "status": "unavailable", "reason": str(error)}
            diagnostics.append(item)
        selections.append(item)
    request = None
    if job:
        record = production_plan._record(doc, job, "J")
        task_ids = {production_plan._ids(plan, s["id"])[0] for s in plan["stages"]}
        production_plan._require(
            record.fields["tk"].id in task_ids, "job belongs to another plan"
        )
        journal = jobs._get(doc, job, root)
        summary = jobs._summary(doc, record, journal, root, state_path.parent)
        request = {
            key: summary[key]
            for key in (
                "id",
                "state",
                "remote_id",
                "intent_sha256",
                "request",
                "blockers",
                "next_action",
            )
        }
    scope = {
        "plan": {
            "id": plan_id,
            "path": marker.fields["ur"],
            "sha256": marker.fields["dg"],
        },
        "baseline": {
            "id": plan["baseline"],
            "fields": codec.to_data(doc.records[plan["baseline"]].fields),
        },
        "criteria": rows,
        "sources": list(sources.values()),
        "controls": controls,
        "decisions": [
            {"id": ident, "fields": codec.to_data(doc.records[ident].fields)}
            for ident in plan["decisions"]
        ],
        "selections": selections,
        "request": request,
    }
    scope_hash = platform._sha(
        {
            **scope,
            "sources": [
                {k: v for k, v in source.items() if k != "absolute_path"}
                for source in scope["sources"]
            ],
        }
    )
    return {
        "version": 1,
        "kind": "production_plan_review",
        **scope,
        "state": {"path": state, "sha256": codec.digest(doc), "revision": doc.revision},
        "review_scope_sha256": scope_hash,
        "criterion_ids": [r["id"] for r in rows],
        "diagnostics": diagnostics,
        "comparison_coverage": _coverage(root, comparison, scope_hash, rows)
        if comparison
        else None,
        "caller_comparison": "unperformed",
        "consistent": None,
        "instruction": "Compare each exact criterion, including collective rules, by source obligation, authority/basis, scope, literal delta, a discriminating alternative and disposition. Split mixed clauses in the interpretation. Preserve required qualitative outcomes; scope expert recipes rather than inventing owner rules. Retain corrections separately from historical records.",
        "scope": "Read-only evidence and structural comparison coverage, not semantic consistency, adoption, provider execution or art acceptance. Current source records marked changed do not reconstruct their historical declarations.",
    }
