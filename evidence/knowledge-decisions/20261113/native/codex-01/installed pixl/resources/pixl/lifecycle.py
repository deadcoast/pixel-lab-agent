"""PX2 intake, planned outputs, candidate acceptance and read-only readiness.

The graph module owns wire/schema, reference, file and evidence-hash validation.
This module runs after those checks. Reports consume an already validated graph
and never create evidence, advance tasks or recursively invoke validation.
"""

from datetime import datetime

from .codec import PixlError, encode_value, to_data

NONRASTER = {"code", "report", "reference"}
CONTRACT_FIELDS = {"nm", "px", "pl", "vw", "sa", "al", "li", "ch", "tg"}
ADOPTION_PHASES = {"production", "delivery"}


def _require(condition, code, detail):
    if not condition:
        raise PixlError(code, detail)


def _ids(references):
    return {reference.id for reference in references}


def _unique(references, code, detail):
    _require(len(_ids(references)) == len(references), code, detail)


def _output_choices(doc, task):
    """Only output contracts impose a task's own project/style obligations.

    A source input may intentionally belong to another project or contract.
    Unrelated project choices also do not gate research or accepted samples.
    """
    choices = set()
    for output in task["op"]:
        contract = doc.records[output.id].fields.get("ct")
        if contract is not None:
            choices.update(_ids(doc.records[contract.id].fields.get("ch", [])))
    return choices


def _activation_blockers(doc, task_id, scope, bound):
    from . import families

    task = doc.records[task_id].fields
    reasons = []
    for dependency in task["dp"]:
        state = doc.records[dependency.id].fields["st"].value
        if state != "done":
            reasons.append(f"task_prerequisite: {dependency.id} is {state}; it must be done")
    for reference in task["op"]:
        output = doc.records[reference.id].fields
        if output["kd"].value not in NONRASTER and "ct" not in output:
            reasons.append(f"output_contract: {reference.id} needs a concrete raster contract")
    choice_ids = sorted(_output_choices(doc, task))
    for choice_id in choice_ids:
        choice = doc.records[choice_id].fields
        state = choice["st"].value
        if state in {"unresolved", "conflict"}:
            reasons.append(
                f"choice_{state}: {choice_id} ({choice['ky']}) is {state}; resolve it before active work"
            )
    if task["ph"].value in ADOPTION_PHASES:
        if not task["dc"]:
            reasons.append(f"task_decision: {task_id} needs an evidence-backed adoption decision")
        for reference in task["kn"]:
            method = doc.records[reference.id].fields
            if not scope(reference.id) <= bound(method.get("pc", []), passing=True):
                reasons.append(f"method_poc: {reference.id} needs current passing method proof")
        for choice_id in choice_ids:
            choice = doc.records[choice_id].fields
            if choice["st"].value in {"observed", "proposed"}:
                reasons.append(f"choice_unconfirmed: {choice_id} ({choice['ky']}) must be confirmed")
    reasons.extend(families.blockers(doc, task_id))
    return reasons


def validate(doc, scope, bound):
    """Validate PX2 semantics after the graph's shared checks.

    ``scope(id)`` returns the semantic proof closure. ``bound(refs, passing)``
    returns IDs bound by current receipts. Both are supplied by graph.validate
    so lifecycle checks use precisely the same evidence interpretation.
    """
    choice_keys = set()
    current_verdicts = {}

    for id_, record in doc.records.items():
        f = record.fields
        if record.kind == "P":
            _unique(f["in"], "intake_project", f"{id_}.in repeats a choice")
            for choice in f["in"]:
                _require(
                    doc.records[choice.id].fields["pr"].id == id_,
                    "intake_project", f"{id_}.in includes another project's choice {choice.id}",
                )
        elif record.kind == "I":
            project_id = f["pr"].id
            _require(
                id_ in _ids(doc.records[project_id].fields["in"]),
                "intake_project", f"{id_} must be listed in {project_id}.in",
            )
            choice_key = (project_id, f["ky"])
            _require(
                bool(f["ky"].strip()) and choice_key not in choice_keys,
                "intake_key", f"{id_}: choice keys must be nonempty and unique within a project",
            )
            choice_keys.add(choice_key)
            state, value = f["st"].value, f["vl"]
            if state == "unresolved":
                _require(value is None, "intake_value", f"{id_}: unresolved value must be null")
            elif state == "conflict":
                _require(
                    isinstance(value, list) and len(value) >= 2,
                    "intake_value", f"{id_}: conflict needs at least two alternatives",
                )
            else:
                _require(value is not None, "intake_value", f"{id_}: {state} value cannot be null")
            if state in {"observed", "confirmed"}:
                _require(bool(f["so"]), "intake_source", f"{id_}: {state} choice needs sources")
            if state == "proposed":
                _require(bool(f["wy"].strip()), "intake_rationale", f"{id_}: proposal needs a rationale")
        elif record.kind == "C":
            _unique(f.get("ch", []), "contract_choice", f"{id_}.ch repeats a choice")
            for reference in f.get("ch", []):
                choice = doc.records[reference.id].fields
                # Retain the last interpretation while an open/blocked task
                # resolves changed intent. Activation is gated separately.
                if choice["st"].value in {"unresolved", "conflict"}:
                    continue
                key = choice["ky"]
                if key in CONTRACT_FIELDS:
                    _require(
                        key in f and encode_value(choice["vl"]) == encode_value(f[key]),
                        "contract_choice", f"{id_}.{key} does not equal choice {reference.id}",
                    )
        elif record.kind == "F":
            owner = doc.records[f["tk"].id].fields
            _require(id_ in _ids(owner["op"]), "output_owner", f"{id_} must be listed by its owning task")
            _require(bool(f["rq"]), "output_requirements", f"{id_} needs at least one acceptance criterion")
            _unique(f["rq"], "output_requirements", f"{id_}.rq repeats a criterion")
        elif record.kind == "Q":
            _require(bool(f["ck"].strip()), "criterion_check", f"{id_} needs an observable check")
            required_mode = {"visual": "visual", "engine": "live"}.get(f["dm"].value)
            _require(
                required_mode is None or f["md"].value == required_mode,
                "criterion_mode", f"{id_}: {f['dm'].value} requires {required_mode} evidence",
            )
        elif record.kind == "X":
            _require(
                f["kd"].value in NONRASTER or "ct" in f,
                "artifact_contract", f"{id_}: a materialized raster needs a contract",
            )
            if "of" in f:
                output = doc.records[f["of"].id].fields
                _require(
                    f["kd"] == output["kd"] and f.get("ct") == output.get("ct"),
                    "candidate_output", f"{id_} must match its planned output's kind and contract",
                )
        elif record.kind == "V":
            task = doc.records[f["tk"].id].fields
            _require(id_ in _ids(task["vr"]), "verdict_owner", f"{id_} must remain in its task's verdict history")
            candidate = doc.records[f["xr"].id].fields
            output_ref = candidate.get("of")
            _require(output_ref is not None, "verdict_owner", f"{id_}: candidate has no planned output")
            output = doc.records[output_ref.id].fields
            _require(
                output["tk"] == f["tk"] and output_ref.id in _ids(task["op"]),
                "verdict_owner", f"{id_}: candidate belongs to another task",
            )
            try:
                datetime.fromisoformat(f["at"])
            except ValueError as error:
                raise PixlError("date", id_) from error
            if f["st"].value == "unavailable":
                _require(bool(f["wy"].strip()), "verdict_reason", f"{id_}: explain the unavailable inspection")
                _require(not f["ev"], "verdict_unavailable", f"{id_}: unavailable verdict must have no receipts")
            if f.get("ob", False):
                continue
            _require(
                f["rq"].id in _ids(output["rq"]),
                "verdict_requirement", f"{id_}: criterion is not required by this candidate's output",
            )
            verdict_key = (f["tk"].id, f["xr"].id, f["rq"].id)
            _require(verdict_key not in current_verdicts, "verdict_duplicate", f"{id_}: supersede the previous verdict first")
            current_verdicts[verdict_key] = record
            if f["st"].value != "unavailable":
                current = [e for e in f["ev"] if not doc.records[e.id].fields.get("ob", False)]
                criterion = doc.records[f["rq"].id].fields
                _require(bool(current), "verdict_evidence", f"{id_}: pass/fail needs current receipts")
                _require(
                    all(doc.records[e.id].fields["rs"] == f["st"]
                        and doc.records[e.id].fields["md"] == criterion["md"] for e in current),
                    "verdict_evidence", f"{id_}: receipts must match the verdict outcome and criterion mode",
                )
                _require(
                    scope(f["xr"].id) | scope(f["rq"].id) <= bound(current),
                    "verdict_proof", f"{id_}: receipts must bind the exact candidate, criterion and their semantic scopes",
                )

    for id_, record in doc.records.items():
        if record.kind != "T":
            continue
        f = record.fields
        _unique(f["op"], "output_owner", f"{id_}.op repeats a planned output")
        _unique(f["vr"], "verdict_owner", f"{id_}.vr repeats a verdict")
        for reference in f["op"]:
            _require(
                doc.records[reference.id].fields["tk"].id == id_,
                "output_owner", f"{id_}: {reference.id} belongs to another task",
            )
        for reference in f["vr"]:
            _require(
                doc.records[reference.id].fields["tk"].id == id_,
                "verdict_owner", f"{id_}: {reference.id} belongs to another task",
            )
        for choice_id in _output_choices(doc, f):
            _require(
                doc.records[choice_id].fields["pr"] == f["pr"],
                "task_project", f"{id_}: output choice {choice_id} belongs to another project",
            )
        nominees = {}
        for reference in f["ca"]:
            candidate = doc.records[reference.id].fields
            output = candidate.get("of")
            _require(
                output is not None and output.id in _ids(f["op"]),
                "candidate_output", f"{id_}: nominated {reference.id} must belong to a planned output",
            )
            _require(
                output.id not in nominees, "candidate_nomination",
                f"{id_}: only one candidate may be nominated for {output.id}",
            )
            nominees[output.id] = reference.id
        if f["st"].value in {"active", "done"}:
            reasons = _activation_blockers(doc, id_, scope, bound)
            if reasons:
                code, detail = reasons[0].split(": ", 1)
                raise PixlError(code, detail)
        if f["st"].value == "done":
            _require(
                bool(f["op"]) and set(nominees) == _ids(f["op"]),
                "completion", f"{id_}: every planned output needs one nominated candidate",
            )
            for output_id, candidate_id in nominees.items():
                for requirement in doc.records[output_id].fields["rq"]:
                    verdict = current_verdicts.get((id_, candidate_id, requirement.id))
                    status = verdict.fields["st"].value if verdict is not None else "unperformed"
                    _require(
                        status == "pass", "completion",
                        f"{id_}: {candidate_id} requirement {requirement.id} is {status}",
                    )
    return doc


def blockers(doc, task_id):
    """Return activation blockers for a task in an otherwise valid PX2 graph."""
    from .graph import proof_scope

    _require(task_id in doc.records and doc.records[task_id].kind == "T", "unknown_task", task_id)

    def bound(evidence, passing=False):
        covered: set[str] = set()
        for reference in evidence:
            receipt = doc.records[reference.id].fields
            if not receipt.get("ob", False) and (not passing or receipt["rs"].value == "pass"):
                covered.update(binding["rf"].id for binding in receipt["bs"])
        return covered

    return _activation_blockers(doc, task_id, lambda id_: proof_scope(doc, [id_]), bound)


def report(doc):
    """Describe an already validated PX2 graph without changing its state.

    Requirements are shown for each current nominee and for retained older
    candidates. An absent current verdict is unperformed, never a pass.
    """
    intake, tasks, ready = [], [], []
    current = {
        (r.fields["tk"].id, r.fields["xr"].id, r.fields["rq"].id): r
        for r in doc.records.values() if r.kind == "V" and not r.fields.get("ob", False)
    }
    candidates: dict[str, list[str]] = {}
    for id_, record in sorted(doc.records.items()):
        if record.kind == "X" and "of" in record.fields:
            candidates.setdefault(record.fields["of"].id, []).append(id_)

    def requirements(task_id, output, candidate_id):
        results = []
        for reference in output["rq"]:
            criterion = doc.records[reference.id].fields
            verdict = current.get((task_id, candidate_id, reference.id))
            results.append({
                "id": reference.id, "name": criterion["nm"],
                "check": criterion["ck"],
                "domain": criterion["dm"].value, "mode": criterion["md"].value,
                "status": verdict.fields["st"].value if verdict is not None else "unperformed",
                "verdict": verdict.id if verdict is not None else None,
                "reason": verdict.fields["wy"] if verdict is not None else None,
                "reviewer": verdict.fields["wh"].id if verdict is not None else None,
                "evidence": [e.id for e in verdict.fields["ev"]] if verdict is not None else [],
            })
        return results

    for id_, record in sorted(doc.records.items()):
        f = record.fields
        if record.kind == "I":
            intake.append({
                "id": id_, "project": f["pr"].id, "key": f["ky"],
                "status": f["st"].value, "value": to_data(f["vl"]),
                "sources": [s.id for s in f["so"]], "rationale": f["wy"],
            })
        elif record.kind == "T":
            reasons = blockers(doc, id_)
            if f["st"].value == "open" and not reasons:
                ready.append(id_)
            nominees = {doc.records[c.id].fields["of"].id: c.id for c in f["ca"]}
            outputs = []
            for reference in f["op"]:
                output = doc.records[reference.id].fields
                candidate_id = nominees.get(reference.id)
                outputs.append({
                    "id": reference.id, "name": output["nm"], "candidate": candidate_id,
                    "requirements": requirements(id_, output, candidate_id),
                    "candidates": [{
                        "id": other, "nominated": other == candidate_id,
                        "requirements": requirements(id_, output, other),
                    } for other in candidates.get(reference.id, [])],
                })
            tasks.append({
                "id": id_, "project": f["pr"].id, "phase": f["ph"].value,
                "state": f["st"].value, "blockers": reasons, "outputs": outputs,
            })
    return {"intake": intake, "tasks": tasks, "ready": ready}
