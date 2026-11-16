# Continuation note, 2026-11-15 (d): pre-discovery sample request packet and local check tooling

Cold resume of the scout and medic family project by PIXL (agent) in an isolated development
evaluation, assigned by a calling agent. No generation provider, official PixelLab tool, game
engine or network was available or used. Nothing was generated; no provider job exists; no
candidate, evidence or verdict was created; no task state changed; no intake status or value
moved; the two accepted research candidates (`x_study`, `x_aid`) and their verdicts are
untouched. Earlier notes (2026-11-14, 2026-11-15, 2026-11-15b, 2026-11-15c) are preserved
unchanged. This session's consumer root is
`C:/Users/ryanf/AppData/Local/Temp/pixl caller review e3c7ebe124824b69828309bf1645f322/consumer`,
the kit is `pixl-kit/` inside it, and the interpreter is
`C:/github/pixel-lab-agent/.venv/Scripts/python.exe` (Python 3.14.3, Pillow 12.3.0,
jsonschema 4.26.0). Paths in older notes and scripts are provenance only.

## State identity on entry

- `state.px/state.px`: PX2, revision 9, canonical state hash
  `fdf4ebfe7d2dc1565a9c003c28d61ecfa5b255ec19937198aa11d405c38b8ca1`, 71 records, valid, all
  bound files verified (`pixl_workflow`, `pixl_ready`, `pixl_jobs`, focused
  `pixl_context(t_sample, authoring)` this session). `handoff_5` is the current N record.
- Ready: `[t_sample]`, no blockers. `t_scout`, `t_medic`: `task_prerequisite`, `output_contract`,
  `task_decision`. `t_family`: two prerequisites and a decision blocker. No jobs. No families.
- Re-hashed this session, all matching their S records: `sources/brief.md` (`a78aca77...4cf5324`),
  `sources/controlled-evaluation-answers.md` (`87cf7eec...52f6e30`),
  `sources/reference-observations.md` (`d0862d14...a960495`), `sources/method-research.md`
  (`1b1503b7...794e51`), `reference.png` (`d997cade...70aa7`), `reference-b.png`
  (`e76b40ce...14a12a`), the four earlier continuation notes.
- Both references re-measured with `pixl_asset_check`: 32 x 32, 390 visible pixels, zero
  fractional-alpha pixels, one opaque component, visible bbox `[7, 3, 25, 28]` (half-open);
  reference.png 3 colours, reference-b.png 2 colours, none outside
  `#56B5BC / #F4DDA2 / #25354A`. Both 12x views under `work/reference-views/` were viewed: the
  navy in reference.png forms the full contour, both stalks, the shoulder bar and the base
  bar; reference-b.png is the same mask in flat teal with the cream eyes only. Matches the study.

## State identity on exit

- Revision 10, 76 records (71 + `s_sample_brief`, `s_sample_criteria`,
  `s_sample_request_review`, `s_continuation_5`, `handoff_6`), committed to the store folder
  `state.px` with expected hash `fdf4ebfe...8ca1`.
- The revision 10 canonical hash is not written here: this note's own digest is bound by
  `s_continuation_5` inside revision 10. Read it from `state.px/state.px`, its copy in
  `state.px/history/<hash>.px`, `SESSION.md`, or the caller return of this session.
- Expected after commit (no I/C/F/Q/T change, so the lifecycle report cannot differ): ready
  `[t_sample]`; `t_sample` blockers `[]`; production and delivery blockers exactly as on entry.
  `work/verify_rev10.py` checks this against the committed head.

## Owner decisions and authorization, recovered separately from predecessor proposals

- Owner (brief, 2026-09-14, `sources/brief.md`): roster scout + medic (confirmed); side-view game
  (confirmed); the two references are the style authority and disagree about outline; the final
  canvas size is explicitly not chosen; scope "begin the project and make the progress possible
  in this session". That scope is the standing authorization for sample work.
- Controlled-evaluation input (`sources/controlled-evaluation-answers.md`, 8 lines): outlined as
  reference.png (line 5) and 32 x 32 (line 6), for the representative sample only; explicitly not
  an owner preference, not family/production policy, not human acceptance (line 8). Applied in
  revision 9 as `proposed`. No new owner answers exist in this session and none were invented.
- Predecessor proposals (PIXL, not owner): design language (style swatch, side-view figure),
  nearest sampling, facing right, the identity-landmark list, palette exclusivity for the
  sample. All remain proposals; nothing in this session promotes them.
- Not authorized or possible: paid, remote, network or host-configuration actions.

## What was done and why

**(a) Pre-discovery request packet** under `deliverables/sample-request/`. The next operation
(`job-prepare` for `t_sample`) needs the live PixelLab declaration, which this host does not
expose. Everything that does not depend on that declaration was prepared so that the future
translation is a mechanical step against a reviewed contract rather than fresh interpretation:

1. `sample-creative-brief.json`: provider-neutral translation of `c_sample` with `kind`
   `creative_brief`, `executable: false`. The intent is `c_sample.li` verbatim plus a
   component table in which each component keeps its authority wording (observed / PIXL
   proposal / controlled-evaluation sample confirmation / scoped specialist choice; nothing
   called confirmed). Hard constraints: 32 x 32, binary alpha, nearest (as a delivery rule, not
   a generation parameter), single static image, side view, facing right, the three-colour
   working palette, the outlined treatment. Reference roles per `pixellab-operations.md`:
   `reference.png` = style (primary anchor) + palette (sample working set; observed, not
   adopted), not identity/pose/layout/mask/motion; `reference-b.png` = style (secondary),
   conditionally included only if the live operation takes more than one style image with
   `reference.png` first, otherwise omitted from the request (its no-outline treatment pulls
   against the treatment under trial) while remaining the review comparison for
   `q_style_match`. Output cardinality 1 with the retain-all / nominate-one rule. Nine schema
   questions (SQ1-SQ9) that must be answered from the live declaration before translation:
   fixed 32 x 32 output, style-image count and transport, transparency and binary-vs-fractional
   alpha, output count, single-image vs character operation, intent field and parameter-level
   controls, forced palette, poll/retrieve tool, cost.
2. `sample-criteria.json`: validates against `pixl-kit/runtime/pixl/asset-plan.schema.json`
   (version 1, scope, one output `f_sample`, contract size/palette/view/sampling/alpha/intent,
   the five exact revision 9 criterion texts with id, check, domain, mode, basis, scope,
   authority and sources). Every `lines` bound was verified by opening the file; the retained
   validation output (`criteria-schema-validation.json`) records `schema_valid: true` and all 18
   bounds inside their files. Authority labels: `proposal` for the four `wh=actor` sample
   criteria (each basis splits the observed, evaluation-confirmed and specialist clauses, since
   the schema allows one label per criterion), `requirement` for the owner-owned
   `q_style_match`.
3. `request-review.json` per `request-review.md`: sources with sha256 and locators, `request`
   pointing at the brief with `kind: creative_brief`, `executable: false`, `tool: null`;
   `criteria` with the validation link and the saved Q record hashes; `choices`; `resume`
   (store/task/output/contract/hash); local tooling links. It states that `pixl_request_review`
   cannot consume it: the runtime (`request_review.py` lines 130-134) requires
   `request.kind == "provider_arguments"`. This was demonstrated and retained
   (`request-review-tool-refusal.json`, exit 2, "review expects exact provider arguments, not a
   creative brief"). That refusal is the expected behaviour for a pre-discovery packet, not a
   packet defect; a successor packet with exact provider arguments will be reviewable.

**(b) Operation shortlist** `operation-shortlist.json`, built from `pixl_capabilities` and
labelled as what it is: a documentation catalog retrieved 2026-09-11 with `live_discovery:
false`, supplying names, required argument names and poll tools only. Five plausible rows
(`create_image_pro`, `create_image_pixflux`, `create_image_pixen`, `create_character`,
`create_1_direction_object`) each carry the discriminating questions to put to the live
declaration; post-processing tools and non-applicable tools are listed separately; no tool is
decided. Decision rule: fixed 32 x 32 output, an actual style-image input with usable
transport, transparent output, single-image packaging; otherwise report the mismatch with a
staged path rather than changing the contract.

**(c) Local mechanical check harness** `work/sample-checks/check_sample_mechanical.py`,
runnable with the selected interpreter under `-I` against any PNG. It evaluates the two
local-mode criteria with their saved text embedded verbatim (record hashes
`09be7cba...aabd8` and `0563ebde...40589`): `q_sample_canvas` = width 32, height 32, zero
pixels with 0 < alpha < 255; `q_sample_palette` = every pixel with alpha > 0 in the three
colours. Frame count is reported as an additional measurement outside both criteria (a first
in-session draft had folded it into the canvas pass; that was corrected before anything was
bound, and the dry run was re-run with the corrected file). Dry run on `reference.png`,
`reference-b.png` and three synthetic fixtures derived from `reference.png` with exactly one
condition broken each (33 x 33; one `#FF00FF` pixel; one alpha-128 pixel): results
pass/pass, pass/pass, FAIL/pass, pass/FAIL, FAIL/pass, exit codes 0 0 1 1 1,
`discriminates_as_expected: true` in `dry-run.json`. This is tooling, not evidence: no X, E or
V record and no verdict was created; the references are not candidates.

**(d) This note**, bound as `s_continuation_5`, with `handoff_6` (rv 10). **(e)** `SESSION.md`
current-session pointer updated to this note, this invocation's paths and the revision 10 head,
keeping the predecessor provenance lines.

## Files created this session (consumer-relative, sha256)

| Path | sha256 | Role |
|---|---|---|
| `deliverables/sample-request/sample-creative-brief.json` | `cc21bf77519ed46e7a6f634718efcc79816a8f9895cc4ece4e89b007bf7380ce` | creative brief (request, not executable); bound `s_sample_brief` |
| `deliverables/sample-request/sample-criteria.json` | `14c979ea9bbfb686f7a9c693d552facfac5a135c45c3184d969611116611834b` | criteria plan, schema-valid; bound `s_sample_criteria` |
| `deliverables/sample-request/request-review.json` | `ffa933ede2b985eafd4c616e83b4a69d0b34a99002a731439704dcd0d781e78b` | request-review packet; bound `s_sample_request_review` |
| `deliverables/sample-request/operation-shortlist.json` | `7294d9d779982ee6602412eaed925ca2dab6e0b0c787f314455de6f53ed00186` | dated-documentation shortlist, not discovery |
| `deliverables/sample-request/criteria-schema-validation.json` | `93643a34d32353b5471fd9943aed8bb3a0bf8cb48a94d8413c42635a1aaeb16a` | retained validation output (schema_valid true; 18/18 bounds inside files) |
| `deliverables/sample-request/validate_criteria.py` | `48f3d0f1274b9635284571eed78405955c0e9aa57fa0ee8e57ce2fa955adbe45` | validation script (Draft 2020-12, same validator class as the runtime) |
| `deliverables/sample-request/request-review-tool-refusal.json` | `54ac0e6a74705cae79f140df417ff5b710739a9804070eef35ae591a565aa625` | retained runtime refusal of the creative-brief packet (exit 2) |
| `work/sample-checks/check_sample_mechanical.py` | `a0fc3d5c00ed7644218265492dc386efed24fc1e2e09444a1143bed6f15ddc69` | mechanical harness for `q_sample_canvas`, `q_sample_palette` |
| `work/sample-checks/make_fixtures.py` | `17306777635b4d4d735475d5831c762558cb7e7078a332c075399b6546361a04` | fixture generator |
| `work/sample-checks/aggregate_dry_run.py` | `346b425725cd44cddc3a404c698300360657e3704e2e45a0b02336e7ce5848c0` | dry-run aggregator |
| `work/sample-checks/fixtures.json` | `66276ba05234b8bac4f95b75c444ad07b7715d6672a3677003ab70ac2ffe803b` | fixture manifest |
| `work/sample-checks/fixture-33x33.png` | `564fd4d518d96be4db7e38a834862a8e3c43c207e187dc6341fbdcd371487277` | failing fixture (canvas) |
| `work/sample-checks/fixture-offpalette.png` | `ef37ba6f701a1fd18d319565f8490a7459435f03777ca909f3ddd60b1075ecd9` | failing fixture (palette; pixel [9, 11]) |
| `work/sample-checks/fixture-fractional-alpha.png` | `da90b6b7d2f45c256871400d41dc0f6bc76875e9cb5962650042ede44effe364` | failing fixture (alpha; pixel [9, 11]) |
| `work/sample-checks/run-reference.json` | `b01f423edd003223f4317f0736c243152a81396896b92c649ac764cd22ccfc0e` | dry-run output |
| `work/sample-checks/run-reference-b.json` | `bd2c60fbf2013a09ceecbb6dc5a8013ba4624760f82adafcba160837b6e1feec` | dry-run output |
| `work/sample-checks/run-fixture-33x33.json` | `e439a91e66528ff6ef75fbd1994d6006f5540a2cc7746a6d75f48c6d15a96ea9` | dry-run output |
| `work/sample-checks/run-fixture-offpalette.json` | `41018002e61c8c9968de2f2d36d21e4f2554caf1ccdb2ce8e92ce6722a1b6ab3` | dry-run output |
| `work/sample-checks/run-fixture-fractional-alpha.json` | `4f7ff42d5e0cdaecf22c314f2bb1f3b155f1ffc5cfa860a845519112488a996f` | dry-run output |
| `work/sample-checks/dry-run.json` | `e379ff5e405593bf3daf3c7d7cff5feaec8c27d91c40c4686df12cc42804fb8b` | aggregated dry run, `discriminates_as_expected: true` |
| `work/build_rev10.py` | `493ad0aa67bff17f8f598a5848f23718592b9de2af8dc6a228b94d3ac28b5093` | revision 10 builder |
| `work/verify_rev10.py` | `f5e5f961ecff786775f4d5f333e728ab53c3345e1fc2079237a9b045d29be4b5` | revision 10 verifier (read-only) |
| `work/rev10.json`, `work/rev10.px` | produced by the builder; `rev10.px` bytes equal the committed head | candidate document and wire |
| `deliverables/continuation-2026-11-15d.md` | bound by `s_continuation_5` (digest in the state) | this note |
| `SESSION.md` | edited; hash in the caller return | current-session pointer |

Timestamps inside the retained JSON files are host-clock UTC readings and cross midnight
(`2026-11-15T23:58Z` to `2026-11-16T00:0xZ`); the session date and every `S.at` is
`2026-11-15`.

## Why the three packet files are bound as S records

`s_sample_brief`, `s_sample_criteria` and `s_sample_request_review` are the exact reviewed
translation that the next operation must compare against before `job-prepare` and again before
dispatch (`provider-recovery.md`, "compare the saved prepared request with the exact arguments
in the reviewed request packet"). Binding them makes `validate` detect any drift of those bytes,
and a future `provider_arguments` packet is a new file beside them, not an edit. Not bound: the
shortlist (a derivation from dated documentation; its hash is inside the packet), the
validation and refusal outputs (tool output; hashes here and in the packet), and the harness,
fixtures and dry-run (tooling, not evidence; binding them as sources would present measurements
of fixtures as project evidence). `handoff_6.fo` names the four new S records, the previous
note and evaluation input, `c_sample`, `f_sample`, the open and proposed choices and the two
accepted research artifacts.

## Records added in revision 10 (9 -> 10 delta)

| Record | Kind | Content |
|---|---|---|
| `s_sample_brief` | S (new) | `ur deliverables/sample-request/sample-creative-brief.json`, `dg cc21bf77...380ce`, `ln [1, 140]`, `at 2026-11-15`, `au local` |
| `s_sample_criteria` | S (new) | `ur deliverables/sample-request/sample-criteria.json`, `dg 14c979ea...1834b`, `ln [1, 101]`, `at 2026-11-15`, `au local` |
| `s_sample_request_review` | S (new) | `ur deliverables/sample-request/request-review.json`, `dg ffa933ed...1e78b`, `ln [1, 66]`, `at 2026-11-15`, `au local` |
| `s_continuation_5` | S (new) | this note, `ln [1, N]` with its actual line count, `at 2026-11-15`, `au local` |
| `handoff_6` | N (new) | `wh actor`; `rv 10`; `nx [t_sample]`; `bl [t_scout, t_medic, t_family]`; `fo` = `s_continuation_5`, `s_sample_brief`, `s_sample_criteria`, `s_sample_request_review`, `s_continuation_4`, `s_eval_answers`, `c_sample`, `f_sample`, `i_outline`, `i_canvas`, `i_palette`, `i_design_language`, `i_backgrounds`, `i_display_scale`, `i_role_diff`, `i_animation`, `i_engine`, `x_aid`, `x_study` |

Header `PX2 9 -> PX2 10`. Nothing else: every I (status, value, sources, rationale), C, F, Q,
T, X, E, V, P, earlier S and N record is byte-identical to revision 9 (`work/verify_rev10.py`
compares all 71 against `work/rev9.json`, which the caller verified identical to the revision 9
head). No D exists.

## Decision table (authority and status unchanged by this session)

"Needed for job-prepare?" is about preparing the sample request against `c_sample`. An answer
adopts only the choices it explicitly supplies; unasked rows keep their status.

| Choice (record) | Authority / saved status | Needed for job-prepare? | Effect / where it binds |
|---|---|---|---|
| Outline (`i_outline`) | Owner for the project; **proposed** (controlled-evaluation sample confirmation, `s_eval_answers`; reference-b alternative preserved in `wy`) | No (already in `c_sample.li` component 3) | Brief component 3; `q_sample_outline` (visual). Family treatment still the owner's. |
| Canvas (`i_canvas`) | Owner; **proposed** `[32, 32]` (sample-scoped) | No (pins `C.px`) | Brief hard constraint; SQ1; `q_sample_canvas`. Production canvas still the owner's. |
| Palette (`i_palette`) | Owner; **observed** three colours | No (pins `C.pl`) | Brief working palette; SQ7; `q_sample_palette` exclusivity is a sample working rule. Confirmation coupled to `i_role_diff`. |
| View (`i_view`) | Owner; **confirmed** `side` | Settled | Brief hard constraint; `q_sample_readability`. |
| Sampling (`i_sampling`) | PIXL proposal; **proposed** `nearest` | No | Delivery/engine rule in the brief, not a generation parameter. |
| Alpha (`i_alpha`) | Observed; **observed** `binary` | No (pins `C.al`) | Brief hard constraint; SQ3; `q_sample_canvas`. |
| Lighting (`i_lighting`) | Observed; **observed** flat | No | Brief component 1. |
| Design language (`i_design_language`) | PIXL proposal; **proposed** | No; the sample trials it | Brief component 2 and landmark list (component 4). Owner can override; landmarks then follow. |
| Game backgrounds (`i_backgrounds`) | Owner; **unresolved** | No; before visual review it replaces the specialist's light/dark/busy test set | `q_sample_readability` prerequisite named in the check. |
| Display scale (`i_display_scale`) | Owner; **unresolved** | No; before visual review (target integer zoom) | `q_sample_readability`, `q_sample_outline` zoom; `pixl_inspection_prepare` view scales. |
| Role differentiation (`i_role_diff`) | Owner; **unresolved** | No (sample carries no role device) | Before scout/medic production; may reopen palette exclusivity. |
| Animation (`i_animation`) | Owner; **unresolved** | No (sample is a single static sprite by plan) | Before scout/medic production: output kinds and operation choice. |
| Engine (`i_engine`) | Owner; **unresolved** | No | `q_engine_import` on the family delivery stays unavailable. |
| Roster (`i_roster`) | Owner; **confirmed** | Settled | None. |

## Operation-effect trace: the next operation is `job-prepare` for `t_sample`

Traced on revision 9 (identical lifecycle inputs in revision 10):

- `t_sample` (phase `sample`, `open`, `dp [t_study]` done, `op [f_sample]`, `ca []`, `dc []`,
  `kn []`) -> `f_sample.ct = c_sample`, `f_sample.rq` = the five Q -> `c_sample.ch` ->
  `i_canvas` proposed (pins `px`), `i_palette` observed (pins `pl`), `i_view` confirmed (pins
  `vw`), `i_sampling` proposed (pins `sa`), `i_alpha` observed (pins `al`), `i_lighting`
  observed, `i_outline` proposed, `i_design_language` proposed (linked, not pinned). No linked
  choice is `unresolved` or `conflict`, so the sample-phase gate is satisfied; `pixl_workflow`
  reports blockers `[]`. The production-phase `choice_unconfirmed` gate does not apply to a
  sample task. `other_intake` (`i_animation`, `i_backgrounds`, `i_display_scale`, `i_engine`,
  `i_role_diff` unresolved; `i_roster` confirmed) is unlinked and does not gate preparation;
  two of them gate visual review later (table above).
- `pixl_jobs`: no prepared, unknown, submitted or running attempt on `f_sample`, so a new
  request does not duplicate pending work.

`job-prepare STORE JOB TASK REQUEST_JSON --outputs OUTPUT --expect HASH --root ROOT` consumes:

| Input | Status |
|---|---|
| `STORE` = `state.px`; `TASK` = `t_sample`; `--outputs f_sample`; `--root` = this consumer root | available |
| `--expect` = the revision 10 canonical hash | available after this session's commit (in `SESSION.md` and the caller return) |
| `JOB` = a new job ID (for example `j_sample_1`) | to be chosen at preparation |
| `REQUEST_JSON.provider` = the actual connected PixelLab identity | **missing**: the host's authenticated PixelLab MCP connection |
| `REQUEST_JSON.tool` = the chosen operation's actual name | **missing**: decided from the live declaration using `operation-shortlist.json` and SQ1-SQ5 |
| `REQUEST_JSON.schema` = the full live `inputSchema` object | **missing**: `pixl_capabilities` cannot supply it |
| `REQUEST_JSON.arguments` = exact provider arguments | **missing**: translated from `sample-creative-brief.json` once SQ1-SQ7 are answered; reference.png travels as an actual image input (upload handle / URL / ID bound to `d997cade...70aa7`, role style); reviewed through a successor `request-review.json` with `kind provider_arguments` that `pixl_request_review` can consume |
| `REQUEST_JSON.discovery` = `{source, observed_at, evidence}` | **missing**: live tool listing with a host-clock timestamp |
| `REQUEST_JSON.authorization` = `{scope, evidence}` | scope text available (brief's "make the progress possible" for the sample; evaluation answers bind the sample only); **evidence object and cost coverage** to be supplied by the caller/host (SQ9) |

Preparation then saves J (prepared) plus journal X/E with no remote action; after the caller's
comparison of the saved request with the reviewed packet, `job-dispatch` publishes the single
claim, the host makes the one call, `job-observe` records the returned identifier and states,
`job-import` snapshots the downloaded bytes as an unaccepted X for `f_sample`. Acceptance then
needs the local harness run recorded through `pixl_candidate_review` / inspection as E/V for
`q_sample_canvas` and `q_sample_palette`, and `pixl_inspection_prepare` / `pixl_inspection_review`
for the three visual criteria, which need `i_display_scale` (and benefit from `i_backgrounds`).

## What later production still needs (unchanged, listed so nothing is dropped)

- `t_sample` done: a nominated candidate passing all five `f_sample.rq` criteria.
- Owner answers (not sample-blocking): final outline treatment for the family, final canvas,
  role-differentiation device (and with it the palette confirmation, possibly with a reserved
  accent), animation requirements, target backgrounds, display scale, engine/importer.
- Raster contracts for `f_scout`/`f_medic` whose linked choices are **confirmed** (production
  phase), evidence-backed `D` decision records with executed proofs for `t_scout`, `t_medic`,
  `t_family`, and the family baseline/continuity plan per the family-delivery operation.
- `q_engine_import` remains unavailable until `i_engine` is answered.

## Defects looked for and not found; one kit limitation

No defect was found in `c_sample` or the five saved criteria that would need a corrected
proposal: the texts, authority labels inside `li`, and the scope sentences match the sources
cited by line. One limitation of the kit's `asset-plan.schema.json`: a criterion carries a single
`authority` label, so the four mixed-authority sample criteria are labelled `proposal` with the
split written into `basis` and `scope`; the caller should read those fields, not the label alone.

## Preserved and unchanged

All earlier reports, evidence files, review files, state history copies, `work/` builders and
candidates for revisions 2-9, `x_study` and `x_aid` with their verdicts, `handoff` through
`handoff_5`, every source byte, both references, `pixl-kit/`, `CALLER-RESULT.json` and
`CALLER-RESULT-ANSWER-STATE.json`. `SESSION.md` is the only pre-existing file edited.
