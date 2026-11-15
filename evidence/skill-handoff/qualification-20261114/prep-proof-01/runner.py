"""Actual default preparation only; no model or provider execution."""

import difflib
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASE = OUT.parent
sys.path.insert(0, str(ROOT))

from evaluations import skill_handoff_trials as trials
from evaluations.host_trials import inventory, sha, write_json


if __name__ == "__main__":
    if (OUT / "RESULT.json").exists() or (OUT / "attempt").exists():
        raise ValueError("Use a fresh preparation proof; retain prior receipts")
    names = ("reference.png", "reference-b.png")
    tracked = ROOT / "evidence/host-evaluation/fixture-inputs"
    predecessor = ROOT / "evidence/skill-handoff/revised-routing/fixture-inputs"
    expected = {name: sha(tracked / name) for name in names}
    old = {name: sha(predecessor / name) for name in names}
    command = ["git", "ls-files", "--", *(str((tracked / name).relative_to(ROOT)).replace("\\", "/") for name in names)]
    tracked_output = subprocess.check_output(command, cwd=ROOT, text=True)
    (OUT / "tracked-fixtures.txt").write_text(tracked_output, encoding="utf-8")
    before = inventory(ROOT / "plugins/pixl", ("__pycache__",))
    attempt = OUT / "attempt"
    consumer = trials.prepare(attempt, "fresh")
    identity = json.loads((attempt / "identity.json").read_bytes())
    with zipfile.ZipFile(attempt / "input-project.zip") as archive:
        archived = {name: hashlib.sha256(archive.read(name)).hexdigest() for name in archive.namelist()}
    prior_runner = BASE / "fresh-05/runner.py.txt"
    old_source = prior_runner.read_text(encoding="utf-8")
    new_source = (ROOT / "evaluations/skill_handoff_trials.py").read_text(encoding="utf-8")
    (OUT / "harness-change.diff").write_text("".join(difflib.unified_diff(old_source.splitlines(True), new_source.splitlines(True),
        fromfile="native-frozen-harness", tofile="portable-default-fixtures")), encoding="utf-8")
    expected_source = old_source.replace('FIXTURES = ROOT / "evidence/skill-handoff/revised-routing/fixture-inputs"',
                                        'FIXTURES = ROOT / "evidence/host-evaluation/fixture-inputs"')
    checks = {
        "both_default_fixtures_tracked": len(tracked_output.splitlines()) == 2,
        "default_path_uses_tracked_tree": trials.FIXTURES == tracked,
        "tracked_and_historical_images_byte_identical": expected == old,
        "actual_prepared_input_hashes_identical": identity["inputs"] == expected,
        "complete_input_archive_hashes_identical": archived == expected,
        "current_source_change_is_only_fixture_locator": new_source == expected_source,
        "package_unchanged": inventory(ROOT / "plugins/pixl", ("__pycache__",)) == before,
        "tracked_fixture_sources_unchanged": {name: sha(tracked / name) for name in names} == expected,
        "no_model_execution_receipts": not any((attempt / name).exists() for name in ("stdout.jsonl", "stderr.txt", "continuation.json", "record.json", "project.zip")),
    }
    result = {"status": "pass" if all(checks.values()) else "fail", "checks": checks,
        "passed": sum(checks.values()), "total": len(checks), "command": [sys.executable, "-B", str(Path(__file__).resolve())],
        "version_control_command": command, "prepared_attempt": str(attempt), "unused_consumer": str(consumer),
        "fixture_hashes": expected, "source_sha256": sha(ROOT / "evaluations/skill_handoff_trials.py"),
        "previous_native_source": {"path": str(prior_runner), "sha256": sha(prior_runner)},
        "scope": "Actual default fresh preparation with current copied kit and selected interpreter; host --version and runtime inventory probes only. No native model, provider, build or runtime mutation. Prior native outcomes remain tied to their frozen harness and identical image bytes."}
    write_json(OUT / "RESULT.json", result)
    print(json.dumps(result, indent=2))
