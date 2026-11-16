# Continuation note, 2026-11-15 (f): handoff-only continuation under a new consumer root

This increment retains the prepared work, re-inspects the actual current state and the artifacts
the revision 11 handoff relies on, and saves a current continuation for the next session. It is a
**handoff-only increment**: no request packet, fixture, harness, generation, provider, candidate,
verdict, evidence, intake-status or task-state work was assigned or performed. The contract
`c_sample`, the five sample criteria, every I record, every T state and every retained file keep
their bytes. The only production-state change is the addition of this note's S record and a new N
record (revision 12, below). No owner answers were supplied in this invocation and none are invented.

## Consumer-root change

| | Root |
|---|---|
| Current (this increment) | `C:/Users/ryanf/AppData/Local/Temp/pixl caller review a97de5914a21428aad2fef3c65ecfcec/consumer` |
| Previous session (e note, `SESSION.md` before this edit, previous caller result) | `C:/Users/ryanf/AppData/Local/Temp/pixl caller review e3c7ebe124824b69828309bf1645f322/consumer` |
| Predecessor (2026-09-14) | kit at `.agents/skills/pixl-kit`, interpreter `.../pixel-lab-docsuite/.venv/...` |

Every absolute path inside a retained file (`SESSION.md` before this edit, `CALLER-RESULT*.json`,
earlier notes, `work/` scripts, `sources/brief.md` session constraints) is **provenance** of the
session that wrote it, not a current location. All consumer-relative paths and all S-record
`ur`/`dg` bindings resolve unchanged under the new root: `pixl_validate` reports
`files_verified true` with the root relocated, which is the only check the relocation needed.
The kit path (`pixl-kit/` inside the consumer root), the interpreter
(`C:/github/pixel-lab-agent/.venv/Scripts/python.exe`) and the runner (`pixl-kit/scripts/pixl.py`)
are unchanged from the previous session.

## State identity on entry

| Item | Observed |
|---|---|
| `state.px/state.px` | PX2, revision 11, 80 records, valid, `files_verified true` |
| Canonical state hash (= head sha256 = `state.px/history/720a1a1e....px`) | `720a1a1ecc59f210654485f4e279b1cb58dd881629ece37ef2db323c1ecec443` |
| `pixl_ready` | `[t_sample]` |
| `pixl_jobs` | `[]` (no prepared, unknown, submitted or running attempt) |
| `pixl_workflow` blockers | `t_sample` none; `t_scout`, `t_medic`: `t_sample` open, output needs a raster contract, task needs an adoption decision; `t_family`: `t_scout` and `t_medic` open, needs an adoption decision; `t_aid`, `t_study` done |
| Head N record | `handoff_7` (rv 11) |
| `work/verify_rev11.py` (run with `-I`) | `problems []`, exit 0 |
| Families / plans | none |

## State identity on exit

Revision 12, 82 records (80 + `s_continuation_7` + `handoff_8`), committed to the store folder
`state.px` with expected hash `720a1a1e...c443`. The revision 12 canonical hash is not written
here because this note's digest is bound inside it; read it from `state.px/state.px`,
`SESSION.md` or the caller return. Expected after commit (checked by `work/verify_rev12.py`):
ready `[t_sample]`, blockers unchanged, no jobs, all 80 revision 11 records byte-identical.

## Kit identity observed now

`pixl_readiness` (host `claude`, installation `pixl-kit`): kit present, bundle manifest
**verified**, 256 files checked, no issues; Python 3.14.3, pillow 12.3.0, jsonschema 4.26.0,
referencing 0.37.0. Official PixelLab tools `not_observed`; `named_role not_observed` from static
files (the `.claude/agents/pixl.md` and `.claude/skills/pixl/SKILL.md` adapters are not present in
this consumer, which is expected: the skill was loaded through the plugin inventory). Manifest
verification means the payload bytes match the local manifest; publisher authenticity is not
established by it.

| Kit file | sha256 now | Previous caller record (`CALLER-RESULT-PREREQUISITES.json`) |
|---|---|---|
| `pixl-kit/bundle-manifest.json` | `cc38dcf31fa55f68866092b005f6fb790e20255ffb408cee89b1083dc4ef9354` | `fe355d44...` (changed) |
| `skills/pixl/references/delegation.md` (241 lines) | `43f086a02bf772df9f6f96342514f335aa65eef52af253746ac1d998a5da1b47` | `2ca298b9...` (changed; manifest lines 1415-1418 list `43f086a0...`) |
| `skills/pixl/references/intake-sample.md` (161 lines) | `55fe94fcdfaff27eff35fbb0a8cc56c2c2ddee95daafd14f062b4ee8e8a2b959` | `8da6141b...` (changed; manifest lines 1445-1448 list `55fe94fc...`) |
| `skills/pixl/SKILL.md` | `04a46dae9b55e5e54eec5b1a033e6e597f3e44170d930e96da3554289b34a5a2` | unchanged |
| `agents/pixl.md` | `34187821f9875c880e703588065ec62dc7a85e1a044b5c7565825c200b7b10b9` | unchanged |
| `runtime/pixl/request_review.py` | `af7bf5bf1f599a03645d12e6faadb14db050dec5a31eae067ed3fc36295a1c23` | unchanged |
| `runtime/pixl/lifecycle.py` | `5e37cefb2bcb357373332af4970b7c30df4e18df6d78e36022fe349a616a6a23` | unchanged |
| `skills/pixl/references/state-authority.md` | `4f883c6832d63a5e8ff134f69dbbf6d90abdc96c3004b39cae7aec6a87715112` | unchanged |
| `resources/agent/PROFILE.md` | `8aeaedb1f345af7f80d289f3f8372de00e20619ccf4ec685ed6db229c4d99265` | (not recorded before; listed for the next comparison) |

The manifest change is consistent with exactly those two reference files changing (the manifest
lists their current hashes and the readiness verification found no mismatch). The previous bytes
of the two files are not retained anywhere in this consumer, so a textual diff is not possible
here; what follows is read from the **current** text.

**Does anything in the current handoff depend on the changed references?** Yes, procedurally,
and nothing in it contradicts the current text:

- `intake-sample.md` "Check what an answer enables" (lines 70-129) is the procedure this note's
  operation-effect check follows: name the operation, task and phase; trace **T.op -> F.ct ->
  C.ch -> I**; inspect `other_intake`; for production/delivery account for prerequisites, raster
  contracts, confirmation of every linked choice and the adoption decision; project only the
  supplied answer; derive `question`, `necessary_for`, `unlocks`, `next`, `blocked_on` from the
  checked table (lines 106-108); reconcile literal conditions before publishing (lines 116-123).
- `intake-sample.md` "Cold intake handoff" (lines 131-159) prescribes the decision-table columns
  used below (line 142-143: choice, actual authority/status, whether an answer is needed now,
  effect) and the final-response rule (lines 154-159): when the necessary choices are already
  supplied, use them and state the next operation without asking again. For the sample, no owner
  answer is pending (table below), so this handoff asks no question of the owner and states the
  next operation and its missing capability inputs instead.
- `delegation.md` "Specialist -> caller at completion" (lines 134-154) gives the result fields
  (`status`, `artifacts`, `checks`, `request_review`, `provider`, `questions`/`next`) used in the
  returned result; line 150-153 keeps a planning-only increment free of manufactured production
  state and judges completion against the delegated scope. "Caller: review a cold continuation"
  (lines 71-132) is the caller's procedure for reading this note; step 3 (lines 96-108) and step 5
  (lines 118-132) are what the operation-effect section below is written to be checked against.
- Retained artifacts that cite these files: `sample-creative-brief-v2.json` line 100 cites
  "intake-sample.md, keep authority through derived rules" by section name; that heading is
  still present (line 11). `CALLER-RESULT.json` lines 93 and 105 cite `delegation.md:25-35` and
  `:21-23` against the two-versions-old hash `a147f5c8...`; in the current file lines 21-23 are
  still the PLAR hand-over / native-delegation paragraphs and lines 25-35 the reassess-or-correct
  paragraph, so those citations still land on the same subjects. No retained artifact depends on
  a line of either file that the current text lacks.

## Re-verified this increment (observed, not asserted)

- `pixl_validate`, `pixl_workflow`, `pixl_ready`, `pixl_jobs`, focused `pixl_context`
  (`t_sample`, authoring view) and `pixl_readiness` on the current root: values in the two tables
  above.
- `work/verify_rev11.py` with `-I`: `problems []`.
- sha256 of every file named in this note was computed in this increment; the e note is
  `f174f93971f3044b9731aae34e2704d5e090c5468761361063548d15056d597f` (equals `s_continuation_6.dg`),
  `request-review-v2.json` `a596f02a...84d73`, `sample-creative-brief-v2.json` `f84b2628...a5b80`,
  `sample-criteria.json` `14c979ea...1834b`, `criteria-schema-validation.json` `93643a34...b16a`,
  `validate_criteria_v2.py` `b582f327...719b`, `sources/brief.md` `a78aca77...5324`,
  `sources/controlled-evaluation-answers.md` `87cf7eec...6e30`, `sources/reference-observations.md`
  `d0862d14...0495`; all equal the digests bound in the S records that name them.
- A sha256 snapshot of all 364 files under the consumer root was taken before any write
  (`work/rev12-protected-snapshot.sha256`); `work/verify_rev12.py` re-checks every entry except
  the two files this increment edits on purpose (`SESSION.md`, `state.px/state.px`).
- `validate_criteria.py` was **not** run; the v2 validator's print-only run inside the verifiers
  leaves the retained artifact unchanged.

## Decision table (re-derived from the revision 11 I records; every status unchanged)

Read from the `pixl_workflow` intake list and the focused `pixl_context` on `t_sample`, not copied
from the d note; the result is compared with the d note's table (lines 201-216) afterwards and
agrees row by row. "Answer needed now?" means: needed before `job-prepare` for `t_sample` /
`f_sample` against `c_sample`. An answer adopts only the choices it explicitly supplies; unasked
rows keep their status.

| Choice (record) | Actual authority / saved status | Answer needed now? | Effect / where it binds |
|---|---|---|---|
| Outline (`i_outline`) | Owner for the project; **proposed** (sample-scoped controlled-evaluation confirmation, `s_eval_answers` line 5; reference-b alternative preserved in `wy`) | No; already composed into `c_sample.li` component 3 | Brief component 3a-3c; `q_sample_outline` (visual). Family treatment still the owner's. |
| Canvas (`i_canvas`) | Owner; **proposed** `[32, 32]` (sample-scoped, `s_eval_answers` line 6; owner explicitly has not chosen, `s_brief` line 23) | No; pins `C.px` | Brief hard constraint; `q_sample_canvas`. Production canvas still the owner's. |
| Palette (`i_palette`) | Owner; **observed** three measured colours | No; pins `C.pl` | Brief working palette; `q_sample_palette` exclusivity is a sample working rule. Confirmation coupled to `i_role_diff`. |
| View (`i_view`) | Owner; **confirmed** `side` (`s_brief` line 19) | Settled | Pins `C.vw`; `q_sample_readability`. |
| Sampling (`i_sampling`) | PIXL proposal; **proposed** `nearest` | No; pins `C.sa`; a delivery rule, not a generation parameter | Brief delivery rule; `pixl_inspection_prepare` views. |
| Alpha (`i_alpha`) | Observation; **observed** `binary` | No; pins `C.al` | Brief hard constraint; `q_sample_canvas`. |
| Lighting (`i_lighting`) | Observation; **observed** flat | No; composed into `c_sample.li` component 1 | Brief component 1. |
| Design language (`i_design_language`) | PIXL proposal; **proposed** | No; the sample trials it | Brief component 2 and landmarks (component 4). Owner can override; landmarks then follow. |
| Game backgrounds (`i_backgrounds`) | Owner; **unresolved** (unlinked `other_intake`) | No; before **visual review** it replaces the specialist's light/dark/busy test set | Named in the `q_sample_readability` check text. |
| Display scale (`i_display_scale`) | Owner; **unresolved** (unlinked) | No; before **visual review** (target integer zoom) | `q_sample_readability`, `q_sample_outline` zoom; inspection view scales. |
| Role differentiation (`i_role_diff`) | Owner; **unresolved** (unlinked) | No; the sample carries no role device by plan | Before scout/medic production; may reopen palette exclusivity. |
| Animation (`i_animation`) | Owner; **unresolved** (unlinked) | No; the sample is one static sprite by plan | Before scout/medic production: output kinds and operation choice. |
| Engine (`i_engine`) | Owner; **unresolved** (unlinked) | No | `q_engine_import` on `f_family` stays unavailable. |
| Roster (`i_roster`) | Owner; **confirmed** `[scout, medic]` | Settled | None for the sample. |

No row changed status or value in this increment (record hashes of all 14 I records are those
listed by `pixl_validate` for revision 11 and are byte-identical in revision 12).

## Operation-effect check: the next operation is `job-prepare` for `t_sample`

Operation: `pixl_job_prepare` / `job-prepare state.px JOB t_sample REQUEST_JSON --outputs f_sample
--expect HASH --root <this consumer root>`. Task `t_sample`, phase `sample`, output `f_sample`
(kind `sprite`), contract `c_sample`. Gates read from the current kit code
(`runtime/pixl/lifecycle.py` lines 44-77, `runtime/pixl/jobs.py` lines 717-743,
`runtime/pixl/platform.py` lines 866-889 and 1017-1023) and evaluated against revision 11:

| Gate (code) | Current state | Result |
|---|---|---|
| `job_exists`: JOB not already a record | no J records exist | passes for any new ID (for example `j_sample_1`) |
| `job_outputs`: outputs within `T.op` | `t_sample.op = [f_sample]` | passes for `--outputs f_sample` |
| `task_prerequisite` (`T.dp` all done) | `dp [t_study]`, `t_study` done | passes |
| `output_contract` (raster F has `ct`) | `f_sample.ct = c_sample` | passes |
| `choice_unresolved` / `choice_conflict` over `C.ch` | `c_sample.ch` = `i_canvas` proposed, `i_palette` observed, `i_view` confirmed, `i_sampling` proposed, `i_alpha` observed, `i_lighting` observed, `i_outline` proposed, `i_design_language` proposed | passes: none unresolved or in conflict |
| `task_decision`, `method_poc`, `choice_unconfirmed` | apply only to `ADOPTION_PHASES = {production, delivery}`; `t_sample.ph = sample` | not applicable |
| family blockers / plan blockers | no families, no connected plans | none |
| `job_pending` (another attempt on `f_sample`) | `pixl_jobs []` | passes; a new request duplicates nothing |
| `--expect` | revision 11 hash now; revision 12 hash after this commit | available (`SESSION.md`, caller return) |

So the state-side gates are all satisfied; `pixl_workflow` reporting `t_sample` blockers `[]`
is the same conclusion. What the operation still consumes, and which of it exists:

| `job-prepare` input | Status now |
|---|---|
| `STORE` = `state.px`; `TASK` = `t_sample`; `--outputs f_sample`; `--root` = the current consumer root | available |
| `--expect` = the then-current canonical hash | available after this commit |
| `JOB` = a new job ID | chosen at preparation |
| `provider` = identity text of the actual connected PixelLab service | **missing**: no official PixelLab tool observed in this host (`pixl_readiness`) |
| `tool` = the chosen operation's actual declared name | **missing**: decided from the live declaration; `operation-shortlist.json` is a dated catalog and decides nothing |
| `schema` = the full live `inputSchema` object (arguments are validated against it, line 889) | **missing**: `pixl_capabilities` is a dated inventory, not the live schema |
| `arguments` = exact provider arguments, a JSON object, no secrets | **missing**: translated from `sample-creative-brief-v2.json` once the tool and schema are known; `reference.png` (`d997cade...70aa7`, role style) travels as an actual image input (upload handle / URL / ID), not a filename in a prompt; reviewed through a successor packet with `request.kind provider_arguments` that `pixl_request_review` can consume (`request_review.py` lines 130-134 reject the current `creative_brief` kind) |
| `discovery` = `{source: text, observed_at: ISO timestamp not in the future, evidence: nonempty object}` | **missing**: requires the live tool listing and a host-clock timestamp |
| `authorization` = `{scope: text, evidence: nonempty object}` | `scope` text available (brief: "make the progress possible in this session" for the sample; evaluation answers bind the sample only); **`evidence` object and cost coverage missing**, to be supplied by the caller/host |

Every missing input is a **capability or caller input**, not an owner art decision. Therefore:
`blocked_on` = the host's authenticated PixelLab connection (tool declaration and schema), the
image transport handle for `reference.png`, the discovery evidence and the authorization evidence;
`necessary_for` of each open I record is **not** `job-prepare`. After preparation the sequence is
unchanged from the d note (lines 249-255): caller comparison of the saved request with the packet,
`job-dispatch` (single claim), one host call, `job-observe`, `job-import` as an unaccepted X for
`f_sample`, then mechanical E/V for `q_sample_canvas` and `q_sample_palette` via the local harness
and `pixl_candidate_review`, and visual E/V for the three visual criteria via
`pixl_inspection_prepare` / `pixl_inspection_review`, which need `i_display_scale` and benefit
from `i_backgrounds`. Those two unresolved choices gate **visual review**, the operation two steps
after `job-prepare`; they do not gate preparation and no earlier artifact claims otherwise.

## What later production still needs (unchanged; listed so nothing is dropped)

- `t_sample` done: a nominated candidate passing all five `f_sample.rq` criteria.
- Owner answers (not sample-blocking): final outline treatment for the family, final canvas,
  role-differentiation device (and with it the palette confirmation, possibly a reserved accent),
  animation requirements, target backgrounds, display scale, engine/importer.
- Raster contracts for `f_scout` / `f_medic` whose linked choices are **confirmed** (production
  phase `choice_unconfirmed` gate), evidence-backed `D` records with executed proofs for `t_scout`,
  `t_medic`, `t_family`, and the family baseline / continuity plan per the family-delivery operation.
- `q_engine_import` on `f_family` remains unavailable until `i_engine` is answered.

## Files added or edited this increment (consumer-relative, sha256)

| Path | sha256 | Role |
|---|---|---|
| `work/rev12-protected-snapshot.sha256` | `028eda400c0eb03e159e044479c3d4b172ced794c528f3a0562370eb164aedc2` | sha256 of all 364 pre-existing files, taken before any write; read by the verifier |
| `work/build_rev12.py` | `7b3ccb09a49bd83395e119c7ac05ac6f9467bfb6820ba1f0694385fa738b2781` | revision 12 builder (decode head, append 2 records, encode) |
| `work/verify_rev12.py` | `eaf428713144b2ea347c1c6f444b4dd416979a5b33078032f46891b8c1a5c50a` | revision 12 verifier, read-only; also proves protected files unchanged |
| `work/rev12.json`, `work/rev12.px` | produced by the builder; `rev12.px` bytes equal the committed head | candidate document and wire |
| `deliverables/continuation-2026-11-15f.md` | bound by `s_continuation_7` | this note |
| `SESSION.md` | edited; hash in the caller return | current-session pointer (new root, revision 12) |

Nothing else was written. The hashes of `rev12.json`, `rev12.px` and `SESSION.md` cannot appear
here because they are produced after this note is final; the caller return lists them.

## Records added in revision 12 (11 -> 12 delta)

| Record | Kind | Content |
|---|---|---|
| `s_continuation_7` | S (new) | `ur deliverables/continuation-2026-11-15f.md`, `dg` = this note's sha256, `ln [1, N]` with its actual line count, `at 2026-11-15`, `au local` |
| `handoff_8` | N (new) | `wh actor`; `rv 12`; `nx [t_sample]`; `bl [t_scout, t_medic, t_family]`; `fo` = `s_continuation_7`, `s_continuation_6`, `s_sample_brief_v2`, `s_sample_request_review_v2`, `s_sample_criteria`, `s_sample_brief`, `s_sample_request_review`, `s_eval_answers`, `c_sample`, `f_sample`, every I record whose status is not `confirmed` in state order (`i_alpha`, `i_animation`, `i_backgrounds`, `i_canvas`, `i_design_language`, `i_display_scale`, `i_engine`, `i_lighting`, `i_outline`, `i_palette`, `i_role_diff`, `i_sampling`), `x_aid`, `x_study` |

Header `PX2 11 -> PX2 12`. Nothing else: all 80 revision 11 records byte-identical (verified
against `work/rev11.json`). The `fo` rule differs from `handoff_7` only by adding the three
non-confirmed records it omitted (`i_sampling` proposed, `i_alpha` and `i_lighting` observed) so
that no observed or proposed policy pinned by `c_sample` can silently read as confirmed.

## Preserved and unchanged

All earlier reports, evidence, review files, state history copies (13 after this commit),
`work/` builders and verifiers for revisions 2-11, the research candidates and verdicts,
`handoff` through `handoff_7`, every source byte, both references, `pixl-kit/`,
`CALLER-RESULT*.json`, the caller's `work/caller-restore-validation.py`, every
`deliverables/*.md` and `deliverables/sample-request/*` file. `SESSION.md` is again the only
pre-existing file edited.
