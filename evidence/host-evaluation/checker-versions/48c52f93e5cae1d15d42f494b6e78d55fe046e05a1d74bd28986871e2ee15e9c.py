"""Verify retained trial identities and replay saved PIXL state without a model."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evaluations.host_trials import EVIDENCE, REPO, freeze, sha, verify_run, write_json


def retained_state_paths(artifacts: dict[str, str]) -> list[str]:
    """Replay recorded store heads wherever a host chose to save the store."""
    return sorted(path for path in artifacts if Path(path).name == "state.px")


def main() -> None:
    identity = freeze()
    rows = []
    for trial in sorted((EVIDENCE / "runs").iterdir()):
        if not (trial / "record.json").is_file():
            rows.append({"attempt": trial.name, "errors": ["trial has no final record"]})
            continue
        record = json.loads((trial / "record.json").read_text(encoding="utf-8"))
        errors = verify_run(trial)
        archived_runner = EVIDENCE / "runner-versions" / (record["runner_sha256"] + ".py")
        if not archived_runner.is_file() or sha(archived_runner) != record["runner_sha256"]:
            errors.append("executed runner version missing or changed")
        if record["bundle_manifest_sha256"] != identity["bundle_manifest_sha256"]:
            errors.append("unexpected package baseline")
        row = {"attempt": trial.name, "record_sha256": sha(trial / "record.json"), "errors": errors,
               "execution_status": record["execution_status"], "state_replay": [], "state_validation_errors": [],
               "state_paths": retained_state_paths(record["artifacts"])}
        if row["state_paths"] and not errors:
            with tempfile.TemporaryDirectory(prefix="pixl-evidence-replay-") as folder:
                project = Path(folder)
                shutil.copytree(trial / "project", project, dirs_exist_ok=True)
                package = project / ".agents" / "skills" / "pixl-kit"
                shutil.copytree(EVIDENCE / "package", package)
                for state_path in row["state_paths"]:
                    for operation in ("validate", "workflow", "jobs"):
                        command = [str(REPO / ".venv" / "Scripts" / "python.exe"), "-I",
                                   str(package / "scripts" / "pixl.py"), operation, state_path, "--root", str(project)]
                        result = subprocess.run(command, cwd=project, text=True, encoding="utf-8", capture_output=True, check=False, timeout=45)
                        row["state_replay"].append({"state_path": state_path, "command": command, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
                        if result.returncode:
                            row["state_validation_errors"].append(f"retained state {state_path} {operation} failed")
        rows.append(row)
    evidence_error_count = sum(len(row["errors"]) for row in rows)
    state_validation_error_count = sum(len(row.get("state_validation_errors", [])) for row in rows)
    report = {"purpose": "Evidence integrity and deterministic replay only; no behavioral scoring or provider execution.",
              "bundle_manifest_sha256": identity["bundle_manifest_sha256"], "runs": rows,
              "evidence_error_count": evidence_error_count,
              "state_validation_error_count": state_validation_error_count,
              "error_count": evidence_error_count + state_validation_error_count}
    write_json(EVIDENCE / "integrity.json", report)
    print(json.dumps({"runs": len(rows), "errors": report["error_count"]}))
    raise SystemExit(bool(report["error_count"]))


if __name__ == "__main__":
    main()
