"""Concise structural comparison backed by exact connected-plan review reports."""

from pathlib import Path
from urllib.parse import urlsplit

from . import codec, graph, platform, production_plan, production_review, store
from .codec import PixlError


def _plan(root, doc, ident):
    marker = production_plan._record(doc, ident, "X")
    return marker, production_plan._snapshot(root, marker)


def _delta(before, after):
    common = sorted(before.keys() & after.keys())
    return {
        "added": [{"key": key, "after": after[key]} for key in sorted(after.keys() - before.keys())],
        "removed": [{"key": key, "before": before[key]} for key in sorted(before.keys() - after.keys())],
        "changed": [{"key": key, "before": before[key], "after": after[key],
                     "fields": sorted(k for k in before[key].keys() | after[key].keys()
                                      if before[key].get(k) != after[key].get(k))}
                    for key in common if before[key] != after[key]],
        "unchanged": [key for key in common if before[key] == after[key]],
    }


def _criteria(snapshot):
    plan = snapshot["plan"]
    return {stage["id"] + "/" + q["id"]: {k: q[k] for k in ("check", "domain", "mode", "sources")}
            for stage in [*plan["stages"], {"id": "delivery", **plan["delivery"]}]
            for q in stage["criteria"]}


def _bound(doc, marker, kinds):
    # A changed current declaration cannot reconstruct historical fields.
    result = {}
    for ident, expected in marker.fields["mt"]["scope"].items():
        record = doc.records.get(ident)
        if record is not None and record.kind in kinds:
            actual = codec.record_hash(record)
            result[ident] = {"record_sha256": expected, "current_record_sha256": actual,
                             "current": expected == actual,
                             "declaration": codec.to_data(record.fields) if expected == actual else None}
    return result


def _receipts(doc, root, verdict):
    result = []
    for ref in verdict.fields["ev"]:
        record = doc.records[ref.id]
        fields = record.fields
        stale = [b["rf"].id for b in fields["bs"]
                 if b["rf"].id not in doc.records or codec.record_hash(doc.records[b["rf"].id]) != b["dg"]]
        if urlsplit(fields["ur"]).scheme in ("http", "https"):
            file_status = "remote_unverified"
        else:
            try:
                path = graph.confined(root, fields["ur"])
                file_status = "current" if graph.file_hash(path) == fields["dg"] else "changed"
            except (OSError, PixlError):
                file_status = "unavailable"
        result.append({"id": ref.id, "path": fields["ur"], "sha256": fields["dg"],
                       "obsolete": fields.get("ob", False), "stale_bindings": stale, "file_status": file_status})
    return result


def _reviews(doc, root, state, snapshot):
    plan = snapshot["plan"]
    task_ids = [production_plan._ids(plan, stage)[0] for stage in [*(s["id"] for s in plan["stages"]), "delivery"]]
    history = []
    outputs = []
    for task_id in task_ids:
        task = doc.records[task_id]
        nominees = {doc.records[r.id].fields["of"].id: r.id for r in task.fields["ca"]}
        verdicts = [doc.records[r.id] for r in task.fields["vr"]]
        for verdict in verdicts:
            fields = verdict.fields
            receipts = _receipts(doc, root, verdict)
            if fields["st"].value != "pass" or fields.get("ob", False) or any(
                r["obsolete"] or r["stale_bindings"] or r["file_status"] != "current" for r in receipts
            ):
                history.append({"id": verdict.id, "criterion": fields["rq"].id,
                                "candidate": fields["xr"].id, "status": fields["st"].value,
                                "obsolete": fields.get("ob", False), "reason": fields["wy"], "receipts": receipts})
        for output_ref in task.fields["op"]:
            output = doc.records[output_ref.id]
            candidate = nominees.get(output.id)
            current = {v.fields["rq"].id: v for v in verdicts
                       if not v.fields.get("ob", False) and v.fields["xr"].id == candidate}
            outstanding = []
            for requirement in output.fields["rq"]:
                verdict = current.get(requirement.id)
                usable = False
                if verdict is not None and verdict.fields["st"].value == "pass":
                    receipts = [r for r in _receipts(doc, root, verdict) if not r["obsolete"]]
                    covered = {b["rf"].id for r in receipts for b in doc.records[r["id"]].fields["bs"]}
                    usable = bool(receipts) and all(
                        not r["stale_bindings"] and r["file_status"] == "current"
                        and doc.records[r["id"]].fields["rs"].value == "pass"
                        and doc.records[r["id"]].fields["md"] == doc.records[requirement.id].fields["md"]
                        for r in receipts
                    ) and graph.proof_scope(doc, [candidate, requirement.id]) <= covered
                if not usable:
                    outstanding.append(requirement.id)
            outputs.append({"output": output.id, "task": task.id, "task_status": task.fields["st"].value,
                            "nominee": candidate, "requires_review": outstanding,
                            "retrieve": {"tool": "pixl_context", "arguments": {"path": state, "focus": task.id}},
                            "candidate_review": {"tool": "pixl_review_context", "arguments": {"path": state, "candidate_id": candidate}} if candidate else None})
    return {"outputs": outputs, "failures_obsolete_or_stale": history,
            "limit": "Saved nominations/verdicts and receipt freshness only; this comparison creates no acceptance and never transfers predecessor reviews."}


def report(root, state, plan_id, against_plan, job=None, comparison=None):
    root = Path(root).resolve()
    path = graph.confined(root, state)
    production_plan._require(path.name == "state.px", "review needs store state.px")
    doc = store.load(path.parent)
    if not against_plan or plan_id == against_plan:
        raise PixlError("request_review", "changes view needs a distinct explicit against_plan")
    old_marker, before = _plan(root, doc, against_plan)
    new_marker, after = _plan(root, doc, plan_id)
    production_plan._require(before["plan"]["project"] == after["plan"]["project"], "plans must belong to the same project")
    old = production_review.report(root, state, against_plan)
    new = production_review.report(root, state, plan_id, job, comparison)
    old_criteria, new_criteria = _criteria(before), _criteria(after)
    criteria = _delta(old_criteria, new_criteria)
    for category in ("added", "removed", "changed"):
        for row in criteria[category]:
            stage, criterion = row["key"].split("/", 1)
            for side, snapshot, full in (("before", before, old), ("after", after, new)):
                if side in row:
                    ident = snapshot["plan"]["id"] + "." + stage + ".q." + criterion
                    exact = next(q for q in full["criteria"] if q["id"] == ident)
                    # The compact view names the exact delta; literal clauses stay
                    # in the unchanged full report, not shortened paraphrases.
                    row[side].pop("check")
                    row[side].update(id=ident, record_sha256=exact["record_sha256"], record_status=exact["record_status"],
                                     literal_check="Retrieve this exact ID from the full report")

    def selections(snapshot):
        return {s["selection"]["path"] + ":" + s["selection"]["asset"]: s["selection"]
                for s in snapshot["plan"]["stages"] if "selection" in s}

    def controls(snapshot):
        plan = snapshot["plan"]
        return {"shared": {k: plan[k] for k in ("baseline", "decisions", "knowledge")},
                **{s["id"]: {k: v for k, v in s.items() if k not in ("criteria", "selection", "name", "id")}
                   for s in [*plan["stages"], {"id": "delivery", **plan["delivery"]}]}}

    def sources(full, marker):
        return {s["id"]: {"record_sha256": marker.fields["mt"]["scope"].get(s["id"]),
                           "current_record_sha256": s.get("record_sha256"),
                           "current_path": s.get("path"), "status": s["status"],
                           "record_status": s.get("record_status", "current")}
                for s in full["sources"]}

    changes = {"criteria": criteria, "sources": _delta(sources(old, old_marker), sources(new, new_marker)),
               "choices": _delta(_bound(doc, old_marker, {"I"}), _bound(doc, new_marker, {"I"})),
               "contracts": _delta(_bound(doc, old_marker, {"C"}), _bound(doc, new_marker, {"C"})),
               "selections": _delta(selections(before), selections(after)),
               "controls": _delta(controls(before), controls(after))}
    def asset(snapshot, key):
        stages = {s["id"] for s in snapshot["plan"]["stages"] if "selection" in s
                  and s["selection"]["path"] + ":" + s["selection"]["asset"] == key}
        return next((value["asset"] for stage, value in snapshot["selections"].items() if stage in stages), {})

    for change in changes["selections"]["changed"]:
        left, right = asset(before, change["key"]), asset(after, change["key"])
        change["changed_asset_fields"] = sorted(k for k in left.keys() | right.keys()
                                               if k not in ("status", "next", "evidence", "production") and left.get(k) != right.get(k))
    result = {
        "version": 1, "kind": "production_plan_changes", "view": "changes", "state": new["state"],
        "before": {"plan": old["plan"], "review_scope_sha256": old["review_scope_sha256"],
                   "retrieve": {"tool": "pixl_request_review", "arguments": {"packet": state, "plan": against_plan}}},
        "after": {"plan": new["plan"], "review_scope_sha256": new["review_scope_sha256"],
                  "retrieve": {"tool": "pixl_request_review", "arguments": {"packet": state, "plan": plan_id, **({"job": job} if job else {}), **({"comparison": comparison} if comparison else {})}}},
        "counts": {name: {kind: len(rows) for kind, rows in delta.items()} for name, delta in changes.items()},
        "changes": changes,
        "criterion_index": {"before": [{"id": q["id"], "record_sha256": q["record_sha256"]} for q in old["criteria"]],
                            "after": [{"id": q["id"], "record_sha256": q["record_sha256"]} for q in new["criteria"]]},
        "retained_choices": [{"id": key, **_bound(doc, new_marker, {"I"})[key]} for key in changes["choices"]["unchanged"]],
        "review_attention": {"before": _reviews(doc, root, state, before), "after": _reviews(doc, root, state, after)},
        "diagnostics": {"before": old["diagnostics"], "after": new["diagnostics"]},
        "comparison_coverage": new["comparison_coverage"],
        "request": {key: new["request"][key] for key in ("id", "state", "intent_sha256", "blockers", "next_action")} if new["request"] else None,
        "consistent": None, "caller_comparison": "unperformed",
        "scope": "Structural comparison of explicitly selected plans in one store, not an assertion of direct succession or semantic equivalence. Criteria align only by exact stage and local criterion IDs; renamed clauses remain added/removed. Literal check text is deliberately in the exact full reports, never truncated or paraphrased here. Every criterion ID/hash stays indexed. Retained plan paths expose original allocation snapshots; current selection drift stays diagnostic. Missing historical declarations are not reconstructed. No state, adoption or acceptance changes.",
    }
    result["comparison_sha256"] = platform._sha(result)
    return result
