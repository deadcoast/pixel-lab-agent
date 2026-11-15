"""Accepted-candidate completion preserves review and lifecycle requirements."""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, completion, graph, mcp, store
from pixl.codec import PixlError, Record, Ref, Symbol
from tests.lifecycle_support import add_candidate, add_verdict, sample


class CompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / ".pixl"

    def project(
        self, statuses=("pass", "pass", "pass"), pending=False, two_outputs=False
    ):
        doc = sample(self.root)
        add_candidate(doc, self.root, "candidate")
        if two_outputs:
            second = copy.deepcopy(doc.records["output"])
            second.id = "output2"
            doc.records[second.id] = second
            doc.records["task"].fields["op"].append(Ref(second.id))
            add_candidate(doc, self.root, "candidate2")
            doc.records["candidate2"].fields["of"] = Ref(second.id)
        doc.records["task"].fields["ca"] = []
        if pending:
            doc.records["job"] = Record(
                "job",
                "J",
                {
                    "tk": Ref("task"),
                    "tl": "fixture",
                    "ah": "0" * 64,
                    "si": Symbol("unknown"),
                    "ri": "",
                    "ev": [],
                },
            )
        store.initialize(self.folder, doc, self.root)
        reviewed = copy.deepcopy(doc)
        reviewed.revision += 1
        for candidate in ["candidate", "candidate2"] if two_outputs else ["candidate"]:
            for index, status in enumerate(statuses):
                if status is not None:
                    add_verdict(
                        reviewed,
                        self.root,
                        candidate,
                        ["q.mechanical", "q.visual", "q.engine"][index],
                        status,
                        candidate + ".verdict" + str(index),
                    )
        store.commit(self.folder, reviewed, codec.digest(doc), self.root)
        return reviewed

    def test_completes_and_repeats_without_new_acceptance_or_history(self):
        before = self.project()
        result = completion.complete(
            self.folder, codec.digest(before), "task", ["candidate"], self.root
        )
        after = store.load(self.folder)
        self.assertEqual(after.records["task"].fields["st"], Symbol("done"))
        self.assertEqual(after.records["task"].fields["ca"], [Ref("candidate")])
        self.assertEqual(len(result["publications"]), 2)
        self.assertFalse(result["acceptance_created"])
        self.assertFalse(result["remote_executed"])
        for id_, record in before.records.items():
            if id_ != "task":
                self.assertEqual(record, after.records[id_])
        repeated = completion.complete(
            self.folder, result["hash"], "task", ["candidate"], self.root
        )
        self.assertTrue(repeated["already_complete"])
        self.assertEqual(repeated["hash"], result["hash"])
        self.assertEqual(repeated["publications"], [])

    def test_missing_failed_or_unavailable_requirement_cannot_complete(self):
        for status in (None, "fail", "unavailable"):
            with self.subTest(status=status), TemporaryDirectory() as temp:
                self.root = Path(temp)
                self.folder = self.root / ".pixl"
                before = self.project(("pass", status, "pass"))
                with self.assertRaisesRegex(PixlError, "completion"):
                    completion.complete(
                        self.folder,
                        codec.digest(before),
                        "task",
                        ["candidate"],
                        self.root,
                    )
                self.assertEqual(
                    codec.digest(store.load(self.folder)), codec.digest(before)
                )

    def test_stale_hash_and_pending_job_cannot_change_state(self):
        before = self.project(pending=True)
        for expected, message in (
            ("0" * 64, "stale_write"),
            (codec.digest(before), "pending_jobs"),
        ):
            with self.assertRaisesRegex(PixlError, message):
                completion.complete(
                    self.folder, expected, "task", ["candidate"], self.root
                )
        self.assertEqual(codec.digest(store.load(self.folder)), codec.digest(before))

    def test_all_outputs_required_and_wrong_or_duplicate_candidates_rejected(self):
        before = self.project(two_outputs=True)
        for candidates in (
            ["candidate"],
            ["candidate", "candidate"],
            ["missing", "candidate2"],
        ):
            with self.subTest(candidates=candidates), self.assertRaises(PixlError):
                completion.complete(
                    self.folder, codec.digest(before), "task", candidates, self.root
                )
            self.assertEqual(
                codec.digest(store.load(self.folder)), codec.digest(before)
            )
        completion.complete(
            self.folder,
            codec.digest(before),
            "task",
            ["candidate2", "candidate"],
            self.root,
        )
        graph.validate(store.load(self.folder), self.root)

    def test_file_drift_does_not_complete(self):
        before = self.project()
        (self.root / "candidate.png").write_bytes(b"changed")
        with self.assertRaises(PixlError):
            completion.complete(
                self.folder, codec.digest(before), "task", ["candidate"], self.root
            )
        self.assertEqual(codec.digest(store.load(self.folder)), codec.digest(before))

    def test_interrupted_publication_resumes_from_valid_active_state(self):
        before = self.project()
        publish = store._publish
        calls = 0

        def stop_after_activation(folder, doc):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated interruption")
            return publish(folder, doc)

        with (
            patch.object(store, "_publish", stop_after_activation),
            self.assertRaises(OSError),
        ):
            completion.complete(
                self.folder, codec.digest(before), "task", ["candidate"], self.root
            )
        active = store.load(self.folder)
        graph.validate(active, self.root)
        self.assertEqual(active.records["task"].fields["st"], Symbol("active"))
        result = completion.complete(
            self.folder, codec.digest(active), "task", ["candidate"], self.root
        )
        self.assertEqual(len(result["publications"]), 1)
        self.assertEqual(
            store.load(self.folder).records["task"].fields["st"], Symbol("done")
        )

    def test_cli_and_mcp_share_completion_contract(self):
        before = self.project()
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "pixl",
                "task-complete",
                str(self.folder),
                "task",
                "candidate",
                "--expect",
                codec.digest(before),
                "--root",
                str(self.root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        published = json.loads(result.stdout)
        response = mcp.dispatch(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "pixl_task_complete",
                    "arguments": {
                        "store": ".pixl",
                        "expect": published["hash"],
                        "task_id": "task",
                        "candidates": ["candidate"],
                    },
                },
            },
            self.root,
        )["result"]
        self.assertFalse(response["isError"], response)
        self.assertTrue(response["structuredContent"]["already_complete"])
        tools = mcp.dispatch(
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, self.root
        )["result"]["tools"]
        declared = next(t for t in tools if t["name"] == "pixl_task_complete")
        self.assertFalse(declared["annotations"]["readOnlyHint"])
