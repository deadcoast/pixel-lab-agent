"""Native continuation records preserve interruptions without inventing host success."""

import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from evaluations import native_trial_records as records
from evaluations.host_trials import sha, write_json

SESSION = "12345678-1234-1234-1234-123456789abc"
CHILD = "a123456789"


def windows_replace_probe(root):
    """Exercise an actual owned Windows handle that denies shared deletion."""
    import ctypes
    import threading
    from ctypes import wintypes

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
                                  wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    target = Path(root) / "continuation.json"
    write_json(target, {"snapshot": "original"})
    original = target.read_bytes()
    # GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_WRITE, OPEN_EXISTING. The
    # intentionally absent FILE_SHARE_DELETE holds replacement until release.
    handle = kernel.CreateFileW(str(target), 0x80000000, 0x1 | 0x2, None, 3, 0x80, None)
    if handle == ctypes.c_void_p(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    closed = []

    def release():
        closed.append(bool(kernel.CloseHandle(handle)))

    timer = threading.Timer(0.2, release)
    replace, observed = os.replace, []

    def observe_replace(source, destination):
        try:
            replace(source, destination)
        except PermissionError as error:
            observed.append({"winerror": getattr(error, "winerror", None), "errno": error.errno,
                             "original_bytes_preserved": target.read_bytes() == original})
            raise

    started = time.monotonic()
    timer.start()
    try:
        with patch.object(records.os, "replace", side_effect=observe_replace):
            records.atomic_json(target, {"snapshot": "replacement"})
    finally:
        timer.join()
    return {"scope": "Owned temporary file and actual Windows sharing lock; no native model or provider execution",
            "denied_attempts": observed, "handle_closed": closed == [True],
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "replacement_saved": json.loads(target.read_bytes()) == {"snapshot": "replacement"},
            "pending_files_after_success": len(list(target.parent.glob("*.tmp")))}


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

    def windows_lock(self):
        error = PermissionError(13, "Synthetic Windows replacement denial")
        error.winerror = 5
        return error

    def test_atomic_json_retries_transient_windows_lock_with_same_pending_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "continuation.json"
            target.write_bytes(b"old target")
            replace = os.replace
            attempts = []

            def transient(source, destination):
                attempts.append((Path(source), Path(source).read_bytes()))
                self.assertEqual(target.read_bytes(), b"old target")
                if len(attempts) < 3:
                    raise self.windows_lock()
                replace(source, destination)

            with patch.object(records.os, "replace", side_effect=transient), patch.object(records.time, "sleep") as sleep:
                records.atomic_json(target, {"new": "value"})
            self.assertEqual(json.loads(target.read_bytes()), {"new": "value"})
            self.assertEqual(len(attempts), 3)
            self.assertTrue(all(item == attempts[0] for item in attempts))
            self.assertEqual(sleep.call_count, 2)
            self.assertFalse(list(target.parent.glob("*.tmp")))

    def test_atomic_json_permanent_lock_preserves_original_and_each_pending_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "continuation.json"
            target.write_bytes(b"old target")
            pending = []
            with patch.object(records.os, "replace", side_effect=lambda *_: (_ for _ in ()).throw(self.windows_lock())) as replace, patch.object(records.time, "sleep"):
                for value in (1, 2):
                    with self.assertRaises(PermissionError) as caught:
                        records.atomic_json(target, {"snapshot": value})
                    pending.append(Path(caught.exception.pending_json_path))
                    self.assertEqual(caught.exception.atomic_replace_attempts, 5)
            self.assertEqual(replace.call_count, 10)
            self.assertEqual(target.read_bytes(), b"old target")
            self.assertEqual(len(set(pending)), 2)
            self.assertEqual([json.loads(path.read_bytes()) for path in pending], [{"snapshot": 1}, {"snapshot": 2}])

    def test_atomic_json_does_not_retry_unrelated_io_error(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "continuation.json"
            target.write_bytes(b"old target")
            with (patch.object(records.os, "replace", side_effect=OSError(5, "synthetic I/O failure")) as replace,
                  patch.object(records.time, "sleep") as sleep, self.assertRaises(OSError)):
                records.atomic_json(target, {"snapshot": "pending"})
            self.assertEqual(replace.call_count, 1)
            sleep.assert_not_called()
            self.assertEqual(target.read_bytes(), b"old target")

    @unittest.skipUnless(os.name == "nt", "An actual Windows sharing handle is required")
    def test_actual_windows_share_lock_releases_during_bounded_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            result = windows_replace_probe(directory)
        self.assertTrue(result["denied_attempts"])
        self.assertTrue(all(row["original_bytes_preserved"] for row in result["denied_attempts"]))
        self.assertTrue(result["handle_closed"])
        self.assertTrue(result["replacement_saved"])
        self.assertEqual(result["pending_files_after_success"], 0)

    def test_recording_lock_does_not_abandon_live_child_or_claim_launch_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, consumer, launch = self.setup_attempt(root)
            launch["host"] = "codex"
            script = consumer / "host.py"
            script.write_text(
                "import json,time,pathlib\n"
                "print(json.dumps({'type':'thread.started','thread_id':" + repr(SESSION) + "}),flush=True)\n"
                "deadline=time.monotonic()+8\n"
                "while not pathlib.Path('release').exists() and time.monotonic()<deadline: time.sleep(.02)\n"
                "time.sleep(.15)\npathlib.Path('finished').write_text('completed once')\n"
                "print(json.dumps({'type':'turn.completed'}),flush=True)\n", encoding="utf-8")
            launch["command"] = [sys.executable, str(script)]
            write_json(attempt / "launch.json", launch)
            replace = os.replace
            original = []

            def locked_after_initial(source, destination):
                if not original:
                    replace(source, destination)
                    original.append(Path(destination).read_bytes())
                    return
                (consumer / "release").write_text("recording failed while native process was owned", encoding="utf-8")
                raise self.windows_lock()

            with patch.object(records.os, "replace", side_effect=locked_after_initial), patch.object(records, "stop_process") as stop:
                code, _, events, result = records.execute(attempt, launch, dict(os.environ), timeout=10)
            stop.assert_not_called()
            self.assertEqual(code, 0)
            self.assertEqual((consumer / "finished").read_text(), "completed once")
            self.assertEqual([event["type"] for event in events], ["thread.started", "turn.completed"])
            self.assertEqual(result["status"], "finished")
            self.assertIsNone(result["interruption_reason"])
            self.assertEqual(result["recording_status"], "snapshot_failed")
            self.assertTrue(all(failure["process_started"] for failure in result["recording_errors"]))
            self.assertEqual((attempt / "continuation.json").read_bytes(), original[0])
            receipts = [json.loads(path.read_bytes()) for path in attempt.glob("recording-error-*.json")]
            final = next(item for item in receipts if item["failure"]["snapshot_status"] == "finished")
            self.assertEqual(final["record"]["returncode"], 0)
            self.assertEqual(final["record"]["session_id"], SESSION)
            self.assertIsNone(final["record"]["interruption_reason"])
            self.assertGreaterEqual(len(list(attempt.glob("continuation.json.*.tmp"))), 2)

    def test_real_launch_failure_remains_distinct_from_recording_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            attempt, _, launch = self.setup_attempt(Path(directory))
            with (patch.object(records.subprocess, "Popen", side_effect=OSError(2, "synthetic launch failure")),
                  self.assertRaises(OSError)):
                records.execute(attempt, launch, dict(os.environ))
            result = json.loads((attempt / "continuation.json").read_bytes())
            self.assertEqual(result["interruption_reason"], "launch_error")
            self.assertEqual(result["recording_status"], "recorded")

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

    def test_explicit_consumer_configuration_and_generated_package_drift_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, consumer, launch = self.setup_attempt(root)
            role = consumer / "role.toml"
            wrapper = consumer / "SKILL.md"
            role.write_text('name = "pixl"\ndeveloper_instructions = "Follow the selected skill."\n', encoding="utf-8")
            wrapper.write_text("Selected wrapper", encoding="utf-8")
            package = consumer / "kit"
            package.mkdir()
            generated = package / "generated.md"
            generated.write_text("frozen", encoding="utf-8")
            write_json(package / "bundle-manifest.json", {"files": [], "generated_files": [
                {"path": "generated.md", "sha256": sha(generated)}]})
            launch["configuration_files"] = {"role": "role.toml", "wrapper": str(wrapper),
                                              "package": "kit/bundle-manifest.json"}
            write_json(attempt / "launch.json", launch)
            saved = records.AttemptRecord(attempt, launch, {}).snapshot("finished", returncode=0)
            self.assertEqual(saved["configuration"]["file:role"]["path"], str(role.resolve()))
            records.verify_inputs(saved)
            generated.write_text("changed", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "package payload changed"):
                records.verify_inputs(saved)
            generated.write_text("frozen", encoding="utf-8")
            wrapper.write_text("Changed wrapper", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "configuration changed"):
                records.verify_inputs(saved)
            role.unlink()
            with self.assertRaises(FileNotFoundError):
                records.AttemptRecord(attempt, launch, {})

    def test_codex_requested_role_and_observed_role_are_distinct_with_same_child_followup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, consumer, launch = self.setup_attempt(root)
            launch["host"] = "codex"
            role = consumer / "role.toml"
            instruction = "Read the selected profile and preserve this consumer's assignment."
            role.write_text('name = "pixl"\ndeveloper_instructions = ' + json.dumps(instruction), encoding="utf-8")
            launch["configuration_files"] = {"role": "role.toml"}
            self.event(attempt, {"type": "thread.started", "thread_id": SESSION})
            self.event(attempt, {"type": "turn.completed"})
            child = "12345678-1234-1234-1234-123456789def"
            parent_events = [{"type": "session_meta", "payload": {"id": SESSION, "session_id": SESSION,
                              "cwd": str(consumer)}}]
            for index, tool in enumerate(["spawn_agent", "followup_task"]):
                call_id = "call-" + str(index)
                args = {"agent_type": "pixl", "task_name": "specialist", "message": "opaque-content"} if index == 0 else {
                    "target": "specialist", "message": "opaque-content"}
                parent_events.extend([
                    {"type": "response_item", "payload": {"type": "function_call", "namespace": "collaboration",
                     "name": tool, "call_id": call_id, "arguments": json.dumps(args)}},
                    {"type": "event_msg", "payload": {"type": "item_completed", "item": {"type": "SubAgentActivity",
                     "id": call_id, "kind": "started" if index == 0 else "interacted", "agent_thread_id": child,
                     "agent_path": "/root/specialist"}}},
                    {"type": "response_item", "payload": {"type": "function_call_output", "call_id": call_id, "output": ""}},
                ])
            parent_path = attempt / ("native-" + SESSION + ".jsonl")
            parent_path.write_text("\n".join(map(json.dumps, parent_events)) + '\n{"unfinished":', encoding="utf-8")
            child_meta = {"type": "session_meta", "payload": {"id": child, "session_id": SESSION,
                "parent_thread_id": SESSION, "cwd": str(consumer), "subagent_history_start_ordinal": 5,
                "source": {"subagent": {"thread_spawn": {"agent_role": None}}}}}
            inherited_call = {**parent_events[1], "ordinal": 2}
            developer = {"type": "response_item", "ordinal": 6, "payload": {"type": "message", "role": "developer",
                          "content": [{"type": "input_text", "text": instruction}]}}
            child_path = attempt / ("native-" + child + ".jsonl")
            for actual_role in [None, "pixl", {"name": "pixl", "path": str(role)}]:
                with self.subTest(actual_role=actual_role):
                    child_meta["payload"]["source"]["subagent"]["thread_spawn"]["agent_role"] = actual_role
                    child_path.write_text("\n".join(map(json.dumps, [child_meta, inherited_call,
                        {**developer, "ordinal": 3}, developer])) + "\n", encoding="utf-8")
                    journal = records.AttemptRecord(attempt, launch, {})
                    saved = journal.snapshot("finished", returncode=0)
                    self.assertEqual(saved["children"][0]["role"], actual_role)
                    calls = saved["native_collaboration_calls"]
                    self.assertEqual([row["tool"] for row in calls], ["spawn_agent", "followup_task"])
                    self.assertEqual(calls[0]["requested_role"], "pixl")
                    self.assertEqual({row["child_id"] for row in calls}, {child})
                    self.assertTrue(all(row["result_observed"] for row in calls))
                    self.assertEqual(calls[1]["to"], "specialist")
                    self.assertNotIn("opaque-content", json.dumps(saved))
                    observations = saved["native_instruction_observations"]
                    self.assertEqual([row["context_scope"] for row in observations],
                        ["inherited_or_initial_child_context", "own_execution"])
                    self.assertEqual(observations[1]["configured_instruction_matches"][0]["sha256"], sha(role))
                    self.assertEqual(saved["native_session_metadata"][child]["cwd"], str(consumer))
                    self.assertEqual(saved["behavioral_verdict"], "ungraded")
                    self.assertFalse(saved["native_resume"]["available"])
            role.write_text('developer_instructions = "Changed after recording"', encoding="utf-8")
            records.codex_journals(attempt, saved)
            self.assertTrue(all(not row["configured_instruction_matches"] for row in saved["native_instruction_observations"]))

    def test_codex_stdout_collaboration_records_observed_status_without_role_inference(self):
        with tempfile.TemporaryDirectory() as directory:
            attempt, _, launch = self.setup_attempt(Path(directory))
            launch["host"] = "codex"
            self.event(attempt, {"type": "thread.started", "thread_id": SESSION})
            item = {"id": "item_11", "type": "collab_tool_call", "tool": "wait", "sender_thread_id": SESSION,
                    "receiver_thread_ids": [], "prompt": None, "agents_states": {}, "status": "in_progress"}
            self.event(attempt, {"type": "item.started", "item": item})
            self.event(attempt, {"type": "item.completed", "item": {**item, "status": "completed"}})
            result = records.AttemptRecord(attempt, launch, {}).snapshot("finished", returncode=0)
            self.assertEqual(result["calls"][0]["tool"], "wait")
            self.assertEqual(result["calls"][0]["result_line"], 3)
            self.assertEqual(result["calls"][0]["status"], "completed")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["native_instruction_observations"], [])

    def test_codex_role_parameter_availability_comes_from_actual_tool_declaration(self):
        with tempfile.TemporaryDirectory() as directory:
            attempt, _, launch = self.setup_attempt(Path(directory))
            launch["host"] = "codex"
            self.event(attempt, {"type": "thread.started", "thread_id": SESSION})
            path = attempt / ("native-" + SESSION + ".jsonl")
            metadata = {"type": "session_meta", "payload": {"id": SESSION}}
            for role_parameter in [None, {"type": "string", "description": "Available roles: pixl"}]:
                with self.subTest(role_parameter=role_parameter):
                    properties = {"task_name": {"type": "string"}, "message": {"type": "string", "encrypted": True}}
                    if role_parameter:
                        properties["agent_type"] = role_parameter
                    tool = {"type": "function", "name": "spawn_agent", "parameters": {"properties": properties}}
                    declaration = {"type": "response_item", "payload": {"type": "additional_tools",
                        "tools": [{"type": "namespace", "name": "collaboration", "tools": [tool]}]}}
                    path.write_text(json.dumps(metadata) + "\n" + json.dumps(declaration) + "\n", encoding="utf-8")
                    saved = records.AttemptRecord(attempt, launch, {}).snapshot("finished", returncode=0)
                    observed = saved["native_tool_declarations"][0]
                    self.assertEqual(observed["role_parameter"], role_parameter)
                    self.assertEqual("agent_type" in observed["parameter_names"], bool(role_parameter))
                    self.assertEqual(observed["line"], 2)
                    self.assertEqual(saved["children"], [])
                    self.assertEqual(saved["behavioral_verdict"], "ungraded")

    def test_codex_cold_child_instruction_scope_requires_observed_no_history_spawn(self):
        with tempfile.TemporaryDirectory() as directory:
            attempt, consumer, launch = self.setup_attempt(Path(directory))
            launch["host"] = "codex"
            self.event(attempt, {"type": "thread.started", "thread_id": SESSION})
            # Sort the child before the parent to exercise parent-first parsing.
            child = "02345678-1234-1234-1234-123456789def"
            parent_events = [{"type": "session_meta", "payload": {"id": SESSION}},
                {"type": "response_item", "payload": {"type": "function_call", "namespace": "collaboration",
                 "name": "spawn_agent", "call_id": "spawn", "arguments": json.dumps({"agent_type": "pixl", "fork_turns": "none"})}},
                {"type": "event_msg", "payload": {"item": {"type": "SubAgentActivity", "id": "spawn",
                 "kind": "started", "agent_thread_id": child, "agent_path": "/root/specialist"}}}]
            parent_path = attempt / ("native-" + SESSION + ".jsonl")
            parent_path.write_text("\n".join(map(json.dumps, parent_events)) + "\n", encoding="utf-8")
            metadata = {"type": "session_meta", "payload": {"id": child, "session_id": SESSION,
                "parent_thread_id": SESSION, "cwd": str(consumer), "agent_role": "pixl",
                "source": {"subagent": {"thread_spawn": {"agent_role": "pixl"}}}}}
            developer = {"type": "response_item", "ordinal": 4, "payload": {"type": "message", "role": "developer",
                "content": [{"type": "input_text", "text": "Role instructions"}]}}
            child_path = attempt / ("native-" + child + ".jsonl")
            for forked_from in [None, SESSION]:
                with self.subTest(forked_from=forked_from):
                    metadata["payload"]["forked_from_id"] = forked_from
                    child_path.write_text(json.dumps(metadata) + "\n" + json.dumps(developer) + "\n", encoding="utf-8")
                    saved = records.AttemptRecord(attempt, launch, {}).snapshot("finished", returncode=0)
                    self.assertEqual(saved["native_session_metadata"][child]["observed_fork_turns"], "none")
                    self.assertEqual(saved["children"][0]["top_level_role"], "pixl")
                    self.assertEqual(saved["native_instruction_observations"][0]["context_scope"],
                        "own_execution" if forked_from is None else "inherited_or_initial_child_context")

    def test_new_codex_preparation_registers_exact_project_role_and_records_its_hash(self):
        from evaluations import request_review_trials as trials

        with tempfile.TemporaryDirectory() as directory:
            attempt = (Path(directory) / "attempt").resolve()
            with patch.object(trials, "codex_command", return_value=["codex"]), patch.object(
                    trials.subprocess, "check_output", return_value="fixture-version\n"):
                trials.prepare(attempt, "codex", "save-indicator")
            launch = json.loads((attempt / "launch.json").read_bytes())
            registration = next(arg for arg in launch["command"] if arg.startswith("agents.pixl.config_file="))
            role = Path(json.loads(registration.split("=", 1)[1]))
            self.assertEqual(role, attempt / "project/.codex/agents/pixl.toml")
            self.assertEqual(launch["configuration_files"]["codex_role"], str(role))
            saved = records.AttemptRecord(attempt, launch, {}).snapshot("finished", returncode=None)
            self.assertEqual(saved["configuration"]["file:codex_role"]["sha256"], sha(role))
            self.assertEqual(saved["configuration"]["package"]["sha256"], sha(
                attempt / "project/.agents/skills/pixl-kit/bundle-manifest.json"))
            records.verify_inputs(saved)
            self.assertFalse((attempt / "stdout.jsonl").exists())
            self.assertEqual(saved["behavioral_verdict"], "ungraded")

    def test_cloned_export_consumer_relocates_recorded_configuration_with_its_command(self):
        from evaluations import candidate_review_export_case as case

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            predecessor = root / "evidence/candidate-review/20261109/native/codex-01"
            project = predecessor / "project"
            role = project / ".codex/agents/pixl.toml"
            role.parent.mkdir(parents=True)
            role.write_text('name="pixl"\ndeveloper_instructions="Selected role"', encoding="utf-8")
            old_manifest = project / ".agents/skills/review-kit/bundle-manifest.json"
            old_manifest.parent.mkdir(parents=True)
            write_json(old_manifest, {"files": [], "old": True})
            package = root / "plugins/pixl"
            package.mkdir(parents=True)
            write_json(package / "bundle-manifest.json", {"files": [], "current": True})
            (project / "work").mkdir()
            write_json(project / "review.json", {"observation": {}})
            write_json(predecessor / "launch.json", {"host": "codex", "cwd": str(project),
                "command": ["codex", "-C", str(project), "-c", "agents.pixl.config_file=" + json.dumps(str(role))],
                "configuration_files": {"codex_role": str(role), "package": str(old_manifest)}})
            original_launch = sha(predecessor / "launch.json")
            candidate = SimpleNamespace(id="candidate")
            doc = SimpleNamespace(records={
                "provenance-correction.delivery.task": SimpleNamespace(kind="T", fields={"ca": [candidate]}),
                "review": SimpleNamespace(kind="X", id="review", fields={
                    "mt": {"candidate_review": 1, "candidate": candidate}, "ur": "review.json"})})
            destination = root / "new-export"
            with patch.object(case, "ROOT", root), patch.object(case.store, "load", return_value=doc), patch.object(
                    case.graph, "validate"), patch.object(case.codec, "digest", return_value="state"):
                case.prepare(destination, "codex")
            launch = json.loads((destination / "launch.json").read_bytes())
            new_role = destination / "project/.codex/agents/pixl.toml"
            self.assertEqual(launch["configuration_files"]["codex_role"], str(new_role))
            self.assertEqual(json.loads(launch["command"][-1].split("=", 1)[1]), str(new_role))
            self.assertEqual(launch["configuration_files"]["package"],
                             str(destination / "project/.agents/skills/export-kit/bundle-manifest.json"))
            saved = records.AttemptRecord(destination, launch, {}).snapshot("finished", returncode=None)
            role.unlink()
            old_manifest.unlink()
            records.verify_inputs(saved)
            self.assertEqual(sha(predecessor / "launch.json"), original_launch)

    def test_codex_retains_children_with_partial_journal_tail(self):
        from evaluations.request_review_trials import retain_journals

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            attempt, _, _ = self.setup_attempt(root)
            sessions = root / "host/sessions"
            sessions.mkdir(parents=True)
            child = "12345678-1234-1234-1234-123456789def"
            parent = sessions / (SESSION + ".jsonl")
            parent.write_text(json.dumps({"payload": {"item": {"type": "SubAgentActivity", "agent_thread_id": child}}})
                              + '\n{"unfinished":', encoding="utf-8")
            child_path = sessions / (child + ".jsonl")
            child_path.write_text("{}\n", encoding="utf-8")
            with patch.dict(os.environ, {"CODEX_HOME": str(root / "host")}):
                retain_journals(attempt, [{"type": "thread.started", "thread_id": SESSION}])
            self.assertEqual(sha(attempt / ("native-" + SESSION + ".jsonl")), sha(parent))
            self.assertEqual(sha(attempt / ("native-" + child + ".jsonl")), sha(child_path))


records_locations = records.transcript_locations


if __name__ == "__main__":
    unittest.main()
