"""TM-03 controlled publication faults; no remote, visual or engine acceptance."""

import hashlib
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Barrier
from unittest.mock import patch

from PIL import Image

from pixl import candidate_review as review
from pixl import codec, graph, jobs, store
from tests.lifecycle_support import add_candidate, sample


class RecoveryPublicationTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.folder = self.root / ".pixl"

    def current(self):
        return store.load(self.folder)

    def expected(self):
        return codec.digest(self.current())

    def files(self):
        return {
            path.relative_to(self.root).as_posix(): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }

    def assert_preserved(self, before):
        for name, content in before.items():
            if name != ".pixl/state.px":
                self.assertEqual((self.root / name).read_bytes(), content, name)
        self.assertFalse((self.folder / ".lock").exists())
        graph.validate(self.current(), self.root)

    def prepare(self):
        store.initialize(self.folder, sample(self.root), self.root)
        return jobs.prepare(
            self.folder,
            self.expected(),
            "job",
            "task",
            ["output"],
            "controlled-publication-fixture",
            "generate_fixture",
            {"description": "No provider request is made"},
            {"type": "object", "properties": {"description": {"type": "string"}},
             "required": ["description"], "additionalProperties": False},
            {"source": "controlled fixture schema", "observed_at": "2026-09-11T12:00:00Z",
             "evidence": {"fixture": True}},
            {"scope": "Local publication tests only", "evidence": {"fixture": True}},
            root=self.root,
        )

    def ready_import(self):
        self.prepare()
        jobs.dispatch(self.folder, self.expected(), "job", root=self.root)
        jobs.observe(self.folder, self.expected(), "job", "succeeded",
                     {"fixture": "Simulated completion"}, remote_id="fixture-id", root=self.root)
        Image.new("RGBA", (2, 2), "magenta").save(self.root / "download.png")

    def import_candidate(self, candidate="candidate", expected=None):
        return jobs.import_artifact(
            self.folder, self.expected() if expected is None else expected,
            "job", "output", candidate, "download.png",
            {"fixture": "Actual local test bytes; no remote download"}, root=self.root,
        )

    def job(self):
        return jobs.report(self.current(), self.root)["jobs"][0]

    def assert_unaccepted_import(self, candidate):
        doc = self.current()
        self.assertEqual(doc.records[candidate].fields["of"], codec.Ref("output"))
        self.assertEqual(doc.records["task"].fields["ca"], [])
        self.assertEqual(doc.records["task"].fields["vr"], [])
        self.assertEqual(doc.records["task"].fields["st"], codec.Symbol("open"))
        self.assertFalse(any(record.kind == "V" for record in doc.records.values()))

    def test_dispatch_history_without_head_never_grants_a_request(self):
        self.prepare()
        before = self.files()
        expected = self.expected()
        original_history = set((self.folder / "history").glob("*.px"))
        atomic = store._atomic
        returned_requests = []

        def interrupt(path, data):
            if Path(path) == self.folder / "state.px":
                raise OSError("controlled interruption before head replacement")
            return atomic(path, data)

        with patch("pixl.store._atomic", side_effect=interrupt), self.assertRaises(OSError):
            result = jobs.dispatch(self.folder, expected, "job", root=self.root)
            returned_requests.append(result["dispatch_request"])
        self.assertEqual(returned_requests, [])
        self.assertEqual(self.expected(), expected)
        self.assertEqual(self.job()["state"], "prepared")
        self.assertEqual(self.job()["events"], [])
        orphan_history = set((self.folder / "history").glob("*.px")) - original_history
        self.assertEqual(len(orphan_history), 1)
        orphan = codec.parse(orphan_history.pop().read_bytes())
        self.assertEqual(orphan.records["job"].fields["si"], codec.Symbol("unknown"))
        self.assert_preserved(before)

        result = jobs.dispatch(self.folder, expected, "job", root=self.root)
        self.assertIn("dispatch_request", result)
        self.assertEqual([event["event"] for event in self.job()["events"]], ["dispatch"])
        self.assert_preserved(before)

    def test_dispatch_head_without_response_cannot_be_dispatched_again(self):
        self.prepare()
        before = self.files()
        expected = self.expected()
        intent = self.job()["request"]
        atomic = store._atomic

        def lose_response(path, data):
            atomic(path, data)
            if Path(path) == self.folder / "state.px":
                raise OSError("controlled lost response after head replacement")

        with patch("pixl.store._atomic", side_effect=lose_response), self.assertRaises(OSError):
            jobs.dispatch(self.folder, expected, "job", root=self.root)
        cold = self.job()
        self.assertEqual(cold["state"], "unknown")
        self.assertEqual(cold["request"], intent)
        self.assertEqual(cold["next_action"], "reconcile")
        self.assertNotIn("dispatch_request", cold)
        self.assertEqual(cold["remote_id"], None)
        self.assert_preserved(before)
        committed = self.files()
        with self.assertRaisesRegex(codec.PixlError, "stale_write"):
            jobs.dispatch(self.folder, expected, "job", root=self.root)
        with self.assertRaises(codec.PixlError):
            jobs.dispatch(self.folder, self.expected(), "job", root=self.root)
        self.assertEqual(self.files(), committed)
        self.assertEqual([event["event"] for event in self.job()["events"]], ["dispatch"])

    def test_import_history_without_head_recovers_once_without_acceptance(self):
        self.ready_import()
        before = self.files()
        expected = self.expected()
        prefix = self.job()["events"]
        atomic = store._atomic

        def interrupt(path, data):
            if Path(path) == self.folder / "state.px":
                raise OSError("controlled import interruption before head replacement")
            return atomic(path, data)

        with patch("pixl.store._atomic", side_effect=interrupt), self.assertRaises(OSError):
            self.import_candidate()
        self.assertEqual(self.expected(), expected)
        self.assertNotIn("candidate", self.current().records)
        self.assertEqual(self.job()["events"], prefix)
        self.assertEqual(self.job()["candidates"], [])
        self.assert_preserved(before)

        self.import_candidate(expected=expected)
        events = self.job()["events"]
        self.assertEqual(events[:-1], prefix)
        self.assertEqual(events[-1]["artifact"]["id"], "candidate")
        self.assertEqual(sum(event["event"] == "imported" for event in events), 1)
        self.assert_unaccepted_import("candidate")
        self.assert_preserved(before)

    def test_import_head_without_response_reuses_exact_import_after_cold_read(self):
        self.ready_import()
        before = self.files()
        expected = self.expected()
        atomic = store._atomic

        def lose_response(path, data):
            atomic(path, data)
            if Path(path) == self.folder / "state.px":
                raise OSError("controlled lost import response after head replacement")

        with patch("pixl.store._atomic", side_effect=lose_response), self.assertRaises(OSError):
            self.import_candidate(expected=expected)
        self.assert_unaccepted_import("candidate")
        cold = self.job()
        self.assertEqual(cold["remote_id"], "fixture-id")
        self.assertEqual([item["id"] for item in cold["candidates"]], ["candidate"])
        self.assert_preserved(before)
        committed = self.files()
        current_hash = self.expected()
        with self.assertRaisesRegex(codec.PixlError, "stale_write"):
            self.import_candidate(expected=expected)
        repeated = self.import_candidate(expected=current_hash)
        self.assertTrue(repeated["reused_import"])
        self.assertEqual(repeated["hash"], current_hash)
        self.assertEqual(self.files(), committed)
        self.assertEqual(sum(e["event"] == "imported" for e in self.job()["events"]), 1)

    def race(self, operation, values):
        barrier = Barrier(2)

        def compete(value):
            barrier.wait(timeout=5)
            try:
                return {"value": value, "result": operation(value)}
            except codec.PixlError as error:
                return {"value": value, "error": error.code, "detail": error.detail}

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(compete, values))
        winners = [result for result in results if "result" in result]
        failures = [result for result in results if "error" in result]
        self.assertEqual(len(winners), 1, results)
        self.assertEqual(len(failures), 1, results)
        return winners[0], failures[0]

    def test_competing_observations_publish_one_prefix_and_preserve_identity(self):
        self.prepare()
        jobs.dispatch(self.folder, self.expected(), "job", root=self.root)
        jobs.observe(self.folder, self.expected(), "job", "submitted", {"fixture": True},
                     remote_id="fixture-id", root=self.root)
        before = self.files()
        prefix = self.job()["events"]
        expected = self.expected()
        winner, loser = self.race(
            lambda event: jobs.observe(self.folder, expected, "job", event,
                                       {"fixture": event}, remote_id="fixture-id", root=self.root),
            ("running", "succeeded"),
        )
        cold = self.job()
        self.assertEqual(cold["state"], winner["value"])
        self.assertEqual(cold["remote_id"], "fixture-id")
        self.assertEqual(cold["events"][:-1], prefix)
        self.assertEqual(cold["events"][-1]["event"], winner["value"])
        self.assert_preserved(before)
        self.assertIn(loser["error"], {"store_locked", "stale_write"}, loser)

    def test_competing_imports_publish_one_candidate_without_acceptance(self):
        self.ready_import()
        before = self.files()
        prefix = self.job()["events"]
        expected = self.expected()
        winner, loser = self.race(
            lambda candidate: self.import_candidate(candidate, expected),
            ("candidate.a", "candidate.b"),
        )
        cold = self.job()
        self.assertEqual(cold["events"][:-1], prefix)
        self.assertEqual([item["id"] for item in cold["candidates"]], [winner["value"]])
        self.assertNotIn(loser["value"], self.current().records)
        self.assert_unaccepted_import(winner["value"])
        self.assert_preserved(before)
        self.assertIn(loser["error"], {"store_locked", "stale_write"}, loser)

    def review_project(self):
        doc = sample(self.root)
        add_candidate(doc, self.root, "candidate.a")
        add_candidate(doc, self.root, "candidate.b")
        doc.records["task"].fields["ca"] = []
        store.initialize(self.folder, doc, self.root)
        self.observation = self.root / "observations.txt"
        self.observation.write_text("Synthetic publication checks, not actual artistic or engine acceptance.\n",
                                    encoding="utf-8")

    def review_request(self, candidate, action):
        context = review.context(self.current(), self.root, candidate)
        modes = ("local", "visual", "live")
        return {
            "version": 1, "binding_hash": context["binding_hash"], "reviewer": "actor",
            "observed_at": datetime.now(UTC).isoformat(),
            "observations": [{"path": self.observation.name,
                              "sha256": hashlib.sha256(self.observation.read_bytes()).hexdigest(),
                              "mode": mode, "note": "Synthetic " + mode} for mode in modes],
            "verdicts": [{"criterion": row["id"], "status": "pass", "reason": "Synthetic judgment",
                          "supersedes": row["verdict"], "observations": [modes.index(row["mode"])]}
                         for row in context["criteria"]],
            "action": action, "next_action": "Read current result", "limitations": ["Controlled fixture"],
        }

    def test_competing_reviews_nominate_only_the_winners_candidate(self):
        self.review_project()
        before = self.files()
        expected = self.expected()
        requests = {candidate: self.review_request(candidate, "nominate")
                    for candidate in ("candidate.a", "candidate.b")}
        winner, loser = self.race(
            lambda candidate: review.submit(self.folder, expected, candidate, "review." + candidate,
                                             requests[candidate], self.root),
            ("candidate.a", "candidate.b"),
        )
        doc = self.current()
        self.assertEqual(doc.records["task"].fields["ca"], [codec.Ref(winner["value"])])
        self.assertEqual(doc.records["task"].fields["st"], codec.Symbol("open"))
        verdicts = [record for record in doc.records.values() if record.kind == "V"]
        self.assertEqual(len(verdicts), 3)
        self.assertTrue(all(record.id.startswith("review." + winner["value"] + ".") for record in verdicts))
        self.assertFalse(any(key.startswith("review." + loser["value"]) for key in doc.records))
        self.assert_preserved(before)
        self.assertIn(loser["error"], {"store_locked", "stale_write"}, loser)

    def test_review_head_without_response_reuses_verdicts_and_finishes_completion(self):
        self.review_project()
        before = self.files()
        request = self.review_request("candidate.a", "complete")
        atomic = store._atomic

        def lose_response(path, data):
            atomic(path, data)
            if Path(path) == self.folder / "state.px":
                raise OSError("controlled lost review response after head replacement")

        with patch("pixl.store._atomic", side_effect=lose_response), self.assertRaises(OSError):
            review.submit(self.folder, self.expected(), "candidate.a", "review", request, self.root)
        cold = self.current()
        verdicts = {key: record for key, record in cold.records.items() if record.kind == "V"}
        self.assertEqual(len(verdicts), 3)
        self.assertEqual(cold.records["task"].fields["st"], codec.Symbol("open"))
        self.assertEqual(cold.records["task"].fields["ca"], [])
        self.assert_preserved(before)
        retained = self.files()
        result = review.submit(self.folder, self.expected(), "candidate.a", "review", request, self.root)
        self.assertTrue(result["reused_review"])
        self.assertTrue(result["current_acceptance"]["task_complete"])
        self.assertEqual(len(result["publications"]), 2)
        final = self.current()
        self.assertEqual({key: record for key, record in final.records.items() if record.kind == "V"}, verdicts)
        self.assertEqual(final.records["task"].fields["ca"], [codec.Ref("candidate.a")])
        self.assertEqual([r for r in final.records.values() if r.kind == "J"], [])
        self.assert_preserved(retained)


if __name__ == "__main__":
    unittest.main()
