import json
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from pixl.codec import PixlError, encode
from pixl.graph import context, validate
from pixl.service import load_document
from scripts import build_knowledge
from scripts.build_knowledge import build

ROOT = Path(__file__).resolve().parents[1]


class KnowledgeCompilationTests(unittest.TestCase):
    def copy_inputs(self, root):
        report = json.loads((ROOT / "evidence/art-methods/poc-report.json").read_text(encoding="utf-8"))
        names = ["pixl/poc.py", "knowledge/pixel-art.json", "evidence/art-methods/poc-report.json"]
        names.extend(report["source_sha256"])
        names.extend("evidence/art-methods/" + a["path"] for a in report["artifacts"])
        for name in names:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        return report

    def test_all_source_prerequisites_procedures_checks_and_pitfalls_survive(self):
        build()
        doc = load_document(ROOT / "knowledge/library.px")
        validate(doc, ROOT)
        corpus = json.loads((ROOT / "knowledge/pixel-art.json").read_text(encoding="utf-8"))
        aliases = json.loads((ROOT / "knowledge/applicability.json").read_text(encoding="utf-8"))["symbols"]
        self.assertEqual(sum(r.kind == "K" for r in doc.records.values()), len(corpus["methods"]))
        for method in corpus["methods"]:
            with self.subTest(method=method["id"]):
                fields = doc.records["k." + method["id"]].fields
                self.assertEqual(fields["op"], method["procedure"])
                self.assertEqual(fields["ck"], method["checks"])
                self.assertEqual(fields["rq"], method["requires"])
                self.assertEqual(fields["rk"], method["pitfalls"])
                self.assertEqual([aliases[a.value] for a in fields["ap"]], method["applies_to"])
                ranges = {(doc.records[s.id].fields["ur"], tuple(doc.records[s.id].fields["ln"])) for s in fields["so"]}
                for source in method["sources"]:
                    self.assertIn((source["path"], (source["start"], source["end"])), ranges)

    def test_context_selects_only_requested_method_and_required_evidence(self):
        build()
        doc = load_document(ROOT / "knowledge/library.px")
        packet = context(doc, "k.palette-contract")
        validate(packet, ROOT)
        self.assertEqual([r.id for r in packet.records.values() if r.kind == "K"], ["k.palette-contract"])
        self.assertTrue(any(r.kind == "E" for r in packet.records.values()))
        self.assertLess(len(encode(packet)), len(encode(doc)) // 4)

    def test_changed_curated_methods_cannot_reuse_old_poc_receipt(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("pixl/poc.py", "knowledge/pixel-art.json", "evidence/art-methods/poc-report.json"):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            path = root / "knowledge/pixel-art.json"
            corpus = json.loads(path.read_text(encoding="utf-8"))
            corpus["methods"][0]["procedure"] = ["a changed unproved procedure"]
            path.write_text(json.dumps(corpus), encoding="utf-8")
            with patch.object(build_knowledge, "ROOT", root), self.assertRaisesRegex(RuntimeError, "knowledge changed"):
                build_knowledge.build()

    def test_changed_research_cannot_be_rebound_to_old_poc(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = self.copy_inputs(root)
            source = root / next(iter(report["source_sha256"]))
            source.write_bytes(source.read_bytes() + b"\nChanged research.\n")
            with patch.object(build_knowledge, "ROOT", root), self.assertRaisesRegex(RuntimeError, "POC source changed"):
                build_knowledge.build()

    def test_corrupt_fixture_cannot_be_published_as_passing(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = self.copy_inputs(root)
            (root / "evidence/art-methods" / report["artifacts"][0]["path"]).write_bytes(b"corrupt fixture")
            with patch.object(build_knowledge, "ROOT", root), self.assertRaisesRegex(RuntimeError, "POC artifact changed"):
                build_knowledge.build()

    def test_artifact_drift_is_rejected_in_compiled_method_context(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = self.copy_inputs(root)
            with patch.object(build_knowledge, "ROOT", root):
                build_knowledge.build()
            doc = load_document(root / "knowledge/library.px")
            packet = context(doc, "k.palette-contract")
            validate(packet, root)
            self.assertEqual(sum(r.kind == "X" for r in packet.records.values()), len(report["artifacts"]))
            (root / "evidence/art-methods" / report["artifacts"][0]["path"]).write_bytes(b"changed after compilation")
            with self.assertRaisesRegex(PixlError, "file_hash"):
                validate(packet, root)

    def test_unbound_source_manifest_cannot_support_compilation(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = self.copy_inputs(root)
            report.pop("source_sha256")
            (root / "evidence/art-methods/poc-report.json").write_text(json.dumps(report), encoding="utf-8")
            with patch.object(build_knowledge, "ROOT", root), self.assertRaisesRegex(RuntimeError, "source manifest"):
                build_knowledge.build()
