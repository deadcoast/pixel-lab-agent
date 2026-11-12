"""Synthetic negative proofs for CF-10 grading; no provider execution or art claims."""
from __future__ import annotations

import base64
import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from PIL import Image

from evaluations import native_production_grade as grade
from pixl import codec


def mcp(server, tool, arguments, result, start, finish, *, success=True):
    item = {"id": f"call-{start}", "type": "McpToolCall", "server": server, "tool": tool, "arguments": arguments}
    return [
        {"file": "native.jsonl", "line": start, "timestamp": f"2026-11-12T08:00:{start:02d}+00:00", "payload": {"type": "item_started", "item": {**item, "status": "in_progress"}}},
        {"file": "native.jsonl", "line": finish, "timestamp": f"2026-11-12T08:00:{finish:02d}+00:00", "payload": {"type": "item_completed", "item": {**item, "status": "completed", "result": {"isError": not success, "structuredContent": result}}}},
    ]


def journal():
    return {"intent": {"job": "production.job", "request": {"tool": "create_image_pro_flash", "provider": "pixellab-official", "arguments": {"description": "Synthetic grading request"}, "authorization": {"evidence": {}}, "discovery": {"evidence": {}}}},
            "intent_sha256": "a" * 64, "remote_id": "synthetic-returned-id", "events": [{"event": "dispatch", "recorded_at": "2026-11-12T08:00:01+00:00", "evidence": {"origin": "local_dispatch_claim"}}]}


def native_trace(value):
    local = {"job": {"id": value["intent"]["job"], "intent_sha256": value["intent_sha256"], "state": "unknown", "events": value["events"][:1]}}
    return mcp("pixl_local", "pixl_job_dispatch", {"job_id": "production.job"}, local, 2, 3) + mcp("pixellab", value["intent"]["request"]["tool"], value["intent"]["request"]["arguments"], {"image_id": value["remote_id"], "status": "queued"}, 4, 5)


def ref(root, name):
    return {"path": name, "sha256": grade.sha(root / name)}


class NativeProductionTraceTests(unittest.TestCase):
    def test_paired_native_call_preserves_request_time_and_result(self):
        rows = native_trace(journal())
        calls = grade.tool_calls([rows])
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[1]["start_line"], 4)
        self.assertEqual(calls[1]["line"], 5)
        self.assertTrue(calls[1]["success"])

    def test_claude_requires_real_paired_tool_result(self):
        start = {"type": "assistant", "file": "child", "line": 1, "timestamp": "2026-11-12T08:00:01Z", "message": {"content": [{"type": "tool_use", "id": "x", "name": "mcp__pixellab__create_image_pro_flash", "input": {"description": "synthetic"}}]}}
        stop = {"type": "user", "file": "child", "line": 2, "message": {"content": [{"type": "tool_result", "tool_use_id": "x", "content": [{"type": "text", "text": '{"image_id":"synthetic"}'}]}]}}
        self.assertEqual(grade.tool_calls([[start]]), [])
        self.assertTrue(grade.tool_calls([[start, stop]])[0]["success"])
        stop["message"]["content"][0]["is_error"] = True
        self.assertFalse(grade.tool_calls([[start, stop]])[0]["success"])

    def test_exact_native_dispatch_then_official_call_passes(self):
        value = journal()
        rows = native_trace(value)
        self.assertTrue(grade.job_proof(value, grade.tool_calls([rows]), [rows])["pass"])

    def test_official_qualified_tool_matches_bare_native_name_only(self):
        value = journal()
        rows = native_trace(value)
        value["intent"]["request"]["tool"] = "mcp__pixellab__create_image_pro_flash"
        self.assertTrue(grade.job_proof(value, grade.tool_calls([rows]), [rows])["pass"])
        value["intent"]["request"]["tool"] = "mcp__fake__create_image_pro_flash"
        self.assertFalse(grade.job_proof(value, grade.tool_calls([rows]), [rows])["pass"])

    def test_local_journal_and_authorship_cannot_fabricate_provider_execution(self):
        value = journal()
        self.assertFalse(grade.job_proof(value, [], [])["pass"])

    def test_wrong_provider_arguments_or_identifier_rejects_binding(self):
        for mutation in ("arguments", "identity", "server", "error"):
            with self.subTest(mutation=mutation):
                value = journal()
                rows = native_trace(value)
                item = rows[-1]["payload"]["item"]
                if mutation == "arguments":
                    item["arguments"] = {"description": "different"}
                elif mutation == "identity":
                    item["result"]["structuredContent"]["image_id"] = "different"
                elif mutation == "server":
                    item["server"] = "fake-provider"
                else:
                    item["result"]["isError"] = True
                self.assertFalse(grade.job_proof(value, grade.tool_calls([rows]), [rows])["pass"])

    def test_dispatch_after_provider_cannot_be_backdated_by_journal(self):
        value = journal()
        rows = native_trace(value)
        rows[1]["line"] = 7
        self.assertFalse(grade.job_proof(value, grade.tool_calls([rows]), [rows])["pass"])

    def test_late_journal_timestamp_does_not_override_early_native_receipt(self):
        value = journal()
        value["events"][0]["recorded_at"] = "2026-11-12T08:00:30Z"
        rows = native_trace(value)
        self.assertFalse(grade.job_proof(value, grade.tool_calls([rows]), [rows])["pass"])

    def test_simulation_evidence_rejects_remote_claim_but_schema_names_do_not(self):
        value = journal()
        value["intent"]["request"]["schema"] = {"properties": {"fixture": {"const": True}}}
        self.assertFalse(grade.simulated(value))
        value["events"][0]["evidence"]["provider_simulated"] = True
        self.assertTrue(grade.simulated(value))

    def test_complete_responses_match_across_mcp_wrappers(self):
        value = {"image_id": "synthetic-id", "status": "queued", "metadata": {"width": 16}}
        self.assertTrue(grade.response_matches(value, {"content": [{"type": "text", "text": json.dumps(value)}], "isError": False}))
        changed = copy.deepcopy(value)
        changed["image_id"] = "forged"
        self.assertFalse(grade.response_matches(changed, value))
        self.assertFalse(grade.response_matches({"width": 16}, value))

    def test_cross_file_order_requires_real_timestamps(self):
        a = {"file": "parent", "line": 3, "timestamp": "2026-11-12T08:00:03Z"}
        b = {"file": "child", "line": 5, "start_line": 4, "timestamp": "2026-11-12T08:00:04Z"}
        self.assertTrue(grade.before(a, b, [[a]]))
        a.pop("timestamp")
        self.assertFalse(grade.before(a, b, [[a]]))

    def test_naive_or_invalid_clock_is_not_temporal_proof(self):
        for value in (None, "yesterday", "2026-11-12T08:00:00"):
            self.assertIsNone(grade.stamp(value))


class NativeProductionArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_report_layout_is_not_coupled_to_tm07_fields(self):
        self.assertEqual(grade.report_fields({"status": "partial", "refs": {"handoff_ref": "x"}})["handoff_ref"], "x")
        with self.assertRaises(ValueError):
            grade.report_fields({"handoff_ref": "x", "refs": {"handoff_ref": "y"}})

    def test_literal_or_hash_criterion_coverage_and_missing_row(self):
        document = SimpleNamespace(records={"q.one": codec.Record("q.one", "Q", {"ck": "Preserve original identity."}), "q.two": codec.Record("q.two", "Q", {"ck": "Use transparent pixels."})})
        comparison = {"q.one": {"check": "Preserve original identity."}, "q.two": {"record_sha256": codec.record_hash(document.records["q.two"])}}
        self.assertTrue(grade.criteria_coverage(comparison, document, set(document.records))["pass"])
        del comparison["q.two"]
        self.assertEqual(grade.criteria_coverage(comparison, document, set(document.records))["missing"], ["q.two"])
        comparison["q.two"] = {"check": "Use opaque pixels."}
        self.assertFalse(grade.criteria_coverage(comparison, document, set(document.records))["pass"])

    def ready(self):
        (self.root / "assets").mkdir()
        (self.root / grade.INPUTS).mkdir(parents=True)
        image = Image.new("RGBA", (16, 16))
        image.putpixel((3, 3), (50, 180, 210, 255))
        image.save(self.root / grade.INPUTS / "original-ready.png")
        image.putpixel((4, 4), (50, 180, 210, 255))
        image.save(self.root / "assets/ready-confirmed.png")
        return [ref(self.root, "assets/ready-confirmed.png")]

    def test_artifact_geometry_does_not_invent_output_difference_requirement(self):
        delivered = self.ready()
        self.assertEqual(grade.delivered_errors(self.root, "queue-ready", delivered), [])
        (self.root / "assets/ready-confirmed.png").write_bytes((self.root / grade.INPUTS / "original-ready.png").read_bytes())
        errors = grade.delivered_errors(self.root, "queue-ready", [ref(self.root, "assets/ready-confirmed.png")])
        self.assertEqual(errors, [])  # Real native generation/import is a separate mandatory proof.

    def test_source_bound_plan_maps_local_ids_by_exact_literal_and_contract(self):
        document = SimpleNamespace(records={"q.full": codec.Record("q.full", "Q", {"nm": "local", "ck": "Exact criterion.", "dm": codec.Symbol("visual"), "md": codec.Symbol("visual")})})
        plan = {"criteria": [{"id": "local", "check": "Exact criterion.", "domain": "visual", "mode": "visual", "sources": [{"path": "BRIEF.md", "locator": "line 1"}], "authority": "requirement"}]}
        path = self.root / "plan.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        comparison = {"criteria": ref(self.root, "plan.json"), "criterion_comparisons": [{"criterion": "local", "finding": "Scoped comparison."}]}
        self.assertTrue(grade.criteria_coverage(comparison, document, {"q.full"}, self.root)["pass"])
        for field, wrong in (("check", "Changed criterion."), ("domain", "mechanical"), ("id", "full")):
            broken = copy.deepcopy(plan)
            broken["criteria"][0][field] = wrong
            path.write_text(json.dumps(broken), encoding="utf-8")
            comparison["criteria"] = ref(self.root, "plan.json")
            self.assertFalse(grade.criteria_coverage(comparison, document, {"q.full"}, self.root)["pass"])

    def test_inline_image_must_be_emitted_not_merely_returned_or_mentioned(self):
        delivered = self.ready()
        raw = (self.root / delivered[0]["path"]).read_bytes()
        block = {"type": "input_image", "image_url": "data:image/png;base64," + base64.b64encode(raw).decode()}
        row = {"file": "native", "line": 1, "payload": {"type": "custom_tool_call_output", "output": [block]}}
        self.assertIn(delivered[0]["sha256"], grade.actual_image_views([[row]], self.root))
        row["payload"]["type"] = "custom_tool_call"
        self.assertNotIn(delivered[0]["sha256"], grade.actual_image_views([[row]], self.root))
        row["payload"]["type"] = "custom_tool_call_output"
        block["type"] = "input_text"
        self.assertNotIn(delivered[0]["sha256"], grade.actual_image_views([[row]], self.root))

    def test_repeated_local_criteria_require_the_correct_output(self):
        criterion = {"id": "shape", "check": "Preserve shape.", "domain": "visual", "mode": "visual", "sources": [{"path": "BRIEF.md"}], "authority": "requirement"}
        plan = {"outputs": [{"id": name, "criteria": [criterion]} for name in ("east", "west")]}
        (self.root / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
        records = {f"criterion.{name}.shape": codec.Record(f"criterion.{name}.shape", "Q", {"nm": "shape", "ck": "Preserve shape.", "dm": codec.Symbol("visual"), "md": codec.Symbol("visual")}) for name in ("east", "west")}
        document = SimpleNamespace(records=records)
        comparison = {"criteria": ref(self.root, "plan.json"), "rows": [{"output": name, "criterion": "shape"} for name in ("east", "west")]}
        self.assertTrue(grade.criteria_coverage(comparison, document, set(records), self.root)["pass"])
        comparison["rows"].pop()
        self.assertEqual(grade.criteria_coverage(comparison, document, set(records), self.root)["missing"], ["criterion.west.shape"])

    def test_successful_exact_native_file_creation_is_authorship(self):
        path = self.root / "comparison.json"
        path.write_text('{"status":"consistent"}\n', encoding="utf-8")
        item = {"type": "FileChange", "status": "completed", "changes": {str(path): {"type": "add", "content": path.read_text()}}}
        rows = [[{"file": "parent", "line": 1, "payload": {"item": item}}]]
        self.assertTrue(grade.authored_file_proof(rows, path))
        item["status"] = "failed"
        self.assertFalse(grade.authored_file_proof(rows, path))
        item["status"] = "completed"
        item["changes"][str(path)]["content"] = '{"status":"different"}'
        self.assertFalse(grade.authored_file_proof(rows, path))

    def test_encrypted_transport_needs_exact_authorship_matching_receipt_and_bound_read(self):
        (self.root / "plan.json").write_text("{}", encoding="utf-8")
        comparison = {"status": "consistent", "criteria": ref(self.root, "plan.json")}
        path = self.root / "COMPARISON.json"
        path.write_text(json.dumps(comparison), encoding="utf-8")
        parent = [{"file": "parent", "line": 1, "timestamp": "2026-11-12T08:00:01Z", "payload": {"item": {"type": "FileChange", "status": "completed", "changes": {str(path): {"type": "add", "content": path.read_text()}}}}},
                  {"file": "parent", "line": 2, "timestamp": "2026-11-12T08:00:02Z", "payload": {"type": "function_call", "name": "send_message", "arguments": json.dumps({"target": "pixl", "message": "encrypted-opaque-token"})}}]
        child = [{"file": "child", "line": 3, "timestamp": "2026-11-12T08:00:03Z", "payload": {"type": "agent_message", "recipient": "/root/pixl", "content": [{"type": "encrypted_content", "encrypted_content": "encrypted-opaque-token"}]}},
                 {"file": "child", "line": 4, "timestamp": "2026-11-12T08:00:04Z", "payload": {"item": {"type": "CommandExecution", "id": "read", "command": "Get-Content COMPARISON.json -TotalCount 10", "exit_code": 0, "aggregated_output": '"consistent" ' + comparison["criteria"]["sha256"]}}}]
        proof = grade.comparison_communication([parent], [child], path)
        self.assertTrue(proof["caller"] and proof["child"])
        self.assertIn("not plaintext", proof["transport_limit"])
        for mutation in ("receipt", "target", "digest", "authorship"):
            bad_parent, bad_child = copy.deepcopy(parent), copy.deepcopy(child)
            if mutation == "receipt":
                bad_child[0]["payload"]["content"][0]["encrypted_content"] = "different"
            elif mutation == "target":
                bad_child[0]["payload"]["recipient"] = "/root/other"
            elif mutation == "digest":
                bad_child[1]["payload"]["item"]["aggregated_output"] = '"consistent"'
            else:
                bad_parent[0]["payload"]["item"]["status"] = "failed"
            self.assertFalse(grade.comparison_communication([bad_parent], [bad_child], path)["child"])

    def test_exact_file_reference_tampering_raises(self):
        delivered = self.ready()
        (self.root / "assets/ready-confirmed.png").write_bytes(b"changed")
        with self.assertRaises(ValueError):
            grade.delivered_errors(self.root, "queue-ready", delivered)

    def test_missing_or_extra_delivered_destination_fails(self):
        delivered = self.ready()
        self.assertTrue(grade.delivered_errors(self.root, "queue-ready", []))
        self.assertTrue(grade.delivered_errors(self.root, "queue-ready", delivered * 2))

    def test_valid_extra_retained_artifact_is_not_an_extra_destination(self):
        delivered = self.ready()
        (self.root / "retained.png").write_bytes((self.root / "assets/ready-confirmed.png").read_bytes())
        self.assertEqual(grade.delivered_errors(self.root, "queue-ready", [*delivered, ref(self.root, "retained.png")]), [])

    def test_grouped_handoff_keeps_caller_view_and_exact_reference(self):
        (self.root / "caller.json").write_text("{}", encoding="utf-8")
        (self.root / "full.json").write_text("{}", encoding="utf-8")
        value = {"handoff_ref": {"caller_view": ref(self.root, "caller.json"), "full": ref(self.root, "full.json")}}
        self.assertEqual(grade.named_ref(value, "handoff_ref", self.root), ref(self.root, "caller.json"))

    def test_independent_review_must_bind_exact_state_comparison_and_pixels(self):
        delivered = self.ready()
        (self.root / "state.px").write_text("synthetic state", encoding="utf-8")
        (self.root / "comparison.json").write_text("{}", encoding="utf-8")
        (self.root / "destination.png").write_bytes((self.root / "assets/ready-confirmed.png").read_bytes())
        state, comparison = ref(self.root, "state.px"), ref(self.root, "comparison.json")
        review = {"case": "queue-ready", "state_ref": state, "comparison_ref": comparison, "delivered_files": delivered,
                  "criteria_authority_pass": True, "art_pass": True, "destination_visual_pass": True, "inspected_images": [*delivered, ref(self.root, "destination.png")],
                  "rationale": "Synthetic receipt for parser testing only."}
        self.assertEqual(grade.review_errors(self.root, review, "queue-ready", state, comparison, delivered), [])
        review["art_pass"] = "true"
        self.assertTrue(grade.review_errors(self.root, review, "queue-ready", state, comparison, delivered))
        review["art_pass"] = True
        review["state_ref"] = {**state, "sha256": "0" * 64}
        self.assertTrue(grade.review_errors(self.root, review, "queue-ready", state, comparison, delivered))

    def test_changed_or_unpinned_checker_is_never_executed(self):
        (self.root / "renderer-native").mkdir()
        (self.root / "renderer-native/check.py").write_text("raise RuntimeError('must not execute')", encoding="utf-8")
        for inputs in ({}, {"renderer-native/check.py": "0" * 64}):
            with self.subTest(inputs=inputs), self.assertRaises(ValueError):
                grade.renderer_check(self.root, {"inputs": inputs}, {}, "robot-directions")

    def test_missing_attempt_keeps_explicit_pending_evidence(self):
        result = grade.grade(self.root)
        self.assertEqual(result["status"], "review_required")
        self.assertIn("attempt_inputs_readable", result["pending"])
        self.assertEqual(result["passed"], 0)

    def test_response_files_must_match_native_bytes_not_self_claims(self):
        value = journal()
        rows = native_trace(value)
        (self.root / "arguments.json").write_text(json.dumps(value["intent"]["request"]["arguments"]), encoding="utf-8")
        (self.root / "response.json").write_text(json.dumps({"image_id": value["remote_id"], "status": "queued"}), encoding="utf-8")
        operations = [{"job": "production.job", "arguments_ref": ref(self.root, "arguments.json"), "response_ref": ref(self.root, "response.json")}]
        self.assertTrue(grade.response_bindings(self.root, operations, [value], grade.tool_calls([rows]))[0]["pass"])
        (self.root / "response.json").write_text(json.dumps({"image_id": value["remote_id"], "status": "invented"}), encoding="utf-8")
        operations[0]["response_ref"] = ref(self.root, "response.json")
        self.assertFalse(grade.response_bindings(self.root, operations, [value], grade.tool_calls([rows]))[0]["pass"])

    def test_complete_saved_response_wrapper_requires_exact_tool_and_arguments(self):
        value = journal()
        native = grade.tool_calls([native_trace(value)])
        args = value["intent"]["request"]["arguments"]
        (self.root / "args.json").write_text(json.dumps(args), encoding="utf-8")
        wrapper = {"tool": "mcp__pixellab__create_image_pro_flash", "arguments": args, "response": native[-1]["result"]}
        path = self.root / "response.json"
        for mutation in (None, "tool", "arguments", "response"):
            data = copy.deepcopy(wrapper)
            if mutation == "tool":
                data["tool"] = "mcp__fake__create_image_pro_flash"
            elif mutation == "arguments":
                data["arguments"] = {}
            elif mutation == "response":
                data["response"]["structuredContent"]["status"] = "forged"
            path.write_text(json.dumps(data), encoding="utf-8")
            operations = [{"job": "production.job", "arguments_ref": ref(self.root, "args.json"), "response_ref": ref(self.root, "response.json")}]
            self.assertEqual(grade.response_bindings(self.root, operations, [value], native)[0]["pass"], mutation is None)

    def test_native_download_and_import_require_exact_dataflow(self):
        path = self.root / "download.png"
        path.write_bytes(b"synthetic downloaded bytes")
        document = SimpleNamespace(records={"candidate": codec.Record("candidate", "X", {"dg": grade.sha(path)})})
        remote = {"server": "pixellab", "success": True, "result": {"download_url": "https://api.pixellab.ai/synthetic/image.png"}}
        download = {"file": "native.jsonl", "line": 2, "payload": {"item": {"type": "CommandExecution", "id": "dl", "command": f'curl -L https://api.pixellab.ai/synthetic/image.png -o "{path}"', "exit_code": 0, "aggregated_output": ""}}}
        imported = mcp("pixl_local", "pixl_job_import", {"candidate_id": "candidate", "path": "download.png"}, {"imported": True}, 4, 5)
        trace = [download, *imported]
        self.assertTrue(grade.retrieval_proofs([trace], self.root, document, [remote])[0]["pass"])
        download["payload"]["item"]["command"] = 'echo ' + download["payload"]["item"]["command"]
        self.assertFalse(grade.retrieval_proofs([trace], self.root, document, [remote])[0]["pass"])


if __name__ == "__main__":
    unittest.main()
