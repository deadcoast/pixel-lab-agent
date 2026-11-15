"""Exercise isolated caller-review preparation and retention without model sampling."""

import json
import sys
import tempfile
import unittest
import uuid
import zipfile
from pathlib import Path
from unittest.mock import patch

from evaluations import cold_caller_review as trials
from evaluations.host_trials import inventory, sha, write_json


class ColdCallerReviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.package = self.root / "source kit"
        self.file(self.package, "scripts/pixl.py", "# local runtime fixture\n")
        self.file(self.package, "skills/pixl/SKILL.md", "# frozen skill fixture\n")
        self.file(self.package, "agents/pixl.md", "---\nname: pixl\nmodel: inherit\n---\n")
        write_json(self.package / "bundle-manifest.json", {"files": [
            {"path": name, "sha256": digest} for name, digest in inventory(self.package).items()]})
        self.seed = self.root / "seed"
        for name in ("SESSION.md", "sources/brief.md", "state.px/state.px", "state.px/history/prior.px",
                     ".pixl/library-sources/source.txt", "deliverables/prior.md"):
            self.file(self.seed, name, "original retained " + name + "\n")
        self.file(self.seed, "reference.png", b"reference fixture")
        self.manifest = self.root / "seed-manifest.json"
        write_json(self.manifest, inventory(self.seed))
        self.protocol = self.root / "protocol.json"
        self.assignment = {"neutral_task_core": "Continue through the native pixl:pixl specialist and independently review its result.",
            "setup_template": "Consumer {CONSUMER_ROOT}; selected Python {PYTHON_EXE}."}
        write_json(self.protocol, {"assignment": self.assignment, "evaluator_only": "DO NOT SUPPLY GRADER FINDINGS"})
        self.amendment = self.root / "amendment.json"
        write_json(self.amendment, {"assignment": {"appended_prompt_text": "Save your own CALLER-RESULT.json with actual file hashes."},
            "evaluator_only": "EXPECTED OUTCOME MUST STAY OUTSIDE INPUT"})
        self.probe = patch.object(trials.subprocess, "check_output", side_effect=self.probe_output)
        self.probe.start()
        self.addCleanup(self.probe.stop)

    @staticmethod
    def file(root, name, content):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())
        return path

    @staticmethod
    def probe_output(command, **kwargs):
        if command[0] == "git":
            return "fixture-source-revision\n"
        if "--version" in command:
            return "Claude fixture version\n"
        return json.dumps({"executable": sys.executable, "version": "fixture", "packages": []})

    def prepare(self, name="attempt", **kwargs):
        destination, consumer = self.root / name, self.root / (name + " consumer")
        options = {"seed": self.seed, "seed_manifest": self.manifest, "protocol": self.protocol,
            "amendment": self.amendment, "python": Path(sys.executable), "package": self.package, "consumer": consumer}
        options.update(kwargs)
        trials.prepare(destination, **options)
        return destination, consumer

    def test_exact_seed_and_only_neutral_assignment_reach_registered_native_topology(self):
        with patch.object(trials, "run_native") as native:
            destination, consumer = self.prepare()
            second, _ = self.prepare("second")
            native.assert_not_called()
        identity = json.loads((destination / "identity.json").read_bytes())
        launch = json.loads((destination / "launch.json").read_bytes())
        command = launch["command"]
        uuid.UUID(launch["expected_session_id"])
        self.assertNotEqual(launch["expected_session_id"], json.loads((second / "launch.json").read_bytes())["expected_session_id"])
        self.assertEqual(identity["inputs"], inventory(self.seed))
        self.assertEqual(inventory(destination / "input-project"), inventory(self.seed))
        self.assertEqual(inventory(consumer, (trials.KIT,)), inventory(self.seed))
        self.assertEqual(identity["target_role"], "pixl:pixl")
        self.assertEqual(Path(command[command.index("--plugin-dir") + 1]), consumer / trials.KIT)
        self.assertEqual(command[command.index("--setting-sources") + 1], "")
        self.assertTrue({"Agent", "SendMessage", "TaskOutput"}.issubset(command[command.index("--tools") + 1].split(",")))
        self.assertIn("--forward-subagent-text", command)
        self.assertNotIn("--no-session-persistence", command)
        self.assertNotIn("--resume", command)
        self.assertNotIn("--agents", command)
        self.assertEqual(Path(launch["configuration_files"]["claude_plugin_agent"]), consumer / trials.KIT / "agents/pixl.md")
        expected = (self.assignment["neutral_task_core"] + "\n\n"
            + self.assignment["setup_template"].format(CONSUMER_ROOT=consumer.as_posix(), PYTHON_EXE=Path(sys.executable).resolve().as_posix())
            + "\n\nSave your own CALLER-RESULT.json with actual file hashes.\n")
        self.assertEqual((destination / "prompt.txt").read_text(), expected)
        self.assertNotIn("GRADER", expected)
        self.assertNotIn("EXPECTED OUTCOME", expected)
        mcp = json.loads((destination / "mcp.json").read_bytes())["mcpServers"]
        self.assertEqual(set(mcp), {"pixl-local"})
        self.assertEqual(mcp["pixl-local"]["args"][:2], ["-B", "-I"])
        with zipfile.ZipFile(destination / "input-project.zip") as archive:
            self.assertEqual(set(archive.namelist()), set(inventory(self.seed)))
            self.assertEqual(archive.read(".pixl/library-sources/source.txt"), (self.seed / ".pixl/library-sources/source.txt").read_bytes())
        for item in identity["source_files"]:
            self.assertEqual(item["source"]["sha256"], item["snapshot"]["sha256"])

    def test_stale_or_missing_supplied_manifest_stops_before_creating_outputs(self):
        for supplied in (None, {}, {"reference.png": "0" * 64}):
            with self.subTest(manifest=supplied), self.assertRaisesRegex(ValueError, "required supplied manifest"):
                self.prepare(seed_manifest=supplied)
        self.assertFalse((self.root / "attempt").exists())
        self.assertFalse((self.root / "attempt consumer").exists())

    def test_feedback_and_evaluator_protocol_are_not_allowed_in_seed(self):
        for name in ("CALLER-REVIEW.md", "old/semantic-review-04.json", "grader/findings.md", "nested/PIXL-KIT/skill.md"):
            added = self.file(self.seed, name, "not a permitted seed input\n")
            try:
                with self.subTest(name=name), self.assertRaises(ValueError):
                    self.prepare(seed_manifest=inventory(self.seed))
            finally:
                added.unlink()
        nested = self.seed / "protocol.json"
        nested.write_bytes(self.protocol.read_bytes())
        with self.assertRaisesRegex(ValueError, "outside the project seed"):
            self.prepare(protocol=nested, seed_manifest=inventory(self.seed))
        self.assertFalse((self.root / "attempt").exists())

    def test_changed_binding_or_prepared_input_refuses_native_execution(self):
        mutations = ("prompt.txt", "runtime-environment.json", "mcp.json", "input-project.zip", "runner.py.txt",
                     "runner-sources/evaluations/skill_handoff_trials.py.txt", "consumer/state.px/state.px", "protocol.json")
        for index, name in enumerate(mutations):
            with self.subTest(name=name):
                destination, consumer = self.prepare("attempt-" + str(index))
                if name == "protocol.json":
                    target = self.protocol
                elif name.startswith("consumer/"):
                    target = consumer / name.removeprefix("consumer/")
                else:
                    target = destination / name
                target.write_bytes(target.read_bytes() + b"\nchanged after preparation\n")
                with patch.object(trials, "run_native") as native, self.assertRaisesRegex(ValueError, "changed before execution"):
                    trials.run(destination)
                native.assert_not_called()
                self.assertFalse((destination / "preservation.json").exists())

    def test_native_failure_keeps_partial_child_output_and_stream_with_no_default_timeout(self):
        destination, consumer = self.prepare()

        def fail(attempt, *, timeout):
            self.assertIsNone(timeout)
            self.file(attempt, "stderr.txt", "simulated native failure\n")
            self.file(consumer, "PARTIAL.md", "retained child progress\n")
            raise OSError("simulated native failure")

        with patch.object(trials, "run_native", side_effect=fail), self.assertRaisesRegex(OSError, "simulated native failure"):
            trials.run(destination)
        self.assertEqual((destination / "stderr.txt").read_text(), "simulated native failure\n")
        self.assertEqual((destination / "project/PARTIAL.md").read_text(), "retained child progress\n")
        self.assertTrue((destination / "preservation.json").is_file())
        self.assertEqual(inventory(destination / "input-project"), inventory(self.seed))

    def test_output_retention_separates_active_updates_from_original_source_history(self):
        destination, consumer = self.prepare()
        before_archive = sha(destination / "input-project.zip")
        for name in ("SESSION.md", "state.px/state.px", "sources/brief.md", "state.px/history/prior.px"):
            self.file(consumer, name, "changed " + name + "\n")
        self.file(consumer, "CALLER-RESULT.json", '{"status":"partial"}\n')
        self.file(consumer, "deliverables/current.md", "new useful continuation\n")
        result = trials.retain(destination)
        self.assertEqual(set(result["static_input_changes"]), {"sources/brief.md", "state.px/history/prior.px"})
        self.assertIn("CALLER-RESULT.json", result["new"])
        self.assertTrue(result["package_unchanged"])
        self.assertEqual(sha(destination / "input-project.zip"), before_archive)
        self.assertEqual(inventory(destination / "input-project"), inventory(self.seed))
        with zipfile.ZipFile(destination / "project.zip") as archive:
            self.assertEqual(archive.read("CALLER-RESULT.json"), (consumer / "CALLER-RESULT.json").read_bytes())
        with self.assertRaisesRegex(ValueError, "already retained"):
            trials.retain(destination)

    def test_reused_attempt_or_retained_run_preserves_receipts(self):
        destination, _ = self.prepare()
        before = inventory(destination)
        with self.assertRaisesRegex(ValueError, "fresh attempt"):
            self.prepare()
        self.assertEqual(inventory(destination), before)
        trials.retain(destination)
        retained = inventory(destination)
        with patch.object(trials, "run_native") as native, self.assertRaisesRegex(ValueError, "previous outcomes"):
            trials.run(destination)
        native.assert_not_called()
        self.assertEqual(inventory(destination), retained)


if __name__ == "__main__":
    unittest.main()
