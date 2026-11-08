"""Update queue.ready progress fields (next, evidence) after the rev2 preparation.

Run: python -I plar-progress.py PROJECT_ROOT OUTPUT_JSON
"""
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
doc = json.loads((root / "plar.txt").read_text(encoding="utf-8"))
row = next(a for a in doc["assets"] if a["id"] == "queue.ready")
assert row["production"]["task"] == "r.f9e2fa53f4fcac2a.task"


def sha(rel):
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


row["next"] = (
    "Revised request r.f9e2fa53f4fcac2a.request (task r.f9e2fa53f4fcac2a.task, output "
    "r.f9e2fa53f4fcac2a.output.ready, store .pixl/assets/queue.ready revision 6) is prepared and NOT dispatched; "
    "controlled pixellab-test, provider_simulated=true. Caller: independently compare "
    "work/queue.ready/rev2/request-review.json against BRIEF/OWNER/source, reread this row, then claim dispatch of "
    "that existing job and submit exactly its saved arguments as the one further authorized controlled request; "
    "record the actual response. first_request (controlled-create-0001) remains failed with no image "
    "(work/queue.ready/provider-observation-failed.json). Later: retrieve/import any real candidate, inspect at 1x/3x "
    "nearest on #172336 against the eight rev2 criteria, record the Ready style decision before expanding "
    "Working/Retry/Paused, then deliver to assets/ready-confirmed.png. Not integrated."
)
row["evidence"].extend([
    {"path": "work/queue.ready/rev2/request-review.json",
     "note": (f"Revised Ready request/criteria packet (sha256 {sha('work/queue.ready/rev2/request-review.json')}), "
              "requirements_hash 244f4591...; prepared as job r.f9e2fa53f4fcac2a.request, not dispatched; "
              "independent caller comparison not yet performed; provider_simulated=true; no image, review or integration.")},
    {"path": "work/queue.ready/rev2/request-review-report.json",
     "note": (f"pixl request-review locator report for the rev2 packet: all cited lines resolved, no diagnostics; "
              f"not a consistency verdict. sha256 {sha('work/queue.ready/rev2/request-review-report.json')}.")},
])
out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out)
