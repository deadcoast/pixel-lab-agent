import copy
import hashlib
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl import codec, graph, retention, service, store
from pixl.codec import PixlError, Record, Ref, Symbol

ROOT = Path(__file__).resolve().parents[1]


class LibraryRetentionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.folder = self.root / ".pixl"
        self.kit = self.root / "kit"
        self.source = self.kit / "resources/method.txt"
        self.source.parent.mkdir(parents=True)
        self.original = (
            b"Original source revision.\nIts limited proof remains original.\n"
        )
        self.source.write_bytes(self.original)
        self.sha = hashlib.sha256(self.original).hexdigest()
        self.write_manifest(self.kit, self.sha)
        (self.root / "brief.txt").write_bytes(b"Current consumer requirements.\n")
        doc = store.intake_project(
            "Retained library", "Preserve exact source evidence."
        )
        doc.records["source"] = Record(
            "source",
            "S",
            {
                "ur": "kit/resources/method.txt",
                "dg": self.sha,
                "ln": [1, 2],
                "at": "2026-11-07",
                "au": Symbol("study"),
            },
        )
        doc.records["brief"] = Record(
            "brief",
            "S",
            {
                "ur": "brief.txt",
                "dg": graph.file_hash(self.root / "brief.txt"),
                "ln": [1, 1],
                "at": "2026-11-07",
                "au": Symbol("local"),
            },
        )
        receipt = self.root / "proof.json"
        receipt.write_bytes(
            b'{"scope":"Original source, not an updated implementation."}\n'
        )
        doc.records["proof"] = Record(
            "proof",
            "E",
            {
                "nm": "Original proof",
                "ur": "proof.json",
                "dg": graph.file_hash(receipt),
                "rs": Symbol("pass"),
                "md": Symbol("local"),
                "at": "2026-11-07",
                "bs": [
                    {
                        "rf": Ref("source"),
                        "dg": codec.record_hash(doc.records["source"]),
                    }
                ],
            },
        )
        self.initial = store.initialize(self.folder, doc, self.root)
        self.doc = store.load(self.folder)
        self.state = (self.folder / "state.px").read_bytes()

    def write_manifest(self, kit, digest):
        (kit / "bundle-manifest.json").write_text(
            json.dumps({"files": [{"path": "resources/method.txt", "sha256": digest}]}),
            "utf-8",
        )

    def retain(self, **kwargs):
        return retention.retain(
            self.folder, self.initial["hash"], "kit", self.root, **kwargs
        )

    def replace_source(self):
        data = b"Updated implementation with a different proof.\n"
        self.source.write_bytes(data)
        self.write_manifest(self.kit, hashlib.sha256(data).hexdigest())
        return data

    def test_original_failure_remains_without_explicit_retention(self):
        self.replace_source()
        with self.assertRaises(PixlError) as failure:
            service.workflow(self.folder / "state.px", self.root)
        self.assertEqual(failure.exception.code, "file_hash")

    def test_update_resumes_same_state_and_receipt_against_original_source(self):
        result = self.retain()
        self.assertEqual(result["sources"], ["source"])
        self.assertFalse(result["state_changed"])
        self.replace_source()
        report = service.workflow(self.folder / "state.px", self.root)
        self.assertTrue(report["files_verified"])
        retained = report["retained_sources"][0]
        self.assertEqual(retained["status"], "retained_revision")
        self.assertEqual(retained["expected_sha256"], self.sha)
        self.assertNotEqual(retained["current_sha256"], self.sha)
        self.assertEqual(Path(retained["retained_path"]).read_bytes(), self.original)
        self.assertEqual((self.folder / "state.px").read_bytes(), self.state)
        self.assertEqual(
            store.load(self.folder).records["proof"], self.doc.records["proof"]
        )

    def test_source_removal_still_resolves_its_explicit_snapshot(self):
        self.retain()
        self.source.unlink()
        report = service.inspect_document(self.folder / "state.px", self.root)
        self.assertEqual(report["retained_sources"][0]["location_status"], "missing")
        self.assertTrue(report["valid"])

    def test_recover_after_replacement_from_the_original_kit(self):
        shutil.copytree(self.kit, self.root / "original-kit")
        self.replace_source()
        self.retain(from_library="original-kit")
        self.assertTrue(
            service.inspect_document(self.folder / "state.px", self.root)["valid"]
        )
        self.assertEqual((self.folder / "state.px").read_bytes(), self.state)

    def test_changed_kit_cannot_invent_original_bytes(self):
        self.replace_source()
        with self.assertRaises(PixlError) as failure:
            self.retain()
        self.assertEqual(failure.exception.code, "library_source_hash")
        self.assertFalse((self.root / retention.CACHE).exists())
        self.assertEqual((self.folder / "state.px").read_bytes(), self.state)

    def test_corrupted_retained_source_is_rejected(self):
        self.retain()
        self.replace_source()
        blob = self.root / retention.CACHE / "objects" / self.sha
        blob.write_bytes(b"Corrupted retained bytes.")
        with self.assertRaises(PixlError) as failure:
            graph.validate(self.doc, self.root)
        self.assertEqual(failure.exception.code, "library_snapshot_corrupt")

    def test_corrupted_manifest_is_rejected(self):
        self.retain()
        self.replace_source()
        entry = json.loads(
            next((self.root / retention.CACHE / "refs").iterdir()).read_text("utf-8")
        )
        (
            self.root / retention.CACHE / "objects" / entry["manifest_sha256"]
        ).write_bytes(b"{}")
        with self.assertRaises(PixlError) as failure:
            graph.validate(self.doc, self.root)
        self.assertEqual(failure.exception.code, "library_snapshot_corrupt")

    def test_stale_write_and_path_escape_preserve_project(self):
        with self.assertRaises(PixlError) as failure:
            retention.retain(self.folder, "0" * 64, "kit", self.root)
        self.assertEqual(failure.exception.code, "stale_write")
        with self.assertRaises(PixlError) as failure:
            retention.retain(self.folder, self.initial["hash"], "../kit", self.root)
        self.assertEqual(failure.exception.code, "path_escape")
        self.assertFalse((self.root / retention.CACHE).exists())

    def test_retention_does_not_hide_live_brief_or_receipt_drift(self):
        self.retain()
        self.replace_source()
        for path in ("brief.txt", "proof.json"):
            with self.subTest(path=path):
                target = self.root / path
                original = target.read_bytes()
                target.write_bytes(b"Changed consumer file.")
                with self.assertRaises(PixlError) as failure:
                    graph.validate(self.doc, self.root)
                self.assertEqual(failure.exception.code, "file_hash")
                target.write_bytes(original)

    def test_new_requested_revision_does_not_reuse_old_proof(self):
        self.retain()
        self.replace_source()
        candidate = copy.deepcopy(self.doc)
        candidate.records["source"].fields["dg"] = graph.file_hash(self.source)
        with self.assertRaises(PixlError) as failure:
            graph.validate(candidate, self.root)
        self.assertEqual(failure.exception.code, "stale_evidence")
        candidate.records["proof"].fields["ob"] = True
        candidate.records["source"].fields["dg"] = "1" * 64
        with self.assertRaises(PixlError) as failure:
            graph.validate(candidate, self.root)
        self.assertEqual(failure.exception.code, "file_hash")

    def test_source_line_range_is_checked_against_retained_bytes(self):
        self.retain()
        self.replace_source()
        candidate = copy.deepcopy(self.doc)
        candidate.records["proof"].fields["ob"] = True
        candidate.records["source"].fields["ln"] = [1, 900]
        with self.assertRaises(PixlError) as failure:
            graph.validate(candidate, self.root)
        self.assertEqual(failure.exception.code, "source_range")

    def test_repeat_retention_is_idempotent_after_update(self):
        self.retain()
        self.replace_source()
        self.assertEqual(self.retain()["new_snapshots"], 0)
        self.assertEqual((self.folder / "state.px").read_bytes(), self.state)

    def test_relocated_project_resolves_its_own_snapshots(self):
        self.retain()
        self.replace_source()
        with TemporaryDirectory() as target:
            moved = Path(target).resolve() / "moved project"
            shutil.copytree(self.root, moved)
            report = service.workflow(moved / ".pixl/state.px", moved)
            self.assertTrue(
                Path(report["retained_sources"][0]["retained_path"]).is_relative_to(
                    moved
                )
            )

    def test_project_source_retrieval_and_current_library_stay_distinct(self):
        self.retain()
        current = self.replace_source()
        args = {
            "path": "kit/resources/method.txt",
            "expect": self.sha,
            "start": 1,
            "end": 2,
        }
        retained = service.call("pixl_source", args, self.root)
        self.assertEqual(retained["text"], self.original.decode())
        self.assertTrue(retained["retained_revision"])
        with patch("pixl.service.resource_root", return_value=self.kit / "resources"):
            live = service.call(
                "pixl_source",
                {
                    "scope": "library",
                    "path": "method.txt",
                    "expect": hashlib.sha256(current).hexdigest(),
                    "start": 1,
                    "end": 1,
                },
                self.root,
            )
        self.assertEqual(live["text"], current.decode())
        self.assertNotIn("retained_revision", live)

    def test_native_mcp_retention_then_cli_cold_resume(self):
        call = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "pixl_retain_library",
                "arguments": {
                    "store": ".pixl",
                    "expect": self.initial["hash"],
                    "library": "kit",
                },
            },
        }
        result = subprocess.run(
            [sys.executable, "-B", "-m", "pixl", "mcp", "--root", str(self.root)],
            cwd=ROOT,
            input=json.dumps(call) + "\n",
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        response = json.loads(result.stdout)["result"]
        self.assertFalse(response.get("isError", False), response)
        self.replace_source()
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "pixl",
                "workflow",
                str(self.folder / "state.px"),
                "--root",
                str(self.root),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout)["retained_sources"][0]["expected_sha256"],
            self.sha,
        )

    def test_shared_source_file_is_retained_once(self):
        candidate = copy.deepcopy(self.doc)
        candidate.revision += 1
        candidate.records["source.second"] = Record(
            "source.second", "S", dict(candidate.records["source"].fields)
        )
        current = store.commit(self.folder, candidate, self.initial["hash"], self.root)
        result = retention.retain(self.folder, current["hash"], "kit", self.root)
        self.assertEqual(result["sources"], ["source", "source.second"])
        self.assertEqual(result["new_snapshots"], 1)

    def test_all_sources_are_preflighted_before_publication(self):
        candidate = copy.deepcopy(self.doc)
        candidate.revision += 1
        missing = self.kit / "resources/later.txt"
        missing.write_bytes(b"A second original source.\n")
        candidate.records["source.later"] = Record(
            "source.later",
            "S",
            {
                "ur": "kit/resources/later.txt",
                "dg": graph.file_hash(missing),
                "ln": [1, 1],
                "at": "2026-11-07",
                "au": Symbol("study"),
            },
        )
        manifest = json.loads((self.kit / "bundle-manifest.json").read_text("utf-8"))
        manifest["files"].append(
            {"path": "resources/later.txt", "sha256": graph.file_hash(missing)}
        )
        (self.kit / "bundle-manifest.json").write_text(json.dumps(manifest), "utf-8")
        current = store.commit(self.folder, candidate, self.initial["hash"], self.root)
        missing.unlink()
        with self.assertRaises(PixlError) as failure:
            retention.retain(self.folder, current["hash"], "kit", self.root)
        self.assertEqual(failure.exception.code, "library_source_missing")
        self.assertFalse((self.root / retention.CACHE).exists())
