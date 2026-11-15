"""Store directories and readable state files have distinct public locators."""

import argparse
import json
import shutil
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import (
    cli,
    codec,
    completion,
    delivery,
    diagnostics,
    jobs,
    mcp,
    plar,
    service,
    store,
)


class StoreLocatorTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory(prefix="pixl store locator ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        # A directory may itself have a .px suffix; never infer its type by name.
        self.folder = self.root / "state.px"
        self.doc = store.intake_project("Retained project", "Keep original choices")
        store.initialize(self.folder, self.doc, self.root)
        self.head = self.folder / "state.px"
        self.candidate = deepcopy(self.doc)
        self.candidate.revision = 1
        self.candidate.records["project"].fields["nm"] = "Continued project"

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in self.root.rglob("*") if p.is_file()}

    def test_file_valued_store_is_rejected_before_lock_without_parent_substitution(self):
        other = self.root / "ordinary-file"
        other.write_bytes(b"preserve this unrelated file\n")
        before = self.snapshot()
        for path in (self.head, other):
            for operation in ("lock", "load", "initialize", "commit"):
                with self.subTest(path=path, operation=operation):
                    with patch.object(store.os, "open") as opened, self.assertRaises(codec.PixlError) as caught:
                        if operation == "lock":
                            with store.lock(path):
                                self.fail("Entered lock body for a file")
                        elif operation == "load":
                            store.load(path)
                        elif operation == "initialize":
                            store.initialize(path, self.doc, self.root)
                        else:
                            store.commit(path, self.candidate, codec.digest(self.doc), self.root)
                    self.assertEqual(caught.exception.code, "directory_required")
                    self.assertIn(str(path), caught.exception.detail)
                    opened.assert_not_called()
                    self.assertEqual(self.snapshot(), before)
        self.assertEqual(store.load(self.folder), self.doc)
        self.assertFalse((self.folder / ".lock").exists())

    def test_load_first_and_lock_first_operations_share_the_locator_failure(self):
        before = self.snapshot()
        expected = codec.digest(self.doc)
        operations = (
            lambda: jobs.dispatch(self.head, expected, "job", self.root),
            lambda: delivery.snapshot(self.head, expected, "output", "candidate", self.root),
            lambda: completion.complete(self.head, expected, "task", ["candidate"], self.root),
        )
        for operation in operations:
            with self.subTest(operation=operation), self.assertRaises(codec.PixlError) as caught:
                operation()
            self.assertEqual(caught.exception.code, "directory_required")
            self.assertEqual(self.snapshot(), before)

    def test_valid_directory_publication_and_state_file_reads_keep_both_formats(self):
        for format_, document in ((1, store.empty_project()), (2, self.doc)):
            with self.subTest(format=format_):
                folder = self.root / ("valid-" + str(format_) + ".px")
                initial = store.initialize(folder, document, self.root)
                current = deepcopy(document)
                current.revision = 1
                current.records["project"].fields["nm"] = "Changed display name"
                result = store.commit(folder, current, initial["hash"], self.root)
                self.assertEqual(result["hash"], codec.digest(current))
                self.assertEqual(store.load(folder), current)
                self.assertEqual((folder / "history" / (initial["hash"] + ".px")).read_bytes(), codec.encode(document))
                report = service.call("pixl_validate", {"path": (folder / "state.px").relative_to(self.root).as_posix()}, self.root)
                self.assertTrue(report["valid"])
                self.assertEqual(report["hash"], codec.digest(current))

    def test_missing_and_unreadable_heads_keep_store_read_error(self):
        missing = self.root / "missing"
        with self.assertRaises(codec.PixlError) as absent:
            store.load(missing)
        self.assertEqual(absent.exception.code, "store_read")
        self.assertIsInstance(absent.exception.__cause__, FileNotFoundError)
        self.assertFalse(missing.exists())
        with (patch.object(Path, "read_bytes", side_effect=PermissionError("retained read denial")),
              self.assertRaises(codec.PixlError) as denied):
            store.load(self.folder)
        self.assertEqual(denied.exception.code, "store_read")
        self.assertIsInstance(denied.exception.__cause__, PermissionError)
        for error in (absent.exception, denied.exception):
            self.assertNotEqual(diagnostics.error_result("load", error)["category"], "invalid_authoring")

    def test_lock_and_unrelated_os_errors_are_not_reclassified_as_locator_failures(self):
        with store.lock(self.folder):
            before = self.snapshot()
            with self.assertRaises(codec.PixlError) as caught:
                store.commit(self.folder, self.candidate, codec.digest(self.doc), self.root)
            self.assertEqual(caught.exception.code, "store_locked")
            result = diagnostics.error_result("commit", caught.exception)
            self.assertEqual(result["category"], "unfinished_work")
            self.assertEqual(result["recovery"]["action"], "inspect_lock_owner")
            self.assertEqual(self.snapshot(), before)
        before = self.snapshot()
        with (patch.object(store, "_atomic", side_effect=FileExistsError("unrelated publication collision")),
              self.assertRaises(FileExistsError) as collision):
            store.commit(self.folder, self.candidate, codec.digest(self.doc), self.root)
        result = diagnostics.error_result("commit", collision.exception)
        self.assertEqual(result["error"], "operation")
        self.assertEqual(result["category"], "unavailable_observation")
        self.assertEqual(self.snapshot(), before)

    def test_locator_diagnostic_is_precise_and_does_not_propose_an_automatic_retry(self):
        error = codec.PixlError("directory_required", "observed file argument")
        result = diagnostics.error_result("pixl_commit", error, {"store": "state.px/state.px"})
        self.assertEqual(result["category"], "invalid_authoring")
        self.assertEqual(result["recovery"]["action"], "correct_directory_path")
        self.assertIn("STORE/state.px", result["recovery"]["detail"])
        self.assertEqual(result["identity"]["store"], "state.px/state.px")
        self.assertNotIn("operation", result["recovery"])
        self.assertNotIn("arguments", result["recovery"])

    def test_actual_cli_and_mcp_commit_errors_preserve_all_files(self):
        candidate = self.root / "candidate.px"
        candidate.write_bytes(codec.encode(self.candidate))
        before = self.snapshot()
        command = [sys.executable, "-B", "-m", "pixl"]
        direct = subprocess.run(command + ["commit", str(self.head), str(candidate), "--expect", codec.digest(self.doc), "--root", str(self.root)],
            capture_output=True, check=False, timeout=30)
        self.assertEqual(direct.returncode, 2, direct.stderr.decode())
        cli_result = json.loads(direct.stderr)
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "pixl_commit",
            "arguments": {"store": "state.px/state.px", "candidate": "candidate.px", "expect": codec.digest(self.doc)}}}
        rpc = subprocess.run(command + ["mcp", "--root", str(self.root)], input=json.dumps(request).encode() + b"\n",
            capture_output=True, check=False, timeout=30)
        self.assertEqual(rpc.returncode, 0, rpc.stderr.decode())
        response = json.loads(rpc.stdout)["result"]
        self.assertTrue(response["isError"])
        for key in ("error", "detail", "category", "recovery"):
            self.assertEqual(cli_result[key], response["structuredContent"][key], key)
        self.assertEqual(cli_result["error"], "directory_required")
        self.assertEqual(self.snapshot(), before)

    def test_mcp_initializers_reject_file_store_before_publication(self):
        before = self.snapshot()
        for tool in ("pixl_init", "pixl_intake"):
            response = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                "params": {"name": tool, "arguments": {"store": "state.px/state.px"}}}, self.root)["result"]
            self.assertTrue(response["isError"])
            self.assertEqual(response["structuredContent"]["error"], "directory_required")
            self.assertEqual(self.snapshot(), before)

    def test_auxiliary_plar_lock_file_gets_directory_recovery_without_inventing_a_store(self):
        project = self.root / "plar consumer"
        shutil.copytree(Path(__file__).resolve().parents[1] / "examples/plar-project", project)
        document = json.loads((project / "plar.txt").read_bytes())
        expected = plar.read(project)["hash"]
        auxiliary = project / ".pixl/plar-lock"
        auxiliary.parent.mkdir(exist_ok=True)
        auxiliary.write_bytes(b"retained conflicting project file\n")
        before = self.snapshot()
        with self.assertRaises(codec.PixlError) as caught:
            plar.save(project, document, expected)
        self.assertEqual(caught.exception.code, "directory_required")
        self.assertIn(str(auxiliary), caught.exception.detail)
        self.assertNotIn("state.px", caught.exception.detail)
        result = diagnostics.error_result("pixl_plar_save", caught.exception, {"path": "plar.txt", "expect": expected})
        self.assertEqual(result["category"], "invalid_authoring")
        self.assertEqual(result["recovery"]["action"], "correct_directory_path")
        self.assertNotIn("store", result["identity"])
        self.assertIn("For a store argument", result["recovery"]["detail"])
        self.assertIn("Auxiliary lock/output directories do not require a state.px file", result["recovery"]["detail"])
        self.assertNotIn("operation", result["recovery"])
        self.assertEqual(self.snapshot(), before)

    def test_discovery_describes_every_store_argument_including_nested_prepare(self):
        parsers = [cli.parser()]
        cli_help = []
        while parsers:
            current = parsers.pop()
            for action in current._actions:
                if isinstance(action, argparse._SubParsersAction):
                    parsers.extend(action.choices.values())
                elif action.dest == "store":
                    cli_help.append(action.help)
        declarations = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, self.root)["result"]["tools"]
        mcp_help = [t["inputSchema"]["properties"]["store"]["description"] for t in declarations if "store" in t["inputSchema"]["properties"]]
        self.assertGreaterEqual(len(cli_help), 10)
        self.assertGreaterEqual(len(mcp_help), 10)
        for description in cli_help + mcp_help:
            self.assertIn("directory", description)
            self.assertIn("STORE/state.px", description)
        shown = subprocess.run([sys.executable, "-B", "-m", "pixl", "commit", "--help"], capture_output=True, check=False, timeout=30)
        self.assertEqual(shown.returncode, 0, shown.stderr.decode())
        self.assertIn("Store directory", shown.stdout.decode())
        self.assertIn("STORE/state.px", shown.stdout.decode())


if __name__ == "__main__":
    unittest.main()
