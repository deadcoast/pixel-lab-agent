"""Exact historical reconstruction and bounded native preparation, without launches."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from evaluations import consumer_execution_case as case
from evaluations.host_trials import inventory, sha, write_json
from pixl import candidate_review, codec, store


class ConsumerExecutionCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # One real durable reconstruction, including every source hash and the
        # historical Git package. No ignored build directory supplies an input.
        cls.files, cls.provenance = case.retained_project()

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="consumer execution fixture ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.destination = self.root / "attempt"
        self.consumer = self.root / "external consumer"

    def fake_host_setup(self, destination, host, setup, python, *, package, consumer):
        """Replace native discovery only; production validation remains real."""
        destination.mkdir()
        consumer.mkdir()
        (consumer / "BRIEF.md").write_text("disposable readiness marker\n", encoding="utf-8")
        (consumer / "AGENTS.md").write_text("current setup\n", encoding="utf-8")
        current_role = consumer / ".codex/agents/pixl.toml"
        current_role.parent.mkdir(parents=True)
        current_role.write_text('name = "pixl"\n# current role\n', encoding="utf-8")
        write_json(destination / "identity.json", {"inputs": {}, "package_files": {}})
        write_json(destination / "launch.json", {"host": host, "cwd": str(consumer)})
        (destination / "runner.py.txt").write_bytes(b"current host setup runner\n")
        return consumer

    def prepare(self, *, files=None):
        with patch.object(case, "retained_project", return_value=(files or dict(self.files), copy.deepcopy(self.provenance))), \
                patch.object(case.readiness_case, "prepare", side_effect=self.fake_host_setup):
            return case.prepare(self.destination, "codex", Path(sys.executable), consumer=self.consumer)

    def test_restores_exact_accepted_state_sources_art_and_inactive_historical_host(self):
        self.prepare()
        identity = json.loads((self.destination / "identity.json").read_bytes())
        for name, digest in self.provenance["files"].items():
            self.assertEqual(sha(self.consumer / case.historical_target(name)), digest, name)
        self.assertEqual(identity["restoration"]["omitted_files"], [])
        self.assertEqual(len(identity["restoration"]["historical_kit_files"]), 174)
        self.assertNotEqual((self.consumer / "AGENTS.md").read_bytes(), self.files["AGENTS.md"])
        self.assertIn(b"current role", (self.consumer / ".codex/agents/pixl.toml").read_bytes())
        self.assertFalse((self.consumer / ".agents/skills/artistic-revision-kit").exists())
        self.assertTrue((self.consumer / case.INPUTS / "historical-host/.agents/skills/artistic-revision-kit/bundle-manifest.json").is_file())
        document = store.load(self.consumer / Path(case.STATE).parent)
        context = candidate_review.context(document, self.consumer, case.CANDIDATE)
        self.assertEqual(context["current_acceptance"], {"all_required_pass": True, "task_complete": True})
        self.assertFalse(context["snapshot_acceptance"]["accepted"])
        self.assertEqual((self.consumer / case.STATE).read_bytes(), self.files[case.STATE])
        self.assertEqual(inventory(self.consumer / ".pixl"), identity["baseline_production"])
        config = json.loads((self.consumer / case.INPUTS / "config.json").read_bytes())
        self.assertEqual(config["modules"]["view"], "src/queue-view-artistic.ts")
        self.assertEqual({row["output"] for row in context["members"]}, set(config["destinations"]))
        for member in context["members"]:
            self.assertEqual(sha(self.consumer / config["destinations"][member["output"]]), member["sha256"])
        self.assertFalse((self.destination / "stdout.jsonl").exists())
        self.assertFalse((self.consumer / case.WORK / "execution-01").exists())
        assignment = (self.consumer / "CONSUMER-EXECUTION.md").read_text(encoding="utf-8")
        for required in ("pixl_consumer_execute", "actual returned PNGs", "acceptance_created=false",
                         "production profile", "Do not create candidate reviews", "M1/M2 and broader M3"):
            self.assertIn(required, assignment)

    def test_mismatched_served_art_cannot_be_prepared_as_the_retained_family(self):
        files = dict(self.files)
        files["assets/working.png"] = files["assets/paused.png"]
        with self.assertRaisesRegex((ValueError, codec.PixlError), "asset differs|hash|digest"):
            self.prepare(files=files)
        self.assertFalse((self.destination / "stdout.jsonl").exists())
        self.assertFalse((self.consumer / case.WORK / "execution-01").exists())

    def test_retention_preserves_failed_run_and_unexpected_changes_without_overwrite(self):
        self.prepare()
        write_json(self.consumer / case.WORK / "execution-result.json", {"status": "unavailable", "acceptance_created": False})
        write_json(self.consumer / case.WORK / "execution-01/failure.json", {"reason": "No browser capability"})
        (self.consumer / case.STATE).write_bytes(b"unexpected state change\n")
        (self.consumer / "assets/paused.png").unlink()
        (self.consumer / "unexpected.txt").write_bytes(b"unexpected addition\n")
        case.retain(self.destination)
        preserved = json.loads((self.destination / "preservation.json").read_bytes())
        self.assertFalse(preserved["production_unchanged"])
        self.assertIn(case.STATE, preserved["changed"])
        self.assertIn("assets/paused.png", preserved["removed"])
        self.assertEqual(json.loads((self.destination / "outputs/execution-result.json").read_bytes())["status"], "unavailable")
        with zipfile.ZipFile(self.destination / "unexpected-delta.zip") as archive:
            self.assertEqual(archive.read(case.STATE), b"unexpected state change\n")
            self.assertEqual(archive.read("unexpected.txt"), b"unexpected addition\n")
        before = inventory(self.destination)
        with self.assertRaisesRegex(ValueError, "Preserve prior retention"):
            case.retain(self.destination)
        self.assertEqual(inventory(self.destination), before)

    def test_corrupt_durable_delta_fails_before_host_setup_or_consumer_creation(self):
        retained = self.root / "tampered retained inputs"
        retained.mkdir()
        for name in ("identity.json", "consumer-delta.json", "consumer-entrypoints.zip"):
            shutil.copyfile(case.RETAINED / name, retained / name)
        (retained / "consumer-delta.zip").write_bytes(b"not the retained archive")
        with (patch.object(case, "RETAINED", retained), patch.object(case.readiness_case, "prepare") as host,
              self.assertRaisesRegex(ValueError, "delta archive changed")):
            case.prepare(self.destination, "codex", Path(sys.executable), consumer=self.consumer)
        host.assert_not_called()
        self.assertFalse(self.destination.exists())
        self.assertFalse(self.consumer.exists())


if __name__ == "__main__":
    unittest.main()
