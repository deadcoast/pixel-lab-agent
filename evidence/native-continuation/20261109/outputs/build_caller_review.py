"""Build work/continuation/CALLER-REVIEW-01.json: the calling agent's independent comparison of the 20 original
authoring-01 criteria with the retained 29-criterion reduced-motion proposal (work/focused-successor/specialist-proposal.json).

Literal checks, IDs and record hashes are read programmatically from the retained artifacts; every source locator
cited below is opened at build time and must contain its expected wording, otherwise the build fails.
The caller's dispositions are authored in this file. Nothing outside work/continuation is written.

Usage: python -I work/continuation/build_caller_review.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
OUT = "work/continuation/CALLER-REVIEW-01.json"


def sha(path: str) -> str:
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def load(path: str):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def lines_of(path: str) -> list[str]:
    with open(path, encoding="utf-8", errors="strict") as handle:
        return handle.read().split("\n")


# ---------------------------------------------------------------- retained artifacts
PROPOSAL = "work/focused-successor/specialist-proposal.json"
REPORT = "work/focused-successor/specialist-report.json"
CONTEXT = "work/focused-successor/context-authoring-raw.json"
R2 = "work/criteria-review-01/specialist-proposal-r2.json"
PRIOR_CALLER = "work/export-review-01/caller-comparison.json"
EXPORT = "work/continuation/request-review-authoring-01.json"
PLAR_READ = "work/continuation/plar-read-queue-working-raw.json"
MEASURE = "work/continuation/caller-measurements.json"
ROUND1 = "work/continuation/SPECIALIST-ROUND1.json"

proposal = load(PROPOSAL)
report = load(REPORT)
context = load(CONTEXT)
r2 = load(R2)
prior = load(PRIOR_CALLER)
export = load(EXPORT)
plar_read = load(PLAR_READ)
measurements = load(MEASURE)

EXPECTED_PROPOSAL_SHA = "792d4b8f47211a0c646466793e54cc4c16e85c6556bd471f44de2562809b14b3"
assert sha(PROPOSAL) == EXPECTED_PROPOSAL_SHA, "proposal bytes changed"
assert report["request_review"]["sha256"] == EXPECTED_PROPOSAL_SHA

# ---------------------------------------------------------------- source index with verified locators
SOURCES = {
    "brief": ("BRIEF.md", "owner brief"),
    "update": ("AUTHORING-UPDATE.md", "caller reduced-motion update for the authoring branch"),
    "plar": ("authoring-plar.txt", "current authoring PLAR; queue.working row lines 420-675"),
    "assignment": ("FOCUSED-SUCCESSOR.md", "assignment answered by the proposal (steps 2-6)"),
    "authoring-stage": ("AUTHORING-STAGE.md", "earlier authoring assignment; source of the frame-selection/assembly policy process requirement (omitted from the proposal's source index)"),
    "continuation": ("CONTINUATION-ASSIGNMENT.md", "this comparison assignment"),
    "queue-ts": ("src/queue.ts", "backend state machine shared by both consumers"),
    "view-ts": ("src/queue-view.ts", "original consumer module, unchanged (historical destination)"),
    "successor-ts": ("src/queue-view-successor.ts", "caller-proposed successor consumer module (design proposal, not owner authority)"),
    "succ-view": ("renderer-successor/view.mjs", "successor browser fixture (evidence route for engine/live criteria)"),
    "succ-check": ("renderer-successor/check.py", "successor mechanical checker"),
    "succ-capture": ("renderer-successor/capture.mjs", "successor capture driver"),
    "succ-index": ("renderer-successor/index.html", "successor fixture page"),
    "old-view": ("renderer/view.mjs", "original fixture, unchanged"),
    "state": (".pixl/assets/queue.ready/state.px", "PX2 store revision 88, read only"),
    "working-png": ("assets/working.png", "existing PixelLab-produced Working sheet 64x16 (reuse candidate)"),
    "ready-png": ("assets/ready-confirmed.png", "exact Ready style baseline ready.retained"),
    "paused-png": ("assets/paused.png", "delivered Paused member"),
    "retry-png": ("assets/error-retry.png", "delivered Retry member"),
    "start-svg": ("assets/start.svg", "preserved vector Start control"),
    "seed-png": (".pixl/assets/queue.ready/artifacts/21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png", "accepted Working seed"),
    "proposal": (PROPOSAL, "reviewed 29-criterion proposal (unchanged)"),
    "report": (REPORT, "specialist delegation result for the proposal"),
    "context": (CONTEXT, "focused authoring context: the 20 original criteria with record hashes"),
    "r2": (R2, "prior corrected proposal r2 (D1-D4 corrections)"),
    "prior-caller": (PRIOR_CALLER, "prior caller comparison of the 20 criteria"),
    "export": (EXPORT, "fresh pixl_request_review export retained by this caller"),
    "plar-read": (PLAR_READ, "fresh pixl_plar_read(queue.working) retained as exact bytes"),
    "measurements": (MEASURE, "caller's own reproducible measurements"),
    "render-01": ("work/focused-successor/render-01/launch.json", "incomplete successor capture (no render.json)"),
}
sources = {k: {"path": p, "sha256": sha(p), "role": role} for k, (p, role) in SOURCES.items()}

# locator id -> (source id, [first,last], expected substring)
LOCATORS = {
    "brief-cells": ("brief", [3, 3], "Status cells are 16 by 16 logical pixels"),
    "brief-working": ("brief", [3, 3], "Working uses four horizontal frames with a 100 ms frame duration"),
    "brief-static": ("brief", [3, 3], "Ready and Retry are static images"),
    "brief-transparent": ("brief", [3, 3], "Use transparent backgrounds, readable silhouettes and the existing UI's cool blue accent; a fixed palette is not required"),
    "brief-inspect": ("brief", [3, 3], "Inspect at 1x and 3x nearest display scale on the actual dark panel"),
    "brief-activity": ("brief", [3, 3], "The working loop must communicate activity without looking like success"),
    "brief-retry": ("brief", [3, 3], "Error/retry must be distinguishable without color alone"),
    "brief-start": ("brief", [3, 3], "Preserve the existing vector Start control"),
    "brief-paths": ("brief", [5, 5], "Assets belong at the paths already used by the view"),
    "brief-paused": ("brief", [7, 7], "Its status image must be distinguishable from activity, completion and retry without relying on color alone"),
    "brief-keep": ("brief", [7, 7], "Keep the existing style and display requirements"),
    "brief-ready": ("brief", [9, 9], "Ready must visibly use a check mark with asymmetrical arms"),
    "update-req": ("update", [2, 4], "a stationary Working\nsymbol distinct from Ready and Paused"),
    "plar-purpose": ("plar", [422, 422], "the reduced-motion mode must use a stationary Working symbol distinguishable from Ready and Paused. Confirm its consumer mapping before any further generation."),
    "plar-purpose-nosuccess": ("plar", [422, 422], "Communicate ongoing work in both full and compact status cells without implying success"),
    "plar-style": ("plar", [512, 528], "approved_style_reference"),
    "plar-geometry": ("plar", [529, 545], "image_geometry"),
    "plar-animation": ("plar", [546, 559], "frame_duration_ms"),
    "plar-meaning": ("plar", [560, 570], "success-like terminal pose"),
    "plar-delivery": ("plar", [606, 619], "Play the loop at 100 ms per frame and inspect the fourth-to-first transition"),
    "assign-step2": ("assignment", [18, 23], "holding frame zero of the\n   existing PixelLab-produced Working sheet"),
    "assign-step3": ("assignment", [24, 31], "Add explicit reduced-motion mapping and live preference-switch acceptance"),
    "assign-step4": ("assignment", [32, 43], "respect prefers-reduced-motion and changes while open"),
    "assign-step6": ("assignment", [52, 58], "switching the preference in the same session"),
    "stage-assembly": ("authoring-stage", [31, 32], "retain the\nexact intended frame-selection/assembly policy and its separate review obligations"),
    "assign-step4-reuse": ("assignment", [40, 43], "Reuse reviewed existing art when it satisfies the new criteria"),
    "sv-live-sample": ("succ-view", [157, 157], "elapsed: performance.now() - origin"),
    "sc-live-single": ("succ-check", [140, 140], "live frame agrees with elapsed time (frame-boundary tolerance)"),
    "sc-switch-running-only": ("succ-check", [180, 180], "r[\"state\"] == \"running\""),
    "sc-phase-map": ("succ-check", [67, 69], "\"normal-start\": \"normal\", \"reduced\": \"reduced\", \"normal-restored\": \"normal\""),
    "cont-scope": ("continuation", [9, 14], "Do not adopt/rewrite production,\nrun a renderer, or create new art acceptance"),
    "cont-no-pass": ("continuation", [27, 27], "Do not turn retained"),
    "queue-state": ("queue-ts", [1, 3], "started: \"running\""),
    "view-idle": ("view-ts", [3, 3], "idle: { label: \"Start\", path: \"assets/start.svg\", frames: 1 }"),
    "view-display": ("view-ts", [9, 9], "frameMs: 100, background: \"#172336\""),
    "view-consumers": ("view-ts", [10, 11], "export function compactStatus(state: QueueState) { return statusVisuals[state]; }"),
    "succ-idle": ("successor-ts", [7, 7], "idle: { label: \"Start\", path: \"assets/start.svg\", frames: 1, still: 0 }"),
    "succ-running": ("successor-ts", [8, 8], "running: { label: \"Working\", path: \"assets/working.png\", frames: 4, still: 0 }"),
    "succ-display": ("successor-ts", [13, 13], "frameMs: 100, background: \"#172336\""),
    "succ-still-comment": ("successor-ts", [14, 14], "`still` is the cell held when motion is reduced"),
    "succ-motion": ("successor-ts", [17, 19], "globalThis.matchMedia?.(reducedMotionQuery)"),
    "succ-describe": ("successor-ts", [20, 23], "holdFrame: animate ? null : visual.still"),
    "succ-frameat": ("successor-ts", [24, 26], "descriptor.holdFrame ?? 0"),
    "succ-consumers": ("successor-ts", [27, 28], "export function compactStatus(state: QueueState, motion: MotionPreference = motionPreference())"),
    "sv-session": ("succ-view", [8, 8], "const sessionId = crypto.randomUUID()"),
    "sv-paint": ("succ-view", [41, 52], "context.drawImage(asset.image, frame * width, 0, width, height, 0, 0, width * scale, height * scale)"),
    "sv-elapsed-default": ("succ-view", [56, 56], "elapsed = 0"),
    "sv-label": ("succ-view", [62, 62], "label.textContent = descriptor.label"),
    "sv-paint-at-creation": ("succ-view", [69, 69], "info.frame = paint(canvas, asset, descriptor, scale, elapsed)"),
    "sv-refresh": ("succ-view", [80, 87], "Re-derive a tracked cell from the same consumer under the current preference and repaint it in place"),
    "sv-change": ("succ-view", [114, 121], "media.addEventListener('change'"),
    "sv-animate": ("succ-view", [123, 130], "requestAnimationFrame(animate)"),
    "sv-timeline": ("succ-view", [141, 149], "timeline.push("),
    "sc-modules": ("succ-check", [51, 52], "fixture did not execute the retained original consumer module"),
    "sc-session": ("succ-check", [58, 59], "all phases observed in one open page session"),
    "sc-descriptor": ("succ-check", [81, 86], "hold frame is the declared still cell when stationary"),
    "sc-compositing": ("succ-check", [105, 112], "source pixels and alpha compositing (rounding tolerance one)"),
    "sc-identical": ("succ-check", [126, 131], "both consumers return the identical running descriptor under this preference"),
    "sc-live": ("succ-check", [133, 146], "live cell holds the still cell under reduced motion"),
    "sc-timeline": ("succ-check", [148, 166], "normal motion cycles through all four cells including the wrap"),
    "sc-switch": ("succ-check", [170, 190], "every Working cell stopped on the held cell without reload"),
    "sc-scope": ("succ-check", [191, 192], "it does not judge whether the held cell reads as Working"),
    "cap-phases": ("succ-capture", [4, 5], "as-launched (no emulation; use with --chrome-flag --force-prefers-reduced-motion"),
    "cap-emulate": ("succ-capture", [68, 68], "Emulation.setEmulatedMedia"),
    "cap-scope": ("succ-capture", [98, 98], "Mechanical fixture evidence only"),
    "si-pixelated": ("succ-index", [21, 21], "image-rendering: pixelated"),
    "state-candidate": ("state", [259, 259], "dg=~64:cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc"),
    "state-style-choice": ("state", [392, 392], "not_fixed=[~9:exact hex,~13:palette count,~12:binary alpha,~12:stroke width,~7:margins,~28:check motif for other states]"),
}
locators = {}
for lid, (sid, (a, b), expected) in LOCATORS.items():
    text = "\n".join(lines_of(sources[sid]["path"])[a - 1 : b])
    if expected not in text:
        sys.exit(f"locator {lid} failed: {sources[sid]['path']} lines {a}-{b} do not contain {expected!r}")
    locators[lid] = {"source": sid, "lines": [a, b], "expected_wording": expected, "verified": True}

# ---------------------------------------------------------------- identities
ctx_by = {c["id"]: c for c in context["criteria"]}
exp_by = {c["id"]: c for c in export["criteria"]}
r2_by = {c["criterion"]: c for c in r2["criteria"]}
prior_by = {c["criterion"]: c for c in prior["criterion_comparisons"]}
map_by = {m["original_id"]: m for m in proposal["mapping"]}
prop_by = {c["id"]: c for c in proposal["criteria"]}
assert len(ctx_by) == len(exp_by) == len(r2_by) == len(prior_by) == len(map_by) == 20
assert len(prop_by) == 29
for oid, c in ctx_by.items():
    assert c["record_sha256"] == exp_by[oid]["record_sha256"] == exp_by[oid]["current_record_sha256"]
    assert c["record_sha256"] == r2_by[oid]["record_sha256"] == prior_by[oid]["record_sha256"] == map_by[oid]["record_sha256"]
    assert c["fields"]["ck"] == exp_by[oid]["check"] == map_by[oid]["original_check"] == r2_by[oid]["original_check"]
carried = {}
for c in proposal["criteria"]:
    for k in c.get("carries") or []:
        carried.setdefault(k["id"], []).append(c["id"])
for oid, m in map_by.items():
    assert sorted(m["carried_by"]) == sorted(carried[oid]), oid
production = plar_read["production"]
continuation = production["continuation"]
assert continuation["state_hash"] == export["state"]["sha256"] == "3484cf385c91c8c28fa04316fb2c7c5b52c740178b505ccbd88631f57c893c9b"
job = continuation["jobs"][0]
assert job["id"] == "authoring-01.working.join-01" and job["state"] == "prepared" and job["remote_id"] is None

identities = {
    "proposal": {"path": PROPOSAL, "sha256": EXPECTED_PROPOSAL_SHA},
    "specialist_report": {"path": REPORT, "sha256": sha(REPORT)},
    "context_packet": {"path": CONTEXT, "sha256": sha(CONTEXT), "criteria": 20, "sources": len(context["sources"])},
    "state": {"path": ".pixl/assets/queue.ready/state.px", "sha256": continuation["state_hash"], "revision": export["state"]["revision"], "validate_records": 412},
    "requirements_hash": {
        "current_selection": plar_read["requirements_hash"],
        "bound_in_plan_and_job": "e0614bd962a53a19003707f3d73326be436891e198eb1e4a262f12412fbfb027",
        "selection_status": "changed",
    },
    "plar_file_hash": plar_read["hash"],
    "plan": export["plan"],
    "job": {
        "id": job["id"], "state": job["state"], "remote_id": job["remote_id"], "next_action": job["next_action"],
        "tool": job.get("tool"), "intent_sha256": proposal["reduced_motion_design"]["job_identity_preserved"]["intent_sha256"],
        "note": "untouched by this review; its resolution route (local failed observation, no remote id) belongs to a later production step, not to this comparison",
    },
    "review_scope_sha256": export["review_scope_sha256"],
    "review_scope_equals_prior_caller_comparison": export["review_scope_sha256"] == prior["review_scope_sha256"],
    "production_continuation_action": continuation["action"],
    "new_request_allowed": production.get("new_request_allowed"),
}

# ---------------------------------------------------------------- caller verification of the proposal's own facts
report_checks = {"citations_total": len(report["verification"]), "citations_failed": 0}
for v in report["verification"]:
    seg = "\n".join(lines_of(v["path"])[v["lines"][0] - 1 : v["lines"][1]])
    if v["expected_wording"] not in seg:
        report_checks["citations_failed"] += 1
source_hash_mismatches = [k for k, s in proposal["sources"].items() if not os.path.exists(s["path"]) or sha(s["path"]) != s["sha256"]]
caller_verification = {
    "proposal_source_hashes": {"declared": len(proposal["sources"]), "mismatches": source_hash_mismatches},
    "specialist_citations_rerun": report_checks,
    "twenty_original_rows": "ids, record hashes, literal checks and domain/mode identical across the context packet, the fresh request-review export, r2, the prior caller comparison and the proposal mapping; record hashes also match pixl_validate record_hashes (state revision 88)",
    "carried_by_inverse_of_carries": True,
    "six_new_criteria_carry_nothing": sorted(cid for cid, c in prop_by.items() if not c.get("carries")),
    "reuse_provenance": "state.px line 259: live.working-animation-motion-01.candidate dg = cf101610... equals sha256(assets/working.png); artifact file present",
    "measurements": measurements,
    "render_01_status": "work/focused-successor/render-01 holds launch.json, browser-process.json and 41 PNG views but no render.json; renderer-successor/check.py has never run on a successor capture; launch.json project root points at C:/github/pixel-lab-agent/evidence/focused-authoring/20261109/native/claude-01/project, not this consumer root",
    "visual_observation": {
        "mode": "caller viewing of the specialist's composite PNGs (not fixture captures); observation only, not acceptance; does not convert any unavailable check into a pass (CONTINUATION-ASSIGNMENT.md line 27)",
        "viewed": [
            {"path": "work/focused-successor/specialist-views/specialist-pair-w0-retry-ready-paused.png", "sha256": sha("work/focused-successor/specialist-views/specialist-pair-w0-retry-ready-paused.png")},
            {"path": "work/focused-successor/specialist-views/specialist-family-color-12x.png", "sha256": sha("work/focused-successor/specialist-views/specialist-family-color-12x.png")},
            {"path": "work/focused-successor/specialist-views/specialist-family-gray-3x.png", "sha256": sha("work/focused-successor/specialist-views/specialist-family-gray-3x.png")},
            {"path": "work/focused-successor/specialist-views/specialist-family-color-1x.png", "sha256": sha("work/focused-successor/specialist-views/specialist-family-color-1x.png")},
        ],
        "findings": [
            "Held cell (W0) reads as three short arc segments around an empty centre, a broken ring; Ready is one continuous asymmetric check; Paused is two solid bars. At 3x and 12x, colour and grayscale, the three are not confusable by silhouette. Agrees with the specialist's preliminary finding; still preliminary.",
            "Retry is the closest neighbour: a heavier near-closed ring with an arrowhead. At 3x grayscale W0 and Retry separate by mass and by the three gaps; at 1x (the 1x composite) all four Working cells and Retry are small round blobs and the difference is subtle. The decisive view must be the native-scale fixture capture, which does not exist yet.",
            "Frozen, W0 does not convey motion; with the Working label beside it the cell reads as busy/in progress by idiom; without the label it could read as stalled. No source requires motion from the stationary symbol; this is a recorded limit, not a failure of PLAR line 422.",
            "No matte, plate or fringe is visible in any member on the composites; exterior pixels show the panel. This is consistent with the measured alpha histograms but is not the visual acceptance review, which needs saved native/enlarged fixture views.",
        ],
    },
}

# ---------------------------------------------------------------- evidence classes shared by rows
EVIDENCE = {
    "mechanical": "local decode/measurement of retained bytes (pixl_asset_check or Pillow); decides only what it measures",
    "visual": "caller viewing of saved native and enlarged views on #172336 (fixture captures or pixl_inspection views); decides readability, meaning, matte, coherence",
    "temporal": "actual playback/frame-sequence evidence: capture timeline frame indices and observed cycling; wall-clock duration is not measured; viewing of playback remains visual",
    "destination": "fixture execution of the actual modules at the destination: served-file hashes, descriptors through both consumers, canvas geometry, compositing, screenshot placement, preference switch",
}
NO_EVIDENCE = "none retained: successor capture never completed (no render.json), check.py never run"
PRELIM = "specialist preliminary views only (specialist-views/*.png); caller observation above; no fixture views; not acceptance"
MEASURED = "caller reproduced the measurement independently (caller-measurements.json)"

# ---------------------------------------------------------------- the 29 proposed rows: caller dispositions
P = {}


def row(cid, *, split, obligation, delta, alternative, disposition, correction, evidence, status, carries_note=None):
    c = prop_by[cid]
    P[cid] = {
        "id": cid,
        "check": c["check"],
        "domain": c["domain"],
        "mode": c["mode"],
        "labelled_authority": c["authority"],
        "labelled_scope": c["scope"],
        "carries": c.get("carries") or [],
        "caller_authority_split": split,
        "source_obligation": obligation,
        "literal_delta": delta,
        "discriminating_alternative": alternative,
        "disposition": disposition,
        "correction": correction,
        "evidence_class": evidence,
        "evidence_route": [EVIDENCE[e] for e in evidence],
        "evidence_status": status,
        "carry_note": carries_note,
    }


row("successor-01.working.q.geometry",
    split=[
        {"clause": "64x16, four horizontal 16x16 cells at x=0,16,32,48, no gutters or added canvas", "class": "owner requirement", "locators": ["brief-cells", "brief-working", "plar-geometry"]},
        {"clause": "transparent margin inside a cell is composition, not padding", "class": "clarification adopted by the prior caller (r2 geometry); it removes nothing the brief requires", "locators": ["brief-working"]},
        {"clause": "frames 4 unchanged under either preference", "class": "owner requirement (four frames) read with the caller update (a hold does not change the sheet)", "locators": ["brief-working", "plar-purpose"]},
        {"clause": "successor module declares frames 4 / cell [16,16] / frameMs 100; fixture draws only when width == 16*frames; frameAt() derivation", "class": "consumer-code fact of the PROPOSED successor module and fixture (design proposal), observation", "locators": ["succ-running", "succ-display", "succ-frameat", "sv-paint"]},
    ],
    obligation="BRIEF line 3 fixes 16x16 status cells and four horizontal frames at 100 ms; the view slices 16-wide cells. The brief leaves in-cell composition open.",
    delta="Adds the proposed successor module and fixture as the geometry basis in place of the original module; carries the r2 'padding = added canvas' clarification; adds 'unchanged under either preference'. No owner outcome dropped.",
    alternative="A 64x16 sheet whose marks sit inside 2-px transparent in-cell margins: accepted (correct). A 72x16 sheet with 2-px gutters: rejected (correct; the consumer slices frame*16).",
    disposition="keep", correction="Label the successor-module/fixture clauses as observations of the proposed destination rather than owner authority (C3). No wording change needed.",
    evidence=["mechanical"], status=MEASURED + ": 64x16, fractional alpha 0")

row("successor-01.working.q.transparent-exterior-measured",
    split=[
        {"clause": "retain alpha histogram and exact RGBA component boxes; FLAG four-edge or >half-cell components for visual review; flag is not a rejection", "class": "measured fact / diagnostic (observation) per prior caller decision D1", "locators": ["brief-transparent"]},
        {"clause": "RGB of alpha-0 pixels is not significant", "class": "observation (prior caller measurement)", "locators": ["brief-transparent"]},
        {"clause": "mechanical REJECTION decidable only under the seed-rotation construction: cell alpha == alpha of cw^k(seed)", "class": "scoped expert choice (proposal, seed-rotation construction only), not an observation", "locators": ["brief-transparent"]},
    ],
    obligation="BRIEF line 3 'transparent backgrounds': the exterior must be transparent; the brief does not fix binary alpha, a construction or a mechanical proxy.",
    delta="Faithful to r2/D1 (flag not rejection; visual record decides). Adds the explicit rotation formula and the 32 alpha-255 count, both measured facts of this seed.",
    alternative="A brief-conforming anti-aliased Working design with partial-alpha edge pixels and a transparent exterior: not rejected by this record (correct, since the rejection form applies only under the rotation construction).",
    disposition="keep", correction="The single 'observation' label is mixed: the construction-scoped rejection clause is a proposal. Record both classes in the corrected proposal (C6).",
    evidence=["mechanical"], status=MEASURED + ": cell 0 alpha {0:224,255:32}; components [5,3,10,5]/[12,6,14,11]/[3,10,8,14]; cells 1-3 equal cw^k(cell 0) on alpha and visible RGBA; cell 0 equals the accepted seed")

row("successor-01.working.q.transparent-exterior-visual",
    split=[
        {"clause": "exterior of every frame including the held cell shows the panel with no unintended matte, tile, plate, halo or fringe", "class": "owner requirement (deciding visual rule, D1)", "locators": ["brief-transparent", "brief-inspect"]},
        {"clause": "a deliberate opaque backing shape is acceptable only when part of the mark's recorded design", "class": "clarification from the profile's visual-role distinction; removes an unsupported blanket 'no plate'", "locators": ["brief-transparent"]},
        {"clause": "partial alpha permitted; binary alpha not required", "class": "owner non-restriction (brief) and adopted style not_fixed list", "locators": ["brief-transparent", "state-style-choice"]},
    ],
    obligation="BRIEF line 3 'transparent backgrounds' judged at 1x and 3x on the dark panel.",
    delta="Same as r2's visual record; adds 'including the held cell when stationary' (the held cell is cell 0, already a frame) and demotes the 193-pixel grey matte to an example of the failure class.",
    alternative="A mark with a deliberate opaque badge and transparent exterior: accepted when recorded as design (correct). A full-cell grey tile: rejected (correct).",
    disposition="keep", correction=None,
    evidence=["visual"], status=PRELIM)

row("successor-01.working.q.frame-assembly",
    split=[
        {"clause": "reuse case: no assembly; record must name exact candidate bytes and provenance", "class": "assignment requirement (reuse reviewed art; no silent rebind) and evidence discipline", "locators": ["assign-step4-reuse"]},
        {"clause": "future assembly: exact source frames in play order; lossless = identical alpha and identical RGBA where alpha>0; no undocumented duplication or silent frame drop; raw outputs retained", "class": "process requirement whose actual source is AUTHORING-STAGE.md lines 31-32, not FOCUSED-SUCCESSOR lines 40-43 as cited (locator defect, C11); r2 bounds applied", "locators": ["stage-assembly", "brief-working"]},
        {"clause": "cells equal cw^k(seed)", "class": "scoped expert choice (construction), correctly listed as an expert clause", "locators": ["brief-working"]},
    ],
    obligation="FOCUSED-SUCCESSOR step 4 requires reuse of reviewed existing art when it satisfies the criteria and no silent rebinding; BRIEF line 3 fixes four frames. The owner brief says nothing about assembly records.",
    delta="Specialises the r2 text to the reuse case (vacuous assembly) and keeps the conditional rule for a future provider result.",
    alternative="A future five-frame provider result assembled to four cells with a documented repeated phase: accepted when the record says so (correct).",
    disposition="clarify", correction="Add AUTHORING-STAGE.md to the source index and cite lines 31-32 for the assembly-policy clause; keep FOCUSED-SUCCESSOR lines 40-43 for the reuse authorisation only (C11, verified by the caller after the specialist's S3).",
    evidence=["mechanical"], status=MEASURED + "; provenance verified at state.px line 259")

row("successor-01.working.q.activity-not-success",
    split=[
        {"clause": "the running loop reads as ongoing activity and not as completion; no check mark or success-like terminal pose", "class": "owner requirement", "locators": ["brief-activity", "brief-ready", "plar-meaning"]},
        {"clause": "each individual frame reads as activity", "class": "mixed: owner/caller-update requirement for the held frame (PLAR 422: the stationary symbol is shown alone); scoped expert extension for the other frames (shown singly for 100 ms)", "locators": ["plar-purpose", "sv-paint-at-creation", "sv-elapsed-default"]},
        {"clause": "beside the exact Ready baseline as the comparison method", "class": "method (proposal), disclosed", "locators": ["brief-inspect"]},
        {"clause": "avoid frames resembling Start arrowhead or pause bars", "class": "scoped expert clause, correctly separated from the check (r2)", "locators": ["brief-start"]},
    ],
    obligation="BRIEF line 3 binds the loop; PLAR line 422 binds the stationary held symbol; neither binds every transient frame of normal motion.",
    delta="Keeps r2's loop/frame wording; the basis discloses per-frame reading as an expert extension but the check labelled 'requirement' still binds every frame.",
    alternative="A loop in which one 100 ms transient frame momentarily resembles a check while the loop and the held cell clearly read as activity: satisfies the owner obligation; the literal per-frame clause rejects it.",
    disposition="clarify", correction="Scope the per-frame clause: binding for the held cell (caller update) and for the loop (owner); expert clause for the remaining transient frames (C4).",
    evidence=["visual"], status=PRELIM)

row("successor-01.working.q.motion-continuity",
    split=[
        {"clause": "under normal motion play the four frames at 100 ms including the wrap; one continuous activity loop with no visible wrap discontinuity", "class": "owner requirement (D2 applied)", "locators": ["brief-working", "plar-animation", "plar-delivery", "succ-display"]},
        {"clause": "all four frames remain in the sheet and in play under normal motion; the hold does not remove or reorder them", "class": "owner requirement read with the caller update", "locators": ["brief-working", "plar-purpose"]},
        {"clause": "stable centre/anchor and volume; evenly paced, no near-hold; stable cluster count, no morphing", "class": "scoped expert clauses (correctly outside the check); pacing is not the owner's 100 ms requirement", "locators": ["brief-working"]},
    ],
    obligation="BRIEF line 3: four frames at 100 ms forming a working loop that communicates activity. The brief does not require equal motion increments.",
    delta="D2 applied faithfully; adds the reduced-motion non-removal sentence.",
    alternative="An unevenly paced but continuous loop: accepted by the check (correct); it is judged only by the expert clause.",
    disposition="clarify", correction="Name the route for the actual-playback leg: caller viewing of the live fixture page under normal motion at 1x and 3x recorded as a visual observation (a frame-sequence preview may aid viewing but is not fixture evidence); the timeline stills and frameMs constant are mechanical legs only (C10).",
    evidence=["temporal", "visual"], status=NO_EVIDENCE + "; no artefact or named route for viewing actual playback exists yet")

STYLE_SPLIT = [
    {"clause": "readable silhouette(s); perceptible cool-blue accent related to the Ready baseline and the Start accent; judged at 1x and 3x on #172336", "class": "owner requirement (colour role is perceptibility, not extent)", "locators": ["brief-transparent", "brief-inspect", "view-display"]},
    {"clause": "compact; deliberate coherent clusters and stepped edges consistent with the exact Ready baseline", "class": "adopted scoped caller decision (render.choice.style, state.px line 392; authoring-plar approved_style_reference), not the original brief", "locators": ["state-style-choice", "plar-style"]},
    {"clause": "selective intentional anti-aliasing permitted under the full-alpha contract; accidental blur or noise is not", "class": "clarification preserving the adopted not_fixed list (binary alpha not fixed)", "locators": ["state-style-choice"]},
    {"clause": "no exact hex, palette count, binary alpha, stroke width or margin rule", "class": "explicit non-restriction (observation)", "locators": ["state-style-choice"]},
]
for cid, member in [("successor-01.working.q.style-coherence", "Working sheet including the held cell"), ("successor-01.retry.q.style-coherence", "Retry"), ("successor-01.paused.q.style-coherence", "Paused")]:
    row(cid, split=STYLE_SPLIT,
        obligation="BRIEF line 3: readable silhouettes and the existing cool blue accent with no fixed palette, inspected at 1x and 3x on the dark panel; the exact Ready baseline is a scoped adopted project choice.",
        delta="Identical to r2 except 'silhouette(s)'; selective anti-aliasing explicitly permitted. " + ("Held cell added to the scope." if "working" in cid else "No change of scope."),
        alternative="A member with two intentional anti-aliased edge pixels: accepted (correct). A member whose accent is a thin perceptible blue highlight on a neutral body: accepted (correct; role not extent).",
        disposition="keep", correction="Record the mixed authority (owner + adopted scoped decision) per clause instead of one 'requirement' label (C3). Scope: " + member + ".",
        evidence=["visual"], status=PRELIM)

row("successor-01.working.q.consumers-normal-motion",
    split=[
        {"clause": "started -> running through stateAfter; both statusCell and compactStatus; label Working; assets/working.png; frames 4; 100 ms; nearest sampling at 1 and 3; compositing on #172336", "class": "consumer-code fact of the ORIGINAL module and owner brief (requirement)", "locators": ["queue-state", "view-display", "view-consumers", "brief-working", "brief-inspect"]},
        {"clause": "identical descriptor {still 0, motion normal, animate true, holdFrame null}", "class": "consumer-code fact of the PROPOSED successor module (caller design proposal); scoped to this destination", "locators": ["succ-running", "succ-describe", "succ-consumers"]},
        {"clause": "fixture renderer-successor/view.mjs + check.py as the evidence route; timeline frame indices 0,0,1,1,2,2,3,3,0 at the sample points; wall-clock not claimed", "class": "evidence route (method) bounded correctly (r2) for the synthetic timeline", "locators": ["sv-paint", "sv-animate", "sv-timeline", "sc-identical", "sc-timeline", "si-pixelated"]},
        {"clause": "the live requestAnimationFrame loop is observed cycling through all four cells", "class": "overclaimed evidence: the fixture samples each live cell once and check.py tests that single frame against elapsed with a boundary tolerance; cycling through all four cells is asserted only on the synthetic timeline (C10)", "locators": ["sv-live-sample", "sc-live-single", "sc-timeline"]},
    ],
    obligation="BRIEF line 3 timing/frames and inspection scales; both consumers share one running descriptor (original module lines 10-11).",
    delta="Replaces the original fixture/module with the successor ones and adds the successor descriptor fields; frame-advance evidence stays bounded to indices, except the 'live loop observed cycling' sentence, which the checker does not establish.",
    alternative="A successor mapping without a `still` field (M1 separate static file) that still shows four frames at 100 ms through both consumers: satisfies the owner obligation; the literal descriptor clause rejects it. A live loop that stalls after the first paint while the synthetic timeline is correct: passes every check.py assertion, so the 'observed cycling' clause has no checker support.",
    disposition="clarify", correction="Scope the descriptor-field clause to the proposed successor destination (C3); reword the live-loop sentence to what check.py asserts (one live sample agrees with elapsed; the synthetic timeline cycles 0..3 with the 400 ms wrap) and route actual cycling to visual viewing of the live page or a multi-sample observation (C10).",
    evidence=["destination", "temporal"], status=NO_EVIDENCE)

row("successor-01.working.q.stationary-cell-identity",
    split=[
        {"clause": "the stationary symbol is cell 0 (crop 0,0,16,16) = statusVisuals.running.still", "class": "scoped expert choice (specialist proposal P1) bound to the caller's successor design (still: 0); not an observation and not owner authority", "locators": ["succ-running", "succ-still-comment", "assign-step2"]},
        {"clause": "visible 32 px; components [5,3,10,5]/[12,6,14,11]/[3,10,8,14]; visible box [3,3,14,14]; centroid [7.906,9.0]; alpha {0:224,255:32}; equals accepted seed", "class": "measured facts (zero-based, half-open, pixel-edge centres)", "locators": ["succ-frameat", "sv-paint"]},
        {"clause": "if still changes the identity record and visual verdicts must be redone", "class": "process rule (review discipline), sound", "locators": ["succ-describe"]},
    ],
    obligation="PLAR line 422 requires a stationary Working symbol; it does not name the symbol. FOCUSED-SUCCESSOR lines 18-23 offer frame zero as a proposed implementation.",
    delta="New criterion. Binds the visual verdicts to the exact pixels painted, which is sound review discipline.",
    alternative="Holding cell 2 or a new static glyph: satisfies PLAR 422; this record would simply be re-measured, so nothing valid is rejected.",
    disposition="clarify", correction="Label the cell choice 'proposal' and the numbers 'observation' (C5); keep as the identity record.",
    evidence=["mechanical"], status=MEASURED)

row("successor-01.working.q.stationary-distinct-ready-paused",
    split=[
        {"clause": "held cell distinguishable from Ready and from Paused by shape or structure alone", "class": "caller update requirement (PLAR 422 / AUTHORING-UPDATE 2-4) read with BRIEF line 7 non-colour distinction", "locators": ["plar-purpose", "update-req", "brief-paused", "brief-keep"]},
        {"clause": "does not read as completion or as pause", "class": "owner requirement (without looking like success) and the natural reading of 'distinguishable from Paused'", "locators": ["brief-activity", "plar-purpose-nosuccess"]},
        {"clause": "grayscale or binarized silhouettes as the non-colour method", "class": "method (proposal), disclosed", "locators": ["brief-inspect"]},
    ],
    obligation="PLAR line 422: stationary Working symbol distinguishable from Ready and Paused; BRIEF line 7: distinction without relying on colour alone.",
    delta="New criterion; adds nothing beyond the update and brief.",
    alternative="A stationary symbol distinct from Ready and Paused only by hue: rejected (correct per BRIEF line 7).",
    disposition="keep", correction="Label the authority as caller update (authoring branch), not original owner brief (C3).",
    evidence=["visual"], status=PRELIM)

row("successor-01.working.q.stationary-distinct-retry-start",
    split=[
        {"clause": "held cell distinguishable by shape or structure alone from Retry; does not read as failure/retry", "class": "owner requirement by direct reading: BRIEF line 3 'Error/retry must be distinguishable without color alone' over the statuses shown, and the held cell is now a shown status", "locators": ["brief-retry", "plar-purpose"]},
        {"clause": "distinguishable from the preserved Start triangle; does not read as the Start control", "class": "inference (shared-consumer): idle resolves to Start in the same status cells through both consumers; not an owner line (D4)", "locators": ["view-idle", "view-consumers", "succ-idle", "succ-consumers"]},
    ],
    obligation="BRIEF line 3 states the Retry non-colour distinction; nothing in the brief names Start as a compared status, but the view shows it in the same cells.",
    delta="New criterion. The `authority` field says 'requirement' while the basis says 'inference, not an owner line'; the two clauses have different authority.",
    alternative="A held cell with the Retry ring silhouette in blue: rejected by the Retry clause (correct). A held cell shaped like a right-pointing triangle: rejected only by the Start clause, whose basis is the shared-consumer inference.",
    disposition="correct", correction="Split into two labelled clauses: Retry = requirement (BRIEF line 3); Start = inference (shared-consumer, as in D4). Answer to the specialist's second question: adopt both, with those labels (C2).",
    evidence=["visual"], status=PRELIM + "; closest pair, decisive at native 1x on the fixture")

row("successor-01.working.q.stationary-meaning",
    split=[
        {"clause": "held cell reads as the Working status's own symbol: not success (no check mark or terminal pose), not pause", "class": "owner requirement and caller update", "locators": ["plar-purpose-nosuccess", "brief-activity", "plar-purpose"]},
        {"clause": "with its consumer label present", "class": "consumer-code fact of the fixture (label rendered beside the glyph); context for viewing, not a substitute for the glyph's own reading", "locators": ["sv-label"]},
        {"clause": "it is recognisably one phase of the Working loop so that switching the preference changes motion, not identity", "class": "scoped expert choice (specialist proposal P1) promoted into a requirement-labelled check", "locators": ["assign-step2"]},
    ],
    obligation="PLAR line 422 and BRIEF line 3: the stationary symbol must not imply success and must be distinguishable from Ready and Paused. No source requires it to be a phase of the loop or to convey motion.",
    delta="New criterion. Adds the phase-of-the-loop identity clause to the check.",
    alternative="P2, a new static three-dot glyph distinct from Ready/Paused and not success-like: satisfies the owner obligation; the literal check rejects it because it is not a phase of the loop.",
    disposition="correct", correction="Move the phase-identity clause to the expert clause set (where it already appears) and keep the required outcome: reads as Working's own symbol, not success, not pause, judged on the glyph with the label as context (C1, C7).",
    evidence=["visual"], status=PRELIM + "; frozen-spinner 'stalled' reading is a recorded limit, not a failure")

row("successor-01.working.q.reduced-motion-consumer-mapping",
    split=[
        {"clause": "under reduced motion both consumers return one identical descriptor and every Working cell paints the held cell; sheet geometry unchanged; static members unaffected", "class": "caller update requirement ('confirm its consumer mapping') plus owner outcome that both consumers share one asset", "locators": ["plar-purpose", "update-req", "view-consumers"]},
        {"clause": "preference source is matchMedia('(prefers-reduced-motion: reduce)') through motionPreference(); explicit argument overrides", "class": "assignment requirement (respect prefers-reduced-motion) implemented as consumer-code of the PROPOSED successor module", "locators": ["assign-step4", "succ-motion", "succ-consumers"]},
        {"clause": "descriptor fields {still 0, motion reduced, animate false, holdFrame 0}; frame 0 at every timeline sample; no animation loop repaints", "class": "consumer-code fact of the PROPOSED successor module and fixture (design proposal, M2-style); scoped to this destination", "locators": ["succ-running", "succ-describe", "succ-frameat", "sv-paint", "sc-descriptor", "sc-identical", "sc-live", "sc-timeline"]},
    ],
    obligation="PLAR line 422: confirm the consumer mapping of the stationary symbol; FOCUSED-SUCCESSOR step 4: both consumers, respect prefers-reduced-motion. The sources leave the mapping mechanism (descriptor field, separate file, state) open.",
    delta="New criterion. Binds the specific M2-style descriptor design.",
    alternative="M1: a separate static file selected by a different descriptor path under reduced motion, through both consumers: satisfies the update and assignment; the literal descriptor clause rejects it.",
    disposition="clarify", correction="Keep the outcome clauses as requirement; scope the descriptor-field clauses to the proposed successor destination and label them consumer-code of a design proposal (C3). M1 remains an open, untested alternative.",
    evidence=["destination"], status=NO_EVIDENCE + "; the as-launched (--force-prefers-reduced-motion) run is also outstanding")

row("successor-01.working.q.live-preference-switch",
    split=[
        {"clause": "changing the preference in the same page session repaints every Working cell in both consumers in place (held cell when reduced, cycling when normal), no reload, one sessionId, change event recorded", "class": "assignment requirement (FOCUSED-SUCCESSOR lines 31, 39, 54), correctly attributed; not an owner line", "locators": ["assign-step3", "assign-step4", "assign-step6"]},
        {"clause": "fixture change listener/refresh, sessionId, checker [switch] observations, DevTools emulation", "class": "evidence route (fixture/checker/capture code), observation", "locators": ["sv-change", "sv-refresh", "sv-session", "sc-switch", "sc-session", "cap-phases", "cap-emulate", "cap-scope"]},
    ],
    obligation="FOCUSED-SUCCESSOR requires respecting changes while open and switching the preference in the same session.",
    delta="New criterion; faithful to the assignment.",
    alternative="A successor that applies the preference only at page load: rejected (correct per the assignment). A regression that repaints Ready wrongly on the change event, or a startup path that ignores a forced launch preference: passes check.py, because its [switch] block inspects only running cells and its phase map covers only the three default phases.",
    disposition="clarify", correction="'Other states repaint unchanged' and the as-launched forced-reduced run have no checker assertion (check.py lines 180 and 67-69); either add those assertions or label the clauses as caller visual observations on the reduced-phase screenshot (C12).",
    evidence=["destination", "temporal"], status=NO_EVIDENCE)

for cid, member, png in [("successor-01.retry.q.geometry", "Retry", "assets/error-retry.png"), ("successor-01.paused.q.geometry", "Paused", "assets/paused.png")]:
    row(cid, split=[
            {"clause": "exactly one static 16x16 frame; no strip, animation or extra canvas", "class": "owner requirement", "locators": ["brief-cells", "brief-static", "brief-keep"]},
            {"clause": "consumer frames 1; fixture geometry gate", "class": "consumer-code fact (original and successor modules agree), observation", "locators": ["succ-idle", "sv-paint"]},
        ],
        obligation="BRIEF line 3: 16x16 cells, Ready and Retry static; line 7: keep existing display requirements for Paused.",
        delta="Only the file name replaces 'the delivered PNG'. Prior caller disposition keep.",
        alternative="A 16x16 PNG with in-cell transparent margins: accepted (correct).",
        disposition="keep", correction=None,
        evidence=["mechanical"], status=MEASURED + f": {png} 16x16")

for cid, member in [("successor-01.retry.q.transparent-exterior-measured", "Retry"), ("successor-01.paused.q.transparent-exterior-measured", "Paused")]:
    row(cid, split=[
            {"clause": "retain alpha histogram and component boxes; FLAG four-edge or >half-cell components; not a rejection", "class": "measured fact / diagnostic (observation), D1", "locators": ["brief-transparent"]},
            {"clause": "no mechanical rejection decidable for a static member", "class": "observation (correct: no construction fixes its alpha set)", "locators": ["brief-transparent"]},
        ],
        obligation="BRIEF line 3 'transparent backgrounds'; no mechanical proxy is required by the owner.",
        delta="Faithful to r2/D1 for a static member.",
        alternative="A corner-to-corner X with transparent exterior: flagged for visual review, not rejected (correct).",
        disposition="keep", correction=None,
        evidence=["mechanical"], status=MEASURED + (": alpha {0:202,255:54}, one component [3,2,13,14]" if member == "Retry" else ": alpha {0:196,255:60}, two 30-px components [4,3,7,13] and [9,3,12,13]"))

for cid in ["successor-01.retry.q.transparent-exterior-visual", "successor-01.paused.q.transparent-exterior-visual"]:
    row(cid, split=[
            {"clause": "exterior shows the panel with no unintended matte, tile, plate, halo or fringe at 1x and 3x", "class": "owner requirement (deciding visual rule, D1)", "locators": ["brief-transparent", "brief-inspect"]},
            {"clause": "deliberate backing acceptable when recorded; partial alpha permitted", "class": "clarification and owner non-restriction", "locators": ["brief-transparent", "state-style-choice"]},
        ],
        obligation="BRIEF line 3 'transparent backgrounds' at the inspection scales.",
        delta="Same as r2's visual record; the magenta intermediate becomes an example rather than the rule.",
        alternative="A mark with a deliberate recorded badge: accepted (correct).",
        disposition="keep", correction=None,
        evidence=["visual"], status=PRELIM)

for cid, member, loc in [("successor-01.retry.q.retry-meaning-without-color", "Retry", "brief-retry"), ("successor-01.paused.q.pause-meaning-without-color", "Paused", "brief-paused")]:
    row(cid, split=[
            {"clause": f"{member} reads as its meaning and is identifiable by shape alone against Ready, every Working frame including the held cell, and the other delivered member", "class": "owner requirement (BRIEF line 3 for Retry, line 7 for Paused); the held cell joins the compared set through the caller update", "locators": [loc, "brief-keep", "plar-purpose"]},
            {"clause": "against the preserved Start triangle", "class": "inference (shared-consumer, D4), labelled in the basis but not in the authority field", "locators": ["view-idle", "view-consumers", "succ-idle", "succ-consumers"]},
            {"clause": "no specific motif required; grayscale or binarized silhouettes as method", "class": "non-restriction and method (proposal)", "locators": ["brief-inspect"]},
        ],
        obligation=("BRIEF line 3: Error/retry distinguishable without colour alone." if member == "Retry" else "BRIEF line 7: Paused distinguishable from activity, completion and retry without relying on colour alone."),
        delta="r2 text plus 'including the held cell'. Prior caller disposition clarify (D4 basis).",
        alternative=f"A {member} mark distinct from every other status only by hue: rejected (correct).",
        disposition="keep", correction="Record the Start clause as inference in the authority field, not only in the basis (C2/C3).",
        evidence=["visual"], status=PRELIM)

for cid, member, png in [("successor-01.retry.q.consumers", "Retry", "assets/error-retry.png"), ("successor-01.paused.q.consumers", "Paused", "assets/paused.png")]:
    row(cid, split=[
            {"clause": f"error/pause transition through stateAfter; both consumers; label {member}; path {png}; frames 1; nearest at 1 and 3; compositing on #172336; static", "class": "consumer-code fact of the ORIGINAL module and owner brief (requirement)", "locators": ["queue-state", "view-display", "view-consumers", "brief-inspect"]},
            {"clause": "identical descriptor {still 0, animate false, holdFrame 0} under both preferences", "class": "consumer-code fact of the PROPOSED successor module (design proposal); scoped to this destination", "locators": ["succ-idle", "succ-describe", "succ-consumers", "sc-descriptor"]},
            {"clause": "successor fixture + check.py as the route", "class": "evidence route (method)", "locators": ["sv-paint", "si-pixelated"]},
        ],
        obligation="BRIEF line 3/7 display conditions; the original module maps the state to one shared descriptor for both consumers.",
        delta="Fixture renamed to the successor; successor descriptor fields added; 'under both preferences' added.",
        alternative="A successor whose static members carry no `still` field: satisfies the owner obligation; the literal descriptor clause rejects it.",
        disposition="clarify", correction="Scope the descriptor-field clause to the proposed successor destination (C3).",
        evidence=["destination"], status=NO_EVIDENCE)

row("successor-01.delivery.q.continuity",
    split=[
        {"clause": "compare all four members together at 1x and 3x on #172336 against the exact Ready baseline: coherent deliberate pixel treatment, perceptible cool-blue accent, transparent exteriors", "class": "owner requirement (coherent assets, inspection conditions) with the adopted scoped baseline as the comparison anchor", "locators": ["brief-transparent", "brief-inspect", "plar-style"]},
        {"clause": "readable visual weight coherent with the Ready baseline; identical stroke width or footprint not required", "class": "owner requirement as corrected by D3 (coherence does not impose identical weight)", "locators": ["brief-transparent"]},
        {"clause": "including Working's four frames, 100 ms playback with the wrap under normal motion, and the held cell stationary under reduced motion", "class": "owner requirement plus caller update", "locators": ["brief-working", "plar-purpose"]},
        {"clause": "no exact palette, alpha, stroke, margin or copied completion-motif requirement", "class": "non-restriction (observation)", "locators": ["state-style-choice"]},
    ],
    obligation="BRIEF line 3 'coherent pixel-art status assets' inspected at 1x and 3x; the exact baseline is an adopted scoped decision.",
    delta="D3 applied; held cell added to the compared set.",
    alternative="A member with a visibly lighter stroke that still reads coherent: accepted (correct after D3).",
    disposition="keep", correction=None,
    evidence=["visual", "temporal"], status=PRELIM + "; playback viewing outstanding")

row("successor-01.delivery.q.distinction",
    split=[
        {"clause": "Working (animated or held) never reads as success; Retry and Paused distinct from activity (incl. held cell), completion and each other by shape or structure alone", "class": "owner requirement (BRIEF lines 3 and 7)", "locators": ["brief-activity", "brief-retry", "brief-paused"]},
        {"clause": "held cell distinct from Ready and from Paused by shape or structure alone", "class": "caller update requirement (PLAR 422)", "locators": ["plar-purpose"]},
        {"clause": "preserved Start triangle separately identifiable from every member including the held cell", "class": "inference (shared-consumer, D4)", "locators": ["view-idle", "view-consumers", "succ-idle", "succ-consumers"]},
    ],
    obligation="BRIEF lines 3 and 7 and PLAR line 422 distinction requirements over the statuses the view shows.",
    delta="Prior caller disposition keep; held cell and stationary symbol added; D4 basis carried.",
    alternative="A family distinct only by colour: rejected (correct).",
    disposition="keep", correction="Record the Start clause as inference in the authority field (C2/C3).",
    evidence=["visual"], status=PRELIM)

row("successor-01.delivery.q.destination",
    split=[
        {"clause": "assets at the existing paths used by the view", "class": "owner requirement", "locators": ["brief-paths"]},
        {"clause": "destination = src/queue-view-successor.ts + renderer-successor/; original module, renderer/ and every asset byte unchanged against the baseline; fixture executed the successor and not the original; assets/start.svg hash unchanged", "class": "assignment requirement (FOCUSED-SUCCESSOR step 4) and owner (preserve Start)", "locators": ["assign-step4", "brief-start", "sc-modules"]},
        {"clause": "all transitions through both consumers under normal and reduced; labels; frame counts; slicing; frame index at timeline samples incl. 400 ms wrap and frame 0 under reduced; nearest at 1 and 3; compositing", "class": "owner display requirements plus consumer-code of the proposed successor; timing bounded to indices (r2)", "locators": ["queue-state", "brief-inspect", "sc-timeline", "sc-compositing"]},
        {"clause": "recorded integer canvas placement matching the screenshot pixels", "class": "adopted destination-check method (recheck.decision.destination), not an owner rule", "locators": ["sc-compositing"]},
    ],
    obligation="BRIEF line 5 fixes the asset paths; the assignment names the successor destination and the unchanged originals.",
    delta="Destination moved to the successor files per the assignment; reduced-motion sampling added; everything else as r2.",
    alternative="A destination that rebinds the original module in place: rejected (correct per the assignment).",
    disposition="keep", correction="Label the integer-placement method and successor descriptor clauses as method/consumer-code of the proposal (C3).",
    evidence=["destination", "temporal"], status=NO_EVIDENCE)

assert set(P) == set(prop_by), set(prop_by) - set(P)

# ---------------------------------------------------------------- the 20 original rows
original_rows = []
for oid in sorted(ctx_by):
    c = ctx_by[oid]
    m = map_by[oid]
    pr = prior_by[oid]
    carried_ids = m["carried_by"]
    faithful = all(P[cid]["disposition"] in ("keep", "clarify", "correct") for cid in carried_ids)
    original_rows.append({
        "id": oid,
        "record_sha256": c["record_sha256"],
        "check": c["fields"]["ck"],
        "domain": c["fields"]["dm"]["$symbol"],
        "mode": c["fields"]["md"]["$symbol"],
        "state_px_record_current": exp_by[oid]["record_status"],
        "prior_caller_disposition": pr["disposition"],
        "r2_change": r2_by[oid]["change"],
        "mapped_proposed_ids": carried_ids,
        "caller_mapping_verdict": "mapped; required outcome retained; see proposed rows for authority corrections" if faithful else "see proposed rows",
        "non_applicability": m.get("non_applicability"),
    })

# ---------------------------------------------------------------- corrections (without rewriting the original proposal)
corrections = [
    {"id": "C1", "severity": "correct", "criteria": ["successor-01.working.q.stationary-meaning"], "field": "check (last clause) / authority",
     "finding": "The specialist proposal P1 ('hold a phase of the loop so the switch changes motion, not identity') is written into a requirement-labelled check. PLAR line 422 and BRIEF line 3 do not require the stationary symbol to be a phase of the loop; a new static glyph (P2) would satisfy them and be rejected.",
     "correction": "Keep the required outcome (Working's own symbol; not success; not pause). Move the phase-identity clause to the expert clause set with scope 'this successor, P1'.",
     "locators": ["plar-purpose", "brief-activity", "assign-step2"]},
    {"id": "C2", "severity": "correct", "criteria": ["successor-01.working.q.stationary-distinct-retry-start", "successor-01.retry.q.retry-meaning-without-color", "successor-01.paused.q.pause-meaning-without-color", "successor-01.delivery.q.distinction"], "field": "authority",
     "finding": "The authority field says 'requirement' while the basis labels the Start clause an inference. Retry and Start have different authority: Retry distinction is BRIEF line 3 by direct reading; Start distinction is the shared-consumer inference settled as D4.",
     "correction": "Split the authority per clause: Retry = requirement (brief-retry); Start = inference (view-idle, view-consumers, succ-idle, succ-consumers). Caller answer to the specialist's question 2: adopt both clauses with those labels.",
     "locators": ["brief-retry", "view-idle", "view-consumers", "succ-idle", "succ-consumers"]},
    {"id": "C3", "severity": "clarify", "criteria": ["successor-01.working.q.geometry", "successor-01.working.q.consumers-normal-motion", "successor-01.working.q.reduced-motion-consumer-mapping", "successor-01.retry.q.consumers", "successor-01.paused.q.consumers", "successor-01.delivery.q.destination", "successor-01.working.q.style-coherence", "successor-01.retry.q.style-coherence", "successor-01.paused.q.style-coherence", "successor-01.working.q.stationary-distinct-ready-paused"], "field": "authority / scope",
     "finding": "The proposal's convention folds owner brief, caller update, assignment process requirements and consumer-code of the PROPOSED successor module into one 'requirement' label. The successor module is itself a revisable design proposal (the proposal's own source role), so descriptor-field clauses (still, holdFrame, animate, motion) bind a design, not an owner outcome; a different mapping (M1) would be rejected by the literal checks while satisfying PLAR line 422 and the assignment.",
     "correction": "In the corrected proposal, carry per-clause authority classes: owner (BRIEF), caller update (PLAR 422/AUTHORING-UPDATE), assignment (FOCUSED-SUCCESSOR), consumer-code (original module | proposed successor | fixture), measured, expert, inference. Scope successor-specific clauses to 'this successor destination as designed'. No outcome changes.",
     "locators": ["plar-purpose", "assign-step4", "succ-running", "succ-describe"]},
    {"id": "C4", "severity": "clarify", "criteria": ["successor-01.working.q.activity-not-success"], "field": "check / scope",
     "finding": "The check binds every individual frame while the brief binds the loop; the held frame is bound by the caller update. The basis discloses the extension but the check does not scope it.",
     "correction": "Scope: loop (owner) and held cell (caller update) are required; transient frames are an expert clause with the stated 100 ms rationale.",
     "locators": ["brief-activity", "plar-purpose"]},
    {"id": "C5", "severity": "clarify", "criteria": ["successor-01.working.q.stationary-cell-identity"], "field": "authority",
     "finding": "Labelled 'observation', but the first clause chooses cell 0 (specialist proposal P1 bound to the caller's `still: 0` design); only the numbers are observations.",
     "correction": "Label 'proposal (cell choice) + observation (measurements)'; keep the record and its redo rule.",
     "locators": ["succ-running", "succ-still-comment"]},
    {"id": "C6", "severity": "clarify", "criteria": ["successor-01.working.q.transparent-exterior-measured"], "field": "authority",
     "finding": "Labelled 'observation', but the construction-scoped rejection clause (alpha == cw^k(seed)) is an expert construction choice.",
     "correction": "Label the rejection clause 'proposal (seed-rotation construction only)'; keep the flag as diagnostic.",
     "locators": ["brief-transparent"]},
    {"id": "C7", "severity": "note", "criteria": ["successor-01.working.q.stationary-meaning"], "field": "check ('with its consumer label present')",
     "finding": "The fixture renders the label beside the glyph (view.mjs line 62), but BRIEF line 3 asks for readable silhouettes; the label is viewing context, not a carrier of the required reading.",
     "correction": "State that the glyph must carry the non-success/non-pause reading by itself; the label may be present as in the consumer.",
     "locators": ["sv-label", "brief-transparent"]},
    {"id": "C8", "severity": "note", "criteria": ["all engine/live and visual criteria"], "field": "evidence status",
     "finding": "No successor fixture capture exists (render-01 has no render.json; its launch.json root is a different project copy), so every destination/temporal criterion is unevidenced and every visual criterion has only the specialist's preliminary composites. The proposal states this correctly; this review does not convert any of it into a pass.",
     "correction": "None to the proposal. Production-time work (outside this assignment): run renderer-successor/capture.mjs against this consumer root, run check.py with a baseline, retain the capture, then perform caller viewing of native/enlarged fixture views.",
     "locators": ["cont-scope", "cont-no-pass", "cap-scope", "sc-scope"]},
    {"id": "C9", "severity": "note", "criteria": ["reuse"], "field": "reuse.satisfied_now_by_specialist_measurement",
     "finding": "Listing geometry, measured-exterior, frame-assembly (reuse case) and cell-identity as satisfied by measurement is correct for mechanical records and was reproduced by the caller. The 'preliminary visual pass' list is correctly labelled not acceptance.",
     "correction": "None.",
     "locators": ["state-candidate"]},
    {"id": "C10", "severity": "clarify", "criteria": ["successor-01.working.q.consumers-normal-motion", "successor-01.working.q.motion-continuity", "successor-01.delivery.q.continuity"], "field": "check / evidence_route (temporal evidence)",
     "finding": "Raised by the specialist in round 1 (S5) and verified by the caller against the fixture and checker: the fixture samples each live cell once (view.mjs line 157) and check.py tests that one frame with a boundary tolerance (line 140); 'cycling through all four cells' is asserted only on the synthetic timeline (lines 163-164). The actual-playback leg of motion-continuity and delivery continuity has no artefact and no named viewing route; check.py's scope says it does not judge animation.",
     "correction": "Reword consumers-normal-motion to what the checker asserts; keep 'wall-clock not measured'; name caller viewing of the live page under normal motion (1x and 3x) as the route for the playback leg, recorded as a visual observation. Three legs stay separate: frameMs constant (mechanical), frame-index arithmetic (mechanical), actual playback (visual/temporal).",
     "locators": ["sv-live-sample", "sc-live-single", "sc-timeline", "sc-scope"]},
    {"id": "C11", "severity": "clarify", "criteria": ["successor-01.working.q.frame-assembly"], "field": "sources / basis",
     "finding": "Raised by the specialist (S3) and verified by the caller: the frame-selection/assembly policy obligation is stated in AUTHORING-STAGE.md lines 31-32, which the proposal's 33-entry source index omits; FOCUSED-SUCCESSOR lines 40-43 authorise reuse and forbid invented observations but do not state an assembly policy.",
     "correction": "Add AUTHORING-STAGE.md (sha256 in this file's source index) and cite lines 31-32 for the assembly clause; keep lines 40-43 for reuse authorisation.",
     "locators": ["stage-assembly", "assign-step4-reuse"]},
    {"id": "C12", "severity": "note", "criteria": ["successor-01.working.q.live-preference-switch", "successor-01.working.q.reduced-motion-consumer-mapping"], "field": "check vs checker support",
     "finding": "Raised by the specialist (S12) and verified by the caller: check.py's [switch] block inspects only running cells (line 180), so 'other states repaint unchanged' is unasserted; the phase map (lines 67-69) has no expected motion for an as-launched forced-reduced run, so the startup-preference route named in the evidence_route is unasserted.",
     "correction": "Add the two assertions to the checker at production time, or label those clauses as caller visual observations on the reduced-phase screenshot. No change to the required outcome.",
     "locators": ["sc-switch-running-only", "sc-phase-map", "cap-phases"]},
]

# ---------------------------------------------------------------- cross-check with the specialist's round-1 assessment (read after the caller's rows were authored)
specialist_crosscheck = None
specialist_answers = None
if os.path.exists(ROUND1):
    r1 = load(ROUND1)
    r1_by = {d["id"]: d for d in r1.get("defects", [])}
    specialist_crosscheck = {
        "read_after_authoring_caller_rows": True,
        "specialist_defects": {k: {"severity": v["severity"], "criteria": v["criterion_ids"]} for k, v in r1_by.items()},
        "agreement": {
            "S1": "agrees with C1 (P1 clause promoted to requirement); caller chooses option (b): remove the clause from the check, keep it as an expert clause scoped to P1",
            "S2": "agrees with C7 (label is context); caller adopts 'judge alone and beside the label'",
            "S3": "new to the caller; verified against AUTHORING-STAGE.md lines 31-32 and FOCUSED-SUCCESSOR lines 40-43; adopted as C11",
            "S4": "agrees with C4",
            "S5": "new to the caller; verified against view.mjs line 157 and check.py lines 140, 163-164, 191-192; adopted as C10",
            "S6": "agrees with C3 (descriptor shapes are the proposed module's design)",
            "S7": "agrees with C3 (per-clause authority classes)",
            "S8": "accepted as a wording note (counts are measured values of the current seed, not the rule)",
            "S9": "accepted as a note: the Start-accent relation is an inference from assets/start.svg fill #70b9ed; the check already binds perceptibility, not hue",
            "S10": "accepted as a basis note; no check change",
            "S11": "agrees with C2; caller answers the open question below",
            "S12": "new to the caller; verified against check.py lines 180 and 67-69; adopted as C12",
        },
        "caller_findings_not_raised_by_specialist": ["C5 (stationary-cell-identity label hides the cell choice)", "C6 (construction-scoped rejection clause labelled observation)", "C8/C9 evidence-status notes"],
        "visual_concurrence": "both parties independently read the held cell as distinct from Ready and Paused by structure, Retry as the closest pair needing native-scale fixture viewing, and the frozen-spinner 'stalled' reading as a recorded limit; neither reading is acceptance",
    }
    specialist_answers = {
        "Q1_scope_of_the_criteria_set": "The owner, caller-update and assignment outcome clauses are the successor's universal Working contract. P1-specific clauses (loop-phase identity, cell-0 identity record, exact descriptor shapes) are scoped to the P1 held-cell candidate as designed. Fix S1/C1 by removing the loop-phase clause from the check (option b) and keeping it as an expert clause scoped to P1; fix S6/C3 by scoping descriptor equality to this implementation, re-derived if the module changes.",
        "Q2_retry_and_start_distinction": "Adopt both, with separate labels: distinction from Retry is an owner requirement by direct reading of BRIEF line 3 over the statuses the view shows; distinction from Start is the shared-consumer inference settled as D4. Neither is a new owner line.",
    }

# ---------------------------------------------------------------- evidence separation summary
evidence_separation = {
    "classes": EVIDENCE,
    "by_class": {
        "mechanical": [cid for cid, r in P.items() if r["evidence_class"] == ["mechanical"]],
        "visual": [cid for cid, r in P.items() if "visual" in r["evidence_class"] and "temporal" not in r["evidence_class"]],
        "temporal": [cid for cid, r in P.items() if "temporal" in r["evidence_class"]],
        "destination": [cid for cid, r in P.items() if "destination" in r["evidence_class"]],
    },
    "status": {
        "mechanical": "caller reproduced every measured fact the proposal relies on (caller-measurements.json)",
        "visual": "specialist preliminary composites only; caller observation recorded above; no fixture or pixl_inspection views; no acceptance",
        "temporal": "no retained capture; no playback viewed",
        "destination": "no retained capture; check.py never run",
    },
    "rule": "a mechanical pass never supplies visual acceptance; a visual reading of composites never supplies destination evidence; retained unavailable checks stay unavailable (CONTINUATION-ASSIGNMENT.md line 27)",
}

# ---------------------------------------------------------------- reduced-motion assessment (caller)
reduced_motion = {
    "requirement": {"text": "the reduced-motion mode must use a stationary Working symbol distinguishable from Ready and Paused. Confirm its consumer mapping before any further generation.", "locators": ["plar-purpose", "update-req"]},
    "specialist_recommendation": proposal["reduced_motion_design"]["recommendation"]["symbol"],
    "caller_assessment": [
        "P1 (hold cell 0 of the existing accepted sheet) is consistent with every owner line and the caller update: no new art, one shared mapping through both consumers, accepted provenance untouched. It is a proposal; this comparison does not adopt it (CONTINUATION-ASSIGNMENT.md lines 12-14).",
        "The held cell is distinct from Ready and Paused by structure on every view the caller saw; the Retry pair is the risk and must be judged on a native-scale fixture capture.",
        "The frozen-spinner 'stalled' reading is a real limit the specialist disclosed honestly; it is not a failure of PLAR line 422. Whether the owner accepts frozen-spinner semantics is a remaining decision (specialist question 1), to be taken at production time, not here.",
        "P2 (new static glyph) would need one PixelLab generation and a new descriptor path; P3 (gapped ring) would weaken Retry distinction; M3 (new queue state) is not a presentation concern. The caller agrees with the specialist's ordering but records them as alternatives, not rejections.",
        "M1 (separate static file mapping) was not tested by the proposal and remains open; the literal mapping criteria currently exclude it (C3).",
    ],
    "no_pixellab_work_needed_for_P1": True,
}

limitations = [
    "Comparison only: no production adoption, no renderer run, no art acceptance, no state commit, no PLAR write, no job action (CONTINUATION-ASSIGNMENT.md lines 12-14).",
    "The earlier child that wrote the proposal is gone; this is an artifact-based restart. The native child used in this phase is a new instance whose ID is retained in PHASE1-CALLER.json for reconciliation.",
    "No successor fixture capture exists for this consumer root; destination and temporal evidence is absent; visual evidence is preliminary.",
    "Caller viewing used the specialist's composite PNGs, not independently rendered views; it is an observation, not acceptance.",
    "The original 20 Q records remain unchanged in state.px revision 88; no verdict is transferred to any successor criterion; no successor criteria are authored in the store by this review.",
    "M1 and broader host reliability remain open.",
]
remaining_decisions = [
    "Owner/caller: accept frozen-spinner semantics for reduced motion (P1) or require a distinct static glyph (P2 with one generation).",
    "Caller at production time: author the successor plan/criteria through the public operations with per-clause authority classes (C1-C7), preserving the 20 original Q records and the prepared job's history.",
    "Caller at production time: resolve job authoring-01.working.join-01 through its existing failed-observation route (no remote id); not performed here.",
    "Caller at production time: run the successor capture and check.py against this root, retain them, and perform the visual review on native/enlarged fixture views.",
]

round1 = None
if os.path.exists(ROUND1):
    round1 = {"path": ROUND1, "sha256": sha(ROUND1), "note": "specialist round-1 assessment produced by the native child in this phase; the caller's rows above were authored independently of it"}

review = {
    "version": 1,
    "kind": "caller-review",
    "reviewer_role": "calling agent (parent), independent caller review; the native PIXL child owns the specialist assessment",
    "assignment": {"path": "CONTINUATION-ASSIGNMENT.md", "sha256": sha("CONTINUATION-ASSIGNMENT.md"), "phase": 1},
    "restart": "artifact-based restart of the interrupted focused-authoring comparison; the prior child is not resumed; all old files and grades preserved",
    "identities": identities,
    "sources": sources,
    "locators": locators,
    "caller_verification": caller_verification,
    "original_criteria": original_rows,
    "proposed_criteria": [P[c["id"]] for c in proposal["criteria"]],
    "corrections": corrections,
    "r2_corrections_applied": {
        "D1": "applied in all three members: measured record is a flag, visual record decides; construction-scoped rejection only for Working",
        "D2": "applied: required outcome is one continuous loop at 100 ms with no wrap discontinuity; pacing clauses are expert",
        "D3": "applied: readable visual weight coherent with the baseline; identical stroke/footprint not required",
        "D4": "applied in the basis text; not reflected in the authority field (C2)",
    },
    "evidence_separation": evidence_separation,
    "reduced_motion": reduced_motion,
    "specialist_round1": round1,
    "specialist_round1_crosscheck": specialist_crosscheck,
    "answers_to_specialist_questions": specialist_answers,
    "verdict": {
        "contract_consistency": "changes_requested",
        "summary": "Every owner outcome of the 20 original criteria survives into the 29 proposed criteria with the r2 corrections applied; nothing is dropped, and the one weakened leg is the temporal evidence route (C10). Two corrections (C1, C2) and clarifications C3-C7, C10-C12 concern authority labels, scope, one source locator and checker support, mainly where the specialist's P1 proposal or the caller's own successor design is written as a requirement. No production, renderer or acceptance claim is made.",
        "counts": {"keep": sum(1 for r in P.values() if r["disposition"] == "keep"), "clarify": sum(1 for r in P.values() if r["disposition"] == "clarify"), "correct": sum(1 for r in P.values() if r["disposition"] == "correct")},
    },
    "limitations": limitations,
    "remaining_decisions": remaining_decisions,
    "next_action": "Retain this review; a separate invocation resumes this parent session and sends the retained native child the review for reconciliation (C1-C7 and the two answered questions). No production step follows in this phase.",
    "generated_at": datetime.now(timezone.utc).isoformat(),
}
with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
    json.dump(review, handle, indent=1, ensure_ascii=False)
    handle.write("\n")
print(json.dumps({"out": OUT, "sha256": sha(OUT), "proposed_rows": len(P), "original_rows": len(original_rows), "corrections": len(corrections), "counts": review["verdict"]["counts"], "round1": round1}))
