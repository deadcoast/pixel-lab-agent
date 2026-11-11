"""Public destination import exports exact observations without accepting state."""

import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import codec, mcp, service, store
from tests.test_destination_observation import observation_fixture


class DestinationSurfaceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        observation_fixture(self.root)
        self.initial = codec.digest(store.load(self.root / ".pixl"))

    def arguments(self, out="work/imported"):
        return {"path": ".pixl/state.px", "candidate_id": "package",
                "report_path": "capture/observation.json", "out": out}

    def test_mcp_export_and_metadata_preserve_explicit_acceptance_boundary(self):
        tools = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, self.root)["result"]["tools"]
        tool = next(t for t in tools if t["name"] == "pixl_destination_import")
        self.assertFalse(tool["annotations"]["readOnlyHint"])
        self.assertIn("result_path", tool["inputSchema"]["properties"])
        reply = mcp.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
            "name": "pixl_destination_import", "arguments": {**self.arguments(), "result_path": "work/result.json"}}}, self.root)
        self.assertFalse(reply["result"].get("isError"), reply)
        summary = reply["result"]["structuredContent"]
        raw = (self.root / summary["result_path"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), summary["result_sha256"])
        saved = json.loads(raw)
        self.assertEqual(saved["hash_domains"]["binding_hash"], "candidate_bindings_sha256")
        self.assertEqual(saved["hash_domains"]["bundle.sha256"], "file_sha256")
        self.assertTrue(saved["files_verified"])
        for name in ("renderer_executed", "automatic_acceptance", "state_changed"):
            self.assertIs(saved[name], False)
        self.assertEqual(codec.digest(store.load(self.root / ".pixl")), self.initial)

    def test_cli_and_mcp_retain_same_content_and_refuse_overwrite(self):
        via_service = service.call("pixl_destination_import", self.arguments(), self.root)
        command = [sys.executable, "-m", "pixl", "destination-import", str(self.root / ".pixl/state.px"), "package",
                   "capture/observation.json", "--out", "work/cli", "--root", str(self.root),
                   "--result-path", "work/cli-result.json"]
        result = subprocess.run(command, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = json.loads((self.root / json.loads(result.stdout)["result_path"]).read_bytes())
        self.assertEqual(via_service["bundle"]["sha256"], saved["bundle"]["sha256"])
        before = (self.root / "work/cli-result.json").read_bytes()
        retry = subprocess.run(command, capture_output=True, check=False)
        self.assertEqual(retry.returncode, 2)
        self.assertEqual((self.root / "work/cli-result.json").read_bytes(), before)
        self.assertEqual(codec.digest(store.load(self.root / ".pixl")), self.initial)

    def test_export_collision_preflight_writes_no_import_directory(self):
        (self.root / "existing.json").write_text("keep", encoding="utf-8")
        with self.assertRaises(codec.PixlError):
            service.call("pixl_destination_import", {**self.arguments(), "result_path": "existing.json"}, self.root)
        self.assertFalse((self.root / "work/imported").exists())
        self.assertEqual(codec.digest(store.load(self.root / ".pixl")), self.initial)

    def test_cli_state_path_remains_relative_to_working_directory(self):
        relative_state = os.path.relpath(self.root / ".pixl/state.px", Path.cwd())
        result = subprocess.run([sys.executable, "-m", "pixl", "destination-import", relative_state,
                                 "package", "capture/observation.json", "--out", "work/relative",
                                 "--root", str(self.root)], capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["files_verified"])
        self.assertEqual(codec.digest(store.load(self.root / ".pixl")), self.initial)


if __name__ == "__main__":
    unittest.main()
