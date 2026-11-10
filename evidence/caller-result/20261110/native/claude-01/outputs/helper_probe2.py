"""Second probe: production continuation, jobs, delivery, task states, stale plan review identity, file hashes."""
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = root / "work" / "compact-caller"


def sha(rel: str) -> str:
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


plar = json.loads((out / "specialist-plar-read.json").read_text("utf-8"))
prod = plar["production"]
trimmed = {k: v for k, v in prod.items() if k != "outputs"}
print("PRODUCTION (no outputs):")
print(json.dumps(trimmed, indent=1))
print("OUTPUT summary:")
for o in prod["outputs"]:
    reqs = o.get("requirements", [])
    print(" ", o["id"], o.get("candidate"), "requirements", len(reqs), "statuses", sorted({r.get("status") for r in reqs}))
asset = plar["asset"]
print("ASSET next:", json.dumps(asset.get("next"))[:800])
print("ASSET production:", json.dumps(asset.get("production"))[:1500])
print("ASSET delivery:", json.dumps(asset.get("delivery"))[:1500])
print("ASSET evidence:", json.dumps(asset.get("evidence"))[:1500])
print("ASSET existing:", json.dumps(asset.get("existing"))[:1500])
print("ASSET consumers:", json.dumps(asset.get("consumers"))[:1500])

wf = json.loads((out / "specialist-workflow.json").read_text("utf-8"))
for t in wf["tasks"]:
    if t["id"] in ("artistic-02.working.task", "artistic-02.delivery.task", "artistic-01.working.task", "artistic-01.delivery.task", "authoring-01.working.task"):
        tt = dict(t)
        outs = tt.pop("outputs", None)
        print("TASK", json.dumps(tt)[:1800])
        for o in outs or []:
            oo = dict(o)
            cands = oo.pop("candidates", None)
            print("   OUT", json.dumps(oo)[:900])
            for c in cands or []:
                cc = {k: v for k, v in c.items() if k in ("id", "status", "nominated", "accepted", "verdicts", "criteria", "state", "family")}
                print("     CAND", json.dumps(cc)[:700])
print("INTAKE:", json.dumps(wf.get("intake"))[:2500])

rr = json.loads((root / "work/artistic-revision/request-review-02.json").read_text("utf-8"))
print("RR02 keys:", sorted(rr.keys()))
for k in ("state", "plan", "review_scope_sha256", "stages", "delivery", "choices"):
    if k in rr:
        print("RR02", k, json.dumps(rr[k])[:700])

files = [
    "work/compact-caller-inputs/fixtures.json",
    "work/artistic-revision/CALLER-RESULT.json",
    "work/artistic-revision/SPECIALIST-RESULT.json",
    "work/artistic-revision/request-review-02.json",
    "work/artistic-revision/request-review-plan02.json",
    "work/artistic-revision/caller-capture-switch-01/render.json",
    "work/artistic-revision/caller-capture-initial-reduced-01/render.json",
    "work/artistic-revision/capture-switch-04/render.json",
    "work/artistic-revision/capture-initial-reduced-03/render.json",
    "work/artistic-revision/retained-failures.json",
    "work/artistic-revision/adopted-criteria.json",
    "work/artistic-revision/CALLER-REVIEW.json",
    "work/artistic-revision/caller-independent-verification.json",
    "assets/working.png",
    "assets/error-retry.png",
    "assets/paused.png",
    "assets/ready-confirmed.png",
    "src/queue-view-artistic.ts",
    "renderer-artistic/view.mjs",
    "renderer-artistic/capture.mjs",
    "renderer-artistic/check.py",
    ".pixl/handoffs/e560a32dcaf31134abbb81b661a0a2fc12824461a049c90b1c780cc01464273d.json",
    ".pixl/assets/queue.ready/production-plans/9fa2988ddf8a9eae73258d5c3b5fa23dbfc08f6f3dc77b0402fd82855ccbf9a1.json",
    "work/compact-caller/specialist-plar-read.json",
    "work/compact-caller/specialist-workflow.json",
    "work/compact-caller/specialist-validate.json",
    "work/compact-caller/specialist-review-context-working.json",
    "work/compact-caller/specialist-review-context-delivery.json",
]
print("HASHES:")
for f in files:
    p = root / f
    print(" ", f, sha(f) if p.exists() else "MISSING", p.stat().st_size if p.exists() else "")
