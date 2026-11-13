"""Host-spill adapters require exact native locators and independently retained bytes."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evaluations import claude_result_proofs as proofs
from evaluations.grade_caller_result import matching_calls, mcp_calls
from evaluations.grade_named_codex_role import rows
from evaluations.host_trials import write_json


class ClaudeResultProofTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="native host spill ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.attempt, self.archive = self.root / "attempt", self.root / "archive"
        self.journal = self.attempt / "native-transcripts/parent.jsonl"
        self.journal.parent.mkdir(parents=True)
        self.source = self.root / "host/session/tool-results/mcp-pixl-local-pixl_plar_read-123.txt"
        self.source.parent.mkdir(parents=True)
        self.body = {"hash": "a" * 64, "project": "Exact observed host body: é", "production": {"jobs": []}}
        self.source.write_bytes(json.dumps(self.body, ensure_ascii=False, indent=2).encode())
        text = self.source.read_bytes().decode()
        returned = f"Error: result ({len(text):,} characters) exceeds maximum allowed tokens. Output has been saved to {self.source}.\nFormat: JSON with schema: {{hash: string}}"
        native = [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "read-call", "name": "mcp__pixl-local__pixl_plar_read",
                    "input": {"asset_id": "asset", "path": "plar.txt"}}]}},
                  {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "read-call", "content": returned}]}}]
        self.journal.write_text("\n".join(json.dumps(row) for row in native) + "\n")
        write_json(self.attempt / "continuation.json", {"status": "finished", "session_id": "session"})

    def calls(self):
        return mcp_calls([rows(self.journal)])

    def test_exact_retained_body_binds_native_call_and_survives_host_cache_removal(self):
        manifest = proofs.retain(self.attempt, self.archive)
        self.assertEqual(len(manifest["bindings"]), 1)
        self.assertEqual(manifest["bindings"][0]["source"]["bytes"], self.source.stat().st_size)
        self.source.unlink()
        calls = proofs.bind_retained(self.calls(), "session", [self.archive])
        matched = matching_calls(calls, "pixl_plar_read", self.body, {"asset_id": "asset", "path": "plar.txt"})
        self.assertTrue(matched)
        self.assertIn("native_spill", matched[0])
        wrong = {**self.body, "hash": "b" * 64}
        self.assertFalse(matching_calls(calls, "pixl_plar_read", wrong))

    def test_missing_host_file_never_uses_a_caller_copy(self):
        self.source.unlink()
        write_json(self.attempt / "caller-result.json", self.body)
        with self.assertRaises(FileNotFoundError):
            proofs.retain(self.attempt, self.archive)
        self.assertFalse(self.archive.exists())

    def test_archive_native_journal_or_reported_length_drift_is_rejected(self):
        manifest = proofs.retain(self.attempt, self.archive)
        archived = Path(manifest["bindings"][0]["archive"]["path"])
        original = archived.read_bytes()
        archived.write_bytes(original + b" ")
        with self.assertRaisesRegex(ValueError, "bytes or source identity"):
            proofs.bind_retained(self.calls(), "session", [self.archive])
        archived.write_bytes(original)
        self.journal.write_text(self.journal.read_text() + "{}\n")
        with self.assertRaisesRegex(ValueError, "native journal changed"):
            proofs.bind_retained(self.calls(), "session", [self.archive])
        self.source.write_bytes(self.source.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "length differs"):
            proofs.retain(self.attempt, self.root / "second-archive")

    def test_other_call_session_or_arguments_cannot_borrow_archived_body(self):
        proofs.retain(self.attempt, self.archive)
        for field, value in (("call_id", "other"), ("arguments", {"asset_id": "other", "path": "plar.txt"})):
            calls = [{**self.calls()[0], field: value}]
            bound = proofs.bind_retained(calls, "session", [self.archive])
            self.assertFalse(matching_calls(bound, "pixl_plar_read", self.body))
        with self.assertRaisesRegex(ValueError, "different session"):
            proofs.bind_retained(self.calls(), "other", [self.archive])

    def test_locator_must_name_the_matching_tool_and_session_directory(self):
        call = self.calls()[0]
        self.assertIsNotNone(proofs.spill_locator(call, "session"))
        self.assertIsNone(proofs.spill_locator(call, "other"))
        self.assertIsNone(proofs.spill_locator({**call, "tool": "pixl_jobs"}, "session"))
        self.assertIsNone(proofs.spill_locator({**call, "result": "Report says " + call["result"]}, "session"))


if __name__ == "__main__":
    unittest.main()
