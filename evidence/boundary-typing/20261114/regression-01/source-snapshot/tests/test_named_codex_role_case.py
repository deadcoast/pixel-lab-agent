"""Preserved-baseline recovery and evidence rejection for named-role trials."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from evaluations import named_codex_role_case as case
from evaluations.grade_named_codex_role import (
    named_route_checks,
    own_rows,
    public_operation_proofs,
    trace_facts,
)
from evaluations.host_trials import inventory, sha, write_json


class NamedRoleBaselineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.consumer = self.root / "consumer"
        self.consumer.mkdir()
        self.manifest = self.root / "baseline.json"
        self.archive = self.root / "baseline.zip"
        self.data = b"retained state\n"
        self.digest = hashlib.sha256(self.data).hexdigest()

    def baseline(self, name=".pixl/assets/task/state.px"):
        with zipfile.ZipFile(self.archive, "w") as archive:
            archive.writestr(name, self.data)
        write_json(self.manifest, {"archive": self.archive.name, "sha256": sha(self.archive),
                                   "files": {name: self.digest}})
        return {"artifacts": {name: self.digest}}

    def test_missing_ignored_state_recovers_and_existing_sources_stay_unchanged(self):
        retained = self.baseline()
        source = self.consumer / "BRIEF.md"
        source.write_bytes(b"original intent\n")
        retained["artifacts"]["BRIEF.md"] = sha(source)
        with patch.object(case, "BASELINE", self.manifest):
            case.restore_inputs(self.consumer, retained)
            case.restore_inputs(self.consumer, retained)
        self.assertEqual((self.consumer / ".pixl/assets/task/state.px").read_bytes(), self.data)
        self.assertEqual(source.read_bytes(), b"original intent\n")

    def test_corrupt_archive_fails_before_recovery(self):
        retained = self.baseline()
        with self.archive.open("ab") as stream:
            stream.write(b"changed")
        with patch.object(case, "BASELINE", self.manifest), self.assertRaisesRegex(ValueError, "archive changed"):
            case.restore_inputs(self.consumer, retained)
        self.assertEqual(list(self.consumer.iterdir()), [])

    def test_recovery_preserves_conflicting_existing_bytes(self):
        retained = self.baseline()
        target = self.consumer / ".pixl/assets/task/state.px"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"newer state, never overwrite")
        with patch.object(case, "BASELINE", self.manifest), self.assertRaisesRegex(ValueError, "Existing baseline input changed"):
            case.restore_inputs(self.consumer, retained)
        self.assertEqual(target.read_bytes(), b"newer state, never overwrite")

    def test_archive_cannot_escape_consumer(self):
        retained = self.baseline("../outside.px")
        with patch.object(case, "BASELINE", self.manifest), self.assertRaisesRegex(ValueError, "escapes consumer"):
            case.restore_inputs(self.consumer, retained)
        self.assertFalse((self.root / "outside.px").exists())

    def test_retained_outputs_include_handoff_and_report_changed_or_removed_state(self):
        self.baseline()
        attempt = self.root / "attempt"
        attempt.mkdir()
        for name in (*case.ENTRYPOINTS, case.KIT + "/bundle-manifest.json", ".pixl/old.json", ".pixl/deleted.json"):
            path = self.consumer / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"baseline\n")
        write_json(attempt / "launch.json", {"cwd": str(self.consumer)})
        write_json(attempt / "identity.json", {"inputs": inventory(self.consumer)})
        (self.consumer / ".pixl/old.json").write_bytes(b"changed state to preserve as failed evidence\n")
        (self.consumer / ".pixl/deleted.json").unlink()
        handoff = self.consumer / ".pixl/handoffs/new.json"
        handoff.parent.mkdir()
        handoff.write_bytes(b'{"returned":"actual handoff bytes"}\n')
        work = self.consumer / case.WORK
        work.mkdir(parents=True)
        (work / "CALLER-RESULT.json").write_bytes(b'{"status":"partial"}\n')
        with patch.object(case, "BASELINE", self.manifest):
            case.retain_outputs(attempt)
        delta = json.loads((attempt / "consumer-delta.json").read_bytes())
        self.assertEqual(delta["changed_existing"], [".pixl/old.json"])
        self.assertEqual(delta["removed"], [".pixl/deleted.json"])
        with zipfile.ZipFile(attempt / "consumer-delta.zip") as archive:
            self.assertEqual(set(archive.namelist()), {".pixl/old.json", ".pixl/handoffs/new.json"})
            self.assertEqual(archive.read(".pixl/handoffs/new.json"), handoff.read_bytes())
            self.assertEqual(archive.read(".pixl/old.json"), (self.consumer / ".pixl/old.json").read_bytes())
        self.assertEqual((attempt / "outputs/CALLER-RESULT.json").read_bytes(), (work / "CALLER-RESULT.json").read_bytes())


def event(ordinal, payload, *, timestamp=None, kind="response_item"):
    return {"ordinal": ordinal, "line": ordinal + 1, "file": "fixture.jsonl", "type": kind,
            "timestamp": timestamp or f"2026-11-09T23:00:{ordinal:02d}Z", "payload": payload}


def native_journals(role="pixl", *, completed=True, inherited=False, delivered=True):
    parent = [event(0, {"id": "parent", "session_id": "parent", "source": "exec"}, kind="session_meta")]
    parent.append(event(1, {"type": "additional_tools", "tools": [{"name": "collaboration", "tools": [
        {"name": "spawn_agent", "description": "Available role: pixl", "parameters": {"properties": {"agent_type": {"type": "string"}}}}
    ]}]}))
    parent.append(event(2, {"type": "function_call", "namespace": "collaboration", "name": "spawn_agent",
                            "call_id": "spawn-1", "arguments": json.dumps({"agent_type": "pixl"})}))
    parent.append(event(8, {"type": "function_call", "namespace": "collaboration", "name": "followup_task",
                            "call_id": "follow-1", "arguments": json.dumps({"target": "pixl_child"}),
                            "internal_chat_message_metadata_passthrough": {"turn_id": "parent-turn"}}))
    if delivered:
        parent.append(event(8, {"type": "item_completed", "item": {"type": "SubAgentActivity", "id": "follow-1",
                              "kind": "interacted", "agent_thread_id": "child"}}, kind="event_msg"))
    parent.append(event(8, {"type": "function_call_output", "call_id": "follow-1", "is_error": not delivered}))
    developer = {"type": "message", "role": "developer", "content": [{"text": "Exact registered role instructions"}]}
    if inherited:
        parent.append(event(3, developer))
    child = [event(0, {"id": "child", "session_id": "parent", "cwd": "fixture",
                      "subagent_history_start_ordinal": 4,
                      "source": {"subagent": {"thread_spawn": {"parent_thread_id": "parent", "agent_path": "/root/pixl_child", "agent_role": role}}}},
                   kind="session_meta"), event(3, developer)]
    if completed:
        child += [event(9, {"type": "task_started", "turn_id": "round2", "turn_attribution": {"parent_turn_id": "parent-turn"}}, kind="event_msg"),
                  event(10, {"type": "item_completed", "turn_id": "round2", "item": {"type": "CommandExecution",
                            "command": ["write SPECIALIST-ROUND2.json"]}}, kind="event_msg"),
                  event(11, {"type": "task_complete", "turn_id": "round2"}, kind="event_msg")]
    return [parent, child]


class NamedRoleTraceTests(unittest.TestCase):
    def verdicts(self, **kwargs):
        facts = trace_facts(native_journals(**kwargs), "parent", "Exact registered role instructions")
        return {name: passed for name, passed, _ in named_route_checks(facts)}

    def test_generic_child_cannot_satisfy_named_role_even_when_requested(self):
        result = self.verdicts(role=None)
        self.assertTrue(result["one_explicit_pixl_spawn"])
        self.assertFalse(result["one_actual_named_child"])
        self.assertFalse(result["configured_role_instructions_loaded"])
        self.assertFalse(result["same_child_completed_after_followup"])

    def test_followup_call_without_later_child_work_is_not_completion(self):
        result = self.verdicts(completed=False)
        self.assertTrue(result["one_actual_named_child"])
        self.assertTrue(result["configured_role_instructions_loaded"])
        self.assertFalse(result["same_child_completed_after_followup"])

    def test_inherited_parent_text_is_not_role_injection(self):
        result = self.verdicts(inherited=True)
        self.assertTrue(result["one_actual_named_child"])
        self.assertFalse(result["configured_role_instructions_loaded"])

    def test_rejected_followup_does_not_count_existing_child_work(self):
        result = self.verdicts(delivered=False)
        self.assertTrue(result["one_actual_named_child"])
        self.assertFalse(result["same_child_completed_after_followup"])

    def test_named_role_injection_and_completed_followup_are_separate_proofs(self):
        self.assertTrue(all(self.verdicts().values()))

    def test_cold_child_requires_correlated_no_history_spawn(self):
        journals = native_journals()
        del journals[1][0]["payload"]["subagent_history_start_ordinal"]
        self.assertEqual(own_rows(journals[1], "parent"), [])
        journals[0][2]["payload"]["arguments"] = json.dumps({"agent_type": "pixl", "fork_turns": "none"})
        journals[0].append(event(2, {"type": "item_completed", "item": {"type": "SubAgentActivity", "id": "spawn-1",
                                                "kind": "spawned", "agent_thread_id": "child"}}, kind="event_msg"))
        journals[0].append(event(2, {"type": "function_call_output", "call_id": "spawn-1"}))
        facts = trace_facts(journals, "parent", "Exact registered role instructions")
        self.assertEqual(facts["cold_children"], ["child"])
        self.assertTrue({n: p for n, p, _ in named_route_checks(facts)}["same_child_completed_after_followup"])


class NamedRolePublicProofTests(unittest.TestCase):
    def test_replay_shaped_file_without_public_native_call_cannot_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            consumer = Path(directory)
            path = consumer / "work/named-role/copied-result.json"
            path.parent.mkdir(parents=True)
            write_json(path, {"candidate": "candidate", "review": "review", "reused_review": True, "publications": []})
            copied = event(1, {"type": "item_completed", "item": {"type": "CommandExecution", "exit_code": 0,
                                     "command": ["Copy-Item", "old.json", str(path)], "aggregated_output": ""}}, kind="event_msg")
            self.assertEqual(public_operation_proofs([copied], consumer, "candidate-review", ["candidate", "review"],
                             path.relative_to(consumer).as_posix(), sha(path)), [])

    def test_mcp_proof_requires_success_and_matching_result_identity(self):
        item = {"type": "McpToolCall", "server": "pixl_local", "tool": "pixl_review_context", "status": "completed",
                "arguments": {"candidate_id": "candidate", "result_path": "work/named-role/context.json"},
                "result": {"isError": False, "structuredContent": {"result_path": "work/named-role/context.json", "result_sha256": "a" * 64}}}
        observed = event(1, {"type": "item_completed", "item": item}, kind="event_msg")
        args = ([observed], Path.cwd(), "review-context", ["candidate"], "work/named-role/context.json", "a" * 64)
        self.assertEqual(len(public_operation_proofs(*args)), 1)
        item["result"]["isError"] = True
        self.assertEqual(public_operation_proofs(*args), [])
        item["result"]["isError"] = False
        item["result"]["structuredContent"]["result_sha256"] = "b" * 64
        self.assertEqual(public_operation_proofs(*args), [])


if __name__ == "__main__":
    unittest.main()
