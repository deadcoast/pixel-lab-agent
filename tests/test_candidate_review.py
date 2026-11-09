"""Explicit synthetic reviews test retention/recovery, not artistic quality."""

import copy
import hashlib
import json
import subprocess
import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import candidate_review as review
from pixl import codec, delivery, graph, mcp, service, store
from pixl.codec import PixlError, Record, Ref, Symbol
from tests.family_support import family
from tests.lifecycle_support import add_candidate, sample


class CandidateReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / ".pixl"

    def project(self):
        doc = sample(self.root)
        add_candidate(doc, self.root, "candidate")
        doc.records["task"].fields["ca"] = []
        store.initialize(self.folder, doc, self.root)

    def expected(self):
        return codec.digest(store.load(self.folder))

    def request(self, candidate="candidate", action="complete"):
        ctx = review.context(store.load(self.folder), self.root, candidate)
        path = self.root / "observation.txt"
        path.write_text("Synthetic retained observations, not an actual visual/engine outcome.", encoding="utf-8")
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        return {"version": 1, "binding_hash": ctx["binding_hash"], "reviewer": "actor",
                "observed_at": datetime.now(UTC).isoformat(),
                "observations": [{"path": path.name, "sha256": sha, "mode": m, "note": "Synthetic " + m} for m in ("local", "visual", "live")],
                "verdicts": [{"criterion": q["id"], "status": "pass", "reason": "Synthetic fixture judgment",
                              "supersedes": q["verdict"], "observations": [("local", "visual", "live").index(q["mode"])]}
                             for q in ctx["criteria"]],
                "action": action, "next_action": "Read current result", "limitations": ["Synthetic test"]}

    def submit(self, value, candidate="candidate", ident="review"):
        return review.submit(self.folder, self.expected(), candidate, ident, value, self.root)

    def test_candidate_review_nomination_completion_and_idempotent_retry(self):
        self.project()
        before = store.load(self.folder)
        request = self.request()
        result = self.submit(request)
        self.assertTrue(result["current_acceptance"]["task_complete"])
        self.assertTrue(result["nominated"])
        self.assertEqual(len(result["publications"]), 3)
        after = store.load(self.folder)
        for key, value in before.records.items():
            if key != "task":
                self.assertEqual(value, after.records[key])
        self.assertEqual(len([r for r in after.records.values() if r.kind == "V"]), 3)
        repeat = self.submit(request)
        self.assertTrue(repeat["reused_review"])
        self.assertEqual(repeat["state_hash"], result["state_hash"])
        self.assertEqual(repeat["publications"], [])

    def test_failed_and_unavailable_reviews_remain_honest_and_cannot_complete(self):
        self.project()
        request = self.request(action="record")
        request["verdicts"][1]["status"] = "fail"
        request["verdicts"][2].update(status="unavailable", observations=[])
        bad = copy.deepcopy(request)
        bad["action"] = "complete"
        before = self.expected()
        with self.assertRaisesRegex(PixlError, "completion"):
            self.submit(bad)
        self.assertEqual(self.expected(), before)
        result = self.submit(request)
        self.assertEqual([q["status"] for q in result["criteria"]], ["pass", "fail", "unavailable"])
        self.assertFalse(result["nominated"])
        doc = store.load(self.folder)
        self.assertNotIn("review.evidence.2", doc.records)
        revised = self.request()
        result = self.submit(revised, ident="revised")
        self.assertTrue(result["current_acceptance"]["task_complete"])
        for i in range(3):
            self.assertTrue(store.load(self.folder).records[f"review.verdict.{i}"].fields["ob"])

    def test_partial_review_and_nomination_preserves_other_requirements(self):
        self.project()
        request = self.request(action="nominate")
        request["verdicts"] = request["verdicts"][:1]
        result = self.submit(request)
        self.assertTrue(result["nominated"])
        self.assertEqual(result["task_status"], "open")
        self.assertEqual([q["status"] for q in result["criteria"]], ["pass", "unperformed", "unperformed"])

    def test_interruption_after_review_or_activation_recovers_without_duplicate_verdicts(self):
        self.project()
        request = self.request()
        publish = store._publish
        calls = []

        def interrupt(folder, doc):
            calls.append(doc.revision)
            if len(calls) == 2:
                raise OSError("injected publication interruption")
            return publish(folder, doc)

        with patch("pixl.store._publish", side_effect=interrupt), self.assertRaises(OSError):
            self.submit(request)
        self.assertEqual(store.load(self.folder).records["task"].fields["st"], Symbol("open"))
        saved = self.expected()
        changed = copy.deepcopy(request)
        changed["verdicts"][0]["reason"] = "Changed review"
        with self.assertRaisesRegex(PixlError, "different request"):
            self.submit(changed)
        self.assertEqual(self.expected(), saved)
        calls.clear()
        with patch("pixl.store._publish", side_effect=interrupt), self.assertRaises(OSError):
            self.submit(request)
        self.assertEqual(store.load(self.folder).records["task"].fields["st"], Symbol("active"))
        result = self.submit(request)
        self.assertTrue(result["reused_review"])
        self.assertTrue(result["current_acceptance"]["task_complete"])
        self.assertEqual(len([r for r in store.load(self.folder).records.values() if r.kind == "V"]), 3)

    def test_stale_state_and_semantic_binding_rejected(self):
        self.project()
        request = self.request()
        with self.assertRaisesRegex(PixlError, "stale_write"):
            review.submit(self.folder, "0" * 64, "candidate", "review", request, self.root)
        current = store.load(self.folder)
        changed = copy.deepcopy(current)
        changed.records["q.visual"].fields["ck"] = "Changed literal requirement"
        changed.revision += 1
        store.commit(self.folder, changed, self.expected(), self.root)
        with self.assertRaisesRegex(PixlError, "review_binding"):
            self.submit(request)
        self.assertNotIn("review", store.load(self.folder).records)

    def test_observation_hash_mode_timestamp_and_supersession_validation(self):
        self.project()
        original = self.request()
        mutations = [lambda x: x["observations"][0].update(sha256="0" * 64),
                     lambda x: x["observations"][0].update(path="../outside"),
                     lambda x: x["observations"][1].update(mode="local"),
                     lambda x: x.update(observed_at="2999-01-01T00:00:00+00:00"),
                     lambda x: x.update(observed_at="2026-01-01"),
                     lambda x: x["verdicts"][0].update(supersedes="invented"),
                     lambda x: x["verdicts"][0].update(observations=[True]),
                     lambda x: x["verdicts"][0].update(criterion="other"),
                     lambda x: x.update(extra="undeclared")]
        before = self.expected()
        for mutate in mutations:
            value = copy.deepcopy(original)
            mutate(value)
            with self.subTest(value=value), self.assertRaises(PixlError):
                self.submit(value)
            self.assertEqual(self.expected(), before)

    def test_superseded_review_cannot_be_replayed(self):
        self.project()
        original = self.request(action="record")
        self.submit(original)
        self.submit(self.request(action="record"), ident="successor")
        with self.assertRaisesRegex(PixlError, "review_superseded"):
            self.submit(original)

    def test_pending_provider_blocks_completion_without_publishing_review(self):
        self.project()
        doc = store.load(self.folder)
        doc.revision += 1
        doc.records["pending"] = Record("pending", "J", {"tk": Ref("task"), "tl": "fixture", "ah": "0" * 64,
                                                          "si": Symbol("unknown"), "ri": "", "ev": []})
        store.commit(self.folder, doc, self.expected(), self.root)
        before = self.expected()
        with self.assertRaisesRegex(PixlError, "pending_jobs"):
            self.submit(self.request())
        self.assertEqual(self.expected(), before)

    def test_retained_files_survive_origin_change_and_detect_retained_tampering(self):
        self.project()
        result = self.submit(self.request(action="record"))
        (self.root / "observation.txt").write_text("changed source report")
        doc = store.load(self.folder)
        graph.validate(doc, self.root)
        self.assertFalse(result["automatic_artistic_judgment"])
        retained = self.root / doc.records["review.file.0"].fields["ur"]
        retained.write_text("tampered retained bytes")
        with self.assertRaises(PixlError):
            review.context(doc, self.root, "candidate")

    def test_family_current_acceptance_separate_from_immutable_creation(self):
        family(self.root, self.folder)
        delivery.snapshot(self.folder, self.expected(), "delivery.output", "package", self.root)
        doc = store.load(self.folder)
        manifest = self.root / doc.records["package"].fields["ur"]
        original = manifest.read_bytes()
        result = self.submit(self.request("package"), "package")
        self.assertFalse(result["snapshot_acceptance"]["accepted"])
        self.assertTrue(result["current_acceptance"]["task_complete"])
        self.assertTrue(result["current_acceptance"]["all_required_pass"])
        self.assertEqual(manifest.read_bytes(), original)
        self.assertTrue(result["members"])

    def test_cli_service_mcp_share_contract_and_results(self):
        self.project()
        request = self.request(action="nominate")
        request_path = self.root / "review.json"
        request_path.write_text(json.dumps(request), encoding="utf-8")
        result = subprocess.run([sys.executable, "-m", "pixl", "candidate-review", str(self.folder), "candidate", "review",
                                 str(request_path), "--expect", self.expected(), "--root", str(self.root)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        cli = json.loads(result.stdout)
        direct = service.call("pixl_review_context", {"path": ".pixl/state.px", "candidate_id": "candidate"}, self.root)
        self.assertEqual(cli["state_hash"], direct["state_hash"])
        response = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "pixl_candidate_review", "arguments": {
            "store": ".pixl", "expect": self.expected(), "candidate_id": "candidate", "review_id": "review", "observation": request}}}, self.root)
        self.assertFalse(response["result"].get("isError"), response)
        repeated = response["result"]["structuredContent"]
        self.assertTrue(repeated["reused_review"])
        self.assertEqual(repeated["state_hash"], cli["state_hash"])


if __name__ == "__main__":
    unittest.main()
