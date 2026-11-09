"""Build revision 2 of the PIXL specialist corrected proposal (authoring-01 criteria review).

Artifact-based restart: loads the r1 proposal/report bytes, applies ONLY the edits the
caller's four findings (D1-D4) require plus revision metadata, re-verifies every cited
source range (hash + bounds + relied-on wording), re-hashes the historical files, and
writes two NEW files:
  work/criteria-review-01/specialist-proposal-r2.json
  work/criteria-review-01/specialist-report-r2.json
Nothing else is written. Read-only on the store, PLAR, jobs and the r1 artifacts.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(r"C:\github\pixel-lab-agent\evidence\criteria-handoff\20261109\native\claude-01\project")
OUT_DIR = ROOT / "work" / "criteria-review-01"
R1_PROPOSAL = OUT_DIR / "specialist-proposal.json"
R1_REPORT = OUT_DIR / "specialist-report.json"
R2_PROPOSAL = OUT_DIR / "specialist-proposal-r2.json"
R2_REPORT = OUT_DIR / "specialist-report-r2.json"

EXPECT = {
    "work/criteria-review-01/specialist-proposal.json": "441f5806bbc2d4b15e4507b862c9aa2bc92a91250448b2a040399cb79a21f144",
    "work/criteria-review-01/specialist-report.json": "bd7598a1b814b3d53196b2dcab0af0785edb9d37378248c1fcf16fc6809b0cf7",
    "work/criteria-review-01/request-review.json": "5563d65e834448a88974f984817bc4d6c1ac91ea7b254624fb15b01740fb5068",
    "work/criteria-review-01/request-review-raw.txt": "f0bb3c5c08ff3f5b7f4bdda09d56a7383209f3828b2074943856414ed3e80cc4",
    ".pixl/assets/queue.ready/state.px": "3484cf385c91c8c28fa04316fb2c7c5b52c740178b505ccbd88631f57c893c9b",
    "authoring-plar.txt": "7c6c54fb55f0cb46fb8f5707468b3776438bd62ab102beafb49c2e91e50e3b41",
    "plar.txt": "a462ecf3b6b45c0382d3483b0f4f6912a9d0bd1d68e75253143faa1423837344",
    "AUTHORING-RESULT.json": "3724bfa77c0a9af49bbcec6389b3f3b2d3879a49954e3148bdba8321537bdad7",
    "AUTHORING-REVIEW.md": "3e23ca557c94a047bcb2e57da8395d76ff680da53dc9a6e2bb8ffc2c50a586f2",
    "BRIEF.md": "aebe00949f3a9510a44f6f554b8fc97e53476d7658a4bb29419db85b417f02ab",
    "src/queue-view.ts": "4d6ee92e40374d4dd4c6a49a3a20a6caf34e7f2d61a32a230c8ecf54691b5c49",
    "work/family-render-review/caller-comparison-final.json": "ddacac1e4c7b10a063eb2dd3595edf6ff28dd39f3c24fabb9b945bcba879cde2",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


for rel, expected in EXPECT.items():
    actual = sha256(ROOT / rel)
    if actual != expected:
        raise SystemExit(f"precondition failed: {rel} is {actual}, expected {expected}")

for out in (R2_PROPOSAL, R2_REPORT):
    if out.exists():
        raise SystemExit(f"refusing to overwrite existing {out}")

_lines_cache: dict[str, list[str]] = {}
_sha_cache: dict[str, str] = {}


def file_lines(rel: str) -> list[str]:
    if rel not in _lines_cache:
        _lines_cache[rel] = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    return _lines_cache[rel]


def file_sha(rel: str) -> str:
    if rel not in _sha_cache:
        _sha_cache[rel] = sha256(ROOT / rel)
    return _sha_cache[rel]


new_citations: list[dict] = []


def S(rel: str, lines: list[int], expect: str) -> dict:
    """Verified source pointer: one-based inclusive file-local bounds containing `expect`."""
    first, last = lines
    content = file_lines(rel)
    if not (1 <= first <= last <= len(content)):
        raise SystemExit(f"bounds out of range: {rel} {lines}")
    segment = "\n".join(content[first - 1 : last])
    if expect not in segment:
        raise SystemExit(f"citation not verified: {rel} {lines} lacks {expect!r}")
    pointer = {"path": rel, "sha256": file_sha(rel), "lines": [first, last]}
    new_citations.append({**pointer, "verified_wording": expect})
    return pointer


# ------------------------------------------------------------------ load r1 ----
r1 = json.loads(R1_PROPOSAL.read_text(encoding="utf-8"))
r1_report = json.loads(R1_REPORT.read_text(encoding="utf-8"))
r2 = copy.deepcopy(r1)
by_id = {c["criterion"]: c for c in r2["criteria"]}
if len(by_id) != 20:
    raise SystemExit("expected 20 criteria in r1")

# ------------------------------------------------------- new source pointers ----
QV_IDLE = S("src/queue-view.ts", [3, 3], 'idle: { label: "Start", path: "assets/start.svg", frames: 1 }')
QV_CONSUMERS = S("src/queue-view.ts", [10, 11], "export function compactStatus(state: QueueState) { return statusVisuals[state]; }")
BRIEF_MAIN = S("BRIEF.md", [3, 3], "Preserve the existing vector Start control")
BRIEF_PAUSED = S("BRIEF.md", [7, 7], "distinguishable from activity, completion and retry without relying on color alone")
AP_R_CHECKS = S("authoring-plar.txt", [846, 846], "grayscale comparison with Start, Ready and all Working frames")
AP_W_ANIM = S("authoring-plar.txt", [546, 559], '"frame_duration_ms": 100')
QV_DISPLAY = S("src/queue-view.ts", [9, 9], "frameMs: 100")
SP_CT_WORKING = S(".pixl/assets/queue.ready/state.px", [62, 62], "Review every frame and actual loop,loop boundary,anchor and volume stability")
SP_V_REPAIR = S(".pixl/assets/queue.ready/state.px", [320, 320], "Segments morph and near-hold across phases2/3, then jump atwrap")
SP_V_ANIM01 = S(".pixl/assets/queue.ready/state.px", [258, 258], "contains193 opaque #808080 pixels in its background")
SP_V_PAUSED02 = S(".pixl/assets/queue.ready/state.px", [183, 183], "Opaque magenta intermediate fails final transparent-exterior criterion")
SP_CH_STYLE = S(".pixl/assets/queue.ready/state.px", [392, 392], "not_fixed=[~9:exact hex,~13:palette count,~12:binary alpha,~12:stroke width,~7:margins")
CC_NOTP = S("work/family-render-review/caller-comparison-final.json", [120, 125], "Exact stroke weight, margin or footprint")
CC_RATIONALE = S("work/family-render-review/caller-comparison-final.json", [126, 126], "no matte/fringe or resampling blur")
RP = "work/authoring-01/working-rotation-policy.json"
RP_TRANS = S(RP, [52, 52], "#00000000 (all 224 transparent seed pixels are RGBA 0,0,0,0)")
RP_OBLIG = S(RP, [1017, 1023], "pixel-exact: each delivered cell equals cw^k(seed) (local check)")
RP_PLAY = S(RP, [1016, 1016], "angular velocity is uniform and the loop boundary is not a special case")
KIT_RR = ".agents/skills/pixl-kit/skills/pixl/references/request-review.md"
KIT_RR_DIAG = S(KIT_RR, [185, 185], "Do not silently turn a process restriction into an extra output-difference test, or a diagnostic into a rejection rule")
KIT_RR_OBS = S(KIT_RR, [20, 20], "Observations alone do not become rejection rules.")
KIT_RR_ROUTE = S(KIT_RR, [149, 153], "It cannot decide which\nshape is intentional foreground, whether a matte is unwanted")
KIT_PROFILE = ".agents/skills/pixl-kit/resources/agent/PROFILE.md"
KIT_PROFILE_TRANSP = S(KIT_PROFILE, [62, 67], "that is different from\n  an unintended opaque canvas matte")
AR_TRANSRGB = S("AUTHORING-RESULT.json", [130, 130], "210 fully transparent pixels carry RGB 128,128,128")

revision_changes: list[dict] = []

# ======================================================================= D1 =====
D1_IDS = {
    "authoring-01.working.q.transparent-exterior": "working",
    "authoring-01.retry.q.transparent-exterior": "retry",
    "authoring-01.paused.q.transparent-exterior": "paused",
}

DIAG_CLAUSE_TEXT = (
    "[proposed MEASURED record - diagnostic] retain the alpha histogram and exact RGBA component boxes of every cell "
    "(pixl_asset_check(alpha=full, regions=...); zero-based, exclusive right/bottom); flag for visual review any alpha>0 "
    "component that touches all four cell edges, or any single alpha>0 component covering more than half of the cell's 256 pixels "
    "(diagnostic threshold chosen by the specialist; the 193-pixel grey tile and a full canvas matte trip it, the 32-pixel seed does not)"
)
DIAG_CLAUSE_BASIS = (
    "A diagnostic proxy for an unintended canvas matte / grey tile. It is NOT a rejection condition: a brief-conforming mark such as a "
    "corner-to-corner X, or a full-height/full-width glyph, has a single component touching all four cell edges while its exterior stays "
    "transparent, so the proxy cannot decide the requirement. The kit's request-review reference forbids turning a diagnostic into a "
    "rejection rule and states that a local mechanical check cannot decide whether a matte is unwanted; the PIXL profile separates an "
    "unintended canvas matte from a deliberate backing. r1 wrote this proxy as 'no cell may contain an alpha>0 region that reaches all "
    "four cell edges or fills the cell' (a rejection rule); r2 demotes it to a flag that triggers the VISUAL record."
)
DIAG_CLAUSE_SCOPE = "diagnostic proxy; triggers visual review; not a rejection rule (whole asset, every cell)"

CONSTR_CLAUSE_TEXT = (
    "[proposed MEASURED record - construction-scoped rejection rule] under the seed-rotation construction, each delivered cell's alpha "
    "channel equals that of cw^k(seed) (224 alpha-0 pixels per cell, exactly the seed's alpha-0 set rotated); RGB values of alpha-0 pixels are not significant"
)
CONSTR_CLAUSE_BASIS = (
    "The only mechanically decidable form of the transparent-exterior requirement: the construction fixes the exterior as the alpha-0 set of "
    "cw^k(seed), so inequality is a definite defect. Expert construction choice (rotation policy), not an owner rule; it does not apply to any "
    "other construction. Transparent RGB is insignificant because the accepted motion strip carries RGB 128,128,128 on alpha-0 pixels."
)

VISUAL_DECIDES = (
    "The VISUAL record is the deciding rule for unintended matte, tile, plate or fringe (which pixels are 'the mark' and whether a backing is "
    "unwanted is visual judgment); the measured record only flags candidates for that judgment, except for the seed-rotation alpha-equality rule."
)


def d1_proposed_check(stage: str) -> str:
    cells = "every cell's" if stage == "working" else "the cell's"
    frames = "every frame" if stage == "working" else "the image"
    constr = (
        " Mechanical REJECTION is decidable only under the seed-rotation construction: each cell's alpha channel must equal that of cw^k(seed) "
        "(224 alpha-0 pixels per cell); RGB values of alpha-0 pixels are not significant."
        if stage == "working"
        else " No mechanical rejection rule is decidable for this static member (no construction fixes its alpha set); RGB values of alpha-0 pixels are not significant."
    )
    example = {
        "working": " The rejected frame with 193 opaque #808080 background pixels (live.working-animation-01.review.verdict.1) is the failure class.",
        "retry": "",
        "paused": " The rejected opaque magenta intermediate (live.paused-02.review.verdict.1) is the failure class.",
    }[stage]
    return (
        "Two records (caller decision: adopt the split for any future plan; for the existing Q record this is documented correction only). "
        f"MEASURED record (mechanical/local): retain {cells} alpha histogram and exact RGBA component boxes; FLAG for visual review any alpha>0 component "
        "touching all four cell edges, or any single alpha>0 component covering more than half of the cell's 256 pixels. The flag is a diagnostic proxy "
        "for a canvas matte / grey tile and is not a rejection condition: a corner-to-corner X or a full-height/full-width glyph legitimately touches all "
        f"four edges with a transparent exterior.{constr} "
        f"VISUAL record (visual/visual; the deciding rule): viewed at 1x and 3x on #172336, the exterior of {frames} shows the panel with no unintended matte, "
        "tile, plate, halo or fringe; a deliberate opaque backing shape is acceptable only when it is part of the mark's recorded design and the exterior "
        f"stays transparent.{example} Partial alpha on mark pixels is permitted; binary alpha is not required."
    )


D1_ALT = (
    "(1) A corner-to-corner X (two full diagonals) or a full-height/full-width glyph: one alpha>0 component touches all four cell edges while every "
    "pixel outside the strokes has alpha 0, so BRIEF line 3 'transparent backgrounds' holds. r1's measured clause rejects it mechanically; r2 only flags it "
    "and the visual record accepts it. (2) A mark on a small deliberate dark-blue badge (10x10 rounded plate) with transparent edges and corners: the "
    "original 'no ... plate' rejects it; r2 judges it visually as a recorded design element. (3) A candidate whose alpha-0 pixels carry RGB 128,128,128 "
    "(AUTHORING-RESULT.json line 130) must not be rejected on RGB of transparent pixels. (4) Under the seed-rotation construction a cell whose alpha set "
    "differs from cw^k(seed) is rejected mechanically; that rejection is construction-scoped and intended."
)

for cid, stage in D1_IDS.items():
    c = by_id[cid]
    old_check = c["proposed_check"]
    # clause 1: exterior alpha 0 - correct the mechanical-form statement per member
    cl1 = c["clauses"][0]
    if stage == "working":
        cl1["basis"] = (
            "BRIEF line 3 'transparent backgrounds'; authoring-plar background requirement (transparent; binary alpha not required). Which opaque pixels "
            "are 'the mark' is a visual judgment (deciding rule: the VISUAL record). Under the seed-rotation construction only, the exterior is exactly the "
            "alpha-0 set of cw^k(seed) and is mechanically decidable; the edge/coverage proxy is a diagnostic, not a rejection rule."
        )
        cl1["scope"] = "whole asset (outcome, decided visually); mechanical rejection form only under the seed-rotation construction"
    else:
        cl1["basis"] = (
            "BRIEF line 3 'transparent backgrounds'; authoring-plar background requirement (transparent; binary alpha not required). Which opaque pixels "
            "are 'the mark' is a visual judgment (deciding rule: the VISUAL record). r1's basis mentioned the seed-rotation construction, which belongs to "
            "the Working strip only; for this static member no construction fixes the alpha set, so there is no mechanical rejection form - the measured "
            "record is diagnostic only."
        )
        cl1["scope"] = "whole asset (outcome, decided visually); no construction-scoped mechanical form for this member"
    # clause 2: matte/plate/fringe - visual decides
    cl2 = c["clauses"][1]
    cl2["basis"] = (
        "Unintended canvas matte / grey tile / fringe violates the transparent-background requirement (historical verdict evidence) and is decided by the "
        "VISUAL record. 'Plate' as a blanket prohibition is an expert construction preference: the PIXL profile distinguishes an unintended canvas matte "
        "from a deliberate plate/badge/backing with transparent exterior, which the brief does not forbid."
    )
    cl2["scope"] = (
        "matte/tile/fringe: whole asset (requirement; VISUAL record decides); 'no deliberate plate': expert proposal, scoped to this authoring branch's construction"
    )
    cl2["source"] = cl2["source"] + [KIT_PROFILE_TRANSP]
    # insert diagnostic clause (and construction clause for working) before the trailing observation clauses
    insert_at = 2
    diag_sources = [KIT_RR_DIAG, KIT_RR_OBS, KIT_RR_ROUTE, KIT_PROFILE_TRANSP, CC_RATIONALE] + (
        [SP_V_ANIM01] if stage == "working" else ([SP_V_PAUSED02] if stage == "paused" else [])
    )
    new_clauses = [
        {"text": DIAG_CLAUSE_TEXT, "authority": "observation", "basis": DIAG_CLAUSE_BASIS, "scope": DIAG_CLAUSE_SCOPE, "source": diag_sources}
    ]
    if stage == "working":
        new_clauses.append(
            {
                "text": CONSTR_CLAUSE_TEXT,
                "authority": "proposal",
                "basis": CONSTR_CLAUSE_BASIS,
                "scope": "seed rotation construction only; mechanical rejection rule (local)",
                "source": [RP_TRANS, RP_OBLIG, AR_TRANSRGB],
            }
        )
    c["clauses"] = c["clauses"][:insert_at] + new_clauses + c["clauses"][insert_at:]
    c["proposed_check"] = d1_proposed_check(stage)
    c["proposed_domain"] = "split (caller decision): measured record mechanical; visual record visual (deciding). If the existing single Q record is read as one rule, its domain is visual."
    c["proposed_mode"] = "split (caller decision): measured record local; visual record visual (deciding). If the existing single Q record is read as one rule, its mode is visual."
    c["change"] = "correct"
    c["change_explanation"] = (
        "Old (Q record): one mechanical/local check deciding what is 'outside the mark' and prohibiting any 'plate'. r1: split into measured + visual, but wrote "
        "the measured edge/coverage test as a rejection rule ('no cell may contain an alpha>0 region that reaches all four cell edges or fills the cell'), "
        "which would wrongly reject a corner-to-corner X or a full-height/full-width glyph. r2: that test is a DIAGNOSTIC that flags a candidate for visual "
        "review (authority observation; scope 'diagnostic proxy; triggers visual review; not a rejection rule'); "
        + (
            "mechanical rejection is kept only where decidable (seed-rotation construction: cell alpha equals cw^k(seed)); "
            if stage == "working"
            else "no mechanical rejection form exists for this static member; "
        )
        + "the VISUAL record is the deciding rule for unintended matte/tile/plate/fringe. 'No plate' remains narrowed to unintended matte; transparent RGB remains insignificant. "
        "Caller decision recorded: adopt the split for any future plan; for the existing Q record this is documented correction only."
    )
    c["discriminating_alternative"] = D1_ALT
    revision_changes.append(
        {
            "finding": "D1",
            "criterion": cid,
            "record_sha256": c["record_sha256"],
            "field": "proposed_check (measured part), clauses, proposed_domain/mode, change_explanation, discriminating_alternative",
            "old": old_check,
            "new": c["proposed_check"],
            "old_to_new": (
                "measured clause 'no cell may contain an alpha>0 region that reaches all four cell edges or fills the cell (canvas matte / grey tile)' "
                "[rejection rule] -> 'FLAG for visual review any alpha>0 component touching all four cell edges, or any single component covering more "
                "than half of the cell' [diagnostic proxy; triggers visual review; not a rejection rule]; "
                + (
                    "mechanical rejection retained only as 'cell alpha equals cw^k(seed)' under the seed-rotation construction; "
                    if stage == "working"
                    else "r1's seed-rotation mechanical form removed from this static member's basis (it belongs to Working only); "
                )
                + "VISUAL record named as the deciding rule for unintended matte/tile/plate/fringe."
            ),
            "basis": "kit request-review.md line 185 (diagnostic is not a rejection rule), line 20 (observations alone do not become rejection rules), lines 149-153 (mechanical check cannot decide whether a matte is unwanted); PROFILE.md lines 62-67 (unintended matte vs deliberate backing); BRIEF line 3 'transparent backgrounds' is satisfied by an X or full-span glyph with transparent exterior.",
            "caller_decision_recorded": "Adopt the SPLIT (one measured/diagnostic record + one visual record) for any future plan; for the existing Q records this is documented correction only.",
        }
    )

# ======================================================================= D2 =====
cid = "authoring-01.working.q.motion-continuity"
c = by_id[cid]
old_check = c["proposed_check"]
cl5 = c["clauses"][4]  # 'near-hold or wrap jump (...)'
cl5["basis"] = (
    "'Wrap jump': required outcome - BRIEF line 3 fixes four frames at 100 ms and a loop that communicates activity; authoring-plar animation loop:true; "
    "the contract's loop-boundary review (requirement). 'Near-hold' / even pacing of motion: expert quality clause (specialist proposal). BRIEF line 3 does "
    "not require equal motion increments per frame; at 4 x 100 ms a held pair reads as a stutter, which is expert judgment, not owner authority. Under the "
    "seed-rotation construction even pacing is satisfied by construction (uniform angular velocity, policy line 1016). The parenthetical is an observation "
    "of live.working-animation-repair-01.review.verdict.1."
)
cl5["scope"] = "wrap jump: whole asset (requirement); near-hold / even pacing: expert quality clause, whole Working asset, not owner authority (satisfied by construction under seed rotation); parenthetical: example"
cl5["source"] = [SP_V_REPAIR, AP_W_ANIM, SP_CT_WORKING, RP_PLAY, QV_DISPLAY]
c["proposed_check"] = (
    "Play the actual four frames at the consumer's 100 ms per frame including the fourth-to-first wrap, at 1x and 3x on #172336. Required outcome: the "
    "strip plays as one continuous activity loop with no visible discontinuity at the fourth-to-first wrap (BRIEF line 3: four frames, 100 ms, loop "
    "communicates activity; display.frameMs 100; contract loop-boundary review). Expert quality clauses binding through family.working.contract for this "
    "Working asset: stable centre/anchor and stable visual volume across phases. Expert quality clause by specialist judgment (not in the contract text, "
    "not owner authority): motion is evenly paced across the four frames with no near-hold, because at 4 x 100 ms a held pair reads as a stutter; under the "
    "seed-rotation construction this is satisfied by construction (uniform angular velocity). Construction-scoped clauses for the seed-rotation construction "
    "only: stable cluster count (three components per cell) and stepped quarter-turn phases with no morphing. The rejected AI animation "
    "(live.working-animation-repair-01.review.verdict.1: morph/near-hold across phases 2/3, jump at wrap) is the failure class, not the definition of the rule."
)
c["change_explanation"] = (
    "Old: one undifferentiated rule. r1: separated a required outcome but placed 'evenly paced' inside it. r2: the required outcome is only what BRIEF line 3 "
    "and the consumer fix - one continuous activity loop at 100 ms per frame with no visible discontinuity at the wrap; 'evenly paced' and 'no near-hold' "
    "move to the expert clause set as a specialist quality clause for this Working asset (satisfied by construction under seed rotation), with basis. "
    "Anchor/volume stability remain expert clauses bound through the adopted contract; cluster count and no-morphing remain construction-scoped. "
    "No clause deleted; nothing promoted to owner authority."
)
c["discriminating_alternative"] = (
    "(1) A four-frame loop whose motion increments are deliberately uneven (three small steps and one larger catch-up step) yet plays as one continuous "
    "activity loop with no discontinuity at the wrap: satisfies BRIEF line 3; r1's required outcome 'evenly paced' would reject it on owner authority; "
    "r2 judges it under the expert clause (the specialist may still criticise the stutter, as expert judgment). (2) A four-frame pulse in which a dot grows "
    "into a ring and back (cluster count and volume vary) with a seamless wrap: satisfies BRIEF line 3; the literal 'stable cluster count ... no morphing' "
    "rejects it, which is why those clauses are construction-scoped."
)
revision_changes.append(
    {
        "finding": "D2",
        "criterion": cid,
        "record_sha256": c["record_sha256"],
        "field": "proposed_check (required outcome vs expert clauses), clause 'near-hold or wrap jump' basis/scope/sources, change_explanation, discriminating_alternative",
        "old": old_check,
        "new": c["proposed_check"],
        "old_to_new": (
            "required outcome 'one continuous, evenly paced activity cycle with no visible jump at the wrap' -> required outcome 'one continuous activity loop at the "
            "consumer's 100 ms per frame with no visible discontinuity at the fourth-to-first wrap'; 'evenly paced' and 'no near-hold' moved to the expert clause set "
            "(specialist quality clause for this Working asset; satisfied by construction under seed rotation; not owner authority)."
        ),
        "basis": "BRIEF line 3 fixes four frames at 100 ms and that the loop communicates activity; it does not require equal motion increments per frame. src/queue-view.ts line 9 frameMs 100; state.px line 62 contract (loop boundary, anchor, volume - no pacing clause); rotation policy line 1016 (uniform angular velocity by construction).",
    }
)

# ======================================================================= D3 =====
cid = "authoring-01.delivery.q.continuity"
c = by_id[cid]
old_check = c["proposed_check"]
cl2 = c["clauses"][1]
cl2["basis"] = (
    "BRIEF line 3 (coherent, readable, cool-blue accent, transparent); adopted style carry list. 'Readable visual weight' is ambiguous in one direction "
    "(could be read as requiring equal stroke weight); r1's 'comparable (not identical) visual weight' added a cross-member comparability restriction the "
    "sources do not state. r2 keeps the brief's outcome - readable visual weight coherent with the Ready baseline - and states the explicit non-requirement: "
    "identical stroke width or footprint is not required (render.choice.style not_fixed lists stroke width and margins; caller-comparison-final not_prescribed "
    "'Exact stroke weight, margin or footprint')."
)
cl2["scope"] = "collective delivery; wording clarified without a comparability rule"
cl2["source"] = cl2["source"] + [SP_CH_STYLE]
c["proposed_check"] = (
    "Compare all four actual members together at 1x and 3x nearest on #172336 against the exact Ready baseline: coherent deliberate pixel treatment, readable "
    "visual weight coherent with the Ready baseline (identical stroke width or footprint is not required), perceptible cool-blue accent and transparent "
    "exteriors, including Working's four frames and its actual 100 ms playback with the wrap; no exact palette, alpha, stroke, margin or copied "
    "completion-motif requirement."
)
c["change_explanation"] = (
    "Old: 'readable visual weight' (ambiguous toward equal weight). r1: 'comparable (not identical) visual weight' (added an unsourced cross-member comparability "
    "restriction). r2: 'readable visual weight coherent with the Ready baseline; identical stroke width or footprint is not required' - keeps BRIEF line 3's "
    "readability outcome and the adopted baseline coherence, adds no comparability rule, and states the not_fixed items explicitly. Otherwise unchanged."
)
c["discriminating_alternative"] = (
    "A Retry mark drawn with 1-px strokes beside Ready's 2-px-reading strokes, equally readable at 1x/3x and coherent in cluster treatment and accent: "
    "brief-conforming. The original 'readable visual weight' could be read to require equal weight; r1's 'comparable visual weight' could reject it as not "
    "comparable; r2 asks only for readability coherent with the baseline and explicitly does not require identical stroke width or footprint. "
    "(Tests the 'visual weight' clause.)"
)
revision_changes.append(
    {
        "finding": "D3",
        "criterion": cid,
        "record_sha256": c["record_sha256"],
        "field": "proposed_check ('visual weight' clause), clause basis/scope/sources, change_explanation, discriminating_alternative",
        "old": old_check,
        "new": c["proposed_check"],
        "old_to_new": "'comparable (not identical) visual weight' -> 'readable visual weight coherent with the Ready baseline (identical stroke width or footprint is not required)'.",
        "basis": "BRIEF line 3 readable silhouettes / coherent assets; state.px line 392 render.choice.style not_fixed (stroke width, margins); caller-comparison-final.json lines 120-125 not_prescribed 'Exact stroke weight, margin or footprint'. No source states a cross-member comparability rule.",
    }
)

# ======================================================================= D4 =====
START_BASIS_LABEL = "requirement by reasonable reading of BRIEF line 3/7 over the view's status set"


def start_basis(member_line: str) -> str:
    return (
        f"{member_line} Distinction from the preserved Start triangle is NOT stated by BRIEF line 3 'Preserve the existing vector Start control' (that sentence "
        "preserves the Start asset and its role). Its actual basis: idle resolves to Start in the same status cells - src/queue-view.ts line 3 "
        "(idle: {label Start, path assets/start.svg, frames 1}) with lines 10-11 (statusCell and compactStatus return statusVisuals[state] for every state) - "
        "so Start is one of the view's status visuals, and 'distinguishable without color alone' read over the view's status set reasonably includes it. "
        f"Label: {START_BASIS_LABEL}. The specialist-authored delivery check listing Start in the grayscale comparison (authoring-plar line 846) is a "
        "proposal consistent with this reading, not its authority."
    )


D4 = [
    (
        "authoring-01.retry.q.retry-meaning-without-color",
        3,
        "BRIEF line 3 'Error/retry must be distinguishable without color alone' (Ready, every Working frame); BRIEF line 7 Paused distinct from retry (mutual).",
        "whole Retry asset; Start inclusion: " + START_BASIS_LABEL + " (src/queue-view.ts lines 3, 10-11)",
    ),
    (
        "authoring-01.paused.q.pause-meaning-without-color",
        3,
        "BRIEF line 7: distinguishable from activity, completion and retry without relying on color alone. No pause-bar motif is required (authoring-plar paused_motif is a proposal).",
        "whole Paused asset; Start inclusion: " + START_BASIS_LABEL + " (src/queue-view.ts lines 3, 10-11)",
    ),
    (
        "authoring-01.delivery.q.distinction",
        4,
        "statusVisuals.idle is the Start descriptor; the assessment records Start as a distinct right-pointing triangle.",
        "collective delivery; Start clause: " + START_BASIS_LABEL + " (src/queue-view.ts lines 3, 10-11)",
    ),
]
for cid, idx, member_line, scope in D4:
    c = by_id[cid]
    cl = c["clauses"][idx]
    old_basis = cl["basis"]
    cl["basis"] = start_basis(member_line)
    cl["scope"] = scope
    extra = [p for p in (QV_IDLE, QV_CONSUMERS, BRIEF_MAIN, BRIEF_PAUSED, AP_R_CHECKS) if p not in cl["source"]]
    cl["source"] = cl["source"] + extra
    c["change_explanation"] = (
        c["change_explanation"]
        + " r2 (basis text only; check text unchanged): the Start clause's basis no longer cites 'Preserve the existing vector Start control'; it rests on "
        "src/queue-view.ts line 3 with lines 10-11 (idle resolves to Start in the same status cells) and is labelled '"
        + START_BASIS_LABEL
        + "'."
    )
    revision_changes.append(
        {
            "finding": "D4",
            "criterion": cid,
            "record_sha256": c["record_sha256"],
            "field": f"clauses[{idx}].basis / scope / source (basis text only; proposed_check unchanged)",
            "old": old_basis,
            "new": cl["basis"],
            "old_to_new": "basis 'BRIEF line 3 preserve the existing vector Start control' -> 'idle resolves to Start in the same status cells (src/queue-view.ts line 3 with lines 10-11); " + START_BASIS_LABEL + "'.",
            "basis": "src/queue-view.ts line 3 (idle descriptor Start) and lines 10-11 (both consumers return statusVisuals[state]); BRIEF line 3 (error/retry without color alone) and line 7 (paused distinct without color alone); authoring-plar line 846 is a specialist delivery check (proposal).",
        }
    )

# ----------------------------------------------------------- top-level edits ----
r2["revision"] = 2
r2["supersedes"] = {
    "path": "work/criteria-review-01/specialist-proposal.json",
    "sha256": EXPECT["work/criteria-review-01/specialist-proposal.json"],
    "report_path": "work/criteria-review-01/specialist-report.json",
    "report_sha256": EXPECT["work/criteria-review-01/specialist-report.json"],
    "relationship": "r1 remains retained and unchanged as the historical specialist proposal; r2 is an artifact-based restart that resolves caller findings D1-D4 and changes nothing else.",
}
r2["role"] = r1["role"] + "; revision 2 (artifact-based restart resolving the caller's findings D1-D4; no generation, no provider request, no store/PLAR/job writes)"
r2["revision_changes"] = revision_changes

summary = r2["summary_of_substantive_corrections"]
summary[0] = (
    "transparent-exterior (working, retry, paused): review route corrected and split (caller decision for any future plan; documented correction only for the "
    "existing Q records). Measured record: alpha histogram + exact RGBA component boxes; all-four-edges / more-than-half-cell component is a DIAGNOSTIC that "
    "triggers visual review, not a rejection rule (r2 demotion; r1 wrote it as a rejection). Mechanical rejection only where decidable: seed-rotation cell alpha "
    "equals cw^k(seed) (Working only). Visual record decides unintended matte/tile/plate/fringe; blanket 'no plate' narrowed to unintended matte/tile."
)
summary[2] = (
    "working.q.motion-continuity: required outcome limited to what BRIEF line 3 and the consumer fix (one continuous activity loop at 100 ms per frame, no "
    "visible discontinuity at the wrap); 'evenly paced' / 'no near-hold' moved to the expert clause set (r2; r1 had placed 'evenly paced' in the required outcome); "
    "anchor/volume remain contract-bound expert clauses; cluster count and no-morphing remain construction-scoped."
)
summary.append(
    "delivery.q.continuity (r2): 'comparable (not identical) visual weight' replaced by 'readable visual weight coherent with the Ready baseline; identical stroke "
    "width or footprint is not required' - no cross-member comparability rule."
)
summary.append(
    "retry/paused meaning-without-color and delivery.q.distinction (r2, basis text only): distinction from Start rests on src/queue-view.ts line 3 with lines 10-11 "
    "(idle resolves to Start in the same status cells), labelled 'requirement by reasonable reading of BRIEF line 3/7 over the view's status set', not on "
    "'Preserve the existing vector Start control'."
)

r2["sources"] = r2["sources"] + [
    {
        "path": KIT_RR,
        "sha256": file_sha(KIT_RR),
        "role": "installed kit guidance cited for D1: line 20 observations alone do not become rejection rules; lines 149-153 mechanical check cannot decide whether a matte is unwanted; line 185 do not turn a diagnostic into a rejection rule",
    },
    {
        "path": KIT_PROFILE,
        "sha256": file_sha(KIT_PROFILE),
        "role": "installed PIXL profile cited for D1: lines 62-67 transparency and subject construction (unintended canvas matte vs deliberate backing)",
    },
]

r2["reduced_motion"]["r2_note"] = (
    "Unchanged from r1 by caller decision. The caller does not adopt P1/M1 here; they remain labelled specialist proposals with the owner decisions open. "
    "The animated four-frame 100 ms strip remains required (BRIEF line 3; AUTHORING-UPDATE.md lines 5-10: the older plan/request remains retained)."
)

hp = r2["historical_preservation"]
hp["statement"] = (
    "No existing file was modified by r1 or r2. The store (state.px revision 88), PLAR files, plan snapshot, stage-request packet, job and all Q records are "
    "untouched; r1 (specialist-proposal.json, specialist-report.json) is retained unchanged; r2 is a separate artifact beside them."
)
for rel in ("work/criteria-review-01/specialist-proposal.json", "work/criteria-review-01/specialist-report.json", "work/criteria-review-01/build_specialist_proposal.py"):
    hp["files"].append({"path": rel, "sha256": sha256(ROOT / rel), "observed": "r1 artifact; unchanged (re-hashed at r2 build time)"})
for entry in hp["files"]:
    actual = sha256(ROOT / entry["path"])
    if actual != entry["sha256"]:
        raise SystemExit(f"historical file changed: {entry['path']} {actual}")
hp["tools_called"] = [
    "r2: file reads, grep, Python -I hashing only (no pixl_asset_check re-run; r1 measurements carried unchanged)",
    *hp["tools_called"],
]
r2["not_claimed"] = r2["not_claimed"] + [
    "that the P1/M1 reduced-motion proposals are adopted (owner decisions open)",
    "that any existing Q record was rewritten (r2 is documented correction; the split applies to a future plan)",
]

# ------------------------------------------------------- integrity checks ----
ids = [c["criterion"] for c in r2["criteria"]]
if ids != [c["criterion"] for c in r1["criteria"]]:
    raise SystemExit("criterion order/identity changed")
for a, b in zip(r1["criteria"], r2["criteria"]):
    for key in ("criterion", "record_sha256", "stage", "output", "original_check", "original_domain", "original_mode", "original_sources"):
        if a[key] != b[key]:
            raise SystemExit(f"historical field changed: {a['criterion']}.{key}")
changed_ids = {rc["criterion"] for rc in revision_changes}
for a, b in zip(r1["criteria"], r2["criteria"]):
    if a["criterion"] not in changed_ids and a != b:
        raise SystemExit(f"unexpected change in untouched criterion {a['criterion']}")
counts = {"keep": 0, "clarify": 0, "correct": 0}
for c in r2["criteria"]:
    counts[c["change"]] += 1

# verify every (path, sha256, lines) pointer in r2 against disk (hash + bounds)
pointers_checked = 0


def walk(obj):
    global pointers_checked
    if isinstance(obj, dict):
        if {"path", "sha256", "lines"} <= set(obj) and isinstance(obj["lines"], list) and len(obj["lines"]) == 2:
            if file_sha(obj["path"]) != obj["sha256"]:
                raise SystemExit(f"pointer hash mismatch: {obj}")
            first, last = obj["lines"]
            if not (1 <= first <= last <= len(file_lines(obj["path"]))):
                raise SystemExit(f"pointer bounds invalid: {obj}")
            pointers_checked += 1
        for v in obj.values():
            walk(v)
    elif isinstance(obj, list):
        for v in obj:
            walk(v)


walk(r2)

# re-verify r1's verified citations (wording still present at the same bounds)
reverified = 0
for cit in r1_report["verified_citations"]:
    first, last = cit["lines"]
    seg = "\n".join(file_lines(cit["path"])[first - 1 : last])
    if cit["verified_wording"] not in seg or file_sha(cit["path"]) != cit["sha256"]:
        raise SystemExit(f"r1 citation no longer verifies: {cit}")
    reverified += 1

# ------------------------------------------------------------------- write ----
proposal_bytes = (json.dumps(r2, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
R2_PROPOSAL.write_bytes(proposal_bytes)
proposal_sha = hashlib.sha256(proposal_bytes).hexdigest()

seen = set()
merged_citations = []
for cit in r1_report["verified_citations"] + new_citations:
    key = (cit["path"], tuple(cit["lines"]), cit["verified_wording"])
    if key in seen:
        continue
    seen.add(key)
    merged_citations.append(cit)

report = {
    "version": 1,
    "revision": 2,
    "kind": "specialist_report",
    "status": "delivered",
    "status_scope": (
        "Revision 2 of the AUTHORING-REVIEW.md specialist deliverable (artifact-based restart): resolves the caller's four findings D1-D4 against the r1 "
        "proposal as NEW files only; all 20 criteria covered with clause-level authority/basis/scope/source; r1 and every historical artifact unchanged. "
        "The caller's independent comparison, coverage check and CRITERIA-RESULT.json remain the caller's work. No generation, request, dispatch or state write occurred."
    ),
    "proposal": {"path": "work/criteria-review-01/specialist-proposal-r2.json", "sha256": proposal_sha},
    "supersedes": r2["supersedes"],
    "reviewed_report": r1_report["reviewed_report"],
    "counts": {"criteria_covered": len(r2["criteria"]), **counts},
    "resolved_findings": [
        {
            "finding": rc["finding"],
            "criterion": rc["criterion"],
            "old_to_new": rc["old_to_new"],
        }
        for rc in revision_changes
    ],
    "caller_decisions_recorded": [
        "D1: adopt the split (measured/diagnostic record + visual record) for any future plan; existing Q records: documented correction only.",
        "Reduced motion: r1 section kept; P1/M1 not adopted; animated strip remains required.",
    ],
    "unchanged_from_r1": "all criteria not named in D1-D4 (13 of 20), choices, measurements, reduced_motion (plus an r2 note), not_claimed (plus two r2 lines)",
    "substantive_corrections": r2["summary_of_substantive_corrections"],
    "verification": {
        "r1_proposal_sha256_at_build": EXPECT["work/criteria-review-01/specialist-proposal.json"],
        "r1_report_sha256_at_build": EXPECT["work/criteria-review-01/specialist-report.json"],
        "criteria_copied_verbatim_from_report": True,
        "historical_fields_identical_to_r1": True,
        "untouched_criteria_identical_to_r1": True,
        "source_pointers_checked_hash_and_bounds": pointers_checked,
        "r1_citations_reverified": reverified,
        "new_citations_verified": len(new_citations),
        "citation_method": "each cited [first,last] range opened from disk and checked to contain the relied-on wording; file hash compared; build aborts on any failure",
        "historical_hashes_rechecked": len(hp["files"]),
        "q_record_lines_checked_in_state_px": r1_report["verification"]["q_record_lines_checked_in_state_px"],
        "measurements": r1_report["verification"]["measurements"],
    },
    "reduced_motion_summary": {**r1_report["reduced_motion_summary"], "r2": "unchanged by caller decision; P1/M1 remain proposals; strip remains required"},
    "questions_for_caller": [
        "Reduced motion (unchanged, owner decisions open): which mapping (renderer rule holding a designated strip cell vs separate static file/descriptor) and which preference source; is distinction from Retry/Start also required for the stationary symbol? The animated strip remains required meanwhile.",
    ],
    "resolved_questions": [
        "Transparent-exterior route: caller adopted the split (measured/diagnostic + visual) for any future plan; existing Q records are documented correction only.",
    ],
    "verified_citations": merged_citations,
}
report_bytes = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
R2_REPORT.write_bytes(report_bytes)
report_sha = hashlib.sha256(report_bytes).hexdigest()

print(json.dumps({
    "proposal": {"path": str(R2_PROPOSAL), "sha256": proposal_sha, "bytes": len(proposal_bytes)},
    "report": {"path": str(R2_REPORT), "sha256": report_sha, "bytes": len(report_bytes)},
    "counts": report["counts"],
    "pointers_checked": pointers_checked,
    "r1_citations_reverified": reverified,
    "new_citations": len(new_citations),
    "revision_changes": [(rc["finding"], rc["criterion"]) for rc in revision_changes],
}, indent=2))
