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

    def test_refresh_tracks_requirement_changes_and_transitive_dependents(self):
        before = plar.read(self.root)
        self.document["assets"][0]["requirements"][0]["value"] = [80, 16]
        saved = plar.save(self.root, self.document, before["hash"])
        self.assertEqual(saved["changes"]["direct_assets"], ["queue.working"])
        self.assertEqual(
            saved["changes"]["affected_assets"],
            ["queue.ready", "queue.retry", "queue.working"],
        )
        self.assertEqual(saved["changes"]["unaffected_assets"], ["queue.start"])
        compared = service.call("pixl_plar_read", {"since": before["hash"]}, self.root)
        self.assertEqual(compared["changes"], saved["changes"])
        self.document["assets"][0]["next"] = "Continue with the same requirements"
        progress = plar.save(self.root, self.document, saved["hash"])
        self.assertEqual(progress["changes"]["affected_assets"], [])
        self.assertEqual(
            plar.read(self.root, since=progress["hash"])["changes"]["affected_assets"],
            [],
        )

    def test_refresh_source_drift_and_dependency_issues_do_not_rebind(self):
        self.add_reference()
        (self.root / "style.txt").write_text("changed", encoding="utf-8")
        before = (self.root / "plar.txt").read_bytes()
        queue = plar.read(self.root)
        self.assertEqual(queue["changes"]["changed_sources"], ["style"])
        self.assertEqual(queue["changes"]["direct_assets"], ["queue.working"])
        self.assertEqual(
            queue["changes"]["affected_assets"],
            ["queue.ready", "queue.retry", "queue.working"],
        )
        focused = plar.read(self.root, asset_id="queue.ready")
        self.assertEqual(
            focused["dependency_issues"], {"queue.working": ["source style: changed"]}
        )
        self.assertEqual((self.root / "plar.txt").read_bytes(), before)

    def test_refresh_reports_added_removed_roles_and_checks_history_bytes(self):
        before = plar.read(self.root)
        self.document["assets"] = [
            r for r in self.document["assets"] if r["id"] != "queue.retry"
        ]
        paused = copy.deepcopy(self.document["assets"][1])
        paused["id"] = "queue.paused"
        paused["delivery"]["path"] = "assets/paused.png"
        self.document["assets"].append(paused)
        saved = plar.save(self.root, self.document, before["hash"])
        self.assertEqual(saved["changes"]["added_assets"], ["queue.paused"])
        self.assertEqual(saved["changes"]["removed_assets"], ["queue.retry"])
        history = self.root / ".pixl/plar-history" / (before["hash"] + ".json")
        history.write_text(json.dumps(self.document), encoding="utf-8")
        with self.assertRaisesRegex(PixlError, "retained PLAR bytes"):
            plar.read(self.root, since=before["hash"])
        with self.assertRaises(PixlError):
            plar.read(self.root, since="../outside")
        with self.assertRaisesRegex(PixlError, "compare the queue"):
            plar.read(self.root, asset_id="queue.ready", since=saved["hash"])

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

    def add_reference(self):
        source = self.root / "style.txt"
        source.write_text("Reference bytes for a binding test.", encoding="utf-8")
        self.document["sources"].append({"id": "style", "path": "style.txt"})
        # A dependent asset must carry the baseline's visual input even when its
        # own source locators do not mention that file.
        self.document["assets"][0]["references"] = [
            {
                "source": "style",
                "role": "identity",
                "instructions": "Preserve this subject.",
            }
        ]
        plar.save(self.root, self.document, plar.read(self.root)["hash"])
        return source

    def test_transitive_reference_context_survives_delegation(self):
        self.add_reference()
        packet = plar.read(self.root, asset_id="queue.ready")
        self.assertEqual(packet["project_root"], str(self.root.resolve()))
        baseline = packet["dependencies"][0]
        self.assertEqual(baseline["id"], "queue.working")
        self.assertTrue(baseline["requirements"])
        self.assertEqual(baseline["references"][0]["role"], "identity")
        reference = packet["visual_references"][0]
        self.assertEqual(reference["asset_id"], "queue.working")
        self.assertEqual(reference["absolute_path"], str(self.root / "style.txt"))
        self.assertEqual(reference["sha256"], reference["observed_sha256"])

    def test_changed_dependency_reference_is_visible_without_selecting_it(self):
        source = self.add_reference()
        before = plar.read(self.root, asset_id="queue.ready")
        source.write_text(
            "A different source image would have different bytes.", encoding="utf-8"
        )
        after = plar.read(self.root, asset_id="queue.ready")
        self.assertNotEqual(before["requirements_hash"], after["requirements_hash"])
        self.assertIn("source style: changed", after["dependencies"][0]["issues"])
        self.assertEqual(after["visual_references"][0]["binding"], "changed")

    def test_requirements_identity_ignores_progress_but_tracks_dependency_contract(
        self,
    ):
        before = plar.read(self.root, asset_id="queue.ready")
        self.document["assets"][0]["status"] = "in_progress"
        self.document["assets"][0]["next"] = "Inspect the generated candidate"
        self.document["assets"][2]["purpose"] = "Unrelated retry work"
        plar.save(self.root, self.document, before["hash"])
        progress = plar.read(self.root, asset_id="queue.ready")
        self.assertNotEqual(before["hash"], progress["hash"])
        self.assertEqual(before["requirements_hash"], progress["requirements_hash"])
        self.assertEqual(progress["dependencies"][0]["status"], "in_progress")
        self.document["assets"][0]["requirements"][0]["value"] = [128, 16]
        plar.save(self.root, self.document, progress["hash"])
        changed = plar.read(self.root, asset_id="queue.ready")
        self.assertNotEqual(progress["requirements_hash"], changed["requirements_hash"])

    def test_context_can_rebase_without_changing_requirement_identity(self):
        self.add_reference()
        before = plar.read(self.root, asset_id="queue.ready")
        with TemporaryDirectory() as moved:
            shutil.copytree(self.root, moved, dirs_exist_ok=True)
            after = plar.read(moved, asset_id="queue.ready")
            self.assertEqual(before["requirements_hash"], after["requirements_hash"])
            self.assertNotEqual(before["project_root"], after["project_root"])
            self.assertNotEqual(
                before["visual_references"][0]["absolute_path"],
                after["visual_references"][0]["absolute_path"],
            )

    def test_unknown_reference_source_or_role_is_rejected(self):
        self.document["assets"][0]["references"] = [
            {
                "source": "absent",
                "role": "identity",
                "instructions": "Keep this subject",
            }
        ]
        with self.assertRaises(PixlError):
            plar.validate(self.document, self.root)
        self.document["assets"][0]["references"][0].update(
            source="brief", role="invented"
        )
        with self.assertRaises(PixlError):
            plar.validate(self.document, self.root)
