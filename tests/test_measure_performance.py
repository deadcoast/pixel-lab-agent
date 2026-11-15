"""Maintainer measurements preserve results, expected refusals and input identity."""

import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pixl import codec, service
from scripts import measure_performance as benchmark
from tests.family_support import family


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="pixl-measurement-")
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.root = self.workspace / "consumer"
        self.root.mkdir()
        family(self.root)
        self.manifest = self.workspace / "manifest.json"
        self.case = {"id": "retained-fixture", "root": str(self.root), "path": ".pixl/state.px",
                     "focus": "delivery.task", "output_id": "delivery.output"}
        self.save_manifest()

    def save_manifest(self, cases=None):
        self.manifest.write_bytes(benchmark.json_bytes({"version": 1, "cases": cases or [self.case]}))

    def test_statistics_use_raw_samples_and_nearest_rank(self):
        self.assertIsNone(benchmark.stats([]))
        self.assertEqual(benchmark.stats([40, 10, 30, 20]), {
            "count": 4, "min_ns": 10, "max_ns": 40, "median_ns": 25, "p95_ns": 40})
        self.assertEqual(benchmark.stats(list(range(1, 21)))["p95_ns"], 19)

    def test_operation_timer_excludes_json_serialization(self):
        value = {"message": "pixel \u00e9", "hash_domains": {"hash": "canonical_state_sha256"}}
        with patch.object(benchmark.time, "perf_counter_ns", side_effect=[100, 400, 500, 700]):
            row = benchmark.observe(lambda: value, codec, public=True)
        expected = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        self.assertEqual(row["elapsed_ns"], 300)
        self.assertEqual(row["serialization_ns"], 200)
        self.assertEqual(row["outcome"]["sha256"], benchmark.sha(expected))
        self.assertEqual(row["outcome"]["bytes"], len(expected))

    def test_expected_refusal_is_retained_and_unexpected_success_fails(self):
        def refused():
            raise codec.PixlError("file_hash", "source: source.txt")

        report = benchmark.measure(refused, codec, 1, 2, ["file_hash"], public=True)
        self.assertEqual(report["status"], "observed_expected_refusal")
        self.assertEqual(len(report["warmups"]), 1)
        self.assertEqual(len(report["samples"]), 2)
        self.assertEqual(report["samples"][0]["outcome"], {
            "status": "refused", "code": "file_hash", "detail": "source: source.txt"})
        self.assertIsNone(report["serialization_timing"])
        self.assertEqual(benchmark.measure(refused, codec, 0, 1)["status"], "fail")
        self.assertEqual(benchmark.measure(dict, codec, 0, 1, ["file_hash"])["status"], "fail")

    def test_changed_results_and_unexpected_errors_fail(self):
        results = iter([{"version": 1}, {"version": 2}])
        report = benchmark.measure(lambda: next(results), codec, 0, 2)
        self.assertFalse(report["stable"])
        self.assertEqual(report["status"], "fail")

        def crash():
            raise RuntimeError("retained unexpected failure")

        report = benchmark.measure(crash, codec, 0, 1)
        self.assertEqual(report["status"], "fail")
        self.assertEqual(report["samples"][0]["outcome"]["detail"], "retained unexpected failure")

    def test_real_public_operations_and_child_preserve_inputs(self):
        before = benchmark.tree_identity(self.root)
        report = benchmark.run(self.manifest, warmups=1, iterations=2, fresh=1)
        self.assertEqual(report["status"], "pass", report)
        self.assertTrue(report["manifest_unchanged"])
        self.assertEqual(report["source_changes"], [])
        case = report["cases"][0]
        self.assertEqual(case["inputs"], before)
        self.assertEqual(benchmark.tree_identity(self.root), before)
        self.assertEqual(case["input_changes"], [])
        self.assertEqual(set(case["operations"]), benchmark.OPERATIONS)
        self.assertEqual(case["fresh_process_authoring"]["timing"]["count"], 1)
        self.assertGreater(case["fresh_process_authoring"]["samples"][0]["child"]["runtime_import_ns"], 0)
        for result in case["operations"].values():
            self.assertEqual(result["status"], "measured")
            self.assertEqual(result["timing"]["count"], 2)
            self.assertEqual(len(result["warmups"]), 1)
        complete = case["operations"]["complete_context"]["samples"][0]["outcome"]
        self.assertGreater(complete["bytes"], complete["wire_bytes"])
        public = service.call("pixl_family", {"path": self.case["path"], "output": "delivery.output"}, self.root)
        self.assertEqual(case["operations"]["family_report"]["samples"][0]["outcome"]["sha256"],
                         benchmark.sha(benchmark.json_bytes(public)))

    def test_real_changed_source_keeps_authoring_and_expected_validation_refusals(self):
        (self.root / "source.txt").write_text("A changed source, intentionally retained for this test.\n", encoding="utf-8")
        self.case["expected_errors"] = {name: ["file_hash"] for name in (
            "file_validation", "validate_report", "complete_context", "family_report")}
        self.save_manifest()
        report = benchmark.run(self.manifest, warmups=0, iterations=1, fresh=0)
        self.assertEqual(report["status"], "pass", report)
        operations = report["cases"][0]["operations"]
        self.assertEqual(operations["authoring_context"]["status"], "measured")
        self.assertEqual(operations["file_validation"]["status"], "observed_expected_refusal")
        self.assertEqual(operations["file_validation"]["samples"][0]["outcome"]["code"], "file_hash")

    def test_new_file_during_measurement_is_detected(self):
        original = benchmark.measure
        written = False

        def mutate_then_measure(*args, **kwargs):
            nonlocal written
            if not written:
                (self.root / "unexpected.txt").write_bytes(b"changed during run")
                written = True
            return original(*args, **kwargs)

        with patch.object(benchmark, "measure", side_effect=mutate_then_measure):
            report = benchmark.run(self.manifest, warmups=0, iterations=1, fresh=0)
        self.assertEqual(report["status"], "fail")
        self.assertIn("unexpected.txt", report["cases"][0]["input_changes"])

    def test_same_size_same_mtime_content_drift_is_detected(self):
        path = self.root / "unchanged-size.txt"
        path.write_bytes(b"first")
        before = benchmark.tree_identity(self.root)
        stat = path.stat()
        path.write_bytes(b"other")
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        self.assertIn(path.name, benchmark.changed(before, benchmark.tree_identity(self.root)))

    def test_removed_manifest_retains_measurements_and_fails_preservation(self):
        original = benchmark.fresh_processes

        def remove_after_measurement(*args, **kwargs):
            result = original(*args, **kwargs)
            self.manifest.unlink()
            return result

        with patch.object(benchmark, "fresh_processes", side_effect=remove_after_measurement):
            report = benchmark.run(self.manifest, warmups=0, iterations=1, fresh=0)
        self.assertEqual(report["status"], "fail")
        self.assertFalse(report["manifest_unchanged"])
        self.assertEqual(report["preservation_errors"][0]["scope"], "manifest")
        self.assertEqual(report["cases"][0]["operations"]["authoring_context"]["status"], "measured")

    def test_manifest_rejects_escape_duplicate_ids_and_unused_expectations(self):
        for update in ({"path": "../state.px"}, {"path": str(self.root / ".pixl/state.px")},
                       {"path": ".pixl\\state.px"}, {"expected_errors": {"typo": ["file_hash"]}}):
            with self.subTest(update=update):
                self.save_manifest([{**self.case, **update}])
                with self.assertRaises(ValueError):
                    benchmark.read_manifest(self.manifest)
        self.save_manifest([self.case, self.case])
        with self.assertRaises(ValueError):
            benchmark.read_manifest(self.manifest)
        no_family = {key: value for key, value in self.case.items() if key != "output_id"}
        no_family["expected_errors"] = {"family_report": ["file_hash"]}
        self.save_manifest([no_family])
        with self.assertRaises(ValueError):
            benchmark.read_manifest(self.manifest)

    def test_cli_invalid_configuration_is_json_and_nonzero(self):
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run([sys.executable, "-B", str(Path(benchmark.__file__).resolve()),
                                 "--manifest", str(self.manifest), "--iterations", "0"],
                                capture_output=True, env=environment, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, b"")
        self.assertEqual(json.loads(result.stdout)["status"], "configuration_error")

    def test_child_invalid_json_retains_actual_process_output(self):
        real_run = subprocess.run
        for raw in (b"not-json retained diagnostic\xff\n", b"[]", b'{"outcome":{"status":"refused"}}'):
            with self.subTest(raw=raw):
                def malformed_child(_command, raw=raw, **kwargs):
                    return real_run([sys.executable, "-B", "-c",
                                     f"import sys; sys.stdout.buffer.write({raw!r})"], **kwargs)

                with patch.object(benchmark.subprocess, "run", side_effect=malformed_child):
                    report = benchmark.fresh_processes(self.manifest, self.case, 1, 5)
                self.assertEqual(report["status"], "fail")
                outcome = report["samples"][0]["outcome"]
                self.assertEqual(outcome["exit_code"], 0)
                self.assertEqual(base64.b64decode(outcome["stdout_base64"]), raw)
                self.assertEqual(base64.b64decode(outcome["stderr_base64"]), b"")

    def test_child_timeout_retains_partial_stdout_and_stderr_bytes(self):
        stdout, stderr = b"partial diagnostic\xff", b"partial error\xfe"
        error = subprocess.TimeoutExpired(["probe"], 1, output=stdout, stderr=stderr)
        with patch.object(benchmark.subprocess, "run", side_effect=error):
            report = benchmark.fresh_processes(self.manifest, self.case, 1, 1)
        self.assertEqual(report["status"], "fail")
        outcome = report["samples"][0]["outcome"]
        self.assertEqual(outcome["type"], "TimeoutExpired")
        self.assertEqual(outcome["output_encoding"], "base64 of exact captured bytes")
        self.assertEqual(base64.b64decode(outcome["stdout_base64"]), stdout)
        self.assertEqual(base64.b64decode(outcome["stderr_base64"]), stderr)


if __name__ == "__main__":
    unittest.main()
