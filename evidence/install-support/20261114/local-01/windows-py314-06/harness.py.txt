"""Fresh, immutable installation/update matrix cells; no native host or provider calls.

Build a retained distribution once, then run explicit interpreter cells. Each cell
uses fresh environments and public CLI processes. Relocation moves only consumer
files and a copied kit; virtual environments stay at their original locations.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import platform
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if not __package__:
    sys.path.insert(0, str(ROOT))

from evaluations.consumer_setup_check import (
    FORBIDDEN,
    IGNORED,
    PACKAGE_CODE,
    SOURCE_DIRS,
    SOURCE_FILES,
    Commands,
    clean_environment,
    copy_exact,
    digest,
    inventory,
    now,
    reference,
    runtime_python,
    source_inventory,
    write_json,
)
from scripts.plar_probe import run_plar_probe

SCOPE = ("Local installation, saved production and cold artifact resume. PLAR probe "
         "uses synthetic schema/observations and a local dispatch claim only; no "
         "provider execution, generated art, native host behavior or acceptance.")
logger = logging.getLogger(__name__)


def fresh_paths(work, evidence):
    work, evidence = Path(work).resolve(), Path(evidence).resolve()
    for path, parent in ((work, ROOT / "build"), (evidence, ROOT / "evidence/install-support")):
        if not path.is_relative_to(parent) or path == parent:
            raise ValueError(f"Output must be a child of {parent}")
        if path.exists():
            raise FileExistsError(f"Preserve existing attempt: {path}")
    work.mkdir(parents=True)
    evidence.mkdir(parents=True)
    return work, evidence


def safe_move(source, destination, work):
    source, destination, work = Path(source).resolve(), Path(destination).resolve(), Path(work).resolve()
    if any(not p.is_relative_to(work) or p == work for p in (source, destination)):
        raise ValueError("Relocation must stay inside this attempt's workspace")
    if source.is_relative_to(destination) or destination.is_relative_to(source):
        raise ValueError("Relocation source and destination cannot overlap")
    if destination.exists():
        raise FileExistsError("Preserve existing relocation destination")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))


def exact_kit(kit):
    kit = Path(kit).resolve()
    manifest = json.loads((kit / "bundle-manifest.json").read_bytes())
    for row in manifest["files"] + manifest.get("generated_files", []):
        path = (kit / row["path"]).resolve()
        if not path.is_relative_to(kit) or not path.is_file() or digest(path) != row["sha256"]:
            raise ValueError(f"Kit manifest mismatch: {row['path']}")
    return reference(kit / "bundle-manifest.json")


def inspect_packages(commands, python, label, *, installed):
    value = commands.json(label, [python, "-I", "-B", "-c", PACKAGE_CODE])
    found = set(value["distributions"])
    # Python 3.11's standard venv includes setuptools as a bootstrap tool. It is
    # recorded, not falsely attributed to PIXL or treated as a requested dev extra.
    if found & (FORBIDDEN - {"setuptools"}):
        raise RuntimeError(f"Maintainer extras present in {label}")
    if installed and not {"pillow", "jsonschema", "referencing"} <= found:
        raise RuntimeError(f"Missing runtime dependencies in {label}")
    value["bootstrap_setuptools_present"] = "setuptools" in found
    return value


def build_distribution(work, evidence, python):
    python = Path(python).resolve()
    work, evidence = fresh_paths(work, evidence)
    commands = Commands(evidence, work)
    shutil.copyfile(__file__, evidence / "harness.py.txt")
    result = {"version": 1, "status": "running", "started_at": now(), "scope": "Fresh isolated source -> sdist/wheel; no bundle regeneration"}
    write_json(evidence / "START.json", result)
    try:
        inputs = source_inventory()
        source = work / "frozen source"
        copy_exact(ROOT, source, inputs)
        write_json(evidence / "source-inputs.json", inputs)
        with zipfile.ZipFile(evidence / "source-inputs.zip", "x", zipfile.ZIP_DEFLATED) as archive:
            for name in inputs:
                archive.write(source / name, name)
        uv = shutil.which("uv")
        if not uv:
            raise RuntimeError("uv is required for this isolated distribution build")
        commands.run("build", [uv, "build", "--python", python, "--out-dir", evidence / "artifacts", source])
        artifacts = list((evidence / "artifacts").glob("*.whl"))
        if len(artifacts) != 1:
            raise RuntimeError("Expected one retained wheel")
        wheel = artifacts[0]
        with zipfile.ZipFile(wheel) as archive:
            for path in (ROOT / "pixl").iterdir():
                if path.suffix in (".py", ".json"):
                    for prefix in ("pixl/", "pixl/resources/pixl/"):
                        if archive.read(prefix + path.name) != path.read_bytes():
                            raise RuntimeError(f"Wheel runtime differs: {prefix}{path.name}")
        if inventory(source, inputs) != inputs:
            raise RuntimeError("Build changed a frozen source input")
        result.update(status="pass", wheel=reference(wheel), artifacts=[reference(p) for p in (evidence / "artifacts").iterdir() if p.is_file()],
                      frozen_source=str(source), source_input_count=len(inputs), source_inputs_unchanged=True,
                      script=reference(__file__))
    except Exception as error:
        logger.exception("Distribution qualification failed; preserving the failed attempt")
        result.update(status="fail", error={"type": type(error).__name__, "detail": str(error)})
    result.update(finished_at=now(), commands=commands.rows)
    write_json(evidence / "RESULT.json", result)
    return result


def cli_for(commands, command, label):
    def cli(args):
        return commands.json(label, [*command, *args])
    return cli


def current_identity(cli, consumer):
    selected = cli(["plar", "read", "--root", str(consumer), "--asset", "queue.working"])
    production = selected["production"]
    state = consumer / selected["asset"]["production"]["store"] / "state.px"
    jobs = cli(["jobs", str(state), "--root", str(consumer)])
    pending = production["pending_jobs"]
    if not pending or not production["selection_current"]:
        raise RuntimeError("Expected a current prepared successor with retained pending work")
    return {"requirements_hash": selected["requirements_hash"], "state_sha256": digest(state),
            "pending_jobs": pending, "continuation": production["continuation"],
            "job_states": {row["id"]: row["state"] for row in jobs["jobs"]}}


def runtime_payload(folder):
    return {p.name: digest(p) for p in sorted(Path(folder).iterdir()) if p.is_file() and p.suffix in (".py", ".json")}


def useful_route(commands, command, consumer, resources, label, expected_runtime, installation=None):
    shutil.copytree(resources / "examples/plar-project", consumer, ignore=shutil.ignore_patterns("__pycache__"))
    cli = cli_for(commands, command, label)
    readiness_args = ["readiness", "--root", str(consumer)]
    if installation:
        readiness_args += ["--installation", str(installation)]
    readiness = cli(readiness_args)
    if readiness["local_operations"]["runtime_requirements"] != "satisfied":
        raise RuntimeError("Installed runtime is incomplete")
    kind = readiness["installation"]["kind"]
    expected = (Path(installation) / "runtime/pixl/readiness.py" if kind == "plugin" else
                Path(installation) / "pixl/readiness.py" if kind == "source" else resources.parent / "readiness.py")
    reporter = Path(readiness["reporter"]["module"]).resolve()
    if reporter != expected.resolve() or runtime_payload(reporter.parent) != expected_runtime:
        raise RuntimeError("Public CLI executed a different runtime than the intended installation")
    brief = cli(["source", "BRIEF.md", "--root", str(consumer), "--expect", digest(consumer / "BRIEF.md"), "--start", "1", "--end", "3"])
    library = cli(["sources"])
    if Path(library.get("root", "")).resolve() != resources.resolve() or library.get("files_verified") is not True:
        raise RuntimeError("Installed library root differs from the intended resources")
    document = library["documents"][0]
    # CLI source uses an absolute installed locator; scope=library belongs to
    # MCP source and the CLI context operation, not this CLI source parser.
    retrieved = cli(["source", str(resources / document["path"]), "--expect", document["sha256"], "--start", "1", "--end", "3"])
    if retrieved["sha256"] != document["sha256"] or brief["sha256"] != digest(consumer / "BRIEF.md"):
        raise RuntimeError("Exact source/library retrieval differs")
    probe = run_plar_probe(cli, consumer)
    identity = current_identity(cli, consumer)
    return {"readiness": readiness, "probe": probe, "identity": identity,
            "consumer_source_sha256": brief["sha256"], "library_source": document,
            "executed_runtime": {name: reference(reporter.parent / name)
                                 for name in ("readiness.py", "production_plan.py", "jobs.py")},
            "runtime_payload_matches_frozen_kit": True, "runtime_payload": runtime_payload(reporter.parent),
            "status": "pass"}


def retained_update(commands, python, kit, work, evidence):
    original = ROOT / "evidence/successor-acceptance/20261109/maintainer-01/project"
    consumer = work / "retained consumer"
    shutil.copytree(original, consumer, ignore=shutil.ignore_patterns("__pycache__"))
    before = inventory(consumer)
    installed = consumer / ".agents/skills/pixl-kit"
    old_manifest = exact_kit(installed)
    old_installation = str(installed)
    args = ["request-review", ".pixl/assets/queue.ready/state.px", "--plan", "successor-adoption-02.plan",
            "--comparison", "work/successor-adoption/caller-comparison.json", "--root", str(consumer)]
    old = commands.json("retained-old-kit-review", [python, "-I", "-B", installed / "scripts/pixl.py", *args])
    retired = work / "retired original kit"
    safe_move(installed, retired, work)
    shutil.copytree(kit, installed)
    new = commands.json("retained-new-kit-review", [python, "-I", "-B", installed / "scripts/pixl.py", *args])
    after = inventory(consumer)
    prefix = ".agents/skills/pixl-kit/"
    nonkit = {name: value for name, value in before.items() if not name.startswith(prefix)}
    if {name: value for name, value in after.items() if not name.startswith(prefix)} != nonkit:
        raise RuntimeError("Kit replacement changed a non-kit consumer file")
    original_kit = {name[len(prefix):]: value for name, value in before.items() if name.startswith(prefix)}
    if inventory(retired) != original_kit:
        raise RuntimeError("Original kit was not preserved exactly outside the consumer")
    retained_manifest = exact_kit(retired)
    if retained_manifest["sha256"] != old_manifest["sha256"]:
        raise RuntimeError("Retired kit manifest differs from the executed original")
    labels = new.pop("hash_domains", None)
    if new != old or not labels:
        raise RuntimeError("Saved plan review semantics changed across kit replacement")
    write_json(evidence / "retained-before.json", before)
    write_json(evidence / "retained-after.json", after)
    return {"status": "pass", "same_path_replacement": str(installed), "old_installation": old_installation,
            "old_manifest": retained_manifest,
            "new_manifest": exact_kit(installed), "nonkit_files_preserved": len(nonkit),
            "report_delta": "Only additive hash_domains metadata", "comparison_coverage": new["comparison_coverage"],
            "state": new["state"], "old_kit_preserved": True}


def run_cell(work, evidence, python, kit, wheel, source=None):
    python, kit, wheel = Path(python).resolve(), Path(kit).resolve(), Path(wheel).resolve()
    # Preflight supplied identities before creating an attempt; malformed input
    # cannot consume an output directory and leave an unrecorded half-attempt.
    identities = {"target_python": reference(python), "wheel": reference(wheel), "kit_manifest": exact_kit(kit)}
    work, evidence = fresh_paths(work, evidence)
    commands = Commands(evidence, work)
    shutil.copyfile(__file__, evidence / "harness.py.txt")
    result = {"version": 1, "status": "running", "started_at": now(), "scope": SCOPE,
              "platform": {"system": platform.system(), "release": platform.release(), "version": platform.version(), "machine": platform.machine()},
              **identities,
              "routes": {}, "script": reference(__file__)}
    write_json(evidence / "START.json", result)
    try:
        result["python_version"] = commands.run("python-version", [python, "--version"]).strip()
        kit_original = inventory(kit)
        expected_runtime = runtime_payload(kit / "runtime/pixl")
        result["expected_runtime_payload"] = expected_runtime
        copied = work / "initial copied kit"
        copy_exact(kit, copied, kit_original)
        env = work / "kit runtime"
        py = runtime_python(env)
        commands.run("kit-create-venv", [python, "-m", "venv", env])
        bare_packages = inspect_packages(commands, py, "bare-packages", installed=False)
        if bare_packages["pixl_origin"] or {"pillow", "jsonschema"} & set(bare_packages["distributions"]):
            raise RuntimeError("Bare environment inherited project dependencies")
        bare_root = work / "bare consumer"
        bare_root.mkdir()
        bare = commands.json("bare-readiness", [py, "-I", "-B", copied / "scripts/pixl.py", "readiness", "--root", bare_root], expected=1)
        if bare["dependencies"]["status"] != "incomplete" or inventory(bare_root):
            raise RuntimeError("Bare readiness did not preserve incomplete setup")
        commands.run("kit-install", [py, "-m", "pip", "install", "-r", copied / "requirements.txt"])
        package = inspect_packages(commands, py, "kit-packages", installed=True)
        if package["pixl_origin"]:
            raise RuntimeError("Copied-kit environment unexpectedly has installed PIXL")
        result["bare_bootstrap"] = {"status": "pass", "report": bare, "packages": bare_packages}
        write_json(evidence / "RUNTIME-READY.json", {"python": str(py), "packages": package})
        command = [py, "-I", "-B", copied / "scripts/pixl.py"]
        consumer = work / "kit consumer"
        route = useful_route(commands, command, consumer, copied / "resources", "kit-operation", expected_runtime, copied)
        consumer_before = inventory(consumer)
        moved_consumer, moved_kit = work / "relocated project with spaces", work / "relocated kit with spaces"
        safe_move(consumer, moved_consumer, work)
        safe_move(copied, moved_kit, work)
        cold = current_identity(cli_for(commands, [py, "-I", "-B", moved_kit / "scripts/pixl.py"], "cold-kit-read"), moved_consumer)
        if cold != route["identity"] or inventory(moved_consumer) != consumer_before or inventory(moved_kit) != kit_original:
            raise RuntimeError("Relocated cold read changed production identity or input bytes")
        route.update(packages=package, relocation="actual project and kit move; unchanged fixed venv", cold_identity=cold,
                     consumer_files_preserved=len(consumer_before), kit_files_unchanged=True)
        result["routes"]["copied_kit"] = route
        result["routes"]["retained_kit_update"] = retained_update(commands, py, moved_kit, work, evidence)

        wheel_env = work / "wheel runtime"
        wheel_py = runtime_python(wheel_env)
        commands.run("wheel-create-venv", [python, "-m", "venv", wheel_env])
        commands.run("wheel-install", [wheel_py, "-m", "pip", "install", wheel])
        package = inspect_packages(commands, wheel_py, "wheel-packages", installed=True)
        origin, site = Path(package["pixl_origin"] or "").resolve(), Path(package["site"]).resolve()
        if not origin.is_relative_to(site) or not site.is_relative_to(wheel_env):
            raise RuntimeError("Wheel imports outside its fresh environment")
        console = wheel_env / ("Scripts/pixl.exe" if os.name == "nt" else "bin/pixl")
        consumer = work / "wheel consumer"
        route = useful_route(commands, [console], consumer, origin.parent / "resources", "wheel-operation", expected_runtime)
        before = inventory(consumer)
        relocated = work / "relocated wheel consumer"
        safe_move(consumer, relocated, work)
        cold = current_identity(cli_for(commands, [console], "cold-wheel-read"), relocated)
        if cold != route["identity"] or inventory(relocated) != before:
            raise RuntimeError("Wheel cold read changed retained production")
        route.update(packages=package, console=reference(console), consumer_files_preserved=len(before),
                     relocation="consumer moved; environment and console remain fixed", cold_identity=cold)
        result["routes"]["wheel"] = route

        if source is not None:
            source = Path(source).resolve()
            frozen = work / "locked source"
            selected = list(SOURCE_FILES)
            for name in SOURCE_DIRS:
                selected.extend(p.relative_to(source).as_posix() for p in (source / name).rglob("*")
                                if p.is_file() and not IGNORED.intersection(p.relative_to(source / name).parts))
            rows = inventory(source, selected)
            write_json(evidence / "locked-source-inputs.json", rows)
            copy_exact(source, frozen, rows)
            source_env = frozen / ".venv"
            env = clean_environment()
            env["UV_PROJECT_ENVIRONMENT"] = str(source_env)
            commands.run("source-locked-sync", [shutil.which("uv"), "sync", "--locked", "--no-dev", "--python", python], cwd=frozen, env=env)
            source_py = runtime_python(source_env)
            package = inspect_packages(commands, source_py, "source-packages", installed=True)
            if Path(package["pixl_origin"]).resolve() != frozen / "pixl/__init__.py":
                raise RuntimeError("Locked source did not resolve confined editable runtime")
            route = useful_route(commands, [source_py, "-I", "-B", "-m", "pixl"], work / "source consumer", frozen, "source-operation", expected_runtime, frozen)
            if inventory(frozen, rows) != rows:
                raise RuntimeError("Locked sync or public operations changed frozen source inputs")
            route.update(packages=package, frozen_inputs_unchanged=True)
            result["routes"]["locked_source"] = route
        if inventory(kit) != kit_original:
            raise RuntimeError("Qualification changed supplied source kit")
        result.update(status="pass", input_kit_unchanged=True)
    except Exception as error:
        logger.exception("Installation qualification failed; preserving the failed attempt")
        result.update(status="fail", error={"type": type(error).__name__, "detail": str(error)})
    result.update(finished_at=now(), command_count=len(commands.rows), commands=commands.rows)
    write_json(evidence / "RESULT.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "cell"))
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--kit", type=Path)
    parser.add_argument("--wheel", type=Path)
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    if args.mode == "build":
        result = build_distribution(args.work, args.evidence, args.python)
    else:
        if args.kit is None or args.wheel is None:
            parser.error("cell requires --kit and --wheel")
        result = run_cell(args.work, args.evidence, args.python, args.kit, args.wheel, args.source)
    print(json.dumps({"status": result["status"], "evidence": str(args.evidence), "error": result.get("error")}))
    raise SystemExit(0 if result["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
