"""Replay a genuinely retained connected plan through separate installed kits.

No state, art, comparison, source or acceptance mutation is requested. The
original consumer and its frozen kit remain intact. The current kit is installed
beside the copied consumer so historical library references keep exact bytes.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


REPO = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
SOURCE = REPO / "evidence/successor-acceptance/20261109/maintainer-01/project"
WORK = REPO / "build/sc06-plan-upgrade-01"
PROJECT = WORK / "project"
STATE = ".pixl/assets/queue.ready/state.px"
PLAN = "successor-adoption-02.plan"
COMPARISON = "work/successor-adoption/caller-comparison.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix(): digest(p)
            for p in sorted(root.rglob("*")) if p.is_file()}


def save(name, value):
    path = EVIDENCE / name
    if path.exists():
        raise RuntimeError(f"Preserve existing receipt: {path}")
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("old", "new"))
    parser.add_argument("--kit", type=Path)
    args = parser.parse_args()
    if args.phase == "old":
        if PROJECT.exists():
            raise RuntimeError("Preserve existing copied consumer; use its retained receipts")
        original = inventory(SOURCE)
        shutil.copytree(SOURCE, PROJECT)
        before = inventory(PROJECT)
        save("original-files.json", original)
        save("copied-files.json", before)
        if before != original:
            raise RuntimeError("Consumer copy changed file identities")
        kit = PROJECT / ".agents/skills/pixl-kit"
    else:
        if args.kit is None:
            parser.error("new phase requires --kit for the final verified kit")
        kit = WORK / "current-kit"
        shutil.copytree(args.kit.resolve(), kit)
        before = inventory(PROJECT)
    kit_before = inventory(kit)
    argv = [sys.executable, str(kit / "scripts/pixl.py"), "request-review", STATE,
            "--plan", PLAN, "--comparison", COMPARISON, "--root", str(PROJECT)]
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    started = time.perf_counter()
    run = subprocess.run(argv, cwd=PROJECT, env=environment, capture_output=True, text=True)
    stdout = EVIDENCE / f"{args.phase}-stdout.json"
    stderr = EVIDENCE / f"{args.phase}-stderr.txt"
    if stdout.exists() or stderr.exists():
        raise RuntimeError("Preserve previous run outputs")
    stdout.write_text(run.stdout, encoding="utf-8")
    stderr.write_text(run.stderr, encoding="utf-8")
    after = inventory(PROJECT)
    original_after = inventory(SOURCE)
    original_before = json.loads((EVIDENCE / "original-files.json").read_text())
    report = json.loads(run.stdout) if run.returncode == 0 else None
    receipt = {
        "version": 1, "phase": args.phase, "argv": argv, "exit_code": run.returncode,
        "seconds": round(time.perf_counter() - started, 3),
        "scope": "Read-only compatibility of a retained delivered consumer's authored plan, snapshot, metadata and unversioned caller comparison. No new provider execution, native model judgment, art quality or human acceptance claim.",
        "source_project": SOURCE.relative_to(REPO).as_posix(),
        "retained_source_head": "74646f6ee2d3138057d54a6f9a6aade765b0402d",
        "consumer_file_count": len(before),
        "original_consumer_unchanged": original_after == original_before,
        "copied_consumer_unchanged": before == after,
        "copied_consumer_matches_original": before == original_before,
        "kit_unchanged": kit_before == inventory(kit),
        "kit_manifest_sha256": digest(kit / "bundle-manifest.json"),
        "kit_runtime_sha256": {p: digest(kit / "runtime/pixl" / p) for p in ("production_plan.py", "production_review.py")},
        "stdout_sha256": digest(stdout), "stderr_sha256": digest(stderr),
        "authored_plan_sha256": digest(PROJECT / "work/successor-adoption/public-plan-02.json"),
        "caller_comparison_sha256": digest(PROJECT / COMPARISON),
        "state_file_sha256": digest(PROJECT / STATE),
        "report": {key: report.get(key) for key in ("version", "kind", "state", "plan", "review_scope_sha256", "comparison_coverage", "consistent", "diagnostics")} if report else None,
    }
    if args.phase == "new" and report:
        old = json.loads((EVIDENCE / "old-stdout.json").read_text())
        receipt["same_saved_plan_identity"] = old["plan"] == report["plan"]
        receipt["same_review_scope"] = old["review_scope_sha256"] == report["review_scope_sha256"]
        receipt["same_criterion_identities_and_text"] = old["criteria"] == report["criteria"]
        receipt["same_coverage"] = old["comparison_coverage"] == report["comparison_coverage"]
        receipt["same_report"] = old == report
    save(f"{args.phase}-result.json", receipt)
    print(json.dumps(receipt, indent=2))
    if run.returncode or not all((receipt["original_consumer_unchanged"], receipt["copied_consumer_unchanged"], receipt["kit_unchanged"])):
        raise SystemExit(run.returncode or 1)


if __name__ == "__main__":
    main()
