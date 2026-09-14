"""Persisted job mechanics with explicitly synthetic provider observations."""

import json
import unittest
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier
from unittest.mock import patch

from PIL import Image

from pixl import codec, graph, store
from tests.lifecycle_support import sample


class JobsTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / ".pixl"
        store.initialize(self.folder, sample(self.root), self.root)

    def current(self):
        return store.load(self.folder)

    def expected(self):
        return codec.digest(self.current())

    def prepare(self, id_="job", **changes):
        from pixl import jobs

        args = {
            "folder": self.folder,
            "expected": self.expected(),
            "job_id": id_,
            "task_id": "task",
            "outputs": ["output"],
            "provider": "fictional-fixture",
            "tool": "generate_fixture",
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
                "scope": "Local test only; no paid generation",
                "evidence": {"fixture": True},
            },
            "root": self.root,
        }
        args.update(changes)
        return jobs.prepare(**args)

    def dispatch(self):
        from pixl import jobs

        return jobs.dispatch(self.folder, self.expected(), "job", root=self.root)

    def observe(self, event, remote_id=None):
        from pixl import jobs

        return jobs.observe(
            self.folder,
            self.expected(),
            "job",
            event,
            {"fixture": "caller-supplied observation"},
            remote_id=remote_id,
            root=self.root,
        )

    def test_unknown_submission_resumes_then_imports_without_acceptance(self):
        from pixl import jobs, service

        prepared = self.prepare()
        self.assertEqual(prepared["job"]["state"], "prepared")
        self.assertNotIn("dispatch_request", prepared)
        dispatched = self.dispatch()
        self.assertEqual(
            dispatched["dispatch_request"]["arguments"], {"description": "fixture"}
        )
        self.assertEqual(dispatched["job"]["state"], "unknown")
        cold = jobs.report(self.current(), self.root)
        self.assertEqual(cold["jobs"][0]["next_action"], "reconcile")
        self.assertFalse(cold["remote_executed"])
        self.observe("unknown")
        self.observe("running", "fixture-remote-id")
        self.observe("running")
        self.observe("succeeded")
        Image.new("RGBA", (2, 2), "magenta").save(self.root / "download.png")
        imported = jobs.import_artifact(
            self.folder,
            self.expected(),
            "job",
            "output",
            "candidate",
            "download.png",
            {"fixture": "downloaded locally"},
            root=self.root,
        )
        artifact = self.current().records["candidate"]
        self.assertEqual(artifact.fields["of"], codec.Ref("output"))
        self.assertNotEqual(artifact.fields["ur"], "download.png")
        self.assertEqual(
            (self.root / artifact.fields["ur"]).read_bytes(),
            (self.root / "download.png").read_bytes(),
        )
        self.assertEqual(imported["job"]["state"], "succeeded")
        task = service.workflow(self.folder / "state.px", self.root)["tasks"][0]
        self.assertIsNone(task["outputs"][0]["candidate"])
        self.assertEqual(
            {q["status"] for q in task["outputs"][0]["candidates"][0]["requirements"]},
            {"unperformed"},
        )
        self.assertEqual(
            self.current().records["task"].fields["st"], codec.Symbol("open")
        )
        packet = graph.context(self.current(), "job")
        self.assertIn("candidate", packet.records)
        graph.validate(packet, self.root)

    def test_changed_contract_cannot_relabel_old_provider_output(self):
        from pixl import jobs

        self.prepare()
        self.dispatch()
        self.observe("succeeded", "fixture-id")
        changed = self.current()
        changed.records["contract"].fields["li"] = (
            "A different intended light direction"
        )
        changed.revision += 1
        store.commit(self.folder, changed, self.expected(), self.root)
        Image.new("RGBA", (2, 2), "magenta").save(self.root / "download.png")
        with self.assertRaisesRegex(codec.PixlError, "job_stale"):
            jobs.import_artifact(
                self.folder,
                self.expected(),
                "job",
                "output",
                "candidate",
                "download.png",
                {"fixture": True},
                root=self.root,
            )

    def test_dispatch_cannot_repeat_or_reuse_stale_hash(self):
        from pixl import jobs

        self.prepare()
        expected = self.expected()
        self.dispatch()
        before = codec.encode(self.current())
        with self.assertRaisesRegex(codec.PixlError, "stale_write"):
            jobs.dispatch(self.folder, expected, "job", root=self.root)
        with self.assertRaises(codec.PixlError):
            self.dispatch()
        self.assertEqual(codec.encode(self.current()), before)

    def test_competing_dispatchers_return_only_one_request(self):
        from pixl import jobs

        self.prepare()
        expected = self.expected()
        barrier = Barrier(2)

        def claim():
            barrier.wait(timeout=5)
            try:
                return jobs.dispatch(self.folder, expected, "job", root=self.root)
            except codec.PixlError as error:
                return {"error": error.code}

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: claim(), range(2)))
        self.assertEqual(sum("dispatch_request" in result for result in results), 1)
        failures = [r["error"] for r in results if "error" in r]
        self.assertEqual(len(failures), 1)
        self.assertIn(failures[0], {"stale_write", "store_locked"})
        self.assertEqual(
            self.current().records["job"].fields["si"], codec.Symbol("unknown")
        )

    def test_direct_preparation_cannot_change_its_plan_in_same_commit(self):
        from pixl import job_history, jobs, platform

        changed = self.current()
        changed.records["q.visual"].fields["ck"] = "Changed acceptance before intent"
        request = platform.prepare_discovered(
            "fixture",
            "fixture",
            {},
            {"type": "object"},
            {
                "source": "fixture",
                "observed_at": "2026-09-11T00:00:00Z",
                "evidence": {"fixture": True},
            },
            {"scope": "Fixture only", "evidence": {"fixture": True}},
        )
        journal = job_history.new(
            "job", request, jobs._context(changed, "task", ["output"])
        )
        jobs._project(changed, self.folder, self.root, journal)
        changed.revision += 1
        with self.assertRaisesRegex(codec.PixlError, "job_stale"):
            store.commit(self.folder, changed, self.expected(), self.root)

    def test_pending_attempt_blocks_different_request_for_same_output(self):
        self.prepare()
        with self.assertRaisesRegex(codec.PixlError, "job_pending"):
            self.prepare("second", arguments={"description": "different fixture"})
        self.dispatch()
        with self.assertRaisesRegex(codec.PixlError, "job_pending"):
            self.prepare("third")

    def test_failed_attempt_allows_new_authorized_intent(self):
        self.prepare()
        self.observe("failed")
        result = self.prepare("retry")
        self.assertEqual(result["job"]["state"], "prepared")
        self.assertIn("job", self.current().records)

    def test_plan_drift_blocks_dispatch_but_preserves_observation(self):
        from pixl import jobs

        self.prepare()
        changed = self.current()
        changed.records["contract"].fields["li"] = "Revised fixture lighting"
        changed.revision += 1
        store.commit(self.folder, changed, self.expected(), self.root)
        with self.assertRaisesRegex(codec.PixlError, "job_stale"):
            self.dispatch()
        self.assertTrue(jobs.report(self.current(), self.root)["jobs"][0]["stale"])
        self.observe("failed")

    def test_unrelated_project_change_does_not_block_dispatch(self):
        self.prepare()
        changed = self.current()
        changed.records["project"].fields["nm"] = "Different display name"
        changed.revision += 1
        store.commit(self.folder, changed, self.expected(), self.root)
        self.dispatch()

    def test_unknown_output_choice_blocks_preparation(self):
        changed = self.current()
        changed.records["choice"].fields.update(st=codec.Symbol("unresolved"), vl=None)
        changed.revision += 1
        store.commit(self.folder, changed, self.expected(), self.root)
        with self.assertRaisesRegex(codec.PixlError, "job_blocked"):
            self.prepare()

    def test_lost_publish_does_not_grant_dispatch(self):
        self.prepare()
        before = codec.encode(self.current())
        with patch(
            "pixl.store._publish", side_effect=OSError("fixture publication failure")
        ), self.assertRaisesRegex(OSError, "fixture publication failure"):
            self.dispatch()
        self.assertEqual(codec.encode(self.current()), before)
        result = self.dispatch()
        self.assertIn("dispatch_request", result)

    def test_direct_job_projection_tamper_preserves_state(self):
        self.prepare()
        changed = self.current()
        changed.records["job"].fields.update(
            si=codec.Symbol("succeeded"), ri="invented"
        )
        changed.revision += 1
        before = codec.encode(self.current())
        with self.assertRaises(codec.PixlError):
            store.commit(self.folder, changed, self.expected(), self.root)
        self.assertEqual(codec.encode(self.current()), before)

    def test_journal_file_drift_is_rejected(self):
        from pixl import jobs

        self.prepare()
        doc = self.current()
        snapshot = doc.records[doc.records["job"].fields["jr"].id]
        path = self.root / snapshot.fields["ur"]
        journal = json.loads(path.read_bytes())
        journal["state"] = "succeeded"
        path.write_text(json.dumps(journal), encoding="utf-8")
        with self.assertRaises(codec.PixlError):
            jobs.report(doc, self.root)

    def test_prepared_snapshot_cannot_initialize_a_fabricated_success(self):
        self.prepare()
        self.dispatch()
        self.observe("succeeded", "fixture-id")
        candidate = self.current()
        candidate.revision = 0
        with self.assertRaisesRegex(codec.PixlError, "job_history"):
            store.initialize(self.root / "other", candidate, self.root)

    def test_old_journal_receipt_and_snapshot_cannot_be_rewritten(self):
        self.prepare()
        old = deepcopy(self.current().records)
        self.dispatch()
        changed = self.current()
        snapshot_id = old["job"].fields["jr"].id
        changed.records[snapshot_id].fields["nm"] = "Rewritten historical snapshot"
        receipt = old["job"].fields["ev"][0].id
        changed.records[receipt].fields["ob"] = True
        changed.revision += 1
        with self.assertRaises(codec.PixlError):
            store.commit(self.folder, changed, self.expected(), self.root)

    def test_direct_commit_cannot_publish_a_journal_outside_immutable_storage(self):
        from pixl import job_history, jobs

        self.prepare()
        changed = self.current()
        journal = job_history.append(
            jobs._get(changed, "job", self.root), "dispatch", {"fixture": True}
        )
        jobs._project(changed, self.folder, self.root, journal)
        fields = changed.records["job"].fields
        snapshot = changed.records[fields["jr"].id]
        receipt = changed.records[fields["ev"][-1].id]
        (self.root / "journal.json").write_bytes(
            (self.root / snapshot.fields["ur"]).read_bytes()
        )
        snapshot.fields["ur"] = "journal.json"
        receipt.fields["ur"] = "journal.json"
        receipt.fields["bs"][0]["dg"] = codec.record_hash(snapshot)
        changed.revision += 1
        with self.assertRaisesRegex(codec.PixlError, "job_storage"):
            store.commit(self.folder, changed, self.expected(), self.root)

    def test_direct_commit_cannot_import_an_unretained_working_file(self):
        from pixl import job_history, jobs

        self.prepare()
        self.dispatch()
        self.observe("succeeded", "fixture-id")
        changed = self.current()
        path = self.root / "download.bin"
        path.write_bytes(b"caller supplied downloaded fixture")
        candidate = codec.Record(
            "candidate",
            "X",
            {
                "nm": "Fixture",
                "ur": path.name,
                "dg": graph.file_hash(path),
                "kd": codec.Symbol("sprite"),
                "ct": codec.Ref("contract"),
                "of": codec.Ref("output"),
            },
        )
        changed.records["candidate"] = candidate
        journal = job_history.append(
            jobs._get(self.current(), "job", self.root),
            "imported",
            {"fixture": True},
            artifact={
                "id": "candidate",
                "output": "output",
                "record_sha256": codec.record_hash(candidate),
            },
        )
        jobs._project(changed, self.folder, self.root, journal)
        changed.revision += 1
        with self.assertRaisesRegex(codec.PixlError, "job_storage"):
            store.commit(self.folder, changed, self.expected(), self.root)

    def test_remote_identity_cannot_be_rebound(self):
        self.prepare()
        self.dispatch()
        self.observe("submitted", "fixture-id")
        with self.assertRaises(codec.PixlError):
            self.observe("running", "another-id")

    def test_import_requires_success_and_keeps_original_download(self):
        from pixl import jobs

        self.prepare()
        Image.new("RGBA", (2, 2), "magenta").save(self.root / "download.png")
        before = (self.root / "download.png").read_bytes()
        with self.assertRaises(codec.PixlError):
            jobs.import_artifact(
                self.folder,
                self.expected(),
                "job",
                "output",
                "candidate",
                "download.png",
                {"fixture": True},
                root=self.root,
            )
        self.assertEqual((self.root / "download.png").read_bytes(), before)

    def test_legacy_jobs_do_not_silently_gain_durable_history(self):
        from pixl import jobs

        changed = self.current()
        changed.records["legacy"] = codec.Record(
            "legacy",
            "J",
            {
                "tk": codec.Ref("task"),
                "tl": "fixture",
                "ah": "a" * 64,
                "si": codec.Symbol("prepared"),
                "ri": "",
                "ev": [],
            },
        )
        changed.revision += 1
        store.commit(self.folder, changed, self.expected(), self.root)
        graph.validate(self.current(), self.root)
        with self.assertRaisesRegex(codec.PixlError, "job_pending"):
            self.prepare()
        report = jobs.report(self.current(), self.root)
        self.assertFalse(report["jobs"][0]["durable"])


if __name__ == "__main__":
    unittest.main()
