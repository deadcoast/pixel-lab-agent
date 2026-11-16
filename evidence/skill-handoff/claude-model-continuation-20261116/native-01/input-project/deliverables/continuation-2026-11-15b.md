# Continuation note, 2026-11-15 (b): correction after caller review

Amends `deliverables/continuation-2026-11-15.md` (retained unchanged; its bytes are bound by
`s_continuation_2`). Everything in that note stands except the point corrected below.
Same session, same isolation: no generation provider, official PixelLab tool, engine or
network was used. No intake status moved, no owner answer invented, no acceptance touched.

## State identity on entry to this correction

- `state.px/state.px`: PX2, revision 7, canonical hash
  `6007ba8338475d50c6ee87af27c7d6766d762890f3b12f9a040d74fa3916b5a5`, 61 records,
  valid, files verified. The caller independently re-validated this, re-hashed every
  pre-existing byte, and confirmed the revision 6 to 7 diff is exactly `handoff_3`,
  `i_animation`, `i_lighting`, `s_continuation_2` and the `project.in` list.

## The discrepancy (caller finding, verified by PIXL against the kit)

The 2026-11-15 note described `C.li` as "a lighting field" and planned
`C.li = i_lighting.vl` with `i_lighting` keyed `li` and linked through `C.ch`. The kit
defines the field more broadly:

- `pixl-kit/runtime/pixl/registry.json` line 30: `C.li` = "lighting and aesthetic intent".
- `pixl-kit/runtime/pixl/store.py` line 233: the intake default for `li` is a whole-intent
  placeholder ("replace with source-grounded project intent before generation").
- `pixl-kit/runtime/pixl/asset-plan.schema.json` lines 77-88 and `plar_prepare.py` line
  290: the plan field that maps to `li` is named `intent`.
- `pixl-kit/runtime/pixl/lifecycle.py` lines 133-138: a linked choice whose key is one of
  the contract field names must encode equal to that field.

Consequence of the old recipe: because `li` is a contract field name, linking `i_lighting`
(key `li`) would have pinned the sample contract's entire intent string to
"flat (no directional light, no shading ramps)", leaving nowhere in the contract for the
aesthetic intent the field exists to carry: the style-swatch design language, the
flat-colour / no-anti-aliasing / blocky construction, and the outline treatment once the
owner chooses it. That was a defect in my next-operation recipe, not a source fact.

## Old to new

| | Old (rev 7 / note 2026-11-15) | New (rev 8 / this note) |
|---|---|---|
| `i_lighting.ky` | `li` (a contract field name; value-pinned to `C.li`) | `lighting` (not a contract field name; linkable in `C.ch` as semantic context without pinning) |
| `i_lighting.vl`, `st`, `so` | `flat (no directional light, no shading ramps)`, observed, `s_refobs` + both references | unchanged |
| `i_lighting.wy` | "...a concrete raster contract requires a lighting field (C.li)..." | Rewritten: the observation supplies the lighting component of `C.li`, which the kit defines as lighting and aesthetic intent; keyed outside the contract field names so the full intent can be composed at contract time. |
| Next-operation step 3 | `li` = `i_lighting.vl` | `li` composed at contract time (recipe below) |
| Correction 2 of the earlier note | "A hidden contract prerequisite was missing (`li`)" | Still true that `li` is required and had no intake backing; the fix is now the lighting observation plus a composition rule, not a one-to-one copy. |

Disposition chosen: (a) rekey, rather than (b) keep `li` and move the aesthetic intent
elsewhere. Reason: `C.li` is the one free-text field in the contract that reaches the
provider translation; it should carry the whole source-grounded intent, and the
lighting observation is one input to it.

## Composition rule for `C.li` at contract time (proposal; written only when the contract is saved)

`C.li` is one string assembled from, in order:

1. the lighting observation (`i_lighting`, observed): flat colour, no directional light,
   no shading ramps;
2. the design-language proposal (`i_design_language`, proposed): no anti-aliasing, binary
   alpha, blocky low-detail construction of the references carried into a genuinely
   side-view figure, references treated as a style swatch (or the owner's override if
   the optional question is answered);
3. the outline treatment as answered or delegated (`i_outline`): outlined as
   `reference.png` with the contour carrying shoulder bar, base bar and solid stalks; or
   no outline as `reference-b.png` with those landmarks re-authored in a named way; or
   the recorded proposal on the delegated path;
4. the identity landmarks the readability criterion will name (see the earlier note's
   correction 4), so the contract record itself carries them.

Each component keeps the authority of its source choice; composing them into one string
does not confirm any of them. All contributing choices are linked through `C.ch`; only
`px`, `pl`, `vw`, `sa`, `al` are value-pinned by the runtime, because only those keys
name contract fields.

## What changed in the store (revision 8)

| Record | Change |
|---|---|
| `i_lighting` | `ky` `li` -> `lighting`; `wy` rewritten as above; value, status and sources unchanged. ID retained; revision 7 bytes remain in `state.px/history/`. |
| `s_continuation_3` | this note, as a local source |
| `handoff_4` | rv 8; focus on this note and the earlier one, the open choices and the two accepted research artifacts; next `t_sample` |
| `project.in` | unchanged membership (no new choice) |

Nothing else: no `C`, no status moves, no criterion edits, no candidate/verdict/evidence
change. Blockers are expected to be identical to revision 7.

## Everything else carried forward unchanged from the 2026-11-15 note

The decision table, the two necessary owner questions (outline treatment; canvas for the
sample) with their alternatives and what each unlocks, the optional questions, the
specialist trial proposal, corrections 1, 3, 4 and 5, and the list of operations that the
local runtime cannot perform (request preparation needs the official PixelLab tool
declarations; dispatch/poll/download need the host's authenticated connection; visual
review needs the display scale; engine import needs the engine).

Amended next-operation step 3 reads: add `C` `c_sample` with `nm`, `px` (= `i_canvas.vl`),
`pl` (= `i_palette.vl`), `vw = side`, `sa = nearest`, `al = binary`, `li` composed per the
rule above, and `ch = [i_canvas, i_palette, i_view, i_sampling, i_alpha, i_lighting,
i_outline, i_design_language]`; set `f_sample.ct = c_sample`. Steps 1, 2, 4 and 5 are
unchanged, except that the revision-8 hash published by this correction is the one the
contract commit must expect.
