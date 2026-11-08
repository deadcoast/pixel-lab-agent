"""Derive the refreshed plar.txt document for the queue.ready rev2 update.

Reads the current plar.txt, changes only: brief/queue-view source hashes, coverage
lines for this refresh, and the queue.ready row (destination move, new owner
requirement, motif reconciliation, checks, next, evidence). Other rows untouched.
Writes work/queue.ready/rev2/plar-refresh.json for `plar save --expect`.
"""
import copy
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
doc = json.loads((root / "plar.txt").read_text(encoding="utf-8"))
before = copy.deepcopy(doc)

NEW = {"brief": "aebe00949f3a9510a44f6f554b8fc97e53476d7658a4bb29419db85b417f02ab",
       "queue-view": "4d6ee92e40374d4dd4c6a49a3a20a6caf34e7f2d61a32a230c8ecf54691b5c49"}
for s in doc["sources"]:
    if s["id"] in NEW:
        s["sha256"] = NEW[s["id"]]

cov = doc["coverage"]
cov["included"][0] = ("Read BRIEF.md and SOURCE-MAP.md in full; re-read the changed brief (current update paragraph, line 9) "
                      "and changed queue-view (statusVisuals.succeeded, line 6) for this refresh; queue-state, start.svg and SOURCE-MAP.md are byte-unchanged.")
cov["included"][3] = ("Inspect the only checked-in art, assets/start.svg, at source level for shape, dimensions and accent; "
                      "verify the four current PNG destinations (working.png, paused.png, ready-confirmed.png, error-retry.png) are absent.")
cov["included"].insert(5, "Reconcile the Ready destination move from assets/ready.png to assets/ready-confirmed.png while preserving its queue.ready ID, "
                          "unchanged success/completion purpose and existing production history; add the brief's asymmetrical-arm check-mark requirement to queue.ready only.")
cov["unresolved"][1] = ("No approved style reference exists. Ready remains the proposed representative sample (now required to use an asymmetrical-arm check mark); "
                        "Working, Retry and Paused depend on its review before family expansion.")

ready = next(a for a in doc["assets"] if a["id"] == "queue.ready")
ready["consumers"][0]["usage"] = "Maps succeeded to the Ready label, current assets/ready-confirmed.png path and one static frame."
ready["existing"] = [{"path": "assets/ready-confirmed.png",
                      "role": "Current required Ready destination is missing; the previous assets/ready.png target is superseded by the updated view. No reusable Ready image was supplied."}]

reqs = ready["requirements"]
idx = {r["property"]: i for i, r in enumerate(reqs)}
reqs[idx["sample_motif"]] = {
    "property": "sample_motif",
    "value": ("The check-mark form is now an owner requirement (see ready_check_mark). Remaining motif details are proposals for style review: "
              "stroke weight, arm proportions and orientation, highlight treatment and the absence of a backing plate or badge."),
    "authority": "proposal",
    "sources": [],
    "reason": "The current brief fixes a check mark with asymmetrical arms but not its stroke weight, exact proportions, orientation, shading or framing."}
reqs.insert(idx["state_meaning"] + 1, {
    "property": "ready_check_mark",
    "value": "Ready visibly uses a check mark with asymmetrical arms to convey successful completion.",
    "authority": "requirement",
    "sources": ["brief"],
    "reason": "The brief's current update requires this specific mark; the exact arm ratio, orientation and stroke weight are not specified."})
reqs.append({
    "property": "destination_update",
    "value": "The current Ready destination is assets/ready-confirmed.png; the established queue.ready asset identity, success/completion purpose and production history are unchanged.",
    "authority": "observation",
    "sources": ["brief", "queue-view"],
    "reason": "The current brief says the destination follows the updated view; statusVisuals.succeeded supplies the new path. Previous allocation bytes remain in PLAR history."})

ready["delivery"] = {
    "path": "assets/ready-confirmed.png",
    "checks": [
        "Decode the delivered PNG and confirm the row-specific dimensions and frame count.",
        "Confirm a transparent background without opaque matte pixels; do not impose an unstated binary-alpha rule.",
        "Inspect at 1x and 3x nearest scaling on #172336 for readable silhouettes, edge quality and cool blue family coherence.",
        "Inspect at 1x and 3x nearest on #172336 that the mark is visibly a check mark with asymmetrical arms conveying successful completion.",
        "Exercise both statusCell and compactStatus in an actual renderer and confirm the intended label and asset appear for the relevant queue transition.",
        "Record visual review and consumer integration evidence separately from mechanical checks; no delivered art has yet been reviewed.",
        "Review and record the representative sample decision before expanding the other status assets; source-bind the approved visual reference for later handoff.",
        "Compare the Paused silhouette against this status at 1x and 3x, including grayscale/non-color comparison, to confirm Paused remains distinct from activity, completion and retry.",
        "Confirm statusVisuals.succeeded resolves assets/ready-confirmed.png; do not deliver new Ready art to the superseded assets/ready.png path."]}

ready["next"] = ("First attempt first_request (pixellab-test, remote_id controlled-create-0001, provider_simulated=true) is terminal failed without an image, "
                 "observed by the caller on its originating connection (work/queue.ready/rev2/original-status.json). The brief and view changed: Ready now needs an "
                 "asymmetrical-arm check mark at assets/ready-confirmed.png. Next: specialist prepares the revised packet in work/queue.ready/rev2/ and a revised "
                 "generation in .pixl/assets/queue.ready via plar prepare --revise; caller independently compares it, then claims dispatch and submits the one further "
                 "controlled pixellab-test request. No image, style approval or integration exists. Not integrated.")
ready["evidence"].append({
    "path": "work/queue.ready/rev2/original-status.json",
    "note": "Caller's pixellab-test list_jobs observation at resume: controlled-create-0001 failed without an image (provider_simulated=true); recorded on job first_request (store revision 4, hash 47ef2326...). sha256 7d0e1b38718e6bed9740a175e47798f3e409469c9295818dfaf75ff4f0f10bab."})

# Guard: every other row must be byte-identical in JSON terms.
for a, b in zip(before["assets"], doc["assets"]):
    if a["id"] != "queue.ready":
        assert a == b, a["id"]
assert [a["id"] for a in before["assets"]] == [a["id"] for a in doc["assets"]]

out = root / "work/queue.ready/rev2/plar-refresh.json"
out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out)
