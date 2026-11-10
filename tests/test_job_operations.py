"""Real local CLI/MCP recovery with fictional provider observations only."""

import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from pixl import codec, service, store
from tests.lifecycle_support import sample


class JobOperationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / ".pixl"
        store.initialize(self.folder, sample(self.root), self.root)
        self.request = {
            "provider": "fictional-fixture",
            "tool": "generate_fixture",
            "arguments": {"description": "Local adapter fixture"},
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
        self.request_path = self.root / "request.json"
        self.request_path.write_text(json.dumps(self.request), encoding="utf-8")
        self.evidence = {"fixture": "Caller-supplied synthetic observation"}
        self.evidence_path = self.root / "observation.json"
        self.evidence_path.write_text(json.dumps(self.evidence), encoding="utf-8")

    def expected(self):
        return codec.digest(store.load(self.folder))

    def cli(self, *args, expected_code=0):
        result = subprocess.run(
            [sys.executable, "-m", "pixl", *map(str, args)],
            capture_output=True,
            check=False,
            timeout=15,
        )
        self.assertEqual(result.returncode, expected_code, result.stderr.decode())
        output = result.stdout if expected_code == 0 else result.stderr
        self.assertTrue(output.lstrip().startswith(b"{"), output.decode())
        return json.loads(output)

    def prepare_cli(self, expected_code=0):
        return self.cli(
            "job-prepare",
            self.folder,
            "job",
            "task",
            self.request_path,
            "--outputs",
            "output",
            "--expect",
            self.expected(),
            "--root",
            self.root,
            expected_code=expected_code,
        )

    def rpc(self, requests):
        result = subprocess.run(
            [sys.executable, "-m", "pixl", "mcp", "--root", str(self.root)],
            input="".join(json.dumps(row) + "\n" for row in requests),
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return [json.loads(line)["result"] for line in result.stdout.splitlines()]

    def mcp(self, name, arguments, error=False):
        result = self.rpc(
            [
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": name, "arguments": arguments},
                }
            ]
        )[0]
        self.assertEqual(result["isError"], error, result)
        return result if error else result["structuredContent"]

    def mutation(self, **extra):
        return {"store": ".pixl", "expect": self.expected(), "job_id": "job", **extra}

    def assert_import_unaccepted(self):
        doc = store.load(self.folder)
        candidate = doc.records["candidate"]
        self.assertEqual(candidate.fields["of"], codec.Ref("output"))
        self.assertEqual(
            (self.root / candidate.fields["ur"]).read_bytes(),
            (self.root / "download.png").read_bytes(),
        )
        report = service.workflow(self.folder / "state.px", self.root)
        output = report["tasks"][0]["outputs"][0]
        self.assertIsNone(output["candidate"])
        self.assertEqual(
            {row["status"] for row in output["candidates"][0]["requirements"]},
            {"unperformed"},
        )
        self.assertEqual(doc.records["task"].fields["st"], codec.Symbol("open"))

    def test_cli_cold_recovery_preserves_unknown_then_imports_unaccepted_candidate(
        self,
    ):
        prepared = self.prepare_cli()
        self.assertEqual(prepared["job"]["state"], "prepared")
        self.assertNotIn("dispatch_request", prepared)
        dispatched = self.cli(
            "job-dispatch",
            self.folder,
            "job",
            "--expect",
            prepared["hash"],
            "--root",
            self.root,
        )
        self.assertEqual(
            dispatched["dispatch_request"]["arguments"], self.request["arguments"]
        )
        self.assertEqual(dispatched["job"]["state"], "unknown")
        self.assertFalse(dispatched["remote_executed"])
        cold = self.cli("jobs", self.folder / "state.px", "--root", self.root)
        self.assertEqual(cold["jobs"][0]["next_action"], "reconcile")
        self.assertNotIn("dispatch_request", cold)
        before = self.expected()
        self.cli(
            "job-dispatch",
            self.folder,
            "job",
            "--expect",
            before,
            "--root",
            self.root,
            expected_code=2,
        )
        self.assertEqual(self.expected(), before)
        for event, remote in [
            ("unknown", []),
            ("running", ["--remote-id", "fixture-id"]),
            ("succeeded", []),
        ]:
            observed = self.cli(
                "job-observe",
                self.folder,
                "job",
                event,
                self.evidence_path,
                "--expect",
                self.expected(),
                "--root",
                self.root,
                *remote,
            )
            self.assertEqual(observed["job"]["state"], event)
            self.assertFalse(observed["remote_executed"])
        Image.new("RGBA", (2, 2), "magenta").save(self.root / "download.png")
        imported = self.cli(
            "job-import",
            self.folder,
            "job",
            "output",
            "candidate",
            "download.png",
            self.evidence_path,
            "--expect",
            self.expected(),
            "--root",
            self.root,
        )
        self.assertEqual(imported["job"]["candidates"][0]["id"], "candidate")
        self.assertFalse(imported["remote_executed"])
        self.assert_import_unaccepted()

    def test_cli_request_json_requires_exact_shape_before_publication(self):
        before = self.expected()
        missing = deepcopy(self.request)
        del missing["discovery"]
        for request in [missing, {**self.request, "execute": True}, []]:
            with self.subTest(request=request):
                self.request_path.write_text(json.dumps(request), encoding="utf-8")
                result = self.prepare_cli(expected_code=2)
                self.assertEqual(result["error"], "job_request")
                self.assertEqual(self.expected(), before)

    def test_cli_cold_report_requires_explicit_root(self):
        result = subprocess.run(
            [sys.executable, "-m", "pixl", "jobs", str(self.folder / "state.px")],
            capture_output=True,
            check=False,
            timeout=15,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"--root", result.stderr)

    def test_mcp_cold_recovery_never_grants_repeat_dispatch_and_imports_locally(self):
        prepared = self.mcp(
            "pixl_job_prepare",
            self.mutation(task_id="task", outputs=["output"], **self.request),
        )
        self.assertEqual(prepared["job"]["state"], "prepared")
        self.assertNotIn("dispatch_request", prepared)
        dispatched = self.mcp("pixl_job_dispatch", self.mutation())
        self.assertEqual(
            dispatched["dispatch_request"]["arguments"], self.request["arguments"]
        )
        self.assertFalse(dispatched["remote_executed"])
        cold = self.mcp("pixl_jobs", {"path": ".pixl/state.px"})
        self.assertEqual(cold["jobs"][0]["state"], "unknown")
        self.assertEqual(cold["jobs"][0]["next_action"], "reconcile")
        self.assertEqual(
            cold["jobs"][0]["request"]["discovery"], self.request["discovery"]
        )
        self.assertNotIn("dispatch_request", cold)
        before = self.expected()
        failed = self.mcp("pixl_job_dispatch", self.mutation(), error=True)
        diagnostic = failed["structuredContent"]
        self.assertEqual(diagnostic["category"], "uncertain_remote_result")
        self.assertEqual(diagnostic["identity"]["job_id"], "job")
        self.assertEqual(diagnostic["identity"]["state_hash"], before)
        self.assertEqual(diagnostic["recovery"]["operation"], "pixl_jobs")
        self.assertNotIn("dispatch_request", diagnostic)
        self.assertEqual(self.expected(), before)
        self.mcp(
            "pixl_job_observe",
            self.mutation(event="unknown", evidence=self.evidence),
        )
        observed = self.mcp(
            "pixl_job_observe",
            self.mutation(
                event="succeeded", evidence=self.evidence, remote_id="fixture-id"
            ),
        )
        self.assertEqual(observed["job"]["remote_id"], "fixture-id")
        Image.new("RGBA", (2, 2), "magenta").save(self.root / "download.png")
        imported = self.mcp(
            "pixl_job_import",
            self.mutation(
                output_id="output",
                candidate_id="candidate",
                path="download.png",
                evidence=self.evidence,
            ),
        )
        self.assertEqual(imported["job"]["candidates"][0]["id"], "candidate")
        self.assertFalse(imported["remote_executed"])
        self.assert_import_unaccepted()

    def test_mcp_mutability_and_schema_reject_unchecked_mutations(self):
        listed = self.rpc([{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}])[0]
        by_name = {tool["name"]: tool for tool in listed["tools"]}
        mutators = {
            "pixl_job_prepare",
            "pixl_job_dispatch",
            "pixl_job_observe",
            "pixl_job_import",
        }
        self.assertTrue(mutators | {"pixl_jobs"} <= by_name.keys())
        for name in mutators:
            self.assertFalse(by_name[name]["annotations"]["readOnlyHint"])
            self.assertFalse(by_name[name]["annotations"]["openWorldHint"])
        self.assertTrue(by_name["pixl_jobs"]["annotations"]["readOnlyHint"])
        before = self.expected()
        valid = self.mutation(task_id="task", outputs=["output"], **self.request)
        missing = deepcopy(valid)
        del missing["expect"]
        for args in [missing, {**valid, "execute": True}, {**valid, "outputs": []}]:
            self.mcp("pixl_job_prepare", args, error=True)
            self.assertEqual(self.expected(), before)

    def test_mcp_schema_errors_do_not_echo_credential_values(self):
        before = self.expected()
        valid = self.mutation(task_id="task", outputs=["output"], **self.request)
        result = self.mcp(
            "pixl_job_prepare",
            {**valid, "authorization": "Bearer DO_NOT_ECHO"},
            error=True,
        )
        self.assertNotIn("DO_NOT_ECHO", json.dumps(result))
        self.assertIn("type", result["content"][0]["text"])
        self.assertEqual(self.expected(), before)

    def test_mcp_store_and_report_paths_stay_inside_configured_root(self):
        before = self.expected()
        actions = [
            (
                "pixl_job_prepare",
                self.mutation(task_id="task", outputs=["output"], **self.request),
            ),
            ("pixl_job_dispatch", self.mutation()),
            (
                "pixl_job_observe",
                self.mutation(event="unknown", evidence=self.evidence),
            ),
            (
                "pixl_job_import",
                self.mutation(
                    output_id="output",
                    candidate_id="candidate",
                    path="download.png",
                    evidence=self.evidence,
                ),
            ),
        ]
        for name, args in actions:
            with self.subTest(name=name):
                result = self.mcp(name, {**args, "store": "../outside"}, error=True)
                self.assertIn("path_escape", result["content"][0]["text"])
        result = self.mcp("pixl_jobs", {"path": "../outside/state.px"}, error=True)
        self.assertIn("path_escape", result["content"][0]["text"])
        self.assertEqual(self.expected(), before)


if __name__ == "__main__":
    unittest.main()
