# Caller comparison, version 6 (2026-11-16): handoff-only continuation (revision 14)

Reviewer: the calling agent (not PIXL). Versions 1 to 5 (`review/caller-comparison-2026-11-15-v1.md` ...
`-v5.md`, v5 sha256 5c4b6ff5d35bc971688f742a88d02aca9b97c96a7ea7b73dfd42fdf82b006ad8) reviewed revisions 7 to 13
and are retained unchanged. This version reviews the handoff-only increment assigned in this invocation:
the specialist's revision 14 return, my findings, and its one SESSION.md correction.

Specialist: native child `a2243e0a858503645`, subagent type `pixl:pixl`, one foreground `Agent` round
(revision 14) and one `SendMessage` continuation of the same child (SESSION.md wording correction). Its own
review is in `deliverables/continuation-2026-11-16.md` and its two returned results; this file is mine.

## Invocation facts

- Consumer root (current): `C:/Users/ryanf/AppData/Local/Temp/pixl caller review 9f6e7c37402f4037acf44abe70f04834/consumer`.
  The previous root (`...a97de5914a21428aad2fef3c65ecfcec/consumer`) is named in the entry `SESSION.md`, the f and g
  notes, `CALLER-RESULT-PREREQUISITES-02.json` and v5; it is provenance.
- Kit `pixl-kit/` inside the root (read-only); interpreter `C:/github/pixel-lab-agent/.venv/Scripts/python.exe`.
- Assignment: handoff-only. No request packet, fixture, generation, provider, candidate, verdict, evidence,
  intake or task-state work. No new owner answers; the controlled-evaluation answers remain applied within
  their sample scope (`sources/controlled-evaluation-answers.md` lines 5, 6, 8).

## Inputs I read myself before delegation (entry snapshot: `work/caller-reconciliation/entry-snapshot.sha256`, 123 non-kit files)

| File | sha256 | What I used it for |
|---|---|---|
| `sources/brief.md` | a78aca77135c5e533b8000272558b5b65e40ee421d1913cab961d7adc4cf5324 | owner brief; lines 5, 6-7, 11-15, 19, 20, 23 reopened |
| `sources/controlled-evaluation-answers.md` | 87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30 | sample-scoped answers; unchanged |
| `deliverables/continuation-2026-11-15g.md` | 001065a3422bfb76997b375f9f66d22324e87a2841eb06d742e166d44fef2e4f | current corrections on entry (s_continuation_8) |
| `deliverables/continuation-2026-11-15f.md` | 9e0df8a1d8d4bbfa6591d16fffe07406f53c639d32b797e320232b15177a135f | full continuation on entry (s_continuation_7); kit table lines 59-69, citations 79-103 |
| `SESSION.md` on entry | 2bf8396a8c519da76af8091e7817d4c47597bebfff2ecf3658896411f3717a92 | pointer naming the previous root and revision 13 |
| `CALLER-RESULT-PREREQUISITES-02.json` | 03e4dfeca7dd0e618ffdaffe786b3c5b05e446426ae722fba53869b97961e2df | previous caller result (revisions 12-13); format and provenance |
| `review/caller-comparison-2026-11-15-v5.md` | 5c4b6ff5d35bc971688f742a88d02aca9b97c96a7ea7b73dfd42fdf82b006ad8 | previous caller comparison |
| `state.px/state.px` on entry | 42db4c758d328c521c1f73baae1873b56b14e8a4d4d1b580c1d720dcecd8acd2 | revision 13, 84 records, valid, files verified, ready [t_sample], no jobs |
| `pixl-kit/bundle-manifest.json` | e1fb00650c4526b26584aae83b7989ff3d56892045bfb1fe2e975598968dd398 | kit manifest; **differs** from the f note's cc38dcf3... |
| `pixl-kit/skills/pixl/references/delegation.md` | 2f5af8b5339daaef3402eacb5fc532a0123cafeb0b8b2c5fc990c1221ab5bdc5 | 245 lines (**was** 43f086a0..., 241); read in full |
| `pixl-kit/skills/pixl/references/intake-sample.md` | b24dad8e654215d04b3229b3d7b08b2c06b32cb1442cdf53c49b066776fe47f6 | 188 lines (**was** 55fe94fc..., 161); lines 60-188 read |
| `pixl-kit/agents/pixl.md`, `skills/pixl/SKILL.md`, `resources/agent/PROFILE.md`, `references/state-authority.md` | 34187821..., 04a46dae..., 8aeaedb1..., 4f883c68... | unchanged from the previous record |
| `pixl-kit/runtime/pixl/lifecycle.py`, `jobs.py`, `platform.py`, `request_review.py` | 5e37cefb..., 18d543f7..., 7693533d..., af7bf5bf... | unchanged; gate lines reopened after the return |
| `work/verify_rev13.py` | 270d6c4416c4792a1c2ebfdc33601d09ec98a83cc19203434ee0b35ccfbbd78b | run by me with `-I` on entry: exit 1, 20 problems, all kit-identity (3 drifted kit files, 17 missing `__pycache__` entries) |

`pixl_readiness` (host claude, installation pixl-kit) run by me on entry: manifest verified, 256 files, no
issues; Python 3.14.3; official PixelLab tools not observed; named_role not observed from static files.
Kit observation: the kit changed version between evaluation roots for the third time in this series; the
previous bytes are not retained here, so citations were checked against the current text.

## Round 1 (revision 14): what I verified

- `pixl_validate`: valid, format 2, revision 14, 86 records, files_verified true, hash
  247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af; equals head sha256, the 15th history
  copy and `work/rev14.px` (`cmp` identical). All 84 revision 13 record hashes identical. `pixl_ready`
  [t_sample]; `pixl_jobs` [] (remote_executed false).
- Sorted line diff rev 13 -> rev 14: exactly `s_continuation_9` (ur the new note, dg 157d131c..., ln [1,309],
  at 2026-11-16, au local), `handoff_10` (rv 14, nx [t_sample], bl [t_scout, t_medic, t_family], wh actor,
  fo = s_continuation_9 + handoff_9's 25 entries, compared entry by entry) and the header `PX2 13 -> PX2 14`.
- Note `deliverables/continuation-2026-11-16.md`: sha256 157d131cd3979d2b4e7e1729e4accbd2f8446f3573beed6e0fea543eb68fd420,
  309 lines (= `s_continuation_9.ln`); zero occurrences of the revision 14 hash.
- `sha256sum -c` of my entry snapshot: only `SESSION.md` and `state.px/state.px` changed; no file missing.
  New non-kit files: the note, the revision 14 history copy, `work/build_rev14.py`, `work/verify_rev14.py`,
  `work/rev14.json`, `work/rev14.px`, `work/rev14-protected-snapshot.sha256` (381 entries: 124 non-kit,
  257 kit, 0 `__pycache__`).
- `work/verify_rev14.py` (`-I`) run by me on the head: `problems []`, exit 0; kit block reports manifest
  e1fb0065... in snapshot and now, verification `verified`, 256 files, `kit_changed_since_snapshot false`.
  I read its body: non-kit snapshot entries are byte-checked except the two edited on purpose, kit entries
  are compared but reported as observations, `__pycache__` paths skipped, the runner's readiness manifest
  verification is required, `validate_criteria_v2.py` print-only, runner workflow/jobs checked.
- Locators in the note opened by me and found to land: `intake-sample.md` 11, 25, 70, 97, 106-126, 129,
  142-145, 146-151, 159-188, 169-173, 171, 181-186; `delegation.md` 21-23, 25-35, 69, 71-136, 88, 138-158,
  146-152, 154, 156; `lifecycle.py` 44-77 (49-52 task_prerequisite, 53-56 output_contract, 57-64
  choice_unresolved/conflict, 65-75 ADOPTION_PHASES gates, 76 families); `jobs.py` 731-741; `platform.py`
  869-889, 1018-1023; `request_review.py` 132; `SKILL.md` line 26 (quoted sentence present); `PROFILE.md`
  32 and 44; `state-authority.md` 13; `sources/brief.md` 5, 6-7, 11-15, 19, 20, 23; `verify_rev13.py`
  114-124; g note 61-72; f note 11-26, 49-103, 124-150, 132-147, 152-197, 190-197, 199-208. The phrase
  "cannot silently gain confirmation" (quoted by v5 line 73 from the old kit) is absent from the current
  `intake-sample.md`, as the note states. The g note cites no kit file by line (grep).
- Decision table: all 14 record-hash prefixes match `pixl_validate`; statuses unchanged by construction
  (identical record hashes) and re-read against the revision 13 `pixl_workflow` intake list.
- Worksheet rows R1-R9: traced by me through `t_sample.dp [t_study] done`, `f_sample.ct c_sample`,
  `c_sample.ch` (4 proposed, 3 observed, 1 confirmed, none unresolved/conflict), phase `sample` outside
  `ADOPTION_PHASES`, no J records, no families; agrees with `pixl_workflow` blockers `[]` for `t_sample`.
  R10-R15: every missing input is a request field enforced by `platform.py` 869-889 / 1018-1023 that no
  local file supplies; none is an owner art decision. A1-A3 are source-permitted alternatives, not
  prerequisites of `job-prepare`. The effect sentence and SESSION.md final wording promise no more than this.
- Specialist choices preserved as choices: worksheet rows R1-R15/A1-A3 as the claim set; decision table
  retained as a layout under current `intake-sample.md` 97; kit identity recorded through the manifest in
  `verify_rev14.py` instead of per-file kit protection; bytecode cache left in place and disclosed.

## Finding sent to the same child (SendMessage, one message)

**F1 (environment-dependent claim stated unconditionally, SESSION.md).** The round-1 `SESSION.md`
(e146b2a3ec9aaff3f70cd1d9176bc7bfcb81a9952770255dff0f8292232fa1b5) said the builder and verifier runner
subprocesses write a 17-file bytecode cache under `pixl-kit/runtime/pixl/__pycache__/`. Evidence: my
`verify_rev13.py` run on entry invoked the runner the same way and wrote none (257 kit files, no cache
afterwards; my shell has `PYTHONDONTWRITEBYTECODE=1`); the 17 `.pyc` files are timestamped 03:15:44.83,
0.4 s after the specialist's pre-write snapshot; `pixl-kit/scripts/pixl.py` sets no bytecode option.
Requested: reword that sentence in `SESSION.md` only (entry state, what wrote the cache and under which
condition, not payload / not manifest-listed / excluded by snapshot and verifier, may or may not recur);
no new revision, note or deletion.

## Round 2 (SESSION.md correction): what I verified

- `SESSION.md` now 4d95c8c665c348418abc45293fa7c2acf4dc99de5b7148c1df3f5b11aea9bf16; the old phrase
  occurs 0 times; the replacement states the entry state, the cause (the specialist's direct
  `python -I pixl-kit/scripts/pixl.py ...` calls; `-I` implies `-E`, which ignores
  `PYTHONDONTWRITEBYTECODE`), that builder/verifier subprocesses and my shell wrote none, non-payload
  status, exclusion by snapshot and verifier, and that recurrence depends on the setting. I reproduced
  the cause: with the selected interpreter, `sys.dont_write_bytecode` is `False` under `-I` and `True`
  without it in this shell. Every other sentence of `SESSION.md` reads as in the round-1 version.
- State unchanged: head sha256 still 247b22ba...; note still 157d131c...; 15 history files; `verify_rev14.py`
  (`-I`) `problems []`, exit 0; entry snapshot still differs only in `SESSION.md` and `state.px/state.px`.
- Kit: 274 files = 257 payload (manifest-listed 256 + manifest) + 17 cache files; manifest verification
  unaffected (verifier kit block). The bound note's statement "257 files and no `__pycache__`" (lines
  65-66) was true at its observation time; the current fact is carried by `SESSION.md`.

## Adoption finding (bound to revision 14, SESSION.md 4d95c8c6...)

The specialist's revision 14 handoff is structurally correct, its kit and runtime citations are exact
against the current kit version, its re-map of the f note's citations into the two changed reference
files is accurate where I could check it against the current text, and its worksheet does not convert
alternatives into prerequisites or a usable plan into readiness. The one discrepancy was an unconditional
statement about an environment-dependent side effect in the mutable pointer; it was corrected in the same
child with the cause identified and reproduced. I adopt `deliverables/continuation-2026-11-16.md` as the
current continuation, with the g note's findings 1 and 2 and the f note's decision table, operation-effect
check and later-production list as the applicable source sections it names. Nothing was generated,
accepted, decided or changed in intake or task state in this invocation.

Limitation I carry forward: the Python interpreter wrote a bytecode cache into the read-only kit during
the specialist's direct runner calls. It is not kit payload and I did not delete it (a deletion would be a
further write into the kit, and any default-environment runner call would recreate it); the next session
should treat `pixl-kit/runtime/pixl/__pycache__/` as ignorable and may set `PYTHONDONTWRITEBYTECODE=1`
without `-I` on the runner, or pass `-B`, to avoid recreating it.

Reviewer: calling agent, 2026-11-16. Specialist output and caller review are distinct files.
