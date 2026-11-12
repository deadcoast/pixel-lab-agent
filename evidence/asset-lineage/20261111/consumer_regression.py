"""Run the final NF-08 kit through the existing isolated TM-07 operation."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from evaluations import asset_lineage_case, readiness_case
from evaluations.host_trials import inventory, sha, write_json


def run():
    target = Path(__file__).resolve().parent / "consumer-regression"
    if target.exists():
        raise ValueError("Preserve previous regression evidence; choose a new attempt")
    root = asset_lineage_case.prepare(target / "setup", "codex", readiness_case.DEFAULT_PYTHON)
    baseline = inventory(root, ("__pycache__",))
    kit = root / asset_lineage_case.KIT
    output = "work/asset-lineage/consumer-execution-regression"
    argv = [str(readiness_case.DEFAULT_PYTHON), "-I", str(kit / "scripts/pixl.py"),
            "consumer-execute", str(root / asset_lineage_case.STATE), "artistic2.delivery.candidate",
            str(root / "work/consumer-execution-inputs/config.json"), "--out", output, "--root", str(root)]
    result = subprocess.run(argv, cwd=root, capture_output=True, timeout=180, check=False)
    (target / "stdout.json").write_bytes(result.stdout)
    (target / "stderr.txt").write_bytes(result.stderr)
    report_path = root / output / "result.json"
    report = json.loads(report_path.read_bytes()) if report_path.exists() else {}
    imported_path = root / report["import_result"] if report.get("import_result") else None
    imported = json.loads(imported_path.read_bytes()) if imported_path else {}
    context_path = root / output / "review-context.json"
    context = json.loads(context_path.read_bytes()) if context_path.exists() else {}
    changed = [name for name, digest in baseline.items()
               if not (root / name).is_file() or sha(root / name) != digest]
    checks = {
        "public_operation_completed": result.returncode == 0 and report.get("status") == "complete",
        "actual_enriched_review_members_consumed": len(context.get("members", [])) == 4 and all(
            member.get("lineage", {}).get("candidate") == member["candidate"] for member in context.get("members", [])),
        "actual_renderer_executed": report.get("renderer_executed") is True,
        "exact_files_and_import_verified": report.get("files_verified") is True and imported.get("files_verified") is True,
        "owned_processes_cleaned": report.get("cleanup", {}).get("complete") is True,
        "all_initial_inputs_unchanged": not changed,
        "no_state_write_or_acceptance": report.get("state_written") is False and report.get("automatic_acceptance") is False,
        "same_final_verified_kit": sha(kit / "bundle-manifest.json") == sha(ROOT / "plugins/pixl/bundle-manifest.json"),
    }
    for source, name in ((report_path, "result.json"), (context_path, "review-context.json"),
                         (root / output / "check.json", "check.json"), (kit / "bundle-manifest.json", "bundle-manifest.json")):
        if source.exists():
            shutil.copyfile(source, target / name)
    if imported_path:
        shutil.copyfile(imported_path, target / "import-result.json")
        shutil.copyfile(root / imported["bundle"]["path"], target / "observations.zip")
        checks["exact_observation_bundle_retained"] = sha(target / "observations.zip") == imported["bundle"]["sha256"]
    receipt = {"status": "pass" if all(checks.values()) else "fail", "checks": checks,
               "argv": argv, "cwd": str(root), "returncode": result.returncode, "changed_inputs": changed,
               "bundle_manifest_sha256": sha(kit / "bundle-manifest.json"), "runner_sha256": sha(Path(__file__)),
               "scope": "Actual isolated existing consumer execution with enriched NF-08 review context. Mechanical regression only; no native model trial, new provider work, artistic judgment or acceptance."}
    write_json(target / "receipt.json", receipt)
    print(json.dumps({"status": receipt["status"], "passed": sum(checks.values()), "total": len(checks)}))
    return not all(checks.values())


if __name__ == "__main__":
    raise SystemExit(run())
