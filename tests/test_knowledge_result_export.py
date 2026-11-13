"""Exact retrieval exports preserve source scope, authority and failed observations."""

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pixl import mcp, service
from pixl.codec import PixlError

EXPORT_TOOLS = {"pixl_sources", "pixl_knowledge", "pixl_source"}


class KnowledgeResultExportTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "consumer"
        self.root.mkdir()
        self.kit = self.base / "kit"
        self.resources = self.kit / "resources"
        self.source_name = "training/original-docs/source.md"
        source = self.resources / self.source_name
        source.parent.mkdir(parents=True)
        self.library_bytes = "# Méthod source\nExample timing is not a project requirement.\n".encode()
        source.write_bytes(self.library_bytes)
        self.source_hash = hashlib.sha256(self.library_bytes).hexdigest()
        self.inventory = {"version": 1, "documents": [{"id": "research", "path": self.source_name,
            "sha256": self.source_hash, "lines": 2, "previous": None}]}
        (self.resources / "training/source-inventory.json").write_text(json.dumps(self.inventory), encoding="utf-8")
        self.method = {"id": "sample-method", "title": "Review the assigned timing", "applies_to": ["declared frame timing"],
            "requires": ["Actual authored durations"], "procedure": ["Compare actual timing to the assignment."],
            "checks": ["Preserve the assigned durations."], "pitfalls": ["A source example does not establish this project's timing."],
            "sources": [{"path": self.source_name, "start": 1, "end": 2}],
            "poc": {"kind": "fixture", "procedure": ["Inspect reference timing only."], "acceptance": ["Reference identity only."]}}
        knowledge = self.resources / "knowledge/pixel-art.json"
        knowledge.parent.mkdir()
        knowledge.write_text(json.dumps({"version": 1, "methods": [self.method]}), encoding="utf-8")
        environment = patch.dict(os.environ, {"PIXL_PLUGIN_ROOT": str(self.kit)})
        environment.start()
        self.addCleanup(environment.stop)

    def source_args(self, **extra):
        return {"path": self.source_name, "scope": "library", "expect": self.source_hash,
                "start": 1, "end": 2, **extra}

    def exported(self, name, arguments, destination):
        expected = service.call(name, arguments, self.root)
        response = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
            "params": {"name": name, "arguments": arguments | {"result_path": destination}}}, self.root)
        self.assertFalse(response["result"].get("isError"), response)
        summary = response["result"]["structuredContent"]
        data = (self.root / destination).read_bytes()
        self.assertTrue(summary["result_saved"])
        self.assertEqual(summary["result_path"], destination)
        self.assertEqual(summary["result_sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(summary["result_bytes"], len(data))
        self.assertEqual(summary["hash_domains"]["result_sha256"], "file_sha256")
        self.assertEqual(json.loads(data), expected)
        return json.loads(data)

    def test_sources_export_preserves_verified_library_inventory(self):
        before = (self.resources / "training/source-inventory.json").read_bytes()
        result = self.exported("pixl_sources", {}, "work/sources.json")
        self.assertTrue(result["files_verified"])
        self.assertEqual(result["root"], str(self.resources))
        self.assertEqual(result["documents"], self.inventory["documents"])
        self.assertEqual((self.resources / "training/source-inventory.json").read_bytes(), before)

    def test_method_index_and_detail_export_preserve_conditions_and_limits(self):
        index = self.exported("pixl_knowledge", {}, "work/index.json")
        detail = self.exported("pixl_knowledge", {"method": "sample-method"}, "work/method.json")
        self.assertEqual(index["methods"][0]["id"], self.method["id"])
        self.assertEqual(detail, self.method)
        self.assertEqual(detail["pitfalls"], self.method["pitfalls"])
        self.assertEqual(detail["poc"], self.method["poc"])

    def test_source_export_preserves_exact_unicode_slice_and_source_identity(self):
        result = self.exported("pixl_source", self.source_args(start=2), "work/source.json")
        self.assertEqual(result["text"], "Example timing is not a project requirement.\n")
        self.assertEqual(result["sha256"], self.source_hash)
        self.assertEqual(result["hash_domains"]["sha256"], "file_sha256")
        self.assertEqual((result["start"], result["end"]), (2, 2))

    def test_source_default_project_scope_does_not_switch_to_library_on_export(self):
        project = self.root / self.source_name
        project.parent.mkdir(parents=True)
        project.write_bytes(b"# Project\nIts own requirement.\n")
        arguments = self.source_args(expect=hashlib.sha256(project.read_bytes()).hexdigest())
        del arguments["scope"]
        result = self.exported("pixl_source", arguments, "work/project-source.json")
        self.assertEqual(result["text"], project.read_text())
        self.assertNotEqual(result["sha256"], self.source_hash)

    def test_existing_results_and_export_escapes_are_rejected_before_lookup(self):
        existing = self.root / "existing.json"
        existing.write_bytes(b"preserve exact previous retrieval")
        for name, arguments in (("pixl_sources", {}), ("pixl_knowledge", {}), ("pixl_source", self.source_args())):
            for target in ("existing.json", "../kit/resources/stolen.json", (self.resources / "absolute.json").as_posix()):
                with self.subTest(tool=name, target=target), self.assertRaises(PixlError):
                    service.call(name, arguments | {"result_path": target}, self.root)
        self.assertEqual(existing.read_bytes(), b"preserve exact previous retrieval")
        self.assertFalse((self.resources / "stolen.json").exists())

    def test_stale_source_and_budget_failure_do_not_publish_successful_export(self):
        for key, arguments, error in (
            ("stale", self.source_args(expect="0" * 64), "source_hash"),
            ("budget", self.source_args(budget=1), "source_budget"),
            ("range", self.source_args(start=3), "source_range"),
        ):
            with self.subTest(case=key), self.assertRaisesRegex(PixlError, error):
                service.call("pixl_source", arguments | {"result_path": f"work/{key}.json"}, self.root)
            self.assertFalse((self.root / f"work/{key}.json").exists())
        self.assertFalse((self.root / "work").exists())

    def test_failed_inventory_or_unknown_method_leaves_no_export(self):
        (self.resources / self.source_name).write_bytes(b"changed source revision")
        with self.assertRaisesRegex(PixlError, "source_hash"):
            service.call("pixl_sources", {"result_path": "work/sources.json"}, self.root)
        with self.assertRaisesRegex(PixlError, "unknown_method"):
            service.call("pixl_knowledge", {"method": "unknown", "result_path": "work/method.json"}, self.root)
        self.assertFalse((self.root / "work").exists())

    def test_mcp_discovery_marks_optional_exports_without_new_tools(self):
        tools = mcp.dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, self.root)["result"]["tools"]
        selected = [item for item in tools if item["name"] in EXPORT_TOOLS]
        self.assertEqual(len(selected), 3)
        for item in selected:
            self.assertIn("result_path", item["inputSchema"]["properties"])
            self.assertNotIn("result_path", item["inputSchema"].get("required", []))
            self.assertFalse(item["annotations"]["readOnlyHint"])


if __name__ == "__main__":
    unittest.main()
