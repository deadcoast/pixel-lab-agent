"""Compile curated knowledge and actual bounded POC receipts into operational PIXL."""

import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pixl.codec import Document, Record, Ref, Symbol, encode, record_hash
from pixl.graph import file_hash, proof_scope, validate


def build():
    corpus = json.loads((ROOT / "knowledge/pixel-art.json").read_text(encoding="utf-8"))
    report_path = ROOT / "evidence/art-methods/poc-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report["implementation_sha256"] != file_hash(ROOT / "pixl/poc.py"):
        raise RuntimeError("POC runner changed; execute current proofs before compiling knowledge")
    if report.get("knowledge_sha256") != file_hash(ROOT / "knowledge/pixel-art.json"):
        raise RuntimeError("POC knowledge changed or receipt lacks its hash; execute current proofs before compiling knowledge")
    aliases = {}
    def atom(phrase):
        base = re.sub(r"[^a-z0-9]+", "_", phrase.lower()).strip("_")
        if not base or not base[0].isalpha():
            base = "a_" + base
        base = base[:70] + "_" + hashlib.sha256(phrase.encode()).hexdigest()[:8]
        aliases[base] = phrase
        return Symbol(base)
    for method in corpus["methods"]:
        for phrase in method["applies_to"]:
            atom(phrase)
    alias_path = ROOT / "knowledge/applicability.json"
    alias_path.write_text(json.dumps({"version": 1, "symbols": aliases}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    doc = Document(0)
    def add(record):
        doc.records[record.id] = record
        return Ref(record.id)
    def source(path, start=None, end=None):
        relative = Path(path).as_posix()
        key = "s" + hashlib.sha256(f"{relative}:{start}:{end}".encode()).hexdigest()[:20]
        return add(Record(key, "S", {"ur": relative, "dg": file_hash(ROOT / relative),
                   "ln": [start, end] if start is not None else [], "at": "2026-09-10", "au": Symbol("local")}))
    vocabulary = source("knowledge/applicability.json")
    implementation = source("pixl/poc.py")
    curated = source("knowledge/pixel-art.json")
    evidence_ids = []
    for method in corpus["methods"]:
        id_ = "k." + method["id"]
        fields = {"nm": method["title"], "ap": [atom(s) for s in method["applies_to"]],
                  "op": method["procedure"], "ck": method["checks"], "rq": method["requires"], "rk": method["pitfalls"],
                  "so": [vocabulary, implementation, curated] + [source(s["path"], s["start"], s["end"]) for s in method["sources"]], "tg": [method["id"]]}
        checks = [c for c in report["checks"] if method["id"] in c["method_ids"]]
        if checks:
            eid = "e." + method["id"]
            fields["pc"] = [Ref(eid)]
            add(Record(eid, "E", {"nm": "Bounded reference POC: " + ",".join(c["id"] for c in checks),
                      "ur": "evidence/art-methods/poc-report.json", "dg": file_hash(report_path),
                      "rs": Symbol("pass" if all(c["status"] == "pass" for c in checks) else "fail"),
                      "md": Symbol("local"), "at": "2026-09-10", "bs": []}))
            evidence_ids.append((eid, id_))
        add(Record(id_, "K", fields))
    for eid, method in evidence_ids:
        doc.records[eid].fields["bs"] = [{"rf": Ref(id_), "dg": record_hash(doc.records[id_])} for id_ in sorted(proof_scope(doc, [method]))]
    validate(doc, ROOT)
    path = ROOT / "knowledge/library.px"
    path.write_bytes(encode(doc))
    return {"records": len(doc.records), "methods": len(corpus["methods"]), "methods_with_executed_reference_poc": len(evidence_ids), "bytes": path.stat().st_size}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
