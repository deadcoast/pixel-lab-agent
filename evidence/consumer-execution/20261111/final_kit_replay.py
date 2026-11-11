"""Replay the final kit in already-qualified consumers without new model claims."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).resolve().parent
PYTHON = ROOT / "build/readiness-setup-01/runtime/Scripts/python.exe"
KIT = ROOT / "build/tm07-final-kit"


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def run():
    shutil.copytree(ROOT / "plugins/pixl", KIT, ignore=shutil.ignore_patterns("__pycache__"))
    manifest = read(KIT / "bundle-manifest.json")
    final_files = {r["path"]:r["sha256"] for r in manifest["files"]}
    outputs = []
    for name in ("codex-01", "claude-01"):
        attempt = EVIDENCE / name
        identity, launch = read(attempt / "identity.json"), read(attempt / "launch.json")
        root = Path(launch["cwd"])
        target = EVIDENCE / (name + "-final-kit")
        target.mkdir(exist_ok=False)
        state = root / ".pixl/assets/queue.ready/state.px"
        before = sha(state)
        output = "work/consumer-execution/final-kit-replay"
        argv = [str(PYTHON), "-B", str(KIT / "scripts/pixl.py"), "consumer-execute", str(state),
                "artistic2.delivery.candidate", str(root / "work/consumer-execution-inputs/config.json"),
                "--out", output, "--root", str(root)]
        unavailable_argv = list(argv)
        unavailable_argv[unavailable_argv.index("--out") + 1] = "work/consumer-execution/final-kit-unavailable"
        unavailable_argv += ["--node", str(root / "tm07-definitely-missing-node.exe")]
        unavailable_run = subprocess.run(unavailable_argv, cwd=root, capture_output=True, timeout=30)
        (target / "unavailable-stdout.json").write_bytes(unavailable_run.stdout)
        (target / "unavailable-stderr.txt").write_bytes(unavailable_run.stderr)
        failed_path = root / "work/consumer-execution/final-kit-unavailable/result.json"
        unavailable = read(failed_path)
        failed_hash = sha(failed_path)
        shutil.copyfile(failed_path, target / "unavailable-result.json")
        invoked = subprocess.run(argv, cwd=root, capture_output=True, timeout=120)
        (target / "stdout.json").write_bytes(invoked.stdout)
        (target / "stderr.txt").write_bytes(invoked.stderr)
        result = read(root / output / "result.json")
        imported = read(root / result["import_result"]) if result.get("import_result") else {}
        for source, dest in ((root / output / "result.json", "result.json"),
                             (root / output / "check.json", "check.json"),
                             (KIT / "bundle-manifest.json", "bundle-manifest.json")):
            if source.exists():
                shutil.copyfile(source, target / dest)
        if imported:
            shutil.copyfile(root / imported["bundle"]["path"], target / "observations.zip")
            save(target / "import-result.json", imported)
        relevant = [p for p in final_files if p.startswith(("runtime/", "agents/", "skills/", "resources/examples/consumer-execution/"))
                    or p == "resources/spec/consumer-execution.md"]
        changed = [p for p in final_files if final_files[p] != identity["package_files"].get(p)]
        checks = {
            "public_command_completed": invoked.returncode == 0 and result["status"] == "complete",
            "unavailable_capability_retained": unavailable_run.returncode == 1 and unavailable["status"] == "unavailable" and unavailable["error"]["code"] == "consumer_capability",
            "unavailable_attempt_executed_no_renderer": unavailable["renderer_executed"] is False and unavailable["automatic_acceptance"] is False,
            "fresh_retry_preserves_unavailable_receipt": sha(failed_path) == failed_hash and failed_path != root / output / "result.json",
            "frozen_native_operation_sources_identical": all(final_files[p] == identity["package_files"].get(p) for p in relevant),
            "fresh_copied_final_kit_exact": all(sha(KIT / p) == digest for p, digest in final_files.items()),
            "same_unchanged_production_state": sha(state) == before == identity["baseline_state"]["sha256"],
            "all_original_inputs_unchanged": all((root / p).is_file() and sha(root / p) == digest for p, digest in identity["inputs"].items()),
            "exact_files_verified": result["files_verified"] and imported.get("files_verified") is True,
            "owned_cleanup_confirmed": result["cleanup"]["complete"] is True,
            "real_renderer_execution": result["renderer_executed"] is True and imported.get("renderer_executed") is False,
            "no_acceptance_created": result["automatic_acceptance"] is False and result["state_written"] is False,
            "retained_bundle_exact": bool(imported) and sha(target / "observations.zip") == imported["bundle"]["sha256"],
        }
        receipt = {"status":"pass" if all(checks.values()) else "fail", "checks":checks,
                   "argv":argv,"unavailable_argv":unavailable_argv,"cwd":str(root),"returncode":invoked.returncode,
                   "bundle_manifest_sha256":sha(KIT / "bundle-manifest.json"),
                   "changed_since_native_package":changed,"scope":"Final copied-kit public execution compatibility; not another native model trial or new artistic acceptance."}
        save(target / "receipt.json",receipt)
        outputs.append({"attempt":name,"status":receipt["status"],"passed":sum(checks.values()),"total":len(checks)})
    print(json.dumps(outputs))
    return not all(r["status"] == "pass" for r in outputs)


if __name__ == "__main__":
    raise SystemExit(run())
