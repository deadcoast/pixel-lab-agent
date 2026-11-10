"""Known failures return safe reads, without inventing remote observations."""

import json
import unittest

from pixl import diagnostics, jobs
from pixl.codec import PixlError
from tests import test_jobs as job_fixture


class DiagnosticsTests(unittest.TestCase):
    def test_existing_exception_text_and_code_stay_compatible(self):
        plain = PixlError("stale_write", "reload the selected state")
        context = {"job_state": "unknown"}
        attached = PixlError("stale_write", "reload the selected state", context=context)
        context["job_state"] = "failed"
        self.assertEqual(str(plain), str(attached))
        self.assertEqual(plain.context, {})
        self.assertEqual(attached.context, {"job_state": "unknown"})
        result = diagnostics.error_result("pixl_plar_handoff", plain, {"asset_id": "queue.working", "expect": "a" * 64})
        self.assertEqual(result["error"], plain.code)
        self.assertEqual(result["detail"], str(plain))
        self.assertEqual(result["category"], "stale_local_state")
        self.assertEqual(result["recovery"]["operation"], "pixl_plar_read")
        self.assertEqual(result["recovery"]["arguments"], {"path": "plar.txt", "asset_id": "queue.working"})

    def test_cli_and_mcp_argument_aliases_produce_same_safe_job_recovery(self):
        error = PixlError("job_stale", "saved request context changed")
        cli = diagnostics.error_result("job-dispatch", error, {"job": "kept.job", "store": ".pixl/asset", "expect": "b" * 64})
        mcp = diagnostics.error_result("pixl_job_dispatch", error, {"job_id": "kept.job", "store": ".pixl/asset", "expect": "b" * 64})
        self.assertEqual(cli, mcp)
        self.assertEqual(cli["recovery"]["operation"], "pixl_jobs")
        self.assertEqual(cli["recovery"]["arguments"], {"path": ".pixl/asset/state.px"})

    def test_only_observed_context_can_classify_unknown_remote_result(self):
        error = PixlError("job_pending", "a job may be unknown; inspect it")
        arguments = {"store": ".pixl", "job_id": "new.job", "job_state": "unknown", "context": {"job_state": "unknown"}}
        unknown_claim = diagnostics.error_result("pixl_job_prepare", error, arguments)
        self.assertEqual(unknown_claim["category"], "unclassified")
        self.assertNotIn("job_state", unknown_claim["identity"])
        error = PixlError(error.code, error.detail, context={"job_state": "unknown", "job_id": "kept.job", "task_id": "retained.task", "state_hash": "c" * 64})
        result = diagnostics.error_result("pixl_job_prepare", error, arguments)
        self.assertEqual(result["category"], "uncertain_remote_result")
        self.assertEqual(result["identity"]["job_id"], "kept.job")
        self.assertEqual(result["identity"]["state_hash"], "c" * 64)
        self.assertEqual(result["recovery"]["action"], "reconcile_existing_job")
        self.assertEqual(result["recovery"]["operation"], "pixl_jobs")
        self.assertNotIn("new.job", json.dumps(result))

    def test_known_prepared_running_and_terminal_work_is_not_uncertain_submission(self):
        for state, action in [
            ("prepared", "inspect_prepared_job"), ("submitted", "observe_existing_job"),
            ("running", "observe_existing_job"), ("succeeded", "inspect_retained_result"),
            ("failed", "inspect_retained_failure"),
        ]:
            with self.subTest(state=state):
                result = diagnostics.error_result("job-dispatch", PixlError("job_history", "existing attempt", context={"job_state": state, "job_id": "retained"}), {"store": ".pixl"})
                self.assertEqual(result["category"], "retained_work")
                self.assertEqual(result["recovery"]["action"], action)
                self.assertEqual(result["recovery"]["operation"], "pixl_jobs")

    def test_catalog_omission_is_not_live_missing_capability(self):
        cached = diagnostics.error_result("prepare", PixlError("platform_tool", "tool is not in dated catalog"))
        missing = diagnostics.error_result("pixl_unknown", PixlError("unknown_tool", "pixl_unknown"))
        self.assertEqual(cached["category"], "unclassified")
        self.assertEqual(cached["recovery"]["action"], "inspect_current_tool_declarations")
        self.assertEqual(missing["category"], "missing_capability")
        self.assertNotIn("operation", missing["recovery"])

    def test_malformed_authoring_is_separate_from_unavailable_observation(self):
        for code in ["input_schema", "caller_result_input", "caller_result_size", "handoff_details", "syntax", "json"]:
            with self.subTest(code=code):
                result = diagnostics.error_result("plar_handoff", PixlError(code, "invalid input"))
                self.assertEqual(result["category"], "invalid_authoring")
                self.assertEqual(result["recovery"]["action"], "correct_input")
        for error in [PixlError("file_read", "missing input"), PixlError("caller_artifact_unavailable", "missing report"), FileNotFoundError("missing input")]:
            result = diagnostics.error_result("plar_handoff", error)
            self.assertEqual(result["category"], "unavailable_observation")
            self.assertEqual(result["recovery"]["action"], "restore_observation")

    def test_json_read_uses_actual_exception_cause_not_message_guessing(self):
        for cause, category in [(OSError("cannot read"), "unavailable_observation"), (ValueError("cannot parse"), "invalid_authoring"), (None, "unclassified")]:
            error = PixlError("json_read", "input.json")
            error.__cause__ = cause
            result = diagnostics.error_result("plar_handoff", error)
            self.assertEqual(result["category"], category)

    def test_source_drift_returns_reindex_not_same_stale_read(self):
        arguments = {"path": "work/report.json", "expect": "d" * 64, "start": 1, "end": 20}
        result = diagnostics.error_result("source", PixlError("source_hash", "source changed"), arguments)
        self.assertEqual(result["category"], "stale_local_state")
        self.assertEqual(result["recovery"]["operation"], "pixl_catalog")
        self.assertEqual(result["recovery"]["arguments"], {"paths": ["work/report.json"]})
        library = diagnostics.error_result("pixl_source", PixlError("source_hash", "source changed"), {**arguments, "scope": "library"})
        self.assertEqual(library["recovery"]["operation"], "pixl_sources")
        self.assertEqual(library["recovery"]["arguments"], {})

    def test_stale_state_reads_correct_domain_and_never_retries_a_write(self):
        cases = [
            ("pixl_plar_save", {"path": "requirements.txt"}, "pixl_plar_read", {"path": "requirements.txt"}),
            ("candidate-review", {"store": ".pixl/kept"}, "pixl_validate", {"path": ".pixl/kept/state.px"}),
            ("pixl_job_observe", {"store": ".pixl/kept"}, "pixl_jobs", {"path": ".pixl/kept/state.px"}),
        ]
        for operation, args, read, expected in cases:
            with self.subTest(operation=operation):
                result = diagnostics.error_result(operation, PixlError("stale_write", "refresh"), args)
                self.assertEqual(result["recovery"]["operation"], read)
                self.assertEqual(result["recovery"]["arguments"], expected)
        insufficient = diagnostics.error_result("commit", PixlError("stale_write", "refresh"), {})
        self.assertNotIn("operation", insufficient["recovery"])

    def test_secrets_payloads_and_unsafe_identities_are_not_echoed(self):
        secret = "Bearer DO_NOT_ECHO"
        args = {
            "connection": {"headers": {"Authorization": secret}}, "headers": secret,
            "details": {"secret": secret}, "arguments": {"api_key": secret},
            "schema": {"default": secret}, "discovery": {"evidence": secret},
            "authorization": {"scope": secret}, "root": "C:/private/root",
            "path": "../private/token", "store": "C:/private/root", "job_id": secret,
            "expect": secret, "asset_id": "queue.working", "requirements_hash": "e" * 64,
        }
        error = PixlError("input_schema", "arguments violate inputSchema", context={"headers": secret, "discovery": secret, "job_id": secret, "job_state": secret})
        result = diagnostics.error_result("pixl_job_prepare", error, args)
        self.assertEqual(result["identity"], {"asset_id": "queue.working", "requirements_hash": "e" * 64})
        rendered = json.dumps(result)
        self.assertNotIn(secret, rendered)
        self.assertNotIn("private", rendered)
        self.assertNotIn("headers", rendered)

    def test_malformed_operation_args_context_cannot_break_reporting(self):
        for operation in [None, {}, [], 3, "invalid operation"]:
            for args in [None, [], "secret", 3, {"job_id": {}, "path": []}]:
                error = PixlError("input_schema", "invalid schema")
                error.context = []
                result = diagnostics.error_result(operation, error, args)
                self.assertEqual(result["category"], "invalid_authoring")
                self.assertEqual(result["identity"], {})
        for path in ["C:relative", "C:/absolute", "\\rooted", "/rooted", "../escape", "work/../escape", "work/secret\nvalue", "work/\ud800"]:
            result = diagnostics.error_result("source", PixlError("source_hash", "changed"), {"path": path})
            self.assertEqual(result["identity"], {})
            self.assertNotIn("operation", result["recovery"])

    def test_file_failure_identifies_declared_file_separately_from_allocation(self):
        error = PixlError("caller_artifact_stale", "declared file changed", context={
            "path": "work/report.json", "expected_file_sha256": "a" * 64,
            "observed_file_sha256": "b" * 64,
        })
        result = diagnostics.error_result("plar_handoff", error, {"path": "other-plar.txt", "asset_id": "queue.working"})
        self.assertEqual(result["identity"], {
            "path": "work/report.json", "plar_path": "other-plar.txt", "asset_id": "queue.working",
            "expected_file_sha256": "a" * 64, "observed_file_sha256": "b" * 64,
        })
        self.assertEqual(result["recovery"]["action"], "reconcile_declared_files")
        self.assertNotIn("operation", result["recovery"])

    def test_real_pending_and_duplicate_dispatch_attach_observed_context_without_mutation(self):
        fixture = job_fixture.JobsTests("test_dispatch_cannot_repeat_or_reuse_stale_hash")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        fixture.prepare()

        def files():
            return {p.relative_to(fixture.root): p.read_bytes() for p in fixture.root.rglob("*") if p.is_file()}

        before = files()
        with self.assertRaises(PixlError) as prepared:
            fixture.prepare(id_="other")
        self.assertEqual(files(), before)
        self.assertEqual(prepared.exception.code, "job_pending")
        first = diagnostics.error_result("job-prepare", prepared.exception, {"store": ".pixl", "job": "other"})
        self.assertEqual(first["category"], "retained_work")
        self.assertEqual(first["identity"]["job_state"], "prepared")
        self.assertEqual(first["identity"]["job_id"], "job")

        dispatched = fixture.dispatch()
        before = files()
        with self.assertRaises(PixlError) as duplicate:
            fixture.dispatch()
        self.assertEqual(files(), before)
        self.assertEqual(duplicate.exception.code, "job_history")
        self.assertIn("dispatch requires prepared intent", duplicate.exception.detail)
        result = diagnostics.error_result("job-dispatch", duplicate.exception, {"store": ".pixl", "job": "job"})
        self.assertEqual(result["category"], "uncertain_remote_result")
        self.assertEqual(result["identity"]["state_hash"], dispatched["hash"])
        self.assertEqual(result["identity"]["task_id"], "task")
        self.assertEqual(result["recovery"]["operation"], "pixl_jobs")
        with self.assertRaises(PixlError) as pending:
            fixture.prepare(id_="other")
        self.assertEqual(files(), before)
        self.assertEqual(pending.exception.context["job_state"], "unknown")
        self.assertEqual(pending.exception.context["job_id"], "job")

    def test_actual_running_duplicate_does_not_claim_unknown_outcome(self):
        fixture = job_fixture.JobsTests("test_dispatch_cannot_repeat_or_reuse_stale_hash")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        fixture.prepare()
        fixture.dispatch()
        fixture.observe("running", "existing-remote")
        before = fixture.expected()
        with self.assertRaises(PixlError) as duplicate:
            jobs.dispatch(fixture.folder, before, "job", fixture.root)
        result = diagnostics.error_result("pixl_job_dispatch", duplicate.exception, {"store": ".pixl", "job_id": "job"})
        self.assertEqual(result["category"], "retained_work")
        self.assertEqual(result["identity"]["job_state"], "running")
        self.assertEqual(result["recovery"]["action"], "observe_existing_job")
        self.assertEqual(fixture.expected(), before)


if __name__ == "__main__":
    unittest.main()
