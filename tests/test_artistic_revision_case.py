"""Original-consumer isolation and durable evidence for artistic revision trials."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from evaluations import artistic_revision_case as case
from evaluations.host_trials import inventory, sha, write_json


class ArtisticRevisionCaseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.consumer = self.root / "consumer"
        self.attempt = self.root / "attempt"
        self.manifest = self.root / "original-manifest.json"
        self.archive = self.root / "original.zip"

    def archive_inputs(self, files=None):
        files = files or {
            "project/BRIEF.md": b"unchanged owner intent\n",
            "project/AGENTS.md": b"old entrypoint\n",
            "project/SESSION.md": b"old session\n",
            "project/authoring-plar.txt": b"original requirements and links\n",
            "project/.pixl/assets/queue.ready/state.px": b"original twenty criteria\n",
            "project/work/focused-successor/specialist-proposal.json": b'{"original":29}\n',
            "project/src/queue-view-successor.ts": b"retained proposed consumer\n",
            "project/renderer-successor/view.mjs": b"retained proposed fixture\n",
        }
        with zipfile.ZipFile(self.archive, "w") as archive:
            for name, data in files.items():
                archive.writestr(name, data)
        write_json(self.manifest, {"archive": self.archive.name, "archive_sha256": sha(self.archive),
                                   "files": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}})
        return files

    def prepare_inputs(self):
        self.archive_inputs()
        predecessor = self.root / "predecessor"
        predecessor.mkdir()
        write_json(predecessor / "record.json", {"execution_status": "host_error"})
        continuation = self.root / "continuation"
        continuation.mkdir()
        for name in ("SPECIALIST-ROUND2.json", "PHASE2-CALLER.json"):
            write_json(continuation / name, {"retained": name})
        contracts = self.root / "contracts"
        contracts.mkdir()
        for name in ("current-tool-declarations.json", "workbench-describe-edits-response.json"):
            write_json(contracts / name, {"observed": name})
        role = self.root / ".codex/agents/pixl.toml"
        role.parent.mkdir(parents=True)
        role.write_text('name = "pixl"\ndeveloper_instructions = "Original role"\n')
        kit = self.root / "plugins/pixl"
        kit.mkdir(parents=True)
        write_json(kit / "bundle-manifest.json", {"version": "current"})
        for attribute, value in (("ROOT", self.root), ("ARCHIVE_MANIFEST", self.manifest),
                                 ("PREDECESSOR", predecessor), ("CONTINUATION", continuation)):
            patcher = patch.object(case, attribute, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        return contracts, role

    def test_exact_archive_restoration_preserves_prior_source_and_rejects_overlay(self):
        files = self.archive_inputs()
        original = case.restore_consumer(self.consumer, self.manifest)
        for name, data in files.items():
            self.assertEqual((self.consumer / name.removeprefix("project/")).read_bytes(), data)
        self.assertEqual(inventory(self.consumer), original["files"])
        with self.assertRaisesRegex(ValueError, "fresh consumer"):
            case.restore_consumer(self.consumer, self.manifest)

    def test_corrupt_archive_and_entry_hash_fail_before_writing_consumer(self):
        self.archive_inputs()
        with self.archive.open("ab") as stream:
            stream.write(b"corruption")
        with self.assertRaisesRegex(ValueError, "archive changed"):
            case.restore_consumer(self.consumer, self.manifest)
        self.assertFalse(self.consumer.exists())
        manifest = json.loads(self.manifest.read_bytes())
        manifest["archive_sha256"] = sha(self.archive)
        manifest["files"]["project/BRIEF.md"] = "0" * 64
        write_json(self.manifest, manifest)
        with self.assertRaisesRegex(ValueError, "entry changed"):
            case.restore_consumer(self.consumer, self.manifest)
        self.assertFalse(self.consumer.exists())

    def test_archive_traversal_fails_without_creating_any_consumer(self):
        self.archive_inputs({"project/../../outside.txt": b"escape"})
        with self.assertRaisesRegex(ValueError, "escapes consumer"):
            case.restore_consumer(self.consumer, self.manifest)
        self.assertFalse(self.consumer.exists())
        self.assertFalse((self.root.parent / "outside.txt").exists())

    def test_prepare_keeps_baseline_bytes_and_registers_unchanged_named_role(self):
        contracts, role = self.prepare_inputs()
        with patch.object(case, "codex_command", return_value=["codex"]), \
                patch.object(case.subprocess, "check_output", return_value="observed-version\n"):
            case.prepare(self.attempt, self.consumer, contracts=contracts)
        identity = json.loads((self.attempt / "identity.json").read_bytes())
        launch = json.loads((self.attempt / "launch.json").read_bytes())
        self.assertEqual((self.consumer / ".codex/agents/pixl.toml").read_bytes(), role.read_bytes())
        self.assertIn("agents.pixl.config_file=" + json.dumps((self.consumer / ".codex/agents/pixl.toml").as_posix()), launch["command"])
        self.assertEqual(Path(identity["baseline_state"]["path"]).read_bytes(), b"original twenty criteria\n")
        self.assertEqual(Path(identity["baseline_plar"]["path"]).read_bytes(), b"original requirements and links\n")
        self.assertEqual(Path(identity["original_proposal"]["path"]).read_bytes(), b'{"original":29}\n')
        self.assertEqual((self.consumer / "src/queue-view-successor.ts").read_bytes(), b"retained proposed consumer\n")
        self.assertEqual(identity["original_inputs"]["AGENTS.md"], hashlib.sha256(b"old entrypoint\n").hexdigest())
        self.assertEqual(identity["contracts"], inventory(contracts))
        self.assertFalse((self.attempt / "stdout.jsonl").exists())

    def test_missing_contracts_fail_without_preparing_state(self):
        contracts, _ = self.prepare_inputs()
        (contracts / "current-tool-declarations.json").unlink()
        with self.assertRaisesRegex(ValueError, "Missing current contract"):
            case.prepare(self.attempt, self.consumer, contracts=contracts)
        self.assertFalse(self.consumer.exists())
        self.assertFalse(self.attempt.exists())

    def test_retention_captures_partial_outputs_and_unexpected_state_changes(self):
        contracts, _ = self.prepare_inputs()
        with patch.object(case, "codex_command", return_value=["codex"]), \
                patch.object(case.subprocess, "check_output", return_value="observed-version\n"):
            case.prepare(self.attempt, self.consumer, contracts=contracts)
        state = self.consumer / ".pixl/assets/queue.ready/state.px"
        state.write_bytes(b"new publication\n")
        (self.consumer / "BRIEF.md").unlink()
        write_json(self.consumer / case.WORK / "CALLER-RESULT.json", {"unresolved": ["actual visual review"]})
        case.retain_outputs(self.attempt)
        delta = json.loads((self.attempt / "consumer-delta.json").read_bytes())
        self.assertIn(".pixl/assets/queue.ready/state.px", delta["changed_existing"])
        self.assertEqual(delta["removed"], ["BRIEF.md"])
        with zipfile.ZipFile(self.attempt / "consumer-delta.zip") as saved:
            self.assertEqual(saved.read(".pixl/assets/queue.ready/state.px"), b"new publication\n")
        self.assertEqual(json.loads((self.attempt / "outputs/CALLER-RESULT.json").read_bytes()),
                         {"unresolved": ["actual visual review"]})


if __name__ == "__main__":
    unittest.main()
