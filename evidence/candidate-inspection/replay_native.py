"""Verify both frozen inspection series and replay retained stores without models."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[1]
sys.path.insert(0, str(REPO))
from evaluations.host_trials import inventory, sha, verify_run


def run():
    results = []
    for series_name in ("native-operation", "native-operation-clarified"):
        series = BASE / series_name
        identity = json.loads((series / "identity.json").read_text(encoding="utf-8"))
        assert inventory(series / "package") == identity["package_files"]
        protocol = json.loads((series / "inspection-protocol.json").read_text(encoding="utf-8"))
        assert sha(series / "protocol-source.py") == protocol["wrapper_sha256"]
        assert sha(series / "fixture-inputs/seeded-project.zip") == protocol["seed_zip_sha256"]
        assert sha(series / "discovery/codex-session-overrides.json") == protocol["codex_session_overrides_sha256"]
        for trial in sorted((series / "runs").iterdir()):
            record = json.loads((trial / "record.json").read_text(encoding="utf-8"))
            assert verify_run(trial) == []
            assert inventory(trial / "project") == record["artifacts"]
            assert record["bundle_manifest_sha256"] == identity["bundle_manifest_sha256"]
            assert sha(series / "runner-versions" / (record["runner_sha256"] + ".py")) == record["runner_sha256"]
            assert record["runner_sha256"] == protocol["shared_runner_sha256"]
            calls = []
            with tempfile.TemporaryDirectory(prefix="pixl-inspection-replay-") as folder:
                temp = Path(folder)
                package, project = temp / "package", temp / "project"
                shutil.copytree(series / "package", package)
                shutil.copytree(trial / "project", project)
                env = dict(os.environ)
                env.pop("PYTHONPATH", None)
                env.pop("PIXL_PLUGIN_ROOT", None)
                for state in sorted(project.rglob("state.px")):
                    for operation in ("validate", "workflow", "inspection", "jobs"):
                        command = [sys.executable, "-I", str(package / "scripts/pixl.py"),
                                   operation, str(state), "--root", str(project)]
                        result = subprocess.run(command, cwd=project, env=env, capture_output=True,
                                                text=True, encoding="utf-8", timeout=45, check=False)
                        calls.append({"operation": operation, "state": state.relative_to(project).as_posix(),
                                      "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
                        assert result.returncode == 0, result.stderr
                assert inventory(project) == record["artifacts"]
            results.append({"series": series_name, "attempt": trial.name,
                            "record_sha256": sha(trial / "record.json"),
                            "package_manifest_sha256": identity["bundle_manifest_sha256"],
                            "calls": calls, "evidence_errors": []})
    result = {"purpose": "Integrity and isolated state replay only; no behavioral grading.",
              "analysis_source_sha256": sha(Path(__file__)), "runs": results,
              "error_count": 0, "replay_operations": sum(len(row["calls"]) for row in results)}
    with (BASE / "native-integrity.json").open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"runs": len(results), "operations": result["replay_operations"], "errors": 0}))


if __name__ == "__main__":
    run()
