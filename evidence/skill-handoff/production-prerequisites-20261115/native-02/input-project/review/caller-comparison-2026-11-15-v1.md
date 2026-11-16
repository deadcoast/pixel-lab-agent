# Caller comparison, version 1 (2026-11-15)

Reviewer: the calling agent (not PIXL). Scope: the first return of the native PIXL
specialist (agent ID `a7f9957f93675cbf8`), i.e. store revision 7 (canonical hash
`6007ba8338475d50c6ee87af27c7d6766d762890f3b12f9a040d74fa3916b5a5`) and
`deliverables/continuation-2026-11-15.md` (sha256
`d2114fc7be4337a55e5da8b2f0b19bc80c9b4445de0ae42eb302bab0acba5962`).
This version is retained unchanged; a later version binds the final state.

## Inputs I read myself

- `sources/brief.md` (a78aca77…5324), `sources/reference-observations.md`
  (d0862d14…0495), `sources/method-research.md` (1b1503b7…4e51),
  `deliverables/outline-decision-brief.md` (32b59ab7…78e2),
  `deliverables/continuation-2026-11-14.md` (d9755b26…d8e9),
  `evidence/reference-visual-inspection.md` (438b0ea0…cb69), `SESSION.md`.
- `deliverables/outline-scale-comparison.png` viewed as an image.
- `state.px/state.px` before delegation: rev 6, hash b9a66bef…b5b7, 57 records,
  valid, files verified, ready list empty.
- Kit runtime: `pixl-kit/runtime/pixl/lifecycle.py`, `registry-v2.json`,
  `registry.json`, `store.py`, `asset-plan.schema.json`; `pixl-kit/agents/pixl.md`;
  `pixl-kit/skills/pixl/references/delegation.md`.

## Mechanical verification of the return

| Check | Result |
|---|---|
| `pixl_validate` head after return | valid, format 2, rev 7, hash 6007ba83…b5a5, 61 records, files verified |
| `pixl_ready` | empty (unchanged) |
| History | rev-6 file `b9a66bef…b5b7.px` retained; rev-7 copy present and byte-identical to head |
| Pre-existing bytes | all sources, references, deliverables, evidence, SESSION.md and older history re-hashed: unchanged |
| `diff` rev 6 vs rev 7 | adds exactly `handoff_3`, `i_animation`, `i_lighting`, `s_continuation_2`; `project.in` gains the two choices; nothing else |
| Returned paths | all inside the consumer root; reported hashes match actual bytes |

## Claim-by-claim comparison

| Claim or clause | Source and locator | Authority / status | Change authorized | Prerequisite | Finding and disposition |
|---|---|---|---|---|---|
| Sample is blocked only by the missing raster contract | lifecycle.py:53-56 | runtime | none | `f_sample.ct` | Consistent. Verified in code and in `pixl_workflow`. |
| Only contract-linked choices in unresolved/conflict gate `t_sample`; observed/proposed acceptable for the sample phase | lifecycle.py:30-41, 57-64, 65-75 (`ADOPTION_PHASES = {production, delivery}`) | runtime | none | `C.ch` | Consistent. Correction 1 and 3 of the 11-15 note (design language not a blocker; 11-14 note overstated confirmation needs) are supported by the code and by delegation.md:102-105 ("scoped expert proposals can support an authorized sample"). |
| Production/delivery need confirmed choices and a `D` record | lifecycle.py:65-75 | runtime | none | `t_scout.dc` etc. | Consistent. |
| Linked choice with a contract-field key must equal that field | lifecycle.py:131-138 | runtime | none | contract authoring | Consistent, and it is what exposes the discrepancy below. |
| `i_animation` unresolved, sources brief + study | brief.md:31; reference-observations.md:73 | owner; unresolved | add record only | none | Consistent. Both sources name the gap. No status invented. |
| `i_lighting` observed "flat (no directional light, no shading ramps)" | reference-observations.md:16, 24, 29, 40 (3 flat colours, no ramp, no AA/dither); decision-brief.md | owner; observed from references | add record only | none | Content supported as an observation. Not a confirmed output policy; the note says so. |
| "C requires li, a lighting field" and plan `C.li = i_lighting.vl` with key `li` in `C.ch` | registry-v2.json:10 and registry.json:30 define `li` = "lighting **and aesthetic intent**"; store.py:233 default "replace with source-grounded project intent"; asset-plan.schema.json:77-88 names the field `intent`; lifecycle.py:133-138 equality rule | kit field semantics | plan recipe only | contract authoring | **Discrepancy.** Keying the intake choice `li` would force the sample contract's whole intent string to the lighting-only value, narrowing a kit-defined field. Sent to the specialist for a corrected proposal (rename key, or state where the aesthetic intent lives). |
| Criteria `q_canvas`/`q_palette`/`q_outline` are worded against *confirmed* values | state.px Q records; lifecycle has no notion of "confirmed" inside `ck` text | prior agent authoring under owner authority | none now; deferred to the contract commit | owner answer path | Reasonable: on a delegated-trial path the literal wording is unsatisfiable. Deferral is acceptable; it must be an explicit old-to-new change when applied (delegation.md:25-35). |
| `q_readability` presumes head/torso/limb landmarks | method-research.md:15-16 ("named identity landmarks"); reference-observations.md:24-28, 66-69 (single block, stalks, eyes; no limbs) | prior agent assumption | none now; deferred | design-language answer | Supported. The replacement text keeps the required outcome (facing direction, separable landmarks, light/dark/busy backgrounds) and adds the method's "target scale" input. |
| Palette confirmation coupled to role device (`q_palette` exclusive) | state.px `q_palette.ck`; `i_role_diff` unresolved | derived rule, not brief | none | none | Consistent and useful; the 11-14 note already flagged exclusivity as derived. |
| Owner questions 1 (outline) and 2 (canvas) are the necessary ones | brief.md:3-6 (owner states the disagreement; canvas "not chosen") | owner | none | `C.px`, palette, `q_outline` | Consistent. Option (c) "delegate for the sample" is offered as an owner choice, not taken. No answer invented. |
| Specialist trial proposal (outlined, 32x32, facing right…) | note section "Specialist proposal" | specialist proposal, labelled | none | owner picks (c) on both | Labelled correctly as a proposal; would not confirm any choice. |
| Request preparation needs official PixelLab declarations; not available here | readiness report: official tools not observed; delegation.md:21-23 | runtime fact | none | host PixelLab connection | Consistent with my own readiness read. |

## Disposition after version 1

One discrepancy (the `li` key semantics) sent to the same native specialist with the
source evidence above; waiting for its revision. No other correction requested.
