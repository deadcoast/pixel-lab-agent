"""Cross-layer PLAR planning, revision, allocation and acceptance regressions."""

import copy
import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, completion, graph, jobs, plar, service, store
from pixl.codec import PixlError, Record, Ref, Symbol
from tests.lifecycle_support import add_candidate, add_verdict, sample
from tests.test_plar_prepare import seed, write


class PLARWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "consumer"
        self.args, self.packet, self.plan, self.arguments = seed(self.root)

    def prepare(self, **options):
        return service.call("pixl_plar_prepare", {**self.args, **options}, self.root)

    def selected(self):
        return plar.read(self.root, asset_id=self.args["asset_id"])

    def files(self):
        return {
            p.relative_to(self.root).as_posix(): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }

    def revise_packet(self, source_change=False):
        if source_change:
            source = self.root / "BRIEF.md"
            source.write_text(
                source.read_text(encoding="utf-8")
                + "\nNew owner requirement: preserve a clearly asymmetrical motion cue.\n",
                encoding="utf-8",
            )
            document = json.loads((self.root / "plar.txt").read_bytes())
            for row in document["sources"]:
                if row["path"] == "BRIEF.md":
                    row.pop("sha256", None)
            for row in document["assets"]:
                if row["id"] == "queue.working":
                    row["purpose"] += " With asymmetrical motion."
            plar.save(self.root, document, plar.read(self.root)["hash"])
        current = self.selected()
        self.args["requirements_hash"] = current["requirements_hash"]
        self.packet["requirements_hash"] = current["requirements_hash"]
        self.packet["sources"] = [
            {"path": row["path"], "sha256": row["sha256"], "role": "consumer source"}
            for row in current["sources"]
        ]
        self.plan["outputs"][0]["criteria"][1]["check"] += (
            " Preserve asymmetrical motion."
        )
        self.packet["criteria"] = write(self.root, "work/criteria-r2.json", self.plan)
        self.arguments["description"] += " Preserve asymmetrical motion."
        self.packet["request"].update(
            write(self.root, "work/arguments-r2.json", self.arguments)
        )
        self.args["packet"] = "work/request-review-r2.json"
        write(self.root, self.args["packet"], self.packet)

    def terminal(self, result):
        return jobs.observe(
            self.root / result["store"],
            result["hash"],
            result["job"]["id"],
            "failed",
            {
                "fixture": "Explicit test observation: original attempt ended without an image."
            },
            root=self.root,
        )

    def test_first_request_links_asset_and_exposes_exact_pending_context(self):
        before = self.selected()
        result = self.prepare()
        current = self.selected()
        self.assertEqual(result["allocation"]["status"], "linked")
        self.assertEqual(before["requirements_hash"], current["requirements_hash"])
        self.assertEqual(current["asset"]["production"]["task"], result["task"])
        status = current["production"]
        self.assertEqual(status["next_action"], "dispatch")
        self.assertEqual(status["pending_jobs"], ["first_request"])
        self.assertFalse(status["new_request_allowed"])
        self.assertEqual(
            status["jobs"][0]["provider"], self.args["connection"]["provider"]
        )
        self.assertTrue(
            (self.root / current["asset"]["evidence"][-1]["path"]).is_file()
        )
        unchanged = self.files()
        self.prepare()
        self.assertEqual(unchanged, self.files())

    def test_source_table_reordering_resumes_exact_current_job_without_writes(self):
        first = self.prepare()
        document = json.loads((self.root / "plar.txt").read_bytes())
        document["sources"].reverse()
        plar.save(self.root, document, plar.read(self.root)["hash"])
        before = self.files()
        second = self.prepare()
        self.assertTrue(second["already_prepared"])
        self.assertEqual(second["hash"], first["hash"])
        self.assertEqual(before, self.files())

    def test_precanonical_snapshot_resumes_after_source_reorder_without_migration(self):
        # Reproduce the old identity algorithm; keep its saved bytes and IDs.
        with patch("pixl.plar_prepare._canonical_identity", side_effect=copy.deepcopy):
            first = self.prepare()
        document = json.loads((self.root / "plar.txt").read_bytes())
        document["sources"].reverse()
        plar.save(self.root, document, plar.read(self.root)["hash"])
        before = self.files()
        second = self.prepare()
        self.assertTrue(second["already_prepared"])
        self.assertEqual(second["hash"], first["hash"])
        self.assertEqual(second["task"], first["task"])
        self.assertEqual(second["job"]["id"], first["job"]["id"])
        self.assertEqual(before, self.files())

    def test_revision_accepts_explicit_selection_metadata_on_a_text_report(self):
        from hashlib import sha256

        first = self.prepare()
        terminal = self.terminal(first)
        folder = self.root / first["store"]
        current = store.load(folder)
        report = self.root / "work/selection.txt"
        report.write_text(
            "Explicit PLAR binding report, not a preparation snapshot.",
            encoding="utf-8",
        )
        current.records["selection"].fields.update(
            ur="work/selection.txt", dg=sha256(report.read_bytes()).hexdigest()
        )
        current.revision += 1
        store.commit(folder, current, terminal["hash"], self.root)
        self.revise_packet()
        revised = self.prepare(revise=True, expect=codec.digest(current))
        self.assertEqual(revised["job"]["state"], "prepared")
        self.assertEqual(revised["job"]["next_action"], "dispatch")
        self.assertEqual(
            store.load(folder).records["selection"], current.records["selection"]
        )

    def test_custom_linked_store_resumes_without_repeating_store_option(self):
        first = self.prepare(store="work/retained asset")
        second = self.prepare()
        self.assertEqual(first["hash"], second["hash"])
        self.assertEqual(second["store"], "work/retained asset")

    def test_interrupted_allocation_link_is_discoverable_and_repairable(self):
        with patch(
            "pixl.plar_workflow.synchronize",
            return_value={"status": "needs_reconciliation"},
        ):
            first = self.prepare()
        status = self.selected()["production"]
        self.assertEqual(status["link_status"], "discovered")
        self.assertEqual(status["pending_jobs"], ["first_request"])
        second = self.prepare()
        self.assertEqual(first["hash"], second["hash"])
        self.assertEqual(second["allocation"]["status"], "linked")

    def test_allocation_cas_conflict_retains_job_and_preserves_other_rows(self):
        original_save = plar.save
        changed = False

        def concurrent(root, document, expected, path="plar.txt"):
            nonlocal changed
            if not changed:
                changed = True
                update = json.loads((self.root / "plar.txt").read_bytes())
                update["assets"][-1]["next"] = "Concurrent caller priority note"
                original_save(root, update, expected, path)
            return original_save(root, document, expected, path)

        with patch("pixl.plar.save", side_effect=concurrent):
            first = self.prepare()
        self.assertEqual(first["allocation"]["status"], "needs_reconciliation")
        self.assertEqual(
            json.loads((self.root / "plar.txt").read_bytes())["assets"][-1]["next"],
            "Concurrent caller priority note",
        )
        self.assertEqual(self.prepare()["hash"], first["hash"])

    def test_changed_contract_cannot_bypass_pending_job_by_provider_or_new_task(self):
        first = self.prepare()
        dispatch = jobs.dispatch(
            self.root / first["store"], first["hash"], "first_request", self.root
        )
        submitted = jobs.observe(
            self.root / first["store"],
            dispatch["hash"],
            "first_request",
            "submitted",
            {"fixture": True},
            remote_id="original-provider-id",
            root=self.root,
        )
        self.revise_packet(source_change=True)
        self.args["connection"]["provider"] = "another-connection"
        before = self.files()
        with self.assertRaisesRegex(PixlError, "job_pending"):
            self.prepare(revise=True, expect=submitted["hash"])
        self.assertEqual(before, self.files())
        status = self.selected()["production"]
        self.assertEqual(status["next_action"], "observe")
        self.assertFalse(status["selection_current"])
        self.assertEqual(status["jobs"][0]["remote_id"], "original-provider-id")

    def test_revision_retains_original_plan_and_journal_and_links_new_generation(self):
        first = self.prepare()
        terminal = self.terminal(first)
        folder = self.root / first["store"]
        original = store.load(folder)
        self.revise_packet(source_change=True)
        second = self.prepare(revise=True, expect=terminal["hash"])
        self.assertNotEqual(first["task"], second["task"])
        self.assertEqual(second["job"]["next_action"], "dispatch")
        self.assertNotEqual(first["outputs"], second["outputs"])
        current = store.load(folder)
        for id_, record in original.records.items():
            if id_ != "project":
                self.assertEqual(record, current.records[id_])
        self.assertEqual(current.records[second["task"]].fields["ca"], [])
        self.assertEqual(current.records[second["task"]].fields["vr"], [])
        self.assertFalse(any(r.kind == "V" for r in current.records.values()))
        self.assertEqual(self.selected()["asset"]["production"]["task"], second["task"])
        self.assertEqual(self.prepare()["hash"], second["hash"])
        sent = jobs.dispatch(folder, second["hash"], second["job"]["id"], self.root)
        self.assertEqual(sent["dispatch_request"]["arguments"], self.arguments)
        self.assertEqual(
            jobs.report(store.load(folder), self.root)["jobs"][0]["state"], "failed"
        )
        moved = self.root.parent / "relocated"
        shutil.copytree(self.root, moved)
        self.assertEqual(
            plar.read(moved, asset_id="queue.working")["production"]["next_action"],
            "reconcile",
        )

    def test_revision_requires_current_cas_and_explicit_intent_before_writes(self):
        first = self.prepare()
        terminal = self.terminal(first)
        self.revise_packet()
        before = self.files()
        for options in (
            {},
            {"revise": True},
            {"revise": True, "expect": first["hash"]},
        ):
            with self.assertRaises(PixlError):
                self.prepare(**options)
            self.assertEqual(before, self.files())
        self.assertEqual(
            self.prepare(revise=True, expect=terminal["hash"])["job"]["state"],
            "prepared",
        )

    def test_interrupted_revision_job_publication_resumes_same_generation(self):
        first = self.prepare()
        terminal = self.terminal(first)
        self.revise_packet()
        with (
            patch("pixl.plar_prepare.jobs.prepare", side_effect=OSError("interrupted")),
            self.assertRaises(OSError),
        ):
            self.prepare(revise=True, expect=terminal["hash"])
        folder = self.root / first["store"]
        partial = store.load(folder)
        self.assertEqual(sum(r.kind == "T" for r in partial.records.values()), 2)
        resumed = self.prepare(revise=True, expect=codec.digest(partial))
        self.assertEqual(
            sum(r.kind == "T" for r in store.load(folder).records.values()), 2
        )
        self.assertEqual(resumed["job"]["state"], "prepared")

    def test_low_level_prepare_cannot_duplicate_same_asset_under_new_output_ids(self):
        first = self.prepare()
        folder = self.root / first["store"]
        current = store.load(folder)
        candidate = copy.deepcopy(current)
        task = copy.deepcopy(candidate.records["task"])
        task.id = "other.task"
        task.fields["op"] = [Ref("other.output")]
        output = copy.deepcopy(candidate.records["output.working"])
        output.id = "other.output"
        output.fields["tk"] = Ref(task.id)
        candidate.records[task.id] = task
        candidate.records[output.id] = output
        candidate.revision += 1
        store.commit(folder, candidate, first["hash"], self.root)
        before = self.files()
        with self.assertRaisesRegex(PixlError, "job_pending"):
            jobs.prepare(
                folder,
                codec.digest(candidate),
                "other.job",
                task.id,
                [output.id],
                tool="create_image_pro_flash",
                arguments=self.arguments,
                root=self.root,
                **self.args["connection"],
            )
        self.assertEqual(before, self.files())

    def test_wrong_and_missing_links_are_actionable_without_losing_requirements(self):
        first = self.prepare()
        document = json.loads((self.root / "plar.txt").read_bytes())
        document["assets"][0]["production"]["task"] = "does.not.exist"
        plar.save(self.root, document, plar.read(self.root)["hash"])
        self.assertEqual(self.selected()["production"]["status"], "unavailable")
        self.assertIn("requirements", self.selected()["asset"])
        (self.root / first["store"] / "state.px").rename(
            self.root / first["store"] / "state-retained.px"
        )
        self.assertEqual(
            self.selected()["production"]["next_action"], "restore_linked_state"
        )

    def reviewed_sample(self):
        doc = sample(self.root)
        binding = write(self.root, "binding.json", {"fixture": "explicit PLAR input"})
        doc.records["selection"] = Record(
            "selection",
            "X",
            {
                "nm": "Selection",
                "ur": binding["path"],
                "dg": binding["sha256"],
                "kd": Symbol("report"),
                "mt": {
                    "binding": "pixl.plar.selection/1",
                    "plar_path": "plar.txt",
                    "asset_id": "queue.working",
                    "requirements_hash": self.selected()["requirements_hash"],
                },
            },
        )
        doc.records["task"].fields["ip"].append(Ref("selection"))
        add_candidate(doc, self.root, "candidate")
        doc.records["task"].fields["ca"] = []
        folder = self.root / "reviewed"
        store.initialize(folder, doc, self.root)
        reviewed = copy.deepcopy(doc)
        reviewed.revision += 1
        for index, criterion in enumerate(("q.mechanical", "q.visual", "q.engine")):
            add_verdict(
                reviewed, self.root, "candidate", criterion, "pass", f"verdict{index}"
            )
        store.commit(folder, reviewed, codec.digest(doc), self.root)
        return folder, reviewed

    def test_changed_consumer_cannot_complete_or_activate_old_review_but_history_reads(
        self,
    ):
        folder, reviewed = self.reviewed_sample()
        (self.root / "BRIEF.md").write_text(
            "Changed consumer request", encoding="utf-8"
        )
        graph.validate(store.load(folder), self.root)
        workflow = service.workflow(folder / "state.px", self.root)
        self.assertNotIn("task", workflow["ready"])
        self.assertTrue(workflow["tasks"][0]["selection_bindings"])
        before = self.files()
        with self.assertRaisesRegex(PixlError, "plar_selection"):
            completion.complete(
                folder, codec.digest(reviewed), "task", ["candidate"], self.root
            )
        next_doc = copy.deepcopy(reviewed)
        next_doc.revision += 1
        next_doc.records["task"].fields["st"] = Symbol("active")
        with self.assertRaisesRegex(PixlError, "plar_selection"):
            store.commit(folder, next_doc, codec.digest(reviewed), self.root)
        self.assertEqual(before, self.files())

    def test_done_history_remains_readable_but_stale_recompletion_is_not_current_acceptance(
        self,
    ):
        folder, reviewed = self.reviewed_sample()
        done = completion.complete(
            folder, codec.digest(reviewed), "task", ["candidate"], self.root
        )
        (self.root / "BRIEF.md").write_text(
            "Changed consumer request", encoding="utf-8"
        )
        graph.validate(store.load(folder), self.root)
        with self.assertRaisesRegex(PixlError, "plar_selection"):
            completion.complete(folder, done["hash"], "task", ["candidate"], self.root)
        self.assertEqual(
            service.workflow(folder / "state.px", self.root)["tasks"][0]["state"],
            "done",
        )

    def test_same_task_name_in_a_different_selected_store_cannot_dispatch(self):
        first = self.prepare()
        document = json.loads((self.root / "plar.txt").read_bytes())
        document["assets"][0]["production"]["store"] = "another-context"
        plar.save(self.root, document, plar.read(self.root)["hash"])
        before = self.files()
        with self.assertRaisesRegex(PixlError, "job_blocked"):
            jobs.dispatch(
                self.root / first["store"], first["hash"], "first_request", self.root
            )
        self.assertEqual(before, self.files())
        reported = service.job_report(
            self.root / first["store"] / "state.px", self.root
        )
        self.assertFalse(
            reported["jobs"][0]["selection_bindings"][0]["selected_for_asset"]
        )

    def test_revision_link_interruption_resumes_job_and_returns_current_action(self):
        first = self.prepare()
        terminal = self.terminal(first)
        self.revise_packet()
        with patch(
            "pixl.plar_workflow.synchronize",
            return_value={"status": "needs_reconciliation"},
        ):
            second = self.prepare(revise=True, expect=terminal["hash"])
        self.assertEqual(second["job"]["next_action"], "resolve_context")
        repaired = self.prepare(revise=True, expect=second["hash"])
        self.assertEqual(repaired["hash"], second["hash"])
        self.assertEqual(repaired["job"]["next_action"], "dispatch")
        self.assertEqual(self.selected()["asset"]["production"]["task"], second["task"])

    def test_initial_active_publication_cannot_bypass_changed_selection(self):
        _, reviewed = self.reviewed_sample()
        initial = sample(self.root)
        initial.records["selection"] = copy.deepcopy(reviewed.records["selection"])
        initial.records["task"].fields["ip"].append(Ref("selection"))
        initial.records["task"].fields["st"] = Symbol("active")
        (self.root / "BRIEF.md").write_text("New consumer", encoding="utf-8")
        folder = self.root / "new-active"
        with self.assertRaisesRegex(PixlError, "plar_selection"):
            store.initialize(folder, initial, self.root)
        self.assertFalse((folder / "state.px").exists())

    def test_revision_preserves_accepted_candidate_and_reviews_without_inheriting_them(
        self,
    ):
        from PIL import Image

        first = self.prepare()
        folder = self.root / first["store"]
        dispatched = jobs.dispatch(folder, first["hash"], "first_request", self.root)
        succeeded = jobs.observe(
            folder,
            dispatched["hash"],
            "first_request",
            "succeeded",
            {"fixture": "Synthetic lifecycle success, not PixelLab generation"},
            remote_id="synthetic-only",
            root=self.root,
        )
        Image.new("RGBA", (64, 16), "magenta").save(self.root / "synthetic.png")
        imported = jobs.import_artifact(
            folder,
            succeeded["hash"],
            "first_request",
            first["outputs"][0],
            "candidate",
            "synthetic.png",
            {"fixture": "Synthetic test raster"},
            root=self.root,
        )
        reviewed = store.load(folder)
        reviewed.revision += 1
        for index, criterion in enumerate(
            reviewed.records[first["outputs"][0]].fields["rq"]
        ):
            add_verdict(
                reviewed,
                self.root,
                "candidate",
                criterion.id,
                "pass",
                f"verdict{index}",
            )
        store.commit(folder, reviewed, imported["hash"], self.root)
        done = completion.complete(
            folder, codec.digest(reviewed), first["task"], ["candidate"], self.root
        )
        original = store.load(folder)
        self.revise_packet(source_change=True)
        second = self.prepare(revise=True, expect=done["hash"])
        current = store.load(folder)
        for id_, record in original.records.items():
            if id_ != "project":
                self.assertEqual(record, current.records[id_])
        self.assertEqual(current.records[first["task"]].fields["st"], Symbol("done"))
        self.assertEqual(current.records[second["task"]].fields["st"], Symbol("open"))
        self.assertEqual(current.records[second["task"]].fields["ca"], [])
        self.assertEqual(current.records[second["task"]].fields["vr"], [])
        self.assertEqual(second["job"]["next_action"], "dispatch")
        self.assertEqual(self.selected()["production"]["task"], second["task"])

    def test_cli_and_mcp_readiness_agree_with_current_consumer(self):
        import subprocess
        import sys

        folder, _ = self.reviewed_sample()
        (self.root / "BRIEF.md").write_text("New consumer", encoding="utf-8")
        args = {"path": (folder / "state.px").relative_to(self.root).as_posix()}
        mcp = service.call("pixl_ready", args, self.root)
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "pixl",
                "ready",
                str(self.root / args["path"]),
                "--root",
                str(self.root),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(json.loads(result.stdout), mcp)
        self.assertNotIn("task", mcp["ready"])


if __name__ == "__main__":
    unittest.main()
