"""Public execution routes retain unavailable results without state acceptance."""

import hashlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import cli, codec, mcp, service
from tests.test_consumer_execution import execution_fixture


class ConsumerSurfaceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.state, self.config = execution_fixture(self.root)
        self.initial = self.state.read_bytes()
        self.missing = str(self.root / "missing-node.exe")

    def arguments(self, out="work/execute"):
        return {"path": self.state.relative_to(self.root).as_posix(), "candidate_id": "package",
                "config": self.config, "out": out, "node": self.missing}

    def test_mcp_export_and_closed_schema_keep_execution_tier_explicit(self):
        listing = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, self.root)
        tool = next(t for t in listing["result"]["tools"] if t["name"] == "pixl_consumer_execute")
        self.assertFalse(tool["annotations"]["readOnlyHint"])
        self.assertFalse(tool["inputSchema"]["properties"]["config"]["additionalProperties"])
        reply = mcp.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
            "name": "pixl_consumer_execute", "arguments": {**self.arguments(), "result_path": "work/export.json"}}}, self.root)
        self.assertFalse(reply["result"].get("isError"), reply)
        summary = reply["result"]["structuredContent"]
        raw = (self.root / summary["result_path"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), summary["result_sha256"])
        saved = json.loads(raw)
        self.assertEqual(saved["status"], "unavailable")
        self.assertEqual(saved["hash_domains"]["binding_hash"], "candidate_bindings_sha256")
        for key in ("renderer_executed", "automatic_acceptance", "state_changed"):
            self.assertIs(saved[key], False)
        self.assertEqual(len(json.loads((self.root / "work/execute/renderer-sources.json").read_bytes())), 6)
        self.assertEqual(self.state.read_bytes(), self.initial)

    def test_cli_unavailable_is_nonzero_with_retained_json_and_cwd_relative_state(self):
        config = self.root / "config.json"
        config.write_text(json.dumps(self.config), encoding="utf-8")
        relative = os.path.relpath(self.state, Path.cwd())
        command = [sys.executable, "-m", "pixl", "consumer-execute", relative, "package", str(config),
                   "--out", "work/cli", "--root", str(self.root), "--node", self.missing,
                   "--result-path", "work/cli-export.json"]
        result = subprocess.run(command, capture_output=True, check=False, timeout=15)
        self.assertEqual(result.returncode, 1, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["status"], "unavailable")
        self.assertTrue(summary["result_saved"])
        self.assertEqual(self.state.read_bytes(), self.initial)
        self.assertTrue((self.root / "work/cli/result.json").is_file())

    def test_result_export_collision_refuses_before_execution(self):
        (self.root / "existing.json").write_bytes(b"keep")
        with patch("pixl.consumer_execution.execute") as execute:
            with self.assertRaises(codec.PixlError):
                service.call("pixl_consumer_execute", {**self.arguments(), "result_path": "existing.json"}, self.root)
            execute.assert_not_called()
        self.assertFalse((self.root / "work/execute").exists())
        self.assertEqual((self.root / "existing.json").read_bytes(), b"keep")

    def test_late_export_collision_retains_result_without_replay(self):
        result = service.call("pixl_consumer_execute", {**self.arguments(), "result_path": "work/execute/result.json"}, self.root)
        self.assertFalse(result["result_saved"])
        self.assertEqual(result["operation_result"]["status"], "unavailable")
        self.assertIn("Do not replay", result["recovery"]["detail"])
        self.assertEqual(self.state.read_bytes(), self.initial)

    def test_cli_complete_and_other_status_exit_codes(self):
        config = self.root / "config.json"
        config.write_text(json.dumps(self.config), encoding="utf-8")
        argv = ["consumer-execute", str(self.state), "package", str(config), "--out", "work/unused", "--root", str(self.root)]
        for status in ("complete", "failed", "partial", "timeout", "interrupted"):
            with self.subTest(status=status), patch("pixl.service.call", return_value={"status": status}), patch("pixl.cli.sys.stdout"):
                self.assertEqual(cli.main(argv), 0 if status == "complete" else 1)
