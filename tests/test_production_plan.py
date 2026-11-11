"""Connected authoring/recovery checks; synthetic inputs establish no art quality."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pixl import codec, delivery, jobs, lifecycle, plar, production_plan, service, store
from pixl.codec import PixlError, Record, Ref, Symbol
from tests.family_support import family
from tests.test_plar_prepare import seed


def plan():
    criterion = {
        "id": "shape",
        "check": "Preserve the fixture's requested silhouette",
        "domain": "visual",
        "mode": "visual",
        "sources": ["source"],
    }
    return {
        "version": 1,
        "id": "next",
        "project": "project",
        "actor": "actor",
        "baseline": "sample",
        "decisions": ["decision"],
        "knowledge": ["method"],
        "stages": [
            {
                "id": "motion",
                "name": "Animate accepted fixture member",
                "phase": "production",
                "kind": "sprite",
                "contract": "contract",
                "needs": ["member.output"],
                "criteria": [criterion],
            }
        ],
        "delivery": {
            "name": "Next family",
            "members": ["output", "motion"],
            "destinations": ["destination"],
            "criteria": [{**criterion, "domain": "continuity"}],
        },
    }


def packet(doc):
    return {
        "version": 1,
        "inputs": {
            "member.output": {
                "candidate": "member",
                "sha256": doc.records["member"].fields["dg"],
            }
        },
        "request": {
            "provider": "fictional-fixture",
            "tool": "animate_fixture",
            "arguments": {"description": "fixture"},
            "schema": {
                "type": "object",
                "properties": {"description": {"type": "string"}},
                "required": ["description"],
                "additionalProperties": False,
            },
            "discovery": {
                "source": "fixture tools/list",
                "observed_at": "2026-09-11T12:00:00+00:00",
                "evidence": {"fixture": True},
            },
            "authorization": {
                "scope": "Synthetic local mechanics",
                "evidence": {"fixture": True},
            },
        },
    }


class ProductionPlanTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.folder = self.root / ".pixl"
        family(self.root)

    def current(self):
        return store.load(self.folder)

    def expected(self):
        return codec.digest(self.current())

    def author(self, value=None):
        return production_plan.author(
            self.folder, self.expected(), value or plan(), self.root
        )

    def prepare(self, value=None, job="next.job"):
        return production_plan.prepare(
            self.folder,
            self.expected(),
            "next.plan",
            "motion",
            job,
            value or packet(self.current()),
            self.root,
        )

    def test_compiles_connections_and_prepares_exact_input_without_acceptance(self):
        before = self.current()
        result = self.author()
        doc = self.current()
        self.assertFalse(result["remote_executed"])
        for ident, record in before.records.items():
            self.assertEqual(record, doc.records[ident])
        self.assertEqual(
            doc.records["next.motion.task"].fields["dp"],
            [Ref("task"), Ref("member.task")],
        )
        self.assertEqual(
            doc.records["next.delivery.output"].fields["mb"],
            [Ref("output"), Ref("next.motion.output")],
        )
        retained = self.expected()
        self.assertTrue(self.author()["already_authored"])
        self.assertEqual(self.expected(), retained)
        self.prepare()
        doc = self.current()
        self.assertIn(Ref("member"), doc.records["next.motion.task"].fields["ip"])
        self.assertEqual(doc.records["next.motion.task"].fields["st"], Symbol("open"))
        self.assertFalse(doc.records["next.motion.task"].fields["ca"])
        self.assertEqual(doc.records["next.job"].fields["si"], Symbol("prepared"))
        jobs.dispatch(self.folder, self.expected(), "next.job", self.root)
        retained = self.expected()
        result = self.prepare()
        self.assertTrue(result["already_prepared"])
        self.assertEqual(self.expected(), retained)
        self.assertEqual(
            self.current().records["next.job"].fields["si"], Symbol("unknown")
        )
        with self.assertRaises(PixlError):
            self.prepare(job="duplicate.job")

    def test_wrong_input_invalid_schema_and_missing_input_publish_nothing(self):
        self.author()
        for change in ("hash", "missing", "schema"):
            value = packet(self.current())
            if change == "hash":
                value["inputs"]["member.output"]["sha256"] = "0" * 64
            elif change == "missing":
                value["inputs"] = {}
            else:
                value["request"]["arguments"] = {"unsupported": True}
            before = self.expected()
            with self.assertRaises(PixlError):
                self.prepare(value)
            self.assertEqual(self.expected(), before)

    def test_delivery_only_plan_reuses_accepted_sample_without_new_production(self):
        value = plan()
        value["stages"] = []
        value["delivery"]["members"] = ["output"]
        before = self.current()
        result = self.author(value)
        doc = self.current()
        self.assertEqual(result["stages"], {})
        self.assertEqual(result["allocation"], [])
        self.assertFalse(result["accepted"])
        self.assertFalse(result["remote_executed"])
        self.assertEqual(set(doc.records) - set(before.records), {
            "next.plan", "next.delivery.task", "next.delivery.output",
            "next.delivery.q.shape",
        })
        for ident, record in before.records.items():
            self.assertEqual(record, doc.records[ident])
        self.assertEqual(doc.records["next.delivery.task"].fields["dp"], [Ref("task")])
        self.assertEqual(doc.records["next.delivery.output"].fields["mb"], [Ref("output")])
        retained = self.expected()
        self.assertTrue(self.author(value)["already_authored"])
        self.assertEqual(self.expected(), retained)
        with self.assertRaises(PixlError):
            self.prepare()
        self.assertEqual(self.expected(), retained)
        result = delivery.snapshot(
            self.folder, retained, "next.delivery.output", "next.package", self.root
        )
        self.assertFalse(result["accepted"])
        doc = self.current()
        self.assertEqual(doc.records["next.package"].fields["xs"], [Ref("sample"), Ref("sample")])
        self.assertEqual(doc.records["next.delivery.task"].fields["st"], Symbol("open"))
        self.assertEqual(doc.records["next.delivery.task"].fields["ca"], [])
        self.assertFalse(any(record.kind == "J" for record in doc.records.values()))

    def test_delivery_only_invalid_family_preserves_state(self):
        for change in ("empty", "missing", "candidate", "baseline", "destination", "continuity", "decision"):
            with self.subTest(change=change):
                value = plan()
                value["stages"] = []
                value["delivery"]["members"] = ["output"]
                if change in {"empty", "missing", "candidate"}:
                    value["delivery"]["members"] = {
                        "empty": [], "missing": ["motion"], "candidate": ["sample"]
                    }[change]
                elif change == "baseline":
                    value["baseline"] = "member"
                elif change == "destination":
                    value["delivery"]["destinations"] = []
                elif change == "continuity":
                    value["delivery"]["criteria"][0]["domain"] = "visual"
                else:
                    value["decisions"] = ["missing.decision"]
                before = self.expected()
                with self.assertRaises(PixlError):
                    self.author(value)
                self.assertEqual(self.expected(), before)

    def test_delivery_only_unaccepted_baseline_still_blocks_activation_and_snapshot(self):
        doc = self.current()
        original = doc.records["sample"]
        doc.records["unaccepted"] = Record("unaccepted", "X", dict(original.fields))
        doc.revision += 1
        store.commit(self.folder, doc, self.expected(), self.root)
        value = plan()
        value["stages"] = []
        value["baseline"] = "unaccepted"
        value["delivery"]["members"] = ["output"]
        self.author(value)
        before = self.expected()
        self.assertTrue(any("family_baseline" in reason for reason in
                            lifecycle.blockers(self.current(), "next.delivery.task")))
        with self.assertRaisesRegex(PixlError, "family_baseline"):
            delivery.snapshot(self.folder, before, "next.delivery.output", "next.package", self.root)
        self.assertEqual(self.expected(), before)
        for state in ("active", "done"):
            doc = self.current()
            doc.records["next.delivery.task"].fields["st"] = Symbol(state)
            doc.revision += 1
            with self.assertRaises(PixlError):
                store.commit(self.folder, doc, before, self.root)
            self.assertEqual(self.expected(), before)

    def test_delivery_only_snapshot_preserves_pending_job_gate(self):
        value = plan()
        value["stages"] = []
        value["delivery"]["members"] = ["output"]
        self.author(value)
        doc = self.current()
        doc.records["pending"] = Record("pending", "J", {
            "tk": Ref("task"), "tl": "synthetic", "ah": "a" * 64,
            "si": Symbol("unknown"), "ri": "", "ev": [],
        })
        doc.revision += 1
        store.commit(self.folder, doc, self.expected(), self.root)
        before = self.expected()
        with self.assertRaisesRegex(PixlError, "family_job"):
            delivery.snapshot(self.folder, before, "next.delivery.output", "next.package", self.root)
        self.assertEqual(self.expected(), before)

    def test_interrupted_input_binding_recovers_same_job(self):
        self.author()
        with (
            patch.object(
                jobs, "prepare", side_effect=OSError("interrupted before intent")
            ),
            self.assertRaises(OSError),
        ):
            self.prepare()
        self.assertNotIn("next.job", self.current().records)
        self.prepare()
        result = self.prepare()
        self.assertTrue(result["already_prepared"])
        self.assertEqual(sum(r.kind == "J" for r in self.current().records.values()), 1)

    def test_invalid_cycles_conflicting_ids_and_changed_retry_preserve_state(self):
        original = self.expected()
        value = plan()
        value["stages"][0]["needs"] = ["motion"]
        with self.assertRaises(PixlError):
            self.author(value)
        self.assertEqual(self.expected(), original)
        self.author()
        original = self.expected()
        value = plan()
        value["stages"][0]["criteria"][0]["check"] = "different"
        with self.assertRaises(PixlError):
            self.author(value)
        self.assertEqual(self.expected(), original)
        self.prepare()
        value = packet(self.current())
        value["request"]["arguments"]["description"] = "different"
        with self.assertRaises(PixlError):
            self.prepare(value)

    def test_service_surface_matches_direct_operation(self):
        result = service.call(
            "pixl_production_plan",
            {"store": ".pixl", "expect": self.expected(), "plan": plan()},
            self.root,
        )
        self.assertIn("next.motion.output", str(result))
        result = service.call(
            "pixl_stage_prepare",
            {
                "store": ".pixl",
                "expect": self.expected(),
                "plan": "next.plan",
                "stage": "motion",
                "job": "next.job",
                "packet": packet(self.current()),
            },
            self.root,
        )
        self.assertFalse(result["remote_executed"])

    def test_changed_authored_criteria_cannot_silently_reuse_plan(self):
        self.author()
        doc = self.current()
        expected = self.expected()
        doc.records["next.motion.q.shape"].fields["ck"] = "new requirement"
        doc.revision += 1
        store.commit(self.folder, doc, expected, self.root)
        with self.assertRaisesRegex(PixlError, "scope changed"):
            self.prepare()
        with self.assertRaisesRegex(PixlError, "scope changed"):
            self.author()

    def test_future_stage_cannot_prepare_before_seed_acceptance(self):
        value = plan()
        seed_stage = {
            **value["stages"][0],
            "id": "seed",
            "name": "Seed first",
            "phase": "sample",
            "needs": [],
        }
        value["stages"].insert(0, seed_stage)
        value["stages"][1]["needs"] = ["seed"]
        self.author(value)
        request = packet(self.current())
        request["inputs"] = {
            "next.seed.output": {
                "candidate": "member",
                "sha256": self.current().records["member"].fields["dg"],
            }
        }
        before = self.expected()
        with self.assertRaises(PixlError):
            self.prepare(request)
        self.assertEqual(self.expected(), before)

    def test_plar_link_recovery_and_requirement_drift(self):
        seed(self.root)
        value = plan()
        selected = plar.read(
            self.root, asset_id="queue.working", include_production=False
        )
        value["stages"][0]["selection"] = {
            "path": "plar.txt",
            "asset": "queue.working",
            "requirements_hash": selected["requirements_hash"],
        }
        # Store publication succeeds while the subsequent allocation CAS is interrupted.
        with patch.object(plar, "save", side_effect=OSError("interrupted allocation")):
            result = self.author(value)
        self.assertEqual(result["allocation"][0]["status"], "needs_reconciliation")
        retained = self.expected()
        self.assertEqual(self.author(value)["allocation"][0]["status"], "linked")
        self.assertEqual(retained, self.expected())
        selected = plar.read(self.root, asset_id="queue.working")
        self.assertEqual(selected["asset"]["production"]["task"], "next.motion.task")
        self.assertEqual(
            selected["requirements_hash"],
            value["stages"][0]["selection"]["requirements_hash"],
        )
        self.prepare()
        queue = json.loads((self.root / "plar.txt").read_text(encoding="utf-8"))
        asset = next(a for a in queue["assets"] if a["id"] == "queue.working")
        asset["purpose"] += " New requirement."
        plar.save(self.root, queue, plar.read(self.root)["hash"])
        with self.assertRaisesRegex(
            PixlError, "PLAR requirements changed|plar_selection"
        ):
            jobs.dispatch(self.folder, self.expected(), "next.job", self.root)
        self.assertEqual(
            self.current().records["next.job"].fields["si"], Symbol("prepared")
        )

    def linked_successor(self):
        seed(self.root)
        first = plan()
        selected = plar.read(self.root, asset_id="queue.working", include_production=False)
        first["stages"][0]["selection"] = {
            "path": "plar.txt", "asset": "queue.working",
            "requirements_hash": selected["requirements_hash"],
        }
        self.author(first)
        selected = plar.read(self.root, asset_id="queue.working", include_production=False)
        successor = plan()
        successor["id"] = "successor"
        successor["stages"][0]["selection"] = {
            **first["stages"][0]["selection"], "replaces": selected["asset"]["production"],
        }
        return successor

    def test_successor_requires_exact_link_and_resolved_old_intent(self):
        successor = self.linked_successor()
        self.prepare()
        before = self.expected()
        with self.assertRaises(PixlError):
            self.author(successor)
        self.assertEqual(self.expected(), before)
        jobs.observe(self.folder, before, "next.job", "failed", {"reason": "Local abandoned prepared fixture; not provider failure"}, root=self.root)
        historical = dict(self.current().records)
        result = self.author(successor)
        self.assertEqual(result["allocation"][0]["status"], "revised")
        self.assertEqual(result["allocation"][0]["previous_production"]["task"], "next.motion.task")
        self.assertTrue(all(self.current().records[k] == v for k, v in historical.items()))
        self.assertEqual(plar.read(self.root, asset_id="queue.working")["asset"]["production"]["task"], "successor.motion.task")
        self.assertEqual(plar.read(self.root, asset_id="queue.working")["asset"]["status"], "in_progress")
        self.assertFalse(result["accepted"])
        self.assertFalse(result["remote_executed"])
        self.assertEqual(self.author(successor)["allocation"][0]["status"], "unchanged")

    def test_successor_rejects_missing_or_wrong_replacement_without_mutation(self):
        successor = self.linked_successor()
        before = self.expected()
        selection = successor["stages"][0]["selection"]
        original = selection.pop("replaces")
        with self.assertRaises(PixlError):
            self.author(successor)
        selection["replaces"] = {**original, "task": "member.task"}
        with self.assertRaises(PixlError):
            self.author(successor)
        selection["replaces"] = {**original, "store": "another-store"}
        with self.assertRaises(PixlError):
            self.author(successor)
        self.assertEqual(self.expected(), before)

    def test_successor_interrupted_link_rechecks_pending_work_before_recovery(self):
        successor = self.linked_successor()
        with patch.object(plar, "save", side_effect=OSError("interrupted successor allocation")):
            result = self.author(successor)
        self.assertEqual(result["allocation"][0]["status"], "needs_reconciliation")
        retained = self.expected()
        self.prepare()  # Old link still owns the asset and may acquire work.
        blocked = self.author(successor)
        self.assertEqual(blocked["allocation"][0]["status"], "needs_reconciliation")
        self.assertEqual(plar.read(self.root, asset_id="queue.working")["asset"]["production"]["task"], "next.motion.task")
        jobs.observe(self.folder, self.expected(), "next.job", "failed", {"reason": "Local fixture abandonment"}, root=self.root)
        before_recovery = self.expected()
        self.assertEqual(self.author(successor)["allocation"][0]["status"], "revised")
        self.assertEqual(self.expected(), before_recovery)
        self.assertNotEqual(retained, before_recovery)

    def test_existing_asset_link_is_not_replaced(self):
        seed(self.root)
        queue = json.loads((self.root / "plar.txt").read_text(encoding="utf-8"))
        asset = next(a for a in queue["assets"] if a["id"] == "queue.working")
        asset["production"] = {
            "store": ".pixl",
            "task": "member.task",
            "output": "member.output",
        }
        plar.save(self.root, queue, plar.read(self.root)["hash"])
        value = plan()
        value["stages"][0]["selection"] = {
            "path": "plar.txt",
            "asset": "queue.working",
            "requirements_hash": plar.read(self.root, asset_id="queue.working")[
                "requirements_hash"
            ],
        }
        before = self.expected()
        with self.assertRaisesRegex(PixlError, "already has production"):
            self.author(value)
        self.assertEqual(before, self.expected())

    def test_downstream_change_blocks_seed_dispatch_and_activation_not_unrelated_stage(
        self,
    ):
        seed(self.root)
        value = plan()
        motion = value["stages"][0]
        selected = plar.read(
            self.root, asset_id="queue.working", include_production=False
        )
        motion["selection"] = {
            "path": "plar.txt",
            "asset": "queue.working",
            "requirements_hash": selected["requirements_hash"],
        }
        motion["needs"] = ["seed"]
        value["stages"].insert(
            0,
            {
                k: v
                for k, v in {
                    **motion,
                    "id": "seed",
                    "name": "Preparatory seed",
                    "phase": "sample",
                    "needs": [],
                }.items()
                if k != "selection"
            },
        )
        retry = {
            k: v
            for k, v in {
                **motion,
                "id": "retry",
                "name": "Independent Retry",
                "needs": [],
            }.items()
            if k != "selection"
        }
        selected = plar.read(
            self.root, asset_id="queue.start", include_production=False
        )
        retry["selection"] = {
            "path": "plar.txt",
            "asset": "queue.start",
            "requirements_hash": selected["requirements_hash"],
        }
        value["stages"].append(retry)
        value["delivery"]["members"].append("retry")
        self.author(value)
        request = packet(self.current())
        request["inputs"] = {}
        production_plan.prepare(
            self.folder,
            self.expected(),
            "next.plan",
            "seed",
            "seed.job",
            request,
            self.root,
        )
        queue = json.loads((self.root / "plar.txt").read_text(encoding="utf-8"))
        next(a for a in queue["assets"] if a["id"] == "queue.working")["purpose"] += (
            " Changed downstream target."
        )
        plar.save(self.root, queue, plar.read(self.root)["hash"])
        with self.assertRaisesRegex(PixlError, "PLAR requirements changed"):
            jobs.dispatch(self.folder, self.expected(), "seed.job", self.root)
        doc = self.current()
        expected = self.expected()
        doc.records["next.seed.task"].fields["st"] = Symbol("active")
        doc.revision += 1
        with self.assertRaisesRegex(PixlError, "PLAR requirements changed"):
            store.commit(self.folder, doc, expected, self.root)
        # A different member does not inherit this row's change merely by sharing a plan.
        production_plan.prepare(
            self.folder,
            self.expected(),
            "next.plan",
            "retry",
            "retry.job",
            request,
            self.root,
        )
        self.assertEqual(
            self.current().records["retry.job"].fields["si"], Symbol("prepared")
        )


if __name__ == "__main__":
    unittest.main()
