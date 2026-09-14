"""Exercise recorder failure paths with local fake processes, never model hosts."""

from __future__ import annotations

import json
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from evaluations import host_trials as recorder  # noqa: E402


def main() -> None:
    root = Path(tempfile.mkdtemp(prefix="check-", dir=Path(__file__).parent / "recorder-probes"))
    evidence = root / "evidence"
    baseline = evidence / "package"
    baseline.mkdir(parents=True)
    (baseline / "sample.txt").write_text("original sample\n", encoding="utf-8")
    (baseline / "remove.txt").write_text("original removable fixture\n", encoding="utf-8")
    (evidence / "discovery").mkdir()
    (evidence / "discovery" / "codex-session-overrides.json").write_text("[]", encoding="utf-8")
    identity = {
        "source_revision": "controlled-recorder-fixture-not-a-production-package",
        "profile_hash": "0" * 64, "skill_hashes": {}, "runtime_hashes": {},
        "bundle_manifest_sha256": "0" * 64, "package_files": recorder.inventory(baseline),
    }
    fake = root / "fake_host.py"
    fake.write_text(
        "import sys\nfrom pathlib import Path\n"
        "if '--version' in sys.argv:\n print('fake-host recorder-fixture 1.0')\n"
        "else:\n sys.stdin.read()\n"
        " if sys.argv[1] == 'null':\n  print('null')\n"
        " else:\n"
        "  package=Path.cwd()/'.agents'/'skills'/'pixl-kit'\n"
        "  (package/'sample.txt').write_text('changed sample\\n',encoding='utf-8')\n"
        "  (package/'added.txt').write_text('new fixture file\\n',encoding='utf-8')\n"
        "  (package/'remove.txt').unlink()\n"
        "  print('{\"type\":\"turn.completed\"}')\n",
        encoding="utf-8",
    )
    actual_mkdtemp = tempfile.mkdtemp

    def project_temp(*args: object, **kwargs: object) -> str:
        kwargs["dir"] = str(root)
        return actual_mkdtemp(*args, **kwargs)

    observations = []
    for mode in ("null", "mutation"):
        with (
            patch.object(recorder, "EVIDENCE", evidence),
            patch.object(recorder, "freeze", return_value=identity),
            patch.object(recorder, "codex_command", return_value=[sys.executable, str(fake), mode]),
            patch.object(recorder.tempfile, "mkdtemp", side_effect=project_temp),
        ):
            target = recorder.run("codex", "maintainer-role", mode, None, 10)
        record = json.loads((target / "record.json").read_text(encoding="utf-8"))
        item = {
            "mode": mode, "attempt": str(target), "record_sha256": recorder.sha(target / "record.json"),
            "execution_status": record["execution_status"],
            "observed_model": record["observed_model"], "integrity_errors": recorder.verify_run(target),
            "package_mutated": record["package_mutated"],
            "baseline_unchanged": recorder.inventory(baseline) == identity["package_files"],
        }
        assert item["integrity_errors"] == [] and item["baseline_unchanged"]
        if mode == "null":
            assert record["execution_status"] == "incomplete_no_completion_event"
            assert record["observed_model"] is None and not record["package_mutated"]
            item["null_transcript_preserved"] = (target / "stdout.jsonl").read_text(encoding="utf-8") == "null\n"
            assert item["null_transcript_preserved"]
        else:
            retained = target / "mutated-package"
            assert record["package_mutated"]
            assert recorder.inventory(retained) == record["mutated_package_files"]
            assert (retained / "sample.txt").read_text(encoding="utf-8") == "changed sample\n"
            assert (retained / "added.txt").read_text(encoding="utf-8") == "new fixture file\n"
            assert not (retained / "remove.txt").exists()
            item["mutated_package_files"] = record["mutated_package_files"]
            item["changed_new_and_deleted_files_retained"] = True
            item["all_mutated_files_bound_in_evidence_hashes"] = all(
                record["evidence_hashes"].get("mutated-package/" + name) == value
                for name, value in record["mutated_package_files"].items()
            )
            assert item["all_mutated_files_bound_in_evidence_hashes"]
        observations.append(item)
    result = {
        "observed_at": datetime.now(UTC).isoformat(),
        "method": "Actual run() invokes a controlled local Python executable; only fixture paths, frozen identity and command discovery are patched.",
        "model_inference_executed": False, "production_package_used": False,
        "runner_sha256": recorder.sha(Path(recorder.__file__)),
        "probe_sha256": recorder.sha(Path(__file__)),
        "fake_host_sha256": recorder.sha(fake),
        "checks": observations, "passed": True,
    }
    recorder.write_json(root / "result.json", result)
    print(json.dumps({"result": str(root / "result.json"), **result}, indent=2))


if __name__ == "__main__":
    (Path(__file__).parent / "recorder-probes").mkdir(exist_ok=True)
    main()
