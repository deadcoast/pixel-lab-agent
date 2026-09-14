import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from pixl import codec, graph, inspection, store
from pixl.codec import PixlError
from tests.inspection_support import options, project


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        project(self.root)
        self.folder = self.root / ".pixl"

    def prepare(self):
        return inspection.prepare(
            self.folder,
            codec.digest(store.load(self.folder)),
            "candidate",
            "packet",
            options(),
            self.root,
        )

    def declaration(self, result, status="fail", delivered=None):
        return {
            "reviewer": "actor",
            "observed_at": datetime.now(UTC).isoformat(),
            "observations": [
                {
                    "view": result["views"][0]["id"],
                    "delivered_size": delivered,
                    "note": "Observed missing antenna.",
                }
            ],
            "verdicts": [
                {
                    "criterion": "q.visual",
                    "status": status,
                    "reason": "Missing antenna",
                    "supersedes": None,
                }
            ],
            "next_action": "Retain a new candidate.",
            "limitations": ["No engine project."],
        }

    def review(self, value, id_="review"):
        return inspection.review(
            self.folder,
            codec.digest(store.load(self.folder)),
            "packet",
            id_,
            value,
            self.root,
        )

    def test_prepare_no_verdict_and_cold_relocation(self):
        result = self.prepare()
        doc = store.load(self.folder)
        self.assertFalse(any(r.kind in ("E", "V") for r in doc.records.values()))
        self.assertEqual(result["views"][0]["id"], "packet.view.0")
        with tempfile.TemporaryDirectory() as temp:
            copied = Path(temp) / "project"
            shutil.copytree(self.root, copied)
            packet = inspection.report(store.load(copied / ".pixl"), copied, "packet")[
                "packets"
            ][0]
            self.assertEqual(packet["binding_drift"], [])
            self.assertEqual(packet["criteria"][1]["status"], "unperformed")

    def test_fail_and_explicit_supersession(self):
        result = self.prepare()
        value = self.declaration(result)
        saved = self.review(value)
        doc = store.load(self.folder)
        graph.validate(doc, self.root)
        old = saved["verdicts"][0]
        with self.assertRaises(PixlError):
            self.review(value, "replacement")
        value["verdicts"][0]["supersedes"] = old
        self.review(value, "replacement")
        self.assertTrue(store.load(self.folder).records[old].fields["ob"])

    def test_partial_or_unknown_cannot_pass(self):
        result = self.prepare()
        for delivered in (None, [1, 1], [32, 32]):
            with self.subTest(delivered=delivered), self.assertRaises(PixlError):
                self.review(self.declaration(result, "pass", delivered))

    def test_full_coverage_pass_and_unavailable_engine(self):
        result = self.prepare()
        value = self.declaration(result, "pass")
        value["observations"] = [
            {
                "view": v["id"],
                "delivered_size": [v["width"], v["height"]],
                "note": "Inspected.",
            }
            for v in result["views"]
        ]
        value["verdicts"].append(
            {
                "criterion": "q.engine",
                "status": "unavailable",
                "reason": "No engine project.",
                "supersedes": None,
            }
        )
        saved = self.review(value)
        doc = store.load(self.folder)
        self.assertEqual(doc.records[saved["verdicts"][1]].fields["ev"], [])

    def test_stale_state_source_and_reused_id(self):
        expected = codec.digest(store.load(self.folder))
        self.prepare()
        with self.assertRaises(PixlError):
            inspection.prepare(
                self.folder, expected, "candidate", "other", options(), self.root
            )
        with self.assertRaises(PixlError):
            self.prepare()
        (self.root / "candidate.png").write_bytes(b"changed")
        with self.assertRaises(PixlError):
            inspection.prepare(
                self.folder,
                codec.digest(store.load(self.folder)),
                "candidate",
                "other",
                options(),
                self.root,
            )

    def test_amendment_preserves_original_check_and_blocks_review(self):
        result = self.prepare()
        doc = store.load(self.folder)
        original = doc.records["q.visual"].fields["ck"]
        expected = codec.digest(doc)
        doc.records["q.visual"].fields["ck"] = "Amended condition."
        doc.revision += 1
        store.commit(self.folder, doc, expected, self.root)
        packet = inspection.report(store.load(self.folder), self.root, "packet")[
            "packets"
        ][0]
        self.assertIn("q.visual", packet["binding_drift"])
        self.assertEqual(packet["criteria"][1]["check"], original)
        with self.assertRaises(PixlError):
            self.review(self.declaration(result))

    def test_tampered_typed_projection_rejected(self):
        self.prepare()
        doc = store.load(self.folder)
        doc.records["packet"].fields["mt"]["candidate"] = "candidate"
        with self.assertRaises(PixlError):
            inspection.report(doc, self.root, "packet")

    def test_new_candidate_unperformed(self):
        result = self.prepare()
        self.review(self.declaration(result))
        doc = store.load(self.folder)
        expected = codec.digest(doc)
        other = copy.deepcopy(doc.records["candidate"])
        other.id = "candidate2"
        doc.records[other.id] = other
        doc.revision += 1
        store.commit(self.folder, doc, expected, self.root)
        inspection.prepare(
            self.folder,
            codec.digest(doc),
            "candidate2",
            "packet2",
            options(),
            self.root,
        )
        packet = inspection.report(store.load(self.folder), self.root, "packet2")[
            "packets"
        ][0]
        self.assertTrue(all(q["status"] == "unperformed" for q in packet["criteria"]))

    def test_superseded_receipt_still_has_exact_retained_closure(self):
        result = self.prepare()
        self.review(self.declaration(result))
        doc = store.load(self.folder)
        doc.records["review.verdict.0"].fields["ob"] = True
        receipt = doc.records["review.evidence.0"]
        receipt.fields["ob"] = True
        receipt.fields["bs"] = receipt.fields["bs"][:1]
        graph.validate(doc, self.root)
        with self.assertRaises(PixlError):
            inspection.report(doc, self.root, "packet")

    def test_malformed_reviewer_is_structured_error(self):
        result = self.prepare()
        value = self.declaration(result)
        value["reviewer"] = []
        with self.assertRaises(PixlError):
            self.review(value)

    def test_review_cannot_hide_by_removing_its_metadata_tag(self):
        result = self.prepare()
        self.review(self.declaration(result))
        doc = store.load(self.folder)
        for record in doc.records.values():
            if record.kind in ("V", "E"):
                record.fields["ob"] = True
        doc.records["review"].fields.pop("mt")
        graph.validate(doc, self.root)
        with self.assertRaises(PixlError):
            inspection.report(doc, self.root, "packet")

    def test_reference_only_failure_rejected(self):
        result = self.prepare()
        value = self.declaration(result)
        value["observations"][0]["view"] = next(
            v["id"] for v in result["views"] if v["source"] == "reference"
        )
        with self.assertRaises(PixlError):
            self.review(value)

    def test_boolean_projection_version_rejected(self):
        self.prepare()
        doc = store.load(self.folder)
        doc.records["packet"].fields["mt"]["version"] = True
        graph.validate(doc, self.root)
        with self.assertRaises(PixlError):
            inspection.report(doc, self.root, "packet")

    def test_rehashed_manifest_float_width_rejected(self):
        self.prepare()
        doc = store.load(self.folder)
        artifact = doc.records["packet"]
        old_path = self.root / artifact.fields["ur"]
        value = json.loads(old_path.read_bytes())
        value["rendering"]["views"][0]["width"] = 32.0
        data = inspection._bytes(value)
        sha = hashlib.sha256(data).hexdigest()
        directory = old_path.parent.parent / sha
        shutil.copytree(old_path.parent, directory)
        (directory / "manifest.json").write_bytes(data)
        old_prefix = old_path.parent.relative_to(self.root).as_posix() + "/"
        new_prefix = directory.relative_to(self.root).as_posix() + "/"
        for record in doc.records.values():
            if record.kind == "X" and record.fields["ur"].startswith(old_prefix):
                record.fields["ur"] = (
                    new_prefix + record.fields["ur"][len(old_prefix) :]
                )
        artifact.fields["dg"] = sha
        graph.validate(doc, self.root)
        with self.assertRaises(PixlError):
            inspection.report(doc, self.root, "packet")


if __name__ == "__main__":
    unittest.main()
