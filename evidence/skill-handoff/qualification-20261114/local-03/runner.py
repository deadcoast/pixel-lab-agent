"""Retain the default-fixture portability regression and focused lint results."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent


if __name__ == "__main__":
    if (OUT / "RESULT.json").exists():
        raise ValueError("Retain prior results and use a new evidence directory")
    commands = [
        ("tests", [sys.executable, "-B", "-m", "unittest", "tests.test_skill_handoff_trials", "tests.test_native_trial_records", "-v"]),
        ("ruff", [sys.executable, "-B", "-m", "ruff", "check", "evaluations/skill_handoff_trials.py", "tests/test_skill_handoff_trials.py"]),
    ]
    results = []
    for name, command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True)
        for stream in ("stdout", "stderr"):
            with (OUT / (name + "-" + stream + ".txt")).open("xb") as output:
                output.write(getattr(result, stream))
        results.append({"name": name, "command": command, "returncode": result.returncode})
    files = ["evaluations/skill_handoff_trials.py", "tests/test_skill_handoff_trials.py",
             "evaluations/native_trial_records.py", "evaluations/request_review_trials.py"]
    record = {"status": "pass" if all(row["returncode"] == 0 for row in results) else "fail", "commands": results,
        "source_hashes": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in files},
        "scope": "Local maintainer preparation/retention and existing recorder regression. Adds a fresh-checkout-like default preparation with no ignored predecessor tree. No model, provider, runtime or package build."}
    with (OUT / "RESULT.json").open("x", encoding="utf-8") as stream:
        json.dump(record, stream, indent=2)
        stream.write("\n")
    print(json.dumps(record, indent=2))
