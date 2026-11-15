"""CF-10 preparation boundaries, not native behavior or generated quality."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from evaluations import integration_change_case
from evaluations import native_production_case as case
from evaluations.host_trials import inventory, sha, write_json
from pixl import plar


class NativeProductionCaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "consumer"
        self.root.mkdir()

    def copy_source(self, name):
        source = integration_change_case.SOURCE if name == "queue-ready" else case.ROOT / "examples/delegation"
        paths = (integration_change_case.source_paths(source) if name == "queue-ready" else
                 ["BRIEF.md", "plar.txt", "src/robot.ts", "assets/robot-base.png"])
        for path in paths:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / path, target)
        (self.root / case.INPUTS).mkdir(parents=True)
        if name == "queue-ready":
            shutil.copyfile(self.root / "assets/ready-confirmed.png", self.root / case.INPUTS / "original-ready.png")
        (self.root / case.AUTHORITY).write_text("Explicit fresh production authority", encoding="utf-8")

    def test_replacement_cannot_change_retained_style_authority(self):
        self.copy_source("queue-ready")
        before = inventory(self.root)
        doc = case.prospective(self.root, "queue-ready")
        self.assertEqual(before, inventory(self.root))
        plar.validate(doc, self.root)
        source = next(row for row in doc["sources"] if row["id"] == "approved-ready")
        self.assertEqual(f"{case.INPUTS}/original-ready.png", source["path"])
        for row in doc["assets"]:
            for rule in row["requirements"]:
                if rule["property"] == "approved_style_reference":
                    self.assertEqual(source["path"], rule["value"]["path"])
        (self.root / "assets/ready-confirmed.png").write_bytes(b"new output not a style input")
        self.assertEqual(source["sha256"], sha(self.root / source["path"]))
        self.assertFalse((self.root / ".pixl").exists())
        self.assertTrue(all("production" not in row for row in doc["assets"]))
        self.assertEqual(["queue.ready"], [row["id"] for row in doc["assets"] if row["status"] == "todo"])

    def test_robot_keeps_dependency_identity_and_original_plan_only_brief(self):
        self.copy_source("robot-directions")
        before = inventory(self.root)
        doc = case.prospective(self.root, "robot-directions")
        self.assertEqual(before, inventory(self.root))
        plar.validate(doc, self.root)
        robot = next(row for row in doc["assets"] if row["id"] == "robot.directions")
        self.assertEqual(["robot.base"], robot["depends_on"])
        self.assertEqual("assets/robot", robot["delivery"]["path"])
        self.assertIn("plan, not remote execution", (self.root / "BRIEF.md").read_text())
        self.assertEqual("cf10_production_scope", robot["requirements"][-1]["property"])

    def test_retention_discloses_unauthorized_changes_and_keeps_ignored_state(self):
        evidence = Path(self.temp.name) / "evidence"
        evidence.mkdir()
        (self.root / "source.txt").write_text("original")
        (self.root / case.PLAR).write_text("old")
        write_json(evidence / "identity.json", {"inputs": inventory(self.root),
                   "authorized_changes": [case.PLAR], "authorized_new_prefixes": [case.WORK + "/", ".pixl/"]})
        write_json(evidence / "launch.json", {"cwd": str(self.root)})
        (self.root / "source.txt").write_text("changed")
        (self.root / case.PLAR).write_text("new")
        write_json(self.root / ".pixl/state.json", {"real": "retained test state"})
        write_json(self.root / case.WORK / "partial.json", {"status": "incomplete"})
        case.retain(evidence)
        receipt = json.loads((evidence / "preservation.json").read_bytes())
        self.assertEqual(["source.txt"], receipt["unexpected"])
        self.assertIn(".pixl/state.json", receipt["new"])
        self.assertTrue((evidence / "consumer-delta.zip").is_file())
        self.assertEqual("incomplete", json.loads((evidence / "outputs/partial.json").read_bytes())["status"])
        with self.assertRaisesRegex(ValueError, "immutable"):
            case.retain(evidence)

    def test_retention_reports_removed_protected_input(self):
        evidence = Path(self.temp.name) / "removed-evidence"
        evidence.mkdir()
        write_json(evidence / "identity.json", {
            "inputs": {"missing-original.png": "0" * 64},
            "authorized_changes": [], "authorized_new_prefixes": [case.WORK + "/"]})
        write_json(evidence / "launch.json", {"cwd": str(self.root)})
        case.retain(evidence)
        receipt = json.loads((evidence / "preservation.json").read_bytes())
        self.assertEqual(["missing-original.png"], receipt["removed"])
        self.assertEqual(["missing-original.png"], receipt["unexpected"])


if __name__ == "__main__":
    unittest.main()
