from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from pixl.codec import PixlError, Ref, Record, Symbol, record_hash
from pixl import graph
from tests.support import sample


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.doc = sample(self.root)

    def test_valid_project_closure_and_ready(self):
        graph.validate(self.doc, self.root)
        self.assertEqual(graph.ready(self.doc), ["task"])
        packet = graph.context(self.doc, "task")
        graph.validate(packet, self.root)
        self.assertEqual(set(packet.records), set(self.doc.records))

    def test_rejects_bad_types_unresolved_refs_and_missing_decision_proof(self):
        for key, value in [("wh", Ref("source")), ("pc", []), ("wr", [Ref("missing")]), ("wt", Symbol("wrong_type"))]:
            doc = deepcopy(self.doc)
            doc.records["decision"].fields[key] = value
            with self.subTest(key=key), self.assertRaises(PixlError):
                graph.validate(doc)

    def test_detects_cycle_in_tasks_without_forbidding_evidence_cycles(self):
        self.doc.records["task"].fields["dp"] = [Ref("task")]
        with self.assertRaisesRegex(PixlError, "cycle"):
            graph.validate(self.doc)

    def test_full_record_binding_detects_art_contract_drift(self):
        self.doc.records["asset"].fields["nm"] = "changed"
        with self.assertRaisesRegex(PixlError, "stale_evidence"):
            graph.validate(self.doc)

    def test_external_file_mutation_detected(self):
        (self.root / "asset.txt").write_text("drift", encoding="utf-8")
        with self.assertRaisesRegex(PixlError, "file_hash"):
            graph.validate(self.doc, self.root)

    def test_contract_change_invalidates_existing_asset_proof(self):
        self.doc.records["style"].fields["px"] = [32, 32]
        with self.assertRaisesRegex(PixlError, "stale_evidence"):
            graph.validate(self.doc)

    def test_asset_proof_cannot_omit_contract_binding(self):
        self.doc.records["proof"].fields["bs"] = [b for b in self.doc.records["proof"].fields["bs"] if b["rf"].id != "style"]
        with self.assertRaisesRegex(PixlError, "evidence_context|decision_proof"):
            graph.validate(self.doc)

    def test_done_needs_bound_passing_evidence(self):
        task = self.doc.records["task"].fields
        task["st"] = Symbol("done")
        with self.assertRaisesRegex(PixlError, "completion"):
            graph.validate(self.doc)
        task["ev"] = [Ref("proof")]
        graph.validate(self.doc, self.root)
        self.assertEqual(graph.ready(self.doc), [])

    def test_no_silent_context_truncation(self):
        with self.assertRaisesRegex(PixlError, "context_budget"):
            graph.context(self.doc, "task", budget=20)

    def test_impact_carries_reverse_transitive_dependencies(self):
        self.assertEqual(set(graph.impact(self.doc, "asset")), {"asset", "proof", "decision", "task"})

    def test_does_not_load_unrelated_task_into_context(self):
        other = deepcopy(self.doc.records["task"])
        other.id = "unrelated"
        self.doc.records[other.id] = other
        self.assertNotIn("unrelated", graph.context(self.doc, "task").records)

    def test_path_escape_is_rejected(self):
        self.doc.records["source"].fields["ur"] = "../outside.txt"
        with self.assertRaisesRegex(PixlError, "path_escape"):
            graph.validate(self.doc, self.root)

    def test_closed_schema_rejects_undeclared_field(self):
        self.doc.records["task"].fields["invented"] = 4
        with self.assertRaisesRegex(PixlError, "unknown_field"):
            graph.validate(self.doc)

    def test_active_method_cannot_borrow_unrelated_asset_proof(self):
        self.doc.records["method"] = Record("method", "K", {"nm": "unproven", "ap": [Symbol("sprite")],
            "op": ["new algorithm"], "ck": ["real execution"], "so": [Ref("source")], "pc": [Ref("proof")]})
        self.doc.records["task"].fields["kn"] = [Ref("method")]
        self.doc.records["task"].fields["st"] = Symbol("active")
        with self.assertRaisesRegex(PixlError, "method_poc"):
            graph.validate(self.doc)

    def test_decision_cannot_change_what_without_new_evidence(self):
        self.doc.records["decision"].fields["wt"] = "entirely different design"
        with self.assertRaisesRegex(PixlError, "stale_evidence|decision_proof"):
            graph.validate(self.doc)

    def test_superseded_evidence_is_preserved_but_cannot_complete_work(self):
        old = deepcopy(self.doc.records["proof"])
        old.id = "oldproof"
        old.fields["ob"] = True
        old.fields["bs"][0]["dg"] = "0" * 64
        self.doc.records[old.id] = old
        graph.validate(self.doc)
        self.doc.records["task"].fields["st"] = Symbol("done")
        self.doc.records["task"].fields["ev"] = [Ref("oldproof")]
        with self.assertRaisesRegex(PixlError, "completion"):
            graph.validate(self.doc)
