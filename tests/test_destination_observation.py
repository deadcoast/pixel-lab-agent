"""Supplied synthetic observations prove retention mechanics, never art quality."""

import copy
import hashlib
import io
import json
import unittest
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import Image

from pixl import candidate_review, codec, delivery, graph, store
from pixl import destination_observation as destination
from pixl.codec import PixlError, Ref
from tests.family_support import family


def observation_fixture(root):
    """Create a published family and a complete synthetic v1 report for surfaces."""
    root = Path(root)
    folder = root / ".pixl"
    family(root, folder)
    delivery.snapshot(folder, codec.digest(store.load(folder)), "delivery.output", "package", root)
    doc = store.load(folder)
    context = candidate_review.context(doc, root, "package")
    capture = root / "capture"
    capture.mkdir()
    (capture / "renderer.py").write_text("# Synthetic renderer identity only; not executed\n", encoding="utf-8")
    (capture / "consumer.py").write_text("# Synthetic consumer identity only; not executed\n", encoding="utf-8")
    (capture / "render.json").write_text('{"purpose":"synthetic report"}\n', encoding="utf-8")
    Image.new("RGBA", (12, 8), (255, 0, 255, 255)).save(capture / "view.png")

    def file_ref(name):
        return {"path": "capture/" + name, "sha256": hashlib.sha256((capture / name).read_bytes()).hexdigest()}

    destinations = []
    for i, member in enumerate(context["members"]):
        name = f"served-{i}.png"
        (capture / name).write_bytes((root / member["retained_path"]).read_bytes())
        destinations.append({"output": member["output"], "candidate": member["candidate"], **file_ref(name)})
    report = {
        "version": 1, "candidate": "package", "binding_hash": context["binding_hash"],
        "manifest": context["candidate_file"], "observed_at": datetime.now(UTC).isoformat(),
        "renderer": {"name": "Synthetic renderer", "command": ["python", "capture/renderer.py"],
                     "runtime": {"name": "synthetic", "version": "1"}, "files": [file_ref("renderer.py")]},
        "consumer_sources": [file_ref("consumer.py")], "destinations": destinations,
        "viewport": {"width": 12, "height": 8, "device_scale_factor": 1},
        "views": [{"consumer": "test", "state": "test", "scale": 2, "output_id": "view",
                   "member_outputs": [member["output"] for member in context["members"]]}],
        "motion": [{"consumer": "test", "state": "test", "mode": "synthetic",
                    "status": "observed", "frame_count": 2, "frame_ms": 100,
                    "samples": [{"elapsed_ms": 0, "frame": 0, "output_id": "view"},
                                {"elapsed_ms": 100, "frame": 1, "output_id": "view"}],
                    "limitation": "Synthetic samples; no playback executed"}],
        "files": [{"id": "view", **file_ref("view.png"), "role": "image"},
                  {"id": "render", **file_ref("render.json"), "role": "data"}],
        "limitations": ["Synthetic fixture; no rendering, visual review or artistic acceptance"],
    }
    (capture / "observation.json").write_text(json.dumps(report), encoding="utf-8")
    return doc, report


class DestinationObservationTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.doc, self.report = observation_fixture(self.root)
        self.folder = self.root / ".pixl"

    def write_report(self, value=None):
        (self.root / "capture/observation.json").write_text(json.dumps(self.report if value is None else value), encoding="utf-8")

    def run_import(self, out="evidence/imported"):
        return destination.import_observation(self.doc, self.root, "package", "capture/observation.json", out)

    def unchanged(self):
        return {p.relative_to(self.folder).as_posix(): p.read_bytes() for p in self.folder.rglob("*") if p.is_file()}

    def test_complete_deterministic_snapshot_and_state_unchanged(self):
        state = self.unchanged()
        first = self.run_import()
        second = self.run_import("evidence/another")
        self.assertEqual(self.unchanged(), state)
        self.assertEqual(first["bundle"]["sha256"], second["bundle"]["sha256"])
        self.assertFalse(first["renderer_executed"])
        self.assertFalse(first["state_changed"])
        self.assertFalse(first["automatic_acceptance"])
        self.assertEqual(first["binding_hash"], self.report["binding_hash"])
        self.assertEqual(first, json.loads((self.root / "evidence/imported/result.json").read_bytes()))
        self.assertEqual(first["previews"][0]["width"], 12)
        with zipfile.ZipFile(self.root / first["bundle"]["path"]) as archive:
            self.assertEqual(archive.read("report.json"), (self.root / "capture/observation.json").read_bytes())
            self.assertEqual(archive.read("package/manifest.json"), (self.root / self.report["manifest"]["path"]).read_bytes())
            index = json.loads(archive.read("index.json"))
            self.assertEqual(len(index["files"]), 6)
            for row in index["files"]:
                self.assertEqual(archive.read(row["archive_path"]), (self.root / row["original_path"]).read_bytes())
            self.assertTrue(all(info.date_time == (1980, 1, 1, 0, 0, 0) for info in archive.infolist()))

    def test_wrong_package_binding_manifest_and_served_member_rejected_before_export(self):
        variants = []
        for field, value in [("candidate", "member"), ("binding_hash", "0" * 64)]:
            altered = copy.deepcopy(self.report)
            altered[field] = value
            variants.append(altered)
        for field, value in [("path", "capture/render.json"), ("sha256", "0" * 64)]:
            altered = copy.deepcopy(self.report)
            altered["manifest"][field] = value
            variants.append(altered)
        for field, value in [("output", "different.output"), ("candidate", "sample"), ("sha256", "0" * 64)]:
            altered = copy.deepcopy(self.report)
            altered["destinations"][-1][field] = value
            variants.append(altered)
        altered = copy.deepcopy(self.report)
        altered["destinations"].pop()
        variants.append(altered)
        for i, value in enumerate(variants):
            with self.subTest(case=i):
                self.write_report(value)
                with self.assertRaises(PixlError):
                    self.run_import()
                self.assertFalse((self.root / "evidence/imported").exists())

    def test_changed_declared_source_destination_and_output_rejected(self):
        for name in ("renderer.py", "consumer.py", "served-0.png", "view.png", "render.json"):
            with self.subTest(file=name):
                path = self.root / "capture" / name
                previous = path.read_bytes()
                path.write_bytes(b"changed")
                with self.assertRaises(PixlError):
                    self.run_import()
                path.write_bytes(previous)
                self.assertFalse((self.root / "evidence/imported").exists())

    def test_historical_family_rejected_even_with_fresh_review_binding(self):
        self.doc.records["delivery.output"].fields["mb"] = [Ref("output")]
        self.doc.revision += 1
        store.commit(self.folder, self.doc, codec.digest(store.load(self.folder)), self.root)
        self.doc = store.load(self.folder)
        current = candidate_review.context(self.doc, self.root, "package")
        self.assertNotEqual(current["binding_hash"], self.report["binding_hash"])
        self.report["binding_hash"] = current["binding_hash"]
        self.write_report()
        with self.assertRaisesRegex(PixlError, "family candidate is not current"):
            self.run_import()
        self.assertFalse((self.root / "evidence/imported").exists())

    def test_duplicate_or_missing_references_rejected(self):
        variants = []
        for key in ("files", "destinations", "consumer_sources"):
            altered = copy.deepcopy(self.report)
            altered[key].append(altered[key][0].copy())
            variants.append(altered)
        altered = copy.deepcopy(self.report)
        altered["files"][1]["path"] = altered["files"][0]["path"]
        variants.append(altered)
        for reference in ("missing", "render"):
            altered = copy.deepcopy(self.report)
            altered["views"][0]["output_id"] = reference
            variants.append(altered)
        altered = copy.deepcopy(self.report)
        altered["motion"][0]["samples"][0]["output_id"] = "missing"
        variants.append(altered)
        altered = copy.deepcopy(self.report)
        altered["views"][0]["member_outputs"] = ["unrelated"]
        variants.append(altered)
        for i, value in enumerate(variants):
            with self.subTest(case=i):
                self.write_report(value)
                with self.assertRaises(PixlError):
                    self.run_import()

    def test_unknown_and_unavailable_motion_preserved_without_inference(self):
        self.report["motion"][0].update(frame_count=None, frame_ms=None)
        for sample in self.report["motion"][0]["samples"]:
            sample["frame"] = None
        self.report["motion"].append({"consumer": "another", "state": "unknown", "mode": "unavailable",
            "status": "unavailable", "frame_count": None, "frame_ms": None, "samples": [],
            "limitation": "No timing available"})
        self.report["views"][0].update(consumer="custom", state="custom", scale=1.25, member_outputs=[])
        self.write_report()
        result = self.run_import()
        self.assertEqual(result["supplied_observations"]["motion"], self.report["motion"])
        self.assertEqual(result["supplied_observations"]["views"], self.report["views"])

    def test_invalid_motion_timing_rejected(self):
        for field, value in [("status", "unknown"), ("status", "unavailable"), ("samples", []),
                             ("frame_count", 1), ("frame_count", 1.0), ("frame_ms", 0), ("frame_ms", True)]:
            with self.subTest(field=field, value=value):
                altered = copy.deepcopy(self.report)
                altered["motion"][0][field] = value
                self.write_report(altered)
                with self.assertRaises(PixlError):
                    self.run_import()
        for field, value in [("elapsed_ms", 0), ("elapsed_ms", -1), ("frame", -1)]:
            with self.subTest(sample=field, value=value):
                altered = copy.deepcopy(self.report)
                altered["motion"][0]["samples"][1][field] = value
                self.write_report(altered)
                with self.assertRaises(PixlError):
                    self.run_import()

    def test_closed_schema_timestamp_and_strict_json_rejected(self):
        for field, value in [("version", 1.0), ("version", True), ("unknown", "value"),
                             ("observed_at", "2030-01-01T00:00:00Z"), ("observed_at", "2026-01-01"),
                             ("observed_at", "not a timestamp")]:
            with self.subTest(field=field, value=value):
                altered = copy.deepcopy(self.report)
                altered[field] = value
                self.write_report(altered)
                with self.assertRaises(PixlError):
                    self.run_import()
        for raw in [b'{"version":1,"version":1}', b'{"scale":NaN}', b'{"scale":Infinity}', b"[]"]:
            with self.subTest(raw=raw):
                (self.root / "capture/observation.json").write_bytes(raw)
                with self.assertRaises(PixlError):
                    self.run_import()

    def test_existing_export_is_preserved(self):
        first = self.run_import()
        previous = (self.root / first["bundle"]["path"]).read_bytes()
        with self.assertRaises(PixlError):
            self.run_import()
        self.assertEqual(previous, (self.root / first["bundle"]["path"]).read_bytes())

    def test_input_change_during_archive_creation_rejected_before_export(self):
        original = destination._archive

        def changed(entries):
            data = original(entries)
            (self.root / "capture/consumer.py").write_bytes(b"changed during import")
            return data

        with patch.object(destination, "_archive", side_effect=changed), self.assertRaises(PixlError):
            self.run_import()
        self.assertFalse((self.root / "evidence/imported").exists())

    def test_changed_state_dependency_during_archive_creation_rejected(self):
        original = destination._archive

        def changed(entries):
            data = original(entries)
            member = self.doc.records["member"]
            (self.root / member.fields["ur"]).write_bytes(b"changed bound artifact")
            return data

        with patch.object(destination, "_archive", side_effect=changed), self.assertRaises(PixlError):
            self.run_import()
        self.assertFalse((self.root / "evidence/imported").exists())

    def test_partial_export_is_retained_without_success_marker_and_refuses_retry(self):
        original = Path.open

        def fail_preview(path, *args, **kwargs):
            if "previews" in path.parts and args and args[0] == "xb":
                raise OSError("synthetic interrupted write")
            return original(path, *args, **kwargs)

        before = self.unchanged()
        with patch.object(Path, "open", fail_preview), self.assertRaisesRegex(PixlError, "retained partial files"):
            self.run_import()
        exported = self.root / "evidence/imported"
        self.assertEqual(len(list(exported.glob("*.zip"))), 1)
        self.assertFalse((exported / "result.json").exists())
        self.assertEqual(self.unchanged(), before)
        with self.assertRaisesRegex(PixlError, "fresh output directory"):
            self.run_import()

    def test_input_change_after_writing_export_keeps_failed_evidence(self):
        original = destination._Capture.verify
        calls = 0

        def changed(capture):
            nonlocal calls
            calls += 1
            if calls == 2:
                (self.root / "capture/renderer.py").write_bytes(b"changed during export")
            return original(capture)

        with patch.object(destination._Capture, "verify", changed), self.assertRaises(PixlError):
            self.run_import()
        exported = self.root / "evidence/imported"
        self.assertEqual(len(list(exported.glob("*.zip"))), 1)
        self.assertFalse((exported / "result.json").exists())

    def test_limits_reject_without_export(self):
        for setting, limit in [("MAX_FILE_BYTES", 1), ("MAX_TOTAL_BYTES", 1), ("MAX_ARCHIVE_BYTES", 1)]:
            with self.subTest(setting=setting):
                with patch.object(destination, setting, limit), self.assertRaises(PixlError):
                    self.run_import()
                self.assertFalse((self.root / "evidence/imported").exists())

    def test_invalid_png_and_paths_rejected(self):
        for path in ("../capture/view.png", "/capture/view.png", "capture/../capture/view.png", "capture\\view.png"):
            with self.subTest(path=path):
                altered = copy.deepcopy(self.report)
                altered["files"][0]["path"] = path
                self.write_report(altered)
                with self.assertRaises(PixlError):
                    self.run_import()
        (self.root / "capture/view.png").write_bytes(b"not PNG")
        self.report["files"][0]["sha256"] = hashlib.sha256(b"not PNG").hexdigest()
        self.write_report()
        with self.assertRaises(PixlError):
            self.run_import()

    def test_png_with_invalid_crc_has_structured_error(self):
        path = self.root / "capture/view.png"
        data = bytearray(path.read_bytes())
        chunk = data.index(b"IDAT")
        length = int.from_bytes(data[chunk - 4:chunk], "big")
        data[chunk + 4 + length] ^= 1
        path.write_bytes(data)
        self.report["files"][0]["sha256"] = hashlib.sha256(data).hexdigest()
        self.write_report()
        with self.assertRaisesRegex(PixlError, "invalid PNG output"):
            self.run_import()
        self.assertFalse((self.root / "evidence/imported").exists())

    def test_retained_bundle_survives_original_removal_and_review_copy(self):
        imported = self.run_import()
        original_archive = (self.root / imported["bundle"]["path"]).read_bytes()
        for path in (self.root / "capture").iterdir():
            path.unlink()
        ctx = candidate_review.context(self.doc, self.root, "package")
        observation = imported["observation"]
        request = {"version": 1, "binding_hash": ctx["binding_hash"], "reviewer": "actor",
            "observed_at": datetime.now(UTC).isoformat(), "observations": [observation],
            "verdicts": [{"criterion": "q.delivery.engine", "status": "fail",
                "reason": "Synthetic retained report is not actual engine acceptance", "supersedes": None, "observations": [0]}],
            "action": "record", "next_action": "Actual independent review remains required", "limitations": ["Synthetic test"]}
        reviewed = candidate_review.submit(self.folder, codec.digest(self.doc), "package", "import.review", request, self.root)
        self.assertFalse(reviewed["current_acceptance"]["all_required_pass"])
        after = store.load(self.folder)
        retained = self.root / after.records["import.review.file.0"].fields["ur"]
        for path in (self.root / "evidence/imported").rglob("*"):
            if path.is_file():
                path.unlink()
        graph.validate(after, self.root)
        self.assertEqual(retained.read_bytes(), original_archive)
        with zipfile.ZipFile(io.BytesIO(retained.read_bytes())) as archive:
            index = json.loads(archive.read("index.json"))
            self.assertEqual(len(index["files"]), 6)
            self.assertTrue(archive.read("outputs/0000.png").startswith(b"\x89PNG"))


if __name__ == "__main__":
    unittest.main()
