"""Verify the unmodified project: it has no imported library sources to retain."""

import json
import os
import shutil
import subprocess
import sys
import zipfile

from prepare_seed import HERE, HISTORICAL, CURRENT, KIT, PREFIX, REPO, STATE, inventory, save, sha


def main():
    work, seed = HERE / "work", HERE / "seed"
    original, runtime = work / "original-project", work / "current-kit"
    if seed.exists():
        raise RuntimeError("Refusing to overwrite existing seed")
    shutil.copytree(original, seed)
    before = json.loads((HERE / "original-project-manifest.json").read_text())
    cli = [sys.executable, str(runtime / "scripts/pixl.py")]
    records = []

    def run(name, args):
        result = subprocess.run(cli + args, cwd=REPO, capture_output=True, timeout=60,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"})
        out, err = HERE / "commands" / (name + ".stdout.txt"), HERE / "commands" / (name + ".stderr.txt")
        out.write_bytes(result.stdout)
        err.write_bytes(result.stderr)
        records.append({"name": name, "command": cli + args, "cwd": str(REPO), "returncode": result.returncode,
                        "stdout": out.relative_to(HERE).as_posix(), "stderr": err.relative_to(HERE).as_posix(),
                        "stdout_sha256": sha(result.stdout), "stderr_sha256": sha(result.stderr)})
        save(HERE / "final-commands.json", records)
        if result.returncode:
            raise RuntimeError(f"{name}: exit {result.returncode}; evidence retained")
        return json.loads(result.stdout)

    portable = run("04-portable-seed-validation", ["validate", str(seed / STATE), "--root", str(seed)])
    run("05-portable-seed-workflow", ["workflow", str(seed / STATE), "--root", str(seed)])
    run("06-portable-authoring-context", ["context", str(seed / STATE), "project", "--view", "authoring", "--root", str(seed)])
    decoded = run("07-portable-decode", ["decode", str(seed / STATE)])
    sources = [row for row in decoded["records"] if row["kind"] == "S"]
    files = inventory(seed)
    checks = {"original_project_36_files": len(before) == 36,
        "exact_original_project_preserved": files == before,
        "original_working_snapshot_unchanged": inventory(original) == before,
        "original_archive_unchanged": sha(HISTORICAL.read_bytes()) == "661dedfaf997431f63128763e62fe3ce7bc9fedccea6cf513a8b67d5f077640b",
        "state_file_unchanged": files[STATE] == "dc5029e484e22ee4dd9965287e2d1238864671c9a110825046e92d9f8d957000",
        "same_canonical_hash": portable["hash"] == "dc5029e484e22ee4dd9965287e2d1238864671c9a110825046e92d9f8d957000",
        "no_installed_or_donor_kit_in_seed": not (seed / ".agents").exists() and not (seed / "recovery").exists(),
        "all_five_sources_are_project_owned": len(sources) == 5 and all(row["fields"]["ur"] in files for row in sources),
        "no_imported_kit_sources": all(not row["fields"]["ur"].startswith(KIT) for row in sources)}
    save(HERE / "seed-manifest.json", files)
    with zipfile.ZipFile(HERE / "seed.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in files:
            z.write(seed / name, name)
    result = {"status": "pass" if all(checks.values()) else "fail", "checks": checks,
        "source_archive": str(HISTORICAL.relative_to(REPO)), "source_archive_sha256": sha(HISTORICAL.read_bytes()),
        "source_project_prefix": PREFIX, "original_project_archive_sha256": sha((HERE / "original-project.zip").read_bytes()),
        "current_kit_archive_sha256": sha(CURRENT.read_bytes()),
        "old_bundle_manifest_sha256": sha((work / "old-kit-project" / KIT / "bundle-manifest.json").read_bytes()),
        "current_bundle_manifest_sha256": sha((runtime / "bundle-manifest.json").read_bytes()),
        "state_path": STATE, "canonical_state_hash": portable["hash"], "original_file_count": len(before), "seed_file_count": len(files),
        "seed_manifest_sha256": sha((HERE / "seed-manifest.json").read_bytes()), "seed_archive_sha256": sha((HERE / "seed.zip").read_bytes()),
        "sources": sources, "retention_needed": False, "retention_performed": False,
        "preserved_failures": ["attempt-01-assumption-failure.json", "continuation-commands.json", "commands/03-retain-from-original-kit.stdout.txt"],
        "limits": ["Artifact cold restart; original Claude session was not persisted.",
                   "All original artistic claims and reports survive, including unsupported thresholds.",
                   "Library retention correctly refused because no library S records are imported; every source is project-owned.",
                   "Preparation and compatibility checks are evaluator work, not native model behavior or new verdicts.",
                   "No provider/model calls or full verifier. Human acceptance remains separate."]}
    save(HERE / "RESULT.json", result)
    if not all(checks.values()):
        raise RuntimeError("Seed preservation checks failed")
    print(json.dumps({"status": "pass", "checks": len(checks), "seed_files": len(files), "seed": str(seed)}))


if __name__ == "__main__":
    main()
