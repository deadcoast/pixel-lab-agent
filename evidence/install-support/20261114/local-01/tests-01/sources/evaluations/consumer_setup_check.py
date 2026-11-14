"""Retain fresh consumer installation proofs without touching the maintainer env.

Run only after freezing the source and generated plugin. This creates persistent
fixtures and refuses to reuse any output directory. It performs package installs
and local reads, but never launches a host, reads credentials or calls PixelLab.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if not __package__:
    sys.path.insert(0, str(ROOT))

from scripts.readiness_probe import run_readiness_probe

SOURCE_DIRS = (
    "pixl", ".agents", ".claude", ".codex", "plugins/pixl", "spec",
    "knowledge", "training/original-docs", "examples", "methods", "docs/research",
    "evidence/art-methods",
)
SOURCE_FILES = (
    "pyproject.toml", "uv.lock", "setup.py", "MANIFEST.in", "README.md",
    "NOTICE.md", "AGENTS.md", "training/source-inventory.json",
    "evidence/source-migration/range-review.json",
)
IGNORED = {"__pycache__", ".git", ".venv", "node_modules", ".pytest_cache", ".ruff_cache"}
FORBIDDEN = {
    "coverage", "mypy", "ruff", "setuptools", "sourcery", "tiktoken",
    "types-jsonschema", "types-setuptools",
}


def now():
    return datetime.now(UTC).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def reference(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": digest(path), "bytes": path.stat().st_size}


def write_json(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=True, indent=2)
        stream.write("\n")


def inventory(root, selected=None):
    root = Path(root).resolve()
    paths = (root / name for name in selected) if selected is not None else root.rglob("*")
    rows = {}
    for path in sorted(paths):
        if not path.is_file():
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise RuntimeError(f"Inventory path escapes its fixture: {path}")
        rows[path.relative_to(root).as_posix()] = {"sha256": digest(path), "bytes": path.stat().st_size}
    return rows


def source_inventory():
    selected = []
    for name in SOURCE_DIRS:
        folder = ROOT / name
        if not folder.is_dir():
            raise RuntimeError(f"Required source directory is missing: {name}")
        selected.extend(path.relative_to(ROOT).as_posix() for path in folder.rglob("*")
                        if path.is_file() and not IGNORED.intersection(path.relative_to(folder).parts))
    for name in SOURCE_FILES:
        if not (ROOT / name).is_file():
            raise RuntimeError(f"Required source input is missing: {name}")
        selected.append(name)
    return inventory(ROOT, selected)


def copy_exact(source, destination, rows):
    destination.mkdir(parents=True, exist_ok=False)
    for name in rows:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    if inventory(destination) != rows:
        raise RuntimeError("Copied fixture differs from its captured source inputs")


def runtime_python(environment):
    return environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def clean_environment():
    env = os.environ.copy()
    for name in ("PYTHONPATH", "PYTHONHOME", "PYTHONUSERBASE", "PIXL_PLUGIN_ROOT", "VIRTUAL_ENV",
                 "UV_PROJECT_ENVIRONMENT", "UV_PROJECT", "UV_WORKING_DIRECTORY", "UV_CONFIG_FILE",
                 "PIP_TARGET", "PIP_PREFIX", "PIP_USER", "PIP_ROOT"):
        env.pop(name, None)
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1", PIP_CONFIG_FILE=os.devnull)
    return env


class Commands:
    def __init__(self, evidence, cwd):
        self.evidence = evidence
        self.cwd = cwd
        self.rows = []

    def run(self, label, args, *, expected=0, cwd=None, env=None, timeout=240):
        index = len(self.rows) + 1
        stem = f"{index:02d}-{label}"
        record = {"label": label, "argv": list(map(str, args)), "cwd": str(cwd or self.cwd),
                  "started_at": now(), "expected_returncode": expected}
        started = time.monotonic()
        output = error = ""
        caught = None
        try:
            result = subprocess.run(record["argv"], cwd=record["cwd"], env=env or clean_environment(),
                                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                                    check=False, timeout=timeout)
            output, error = result.stdout, result.stderr
            record["returncode"] = result.returncode
        except (OSError, subprocess.TimeoutExpired) as exc:
            caught = exc
            record.update(returncode=None, error_type=type(exc).__name__)
            if isinstance(exc, subprocess.TimeoutExpired):
                output = exc.stdout or ""
                error = exc.stderr or ""
                if isinstance(output, bytes):
                    output = output.decode("utf-8", errors="replace")
                if isinstance(error, bytes):
                    error = error.decode("utf-8", errors="replace")
        record.update(finished_at=now(), elapsed_seconds=round(time.monotonic() - started, 3))
        for suffix, data in (("stdout", output), ("stderr", error)):
            path = self.evidence / f"{stem}.{suffix}.txt"
            with path.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(data)
            record[suffix] = reference(path)
        write_json(self.evidence / f"{stem}.json", record)
        self.rows.append(record)
        if caught:
            raise RuntimeError(f"{label} failed ({type(caught).__name__}); retained command receipt") from caught
        if record["returncode"] != expected:
            raise RuntimeError(f"{label} exited {record['returncode']}, expected {expected}; retained command receipt")
        return output

    def json(self, label, args, **kwargs):
        return json.loads(self.run(label, args, **kwargs))


PACKAGE_CODE = """import importlib.metadata as m, importlib.util as u, json, sys, sysconfig
spec = u.find_spec('pixl')
print(json.dumps({'executable':sys.executable,'prefix':sys.prefix,
 'site':sysconfig.get_path('purelib'),'pixl_origin':spec.origin if spec else None,
 'distributions':{d.metadata['Name'].lower().replace('_','-'):d.version for d in m.distributions()}}))
"""


def packages(commands, python, label, *, installed):
    result = commands.json(label, [python, "-I", "-B", "-c", PACKAGE_CODE])
    found = set(result["distributions"])
    if found & FORBIDDEN:
        raise RuntimeError(f"Maintainer packages found in {label}: {sorted(found & FORBIDDEN)}")
    if installed and not {"pillow", "jsonschema", "referencing"} <= found:
        raise RuntimeError(f"Missing runtime dependencies in {label}")
    return result


def retained_probe(commands, evidence, label, command, consumer, kind, package_root, installation=None):
    package_before = inventory(package_root)
    write_json(evidence / f"{label}-package-before.json", package_before)
    consumer_before = None
    sequence = 0

    def cli(args):
        nonlocal consumer_before, sequence
        if consumer_before is None:
            consumer_before = inventory(consumer)
            write_json(evidence / f"{label}-consumer-before.json", consumer_before)
        sequence += 1
        return commands.json(f"{label}-probe-{sequence}", [*command, *args])

    result = run_readiness_probe(cli, consumer, kind, installation)
    package_after, consumer_after = inventory(package_root), inventory(consumer)
    write_json(evidence / f"{label}-package-after.json", package_after)
    write_json(evidence / f"{label}-consumer-after.json", consumer_after)
    if package_after != package_before or consumer_after != consumer_before:
        raise RuntimeError(f"{label} read-only probe changed package or consumer bytes")
    if result["report"]["installation"]["status"] != "present":
        raise RuntimeError(f"{label} installation is not complete")
    result.update(package_files_unchanged=True, package_file_count=len(package_before),
                  consumer_file_count=len(consumer_after), command=list(map(str, command)))
    write_json(evidence / f"{label}-probe.json", result)
    return result


def run(work, evidence):
    work, evidence = Path(work).resolve(), Path(evidence).resolve()
    if not work.is_relative_to(ROOT / "build") or work == ROOT / "build":
        raise ValueError("Work output must be a fresh child of this repository's build directory")
    allowed_evidence = ROOT / "evidence/readiness/20261109/setup"
    if not evidence.is_relative_to(allowed_evidence):
        raise ValueError("Evidence output must be confined to evidence/readiness/20261109/setup")
    if work.exists() or evidence.exists():
        raise FileExistsError("Choose fresh work and evidence directories; retained attempts are immutable")
    uv = shutil.which("uv")
    if not uv:
        raise RuntimeError("uv must be available for wheel and locked source installation")
    work.mkdir(parents=True, exist_ok=False)
    evidence.mkdir(parents=True, exist_ok=False)
    unrelated = work / "unrelated working directory"
    unrelated.mkdir()
    commands = Commands(evidence, unrelated)
    result = {"version": 1, "status": "running", "started_at": now(), "work": str(work),
              "evidence": str(evidence), "routes": {}, "scope":
              "Fresh local installation and exact source reads only. Inventories supplied to readiness are fixtures, not live host or provider observations.",
              "limits": ["No native role loading or instruction following established.",
                         "No provider discovery, authentication, generation or artwork acceptance performed."],
              "installer_isolation": "Fresh explicit interpreters; inherited Python/project/pip target overrides removed and pip config disabled. No global installation target used.",
              "verifier": reference(__file__), "readiness_probe": reference(ROOT / "scripts/readiness_probe.py")}
    write_json(evidence / "START.json", result)
    try:
        inputs = source_inventory()
        write_json(evidence / "source-inputs.json", inputs)
        maintainer_config = reference(ROOT / ".venv/pyvenv.cfg")
        maintainer_python = reference(runtime_python(ROOT / ".venv"))
        fixture = work / "source checkout"
        copy_exact(ROOT, fixture, inputs)
        kit = work / "copied kit"
        kit_input = inventory(fixture / "plugins/pixl")
        copy_exact(fixture / "plugins/pixl", kit, kit_input)
        result["bundle_manifest"] = reference(kit / "bundle-manifest.json")

        # Exactly the copied-kit guide's venv/pip route, kept for native trials.
        runtime = work / "runtime"
        python = runtime_python(runtime)
        commands.run("kit-create-venv", [sys.executable, "-m", "venv", runtime])
        bare_packages = packages(commands, python, "bare-packages", installed=False)
        if bare_packages["pixl_origin"] is not None or {"pillow", "jsonschema"} & set(bare_packages["distributions"]):
            raise RuntimeError("Bare environment inherited PIXL or runtime dependencies")
        bare_consumer = work / "bare consumer"
        bare_consumer.mkdir()
        bare_before = inventory(bare_consumer)
        write_json(evidence / "bare-consumer-before.json", bare_before)
        write_json(evidence / "bare-package-before.json", inventory(kit))
        bare = commands.json("bare-readiness", [python, "-I", "-B", kit / "scripts/pixl.py", "readiness",
                             "--root", bare_consumer, "--host", "codex", "--installation", kit], expected=1)
        if bare.get("status") != "reported" or bare["dependencies"]["status"] != "incomplete":
            raise RuntimeError("Missing dependencies did not produce a structured incomplete report")
        if bare["local_operations"]["runtime_requirements"] != "incomplete":
            raise RuntimeError("Bare environment incorrectly claimed runtime prerequisites")
        if bare["official_pixellab"]["visibility"]["status"] != "not_observed":
            raise RuntimeError("Bare readiness inferred provider visibility")
        write_json(evidence / "bare-consumer-after.json", inventory(bare_consumer))
        write_json(evidence / "bare-package-after.json", inventory(kit))
        if inventory(bare_consumer) != bare_before or inventory(kit) != kit_input:
            raise RuntimeError("Bare readiness changed project or kit files")
        result["routes"]["bare_bootstrap"] = {"status": "pass", "returncode": 1, "report": bare,
                                              "packages": bare_packages, "project_and_kit_unchanged": True}
        commands.run("kit-install-requirements", [python, "-m", "pip", "install", "-r", kit / "requirements.txt"])
        kit_packages = packages(commands, python, "kit-packages", installed=True)
        if kit_packages["pixl_origin"] is not None:
            raise RuntimeError("Copied-kit proof unexpectedly has an installed or inherited PIXL package")
        result["routes"]["copied_kit"] = retained_probe(
            commands, evidence, "kit", [python, "-I", "-B", kit / "scripts/pixl.py"],
            work / "kit consumer", "plugin", kit, kit)
        result["routes"]["copied_kit"]["packages"] = kit_packages
        result["runtime_python"] = str(python)
        write_json(evidence / "RUNTIME-READY.json", {"runtime_python": str(python),
                   "copied_kit": str(kit), "packages": kit_packages, "scope": result["scope"]})

        # Build from the frozen confined source, then install the exact wheel.
        wheels = work / "distribution"
        commands.run("wheel-build", [uv, "build", "--python", sys.executable, "--out-dir", wheels, fixture])
        artifacts = sorted(wheels.glob("*.whl"))
        if len(artifacts) != 1:
            raise RuntimeError("Build did not produce exactly one wheel")
        wheel = artifacts[0]
        result["distribution"] = [reference(path) for path in sorted(wheels.iterdir()) if path.is_file()]
        wheel_env = work / "wheel runtime"
        wheel_python = runtime_python(wheel_env)
        commands.run("wheel-create-venv", [sys.executable, "-m", "venv", wheel_env])
        commands.run("wheel-install", [wheel_python, "-m", "pip", "install", wheel])
        wheel_packages = packages(commands, wheel_python, "wheel-packages", installed=True)
        origin = Path(wheel_packages["pixl_origin"] or "").resolve()
        site = Path(wheel_packages["site"]).resolve()
        if not site.is_relative_to(wheel_env) or not origin.is_relative_to(site):
            raise RuntimeError("Wheel runtime resolved PIXL outside its installed site-packages")
        console = wheel_env / ("Scripts/pixl.exe" if os.name == "nt" else "bin/pixl")
        result["routes"]["wheel"] = retained_probe(
            commands, evidence, "wheel", [console], work / "wheel consumer", "wheel", origin.parent)
        result["routes"]["wheel"].update(packages=wheel_packages, wheel=reference(wheel),
                                        console_entrypoint=reference(console))

        # No maintainer group; explicitly confine uv's project environment.
        source_env = fixture / ".venv"
        env = clean_environment()
        env["UV_PROJECT_ENVIRONMENT"] = str(source_env)
        commands.run("source-sync-runtime-only", [uv, "sync", "--locked", "--no-dev", "--python", sys.executable],
                     cwd=fixture, env=env)
        source_python = runtime_python(source_env)
        source_packages = packages(commands, source_python, "source-packages", installed=True)
        if Path(source_packages["pixl_origin"] or "").resolve() != fixture / "pixl/__init__.py":
            raise RuntimeError("Source environment did not resolve its confined editable package")
        result["routes"]["source"] = retained_probe(
            commands, evidence, "source", [source_python, "-I", "-B", "-m", "pixl"],
            work / "source consumer", "source", fixture / "pixl", fixture)
        result["routes"]["source"]["packages"] = source_packages

        copied_after = inventory(fixture, inputs)
        write_json(evidence / "source-inputs-after.json", copied_after)
        if copied_after != inputs:
            raise RuntimeError("Installation/probe changed frozen source input bytes")
        if reference(ROOT / ".venv/pyvenv.cfg") != maintainer_config or reference(runtime_python(ROOT / ".venv")) != maintainer_python:
            raise RuntimeError("The maintainer environment identity changed during setup verification")
        result["maintainer_environment"] = {"pyvenv_cfg": maintainer_config, "python": maintainer_python,
                                            "selected_identity_files_unchanged": True,
                                            "scope": "All installations targeted fresh fixture environments; original environment was not a target."}
        result.update(status="pass", frozen_source_inputs_unchanged=True)
    except Exception as exc:  # noqa: BLE001 - Retain any failed proof; never erase or silently retry an attempt.
        result.update(status="fail", error={"type": type(exc).__name__, "detail": str(exc)})
    result.update(finished_at=now(), command_count=len(commands.rows), commands=commands.rows)
    write_json(evidence / "RESULT.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, default=ROOT / "build/readiness-setup-01")
    parser.add_argument("--evidence", type=Path, default=ROOT / "evidence/readiness/20261109/setup/attempt-01")
    args = parser.parse_args()
    result = run(args.work, args.evidence)
    print(json.dumps({"status": result["status"], "evidence": result["evidence"],
                      "runtime_python": result.get("runtime_python"), "error": result.get("error")}, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
