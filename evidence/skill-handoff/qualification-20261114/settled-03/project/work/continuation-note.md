# Continuation note: side-view character family (scout, medic)

Written by PIXL at the end of the 2026-11-15 session. Store: `.pixl/characters`
(state revision 14, hash 8362097a45b3a1a43c831db21f002bc7a94a51651c559ae5180d2adf1e153ab6 at
the time of writing; reread `pixl_workflow` before acting). Queue: `plar.txt`.

## What exists

| Item | Where | Status |
| --- | --- | --- |
| Owner brief | `BRIEF.md` | Source `brief`, bound in PLAR and state |
| Scout sample | `candidates/scout-local-01.png` (X `scout_local_01`) | Task `scout_sample` **done**; all 6 criteria passed in `scout_review_01` |
| Medic preview | `candidates/medic-local-01.png` (X `medic_local_02`, same bytes as `medic_local_01`) | Task `family_plan_02.medic.task` open; all 6 criteria passed in `medic_review_01`; **not nominated** |
| Family plan | `family_plan_02.plan` | Medic stage + delivery; PLAR `character.medic` bound by selection; `character.family` linked manually |
| Superseded plan | `family_plan_01.plan` | Its two tasks are `dropped` (a decision-link edit changed its plan context); `medic_local_01` and `medic_inspect_01` remain as history |
| Adoption decision | `adopt_family_construction` + proof `work/proofs/adopt-family-construction.json` | Valid; wired into plan 02 |
| Creative brief for PixelLab | `work/request/scout-creative-brief.md` | Not executable: no provider schema was discovered |

Both candidates are **deterministic local constructions** by PIXL
(`work/scripts/build_scout.py`). No generation provider was assigned or called.
Lineage shows `provenance_status: unrecorded` because there is no provider job.

## Decision table

| Choice (I record) | Authority / status | Answer needed now? | Effect of the answer |
| --- | --- | --- | --- |
| canvas 32x32, outline, palette roles, binary alpha, side view, nearest sampling | Owner, **confirmed** (BRIEF.md) | No | Already drive the contract |
| `palette_hex` = #56b5bc / #f4dda2 / #25354a | PIXL proposal from measured references | **Yes** | Confirming unblocks `family_plan_02.medic.task` (with `lighting`) |
| `lighting` = flat fill, no ramps/AA | PIXL proposal from reference observation | **Yes** | Same blocker as above; choosing shading instead needs more colors and a revised contract |
| Baseline = local construction `scout_local_01` | PIXL sample, task done | **Yes (owner adoption)** | Keep it, or request a PixelLab revision of the scout when a connection exists |
| `facing` right, `scout_identity`, `medic_identity` | PIXL proposals | Not blocking | Shape the current drafts; change requires new candidates |
| `destination_scout`, `destination_medic` paths | PIXL proposals | Before delivery | Confirming unblocks `family_plan_02.delivery.task` activation |
| `destination_engine` | Unresolved | Before delivery | Needed for the live `destination_display` criterion |
| `display_scale` | Unresolved | Not blocking | Would add a review at the real game scale |

## Exact next local operations

1. Owner answers the three "Yes" rows. Record confirmations by amending the I
   records (`st=confirmed`, add a source line in BRIEF.md) through `pixl_commit`.
2. If the local medic is accepted: `pixl_task_complete` on `family_plan_02.medic.task`
   with `medic_local_02`. If PixelLab art is wanted: discover the real tool schema,
   then `pixl_stage_prepare` for stage `medic` of `family_plan_02.plan` (and a
   `revise` of the scout if the baseline is replaced).
3. Confirm destinations, then `pixl_family_snapshot` on `family_plan_02.delivery.output`,
   review continuity through `pixl_review_context` / `pixl_candidate_review`, and
   leave `destination_display` unavailable until an engine exists.

## Limits

- All reviews are self-reviews by the constructing agent; no independent caller comparison.
- Visual checks were at 1x and 8x on white and #202838 only.
- Engine import and nearest-neighbor display in the game are unverified.
