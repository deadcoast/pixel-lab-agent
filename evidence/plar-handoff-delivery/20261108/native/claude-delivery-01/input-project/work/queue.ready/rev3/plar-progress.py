"""Update queue.ready progress fields (next, evidence) after the rev3 preparation.

Run: python -I plar-progress.py PROJECT_ROOT OUTPUT_JSON
Changes only the queue.ready row's `next` and appends evidence entries.
"""
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
doc = json.loads((root / "plar.txt").read_text(encoding="utf-8"))
row = next(a for a in doc["assets"] if a["id"] == "queue.ready")
assert row["production"]["task"] == "r.028f320bf7292612.task"
assert row["production"]["output"] == "r.028f320bf7292612.output.ready"


def sha(rel):
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


R2, R3 = "work/queue.ready/rev2", "work/queue.ready/rev3"
row["next"] = (
    "Revised request r.028f320bf7292612.request (task r.028f320bf7292612.task, output "
    "r.028f320bf7292612.output.ready, store .pixl/assets/queue.ready revision 9) is prepared and NOT dispatched; "
    "controlled pixellab-test, provider_simulated=true. Caller: independently compare "
    "work/queue.ready/rev3/request-review.json against BRIEF/OWNER/source, reread this row, then claim dispatch of "
    "that existing job and submit exactly its saved arguments as the one further authorized controlled request "
    "(OWNER.md line 7, still unused); record the actual response. first_request (controlled-create-0001) remains "
    "failed with no image; rev2 job r.f9e2fa53f4fcac2a.request was withdrawn locally before dispatch "
    "(work/queue.ready/rev2/withdrawal.json). Later: retrieve/import any real candidate, inspect at 1x/3x nearest on "
    "#172336 against the eight rev3 criteria, record the Ready style decision before expanding "
    "Working/Retry/Paused, then deliver to assets/ready-confirmed.png. Not integrated."
)
row["evidence"].extend([
    {"path": f"{R2}/caller-review.json",
     "note": (f"Independent caller comparison of the rev2 packet: changes_requested (check-mark-asymmetrical-arms "
              f"narrowed 'asymmetrical arms' to unequal length). sha256 {sha(f'{R2}/caller-review.json')}.")},
    {"path": f"{R2}/withdrawal.json",
     "note": (f"Caller local withdrawal of undispatched rev2 job r.f9e2fa53f4fcac2a.request (no remote identity, "
              f"not a provider observation). sha256 {sha(f'{R2}/withdrawal.json')}.")},
    {"path": f"{R3}/request-review.json",
     "note": (f"Third-generation Ready request/criteria packet (sha256 {sha(f'{R3}/request-review.json')}), "
              "requirements_hash 244f4591...; corrects only check-mark-asymmetrical-arms; provider arguments "
              "byte-identical to rev2; prepared as job r.028f320bf7292612.request, not dispatched; "
              "independent caller comparison not yet performed; provider_simulated=true; no image, review or integration.")},
    {"path": f"{R3}/request-review-report.json",
     "note": (f"pixl request-review locator report for the rev3 packet: all cited lines resolved, no diagnostics; "
              f"not a consistency verdict. sha256 {sha(f'{R3}/request-review-report.json')}.")},
])
out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out)
