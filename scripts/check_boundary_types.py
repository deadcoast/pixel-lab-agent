"""Check real operation types and expected static refusals without executing fixtures."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
VALID = "tests/typing/valid_boundaries.py"
INVALID = "tests/typing/invalid_boundaries.py"
MARKER = re.compile(r"# expect: ([a-z0-9-]+) \[([a-z0-9-]+)\]")
DIAGNOSTIC = re.compile(r"^(.+?):(\d+)(?::\d+)?: error: (.*?)  \[([a-z0-9-]+)\]$")


def run(command: list[str]) -> dict:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=180, check=False)
        return {"command": command, "exit_code": result.returncode,
                "stdout": result.stdout, "stderr": result.stderr,
                "elapsed_seconds": round(time.monotonic() - started, 3)}
    except subprocess.TimeoutExpired as error:
        def decoded(value):
            return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""
        return {"command": command, "exit_code": None, "error": "mypy timeout after 180 seconds",
                "stdout": decoded(error.stdout), "stderr": decoded(error.stderr),
                "elapsed_seconds": round(time.monotonic() - started, 3)}


def check() -> dict:
    def input_hashes() -> dict[str, str]:
        paths = [*sorted((ROOT / "pixl").glob("*.py")), ROOT / "pyproject.toml", ROOT / "uv.lock",
                 ROOT / VALID, ROOT / INVALID, Path(__file__).resolve()]
        return {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    before = input_hashes()
    expectations = []
    for number, line in enumerate((ROOT / INVALID).read_text(encoding="utf-8").splitlines(), 1):
        if match := MARKER.search(line):
            expectations.append({"label": match[1], "path": INVALID, "line": number, "code": match[2]})
    labels = [row["label"] for row in expectations]
    if not labels or len(set(labels)) != len(labels):
        raise ValueError("Static refusal markers must be nonempty and uniquely labeled")
    with TemporaryDirectory(prefix="pixl-boundary-mypy-") as cache:
        base = [sys.executable, "-B", "-m", "mypy", "--config-file", str(ROOT / "pyproject.toml"),
                "--cache-dir", cache, "--no-pretty", "--no-color-output", "--show-error-codes",
                "--no-error-summary"]
        positive = run([*base, "pixl", VALID])
        negative = run([*base, INVALID])
    diagnostics, unparsed_errors = [], []
    for line in negative["stdout"].splitlines():
        if match := DIAGNOSTIC.match(line):
            path = Path(match[1]).as_posix()
            if Path(path).is_absolute():
                path = Path(path).relative_to(ROOT).as_posix()
            diagnostics.append({"path": path, "line": int(match[2]), "code": match[4], "message": match[3]})
        elif ": error:" in line:
            unparsed_errors.append(line)
    expected = Counter((row["path"], row["line"], row["code"]) for row in expectations)
    actual = Counter((row["path"], row["line"], row["code"]) for row in diagnostics)
    after = input_hashes()
    checks = {
        "configured_runtime_and_positive_consumers_pass": positive["exit_code"] == 0,
        "negative_fixture_rejected": negative["exit_code"] == 1,
        "every_expected_refusal_and_no_extra_errors": expected == actual and not unparsed_errors,
        "no_checker_stderr": not positive["stderr"] and not negative["stderr"],
        "source_and_fixture_inputs_unchanged": before == after,
    }
    return {
        "version": 1, "observed_at": datetime.now(UTC).isoformat(),
        "status": "pass" if all(checks.values()) else "fail",
        "python": sys.version, "mypy": version("mypy"),
        "checks": checks, "passed": sum(checks.values()), "total": len(checks),
        "expected_refusals": expectations, "observed_refusals": diagnostics,
        "unparsed_errors": unparsed_errors, "positive": positive, "negative": negative,
        "source_hashes": before,
        "input_changes": sorted(name for name in before.keys() | after.keys() if before.get(name) != after.get(name)),
        "scope": "Configured mypy over runtime and static-only positive consumers, plus exact expected refusal diagnostics. Fixtures are parsed, never executed. The six selected boundary modules include untyped bodies; other modules retain default scope.",
        "effects": "Writes and removes a temporary mypy cache; suppresses bytecode. No builder, test execution, host/model, provider or production-state operation. Redirected stdout is caller-owned evidence.",
        "limits": ["Type checking does not replace runtime validation of raw JSON, hashes, timestamps, paths or exact integers; bool is an int subtype statically.",
                   "Opaque provider, lineage, continuation and UDL payloads retain their separate runtime contracts.",
                   "No native behavior, artistic outcome or human acceptance is established."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print the complete report including checker diagnostics")
    args = parser.parse_args()
    try:
        report = check()
    except (OSError, ValueError, PackageNotFoundError) as error:
        print(json.dumps({"status": "fail", "error": str(error)}))
        return 2
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Boundary typing: {report['status']} ({report['passed']}/{report['total']} checks)")
        print(f"Expected static refusals: {len(report['expected_refusals'])}; observed: {len(report['observed_refusals'])}")
        if report["status"] != "pass":
            for name in ("positive", "negative"):
                print(f"{name} checker exit: {report[name]['exit_code']}")
                print(report[name]["stdout"] + report[name]["stderr"])
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
