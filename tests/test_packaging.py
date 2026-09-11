import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

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
            launch = f"import sys,runpy;sys.path.extend({dependency_paths!r});p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name='__main__')"
            runner = [sys.executable, "-I", "-c", launch, str(plugin / "scripts/pixl.py")]
            for command in (["knowledge", "palette-contract"], ["capabilities", "create_character"],
                            ["validate", str(plugin / "resources/examples/atelier/project.px"), "--root", str(plugin / "resources")],
                            ["validate", str(plugin / "resources/knowledge/library.px"), "--root", str(plugin / "resources")],
                            ["poc", "--out", str(cwd / "proof")]):
                result = subprocess.run(runner + command, cwd=cwd, env=env, capture_output=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                data = json.loads(result.stdout)
                self.assertIsInstance(data, dict)
                if command[0] == "poc":
                    from hashlib import sha256
                    self.assertEqual(data["status"], "pass")
                    self.assertEqual(len({m for check in data["checks"] for m in check["method_ids"]}), 43)
                    self.assertEqual(data["implementation_sha256"], sha256((plugin / "runtime/pixl/poc.py").read_bytes()).hexdigest())
                    for name, expected in data["source_sha256"].items():
                        self.assertEqual(expected, sha256((plugin / "resources" / name).read_bytes()).hexdigest())

    def test_manifest_digests_match_source_and_bundle_bytes(self):
        from hashlib import sha256

        from scripts.build_plugin import build
        build()
        plugin = ROOT / "plugins/pixl"
        manifest = json.loads((plugin / "bundle-manifest.json").read_text())
        for entry in manifest["files"]:
            with self.subTest(path=entry["path"]):
                self.assertEqual(sha256((plugin / entry["path"]).read_bytes()).hexdigest(), entry["sha256"])
                self.assertEqual((plugin / entry["path"]).read_bytes(), (ROOT / entry["source"]).read_bytes())
