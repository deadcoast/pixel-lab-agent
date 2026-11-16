# Continuation note, 2026-11-15

Cold resume of the scout and medic family project by PIXL (agent) in an isolated
evaluation session, assigned by a calling agent. No generation provider, official
PixelLab tool or game engine is connected in this session, so nothing was generated and
no provider job exists. The earlier notes (`deliverables/continuation-2026-11-14.md`,
`deliverables/outline-decision-brief.md`) are preserved unchanged; this note amends
their reading where stated below and does not alter any saved acceptance.

## State identity on entry

- `state.px/state.px`: PX2, revision 6, canonical state hash
  `b9a66beff93bcc2197a442d1de8ed6d7d9178aacf0c10606512a38e64d78b5b7`, 57 records,
  valid, all bound files verified.
- Tasks: `t_study` and `t_aid` done with passing verdicts; `t_sample` open with the single
  blocker `output_contract: f_sample needs a concrete raster contract`; `t_scout`,
  `t_medic`, `t_family` open behind it. Ready list empty. No families, no jobs.
- Owner brief (`sources/brief.md`, 2026-09-14, verbatim): roster scout + medic, side-view
  game, references `reference.png` and `reference-b.png` which disagree about outline
  treatment, final canvas size explicitly not chosen, scope "begin the project and make
  the progress possible in this session".

## Independently re-checked this session

- Both references re-measured with the bundled asset check: 32 x 32, 390 visible pixels,
  visible bbox x 7..24 / y 3..27, zero fractional-alpha pixels, one opaque component;
  reference.png 3 colours, reference-b.png 2 colours. Matches the retained study.
- Every bound source file re-hashed; all match their S records (brief, study, methods,
  both references, previous continuation, decision brief, comparison sheet).
- Viewed: `deliverables/outline-scale-comparison.png` and the 12x views under
  `work/reference-views/`. What was seen agrees with the decision brief: both treatments
  read on the light band; on the dark band the navy contour merges with the field and the
  outlined figure reads smaller with near-invisible stalks; on the busy band the contour
  is what separates the outlined figure while the plain teal starts to blend. At 1x the
  two treatments are not reliably told apart; from 3x they are. The navy in reference.png
  also forms the shoulder bar, base bar and the whole of both stalks.

## What changed in the store this session (revision 7)

Four additions, no status changes, no change to any existing record's acceptance:

| Record | Kind | Content | Why |
|---|---|---|---|
| `s_continuation_2` | S | this note | Retains the amended continuation as a project source. |
| `i_lighting` | I, key `li`, **observed** | `flat (no directional light, no shading ramps)` from `s_refobs`, `s_ref_a`, `s_ref_b` | A concrete raster contract (`C`) requires a lighting field `li`; no intake choice held it, so the next operation would have stalled on an undeclared prerequisite. Observed from the references only; not a confirmed output policy. |
| `i_animation` | I, key `animation`, **unresolved** | null; sources `s_brief`, `s_refobs` | The brief names a "character family" but no poses, cycles, directions or timing, and neither reference shows motion; both retained sources name this gap. Not needed for the sample. Before scout/medic production it decides whether each output is one sprite or an animation set, which changes the planned output kinds and the PixelLab operation. |
| `handoff_3` | N, rv 7 | focus on this note, the open choices and the two accepted research artifacts; next `t_sample` | Resumption pointer. |

Not done, deliberately: no `C` contract (canvas is unresolved and outline is in conflict,
and the runtime blocks any task whose contract links an unresolved or conflicting choice);
no intake status moved; no criterion text edited; no candidate, verdict or evidence
touched.

## Corrections to the 2026-11-14 reading (old to new)

1. **Design language is not a blocker.** The previous table marked `i_design_language`
   as needed now ("the sample request cannot be written honestly without this"). The
   runtime does not gate a sample on a proposed choice, and the skill's own rule is that
   a scoped expert proposal can support an authorized sample while the final choice stays
   open. Side view is already confirmed (`i_view`), so the reference pose cannot be
   reproduced literally in any case; the proposal only names which reference properties
   the side-view figure carries. New reading: not blocking; the sample is the trial of this
   proposal; the owner can override it, and an early answer changes the readability
   landmarks (see 4). Status stays **proposed**.
2. **A hidden contract prerequisite was missing.** `C` requires `li`. Added `i_lighting`
   (observed) so the contract can be written as soon as the two owner answers arrive.
3. **The runtime gate is narrower than the earlier note implied.** Only choices linked
   through the sample output's contract (`C.ch`) gate `t_sample`, and for a sample phase
   `observed`/`proposed` values are acceptable; only `unresolved`/`conflict` block.
   Confirmation is required for `t_scout`/`t_medic`/`t_family` (production/delivery),
   which also need an evidence-backed decision record `D`. The earlier note did not
   distinguish these, and so overstated what the owner must confirm before a sample.
4. **Two saved criteria presume answers that are still open.** These are plan defects to
   fix in the same commit that saves the contract, not now, because their correct text
   depends on the path the owner chooses:
   - `q_canvas`, `q_palette`, `q_outline` are worded against the **confirmed** canvas,
     palette and outline treatment. On the owner-confirms path that is right. On a
     delegated-trial path nothing is confirmed, so these three would be unsatisfiable for
     the sample; sample-specific copies worded against "the sample contract" (e.g.
     `q_sample_canvas`, `q_sample_palette`, `q_sample_outline`) must replace them in
     `f_sample.rq` before any candidate is evaluated. Production outputs keep the
     confirmed wording.
   - `q_readability` requires "separable head, torso and limb landmarks". The references
     have no head/torso split and no limbs (a single body block with two stalks, two eyes
     and, in reference.png, shoulder and base bars). The silhouette-readability method
     (`s_methods`) asks for *named identity landmarks*; the head/torso/limb list is the
     predecessor's assumption of a limbed figure, which is exactly what
     `i_design_language` leaves proposed. Proposed replacement text once the sample
     contract exists: "At native scale and at the target integer zoom, on light, dark and
     busy test backgrounds, the figure reads as a side-view character with an
     unambiguous facing direction, and the identity landmarks named in the sample
     contract remain separable." The landmark list is then written into the contract's
     own record (`C.nm` or the handoff) from the adopted construction.
5. **Palette confirmation is coupled to role differentiation.** `q_palette` is exclusive
   ("no colours outside it"). If the owner confirms the palette as exactly the reference
   colours and the role device later turns out to need an accent hue, the palette must be
   reopened. Recommendation: confirm the palette only together with the role device, or
   confirm it explicitly as the base palette with one reserved accent slot.

## Decision table

Authority: who decides, and the saved status. "Needed now" means the next local
operation (saving the sample contract) cannot proceed without it. An answer adopts only
the choices it explicitly supplies; unasked rows keep their status.

| Choice (record) | Authority / saved status | Needed now? | Effect of the answer |
|---|---|---|---|
| Outline treatment (`i_outline`) | Owner; **conflict** between the two references (owner stated the disagreement) | **Yes** | See question 1. Decides whether `#25354A` is in the palette and what `q_outline` tests. The references contain two treatments; the owner has required neither. |
| Canvas size (`i_canvas`) | Owner; **unresolved**, explicitly deferred by the owner | **Yes** | See question 2. The references are 32 x 32 (observation, not a requirement). Lets `C.px` be written. |
| Game backgrounds (`i_backgrounds`) | Owner; **unresolved** | Helpful, not blocking | Turns the outline choice into an informed one (sheet: outline helps on busy mid-value fields, hurts on dark ones) and makes the readability review backgrounds representative instead of the agent's light/dark/busy test set. |
| Design language (`i_design_language`) | Owner; **proposed** by the predecessor (style swatch, not the body design) | No (corrected) | The sample trials this proposal. If the owner says the side-view figure must keep the reference's stalk-and-block body, the readability landmarks are the stalks, notch, eyes and bars; if a different construction is wanted, name it and the landmarks follow. |
| Lighting (`i_lighting`, new) | Owner; **observed** flat | No; supplies `C.li` | Observed from the references; the sample uses it as-is. Confirming it is only needed before production. |
| Animation (`i_animation`, new) | Owner; **unresolved** | No, not before scout/medic production | Decides whether `f_scout`/`f_medic` stay single sprites or become animation sets (new F kinds, different PixelLab operation, continuity criteria per cycle). |
| Display scale (`i_display_scale`) | Owner; **unresolved** | Before visual review of the sample, not before the contract | Sets the integer zoom for `q_readability` and `q_style_match`. The sheet shows the outline difference is not judgeable at 1x and clear from 3x. |
| Role differentiation (`i_role_diff`) | Owner; **unresolved** | Before scout/medic production; useful earlier (see correction 5) | Chooses the device (reserved accent hue, silhouette attachment, or both). The sample is the scout; an early answer lets the sample carry the device and lets the palette be confirmed once. |
| Palette (`i_palette`) | Owner; **observed** (3 reference colours) | Follows the outline answer | Confirming also adopts the exclusive rule in `q_palette`, which is a derived rule, not a brief statement. Confirm together with the role device. |
| Alpha (`i_alpha`) | Owner; **observed** binary | No; `C.al` can carry the observed value for the sample | Confirming makes `q_canvas` fully specified for production. |
| Sampling (`i_sampling`) | Owner; **proposed** nearest | No | Depends on the engine; nearest preserves the flat look. |
| Engine / importer (`i_engine`) | Owner; **unresolved** | No | Only `q_engine_import` on the family delivery needs it; until then that criterion is unavailable, not failed. |
| Roster, side view (`i_roster`, `i_view`) | Owner; **confirmed** from the brief | Settled | None. |

## Questions for the owner (necessary: 1 and 2)

**1. Outline treatment for the sample and the family.** Which do you want?

- (a) **Outlined**, as `reference.png`: flat 2 px `#25354A` contour that also carries the
  shoulder bar, base bar and solid stalks. Unlocks: `i_outline` confirmed with your
  answer as source; palette can be confirmed as the three reference colours (plus any
  role accent); `q_outline` tests the contour and those interior landmarks.
- (b) **No outline**, as `reference-b.png`: flat teal silhouette with cream eyes. Unlocks
  the same, with the palette as two colours, but the shoulder, base and stalk landmarks
  that the navy carried must be re-authored (a second teal value or a cream accent) or
  dropped deliberately; say which, or let PIXL propose it for the sample.
- (c) **Delegate for the sample only**: PIXL picks one treatment as a recorded proposal,
  you decide after seeing the sample. Unlocks the sample contract now with `i_outline`
  moved to proposed; production still waits for your confirmation.

If your levels are predominantly dark, the sheet favours (b); if they are busy or
mid-value, it favours (a); on light fields either works. Telling us the typical level
backgrounds answers `i_backgrounds` and informs this choice.

**2. Canvas for the sample.** Which do you want?

- (a) **32 x 32**, the references' canvas, carrying a figure about 18 x 25. Unlocks
  `i_canvas` confirmed and `C.px = [32, 32]`.
- (b) **Another size** you name. Note from the study: with a 2 px outline, a materially
  smaller canvas leaves little interior for the scout and medic to differ in; a materially
  larger one makes the 2 px contour read thinner than the references' weight.
- (c) **Delegate for the sample only**: PIXL trials 32 x 32 as a recorded proposal and the
  final canvas stays open, as your brief says. Unlocks the sample contract now with
  `i_canvas` moved to proposed; production still waits for your confirmation.

**Optional, answer now if easy (not blocking):** is the side-view character meant to keep
the references' stalk-and-block body, or are the references a style swatch for a figure
you will let PIXL construct (`i_design_language`)? And how should the scout and medic be
told apart: accent colour, silhouette attachment, or both (`i_role_diff`)?

## Specialist proposal for the trial sample (a proposal, not an owner requirement)

If both answers are "delegate": outlined, 32 x 32, binary alpha, nearest sampling, flat
lighting, three-colour palette, one idle pose facing right (facing direction is a scoped
specialist choice for the sample; the engine can mirror it), body carrying the two-stalk
silhouette and eye placement of the references adapted to profile, with the shoulder
and base bars as the side-view torso landmarks. Rationale: it is the reversible option,
keeps every reference landmark available for role differentiation, and is the treatment
the sheet favours on busy and light fields. This proposal would not confirm any choice.

## Exact next local operation and its prerequisites

Once questions 1 and 2 are answered (or delegated), all of the following is executable
with the local runtime alone (Python 3.11+, Pillow, jsonschema are present; verified by
`readiness`):

1. Save the owner's answer verbatim as a new project source file (e.g.
   `sources/owner-answers-<date>.md`) and add an `S` record for it.
2. Update intake: `i_outline` and `i_canvas` to confirmed (owner answer as source) or to
   proposed (delegated path, alternatives preserved in `wy`); `i_palette` to the
   resulting colour list (confirm only with the role device, or as base + reserved
   accent); `i_backgrounds` if supplied. Do not touch unasked rows.
3. Add `C` `c_sample` with `nm`, `px` (= `i_canvas.vl`), `pl` (= `i_palette.vl`),
   `vw = side`, `sa = nearest`, `al = binary`, `li` (= `i_lighting.vl`) and
   `ch = [i_canvas, i_palette, i_view, i_sampling, i_alpha, i_lighting, i_outline,
   i_design_language]`; set `f_sample.ct = c_sample`. The runtime requires each linked
   choice whose key names a contract field to equal that field's value.
4. On the delegated path, add the sample-specific `q_sample_*` criteria and the corrected
   readability text (correction 4), and swap them into `f_sample.rq`. On the confirmed
   path, apply only the readability correction. Either way this plan change must be
   committed before any candidate is evaluated.
5. Bump to revision 8, `validate --root <consumer root>`, then `commit` against the hash
   published by revision 7. `ready` should then list `t_sample`.

Beyond that, the following are **not** available to the local runtime and were not
attempted here:

- **Request preparation** (`job-prepare`) needs the official PixelLab tool declarations
  (names and input schemas) from the host's authenticated PixelLab MCP connection, which
  this session does not expose. Tool choice depends on them: the sample needs a tool that
  accepts style reference images (both references) with a fixed output size and binary
  alpha; whether a single-image or a character tool is right is decided from the actual
  declarations, not from a cached list.
- **Dispatch, polling, download** need that same connection and are paid operations; a
  dispatch claim is published locally first.
- **Visual review** of the returned candidate needs the display scale (`i_display_scale`)
  to pick the integer zoom, plus a reviewer actually viewing the native and enlarged views.
- **Engine import** (`q_engine_import`) needs `i_engine`; until then it stays unavailable.

## Preserved and unchanged

All earlier reports, evidence files, state history, the two research candidates
(`x_study`, `x_aid`) and their passing verdicts, `handoff` and `handoff_2`, and every
source byte. The 2026-11-14 note remains the record of that session; this note amends its
reading only where the corrections above say so.
