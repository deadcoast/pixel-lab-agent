"""Derive the renderer-recheck PLAR proposal (pixl_plar_save input + change ledger) from the live plar.txt WITHOUT saving it,
then probe requirements_hash per asset in scratch copies with the kit CLI. Usage: python propose.py ROOT [--no-adopt]"""
import copy
import json
import re
import shutil
import subprocess
import sys
from hashlib import sha256
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
ADOPT = "--no-adopt" not in sys.argv
PY = sys.executable
KIT = ROOT / ".agents/skills/pixl-kit/scripts/pixl.py"
OUT = ROOT / "work/render-recheck-pixl"
digest = lambda p: sha256(Path(p).read_bytes()).hexdigest()
current_bytes = (ROOT / "plar.txt").read_bytes()
doc = json.loads(current_bytes)
base = copy.deepcopy(doc)
ledger = []
HASH_COVERED_ROOTS = ("requirements", "existing", "delivery", "depends_on", "consumers", "kind", "purpose", "references", "sources", "project")


def change(entry_id, where, field, old, new, why, conditional=None, optional=None, at_save_time=None):
    root = re.split(r"[.\[]", field)[0]
    ledger.append({"id": entry_id, "where": where, "field": field, "old": old, "new": new, "why": why,
                   "hash_covered": root in HASH_COVERED_ROOTS and not field.startswith("coverage"),
                   "conditional_on_style_adoption": bool(conditional), "if_not_adopted": conditional, "optional": optional,
                   **({"at_save_time": at_save_time} if at_save_time else {})})


READY_SHA = digest(ROOT / "assets/ready-confirmed.png")
VIEW_SHA = digest(ROOT / "renderer-recheck/view.mjs")
RENDER_STAGE_SHA = digest(ROOT / "RENDER-STAGE.md")
RENDER_RECHECK_SHA = digest(ROOT / "RENDER-RECHECK.md")
CAPTURE = "work/render-recheck-pixl-01"
RENDER_JSON_SHA = digest(ROOT / CAPTURE / "render.json")
SHOT_SHA = digest(ROOT / CAPTURE / "destination.png")
CHECK_SHA = digest(OUT / "check-render-recheck-pixl-01.json")
MEAS_SHA = digest(OUT / "measurements.json")
REVIEW = "work/render-stage-pixl/render-review.json"
REVIEW_SHA = digest(ROOT / REVIEW)
RECHECK_REVIEW = "work/render-recheck-pixl/render-recheck-review.json"
RECHECK_REVIEW_SHA = digest(ROOT / RECHECK_REVIEW)
OLD_CAPTURE = "work/render-pixl-01"
OLD_RENDER_SHA = digest(ROOT / OLD_CAPTURE / "render.json")
OLD_CHECK = "work/render-stage-pixl/check-render-pixl-01.json"
OLD_CHECK_SHA = digest(ROOT / OLD_CHECK)
OLD_MEAS = "work/render-stage-pixl/measurements.json"
OLD_MEAS_SHA = digest(ROOT / OLD_MEAS)
OFFSET = "work/render-stage-review/screenshot-offset-search.json"
OFFSET_SHA = digest(ROOT / OFFSET)
CALLER_CAPTURE = "work/render-recheck-caller-01"
CALLER_SHOT_SHA = digest(ROOT / CALLER_CAPTURE / "destination.png")
for p in (REVIEW, RECHECK_REVIEW, OLD_CHECK, OLD_MEAS, OFFSET, f"{CAPTURE}/render.json", f"{CAPTURE}/destination.png", f"{OLD_CAPTURE}/render.json", f"{CALLER_CAPTURE}/render.json", "work/queue.ready-reassessment/request-review.json"):
    assert (ROOT / p).exists(), p

# ---- sources
new_sources = [
    {"id": "ready-sample", "path": "assets/ready-confirmed.png", "sha256": READY_SHA},
    {"id": "renderer-view", "path": "renderer-recheck/view.mjs", "sha256": VIEW_SHA},
    {"id": "render-stage", "path": "RENDER-STAGE.md", "sha256": RENDER_STAGE_SHA},
    {"id": "render-recheck", "path": "RENDER-RECHECK.md", "sha256": RENDER_RECHECK_SHA},
]
doc["sources"].extend(new_sources)
change("U01", "sources", "sources", None, new_sources,
       "Bind the exact delivered sample bytes (fc5e43ae...) so a style baseline can be cited by source ID; bind the renderer view module actually executed by the corrected capture (renderer-recheck/view.mjs, byte-identical to renderer/view.mjs 5f64fc51...); bind RENDER-STAGE.md (authority delegating the scoped style decision to the caller) and RENDER-RECHECK.md (authority for this renderer-repair continuation).")

# ---- coverage
old_unresolved = list(doc["coverage"]["unresolved"])
doc["coverage"]["included"].append(
    "Render stage and renderer recheck: ran renderer/capture.mjs (historical) and the separately versioned renderer-recheck/capture.mjs (HeadlessChrome 156, DPR 1, 1280x1000 device metrics set via CDP before navigation) against the actual src/queue.ts and src/queue-view.ts for every statusVisuals state in both statusCell and compactStatus at 1x and 3x; checked identities, screenshot/canvas correspondence, alpha compositing and nearest blocks with check.py (historical 95/104 explained; recheck 104/104); inspected the retained PNGs and derived crops visually; the caller ran an independent recheck capture with byte-identical output.")
doc["coverage"]["unresolved"] = [
    "The representative renderer (renderer/, and the separately versioned renderer-recheck/ whose capture.mjs sets device metrics before navigation) is a scoped headless-Chrome fixture importing the real view modules; it is not the production UI. The original renderer/capture.mjs measured DOM bounds at a 1262x904 viewport while Chromium screenshotted at 1280x1000, so renderer/check.py failed 9 of 104 checks (dx=+9 bookkeeping offset, no rendering defect); renderer-recheck/check.py passes 104/104 on pixel-identical canvases. Production-host display acceptance (other browsers, DPR, zoom, the real shell) remains unverified.",
    "Style baseline: the delivered Ready fixture is a controlled pixellab-test sample (provider_simulated=true). Adopting it as the family style reference establishes edge treatment, stroke weight, fill/colour role, margin/footprint and alpha policy only; it does not establish the other members' silhouettes, motion or meaning, non-colour distinction, family continuity, nor actual PixelLab output quality.",
    "The account badge registry is populated remotely and is not enumerable from this checkout; badges remain excluded.",
    "Working, Retry and Paused have no artwork, no production store, no candidate and no review; the renderer shows 'Missing asset' for them. Timed loop playback at 100 ms can only be observed interactively (node renderer-recheck/server.mjs) because the capture samples frame boundaries, not real-time playback. No PX2 family plan exists yet.",
]
change("U02", "coverage", "coverage.included", None, doc["coverage"]["included"][-1], "Record the render-stage and recheck scan boundary.")
change("U03", "coverage", "coverage.unresolved", old_unresolved, doc["coverage"]["unresolved"],
       "The first and fourth unresolved items ('no executable UI entry point', 'SVG inspected as source only') are no longer true after the browser captures; replaced by the renderer's actual limits including the historical offset and the corrected recheck. The style-reference item is restated to name what adoption does and does not establish.")

assets = {a["id"]: a for a in doc["assets"]}
ready, working, retry, paused, start = (assets["queue.ready"], assets["queue.working"], assets["queue.retry"], assets["queue.paused"], assets["queue.start"])
assert [a["id"] for a in base["assets"]] == ["queue.ready", "queue.working", "queue.retry", "queue.start", "queue.paused"]

# ---- queue.ready: stale hash-covered text (deliberate requirements revision)
old_role = ready["existing"][0]["role"]
ready["existing"][0]["role"] = f"Delivered Ready sample (candidate ready.retained, sha256 {READY_SHA}, 16x16, one frame) from controlled pixellab-test job controlled-create-0002; assets/ready.png is superseded. Rendered by both consumers for ok -> succeeded in the representative renderer (renderer-recheck/, capture {CAPTURE}, 104/104 checks). Earlier attempts remain retained."
change("U04", "queue.ready", "existing[0].role", old_role, ready["existing"][0]["role"], "Stale: the destination is no longer missing (HANDOFF-RESULT.json deliberately_not_edited; reassessment ledger C17). Refreshed now as a deliberate requirements revision; this flips the done task's selection binding to 'changed' (diagnostic to preserve).")
old_check5 = ready["delivery"]["checks"][4]
ready["delivery"]["checks"][4] = "Record visual review and consumer integration evidence separately from mechanical checks. Status: six historical verdicts pass (ready.delivery.review); specialist art assessment, render-stage review (work/render-stage-pixl/render-review.json) and renderer-recheck review (work/render-recheck-pixl/render-recheck-review.json) retained; mechanical/visual/integration evidence are linked separately in this row's evidence."
change("U05", "queue.ready", "delivery.checks[4]", old_check5, ready["delivery"]["checks"][4], "Stale clause 'no delivered art has yet been reviewed' contradicted by the retained verdicts and reviews.")
old_check4 = ready["delivery"]["checks"][3]
ready["delivery"]["checks"][3] = f"Exercise both statusCell and compactStatus in an actual renderer and confirm the intended label and asset appear for the relevant queue transition. Status: observed in the representative renderer for ok -> succeeded (label Ready, assets/ready-confirmed.png, both consumers, 1x and 3x; {CAPTURE}/render.json; renderer-recheck/check.py 104/104 including screenshot/canvas correspondence). Production-host display remains unverified."
change("U06", "queue.ready", "delivery.checks[3]", old_check4, ready["delivery"]["checks"][3], "Record that the representative renderer exercised this check with the corrected capture; keep the production-host boundary explicit.")

if ADOPT:
    for req in ready["requirements"]:
        if req["property"] == "approved_style_reference":
            old_req = copy.deepcopy(req)
            req["value"] = {"path": "assets/ready-confirmed.png", "sha256": READY_SHA, "candidate": "ready.retained", "store": ".pixl/assets/queue.ready", "task": "r.22e90a2a03fe453a.task",
                            "scope": "Family style baseline for Working, Retry and Paused: flat single cool-blue fill (#70b9ed as rendered, equal to the Start fill), hard pixel edges with no anti-aliasing or outline, about 2 px perpendicular stroke (3-pixel runs on 45-degree diagonals; 2-pixel orthogonal strokes), no backing plate, transparent exterior with binary alpha in practice, footprint about 9-12 px inside a centred 12x12 safe area of the 16x16 cell (sample 11x9), visual mass comparable to the sample's 29 pixels. It does not prescribe the other members' silhouettes, motion, meaning or non-colour distinction and is not evidence of PixelLab-generated quality (provider_simulated=true)."}
            req["authority"] = "requirement"
            req["sources"] = ["render-stage", "ready-sample", "brief"]
            req["reason"] = "RENDER-STAGE.md lines 4-6 authorize the caller's scoped style decision for this representative consumer; this value records the caller's adoption of the exact delivered sample bytes as the approved reference that BRIEF.md line 5 said did not yet exist, following the specialist recommendation in work/render-stage-pixl/render-review.json and the caller's independent comparison. Adoption scope and limits are stated in the value."
            change("A01", "queue.ready", "requirements[approved_style_reference]", old_req, copy.deepcopy(req),
                   "Source-bind the approved baseline by exact identity if the caller adopts the sample.",
                   conditional="Keep authority 'unknown' and value null; append the caller's decision artifact to evidence; the dependent rows keep 'After the Ready sample is reviewed and bound as a style reference' in next.",
                   at_save_time="Append the caller's decision artifact {path, note} to queue.ready evidence (hash-safe) so the 'requirement' authority has an addressable owner decision.")
            break
ready["requirements"].append({
    "property": "renderer_display_observation",
    "value": {"renderer": "renderer-recheck/ (Chrome/156.0.8078.80 headless, devicePixelRatio 1, 1280x1000 device metrics set via CDP before navigation); renderer/ historical capture pixel-identical with a +9 px bounds bookkeeping offset",
              "consumers": ["statusCell", "compactStatus"], "scales": [1, 3],
              "observed": "ok -> succeeded -> label Ready with assets/ready-confirmed.png in both consumers; canvases are exact straight-alpha composites on #172336 with nearest 3x3 blocks (zero difference from an independent Pillow composite) and match the screenshot at their reported integer bounds (dx=0); canvases sit vertically centred on the row axis with a 12 px (full) / 6 px (compact) CSS gap to the label (first 'Ready' ink at 13/7 px); the SVG Start control is browser-rasterised with anti-aliasing (9 tones, 28 intermediate pixels at 1x, 84 at 3x) beside the hard-edged Ready mark."},
    "authority": "observation",
    "sources": ["renderer-view", "render-recheck", "queue-view", "queue-state"],
    "reason": f"Measured in {CAPTURE} and work/render-recheck-pixl/measurements.json; this is the representative fixture's behaviour, not production-host acceptance.",
})
change("U07", "queue.ready", "requirements[renderer_display_observation]", None, ready["requirements"][-1], "Record the corrected renderer evidence as an observation on the delivered row.")
ready["questions"] = ["Caller style decision pending at proposal time: does the delivered Ready sample become the family style baseline (recommended by the specialist in work/render-stage-pixl/render-review.json; no revision required by the renderer recheck per work/render-recheck-pixl/render-recheck-review.json)?"] if not ADOPT else []
change("U08", "queue.ready", "questions", base["assets"][0]["questions"], ready["questions"],
       "Adopt variant: the single pending question is answered by the caller's decision, so the list is emptied. No-adopt variant: narrow the open question to the single pending decision." if ADOPT else "Narrow the open question to the single pending decision.")
ready["next"] = (f"render_recheck: corrected renderer-recheck capture {CAPTURE} (errors [], viewport 1280x1000 set via CDP before navigation, destination.png {SHOT_SHA[:8]}... byte-identical to the caller's {CALLER_CAPTURE}, eight views pixel-identical to the historical renderer/ captures) and renderer-recheck/check.py 104/104 retained; the historical renderer/ result (95/104, dx=+9 capture-layout offset, {OLD_CAPTURE}) stays as evidence. "
                 + ("Style decision saved in this row (approved_style_reference). " if ADOPT else "Style decision pending (approved_style_reference stays unknown). ")
                 + "Next: keep status in_progress until production-host display is verified or the owner labels integration; do not reopen the done sample task r.22e90a2a03fe453a.task; this requirements revision flips its selection binding to 'changed' (preserve the diagnostic, do not rebind old jobs or transfer verdicts); new Ready generation only under explicit new authorization against the corrected packet (work/queue.ready-reassessment/request-review.json).")
change("U09", "queue.ready", "next", base["assets"][0]["next"], ready["next"], "Replace the consumed reassessment continuation with the render-recheck continuation.")
ready["evidence"].extend([
    {"path": f"{CAPTURE}/render.json", "note": f"Specialist renderer-recheck browser capture (sha256 {RENDER_JSON_SHA}): Chrome/156.0.8078.80 headless, DPR 1, device metrics 1280x1000 set before navigation, capture_layout 1280x1000, errors [], missing working/paused/error-retry; eight available views; served/renderer file hashes bound. Not a visual verdict."},
    {"path": f"{CAPTURE}/destination.png", "note": f"Recheck screenshot 1280x1000 (sha256 {SHOT_SHA}); byte-identical to the caller's {CALLER_CAPTURE}/destination.png ({CALLER_SHOT_SHA[:8]}...); differs from the historical 1d13cde1... screenshot in 8 border pixels by at most 1 channel level."},
    {"path": "work/render-recheck-pixl/check-render-recheck-pixl-01.json", "note": f"renderer-recheck/check.py stdout (sha256 {CHECK_SHA}): status pass, 104 of 104 observations, failures []. Identities, screenshot/canvas correspondence, compositing, nearest blocks; not an artistic verdict."},
    {"path": "work/render-recheck-pixl/measurements.json", "note": f"Independent Pillow measurements of the recheck capture (sha256 {MEAS_SHA}): zero-difference canvas matches at dx=0, zero-difference composites, label gaps, Start SVG rasterisation 28/84 intermediate px, fixture geometry/contrast, old-vs-new screenshot diff (8 px, max 1)."},
    {"path": REVIEW, "note": f"Specialist render-stage review (sha256 {REVIEW_SHA}): per-view observations with hashes, cross-check of preserved drafts and caller notes (the '4 -> 12' edge-pixel claim is wrong; 28/84 is correct), style recommendation ADOPT with carried/not-established properties, owner requirements vs expert choices, family inventory. Recommendation only; the caller owns the decision."},
    {"path": RECHECK_REVIEW, "note": f"Specialist renderer-recheck review (sha256 {RECHECK_REVIEW_SHA}): checker outcome 104/104, what the new evidence resolves (delivery check 4, Start check 2, screenshot/viewport correspondence for the available members) and cannot resolve (absent members, Working playback, non-colour distinction, Paused, family continuity, production host, PixelLab quality); no scoped revision of the style recommendation required."},
    {"path": OLD_CHECK, "note": f"HISTORICAL renderer/check.py stdout on {OLD_CAPTURE} (sha256 {OLD_CHECK_SHA}): 95 of 104 pass; the 9 failures ('screenshot and observed viewport dimensions' + 8 'screenshot matches canvas pixels') are the dx=+9 capture-layout offset, see {OLD_MEAS} ({OLD_MEAS_SHA[:8]}...) and {OFFSET} ({OFFSET_SHA[:8]}...). Kept as evidence of the original trial; not relabelled."},
    {"path": f"{OLD_CAPTURE}/render.json", "note": f"HISTORICAL render-stage capture (sha256 {OLD_RENDER_SHA}): reported viewport 1262x904 vs 1280x1000 screenshot; eight views byte-identical to the recheck capture."},
])
change("U10", "queue.ready", "evidence", "(+0)", "(+8 render-stage/recheck links: recheck render.json, destination.png, 104/104 check, measurements, render-review, render-recheck-review, historical 95/104 check, historical render.json)", "Link the render-stage and recheck evidence (hash-safe field).")

# ---- dependent rows
REF = {"source": "ready-sample", "role": "style",
       "instructions": "Match the approved Ready sample's treatment: flat single #70b9ed fill, hard pixel edges without anti-aliasing or outline, about 2 px perpendicular strokes (3-pixel runs on 45-degree diagonals, 2-pixel orthogonals), no backing plate, transparent exterior with binary alpha in practice, footprint 9-12 px inside the centred 12x12 safe area of the 16x16 cell, visual mass comparable to the sample's 29 pixels. Do not copy its silhouette; this member's own shape, meaning, non-colour distinction and (for Working) motion are decided by its own requirements and review."}
for row, name in ((working, "queue.working"), (retry, "queue.retry"), (paused, "queue.paused")):
    if ADOPT:
        row["references"] = [copy.deepcopy(REF)]
        change(f"A02-{name}", name, "references", None, row["references"], "Source-bound style reference to the exact sample if adopted (format.md reference-role extension).",
               conditional="Omit the references field entirely.")
        old = next(r for r in row["requirements"] if r["property"] == "approved_style_reference")
        old_copy = copy.deepcopy(old)
        old["value"] = {"path": "assets/ready-confirmed.png", "sha256": READY_SHA, "establishes": ["stroke weight", "edge construction", "fill treatment", "colour role", "margin/footprint", "alpha policy"], "does_not_establish": ["this member's silhouette", "motion/timing legibility", "meaning", "non-colour distinction", "PixelLab-generated quality"]}
        old["authority"] = "requirement"
        old["sources"] = ["render-stage", "ready-sample", "brief"]
        old["reason"] = "Caller's scoped style decision under RENDER-STAGE.md lines 4-6 adopting the delivered sample as the family baseline; limits stated in the value."
        change(f"A03-{name}", name, "requirements[approved_style_reference]", old_copy, copy.deepcopy(old), "Mirror the adopted baseline on each dependent row.",
               conditional="Keep authority 'unknown' and value null.")
    row["evidence"].append({"path": f"{CAPTURE}/render.json", "note": "Renderer-recheck observation for this member's transition: descriptor resolved with label and path, asset 404 -> 'Missing asset' shown in both consumers at 1x and 3x; no view invented, no candidate exists."})

for r in working["requirements"]:
    if r["property"] == "renderer_frame_extraction":
        old_copy = copy.deepcopy(r)
        r["value"] = {"module": "renderer-recheck/view.mjs paint() (byte-identical to renderer/view.mjs)", "strip": "horizontal; frame i is source rect [i*16, 0, 16, 16]", "frame_index": "floor(max(elapsed,0) / 100) % 4", "geometry_gate": "drawn only when image width == 16*frames and height == 16; otherwise 'Wrong sheet size' is shown and the canvas stays panel-coloured", "sampling": "imageSmoothingEnabled=false, CSS image-rendering: pixelated, destination 16*scale square", "capture_timeline": "frame-boundary samples at 0, 99, 100, 199, 200, 299, 300, 399 and 400 ms (expected frames 0,0,1,1,2,2,3,3,0) as 1x statusCell canvases; real-time loop playback is only observable interactively"}
        r["authority"] = "observation"
        r["sources"] = ["renderer-view", "queue-view"]
        r["reason"] = "Observed in the representative renderer fixture; a production host may crop differently, so retain this as the fixture's behaviour."
        change("U11", "queue.working", "requirements[renderer_frame_extraction]", old_copy, copy.deepcopy(r), "The unknown is resolved for the representative renderer; anchor policy is now concrete (left-to-right 16 px frames, no padding).",
               optional="Hash-covered: changes queue.working's requirements_hash (no production link exists, so nothing breaks). Drop to keep the row's requirements identical; the observation then lives only in evidence/next.")
working["questions"] = ["Which activity motif and frame placement should be adopted under the Ready baseline (specialist proposal: rotating 3- or 4-segment arc, no frame containing a check-like diagonal pair, constant footprint box)?"]
change("U12", "queue.working", "questions", base["assets"][1]["questions"], working["questions"], "The renderer question is answered by renderer-recheck/view.mjs; the motif question remains.")
working["next"] = "After the style decision is saved: author/request the 64x16 four-frame strip for assets/working.png under the Ready baseline (pixl_plar_prepare against a fresh caller-compared request/criteria packet; explicit new provider authorization required), then run node renderer-recheck/capture.mjs --out work/NEW_DIR and renderer-recheck/check.py: expect nine timeline samples with frames 0,0,1,1,2,2,3,3,0, 'nearest pixel blocks' and compositing passes, no 'Wrong sheet size'; view every frame at 1x and 3x beside Ready and Start; inspect the 300->400 ms wrap interactively via node renderer-recheck/server.mjs."
change("U13", "queue.working", "next", base["assets"][1]["next"], working["next"], "Concrete next work tied to the corrected renderer's actual capabilities and PLAR delivery checks.")
retry["questions"] = ["Which Retry silhouette best distinguishes failure/retry from the Ready check and the planned Working arc without colour (specialist proposal: circular arrow with a clear gap and 2-pixel arrowhead)?"]
change("U14", "queue.retry", "questions", base["assets"][2]["questions"], retry["questions"], "Carry the open motif question with the specialist proposal named.")
retry["next"] = "After the style decision is saved: request the static 16x16 Retry icon for assets/error-retry.png under the Ready baseline (fresh packet, caller comparison, explicit authorization), then capture with renderer-recheck/: expect error -> failed -> label Retry with the new asset in both consumers at 1x and 3x; compare grayscale silhouettes against Start, Ready and every Working frame; keep the superseded assets/retry.png path unused."
change("U15", "queue.retry", "next", base["assets"][2]["next"], retry["next"], "Concrete renderer-tied next work.")
paused["questions"] = ["Does the proposed two-bar pause silhouette (2-pixel bars, 2-pixel gap, 8-9 px tall) remain distinct from the Ready check, Working arc and Retry arrow without colour?"]
change("U16", "queue.paused", "questions", base["assets"][4]["questions"], paused["questions"], "The renderer question is answered (renderer-recheck/ exercises pause -> paused); the silhouette question remains.")
paused["next"] = "After the style decision is saved: request the static 16x16 Paused icon for assets/paused.png under the Ready baseline (fresh packet, caller comparison, explicit authorization), then capture with renderer-recheck/: expect pause -> paused -> label Paused with the new asset in both consumers at 1x and 3x; compare at both scales and in grayscale with Ready, Retry and all Working frames."
change("U17", "queue.paused", "next", base["assets"][4]["next"], paused["next"], "Concrete renderer-tied next work.")

old_start_role = start["existing"][0]["role"]
start["existing"][0]["role"] = f"Existing vector Start control reused unchanged (sha256 ee2ba2fe...); observed rendered by both consumers for idle in the representative renderer ({CAPTURE}): browser-rasterised with anti-aliased edges at 1x (28 intermediate pixels) and smooth re-rasterisation at 3x (84)."
change("U18", "queue.start", "existing[0].role", old_start_role, start["existing"][0]["role"], "The 'inspected as SVG source, not rendered UI' clause is no longer true; the idle mapping was exercised in the renderer.",
       optional="OPTIONAL. Hash-covered: changes queue.start's requirements_hash (no production link exists, so nothing breaks). Drop this entry to keep queue.start's requirements_hash stable; the renderer observation then lives only in evidence/next.")
start["evidence"].append({"path": f"{CAPTURE}/render.json", "note": "idle -> Start with assets/start.svg (sha256 ee2ba2fe...) in both consumers at 1x and 3x; views view-000..003; renderer-recheck/check.py 104/104. Byte hash unchanged."})
start["next"] = "Preserve the existing vector file and idle mapping; delivery check 2 observed in the representative renderer (idle resolves to the preserved Start control in both consumers; renderer-recheck 104/104). No new Start asset is allocated."
change("U19", "queue.start", "next", base["assets"][3]["next"], start["next"], "Record that the runnable-UI check has been exercised.")

suffix = "" if ADOPT else "-no-adopt"
proposal = OUT / f"plar-update-proposal{suffix}.json"
proposal.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

# ---- requirements_hash probe in a scratch copy (never touches the live plar.txt)
probe = OUT / f"hash-probe{'-adopt' if ADOPT else '-no-adopt'}"
if probe.exists():
    shutil.rmtree(probe)
probe.mkdir(parents=True)
for rel in ("BRIEF.md", "SOURCE-MAP.md", "RENDER-STAGE.md", "RENDER-RECHECK.md", "src/queue.ts", "src/queue-view.ts", "assets/start.svg", "assets/ready-confirmed.png", "renderer-recheck/view.mjs"):
    (probe / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / rel, probe / rel)
shutil.copytree(ROOT / ".pixl/assets/queue.ready", probe / ".pixl/assets/queue.ready")
shutil.copy2(proposal, probe / "plar.txt")
ASSETS = ["queue.ready", "queue.working", "queue.retry", "queue.start", "queue.paused"]


def read_asset(root, asset):
    run = subprocess.run([PY, "-I", str(KIT), "plar", "read", "--root", str(root), "--asset", asset], capture_output=True, text=True, encoding="utf-8")
    if run.returncode != 0:
        return {"error": run.stderr[-800:], "returncode": run.returncode}
    j = json.loads(run.stdout)
    prod = j.get("production") or {}
    return {"requirements_hash": j.get("requirements_hash"), "file_hash": j.get("hash"), "link_status": prod.get("link_status"),
            "selection_bindings": [{"input": s.get("input"), "status": s.get("status"), "selected_for_asset": s.get("selected_for_asset"), "bound_requirements_hash": s.get("requirements_hash")} for s in prod.get("selection_bindings", [])],
            "task_state": prod.get("task_state"), "next_action": prod.get("next_action"), "sources_changed": [s["id"] for s in j.get("sources", []) if s.get("binding") not in (None, "current")]}


probe_results = {a: read_asset(probe, a) for a in ASSETS}
live_results = {a: read_asset(ROOT, a) for a in ASSETS}
for a in ASSETS:
    (probe / f"read-{a}.json").write_text(json.dumps(probe_results[a], indent=2) + "\n", encoding="utf-8")

ledger_doc = {
    "version": 2,
    "variant": "adopt (specialist recommendation; applies only if the caller adopts)" if ADOPT else "no-adopt (unconditional refreshes only)",
    "scope": "Proposed pixl_plar_save document for plar.txt; NOT saved. Entries prefixed U are unconditional refreshes; entries prefixed A apply only if the caller adopts the delivered Ready sample as the family style baseline, with the fallback given in if_not_adopted. Entries with 'optional' may be dropped by the caller. Supersedes the preserved drafts in work/render-stage-pixl/ (which cited the historical offset capture); those drafts are kept.",
    "base_plar_sha256": sha256(current_bytes).hexdigest(),
    "expect_for_save": sha256(current_bytes).hexdigest(),
    "proposal_path": f"work/render-recheck-pixl/plar-update-proposal{suffix}.json",
    "proposal_sha256": digest(proposal),
    "preserved_drafts_superseded": {"work/render-stage-pixl/plar-update-proposal.json": digest(ROOT / "work/render-stage-pixl/plar-update-proposal.json"), "work/render-stage-pixl/plar-update-proposal-no-adopt.json": digest(ROOT / "work/render-stage-pixl/plar-update-proposal-no-adopt.json"), "work/render-stage-pixl/plar-change-ledger.json": digest(ROOT / "work/render-stage-pixl/plar-change-ledger.json"), "work/render-stage-pixl/plar-change-ledger-no-adopt.json": digest(ROOT / "work/render-stage-pixl/plar-change-ledger-no-adopt.json")},
    "requirements_hash_by_asset": {a: {"live": live_results[a].get("requirements_hash"), "proposed": probe_results[a].get("requirements_hash"), "changed": live_results[a].get("requirements_hash") != probe_results[a].get("requirements_hash"),
                                       "live_selection_bindings": live_results[a].get("selection_bindings"), "proposed_selection_bindings": probe_results[a].get("selection_bindings"), "link_status": probe_results[a].get("link_status"), "error": probe_results[a].get("error")} for a in ASSETS},
    "production_selection_diagnostic": "queue.ready's done task r.22e90a2a03fe453a.task is bound to requirements_hash 806a1f2d...; after this save its selection binding reads 'changed'. Preserve and report it; do not rebind old jobs, reopen the done task or transfer the six historical verdicts to the new contract.",
    "probe_method": f"Scratch copy under {probe.relative_to(ROOT).as_posix()}/ (sources, assets, renderer-recheck/view.mjs, copy of .pixl/assets/queue.ready, proposal as plar.txt); kit CLI 'plar read --root PROBE --asset ID' with {PY}; live plar.txt untouched. Caller may delete the scratch directories.",
    "entries": ledger,
}
(OUT / f"plar-change-ledger{suffix}.json").write_text(json.dumps(ledger_doc, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"variant": ledger_doc["variant"], "proposal_sha256": ledger_doc["proposal_sha256"], "hashes": {a: (v["live"], v["proposed"], v["changed"], [s["status"] for s in (v["proposed_selection_bindings"] or [])], v["error"]) for a, v in ledger_doc["requirements_hash_by_asset"].items()}, "entries": [(e["id"], e["hash_covered"], e["conditional_on_style_adoption"], bool(e["optional"])) for e in ledger]}, indent=1))
