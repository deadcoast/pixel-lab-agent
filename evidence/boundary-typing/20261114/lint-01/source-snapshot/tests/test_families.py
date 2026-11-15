"""Family semantic checks against saved plans and retained synthetic receipts."""

import importlib
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import codec, graph, store
from pixl.codec import PixlError, Record, Ref, Symbol
from tests.family_support import family
from tests.lifecycle_support import add_candidate, add_verdict, sample


class FamilySchemaTests(unittest.TestCase):
    def test_published_baseline_and_family_plan_are_understood(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            try:
                doc = family(root)
                graph.validate(doc, root)
            except PixlError as error:
                self.fail(f"A saved family plan must be understood: {error}")
            self.assertEqual(store.load(root / ".pixl"), doc)
            self.assertEqual(doc.records["task"].fields["st"], Symbol("done"))
            self.assertEqual(doc.records["member.task"].fields["st"], Symbol("done"))
            self.assertEqual(doc.records["delivery.task"].fields["st"], Symbol("open"))

    def test_family_api_exists_for_readiness_without_io(self):
        self.assertIsNotNone(importlib.util.find_spec("pixl.families"), "Family planning API is missing")


class FamilyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.doc = family(self.root)
        self.families = importlib.import_module("pixl.families")

    def test_plan_freezes_ordered_members_destinations_and_semantic_bindings(self):
        plan = self.families.plan(self.doc, "delivery.output")
        self.assertEqual(set(plan), {"output", "task", "baseline", "members", "destinations", "bindings"})
        self.assertEqual(plan["output"], "delivery.output")
        self.assertEqual(plan["task"], "delivery.task")
        self.assertEqual(plan["baseline"], "sample")
        self.assertEqual(plan["members"], ["output", "member.output"])
        self.assertEqual(plan["destinations"], ["destination"])
        self.assertEqual(list(plan["bindings"]), sorted(plan["bindings"]))
        self.assertTrue({"delivery.output", "member.output", "output", "sample", "contract", "choice", "destination", "q.continuity", "q.delivery.engine"} <= plan["bindings"].keys())
        self.assertNotIn("member", plan["bindings"])
        self.assertEqual(self.families.selection(self.doc, "delivery.output"), ["sample", "member"])

    def test_baseline_must_be_current_nominee_of_completed_sample(self):
        for change in ("unfinished", "unselected", "replaced"):
            with self.subTest(change=change):
                doc = deepcopy(self.doc)
                doc.records["member.task"].fields["st"] = Symbol("open")
                doc.records["task"].fields["st"] = Symbol("open")
                if change == "unselected":
                    doc.records["task"].fields["ca"] = []
                elif change == "replaced":
                    add_candidate(doc, self.root, "replacement")
                graph.validate(doc, self.root)
                reasons = self.families.blockers(doc, "member.task")
                self.assertIn("family_baseline", " ".join(reasons))
                self.assertFalse(self.families.describe(doc, "delivery.output")["baseline"]["eligible"])
                self.assertNotIn("member.task", graph.ready(doc))

    def test_current_baseline_and_member_receipts_enable_snapshot(self):
        before = codec.encode(self.doc)
        self.assertEqual(self.families.snapshot_blockers(self.doc, "delivery.output"), [])
        report = self.families.describe(self.doc, "delivery.output")
        self.assertTrue(report["baseline"]["eligible"])
        self.assertEqual([m["accepted"] for m in report["members"]], [True, True])
        self.assertEqual([q["status"] for q in report["requirements"]], ["unperformed", "unperformed"])
        self.assertEqual(codec.encode(self.doc), before)

    def test_destination_confirmation_gates_activation_but_not_local_snapshot(self):
        for status, value in [("unresolved", None), ("conflict", ["one", "two"]), ("proposed", "target"), ("observed", "target")]:
            with self.subTest(status=status):
                doc = deepcopy(self.doc)
                doc.records["destination"].fields.update(st=Symbol(status), vl=value)
                graph.validate(doc, self.root)
                self.assertIn("family_destination", " ".join(self.families.blockers(doc, "delivery.task")))
                self.assertNotIn("delivery.task", graph.ready(doc))
                self.assertEqual(self.families.snapshot_blockers(doc, "delivery.output"), [])
                doc.records["delivery.task"].fields["st"] = Symbol("active")
                with self.assertRaisesRegex(PixlError, "family_destination"):
                    graph.validate(doc, self.root)

    def test_snapshot_does_not_require_adoption_or_delivery_verdicts(self):
        self.doc.records["delivery.task"].fields["dc"] = []
        graph.validate(self.doc, self.root)
        self.assertEqual(self.families.snapshot_blockers(self.doc, "delivery.output"), [])
        self.assertIn("task_decision", " ".join(self.families.describe(self.doc, "delivery.output")["blockers"]))

    def test_snapshot_requires_open_or_active_delivery_and_completed_members(self):
        for state in ("blocked", "dropped"):
            with self.subTest(state=state):
                doc = deepcopy(self.doc)
                doc.records["delivery.task"].fields["st"] = Symbol(state)
                graph.validate(doc, self.root)
                self.assertIn("family_state", " ".join(self.families.snapshot_blockers(doc, "delivery.output")))
        self.doc.records["member.task"].fields.update(st=Symbol("open"), ca=[])
        graph.validate(self.doc, self.root)
        self.assertEqual(self.families.selection(self.doc, "delivery.output"), ["sample", None])
        self.assertIn("family_member", " ".join(self.families.snapshot_blockers(self.doc, "delivery.output")))

    def test_pending_jobs_include_baseline_member_and_delivery_tasks(self):
        for task in ("task", "member.task", "delivery.task"):
            for state in ("prepared", "unknown", "submitted", "running"):
                with self.subTest(task=task, state=state):
                    doc = deepcopy(self.doc)
                    doc.records["pending"] = Record("pending", "J", {
                        "tk": Ref(task), "tl": "Synthetic existing attempt", "ah": "0" * 64,
                        "si": Symbol(state), "ri": "fixture-remote-id" if state in {"submitted", "running"} else "", "ev": [],
                    })
                    graph.validate(doc, self.root)
                    report = self.families.describe(doc, "delivery.output")
                    self.assertEqual(report["pending_jobs"], [{"id": "pending", "task": task, "state": state}])
                    self.assertIn("family_job", " ".join(report["snapshot_blockers"]))

    def test_family_structural_contract_rejects_invalid_relationships(self):
        mutations = [
            ("family_fields", lambda d: d.records["delivery.output"].fields.pop("ds")),
            ("family_fields", lambda d: d.records["delivery.output"].fields.pop("bs")),
            ("family_kind", lambda d: d.records["delivery.output"].fields.update(kd=Symbol("code"))),
            ("family_phase", lambda d: d.records["delivery.task"].fields.update(ph=Symbol("research"))),
            ("family_members", lambda d: d.records["delivery.output"].fields.update(mb=[])),
            ("family_members", lambda d: d.records["delivery.output"].fields.update(mb=[Ref("output"), Ref("output")])),
            ("family_members", lambda d: d.records["delivery.output"].fields.update(mb=[Ref("delivery.output")])),
            ("family_destinations", lambda d: d.records["delivery.output"].fields.update(ds=[])),
            ("family_destinations", lambda d: d.records["delivery.output"].fields.update(ds=[Ref("destination"), Ref("destination")])),
            ("family_continuity", lambda d: d.records["delivery.output"].fields.update(rq=[Ref("q.delivery.engine")])),
            ("family_prerequisite", lambda d: d.records["delivery.task"].fields.update(dp=[Ref("task")])),
            ("family_baseline_input", lambda d: d.records["delivery.task"].fields.update(ip=[])),
        ]
        for code, mutate in mutations:
            with self.subTest(code=code, mutate=mutate):
                doc = deepcopy(self.doc)
                mutate(doc)
                with self.assertRaisesRegex(PixlError, code):
                    graph.validate(doc)

    def test_cross_project_baseline_member_and_destination_are_rejected(self):
        for target, field, code in [("task", "pr", "family_project"), ("member.task", "pr", "family_project"), ("destination", "pr", "family_project")]:
            with self.subTest(target=target):
                doc = deepcopy(self.doc)
                doc.records["other.project"] = Record("other.project", "P", {"nm": "Other", "ow": Ref("actor"), "sc": [], "in": []})
                doc.records[target].fields[field] = Ref("other.project")
                with self.assertRaisesRegex(PixlError, code):
                    graph.validate(doc)

    def test_baseline_needs_sample_owner_and_explicit_dependency(self):
        for field, value, code in [("ph", Symbol("research"), "family_baseline_owner"), ("dp", [], "family_prerequisite")]:
            doc = deepcopy(self.doc)
            task = "task" if field == "ph" else "delivery.task"
            doc.records[task].fields[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(PixlError, code):
                graph.validate(doc)

    def test_nested_member_is_rejected_before_lifecycle(self):
        self.doc.records["nested.task"] = deepcopy(self.doc.records["delivery.task"])
        self.doc.records["nested.task"].id = "nested.task"
        self.doc.records["nested.task"].fields["op"] = [Ref("nested.output")]
        self.doc.records["nested.output"] = deepcopy(self.doc.records["delivery.output"])
        self.doc.records["nested.output"].id = "nested.output"
        self.doc.records["nested.output"].fields["tk"] = Ref("nested.task")
        self.doc.records["delivery.output"].fields["mb"] = [Ref("nested.output")]
        self.doc.records["delivery.task"].fields["dp"].append(Ref("nested.task"))
        with self.assertRaisesRegex(PixlError, "family_members"):
            graph.validate(self.doc)

    def test_manifest_constituents_only_belong_to_family_report_candidates(self):
        self.doc.records["sample"].fields["xs"] = [Ref("member")]
        # Isolate schema/structure from intentionally unchanged old proof hashes.
        with self.assertRaisesRegex(PixlError, "family_candidate"):
            self.families.validate(self.doc)

    def test_family_candidate_cannot_bypass_snapshot_checks_by_omitting_constituents(self):
        self.doc.records["unretained"] = Record("unretained", "X", {
            "nm": "Unretained report", "ur": "source.txt",
            "dg": self.doc.records["source"].fields["dg"],
            "kd": Symbol("report"), "of": Ref("delivery.output"),
        })
        with self.assertRaisesRegex(PixlError, "family_candidate"):
            graph.validate(self.doc, self.root)

    def test_family_manifest_plan_cannot_adopt_a_raster_contract(self):
        self.doc.records["delivery.output"].fields["ct"] = Ref("contract")
        with self.assertRaisesRegex(PixlError, "family_contract"):
            graph.validate(self.doc, self.root)

    def test_member_and_family_output_ownership_remains_reciprocal(self):
        for output, task in [("member.output", "member.task"), ("delivery.output", "delivery.task")]:
            with self.subTest(output=output):
                doc = deepcopy(self.doc)
                doc.records[task].fields["op"] = []
                with self.assertRaisesRegex(PixlError, "output_owner"):
                    graph.validate(doc)

    def test_production_member_requires_the_declared_family_baseline(self):
        doc = deepcopy(self.doc)
        doc.records["member.output"].fields.pop("bs")
        with self.assertRaisesRegex(PixlError, "family_member_baseline"):
            self.families.validate(doc)

    def test_collective_verdict_rejects_receipts_missing_exact_constituents(self):
        from pixl import delivery

        delivery.snapshot(self.root / ".pixl", codec.digest(self.doc), "delivery.output", "manifest", self.root)
        self.doc = store.load(self.root / ".pixl")
        add_verdict(self.doc, self.root, "manifest", "q.continuity", "pass", "family.v.continuity")
        graph.validate(self.doc, self.root)
        for missing in ("sample", "member", "destination", "q.continuity"):
            with self.subTest(missing=missing):
                doc = deepcopy(self.doc)
                receipt = doc.records["family.v.continuity.e"].fields
                receipt["bs"] = [binding for binding in receipt["bs"] if binding["rf"].id != missing]
                with self.assertRaisesRegex(PixlError, "evidence_context|verdict_proof"):
                    graph.validate(doc, self.root)

    def test_describe_retains_unavailable_engine_and_failed_continuity(self):
        from pixl import delivery

        delivery.snapshot(self.root / ".pixl", codec.digest(self.doc), "delivery.output", "manifest", self.root)
        self.doc = store.load(self.root / ".pixl")
        add_verdict(self.doc, self.root, "manifest", "q.continuity", "fail", "family.v.continuity")
        add_verdict(self.doc, self.root, "manifest", "q.delivery.engine", "unavailable", "family.v.engine")
        self.doc.records["delivery.task"].fields["ca"] = [Ref("manifest")]
        graph.validate(self.doc, self.root)
        report = self.families.describe(self.doc, "delivery.output")
        self.assertEqual([q["status"] for q in report["requirements"]], ["fail", "unavailable"])
        self.assertEqual(report["requirements"][1]["evidence"], [])
        self.assertFalse(report["members"][0]["reasons"])
        self.doc.records["delivery.task"].fields["st"] = Symbol("done")
        with self.assertRaisesRegex(PixlError, "completion"):
            graph.validate(self.doc, self.root)

    def test_collective_proof_contains_baseline_and_actual_constituents(self):
        self.doc.records["manifest"] = Record("manifest", "X", {
            "nm": "Unpublished scope fixture", "ur": "manifest.json", "dg": "0" * 64,
            "kd": Symbol("report"), "of": Ref("delivery.output"),
            "xs": [Ref("sample"), Ref("sample"), Ref("member")],
        })
        scope = graph.proof_scope(self.doc, ["manifest"])
        self.assertTrue({"sample", "member", "output", "member.output", "delivery.output", "destination", "q.continuity", "q.delivery.engine"} <= scope)
        self.assertTrue({"task", "member.task", "delivery.task", "project"}.isdisjoint(scope))
        member_scope = graph.proof_scope(self.doc, ["member"])
        self.assertIn("sample", member_scope)

    def test_legacy_sample_has_unchanged_readiness(self):
        doc = sample(self.root / "legacy")
        graph.validate(doc, self.root / "legacy")
        self.assertEqual(graph.ready(doc), ["task"])
        self.assertEqual(self.families.blockers(doc, "task"), [])

    def test_px1_ignores_family_activation_and_rejects_new_fields(self):
        from tests.support import sample as legacy_sample

        doc = legacy_sample(self.root / "px1")
        graph.validate(doc, self.root / "px1")
        self.assertEqual(graph.ready(doc), ["task"])
        self.assertEqual(self.families.blockers(doc, "task"), [])
        doc.records["asset"].fields["xs"] = [Ref("asset")]
        with self.assertRaisesRegex(PixlError, "unknown_field"):
            graph.validate(doc)


if __name__ == "__main__":
    unittest.main()
