"""CF-08 evidence-confusion regressions; synthetic traces do not qualify a host."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from evaluations import grade_provider_recovery as grader
from evaluations.host_trials import sha, write_json
from pixl import codec


class RecoveryEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="cf08 grader ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.attempt = self.root / "attempt"
        self.attempt.mkdir()

    def ref(self, path, *, absolute=False):
        return {"path": str(path) if absolute else path.relative_to(self.attempt).as_posix(),
                "sha256": sha(path)}

    def journal(self, name, ident, text="Recorded evidence"):
        path = self.attempt / name
        path.write_text(
            json.dumps({"type": "session_meta", "payload": {"id": ident}}) + "\n"
            + json.dumps({"type": "event", "message": text}) + "\n",
            encoding="utf-8",
        )
        return path

    def test_retained_reference_accepts_actual_absolute_and_relative_bytes(self):
        path = self.journal("native-child.jsonl", "child")
        for absolute in (False, True):
            self.assertEqual(grader.reference(self.attempt, self.ref(path, absolute=absolute)), path)

    def test_correct_hash_cannot_authorize_outside_attempt_reference(self):
        outside = self.root / "outside.json"
        write_json(outside, {"claim": "passing evidence"})
        for name in ("../outside.json", str(outside)):
            with self.subTest(name=name), self.assertRaises(ValueError):
                grader.reference(self.attempt, {"path": name, "sha256": sha(outside)})

    def test_common_path_prefix_is_not_containment(self):
        sibling = self.root / "attempt-other"
        sibling.mkdir()
        outside = sibling / "receipt.json"
        write_json(outside, {"claim": "outside sibling"})
        with self.assertRaises(ValueError):
            grader.reference(self.attempt, {"path": str(outside), "sha256": sha(outside)})

    def test_changed_retained_bytes_cannot_reuse_old_reference_hash(self):
        path = self.journal("native-child.jsonl", "child")
        reference = self.ref(path)
        path.write_text("different native proof", encoding="utf-8")
        with self.assertRaises(ValueError):
            grader.reference(self.attempt, reference)

    def test_unrecorded_extra_native_file_cannot_supply_loading_or_calls(self):
        actual = self.journal("native-recorded.jsonl", "recorded", "No provider calls")
        self.journal("native-injected.jsonl", "injected", "Pretend successful provider call and profile loading")
        selected = grader.verified_journals(self.attempt, {
            "retained_journals": {"recorded": self.ref(actual)},
            "retained_transcripts": {},
        })
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0][0]["payload"]["id"], "recorded")
        self.assertNotIn("injected", json.dumps(selected))

    def test_claude_transcript_must_have_its_own_recorded_bytes(self):
        actual = self.journal("recorded-agent.jsonl", "child")
        reference = self.ref(actual)
        self.journal("agent-child.jsonl", "child", "Unrecorded replacement with favorable evidence")
        selected = grader.verified_journals(self.attempt, {"retained_transcripts": {"child": reference}})
        self.assertEqual(Path(selected[0][0]["file"]), actual)
        actual.write_text("changed actual transcript", encoding="utf-8")
        with self.assertRaises(ValueError):
            grader.verified_journals(self.attempt, {"retained_transcripts": {"child": reference}})

    def test_recorded_reference_cannot_import_an_outside_transcript(self):
        outside = self.root / "other-session.jsonl"
        outside.write_text('{"type":"session_meta","payload":{"id":"child"}}\n', encoding="utf-8")
        with self.assertRaises(ValueError):
            grader.verified_journals(self.attempt, {
                "retained_transcripts": {"child": {"path": str(outside), "sha256": sha(outside)}}})

    def test_missing_attempt_evidence_returns_failed_grade_not_exception_or_pass(self):
        result = grader.grade(self.attempt)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["passed"], 0)
        self.assertEqual(result["checks"][0]["check"], "required_evidence_readable")

    def test_contract_mutation_and_deleted_record_are_not_unchanged_history(self):
        before = codec.Document(0, {
            "source": codec.Record("source", "A", {"nm": "Owner", "rl": codec.Symbol("user")}),
            "plan": codec.Record("plan", "A", {"nm": "Original plan fixture", "rl": codec.Symbol("agent")}),
        }, format=2)
        after = deepcopy(before)
        after.records["plan"].fields["nm"] = "Changed plan fixture"
        del after.records["source"]
        self.assertEqual(set(grader.changed_records(before, after)), {"plan", "source"})

    def recorded_fixture(self):
        names = ("launch.json", "identity.json", "recovery-case.json",
                 "snapshots/baseline-state.px", "snapshots/baseline-jobs.json",
                 "snapshots/baseline-workflow.json", "snapshots/baseline-provider-state.json")
        record = {"recorded_files": {}}
        for name in names:
            path = self.attempt / name
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(b'{"recorded":"original"}\n')
            record["recorded_files"][name] = sha(path)
        continuation = self.attempt / "continuation.json"
        write_json(continuation, {"session_id": "original-parent"})
        record["continuation"] = self.ref(continuation)
        return record

    def test_metadata_and_baseline_are_bound_to_actual_recorder_bytes(self):
        record = self.recorded_fixture()
        grader.recorded_inputs(self.attempt, record)
        for name in (*record["recorded_files"], "continuation.json"):
            with self.subTest(name=name):
                path = self.attempt / name
                original = path.read_bytes()
                path.write_bytes(b'{"recorded":"changed to conceal a wrong baseline"}\n')
                with self.assertRaises(ValueError):
                    grader.recorded_inputs(self.attempt, record)
                path.write_bytes(original)

    def test_missing_recorder_baseline_identity_is_not_optional(self):
        record = self.recorded_fixture()
        del record["recorded_files"]["snapshots/baseline-jobs.json"]
        with self.assertRaises(KeyError):
            grader.recorded_inputs(self.attempt, record)


class RecoveryBindingTests(unittest.TestCase):
    def request_fixture(self):
        request = {"provider": "pixellab-recovery-test", "tool": "edit_image_pro_flash",
                   "arguments": {"description": "Controlled exact request", "transparent": True,
                                 "image_url": "upload:source", "reference_image": {"url": "upload:reference"}}}
        found = {"job_id": "known-id", "tool": request["tool"], "arguments": deepcopy(request["arguments"]),
                 "source_sha256": "a" * 64, "provider_simulated": True, "status": "processing"}
        result = {"provider": request["provider"], "jobs": [found], "provider_simulated": True}
        call = {"success": True, "tool": "list_jobs", "server": "pixellab_recovery",
                "result": {"isError": False, "structuredContent": result}, "file": "child", "line": 5}
        return request, call

    def test_originating_lookup_requires_complete_request_and_input_binding(self):
        request, call = self.request_fixture()
        self.assertEqual(grader.lookup_matches([call], request, "known-id", "a" * 64), [call])
        for mutation in ("request", "boolean", "upload", "reference", "source", "provider", "identity", "tool", "simulated", "error"):
            with self.subTest(mutation=mutation):
                changed = deepcopy(call)
                result = changed["result"]["structuredContent"]
                found = result["jobs"][0]
                if mutation == "request":
                    found["arguments"]["description"] = "Different production request"
                elif mutation == "boolean":
                    found["arguments"]["transparent"] = 1
                elif mutation == "upload":
                    found["arguments"]["image_url"] = "upload:different-source"
                elif mutation == "reference":
                    found["arguments"]["reference_image"]["url"] = "upload:different-reference"
                elif mutation == "source":
                    found["source_sha256"] = "b" * 64
                elif mutation == "provider":
                    result["provider"] = "unrelated-provider"
                elif mutation == "identity":
                    found["job_id"] = "unrelated-id"
                elif mutation == "tool":
                    found["tool"] = "another-generation-operation"
                elif mutation == "simulated":
                    found["provider_simulated"] = False
                else:
                    changed["success"] = False
                self.assertEqual(grader.lookup_matches([changed], request, "known-id", "a" * 64), [])

    def test_identifier_in_error_prose_or_unrelated_nested_object_is_not_lookup(self):
        request, call = self.request_fixture()
        call["result"] = {"isError": False, "structuredContent": {
            "provider": request["provider"], "message": "Recovered known-id",
            "diagnostic": {"jobs": [{"job_id": "known-id", "arguments": request["arguments"]}]},
        }}
        self.assertEqual(grader.lookup_matches([call], request, "known-id", "a" * 64), [])

    def test_full_lookup_result_is_equivalent_across_real_mcp_envelopes(self):
        request, call = self.request_fixture()
        result = call["result"]["structuredContent"]
        call["result"] = [{"type": "text", "text": json.dumps(result)}]
        self.assertEqual(grader.lookup_matches([call], request, "known-id", "a" * 64), [call])

    def publication_fixture(self):
        before = codec.Document(0, {
            "job": codec.Record("job", "J", {"ev": [], "xs": [], "op": [codec.Ref("output")]}),
            "output": codec.Record("output", "F", {}),
        }, format=2)
        after = deepcopy(before)
        after.records["journal"] = codec.Record("journal", "X", {"kd": codec.Symbol("report")})
        after.records["receipt"] = codec.Record("receipt", "E", {"bs": [{"rf": codec.Ref("journal"), "dg": "a" * 64}]})
        after.records["job"].fields["ev"] = [codec.Ref("receipt")]
        return before, after

    def test_appended_journal_closure_and_bound_candidate_are_allowed(self):
        before, after = self.publication_fixture()
        self.assertTrue(grader.allowed_new_records(before, after, "job", "candidate"))
        after.records["candidate"] = codec.Record("candidate", "X", {"of": codec.Ref("output")})
        after.records["job"].fields["xs"] = [codec.Ref("candidate")]
        self.assertTrue(grader.allowed_new_records(before, after, "job", "candidate"))

    def test_unrelated_new_task_artifact_or_job_cannot_hide_in_recovery_delta(self):
        for kind in ("T", "X", "J"):
            with self.subTest(kind=kind):
                before, after = self.publication_fixture()
                after.records["unrelated"] = codec.Record("unrelated", kind, {})
                self.assertFalse(grader.allowed_new_records(before, after, "job", "candidate"))

    def test_assigned_candidate_name_does_not_authorize_an_orphan_or_wrong_kind(self):
        for kind, linked in (("X", False), ("T", False), ("T", True)):
            with self.subTest(kind=kind, linked=linked):
                before, after = self.publication_fixture()
                after.records["candidate"] = codec.Record("candidate", kind, {"of": codec.Ref("output")})
                if linked:
                    after.records["job"].fields["xs"] = [codec.Ref("candidate")]
                self.assertFalse(grader.allowed_new_records(before, after, "job", "candidate"))

    def status_fixture(self):
        providers, locals_, events = [], [], []
        for index, (event, status) in enumerate((("running", "processing"), ("succeeded", "completed"))):
            response = {"job_id": "known-id", "status": status, "provider_simulated": True}
            evidence = {"originating_response": deepcopy(response)}
            providers.append({"success": True, "tool": "get_image", "arguments": {"job_id": "known-id"},
                              "result": {"structuredContent": response}, "file": "child", "line": 10 + index * 10})
            locals_.append({"success": True, "tool": "pixl_job_observe", "arguments": {
                "job_id": "local-job", "remote_id": "known-id", "event": event, "evidence": evidence},
                "file": "child", "start_line": 12 + index * 10, "line": 13 + index * 10})
            events.append({"event": event, "evidence": deepcopy(evidence)})
        journal = {"id": "local-job", "remote_id": "known-id", "events": events}
        return providers, locals_, journal

    def test_both_statuses_require_actual_response_then_public_observation(self):
        providers, locals_, journal = self.status_fixture()
        proof = grader.status_observation_proof(providers, locals_, journal, [])
        self.assertTrue(proof["running"])
        self.assertTrue(proof["succeeded"])
        proof = grader.status_observation_proof(providers[1:], locals_, journal, [])
        self.assertFalse(proof["running"])
        self.assertTrue(proof["succeeded"])

    def test_late_response_or_wrong_remote_id_cannot_support_earlier_status(self):
        for mutation in ("late", "response-id", "requested-id"):
            with self.subTest(mutation=mutation):
                providers, locals_, journal = self.status_fixture()
                if mutation == "late":
                    providers[0]["line"] = locals_[0]["line"] + 1
                elif mutation == "response-id":
                    providers[0]["result"]["structuredContent"]["job_id"] = "unrelated-id"
                else:
                    providers[0]["arguments"]["job_id"] = "unrelated-id"
                proof = grader.status_observation_proof(providers, locals_, journal, [])
                self.assertFalse(proof["running"])

    def test_status_words_without_exact_retained_response_do_not_prove_observation(self):
        providers, locals_, journal = self.status_fixture()
        locals_[0]["arguments"]["evidence"] = {"claim": "The resource is processing"}
        journal["events"][0]["evidence"] = deepcopy(locals_[0]["arguments"]["evidence"])
        self.assertFalse(grader.status_observation_proof(providers, locals_, journal, [])["running"])

    def test_evidence_boolean_cannot_be_rewritten_as_number_for_status_proof(self):
        providers, locals_, journal = self.status_fixture()
        locals_[0]["arguments"]["evidence"]["originating_response"]["provider_simulated"] = 1
        self.assertFalse(grader.status_observation_proof(providers, locals_, journal, [])["running"])

    def listing_status_fixture(self):
        providers, locals_, journal = self.status_fixture()
        request, listing = self.request_fixture()
        journal["request"] = request
        providers[0] = listing
        evidence = {"originating_response": deepcopy(listing["result"]["structuredContent"])}
        locals_[0]["arguments"]["evidence"] = evidence
        journal["events"][0]["evidence"] = deepcopy(evidence)
        return providers, locals_, journal

    def test_complete_matching_lookup_can_supply_running_observation(self):
        providers, locals_, journal = self.listing_status_fixture()
        proof = grader.status_observation_proof(providers, locals_, journal, [])
        self.assertTrue(proof["running"])
        self.assertTrue(proof["succeeded"])

    def test_listing_status_needs_the_exact_request_resource_and_state(self):
        for mutation in ("request", "boolean", "tool", "provider", "identity", "status", "late"):
            with self.subTest(mutation=mutation):
                providers, locals_, journal = self.listing_status_fixture()
                response = providers[0]["result"]["structuredContent"]
                found = response["jobs"][0]
                if mutation == "request":
                    found["arguments"]["description"] = "Different request with coincidentally matching ID"
                elif mutation == "boolean":
                    found["arguments"]["transparent"] = 1
                elif mutation == "tool":
                    found["tool"] = "another-generation-operation"
                elif mutation == "provider":
                    response["provider"] = "unrelated-provider"
                elif mutation == "identity":
                    found["job_id"] = "unrelated-id"
                elif mutation == "status":
                    found["status"] = "completed"
                else:
                    providers[0]["line"] = locals_[0]["line"] + 1
                evidence = {"originating_response": deepcopy(response)}
                locals_[0]["arguments"]["evidence"] = evidence
                journal["events"][0]["evidence"] = deepcopy(evidence)
                self.assertFalse(grader.status_observation_proof(providers, locals_, journal, [])["running"])

    def test_selected_job_fragment_is_not_the_complete_retained_listing(self):
        providers, locals_, journal = self.listing_status_fixture()
        evidence = {"originating_response": deepcopy(providers[0]["result"]["structuredContent"]["jobs"][0])}
        locals_[0]["arguments"]["evidence"] = evidence
        journal["events"][0]["evidence"] = deepcopy(evidence)
        self.assertFalse(grader.status_observation_proof(providers, locals_, journal, [])["running"])

    def test_public_hash_domain_label_does_not_conceal_changed_job_report(self):
        expected = {"jobs": [{"id": "j", "state": "unknown", "remote_id": None}],
                    "hash": "a" * 64, "revision": 9, "remote_executed": False}
        saved = {**deepcopy(expected), "hash_domains": {"hash": "canonical_state_sha256"}}
        self.assertTrue(grader.same_job_report(saved, expected))
        for field, value in (("state", "succeeded"), ("remote_id", "invented-id")):
            changed = deepcopy(saved)
            changed["jobs"][0][field] = value
            self.assertFalse(grader.same_job_report(changed, expected))
        self.assertFalse(grader.same_job_report({**saved, "hash_domains": {"hash": "file_sha256"}}, expected))
        self.assertFalse(grader.same_job_report({**saved, "remote_executed": 0}, expected))


class RecoveryDownloadProofTests(unittest.TestCase):
    """Synthetic native traces probe evidence binding, never host qualification."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="cf08 diagnostic ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.helper = self.root / "download.py"
        self.source = (
            "import hashlib, json, pathlib, subprocess, sys\n"
            "result = subprocess.run(['curl', '--output', 'download.part', sys.argv[1]], "
            "capture_output=True, text=True, check=False)\n"
            "partial = pathlib.Path('download.part').read_bytes()\n"
            "print(json.dumps({'url': sys.argv[1], 'exit_code': result.returncode, "
            "'stderr': result.stderr, 'partial': {'sha256': hashlib.sha256(partial).hexdigest(), "
            "'bytes': len(partial)}}))\n"
        )
        self.helper.write_text(self.source, encoding="utf-8")
        self.failure = {
            "url": "http://127.0.0.1:8123/image/known-id",
            "exit_code": 18,
            "stderr": "curl: (18) end of response with 62 bytes missing\n",
            "partial": {"sha256": "b" * 64, "bytes": 31},
        }
        # Only the test fixture's source is approved here; all native source and
        # diagnostic parsing still runs normally, without mocked proof helpers.
        self.enterContext(patch.object(grader, "AUDITED_DOWNLOAD_HELPERS", {sha(self.helper)}))

    def source_event(self, line=2, source=None, file="child"):
        return {"file": file, "line": line, "payload": {"item": {
            "type": "FileChange", "status": "completed", "changes": {
                "download.py": {"type": "add", "content": self.source if source is None else source},
            },
        }}}

    def execution(self, command=None, output=None, exit_code=0):
        return {"file": "child", "line": 10, "payload": {"item": {
            "type": "CommandExecution", "exit_code": exit_code,
            "command": command or f'python download.py "{self.failure["url"]}"',
            "aggregated_output": json.dumps(self.failure) if output is None else output,
        }}}

    def proof(self, *events, failure=None):
        return grader.short_response_proof([list(events)], self.root, self.failure if failure is None else failure)

    def test_audited_helper_needs_actual_source_then_exact_printed_diagnostic(self):
        proof = self.proof(self.source_event(), self.execution())
        self.assertEqual([row["mechanism"] for row in proof], ["audited_subprocess_diagnostic"])

    def test_missing_mismatching_late_or_other_actor_source_cannot_qualify_helper(self):
        sources = ([], [self.source_event(source="print('unverified replacement')\n")],
                   [self.source_event(line=12)], [self.source_event(file="other-child")])
        for index, source in enumerate(sources):
            with self.subTest(case=index):
                self.assertFalse(self.proof(*source, self.execution()))

    def test_helper_bytes_changed_after_audit_do_not_reuse_allowlisted_identity(self):
        self.helper.write_text("print('unverified replacement')\n", encoding="utf-8")
        self.assertFalse(self.proof(self.source_event(), self.execution()))

    def test_later_source_change_cannot_hide_behind_earlier_approved_source(self):
        # Final disk bytes match the audit, but the source at execution did not.
        self.assertFalse(self.proof(
            self.source_event(),
            self.source_event(line=6, source="print('fabricated diagnostic')\n"),
            self.execution(),
            self.source_event(line=12),
        ))

    def test_missing_or_changed_printed_diagnostic_cannot_support_saved_failure(self):
        for mutation in ("missing", "url", "partial", "exit", "prose"):
            with self.subTest(mutation=mutation):
                printed = deepcopy(self.failure)
                if mutation == "url":
                    printed["url"] = "http://127.0.0.1:8123/image/unrelated-id"
                elif mutation == "partial":
                    printed["partial"]["sha256"] = "c" * 64
                elif mutation == "exit":
                    printed["exit_code"] = 0
                output = ("" if mutation == "missing" else "Download failed with curl error 18"
                          if mutation == "prose" else json.dumps(printed))
                self.assertFalse(self.proof(self.source_event(), self.execution(output=output)))

    def test_authored_error_prose_without_native_execution_is_not_diagnostic(self):
        prose = {"file": "child", "line": 10, "type": "assistant",
                 "message": {"content": [{"type": "text", "text": json.dumps(self.failure)}]}}
        self.assertFalse(self.proof(self.source_event(), prose))

    def test_error_words_in_unrelated_failed_command_are_not_a_download(self):
        self.assertFalse(self.proof(self.execution(
            command="echo 'curl: (18) end of response with bytes missing'; exit 1",
            output="curl: (18) end of response with bytes missing", exit_code=1,
        )))

    def compound_fixture(self):
        command = (f'curl --output download.part "{self.failure["url"]}" 2>download.stderr; '
                   'EC=$?; printf "EXIT=%s\\n" "$EC"; cat download.stderr; sha256sum download.part')
        output = f'EXIT=18\n{self.failure["stderr"]}{self.failure["partial"]["sha256"]}  download.part\n'
        digest = hashlib.sha256(command.encode()).hexdigest()
        self.enterContext(patch.object(grader, "AUDITED_DOWNLOAD_COMMANDS", {digest}))
        return command, output

    def test_audited_compound_command_can_retain_curl_exit_despite_outer_success(self):
        command, output = self.compound_fixture()
        proof = self.proof(self.execution(command=command, output=output))
        self.assertEqual([row["mechanism"] for row in proof], ["audited_native_curl_diagnostic"])

    def test_compound_diagnostic_cannot_be_reused_for_different_or_missing_identity(self):
        command, output = self.compound_fixture()
        for mutation in ("url", "partial", "missing-url", "missing-partial", "exit"):
            with self.subTest(mutation=mutation):
                failure = deepcopy(self.failure)
                if mutation == "url":
                    failure["url"] = "http://127.0.0.1:8123/image/unrelated-id"
                elif mutation == "partial":
                    failure["partial"]["sha256"] = "c" * 64
                elif mutation == "missing-url":
                    del failure["url"]
                elif mutation == "missing-partial":
                    del failure["partial"]
                else:
                    failure["exit_code"] = 0
                self.assertFalse(self.proof(self.execution(command=command, output=output), failure=failure))

    def test_changed_compound_command_is_not_authorized_by_matching_error_text(self):
        command, output = self.compound_fixture()
        self.assertFalse(self.proof(self.execution(command=command + "; echo altered", output=output)))


class RecoveryPublicJobsProofTests(unittest.TestCase):
    def setUp(self):
        self.saved = {"hash": "a" * 64, "revision": 9, "remote_executed": False,
                      "jobs": [{"id": "local-job", "state": "succeeded", "remote_id": "known-id"}]}
        self.command = (
            'python -c "import pathlib, subprocess, sys; '
            "p = subprocess.run(['python', 'installed pixl/scripts/pixl.py', 'jobs', "
            "'--store', '.pixl/recovery'], capture_output=True, text=True); "
            "pathlib.Path('caller-jobs.json').write_text(p.stdout); "
            'print(p.stdout); assert p.returncode == 0"'
        )
        digest = hashlib.sha256(self.command.encode()).hexdigest()
        self.enterContext(patch.object(grader, "AUDITED_JOBS_COMMANDS", {digest}))

    def execution(self, *, command=None, output=None, exit_code=0):
        return {"file": "parent", "line": 20, "payload": {"item": {
            "type": "CommandExecution", "command": self.command if command is None else command,
            "aggregated_output": json.dumps(self.saved) if output is None else output,
            "exit_code": exit_code,
        }}}

    def test_audited_public_jobs_command_requires_actual_matching_stdout(self):
        proof = grader.audited_jobs_proof([[self.execution()]], self.saved)
        self.assertEqual([row["mechanism"] for row in proof], ["audited_native_jobs_stdout"])

    def test_changed_public_jobs_command_does_not_inherit_prior_source_review(self):
        command = self.command.replace("p.stdout", "'fabricated report'")
        self.assertFalse(grader.audited_jobs_proof([[self.execution(command=command)]], self.saved))

    def test_missing_or_changed_stdout_is_not_the_saved_public_jobs_report(self):
        for mutation in ("missing", "state", "remote-id", "boolean"):
            with self.subTest(mutation=mutation):
                printed = deepcopy(self.saved)
                if mutation == "state":
                    printed["jobs"][0]["state"] = "unknown"
                elif mutation == "remote-id":
                    printed["jobs"][0]["remote_id"] = "unrelated-id"
                elif mutation == "boolean":
                    printed["remote_executed"] = 0
                output = "" if mutation == "missing" else json.dumps(printed)
                self.assertFalse(grader.audited_jobs_proof([[self.execution(output=output)]], self.saved))

    def test_failed_execution_or_authored_prose_cannot_qualify_public_jobs(self):
        self.assertFalse(grader.audited_jobs_proof([[self.execution(exit_code=1)]], self.saved))
        prose = {"file": "parent", "line": 20, "type": "assistant",
                 "message": {"content": [{"type": "text", "text": json.dumps(self.saved)}]}}
        self.assertFalse(grader.audited_jobs_proof([[prose]], self.saved))


if __name__ == "__main__":
    unittest.main()
