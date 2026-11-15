"""Actual local family snapshots; synthetic acceptance never means real art approval."""

import importlib
import importlib.util
import json
import os
import shutil
import subprocess
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, graph, store
from pixl.codec import PixlError, Record, Ref, Symbol


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(
            importlib.util.find_spec("pixl.delivery"),
            "family delivery operation is missing",
        )
        self.delivery = importlib.import_module("pixl.delivery")
        from tests.family_support import family

        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / ".pixl"
        self.doc = family(self.root, self.folder)

    def expected(self):
        return codec.digest(store.load(self.folder))

    def snapshot(self, candidate="package"):
        return self.delivery.snapshot(
            self.folder, self.expected(), "delivery.output", candidate, self.root
        )

    def amend(self, doc):
        doc.revision = store.load(self.folder).revision + 1
        return store.commit(self.folder, doc, self.expected(), self.root)

    def manifest(self, candidate="package"):
        doc = store.load(self.folder)
        path = self.root / doc.records[candidate].fields["ur"]
        return path, json.loads(path.read_bytes())

    def inventory(self):
        return {
            p.relative_to(self.folder).as_posix(): p.read_bytes()
            for p in self.folder.rglob("*")
            if p.is_file()
        }

    def unpublished_snapshot(self):
        captured = {}

        def intercept(folder, candidate, expected, root):
            captured["candidate"] = deepcopy(candidate)
            raise RuntimeError("publication intercepted for direct-commit regression")

        with (
            patch("pixl.delivery.store.commit", side_effect=intercept),
            self.assertRaisesRegex(RuntimeError, "publication intercepted"),
        ):
            self.snapshot()
        return captured["candidate"]

    def test_generic_snapshot_publication_cannot_also_activate_the_task(self):
        candidate = self.unpublished_snapshot()
        candidate.records["delivery.task"].fields["st"] = Symbol("active")
        before = (self.folder / "state.px").read_bytes()
        with self.assertRaisesRegex(PixlError, "delivery_publication"):
            store.commit(self.folder, candidate, self.expected(), self.root)
        self.assertEqual((self.folder / "state.px").read_bytes(), before)

    def test_rooted_report_rejects_redirected_manifest_directory(self):
        self.snapshot()
        path, _ = self.manifest()
        original = path.parent
        target = self.root / "retained-copy" / original.name
        self.assertTrue(original.resolve().is_relative_to(self.root.resolve()))
        self.assertTrue(target.resolve().is_relative_to(self.root.resolve()))
        target.parent.mkdir()
        original.rename(target)
        if os.name == "nt":
            quote = lambda value: "'" + str(value).replace("'", "''") + "'"
            command = f"New-Item -ItemType Junction -Path {quote(original)} -Value {quote(target)} | Out-Null"
            created = subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
                capture_output=True,
                check=False,
                timeout=20,
            )
            self.assertEqual(created.returncode, 0, created.stderr.decode())
        else:
            original.symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(PixlError, "delivery_storage"):
            self.delivery.report(store.load(self.folder), self.root)

    def test_new_snapshot_cannot_use_unretained_working_storage(self):
        candidate = self.unpublished_snapshot()
        artifact = candidate.records["package"]
        original = self.root / artifact.fields["ur"]
        target = self.root / "working" / original.parent.name
        shutil.copytree(original.parent, target)
        artifact.fields["ur"] = (
            (target / "manifest.json").relative_to(self.root).as_posix()
        )
        with self.assertRaisesRegex(PixlError, "delivery_storage"):
            store.commit(self.folder, candidate, self.expected(), self.root)

    def test_new_snapshot_requires_unchanged_previously_saved_plan(self):
        candidate = self.unpublished_snapshot()
        candidate.records["delivery.output"].fields["nm"] = (
            "Changed after capturing snapshot"
        )
        with self.assertRaisesRegex(PixlError, "delivery_plan"):
            store.commit(self.folder, candidate, self.expected(), self.root)

    def test_snapshot_retains_actual_member_bytes_without_acceptance(self):
        before = store.load(self.folder)
        result = self.snapshot()
        after = store.load(self.folder)
        self.assertFalse(result["accepted"])
        self.assertFalse(result["remote_executed"])
        self.assertEqual(set(after.records) - set(before.records), {"package"})
        for key in before.records:
            self.assertEqual(before.records[key], after.records[key])
        path, manifest = self.manifest()
        self.assertEqual(path.parent.name, after.records["package"].fields["dg"])
        self.assertEqual(manifest["source_state_sha256"], codec.digest(before))
        self.assertEqual(
            after.records["package"].fields["xs"],
            [Ref("sample"), *[Ref(item["candidate"]) for item in manifest["files"]]],
        )
        for item in manifest["files"]:
            self.assertEqual(
                (path.parent / item["path"]).read_bytes(),
                (self.root / item["source_path"]).read_bytes(),
            )
        self.assertEqual(after.records["delivery.task"].fields["ca"], [])
        self.assertEqual(after.records["delivery.task"].fields["vr"], [])

    def test_cold_report_reads_current_snapshot_without_changing_state(self):
        self.snapshot()
        before = self.inventory()
        report = self.delivery.report(
            store.load(self.folder), self.root, "delivery.output"
        )
        self.assertTrue(report["files_verified"])
        self.assertEqual(report["families"][0]["snapshots"][0]["candidate"], "package")
        self.assertEqual(report["families"][0]["snapshots"][0]["stale"], [])
        self.assertEqual(self.inventory(), before)

    def test_collective_proof_contains_baseline_members_and_destination(self):
        self.snapshot()
        scope = graph.proof_scope(store.load(self.folder), ["package"])
        self.assertTrue(
            {
                "sample",
                "member",
                "member.output",
                "delivery.output",
                "destination",
                "q.continuity",
                "q.delivery.engine",
            }
            <= scope
        )

    def test_stale_writer_creates_no_files_or_candidate(self):
        before = self.inventory()
        with self.assertRaisesRegex(PixlError, "stale_write"):
            self.delivery.snapshot(
                self.folder, "0" * 64, "delivery.output", "package", self.root
            )
        self.assertEqual(self.inventory(), before)

    def test_failed_publication_retains_state_and_original_files(self):
        before = (self.folder / "state.px").read_bytes()
        original = (self.root / self.doc.records["member"].fields["ur"]).read_bytes()
        with (
            patch(
                "pixl.delivery.store.commit",
                side_effect=PixlError("stale_write", "competing writer"),
            ),
            self.assertRaisesRegex(PixlError, "stale_write"),
        ):
            self.snapshot()
        self.assertEqual((self.folder / "state.px").read_bytes(), before)
        self.assertEqual(
            (self.root / self.doc.records["member"].fields["ur"]).read_bytes(), original
        )

    def test_pending_unknown_member_job_blocks_snapshot_and_is_reported(self):
        doc = store.load(self.folder)
        doc.records["pending"] = Record(
            "pending",
            "J",
            {
                "tk": Ref("member.task"),
                "tl": "synthetic",
                "ah": "a" * 64,
                "si": Symbol("unknown"),
                "ri": "",
                "ev": [],
            },
        )
        self.amend(doc)
        with self.assertRaisesRegex(PixlError, "delivery_blocked"):
            self.snapshot()
        report = self.delivery.report(store.load(self.folder), self.root)
        self.assertEqual(report["families"][0]["pending_jobs"][0]["id"], "pending")

    def test_reopened_member_blocks_new_snapshot(self):
        doc = store.load(self.folder)
        doc.records["member.task"].fields["st"] = Symbol("open")
        self.amend(doc)
        with self.assertRaisesRegex(PixlError, "delivery_blocked"):
            self.snapshot()

    def test_snapshot_allowed_with_unresolved_destination_without_finishing_task(self):
        doc = store.load(self.folder)
        doc.records["destination"].fields.update(
            st=Symbol("unresolved"), vl=None, so=[]
        )
        self.amend(doc)
        self.snapshot()
        report = self.delivery.report(store.load(self.folder), self.root)
        self.assertTrue(report["families"][0]["blockers"])
        self.assertEqual(
            store.load(self.folder).records["delivery.task"].fields["st"],
            Symbol("open"),
        )

    def test_membership_amendment_retains_previous_snapshot(self):
        self.snapshot()
        path, manifest = self.manifest()
        before = path.read_bytes()
        doc = store.load(self.folder)
        doc.records["delivery.output"].fields["mb"] = [Ref("output")]
        self.amend(doc)
        self.assertEqual(path.read_bytes(), before)
        report = self.delivery.report(store.load(self.folder), self.root)
        self.assertTrue(report["families"][0]["snapshots"][0]["stale"])
        self.assertEqual(len(manifest["files"]), 2)
        self.snapshot("revised.package")
        _, revised = self.manifest("revised.package")
        self.assertEqual(len(revised["files"]), 1)

    def test_actual_copy_corruption_fails_rooted_validation(self):
        self.snapshot()
        path, manifest = self.manifest()
        (path.parent / manifest["files"][0]["path"]).write_bytes(
            b"damaged package member"
        )
        with self.assertRaisesRegex(PixlError, "delivery_file"):
            self.delivery.report(store.load(self.folder), self.root)

    def test_published_manifest_and_constituent_records_are_immutable(self):
        self.snapshot()
        for target in ["package", "sample", "member"]:
            with self.subTest(target=target):
                doc = store.load(self.folder)
                doc.records[target].fields["nm"] += " rewritten"
                with self.assertRaises(PixlError):
                    self.amend(doc)

    def test_cannot_shed_family_extension(self):
        self.snapshot()
        doc = store.load(self.folder)
        for key in ["bs", "mb", "ds"]:
            doc.records["delivery.output"].fields.pop(key)
        with self.assertRaises(PixlError):
            self.amend(doc)

    def test_direct_commit_cannot_relocate_manifest_to_working_storage(self):
        self.snapshot()
        doc = store.load(self.folder)
        path, _ = self.manifest()
        target = self.root / "working" / path.parent.name
        shutil.copytree(path.parent, target)
        doc.records["package"].fields["ur"] = (
            (target / "manifest.json").relative_to(self.root).as_posix()
        )
        with self.assertRaises(PixlError):
            self.amend(doc)

    def test_px1_report_does_not_infer_a_family(self):
        with self.assertRaisesRegex(PixlError, "family_format"):
            self.delivery.report(store.empty_project(), self.root)

    def test_candidate_id_reuse_is_rejected_before_copying(self):
        self.snapshot()
        before = self.inventory()
        with self.assertRaisesRegex(PixlError, "delivery_candidate"):
            self.snapshot()
        self.assertEqual(self.inventory(), before)

    def test_unavailable_engine_is_not_accepted_delivery(self):
        from tests.lifecycle_support import add_verdict

        self.snapshot()
        doc = store.load(self.folder)
        doc.records["delivery.task"].fields["ca"] = [Ref("package")]
        add_verdict(
            doc, self.root, "package", "q.continuity", "pass", "family.continuity"
        )
        add_verdict(
            doc,
            self.root,
            "package",
            "q.delivery.engine",
            "unavailable",
            "family.engine",
        )
        self.amend(doc)
        report = self.delivery.report(store.load(self.folder), self.root)
        statuses = {r["id"]: r["status"] for r in report["families"][0]["requirements"]}
        self.assertEqual(statuses["q.delivery.engine"], "unavailable")
        self.assertEqual(
            store.load(self.folder).records["delivery.task"].fields["st"],
            Symbol("open"),
        )

    def test_changed_selection_cannot_receive_current_family_verdict(self):
        from tests.lifecycle_support import add_verdict

        self.snapshot()
        doc = store.load(self.folder)
        doc.records["member.task"].fields["st"] = Symbol("open")
        doc.records["member.task"].fields["ca"] = []
        self.amend(doc)
        doc = store.load(self.folder)
        add_verdict(
            doc, self.root, "package", "q.continuity", "pass", "stale.continuity"
        )
        with self.assertRaisesRegex(PixlError, "family_stale"):
            self.amend(doc)


if __name__ == "__main__":
    unittest.main()
