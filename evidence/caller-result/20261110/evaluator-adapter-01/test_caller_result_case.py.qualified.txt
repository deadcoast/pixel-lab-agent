"""Native evaluation rejects report-only proof and preserves independent fixture roots."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import caller_result_case as case
from evaluations.grade_caller_result import (
    bind_exports,
    child_identity,
    command_proofs,
    error_object,
    matching_calls,
    mcp_attempts,
    mcp_calls,
    prohibited_attempts,
    refresh_proofs,
    source_locator_errors,
)
from evaluations.host_trials import sha, write_json


class CallerResultNativeProofTests(unittest.TestCase):
    def test_rejected_dispatch_does_not_excuse_another_attempt_with_same_arguments(self):
        error = {"category": "uncertain_remote_result", "error": "job_history", "recovery": {}, "detail": "unknown"}
        def event(ident, status, result=None, file="parent"):
            return {"file": file, "line": 4, "payload": {"type": "item_completed", "item": {"type": "McpToolCall",
                "id": ident, "tool": "pixl_job_dispatch", "server": "pixl_unknown", "arguments": {"job_id": "member.job"},
                "status": status, "result": result}}}
        first = event("first", "failed", {"isError": True, "structuredContent": error})
        second = event("second", "in_progress")
        self.assertEqual(prohibited_attempts([[first]]), [])
        self.assertEqual([c["call_id"] for c in prohibited_attempts([[first, second]])], ["second"])
        self.assertTrue(prohibited_attempts([[first, event("first", "in_progress", file="other")]]))

    def test_typed_native_child_identity_is_not_role_self_description(self):
        self.assertEqual(child_identity({"agent_type": "pixl", "canonical_task": "/root/specialist", "fork_turns": "none"}), "/root/specialist")
        self.assertIsNone(child_identity({"agent_type": "default", "canonical_task": "/root/specialist"}))
        self.assertIsNone(child_identity({"agent_type": "pixl"}))

    def test_failed_native_mcp_return_retains_real_diagnostic(self):
        error = {"error": "job_history", "category": "uncertain_remote_result", "detail": "dispatch refused", "recovery": {"action": "reconcile_existing_job"}}
        row = {"file": "parent", "line": 4, "payload": {"type": "item_completed", "item": {
            "type": "McpToolCall", "server": "pixl_unknown", "tool": "pixl_job_dispatch", "status": "failed",
            "arguments": {"job_id": "member.job"}, "result": {"isError": True, "structuredContent": error}}}}
        self.assertTrue(matching_calls(mcp_calls([[row]]), "pixl_job_dispatch", error, server="pixl_unknown"))
        row["payload"]["item"]["result"] = None
        self.assertFalse(matching_calls(mcp_calls([[row]]), "pixl_job_dispatch", error, server="pixl_unknown"))

    def test_truncated_refresh_requires_whole_anchored_continuation_not_hash_text(self):
        continuation = {"state_hash": "a" * 64, "requirements_hash": "b" * 64, "action": "delivered", "jobs": []}
        saved = {"production": {"continuation": continuation}, "requirements_hash": "b" * 64}
        tail = ('"continuation":' + json.dumps(continuation) + ',"link_action":null},"hash_domains":'
                '{"production.continuation.state_hash":"canonical_state_sha256","requirements_hash":"selected_requirements_sha256"}},"isError":false}')
        text = '{"content":[{"text":"partial…1000 chars truncated…' + tail
        call = {"tool": "pixl_plar_read", "server": "pixl_local", "arguments": {"asset_id": "queue.working"},
                "result": {"content": [{"text": text}]}, "file": "parent", "line": 10}
        proof = refresh_proofs([call], saved, {"asset_id": "queue.working"})
        self.assertTrue(proof[0]["native_full_result_truncated"])
        altered = {"production": {"continuation": {**continuation, "action": "dispatch"}}, "requirements_hash": "b" * 64}
        self.assertFalse(refresh_proofs([call], altered, {"asset_id": "queue.working"}))
        self.assertFalse(refresh_proofs([call], saved, {"asset_id": "another"}))
        call["result"]["content"][0]["text"] = text[:-1]
        self.assertFalse(refresh_proofs([call], saved, {"asset_id": "queue.working"}))

    def test_report_text_cannot_establish_parent_tool_execution(self):
        saved = {"requirements_hash": "a" * 64}
        journal = [{"message": {"content": [{"type": "text", "text": json.dumps(saved)}]}}]
        self.assertEqual(matching_calls(mcp_calls([journal]), "pixl_plar_read", saved), [])

    def test_exact_native_arguments_and_correct_server_required(self):
        saved = {"text": "exact source", "sha256": "a" * 64}
        args = {"path": ".pixl/handoffs/a.json", "expect": "a" * 64, "start": 4, "end": 8}
        journal = [{"file": "parent.jsonl", "line": 5, "payload": {"type": "item_completed", "item": {
            "type": "McpToolCall", "server": "pixl_local", "tool": "pixl_source", "status": "completed",
            "arguments": args, "result": {"isError": False, "structuredContent": saved}}}}]
        calls = mcp_calls([journal])
        self.assertTrue(matching_calls(calls, "pixl_source", saved, args))
        self.assertFalse(matching_calls(calls, "pixl_source", saved, {**args, "start": 1}))
        self.assertFalse(matching_calls(calls, "pixl_source", saved, args, "pixl_unknown"))

    def test_actual_claude_unknown_error_is_bound_to_its_tool_result(self):
        error = {"error": "job_state", "detail": "already unknown", "category": "uncertain_remote_result", "recovery": {"action": "reconcile_existing_job"}}
        journal = [{"line": 1, "file": "parent", "message": {"content": [{"type": "tool_use", "id": "call",
            "name": "mcp__pixl-unknown__pixl_job_dispatch", "input": {"job_id": "member.job"}}]}},
            {"line": 2, "file": "parent", "message": {"content": [{"type": "tool_result", "tool_use_id": "call", "is_error": True,
              "content": [{"type": "text", "text": json.dumps(error)}]}]}}]
        self.assertEqual(error_object(error), error)
        self.assertTrue(matching_calls(mcp_calls([journal]), "pixl_job_dispatch", error, server="pixl_unknown"))
        journal[1]["message"]["content"][0]["tool_use_id"] = "unrelated"
        self.assertFalse(mcp_calls([journal]))

    def test_provider_attempts_are_visible_even_without_completed_result(self):
        codex = [{"file": "child", "line": 1, "payload": {"type": "item_started", "item": {
            "type": "McpToolCall", "server": "pixellab", "tool": "create_image", "status": "in_progress"}}}]
        claude = [{"file": "child", "line": 2, "message": {"content": [{"type": "tool_use", "id": "remote",
            "name": "mcp__pixellab__create_image", "input": {}}]}}]
        self.assertEqual([c["server"] for c in mcp_attempts([codex, claude])], ["pixellab", "pixellab"])
        self.assertEqual(mcp_calls([codex, claude]), [])

    def test_receipt_default_is_the_same_public_view(self):
        saved = {"path": ".pixl/handoffs/a.json", "sha256": "a" * 64}
        call = {"tool": "pixl_plar_handoff", "server": "pixl_local", "arguments": {}, "result": saved, "file": "parent", "line": 1}
        self.assertTrue(matching_calls([call], "pixl_plar_handoff", saved, {"view": "receipt"}))
        self.assertFalse(matching_calls([call], "pixl_plar_handoff", saved, {"view": "caller"}))

    def test_exact_locator_slice_preserves_trailing_member_comma_and_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "handoff.json"
            path.write_bytes(b'{\n  "details": {"status":"partial"},\n  "next":"delivered"\n}\n')
            text = '  "details": {"status":"partial"},\n'
            locator = {"path": "handoff.json", "sha256": sha(path), "start": 2, "end": 2, "bytes": len(text.encode())}
            saved = {"text": text, "sha256": sha(path), "start": 2, "end": 2}
            self.assertEqual(source_locator_errors(root, locator, saved), [])
            self.assertTrue(source_locator_errors(root, locator, {**saved, "text": text.replace(",", "")}))
            path.write_bytes(path.read_bytes() + b" ")
            self.assertTrue(source_locator_errors(root, locator, saved))

    def test_export_receipt_binds_exact_saved_bytes_not_report_assertion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_json(root / "actual.json", {"observed": "real"})
            saved = {"observed": "real"}
            call = {"tool": "pixl_plar_read", "server": "pixl_local", "file": "parent", "line": 1,
                    "arguments": {"result_path": "actual.json"}, "result": {"structuredContent": {
                        "result_path": "actual.json", "result_sha256": sha(root / "actual.json")}}}
            self.assertTrue(matching_calls(bind_exports([call], root), "pixl_plar_read", saved))
            write_json(root / "actual.json", {"observed": "forged"})
            self.assertFalse(matching_calls(bind_exports([call], root), "pixl_plar_read", {"observed": "forged"}))

    def test_direct_protocol_proof_requires_actual_completed_native_command(self):
        response = {"id": 2, "result": {"isError": True}}
        row = {"line": 9, "file": "parent", "payload": {"type": "item_completed", "item": {"type": "CommandExecution",
            "command": "python missing_capability_probe.py", "exit_code": 0, "aggregated_output": json.dumps({"protocol_response": response})}}}
        self.assertTrue(command_proofs([row], "missing_capability_probe.py", response))
        row["payload"]["item"]["exit_code"] = 1
        self.assertFalse(command_proofs([row], "missing_capability_probe.py", response))


class CallerResultPreparationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="compact caller test ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source, self.unknown = self.root / "accepted", self.root / "unknown"
        for base, files in ((self.source, {".pixl/assets/queue.ready/state.px": "accepted original", "AGENTS.md": "old entrypoint",
                                         "BRIEF.md": "original brief", "work/artistic-revision/SPECIALIST-RESULT.json": "{}"}),
                            (self.unknown, {".pixl/state.px": "controlled unknown", "source.txt": "fixture"})):
            for name, text in files.items():
                p = base / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text, encoding="utf-8")

    def fake_prepare(self, destination, host, setup, python, *, package, consumer):
        destination.mkdir()
        consumer.mkdir()
        write_json(destination / "identity.json", {"inputs": {}, "package_files": {}})
        write_json(destination / "launch.json", {"host": host, "cwd": str(consumer), "command": ["codex", "-"]})
        (consumer / "AGENTS.md").write_text("new evaluation entrypoint")
        return consumer

    def prepare(self):
        destination, consumer = self.root / "attempt", self.root / "consumer"
        selected = {"requirements_hash": "a" * 64, "production": {"continuation": {"state_hash": "b" * 64}}}
        with patch.object(case.readiness_case, "prepare", side_effect=self.fake_prepare), patch.object(
                case.subprocess, "check_output", return_value=json.dumps(selected)):
            case.prepare(destination, "codex", Path("python.exe"), consumer=consumer, source=self.source, unknown_source=self.unknown)
        return destination, consumer

    def test_sources_preserved_unknown_separate_and_native_roots_explicit(self):
        destination, consumer = self.prepare()
        identity = json.loads((destination / "identity.json").read_bytes())
        self.assertEqual((consumer / "BRIEF.md").read_text(), "original brief")
        self.assertEqual((consumer / case.UNKNOWN / ".pixl/state.px").read_text(), "controlled unknown")
        self.assertEqual((self.source / "AGENTS.md").read_text(), "old entrypoint")
        self.assertNotIn("AGENTS.md", identity["original_inputs"])
        self.assertEqual(identity["fixtures"]["unknown"]["root"], str(consumer / case.UNKNOWN))
        command = json.loads((destination / "launch.json").read_bytes())["command"]
        self.assertTrue(any(v.startswith("mcp_servers.pixl_unknown.args=") and str(consumer / case.UNKNOWN).replace("\\", "\\\\") in v for v in command))
        probe = (consumer / case.INPUTS / "missing_capability_probe.py").read_text()
        compile(probe, "probe", "exec")
        self.assertLess(probe.index("if out.exists()"), probe.index("subprocess.run"))
        self.assertIn('out.open("xb"', probe)

    def test_retention_cannot_overwrite_prior_receipt(self):
        destination, consumer = self.prepare()
        write_json(consumer / case.WORK / "CALLER-RESULT.json", {"status": "partial"})
        case.retain(destination)
        with self.assertRaisesRegex(ValueError, "Preserve"):
            case.retain(destination)


if __name__ == "__main__":
    unittest.main()
