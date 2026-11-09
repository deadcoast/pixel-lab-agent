"""Derive the proposed PLAR document from the current plar.txt without saving it (pixl_plar_save input + change ledger)."""
import copy
import json
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "work/render-stage-pixl"
digest = lambda p: sha256(Path(p).read_bytes()).hexdigest()
current_bytes = (ROOT / "plar.txt").read_bytes()
doc = json.loads(current_bytes)
base = copy.deepcopy(doc)
ledger = []


import re

ADOPT = "--no-adopt" not in sys.argv
HASH_COVERED_ROOTS = ("requirements", "existing", "delivery", "depends_on", "consumers", "kind", "purpose", "references", "sources", "project")


def change(entry_id, where, field, old, new, why, conditional=None, optional=None):
    root = re.split(r"[.\[]", field)[0]
    ledger.append({"id": entry_id, "where": where, "field": field, "old": old, "new": new, "why": why,
                   "hash_covered": root in HASH_COVERED_ROOTS and not field.startswith("coverage"),
                   "conditional_on_style_adoption": bool(conditional), "if_not_adopted": conditional, "optional": optional})


READY_SHA = digest(ROOT / "assets/ready-confirmed.png")
VIEW_SHA = digest(ROOT / "renderer/view.mjs")
RENDER_STAGE_SHA = digest(ROOT / "RENDER-STAGE.md")
CAPTURE = "work/render-pixl-01"
RENDER_JSON_SHA = digest(ROOT / CAPTURE / "render.json")
SHOT_SHA = digest(ROOT / CAPTURE / "destination.png")
CHECK_SHA = digest(OUT / "check-render-pixl-01.json")
MEAS_SHA = digest(OUT / "measurements.json")
REVIEW_PATH = "work/render-stage-pixl/render-review.json"  # written after this script; hash recorded in the final result, not here

# ---- sources: bind the exact sample bytes, the representative renderer view module and the stage authority
new_sources = [
    {"id": "ready-sample", "path": "assets/ready-confirmed.png", "sha256": READY_SHA},
    {"id": "renderer-view", "path": "renderer/view.mjs", "sha256": VIEW_SHA},
    {"id": "render-stage", "path": "RENDER-STAGE.md", "sha256": RENDER_STAGE_SHA},
]
doc["sources"].extend(new_sources)
change("U01", "sources", "sources", None, new_sources,
       "Bind the exact delivered sample bytes (fc5e43ae...) so a style baseline can be cited by source ID; bind the representative browser renderer module whose crop/scale/compositing behaviour is now observed; bind RENDER-STAGE.md as the authority that delegates the scoped style decision to the caller.")

# ---- coverage
old_unresolved = list(doc["coverage"]["unresolved"])
doc["coverage"]["included"].append(
    "Render stage: ran renderer/capture.mjs (HeadlessChrome 156, DPR 1) against the actual src/queue.ts and src/queue-view.ts for every statusVisuals state in both statusCell and compactStatus at 1x and 3x; checked identities, canvas pixels, alpha compositing and nearest blocks with renderer/check.py; inspected the retained PNGs visually.")
doc["coverage"]["unresolved"] = [
    "The representative renderer in renderer/ is a scoped browser fixture that imports the real view modules; it is not the production UI, and its headless screenshot is laid out at the 1280 px window width while DOM bounds are measured at the 1262 px viewport, so renderer/check.py reports a 9 px horizontal offset (see queue.ready evidence). Production-host display acceptance remains unverified.",
    "Style baseline: the delivered Ready fixture is a controlled pixellab-test sample (provider_simulated=true). Adopting it as the family style reference establishes edge treatment, stroke weight, fill/colour role, margin and alpha policy only; it does not establish the other members' silhouettes, motion or meaning, nor actual PixelLab output quality.",
    "The account badge registry is populated remotely and is not enumerable from this checkout; badges remain excluded.",
    "Working, Retry and Paused have no artwork, no production store, no candidate and no review; timed loop playback at 100 ms can only be observed interactively (node renderer/server.mjs) because the capture samples frame boundaries, not real-time playback.",
]
change("U02", "coverage", "coverage.included", None, doc["coverage"]["included"][-1], "Record the render-stage scan boundary.")
change("U03", "coverage", "coverage.unresolved", old_unresolved, doc["coverage"]["unresolved"],
       "The first and fourth unresolved items ('no executable UI entry point', 'SVG inspected as source only') are no longer true after the browser capture; replaced by the renderer's actual limits. The style-reference item is restated to name what adoption does and does not establish.")

assets = {a["id"]: a for a in doc["assets"]}
ready, working, retry, paused, start = (assets["queue.ready"], assets["queue.working"], assets["queue.retry"], assets["queue.paused"], assets["queue.start"])
assert [a["id"] for a in base["assets"]] == ["queue.ready", "queue.working", "queue.retry", "queue.start", "queue.paused"]

# ---- queue.ready: stale hash-covered text (deliberate requirements revision)
old_role = ready["existing"][0]["role"]
ready["existing"][0]["role"] = "Delivered Ready sample (candidate ready.retained, sha256 fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5, 16x16, one frame) from controlled pixellab-test job controlled-create-0002; assets/ready.png is superseded. Rendered by both consumers for ok -> succeeded in renderer/ (work/render-pixl-01). Earlier attempts remain retained."
change("U04", "queue.ready", "existing[0].role", old_role, ready["existing"][0]["role"], "Stale: the destination is no longer missing (HANDOFF-RESULT.json deliberately_not_edited; ledger C17). Refreshed now as a deliberate requirements revision.")
old_check5 = ready["delivery"]["checks"][4]
ready["delivery"]["checks"][4] = "Record visual review and consumer integration evidence separately from mechanical checks. Status: six historical verdicts pass (ready.delivery.review), specialist art assessment and render-stage browser review retained; mechanical/visual/integration evidence are linked separately in this row's evidence."
change("U05", "queue.ready", "delivery.checks[4]", old_check5, ready["delivery"]["checks"][4], "Stale clause 'no delivered art has yet been reviewed' contradicted by the retained verdicts and reviews.")
old_check4 = ready["delivery"]["checks"][3]
ready["delivery"]["checks"][3] = "Exercise both statusCell and compactStatus in an actual renderer and confirm the intended label and asset appear for the relevant queue transition. Status: observed in renderer/ for ok -> succeeded (label Ready, assets/ready-confirmed.png, both consumers, 1x and 3x; work/render-pixl-01/render.json). Production-host display remains unverified."
change("U06", "queue.ready", "delivery.checks[3]", old_check4, ready["delivery"]["checks"][3], "Record that the representative renderer exercised this check; keep the production-host boundary explicit.")

# approved style reference (conditional on the caller's decision)
for req in ready["requirements"]:
    if req["property"] == "approved_style_reference" and ADOPT:
        old_req = copy.deepcopy(req)
        req["value"] = {"path": "assets/ready-confirmed.png", "sha256": READY_SHA, "candidate": "ready.retained", "store": ".pixl/assets/queue.ready", "task": "r.22e90a2a03fe453a.task",
                        "scope": "Family style baseline for Working, Retry and Paused: flat single cool-blue fill (#70b9ed as rendered), hard pixel edges with no anti-aliasing or outline, about 2 px perpendicular stroke (3-pixel runs on 45-degree diagonals; 2-pixel orthogonal strokes), no backing plate, transparent exterior, footprint about 11x9 within 2-3 px margins of the 16x16 cell. It does not prescribe the other members' silhouettes, motion or meaning and is not evidence of PixelLab-generated quality (provider_simulated=true)."}
        req["authority"] = "requirement"
        req["sources"] = ["render-stage", "ready-sample", "brief"]
        req["reason"] = "RENDER-STAGE.md lines 4-6 authorize the caller's scoped style decision for this representative consumer; this value records adoption of the exact delivered sample bytes as the approved reference the brief (line 5) said did not yet exist. Adoption scope and limits are stated in the value."
        change("A01", "queue.ready", "requirements[approved_style_reference]", old_req, copy.deepcopy(req),
               "Source-bind the approved baseline by exact identity if the caller adopts the sample.",
               conditional="Keep authority 'unknown' and value null; append the caller's decision artifact to evidence; the other rows keep 'After the Ready sample is reviewed and bound as a style reference' in next.")
        break
ready["requirements"].append({
    "property": "renderer_display_observation",
    "value": {"renderer": "renderer/ (HeadlessChrome 156, devicePixelRatio 1)", "consumers": ["statusCell", "compactStatus"], "scales": [1, 3],
              "observed": "ok -> succeeded -> label Ready with assets/ready-confirmed.png in both consumers; canvases are exact alpha composites on #172336 with nearest 3x3 blocks (zero difference from an independent Pillow composite); canvases sit vertically centred on the row axis with a 12 px (full) / 6 px (compact) CSS gap to the label; the SVG Start control is browser-rasterised with anti-aliasing (9 tones at 1x, smooth re-rasterisation at 3x) beside the hard-edged Ready mark."},
    "authority": "observation",
    "sources": ["renderer-view", "queue-view", "queue-state"],
    "reason": "Measured in work/render-pixl-01 and work/render-stage-pixl/measurements.json; this is the representative fixture's behaviour, not production-host acceptance.",
})
change("U07", "queue.ready", "requirements[renderer_display_observation]", None, ready["requirements"][-1], "Record the renderer evidence as an observation on the delivered row.")
ready["questions"] = ["Caller style decision pending at proposal time: does the delivered Ready sample become the family style baseline (recommended by the specialist in work/render-stage-pixl/render-review.json)?"]
change("U08", "queue.ready", "questions", base["assets"][0]["questions"], ready["questions"], "Narrow the open question to the single pending decision.")
ready["next"] = "render_stage: browser capture work/render-pixl-01 (errors [], destination.png 1d13cde1..., eight views pixel-identical to the caller's capture) and renderer/check.py (95/104 pass; the 9 failures are the screenshot-layout offset dx=9 explained in work/render-stage-pixl/render-review.json, not a consumer defect) retained. Next: after the caller's style decision is saved in this row, keep status in_progress until production-host display is verified or the owner labels integration; do not reopen the done sample task; new Ready generation only under explicit new authorization against the corrected packet (work/queue.ready-reassessment/request-review.json)."
change("U09", "queue.ready", "next", base["assets"][0]["next"], ready["next"], "Replace the consumed reassessment continuation with the render-stage continuation.")
ready["evidence"].extend([
    {"path": f"{CAPTURE}/render.json", "note": f"Specialist browser capture (sha256 {RENDER_JSON_SHA}): HeadlessChrome 156, DPR 1, errors [], missing working/paused/error-retry; eight available views; served/renderer file hashes bound. Not a visual verdict."},
    {"path": f"{CAPTURE}/destination.png", "note": f"Headless screenshot 1280x1000 (sha256 {SHOT_SHA}); byte-identical to work/render-caller-01/destination.png."},
    {"path": "work/render-stage-pixl/check-render-pixl-01.json", "note": f"renderer/check.py stdout (sha256 {CHECK_SHA}): status fail, 95 of 104 observations pass; failures are 'screenshot and observed viewport dimensions' and eight 'screenshot matches canvas pixels'. Diagnosed as a capture-layout offset (dx=+9, dy=0, exact match) not a rendering defect."},
    {"path": "work/render-stage-pixl/measurements.json", "note": f"Independent Pillow measurements (sha256 {MEAS_SHA}): exact-match offsets, zero-difference composites, label gaps, Start SVG rasterisation, fixture geometry/contrast."},
    {"path": REVIEW_PATH, "note": "Specialist render-stage review: per-view observations with hashes, checker diagnosis, prior-assessment fact verification, style recommendation with carried/not-established properties, family inventory. Recommendation only; the caller owns the style decision."},
])
change("U10", "queue.ready", "evidence", "(+0)", "(+5 render-stage links)", "Link the render-stage evidence (hash-safe field).")

# ---- dependent rows: references (conditional), renderer observation, questions, next
REF = {"source": "ready-sample", "role": "style",
       "instructions": "Match the approved Ready sample's treatment: flat single #70b9ed fill, hard pixel edges without anti-aliasing or outline, about 2 px perpendicular strokes (3-pixel runs on 45-degree diagonals, 2-pixel orthogonals), no backing plate, transparent exterior, footprint 9-12 px inside the centred 12x12 safe area of the 16x16 cell, visual mass comparable to the sample's 29 pixels. Do not copy its silhouette; this member's own shape, meaning and (for Working) motion are decided by its own requirements and review."}
for row, name in ((working, "queue.working"), (retry, "queue.retry"), (paused, "queue.paused")):
    if ADOPT:
        row["references"] = [copy.deepcopy(REF)]
        change(f"A02-{name}", name, "references", None, row["references"], "Source-bound style reference to the exact sample if adopted (format.md reference-role extension).",
               conditional="Omit the references field entirely.")
        old = next(r for r in row["requirements"] if r["property"] == "approved_style_reference")
        old_copy = copy.deepcopy(old)
        old["value"] = {"path": "assets/ready-confirmed.png", "sha256": READY_SHA, "establishes": ["stroke weight", "edge construction", "fill treatment", "colour role", "margin/footprint", "alpha policy"], "does_not_establish": ["this member's silhouette", "motion/timing legibility", "meaning", "PixelLab-generated quality"]}
        old["authority"] = "requirement"
        old["sources"] = ["render-stage", "ready-sample", "brief"]
        old["reason"] = "Caller's scoped style decision under RENDER-STAGE.md lines 4-6 adopting the delivered sample as the family baseline; limits stated in the value."
        change(f"A03-{name}", name, "requirements[approved_style_reference]", old_copy, copy.deepcopy(old), "Mirror the adopted baseline on each dependent row.",
               conditional="Keep authority 'unknown' and value null.")
    row["evidence"].append({"path": f"{CAPTURE}/render.json", "note": f"Renderer observation for this member's transition: descriptor resolved with label and path, asset 404 -> 'Missing asset' shown; no view invented, no candidate exists."})

# working: renderer frame extraction is now observed
for r in working["requirements"]:
    if r["property"] == "renderer_frame_extraction":
        old_copy = copy.deepcopy(r)
        r["value"] = {"module": "renderer/view.mjs paint()", "strip": "horizontal; frame i is source rect [i*16, 0, 16, 16]", "frame_index": "floor(max(elapsed,0) / 100) % 4", "geometry_gate": "drawn only when image width == 16*frames and height == 16; otherwise 'Wrong sheet size' is shown and the canvas stays panel-coloured", "sampling": "imageSmoothingEnabled=false, CSS image-rendering: pixelated, destination 16*scale square", "capture_timeline": "frame-boundary samples at 0, 99, 100, 199, 200, 299, 300, 399 and 400 ms (expected frames 0,0,1,1,2,2,3,3,0) as 1x statusCell canvases; real-time loop playback is only observable interactively"}
        r["authority"] = "observation"
        r["sources"] = ["renderer-view", "queue-view"]
        r["reason"] = "Observed in the representative renderer fixture; a production host may crop differently, so retain this as the fixture's behaviour."
        change("U11", "queue.working", "requirements[renderer_frame_extraction]", old_copy, copy.deepcopy(r), "The unknown is resolved for the representative renderer; anchor policy is now concrete (left-to-right 16 px frames, no padding).")
working["questions"] = ["Which activity motif and frame placement should be adopted under the Ready baseline (specialist proposal: rotating 3- or 4-segment arc, no frame containing a check-like diagonal pair, constant footprint box)?"]
change("U12", "queue.working", "questions", base["assets"][1]["questions"], working["questions"], "The renderer question is answered by renderer/view.mjs; the motif question remains.")
working["next"] = "After the style decision is saved: author/request the 64x16 four-frame strip for assets/working.png under the Ready baseline (pixl_plar_prepare against a fresh caller-compared request/criteria packet; explicit new provider authorization required), then run node renderer/capture.mjs --out work/NEW_DIR and renderer/check.py: expect nine timeline samples with frames 0,0,1,1,2,2,3,3,0, 'nearest pixel blocks' and compositing passes, no 'Wrong sheet size'; view every frame at 1x and 3x beside Ready and Start; inspect the 300->400 ms wrap interactively via node renderer/server.mjs."
change("U13", "queue.working", "next", base["assets"][1]["next"], working["next"], "Concrete next work tied to the renderer's actual capabilities and PLAR delivery checks.")
retry["questions"] = ["Which Retry silhouette best distinguishes failure/retry from the Ready check and the planned Working arc without colour (specialist proposal: circular arrow with a clear gap and 2-pixel arrowhead)?"]
change("U14", "queue.retry", "questions", base["assets"][2]["questions"], retry["questions"], "Carry the open motif question with the specialist proposal named.")
retry["next"] = "After the style decision is saved: request the static 16x16 Retry icon for assets/error-retry.png under the Ready baseline (fresh packet, caller comparison, explicit authorization), then capture in renderer/: expect error -> failed -> label Retry with the new asset in both consumers at 1x and 3x; compare grayscale silhouettes against Start, Ready and every Working frame; keep the superseded assets/retry.png path unused."
change("U15", "queue.retry", "next", base["assets"][2]["next"], retry["next"], "Concrete renderer-tied next work.")
paused["questions"] = ["Does the proposed two-bar pause silhouette (2-pixel bars, 2-pixel gap, 8-9 px tall) remain distinct from the Ready check, Working arc and Retry arrow without colour?"]
change("U16", "queue.paused", "questions", base["assets"][4]["questions"], paused["questions"], "The renderer question is answered (renderer/ exercises pause -> paused); the silhouette question remains.")
paused["next"] = "After the style decision is saved: request the static 16x16 Paused icon for assets/paused.png under the Ready baseline (fresh packet, caller comparison, explicit authorization), then capture in renderer/: expect pause -> paused -> label Paused with the new asset in both consumers at 1x and 3x; compare at both scales and in grayscale with Ready, Retry and all Working frames."
change("U17", "queue.paused", "next", base["assets"][4]["next"], paused["next"], "Concrete renderer-tied next work.")
old_start_role = start["existing"][0]["role"]
start["existing"][0]["role"] = "Existing vector Start control reused unchanged (sha256 ee2ba2fe...); observed rendered by both consumers for idle in renderer/ (work/render-pixl-01): browser-rasterised with anti-aliased edges at 1x and smooth re-rasterisation at 3x."
change("U18", "queue.start", "existing[0].role", old_start_role, start["existing"][0]["role"], "The 'inspected as SVG source, not rendered UI' clause is no longer true; the idle mapping was exercised in the renderer.",
       optional="Hash-covered: changes queue.start's requirements_hash (no production link exists, so nothing breaks). Drop this entry to keep queue.start's hash d25bb898... stable; the renderer observation then lives only in evidence/next.")
start["evidence"].append({"path": f"{CAPTURE}/render.json", "note": "idle -> Start with assets/start.svg (sha256 ee2ba2fe...) in both consumers at 1x and 3x; views view-000..003. Byte hash unchanged."})
start["next"] = "Preserve the existing vector file and idle mapping; delivery check 2 observed in the representative renderer (idle resolves to the preserved Start control in both consumers). No new Start asset is allocated."
change("U19", "queue.start", "next", base["assets"][3]["next"], start["next"], "Record that the runnable-UI check has been exercised.")

suffix = "" if ADOPT else "-no-adopt"
proposal = OUT / f"plar-update-proposal{suffix}.json"
proposal.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
ledger_doc = {
    "version": 1,
    "variant": "adopt (specialist recommendation)" if ADOPT else "no-adopt (unconditional refreshes only)",
    "scope": "Proposed pixl_plar_save document for plar.txt; NOT saved. Entries prefixed U are unconditional refreshes; entries prefixed A apply only if the caller adopts the delivered Ready sample as the family style baseline, with the fallback given in if_not_adopted. Entries with 'optional' may be dropped by the caller.",
    "base_plar_sha256": sha256(current_bytes).hexdigest(),
    "proposal_path": "work/render-stage-pixl/plar-update-proposal.json",
    "proposal_sha256": digest(proposal),
    "expect_for_save": sha256(current_bytes).hexdigest(),
    "entries": ledger,
}
(OUT / f"plar-change-ledger{suffix}.json").write_text(json.dumps(ledger_doc, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"proposal_sha256": ledger_doc["proposal_sha256"], "entries": [(e["id"], e["hash_covered"], e["conditional_on_style_adoption"]) for e in ledger]}))
