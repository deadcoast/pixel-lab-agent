"""Read-only literal coverage of declared authored handoff subtrees.

Identity, exact values and review coverage are checked here. Source meaning,
authority, omitted operational carriers and artistic acceptance are not judged.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from .codec import MAX_BYTES, PixlError
from .graph import confined
from .request_review import source_evidence
from .service import parse_json


def _require(condition, detail):
    if not condition:
        raise PixlError("handoff_review", detail)


def _path(root, name):
    _require(isinstance(name, str), "file paths must be relative strings")
    _require(".." not in name.split("/"), "parent traversal is not accepted")
    return confined(root, name)


def _literal(value):
    """JSON-type-aware equality: booleans, integers and decimals stay distinct."""
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    except (TypeError, ValueError, RecursionError) as error:
        raise PixlError("handoff_review", "expected finite JSON values") from error


def _read(root, name):
    path = _path(root, name)
    try:
        _require(path.stat().st_size <= MAX_BYTES, "JSON input exceeds 16 MiB")
        data = path.read_bytes()
        value = parse_json(data)
        _literal(value)  # parse_constant also rejects NaN/Infinity; this catches 1e999.
    except (OSError, ValueError, RecursionError) as error:
        raise PixlError("handoff_review", f"cannot read finite JSON from {name!r}") from error
    return value, {"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(data).hexdigest()}


def _tokens(pointer):
    _require(isinstance(pointer, str) and (pointer == "" or pointer.startswith("/")), "scope and claim pointers must be JSON Pointers")
    _require(re.search(r"~(?![01])", pointer) is None, "JSON Pointer has an invalid tilde escape")
    return tuple(part.replace("~1", "/").replace("~0", "~") for part in pointer.split("/")[1:]) if pointer else ()


def _resolve(value, tokens):
    for token in tokens:
        if isinstance(value, dict):
            _require(token in value, "selected scope does not exist")
            value = value[token]
        elif isinstance(value, list):
            _require(re.fullmatch(r"0|[1-9][0-9]*", token) is not None, "array pointers require canonical nonnegative indices")
            index = int(token)
            _require(index < len(value), "selected array index is out of range")
            value = value[index]
        else:
            raise PixlError("handoff_review", "selected scope traverses a scalar")
    return value


def _leaves(value, pointer):
    if isinstance(value, (dict, list)) and value:
        items = value.items() if isinstance(value, dict) else enumerate(value)
        for key, child in items:
            token = str(key).replace("~", "~0").replace("/", "~1")
            yield from _leaves(child, pointer + "/" + token)
    else:
        yield pointer, value


def _scopes(scopes):
    _require(isinstance(scopes, (list, tuple)) and bool(scopes), "at least one explicit authored scope is required")
    tokens = [_tokens(pointer) for pointer in scopes]
    for index, current in enumerate(tokens):
        for previous in tokens[:index]:
            _require(current != previous, "duplicate authored scopes are not accepted")
            _require(current[:len(previous)] != previous and previous[:len(current)] != current, "overlapping authored scopes are not accepted")
    return tokens


def _citation(root, value, *, carrier=False):
    _require(isinstance(value, dict), "sources and carriers must be objects")
    required = {"path", "sha256", "lines"} | ({"text"} if carrier else set())
    _require(required <= value.keys() <= required | {"locator"}, "source/carrier needs path, sha256 and lines; carriers also need text")
    _path(root, value["path"])
    _require(isinstance(value["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", value["sha256"]) is not None, "source/carrier sha256 must be a lowercase SHA-256")
    _require(isinstance(value["lines"], list), "source/carrier lines must be explicit [first, last] bounds")
    _require("locator" not in value or isinstance(value["locator"], str), "optional locator must be a string")
    if carrier:
        _require(isinstance(value["text"], str), "carrier text must be an exact string")
    observed = source_evidence(root, value, value["sha256"])
    if carrier:
        observed["expected_text"] = value["text"]
        observed["text_matches"] = observed["status"] == "resolved" and len(observed["excerpts"]) == 1 and observed["excerpts"][0]["text"] == value["text"]
    return observed


def report(root, result_path, scopes, review_path=None):
    """Inventory saved leaves independently of optional comparison rows; never write."""
    root = Path(root).resolve()
    _require(root.is_dir(), "root must be an existing consumer directory")
    scope_tokens = _scopes(scopes)
    value, result_binding = _read(root, result_path)
    expected = {}
    for pointer, tokens in zip(scopes, scope_tokens, strict=True):
        expected.update(_leaves(_resolve(value, tokens), pointer))
    result = {
        "version": 1, "operation": "handoff_review", "status": "inventory",
        "result": result_binding, "scopes": list(scopes),
        "inventory": [{"pointer": key, "value": item} for key, item in sorted(expected.items())],
        "semantic_verdict": "not_assessed", "coverage": None, "carriers": [],
        "limits": [
            "Coverage includes every scalar or empty container only inside the explicitly selected authored subtrees.",
            "Exact values, hashes, line ranges and nonempty findings do not prove source support, authority or semantic consistency.",
            "Metadata classification is supplied by the reviewer, not inferred or certified by this tool.",
            "Only explicitly declared carrier excerpts are checked; omitted adopted instructions are not discovered.",
            "No project state, owner confirmation, acceptance or provider action is changed.",
        ],
    }
    if review_path is None:
        return result
    review, review_binding = _read(root, review_path)
    _require(isinstance(review, dict) and set(review) == {"version", "result", "scopes", "claims", "carriers"}, "review needs version, result, scopes, claims and carriers")
    _require(type(review["version"]) is int and review["version"] == 1, "expected review version 1")
    _require(isinstance(review["result"], dict) and set(review["result"]) == {"path", "sha256"}, "review result needs path and sha256")
    reviewed_result = _path(root, review["result"]["path"]).relative_to(root).as_posix()
    _scopes(review["scopes"])
    _require(isinstance(review["claims"], list) and isinstance(review["carriers"], list), "claims and carriers must be lists")
    seen, duplicates, unexpected, changed, incomplete, metadata = set(), [], [], [], [], []
    rows = []
    for row in review["claims"]:
        _require(isinstance(row, dict) and set(row) == {"pointer", "expected", "basis", "finding", "sources"}, "claim needs pointer, expected, basis, finding and sources")
        pointer = row["pointer"]
        _tokens(pointer)
        if pointer in seen:
            duplicates.append(pointer)
        seen.add(pointer)
        if pointer not in expected:
            unexpected.append(pointer)
        elif _literal(row["expected"]) != _literal(expected[pointer]):
            changed.append(pointer)
        _require(isinstance(row["sources"], list), "claim sources must be a list")
        sources = [_citation(root, source) for source in row["sources"]]
        issues = []
        if not isinstance(row["finding"], str) or not row["finding"].strip():
            issues.append("missing_finding")
        if row["basis"] == "metadata":
            metadata.append(pointer)
            if sources:
                issues.append("metadata_must_not_claim_source_comparison")
        elif row["basis"] == "source_comparison":
            if not sources:
                issues.append("missing_source")
        else:
            issues.append("unsupported_basis")
        if any(source["status"] != "resolved" for source in sources):
            issues.append("unresolved_source")
        if issues:
            incomplete.append({"pointer": pointer, "issues": issues})
        rows.append({**row, "source_observations": sources})
    carriers = [_citation(root, carrier, carrier=True) for carrier in review["carriers"]]
    missing = sorted(set(expected) - seen)
    binding_current = reviewed_result == result_binding["path"] and review["result"]["sha256"] == result_binding["sha256"]
    scope_current = set(review["scopes"]) == set(scopes)
    complete = binding_current and scope_current and not any((missing, duplicates, unexpected, changed, incomplete)) and all(carrier["text_matches"] for carrier in carriers)
    result.update(
        status="coverage_complete" if complete else "coverage_incomplete",
        review=review_binding, comparisons=rows, carriers=carriers,
        coverage={"complete": complete, "expected": len(expected), "observed": len(rows),
                  "result_current": binding_current, "scopes_current": scope_current,
                  "missing": missing, "duplicates": duplicates, "unexpected": unexpected,
                  "changed_values": changed, "incomplete": incomplete,
                  "metadata_pointers": metadata, "declared_carriers": len(carriers),
                  "carrier_mismatches": [index for index, carrier in enumerate(carriers) if not carrier["text_matches"]]},
    )
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", help="saved authored JSON, relative to --root")
    parser.add_argument("--root", required=True, help="existing consumer root")
    parser.add_argument("--scope", action="append", required=True, help="whole authored subtree JSON Pointer; repeat for each subtree")
    parser.add_argument("--review", help="version-1 comparison JSON, relative to --root")
    parser.add_argument("--out", help="new report path inside --root; existing parent required")
    args = parser.parse_args(argv)
    try:
        result = report(args.root, args.result, args.scope, args.review)
        encoded = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.out:
            with _path(Path(args.root).resolve(), args.out).open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(encoded)
        else:
            print(encoded, end="")
        return 1 if result["status"] == "coverage_incomplete" else 0
    except (PixlError, OSError, ValueError, RecursionError) as error:
        detail = error.detail if isinstance(error, PixlError) else str(error)
        print(json.dumps({"error": {"code": getattr(error, "code", "handoff_review"), "detail": detail}, "semantic_verdict": "not_assessed"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
