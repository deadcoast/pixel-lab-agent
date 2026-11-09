"""Explicit candidate/family judgments, retention, nomination and recoverable completion."""

from __future__ import annotations

import copy
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

from . import codec, completion, graph, store
from .codec import Document, PixlError, Record, Ref, Symbol

Json = dict[str, Any]
TEXT = {"type": "string", "minLength": 1, "pattern": r"\S"}
SHA = {"type": "string", "pattern": "^[a-f0-9]{64}$"}


def _object(fields: Json) -> Json:
    return {"type": "object", "properties": fields, "required": list(fields), "additionalProperties": False}


OBSERVATION_SCHEMA = _object({
    "version": {"type": "integer", "const": 1},
    "binding_hash": SHA,
    "reviewer": TEXT,
    "observed_at": TEXT,
    "observations": {"type": "array", "maxItems": 64, "items": _object({
        "path": TEXT, "sha256": SHA, "mode": {"enum": ["local", "visual", "live"]}, "note": TEXT,
    })},
    "verdicts": {"type": "array", "minItems": 1, "maxItems": 1024, "items": _object({
        "criterion": TEXT, "status": {"enum": ["pass", "fail", "unavailable"]},
        "reason": TEXT, "supersedes": {"anyOf": [TEXT, {"type": "null"}]},
        "observations": {"type": "array", "uniqueItems": True, "items": {"type": "integer", "minimum": 0}},
    })},
    "action": {"enum": ["record", "nominate", "complete"]},
    "next_action": TEXT,
    "limitations": {"type": "array", "items": TEXT},
})


def _require(condition: bool, detail: str, code: str = "candidate_review") -> None:
    if not condition:
        raise PixlError(code, detail)


def _json(value: Any) -> bytes:
    data = (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode()
    _require(len(data) <= codec.MAX_BYTES, "review exceeds 16 MiB")
    return data


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _target(doc: Document, candidate_id: str) -> tuple[Record, Record, Record]:
    _require(doc.format == 2, "candidate review requires PX2")
    candidate = doc.records.get(candidate_id)
    _require(candidate is not None and candidate.kind == "X" and "of" in candidate.fields,
             "expected an existing planned candidate")
    assert candidate is not None
    output = doc.records[candidate.fields["of"].id]
    return candidate, output, doc.records[output.fields["tk"].id]


def _bindings(doc: Document, candidate_id: str) -> dict[str, str]:
    return {key: codec.record_hash(doc.records[key]) for key in sorted(graph.proof_scope(doc, [candidate_id]))}


def _current(doc: Document, candidate_id: str) -> dict[str, Record]:
    return {r.fields["rq"].id: r for r in doc.records.values()
            if r.kind == "V" and r.fields["xr"].id == candidate_id and not r.fields.get("ob", False)}


def context(doc: Document, root: Path, candidate_id: str) -> Json:
    """Resolve exact review inputs and current acceptance without changing state."""
    root = Path(root).resolve()
    graph.validate(doc, root)
    candidate, output, task = _target(doc, candidate_id)
    current = _current(doc, candidate_id)
    criteria = []
    for ref in output.fields["rq"]:
        q = doc.records[ref.id].fields
        verdict = current.get(ref.id)
        criteria.append({"id": ref.id, "check": q["ck"], "domain": q["dm"].value,
                         "mode": q["md"].value, "sources": [r.id for r in q["so"]],
                         "status": verdict.fields["st"].value if verdict else "unperformed",
                         "verdict": verdict.id if verdict else None})
    result = {
        "state_hash": codec.digest(doc), "revision": doc.revision,
        "binding_hash": _sha(_json(_bindings(doc, candidate_id))),
        "candidate": candidate_id, "candidate_file": {"path": candidate.fields["ur"], "sha256": candidate.fields["dg"]},
        "output": output.id, "task": task.id, "task_status": task.fields["st"].value,
        "nominated": Ref(candidate_id) in task.fields["ca"], "criteria": criteria,
        "current_acceptance": {"all_required_pass": all(q["status"] == "pass" for q in criteria),
                               "task_complete": task.fields["st"].value == "done"},
        "files_verified": True, "automatic_artistic_judgment": False,
    }
    if "mb" in output.fields:
        manifest = json.loads(graph.confined(root, candidate.fields["ur"]).read_bytes())
        directory = Path(candidate.fields["ur"]).parent
        result["snapshot_acceptance"] = {"accepted": manifest["acceptance"]["accepted"],
                                         "source_state_hash": manifest["source_state_sha256"],
                                         "created_at": manifest["created_at"]}
        result["members"] = [{**row, "retained_path": (directory / row["path"]).as_posix()} for row in manifest["files"]]
    return result


def _validate_request(doc: Document, candidate_id: str, observation: Json) -> None:
    try:
        Draft202012Validator(OBSERVATION_SCHEMA).validate(observation)
    except ValidationError as error:
        raise PixlError("candidate_review", "invalid observation at " + ".".join(map(str, error.absolute_path))) from error
    _require(type(observation["version"]) is int, "version must be integer 1")
    try:
        at = datetime.fromisoformat(observation["observed_at"])
        _require(at.utcoffset() is not None and at <= datetime.now(UTC), "observation needs an actual nonfuture timestamp with UTC offset")
    except ValueError as error:
        raise PixlError("candidate_review", "invalid observation timestamp") from error
    actor = doc.records.get(observation["reviewer"])
    _require(actor is not None and actor.kind == "A", "reviewer must name a saved actor")
    _require(observation["binding_hash"] == _sha(_json(_bindings(doc, candidate_id))),
             "candidate or criterion bindings changed; reread and reassess", "review_binding")
    _, output, _ = _target(doc, candidate_id)
    required = {r.id for r in output.fields["rq"]}
    seen: set[str] = set()
    for verdict in observation["verdicts"]:
        qid = verdict["criterion"]
        _require(qid in required and qid not in seen, "criteria must be distinct requirements of this candidate")
        seen.add(qid)
        indices = verdict["observations"]
        _require(all(type(i) is int and 0 <= i < len(observation["observations"]) for i in indices), "invalid observation index")
        if verdict["status"] == "unavailable":
            _require(not indices, "unavailable verdict cannot claim performed evidence")
        else:
            _require(bool(indices), "performed verdict needs actual observations")
            mode = doc.records[qid].fields["md"].value
            _require(all(observation["observations"][i]["mode"] == mode for i in indices), "observation modes must match the criterion")


def _capture(root: Path, observations: list[Json]) -> list[tuple[Json, bytes]]:
    captured = []
    total = 0
    for index, item in enumerate(observations):
        path = graph.confined(root, item["path"])
        try:
            with path.open("rb") as stream:
                data = stream.read(min(64 * 1024 * 1024, 256 * 1024 * 1024 - total) + 1)
        except OSError as error:
            raise PixlError("review_file", item["path"]) from error
        total += len(data)
        _require(len(data) <= 64 * 1024 * 1024 and total <= 256 * 1024 * 1024, "observation files exceed retention limit")
        _require(_sha(data) == item["sha256"], "observation file changed: " + item["path"], "review_file")
        suffix = path.suffix if path.suffix[1:].isalnum() and len(path.suffix) <= 17 else ".bin"
        captured.append(({"path": f"files/{index:04d}{suffix}", "sha256": _sha(data), "bytes": len(data)}, data))
    return captured


def _retain(folder: Path, report: Json, captured: list[tuple[Json, bytes]]) -> tuple[Path, str]:
    data = _json(report)
    digest = _sha(data)
    relative = f"reviews/{digest}"
    directory = graph.confined(folder, relative)
    for name, content in [("review.json", data), *[(row["path"], content) for row, content in captured]]:
        path = graph.confined(folder, relative + "/" + name)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            _require(path.read_bytes() == content, "retained review bytes differ", "review_file")
        else:
            store._atomic(path, content)
    return directory, digest


def _record_review(current: Document, folder: Path, root: Path, candidate_id: str,
                   review_id: str, observation: Json) -> Document:
    candidate, _, task = _target(current, candidate_id)
    _require(task.fields["st"].value != "done", "reopen the completed task before a new review", "reopen_required")
    existing = _current(current, candidate_id)
    for item in observation["verdicts"]:
        previous = existing.get(item["criterion"])
        _require(item["supersedes"] == (previous.id if previous else None), "name the exact current verdict to supersede", "review_supersedes")
    ids = [review_id, *[f"{review_id}.file.{i}" for i in range(len(observation["observations"]))],
           *[f"{review_id}.{kind}.{i}" for kind in ("evidence", "verdict") for i in range(len(observation["verdicts"]))]]
    _require(all(codec.IDENT.fullmatch(key.encode()) and key not in current.records for key in ids), "review IDs must be valid, fresh and leave room for generated suffixes")
    captured = _capture(root, observation["observations"])
    report = {"version": 1, "review": review_id, "candidate": candidate_id,
              "source_state_hash": codec.digest(current), "recorded_at": datetime.now(UTC).isoformat(),
              "bindings": _bindings(current, candidate_id), "observation": observation,
              "files": [row for row, _ in captured]}
    directory, digest = _retain(folder, report, captured)
    updated = copy.deepcopy(current)
    updated.revision += 1
    file_refs = []
    for index, (row, _) in enumerate(captured):
        ident = f"{review_id}.file.{index}"
        updated.records[ident] = Record(id=ident, kind="X", fields={
            "nm": observation["observations"][index]["note"], "kd": Symbol("reference"),
            "ur": (directory / row["path"]).relative_to(root).as_posix(), "dg": row["sha256"],
        })
        file_refs.append(Ref(ident))
    updated.records[review_id] = Record(id=review_id, kind="X", fields={
        "nm": "Explicit candidate review", "kd": Symbol("report"),
        "ur": (directory / "review.json").relative_to(root).as_posix(), "dg": digest,
        "mt": {"candidate_review": 1, "candidate": Ref(candidate_id), "files": file_refs},
    })
    for index, item in enumerate(observation["verdicts"]):
        if item["supersedes"]:
            updated.records[item["supersedes"]].fields["ob"] = True
        evidence = []
        if item["status"] != "unavailable":
            ident = f"{review_id}.evidence.{index}"
            scope = graph.proof_scope(updated, [candidate_id, item["criterion"], review_id])
            updated.records[ident] = Record(id=ident, kind="E", fields={
                "nm": item["reason"], "ur": updated.records[review_id].fields["ur"], "dg": digest,
                "rs": Symbol(item["status"]), "md": current.records[item["criterion"]].fields["md"],
                "at": observation["observed_at"],
                "bs": [{"rf": Ref(key), "dg": codec.record_hash(updated.records[key])} for key in sorted(scope)],
            })
            evidence = [Ref(ident)]
        ident = f"{review_id}.verdict.{index}"
        updated.records[ident] = Record(id=ident, kind="V", fields={
            "tk": Ref(task.id), "rq": Ref(item["criterion"]), "xr": Ref(candidate.id),
            "st": Symbol(item["status"]), "wh": Ref(observation["reviewer"]),
            "wy": item["reason"], "at": observation["observed_at"], "ev": evidence,
        })
        updated.records[task.id].fields["vr"].append(Ref(ident))
    return updated


def _replay(doc: Document, root: Path, candidate_id: str, review_id: str, observation: Json) -> None:
    record = doc.records[review_id]
    _require(record.kind == "X" and record.fields.get("mt", {}).get("candidate_review") == 1, "review ID already belongs to another record")
    path = graph.confined(root, record.fields["ur"])
    data = path.read_bytes()
    _require(_sha(data) == record.fields["dg"], "saved review changed", "review_file")
    saved = json.loads(data)
    _require(saved["review"] == review_id and saved["candidate"] == candidate_id and
             _json(saved["observation"]) == _json(observation), "review ID has a different request; use a fresh ID")
    current = _current(doc, candidate_id)
    for index, item in enumerate(observation["verdicts"]):
        verdict = current.get(item["criterion"])
        _require(verdict is not None and verdict.id == f"{review_id}.verdict.{index}",
                 "review has been superseded; cannot replay as acceptance", "review_superseded")


def submit(folder: Path, expected: str, candidate_id: str, review_id: str,
           observation: Json, root: Path | None = None) -> Json:
    """Preflight and publish an explicit review and its requested lifecycle action."""
    folder = Path(folder).resolve()
    root = Path(root).resolve() if root is not None else folder.parent
    _require(folder != root and folder.is_relative_to(root), "review store must be a consumer subdirectory", "store_path")
    with store.lock(folder):
        current = store.load(folder)
        _require(codec.digest(current) == expected, "reload canonical state_hash before review publication", "stale_write")
        graph.validate(current, root)
        _target(current, candidate_id)
        _validate_request(current, candidate_id, observation)
        reused = review_id in current.records
        steps = []
        if reused:
            _replay(current, root, candidate_id, review_id, observation)
            reviewed = current
        else:
            reviewed = _record_review(current, folder, root, candidate_id, review_id, observation)
            steps.append(reviewed)
        _, output, task = _target(reviewed, candidate_id)
        if observation["action"] != "record":
            selected = {reviewed.records[ref.id].fields["of"].id: ref.id for ref in task.fields["ca"]}
            selected[output.id] = candidate_id
            nominees = [selected[ref.id] for ref in task.fields["op"] if ref.id in selected]
            if observation["action"] == "complete":
                steps.extend(completion.planned_steps(reviewed, task.id, nominees, root, folder))
            elif task.fields["ca"] != [Ref(key) for key in nominees]:
                from .plar_workflow import current_bindings

                current_bindings(reviewed, task.id, root, folder)
                nominated = copy.deepcopy(reviewed)
                nominated.revision += 1
                nominated.records[task.id].fields["ca"] = [Ref(key) for key in nominees]
                steps.append(nominated)
        previous = current
        for step in steps:
            store._check_commit(previous, step, codec.digest(previous), root, folder)
            previous = step
        publications = [store._publish(folder, step) for step in steps]
        final = steps[-1] if steps else current
        return {"review": review_id, "review_sha256": final.records[review_id].fields["dg"],
                "review_path": final.records[review_id].fields["ur"], "reused_review": reused,
                "publications": publications, "remote_executed": False,
                **context(final, root, candidate_id)}
