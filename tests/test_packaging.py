from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
import site


ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def test_relocated_bundle_reads_knowledge_and_uses_own_runtime(self):
        from scripts.build_plugin import build
        build()
        with TemporaryDirectory(prefix="pixl copied kit ") as tmp:
            plugin = Path(tmp) / "kit" / "pixl"
            shutil.copytree(ROOT / "plugins/pixl", plugin, ignore=shutil.ignore_patterns("__pycache__"))
            cwd = Path(tmp) / "project"
            cwd.mkdir()
            env = dict(os.environ)
            env.pop("PYTHONPATH", None)
            env.pop("PIXL_PLUGIN_ROOT", None)
            # Keep the test interpreter's dependency sites, never its cwd/source path.
            # -I normally hides user-site Pillow on this Windows installation.
            dependency_paths = [p for p in sys.path if p.endswith("site-packages")]
            launch = "import sys,runpy;sys.path.extend(" + repr(dependency_paths) + ");p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name='__main__')"
            runner = [sys.executable, "-I", "-c", launch, str(plugin / "scripts/pixl.py")]
            for command in (["knowledge", "palette-contract"], ["capabilities", "create_character"],
                            ["validate", str(plugin / "resources/examples/atelier/project.px"), "--root", str(plugin / "resources")]):
                result = subprocess.run(runner + command, cwd=cwd, env=env, capture_output=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                data = json.loads(result.stdout)
                self.assertIsInstance(data, dict)

    def test_manifest_digests_match_source_and_bundle_bytes(self):
        from scripts.build_plugin import build
        from hashlib import sha256
        build()
        plugin = ROOT / "plugins/pixl"
        manifest = json.loads((plugin / "bundle-manifest.json").read_text())
        for entry in manifest["files"]:
            with self.subTest(path=entry["path"]):
                self.assertEqual(sha256((plugin / entry["path"]).read_bytes()).hexdigest(), entry["sha256"])
                self.assertEqual((plugin / entry["path"]).read_bytes(), (ROOT / entry["source"]).read_bytes())
