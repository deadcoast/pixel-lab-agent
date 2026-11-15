"""Allocation fixtures preserve real history and keep observation boundaries explicit."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import plar_coverage_case as case
from evaluations.host_trials import inventory, sha, write_json


class CoveragePreparationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="allocation fixture test ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.source = self.root / "retained source"
        shutil.copytree(case.SOURCE, self.source)
        self.original = inventory(self.source, ("__pycache__",))
        self.destination = self.root / "attempt"
        self.consumer = self.root / "external consumer"

    def fake_host_setup(self, destination, host, setup, python, *, package, consumer):
        """Replace host discovery only; baseline reads still execute the real CLI."""
        destination.mkdir()
        consumer.mkdir()
        scripts = consumer / case.KIT / "scripts"
        scripts.mkdir(parents=True)
        bridge = (
            "import sys\n"
            f"sys.path.insert(0, {str(case.ROOT)!r})\n"
            "from pixl.entrypoint import main\n"
            "main()\n"
        )
        (scripts / "pixl.py").write_text(bridge, encoding="utf-8")
        write_json(destination / "identity.json", {"inputs": {}, "package_files": {}})
        write_json(destination / "launch.json", {"host": host, "cwd": str(consumer)})
        (destination / "runner.py.txt").write_bytes(b"retained host setup runner\n")
        (consumer / "AGENTS.md").write_text("new isolated host instructions", encoding="utf-8")
        return consumer

    def prepare(self):
        with patch.object(case.readiness_case, "prepare", side_effect=self.fake_host_setup):
            return case.prepare(
                self.destination, "codex", Path(sys.executable),
                consumer=self.consumer, source=self.source,
            )

    @unittest.skipUnless(shutil.which("node"), "Node is required for descriptor execution")
    def test_external_fixture_preserves_original_bytes_state_and_existing_drift(self):
        self.assertFalse(self.root.is_relative_to(case.ROOT))
        self.assertEqual(self.prepare(), self.consumer)
        identity = json.loads((self.destination / "identity.json").read_bytes())
        self.assertEqual(inventory(self.source, ("__pycache__",)), self.original)
        for name, digest in identity["original_inputs"].items():
            self.assertEqual(sha(self.consumer / name), digest, name)
        state = ".pixl/assets/queue.working/state.px"
        self.assertEqual((self.consumer / state).read_bytes(), (self.source / state).read_bytes())
        self.assertEqual((self.destination / "baseline-plar.txt").read_bytes(), (self.source / "plar.txt").read_bytes())
        self.assertEqual(identity["baseline_hash"], self.original["plar.txt"])
        self.assertEqual(identity["brief"]["sha256"], self.original["BRIEF.md"])
        queue = json.loads((self.destination / "baseline-queue.json").read_bytes())
        self.assertEqual(queue["changes"]["changed_sources"], ["view"])
        view = next(row for row in queue["sources"] if row["id"] == "view")
        self.assertEqual(view["binding"], "changed")
        self.assertEqual(view["observed_sha256"], sha(self.consumer / "src/queue-view.ts"))
        self.assertNotEqual(view["sha256"], view["observed_sha256"])
        self.assertEqual(identity["baseline_changes"], queue["changes"])

    @unittest.skipUnless(shutil.which("node"), "Node is required for descriptor execution")
    def test_baseline_selections_bind_real_external_rows_and_populated_history(self):
        self.prepare()
        identity = json.loads((self.destination / "identity.json").read_bytes())
        selections = json.loads((self.destination / "baseline-selections.json").read_bytes())
        document = json.loads((self.source / "plar.txt").read_bytes())
        rows = {row["id"]: row for row in document["assets"]}
        self.assertEqual(set(selections), set(rows))
        self.assertEqual(identity["baseline_document"], document)
        self.assertEqual(identity["baseline_selections"], selections)
        for asset, selected in selections.items():
            self.assertEqual(selected["asset"], rows[asset])
            self.assertEqual(selected["hash"], sha(self.source / "plar.txt"))
            self.assertEqual(Path(selected["project_root"]), self.consumer)
            self.assertRegex(selected["requirements_hash"], r"^[0-9a-f]{64}$")
            for source in selected["sources"]:
                self.assertEqual(Path(source["absolute_path"]), self.consumer / source["path"])
                self.assertEqual(source["observed_sha256"], sha(self.consumer / source["path"]))
        working = rows["queue.working"]
        self.assertTrue(working["evidence"])
        self.assertEqual(working["production"]["store"], ".pixl/assets/queue.working")
        self.assertTrue(selections["queue.working"]["production"]["jobs"])
        self.assertTrue(list((self.consumer / ".pixl/plar-history").glob("*.json")))

    @unittest.skipUnless(shutil.which("node"), "Node is required for descriptor execution")
    def test_actual_node_descriptor_and_present_excluded_renderer_are_distinct(self):
        self.prepare()
        observation = json.loads((self.destination / "entrypoint-observation.json").read_bytes())
        self.assertEqual(observation["returncode"], 0)
        self.assertEqual(json.loads(observation["stdout"]), {
            "label": "Start", "path": "assets/start.svg", "frames": 1,
        })
        self.assertEqual(Path(observation["command"][1]), self.consumer / "src/shortcut-entry.mjs")
        self.assertIn("not a browser render", observation["scope"])
        self.assertEqual(
            (self.consumer / case.UNINSPECTED).read_bytes(),
            (case.ROOT / "examples/plar-project/renderer/view.mjs").read_bytes(),
        )
        overview = (self.consumer / "SOURCE-MAP.md").read_text(encoding="utf-8")
        self.assertIn("present copy", overview)
        self.assertIn("outside this assignment's inspection boundary", overview)
        self.assertIn("remote account badge registry is separately", overview)
        self.assertIn("unavailable", overview)
        identity = json.loads((self.destination / "identity.json").read_bytes())
        self.assertEqual(identity["fixture"]["uninspected"], [case.UNINSPECTED])
        self.assertEqual(identity["inputs"][case.UNINSPECTED], sha(self.consumer / case.UNINSPECTED))
        self.assertTrue(all(not (self.consumer / name).exists() for name in identity["fixture"]["missing_paths"]))

    @unittest.skipUnless(shutil.which("node"), "Node is required for descriptor execution")
    def test_wrong_executed_descriptor_retains_failure_instead_of_qualifying_fixture(self):
        with (
            patch.object(case, "ENTRY", 'console.log(JSON.stringify({label:"Different",path:"assets/start.svg",frames:1}));\n'),
            self.assertRaisesRegex(ValueError, "did not reuse"),
        ):
            self.prepare()
        observed = json.loads((self.destination / "entrypoint-observation.json").read_bytes())
        self.assertEqual(observed["returncode"], 0)
        self.assertEqual(json.loads(observed["stdout"])["label"], "Different")
        self.assertEqual((self.destination / "baseline-plar.txt").read_bytes(), (self.source / "plar.txt").read_bytes())
        self.assertEqual(inventory(self.source, ("__pycache__",)), self.original)

    def test_missing_source_or_node_rejects_before_host_setup(self):
        with patch.object(case.readiness_case, "prepare") as host_setup:
            with self.assertRaisesRegex(ValueError, "retained populated allocation"):
                case.prepare(self.destination, "codex", Path(sys.executable), source=self.root / "missing")
            with patch.object(case.shutil, "which", return_value=None), self.assertRaisesRegex(ValueError, "Node is required"):
                case.prepare(self.destination, "codex", Path(sys.executable), source=self.source)
            host_setup.assert_not_called()
        self.assertFalse(self.destination.exists())


class CoverageRetentionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="allocation retention test ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.consumer = self.root / "consumer"
        self.consumer.mkdir()
        self.destination = self.root / "attempt"
        self.destination.mkdir()
        (self.consumer / "plar.txt").write_bytes(b'{"old":"allocation"}\n')
        (self.consumer / "state.px").write_bytes(b"original production state\n")
        (self.consumer / "source.ts").write_bytes(b"original source\n")
        write_json(self.destination / "launch.json", {"cwd": str(self.consumer)})
        write_json(self.destination / "identity.json", {"inputs": inventory(self.consumer)})

    def test_retention_records_mutation_deletion_new_history_and_exact_outputs(self):
        old_plar = (self.consumer / "plar.txt").read_bytes()
        old_hash = sha(self.consumer / "plar.txt")
        (self.consumer / "state.px").write_bytes(b"changed production state\n")
        (self.consumer / "source.ts").unlink()
        (self.consumer / "plar.txt").write_bytes(b'{"new":"allocation"}\n')
        history = self.consumer / ".pixl/plar-history" / f"{old_hash}.json"
        history.parent.mkdir(parents=True)
        history.write_bytes(old_plar)
        result = self.consumer / case.WORK / "CALLER-RESULT.json"
        write_json(result, {"claim": "not an independent pass"})
        case.retain(self.destination)
        record = json.loads((self.destination / "preservation.json").read_bytes())
        self.assertEqual(set(record["changed"]), {"plar.txt", "state.px", "source.ts"})
        self.assertEqual(record["added"][history.relative_to(self.consumer).as_posix()], old_hash)
        self.assertEqual((self.destination / "plar-history" / history.name).read_bytes(), old_plar)
        self.assertEqual((self.destination / "outputs/CALLER-RESULT.json").read_bytes(), result.read_bytes())
        self.assertEqual((self.destination / "final-plar.txt").read_bytes(), (self.consumer / "plar.txt").read_bytes())

    def test_every_partial_or_complete_retention_target_is_preserved(self):
        write_json(self.consumer / case.WORK / "CALLER-RESULT.json", {"new": True})
        for name, directory in (("preservation.json", False), ("outputs", True),
                                ("final-plar.txt", False), ("plar-history", True)):
            with self.subTest(existing=name):
                destination = self.root / name.replace(".", "-")
                shutil.copytree(self.destination, destination)
                target = destination / name
                if directory:
                    target.mkdir()
                    (target / "retained.txt").write_bytes(b"preserve exact earlier evidence\n")
                else:
                    target.write_bytes(b"preserve exact earlier evidence\n")
                before = inventory(destination)
                with self.assertRaisesRegex(ValueError, "Preserve"):
                    case.retain(destination)
                self.assertEqual(inventory(destination), before)

    def test_failed_nested_history_keeps_distinct_files_with_the_same_basename(self):
        history = self.consumer / ".pixl/plar-history"
        for folder, data in (("a", b"first failed history bytes\n"), ("b", b"different failed history bytes\n")):
            target = history / folder / "snapshot.json"
            target.parent.mkdir(parents=True)
            target.write_bytes(data)
        case.retain(self.destination)
        for folder in ("a", "b"):
            self.assertEqual(
                (self.destination / "plar-history" / folder / "snapshot.json").read_bytes(),
                (history / folder / "snapshot.json").read_bytes(),
            )
        record = json.loads((self.destination / "preservation.json").read_bytes())
        self.assertIn(".pixl/plar-history/a/snapshot.json", record["added"])
        self.assertIn(".pixl/plar-history/b/snapshot.json", record["added"])


if __name__ == "__main__":
    unittest.main()
