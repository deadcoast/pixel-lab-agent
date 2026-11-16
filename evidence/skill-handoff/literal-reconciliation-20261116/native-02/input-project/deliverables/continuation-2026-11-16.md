# Continuation note, 2026-11-16: handoff-only continuation under a new consumer root; kit changed again

This increment retains the prepared work, re-inspects the actual current state and the artifacts the
revision 13 handoff relies on, and saves a current, self-contained continuation for the next session.
It is a **handoff-only increment**: no request packet, criteria v2 file, fixture, harness run,
generation, provider, candidate, verdict, evidence, intake-status or task-state work was assigned or
performed. The contract `c_sample`, the five sample criteria, every I record, every T state and every
retained file keep their bytes. The only production-state change is the addition of this note's S
record and a new N record (revision 14, below). No owner answers were supplied in this invocation and
none are invented; the controlled-evaluation answers (`sources/controlled-evaluation-answers.md`
`87cf7eec...6e30`, lines 5-6, scope statement line 8) remain applied within their sample scope.

The previous notes stay source evidence. Which of their sections remain applicable is named in the
section "Earlier notes: what remains applicable" at the end; nothing in them is adopted wholesale.

## Consumer-root change

| | Root | Revisions committed there | Notes |
|---|---|---|---|
| Current (this increment) | `C:/Users/ryanf/AppData/Local/Temp/pixl caller review 9f6e7c37402f4037acf44abe70f04834/consumer` | 13 -> 14 | this note |
| Previous (provenance) | `.../pixl caller review a97de5914a21428aad2fef3c65ecfcec/consumer` | 11 -> 12 -> 13 | f (`continuation-2026-11-15f.md`), g (`-15g.md`); caller files `CALLER-RESULT-PREREQUISITES-02.json`, `review/caller-comparison-2026-11-15-v5.md` |
| Earlier (provenance) | `.../pixl caller review e3c7ebe124824b69828309bf1645f322/consumer` | 9 -> 10 -> 11 | d, e; `CALLER-RESULT-PREREQUISITES.json` |
| Earlier (provenance) | `.../pixl caller review d31ffb17787d4358adda6c5e32024830/consumer` | 8 -> 9 | c; `CALLER-RESULT-ANSWER-STATE.json` |
| Earlier (provenance) | `.../pixl caller review ca2b0073ba6c4da79a6c306380a10742/consumer` | 6 -> 7 -> 8 | 2026-11-15, 2026-11-15b; `CALLER-RESULT.json` |
| 2026-11-14 session (root not recorded in a retained caller result) | unknown | 5 -> 6 | `continuation-2026-11-14.md` |
| Predecessor, 2026-09-14 | kit at `.agents/skills/pixl-kit`, interpreter `.../pixel-lab-docsuite/.venv/...` | 1-5 | `sources/brief.md` lines 11-15 |

Every absolute path inside a retained file (`SESSION.md` before this edit, `CALLER-RESULT*.json`,
earlier notes, `review/*.md`, `work/` scripts, `sources/brief.md` session constraints) is provenance of
the session that wrote it, not a current location. All consumer-relative paths and all S-record
`ur`/`dg` bindings resolve unchanged under the new root: `pixl_validate` reports `files_verified true`
with the root relocated. The kit path (`pixl-kit/` inside the consumer root), the interpreter
(`C:/github/pixel-lab-agent/.venv/Scripts/python.exe`) and the runner (`pixl-kit/scripts/pixl.py`) are
the same layout as the previous four roots, but the kit **contents** changed (next section).

## State identity on entry (observed in this increment)

| Item | Observed |
|---|---|
| `state.px/state.px` | PX2, revision 13, 84 records, valid, `files_verified true` |
| Canonical state hash (= head sha256 = `state.px/history/42db4c75....px` = `work/rev13.px`) | `42db4c758d328c521c1f73baae1873b56b14e8a4d4d1b580c1d720dcecd8acd2` |
| `pixl_ready` | `[t_sample]` |
| `pixl_jobs` | `[]` (no prepared, unknown, submitted or running attempt; `remote_executed false`) |
| `pixl_workflow` blockers | `t_sample` none; `t_scout`, `t_medic`: `t_sample` open, output needs a raster contract, task needs an adoption decision; `t_family`: `t_scout` and `t_medic` open, needs an adoption decision; `t_aid`, `t_study` done |
| Head N record | `handoff_9` (rv 13) |
| Families / connected plans | none |
| History copies | 14 (`PX2 0..13`) |
| `work/verify_rev13.py` (run with `-I` on the head) | exit 1 with 20 problems, **all kit-identity entries** (explained below); no record, binding, handoff or retained-project-file problem |

## State identity on exit

Revision 14, 86 records (84 + `s_continuation_9` + `handoff_10`), committed to the store folder
`state.px` with expected hash `42db4c75...8acd2`. The revision 14 canonical hash is not written here
because this note's digest is bound inside it; read it from `state.px/state.px`, `SESSION.md` or the
caller return. Expected after commit (checked by `work/verify_rev14.py`): ready `[t_sample]`,
blockers unchanged, no jobs, all 84 revision 13 records byte-identical.

## Kit identity observed now

`pixl_readiness` (host `claude`, installation `pixl-kit`): kit present, bundle manifest **verified**,
256 files checked, no issues; Python 3.14.3, pillow 12.3.0, jsonschema 4.26.0, referencing 0.37.0.
Official PixelLab tools `not_observed`, authentication `not_verified`; `named_role not_observed` from
static files (the `.claude/agents/pixl.md` and `.claude/skills/pixl/SKILL.md` adapters are absent in
this consumer, expected for plugin loading). Manifest verification means the payload bytes match the
local manifest; publisher authenticity is not established by it. The kit directory holds 257 files
(256 manifest-listed plus the manifest itself) and **no** `__pycache__` directory.

### Changed kit files (sha256 measured in this increment)

| Kit file | Previous (f note lines 61-63, caller result 02 lines 63-64, 72) | Now | Lines before -> now |
|---|---|---|---|
| `pixl-kit/bundle-manifest.json` | `cc38dcf31fa55f68866092b005f6fb790e20255ffb408cee89b1083dc4ef9354` | `e1fb00650c4526b26584aae83b7989ff3d56892045bfb1fe2e975598968dd398` | n/a |
| `pixl-kit/skills/pixl/references/delegation.md` | `43f086a02bf772df9f6f96342514f335aa65eef52af253746ac1d998a5da1b47` | `2f5af8b5339daaef3402eacb5fc532a0123cafeb0b8b2c5fc990c1221ab5bdc5` | 241 -> 245 |
| `pixl-kit/skills/pixl/references/intake-sample.md` | `55fe94fcdfaff27eff35fbb0a8cc56c2c2ddee95daafd14f062b4ee8e8a2b959` | `b24dad8e654215d04b3229b3d7b08b2c06b32cb1442cdf53c49b066776fe47f6` | 161 -> 188 |

Unchanged by hash (measured now, equal to the f note / caller result 02 values): `skills/pixl/SKILL.md`
`04a46dae9b55e5e54eec5b1a033e6e597f3e44170d930e96da3554289b34a5a2`; `agents/pixl.md`
`34187821f9875c880e703588065ec62dc7a85e1a044b5c7565825c200b7b10b9`; `resources/agent/PROFILE.md`
`8aeaedb1f345af7f80d289f3f8372de00e20619ccf4ec685ed6db229c4d99265`;
`skills/pixl/references/state-authority.md` `4f883c6832d63a5e8ff134f69dbbf6d90abdc96c3004b39cae7aec6a87715112`;
`runtime/pixl/lifecycle.py` `5e37cefb2bcb357373332af4970b7c30df4e18df6d78e36022fe349a616a6a23`;
`runtime/pixl/jobs.py` `18d543f7d81134b46c5282728be7e7681c94789c554a9f6e3abe0f882c92ecc3`;
`runtime/pixl/platform.py` `7693533dea30d9027cd7f89b47629227b87b18f23e993ae6eab848cb78efbea0`;
`runtime/pixl/request_review.py` `af7bf5bf1f599a03645d12e6faadb14db050dec5a31eae067ed3fc36295a1c23`.
The previous bytes of the three changed files are not retained anywhere in this consumer, so a textual
diff is not possible; the re-map below compares the f note's description of the old text with the
current text.

### Citation re-map into the two changed reference files (old line -> current line)

The g note (`001065a3...2e4f`) cites no kit file by line (checked by search). The f note's citations
are at its lines 79-103. Caller files that repeat the old numbers are listed afterwards for the
caller's own records; they are not edited.

| f note line | Old citation (as the f note describes it) | Current location | Status of the subject |
|---|---|---|---|
| 79 | `intake-sample.md` "Check what an answer enables", lines 70-129 | lines 70-157 (heading still line 70) | Same subject; lines 70-105 carry the same procedure (name operation/task/phase; trace T.op -> F.ct -> C.ch -> I; `other_intake`; production/delivery prerequisites; project only the supplied answer). A **new** subsection "Write the current effect before the return" occupies 106-157 |
| 84 | lines 106-108: derive `question`, `necessary_for`, `unlocks`, `next`, `blocked_on` from the checked table | lines 142-145 (worksheet item 4) | Same subject, **reworded and tightened**: fields are built "from these fresh checked statements", and "Do not initialize their meaning from an old result's fields" |
| 84 | lines 116-123: reconcile literal conditions before publishing | lines 146-151 (worksheet item 5) | Same subject, **reworded and extended**: reopen the saved note and result, compare each carrier's words with the worksheet and source, correct the current version before returning. The unchanged-position text at 97-104 (project only the supplied answer; rerun workflow before claiming readiness) also still covers it |
| 85 | "Cold intake handoff", lines 131-159 | lines 159-188 | Same subject, four numbered steps |
| 86 | lines 142-143: decision-table columns (choice, actual authority/status, answer needed now, effect) | lines 169-173 (step 2) | **Changed**: step 2 now prescribes saving the current-effect worksheet "in a new continuation note", with observed/proposed choices, their real authority, source and scope, and "unasked rows keep their status". The four-column decision-table prescription as the f note describes it is not in the current text; the current text does not forbid a decision table (line 97 still says "In the saved decision table, project only the supplied answer") |
| 87 | lines 154-159: final-response rule (when the necessary choices are already supplied, use them and state the next operation without asking again) | lines 181-186 (step 4) | Same subject, same rule |
| 91 | `delegation.md` "Specialist -> caller at completion", lines 134-154 | lines 138-158 (heading 138; result fields 146-152) | Same subject and fields (`status`, `asset_id`/`requirements_hash`, `artifacts`, `checks`, `request_review`, `provider`, `questions`/`next`) |
| 93 | lines 150-153: planning-only increment needs no manufactured production state; judge completion against the delegated scope | lines 154 and 156 | Same subject, same wording |
| 94-96 | "Caller: review a cold continuation", lines 71-132; step 3 at 96-108; step 5 at 118-132 | lines 71-136; step 3 at 100-113; step 5 at 122-136 | Same subject. Step 2 (86-98) **now names** "the specialist's current-effect worksheet" (line 88, linking to `intake-sample.md#write-the-current-effect-before-the-return`) as the proposed claim set the caller reads independently |
| 98 | `intake-sample.md` line 11 heading "Keep authority through derived rules" (cited by `sample-creative-brief-v2.json` line 100 by section name) | line 11 | Unchanged |
| 99-102 | `delegation.md` lines 21-23 (PLAR hand-over, native delegation) and 25-35 (reassess-or-correct paragraph), cited by `CALLER-RESULT.json` lines 93 and 105 | lines 21-23 and 25-35 | Unchanged subjects, read in this increment |

Runtime citations in the f note (lines 156-158, 183) land unchanged, re-read now: `lifecycle.py` 44-77
(`_activation_blockers`; `ADOPTION_PHASES` gates at 65-75), `jobs.py` 717-743 (`prepare()`:
`job_exists` 732-734, context 735, blockers 736-737, pending 738, `prepare_discovered` 739-741),
`platform.py` 869-889 (identity, arguments object, discovery/authorization fields, nonempty evidence,
no secrets, schema validation) and 1017-1023 (`observed_at` not in the future), `request_review.py`
132 (`kind == "provider_arguments"`).

Caller-authored files carrying the old numbers (retained, not mine): `CALLER-RESULT-PREREQUISITES-02.json`
lines 63-64 (`delegation.md` 71-132 / 134-154 / 150-153; `intake-sample.md` 70-129 / 106-108 /
116-123 / 131-159 / 141-143 / 154-159) and `review/caller-comparison-2026-11-15-v5.md` lines 40-41,
65-66 and 73. Line 73 of v5 quotes old `intake-sample.md` line 143 ("observed and proposed policies
... cannot silently gain confirmation"); that phrase is **absent** from the current file; its meaning is
carried by current lines 129 ("Keep every unasked choice unchanged") and 171 ("unasked rows keep their
status"). v5 line 122 cites `delegation.md` 28-35, which still lands in the unchanged 25-35 paragraph.

### Dependence statement

- **Nothing in the current handoff depends on text the current kit lacks.** Every subject the f and g
  notes rely on (operation-effect procedure, final-response rule, completion fields, planning-only
  scope rule, PLAR/native-delegation paragraphs, reassess-or-correct paragraph, the "keep authority"
  heading, all runtime gates) is present in the current text at the re-mapped lines. The one
  prescription that is gone, the four-column decision table as the f note describes old lines 142-143,
  was a layout; the decision table in this note is kept as a specialist layout under current line 97
  and is not an owner requirement or a kit requirement.
- **The current kit adds requirements the f and g notes do not satisfy by themselves**, which this
  note supplies: (1) `intake-sample.md` 106-126 and 169-170: a current-effect worksheet saved inside
  the new continuation note (section below); the f and g notes contain no worksheet. (2) 142-145:
  the authored `next` / `blocked_on` / `questions` fields of this increment's return are built from
  the worksheet rows, not from `CALLER-RESULT-PREREQUISITES-02.json` `next_action` / `remaining_questions`.
  (3) 146-151: the carrier check (section "Carrier check") was performed on this note and the return
  before returning. (4) `delegation.md` 86-98: the caller's step 2 now reads the worksheet as the
  claim set; this note's worksheet is written to be read that way.
- The runtime files that enforce the next operation's gates are unchanged by hash, so the gate
  evaluation below is not affected by the kit change.

## Current-effect worksheet (as `intake-sample.md` lines 112-126 prescribe)

```text
Current operation and answer effects
State/plan identity: state.px/state.px, PX2 revision 13, canonical 42db4c758d328c521c1f73baae1873b56b14e8a4d4d1b580c1d720dcecd8acd2 on entry (revision 14 after this commit; read its hash from the head, SESSION.md or the caller return). Plan traced: T t_sample (ph sample, st open, dp [t_study] done, op [f_sample], ca [], dc [], kn []) -> F f_sample (kd sprite, ct c_sample, rq [q_sample_canvas, q_sample_palette, q_sample_outline, q_sample_readability, q_style_match]) -> C c_sample (record b7f77964...7737; px [32,32], pl [#56B5BC, #F4DDA2, #25354A], vw side, sa nearest, al binary) -> ch [i_canvas proposed, i_palette observed, i_view confirmed, i_sampling proposed, i_alpha observed, i_lighting observed, i_outline proposed, i_design_language proposed]. other_intake: i_animation, i_backgrounds, i_display_scale, i_engine, i_role_diff unresolved; i_roster confirmed.
Operation and phase: pixl_job_prepare (CLI: job-prepare state.px JOB t_sample REQUEST_JSON --outputs f_sample --expect <current hash> --root <this consumer root>); task t_sample, phase sample, output f_sample, contract c_sample.
Question (or "no owner answer needed for this operation"): no owner answer needed for this operation.
Assume only this answer: none is supplied or assumed; every I record keeps its status, value and scope.

Prerequisite or permitted alternative | Source + locator | Current status | After only this answer | Still required
R1 job_exists: JOB is not an existing record | pixl-kit/runtime/pixl/jobs.py 732-734 | satisfied for any new ID: no J record exists (pixl_validate record list; pixl_jobs []) | unchanged | choose a new ID at preparation (for example j_sample_1)
R2 job outputs lie within T.op | jobs.py 735 (_context); t_sample.op [f_sample] (pixl_context authoring view) | satisfied for --outputs f_sample | unchanged | none
R3 task_prerequisite: every T.dp done | lifecycle.py 49-52; t_sample.dp [t_study], t_study.st done | satisfied | unchanged | none
R4 output_contract: raster F has ct | lifecycle.py 53-56; f_sample.ct c_sample | satisfied | unchanged | none
R5 choice_unresolved / choice_conflict over C.ch | lifecycle.py 57-64; c_sample.ch statuses from pixl_workflow intake: 4 proposed, 3 observed, 1 confirmed, 0 unresolved, 0 conflict | satisfied | unchanged | none
R6 task_decision, method_poc, choice_unconfirmed | lifecycle.py 65-75: applied only when T.ph in ADOPTION_PHASES (production, delivery); t_sample.ph sample | not applicable to this operation | unchanged | none for the sample (they apply to t_scout, t_medic, t_family later)
R7 family / connected-plan blockers | lifecycle.py 76 (families.blockers); pixl_workflow: no families, no plans; pixl_context plans [] | none | unchanged | none
R8 job_pending: no other attempt on f_sample | jobs.py 738 (_pending); pixl_jobs [] | satisfied | unchanged | none
R9 --expect = current canonical hash | jobs.py 731 (_load with expected); state-authority.md 13 | available: revision 14 hash after this commit (SESSION.md, caller return, pixl_validate) | unchanged | reread the head immediately before the call
R10 provider = identity text of the connected PixelLab service | platform.py 869 (_request_identity) | MISSING: official PixelLab tools not_observed, authentication not_verified (pixl_readiness official_pixellab) | unchanged | the host's authenticated PixelLab connection
R11 tool = the chosen operation's declared name | platform.py 870 | MISSING: must come from the live declaration; deliverables/sample-request/operation-shortlist.json is a dated catalog and decides nothing (readiness.md; pixl_capabilities is "not live tool discovery") | unchanged | live tool listing in the host
R12 schema = the full live inputSchema object | platform.py 888-889 (_schema_no_secrets, _validate_schema) | MISSING | unchanged | live declaration
R13 arguments = exact provider arguments (JSON object, no secrets, valid under R12) | platform.py 871-872, 887, 889; PROFILE.md 44 (a filename in a prompt is not an uploaded reference); request_review.py 132 (packet kind provider_arguments) | MISSING: to be translated from sample-creative-brief-v2.json (f84b2628...a5b80) once R11/R12 are known, with reference.png (d997cade...70aa7, role style) as an actual image input (upload handle / URL / owned ID) | unchanged | R11, R12, image transport handle; then the provider_arguments successor packet, including the criteria-v2 supersession of sample-criteria.json (g note lines 61-72: q_sample_readability brief source lines [20,20], optionally [5,5], five check texts unchanged, validated with validate_criteria_v2.py --out <fresh work/ path>, bound as a new S beside s_sample_criteria), pixl_request_review on that packet, and the caller's request/criteria comparison (delegation.md 69; request-review.md)
R14 discovery = {source text, observed_at ISO timestamp not in the future, evidence nonempty object} | platform.py 873, 875-876, 878-885; 1018-1023 | MISSING | unchanged | live tool listing plus a host-clock timestamp
R15 authorization = {scope text, evidence nonempty object} | platform.py 874, 877, 878-885 | scope text AVAILABLE (brief.md lines 6-7 "Begin the project and make the progress possible in this session"; P.br); evidence object MISSING | unchanged | caller/host supplies the evidence object, including coverage of the cost of one call
A1 Route alternative: authenticated official PixelLab MCP tool surface (primary) OR the optional HTTP adapter explicitly selected for its documented operation | SKILL.md ("Production uses the official paid PixelLab API, preferring the authenticated MCP tool surface. The optional HTTP adapter is a separate explicitly selected route"); PROFILE.md 32 | neither observed in this host | unchanged | one of the two, selected by the caller/host; not an owner decision
A2 First-candidate path alternative: record-level job-prepare OR pixl_plar_prepare for a selected PLAR asset | intake-sample.md 25; SKILL.md PLAR paragraph | no plar.txt exists in this consumer, so the PLAR route is not available here; job-prepare is the route | unchanged | none (job-prepare)
A3 Visual-review inputs: owner i_display_scale and i_backgrounds OR the specialist's light/dark/busy test set | q_sample_readability.ck (record 541b9a97...acd4); i_backgrounds.wy; i_display_scale.wy | both unresolved; the test set is the authorized fallback for backgrounds ("the specialist's test set until i_backgrounds is answered"); no default exists for the target integer zoom | unchanged | before pixl_inspection_prepare / pixl_inspection_review of a returned candidate (two steps after job-prepare); not before job-prepare

Current effect sentence: No owner answer is pending for the sample and no state-side gate blocks job-prepare for t_sample / f_sample against c_sample (R1-R9 satisfied or not applicable, the same conclusion as pixl_workflow blockers []); the operation is still not executable locally now, because R10-R15 (provider identity, tool name, live inputSchema, exact arguments with an actual image input for reference.png, discovery evidence with a host-clock timestamp, authorization evidence) are capability or caller inputs that no local file supplies, and R13 additionally requires the provider_arguments successor packet with the criteria-v2 supersession and the caller's comparison before preparation.
Remaining prerequisites: R10, R11, R12, R13 (including the successor packet, criteria v2 and caller comparison), R14, R15 evidence object.
Authorized default/alternative (or none established): A1 is a caller/host selection between two source-permitted routes; A2 is fixed to job-prepare in this consumer; A3: the specialist's test backgrounds are an authorized fallback, the display scale has no default and is needed before visual review only. No default exists for R10-R12, R14 or the R15 evidence object.
Current carriers: note sections "Current-effect worksheet", "Decision table" and "What later production still needs"; authored result fields status, next.operation, next.blocked_on, next.missing_inputs, next.sequence_after_prepare, questions (empty for the owner on the sample); final wording: "The next operation is job-prepare for t_sample / f_sample against c_sample. It is blocked only on capability inputs (the host's live PixelLab tool declaration and schema, an image transport handle for reference.png, discovery evidence and authorization evidence) and on the provider_arguments successor packet with the criteria-v2 supersession and caller comparison; no owner answer is needed for this operation. i_display_scale is needed before visual review of a returned candidate, not before preparation."
Prior instruction superseded: (a) f note lines 79-103: its line citations into intake-sample.md and delegation.md are superseded by the re-map table above (kit changed; subjects stand). (b) f note line 137 and the bound packet locators ("brief.md line 19" for the side view): already superseded by g note finding 1 (line 20; verbatim line 5); still current and repeated in the decision table below. (c) work/verify_rev13.py as a current verifier for this root: superseded by work/verify_rev14.py; its exit 1 reflects the kit identity change and the absent bytecode cache only (section below) and it remains correct for the a97de591 root's kit. (d) f note lines 85-87 reliance on the old decision-table-column prescription (old intake-sample.md 142-143): the current kit prescribes this worksheet; the decision table is retained as a layout. (e) SESSION.md as written in the g round (2bf8396a...a92): superseded by the SESSION.md edited in this increment. (f) CALLER-RESULT-PREREQUISITES-02.json next_action / remaining_questions and g note "Effect on the current handoff": source evidence for the last round; the current wording is the effect sentence above (same conclusion, now carried with its rows).
```

### Carrier check (worksheet item 5, performed before returning)

Reopened after writing: this note's effect sentence, the decision table's "Answer needed now?" column,
the "What later production still needs" list and the return's `next` / `questions` fields were compared
with the rows. None promises more than R1-R9 (a usable local plan and satisfied state gates; not
preparation, not readiness for dispatch, not acceptance), none omits R10-R15, and none turns A1 or A3
into a prerequisite of `job-prepare`. The `questions` field carries no owner question for the sample;
the owner answers listed under later production are explicitly not sample-blocking.

## Decision table (re-derived from `pixl_workflow` intake and the focused `pixl_context`; every status unchanged)

"Answer needed now?" means needed before `job-prepare` for `t_sample` / `f_sample` against `c_sample`.
Record hashes are those listed by `pixl_validate` for revision 13; they are the same in revision 14.
Locators corrected per the g note: view = `sources/brief.md` line 20 (verbatim line 5); roster = line 19.

| Choice (record, hash prefix) | Actual authority / saved status | Answer needed now? | Effect / where it binds |
|---|---|---|---|
| Outline (`i_outline`, `fac2007a`) | Owner for the project; **proposed** (sample-scoped controlled-evaluation confirmation, `s_eval_answers` line 5, scope line 8; reference-b alternative preserved in `wy`) | No; composed into `c_sample.li` component 3 | Brief component 3a-3c; `q_sample_outline` (visual). Family treatment still the owner's |
| Canvas (`i_canvas`, `ffa24f94`) | Owner; **proposed** `[32, 32]` (sample-scoped, `s_eval_answers` line 6; owner explicitly has not chosen, `s_brief` line 23) | No; pins `C.px` | Brief hard constraint; `q_sample_canvas`. Production canvas still the owner's |
| Palette (`i_palette`, `0c883c56`) | Owner; **observed** three measured colours | No; pins `C.pl` | Brief working palette; `q_sample_palette` exclusivity is a sample working rule. Confirmation coupled to `i_role_diff` |
| View (`i_view`, `0fcd4280`) | Owner; **confirmed** `side` (`s_brief` line 20; verbatim line 5) | Settled | Pins `C.vw`; `q_sample_readability` |
| Sampling (`i_sampling`, `97393056`) | PIXL proposal; **proposed** `nearest` | No; pins `C.sa`; a delivery rule, not a generation parameter | Brief delivery rule; inspection views |
| Alpha (`i_alpha`, `394eb547`) | Observation; **observed** `binary` | No; pins `C.al` | Brief hard constraint; `q_sample_canvas` |
| Lighting (`i_lighting`, `1a704f2b`) | Observation; **observed** flat | No; composed into `c_sample.li` component 1 | Brief component 1 |
| Design language (`i_design_language`, `0208e12a`) | PIXL proposal; **proposed** | No; the sample trials it | Brief component 2 and landmarks (component 4). Owner can override; landmarks then follow |
| Game backgrounds (`i_backgrounds`, `291a2f03`) | Owner; **unresolved** (unlinked `other_intake`) | No; before **visual review** it replaces the specialist's light/dark/busy test set (A3) | Named in the `q_sample_readability` check text |
| Display scale (`i_display_scale`, `8b73da53`) | Owner; **unresolved** (unlinked) | No; before **visual review** (target integer zoom; A3) | `q_sample_readability`, `q_sample_outline` zoom; inspection view scales |
| Role differentiation (`i_role_diff`, `ebfa6ae1`) | Owner; **unresolved** (unlinked) | No; the sample carries no role device by plan | Before scout/medic production; may reopen palette exclusivity |
| Animation (`i_animation`, `d32f4475`) | Owner; **unresolved** (unlinked) | No; the sample is one static sprite by plan | Before scout/medic production: output kinds and operation choice |
| Engine (`i_engine`, `9a97eeba`) | Owner; **unresolved** (unlinked) | No | `q_engine_import` on `f_family` stays unavailable |
| Roster (`i_roster`, `83e52131`) | Owner; **confirmed** `[scout, medic]` (`s_brief` line 19) | Settled | None for the sample |

No row changed status or value in this increment. Compared row by row with the f note's table (lines
132-147): identical except the two locators the g note corrected.

## `work/verify_rev13.py` drift: what it means, and how `verify_rev14.py` handles kit files

`verify_rev13.py` (lines 114-124) treats **every** entry of `work/rev13-protected-snapshot.sha256` as
a protected file. That snapshot (388 entries, taken under the `a97de591` root) included the whole kit
and 17 `pixl-kit/runtime/pixl/__pycache__/*.cpython-314.pyc` bytecode files that the runner had
written there. Under this root the kit is a different version (three files changed, table above) and
no bytecode cache exists (the kit holds 257 files). Run here with `-I`, the verifier therefore reports
exactly 20 problems: `protected file drifted` for `pixl-kit/bundle-manifest.json`,
`skills/pixl/references/delegation.md` and `skills/pixl/references/intake-sample.md`, and `snapshot
file missing` for the 17 `.pyc` paths. Its other checks all passed in the same run: revision 13, 84
records, 82 revision 12 records unchanged, `s_continuation_8` binding, `handoff_9` fields, every
`RETAINED` hash, the g note's listed hashes, no revision 13 hash in the g note, every non-kit snapshot
entry unchanged, `validate_criteria_v2.py` print-only leaving the artifact unchanged, runner `workflow`
ready `[t_sample]` with files verified, `jobs` empty. **This is kit/environment drift between roots,
not project-state drift**; the caller's reading is confirmed from the verifier's code and output.

`work/verify_rev14.py` (read-only) keeps the same record, binding, handoff, retained-file, note,
validator and runner checks for revision 14, and changes the protected-file check as follows: the
pre-write snapshot `work/rev14-protected-snapshot.sha256` excludes `__pycache__` paths (381 entries:
124 non-kit, 257 kit); every non-kit entry is byte-checked except `SESSION.md` and the head; kit
entries are not byte-checked one by one. Instead the verifier records the manifest's sha256 from the
snapshot and now, runs the runner's `readiness --root . --host claude --installation pixl-kit` and
requires `bundle_manifest.status == "verified"` with no issues, and reports
`kit_changed_since_snapshot` and any differing kit paths as observations, not problems. A future kit
version change will therefore be visible in its output without making the project-state checks fail.

## What later production still needs (unchanged; restated so nothing is dropped)

- `t_sample` done: a nominated candidate passing all five `f_sample.rq` criteria (two mechanical/local
  via the harness under `work/sample-checks/` recorded through `pixl_candidate_review`; three
  visual via `pixl_inspection_prepare` / `pixl_inspection_review`, which need `i_display_scale` and
  benefit from `i_backgrounds`).
- Sequence after `job-prepare` (unchanged from the d note lines 249-255 and the f note lines 190-197):
  caller comparison of the saved request with the packet, `job-dispatch` (single claim), one host
  call, `job-observe`, `job-import` as an unaccepted X for `f_sample`, then the E/V above.
- Owner answers (not sample-blocking): final outline treatment for the family, final canvas,
  role-differentiation device (and with it the palette confirmation, possibly a reserved accent),
  animation requirements, target backgrounds, display scale, engine/importer.
- Raster contracts for `f_scout` / `f_medic` whose linked choices are **confirmed** (production-phase
  `choice_unconfirmed` gate, `lifecycle.py` 72-75), evidence-backed `D` records with executed proofs
  for `t_scout`, `t_medic`, `t_family` (`task_decision`, 66-67), and the family baseline / continuity
  plan per the family-delivery operation.
- `q_engine_import` on `f_family` remains unavailable until `i_engine` is answered.

## Files added or edited this increment (consumer-relative, sha256)

| Path | sha256 | Role |
|---|---|---|
| `work/rev14-protected-snapshot.sha256` | `e026a8df9b99afc130e893ed9861a7ef960ef48cb64d8712478e2b9d993ddc6f` | sha256 of all 381 files present before any write in this increment (`__pycache__` excluded; none existed); read by the verifier |
| `work/build_rev14.py` | `0595e7c5df5f0139cf87fc9405a6a292d5a3d82e80ba0738b4f34d091f7b1d4b` | revision 14 builder (decode head, append 2 records, encode) |
| `work/verify_rev14.py` | `e49ba11c72b7a6da5f2dad50237c7ec45e600f0ba553cfd5f3ed9cc7e4753e10` | revision 14 verifier, read-only; kit identity through the manifest (section above) |
| `work/rev14.json`, `work/rev14.px` | produced by the builder after this note is final; `rev14.px` bytes equal the committed head | candidate document and wire |
| `deliverables/continuation-2026-11-16.md` | bound by `s_continuation_9` | this note |
| `SESSION.md` | edited after the commit; hash in the caller return | current-session pointer (new root, revision 14, kit change) |

Nothing else was written. `validate_criteria.py` was **not** run; the v2 validator's print-only run
inside the verifier leaves `criteria-schema-validation.json` (`93643a34...b16a`) unchanged.

## Records added in revision 14 (13 -> 14 delta)

| Record | Kind | Content |
|---|---|---|
| `s_continuation_9` | S (new) | `ur deliverables/continuation-2026-11-16.md`, `dg` = this note's sha256, `ln [1, N]` with its actual line count, `at 2026-11-16`, `au local` |
| `handoff_10` | N (new) | `wh actor`; `rv 14`; `nx [t_sample]`; `bl [t_scout, t_medic, t_family]`; `fo` = `s_continuation_9` followed by `handoff_9`'s complete list (`s_continuation_8`, `s_continuation_7`, `s_continuation_6`, `s_sample_brief_v2`, `s_sample_request_review_v2`, `s_sample_criteria`, `s_sample_brief`, `s_sample_request_review`, `s_eval_answers`, `c_sample`, `f_sample`, the 12 non-confirmed I records in state order, `x_aid`, `x_study`) |

Header `PX2 13 -> PX2 14`. Nothing else: all 84 revision 13 records byte-identical (verified against
`work/rev13.json` by `verify_rev14.py`). Revision chain after this commit: 12 -> 13 -> 14 with record
counts 82 -> 84 -> 86; the 15th history copy is the revision 14 wire.

## Earlier notes: what remains applicable (named sections, not wholesale adoption)

- g note (`continuation-2026-11-15g.md`, `001065a3...`, `s_continuation_8`): **Finding 1** (line 20 /
  line 5 locator; criteria-v2 supersession as a required step of the `provider_arguments` successor
  packet) remains current and is carried in R13; **Finding 2** (per-root provenance table) remains
  current and is extended by one row in this note's root table; **Effect on the current handoff** is
  the same conclusion as this note's effect sentence and is superseded in wording only. Its state
  identity, files and records sections are history of revision 13.
- f note (`continuation-2026-11-15f.md`, `9e0df8a1...`, `s_continuation_7`): **Decision table** (lines
  124-150) remains applicable with the two g-note locator corrections and is re-derived above;
  **Operation-effect check** (152-197) remains applicable and is re-derived above as R1-R15 / A1-A3
  with current locators; **What later production still needs** (199-208) remains applicable and is
  restated above. **Kit identity observed now** (49-103) is superseded for hashes, line counts, line
  citations and the dependence statement by this note; **Consumer-root change** (11-26) is provenance;
  its state-identity, re-verified, files, records and preserved sections are history of revision 12.
- Earlier notes (2026-11-14 through 2026-11-15e) are source evidence only; the d note's sequence
  (lines 249-255) is restated above.

## Preserved and unchanged

All earlier reports, evidence, review files, state history copies (15 after this commit), `work/`
builders and verifiers for revisions 2-13, the research candidates and verdicts, `handoff` through
`handoff_9`, every source byte, both references, `pixl-kit/` (read-only; different version from the
previous root, recorded above), `CALLER-RESULT*.json`, `review/*`, the caller's `work/caller-*`
files, every `deliverables/*.md` and `deliverables/sample-request/*` file. `SESSION.md` is again the
only pre-existing file edited besides the head.
