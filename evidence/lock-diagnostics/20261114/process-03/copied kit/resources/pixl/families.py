"""Pure PX2 baseline, family membership and delivery readiness interpretation.

Shared graph validation owns schema, references and current acceptance proof.
This module interprets already checked records without file I/O or mutation.
Snapshot bytes, historical plans and publication rules belong to delivery.
"""

from .codec import PixlError, record_hash

PENDING_STATES = {"prepared", "unknown", "submitted", "running"}


def _require(condition, code, detail):
    if not condition:
        raise PixlError(code, detail)


def _ids(references):
    return [reference.id for reference in references]


def _family(doc, output_id):
    output = doc.records.get(output_id)
    _require(
        doc.format == 2 and output is not None and output.kind == "F"
        and {"bs", "mb", "ds"} <= output.fields.keys(),
        "family_output", f"{output_id} is not a family delivery output",
    )
    return output.fields


def _nominee(doc, output_id):
    output = doc.records[output_id].fields
    task = doc.records[output["tk"].id].fields
    return next((
        candidate.id for candidate in task["ca"]
        if doc.records[candidate.id].fields.get("of") is not None
        and doc.records[candidate.id].fields["of"].id == output_id
    ), None)


def _baseline(doc, output_id):
    candidate_id = doc.records[output_id].fields["bs"].id
    candidate = doc.records[candidate_id].fields
    sample_output = candidate["of"].id
    task_id = doc.records[sample_output].fields["tk"].id
    task = doc.records[task_id].fields
    reasons = []
    if _nominee(doc, sample_output) != candidate_id:
        reasons.append(f"family_baseline: {output_id} baseline {candidate_id} is not the current sample nominee")
    if task["st"].value != "done":
        reasons.append(f"family_baseline: {output_id} baseline task {task_id} is {task['st'].value}; it must be done")
    return {"candidate": candidate_id, "output": sample_output, "task": task_id,
            "eligible": not reasons, "reasons": reasons}


def validate(doc):
    """Validate opt-in relationships after shared schema checks, before lifecycle.

    Old documents without these fields retain their previous interpretation.
    A historical manifest's xs is deliberately not compared with current mb;
    delivery validation checks that projection against its frozen saved plan.
    """
    if doc.format != 2:
        return
    for output_id, record in doc.records.items():
        if record.kind != "F":
            continue
        output = record.fields
        family = "mb" in output or "ds" in output
        if family:
            _require({"bs", "mb", "ds"} <= output.keys(), "family_fields",
                     f"{output_id}: a family requires bs, mb and ds together")
            _require(output["kd"].value == "report", "family_kind",
                     f"{output_id}: a family delivery output must be report kind")
            _require("ct" not in output, "family_contract",
                     f"{output_id}: a family manifest cannot carry a raster contract")
        if "bs" not in output:
            continue
        task_id = output["tk"].id
        task = doc.records[task_id].fields
        _require(task["ph"].value in {"production", "delivery"}, "family_phase",
                 f"{output_id}: baseline outputs require production or delivery phase")
        baseline_id = output["bs"].id
        baseline = doc.records[baseline_id].fields
        _require("of" in baseline, "family_baseline_owner",
                 f"{output_id}: baseline {baseline_id} needs an owning sample output")
        sample_output_id = baseline["of"].id
        sample_output = doc.records[sample_output_id].fields
        sample_task_id = sample_output["tk"].id
        sample_task = doc.records[sample_task_id].fields
        _require(sample_task["ph"].value == "sample" and sample_task_id != task_id,
                 "family_baseline_owner", f"{output_id}: baseline must belong to another sample task")
        _require(sample_task["pr"] == task["pr"], "family_project",
                 f"{output_id}: baseline belongs to another project")
        _require(baseline_id in _ids(task["ip"]), "family_baseline_input",
                 f"{output_id}: baseline {baseline_id} must be a task input")
        _require(sample_task_id in _ids(task["dp"]), "family_prerequisite",
                 f"{output_id}: sample task {sample_task_id} must be a direct prerequisite")
        if not family:
            continue
        _require(task["ph"].value == "delivery", "family_phase",
                 f"{output_id}: a family output requires a delivery task")
        members = _ids(output["mb"])
        _require(bool(members) and len(members) == len(set(members)), "family_members",
                 f"{output_id}: members must be nonempty, distinct and ordered")
        for member_id in members:
            member = doc.records[member_id].fields
            _require(member_id != output_id and not {"mb", "ds"} & member.keys(),
                     "family_members", f"{output_id}: nested or self member {member_id}")
            owner_id = member["tk"].id
            owner = doc.records[owner_id].fields
            _require(owner["pr"] == task["pr"], "family_project",
                     f"{output_id}: member {member_id} belongs to another project")
            _require(owner_id in _ids(task["dp"]), "family_prerequisite",
                     f"{output_id}: member task {owner_id} must be a direct prerequisite")
            _require(member_id == sample_output_id or (
                owner["ph"].value == "production" and member.get("bs") == output["bs"]
            ), "family_member_baseline",
                f"{output_id}: member {member_id} must be the baseline output or production with the same baseline")
        destinations = _ids(output["ds"])
        _require(bool(destinations) and len(destinations) == len(set(destinations)),
                 "family_destinations", f"{output_id}: destinations must be nonempty and distinct")
        for destination_id in destinations:
            _require(doc.records[destination_id].fields["pr"] == task["pr"],
                     "family_project", f"{output_id}: destination {destination_id} belongs to another project")
        _require(any(doc.records[q.id].fields["dm"].value == "continuity" for q in output["rq"]),
                 "family_continuity", f"{output_id}: family delivery requires a continuity criterion")

    for candidate_id, record in doc.records.items():
        if record.kind != "X":
            continue
        candidate = record.fields
        output_ref = candidate.get("of")
        output = doc.records[output_ref.id].fields if output_ref is not None else {}
        if {"mb", "ds"} & output.keys():
            _require("xs" in candidate, "family_candidate",
                     f"{candidate_id}: a family report candidate must retain its typed constituents")
        if "xs" not in candidate:
            continue
        _require(candidate["kd"].value == "report" and {"bs", "mb", "ds"} <= output.keys(),
                 "family_candidate", f"{candidate_id}: xs belongs only to family report candidates")
        _require(bool(candidate["xs"]) and candidate_id not in _ids(candidate["xs"]),
                 "family_candidate", f"{candidate_id}: constituents must be nonempty and cannot include itself")


def blockers(doc, task_id):
    """Return only family activation blockers; never call lifecycle recursively."""
    if doc.format != 2:
        return []
    _require(task_id in doc.records and doc.records[task_id].kind == "T", "unknown_task", task_id)
    reasons = []
    for reference in doc.records[task_id].fields["op"]:
        output = doc.records[reference.id].fields
        if "bs" in output:
            reasons.extend(_baseline(doc, reference.id)["reasons"])
        for destination_ref in output.get("ds", []):
            destination = doc.records[destination_ref.id].fields
            if destination["st"].value != "confirmed":
                reasons.append(f"family_destination: {destination_ref.id} is {destination['st'].value}; confirm it before delivery")
    return reasons


def plan(doc, output_id):
    """Return ordered saved planning identities and sorted semantic hash bindings."""
    from .graph import proof_scope

    output = _family(doc, output_id)
    return {
        "output": output_id, "task": output["tk"].id, "baseline": output["bs"].id,
        "members": _ids(output["mb"]), "destinations": _ids(output["ds"]),
        "bindings": {id_: record_hash(doc.records[id_]) for id_ in sorted(proof_scope(doc, [output_id]))},
    }


def selection(doc, output_id):
    """Return each member's current nominee, in saved membership order."""
    return [_nominee(doc, member.id) for member in _family(doc, output_id)["mb"]]


def _member_reasons(doc, output_id, candidate_id):
    task_id = doc.records[output_id].fields["tk"].id
    state = doc.records[task_id].fields["st"].value
    reasons = []
    if candidate_id is None:
        reasons.append(f"family_member: {output_id} has no nominated candidate")
    if state != "done":
        reasons.append(f"family_member: {output_id} task {task_id} is {state}; it must be done")
    return reasons


def _pending_jobs(doc, output_id):
    output = _family(doc, output_id)
    tasks = {output["tk"].id, _baseline(doc, output_id)["task"]}
    tasks.update(doc.records[member.id].fields["tk"].id for member in output["mb"])
    return [
        {"id": id_, "task": record.fields["tk"].id, "state": record.fields["si"].value}
        for id_, record in sorted(doc.records.items())
        if record.kind == "J" and record.fields["tk"].id in tasks
        and record.fields["si"].value in PENDING_STATES
    ]


def snapshot_blockers(doc, output_id):
    """Require accepted inputs and settled jobs, independently of delivery checks."""
    output = _family(doc, output_id)
    state = doc.records[output["tk"].id].fields["st"].value
    reasons = []
    if state not in {"open", "active"}:
        reasons.append(f"family_state: {output['tk'].id} is {state}; snapshots require an open or active task")
    reasons.extend(_baseline(doc, output_id)["reasons"])
    for member, candidate in zip(output["mb"], selection(doc, output_id), strict=True):
        reasons.extend(_member_reasons(doc, member.id, candidate))
    for job in _pending_jobs(doc, output_id):
        reasons.append(f"family_job: {job['id']} for {job['task']} is {job['state']}; reconcile existing work before snapshot")
    return reasons


def describe(doc, output_id):
    """Describe acceptance observations without file I/O, validation or mutation."""
    from . import lifecycle

    output = _family(doc, output_id)
    workflow = lifecycle.report(doc)
    tasks = {task["id"]: task for task in workflow["tasks"]}
    outputs = {item["id"]: item for task in tasks.values() for item in task["outputs"]}
    intake = {choice["id"]: choice for choice in workflow["intake"]}
    baseline = _baseline(doc, output_id)
    baseline["requirements"] = next(
        candidate["requirements"] for candidate in outputs[baseline["output"]]["candidates"]
        if candidate["id"] == baseline["candidate"]
    )
    members = []
    for reference in output["mb"]:
        item = outputs[reference.id]
        owner = doc.records[reference.id].fields["tk"].id
        reasons = _member_reasons(doc, reference.id, item["candidate"])
        members.append({
            "output": reference.id, "task": owner, "state": tasks[owner]["state"],
            "candidate": item["candidate"], "accepted": not reasons, "reasons": reasons,
            "requirements": item["requirements"], "candidates": item["candidates"],
        })
    task = tasks[output["tk"].id]
    current = outputs[output_id]
    return {
        "output": output_id, "task": task["id"], "state": task["state"], "baseline": baseline,
        "destinations": [intake[reference.id] for reference in output["ds"]], "members": members,
        "candidate": current["candidate"], "requirements": current["requirements"],
        "candidates": current["candidates"], "blockers": task["blockers"],
        "snapshot_blockers": snapshot_blockers(doc, output_id), "pending_jobs": _pending_jobs(doc, output_id),
    }
