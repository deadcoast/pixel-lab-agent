import hashlib
import json
import runpy
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl.catalog import build
from pixl.codec import PixlError


class SourceInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "training/original-docs/source.md"
        self.path.parent.mkdir(parents=True)
        self.path.write_bytes(b"# Research\nsource meaning\n")
        (self.root / "README.md").write_text("# Package instructions\n")
        self.inventory = {
            "version": 1,
            "documents": [
                {
                    "id": "research",
                    "path": "training/original-docs/source.md",
                    "sha256": hashlib.sha256(self.path.read_bytes()).hexdigest(),
                    "lines": 2,
                    "previous": None,
                }
            ],
        }
        self.write_inventory()

    def write_inventory(self):
        (self.root / "training/source-inventory.json").write_text(
            json.dumps(self.inventory), encoding="utf-8"
        )

    def test_catalog_discovers_corpus_instead_of_package_readme(self):
        result = build(self.root)
        self.assertEqual(
            [row["path"] for row in result["documents"]],
            ["training/original-docs/source.md"],
        )
        self.assertEqual(result["documents"][0]["sections"][0]["title"], "Research")

    def test_corpus_without_inventory_does_not_silently_fall_back(self):
        (self.root / "training/source-inventory.json").unlink()
        with self.assertRaisesRegex(PixlError, "source_inventory"):
            build(self.root)

    def test_missing_source_is_an_error_not_a_smaller_catalog(self):
        self.path.unlink()
        with self.assertRaisesRegex(PixlError, "source_missing"):
            build(self.root)

    def test_changed_source_cannot_reuse_approved_identity(self):
        self.path.write_bytes(b"# Research\nchanged meaning\n")
        with self.assertRaisesRegex(PixlError, "source_hash"):
            build(self.root)

    def test_wrong_line_count_rejects_stale_locators(self):
        self.inventory["documents"][0]["lines"] = 3
        self.write_inventory()
        with self.assertRaisesRegex(PixlError, "source_lines"):
            build(self.root)

    def test_duplicate_paths_are_not_independent_sources(self):
        self.inventory["documents"].append(
            dict(self.inventory["documents"][0], id="other")
        )
        self.write_inventory()
        with self.assertRaisesRegex(PixlError, "source_inventory"):
            build(self.root)

    def test_path_escape_is_rejected(self):
        self.inventory["documents"][0]["path"] = "../outside.md"
        self.write_inventory()
        with self.assertRaisesRegex(PixlError, "path_escape"):
            build(self.root)

    def test_malformed_inventory_is_rejected(self):
        for value in (
            {"version": 2, "documents": []},
            {"version": 1, "documents": []},
            {"version": 1, "documents": "sources"},
        ):
            with self.subTest(value=value):
                self.inventory = value
                self.write_inventory()
                with self.assertRaisesRegex(PixlError, "source_inventory"):
                    build(self.root)

    def test_explicit_project_sources_are_still_supported(self):
        result = build(self.root, ["README.md"])
        self.assertEqual([row["path"] for row in result["documents"]], ["README.md"])

    def test_cli_sources_verifies_explicit_corpus_root(self):
        result = subprocess.run(
            [sys.executable, "-m", "pixl", "sources", "--root", str(self.root)],
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["files_verified"])
        self.assertEqual(data["documents"], self.inventory["documents"])

    def test_mcp_library_discovery_and_slice_work_outside_project(self):
        from pixl.mcp import dispatch

        with (
            TemporaryDirectory() as project,
            patch("pixl.service.resource_root", return_value=self.root),
        ):
            listed = dispatch(
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": "pixl_sources", "arguments": {}},
                },
                project,
            )
            self.assertFalse(listed["result"]["isError"], listed)
            self.assertEqual(
                listed["result"]["structuredContent"]["documents"],
                self.inventory["documents"],
            )
            row = self.inventory["documents"][0]
            sliced = dispatch(
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "pixl_source",
                        "arguments": {
                            "scope": "library",
                            "path": row["path"],
                            "expect": row["sha256"],
                            "start": 2,
                            "end": 2,
                        },
                    },
                },
                project,
            )
            self.assertFalse(sliced["result"]["isError"], sliced)
            self.assertEqual(
                sliced["result"]["structuredContent"]["text"], "source meaning\n"
            )

    def test_failed_source_preflight_does_not_partially_update_bundle(self):
        from scripts import build_plugin

        with TemporaryDirectory() as destination:
            plugin = Path(destination)
            runtime = self.root / "pixl"
            runtime.mkdir()
            (runtime / "example.py").write_text("new bytes\n")
            # Supply the old builder's inputs so only its absent preflight is tested.
            for name in (
                "NOTICE.md",
                "links.md",
                "AGENT-PIXELART-TRAINING.md",
                "PIXEL-ART-ASSETS.md",
                "pixel-art-deep-research-report.md",
                "research-pixel-art-systems.md",
            ):
                (self.root / name).write_text("legacy fixture\n")
            (self.root / "pyproject.toml").write_text(
                '[project]\nversion="0"\ndependencies=[]\n'
            )
            target = plugin / "runtime/pixl/example.py"
            target.parent.mkdir(parents=True)
            target.write_text("installed bytes\n")
            self.path.write_bytes(b"unreviewed new source\n")
            with (
                patch.object(build_plugin, "ROOT", self.root),
                patch.object(build_plugin, "PLUGIN", plugin),
                self.assertRaisesRegex(PixlError, "source_hash"),
            ):
                build_plugin.build()
            self.assertEqual(target.read_text(), "installed bytes\n")

    def test_bundle_prunes_only_unchanged_obsolete_generated_files(self):
        from scripts import build_plugin

        with TemporaryDirectory() as destination:
            plugin = Path(destination)
            (self.root / "pixl").mkdir()
            (self.root / "NOTICE.md").write_text("notice\n")
            (self.root / "pyproject.toml").write_text(
                '[project]\nversion="0"\ndependencies=[]\n'
            )
            obsolete = plugin / "resources/old-source.md"
            obsolete.parent.mkdir(parents=True)
            obsolete.write_bytes(b"old source\n")
            manifest = {
                "files": [
                    {
                        "path": "resources/old-source.md",
                        "sha256": hashlib.sha256(obsolete.read_bytes()).hexdigest(),
                    }
                ]
            }
            (plugin / "bundle-manifest.json").write_text(json.dumps(manifest))
            unrelated = plugin / "resources/local-note.md"
            unrelated.write_bytes(b"unmanaged\n")
            with (
                patch.object(build_plugin, "ROOT", self.root),
                patch.object(build_plugin, "PLUGIN", plugin),
            ):
                build_plugin.build()
            self.assertFalse(obsolete.exists())
            self.assertEqual(unrelated.read_bytes(), b"unmanaged\n")
            self.assertEqual(
                (plugin / "resources/training/original-docs/source.md").read_bytes(),
                self.path.read_bytes(),
            )

    def test_modified_obsolete_file_blocks_bundle_without_removing_it(self):
        from scripts import build_plugin

        with TemporaryDirectory() as destination:
            plugin = Path(destination)
            (self.root / "pixl").mkdir()
            (self.root / "NOTICE.md").write_text("new notice\n")
            (self.root / "pyproject.toml").write_text(
                '[project]\nversion="0"\ndependencies=[]\n'
            )
            obsolete = plugin / "resources/old-source.md"
            obsolete.parent.mkdir(parents=True)
            obsolete.write_bytes(b"user changed this\n")
            manifest = {
                "files": [
                    {
                        "path": "resources/old-source.md",
                        "sha256": hashlib.sha256(b"old source\n").hexdigest(),
                    }
                ]
            }
            (plugin / "bundle-manifest.json").write_text(json.dumps(manifest))
            (plugin / "NOTICE.md").write_text("installed notice\n")
            with (
                patch.object(build_plugin, "ROOT", self.root),
                patch.object(build_plugin, "PLUGIN", plugin),
                self.assertRaisesRegex(
                    ValueError, "obsolete generated file was modified"
                ),
            ):
                build_plugin.build()
            self.assertEqual(obsolete.read_bytes(), b"user changed this\n")
            self.assertEqual((plugin / "NOTICE.md").read_text(), "installed notice\n")

    def test_bad_package_metadata_does_not_publish_partial_bundle(self):
        from scripts import build_plugin

        with TemporaryDirectory() as destination:
            plugin = Path(destination)
            (self.root / "pixl").mkdir()
            (self.root / "NOTICE.md").write_text("new notice\n")
            (self.root / "pyproject.toml").write_text('[project]\nversion="0"\n')
            (plugin / "NOTICE.md").write_text("installed notice\n")
            with (
                patch.object(build_plugin, "ROOT", self.root),
                patch.object(build_plugin, "PLUGIN", plugin),
                self.assertRaises((ValueError, KeyError)),
            ):
                build_plugin.build()
            self.assertEqual((plugin / "NOTICE.md").read_text(), "installed notice\n")
            self.assertFalse((plugin / "resources").exists())

    def test_bundle_inventory_digest_matches_the_published_snapshot(self):
        from pixl.sources import load_inventory
        from scripts import build_plugin

        with TemporaryDirectory() as destination:
            plugin = Path(destination)
            (self.root / "pixl").mkdir()
            notice = self.root / "NOTICE.md"
            notice.write_text("notice\n")
            (self.root / "pyproject.toml").write_text(
                '[project]\nversion="0"\ndependencies=[]\n'
            )
            read_bytes = Path.read_bytes

            def edit_inventory_on_later_read(path):
                if path == notice:
                    self.inventory["documents"][0]["previous"] = {
                        "path": "previous.md",
                        "sha256": "0" * 64,
                        "lines": 1,
                    }
                    self.write_inventory()
                return read_bytes(path)

            with (
                patch.object(build_plugin, "ROOT", self.root),
                patch.object(build_plugin, "PLUGIN", plugin),
                patch.object(Path, "read_bytes", edit_inventory_on_later_read),
            ):
                build_plugin.build()
            shipped = plugin / "resources/training/source-inventory.json"
            manifest = json.loads((plugin / "bundle-manifest.json").read_text())
            self.assertEqual(
                manifest["source_inventory_sha256"],
                hashlib.sha256(shipped.read_bytes()).hexdigest(),
            )
            self.assertIsNone(
                load_inventory(plugin / "resources")["documents"][0]["previous"]
            )

    def test_wheel_resource_rebuild_removes_stale_source_files(self):
        from setuptools import Distribution
        from setuptools.command.build_py import build_py

        with patch("setuptools.setup"):
            namespace = runpy.run_path(
                str(Path(__file__).resolve().parents[1] / "setup.py")
            )
        command = namespace["BuildResources"](Distribution())
        (self.root / "pixl").mkdir()
        (self.root / "NOTICE.md").write_text("notice\n")
        with TemporaryDirectory() as destination:
            command.build_lib = destination
            target = Path(destination) / "pixl/resources"
            target.mkdir(parents=True)
            (target / "obsolete-source.md").write_text("obsolete bytes\n")
            with (
                patch.dict(command.run.__globals__, ROOT=self.root),
                patch.object(build_py, "run"),
            ):
                command.run()
            self.assertFalse((target / "obsolete-source.md").exists())
            self.assertEqual(
                (target / "training/original-docs/source.md").read_bytes(),
                self.path.read_bytes(),
            )

    def test_aliased_source_path_uses_captured_bytes(self):
        from scripts import build_plugin

        self.inventory["documents"][0]["path"] = "./training/original-docs/source.md"
        self.write_inventory()
        expected = self.path.read_bytes()
        capture = build_plugin.capture_inventory

        def change_after_capture(root):
            result = capture(root)
            self.path.write_bytes(b"changed after capture\n")
            return result

        with TemporaryDirectory() as destination:
            plugin = Path(destination)
            (self.root / "pixl").mkdir()
            (self.root / "NOTICE.md").write_text("notice\n")
            (self.root / "pyproject.toml").write_text(
                '[project]\nversion="0"\ndependencies=[]\n'
            )
            with (
                patch.object(build_plugin, "ROOT", self.root),
                patch.object(build_plugin, "PLUGIN", plugin),
                patch.object(
                    build_plugin, "capture_inventory", side_effect=change_after_capture
                ),
            ):
                build_plugin.build()
            self.assertEqual(
                (plugin / "resources/training/original-docs/source.md").read_bytes(),
                expected,
            )
