"""Fixed-profile orchestration tests; synthetic reports do not prove rendering."""

import copy
import hashlib
import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, store
from pixl import consumer_execution as execution
from pixl.codec import PixlError, Ref
from tests.test_destination_observation import observation_fixture


def execution_fixture(root):
    """Return (state_path, config) for current family candidate 'package'."""
    root = Path(root)
    _, report = observation_fixture(root)
    (root / "src").mkdir()
    (root / "assets").mkdir()
    for row in report["destinations"]:
        old = root / row["path"]
        row["path"] = "assets/" + old.name
        (root / row["path"]).write_bytes(old.read_bytes())
    (root / "capture/observation.json").write_text(json.dumps(report), encoding="utf-8")
    (root / "src/state.mjs").write_text("export const synthetic = true;\n", encoding="utf-8")
    (root / "src/view.mjs").write_text("export const view = 'synthetic';\n", encoding="utf-8")
    config = {"version": 1, "profile": "queue-motion-v1", "modules": {"state": "src/state.mjs", "view": "src/view.mjs"},
              "destinations": {row["output"]: row["path"] for row in report["destinations"]},
              "scales": [1, 3], "observed_wraps": 2, "phase_timeout_ms": 1000, "hold_ms": 100,
              "timeout_seconds": 10}
    return root / ".pixl/state.px", config


CAPTURE = '''import json, pathlib, sys
args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
root = pathlib.Path(args['--project'])
out = pathlib.Path(args['--out'])
out.mkdir()
(out / 'partial.txt').write_text('retained synthetic capture', encoding='utf-8')
(out / 'capture.json').write_text(json.dumps({'synthetic': True}), encoding='utf-8')
(out / 'execution.json').write_text(json.dumps({'status': 'complete', 'renderer_executed': True, 'cleanup': {'complete': True}}), encoding='utf-8')
'''
CHECK = '''import json, pathlib, sys
args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
pathlib.Path(args['--out']).write_text(json.dumps({'status': 'pass', 'pass': True, 'facts': {'pixel_checks': 1, 'source_checks': 2, 'clock_checks': 3, 'phases': {}}, 'limitations': ['synthetic test']}), encoding='utf-8')
'''
BRIDGE = '''import hashlib, json, pathlib, sys
args = dict(zip(sys.argv[1::2], sys.argv[2::2]))
root = pathlib.Path(args['--project'])
value = json.loads((root / 'capture/observation.json').read_bytes())
def ref(path):
    return {'path': path.relative_to(root).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
value['renderer']['files'] = [ref(p) for p in sorted(pathlib.Path(args['--renderer']).iterdir())]
value['consumer_sources'] = [ref(p) for p in sorted((root / 'src').rglob('*')) if p.is_file()]
pathlib.Path(args['--out']).write_text(json.dumps(value), encoding='utf-8')
'''


class ConsumerExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state, self.config = execution_fixture(self.root)
        self.before = self.state.read_bytes()
        self.resources = self.root / "synthetic-resources"
        self.profile = self.resources / "examples/consumer-execution/queue-motion"
        self.profile.mkdir(parents=True)
        self.scripts = {"capture.mjs": CAPTURE, "check.py": CHECK, "observation.py": BRIDGE,
                        "server.mjs": "// synthetic\n", "view.mjs": "// synthetic\n", "index.html": "synthetic\n"}
        for name, data in self.scripts.items():
            (self.profile / name).write_text(data, encoding="utf-8")
        self.addCleanup(patch.stopall)
        patch.object(execution.service, "resource_root", return_value=self.resources).start()
        real_run = execution._run
        self.real_run = real_run
        def synthetic_node(argv, root, directory, name, deadline):
            # This fixture runs Python scripts, not a real Node/browser renderer.
            if name == "node-capabilities":
                argv = [sys.executable, "-c", "print('synthetic Node capability test double')"]
            return real_run(argv, root, directory, name, deadline)
        patch.object(execution, "_run", side_effect=synthetic_node).start()

    def run_execution(self, **kwargs):
        return execution.execute(self.state, self.root, "package", self.config, kwargs.pop("out", "runs/one"),
                                 node=kwargs.pop("node", sys.executable), **kwargs)

    def script(self, name, text):
        (self.profile / name).write_text(text, encoding="utf-8")

    def retained(self, result):
        self.assertEqual(json.loads((self.root / result["result_path"]).read_bytes()), result)
        self.assertEqual(self.state.read_bytes(), self.before)
        self.assertFalse(result["state_written"])
        self.assertFalse(result["automatic_acceptance"])

    def test_synthetic_pipeline_retains_importable_archive_without_acceptance(self):
        result = self.run_execution()
        self.assertEqual(result["status"], "complete", result)
        self.assertTrue(result["files_verified"])
        self.assertTrue(result["renderer_executed"])
        self.assertEqual(result["observation"]["mode"], "live")
        self.assertTrue((self.root / result["bundle"]["path"]).is_file())
        self.assertNotIn("supplied_observations", result)
        self.assertNotIn("previews", result)
        self.assertEqual(len(result["phases"]), 5)
        self.assertEqual(result["check_summary"]["pixel_checks"], 1)
        self.assertEqual(result["timeout_scope"], "subprocesses")
        self.assertEqual(result["requested_inputs"]["config.json"], result["artifacts"]["config.json"])
        receipt = json.loads((self.root / "runs/one/execution/capture.json").read_bytes())
        self.assertEqual(receipt["argv"][0], str(Path(sys.executable).resolve()))
        self.assertEqual(receipt["returncode"], 0)
        self.assertTrue(receipt["cleanup"]["process_reaped"])
        self.assertTrue((self.root / "runs/one/renderer-sources.json").is_file())
        self.retained(result)

    def test_closed_config_and_exact_integer_bounds_refuse_before_launch(self):
        invalid = [{**self.config, "arbitrary_command": "echo wrong"}, {**self.config, "version": True},
                   {**self.config, "timeout_seconds": 5.0}, {**self.config, "scales": [1, 1]},
                   {**self.config, "scales": [True]}, {**self.config, "scales": []},
                   {**self.config, "modules": {"state": "src/state.mjs", "view": "../outside.mjs"}},
                   {**self.config, "destinations": {"output": "other/path.png"}},
                   {k: v for k, v in self.config.items() if k != "hold_ms"}]
        with patch.object(execution, "_run") as run:
            for config in invalid:
                with self.subTest(config=config), self.assertRaises(PixlError):
                    execution.execute(self.state, self.root, "package", config, "runs/refused")
            run.assert_not_called()
        self.assertFalse((self.root / "runs").exists())

    def test_historical_package_is_rejected_before_launch(self):
        folder = self.state.parent
        doc = store.load(folder)
        expect = codec.digest(doc)
        doc.records["delivery.output"].fields["mb"] = [Ref("output")]
        doc.revision += 1
        store.commit(folder, doc, expect, self.root)
        with patch.object(execution, "_run") as run, self.assertRaisesRegex(PixlError, "not current"):
            self.run_execution()
        run.assert_not_called()
        self.assertFalse((self.root / "runs").exists())

    def test_package_map_and_destination_mismatch_refuse_before_launch(self):
        first = next(iter(self.config["destinations"]))
        bad = copy.deepcopy(self.config)
        bad["destinations"].pop(first)
        with self.assertRaisesRegex(PixlError, "every manifest member"):
            execution.execute(self.state, self.root, "package", bad, "runs/refused")
        (self.root / self.config["destinations"][first]).write_bytes(b"wrong delivered bytes")
        with self.assertRaisesRegex(PixlError, "differs from package"):
            self.run_execution()
        self.assertFalse((self.root / "runs").exists())

    def test_existing_or_noncanonical_output_preserves_existing_files(self):
        directory = self.root / "runs/one"
        directory.mkdir(parents=True)
        (directory / "keep").write_bytes(b"old failed attempt")
        with patch.object(execution, "_run") as run:
            for out in ("runs/one", "../outside", "src/run", ".pixl/run", "runs//other"):
                with self.subTest(out=out), self.assertRaises(PixlError):
                    self.run_execution(out=out)
            run.assert_not_called()
        self.assertEqual((directory / "keep").read_bytes(), b"old failed attempt")

    def test_missing_node_and_browser_retain_unavailable_no_launch(self):
        with patch.object(execution, "_run") as run:
            for index, kwargs in enumerate(({"node": str(self.root / "missing-node")},
                                             {"browser": str(self.root / "missing-browser")})):
                result = self.run_execution(out=f"runs/unavailable-{index}", **kwargs)
                self.assertEqual(result["status"], "unavailable")
                self.assertFalse(result["renderer_executed"])
                self.assertIsNone(result["observation"])
                self.retained(result)
            run.assert_not_called()

    def test_missing_installed_profile_retains_unavailable(self):
        (self.profile / "server.mjs").unlink()
        result = self.run_execution()
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["error"]["code"], "consumer_profile")
        self.assertTrue((self.root / "runs/one/renderer/capture.mjs").exists())
        self.retained(result)

    def test_unsupported_node_capabilities_retained_as_unavailable(self):
        real = execution._run
        def unsupported(argv, root, directory, name, deadline):
            if name == "node-capabilities":
                argv = [sys.executable, "-c", "import sys; sys.exit(3)"]
                return self.real_run(argv, root, directory, name, deadline)
            return real(argv, root, directory, name, deadline)
        with patch.object(execution, "_run", side_effect=unsupported):
            result = self.run_execution()
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["error"]["code"], "consumer_capability")
        self.assertFalse(result["process_started"])
        self.retained(result)

    def test_nonzero_capture_preserves_partial_files_and_logs(self):
        self.script("capture.mjs", CAPTURE + "print('failure diagnostic', file=sys.stderr)\nsys.exit(7)\n")
        result = self.run_execution()
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["phases"][-1]["returncode"], 7)
        self.assertEqual((self.root / "runs/one/capture/partial.txt").read_text(), "retained synthetic capture")
        self.assertIn("failure diagnostic", (self.root / "runs/one/execution/capture.stderr.log").read_text())
        self.assertFalse((self.root / "runs/one/import").exists())
        self.retained(result)

    def test_unavailable_renderer_is_not_an_art_failure(self):
        self.script("capture.mjs", CAPTURE + "(out / 'execution.json').write_text(json.dumps({'status':'unavailable','renderer_executed':False,'cleanup':{'complete':True}}))\nsys.exit(2)\n")
        result = self.run_execution()
        self.assertEqual(result["status"], "unavailable")
        self.assertIsNone(result["observation"])
        self.assertFalse(result["renderer_executed"])
        self.retained(result)

    def test_missing_cleanup_confirmation_is_partial_without_import(self):
        self.script("capture.mjs", CAPTURE + "(out / 'execution.json').unlink()\n")
        result = self.run_execution()
        self.assertEqual(result["status"], "partial")
        self.assertIsNone(result["observation"])
        self.assertFalse((self.root / "runs/one/import").exists())
        self.retained(result)

    def test_failed_checker_never_creates_review_observation(self):
        self.script("check.py", CHECK.replace("'status': 'pass', 'pass': True", "'status': 'fail', 'pass': False"))
        result = self.run_execution()
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["error"]["code"], "consumer_check")
        self.assertIsNone(result["observation"])
        self.retained(result)

    def test_bridge_report_mismatch_retains_report_without_import(self):
        self.script("observation.py", BRIDGE.replace("value['consumer_sources'] =", "value['binding_hash'] = '0' * 64\nvalue['consumer_sources'] ="))
        result = self.run_execution()
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["error"]["code"], "destination_binding")
        self.assertIn("observation.json", result["artifacts"])
        self.assertIsNone(result["observation"])
        self.retained(result)

    def test_generated_request_changes_stop_after_capture_and_preserve_original_hashes(self):
        changes = {
            "config.json": "value['observed_wraps'] = 1",
            "review-context.json": "value['binding_hash'] = '0' * 64",
            "destinations.json": "value[next(iter(value))] = 'assets/unrequested.png'",
        }
        for index, (name, change) in enumerate(changes.items()):
            with self.subTest(name=name):
                self.script("capture.mjs", CAPTURE + f"target = out.parent / {name!r}\n"
                    "original = target.read_bytes()\n(out / 'original-request.json').write_bytes(original)\n"
                    "value = json.loads(original)\n" + change + "\ntarget.write_text(json.dumps(value))\n")
                result = self.run_execution(out=f"runs/request-{index}")
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["error"]["code"], "consumer_inputs_changed")
                self.assertIn(name, result["error"]["detail"])
                self.assertEqual([phase["phase"] for phase in result["phases"]],
                                 ["node-version", "node-capabilities", "capture"])
                self.assertTrue(result["process_started"])
                self.assertTrue(result["renderer_executed"])
                self.assertTrue(result["cleanup"]["renderer"]["complete"])
                original = (self.root / f"runs/request-{index}/capture/original-request.json").read_bytes()
                self.assertEqual(result["requested_inputs"][name]["sha256"], hashlib.sha256(original).hexdigest())
                self.assertNotEqual(result["requested_inputs"][name]["sha256"], result["artifacts"][name]["sha256"])
                self.assertIsNone(result["observation"])
                self.assertFalse((self.root / f"runs/request-{index}/import").exists())
                self.retained(result)

    def test_generated_request_changed_before_first_process_never_launches(self):
        real_write = execution._write
        def changed(path, value):
            real_write(path, value)
            if path.name == "executables.json":
                config = self.root / "runs/one/config.json"
                config.write_bytes(config.read_bytes() + b"\n")
        with patch.object(execution, "_write", side_effect=changed), patch.object(execution, "_run") as run:
            result = self.run_execution()
        run.assert_not_called()
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["phases"], [])
        self.assertFalse(result["process_started"])
        self.retained(result)

    def test_generated_request_changed_after_probe_stops_before_capture(self):
        real_run = execution._run
        def changed(argv, root, directory, name, deadline):
            receipt = real_run(argv, root, directory, name, deadline)
            if name == "node-version":
                config = directory / "config.json"
                config.write_bytes(config.read_bytes() + b"\n")
            return receipt
        with patch.object(execution, "_run", side_effect=changed):
            result = self.run_execution()
        self.assertEqual(result["status"], "failed")
        self.assertEqual([phase["phase"] for phase in result["phases"]], ["node-version"])
        self.assertFalse(result["process_started"])
        self.assertFalse(result["renderer_executed"])
        self.retained(result)

    def test_generated_request_changed_by_bridge_stops_before_import(self):
        self.script("observation.py", BRIDGE + "config = pathlib.Path(args['--out']).parent / 'config.json'\n"
                    "config.write_bytes(config.read_bytes() + b'\\n')\n")
        result = self.run_execution()
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["phases"][-1]["phase"], "observation")
        self.assertIsNone(result["observation"])
        self.assertFalse((self.root / "runs/one/import").exists())
        self.retained(result)

    def test_generated_request_changed_during_import_invalidates_ready_observation(self):
        real_import = execution.destination_observation.import_observation
        def changed(*args, **kwargs):
            imported = real_import(*args, **kwargs)
            config = self.root / "runs/one/config.json"
            config.write_bytes(config.read_bytes() + b"\n")
            return imported
        with patch.object(execution.destination_observation, "import_observation", side_effect=changed):
            result = self.run_execution()
        self.assertEqual(result["status"], "failed")
        self.assertIsNone(result["observation"])
        self.assertFalse(result["files_verified"])
        self.assertTrue((self.root / "runs/one/import/result.json").is_file())
        self.retained(result)

    def test_pipeline_timeout_retains_partial_and_parent_cleanup(self):
        self.script("capture.mjs", CAPTURE + "import time; time.sleep(60)\n")
        real = execution._run
        def timeout(argv, root, directory, name, deadline):
            return real(argv, root, directory, name, time.monotonic() + .3 if name == "capture" else deadline)
        with patch.object(execution, "_run", side_effect=timeout):
            result = self.run_execution()
        self.assertEqual(result["status"], "timeout")
        self.assertTrue(result["cleanup"]["process"]["attempted"])
        self.assertTrue(result["cleanup"]["process"]["process_reaped"])
        self.assertTrue((self.root / "runs/one/capture/partial.txt").is_file())
        self.assertIsNone(result["observation"])
        self.retained(result)

    def test_parent_cleanup_uncertainty_overrides_stale_renderer_receipt(self):
        self.script("capture.mjs", CAPTURE + "import time; time.sleep(60)\n")
        real_run, real_stop = execution._run, execution._stop_owned
        def timeout(argv, root, directory, name, deadline):
            return real_run(argv, root, directory, name, time.monotonic() + .3 if name == "capture" else deadline)
        def uncertain(process):
            receipt = real_stop(process)
            return {**receipt, "complete": False, "tree_confirmed": False, "error": "synthetic uncertainty after actual cleanup"}
        with patch.object(execution, "_run", side_effect=timeout), patch.object(execution, "_stop_owned", side_effect=uncertain):
            result = self.run_execution()
        self.assertEqual(result["status"], "timeout")
        self.assertFalse(result["cleanup"]["complete"])
        self.assertTrue(result["cleanup"]["renderer"]["complete"])
        self.retained(result)

    def test_transitive_source_destination_and_renderer_changes_are_detected(self):
        (self.root / "src/transitive.mjs").write_text("export default 1;", encoding="utf-8")
        changes = ["(root / 'src/transitive.mjs').write_text('changed')",
                   "next((root / 'assets').glob('served-*.png')).write_bytes(b'changed')",
                   "(pathlib.Path(__file__).parent / 'view.mjs').write_text('changed')"]
        for index, change in enumerate(changes):
            with self.subTest(change=change):
                self.script("capture.mjs", CAPTURE + change + "\n")
                result = self.run_execution(out=f"runs/changed-{index}")
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["error"]["code"], "consumer_inputs_changed")
                self.assertIsNone(result["observation"])
                self.retained(result)
                # Restore the exact fixture destination between independent attempts.
                if index == 1:
                    report = json.loads((self.root / "capture/observation.json").read_bytes())
                    context = json.loads((self.root / f"runs/changed-{index}/review-context.json").read_bytes())
                    for dest, member in zip(report["destinations"], context["members"], strict=True):
                        (self.root / dest["path"]).write_bytes((self.root / member["retained_path"]).read_bytes())

    def test_changed_state_is_reported_without_reverting_concurrent_writer(self):
        self.script("capture.mjs", CAPTURE + "state = root / '.pixl/state.px'\nstate.write_bytes(state.read_bytes() + b'\\n')\n")
        result = self.run_execution()
        self.assertEqual(result["status"], "failed")
        self.assertTrue(result["state_changed"])
        self.assertFalse(result["state_written"])
        self.assertEqual(self.state.read_bytes(), self.before + b"\n")
        self.assertIsNone(result["observation"])
        self.assertEqual(result, json.loads((self.root / result["result_path"]).read_bytes()))

    def test_keyboard_interrupt_retains_completed_phase_receipts(self):
        real = execution._run
        def interrupt(argv, root, directory, name, deadline):
            if name == "capture":
                raise KeyboardInterrupt
            return real(argv, root, directory, name, deadline)
        with patch.object(execution, "_run", side_effect=interrupt):
            result = self.run_execution()
        self.assertEqual(result["status"], "interrupted")
        self.assertEqual(result["phases"][0]["phase"], "node-version")
        self.retained(result)

    def test_execution_export_failure_retains_result_in_error(self):
        real = execution._write
        def fail_result(path, value):
            if path == self.root / "runs/one/result.json":
                raise OSError("synthetic write failure")
            return real(path, value)
        with patch.object(execution, "_write", side_effect=fail_result), self.assertRaises(PixlError) as caught:
            self.run_execution()
        self.assertEqual(caught.exception.code, "consumer_export")
        self.assertEqual(caught.exception.context["operation_result"]["status"], "complete")
        self.assertTrue((self.root / "runs/one/import/result.json").is_file())


class OwnedProcessTests(unittest.TestCase):
    def test_timeout_stops_owned_descendant_and_preserves_unrelated_process(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "execution").mkdir()
            child = "import pathlib,time; p=pathlib.Path('heartbeat'); [(p.write_text(str(i)),time.sleep(.05)) for i in range(1000)]"
            parent = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c'," + repr(child) + "]); time.sleep(60)"
            unrelated = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                **({"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}))
            try:
                result = execution._run([sys.executable, "-c", parent], root, root, "timeout", time.monotonic() + 1)
                self.assertEqual(result["status"], "timeout")
                self.assertTrue(result["cleanup"]["process_reaped"])
                before = (root / "heartbeat").read_text()
                time.sleep(.2)
                self.assertEqual((root / "heartbeat").read_text(), before)
                self.assertIsNone(unrelated.poll())
                self.assertTrue((root / "execution/timeout.json").is_file())
            finally:
                unrelated.terminate()
                unrelated.wait(timeout=5)

    def test_interrupted_wait_stops_real_owned_process(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "execution").mkdir()
            options = {"creationflags": subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
            process = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], **options)
            original_wait = process.wait
            waits = 0
            def wait(*args, **kwargs):
                nonlocal waits
                waits += 1
                if waits == 1:
                    raise KeyboardInterrupt
                return original_wait(*args, **kwargs)
            try:
                with patch.object(execution.subprocess, "Popen", return_value=process), patch.object(process, "wait", side_effect=wait):
                    # Windows taskkill uses subprocess.run, which also needs real Popen.
                    real_stop = execution._stop_owned
                    with patch.object(execution, "_stop_owned", side_effect=lambda p: self.stop_without_popen_patch(p, real_stop)):
                        result = execution._run([sys.executable, "-c", "unused"], root, root, "interrupt", time.monotonic() + 5)
                self.assertEqual(result["status"], "interrupted")
                self.assertTrue(result["cleanup"]["process_reaped"])
                self.assertIsNotNone(process.poll())
            finally:
                if process.poll() is None:
                    process.kill()
                    original_wait(timeout=5)

    @staticmethod
    def stop_without_popen_patch(process, stop):
        # Restore only Popen while terminating the real child; other patches stay active.
        with patch.object(execution.subprocess, "Popen", _REAL_POPEN):
            return stop(process)


_REAL_POPEN = subprocess.Popen


if __name__ == "__main__":
    unittest.main()
