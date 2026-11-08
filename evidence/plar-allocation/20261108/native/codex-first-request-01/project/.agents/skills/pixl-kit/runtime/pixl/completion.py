"""Nominate already-reviewed candidates and complete a PX2 task without new verdicts."""

import copy
from pathlib import Path

from . import codec, graph, store
from .codec import PixlError, Ref, Symbol


def complete(folder, expected, task_id, candidates, root=None):
    folder = Path(folder).resolve()
    root = Path(root).resolve() if root is not None else folder.parent
    if folder == root or not folder.is_relative_to(root):
        raise PixlError(
            "store_path", "completion store must be a consumer subdirectory"
        )
    with store.lock(folder):
        current = store.load(folder)
        if codec.digest(current) != expected:
            raise PixlError("stale_write", "reload state before completing the task")
        graph.validate(current, root)
        if current.format != 2:
            raise PixlError("format", "task completion requires PX2")
        task = current.records.get(task_id)
        if task is None or task.kind != "T":
            raise PixlError("unknown_task", str(task_id))
        if (
            not isinstance(candidates, list)
            or not candidates
            or any(not isinstance(id_, str) for id_ in candidates)
            or len(set(candidates)) != len(candidates)
        ):
            raise PixlError(
                "candidate_nomination",
                "provide distinct candidate IDs for every planned output",
            )
        outputs = [ref.id for ref in task.fields["op"]]
        selected = {}
        for id_ in candidates:
            record = current.records.get(id_)
            owner = record.fields.get("of") if record is not None else None
            if (
                record is None
                or record.kind != "X"
                or not isinstance(owner, Ref)
                or owner.id not in outputs
                or owner.id in selected
            ):
                raise PixlError(
                    "candidate_nomination",
                    f"{id_}: expected one candidate per task output",
                )
            selected[owner.id] = id_
        if set(selected) != set(outputs):
            raise PixlError(
                "completion", "every planned output needs a selected candidate"
            )
        pending = [
            r.id
            for r in current.records.values()
            if r.kind == "J"
            and r.fields["tk"].id == task_id
            and r.fields["si"].value not in {"succeeded", "failed"}
        ]
        if pending:
            raise PixlError(
                "pending_jobs",
                "reconcile provider attempts before completion: " + ", ".join(pending),
            )
        state = task.fields["st"].value
        if state == "done":
            if {ref.id for ref in task.fields["ca"]} != set(candidates):
                raise PixlError("reopen_required", task_id)
            return {
                "revision": current.revision,
                "hash": expected,
                "state": str(folder / "state.px"),
                "task": task_id,
                "candidates": candidates,
                "already_complete": True,
                "acceptance_created": False,
                "remote_executed": False,
                "publications": [],
            }
        if state not in {"open", "active", "blocked"}:
            raise PixlError("reopen_required", task_id)
        steps = []
        next_doc = copy.deepcopy(current)
        next_doc.records[task_id].fields["ca"] = [Ref(selected[id_]) for id_ in outputs]
        if state != "active":
            next_doc.revision += 1
            next_doc.records[task_id].fields["st"] = Symbol("active")
            steps.append(copy.deepcopy(next_doc))
        next_doc.revision += 1
        next_doc.records[task_id].fields["st"] = Symbol("done")
        steps.append(next_doc)
        previous = current
        # Check the complete sequence before changing state. No criteria/evidence are created.
        for step in steps:
            store._check_commit(previous, step, codec.digest(previous), root, folder)
            previous = step
        publications = [store._publish(folder, step) for step in steps]
        return {
            **publications[-1],
            "task": task_id,
            "candidates": [selected[id_] for id_ in outputs],
            "already_complete": False,
            "acceptance_created": False,
            "remote_executed": False,
            "publications": publications,
        }
