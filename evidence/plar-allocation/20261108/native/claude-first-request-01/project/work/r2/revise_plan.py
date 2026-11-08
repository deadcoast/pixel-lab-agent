"""Author the PX2 plan-revision document for queue.ready (local helper, no network).

Reads a decoded state JSON (argv[1]), changes only criterion.ready.family_sample_suitability
(check text plus provenance to the r2 artifacts), adds S records for the r2 packet/criteria
and the caller review, bumps the revision, and writes the candidate document (argv[2]).
Commit goes through pixl_commit with the expected hash; nothing under .pixl is edited here.
"""
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
src_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
doc = json.loads(src_path.read_text(encoding="utf-8"))
records = {r["id"]: r for r in doc["records"]}

NEW_CHECK = json.loads((ROOT / "work/queue-ready-criteria-r2.json").read_text(encoding="utf-8"))
NEW_CHECK = next(c for o in NEW_CHECK["outputs"] for c in o["criteria"] if c["id"] == "family_sample_suitability")["check"]

at = datetime.now(UTC).isoformat(timespec="microseconds")


def source(rel):
    data = (ROOT / rel).read_bytes()
    lines = data.count(b"\n") or 1
    return {"ur": rel, "dg": hashlib.sha256(data).hexdigest(), "ln": [1, lines], "at": at, "au": {"$symbol": "local"}}


new_sources = {
    "source.11": source("work/request-review-r2.json"),
    "source.12": source("work/queue-ready-criteria-r2.json"),
    "source.13": source("work/caller-review-1.json"),
}
for sid in new_sources:
    assert sid not in records, sid
    doc["records"].append({"id": sid, "kind": "S", "fields": new_sources[sid]})

q = records["criterion.ready.family_sample_suitability"]["fields"]
# Replace r1 packet/criteria citations (source.1, source.4) with the r2 ones; keep the rest.
q["so"] = [s for s in q["so"] if s["$ref"] not in {"source.1", "source.4"}] + [
    {"$ref": "source.11"}, {"$ref": "source.12"}, {"$ref": "source.13"}]
q["ck"] = NEW_CHECK

p = records["project"]["fields"]
p["sc"] = p["sc"] + [{"$ref": s} for s in new_sources]

doc["revision"] += 1
out_path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print("revision", doc["revision"], "at", at)
