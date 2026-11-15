"""Actual CLI/MCP inspection and review publication from a saved fixture."""

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from pixl import codec, store
from tests.inspection_support import options, project


class InspectionOperationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / ".pixl"
        project(self.root)

    def cli(self, *args, error=False):
        result = subprocess.run(
            [sys.executable, "-m", "pixl", *map(str, args)],
            capture_output=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 2 if error else 0, result.stderr.decode())
        output = result.stderr if error else result.stdout
        self.assertTrue(output.lstrip().startswith(b"{"), output.decode())
        return json.loads(output)

    def rpc(self, method, params=None):
        request = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
        result = subprocess.run(
            [sys.executable, "-m", "pixl", "mcp", "--root", str(self.root)],
            input=json.dumps(request) + "\n",
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)["result"]

    def mcp(self, name, arguments, error=False):
        result = self.rpc("tools/call", {"name": name, "arguments": arguments})
        self.assertEqual(result["isError"], error, result)
        return result if error else result["structuredContent"]

    def expected(self):
        return codec.digest(store.load(self.folder))

    def prepare_args(self):
        return {
            "store": ".pixl",
            "expect": self.expected(),
            "candidate_id": "candidate",
            "packet_id": "packet",
            "options": options(),
        }

    def observation(self, views):
        return {
            "reviewer": "user",
            "observed_at": datetime.now(UTC).isoformat(),
            "observations": [
                {
                    "view": view["id"],
                    "delivered_size": None,
                    "note": "Controlled fixture declaration: supplied missing landmark.",
                }
                for view in views[:1]
            ],
            "verdicts": [
                {
                    "criterion": "q.mechanical",
                    "status": "pass",
                    "reason": "Fixture measurements satisfy the saved criterion.",
                    "supersedes": None,
                },
                {
                    "criterion": "q.visual",
                    "status": "fail",
                    "reason": "Fixture review: left antenna and right eye absent.",
                    "supersedes": None,
                },
                {
                    "criterion": "q.engine",
                    "status": "unavailable",
                    "reason": "No browser project exists in this fixture.",
                    "supersedes": None,
                },
            ],
            "next_action": "Retain a separate corrected candidate before its own review.",
            "limitations": [
                "Developer-supplied test observation; no model viewing or engine execution."
            ],
        }

    def assert_review(self):
        doc = store.load(self.folder)
        verdicts = [doc.records[ref.id] for ref in doc.records["task"].fields["vr"]]
        self.assertEqual(
            {v.fields["rq"].id: v.fields["st"].value for v in verdicts},
            {"q.mechanical": "pass", "q.visual": "fail", "q.engine": "unavailable"},
        )
        self.assertEqual(doc.records["task"].fields["st"].value, "open")
        self.assertEqual(doc.records["task"].fields["ca"], [codec.Ref("candidate")])
        self.assertEqual(len([r for r in doc.records.values() if r.kind == "E"]), 2)
        return doc

    def test_mcp_discovery_and_closed_mutation_envelopes(self):
        found = {row["name"]: row for row in self.rpc("tools/list")["tools"]}
        names = {"pixl_inspection", "pixl_inspection_prepare", "pixl_inspection_review"}
        self.assertTrue(names <= found.keys())
        for name in names:
            self.assertEqual(
                found[name]["annotations"]["readOnlyHint"], name == "pixl_inspection"
            )
            self.assertFalse(found[name]["annotations"]["openWorldHint"])
        before = self.expected()
        for bad in (
            {k: v for k, v in self.prepare_args().items() if k != "expect"},
            {**self.prepare_args(), "execute": True},
        ):
            response = self.mcp("pixl_inspection_prepare", bad, error=True)
            self.assertIn("inputSchema", response["content"][0]["text"])
        self.assertEqual(self.expected(), before)

    def test_cli_prepare_mcp_review_and_cold_reports(self):
        opts = self.root / "options.json"
        opts.write_text(json.dumps(options()), encoding="utf-8")
        before = store.load(self.folder)
        prepared = self.cli(
            "inspection-prepare",
            self.folder,
            "candidate",
            "packet",
            opts,
            "--expect",
            self.expected(),
            "--root",
            self.root,
        )
        self.assertEqual(
            store.load(self.folder).records["task"], before.records["task"]
        )
        self.assertTrue(prepared["measurements"]["candidate"]["pass"])
        result = self.mcp(
            "pixl_inspection_review",
            {
                "store": ".pixl",
                "expect": self.expected(),
                "packet_id": "packet",
                "review_id": "review",
                "observation": self.observation(prepared["views"]),
            },
        )
        self.assert_review()
        cold = self.cli(
            "inspection", self.folder / "state.px", "packet", "--root", self.root
        )
        self.assertEqual(cold["hash"], result["hash"])
        self.assertEqual(len(cold["packets"][0]["reviews"]), 1)
        mcp_cold = self.mcp(
            "pixl_inspection", {"path": ".pixl/state.px", "packet_id": "packet"}
        )
        self.assertEqual(cold, mcp_cold)

    def test_mcp_prepare_cli_review_stale_retry_cannot_duplicate(self):
        prepared = self.mcp("pixl_inspection_prepare", self.prepare_args())
        observed = self.root / "review.json"
        observed.write_text(
            json.dumps(self.observation(prepared["views"])), encoding="utf-8"
        )
        expected = self.expected()
        self.cli(
            "inspection-review",
            self.folder,
            "packet",
            "review",
            observed,
            "--expect",
            expected,
            "--root",
            self.root,
        )
        final = self.assert_review()
        self.cli(
            "inspection-review",
            self.folder,
            "packet",
            "duplicate",
            observed,
            "--expect",
            expected,
            "--root",
            self.root,
            error=True,
        )
        self.assertEqual(self.expected(), codec.digest(final))

    def test_mcp_confines_paths_before_store_access(self):
        for name, args in (
            ("pixl_inspection", {"path": "../outside.px"}),
            ("pixl_inspection_prepare", {**self.prepare_args(), "store": "../outside"}),
        ):
            response = self.mcp(name, args, error=True)
            self.assertIn("path_escape", response["content"][0]["text"])

    def test_cli_rejects_nonfinite_json_before_mutation(self):
        invalid = self.root / "invalid.json"
        invalid.write_text('{"scale": NaN}', encoding="utf-8")
        before = self.expected()
        response = self.cli(
            "inspection-prepare",
            self.folder,
            "candidate",
            "packet",
            invalid,
            "--expect",
            before,
            "--root",
            self.root,
            error=True,
        )
        self.assertEqual(response["error"], "json_read")
        self.assertEqual(self.expected(), before)


if __name__ == "__main__":
    unittest.main()
