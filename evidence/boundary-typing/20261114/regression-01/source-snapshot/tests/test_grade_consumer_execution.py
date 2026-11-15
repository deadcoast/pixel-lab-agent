"""Frozen renderer provenance and actual phase evidence cannot be replaced by claims."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from evaluations import grade_consumer_execution as grader
from evaluations.host_trials import sha, write_json


def phase_fixture():
    phases, facts = [], {}
    cells = ("statusCell@1", "statusCell@3", "compactStatus@1", "compactStatus@3")
    for name in grader.PHASES:
        reduced = name in ("reduced", "initially-reduced")
        switches = [] if name in ("normal-start", "initially-reduced") else [{"from": "normal", "to": "reduced"}]
        if name == "normal-restored":
            switches.append({"from": "reduced", "to": "normal"})
        phases.append({"name": name, "sessionId": "second" if name == "initially-reduced" else "first",
                       "status": "observed", "motion": "reduced" if reduced else "normal",
                       "initialMotion": "reduced" if name == "initially-reduced" else "normal",
                       "preferenceEvents": switches, "frameCount": 3})
        facts[name] = {"status": "observed", "sample_count": 30, "switches": len(switches),
                       "reconciliations": len(switches), "counts": {cell: {
                           "frames": [2] if reduced else [0, 1, 2], "transitions": 0 if reduced else 6,
                           "wraps": 0 if reduced else 2, "skips": 0, "last": 2 if reduced else 0}
                           for cell in cells}}
    return {"phases": phases}, {"facts": {"phases": facts, "pixel_checks": 120, "source_checks": 12, "clock_checks": 120}}


def viewing_fixture():
    capture, _ = phase_fixture()
    cells = [{"consumer": consumer, "scale": scale, "state": "running", "geometryMatches": True,
              "image": {"sha256": consumer + str(scale)}}
             for consumer in ("statusCell", "compactStatus") for scale in (1, 3)]
    capture["views"] = copy.deepcopy(cells)
    capture["screenshots"] = [{"phase": name, "sha256": name + "-screenshot"} for name in grader.PHASES]
    for phase in capture["phases"]:
        phase["samples"] = [{"cells": copy.deepcopy(cells)}]
    return capture


class ConsumerExecutionGradeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="consumer execution grade ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()

    def reference(self, path):
        return {"path": path.relative_to(self.root).as_posix(), "sha256": sha(path)}

    def test_observed_task_name_layout_keeps_role_and_alias_consistency(self):
        actual = {"task_name": "/root/consumer_execution", "agent_type": "pixl", "fork_turns": "none",
                  "distinct_agent_id_returned": False}
        self.assertEqual(grader.selected_identity(actual, "codex"), "/root/consumer_execution")
        self.assertEqual(grader.selected_identity({**actual, "canonical_task": actual["task_name"]}, "codex"), actual["task_name"])
        for field, value in (("canonical_task", "/root/other"), ("agent_id", "unbound-child-id"),
                             ("agent_type", "default"), ("subagent_type", "default"),
                             ("fork_turns", "all"), ("task_name", "consumer_execution")):
            with self.subTest(field=field):
                self.assertIsNone(grader.selected_identity({**actual, field: value}, "codex"))

    def test_structured_preservation_requires_actual_unchanged_bytes_and_no_contradictions(self):
        actual = {"unchanged": True, "changes": [], "before_count": 4440, "after_count": 4440}
        self.assertTrue(grader.reported_unchanged(actual, True))
        self.assertTrue(grader.reported_unchanged(True, True))
        self.assertFalse(grader.reported_unchanged(actual, False))
        self.assertFalse(grader.reported_unchanged(True, False))
        for value in ({"unchanged": "true"}, {"unchanged": True, "changed": True},
                      {"unchanged": True, "changes": ["state.px"]}, {"unchanged": True, "differences": ["source"]},
                      {"unchanged": True, "added_outside_reports": ["extra"]}, "unchanged"):
            with self.subTest(value=value):
                self.assertFalse(grader.reported_unchanged(value, True))

    def test_annotated_refs_keep_exact_bytes_and_reject_flat_wrapper_conflicts(self):
        ref = {"path": "work/operation.json", "sha256": "a" * 64, "bytes": 10}
        report = {"operation_result": {"reference": ref, "status": "complete"},
                  "execution_report": {"result": ref, "linked": {}}, "scope": "execution"}
        normalized = grader.report_fields(report)
        self.assertEqual(normalized["operation_result"], ref)
        self.assertEqual(normalized["execution_report"], ref)
        self.assertIn("reference", report["operation_result"])
        self.assertEqual(grader.report_reference({**ref, "reference": ref}, "reference"), ref)
        for value in ({**ref, "reference": {**ref, "sha256": "b" * 64}},
                      {**ref, "reference": {**ref, "path": "other.json"}},
                      {"reference": {"path": ref["path"]}}, {"status": "complete"}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                grader.report_reference(value, "reference")

    def test_verified_preservation_requires_matching_state_and_explicit_zero_change_results(self):
        child = {"verified": True, "state_hash_after": "a" * 64, "state_changed_reported": False,
                 "state_written_reported": False, "results": {"baseline_sha256sum_c_returncode": 0,
                 "kit_sha256sum_c_returncode": 0, "missing_baseline_files": 0,
                 "files_newer_than_baseline_outside_work_consumer_execution": 0}}
        caller = {"verified": True, "canonical_state": {"state_hash": "a" * 64,
                  "state_changed_reported_by_operation": False, "state_written_reported_by_operation": False},
                  "results": {"file_set_drift": 0, "kit_file_set_drift": 0,
                  "files_newer_than_baseline_outside_work_consumer_execution": 0, "kit_pycache_present_after": False}}
        for value in (child, caller):
            self.assertTrue(grader.reported_unchanged(value, True, "a" * 64))
            self.assertFalse(grader.reported_unchanged(value, False, "a" * 64))
            self.assertFalse(grader.reported_unchanged(value, True, "b" * 64))
            self.assertFalse(grader.reported_unchanged({**value, "unchanged": False}, True, "a" * 64))
            changed = copy.deepcopy(value)
            changed["results"]["files_newer_than_baseline_outside_work_consumer_execution"] = 1
            self.assertFalse(grader.reported_unchanged(changed, True, "a" * 64))
        child["state_written_reported"] = True
        caller["canonical_state"]["state_changed_reported_by_operation"] = True
        self.assertFalse(grader.reported_unchanged(child, True, "a" * 64))
        self.assertFalse(grader.reported_unchanged(caller, True, "a" * 64))
        self.assertFalse(grader.reported_unchanged({"verified": True}, True, "a" * 64))

    def test_unchanged_alias_cannot_bypass_supplied_state_result_or_count_contradictions(self):
        contradictions = (
            {"verified": False}, {"state_changed_reported": True}, {"state_written_reported": True},
            {"state_hash_after": "b" * 64}, {"canonical_state": {"state_hash": "b" * 64}},
            {"canonical_state": {"state_changed_reported_by_operation": True}},
            {"canonical_state": {"state_written_reported_by_operation": True}},
            {"results": {"file_set_drift": 1}}, {"results": {"kit_file_set_drift": 1}},
            {"results": {"missing_baseline_files": 1}}, {"results": {"baseline_sha256sum_c_returncode": 1}},
            {"results": {"kit_sha256sum_c_returncode": 1}},
            {"results": {"files_newer_than_baseline_outside_work_consumer_execution": 1}},
            {"results": {"kit_pycache_present_after": True}}, {"results": {"file_set_drift": False}},
            {"results": {"file_set_drift": "0"}}, {"results": []}, {"canonical_state": "unchanged"},
            {"before_count": 2, "after_count": 3}, {"baseline_count": 2, "current_count": 3},
            {"before_count": True}, {"baseline_count": -1},
        )
        for contradiction in contradictions:
            with self.subTest(contradiction=contradiction):
                self.assertFalse(grader.reported_unchanged({"unchanged": True, **contradiction}, True, "a" * 64))
        consistent = {"unchanged": True, "verified": True, "state_hash_after": "a" * 64,
                      "state_changed_reported": False, "canonical_state": {"state_hash": "a" * 64,
                      "state_written_reported_by_operation": False}, "results": {"file_set_drift": 0}}
        self.assertTrue(grader.reported_unchanged(consistent, True, "a" * 64))
        self.assertFalse(grader.reported_unchanged(consistent, True))

    def test_verified_layout_cannot_ignore_contradictory_fields_from_other_layout(self):
        child = {"verified": True, "state_hash_after": "a" * 64, "state_changed_reported": False,
                 "state_written_reported": False, "results": {"baseline_sha256sum_c_returncode": 0,
                 "kit_sha256sum_c_returncode": 0, "missing_baseline_files": 0,
                 "files_newer_than_baseline_outside_work_consumer_execution": 0}}
        caller = {"verified": True, "canonical_state": {"state_hash": "a" * 64,
                  "state_changed_reported_by_operation": False, "state_written_reported_by_operation": False},
                  "results": {"file_set_drift": 0, "kit_file_set_drift": 0,
                  "files_newer_than_baseline_outside_work_consumer_execution": 0, "kit_pycache_present_after": False}}
        child["results"]["file_set_drift"] = 1
        caller["state_changed_reported"] = True
        for value in (child, caller):
            self.assertFalse(grader.reported_unchanged(value, True, "a" * 64))
            self.assertFalse(grader.reported_unchanged({**value, "unchanged": True}, True, "a" * 64))

    def frozen_fixture(self):
        out = self.root / "work/consumer-execution/execution-01"
        (out / "renderer").mkdir(parents=True)
        (out / "capture").mkdir()
        kit = self.root / grader.KIT / "resources/examples/consumer-execution/queue-motion"
        kit.mkdir(parents=True)
        files, provenance = {}, []
        for name in grader.PROFILE_FILES:
            data = ("from pathlib import Path\ndef check(project, capture, renderer=None):\n"
                    "    return {'checker': str(Path(__file__).resolve()), 'renderer': str(renderer), 'synthetic': True}\n"
                    if name == "check.py" else "synthetic retained " + name + "\n").encode()
            copied, resource = out / "renderer" / name, kit / name
            copied.write_bytes(data)
            resource.write_bytes(data)
            files[resource.relative_to(self.root / grader.KIT).as_posix()] = sha(resource)
            provenance.append({"resource": str(resource), "copy": copied.relative_to(self.root).as_posix(), "sha256": sha(resource)})
        write_json(out / "capture/capture.json", {"synthetic": True})
        write_json(out / "renderer-sources.json", provenance)
        return {"package_files": files}, {"artifacts": {
            "capture/capture.json": self.reference(out / "capture/capture.json"),
            "renderer-sources.json": self.reference(out / "renderer-sources.json")}}, out

    def test_phase_verifier_uses_actual_per_consumer_counts_and_consumer_owned_geometry(self):
        capture, checked = phase_fixture()
        # Three source-defined frames and a nonzero held cell are valid; this is
        # a grader contract fixture, not actual browser or artistic evidence.
        self.assertEqual(grader.phase_errors(capture, checked), [])
        self.assertEqual(grader.summary(checked["facts"])["phases"]["normal-start"]["counts"]["statusCell@1"]["distinct_frames"], 3)
        mutations = (("wraps", 1), ("skips", 1), ("frames", [0, 2]))
        for field, value in mutations:
            with self.subTest(field=field):
                changed = copy.deepcopy(checked)
                changed["facts"]["phases"]["normal-start"]["counts"]["compactStatus@1"][field] = value
                self.assertTrue(grader.phase_errors(capture, changed))
        checked["facts"]["phases"]["reduced"]["counts"]["statusCell@3"]["transitions"] = 1
        self.assertIn("Held consumer changed frames: reduced/statusCell@3", grader.phase_errors(capture, checked))

    def test_new_page_or_claimed_switch_cannot_qualify_same_page_reconciliation(self):
        capture, checked = phase_fixture()
        changed = copy.deepcopy(capture)
        changed["phases"][1]["sessionId"] = "replacement-page"
        self.assertTrue(grader.phase_errors(changed, checked))
        changed = copy.deepcopy(capture)
        changed["phases"][2]["preferenceEvents"] = []
        self.assertTrue(grader.phase_errors(changed, checked))
        changed = copy.deepcopy(capture)
        changed["phases"][3]["initialMotion"] = "normal"
        self.assertIn("Initial preference not applied before page startup: initially-reduced", grader.phase_errors(changed, checked))
        del checked["facts"]["phases"]["normal-restored"]["counts"]["statusCell@1"]
        self.assertIn("Missing actual consumer/scale coverage: normal-restored", grader.phase_errors(capture, checked))

    def test_checker_reexecution_uses_exact_frozen_copy_and_rejects_tampering_before_loading(self):
        identity, result, out = self.frozen_fixture()
        checked, capture, directory = grader.frozen_recheck(self.root, identity, result)
        self.assertEqual(checked["checker"], str(out / "renderer/check.py"))
        self.assertEqual(checked["renderer"], str(out / "renderer"))
        self.assertEqual(directory, out)
        self.assertEqual(capture, {"synthetic": True})
        marker = self.root / "tampered-code-executed"
        (out / "renderer/check.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('bad')\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs from declared bytes"):
            grader.frozen_recheck(self.root, identity, result)
        self.assertFalse(marker.exists())

    def test_rehashed_copy_cannot_replace_frozen_shipped_closure(self):
        identity, result, out = self.frozen_fixture()
        copied = out / "renderer/view.mjs"
        copied.write_text("different renderer\n", encoding="utf-8")
        resource = self.root / grader.KIT / "resources/examples/consumer-execution/queue-motion/view.mjs"
        resource.write_bytes(copied.read_bytes())
        provenance = json.loads((out / "renderer-sources.json").read_bytes())
        next(item for item in provenance if Path(item["copy"]).name == "view.mjs")["sha256"] = sha(copied)
        write_json(out / "renderer-sources.json", provenance)
        result["artifacts"]["renderer-sources.json"] = self.reference(out / "renderer-sources.json")
        with self.assertRaisesRegex(ValueError, "exact frozen installed kit"):
            grader.frozen_recheck(self.root, identity, result)

    def test_duplicate_renderer_entry_does_not_establish_a_complete_closure(self):
        identity, result, out = self.frozen_fixture()
        provenance = json.loads((out / "renderer-sources.json").read_bytes())
        provenance[-1] = provenance[0]
        write_json(out / "renderer-sources.json", provenance)
        result["artifacts"]["renderer-sources.json"] = self.reference(out / "renderer-sources.json")
        with self.assertRaisesRegex(ValueError, "Incomplete or duplicate"):
            grader.frozen_recheck(self.root, identity, result)

    def test_phase_screenshots_cover_checked_both_consumer_scales_without_duplicate_cell_views(self):
        capture = viewing_fixture()
        screenshots = {item["sha256"] for item in capture["screenshots"]}
        coverage = grader.viewing_coverage(capture, screenshots, screenshots)
        self.assertTrue(coverage["pass"])
        self.assertTrue(coverage["combined_screenshot_consumer_scale_coverage"])
        self.assertFalse(coverage["standalone_consumer_scale_coverage"])

    def test_named_screenshots_without_actual_viewing_or_missing_phase_do_not_pass(self):
        capture = viewing_fixture()
        screenshots = {item["sha256"] for item in capture["screenshots"]}
        self.assertFalse(grader.viewing_coverage(capture, set(), screenshots)["pass"])
        self.assertFalse(grader.viewing_coverage(capture, screenshots, set())["pass"])
        capture["screenshots"].pop()
        self.assertFalse(grader.viewing_coverage(capture, screenshots, screenshots)["pass"])

    def test_standalone_images_are_equivalent_scale_evidence_when_combined_inventory_is_incomplete(self):
        capture = viewing_fixture()
        screenshots = {item["sha256"] for item in capture["screenshots"]}
        capture["phases"][0]["samples"][0]["cells"].pop()
        self.assertFalse(grader.viewing_coverage(capture, screenshots, screenshots)["pass"])
        both = screenshots | {view["image"]["sha256"] for view in capture["views"]}
        coverage = grader.viewing_coverage(capture, both, both)
        self.assertTrue(coverage["pass"])
        self.assertFalse(coverage["combined_screenshot_consumer_scale_coverage"])
        self.assertTrue(coverage["standalone_consumer_scale_coverage"])
        # Independent motion/checker coverage is still a separate required grade.

    def test_authored_success_without_required_native_and_artifact_evidence_fails(self):
        write_json(self.root / "CALLER-RESULT.json", {"status": "pass", "production_unchanged": True, "acceptance_created": False})
        result = grader.grade(self.root)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["passed"], 0)
        self.assertEqual(result["checks"][0]["check"], "required_evidence_readable")


if __name__ == "__main__":
    unittest.main()
