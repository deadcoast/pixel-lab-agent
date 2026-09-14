"""PX2 lifecycle behavior against real records, paths, hashes and reports."""

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import graph
from pixl.codec import PixlError, Record, Ref, Symbol, record_hash
from tests.lifecycle_support import add_candidate, add_verdict, sample


class LifecycleValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.doc = sample(self.root)

    def assert_valid(self, doc=None):
        try:
            graph.validate(self.doc if doc is None else doc, self.root)
        except (PixlError, ImportError) as error:
            self.fail(f"Valid PX2 lifecycle rejected: {error}")

    def rejected(self, code):
        return self.assertRaisesRegex(PixlError, code)

    def report(self):
        from pixl.lifecycle import report
        self.assert_valid()
        return report(self.doc)

    def add_method(self):
        self.doc.records["method"] = Record("method", "K", {
            "nm": "Unproven fixture method", "ap": [Symbol("fixture")],
            "op": ["Investigate the declared criterion"], "ck": ["Retain results"],
            "so": [Ref("source")],
        })
        self.doc.records["task"].fields["kn"] = [Ref("method")]

    def add_adoption(self, passing=True):
        self.doc.records["decision"] = Record("decision", "D", {
            "wh": Ref("actor"), "wt": "Adopt fixture method", "wr": [Ref("method")],
            "wy": "Developer test decision", "rs": [Ref("source")],
            "pc": [Ref("adoption.e")],
        })
        self.doc.records["method"].fields["pc"] = [Ref("adoption.e")]
        self.doc.records["task"].fields["dc"] = [Ref("decision")]
        self.doc.records["adoption.e"] = Record("adoption.e", "E", {
            "nm": "Synthetic adoption test", "ur": "source.txt",
            "dg": self.doc.records["source"].fields["dg"],
            "rs": Symbol("pass" if passing else "fail"), "md": Symbol("local"),
            "at": "2026-09-11", "bs": [
                {"rf": Ref(id_), "dg": record_hash(self.doc.records[id_])}
                for id_ in sorted(graph.proof_scope(self.doc, ["decision"]))
            ],
        })

    def confirm(self):
        self.doc.records["choice"].fields.update(
            st=Symbol("confirmed"), so=[Ref("source")]
        )

    def pass_all(self, candidate="candidate"):
        add_candidate(self.doc, self.root, candidate)
        for criterion in ("q.mechanical", "q.visual", "q.engine"):
            add_verdict(self.doc, self.root, candidate, criterion, "pass", f"v.{criterion}")

    def test_open_plan_needs_no_artifact_or_adopted_decision(self):
        self.assert_valid()
        self.assertEqual(graph.ready(self.doc), ["task"])
        self.assertFalse(any(r.kind == "X" for r in self.doc.records.values()))

    def test_choice_states_keep_unknown_and_conflict_values_explicit(self):
        self.doc.records["contract"].fields["ch"] = []
        for status, value in [("unresolved", None), ("conflict", [[2, 2], [4, 4]])]:
            with self.subTest(status=status):
                self.doc.records["choice"].fields.update(st=Symbol(status), vl=value)
                self.assert_valid()
        for status, value in [("unresolved", [2, 2]), ("conflict", []), ("conflict", [2]), ("proposed", None)]:
            with self.subTest(status=status, value=value):
                self.doc.records["choice"].fields.update(st=Symbol(status), vl=value)
                with self.rejected("intake_value"):
                    graph.validate(self.doc)

    def test_observed_and_confirmed_choices_need_sources(self):
        for status in ("observed", "confirmed"):
            with self.subTest(status=status):
                self.doc.records["choice"].fields.update(st=Symbol(status), so=[])
                with self.rejected("intake_source"):
                    graph.validate(self.doc)
                self.doc.records["choice"].fields["so"] = [Ref("source")]
                self.assert_valid()

    def test_proposal_requires_rationale_and_choice_key_is_not_blank(self):
        self.doc.records["choice"].fields["wy"] = "   "
        with self.rejected("intake_rationale"):
            graph.validate(self.doc)
        self.doc.records["choice"].fields.update(wy="fixture reason", ky=" ")
        with self.rejected("intake_key"):
            graph.validate(self.doc)

    def test_project_and_intake_links_are_reciprocal(self):
        self.doc.records["project"].fields["in"] = []
        with self.rejected("intake_project"):
            graph.validate(self.doc)

    def test_one_project_cannot_define_a_choice_key_twice(self):
        duplicate = deepcopy(self.doc.records["choice"])
        duplicate.id = "choice.duplicate"
        self.doc.records[duplicate.id] = duplicate
        self.doc.records["project"].fields["in"].append(Ref(duplicate.id))
        with self.rejected("intake_key"):
            graph.validate(self.doc)

    def test_unresolved_choices_retain_old_contract_and_block_active_work(self):
        for status, value in [("unresolved", None), ("conflict", [[2, 2], [4, 4]])]:
            with self.subTest(status=status):
                self.doc.records["choice"].fields.update(st=Symbol(status), vl=value)
                self.doc.records["task"].fields.update(st=Symbol("open"), ph=Symbol("sample"))
                self.assert_valid()
                self.assertEqual(self.doc.records["contract"].fields["px"], [2, 2])
                result = self.report()
                self.assertEqual(result["ready"], [])
                self.assertIn(f"choice_{status}", " ".join(result["tasks"][0]["blockers"]))
                self.doc.records["task"].fields["st"] = Symbol("blocked")
                self.assert_valid()
                for phase in ("research", "sample", "production", "delivery"):
                    for state in ("active", "done"):
                        with self.subTest(phase=phase, state=state):
                            self.doc.records["task"].fields.update(st=Symbol(state), ph=Symbol(phase))
                            with self.rejected(f"choice_{status}"):
                                graph.validate(self.doc)

    def test_unknown_choice_can_retain_materialized_candidate_after_supersession(self):
        self.pass_all()
        for record in self.doc.records.values():
            if record.kind in {"V", "E"}:
                record.fields["ob"] = True
        self.doc.records["choice"].fields.update(st=Symbol("unresolved"), vl=None)
        self.doc.records["task"].fields["st"] = Symbol("blocked")
        self.assert_valid()
        self.assertEqual(self.report()["tasks"][0]["outputs"][0]["candidate"], "candidate")
        self.assertTrue((self.root / "candidate.png").is_file())

    def test_contract_field_choice_must_equal_instantiated_value(self):
        self.doc.records["choice"].fields["vl"] = [4, 4]
        with self.rejected("contract_choice"):
            graph.validate(self.doc)
        self.doc.records["choice"].fields.update(ky="silhouette", vl="fixture block")
        self.assert_valid()

    def other_project(self):
        self.doc.records["other.project"] = Record("other.project", "P", {
            "nm": "Independent source project", "ow": Ref("actor"), "sc": [],
            "in": [Ref("other.choice")],
        })
        self.doc.records["other.choice"] = deepcopy(self.doc.records["choice"])
        self.doc.records["other.choice"].id = "other.choice"
        self.doc.records["other.choice"].fields["pr"] = Ref("other.project")
        self.doc.records["other.contract"] = deepcopy(self.doc.records["contract"])
        self.doc.records["other.contract"].id = "other.contract"
        self.doc.records["other.contract"].fields["ch"] = [Ref("other.choice")]

    def test_output_choices_belong_to_task_project_but_source_inputs_may_differ(self):
        self.other_project()
        self.doc.records["output"].fields["ct"] = Ref("other.contract")
        with self.rejected("task_project"):
            graph.validate(self.doc)
        self.doc.records["output"].fields["ct"] = Ref("contract")
        add_candidate(self.doc, self.root, "input")
        self.doc.records["input"].fields.pop("of")
        self.doc.records["input"].fields["ct"] = Ref("other.contract")
        self.doc.records["task"].fields.update(ip=[Ref("input")], ca=[], st=Symbol("active"))
        self.assert_valid()

    def test_research_and_sample_can_activate_with_unproven_methods(self):
        self.add_method()
        for phase in ("research", "sample"):
            self.doc.records["task"].fields.update(st=Symbol("active"), ph=Symbol(phase))
            self.assert_valid()

    def test_production_readiness_requires_adoption_proofs_and_confirmation(self):
        self.add_method()
        self.doc.records["task"].fields["ph"] = Symbol("production")
        self.assertEqual(self.report()["ready"], [])
        messages = " ".join(self.report()["tasks"][0]["blockers"])
        for blocker in ("task_decision", "method_poc", "choice_unconfirmed"):
            self.assertIn(blocker, messages)
        self.add_adoption()
        self.confirm()
        self.assertEqual(self.report()["ready"], ["task"])
        self.doc.records["task"].fields["st"] = Symbol("active")
        self.assert_valid()

    def test_active_production_and_delivery_reject_missing_adoption(self):
        self.confirm()
        for phase in ("production", "delivery"):
            with self.subTest(phase=phase):
                self.doc.records["task"].fields.update(st=Symbol("active"), ph=Symbol(phase))
                with self.rejected("task_decision"):
                    graph.validate(self.doc)

    def test_failed_method_proof_cannot_activate_production(self):
        self.add_method()
        self.add_adoption(passing=False)
        self.confirm()
        self.doc.records["task"].fields.update(ph=Symbol("production"), st=Symbol("active"))
        with self.rejected("method_poc"):
            graph.validate(self.doc)

    def test_unconfirmed_linked_choice_cannot_activate_production(self):
        self.add_method()
        self.add_adoption()
        self.doc.records["task"].fields.update(ph=Symbol("production"), st=Symbol("active"))
        with self.rejected("choice_unconfirmed"):
            graph.validate(self.doc)

    def test_all_active_phases_require_completed_prerequisites(self):
        dependency = deepcopy(self.doc.records["task"])
        dependency.id = "prerequisite"
        dependency.fields.update(op=[], ca=[], vr=[])
        self.doc.records[dependency.id] = dependency
        self.doc.records["task"].fields["dp"] = [Ref(dependency.id)]
        self.assertEqual(self.report()["ready"], ["prerequisite"])
        for phase in ("research", "sample", "production", "delivery"):
            with self.subTest(phase=phase):
                self.doc.records["task"].fields.update(ph=Symbol(phase), st=Symbol("active"))
                with self.rejected("task_prerequisite"):
                    graph.validate(self.doc)

    def test_raster_output_needs_contract_before_activation_but_reports_do_not(self):
        self.doc.records["output"].fields.pop("ct")
        self.assertEqual(self.report()["ready"], [])
        self.doc.records["task"].fields["st"] = Symbol("active")
        with self.rejected("output_contract"):
            graph.validate(self.doc)
        for kind in ("report", "code", "reference"):
            self.doc.records["output"].fields["kd"] = Symbol(kind)
            self.assert_valid()

    def test_output_ownership_and_declared_requirements_are_mandatory(self):
        self.doc.records["task"].fields["op"] = []
        with self.rejected("output_owner"):
            graph.validate(self.doc)
        self.doc.records["task"].fields["op"] = [Ref("output")]
        self.doc.records["output"].fields["rq"] = []
        with self.rejected("output_requirements"):
            graph.validate(self.doc)

    def test_visual_and_engine_criteria_enforce_corresponding_modes(self):
        for id_ in ("q.visual", "q.engine"):
            old = self.doc.records[id_].fields["md"]
            self.doc.records[id_].fields["md"] = Symbol("local")
            with self.subTest(criterion=id_), self.rejected("criterion_mode"):
                graph.validate(self.doc)
            self.doc.records[id_].fields["md"] = old
        self.doc.records["q.mechanical"].fields["ck"] = "   "
        with self.rejected("criterion_check"):
            graph.validate(self.doc)

    def test_materialized_raster_requires_contract_and_must_match_its_output(self):
        add_candidate(self.doc, self.root, "candidate")
        self.doc.records["candidate"].fields.pop("ct")
        with self.rejected("artifact_contract"):
            graph.validate(self.doc)
        self.doc.records["candidate"].fields["ct"] = Ref("contract")
        self.doc.records["candidate"].fields["kd"] = Symbol("tileset")
        with self.rejected("candidate_output"):
            graph.validate(self.doc)
        self.doc.records["candidate"].fields["kd"] = Symbol("sprite")
        self.other_project()
        self.doc.records["candidate"].fields["ct"] = Ref("other.contract")
        with self.rejected("candidate_output"):
            graph.validate(self.doc)

    def test_standalone_nonraster_input_can_omit_contract(self):
        add_candidate(self.doc, self.root, "input")
        fields = self.doc.records["input"].fields
        fields.pop("ct")
        fields.pop("of")
        fields["kd"] = Symbol("reference")
        self.doc.records["task"].fields.update(ca=[], ip=[Ref("input")])
        self.assert_valid()

    def test_only_one_candidate_can_be_nominated_for_a_planned_output(self):
        add_candidate(self.doc, self.root, "old")
        add_candidate(self.doc, self.root, "new")
        self.assert_valid()
        self.doc.records["task"].fields["ca"].append(Ref("old"))
        with self.rejected("candidate_nomination"):
            graph.validate(self.doc)

    def test_nomination_cannot_reference_an_unplanned_input(self):
        add_candidate(self.doc, self.root, "candidate")
        self.doc.records["candidate"].fields.pop("of")
        with self.rejected("candidate_output"):
            graph.validate(self.doc)

    def test_verdict_must_belong_to_task_and_required_candidate_criterion(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.mechanical", "unavailable", "verdict")
        self.doc.records["task"].fields["vr"] = []
        with self.rejected("verdict_owner"):
            graph.validate(self.doc)
        self.doc.records["task"].fields["vr"] = [Ref("verdict")]
        self.doc.records["output"].fields["rq"] = [Ref("q.visual")]
        with self.rejected("verdict_requirement"):
            graph.validate(self.doc)

    def test_unperformed_is_reported_and_does_not_complete_a_sample(self):
        add_candidate(self.doc, self.root, "candidate")
        requirements = self.report()["tasks"][0]["outputs"][0]["requirements"]
        self.assertEqual([r["status"] for r in requirements], ["unperformed"] * 3)
        self.doc.records["task"].fields["st"] = Symbol("done")
        with self.rejected("completion"):
            graph.validate(self.doc)

    def test_mechanical_pass_visual_failure_and_unavailable_engine_remain_resumable(self):
        add_candidate(self.doc, self.root, "rejected")
        for criterion, status in [("q.mechanical", "pass"), ("q.visual", "fail"), ("q.engine", "unavailable")]:
            add_verdict(self.doc, self.root, "rejected", criterion, status, f"v.{criterion}")
        self.doc.records["task"].fields["st"] = Symbol("active")
        result = self.report()
        requirements = result["tasks"][0]["outputs"][0]["requirements"]
        self.assertEqual([r["status"] for r in requirements], ["pass", "fail", "unavailable"])
        self.assertEqual(result["ready"], [])
        self.doc.records["task"].fields["st"] = Symbol("done")
        with self.rejected("completion"):
            graph.validate(self.doc)

    def test_workflow_includes_check_and_verdict_reason_and_reviewer(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.engine", "unavailable", "engine.v")
        self.doc.records["engine.v"].fields.update(
            wy="The target engine is unavailable in this fixture environment.", wh=Ref("user")
        )
        requirements = self.report()["tasks"][0]["outputs"][0]["requirements"]
        self.assertEqual(requirements[2].get("check"), "Caller retains target-engine execution evidence.")
        self.assertEqual(requirements[2].get("reason"), "The target engine is unavailable in this fixture environment.")
        self.assertEqual(requirements[2].get("reviewer"), "user")
        self.assertIsNone(requirements[0].get("reason"))
        self.assertIsNone(requirements[0].get("reviewer"))

    def test_done_requires_a_plan_and_nominee_for_every_output(self):
        self.doc.records["task"].fields["st"] = Symbol("done")
        with self.rejected("completion"):
            graph.validate(self.doc)
        self.doc.records.pop("output")
        self.doc.records["task"].fields["op"] = []
        with self.rejected("completion"):
            graph.validate(self.doc)

    def test_all_current_required_passes_complete_candidate(self):
        self.pass_all()
        self.doc.records["task"].fields["st"] = Symbol("done")
        self.assert_valid()
        result = self.report()
        self.assertEqual(result["ready"], [])
        self.assertEqual(result["tasks"][0]["outputs"][0]["candidate"], "candidate")
        self.assertEqual([r["status"] for r in result["tasks"][0]["outputs"][0]["requirements"]], ["pass"] * 3)

    def test_completion_covers_every_output_even_when_first_candidate_passes(self):
        self.pass_all()
        second = deepcopy(self.doc.records["output"])
        second.id = "second.output"
        second.fields["rq"] = [Ref("q.mechanical")]
        self.doc.records[second.id] = second
        self.doc.records["task"].fields["op"].append(Ref(second.id))
        self.doc.records["task"].fields["st"] = Symbol("done")
        with self.rejected("completion"):
            graph.validate(self.doc)
        add_candidate(self.doc, self.root, "second.candidate")
        self.doc.records["second.candidate"].fields["of"] = Ref(second.id)
        self.doc.records["task"].fields["ca"] = [Ref("candidate"), Ref("second.candidate")]
        with self.rejected("completion"):
            graph.validate(self.doc)
        add_verdict(self.doc, self.root, "second.candidate", "q.mechanical", "pass", "second.v")
        self.assert_valid()

    def test_verdict_requires_candidate_and_all_semantic_scope_bindings(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.mechanical", "pass", "verdict")
        original = deepcopy(self.doc.records["verdict.e"].fields["bs"])
        for omitted in ("candidate", "output", "q.mechanical", "contract", "choice", "source"):
            with self.subTest(omitted=omitted):
                self.doc.records["verdict.e"].fields["bs"] = [
                    binding for binding in original if binding["rf"].id != omitted
                ]
                with self.rejected("verdict_proof|evidence_context"):
                    graph.validate(self.doc)
        self.doc.records["verdict.e"].fields["bs"] = original
        self.assert_valid()

    def test_current_verdict_cannot_borrow_another_candidate_receipt(self):
        add_candidate(self.doc, self.root, "old")
        add_verdict(self.doc, self.root, "old", "q.mechanical", "pass", "old.v")
        add_candidate(self.doc, self.root, "new")
        add_verdict(self.doc, self.root, "new", "q.mechanical", "pass", "new.v")
        self.doc.records["new.v"].fields["ev"] = [Ref("old.v.e")]
        with self.rejected("verdict_proof"):
            graph.validate(self.doc)

    def test_current_verdict_requires_matching_receipt_mode_and_outcome(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.visual", "pass", "verdict")
        receipt = self.doc.records["verdict.e"].fields
        receipt["md"] = Symbol("local")
        with self.rejected("verdict_evidence"):
            graph.validate(self.doc)
        receipt.update(md=Symbol("visual"), rs=Symbol("fail"))
        with self.rejected("verdict_evidence"):
            graph.validate(self.doc)

    def test_superseded_receipts_cannot_support_current_verdict(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.mechanical", "pass", "verdict")
        self.doc.records["verdict.e"].fields["ob"] = True
        with self.rejected("verdict_evidence|verdict_proof"):
            graph.validate(self.doc)

    def test_unavailable_verdict_needs_reason_and_contains_no_receipts(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.engine", "unavailable", "verdict")
        self.assert_valid()
        self.doc.records["verdict"].fields["wy"] = "   "
        with self.rejected("verdict_reason"):
            graph.validate(self.doc)
        self.doc.records["verdict"].fields["wy"] = "Target engine unavailable."
        add_verdict(self.doc, self.root, "candidate", "q.mechanical", "pass", "mechanical")
        self.doc.records["verdict"].fields["ev"] = [Ref("mechanical.e")]
        with self.rejected("verdict_unavailable"):
            graph.validate(self.doc)

    def test_verdict_date_is_an_actual_iso_date(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.engine", "unavailable", "verdict")
        self.doc.records["verdict"].fields["at"] = "later"
        with self.rejected("date"):
            graph.validate(self.doc)

    def test_supersession_retains_history_without_current_duplicate_verdicts(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.visual", "fail", "old.v")
        add_verdict(self.doc, self.root, "candidate", "q.visual", "pass", "new.v")
        with self.rejected("verdict_duplicate"):
            graph.validate(self.doc)
        self.doc.records["old.v"].fields["ob"] = True
        self.assert_valid()
        self.assertEqual(self.report()["tasks"][0]["outputs"][0]["requirements"][1]["verdict"], "new.v")
        self.assertFalse(self.doc.records["old.v.e"].fields.get("ob", False))
        self.doc.records["task"].fields["vr"].remove(Ref("old.v"))
        with self.rejected("verdict_owner"):
            graph.validate(self.doc)

    def test_superseded_verdict_survives_removal_of_its_old_requirement(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.engine", "fail", "old.v")
        self.doc.records["old.v"].fields["ob"] = True
        self.doc.records["old.v.e"].fields["ob"] = True
        self.doc.records["output"].fields["rq"].remove(Ref("q.engine"))
        self.assert_valid()
        self.assertIn(Ref("old.v"), self.doc.records["task"].fields["vr"])
        self.assertEqual(
            [r["id"] for r in self.report()["tasks"][0]["outputs"][0]["requirements"]],
            ["q.mechanical", "q.visual"],
        )

    def test_old_rejected_candidate_is_reported_after_new_nomination(self):
        add_candidate(self.doc, self.root, "rejected")
        add_verdict(self.doc, self.root, "rejected", "q.visual", "fail", "rejection")
        add_candidate(self.doc, self.root, "replacement")
        output = self.report()["tasks"][0]["outputs"][0]
        self.assertEqual(output["candidate"], "replacement")
        self.assertEqual([r["status"] for r in output["requirements"]], ["unperformed"] * 3)
        rejected = next(c for c in output["candidates"] if c["id"] == "rejected")
        self.assertFalse(rejected["nominated"])
        self.assertEqual(rejected["requirements"][1]["status"], "fail")

    def test_proof_scope_includes_plan_criteria_choices_but_excludes_workflow(self):
        add_candidate(self.doc, self.root, "candidate")
        add_verdict(self.doc, self.root, "candidate", "q.mechanical", "pass", "verdict")
        self.assertEqual(graph.proof_scope(self.doc, ["candidate"]), {
            "candidate", "output", "contract", "choice", "actor", "source",
            "q.mechanical", "q.visual", "q.engine",
        })
        self.assert_valid()

    def test_workflow_report_does_not_mutate_or_recursively_validate(self):
        from unittest.mock import patch

        from pixl.lifecycle import blockers, report

        before = deepcopy(self.doc)
        self.assert_valid()
        with patch.object(graph, "validate", side_effect=AssertionError("recursive validation")):
            self.assertEqual(blockers(self.doc, "task"), [])
            result = report(self.doc)
        self.assertEqual(result["intake"][0]["status"], "proposed")
        self.assertEqual(result["intake"][0]["value"], [2, 2])
        self.assertEqual(self.doc, before)


if __name__ == "__main__":
    unittest.main()
