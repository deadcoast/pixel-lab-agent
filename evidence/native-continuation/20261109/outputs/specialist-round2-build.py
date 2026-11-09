"""Build work/continuation/SPECIALIST-ROUND2.json: PIXL round-2 reconciliation of CALLER-REVIEW-01.json with SPECIALIST-ROUND1.json.

Reads only; writes exactly one new file. Every text citation is opened and verified at build time (one-based inclusive
lines must contain the listed wording); JSON-field citations are verified by path. Hashes come from the actual bytes.
Usage: python -I work/continuation/specialist-round2-build.py CONSUMER_ROOT
"""
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "work/continuation/SPECIALIST-ROUND2.json"
assert not OUT.exists(), "SPECIALIST-ROUND2.json already exists; refuse to overwrite"


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def lines_of(rel):
    return (ROOT / rel).read_text(encoding="utf-8").splitlines()


def jload(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- inputs (verified before use)
EXPECTED = {
    "work/continuation/CALLER-REVIEW-01.json": "513e808bc7bbf02b4ad8d2b5fdd916651136b047bd9a3c357da487838fd95a0e",
    "work/continuation/SPECIALIST-ROUND1.json": "8333476302c408cd42758aa30b3b7247d479d9cb710541adc27179481a1899f5",
    "work/continuation/PHASE1-CALLER.json": "fd3ca89131a78676a32575acc0f4fc9cfb3e8b077e89de028fcb72a404a99d11",
    "work/focused-successor/specialist-proposal.json": "792d4b8f47211a0c646466793e54cc4c16e85c6556bd471f44de2562809b14b3",
    ".pixl/assets/queue.ready/state.px": "3484cf385c91c8c28fa04316fb2c7c5b52c740178b505ccbd88631f57c893c9b",
}
for rel, exp in EXPECTED.items():
    assert sha(rel) == exp, f"identity mismatch {rel}"
caller = jload("work/continuation/CALLER-REVIEW-01.json")
round1 = jload("work/continuation/SPECIALIST-ROUND1.json")
phase1 = jload("work/continuation/PHASE1-CALLER.json")
proposal = jload("work/focused-successor/specialist-proposal.json")
prop = {c["id"]: c for c in proposal["criteria"]}
r1 = {c["id"]: c for c in round1["criteria_classification"]}
assert len(prop) == 29 and len(r1) == 29
assert caller["verdict"]["counts"] == {"keep": 18, "clarify": 9, "correct": 2}
assert [c["id"] for c in caller["corrections"]] == [f"C{i}" for i in range(1, 13)]
assert caller["specialist_round1"]["sha256"] == EXPECTED["work/continuation/SPECIALIST-ROUND1.json"]
assert phase1["caller_review"]["sha256"] == EXPECTED["work/continuation/CALLER-REVIEW-01.json"]
NATIVE_CHILD_ID = phase1["native_child"]["agent_id"]

# ---------------------------------------------------------------- source index (round-1 index + round-2 inputs)
SOURCE_INDEX = dict(round1["sources"])
for key, rel in SOURCE_INDEX.items():
    assert sha(rel["path"]) == rel["sha256"], f"round-1 source changed: {key}"
SOURCE_INDEX.update({
    "caller-review": {"path": "work/continuation/CALLER-REVIEW-01.json", "sha256": sha("work/continuation/CALLER-REVIEW-01.json"), "role": "caller's independent review (round 2 input): C1-C12, 20 original rows, 29 proposed rows, answers Q1/Q2"},
    "round1": {"path": "work/continuation/SPECIALIST-ROUND1.json", "sha256": sha("work/continuation/SPECIALIST-ROUND1.json"), "role": "my round-1 assessment: S1-S12, 29 criteria x 143 clause classifications, mapping check, reduced-motion assessment"},
    "phase1": {"path": "work/continuation/PHASE1-CALLER.json", "sha256": sha("work/continuation/PHASE1-CALLER.json"), "role": "phase-1 caller result; follow_up_for_same_child superseded in one detail (corrected wording goes into SPECIALIST-ROUND2.json)"},
})
assert "authoring-stage" in SOURCE_INDEX and SOURCE_INDEX["authoring-stage"]["sha256"] == "29e73af9a110353dd1453b1bbbb73d7166cf42a0b8eb97f71b53e73701b600aa"

VERIFIED = []


def cite(src, first, last, must):
    text = "\n".join(lines_of(SOURCE_INDEX[src]["path"])[first - 1:last])
    if must not in text:
        raise SystemExit(f"CITATION FAILED {src} {first}-{last}: {must!r}")
    VERIFIED.append([src, first, last, must])
    return {"source": src, "lines": [first, last], "contains": must}


def jcite(src, path, expect=None):
    node = jload(SOURCE_INDEX[src]["path"])
    for part in path.replace("]", "").split("."):
        if "[" in part:
            name, idx = part.split("[")
            node = (node[name] if name else node)[int(idx)]
        else:
            node = node[part]
    if expect is not None and node != expect:
        raise SystemExit(f"JSON CITATION FAILED {src} {path}: {node!r} != {expect!r}")
    VERIFIED.append([src, "json", path, expect if expect is not None else "(exists)"])
    return {"source": src, "field": path, "value": expect if expect is not None else "(exists)"}


# caller locators re-verified by me (all 68)
caller_locators_recheck = []
for name, loc in caller["locators"].items():
    text = "\n".join(lines_of(caller["sources"][loc["source"]]["path"])[loc["lines"][0] - 1:loc["lines"][1]])
    caller_locators_recheck.append({"locator": name, "verified_by_me": loc["expected_wording"] in text})
assert all(x["verified_by_me"] for x in caller_locators_recheck) and len(caller_locators_recheck) == 68

B3_ACTIVITY = cite("brief", 3, 3, "The working loop must communicate activity without looking like success")
B3_RETRY = cite("brief", 3, 3, "Error/retry must be distinguishable without color alone")
B3_SILH = cite("brief", 3, 3, "readable silhouettes")
B3_TRANSP = cite("brief", 3, 3, "Use transparent backgrounds")
B3_FRAMES = cite("brief", 3, 3, "Working uses four horizontal frames with a 100 ms frame duration")
B3_INSPECT = cite("brief", 3, 3, "Inspect at 1x and 3x nearest display scale on the actual dark panel")
B3_BLUE = cite("brief", 3, 3, "the existing UI's cool blue accent")
B7_PAUSED = cite("brief", 7, 7, "distinguishable from activity, completion and retry without relying on color alone")
P422 = cite("plar", 422, 422, "stationary Working symbol distinguishable from Ready and Paused")
P422_NOSUCCESS = cite("plar", 422, 422, "without implying success")
P422_MAPPING = cite("plar", 422, 422, "Confirm its consumer mapping before any further generation")
P_MEANING = cite("plar", 560, 570, "success-like terminal pose")
P_DELIV_WRAP = cite("plar", 606, 619, "Play the loop at 100 ms per frame and inspect the fourth-to-first transition")
A_STEP2 = cite("assignment", 18, 23, "not an owner-imposed motif, palette or frame choice")
A_STEP3_START = cite("assignment", 24, 31, "distinction is a shared-consumer inference")
A_STEP4_PREF = cite("assignment", 32, 43, "respect prefers-reduced-motion and changes while open")
A_STEP4_BOTH = cite("assignment", 32, 43, "both statusCell and")
A_STEP4_REUSE = cite("assignment", 40, 43, "Reuse reviewed existing art when it satisfies the new criteria")
A_STEP6_VIEW = cite("assignment", 52, 58, "Inspect actual output views at native/enlarged scale")
AS_ASSEMBLY = cite("authoring-stage", 31, 32, "frame-selection/assembly policy")
CONT_SCOPE = cite("continuation", 9, 14, "Do not adopt/rewrite production")
CONT_NOPASS = cite("continuation", 27, 27, "Do not turn retained")
V_IDLE = cite("view-ts", 3, 3, 'idle: { label: "Start"')
V_RUNNING = cite("view-ts", 4, 4, "frames: 4")
V_DISPLAY = cite("view-ts", 9, 9, "frameMs: 100")
V_CONSUMERS = cite("view-ts", 10, 11, "compactStatus")
S_IDLE = cite("successor-ts", 7, 7, 'label: "Start"')
S_RUNNING = cite("successor-ts", 8, 8, "frames: 4, still: 0")
S_DISPLAY = cite("successor-ts", 13, 13, "frameMs: 100")
S_STILL = cite("successor-ts", 14, 14, "`still` is the cell held when motion is reduced")
S_DESCRIPTOR = cite("successor-ts", 16, 16, "holdFrame: number | null")
S_MOTION = cite("successor-ts", 17, 19, "matchMedia")
S_DESCRIBE = cite("successor-ts", 20, 23, "holdFrame: animate ? null : visual.still")
S_CONSUMERS = cite("successor-ts", 27, 28, "compactStatus")
F_ELAPSED0 = cite("succ-view", 56, 56, "elapsed = 0")
F_LABEL = cite("succ-view", 62, 62, "label.textContent = descriptor.label")
F_CREATE = cite("succ-view", 69, 69, "info.frame = paint(")
F_MATRIX = cite("succ-view", 95, 95, "for (const scale of [1, display.scale])")
F_LIVE3X = cite("succ-view", 105, 105, "makeCell(consumer, state, display.scale, 0, false)")
F_ANIMATE_LIVE = cite("succ-view", 124, 124, "for (const cell of liveCells) if (cell.canvas && cell.descriptor.animate)")
F_TIMELINE_SYNTH = cite("succ-view", 146, 146, "makeCell(consumer, state, 1, elapsed, false)")
F_LIVE_SAMPLE = cite("succ-view", 157, 157, "elapsed: performance.now() - origin")
C_PHASES = cite("succ-check", 67, 69, '"normal-start": "normal", "reduced": "reduced", "normal-restored": "normal"')
C_LIVE_ONE = cite("succ-check", 140, 140, "frame-boundary tolerance")
C_CYCLE = cite("succ-check", 161, 164, "frames_seen == {0, 1, 2, 3}")
C_SWITCH_RUNNING = cite("succ-check", 180, 180, 'r["state"] == "running"')
C_SCOPE = cite("succ-check", 191, 192, "it does not judge whether the held cell reads as Working")
CAP_PHASES = cite("succ-capture", 4, 5, "as-launched")
CAP_SCOPE = cite("succ-capture", 98, 98, "Mechanical fixture evidence only")
STATE_CAND = cite("state", 259, 259, "dg=~64:cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc")
K_RECIPE = cite("kit-request-review", 32, 32, "Keep a required outcome separate from the recipe")
K_LABEL = cite("kit-request-review", 76, 78, "This label is an assertion to compare")
K_ROUTE = cite("kit-request-review", 172, 181, "review route")
K_REFERENCE = cite("kit-intake", 15, 15, "matching a reference does not adopt every measured dimension")
R2_M1 = jcite("r2", "reduced_motion.d_expert_proposals.consumer_mapping_options[0]", None)
CR_Q1 = jcite("caller-review", "answers_to_specialist_questions.Q1_scope_of_the_criteria_set", None)
CR_Q2 = jcite("caller-review", "answers_to_specialist_questions.Q2_retry_and_start_distinction", None)
R1_S = {sid: jcite("round1", f"defects[{i}].id", sid) for i, sid in enumerate([f"S{n}" for n in range(1, 13)])}
CR_C = {cid: jcite("caller-review", f"corrections[{i}].id", cid) for i, cid in enumerate([f"C{n}" for n in range(1, 13)])}
m1_text = jload(SOURCE_INDEX["r2"]["path"])["reduced_motion"]["d_expert_proposals"]["consumer_mapping_options"][0]
assert m1_text.startswith("M1 - renderer rule")

# ---------------------------------------------------------------- dispositions C1-C12
def disp(cid, disposition, maps_to, basis, text, narrowing=None):
    c = next(x for x in caller["corrections"] if x["id"] == cid)
    return {"id": cid, "caller_severity": c["severity"], "caller_criteria": c["criteria"], "caller_field": c["field"], "caller_finding": c["finding"], "caller_correction": c["correction"],
            "disposition": disposition, "maps_to_round1": maps_to, "source_basis": basis, "reconciliation": text, "narrowing": narrowing, "locator_ref": CR_C[cid]}


dispositions = [
    disp("C1", "agree", ["S1 (blocking)"], [P422, B3_ACTIVITY, A_STEP2, K_RECIPE],
         "Identical finding to S1; the caller's option (b) is adopted: the loop-phase clause leaves the check and becomes an expert clause scoped 'this successor, P1 candidate'. Required outcome retained: Working's own symbol, not success, not pause. Corrected wording below."),
    disp("C2", "narrow", ["S11 (note); round-1 clause classification already split Retry (inference) from Start (inference)"], [B3_RETRY, P422, V_IDLE, V_CONSUMERS, S_IDLE, S_CONSUMERS, A_STEP3_START, CR_Q2],
         "Agree with the per-clause split and with adopting both clauses; agree Start is the D4 shared-consumer inference. Narrow the attribution of the Retry clause: BRIEF line 3 states the Retry obligation over the statuses the view shows, but the held cell is a shown status only because of the caller update (PLAR line 422) and the successor design; so the clause is 'owner requirement (BRIEF line 3) applied to the status set extended by the caller update', not a bare direct reading of the brief. This changes the basis text only; the clause binds as a requirement either way, which agrees with the caller's answer that neither clause is a new owner line.",
         narrowing="Retry clause class = owner (BRIEF line 3) + caller_update (PLAR 422 adds the held cell to the shown status set); label 'requirement'. Start clause class = inference; label 'inference'."),
    disp("C3", "agree", ["S6 (clarify)", "S7 (clarify)"], [P422_MAPPING, A_STEP4_BOTH, S_RUNNING, S_DESCRIBE, S_DESCRIPTOR, R2_M1, K_LABEL],
         "Agree. The descriptor-field clauses (still, holdFrame, animate, motion) are facts of the proposed successor module and are scoped 'this successor destination as designed; re-derive if the module changes'. Verified the M1 example: r2's M1 ('renderer rule ... statusVisuals unchanged') yields descriptors without still/holdFrame, so the literal equality rejects it while PLAR 422 and assignment step 4 are satisfied. Per-clause classes are carried in corrected_criteria below; no outcome changes."),
    disp("C4", "agree", ["S4 (clarify)"], [B3_ACTIVITY, P422, P_MEANING, F_CREATE],
         "Agree. Loop = owner; held cell = caller update (bound by stationary-meaning); transient cells 1-3 seen singly = expert clause with the 100 ms / painted-at-creation rationale. Corrected wording below."),
    disp("C5", "agree", ["not raised in round 1 as a defect; round-1 clause classification already classed the cell choice as expert_choice (criteria_classification[stationary-cell-identity].clauses[0])"], [S_RUNNING, S_STILL, A_STEP2],
         "Agree. The record-level label 'observation' hides the cell-0 choice, which is my P1 proposal bound to the proposed module's still: 0. Corrected label 'proposal (cell choice) + observation (measurements)'; the measurement record and the redo rule are kept verbatim."),
    disp("C6", "agree", ["S8 (note) covers the 224/32 wording; the construction clause itself was classed expert_choice in round 1 but not raised as a label defect"], [B3_TRANSP, K_REFERENCE],
         "Agree. The construction-scoped rejection clause is an expert construction choice and is labelled 'proposal (seed-rotation construction only)'; the four-edge / >half-cell flag stays diagnostic; the S8 wording ('for the current seed 21f5baca...: measured 224 alpha-0 / 32 alpha-255 per cell') is applied."),
    disp("C7", "agree", ["S2 (clarify; caller severity note)"], [F_LABEL, B3_SILH],
         "Agree on substance: the glyph must carry the non-success/non-pause reading by itself; the label may be present as the consumers render it. Severity is the caller's; the corrected wording judges the glyph alone and then beside the label."),
    disp("C8", "agree", ["unavailable_or_not_claimed in round 1"], [CONT_SCOPE, CONT_NOPASS, CAP_SCOPE, C_SCOPE],
         "Agree. No fixture capture (render-01 has no render.json; its launch.json project is another root), no check.py run, no inspection views, no playback viewed; nothing becomes a pass here."),
    disp("C9", "agree", ["reuse judgement accepted in round 1 (reduced_motion_assessment.measurements.agreement_with_proposal)"], [STATE_CAND],
         "Agree. state.px line 259 binds live.working-animation-motion-01.candidate to dg cf101610..., which equals assets/working.png; the mechanical reuse records are reproduced by both parties; the preliminary visual list is not acceptance."),
    disp("C10", "narrow", ["S5 (clarify)"], [F_LIVE_SAMPLE, C_LIVE_ONE, F_TIMELINE_SYNTH, C_CYCLE, C_SCOPE, F_LIVE3X, F_ANIMATE_LIVE, F_MATRIX, F_ELAPSED0, P_DELIV_WRAP, K_ROUTE],
         "Agree with the finding and with keeping the three legs separate. Narrow the named route: 'caller viewing of the live page under normal motion at 1x and 3x' is only partly available in the fixture as designed, because the live cells are created at display.scale (3) only (view.mjs line 105) and animate() repaints only liveCells (line 124); the 1x matrix cells are painted once at elapsed 0 (lines 56, 95) and never animate. So the 3x playback leg can be viewed on the live page; the 1x playback leg needs either a fixture change (a 1x live cell) or a separately labelled viewing aid. The corrected evidence route says so.",
         narrowing="playback route: 3x = live fixture page under normal motion (visual observation); 1x = not available in the current fixture; requires a fixture change or a labelled viewing aid; frame content per boundary = synthetic timeline crops (mechanical); wall-clock cadence not measured."),
    disp("C11", "agree", ["S3 (clarify)"], [AS_ASSEMBLY, A_STEP4_REUSE],
         "Agree (adopted from S3). AUTHORING-STAGE.md (sha256 29e73af9...) is in this file's source index; lines 31-32 are cited for the assembly clause; FOCUSED-SUCCESSOR 40-43 remain the reuse authorisation."),
    disp("C12", "agree", ["S12 (note)"], [C_SWITCH_RUNNING, C_PHASES, CAP_PHASES],
         "Agree (adopted from S12). 'Other states repaint unchanged' and the as-launched forced-reduced startup path are labelled caller visual observations on the reduced-phase screenshot unless the two assertions are added to check.py at production time; no outcome change."),
]
accepted_notes = {
    "S8": {"status": "accepted by the caller as a wording note; applied in corrected transparent-exterior-measured (working)", "ref": R1_S["S8"]},
    "S9": {"status": "accepted by the caller as a basis note; applied as basis text in the three style-coherence criteria (Start-accent relation = inference from assets/start.svg fill #70b9ed); check unchanged", "ref": R1_S["S9"]},
    "S10": {"status": "accepted by the caller as a basis note; applied as basis text in stationary-distinct-ready-paused and delivery.distinction (non-colour condition for the held-vs-Ready pair = inference/adopted method); check unchanged", "ref": R1_S["S10"]},
    "S11": {"status": "superseded by C2 (narrowed above)", "ref": R1_S["S11"]},
    "S7": {"status": "subsumed by C3 (per-clause authority classes)", "ref": R1_S["S7"]},
}
counts = {k: sum(1 for d in dispositions if d["disposition"] == k) for k in ("agree", "narrow", "challenge")}

# ---------------------------------------------------------------- corrected criteria (beside, never over, the original)
CLASSES = dict(round1["conventions"]["authority_classes"])
CLASSES["owner+caller_update"] = "owner line applied to a status set the caller update extended (the held cell is a shown status only because of PLAR line 422)"
SCOPE_IMPL = "this successor destination as designed (src/queue-view-successor.ts + renderer-successor/); re-derive if the module changes"
ROUTE_FIXTURE = "renderer-successor capture + check.py (destination/mechanical); no capture exists yet"


def rc(cid, status, corrected_check, label, clauses, explanation, maps_to, expert_clauses=None, evidence_route=None, sources_added=None):
    o = prop[cid]
    for c in clauses:
        assert c["class"] in CLASSES, c["class"]
    return {"id": cid, "status": status, "original_check": o["check"], "original_authority": o["authority"], "original_scope": o["scope"], "domain": o["domain"], "mode": o["mode"],
            "carries": [k["id"] for k in o.get("carries", [])], "corrected_check": corrected_check if corrected_check is not None else "(unchanged)",
            "authority_label_for_record": label, "clauses": clauses, "expert_clauses": expert_clauses if expert_clauses is not None else [e["text"] for e in o.get("expert_clauses", [])],
            "evidence_route": evidence_route if evidence_route is not None else o.get("evidence_route"), "sources_added": sources_added or [], "change_explanation": explanation, "maps_to": maps_to}


def c(text, klass, scope, basis=None):
    d = {"text": text, "class": klass, "scope": scope}
    if basis:
        d["basis"] = basis
    return d


def r1_clauses(cid, overrides=None):
    """Copy round-1 clause classification (text/class/scope) with optional per-index overrides."""
    overrides = overrides or {}
    out = []
    for i, cl in enumerate(r1[cid]["clauses"]):
        d = {"text": cl["text"], "class": cl["class"], "scope": cl["scope"]}
        d.update(overrides.get(i, {}))
        out.append(d)
    return out


STYLE_NOTE = "basis note (S9 accepted): the relation to the preserved Start accent is an inference from assets/start.svg fill #70b9ed; the owner line binds a perceptible cool-blue accent, not a hue or an extent"
corrected = [
    rc("successor-01.working.q.geometry", "authority/scope and descriptive wording corrected",
       "Decode assets/working.png as exactly 64x16: four horizontal 16x16 cells at x=0,16,32,48 with no gutters or added canvas between or around the cells (transparent margin inside a cell is composition, not padding). Consumer basis (unchanged original module src/queue-view.ts lines 4 and 9; identical constants in the proposed successor module lines 8 and 13): running frames 4 (the sheet's cell count, unchanged under either preference), display.cell [16,16] and frameMs 100. Fixture behaviour, descriptive only and scoped to this successor destination as designed: the successor fixture draws only when width == 16*frames and height == 16, slices frame*16,0,16,16 and derives the frame from frameAt() (floor(elapsed/100) mod 4 when animating; the held cell otherwise).",
       "requirement (sheet geometry: owner + original consumer); fixture clause descriptive",
       r1_clauses("successor-01.working.q.geometry", {2: {"class": "consumer_fact_original", "scope": "whole sheet; the proposed module repeats the same constants"}, 3: {"scope": SCOPE_IMPL}}),
       "C3/S7: the geometry obligation is attributed to the owner line and the unchanged original module so it does not depend on adopting the successor module; the fixture sentence is marked descriptive and scoped to the implementation. Outcome unchanged.", ["C3", "S7"]),
    rc("successor-01.working.q.transparent-exterior-measured", "authority split and wording corrected",
       "MEASURED record (mechanical/local, diagnostic): retain every cell's alpha histogram and exact RGBA component boxes (zero-based, half-open). FLAG for visual review any alpha>0 component touching all four cell edges, or any single alpha>0 component covering more than half of the cell's 256 pixels. The flag is a diagnostic proxy for a canvas matte or grey tile and is NOT a rejection condition (a corner-to-corner X or full-span glyph legitimately touches all four edges with a transparent exterior). RGB values of alpha-0 pixels are not significant. PROPOSAL (seed-rotation construction only): mechanical REJECTION is decidable only under that construction, where each cell's alpha channel must equal that of cw^k(seed) under dst(x,y)=src(y,15-x) (for the current seed 21f5baca...: measured 224 alpha-0 / 32 alpha-255 pixels per cell). Outside that construction the measured record carries no rejection rule.",
       "observation (measurement and flag) + proposal (construction-scoped rejection clause)",
       r1_clauses("successor-01.working.q.transparent-exterior-measured", {3: {"class": "expert_choice", "scope": "seed-rotation construction only (proposal)"}}),
       "C6: the construction-scoped rejection clause is labelled proposal; S8: the 224/32 counts are stated as measured values of the current seed. Flag stays diagnostic; D1 split unchanged.", ["C6", "S8"]),
    rc("successor-01.working.q.transparent-exterior-visual", "unchanged", None, prop["successor-01.working.q.transparent-exterior-visual"]["authority"], r1_clauses("successor-01.working.q.transparent-exterior-visual"), "No change (caller keep).", []),
    rc("successor-01.working.q.frame-assembly", "sources/basis corrected (check unchanged)", None, "requirement (assignment process requirement, AUTHORING-STAGE.md 31-32) with a reuse-case provenance record; construction clause proposal",
       r1_clauses("successor-01.working.q.frame-assembly"),
       "C11/S3: the assembly-policy obligation is cited to AUTHORING-STAGE.md lines 31-32 (added to the source index); FOCUSED-SUCCESSOR lines 40-43 remain the reuse authorisation. Check text unchanged.", ["C11", "S3"],
       sources_added=[{"id": "authoring-stage", "lines": [31, 32], "locator": "stage-assembly", "sha256": SOURCE_INDEX["authoring-stage"]["sha256"]}]),
    rc("successor-01.working.q.activity-not-success", "check and scope corrected",
       "Viewed at 1x and 3x nearest on #172336 (beside the exact Ready baseline as the comparison method). REQUIRED (owner, BRIEF line 3; PLAR 560-570 state_meaning): the running loop reads as ongoing activity and not as completion, with no completion/success silhouette or success-like terminal pose in the loop. REQUIRED (caller update, PLAR line 422; judged in stationary-meaning): the held cell, shown alone under reduced motion, reads as activity and not as completion. EXPERT CLAUSE (specialist; scope this successor): each transient frame (cells 1-3), seen singly, also reads as activity rather than completion, because frames are exposed singly for 100 ms and frame 0 is painted at cell creation.",
       "requirement (loop: owner; held cell: caller update) + proposal (transient frames singly)",
       [c("the running loop reads as ongoing activity and not as completion ... no completion/success silhouette or success-like terminal pose in the loop", "owner", "whole asset"),
        c("the held cell, shown alone under reduced motion, reads as activity and not as completion", "caller_update", "held cell (judged in stationary-meaning)"),
        c("each transient frame (cells 1-3), seen singly, also reads as activity rather than completion", "expert_choice", "this successor; specialist clause with the 100 ms / painted-at-creation rationale"),
        c("beside the exact Ready baseline as the comparison method", "method", "method"),
        c("Viewed at 1x and 3x nearest on #172336", "owner", "review conditions")],
       "C4/S4: the per-frame clause is split out of the owner requirement; loop and held cell remain required; transient frames become a scoped expert clause.", ["C4", "S4"]),
    rc("successor-01.working.q.motion-continuity", "evidence route named (check unchanged)", None, "requirement (one continuous loop at the consumer's 100 ms with no visible wrap discontinuity) + expert clauses (D2)",
       r1_clauses("successor-01.working.q.motion-continuity"),
       "C10/S5 (narrowed): the actual-playback leg is routed to caller viewing of the live fixture page under normal motion, which exists only at 3x as the fixture stands (live cells at display.scale, view.mjs line 105; animate() repaints only liveCells, line 124; the 1x matrix is painted once at elapsed 0, lines 56 and 95). Check text unchanged.", ["C10", "S5"],
       evidence_route="Three separate legs: (1) frameMs 100 constant in the consumer module = mechanical; (2) frame-index arithmetic on the synthetic capture timeline incl. the 400 ms wrap = mechanical (check.py 148-166); (3) actual playback = visual/temporal: caller viewing of the live fixture page under normal motion, available at 3x only in the current fixture; 1x playback requires a fixture change (a 1x live cell) or a separately labelled viewing aid; recorded as a visual observation, never as a checker pass. Wall-clock cadence is not measured and not claimed."),
    rc("successor-01.working.q.style-coherence", "per-clause authority carried (check unchanged)", None, "requirement (owner readability/accent/inspection) + adopted scoped caller decision (compact, deliberate clusters, stepped edges) + inference (Start-accent relation)",
       r1_clauses("successor-01.working.q.style-coherence"), "C3/S7 per-clause classes; " + STYLE_NOTE, ["C3", "S9"]),
    rc("successor-01.working.q.consumers-normal-motion", "check corrected (descriptor scope, temporal evidence)",
       "In the successor browser fixture renderer-successor/view.mjs executing the actual src/queue.ts and src/queue-view-successor.ts modules, checked by renderer-successor/check.py against the retained capture, with the preference resolving to normal, exercise started -> running through stateAfter. REQUIRED (caller update PLAR 422 consumer mapping; assignment step 4 both consumers): statusCell and compactStatus resolve the same Working visual for the running state, and the live cells (scale 3) and the state-matrix cells (scale 1 and 3) render assets/working.png with imageSmoothingEnabled false / image-rendering pixelated, composited over #172336, geometryMatches true. CONSUMER-CODE FACT of the proposed successor module (scope: this successor destination as designed; re-derive if the module changes): the identical descriptor is {label Working, path assets/working.png, frames 4, still 0, motion normal, animate true, holdFrame null}. Frame-advance evidence as the checker asserts (mechanical): the synthetic capture timeline (cells painted at chosen elapsed values) reports frame indices 0,0,1,1,2,2,3,3,0 at elapsed 0,99,100,199,200,299,300,399,400 ms (floor(elapsed/100) mod 4; wrap at 400 ms) and covers all four cells; each live cell is sampled once and its frame agrees with its elapsed time within the frame-boundary tolerance. Not asserted by this criterion: cycling of the live requestAnimationFrame loop and wall-clock frame duration; actual playback is the visual/temporal leg of motion-continuity.",
       "requirement (outcome: caller update + assignment + owner display conditions) with implementation-scoped consumer-code facts and bounded mechanical temporal evidence",
       r1_clauses("successor-01.working.q.consumers-normal-motion", {2: {"scope": SCOPE_IMPL}, 6: {"text": "each live cell is sampled once and its frame agrees with its elapsed time within the frame-boundary tolerance (live cycling not asserted)", "class": "checker_fact", "scope": "mechanical temporal evidence"}}),
       "C3/S6: descriptor equality scoped to the implementation; C10/S5: the overclaimed 'live loop observed cycling' is replaced by what check.py asserts (single live sample; cycling on the synthetic timeline); wall-clock still not claimed.", ["C3", "C10", "S5", "S6"],
       evidence_route=ROUTE_FIXTURE + "; playback leg routed in motion-continuity"),
    rc("successor-01.working.q.stationary-cell-identity", "authority label corrected",
       "PROPOSAL (P1; specialist cell choice bound to the proposed module's statusVisuals.running.still = 0, painted when animate is false): the stationary Working symbol is cell 0 of assets/working.png, the crop (0,0,16,16) in zero-based half-open coordinates. OBSERVATION (measured on cf101610... frame 0): visible pixels 32, three 4-connected components with boxes [[5, 3, 10, 5], [12, 6, 14, 11], [3, 10, 8, 14]] (half-open, zero-based), visible box [3, 3, 14, 14], mass centroid [7.906, 9.0] in pixel-edge coordinates (canvas centre 8.0,8.0), alpha histogram {'0': 224, '255': 32}; cell 0 equals the accepted seed (sha256 21f5baca...) on alpha and visible RGBA. The visual criteria are judged on exactly this cell; if `still` changes, the identity record and those visual verdicts must be redone.",
       "proposal (cell choice) + observation (measurements)", r1_clauses("successor-01.working.q.stationary-cell-identity", {0: {"scope": "P1 candidate; " + SCOPE_IMPL}}),
       "C5: the record label now shows the cell-0 choice as a proposal; the measurement record and the redo rule are unchanged.", ["C5"]),
    rc("successor-01.working.q.stationary-distinct-ready-paused", "per-clause authority carried (check unchanged)", None, "requirement (caller update: distinguishable from Ready and Paused; owner: non-colour for the Paused pair) + inference/method (non-colour for the Ready pair)",
       r1_clauses("successor-01.working.q.stationary-distinct-ready-paused"), "C3 per-clause classes; S10 accepted: the non-colour condition for the held-vs-Ready pair is an inference/adopted method, stated in the basis; check unchanged.", ["C3", "S10"]),
    rc("successor-01.working.q.stationary-distinct-retry-start", "check split per clause; authority corrected",
       "Viewed stationary at 1x and 3x nearest on #172336, in colour and in a non-colour comparison. (a) REQUIREMENT (owner BRIEF line 3 'Error/retry must be distinguishable without color alone', read over the statuses the view shows; the held cell is a shown status by the caller update PLAR line 422): the held cell is distinguishable by shape or structure alone from the Retry mark (assets/error-retry.png) and does not read as failure/retry. (b) INFERENCE (shared-consumer, D4; adopted by the caller, not an owner line: idle resolves to Start in the same status cells through both consumers in the original module src/queue-view.ts lines 3, 10-11 and the successor lines 7, 27-28): the held cell is distinguishable by shape or structure alone from the preserved Start triangle (assets/start.svg as rendered in the idle cell) and does not read as the Start control.",
       "requirement (clause a, owner + caller update) / inference (clause b)",
       [c("(a) distinguishable by shape or structure alone from the Retry mark and does not read as failure/retry", "owner+caller_update", "held cell vs Retry; whole successor", "BRIEF line 3 over the shown status set; PLAR 422 makes the held cell a shown status"),
        c("(b) distinguishable by shape or structure alone from the preserved Start triangle and does not read as the Start control", "inference", "held cell vs Start; adopted by the caller (Q2)", "shared-consumer inference (D4): view-ts 3, 10-11; successor-ts 7, 27-28"),
        c("Viewed stationary at 1x and 3x nearest on #172336, in colour and in a non-colour comparison", "owner", "review conditions"),
        c("assets/start.svg as rendered in the idle cell", "honest_limit", "the prior rasterised Start is a comparison aid; browser rendering not yet viewed")],
       "C2 (narrowed) / S11: the two clauses carry separate labels; Retry = requirement (owner line applied to the caller-extended status set), Start = inference; both adopted per the caller's Q2 answer.", ["C2", "S11"]),
    rc("successor-01.working.q.stationary-meaning", "check corrected; P1 clause moved to expert clauses",
       "Viewed stationary at 1x and 3x on #172336, the held cell is judged alone and then beside its consumer label as the consumers render it: by itself it reads as the Working status's own symbol, does not read as success (no check mark or terminal pose) and does not read as pause; the label is viewing context and does not carry this reading.",
       "requirement (owner BRIEF line 3 / PLAR 422 non-success; caller update non-pause)",
       [c("reads as the Working status's own symbol and does not read as success (no check mark or terminal pose)", "owner", "held cell", "BRIEF line 3; PLAR 422 'without implying success'"),
        c("does not read as pause", "caller_update", "held cell", "PLAR 422 distinct from Paused; BRIEF line 7 mutual"),
        c("judged alone and then beside its consumer label ...; the label is viewing context and does not carry this reading", "method", "review method", "C7/S2: the glyph carries the reading; label rendered by both consumers (view.mjs 62)"),
        c("Viewed stationary at 1x and 3x on #172336", "owner", "review conditions")],
       "C1/S1 (option b): the loop-phase identity clause is removed from the check and kept as an expert clause scoped to the P1 candidate; C7/S2: the glyph is judged alone and beside the label. Required outcome unchanged. The frozen-spinner 'stalled' limit remains recorded.", ["C1", "C7", "S1", "S2"],
       expert_clauses=["PROPOSAL (this successor, P1 candidate only): prefer a held cell that is literally a phase of the Working loop, so the stationary and animated forms share identity and the preference switch repaints in place without changing the symbol.",
                       "OBSERVATION (fixture/consumer behaviour, view.mjs line 62): the text label 'Working' is rendered beside the glyph in both consumers; it is context, not a carrier of the required reading.",
                       "HONEST LIMIT: a frozen spinner communicates 'in progress / busy' by UI idiom but can also read as 'stalled'; no source requires the stationary symbol to convey motion; accepting frozen-spinner semantics is an owner/caller decision (P1 vs P2)."]),
    rc("successor-01.working.q.reduced-motion-consumer-mapping", "check corrected (descriptor scope; checker-support labels)",
       "In the successor browser fixture renderer-successor/view.mjs executing the actual src/queue.ts and src/queue-view-successor.ts modules, checked by renderer-successor/check.py against the retained capture, with the preference resolving to reduced ((prefers-reduced-motion: reduce) matches; the preference mechanism is fixed by assignment step 4), exercise started -> running through stateAfter. REQUIRED (caller update PLAR line 422 'confirm its consumer mapping'; assignment step 4 both consumers): statusCell and compactStatus resolve one and the same stationary Working visual, no animation loop repaints Working cells, every Working cell (live 3x, matrix 1x and 3x) shows the designated held cell, and the sheet geometry stays 64x16 with frames 4 under both preferences (owner: frames is the sheet's cell count, never changed by the preference). CONSUMER-CODE FACTS of the proposed successor module (scope: this successor destination as designed; re-derive if the module changes): the identical descriptor is {label Working, path assets/working.png, frames 4, still 0, motion reduced, animate false, holdFrame 0} (under normal {..., motion normal, animate true, holdFrame null}); the held cell index is holdFrame = still = 0 and the capture timeline reports frame 0 at every sample point (0..400 ms); the static members (Start, Ready, Paused, Retry) resolve animate false / holdFrame 0 with frames 1 under both preferences; the default preference source is matchMedia('(prefers-reduced-motion: reduce)') consulted by both consumers through motionPreference(), and an explicit motion argument overrides it identically for both.",
       "requirement (outcome: caller update + assignment + owner geometry) with implementation-scoped consumer-code facts",
       r1_clauses("successor-01.working.q.reduced-motion-consumer-mapping", {2: {"scope": SCOPE_IMPL}, 5: {"scope": SCOPE_IMPL}, 6: {"scope": SCOPE_IMPL}}),
       "C3/S6: outcome clauses separated from the proposed module's descriptor shape, which is scoped to the implementation; C12/S12: the as-launched forced-reduced startup run is labelled a caller visual observation unless check.py gains an expected-motion assertion for that phase.", ["C3", "C12", "S6", "S12"],
       evidence_route="renderer-successor capture phase 'reduced' (DevTools media emulation) + check.py; the as-launched run with --force-prefers-reduced-motion is NOT asserted by check.py (lines 67-69 map only the three default phases) and counts as a caller visual observation on its screenshot unless the assertion is added at production time; no capture exists yet"),
    rc("successor-01.working.q.live-preference-switch", "check corrected (descriptor scope; checker-support labels)",
       "With the page open and Working shown (live cells and the state matrix in both consumers), change the preference in the same page session. REQUIRED (assignment step 4 'changes while open', step 6 'switching the preference in the same session', step 3): on the media query change event every Working cell in both consumers (statusCell and compactStatus; live 3x; matrix 1x and 3x) is re-derived from the same consumer under the new preference and repainted in place, with no reload: stationary on the designated held cell when the preference becomes reduced, and cycling again when it returns to normal. CONSUMER-CODE FACTS of the proposed successor module and fixture (scope: this successor destination as designed; re-derive if the module changes): the repainted descriptors read animate false, frame == holdFrame == 0 under reduced and animate true, holdFrame null under normal; cycling after restore is asserted on the normal-restored synthetic timeline (all four cells); one sessionId across all phases, the change event recorded with from/to and the repainted cell list, and the live Working cells among the repainted cells. CALLER VISUAL OBSERVATION on the reduced-phase screenshot (not asserted by check.py, whose [switch] block inspects only running cells) unless an assertion is added at production time: other states repaint unchanged.",
       "requirement (assignment process requirement) with implementation-scoped consumer-code/fixture facts and one caller visual observation",
       r1_clauses("successor-01.working.q.live-preference-switch", {1: {"scope": SCOPE_IMPL}, 3: {"class": "method", "scope": "caller visual observation on the reduced-phase screenshot, or a check.py assertion added at production time"}}),
       "C3/S6: descriptor shape scoped; C12/S12: 'other states repaint unchanged' labelled a caller visual observation; 'all four cells observed' bound to the synthetic timeline.", ["C3", "C12", "S6", "S12"]),
    rc("successor-01.retry.q.geometry", "unchanged", None, prop["successor-01.retry.q.geometry"]["authority"], r1_clauses("successor-01.retry.q.geometry"), "No change (caller keep).", []),
    rc("successor-01.retry.q.transparent-exterior-measured", "unchanged", None, prop["successor-01.retry.q.transparent-exterior-measured"]["authority"], r1_clauses("successor-01.retry.q.transparent-exterior-measured"), "No change (caller keep).", []),
    rc("successor-01.retry.q.transparent-exterior-visual", "unchanged", None, prop["successor-01.retry.q.transparent-exterior-visual"]["authority"], r1_clauses("successor-01.retry.q.transparent-exterior-visual"), "No change (caller keep).", []),
    rc("successor-01.retry.q.retry-meaning-without-color", "per-clause authority carried (check unchanged)", None, "requirement (owner line 3 over the shown status set incl. the held cell via PLAR 422) / inference (Start clause)",
       r1_clauses("successor-01.retry.q.retry-meaning-without-color", {1: {"class": "owner+caller_update", "scope": "whole Retry asset; the held cell is a shown status by PLAR 422"}}),
       "C2 (narrowed): Retry-versus-held-cell = owner line applied to the caller-extended status set; Start = inference (D4). Check unchanged.", ["C2"]),
    rc("successor-01.retry.q.style-coherence", "per-clause authority carried (check unchanged)", None, "requirement + adopted scoped caller decision + inference (Start-accent relation)", r1_clauses("successor-01.retry.q.style-coherence"), "C3 per-clause classes; " + STYLE_NOTE, ["C3", "S9"]),
    rc("successor-01.retry.q.consumers", "check corrected (descriptor scope)",
       "In the successor browser fixture renderer-successor/view.mjs executing the actual src/queue.ts and src/queue-view-successor.ts modules, checked by renderer-successor/check.py against the retained capture, exercise error -> failed through stateAfter under both preferences. REQUIRED (owner BRIEF lines 3 and 7; original module line 7; assignment step 4 both consumers): statusCell and compactStatus resolve the same Retry visual {label Retry, path assets/error-retry.png, frames 1}, the live cells (scale 3) and the state-matrix cells (scale 1 and 3) render the PNG with imageSmoothingEnabled false / image-rendering pixelated over #172336, geometryMatches true, and the static member does not animate under either preference. CONSUMER-CODE FACT of the proposed successor module (scope: this successor destination as designed; re-derive if the module changes): the identical descriptor is {label Retry, path assets/error-retry.png, frames 1, still 0, animate false, holdFrame 0}; static behaviour follows the frames > 1 gate in describe().",
       "requirement (outcome) with implementation-scoped consumer-code facts", r1_clauses("successor-01.retry.q.consumers", {2: {"scope": SCOPE_IMPL}, 5: {"scope": SCOPE_IMPL}}),
       "C3/S6: label/path/frames and static behaviour remain required (owner + original module); still/animate/holdFrame scoped to the implementation.", ["C3", "S6"]),
    rc("successor-01.paused.q.geometry", "unchanged", None, prop["successor-01.paused.q.geometry"]["authority"], r1_clauses("successor-01.paused.q.geometry"), "No change (caller keep).", []),
    rc("successor-01.paused.q.transparent-exterior-measured", "unchanged", None, prop["successor-01.paused.q.transparent-exterior-measured"]["authority"], r1_clauses("successor-01.paused.q.transparent-exterior-measured"), "No change (caller keep).", []),
    rc("successor-01.paused.q.transparent-exterior-visual", "unchanged", None, prop["successor-01.paused.q.transparent-exterior-visual"]["authority"], r1_clauses("successor-01.paused.q.transparent-exterior-visual"), "No change (caller keep).", []),
    rc("successor-01.paused.q.pause-meaning-without-color", "per-clause authority carried (check unchanged)", None, "requirement (owner BRIEF line 7 incl. the held cell as activity) / inference (Start clause)",
       r1_clauses("successor-01.paused.q.pause-meaning-without-color"), "C2: Start clause labelled inference (D4); the held-cell inclusion is owner-grounded here (line 7 'activity'). Check unchanged.", ["C2"]),
    rc("successor-01.paused.q.style-coherence", "per-clause authority carried (check unchanged)", None, "requirement + adopted scoped caller decision + inference (Start-accent relation)", r1_clauses("successor-01.paused.q.style-coherence"), "C3 per-clause classes; " + STYLE_NOTE, ["C3", "S9"]),
    rc("successor-01.paused.q.consumers", "check corrected (descriptor scope)",
       "In the successor browser fixture renderer-successor/view.mjs executing the actual src/queue.ts and src/queue-view-successor.ts modules, checked by renderer-successor/check.py against the retained capture, exercise pause -> paused through stateAfter under both preferences. REQUIRED (owner BRIEF lines 3, 5 and 7; original module line 5; assignment step 4 both consumers): statusCell and compactStatus resolve the same Paused visual {label Paused, path assets/paused.png, frames 1}, the live cells (scale 3) and the state-matrix cells (scale 1 and 3) render the PNG with imageSmoothingEnabled false / image-rendering pixelated over #172336, geometryMatches true, and the static member does not animate under either preference. CONSUMER-CODE FACT of the proposed successor module (scope: this successor destination as designed; re-derive if the module changes): the identical descriptor is {label Paused, path assets/paused.png, frames 1, still 0, animate false, holdFrame 0}; static behaviour follows the frames > 1 gate in describe().",
       "requirement (outcome) with implementation-scoped consumer-code facts", r1_clauses("successor-01.paused.q.consumers", {2: {"scope": SCOPE_IMPL}, 5: {"scope": SCOPE_IMPL}}),
       "C3/S6 as for the Retry consumers criterion.", ["C3", "S6"]),
    rc("successor-01.delivery.q.continuity", "evidence route named (check unchanged)", None, "requirement (owner coherence/accent/transparency/inspection + caller update held cell) + adopted baseline decision; D3 wording retained",
       r1_clauses("successor-01.delivery.q.continuity"), "C10/S5 (narrowed): the 'actual 100 ms playback with the wrap' leg uses the motion-continuity route (3x live page; 1x needs a fixture change or a labelled aid); check unchanged.", ["C10", "S5"],
       evidence_route="saved views from both fixture phases (normal and reduced) for the stills; the playback leg as routed in motion-continuity (3x live page viewing; 1x not available in the current fixture); no capture exists yet"),
    rc("successor-01.delivery.q.distinction", "per-clause authority carried (check unchanged)", None, "requirement (owner lines 3/7; caller update held cell) / inference (Start clause; non-colour for the held-vs-Ready pair)",
       r1_clauses("successor-01.delivery.q.distinction"), "C2: Start clause labelled inference (D4 settled; caller disposition keep); S10 accepted as basis note. Check unchanged.", ["C2", "S10"]),
    rc("successor-01.delivery.q.destination", "per-clause authority carried (check unchanged)", None, "requirement (owner paths/Start/inspection; assignment destination files; original transitions) with fixture/checker facts and the adopted integer-placement method; temporal leg bounded",
       r1_clauses("successor-01.delivery.q.destination", {3: {"scope": "mechanical temporal evidence; the actual-playback leg is routed in motion-continuity"}}),
       "C3 per-clause classes; the '100 ms timing' leg stays bounded to the consumer constant and frame-index arithmetic (wall-clock not measured); check unchanged.", ["C3", "S5"]),
]
assert len(corrected) == 29 and {x["id"] for x in corrected} == set(prop)
changed_text = [x["id"] for x in corrected if x["corrected_check"] != "(unchanged)"]
changed_other = [x["id"] for x in corrected if x["corrected_check"] == "(unchanged)" and x["status"] != "unchanged"]
unchanged = [x["id"] for x in corrected if x["status"] == "unchanged"]
assert len(changed_text) + len(changed_other) + len(unchanged) == 29

# ---------------------------------------------------------------- retained comparison (by reference to phase-1 rows)
VALIDATE_HASHES = {r["original_id"]: r["record_sha256"] for r in round1["mapping_check"]["rows"]}
assert len(VALIDATE_HASHES) == 20
cr_orig = {r["id"]: r for r in caller["original_criteria"]}
assert set(cr_orig) == set(VALIDATE_HASHES) and all(cr_orig[k]["record_sha256"] == v for k, v in VALIDATE_HASHES.items())
for m in proposal["mapping"]:
    assert m["record_sha256"] == VALIDATE_HASHES[m["original_id"]] and m["original_check"] == cr_orig[m["original_id"]]["check"]
retained_comparison = {
    "statement": "The exact 20-original / 29-proposed comparison is retained by reference, not re-authored: the 20 ids, record hashes and literal checks are identical in CALLER-REVIEW-01.json.original_criteria, SPECIALIST-ROUND1.json.mapping_check.rows, the proposal's mapping and the context packet (all re-checked here against pixl_validate revision 88 hashes copied in round 1); the 29 proposed literal checks are quoted verbatim in corrected_criteria[*].original_check.",
    "original_20": [{"id": k, "record_sha256": v} for k, v in sorted(VALIDATE_HASHES.items())],
    "phase1_rows": {"caller_review": {"path": SOURCE_INDEX["caller-review"]["path"], "sha256": SOURCE_INDEX["caller-review"]["sha256"], "fields": "original_criteria (20), proposed_criteria (29)"}, "round1": {"path": SOURCE_INDEX["round1"]["path"], "sha256": SOURCE_INDEX["round1"]["sha256"], "fields": "criteria_classification (29 x 143 clauses), mapping_check.rows (20)"}},
    "r2_D1_D4_retained": {"D1": "measured flag + visual deciding record in all three members; construction-scoped rejection only for Working, now labelled proposal (C6)", "D2": "one continuous loop at the consumer's 100 ms with no wrap discontinuity; pacing clauses expert", "D3": "readable visual weight coherent with the baseline; identical stroke/footprint not required", "D4": "Start distinction = shared-consumer inference in every Start clause; now also carried in the authority label (C2)"},
    "owner_vs_expert_authority_retained": "Owner lines (BRIEF 3/5/7/9), the caller update (PLAR 422 / AUTHORING-UPDATE), assignment process requirements, original-module facts, proposed-module/fixture/checker facts, measurements, expert choices, inferences and methods are carried per clause (CLASSES); no expert or design clause is labelled owner; no owner outcome is dropped or weakened (the temporal evidence leg is bounded and routed, not dropped).",
    "distinctions_preserved": round1["assessment"]["distinctions_preserved"],
}

# ---------------------------------------------------------------- re-hash: nothing outside work/continuation changed; no phase-1 file changed
def tree_hashes():
    files = {}
    for base, dirs, names in os.walk(ROOT):
        rel_base = os.path.relpath(base, ROOT).replace(os.sep, "/")
        dirs[:] = [d for d in dirs if d != "__pycache__" and not (rel_base == "work" and d == "continuation")]
        for name in sorted(names):
            rel = os.path.relpath(os.path.join(base, name), ROOT).replace(os.sep, "/")
            files[rel] = hashlib.sha256(Path(base, name).read_bytes()).hexdigest()
    return files


baseline = jload("work/continuation/baseline-hashes.json")["files"]
now = tree_hashes()
assert phase1["preservation"]["baseline"]["sha256"] == sha("work/continuation/baseline-hashes.json")
tree_diff = {"baseline_files": len(baseline), "files_now": len(now), "changed": [k for k in baseline if k in now and baseline[k] != now[k]], "removed": [k for k in baseline if k not in now], "added_outside_work_continuation": [k for k in now if k not in baseline]}
assert not tree_diff["changed"] and not tree_diff["removed"] and not tree_diff["added_outside_work_continuation"]
phase1_files = dict(phase1["outputs"])
phase1_files["work/continuation/PHASE1-CALLER.json"] = EXPECTED["work/continuation/PHASE1-CALLER.json"]
phase1_check = [{"path": p, "expected": h, "unchanged": sha(p) == h} for p, h in sorted(phase1_files.items())]
assert all(x["unchanged"] for x in phase1_check)

doc = {
    "version": 1,
    "kind": "specialist-round2-reconciliation",
    "role": f"PIXL specialist (same native registered pixl child as round 1, agent id {NATIVE_CHILD_ID}, continued by SendMessage; host model Claude Fable 5.1); reconciles the caller's independent review with SPECIALIST-ROUND1.json; no production, renderer, provider, state, PLAR, job, inspection or acceptance action",
    "inputs": {k: {"path": k, "sha256": v, "verified": True} for k, v in EXPECTED.items()},
    "caller_verdict_received": caller["verdict"],
    "conventions": {"lines": "one-based inclusive file-local lines; every locator below was opened at build time by specialist-round2-build.py and verified to contain its wording; JSON-field locators verified by path", "authority_classes": CLASSES, "corrections": "written beside, never over, the original: corrected_criteria[*].original_check is the exact proposal text; corrected_check is the proposed replacement for a successor plan the caller may author later; nothing here is adopted, accepted or committed"},
    "sources": SOURCE_INDEX,
    "caller_locators_recheck": {"count": len(caller_locators_recheck), "all_verified_by_me": True},
    "dispositions": dispositions,
    "disposition_counts": counts,
    "challenges": [],
    "accepted_notes": accepted_notes,
    "answers_received": {"Q1": CR_Q1, "Q1_applied": "universal clauses = owner/caller-update/assignment outcomes; P1-specific clauses (loop-phase identity, cell-0 identity, exact descriptor shapes) scoped to the P1 candidate / this implementation (C1 option b; C3 scoping)", "Q2": CR_Q2, "Q2_applied": "both adopted with separate labels; Retry attribution narrowed to 'owner line applied to the caller-extended status set' (C2)"},
    "corrected_criteria": corrected,
    "corrected_summary": {"check_text_changed": changed_text, "authority_scope_sources_or_route_only": changed_other, "unchanged": unchanged, "counts": {"check_text_changed": len(changed_text), "other_changes": len(changed_other), "unchanged": len(unchanged)}},
    "retained_comparison": retained_comparison,
    "remaining_choices": [
        "Owner/caller: accept frozen-spinner semantics for the stationary Working symbol (P1, no new art) or require a distinct static glyph (P2, one generation; identity swap on preference change; 1x dashed-line risk).",
        "Caller: M1 mapping alternative (renderer rule, statusVisuals unchanged) versus the implemented M2-style descriptor extension with `still`; the corrected criteria bind the outcome under either and scope the descriptor shape to the chosen implementation.",
        "Caller at production time: fixture change for a 1x live cell (or a labelled viewing aid) so the 1x playback leg can be viewed; optional check.py assertions for static states on the change event and for the as-launched forced-reduced phase.",
        "Caller: resolve job authoring-01.working.join-01 through its existing failed-observation route (untouched here).",
    ],
    "limits": [
        "No successor fixture capture exists (work/focused-successor/render-01 has no render.json); check.py has never run; no pixl_inspection views; no playback viewed; wall-clock cadence not measured. No engine/live or visual criterion has evidence and none is given a pass here.",
        "Nothing is accepted or adopted: the original proposal (sha256 792d4b8f...), the 20 Q records, state.px revision 88, PLAR, the prepared job and all phase-1 files are unchanged (see rehash).",
        "Visual statements in round 1 and here are the specialist's and caller's preliminary viewing of composites, not fixture captures.",
    ],
    "rehash": {"outside_work_continuation": tree_diff, "statement_outside": "no file outside work/continuation changed, was removed or was added (1332 files, baseline-hashes.json sha256 3d794d19...)", "phase1_files_under_work_continuation": phase1_check, "statement_phase1": "every phase-1 file listed in PHASE1-CALLER.json.outputs, plus PHASE1-CALLER.json itself, has its recorded sha256"},
    "files_created": ["work/continuation/SPECIALIST-ROUND2.json", "work/continuation/specialist-round2-build.py"],
    "files_modified": [],
    "tools_used": ["Read", "Bash: C:/github/pixel-lab-agent/.venv/Scripts/python.exe -I (json, hashlib, os)"],
    "tools_not_called": ["pixl_commit", "pixl_job_*", "pixl_plar_save", "pixl_plar_prepare", "pixl_production_plan", "pixl_stage_prepare", "pixl_inspection_prepare", "pixl_inspection_review", "pixl_task_complete", "pixl_plar_handoff", "pixl_family_snapshot", "pixl_request_review", "pixl_context", "pixl_validate (round-1 result reused; record hashes re-checked by value)", "pixl_asset_check (round-1 results reused)", "any PixelLab tool", "renderer-successor capture"],
    "status": "delivered against round 2 (reconciliation and corrected wording); production, rendering and acceptance remain separate and open",
    "build_verification": {"verified_citations": VERIFIED},
}
OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"path": "work/continuation/SPECIALIST-ROUND2.json", "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(), "bytes": OUT.stat().st_size, "dispositions": counts, "changed_text": len(changed_text), "other_changes": len(changed_other), "unchanged": len(unchanged), "citations_verified": len(VERIFIED), "caller_locators_rechecked": len(caller_locators_recheck)}))
