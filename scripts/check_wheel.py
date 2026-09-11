"""Build and exercise a wheel in a temporary target, without installing globally."""

import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def run():
    with TemporaryDirectory(prefix="pixl-wheel-") as tmp:
        folder = Path(tmp)
        wheels, target, cwd = folder / "wheels", folder / "site", folder / "project"
        cwd.mkdir()
        built = subprocess.run([sys.executable, "-m", "pip", "wheel", str(ROOT), "--no-deps", "--wheel-dir", str(wheels)], capture_output=True, text=True, timeout=60)
        if built.returncode:
            raise RuntimeError(built.stdout + built.stderr)
        wheel = next(wheels.glob("pixl_agent-*.whl"))
        with zipfile.ZipFile(wheel) as archive:
            names = archive.namelist()
            for needed in ("pixl/registry.json", "pixl/resources/knowledge/pixel-art.json", "pixl/resources/knowledge/pixellab-capabilities.json"):
                if needed not in names:
                    raise RuntimeError(f"wheel missing {needed}")
        installed = subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "--no-compile", "--target", str(target), str(wheel)], capture_output=True, text=True, timeout=60)
        if installed.returncode:
            raise RuntimeError(installed.stdout + installed.stderr)
        dependency_paths = [p for p in sys.path if p.endswith("site-packages")]
        launch = f"import sys,runpy;from pathlib import Path;sys.path[:0]={[str(target)] + dependency_paths!r};import pixl;assert Path(pixl.__file__).is_relative_to({str(target)!r});sys.argv=['pixl']+sys.argv[1:];runpy.run_module('pixl',run_name='__main__')"
        env = dict(os.environ)
        env.pop("PIXL_PLUGIN_ROOT", None)
        env.pop("PYTHONPATH", None)
        checks = []
        resource_root = target / "pixl/resources"
        for args in (["knowledge", "palette-contract"], ["capabilities", "create_character"],
                     ["init", ".pixl", "--root", str(cwd)], ["validate", ".pixl/state.px", "--root", str(cwd)],
                     ["validate", str(resource_root / "knowledge/library.px"), "--root", str(resource_root)],
                     ["poc", "--out", str(cwd / "proof")]):
            result = subprocess.run([sys.executable, "-I", "-c", launch, *args], cwd=cwd, env=env, capture_output=True, timeout=20)
            if result.returncode:
                raise RuntimeError(result.stderr.decode("utf-8"))
            data = json.loads(result.stdout)
            if args[0] == "poc":
                from hashlib import sha256
                if data["status"] != "pass" or data["implementation_sha256"] != sha256((target / "pixl/poc.py").read_bytes()).hexdigest():
                    raise RuntimeError("wheel proof failed or identified a different runner")
            checks.append({"command": args[0], "status": "pass"})
        return {"status": "pass", "wheel": wheel.name, "wheel_files": len(names), "checks": checks,
                "scope": "temporary wheel installation; runtime dependencies reused; no global installation or source import"}


if __name__ == "__main__":
    result = run()
    (ROOT / "evidence/wheel-check.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
