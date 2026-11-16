# Continuation note, 2026-11-16 (b): handoff-only continuation under a new consumer root; kit changed a fourth time; the literal handoff review is now required

This increment retains the prepared work, re-inspects the actual current state and the artifacts the
revision 14 handoff relies on, and saves a current, self-contained continuation for the next session.
It is a **handoff-only increment**: no request packet, criteria v2 file, fixture, harness run,
generation, provider, candidate, verdict, evidence, intake-status or task-state work was assigned or
performed. The contract `c_sample`, the five sample criteria, every I record, every T state and every
retained file keep their bytes. The only production-state change is the addition of this note's S
record and a new N record (revision 15, below). No owner answers were supplied in this invocation and
none are invented; the controlled-evaluation answers (`sources/controlled-evaluation-answers.md`
`87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30`, lines 5-6, scope statement line 8)
remain applied within their sample scope only. The owner brief is `sources/brief.md` lines 3-7
(verbatim); its lines 11-15 are the 2026-09-14 predecessor's session constraints, provenance only.

This is an artifact-based restart: the native child of the previous session (`a2243e0a858503645`,
recorded in `CALLER-RESULT-LITERAL-RECONCILIATION.json`) was not resumed; its work is consumed through
the retained files and the store history. The previous notes stay source evidence. Which of their
sections remain applicable is named in "Earlier notes: what remains applicable" at the end, together
with an explicit old-to-new list of what this note supersedes; nothing in them is adopted wholesale.

## Consumer-root change

| | Root | Revisions committed there | Notes / caller files |
|---|---|---|---|
| Current (this increment) | `C:/Users/ryanf/AppData/Local/Temp/pixl caller review 249faf48d4f549729dad6842462c74ce/consumer` | 14 -> 15 | this note (`continuation-2026-11-16b.md`) |
| Previous (provenance) | `.../pixl caller review 9f6e7c37402f4037acf44abe70f04834/consumer` | 13 -> 14 | `continuation-2026-11-16.md`; caller files `CALLER-RESULT-LITERAL-RECONCILIATION.json`, `review/caller-comparison-2026-11-16-v6.md` |
| Earlier (provenance) | `.../pixl caller review a97de5914a21428aad2fef3c65ecfcec/consumer` | 11 -> 12 -> 13 | f (`continuation-2026-11-15f.md`), g (`-15g.md`); `CALLER-RESULT-PREREQUISITES-02.json`, `review/caller-comparison-2026-11-15-v5.md` |
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
the same layout as the previous five roots, but the kit **contents** changed again (next section).
The bare `python` on this shell's PATH (`C:/Python314/python`, 3.14.3, without `jsonschema`) is **not**
the selected interpreter and cannot run the kit runner; every kit run in this increment used the
selected interpreter's absolute path.

## State identity on entry (observed in this increment)

| Item | Observed |
|---|---|
| `state.px/state.px` | PX2, revision 14, 86 records, valid, `files_verified true` |
| Canonical state hash (= head sha256 = `state.px/history/247b22ba....px` = `work/rev14.px`) | `247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af` |
| `pixl_ready` | `[t_sample]` |
| `pixl_jobs` | `[]` (no prepared, unknown, submitted or running attempt; `remote_executed false`) |
| `pixl_workflow` blockers | `t_sample` none; `t_scout`, `t_medic`: `t_sample` open, output needs a raster contract, task needs an adoption decision; `t_family`: `t_scout` and `t_medic` open, needs an adoption decision; `t_aid`, `t_study` done |
| Head N record | `handoff_10` (rv 14) |
| Families / connected plans | none (`pixl_context` plans `[]`) |
| History copies | 15 (`PX2 0..14`) |
| `work/verify_rev14.py` (run by the caller with `-I`; re-run here with `-B -I`) | `problems []`, exit 0; its kit block reports `kit_changed_since_snapshot true` with the three differing kit files below |
| `work/verify_rev13.py` | still exits 1 on kit-identity entries only, as the 2026-11-16 note (lines 215-229) explains; not re-run |
| `pixl-kit/` bytecode cache | **none** on entry (261 files, 0 `__pycache__` directories) |

## State identity on exit

Revision 15, 88 records (86 + `s_continuation_10` + `handoff_11`), committed to the store folder
`state.px` with expected hash `247b22ba...e4af`. The revision 15 canonical hash is not written here
because this note's digest is bound inside it; read it from `state.px/state.px`, `SESSION.md` or the
caller return (`deliverables/specialist-return-2026-11-16b.json`). Expected after commit (checked by
`work/verify_rev15.py`): ready `[t_sample]`, blockers unchanged, no jobs, all 86 revision 14 records
byte-identical, no `__pycache__` under `pixl-kit/`.

## Kit identity observed now

`pixl_readiness` (host `claude`, installation `pixl-kit`): kit present, bundle manifest **verified**,
`sha256 31b64de8b9fa14a3faacaee21ee21e40883b48bd64c493912aff7ea7aceb564a`, 260 files checked, no issues;
Python 3.14.3, pillow 12.3.0, jsonschema 4.26.0, referencing 0.37.0. Official PixelLab tools
`not_observed`, authentication `not_verified`, execution `not_attempted`; `named_role not_observed` from
static files (the `.claude/agents/pixl.md` and `.claude/skills/pixl/SKILL.md` adapters are absent in this
consumer, expected for plugin loading). Manifest verification means the payload bytes match the local
manifest; publisher authenticity is not established by it. The kit directory holds **261** files (259
manifest-listed files, the manifest itself, and `resources/pixl/handoff_review.py`, which the manifest
report counts among its 260 checked files) and **no** `__pycache__` directory, on entry and after every
kit run of this increment (all run as `python -B -I ...`).

### Changed kit files (sha256 measured in this increment; previous = the 2026-11-16 note's values, lines 72-74)

| Kit file | Previous (2026-11-16 note) | Now | Lines before -> now |
|---|---|---|---|
| `pixl-kit/bundle-manifest.json` | `e1fb00650c4526b26584aae83b7989ff3d56892045bfb1fe2e975598968dd398` (256 entries) | `31b64de8b9fa14a3faacaee21ee21e40883b48bd64c493912aff7ea7aceb564a` (259 entries) | 1544 -> 1568 |
| `pixl-kit/skills/pixl/references/delegation.md` | `2f5af8b5339daaef3402eacb5fc532a0123cafeb0b8b2c5fc990c1221ab5bdc5` | `72bd2cdfd03333ae0cc3bcd325c4a231f0730ca2f42fbece1955b18b5648199b` | 245 -> 244 |
| `pixl-kit/skills/pixl/references/intake-sample.md` | `b24dad8e654215d04b3229b3d7b08b2c06b32cb1442cdf53c49b066776fe47f6` | `9fd421030d44e104ff36446409d4562a976daec1650f7a956a950ae8043846ef` | 188 -> 190 |

The previous bytes of the three changed files are not retained anywhere in this consumer, so a textual
diff is not possible; the re-map below compares the 2026-11-16 note's description of the previous text
with the current text. The diff above is measured against the kit entries of
`work/rev14-protected-snapshot.sha256` (257 kit entries, taken under the 9f6e7c37 root): exactly these
three files differ, exactly the four files below are new, and no kit file is gone.

### New kit files (absent from the 2026-11-16 note and from the revision 14 snapshot)

| Kit file | sha256 | Lines | Role |
|---|---|---|---|
| `pixl-kit/skills/pixl/references/handoff-review.md` | `42f73d779736ce90738542f7d5fb52d78d0f6c65c6ea81ddf151f181f794204f` | 126 | the literal handoff review operation: establish current instructions (8-18), save the result and select whole subtrees (20-24), inventory (26-46, `-B -I` rule 40-42), review every value (48-99, one row per leaf 80-86, carriers 88-93, 16,384-byte excerpt limit 95-99), coverage check (101-120), keep review/check hashes out of the result (122-126) |
| `pixl-kit/scripts/check_handoff.py` | `ac1afd38549c6e951ab02afdfcc1695f3dcd309b3e357bca524a679271c02acc` | 24 | launcher; sets `sys.dont_write_bytecode = True` (lines 9-11) and runs `pixl.handoff_review` from `runtime/` |
| `pixl-kit/runtime/pixl/handoff_review.py` | `5f49e8f3514bc59117714f7392528b9f60f1aa0ba874d5caef262a093153c7d4` | 214 | the read-only inventory/coverage module: leaves of the selected scopes (72-79), overlapping/duplicate scope refusal (82-89), citation resolution through `request_review.source_evidence` (92-106), coverage comparison (133-186), `semantic_verdict` always `not_assessed` (122, 129) |
| `pixl-kit/resources/pixl/handoff_review.py` | `5f49e8f3514bc59117714f7392528b9f60f1aa0ba874d5caef262a093153c7d4` (identical bytes) | 214 | packaged copy of the same module |

Unchanged by hash (measured now, equal to the 2026-11-16 note lines 76-84 and the f note):
`skills/pixl/SKILL.md` `04a46dae9b55e5e54eec5b1a033e6e597f3e44170d930e96da3554289b34a5a2`; `agents/pixl.md`
`34187821f9875c880e703588065ec62dc7a85e1a044b5c7565825c200b7b10b9`; `resources/agent/PROFILE.md`
`8aeaedb1f345af7f80d289f3f8372de00e20619ccf4ec685ed6db229c4d99265`;
`skills/pixl/references/state-authority.md` `4f883c6832d63a5e8ff134f69dbbf6d90abdc96c3004b39cae7aec6a87715112`;
`skills/pixl/references/readiness.md` `fd9156896d7789046d45a09dc5e94330f59a1949ad44953843ac128a1a823d4f`;
`skills/pixl/references/request-review.md` `98ac6d9daee4fd7855ca365674c9a9625b666301e32dfd9547cf34fe65017ee2`;
`runtime/pixl/lifecycle.py` `5e37cefb2bcb357373332af4970b7c30df4e18df6d78e36022fe349a616a6a23`;
`runtime/pixl/jobs.py` `18d543f7d81134b46c5282728be7e7681c94789c554a9f6e3abe0f882c92ecc3`;
`runtime/pixl/platform.py` `7693533dea30d9027cd7f89b47629227b87b18f23e993ae6eab848cb78efbea0`;
`runtime/pixl/request_review.py` `af7bf5bf1f599a03645d12e6faadb14db050dec5a31eae067ed3fc36295a1c23`;
`scripts/pixl.py` `37fc3d39169803bdcc6df70c861184ca2bfcd52e085bec75015cdb17813974e4`.

### Citation re-map of the 2026-11-16 note's kit locators (previous line -> current line)

The 2026-11-16 note (`157d131cd3979d2b4e7e1729e4accbd2f8446f3573beed6e0fea543eb68fd420`) cites the two
changed reference files in four places: its re-map table (lines 95-107), its runtime citations (109-114),
its dependence statement (124-142) and the locators of its worksheet rows (153-171). Each subject is
marked **same** (same lines, same words), **moved** (same words, other lines), **reworded** (same
subject, changed words) or **gone** (the cited text no longer exists in that file). The g note cites no
kit file by line; the f note's kit citations were already superseded by the 2026-11-16 note.

**A. The 2026-11-16 note's re-map table (its lines 95-107)**

| Note line | Subject | Location given there | Current location | Status |
|---|---|---|---|---|
| 97 | `intake-sample.md` "Check what an answer enables", including "Write the current effect before the return" | 70-157; subsection 106-157 | 70-159; heading 70; procedure 70-105 word for word; subsection 106-159 (template 112-126; items 128-153; closing paragraph 155-159) | moved (section end +2); procedure same |
| 98 | worksheet item 4: build `question`, `necessary_for`, `unlocks`, `next`, `blocked_on` from fresh checked statements | 142-145 | 143-146 | moved; same words |
| 99 | worksheet item 5 (the "carrier check") | 146-151 | 147-153 | moved and **reworded/extended**: item 5 now reads "For a saved JSON result, perform the literal handoff review (handoff-review.md): inventory the whole question collection and whole authored next-operation subtree, review every listed value and bind the complete current instruction excerpts. Start with `python -B -I KIT/scripts/check_handoff.py RESULT --root ROOT --scope /remaining_questions --scope /next_action`, using the actual field names. Reopen the saved fields and current text after the coverage check and compare their meaning with the sources. Coverage is not semantic acceptance." The prose comparison the 2026-11-16 note performed as its carrier check (its lines 180-187) is no longer the prescribed form. The unchanged-position text at 97-104 (project only the supplied answer; rerun workflow before claiming readiness) still stands |
| 100 | "Cold intake handoff" | 159-188 | 161-190 (steps 163-169, 171-175, 177-181, 183-188; family paragraph 190) | moved (+2); four steps, same words |
| 101 | step 2: save the worksheet in a new continuation note; "unasked rows keep their status" | 169-173; 171 | 171-175; 173 | moved; same words. Line 97 still says "In the saved decision table, project only the supplied answer" |
| 102 | step 4: final-response rule (choices already supplied: use them and state the next operation without asking again) | 181-186 | 183-188 | moved; same rule |
| 103 | `delegation.md` "Specialist -> caller at completion"; result fields | 138-158; 146-152 | 137-157; 145-151 | moved (-1); same fields (`status`, `asset_id`/`requirements_hash`, `artifacts`, `checks`, `request_review`, `provider`, `questions`/`next`) |
| 104 | planning-only rules (no manufactured production state; judge completion against the delegated scope) | 154 and 156 | 153 and 155 | moved (-1); same words |
| 105 | "Caller: review a cold continuation"; step 2 naming "the specialist's current-effect worksheet" at line 88 with a link to `intake-sample.md#write-the-current-effect-before-the-return`; step 3; step 5 | 71-136; 86-98 (88); 100-113; 122-136 | 71-135; step 2 86-97; step 3 99-111; step 4 112-119; step 5 121-135 with **new** line 128 ("Run the literal coverage check ... on your saved result and current instruction excerpts") | **reworded**: step 2 lines 88-90 now read "For JSON returns, use the literal handoff review (handoff-review.md) to inventory the whole question collection and whole authored next-operation subtree. Review every listed value; the specialist's worksheet does not choose the coverage." The link to the worksheet section is **gone** from `delegation.md`; the same link now stands in `handoff-review.md` line 11 |
| 106 | `intake-sample.md` line 11 heading "Keep authority through derived rules" (cited by `sample-creative-brief-v2.json` line 100 by section name) | 11 | 11 | same |
| 107 | `delegation.md` 21-23 (PLAR hand-over, native delegation) and 25-35 (reassess-or-correct paragraph), cited by `CALLER-RESULT.json` lines 93 and 105 | 21-23; 25-35 | 21-23; 25-35 | same |

Also still at the same lines: `delegation.md` 69 (request-and-criteria handoff before adopting a
proposed production contract) and `intake-sample.md` 25 (PLAR preparation route) and 129 ("Keep every
unasked choice unchanged").

**B. Runtime citations (2026-11-16 note lines 109-114)**: `lifecycle.py` 44-77 (`_activation_blockers`;
`task_prerequisite` 49-52, `output_contract` 53-56, `choice_unresolved`/`conflict` 57-64,
`ADOPTION_PHASES` gates 65-75, families 76), `jobs.py` 717-743 (`prepare()`: `_load` with expected 731,
`job_exists` 732-734, `_context` 735, blockers 736-737, `_pending` 738, `prepare_discovered` 739-741),
`platform.py` 869-889 (identity 869-870, arguments object 871-872, discovery/authorization fields
873-874, texts 875-877, nonempty evidence 878-885, no secrets 886-888, schema validation 889) and
1017-1023 (`observed_at` not in the future, 1019-1023), `request_review.py` 130-134 (`kind ==
"provider_arguments"` at 132). All four files are unchanged by hash and were re-read in this increment:
**same**.

**C. Dependence statement (2026-11-16 note lines 124-142)**

| Note lines | Claim there | Current text | Status |
|---|---|---|---|
| 126-132 | nothing in the handoff depends on text the kit lacks; the decision table is kept as a layout under `intake-sample.md` 97 | every subject still present (table A); line 97 unchanged | same, with one addition: the worksheet link that stood in `delegation.md` 88 is gone from that file and lives in `handoff-review.md` 11 |
| 134-135, item (1) | `intake-sample.md` 106-126 and 169-170: worksheet saved inside the new note | 106-126 same; 171-173 | moved |
| 135-137, item (2) | 142-145: authored `next`/`blocked_on`/`questions` built from the worksheet rows | 143-146 | moved |
| 138-139, item (3) | 146-151: "the carrier check ... was performed on this note and the return before returning" | 147-153 | **reworded/extended**: a saved JSON result must undergo the literal handoff review with `check_handoff.py`; a prose carrier check no longer satisfies the text (see Dependence statement below) |
| 139-140, item (4) | `delegation.md` 86-98: the caller's step 2 reads the worksheet as the claim set | 86-97 | **reworded**: the caller inventories the JSON return with the literal handoff review; "the specialist's worksheet does not choose the coverage" |
| 141-142 | runtime gate files unchanged by hash, gate evaluation unaffected | unchanged by hash again | same |

**D. Locators inside the worksheet rows (2026-11-16 note lines 153-171)**: R1 `jobs.py` 732-734; R2
`jobs.py` 735; R3 `lifecycle.py` 49-52; R4 53-56; R5 57-64; R6 65-75; R7 76; R8 `jobs.py` 738; R9 `jobs.py`
731 and `state-authority.md` 13; R10 `platform.py` 869; R11 `platform.py` 870 and `readiness.md`
(101-102: "A dated `pixl_capabilities` catalog is documentation, not live official-tool visibility");
R12 `platform.py` 888-889; R13 `platform.py` 871-872, 887, 889, `PROFILE.md` 44, `request_review.py` 132;
R14 `platform.py` 873, 875-876, 878-885, 1018-1023; R15 `platform.py` 874, 877, 878-885; A1 `SKILL.md`
line 26 and `PROFILE.md` 32; A2 `intake-sample.md` 25 and `SKILL.md` 24 (PLAR paragraph); A3 the
`q_sample_readability` record. Every one of these files except `intake-sample.md` is unchanged by hash,
and `intake-sample.md` line 25 is unchanged: **same** for every row.

**Caller-authored files carrying the previous kit numbers (retained, not mine, not edited):**
`CALLER-RESULT-LITERAL-RECONCILIATION.json` (`7b033ec23f1307ab3083e8061fb5456a61fc389085b8b00ac36158d0f03229e3`)
lines 26 and 69-71 (manifest `e1fb0065...` with 1544 lines / 256 entries; `delegation.md` `2f5af8b5...`
245 lines with 71-136 / 88 / 114-120 / 122-136 / 138-158; `intake-sample.md` `b24dad8e...` 188 lines
with 70-157 / 106-157 / 112-126 / 128-151 / 159-188), line 166 (`kit_identity`) and lines 27, 123, 200
and 208 (a bytecode cache in the **previous** root); `review/caller-comparison-2026-11-16-v6.md`
(`1c7e717745e00c11ac80b8bc13ff41c0be2c156b9f013bf5b401eea62fc4a0b5`) lines 34-36, 66-67, 110-112 and
126-130. Read them with table A and the cache paragraph below.

### Dependence statement

- **Nothing in the current handoff depends on text the current kit lacks.** Every subject the
  2026-11-16, g and f notes rely on (operation-effect procedure, worksheet template, final-response
  rule, completion fields, planning-only scope rule, PLAR/native-delegation paragraphs,
  reassess-or-correct paragraph, the "keep authority" heading, all runtime gates) is present in the
  current text at the re-mapped lines. The one link that left `delegation.md` (to the worksheet
  section) is present in `handoff-review.md` line 11. The decision table remains a specialist layout
  under current `intake-sample.md` 97; it is not an owner requirement or a kit requirement.
- **The current kit newly requires what the 2026-11-16 note does not satisfy**, and this increment
  supplies it:
  1. **Literal handoff review of a saved JSON result** (`intake-sample.md` 147-153; `handoff-review.md`
     20-24, 26-46, 48-99, 101-120, 122-126; `delegation.md` 86-97 and 128 for the caller's side). The
     2026-11-16 note's carrier check (its lines 180-187) was a prose comparison; revision 14's return was
     not saved as a JSON file in this consumer and no inventory, review or check file exists for it.
     This increment saves the return as `deliverables/specialist-return-2026-11-16b.json`, inventories
     its whole `questions` collection, whole `next` subtree and `limitations` list with
     `check_handoff.py` (scopes `/questions`, `/next`, `/limitations`, the actual field names), writes a
     version-1 review with one row per inventory leaf (source-comparison rows with actual source hashes
     and inclusive line ranges; metadata rows only for identifiers) and the current-instruction
     excerpts of this note as carriers, then runs the coverage check. Output files are under
     `work/handoff-review-rev15/`; their hashes are reported in the final response and kept out of the
     result's own file-reference list (`handoff-review.md` 122-126). `coverage_complete` means the
     declared coverage and bindings match; `semantic_verdict` stays `not_assessed` (107-113).
  2. **`-B -I` for the helper and every other Python read of the read-only kit** (`handoff-review.md`
     40-42; also `check_handoff.py` 9-11, which forces `dont_write_bytecode` for its own imports). The
     2026-11-16 note and the previous `SESSION.md` prescribe `-I` alone (`work/verify_rev14.py`
     docstring line 23; `work/build_rev14.py` line 13), which ignores `PYTHONDONTWRITEBYTECODE` and in
     the previous root produced a 17-file bytecode cache. In this increment every kit run, including the
     runner subprocesses of `work/build_rev15.py` and `work/verify_rev15.py`, uses `-B -I`; this root
     held no `pixl-kit/**/__pycache__` on entry and holds none after this increment; `verify_rev15.py`
     reports any cache directory as an observation.
  3. **A saved result whose authored fields are built from fresh checked statements**
     (`intake-sample.md` 143-146): `questions`, `next` and `limitations` in the saved return are
     written from the worksheet rows below, not from `CALLER-RESULT-LITERAL-RECONCILIATION.json`
     `remaining_questions` / `next_action`.
  4. **A self-contained current operation section** (`handoff-review.md` 8-18; `intake-sample.md`
     137-142; `delegation.md` 124-127): the section "Current operation and conditions" below carries
     every instruction governing the next operation, including permitted alternatives and the
     procedural prescriptions; earlier notes are history/evidence even where this note names their
     sections.
- The runtime files that enforce the next operation's gates are unchanged by hash, so the gate
  evaluation below is not affected by the kit change. The new `handoff_review.py` reads files and
  writes only its `--out` report; it touches no production state.

## Current operation and conditions (self-contained; `intake-sample.md` 112-126 worksheet)

```text
Current operation and answer effects
State/plan identity: state.px/state.px, PX2 revision 14, canonical 247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af on entry (revision 15 after this commit; read its hash from the head, SESSION.md or deliverables/specialist-return-2026-11-16b.json). Plan traced from the live pixl_workflow and pixl_context (focus t_sample, view authoring): T t_sample (ph sample, st open, dp [t_study] done, op [f_sample], ca [], dc [], kn []) -> F f_sample (kd sprite, ct c_sample, rq [q_sample_canvas, q_sample_palette, q_sample_outline, q_sample_readability, q_style_match]) -> C c_sample (record b7f77964...7737; px [32,32], pl [#56B5BC, #F4DDA2, #25354A], vw side, sa nearest, al binary) -> ch [i_canvas proposed, i_palette observed, i_view confirmed, i_sampling proposed, i_alpha observed, i_lighting observed, i_outline proposed, i_design_language proposed]. other_intake: i_animation, i_backgrounds, i_display_scale, i_engine, i_role_diff unresolved; i_roster confirmed. Plans [], jobs [], decisions [], knowledge [].
Operation and phase: pixl_job_prepare (CLI: python -B -I pixl-kit/scripts/pixl.py job-prepare state.px JOB t_sample REQUEST_JSON --outputs f_sample --expect <current hash> --root <this consumer root>); task t_sample, phase sample, output f_sample, contract c_sample.
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
R9 --expect = current canonical hash | jobs.py 731 (_load with expected); state-authority.md 13 | available: revision 15 hash after this commit (SESSION.md, caller return, pixl_validate) | unchanged | reread the head immediately before the call
R10 provider = identity text of the connected PixelLab service | platform.py 869 (_request_identity) | MISSING: official PixelLab tools not_observed, authentication not_verified (pixl_readiness official_pixellab) | unchanged | the host's authenticated PixelLab connection
R11 tool = the chosen operation's declared name | platform.py 870 | MISSING: must come from the live declaration; deliverables/sample-request/operation-shortlist.json (7294d9d7...0186) is a dated catalog and decides nothing (readiness.md 101-102; pixl_capabilities is "not live tool discovery") | unchanged | live tool listing in the host
R12 schema = the full live inputSchema object | platform.py 888-889 (_schema_no_secrets, _validate_schema) | MISSING | unchanged | live declaration
R13 arguments = exact provider arguments (JSON object, no secrets, valid under R12) | platform.py 871-872, 887, 889; PROFILE.md 44 (a filename in a prompt is not an uploaded reference); request_review.py 132 (packet kind provider_arguments) | MISSING: to be translated from sample-creative-brief-v2.json (f84b2628...a5b80; its schema questions SQ1-SQ4 at lines 142-171 are answered against the live declaration first) once R11/R12 are known, with reference.png (d997cade...70aa7, role style) as an actual image input (upload handle / URL / owned ID) | unchanged | R11, R12, image transport handle; then the provider_arguments successor packet, including the criteria-v2 supersession of sample-criteria.json (g note lines 61-74: q_sample_readability brief source lines [20,20], optionally [5,5], five check texts unchanged, validated with validate_criteria_v2.py --criteria <v2 file> --out <fresh work/ path>, bound as a new S beside the unchanged s_sample_criteria), pixl_request_review on that packet, and the caller's request/criteria comparison (delegation.md 69; request-review.md)
R14 discovery = {source text, observed_at ISO timestamp not in the future, evidence nonempty object} | platform.py 873, 875-876, 878-885; 1018-1023 | MISSING | unchanged | live tool listing plus a host-clock timestamp
R15 authorization = {scope text, evidence nonempty object} | platform.py 874, 877, 878-885 | scope text AVAILABLE (brief.md lines 6-7 "Begin the project and make the progress possible in this session"; P.br); evidence object MISSING | unchanged | caller/host supplies the evidence object, including coverage of the cost of one call
A1 Route alternative: authenticated official PixelLab MCP tool surface (primary) OR the optional HTTP adapter explicitly selected for its documented operation | SKILL.md 26 ("Production uses the official paid PixelLab API, preferring the authenticated MCP tool surface. The optional HTTP adapter is a separate explicitly selected route"); PROFILE.md 32 | neither observed in this host | unchanged | one of the two, selected by the caller/host; not an owner decision
A2 First-candidate path alternative: record-level job-prepare OR pixl_plar_prepare for a selected PLAR asset | intake-sample.md 25; SKILL.md 24 | no plar.txt exists in this consumer, so the PLAR route is not available here; job-prepare is the route | unchanged | none (job-prepare)
A3 Visual-review inputs: owner i_display_scale and i_backgrounds OR the specialist's light/dark/busy test set | q_sample_readability.ck (record 541b9a97...acd4); i_backgrounds.wy; i_display_scale.wy | both unresolved; the test set is the authorized fallback for backgrounds ("the specialist's test set until i_backgrounds is answered"); no default exists for the target integer zoom | unchanged | before pixl_inspection_prepare / pixl_inspection_review of a returned candidate (two steps after job-prepare); not before job-prepare

Current effect sentence: No owner answer is pending for the sample and no state-side gate blocks job-prepare for t_sample / f_sample against c_sample (R1-R9 satisfied or not applicable, the same conclusion as pixl_workflow blockers []); the operation is still not executable locally now, because R10-R15 (provider identity, tool name, live inputSchema, exact arguments with an actual image input for reference.png, discovery evidence with a host-clock timestamp, authorization evidence) are capability or caller inputs that no local file supplies, and R13 additionally requires the provider_arguments successor packet with the criteria-v2 supersession and the caller's comparison before preparation.
Remaining prerequisites: R10, R11, R12, R13 (including the successor packet, criteria v2 and caller comparison), R14, R15 evidence object.
Authorized default/alternative (or none established): A1 is a caller/host selection between two source-permitted routes; A2 is fixed to job-prepare in this consumer; A3: the specialist's test backgrounds are an authorized fallback, the display scale has no default and is needed before visual review only. No default exists for R10-R12, R14 or the R15 evidence object.
Current carriers: this note's sections "Current operation and conditions", "Procedural prescriptions", "Decision table" and "What later production still needs"; authored result fields in deliverables/specialist-return-2026-11-16b.json: /status, /questions (whole collection), /next (whole subtree), /limitations; final wording: "The next operation is job-prepare for t_sample / f_sample against c_sample. It is blocked only on capability inputs (the host's live PixelLab tool declaration and schema, an image transport handle for reference.png, discovery evidence and authorization evidence) and on the provider_arguments successor packet with the criteria-v2 supersession and caller comparison; no owner answer is needed for this operation. i_display_scale is needed before visual review of a returned candidate, not before preparation."
Prior instruction superseded: see the list "Superseded, old to new" at the end of this note.
```

### Procedural prescriptions for this root (current instructions, not gates of `job-prepare`)

- P1 **Literal handoff review of every saved JSON result** that carries authored questions, answer
  effects or a next operation (`intake-sample.md` 147-153; `handoff-review.md` 20-24, 26-46, 48-99,
  101-126): from the consumer root, `python -B -I pixl-kit/scripts/check_handoff.py RESULT --root .
  --scope <each whole authored subtree> --out <fresh path>`; then a version-1 review with one row per
  inventory leaf and carriers = exact current-instruction excerpts of the current note; then the same
  command with `--review`. Use the actual field names; keep the review/check hashes out of the
  result's own file-reference list; report `coverage_complete` and that `semantic_verdict` stays
  `not_assessed`; reopen the fields and the current text afterwards and compare their meaning with
  the sources.
- P2 **`python -B -I`** for `check_handoff.py`, the runner `pixl-kit/scripts/pixl.py` and every other
  Python read of the read-only kit, with the selected interpreter
  `C:/github/pixel-lab-agent/.venv/Scripts/python.exe` (`handoff-review.md` 40-42). `-I` alone ignores
  `PYTHONDONTWRITEBYTECODE`. Scripts that start the runner as a subprocess pass `-B -I` to it
  (`work/build_rev15.py`, `work/verify_rev15.py`).
- P3 **No bytecode cache exists in this root and none may be created**: `pixl-kit/` holds 261 files and
  no `__pycache__`; `work/verify_rev15.py` reports `kit_bytecode_cache_dirs` as an observation. The
  earlier advice to "ignore `pixl-kit/runtime/pixl/__pycache__/`" described the previous root.
- P4 **Criteria validation only with `deliverables/sample-request/validate_criteria_v2.py`** (read-only;
  `--out` to a fresh path under `work/` if a file is wanted); never `validate_criteria.py`, which
  overwrites the retained artifact `criteria-schema-validation.json` (`93643a34...b16a`).
- P5 **Current verifier**: `python -B -I work/verify_rev15.py` from the consumer root, expected
  `problems []`; its kit block reports kit identity through the manifest and the runner's manifest
  verification as observations. `work/verify_rev14.py` remains correct for the 9f6e7c37 root's kit and
  exits 0 here with `kit_changed_since_snapshot true`; `work/verify_rev13.py` exits 1 here on
  kit-identity entries only (2026-11-16 note lines 215-229, history).
- P6 **Cold start for the next session**: read `SESSION.md`, then this note; run `pixl_validate`,
  `pixl_workflow`, `pixl_ready`, `pixl_jobs` on `state.px/state.px` and expect revision 15, ready
  `[t_sample]`, no jobs; run P5; if the kit changed again, the verifier's kit block reports it as an
  observation and the citation re-map must be redone against the new text before any kit locator in
  this note is relied on. Readers of the bound v1/v2 packet files and the f note read
  "`sources/brief.md` line 19" for the side-view destination as line 20 (g note finding 1) until the
  criteria-v2 successor exists.

### Carrier check (worksheet item 5, in its current form)

Performed as the literal handoff review (P1) on `deliverables/specialist-return-2026-11-16b.json` with
scopes `/questions`, `/next`, `/limitations`; inventory, review and check files under
`work/handoff-review-rev15/`, hashes in the final response. Reopened afterwards: this note's effect
sentence, the decision table's "Answer needed now?" column, the "What later production still needs"
list and the return's `questions` / `next` / `limitations` were compared with the rows. None promises
more than R1-R9 (a usable local plan and satisfied state gates; not preparation, not readiness for
dispatch, not acceptance), none omits R10-R15, and none turns A1 or A3 into a prerequisite of
`job-prepare`. The `questions` collection carries no owner question that blocks the sample; the owner
answers listed under later production are explicitly not sample-blocking, and the capability input is
addressed to the caller/host, not the owner.

## Decision table (re-derived from the live `pixl_workflow` intake and the focused `pixl_context`; every status unchanged)

"Answer needed now?" means needed before `job-prepare` for `t_sample` / `f_sample` against `c_sample`.
Record hashes are those listed by `pixl_validate` for revision 14; they are the same in revision 15.
Locators per the g note: view = `sources/brief.md` line 20 (verbatim line 5); roster = line 19.

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

No row changed status or value in this increment. Compared row by row with the 2026-11-16 note's table
(lines 195-210): identical.

## Verifiers under this root

`work/verify_rev14.py` (read-only, `e49ba11c...`) was re-run here with `-B -I` on the head before any
write: `problems []`, exit 0; its kit block reports the manifest `e1fb0065...` in its snapshot and
`31b64de8...` now, `kit_changed_since_snapshot true`, three differing kit paths (the table above),
manifest verification `verified`, 260 files. That is the kit/environment drift this note records, not
project-state drift. `work/verify_rev15.py` (read-only) keeps the same record, binding, handoff,
retained-file, note, validator and runner checks for revision 15, adds the 2026-11-16 note, the
revision 14 work files and the caller's revision 14 files to its retained set, starts every runner
subprocess with `-B -I`, and reports `kit_files_now` and `kit_bytecode_cache_dirs` beside the manifest
identity as observations. Its pre-write snapshot `work/rev15-protected-snapshot.sha256` holds 400
entries (139 non-kit, 261 kit, 0 `__pycache__`); every non-kit entry is byte-checked except
`SESSION.md` and the head.

## What later production still needs (unchanged; restated so nothing is dropped)

- `t_sample` done: a nominated candidate passing all five `f_sample.rq` criteria (two mechanical/local
  via the harness under `work/sample-checks/` recorded through `pixl_candidate_review`; three
  visual via `pixl_inspection_prepare` / `pixl_inspection_review`, which need `i_display_scale` and
  benefit from `i_backgrounds`).
- Sequence after `job-prepare` (unchanged from the d note lines 249-255): caller comparison of the
  saved request with the packet, `job-dispatch` (single claim), one host call, `job-observe`,
  `job-import` as an unaccepted X for `f_sample`, then the E/V above.
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
| `work/rev15-protected-snapshot.sha256` | `8f4872b079b393a919fb5b4957983fc9428efd47010da30c8dce00ae4f082dbf` | sha256 of all 400 files present before any write in this increment (`__pycache__` excluded; none existed); read by the verifier |
| `work/build_rev15.py` | `1cce24175089b2c7cb0aa67a3e3b7b138f0e4bfd6f4202b98b3569cb08034c0e` | revision 15 builder (decode head, append 2 records, encode; runner subprocesses with `-B -I`) |
| `work/verify_rev15.py` | `ff0dcb876c1bd2465c596e179eabc83f0df1a9f4781246dba967d0b758151c99` | revision 15 verifier, read-only; kit identity through the manifest; bytecode-cache observation |
| `work/rev15.json`, `work/rev15.px` | produced by the builder after this note is final; `rev15.px` bytes equal the committed head | candidate document and wire |
| `deliverables/continuation-2026-11-16b.md` | bound by `s_continuation_10` | this note |
| `deliverables/specialist-return-2026-11-16b.json` | produced after the commit; hash in the final response | the saved structured return (status, artifacts, checks, request_review, provider, questions, next, limitations, state hashes before/after) |
| `work/handoff-review-rev15/handoff-inventory-01.json`, `handoff-review-01.json`, `handoff-check-01.json` (and `build_review.py`) | produced after the return; hashes in the final response, kept out of the return's file-reference list | literal handoff review of the saved return (P1) |
| `SESSION.md` | edited after the commit; hash in the final response | current-session pointer (new root, revision 15, kit change, P1-P6) |

Nothing else was written. `validate_criteria.py` was **not** run; the v2 validator's print-only run
inside the verifier leaves `criteria-schema-validation.json` (`93643a34...b16a`) unchanged.

## Records added in revision 15 (14 -> 15 delta)

| Record | Kind | Content |
|---|---|---|
| `s_continuation_10` | S (new) | `ur deliverables/continuation-2026-11-16b.md`, `dg` = this note's sha256, `ln [1, N]` with its actual line count, `at 2026-11-16`, `au local` |
| `handoff_11` | N (new) | `wh actor`; `rv 15`; `nx [t_sample]`; `bl [t_scout, t_medic, t_family]`; `fo` = `s_continuation_10` followed by `handoff_10`'s complete list (`s_continuation_9`, `s_continuation_8`, `s_continuation_7`, `s_continuation_6`, `s_sample_brief_v2`, `s_sample_request_review_v2`, `s_sample_criteria`, `s_sample_brief`, `s_sample_request_review`, `s_eval_answers`, `c_sample`, `f_sample`, the 12 non-confirmed I records in state order, `x_aid`, `x_study`) |

Header `PX2 14 -> PX2 15`. Nothing else: all 86 revision 14 records byte-identical (verified against
`work/rev14.json` by `verify_rev15.py`). Revision chain after this commit: 13 -> 14 -> 15 with record
counts 84 -> 86 -> 88; the 16th history copy is the revision 15 wire.

## Earlier notes: what remains applicable (named sections, not wholesale adoption)

- 2026-11-16 note (`continuation-2026-11-16.md`, `157d131c...`, `s_continuation_9`): **Consumer-root
  change** (16-34) remains current and is extended by one row above; **`work/verify_rev13.py` drift**
  (215-239) remains the explanation of that verifier's exit 1 and of `verify_rev14.py`'s design;
  **Decision table** (189-213), **Current-effect worksheet** (144-178) and **What later production
  still needs** (241-257) remain applicable in substance and are re-derived above against the live
  state; **Kit identity observed now** (58-142: hashes, counts, line citations, re-map table, runtime
  citations, dependence statement) is superseded by this note's kit section; **Carrier check**
  (180-187) is superseded in form by P1. Its state identity, files, records and preserved sections are
  history of revision 14. Its statement "the kit directory holds 257 files and no `__pycache__`"
  (65-66) described the previous root at its observation time.
- g note (`continuation-2026-11-15g.md`, `001065a3...`, `s_continuation_8`): **Finding 1** (line 20 /
  line 5 locator; criteria-v2 supersession as a required step of the `provider_arguments` successor
  packet, lines 61-74) remains current and is carried in R13 and P6; **Finding 2** (per-root provenance
  table) remains current and is extended by the root table above; **Effect on the current handoff**
  (127-134) is the same conclusion as this note's effect sentence. Its state identity, files and
  records sections are history of revision 13.
- f note (`continuation-2026-11-15f.md`, `9e0df8a1...`, `s_continuation_7`): **Decision table** (124-150)
  with the two g-note locator corrections, **Operation-effect check** (152-197) and **What later
  production still needs** (199-208) remain applicable in substance and are re-derived above; its kit
  section (49-103) was superseded by the 2026-11-16 note and is now two kit versions old.
- Earlier notes (2026-11-14 through 2026-11-15e) are source evidence only; the d note's sequence
  (lines 249-255) is restated above.

### Superseded, old to new (explicit list)

| Old instruction or text | New | Why |
|---|---|---|
| 2026-11-16 note lines 58-142 (kit hashes, 257-file count, re-map table, dependence statement) | this note's "Kit identity observed now" section (tables A-D, new-file table, dependence statement) | the kit changed a fourth time: three files differ, four are new; the previous numbers describe a kit that is not installed here |
| 2026-11-16 note lines 180-187 (prose carrier check as worksheet item 5) | P1 and the "Carrier check" section: the literal handoff review with `check_handoff.py` | current `intake-sample.md` 147-153 and `handoff-review.md` prescribe the literal review for a saved JSON result |
| `-I` alone as the runner/verifier prescription (`work/verify_rev14.py` 23, `work/build_rev14.py` 13, 2026-11-16 note 48, previous `SESSION.md`) | P2: `-B -I` | `handoff-review.md` 40-42; `-I` alone ignores `PYTHONDONTWRITEBYTECODE` and wrote a cache in the previous root |
| "ignore `pixl-kit/runtime/pixl/__pycache__/`" (previous `SESSION.md`; `CALLER-RESULT-LITERAL-RECONCILIATION.json` 200, 208; v6 126-130, caller files not edited) | P3: no cache exists in this root and none may be created | the cache described was in the 9f6e7c37 root; this root holds none |
| `work/verify_rev14.py` as the current verifier for this root | P5: `work/verify_rev15.py` | revision 15 and the new snapshot; `verify_rev14.py` stays correct for the previous root and still exits 0 here with a kit-change observation |
| 2026-11-16 note worksheet "State/plan identity" (revision 13 on entry, 14 after) and R9 | this note's worksheet (revision 14 on entry, 15 after) | new revision |
| `SESSION.md` as edited in the 2026-11-16 round (`4d95c8c665c348418abc45293fa7c2acf4dc99de5b7148c1df3f5b11aea9bf16`) | `SESSION.md` edited in this increment | new root, revision, kit identity and prescriptions; previous sessions' paragraphs kept as provenance |
| `CALLER-RESULT-LITERAL-RECONCILIATION.json` `remaining_questions` / `next_action` and the 2026-11-16 note's effect sentence, as the current wording of the handoff | this note's effect sentence and the saved return's `questions` / `next` | same conclusion, now built from the re-derived rows and covered by the literal review; the caller file is source evidence for the last round |
| f note lines 79-103 and 2026-11-16 note re-map rows citing them | table A above | two kit versions since the f note; the 2026-11-16 note's re-map is itself re-mapped |

Not superseded: the g note's finding 1 (line 20 / line 5; criteria-v2 supersession step), the g
note's finding 2, every owner requirement in `sources/brief.md`, the sample-scoped controlled-evaluation
answers, every saved criterion and contract, and every historical artifact and acceptance. A new note
cannot supersede owner requirements or source criteria; this list corrects only the agent's own
locators, prescriptions and procedure.

## Preserved and unchanged

All earlier reports, evidence, review files, state history copies (16 after this commit), `work/`
builders and verifiers for revisions 2-14, the research candidates and verdicts, `handoff` through
`handoff_10`, every source byte, both references, `pixl-kit/` (read-only; different version from the
previous root, recorded above; no bytecode cache), `CALLER-RESULT*.json`, `review/*`, the caller's
`work/caller-*` folders and files (including `work/caller-reconciliation-02/`), every `deliverables/*.md`
and `deliverables/sample-request/*` file, and `work/sample-checks/`. `SESSION.md` is again the only
pre-existing file edited besides the head.
