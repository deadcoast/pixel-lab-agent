"""Adversarial authority/source and real pixel-destination evidence checks."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from evaluations.grade_artistic_revision import (
    capture_errors,
    completion_observation,
    criteria_errors,
    historical_record_errors,
    image_error,
    outcome_status,
    plan_errors,
    semantic_changes,
    timing_error,
)
from evaluations.host_trials import sha, write_json
from pixl import codec
from pixl.codec import Document, Record, Ref, Symbol


class RecoveredRecorderEvidenceTests(unittest.TestCase):
    def test_terminal_native_event_does_not_invent_successful_process_completion(self):
        recovered = {"status": "finished", "returncode": None, "interruption_reason": "recording_error",
                     "native_terminal_proof": {"type": "turn.completed", "caller_result_delivered": True}}
        passed, evidence = completion_observation(recovered)
        self.assertFalse(passed)
        self.assertIsNone(evidence["returncode"])
        self.assertEqual(evidence["interruption_reason"], "recording_error")

    def test_task_checks_can_pass_with_partial_recorder_outcome(self):
        checks = [{"check": "actual_saved_artifact_and_reviews", "pass": True},
                  {"check": "native_attempt_completed", "pass": False}]
        self.assertEqual(outcome_status(checks), "partial")
        checks[0]["pass"] = False
        self.assertEqual(outcome_status(checks), "fail")

    def test_clean_observed_process_completion_remains_distinct(self):
        self.assertTrue(completion_observation({"status": "finished", "returncode": 0,
                                                "interruption_reason": None})[0])
        self.assertFalse(completion_observation({"status": "finished", "returncode": None,
                                                 "interruption_reason": None})[0])


class AdditiveDestinationHistoryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name in ("src/queue-view-artistic.ts", "renderer-artistic/view.mjs"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("actual destination\n", encoding="utf-8")
        self.baseline = Document(format=2, records={"project": Record("project", "P", {
            "nm": "original project", "in": [Ref("old.destination")]})})
        self.document = copy.deepcopy(self.baseline)
        self.document.records["project"].fields["in"].append(Ref("new.destination"))
        self.document.records.update({
            "plan": Record("plan", "X", {"mt": {"tasks": {"delivery.task": {}}}}),
            "delivery.task": Record("delivery.task", "T", {"op": [Ref("delivery.output")]}),
            "delivery.output": Record("delivery.output", "F", {"mb": [], "ds": [Ref("new.destination")]}),
            "new.destination": Record("new.destination", "I", {"pr": Ref("project"), "st": Symbol("confirmed"),
                "vl": {"module": "src/queue-view-artistic.ts", "fixture": "renderer-artistic/"}})})

    def errors(self):
        return historical_record_errors(self.document, self.baseline, "plan", self.root)

    def test_only_final_collective_actual_destination_may_be_appended(self):
        self.assertEqual(self.errors(), [])
        self.document.records["delivery.output"].fields["ds"] = []
        self.assertEqual(self.errors(), ["project"])

    def test_removing_old_reference_or_mutating_project_is_rejected(self):
        self.document.records["project"].fields["in"].pop(0)
        self.assertEqual(self.errors(), ["project"])
        self.document.records["project"] = copy.deepcopy(self.baseline.records["project"])
        self.document.records["project"].fields["in"].append(Ref("new.destination"))
        self.document.records["project"].fields["nm"] = "replacement project"
        self.assertEqual(self.errors(), ["project"])


class CompletedCollectiveTests(unittest.TestCase):
    def setUp(self):
        self.document = Document(format=2, records={
            "plan": Record("plan", "X", {"mt": {"binding": "pixl.production.plan/1", "tasks": {"delivery.task": {}}}}),
            "delivery.task": Record("delivery.task", "T", {"st": Symbol("done"), "op": [Ref("delivery.output")]}),
            "delivery.output": Record("delivery.output", "F", {"mb": [], "rq": [Ref("q")]}),
        })
        self.current = {"task": "delivery.task", "state": "done", "candidate": "accepted.snapshot", "blockers": [],
                        "snapshot_blockers": ["family_state: delivery.task is done; snapshots require an open or active task"],
                        "pending_jobs": [], "members": [{"accepted": True}]}

    def errors(self):
        with patch("evaluations.grade_artistic_revision.families.describe", return_value=self.current):
            return plan_errors(self.document, "plan", {"q"})

    def test_done_guard_prevents_another_snapshot_not_current_acceptance(self):
        self.assertEqual(self.errors(), [])

    def test_other_snapshot_and_member_blockers_still_reject_completion(self):
        self.current["snapshot_blockers"].append("baseline candidate is no longer eligible")
        self.assertTrue(self.errors())
        self.current["snapshot_blockers"].pop()
        self.current["members"][0]["accepted"] = False
        self.assertTrue(self.errors())


class CriteriaAuthorityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        source = self.root / "BRIEF.md"
        source.write_text("Cool blue is an accent.\n", encoding="utf-8")
        self.digest = sha(source)
        self.baseline = Document(format=2)
        originals = []
        for i in range(20):
            record = Record(f"old.q{i}", "Q", {"ck": f"original condition {i}"})
            self.baseline.records[record.id] = record
            originals.append({"id": record.id, "record_sha256": codec.record_hash(record)})
        self.document = copy.deepcopy(self.baseline)
        self.document.records["source"] = Record("source", "S", {"ur": "BRIEF.md", "dg": self.digest, "ln": [1, 1]})
        self.correction = {"retained_comparison": {"original_20": originals}, "corrected_criteria": [],
                           "sources": {"brief": {"sha256": self.digest}}}
        self.proposal = {"criteria": [], "sources": {"brief": {"sha256": self.digest}}}
        self.mapping = {"original_20": copy.deepcopy(originals), "corrected_29": []}
        for i in range(29):
            old, new = f"proposed.q{i}", f"adopted.q{i}"
            corrected = {"id": old, "corrected_check": f"Keep accent perceptible {i}", "original_check": f"Blue dominates {i}",
                         "authority_label_for_record": "owner (accent) / expert choice (coverage)",
                         "domain": "visual", "mode": "visual", "clauses": [{"text": "accent", "class": "owner"}],
                         "expert_clauses": [{"text": "coverage", "class": "expert_choice"}],
                         "carries": [f"old.q{i % 20}"], "sources_added": [], "evidence_route": None}
            self.correction["corrected_criteria"].append(corrected)
            self.proposal["criteria"].append({"id": old, "sources": [{"id": "brief"}]})
            adopted = {k: copy.deepcopy(v) for k, v in corrected.items()
                       if k in ("authority_label_for_record", "clauses", "expert_clauses", "carries", "sources_added", "evidence_route")}
            adopted.update(source_id=old, record_id=new, check=corrected["corrected_check"])
            self.mapping["corrected_29"].append(adopted)
            self.document.records[new] = Record(new, "Q", {"ck": adopted["check"], "dm": Symbol("visual"),
                                                           "md": Symbol("visual"), "so": [Ref("source")]})

    def errors(self):
        return criteria_errors(self.document, self.baseline, self.correction, self.proposal, self.mapping, self.root)

    def test_exact_reconciliation_and_saved_record_sources_pass(self):
        self.assertEqual(self.errors(), [])

    def test_label_only_repair_cannot_hide_narrowed_saved_check(self):
        self.document.records["adopted.q0"].fields["ck"] = "Blue must dominate"
        self.assertTrue(any("saved check" in e for e in self.errors()))

    def test_expert_clause_cannot_be_promoted_to_owner(self):
        self.mapping["corrected_29"][0]["expert_clauses"][0]["class"] = "owner"
        self.assertTrue(any("authority/lineage" in e for e in self.errors()))

    def test_valid_locator_does_not_substitute_another_source(self):
        replacement = self.root / "other.md"
        replacement.write_text("Blue must dominate.\n", encoding="utf-8")
        self.document.records["source"].fields.update(ur="other.md", dg=sha(replacement))
        self.assertTrue(any("retained source not bound" in e for e in self.errors()))

    def test_renamed_runtime_source_binds_new_bytes_but_cannot_replace_owner(self):
        new = self.root / "renderer-artistic/view.mjs"
        new.parent.mkdir()
        new.write_text("// actual additional live evidence\n", encoding="utf-8")
        self.proposal["sources"]["succ-view"] = {"path": "renderer-successor/view.mjs", "sha256": "a" * 64}
        self.proposal["criteria"][0]["sources"].append({"id": "succ-view"})
        self.document.records["runtime"] = Record("runtime", "S", {"ur": "renderer-artistic/view.mjs", "dg": sha(new), "ln": [1, 1]})
        self.document.records["adopted.q0"].fields["so"].append(Ref("runtime"))
        self.assertEqual(self.errors(), [])
        self.document.records["adopted.q0"].fields["so"] = [Ref("runtime")]
        self.assertTrue(any(":brief" in e for e in self.errors()))

    def test_omitted_criterion_and_changed_original_are_rejected(self):
        self.mapping["corrected_29"].pop()
        self.document.records["old.q0"].fields["ck"] = "replaced history"
        errors = self.errors()
        self.assertTrue(any("membership" in e for e in errors))
        self.assertTrue(any("original20 changed" in e for e in errors))

    def test_literal_rederivation_requires_separate_exact_review(self):
        row = self.mapping["corrected_29"][0]
        before = row["check"]
        row["check"] += "; both display scales were observed"
        self.document.records["adopted.q0"].fields["ck"] = row["check"]
        self.assertTrue(any("semantic review required" in e for e in self.errors()))
        review = {row["source_id"]: {"record_id": row["record_id"], "before": before, "after": row["check"]}}
        self.assertEqual(criteria_errors(self.document, self.baseline, self.correction, self.proposal,
                                         self.mapping, self.root, review), [])
        review[row["source_id"]]["after"] += " AND BLUE MUST DOMINATE"
        self.assertTrue(criteria_errors(self.document, self.baseline, self.correction, self.proposal,
                                        self.mapping, self.root, review))

    def test_independent_review_rejects_stale_mapping_or_unbound_evidence(self):
        mapping = self.root / "mapping.json"
        correction = self.root / "correction.json"
        approval = self.root / "independent-review.json"
        write_json(mapping, self.mapping)
        write_json(correction, self.correction)
        review = {"version": 1, "mapping_sha256": sha(mapping), "reconciliation_sha256": sha(correction),
                  "decisions": [{"source_id": "proposed.q0", "record_id": "adopted.q0", "approved": True,
                                 "before": "prior description", "after": "observed description", "reason": "independent exact comparison",
                                 "evidence": [{"path": "BRIEF.md", "sha256": self.digest}]}]}
        write_json(approval, review)
        self.assertIn("proposed.q0", semantic_changes(approval, self.root, mapping, correction))
        mapping.write_bytes(b"changed mapping")
        with self.assertRaisesRegex(ValueError, "does not bind"):
            semantic_changes(approval, self.root, mapping, correction)


class DestinationEvidenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.capture = self.root / "capture"
        self.capture.mkdir()
        (self.root / "assets").mkdir()
        (self.root / "src").mkdir()
        module = self.root / "src/queue-view-artistic.ts"
        module.write_text("export const representative = true;\n", encoding="utf-8")
        self.display = {"cell": [16, 16], "frameMs": 100, "filter": "nearest", "background": "#172336"}
        self.count = 0
        for state in ("idle", "running", "succeeded", "failed", "paused"):
            image = Image.new("RGBA", (64 if state == "running" else 16, 16), (0, 0, 0, 0))
            for frame in range(image.width // 16):
                image.putpixel((frame * 16 + 4 + frame, 8), (112, 185, 237, 255))
            image.save(self.root / f"assets/{state}.png")
        self.render = {"served_files": {"consumer/src/queue-view-artistic.ts": sha(module)}, "phases": []}
        for name, motion in (("normal-start", "normal"), ("reduced", "reduced"), ("normal-restored", "normal")):
            self.render["phases"].append(self.phase(name, motion))
        self.path = self.capture / "render.json"

    def image(self, image):
        name = f"image-{self.count}.png"
        self.count += 1
        image.save(self.capture / name)
        return {"path": name, "sha256": sha(self.capture / name)}

    def item(self, consumer, state, scale, motion, elapsed=0):
        animate = state == "running" and motion == "normal"
        frame = int(elapsed // 100) % 4 if animate else 0
        source = self.root / f"assets/{state}.png"
        with Image.open(source) as image:
            crop = image.convert("RGBA").crop((frame * 16, 0, (frame + 1) * 16, 16))
        actual = Image.alpha_composite(Image.new("RGBA", (16, 16), "#172336"), crop).resize((16 * scale, 16 * scale), Image.Resampling.NEAREST)
        return {"consumer": consumer, "state": state, "scale": scale, "elapsed": elapsed, "frame": frame,
                "asset": {"sha256": sha(source)}, "image": self.image(actual),
                "descriptor": {"path": f"assets/{state}.png", "frames": 4 if state == "running" else 1,
                               "motion": motion, "animate": animate, "holdFrame": None if animate else 0}}

    def phase(self, name, motion):
        views, playback, repaint = [], [], []
        screenshot = Image.new("RGBA", (4 * 64, 5 * 64), "#172336")
        for y, state in enumerate(("idle", "running", "succeeded", "failed", "paused")):
            for x, (consumer, scale) in enumerate((('statusCell', 1), ('statusCell', 3), ('compactStatus', 1), ('compactStatus', 3))):
                item = self.item(consumer, state, scale, motion)
                item["bounds"] = {"x": x * 64, "y": y * 64, "width": 16 * scale, "height": 16 * scale}
                with Image.open(self.capture / item["image"]["path"]) as actual:
                    screenshot.paste(actual, (x * 64, y * 64))
                views.append(item)
                repaint.append({"consumer": consumer, "state": state, "scale": scale, "frame": item["frame"],
                                "animate": item["descriptor"]["animate"], "holdFrame": item["descriptor"]["holdFrame"]})
                if state in {"running", "failed", "paused"}:
                    for elapsed in (range(0, 801, 50) if state == "running" else [0]):
                        playback.append(self.item(consumer, state, scale, motion, elapsed))
        report = {"sessionId": "one-page", "motion": motion, "mediaMatches": motion == "reduced",
                  "devicePixelRatio": 1, "errors": [], "missing": [], "display": self.display,
                  "views": views, "playback": playback,
                  "preferenceEvents": [{"sessionId": "one-page", "to": motion, "repainted": repaint}]}
        return {"name": name, "screenshot": self.image(screenshot), "report": report}

    def errors(self):
        write_json(self.path, self.render)
        return capture_errors(self.root, self.path)[0]

    def test_actual_decoded_pixels_both_consumers_scales_and_switches_pass(self):
        self.assertEqual(self.errors(), [])

    def test_pass_summary_cannot_hide_omitted_destination(self):
        self.render["checks"] = {"pass": True}
        self.render["phases"][0]["report"]["views"].pop()
        self.assertTrue(any("destination" in e for e in self.errors()))

    def test_deterministic_timeline_cannot_stand_in_for_observed_playback(self):
        report = self.render["phases"][0]["report"]
        report["timeline"] = report.pop("playback")
        self.assertTrue(any("wall-clock" in e for e in self.errors()))

    def test_rehashed_capture_pixel_corruption_is_detected(self):
        item = self.render["phases"][0]["report"]["views"][1]
        path = self.capture / item["image"]["path"]
        with Image.open(path) as image:
            changed = image.copy()
        changed.putpixel((0, 0), (255, 0, 0, 255))
        changed.save(path)
        item["image"]["sha256"] = sha(path)
        self.assertIn("pixels differ", image_error(self.root, self.capture, item, self.display))

    def test_reduced_phase_with_reloaded_session_is_rejected(self):
        self.render["phases"][1]["report"]["sessionId"] = "new-page"
        self.assertTrue(any("one page session" in e for e in self.errors()))

    def test_static_live_destination_omission_is_rejected(self):
        report = self.render["phases"][0]["report"]
        report["playback"] = [r for r in report["playback"] if r["state"] != "paused"]
        self.assertTrue(any("missing live paused" in e for e in self.errors()))

    def test_wrong_cadence_with_all_frames_and_wrap_is_rejected(self):
        for sample in self.render["phases"][0]["report"]["playback"]:
            if sample["state"] == "running":
                sample["elapsed"] = sample["elapsed"] * 10 + 50
        self.assertTrue(any("100ms timing" in e for e in self.errors()))

    def native_layout(self):
        for phase in self.render["phases"]:
            report = phase["report"]
            report["live"] = [copy.deepcopy(r) for r in report["views"] if r["state"] == "running"]
            report["stateLive"] = [r for r in report["playback"] if r["state"] != "running"]
            report["playback"] = [r for r in report["playback"] if r["state"] == "running"]
            for row in report["playback"]:
                row["motion"] = row["descriptor"]["motion"]
                row.pop("descriptor")

    def test_raw_raf_samples_join_exact_live_descriptor_and_static_state_captures(self):
        self.native_layout()
        for phase in self.render["phases"]:
            phase["report"]["stateLive"].append(copy.deepcopy(phase["report"]["live"][0]))
        self.assertEqual(self.errors(), [])

    def test_raw_raf_without_matching_live_destination_cannot_be_inferred(self):
        self.native_layout()
        self.render["phases"][0]["report"]["live"].pop()
        self.assertTrue(any("no unique" in e for e in self.errors()))

    def test_capture_boundary_uses_separate_paint_timestamp_and_exact_frame(self):
        sample = {"frame": 2, "elapsed": 300.1, "at": 900.1, "paintElapsed": 299.2, "paintAt": 899.2,
                  "descriptor": {"holdFrame": None}}
        self.assertIsNone(timing_error(sample, "normal"))
        sample["frame"] = 3
        self.assertIn("paint timing", timing_error(sample, "normal"))

    def test_paint_timestamp_cannot_disagree_with_capture_origin(self):
        sample = {"frame": 2, "elapsed": 300.1, "at": 900.1, "paintElapsed": 299.2, "paintAt": 899.2,
                  "descriptor": {"holdFrame": None}}
        self.assertIsNone(timing_error(sample, "normal"))
        sample["paintAt"] = 899.3
        self.assertIn("shared origin", timing_error(sample, "normal"))

    def test_stationary_construction_paint_can_precede_live_timing_epoch(self):
        sample = {"frame": 0, "elapsed": 300.2, "at": 3545.8, "paintElapsed": 0, "paintAt": 3245.5,
                  "descriptor": {"holdFrame": 0}}
        self.assertIsNone(timing_error(sample, "reduced"))


if __name__ == "__main__":
    unittest.main()
