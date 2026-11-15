"""The seeded native protocol cannot silently change its host configuration."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import host_trials, inspection_trials


class InspectionTrialTests(unittest.TestCase):
    def test_reused_protocol_rejects_changed_host_controls(self):
        with (
            tempfile.TemporaryDirectory() as folder,
            patch.object(host_trials, "EVIDENCE"),
        ):
            series = Path(folder) / "series"
            inspection_trials.prepare(series)
            protocol = json.loads(
                (series / "inspection-protocol.json").read_text(encoding="utf-8")
            )
            self.assertIn(".pixl/state.px", protocol["seed_files"])
            controls = series / "discovery/codex-session-overrides.json"
            controls.write_text("[]\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "protocol changed"):
                inspection_trials.prepare(series)


if __name__ == "__main__":
    unittest.main()
