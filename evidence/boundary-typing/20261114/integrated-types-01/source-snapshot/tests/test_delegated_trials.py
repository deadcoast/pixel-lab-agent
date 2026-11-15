"""Validate trial isolation without starting an agent or contacting a provider."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import delegated_asset_trials as trials


class DelegatedTrialTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_hosts_share_frozen_inputs_and_expose_only_mock_provider(self):
        with patch.object(trials, "codex_command", return_value=["codex-test"]):
            codex = trials.prepare(self.root / "codex", "codex")
            claude = trials.prepare(self.root / "claude", "claude")
        self.assertEqual(codex["package_files"], claude["package_files"])
        self.assertEqual(codex["fixture_sha256"], claude["fixture_sha256"])
        self.assertEqual(codex["prompt_sha256"], claude["prompt_sha256"])
        config = json.loads((self.root / "claude/mcp.json").read_text())
        self.assertEqual(set(config["mcpServers"]), {"pixl-local", "pixellab-test"})
        self.assertIn(
            "pixellab_mock.py", config["mcpServers"]["pixellab-test"]["args"][0]
        )
        command = json.loads((self.root / "codex/launch.json").read_text())["command"]
        self.assertIn('default_permissions=":workspace"', command)
        self.assertIn(
            'mcp_servers.pixellab_test.default_tools_approval_mode="approve"', command
        )
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)
        for host in ("claude", "codex"):
            folder = self.root / host
            self.assertFalse((folder / "stdout.jsonl").exists())
            self.assertFalse((folder / "provider-calls.jsonl").exists())
            self.assertIn("front-facing", (folder / "project/BRIEF.md").read_text())
            self.assertTrue(
                json.loads((folder / "identity.json").read_text())["provider_simulated"]
            )

    def _launch(self):
        project = self.root / "project"
        project.mkdir()
        (self.root / "launch.json").write_text(
            json.dumps(
                {"host": "codex", "command": ["fictional-host"], "cwd": str(project)}
            )
        )
        (self.root / "prompt.txt").write_text("Mocked provider only")

    def test_run_scrubs_provider_and_model_api_keys_and_preserves_host_login_location(
        self,
    ):
        self._launch()
        captured = {}

        class Process:
            returncode = 0

            def communicate(self, data, timeout):
                captured["stdout"].write(b'{"type":"turn.completed"}\n')

        def launch(command, **kwargs):
            captured.update(kwargs)
            return Process()

        env = {
            "PIXELLAB_API_KEY": "fictional",
            "PIXEL_LAB_TOKEN": "fictional",
            "OPENAI_API_KEY": "fictional",
            "ANTHROPIC_API_KEY": "fictional",
            "CODEX_HOME": str(self.root / "existing-host-home"),
            "PYTHONPATH": "fictional",
        }
        with (
            patch.dict(os.environ, env),
            patch.object(trials.subprocess, "Popen", side_effect=launch),
        ):
            result = trials.run(self.root)
        for key in env:
            if key != "CODEX_HOME":
                self.assertNotIn(key, captured["env"])
        self.assertEqual(captured["env"]["CODEX_HOME"], env["CODEX_HOME"])
        self.assertEqual(result["execution_status"], "host_completed_ungraded")
        self.assertEqual(result["behavioral_verdict"], "ungraded")
        self.assertTrue(result["provider_simulated"])

    def test_prior_attempt_cannot_be_overwritten(self):
        self._launch()
        marker = self.root / "stdout.jsonl"
        marker.write_text("previous failed evidence")
        with patch.object(trials.subprocess, "Popen") as launch:
            with self.assertRaisesRegex(ValueError, "only once"):
                trials.run(self.root)
            launch.assert_not_called()
        self.assertEqual(marker.read_text(), "previous failed evidence")

    def test_modified_package_is_rejected_before_host_launch(self):
        repository = self.root / "repository"
        plugin = repository / "plugins/pixl"
        plugin.mkdir(parents=True)
        (plugin / "file.txt").write_text("changed")
        (plugin / "bundle-manifest.json").write_text(
            json.dumps({"files": [{"path": "file.txt", "sha256": "0" * 64}]})
        )
        with (
            patch.object(trials, "ROOT", repository),
            self.assertRaisesRegex(ValueError, "Build the plugin"),
        ):
            trials.prepare(self.root / "attempt", "claude")
        self.assertFalse((self.root / "attempt/launch.json").exists())


if __name__ == "__main__":
    unittest.main()
