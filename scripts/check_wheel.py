"""Build and exercise a wheel in a temporary target, without installing globally."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
if not __package__:
    sys.path.insert(0, str(ROOT))

from scripts.candidate_review_probe import run_candidate_review_probe
from scripts.family_probe import run_family_probe
from scripts.plar_probe import run_plar_probe
from scripts.production_plan_probe import run_production_plan_probe
from scripts.provider_probe import run_provider_probe
from scripts.readiness_probe import run_readiness_probe
from scripts.retention_probe import run_retention_probe


def run(log_dir=None):
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required to build and verify the wheel")
    with TemporaryDirectory(prefix="pixl-wheel-") as tmp:
        folder = Path(tmp)
        wheels, cwd = folder / "wheels", folder / "project"
        cwd.mkdir()
        built = subprocess.run(
            [
                uv,
                "build",
                "--python",
                sys.executable,
                "--out-dir",
                str(wheels),
                str(ROOT),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        if log_dir is not None:
            Path(log_dir).mkdir(parents=True, exist_ok=True)
            (Path(log_dir) / "distribution-build.log").write_text(
                built.stdout + built.stderr, encoding="utf-8"
            )
        if built.returncode:
            raise RuntimeError(built.stdout + built.stderr)
        sdist = next(wheels.glob("pixl_agent-*.tar.gz"))
        source_inventory = json.loads(
            (ROOT / "training/source-inventory.json").read_bytes()
        )
        with tarfile.open(sdist) as source_archive:
            prefix = source_archive.getmembers()[0].name.split("/", 1)[0]
            for row in source_inventory["documents"]:
                member = source_archive.extractfile(prefix + "/" + row["path"])
                if (
                    member is None
                    or hashlib.sha256(member.read()).hexdigest() != row["sha256"]
                ):
                    raise RuntimeError(f"sdist source identity differs: {row['path']}")
        wheel = next(wheels.glob("pixl_agent-*.whl"))
        with zipfile.ZipFile(wheel) as archive:
            names = archive.namelist()
            for needed in (
                "pixl/registry.json",
                "pixl/registry-v2.json",
                "pixl/resources/spec/PIXL-2.md",
                "pixl/resources/knowledge/pixel-art.json",
                "pixl/resources/knowledge/pixellab-capabilities.json",
                "pixl/resources/pixl/__init__.py",
                "pixl/resources/pixl/service.py",
                "pixl/resources/training/source-inventory.json",
                "pixl/resources/training/original-docs/PIXEL-ART-DEEP-RESEARCH.md",
                "pixl/resources/evidence/source-migration/range-review.json",
            ):
                if needed not in names:
                    raise RuntimeError(f"wheel missing {needed}")
            if (
                archive.read("pixl/resources/agent/PROFILE.md")
                != (ROOT / ".agents/PROFILE.md").read_bytes()
            ):
                raise RuntimeError(
                    "wheel profile differs from canonical .agents/PROFILE.md"
                )
            inventory = json.loads(
                archive.read("pixl/resources/training/source-inventory.json")
            )
            if inventory != source_inventory:
                raise RuntimeError("wheel inventory differs from source checkout")
            for row in inventory["documents"]:
                if (
                    hashlib.sha256(
                        archive.read("pixl/resources/" + row["path"])
                    ).hexdigest()
                    != row["sha256"]
                ):
                    raise RuntimeError(f"wheel source identity differs: {row['path']}")
                previous = row.get("previous")
                if (
                    previous
                    and previous["path"] != row["path"]
                    and "pixl/resources/" + previous["path"] in names
                ):
                    raise RuntimeError(
                        f"wheel retained obsolete source {previous['path']}"
                    )
            for path in (ROOT / "pixl").iterdir():
                if path.suffix in (".py", ".json"):
                    for prefix in ("pixl/", "pixl/resources/pixl/"):
                        if archive.read(prefix + path.name) != path.read_bytes():
                            raise RuntimeError(
                                f"wheel runtime differs: {prefix}{path.name}"
                            )
        # A fresh unseeded environment proves runtime use without maintainer tooling.
        environment = folder / "runtime"
        created = subprocess.run(
            [uv, "venv", "--python", sys.executable, str(environment)],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        if created.returncode:
            raise RuntimeError(created.stdout + created.stderr)
        runtime_python = environment / (
            "Scripts/python.exe" if os.name == "nt" else "bin/python"
        )
        installed = subprocess.run(
            [uv, "pip", "install", "--python", str(runtime_python), str(wheel)],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        if log_dir is not None:
            (Path(log_dir) / "distribution-install.log").write_text(
                created.stdout + created.stderr + installed.stdout + installed.stderr,
                encoding="utf-8",
            )
        if installed.returncode:
            raise RuntimeError(installed.stdout + installed.stderr)
        environment_info = json.loads(
            subprocess.check_output(
                [
                    str(runtime_python),
                    "-I",
                    "-c",
                    (
                        "import json,sysconfig;from importlib.metadata import distributions;"
                        "print(json.dumps({'site':sysconfig.get_path('purelib'),"
                        "'packages':sorted(d.metadata['Name'].lower() for d in distributions())}))"
                    ),
                ],
                cwd=cwd,
                text=True,
            )
        )
        target = Path(environment_info["site"])
        forbidden = {
            "coverage",
            "mypy",
            "ruff",
            "setuptools",
            "sourcery",
            "tiktoken",
            "types-jsonschema",
            "types-setuptools",
        }
        if forbidden.intersection(environment_info["packages"]):
            raise RuntimeError("runtime install contains development tooling")
        launch = f"import sys,runpy;from pathlib import Path;import pixl;assert Path(pixl.__file__).is_relative_to({str(target)!r});sys.argv=['pixl']+sys.argv[1:];runpy.run_module('pixl',run_name='__main__')"
        env = dict(os.environ)
        env.pop("PIXL_PLUGIN_ROOT", None)
        env.pop("PYTHONPATH", None)
        checks = []
        resource_root = target / "pixl/resources"

        def cli(args):
            result = subprocess.run(
                [str(runtime_python), "-I", "-c", launch, *args],
                cwd=cwd,
                env=env,
                capture_output=True,
                check=False,
                timeout=20,
            )
            if result.returncode:
                raise RuntimeError(result.stderr.decode("utf-8"))
            return json.loads(result.stdout) if result.stdout else None

        shutil.copytree(resource_root / "examples/plar-project", cwd / "consumer")
        plar_packet = cli(
            [
                "plar",
                "read",
                "--root",
                str(cwd / "consumer"),
                "--asset",
                "queue.working",
            ]
        )
        if plar_packet["asset"]["delivery"]["path"] != "assets/working.png":
            raise RuntimeError("installed PLAR handoff differs from consumer contract")
        checks.append({"command": "plar", "status": "pass"})
        plar_preparation = run_plar_probe(cli, cwd / "consumer")
        checks.append(
            {"command": "plar selected preparation and refresh", **plar_preparation}
        )
        shutil.copytree(resource_root / "examples/delegation", cwd / "directions")
        reference_packet = cli(
            [
                "plar",
                "read",
                "--root",
                str(cwd / "directions"),
                "--asset",
                "robot.directions",
            ]
        )
        reference = reference_packet["visual_references"][0]
        if (
            reference["role"] != "identity"
            or reference["binding"] != "current"
            or not Path(reference["absolute_path"]).is_relative_to(cwd / "directions")
            or reference_packet["dependencies"][0]["id"] != "robot.base"
            or not reference_packet["dependencies"][0]["requirements"]
            or len(reference_packet["requirements_hash"]) != 64
        ):
            raise RuntimeError(
                "installed reference handoff lost its dependency context"
            )
        checks.append({"command": "plar reference handoff", "status": "pass"})
        retention_check = run_retention_probe(cli, cwd / "retained library project")
        checks.append({"command": "retain-library", **retention_check})
        for args in (
            ["sources"],
            ["intake", ".px2", "--root", str(cwd), "--brief", "Canvas unresolved"],
            ["workflow", ".px2/state.px", "--root", str(cwd)],
            [
                "workflow",
                str(resource_root / "examples/intake/project.px"),
                "--root",
                str(resource_root),
            ],
            ["knowledge", "palette-contract"],
            ["capabilities", "create_character"],
            ["init", ".pixl", "--root", str(cwd)],
            ["validate", ".pixl/state.px", "--root", str(cwd)],
            [
                "validate",
                str(resource_root / "knowledge/library.px"),
                "--root",
                str(resource_root),
            ],
            ["poc", "--out", str(cwd / "proof")],
        ):
            data = cli(args)
            if args[0] == "sources" and (
                not data["files_verified"] or Path(data["root"]) != resource_root
            ):
                raise RuntimeError(
                    "wheel source discovery did not use installed resources"
                )
            if args[0] == "poc":
                from hashlib import sha256

                if (
                    data["status"] != "pass"
                    or data["implementation_sha256"]
                    != sha256((target / "pixl/poc.py").read_bytes()).hexdigest()
                ):
                    raise RuntimeError(
                        "wheel proof failed or identified a different runner"
                    )
            checks.append({"command": args[0], "status": "pass"})
        # The copied plugin also runs with only this environment's production dependencies.
        plugin = folder / "copied plugin"
        shutil.copytree(
            ROOT / "plugins/pixl", plugin, ignore=shutil.ignore_patterns("__pycache__")
        )
        copied = subprocess.run(
            [
                str(runtime_python),
                "-I",
                str(plugin / "scripts/pixl.py"),
                "knowledge",
                "palette-contract",
            ],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
        if copied.returncode or not json.loads(copied.stdout):
            raise RuntimeError(
                "minimal copied-plugin execution failed: " + copied.stderr
            )
        checks.append(
            {"command": "copied-plugin with runtime dependencies", "status": "pass"}
        )

        def plugin_cli(args):
            result = subprocess.run(
                [str(runtime_python), "-I", str(plugin / "scripts/pixl.py"), *args],
                cwd=cwd,
                env=env,
                capture_output=True,
                check=False,
                timeout=20,
            )
            if result.returncode:
                raise RuntimeError(result.stderr.decode("utf-8"))
            return json.loads(result.stdout)

        readiness = run_readiness_probe(cli, cwd / "wheel-readiness", "wheel")
        copied_readiness = run_readiness_probe(plugin_cli, cwd / "plugin-readiness", "plugin", plugin)
        checks.append({"command": "installed read-only readiness", **readiness})
        checks.append({"command": "copied-plugin read-only readiness", **copied_readiness})
        shutil.copytree(
            plugin / "resources/examples/plar-project", cwd / "plugin consumer"
        )
        copied_plar = run_plar_probe(plugin_cli, cwd / "plugin consumer")
        checks.append(
            {"command": "copied-plugin PLAR preparation and refresh", **copied_plar}
        )
        provider = run_provider_probe(cli, cwd)
        checks.extend(provider["checks"])
        family = run_family_probe(cli, cwd)
        checks.extend(family["checks"])
        review = run_candidate_review_probe(cli, cwd / "candidate-review-wheel")
        copied_review = run_candidate_review_probe(plugin_cli, cwd / "candidate-review-plugin")
        checks.append({"command": "installed candidate/family review", **review})
        checks.append({"command": "copied-plugin candidate/family review", **copied_review})
        shutil.copytree(cwd / "family-fixture", cwd / "plugin-family-authoring")
        authoring = run_production_plan_probe(cli, cwd / "family-fixture")
        copied_authoring = run_production_plan_probe(plugin_cli, cwd / "plugin-family-authoring")
        checks.append({"command": "installed production-plan and stage-prepare", **authoring})
        checks.append({"command": "copied-plugin production-plan and stage-prepare", **copied_authoring})
        return {
            "status": "pass",
            "wheel": wheel.name,
            "wheel_sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
            "sdist": sdist.name,
            "sdist_sha256": hashlib.sha256(sdist.read_bytes()).hexdigest(),
            "build_route": "checkout -> sdist -> wheel -> fresh runtime environment",
            "runtime_packages": environment_info["packages"],
            "source_documents_verified": len(inventory["documents"]),
            "wheel_files": len(names),
            "checks": checks,
            "provider_probe": provider,
            "family_probe": family,
            "production_authoring": {"wheel": authoring, "copied_plugin": copied_authoring},
            "readiness": {"wheel": readiness, "copied_plugin": copied_readiness},
            "scope": "uv default sdist-to-wheel build; fresh wheel installation with resolved production dependencies; copied-plugin execution; no global installation or source import; no whole-module coverage claim",
        }


if __name__ == "__main__":
    result = run()
    (ROOT / "evidence/wheel-check.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
