"""Exercise the real CLI and MCP boundaries without provider or state writes."""

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import service

ROOT = Path(__file__).resolve().parents[1]


class ReadinessSurfaceTests(unittest.TestCase):
    def test_bootstrap_reports_missing_dependencies_without_runtime_import(self):
        with TemporaryDirectory() as temporary:
            result = subprocess.run(
                [sys.executable, "-S", "-B", "-m", "pixl", "readiness", "--root", temporary,
                 "--installation", str(ROOT)], cwd=ROOT, capture_output=True, text=True, timeout=20, check=False,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)["dependencies"]["status"], "incomplete")
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_cli_service_and_real_mcp_share_read_only_report(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            observations = {"host": "codex", "observed_at": "2026-11-10T00:00:00Z",
                            "named_role": "unavailable",
                            "local_tools": {"names": ["pixl_readiness"], "complete_inventory": False},
                            "official_tools": {"names": [], "complete_inventory": False}}
            source = root / "observations.json"
            source.write_text(json.dumps(observations), encoding="utf-8")
            before = source.read_bytes()
            arguments = {"host": "codex", "installation": str(ROOT), "observations": observations}
            direct = service.call("pixl_readiness", arguments, root)
            cli = subprocess.run(
                [sys.executable, "-B", "-m", "pixl", "readiness", "--root", temporary,
                 "--host", "codex", "--installation", str(ROOT), "--observations", "observations.json"],
                cwd=ROOT, capture_output=True, text=True, timeout=20, check=False,
            )
            self.assertEqual(cli.returncode, 0, cli.stderr)
            self.assertEqual(json.loads(cli.stdout), direct)
            requests = [
                {"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                 "params": {"name": "pixl_readiness", "arguments": arguments}},
            ]
            process = subprocess.run(
                [sys.executable, "-B", "-m", "pixl", "mcp", "--root", temporary], cwd=ROOT,
                input="".join(json.dumps(item) + "\n" for item in requests),
                capture_output=True, text=True, timeout=20, check=False,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            replies = [json.loads(line) for line in process.stdout.splitlines()]
            tool = next(item for item in replies[0]["result"]["tools"] if item["name"] == "pixl_readiness")
            self.assertTrue(tool["annotations"]["readOnlyHint"])
            self.assertFalse(tool["annotations"]["openWorldHint"])
            self.assertEqual(replies[1]["result"]["structuredContent"], direct)
            self.assertEqual(direct["official_pixellab"]["visibility"]["status"], "not_observed")
            self.assertEqual(direct["official_pixellab"]["authentication"], "not_verified")
            self.assertEqual(direct["specialist"]["named_role"], "unavailable")
            self.assertEqual(source.read_bytes(), before)
            self.assertEqual([p.name for p in root.iterdir()], ["observations.json"])

    def test_mcp_rejects_configuration_payload_without_echoing_it(self):
        from pixl.mcp import dispatch

        with TemporaryDirectory() as temporary:
            secret = "fixture-credential-must-not-be-echoed"
            reply = dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
                "name": "pixl_readiness", "arguments": {"observations": {
                    "host": "claude", "observed_at": "2026-11-10T00:00:00Z", "Authorization": secret,
                }}}}, Path(temporary))
            self.assertTrue(reply["result"]["isError"])
            self.assertNotIn(secret, json.dumps(reply))
            self.assertEqual(list(Path(temporary).iterdir()), [])
