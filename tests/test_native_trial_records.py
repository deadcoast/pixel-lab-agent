"""Native continuation records preserve interruptions without inventing host success."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import native_trial_records as records
from evaluations.host_trials import sha, write_json

SESSION = "12345678-1234-1234-1234-123456789abc"
CHILD = "a123456789"


class NativeTrialRecordTests(unittest.TestCase):
    def setup_attempt(self, root, disabled=False):
        attempt = root / "attempt"
        consumer = root / "consumer"
        attempt.mkdir()
        consumer.mkdir()
        launch = {"host": "claude", "case": "test", "cwd": str(consumer), "host_version": "fixture",
                  "command": ["claude", "--print", "--session-id", SESSION], "artifact_roots": ["work"]}
        if disabled:
            launch["command"].append("--no-session-persistence")
        write_json(attempt / "launch.json", launch)
        (attempt / "prompt.txt").write_text("Continue exact work", encoding="utf-8")
        return attempt, consumer, launch

    def event(self, attempt, value):
        with (attempt / "stdout.jsonl").open("ab") as stream:
            stream.write((json.dumps(value) + "\n").encode())

    def transcript(self, root):
        parent = root / "host/project" / (SESSION + ".jsonl")
        child = parent.with_suffix("") / "subagents" / ("agent-" + CHILD + ".jsonl")
        child.parent.mkdir(parents=True)
        parent.write_text("parent history", encoding="utf-8")
        child.write_text("child history", encoding="utf-8")
        return parent, child

    def test_incremental_stream_preserves_ids_and_partial_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, _, launch = self.setup_attempt(root)
            journal = records.AttemptRecord(attempt, launch, {}, host_root=root / "host")
            data = (json.dumps({"type": "system", "session_id": SESSION}, ensure_ascii=False) + "\n").encode()
            (attempt / "stdout.jsonl").write_bytes(data[:12])
            first = journal.snapshot()
            self.assertIsNone(first["session_id"])
            self.assertEqual(first["stream"]["partial_tail_bytes"], 12)
            with (attempt / "stdout.jsonl").open("ab") as stream:
                stream.write(data[12:])
            self.event(attempt, {"type": "assistant", "agent_id": CHILD, "session_id": SESSION,
                                "message": {"content": [{"type": "tool_use", "id": "send", "name": "SendMessage", "input": {"to": CHILD}}]}})
            self.event(attempt, {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "send", "is_error": True, "content": "No transcript found"}]}})
            final = journal.snapshot("finished", returncode=0)
            self.assertEqual(final["session_id"], SESSION)
            self.assertEqual(final["children"][0]["id"], CHILD)
            self.assertTrue(final["calls"][0]["transcript_missing"])
            self.assertEqual(final["interruption_reason"], "incomplete_stream")
            self.assertFalse(final["native_resume"]["available"])
            self.assertEqual(final["behavioral_verdict"], "ungraded")

    def test_usage_limit_and_disabled_persistence_remain_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, _, launch = self.setup_attempt(root, True)
            self.transcript(root)
            self.event(attempt, {"type": "result", "session_id": SESSION, "subtype": "success", "is_error": True,
                                "result": "You're out of usage credits"})
            result = records.AttemptRecord(attempt, launch, {}, host_root=root / "host").snapshot("finished", returncode=1)
            self.assertEqual(result["interruption_reason"], "usage_limit")
            self.assertFalse(result["native_resume"]["available"])
            self.assertEqual(result["persistence"]["configured"], "disabled")
            with self.assertRaisesRegex(ValueError, "artifact-based restart"):
                records.prepare_resume(attempt, root / "resume", "Continue", CHILD)
            self.assertFalse((root / "resume").exists())

    def test_native_resume_preserves_cwd_session_configuration_and_original_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, consumer, launch = self.setup_attempt(root)
            self.transcript(root)
            self.event(attempt, {"type": "assistant", "session_id": SESSION, "agent_id": CHILD})
            self.event(attempt, {"type": "result", "session_id": SESSION, "is_error": False})
            journal = records.AttemptRecord(attempt, launch, {}, host_root=root / "host")
            journal.snapshot("finished", returncode=0, retain=True)
            original = {p.name: sha(p) for p in attempt.iterdir() if p.is_file()}
            with patch.object(records, "transcript_locations", side_effect=lambda s, c: records_locations(s, c, root / "host")):
                records.prepare_resume(attempt, root / "round2", "Continue same child", CHILD)
                with self.assertRaisesRegex(ValueError, "not observed"):
                    records.prepare_resume(attempt, root / "wrong", "Continue", "unknown")
                (attempt / "prompt.txt").write_text("drift", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "configuration changed"):
                    records.prepare_resume(attempt, root / "drift", "Continue", CHILD)
                next_launch = json.loads((root / "round2/launch.json").read_bytes())
                with self.assertRaisesRegex(ValueError, "configuration changed"):
                    records.execute(root / "round2", next_launch, {})
                self.assertFalse((root / "round2/stdout.jsonl").exists())
            next_launch = json.loads((root / "round2/launch.json").read_bytes())
            self.assertEqual(next_launch["cwd"], str(consumer))
            self.assertEqual(next_launch["command"][-2:], ["--resume", SESSION])
            self.assertNotIn("--session-id", next_launch["command"])
            self.assertEqual(next_launch["expected_child_id"], CHILD)
            self.assertEqual(sha(attempt / "continuation.json"), original["continuation.json"])
            self.assertEqual(sha(attempt / "native-transcripts/parent.jsonl"), sha(root / "host/project" / (SESSION + ".jsonl")))
            self.assertFalse((root / "wrong").exists())
            self.assertFalse((root / "drift").exists())

    def test_real_process_timeout_retains_last_artifact_and_resumable_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, consumer, launch = self.setup_attempt(root)
            script = consumer / "host.py"
            script.write_text("import json,time,pathlib\npathlib.Path('work').mkdir()\npathlib.Path('work/partial.json').write_text('{}')\nprint(json.dumps({'type':'system','session_id':" + repr(SESSION) + "}),flush=True)\ntime.sleep(60)\n", encoding="utf-8")
            launch["command"] = [sys.executable, str(script)]
            write_json(attempt / "launch.json", launch)
            code, _, _, result = records.execute(attempt, launch, dict(os.environ), timeout=2)
            self.assertNotEqual(code, 0)
            self.assertEqual(result["interruption_reason"], "timeout")
            self.assertEqual(result["session_id"], SESSION)
            self.assertEqual(result["status"], "finished")
            self.assertEqual(len(result["artifacts"]), 1)
            self.assertEqual(result["artifacts"][0]["sha256"], sha(consumer / "work/partial.json"))
            self.assertEqual(result["behavioral_verdict"], "ungraded")
            original = sha(attempt / "continuation.json")
            with self.assertRaisesRegex(ValueError, "fresh native attempt"):
                records.execute(attempt, launch, dict(os.environ))
            self.assertEqual(sha(attempt / "continuation.json"), original)

    def test_common_runner_records_shared_consumer_and_scoped_environment(self):
        from evaluations.request_review_trials import run

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, consumer, launch = self.setup_attempt(root)
            script = consumer / "host.py"
            script.write_text("import os,json,pathlib\npathlib.Path('work').mkdir()\npathlib.Path('work/env.json').write_text(json.dumps({k:k in os.environ for k in ['ANTHROPIC_API_KEY','CLAUDE_CODE_SKIP_PROMPT_HISTORY']}))\nprint(json.dumps({'type':'result','session_id':" + repr(SESSION) + ",'is_error':False}))\n", encoding="utf-8")
            launch["command"] = [sys.executable, str(script)]
            write_json(attempt / "launch.json", launch)
            with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "fixture", "CLAUDE_CODE_SKIP_PROMPT_HISTORY": "1"}):
                run(attempt)
            record = json.loads((attempt / "record.json").read_bytes())
            self.assertEqual(record["execution_status"], "host_completed_ungraded")
            self.assertIn("work/env.json", record["artifacts"])
            self.assertEqual(record["continuation"]["sha256"], sha(attempt / "continuation.json"))
            self.assertFalse(any(json.loads((consumer / "work/env.json").read_bytes()).values()))
            self.assertTrue(json.loads((attempt / "execution-environment.json").read_bytes())["removed_history_override"])

    def test_historical_inspection_never_rewrites_old_record(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, _, _ = self.setup_attempt(root, True)
            self.event(attempt, {"type": "result", "session_id": SESSION, "is_error": True, "result": "You're out of usage credits"})
            write_json(attempt / "record.json", {"returncode": 1, "execution_status": "host_error"})
            original = {p.name: sha(p) for p in attempt.iterdir()}
            output = root / "review/historical.json"
            with patch.object(sys, "argv", ["native_trial_records", "inspect", str(attempt), "--out", str(output)]):
                records.main()
                with self.assertRaisesRegex(ValueError, "fresh"):
                    records.main()
            self.assertEqual(original, {p.name: sha(p) for p in attempt.iterdir()})
            self.assertEqual(json.loads(output.read_bytes())["interruption_reason"], "usage_limit")

    def test_nonclaude_session_and_pathlike_identifiers_cannot_claim_claude_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, _, launch = self.setup_attempt(root)
            launch["host"] = "codex"
            self.event(attempt, {"type": "thread.started", "thread_id": SESSION})
            self.event(attempt, {"type": "turn.completed"})
            result = records.AttemptRecord(attempt, launch, {}).snapshot("finished", returncode=0)
            self.assertEqual(result["session_id"], SESSION)
            self.assertIsNone(result["interruption_reason"])
            self.assertFalse(result["native_resume"]["available"])
            self.assertEqual(records.transcript_locations("../*", ["../../secret"], root)["parent_matches"], 0)

    def test_package_payload_drift_is_rejected_with_unchanged_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, consumer, launch = self.setup_attempt(root)
            kit = consumer / "kit"
            kit.mkdir()
            payload = kit / "profile.md"
            payload.write_text("original instructions", encoding="utf-8")
            write_json(kit / "bundle-manifest.json", {"files": [{"path": "profile.md", "sha256": sha(payload)}]})
            launch["command"] += ["--plugin-dir", str(kit)]
            write_json(attempt / "launch.json", launch)
            saved = records.AttemptRecord(attempt, launch, {}).snapshot("finished", returncode=0)
            records.verify_inputs(saved)
            payload.write_text("changed instructions", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "package payload changed"):
                records.verify_inputs(saved)

    def test_codex_journal_preserves_generic_child_identity_without_claiming_named_role(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, _, launch = self.setup_attempt(root)
            launch["host"] = "codex"
            self.event(attempt, {"type": "thread.started", "thread_id": SESSION})
            self.event(attempt, {"type": "turn.completed"})
            child = "12345678-1234-1234-1234-123456789def"
            event = {"type": "session_meta", "payload": {"id": child, "session_id": SESSION,
                     "parent_thread_id": SESSION, "agent_path": "/root/pixl_specialist",
                     "source": {"subagent": {"thread_spawn": {"agent_role": None}}}}}
            (attempt / ("native-" + child + ".jsonl")).write_text(json.dumps(event) + "\n", encoding="utf-8")
            result = records.AttemptRecord(attempt, launch, {}).snapshot("finished", returncode=0)
            self.assertEqual(result["children"][0]["id"], child)
            self.assertIsNone(result["children"][0]["role"])
            self.assertIn(child, result["retained_journals"])
            self.assertIn("not qualified", result["native_resume"]["reason"])


records_locations = records.transcript_locations


if __name__ == "__main__":
    unittest.main()
