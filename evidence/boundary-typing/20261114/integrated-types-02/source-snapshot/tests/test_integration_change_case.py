"""Controlled source-change setup and capture bridging, without native model launches."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from evaluations import integration_change_case as case
from evaluations.host_trials import inventory, sha, write_json
from pixl import (
    candidate_review,
    codec,
    delivery,
    destination_observation,
    jobs,
    plar,
    store,
)
from pixl.codec import PixlError
from tests.family_support import family

ADAPTER = case.ROOT / "examples/plar-project/renderer/observation.py"
spec = importlib.util.spec_from_file_location("queue_observation", ADAPTER)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class IntegrationPreparationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="integration fixture test ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.source = self.root / "tracked source closure"
        self.source.mkdir()
        for name in case.source_paths(case.SOURCE):
            target = self.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(case.SOURCE / name, target)
        self.original = inventory(self.source)
        self.destination = self.root / "attempt"
        self.consumer = self.root / "external consumer"

    def fake_host_setup(self, destination, host, setup, python, *, package, consumer):
        """Mock native discovery only: setup still executes real public operations."""
        destination.mkdir()
        consumer.mkdir()
        scripts = consumer / case.KIT / "scripts"
        scripts.mkdir(parents=True)
        (scripts / "pixl.py").write_text("import sys\n" + f"sys.path.insert(0, {str(case.ROOT)!r})\n" +
                                        "from pixl.entrypoint import main\nraise SystemExit(main())\n", encoding="utf-8")
        write_json(destination / "identity.json", {"inputs": {}, "package_files": {}})
        write_json(destination / "launch.json", {"host": host, "cwd": str(consumer)})
        (destination / "runner.py.txt").write_bytes(b"host setup runner\n")
        return consumer

    def prepare(self):
        with patch.object(case.readiness_case, "prepare", side_effect=self.fake_host_setup):
            return case.prepare(self.destination, "codex", Path(sys.executable), consumer=self.consumer, source=self.source)

    def test_tracked_originals_preserved_fresh_prospective_baseline_and_only_timing_changed(self):
        self.prepare()
        identity = json.loads((self.destination / "identity.json").read_bytes())
        self.assertEqual(inventory(self.source), self.original)
        self.assertEqual(identity["original_inputs"], self.original)
        for path, digest in self.original.items():
            self.assertEqual(sha(self.consumer / path), digest, path)
        self.assertTrue(identity["fixture"]["fresh_prospective_store"])
        self.assertFalse(identity["fixture"]["original_producer_state_retained"])
        changes = json.loads((self.destination / "source-change.json").read_bytes())
        self.assertEqual(set(changes["before"]), {case.TIMING, case.AUTHORITY})
        self.assertEqual(set(changes["after"]), {case.TIMING, case.AUTHORITY})
        self.assertNotEqual(changes["before"], changes["after"])
        self.assertEqual((self.destination / "baseline-plar.txt").read_bytes(), (self.consumer / case.PLAR).read_bytes())
        self.assertIn(b"queue-view-integration.ts", (self.consumer / case.RENDERER / "view.mjs").read_bytes())
        self.assertIn(b"capturePlayback", (self.consumer / case.RENDERER / "view.mjs").read_bytes())
        self.assertIn(b'playback["samples"]', (self.consumer / case.RENDERER / "check.py").read_bytes())
        self.assertIn("frameMs = 150", (self.consumer / case.TIMING).read_text())
        self.assertIn("supersedes only", (self.consumer / case.AUTHORITY).read_text())
        self.assertIn("Native 1x live playback remains unperformed", (self.consumer / case.AUTHORITY).read_text())
        self.assertTrue((self.destination / "baseline-pixl/assets/queue.working/state.px").is_file())

    def test_public_prepared_intent_is_real_unsubmitted_and_refuses_changed_source_dispatch(self):
        self.prepare()
        prepared = json.loads((self.destination / "baseline-prepare.json").read_bytes())
        self.assertFalse(prepared["remote_executed"])
        self.assertFalse(prepared["acceptance_created"])
        self.assertEqual(prepared["job"]["state"], "prepared")
        folder = self.consumer / prepared["store"]
        doc = store.load(folder)
        before = inventory(folder)
        with self.assertRaisesRegex(PixlError, "source|selection|requirements"):
            jobs.dispatch(folder, codec.digest(doc), prepared["job"]["id"], self.consumer)
        self.assertEqual(inventory(folder), before)
        self.assertFalse(any(r.kind == "V" for r in doc.records.values()))
        self.assertIn("100 ms", doc.records["contract.working"].fields["li"])
        current = plar.read(self.consumer, path=case.PLAR)
        self.assertEqual(set(current["changes"]["changed_sources"]), {"working-timing", "timing-authority"})
        self.assertEqual(current["changes"]["direct_assets"], ["queue.working"])

    def test_prospective_preserves_original_normative_clauses_except_explicit_timing_authority(self):
        self.prepare()
        original = json.loads((self.source / "plar.txt").read_bytes())
        baseline = json.loads((self.destination / "baseline-plar.txt").read_bytes())
        for old, new in zip(original["assets"], baseline["assets"], strict=True):
            self.assertEqual(old["id"], new["id"])
            for requirement in old["requirements"]:
                if old["id"] == "queue.working" and requirement["property"] in {"animation", "renderer_frame_extraction"}:
                    continue
                self.assertIn(requirement, new["requirements"])
            if new["id"] != "queue.working":
                self.assertNotIn("production", new)
        guidance = (self.consumer / "INTEGRATION-ASSIGNMENT.md").read_text(encoding="utf-8")
        for required in ("production profile", "stages:[]", "obsolete-completion.json", "LOCAL abandonment", "pixl_destination_import", "No job-import"):
            self.assertIn(required, guidance)

    def test_retains_entire_state_and_history_and_never_overwrites_partial_retention(self):
        self.prepare()
        write_json(self.consumer / case.WORK / "CALLER-RESULT.json", {"status": "incomplete", "not_a_pass": True})
        case.retain(self.destination)
        self.assertEqual(inventory(self.destination / "final-pixl"), inventory(self.consumer / ".pixl"))
        self.assertEqual(inventory(self.destination / "retained-inputs"), inventory(self.consumer / case.INPUTS))
        before = inventory(self.destination)
        with self.assertRaisesRegex(ValueError, "Preserve"):
            case.retain(self.destination)
        self.assertEqual(inventory(self.destination), before)


class ObservationBridgeTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="capture bridge test ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        folder = self.root / ".pixl"
        family(self.root, folder)
        delivery.snapshot(folder, codec.digest(store.load(folder)), "delivery.output", "package", self.root)
        self.doc = store.load(folder)
        self.context = candidate_review.context(self.doc, self.root, "package")
        write_json(self.root / "context.json", self.context)
        self.capture = self.root / "capture"
        self.capture.mkdir()
        self.renderer = self.root / "renderer"
        self.renderer.mkdir()
        (self.renderer / "view.mjs").write_bytes(b"// synthetic renderer identity, not executed\n")
        (self.root / "consumer.ts").write_bytes(b"// synthetic consumer identity, not executed\n")
        Image.new("RGBA", (16, 16), (30, 70, 130, 255)).save(self.capture / "view.png")
        image = {"path": "view.png", "sha256": sha(self.capture / "view.png")}
        mapping = {}
        served = {"consumer/consumer.ts": sha(self.root / "consumer.ts"), "renderer/view.mjs": sha(self.renderer / "view.mjs")}
        for i, member in enumerate(self.context["members"]):
            path = f"served-{i}.png"
            shutil.copyfile(self.root / member["retained_path"], self.root / path)
            mapping[member["output"]] = path
            served["consumer/" + path] = member["sha256"]
        write_json(self.root / "destinations.json", mapping)
        first = self.context["members"][0]
        path = mapping[first["output"]]
        self.raw = {"served_files": served, "renderer_files": {"view.mjs": sha(self.renderer / "view.mjs")},
            "views": [{"consumer": consumer, "state": "running", "scale": scale, "image": image,
                       "descriptor": {"path": path}, "asset": {"sha256": first["sha256"]}}
                      for consumer in ("statusCell", "compactStatus") for scale in (1, 3)],
            "playback": {"status": "observed", "reason": "Synthetic test data; no browser executed", "frameCount": 4, "frameMs": 150,
                         "transition": {"state": "running", "consumers": [{"consumer": c} for c in ("statusCell", "compactStatus")]},
                         "samples": [{"elapsed": elapsed, "cells": [{"consumer": c, "frame": frame, "image": image}
                                      for c in ("statusCell", "compactStatus")]} for elapsed, frame in ((0, 0), (150, 1), (600, 0))]},
            "timeline": [{"state": "running", "elapsed": 0, "frame": 0, "image": image}], "display": {"frameMs": 150},
            "viewport": {"width": 1280, "height": 1000}, "devicePixelRatio": 1, "screenshot": image,
            "browser_version": {"product": "SyntheticBrowser/1"}, "observed_at": datetime.now(UTC).isoformat()}
        write_json(self.capture / "render.json", self.raw)
        write_json(self.capture / "launch.json", {"project": str(self.root), "browser": "synthetic-browser", "args": ["--synthetic-test"]})
        write_json(self.capture / "capture-commands.json", [{"method": "SyntheticFixture"}])

    def build(self):
        return adapter.build(self.root, self.capture, self.root / "context.json", self.renderer, self.root / "destinations.json")

    def test_bridge_import_retains_real_refs_and_distinguishes_controlled_from_live_samples(self):
        value = self.build()
        write_json(self.root / "observation.json", value)
        result = destination_observation.import_observation(self.doc, self.root, "package", "observation.json", "imported")
        self.assertFalse(result["renderer_executed"])
        self.assertFalse(result["automatic_acceptance"])
        self.assertEqual(value["renderer"]["command"], ["synthetic-browser", "--synthetic-test"])
        live = [row for row in value["motion"] if row["mode"] == "requestAnimationFrame playback"]
        self.assertEqual({row["consumer"] for row in live}, {"statusCell", "compactStatus"})
        self.assertTrue(all(row["frame_ms"] == 150 for row in live))
        self.assertEqual({row["scale"] for row in value["views"]}, {1, 3})
        self.assertTrue(any(row["path"].endswith("capture-commands.json") for row in value["files"]))

    def test_unavailable_playback_keeps_raw_partial_images_without_claiming_observed_samples(self):
        self.raw["playback"]["status"] = "unavailable"
        write_json(self.capture / "render.json", self.raw)
        value = self.build()
        live = [row for row in value["motion"] if row["mode"] == "requestAnimationFrame playback"]
        self.assertTrue(all(row["status"] == "unavailable" and row["samples"] == [] for row in live))
        write_json(self.root / "observation.json", value)
        destination_observation.import_observation(self.doc, self.root, "package", "observation.json", "imported")

    def test_member_lineage_is_presentation_only_and_bridge_is_read_only(self):
        self.assertTrue(all("lineage" in member for member in self.context["members"]))
        baseline = self.build()
        enriched = copy.deepcopy(self.context)
        for member in enriched["members"]:
            member["lineage"]["limitations"].append("Presentation-only regression annotation")
        write_json(self.root / "context.json", enriched)
        before = inventory(self.root)
        observed = self.build()
        self.assertEqual(inventory(self.root), before)
        self.assertEqual(observed["manifest"], baseline["manifest"])
        self.assertEqual(observed["destinations"], baseline["destinations"])
        self.assertEqual(observed["binding_hash"], baseline["binding_hash"])
        context_ref = next(row for row in observed["files"] if row["path"] == "context.json")
        self.assertEqual(context_ref["sha256"], sha(self.root / "context.json"))

    def test_lineage_does_not_mask_changed_member_identity_or_unknown_fields(self):
        changes = {"output": "different.output", "candidate": "different.candidate",
                   "path": "files/other.png", "sha256": "0" * 64,
                   "unrecognized_identity": "must not be silently discarded"}
        for field, value in changes.items():
            with self.subTest(field=field):
                changed = copy.deepcopy(self.context)
                changed["members"][0][field] = value
                write_json(self.root / "context.json", changed)
                before = inventory(self.root)
                with self.assertRaisesRegex(ValueError, "disagree"):
                    self.build()
                self.assertEqual(inventory(self.root), before)

    def test_wrong_destination_changed_renderer_and_wrong_context_fail_without_output(self):
        mapping = json.loads((self.root / "destinations.json").read_bytes())
        altered = copy.deepcopy(mapping)
        altered[next(iter(altered))] = "consumer.ts"
        write_json(self.root / "destinations.json", altered)
        with self.assertRaisesRegex(ValueError, "not served"):
            self.build()
        write_json(self.root / "destinations.json", mapping)
        original = (self.renderer / "view.mjs").read_bytes()
        (self.renderer / "view.mjs").write_bytes(b"changed renderer")
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            self.build()
        (self.renderer / "view.mjs").write_bytes(original)
        changed = copy.deepcopy(self.context)
        changed["members"][0]["sha256"] = "0" * 64
        write_json(self.root / "context.json", changed)
        with self.assertRaisesRegex(ValueError, "disagree"):
            self.build()

    def test_output_no_clobber_and_outside_root_paths_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            adapter.build(self.root, self.capture, self.root.parent / "context.json", self.renderer, self.root / "destinations.json")
        target = self.root / "observation.json"
        target.write_bytes(b"earlier failed evidence\n")
        argv = [str(ADAPTER), "--project", str(self.root), "--capture", str(self.capture), "--context", str(self.root / "context.json"),
                "--renderer", str(self.renderer), "--destinations", str(self.root / "destinations.json"), "--out", str(target)]
        with patch.object(sys, "argv", argv), self.assertRaisesRegex(ValueError, "fresh"):
            adapter.main()
        self.assertEqual(target.read_bytes(), b"earlier failed evidence\n")


if __name__ == "__main__":
    unittest.main()
