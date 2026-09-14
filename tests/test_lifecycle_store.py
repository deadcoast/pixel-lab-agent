import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import codec, graph, store
from tests.lifecycle_support import add_candidate, add_verdict, sample


class LifecycleStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / ".pixl"
        self.doc = sample(self.root)
        store.initialize(self.folder, self.doc, self.root)

    def publish(self, candidate):
        candidate.revision = self.doc.revision + 1
        store.commit(self.folder, candidate, codec.digest(self.doc), self.root)
        self.doc = store.load(self.folder)

    def evaluated(self, done=False):
        doc = deepcopy(self.doc)
        add_candidate(doc, self.root, "candidate")
        for domain in ("mechanical", "visual", "engine"):
            add_verdict(
                doc, self.root, "candidate", "q." + domain, "pass", "v." + domain
            )
        doc.records["task"].fields["st"] = codec.Symbol("done" if done else "active")
        return doc

    def test_criteria_must_predate_verdicts(self):
        doc = deepcopy(self.doc)
        add_candidate(doc, self.root, "candidate")
        doc.records["q.visual"].fields["ck"] = (
            "A weaker condition chosen after seeing the candidate"
        )
        # Bind valid current bytes so rejection comes from planning order.
        add_verdict(doc, self.root, "candidate", "q.visual", "pass", "v.visual")
        with self.assertRaisesRegex(codec.PixlError, "acceptance_plan"):
            self.publish(doc)
        self.assertEqual(store.load(self.folder), self.doc)

    def test_cannot_initialize_with_already_evaluated_lifecycle(self):
        with self.assertRaisesRegex(codec.PixlError, "acceptance_plan"):
            store.initialize(self.root / "new", self.evaluated(), self.root)

    def test_new_verdict_cannot_arrive_as_unproven_superseded_history(self):
        doc = deepcopy(self.doc)
        add_candidate(doc, self.root, "candidate")
        criterion = deepcopy(doc.records["q.visual"])
        criterion.id = "invented_history_criterion"
        doc.records[criterion.id] = criterion
        verdict = codec.Record(
            "invented_history",
            "V",
            {
                "tk": codec.Ref("task"),
                "rq": codec.Ref(criterion.id),
                "xr": codec.Ref("candidate"),
                "st": codec.Symbol("pass"),
                "wh": codec.Ref("actor"),
                "wy": "Never observed",
                "at": "2026-09-11",
                "ev": [],
                "ob": True,
            },
        )
        doc.records[verdict.id] = verdict
        doc.records["task"].fields["vr"].append(codec.Ref(verdict.id))
        with self.assertRaisesRegex(codec.PixlError, "verdict_history"):
            self.publish(doc)

    def test_verdict_is_immutable_but_supersession_is_preserved(self):
        self.publish(self.evaluated())
        doc = deepcopy(self.doc)
        doc.records["v.visual"].fields["wy"] = "rewritten history"
        with self.assertRaisesRegex(codec.PixlError, "verdict_immutable"):
            self.publish(doc)
        doc = deepcopy(self.doc)
        doc.records["v.visual"].fields["ob"] = True
        add_verdict(doc, self.root, "candidate", "q.visual", "fail", "v.visual.reject")
        self.publish(doc)
        self.assertTrue(self.doc.records["v.visual"].fields["ob"])
        self.assertEqual(
            self.doc.records["v.visual.reject"].fields["st"], codec.Symbol("fail")
        )

    def test_unrelated_intake_edit_does_not_reopen_completed_sample(self):
        self.publish(self.evaluated())
        doc = deepcopy(self.doc)
        doc.records["task"].fields["st"] = codec.Symbol("done")
        self.publish(doc)
        doc = deepcopy(self.doc)
        doc.records["project"].fields["nm"] = "Changed display name"
        unrelated = codec.Record(
            "other_choice",
            "I",
            {
                "pr": codec.Ref("project"),
                "wh": codec.Ref("user"),
                "ky": "unrelated_background",
                "st": codec.Symbol("unresolved"),
                "vl": None,
                "so": [],
                "wy": "For a later background task",
            },
        )
        doc.records[unrelated.id] = unrelated
        doc.records["project"].fields["in"].append(codec.Ref(unrelated.id))
        self.publish(doc)
        self.assertEqual(self.doc.records["task"].fields["st"], codec.Symbol("done"))

    def test_contract_change_requires_reopening_and_superseding_evidence(self):
        self.publish(self.evaluated())
        doc = deepcopy(self.doc)
        doc.records["task"].fields["st"] = codec.Symbol("done")
        self.publish(doc)
        doc = deepcopy(self.doc)
        doc.records["contract"].fields["li"] = "Changed lighting direction"
        with self.assertRaisesRegex(codec.PixlError, "reopen_required"):
            self.publish(doc)
        doc.records["task"].fields["st"] = codec.Symbol("open")
        with self.assertRaisesRegex(codec.PixlError, "stale_evidence"):
            self.publish(doc)
        for record in doc.records.values():
            if record.kind in ("E", "V"):
                record.fields["ob"] = True
        self.publish(doc)
        graph.validate(self.doc, self.root)
        self.assertIn("task", graph.ready(self.doc))


if __name__ == "__main__":
    unittest.main()
