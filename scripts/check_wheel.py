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

from scripts.family_probe import run_family_probe
from scripts.provider_probe import run_provider_probe


def run(log_dir=None):
    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required to build and verify the wheel")
    with TemporaryDirectory(prefix="pixl-wheel-") as tmp:
        folder = Path(tmp)
        wheels, target, cwd = folder / "wheels", folder / "site", folder / "project"
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
        installed = subprocess.run(
            [
                uv,
                "pip",
                "install",
                "--python",
                sys.executable,
                "--no-deps",
                "--target",
                str(target),
                str(wheel),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        if log_dir is not None:
            (Path(log_dir) / "distribution-install.log").write_text(
                installed.stdout + installed.stderr, encoding="utf-8"
            )
        if installed.returncode:
            raise RuntimeError(installed.stdout + installed.stderr)
        dependency_paths = [p for p in sys.path if p.endswith("site-packages")]
        launch = f"import sys,runpy;from pathlib import Path;sys.path[:0]={[str(target)] + dependency_paths!r};import pixl;assert Path(pixl.__file__).is_relative_to({str(target)!r});sys.argv=['pixl']+sys.argv[1:];runpy.run_module('pixl',run_name='__main__')"
        env = dict(os.environ)
        env.pop("PIXL_PLUGIN_ROOT", None)
        env.pop("PYTHONPATH", None)
        checks = []
        resource_root = target / "pixl/resources"

        def cli(args):
            result = subprocess.run(
                [sys.executable, "-I", "-c", launch, *args],
                cwd=cwd,
                env=env,
                capture_output=True,
                check=False,
                timeout=20,
            )
            if result.returncode:
                raise RuntimeError(result.stderr.decode("utf-8"))
            return json.loads(result.stdout) if result.stdout else None

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
        provider = run_provider_probe(cli, cwd)
        checks.extend(provider["checks"])
        family = run_family_probe(cli, cwd)
        checks.extend(family["checks"])
        return {
            "status": "pass",
            "wheel": wheel.name,
            "wheel_sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
            "sdist": sdist.name,
            "sdist_sha256": hashlib.sha256(sdist.read_bytes()).hexdigest(),
            "build_route": "checkout -> sdist -> wheel -> temporary installation",
            "source_documents_verified": len(inventory["documents"]),
            "wheel_files": len(names),
            "checks": checks,
            "provider_probe": provider,
            "family_probe": family,
            "scope": "uv default sdist-to-wheel build; temporary wheel installation; runtime dependencies reused; no global installation or source import; no whole-module coverage claim",
        }


if __name__ == "__main__":
    result = run()
    (ROOT / "evidence/wheel-check.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
