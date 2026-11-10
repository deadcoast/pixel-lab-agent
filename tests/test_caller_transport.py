"""Public caller views retain actionable identities across CLI, MCP and export."""

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import mcp, service
from tests.test_plar_prepare import seed, write


class CallerTransportTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "consumer"
        args, _, _, _ = seed(self.root)
        prepared = service.call("pixl_plar_prepare", args, self.root)
        self.inputs = {"asset_id": args["asset_id"], "requirements_hash": args["requirements_hash"],
                       "expect": prepared["hash"], "view": "caller",
                       "details": {"status": "partial", "caller": {
                           "summary": "The saved request still needs an observed result.",
                           "integration": {"status": "unavailable", "summary": "No engine observation supplied."}}}}
        write(self.root, "details.json", self.inputs["details"])

    def cli(self, *extra):
        return subprocess.run([sys.executable, "-B", "-m", "pixl", "plar", "handoff",
                               str(self.root / "details.json"), "--root", str(self.root),
                               "--asset", self.inputs["asset_id"], "--requirements", self.inputs["requirements_hash"],
                               "--expect", self.inputs["expect"], "--view", "caller", *extra],
                              capture_output=True, text=True, check=False)

    def mcp(self, args):
        return mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                             "params": {"name": "pixl_plar_handoff", "arguments": args}}, self.root)["result"]

    def test_cli_mcp_and_export_preserve_caller_and_exact_saved_bytes(self):
        direct = self.mcp(self.inputs)
        self.assertFalse(direct["isError"])
        result = direct["structuredContent"]
        cli = self.cli()
        self.assertEqual(cli.returncode, 0, cli.stderr)
        self.assertEqual(json.loads(cli.stdout), result)
        exported = self.mcp({**self.inputs, "result_path": "work/caller.json"})["structuredContent"]
        for key, value in result.items():
            if key != "hash_domains":
                self.assertEqual(exported[key], value, key)
        raw = (self.root / exported["result_path"]).read_bytes()
        self.assertEqual(json.loads(raw), result)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), exported["result_sha256"])
        self.assertEqual(exported["hash_domains"]["sha256"], "file_sha256")
        self.assertEqual(exported["hash_domains"]["requirements_hash"], "selected_requirements_sha256")
        self.assertEqual(result["assignment"]["status"], "partial")
        self.assertEqual(result["caller"]["integration"]["status"], "unavailable")

    def test_cli_mcp_stale_identity_is_actionable_without_publication(self):
        expected = self.inputs["expect"]
        self.inputs["expect"] = "0" * 64
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        cli = self.cli()
        self.assertEqual(cli.returncode, 2)
        cli_error = json.loads(cli.stderr)
        response = self.mcp(self.inputs)
        self.assertTrue(response["isError"])
        error = response["structuredContent"]
        self.assertEqual(json.loads(response["content"][0]["text"]), error)
        self.assertEqual(cli_error["category"], error["category"])
        self.assertEqual(error["category"], "stale_local_state")
        self.assertEqual(error["error"], "handoff_stale")
        self.assertEqual(error["identity"]["asset_id"], self.inputs["asset_id"])
        self.assertNotEqual(expected, self.inputs["expect"])
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_invalid_schema_is_sanitized_and_mcp_remains_usable(self):
        response = self.mcp({**self.inputs, "secret_unsupported": "do-not-echo-this-value"})
        self.assertTrue(response["isError"])
        self.assertEqual(response["structuredContent"]["category"], "invalid_authoring")
        self.assertNotIn("do-not-echo-this-value", json.dumps(response))
        self.assertFalse(self.mcp(self.inputs)["isError"])

    def test_malformed_tool_name_is_authoring_error_without_echoing_payload(self):
        for name in [{"key": "do-not-echo-this-value"}, ["do-not-echo-this-value"], "do-not-echo-this-value" * 20]:
            with self.subTest(shape=type(name).__name__):
                response = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                         "params": {"name": name, "arguments": {}}}, self.root)["result"]
                self.assertTrue(response["isError"])
                self.assertEqual(response["structuredContent"]["category"], "invalid_authoring")
                self.assertNotIn("do-not-echo-this-value", json.dumps(response))
        self.assertFalse(self.mcp(self.inputs)["isError"])


if __name__ == "__main__":
    unittest.main()
