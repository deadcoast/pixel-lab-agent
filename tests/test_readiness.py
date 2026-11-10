"""Readiness separates local facts, observed visibility and unknown host state."""

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
from types import SimpleNamespace
from unittest.mock import patch

from pixl import entrypoint, readiness

ROOT = Path(__file__).resolve().parents[1]
AVAILABLE = {"status": "available", "python": "3.11.0", "checks": []}
STAMP = "2026-11-09T12:00:00+00:00"


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.consumer = self.root / "consumer"
        self.consumer.mkdir()
        dependency = patch.object(readiness, "probe_dependencies", return_value=AVAILABLE)
        self.dependencies = dependency.start()
        self.addCleanup(dependency.stop)

    def file(self, root, relative, text="fixture"):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def installation(self, kind):
        root = self.root / kind
        root.mkdir()
        profile = ".agents/PROFILE.md" if kind == "source" else "resources/agent/PROFILE.md"
        self.file(root, profile)
        self.file(root, {"source": "pixl/__main__.py", "plugin": "runtime/pixl/__main__.py", "wheel": "__main__.py"}[kind])
        if kind == "wheel":
            self.file(root, "__init__.py")
        else:
            prefix = "plugins/pixl/" if kind == "source" else ""
            for skill in ("pixl", "plar"):
                self.file(root, prefix + "skills/" + skill + "/SKILL.md", "---\nname: " + skill + "\ndescription: Fixture workflow\n---\nBody")
        if kind == "plugin":
            entries = [{"path": path.relative_to(root).as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                       for path in sorted(root.rglob("*")) if path.is_file()]
            self.file(root, "bundle-manifest.json", json.dumps({"files": entries}))
        return root

    def observed(self, **fields):
        return {"host": "codex", "observed_at": STAMP, **fields}

    def test_source_report_does_not_invent_host_or_provider_readiness(self):
        installation = self.installation("source")
        result = readiness.report(self.consumer, "codex", installation)
        self.assertEqual(result["installation"]["kind"], "source")
        self.assertEqual(result["installation"]["status"], "present")
        self.assertEqual(result["local_operations"]["runtime_requirements"], "satisfied")
        self.assertEqual(result["specialist"]["named_role"], "not_observed")
        self.assertEqual(result["official_pixellab"]["visibility"]["status"], "not_observed")
        self.assertEqual(result["official_pixellab"]["authentication"], "not_verified")
        self.assertNotIn("ready", result)

    def test_missing_or_file_project_root_is_rejected_without_creating_it(self):
        for root in (self.root / "missing", self.file(self.root, "file.txt")):
            with self.subTest(root=root), self.assertRaises(readiness.ReadinessError) as caught:
                readiness.report(root)
            self.assertEqual(caught.exception.code, "readiness_root")
        self.assertFalse((self.root / "missing").exists())

    def test_partial_inventory_absence_remains_unknown(self):
        installation = self.installation("source")
        result = readiness.report(self.consumer, installation=installation, observations=self.observed(
            local_tools={"names": ["pixl_validate"], "complete_inventory": False},
            official_tools={"names": [], "complete_inventory": False}))
        self.assertEqual(result["local_operations"]["mcp_visibility"]["readiness_operation"], "not_observed")
        self.assertEqual(result["official_pixellab"]["visibility"]["status"], "not_observed")

    def test_complete_supplied_inventory_can_report_not_listed_without_authentication_claim(self):
        result = readiness.report(self.consumer, installation=self.installation("source"), observations=self.observed(
            named_role="unavailable", local_tools={"names": [], "complete_inventory": True},
            official_tools={"names": [], "complete_inventory": True}))
        self.assertEqual(result["local_operations"]["mcp_visibility"]["readiness_operation"], "not_listed")
        self.assertEqual(result["official_pixellab"]["visibility"]["status"], "not_listed")
        self.assertEqual(result["official_pixellab"]["authentication"], "not_verified")
        self.assertEqual(result["specialist"]["named_role"], "unavailable")

    def test_present_role_and_secret_instruction_body_do_not_establish_loaded_role_or_leak_body(self):
        secret = "fixture-private-instruction-value"
        self.file(self.consumer, ".codex/agents/pixl.toml", 'name="pixl"\ndeveloper_instructions="' + secret + '"\n')
        result = readiness.report(self.consumer, "codex", self.installation("source"))
        self.assertEqual(result["specialist"]["static_adapters"]["codex"]["role_file"]["status"], "present")
        self.assertEqual(result["specialist"]["named_role"], "not_observed")
        self.assertEqual(result["specialist"]["instruction_loading"], "not_verified")
        self.assertNotIn(secret, json.dumps(result))

    def test_unknown_fields_and_malformed_values_are_rejected_without_echo(self):
        secret = "Bearer private-credential-do-not-echo"
        cases = [self.observed(headers={"Authorization": secret}), self.observed(host_version=secret),
                 self.observed(named_role=secret), self.observed(observed_at=secret),
                 self.observed(local_tools={"names": [secret], "complete_inventory": True}),
                 self.observed(official_tools={"names": [], "complete_inventory": 1}),
                 self.observed(official_tools={"names": ["get_image", "get_image"], "complete_inventory": False}),
                 self.observed(official_tools={"names": [], "complete_inventory": False, "token": secret})]
        for observation in cases:
            with self.subTest(observation=observation), self.assertRaises(readiness.ReadinessError) as caught:
                readiness.validate_observations(observation)
            self.assertNotIn(secret, str(caught.exception))

    def test_host_mismatch_and_naive_timestamp_are_rejected(self):
        with self.assertRaises(readiness.ReadinessError):
            readiness.validate_observations(self.observed(), "claude")
        with self.assertRaises(readiness.ReadinessError):
            readiness.validate_observations(self.observed(observed_at="2026-11-09T12:00:00"))

    def test_valid_observations_are_detached_and_visibility_is_not_authentication(self):
        observation = self.observed(named_role="available", local_tools={"names": ["pixl_readiness"], "complete_inventory": False},
                                    official_tools={"names": ["pixelart_workbench"], "complete_inventory": False})
        result = readiness.report(self.consumer, installation=self.installation("source"), observations=observation)
        observation["official_tools"]["names"].append("get_image")
        self.assertEqual(result["official_pixellab"]["visibility"]["names"], ["pixelart_workbench"])
        self.assertEqual(result["official_pixellab"]["authentication"], "not_verified")
        self.assertEqual(result["official_pixellab"]["execution"], "not_attempted")

    def test_plugin_hash_mismatch_and_missing_skill_remain_visible(self):
        installation = self.installation("plugin")
        self.file(installation, "skills/pixl/SKILL.md", "changed")
        (installation / "skills/plar/SKILL.md").unlink()
        result = readiness.report(self.consumer, installation=installation)
        self.assertEqual(result["installation"]["status"], "incomplete")
        self.assertEqual(result["installation"]["bundle_manifest"]["status"], "mismatch")
        self.assertEqual(result["installation"]["files"]["plar_skill"]["status"], "missing")

    def test_manifest_rejects_escape_duplicate_path_and_malformed_shape(self):
        installation = self.installation("plugin")
        manifest = installation / "bundle-manifest.json"
        valid = json.loads(manifest.read_text())
        cases = [{"files": [{"path": "../outside", "sha256": "a" * 64}]},
                 {"files": [valid["files"][0], valid["files"][0]]}, {"files": []}, {"files": "wrong"}]
        for value in cases:
            manifest.write_text(json.dumps(value), encoding="utf-8")
            self.assertEqual(readiness.verify_manifest(installation)["status"], "invalid_or_unreadable")

    def test_generated_manifest_rows_are_verified_too(self):
        installation = self.installation("plugin")
        path = installation / "bundle-manifest.json"
        manifest = json.loads(path.read_text())
        manifest["generated_files"] = [{"path": "requirements.txt", "sha256": "b" * 64}]
        path.write_text(json.dumps(manifest), encoding="utf-8")
        result = readiness.verify_manifest(installation)
        self.assertEqual(result["status"], "mismatch")
        self.assertEqual(result["issues"][-1]["status"], "missing")

    def test_manifest_itself_cannot_resolve_outside_installation(self):
        installation = self.installation("plugin")
        manifest = installation / "bundle-manifest.json"
        outside = self.file(self.root, "outside-manifest.json", "private external bytes")
        original_resolve = Path.resolve

        def escaped(path, *args, **kwargs):
            return outside if path == manifest else original_resolve(path, *args, **kwargs)

        with patch.object(Path, "resolve", autospec=True, side_effect=escaped):
            result = readiness.verify_manifest(installation)
        self.assertEqual(result["status"], "invalid_or_unreadable")
        self.assertEqual(result["files_checked"], 0)
        self.assertNotIn("private external bytes", json.dumps(result))

    def test_manifest_hash_identifies_the_bytes_parsed_before_concurrent_replacement(self):
        installation = self.installation("plugin")
        manifest = installation / "bundle-manifest.json"
        original = manifest.read_bytes()
        replacement = b'{"files":[],"changed":true}'
        original_hash = readiness._hash

        def changed_during_payload_check(path):
            manifest.write_bytes(replacement)
            return original_hash(path)

        with patch.object(readiness, "_hash", side_effect=changed_during_payload_check):
            result = readiness.verify_manifest(installation)
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["sha256"], hashlib.sha256(original).hexdigest())
        self.assertNotEqual(result["sha256"], hashlib.sha256(manifest.read_bytes()).hexdigest())

    def test_relocated_plugin_uses_its_own_manifest_and_files(self):
        original = self.installation("plugin")
        relocated = self.root / "relocated" / "kit"
        shutil.copytree(original, relocated)
        result = readiness.report(self.consumer, installation=relocated)
        self.assertEqual(result["installation"]["root"], str(relocated))
        self.assertEqual(result["installation"]["bundle_manifest"]["status"], "verified")

    def test_relative_installation_uses_project_root_not_server_working_directory(self):
        original = self.installation("plugin")
        copied = self.consumer / "local-kit"
        shutil.copytree(original, copied)
        self.assertNotEqual(Path.cwd(), self.consumer)
        result = readiness.report(self.consumer, installation="local-kit")
        self.assertEqual(result["installation"]["root"], str(copied))
        self.assertEqual(result["installation"]["kind"], "plugin")
        self.assertEqual(result["installation"]["bundle_manifest"]["status"], "verified")
        absolute = readiness.report(self.consumer, installation=original)
        self.assertEqual(absolute["installation"]["root"], str(original))

    @unittest.skipUnless(sys.platform == "win32", "Windows drive-relative and rooted-relative paths")
    def test_ambiguous_windows_installation_paths_are_rejected(self):
        for installation in ("C:kit", "\\kit", "/kit"):
            with self.subTest(installation=installation), self.assertRaises(readiness.ReadinessError) as caught:
                readiness.report(self.consumer, installation=installation)
            self.assertEqual(caught.exception.code, "readiness_input")

    def test_wheel_does_not_require_portable_skills_or_manifest(self):
        result = readiness.report(self.consumer, installation=self.installation("wheel"))
        self.assertEqual(result["installation"]["kind"], "wheel")
        self.assertEqual(result["installation"]["status"], "present")
        self.assertEqual(result["installation"]["bundle_manifest"]["status"], "not_applicable")
        self.assertEqual(result["installation"]["files"]["pixl_skill"]["status"], "not_in_distribution")

    def test_read_only_report_preserves_consumer_and_installation_bytes(self):
        installation = self.installation("plugin")
        self.file(self.consumer, "state.txt", "retained")
        before = {str(path): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        readiness.report(self.consumer, installation=installation)
        self.assertEqual(before, {str(path): path.read_bytes() for path in self.root.rglob("*") if path.is_file()})

    def test_cli_rejects_secret_observation_file_and_outside_path_without_echo(self):
        secret = "fixture-auth-token-value"
        self.file(self.consumer, "observed.json", json.dumps(self.observed(token=secret)))
        for relative in ("observed.json", "../outside.json"):
            output, errors = io.StringIO(), io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                code = readiness.main(["--root", str(self.consumer), "--observations", relative])
            self.assertEqual(code, 2)
            self.assertNotIn(secret, output.getvalue() + errors.getvalue())

    def test_observation_read_is_bounded_even_if_earlier_size_observation_is_small(self):
        path = self.file(self.consumer, "large.json", " " * (readiness.MAX_INPUT_BYTES * 2))
        original_stat = Path.stat

        def stale_size(selected, *args, **kwargs):
            return SimpleNamespace(st_size=1) if selected == path else original_stat(selected, *args, **kwargs)

        output, errors = io.StringIO(), io.StringIO()
        with (patch.object(Path, "stat", autospec=True, side_effect=stale_size),
              patch.object(readiness, "_json", side_effect=AssertionError("oversized input must not reach parsing")),
              redirect_stdout(output), redirect_stderr(errors)):
            code = readiness.main(["--root", str(self.consumer), "--observations", "large.json"])
        self.assertEqual(code, 2)
        self.assertIn("64 KiB", errors.getvalue())

    def test_stdlib_bootstrap_reports_missing_dependencies(self):
        result = subprocess.run([sys.executable, "-B", "-S", "-m", "pixl", "readiness", "--root", str(self.consumer),
                                 "--installation", str(ROOT)], cwd=ROOT, capture_output=True, text=True, timeout=20, check=False)
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["dependencies"]["status"], "incomplete")
        self.assertTrue(any(row["status"] == "missing" for row in report["dependencies"]["checks"]))
        self.assertNotIn("Traceback", result.stderr)

    def test_entrypoint_dispatches_readiness_without_importing_cli(self):
        with patch.object(readiness, "main", return_value=7) as main:
            self.assertEqual(entrypoint.main(["readiness", "--root", "fixture"]), 7)
        main.assert_called_once_with(["--root", "fixture"])


class DependencyProbeTests(unittest.TestCase):
    def test_dependency_failures_suppress_output_and_restore_bytecode_policy(self):
        secret = "fixture-secret-from-import-error"
        prior = sys.dont_write_bytecode

        def failure(_):
            print(secret)
            raise ModuleNotFoundError(secret)

        output, errors = io.StringIO(), io.StringIO()
        with (patch.object(readiness.importlib, "import_module", side_effect=failure),
              patch.object(readiness.importlib.metadata, "version", side_effect=readiness.importlib.metadata.PackageNotFoundError),
              redirect_stdout(output), redirect_stderr(errors)):
            result = readiness.probe_dependencies()
        self.assertEqual(result["status"], "incomplete")
        self.assertTrue(all(row["status"] == "missing" for row in result["checks"]))
        self.assertNotIn(secret, json.dumps(result) + output.getvalue() + errors.getvalue())
        self.assertEqual(sys.dont_write_bytecode, prior)


if __name__ == "__main__":
    unittest.main()
