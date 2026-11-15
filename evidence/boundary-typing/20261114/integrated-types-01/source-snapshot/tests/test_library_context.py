"""Installed knowledge context remains complete and separate from consumer state."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pixl import codec, graph, mcp, service
from pixl.codec import PixlError

REPO = Path(__file__).resolve().parents[1]


class LibraryContextTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "consumer"
        self.root.mkdir()
        self.kit = self.base / "installed-kit"
        self.resources = self.kit / "resources"
        self.resources.mkdir(parents=True)
        self.document = graph.context(
            service.load_document(REPO / "knowledge/library.px"), "k.animation-anchors"
        )
        for record in self.document.records.values():
            if record.kind in {"S", "E", "X"}:
                name = record.fields["ur"]
                if "://" not in name:
                    source = graph.confined(REPO, name)
                    target = self.resources / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, target)
        self.library = self.resources / "knowledge/library.px"
        self.library.parent.mkdir(parents=True, exist_ok=True)
        self.library.write_bytes(codec.encode(self.document))
        graph.validate(self.document, self.resources)
        self.environment = patch.dict(os.environ, {"PIXL_PLUGIN_ROOT": str(self.kit)})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.args = {"path": "knowledge/library.px", "focus": "k.animation-anchors", "scope": "library"}

    def call(self, **extra):
        return service.call("pixl_context", self.args | extra, self.root)

    def cli(self, *extra):
        return subprocess.run(
            [sys.executable, "-m", "pixl", "context", "knowledge/library.px", "k.animation-anchors",
             "--scope", "library", *extra],
            cwd=REPO, capture_output=True, check=False,
        )

    def test_external_consumer_mcp_gets_exact_method_source_and_proof_closure(self):
        # A consumer file with the same locator must not shadow installed knowledge.
        shadow = self.root / "knowledge/library.px"
        shadow.parent.mkdir()
        shadow.write_bytes(b"consumer-owned bytes")
        response = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                 "params": {"name": "pixl_context", "arguments": self.args}}, self.root)
        self.assertFalse(response["result"].get("isError"), response)
        result = response["result"]["structuredContent"]
        self.assertEqual(result["wire"].encode(), self.library.read_bytes())
        self.assertEqual(result["bytes"], self.library.stat().st_size)
        self.assertEqual(result["hash"], codec.digest(self.document))
        self.assertEqual(result["root"], str(self.resources))
        self.assertEqual(result["scope"], "library")
        packet = codec.parse(result["wire"].encode())
        self.assertTrue({"K", "S", "E"} <= {r.kind for r in packet.records.values()})
        self.assertEqual({r.id: codec.record_hash(r) for r in packet.records.values()},
                         {r.id: codec.record_hash(r) for r in self.document.records.values()})
        self.assertEqual(shadow.read_bytes(), b"consumer-owned bytes")

    def test_default_project_scope_does_not_fall_back_to_installed_library(self):
        arguments = {key: value for key, value in self.args.items() if key != "scope"}
        with self.assertRaisesRegex(PixlError, "file_read"):
            service.call("pixl_context", arguments, self.root)
        with self.assertRaisesRegex(PixlError, "path_escape"):
            service.call("pixl_context", arguments | {"path": self.library.as_posix()}, self.root)

    def test_explicit_project_scope_preserves_default_response(self):
        shutil.copytree(self.resources, self.root, dirs_exist_ok=True)
        arguments = {key: value for key, value in self.args.items() if key != "scope"}
        default = service.call("pixl_context", arguments, self.root)
        explicit = service.call("pixl_context", arguments | {"scope": "project"}, self.root)
        self.assertEqual(default, explicit)
        self.assertNotIn("scope", default)
        self.assertNotIn("root", default)

    def test_library_rejects_traversal_and_absolute_paths(self):
        for name in ("../../consumer/state.px", self.library.as_posix(), "../resources/knowledge/library.px/../../../../outside.px"):
            with self.subTest(path=name), self.assertRaisesRegex(PixlError, "path_escape"):
                self.call(path=name)

    def test_library_rejects_resolved_symlink_escape(self):
        link = self.resources / "escaped.px"
        outside = self.base / "outside.px"
        outside.write_bytes(self.library.read_bytes())
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("Creating symlinks requires unavailable platform privileges")
        with self.assertRaisesRegex(PixlError, "path_escape"):
            self.call(path="escaped.px")

    def test_budget_keeps_entire_required_closure(self):
        size = len(self.library.read_bytes())
        self.assertEqual(self.call(budget=size)["bytes"], size)
        with self.assertRaisesRegex(PixlError, "context_budget"):
            self.call(budget=size - 1)

    def test_changed_source_cannot_be_read_as_verified_library_context(self):
        source = next(r for r in self.document.records.values() if r.kind == "S")
        path = self.resources / source.fields["ur"]
        path.write_bytes(path.read_bytes() + b"\nchanged source\n")
        with self.assertRaisesRegex(PixlError, "file_hash"):
            self.call()

    def test_changed_proof_cannot_be_read_as_verified_library_context(self):
        proof = next(r for r in self.document.records.values() if r.kind == "E")
        path = self.resources / proof.fields["ur"]
        path.write_bytes(path.read_bytes() + b"\nchanged proof\n")
        with self.assertRaisesRegex(PixlError, "file_hash"):
            self.call()

    def test_scope_and_project_authoring_options_are_rejected(self):
        for extra in ({"scope": "typo"}, {"view": "authoring"}, {"plar_path": "plar.txt"}, {"asset_id": "robot.idle"}):
            with self.subTest(extra=extra), self.assertRaisesRegex(PixlError, "context_scope"):
                self.call(**extra)
        with self.assertRaisesRegex(PixlError, "context_view"):
            self.call(view="typo")

    def test_export_is_exact_fresh_and_consumer_owned(self):
        before = {p.relative_to(self.resources): p.read_bytes() for p in self.resources.rglob("*") if p.is_file()}
        expected = self.call()
        summary = self.call(result_path="work/context.json")
        path = self.root / summary["result_path"]
        data = path.read_bytes()
        self.assertTrue(summary["result_saved"])
        self.assertEqual(json.loads(data), expected)
        self.assertEqual(summary["result_sha256"], hashlib.sha256(data).hexdigest())
        with self.assertRaisesRegex(PixlError, "result_exists"):
            self.call(result_path="work/context.json")
        self.assertEqual(path.read_bytes(), data)
        with self.assertRaisesRegex(PixlError, "path_escape"):
            self.call(result_path="../installed-kit/resources/context.json")
        self.assertEqual(before, {p.relative_to(self.resources): p.read_bytes() for p in self.resources.rglob("*") if p.is_file()})

    def test_px2_context_keeps_its_original_format(self):
        self.document.format = 2
        self.library.write_bytes(codec.encode(self.document))
        result = self.call()
        self.assertTrue(result["wire"].startswith("PX2 "))
        graph.validate(codec.parse(result["wire"].encode()), self.resources)

    def test_cli_library_wire_and_export_match_mcp(self):
        expected = self.call()["wire"].encode()
        default = self.cli()
        self.assertEqual(default.returncode, 0, default.stderr)
        self.assertEqual(default.stdout, expected)
        exported = self.cli("--root", str(self.root), "--result-path", "work/context.px")
        self.assertEqual(exported.returncode, 0, exported.stderr)
        result = json.loads(exported.stdout)
        self.assertEqual((self.root / result["result_path"]).read_bytes(), expected)
        self.assertEqual(result["media_type"], "text/plain")
        self.assertEqual(result["hash"], codec.digest(self.document))

    def test_cli_legacy_absolute_library_path_and_invalid_library_combinations(self):
        legacy = subprocess.run([sys.executable, "-m", "pixl", "context", str(self.library),
                                 "k.animation-anchors", "--root", str(self.resources)],
                                cwd=REPO, capture_output=True, check=False)
        self.assertEqual(legacy.returncode, 0, legacy.stderr)
        self.assertEqual(legacy.stdout, self.call()["wire"].encode())
        for options in (("--view", "authoring"), ("--plar", "plar.txt"), ("--asset", "robot.idle")):
            with self.subTest(options=options):
                result = self.cli(*options)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stderr)["error"], "context_scope")
        exported = self.cli("--result-path", "context.px")
        self.assertEqual(exported.returncode, 2)
        self.assertEqual(json.loads(exported.stderr)["error"], "result_path")

    def test_mcp_schema_advertises_explicit_scope_and_keeps_result_export(self):
        declaration = next(item[2] for item in mcp.TOOLS if item[0] == "pixl_context")
        self.assertEqual(declaration["properties"]["scope"]["enum"], ["project", "library"])
        self.assertIn("result_path", declaration["properties"])
        self.assertNotIn("scope", declaration["required"])


if __name__ == "__main__":
    unittest.main()
