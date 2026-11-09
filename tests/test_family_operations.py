"""Real local CLI/MCP family operations; fixture claims are never art acceptance."""

import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import codec, service, store
from tests.family_support import family
from tests.lifecycle_support import add_verdict


class FamilyOperationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / ".pixl"

    def cli(self, *args, expected_code=0):
        result = subprocess.run(
            [sys.executable, "-m", "pixl", *map(str, args)],
            capture_output=True,
            check=False,
            timeout=20,
        )
        self.assertEqual(result.returncode, expected_code, result.stderr.decode())
        output = result.stdout if expected_code == 0 else result.stderr
        self.assertTrue(output.lstrip().startswith(b"{"), output.decode())
        return json.loads(output)

    def rpc(self, method, params=None):
        request = {"jsonrpc": "2.0", "id": 1, "method": method}
        if params is not None:
            request["params"] = params
        result = subprocess.run(
            [sys.executable, "-m", "pixl", "mcp", "--root", str(self.root)],
            input=json.dumps(request) + "\n",
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)["result"]

    def mcp(self, name, arguments, error=False):
        result = self.rpc("tools/call", {"name": name, "arguments": arguments})
        self.assertEqual(result["isError"], error, result)
        return result if error else result["structuredContent"]

    def expected(self):
        return codec.digest(store.load(self.folder))

    def publish(self, doc):
        previous = store.load(self.folder)
        doc.revision = previous.revision + 1
        return store.commit(self.folder, doc, codec.digest(previous), self.root)

    def mutation(self, **extra):
        return {
            "store": ".pixl",
            "output_id": "delivery.output",
            "candidate_id": "package",
            "expect": self.expected(),
            **extra,
        }

    def assert_retained_without_acceptance(self, before, result):
        self.assertFalse(result["accepted"])
        self.assertFalse(result["remote_executed"])
        doc = store.load(self.folder)
        self.assertEqual(doc.revision, before.revision + 1)
        self.assertEqual(set(doc.records) - set(before.records), {"package"})
        self.assertEqual(doc.records["delivery.task"], before.records["delivery.task"])
        self.assertEqual(
            doc.records["package"].fields["of"], codec.Ref("delivery.output")
        )
        self.assertEqual(
            doc.records["package"].fields["xs"],
            [codec.Ref("sample"), codec.Ref("sample"), codec.Ref("member")],
        )
        manifest_path = self.root / doc.records["package"].fields["ur"]
        manifest = json.loads(manifest_path.read_bytes())
        self.assertEqual(manifest["source_state_sha256"], codec.digest(before))
        self.assertEqual(
            [(row["output"], row["candidate"]) for row in manifest["files"]],
            [("output", "sample"), ("member.output", "member")],
        )
        for row in manifest["files"]:
            copied = manifest_path.parent / row["path"]
            original = self.root / before.records[row["candidate"]].fields["ur"]
            self.assertNotEqual(copied, original)
            self.assertEqual(copied.read_bytes(), original.read_bytes())
        self.assertEqual(manifest_path.parent, self.root / result["package"])
        return doc

    def test_cli_family_routes_missing_state_to_structured_error(self):
        result = self.cli(
            "family",
            self.folder / "state.px",
            "--root",
            self.root,
            expected_code=2,
        )
        self.assertEqual(result["error"], "file_read")

    def test_cli_snapshot_routes_missing_store_to_structured_error(self):
        result = self.cli(
            "family-snapshot",
            self.folder,
            "delivery.output",
            "package",
            "--expect",
            "0" * 64,
            "--root",
            self.root,
            expected_code=2,
        )
        self.assertIn("error", result)

    def test_mcp_mutability_and_schema_reject_unchecked_mutations(self):
        by_name = {tool["name"]: tool for tool in self.rpc("tools/list")["tools"]}
        self.assertTrue({"pixl_family", "pixl_family_snapshot"} <= by_name.keys())
        # Default queries remain read-only, but optional result_path writes a file.
        self.assertFalse(by_name["pixl_family"]["annotations"]["readOnlyHint"])
        self.assertFalse(by_name["pixl_family_snapshot"]["annotations"]["readOnlyHint"])
        for name in ("pixl_family", "pixl_family_snapshot"):
            self.assertFalse(by_name[name]["annotations"]["openWorldHint"])
            self.assertFalse(by_name[name]["annotations"]["destructiveHint"])
        args = {
            "store": ".pixl",
            "output_id": "delivery.output",
            "candidate_id": "package",
        }
        for invalid in (args, {**args, "expect": "0" * 64, "execute": True}):
            result = self.mcp("pixl_family_snapshot", invalid, error=True)
            self.assertIn("inputSchema", result["content"][0]["text"])
        self.assertFalse(self.folder.exists())

    def test_mcp_family_paths_are_confined_before_read_or_write(self):
        report = self.mcp("pixl_family", {"path": "../outside.px"}, error=True)
        self.assertIn("path_escape", report["content"][0]["text"])
        snapshot = self.mcp(
            "pixl_family_snapshot",
            {
                "store": "../outside",
                "output_id": "delivery.output",
                "candidate_id": "package",
                "expect": "0" * 64,
            },
            error=True,
        )
        self.assertIn("path_escape", snapshot["content"][0]["text"])
        self.assertFalse(self.folder.exists())

    def test_cli_family_report_requires_explicit_root(self):
        result = subprocess.run(
            [sys.executable, "-m", "pixl", "family", str(self.folder / "state.px")],
            capture_output=True,
            check=False,
            timeout=20,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"--root", result.stderr)

    def test_cli_snapshot_and_cold_report_retain_files_without_acceptance(self):
        before = family(self.root)
        initial = self.cli("family", self.folder / "state.px", "--root", self.root)
        self.assertEqual(initial["families"][0]["output"], "delivery.output")
        self.assertEqual(initial["families"][0]["snapshots"], [])
        result = self.cli(
            "family-snapshot",
            self.folder,
            "delivery.output",
            "package",
            "--expect",
            initial["hash"],
            "--root",
            self.root,
        )
        self.assert_retained_without_acceptance(before, result)
        unchanged = self.expected()
        cold = self.cli(
            "family",
            self.folder / "state.px",
            "delivery.output",
            "--root",
            self.root,
        )
        self.assertEqual(self.expected(), unchanged)
        self.assertTrue(cold["files_verified"])
        row = cold["families"][0]
        self.assertIsNone(row["candidate"])
        self.assertEqual(row["state"], "open")
        self.assertEqual(
            [item["candidate"] for item in row["members"]], ["sample", "member"]
        )
        self.assertEqual(row["snapshots"][0]["candidate"], "package")
        self.assertEqual(row["snapshots"][0]["stale"], [])
        self.assertFalse(row["snapshots"][0]["retention_is_acceptance"])
        self.assertEqual({q["status"] for q in row["requirements"]}, {"unperformed"})

    def test_mcp_snapshot_and_cold_report_preserve_unavailable_engine_boundary(self):
        before = family(self.root)
        result = self.mcp("pixl_family_snapshot", self.mutation())
        doc = self.assert_retained_without_acceptance(before, result)
        doc.records["delivery.task"].fields["ca"] = [codec.Ref("package")]
        doc.records["delivery.task"].fields["st"] = codec.Symbol("active")
        add_verdict(
            doc, self.root, "package", "q.continuity", "pass", "fixture.continuity"
        )
        add_verdict(
            doc,
            self.root,
            "package",
            "q.delivery.engine",
            "unavailable",
            "engine.unavailable",
        )
        doc.records["engine.unavailable"].fields["wy"] = (
            "Fixture target project unavailable. Import the retained PNGs into the named "
            "target project and execute its saved import checks before accepting delivery."
        )
        self.publish(doc)
        unchanged = self.expected()
        cold = self.mcp(
            "pixl_family", {"path": ".pixl/state.px", "output": "delivery.output"}
        )
        self.assertEqual(self.expected(), unchanged)
        row = cold["families"][0]
        self.assertEqual(row["candidate"], "package")
        self.assertEqual(row["state"], "active")
        self.assertEqual(
            {q["id"]: q["status"] for q in row["requirements"]},
            {"q.continuity": "pass", "q.delivery.engine": "unavailable"},
        )
        current = store.load(self.folder)
        self.assertEqual(current.records["engine.unavailable"].fields["ev"], [])
        complete = codec.Document(current.revision + 1, dict(current.records), format=2)
        complete.records["delivery.task"] = codec.Record(
            "delivery.task",
            "T",
            {**current.records["delivery.task"].fields, "st": codec.Symbol("done")},
        )
        candidate_path = self.root / "invalid-completion.px"
        candidate_path.write_bytes(codec.encode(complete))
        failure = self.mcp(
            "pixl_commit",
            {"store": ".pixl", "candidate": candidate_path.name, "expect": unchanged},
            error=True,
        )
        self.assertIn("completion", failure["content"][0]["text"])
        self.assertIn("q.delivery.engine is unavailable", failure["content"][0]["text"])
        self.assertEqual(self.expected(), unchanged)

    def test_cold_unknown_member_job_blocks_snapshot_without_repeating_dispatch(self):
        doc = family(self.root)
        doc.records["member.task"].fields["st"] = codec.Symbol("open")
        self.publish(doc)
        request = {
            "provider": "fictional-fixture",
            "tool": "generate_fixture",
            "arguments": {"description": "Local family adapter fixture"},
            "schema": {
                "type": "object",
                "properties": {"description": {"type": "string"}},
                "required": ["description"],
                "additionalProperties": False,
            },
            "discovery": {
                "source": "Fictional fixture tools/list",
                "observed_at": "2026-09-11T12:00:00+00:00",
                "evidence": {"fixture": True},
            },
            "authorization": {
                "scope": "Local adapter test only; no remote execution",
                "evidence": {"fixture": True},
            },
        }
        self.mcp(
            "pixl_job_prepare",
            {
                "store": ".pixl",
                "expect": self.expected(),
                "job_id": "member.job",
                "task_id": "member.task",
                "outputs": ["member.output"],
                **request,
            },
        )
        dispatch = self.mcp(
            "pixl_job_dispatch",
            {"store": ".pixl", "expect": self.expected(), "job_id": "member.job"},
        )
        self.assertFalse(dispatch["remote_executed"])
        unchanged = self.expected()
        cold = self.cli("family", self.folder / "state.px", "--root", self.root)
        row = cold["families"][0]
        self.assertEqual(
            row["pending_jobs"],
            [{"id": "member.job", "task": "member.task", "state": "unknown"}],
        )
        self.assertTrue(
            any("member.job" in reason for reason in row["snapshot_blockers"])
        )
        history = self.mcp("pixl_jobs", {"path": ".pixl/state.px"})
        self.assertEqual(history["jobs"][0]["next_action"], "reconcile")
        self.assertNotIn("dispatch_request", history)
        failed = self.cli(
            "family-snapshot",
            self.folder,
            "delivery.output",
            "package",
            "--expect",
            unchanged,
            "--root",
            self.root,
            expected_code=2,
        )
        self.assertEqual(failed["error"], "delivery_blocked")
        self.mcp("pixl_family_snapshot", self.mutation(), error=True)
        self.assertEqual(self.expected(), unchanged)
        self.assertNotIn("package", store.load(self.folder).records)

    def test_stale_snapshot_and_corrupted_copy_fail_through_public_operations(self):
        family(self.root)
        stale = self.expected()
        self.mcp("pixl_family_snapshot", self.mutation())
        unchanged = self.expected()
        failed = self.cli(
            "family-snapshot",
            self.folder,
            "delivery.output",
            "second.package",
            "--expect",
            stale,
            "--root",
            self.root,
            expected_code=2,
        )
        self.assertEqual(failed["error"], "stale_write")
        self.assertEqual(self.expected(), unchanged)
        report = service.family_report(
            self.folder / "state.px", self.root, "delivery.output"
        )
        snapshot = report["families"][0]["snapshots"][0]
        copied = (self.root / snapshot["manifest"]).parent / snapshot["files"][0][
            "path"
        ]
        copied.write_bytes(b"corrupted fixture copy")
        cli_failed = self.cli(
            "family", self.folder / "state.px", "--root", self.root, expected_code=2
        )
        self.assertEqual(cli_failed["error"], "delivery_file")
        mcp_failed = self.mcp("pixl_family", {"path": ".pixl/state.px"}, error=True)
        self.assertIn("delivery_file", mcp_failed["content"][0]["text"])
        self.assertEqual(self.expected(), unchanged)
