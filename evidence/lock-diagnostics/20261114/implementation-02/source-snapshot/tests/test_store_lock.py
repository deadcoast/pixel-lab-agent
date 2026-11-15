"""Recorded lock ownership is useful context, never automatic recovery authority."""

import json
import os
import subprocess
import sys
import unittest
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from pixl import diagnostics, store
from pixl.codec import PixlError, Symbol, digest, encode
from tests.support import sample


class StoreLockTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory(prefix="pixl lock diagnostics ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.folder = self.root / ".pixl"
        self.folder.mkdir()
        self.path = self.folder / ".lock"

    def blocked(self, folder=None):
        with self.assertRaises(PixlError) as caught:
            with store.lock(self.folder if folder is None else folder):
                self.fail("A contender acquired an existing lock")
        self.assertEqual(caught.exception.code, "store_locked")
        return caught.exception

    def preserved_block(self, expected):
        before = self.path.read_bytes(), self.path.stat().st_mtime_ns
        error = self.blocked()
        self.assertEqual(error.context["lock"]["metadata_status"], expected)
        self.assertEqual(error.context["lock"]["owner_state"], "unverified")
        self.assertEqual((self.path.read_bytes(), self.path.stat().st_mtime_ns), before)
        return error

    def test_new_lock_has_recorded_owner_and_normal_release(self):
        with store.lock(self.folder):
            metadata = json.loads(self.path.read_bytes())
            self.assertEqual(metadata["pid"], os.getpid())
            self.assertTrue(metadata["host"])
            self.assertEqual(datetime.fromisoformat(metadata["acquired_at"]).utcoffset().total_seconds(), 0)
            error = self.preserved_block("readable")
            self.assertEqual(error.context["lock"]["path"], str(self.path.resolve()))
            self.assertEqual(error.context["lock"]["owner"], metadata)
            self.assertIn(f"recorded PID {os.getpid()}", error.detail)
            self.assertIn("liveness is unverified", error.detail)
        self.assertFalse(self.path.exists())

    def test_body_failure_releases_normal_owned_lock(self):
        with self.assertRaisesRegex(RuntimeError, "interrupted operation"):
            with store.lock(self.folder):
                raise RuntimeError("interrupted operation")
        self.assertFalse(self.path.exists())
        with store.lock(self.folder):
            self.assertTrue(self.path.exists())

    def test_unavailable_hostname_does_not_block_acquisition(self):
        with patch.object(store.socket, "gethostname", side_effect=OSError("host unavailable")):
            with store.lock(self.folder):
                metadata = json.loads(self.path.read_bytes())
                self.assertNotIn("host", metadata)
                self.assertEqual(self.preserved_block("readable").context["lock"]["owner"]["pid"], os.getpid())
        self.assertFalse(self.path.exists())

    def test_legacy_pid_and_old_mtime_never_establish_abandonment(self):
        self.path.write_text(json.dumps({"pid": os.getpid()}), encoding="utf-8")
        os.utime(self.path, (1, 1))
        error = self.preserved_block("readable")
        self.assertEqual(error.context["lock"]["owner"], {"pid": os.getpid()})
        self.assertIn("PID or age alone is not proof", error.detail)

    def test_unusable_metadata_keeps_lock_without_echoing_payload(self):
        values = [
            (b"", "incomplete"), (b" \r\n", "incomplete"),
            (b'{"pid":', "malformed"), (b"[]", "malformed"),
            (b'{"pid":true}', "malformed"), (b'{"pid":0}', "malformed"),
            (b'{"pid":-2}', "malformed"), (b'{"pid":4294967296}', "malformed"),
            (b'{"pid":NaN}', "malformed"), (b'{"pid":1,"pid":2}', "malformed"),
            (b'{"secret":"NEVER_ECHO_THIS_PAYLOAD"}', "malformed"),
            (b"\xff", "malformed"), (b"[" * 1500 + b"]" * 1500, "malformed"),
        ]
        for payload, status in values:
            with self.subTest(payload=payload[:80]):
                self.path.write_bytes(payload)
                error = self.preserved_block(status)
                self.assertNotIn("owner", error.context["lock"])
                self.assertNotIn("NEVER_ECHO_THIS_PAYLOAD", str(error))

    def test_oversized_metadata_is_not_opened_for_reading(self):
        self.path.write_bytes(b"NEVER_ECHO_THIS_PAYLOAD" * 300)
        with patch.object(store.os, "fdopen", side_effect=AssertionError("oversized metadata was opened")):
            error = self.preserved_block("oversized")
        self.assertNotIn("NEVER_ECHO_THIS_PAYLOAD", str(error))

    def test_metadata_read_denial_preserves_original_contention_error(self):
        self.path.write_text('{"pid":123}', encoding="utf-8")
        real_open = os.open

        def denied(path, flags, *args, **kwargs):
            if not flags & os.O_CREAT:
                raise PermissionError("permission detail must not escape")
            return real_open(path, flags, *args, **kwargs)

        with patch.object(store.os, "open", side_effect=denied):
            error = self.preserved_block("unreadable")
        self.assertNotIn("permission detail", error.detail)

    def test_directory_lock_is_not_opened_or_removed(self):
        self.path.mkdir()
        error = self.blocked()
        self.assertEqual(error.context["lock"]["metadata_status"], "non_regular")
        self.assertTrue(self.path.is_dir())

    def test_symlink_lock_does_not_read_target(self):
        target = self.root / "outside-owner.json"
        target.write_text('{"pid":123,"secret":"NEVER_ECHO_TARGET"}', encoding="utf-8")
        try:
            self.path.symlink_to(target)
        except OSError as error:
            self.skipTest(f"Symlink creation unavailable: {error}")
        before = target.read_bytes(), target.stat().st_mtime_ns
        error = self.blocked()
        self.assertEqual(error.context["lock"]["metadata_status"], "non_regular")
        self.assertTrue(self.path.is_symlink())
        self.assertEqual((target.read_bytes(), target.stat().st_mtime_ns), before)
        self.assertNotIn("NEVER_ECHO_TARGET", str(error))

    def test_replaced_path_before_open_has_no_attributed_owner(self):
        self.path.write_text('{"pid":123}', encoding="utf-8")
        replacement = self.root / "replacement.lock"
        replacement.write_text('{"pid":456}', encoding="utf-8")
        replacement_bytes = replacement.read_bytes()
        real_open = os.open

        def replaced(path, flags, *args, **kwargs):
            if not flags & os.O_CREAT:
                os.replace(replacement, self.path)
            return real_open(path, flags, *args, **kwargs)

        with patch.object(store.os, "open", side_effect=replaced):
            error = self.blocked()
        self.assertEqual(error.context["lock"]["metadata_status"], "changed")
        self.assertNotIn("owner", error.context["lock"])
        self.assertEqual(self.path.read_bytes(), replacement_bytes)

    def test_changed_descriptor_metadata_discards_observation(self):
        self.path.write_text('{"pid":123}', encoding="utf-8")
        real_fstat = os.fstat
        calls = 0

        def changed(fd):
            nonlocal calls
            value = real_fstat(fd)
            calls += 1
            if calls == 2:
                fields = {name: getattr(value, name) for name in (
                    "st_dev", "st_ino", "st_mode", "st_size", "st_mtime_ns", "st_ctime_ns")}
                fields["st_mtime_ns"] += 1
                return SimpleNamespace(**fields)
            return value

        with patch.object(store.os, "fstat", side_effect=changed):
            error = self.preserved_block("changed")
        self.assertNotIn("owner", error.context["lock"])

    def test_path_and_descriptor_ctime_are_compared_within_their_own_api(self):
        self.path.write_text('{"pid":123}', encoding="utf-8")
        real_fstat = os.fstat

        def descriptor_ctime(fd):
            value = real_fstat(fd)
            fields = {name: getattr(value, name) for name in (
                "st_dev", "st_ino", "st_mode", "st_size", "st_mtime_ns", "st_ctime_ns")}
            fields["st_ctime_ns"] = 123456789
            return SimpleNamespace(**fields)

        with patch.object(store.os, "fstat", side_effect=descriptor_ctime):
            self.assertEqual(self.preserved_block("readable").context["lock"]["owner"], {"pid": 123})

    def test_permission_denial_without_observed_lock_stays_access_error(self):
        with patch.object(store.os, "open", side_effect=PermissionError("cannot create lock")):
            with self.assertRaisesRegex(PermissionError, "cannot create lock"):
                with store.lock(self.folder):
                    self.fail("Unexpected acquisition")
        self.assertFalse(self.path.exists())

    def test_owner_release_during_observation_does_not_retry_or_recreate(self):
        self.path.write_text('{"pid":123}', encoding="utf-8")
        real_open = os.open

        def vanished(path, flags, *args, **kwargs):
            if not flags & os.O_CREAT:
                self.path.unlink()
            return real_open(path, flags, *args, **kwargs)

        with patch.object(store.os, "open", side_effect=vanished):
            error = self.blocked()
        self.assertEqual(error.context["lock"]["metadata_status"], "changed")
        self.assertFalse(self.path.exists())

    def test_optional_fields_are_bounded_and_control_timestamp_is_ignored(self):
        self.path.write_text(json.dumps({"pid": 123, "host": "host\nFORGED_LINE",
                                        "acquired_at": "2026-11-14\n12:00:00+00:00",
                                        "secret": "NEVER_ECHO_THIS_PAYLOAD"}), encoding="utf-8")
        error = self.preserved_block("readable")
        self.assertEqual(error.context["lock"]["owner"], {"pid": 123})
        self.assertNotIn("FORGED_LINE", error.detail)
        self.assertNotIn("2026-11-14", error.detail)
        self.assertNotIn("NEVER_ECHO_THIS_PAYLOAD", error.detail)

    def test_non_utc_or_invalid_time_does_not_become_owner_fact(self):
        for stamp in ("2026-11-14T12:00:00-08:00", "2026-11-14T12:00:00",
                      "2026-99-99T12:00:00+00:00", "x" * 41):
            with self.subTest(stamp=stamp):
                self.path.write_text(json.dumps({"pid": 123, "acquired_at": stamp}), encoding="utf-8")
                self.assertEqual(self.preserved_block("readable").context["lock"]["owner"], {"pid": 123})

    def test_public_recovery_preserves_code_and_recorded_identity_only(self):
        self.path.write_text('{"pid":123,"host":"recorded-host","acquired_at":"2026-11-14T12:00:00Z"}', encoding="utf-8")
        error = self.preserved_block("readable")
        result = diagnostics.error_result("commit", error, {"lock": {"owner": {"pid": 999}}, "pid": 999})
        self.assertEqual(result["error"], "store_locked")
        self.assertEqual(result["detail"], str(error))
        self.assertEqual(result["category"], "unfinished_work")
        self.assertEqual(result["lock"], error.context["lock"])
        self.assertEqual(result["recovery"]["action"], "inspect_lock_owner")
        self.assertNotIn("operation", result["recovery"])
        self.assertNotIn("arguments", result["recovery"])
        self.assertNotIn("999", json.dumps(result))

    def test_arguments_cannot_invent_lock_observations(self):
        result = diagnostics.error_result("commit", PixlError("store_locked", "held"), {
            "lock": {"path": "invented.lock", "metadata_status": "readable", "owner": {"pid": 123}},
            "context": {"lock": {"owner": {"pid": 123}}}})
        self.assertNotIn("lock", result)
        self.assertEqual(result["category"], "unfinished_work")

    def test_public_context_sanitizes_malformed_or_unrelated_values(self):
        cases = [[], {"metadata_status": [], "owner": {"pid": 123}},
                 {"metadata_status": "changed", "owner": {"pid": 123}},
                 {"metadata_status": "readable", "owner": {"pid": True}},
                 {"metadata_status": "readable", "path": "\nFORGED_LINE", "secret": "NEVER_ECHO",
                  "owner_state": "dead", "owner": {"pid": 123, "secret": "NEVER_ECHO",
                  "host": "\nFORGED_LINE", "acquired_at": "2026-11-14\n12:00:00+00:00"}}]
        for value in cases:
            with self.subTest(value=value):
                result = diagnostics.error_result("commit", PixlError("store_locked", "held", context={"lock": value}))
                serialized = json.dumps(result)
                self.assertNotIn("NEVER_ECHO", serialized)
                self.assertNotIn("FORGED_LINE", serialized)
                self.assertNotIn('"dead"', serialized)
                self.assertNotIn("2026-11-14", serialized)
                if isinstance(value, dict) and value.get("metadata_status") != "readable":
                    self.assertNotIn("owner", result.get("lock", {}))

    def test_auxiliary_lock_recovery_does_not_invent_state_file(self):
        for name in ("plar-lock", "handoffs"):
            folder = self.folder / name
            with store.lock(folder):
                error = self.blocked(folder)
                result = diagnostics.error_result("pixl_plar_save", error, {"path": "plar.txt"})
                self.assertEqual(result["lock"]["path"], str(folder.resolve() / ".lock"))
                self.assertNotIn("operation", result["recovery"])
                self.assertNotIn("state.px", json.dumps(result))

    def test_actual_cli_and_mcp_locked_commit_preserve_state_and_diagnostics(self):
        doc = sample(self.root)
        store.initialize(self.folder, doc, root=self.root)
        candidate = deepcopy(doc)
        candidate.revision += 1
        candidate.records["task"].fields["st"] = Symbol("active")
        candidate_path = self.root / "candidate.px"
        candidate_path.write_bytes(encode(candidate))
        before = {p.relative_to(self.root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.root.rglob("*") if p.is_file()}
        command = [sys.executable, "-B", "-m", "pixl"]
        with store.lock(self.folder):
            lock_before = self.path.read_bytes(), self.path.stat().st_mtime_ns
            cli = subprocess.run(command + ["commit", str(self.folder), str(candidate_path),
                                 "--expect", digest(doc), "--root", str(self.root)],
                                 capture_output=True, check=False, timeout=30)
            self.assertEqual(cli.returncode, 2)
            cli_result = json.loads(cli.stderr)
            request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
                "name": "pixl_commit", "arguments": {"store": ".pixl", "candidate": "candidate.px", "expect": digest(doc)}}}
            rpc = subprocess.run(command + ["mcp", "--root", str(self.root)],
                                 input=json.dumps(request).encode() + b"\n", capture_output=True, check=False, timeout=30)
            self.assertEqual(rpc.returncode, 0, rpc.stderr.decode())
            envelope = json.loads(rpc.stdout)["result"]
            self.assertTrue(envelope["isError"])
            mcp_result = envelope["structuredContent"]
            for key in ("error", "detail", "category", "recovery", "lock"):
                self.assertEqual(cli_result[key], mcp_result[key], key)
            self.assertEqual(cli_result["lock"]["owner"]["pid"], os.getpid())
            self.assertEqual(cli_result["lock"]["owner_state"], "unverified")
            self.assertEqual((self.path.read_bytes(), self.path.stat().st_mtime_ns), lock_before)
        after = {p.relative_to(self.root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(after, before)
        self.assertEqual(digest(store.load(self.folder)), digest(doc))


if __name__ == "__main__":
    unittest.main()
