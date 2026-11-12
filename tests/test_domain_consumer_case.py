"""Controlled domain preparation must not turn geometry into artistic acceptance."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageChops

from evaluations import domain_consumer_case as case
from evaluations.host_trials import inventory, sha, write_json
from pixl import candidate_review, store


def declaration(domain):
    text = (case.PROJECT / f"src/{domain}.ts").read_text(encoding="utf-8")
    return json.loads(text.removeprefix(f"export const {domain} = ").split(";\n", 1)[0])


class DomainConsumerSourceTests(unittest.TestCase):
    def test_terrain_grids_cover_every_explicit_corner_pattern(self):
        terrain = declaration("terrain")
        self.assertEqual(terrain["corner_order"], ["nw", "ne", "se", "sw"])
        self.assertEqual(set(terrain["tiles"]), {str(i) for i in range(16)})
        self.assertEqual({tile["path"] for tile in terrain["tiles"].values()}, set(case.config("terrain")["destinations"].values()))
        patterns = set()
        for neighborhood in terrain["neighborhoods"]:
            vertices = neighborhood["vertices"]
            self.assertTrue(2 <= len(vertices) <= 17)
            self.assertTrue(2 <= len(vertices[0]) <= 17)
            self.assertTrue(all(len(row) == len(vertices[0]) and set(row) <= {0, 1} for row in vertices))
            for row in range(len(vertices) - 1):
                for col in range(len(vertices[0]) - 1):
                    corners = [vertices[row][col], vertices[row][col + 1], vertices[row + 1][col + 1], vertices[row + 1][col]]
                    patterns.add(sum(bit * 2 ** index for index, bit in enumerate(corners)))
        self.assertEqual(patterns, set(range(16)))
        self.assertEqual(len(terrain["neighborhoods"]), 2)
        for tile in terrain["tiles"].values():
            with Image.open(case.PROJECT / tile["path"]) as image:
                self.assertEqual(image.size, tuple(terrain["tile_size"]))
                self.assertEqual(image.convert("RGBA").getchannel("A").getextrema(), (255, 255))

    def test_animation_preserves_uneven_timing_loop_and_one_shot(self):
        animation = declaration("animation")
        self.assertEqual({clip["loop"] for clip in animation["clips"]}, {True, False})
        self.assertEqual({frame["path"] for clip in animation["clips"] for frame in clip["frames"]}, set(case.config("animation")["destinations"].values()))
        for clip in animation["clips"]:
            self.assertEqual([f["duration_ms"] for f in clip["frames"]], [120, 180, 120, 240])
            self.assertEqual(clip["anchor"], [20, 28])
            self.assertTrue(all(f["pivot"] == [8, 14] and f["rect"] == [0, 0, 16, 16] for f in clip["frames"]))
            # The source art has equal opaque floor contact before the controlled
            # pixel-only fault; fixed pivots alone would not prove this.
            bottoms = []
            for frame in clip["frames"]:
                with Image.open(case.PROJECT / frame["path"]) as image:
                    bottoms.append(image.convert("RGBA").getchannel("A").getbbox()[3])
            self.assertEqual(len(set(bottoms)), 1)


class DomainConsumerPreparationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)

    def test_only_measured_member_geometry_is_accepted(self):
        root = self.base / "consumer"
        result = case.project(root)
        self.assertFalse(result["generated_art"])
        self.assertFalse(result["family_artistic_acceptance"])
        self.assertFalse(result["human_acceptance"])
        for domain, member_count in (("terrain", 16), ("animation", 4)):
            doc = store.load(root / Path(case.state(domain)).parent)
            family = candidate_review.context(doc, root, "delivery.candidate")
            self.assertFalse(family["current_acceptance"]["all_required_pass"])
            self.assertFalse(family["current_acceptance"]["task_complete"])
            self.assertFalse(family["snapshot_acceptance"]["accepted"])
            self.assertEqual({q["id"]: q["status"] for q in family["criteria"]}, {"q.continuity": "unperformed", "q.destination": "unperformed"})
            verdicts = [record for record in doc.records.values() if record.kind == "V"]
            self.assertEqual(len(verdicts), member_count)
            self.assertTrue(all(v.fields["rq"].id == "q.geometry" and v.fields["st"].value == "pass" for v in verdicts))
            for i in range(member_count):
                member = candidate_review.context(doc, root, f"member.{i}")
                self.assertTrue(member["current_acceptance"]["all_required_pass"])
                self.assertEqual([(q["domain"], q["mode"]) for q in member["criteria"]], [("mechanical", "local")])
                receipt = json.loads((root / case.INPUTS / f"{domain}-member-{i}-geometry.json").read_text(encoding="utf-8"))
                self.assertEqual(receipt["sha256"], sha(root / receipt["path"]))
                self.assertIn("human unreviewed", receipt["scope"])

    def test_controlled_faults_change_exactly_two_assets_and_preserve_source(self):
        source_inventory = inventory(case.PROJECT)
        root = self.base / "consumer"
        prepared = case.project(root, defects=True)
        changed = {name for name, digest in source_inventory.items() if sha(root / name) != digest}
        wanted = {"assets/terrain/tile-6.png", "assets/motion/frame-2.png"}
        self.assertEqual(changed, wanted)
        self.assertEqual(set(prepared["pixel_changes"]), wanted)
        self.assertEqual(inventory(case.PROJECT), source_inventory)
        for name, change in prepared["pixel_changes"].items():
            self.assertEqual(change, {"original_sha256": source_inventory[name], "controlled_sha256": sha(root / name)})
        with Image.open(case.PROJECT / "assets/terrain/tile-6.png") as original, Image.open(root / "assets/terrain/tile-6.png") as altered:
            self.assertEqual(ImageChops.difference(original.convert("RGB"), altered.convert("RGB")).getbbox(), (0, 0, 8, 8))
        with Image.open(case.PROJECT / "assets/motion/frame-2.png") as original, Image.open(root / "assets/motion/frame-2.png") as altered:
            self.assertEqual(altered.convert("RGBA").getchannel("A").getbbox()[3], original.convert("RGBA").getchannel("A").getbbox()[3] + 2)
        for domain in case.PROFILES:
            context = json.loads((root / case.INPUTS / f"{domain}-context.json").read_text(encoding="utf-8"))
            self.assertFalse(context["current_acceptance"]["all_required_pass"])
            for member in context["members"]:
                path = case.config(domain)["destinations"][member["output"]]
                self.assertEqual(member["sha256"], sha(root / path))

    def test_preexisting_project_collision_preserves_every_byte(self):
        for collision in ("assets", "src", ".pixl", case.INPUTS):
            with self.subTest(collision=collision):
                root = self.base / collision.replace("/", "-").replace(".", "-")
                folder = root / collision
                folder.mkdir(parents=True)
                (folder / "existing.txt").write_text("Keep existing work.\n", encoding="utf-8")
                (root / "BRIEF.md").write_text("Keep this prior brief on collision.\n", encoding="utf-8")
                before = inventory(root)
                with self.assertRaises(ValueError):
                    case.project(root, defects=True)
                self.assertEqual(inventory(root), before)

    def test_repeated_preparation_cannot_overwrite_changed_pixels(self):
        root = self.base / "consumer"
        case.project(root)
        path = root / "assets/terrain/tile-6.png"
        path.write_bytes(path.read_bytes() + b"preserved private marker")
        before = inventory(root)
        with self.assertRaises(ValueError):
            case.project(root, defects=True)
        self.assertEqual(inventory(root), before)

    def test_prepare_preserves_existing_attempt_and_consumer(self):
        attempt = self.base / "existing-attempt"
        attempt.mkdir()
        (attempt / "receipt.txt").write_text("Prior evidence", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "fresh attempt"):
            case.prepare(attempt, "codex", Path(sys.executable))
        self.assertEqual((attempt / "receipt.txt").read_text(encoding="utf-8"), "Prior evidence")
        consumer = self.base / "existing-consumer"
        consumer.mkdir()
        (consumer / "work.txt").write_text("Prior consumer", encoding="utf-8")
        with patch.object(case.readiness_case, "verify_manifest", return_value={"status": "verified"}), self.assertRaisesRegex(ValueError, "fresh consumer"):
            case.prepare(self.base / "new-attempt", "codex", Path(sys.executable), consumer=consumer)
        self.assertFalse((self.base / "new-attempt").exists())
        self.assertEqual((consumer / "work.txt").read_text(encoding="utf-8"), "Prior consumer")

    def test_prepare_keeps_keyword_handoff_and_bound_inputs(self):
        attempt, consumer, package = self.base / "attempt", self.base / "consumer", self.base / "package"
        received = {}

        def prepared(destination, host, setup, python, *, package=None, consumer=None):
            received.update(host=host, setup=setup, python=python, package=package, consumer=consumer)
            destination.mkdir()
            consumer.mkdir()
            write_json(destination / "launch.json", {"cwd": str(consumer), "host": host})
            write_json(destination / "identity.json", {})
            (destination / "runner.py.txt").write_text("original setup runner", encoding="utf-8")
            return consumer

        with patch.object(case.readiness_case, "prepare", side_effect=prepared):
            root = case.prepare(attempt, "codex", Path(sys.executable), package=package, consumer=consumer)
        self.assertEqual(root, consumer)
        self.assertEqual(received["package"], package)
        self.assertEqual(received["consumer"], consumer)
        self.assertEqual(received["setup"], "clean")
        identity = json.loads((attempt / "identity.json").read_text(encoding="utf-8"))
        self.assertEqual(identity["inputs"], inventory(root, ("__pycache__",)))
        self.assertEqual(identity["baseline_production"], inventory(root / ".pixl"))
        self.assertEqual((attempt / "setup-runner.py.txt").read_text(encoding="utf-8"), "original setup runner")
        self.assertEqual(sha(attempt / "runner.py.txt"), sha(Path(case.__file__)))
        self.assertTrue(all(ref["sha256"] == sha(Path(ref["path"])) for ref in identity["configs"].values()))

    def test_retention_records_removal_and_archives_surviving_changes(self):
        root, attempt = self.base / "consumer", self.base / "attempt"
        root.mkdir()
        attempt.mkdir()
        (root / ".pixl").mkdir()
        (root / ".pixl/state.px").write_text("saved state", encoding="utf-8")
        (root / "removed.txt").write_text("original", encoding="utf-8")
        (root / "changed.txt").write_text("original", encoding="utf-8")
        write_json(attempt / "launch.json", {"cwd": str(root)})
        write_json(attempt / "identity.json", {"inputs": inventory(root), "baseline_production": inventory(root / ".pixl")})
        (root / "removed.txt").unlink()
        (root / "changed.txt").write_text("changed", encoding="utf-8")
        (root / case.WORK).mkdir(parents=True)
        (root / case.WORK / "result.json").write_text("{}", encoding="utf-8")
        case.retain(attempt)
        preservation = json.loads((attempt / "preservation.json").read_text(encoding="utf-8"))
        self.assertEqual(preservation["removed"], ["removed.txt"])
        self.assertEqual(set(preservation["changed"]), {"changed.txt", "removed.txt"})
        self.assertTrue(preservation["production_unchanged"])
        with zipfile.ZipFile(attempt / "unexpected-delta.zip") as archive:
            self.assertEqual(archive.namelist(), ["changed.txt"])
        self.assertTrue((attempt / "outputs/result.json").is_file())
        before = inventory(attempt)
        with self.assertRaisesRegex(ValueError, "prior evidence"):
            case.retain(attempt)
        self.assertEqual(inventory(attempt), before)


if __name__ == "__main__":
    unittest.main()
