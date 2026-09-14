"""The report describes observed trials, including authentic negative outcomes."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from evaluations.host_trials import inventory, sha, write_json
from evaluations.write_host_report import build_report


class HostReportTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.identity = {
            "source_revision": "fixture", "source_tree_dirty": True,
            "bundle_manifest_sha256": "bundle", "profile_hash": "profile",
            "skill_hashes": {}, "runtime_hashes": {},
        }
        self.review = {"runs": [], "supplementary_continuations": [], "summary": {}, "global_limitations": []}
        self.integrity = {"runs": [], "evidence_error_count": 0, "state_validation_error_count": 0, "error_count": 0}
        write_json(self.root / "profile-scenarios.json", {"cases": [
            {"id": "mechanical-pass-visual-rejection", "criteria": ["Inspect the actual pixels."]},
            {"id": "missing-provider", "criteria": ["Do not invent a provider result."]},
            {"id": "unavailable-engine", "criteria": ["Leave unavailable engine checks unresolved."]},
        ]})

    def add_trial(self, attempt, host, *, auth_error=False, verdict="pass", prompt="same prompt", image="same pixels", cold=False):
        trial = self.root / "runs" / attempt
        trial.mkdir(parents=True)
        (trial / "input-project").mkdir()
        (trial / "project").mkdir()
        (trial / "input-project" / "candidate.png").write_text(image, encoding="utf-8")
        (trial / "prompt.txt").write_text(prompt, encoding="utf-8")
        write_json(trial / "inputs.json", inventory(trial / "input-project"))
        if host == "claude":
            events = [{"type": "system", "subtype": "init", "model": "claude-selected",
                       "plugins": [{"name": "pixl"}], "skills": ["pixl:pixl"], "mcp_servers": [{"name": "pixl-local", "status": "connected"}]}]
            if not auth_error:
                events.append({"type": "assistant", "message": {"model": "claude-observed", "content": [{"text": "Reviewed."}]}})
            events.append({"type": "result", "subtype": "success", "is_error": auth_error,
                           "usage": {"input_tokens": 0 if auth_error else 30, "output_tokens": 0 if auth_error else 6},
                           "modelUsage": {} if auth_error else {"claude-observed": {"inputTokens": 30}},
                           "total_cost_usd": 0 if auth_error else 0.01, "duration_api_ms": 0 if auth_error else 200})
        else:
            events = [{"type": "turn.completed", "usage": {"input_tokens": 50, "output_tokens": 7}}]
        (trial / "stdout.jsonl").write_text("\n".join(json.dumps(event) for event in events) + "\n", encoding="utf-8")
        record = {
            "attempt": attempt, "host": host, "host_and_version": host + " fixture-version",
            "case_id": "mechanical-pass-visual-rejection", "phase": "cold_resume" if cold else "fresh",
            "requested_model": "codex-requested" if host == "codex" else None,
            "observed_model": "claude-selected" if auth_error else None,
            "execution_status": "host_error" if auth_error else "host_completed_ungraded",
            "elapsed_seconds": 1, "artifacts": {}, "package_mutated": False,
            "bundle_manifest_sha256": "bundle", "shell_sandbox": "fixture-access",
            "command": [host, "--ephemeral"] if host == "codex" else [host, "--no-session-persistence", "--plugin-dir", "fixture"],
            "evidence_hashes": inventory(trial),
        }
        write_json(trial / "record.json", record)
        review = {"attempt": attempt, "case_id": record["case_id"],
                  "reviewed_evidence_hashes": {name: sha(trial / name) for name in ("record.json", "stdout.jsonl", "prompt.txt")},
                  "host_layer": {"execution": record["execution_status"]}, "production_layer": {"provider_execution": "not_performed"}}
        if cold:
            review["checks"] = [{"check": "Loads saved context.", "verdict": verdict}]
            self.review["supplementary_continuations"].append(review)
        else:
            review["criteria"] = [{"criterion": "Inspect the actual pixels.", "verdict": verdict}]
            self.review["runs"].append(review)
        self.integrity["runs"].append({"attempt": attempt, "record_sha256": sha(trial / "record.json"), "errors": [], "state_replay": []})
        return trial

    def compile(self):
        counts = {}
        for entry in self.review["runs"]:
            for criterion in entry["criteria"]:
                counts[criterion["verdict"]] = counts.get(criterion["verdict"], 0) + 1
        self.review["summary"]["original_criterion_verdicts"] = counts
        write_json(self.root / "criterion-review.json", self.review)
        write_json(self.root / "integrity.json", self.integrity)
        return build_report(self.root, self.identity)

    def test_new_claude_success_does_not_promote_old_auth_failure(self):
        self.add_trial("codex-a", "codex")
        self.add_trial("claude-auth", "claude", auth_error=True, verdict="unverified")
        self.add_trial("claude-a", "claude")
        report = self.compile()
        hosts = report["coverage"]["by_host"]
        self.assertEqual(hosts["claude"]["completed_inference_sessions"], 1)
        self.assertEqual(hosts["claude"]["execution_status_counts"]["host_error"], 1)
        auth = next(row for row in report["attempts"] if row["attempt"] == "claude-auth")
        self.assertEqual(auth["host_reported_model"], "claude-selected")
        self.assertIsNone(auth["observed_model"])
        self.assertFalse(auth["inference_observed"])
        successful = next(row for row in report["attempts"] if row["attempt"] == "claude-a")
        self.assertEqual(successful["observed_model"], "claude-observed")
        self.assertEqual(successful["claude_reported_usage"]["output_tokens"], 6)
        self.assertIsNone(successful["codex_reported_usage"])
        self.assertEqual(report["coverage"]["original_criterion_verdicts"], {"pass": 2, "unverified": 1})

    def test_invalid_model_state_is_reportable_but_corruption_is_rejected(self):
        self.add_trial("codex-a", "codex", verdict="fail")
        self.integrity["state_validation_error_count"] = self.integrity["error_count"] = 1
        self.integrity["runs"][0]["state_replay"] = [{"returncode": 2, "command": ["pixl", "validate"]}]
        report = self.compile()
        self.assertEqual(report["evidence_validation"]["state_validation_error_count"], 1)
        self.assertEqual(report["attempts"][0]["state_validation_failures"], 1)
        self.integrity["evidence_error_count"] = 1
        with self.assertRaisesRegex(ValueError, "corrupt"):
            self.compile()

    def test_pairs_compare_actual_bytes_and_keep_protocol_differences(self):
        self.add_trial("codex-visual-first", "codex")
        self.add_trial("codex-visual-repeat", "codex")
        self.add_trial("claude-visual-first", "claude")
        self.add_trial("claude-other-input", "claude", image="different pixels", prompt="different prompt")
        report = self.compile()
        pairs = report["comparisons"]["cross_host_pairs"]
        same = next(row for row in pairs if row["left"] == "codex-visual-first" and row["right"] == "claude-visual-first")
        self.assertTrue(same["prompt_bytes_equal"] and same["input_image_bytes_equal"])
        self.assertIn("host_protocol_differs", same["differences"])
        different = next(row for row in pairs if row["left"] == "codex-visual-first" and row["right"] == "claude-other-input")
        self.assertFalse(different["prompt_bytes_equal"] or different["input_image_bytes_equal"])
        repeats = report["comparisons"]["same_host_repeat_pairs"]
        self.assertEqual(len(repeats), 2)

    def test_cold_continuation_does_not_add_catalog_case_coverage(self):
        self.add_trial("codex-cold", "codex", cold=True)
        report = self.compile()
        self.assertEqual(report["coverage"]["by_host"]["codex"]["completed_inference_sessions"], 1)
        self.assertEqual(report["coverage"]["by_host"]["codex"]["catalog_cases_with_completed_inference"], [])
        self.assertEqual(report["coverage"]["original_criterion_verdicts"], {})
        self.assertEqual(report["coverage"]["supplementary_check_verdicts"], {"pass": 1})

    def test_changed_reviewed_evidence_is_rejected(self):
        trial = self.add_trial("codex-a", "codex")
        (trial / "stdout.jsonl").write_text("changed", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.compile()

    def test_authentication_only_attempt_cannot_receive_behavior_pass(self):
        self.add_trial("claude-auth", "claude", auth_error=True, verdict="pass")
        with self.assertRaisesRegex(ValueError, "lacks observed inference"):
            self.compile()

    def test_interrupted_inference_preserves_observable_verdicts_without_completed_turn(self):
        self.add_trial("codex-a", "codex")
        trial = self.add_trial("claude-interrupted", "claude", verdict="fail")
        record = json.loads((trial / "record.json").read_text(encoding="utf-8"))
        record["execution_status"] = "interrupted_timeout"
        write_json(trial / "record.json", record)
        digest = sha(trial / "record.json")
        self.review["runs"][-1]["reviewed_evidence_hashes"]["record.json"] = digest
        self.integrity["runs"][-1]["record_sha256"] = digest
        report = self.compile()
        claude = report["coverage"]["by_host"]["claude"]
        self.assertEqual(claude["sessions_with_observed_inference"], 1)
        self.assertEqual(claude["completed_inference_sessions"], 0)
        self.assertEqual(claude["original_criterion_verdicts"], {"fail": 1})
        pair = report["comparisons"]["cross_host_pairs"][0]
        self.assertTrue(pair["both_observed_inference"])
        self.assertFalse(pair["both_completed_inference"])
        self.assertIn("incomplete_host_turn_pair", pair["differences"])
        self.assertEqual(report["comparisons"]["catalog_cases_with_matched_observed_inference"], ["mechanical-pass-visual-rejection"])
        self.assertEqual(report["comparisons"]["catalog_cases_with_matched_completed_inference"], [])

    def test_interrupted_codex_activity_counts_without_completion_usage(self):
        trial = self.add_trial("codex-partial", "codex")
        for item in ({"type": "agent_message", "text": "Inspecting the supplied image."},
                     {"type": "reasoning", "text": "Need to inspect actual image bytes."},
                     {"type": "mcp_tool_call", "server": "pixl_local", "tool": "pixl_asset_check"}):
            with self.subTest(item_type=item["type"]):
                (trial / "stdout.jsonl").write_text(json.dumps({"type": "item.completed", "item": item}) + "\n", encoding="utf-8")
                record = json.loads((trial / "record.json").read_text(encoding="utf-8"))
                record["execution_status"] = "interrupted_timeout"
                record["evidence_hashes"]["stdout.jsonl"] = sha(trial / "stdout.jsonl")
                write_json(trial / "record.json", record)
                for name in ("record.json", "stdout.jsonl"):
                    self.review["runs"][0]["reviewed_evidence_hashes"][name] = sha(trial / name)
                self.integrity["runs"][0]["record_sha256"] = sha(trial / "record.json")
                row = self.compile()["attempts"][0]
                self.assertTrue(row["inference_observed"])
                self.assertFalse(row["completed_inference_session"])
                self.assertIsNone(row["codex_reported_usage"])

    def test_codex_thread_initialization_is_not_inference(self):
        trial = self.add_trial("codex-startup", "codex", verdict="unverified")
        (trial / "stdout.jsonl").write_text('{"type":"thread.started"}\n{"type":"turn.started"}\n', encoding="utf-8")
        record = json.loads((trial / "record.json").read_text(encoding="utf-8"))
        record["execution_status"] = "interrupted_timeout"
        record["evidence_hashes"]["stdout.jsonl"] = sha(trial / "stdout.jsonl")
        write_json(trial / "record.json", record)
        for name in ("record.json", "stdout.jsonl"):
            self.review["runs"][0]["reviewed_evidence_hashes"][name] = sha(trial / name)
        self.integrity["runs"][0]["record_sha256"] = sha(trial / "record.json")
        row = self.compile()["attempts"][0]
        self.assertFalse(row["inference_observed"])
        self.assertFalse(row["completed_inference_session"])


if __name__ == "__main__":
    unittest.main()
