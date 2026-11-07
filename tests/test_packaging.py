import json
import os
import runpy
import shutil
import subprocess
import sys
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class PackagingTests(unittest.TestCase):
    def test_copied_launcher_rejects_old_python_before_runtime_import(self):
        launcher = runpy.run_path(str(ROOT / "plugins/pixl/scripts/pixl.py"))
        errors = StringIO()
        with (
            patch.object(sys, "version_info", (3, 10, 0)),
            patch.object(runpy, "run_module") as run_module,
            redirect_stderr(errors),
            self.assertRaises(SystemExit) as failure,
        ):
            launcher["main"]()
        self.assertEqual(failure.exception.code, 2)
        self.assertIn("Python 3.11 or newer", errors.getvalue())
        run_module.assert_not_called()

    def test_resource_source_package_can_run_its_own_proofs(self):
        from scripts.build_plugin import build

        build()
        with TemporaryDirectory(prefix="pixl source package ") as tmp:
            resources = Path(tmp) / "resources"
            shutil.copytree(
                ROOT / "plugins/pixl/resources",
                resources,
                ignore=shutil.ignore_patterns("__pycache__"),
            )
            self.assertTrue(
                (resources / "pixl/__init__.py").is_file(),
                "source evidence needs a complete Python package",
            )
            env = dict(os.environ)
            env.pop("PYTHONPATH", None)
            env.pop("PIXL_PLUGIN_ROOT", None)
            dependency_paths = [p for p in sys.path if p.endswith("site-packages")]
            launch = (
                "import sys,json;from pathlib import Path;"
                f"sys.path[:0]={[str(resources)] + dependency_paths!r};"
                "import pixl;from pixl.service import resource_root;from pixl.poc import run_all;"
                f"assert Path(pixl.__file__).resolve().parent==Path({str(resources / 'pixl')!r});"
                f"assert resource_root()==Path({str(resources)!r});"
                f"report=run_all(Path({str(Path(tmp) / 'proof')!r}));"
                "print(json.dumps({'status':report['status'],'methods':len({m for c in report['checks'] for m in c['method_ids']})}))"
            )
            result = subprocess.run(
                [sys.executable, "-I", "-c", launch],
                cwd=tmp,
                env=env,
                capture_output=True,
                check=False,
                timeout=20,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual(
                json.loads(result.stdout), {"status": "pass", "methods": 43}
            )

    def test_relocated_bundle_reads_knowledge_and_uses_own_runtime(self):
        from scripts.build_plugin import build

        build()
        with TemporaryDirectory(prefix="pixl copied kit ") as tmp:
            plugin = Path(tmp) / "kit" / "pixl"
            shutil.copytree(
                ROOT / "plugins/pixl",
                plugin,
                ignore=shutil.ignore_patterns("__pycache__"),
            )
            self.assertEqual(
                (plugin / "resources/agent/PROFILE.md").read_bytes(),
                (ROOT / ".agents/PROFILE.md").read_bytes(),
            )
            cwd = Path(tmp) / "project"
            cwd.mkdir()
            env = dict(os.environ)
            env.pop("PYTHONPATH", None)
            env.pop("PIXL_PLUGIN_ROOT", None)
            # Keep the test interpreter's dependency sites, never its cwd/source path.
            # -I normally hides user-site Pillow on this Windows installation.
            dependency_paths = [p for p in sys.path if p.endswith("site-packages")]
            launch = f"import sys,runpy;sys.path.extend({dependency_paths!r});p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name='__main__')"
            runner = [
                sys.executable,
                "-I",
                "-c",
                launch,
                str(plugin / "scripts/pixl.py"),
            ]

            def cli(command):
                result = subprocess.run(
                    runner + command,
                    cwd=cwd,
                    env=env,
                    capture_output=True,
                    check=False,
                    timeout=20,
                )
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                return json.loads(result.stdout) if result.stdout else None

            shutil.copytree(ROOT / "examples/plar-project", cwd / "consumer")
            packet = cli(
                [
                    "plar",
                    "read",
                    "--root",
                    str(cwd / "consumer"),
                    "--asset",
                    "queue.working",
                ]
            )
            self.assertEqual(packet["asset"]["delivery"]["path"], "assets/working.png")
            self.assertTrue((plugin / "skills/plar/SKILL.md").is_file())
            for command in (
                ["sources"],
                [
                    "intake",
                    str(cwd / ".px2"),
                    "--root",
                    str(cwd),
                    "--brief",
                    "No chosen canvas",
                ],
                ["workflow", str(cwd / ".px2/state.px"), "--root", str(cwd)],
                [
                    "workflow",
                    str(plugin / "resources/examples/intake/project.px"),
                    "--root",
                    str(plugin / "resources"),
                ],
                ["knowledge", "palette-contract"],
                ["capabilities", "create_character"],
                [
                    "validate",
                    str(plugin / "resources/examples/atelier/project.px"),
                    "--root",
                    str(plugin / "resources"),
                ],
                [
                    "validate",
                    str(plugin / "resources/knowledge/library.px"),
                    "--root",
                    str(plugin / "resources"),
                ],
                ["poc", "--out", str(cwd / "proof")],
            ):
                data = cli(command)
                self.assertIsInstance(data, dict)
                if command[0] == "workflow":
                    self.assertEqual(data["format"], 2)
                    self.assertTrue(data["files_verified"])
                    self.assertEqual(data["ready"], [])
                if command[0] == "sources":
                    self.assertTrue(data["files_verified"])
                    self.assertEqual(Path(data["root"]), plugin / "resources")
                    for source in data["documents"]:
                        self.assertTrue(
                            (plugin / "resources" / source["path"]).is_file()
                        )
                        self.assertFalse(
                            (plugin / "resources" / source["previous"]["path"]).exists()
                        )
                if command[0] == "poc":
                    from hashlib import sha256

                    self.assertEqual(data["status"], "pass")
                    self.assertEqual(
                        len(
                            {m for check in data["checks"] for m in check["method_ids"]}
                        ),
                        43,
                    )
                    self.assertEqual(
                        data["implementation_sha256"],
                        sha256(
                            (plugin / "runtime/pixl/poc.py").read_bytes()
                        ).hexdigest(),
                    )
                    for name, expected in data["source_sha256"].items():
                        self.assertEqual(
                            expected,
                            sha256(
                                (plugin / "resources" / name).read_bytes()
                            ).hexdigest(),
                        )

            from scripts.provider_probe import run_provider_probe

            provider = run_provider_probe(cli, cwd)
            self.assertEqual(provider["status"], "pass")
            self.assertFalse(provider["remote_executed"])

            from scripts.family_probe import run_family_probe

            family = run_family_probe(cli, cwd)
            self.assertEqual(family["status"], "pass")
            self.assertFalse(family["remote_executed"])

    def test_manifest_digests_match_source_and_bundle_bytes(self):
        from hashlib import sha256

        from scripts.build_plugin import build

        build()
        plugin = ROOT / "plugins/pixl"
        manifest = json.loads((plugin / "bundle-manifest.json").read_text())
        for entry in manifest["files"]:
            with self.subTest(path=entry["path"]):
                self.assertEqual(
                    sha256((plugin / entry["path"]).read_bytes()).hexdigest(),
                    entry["sha256"],
                )
                self.assertEqual(
                    (plugin / entry["path"]).read_bytes(),
                    (ROOT / entry["source"]).read_bytes(),
                )
