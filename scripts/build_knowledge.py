"""Compile curated knowledge and actual bounded POC receipts into operational PIXL."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pixl.codec import Document, Record, Ref, Symbol, encode, record_hash
from pixl.graph import confined, file_hash, proof_scope, validate


def build():
    corpus_bytes = (ROOT / "knowledge/pixel-art.json").read_bytes()
    corpus = json.loads(corpus_bytes)
    report_path = ROOT / "evidence/art-methods/poc-report.json"
    report_bytes = report_path.read_bytes()
    report = json.loads(report_bytes)
    observed_date = report["observed_at"].split("T", 1)[0]
    if report["implementation_sha256"] != file_hash(ROOT / "pixl/poc.py"):
        raise RuntimeError("POC runner changed; execute current proofs before compiling knowledge")
    if report.get("knowledge_sha256") != hashlib.sha256(corpus_bytes).hexdigest():
        raise RuntimeError("POC knowledge changed or receipt lacks its hash; execute current proofs before compiling knowledge")
    source_names = {source["path"] for method in corpus["methods"] for source in method["sources"]}
    expected_sources = report.get("source_sha256", {})
    if set(expected_sources) != source_names:
        raise RuntimeError("POC source manifest missing or incomplete; execute current proofs before compiling knowledge")
    for name, expected in expected_sources.items():
        if file_hash(confined(ROOT, name)) != expected:
            raise RuntimeError(f"POC source changed: {name}; execute current proofs before compiling knowledge")
    artifacts = report.get("artifacts", [])
    if not artifacts or len({a["path"] for a in artifacts}) != len(artifacts):
        raise RuntimeError("POC artifact manifest missing, empty or duplicated")
    for artifact in artifacts:
        if file_hash(confined(report_path.parent, artifact["path"])) != artifact["sha256"]:
            raise RuntimeError(f"POC artifact changed: {artifact['path']}; execute current proofs before compiling knowledge")
    aliases = {}
    def atom(phrase):
        base = re.sub(r"[^a-z0-9]+", "_", phrase.lower()).strip("_")
        if not base or not base[0].isalpha():
            base = f"a_{base}"
        base = f"{base[:70]}_{hashlib.sha256(phrase.encode()).hexdigest()[:8]}"
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

    expected_sources = dict(expected_sources, **{"pixl/poc.py": report["implementation_sha256"],
                            "knowledge/pixel-art.json": report["knowledge_sha256"],
                            "knowledge/applicability.json": file_hash(alias_path)})
    def source(path, start=None, end=None):
        relative = Path(path).as_posix()
        key = f's{hashlib.sha256(f"{relative}:{start}:{end}".encode()).hexdigest()[:20]}'
        return add(Record(key, "S", {"ur": relative, "dg": expected_sources[relative],
                   "ln": [start, end] if start is not None else [], "at": observed_date, "au": Symbol("local")}))

    vocabulary = source("knowledge/applicability.json")
    implementation = source("pixl/poc.py")
    curated = source("knowledge/pixel-art.json")
    artifact_ids = []
    for artifact in artifacts:
        key = hashlib.sha256(artifact["path"].encode()).hexdigest()[:20]
        contract = add(
            Record(
                f"c{key}",
                "C",
                {
                    "nm": "Reference fixture: " + artifact["path"],
                    "px": [artifact["width"], artifact["height"]],
                    "pl": [],
                    "vw": Symbol("ui"),
                    "sa": Symbol("nearest"),
                    "al": Symbol("full"),
                    "li": "Bounded local test fixture; no production aesthetic acceptance",
                },
            )
        )
        aid = "x" + key
        add(Record(aid, "X", {"nm": artifact["path"], "ur": "evidence/art-methods/" + artifact["path"],
                   "dg": artifact["sha256"], "ct": contract, "kd": Symbol("reference"),
                   "mt": {"origin": "local_reference_fixture", "mode": artifact["mode"]}}))
        artifact_ids.append(aid)
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
                      "ur": "evidence/art-methods/poc-report.json", "dg": hashlib.sha256(report_bytes).hexdigest(),
                      "rs": Symbol("pass" if all(c["status"] == "pass" for c in checks) else "fail"),
                      "md": Symbol("local"), "at": report["observed_at"], "bs": []}))
            evidence_ids.append((eid, id_))
        add(Record(id_, "K", fields))
    for eid, method in evidence_ids:
        # The aggregate receipt owns every listed artifact; retaining all bindings
        # prevents a partial context packet from concealing drift in that receipt.
        doc.records[eid].fields["bs"] = [{"rf": Ref(id_), "dg": record_hash(doc.records[id_])} for id_ in sorted(proof_scope(doc, [method] + artifact_ids))]
    validate(doc, ROOT)
    path = ROOT / "knowledge/library.px"
    path.write_bytes(encode(doc))
    return {"records": len(doc.records), "methods": len(corpus["methods"]), "methods_with_executed_reference_poc": len(evidence_ids), "bytes": path.stat().st_size}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
