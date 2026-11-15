"""Measure retained PIXL histories read-only; print JSON, never publish evidence."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
import platform
import statistics
import subprocess
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OPERATIONS = {
    "parse", "store_load", "canonical_digest", "raw_state_sha256",
    "structural_validation", "file_validation", "validate_report",
    "authoring_context", "complete_context", "family_report",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    """Match the public CLI's JSON representation, including its final newline."""
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def stats(values):
    """Nearest-rank p95; raw integer nanoseconds remain the primary evidence."""
    ordered = sorted(values)
    if not ordered:
        return None
    return {"count": len(ordered), "min_ns": ordered[0], "max_ns": ordered[-1],
            "median_ns": statistics.median(ordered),
            "p95_ns": ordered[math.ceil(len(ordered) * 0.95) - 1]}


def linked(path):
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def no_links(path):
    for part in (path, *path.parents):
        if linked(part):
            raise ValueError(f"symlink or junction input is not supported: {part.name}")


def relative_path(value, label):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError(f"{label} must be a nonempty forward-slash relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in (".", "..") for part in value.split("/")):
        raise ValueError(f"{label} must remain inside its declared root")
    return Path(value)


def read_manifest(path, repository=ROOT):
    no_links(path.absolute())
    data = json.loads(path.read_bytes())
    if not isinstance(data, dict) or type(data.get("version")) is not int or data["version"] != 1:
        raise ValueError("manifest version must be integer 1")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("manifest cases must be a nonempty list")
    seen = set()
    normalized = []
    for case in cases:
        if not isinstance(case, dict):
            raise TypeError("each case must be an object")
        ident = case.get("id")
        if not isinstance(ident, str) or not ident or ident in seen:
            raise ValueError("case ids must be unique nonempty strings")
        seen.add(ident)
        root_value = case.get("root")
        if not isinstance(root_value, str) or not root_value:
            raise ValueError(f"{ident}: root must name an existing directory")
        root = Path(root_value)
        if not root.is_absolute():
            root = repository / relative_path(root_value, "root")
        no_links(root.absolute())
        root = root.resolve(strict=True)
        if not root.is_dir() or root == Path(root.anchor):
            raise ValueError(f"{ident}: root must be a project directory, not a drive")
        state = root / relative_path(case.get("path"), "path")
        no_links(state)
        if state.name != "state.px" or not state.is_file():
            raise ValueError(f"{ident}: path must name an existing state.px")
        if not isinstance(case.get("focus"), str) or not case["focus"]:
            raise ValueError(f"{ident}: focus must be a nonempty record id")
        if "output_id" in case and (not isinstance(case["output_id"], str) or not case["output_id"]):
            raise ValueError(f"{ident}: output_id must be a nonempty record id")
        expected = case.get("expected_errors", {})
        if not isinstance(expected, dict) or any(
            name not in OPERATIONS or not isinstance(codes, list) or not codes
            or any(not isinstance(code, str) or not code for code in codes)
            for name, codes in expected.items()
        ):
            raise ValueError(f"{ident}: expected_errors must map operation names to nonempty code lists")
        if "family_report" in expected and "output_id" not in case:
            raise ValueError(f"{ident}: family_report expectations need output_id")
        normalized.append({**case, "root_path": root, "state_path": state})
    return normalized


def identity(path):
    before = path.stat()
    digest = sha(path.read_bytes())
    after = path.stat()
    if (before.st_size, before.st_mtime_ns, before.st_mode) != (after.st_size, after.st_mtime_ns, after.st_mode):
        raise ValueError(f"input changed while hashing: {path.name}")
    return {"bytes": after.st_size, "sha256": digest, "mtime_ns": after.st_mtime_ns,
            "mode": after.st_mode}


def tree_identity(root):
    """No ignored subtrees: retained histories, receipts and existing caches count."""
    result = {}
    for path in [root, *sorted(root.rglob("*"))]:
        if linked(path):
            raise ValueError(f"symlink or junction input is not supported: {path.relative_to(root)}")
        name = path.relative_to(root).as_posix()
        if path.is_file():
            result[name] = {"kind": "file", **identity(path)}
        elif path.is_dir():
            info = path.stat()
            result[name] = {"kind": "directory", "mtime_ns": info.st_mtime_ns, "mode": info.st_mode}
        else:
            raise ValueError(f"nonregular input is not supported: {name}")
    return result


def changed(before, after):
    return sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name))


def source_identity():
    paths = [path for path in (ROOT / "pixl").rglob("*")
             if path.is_file() and path.suffix in (".py", ".json") and "__pycache__" not in path.parts]
    paths += [Path(__file__).resolve(), ROOT / "pyproject.toml", ROOT / "uv.lock"]
    return {path.relative_to(ROOT).as_posix(): identity(path) for path in sorted(paths)}


def dependency_versions():
    result = {}
    for name in ("jsonschema", "pillow"):
        try:
            result[name] = version(name)
        except PackageNotFoundError:
            result[name] = None
    return result


def runtime():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from pixl import codec, graph, service, store

    return codec, graph, service, store


def observe(function, codec, public=False):
    started = time.perf_counter_ns()
    try:
        value = function()
    except codec.PixlError as error:
        elapsed = time.perf_counter_ns() - started
        return {"elapsed_ns": elapsed, "outcome": {"status": "refused", "code": error.code,
                                                   "detail": error.detail}}
    except Exception as error:  # noqa: BLE001 - retain unexpected operation failures as failed measurements
        elapsed = time.perf_counter_ns() - started
        return {"elapsed_ns": elapsed, "outcome": {"status": "unexpected_error",
                    "type": type(error).__name__, "detail": str(error)}}
    elapsed = time.perf_counter_ns() - started
    serialization_started = time.perf_counter_ns()
    try:
        if isinstance(value, codec.Document):
            encoded, encoding = codec.encode(value), "canonical_px"
        elif isinstance(value, bytes):
            encoded, encoding = value, "raw_bytes"
        else:
            encoded, encoding = json_bytes(value), "pretty_json_utf8_newline"
        serialization_ns = time.perf_counter_ns() - serialization_started
        outcome = {"status": "ok", "sha256": sha(encoded), "bytes": len(encoded), "encoding": encoding}
        row = {"elapsed_ns": elapsed, "outcome": outcome}
        if public:
            row["serialization_ns"] = serialization_ns
            if isinstance(value, dict) and isinstance(value.get("wire"), str):
                wire = value["wire"].encode("utf-8")
                outcome["wire_bytes"] = len(wire)
                outcome["wire_sha256"] = sha(wire)
        return row
    except Exception as error:  # noqa: BLE001 - preserve the completed timing when result encoding fails
        return {"elapsed_ns": elapsed, "outcome": {"status": "unexpected_error",
                    "type": type(error).__name__, "detail": "result encoding: " + str(error)}}


def summarize(warmups, samples, expected_codes=()):
    rows = warmups + samples
    outcomes = [row["outcome"] for row in rows]
    stable = all(value == outcomes[0] for value in outcomes)
    matched = all(
        value["status"] == "refused" and value["code"] in expected_codes
        if expected_codes else value["status"] == "ok"
        for value in outcomes
    )
    return {"warmups": warmups, "samples": samples, "timing": stats([r["elapsed_ns"] for r in samples]),
            "serialization_timing": stats([r["serialization_ns"] for r in samples if "serialization_ns" in r]),
            "stable": stable, "expected_error_codes": list(expected_codes), "expectation_matched": matched,
            "status": ("observed_expected_refusal" if expected_codes else "measured") if stable and matched else "fail"}


def measure(function, codec, warmups, iterations, expected_codes=(), public=False):
    warm = [observe(function, codec, public) for _ in range(warmups)]
    samples = [observe(function, codec, public) for _ in range(iterations)]
    return summarize(warm, samples, expected_codes)


def operations(case, codec, graph, service, store):
    state, root = case["state_path"], case["root_path"]
    raw = state.read_bytes()
    doc = codec.parse(raw)
    args = {"path": case["path"], "focus": case["focus"]}
    values = {
        "parse": (lambda: codec.parse(raw), False),
        "store_load": (lambda: store.load(state.parent), False),
        "canonical_digest": (lambda: codec.digest(doc), False),
        "raw_state_sha256": (lambda: graph.file_hash(state), False),
        "structural_validation": (lambda: graph.validate(doc), False),
        "file_validation": (lambda: graph.validate(doc, root), False),
        "validate_report": (lambda: service.call("pixl_validate", {"path": case["path"]}, root), True),
        "authoring_context": (lambda: service.call("pixl_context", {**args, "view": "authoring"}, root), True),
        "complete_context": (lambda: service.call("pixl_context", args, root), True),
    }
    if "output_id" in case:
        values["family_report"] = (lambda: service.call("pixl_family", {
            "path": case["path"], "output": case["output_id"]}, root), True)
    dimensions = {"state_bytes": len(raw), "state_file_sha256": sha(raw),
                  "canonical_state_sha256": codec.digest(doc), "revision": doc.revision,
                  "format": doc.format, "records": len(doc.records),
                  "record_kinds": dict(sorted(Counter(r.kind for r in doc.records.values()).items())),
                  "durable_journal_prefixes": sum(len(r.fields["ev"]) for r in doc.records.values()
                                                  if r.kind == "J" and "jr" in r.fields)}
    return values, dimensions


def child_observation(case):
    started = time.perf_counter_ns()
    codec, _graph, service, _store = runtime()
    imported = time.perf_counter_ns() - started
    result = observe(lambda: service.call("pixl_context", {
        "path": case["path"], "focus": case["focus"], "view": "authoring"}, case["root_path"]), codec, True)
    return {"runtime_import_ns": imported, **result}


def captured_output(stdout, stderr):
    """Retain exact bytes from capture_output=True, including invalid UTF-8."""
    return {"output_encoding": "base64 of exact captured bytes",
            "stdout_base64": base64.b64encode(stdout or b"").decode("ascii"),
            "stderr_base64": base64.b64encode(stderr or b"").decode("ascii")}


def fresh_processes(manifest, case, count, timeout):
    samples = []
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [sys.executable, "-B", str(Path(__file__).resolve()), "--manifest", str(manifest),
               "--child-case", case["id"]]
    for _ in range(count):
        started = time.perf_counter_ns()
        completed = None
        try:
            completed = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
                                       timeout=timeout, check=False)
            elapsed = time.perf_counter_ns() - started
            if completed.returncode != 0 or completed.stderr:
                row = {"elapsed_ns": elapsed, "outcome": {"status": "unexpected_error",
                       "type": "child_process", "exit_code": completed.returncode,
                       **captured_output(completed.stdout, completed.stderr)}}
            else:
                result = json.loads(completed.stdout)
                if not isinstance(result, dict) or not isinstance(result.get("outcome"), dict):
                    raise ValueError("child output must contain an observation object")
                outcome = result["outcome"]
                required = {"ok": ("sha256", "bytes", "encoding"), "refused": ("code", "detail"),
                            "unexpected_error": ("type", "detail")}.get(outcome.get("status"))
                if required is None or any(key not in outcome for key in required):
                    raise ValueError("child observation has an invalid outcome shape")
                row = {"elapsed_ns": elapsed, "outcome": result["outcome"],
                       "child": result, "exit_code": completed.returncode}
        except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError) as error:
            row = {"elapsed_ns": time.perf_counter_ns() - started,
                   "outcome": {"status": "unexpected_error", "type": type(error).__name__, "detail": str(error)}}
            if isinstance(error, subprocess.TimeoutExpired):
                row["outcome"].update(captured_output(error.stdout, error.stderr))
            elif completed is not None:
                row["outcome"].update(exit_code=completed.returncode,
                                      **captured_output(completed.stdout, completed.stderr))
        samples.append(row)
    if not samples:
        return {"status": "not_measured", "samples": [], "reason": "--fresh-processes 0"}
    return {**summarize([], samples, case.get("expected_errors", {}).get("authoring_context", [])),
            "scope": "Parent wall time includes probe startup, standard/runtime imports, manifest read, authoring operation, full result serialization for size/hash, compact probe JSON output and exit. This is not the full CLI transport. OS filesystem caches are not flushed."}


def run(manifest, warmups=2, iterations=15, fresh=3, timeout=120):
    manifest = Path(manifest).absolute()
    manifest_before = identity(manifest)
    cases = read_manifest(manifest)
    sources = source_identity()
    # Take all baselines before measuring any case, including shared/overlapping roots.
    roots_before = {case["id"]: tree_identity(case["root_path"]) for case in cases}
    started = time.perf_counter_ns()
    codec, graph, service, store = runtime()
    imported = time.perf_counter_ns() - started
    results = []
    for case in cases:
        row = {"id": case["id"], "path": case["path"], "focus": case["focus"],
               "inputs": roots_before[case["id"]], "operations": {}}
        try:
            functions, dimensions = operations(case, codec, graph, service, store)
            row["dimensions"] = dimensions
            for name, (function, public) in functions.items():
                row["operations"][name] = measure(function, codec, warmups, iterations,
                    case.get("expected_errors", {}).get(name, []), public)
            row["fresh_process_authoring"] = fresh_processes(manifest, case, fresh, timeout)
        except Exception as error:  # noqa: BLE001 - one failed fixture must not discard other measurements
            row["setup_error"] = {"type": type(error).__name__, "detail": str(error)}
            if isinstance(error, codec.PixlError):
                row["setup_error"].update(code=error.code, detail=error.detail)
        results.append(row)
    for case, row in zip(cases, results, strict=True):
        try:
            row["input_changes"] = changed(roots_before[case["id"]], tree_identity(case["root_path"]))
        except (OSError, ValueError) as error:
            row["input_changes"] = ["inventory_unavailable"]
            row["preservation_error"] = str(error)
        fresh_result = row.get("fresh_process_authoring", {})
        row["status"] = "pass" if (
            not row["input_changes"] and "setup_error" not in row
            and all(value["status"] != "fail" for value in row["operations"].values())
            and fresh_result.get("status") != "fail"
            and (fresh_result.get("status") == "not_measured" or
                 fresh_result["samples"][0]["outcome"] == row["operations"]["authoring_context"]["samples"][0]["outcome"])
        ) else "fail"
    preservation_errors = []
    try:
        source_changes = changed(sources, source_identity())
    except (OSError, ValueError) as error:
        source_changes = ["inventory_unavailable"]
        preservation_errors.append({"scope": "runtime_sources", "detail": str(error)})
    try:
        manifest_unchanged = manifest_before == identity(manifest)
    except (OSError, ValueError) as error:
        manifest_unchanged = False
        preservation_errors.append({"scope": "manifest", "detail": str(error)})
    return {"version": 1, "observed_at": datetime.now(UTC).isoformat(),
            "status": "pass" if all(row["status"] == "pass" for row in results)
                      and not source_changes and manifest_unchanged else "fail",
            "configuration": {"warmups": warmups, "iterations": iterations, "fresh_processes": fresh,
                              "timeout_seconds": timeout, "p95_method": "nearest rank"},
            "environment": {"python": sys.version, "implementation": platform.python_implementation(),
                            "platform": platform.platform(), "machine": platform.machine(),
                            "processor": platform.processor(), "logical_cpus": os.cpu_count(),
                            "dependencies": dependency_versions(),
                            "perf_counter_resolution_seconds": time.get_clock_info("perf_counter").resolution},
            "manifest": manifest_before, "manifest_unchanged": manifest_unchanged,
            "preservation_errors": preservation_errors,
            "sources": sources, "source_changes": source_changes,
            "runtime_import_ns": imported, "cases": results,
            "effects": "Read-only input/runtime/manifest reads and isolated child processes; no excluded fixture subtrees, provider requests, builds or file publication. Bytecode is disabled. Caller-owned stdout capture is outside the measured inputs.",
            "limits": ["Warm samples follow input hashing and setup; neither filesystem nor CPU caches are flushed.",
                       "Fresh child processes are Python/process-start measurements, not cold disk measurements.",
                       "Component costs overlap; timings are not additive. No CPU affinity, load isolation or cross-machine performance claim.",
                       "Expected refusals are retained failed operations, not successful context or validation results.",
                       "Authoring orientation and complete context have different semantics; JSON size is not a reasoning-quality measure.",
                       "No native model behavior, provider execution, artistic quality or human acceptance is established."]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--warmups", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=15)
    parser.add_argument("--fresh-processes", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=120, help="seconds per fresh child process")
    parser.add_argument("--child-case", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.warmups < 0 or args.iterations < 1 or args.fresh_processes < 0 or args.timeout < 1:
            raise ValueError("warmups/fresh-processes must be nonnegative; iterations/timeout must be positive")
        if args.child_case is not None:
            cases = read_manifest(args.manifest)
            matches = [case for case in cases if case["id"] == args.child_case]
            if len(matches) != 1:
                raise ValueError("unknown child case")
            report = child_observation(matches[0])
            exit_code = 0  # Parent evaluates outcome against declared expectations.
        else:
            report = run(args.manifest, args.warmups, args.iterations, args.fresh_processes, args.timeout)
            exit_code = 0 if report["status"] == "pass" else 1
    except (OSError, ValueError, KeyError, TypeError) as error:
        report = {"version": 1, "status": "configuration_error", "error": {"type": type(error).__name__, "detail": str(error)}}
        exit_code = 2
    sys.stdout.buffer.write(json_bytes(report))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
