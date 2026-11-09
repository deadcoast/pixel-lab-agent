"""Build specialist-proposal.json and specialist-report.json for FOCUSED-SUCCESSOR.md step 2 (PIXL specialist, foreground).

Every cited (source, lines) pair is verified by opening the file and checking that the inclusive one-based range
contains the expected wording; the build fails on any miss. Hashes are computed from the actual bytes at build time.
Run: python -I specialist-build-proposal.py --root PROJECT_ROOT
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
ROOT = Path(parser.parse_args().root).resolve()
OUT = ROOT / "work/focused-successor"
VIEWS = OUT / "specialist-views"


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def lines_of(rel):
    return (ROOT / rel).read_text(encoding="utf-8").splitlines()


# ---------------------------------------------------------------- shared source index (ONE index; clauses reference ids)
SOURCE_DEFS = {
    "brief": ("BRIEF.md", "owner brief"),
    "update": ("AUTHORING-UPDATE.md", "caller reduced-motion update (authoring branch)"),
    "plar": ("authoring-plar.txt", "current authoring PLAR; queue.working row lines 420-675"),
    "assignment": ("FOCUSED-SUCCESSOR.md", "current assignment (step 2 delegated to PIXL; step 3 constraints; step 4 destination)"),
    "queue-ts": ("src/queue.ts", "backend state machine (shared by both consumers)"),
    "view-ts": ("src/queue-view.ts", "original consumer module, retained unchanged (historical destination)"),
    "successor-ts": ("src/queue-view-successor.ts", "caller-proposed successor consumer module (revisable design proposal)"),
    "succ-view": ("renderer-successor/view.mjs", "successor browser fixture executing the actual successor modules; evidence route"),
    "succ-check": ("renderer-successor/check.py", "successor mechanical checker"),
    "succ-index": ("renderer-successor/index.html", "successor fixture page"),
    "succ-capture": ("renderer-successor/capture.mjs", "successor capture driver (preference emulation phases)"),
    "old-view": ("renderer/view.mjs", "original fixture, retained unchanged"),
    "working-png": ("assets/working.png", "existing PixelLab-produced Working sheet 64x16 (byte-identical to accepted live.working-animation-motion-01.candidate)"),
    "ready-png": ("assets/ready-confirmed.png", "exact Ready style baseline ready.retained"),
    "paused-png": ("assets/paused.png", "delivered Paused member"),
    "retry-png": ("assets/error-retry.png", "delivered Retry member"),
    "start-svg": ("assets/start.svg", "preserved vector Start control"),
    "seed-png": (".pixl/assets/queue.ready/artifacts/21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png", "accepted Working seed live.working-seed.candidate"),
    "state": (".pixl/assets/queue.ready/state.px", "PX2 store revision 88 (read only)"),
    "context": ("work/focused-successor/context-authoring-raw.json", "focused authoring context (exact bytes): 20 criteria ids + record_sha256 + ck, 29 sources, contracts, choices, decisions, job, selection"),
    "r2": ("work/criteria-review-01/specialist-proposal-r2.json", "prior corrected proposal r2 (carried; not re-litigated)"),
    "caller-cmp": ("work/export-review-01/caller-comparison.json", "caller comparison: D1-D4 resolutions and keep/clarify/correct dispositions"),
    "discovery": ("official-discovery.json", "retained official PixelLab tool declarations observed by the host"),
    "views-color-1x": ("work/focused-successor/specialist-views/specialist-family-color-1x.png", "specialist view: W0..W3, Ready, Paused, Retry, rasterized Start on #172336 at 1x colour"),
    "views-gray-1x": ("work/focused-successor/specialist-views/specialist-family-gray-1x.png", "specialist view: same at 1x grayscale"),
    "views-color-3x": ("work/focused-successor/specialist-views/specialist-family-color-3x.png", "specialist view: same at 3x colour"),
    "views-gray-3x": ("work/focused-successor/specialist-views/specialist-family-gray-3x.png", "specialist view: same at 3x grayscale"),
    "views-color-12x": ("work/focused-successor/specialist-views/specialist-family-color-12x.png", "specialist view: same at 12x colour (inspection scale)"),
    "views-gray-12x": ("work/focused-successor/specialist-views/specialist-family-gray-12x.png", "specialist view: same at 12x grayscale"),
    "views-pair": ("work/focused-successor/specialist-views/specialist-pair-w0-retry-ready-paused.png", "specialist view: held cell 0 beside Retry, Ready, Paused at 1x/3x/12x colour+gray"),
    "views-grid": ("work/focused-successor/specialist-views/specialist-working-cell0-grid-20x.png", "specialist view: cell 0 on a 20x pixel grid"),
    "views-start": ("work/focused-successor/specialist-views/specialist-start-raster-16.png", "specialist rasterization of assets/start.svg (16x supersample, box downsample) used only for side-by-side comparison"),
    "measurements": ("work/focused-successor/specialist-views/specialist-measurements.json", "reproducible component/centroid/alpha measurements (zero-based, half-open boxes)"),
}
SOURCES = {sid: {"path": p, "sha256": sha(p), "role": r} for sid, (p, r) in SOURCE_DEFS.items()}

# ---------------------------------------------------------------- citations: (source id, [first,last], expected substring)
CITES = {
    "brief-working": ("brief", [3, 3], "Working uses four horizontal frames with a 100 ms frame duration"),
    "brief-transparent": ("brief", [3, 3], "Use transparent backgrounds, readable silhouettes"),
    "brief-inspect": ("brief", [3, 3], "Inspect at 1x and 3x nearest display scale on the actual dark panel"),
    "brief-activity": ("brief", [3, 3], "The working loop must communicate activity without looking like success"),
    "brief-retry": ("brief", [3, 3], "Error/retry must be distinguishable without color alone"),
    "brief-static": ("brief", [3, 3], "Ready and Retry are static images"),
    "brief-start": ("brief", [3, 3], "Preserve the existing vector Start control"),
    "brief-paths": ("brief", [5, 5], "Assets belong at the paths already used by the view"),
    "brief-paused": ("brief", [7, 7], "distinguishable from activity, completion and retry without relying on color alone"),
    "brief-keep": ("brief", [7, 7], "Keep the existing style and display requirements"),
    "brief-ready": ("brief", [9, 9], "check mark with asymmetrical arms"),
    "update-req": ("update", [2, 4], "stationary Working"),
    "update-retain": ("update", [5, 10], "no additional generation is requested"),
    "plar-row": ("plar", [420, 423], '"id": "queue.working"'),
    "plar-purpose": ("plar", [422, 422], "stationary Working symbol distinguishable from Ready and Paused"),
    "plar-purpose-nosuccess": ("plar", [422, 422], "without implying success"),
    "plar-geometry": ("plar", [529, 545], '"frames": 4'),
    "plar-animation": ("plar", [546, 559], '"frame_duration_ms": 100'),
    "plar-meaning": ("plar", [560, 570], "avoiding completion/success silhouettes"),
    "plar-style": ("plar", [512, 528], "approved_style_reference"),
    "plar-delivery": ("plar", [606, 619], "Play the loop at 100 ms per frame"),
    "plar-production": ("plar", [670, 674], "authoring-01.working.task"),
    "assign-step2": ("assignment", [18, 23], "holding frame zero of the"),
    "assign-step3": ("assignment", [24, 31], "Add explicit reduced-motion mapping and live preference-switch acceptance"),
    "assign-step4": ("assignment", [32, 43], "implement the successor"),
    "assign-step4-reuse": ("assignment", [40, 43], "Reuse reviewed existing art when it satisfies the new criteria"),
    "assign-step6": ("assignment", [52, 58], "switching the preference in the same session"),
    "queue-state": ("queue-ts", [1, 3], "stateAfter"),
    "view-idle": ("view-ts", [3, 3], 'idle: { label: "Start", path: "assets/start.svg"'),
    "view-running": ("view-ts", [4, 4], 'running: { label: "Working", path: "assets/working.png", frames: 4 }'),
    "view-paths": ("view-ts", [3, 7], "assets/error-retry.png"),
    "view-display": ("view-ts", [9, 9], 'frameMs: 100, background: "#172336"'),
    "view-consumers": ("view-ts", [10, 11], "export function compactStatus"),
    "succ-header": ("successor-ts", [1, 2], "queue-view.ts is retained unchanged"),
    "succ-pref": ("successor-ts", [4, 5], "(prefers-reduced-motion: reduce)"),
    "succ-idle": ("successor-ts", [7, 7], 'idle: { label: "Start", path: "assets/start.svg", frames: 1, still: 0 }'),
    "succ-running": ("successor-ts", [8, 8], 'running: { label: "Working", path: "assets/working.png", frames: 4, still: 0 }'),
    "succ-paths": ("successor-ts", [6, 12], "assets/paused.png"),
    "succ-display": ("successor-ts", [13, 13], 'frameMs: 100, background: "#172336"'),
    "succ-still-comment": ("successor-ts", [14, 14], "`still` is the cell held when motion is reduced"),
    "succ-descriptor": ("successor-ts", [16, 16], "holdFrame: number | null"),
    "succ-motion": ("successor-ts", [17, 19], "globalThis.matchMedia?.(reducedMotionQuery)"),
    "succ-describe": ("successor-ts", [20, 23], "holdFrame: animate ? null : visual.still"),
    "succ-frameat": ("successor-ts", [24, 26], "Math.floor(Math.max(elapsed, 0) / display.frameMs) % descriptor.frames : descriptor.holdFrame ?? 0"),
    "succ-consumers": ("successor-ts", [27, 28], "export function compactStatus(state: QueueState, motion: MotionPreference = motionPreference())"),
    "sv-imports": ("succ-view", [3, 4], "/src/queue-view-successor.ts"),
    "sv-consumers": ("succ-view", [12, 14], "const media = matchMedia(reducedMotionQuery)"),
    "sv-paint": ("succ-view", [41, 52], "context.drawImage(asset.image, frame * width, 0, width, height, 0, 0, width * scale, height * scale)"),
    "sv-smoothing": ("succ-view", [45, 45], "context.imageSmoothingEnabled = display.filter !== 'nearest'"),
    "sv-geometry": ("succ-view", [48, 48], "asset.width === width * descriptor.frames && asset.height === height"),
    "sv-makecell": ("succ-view", [56, 78], "label.textContent = descriptor.label"),
    "sv-label": ("succ-view", [62, 62], "label.textContent = descriptor.label"),
    "sv-paint-at-creation": ("succ-view", [69, 69], "info.frame = paint(canvas, asset, descriptor, scale, elapsed)"),
    "sv-refresh": ("succ-view", [80, 87], "Re-derive a tracked cell from the same consumer under the current preference and repaint it in place"),
    "sv-select": ("succ-view", [103, 110], "stateAfter(event)"),
    "sv-change": ("succ-view", [114, 121], "media.addEventListener('change'"),
    "sv-animate": ("succ-view", [123, 130], "if (cell.canvas && cell.descriptor.animate)"),
    "sv-timeline": ("succ-view", [141, 149], "display.frameMs * statusVisuals[state].frames"),
    "sv-session": ("succ-view", [8, 8], "proves no reload between preference switches"),
    "sv-scope": ("succ-view", [158, 160], "Image provenance and visual/style acceptance are separate"),
    "sc-modules": ("succ-check", [51, 52], "fixture did not execute the retained original consumer module"),
    "sc-session": ("succ-check", [58, 59], "all phases observed in one open page session"),
    "sc-descriptor": ("succ-check", [81, 86], "hold frame is the declared still cell when stationary"),
    "sc-identical": ("succ-check", [126, 131], "both consumers return the identical running descriptor under this preference"),
    "sc-live": ("succ-check", [133, 146], "live cell holds the still cell under reduced motion"),
    "sc-timeline": ("succ-check", [148, 166], "reduced motion never leaves the held cell"),
    "sc-wrap": ("succ-check", [163, 164], "normal motion cycles through all four cells including the wrap"),
    "sc-switch": ("succ-check", [170, 190], "every Working cell stopped on the held cell without reload"),
    "sc-scope": ("succ-check", [191, 192], "it does not judge whether the held cell reads as Working"),
    "sc-compositing": ("succ-check", [105, 112], "source pixels and alpha compositing (rounding tolerance one)"),
    "sc-labels": ("succ-check", [126, 127], '"idle": "Start", "running": "Working", "paused": "Paused", "succeeded": "Ready", "failed": "Retry"'),
    "si-pixelated": ("succ-index", [21, 21], "image-rendering: pixelated"),
    "cap-phases": ("succ-capture", [4, 5], "normal-restored (emulate no-preference)"),
    "cap-emulate": ("succ-capture", [68, 68], "prefers-reduced-motion"),
    "cap-scope": ("succ-capture", [98, 98], "no reload between phases"),
    "disc-observed": ("discovery", [2, 3], "Current connected official PixelLab tool declarations exposed by host"),
    "disc-workbench": ("discovery", [14, 14], "mcp__pixellab__pixelart_workbench"),
    "disc-flash": ("discovery", [18, 18], "mcp__pixellab__create_image_pro_flash"),
    "disc-animate": ("discovery", [10, 10], "mcp__pixellab__animate_image"),
}


def verify_cites():
    results = []
    ok = True
    for key, (sid, (a, b), needle) in CITES.items():
        rel = SOURCES[sid]["path"]
        ls = lines_of(rel)
        text = "\n".join(ls[a - 1:b]) if 1 <= a <= b <= len(ls) else ""
        hit = needle in text
        ok &= hit
        results.append({"cite": key, "source": sid, "path": rel, "lines": [a, b], "expected_wording": needle, "verified": hit})
    if not ok:
        bad = [r for r in results if not r["verified"]]
        sys.exit("CITATION VERIFICATION FAILED: " + json.dumps(bad, indent=1))
    return results


def S(*keys):
    """Expand citation keys into source pointers {id, lines, locator}."""
    out = []
    for k in keys:
        sid, ln, needle = CITES[k]
        out.append({"id": sid, "lines": list(ln), "locator": k})
    return out


# ---------------------------------------------------------------- context packet: the 20 current criteria (exact ids + record hashes)
ctx = json.loads((ROOT / SOURCES["context"]["path"]).read_text(encoding="utf-8"))
assert ctx["hash"] == "3484cf385c91c8c28fa04316fb2c7c5b52c740178b505ccbd88631f57c893c9b" and ctx["revision"] == 88
CTX_CRITERIA = {c["id"]: {"record_sha256": c["record_sha256"], "ck": c["fields"]["ck"], "dm": c["fields"]["dm"]["$symbol"], "md": c["fields"]["md"]["$symbol"]} for c in ctx["criteria"]}
assert len(CTX_CRITERIA) == 20, len(CTX_CRITERIA)
JOB = ctx["jobs"][0]
assert JOB["id"] == "authoring-01.working.join-01" and JOB["state"] == "prepared" and JOB["remote_id"] is None
SEL = ctx["selection"]
assert SEL["requirements_hash"] == "2901c7107d4f162e98653140ea8061dfe213821b22a5e1338d9d2d6de5b4ad0c"
assert JOB["selection_bindings"][0]["requirements_hash"] == "e0614bd962a53a19003707f3d73326be436891e198eb1e4a262f12412fbfb027"

r2 = json.loads((ROOT / SOURCES["r2"]["path"]).read_text(encoding="utf-8"))
R2 = {c["criterion"]: c for c in r2["criteria"]}
assert set(R2) == set(CTX_CRITERIA)
for cid, c in R2.items():
    assert c["record_sha256"] == CTX_CRITERIA[cid]["record_sha256"], cid
cc = json.loads((ROOT / SOURCES["caller-cmp"]["path"]).read_text(encoding="utf-8"))
CC_DISP = {row["criterion"]: row for row in cc["criterion_comparisons"]}
assert set(CC_DISP) == set(CTX_CRITERIA)
VERDICT = cc["verdict"]

measurements = json.loads((ROOT / SOURCES["measurements"]["path"]).read_text(encoding="utf-8"))
assert measurements["source_sheet_sha256"] == SOURCES["working-png"]["sha256"]
M = {item["name"]: item for item in measurements["items"]}
CELL0 = M["working.png cell 0 (crop x=0..15)"]

# ---------------------------------------------------------------- shared clause texts
VIEW_COND = "Viewed at 1x and 3x nearest on #172336"
STYLE_TAIL = ("Readable compact silhouette(s), deliberate coherent clusters and stepped edges consistent with the exact Ready baseline "
              "(selective, intentional anti-aliasing is permitted under the full-alpha contract; accidental resampling blur or stray noise is not), "
              "and a perceptible cool-blue accent related to the Ready baseline and the preserved Start accent, judged qualitatively at 1x and 3x on #172336; "
              "no exact hex, palette count, binary alpha, stroke width or margin rule.")
FIXTURE = ("the successor browser fixture renderer-successor/view.mjs executing the actual src/queue.ts and src/queue-view-successor.ts modules, "
           "checked by renderer-successor/check.py against the retained capture")
START_BASIS = ("Inference, not an owner line: BRIEF line 3 and line 7 require non-colour distinction over the statuses the view shows; idle resolves to the Start control "
               "in the same status cells through both consumers in the original module (src/queue-view.ts lines 3, 10-11) and the successor (src/queue-view-successor.ts lines 7, 27-28), "
               "so the status set compared includes Start. 'Preserve the existing vector Start control' (BRIEF line 3) is NOT the basis; it only fixes the Start bytes.")


def measured_record(member_scope, construction_clause):
    return ("MEASURED record (mechanical/local, diagnostic): retain every cell's alpha histogram and exact RGBA component boxes (zero-based, half-open). "
            "FLAG for visual review any alpha>0 component touching all four cell edges, or any single alpha>0 component covering more than half of the cell's 256 pixels. "
            "The flag is a diagnostic proxy for a canvas matte or grey tile and is NOT a rejection condition (a corner-to-corner X or full-span glyph legitimately touches all four edges with a transparent exterior). "
            "RGB values of alpha-0 pixels are not significant. " + construction_clause)


VISUAL_RECORD = ("VISUAL record (visual/visual; the deciding rule): viewed at 1x and 3x on #172336, the exterior of {what} shows the panel with no unintended matte, tile, plate, halo or fringe; "
                 "a deliberate opaque backing shape is acceptable only when it is part of the mark's recorded design and the exterior stays transparent. "
                 "Partial alpha on mark pixels is permitted; binary alpha is not required.")

criteria = []


def add(cid, check, domain, mode, authority, basis, scope, sources, carries=(), expert_clauses=None, corrections=None, evidence_route=None, notes=None):
    rec = {"id": cid, "check": check, "domain": domain, "mode": mode, "authority": authority, "basis": basis, "scope": scope, "sources": sources}
    if carries:
        rec["carries"] = [{"id": c, "record_sha256": CTX_CRITERIA[c]["record_sha256"]} for c in carries]
    if expert_clauses:
        rec["expert_clauses"] = expert_clauses
    if corrections:
        rec["r2_corrections_applied"] = corrections
    if evidence_route:
        rec["evidence_route"] = evidence_route
    if notes:
        rec["notes"] = notes
    criteria.append(rec)


# ================================================================ WORKING successor stage
add("successor-01.working.q.geometry",
    "Decode assets/working.png as exactly 64x16: four horizontal 16x16 cells at x=0,16,32,48 with no gutters or added canvas between or around the cells "
    "(transparent margin inside a cell is composition, not padding). Consumer basis: src/queue-view-successor.ts declares running frames 4 (the sheet's cell count, unchanged under either preference), "
    "display.cell [16,16] and frameMs 100; the successor fixture draws only when width == 16*frames and height == 16, slices frame*16,0,16,16 and derives the frame from frameAt() "
    "(floor(elapsed/100) mod 4 when animating; the held cell otherwise).",
    "mechanical", "local", "requirement",
    "BRIEF line 3 (16x16 cells, four horizontal frames at 100 ms) with the successor consumer's frames 4 / display constants and the fixture geometry gate. r2 geometry correction carried: 'padding' means added canvas.",
    "whole Working sheet (both motion preferences)",
    S("brief-working", "succ-running", "succ-display", "succ-frameat", "sv-geometry", "sv-paint", "plar-geometry"),
    carries=["authoring-01.working.q.geometry"],
    corrections=["padding = added canvas between/around cells; in-cell transparent margins are composition (caller disposition: clarify)", "slicing/advance attributed to the fixture; frames and frameMs supplied by the consumer module (now the successor module)"],
    notes="Measured now on cf101610...: 64x16, fractional_alpha_pixels 0 (pixl_asset_check alpha=full). Mechanical only; not art acceptance.")

add("successor-01.working.q.transparent-exterior-measured",
    measured_record("Working", "Mechanical REJECTION is decidable only under the seed-rotation construction: each cell's alpha channel must equal that of cw^k(seed) under dst(x,y)=src(y,15-x) "
                    "(224 alpha-0 and 32 alpha-255 pixels per cell). Outside that construction the measured record carries no rejection rule."),
    "mechanical", "local", "observation",
    "BRIEF line 3 'transparent backgrounds' is the outcome; the measured record is the diagnostic/measurement route adopted by the caller (D1) for any future plan. "
    "The seed-rotation equality is construction-scoped (expert construction, not an owner rule).",
    "diagnostic proxy for every cell; triggers visual review; not a rejection rule. Mechanical rejection form only under the seed-rotation construction.",
    S("brief-transparent", "plar-geometry"),
    carries=["authoring-01.working.q.transparent-exterior"],
    corrections=["D1: four-edge / >half-cell component is a FLAG for visual review, not a rejection", "construction-scoped cw^k(seed) alpha equality is the only mechanical rejection form", "transparent-pixel RGB insignificant"],
    notes=f"Measured now (specialist-measurements.json): cell 0 alpha histogram {CELL0['alpha_histogram']}, components {CELL0['components']}, four_edge_components {CELL0['four_edge_components']}, over_half_cell_components {CELL0['over_half_cell_components']}; cells 1-3 equal cw^k(cell 0) on alpha and visible RGBA (True); cell 0 equals the accepted seed on alpha+visible RGBA (True). Transparent RGB in the sheet: 817 pixels (128,128,128,0), 79 pixels (0,0,0,0) - not significant.")

add("successor-01.working.q.transparent-exterior-visual",
    VISUAL_RECORD.format(what="every frame, including the held cell when stationary") + " The rejected generated frame whose background held 193 opaque #808080 pixels is the failure class, not the definition of the rule.",
    "visual", "visual", "requirement",
    "BRIEF line 3 'transparent backgrounds'; which opaque pixels are 'the mark' and whether a backing is unintended is a visual judgment (deciding rule). 'No plate' narrowed to unintended matte/tile/plate/fringe (D1).",
    "whole Working sheet; deciding rule for the transparent-exterior outcome",
    S("brief-transparent", "brief-inspect"),
    carries=["authoring-01.working.q.transparent-exterior"],
    corrections=["D1 split: visual record decides; blanket 'no plate' narrowed to unintended matte/tile/plate/fringe"],
    evidence_route="saved native/enlarged candidate views (fixture captures or pixl_inspection views); specialist views in specialist-views/ are preliminary, not the acceptance review")

add("successor-01.working.q.frame-assembly",
    "For the successor the candidate sheet is the existing assets/working.png (sha256 cf101610...), already the exact 64x16 four-cell sheet, so no assembly step occurs and this clause is satisfied vacuously; "
    "the retained record must still name the exact candidate bytes and their provenance (byte-identical to accepted live.working-animation-motion-01.candidate; cells equal cw^k(seed) on alpha and visible RGBA). "
    "If a future provider result is not already the exact 64x16 four-cell sheet, the retained assembly record names the exact source frames or cell rectangles in play order and every delivered cell is a lossless copy: "
    "identical alpha everywhere and identical RGBA where alpha>0 (RGB of alpha-0 pixels is not significant); no resize, resample or recolor; no undocumented duplication or silent frame drop "
    "(a deliberately repeated phase is allowed when the record says so); all raw provider outputs are retained beside the assembled strip.",
    "mechanical", "local", "requirement",
    "Assignment process requirement (retain exact frame-selection/assembly policy) and PIXL evidence discipline; r2 bounded 'lossless' and 'duplication'. Construction-scoped cw^k(seed) clause remains an expert proposal.",
    "this successor branch; conditional on any new assembly; the reuse case records provenance only",
    S("assign-step4-reuse", "brief-working"),
    carries=["authoring-01.working.q.frame-assembly"],
    corrections=["lossless bounded to alpha + visible RGBA", "duplication bounded to undocumented substitution", "construction-scoped rotation clause is a proposal"],
    expert_clauses=[{"text": "Under the seed-rotation construction, delivered cell k equals cw^k(seed) under dst(x,y)=src(y,15-x).", "authority": "proposal", "scope": "seed-rotation construction only", "status_for_reuse": "measured True for all four cells of cf101610..."}])

add("successor-01.working.q.activity-not-success",
    VIEW_COND + " (beside the exact Ready baseline as the comparison method), the running loop and each individual frame read as ongoing activity and not as completion: "
    "no frame forms a check mark or another success-like terminal pose.",
    "visual", "visual", "requirement",
    "BRIEF line 3 'The working loop must communicate activity without looking like success'; PLAR purpose 'without implying success'; BRIEF line 9 fixes the success motif as the asymmetrical check. "
    "Per-frame reading is an expert extension (frames show singly for 100 ms; frame 0 is painted at cell creation; the successor also holds one frame deliberately under reduced motion).",
    "loop: whole asset (requirement); per-frame: expert clause with rationale",
    S("brief-activity", "brief-ready", "plar-purpose-nosuccess", "plar-meaning", "sv-paint-at-creation"),
    carries=["authoring-01.working.q.activity-not-success"],
    corrections=["'arrowhead' and 'pause bars' are scoped expert guidance, not owner rules; binding distinction against delivered Retry/Paused is judged in the delivery distinction criterion"],
    expert_clauses=[{"text": "Avoid frames that read as the static symbol of another member (preserved Start arrowhead, paired pause bars).", "authority": "proposal", "scope": "this branch"}])

add("successor-01.working.q.motion-continuity",
    "Under normal motion, play the actual four frames at the consumer's 100 ms per frame including the fourth-to-first wrap, at 1x and 3x on #172336. Required outcome: the strip plays as one continuous activity loop "
    "with no visible discontinuity at the fourth-to-first wrap. All four frames remain in the sheet and in play under normal motion; the reduced-motion hold does not remove or reorder them.",
    "visual", "visual", "requirement",
    "BRIEF line 3 (four frames, 100 ms, loop communicates activity); display.frameMs 100; PLAR animation requirement loop:true nominal 400 ms; PLAR delivery check 'inspect the fourth-to-first transition'. "
    "D2 applied: even pacing / no near-hold are expert clauses, not the owner's 100 ms requirement.",
    "whole Working sheet under normal motion",
    S("brief-working", "succ-display", "plar-animation", "plar-delivery"),
    carries=["authoring-01.working.q.motion-continuity"],
    corrections=["D2: required outcome limited to one continuous loop at 100 ms/frame with no visible wrap discontinuity; 'evenly paced'/'no near-hold' moved to expert clauses"],
    expert_clauses=[
        {"text": "Stable centre/anchor and stable visual volume across phases (both consumers paint into a fixed 16x16 cell; drift reads as jitter).", "authority": "proposal", "scope": "whole Working asset (contract-bound expert clause via family.working.contract)"},
        {"text": "Motion evenly paced across the four frames with no near-hold (a held pair at 4 x 100 ms reads as a stutter).", "authority": "proposal", "scope": "specialist quality clause; satisfied by construction under seed rotation"},
        {"text": "Stable cluster count (three components per cell) and stepped quarter-turn phases with no morphing.", "authority": "proposal", "scope": "seed-rotation construction only"},
    ])

add("successor-01.working.q.style-coherence", STYLE_TAIL,
    "visual", "visual", "requirement",
    "BRIEF line 3 readable silhouettes / cool blue accent; adopted scoped caller style decision (exact ready.retained baseline: carry readable compact silhouettes, deliberate clusters/stepped edges, perceptible cool-blue accent, transparent exterior; not fixed: exact hex, palette count, binary alpha, stroke width, margins, check motif). "
    "'compact' and 'deliberate clusters' come from the adopted caller decision, not the original brief.",
    "whole Working sheet including the held cell; 'compact/deliberate clusters' scoped to this consumer status family",
    S("brief-transparent", "brief-inspect", "plar-style"),
    carries=["authoring-01.working.q.style-coherence"],
    corrections=["selective intentional anti-aliasing explicitly permitted under the full-alpha contract; accidental blur/noise is not"])

add("successor-01.working.q.consumers-normal-motion",
    "In " + FIXTURE + ", with the preference resolving to normal, exercise started -> running through stateAfter: both statusCell and compactStatus return the identical descriptor "
    "{label Working, path assets/working.png, frames 4, still 0, motion normal, animate true, holdFrame null}; the live cells (scale 3) and the state-matrix cells (scale 1 and 3) render assets/working.png "
    "with imageSmoothingEnabled false / image-rendering pixelated, composited over #172336, geometryMatches true. Frame-advance evidence: the capture timeline reports frame indices 0,0,1,1,2,2,3,3,0 at elapsed "
    "0,99,100,199,200,299,300,399,400 ms (floor(elapsed/100) mod 4; wrap at 400 ms) and the live requestAnimationFrame loop is observed cycling through all four cells; wall-clock frame duration is not measured and not claimed.",
    "engine", "live", "requirement",
    "src/queue.ts stateAfter; successor consumers (lines 27-28) both call describe(); display constants; fixture paint/animate/timeline; checker timeline and 'identical descriptor' checks. "
    "The fixture is named as the evidence route (r2 consumers correction).",
    "whole Working asset (integration, normal motion)",
    S("queue-state", "succ-consumers", "succ-describe", "succ-frameat", "sv-paint", "sv-animate", "sv-timeline", "sc-identical", "sc-timeline", "sc-wrap", "si-pixelated"),
    carries=["authoring-01.working.q.consumers"],
    corrections=["fixture named; frame-advance evidence = timeline frame indices incl. the 400 ms wrap plus observed cycling; wall-clock not measured; live 3x and matrix 1x/3x routes stated"],
    evidence_route="renderer-successor capture (phase normal-start and normal-restored) + check.py pass; the caller runs the browser capture")

add("successor-01.working.q.stationary-cell-identity",
    f"The stationary Working symbol is cell 0 of assets/working.png: the crop (0,0,16,16) in zero-based half-open coordinates, i.e. the cell declared by statusVisuals.running.still = 0 and painted when animate is false. "
    f"Record and re-measure: visible pixels {CELL0['visible_pixels']}, three 4-connected components with boxes {[c['box'] for c in CELL0['components']]} (half-open, zero-based), visible box {CELL0['visible_box_half_open']}, "
    f"mass centroid {CELL0['mass_centroid_edge_coords']} in pixel-edge coordinates (canvas centre 8.0,8.0), alpha histogram {CELL0['alpha_histogram']}; cell 0 equals the accepted seed (sha256 21f5baca...) on alpha and visible RGBA. "
    "The visual criteria below are judged on exactly this cell; if `still` changes, the identity record and those visual verdicts must be redone.",
    "mechanical", "local", "observation",
    "Ties the reviewed symbol to the consumer's actual held cell so the visual verdicts are about the pixels the consumer paints. Choosing cell 0 is a specialist proposal (see reduced_motion_design); the measurements are facts about cf101610....",
    "the held cell under reduced motion (cell index = statusVisuals.running.still)",
    S("succ-running", "succ-still-comment", "succ-describe", "succ-frameat", "sv-paint"),
    notes="Coordinate convention: zero-based pixel indices, boxes [left,top,right,bottom] half-open, centres in pixel-edge coordinates (index centroid + 0.5). Source image sha256 " + SOURCES["working-png"]["sha256"] + ", frame 0.")

add("successor-01.working.q.stationary-distinct-ready-paused",
    "Viewed stationary (no animation) at 1x and 3x nearest on #172336, in colour and in a non-colour comparison (grayscale or binarized silhouettes), the held cell is distinguishable from the Ready mark "
    "(assets/ready-confirmed.png) and from the Paused mark (assets/paused.png) by shape or structure alone, and does not read as completion or as pause.",
    "visual", "visual", "requirement",
    "authoring-plar.txt line 422 (caller update): 'the reduced-motion mode must use a stationary Working symbol distinguishable from Ready and Paused'; AUTHORING-UPDATE.md lines 2-4. "
    "'By shape or structure alone' follows BRIEF line 7 (keep existing requirements; distinction without relying on colour alone). Grayscale is the specialist's method; equivalent non-colour comparisons satisfy it.",
    "the held cell (stationary) versus Ready and Paused; whole successor",
    S("plar-purpose", "update-req", "brief-paused", "brief-keep", "brief-inspect"),
    evidence_route="saved native/enlarged views of the held cell beside Ready and Paused (fixture reduced-phase captures or pixl_inspection views); specialist preliminary views: specialist-views/ (views-pair, views-*-1x/3x)",
    notes="Specialist preliminary finding (not acceptance): PASS at 1x and 3x, colour and grayscale - three separated segments around an empty centre vs one continuous asymmetric check vs two solid tall bars; see reduced_motion_design.assessment.")

add("successor-01.working.q.stationary-distinct-retry-start",
    "Viewed stationary at 1x and 3x nearest on #172336, in colour and in a non-colour comparison, the held cell is distinguishable by shape or structure alone from the Retry mark (assets/error-retry.png) "
    "and from the preserved Start triangle (assets/start.svg as rendered in the idle cell), and does not read as failure/retry or as the Start control.",
    "visual", "visual", "requirement",
    START_BASIS + " For Retry: BRIEF line 3 'Error/retry must be distinguishable without color alone' is stated for Retry against the other statuses; the held Working cell is now one of those statuses, so the pair must stay distinct in both directions. "
    "Labelled: requirement by reasonable reading of BRIEF line 3/7 over the view's status set (an inference), not an owner line naming the stationary symbol.",
    "the held cell versus Retry and Start; whole successor",
    S("brief-retry", "brief-paused", "view-idle", "view-consumers", "succ-idle", "succ-consumers"),
    evidence_route="same saved views as the Ready/Paused criterion with Retry and the idle Start cell included",
    notes="Specialist preliminary finding: PASS, but this is the closest pair - both the held cell and Retry are roundish. Distinction rests on structure: Retry is one heavier near-closed ring (54 px, one component) with an arrowhead and a 1-px inner notch; the held cell is three disconnected 8-15 px segments with 2-3 px gaps and a wide empty centre. At 1x grayscale the difference is visible but subtle; the caller's review should look at this pair specifically.")

add("successor-01.working.q.stationary-meaning",
    "Viewed stationary at 1x and 3x on #172336 with its consumer label present, the held cell reads as the Working status's own symbol: it does not read as success (no check mark or terminal pose) "
    "and does not read as pause; it is recognisably one phase of the Working loop so that switching the preference while the page is open changes motion, not identity.",
    "visual", "visual", "requirement",
    "PLAR line 422 first sentence 'Communicate ongoing work ... without implying success' applies to the Working status in both modes; BRIEF line 3 'without looking like success'. "
    "Honest limit: no source requires the frozen symbol to convey motion; a frozen spinner communicates 'in progress / busy' by UI idiom but can also read as 'stalled'; the owner requirement is the non-success / non-pause reading plus Ready/Paused distinction, which is what this criterion binds.",
    "the held cell under reduced motion",
    S("plar-purpose-nosuccess", "brief-activity", "sv-label"),
    expert_clauses=[
        {"text": "Prefer a held cell that is literally a phase of the loop over a new static glyph, so the stationary and animated forms share identity and the preference switch repaints in place without changing the symbol.", "authority": "proposal", "scope": "this successor"},
        {"text": "The text label ('Working') rendered beside the glyph in both consumers carries the word; the glyph need not encode motion when frozen.", "authority": "observation", "scope": "fixture/consumer behaviour (view.mjs line 62)"},
    ])

add("successor-01.working.q.reduced-motion-consumer-mapping",
    "In " + FIXTURE + ", with the preference resolving to reduced ((prefers-reduced-motion: reduce) matches), exercise started -> running through stateAfter: both statusCell and compactStatus return the identical descriptor "
    "{label Working, path assets/working.png, frames 4, still 0, motion reduced, animate false, holdFrame 0}; under normal both return {..., motion normal, animate true, holdFrame null}. "
    "The sheet geometry stays 64x16 with frames 4 under both preferences (frames is the sheet's cell count, never changed by the preference). Under reduced, every Working cell (live 3x, matrix 1x and 3x) paints cell index holdFrame = still = 0 "
    "and the capture timeline reports frame 0 at every sample point (0..400 ms); no animation loop repaints Working cells. The static members (Start, Ready, Paused, Retry) resolve animate false / holdFrame 0 under both preferences with frames 1. "
    "The default preference source is matchMedia('(prefers-reduced-motion: reduce)') consulted by both consumers through motionPreference(); an explicit motion argument overrides it identically for both.",
    "engine", "live", "requirement",
    "PLAR line 422 'Confirm its consumer mapping before any further generation'; successor consumer module (describe/frameAt/statusCell/compactStatus; `still` comment) as the caller's proposed mapping; fixture paint/refresh; checker descriptor, identical-descriptor, live and timeline checks. "
    "The mapping design itself (preference = OS/browser media query; symbol = held cell; descriptor extension with `still`) is the caller's proposal adopted here by the specialist as the recommended mapping.",
    "whole successor (integration, reduced motion); both consumers",
    S("plar-purpose", "update-req", "succ-pref", "succ-running", "succ-still-comment", "succ-descriptor", "succ-motion", "succ-describe", "succ-frameat", "succ-consumers", "sv-consumers", "sv-paint", "sc-descriptor", "sc-identical", "sc-live", "sc-timeline", "sc-labels"),
    evidence_route="renderer-successor capture phase 'reduced' (DevTools media emulation) and, separately, an as-launched run with --force-prefers-reduced-motion for the startup path; check.py pass; the caller runs the capture",
    notes="Measured by the caller's fixture, not by this proposal. Mapping identity: M2-style descriptor extension with a `still` index and no new file (r2 options M1/M2); M3 (new queue state) remains not recommended.")

add("successor-01.working.q.live-preference-switch",
    "With the page open and Working shown (live cells and the state matrix in both consumers), change the preference in the same page session: on the media query change event every Working cell in both consumers "
    "(statusCell and compactStatus; live 3x; matrix 1x and 3x) is re-derived from the same consumer under the new preference and repainted in place - to the held cell (animate false, frame == holdFrame == 0) when the preference becomes reduced, "
    "and back to cycling (animate true, holdFrame null, all four cells observed) when it returns to normal - with no reload: one sessionId across all phases, the change event recorded with from/to and the repainted cell list, "
    "and the live Working cells among the repainted cells. Other states repaint unchanged.",
    "engine", "live", "requirement",
    "FOCUSED-SUCCESSOR.md step 4 'respect prefers-reduced-motion and changes while open' and step 6 'switching the preference in the same session'; step 3 'Add explicit reduced-motion mapping and live preference-switch acceptance'. "
    "Fixture change listener/refresh and sessionId; checker [switch] checks. This is an assignment requirement for the successor, not a BRIEF line.",
    "whole successor (integration); both consumers; same page session",
    S("assign-step4", "assign-step6", "assign-step3", "sv-change", "sv-refresh", "sv-session", "sc-switch", "sc-session", "cap-phases", "cap-emulate", "cap-scope"),
    evidence_route="renderer-successor capture phases normal-start -> reduced -> normal-restored in one page; check.py [switch] observations; the caller runs the capture and inspects the reduced-phase screenshot")

# ================================================================ RETRY and PAUSED members (carried r2-corrected; static members unchanged by the update)
for member, label, path_key, path, meaning_src, meaning_text, orig in (
    ("retry", "Retry", "retry-png", "assets/error-retry.png", "brief-retry",
     "the mark reads as failed work with a retry action and is identifiable by shape alone against Ready, every Working frame including the held cell, Paused and the preserved Start triangle; in particular it must not be confusable with the Working activity loop or its held cell. No specific retry motif (such as an arrow) is required.",
     "authoring-01.retry.q."),
    ("paused", "Paused", "paused-png", "assets/paused.png", "brief-paused",
     "the mark reads as paused work and is identifiable by shape alone against Ready (completion), every Working frame including the held cell (activity), Retry and the preserved Start triangle. No specific pause motif (such as paired bars) is required.",
     "authoring-01.paused.q."),
):
    trans = {"retry": "error -> failed", "paused": "pause -> paused"}[member]
    meaning_name = {"retry": "retry-meaning-without-color", "paused": "pause-meaning-without-color"}[member]
    add(f"successor-01.{member}.q.geometry",
        f"Decode {path} as exactly one static 16x16 frame; no strip, animation or extra canvas.",
        "mechanical", "local", "requirement",
        "BRIEF line 3 (16x16 cells; static) / line 7 (keep existing display requirements); consumer frames 1; fixture geometry gate. Caller disposition: keep.",
        f"whole {label} asset", S("brief-static", "brief-keep", "succ-paths", "sv-geometry"),
        carries=[orig + "geometry"], corrections=["none (keep)"])
    add(f"successor-01.{member}.q.transparent-exterior-measured",
        measured_record(label, "No mechanical rejection rule is decidable for this static member (no construction fixes its alpha set); the measured record is diagnostic only."),
        "mechanical", "local", "observation",
        "BRIEF line 3 'transparent backgrounds' is the outcome; measured record is the diagnostic route adopted by the caller (D1).",
        "diagnostic proxy; triggers visual review; not a rejection rule", S("brief-transparent"),
        carries=[orig + "transparent-exterior"], corrections=["D1 split; flag not rejection; no mechanical rejection form for a static member"],
        notes=f"Measured now: {json.dumps({k: M[path.split('/')[-1]][k] for k in ('visible_pixels', 'components', 'four_edge_components', 'over_half_cell_components', 'alpha_histogram')})}")
    add(f"successor-01.{member}.q.transparent-exterior-visual",
        VISUAL_RECORD.format(what="the image") + (" The rejected opaque magenta intermediate is the failure class, not the definition of the rule." if member == "paused" else ""),
        "visual", "visual", "requirement",
        "BRIEF line 3 'transparent backgrounds'; deciding visual rule (D1); 'no plate' narrowed to unintended matte/tile/plate/fringe.",
        f"whole {label} asset; deciding rule", S("brief-transparent", "brief-inspect"),
        carries=[orig + "transparent-exterior"], corrections=["D1 split: visual record decides"],
        evidence_route="saved native/enlarged views")
    add(f"successor-01.{member}.q.{meaning_name}",
        VIEW_COND + " in colour and in a non-colour comparison (grayscale or binarized silhouettes), " + meaning_text,
        "visual", "visual", "requirement",
        ("BRIEF line 3 'Error/retry must be distinguishable without color alone'; line 7 purpose unchanged." if member == "retry" else "BRIEF line 7 paused distinction without relying on colour alone.")
        + " Grayscale is a method (proposal); the motif is a PLAR proposal, not required. " + START_BASIS + " The held Working cell is added to the compared set because the successor shows it as a status cell.",
        f"whole {label} asset", S(meaning_src, "brief-keep", "view-idle", "view-consumers", "succ-idle", "succ-consumers"),
        carries=[orig + meaning_name],
        corrections=["non-colour comparison method made explicit", "no specific motif required", "D4: Start basis = idle resolves to Start in the same status cells (shared-consumer inference)"])
    add(f"successor-01.{member}.q.style-coherence", STYLE_TAIL,
        "visual", "visual", "requirement",
        "BRIEF line 3; adopted scoped caller style decision (exact ready.retained baseline). Selective intentional anti-aliasing permitted.",
        f"whole {label} asset; 'compact/deliberate clusters' scoped to this consumer status family", S("brief-transparent", "brief-inspect", "plar-style"),
        carries=[orig + "style-coherence"], corrections=["selective intentional anti-aliasing permitted; accidental blur/noise not"])
    add(f"successor-01.{member}.q.consumers",
        "In " + FIXTURE + f", exercise {trans} through stateAfter under both preferences: both statusCell and compactStatus resolve the identical descriptor {{label {label}, path {path}, frames 1, still 0, animate false, holdFrame 0}}; "
        "the live cells (scale 3) and the state-matrix cells (scale 1 and 3) render the PNG with imageSmoothingEnabled false / image-rendering pixelated over #172336, geometryMatches true, and no animation loop runs (frames 1).",
        "engine", "live", "requirement",
        "src/queue.ts stateAfter; successor consumers; fixture paint; checker descriptor checks. Static behaviour is tied to the frames > 1 gate in describe(); the preference does not change a static member.",
        f"whole {label} asset (integration)", S("queue-state", "succ-paths", "succ-describe", "succ-consumers", "sv-paint", "sc-descriptor", "sc-labels", "si-pixelated"),
        carries=[orig + "consumers"], corrections=["fixture named (now the successor fixture); routes stated; static behaviour tied to the frames > 1 gate"],
        evidence_route="renderer-successor capture + check.py")

# ================================================================ DELIVERY collective
add("successor-01.delivery.q.continuity",
    "Compare all four actual members together at 1x and 3x nearest on #172336 against the exact Ready baseline: coherent deliberate pixel treatment, readable visual weight coherent with the Ready baseline "
    "(identical stroke width or footprint is not required), perceptible cool-blue accent and transparent exteriors, including Working's four frames, its actual 100 ms playback with the wrap under normal motion, "
    "and the held cell shown stationary under reduced motion; no exact palette, alpha, stroke, margin or copied completion-motif requirement.",
    "continuity", "visual", "requirement",
    "BRIEF line 3 'coherent pixel-art status assets' and inspection conditions; adopted scoped style baseline (caller decision). D3 applied: coherence does not impose identical weight. The held cell is added to the compared set.",
    "collective delivery (Ready, Working incl. held cell, Retry, Paused)", S("brief-transparent", "brief-inspect", "plar-style"),
    carries=["authoring-01.delivery.q.continuity"],
    corrections=["D3: 'readable visual weight coherent with the Ready baseline (identical stroke width or footprint is not required)'"],
    evidence_route="saved views from both fixture phases (normal and reduced)",
    notes=f"Specialist preliminary observation: visible-pixel counts W-cell 32 / Ready 29 / Paused 60 / Retry 54 - the held cell is the lightest member; coherence is judged qualitatively, not by equal counts. Visible luminance ranges on #172336 (lum 34): W 129-154, Ready 169, Paused 141-161, Retry 139-154.")

add("successor-01.delivery.q.distinction",
    "View Ready, every Working frame, the running loop AND the stationary held cell, Retry and Paused together at 1x and 3x including a grayscale/non-colour comparison: Working (animated or held) never reads as success; "
    "the held cell is distinct from Ready and from Paused by shape or structure alone; Retry and Paused are each distinct from activity (including the held cell), completion and from each other by shape or structure alone; "
    "the preserved Start triangle remains separately identifiable from every member including the held cell.",
    "continuity", "visual", "requirement",
    "BRIEF lines 3 and 7 distinction requirements; PLAR line 422 stationary symbol distinguishable from Ready and Paused (requirement). Start clause: " + START_BASIS + " Caller disposition: keep (basis corrected per D4); the stationary symbol is added to the compared set.",
    "collective delivery", S("brief-activity", "brief-retry", "brief-paused", "plar-purpose", "view-idle", "view-consumers", "succ-idle", "succ-consumers"),
    carries=["authoring-01.delivery.q.distinction"],
    corrections=["D4: Start distinction basis is the shared-consumer inference, not 'preserve the vector Start control'", "held cell added to the compared set"],
    evidence_route="saved views; the reduced-phase fixture screenshot shows all five states held")

add("successor-01.delivery.q.destination",
    "Destination for the successor: src/queue-view-successor.ts + renderer-successor/ with the existing asset paths (assets/working.png, assets/ready-confirmed.png, assets/error-retry.png, assets/paused.png, assets/start.svg); "
    "src/queue-view.ts, renderer/ and every existing asset byte remain unchanged (hashes compared against the retained baseline). In " + FIXTURE + ", exercise all backend transitions (started, ok, error, pause, plus idle) "
    "through both statusCell and compactStatus under normal and reduced preferences with the exact package files at those paths: labels, frame counts (sheet geometry), horizontal slicing, frame index floor(elapsed/100) mod frames "
    "at the timeline sample points including the 400 ms wrap under normal and frame 0 at every sample under reduced (wall-clock duration not measured), nearest sampling at scale 1 (state matrix) and 3 (state matrix and live cells), "
    "alpha compositing on #172336, and - as the adopted destination-check method - recorded integer canvas placement matching the screenshot pixels; assets/start.svg byte hash unchanged; the fixture executed the successor module and not the retained original.",
    "engine", "live", "requirement",
    "BRIEF line 5 'Assets belong at the paths already used by the view'; FOCUSED-SUCCESSOR.md step 4 (keep old files untouched; implement the successor in the named files; identify the new destination); successor module paths; checker served-files/baseline checks. "
    "Integer placement is the adopted method (r2), not an owner rule.",
    "collective delivery (integration) at the successor destination", S("brief-paths", "assign-step4", "succ-header", "succ-paths", "queue-state", "sc-modules", "sc-compositing", "sc-labels", "brief-start"),
    carries=["authoring-01.delivery.q.destination"],
    corrections=["fixture named; timing evidence bounded to timeline frame indices; scale routes stated; integer placement labelled method; start.svg hash requirement unchanged", "destination updated to the successor files (assignment step 4)"],
    evidence_route="renderer-successor capture (all phases) + check.py with --baseline hash map")

CRITERIA_IDS = [c["id"] for c in criteria]
assert len(CRITERIA_IDS) == len(set(CRITERIA_IDS))

# ---------------------------------------------------------------- mapping: all 20 original ids -> new ids
MAP_NOTES = {
    "authoring-01.working.q.geometry": "carried with the r2 clarification (padding = added canvas; frames 4 is sheet geometry under both preferences).",
    "authoring-01.working.q.transparent-exterior": "split per D1 into a measured/diagnostic record and a deciding visual record; held cell included.",
    "authoring-01.working.q.frame-assembly": "carried; vacuous for the reuse candidate (already the exact 64x16 sheet) except the provenance record; r2 bounds applied.",
    "authoring-01.working.q.activity-not-success": "carried with the r2 scoping; the stationary reading is additionally bound by stationary-meaning.",
    "authoring-01.working.q.motion-continuity": "carried with D2 (even pacing is an expert clause); applies to normal motion only.",
    "authoring-01.working.q.style-coherence": "carried with the selective-AA note; held cell included.",
    "authoring-01.working.q.consumers": "carried as the normal-motion consumer criterion (fixture renamed to the successor fixture); the reduced branch and live switch are new criteria.",
    "authoring-01.retry.q.geometry": "carried unchanged (keep).",
    "authoring-01.retry.q.transparent-exterior": "split per D1 (no mechanical rejection form for a static member).",
    "authoring-01.retry.q.retry-meaning-without-color": "carried with r2 clarifications and D4 basis; the held Working cell added to the compared set.",
    "authoring-01.retry.q.style-coherence": "carried with the selective-AA note.",
    "authoring-01.retry.q.consumers": "carried; evaluated under both preferences (static member unchanged by the preference).",
    "authoring-01.paused.q.geometry": "carried unchanged (keep).",
    "authoring-01.paused.q.transparent-exterior": "split per D1 (no mechanical rejection form for a static member).",
    "authoring-01.paused.q.pause-meaning-without-color": "carried with r2 clarifications and D4 basis; the held Working cell added to the compared set.",
    "authoring-01.paused.q.style-coherence": "carried with the selective-AA note.",
    "authoring-01.paused.q.consumers": "carried; evaluated under both preferences.",
    "authoring-01.delivery.q.continuity": "carried with D3; the held cell added to the compared set.",
    "authoring-01.delivery.q.distinction": "carried (keep) with the D4 basis and the stationary symbol added to the compared set.",
    "authoring-01.delivery.q.destination": "carried with r2 clarifications; destination moved to the successor files per assignment step 4.",
}
mapping = []
for oid in sorted(CTX_CRITERIA):
    carriers = [c["id"] for c in criteria if any(x["id"] == oid for x in c.get("carries", []))]
    assert carriers, oid
    mapping.append({
        "original_id": oid,
        "record_sha256": CTX_CRITERIA[oid]["record_sha256"],
        "original_check": CTX_CRITERIA[oid]["ck"],
        "original_domain_mode": [CTX_CRITERIA[oid]["dm"], CTX_CRITERIA[oid]["md"]],
        "caller_disposition": next(k for k in ("keep", "clarify", "correct") if oid in VERDICT[k]),
        "r2_change": R2[oid]["change"],
        "carried_by": carriers,
        "non_applicability": None,
        "note": MAP_NOTES[oid] + " Historical Q record unchanged; no verdict transferred.",
    })
assert len(mapping) == 20
new_only = [c["id"] for c in criteria if not c.get("carries")]

# ---------------------------------------------------------------- reduced-motion design
reduced_motion_design = {
    "assignment_option_assessed": "Hold cell 0 of the existing PixelLab-produced sheet assets/working.png when the user prefers reduced motion, while retaining all four cells at 100 ms under normal motion (FOCUSED-SUCCESSOR.md lines 18-23: a proposed implementation, not an owner-imposed motif/palette/frame choice).",
    "what_was_viewed": {
        "images": ["views-color-1x", "views-gray-1x", "views-color-3x", "views-gray-3x", "views-color-12x", "views-gray-12x", "views-pair", "views-grid"],
        "method": "Cells 0-3 of assets/working.png, Ready, Paused, Retry and a 16x16 rasterization of assets/start.svg (M4 2L14 8L4 14Z, #70b9ed, 16x supersample box-downsampled; comparison aid only - the fixture renders the SVG itself) composited on #172336, nearest-neighbour at 1x, 3x and 12x, colour and grayscale, viewed by the specialist as image files. In the grayscale sheets the tile (including its panel) is converted to L while the margin stays the blue panel; this is a rendering convenience, not a defect of the art.",
    },
    "measured_facts": {
        "convention": measurements["convention"],
        "sheet": {"path": "assets/working.png", "sha256": SOURCES["working-png"]["sha256"], "size": [64, 16], "visible_pixels": 128, "visible_colors": 9, "fractional_alpha_pixels": 0, "opaque_components": 12, "tool": "pixl_asset_check(alpha=full)"},
        "cell0_frame0": CELL0,
        "cells_equal_cw_k_of_cell0_on_alpha_and_visible_rgba": [True, True, True],
        "cell0_equals_accepted_seed_21f5baca_on_alpha_and_visible_rgba": measurements["cell0_equals_seed_alpha_visible_rgba"],
        "transparent_rgb_in_sheet": {"(128,128,128,0)": 817, "(0,0,0,0)": 79, "significance": "none"},
        "comparators": {k: {kk: M[k][kk] for kk in ("visible_pixels", "components", "visible_box_half_open", "mass_centroid_edge_coords")} for k in ("ready-confirmed.png", "paused.png", "error-retry.png")},
        "luminance_on_panel": {"panel": 34, "working_cells": [129, 154], "ready": [169, 169], "paused": [141, 161], "retry": [139, 154], "start_raster": [166, 179], "note": "Rec.601 luma of visible pixels; all members sit 95-145 above the panel, so grayscale contrast is not the discriminator - structure is."},
        "measurements_file": "measurements",
    },
    "assessment": {
        "a_distinct_from_ready_and_paused": "PASS (specialist visual judgment at 1x and 3x, colour and grayscale, on #172336). Cell 0 is three disconnected segments (9, 8 and 15 px) placed top, right and bottom-left around an empty centre - a broken ring. Ready is one continuous diagonal check with asymmetric arms (29 px, one component). Paused is two solid vertical 3x10 bars (two 30-px components). At 1x the held cell reads as a small broken circle, Ready as a check, Paused as two bars; none of the three can be confused by silhouette. Grayscale changes nothing structural.",
        "b_distinct_from_retry_and_start": "PASS with a caveat (inference, not an owner line: BRIEF line 3/7 non-colour distinction read over the view's status set, idle -> Start through both consumers). Start is a solid filled right-pointing triangle - unmistakable. Retry is the closest neighbour: a heavier near-closed ring (54 px, one component) with an arrowhead at top-right and a 1-px inner notch. The held cell differs by structure (three gaps of 2-3 px, wide empty centre, no arrowhead, roughly half the mass). At 3x the pair is clearly distinct; at 1x grayscale the difference is visible but subtle (ring with notch vs ring with three gaps). The caller's visual review should look at this pair specifically on the fixture capture.",
        "c_reads_as_ongoing_work_when_frozen": "QUALIFIED. A frozen spinner cell is the conventional static 'busy / in progress' idiom and does not read as success or pause - the owner requirements that actually bind (PLAR line 422; BRIEF line 3). Honestly: frozen, it does not convey motion, and a user who does not know the preference is active could read it as stalled. Mitigations present in the consumer: the text label 'Working' is rendered beside the glyph in both consumers (view.mjs line 62), and the held cell is literally a phase of the loop, so identity is preserved when the preference switches. No source requires the stationary symbol to convey motion; this criterion set binds non-success/non-pause reading plus distinction, and records the 'stalled' reading as a known limit.",
    },
    "alternatives": [
        {"option": "another cell of the sheet (cells 1-3)", "assessment": "Equivalent by construction: each is a clockwise quarter-turn of cell 0 with the same three components and 32 px. No readability gain. Cell 0 is preferred because it is byte-equal (alpha + visible RGBA) to the accepted seed, so the stationary symbol has the cleanest provenance, and `still: 0` matches the caller's successor default."},
        {"option": "P2 - new static three-dot ellipsis glyph (r2 reduced_motion.d)", "assessment": "Conventional 'in progress' glyph and clearly distinct from check/bars/ring/triangle, but it needs new 16x16 art, a new descriptor path or key, and breaks the identity between the animated and stationary forms (switching the preference would swap symbols, not just stop motion). At 1x, three 2x2 dots risk reading as a dashed line. Not recommended for this successor; viable fallback if the owner rejects frozen-spinner semantics."},
        {"option": "P3 - new static gapped ring", "assessment": "Too close to the delivered Retry ring (a ring minus its arrowhead); would weaken the Retry distinction. Not recommended."},
        {"option": "M3 - a reduced-motion queue state", "assessment": "Not recommended: motion preference is presentation, not a backend transition; the successor correctly keeps src/queue.ts unchanged."},
    ],
    "recommendation": {
        "label": "SPECIALIST PROPOSAL (not an owner requirement; adoption is the caller's decision)",
        "symbol": "P1: hold cell 0 (frame index 0; crop (0,0,16,16)) of the existing assets/working.png under reduced motion; keep all four cells at 100 ms under normal motion.",
        "mapping": "The caller's successor design as read in src/queue-view-successor.ts: statusVisuals.running keeps frames 4 (sheet geometry) and gains still 0; describe() yields animate=false / holdFrame=0 when motionPreference() is reduced and animate=true / holdFrame=null otherwise; both statusCell and compactStatus call describe() so they return the identical descriptor; frameAt() paints the held cell; the fixture listens to the media query change event and repaints every tracked cell in place. This is M2-style (descriptor extension) without a new file; it satisfies the PLAR line 422 'confirm its consumer mapping' obligation once the fixture capture passes check.py.",
        "why": ["no new art, one source of truth, the stationary symbol is a phase of the loop", "both consumers share the mapping automatically", "the sheet and its accepted provenance are untouched", "the preference switch changes motion, not identity"],
        "conditions": ["the caller's visual review on the actual fixture capture confirms (a), (b) and (c) above - especially the held-cell-vs-Retry pair at 1x grayscale", "the owner/caller accepts frozen-spinner semantics for reduced motion (recorded limit: can read as stalled); if not, fall back to P2 with a new generation"],
    },
    "pixellab_work_needed": False,
    "pixellab_request": None,
    "pixellab_reasoning": "none: the recommendation reuses the existing accepted sheet unchanged and changes only the consumer/renderer mapping; the stationary symbol is an existing cell. The old prepared join job authoring-01.working.join-01 (prepared, undispatched, remote_id null, bound to requirements_hash e0614bd9...) is not needed for this successor because the sheet it would construct already exists byte-identically as assets/working.png; its resolution is the caller's (not touched or reinterpreted here). Contingency only (not proposed): if the owner rejects frozen-spinner semantics, P2 would need one 16x16 static image via mcp__pixellab__create_image_pro_flash (declared in official-discovery.json line 18) with assets/ready-confirmed.png as style_image and a new destination/descriptor; that request would be authored only after that decision.",
    "job_identity_preserved": {"id": JOB["id"], "state": JOB["state"], "remote_id": JOB["remote_id"], "intent_sha256": JOB["intent_sha256"], "request_tool": JOB["request_tool"], "bound_requirements_hash": JOB["selection_bindings"][0]["requirements_hash"], "current_requirements_hash": SEL["requirements_hash"], "blockers": JOB["blockers"], "note": "not touched; caller resolves"},
}

reuse = {
    "candidate": {"path": "assets/working.png", "sha256": SOURCES["working-png"]["sha256"], "provenance": "byte-identical to accepted original-family candidate live.working-animation-motion-01.candidate (family.working.output, original plar.txt); cells = cw^k(seed 21f5baca...) on alpha and visible RGBA"},
    "judgment": "PROPOSAL: the existing sheet satisfies the proposed successor criteria as a candidate, pending the caller's fixture capture and visual review. No verdict of the original family is transferred; every check below is new evidence or still owed.",
    "satisfied_now_by_specialist_measurement": ["successor-01.working.q.geometry (64x16, frames 4, no added canvas)", "successor-01.working.q.transparent-exterior-measured (0 fractional alpha; 3 components per cell; no four-edge or >half-cell component; cw^k(seed) alpha equality True)", "successor-01.working.q.frame-assembly (reuse case: provenance recorded; no assembly)", "successor-01.working.q.stationary-cell-identity (cell 0 measured; equals seed)"],
    "preliminary_specialist_visual_pass_not_acceptance": ["successor-01.working.q.transparent-exterior-visual", "successor-01.working.q.activity-not-success", "successor-01.working.q.style-coherence", "successor-01.working.q.stationary-distinct-ready-paused", "successor-01.working.q.stationary-distinct-retry-start (closest pair; re-check at 1x grayscale)", "successor-01.working.q.stationary-meaning (qualified: frozen-spinner semantics)", "successor-01.delivery.q.continuity", "successor-01.delivery.q.distinction"],
    "still_needs_caller_fixture_or_review": ["successor-01.working.q.motion-continuity (actual 100 ms playback with the wrap in the fixture)", "successor-01.working.q.consumers-normal-motion", "successor-01.working.q.reduced-motion-consumer-mapping", "successor-01.working.q.live-preference-switch", "successor-01.retry.q.consumers", "successor-01.paused.q.consumers", "successor-01.delivery.q.destination", "all visual criteria: the caller's own viewing of saved native/enlarged fixture captures (specialist views are preliminary)"],
    "retry_and_paused_members": "unchanged files (80d2b823..., 0fb0ab5e...); their member criteria are carried with r2 corrections; no verdict transferred.",
}

constraints_honored = {
    "measured_vs_visual_matte": "transparent-exterior is split in every member: the measured record (alpha histogram + component boxes; four-edge / >half-cell = flag) is diagnostic and carries a mechanical rejection only under the seed-rotation construction; the visual record decides unintended matte/tile/plate/fringe.",
    "geometry_margins": "geometry criteria define padding as added canvas between/around cells; in-cell transparent margins are composition and are never rejected.",
    "pacing": "motion-continuity binds only one continuous loop at 100 ms/frame with no visible wrap discontinuity as the owner requirement; 'evenly paced' / 'no near-hold' are labelled expert clauses.",
    "coherence_weight": "continuity asks for readable visual weight coherent with the Ready baseline and states that identical stroke width or footprint is not required.",
    "start_inference": "every Start-distinction clause rests on idle -> Start resolving in the same status cells through both consumers (src/queue-view.ts lines 3, 10-11; successor lines 7, 27-28) and is labelled an inference over BRIEF line 3/7, not on 'preserve the vector Start control'.",
    "selective_aa_full_alpha": "style-coherence criteria permit selective intentional anti-aliasing under the full-alpha contract and reject only accidental blur/noise; no binary-alpha rule anywhere.",
    "fixture_evidence_route": "every engine/live criterion names the renderer-successor fixture + check.py as the route and bounds frame-advance evidence to timeline frame indices (incl. the 400 ms wrap) without claiming wall-clock measurement.",
}

not_claimed = [
    "acceptance of any candidate (the existing sheet is proposed for reuse; the caller's fixture and visual review decide)",
    "adoption of this proposal or of criterion ids 'successor-01.*' (the caller authors the plan/ids through the public operations)",
    "any PixelLab generation, dispatch, provider observation or job change (none performed; none needed for the recommendation)",
    "resolution or reinterpretation of job authoring-01.working.join-01 (caller decision)",
    "transfer of any original-family verdict to the successor",
    "browser capture or check.py results (the caller runs the capture; none exists in this proposal)",
    "that the frozen held cell conveys motion (recorded limit)",
    "that the rasterized Start comparison equals the browser's SVG rendering (it is a comparison aid; the fixture renders the SVG)",
    "any change to existing files, kit, runtime, global configuration or persistent memory",
]

proposal = {
    "version": 1,
    "kind": "specialist-proposal",
    "role": "PIXL specialist (foreground delegate, Claude Fable 5.1 host model) for FOCUSED-SUCCESSOR.md step 2",
    "assignment": {"path": "FOCUSED-SUCCESSOR.md", "sha256": SOURCES["assignment"]["sha256"], "step": 2, "lines": [18, 23]},
    "asset_id": "queue.working",
    "requirements_hash": SEL["requirements_hash"],
    "old_requirements_hash_bound_in_plan_and_job": JOB["selection_bindings"][0]["requirements_hash"],
    "state": {"path": SOURCES["state"]["path"], "sha256": SOURCES["state"]["sha256"], "revision": ctx["revision"]},
    "context_packet": {"path": SOURCES["context"]["path"], "sha256": SOURCES["context"]["sha256"], "criteria_count": len(CTX_CRITERIA), "sources_count": len(ctx["sources"])},
    "conventions": {
        "lines": "one-based inclusive file-local bounds; every cited range was opened at build time and verified to contain the wording listed in specialist-report.json.verification",
        "authority": "requirement / proposal / observation (PLAR labels); 'requirement' includes consumer-code behaviour, the caller's PLAR update and assignment process requirements where the basis says so; Start distinction is labelled an inference",
        "images": "zero-based pixel coordinates; component boxes half-open [left,top,right,bottom]; centres in pixel-edge coordinates; measurements are facts, not verdicts",
        "expert_clauses": "listed separately from the check; never owner authority",
    },
    "sources": SOURCES,
    "reduced_motion_design": reduced_motion_design,
    "criteria": criteria,
    "criteria_summary": {"count": len(criteria), "new_for_reduced_motion": new_only, "working": len([c for c in criteria if ".working." in c["id"]]), "retry": len([c for c in criteria if ".retry." in c["id"]]), "paused": len([c for c in criteria if ".paused." in c["id"]]), "delivery": len([c for c in criteria if ".delivery." in c["id"]])},
    "mapping": mapping,
    "reuse": reuse,
    "constraints_honored": constraints_honored,
    "carried_review_artifacts": {"r2": {"path": SOURCES["r2"]["path"], "sha256": SOURCES["r2"]["sha256"]}, "caller_comparison": {"path": SOURCES["caller-cmp"]["path"], "sha256": SOURCES["caller-cmp"]["sha256"], "review_scope_sha256": cc["review_scope_sha256"], "verdict": VERDICT["contract_consistency"]}},
    "not_claimed": not_claimed,
}

verification = verify_cites()
(OUT / "specialist-proposal.json").write_text(json.dumps(proposal, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
proposal_sha = sha("work/focused-successor/specialist-proposal.json")

artifacts = [{"path": "work/focused-successor/specialist-proposal.json", "sha256": proposal_sha, "role": "specialist proposal v1 (criteria, reduced-motion design, mapping, reuse)"}]
for name in sorted(p.name for p in VIEWS.iterdir()):
    artifacts.append({"path": f"work/focused-successor/specialist-views/{name}", "sha256": sha(f"work/focused-successor/specialist-views/{name}"), "role": "specialist inspection view" if name.endswith(".png") else "reproducible measurements"})
artifacts.append({"path": "work/focused-successor/specialist-build-proposal.py", "sha256": sha("work/focused-successor/specialist-build-proposal.py"), "role": "builder (verifies citations, computes hashes)"})

report = {
    "version": 1,
    "kind": "delegation-contract result",
    "status": "delivered",
    "status_basis": "Planning-only assignment (FOCUSED-SUCCESSOR.md step 2): the complete reviewed criteria set, reduced-motion design, 20-row mapping, reuse judgment and constraint statements are returned. No generation, state change or acceptance was in scope; the asset remains unaccepted and the task open.",
    "asset_id": "queue.working",
    "requirements_hash": SEL["requirements_hash"],
    "plar": {"path": "authoring-plar.txt", "sha256": SOURCES["plar"]["sha256"], "row_lines": [420, 675]},
    "state": proposal["state"],
    "artifacts": artifacts,
    "checks": [
        {"check": "hashes of every caller-stated fact file (BRIEF, AUTHORING-UPDATE, authoring-plar, state.px, context packet, r2, caller comparison, assets, src, renderer-successor)", "result": "all match the caller's stated values", "evidence": "specialist-proposal.json.sources"},
        {"check": "pixl_asset_check(alpha=full) on assets/working.png, ready-confirmed.png, paused.png, error-retry.png", "result": "64x16/16x16 as expected; fractional_alpha_pixels 0 for all; components 12/1/2/1; visible 128/29/60/54", "evidence": "specialist-proposal.json.reduced_motion_design.measured_facts"},
        {"check": "cells 1-3 equal cw^k(cell 0) and cell 0 equals accepted seed 21f5baca... on alpha + visible RGBA", "result": "True", "evidence": "work/focused-successor/specialist-views/specialist-measurements.json"},
        {"check": "component boxes / centroids / alpha histograms for cells 0-3, Ready, Paused, Retry (zero-based, half-open)", "result": "recorded", "evidence": "work/focused-successor/specialist-views/specialist-measurements.json"},
        {"check": "visual inspection of W0..W3, Ready, Paused, Retry, rasterized Start on #172336 at 1x/3x/12x colour + grayscale (image files opened by the specialist)", "result": "held cell distinct from Ready and Paused (pass); from Retry and Start (pass; Retry is the closest pair at 1x grayscale); frozen reading qualified (can read as stalled)", "evidence": "work/focused-successor/specialist-views/*.png"},
        {"check": "consumer mapping read in src/queue-view-successor.ts, renderer-successor/view.mjs, check.py, capture.mjs, index.html", "result": "both consumers call describe(); reduced -> animate false / holdFrame = still = 0; frames stays 4; change listener repaints in place; checker covers identical descriptor, timeline, switch, single session", "evidence": "pixl_source retrievals cited in the proposal"},
        {"check": "20 criterion ids + record_sha256 read programmatically from the context packet and cross-checked against r2 and the caller comparison", "result": "all 20 match; each mapped to >= 1 successor criterion", "evidence": "specialist-proposal.json.mapping"},
        {"check": "citation verification (open file, inclusive bounds, expected wording)", "result": f"{sum(1 for v in verification if v['verified'])}/{len(verification)} verified", "evidence": "specialist-report.json.verification"},
    ],
    "unavailable_checks": ["browser capture / check.py run (caller performs)", "pixl_inspection views (caller performs; write tools not permitted to the specialist)", "actual browser rendering of assets/start.svg (rasterization used only as a comparison aid)"],
    "tools_used": ["Skill pixl:pixl", "Read", "Glob", "Grep", "Bash (python -I with Pillow)", "pixl_asset_check", "pixl_source"],
    "tools_not_called": ["pixl_commit", "pixl_job_*", "pixl_plar_save", "pixl_plar_prepare", "pixl_production_plan", "pixl_stage_prepare", "pixl_inspection_prepare", "pixl_inspection_review", "pixl_task_complete", "pixl_plar_handoff", "any PixelLab tool"],
    "files_modified": [],
    "files_created": [a["path"] for a in artifacts] + ["work/focused-successor/specialist-report.json"],
    "verification": verification,
    "request_review": {"packet": "work/focused-successor/specialist-proposal.json", "sha256": proposal_sha, "kind": "criteria/creative contract (no provider_arguments; pixellab_work_needed false)", "caller_action": "independent comparison per FOCUSED-SUCCESSOR.md step 3"},
    "provider": {"observed": None, "job_preserved": reduced_motion_design["job_identity_preserved"]},
    "recommendation": reduced_motion_design["recommendation"]["symbol"],
    "pixellab_work_needed": False,
    "questions": [
        "Does the owner/caller accept frozen-spinner semantics for reduced motion (the held cell reads as busy but not as motion; can read as stalled)? If not, P2 (new static glyph) becomes the fallback and would need one generation.",
        "Does the caller adopt 'distinct from Retry and Start' for the stationary symbol as an inference over BRIEF line 3/7 (proposed here), or keep only the explicit Ready/Paused requirement?",
    ],
    "next": "Caller: compare this proposal independently (step 3), then run renderer-successor/capture.mjs (phases normal-start, reduced, normal-restored; plus an as-launched run with --force-prefers-reduced-motion) and check.py; view the reduced-phase captures natively and enlarged, paying attention to the held cell beside Retry at 1x grayscale; resolve the obsolete job through its failed-observation route; author the successor plan/criteria through the public operations.",
    "generated_at": datetime.now(timezone.utc).isoformat(),
}
(OUT / "specialist-report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"proposal": {"path": "work/focused-successor/specialist-proposal.json", "sha256": proposal_sha}, "report": {"path": "work/focused-successor/specialist-report.json", "sha256": sha("work/focused-successor/specialist-report.json")}, "criteria": len(criteria), "mapping_rows": len(mapping), "citations_verified": f"{sum(1 for v in verification if v['verified'])}/{len(verification)}", "new_criteria": new_only}, indent=1))
