# Caller comparison, version 5 (2026-11-15): handoff-only continuation (revisions 12 and 13)

Reviewer: the calling agent (not PIXL). Versions 1 to 4 (`review/caller-comparison-2026-11-15-v1.md`
77fe69e4fea8044bea62f42389b4831e2d6e3887ecd3604c9b5c2efacd84dc1c; `-v2.md`
c40843fe5c62c19c8b075fa62ef2552981bdadc7e6be176e727e254a7a8ef4e3; `-v3.md`
40161d6ac7216f30d0015a0ca35c3fade08d93f4a58515ff5f63ee84224df886; `-v4.md`
0c2f864ed056d9f0b2b30596d9c6461b2ad6c744a9ce9d5d81b931a58a1e7a58) reviewed revisions 7 to 11 and are
retained unchanged. This version reviews the handoff-only increment assigned in this invocation: the
specialist's revision 12 return, my findings, and its revision 13 correction.

Specialist: native child `aa5b126379050c057`, subagent type `pixl:pixl`, one foreground `Agent` round
(revision 12) and one `SendMessage` continuation of the same child carrying two findings and one
extension (revision 13). Its own review is in `deliverables/continuation-2026-11-15f.md`,
`deliverables/continuation-2026-11-15g.md` and its returned JSON results; this file is mine and is
distinct from it.

## Invocation facts

- Consumer root (current): `C:/Users/ryanf/AppData/Local/Temp/pixl caller review a97de5914a21428aad2fef3c65ecfcec/consumer`.
  The previous session's root (`...e3c7ebe124824b69828309bf1645f322/consumer`) is named in the retained
  `SESSION.md` on entry, the d note and `CALLER-RESULT-PREREQUISITES.json`; it is provenance.
- Kit `pixl-kit/` inside the root (read-only); interpreter `C:/github/pixel-lab-agent/.venv/Scripts/python.exe`.
- Assignment: handoff-only. No request packet, fixture, generation, provider, candidate, verdict,
  evidence, intake or task-state work. No new owner answers; the controlled-evaluation answers remain
  applied within their sample scope.

## Inputs I read myself before delegation (entry snapshot: `work/caller-prereq-02/entry-snapshot.sha256`)

| File | sha256 | Role |
|---|---|---|
| `sources/brief.md` | a78aca77135c5e533b8000272558b5b65e40ee421d1913cab961d7adc4cf5324 | owner brief, verbatim; lines 19-23 reopened for the locator finding |
| `sources/controlled-evaluation-answers.md` | 87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30 | sample-scoped answers (lines 5, 6, 8); already applied; unchanged |
| `deliverables/continuation-2026-11-15e.md` | f174f93971f3044b9731aae34e2704d5e090c5468761361063548d15056d597f | continuation on entry (s_continuation_6) |
| `deliverables/continuation-2026-11-15d.md` (lines 130-282) | 826460e5ff96f7dae2bccff8b8df1278e5457614cfaadd3c0510e0f64feeb1dc | decision table, operation-effect trace, later production needs |
| `deliverables/sample-request/request-review-v2.json` | a596f02addb73ba1c7732cfe05a8071b97b7c7236f26e349fdca5184e0684d73 | current pre-discovery packet (kind creative_brief, not executable) |
| `SESSION.md` on entry | c2bae63cd381e9d9a8e67fdc3f45981bad82cdc1e101f6e84ee21aeb738557aa | pointer naming the previous root |
| `CALLER-RESULT-PREREQUISITES.json` | aac96bb8504edb22bac03aa5da94218970f6715c5d5069fa3988e08bf5800fcf | previous caller result (revisions 10-11), read for continuity and format; unchanged |
| `review/caller-comparison-2026-11-15-v4.md` | 0c2f864ed056d9f0b2b30596d9c6461b2ad6c744a9ce9d5d81b931a58a1e7a58 | previous caller comparison; unchanged |
| `state.px/state.px` on entry | 720a1a1ecc59f210654485f4e279b1cb58dd881629ece37ef2db323c1ecec443 | revision 11, 80 records, valid, files verified, ready [t_sample], no jobs (pixl_validate / workflow / ready / jobs) |
| `pixl-kit/skills/pixl/references/delegation.md` | 43f086a02bf772df9f6f96342514f335aa65eef52af253746ac1d998a5da1b47 | caller/specialist contract; "Caller: review a cold continuation" lines 71-132 |
| `pixl-kit/skills/pixl/references/intake-sample.md` | 55fe94fcdfaff27eff35fbb0a8cc56c2c2ddee95daafd14f062b4ee8e8a2b959 | operation-effect check (70-129), cold intake handoff (131-159) |
| `pixl-kit/skills/pixl/references/state-authority.md` | 4f883c6832d63a5e8ff134f69dbbf6d90abdc96c3004b39cae7aec6a87715112 | observed provenance dates; commit with expected hash |
| `pixl-kit/agents/pixl.md` / `skills/pixl/SKILL.md` | 34187821f9875c880e703588065ec62dc7a85e1a044b5c7565825c200b7b10b9 / 04a46dae9b55e5e54eec5b1a033e6e597f3e44170d930e96da3554289b34a5a2 | role and skill (read-only) |
| `pixl-kit/bundle-manifest.json` | cc38dcf31fa55f68866092b005f6fb790e20255ffb408cee89b1083dc4ef9354 | manifest; verified by pixl_readiness (256 files, no issues) |
| `pixl-kit/runtime/pixl/lifecycle.py` (44-77), `jobs.py` (717-743), `platform.py` (866-889, 1017-1023) | 5e37cefb... / measured in result file | gate code behind the next operation |

`work/verify_rev11.py` run by me with the selected interpreter (`-I`): `problems []`, exit 0.

Kit observation: `bundle-manifest.json`, `delegation.md` and `intake-sample.md` hash differently from the
previous caller's record (fe355d44..., 2ca298b9..., 8da6141b...). Readiness verified every listed file
against the current manifest, so this is a kit version change between evaluation roots, as in version 4.
The previous bytes are not retained here; I compared the specialist's citations against the current text.

## Round 1 (revision 12): what I verified

- `pixl_validate`: valid, format 2, revision 12, 82 records, files_verified true, hash
  f6b2c25456d1abbc49bf4e6f6d1305749bf2e0b105738428f066f14b3070e632; equals head sha256, the history copy
  and `work/rev12.px`. All 80 revision 11 record hashes identical. `pixl_ready` [t_sample]; `pixl_jobs` [].
- Sorted line diff rev 11 -> rev 12: exactly `s_continuation_7`, `handoff_8` and the header.
- `sha256sum -c` of my entry snapshot: only `SESSION.md` and `state.px/state.px` changed; every other
  pre-existing file byte-identical. New files: f note, `work/build_rev12.py`, `work/verify_rev12.py`,
  `work/rev12.json`, `work/rev12.px`, `work/rev12-protected-snapshot.sha256`, the rev 12 history copy.
- `work/verify_rev12.py` (`-I`): `problems []`, exit 0. f note 243 lines (= `s_continuation_7.ln`), no
  occurrence of the rev 12 hash.
- Citations opened by me: intake-sample.md 11, 70-129, 106-108, 131-159, 141-143, 154-159; delegation.md
  21-23, 25-35, 71-132, 134-154, 150-153; lifecycle.py 44-77 (gates and ADOPTION_PHASES), jobs.py 717-743
  (job_exists, blockers, pending, prepare_discovered), platform.py 873-889 (discovery/authorization
  fields, nonempty evidence, schema validation) and 1017-1023 (observed_at not in the future);
  CALLER-RESULT.json lines 93 and 105; brief-v2 line 100; eval answers lines 5-6; brief line 23. All
  say what the f note claims.
- `handoff_7.fo` reopened in the wire: it indeed lacks `i_sampling`, `i_alpha`, `i_lighting`; `handoff_8`
  adds them (specialist's stated rule: every non-confirmed I record). A choice, consistent with
  intake-sample.md line 143 ("observed and proposed policies ... cannot silently gain confirmation").
- Decision table: every status re-read from `pixl_workflow` intake matches the f note rows.
- Operation-effect check for `job-prepare` on `t_sample`: I traced `t_sample.dp [t_study] done`,
  `f_sample.ct c_sample`, `c_sample.ch` eight choices none unresolved/conflict, phase `sample` so
  adoption gates do not apply, no J records, no families; agrees with the note and with `pixl_workflow`
  blockers `[]`. Missing inputs are provider identity, tool name, live inputSchema, exact arguments,
  discovery object, authorization evidence: capabilities, not owner answers. Consistent.
- Caller reruns: `validate_criteria_v2.py` print-only exit 0 (schema_valid true, all bounds inside
  files), retained artifact still 93643a34...; harness exit codes 0 0 1 1 1 on the two references and
  three fixtures.

## Findings sent to the same child (SendMessage, two messages)

**F1 (locator error, inherited).** f note line 137 cites `s_brief` line 19 for the confirmed side view.
`sources/brief.md` line 19 is the roster; line 20 is "Destination: a side-view game." (line 5 verbatim).
Extension: the same "line 19 = side-view" locator is in the bound pre-discovery artifacts
`sample-criteria.json` line 74 (`[19, 19]` for q_sample_readability), `sample-creative-brief.json` line 81,
`sample-creative-brief-v2.json` line 110, `request-review.json` line 9, `request-review-v2.json` line 19,
and the previous caller comparison v4 lines 53 and 85 claimed to have checked line 19. The validator
checks only that bounds lie inside the file. No state record carries a line number (`i_view.wy`,
`q_sample_readability.ck`), so the state is not wrong. Requested disposition: record in the g note with
old-to-new; keep bound bytes; make a v2 criteria file (`[20, 20]`) and corrected locators a required
step of the next packet (the provider_arguments successor), not a new packet in this handoff-only
increment.

**F2 (provenance misattribution, SESSION.md).** SESSION.md after round 1 attributed revision 11 and the
e note to the e3c7ebe1 session and revisions 6-10 and notes a-d to earlier sessions. Evidence:
`CALLER-RESULT-PREREQUISITES.json` (root e3c7ebe1) records revisions 10 and 11 (9 -> 11) with notes d
and e; e note line 3 ("Same session ... as continuation-2026-11-15d.md"); d note lines 9-10 name the
e3c7ebe1 root; `CALLER-RESULT.json` (root ca2b0073) reports revision 8 and `CALLER-RESULT-ANSWER-STATE.json`
(root d31ffb17) reports revision 9. The wording was inherited from the entry SESSION.md.

## Round 2 (revision 13): what I verified after the correction

- `pixl_validate`: valid, format 2, revision 13, 84 records, files_verified true, hash
  42db4c758d328c521c1f73baae1873b56b14e8a4d4d1b580c1d720dcecd8acd2; equals head sha256, the history
  copy and `work/rev13.px`. All 82 revision 12 record hashes identical (including `s_continuation_7`
  169bb7c8... and `handoff_8` 90eec522...). `pixl_ready` [t_sample]; `pixl_jobs` [].
- Sorted line diff rev 12 -> rev 13: exactly `s_continuation_8` (dg 001065a3..., ln [1,134], at
  2026-11-15, au local), `handoff_9` (rv 13, nx [t_sample], bl [t_scout, t_medic, t_family], fo =
  s_continuation_8 + handoff_8's list) and the header `PX2 12 -> PX2 13`.
- `sha256sum -c` of my entry snapshot: still only `SESSION.md` and `state.px/state.px` changed. The f note
  (9e0df8a1...), all rev 12 work files and every bound packet file are byte-identical.
- `work/verify_rev13.py` (`-I`) on the head: `problems []`, exit 0. `work/verify_rev12.py` on `work/rev12.px`:
  `problems []`. g note 134 lines (= `s_continuation_8.ln`), no occurrence of the rev 13 hash.
- F1 correction checked against the sources: brief.md lines 19/20/5 as stated; `s_brief.ln [1, 33]` (whole
  file); `q_sample_readability.so` = [s_methods, s_refobs, s_continuation_2] and `i_view` carry no line, so
  "no state record is wrong" holds. The required next-packet step (criteria v2 at [20, 20], validated with
  `validate_criteria_v2.py --out <fresh>`, bound beside `s_sample_criteria`, check texts unchanged) is
  consistent with delegation.md lines 28-35 (source pointers correctable; both identities retained) and does
  not exceed the handoff-only assignment.
- F2 correction checked against the retained results: `CALLER-RESULT.json` lines 6-7, 23-24 (root ca2b0073,
  revisions 6 -> 7 -> 8, notes 2026-11-15 and 15b); `CALLER-RESULT-ANSWER-STATE.json` lines 6-7, 24 (root
  d31ffb17, 8 -> 9, note c); `CALLER-RESULT-PREREQUISITES.json` (root e3c7ebe1, 9 -> 10 -> 11, notes d, e);
  `continuation-2026-11-14.md` line 4 ("Resumed from ... revision 5"); the 14 history files form the chain
  PX2 0..13 with record counts 3, 40, 44, 48, 49, 54, 57, 61, 63, 71, 76, 80, 82, 84. SESSION.md (2bf8396a...)
  now states exactly this attribution and names revision 13, the g note and the f note.
- Decision table and operation-effect check: unchanged from round 1 except the two locators; every I record
  hash unchanged, so no status moved. `blocked_on` in the g note, SESSION.md and the returned result agree:
  capability inputs only, no owner answer.

## Adoption finding (bound to revision 13)

The specialist's revision 12 handoff was structurally correct and its runtime and kit citations were exact,
but it carried forward an inherited wrong source locator and an inherited provenance misattribution. Both
were corrected in revision 13 through a successor note and the editable session pointer, with explicit
old-to-new statements and every historical identity retained. I adopt the g note plus f note as the current
continuation. Nothing was generated, accepted, decided or changed in intake or task state in this invocation.

Reviewer: calling agent, 2026-11-15. Specialist output and caller review are distinct files.
