"""Closed, replayable provider histories without filesystem or remote execution.

Evidence and remote states are caller assertions. The reducer verifies retained
intent and internal consistency; store publication must protect prior snapshots.
"""

import copy
import re
from datetime import UTC, datetime
from typing import Never

from . import platform
from .codec import PixlError

_JOURNAL_FIELDS = {"version", "intent", "intent_sha256", "events", "state", "remote_id"}
_EVENT_FIELDS = {
    "sequence",
    "event",
    "recorded_at",
    "remote_id",
    "evidence",
    "artifact",
}
_OBSERVATIONS = {"submitted", "running", "succeeded", "failed", "unknown"}
_IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_.-]{0,95}")
_HASH = re.compile(r"[0-9a-f]{64}")


def _fail(detail: str) -> Never:
    raise PixlError("job_history", detail)


def _shape(value, fields, label):
    if not isinstance(value, dict) or set(value) != fields:
        _fail(f"{label} has an invalid object shape")


def _identifier(value, label):
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        _fail(f"{label} must be a valid record identifier")


def _hash(value, label):
    if not isinstance(value, str) or _HASH.fullmatch(value) is None:
        _fail(f"{label} must be a lowercase SHA256 digest")


def _context(context):
    _shape(context, {"task", "outputs", "task_sha256", "bindings"}, "context")
    _identifier(context["task"], "context task")
    _hash(context["task_sha256"], "context task_sha256")
    outputs = context["outputs"]
    if not isinstance(outputs, list) or not outputs:
        _fail("context outputs must be a nonempty list")
    for output in outputs:
        _identifier(output, "context output")
    if len(set(outputs)) != len(outputs):
        _fail("context outputs must be unique")
    bindings = context["bindings"]
    if not isinstance(bindings, dict):
        _fail("context bindings must map record identifiers to hashes")
    for record_id, record_hash in bindings.items():
        _identifier(record_id, "context binding")
        _hash(record_hash, "context binding hash")
    if not set(outputs).issubset(bindings):
        _fail("context bindings must cover every output")


def _artifact(artifact, outputs, imported):
    _shape(artifact, {"id", "output", "record_sha256"}, "imported artifact")
    _identifier(artifact["id"], "candidate")
    _identifier(artifact["output"], "candidate output")
    _hash(artifact["record_sha256"], "candidate record_sha256")
    if artifact["output"] not in outputs:
        _fail("imported artifact must belong to a saved output")
    if artifact["id"] in imported:
        _fail("a candidate can be imported only once")
    imported.add(artifact["id"])


def _replay(events, outputs, prepared_at):
    if not isinstance(events, list):
        _fail("events must be a list")
    state, remote = "prepared", None
    dispatched, running_seen = False, False
    imported: set[str] = set()
    previous_at = platform._iso_timestamp(prepared_at, "prepared_at", "job_history")
    for sequence, row in enumerate(events, 1):
        _shape(row, _EVENT_FIELDS, "event")
        if type(row["sequence"]) is not int or row["sequence"] != sequence:
            _fail("event sequence must be consecutive integers starting at one")
        observed_at = platform._iso_timestamp(
            row["recorded_at"], "event recorded_at", "job_history"
        )
        if observed_at < previous_at:
            _fail("event timestamps cannot run backward or precede preparation")
        previous_at = observed_at
        evidence = row["evidence"]
        if not isinstance(evidence, dict) or not evidence:
            _fail("every event requires a nonempty evidence object")
        platform._no_secrets(evidence)
        event, next_remote = row["event"], row["remote_id"]
        if not isinstance(event, str) or event not in _OBSERVATIONS | {
            "dispatch",
            "imported",
        }:
            _fail("unknown journal event")
        platform._remote_id(next_remote)
        if remote is not None and remote != next_remote:
            _fail("remote identity is immutable once observed")
        if event != "imported" and row["artifact"] is not None:
            _fail("only an imported event may carry an artifact")
        if state == "failed" or state == "succeeded" and event != "imported":
            _fail("terminal history cannot accept this event")

        if event == "dispatch":
            if state != "prepared" or dispatched or next_remote is not None:
                _fail("dispatch requires prepared intent without a remote identity")
            dispatched = True
            state = "unknown"
        elif event == "imported":
            if state != "succeeded":
                _fail("candidate import requires succeeded history")
            _artifact(row["artifact"], outputs, imported)
        else:
            if not dispatched and (event != "failed" or next_remote is not None):
                _fail(
                    "only abandonment without a remote identity is allowed before dispatch"
                )
            if event in {"submitted", "running", "succeeded"} and next_remote is None:
                _fail("accepted observations require a remote identifier")
            if event == "submitted" and running_seen:
                _fail("running history cannot regress to submitted")
            running_seen = running_seen or event == "running"
            state = event
        remote = next_remote
    return state, remote


def validate(journal: dict) -> dict:
    """Replay a closed finite JSON history and return a detached validated copy.

    Hashes detect inconsistent intent, not authenticated provider evidence or
    replacement of the entire history. No catalog, project, or server is read.
    """
    platform._json_bytes(journal)
    _shape(journal, _JOURNAL_FIELDS, "journal")
    if type(journal["version"]) is not int or journal["version"] != 1:
        _fail("unsupported history version")
    intent = journal["intent"]
    _shape(intent, {"job", "request", "context"}, "intent")
    _identifier(intent["job"], "intent job")
    platform.validate_discovered(intent["request"])
    _context(intent["context"])
    _hash(journal["intent_sha256"], "intent_sha256")
    if journal["intent_sha256"] != platform._sha(intent):
        _fail("intent_sha256 disagrees with the retained intent")
    state, remote = _replay(
        journal["events"],
        intent["context"]["outputs"],
        intent["request"]["prepared_at"],
    )
    if journal["state"] != state or journal["remote_id"] != remote:
        _fail("journal state or remote identity disagrees with its events")
    return copy.deepcopy(journal)


def new(job_id: str, request: dict, context: dict) -> dict:
    """Bind an exact prepared request to a job and immutable project context."""
    intent = {"job": job_id, "request": request, "context": context}
    return validate(
        {
            "version": 1,
            "intent": intent,
            "intent_sha256": platform._sha(intent),
            "events": [],
            "state": "prepared",
            "remote_id": None,
        }
    )


def append(
    journal: dict,
    event: str,
    evidence: dict,
    remote_id: str | None = None,
    artifact: dict | None = None,
) -> dict:
    """Return one appended event without changing the supplied history or evidence.

    A missing remote ID retains an identity already observed. Dispatch is a local
    unknown claim; supplying a subsequent state never submits, polls, or retries.
    """
    result = validate(journal)
    result["events"].append(
        {
            "sequence": len(result["events"]) + 1,
            "event": event,
            "recorded_at": datetime.now(UTC).isoformat(),
            "remote_id": result["remote_id"] if remote_id is None else remote_id,
            "evidence": evidence,
            "artifact": artifact,
        }
    )
    platform._json_bytes(result)
    state, remote = _replay(
        result["events"],
        result["intent"]["context"]["outputs"],
        result["intent"]["request"]["prepared_at"],
    )
    result.update(state=state, remote_id=remote)
    return validate(result)
