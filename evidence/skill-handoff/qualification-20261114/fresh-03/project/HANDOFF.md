# Handoff: side-view character family (scout, medic)

Written by PIXL on 2026-11-14 (local). Project root is this consumer directory. Paths below are relative to it.

## Status: needs_input

Intake, requirements queue and the first sample plan are saved. No art has been generated. Two owner decisions block the scout sample's concrete contract, and no PixelLab connection exists in this session.

## What is retained

| Item | Location |
| --- | --- |
| Owner instructions and reference observations | `BRIEF.md` |
| Requirements queue (3 rows: character.scout, character.medic, character.family) | `plar.txt` |
| PX2 production store, revision 1 | `.pixl/characters/state.px` |
| Reference enlargements (12x nearest) | `work/inspect/reference-x12.png`, `work/inspect/reference-b-x12.png` |
| Outline comparison sheet, both references at 8x on white, dark and mid-green backgrounds | `work/inspect/outline-comparison-x8.png` |

Store contents: project `project`, actors `user` and `actor` (PIXL), sources `brief`/`ref_a`/`ref_b`, nine intake choices, sample task `t_scout_sample` with planned output `f_scout_sample` and four criteria (`q_size`, `q_scout_identity`, `q_edge_treatment`, `q_style_kinship`). The task is open and blocked only on `output_contract` because `f_scout_sample` has no concrete C yet.

## Intake choices and their authority

| Key | Status | Value | Authority |
| --- | --- | --- | --- |
| projection | confirmed | side | owner instruction |
| members | confirmed | scout, medic | owner instruction |
| px (canvas) | unresolved | null | owner has not chosen |
| edge_treatment | conflict | continuous 2px dark outline vs no outline | references disagree; owner has not chosen |
| animation_set | unresolved | null | not supplied |
| destination | unresolved | null | not supplied |
| alpha_policy | observed | binary | measured from references |
| palette_roles | observed | body #56B5BC, eyes #F4DDA2, outline #25354A | measured from references |
| reference_canvas | observed | 32x32 (visible 19x26) | measured from references |

Observed values are not adopted requirements. Only the owner's confirmation or an explicit adoption decision turns them into production rejection rules.

## Visual observations (PIXL, comparison sheet viewed at 8x)

- Both references show one mascot form: rounded-rectangle body, two short posts on top, two cream eyes. The scout and medic are new designs that must share this construction, not copies of this mascot.
- On white and mid-green backgrounds the outlined version (`reference.png`) has a crisp, fully defined edge; the outline-free version (`reference-b.png`) reads as a clean flat shape but its edge depends on the teal-versus-background contrast.
- On the near-black background the dark navy outline has little contrast with the background, so the outlined character reads as the smaller teal interior with a dark gap around it. The outline-free version keeps its full silhouette there.
- At the same canvas the outline costs about 2px of interior on each side. Eyes are the same size in both, so the outline's main cost is interior detail budget for role landmarks.

## PIXL proposals (not decisions)

1. Edge treatment: a continuous dark outline suits light or busy backgrounds and keeps edges stable across them, but it needs enough contrast against the game's darkest backgrounds to stay useful. The outline-free treatment gives more interior room and reads well on dark backgrounds. A selective outline is a third option not shown by either reference. Knowing the game's typical background values would make this choice straightforward.
2. Canvas: 32x32 matches the references and leaves room for a scout landmark (for example a scarf or pack) and a medic landmark (for example a cross); a smaller canvas with the outline would crowd those landmarks. This is a proposal to test on the scout sample, not an adoption.
3. First sample: one static side-view scout pose on a transparent background. Animation sets stay open and should be decided before the canvas is final if frames need headroom for motion.

## Next operation once the two answers arrive

1. Record the owner's answers as sources (append to `BRIEF.md`), set `canvas` to confirmed and `edge_treatment` to confirmed in `.pixl/characters/state.px`, add a C contract linked through `ch`, set `f_scout_sample.ct`, and commit revision 2 with the current state hash.
2. When a PixelLab connection is available: discover the actual tool schema, write `work/scout-request.json`, `work/scout-plan.json`, `work/request-review.json` and `work/connection.json`, then `pixl_plar_prepare` for `character.scout` with the fresh `requirements_hash`. Dispatch, observe, import and review through the normal operations.
3. After the scout candidate passes its four criteria and the task is completed, author the medic stage and family delivery with `pixl_production_plan` using the accepted scout candidate as `baseline`, then continue with `pixl_stage_prepare`.

## Limits

- No generation provider is configured; no request was prepared or dispatched, and no provider identifiers exist.
- Engine import behavior is unavailable until a destination is supplied; it is recorded as unresolved, not as a failure.
- All visual notes above are observations of the two 32x32 references and the comparison sheet. They do not establish the owner's aesthetic.
