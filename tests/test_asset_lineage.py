"""Lineage uses retained identities and claims without upgrading their meaning."""

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image

from pixl import asset_lineage, codec, jobs, store
from pixl.codec import Record, Ref
from tests.lifecycle_support import add_candidate, sample


class AssetLineageTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / ".pixl"
        store.initialize(self.folder, sample(self.root), self.root)

    def current(self):
        return store.load(self.folder)

    def expected(self):
        return codec.digest(self.current())

    def imported(self, id_, tool="create_image_pro_flash", arguments=None,
                 remote=None, provider="fixture", evidence=None):
        jobs.prepare(
            self.folder, self.expected(), id_, "task", ["output"], provider, tool,
            arguments or {"description": "synthetic local test"},
            {"type": "object", "additionalProperties": True},
            {"source": "local fixture", "observed_at": "2026-09-11T12:00:00+00:00",
             "evidence": {"fixture": True}},
            {"scope": "Local fixture", "evidence": {"fixture": True}},
            root=self.root,
        )
        jobs.dispatch(self.folder, self.expected(), id_, root=self.root)
        jobs.observe(self.folder, self.expected(), id_, "succeeded",
                     evidence or {"fixture": True}, remote_id=remote or id_ + "-remote",
                     root=self.root)
        source = self.root / (id_ + ".png")
        Image.new("RGBA", (2, 2), (len(id_) * 13 % 255, sum(id_.encode()) % 255, 90, 255)).save(source)
        jobs.import_artifact(self.folder, self.expected(), id_, "output", id_ + ".candidate",
                             source.name, {"fixture": True}, root=self.root)
        return id_ + ".candidate"

    def describe(self, id_, doc=None):
        return asset_lineage.describe(doc or self.current(), self.root, id_)

    def test_generation_intent_does_not_authenticate_execution_or_simulation(self):
        id_ = self.imported("seed")
        row = self.describe(id_)
        self.assertEqual(row["provenance_status"], "recorded_provider_import")
        self.assertFalse(row["remote_verified"])
        job = row["jobs"][0]
        self.assertEqual(job["operation"], "generation_request")
        self.assertIsNone(job["simulated"])
        self.assertFalse(job["remote_verified"])
        self.assertEqual(job["imports"][0]["artifact"]["id"], id_)
        self.assertEqual(job["imports"][0]["locator"], "/events/2")

    def test_explicit_controlled_claim_retained_but_name_does_not_imply_real(self):
        id_ = self.imported("controlled", remote="opaque", evidence={"provider_simulated": True})
        row = self.describe(id_)["jobs"][0]
        self.assertTrue(row["simulated"])
        self.assertEqual(row["simulation_claims"][0]["locator"], "/events/1/evidence/provider_simulated")

    def test_exact_scoped_remote_source_and_guarded_edit_chain(self):
        seed = self.imported("seed", remote="origin")
        self.imported("other", remote="origin", provider="other-provider")
        animation = self.imported("animation", "animate_image", {
            "first_frame_url": "https://api.pixellab.ai/mcp/images/origin/download"}, remote="animated")
        final = self.imported("edited", "pixelart_workbench", {"argv": ["edit", "job:animated", "--changes",
                             json.dumps([{"operation": "patch_pixels", "pixels": [[0, 0, "#00000000", "#ffffffff"]]}])]})
        row = self.describe(final)
        by_id = {job["id"]: job for job in row["jobs"]}
        self.assertEqual(set(by_id), {"seed", "animation", "edited"})
        self.assertEqual(by_id["edited"]["operation"], "deterministic_edit_request")
        self.assertEqual(by_id["edited"]["operation_details"]["patch_count"], 1)
        self.assertEqual(by_id["edited"]["source_requests"][0]["matching_candidates"], [animation])
        self.assertEqual(by_id["animation"]["source_requests"][0]["matching_candidates"], [seed])

    def test_upload_unknown_tool_and_unrecognized_urls_do_not_invent_origins(self):
        self.imported("seed", remote="looks-matching")
        id_ = self.imported("edited", "pixelart_workbench", {"argv": ["edit", "upload:looks-matching"],
                          "image_url": "https://example.test/looks-matching"})
        row = self.describe(id_)["jobs"][0]
        self.assertEqual(row["operation"], "provider_edit_request")
        self.assertTrue(all(source["resolution"] == "unresolved" for source in row["source_requests"]))
        unknown = self.imported("unknown", "looks_like_generate")
        self.assertEqual(self.describe(unknown)["jobs"][0]["operation"], "unknown")

    def test_malformed_url_is_unresolved_and_request_flags_are_not_evidence(self):
        id_ = self.imported("malformed", arguments={"image_url": "https://[", "simulated": True,
                                                  "provider_simulated": True})
        row = self.describe(id_)["jobs"][0]
        self.assertIsNone(row["simulated"])
        self.assertEqual(row["simulation_claims"], [])
        self.assertEqual(row["source_requests"][0]["resolution"], "unresolved")

    def test_empty_download_identity_does_not_match_a_prepared_job(self):
        id_ = self.imported("consumer", "animate_image", {
            "first_frame_url": "https://api.pixellab.ai/mcp/images//download"})
        jobs.prepare(
            self.folder, self.expected(), "prepared", "task", ["output"], "fixture",
            "create_image_pro_flash", {"description": "synthetic local test"},
            {"type": "object", "additionalProperties": True},
            {"source": "local fixture", "observed_at": "2026-09-11T12:00:00+00:00",
             "evidence": {"fixture": True}},
            {"scope": "Local fixture", "evidence": {"fixture": True}},
            root=self.root,
        )
        self.assertEqual(self.current().records["prepared"].fields["ri"], "")
        row = self.describe(id_)
        source = row["jobs"][0]["source_requests"][0]
        self.assertEqual(source["resolution"], "unresolved")
        self.assertEqual(source["matching_jobs"], [])
        self.assertEqual(source["matching_candidates"], [])
        self.assertEqual([job["id"] for job in row["jobs"]], ["consumer"])

    def test_source_matches_and_journal_reads_share_the_node_limit(self):
        for id_ in ["one", "two", "three"]:
            self.imported(id_, remote="shared")
        id_ = self.imported("consumer", "pixelart_workbench", {"argv": ["edit", "shared"]})
        with patch.dict(asset_lineage.LIMITS, {"jobs": 2, "source_matches": 2}):
            with patch.object(jobs, "_get", wraps=jobs._get) as reads:
                row = self.describe(id_)
            self.assertLessEqual(reads.call_count, 2)
        self.assertTrue(row["truncated"])
        self.assertLessEqual(len(row["jobs"]), 2)
        self.assertEqual(row["jobs"][0]["source_requests"][0]["resolution"], "truncated")

    def test_simulation_conflicts_and_scan_limits_remain_unknown(self):
        id_ = self.imported("conflict", evidence={"simulated": False, "response": {"provider_simulated": True}})
        job = self.describe(id_)["jobs"][0]
        self.assertIsNone(job["simulated"])
        self.assertTrue(job["simulation_conflict"])
        with patch.dict(asset_lineage.LIMITS, {"simulation_nodes": 1}):
            job = self.describe(id_)["jobs"][0]
        self.assertIsNone(job["simulated"])
        self.assertTrue(job["simulation_scan_truncated"])

    def test_ambiguous_remote_ids_and_cycles_remain_explicit_and_bounded(self):
        self.imported("one", "pixelart_workbench", {"argv": ["edit", "two-remote"]}, remote="shared")
        self.imported("two", "pixelart_workbench", {"argv": ["edit", "shared"]}, remote="two-remote")
        self.imported("three", remote="shared")
        row = self.describe("two.candidate")
        self.assertEqual(len(row["jobs"]), 3)
        source = next(job for job in row["jobs"] if job["id"] == "two")["source_requests"][0]
        self.assertEqual(source["resolution"], "ambiguous")
        self.assertEqual(source["matching_jobs"], ["one", "three"])

    def test_byte_equivalence_and_workflow_context_do_not_claim_parentage(self):
        id_ = self.imported("seed")
        doc = self.current()
        fields = copy.deepcopy(doc.records[id_].fields)
        fields["nm"] = "Rebound bytes with no explicit parent"
        doc.records["rebound"] = Record("rebound", "X", fields)
        doc.records["task"].fields["ip"] = [Ref(id_)]
        row = self.describe("rebound", doc)
        self.assertEqual(row["provenance_status"], "same_bytes_as_recorded_import")
        self.assertEqual(row["artifact"]["jobs"], [])
        self.assertEqual(row["same_bytes"][0]["candidate"], id_)
        self.assertEqual(row["workflow_inputs"][0]["candidate"], id_)
        self.assertNotIn("parent", row)

    def test_unrecorded_candidate_does_not_gain_provider_history(self):
        doc = self.current()
        add_candidate(doc, self.root, "local")
        row = self.describe("local", doc)
        self.assertEqual(row["provenance_status"], "unrecorded")
        self.assertEqual(row["jobs"], [])

    def test_changed_artifact_and_journal_bytes_fail_without_writes(self):
        id_ = self.imported("seed")
        doc = self.current()
        journal = doc.records[doc.records["seed"].fields["jr"].id]
        path = self.root / journal.fields["ur"]
        original = path.read_bytes()
        path.write_bytes(original + b" ")
        with self.assertRaisesRegex(codec.PixlError, "file_hash"):
            self.describe(id_, doc)
        path.write_bytes(original)
        candidate_path = self.root / doc.records[id_].fields["ur"]
        candidate_path.write_bytes(b"changed")
        with self.assertRaisesRegex(codec.PixlError, "file_hash"):
            self.describe(id_, doc)

    def test_payload_summary_is_bounded_and_exact_locator_is_available(self):
        id_ = self.imported("seed", evidence={"note": "x" * 3000})
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        row = self.describe(id_)
        self.assertTrue(row["truncated"])
        job = row["jobs"][0]
        self.assertLess(len(job["observations"][0]["evidence"]["note"]), 600)
        self.assertEqual(job["observations"][0]["locator"], "/events/1")
        self.assertTrue((self.root / job["journal"]["uri"]).is_file())
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
