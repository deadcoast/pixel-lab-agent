"""Guard against promoting host receipts to successful behavioral evaluations."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import check_host_evidence
from evaluations.check_host_evidence import retained_state_paths
from evaluations.host_trials import copy_inputs, outcome, sha, verify_run, write_json


class HostEvidenceTests(unittest.TestCase):
    def test_unrecorded_project_dependency_blocks_replay(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            trial = root / "runs" / "fixture"
            project = trial / "project"
            project.mkdir(parents=True)
            state = project / "state.px"
            state.write_text("fixture state", encoding="utf-8")
            (project / "unrecorded-dependency.txt").write_text("injected observation", encoding="utf-8")
            runner = root / "runner.py"
            runner.write_text("fixture runner", encoding="utf-8")
            archive = root / "runner-versions" / (sha(runner) + ".py")
            archive.parent.mkdir()
            archive.write_bytes(runner.read_bytes())
            packaged_runner = root / "package" / "scripts" / "pixl.py"
            packaged_runner.parent.mkdir(parents=True)
            replay_marker = root / "replay-ran.txt"
            packaged_runner.write_text(
                f"from pathlib import Path\nPath({str(replay_marker)!r}).write_text('ran')\nprint('{{}}')\n",
                encoding="utf-8",
            )
            write_json(trial / "record.json", {
                "runner_sha256": sha(runner), "bundle_manifest_sha256": "bundle",
                "execution_status": "host_completed_ungraded", "evidence_hashes": {},
                "artifacts": {"state.px": sha(state)},
            })
            with (
                patch.object(check_host_evidence, "EVIDENCE", root),
                patch.object(check_host_evidence, "freeze", return_value={"bundle_manifest_sha256": "bundle"}),
                self.assertRaises(SystemExit),
            ):
                check_host_evidence.main()
            report = json.loads((root / "integrity.json").read_text(encoding="utf-8"))
            self.assertEqual(report["evidence_error_count"], 1)
            self.assertEqual(report["runs"][0]["state_replay"], [])
            self.assertIn("project inventory", report["runs"][0]["errors"][0])
            self.assertFalse(replay_marker.exists())

    def test_store_replay_finds_host_chosen_directories_without_replaying_drafts(self):
        artifacts = {path: "hash" for path in (
            "pixl-state/state.px", ".pixl/state.px", "state.px",
            "pixl-state/history/abc.px", "review/candidate.px",
        )}
        self.assertEqual(retained_state_paths(artifacts),
                         [".pixl/state.px", "pixl-state/state.px", "state.px"])

    def test_claude_auth_error_with_success_subtype_is_not_completion(self):
        event = {"type": "result", "subtype": "success", "is_error": True,
                 "result": "Failed to authenticate", "usage": {"output_tokens": 0}}
        self.assertEqual(outcome(0, False, json.dumps(event)), "host_error")

    def test_interrupted_or_truncated_output_cannot_be_a_completed_trial(self):
        self.assertEqual(outcome(0, False, '{"type":"turn.started"}\n{'), "incomplete_no_completion_event")
        self.assertEqual(outcome(0, True, '{"type":"turn.completed"}'), "interrupted_timeout")
        self.assertEqual(outcome(0, False, 'null\n[]\n42'), "incomplete_no_completion_event")

    def test_successful_process_is_explicitly_ungraded(self):
        self.assertEqual(outcome(0, False, '{"type":"turn.completed"}'), "host_completed_ungraded")
        self.assertEqual(outcome(1, False, '{"type":"turn.completed"}'), "host_error")

    def test_changed_and_missing_transcript_are_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)
            transcript = target / "stdout.jsonl"
            transcript.write_text('{"type":"turn.completed"}\n', encoding="utf-8")
            write_json(target / "record.json", {"evidence_hashes": {"stdout.jsonl": sha(transcript)}, "artifacts": {}})
            self.assertEqual(verify_run(target), [])
            transcript.write_text('{"type":"turn.failed"}\n', encoding="utf-8")
            self.assertEqual(verify_run(target), ["changed or absent evidence: stdout.jsonl"])
            transcript.unlink()
            self.assertEqual(verify_run(target), ["changed or absent evidence: stdout.jsonl"])

    def test_outside_evidence_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)
            write_json(target / "record.json", {"evidence_hashes": {"../elsewhere": "0" * 64}, "artifacts": {}})
            self.assertEqual(verify_run(target), ["outside attempt: ../elsewhere"])

    def test_cold_resume_uses_only_verified_predecessor_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            previous = root / "previous"
            (previous / "project").mkdir(parents=True)
            state = previous / "project" / "saved.txt"
            state.write_text("known unresolved choices", encoding="utf-8")
            write_json(previous / "record.json", {"evidence_hashes": {}, "artifacts": {"saved.txt": sha(state)}})
            destination = root / "next"
            destination.mkdir()
            binding = copy_inputs(destination, root / "absent-fixtures", ["not-saved.png"], previous)
            self.assertEqual([p.name for p in destination.iterdir()], ["saved.txt"])
            self.assertEqual(binding["record_sha256"], sha(previous / "record.json"))
            state.write_text("altered after the trial", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "predecessor"):
                copy_inputs(root / "rejected", root / "absent-fixtures", [], previous)

    def test_unrecorded_predecessor_file_is_not_silently_carried_forward(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "project").mkdir()
            (root / "project" / "unexpected.txt").write_text("new context", encoding="utf-8")
            write_json(root / "record.json", {"evidence_hashes": {}, "artifacts": {}})
            with self.assertRaisesRegex(ValueError, "predecessor"):
                copy_inputs(root / "next", root / "fixtures", [], root)


if __name__ == "__main__":
    unittest.main()
