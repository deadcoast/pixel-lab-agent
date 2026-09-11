import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class MCPTests(unittest.TestCase):
    def test_real_stdio_initialize_tools_and_root_confined_validation(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.px"
            path.write_bytes(b"PX1 0\n@a:A{nm=~4:PIXL;rl=agent}\n")
            requests = [
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
                {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "pixl_validate", "arguments": {"path": "sample.px"}}},
                {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "pixl_validate", "arguments": {"path": "../outside.px"}}},
                {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "pixl_validate", "arguments": {"path": "sample.px", "invented": 1}}},
                {"jsonrpc": "2.0", "id": 6, "method": "missing"}]
            result = subprocess.run([sys.executable, "-m", "pixl", "mcp", "--root", tmp],
                                    input="".join(json.dumps(r) + "\n" for r in requests), capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            replies = [json.loads(line) for line in result.stdout.splitlines()]
            self.assertEqual(len(replies), 6)
            self.assertEqual(replies[0]["result"]["protocolVersion"], "2025-11-25")
            names = {t["name"] for t in replies[1]["result"]["tools"]}
            self.assertTrue({"pixl_context", "pixl_commit", "pixl_prepare", "pixl_job"} <= names)
            self.assertTrue(replies[2]["result"]["structuredContent"]["valid"])
            self.assertTrue(replies[3]["result"]["isError"])
            self.assertTrue(replies[4]["result"]["isError"])
            self.assertEqual(replies[5]["error"]["code"], -32601)

    def test_json_parse_failure_does_not_kill_next_request(self):
        result = subprocess.run([sys.executable, "-m", "pixl", "mcp", "--root", "."],
                                input='invalid\n{"jsonrpc":"2.0","id":8,"method":"ping"}\n',
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        replies = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(replies[0]["error"]["code"], -32700)
        self.assertEqual(replies[1], {"jsonrpc": "2.0", "id": 8, "result": {}})

    def test_unpaired_surrogate_error_does_not_kill_next_request(self):
        requests = [{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "\ud800", "arguments": {}}},
                    {"jsonrpc": "2.0", "id": 2, "method": "ping"}]
        result = subprocess.run([sys.executable, "-m", "pixl", "mcp", "--root", "."],
                                input="".join(json.dumps(r) + "\n" for r in requests), capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        replies = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertTrue(replies[0]["result"]["isError"])
        self.assertEqual(replies[1]["id"], 2)
