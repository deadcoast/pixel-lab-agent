import json
from pathlib import Path
import unittest

from pixl.codec import Ref, encode
from pixl.graph import context, validate
from pixl.service import load_document
from scripts.build_knowledge import build

ROOT = Path(__file__).resolve().parents[1]


class KnowledgeCompilationTests(unittest.TestCase):
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
