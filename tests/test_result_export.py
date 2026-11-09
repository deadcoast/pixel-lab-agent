"""Exact result export removes model JSON transcription and preserves mutations."""

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, mcp, service, store
from pixl.codec import PixlError
from tests.family_support import family


class ResultExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / ".pixl"
        family(self.root, self.folder)

    def expected(self):
        return codec.digest(store.load(self.folder))

    def args(self):
        return {"store": ".pixl", "expect": self.expected(), "output_id": "delivery.output",
                "candidate_id": "package", "result_path": "work/snapshot.json"}

    def test_mutating_mcp_call_saves_exact_valid_json_and_compact_identity(self):
        response = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                 "params": {"name": "pixl_family_snapshot", "arguments": self.args()}}, self.root)
        self.assertFalse(response["result"].get("isError"), response)
        summary = response["result"]["structuredContent"]
        data = (self.root / summary["result_path"]).read_bytes()
        saved = json.loads(data)
        self.assertTrue(summary["result_saved"])
        self.assertEqual(hashlib.sha256(data).hexdigest(), summary["result_sha256"])
        self.assertEqual(saved["hash"], self.expected())
        self.assertEqual(saved["state"], str(self.folder / "state.px"))
        self.assertNotIn("manifest", summary)
        self.assertTrue((self.root / saved["manifest"]).is_file())

    def test_collision_or_path_escape_rejected_before_state_change(self):
        (self.root / "existing.json").write_text("preserve")
        before = self.expected()
        for path in ["existing.json", "../outside.json", ".pixl/state.px"]:
            with self.subTest(path=path), self.assertRaises(PixlError):
                service.call("pixl_family_snapshot", {**self.args(), "result_path": path}, self.root)
            self.assertEqual(before, self.expected())
        self.assertEqual((self.root / "existing.json").read_text(), "preserve")

    def test_post_publication_export_failure_returns_published_result(self):
        real_open = Path.open
        with patch.object(Path, "open", autospec=True) as opened:
            # Inject only the export failure; all store and observation I/O stays real.
            opened.side_effect = lambda path, *a, **kw: (_ for _ in ()).throw(OSError("export unavailable")) if str(path).endswith("snapshot.json") and a and a[0] == "xb" else real_open(path, *a, **kw)
            result = service.call("pixl_family_snapshot", self.args(), self.root)
        self.assertFalse(result["result_saved"])
        self.assertEqual(result["operation_result"]["hash"], self.expected())
        self.assertIn("package", store.load(self.folder).records)

    def test_cli_result_file_and_default_wire_context(self):
        args = [sys.executable, "-m", "pixl", "context", str(self.folder / "state.px"), "delivery.task", "--root", str(self.root)]
        baseline = subprocess.run(args, capture_output=True, check=False)
        exported = subprocess.run(args + ["--result-path", "work/context.px"], capture_output=True, check=False)
        self.assertEqual(exported.returncode, 0, exported.stderr)
        summary = json.loads(exported.stdout)
        self.assertEqual((self.root / summary["result_path"]).read_bytes(), baseline.stdout)
        self.assertEqual(summary["media_type"], "text/plain")

    def test_explicit_root_required_before_cli_mutation_and_metadata_matches(self):
        args = [sys.executable, "-m", "pixl", "family-snapshot", str(self.folder), "delivery.output", "package",
                "--expect", self.expected(), "--result-path", "snapshot.json"]
        before = self.expected()
        result = subprocess.run(args, capture_output=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(before, self.expected())
        tools = mcp.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, self.root)["result"]["tools"]
        for item in tools:
            if item["name"] in service.RESULT_EXPORT_TOOLS:
                self.assertIn("result_path", item["inputSchema"]["properties"])
                self.assertFalse(item["annotations"]["readOnlyHint"])


if __name__ == "__main__":
    unittest.main()
