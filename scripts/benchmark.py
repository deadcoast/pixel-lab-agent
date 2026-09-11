"""Equal-semantics representation size comparison; no LLM reasoning claim."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pixl.codec import encode, to_data
from pixl.graph import context
from pixl.service import load_document


def run():
    doc = load_document(ROOT / "examples/atelier/project.px")
    payload = {"revision": doc.revision, "records": [{"id": r.id, "kind": r.kind, "fields": to_data(r.fields)} for r in sorted(doc.records.values(), key=lambda r: r.id)]}
    forms = {"pixl": encode(doc).decode("utf-8"),
             "json_tuple_lossless": json.dumps([doc.revision, [[r["id"], r["kind"], r["fields"]] for r in payload["records"]]], ensure_ascii=False, separators=(",", ":")),
             "json_compact_lossless": json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
             "json_pretty_lossless": json.dumps(payload, ensure_ascii=False, indent=2)}
    sizes = {name: {"utf8_bytes": len(text.encode("utf-8"))} for name, text in forms.items()}
    bootstrap = (ROOT / "spec/PIXL-1.md").read_text(encoding="utf-8") + (ROOT / "pixl/registry.json").read_text(encoding="utf-8")
    bootstrap_counts = {"utf8_bytes": len(bootstrap.encode("utf-8"))}
    token_status = "not_measured: install pixl-agent[benchmark]"
    try:
        import tiktoken
        for encoding_name in ("cl100k_base", "o200k_base"):
            encoder = tiktoken.get_encoding(encoding_name)
            for name, text in forms.items():
                sizes[name][encoding_name] = len(encoder.encode(text, disallowed_special=()))
            bootstrap_counts[encoding_name] = len(encoder.encode(bootstrap, disallowed_special=()))
        token_status = f"measured with tiktoken {tiktoken.__version__}"
    except ImportError:
        pass
    packet = encode(context(doc, "produce"))
    library = load_document(ROOT / "knowledge/library.px")
    selected = context(library, "k.palette-contract")
    return {"fixture": "examples/atelier/project.px", "records": len(doc.records), "same_semantic_payload": True,
            "sizes": sizes, "bootstrap_spec_plus_registry": bootstrap_counts, "token_status": token_status,
            "context_bytes": len(packet),
            "knowledge_retrieval": {"library_bytes": len(encode(library)), "packet_bytes": len(encode(selected)),
                                    "library_records": len(library.records), "packet_records": len(selected.records),
                                    "focus": "k.palette-contract", "required_closure_complete": True},
            "limitations": ["Single fixture; no language-model accuracy/latency trial.",
                            "JSON comparison retains explicit Ref/Symbol types, so it is not ordinary untyped JSON.",
                            "No claim that byte density or unfamiliar notation improves model reasoning.",
                            "Bootstrap cost is separate and must be amortized across actual project operation."]}


if __name__ == "__main__":
    out = ROOT / "evidence/representation-benchmark.json"
    out.parent.mkdir(exist_ok=True)
    result = run()
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
