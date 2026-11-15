# Continuation note, 2026-11-15

Cold resume of the scout and medic family project by PIXL (agent), delegated by a
calling agent that reviews this note before consuming it. Resumed from
`state.px/state.px` at revision 6 (canonical hash
`b9a66beff93bcc2197a442d1de8ed6d7d9178aacf0c10606512a38e64d78b5b7`), which validated
cleanly: 57 records, every bound source, candidate and evidence file current
(`files_verified: true`), no families, no provider jobs, no ready tasks. No generation
provider, no official PixelLab tool and no game engine were available in this session,
so nothing was generated and no engine check was possible. No saved choice state, task
state, criterion or verdict was changed by this session. This note was written first and
then bound into the store as a source with a new handoff record (`handoff_3`); the
resulting revision 7 hash is recorded in `SESSION.md` and in the caller's report.

## Outcome in plain terms

The project is still at the point the predecessor left it: both research tasks are done
and accepted; the sample, scout, medic and family tasks are open; nothing has been drawn
or generated. The only thing standing between the project and its first generation
request is two owner answers (outline treatment and canvas size) plus a PixelLab
connection. This session narrowed the predecessor's list of "needed now" decisions from
three to two by reading the runtime's actual readiness rule, re-measured the references
to confirm the retained study, and prepared the exact record changes that the owner's
answer will enable, so the next session can act on the answer with one commit.

## What this session did, by kind of claim

**Measured (local tools, this session).**

- `pixl_asset_check` on `reference.png` (sha256 `d997cade…70aa7`): 32 x 32, 390 visible
  pixels, 3 visible colours, 0 fractional-alpha pixels, 1 opaque component, visible bbox
  x 7..24, y 3..27; every visible pixel is one of `#56B5BC`, `#F4DDA2`, `#25354A`.
- `pixl_asset_check` on `reference-b.png` (sha256 `e76b40ce…14a12a`): identical numbers
  except 2 visible colours; every visible pixel is `#56B5BC` or `#F4DDA2`.
- These agree exactly with the retained study `sources/reference-observations.md`. The
  study's 180-pixel difference count was not re-derived here; it is the predecessor's
  measurement and is carried as such.
- `pixl_validate`: valid, format 2, revision 6, 57 records, files verified.
- `pixl_workflow`: `ready: []`; blockers as listed in the decision table below.

**Visually inspected (this session, own observations).**

- `deliverables/outline-scale-comparison.png` (sha256 `eacc9b66…56270`) was opened and
  viewed at its stored size. My reading: on the light band both treatments read clearly;
  on the dark band the navy contour of the outlined figure merges with the field so the
  figure reads as a smaller teal block with a dark fringe and the two top stalks nearly
  vanish, while the unoutlined figure holds its full silhouette; on the busy band the
  dark contour is what separates the outlined figure from the hatched field, and the
  unoutlined figure's edge softens into it at 1x to 3x. At 1x the two columns are not
  reliably distinguishable to me either. This matches the retained verdict
  `v_aid_useful`; I did not re-record that verdict because the task is done and nothing
  I saw contradicts it.
- `work/reference-views/reference-x12.png` and `reference-b-x12.png` were opened. In the
  outlined view the navy forms the full contour, a bar under the stalks, a bar at the
  base, and fills both stalks solid; in the unoutlined view those are all plain teal and
  the figure reads as one flat shape with two cream eyes. This matches
  `evidence/reference-visual-inspection.md`.

**Documentation-supported (read from the installed kit, this session).**

- `pixl-kit/runtime/pixl/lifecycle.py` lines 53-75 and `resources/spec/PIXL-2.md` line
  31: a raster output plan needs a concrete `C` contract (`F.ct`) before its task can
  activate; choices linked by that contract's `ch` block every phase while `unresolved`
  or `conflict`; `observed`/`proposed` choices block only `production`/`delivery` phase
  tasks, not a `sample` phase task. Production/delivery tasks additionally need an
  evidence-backed decision record (`T.dc`), which is agent work after the sample is
  accepted, not an owner question.
- `runtime/pixl/registry-v2.json`: `C` fields are `nm`, `px` (ints), `pl` (strings),
  `vw`, `sa`, `al`, `li` (str) and optional `ch` (refs to `I`). PIXL-2 line 23: when a
  linked choice's key names a `C` field, the values must be equal.

**Inferred / proposed.** Everything under "Prepared operation" and the recommendation
carried from the predecessor is a proposal, not an owner decision.

## Decision table, carried from saved state (revision 6)

Status is exactly as saved. "Blocks sample now" is derived from the readiness rule
above, not from preference. Nothing in this table changes a saved record.

| Choice (record) | Saved status | Blocks `t_sample` now? | Needed later for | Effect of the answer |
|---|---|---|---|---|
| Outline treatment (`i_outline`) | **conflict** (owner's two references disagree) | **Yes.** A conflict blocks every phase, and `q_outline` and `q_palette` are written against the *confirmed* treatment and palette. | everything downstream | Decides whether `#25354A` is in the output palette; lets `i_palette` move observed → confirmed; makes `q_outline` testable. If "no outline", the shoulder bar, base bar and stalk interiors must be re-authored (second teal value or cream accent) or dropped deliberately, which is a follow-up choice. |
| Canvas size (`i_canvas`) | **unresolved** (owner explicitly deferred) | **Yes.** The contract needs `px`; linking an unresolved choice blocks, and writing `px` without linking it would hide the owner's deferral. | everything downstream | Lets the sample contract be saved. Predecessor's proposal stands: 32 x 32 if the outline is kept (keeps interior area for role differentiation). Owner may accept that or name another size. |
| Design language (`i_design_language`) | **proposed** | No, by the rule: a sample may test a proposal. Yes, in practice, for writing an honest request prompt. | production (must be confirmed) | Owner agrees, amends, or lets the sample test the proposal as written (the sample exists to test it). |
| Game backgrounds (`i_backgrounds`) | **unresolved** | No (not a contract field). | informs the outline answer; makes `q_readability` backgrounds representative | Turns the outline choice from a guess into an informed one; the sheet shows the outline helps on busy mid-value fields and hurts on dark ones. |
| Display scale (`i_display_scale`) | **unresolved** | No. | visual review of the sample (`q_readability`, `q_style_match`) | Sets the integer zoom at which the sample is judged. At 1x the outline difference is not visible; from 3x it is. |
| Role differentiation (`i_role_diff`) | **unresolved** | No (the sample is the scout alone). | `t_scout`/`t_medic` (`q_role_read`) | Chooses the device (reserved accent hue, silhouette attachment, or both). An early answer lets the sample carry it. |
| Palette (`i_palette`) | **observed** `#56B5BC #F4DDA2 #25354A` | No as observed, but its value must equal the contract's `pl`, which depends on the outline answer. | production (must be confirmed) | Confirmed by the outline answer: three colours if outlined, two (plus any re-authoring colour) if not. |
| Alpha (`i_alpha`) | **observed** binary | No. | production (must be confirmed) | Low stakes; confirming it fully specifies `q_canvas`. |
| Sampling (`i_sampling`) | **proposed** nearest | No. | production; depends on engine | Nearest is the proposal that preserves the flat look. |
| Engine / importer (`i_engine`) | **unresolved** | No (not a contract field). | `t_family` (`q_engine_import`) | Without it that criterion stays unavailable, not failed. |
| Roster, side view (`i_roster`, `i_view`) | **confirmed** | No. | — | None. |

Current blockers reported by `pixl_workflow` at revision 6: `t_sample`:
`output_contract: f_sample needs a concrete raster contract`. `t_scout`, `t_medic`:
`t_sample` open, no raster contract, no adoption decision. `t_family`: `t_scout` and
`t_medic` open, no adoption decision.

## The single necessary next owner decision

**Outline treatment (`i_outline`), answered together with the game's predominant level
background.** It is first because it fixes the output palette, bounds the canvas
(keeping the 2 px outline argues for 32 x 32 or larger), and is a conflict between the
owner's own references that no agent should settle. The canvas answer then follows as
"accept the 32 x 32 proposal" or "name a different size"; without either, the sample
stays blocked on `i_canvas` even after the outline is answered.

Question to the owner, as it should be relayed:

> Your two references differ only in the 2 px navy outline (`#25354A`). Keep it (as in
> `reference.png`) or drop it (as in `reference-b.png`)? The comparison sheet
> `deliverables/outline-scale-comparison.png` shows the outline separates the figure on
> busy or mid-value backgrounds but nearly disappears on dark ones, so tell us what your
> levels mostly look like. If you keep it, we propose a 32 x 32 canvas for the sample;
> if you drop it, the shoulder bar, base bar and solid stalks need a replacement colour
> or must go. Please also confirm or correct the 32 x 32 canvas.

The predecessor's conditional recommendation is carried unchanged, as a proposal: keep
the outline and 32 x 32 for the sample if the owner has no preference; prefer no outline
if levels are predominantly dark; keep it if they are busy or mid-value.

## Prepared operation: what the answer enables (proposal, not yet applied)

One commit against the then-current state hash, performed by the next PIXL session once
the owner's answer exists as a file the store can bind (for example a new
`sources/owner-decision-<date>.md`; sources were read-only for this session):

1. Add an `S` record for the owner's answer file (actual sha256, line range, observation
   date).
2. `i_outline`: `st=conflict` → `st=confirmed`, `vl` = the chosen treatment, add the new
   source to `so`, rationale updated to cite the answer.
3. `i_palette`: `st=observed` → `st=confirmed`, `vl` = `["#56B5BC","#F4DDA2","#25354A"]`
   if outlined or `["#56B5BC","#F4DDA2"]` plus any agreed re-authoring colour if not.
4. `i_canvas`: `st=unresolved` → `st=confirmed` with `vl` = the owner's size, or
   `st=proposed` with `vl=[32,32]` only if the owner explicitly accepts testing the
   proposal in the sample.
5. Add the sample contract. Branch A (outline kept, 32 x 32 accepted), wire form:

   `@c_sample:C{al=binary;ch=[@i_canvas,@i_palette,@i_outline,@i_view,@i_sampling,@i_alpha,@i_design_language];li=~N:Flat single-value fills with no ramp, anti-aliasing or dithering, as measured in both references; the 2px #25354A contour also carries the shoulder bar, base bar and stalk fills.;nm=~N:Scout and medic side-view sample contract;pl=[~7:#56B5BC,~7:#F4DDA2,~7:#25354A];px=[32,32];sa=nearest;vw=side}`

   Branch B (outline dropped) is the same with `pl=[~7:#56B5BC,~7:#F4DDA2]` plus the
   agreed landmark colour, and the `li` text describing the replacement device. In
   either branch the `ch` values must equal the contract fields for `px`, `pl`, `vw`,
   `sa`, `al` (PIXL-2 line 23).
6. `f_sample`: add `ct=@c_sample`.
7. Commit with `expect` = the current canonical hash. Expected result: `t_sample` has no
   blockers and appears in `pixl_ready`; `t_scout`/`t_medic` remain blocked on
   `t_sample` and on their adoption decisions, which is correct.

After that, preparing the sample's generation request requires the official PixelLab
tool declaration from the host (`pixl_job_prepare` saves the actual discovered schema).
That was not available in this session.

## Readiness observed in this session

Recorded only what was actually observed here.

- `pixl_readiness` (host `claude`, installation `pixl-kit`): installation present as a
  plugin; bundle manifest verified, 256 files checked, no issues; Python 3.14.3 with
  Pillow 12.3.0, jsonschema 4.26.0, referencing 0.37.0, all importable. The static
  Claude adapters it looks for under the consumer's `.claude/` are absent, which is
  expected because the kit lives at `pixl-kit/` and the specialist role was supplied by
  the harness's `pixl:pixl` skill invocation, which I loaded. The tool reports named
  role and MCP visibility as "not observed" because no host observation was supplied to
  it; that is a limit of the report, not evidence of absence.
- Local PIXL MCP operations actually executed in this session: `pixl_workflow`,
  `pixl_validate`, `pixl_readiness`, `pixl_context` (authoring view), `pixl_asset_check`
  (twice), `pixl_knowledge` (index), and `pixl_commit` for revision 7.
- The bundled runner `pixl-kit/scripts/pixl.py` ran under the selected interpreter
  (`--help`, `decode`, `encode`).
- My available tool inventory in this session contained the local `mcp__pixl-local__*`
  tools and no PixelLab provider tool of any kind. No authentication, dispatch or
  polling was attempted.

## Not done, and why

- No sample contract, no choice-state change: the gating choices are owner decisions
  (`conflict` and explicitly deferred `unresolved`) and the assignment forbids inventing
  them.
- No generation: no provider tool was present.
- No engine import check: no engine is named (`i_engine` unresolved).
- No re-verdict of `x_study` or `x_aid`: both were re-viewed and nothing contradicted
  the retained verdicts, so they stand as the predecessor's records.
- `sources/`, `reference*.png`, existing `deliverables/`, `evidence/`, `work/` files and
  `state.px/history/` were not modified. New files from this session: this note,
  `work/build_rev7.py`, `work/rev7.json`, `work/rev7.px`, the revision 7 state and its
  history copy, and an updated `SESSION.md`.
