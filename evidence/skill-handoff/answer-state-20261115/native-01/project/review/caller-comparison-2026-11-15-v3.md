# Caller comparison, version 3 (2026-11-15): revision 9, sample contract from the controlled-evaluation answers

Reviewer: the calling agent (not PIXL). Versions 1 and 2 (`review/caller-comparison-2026-11-15-v1.md`,
`review/caller-comparison-2026-11-15-v2.md`) reviewed the earlier returns (revisions 7 and 8) and are
retained unchanged. This version reviews the return of a new native `pixl:pixl` child
(agent ID `a073ff6729932c33a`) that applied `sources/controlled-evaluation-answers.md` and
committed revision 9. It is distinct from the specialist's own checks, which are recorded in
`deliverables/continuation-2026-11-15c.md` and in the child's returned JSON.

## What I did independently

- Read the brief, the new input, both retained continuation notes, the decision brief, the study,
  the method notes and the prior caller result before delegating.
- Hashed every non-kit file before delegation (baseline) and after the child finished; diffed.
- Decoded revision 8 (from `state.px/history/ac9150f4…4225.px`) and revision 9 (head) with the
  kit runner under the selected interpreter and diffed every record field myself
  (`work/caller-review/rev8-decoded.json`, `work/caller-review/rev9-decoded.json`).
- Ran `pixl_validate`, `pixl_ready`, `pixl_workflow` on the head; read `lifecycle.py`,
  `codec.py` (`encode_value`), `registry-v2.json`, `delegation.md`, `intake-sample.md`,
  `state-authority.md`, `agents/pixl.md`; ran `pixl_readiness`; re-measured both references with
  `pixl_asset_check` against the values the new contract pins.

## Final artifacts I reopened and verified

| File | sha256 | Finding |
|---|---|---|
| `state.px/state.px` | a6dd7768d252a474a3f67c356c8c8928fea83cb1884e5f13d28669ada27bb680 | PX2, revision 9, 71 records, valid, files verified; canonical hash equals file hash; byte-identical to its history copy |
| `state.px/history/a6dd7768…b680.px` | a6dd7768d252a474a3f67c356c8c8928fea83cb1884e5f13d28669ada27bb680 | revision 9 retained |
| `state.px/history/ac9150f4…4225.px` | ac9150f4e8ee656761811370867538130faaa111759d61065153df358ef14225 | revision 8 (entry state) retained, unchanged |
| `deliverables/continuation-2026-11-15c.md` | 96f8da59ec2c96573cde62c54a7cb50533375ac553a5a7f70a1cd4fcb7be5704 | new note, 215 lines; bound by `s_continuation_4` (`ln [1,215]`, digest matches) |
| `sources/controlled-evaluation-answers.md` | 52f68a3242dd72ab0d2bd8315c605160f5e6b76b626164f28a949d1563f30f94 | read-only input, unchanged; bound by `s_eval_answers` (`ln [1,5]`, 5 lines, digest matches) |
| `work/build_rev9.py` / `work/rev9.json` / `work/rev9.px` / `work/_decoded_rev8_readonly.json` | 64df5121…cff75 / e2bc9a14…2ec8 / a6dd7768…b680 / b8476ab8…3cf7 | specialist scratch, inside the consumer root; `rev9.px` byte-identical to the committed head |

File-hash diff against my pre-delegation baseline: only the head changed, and only the six files
above were added. `pixl-kit/`, `sources/`, both references, `CALLER-RESULT.json`, `review/*`,
all earlier deliverables, evidence and older history copies are byte-identical.

Record diff revision 8 to 9 (my own decode): added `s_eval_answers`, `s_continuation_4`,
`c_sample`, `q_sample_canvas`, `q_sample_palette`, `q_sample_outline`, `q_sample_readability`,
`handoff_5`; changed `project.sc`, `i_outline`, `i_canvas`, `i_palette`, `i_view`, `i_sampling`,
`i_alpha`, `f_sample`; nothing removed. This matches the specialist's old-to-new table line by line.
Every X, V, E and T record, the production criteria `q_canvas`/`q_palette`/`q_outline`/
`q_readability`/`q_style_match`, `handoff` through `handoff_4` and every earlier S keep their
revision-8 record hashes.

## Claim-by-claim comparison

| Claim or literal clause | Source and locator | Authority / status | Change actually made | Operation prerequisite | Finding and disposition |
|---|---|---|---|---|---|
| The input answers Q1 = outlined (reference.png) and Q2 = 32 x 32, scoped "for the representative sample", and declares itself simulated, not owner preference or human acceptance | `sources/controlled-evaluation-answers.md:3,5` | evaluation input; self-declared non-owner | `i_outline` conflict -> **proposed**; `i_canvas` unresolved -> **proposed**; both cite `s_eval_answers`; `wy` keeps both outline alternatives and the no-outline consequences; `wh` stays `user` | none | Consistent. `proposed` is the honest status: `lifecycle.py:57-64` blocks a sample only on unresolved/conflict; `:65-75` requires confirmed + `D` for production/delivery, so the production gate the input disclaims stays in place. `wh=user` matches every other I record in the store (all 14 are `wh=user`, including the pre-existing proposed `i_design_language` and `i_sampling`). Adopted. |
| The brief's "final canvas size not chosen" still stands | `sources/brief.md:4-5, 23` | owner | preserved in `i_canvas.wy` and in `c_sample.nm` ("confirms none") | none | Consistent. |
| Palette stays observed; `c_sample.pl` adopts the three measured colours without confirming a project palette | `sources/reference-observations.md:16, 24, 33-35`; correction 5 in `continuation-2026-11-15.md:94-98`; `q_palette.ck` exclusive rule | observation; derived rule | `i_palette.so` + `s_eval_answers`, `wy` rewritten, status and value unchanged | role device (`i_role_diff`) before confirmation | Consistent. My re-measurement: reference.png 3 colours, reference-b.png 2, both entirely inside the three-colour list, binary alpha, 32 x 32. |
| `c_sample` fields: px [32,32], pl three colours, vw side, sa nearest, al binary, ch of eight choices | `registry-v2.json:10`; `lifecycle.py:131-138`; amended step 3 in `continuation-2026-11-15b.md:95-98` | runtime + retained recipe | new record; `f_sample.ct = c_sample` | none | Consistent with the recipe. `pixl_validate` passes, so the five pinned keys equal their choices; the three unpinned keys (`lighting`, `edge_treatment`, `design_language`) are not contract field names (`lifecycle.py:13`). |
| `C.li` composed from lighting observation + design-language proposal + outline answer with landmarks + identity landmarks + scoped pose | composition rule `continuation-2026-11-15b.md:52-72`; `registry.json:30` ("lighting and aesthetic intent"); trial proposal `continuation-2026-11-15.md:158-166` | each clause labelled with its own authority | new string in `c_sample.li` | none | Consistent. Each clause names its status (observed / proposed / adopted for the sample, not owner confirmation / scoped specialist choice). "Facing right" is the retained specialist proposal, labelled as such. Adopted. |
| Correction 4 applied on the delegated path: new `q_sample_canvas`, `q_sample_palette`, `q_sample_outline`, `q_sample_readability`; `f_sample.rq` re-pointed; old Q records untouched for `f_scout`/`f_medic` | `continuation-2026-11-15.md:73-93`; `delegation.md:25-35` (old-to-new, retain identities); `method-research.md:15-16` (named identity landmarks); `reference-observations.md:24-28, 66-69` | derived criteria, `wh actor` | four new Q records; `f_sample.rq` changed; old Q bytes unchanged (record hashes equal) | none | Consistent. The readability text keeps the required outcomes (facing direction, separable named landmarks, light/dark/busy, target zoom) and names the landmarks the contract carries. `wh actor` is right for criteria derived against a proposed contract; production criteria keep `wh user`. Adopted. |
| Correction 6: `i_view`/`i_sampling`/`i_alpha` values were strings; `C.vw`/`sa`/`al` are symbols; the pinning rule compares wire encodings, so the retained recipe's `ch` would have failed | `codec.py:213-217` (symbol -> bare identifier; str -> `~len:bytes`); `lifecycle.py:133-138`; my run: `encode_value("side") = b'~4:side'`, `encode_value(Symbol("side")) = b'side'` | runtime fact | the three `vl` fields re-encoded as symbols; status, `so`, `wh`, `wy` unchanged | none | Verified against the code and by executing `encode_value`. No E receipt binds these records (the four E records bind only `f_*`, `q_*`, `s_*`, `user`, `x_*`), so no acceptance binding changed. The rejected alternative (dropping them from `ch`) would also drop the production `choice_unconfirmed` gate (`lifecycle.py:72-75`). A genuine defect in the revision-7/8 recipe, found and fixed by the specialist with an explicit old-to-new entry. Adopted. |
| `pixl_ready` lists `t_sample` with no blockers; `t_scout`/`t_medic`/`t_family` keep their blockers | `pixl_ready`, `pixl_workflow` on the head | runtime | none beyond the above | none | Confirmed by my own run: `ready: ["t_sample"]`, hash a6dd7768…b680. |
| Historical acceptance untouched | record hashes of x_*, v_*, e_*, t_* in `pixl_validate` rev 8 vs rev 9 | runtime | none | none | Confirmed identical. |
| The next operation needs the host's PixelLab connection (tool discovery, job-prepare, dispatch); visual review needs `i_display_scale` or stated zooms; engine import needs `i_engine` | `pixl_readiness` (official tools not observed, no provider assigned); `delegation.md:21-23`; `q_sample_readability.ck` | runtime fact / owner | none | host connection; owner answers | Consistent with my readiness read. Missing capability, not a failed attempt. |

## Points I weighed and did not treat as discrepancies

- **Confirmed vs proposed for the sample answers.** A reading in which the controlled answers are
  binding owner-equivalent decisions for the whole family would make `confirmed` appropriate. The
  file itself excludes that reading ("not real owner preferences or human acceptance") and scopes
  itself to the sample. `proposed` satisfies the sample gate and is reversible; if a later input
  states that these answers bind the family, the status move is a one-record change with that input
  as source. Recorded as a remaining question of this trial, not a defect.
- **`i_palette.so` gaining `s_eval_answers`** although the input does not mention colours. The
  rationale explains the dependency (the outline answer settles that navy is present). Acceptable
  as a supporting source; it does not change status or value.
- **The note cannot carry the exit hash** (its own bytes are an input to it). The specialist stated
  this and put the hash in the return and the history file name. Correct.

## Adoption finding

The revision-9 return is consistent with the owner brief, the new input's self-declared scope and
authority, the retained sources and the kit runtime. No correction round was needed, so none was
invented. I adopt revision 9 and `deliverables/continuation-2026-11-15c.md` as the current
continuation. `t_sample` is ready; the next operation is the provider request, which this
session cannot perform.
