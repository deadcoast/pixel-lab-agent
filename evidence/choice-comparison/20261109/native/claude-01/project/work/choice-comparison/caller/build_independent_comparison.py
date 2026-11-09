"""Caller's independent comparison of the exact exported criteria.

Reads only saved exports under work/choice-comparison and the original project
sources; writes work/choice-comparison/caller/independent-comparison.json.
The interpretation text below is the caller's own reading, written before the
specialist's result was opened. No state change, no provider action.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORK = ROOT / "work" / "choice-comparison"
OUT = WORK / "caller" / "independent-comparison.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def lines(rel: str, first: int, last: int) -> str:
    text = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    return "\n".join(text[first - 1 : last])


# Authority index: one entry per cited source location, referenced by key below.
AUTHORITY = {
    "brief.l3": {"path": "BRIEF.md", "lines": [3, 3], "kind": "owner requirement",
                  "text": lines("BRIEF.md", 3, 3)},
    "brief.l5": {"path": "BRIEF.md", "lines": [5, 5], "kind": "owner requirement",
                  "text": lines("BRIEF.md", 5, 5)},
    "brief.l7": {"path": "BRIEF.md", "lines": [7, 7], "kind": "owner requirement (Paused update)",
                  "text": lines("BRIEF.md", 7, 7)},
    "brief.l9": {"path": "BRIEF.md", "lines": [9, 9], "kind": "owner requirement (Ready/destination update)",
                  "text": lines("BRIEF.md", 9, 9)},
    "view.map": {"path": "src/queue-view-successor.ts", "lines": [2, 11], "kind": "consumer source (shared statusVisuals map, both consumers, display frameMs 100)",
                  "text": lines("src/queue-view-successor.ts", 2, 11)},
    "view.reduced": {"path": "src/queue-view-successor.ts", "lines": [16, 22], "kind": "consumer source (motionQuery, statusFrame reduced -> frame 0)",
                      "text": lines("src/queue-view-successor.ts", 16, 22)},
    "renderer.paint": {"path": "renderer-successor/view.mjs", "lines": [33, 44], "kind": "renderer fixture (nearest, draws only when width == 16*frames, slices frame*16)",
                        "text": lines("renderer-successor/view.mjs", 33, 44)},
    "renderer.routes": {"path": "renderer-successor/view.mjs", "lines": [94, 115], "kind": "renderer fixture (animation-frame and media-change routes, once per transition, origin reset, repaint live and matrix)",
                         "text": lines("renderer-successor/view.mjs", 94, 115)},
    "renderer.timeline": {"path": "renderer-successor/view.mjs", "lines": [134, 143], "kind": "renderer fixture (timeline samples at frame boundaries and the wrap; no wall-clock measurement)",
                           "text": lines("renderer-successor/view.mjs", 134, 143)},
    "plar.working.purpose": {"path": "authoring-plar.txt", "lines": [446, 446], "kind": "caller requirement update in selected PLAR (stationary Working distinct from Ready and Paused)",
                              "text": lines("authoring-plar.txt", 446, 446)},
    "plar.alpha": {"path": "authoring-plar.txt", "lines": [179, 179], "kind": "PLAR requirement reason (transparent; not binary alpha)",
                    "text": lines("authoring-plar.txt", 179, 179)},
    "focused.l27-31": {"path": "FOCUSED-SUCCESSOR.md", "lines": [27, 31], "kind": "caller assignment (interpretation rules D1-D4, selective AA/full alpha, reduced-motion mapping)",
                        "text": lines("FOCUSED-SUCCESSOR.md", 27, 31)},
    "focused.l20-23": {"path": "FOCUSED-SUCCESSOR.md", "lines": [20, 23], "kind": "caller assignment (frame-zero hold is a proposed implementation, not an owner motif)",
                        "text": lines("FOCUSED-SUCCESSOR.md", 20, 23)},
    "focused.l35-39": {"path": "FOCUSED-SUCCESSOR.md", "lines": [35, 39], "kind": "caller assignment (versioned destination; both consumers; prefers-reduced-motion and changes while open)",
                        "text": lines("FOCUSED-SUCCESSOR.md", 35, 39)},
    "adoption.l31-35": {"path": "SUCCESSOR-ADOPTION.md", "lines": [31, 35], "kind": "caller assignment (scope normal 100ms separately from stationary reduced; keep three alpha splits, full alpha/selective AA, in-cell margins, scoped expert pacing, qualitative coherence, inferred Start distinction)",
                         "text": lines("SUCCESSOR-ADOPTION.md", 31, 35)},
    "adoption.l45-46": {"path": "SUCCESSOR-ADOPTION.md", "lines": [45, 46], "kind": "caller assignment (reuse exact existing assets; provenance to original bytes)",
                         "text": lines("SUCCESSOR-ADOPTION.md", 45, 46)},
    "kit.review-route": {"path": ".agents/skills/export-kit/skills/pixl/references/request-review.md", "lines": [172, 180], "kind": "kit method (mechanical check cannot decide intentional foreground or unwanted matte; split or use visual mode)",
                          "text": lines(".agents/skills/export-kit/skills/pixl/references/request-review.md", 172, 180)},
    "kit.recipe": {"path": ".agents/skills/export-kit/skills/pixl/references/request-review.md", "lines": [32, 34], "kind": "kit method (required outcome separate from recipe; observations are not rejection rules)",
                    "text": lines(".agents/skills/export-kit/skills/pixl/references/request-review.md", 32, 34)},
    "kit.unlinked": {"path": ".agents/skills/export-kit/resources/spec/production-plan.md", "lines": [20, 28], "kind": "kit spec (authoring view choice expansion; unlinked does not mean irrelevant)",
                      "text": lines(".agents/skills/export-kit/resources/spec/production-plan.md", 20, 28)},
    "prior.D1-D4": {"path": "work/focused-successor/caller-comparison-final.json", "field": "prior_corrections_verified", "kind": "prior independent caller comparison (historical evidence, not owner authority)",
                     "text": json.dumps(load("work/focused-successor/caller-comparison-final.json")["prior_corrections_verified"])},
    "expert.pixl": {"kind": "pixel-art expert judgment (PIXL specialist / caller art reading)", "text": "Deliberate pixel placement with selective anti-aliasing versus resampling blur; evenly paced quarter-turn rotation for a segmented spinner; silhouette readability at native scale."},
}

# Caller's own reading per aligned stage/local key. Written from the literal
# text in 03/04 and the sources above, before opening the specialist's files.
READING = {
    "working/geometry": {
        "obligation_change": "clarified_and_rescoped",
        "literal_delta": "Same 64x16 four-cell layout and 16 px slicing. Adds that a transparent margin inside a cell is composition, not padding; names the source basis (view-successor frames 4 / cell / frameMs; fixture draws only when width == 16*frames); scopes the floor(elapsed/100) mod 4 advance to no-preference only; states reduced motion selects frame zero without changing sheet geometry.",
        "discriminating_alternative": "A 64x16 sheet whose glyphs occupy a centred 10x10 region with 3 px transparent in-cell margins. The before wording ('no ... padding') could be read to reject it; the after wording explicitly accepts it. The owner brief fixes only 16x16 cells and four horizontal frames.",
        "authority": ["brief.l3", "view.map", "renderer.paint", "view.reduced", "focused.l27-31", "adoption.l31-35"],
        "caller_disposition": "Consistent. Geometry obligation unchanged; margin clarification removes an unsupported reading; frame-advance scope follows the consumer source.",
    },
    "working/transparent-exterior": {
        "obligation_change": "route_split_outcome_unchanged",
        "literal_delta": "Before: mechanical/local 'all pixels outside the mark have alpha 0', citing a historical 193-pixel #808080 failure. After: visual/visual judgment that the intended exterior shows the panel with no unintended matte/tile/halo/fringe; a deliberate backing shape with transparent exterior is permitted; partial alpha and selective AA permitted; alpha-zero RGB insignificant; measured flags do not reject. The measurement moved to the new .diagnostic criterion.",
        "discriminating_alternative": "A frame with a deliberate 12x12 semi-opaque backing disc behind the segments and alpha-0 exterior. Before: a mechanical 'outside the mark' test would need to decide the disc is the mark; after: judged visually as intended subject design. Also: alpha-0 pixels carrying magenta RGB; before text is silent, after text says insignificant.",
        "authority": ["brief.l3", "plar.alpha", "kit.review-route", "kit.recipe", "focused.l27-31", "adoption.l31-35", "prior.D1-D4"],
        "caller_disposition": "Consistent. Owner outcome (transparent background) unchanged; deciding route corrected from mechanical to visual; the historical failure-class observation was an observation, not a rule, and remains in the old Q record. The 'no plate' clause removed from the old text was a specialist sample choice (choice.ready intent), never an owner requirement.",
    },
    "working/transparent-exterior.diagnostic": {
        "obligation_change": "added_split_diagnostic",
        "literal_delta": "New mechanical/local record: per-cell alpha histogram and nonzero-alpha component boxes; flag four-edge or >50% components for visual review only; no threshold is acceptance/rejection; alpha-zero RGB insignificant.",
        "discriminating_alternative": "A full-span glyph touching all four edges: flagged for review, not rejected. The flag is diagnostic.",
        "authority": ["kit.review-route", "adoption.l31-35", "expert.pixl"],
        "caller_disposition": "Consistent as a non-rejecting diagnostic split from the old transparent-exterior criterion. It must not be read as a threshold.",
    },
    "working/frame-assembly": {
        "obligation_change": "rescoped_to_reuse_path",
        "literal_delta": "Before: conditional assembly policy when provider output is not already the 64x16 sheet. After: reuse-only; record exact source cf101610...76dc and verify byte-identical destination; no assembly/edit; preserve raw provider outputs and assembly records; obsolete join and seed-rotation step-two checks non-applicable to this path.",
        "discriminating_alternative": "A newly joined strip assembled from raw provider frames. Before: acceptable with an assembly record; after: not acceptable under this plan without review of its own assembly policy. This narrowing is scoped to the reviewed reuse successor.",
        "authority": ["adoption.l45-46", "focused.l35-39"],
        "caller_disposition": "Consistent for this plan. Verified: renderer-successor/assets/working.png, assets/working.png and the candidate file share sha256 cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc.",
    },
    "working/activity-not-success": {
        "obligation_change": "rescoped_plus_reduced_motion",
        "literal_delta": "Before forbade frames forming a check mark, an arrowhead, pause bars or a success-like pose. After keeps the owner clause (no check mark / success-like terminal pose), demotes arrowhead/pause-bar avoidance to scoped expert guidance and sends the binding distinction to delivery.q.distinction, and adds: frame zero alone with its Working label must read as the stationary Working indicator distinct from Ready and Paused; frame choice is the specialist's proposal.",
        "discriminating_alternative": "A Working frame that briefly resembles a chevron but never a check mark. Before: rejected here by the arrowhead clause; after: judged in the collective distinction check rather than as a per-frame owner rule. The brief forbids success-likeness only.",
        "authority": ["brief.l3", "brief.l7", "view.map", "plar.working.purpose", "focused.l20-23", "focused.l27-31", "kit.recipe"],
        "caller_disposition": "Consistent. Start distinction is correctly attributed to the shared-consumer map, not to 'preserve the Start control'. Reduced-motion clause is the PLAR caller update, with frame zero as a specialist proposal.",
    },
    "working/motion-continuity": {
        "obligation_change": "owner_timing_kept_recipe_rescoped",
        "literal_delta": "Before: 100 ms playback with wrap; stable centre/anchor, stable cluster count and volume, stepped phases, no morphing/near-hold/wrap jump (the rejected AI-animation class). After: normal motion only; 100 ms playback at 1x and 3x with wrap; required outcome is one continuous loop with no visible discontinuity at the wrap; centre/anchor/volume are scoped expert checks from the Working contract; even pacing/no near-hold is the specialist's quality criterion for this reused rotating design, not an owner requirement; no universal cluster-count/no-morph recipe; reduced motion evaluated separately.",
        "discriminating_alternative": "A four-frame loop at 100 ms with an intentional ease (two close phases then two wide) that still reads continuous at the wrap. Before: rejected by 'near-hold'; after: could satisfy the brief after review because even pacing is a scoped expert criterion.",
        "authority": ["brief.l3", "focused.l27-31", "adoption.l31-35", "prior.D1-D4", "expert.pixl"],
        "caller_disposition": "Consistent. Owner 100 ms cadence retained; perceived motion quality attributed to expert judgment for this exact design. Verdict history: provenance.working.motion.unavailable (unavailable, obsolete) retained; current pass native-review.working.motion.verdict.0 recorded 2026-11-09T16:16:09+00:00 from recorded exposures. Real-time human playback appraisal remains a stated limitation of the still-image host.",
    },
    "working/style-coherence": {
        "obligation_change": "clarified_expert_exclusion_named",
        "literal_delta": "Adds 'consistent with the exact Ready baseline (selective, intentional anti-aliasing is permitted under the full-alpha contract; accidental resampling blur or stray noise is not)'. Retains: no exact hex, palette count, binary alpha, stroke width or margin rule.",
        "discriminating_alternative": "A bilinear-resampled icon with soft edges. Before: already fails 'deliberate ... stepped edges'; after: fails explicitly. No new rejection class; a hand-placed AA pixel at a diagonal is explicitly allowed.",
        "authority": ["brief.l3", "focused.l27-31", "adoption.l31-35", "expert.pixl"],
        "caller_disposition": "Consistent. Blur/noise exclusion is pixel-art expert judgment made explicit, scoped to coherence with the baseline, not an owner palette/stroke rule.",
    },
    "working/consumers": {
        "obligation_change": "widened_reduced_motion_and_switching_evidence_claim_precise",
        "literal_delta": "Before: actual consumer renderer with assets/working.png, 'observed live 100 ms frame advance including the wrap'. After: supplied fixture executing successor sources; descriptor path renderer-successor/assets/working.png; smoothing false; geometryMatches; timeline indices 0,0,1,1,2,2,3,3,0 at 0..400 ms with wall-clock not measured or claimed; reduce: frame zero via statusFrame, same pixel hash >= 800 ms in both consumers; switch to reduce while open via change event or next-animation-frame observation, once per transition; switch back restarts cycling at frame zero, no backend change/reload/stale canvas/duplicate animation.",
        "discriminating_alternative": "A renderer that handles reduce only at page load. Before: accepted (no switching clause); after: rejected. A fixture claiming measured 100 ms wall-clock intervals: before implied, after explicitly not claimed.",
        "authority": ["brief.l3", "brief.l9", "view.map", "view.reduced", "renderer.routes", "renderer.timeline", "plar.working.purpose", "focused.l35-39"],
        "caller_disposition": "Consistent. Owner 100 ms is enforced through display.frameMs 100 and the sampled frame indices; the weaker wording describes what the fixture can evidence, not a weaker requirement.",
    },
    "retry/geometry": {
        "obligation_change": "unchanged_text_sources_rebound",
        "literal_delta": "Check text identical; only the bound source set changed (provenance.source.* added, render.source.view/assessment/assignment, snapshot queue.ts and recheck findings dropped).",
        "discriminating_alternative": "Not applicable; no literal change.",
        "authority": ["brief.l3", "brief.l9", "view.map"],
        "caller_disposition": "Consistent. Identical text does not by itself prove equivalence, but here the obligation (one static 16x16 frame) is the same owner geometry.",
    },
    "retry/transparent-exterior": {
        "obligation_change": "route_split_outcome_unchanged",
        "literal_delta": "Same split as Working: mechanical alpha-0 exterior rule replaced by the visual exterior judgment; measurement moved to retry/transparent-exterior.diagnostic.",
        "discriminating_alternative": "As for Working: a deliberate backing shape with transparent exterior; alpha-zero RGB noise.",
        "authority": ["brief.l3", "plar.alpha", "kit.review-route", "focused.l27-31", "prior.D1-D4"],
        "caller_disposition": "Consistent.",
    },
    "retry/transparent-exterior.diagnostic": {
        "obligation_change": "added_split_diagnostic",
        "literal_delta": "Same diagnostic text as Working's.",
        "discriminating_alternative": "Full-span glyph flagged, not rejected.",
        "authority": ["kit.review-route", "adoption.l31-35"],
        "caller_disposition": "Consistent as non-rejecting diagnostic.",
    },
    "retry/retry-meaning-without-color": {
        "obligation_change": "clarified_recipe_disclaimed",
        "literal_delta": "'in grayscale' widened to 'a non-colour comparison (grayscale or binarized silhouettes)'; 'failed work / retry' reworded 'failed work with a retry action'; adds 'No specific retry motif (such as an arrow) is required.'",
        "discriminating_alternative": "A retry mark drawn as a broken circle with a gap (no arrowhead) that still reads as retry by shape. Both versions accept it; the after text says so explicitly.",
        "authority": ["brief.l3", "view.map", "kit.recipe"],
        "caller_disposition": "Consistent. Owner non-colour distinction preserved; the Start comparison is the shared-consumer inference.",
    },
    "retry/style-coherence": {
        "obligation_change": "clarified_expert_exclusion_named",
        "literal_delta": "Same AA/blur clause as Working's.",
        "discriminating_alternative": "As for Working.",
        "authority": ["brief.l3", "focused.l27-31", "expert.pixl"],
        "caller_disposition": "Consistent.",
    },
    "retry/consumers": {
        "obligation_change": "destination_retargeted_static_unchanged",
        "literal_delta": "Fixture and successor sources named; path renderer-successor/assets/error-retry.png (not assets/retry.png); smoothing false; geometryMatches; 'no animation loop runs for the descriptor (frames 1)' replaces 'static behavior'.",
        "discriminating_alternative": "A renderer that animates a 1-frame descriptor: rejected by both. A renderer serving the old assets/ path: accepted before, rejected after; the brief says the destination follows the updated view.",
        "authority": ["brief.l3", "brief.l7", "brief.l9", "view.map", "focused.l35-39"],
        "caller_disposition": "Consistent.",
    },
    "paused/geometry": {
        "obligation_change": "unchanged_text_sources_rebound",
        "literal_delta": "Check text identical; sources rebound.",
        "discriminating_alternative": "Not applicable.",
        "authority": ["brief.l3", "brief.l7", "view.map"],
        "caller_disposition": "Consistent.",
    },
    "paused/transparent-exterior": {
        "obligation_change": "route_split_outcome_unchanged",
        "literal_delta": "Before cited the 'rejected opaque magenta intermediate' failure class. After: visual judgment with alpha-zero RGB insignificant. The alpha-zero magenta RGB point (prior D1) is resolved by the after wording.",
        "discriminating_alternative": "Paused PNG whose alpha-0 pixels carry magenta RGB: composited over the panel they are invisible. Before text invites a false mechanical fail; after text excludes it.",
        "authority": ["brief.l7", "plar.alpha", "kit.review-route", "prior.D1-D4", "renderer.paint"],
        "caller_disposition": "Consistent.",
    },
    "paused/transparent-exterior.diagnostic": {
        "obligation_change": "added_split_diagnostic",
        "literal_delta": "Same diagnostic text.",
        "discriminating_alternative": "Full-span glyph flagged, not rejected.",
        "authority": ["kit.review-route", "adoption.l31-35"],
        "caller_disposition": "Consistent as non-rejecting diagnostic.",
    },
    "paused/pause-meaning-without-color": {
        "obligation_change": "clarified_recipe_disclaimed",
        "literal_delta": "Non-colour comparison widened; adds 'No specific pause motif (such as paired bars) is required.'",
        "discriminating_alternative": "A pause mark drawn as a single thick bar with a notch. Both accept if it reads as paused by shape; after says so explicitly.",
        "authority": ["brief.l7", "view.map", "kit.recipe"],
        "caller_disposition": "Consistent.",
    },
    "paused/style-coherence": {
        "obligation_change": "clarified_expert_exclusion_named",
        "literal_delta": "Same AA/blur clause.",
        "discriminating_alternative": "As for Working.",
        "authority": ["brief.l3", "brief.l7", "focused.l27-31", "expert.pixl"],
        "caller_disposition": "Consistent.",
    },
    "paused/consumers": {
        "obligation_change": "destination_retargeted_static_unchanged",
        "literal_delta": "Fixture named; path renderer-successor/assets/paused.png; smoothing false; geometryMatches; no animation loop for frames 1.",
        "discriminating_alternative": "As for Retry.",
        "authority": ["brief.l7", "brief.l9", "view.map", "focused.l35-39"],
        "caller_disposition": "Consistent.",
    },
    "delivery/continuity": {
        "obligation_change": "clarified_plus_reduced_motion",
        "literal_delta": "Adds 'readable visual weight coherent with the Ready baseline (identical stroke width or footprint is not required)'; adds Working's '100 ms playback with the wrap under no-preference, and its stationary frame-zero presentation under reduce'.",
        "discriminating_alternative": "A Paused mark with 2 px bars beside a Ready check with 1 px strokes, both deliberate and legible. Before: 'readable visual weight' could be read as comparable thickness; after: explicitly not required.",
        "authority": ["brief.l3", "plar.working.purpose", "focused.l27-31", "adoption.l31-35", "prior.D1-D4"],
        "caller_disposition": "Consistent. Coherence remains qualitative; no identical-weight rule.",
    },
    "delivery/distinction": {
        "obligation_change": "reduced_motion_added_attribution_split",
        "literal_delta": "Adds stationary Working frame zero alone in the non-colour comparison, with required distinction from Ready and Paused; states that distinction from Retry and Start is the shared-consumer inference, not an owner motif requirement.",
        "discriminating_alternative": "A stationary Working frame that resembles the Retry ring. Owner text does not forbid it; the shared-consumer inference still flags it for the caller's judgment, labelled as inference.",
        "authority": ["brief.l3", "brief.l7", "view.map", "plar.working.purpose", "focused.l27-31", "prior.D1-D4"],
        "caller_disposition": "Consistent. Authority correctly split between owner clauses and the inference from one statusVisuals map rendering all five states in the same cells.",
    },
    "delivery/destination": {
        "obligation_change": "retargeted_widened_evidence_claim_precise",
        "literal_delta": "Before: confirmed destination paths assets/*, '100 ms timing', recorded integer placement, assets/start.svg hash unchanged. After: caller-reviewed proposed successor destination (src/queue-view-successor.ts plus renderer-successor/ with copied exact assets), old files byte-unchanged; frame index floor(elapsed/100) mod frames at sample points incl. 400 ms wrap, wall-clock not measured; placement as adopted method; renderer-successor/assets/start.svg unchanged; both reduced-motion settings and switching each direction; both consumers update together without backend change; reduce draws [0,0,16,16]; route via change event or next animation frame, no requirement the browser dispatch a change event; origin reset once per transition; repaint live and matrix.",
        "discriminating_alternative": "A destination that updates only statusCell on preference change: accepted before (no clause), rejected after. A fixture that asserts the browser fired a change event: not required after; view.mjs comments that some headless hosts do not dispatch it.",
        "authority": ["brief.l5", "brief.l9", "view.map", "view.reduced", "renderer.routes", "renderer.timeline", "focused.l35-39", "adoption.l31-35"],
        "caller_disposition": "Consistent. Verified start.svg sha256 ee2ba2fe20bd09a2c9a9c96d889f766e8af80fcdf704e8172934135e2b7e12d3 at both assets/ and renderer-successor/assets/. 'Destination now follows the updated view' (brief line 9) supports the versioned destination without rebinding the historical render.choice.destination.",
    },
}

THEMES = {
    "a.alpha_diagnostic_vs_visual_exterior": {
        "criteria": ["working/transparent-exterior", "working/transparent-exterior.diagnostic", "retry/transparent-exterior", "retry/transparent-exterior.diagnostic", "paused/transparent-exterior", "paused/transparent-exterior.diagnostic"],
        "change": "The owner outcome 'transparent backgrounds' is unchanged. The deciding route moved from a mechanical alpha==0 exterior test to a visual judgment of the intended exterior at 1x/3x on the panel, and the measurement became a separate, explicitly non-rejecting diagnostic. Historical failure classes (193 #808080 pixels; opaque magenta intermediate) left the rule text; they stay in the old Q records as observations.",
        "authority": ["brief.l3", "plar.alpha", "kit.review-route", "kit.recipe", "adoption.l31-35", "prior.D1-D4"],
    },
    "b.geometry_vs_invented_margins": {
        "criteria": ["working/geometry", "retry/geometry", "paused/geometry"],
        "change": "Owner geometry (16x16 cells; four horizontal Working frames) is unchanged. Working's text now says a transparent margin inside a cell is composition, not padding, removing a reading that would have invented a no-margin rule; the renderer only requires width == 16*frames and height == 16.",
        "authority": ["brief.l3", "view.map", "renderer.paint", "focused.l27-31"],
    },
    "c.fixed_100ms_vs_perceived_motion_quality": {
        "criteria": ["working/motion-continuity", "working/consumers", "working/geometry", "delivery/destination"],
        "change": "100 ms per frame is the owner's requirement and is retained in every normal-motion clause and in display.frameMs. Even angular pacing, no near-hold, stable centre/volume and cluster count are expert quality criteria, now labelled as such and scoped to this reused rotating design. The fixture's evidence claim was made precise: frame indices at sampled elapsed times, wall-clock not measured.",
        "authority": ["brief.l3", "view.map", "renderer.timeline", "focused.l27-31", "adoption.l31-35", "prior.D1-D4", "expert.pixl"],
    },
    "d.family_coherence_vs_identical_weight": {
        "criteria": ["working/style-coherence", "retry/style-coherence", "paused/style-coherence", "delivery/continuity"],
        "change": "Coherence with the exact Ready baseline remains qualitative. Delivery continuity now states identical stroke width or footprint is not required. Member checks explicitly permit selective intentional anti-aliasing under the full-alpha contract and exclude accidental resampling blur or stray noise as expert pixel-art judgment.",
        "authority": ["brief.l3", "focused.l27-31", "adoption.l31-35", "prior.D1-D4", "expert.pixl"],
    },
    "e.reduced_motion_and_live_preference_in_shared_consumers": {
        "criteria": ["working/consumers", "working/activity-not-success", "delivery/destination", "delivery/distinction", "delivery/continuity"],
        "change": "New obligations: under reduce both statusCell and compactStatus show stationary Working frame zero with the Working label and unchanged 64x16 geometry; switching the preference while open repaints both live and matrix cells once per observed transition through either the media change event or the next animation frame's matchMedia.matches; switching back restarts cycling at frame zero; backend state never changes. Frame zero is a specialist proposal inside the PLAR caller requirement 'stationary Working symbol distinguishable from Ready and Paused'. Distinction from Retry and the preserved Start is a shared-consumer inference because one statusVisuals map feeds both consumers.",
        "authority": ["plar.working.purpose", "view.map", "view.reduced", "renderer.routes", "focused.l20-23", "focused.l35-39", "brief.l3", "brief.l7"],
    },
}


def main() -> int:
    diff = load("work/choice-comparison/07-criterion-literal-diff.json")
    changes = load("work/choice-comparison/02-request-review-changes.json")
    ctx = load("work/choice-comparison/01-context-authoring.json")
    reviews = {
        "working": load("work/choice-comparison/08-review-context-working-candidate.json"),
        "delivery": load("work/choice-comparison/09-review-context-family-candidate.json"),
        "retry": load("work/choice-comparison/10-review-context-retry-candidate.json"),
        "paused": load("work/choice-comparison/11-review-context-paused-candidate.json"),
    }
    verdict_by_id = {}
    for stage, rc in reviews.items():
        for c in rc["criteria"]:
            verdict_by_id[c["id"]] = {"status": c["status"], "verdict": c["verdict"], "candidate": rc["candidate"], "task_status": rc["task_status"]}

    rows = []
    missing_reading = []
    for r in diff["criteria"]:
        key = r["key"]
        reading = READING.get(key)
        if reading is None:
            missing_reading.append(key)
            continue
        row = {
            "key": key,
            "alignment": r["alignment"],
            "compact_changed_fields": r.get("compact_changed_fields"),
            "before": {k: r["before"][k] for k in ("id", "record_sha256", "domain", "mode")} if "before" in r else None,
            "after": {k: r["after"][k] for k in ("id", "record_sha256", "domain", "mode")} if "after" in r else None,
            "check_text_identical": r.get("check_text_identical"),
            "current_verdict": verdict_by_id.get(r["after"]["id"]) if "after" in r else None,
            **reading,
        }
        rows.append(row)

    before_index = {x["id"]: x["record_sha256"] for x in changes["criterion_index"]["before"]}
    after_index = {x["id"]: x["record_sha256"] for x in changes["criterion_index"]["after"]}
    mapped_before = {row["before"]["id"] for row in rows if row["before"]}
    mapped_after = {row["after"]["id"] for row in rows if row["after"]}

    historical = changes["review_attention"]["after"]["failures_obsolete_or_stale"]
    working_rc = reviews["working"]
    motion_now = verdict_by_id["provenance-correction.working.q.motion-continuity"]

    exports = {}
    for name in sorted(p.name for p in WORK.glob("*.json")):
        exports[name] = {"path": f"work/choice-comparison/{name}", "sha256": sha(WORK / name), "bytes": (WORK / name).stat().st_size}

    result = {
        "version": 1,
        "kind": "caller_independent_comparison",
        "reviewer_role": "independent native caller (parent Claude Code session, claude-fable-5-1); not PIXL self-review",
        "written_before_opening_specialist_output": True,
        "state": {"path": ".pixl/assets/queue.ready/state.px", "sha256": ctx["hash"], "revision": ctx["revision"], "state_file_sha256_recomputed": sha(ROOT / ".pixl/assets/queue.ready/state.px")},
        "plans": diff["plans"],
        "exports_read": exports,
        "choices": {
            "selected_linked": [{"id": c["id"], "record_sha256": c["record_sha256"], "key": c["fields"]["ky"], "status": c["fields"]["st"]["$symbol"]} for c in ctx["choices"]],
            "other_intake_unlinked": ctx["choice_scope"]["other_intake"],
            "other_intake_retrievals": {
                "focused-successor.choice.destination": exports.get("05-other-intake-focused-successor.choice.destination.json"),
                "choice.ready": exports.get("06-other-intake-choice.ready.json"),
                "note": "Both retrievals return the same complete-context closure bytes because each I record closes over the project P, which lists every intake choice. The focus differs; the closure is identical. Both full choice values were read from the wire text.",
            },
            "why_unlinked_is_not_irrelevant": [
                "The authoring view expands choices only through declared semantic links from the selected plan's outputs, contracts, destinations, inputs and decisions. Not being reached by that traversal says nothing about applicability; the kit spec states 'Unlinked does not mean irrelevant' and the index exists so the caller can inspect such a choice.",
                "focused-successor.choice.destination carries the same destination values as the selected provenance.choice.destination (alpha full, 16x16 cells, both consumers, versioned fixture, 100 ms, #172336, renderer-successor/assets paths, stationary frame zero under reduce). It is unlinked only because the corrected plan binds the re-timed provenance.source.* records; the earlier choice bound the successor.source.* records with the unsupported 20:00 timestamps. Its status 'confirmed' is unchanged, and it imposes nothing the selected choice does not already carry.",
                "choice.ready (proposed) is the first-round Ready intent: destination assets/ready.png, cue #70b9ed, and 'Checkmark motif, chunky strokes, cool blue near #70b9ed with a lighter highlight and no backing plate are specialist sample choices, revisable at style review'. It is superseded by r.22e90a2a03fe453a.choice.ready but remains relevant evidence: it shows that 'no backing plate' was a specialist sample choice, which supports reading the new transparent-exterior clause 'a deliberate backing shape is permitted' as removing an expert recipe from an owner-level rule rather than loosening an owner requirement.",
                "Conversely, an unlinked choice grants no new restriction: its values are proposed/confirmed intake records whose authority is fixed by their own sources, and this read-only view changes no saved I status or acceptance rule.",
            ],
            "authority": ["kit.unlinked"],
        },
        "criterion_accounting": {
            "original_total": len(before_index), "successor_total": len(after_index),
            "original_all_mapped": set(before_index) == mapped_before,
            "successor_all_mapped": set(after_index) == mapped_after,
            "index_hashes_match_full_reports": all(r["before"]["index_sha256_matches"] for r in diff["criteria"] if "before" in r) and all(r["after"]["index_sha256_matches"] for r in diff["criteria"] if "after" in r),
            "aligned_pairs": diff["counts"]["aligned_pairs"], "added_diagnostics": diff["counts"]["added"], "removed": diff["counts"]["removed"],
            "identical_check_text_pairs": [r["key"] for r in rows if r.get("check_text_identical")],
            "domain_mode_changed_pairs": [r["key"] for r in rows if r["before"] and r["after"] and (r["before"]["domain"], r["before"]["mode"]) != (r["after"]["domain"], r["after"]["mode"])],
            "all_23_current_verdicts_pass": all(v["status"] == "pass" for v in verdict_by_id.values()) and len(verdict_by_id) == 23,
            "verdict_count": len(verdict_by_id),
        },
        "criteria": rows,
        "themes": THEMES,
        "authority_index": AUTHORITY,
        "source_drift": {
            "unchanged": ["render.source.brief (BRIEF.md)", "render.source.caller (work/family-render-review/caller-comparison-final.json)"],
            "removed_from_criteria_binding": ["render.source.view (src/queue-view.ts; old consumer, superseded as destination basis)", "render.source.assignment (RENDER-STAGE.md)", "render.source.assessment (work/family-render-review/specialist-assessment.json)", "r.22e90a2a03fe453a.source.4 (retained snapshot of src/queue.ts; same bytes as provenance.source.backend)", "recheck.source.findings (work/pixl-render-recheck-01/findings.json)"],
            "added": ["provenance.source.view (src/queue-view-successor.ts)", "provenance.source.renderer (renderer-successor/view.mjs)", "provenance.source.assignment (SUCCESSOR-ADOPTION.md)", "provenance.source.proposal (work/focused-successor/specialist-proposal-r4.json)", "provenance.source.comparison (work/focused-successor/caller-comparison-final.json)", "provenance.source.backend (src/queue.ts)"],
            "meaning": "Authority moved from the old consumer and render-stage assignment to the versioned consumer, its fixture and the successor adoption assignment. Source class does not grant requirement authority: the brief remains the only owner source; proposal/comparison files are specialist and prior-caller records.",
            "diagnostics_retained": diff["diagnostics"]["after"],
            "needs_narrower_range_note": "provenance.source.proposal (3144 lines) and provenance.source.comparison (747 lines) are bound whole-file, so the full report cannot excerpt them. Read directly: r4 art_choice / request.reduced / revision_changes and the caller comparison's prior_corrections_verified D1-D4 and 20 criterion_comparisons.",
        },
        "verdict_distinction": {
            "current_accepted_review": {
                "working_candidate": working_rc["candidate"], "task_status": working_rc["task_status"], "current_acceptance": working_rc["current_acceptance"],
                "motion_criterion": {"id": "provenance-correction.working.q.motion-continuity", **motion_now, "review": "native-review.working.motion", "review_sha256": "8a209b3df1dfc73e9d1aec04e04403d2fb08c0d4ce92ab454263d308a239cb80", "observed_at": "2026-11-09T16:16:09+00:00", "supersedes": "provenance.working.motion.unavailable", "request": "work/native-review/02-working-review-request.json", "result": "work/native-review/02-working-review-result.json"},
                "family_candidate": reviews["delivery"]["candidate"], "family_task_status": reviews["delivery"]["task_status"], "family_current_acceptance": reviews["delivery"]["current_acceptance"], "family_snapshot_acceptance_creation_time": reviews["delivery"]["snapshot_acceptance"],
                "retry": {"candidate": reviews["retry"]["candidate"], "task_status": reviews["retry"]["task_status"], "current_acceptance": reviews["retry"]["current_acceptance"]},
                "paused": {"candidate": reviews["paused"]["candidate"], "task_status": reviews["paused"]["task_status"], "current_acceptance": reviews["paused"]["current_acceptance"]},
            },
            "historical_unavailable_evidence": historical,
            "reading": "The unavailable verdict provenance.working.motion.unavailable remains a true historical observation (still-image host could not judge real-time pacing). It was superseded, not erased, by native-review.working.motion.verdict.0, which cites 17 recorded exposures at roughly 100 ms spacing with wrap exposures identical to frame 0. That pass is a judgment from recorded exposures and sampled frame indices; real-time human playback appraisal is still not asserted. Adding the three alpha diagnostics changes none of this. Saved completed acceptance exists already and is not re-earned by this reading.",
        },
        "caller_findings": [
            "All 20 original and 23 successor criterion IDs and record hashes are present in the compact index and the two full reports, and the index hashes match the full-report record hashes.",
            "Only retry/geometry and paused/geometry have identical check text; every other aligned pair changed literal text, and the three transparent-exterior pairs also changed domain/mode (mechanical/local -> visual/visual) with a new diagnostic split. Stage/local ID alignment is structural only.",
            "No successor criterion drops an owner outcome from BRIEF.md lines 3, 7 or 9. Added clauses are either consumer-sourced (versioned destination, reduced motion, live switching), scoped expert judgments labelled as such, or evidence-claim precision (wall-clock not measured).",
            "The compact report's diagnostics flag two whole-file source bindings as needs_narrower_range; this is a binding-range limitation of provenance.source.proposal and provenance.source.comparison, not a criterion defect, and was worked around by reading the files directly.",
            "Both other-intake retrievals produce byte-identical closures (sha256 eba99386...2147d); the tool delivers the full choice record either way. No error, but a caller should not treat two identical files as two independent observations.",
            "Caller tooling note: the first run of extract_literal_diff.py mis-sliced the stage/local key (sha256 a5c87df7f56a8611c8038369c8a259f70adcb6a991b347b0e399df6b8985229e, overwritten). Alignment was unaffected because both sides were offset equally; the corrected file 53563ead... is the retained one. No interpretation depended on the earlier file.",
        ],
        "limits": "Caller comparison of literal text and named sources. Not a new visual acceptance, provider result, or evidence of broad artistic/host reliability. The earlier interrupted Claude comparison is not resolved by this trial.",
    }
    if missing_reading:
        result["missing_reading_keys"] = missing_reading
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"path": str(OUT.relative_to(ROOT)).replace("\\", "/"), "sha256": sha(OUT), "accounting": result["criterion_accounting"], "missing_reading": missing_reading}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
