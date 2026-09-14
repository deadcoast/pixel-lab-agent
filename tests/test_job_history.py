"""Pure durable history checks with fictional caller-supplied observations."""

import copy
import hashlib
import json
import unittest
from unittest.mock import patch

from pixl.codec import PixlError

try:
    from pixl import job_history
except ImportError:
    job_history = None


def digest(value):
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    ).hexdigest()


def request():
    schema = {"type": "object", "properties": {"prompt": {"type": "string"}}}
    identity = {
        "provider": "fixture",
        "tool": "render",
        "arguments": {"prompt": "A fictional sample"},
        "schema": schema,
    }
    return {
        "version": 1,
        **identity,
        "schema_sha256": digest(schema),
        "request_sha256": digest(identity),
        "discovery": {
            "source": "fictional test harness",
            "observed_at": "2026-09-11T10:00:00+00:00",
            "evidence": {"fixture": "discovery"},
        },
        "authorization": {
            "scope": "one fictional sample",
            "evidence": {"fixture": True},
        },
        "prepared_at": "2026-09-11T10:00:00+00:00",
        "policy": "caller_schema",
        "remote_executed": False,
        "cached_assessment": {
            "advisory": True,
            "source": None,
            "retrieved_at": None,
            "status": "not_applicable",
            "findings": [],
        },
    }


def context():
    return {
        "task": "sample",
        "outputs": ["sprite", "preview"],
        "task_sha256": "a" * 64,
        "bindings": {"sprite": "b" * 64, "preview": "c" * 64, "contract": "d" * 64},
    }


def artifact(candidate="candidate1", output="sprite"):
    return {"id": candidate, "output": output, "record_sha256": "e" * 64}


class JobHistoryTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(job_history, "durable history reducer is not implemented")

    def prepared(self):
        return job_history.new("job1", request(), context())

    def dispatched(self):
        return job_history.append(
            self.prepared(), "dispatch", {"fixture": "local claim"}
        )

    def succeeded(self):
        return job_history.append(
            self.dispatched(), "succeeded", {"fixture": "success"}, "remote-fixture"
        )

    def test_replay_rejects_backward_instants_including_before_preparation(self):
        journal = self.succeeded()
        for index in (0, 1):
            changed = copy.deepcopy(journal)
            changed["events"][index]["recorded_at"] = "2020-01-01T00:00:00+00:00"
            with (
                self.subTest(index=index),
                self.assertRaisesRegex(PixlError, "job_history"),
            ):
                job_history.validate(changed)
        journal["events"][0]["recorded_at"] = "2026-09-11T12:00:00+00:00"
        journal["events"][1]["recorded_at"] = "2026-09-11T13:00:00+02:00"
        with self.assertRaisesRegex(PixlError, "job_history"):
            job_history.validate(journal)
        journal["events"][1]["recorded_at"] = "2026-09-11T13:00:00+01:00"
        self.assertEqual(job_history.validate(journal)["state"], "succeeded")

    def test_timestamp_precision_cannot_hide_backwards_time(self):
        journal = self.succeeded()
        journal["events"][0]["recorded_at"] = "2026-09-11T12:00:00.1234569Z"
        journal["events"][1]["recorded_at"] = "2026-09-11T12:00:00.1234561Z"
        with self.assertRaisesRegex(PixlError, "job_history"):
            job_history.validate(journal)

    def test_new_binds_complete_intent_and_detaches_inputs(self):
        supplied_request, supplied_context = request(), context()
        journal = job_history.new("job1", supplied_request, supplied_context)
        self.assertEqual(journal["state"], "prepared")
        self.assertIsNone(journal["remote_id"])
        self.assertEqual(journal["events"], [])
        self.assertEqual(journal["intent"]["job"], "job1")
        self.assertEqual(journal["intent_sha256"], digest(journal["intent"]))
        supplied_request["arguments"]["prompt"] = "changed"
        supplied_context["outputs"].append("unplanned")
        self.assertEqual(
            journal["intent"]["request"]["arguments"]["prompt"], "A fictional sample"
        )
        self.assertEqual(journal["intent"]["context"]["outputs"], ["sprite", "preview"])

    def test_identity_covers_request_and_context_and_job(self):
        first = self.prepared()
        changed_context = context()
        changed_context["bindings"]["contract"] = "e" * 64
        self.assertNotEqual(
            first["intent_sha256"],
            job_history.new("job1", request(), changed_context)["intent_sha256"],
        )
        self.assertNotEqual(
            first["intent_sha256"],
            job_history.new("job2", request(), context())["intent_sha256"],
        )

    def test_dispatch_is_a_single_durable_unknown_claim(self):
        initial = self.prepared()
        claimed = job_history.append(initial, "dispatch", {"fixture": "claim"})
        self.assertEqual(initial["events"], [])
        self.assertEqual(claimed["state"], "unknown")
        self.assertIsNone(claimed["remote_id"])
        self.assertEqual(claimed["events"][0]["sequence"], 1)
        self.assertEqual(claimed["events"][0]["event"], "dispatch")
        self.assertIsNone(claimed["events"][0]["artifact"])
        with self.assertRaises(PixlError):
            job_history.append(claimed, "dispatch", {"fixture": "duplicate"})
        with self.assertRaises(PixlError):
            job_history.append(initial, "dispatch", {"fixture": "claim"}, "invented")

    def test_only_abandonment_is_allowed_before_dispatch(self):
        for event in ("submitted", "running", "succeeded", "unknown", "imported"):
            with self.subTest(event=event), self.assertRaises(PixlError):
                job_history.append(
                    self.prepared(), event, {"fixture": True}, "remote-fixture"
                )
        abandoned = job_history.append(
            self.prepared(), "failed", {"fixture": "abandoned"}
        )
        self.assertEqual(abandoned["state"], "failed")
        self.assertIsNone(abandoned["remote_id"])
        with self.assertRaises(PixlError):
            job_history.append(
                self.prepared(), "failed", {"fixture": "abandoned"}, "invented"
            )

    def test_lost_response_and_cold_replay_retain_recovered_identity(self):
        history = self.dispatched()
        history = job_history.append(history, "unknown", {"fixture": "response lost"})
        cold = job_history.validate(json.loads(json.dumps(history)))
        history = job_history.append(
            cold, "submitted", {"fixture": "reconciled"}, "remote-fixture"
        )
        history = job_history.append(history, "running", {"fixture": "poll"})
        history = job_history.append(
            history, "unknown", {"fixture": "poll unavailable"}
        )
        self.assertEqual(history["state"], "unknown")
        self.assertEqual(history["remote_id"], "remote-fixture")
        self.assertEqual(len(history["events"]), 5)
        self.assertEqual(job_history.validate(history), history)

    def test_repeated_nonterminal_observations_are_retained(self):
        history = self.dispatched()
        for event in (
            "unknown",
            "unknown",
            "submitted",
            "submitted",
            "running",
            "running",
        ):
            history = job_history.append(
                history, event, {"fixture": event}, "remote-fixture"
            )
        self.assertEqual(history["state"], "running")
        self.assertEqual(len(history["events"]), 7)

    def test_running_cannot_regress_to_submitted_even_through_unknown(self):
        running = job_history.append(
            self.dispatched(), "running", {"fixture": True}, "remote-fixture"
        )
        for history in (
            running,
            job_history.append(running, "unknown", {"fixture": True}),
        ):
            with self.subTest(state=history["state"]), self.assertRaises(PixlError):
                job_history.append(history, "submitted", {"fixture": True})

    def test_accepted_states_require_remote_identity(self):
        for event in ("submitted", "running", "succeeded"):
            with self.subTest(event=event), self.assertRaises(PixlError):
                job_history.append(self.dispatched(), event, {"fixture": True})

    def test_identity_once_known_cannot_be_changed_or_erased(self):
        history = job_history.append(
            self.dispatched(), "submitted", {"fixture": True}, "remote-fixture"
        )
        for event in ("submitted", "running", "unknown", "failed", "succeeded"):
            with self.subTest(event=event), self.assertRaises(PixlError):
                job_history.append(history, event, {"fixture": True}, "different")
        replay = job_history.append(history, "unknown", {"fixture": True})
        replay["events"][-1]["remote_id"] = None
        replay["remote_id"] = None
        with self.assertRaises(PixlError):
            job_history.validate(replay)

    def test_failure_is_terminal_and_success_only_allows_import(self):
        terminal = [
            self.succeeded(),
            job_history.append(self.dispatched(), "failed", {"fixture": True}),
        ]
        for history in terminal:
            for event in (
                "dispatch",
                "submitted",
                "running",
                "unknown",
                "succeeded",
                "failed",
            ):
                with (
                    self.subTest(state=history["state"], event=event),
                    self.assertRaises(PixlError),
                ):
                    job_history.append(history, event, {"fixture": True})
        with self.assertRaises(PixlError):
            job_history.append(
                terminal[1], "imported", {"fixture": True}, artifact=artifact()
            )

    def test_imports_bind_unique_candidates_to_saved_outputs_without_acceptance(self):
        history = self.succeeded()
        for candidate, output in (
            ("first", "sprite"),
            ("second", "sprite"),
            ("third", "preview"),
        ):
            history = job_history.append(
                history,
                "imported",
                {"fixture": "local file"},
                artifact=artifact(candidate, output),
            )
        self.assertEqual(history["state"], "succeeded")
        self.assertEqual(history["remote_id"], "remote-fixture")
        self.assertEqual(
            [row["artifact"]["id"] for row in history["events"][2:]],
            ["first", "second", "third"],
        )
        self.assertNotIn("verdict", history)
        for output in ("sprite", "preview"):
            with self.subTest(output=output), self.assertRaises(PixlError):
                job_history.append(
                    history,
                    "imported",
                    {"fixture": True},
                    artifact=artifact("first", output),
                )

    def test_import_cannot_claim_unplanned_output_or_incomplete_artifact(self):
        invalid = [
            None,
            {},
            artifact(output="other"),
            {**artifact(), "path": "file.png"},
            {**artifact(), "record_sha256": "bad"},
            {**artifact(), "id": "bad id"},
        ]
        for supplied in invalid:
            with self.subTest(artifact=supplied), self.assertRaises(PixlError):
                job_history.append(
                    self.succeeded(), "imported", {"fixture": True}, artifact=supplied
                )
        with self.assertRaises(PixlError):
            job_history.append(
                self.dispatched(),
                "running",
                {"fixture": True},
                "remote-fixture",
                artifact(),
            )

    def test_every_event_requires_nonempty_credential_free_evidence(self):
        for evidence in (
            None,
            {},
            [],
            "observed",
            {"headers": {"Authorization": "DO_NOT_ECHO"}},
            {"nested": [{"api_key": "DO_NOT_ECHO"}]},
        ):
            for history, event in (
                (self.prepared(), "dispatch"),
                (self.dispatched(), "unknown"),
                (self.prepared(), "failed"),
                (self.succeeded(), "imported"),
            ):
                with self.subTest(event=event, evidence=evidence):
                    with self.assertRaises(PixlError) as caught:
                        job_history.append(
                            history,
                            event,
                            evidence,
                            artifact=artifact() if event == "imported" else None,
                        )
                    self.assertNotIn("DO_NOT_ECHO", str(caught.exception))

    def test_non_json_nonfinite_and_excessively_nested_evidence_is_rejected(self):
        nested = {"leaf": True}
        for _ in range(65):
            nested = {"nested": nested}
        for value in (float("nan"), float("inf"), (1, 2), {1: "bad"}, nested):
            with self.subTest(type=type(value).__name__), self.assertRaises(PixlError):
                job_history.append(self.dispatched(), "unknown", {"value": value})

    def test_validation_returns_detached_history_and_append_does_not_alias_evidence(
        self,
    ):
        evidence = {"fixture": ["observed"]}
        history = job_history.append(self.dispatched(), "unknown", evidence)
        evidence["fixture"].append("later")
        validated = job_history.validate(history)
        validated["events"][-1]["evidence"]["fixture"].append("changed")
        self.assertEqual(history["events"][-1]["evidence"], {"fixture": ["observed"]})

    def test_replay_rejects_hash_and_derived_state_tampering(self):
        baseline = self.succeeded()
        for field, value in (
            ("intent_sha256", "f" * 64),
            ("state", "prepared"),
            ("remote_id", "other"),
        ):
            tampered = copy.deepcopy(baseline)
            tampered[field] = value
            with self.subTest(field=field), self.assertRaises(PixlError):
                job_history.validate(tampered)
        tampered = copy.deepcopy(baseline)
        tampered["intent"]["context"]["bindings"]["contract"] = "f" * 64
        with self.assertRaises(PixlError):
            job_history.validate(tampered)

    def test_replay_validates_retained_request_even_when_intent_hash_is_recomputed(
        self,
    ):
        tampered = self.prepared()
        tampered["intent"]["request"]["arguments"]["prompt"] = "changed"
        tampered["intent_sha256"] = digest(tampered["intent"])
        with self.assertRaises(PixlError):
            job_history.validate(tampered)

    def test_replay_requires_exact_closed_shapes(self):
        for location in ((), ("intent",), ("intent", "context"), ("events", 0)):
            for operation in ("add", "remove"):
                tampered = self.dispatched()
                node = tampered
                for key in location:
                    node = node[key]
                if operation == "add":
                    node["extra"] = True
                else:
                    del node[next(iter(node))]
                with (
                    self.subTest(location=location, operation=operation),
                    self.assertRaises(PixlError),
                ):
                    job_history.validate(tampered)

    def test_replay_checks_sequences_timestamps_evidence_and_event_names(self):
        invalid = [
            ("sequence", True),
            ("sequence", 0),
            ("sequence", 2),
            ("sequence", "1"),
            ("recorded_at", "bad"),
            ("recorded_at", "2026-09-11"),
            ("recorded_at", 1),
            ("evidence", {}),
            ("evidence", {"token": "DO_NOT_ECHO"}),
            ("event", "succeeded"),
            ("event", "invented"),
            ("event", []),
            ("remote_id", ""),
            ("remote_id", True),
            ("artifact", artifact()),
        ]
        for field, value in invalid:
            tampered = self.dispatched()
            tampered["events"][0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(PixlError):
                job_history.validate(tampered)

    def test_context_requires_valid_ids_hashes_and_bound_unique_outputs(self):
        invalid = [
            ("task", "bad id"),
            ("task", 1),
            ("outputs", []),
            ("outputs", ["sprite", "sprite"]),
            ("outputs", "sprite"),
            ("outputs", ["unbound"]),
            ("outputs", [1]),
            ("task_sha256", "F" * 64),
            ("task_sha256", True),
            ("bindings", []),
            ("bindings", {"sprite": "bad", "preview": "c" * 64}),
            ("bindings", {"bad id": "a" * 64}),
        ]
        for field, value in invalid:
            supplied = context()
            supplied[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(PixlError):
                job_history.new("job1", request(), supplied)
        for job_id in ("", "bad id", "1job", True, None):
            with self.subTest(job_id=job_id), self.assertRaises(PixlError):
                job_history.new(job_id, request(), context())

    def test_replay_rejects_nonobject_journals_and_boolean_versions(self):
        for supplied in (None, [], "journal", 1):
            with (
                self.subTest(type=type(supplied).__name__),
                self.assertRaises(PixlError),
            ):
                job_history.validate(supplied)
        for version in (True, 1.0, "1", 2):
            supplied = self.prepared()
            supplied["version"] = version
            with self.subTest(version=version), self.assertRaises(PixlError):
                job_history.validate(supplied)

    def test_replay_never_reads_catalog_or_performs_io(self):
        history = self.dispatched()
        with (
            patch(
                "pixl.platform.capabilities", side_effect=AssertionError("catalog read")
            ),
            patch("pathlib.Path.read_bytes", side_effect=AssertionError("file read")),
        ):
            self.assertEqual(job_history.validate(history), history)


if __name__ == "__main__":
    unittest.main()
