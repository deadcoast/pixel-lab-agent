"""Caller summaries preserve exact handoffs and distinguish delivery from claims."""

import copy
import json
import unittest
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import handoff, jobs, plar, service
from pixl.codec import PixlError
from tests import test_plar_family_delivery as family_fixture
from tests.test_plar_prepare import seed, write


class CallerResultTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "consumer"
        self.args, _, _, _ = seed(self.root)
        self.prepared = service.call("pixl_plar_prepare", self.args, self.root)
        self.details = {"status": "partial", "expert_reasoning": "Retain the complete explanation separately."}

    def save(self, details=None, **changes):
        args = {
            "asset_id": self.args["asset_id"], "requirements_hash": self.args["requirements_hash"],
            "expect": self.prepared["hash"], "details": self.details if details is None else details,
            "view": "caller",
        }
        return handoff.save(self.root, **{**args, **changes})

    def files(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def declaration(self):
        reference = {**write(self.root, "work/expert-report.json", {"finding": "Renderer unavailable"}), "role": "expert report"}
        return {
            "summary": "The retained request is ready for the existing connection.",
            "artifacts": [reference], "reports": [reference],
            "issues": [{"category": "unavailable_observation", "summary": "Renderer was unavailable", "recovery": "Inspect in the selected renderer."}],
            "integration": {"status": "unavailable", "summary": "No renderer was available.", "evidence": [reference]},
        }

    def test_default_receipt_and_snapshot_bytes_remain_unchanged(self):
        self.details["caller"] = self.declaration()
        selected = plar.read(self.root, asset_id=self.args["asset_id"])
        expected = {
            "version": 1, "asset_id": self.args["asset_id"], "requirements_hash": self.args["requirements_hash"],
            "resume": selected["production"]["continuation"], "next": selected["production"]["continuation"]["action"],
            "selection": {"path": "plar.txt", "hash": selected["hash"], "current": selected["production"]["selection_current"]},
            "details": self.details,
            "scope": "Snapshot of derived state plus agent-authored observations. No automatic contract, art or delivery acceptance; reread current PLAR before acting.",
        }
        expected_bytes = (json.dumps(expected, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
        receipt = self.save(view="receipt")
        before = self.files()
        compact = self.save()
        self.assertEqual((self.root / receipt["path"]).read_bytes(), expected_bytes)
        self.assertEqual(receipt["sha256"], sha256(expected_bytes).hexdigest())
        self.assertEqual(set(receipt), {"path", "sha256", "asset_id", "requirements_hash", "state_hash", "next", "scope"})
        self.assertEqual({key: compact[key] for key in receipt}, receipt)
        self.assertEqual(self.files(), before)

    def test_caller_reads_one_selected_snapshot_and_retains_exact_resume(self):
        self.details["caller"] = self.declaration()
        selected = plar.read(self.root, asset_id=self.args["asset_id"])
        with patch("pixl.handoff.plar.read", return_value=selected) as read:
            result = self.save()
        self.assertEqual(read.call_count, 1)
        self.assertTrue(result["caller"]["present"])
        self.assertEqual(result["caller"]["artifacts"], self.details["caller"]["artifacts"])
        self.assertEqual(result["caller"]["integration"]["status"], "unavailable")
        self.assertEqual(result["resume"], selected["production"]["continuation"])
        self.assertEqual(result["production"]["criteria"]["by_status"], {"unperformed": 3})
        self.assertEqual(result["production"]["jobs"]["pending"], 1)
        self.assertFalse(result["production"]["delivery_observed"])

    def test_legacy_details_are_not_summarized_or_reinterpreted(self):
        self.details.update(status="delivered", artifacts=["legacy-freeform"], reasoning="x" * 100_000)
        result = self.save()
        self.assertFalse(result["caller"]["present"])
        self.assertNotIn("artifacts", result["caller"])
        self.assertEqual(result["assignment"], {"status": "delivered", "basis": "agent_authored"})
        self.assertEqual(result["production"]["task_state"], "open")
        self.assertIsNone(result["production"]["delivery_complete"])
        self.assertEqual(result["next"], "dispatch")
        self.assertLess(len(json.dumps(result).encode("utf-8")), 8192)
        self.assertGreater(result["details_ref"]["bytes"], 100_000)

    def test_exact_line_locators_retrieve_saved_sections(self):
        self.details["caller"] = self.declaration()
        result = self.save()
        for key, field in [("details_ref", "details"), ("resume_ref", "resume")]:
            reference = result[key]
            section = service.source_slice(self.root / reference["path"], reference["sha256"], reference["start"], reference["end"], reference["bytes"])
            parsed = json.loads("{" + section["text"].rstrip().removesuffix(",") + "}")
            saved = json.loads((self.root / result["path"]).read_bytes())
            self.assertEqual(parsed[field], saved[field])
            self.assertEqual(reference["json_pointer"], "/" + field)

    def test_large_resume_is_retrievable_without_partial_rewrite(self):
        selected = plar.read(self.root, asset_id=self.args["asset_id"])
        selected["production"]["continuation"]["jobs"][0]["discovery"]["evidence"]["extended_capture"] = "x" * 6000
        with patch("pixl.handoff.plar.read", return_value=selected):
            result = self.save()
        self.assertFalse(result["resume_inline"])
        self.assertNotIn("resume", result)
        self.assertEqual(result["store"], selected["production"]["continuation"]["store"])
        self.assertEqual(result["next"], selected["production"]["continuation"]["action"])
        saved = json.loads((self.root / result["path"]).read_bytes())
        self.assertEqual(saved["resume"], selected["production"]["continuation"])
        reference = result["resume_ref"]
        section = service.source_slice(self.root / reference["path"], reference["sha256"], reference["start"], reference["end"], reference["bytes"])
        self.assertIn("extended_capture", section["text"])

    def test_unknown_job_preserves_same_identity_and_reconciliation(self):
        claimed = jobs.dispatch(self.root / self.prepared["store"], self.prepared["hash"], self.prepared["job"]["id"], self.root)
        result = self.save(expect=claimed["hash"])
        self.assertEqual(result["next"], "reconcile")
        self.assertEqual(result["production"]["jobs"]["by_state"], {"unknown": 1})
        retained = result["resume"]["jobs"][0]
        self.assertEqual(retained["id"], self.prepared["job"]["id"])
        self.assertEqual(retained["discovery"], self.args["connection"]["discovery"])
        self.assertEqual(retained["next_action"], "reconcile")

    def test_malformed_or_oversized_input_writes_nothing(self):
        declarations = [
            {"summary": "x" * 601}, {"summary": 3}, {"unknown": "no"},
            {"integration": {"status": "accepted", "summary": "no"}},
            {"issues": [{"category": "anything", "summary": "no"}]},
            {"reports": [{}] * 13},
            {"issues": [{"category": "unfinished_work", "summary": "x" * 600, "recovery": "x" * 600}] * 12},
            {"summary": "\ud800"}, None,
        ]
        before = self.files()
        for caller in declarations:
            with self.subTest(caller=str(caller)[:50]), self.assertRaises(PixlError):
                self.save(details={"status": "partial", "caller": caller})
            self.assertEqual(self.files(), before)

    def test_changed_missing_or_escaping_artifact_writes_nothing(self):
        reference = self.declaration()["artifacts"][0]
        cases = [
            {**reference, "sha256": "0" * 64},
            {**reference, "path": "work/missing.json"},
            {**reference, "path": "../outside.json"},
            {**reference, "path": str(self.root / reference["path"])},
        ]
        before = self.files()
        for item in cases:
            with self.subTest(item=item), self.assertRaises(PixlError) as failed:
                self.save(details={"status": "partial", "caller": {"artifacts": [item]}})
            self.assertEqual(self.files(), before)
            if failed.exception.code in {"caller_artifact_stale", "caller_artifact_unavailable"}:
                self.assertEqual(failed.exception.context["path"], item["path"])
                self.assertEqual(failed.exception.context["expected_file_sha256"], item["sha256"])
            if failed.exception.code == "caller_artifact_stale":
                self.assertEqual(failed.exception.context["observed_file_sha256"], reference["sha256"])

    def test_stale_requirements_and_state_do_not_publish(self):
        before = self.files()
        for changed in [{"expect": "0" * 64}, {"requirements_hash": "0" * 64}]:
            with self.assertRaisesRegex(PixlError, "handoff_stale"):
                self.save(**changed)
            self.assertEqual(self.files(), before)

    def test_existing_receipt_mode_does_not_validate_legacy_caller_field(self):
        result = self.save(view="receipt", details={"status": "partial", "caller": "legacy arbitrary details"})
        self.assertTrue((self.root / result["path"]).is_file())

    def test_integration_absence_and_not_performed_are_distinct(self):
        absent = self.save(details={"status": "partial", "caller": {"summary": "A partial result"}})
        self.assertNotIn("integration", absent["caller"])
        for status in ("not_performed", "not_in_scope", "fail", "pass"):
            result = self.save(details={"status": "partial", "caller": {"integration": {"status": status, "summary": "Agent observation"}}})
            self.assertEqual(result["caller"]["integration"]["status"], status)
            self.assertIsNone(result["production"]["delivery_complete"])

    def test_input_objects_are_not_mutated(self):
        self.details["caller"] = self.declaration()
        original = copy.deepcopy(self.details)
        result = self.save()
        result["caller"]["summary"] = "Changed caller presentation"
        self.assertEqual(self.details, original)
        self.assertEqual(json.loads((self.root / result["path"]).read_bytes())["details"], original)

    def test_family_and_destination_facts_do_not_promote_assignment_status(self):
        fixture = family_fixture.PLARFamilyDeliveryTests("test_current_destination_cannot_bypass_unfinished_collective_review")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)

        def capture():
            selected = plar.read(fixture.root, asset_id="queue.working")
            return handoff.save(fixture.root, "queue.working", selected["requirements_hash"], selected["production"]["hash"], {"status": "partial"}, view="caller")

        def delivery(result):
            if result["production"]["delivery_inline"]:
                return result["production"]["delivery"]
            reference = result["production"]["delivery_ref"]
            self.assertEqual(reference["json_pointer"], "/resume/delivery")
            section = service.source_slice(fixture.root / reference["path"], reference["sha256"],
                                           reference["start"], reference["end"], reference["bytes"])
            return json.loads("{" + section["text"].rstrip().removesuffix(",") + "}")["resume"]["delivery"]

        unfinished = capture()
        self.assertTrue(delivery(unfinished)["destination_matches"])
        self.assertFalse(unfinished["production"]["delivery_complete"])
        fixture.finish_family()
        complete = capture()
        self.assertTrue(complete["production"]["delivery_complete"])
        self.assertEqual(complete["assignment"]["status"], "partial")
        fixture.destination.write_bytes(b"Changed destination")
        changed = capture()
        self.assertFalse(changed["production"]["delivery_complete"])
        self.assertEqual(changed["next"], "review_delivery")
        self.assertEqual(changed["state_hash"], complete["state_hash"])

    def test_large_delivery_has_exact_locator_and_explicit_inline_flag(self):
        selected = plar.read(self.root, asset_id=self.args["asset_id"])
        selected["production"]["continuation"]["delivery"] = {"complete": False, "families": [{"scope": "x" * 3000}]}
        with patch("pixl.handoff.plar.read", return_value=selected):
            result = self.save()
        self.assertFalse(result["production"]["delivery_inline"])
        self.assertNotIn("delivery", result["production"])
        self.assertEqual(result["production"]["delivery_ref"]["json_pointer"], "/resume/delivery")
        self.assertFalse(result["production"]["delivery_complete"])


if __name__ == "__main__":
    unittest.main()
