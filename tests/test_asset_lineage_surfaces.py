"""Derived lineage follows exact delivered candidates without rewriting evidence."""

import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from unittest.mock import Mock, patch

import pixl
from pixl import candidate_review, codec, delivery, handoff, plar, service, store
from pixl.codec import Ref, Symbol
from tests import test_plar_family_delivery as plar_fixture
from tests.family_support import family


class AssetLineageSurfaceTests(unittest.TestCase):
    def setUp(self):
        # Exercise the surface contract independently of provenance derivation.
        self.detail_size = 0
        module = ModuleType("pixl.asset_lineage")
        self.describe = Mock(side_effect=self.lineage)
        module.describe = self.describe
        self.enterContext(patch.object(pixl, "asset_lineage", module, create=True))
        self.enterContext(patch.dict("sys.modules", {"pixl.asset_lineage": module}))
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.folder = self.root / ".pixl"
        family(self.root, self.folder)

    def lineage(self, document, root, candidate_id):
        self.assertIn(candidate_id, document.records)
        return {"candidate": candidate_id, "status": "unknown", "relationships": [],
                "scope": "Unrecorded derivation." + "x" * self.detail_size}

    def inventory(self, root=None):
        root = root or self.root
        return {path.relative_to(root).as_posix(): path.read_bytes()
                for path in root.rglob("*") if path.is_file()}

    def snapshot(self):
        delivery.snapshot(self.folder, codec.digest(store.load(self.folder)),
                          "delivery.output", "package", self.root)
        return store.load(self.folder)

    def selected_successor(self, document):
        successor = copy.deepcopy(document.records["member"])
        successor.id = "member.next"
        document.records[successor.id] = successor
        document.records["member.task"].fields.update(
            st=Symbol("open"), ca=[Ref(successor.id)])
        document.revision += 1
        return document

    def plar_fixture(self):
        fixture = plar_fixture.PLARFamilyDeliveryTests(
            "test_current_destination_cannot_bypass_unfinished_collective_review")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        return fixture

    def test_family_current_and_snapshot_members_share_one_read_only_projection(self):
        document = self.snapshot()
        before = self.inventory()
        digest = codec.digest(document)
        self.describe.reset_mock()
        result = delivery.report(document, self.root)
        row = result["families"][0]
        self.assertEqual(result["hash"], digest)
        self.assertEqual(codec.digest(document), digest)
        self.assertEqual(self.inventory(), before)
        self.assertEqual({call.args[2] for call in self.describe.call_args_list},
                         {"sample", "member"})
        self.assertEqual(self.describe.call_count, 2)
        for member in row["members"]:
            saved = next(item for item in row["snapshots"][0]["files"]
                         if item["candidate"] == member["candidate"])
            self.assertEqual(member["lineage"], saved["lineage"])
            self.assertEqual(member["lineage"]["status"], "unknown")
        self.assertEqual(row["state"], "open")
        self.assertFalse(row["snapshots"][0]["retention_is_acceptance"])
        manifest = json.loads((self.root / row["snapshots"][0]["manifest"]).read_bytes())
        self.assertTrue(all("lineage" not in item for item in manifest["files"]))
        # Cache lifetime ends with this report, even for an unchanged document.
        delivery.report(document, self.root)
        self.assertEqual(self.describe.call_count, 4)

    def test_historical_members_keep_their_candidates_after_current_selection_changes(self):
        document = self.selected_successor(self.snapshot())
        before = self.inventory()
        digest = codec.digest(document)
        row = delivery.report(document, self.root)["families"][0]
        current = next(item for item in row["members"] if item["output"] == "member.output")
        retained = next(item for item in row["snapshots"][0]["files"]
                        if item["output"] == "member.output")
        self.assertEqual(current["candidate"], "member.next")
        self.assertEqual(current["lineage"]["candidate"], "member.next")
        self.assertEqual(retained["candidate"], "member")
        self.assertEqual(retained["lineage"]["candidate"], "member")
        self.assertTrue(row["snapshots"][0]["stale"])
        self.assertEqual(codec.digest(document), digest)
        self.assertEqual(self.inventory(), before)

    def test_unselected_current_member_does_not_borrow_snapshot_lineage(self):
        document = self.snapshot()
        document.records["member.task"].fields.update(st=Symbol("open"), ca=[])
        row = delivery.report(document, self.root)["families"][0]
        member = next(item for item in row["members"] if item["output"] == "member.output")
        self.assertIsNone(member["candidate"])
        self.assertIsNone(member["lineage"])
        retained = next(item for item in row["snapshots"][0]["files"]
                        if item["output"] == "member.output")
        self.assertEqual(retained["lineage"]["candidate"], "member")

    def test_review_context_exposes_exact_candidate_and_historical_member_lineage(self):
        document = self.selected_successor(self.snapshot())
        before = self.inventory()
        result = candidate_review.context(document, self.root, "package")
        self.assertEqual(result["lineage"]["candidate"], "package")
        self.assertFalse(result["nominated"])
        self.assertFalse(result["snapshot_acceptance"]["accepted"])
        self.assertFalse(result["current_acceptance"]["all_required_pass"])
        member = next(item for item in result["members"] if item["output"] == "member.output")
        self.assertEqual(member["lineage"]["candidate"], "member")
        self.assertTrue((self.root / member["retained_path"]).is_file())
        selected = candidate_review.context(document, self.root, "member.next")
        self.assertEqual(selected["lineage"]["candidate"], "member.next")
        self.assertTrue(selected["nominated"])
        self.assertEqual(self.inventory(), before)

    def test_plar_delivery_carries_candidate_and_selected_snapshot_members(self):
        fixture = self.plar_fixture()
        unfinished = fixture.selected()
        self.assertEqual(unfinished["delivery"]["lineage"]["candidate"], "member")
        self.assertEqual(unfinished["delivery"]["families"][0]["members"], [])
        self.assertFalse(unfinished["delivery"]["complete"])
        fixture.finish_family()
        before = self.inventory(fixture.root)
        selected = fixture.selected()
        result = selected["delivery"]
        self.assertEqual(result, selected["continuation"]["delivery"])
        self.assertTrue(result["complete"])
        self.assertEqual({member["lineage"]["candidate"]
                          for member in result["families"][0]["members"]},
                         {"sample", "member"})
        self.assertEqual(self.inventory(fixture.root), before)
        fixture.destination.write_bytes(b"Changed after acceptance")
        changed = fixture.selected()
        self.assertEqual(changed["delivery"]["lineage"], result["lineage"])
        self.assertFalse(changed["delivery"]["complete"])
        self.assertEqual(changed["next_action"], "review_delivery")

    def test_large_lineage_uses_exact_existing_caller_locators_and_stable_handoff(self):
        fixture = self.plar_fixture()
        fixture.finish_family()
        self.detail_size = 6000
        selected = plar.read(fixture.root, asset_id="queue.working")
        before = self.inventory(fixture.root)
        args = (fixture.root, "queue.working", selected["requirements_hash"],
                selected["production"]["hash"], {"status": "partial"})
        result = handoff.save(*args, view="caller")
        self.assertFalse(result["production"]["delivery_inline"])
        self.assertFalse(result["resume_inline"])
        self.assertNotIn("delivery", result["production"])
        self.assertTrue(result["production"]["delivery_complete"])
        self.assertEqual(result["assignment"]["status"], "partial")
        reference = result["production"]["delivery_ref"]
        self.assertEqual(reference["json_pointer"], "/resume/delivery")
        section = service.source_slice(fixture.root / reference["path"], reference["sha256"],
                                       reference["start"], reference["end"], reference["bytes"])
        resume = json.loads("{" + section["text"].rstrip().removesuffix(",") + "}")["resume"]
        saved = json.loads((fixture.root / result["path"]).read_bytes())
        self.assertEqual(resume["delivery"], saved["resume"]["delivery"])
        self.assertEqual(resume["delivery"], selected["production"]["delivery"])
        self.assertEqual(set(self.inventory(fixture.root)) - set(before), {result["path"]})
        self.assertTrue(all((fixture.root / path).read_bytes() == data for path, data in before.items()))
        repeated = handoff.save(*args, view="caller")
        self.assertEqual(result, repeated)


if __name__ == "__main__":
    unittest.main()
