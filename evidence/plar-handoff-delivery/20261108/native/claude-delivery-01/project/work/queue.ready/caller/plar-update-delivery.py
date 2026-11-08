"""Caller helper: update only the queue.ready row after delivery and the consumer check.

Run from the consumer root:
  python -I work/queue.ready/caller/plar-update-delivery.py work/queue.ready/caller/plar-update-delivery.json
Changes queue.ready status/existing/next/evidence only. Requirements, delivery checks,
questions, production links, sources and every other asset row are left byte-equal.
"""
import hashlib
import json
import sys
from pathlib import Path

out = Path(sys.argv[1])
doc = json.loads(Path("plar.txt").read_text(encoding="utf-8"))
before = json.dumps(doc, sort_keys=True)
row = next(a for a in doc["assets"] if a["id"] == "queue.ready")
assert row["production"] == {"store": ".pixl/assets/queue.ready", "task": "r.028f320bf7292612.task",
                             "output": "r.028f320bf7292612.output.ready"}
assert row["delivery"]["path"] == "assets/ready-confirmed.png"


def sha(rel):
    return hashlib.sha256(Path(rel).read_bytes()).hexdigest()


CAND = sha("assets/ready-confirmed.png")
assert CAND == "fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5"
STATE = ".pixl/assets/queue.ready/state.px"
assert sha(STATE) == "fc5455196672aca53193d60b302a599afb49af2aab5b7fdd6a3f57a1ab3e935d"
R3 = "work/queue.ready/rev3"
CL = "work/queue.ready/caller"
PKT = ".pixl/assets/queue.ready/inspections/463ed8e2d432f53c1fdb64722de69fdd819b9d0868153e351ba07b67dec10dc9/manifest.json"
REV = ".pixl/assets/queue.ready/inspections/63af65128d02dfb9cccbf1b33a93a1cde03170b764ecca4bc039385fb51eeb30/manifest.json"

row["status"] = "integrated"
row["existing"] = [{
    "path": "assets/ready-confirmed.png",
    "role": (
        f"Delivered reviewed Ready candidate r.028f320bf7292612.candidate.ready (sha256 {CAND}, 16x16 RGBA, "
        "1 frame), byte-identical to the retained PX2 artifact and to the download of controlled-create-0002 from the "
        "controlled pixellab-test connection (evaluator fixture, provider_simulated=true, not PixelLab-generated art). "
        "Consumer-module check passed; renderer exercise, style decision and family comparison remain open."
    ),
}]
row["next"] = (
    "Delivered: r.028f320bf7292612.task is done (store revision 17, hash fc545519...), candidate "
    "r.028f320bf7292612.candidate.ready passed all eight rev3 criteria (review r.028f320bf7292612.review1) and its "
    "exact bytes are at assets/ready-confirmed.png; node verify-integration.mjs confirmed statusCell and compactStatus "
    "resolve succeeded -> Ready -> this path with frames 1 and a 16x16 PNG header. The image is an evaluator fixture "
    "from the controlled pixellab-test connection (controlled-create-0002), not upstream PixelLab art. Remaining: "
    "(1) record the Ready representative-sample style decision and source-bind the approved reference before "
    "expanding queue.working, queue.retry and queue.paused; (2) exercise statusCell/compactStatus in an actual "
    "renderer when one exists (none supplied; unverified); (3) run the family distinction reviews (Working not "
    "success; Retry and Paused distinguishable without colour) once those assets exist. Do not reuse "
    "controlled-create-0002 on a real PixelLab service; any further Ready generation needs a new, separately "
    "authorized request. Earlier tasks 'task' and r.f9e2fa53f4fcac2a.task remain open history with plar_selection "
    "blockers."
)
row["evidence"].extend([
    {"path": f"{R3}/provider-observation-succeeded.json",
     "note": (f"Caller observation on the originating controlled pixellab-test connection: list_jobs still queued, then "
              f"get_image controlled-create-0002 completed with one 16x16 PNG (declared sha256 {CAND}); downloaded from "
              f"the returned loopback URL; provider_simulated=true. sha256 {sha(f'{R3}/provider-observation-succeeded.json')}.")},
    {"path": f"{R3}/download/controlled-create-0002.png",
     "note": (f"Unmodified downloaded original (sha256 {CAND}); PNG tEXt purpose 'Controlled retrieval fixture, not "
              "PixelLab-generated art'. Recorded as job r.028f320bf7292612.request succeeded (state revision 12) and imported "
              "as candidate r.028f320bf7292612.candidate.ready (revision 13).")},
    {"path": PKT,
     "note": ("Inspection packet r.028f320bf7292612.inspect1: references [], scale 3, backgrounds #172336 and checkerboard; "
              "5 retained views (1x transparent, 1x/3x on #172336, 1x/3x checkerboard); mechanical measurements 16x16, 1 frame, "
              "29 visible px, 1 colour, 0 fractional alpha, 1 component. State revision 14.")},
    {"path": REV,
     "note": ("Specialist review r.028f320bf7292612.review1 (reviewer actor): all 5 views observed at payload size, "
              "8/8 criteria pass with reasons; limitations retained (fixture provenance, no renderer, family/style deferred). "
              "State revision 15; task completed at revisions 16-17.")},
    {"path": f"{R3}/specialist-result.json",
     "note": f"PIXL specialist result for import/inspection/review/completion (status delivered for that bounded scope). sha256 {sha(f'{R3}/specialist-result.json')}."},
    {"path": f"{CL}/independent-inspection.json",
     "note": f"Caller's independent pixel dump, derived 1x/3x/12x and grayscale views and per-criterion observations, made before reading the specialist review; consistent with all eight passes. sha256 {sha(f'{CL}/independent-inspection.json')}."},
    {"path": f"{CL}/integration-check-output.json",
     "note": (f"node verify-integration.mjs assets/ready-confirmed.png output (exit 0): statusCell and compactStatus both map "
              f"succeeded -> Ready -> assets/ready-confirmed.png frames 1; PNG header 16x16 equals display.cell; filter nearest; "
              f"file sha256 {CAND}. Module-level consumer check only, no renderer. sha256 {sha(f'{CL}/integration-check-output.json')}.")},
    {"path": STATE,
     "note": ("PX2 store after delivery stage: revision 17, hash fc5455196672aca53193d60b302a599afb49af2aab5b7fdd6a3f57a1ab3e935d; "
              "task r.028f320bf7292612.task done with nominated candidate r.028f320bf7292612.candidate.ready; job succeeded/imported; "
              "earlier tasks and jobs retained.")},
])
after = json.loads(json.dumps(doc))
# Guard: only the queue.ready row changed, and only the allowed fields.
b = json.loads(before)
for a_old, a_new in zip(b["assets"], after["assets"]):
    if a_old["id"] != "queue.ready":
        assert a_old == a_new, a_old["id"]
    else:
        for k in a_old:
            if k not in ("status", "existing", "next", "evidence"):
                assert a_old[k] == a_new[k], k
for k in b:
    if k != "assets":
        assert b[k] == after[k], k
out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out, hashlib.sha256(out.read_bytes()).hexdigest())
