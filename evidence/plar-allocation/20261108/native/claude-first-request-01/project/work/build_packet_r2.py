"""Derive r2 criteria/packet from retained r1 artifacts (local helper, no network).

Changes only criterion family_sample_suitability per work/caller-review-1.json.
Original artifacts are read, never rewritten. Arguments and connection are reused.
"""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str):
    return json.loads((WORK / name).read_text(encoding="utf-8"))


def write(name: str, obj) -> Path:
    p = WORK / name
    if p.exists():
        raise SystemExit(f"refusing to overwrite {p}")
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return p


R1_PACKET = "request-review.json"
R1_CRITERIA = "queue-ready-criteria.json"
assert sha(WORK / R1_PACKET) == "01f9fc581956766688574f5247d9b9a09273e460296f1e818fd48a2be101ea81"
assert sha(WORK / R1_CRITERIA) == "43c728d81b697ef077457f376876679a05e65018868d95c85ca8ef1396e084d0"

criteria = copy.deepcopy(load(R1_CRITERIA))
hits = [c for o in criteria["outputs"] for c in o["criteria"] if c["id"] == "family_sample_suitability"]
assert len(hits) == 1
hits[0]["check"] = (
    "Silhouette construction, edge handling and color treatment form a coherent treatment "
    "that could plausibly carry the Working/Retry/Paused members at 16x16 (including "
    "non-color-distinct motifs); the review decision is recorded."
)
# basis, scope, sources, domain, mode intentionally unchanged.

crit_path = write("queue-ready-criteria-r2.json", criteria)

packet = copy.deepcopy(load(R1_PACKET))
packet["criteria"] = {"path": "work/queue-ready-criteria-r2.json", "sha256": sha(crit_path)}
# request (arguments) and connection pointers unchanged; verify they still match bytes.
assert packet["request"]["sha256"] == sha(ROOT / packet["request"]["path"])
assert packet["connection"]["sha256"] == sha(ROOT / packet["connection"]["path"])
packet_path = write("request-review-r2.json", packet)

for p in (crit_path, packet_path):
    print(p.relative_to(ROOT).as_posix(), sha(p))
