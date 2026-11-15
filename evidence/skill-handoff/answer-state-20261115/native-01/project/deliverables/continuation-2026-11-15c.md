# Continuation note, 2026-11-15 (c): sample contract from the controlled-evaluation answers

Cold resume by PIXL (agent) in an isolated development evaluation, assigned by a calling
agent. Nothing from the caller's conversation was inherited. No generation provider,
official PixelLab tool, game engine or network was used: nothing was generated, no
provider job exists, no candidate sprite exists, and no acceptance verdict was written.
The earlier notes (`deliverables/continuation-2026-11-14.md`, `-15.md`, `-15b.md`) and the
decision brief are preserved unchanged; this note applies their recipe and records the
result. Historical acceptance (`x_study`, `x_aid`, their verdicts and evidence) is untouched.

## State identity

- **Entry:** `state.px/state.px`, PX2 format 2, revision 8, 63 records, canonical state
  hash `ac9150f4e8ee656761811370867538130faaa111759d61065153df358ef14225`, valid, all bound
  files verified (`pixl_validate`, `pixl_workflow`, `pixl_ready` re-run in this session;
  ready list empty; `t_sample` blocked only by `output_contract: f_sample needs a concrete
  raster contract`).
- **Exit:** revision 9, 71 records (63 + 8 new; no record deleted). The exit canonical
  hash is published by the commit and is the file name of the new copy under
  `state.px/history/<hash>.px`; it is also stated in the return message. It cannot be
  written inside this note, because this note's own bytes are bound by `s_continuation_4`
  and are therefore an input to that hash.

## The new input and the authority it carries

`sources/controlled-evaluation-answers.md`, sha256
`52f68a3242dd72ab0d2bd8315c605160f5e6b76b626164f28a949d1563f30f94`, 5 lines, retained as
`s_eval_answers` (`au local`, `at 2026-11-15`). Its operative sentence: "For the
representative sample, use the outlined treatment shown in reference.png and a 32 x 32
canvas." Its own authority statement: "simulated answers for this isolated development
evaluation, not real owner preferences or human acceptance."

Three facts fix how far it reaches:

1. It answers the two necessary questions of the 2026-11-15 note: Q1 (outline) = the
   outlined treatment of `reference.png`; Q2 (canvas) = 32 x 32.
2. It is scoped "for the representative sample". The brief (`s_brief`) still says the final
   canvas size is not chosen, and the input does not claim to change that.
3. It declares itself simulated: not an owner preference, not human acceptance.

Applied status: **the delegated-trial path (option (c) of both questions)**, with this file
rather than a PIXL pick as the source of the trial values. Both choices move to
**proposed**, not confirmed. Reasons:

- `confirmed` in this store means the owner's adopted project choice (every confirmed
  record, `i_roster` and `i_view`, cites the owner's brief). A source that states it is not
  an owner preference cannot honestly supply that status; recording it as confirmed would
  launder a simulated answer into owner authority.
- The runtime's gates make `proposed` sufficient for exactly the scope the input claims
  and insufficient for the scope it disclaims. `lifecycle.py` blocks a task only on
  `unresolved`/`conflict` choices linked through its output contract (`C.ch`); for the
  production and delivery phases it additionally requires every linked choice to be
  `confirmed` and the task to carry a decision record `D`. So `proposed` unblocks
  `t_sample` and leaves `t_scout`, `t_medic`, `t_family` gated on the real owner, which is
  the honest reading of "for the representative sample".
- `observed` would be wrong: nothing was measured; a selection was made.

Nothing the input does not supply was confirmed. Unasked rows keep their status:
`i_backgrounds`, `i_display_scale`, `i_role_diff`, `i_animation`, `i_engine` unresolved;
`i_design_language`, `i_sampling` proposed; `i_lighting`, `i_alpha` observed; `i_roster`,
`i_view` confirmed. (Three of these have a value-representation fix with no status change;
see correction 6.)

## Old to new, every changed or added record

| Record | Old (rev 8) | New (rev 9) | Source / why |
|---|---|---|---|
| `s_eval_answers` (S) | absent | `sources/controlled-evaluation-answers.md`, dg `52f68a32...0f94`, ln 1-5, au local, at 2026-11-15 | Retains the input verbatim as a project source. |
| `s_continuation_4` (S) | absent | this note, au local, at 2026-11-15 | Retains this continuation. |
| `project.sc` | 5 sources (brief, refobs, methods, ref_a, ref_b) | + `s_eval_answers` | The input carries decision content for the sample; listing it makes it discoverable from the project record. `project.in` unchanged (no new choice). |
| `i_outline` | `conflict`; `vl` = two alternatives; `so` brief, refobs, ref_a, ref_b | **`proposed`**; `vl` = "outlined as reference.png: flat #25354A contour of the references' weight (2 px measured) fully enclosing the body, with the same navy forming the shoulder bar, base bar and solid top stalks"; `so` + `s_eval_answers`; `wy` rewritten, both alternatives preserved in it with the no-outline consequences (two-colour palette; shoulder, base and stalk landmarks re-authored or dropped) | Q1 answered for the sample only by a self-declared simulated source. `wh` stays `user`: the decision remains the owner's. |
| `i_canvas` | `unresolved`; `vl` null; `so` brief, refobs | **`proposed`**; `vl` = `[32, 32]`; `so` + `s_eval_answers`; `wy` rewritten: adopted for the sample, final canvas still not chosen per the brief, 18x25 figure observation and the smaller/larger-canvas consequences preserved | Q2 answered for the sample only. Lets `C.px` be written. |
| `i_palette` | `observed`; `vl` `["#56B5BC","#F4DDA2","#25354A"]`; `so` refobs, ref_a, ref_b | **`observed` (unchanged status and value)**; `so` + `s_eval_answers`; `wy` rewritten | The three colours remain measurements; the sample outline answer settles only that navy is present in the sample, so `c_sample.pl` adopts exactly these three without proposing or confirming a project palette. Not confirmed, deliberately (correction 5): confirmation would adopt the exclusive membership rule for production while the role device (`i_role_diff`) may need an accent hue. Confirm the palette only with the role device, or as base + one reserved accent slot. |
| `i_view.vl` | string `"side"` | symbol `side`; status `confirmed`, `so`, `wh`, `wy` unchanged | Correction 6 (representation only). |
| `i_sampling.vl` | string `"nearest"` | symbol `nearest`; status `proposed`, `so`, `wh`, `wy` unchanged | Correction 6 (representation only). |
| `i_alpha.vl` | string `"binary"` | symbol `binary`; status `observed`, `so`, `wh`, `wy` unchanged | Correction 6 (representation only). |
| `c_sample` (C) | absent | see "Sample contract" below | The contract the recipe's step 3 describes. Instantiates proposed and observed choices; confirms none. |
| `f_sample.ct` | absent | `c_sample` | Removes the `output_contract` blocker. |
| `f_sample.rq` | `q_canvas, q_palette, q_outline, q_readability, q_style_match` | `q_sample_canvas, q_sample_palette, q_sample_outline, q_sample_readability, q_style_match` | Correction 4, delegated path (below). |
| `q_sample_canvas` (Q) | absent | mechanical / local; see text below; `wh actor`; `so s_eval_answers, s_refobs` | Sample-scoped replacement for `q_canvas`. |
| `q_sample_palette` (Q) | absent | mechanical / local; `wh actor`; `so s_eval_answers, s_refobs` | Sample-scoped replacement for `q_palette`. |
| `q_sample_outline` (Q) | absent | visual / visual; `wh actor`; `so s_eval_answers, s_refobs, s_ref_a` | Sample-scoped replacement for `q_outline`. |
| `q_sample_readability` (Q) | absent | visual / visual; `wh actor`; `so s_methods, s_refobs, s_brief` | Corrected readability text (correction 4). |
| `handoff_5` (N) | absent | `rv 9`; focus on this note, the input, `c_sample`, `f_sample`, the changed and still-open choices, `x_aid`, `x_study`; `nx t_sample`; `bl t_scout, t_medic, t_family` | Resumption pointer. `t_sample` is no longer listed as blocked. |

Unchanged: `q_canvas`, `q_palette`, `q_outline`, `q_readability`, `q_style_match` (still
referenced by `f_scout` and `f_medic` with their confirmed wording); every T, X, V, E
record; `handoff` through `handoff_4`; every earlier S; all other I records
(`i_roster`, `i_design_language`, `i_lighting`, `i_backgrounds`, `i_display_scale`,
`i_role_diff`, `i_animation`, `i_engine`).

## Correction 6 (found this session): symbol-valued choices

The runtime pins a linked choice whose key is a contract field name by comparing the wire
encodings of the choice value and the contract field (`lifecycle.py` lines 133-138, via
`codec.encode_value`). `C.vw`, `C.sa` and `C.al` are symbols on the wire (`side`), while the
retained `i_view`, `i_sampling` and `i_alpha` values were stored as strings (`~4:side`). The
two encodings are unequal, so the retained recipe's `ch` list would have failed validation
("c_sample.vw does not equal choice i_view") on the first contract that linked them.
Resolution: re-encode those three values as symbols, the form the state-authority rule
asks for ("use symbols and references as tagged values"). Meaning, status, sources,
responsible actor and rationale are unchanged; no evidence receipt binds these three
records (checked: the four E records bind only `f_*`, `q_*`, `s_*`, `user`, `x_*`), so no
acceptance binding changes. Alternative rejected: leaving them out of `C.ch`, which would
also remove the production-phase `choice_unconfirmed` gate on sampling and alpha.

## Sample contract `c_sample`

- `nm`: Representative sample contract: side-view scout, single idle pose, 32 x 32,
  outlined as reference.png (sample-scoped; adopts proposed and observed choices, confirms
  none)
- `px`: `[32, 32]` (pinned by the runtime to `i_canvas.vl`)
- `pl`: `["#56B5BC", "#F4DDA2", "#25354A"]` (pinned to `i_palette.vl`)
- `vw`: `side` (pinned to `i_view`), `sa`: `nearest` (pinned to `i_sampling`), `al`:
  `binary` (pinned to `i_alpha`)
- `ch`: `i_canvas, i_palette, i_view, i_sampling, i_alpha, i_lighting, i_outline,
  i_design_language` (the last three are keyed `lighting`, `edge_treatment`,
  `design_language`, none a contract field name, so they are linked as semantic context
  and not value-pinned)
- `li` (one string, composed per the 2026-11-15b rule: lighting observation, design-language
  proposal, outline answer with its landmarks, identity landmarks for the readability
  criterion, plus the scoped pose choice), verbatim:

> Lighting (observed from both references): flat colour, no directional light, no shading
> ramps. Design language (proposed, owner may override): no anti-aliasing, binary alpha and
> the blocky low-detail construction of the references carried into a genuinely side-view
> figure; the references' front-facing symmetric shape is a style swatch, not the character
> design. Outline (adopted for the sample from the controlled-evaluation answers, not an
> owner confirmation): outlined as reference.png, a flat #25354A contour of the references'
> weight (2 px measured) fully enclosing the body, with the same navy forming the shoulder
> bar, the base bar and the solid top stalks. Identity landmarks that the sample readability
> criterion names and that must stay separable in profile: the solid navy top-stalk
> silhouette (the references' two stalks adapted to side view), at least one cream eye, the
> navy shoulder bar and the navy base bar. Pose (scoped specialist choice for the sample):
> one idle pose facing right; the engine can mirror it.

Each clause keeps the authority of its source choice; composing them does not confirm any.
The facing direction is a specialist choice scoped to the sample, as the 2026-11-15 note
proposed; it is carried in `li` only so the provider translation and the reviewer use the
same direction.

## Criterion changes (correction 4, delegated path)

Because `i_outline`, `i_canvas` are proposed and `i_palette` is observed, the three
criteria worded against "the confirmed ..." would be unsatisfiable for the sample. New Q
records were added and `f_sample.rq` re-pointed; the old records are untouched and still
serve `f_scout` and `f_medic`.

| Old (kept for production outputs) | New (sample output only) | Check text (new) |
|---|---|---|
| `q_canvas`: "...matches the confirmed canvas size exactly ... under the confirmed alpha policy." | `q_sample_canvas` "sample canvas and alpha" (mechanical, local) | The candidate file is exactly 32 x 32 pixels, the canvas of the sample contract c_sample (adopted for the sample from sources/controlled-evaluation-answers.md; not a confirmed final canvas), and contains zero fractional-alpha pixels under that contract's binary alpha policy. |
| `q_palette`: "...member of the confirmed project palette, with no colours outside it." | `q_sample_palette` "sample palette membership" (mechanical, local) | Every visible pixel of the candidate is one of the three colours of the sample contract c_sample, #56B5BC, #F4DDA2 and #25354A (the measured reference palette, adopted for the sample because the sample outline treatment includes the navy), with no colours outside them. This exclusivity is a sample-scoped derived rule; it does not confirm the project palette, which stays coupled to the role-differentiation device. |
| `q_outline`: "...applies the confirmed outline treatment consistently on every contour and on the interior landmarks that treatment is responsible for..." | `q_sample_outline` "sample outline treatment applied" (visual, visual) | The candidate applies the outlined treatment named in the sample contract c_sample, that of reference.png: a flat #25354A contour of the references' weight (2 px measured) fully encloses the body on every exterior contour, and the same navy forms the interior landmarks that treatment is responsible for (the shoulder bar, the base bar and the solid top stalks), inspected at native scale and at integer zoom. |
| `q_readability`: "At native scale on light, dark and busy backgrounds ... unambiguous facing direction and separable head, torso and limb landmarks." | `q_sample_readability` "sample side-view readability" (visual, visual) | At native scale and at the target integer zoom, on light, dark and busy test backgrounds, the figure reads as a side-view character with an unambiguous facing direction, and the identity landmarks named in the sample contract c_sample (the solid navy top-stalk silhouette, at least one cream eye, the navy shoulder bar and the navy base bar) remain separable. The target integer zoom comes from i_display_scale; until it is supplied, the review states the zooms actually used. |
| `q_style_match` | unchanged, still in `f_sample.rq` | Reading note: with the outlined treatment adopted for the sample, "edge language" is judged against `reference.png`; `reference-b.png` stays in the side-by-side for colour and detail density. Its text did not need to change. |

`wh` of the four new criteria is `actor` (PIXL): they are derived against a proposed
contract under a scoped evaluation input, not owner-stated acceptance. The production
criteria keep `wh user`. Note for later: `q_readability` (head/torso/limb wording) still
sits on `f_scout` and `f_medic`; it should receive the same correction when those outputs
get their contracts, which is the owner's production decision, not this sample's.

## What `pixl_ready` lists after the commit

`t_sample` ("Prove one representative side-view figure before family production"), with no
blockers: its prerequisite `t_study` is done, `f_sample` now has a contract, and no choice
linked through `c_sample.ch` is unresolved or in conflict. Verified on the encoded
revision-9 candidate before the commit and again on the committed head (results in the
return message). `t_scout` and `t_medic` keep `task_prerequisite: t_sample`,
`output_contract` and `task_decision`; `t_family` keeps its three. If a future reader sees
`choice_unconfirmed` on `t_scout`/`t_medic` after they get contracts, that is the intended
gate: the sample answers were never owner confirmation.

## Exact next operation and its prerequisites

**Executable locally now (none performed here):** nothing further changes the plan;
`t_sample` is ready for its provider request. Preparing that request through the durable
`job-prepare` operation is local, but its inputs are not available in this session.

**Needs the host's authenticated PixelLab MCP connection (not exposed here):**

1. Discover the actual PixelLab tool declarations (names, input schemas). The sample needs
   a tool that accepts both references as style inputs, fixes the output at 32 x 32, and
   returns binary-alpha output (or output that can be thresholded and checked by
   `q_sample_canvas`); whether a single-image or character tool fits is decided from the
   actual declarations, not from a cached list.
2. `job-prepare` against `t_sample` / `f_sample`, translating `c_sample` (px, pl, al, li
   including the landmarks and facing direction) and saving the exact schema, request,
   discovery and authorization evidence.
3. `job-dispatch` (publishes the single dispatch claim), then the one authorized host call,
   `job-observe` with the returned identifiers, download, and `job-import` of the bytes as
   the first X candidate for `f_sample`. Paid operation; authorization must be stated by
   the caller.

**Needs the owner (or, in this evaluation, a further scoped input):**

- `i_display_scale`: the target integer zoom for `q_sample_readability` and `q_style_match`.
  Alternatives: a named integer zoom; or "review at the zooms PIXL chooses and state them",
  which the criterion text already permits. The sheet showed the outline difference is not
  judgeable at 1x and clear from 3x.
- `i_engine`: only `q_engine_import` on `f_family` needs it; it stays unavailable until then.
- Before `t_scout`/`t_medic`: the owner's confirmation of outline, canvas, palette (with
  the role device, `i_role_diff`), lighting, alpha and sampling, plus `i_animation`, plus a
  decision record `D` per task. The sample answers do not supply any of these.
- Helpful, not blocking: `i_backgrounds`, so the readability review uses the game's fields
  instead of the agent's light/dark/busy set.

## Preserved and unchanged

All earlier reports, evidence files, state history, both research candidates and their
passing verdicts, `handoff` through `handoff_4`, every earlier source byte, and the
production criteria. The read-only inputs (`pixl-kit/`, `sources/`, both references,
`CALLER-RESULT.json`, `review/*`, earlier continuation notes) were not modified. Scratch
for this revision: `work/build_rev9.py`, `work/rev9.json`, `work/rev9.px`,
`work/_decoded_rev8_readonly.json` (the decoded entry state).
