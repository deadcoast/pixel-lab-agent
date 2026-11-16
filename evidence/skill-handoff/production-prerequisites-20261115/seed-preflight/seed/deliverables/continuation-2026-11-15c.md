# Continuation note, 2026-11-15 (c): sample contract from the controlled-evaluation answers

Cold resume of the scout and medic family project by PIXL (agent) in an isolated development
evaluation, assigned by a calling agent. No generation provider, official PixelLab tool, game
engine or network was used; nothing was generated, no provider job exists, no candidate,
verdict or evidence was created, no task was marked done, and the two accepted research
candidates (`x_study`, `x_aid`) and their verdicts are untouched. This note applies the recipe
retained in `deliverables/continuation-2026-11-15.md` (steps 1-5) as amended by
`deliverables/continuation-2026-11-15b.md` (step 3, the `C.li` composition rule). Both earlier
notes are preserved unchanged; where this note's reading differs it says so.

## State identity on entry

- `state.px/state.px`: PX2, revision 8, canonical state hash
  `ac9150f4e8ee656761811370867538130faaa111759d61065153df358ef14225`, 63 records, valid, all
  bound files verified (`pixl_validate` and `pixl_workflow`, this session).
- Tasks: `t_study`, `t_aid` done; `t_sample` open with the single blocker
  `output_contract: f_sample needs a concrete raster contract`; `t_scout`, `t_medic`, `t_family`
  open behind it. Ready list empty. No families, no jobs.
- Re-hashed this session and matching their S records: `sources/brief.md`
  (`a78aca77...4cf5324`), `deliverables/continuation-2026-11-15.md` (`d2114fc7...acba5962`),
  `deliverables/continuation-2026-11-15b.md` (`351f2863...e01cad`), and the new input below.

## State identity on exit

- Revision 9, 71 records (63 + `s_eval_answers`, `c_sample`, `q_sample_canvas`,
  `q_sample_palette`, `q_sample_outline`, `q_sample_readability`, `handoff_5`,
  `s_continuation_4`), committed to the store folder `state.px` with expected hash
  `ac9150f4...8ef14225`.
- The revision 9 canonical hash is not written here: this note's own byte digest is bound by
  `s_continuation_4` inside revision 9, so the hash depends on these bytes and cannot be
  embedded without changing it. Read it from `state.px/state.px` (head), the matching copy in
  `state.px/history/<hash>.px`, or the caller return of this session. A pre-commit build of the
  same records against a placeholder note validated as revision 9 with `t_sample` ready and no
  blockers; the committed result was re-read with `pixl_workflow` and `pixl_ready` after the
  commit and is reported in the caller return.
- Expected after commit: ready list `[t_sample]`; `t_sample` blockers `[]`; `t_scout` and
  `t_medic` keep `task_prerequisite: t_sample is open`, `output_contract: f_scout|f_medic needs
  a concrete raster contract`, `task_decision: ... needs an evidence-backed adoption decision`;
  `t_family` keeps its two prerequisite blockers and its decision blocker.

## The new input: what it supplies and what it does not

`sources/controlled-evaluation-answers.md`, sha256
`87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30`, 8 lines, read-only, now
bound as `s_eval_answers` (lines 1-8). Its text, in full, is: simulated answers for this
isolated development evaluation; "explicitly confirmed decisions for the representative
sample": use the outlined treatment shown in `reference.png`; use a 32 x 32 canvas; "These
confirmations apply only to the representative sample within this evaluation. They do not
state real owner preferences, bind family or production policy, or provide human acceptance."

It supplies answers to the two necessary questions of the 2026-11-15 note, for the sample only:

- Q1 outline treatment: outlined as `reference.png` (the earlier note's alternative (a), scoped
  as (c): sample now, production still waits for the owner).
- Q2 canvas: 32 x 32 (alternative (a), scoped the same way).

It does not supply: an owner preference for anything; a family or production policy; human
acceptance of any artifact; answers to the optional questions (design language, role
differentiation, game backgrounds, display scale, animation, engine). Those rows keep their
status. It is a controlled-evaluation input, so it is not added to `project.sc` (the project's
intent sources); it is cited from the choices and criteria it actually scopes.

## How the answers are encoded: `proposed`, not `confirmed`

The runtime (`pixl-kit/runtime/pixl/lifecycle.py`) gates a task only on choices linked through
its outputs' contract (`C.ch`, lines 30-41, 57-64): `unresolved`/`conflict` block any phase;
for production/delivery phases only, lines 72-75 add `choice_unconfirmed` for `observed` or
`proposed` choices. So the sample gate is satisfied by `proposed`, while `confirmed` would also
pre-clear the production-phase gate for `t_scout`/`t_medic` the moment their contracts link
these choices. The input states that it does not bind family or production policy. A status
that would remove the production gate therefore encodes more than the input says.

`proposed` with `s_eval_answers` as a source is the honest encoding: the value is adopted for the
sample trial on a cited authority that is not the owner's, and production still needs the
owner's confirmation. This is exactly the "delegate for the sample only" path (c) of the earlier
note, with the delegate's pick replaced by the evaluation's stated answer. The registry
(`registry-v2.json`) requires a `proposed` choice to carry a rationale and allows sources; both
records carry both. The intake-sample reference's rule applies: an answer adopts only the
choices it explicitly supplies, and a scoped sample confirmation does not become an owner
requirement.

## Decision table

Authority is who decides; status is the saved `I.st`. "Needed now" refers to saving the sample
contract. An answer adopts only the choices it explicitly supplies.

| Choice (record) | Authority / status old -> new | Needed now? | Effect |
|---|---|---|---|
| Outline treatment (`i_outline`) | Owner for the project. **conflict -> proposed**, source `s_eval_answers` (controlled-evaluation sample confirmation, not owner). Value: the `reference.png` alternative; the `reference-b.png` alternative preserved in `wy`. | Yes (was) | Composed into `C.li` component 3; `q_sample_outline` tests it. Production/family still need the owner's answer. |
| Canvas (`i_canvas`) | Owner for the project; explicitly deferred in the brief. **unresolved -> proposed**, value `[32, 32]`, source `s_eval_answers`. | Yes (was) | Pins `C.px = [32, 32]` (key `px` is a contract field). Production still needs the owner's final canvas. |
| Palette (`i_palette`) | Owner. **observed -> observed** (unchanged); `so` gains `s_eval_answers`; `wy` rewritten. Value unchanged: `#56B5BC`, `#F4DDA2`, `#25354A`. | Follows the outline answer | Pins `C.pl` (key `pl`). The outline answer makes `#25354A` part of the sample's working palette; nothing confirms the palette; confirmation stays coupled to `i_role_diff` (correction 5). |
| Side view (`i_view`) | Owner; **confirmed -> confirmed**. Value word `side` unchanged; wire type string -> symbol (below). | Settled | Pins `C.vw`. |
| Sampling (`i_sampling`) | PIXL proposal; **proposed -> proposed**. Value word `nearest` unchanged; wire type string -> symbol. | No | Pins `C.sa`. |
| Alpha (`i_alpha`) | Observed from references; **observed -> observed**. Value word `binary` unchanged; wire type string -> symbol. | No | Pins `C.al`. |
| Lighting (`i_lighting`) | Observed; unchanged (key `lighting`, not a contract field, so not pinned). | No | `C.li` component 1. |
| Design language (`i_design_language`) | PIXL proposal; unchanged. | No (correction 1) | `C.li` component 2 and the construction the landmarks follow. The sample is the trial of this proposal. |
| Game backgrounds (`i_backgrounds`) | Owner; **unresolved**, unchanged. | No | `q_sample_readability` keeps the specialist's light/dark/busy test set until answered. |
| Display scale (`i_display_scale`) | Owner; **unresolved**, unchanged. | Before visual review | Sets the target integer zoom in `q_sample_readability`; the earlier sheet shows the outline difference is not judgeable at 1x. |
| Role differentiation (`i_role_diff`) | Owner; **unresolved**, unchanged. | Before scout/medic production | The sample is the scout without a role device; an accent would reopen the palette. |
| Animation (`i_animation`) | Owner; **unresolved**, unchanged. | Before scout/medic production | Single static sprite remains the planned kind. |
| Engine (`i_engine`) | Owner; **unresolved**, unchanged. | No | `q_engine_import` stays unavailable. |
| Roster (`i_roster`) | Owner; **confirmed**, unchanged. | Settled | None. |

## A representation change the recipe did not anticipate (i_view, i_sampling, i_alpha)

The recipe links `i_view`, `i_sampling` and `i_alpha` through `C.ch`. `lifecycle.py` lines
133-138 require, for a linked choice whose key names a contract field, that
`encode_value(choice.vl) == encode_value(contract[key])`. `C.vw`, `C.sa`, `C.al` are symbol
fields in the registry; the three choices stored their values as strings. `codec.py` lines
213-217 encode a symbol as the bare identifier (`side`) and a string as a length-prefixed
literal (`~4:side`), so the two never compare equal. Demonstrated this session: building the
same records with the string values left in place (`work/build_rev9.py --keep-string-values`,
retained as `work/rev9-strings-diagnostic.json`) fails at encode with
`contract_choice: c_sample.vw does not equal choice i_view`.

Disposition: change the wire type of the three values from string to symbol, nothing else.

| Record | Old wire | New wire | Status, sources, rationale |
|---|---|---|---|
| `i_view` | `vl=~4:side` | `vl=side` | unchanged (confirmed, `s_brief`) |
| `i_sampling` | `vl=~7:nearest` | `vl=nearest` | unchanged (proposed, `s_methods`) |
| `i_alpha` | `vl=~6:binary` | `vl=binary` | unchanged (observed, `s_refobs`) |

This touches three rows the assignment did not ask to change. It changes no status, value word,
source or rationale; it only makes the stored value the type the contract field is declared to
be, which the predecessor could not have been checked against because no contract existed. The
alternative, dropping the three from `C.ch`, would have removed the very gate linkage the
recipe planned. The caller is asked to confirm this disposition; the revision 8 bytes remain in
`state.px/history/ac9150f4...8ef14225.px`.

## Records added or changed in revision 9 (old -> new)

| Record | Kind | Change |
|---|---|---|
| `s_eval_answers` | S (new) | `ur sources/controlled-evaluation-answers.md`, `dg 87cf7eec...52f6e30`, `ln [1, 8]`, `at 2026-11-15`, `au local`. The input file is not copied or rewritten. |
| `i_outline` | I | `st conflict -> proposed`; `vl` two-alternative list -> the first alternative verbatim: `reference.png: flat 2px dark outline #25354A fully enclosing the body, also carrying the shoulder bar, base bar and solid top stalks`; `so` + `s_eval_answers`; `wy` old ("The user states the references disagree here. Measured: ... Retained as a conflict; the bundled edge-rhythm method states contour style is authored intent and must not be resolved mechanically.") -> new text in the section below, which preserves the second alternative. |
| `i_canvas` | I | `st unresolved -> proposed`; `vl null -> [32, 32]`; `so` + `s_eval_answers`; `wy` old ("The user has explicitly not chosen the final canvas size. Both references are 32x32 carrying an 18x25 figure, which is an observation ... This choice blocks every raster output plan.") -> new text below. |
| `i_palette` | I | `st observed` and `vl` unchanged; `so` + `s_eval_answers`; `wy` old ("Measured from the references: teal body, cream eyes, and navy present only in reference.png. Observed, not agreed. Whether #25354A belongs to the output palette depends entirely on the unresolved outline decision, so this cannot be confirmed first.") -> new text below. |
| `i_view`, `i_sampling`, `i_alpha` | I | wire type of `vl` string -> symbol (table above). |
| `c_sample` | C (new) | fields in the next section. |
| `f_sample` | F | `ct` absent -> `@c_sample`; `rq [q_canvas, q_palette, q_outline, q_readability, q_style_match] -> [q_sample_canvas, q_sample_palette, q_sample_outline, q_sample_readability, q_style_match]`. `nm`, `kd`, `tk` unchanged. |
| `q_sample_canvas`, `q_sample_palette`, `q_sample_outline`, `q_sample_readability` | Q (new) | literal text in the criteria section. `wh = actor` (PIXL): these are the specialist's sample-scoped translations of the contract, not owner requirements. |
| `q_canvas`, `q_palette`, `q_outline`, `q_readability` | Q | unchanged; still required by `f_scout` and `f_medic` with their confirmed-policy wording. |
| `s_continuation_4` | S (new) | this note, `ln [1, N]` with its actual line count, `at 2026-11-15`, `au local`. |
| `handoff_5` | N (new) | `rv 9`; `fo` = `s_continuation_4`, `s_eval_answers`, `c_sample`, `i_outline`, `i_canvas`, `i_palette`, `i_backgrounds`, `i_design_language`, `i_lighting`, `i_animation`, `i_display_scale`, `i_role_diff`, `i_engine`, `x_aid`, `x_study`; `nx [t_sample]`; `bl [t_scout, t_medic, t_family]` (`t_sample` is no longer blocked). |
| `project` | P | unchanged (`in` membership unchanged: no new choice; `sc` unchanged: the evaluation input is not a project intent source). |

Not changed: every X, E, V, D (none exist), every T (states, `ca`, `vr`, `dc`), `f_scout`,
`f_medic`, `f_family`, `f_study`, `f_aid`, all earlier S and N records.

### New rationale texts (exact)

`i_outline.wy`:

Status moved conflict -> proposed in revision 9 on the authority of sources/controlled-evaluation-answers.md (s_eval_answers), which confirms the outlined treatment of reference.png for the representative sample only and states that it does not express a real owner preference, bind family or production policy, or provide human acceptance. `proposed` rather than `confirmed`: the project-level choice remains the owner's; a confirmed status would present a sample-scoped evaluation answer as an owner decision and would clear the production-phase unconfirmed gate once a production contract links this choice. The value is the first of the two alternatives retained while this choice was in conflict; the other alternative remains open for the family and for production: 'reference-b.png: no outline, flat teal silhouette with cream eyes only'. Measured context unchanged: the two references differ in exactly 180 pixels, every one #25354A becoming #56B5BC; the outline is load-bearing rather than trim because it also carries the shoulder bar, base bar and stalk interiors; the bundled edge-rhythm method states contour style is authored intent and must not be resolved mechanically. The owner's own answer, informed by deliverables/outline-decision-brief.md, still decides the family treatment.

`i_canvas.wy`:

Status moved unresolved -> proposed in revision 9 on the authority of sources/controlled-evaluation-answers.md (s_eval_answers): 32 x 32 is confirmed for the representative sample only, with the stated limits that it is not a real owner preference, does not bind family or production policy and is not human acceptance. `proposed` rather than `confirmed` because the owner has explicitly not chosen the final canvas size (s_brief) and the input does not change that; a confirmed status would read as the project canvas and would clear the production-phase unconfirmed gate once a production contract links this choice. 32 x 32 is also the measured canvas of both references carrying an 18 x 25 figure (s_refobs), an observation that did not by itself adopt the value. Supplies C.px of the sample contract c_sample. The final canvas for scout/medic production remains the owner's decision.

`i_palette.wy`:

Measured from the references: teal body #56B5BC and cream eyes #F4DDA2 in both, navy #25354A present only in reference.png. Observed, not agreed. Revision 9: the sample-scoped outlined-treatment answer in sources/controlled-evaluation-answers.md (s_eval_answers) brings #25354A into the sample's working palette, so all three measured colours supply C.pl of c_sample; the status stays observed because no owner instruction has adopted these exact values as the project palette and the answer binds the sample only. Confirmation for production remains coupled to the unresolved role-differentiation device (i_role_diff), which may need a reserved accent; the exclusive membership rule in q_palette is a derived rule, not a brief statement.

## The sample contract `c_sample` (exact)

- `nm`: Representative sample: side-view scout, single idle pose, 32 x 32, outlined as reference.png; sample-scoped contract from the controlled-evaluation answers, not a family or production contract
- `px`: `[32, 32]` (pinned to `i_canvas`, proposed)
- `pl`: `["#56B5BC", "#F4DDA2", "#25354A"]` (pinned to `i_palette`, observed)
- `vw`: `side` (pinned to `i_view`, confirmed)
- `sa`: `nearest` (pinned to `i_sampling`, proposed)
- `al`: `binary` (pinned to `i_alpha`, observed)
- `ch`: `[i_canvas, i_palette, i_view, i_sampling, i_alpha, i_lighting, i_outline, i_design_language]`
- `li` (one string, composed per the 2026-11-15b rule; each component labelled with its own authority inside the string):

[1 lighting; observed from reference.png and reference-b.png (i_lighting, s_refobs)] Flat colour: no directional light, no shading ramps. [2 design language; PIXL proposal awaiting owner agreement (i_design_language)] Carry the references' flat colour, absent anti-aliasing, binary alpha and blocky low-detail construction into a genuinely side-view figure; the references' front-facing symmetric shape is a style swatch, not the character design. [3 outline; controlled-evaluation sample confirmation (i_outline, sources/controlled-evaluation-answers.md): sample only, not an owner preference, not family or production policy] Outlined as reference.png: a flat #25354A contour at the weight shown there (2 logical px) fully enclosing the figure and also carrying the shoulder bar, base bar and solid top stalks, adapted to the side view; the no-outline treatment of reference-b.png stays open for the family. [4 identity landmarks for the readability criterion; PIXL construction proposal under component 2, not an owner requirement] (a) two top stalks separated by a notch, solid in the contour colour; (b) cream eye placement adapted to profile so the figure has an unambiguous facing direction; (c) the navy shoulder bar; (d) the navy base bar; (e) the enclosing navy contour separating the figure from the background. The single idle pose faces right, a scoped specialist choice for the sample that the engine can mirror.

Identity landmarks named, with authority: (a) two notched top stalks, (b) cream eye placement
indicating facing direction, (c) navy shoulder bar, (d) navy base bar, (e) enclosing navy
contour. Landmarks (a)-(e) are measured features of `reference.png` (`s_refobs`, lines 25-40);
naming them as the side-view figure's identity landmarks is PIXL's construction proposal under
the design-language proposal, which the owner can override (then the landmarks follow the
owner's construction). The "2 logical px" weight is the measured weight of the treatment the
input names, carried unchanged because the sample canvas equals the references' canvas. The
facing direction is a specialist sample choice. Component 1 is observed; component 2 is
proposed; component 3 is the controlled-evaluation sample confirmation. Composing them into
one string confirms none of them.

## Criteria of `f_sample.rq` after the change (exact literal text)

The original `q_canvas`, `q_palette`, `q_outline` are worded against the **confirmed** canvas,
palette and outline treatment. Revision 9 confirms none of these (see the status choice above),
so for the sample those three are unsatisfiable: correction 4 of the 2026-11-15 note applies on
this path. `q_readability` named "head, torso and limb" landmarks the references do not have.
Each change below names its justification. `wh = actor` on the four new criteria: they are
PIXL's sample-scoped translations; the owner's criteria stay on `f_scout`/`f_medic`.

1. `q_sample_canvas` (replaces `q_canvas` for the sample; mechanical / local; sources
   `s_eval_answers`, `s_refobs`). Old: "The candidate file matches the confirmed canvas size
   exactly and contains zero fractional-alpha pixels under the confirmed alpha policy." New:

   The candidate file is exactly 32 x 32 pixels, the canvas of the sample contract c_sample, and contains zero fractional-alpha pixels under that contract's binary alpha. Scope: the representative sample only; the canvas is a sample-scoped controlled-evaluation confirmation and the alpha policy an observation from the references, neither a confirmed project policy.

   Why: `s_eval_answers` line 6 supplies 32 x 32 for the sample only; `i_alpha` is observed
   (`s_refobs` line 23); "confirmed" would be false for both.

2. `q_sample_palette` (replaces `q_palette`; mechanical / local; sources `s_refobs`,
   `s_eval_answers`). Old: "Every visible pixel of the candidate is a member of the confirmed
   project palette, with no colours outside it." New:

   Every visible pixel of the candidate is one of the three colours of the sample contract c_sample palette, #56B5BC, #F4DDA2 and #25354A, with no colours outside it. Scope: the representative sample only; these are the colours measured in the references, all three admitted by the sample-scoped outlined-treatment confirmation, and exclusivity is a sample working rule that a later role accent may reopen; this is not a confirmed project palette.

   Why: the colours are measured (`s_refobs` lines 24, 34); `#25354A` is admitted for the
   sample by `s_eval_answers` line 5; exclusivity is kept as a scoped sample rule because the
   sample is the style proof in the reference colours and carries no role device (correction 5
   keeps the production palette open).

3. `q_sample_outline` (replaces `q_outline`; visual / visual; sources `s_eval_answers`,
   `s_ref_a`, `s_refobs`). Old: "The candidate applies the confirmed outline treatment
   consistently on every contour and on the interior landmarks that treatment is responsible
   for, inspected at native scale and at integer zoom." New:

   Inspected at native scale and at integer zoom, the candidate applies the outlined treatment of the sample contract c_sample, the treatment shown in reference.png: a flat #25354A contour at the weight shown there (2 logical px) fully enclosing the figure, applied consistently on every contour and also carrying the interior landmarks that treatment is responsible for (shoulder bar, base bar, solid top stalks) adapted to the side view. Scope: the representative sample only, under the sample-scoped controlled-evaluation confirmation; not a confirmed family treatment.

   Why: `s_eval_answers` line 5 names the treatment "shown in reference.png"; what is shown is
   measured in `s_refobs` lines 37-40 (flat 2-logical-pixel navy contour, shoulder and base
   bars, solid stalks). The interior landmarks are named rather than left implicit so the
   check is observable.

4. `q_sample_readability` (replaces `q_readability`; visual / visual; sources `s_methods`,
   `s_refobs`, `s_continuation_2`). Old: "At native scale on light, dark and busy backgrounds
   the figure reads as a side-view character with an unambiguous facing direction and
   separable head, torso and limb landmarks." New:

   At native scale and at the target integer zoom, on light, dark and busy test backgrounds, the figure reads as a side-view character with an unambiguous facing direction, and the identity landmarks named in the sample contract c_sample (two notched top stalks, cream eye placement, navy shoulder bar, navy base bar, enclosing navy contour) remain separable. The target integer zoom requires i_display_scale before review; the three test backgrounds are the specialist's test set until i_backgrounds is answered.

   Why: the silhouette-readability method (`s_methods` lines 15-16) requires *named* identity
   landmarks; the references have no head/torso split and no limbs (`s_refobs` lines 25-28,
   45-50); correction 4 of `s_continuation_2` proposed this wording. Delta from that proposed
   wording: the landmark list is copied in parentheses from `c_sample.li` so the check is
   self-contained, and the two review prerequisites are stated in the check itself.

5. `q_style_match` (unchanged, still owner-owned, visual / visual, source `s_refobs`):

   Viewed beside reference.png and reference-b.png at equal integer zoom, the candidate reads as the same art style in colour, detail density and edge language.

Not added: no facing-direction, pose or role gate for the sample. `f_sample.nm` already states
a single idle pose; the role device is out of sample scope (`i_role_diff` unresolved).

## What remains unavailable to the local runtime (unchanged from the earlier notes)

- **Request preparation** (`job-prepare` / `pixl_job_prepare`) needs the official PixelLab
  tool declarations (names and input schemas) from the host's authenticated PixelLab MCP
  connection. Tool choice is decided from the actual declarations: the sample needs an
  operation that accepts style reference images (both references) with a fixed 32 x 32 output
  and binary alpha; whether a single-image or a character operation fits is read from the
  schema, not a cached list.
- **Dispatch, polling, download** need that same connection and are paid operations; a local
  dispatch claim is published first.
- **Visual review** of a returned candidate needs `i_display_scale` for the integer zoom in
  `q_sample_readability` and `q_sample_outline`, plus a reviewer actually viewing native and
  enlarged views (`pixl_inspection_prepare` / `pixl_inspection_review`).
- **Engine import** (`q_engine_import`, on the family delivery) needs `i_engine`; until then it
  stays unavailable, not failed.

## Concrete next operation and its remaining inputs

`t_sample` is ready. Next: prepare the sample request against `c_sample` and `f_sample`.

1. Host supplies the official PixelLab MCP tool list and the exact input schema of the chosen
   operation (discovery evidence) and the existing authorization/limits.
2. PIXL translates `c_sample` into that schema (references as actual image inputs, 32 x 32,
   binary alpha, the `li` intent with its authority labels reduced to provider wording), saves
   a `request-review.json` for the caller comparison per the request-review reference, and
   saves the durable request with `pixl_job_prepare` (task `t_sample`, output `f_sample`).
3. Caller compares request and criteria against the sources; only then dispatch.

Remaining inputs for later steps, not needed to prepare: `i_display_scale` (review zoom),
`i_backgrounds` (representative review backgrounds), and for production the owner's answers to
outline, canvas, role differentiation and animation, plus an evidence-backed decision record
`D` for `t_scout`/`t_medic`.

## Preserved and unchanged

All earlier reports, evidence files, state history copies, `work/` builders and candidates for
revisions 2-8, the research candidates `x_study` and `x_aid` with their passing verdicts,
`handoff` through `handoff_4`, every source byte, and the files `CALLER-RESULT.json`,
`review/*`, `evidence/*`. New files this session: this note, `work/build_rev9.py`,
`work/verify_rev9.py`, `work/rev9.json`, `work/rev9.px`, `work/rev9-texts.json`,
`work/rev9-strings-diagnostic.json`, the new head and its history copy.
