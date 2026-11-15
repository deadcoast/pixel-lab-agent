"""Bounded caller presentation over an unchanged immutable handoff snapshot."""

import json
from collections import Counter

from jsonschema import Draft202012Validator, ValidationError

from . import graph
from .codec import PixlError

MAX_CALLER_BYTES = 8192
MAX_INLINE_RESUME_BYTES = 4096
MAX_INLINE_DELIVERY_BYTES = 2048

FILE_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["path", "sha256", "role"],
    "properties": {
        "path": {"type": "string", "minLength": 1, "maxLength": 512},
        "sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "role": {"type": "string", "minLength": 1, "maxLength": 96},
    },
}
FILES_SCHEMA = {"type": "array", "maxItems": 12, "uniqueItems": True, "items": FILE_SCHEMA}
TEXT_SCHEMA = {"type": "string", "minLength": 1, "maxLength": 600}
ISSUE_CATEGORIES = [
    "invalid_authoring", "stale_local_state", "missing_capability",
    "uncertain_remote_result", "unavailable_observation", "unfinished_work",
]
CALLER_SCHEMA = {
    "type": "object", "additionalProperties": False,
    "properties": {
        "summary": TEXT_SCHEMA,
        "artifacts": FILES_SCHEMA,
        "reports": FILES_SCHEMA,
        "issues": {
            "type": "array", "maxItems": 12,
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["category", "summary"],
                "properties": {
                    "category": {"enum": ISSUE_CATEGORIES},
                    "summary": TEXT_SCHEMA, "recovery": TEXT_SCHEMA,
                },
            },
        },
        "integration": {
            "type": "object", "additionalProperties": False,
            "required": ["status", "summary"],
            "properties": {
                "status": {"enum": ["pass", "fail", "unavailable", "not_performed", "not_in_scope"]},
                "summary": TEXT_SCHEMA, "evidence": FILES_SCHEMA,
            },
        },
    },
}


def _encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def prepare(root, details):
    """Validate only the opt-in caller block; never reinterpret legacy details."""
    if "caller" not in details:
        return {"present": False, "basis": "agent_authored", "reason": "No details.caller block was supplied; read details_ref for the retained observations."}
    caller = details["caller"]
    try:
        data = _encoded(caller)
    except (TypeError, ValueError, UnicodeError, RecursionError) as error:
        raise PixlError("caller_result_input", "details.caller must contain finite UTF-8 JSON") from error
    if len(data) > MAX_CALLER_BYTES:
        raise PixlError("caller_result_size", "details.caller exceeds 8192 UTF-8 bytes; retain detailed observations in linked report files")
    try:
        Draft202012Validator(CALLER_SCHEMA).validate(caller)
    except ValidationError as error:
        raise PixlError("caller_result_input", "details.caller violates the bounded caller-result schema; inspect spec/caller-result.md") from error
    # Freeze caller-owned input and check only declared local files, never URLs.
    caller = json.loads(data)
    files = [*caller.get("artifacts", []), *caller.get("reports", []), *caller.get("integration", {}).get("evidence", [])]
    for reference in files:
        path = graph.confined(root, reference["path"])
        try:
            observed = graph.file_hash(path)
        except OSError as error:
            raise PixlError("caller_artifact_unavailable", "A declared caller file cannot be read; restore or remove the declaration before saving",
                            context={"path": reference["path"], "expected_file_sha256": reference["sha256"]}) from error
        if observed != reference["sha256"]:
            raise PixlError("caller_artifact_stale", "A declared caller file differs from its supplied SHA-256; reread the actual file and reconcile the result before saving",
                            context={"path": reference["path"], "expected_file_sha256": reference["sha256"], "observed_file_sha256": observed})
    return {
        "present": True, "basis": "agent_authored",
        "file_verification": "Declared file bytes matched their SHA-256 at this observation; roles and judgments are agent-authored.",
        **caller,
    }


def _locator(receipt, data, field, pointer=None):
    """Exact physical lines for a root field in the existing pretty JSON format."""
    lines = data.decode("utf-8").splitlines(keepends=True)
    prefix = "  " + json.dumps(field) + ":"
    start = next(i for i, line in enumerate(lines) if line.startswith(prefix))
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith('  "') or lines[i].startswith("}")), len(lines))
    return {
        "path": receipt["path"], "sha256": receipt["sha256"],
        "start": start + 1, "end": end,
        "bytes": len("".join(lines[start:end]).encode("utf-8")),
        "json_pointer": pointer or "/" + field,
    }


def project(receipt, document, selected, data, caller):
    """Present captured facts; do not reload state or decide assignment acceptance."""
    production = selected["production"]
    criteria = [q for output in production.get("outputs", []) for q in output.get("requirements", [])]
    job_rows = production.get("jobs", [])
    resume = document["resume"]
    delivery = resume.get("delivery")
    delivery_inline = len(_encoded(delivery)) <= MAX_INLINE_DELIVERY_BYTES
    resume_bytes = len(_encoded(resume))
    facts = {
        "task": production["task"], "task_state": production["task_state"],
        "selection_current": production["selection_current"],
        "criteria": {
            "total": len(criteria),
            "by_status": dict(sorted(Counter(q["status"] for q in criteria).items())),
            "unresolved": sum(q["status"] != "pass" for q in criteria),
            "scope": "Current nominees only; absent verdicts remain unperformed.",
        },
        "jobs": {
            "total": len(job_rows), "pending": len(production.get("pending_jobs", [])),
            "by_state": dict(sorted(Counter(j["state"] for j in job_rows).items())),
        },
        "delivery_observed": delivery is not None,
        "delivery_complete": delivery.get("complete") if delivery is not None else None,
        "delivery_inline": delivery_inline,
        "scope": "Derived local state and supplied observations; these facts do not determine assignment status or establish undeclared visual/engine checks.",
    }
    if delivery_inline:
        facts["delivery"] = delivery
    else:
        facts["delivery_ref"] = _locator(receipt, data, "resume", "/resume/delivery")
    result = {
        **receipt, "view": "caller", "store": resume["store"],
        "assignment": {"status": document["details"]["status"], "basis": "agent_authored"},
        "caller": caller, "production": facts,
        "details_ref": _locator(receipt, data, "details"),
        "resume_ref": _locator(receipt, data, "resume"),
        "resume_inline": resume_bytes <= MAX_INLINE_RESUME_BYTES,
        "resume_bytes": resume_bytes,
        "refresh": {"operation": "pixl_plar_read", "arguments": {"path": document["selection"]["path"], "asset_id": document["asset_id"]}},
    }
    if result["resume_inline"]:
        result["resume"] = resume
    return result
