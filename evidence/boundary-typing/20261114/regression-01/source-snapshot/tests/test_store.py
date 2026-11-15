import unittest
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import store
from pixl.codec import PixlError, Ref, Symbol, digest, record_hash
from tests.support import sample


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.doc = sample(self.root)
        self.folder = self.root / ".pixl"
        store.initialize(self.folder, self.doc, root=self.root)

    def candidate(self):
        doc = deepcopy(self.doc)
        doc.revision += 1
        doc.records["task"].fields["st"] = Symbol("active")
        return doc

    def test_commit_and_disk_resume_preserve_state_and_history(self):
        next_ = self.candidate()
        receipt = store.commit(self.folder, next_, digest(self.doc), root=self.root)
        self.assertEqual(receipt["hash"], digest(next_))
        self.assertEqual(store.load(self.folder), next_)
        self.assertTrue((self.folder / "history" / f"{digest(self.doc)}.px").is_file())
        self.assertFalse((self.folder / ".lock").exists())

    def test_stale_writer_rejected_without_changing_state(self):
        store.commit(self.folder, self.candidate(), digest(self.doc), root=self.root)
        with self.assertRaisesRegex(PixlError, "stale_write"):
            store.commit(self.folder, self.candidate(), digest(self.doc), root=self.root)
        self.assertEqual(store.load(self.folder).revision, 1)

    def test_exactly_one_concurrent_candidate_commits(self):
        def run(_):
            try:
                store.commit(self.folder, self.candidate(), digest(self.doc), root=self.root)
                return "committed"
            except PixlError as e:
                return e.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(run, [0, 1]))
        self.assertEqual(results.count("committed"), 1)
        self.assertEqual(store.load(self.folder).revision, 1)

    def test_revision_skip_and_disappearing_ids_rejected(self):
        doc = self.candidate()
        doc.revision = 8
        with self.assertRaisesRegex(PixlError, "revision"):
            store.commit(self.folder, doc, digest(self.doc), root=self.root)
        doc.revision = 1
        del doc.records["task"]
        with self.assertRaisesRegex(PixlError, "record_removal"):
            store.commit(self.folder, doc, digest(self.doc), root=self.root)

    def test_invalid_evidence_never_published(self):
        doc = self.candidate()
        (self.root / "asset.txt").write_text("changed")
        with self.assertRaisesRegex(PixlError, "file_hash"):
            store.commit(self.folder, doc, digest(self.doc), root=self.root)
        self.assertEqual(store.load(self.folder), self.doc)

    def test_invalid_task_transition_rejected(self):
        doc = self.candidate()
        doc.records["task"].fields["st"] = Symbol("done")
        with self.assertRaisesRegex(PixlError, "transition"):
            store.commit(self.folder, doc, digest(self.doc), root=self.root)

    def test_initialization_does_not_overwrite_existing_store(self):
        with self.assertRaisesRegex(PixlError, "exists"):
            store.initialize(self.folder, self.doc, root=self.root)

    def test_done_dependency_change_requires_reopening_even_with_refreshed_proof(self):
        active = self.candidate()
        store.commit(self.folder, active, digest(self.doc), root=self.root)
        done = deepcopy(active)
        done.revision = 2
        done.records["task"].fields["st"] = Symbol("done")
        done.records["task"].fields["ev"] = [Ref("proof")]
        store.commit(self.folder, done, digest(active), root=self.root)
        changed = deepcopy(done)
        changed.revision = 3
        changed.records["style"].fields["li"] = "new intent"
        for binding in changed.records["proof"].fields["bs"]:
            binding["dg"] = record_hash(changed.records[binding["rf"].id])
        with self.assertRaisesRegex(PixlError, "reopen_required"):
            store.commit(self.folder, changed, digest(done), root=self.root)

    def test_history_symlink_cannot_redirect_publication(self):
        outside = self.root / "external"
        outside.mkdir()
        another = self.root / "another"
        another.mkdir()
        try:
            (another / "history").symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest("symlink privilege unavailable")
        with self.assertRaisesRegex(PixlError, "store_path"):
            store.initialize(another, self.doc, root=self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_supersession_preserves_old_receipt_and_reactivation_is_rejected(self):
        from pixl.graph import proof_scope
        next_ = deepcopy(self.doc)
        next_.revision = 1
        old_bindings = deepcopy(next_.records["proof"].fields["bs"])
        next_.records["proof"].fields["ob"] = True
        replacement = deepcopy(self.doc.records["proof"])
        replacement.id = "proof2"
        next_.records["proof2"] = replacement
        next_.records["decision"].fields["pc"] = [Ref("proof2")]
        replacement.fields["bs"] = [{"rf": Ref(id_), "dg": record_hash(next_.records[id_])}
                                     for id_ in sorted(proof_scope(next_, ["decision"]))]
        store.commit(self.folder, next_, digest(self.doc), root=self.root)
        saved = store.load(self.folder)
        self.assertEqual(saved.records["proof"].fields["bs"], old_bindings)
        reactivated = deepcopy(saved)
        reactivated.revision += 1
        reactivated.records["proof"].fields["ob"] = False
        with self.assertRaisesRegex(PixlError, "evidence_immutable"):
            store.commit(self.folder, reactivated, digest(saved), root=self.root)
