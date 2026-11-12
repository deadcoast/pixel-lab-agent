"""Profile-specific contracts through the shared consumer execution pipeline.

Synthetic subprocess reports prove orchestration and retention, not rendering.
Real profile rendering has its own tests and retained consumer trials.
"""

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import consumer_execution as execution
from pixl import mcp, service
from pixl.codec import PixlError
from tests.test_consumer_execution import BRIDGE, CAPTURE, CHECK, execution_fixture

NEW_PROFILES = ("tile-neighborhood-v1", "sprite-animation-v1")


def profile_config(queue_config, profile):
    config = copy.deepcopy(queue_config)
    config["profile"] = profile
    if profile == "queue-motion-v1":
        return config
    del config["hold_ms"]
    if profile == "tile-neighborhood-v1":
        config["modules"] = {"terrain": "src/terrain.ts"}
        del config["observed_wraps"]
        del config["phase_timeout_ms"]
    else:
        config["modules"] = {"animation": "src/animation.ts"}
    return config


def checker_report(profile):
    facts = {"pixel_checks": 12, "source_checks": 2, "clock_checks": 0, "phases": {}}
    if profile == "sprite-animation-v1":
        facts.update(clock_checks=18, phases={"playback": {
            "status": "observed", "sample_count": 14,
            "counts": {"walk@1x": {"frames": [0, 1, 2], "transitions": 6, "wraps": 2, "skips": 0},
                       "land@3x": {"frames": [0, 1], "transitions": 1, "wraps": 0, "skips": 0}}}})
    return {"status": "pass", "pass": True, "facts": facts, "limitations": ["synthetic test"]}


class ConsumerProfileTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.state, self.queue_config = execution_fixture(self.root)
        self.initial = self.state.read_bytes()
        for name in ("terrain", "animation"):
            (self.root / f"src/{name}.ts").write_text(f"export const {name} = 'synthetic';\n", encoding="utf-8")
        self.resources = self.root / "synthetic-resources"
        for profile, directory in execution.PROFILE_RESOURCES.items():
            location = self.resources / "examples/consumer-execution" / directory
            location.mkdir(parents=True)
            check = CHECK if profile == "queue-motion-v1" else (
                "import pathlib, sys\n"
                "args = dict(zip(sys.argv[1::2], sys.argv[2::2]))\n"
                f"pathlib.Path(args['--out']).write_text({json.dumps(checker_report(profile))!r}, encoding='utf-8')\n")
            scripts = {"capture.mjs": CAPTURE, "check.py": check, "observation.py": BRIDGE,
                       "server.mjs": f"// {profile} synthetic server\n",
                       "view.mjs": f"// {profile} synthetic view\n", "index.html": f"{profile} synthetic\n"}
            for name, source in scripts.items():
                (location / name).write_text(source, encoding="utf-8")
        resources_patch = patch.object(execution.service, "resource_root", return_value=self.resources)
        resources_patch.start()
        self.addCleanup(resources_patch.stop)
        self.real_run = execution._run

        def synthetic_node(argv, root, directory, name, deadline):
            if name == "node-capabilities":
                argv = [sys.executable, "-c", "print('synthetic Node capability test double')"]
            return self.real_run(argv, root, directory, name, deadline)

        runner_patch = patch.object(execution, "_run", side_effect=synthetic_node)
        runner_patch.start()
        self.addCleanup(runner_patch.stop)

    def config(self, profile):
        return profile_config(self.queue_config, profile)

    def location(self, profile):
        return self.resources / "examples/consumer-execution" / execution.PROFILE_RESOURCES[profile]

    def run_profile(self, profile, *, out=None, **kwargs):
        return execution.execute(self.state, self.root, "package", self.config(profile), out or f"runs/{profile}",
                                 node=kwargs.pop("node", sys.executable), **kwargs)

    def retained(self, result):
        self.assertEqual(json.loads((self.root / result["result_path"]).read_bytes()), result)
        self.assertEqual(self.state.read_bytes(), self.initial)
        self.assertFalse(result["state_written"])
        self.assertFalse(result["automatic_acceptance"])

    def test_closed_profile_schemas_and_public_schema_accept_exact_contracts(self):
        listing = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, self.root)
        tool = next(row for row in listing["result"]["tools"] if row["name"] == "pixl_consumer_execute")
        schema = tool["inputSchema"]["properties"]["config"]
        self.assertFalse(schema["additionalProperties"])
        for profile in execution.PROFILE_RESOURCES:
            with self.subTest(profile=profile):
                config = self.config(profile)
                self.assertEqual(execution._configuration(self.root, config), config)
                execution._Validator(schema).validate(config)
                self.assertIn(profile, tool["description"])
                self.assertEqual(set(execution.PROFILE_SCHEMAS[profile]["required"]), set(config))
        self.assertEqual(set(self.queue_config), {"version", "profile", "modules", "destinations", "scales",
                                                "observed_wraps", "phase_timeout_ms", "hold_ms", "timeout_seconds"})

    def test_cross_profile_modules_and_fields_refuse_before_process_or_output(self):
        cases = []
        for profile in execution.PROFILE_RESOURCES:
            for other in execution.PROFILE_RESOURCES:
                if profile != other:
                    config = self.config(profile)
                    config["modules"] = self.config(other)["modules"]
                    cases.append(config)
            for required in self.config(profile):
                config = self.config(profile)
                del config[required]
                cases.append(config)
        for profile, field in (("tile-neighborhood-v1", "hold_ms"), ("tile-neighborhood-v1", "observed_wraps"),
                               ("tile-neighborhood-v1", "phase_timeout_ms"), ("sprite-animation-v1", "hold_ms")):
            cases.append({**self.config(profile), field: self.queue_config[field]})
        cases.extend([{**self.config(NEW_PROFILES[0]), "profile": "custom-runner"},
                      {**self.config(NEW_PROFILES[1]), "command": "arbitrary"}])
        with patch.object(execution, "_run") as run:
            for config in cases:
                with self.subTest(config=config), self.assertRaises(PixlError) as raised:
                    execution.execute(self.state, self.root, "package", config, "runs/refused")
                self.assertEqual(raised.exception.code, "consumer_config")
            run.assert_not_called()
        self.assertFalse((self.root / "runs/refused").exists())

    def test_new_profile_integer_and_module_path_guards_are_strict(self):
        for profile in NEW_PROFILES:
            cases = []
            fields = ["version", "timeout_seconds"]
            if profile == "sprite-animation-v1":
                fields += ["observed_wraps", "phase_timeout_ms"]
            for field in fields:
                for invalid in (True, float(self.config(profile)[field])):
                    cases.append({**self.config(profile), field: invalid})
            for scales in ([True], [1.0], [1, 1], [0], [17], [1, 2, 3, 4, 5]):
                cases.append({**self.config(profile), "scales": scales})
            key = next(iter(self.config(profile)["modules"]))
            for path in ("src/../terrain.ts", "src//terrain.ts", "assets/terrain.ts", "src/terrain.py"):
                cases.append({**self.config(profile), "modules": {key: path}})
            for config in cases:
                with self.subTest(profile=profile, config=config), self.assertRaises(PixlError):
                    execution._configuration(self.root, config)

    def test_new_profiles_reuse_full_pipeline_and_retain_exact_selected_resources(self):
        for profile in NEW_PROFILES:
            with self.subTest(profile=profile):
                arguments = {"path": self.state.relative_to(self.root).as_posix(), "candidate_id": "package",
                             "config": self.config(profile), "out": f"runs/{profile}", "node": sys.executable}
                result = service.call("pixl_consumer_execute", arguments, self.root)
                self.assertEqual(result["status"], "complete", result)
                self.assertEqual(result["profile"], profile)
                self.assertTrue(result["files_verified"])
                self.assertTrue(result["renderer_executed"])
                self.assertEqual(result["check_summary"], execution._check_summary(checker_report(profile), profile))
                self.assertTrue((self.root / result["bundle"]["path"]).is_file())
                self.assertTrue((self.root / result["import_result"]).is_file())
                sources = json.loads((self.root / arguments["out"] / "renderer-sources.json").read_bytes())
                self.assertEqual({Path(row["resource"]).name for row in sources}, set(execution.PROFILE_FILES))
                for row in sources:
                    self.assertEqual(Path(row["resource"]).parent, self.location(profile))
                    self.assertEqual(row["sha256"], hashlib.sha256(Path(row["resource"]).read_bytes()).hexdigest())
                    self.assertEqual((self.root / row["copy"]).read_bytes(), Path(row["resource"]).read_bytes())
                capture = json.loads((self.root / arguments["out"] / "execution/capture.json").read_bytes())
                self.assertEqual(capture["argv"][1], str(self.root / arguments["out"] / "renderer/capture.mjs"))
                retained = json.loads((self.root / result["result_path"]).read_bytes())
                self.retained(retained)

    def test_missing_profile_resource_never_falls_back_to_queue(self):
        for profile in NEW_PROFILES:
            with self.subTest(profile=profile):
                (self.location(profile) / "view.mjs").unlink()
                with patch.object(execution, "_run") as run:
                    result = self.run_profile(profile)
                    run.assert_not_called()
                self.assertEqual(result["status"], "unavailable")
                self.assertIn(profile, result["error"]["detail"])
                self.assertIn("view.mjs", result["error"]["detail"])
                self.assertIsNone(result["observation"])
                self.retained(result)

    def test_missing_executable_and_capability_failure_are_retained_for_each_profile(self):
        def unavailable_capability(argv, root, directory, name, deadline):
            if name == "node-capabilities":
                self.assertIn("consumerCapabilities", argv[-1])
                argv = [sys.executable, "-c", "import sys; sys.exit(3)"]
            return self.real_run(argv, root, directory, name, deadline)

        for profile in NEW_PROFILES:
            with self.subTest(profile=profile):
                result = self.run_profile(profile, node=str(self.root / "missing-node.exe"), out=f"runs/{profile}-missing")
                self.assertEqual(result["status"], "unavailable")
                self.assertFalse(result["process_started"])
                self.retained(result)
                with patch.object(execution, "_run", side_effect=unavailable_capability):
                    result = self.run_profile(profile)
                self.assertEqual(result["status"], "unavailable")
                self.assertEqual(result["error"]["code"], "consumer_capability")
                self.assertFalse(result["renderer_executed"])
                self.assertEqual([row["phase"] for row in result["phases"]], ["node-version", "node-capabilities"])
                self.retained(result)

    def test_new_profiles_preserve_capture_failure_and_partial_files(self):
        for profile in NEW_PROFILES:
            with self.subTest(profile=profile):
                (self.location(profile) / "capture.mjs").write_text(CAPTURE + "sys.exit(4)\n", encoding="utf-8")
                result = self.run_profile(profile)
                self.assertEqual(result["status"], "failed")
                self.assertTrue(result["renderer_executed"])
                self.assertIsNone(result["observation"])
                self.assertTrue((self.root / f"runs/{profile}/capture/partial.txt").is_file())
                self.assertFalse((self.root / f"runs/{profile}/import").exists())
                self.retained(result)

    def test_changed_sources_or_configuration_invalidate_new_profile_attempt(self):
        mutations = {"tile-neighborhood-v1": "(root / 'src/terrain.ts').write_text('changed', encoding='utf-8')\n",
                     "sprite-animation-v1": "pathlib.Path(args['--config']).write_text('{}', encoding='utf-8')\n"}
        for profile, mutation in mutations.items():
            with self.subTest(profile=profile):
                (self.location(profile) / "capture.mjs").write_text(CAPTURE + mutation, encoding="utf-8")
                result = self.run_profile(profile)
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["error"]["code"], "consumer_inputs_changed")
                self.assertTrue(result["renderer_executed"])
                self.assertIsNone(result["observation"])
                self.assertFalse((self.root / f"runs/{profile}/check.json").exists())
                self.retained(result)

    def test_tile_summary_is_static_and_sprite_summary_requires_observed_playback(self):
        tile = checker_report("tile-neighborhood-v1")
        self.assertEqual(execution._check_summary(tile, "tile-neighborhood-v1")["phases"], {})
        animation = checker_report("sprite-animation-v1")
        summary = execution._check_summary(animation, "sprite-animation-v1")
        self.assertEqual(summary["phases"]["playback"]["counts"]["walk@1x"]["distinct_frames"], 3)
        for profile, report in (("tile-neighborhood-v1", animation), ("sprite-animation-v1", tile)):
            with self.subTest(profile=profile), self.assertRaises(PixlError):
                execution._check_summary(report, profile)
        tile["facts"]["clock_checks"] = 1
        with self.assertRaises(PixlError):
            execution._check_summary(tile, "tile-neighborhood-v1")

    def test_sprite_summary_rejects_foreign_phases_and_invalid_sample_counts(self):
        mutations = [lambda facts: facts["phases"].update(reduced={}),
                     lambda facts: facts["phases"]["playback"].update(status="stepped"),
                     lambda facts: facts["phases"]["playback"].update(sample_count=True),
                     lambda facts: facts["phases"]["playback"].update(sample_count=0),
                     lambda facts: facts["phases"]["playback"].update(counts={})]
        for mutation in mutations:
            report = checker_report("sprite-animation-v1")
            mutation(report["facts"])
            with self.subTest(report=report), self.assertRaises(PixlError):
                execution._check_summary(report, "sprite-animation-v1")

        for field, value in (("frames", [True]), ("frames", [0, 0]), ("frames", [16]),
                             ("frames", []), ("transitions", True), ("wraps", -1), ("skips", 1.0)):
            report = checker_report("sprite-animation-v1")
            report["facts"]["phases"]["playback"]["counts"]["walk@1x"][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(PixlError):
                execution._check_summary(report, "sprite-animation-v1")


class ConsumerProfileBrowserTests(unittest.TestCase):
    def test_public_cli_runs_both_profiles_with_current_exact_family_and_no_acceptance(self):
        from evaluations.domain_consumer_case import PROFILES, config, project, state

        node = shutil.which("node")
        candidates = [Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
                      Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
                      Path("/usr/bin/chromium"), Path("/usr/bin/google-chrome")]
        browser = next((path for path in candidates if path.is_file()), None)
        if not node or not browser:
            self.skipTest("Installed Node/Chromium unavailable")
        with TemporaryDirectory() as folder:
            root = Path(folder)
            project(root)
            production = {p.relative_to(root).as_posix(): p.read_bytes() for p in (root / ".pixl").rglob("*") if p.is_file()}
            for domain, profile in PROFILES.items():
                with self.subTest(profile=profile):
                    config_path = root / f"{domain}-config.json"
                    config_path.write_text(json.dumps(config(domain)), encoding="utf-8")
                    out = f"runs/{domain}"
                    completed = subprocess.run([sys.executable, "-m", "pixl", "consumer-execute",
                        str(root / state(domain)), "delivery.candidate", str(config_path), "--out", out,
                        "--root", str(root), "--node", node, "--browser", str(browser)],
                        capture_output=True, check=False, timeout=120)
                    self.assertEqual(completed.returncode, 0, completed.stdout.decode("utf-8") + completed.stderr.decode("utf-8"))
                    result = json.loads(completed.stdout)
                    self.assertEqual(result["status"], "complete", result)
                    self.assertEqual(result["profile"], profile)
                    self.assertTrue(result["renderer_executed"])
                    self.assertTrue(result["files_verified"])
                    self.assertTrue(result["cleanup"]["complete"])
                    self.assertFalse(result["state_written"])
                    self.assertFalse(result["automatic_acceptance"])
                    report = json.loads((root / out / "observation.json").read_bytes())
                    self.assertEqual({row["path"] for row in report["destinations"]}, set(config(domain)["destinations"].values()))
                    self.assertEqual({row["scale"] for row in report["views"]}, {1, 3})
                    if domain == "terrain":
                        self.assertEqual(report["motion"], [])
                        self.assertEqual(result["check_summary"]["clock_checks"], 0)
                        self.assertEqual(result["check_summary"]["phases"], {})
                    else:
                        self.assertTrue(report["motion"])
                        self.assertEqual(set(result["check_summary"]["phases"]), {"playback"})
                    imported = json.loads((root / result["import_result"]).read_bytes())
                    self.assertFalse(imported["renderer_executed"])
                    self.assertTrue((root / result["bundle"]["path"]).is_file())
            current = {p.relative_to(root).as_posix(): p.read_bytes() for p in (root / ".pixl").rglob("*") if p.is_file()}
            self.assertEqual(current, production)
