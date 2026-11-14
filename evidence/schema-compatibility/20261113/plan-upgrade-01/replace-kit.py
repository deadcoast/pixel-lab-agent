"""Retain source authority, then replace the copied consumer's kit in place.

Use after replay.py old. This is the actual replacement proof; replay.py new is
the optional alongside-reader route and is not used by this qualification.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from replay import COMPARISON, EVIDENCE, PLAN, PROJECT, REPO, SOURCE, STATE, WORK, digest, inventory, save


def execute(name, argv):
    run = subprocess.run(argv, cwd=PROJECT, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), capture_output=True, text=True)
    for suffix, value in (("stdout.json", run.stdout), ("stderr.txt", run.stderr)):
        path = EVIDENCE / f"{name}-{suffix}"
        if path.exists():
            raise RuntimeError("Preserve existing run outputs")
        path.write_text(value, encoding="utf-8")
    return run, json.loads(run.stdout) if run.returncode == 0 else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("retain", "replace"))
    parser.add_argument("--kit", type=Path)
    args = parser.parse_args()
    kit = PROJECT / ".agents/skills/pixl-kit"
    before = inventory(PROJECT)
    original = json.loads((EVIDENCE / "original-files.json").read_text())
    old = json.loads((EVIDENCE / "old-stdout.json").read_text())
    if args.phase == "retain":
        argv = [sys.executable, str(kit / "scripts/pixl.py"), "retain-library",
                str(PROJECT / Path(STATE).parent), ".agents/skills/pixl-kit",
                "--expect", old["state"]["sha256"], "--root", str(PROJECT)]
        run, report = execute("retention", argv)
        after = inventory(PROJECT)
        receipt = {
            "version": 1, "argv": argv, "exit_code": run.returncode, "report": report,
            "all_existing_files_unchanged": all(after.get(p) == h for p, h in before.items()),
            "added_files": sorted(set(after) - set(before)),
            "original_consumer_unchanged": inventory(SOURCE) == original,
            "state_file_sha256": digest(PROJECT / STATE),
        }
        save("retention-result.json", receipt)
        save("retained-files.json", after)
    else:
        if args.kit is None:
            parser.error("replace requires --kit for the final verified package")
        retention = json.loads((EVIDENCE / "retention-result.json").read_text())
        if retention["exit_code"] or not retention["all_existing_files_unchanged"]:
            raise RuntimeError("Source retention must complete without changed existing files")
        archived = WORK / "original-kit"
        # Verify both resolved recursive move targets inside the named workspace.
        if kit.resolve() != (WORK / "project/.agents/skills/pixl-kit").resolve() or not kit.resolve().is_relative_to(WORK.resolve()):
            raise RuntimeError("Unexpected kit move source")
        if archived.exists() or not archived.resolve().is_relative_to(WORK.resolve()):
            raise RuntimeError("Preserve existing old kit or reject outside target")
        old_kit = inventory(kit)
        shutil.move(str(kit.resolve()), str(archived.resolve()))
        shutil.copytree(args.kit.resolve(), kit)
        new_kit = inventory(kit)
        installed = inventory(PROJECT)
        argv = [sys.executable, str(kit / "scripts/pixl.py"), "request-review", STATE,
                "--plan", PLAN, "--comparison", COMPARISON, "--root", str(PROJECT)]
        run, report = execute("replacement", argv)
        after = inventory(PROJECT)
        prefix = ".agents/skills/pixl-kit/"
        receipt = {
            "version": 1, "argv": argv, "exit_code": run.returncode,
            "scope": "Actual kit replacement at the same copied-consumer path after public exact-source retention; no plan/state/art/acceptance edits and no provider or native model execution.",
            "old_kit_preserved": inventory(archived) == old_kit,
            "original_consumer_unchanged": inventory(SOURCE) == original,
            "all_nonkit_files_unchanged_across_replacement": {p:h for p,h in before.items() if not p.startswith(prefix)} == {p:h for p,h in after.items() if not p.startswith(prefix)},
            "review_read_only": installed == after,
            "new_kit_unchanged": inventory(kit) == new_kit,
            "old_manifest_sha256": digest(archived / "bundle-manifest.json"),
            "new_manifest_sha256": digest(kit / "bundle-manifest.json"),
            "new_runtime_sha256": {p: digest(kit / "runtime/pixl" / p) for p in ("adapter_versions.py", "production_plan.py", "production_review.py")},
            "state_file_sha256": digest(PROJECT / STATE),
            "same_saved_plan_identity": report is not None and old["plan"] == report["plan"],
            "same_review_scope": report is not None and old["review_scope_sha256"] == report["review_scope_sha256"],
            "same_criteria": report is not None and old["criteria"] == report["criteria"],
            "same_coverage": report is not None and old["comparison_coverage"] == report["comparison_coverage"],
            "same_diagnostics": report is not None and old["diagnostics"] == report["diagnostics"],
            "same_report": report == old,
            "comparison_coverage": report.get("comparison_coverage") if report else None,
            "consistent": report.get("consistent") if report else None,
        }
        save("replacement-result.json", receipt)
        save("replaced-files.json", after)
    print(json.dumps(receipt, indent=2))
    if run.returncode:
        raise SystemExit(run.returncode)


if __name__ == "__main__":
    main()
