"""Build criterion-mapping.json from the caller's exact exports (02/03/04/07/08).

Literal check text, IDs and record hashes are copied programmatically from the
saved reports; only the per-pair judgments below are authored by the specialist.
Run with: python -I build_criterion_mapping.py  (cwd = project root)
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXPORTS = ROOT / "work" / "choice-comparison"
OUT = Path(__file__).resolve().parent / "criterion-mapping.json"


def load(name: str):
    path = EXPORTS / name
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest()


changes, h02 = load("02-request-review-changes.json")
before, h03 = load("03-request-review-full-before-authoring-01.json")
after, h04 = load("04-request-review-full-after-provenance-correction.json")
diff07, h07 = load("07-criterion-literal-diff.json")
working_ctx, h08 = load("08-review-context-working-candidate.json")
family_ctx, h09 = load("09-review-context-family-candidate.json")

before_by_id = {c["id"]: c for c in before["criteria"]}
after_by_id = {c["id"]: c for c in after["criteria"]}
index_before = {c["id"]: c["record_sha256"] for c in changes["criterion_index"]["before"]}
index_after = {c["id"]: c["record_sha256"] for c in changes["criterion_index"]["after"]}
assert set(index_before) == set(before_by_id) and len(index_before) == 20
assert set(index_after) == set(after_by_id) and len(index_after) == 23
for cid, h in index_before.items():
    assert before_by_id[cid]["record_sha256"] == h
for cid, h in index_after.items():
    assert after_by_id[cid]["record_sha256"] == h


def local_key(cid: str) -> str:
    # authoring-01.working.q.geometry -> working/geometry
    _, stage, _, local = cid.split(".", 3)
    return f"{stage}/{local}"


# ---------------------------------------------------------------------------
# Specialist judgments. Keys are stage/local of the OLD criterion.
# "obligation": unchanged | clarified | narrowed | widened | re-scoped
#   (several may apply; the list is ordered by weight).
# ---------------------------------------------------------------------------
SRC = {
    "brief3": "BRIEF.md line 3 (owner): 16x16 cells; Working four horizontal frames at 100 ms; Ready and Retry static; transparent backgrounds; readable silhouettes; cool blue accent; fixed palette not required; inspect 1x/3x on dark panel; working loop communicates activity without looking like success; error/retry distinguishable without color alone.",
    "brief5": "BRIEF.md line 5 (owner): assets belong at the paths already used by the view; propose a representative sample before expanding the family.",
    "brief7": "BRIEF.md line 7 (owner update): paused state distinguishable from activity, completion and retry without relying on color alone; keep existing style/display requirements; failure visual moved to the path in the updated view, purpose unchanged.",
    "brief9": "BRIEF.md line 9 (owner update): Ready uses an asymmetrical-arm check mark; destination now follows the updated view; keep 16x16, static, transparent, review display conditions.",
    "view4": "src/queue-view-successor.ts line 4: running -> label Working, path renderer-successor/assets/working.png, frames 4.",
    "view5-7": "src/queue-view-successor.ts lines 5-7: paused/succeeded/failed -> paused.png, ready-confirmed.png, error-retry.png, frames 1.",
    "view3": "src/queue-view-successor.ts line 3: idle -> label Start, renderer-successor/assets/start.svg (preserved vector control).",
    "view9": "src/queue-view-successor.ts line 9: display cell [16,16], scale 3, filter nearest, frameMs 100, background #172336.",
    "view10-11": "src/queue-view-successor.ts lines 10-11: statusCell and compactStatus return the same statusVisuals descriptor (shared consumer).",
    "view16-22": "src/queue-view-successor.ts lines 16-22: reduced motion changes only the selected cell; motionQuery '(prefers-reduced-motion: reduce)'; statusFrame returns 0 for running when reduced, else floor(elapsed/frameMs) mod frames.",
    "renderer33-44": "renderer-successor/view.mjs lines 33-44 (paint): frame = statusFrame(state, elapsed, motion.matches); draws only when asset.width == 16*frames and height == 16; slices frame*16,0,16,16; nearest when filter is nearest; fills #172336.",
    "renderer94-115": "renderer-successor/view.mjs lines 94-115: animate() calls applyMotionPreference('animation-frame') every rAF (comment: some hosts update .matches without dispatching change); applyMotionPreference reconciles once per changed matches, resets origin, repaints matrix and live cells; line 115 media change event route.",
    "renderer134-143": "renderer-successor/view.mjs lines 134-143: capture timeline samples elapsed at frame boundaries 0,99,100,...,399 and 400 for statusCell.",
    "queue3": "src/queue.ts line 3: started->running, ok->succeeded, error->failed, pause->paused.",
    "adopt29-35": "SUCCESSOR-ADOPTION.md step 3 (lines 29-35): scope normal 100 ms animation separately from stationary reduced-motion display; keep the three split alpha diagnostics/visual decisions, full alpha/selective AA, in-cell margins, scoped expert pacing, qualitative coherence and inferred Start distinction; retain an exact mapping from all 20 original criteria.",
    "adopt44-54": "SUCCESSOR-ADOPTION.md step 5 (lines 44-54): reuse exact existing PixelLab-produced assets; retain provenance to original bytes; fresh mechanical/visual/engine verdicts scoped to the new criteria; run the versioned renderer for normal/reduced modes, both consumers, all states and live preference switching; verify timing claims at measured scope.",
    "plar-working": "Selected PLAR queue.working purpose (04 selections[].current_requirements.purpose, hash 1ab9df77...): reduced-motion mode must use a stationary Working symbol distinguishable from Ready and Paused; reuse one asset for statusCell and compactStatus.",
    "contract-working": "provenance.working.contract li (01 contracts): four frames at 100 ms under normal motion only; review loop boundary, anchor and volume stability; no fixed palette, binary-alpha, exact stroke or margin rule; reduced motion displays stationary source frame zero with Working label.",
    "style-choice": "render.choice.style (01 choices, confirmed): carry readable compact silhouettes, deliberate coherent clusters and stepped edges, perceptible cool-blue accent, transparent exterior at 1x/3x on panel; not fixed: exact hex, palette count, binary alpha, stroke width, margins, check motif for other states.",
    "D1": "Prior caller comparison (work/focused-successor/caller-comparison-final.json prior_corrections_verified.D1): alpha measurements remain diagnostic; deciding check visual.",
    "D2": "Prior caller comparison D2: 100 ms owner cadence separated from expert even pacing/no near-hold.",
    "D3": "Prior caller comparison D3: coherence imposes no identical/comparable footprint or weight.",
    "D4": "Prior caller comparison D4: Start distinction attributed to shared-consumer inference.",
    "profile-transparency": "PIXL PROFILE.md 'Transparency and subject construction': separate transparent negative space from opaque subject components; a deliberate plate/backing with transparent exterior differs from an unintended canvas matte; a transparency requirement alone does not prohibit every opaque backing shape.",
    "rr-route": "request-review.md 'Check the review route': a local mechanical check cannot decide which shape is intentional foreground or whether a matte is unwanted; split measurement from visual judgment or set mode visual.",
    "rr-process": "request-review.md: keep process requirements, output requirements and diagnostic proxies distinct; a diagnostic is not a rejection rule.",
    "r4-art": "work/focused-successor/specialist-proposal-r4.json art_choice: hold existing Working frame zero for reduced motion; specialist proposal within the owner requirement; alternatives and risk recorded.",
    "r4-reduced": "work/focused-successor/specialist-proposal-r4.json request.reduced: media change event and animation-frame reconciliation share one handler; apply once per actual changed preference; Render-03 observed the animation-frame route; no event-firing claim.",
    "r4-revision": "work/focused-successor/specialist-proposal-r4.json revision_changes: r3 'immediately paint frame zero' relaxed in r4 to 'when the media change event is delivered or when the next animation frame observes changed matchMedia.matches; reconcile only once'.",
    "expert": "Specialist pixel-art judgment (this review, from stills and measurements; labelled as such).",
}

J = {
    "working/geometry": {
        "literal_changes": {
            "check": "Added: '(transparent margin inside a cell is composition, not padding)'; an explicit 'Basis:' sentence naming src/queue-view-successor.ts frames 4 / cell [16,16] / frameMs 100 and the renderer's width==16*frames guard, slice and floor(elapsed/100) mod 4; the advance is qualified 'under no-preference only'; added 'Under reduced motion it selects frame zero without changing the four-cell sheet geometry.' Dropped: 'padding or extra canvas' replaced by 'added canvas between or around the cells'.",
            "domain_mode": "unchanged (mechanical/local)",
            "sources": "render.source.view (old src/queue-view.ts) dropped; render.source.caller, provenance.source.view/renderer/assignment/proposal/comparison/backend added (uniform 8-source list).",
        },
        "obligation": ["unchanged", "clarified"],
        "reasoning": "Owner geometry (brief3) and consumer slicing (view4, view9, renderer33-44) are unchanged. The old 'no gutters, padding or extra canvas' could be read to reject transparent in-cell margins (an invented margin rule); the new text states margins are composition. The reduced-motion sentence describes consumer behaviour (view16-22) and adds no image obligation. The rejection surface is therefore no wider, and one ambiguous reading is removed.",
        "authority": ["brief3", "view4", "view9", "view16-22", "renderer33-44", "adopt29-35"],
    },
    "working/transparent-exterior": {
        "literal_changes": {
            "check": "Old single mechanical rule 'all pixels outside the activity marks have alpha 0; no opaque matte, plate, grey tile or fringe' (with the 193 #808080 failure-class example) replaced by a visual deciding rule: 'every frame's intended exterior shows the panel with no unintended opaque canvas matte, tile, halo or fringe. A deliberate backing shape is permitted if part of the recorded subject design with transparent exterior... This visual record decides transparency appearance; measured alpha/component flags do not reject artwork.' The alpha histogram/component measurement moved to a new separate .diagnostic criterion whose flags are 'for visual review only'. Named failure-class example dropped from the text (the failed verdict live.working-animation-01.review.verdict.1 remains in state).",
            "domain_mode": "mechanical/local -> visual/visual (deciding rule); new sibling .diagnostic is mechanical/local",
            "sources": "same uniform 8-source replacement as above",
        },
        "obligation": ["re-scoped", "narrowed"],
        "reasoning": "The owner obligation (brief3 'transparent backgrounds') is unchanged. The route is re-scoped: deciding which pixels are 'outside the marks' is a visual judgment that a local mechanical rule cannot make (rr-route, D1). The literal rejection is narrowed in one respect: the old text rejected any 'plate'; the new text permits a deliberate backing shape with transparent exterior (profile-transparency). No new restriction is added; the diagnostic flags are explicitly not thresholds (rr-process).",
        "authority": ["brief3", "profile-transparency", "rr-route", "rr-process", "D1", "adopt29-35"],
        "split_to_diagnostic": True,
    },
    "working/frame-assembly": {
        "literal_changes": {
            "check": "Old conditional provider-assembly policy (lossless cell copies, play-order record, raw frames retained) replaced by a reuse-only provenance rule: record exact retained source cf101610... and verify the destination PNG is byte-identical; no new assembly/join/patch/resize/resample/recolor/duplication/drop; preserve earlier raw outputs and assembly records; the obsolete prepared join and proposed seed-rotation checks are declared non-applicable to this reuse path.",
            "domain_mode": "unchanged (mechanical/local)",
            "sources": "render.source.view and render.source.assignment (RENDER-STAGE.md) dropped; uniform 8-source list added",
        },
        "obligation": ["re-scoped"],
        "reasoning": "This is a different obligation, not a paraphrase: a process/provenance requirement for the reuse path authorised by adopt44-54 ('reuse the exact existing PixelLab-produced assets... retain provenance to the original bytes'). The old conditional obligation is not violated; it is inapplicable because no new provider result was assembled. The historical criterion remains the record of the earlier construction policy.",
        "authority": ["adopt44-54", "rr-process"],
    },
    "working/activity-not-success": {
        "literal_changes": {
            "check": "Owner clause kept ('read as ongoing activity and not as completion: no frame forms a check mark or another success-like terminal pose'). The old unattributed rejections 'an arrowhead, pause bars' are demoted to 'Expert guidance, scoped to this branch: avoid frames that read as the static symbol of another member' and the binding distinction is delegated to provenance-correction.delivery.q.distinction. Added: 'For reduced motion, frame zero shown alone with its Working label must read as the stationary Working indicator, distinct from Ready and Paused; the frame choice is this specialist's proposal, not an owner-prescribed motif.' Relative to the r4 proposal text, only the cross-reference ID changed (authoring-01.delivery.q.distinction -> provenance-correction.delivery.q.distinction).",
            "domain_mode": "unchanged (visual/visual)",
            "sources": "render.source.assessment dropped; uniform 8-source list added",
        },
        "obligation": ["narrowed", "widened", "re-scoped"],
        "reasoning": "Narrowed: 'arrowhead' and 'pause bars' are no longer rejection conditions of this criterion; brief3 only requires activity-not-success, so that removal restores owner scope (D4 for the Start inference). Widened: a reduced-motion stationary obligation is added from the caller's PLAR update (plar-working) and adopt29-35; the frame-zero choice is correctly labelled a specialist proposal (r4-art). Net: re-scoped with explicit attribution.",
        "authority": ["brief3", "plar-working", "r4-art", "D4", "adopt29-35"],
    },
    "working/motion-continuity": {
        "literal_changes": {
            "check": "Old: one sentence of rejection conditions 'stable center and anchor, stable cluster count and volume in every phase, deliberate stepped phases with no morphing, near-hold or wrap jump (the rejected AI-animation failure class)'. New: 'Normal motion only'; required outcome = 'one continuous activity loop without a visible discontinuity at the wrap'; 'Stable center/anchor and visual volume are scoped expert quality checks from the Working contract'; 'Evenly paced angular motion/no near-hold is the specialist's chosen quality criterion for this exact reused rotating-segment design, not an owner requirement; a different expressive timing design could satisfy the brief after review'; 'No universal fixed cluster-count/no-morph recipe is imposed'; 'Reduced motion is evaluated separately as stationary frame zero.' Added 1x/3x on #172336.",
            "domain_mode": "unchanged (visual/visual)",
            "sources": "render.source.view, render.source.assessment dropped; uniform 8-source list added",
        },
        "obligation": ["narrowed", "re-scoped"],
        "reasoning": "The owner fixes the cadence (brief3: four frames, 100 ms) and the communicative outcome (loop communicates activity); it does not prescribe cluster count, no-morph or even pacing. The new text keeps the required outcome, carries centre/volume stability as contract-scoped quality (contract-working), and labels even pacing as a design-specific specialist criterion (D2). The rejection surface attributed to the owner is narrower; the expert clauses remain but are scoped so an expressive alternative is reviewable rather than auto-rejected. Expert note: at 4 x 100 ms a held pair does read as a stutter for a rotating design, so the specialist's criterion is sound for this design.",
        "authority": ["brief3", "contract-working", "D2", "adopt29-35", "expert"],
    },
    "working/style-coherence": {
        "literal_changes": {
            "check": "Added 'consistent with the exact Ready baseline (selective, intentional anti-aliasing is permitted under the full-alpha contract; accidental resampling blur or stray noise is not)'. Everything else identical, including the closing 'no exact hex, palette count, binary alpha, stroke width or margin rule'.",
            "domain_mode": "unchanged (visual/visual)",
            "sources": "render.source.assessment dropped; uniform 8-source list added",
        },
        "obligation": ["unchanged", "clarified"],
        "reasoning": "brief3 requires readable silhouettes and the cool-blue accent with no fixed palette; render.choice.style (confirmed caller adoption) carries deliberate clusters and stepped edges. The parenthetical makes explicit that intentional AA is allowed (full-alpha contract) and that accidental blur/noise is not deliberate craft. That is the adopted style's existing meaning, not a new numeric rule; weight/stroke/margins stay unfixed (D3).",
        "authority": ["brief3", "style-choice", "D3", "adopt29-35"],
    },
    "working/consumers": {
        "literal_changes": {
            "check": "Old abstract 'in the actual consumer renderer... assets/working.png... observed live 100 ms frame advance including the wrap'. New: names the fixture (renderer-successor/view.mjs executing src/queue.ts and src/queue-view-successor.ts) and successor path; requires both consumers to resolve the same descriptor; smoothing false / pixelated; geometryMatches true; frame-index timeline 0,0,1,1,2,2,3,3,0 at 0..400 ms; 'wall-clock frame duration is not measured by this fixture and is not claimed'; reduced motion: stationary frame zero via statusFrame, same pixel hash over >= 800 ms in both consumers; live switch to reduce paints frame zero 'when the media change event is delivered or when the next animation frame observes changed matchMedia.matches; reconcile only once per observed preference transition'; switch back restarts cycling at frame zero without backend change, reload, stale canvas or duplicate animation.",
            "domain_mode": "unchanged (engine/live)",
            "sources": "render.source.view, r.22e90a2a03fe453a.source.4 (retained copy of queue.ts), recheck.source.findings dropped; uniform 8-source list added",
        },
        "obligation": ["widened", "re-scoped", "narrowed"],
        "reasoning": "Widened: reduced-motion and live preference-switch obligations are new (plar-working; adopt44-54; view16-22; renderer94-115). Re-scoped: destination moved to the successor paths (brief9 'destination now follows the updated view'). Narrowed in claim: 'observed live 100 ms frame advance' becomes sampled frame indices with wall-clock explicitly unmeasured, which is the honest scope of the fixture (renderer134-143). The r4 relaxation of 'immediately' to event-or-next-rAF reconciliation (r4-revision) matches view.mjs lines 95-97 and avoids inferring a browser event guarantee.",
        "authority": ["queue3", "view10-11", "view16-22", "renderer94-115", "renderer134-143", "plar-working", "brief9", "adopt44-54", "r4-reduced", "r4-revision"],
    },
    "retry/geometry": {
        "literal_changes": {"check": "identical text", "domain_mode": "unchanged (mechanical/local)", "sources": "render.source.view dropped; uniform 8-source list added"},
        "obligation": ["unchanged"],
        "reasoning": "Static 16x16 (brief3, brief7 'purpose unchanged', brief9 'static behavior'; view5-7 frames 1). Only source bindings changed.",
        "authority": ["brief3", "brief7", "view5-7"],
    },
    "retry/transparent-exterior": {
        "literal_changes": {
            "check": "Old mechanical 'All pixels outside the mark have alpha 0; no opaque matte, plate or fringe' replaced by the same visual deciding rule used for Working (deliberate backing permitted; flags do not reject); measurement split into retry.q.transparent-exterior.diagnostic.",
            "domain_mode": "mechanical/local -> visual/visual; sibling .diagnostic mechanical/local",
            "sources": "uniform 8-source list",
        },
        "obligation": ["re-scoped", "narrowed"],
        "reasoning": "Same analysis as working/transparent-exterior: owner transparency outcome unchanged (brief3), route corrected (rr-route, D1), 'plate' prohibition narrowed to unintended mattes (profile-transparency). Note the diagnostic says 'per-cell' for a single-cell image; harmless.",
        "authority": ["brief3", "profile-transparency", "rr-route", "D1"],
        "split_to_diagnostic": True,
    },
    "retry/retry-meaning-without-color": {
        "literal_changes": {
            "check": "'in color and in grayscale' -> 'in colour and in a non-colour comparison (grayscale or binarized silhouettes)'; 'reads as failed work / retry' -> 'reads as failed work with a retry action'; 'it must not be confusable' -> 'in particular it must not be confusable'; added 'No specific retry motif (such as an arrow) is required.'",
            "domain_mode": "unchanged (visual/visual)",
            "sources": "render.source.assessment dropped; uniform 8-source list",
        },
        "obligation": ["unchanged", "clarified"],
        "reasoning": "brief3 requires non-color distinguishability; brief7 keeps the purpose. The comparison method is widened to any non-colour view (method, not obligation). The explicit non-recipe sentence prevents the arrow construction from becoming an owner rule. The Start comparison remains a shared-consumer inference (view3, view10-11; D4).",
        "authority": ["brief3", "brief7", "view3", "view10-11", "D4"],
    },
    "retry/style-coherence": {
        "literal_changes": {"check": "same AA/baseline parenthetical as working/style-coherence", "domain_mode": "unchanged", "sources": "uniform 8-source list"},
        "obligation": ["unchanged", "clarified"],
        "reasoning": "As working/style-coherence. Measured: error-retry.png has 54 opaque pixels in 31 colours (heavily shaded for 16 px); the explicit AA permission is what keeps this member within the adopted style's wording; coherence remains a qualitative judgment, not a palette count.",
        "authority": ["brief3", "style-choice", "D3", "expert"],
    },
    "retry/consumers": {
        "literal_changes": {
            "check": "Fixture and successor path named; descriptor {Retry, renderer-successor/assets/error-retry.png (not the superseded assets/retry.png), frames 1}; smoothing false / pixelated; geometryMatches true; 'no animation loop runs for the descriptor (frames 1)' replaces 'static behavior'.",
            "domain_mode": "unchanged (engine/live)",
            "sources": "render.source.view, r.22e90a2a03fe453a.source.4, recheck.source.findings dropped; uniform 8-source list",
        },
        "obligation": ["re-scoped"],
        "reasoning": "Consumer mapping obligation unchanged (queue3 error->failed; view5-7 line 7). Destination re-scoped to the successor (brief9; adopt step 2). 'No animation loop runs' is the concrete form of 'static behavior' given renderer line 98 (frames > 1 guard).",
        "authority": ["queue3", "view5-7", "view10-11", "brief9", "adopt44-54"],
    },
    "paused/geometry": {
        "literal_changes": {"check": "identical text", "domain_mode": "unchanged", "sources": "uniform 8-source list"},
        "obligation": ["unchanged"],
        "reasoning": "Static 16x16 (brief7, view5-7 line 5).",
        "authority": ["brief7", "view5-7"],
    },
    "paused/transparent-exterior": {
        "literal_changes": {
            "check": "Old mechanical rule with '(the rejected opaque magenta intermediate is this failure class)' replaced by the shared visual deciding rule; measurement split to paused.q.transparent-exterior.diagnostic; the named failure-class example is dropped from the text (live.paused-02.review.verdict.1 fail remains in state).",
            "domain_mode": "mechanical/local -> visual/visual; sibling .diagnostic",
            "sources": "uniform 8-source list",
        },
        "obligation": ["re-scoped", "narrowed"],
        "reasoning": "As working/transparent-exterior. Additional point from the prior comparison: alpha-zero stored RGB (magenta) does not make Paused opaque; the new text states 'RGB values where alpha is zero are insignificant', which the old literal did not say. Measured now: paused.png alpha histogram {0:196, 255:60}, two components, no full-span component.",
        "authority": ["brief3", "brief7", "profile-transparency", "rr-route", "D1"],
        "split_to_diagnostic": True,
    },
    "paused/pause-meaning-without-color": {
        "literal_changes": {
            "check": "'in color and in grayscale' -> 'in colour and in a non-colour comparison (grayscale or binarized silhouettes)'; added 'No specific pause motif (such as paired bars) is required.'",
            "domain_mode": "unchanged (visual/visual)",
            "sources": "uniform 8-source list",
        },
        "obligation": ["unchanged", "clarified"],
        "reasoning": "brief7 is the owner authority (distinguishable from activity, completion and retry without color). The Start comparison is shared-consumer inference (view3, view10-11; D4). The non-recipe sentence keeps paired bars a sample choice.",
        "authority": ["brief7", "view3", "view10-11", "D4"],
    },
    "paused/style-coherence": {
        "literal_changes": {"check": "same AA/baseline parenthetical", "domain_mode": "unchanged", "sources": "uniform 8-source list"},
        "obligation": ["unchanged", "clarified"],
        "reasoning": "As working/style-coherence; paused bars are heavier (60 px) than the Ready check (29 px) and that is permitted (D3).",
        "authority": ["brief3", "brief7", "style-choice", "D3"],
    },
    "paused/consumers": {
        "literal_changes": {"check": "Fixture and successor path named; descriptor {Paused, renderer-successor/assets/paused.png, frames 1}; smoothing/pixelated; geometryMatches; 'no animation loop runs for the descriptor (frames 1)'.", "domain_mode": "unchanged (engine/live)", "sources": "uniform 8-source list"},
        "obligation": ["re-scoped"],
        "reasoning": "As retry/consumers (queue3 pause->paused; view5-7 line 5; brief9 destination).",
        "authority": ["queue3", "view5-7", "view10-11", "brief9", "adopt44-54"],
    },
    "delivery/continuity": {
        "literal_changes": {
            "check": "'readable visual weight' -> 'readable visual weight coherent with the Ready baseline (identical stroke width or footprint is not required)'; 'its actual 100 ms playback with the wrap' -> 'its actual 100 ms playback with the wrap under no-preference, and its stationary frame-zero presentation under reduce'.",
            "domain_mode": "unchanged (continuity/visual)",
            "sources": "render.source.assessment dropped; uniform 8-source list",
        },
        "obligation": ["clarified", "widened"],
        "reasoning": "brief3 asks for coherent assets; render.choice.style leaves stroke width and margins unfixed. The parenthetical (D3) blocks an 'identical weight' reading. The reduced-mode presentation is a new collective obligation from plar-working and adopt29-35 (scope normal animation separately from stationary display).",
        "authority": ["brief3", "style-choice", "D3", "plar-working", "adopt29-35"],
    },
    "delivery/distinction": {
        "literal_changes": {
            "check": "Added: 'Include stationary Working frame zero shown alone in the non-color comparison: required reduced-motion distinction is from Ready and Paused. Distinction from Retry and preserved Start is the shared-consumer inference from the same status set, not a literal owner motif requirement.' First sentence identical.",
            "domain_mode": "unchanged (continuity/visual)",
            "sources": "uniform 8-source list",
        },
        "obligation": ["widened", "clarified"],
        "reasoning": "Widened by the reduced-motion clause (plar-working). The attribution sentence is a clarification: brief3 'Preserve the existing vector Start control' is a preservation requirement, not a distinction requirement; distinction from Start follows from the shared statusVisuals set (view3, view10-11; D4). brief3/brief7 remain the owner authority for Working-vs-success and Retry/Paused non-color distinction.",
        "authority": ["brief3", "brief7", "plar-working", "view3", "view10-11", "D4"],
    },
    "delivery/destination": {
        "literal_changes": {
            "check": "Old 'confirmed destination paths... 100 ms timing... assets/start.svg byte hash unchanged'. New: fixture named; 'caller-reviewed proposed successor destination paths'; 'under no-preference only, frame index floor(elapsed/100) mod frames at the timeline sample points including the 400 ms wrap (wall-clock duration not measured)'; scale 1 (matrix) and 3 (matrix and live); 'recorded integer canvas placement matching the screenshot pixels' as the adopted destination-check method; renderer-successor/assets/start.svg unchanged; successor destination enumerated; 'old src/queue-view.ts, renderer/ and assets/ remain byte-unchanged'; both reduced settings and switching each direction with both consumers updating together without backend change; reduced draws source rect [0,0,16,16]; preference changes via media change event or next-rAF matches with the observed route recorded; 'No requirement that this browser dispatch a change event is inferred'; origin reset once per transition and repaint of live and matrix Working cells.",
            "domain_mode": "unchanged (engine/live)",
            "sources": "render.source.view, r.22e90a2a03fe453a.source.4, recheck.source.findings, render.source.assignment dropped; uniform 8-source list",
        },
        "obligation": ["re-scoped", "widened", "narrowed"],
        "reasoning": "Re-scoped to the successor destination (brief9; adopt steps 2 and 5) while adding an explicit preservation obligation for the old files. Widened by reduced-motion and live-switch checks across both consumers (view16-22, renderer94-115, adopt44-54). Narrowed in claim: '100 ms timing' becomes sampled frame indices with wall-clock unmeasured (renderer134-143), which is what the fixture can establish. The event-or-rAF wording follows view.mjs lines 95-97 and r4-reduced.",
        "authority": ["brief9", "view16-22", "renderer94-115", "renderer134-143", "adopt44-54", "r4-reduced", "r4-revision"],
    },
}

DIAG_KEYS = {
    "working/transparent-exterior.diagnostic": "working/transparent-exterior",
    "retry/transparent-exterior.diagnostic": "retry/transparent-exterior",
    "paused/transparent-exterior.diagnostic": "paused/transparent-exterior",
}

pairs = []
covered_after = set()
for old_id in index_before:  # keep export order
    key = local_key(old_id)
    old = before_by_id[old_id]
    new_ids = [i for i in index_after if local_key(i) == key]
    diag_ids = [i for i in index_after if local_key(i) == key + ".diagnostic"]
    j = J[key]
    entry = {
        "key": key,
        "old": {"id": old_id, "record_sha256": old["record_sha256"], "domain": old["domain"], "mode": old["mode"], "sources": old["sources"], "check": old["check"]},
        "new": [],
        "split_diagnostics": [],
        "check_text_identical": None,
        "literal_changes": j["literal_changes"],
        "obligation_judgment": j["obligation"],
        "reasoning": j["reasoning"],
        "authority": [{"key": a, "text": SRC[a]} for a in j["authority"]],
    }
    for nid in new_ids:
        n = after_by_id[nid]
        covered_after.add(nid)
        entry["new"].append({"id": nid, "record_sha256": n["record_sha256"], "domain": n["domain"], "mode": n["mode"], "sources": n["sources"], "check": n["check"]})
        entry["check_text_identical"] = n["check"] == old["check"]
    for did in diag_ids:
        n = after_by_id[did]
        covered_after.add(did)
        entry["split_diagnostics"].append({"id": did, "record_sha256": n["record_sha256"], "domain": n["domain"], "mode": n["mode"], "sources": n["sources"], "check": n["check"], "relation": "split from the old mixed mechanical rule: measurement retained as a diagnostic proxy; not a rejection rule"})
    pairs.append(entry)

assert covered_after == set(index_after), set(index_after) - covered_after
assert len(pairs) == 20 and sum(len(p["new"]) for p in pairs) == 20 and sum(len(p["split_diagnostics"]) for p in pairs) == 3

# Cross-check the caller's 07 pairing structurally.
seven = {c["key"]: c for c in diff07["criteria"]}
identical_07 = sorted(k for k, c in seven.items() if c.get("check_text_identical") is True)
identical_mine = sorted(p["key"] for p in pairs if p["check_text_identical"])
assert identical_07 == identical_mine == ["paused/geometry", "retry/geometry"], (identical_07, identical_mine)

# Historical verdict preservation (from 02 review_attention and 08 current verdicts).
hist = changes["review_attention"]["after"]["failures_obsolete_or_stale"]
assert any(h["id"] == "provenance.working.motion.unavailable" and h["status"] == "unavailable" and h["obsolete"] is True for h in hist)
working_verdicts = {c["id"]: {"status": c["status"], "verdict": c["verdict"]} for c in working_ctx["criteria"]}
family_verdicts = {c["id"]: {"status": c["status"], "verdict": c["verdict"]} for c in family_ctx["criteria"]}

summary = {
    "pairs": 20,
    "new_criteria": 23,
    "added_diagnostics": 3,
    "check_text_identical_pairs": identical_mine,
    "domain_mode_changed_pairs": [p["key"] for p in pairs if p["new"] and (p["new"][0]["domain"], p["new"][0]["mode"]) != (p["old"]["domain"], p["old"]["mode"])],
    "obligation_counts": {},
    "note": "Alignment by stage/local ID was the caller's structural pairing (07); every judgment above was made by reading the full literal checks in 03/04 and the named sources. Identical IDs did not imply equivalence: 18 of 20 pairs changed check text and all 20 changed source bindings.",
}
for p in pairs:
    for o in p["obligation_judgment"]:
        summary["obligation_counts"][o] = summary["obligation_counts"].get(o, 0) + 1

doc = {
    "version": 1,
    "kind": "criterion-mapping",
    "reviewer": {
        "role": "delegated native PIXL specialist (pixl:pixl skill loaded)",
        "invocation": "Claude Code Agent tool, subagent_type 'pixl' (agents.json role 'PIXL visual asset specialist for source-authority comparison'); model inherited from parent: claude-fable-5-1",
        "scope": "read-only semantic comparison; no PIXL state mutation",
    },
    "plans": {"before": before["plan"], "after": after["plan"]},
    "review_scope_sha256": {"before": before["review_scope_sha256"], "after": after["review_scope_sha256"]},
    "state": changes["state"],
    "inputs": {
        "02-request-review-changes.json": h02,
        "03-request-review-full-before-authoring-01.json": h03,
        "04-request-review-full-after-provenance-correction.json": h04,
        "07-criterion-literal-diff.json": h07,
        "08-review-context-working-candidate.json": h08,
        "09-review-context-family-candidate.json": h09,
    },
    "criterion_index": {"before": changes["criterion_index"]["before"], "after": changes["criterion_index"]["after"]},
    "obligation_vocabulary": {
        "unchanged": "same required outcome and same literal rejection surface",
        "clarified": "same required outcome; wording removes an ambiguous or unattributed reading without adding a restriction",
        "narrowed": "the literal rejection surface attributed to owner authority got smaller (a clause demoted, scoped or removed)",
        "widened": "a new obligation is added (here: reduced-motion / live preference-switch behaviour or old-file preservation)",
        "re-scoped": "the obligation now binds a different path, destination, route or process than before",
    },
    "pairs": pairs,
    "r4_proposal_identity": {
        "note": "All 23 current literal checks are byte-identical to the successor_checks in work/focused-successor/specialist-proposal-r4.json (sha256 18e7e32c...), except provenance-correction.working.q.activity-not-success, whose only difference is the cross-reference ID 'authoring-01.delivery.q.distinction' -> 'provenance-correction.delivery.q.distinction'. The current criteria therefore carry the r4 proposal and the independent caller comparison (caller-comparison-final.json, status 'consistent', review_scope b4c1a4f5...) as their drafting history; that history is evidence of agreement, not owner authority.",
    },
    "historical_verdict_preservation": {
        "preserved_unavailable": {
            "id": "provenance.working.motion.unavailable",
            "criterion": "provenance-correction.working.q.motion-continuity",
            "candidate": "provenance-correction.working.candidate",
            "status": "unavailable",
            "obsolete": True,
            "recorded_at": "2026-11-09T11:29:46.095459+00:00",
            "reason_excerpt": "still-only image host cannot judge perceived pacing, near-hold or visible wrap continuity in real time at1x/3x ... View exact retained Working playback directly, then add a superseding scoped visual review.",
            "where_listed": "02 review_attention.after.failures_obsolete_or_stale; 07 review_attention_after_failures; state.px record @provenance.working.motion.unavailable:V (ob=+)",
        },
        "current_superseding_pass": {
            "id": "native-review.working.motion.verdict.0",
            "recorded_at": "2026-11-09T16:16:09+00:00",
            "status": "pass",
            "evidence": "native-review.working.motion.evidence.0",
            "basis_excerpt": "Viewed the recorded 100 ms playback as a sequence at native 1x and nearest 3x on #172336 across four complete cycles, including every fourth-to-first wrap (transitions 04, 08, 12, 16)... equal 90-degree steps at measured 99.9-100.1 ms intervals, no near-hold.",
            "correction_to_caller_brief": "The caller's delegation described the superseding pass as 'provenance.working.review.verdict.*'. Per 08, provenance.working.review.verdict.0-5 cover geometry, transparent-exterior.diagnostic, transparent-exterior, frame-assembly, activity-not-success and style-coherence; provenance.working.engine.verdict covers consumers; the motion-continuity pass is native-review.working.motion.verdict.0.",
        },
        "current_working_verdicts_per_08": working_verdicts,
        "current_family_verdicts_per_09": family_verdicts,
        "other_retained_failures_named_by_old_text": [
            {"id": "live.working-animation-01.review.verdict.1", "status": "fail", "note": "193 opaque #808080 background pixels (grey tile) - the failure class named in the old working transparent-exterior text; still in state"},
            {"id": "live.paused-02.review.verdict.1", "status": "fail", "note": "opaque magenta intermediate - the failure class named in the old paused transparent-exterior text; still in state"},
            {"id": "live.working-animation-repair-01.review.verdict.1", "status": "fail", "note": "morph/near-hold across phases 2/3 and wrap jump - the failure class named in the old motion-continuity text; still in state"},
        ],
        "rule": "Additional diagnostics (the three .diagnostic criteria) and later passing reviews supersede by date and scope; they do not erase the unavailable or failed observations, which remain retrievable beside the current passes.",
    },
    "summary": summary,
}

OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(OUT, hashlib.sha256(OUT.read_bytes()).hexdigest())
print(json.dumps(summary, indent=1))
