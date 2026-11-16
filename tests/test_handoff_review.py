"""Literal coverage catches omissions without declaring source meaning correct."""

import copy
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from pixl.codec import PixlError
from pixl.handoff_review import main, report

REPO = Path(__file__).resolve().parents[1]


def snapshot(root):
    return {
        path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
        for path in root.rglob("*") if path.is_file()
    }


class HandoffReviewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.value = {
            "questions": [
                {"unlocks": "Draft a contract."},
                {"unlocks": "Choose a review scale."},
                {"unlocks": "Only plan the family."},
            ],
            "next": {"operation": "Prepare locally", "ready": False},
            "history": {"unlocks": "Outside the declared scope"},
        }
        self.scopes = ["/questions", "/next"]
        self.save("result.json", self.value)
        self.source = (
            "Planning is local; production still needs its other prerequisites.\r\n"
            "Review may use a specialist background fallback.\r\n"
            "The scale remains required.\r\n"
        )
        (self.root / "note.md").write_bytes(self.source.encode())
        citation = {"path": "note.md", "sha256": self.digest("note.md"), "lines": [1, 3]}
        pairs = [
            ("/questions/0/unlocks", "Draft a contract."),
            ("/questions/1/unlocks", "Choose a review scale."),
            ("/questions/2/unlocks", "Only plan the family."),
            ("/next/operation", "Prepare locally"),
            ("/next/ready", False),
        ]
        self.review = {
            "version": 1,
            "result": {"path": "result.json", "sha256": self.digest("result.json")},
            "scopes": self.scopes[:],
            "claims": [
                {"pointer": pointer, "expected": value, "basis": "source_comparison",
                 "finding": "The operation remains preparation; other production prerequisites persist.",
                 "sources": [copy.deepcopy(citation)]}
                for pointer, value in pairs
            ],
            "carriers": [{**citation, "text": self.source}],
        }

    def digest(self, name):
        return hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def save(self, name, value):
        (self.root / name).write_text(json.dumps(value), encoding="utf-8")

    def checked(self):
        self.save("review.json", self.review)
        return report(self.root, "result.json", self.scopes, "review.json")

    def cli(self, *extra):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(["result.json", "--root", str(self.root),
                         "--scope", "/questions", "--scope", "/next", *extra])
        return code, out.getvalue(), err.getvalue()

    def test_inventory_is_independent_of_rows_and_covers_later_questions(self):
        result = report(self.root, "result.json", self.scopes)
        self.assertEqual(result["status"], "inventory")
        self.assertIsNone(result["coverage"])
        self.assertEqual(result["semantic_verdict"], "not_assessed")
        self.assertEqual([item["pointer"] for item in result["inventory"]], [
            "/next/operation", "/next/ready", "/questions/0/unlocks",
            "/questions/1/unlocks", "/questions/2/unlocks",
        ])
        self.review["claims"].pop(2)
        checked = self.checked()
        self.assertEqual(checked["status"], "coverage_incomplete")
        self.assertEqual(checked["coverage"]["missing"], ["/questions/2/unlocks"])
        self.assertEqual(len(checked["inventory"]), 5)

    def test_complete_but_wrong_review_does_not_get_semantic_pass(self):
        self.value["questions"][2]["unlocks"] = "All production gates clear now."
        self.save("result.json", self.value)
        self.review["result"]["sha256"] = self.digest("result.json")
        self.review["claims"][2]["expected"] = "All production gates clear now."
        self.review["claims"][2]["finding"] = "The limited answers authorize all production."
        result = self.checked()
        self.assertEqual(result["status"], "coverage_complete")
        self.assertTrue(result["coverage"]["complete"])
        self.assertEqual(result["semantic_verdict"], "not_assessed")
        self.assertNotIn("accepted", result)
        self.assertNotIn("owner_confirmation", result)
        self.assertIn("not prove source support", " ".join(result["limits"]))

    def test_file_binding_changes_even_when_saved_values_do_not(self):
        (self.root / "result.json").write_bytes((self.root / "result.json").read_bytes() + b"\n")
        result = self.checked()
        self.assertFalse(result["coverage"]["result_current"])
        self.assertEqual(result["coverage"]["changed_values"], [])
        self.assertEqual(result["status"], "coverage_incomplete")

    def test_changed_expected_and_duplicate_unexpected_pointers_are_explicit(self):
        self.review["claims"][0]["expected"] = "Proceed with production."
        self.review["claims"].append(copy.deepcopy(self.review["claims"][1]))
        extra = copy.deepcopy(self.review["claims"][2])
        extra["pointer"] = "/history/unlocks"
        self.review["claims"].append(extra)
        coverage = self.checked()["coverage"]
        self.assertEqual(coverage["changed_values"], ["/questions/0/unlocks"])
        self.assertEqual(coverage["duplicates"], ["/questions/1/unlocks"])
        self.assertEqual(coverage["unexpected"], ["/history/unlocks"])
        self.assertFalse(coverage["complete"])

    def test_literal_comparison_distinguishes_bool_integer_and_decimal(self):
        for actual, expected in [(True, 1), (False, 0), (1, 1.0)]:
            with self.subTest(actual=actual, expected=expected):
                self.value["next"]["ready"] = actual
                self.save("result.json", self.value)
                self.review["result"]["sha256"] = self.digest("result.json")
                self.review["claims"][4]["expected"] = expected
                self.assertEqual(self.checked()["coverage"]["changed_values"], ["/next/ready"])

    def test_nonempty_findings_sources_and_explicit_metadata_distinction(self):
        self.review["claims"][0]["finding"] = "  "
        self.review["claims"][1]["sources"] = []
        self.review["claims"][4].update(basis="metadata", sources=[])
        coverage = self.checked()["coverage"]
        self.assertEqual(coverage["metadata_pointers"], ["/next/ready"])
        self.assertEqual(coverage["incomplete"], [
            {"pointer": "/questions/0/unlocks", "issues": ["missing_finding"]},
            {"pointer": "/questions/1/unlocks", "issues": ["missing_source"]},
        ])
        self.review["claims"][0]["basis"] = "metadata"
        issues = self.checked()["coverage"]["incomplete"][0]["issues"]
        self.assertIn("metadata_must_not_claim_source_comparison", issues)

    def test_explicit_metadata_can_complete_coverage_without_source_authority(self):
        self.review["claims"][4].update(basis="metadata", sources=[])
        result = self.checked()
        self.assertTrue(result["coverage"]["complete"])
        self.assertEqual(result["coverage"]["metadata_pointers"], ["/next/ready"])
        self.assertEqual(result["semantic_verdict"], "not_assessed")

    def test_pointer_escaping_arrays_and_empty_containers(self):
        self.save("result.json", {"a/b": {"~": [{"": None}, {}, []]}})
        result = report(self.root, "result.json", ["/a~1b/~0"])
        self.assertEqual(result["inventory"], [
            {"pointer": "/a~1b/~0/0/", "value": None},
            {"pointer": "/a~1b/~0/1", "value": {}},
            {"pointer": "/a~1b/~0/2", "value": []},
        ])
        self.assertEqual(report(self.root, "result.json", [""])["inventory"], result["inventory"])

    def test_invalid_missing_duplicate_and_overlapping_scopes_are_refused(self):
        for scopes in ([], None, "questions", ["questions"], ["/questions/~2"],
                       ["/missing"], ["/next/ready/child"], ["/questions/01"],
                       ["/questions/3"], ["/questions", "/questions"],
                       ["/questions/0", "/questions"], ["", "/next"]):
            with self.subTest(scopes=scopes), self.assertRaises(PixlError):
                report(self.root, "result.json", scopes)

    def test_declared_review_scopes_must_match_external_inventory_scope(self):
        self.review["scopes"] = ["/questions"]
        result = self.checked()
        self.assertFalse(result["coverage"]["scopes_current"])
        self.assertEqual(result["coverage"]["expected"], 5)
        self.assertFalse(result["coverage"]["complete"])

    def test_changed_and_missing_source_remain_unresolved(self):
        (self.root / "note.md").write_text("Replaced source", encoding="utf-8")
        result = self.checked()
        self.assertEqual(result["comparisons"][0]["source_observations"][0]["status"], "changed")
        self.assertFalse(result["coverage"]["complete"])
        self.review["claims"][0]["sources"][0]["path"] = "absent.md"
        result = self.checked()
        self.assertEqual(result["comparisons"][0]["source_observations"][0]["status"], "missing")

    def test_exact_carrier_text_includes_line_endings(self):
        self.review["carriers"][0]["text"] = self.source.replace("\r\n", "\n")
        result = self.checked()
        self.assertEqual(result["coverage"]["carrier_mismatches"], [0])
        self.assertEqual(result["carriers"][0]["status"], "resolved")
        self.assertFalse(result["carriers"][0]["text_matches"])
        self.review["carriers"] = []
        result = self.checked()
        self.assertTrue(result["coverage"]["complete"])
        self.assertEqual(result["coverage"]["declared_carriers"], 0)
        self.assertIn("omitted adopted instructions", " ".join(result["limits"]))

    def test_invalid_line_ranges_cannot_complete_source_or_carrier_coverage(self):
        for bounds in ([0, 1], [3, 2], [1, 4], [True, 2], [1], [1, "2"]):
            with self.subTest(bounds=bounds):
                self.review["claims"][0]["sources"][0]["lines"] = bounds
                self.review["carriers"][0]["lines"] = bounds
                result = self.checked()
                self.assertEqual(result["comparisons"][0]["source_observations"][0]["status"], "invalid_locator")
                self.assertFalse(result["coverage"]["complete"])
        self.review["carriers"][0]["lines"] = None
        self.review["carriers"][0]["locator"] = "line 1"
        with self.assertRaises(PixlError):
            self.checked()

    def test_json_duplicates_nonfinite_and_overflow_are_rejected(self):
        for raw in ('{"next": 1, "next": 2}', '{"next": NaN}',
                    '{"next": Infinity}', '{"next": 1e999}', '[}'):
            with self.subTest(raw=repr(raw)):
                (self.root / "result.json").write_text(raw, encoding="utf-8")
                with self.assertRaises(PixlError):
                    report(self.root, "result.json", [""])
        self.save("result.json", self.value)
        for raw in ('{"version": 1, "version": 1}', '{"version": 1e999}'):
            (self.root / "review.json").write_text(raw, encoding="utf-8")
            with self.assertRaises(PixlError):
                report(self.root, "result.json", self.scopes, "review.json")

    def test_input_and_source_paths_reject_traversal_and_absolute_paths(self):
        for name in ("../result.json", "child/../result.json", "C:/result.json", "child\\result.json"):
            with self.subTest(name=name), self.assertRaises(PixlError):
                report(self.root, name, self.scopes)
        self.review["claims"][0]["sources"][0]["path"] = "../note.md"
        with self.assertRaises(PixlError):
            self.checked()

    def test_symlink_sources_and_outputs_cannot_escape_consumer_root(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside)
            (target / "note.md").write_text(self.source, encoding="utf-8")
            link = self.root / "linked"
            try:
                link.symlink_to(target, target_is_directory=True)
            except OSError as error:
                if sys.platform != "win32":
                    self.skipTest(f"Directory symlink unavailable: {error}")
                junction = subprocess.run(
                    ["cmd", "/c", "mklink", "/J", str(link), str(target)],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(junction.returncode, 0, junction.stderr)
            self.review["claims"][0]["sources"][0]["path"] = "linked/note.md"
            with self.assertRaises(PixlError):
                self.checked()
            code, _, error = self.cli("--out", "linked/report.json")
            self.assertEqual(code, 2)
            self.assertIn("error", json.loads(error))
            self.assertFalse((target / "report.json").exists())

    def test_read_only_api_preserves_all_input_bytes_and_mtimes(self):
        self.save("review.json", self.review)
        before = snapshot(self.root)
        result = report(self.root, "result.json", self.scopes, "review.json")
        self.assertEqual(result["status"], "coverage_complete")
        self.assertEqual(snapshot(self.root), before)

    def test_cli_stdout_errors_and_exclusive_output_preserve_inputs(self):
        self.save("review.json", self.review)
        before = snapshot(self.root)
        code, output, error = self.cli("--review", "review.json")
        self.assertEqual((code, error), (0, ""))
        self.assertEqual(json.loads(output)["status"], "coverage_complete")
        for name in ("result.json", "review.json", "note.md", "../report.json", "missing/report.json"):
            with self.subTest(name=name):
                code, output, error = self.cli("--out", name)
                self.assertEqual((code, output), (2, ""))
                self.assertEqual(json.loads(error)["semantic_verdict"], "not_assessed")
                self.assertNotIn("Traceback", error)
        self.assertEqual(snapshot(self.root), before)
        code, output, error = self.cli("--out", "report.json")
        self.assertEqual((code, output, error), (0, "", ""))
        self.assertEqual(json.loads((self.root / "report.json").read_text())["status"], "inventory")
        self.review["claims"].pop()
        self.save("review.json", self.review)
        code, output, error = self.cli("--review", "review.json")
        self.assertEqual((code, error), (1, ""))
        self.assertEqual(json.loads(output)["status"], "coverage_incomplete")

    def test_relocated_launcher_uses_its_runtime_and_leaves_kit_read_only(self):
        kit = self.root / "relocated-kit"
        (kit / "scripts").mkdir(parents=True)
        shutil.copy2(REPO / "plugins/pixl/scripts/check_handoff.py", kit / "scripts/check_handoff.py")
        shutil.copytree(REPO / "pixl", kit / "runtime/pixl", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        consumer = self.root / "consumer"
        consumer.mkdir()
        (consumer / "pixl").mkdir()
        (consumer / "pixl/__init__.py").write_text("raise RuntimeError('Wrong runtime')", encoding="utf-8")
        (consumer / "result.json").write_text(json.dumps(self.value), encoding="utf-8")
        before = snapshot(self.root)
        result = subprocess.run(
            [sys.executable, "-I", str(kit / "scripts/check_handoff.py"),
             "result.json", "--root", str(consumer), "--scope", "/questions", "--scope", "/next"],
            cwd=consumer, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "inventory")
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(list(kit.rglob("__pycache__")), [])

    def test_module_entrypoint_reports_inventory_and_refusals_without_traceback(self):
        before = snapshot(self.root)
        for scope, expected_code in (("/questions", 0), ("/missing", 2)):
            with self.subTest(scope=scope):
                result = subprocess.run(
                    [sys.executable, "-B", "-m", "pixl.handoff_review", "result.json",
                     "--root", str(self.root), "--scope", scope],
                    cwd=REPO, capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, expected_code, result.stderr)
                body = json.loads(result.stderr if expected_code else result.stdout)
                self.assertEqual(body["semantic_verdict"], "not_assessed")
                self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(snapshot(self.root), before)


if __name__ == "__main__":
    unittest.main()
