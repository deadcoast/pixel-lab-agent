"""Read exact request/criteria and source excerpts for an independent caller review.

This is evidence preparation, not a semantic consistency or art-acceptance verdict.
"""

import re
from hashlib import sha256
from pathlib import Path
from typing import Any

from . import graph, plar


def source_evidence(root, source, expected, budget=16384):
    """Resolve explicit lines or legacy numbered prose against this file only."""
    local = graph.confined(root, source["path"])
    result = {
        "path": source["path"],
        "sha256": expected,
        "locator": source.get("locator"),
        "absolute_path": str(local),
    }
    if not local.is_file():
        return {**result, "status": "missing"}
    if local.stat().st_size > 64 * 1024 * 1024:
        return {**result, "status": "too_large"}
    data = local.read_bytes()
    actual = sha256(data).hexdigest()
    result.update(observed_sha256=actual)
    if actual != expected:
        return {**result, "status": "changed"}
    try:
        lines = data.decode("utf-8-sig").splitlines(keepends=True)
    except UnicodeError:
        return {
            **result,
            "status": "visual_source",
            "instruction": "Inspect the actual referenced artifact through the host.",
        }
    result["line_count"] = len(lines)
    explicit = source.get("lines")
    if explicit is not None:
        if (
            not isinstance(explicit, list)
            or len(explicit) != 2
            or any(type(n) is not int for n in explicit)
        ):
            return {
                **result,
                "status": "invalid_locator",
                "reason": "lines must be [first, last] integer bounds",
            }
        ranges = [explicit]
    else:
        ranges = [
            [int(a), int(b or a)]
            for a, b in re.findall(
                r"\blines?\s+(\d+)(?:\s*[-–]\s*(\d+))?",
                source.get("locator", ""),
                re.IGNORECASE,
            )
        ]
    if not ranges:
        return {
            **result,
            "status": "unresolved_locator",
            "instruction": "Use file-local lines [first,last] or inspect the named source location; no locator is assumed verified.",
        }
    if any(not 1 <= start <= end <= len(lines) for start, end in ranges):
        return {
            **result,
            "status": "invalid_locator",
            "requested_lines": ranges,
            "reason": f"Source has {len(lines)} lines; one or more bounds are outside it.",
        }
    excerpts: list[dict[str, Any]] = [
        {"lines": [start, end], "text": "".join(lines[start - 1 : end])}
        for start, end in ranges
    ]
    if sum(len(item["text"].encode("utf-8")) for item in excerpts) > budget:
        return {**result, "status": "needs_narrower_range", "requested_lines": ranges}
    return {
        **result,
        "status": "resolved",
        "excerpts": excerpts,
        "scope": "Exact cited text only; its meaning and support for the criterion need caller comparison.",
    }


def report(root, packet_path, asset_id=None, path="plar.txt"):
    from jsonschema import Draft202012Validator

    from .plar_prepare import SCHEMA, _artifact, _json_file, _require

    root = Path(root).resolve()
    packet, digest, packet_path = _json_file(root, packet_path)
    _require(
        type(packet.get("version")) is int and packet["version"] == 1,
        "expected request-review version 1",
    )
    _require(isinstance(packet.get("sources"), list), "packet sources must be a list")
    sources: dict[str, dict[str, Any]] = {}
    for source in packet["sources"]:
        _require(
            isinstance(source, dict) and {"path", "sha256", "role"} <= source.keys(),
            "packet sources need path, sha256 and role",
        )
        name = graph.confined(root, source["path"]).relative_to(root).as_posix()
        _require(
            name not in sources or sources[name]["sha256"] == source["sha256"],
            "conflicting source identities",
        )
        sources[name] = source
    pointer = packet.get("request")
    _require(
        isinstance(pointer, dict) and pointer.get("kind") == "provider_arguments",
        "review expects exact provider arguments, not a creative brief",
    )
    request, request_hash, request_path = _artifact(root, packet.get("request"))
    connection = None
    if "connection" in pointer:
        value, connection_hash, connection_path = _artifact(root, pointer["connection"])
        connection = {
            "path": connection_path,
            "sha256": connection_hash,
            "provider": value.get("provider"),
            "discovery": value.get("discovery"),
            "authorization": value.get("authorization"),
        }

    plan, plan_hash, plan_path = _artifact(root, packet.get("criteria"))
    error = next(Draft202012Validator(SCHEMA).iter_errors(plan), None)
    _require(error is None, f"candidate plan: {error.message if error else ''}")
    evidence, comparisons, diagnostics = [], [], []
    if (
        connection
        and "provider" in pointer
        and pointer["provider"] != connection["provider"]
    ):
        diagnostics.append(
            {
                "status": "provider_mismatch",
                "packet": pointer["provider"],
                "connection": connection["provider"],
            }
        )

    source_bindings = []
    for source in packet["sources"]:
        local = graph.confined(root, source["path"])
        name = local.relative_to(root).as_posix()
        observed = (
            graph.file_hash(local)
            if local.is_file() and local.stat().st_size <= 64 * 1024 * 1024
            else None
        )
        status = (
            "current"
            if observed == source["sha256"]
            else "changed"
            if observed is not None
            else "unavailable"
        )
        source_bindings.append(
            {**source, "observed_sha256": observed, "binding": status}
        )
        if status != "current":
            diagnostics.append({"source": name, "status": status})
        pointers = [source] if "locator" in source or "lines" in source else []
        locators = source.get("locators", [])
        if isinstance(locators, list) and all(
            isinstance(value, str) for value in locators
        ):
            pointers.extend({**source, "locator": value} for value in locators)
        else:
            diagnostics.append(
                {"packet_source": name, "status": "unresolved_locator_format"}
            )
        for citation in pointers:
            item = source_evidence(root, citation, source["sha256"])
            if item not in evidence:
                evidence.append(item)
            source_bindings[-1].setdefault("source_evidence", []).append(
                evidence.index(item)
            )
            if item["status"] != "resolved":
                diagnostics.append(
                    {
                        "packet_source": name,
                        "locator": citation.get("locator"),
                        "status": item["status"],
                    }
                )

    for output in plan["outputs"]:
        for criterion in output["criteria"]:
            indices = []
            for source in criterion["sources"]:
                name = graph.confined(root, source["path"]).relative_to(root).as_posix()
                _require(
                    name in sources, f"criterion source absent from packet: {name}"
                )
                item = source_evidence(root, source, sources[name]["sha256"])
                if item not in evidence:
                    evidence.append(item)
                index = evidence.index(item)
                indices.append(index)
                if item["status"] != "resolved":
                    diagnostics.append(
                        {
                            "output": output["id"],
                            "criterion": criterion["id"],
                            "source": index,
                            "status": item["status"],
                        }
                    )
            comparisons.append(
                {
                    "output": output["id"],
                    **criterion,
                    "source_evidence": indices,
                    "comparison": "unperformed",
                }
            )
    selected = plar.read(root, path, asset_id) if asset_id else None
    if selected and packet.get("requirements_hash") != selected["requirements_hash"]:
        diagnostics.append(
            {
                "status": "changed_selection",
                "packet": packet.get("requirements_hash"),
                "current": selected["requirements_hash"],
            }
        )
    return {
        "version": 1,
        "packet": {"path": packet_path, "sha256": digest},
        "request": {
            "path": request_path,
            "sha256": request_hash,
            "tool": packet["request"].get("tool"),
            "provider": pointer.get("provider"),
            "provider_simulated_assertion": pointer.get("provider_simulated"),
            "connection": connection,
            "arguments": request,
        },
        "criteria": {
            "path": plan_path,
            "sha256": plan_hash,
            "scope": plan["scope"],
            "comparisons": comparisons,
        },
        "candidate_controls": [
            {"output": o["id"], "contract": o["contract"]} for o in plan["outputs"]
        ],
        "sources": source_bindings,
        "choices": packet.get("choices", []),
        "source_evidence": evidence,
        "diagnostics": diagnostics,
        "production": selected.get("production") if selected else None,
        "caller_comparison": "unperformed",
        "consistent": None,
        "scope": "Read-only exact evidence. Resolved lines do not establish semantic entailment, contract consistency, execution or asset acceptance.",
    }
