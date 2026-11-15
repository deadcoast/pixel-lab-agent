"""Explicit current multi-output work must not masquerade as a delivery output."""

import copy
import json
import shutil
import unittest
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, graph, jobs, plar, preparation_focus, service, store
from pixl.codec import PixlError, Record
from tests.test_plar_prepare import seed, write


class PreparationFocusTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.args, self.packet, self.plan, _ = seed(self.root)
        second = copy.deepcopy(self.plan["outputs"][0])
        second["id"] = "alternate"
        self.plan["outputs"].append(second)
        self.packet["criteria"] = write(self.root, "work/criteria.json", self.plan)
        write(self.root, self.args["packet"], self.packet)
        self.folder = self.root / ".pixl/assets/queue.working"
        self.head = self.folder / preparation_focus.NAME

    def prepare(self, args=None):
        return service.call("pixl_plar_prepare", args or self.args, self.root)

    def files(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_saved_marker_versions_preserve_numeric_one_and_reject_unsupported_without_focus_bypass(self):
        result = self.prepare()
        document = store.load(self.folder)
        artifact = next(record for record in document.records.values()
                        if record.fields.get("mt", {}).get("binding") == "pixl.plar.selection/1")
        location = self.root / artifact.fields["ur"]
        original = location.read_bytes()
        marker = json.loads(original)
        missing = object()
        for version in (1, 1.0, True, 2, None, missing):
            with self.subTest(version=repr(version)):
                current = copy.deepcopy(document)
                value = copy.deepcopy(marker)
                if version is missing:
                    value.pop("version")
                else:
                    value["version"] = version
                data = (json.dumps(value) + "\n").encode()
                location.write_bytes(data)
                candidate = current.records[artifact.id]
                candidate.fields["dg"] = sha256(data).hexdigest()
                before = self.files()
                operations = (
                    lambda: preparation_focus.binding(current, self.root, self.folder, "plar.txt", "queue.working",
                                                       result["task"], candidate.fields["ur"], candidate.fields["dg"]),
                    lambda: preparation_focus.task_store(current, self.root, result["task"], candidate),
                )
                for operation in operations:
                    if type(version) in (int, float) and version == 1:
                        self.assertIsNotNone(operation())
                    else:
                        with self.assertRaises(PixlError) as caught:
                            operation()
                        self.assertEqual(caught.exception.code, "adapter_version")
                self.assertEqual(self.files(), before)
        location.write_bytes(original)

    def test_marker_version_failure_is_distinct_from_absent_legacy_focus(self):
        result = self.prepare()
        self.head.unlink()
        document = store.load(self.folder)
        self.assertIsNone(preparation_focus.read(document, self.root, self.folder, "plar.txt", "queue.working"))
        artifact = next(record for record in document.records.values()
                        if record.fields.get("mt", {}).get("binding") == "pixl.plar.selection/1")
        marker = json.loads((self.root / artifact.fields["ur"]).read_bytes())
        marker["version"] = 2
        reference = write(self.root, artifact.fields["ur"], marker)
        artifact.fields["dg"] = reference["sha256"]
        before = self.files()
        with self.assertRaises(PixlError) as caught:
            preparation_focus.task_store(document, self.root, result["task"], artifact)
        self.assertEqual(caught.exception.code, "adapter_version")
        self.assertEqual(self.files(), before)

    def test_future_marker_cannot_bypass_focus_by_changing_its_input_shape(self):
        result = self.prepare()
        document = store.load(self.folder)
        artifact = next(record for record in document.records.values()
                        if record.fields.get("mt", {}).get("binding") == "pixl.plar.selection/1")
        marker = json.loads((self.root / artifact.fields["ur"]).read_bytes())
        marker.update(version=2, input={"renamed_future_input": True})
        reference = write(self.root, artifact.fields["ur"], marker)
        artifact.fields["dg"] = reference["sha256"]
        before = self.files()
        with self.assertRaises(PixlError) as caught:
            preparation_focus.task_store(document, self.root, result["task"], artifact)
        self.assertEqual(caught.exception.code, "adapter_version")
        self.assertEqual(self.files(), before)

    def settle(self, result):
        return jobs.observe(self.folder, codec.digest(store.load(self.folder)), result["job"]["id"], "failed",
                            {"kind": "local abandonment of undispatched controlled intent", "remote_executed": False}, root=self.root)

    def revised_args(self):
        plan = copy.deepcopy(self.plan)
        plan["outputs"][0]["criteria"][1]["check"] += " Preserve the scoped cool-blue accent."
        packet = copy.deepcopy(self.packet)
        packet["criteria"] = write(self.root, "work/revision/criteria.json", plan)
        write(self.root, "work/revision/packet.json", packet)
        return {**self.args, "packet": "work/revision/packet.json", "revise": True,
                "expect": codec.digest(store.load(self.folder))}

    def revision(self):
        first = self.prepare()
        self.settle(first)
        args = self.revised_args()
        return first, self.prepare(args), args

    def test_multioutput_focus_is_explicit_idempotent_and_not_delivery(self):
        result = self.prepare()
        before = self.files()
        focused = plar.read(self.root, asset_id="queue.working")
        self.assertNotIn("production", focused["asset"])
        self.assertEqual(focused["production"]["link_status"], "focused")
        self.assertEqual(focused["production"]["task"], result["task"])
        self.assertEqual([row["id"] for row in focused["production"]["outputs"]], result["outputs"])
        self.assertEqual(result["allocation"]["status"], "needs_output_link")
        self.assertEqual(result["preparation_focus"]["status"], "selected")
        retry = self.prepare()
        self.assertEqual(retry["preparation_focus"]["status"], "unchanged")
        self.assertEqual(retry["hash"], result["hash"])
        self.assertEqual(self.files(), before)

    def test_revision_focus_preserves_old_records_and_old_retry_cannot_steal_it(self):
        first = self.prepare()
        self.settle(first)
        before_doc = store.load(self.folder)
        old_head = self.head.read_bytes()
        args = self.revised_args()
        second = self.prepare(args)
        current = store.load(self.folder)
        for id_, record in before_doc.records.items():
            if id_ != "project":
                self.assertEqual(current.records[id_], record)
        self.assertIn(old_head, [p.read_bytes() for p in (self.folder / "preparation-focus").glob("*.json")])
        focused = plar.read(self.root, asset_id="queue.working")["production"]
        self.assertEqual(focused["task"], second["task"])
        self.assertEqual(focused["pending_jobs"], [second["job"]["id"]])
        self.assertFalse(plar.selection_bindings(current, first["task"], self.root, self.folder)[0]["selected_for_asset"])
        self.assertTrue(plar.selection_bindings(current, second["task"], self.root, self.folder)[0]["selected_for_asset"])
        for old_args in (self.args, {**self.args, "revise": True, "expect": codec.digest(current)}):
            before = self.files()
            with self.assertRaisesRegex(PixlError, "plar_focus"):
                self.prepare(old_args)
            self.assertEqual(self.files(), before)
        with self.assertRaisesRegex(PixlError, "plar_selection"):
            from pixl.plar_workflow import current_bindings
            current_bindings(current, first["task"], self.root, self.folder)

    def test_present_invalid_focus_refuses_without_unique_task_fallback(self):
        self.prepare()
        original = json.loads(self.head.read_bytes())
        changes = [
            lambda v: v.update(version=2),
            lambda v: v.update(asset_id="other.asset"),
            lambda v: v.update(plar_path="other-plar.txt"),
            lambda v: v.update(requirements_hash="0" * 64),
            lambda v: v.update(task="other.task"),
            lambda v: v.update(job="other.job"),
            lambda v: v["marker"].update(sha256="0" * 64),
            lambda v: v["marker"].update(input_sha256="0" * 64),
            lambda v: v["marker"].update(path="../outside.json"),
        ]
        for mutate in changes:
            value = copy.deepcopy(original)
            mutate(value)
            self.head.write_text(json.dumps(value), encoding="utf-8")
            before = self.files()
            self.assertEqual(plar.read(self.root, asset_id="queue.working")["production"]["status"], "unavailable")
            with self.assertRaises(PixlError):
                self.prepare()
            self.assertEqual(self.files(), before)
        self.head.write_bytes(b"{malformed")
        before = self.files()
        self.assertEqual(plar.read(self.root, asset_id="queue.working")["production"]["status"], "unavailable")
        with self.assertRaises(PixlError):
            self.prepare()
        self.assertEqual(self.files(), before)

    def test_absent_focus_preserves_legacy_unique_discovery_and_exact_repair(self):
        first = self.prepare()
        expected = self.head.read_bytes()
        self.head.unlink()
        self.assertEqual(plar.read(self.root, asset_id="queue.working")["production"]["link_status"], "discovered")
        retry = self.prepare()
        self.assertEqual(retry["hash"], first["hash"])
        self.assertEqual(self.head.read_bytes(), expected)

    def test_ambiguous_absence_requires_explicit_exact_prepared_intent(self):
        _first, second, args = self.revision()
        self.head.unlink()
        self.assertEqual(plar.read(self.root, asset_id="queue.working")["production"]["status"], "unavailable")
        before = self.files()
        with self.assertRaises(PixlError):
            self.prepare({**self.args, "revise": True, "expect": second["hash"]})
        with self.assertRaises(PixlError):
            self.prepare({k: v for k, v in args.items() if k not in {"revise", "expect"}})
        self.assertEqual(self.files(), before)
        recovered = self.prepare({**args, "expect": second["hash"]})
        self.assertEqual(recovered["hash"], second["hash"])
        self.assertEqual(plar.read(self.root, asset_id="queue.working")["production"]["task"], second["task"])

    def test_interrupted_head_publication_repairs_same_job_without_state_change(self):
        first = self.prepare()
        self.settle(first)
        args = self.revised_args()
        atomic = store._atomic

        def interrupt(path, data):
            if Path(path) == self.head:
                raise OSError("controlled focus publication interruption")
            return atomic(path, data)

        with patch("pixl.preparation_focus.store._atomic", side_effect=interrupt):
            second = self.prepare(args)
        self.assertEqual(second["preparation_focus"]["status"], "needs_reconciliation")
        self.assertEqual(json.loads(self.head.read_bytes())["task"], first["task"])
        recovered = self.prepare({**args, "expect": second["hash"]})
        self.assertEqual(recovered["hash"], second["hash"])
        self.assertEqual(json.loads(self.head.read_bytes())["task"], second["task"])
        self.assertEqual(len(jobs.report(store.load(self.folder), self.root, self.folder)["jobs"]), 2)

    def test_interrupted_plan_before_job_resumes_after_existing_focus(self):
        first = self.prepare()
        self.settle(first)
        args = self.revised_args()
        with patch("pixl.plar_prepare.jobs.prepare", side_effect=OSError("controlled plan-before-job interruption")), self.assertRaises(OSError):
            self.prepare(args)
        resumed = self.prepare({**args, "expect": codec.digest(store.load(self.folder))})
        self.assertEqual(resumed["preparation_focus"]["status"], "selected")
        self.assertEqual(json.loads(self.head.read_bytes())["task"], resumed["task"])

    def test_interrupted_plan_before_job_upgrades_legacy_without_prior_focus(self):
        first = self.prepare()
        self.settle(first)
        self.head.unlink()
        for snapshot in (self.folder / "preparation-focus").glob("*.json"):
            snapshot.unlink()
        args = self.revised_args()
        with patch("pixl.plar_prepare.jobs.prepare", side_effect=OSError("controlled legacy interruption")), self.assertRaises(OSError):
            self.prepare(args)
        resumed = self.prepare({**args, "expect": codec.digest(store.load(self.folder))})
        self.assertEqual(resumed["preparation_focus"]["status"], "selected")

    def test_concurrent_state_advance_does_not_publish_stale_focus(self):
        publish = preparation_focus.publish

        def advance(document, root, folder, path, selected, task_id, marker_path, marker_hash, **kwargs):
            job = next(r for r in document.records.values() if r.kind == "J" and r.fields["tk"].id == task_id)
            jobs.observe(folder, codec.digest(document), job.id, "failed", {"local": "concurrent undispatched withdrawal"}, root=root)
            return publish(document, root, folder, path, selected, task_id, marker_path, marker_hash, **kwargs)

        with patch("pixl.plar_prepare.preparation_focus.publish", side_effect=advance):
            result = self.prepare()
        self.assertEqual(result["preparation_focus"]["status"], "needs_reconciliation")
        self.assertIn("production changed", result["preparation_focus"]["reason"])
        self.assertFalse(self.head.exists())

    def test_old_orphan_marker_cannot_overtake_later_selection_after_head_loss(self):
        first = self.prepare()
        self.settle(first)
        self.head.unlink()
        for snapshot in (self.folder / "preparation-focus").glob("*.json"):
            snapshot.unlink()
        orphan_args = self.revised_args()
        with patch("pixl.plar_prepare.store.commit", side_effect=OSError("controlled before-task interruption")), self.assertRaises(OSError):
            self.prepare(orphan_args)
        other_plan = copy.deepcopy(self.plan)
        other_plan["outputs"][0]["criteria"][1]["check"] += " A separate scoped decision."
        other_packet = copy.deepcopy(self.packet)
        other_packet["criteria"] = write(self.root, "work/other/criteria.json", other_plan)
        write(self.root, "work/other/packet.json", other_packet)
        other = self.prepare({**self.args, "packet": "work/other/packet.json", "revise": True,
                              "expect": codec.digest(store.load(self.folder))})
        self.settle(other)
        self.head.unlink()
        before = self.files()
        with self.assertRaisesRegex(PixlError, "selection history exists"):
            self.prepare({**orphan_args, "expect": codec.digest(store.load(self.folder))})
        self.assertEqual(self.files(), before)

    def test_relocation_preserves_relative_focus_identity(self):
        result = self.prepare()
        with TemporaryDirectory() as temporary:
            copied = Path(temporary) / "consumer"
            shutil.copytree(self.root, copied)
            focused = plar.read(copied, asset_id="queue.working")["production"]
            self.assertEqual(focused["task"], result["task"])
            self.assertEqual(focused["link_status"], "focused")
            self.assertEqual((copied / result["preparation_focus"]["path"]).read_bytes(), self.head.read_bytes())

    def test_explicit_delivery_link_outranks_focus_and_other_task_types_are_not_reselected(self):
        first, second, _ = self.revision()
        doc = store.load(self.folder)
        original = doc.records[first["task"]]
        fields = copy.deepcopy(original.fields)
        fields.update(op=[], ca=[], vr=[])
        doc.records["connected.stage"] = Record("connected.stage", "T", fields)
        self.assertTrue(plar.selection_bindings(doc, "connected.stage", self.root, self.folder)[0]["selected_for_asset"])
        before = self.head.read_bytes()
        allocation, digest = plar._load(self.root / "plar.txt")
        asset = next(a for a in allocation["assets"] if a["id"] == "queue.working")
        asset["production"] = {"store": first["store"], "task": first["task"], "output": first["outputs"][0]}
        plar.save(self.root, allocation, digest)
        focused = plar.read(self.root, asset_id="queue.working")["production"]
        self.assertEqual(focused["link_status"], "linked")
        self.assertEqual(focused["task"], first["task"])
        self.assertEqual(self.head.read_bytes(), before)
        self.assertTrue(plar.selection_bindings(doc, first["task"], self.root, self.folder)[0]["selected_for_asset"])
        self.assertFalse(plar.selection_bindings(doc, second["task"], self.root, self.folder)[0]["selected_for_asset"])

    def test_single_to_multiple_keeps_explicit_link_and_reports_reconciliation(self):
        self.plan["outputs"].pop()
        self.packet["criteria"] = write(self.root, "work/criteria.json", self.plan)
        write(self.root, self.args["packet"], self.packet)
        first = self.prepare()
        self.settle(first)
        second_output = copy.deepcopy(self.plan["outputs"][0])
        second_output["id"] = "alternate"
        self.plan["outputs"].append(second_output)
        args = self.revised_args()
        second = self.prepare(args)
        self.assertEqual(second["preparation_focus"]["status"], "needs_reconciliation")
        selected = plar.read(self.root, asset_id="queue.working")
        self.assertEqual(selected["production"]["task"], first["task"])
        self.assertEqual(selected["asset"]["production"]["output"], first["outputs"][0])
        allocation, digest = plar._load(self.root / "plar.txt")
        next(a for a in allocation["assets"] if a["id"] == "queue.working").pop("production")
        plar.save(self.root, allocation, digest)
        self.assertEqual(plar.read(self.root, asset_id="queue.working")["production"]["task"], second["task"])
        before = self.files()
        with self.assertRaisesRegex(PixlError, "plar_focus"):
            self.prepare()
        self.assertEqual(self.files(), before)

    def test_changed_source_requirements_remain_distinct_from_structural_focus_validity(self):
        first = self.prepare()
        self.settle(first)
        old_focus = self.head.read_bytes()
        brief = self.root / "BRIEF.md"
        brief.write_bytes(brief.read_bytes() + b"\nScoped consumer requirement updated.\n")
        stale = plar.read(self.root, asset_id="queue.working")["production"]
        self.assertEqual(stale["status"], "available")
        self.assertFalse(stale["selection_current"])
        self.assertEqual(stale["selection_bindings"][0]["status"], "changed")
        self.assertEqual(self.head.read_bytes(), old_focus)
        allocation, digest = plar._load(self.root / "plar.txt")
        next(row for row in allocation["sources"] if row["path"] == "BRIEF.md")["sha256"] = graph.file_hash(brief)
        plar.save(self.root, allocation, digest)
        selected = plar.read(self.root, asset_id="queue.working")
        packet = copy.deepcopy(self.packet)
        packet["requirements_hash"] = selected["requirements_hash"]
        packet["sources"] = [{"path": row["path"], "sha256": row["sha256"], "role": "Current scoped consumer requirement"}
                             for row in selected["sources"]]
        write(self.root, "work/source-revision/packet.json", packet)
        second = self.prepare({**self.args, "packet": "work/source-revision/packet.json",
                               "requirements_hash": selected["requirements_hash"], "revise": True,
                               "expect": codec.digest(store.load(self.folder))})
        self.assertNotEqual(second["requirements_hash"], first["requirements_hash"])
        focused = plar.read(self.root, asset_id="queue.working")["production"]
        self.assertEqual(focused["task"], second["task"])
        self.assertTrue(focused["selection_current"])
        document = store.load(self.folder)
        old_binding = plar.selection_bindings(document, first["task"], self.root, self.folder)[0]
        self.assertEqual(old_binding["requirements_hash"], first["requirements_hash"])
        self.assertEqual(old_binding["status"], "changed")
        self.assertFalse(old_binding["selected_for_asset"])

    def test_ordinary_selection_report_with_prefix_none_is_not_a_prepare_marker(self):
        self.prepare()
        document = store.load(self.folder)
        ordinary = write(self.root, "work/plans/" + "0" * 64 + ".json", {"input": {"packet": {}}, "prefix": None})
        original = next(document.records[r.id] for r in document.records["task"].fields["ip"]
                        if document.records[r.id].fields.get("mt", {}).get("binding") == "pixl.plar.selection/1")
        document.records["ordinary.selection"] = Record("ordinary.selection", "X", {
            "nm": "Ordinary explicit selection report", "kd": codec.Symbol("report"),
            "ur": ordinary["path"], "dg": ordinary["sha256"], "mt": copy.deepcopy(original.fields["mt"]),
        })
        fields = copy.deepcopy(document.records["task"].fields)
        fields.update(ip=[codec.Ref("ordinary.selection")], op=[], ca=[], vr=[])
        document.records["ordinary.task"] = Record("ordinary.task", "T", fields)
        binding = plar.selection_bindings(document, "ordinary.task", self.root, self.folder)[0]
        self.assertEqual(binding["status"], "current")
        self.assertTrue(binding["selected_for_asset"])


if __name__ == "__main__":
    unittest.main()
