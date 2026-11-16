# Continuation note, 2026-11-15 (e): corrections after caller review of revision 10

Same session, same isolation and same paths as `deliverables/continuation-2026-11-15d.md`
(retained unchanged, sha256 `826460e5ff96f7dae2bccff8b8df1278e5457614cfaadd3c0510e0f64feeb1dc`,
bound as `s_continuation_5`). The caller reviewed revision 10 independently, verified it
consistent on every claim it checked, accepted the S-record binding of the packet files and the
`deliverables/sample-request/` location, and returned two findings. Both are correct. This note
records the old-to-new correction for each, the files added, and the revision 11 delta. No
generation, provider job, candidate, evidence, verdict, task-state or intake change occurred.
The contract `c_sample`, the five sample criteria and `sample-criteria.json` are untouched.

## State identity on entry

- `state.px/state.px`: PX2, revision 10, canonical state hash
  `23f4ee559508bab7b1966348589c1431604b848b804f7e6599940e48b06968c6`, 76 records, valid, files
  verified. Ready `[t_sample]`, no jobs, no families. `handoff_6` current.
- Retained artifact `deliverables/sample-request/criteria-schema-validation.json` confirmed at
  its quoted hash `93643a34d32353b5471fd9943aed8bb3a0bf8cb48a94d8413c42635a1aaeb16a` after the
  caller's restore (caller script `work/caller-restore-validation.py`, sha256
  `603ede5e838eb8c76312c3666848dd4cd07f1ee68cb21edadb059ce909a64904`, not mine, not edited).

## State identity on exit

- Revision 11, 80 records (76 + `s_sample_brief_v2`, `s_sample_request_review_v2`,
  `s_continuation_6`, `handoff_7`), committed to the store folder `state.px` with expected hash
  `23f4ee55...68c6`. The revision 11 canonical hash is not written here (this note's digest is
  bound inside it); read it from `state.px/state.px`, `SESSION.md` or the caller return.
- Expected after commit: ready `[t_sample]`, blockers unchanged, no jobs.
  `work/verify_rev11.py` checks this against the committed head.

## Finding 1 (reproducibility defect): the v1 validator overwrote a hash-quoted artifact

**Old.** `deliverables/sample-request/validate_criteria.py` (sha256 `48f3d0f1...dbe45`) hard-codes
`OUT` to the retained `criteria-schema-validation.json` and writes it on every run, while its
docstring invites reviewers to run it to reproduce the validation. Doing so rewrites
`validated_at`, changing the artifact's hash, which is quoted in `request-review.json`
(bound `s_sample_request_review`) and in `continuation-2026-11-15d.md` line 141 (bound
`s_continuation_5`). The caller observed exactly this drift (to `82d7df80...765d5`) and
restored the original bytes.

**New.** `deliverables/sample-request/validate_criteria_v2.py` (sha256
`b582f32737eb5733f6be883c3e08b0ce9423408bb7249caa3b7c32d12011719b`): read-only by default
(prints the report); writes only to an explicit `--out` path; opens that path with mode `x`
and refuses to overwrite an existing file (exit 2); accepts `--criteria` / `--schema`
overrides. Demonstrated this session: print-only run (exit 0, `schema_valid true`,
`all_line_bounds_inside_files true`); `--out work/sample-checks/criteria-validation-rerun-v2.json`
(fresh file, sha256 `d22798dcafd78049d59576dc712edeffa48630388a244e7c7fb2bc20a45093bc`); a
second `--out` to the same path refused; the retained artifact still hashed `93643a34...` after
all three runs. `work/verify_rev11.py` repeats the print-only run and fails if the retained
artifact changes.

**Not changed.** `validate_criteria.py` and `criteria-schema-validation.json` keep their bytes:
the v1 script is retained as the one that produced the `93643a34...` artifact. **Instruction
for every reviewer and successor: reproduce the validation only with `validate_criteria_v2.py`;
do not run `validate_criteria.py`.** The v2 packet states the same.

## Finding 2 (mixed authority under one label): brief intent component 3 and wording rules

**Old** (`sample-creative-brief.json`, sha256 `cc21bf77...380ce`, bound `s_sample_brief`,
retained unchanged as the pre-discovery identity). Component 3, labelled "controlled-evaluation
sample confirmation", read: "Outlined as reference.png: a flat #25354A contour at the weight
shown there (2 logical px) fully enclosing the figure, which also forms the shoulder bar, the
base bar and the two solid top stalks, adapted to the side view. The outline colour is the only
dark value; no second outline tone, no selective outlining." The evaluation answer
(`sources/controlled-evaluation-answers.md` line 5) says only "Use the outlined treatment shown
in reference.png." The single-flat-colour fact is a measurement (`sources/reference-observations.md`
lines 37-40, line 40 "Outline is a single flat colour with no ramp"), and "only dark value /
no second outline tone / no selective outlining" is my provider-wording tightening. One label
covered three authorities. Less consequentially, component 1's "no gradients, no dithering"
lacked its locator (line 29, same observed class), and `provider_wording_rules` listed "no drop
shadow" without attributing it as a specialist choice.

**Chosen disposition: (a) a successor brief and packet, bound in revision 11.** Reason: the
brief is the exact text the future `provider_arguments` translation will read. A split recorded
only in a note would have to be re-applied by hand at translation time, which is the same
silent-carry risk the finding identifies; a v2 file makes the split the source. The v1 packet
remains the pre-discovery identity; nothing in it was edited.

**New** (`sample-creative-brief-v2.json`, sha256
`f84b262818bbf044eb22716ab5d02eed1103cc65714360fcfc5d9efd019a5b80`):

| Location | Old (v1) | New (v2) | Authority change |
|---|---|---|---|
| intent component 3 | one clause under "controlled-evaluation sample confirmation" | **3a** the evaluation answer's clause exactly as in `c_sample.li` (sample-scoped confirmation); **3b** what reference.png measurably shows: one flat colour `#25354A`, no ramp or second tone, 2 logical px (observation, lines 37-40); **3c** "no selective outlining; `#25354A` the only dark value; no second outline tone, no inner dark shading" (scoped specialist provider-wording choice, consistent with `c_sample.li` "fully enclosing"; revisable without touching `c_sample`) | none gains authority; the tightening is now attributed to the specialist |
| intent component 1 | "no gradients, no dithering" under observed, no locator for dithering | same text, citing `reference-observations.md` line 29 | none |
| `provider_wording_rules` | flat list; "no drop shadow" unattributed | each rule carries its authority; "no drop shadow" and "outline only in #25354A / no selective outlining / no second tone" labelled scoped specialist choices and added to `specialist_choices_in_this_brief` | attribution corrected |
| `hard_constraints.outline` | authority text mixed | authority text names the three parts (confirmation / measurement / 3c choice) | none |
| `supersedes` block | absent | v1 path, hash, reason, this table | n/a |
| everything else | v1 | unchanged (state binding, deliverable, references, cardinality, SQ1-SQ9, exclusions, acceptance route; `next_operation` now says the then-current hash is revision 11's) | none |

The composed `c_sample.li` string inside the brief is unchanged and still equals the saved
contract field. `q_sample_outline` keeps its revision 9 text; it tests "fully enclosing the
figure ... applied consistently on every contour", which is the required outcome. Component 3c
is wording to help a generator meet that outcome, not a new rejection rule.

`request-review-v2.json` (sha256 `a596f02addb73ba1c7732cfe05a8071b97b7c7236f26e349fdca5184e0684d73`)
points `request` at the v2 brief, keeps `criteria` at the unchanged `sample-criteria.json`
(`14c979ea...1834b`), names `validate_criteria_v2.py` as the only reproduction route, carries
a `supersedes` block for the v1 packet, and lists the two added specialist choices. The runtime
refusal was re-run on it and retained: `request-review-v2-tool-refusal.json` (sha256
`87f06d6dc0ca49f5398116fb7faf40003db713e66e019a2519f1cb9f90781b65`, exit 2, "review expects
exact provider arguments, not a creative brief"), as expected before discovery.

## Files added this session (consumer-relative, sha256)

| Path | sha256 | Role |
|---|---|---|
| `deliverables/sample-request/validate_criteria_v2.py` | `b582f32737eb5733f6be883c3e08b0ce9423408bb7249caa3b7c32d12011719b` | read-only validator; the only reproduction route |
| `work/sample-checks/criteria-validation-rerun-v2.json` | `d22798dcafd78049d59576dc712edeffa48630388a244e7c7fb2bc20a45093bc` | v2 validator run saved to a fresh path (schema_valid true, 18/18 bounds) |
| `deliverables/sample-request/sample-creative-brief-v2.json` | `f84b262818bbf044eb22716ab5d02eed1103cc65714360fcfc5d9efd019a5b80` | successor brief, 171 lines; bound `s_sample_brief_v2` |
| `deliverables/sample-request/request-review-v2.json` | `a596f02addb73ba1c7732cfe05a8071b97b7c7236f26e349fdca5184e0684d73` | successor packet, 85 lines; bound `s_sample_request_review_v2` |
| `deliverables/sample-request/request-review-v2-tool-refusal.json` | `87f06d6dc0ca49f5398116fb7faf40003db713e66e019a2519f1cb9f90781b65` | retained runtime refusal of the v2 packet |
| `work/build_rev11.py` | `5b2bb256014e700ae616ceba5d4b45789810035c000506b261c6e0c318559394` | revision 11 builder |
| `work/verify_rev11.py` | `37c412593bf5b0a47852e285d4b226699e430b328ae4032c800a2e9ef0393981` | revision 11 verifier (read-only; also proves v2 validator leaves the retained artifact unchanged) |
| `work/rev11.json`, `work/rev11.px` | produced by the builder; `rev11.px` bytes equal the committed head | candidate document and wire |
| `deliverables/continuation-2026-11-15e.md` | bound by `s_continuation_6` | this note |
| `SESSION.md` | edited; hash in the caller return | current-session pointer |

Retained unchanged and re-verified by `work/verify_rev11.py`: `sample-creative-brief.json`
(`cc21bf77...380ce`), `sample-criteria.json` (`14c979ea...1834b`), `request-review.json`
(`ffa933ed...1e78b`), `criteria-schema-validation.json` (`93643a34...b16a`),
`validate_criteria.py` (`48f3d0f1...dbe45`), `continuation-2026-11-15d.md` (`826460e5...b1dc`),
and every file listed as protected in the original assignment.

## Records added in revision 11 (10 -> 11 delta)

| Record | Kind | Content |
|---|---|---|
| `s_sample_brief_v2` | S (new) | `ur deliverables/sample-request/sample-creative-brief-v2.json`, `dg f84b2628...a5b80`, `ln [1, 171]`, `at 2026-11-15`, `au local` |
| `s_sample_request_review_v2` | S (new) | `ur deliverables/sample-request/request-review-v2.json`, `dg a596f02a...84d73`, `ln [1, 85]`, `at 2026-11-15`, `au local` |
| `s_continuation_6` | S (new) | this note, `ln [1, N]` with its actual line count, `at 2026-11-15`, `au local` |
| `handoff_7` | N (new) | `wh actor`; `rv 11`; `nx [t_sample]`; `bl [t_scout, t_medic, t_family]`; `fo` = `s_continuation_6`, `s_sample_brief_v2`, `s_sample_request_review_v2`, `s_sample_criteria`, `s_sample_brief`, `s_sample_request_review`, `s_continuation_5`, `s_eval_answers`, `c_sample`, `f_sample`, `i_outline`, `i_canvas`, `i_palette`, `i_design_language`, `i_backgrounds`, `i_display_scale`, `i_role_diff`, `i_animation`, `i_engine`, `x_aid`, `x_study` |

Header `PX2 10 -> PX2 11`. Nothing else: all 76 revision 10 records byte-identical (verified
against `work/rev10.json`). The v1 S records stay bound; `s_sample_criteria` is shared by both
packets because the criteria file did not change.

## Decision table, operation-effect trace, later production needs

Unchanged from `continuation-2026-11-15d.md`: every intake status and value is identical
(verified by the record-hash comparison), `t_sample` remains the ready task, and the next
operation is still `job-prepare` for `t_sample` with the same remaining inputs, except that the
`--expect` hash is now revision 11's and the provider arguments are translated from the **v2**
brief. The sample-blocking inputs are capability inputs (live declaration, transport handles,
authorization evidence), not owner answers; `i_display_scale` and `i_backgrounds` are still
needed before visual review, and the production answers listed in the d note are unchanged.

## Preserved and unchanged

All earlier reports, evidence, review files, state history copies (now 12 after this commit),
`work/` builders for revisions 2-10, the research candidates and verdicts, `handoff` through
`handoff_6`, every source byte, both references, `pixl-kit/`, `CALLER-RESULT*.json`, the caller's
`work/caller-restore-validation.py`. `SESSION.md` is again the only pre-existing file edited.
