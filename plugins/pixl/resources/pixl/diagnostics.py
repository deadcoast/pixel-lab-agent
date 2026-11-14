"""Small public recovery hints derived from known failures and safe identities.

This module performs no I/O. Request arguments cannot assert observed job state.
Recovery operations, when supplied, are reads for reconciliation, never retries.
"""

import json
import re
from pathlib import PurePosixPath

from .codec import PixlError

_ID = re.compile(r"[A-Za-z][A-Za-z0-9_.-]{0,95}\Z")
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_OPERATION = re.compile(r"[a-z][a-z0-9_]{0,95}\Z")
_JOB_STATES = {"prepared", "unknown", "submitted", "running", "succeeded", "failed"}
_STALE = {"stale_write", "handoff_stale", "job_stale", "source_hash", "caller_artifact_stale"}
_INVALID = {
    "input_schema", "schema", "syntax", "json", "input_size", "utf8", "identifier",
    "depth", "value_type", "kind", "revision", "format", "record_id", "record_shape",
    "caller_result_input", "caller_result_size", "handoff_details", "path_escape",
    "source_range", "source_budget", "source_scope", "platform_schema",
    "platform_arguments", "platform_json", "platform_request", "job_request", "job_event",
}
_UNAVAILABLE = {"file_read", "caller_artifact_unavailable"}


def _path(value):
    if not isinstance(value, str) or not 0 < len(value) <= 512:
        return None
    if "\\" in value or ":" in value or any(ord(c) < 32 for c in value):
        return None
    try:
        value.encode("utf-8")
    except UnicodeError:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or str(path) == ".":
        return None
    return value


def _safe_text(value, pattern):
    return value if isinstance(value, str) and pattern.fullmatch(value) else None


def _identity(args, context):
    """Allow only named scalar identities, never request/configuration payloads."""
    identity = {}
    for destination, aliases in {
        "asset_id": ("asset_id",), "job_id": ("job_id", "job"),
        "task_id": ("task_id", "task"), "candidate_id": ("candidate_id", "candidate"),
        "output_id": ("output_id", "output"), "review_id": ("review_id",),
    }.items():
        for name in aliases:
            value = _safe_text(args.get(name), _ID)
            if value is not None:
                identity[destination] = value
                break
    for name in ("expect", "requirements_hash", "binding_hash", "sha256"):
        value = _safe_text(args.get(name), _HASH)
        if value is not None:
            identity[name] = value
    for name in ("path", "plar_path", "store"):
        value = _path(args.get(name))
        if value is not None:
            identity[name] = value
    # Actual retained identities supersede e.g. the new job ID that was refused.
    for name in ("asset_id", "job_id", "task_id", "candidate_id", "output_id", "review_id"):
        value = _safe_text(context.get(name), _ID)
        if value is not None:
            identity[name] = value
    for name in ("state_hash", "expected_file_sha256", "observed_file_sha256"):
        value = _safe_text(context.get(name), _HASH)
        if value is not None:
            identity[name] = value
    for name in ("store", "path", "plar_path"):
        value = _path(context.get(name))
        if value is not None:
            identity[name] = value
    if isinstance(context.get("job_state"), str) and context["job_state"] in _JOB_STATES:
        identity["job_state"] = context["job_state"]
    return identity


def _selection_read(operation, args, identity):
    if operation.startswith("plar_"):
        path = _path(args.get("path", "plar.txt"))
    else:
        path = identity.get("plar_path")
    if path is None:
        return {}
    arguments = {"path": path}
    if "asset_id" in identity:
        arguments["asset_id"] = identity["asset_id"]
    return {"operation": "pixl_plar_read", "arguments": arguments}


def _state_read(operation, identity, jobs=False):
    if "store" in identity:
        path = identity["store"].rstrip("/") + "/state.px"
    elif operation in {"jobs", "validate", "workflow", "context"}:
        path = identity.get("path")
    else:
        path = None
    if path is None:
        return {}
    return {"operation": "pixl_jobs" if jobs else "pixl_validate", "arguments": {"path": path}}


def error_result(operation, error, args=None):
    """Preserve codes/text and add bounded recovery without executing anything."""
    operation = operation.removeprefix("pixl_").replace("-", "_") if isinstance(operation, str) else ""
    if not _OPERATION.fullmatch(operation):
        operation = ""
    args = args if isinstance(args, dict) else {}
    context = getattr(error, "context", {})
    context = context if isinstance(context, dict) else {}
    identity = _identity(args, context)
    if operation.startswith("plar_") and _path(context.get("path")) is not None:
        plar_path = _path(args.get("path", "plar.txt"))
        if plar_path is not None:
            identity["plar_path"] = plar_path
    code = error.code if isinstance(error, PixlError) else "operation"
    category = "unclassified"
    recovery = {"action": "inspect_error", "detail": "Inspect the retained result and relevant input before choosing a recovery; no operation was retried."}

    if identity.get("job_state") == "unknown":
        category = "uncertain_remote_result"
        recovery = {
            "action": "reconcile_existing_job",
            "detail": "Read the retained job and reconcile the same attempt on its originating connection. Do not dispatch or submit another request.",
            **(_state_read(operation, identity, jobs=True) or _selection_read(operation, args, identity)),
        }
    elif code in {"job_pending", "job_history"} and "job_state" in identity:
        category = "retained_work"
        action = {
            "prepared": "inspect_prepared_job", "submitted": "observe_existing_job",
            "running": "observe_existing_job", "succeeded": "inspect_retained_result",
            "failed": "inspect_retained_failure",
        }[identity["job_state"]]
        recovery = {
            "action": action,
            "detail": "Read the existing job and its next action before deciding what work remains. This error does not authorize another submission.",
            **(_state_read(operation, identity, jobs=True) or _selection_read(operation, args, identity)),
        }
    elif code in _STALE:
        category = "stale_local_state"
        recovery = {
            "action": "reread_and_reconcile",
            "detail": "Reread the relevant identity, compare the intended change and preserve prior evidence. A new hash alone does not authorize changed semantics.",
            **(_selection_read(operation, args, identity) or _state_read(operation, identity, jobs=operation.startswith("job_"))),
        }
        if code == "source_hash":
            recovery = {"action": "reindex_source", "detail": "Retrieve the source's current identity and reassess dependent claims before reading with a new hash."}
            if args.get("scope") == "library":
                recovery.update(operation="pixl_sources", arguments={})
            elif "path" in identity:
                recovery.update(operation="pixl_catalog", arguments={"paths": [identity["path"]]})
        elif code == "caller_artifact_stale":
            recovery = {"action": "reconcile_declared_files", "detail": "Reread the declared files, compare changed bytes and correct the caller declaration before saving. Do not substitute a new hash without reviewing the change."}
    elif code == "unknown_tool":
        category = "missing_capability"
        recovery = {"action": "inspect_tool_inventory", "detail": "Inspect this local server's current tools/list and select a supported operation. This does not establish official provider availability."}
    elif code == "adapter_version":
        category = "missing_capability"
        recovery = {
            "action": "use_compatible_adapter",
            "detail": "Preserve the saved file, its hashes and the original kit. Check spec/adapter-compatibility.md and use a kit supporting this format or an explicitly tested migration. Do not relabel its version, replace hashes, or retry provider work. This is a local format limitation, not an observation of provider availability.",
        }
    elif code == "platform_tool":
        recovery = {"action": "inspect_current_tool_declarations", "detail": "Check the actual connected official tool declaration. A dated local catalog lookup does not establish that a live capability is absent."}
    elif code in _INVALID or isinstance(error, json.JSONDecodeError) or (code == "json_read" and isinstance(error.__cause__, ValueError)):
        category = "invalid_authoring"
        recovery = {"action": "correct_input", "detail": "Inspect the operation's declared schema and relevant source, correct the rejected input, and preserve existing state before retrying the local operation."}
    elif code in _UNAVAILABLE or isinstance(error, OSError) or (code == "json_read" and isinstance(error.__cause__, OSError)):
        category = "unavailable_observation"
        recovery = {"action": "restore_observation", "detail": "Restore access to the named local file or retain its unavailable status. Missing observation is not a failed or passing artistic check; do not repeat remote work to repair a read."}
    elif code in {"handoff_state", "handoff_corrupt"}:
        recovery = {"action": "inspect_retained_state", "detail": "Read the selected allocation and inspect its retained production. Preserve existing snapshots; do not manufacture acceptance or replace corrupt evidence.", **_selection_read(operation, args, identity)}
    elif code == "result_exists":
        recovery = {"action": "choose_fresh_export_path", "detail": "Preserve the existing result and choose a fresh project-relative export path. Reconcile any prior operation outcome before repeating a mutation."}

    return {"error": code, "detail": str(error), "category": category, "recovery": recovery, "identity": identity}
