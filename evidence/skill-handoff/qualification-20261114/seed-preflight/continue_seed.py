"""Continue after preserving the incorrect expected-failure assumption in attempt 01."""

import json
import os
import shutil
import subprocess
import sys
import zipfile

from prepare_seed import HERE, HISTORICAL, CURRENT, KIT, PREFIX, REPO, STATE, inventory, save, sha


def main():
    work = HERE / "work"
    original = work / "original-project"
    old = work / "old-kit-project"
    updated = work / "updated-kit-project"
    runtime = work / "current-kit"
    seed = HERE / "seed"
    if seed.exists():
        raise RuntimeError("Refusing to overwrite existing seed")
    before = json.loads((HERE / "original-project-manifest.json").read_text())
    previous = json.loads((HERE / "commands.json").read_text())
    assert len(previous) == 2 and [row["returncode"] for row in previous] == [0, 0]
    save(HERE / "attempt-01-assumption-failure.json", {
        "status": "failed_evaluator_expectation", "command": previous[1],
        "prepare_seed_sha256": sha((HERE / "prepare_seed.py").read_bytes()),
        "reason": "Expected changed-library validation refusal, but the exact original project validates with the current frozen kit; imported source bytes still match.",
        "retained": "Both original command records and outputs remain unchanged; no runtime or saved-state repair was necessary."})
    canonical = json.loads((HERE / previous[0]["stdout"]).read_text())["hash"]
    records = []
    cli = [sys.executable, str(runtime / "scripts/pixl.py")]
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"}

    def run(name, args):
        result = subprocess.run(cli + args, cwd=REPO, env=env, capture_output=True, timeout=60)
        out, err = HERE / "commands" / (name + ".stdout.txt"), HERE / "commands" / (name + ".stderr.txt")
        out.write_bytes(result.stdout)
        err.write_bytes(result.stderr)
        records.append({"name": name, "command": cli + args, "cwd": str(REPO), "returncode": result.returncode,
                        "stdout": out.relative_to(HERE).as_posix(), "stderr": err.relative_to(HERE).as_posix(),
                        "stdout_sha256": sha(result.stdout), "stderr_sha256": sha(result.stderr)})
        save(HERE / "continuation-commands.json", records)
        if result.returncode:
            raise RuntimeError(f"{name}: exit {result.returncode}; evidence retained")
        return json.loads(result.stdout)

    retained = run("03-retain-from-original-kit", ["retain-library", str(updated / "state.px"), KIT,
        "--from-library", "recovery/original-kit", "--expect", canonical, "--root", str(updated)])
    after = run("04-updated-kit-after-retention", ["validate", str(updated / STATE), "--root", str(updated)])
    run("05-updated-kit-workflow", ["workflow", str(updated / STATE), "--root", str(updated)])
    shutil.copytree(original, seed)
    shutil.copytree(updated / ".pixl/library-sources", seed / ".pixl/library-sources")
    portable = run("06-portable-seed-validation", ["validate", str(seed / STATE), "--root", str(seed)])
    run("07-portable-seed-workflow", ["workflow", str(seed / STATE), "--root", str(seed)])
    run("08-portable-authoring-context", ["context", str(seed / STATE), "project", "--view", "authoring", "--root", str(seed)])
    files = inventory(seed)
    checks = {"original_project_36_files": len(before) == 36,
        "all_original_files_preserved": all(files.get(name) == digest for name, digest in before.items()),
        "original_working_snapshot_unchanged": inventory(original) == before,
        "original_archive_unchanged": sha(HISTORICAL.read_bytes()) == "661dedfaf997431f63128763e62fe3ce7bc9fedccea6cf513a8b67d5f077640b",
        "state_unchanged": files[STATE] == "dc5029e484e22ee4dd9965287e2d1238864671c9a110825046e92d9f8d957000",
        "same_canonical_hash": canonical == after["hash"] == portable["hash"],
        "retention_did_not_change_state": retained["state_changed"] is False,
        "no_installed_or_donor_kit_in_seed": not (seed / ".agents").exists() and not (seed / "recovery").exists(),
        "only_explicit_source_retention_added": all(name in before or name.startswith(".pixl/library-sources/") for name in files)}
    save(HERE / "seed-manifest.json", files)
    with zipfile.ZipFile(HERE / "seed.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in files:
            z.write(seed / name, name)
    save(HERE / "RESULT.json", {
        "status": "pass" if all(checks.values()) else "fail", "checks": checks,
        "source_archive": str(HISTORICAL.relative_to(REPO)), "source_archive_sha256": sha(HISTORICAL.read_bytes()),
        "source_project_prefix": PREFIX, "original_project_archive_sha256": sha((HERE / "original-project.zip").read_bytes()),
        "current_kit_archive_sha256": sha(CURRENT.read_bytes()),
        "old_bundle_manifest_sha256": sha((old / KIT / "bundle-manifest.json").read_bytes()),
        "current_bundle_manifest_sha256": sha((runtime / "bundle-manifest.json").read_bytes()),
        "state_path": STATE, "canonical_state_hash": canonical, "original_file_count": len(before), "seed_file_count": len(files),
        "seed_manifest_sha256": sha((HERE / "seed-manifest.json").read_bytes()), "seed_archive_sha256": sha((HERE / "seed.zip").read_bytes()),
        "retained_source_ids": retained["sources"], "new_snapshots": retained["new_snapshots"],
        "limits": ["Artifact cold restart; original Claude session was not persisted.",
                   "Original artistic claims and reports are preserved, including unsupported thresholds.",
                   "Source compatibility does not requalify historical verdicts, current behavior, art or human acceptance.",
                   "No provider or model calls and no full verifier were run.",
                   "The expected source-drift failure did not occur; both old and current kits validate before retention."]})
    if not all(checks.values()):
        raise RuntimeError("Seed preservation checks failed")
    print(json.dumps({"status": "pass", "checks": len(checks), "seed_files": len(files),
                      "new_snapshots": retained["new_snapshots"], "seed": str(seed)}))


if __name__ == "__main__":
    main()
