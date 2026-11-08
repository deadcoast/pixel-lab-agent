"""Build the refreshed plar.txt document for the queue.ready rev2 update.

Reads the current plar.txt, applies only the reconciled changes (source rebinds for
BRIEF.md and src/queue-view.ts, queue.ready destination move and owner check-mark
requirement, failure record) and writes the complete document for pixl plar save.
Run: python -I plar-refresh.py PROJECT_ROOT OUTPUT_JSON
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
doc = json.loads((root / "plar.txt").read_text(encoding="utf-8"))

NEW = {
    "brief": "aebe00949f3a9510a44f6f554b8fc97e53476d7658a4bb29419db85b417f02ab",
    "queue-view": "4d6ee92e40374d4dd4c6a49a3a20a6caf34e7f2d61a32a230c8ecf54691b5c49",
}
for s in doc["sources"]:
    if s["id"] in NEW:
        s["sha256"] = NEW[s["id"]]

doc["coverage"]["included"].append(
    "Refresh for the Ready update: re-read BRIEF.md (aebe0094...) line 9 and src/queue-view.ts "
    "(4d6ee92e...) in full. succeeded now maps to assets/ready-confirmed.png (moved destination, "
    "same Ready role and queue.ready ID); Start (assets/start.svg), Working (assets/working.png, 4 frames), "
    "Paused (assets/paused.png) and Retry (assets/error-retry.png) rows, display descriptor and earlier "
    "brief paragraphs are unchanged. The Ready check mark with asymmetrical arms is now an owner "
    "requirement (BRIEF.md line 9) replacing the former sample_motif proposal."
)

row = next(a for a in doc["assets"] if a["id"] == "queue.ready")
assert row["delivery"]["path"] == "assets/ready.png"

for c in row["consumers"]:
    if c["symbol"] == "statusVisuals.succeeded":
        c["usage"] = ("Maps succeeded to the Ready image path assets/ready-confirmed.png "
                      "(moved from assets/ready.png) with frames 1.")

row["existing"] = [{
    "path": "assets/ready-confirmed.png",
    "role": ("Current required Ready destination from the updated view is missing; no reusable Ready "
             "image was supplied. The previous assets/ready.png target is superseded by the updated view."),
}]

reqs = []
for r in row["requirements"]:
    if r["property"] == "sample_motif":
        reqs.append({
            "property": "completion_mark",
            "value": "Ready must visibly use a check mark with asymmetrical arms to convey successful completion.",
            "authority": "requirement",
            "sources": ["brief"],
            "reason": ("BRIEF.md line 9 (current update) makes the asymmetrical-arm check mark an owner "
                       "requirement; it supersedes the earlier unsourced sample_motif proposal. Which arm is "
                       "longer, stroke weight and other construction details remain open specialist choices."),
        })
    else:
        reqs.append(r)
row["requirements"] = reqs

checks = row["delivery"]["checks"]
row["delivery"] = {
    "path": "assets/ready-confirmed.png",
    "checks": [
        checks[0],
        checks[1],
        "Confirm at 1x and 3x nearest on #172336 that the Ready image visibly uses a check mark with asymmetrical arms conveying successful completion.",
        *checks[2:],
    ],
}

row["evidence"].append({
    "path": "work/queue.ready/provider-observation-failed.json",
    "note": ("Caller list_jobs observation on the originating controlled pixellab-test connection: "
             "first_request (remote_id controlled-create-0001) failed with no image; provider_simulated=true. "
             "Recorded in .pixl/assets/queue.ready state revision 4 (hash b9c3a2f7...), next_action review_failure. "
             "sha256 9b6b983b63a60449a604f80fed2c7d009ec69949074025b4ad5d4641732d8619."),
})

row["next"] = (
    "first_request (remote_id controlled-create-0001, controlled pixellab-test, provider_simulated=true) was "
    "observed failed with no image (work/queue.ready/provider-observation-failed.json) and is retained with its "
    "contract. Next: prepare one revised request for queue.ready under the refreshed contract (packet "
    "work/queue.ready/rev2/request-review.json: asymmetrical-arm check mark, destination "
    "assets/ready-confirmed.png); the caller compares it independently, then dispatches the one further "
    "authorized controlled request. Afterwards retrieve/import any real candidate, inspect it at 1x/3x nearest "
    "on #172336, record the Ready style decision before expanding Working/Retry/Paused. Not integrated."
)

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out)
