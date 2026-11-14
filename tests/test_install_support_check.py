"""Qualification harness boundaries: no accidental overwrite or unbound success."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from evaluations import install_support_check as check


class InstallSupportCheckTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def tree(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def test_existing_evidence_refusal_preserves_work_and_receipts(self):
        evidence = self.root / "evidence/install-support/old"
        evidence.mkdir(parents=True)
        (evidence / "failure.json").write_text('{"status":"fail"}')
        before = self.tree()
        with patch.object(check, "ROOT", self.root), self.assertRaises(FileExistsError):
            check.fresh_paths(self.root / "build/new", evidence)
        self.assertEqual(before, self.tree())
        self.assertFalse((self.root / "build/new").exists())

    def test_outside_output_is_rejected_before_any_directory_creation(self):
        with patch.object(check, "ROOT", self.root), self.assertRaises(ValueError):
            check.fresh_paths(self.root / "outside", self.root / "evidence/install-support/new")
        self.assertEqual(self.tree(), {})

    def test_relocation_preserves_exact_files_and_refuses_existing_destination(self):
        source = self.root / "work/consumer"
        destination = self.root / "work/consumer moved"
        source.mkdir(parents=True)
        (source / "state.px").write_bytes(b"retained state\r\n")
        check.safe_move(source, destination, self.root / "work")
        self.assertFalse(source.exists())
        self.assertEqual((destination / "state.px").read_bytes(), b"retained state\r\n")
        source.mkdir()
        (source / "other").write_text("preserve")
        before = self.tree()
        with self.assertRaises(FileExistsError):
            check.safe_move(source, destination, self.root / "work")
        self.assertEqual(before, self.tree())

    def test_recursive_or_outside_relocation_does_not_change_source(self):
        source = self.root / "work/consumer"
        source.mkdir(parents=True)
        (source / "art.png").write_bytes(b"retained bytes")
        before = self.tree()
        for destination in (source / "nested", self.root / "elsewhere"):
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                check.safe_move(source, destination, self.root / "work")
        self.assertEqual(before, self.tree())

    def test_manifest_byte_drift_is_not_qualified_or_repaired(self):
        kit = self.root / "kit"
        kit.mkdir()
        (kit / "runtime.py").write_bytes(b"original")
        (kit / "bundle-manifest.json").write_text(json.dumps({"files": [
            {"path": "runtime.py", "sha256": hashlib.sha256(b"original").hexdigest()}]}))
        self.assertEqual(check.exact_kit(kit)["path"], str(kit / "bundle-manifest.json"))
        (kit / "runtime.py").write_bytes(b"changed")
        before = self.tree()
        with self.assertRaisesRegex(ValueError, "manifest mismatch"):
            check.exact_kit(kit)
        self.assertEqual(before, self.tree())

    def test_failed_subprocess_retains_actual_exit_and_error(self):
        evidence = self.root / "evidence"
        evidence.mkdir()
        commands = check.Commands(evidence, self.root)
        with self.assertRaisesRegex(RuntimeError, "exited 7"):
            commands.run("failure", [sys.executable, "-c", "import sys; print('retained'); sys.stderr.write('reason'); sys.exit(7)"])
        receipt = json.loads((evidence / "01-failure.json").read_text())
        self.assertEqual(receipt["returncode"], 7)
        self.assertEqual((evidence / "01-failure.stderr.txt").read_text(), "reason")
        self.assertEqual((evidence / "01-failure.stdout.txt").read_text(), "retained\n")

    def test_wrong_interpreter_input_does_not_start_or_consume_attempt(self):
        with patch.object(check, "ROOT", self.root), self.assertRaises(OSError):
            check.run_cell(self.root / "build/new", self.root / "evidence/install-support/new",
                           self.root / "missing-python", self.root / "kit", self.root / "missing-wheel")
        self.assertEqual(self.tree(), {})

    def update_fixture(self, mutation=None):
        original = self.root / "evidence/successor-acceptance/20261109/maintainer-01/project"
        old_kit = original / ".agents/skills/pixl-kit"
        current_kit = self.root / "current kit"
        for kit, content in ((old_kit, b"old"), (current_kit, b"new")):
            kit.mkdir(parents=True)
            (kit / "runtime.py").write_bytes(content)
            (kit / "bundle-manifest.json").write_text(json.dumps({"files": [
                {"path": "runtime.py", "sha256": hashlib.sha256(content).hexdigest()}]}))
        (original / "state.px").write_bytes(b"unchanged")
        work, evidence = self.root / "build/attempt", self.root / "output"
        work.mkdir(parents=True)
        evidence.mkdir()
        report = {"state": {"revision": 126}, "comparison_coverage": {"complete": True}}
        class Reads:
            def json(self, label, args):
                value = copy.deepcopy(report)
                if "new-kit" in label:
                    value["hash_domains"] = {"state.sha256": "canonical_state_sha256"}
                    if mutation == "nonkit":
                        (work / "retained consumer/new-file").write_text("unexpected write")
                    elif mutation == "retired":
                        (work / "retired original kit/runtime.py").write_bytes(b"drift")
                return value
        return Reads(), current_kit, work, evidence

    def test_update_receipt_points_to_preserved_old_manifest(self):
        commands, kit, work, evidence = self.update_fixture()
        with patch.object(check, "ROOT", self.root):
            result = check.retained_update(commands, Path(sys.executable), kit, work, evidence)
        self.assertEqual(Path(result["old_manifest"]["path"]), work / "retired original kit/bundle-manifest.json")
        self.assertEqual(check.digest(result["old_manifest"]["path"]), result["old_manifest"]["sha256"])
        self.assertTrue(result["old_kit_preserved"])

    def test_read_only_update_rejects_new_nonkit_file(self):
        commands, kit, work, evidence = self.update_fixture("nonkit")
        with patch.object(check, "ROOT", self.root), self.assertRaisesRegex(RuntimeError, "non-kit"):
            check.retained_update(commands, Path(sys.executable), kit, work, evidence)

    def test_update_cannot_pass_when_retired_kit_drifts(self):
        commands, kit, work, evidence = self.update_fixture("retired")
        with patch.object(check, "ROOT", self.root), self.assertRaisesRegex(RuntimeError, "Original kit"):
            check.retained_update(commands, Path(sys.executable), kit, work, evidence)

    def test_runtime_inventory_catches_non_reporter_module_drift(self):
        runtime = self.root / "runtime"
        runtime.mkdir()
        (runtime / "readiness.py").write_text("unchanged reporter")
        (runtime / "jobs.py").write_text("original jobs")
        expected = check.runtime_payload(runtime)
        (runtime / "jobs.py").write_text("different jobs")
        actual = check.runtime_payload(runtime)
        self.assertEqual(actual["readiness.py"], expected["readiness.py"])
        self.assertNotEqual(actual, expected)

    def test_library_discovery_cannot_fall_back_to_checkout_with_equal_bytes(self):
        kit = self.root / "kit"
        resources = kit / "resources"
        example = resources / "examples/plar-project"
        runtime = kit / "runtime/pixl"
        example.mkdir(parents=True)
        runtime.mkdir(parents=True)
        (example / "BRIEF.md").write_text("same source bytes\n")
        for name in ("readiness.py", "production_plan.py", "jobs.py"):
            (runtime / name).write_text(name)
        source_digest = check.digest(example / "BRIEF.md")
        class Calls:
            def json(self, label, args):
                if args[0] == "readiness":
                    return {"local_operations": {"runtime_requirements": "satisfied"},
                            "installation": {"kind": "plugin"}, "reporter": {"module": str(runtime / "readiness.py")}}
                if args[0] == "source":
                    return {"sha256": source_digest}
                return {"root": str(resources.parent / "checkout fallback"), "files_verified": True,
                        "documents": [{"path": "BRIEF.md", "sha256": source_digest}]}
        with self.assertRaisesRegex(RuntimeError, "library root"):
            check.useful_route(Calls(), [], self.root / "consumer", resources, "probe",
                               check.runtime_payload(runtime), kit)


if __name__ == "__main__":
    unittest.main()
