"""CF-09 preparation preserves real inputs and cannot fake new output or history."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from evaluations import art_revision_case as case
from evaluations.host_trials import inventory


class ArtRevisionPreparationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.assignment = self.base / "assignment.md"
        self.assignment.write_text("# Scoped CF-09 test assignment\n", encoding="utf-8")

    def test_exact_reconstructable_inputs_have_no_fabricated_outputs_or_state(self):
        attempt = self.base / "attempt"
        root = case.prepare(attempt, assignment=self.assignment)
        receipt = json.loads((attempt / "preparation.json").read_text(encoding="utf-8"))
        actual = inventory(root)
        self.assertEqual(actual, receipt["consumer_inputs"])
        for name, digest in {**case.SOURCE_HASHES, **case.ASSET_HASHES}.items():
            self.assertEqual(actual[name], digest)
        with zipfile.ZipFile(attempt / "consumer-inputs.zip") as retained:
            self.assertEqual(set(retained.namelist()), set(actual))
            for name in retained.namelist():
                self.assertEqual(retained.read(name), (root / name).read_bytes())
        for name in receipt["planned_animation"]["missing_files"]:
            self.assertFalse((root / name).exists())
        self.assertFalse((root / ".pixl").exists())
        self.assertFalse(receipt["artistic_acceptance"])
        self.assertFalse(receipt["human_acceptance"])
        self.assertFalse(receipt["cf09_complete"])
        self.assertEqual(receipt["provider_calls"], 0)
        self.assertEqual(len({member["origin"] for member in receipt["preserved_directions"]}), 3)

    def test_existing_attempt_is_never_overwritten(self):
        attempt = self.base / "attempt"
        attempt.mkdir()
        prior = attempt / "existing.txt"
        prior.write_bytes(b"Keep prior results and work")
        before = inventory(attempt)
        with self.assertRaisesRegex(ValueError, "fresh CF-09"):
            case.prepare(attempt, assignment=self.assignment)
        self.assertEqual(inventory(attempt), before)

    def test_archive_drift_refuses_before_creating_destination(self):
        archive = self.base / "changed.zip"
        archive.write_bytes(case.ARCHIVE.read_bytes() + b"changed")
        attempt = self.base / "attempt"
        with self.assertRaisesRegex(ValueError, "Retained source identity changed"):
            case.prepare(attempt, archive=archive, assignment=self.assignment)
        self.assertFalse(attempt.exists())

    def test_source_drift_refuses_before_creating_destination(self):
        project = self.base / "project"
        for name in case.SOURCE_HASHES:
            destination = project / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(case.PROJECT / name, destination)
        (project / "BRIEF.md").write_bytes(b"Changed source intent")
        attempt = self.base / "attempt"
        with self.assertRaisesRegex(ValueError, "Retained source identity changed: BRIEF.md"):
            case.prepare(attempt, project=project, assignment=self.assignment)
        self.assertFalse(attempt.exists())


if __name__ == "__main__":
    unittest.main()
