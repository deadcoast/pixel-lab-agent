"""Retain old imported sources on isolated copies, preserving every original byte."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
HISTORICAL = REPO / "evidence/skill-handoff/archives/revised-routing.zip"
CURRENT = HERE.parent / "frozen-kit.zip"
PREFIX = "revised-routing/runs/claude-intake-01/project/"
KIT = ".agents/skills/pixl-kit"
STATE = "state.px/state.px"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def inventory(folder):
    return {p.relative_to(folder).as_posix(): sha(p.read_bytes())
            for p in sorted(folder.rglob("*")) if p.is_file()}


def extract(z, prefix, destination):
    for item in z.infolist():
        if not item.filename.startswith(prefix) or item.is_dir():
            continue
        relative = Path(item.filename.removeprefix(prefix))
        target = (destination / relative).resolve()
        if not target.is_relative_to(destination.resolve()):
            raise ValueError(f"Archive path escape: {item.filename}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(z.read(item))


def main():
    work = HERE / "work"
    if work.exists() or (HERE / "seed").exists():
        raise RuntimeError("Refusing to overwrite a retained preflight; use a fresh folder.")
    work.mkdir()
    original = work / "original-project"
    old = work / "old-kit-project"
    updated = work / "updated-kit-project"
    runtime = work / "current-kit"
    seed = HERE / "seed"
    old_archive_sha = sha(HISTORICAL.read_bytes())
    if old_archive_sha != "661dedfaf997431f63128763e62fe3ce7bc9fedccea6cf513a8b67d5f077640b":
        raise RuntimeError("Historical archive identity changed")
    with zipfile.ZipFile(HISTORICAL) as z:
        extract(z, PREFIX, original)
        shutil.copytree(original, old)
        shutil.copytree(original, updated)
        extract(z, "revised-routing/package/", old / KIT)
        extract(z, "revised-routing/package/", updated / "recovery/original-kit")
    with zipfile.ZipFile(CURRENT) as z:
        extract(z, "", runtime)
        extract(z, "", updated / KIT)
    before = inventory(original)
    save(HERE / "original-project-manifest.json", before)
    with zipfile.ZipFile(HERE / "original-project.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in before:
            z.write(original / name, name)
    records = []
    cli = [sys.executable, str(runtime / "scripts/pixl.py")]
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"}

    def command(name, args, expected):
        result = subprocess.run(cli + args, cwd=REPO, env=environment,
                                capture_output=True, timeout=60)
        stdout = HERE / "commands" / f"{name}.stdout.txt"
        stderr = HERE / "commands" / f"{name}.stderr.txt"
        stdout.parent.mkdir(exist_ok=True)
        stdout.write_bytes(result.stdout)
        stderr.write_bytes(result.stderr)
        row = {"name": name, "command": cli + args, "cwd": str(REPO),
               "returncode": result.returncode, "expected_returncode": expected,
               "stdout": stdout.relative_to(HERE).as_posix(),
               "stderr": stderr.relative_to(HERE).as_posix(),
               "stdout_sha256": sha(result.stdout), "stderr_sha256": sha(result.stderr)}
        records.append(row)
        save(HERE / "commands.json", records)
        if result.returncode != expected:
            raise RuntimeError(f"{name}: unexpected exit {result.returncode}; evidence retained")
        return json.loads(result.stdout) if result.returncode == 0 else None

    first = command("01-original-kit-validation", ["validate", str(old / STATE), "--root", str(old)], 0)
    canonical = first["hash"]
    command("02-updated-kit-before-retention", ["validate", str(updated / STATE), "--root", str(updated)], 1)
    retained = command("03-recover-from-original-kit", [
        "retain-library", str(updated / "state.px"), KIT,
        "--from-library", "recovery/original-kit", "--expect", canonical,
        "--root", str(updated)], 0)
    after = command("04-updated-kit-after-retention", ["validate", str(updated / STATE), "--root", str(updated)], 0)
    command("05-updated-kit-workflow", ["workflow", str(updated / STATE), "--root", str(updated)], 0)
    shutil.copytree(original, seed)
    shutil.copytree(updated / ".pixl/library-sources", seed / ".pixl/library-sources")
    portable = command("06-portable-seed-validation", ["validate", str(seed / STATE), "--root", str(seed)], 0)
    command("07-portable-seed-workflow", ["workflow", str(seed / STATE), "--root", str(seed)], 0)
    command("08-portable-authoring-context", ["context", str(seed / STATE), "project", "--view", "authoring", "--root", str(seed)], 0)
    files = inventory(seed)
    checks = {"original_project_36_files": len(before) == 36,
              "all_original_files_preserved": all(files.get(name) == digest for name, digest in before.items()),
              "original_working_snapshot_unchanged": inventory(original) == before,
              "original_archive_unchanged": sha(HISTORICAL.read_bytes()) == old_archive_sha,
              "state_unchanged": files[STATE] == "dc5029e484e22ee4dd9965287e2d1238864671c9a110825046e92d9f8d957000",
              "same_canonical_hash": canonical == after["hash"] == portable["hash"],
              "retention_did_not_change_state": retained["state_changed"] is False,
              "no_installed_or_donor_kit_in_seed": not (seed / ".agents").exists() and not (seed / "recovery").exists(),
              "only_explicit_source_retention_added": all(name in before or name.startswith(".pixl/library-sources/") for name in files)}
    save(HERE / "seed-manifest.json", files)
    with zipfile.ZipFile(HERE / "seed.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for name in files:
            z.write(seed / name, name)
    result = {"status": "pass" if all(checks.values()) else "fail", "checks": checks,
              "source_archive": str(HISTORICAL.relative_to(REPO)), "source_archive_sha256": old_archive_sha,
              "source_project_prefix": PREFIX, "original_project_archive_sha256": sha((HERE / "original-project.zip").read_bytes()),
              "current_kit_archive_sha256": sha(CURRENT.read_bytes()),
              "old_bundle_manifest_sha256": sha((old / KIT / "bundle-manifest.json").read_bytes()),
              "current_bundle_manifest_sha256": sha((runtime / "bundle-manifest.json").read_bytes()),
              "state_path": STATE, "canonical_state_hash": canonical,
              "original_file_count": len(before), "seed_file_count": len(files),
              "seed_manifest_sha256": sha((HERE / "seed-manifest.json").read_bytes()),
              "seed_archive_sha256": sha((HERE / "seed.zip").read_bytes()),
              "retained_source_ids": retained["sources"], "new_snapshots": retained["new_snapshots"],
              "limits": ["Artifact cold restart; original Claude session was not persisted.",
                         "Original artistic claims and reports are preserved, including unsupported thresholds.",
                         "Source compatibility does not requalify historical verdicts, current behavior, art or human acceptance.",
                         "No provider or model calls and no full verifier were run."]}
    save(HERE / "RESULT.json", result)
    if result["status"] != "pass":
        raise RuntimeError("Seed preservation checks failed")
    print(json.dumps({"status": result["status"], "checks": len(checks), "seed_files": len(files),
                      "new_snapshots": retained["new_snapshots"], "seed": str(seed)}, indent=2))


if __name__ == "__main__":
    main()
