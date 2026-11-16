# Continuation note, 2026-11-16 (c): corrections after the caller review of revision 15

Same session, same consumer root (`C:/Users/ryanf/AppData/Local/Temp/pixl caller review 249faf48d4f549729dad6842462c74ce/consumer`),
same kit (manifest `31b64de8...`), interpreter and isolation as `deliverables/continuation-2026-11-16b.md`
(the b note, sha256 `6454d5b65397a7d1b647088055dccfb39e5b58173c34218df436584dae8c62f1`, bound as
`s_continuation_10`, retained unchanged). The caller reviewed revision 15 independently, verified it
consistent on every claim it checked (state identity, wire diff, `handoff_11.fo`, note binding, entry
snapshot, kit identity, `verify_rev15.py`, its own `check_handoff.py` inventory and `--review` runs
reproducing `handoff-inventory-01.json` and `handoff-check-02.json` byte for byte, tables A-D, the
worksheet rows, the decision table and every kit/runtime line claim), and returned five findings
F1-F5. All five are correct. This note records the old-to-new correction for each and otherwise
directs readers to the b note, which remains the current full continuation. This is still a
**handoff-only increment**: no request packet, criteria v2, fixture, harness, generation, provider,
candidate, verdict, evidence, intake-status or task-state work; `c_sample`, the five sample criteria,
every I/T record and every retained file keep their bytes. No owner answers were supplied or invented.

## State identity on entry / exit

| | Value |
|---|---|
| Entry | PX2 revision 15, 88 records, canonical hash `8284e076c7d3052e69b78e47061b46971fa7b5b81f03e2a41b58cc7a511e565c` (= head sha256 = history copy = `work/rev15.px`), ready `[t_sample]`, no jobs, no families, head record `handoff_11`; `pixl-kit/` 261 files, no `__pycache__` |
| Exit | revision 16, 90 records (88 + `s_continuation_11` + `handoff_12`), committed to the store folder `state.px` with expected hash `8284e076...e565c`; ready `[t_sample]`, blockers unchanged, no jobs. The revision 16 hash is not written here (this note's digest is bound inside it); read it from `state.px/state.px`, `SESSION.md` or `deliverables/specialist-return-2026-11-16c.json` |

## Corrections (old -> new)

**F1. Kit-file accounting (b note lines 78-80).** Old: "The kit directory holds **261** files (259
manifest-listed files, the manifest itself, and `resources/pixl/handoff_review.py`, which the manifest
report counts among its 260 checked files)". New: the kit directory holds 261 files = the 259 entries
of the manifest's `files` array (which **includes** `resources/pixl/handoff_review.py`, entry sha256
`5f49e8f3...`) + `pixl-kit/bundle-manifest.json` itself + `pixl-kit/requirements.txt`, the only file
listed under the manifest's `generated_files` (`sha256 9cc16454cea28c8f5e5b6dbd150434f0c3259f698a6fd65086e275760d5891f3`).
`pixl_readiness` `files_checked 260` = 259 `files` entries + the generated `requirements.txt`. The
counts in the b note (261 / 259 / 260) were right; the attribution of the 261st file was wrong. The b
note's new-file table (lines 97-105) is unaffected: `resources/pixl/handoff_review.py` is both
manifest-listed and new relative to the revision 14 snapshot.

**F2. The b result points at the failed first attempt.** Old: `deliverables/specialist-return-2026-11-16b.json`
`/handoff_review/paths` names `work/handoff-review-rev15/handoff-inventory-01.json`,
`handoff-review-01.json` and `handoff-check-01.json`; `handoff-check-01.json` (`4c8ce8b2...`) is the
retained `coverage_incomplete` attempt (two `sources/brief.md` ranges ended at line 34; the file has 33
lines), and the completed binding is `handoff-review-02.json` (`e97a3012...`) / `handoff-check-02.json`
(`fbcd6091...`, `coverage_complete`), bound to the same result hash `7d80d6f9...`. New: the b result and
all five revision 15 review files are retained unchanged as that round's record; the corrected saved
return is `deliverables/specialist-return-2026-11-16c.json`, whose `/handoff_review/paths` pre-names
`work/handoff-review-rev16/handoff-inventory-01.json`, `handoff-review-01.json` and
`handoff-check-01.json`, and exactly those files are produced in this round (a failed attempt, if
any, would be retained under a later `-0N` name and reported, not relabelled).

**F3. Declared carrier not covered.** Old: b note line 265 lists the authored result fields "/status,
/questions (whole collection), /next (whole subtree), /limitations" as current carriers, while the
revision 15 inventory scopes were `/questions`, `/next`, `/limitations`; `/status` had no review row
(`handoff-review.md` 20-24 and 37-38). New: the revision 16 literal review uses scopes `/status`,
`/questions`, `/next`, `/limitations`; `/status` has a source-comparison row (judged against the
delegated scope per `delegation.md` 145 and 153-155).

**F4. Minor locators.** (a) b note line 103: old "`semantic_verdict` always `not_assessed` (122, 129)"
in `pixl-kit/runtime/pixl/handoff_review.py`; line 129 is `],`; new: lines **122 and 209**. (b) b note
line 255 (worksheet row R13), the b result `/questions/0/unlocks` and
`/next/preparatory_steps_once_Q1_is_supplied/0`: old "SQ1-SQ4 ... at lines 142-171" of
`deliverables/sample-request/sample-creative-brief-v2.json` (`f84b2628...a5b80`); measured: the
`schema_questions_for_the_live_declaration` array spans lines **142-152**, SQ1-SQ4 are lines
**143-146**, SQ5-SQ9 are lines 147-151, and 171 is the file's last line. New: "SQ1-SQ4 at lines
143-146 (array 142-152; SQ5-SQ9 at 147-151 are answered in the same step)". The step itself is
unchanged.

**F5. Shell observation (new prescription P7).** Under Git Bash (MSYS), an argument such as
`--scope /questions` is rewritten to a Windows path before `check_handoff.py` sees it, and the helper
fails with "scope and claim pointers must be JSON Pointers". This is not a kit fault: it succeeds
with `MSYS_NO_PATHCONV=1` set in that shell, or from PowerShell / cmd. P7 below records it.

## Current instructions after this note

- The b note remains the current full continuation. Every section of it stays current **except the
  corrected sentences above**: lines 78-80 (F1), line 103 (F4a), line 255's "lines 142-171" (F4b)
  and line 265's carrier list in so far as the revision 15 review did not cover `/status` (F3). Its
  worksheet R1-R15 / A1-A3, effect sentence, decision table, procedural prescriptions P1-P4 and P6,
  "What later production still needs", "Earlier notes" and "Superseded" sections are unchanged
  current instructions and are carried into the revision 16 literal review as carriers together
  with this note's two sections "Corrections (old -> new)" and "Current instructions after this
  note".
- **P5 (updated): current verifier** is `python -B -I work/verify_rev16.py` from the consumer root,
  expected `problems []`; it compares the 88 revision 15 records with `work/rev15.json`, checks the
  b note, the b result and the five revision 15 review files among its retained hashes, and reports
  kit identity and any `__pycache__` as observations. `work/verify_rev15.py` remains correct for
  revision 15 (its snapshot predates this round's files, which it does not list).
- **P7 (new): shell path conversion.** When invoking `check_handoff.py` (or any command taking
  JSON-Pointer arguments) from Git Bash / MSYS, set `MSYS_NO_PATHCONV=1` first, or use PowerShell;
  a "scope and claim pointers must be JSON Pointers" error with a leading-slash scope is the shell's
  rewrite, not a kit defect.
- The saved return to read is `deliverables/specialist-return-2026-11-16c.json` (hash in the final
  response and `SESSION.md`); the b result is the retained revision 15 return. Review/check hashes
  stay out of the result's own file-reference list (`handoff-review.md` 122-126).
- The next operation, its gates, missing inputs and alternatives are unchanged from the b note:
  `job-prepare` for `t_sample` / `f_sample` against `c_sample`, blocked only on capability inputs
  (R10-R15) and the `provider_arguments` successor packet with the criteria-v2 supersession and
  caller comparison; no owner answer is needed for it; `i_display_scale` gates visual review only.

## Files added or edited in this correction round (consumer-relative, sha256)

| Path | sha256 | Role |
|---|---|---|
| `work/rev16-protected-snapshot.sha256` | `f41116671854379a40fce92480314c09ba773198afbb894773c567e0f917fa3f` | sha256 of all 419 files present before any write in this round (158 non-kit, 261 kit, 0 `__pycache__`); read by the verifier |
| `work/build_rev16.py` | `71ee6d19926754fd85b45aae41acbf0e9b2757a5d40689ff6e7fb82b72fa4160` | revision 16 builder (decode head, append 2 records, encode; runner subprocesses with `-B -I`) |
| `work/verify_rev16.py` | `e852bfa5a5936eab66727fcc8183da4aee26732d38c4064e015d03b9c1bdbd50` | revision 16 verifier, read-only |
| `work/rev16.json`, `work/rev16.px` | produced by the builder after this note is final; `rev16.px` bytes equal the committed head | candidate document and wire |
| `deliverables/continuation-2026-11-16c.md` | bound by `s_continuation_11` | this note |
| `deliverables/specialist-return-2026-11-16c.json` | produced after the commit; hash in the final response | corrected saved return (scopes `/status`, `/questions`, `/next`, `/limitations`) |
| `work/handoff-review-rev16/handoff-inventory-01.json`, `handoff-review-01.json`, `handoff-check-01.json`, `build_review.py` | produced after the return; hashes in the final response, kept out of the return's file-reference list | literal handoff review of the corrected return |
| `SESSION.md` | edited after the commit; hash in the final response | pointer: revision 16, read this note then the b note, corrected kit-file accounting, P7 |

Nothing else was written; `validate_criteria.py` was not run; no `__pycache__` was created.

## Records added in revision 16 (15 -> 16 delta)

| Record | Kind | Content |
|---|---|---|
| `s_continuation_11` | S (new) | `ur deliverables/continuation-2026-11-16c.md`, `dg` = this note's sha256, `ln [1, N]` with its actual line count, `at 2026-11-16`, `au local` |
| `handoff_12` | N (new) | `wh actor`; `rv 16`; `nx [t_sample]`; `bl [t_scout, t_medic, t_family]`; `fo` = `s_continuation_11` followed by `handoff_11`'s complete list (`s_continuation_10`, `s_continuation_9`, `s_continuation_8`, `s_continuation_7`, `s_continuation_6`, `s_sample_brief_v2`, `s_sample_request_review_v2`, `s_sample_criteria`, `s_sample_brief`, `s_sample_request_review`, `s_eval_answers`, `c_sample`, `f_sample`, the 12 non-confirmed I records in state order, `x_aid`, `x_study`) |

Header `PX2 15 -> PX2 16`. Nothing else: all 88 revision 15 records byte-identical (verified against
`work/rev15.json` by `verify_rev16.py`). The corrections reach the state only through this note's
binding; no Q, I, C or S record is edited or superseded, because none of them carries the corrected
text.
