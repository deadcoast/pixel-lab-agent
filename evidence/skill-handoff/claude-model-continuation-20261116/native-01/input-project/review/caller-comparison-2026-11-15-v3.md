# Caller comparison, version 3 (2026-11-15): controlled-evaluation answers applied

Reviewer: the calling agent (not PIXL). Versions 1 and 2 (`review/caller-comparison-2026-11-15-v1.md`,
sha256 77fe69e4fea8044bea62f42389b4831e2d6e3887ecd3604c9b5c2efacd84dc1c;
`review/caller-comparison-2026-11-15-v2.md`, sha256 c40843fe5c62c19c8b075fa62ef2552981bdadc7e6be176e727e254a7a8ef4e3)
reviewed the earlier session's revisions 7 and 8 and are retained unchanged. This version reviews
the specialist's single return of this round (revision 9) against the new input, the retained
sources and the installed runtime, and binds my adoption finding to that return.

Specialist: native child `a8efa4804f17d03b7`, subagent type `pixl:pixl`, one foreground round.
Its own review is in `deliverables/continuation-2026-11-15c.md` and its returned JSON; this file
is mine and is distinct from it.

## Inputs I read myself before and after delegation

| File | sha256 | Role |
|---|---|---|
| `sources/brief.md` | a78aca77135c5e533b8000272558b5b65e40ee421d1913cab961d7adc4cf5324 | owner brief, verbatim |
| `sources/controlled-evaluation-answers.md` | 87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30 | new input, 8 lines, read-only; unchanged after the round |
| `sources/reference-observations.md` | d0862d144da0c4b315af96a8129846b32075fac99826b618ad51c62b6a960495 | measured study (x_study) |
| `sources/method-research.md` | 1b1503b7a004c884b5b207a965aa85ac4c694f481d2936619a4030557f794e51 | method excerpts |
| `deliverables/continuation-2026-11-15.md` | d2114fc7be4337a55e5da8b2f0b19bc80c9b4445de0ae42eb302bab0acba5962 | retained continuation (s_continuation_2) |
| `deliverables/continuation-2026-11-15b.md` | 351f28630952562cacc429c9a6054617a7e9e77cce59a6193d536e838be01cad | amendment (s_continuation_3) |
| `deliverables/outline-decision-brief.md` | 32b59ab72587dc072627228f4e50f28cd3585daa8641cfb4f2386b51733878e2 | decision brief (x_aid) |
| `state.px/history/ac9150f4e8ee656761811370867538130faaa111759d61065153df358ef14225.px` | ac9150f4e8ee656761811370867538130faaa111759d61065153df358ef14225 | revision 8, state on entry |
| `pixl-kit/runtime/pixl/lifecycle.py` | 5e37cefb2bcb357373332af4970b7c30df4e18df6d78e36022fe349a616a6a23 | gate and pin rules |
| `pixl-kit/runtime/pixl/codec.py` (lines 208-237) | read | symbol vs string encoding |
| `pixl-kit/runtime/pixl/registry.json` (line 16, 30) | read | C field types; `li` meaning |
| `pixl-kit/runtime/pixl/registry-v2.json` (line 18) | read | I status vocabulary |
| `pixl-kit/skills/pixl/references/delegation.md`, `intake-sample.md`, `artistic-authority.md` (line 9), `request-review.md` (line 247) | read | caller review contract; authority rules |

## Final artifacts I reopened and verified after the specialist's last change

| File | sha256 | Check |
|---|---|---|
| `state.px/state.px` | fdf4ebfe7d2dc1565a9c003c28d61ecfa5b255ec19937198aa11d405c38b8ca1 | `pixl_validate`: valid, format 2, revision 9, 71 records, files verified; canonical hash equals file sha256 |
| `state.px/history/fdf4ebfe7d2dc1565a9c003c28d61ecfa5b255ec19937198aa11d405c38b8ca1.px` | fdf4ebfe7d2dc1565a9c003c28d61ecfa5b255ec19937198aa11d405c38b8ca1 | byte-identical to head; history now holds 10 files, revisions 6, 7 and 8 copies unchanged |
| `deliverables/continuation-2026-11-15c.md` | fd3f500708a1559162e0bc2da4c37d5201ec427a0c1aca90659695978b4e828b | 291 lines; bound by `s_continuation_4` (`ln [1,291]`, digest matches) |
| `work/build_rev9.py` | 821cff9b9c450e17687c1a0eb798c6239fead6c201cb82d9a349fd149e8bc78d | specialist builder |
| `work/verify_rev9.py` | 554b05fff710f4c780c1e8caa8d8dc497921d261390d043edd231bddff623f73 | I ran it with the selected interpreter (`-I`): `problems: []` on the committed head |
| `work/rev9.json` | c0a75ed07baec8478b2011fe994543dd594718307bbc53fc73f6db6ed5a0d519 | host-adapter document |
| `work/rev9.px` | fdf4ebfe7d2dc1565a9c003c28d61ecfa5b255ec19937198aa11d405c38b8ca1 | identical to head |
| `work/rev9-texts.json` | f3aa00609606977a40758c614400c9130345fc8bf8dd1f0be63a1a485b4b3ce4 | exact strings used by the verify script |
| `work/rev9-strings-diagnostic.json` | 1bc97c04479c23a43a59fc489183820b1b03e5675381463cdc3a4e4c645cc0df | diagnostic document for the pin failure; no .px produced |

`pixl_ready` on the head: `["t_sample"]`. Sorted line diff of the revision 8 history copy against
the head contains exactly: `c_sample` (new), `f_sample` (ct added; rq swapped), `handoff_5` (new),
`i_alpha`/`i_sampling`/`i_view` (wire type of `vl` only), `i_canvas`, `i_outline`, `i_palette`,
`q_sample_canvas`/`q_sample_palette`/`q_sample_outline`/`q_sample_readability` (new),
`s_continuation_4` and `s_eval_answers` (new), header `PX2 8` -> `PX2 9`. Nothing else differs.
Every pre-existing source, reference, deliverable, evidence file, review file, `SESSION.md`,
`CALLER-RESULT.json`, older history copy and `work/` file was re-hashed after the round and is
unchanged. The input file was not copied, rewritten or moved.

## Claim-by-claim comparison

| Claim or literal clause | Source and locator | Authority / status | Change actually made | Operation prerequisite | Finding and disposition |
|---|---|---|---|---|---|
| The input answers Q1 (outline) and Q2 (canvas) for the representative sample only, and nothing else | `sources/controlled-evaluation-answers.md` lines 3, 5, 6, 8 | controlled-evaluation input; explicitly not owner preference, not production policy, not human acceptance | `s_eval_answers` added; cited from `i_outline`, `i_canvas`, `i_palette` and the four sample criteria; not added to `project.sc` | none | Consistent. The unasked rows (`i_design_language`, `i_role_diff`, `i_backgrounds`, `i_display_scale`, `i_animation`, `i_engine`, `i_roster`, `i_lighting`) are byte-identical in the diff. Keeping the input out of `project.sc` is a reasonable reading: it is not a project intent source. |
| `i_outline` conflict -> **proposed**, value = the reference.png alternative, other alternative preserved | input line 5; `lifecycle.py:57-64` (sample gate accepts proposed), `lifecycle.py:72-75` (`confirmed` would also clear the production `choice_unconfirmed` gate); `registry-v2.json:18` (proposed needs rationale) | project choice remains the owner's | status, value, `so` (+`s_eval_answers`), `wy` rewritten with old-to-new reasoning and the reference-b.png alternative quoted | sample contract | Consistent with the input's stated scope and with `request-review.md:247` ("do not promote observed/proposed values to confirmed"). `confirmed` would have encoded more than the input says. Adopted. |
| `i_canvas` unresolved -> **proposed** `[32,32]` | input line 6; `sources/brief.md:4-5, 23` (owner has not chosen the final canvas) | owner; still open for production | status, value, `so`, `wy` | pins `C.px` | Consistent; the rationale states the brief's deferral still stands. Adopted. |
| `i_palette` stays **observed**, gains the input as source, rationale rewritten | `reference-observations.md:24, 34` (colours measured); input line 5 admits `#25354A` for the sample | owner; observed | `so`, `wy` only | pins `C.pl` | Consistent with correction 5 of the 2026-11-15 note (confirmation coupled to the role device). No promotion. Adopted. |
| `i_view`, `i_sampling`, `i_alpha` wire type string -> symbol (flagged by the specialist as a deviation) | `registry.json:16` (C.vw/sa/al are `sym` fields); `codec.py:213-217` (Symbol encodes as bare identifier, str as `~len:`); `lifecycle.py:134-138` (`encode_value(choice.vl) == encode_value(contract[key])`) | representation only | diff shows `vl=~4:side` -> `vl=side`, `~7:nearest` -> `nearest`, `~6:binary` -> `binary`; status, value word, `so`, `wy` unchanged | contract linkage of the three choices through `C.ch` | **Forced by the runtime**, not a judgment change. The alternative (dropping them from `C.ch`) would remove the gate linkage the agreed recipe planned. Accepted; confirmation sent to the same child. Revision 8 bytes remain in history. |
| `c_sample`: px/pl/vw/sa/al pinned to the five keyed choices; `i_lighting`, `i_outline`, `i_design_language` linked but not pinned | `lifecycle.py:13` (CONTRACT_FIELDS), `:131-138`; keys `lighting`, `edge_treatment`, `design_language` are not contract fields | runtime | new record | `f_sample.ct` | Consistent with the amended recipe (continuation-2026-11-15b step 3). Validated. |
| `C.li` composed per the 2026-11-15b rule with each component labelled by authority | `continuation-2026-11-15b.md:52-72`; `registry.json:30` (`li` = lighting and aesthetic intent) | component 1 observed; 2 proposed; 3 controlled-evaluation sample confirmation; 4 PIXL construction proposal | new string, 1426 bytes | none | Consistent. Labels inside the string say what each part is. The "2 logical px" weight is measured (`reference-observations.md:37`) and labelled as the weight of the treatment the input names, carried because the sample canvas equals the references'. Facing right is labelled a specialist sample choice. Nothing is called confirmed. Adopted. |
| Identity landmarks (a)-(e) | `reference-observations.md:25-28, 37-40` (stalks and notch, eyes, shoulder and base bars, contour); `method-research.md:15-16` (named identity landmarks) | measured features; naming them is PIXL's construction proposal under `i_design_language` | written into `C.li` and quoted in `q_sample_readability` | owner may override via the design-language answer | Consistent with correction 4 of the 2026-11-15 note. Adopted as a scoped proposal. |
| `f_sample.rq` swaps `q_canvas`/`q_palette`/`q_outline`/`q_readability` for `q_sample_*`; originals untouched on `f_scout`/`f_medic` | the originals' literal text ("confirmed canvas size", "confirmed project palette", "confirmed outline treatment", "head, torso and limb") in the revision 8 head; `delegation.md:25-35` (explicit old-to-new, retain identities) | prior-agent criteria under owner authority; new ones `wh=actor` | four new Q, one F edit | before any candidate is evaluated | Consistent: with nothing confirmed, the originals would be unsatisfiable for the sample. Old-to-new text and justification are given for each. `wh=actor` correctly marks them as specialist translations, not owner requirements. The originals remain for production. Adopted. |
| `q_sample_palette` keeps exclusive membership as a sample working rule | `artistic-authority.md:9` (no fixed palette imposed means production checks omit exact membership) | scoped sample rule, not owner requirement | new Q text says so explicitly and that a role accent may reopen it | none | Consistent: the rule is labelled scoped and does not reach production. Not a discrepancy. |
| `q_sample_readability` requires `i_display_scale` for the target zoom and keeps the specialist's test backgrounds until `i_backgrounds` is answered | `method-research.md:15, 47`; `outline-decision-brief.md:42-46` (not judgeable at 1x) | later review prerequisites, explicit | new Q text | before visual review, not before preparation | Consistent; prerequisites named, not turned into blockers. |
| `t_sample` ready; `t_scout`/`t_medic`/`t_family` blockers unchanged | `pixl_ready`, `pixl_workflow` on the head; `lifecycle.py:49-56, 65-67` | runtime | none | none | Verified: ready `[t_sample]`; production tasks still need `t_sample` done, a contract and a `D` decision. |
| Request preparation, dispatch, visual review and engine import remain unavailable locally | `pixl_readiness` (official PixelLab tools not observed; dependencies available); `delegation.md:21-23` | runtime fact | none | host's authenticated PixelLab connection; `i_display_scale`; `i_engine` | Consistent with my own readiness read. Missing capability, not a failed attempt. |
| Note omits the revision 9 hash because its own digest is bound inside revision 9 | `s_continuation_4.dg` = note sha256 | structural | none | none | Correct; the hash is published here and in the caller result file. |

## Correction round

None needed. The single return was consistent with the input, the sources and the runtime. The
specialist asked for caller confirmation of the forced wire-type change; I sent that
confirmation, with my own evidence, to the same native child and asked it not to change any file
or state. No second revision exists.

## Adoption finding

Revision 9 (`fdf4ebfe7d2dc1565a9c003c28d61ecfa5b255ec19937198aa11d405c38b8ca1`) and
`deliverables/continuation-2026-11-15c.md` apply the controlled-evaluation answers within their
stated scope: the sample contract `c_sample` exists, `t_sample` is ready, and no choice was
promoted beyond what the input states. The accepted research candidates, their verdicts and all
earlier bytes are untouched. I adopt the revision 9 head and the note's next operation. The
project is no longer `needs_input` for the sample contract; it is blocked for the next step on a
capability this session does not have (the official PixelLab tool declarations and connection),
not on an owner answer.
