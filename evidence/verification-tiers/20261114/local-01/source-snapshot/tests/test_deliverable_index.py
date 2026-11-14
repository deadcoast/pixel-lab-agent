"""Consumer indexes retain real local identities, not new artistic acceptance."""

import copy
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, delivery, graph, mcp, retention, service, store
from pixl.codec import PixlError, Record, Ref, Symbol
from tests import family_support, lifecycle_support


class DeliverableIndexTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.folder = self.root / ".pixl"
        self.state = self.folder / "state.px"

    def fixture(self, metadata=None, module=False):
        def sample(root):
            doc = lifecycle_support.sample(root)
            if module:
                path = root / ("kit/resources/module.ts" if module == "library" else "retained-module.ts")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("export const frames = [[0, 0, 2, 2]];\n", encoding="utf-8")
                if module == "library":
                    (root / "kit/bundle-manifest.json").write_text(json.dumps({"files": [
                        {"path": "resources/module.ts", "sha256": graph.file_hash(path)},
                    ]}), encoding="utf-8")
                doc.records["module.source"] = Record("module.source", "S", {
                    "ur": path.relative_to(root).as_posix(), "dg": graph.file_hash(path), "ln": [1, 1],
                    "at": "2026-11-14", "au": Symbol("local"),
                })
                doc.records["rendering"] = Record("rendering", "I", {
                    "pr": Ref("project"), "wh": Ref("user"), "ky": "rendering",
                    "st": Symbol("confirmed"), "vl": {"module": "src/animation.ts", "durations_ms": [100]},
                    "so": [Ref("module.source")], "wy": "Use the explicitly retained module.",
                })
                doc.records["project"].fields["in"].append(Ref("rendering"))
                doc.records["contract"].fields["ch"].append(Ref("rendering"))
            return doc

        def candidate(doc, root, id_):
            result = lifecycle_support.add_candidate(doc, root, id_)
            if metadata is not None:
                doc.records[id_].fields["mt"] = copy.deepcopy(metadata)
            return result

        with (patch.object(family_support, "sample", side_effect=sample),
              patch.object(family_support, "add_candidate", side_effect=candidate)):
            family_support.family(self.root, self.folder)

    def publish(self, doc):
        old = store.load(self.folder)
        doc.revision = old.revision + 1
        store.commit(self.folder, doc, codec.digest(old), self.root)

    def snapshot(self, candidate="package"):
        return delivery.snapshot(self.folder, codec.digest(store.load(self.folder)),
                                 "delivery.output", candidate, self.root)

    def nominate(self, candidate="package", engine=None):
        doc = store.load(self.folder)
        doc.records["delivery.task"].fields["ca"] = [Ref(candidate)]
        if engine:
            for criterion, status in [("q.continuity", "pass"), ("q.delivery.engine", engine)]:
                lifecycle_support.add_verdict(doc, self.root, candidate, criterion, status, "review." + criterion)
            doc.records["delivery.task"].fields["st"] = Symbol("active")
        self.publish(doc)
        if engine == "pass":
            doc = store.load(self.folder)
            doc.records["delivery.task"].fields["st"] = Symbol("done")
            self.publish(doc)

    def report(self, candidate=None):
        return service.call("pixl_family", {"path": ".pixl/state.px", "output": "delivery.output",
                                            "view": "consumer", **({"candidate": candidate} if candidate else {})}, self.root)

    def inventory(self):
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in self.root.rglob("*") if path.is_file()}

    def test_complete_review_is_distinct_from_immutable_creation_acceptance(self):
        self.fixture()
        self.snapshot()
        self.nominate(engine="pass")
        before = self.inventory()
        result = self.report()
        self.assertTrue(result["family"]["current_eligible"])
        self.assertFalse(result["package"]["creation_acceptance"]["accepted"])
        self.assertEqual(result["unresolved"], [])
        self.assertEqual(result["hash_domains"]["hash"], "canonical_state_sha256")
        for row in result["assets"]:
            data = (self.root / row["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])
            self.assertEqual(len(data), row["bytes"])
            self.assertNotEqual(row["path"], row["source_path"])
            self.assertTrue(row["review"]["nominated"])
            self.assertEqual(row["lineage"]["candidate"], row["candidate"])
            self.assertFalse(row["lineage"]["remote_verified"])
        self.assertEqual(before, self.inventory())

    def test_no_nominee_does_not_select_newest_retained_package(self):
        self.fixture()
        self.snapshot()
        self.snapshot("package.new")
        result = self.report()
        self.assertIsNone(result["package"])
        self.assertEqual(result["assets"], [])
        self.assertFalse(result["family"]["current_eligible"])
        self.assertIn("package_unselected", {row["code"] for row in result["unresolved"]})
        self.assertEqual(self.report("package")["package"]["candidate"], "package")

    def test_explicit_historical_package_preserves_its_members_and_nomination(self):
        self.fixture()
        self.snapshot()
        self.snapshot("package.new")
        self.nominate("package.new", engine="pass")
        result = self.report("package")
        self.assertFalse(result["family"]["nominated"])
        self.assertFalse(result["family"]["current_eligible"])
        self.assertEqual(result["family"]["current_candidate"], "package.new")
        self.assertEqual(result["package"]["candidate"], "package")
        self.assertTrue(all(row["status"] == "unperformed" for row in result["family"]["requirements"]))
        self.assertEqual(result["refresh"]["arguments"]["candidate"], "package")
        self.assertNotIn("snapshots", result)

    def test_changed_member_selection_reports_stale_exact_historical_candidate(self):
        self.fixture()
        self.snapshot()
        self.nominate()
        doc = store.load(self.folder)
        new = copy.deepcopy(doc.records["member"])
        new.id = "member.next"
        doc.records[new.id] = new
        doc.records["member.task"].fields.update(st=Symbol("open"), ca=[Ref(new.id)])
        self.publish(doc)
        result = self.report()
        member = result["assets"][1]
        self.assertEqual(member["candidate"], "member")
        self.assertEqual(member["review"]["current_candidate"], "member.next")
        self.assertFalse(member["review"]["nominated"])
        self.assertFalse(result["family"]["current_eligible"])
        self.assertTrue(result["package"]["stale"])

    def test_missing_layout_is_explicit_and_declared_metadata_is_lossless(self):
        self.fixture(metadata={"rects": [[0, 0, 2, 2]], "purpose": Symbol("fixture"), "source": Ref("source")})
        self.snapshot()
        row = self.report("package")["assets"][0]
        self.assertEqual(row["metadata"]["layout_status"], "not_interpreted")
        self.assertEqual(row["metadata"]["value"]["purpose"], {"$symbol": "fixture"})
        self.assertEqual(row["metadata"]["value"]["source"], {"$ref": "source"})
        self.assertEqual(row["contract"]["declared"]["px"], [2, 2])
        self.assertTrue(row["contract"]["current_binding"])

    def test_missing_metadata_does_not_guess_frames_from_contract_or_kind(self):
        self.fixture()
        self.snapshot()
        row = self.report("package")["assets"][0]
        self.assertEqual(row["metadata"]["layout_status"], "not_declared")
        self.assertIsNone(row["metadata"]["value"])
        self.assertNotIn("frame_count", row)

    def test_integration_resolves_contract_choice_sources_for_cold_caller(self):
        self.fixture(module=True)
        self.snapshot()
        result = self.report("package")
        choice = next(row for row in result["integration"]["choices"] if row["id"] == "rendering")
        source = next(row for row in result["integration"]["sources"] if row["id"] == choice["sources"][0])
        self.assertEqual(choice["roles"], ["member_contract"])
        self.assertEqual(choice["value"]["module"], "src/animation.ts")
        self.assertEqual(source["path"], "retained-module.ts")
        self.assertEqual(graph.file_hash(self.root / source["path"]), source["sha256"])
        self.assertEqual(source["observed_sha256"], source["sha256"])
        self.assertTrue(source["current_binding"])
        self.assertEqual(source["lines"], [1, 1])

    def test_unavailable_and_failed_reviews_remain_explicit(self):
        for status in ("unavailable", "fail"):
            with self.subTest(status=status):
                self.fixture()
                self.snapshot()
                self.nominate(engine=status)
                result = self.report()
                self.assertFalse(result["family"]["current_eligible"])
                self.assertIn("review_" + status, {row["code"] for row in result["unresolved"]})
                if status == "unavailable":
                    # The next subcase gets a distinct project, preserving this one.
                    self.root = self.root / "second"
                    self.folder = self.root / ".pixl"
                    self.state = self.folder / "state.px"

    def test_pending_job_does_not_inherit_completed_family_eligibility(self):
        self.fixture()
        self.snapshot()
        self.nominate(engine="pass")
        doc = store.load(self.folder)
        doc.records["pending"] = Record("pending", "J", {
            "tk": Ref("member.task"), "tl": "synthetic", "ah": "a" * 64,
            "si": Symbol("unknown"), "ri": "", "ev": [],
        })
        self.publish(doc)
        result = self.report()
        self.assertFalse(result["family"]["current_eligible"])
        self.assertTrue(result["family"]["all_required_pass"])
        self.assertEqual(result["pending_jobs"], [{"id": "pending", "task": "member.task", "state": "unknown"}])
        self.assertIn("pending_job", {row["code"] for row in result["unresolved"]})

    def test_contract_drift_is_not_presented_as_frozen_package_metadata(self):
        self.fixture(module=True)
        self.snapshot()
        doc = store.load(self.folder)
        for record in doc.records.values():
            if record.kind == "T":
                record.fields["st"] = Symbol("open")
            if record.kind == "V":
                record.fields["ob"] = True
                for evidence in record.fields["ev"]:
                    doc.records[evidence.id].fields["ob"] = True
        doc.records["contract"].fields["li"] = "Changed declared lighting."
        doc.records["rendering"].fields["vl"]["durations_ms"] = [200]
        self.publish(doc)
        result = self.report("package")
        self.assertFalse(result["assets"][0]["contract"]["current_binding"])
        choice = next(row for row in result["integration"]["choices"] if row["id"] == "rendering")
        self.assertFalse(choice["current_binding"])
        self.assertEqual(choice["value"]["durations_ms"], [200])
        self.assertIn("contract", result["package"]["stale"])
        self.assertFalse(result["family"]["current_eligible"])

    def test_library_source_resolution_exposes_exact_retained_revision(self):
        self.fixture(module="library")
        self.snapshot()
        doc = store.load(self.folder)
        retention.retain(self.folder, codec.digest(doc), "kit", self.root)
        source_path = self.root / "kit/resources/module.ts"
        source_path.write_text("Updated implementation, not the retained source.\n", encoding="utf-8")
        before = self.inventory()
        result = self.report("package")
        source = next(row for row in result["integration"]["sources"] if row["id"] == "module.source")
        self.assertEqual(source["status"], "retained_revision")
        self.assertNotEqual(source["path"], source["uri"])
        self.assertEqual(graph.file_hash(self.root / source["path"]), source["sha256"])
        self.assertNotEqual(graph.file_hash(source_path), source["sha256"])
        self.assertEqual(self.inventory(), before)

    def test_report_and_code_members_need_no_raster_contract(self):
        self.fixture()
        doc = store.load(self.folder)
        for kind in ("report", "code"):
            task = copy.deepcopy(doc.records["member.task"])
            task.id = kind + ".task"
            task.fields.update(st=Symbol("open"), op=[Ref(kind + ".output")], ca=[], vr=[])
            output = copy.deepcopy(doc.records["member.output"])
            output.id = kind + ".output"
            output.fields.update(tk=Ref(task.id), kd=Symbol(kind), rq=[Ref("q.member.continuity")])
            del output.fields["ct"]
            doc.records[task.id], doc.records[output.id] = task, output
            doc.records["delivery.task"].fields["dp"].append(Ref(task.id))
            doc.records["delivery.output"].fields["mb"].append(Ref(output.id))
        self.publish(doc)
        doc = store.load(self.folder)
        for kind in ("report", "code"):
            path = self.root / (kind + ".txt")
            path.write_text("Synthetic " + kind, encoding="utf-8")
            doc.records[kind] = Record(kind, "X", {"nm": "Named " + kind, "ur": path.name,
                "dg": graph.file_hash(path), "kd": Symbol(kind), "of": Ref(kind + ".output")})
            doc.records[kind + ".task"].fields.update(st=Symbol("active"), ca=[Ref(kind)])
            lifecycle_support.add_verdict(doc, self.root, kind, "q.member.continuity", "pass", kind + ".review")
        self.publish(doc)
        doc = store.load(self.folder)
        for kind in ("report", "code"):
            doc.records[kind + ".task"].fields["st"] = Symbol("done")
        self.publish(doc)
        self.snapshot()
        rows = self.report("package")["assets"]
        self.assertEqual([row["kind"] for row in rows[-2:]], ["report", "code"])
        self.assertTrue(all(row["contract"] is None for row in rows[-2:]))

    def test_missing_or_changed_retained_file_fails_without_mutating_state(self):
        self.fixture()
        snapshot = self.snapshot()
        manifest = json.loads((self.root / snapshot["manifest"]).read_bytes())
        member = self.root / snapshot["package"] / manifest["files"][0]["path"]
        original = member.read_bytes()
        for changed in (b"corrupt", None):
            if changed is None:
                member.unlink()
            else:
                member.write_bytes(changed)
            before = self.inventory()
            with self.assertRaisesRegex(PixlError, "delivery_file"):
                self.report("package")
            self.assertEqual(self.inventory(), before)
            member.write_bytes(original)

    def test_explicit_output_candidate_and_path_failures_are_structured(self):
        self.fixture()
        self.snapshot()
        for args, code in [
            ({"path": ".pixl/state.px", "view": "consumer"}, "deliverable_output"),
            ({"path": ".pixl/state.px", "output": "delivery.output", "candidate": "package"}, "deliverable_view"),
            ({"path": ".pixl/state.px", "output": "delivery.output", "view": "consumer", "candidate": "member"}, "deliverable_candidate"),
            ({"path": "../outside.px", "output": "delivery.output", "view": "consumer"}, "path_escape"),
        ]:
            with self.subTest(code=code), self.assertRaisesRegex(PixlError, code):
                service.call("pixl_family", args, self.root)

    def test_default_family_report_is_unchanged(self):
        self.fixture()
        self.snapshot()
        doc = store.load(self.folder)
        self.assertEqual(service.family_report(self.state, self.root), delivery.report(doc, self.root))
        self.assertEqual(service.family_report(self.state, self.root, "delivery.output"),
                         service.family_report(self.state, self.root, "delivery.output", "complete"))

    def test_cold_cli_mcp_parity_export_and_no_overwrite(self):
        self.fixture(module=True)
        self.snapshot()
        self.nominate(engine="pass")
        before = self.inventory()
        arguments = ["family", str(self.state), "delivery.output", "--view", "consumer", "--root", str(self.root)]
        command = [sys.executable, "-B", "-m", "pixl"]
        cli = subprocess.run(command + arguments, capture_output=True, check=False, timeout=30)
        self.assertEqual(cli.returncode, 0, cli.stderr.decode())
        result = json.loads(cli.stdout)
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
            "name": "pixl_family", "arguments": {"path": ".pixl/state.px", "output": "delivery.output", "view": "consumer"}}}
        process = subprocess.run(command + ["mcp", "--root", str(self.root)],
                                 input=json.dumps(request).encode() + b"\n", capture_output=True, check=False, timeout=30)
        self.assertEqual(process.returncode, 0, process.stderr.decode())
        rpc = json.loads(process.stdout)["result"]
        self.assertFalse(rpc["isError"])
        self.assertEqual(result, rpc["structuredContent"])
        self.assertEqual(self.inventory(), before)
        exported = subprocess.run(command + arguments + ["--result-path", "consumer-index.json"],
                                  capture_output=True, check=False, timeout=30)
        receipt = json.loads(exported.stdout)
        self.assertTrue(receipt["result_saved"])
        self.assertEqual(json.loads((self.root / receipt["result_path"]).read_bytes()), result)
        preserved = self.inventory()
        retry = subprocess.run(command + arguments + ["--result-path", "consumer-index.json"],
                               capture_output=True, check=False, timeout=30)
        self.assertEqual(retry.returncode, 2)
        self.assertEqual(self.inventory(), preserved)
        schema = next(schema for name, _, schema in mcp.TOOLS if name == "pixl_family")
        self.assertEqual(schema["properties"]["view"]["enum"], ["complete", "consumer"])


if __name__ == "__main__":
    unittest.main()
