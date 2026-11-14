"""A source-linked authoring index, separate from the complete wire closure."""

from pathlib import Path
from urllib.parse import urlsplit

from . import adapter_versions, codec, graph, jobs, plar, retention, store
from .codec import PixlError


def report(path, focus, root, plar_path=None, asset_id=None):
    """Expose current planning records without expanding proof or job history.

    This is orientation, not validation, acceptance or an abbreviated wire packet.
    Sources retain exact retrieval arguments and criteria retain their literal text.
    """
    root = Path(root).resolve()
    path = Path(path).resolve()
    if not path.is_relative_to(root) or path.name != "state.px":
        raise PixlError("authoring_context", "use a project-confined store/state.px")
    doc = store.load(path.parent)
    graph.validate(doc)
    if doc.format != 2 or focus not in doc.records:
        raise PixlError("authoring_context", "focus must identify a PX2 record")
    if (plar_path is None) != (asset_id is None):
        raise PixlError("authoring_context", "supply both plar_path and asset_id")
    state = path.relative_to(root).as_posix()
    records = doc.records
    tasks, outputs, plans = set(), set(), set()
    selected = records[focus]
    if selected.kind == "T":
        tasks.add(focus)
    elif selected.kind == "F":
        outputs.add(focus)
    elif selected.kind == "X" and adapter_versions.is_binding(selected.fields.get("mt", {}).get("binding"), "pixl.production.plan"):
        adapter_versions.require_binding(selected.fields["mt"]["binding"], "pixl.production.plan")
        plans.add(focus)
    else:
        raise PixlError("authoring_context", "focus on a task, output or connected plan")

    # Expand only parents of the initial focus. A reused baseline must not pull
    # every historical family that also used that output into this view.
    outputs.update(r.id for t in tasks for r in records[t].fields["op"])
    tasks.update(records[f].fields["tk"].id for f in outputs)
    seed_tasks, seed_outputs = set(tasks), set(outputs)
    seed_inputs = {ref.id for task in seed_tasks for ref in records[task].fields["ip"]}
    for record in records.values():
        if record.kind == "F" and seed_outputs.intersection(r.id for r in record.fields.get("mb", [])):
            outputs.add(record.id)
        if record.kind == "X" and adapter_versions.is_binding(record.fields.get("mt", {}).get("binding"), "pixl.production.plan"):
            saved_tasks = record.fields["mt"].get("tasks", {})
            plan_tasks = set(saved_tasks) if isinstance(saved_tasks, dict) else set()
            if record.id in plans or record.id in seed_inputs or seed_tasks & plan_tasks:
                adapter_versions.require_binding(record.fields["mt"]["binding"], "pixl.production.plan")
                if not isinstance(saved_tasks, dict):
                    raise PixlError("authoring_context", "connected plan metadata needs saved tasks")
                plans.add(record.id)
                tasks.update(plan_tasks)
    outputs.update(r.id for t in tasks for r in records[t].fields["op"])
    authored_outputs = set(outputs)
    tasks.update(records[f].fields["tk"].id for f in authored_outputs)
    frontier = list(outputs)
    while frontier:
        for ref in records[frontier.pop()].fields.get("mb", []):
            if ref.id not in outputs:
                outputs.add(ref.id)
                frontier.append(ref.id)

    diagnostics = []

    def row(ident, omit=()):
        record = records[ident]
        return {
            "id": ident, "kind": record.kind,
            "record_sha256": codec.record_hash(record),
            "fields": codec.to_data({k: v for k, v in record.fields.items() if k not in omit}),
            "omitted_fields": list(omit),
        }

    def files(ident):
        record = records[ident]
        value = row(ident, ("mt",))
        if urlsplit(record.fields["ur"]).scheme in ("http", "https"):
            value["file_status"] = "remote_unverified"
        else:
            local = graph.confined(root, record.fields["ur"])
            actual = graph.file_hash(local) if local.is_file() else None
            value.update(observed_sha256=actual, file_status=(
                "current" if actual == record.fields["dg"] else "missing" if actual is None else "changed"
            ))
        return value

    prerequisites = ({r.id for t in tasks for r in records[t].fields["dp"]}
                     | {records[f].fields["tk"].id for f in outputs}) - tasks
    projects = {records[t].fields["pr"].id for t in tasks}
    contracts = {records[f].fields["ct"].id for f in outputs if "ct" in records[f].fields}
    criteria = {r.id for f in authored_outputs for r in records[f].fields["rq"]}
    decisions = {r.id for t in tasks for r in records[t].fields["dc"]}
    knowledge = {r.id for t in tasks for r in records[t].fields["kn"]}
    artifacts = {r.id for t in tasks | prerequisites for k in ("ip", "ca") for r in records[t].fields[k]}
    artifacts.update(records[f].fields["bs"].id for f in outputs if "bs" in records[f].fields)
    artifacts -= plans
    # Follow declared semantic links, including F.ds and transitive D.wr/I.vl
    # authority. Never expand P.in through ownership or historical E/T/V links.
    semantic = graph.proof_scope(doc, sorted(outputs | contracts | criteria | decisions | knowledge | artifacts))
    choices = {ident for ident in semantic if records[ident].kind == "I"}
    other_choices = {r.id for p in projects for r in records[p].fields["in"]} - choices
    source_ids = {
        ref for ident in semantic
        for ref in graph.refs(records[ident].fields) if records[ref].kind == "S"
    }
    sources = []
    for ident in sorted(source_ids):
        record = records[ident]
        fields = record.fields
        entry = {"id": ident, "record_sha256": codec.record_hash(record),
                 "source_class": fields["au"].value, "observed_at": fields["at"]}
        if urlsplit(fields["ur"]).scheme in ("http", "https"):
            entry["file_status"] = "remote_unverified"
            entry["binding"] = codec.to_data(fields)
        else:
            local = retention.resolve(root, fields["ur"], fields["dg"])
            actual = graph.file_hash(local) if local.is_file() else None
            entry.update(observed_sha256=actual, file_status=(
                "current" if actual == fields["dg"] else "missing" if actual is None else "changed"
            ))
            entry["retrieve"] = {"tool": "pixl_source", "arguments": {
                "path": fields["ur"], "expect": fields["dg"],
                "start": fields["ln"][0], "end": fields["ln"][1], "scope": "project",
            }}
        sources.append(entry)
    job_rows = []
    for record in sorted(records.values(), key=lambda r: r.id):
        if record.kind != "J" or record.fields["tk"].id not in tasks:
            continue
        try:
            journal = jobs._get(doc, record.id, root) if "jr" in record.fields else None
            summary = jobs._summary(doc, record, journal, root, path.parent)
            job_rows.append({k: v for k, v in summary.items() if k not in {"request", "context", "events"}} | {
                "task": record.fields["tk"].id,
                "request_tool": summary.get("request", {}).get("tool"),
                "journal": row(record.fields["jr"].id) if "jr" in record.fields else None,
                "retrieve": {"tool": "pixl_jobs", "arguments": {"path": state}},
            })
        except (PixlError, OSError) as error:
            diagnostics.append({"job": record.id, "status": "unavailable", "reason": str(error)})
    plan_rows = []
    for ident in sorted(plans):
        value = files(ident)
        value["request_review"] = {"packet": state, "plan": ident}
        value["jobs"] = [j["id"] for j in job_rows if j["task"] in records[ident].fields["mt"]["tasks"]]
        plan_rows.append(value)
    selection = None
    if asset_id is not None:
        selected_plar = plar.read(root, plar_path, asset_id, include_production=False)
        selection = {k: selected_plar[k] for k in (
            "path", "hash", "requirements_hash", "sources", "dependency_issues", "queue",
        )}
        selection["requirements"] = plar._requirements(selected_plar["asset"])
        selection["dependencies"] = [
            {k: a[k] for k in ("id", "purpose", "status", "questions", "issues")}
            | {"retrieve": {"tool": "pixl_plar_read", "arguments": {"path": plar_path, "asset_id": a["id"]}}}
            for a in selected_plar["dependencies"]
        ]
        selection["retrieve"] = {"tool": "pixl_plar_read", "arguments": {"path": plar_path, "asset_id": asset_id}}
    return {
        "view": "authoring", "path": state, "focus": focus,
        "hash": codec.digest(doc), "revision": doc.revision,
        "scope": "Connected plans and enclosing families; direct prerequisites and current nominees. Criteria cover the focused plan/tasks and enclosing delivery, not reused members' historic acceptance. No historical verdicts, proof receipts, embedded artifact metadata or provider payloads. Not a complete context packet or acceptance judgment. Source class does not establish requirement authority.",
        "complete_context": {"tool": "pixl_context", "arguments": {"path": state, "focus": focus}},
        "projects": [row(i, ("sc", "in")) for i in sorted(projects)],
        "tasks": [row(i, ("vr",)) for i in sorted(tasks)],
        "prerequisites": [row(i, ("vr",)) for i in sorted(prerequisites)],
        "outputs": [row(i) for i in sorted(outputs)],
        "contracts": [row(i) for i in sorted(contracts)],
        "choices": [row(i) for i in sorted(choices)],
        "choice_scope": {
            "basis": "Explicit semantic links from selected outputs, contracts, decisions, knowledge and current inputs/nominees, including family destinations. No text/key matching or inferred authority.",
            "other_intake": [{"id": i, "key": records[i].fields["ky"],
                              "status": records[i].fields["st"].value,
                              "retrieve": {"tool": "pixl_context", "arguments": {"path": state, "focus": i}}}
                             for i in sorted(other_choices)],
            "limit": "Unlinked does not mean irrelevant. Inspect an indexed choice when its applicability is uncertain; preserve global caller instructions. This index changes no saved choice or acceptance rule.",
        },
        "decisions": [row(i) for i in sorted(decisions)],
        "knowledge": [row(i, ("op", "ck", "pc")) for i in sorted(knowledge)],
        "criteria": [row(i) for i in sorted(criteria)],
        "sources": sources, "artifacts": [files(i) for i in sorted(artifacts)],
        "plans": plan_rows, "jobs": job_rows, "selection": selection,
        "diagnostics": diagnostics, "consistent": None,
    }
