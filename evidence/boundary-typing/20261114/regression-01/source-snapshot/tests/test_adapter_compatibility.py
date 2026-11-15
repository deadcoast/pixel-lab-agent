"""Saved adapter compatibility without reinterpretation, migration or acceptance."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from pixl import adapter_versions, authoring_context, codec, production_plan, production_review, store, successor_review
from pixl.codec import PixlError
from tests.family_support import family
from tests.test_production_plan import packet, plan


class VersionPolicyTests(unittest.TestCase):
    def test_preserves_numeric_schema_versions_and_legacy_objects(self):
        for version in (1, 1.0):
            value = {"version": version, "other": "unchanged"}
            self.assertIs(adapter_versions.require_version(value, "fixture"), value)
        legacy = {"criterion_comparisons": []}
        self.assertIs(adapter_versions.require_version(legacy, "fixture", optional=True), legacy)
        self.assertIs(adapter_versions.require_version({"version": 1}, "fixture", exact_int=True)["version"], 1)

    def test_unknown_missing_boolean_and_explicit_null_do_not_become_version_one(self):
        for value in ({}, {"version": 2}, {"version": True}, {"version": "1"}, {"version": None}, []):
            with self.subTest(value=value), self.assertRaises(PixlError) as error:
                adapter_versions.require_version(value, "fixture")
            self.assertEqual(error.exception.code, "adapter_version")
        for value in (None, True, 2):
            with self.assertRaises(PixlError):
                adapter_versions.require_version({"version": value}, "fixture", optional=True)
        with self.assertRaises(PixlError):
            adapter_versions.require_version({"version": 1.0}, "fixture", exact_int=True)


class SavedProductionCompatibilityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.folder = self.root / ".pixl"
        family(self.root)
        self.authored = plan()
        production_plan.author(self.folder, codec.digest(store.load(self.folder)), self.authored, self.root)

    def tree(self):
        return {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.root.rglob("*") if p.is_file()}

    def publish(self, change, snapshot_change=None):
        doc = store.load(self.folder)
        expected = codec.digest(doc)
        marker = doc.records["next.plan"]
        if snapshot_change:
            path = self.root / marker.fields["ur"]
            snapshot = json.loads(path.read_bytes())
            snapshot_change(snapshot)
            path.write_text(json.dumps(snapshot), encoding="utf-8")
            marker.fields["dg"] = hashlib.sha256(path.read_bytes()).hexdigest()
        change(marker)
        doc.revision += 1
        store.commit(self.folder, doc, expected, self.root)
        return store.load(self.folder)

    def readers(self, doc):
        return (
            lambda: production_plan.author(self.folder, codec.digest(doc), self.authored, self.root),
            lambda: production_plan.prepare(self.folder, codec.digest(doc), "next.plan", "motion", "next.job", packet(doc), self.root),
            lambda: production_review.report(self.root, ".pixl/state.px", "next.plan"),
            lambda: successor_review._plan(self.root, doc, "next.plan"),
        )

    def test_future_binding_blocks_every_plan_route_and_keeps_wire_readable(self):
        doc = self.publish(lambda marker: marker.fields["mt"].update(binding="pixl.production.plan/2"))
        before = self.tree()
        self.assertEqual(codec.digest(store.load(self.folder)), codec.digest(doc))
        reasons = production_plan.blockers(doc, "next.motion.task", self.root, self.folder)
        self.assertEqual(len(reasons), 1)
        self.assertIn("adapter_version", reasons[0])
        for read in self.readers(doc):
            with self.subTest(read=read), self.assertRaisesRegex(PixlError, "adapter_version"):
                read()
        for focus in ("next.plan", "next.motion.task", "next.motion.output"):
            with self.subTest(focus=focus), self.assertRaisesRegex(PixlError, "adapter_version"):
                authoring_context.report(self.folder / "state.px", focus, self.root)
        self.assertEqual(self.tree(), before)

    def test_future_snapshot_is_rejected_before_any_job_or_state_write(self):
        doc = self.publish(lambda marker: None, lambda snapshot: snapshot.update(version=2))
        before = self.tree()
        reasons = production_plan.blockers(doc, "next.motion.task", self.root, self.folder)
        self.assertIn("unsupported version 2", reasons[0])
        for read in self.readers(doc):
            with self.subTest(read=read), self.assertRaisesRegex(PixlError, "adapter_version"):
                read()
        self.assertEqual(self.tree(), before)

    def test_changed_snapshot_cannot_be_reused_or_prepared(self):
        doc = store.load(self.folder)
        path = self.root / doc.records["next.plan"].fields["ur"]
        path.write_bytes(path.read_bytes() + b" ")
        before = self.tree()
        for read in self.readers(doc):
            with self.subTest(read=read), self.assertRaisesRegex(PixlError, "file_hash|plan snapshot changed"):
                read()
        self.assertEqual(self.tree(), before)

    def test_numeric_v1_snapshot_and_plan_reuse_preserves_saved_bytes(self):
        def numeric(snapshot):
            snapshot["version"] = snapshot["plan"]["version"] = 1.0
        doc = self.publish(lambda marker: None, numeric)
        before = self.tree()
        self.assertEqual(production_plan.blockers(doc, "next.motion.task", self.root, self.folder), [])
        self.assertTrue(self.readers(doc)[0]()["already_authored"])
        self.assertEqual(production_review.report(self.root, ".pixl/state.px", "next.plan")["plan"]["id"], "next.plan")
        self.assertEqual(self.tree(), before)

    def test_unrelated_binding_stays_outside_plan_adapter(self):
        doc = store.load(self.folder)
        doc.records["next.plan"].fields["mt"]["binding"] = "example.unrelated/2"
        self.assertEqual(production_plan.blockers(doc, "next.motion.task", self.root, self.folder), [])

    def test_future_authored_input_and_stage_packet_preserve_state(self):
        doc = store.load(self.folder)
        future_plan = copy.deepcopy(self.authored)
        future_plan.update(id="future", version=2)
        future_packet = packet(doc)
        future_packet["version"] = 2
        before = self.tree()
        for call in (
            lambda: production_plan.author(self.folder, codec.digest(doc), future_plan, self.root),
            lambda: production_plan.prepare(self.folder, codec.digest(doc), "next.plan", "motion", "future.job", future_packet, self.root),
        ):
            with self.assertRaisesRegex(PixlError, "adapter_version"):
                call()
        self.assertEqual(self.tree(), before)

    def test_legacy_comparison_and_numeric_v1_keep_identity_future_is_rejected(self):
        report = production_review.report(self.root, ".pixl/state.px", "next.plan")
        comparison = {
            "review_scope_sha256": report["review_scope_sha256"],
            "criterion_comparisons": [{
                "criterion": row["id"], "record_sha256": row["record_sha256"],
                **dict.fromkeys(("source_obligation", "authority_basis", "scope", "literal_delta", "discriminating_alternative", "disposition"), "Fixture prose; no semantic proof"),
            } for row in report["criteria"]],
        }
        for version in (None, 1, 1.0, 2):
            value = copy.deepcopy(comparison)
            if version is not None:
                value["version"] = version
            path = self.root / "comparison.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            before = self.tree()
            if version == 2:
                with self.assertRaisesRegex(PixlError, "adapter_version"):
                    production_review.report(self.root, ".pixl/state.px", "next.plan", comparison=path.name)
            else:
                result = production_review.report(self.root, ".pixl/state.px", "next.plan", comparison=path.name)
                self.assertTrue(result["comparison_coverage"]["complete"])
                self.assertEqual(result["comparison_coverage"]["semantic_verdict"], "not_assessed")
            self.assertEqual(self.tree(), before)


if __name__ == "__main__":
    unittest.main()
