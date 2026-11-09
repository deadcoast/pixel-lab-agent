"""Structural deltas and retrieval never substitute for semantic caller review."""

import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pixl import codec, mcp, production_plan, service, store
from pixl.codec import PixlError
from tests.family_support import family
from tests.lifecycle_support import add_candidate, add_verdict
from tests.test_production_plan import plan


class SuccessorReviewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        family(self.root)
        self.folder = self.root / ".pixl"
        production_plan.author(self.folder, codec.digest(store.load(self.folder)), plan(), self.root)
        successor = copy.deepcopy(plan())
        successor["id"] = "successor"
        successor["stages"][0]["criteria"][0]["check"] = "Keep the requested silhouette with partial alpha permitted."
        successor["stages"][0]["criteria"].append({**successor["stages"][0]["criteria"][0], "id": "added", "check": "A distinct added obligation."})
        production_plan.author(self.folder, codec.digest(store.load(self.folder)), successor, self.root)
        self.args = {"packet": ".pixl/state.px", "plan": "successor.plan", "against_plan": "next.plan", "view": "changes"}

    def report(self, **options):
        return service.call("pixl_request_review", self.args | options, self.root)

    def test_delta_and_exact_full_criteria_retrieval_preserve_default_identity(self):
        before = (self.folder / "state.px").read_bytes()
        result = self.report()
        self.assertEqual(result["counts"]["criteria"], {"added": 1, "removed": 0, "changed": 1, "unchanged": 1})
        self.assertEqual(result["changes"]["criteria"]["changed"][0]["fields"], ["check"])
        self.assertEqual(len(result["criterion_index"]["before"]), 2)
        self.assertEqual(len(result["criterion_index"]["after"]), 3)
        locator = result["after"]["retrieve"]
        full = service.call(locator["tool"], locator["arguments"], self.root)
        self.assertEqual(full["review_scope_sha256"], result["after"]["review_scope_sha256"])
        self.assertEqual(full["criteria"][0]["check"], "Keep the requested silhouette with partial alpha permitted.")
        self.assertIsNone(result["consistent"])
        self.assertEqual(before, (self.folder / "state.px").read_bytes())

    def test_renamed_clauses_are_added_removed_not_fuzzy_matched(self):
        # A third retained plan has a renamed clause with otherwise identical text.
        value = copy.deepcopy(plan()); value["id"] = "renamed"
        value["stages"][0]["criteria"][0]["id"] = "renamed"
        production_plan.author(self.folder, codec.digest(store.load(self.folder)), value, self.root)
        result = self.report(plan="renamed.plan")
        self.assertEqual(result["counts"]["criteria"], {"added": 1, "removed": 1, "changed": 0, "unchanged": 1})

    def test_source_drift_and_missing_historical_choice_are_explicit(self):
        (self.root / "source.txt").write_text("Changed on disk\n", encoding="utf-8")
        doc = store.load(self.folder)
        doc.records["destination"].fields["wy"] = "Changed current destination declaration"
        (self.folder / "state.px").write_bytes(codec.encode(doc))
        result = self.report()
        self.assertTrue(result["diagnostics"]["before"])
        self.assertTrue(result["diagnostics"]["after"])
        row = next(r for r in result["retained_choices"] if r["id"] == "destination")
        self.assertFalse(row["current"])
        self.assertIsNone(row["declaration"])

    def test_prior_failure_and_stale_receipt_remain_visible(self):
        doc = store.load(self.folder)
        add_candidate(doc, self.root, "failed-art")
        # Attach a synthetic failed candidate to the earlier connected stage.
        doc.records["task"].fields["ca"] = [r for r in doc.records["task"].fields["ca"] if r.id != "failed-art"]
        doc.records["failed-art"].fields["of"] = codec.Ref("next.motion.output")
        add_verdict(doc, self.root, "failed-art", "next.motion.q.shape", "fail", "retained.failure")
        (self.folder / "state.px").write_bytes(codec.encode(doc))
        receipt = self.root / "retained.failure.e.json"
        receipt.write_text("changed receipt", encoding="utf-8")
        result = self.report()
        failed = result["review_attention"]["before"]["failures_obsolete_or_stale"]
        self.assertEqual(failed[0]["status"], "fail")
        self.assertEqual(failed[0]["receipts"][0]["file_status"], "changed")
        self.assertTrue(result["review_attention"]["after"]["outputs"][0]["requires_review"])

    def test_incompatible_options_and_tampered_snapshot_fail(self):
        for args in [{"view": "complete"}, {"against_plan": "successor.plan"}, {"against_plan": None}, {"plan": None}]:
            with self.subTest(args=args), self.assertRaises(PixlError):
                self.report(**args)
        doc = store.load(self.folder)
        (self.root / doc.records["next.plan"].fields["ur"]).write_text("{}", encoding="utf-8")
        with self.assertRaises(PixlError):
            self.report()

    def test_pass_without_current_proof_does_not_hide_review_attention(self):
        doc = store.load(self.folder)
        add_candidate(doc, self.root, "unchecked")
        doc.records["task"].fields["ca"] = [r for r in doc.records["task"].fields["ca"] if r.id != "unchecked"]
        doc.records["unchecked"].fields["of"] = codec.Ref("successor.motion.output")
        doc.records["successor.motion.task"].fields["ca"] = [codec.Ref("unchecked")]
        add_verdict(doc, self.root, "unchecked", "successor.motion.q.shape", "pass", "invalid.pass")
        doc.records["invalid.pass"].fields["ev"] = []
        (self.folder / "state.px").write_bytes(codec.encode(doc))
        self.assertIn("successor.motion.q.shape", self.report()["review_attention"]["after"]["outputs"][0]["requires_review"])

    def test_cli_mcp_export_parity_and_relocation(self):
        result = self.report()
        response = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
            "name": "pixl_request_review", "arguments": self.args}}, self.root)
        self.assertEqual(response["result"]["structuredContent"], result)
        cli = subprocess.run([sys.executable, "-m", "pixl", "request-review", ".pixl/state.px", "--plan", "successor.plan",
                              "--against-plan", "next.plan", "--view", "changes", "--root", str(self.root),
                              "--result-path", "comparison.json"], capture_output=True, check=True)
        self.assertTrue(json.loads(cli.stdout)["result_saved"])
        self.assertEqual(json.loads((self.root / "comparison.json").read_bytes()), result)
        with tempfile.TemporaryDirectory() as temp:
            relocated = Path(temp) / "consumer"; shutil.copytree(self.root, relocated)
            moved = service.call("pixl_request_review", self.args, relocated)
            self.assertEqual(moved["comparison_sha256"], result["comparison_sha256"])
