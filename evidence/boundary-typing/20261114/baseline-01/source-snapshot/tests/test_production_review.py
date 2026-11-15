"""Connected authoring hands exact clauses to review without judging their meaning."""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from pixl import codec, jobs, production_plan, request_review, service, store
from tests.family_support import family
from tests.test_production_plan import packet, plan


class ProductionReviewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        family(self.root)
        self.folder = self.root / ".pixl"
        self.authored = production_plan.author(
            self.folder, codec.digest(store.load(self.folder)), plan(), self.root
        )

    def report(self, **extra):
        return service.call(
            "pixl_request_review",
            {**self.authored["request_review"], **extra},
            self.root,
        )

    def comparison(self, report):
        value = {
            "review_scope_sha256": report["review_scope_sha256"],
            "criterion_comparisons": [
                {
                    "criterion": r["id"],
                    "record_sha256": r["record_sha256"],
                    **dict.fromkeys(
                        (
                            "source_obligation",
                            "authority_basis",
                            "scope",
                            "literal_delta",
                            "discriminating_alternative",
                            "disposition",
                        ),
                        "Fixture assertion, not a semantic proof",
                    ),
                }
                for r in report["criteria"]
            ],
        }
        return value

    def save(self, value):
        (self.root / "comparison.json").write_text(json.dumps(value), encoding="utf-8")

    def test_exact_member_and_collective_rows_and_sources_without_acceptance(self):
        before = (self.folder / "state.px").read_bytes()
        result = self.report()
        self.assertEqual(
            result["criterion_ids"], ["next.motion.q.shape", "next.delivery.q.shape"]
        )
        self.assertEqual(
            result["criteria"][0]["check"], plan()["stages"][0]["criteria"][0]["check"]
        )
        self.assertEqual(result["sources"][0]["status"], "resolved")
        self.assertIsNone(result["consistent"])
        self.assertTrue(
            all(r["authority"] == "unclassified" for r in result["criteria"])
        )
        self.assertEqual(before, (self.folder / "state.px").read_bytes())

    def test_preparation_and_retry_return_same_exact_job_handoff(self):
        doc = store.load(self.folder)
        args = (
            self.folder,
            codec.digest(doc),
            "next.plan",
            "motion",
            "next.job",
            packet(doc),
            self.root,
        )
        first = production_plan.prepare(*args)
        second = production_plan.prepare(self.folder, first["hash"], *args[2:])
        self.assertEqual(first["request_review"], second["request_review"])
        result = self.report(job="next.job")
        self.assertEqual(
            result["request"]["request"]["arguments"],
            packet(doc)["request"]["arguments"],
        )
        self.assertEqual(result["request"]["state"], "prepared")
        self.assertIn("member", [i["id"] for i in result["controls"][0]["inputs"]])
        self.assertEqual(len(result["criteria"]), 2)

    def test_complete_coverage_is_not_a_semantic_verdict(self):
        report = self.report()
        self.save(self.comparison(report))
        result = self.report(comparison="comparison.json")
        self.assertTrue(result["comparison_coverage"]["complete"])
        self.assertEqual(
            result["comparison_coverage"]["semantic_verdict"], "not_assessed"
        )
        self.assertIsNone(result["consistent"])

    def test_job_progress_does_not_invalidate_unchanged_comparison(self):
        doc = store.load(self.folder)
        production_plan.prepare(
            self.folder,
            codec.digest(doc),
            "next.plan",
            "motion",
            "next.job",
            packet(doc),
            self.root,
        )
        original = self.report(job="next.job")
        self.save(self.comparison(original))
        jobs.dispatch(
            self.folder, codec.digest(store.load(self.folder)), "next.job", self.root
        )
        jobs.observe(
            self.folder,
            codec.digest(store.load(self.folder)),
            "next.job",
            "submitted",
            {"fixture": True},
            remote_id="fixture-remote",
            root=self.root,
        )
        current = self.report(job="next.job", comparison="comparison.json")
        self.assertNotEqual(current["request"]["state"], original["request"]["state"])
        self.assertEqual(current["request"]["remote_id"], "fixture-remote")
        self.assertNotEqual(current["state"]["sha256"], original["state"]["sha256"])
        self.assertEqual(
            current["review_scope_sha256"], original["review_scope_sha256"]
        )
        self.assertTrue(current["comparison_coverage"]["complete"])

    def test_missing_collective_duplicate_and_stale_comparison_are_visible(self):
        report = self.report()
        value = self.comparison(report)
        value["criterion_comparisons"][1] = value["criterion_comparisons"][0].copy()
        value["criterion_comparisons"][0]["scope"] = ""
        value["review_scope_sha256"] = "0" * 64
        self.save(value)
        coverage = self.report(comparison="comparison.json")["comparison_coverage"]
        self.assertFalse(coverage["complete"])
        self.assertEqual(coverage["missing"], ["next.delivery.q.shape"])
        self.assertEqual(coverage["duplicates"], ["next.motion.q.shape"])
        self.assertFalse(coverage["scope_current"])
        self.assertTrue(coverage["incomplete"])

    def test_changed_criterion_cannot_hide_behind_original_snapshot(self):
        original = self.report()
        doc = store.load(self.folder)
        doc.records["next.motion.q.shape"].fields["ck"] = "Changed restriction"
        (self.folder / "state.px").write_bytes(codec.encode(doc))
        result = self.report()
        self.assertEqual(result["criteria"][0]["record_status"], "changed")
        self.assertEqual(
            result["criteria"][0]["check"], original["criteria"][0]["check"]
        )
        self.assertNotEqual(
            result["review_scope_sha256"], original["review_scope_sha256"]
        )
        self.assertTrue(
            any(d["status"] == "changed_plan_context" for d in result["diagnostics"])
        )

    def test_changed_source_bytes_report_drift_without_claiming_entailment(self):
        doc = store.load(self.folder)
        source = self.root / doc.records["source"].fields["ur"]
        source.write_text("changed source\n", encoding="utf-8")
        report = self.report()
        self.assertEqual(report["sources"][0]["status"], "changed")
        self.assertIsNone(report["consistent"])

    def test_cli_uses_same_report(self):
        import sys

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pixl",
                "request-review",
                ".pixl/state.px",
                "--plan",
                "next.plan",
                "--root",
                str(self.root),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(
            json.loads(result.stdout)["review_scope_sha256"],
            self.report()["review_scope_sha256"],
        )

    def test_old_packet_arguments_cannot_silently_ignore_connected_options(self):
        with self.assertRaises(codec.PixlError):
            request_review.report(
                self.root, "missing.json", comparison="comparison.json"
            )

    def test_review_identity_survives_consumer_relocation(self):
        original = self.report()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "relocated"
            shutil.copytree(self.root, root)
            result = service.call(
                "pixl_request_review", self.authored["request_review"], root
            )
            self.assertEqual(
                original["review_scope_sha256"], result["review_scope_sha256"]
            )
            self.assertNotEqual(
                original["sources"][0]["absolute_path"],
                result["sources"][0]["absolute_path"],
            )
