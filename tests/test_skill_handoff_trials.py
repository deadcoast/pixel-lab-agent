"""Local preparation and evidence retention do not sample a native model."""

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from evaluations import skill_handoff_trials as trials
from evaluations.host_trials import inventory, sha, write_json


class SkillHandoffTrialsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.package = self.root / "source-kit"
        self.package.mkdir()
        self.file(self.package, "scripts/pixl.py", "# local runtime fixture\n")
        self.file(self.package, "skills/pixl/SKILL.md", "# frozen skill fixture\n")
        write_json(self.package / "bundle-manifest.json", {"files": [
            {"path": name, "sha256": digest} for name, digest in inventory(self.package).items()]})
        self.seed = self.root / "seed"
        self.seed.mkdir()
        self.file(self.seed, "reference.png", b"reference fixture")
        self.file(self.seed, "reference-b.png", b"alternate fixture")
        self.file(self.seed, "state.px/state.px", "saved unresolved choices\n")
        self.file(self.seed, ".pixl/library-sources/source.txt", "retained source bytes\n")
        self.file(self.seed, "SESSION.md", "original recorded session\n")
        self.seed_files = inventory(self.seed)
        self.probe = patch.object(trials.subprocess, "check_output", side_effect=self.probe_output)
        self.probe.start()
        self.addCleanup(self.probe.stop)

    def file(self, root, name, content):
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

    def prepare(self, name="attempt", case="cold", **kwargs):
        destination, consumer = self.root / name, self.root / (name + " consumer")
        trials.prepare(destination, case, Path(sys.executable), package=self.package,
                       consumer=consumer, seed=self.seed, seed_manifest=self.seed_files, **kwargs)
        return destination, consumer

    def test_cold_inputs_are_exact_and_session_is_new_without_delegation(self):
        destination, consumer = self.prepare()
        second, _ = self.prepare("second")
        launch = json.loads((destination / "launch.json").read_bytes())
        other = json.loads((second / "launch.json").read_bytes())
        command = launch["command"]
        self.assertNotEqual(launch["expected_session_id"], other["expected_session_id"])
        self.assertNotIn("--resume", command)
        self.assertNotIn("--no-session-persistence", command)
        self.assertNotIn("--agents", command)
        self.assertNotIn("Agent", command[command.index("--tools") + 1].split(","))
        self.assertEqual(Path(command[command.index("--plugin-dir") + 1]), consumer / trials.KIT)
        self.assertEqual(inventory(destination / "input-project"), self.seed_files)
        for name, digest in self.seed_files.items():
            self.assertEqual(sha(consumer / name), digest)
        with zipfile.ZipFile(destination / "input-project.zip") as archive:
            self.assertIn(".pixl/library-sources/source.txt", archive.namelist())

    def test_default_fresh_preparation_uses_only_tracked_checkout_fixtures(self):
        checkout = self.root / "fresh checkout"
        default_relative = trials.FIXTURES.relative_to(trials.ROOT)
        tracked_relative = Path("evidence/host-evaluation/fixture-inputs")
        expected = {}
        for name in ("reference.png", "reference-b.png"):
            copied = self.file(checkout, (tracked_relative / name).as_posix(),
                               (trials.ROOT / tracked_relative / name).read_bytes())
            expected[name] = sha(copied)
        destination, consumer = self.root / "default attempt", self.root / "default consumer"
        with (
            patch.object(trials, "ROOT", checkout),
            patch.object(trials, "FIXTURES", checkout / default_relative),
            patch.object(trials, "run_native") as native,
        ):
            trials.prepare(destination, "fresh", Path(sys.executable), package=self.package, consumer=consumer)
            native.assert_not_called()
        self.assertFalse((checkout / "evidence/skill-handoff/revised-routing").exists())
        self.assertEqual(inventory(destination / "input-project"), expected)
        identity = json.loads((destination / "identity.json").read_bytes())
        self.assertEqual(identity["inputs"], expected)
        self.assertEqual(Path(identity["seed"]["path"]), checkout / tracked_relative)
        self.assertFalse((destination / "stdout.jsonl").exists())

    def test_stale_manifest_rejected_before_consumer_or_receipts_exist(self):
        self.file(self.seed, "reference.png", b"changed after manifest")
        with self.assertRaisesRegex(ValueError, "supplied manifest"):
            self.prepare()
        self.assertFalse((self.root / "attempt").exists())
        self.assertFalse((self.root / "attempt consumer").exists())

    def test_nested_old_kit_is_rejected_even_when_manifest_matches(self):
        for name in ("PIXL-KIT", "pixl-kit"):
            with self.subTest(name=name):
                old = self.file(self.seed, ".agents/skills/" + name + "/SKILL.md", "stale specialist instructions\n")
                self.seed_files = inventory(self.seed)
                with self.assertRaisesRegex(ValueError, "omit the installed kit"):
                    self.prepare()
                self.assertFalse((self.root / "attempt").exists())
                old.unlink()

    def test_reused_destination_and_consumer_do_not_change_prior_bytes(self):
        destination, consumer = self.prepare()
        before = inventory(destination)
        with self.assertRaisesRegex(ValueError, "fresh attempt"):
            self.prepare()
        with self.assertRaisesRegex(ValueError, "fresh consumer"):
            trials.prepare(self.root / "new", "cold", Path(sys.executable), package=self.package,
                           consumer=consumer, seed=self.seed, seed_manifest=self.seed_files)
        self.assertEqual(inventory(destination), before)

    def test_changed_state_and_static_source_are_reported_without_rewriting_inputs(self):
        destination, consumer = self.prepare()
        original = (destination / "input-project.zip").read_bytes()
        self.file(consumer, "state.px/state.px", "new project decision\n")
        self.file(consumer, "START-HERE.md", "next useful action\n")
        self.file(consumer, "reference.png", b"unexpected image edit")
        result = trials.retain(destination)
        self.assertIn("state.px/state.px", result["changed"])
        self.assertEqual(result["static_input_changes"], ["reference.png"])
        self.assertIn("START-HERE.md", result["new"])
        self.assertTrue(result["package_unchanged"])
        self.assertEqual((destination / "input-project.zip").read_bytes(), original)
        self.assertEqual(inventory(destination / "input-project"), self.seed_files)
        self.assertEqual(inventory(self.seed), self.seed_files)
        with zipfile.ZipFile(destination / "project.zip") as archive:
            self.assertEqual(archive.read("state.px/state.px"), b"new project decision\n")
        with self.assertRaisesRegex(ValueError, "already retained"):
            trials.retain(destination)

    def test_runtime_failure_preserves_partial_project_and_failure_stream(self):
        destination, consumer = self.prepare()

        def fail(attempt, *, timeout):
            self.assertIsNone(timeout)
            self.file(attempt, "stderr.txt", "native launch failed\n")
            self.file(consumer, "PARTIAL.md", "useful incomplete work\n")
            raise OSError("simulated host failure")

        with patch.object(trials, "run_native", side_effect=fail), self.assertRaisesRegex(OSError, "simulated host failure"):
            trials.run(destination)
        self.assertEqual((destination / "stderr.txt").read_text(), "native launch failed\n")
        self.assertEqual((destination / "project/PARTIAL.md").read_text(), "useful incomplete work\n")
        self.assertTrue((destination / "preservation.json").is_file())

    def test_session_handoff_amendment_keeps_both_snapshots_without_static_failure(self):
        for name in ("AGENTS.md", "CLAUDE.md"):
            self.file(self.seed, name, "prior consumer handoff\n")
        self.seed_files = inventory(self.seed)
        destination, consumer = self.prepare()
        for name in ("SESSION.md", "AGENTS.md", "CLAUDE.md"):
            self.file(consumer, name, "current consumer decisions and next action\n")
        result = trials.retain(destination)
        self.assertEqual(result["static_input_changes"], [])
        self.assertTrue(result["package_unchanged"])
        self.assertEqual(set(result["changed"]), {"SESSION.md", "AGENTS.md", "CLAUDE.md"})
        with zipfile.ZipFile(destination / "input-project.zip") as before, zipfile.ZipFile(destination / "project.zip") as after:
            for name in result["changed"]:
                self.assertEqual(before.read(name), (self.seed / name).read_bytes())
                self.assertEqual(after.read(name), (consumer / name).read_bytes())
                self.assertNotEqual(before.read(name), after.read(name))

    def test_changed_prepared_input_prevents_host_execution(self):
        destination, consumer = self.prepare()
        self.file(consumer, "state.px/state.px", "changed before native launch\n")
        with patch.object(trials, "run_native") as native:
            with self.assertRaisesRegex(ValueError, "changed before execution"):
                trials.run(destination)
            native.assert_not_called()

    def test_frozen_kit_mutation_is_retained_as_failure_evidence(self):
        destination, consumer = self.prepare()
        self.file(consumer / trials.KIT, "scripts/pixl.py", "changed runtime\n")
        result = trials.retain(destination)
        self.assertFalse(result["package_unchanged"])
        self.assertEqual((destination / "mutated-package/scripts/pixl.py").read_text(), "changed runtime\n")


if __name__ == "__main__":
    unittest.main()
