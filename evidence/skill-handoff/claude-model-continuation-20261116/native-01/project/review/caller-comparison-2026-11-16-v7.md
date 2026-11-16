# Caller comparison, version 7 (2026-11-16): handoff-only continuation, revisions 15 and 16

Reviewer: the calling agent (not PIXL). Versions 1 to 6 (`review/caller-comparison-2026-11-15-v1.md` ...
`-2026-11-16-v6.md`, v6 sha256 1c7e717745e00c11ac80b8bc13ff41c0be2c156b9f013bf5b401eea62fc4a0b5) are retained
unchanged. This version reviews the handoff-only increment assigned in the consumer root
`C:/Users/ryanf/AppData/Local/Temp/pixl caller review 249faf48d4f549729dad6842462c74ce/consumer`.

Specialist: native child `a94b4dc767b65b243`, subagent type `pixl:pixl`. One foreground `Agent` round
(revision 15), then one `SendMessage` correction round (revision 16). The correction round was
interrupted twice by the host (once when the previous caller process ended, once by an API rate-limit
error) and resumed each time with `SendMessage` to the same ID. The previous session's child
`a2243e0a858503645` was not resumable here; the delegation said so and described the work as an
artifact-based restart (`delegation.md` 37-44). The specialist's own review is in the b and c notes, its
saved returns and its literal-review files; this file is mine.

## Inputs I read myself before delegation

Entry snapshot: `work/caller-reconciliation-02/entry-snapshot.sha256` (135 non-kit files).

| File | sha256 | What I used it for |
|---|---|---|
| `sources/brief.md` | a78aca77135c5e533b8000272558b5b65e40ee421d1913cab961d7adc4cf5324 | owner brief lines 3-7; 19 roster, 20 side view, 23 canvas not chosen; 11-15 predecessor provenance |
| `sources/controlled-evaluation-answers.md` | 87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30 | lines 5-6 sample-scoped answers, line 8 scope limit |
| `sources/reference-observations.md`, `sources/method-research.md` | d0862d14..., 1b1503b7... | reference measurements and method limits |
| `deliverables/continuation-2026-11-16.md` | 157d131cd3979d2b4e7e1729e4accbd2f8446f3573beed6e0fea543eb68fd420 | current continuation on entry (`s_continuation_9`) |
| `SESSION.md` on entry | 4d95c8c665c348418abc45293fa7c2acf4dc99de5b7148c1df3f5b11aea9bf16 | pointer naming the previous root |
| `CALLER-RESULT-LITERAL-RECONCILIATION.json` | 7b033ec23f1307ab3083e8061fb5456a61fc389085b8b00ac36158d0f03229e3 | previous caller result |
| `review/caller-comparison-2026-11-16-v6.md` | 1c7e7177... | previous caller comparison |
| `state.px/state.px` on entry | 247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af | revision 14, 86 records, ready `[t_sample]`, no jobs |
| `pixl-kit/bundle-manifest.json` | 31b64de8b9fa14a3faacaee21ee21e40883b48bd64c493912aff7ea7aceb564a | **changed** from e1fb0065...; 259 `files` entries plus `generated_files` requirements.txt |
| `pixl-kit/skills/pixl/references/delegation.md` | 72bd2cdfd03333ae0cc3bcd325c4a231f0730ca2f42fbece1955b18b5648199b | 244 lines, read in full; **changed** |
| `pixl-kit/skills/pixl/references/intake-sample.md` | 9fd421030d44e104ff36446409d4562a976daec1650f7a956a950ae8043846ef | 190 lines, read in full; **changed** |
| `pixl-kit/skills/pixl/references/handoff-review.md` | 42f73d779736ce90738542f7d5fb52d78d0f6c65c6ea81ddf151f181f794204f | 126 lines, read in full; **new** |
| `pixl-kit/scripts/check_handoff.py`, `runtime/pixl/handoff_review.py` | ac1afd38..., 5f49e8f3... | **new** literal-review helper and module |
| `pixl-kit/runtime/pixl/lifecycle.py`, `jobs.py`, `platform.py`, `request_review.py` | 5e37cefb..., 18d543f7..., 7693533d..., af7bf5bf... | unchanged; gate lines reopened |

`pixl_readiness` on entry: manifest verified, 260 files checked, no issues; official PixelLab tools not
observed; authentication not verified; named role not observed from static files. `work/verify_rev14.py`
run by me with `-I`: problems `[]`, exit 0, kit change reported as an observation.

## Round 1 (revision 15): what I verified

- `pixl_validate`: revision 15, 88 records, files verified, hash 8284e076c7d3052e69b78e47061b46971fa7b5b81f03e2a41b58cc7a511e565c,
  equal to the head, the 16th history copy and `work/rev15.px`; all 86 revision 14 record hashes identical.
- Sorted wire diff 14 to 15: exactly `s_continuation_10`, `handoff_11` and the header. `handoff_11.fo` is
  `s_continuation_10` followed by `handoff_10.fo`, compared entry by entry.
- Note `deliverables/continuation-2026-11-16b.md`: 6454d5b65397a7d1b647088055dccfb39e5b58173c34218df436584dae8c62f1,
  455 lines equal to the bound line range; it does not contain the revision 15 hash.
- Entry snapshot check: only `SESSION.md` and the head changed; 14 new files, all named by the specialist.
- `work/verify_rev15.py` run by me with `-B -I`: problems `[]`, exit 0, no bytecode cache.
- I re-ran `check_handoff.py` myself into fresh paths under `work/caller-reconciliation-02/`. My inventory
  and my `--review` run reproduced the specialist's `handoff-inventory-01.json` (47f0a535...) and
  `handoff-check-02.json` (fbcd6091...) byte for byte: coverage complete, 78 leaves, 7 carriers matching,
  semantic verdict not assessed.
- Kit and runtime locators opened by me and found to land: `intake-sample.md` 11, 25, 70, 97-104, 106-159,
  128-142, 143-146, 147-153, 161-190, 171-175, 183-188; `delegation.md` 21-23, 25-35, 69, 71-135, 86-97, 128,
  137-157, 145-151, 153, 155; `handoff-review.md` 8-18, 20-24, 37-38, 40-42, 80-93, 107-113, 122-126;
  `check_handoff.py` 9-11; `lifecycle.py` 12-14, 44-77; `jobs.py` 717-743; `platform.py` 869-889, 1017-1023;
  `request_review.py` 130-134; `SKILL.md` 24 and 26; `PROFILE.md` 32 and 44; `readiness.md` 101-102.
- Worksheet rows R1-R9 traced by me through the live authoring context: `t_sample.dp [t_study]` done,
  `f_sample.ct c_sample`, `c_sample.ch` with 4 proposed, 3 observed, 1 confirmed, phase `sample` outside
  the adoption phases, no J records, no families or plans. R10-R15 are request fields enforced by
  `platform.py` that no local file supplies. A1-A3 are permitted alternatives, not prerequisites.

## Findings sent to the same child (one SendMessage, five findings)

| ID | Claim or literal text | Source and locator | Finding | Disposition |
|---|---|---|---|---|
| F1 | b note 78-80: the 261st kit file is `resources/pixl/handoff_review.py`, counted among 260 checked files | `bundle-manifest.json` `files` (259 entries, includes that path) and `generated_files` (requirements.txt, 9cc16454...) | attribution wrong, counts right; specialist also self-reported it | corrected in c note lines 26-35; SESSION.md carries the corrected accounting |
| F2 | b result `/handoff_review/paths` name the `-01` files | `work/handoff-review-rev15/handoff-check-01.json` is the retained coverage-incomplete attempt | a reader following the result lands on the failed check | c result pre-names fresh rev16 files; b result retained as history |
| F3 | b note 265 lists `/status` as a current carrier | revision 15 scopes were `/questions`, `/next`, `/limitations`; `handoff-review.md` 20-24, 37-38 | an authored claim had no review row | c result reviewed with `/status` added |
| F4 | b note 103 cites `handoff_review.py` 122 and 129; b note 255 and b result cite brief-v2 SQ1-SQ4 at 142-171 | `handoff_review.py` 122 and 209; brief-v2 array 142-152, SQ1-SQ4 143-146 | locators wrong | corrected in c note 56-64 and c result `/questions/0/unlocks`, `/next/preparatory_steps_once_Q1_is_supplied/0` |
| F5 | none (environment) | Git Bash rewrote `--scope /questions`; helper error "must be JSON Pointers" | not a kit fault; succeeds with `MSYS_NO_PATHCONV=1` | new prescription P7 in c note 86-89, c result and SESSION.md |

## Round 2 (revision 16): what I verified

- `pixl_validate`: revision 16, 90 records, files verified, hash 762659d9df9a92dd54a6489289ca5824d4d6fd8507016f04db66fb37bb8d9ce2,
  equal to the head, the 17th history copy and `work/rev16.px`; all 88 revision 15 record hashes identical.
- Sorted wire diff 15 to 16: exactly `s_continuation_11` (c note, dg 0758e2aa..., lines 1-123), `handoff_12`
  and the header. `handoff_12.fo` equals `s_continuation_11` followed by the 27 entries of `handoff_11.fo`;
  `nx [t_sample]`, `rv 16`, `wh actor`.
- Note `deliverables/continuation-2026-11-16c.md`: 0758e2aa19caf60fa0c86af9201adb0d5f4774f34239bcc04bc3df5c13dbfa16,
  123 lines; does not contain the revision 16 hash. Each corrected sentence was compared with the b note
  lines it names and with the measured source.
- `deliverables/specialist-return-2026-11-16c.json` (d4b7a54e36116da285cdd59ad4ae958d866ab3f781e7725a29f4e8254253abc1):
  a leaf diff against the b result shows only intended changes in the authored subtrees: status meaning,
  the corrected brief-v2 locator, revision numbers in the expect rule and R9, P1 wording, P3/P5/P6 updated
  to the revision 16 verifier, new P7, and limitations 6-8. `/status` stays `delivered`.
- `work/verify_rev16.py` run by me with `-B -I`: problems `[]`, exit 0; kit unchanged since its snapshot;
  no bytecode cache. Its snapshot holds 419 entries: 158 non-kit, 261 kit, 0 cache paths.
- `SESSION.md` b265cb92fa1da6406a5b816599a83f0c16f2c27f57a858b165fd29c10b190941 names revision 16 and its hash,
  says to read the c note then the b note, and carries the corrected kit accounting and P7.
- Revision 15 artifacts are byte-identical after round 2: b note, b result, the five rev15 review files,
  `work/rev15.px`, `work/verify_rev15.py`.

## Caller observation not sent as a correction

**O1 (worksheet locator completeness, no effect on the conclusion).** `jobs.py` `_blockers` (lines
145-161) adds three job-level gates beyond `lifecycle.py`: connected-plan blockers, PLAR selection bindings
and the task state being open or active. The worksheet cites only `lifecycle.py` for R7 and does not
cite these lines. Each gate is satisfied now and is covered in substance: R7 states no plans,
A2 states no `plar.txt` exists and `t_sample.ip` is empty, and the trace states `t_sample` is open. I did
not request a further revision for a locator-only gap. The next session should read R7 together with
`jobs.py` 145-161.

## Round 2 literal review: what I verified after the completed handback

- The specialist's handback arrived after its second resume. It reported the four files under
  `work/handoff-review-rev16/` produced in one pass with no failed attempt.
- My own `check_handoff.py` runs, using `-B -I`, the selected interpreter and `MSYS_NO_PATHCONV=1`,
  wrote fresh outputs under `work/caller-reconciliation-02/`. My inventory (e936c7c1...) and my
  `--review` check (8c0e309a...) are byte-identical to the specialist's `handoff-inventory-01.json` and
  `handoff-check-01.json`.
- The check is bound to the c result d4b7a54e... with scopes `/status`, `/questions`, `/next` and
  `/limitations`. Coverage is complete: 81 leaves expected and observed, none missing, duplicated,
  unexpected, changed or incomplete. 78 rows compare against sources and 3 metadata rows cover the
  question IDs. All 9 carriers match: b note 188-231, 233-267, 269-302, 304-315, 317-341, 357-373 and
  427-445, and c note 24-69 and 71-96. The semantic verdict stays not assessed.
- I read the `/status`, `/questions/0/unlocks`, `/questions/1/blocks_job_prepare`, `/next/owner_answer_needed`,
  `/next/executable_locally_now` and P7 rows against their cited lines. Each finding follows from those
  lines. Every cited source hash equals the file's current hash, and state rows cite the revision 16 head.
- After the handback: `pixl_ready` returns `[t_sample]`, `pixl_jobs` is empty, `work/verify_rev16.py` reports
  no problems, the kit holds 261 files with no bytecode cache, and my entry snapshot shows only
  `SESSION.md` and the head changed.

## Adoption finding (bound to revision 16, SESSION.md b265cb92...)

I adopt the c note as the current corrections and the b note as the current full continuation, except
for the sentences the c note corrects. The revision 15 handoff was structurally correct and its kit and
runtime citations landed. Its five defects were a kit-file attribution, a result pointer to a failed check,
an unreviewed `/status` carrier, two locators and an undocumented shell behaviour. All five are corrected
in the same child with explicit old-to-new text, and every revision 15 artifact is retained unchanged.
The worksheet conclusion holds. No owner answer is needed for `job-prepare` on `t_sample` against
`c_sample`. The operation stays blocked on capability inputs and on the `provider_arguments` successor packet,
which includes the criteria-v2 supersession and the caller comparison. `i_display_scale` is needed before
visual review only. Observation O1 above is carried in my saved result. Nothing was generated, accepted or
decided, and no intake or task status changed.

Reviewer: calling agent, 2026-11-16. Specialist output and caller review are distinct files.
