import json
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import codec, graph, service, store
from tests.support import sample


class IntakeOperationTests(unittest.TestCase):
    def test_intake_has_no_invented_style_and_survives_cold_load(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = service.call(
                "pixl_intake",
                {"store": ".pixl", "name": "Item family", "brief": "Canvas undecided"},
                root,
            )
            doc = store.load(root / ".pixl")
            self.assertEqual(doc.format, 2)
            self.assertEqual(codec.digest(doc), result["hash"])
            self.assertFalse(any(r.kind == "C" for r in doc.records.values()))
            project = doc.records["project"].fields
            self.assertNotIn("ct", project)
            self.assertEqual(project["br"], "Canvas undecided")
            self.assertEqual(project["in"], [])
            self.assertEqual(doc.records["user"].fields["rl"], codec.Symbol("user"))
            report = service.call("pixl_workflow", {"path": ".pixl/state.px"}, root)
            self.assertEqual(report["format"], 2)
            self.assertEqual(report["ready"], [])

    def test_host_adapter_preserves_explicit_format(self):
        data = {"format": 2, "revision": 0, "records": []}
        doc = service.from_json(data)
        self.assertEqual(doc.format, 2)
        self.assertEqual(codec.encode(doc), b"PX2 0\n")
        data.pop("format")
        self.assertEqual(service.from_json(data).format, 1)

    def test_px1_registry_remains_closed(self):
        doc = codec.Document(
            records={
                "user": codec.Record(
                    "user", "A", {"nm": "User", "rl": codec.Symbol("user")}
                )
            }
        )
        with self.assertRaisesRegex(codec.PixlError, "field_type"):
            graph.validate(doc)
        doc.format = 2
        graph.validate(doc)

    def test_store_refuses_implicit_format_migration(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = sample(root)
            store.initialize(root / "store", doc, root)
            candidate = deepcopy(doc)
            candidate.revision += 1
            candidate.format = 2
            with self.assertRaisesRegex(codec.PixlError, "format_change"):
                store.commit(root / "store", candidate, codec.digest(doc), root)
            self.assertEqual(
                codec.encode(store.load(root / "store")), codec.encode(doc)
            )

    def test_cli_intake_decode_encode_and_workflow_from_project(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            runner = (
                Path(__file__).resolve().parents[1] / "plugins/pixl/scripts/pixl.py"
            )

            # Source module route here; copied distribution has its own integration test.
            def cli(*args):
                result = subprocess.run(
                    [sys.executable, "-m", "pixl", *args],
                    capture_output=True,
                    check=False,
                    timeout=15,
                )
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                return json.loads(result.stdout) if result.stdout else None

            self.assertTrue(runner.is_file())
            cli(
                "intake",
                str(root / ".pixl"),
                "--root",
                str(root),
                "--brief",
                "No chosen canvas",
            )
            data = cli("decode", str(root / ".pixl/state.px"))
            self.assertEqual(data["format"], 2)
            adapter = root / "adapter.json"
            adapter.write_text(json.dumps(data), encoding="utf-8")
            cli("encode", str(adapter), "--out", str(root / "roundtrip.px"))
            self.assertEqual(
                (root / "roundtrip.px").read_bytes(),
                (root / ".pixl/state.px").read_bytes(),
            )
            report = cli("workflow", str(root / "roundtrip.px"), "--root", str(root))
            self.assertEqual(report["format"], 2)
            self.assertTrue(report["files_verified"])

    def test_mcp_intake_and_cold_workflow_report(self):
        with TemporaryDirectory() as tmp:
            calls = [
                {"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
                {
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": "pixl_intake",
                        "arguments": {"store": ".pixl", "brief": "Unknown canvas"},
                    },
                },
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "pixl_workflow",
                        "arguments": {"path": ".pixl/state.px"},
                    },
                },
            ]
            result = subprocess.run(
                [sys.executable, "-m", "pixl", "mcp", "--root", tmp],
                input="".join(json.dumps(row) + "\n" for row in calls),
                capture_output=True,
                text=True,
                check=False,
                timeout=15,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            responses = [json.loads(line) for line in result.stdout.splitlines()]
            self.assertTrue(
                {"pixl_intake", "pixl_workflow"}
                <= {t["name"] for t in responses[0]["result"]["tools"]}
            )
            intake_tool = next(
                t for t in responses[0]["result"]["tools"] if t["name"] == "pixl_intake"
            )
            self.assertFalse(intake_tool["annotations"]["readOnlyHint"])
            self.assertFalse(responses[1]["result"].get("isError", False))
            report = responses[2]["result"]["structuredContent"]
            self.assertEqual(report["format"], 2)
            self.assertEqual(report["tasks"], [])


if __name__ == "__main__":
    unittest.main()
