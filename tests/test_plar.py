import copy
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from jsonschema import Draft202012Validator

from pixl import codec, plar, service, store
from pixl.codec import PixlError
from pixl.mcp import TOOLS
from tests.lifecycle_support import sample

ROOT = Path(__file__).resolve().parents[1]


class PLARTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "examples/plar-project", self.root, dirs_exist_ok=True)
        self.document = json.loads((self.root / "plar.txt").read_text("utf-8"))

    def test_focus_binds_consumers_and_keeps_exact_contract(self):
        packet = plar.read(self.root, asset_id="queue.working")
        self.assertEqual(packet["asset"]["delivery"]["path"], "assets/working.png")
        self.assertEqual(len(packet["asset"]["consumers"]), 2)
        self.assertEqual({row["binding"] for row in packet["sources"]}, {"current"})
        self.assertEqual([row["id"] for row in packet["queue"]], ["queue.working"])
        self.assertTrue(packet["coverage"]["unresolved"])
        self.assertEqual(packet["asset"], self.document["assets"][0])

    def test_cas_history_and_source_drift_survive_an_unrelated_edit(self):
        original = (self.root / "plar.txt").read_bytes()
        before = plar.read(self.root)
        (self.root / "src/queue-view.ts").write_text(
            "// changed consumer", encoding="utf-8"
        )
        self.document["assets"][0]["next"] = "Reconcile the changed view"
        saved = plar.save(self.root, self.document, before["hash"])
        self.assertEqual(
            (
                self.root / ".pixl/plar-history" / (before["hash"] + ".json")
            ).read_bytes(),
            original,
        )
        self.assertIn("source view: changed", saved["queue"][0]["issues"])
        with self.assertRaisesRegex(PixlError, "reload"):
            plar.save(self.root, self.document, before["hash"])

    def test_new_source_binding_missing_asset_and_unbound_source(self):
        (self.root / "plar.txt").unlink()
        for source in self.document["sources"]:
            source.pop("sha256")
        raw = copy.deepcopy(self.document)
        (self.root / "src/queue.ts").unlink()
        saved = plar.save(self.root, self.document, "new")
        self.assertEqual(raw, self.document, "saving must not mutate caller input")
        self.assertTrue(any(row["binding"] == "missing" for row in saved["sources"]))
        self.assertFalse((self.root / "assets/working.png").exists())
        with self.assertRaises(PixlError):
            plar.save(self.root, self.document, "new")

    def test_bad_reference_cycle_and_escape_are_rejected(self):
        for mutate in (
            lambda d: d["assets"][0]["depends_on"].append("missing"),
            lambda d: d["assets"][0]["depends_on"].append("queue.working"),
            lambda d: d["sources"][0].update(path="../outside"),
            lambda d: d["assets"][0]["consumers"][0].update(source="missing"),
            lambda d: d["assets"].append(copy.deepcopy(d["assets"][0])),
        ):
            candidate = copy.deepcopy(self.document)
            mutate(candidate)
            with self.assertRaises(PixlError):
                plar.validate(candidate, self.root)

    def test_dependency_focus_and_missing_integration_are_reported(self):
        self.document["assets"][1]["depends_on"] = ["queue.working"]
        self.document["assets"][0]["status"] = "integrated"
        plar.save(self.root, self.document, plar.read(self.root)["hash"])
        packet = plar.read(self.root, asset_id="queue.ready")
        self.assertEqual(packet["dependencies"][0]["id"], "queue.working")
        self.assertIn(
            "integrated destination is missing",
            plar.read(self.root, asset_id="queue.working")["queue"][0]["issues"],
        )

    def test_nonfinite_duplicate_json_and_unknown_version_rejected(self):
        for value in ('{"version":1,"version":1}', '{"version":NaN}'):
            (self.root / "broken.txt").write_text(value, encoding="utf-8")
            with self.assertRaises(PixlError):
                plar.read(self.root, "broken.txt")
        self.document["version"] = 2
        with self.assertRaises(PixlError):
            plar.validate(self.document, self.root)

    def test_cli_from_another_working_directory(self):
        runner = ROOT / "plugins/pixl/scripts/pixl.py"
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(runner),
                "plar",
                "read",
                "--root",
                str(self.root),
                "--asset",
                "queue.working",
            ],
            cwd=self.root,
            capture_output=True,
            check=False,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["asset"]["id"], "queue.working")

    def test_stdio_save_then_focused_read(self):
        (self.root / "plar.txt").unlink()
        requests = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "pixl_plar_save",
                    "arguments": {"document": self.document, "expect": "new"},
                },
            },
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "pixl_plar_read",
                    "arguments": {"asset_id": "queue.working"},
                },
            },
        ]
        result = subprocess.run(
            [sys.executable, "-B", "-m", "pixl", "mcp", "--root", str(self.root)],
            cwd=ROOT,
            input="".join(json.dumps(r) + "\n" for r in requests),
            capture_output=True,
            check=False,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        replies = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertFalse(replies[0]["result"].get("isError", False), replies)
        self.assertEqual(
            replies[1]["result"]["structuredContent"]["asset"]["id"], "queue.working"
        )

    def test_inline_commit_preserves_store_checks_without_a_wire_file(self):
        document = sample(self.root)
        current = store.initialize(self.root / ".px2", document, self.root)
        document.revision = 1
        document.records["task"].fields["st"] = codec.Symbol("active")

        def data(value):
            if isinstance(value, codec.Ref):
                return {"$ref": value.id}
            if isinstance(value, codec.Symbol):
                return {"$symbol": value.value}
            if isinstance(value, list):
                return [data(item) for item in value]
            if isinstance(value, dict):
                return {key: data(item) for key, item in value.items()}
            return value

        payload = {
            "format": 2,
            "revision": 1,
            "records": [
                {"id": row.id, "kind": row.kind, "fields": data(row.fields)}
                for row in document.records.values()
            ],
        }
        args = {"store": ".px2", "expect": current["hash"], "document": payload}
        result = service.call("pixl_commit", args, self.root)
        self.assertEqual(result["revision"], 1)
        self.assertEqual(
            store.load(self.root / ".px2").records["task"].fields["st"].value, "active"
        )
        with self.assertRaisesRegex(PixlError, "reload"):
            service.call("pixl_commit", args, self.root)
        with self.assertRaises(PixlError):
            service.call("pixl_commit", dict(args, candidate="unused.px"), self.root)
        schema = next(s for n, _, s in TOOLS if n == "pixl_commit")
        self.assertFalse(
            Draft202012Validator(schema).is_valid(dict(args, candidate="unused.px"))
        )
        self.assertTrue(Draft202012Validator(schema).is_valid(args))
