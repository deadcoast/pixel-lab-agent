"""Project-bound provider history. All external observations come from the caller.

Immutable blobs precede compare-and-swap state publication. A failed publication
may leave an unreferenced blob, but never grants a dispatch or advances a job.
"""

import copy
import hashlib
import json
from pathlib import Path

from . import codec, graph, job_history, lifecycle, platform, store
from .codec import PixlError, Record, Ref, Symbol

PENDING = {"prepared", "unknown", "submitted", "running"}


def _require(condition, code, detail):
    if not condition:
        raise PixlError(code, detail)


def _task(doc, task_id):
    record = doc.records.get(task_id)
    _require(record is not None and record.kind == "T", "job_task", str(task_id))
    return record


def _context(doc, task_id, outputs):
    task = _task(doc, task_id)
    _require(
        isinstance(outputs, list)
        and bool(outputs)
        and all(isinstance(id_, str) for id_ in outputs)
        and len(set(outputs)) == len(outputs),
        "job_outputs",
        "distinct output IDs required",
    )
    planned = {r.id for r in task.fields["op"]}
    _require(set(outputs) <= planned, "job_outputs", "outputs must belong to the task")
    fields = {k: v for k, v in task.fields.items() if k not in {"st", "ca", "vr"}}
    seeds = set(outputs)
    for field in ("ip", "dc", "kn"):
        seeds.update(r.id for r in task.fields[field])
    return {
        "task": task_id,
        "outputs": sorted(outputs),
        "task_sha256": codec.record_hash(Record(task.id, task.kind, fields)),
        "bindings": {
            id_: codec.record_hash(doc.records[id_])
            for id_ in sorted(graph.proof_scope(doc, seeds))
        },
    }


def _blockers(doc, task_id, root=None, dispatching=False):
    task = _task(doc, task_id)
    reasons = lifecycle.blockers(doc, task_id)
    if root is not None:
        from .plar import selection_bindings

        reasons.extend(
            f"plar_selection: {row.get('asset_id', row['input'])} is {row['status']} (selected={row.get('selected_for_asset', True)}); compare current requirements with the retained plan"
            for row in selection_bindings(doc, task_id, root)
            if row["status"] != "current" or (dispatching and not row.get("selected_for_asset", True))
        )
    if task.fields["st"].value not in {"open", "active"}:
        reasons.append(f"task_state: {task_id} is {task.fields['st'].value}")
    return reasons


def _stale(doc, journal):
    context = journal["intent"]["context"]
    try:
        current = _context(doc, context["task"], context["outputs"])
    except PixlError:
        return ["task or output membership changed"]
    changed = [
        id_
        for id_, digest in context["bindings"].items()
        if current["bindings"].get(id_) != digest
    ]
    changed.extend(id_ for id_ in current["bindings"] if id_ not in context["bindings"])
    if current["task_sha256"] != context["task_sha256"]:
        changed.append(context["task"])
    return sorted(set(changed))


def _journal_bytes(doc, reference, root):
    snapshot = doc.records[reference.id]
    path = graph.confined(root, snapshot.fields["ur"])
    try:
        data = path.read_bytes()
        _require(
            hashlib.sha256(data).hexdigest() == snapshot.fields["dg"],
            "file_hash",
            snapshot.id,
        )
        value = json.loads(data)
        _require(
            data == platform._json_bytes(value) + b"\n",
            "job_history",
            "journal must use canonical JSON bytes",
        )
        return job_history.validate(value)
    except (OSError, ValueError, UnicodeError) as error:
        if isinstance(error, PixlError):
            raise
        raise PixlError("job_history", f"{snapshot.id}: unreadable journal") from error


def _snapshots(doc, record, root):
    """Check every retained prefix and its exact local receipt projection."""
    fields = record.fields
    _require(
        "jr" in fields and "op" in fields and "xs" in fields and bool(fields["op"]),
        "job_projection",
        f"{record.id}: jr, op and xs are required together",
    )
    _require(len(set(fields["op"])) == len(fields["op"]), "job_projection", record.id)
    _require(
        bool(fields["ev"]), "job_projection", f"{record.id}: journal receipts required"
    )
    histories: list[dict] = []
    references = []
    for ref in fields["ev"]:
        receipt = doc.records[ref.id]
        f = receipt.fields
        _require(
            not f.get("ob", False)
            and f["md"] == Symbol("local")
            and f["rs"] == Symbol("pass")
            and len(f["bs"]) == 1,
            "job_projection",
            f"{record.id}: immutable local snapshot receipts required",
        )
        reference = f["bs"][0]["rf"]
        snapshot = doc.records[reference.id]
        _require(
            snapshot.kind == "X"
            and snapshot.fields["kd"] == Symbol("report")
            and "of" not in snapshot.fields
            and "ct" not in snapshot.fields
            and f["ur"] == snapshot.fields["ur"]
            and f["dg"] == snapshot.fields["dg"],
            "job_projection",
            f"{record.id}: receipt must describe its journal X",
        )
        references.append(reference)
        if root is not None:
            journal = _journal_bytes(doc, reference, root)
            _require(
                journal["intent"]["job"] == record.id,
                "job_projection",
                f"{record.id}: different journal owner",
            )
            _require(
                len(journal["events"]) == len(histories),
                "job_history",
                f"{record.id}: retain one snapshot per event prefix",
            )
            if histories:
                previous = histories[-1]
                _require(
                    journal["intent"] == previous["intent"]
                    and journal["events"][:-1] == previous["events"],
                    "job_history",
                    f"{record.id}: journal history was rewritten",
                )
            expected_at = (
                journal["events"][-1]["recorded_at"]
                if journal["events"]
                else journal["intent"]["request"]["prepared_at"]
            )
            _require(
                f["at"] == expected_at,
                "job_projection",
                f"{record.id}: receipt timestamp",
            )
            histories.append(journal)
    _require(
        len(set(references)) == len(references) and references[-1] == fields["jr"],
        "job_projection",
        f"{record.id}: current journal must be last unique snapshot",
    )
    if root is None:
        return []
    journal = histories[-1]
    intent = journal["intent"]
    imported = [
        e["artifact"]["id"] for e in journal["events"] if e["event"] == "imported"
    ]
    _require(
        fields["tk"].id == intent["context"]["task"]
        and [r.id for r in fields["op"]] == intent["context"]["outputs"]
        and fields["ah"] == journal["intent_sha256"]
        and fields["tl"] == intent["request"]["tool"]
        and fields["si"].value == journal["state"]
        and fields["ri"] == (journal["remote_id"] or "")
        and [r.id for r in fields["xs"]] == imported,
        "job_projection",
        f"{record.id}: J disagrees with retained journal",
    )
    for event in journal["events"]:
        if event["event"] == "imported":
            item = event["artifact"]
            artifact = doc.records.get(item["id"])
            _require(
                artifact is not None
                and artifact.kind == "X"
                and artifact.fields.get("of") == Ref(item["output"])
                and codec.record_hash(artifact) == item["record_sha256"],
                "job_artifact",
                f"{record.id}: imported candidate changed or disappeared",
            )
    return histories


def validate(doc, root=None):
    """Called after shared graph checks; legacy J semantics are unchanged."""
    if doc.format != 2:
        return
    for record in doc.records.values():
        if record.kind == "J" and any(k in record.fields for k in ("jr", "op", "xs")):
            _snapshots(doc, record, root)


def _pending(doc, task_id, outputs, except_id=None, root=None):
    def selections(task):
        keys = set()
        for reference in _task(doc, task).fields.get("ip", []):
            metadata = doc.records[reference.id].fields.get("mt", {})
            if metadata.get("binding") == "pixl.plar.selection/1" and all(isinstance(metadata.get(k), str) for k in ("plar_path", "asset_id")):
                path = graph.confined(root, metadata["plar_path"]) if root is not None else Path(metadata["plar_path"])
                keys.add((str(path), metadata["asset_id"]))
        return keys

    selected = selections(task_id)
    for record in doc.records.values():
        if (
            record.kind != "J"
            or record.id == except_id
            or record.fields["si"].value not in PENDING
        ):
            continue
        fields = record.fields
        if selected.intersection(selections(fields["tk"].id)) or ("jr" not in fields and fields["tk"].id == task_id) or (
            "jr" in fields and set(outputs) & {r.id for r in fields["op"]}
        ):
            raise PixlError(
                "job_pending",
                f"{record.id}: reconcile the existing attempt before another request",
            )


def transitions(current, candidate, root, folder):
    """Enforce durable history on generic initialization and commit as well."""
    if candidate.format != 2:
        return
    for record in candidate.records.values():
        if record.kind != "J":
            continue
        old = current.records.get(record.id) if current is not None else None
        durable = "jr" in record.fields
        if old is not None:
            _require(
                durable == ("jr" in old.fields),
                "job_history",
                f"{record.id}: legacy jobs cannot acquire or shed durable history",
            )
        if not durable:
            continue
        _require(
            current is not None,
            "job_history",
            f"{record.id}: initialize the plan before publishing a durable job",
        )
        _retained_storage(candidate, record, folder, root)
        histories = _snapshots(candidate, record, root)
        journal = histories[-1]
        context = journal["intent"]["context"]
        if old is None:
            _require(
                current is not None and not journal["events"],
                "job_history",
                f"{record.id}: save a plan before a new prepared-only job",
            )
            _require(
                context == _context(current, context["task"], context["outputs"])
                and context == _context(candidate, context["task"], context["outputs"]),
                "job_stale",
                f"{record.id}: save unchanged request context first",
            )
            _require(
                not _blockers(candidate, context["task"], root),
                "job_blocked",
                record.id,
            )
            _pending(candidate, context["task"], context["outputs"], record.id, root)
            continue
        previous = _snapshots(current, old, root)[-1]
        _require(journal["intent"] == previous["intent"], "job_history", record.id)
        _require(
            journal["events"][: len(previous["events"])] == previous["events"],
            "job_history",
            f"{record.id}: observations are append-only",
        )
        added = len(journal["events"]) - len(previous["events"])
        _require(
            added in {0, 1}, "job_history", f"{record.id}: publish one event at a time"
        )
        old_receipts = old.fields["ev"]
        _require(
            record.fields["ev"][: len(old_receipts)] == old_receipts,
            "job_history",
            f"{record.id}: keep published snapshot references",
        )
        for reference in old_receipts:
            receipt = current.records[reference.id]
            snapshot_id = receipt.fields["bs"][0]["rf"].id
            _require(
                candidate.records[reference.id] == receipt
                and candidate.records[snapshot_id] == current.records[snapshot_id],
                "job_history",
                f"{record.id}: published snapshots and receipts are immutable",
            )
        if not added:
            _require(
                record == old,
                "job_history",
                f"{record.id}: projection changed without event",
            )
        elif journal["events"][-1]["event"] == "dispatch":
            _require(
                not _stale(candidate, journal) and not _stale(current, journal),
                "job_stale",
                f"{record.id}: request context changed",
            )
            _require(
                not _blockers(candidate, context["task"], root, dispatching=True),
                "job_blocked",
                record.id,
            )
            _pending(candidate, context["task"], context["outputs"], record.id, root)
        elif journal["events"][-1]["event"] == "imported":
            item = journal["events"][-1]["artifact"]
            _require(
                item["id"] not in current.records,
                "job_artifact",
                "import a new candidate ID",
            )
            _output_current(candidate, histories[0], item["output"])


def _output_current(doc, journal, output_id):
    bindings = journal["intent"]["context"]["bindings"]
    _require(
        all(
            codec.record_hash(doc.records[id_]) == bindings.get(id_)
            for id_ in graph.proof_scope(doc, [output_id])
        ),
        "job_stale",
        "output plan or its contract/criteria changed before import",
    )


def _retained_storage(doc, job, folder, root):
    folder, root = _locations(folder, root)
    relative = folder.relative_to(root)
    for reference in job.fields["ev"]:
        receipt = doc.records[reference.id]
        snapshot = doc.records[receipt.fields["bs"][0]["rf"].id]
        expected = (relative / "jobs" / (snapshot.fields["dg"] + ".json")).as_posix()
        _require(
            snapshot.fields["ur"] == expected
            and graph.confined(root, expected).is_relative_to(folder),
            "job_storage",
            "journal snapshots must use content-addressed files inside this store",
        )
    for reference in job.fields["xs"]:
        artifact = doc.records[reference.id]
        suffix = Path(artifact.fields["ur"]).suffix
        expected = (
            relative / "artifacts" / (artifact.fields["dg"] + suffix)
        ).as_posix()
        _require(
            artifact.fields["ur"] == expected
            and graph.confined(root, expected).is_relative_to(folder),
            "job_storage",
            "imported candidates must use content-addressed files inside this store",
        )


def _locations(folder, root):
    folder = Path(folder).resolve()
    root = Path(root).resolve() if root is not None else folder.parent
    _require(
        folder != root and folder.is_relative_to(root),
        "store_path",
        "job store must be a subdirectory of the project root",
    )
    return folder, root


def _load(folder, expected, root):
    folder, root = _locations(folder, root)
    doc = store.load(folder)
    _require(
        codec.digest(doc) == expected,
        "stale_write",
        "reload current state before changing a job",
    )
    _require(
        doc.format == 2, "job_format", "durable jobs require PX2; no implicit migration"
    )
    graph.validate(doc, root)
    return folder, root, doc


def _blob(folder, root, category, data, suffix):
    hash_ = hashlib.sha256(data).hexdigest()
    relative = (folder.relative_to(root) / category / (hash_ + suffix)).as_posix()
    path = graph.confined(root, relative)
    _require(
        path.is_relative_to(folder),
        "store_path",
        "job bytes must stay inside the store",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        _require(path.read_bytes() == data, "history_corrupt", relative)
    else:
        store._atomic(path, data)
    return relative, hash_


def _project(doc, folder, root, journal):
    data = platform._json_bytes(journal) + b"\n"
    uri, hash_ = _blob(folder, root, "jobs", data, ".json")
    snapshot_id, evidence_id = "jx." + hash_, "je." + hash_
    _require(
        snapshot_id not in doc.records and evidence_id not in doc.records,
        "job_history",
        "snapshot already published",
    )
    snapshot = Record(
        snapshot_id,
        "X",
        {
            "nm": "Retained provider journal",
            "kd": Symbol("report"),
            "ur": uri,
            "dg": hash_,
        },
    )
    at = (
        journal["events"][-1]["recorded_at"]
        if journal["events"]
        else journal["intent"]["request"]["prepared_at"]
    )
    receipt = Record(
        evidence_id,
        "E",
        {
            "nm": "Local journal retention; caller observations are not remote or artistic proof",
            "ur": uri,
            "dg": hash_,
            "rs": Symbol("pass"),
            "md": Symbol("local"),
            "at": at,
            "bs": [{"rf": Ref(snapshot_id), "dg": codec.record_hash(snapshot)}],
        },
    )
    doc.records[snapshot_id] = snapshot
    doc.records[evidence_id] = receipt
    intent = journal["intent"]
    previous = doc.records.get(intent["job"])
    refs = previous.fields["ev"] if previous is not None else []
    doc.records[intent["job"]] = Record(
        intent["job"],
        "J",
        {
            "tk": Ref(intent["context"]["task"]),
            "tl": intent["request"]["tool"],
            "ah": journal["intent_sha256"],
            "si": Symbol(journal["state"]),
            "ri": journal["remote_id"] or "",
            "ev": [*refs, Ref(evidence_id)],
            "jr": Ref(snapshot_id),
            "op": [Ref(id_) for id_ in intent["context"]["outputs"]],
            "xs": [
                Ref(e["artifact"]["id"])
                for e in journal["events"]
                if e["event"] == "imported"
            ],
        },
    )


def _summary(doc, record, journal, root=None):
    if journal is None:
        return {
            "id": record.id,
            "durable": False,
            "state": record.fields["si"].value,
            "next_action": "inspect_legacy_history",
            "remote_id": record.fields["ri"] or None,
        }
    stale = _stale(doc, journal)
    state = journal["state"]
    reasons = (
        _blockers(doc, journal["intent"]["context"]["task"], root, dispatching=True)
        if state == "prepared"
        else []
    )
    next_action = {
        "prepared": "resolve_context" if stale or reasons else "dispatch",
        "unknown": "reconcile",
        "submitted": "observe",
        "running": "observe",
        "succeeded": "inspect_candidates",
        "failed": "review_failure",
    }[state]
    from .plar import selection_bindings

    return {
        "selection_bindings": selection_bindings(doc, record.fields["tk"].id, root)
        if root is not None
        else [],
        "id": record.id,
        "durable": True,
        "state": state,
        "remote_id": journal["remote_id"],
        "intent_sha256": journal["intent_sha256"],
        "stale": stale,
        "blockers": reasons,
        "next_action": next_action,
        "request": copy.deepcopy(journal["intent"]["request"]),
        "context": copy.deepcopy(journal["intent"]["context"]),
        "events": copy.deepcopy(journal["events"]),
        "candidates": [
            e["artifact"] for e in journal["events"] if e["event"] == "imported"
        ],
    }


def _save(folder, root, doc, journal, expected):
    _project(doc, folder, root, journal)
    doc.revision += 1
    published = store.commit(folder, doc, expected, root)
    return {
        **published,
        "job": _summary(doc, doc.records[journal["intent"]["job"]], journal, root),
        "remote_executed": False,
    }


def _get(doc, job_id, root):
    record = doc.records.get(job_id)
    _require(
        record is not None and record.kind == "J" and "jr" in record.fields,
        "job_history",
        "select an existing durable job",
    )
    return _snapshots(doc, record, root)[-1]


def prepare(
    folder,
    expected,
    job_id,
    task_id,
    outputs,
    provider,
    tool,
    arguments,
    schema,
    discovery,
    authorization,
    root=None,
):
    folder, root, doc = _load(folder, expected, root)
    _require(
        job_id not in doc.records, "job_exists", "use a new job ID for a new attempt"
    )
    context = _context(doc, task_id, outputs)
    reasons = _blockers(doc, task_id, root)
    _require(not reasons, "job_blocked", "; ".join(reasons))
    _pending(doc, task_id, outputs, root=root)
    request = platform.prepare_discovered(
        provider, tool, arguments, schema, discovery, authorization
    )
    journal = job_history.new(job_id, request, context)
    return _save(folder, root, doc, journal, expected)


def dispatch(folder, expected, job_id, root=None):
    folder, root, doc = _load(folder, expected, root)
    previous = _get(doc, job_id, root)
    _require(not _stale(doc, previous), "job_stale", "saved request context changed")
    task_id = previous["intent"]["context"]["task"]
    reasons = _blockers(doc, task_id, root, dispatching=True)
    _require(not reasons, "job_blocked", "; ".join(reasons))
    journal = job_history.append(
        previous,
        "dispatch",
        {
            "origin": "local_dispatch_claim",
            "meaning": "Saved before host submission; no remote execution.",
        },
    )
    result = _save(folder, root, doc, journal, expected)
    result["dispatch_request"] = copy.deepcopy(journal["intent"]["request"])
    return result


def observe(folder, expected, job_id, event, evidence, remote_id=None, root=None):
    folder, root, doc = _load(folder, expected, root)
    _require(
        event in {"submitted", "running", "succeeded", "failed", "unknown"},
        "job_event",
        "select a supplied observation state",
    )
    journal = job_history.append(
        _get(doc, job_id, root), event, evidence, remote_id=remote_id
    )
    return _save(folder, root, doc, journal, expected)


def import_artifact(
    folder, expected, job_id, output_id, candidate_id, path, evidence, root=None
):
    folder, root, doc = _load(folder, expected, root)
    previous = _get(doc, job_id, root)
    _require(candidate_id not in doc.records, "job_artifact", "use a new candidate ID")
    context = previous["intent"]["context"]
    _require(
        output_id in context["outputs"],
        "job_outputs",
        "output was not requested by this job",
    )
    output = doc.records[output_id]
    _output_current(doc, previous, output_id)
    source = graph.confined(root, path)
    data = source.read_bytes()
    _require(
        bool(data) and len(data) <= 64 * 1024 * 1024,
        "job_artifact",
        "expected a file of at most 64 MiB",
    )
    # The suffix is display metadata only, not a claimed image format or validation.
    suffix = source.suffix.lower()
    _require(
        len(suffix) <= 16 and all(c.isalnum() or c == "." for c in suffix),
        "job_artifact",
        "unsupported filename suffix",
    )
    uri, hash_ = _blob(folder, root, "artifacts", data, suffix)
    fields = {
        "nm": f"Imported candidate {candidate_id}",
        "ur": uri,
        "dg": hash_,
        "kd": output.fields["kd"],
        "of": Ref(output_id),
    }
    if "ct" in output.fields:
        fields["ct"] = output.fields["ct"]
    artifact = Record(candidate_id, "X", fields)
    doc.records[candidate_id] = artifact
    journal = job_history.append(
        previous,
        "imported",
        evidence,
        artifact={
            "id": candidate_id,
            "output": output_id,
            "record_sha256": codec.record_hash(artifact),
        },
    )
    return _save(folder, root, doc, journal, expected)


def report(doc, root):
    _require(
        root is not None,
        "job_root",
        "job recovery requires the project root and journal files",
    )
    graph.validate(doc, root)
    rows = []
    for record in sorted(doc.records.values(), key=lambda r: r.id):
        if record.kind == "J":
            journal = _get(doc, record.id, root) if "jr" in record.fields else None
            rows.append(_summary(doc, record, journal, root))
    return {
        "jobs": rows,
        "hash": codec.digest(doc),
        "revision": doc.revision,
        "files_verified": True,
        "remote_executed": False,
    }
