# Caller comparison, version 2, final (2026-11-15)

Reviewer: the calling agent (not PIXL). Version 1 (`review/caller-comparison-2026-11-15-v1.md`,
sha256 77fe69e4fea8044bea62f42389b4831e2d6e3887ecd3604c9b5c2efacd84dc1c) reviewed the
specialist's first return (revision 7) and is retained unchanged. This version binds my
adoption finding to the specialist's revision after the correction round.

## Final artifacts I reopened and verified

| File | sha256 | Role |
|---|---|---|
| `state.px/state.px` | ac9150f4e8ee656761811370867538130faaa111759d61065153df358ef14225 | head, PX2 revision 8, 63 records; `pixl_validate` valid, files verified; identical to its history copy |
| `state.px/history/6007ba83…b5a5.px` | 6007ba8338475d50c6ee87af27c7d6766d762890f3b12f9a040d74fa3916b5a5 | revision 7 retained |
| `state.px/history/b9a66bef…b5b7.px` | b9a66beff93bcc2197a442d1de8ed6d7d9178aacf0c10606512a38e64d78b5b7 | revision 6 (entry state) retained |
| `deliverables/continuation-2026-11-15b.md` | 351f28630952562cacc429c9a6054617a7e9e77cce59a6193d536e838be01cad | amended continuation (`s_continuation_3`) |
| `deliverables/continuation-2026-11-15.md` | d2114fc7be4337a55e5da8b2f0b19bc80c9b4445de0ae42eb302bab0acba5962 | first continuation of this session (`s_continuation_2`), unchanged |
| `deliverables/continuation-2026-11-14.md` | d9755b269273a364296c6fc501be56d4ee7e305ec9ad6d40f1eca48b1d2d8de9 | predecessor note, unchanged |

Pre-existing sources, references, evidence, decision brief, comparison sheet, SESSION.md
and all older history files re-hashed after the last specialist change: unchanged.
`diff` revision 7 vs 8: header; `i_lighting` key `li` -> `lighting` and rationale
rewritten (value, status, sources unchanged); `s_continuation_3` added; `handoff_4`
added. `project.in` unchanged. `pixl_ready`: empty. No intake status moved, no
acceptance, verdict, candidate or criterion touched.

## Correction round

- My finding (sent to native child `a7f9957f93675cbf8`): the kit defines contract field
  `li` as "lighting and aesthetic intent" (`pixl-kit/runtime/pixl/registry-v2.json:10`,
  `registry.json:30`), its intake default is a whole-intent placeholder (`store.py:233`),
  the plan schema names the mapped field `intent` (`asset-plan.schema.json:77-88`,
  `plar_prepare.py:290`), and `lifecycle.py:133-138` pins a linked choice keyed by a
  contract field name to that field's value. The revision-7 recipe would therefore have
  pinned the sample contract's whole intent to a lighting-only phrase.
- Specialist disposition: accepted; rekeyed `i_lighting` to `lighting`, rewrote its
  rationale, added a composition rule for `C.li` (lighting observation + design-language
  proposal + outline answer + named landmarks, each keeping its own authority), committed
  revision 8 against the revision-7 hash, saved the amendment as a new note with an
  explicit old-to-new table. I re-read the amended note and confirm the old-to-new table
  matches the actual byte diff.

## Claim-by-claim comparison against the final version

| Claim or literal clause | Source and locator | Authority / status | Change authorized | Operation prerequisite | Finding and disposition |
|---|---|---|---|---|---|
| `t_sample` is blocked only by the missing raster contract | lifecycle.py:53-56; `pixl_workflow` | runtime | none | `f_sample.ct` | Consistent at rev 6, 7 and 8. |
| Only `C.ch`-linked choices in unresolved/conflict block a sample; observed/proposed acceptable; confirmed + `D` required only for production/delivery | lifecycle.py:30-41, 57-75 | runtime | none | contract authoring | Consistent. Supports the specialist's corrections 1 and 3 to the 2026-11-14 note; also matches delegation.md:102-105. |
| Linked choice keyed by a contract field must equal it | lifecycle.py:131-138 | runtime | none | contract authoring | Consistent; after the rekey only `px`, `pl`, `vw`, `sa`, `al` will be value-pinned, as the amended note states. |
| `i_lighting` observed flat, key `lighting` | reference-observations.md:16, 24, 29, 37-40 (3 vs 2 flat colours, "single flat colour with no ramp", no AA/dither) | owner; observed from references only | new record (rev 7), rekey (rev 8) | none | Supported as an observation. Not an output policy; the record and note say so. Adopted. |
| `i_animation` unresolved | brief.md:31; reference-observations.md:73 | owner; unresolved | new record only | before scout/medic production | Supported; no value invented. Adopted. |
| `C.li` composition rule | registry.json:30; store.py:233 | specialist proposal for contract authoring | none now | owner answers to questions 1 and 2 | Consistent with the kit's field meaning; each component keeps its source authority. Adopted as the recipe for the next operation. |
| `q_canvas` / `q_palette` / `q_outline` worded against *confirmed* values; sample-specific copies needed on a delegated path | state.px Q records | prior agent authoring under owner authority | deferred to the contract commit with old-to-new explanation | owner answer path | Reasonable and deferred correctly (delegation.md:25-35). Not applied now. |
| `q_readability` "head, torso and limb landmarks" presumes a limbed figure | method-research.md:15-16; reference-observations.md:24-28, 66-69 | prior agent assumption | deferred | design-language answer or trial | Supported; replacement keeps the required outcome (facing direction, separable named landmarks, light/dark/busy, target zoom). |
| Palette confirmation coupled to role device | `q_palette.ck` exclusive rule; `i_role_diff` unresolved | derived rule | none | none | Consistent; useful advice, not a new owner-confirmation requirement. |
| Necessary owner questions: outline treatment; canvas for the sample | brief.md:3-6 (owner states the disagreement and that canvas is not chosen) | owner | none | `C.px`, `C.pl`, `q_outline` | Consistent. Alternatives include "delegate for the sample"; none chosen by the agents. |
| Design language, backgrounds, display scale, role device, animation, engine are not blockers for the contract | lifecycle.py:65-75; decision table | owner; proposed / unresolved | none | later phases | Consistent; later prerequisites left explicit, not turned into blockers. |
| Request preparation and dispatch unavailable here | `pixl_readiness`: official PixelLab tools not observed; delegation.md:21-23 | runtime fact | none | host's authenticated PixelLab connection | Consistent with my own readiness read. Missing capability, not a failed attempt. |

## Adoption finding

The final continuation (`continuation-2026-11-15.md` as amended by
`continuation-2026-11-15b.md`) and revision 8 are consistent with the owner brief, the
retained sources and the kit runtime. The two local additions are observations and gaps
the sources support; nothing was confirmed on the owner's behalf. I adopt the amended
next-operation recipe. The project is correctly `needs_input` on two owner questions.
