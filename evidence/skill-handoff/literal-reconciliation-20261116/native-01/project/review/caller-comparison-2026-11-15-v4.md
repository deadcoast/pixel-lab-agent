# Caller comparison, version 4 (2026-11-15): pre-discovery sample packet and local tooling (revisions 10 and 11)

Reviewer: the calling agent (not PIXL). Versions 1 to 3 (`review/caller-comparison-2026-11-15-v1.md`
77fe69e4fea8044bea62f42389b4831e2d6e3887ecd3604c9b5c2efacd84dc1c; `-v2.md`
c40843fe5c62c19c8b075fa62ef2552981bdadc7e6be176e727e254a7a8ef4e3; `-v3.md`
40161d6ac7216f30d0015a0ca35c3fade08d93f4a58515ff5f63ee84224df886) reviewed revisions 7, 8 and 9
and are retained unchanged. This version reviews the two returns of this session's specialist
(revision 10, then revision 11 after my findings) against the brief, the retained sources and the
installed runtime, and binds my adoption finding to revision 11.

Specialist: native child `a2b7a4ab9b3fa3467`, subagent type `pixl:pixl`, one foreground round
(revision 10) and one `SendMessage` continuation of the same child (revision 11). Its own review
is in `deliverables/continuation-2026-11-15d.md`, `deliverables/continuation-2026-11-15e.md` and
its two returned JSON results; this file is mine and is distinct from it.

## Inputs I read myself before delegation (entry snapshot)

| File | sha256 | Role |
|---|---|---|
| `sources/brief.md` | a78aca77135c5e533b8000272558b5b65e40ee421d1913cab961d7adc4cf5324 | owner brief, verbatim |
| `sources/controlled-evaluation-answers.md` | 87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30 | sample-scoped answers, already applied in rev 9; no new answers this invocation |
| `sources/reference-observations.md` | d0862d144da0c4b315af96a8129846b32075fac99826b618ad51c62b6a960495 | measured study (x_study) |
| `sources/method-research.md` | 1b1503b7a004c884b5b207a965aa85ac4c694f481d2936619a4030557f794e51 | method excerpts |
| `reference.png` / `reference-b.png` | d997cade...70aa7 / e76b40ce...14a12a | owner references, unchanged |
| `deliverables/continuation-2026-11-15c.md` | fd3f500708a1559162e0bc2da4c37d5201ec427a0c1aca90659695978b4e828b | continuation on entry (s_continuation_4) |
| `deliverables/continuation-2026-11-15.md`, `-15b.md`, `-14.md`, `outline-decision-brief.md` | d2114fc7..., 351f2863..., d9755b26..., 32b59ab7... | earlier notes, unchanged |
| `CALLER-RESULT-ANSWER-STATE.json`, `review/caller-comparison-2026-11-15-v3.md` | b2b99880..., 40161d6a... | previous caller result and comparison, read for continuity; unchanged |
| `state.px/state.px` on entry | fdf4ebfe7d2dc1565a9c003c28d61ecfa5b255ec19937198aa11d405c38b8ca1 | revision 9, 71 records, valid, ready [t_sample], no jobs (pixl_validate / workflow / ready / jobs) |
| `pixl-kit/runtime/pixl/request_review.py` (lines 130-134) | af7bf5bf1f599a03645d12e6faadb14db050dec5a31eae067ed3fc36295a1c23 | the review tool requires `request.kind == provider_arguments` |
| `pixl-kit/runtime/pixl/asset-plan.schema.json` | ac8161b495126dc75942b7ce4f20694f86dc192f2083f6fcab5bb0786c86af2e | criteria-plan schema |
| `pixl-kit/runtime/pixl/lifecycle.py` (lines 44-77, 125-138) | 5e37cefb2bcb357373332af4970b7c30df4e18df6d78e36022fe349a616a6a23 | gate and pin rules |
| `pixl-kit/skills/pixl/references/delegation.md`, `request-review.md`, `intake-sample.md`, `pixellab-operations.md`, `provider-recovery.md`, `state-authority.md`, `artistic-authority.md`, `readiness.md`, `everyday.md`; `pixl-kit/agents/pixl.md`; `pixl-kit/skills/pixl/SKILL.md` | 2ca298b9..., 98ac6d9d..., 8da6141b..., aae21df1..., 2956a617..., 4f883c68..., f46ba508..., fd915689..., 3a700e36...; 34187821...; 04a46dae... | kit contracts (read-only) |
| `pixl_capabilities` | retrieved 2026-09-11, `live_discovery: false` | dated documentation, not discovery |
| `pixl_readiness` (host claude, installation pixl-kit) | bundle manifest verified, 256 files; Python 3.14.3, pillow 12.3.0, jsonschema 4.26.0; official PixelLab tools not observed; named_role not_observed from static files | runtime facts |

Kit observation: the installed `delegation.md` hashes 2ca298b9..., while the previous caller's
result recorded a147f5c8... for the same path. `bundle-manifest.json` (fe355d44...) lists
2ca298b9... and readiness verified all 256 files, so this is a kit version change between
evaluation roots, not corruption. Nothing in this session depends on the difference.

## What I verified after each specialist return

**Revision 10 (first return).** `pixl_validate`: valid, rev 10, 76 records, files verified, hash
23f4ee559508bab7b1966348589c1431604b848b804f7e6599940e48b06968c6; every one of the 71 prior
record hashes identical to revision 9. Sorted line diff rev 9 to rev 10: exactly `s_sample_brief`,
`s_sample_criteria`, `s_sample_request_review`, `s_continuation_5`, `handoff_6` and the header.
`pixl_ready` [t_sample]; `pixl_jobs` []; `pixl_workflow` blockers identical to entry. Every
protected file re-hashed unchanged. I reran `work/verify_rev10.py` (-I): problems []. I reran
the harness on both references and the three fixtures: exit codes 0 0 1 1 1. I compared
`sample-criteria.json` with the state records through `work/rev10.json`
(`work/caller-compare-criteria.py`): all five check texts equal the Q `ck` fields, intent equals
`c_sample.li`, size/palette equal `px`/`pl`, domain/mode equal, `wh` actor x4 and user x1. I
opened every cited line range: brief.md 3-7, 19, 21-22, 23; controlled-evaluation-answers 5, 6,
8; reference-observations 17, 20-29, 23, 24, 25-28, 29, 33-35, 37-40, 66-69; method-research
15-16, 41-55; continuation-2026-11-15 83-93, 94-98. All say what the packet claims.

**Caller-induced incident, corrected.** Reproducing the criteria validation exactly as the v1
script's docstring instructed overwrote `criteria-schema-validation.json` (93643a34... became
82d7df80...; only `validated_at` differed). I restored the original bytes exactly by recovering
the timestamp against the recorded hash (`work/caller-restore-validation.py`, recovered
`2026-11-15T23:58:43+00:00`; hash again 93643a34...). This became finding 1 below.

**Revision 11 (after my findings).** `pixl_validate`: valid, rev 11, 80 records, files verified,
hash 720a1a1ecc59f210654485f4e279b1cb58dd881629ece37ef2db323c1ecec443; all 76 revision 10 record
hashes identical. Sorted diff rev 10 to rev 11: exactly `s_sample_brief_v2`,
`s_sample_request_review_v2`, `s_continuation_6`, `handoff_7` and the header. `pixl_ready`
[t_sample]; `pixl_jobs` []. History holds 12 files; rev 9 and rev 10 copies unchanged. Every
protected file and every revision 10 artifact (v1 brief, criteria, v1 packet, 93643a34 artifact,
v1 script, d note, shortlist, harness, fixtures, dry run) re-hashed unchanged. I reran
`work/verify_rev11.py` (-I): problems []. I ran `validate_criteria_v2.py` print-only (exit 0,
schema_valid true, 18/18 bounds) and with `--out` to an existing path (exit 2, refused); the
retained artifact still hashes 93643a34... after both. The composed `c_sample.li` string in the
v2 brief is unchanged. `SESSION.md` (c2bae63c...) names the rev 11 head, the e note, the v2
packet and the v2-only reproduction instruction while keeping the predecessor lines.

## Claim-by-claim comparison (final artifacts, revision 11)

| Claim or literal clause | Source and locator | Authority / status | Change actually made | Operation prerequisite | Finding and disposition |
|---|---|---|---|---|---|
| The next operation (job-prepare for t_sample) cannot run locally; a creative brief is the right pre-discovery artifact and must not be labelled executable | `request-review.md:25`; `provider-recovery.md:10, 35`; `pixl_readiness` (official tools not observed); `request_review.py:130-134` | runtime fact | brief v1/v2 with `kind creative_brief`, `executable false`, `tool null`; runtime refusal demonstrated and retained for both packets | live PixelLab declaration and connection | Consistent. The refusal is the documented behaviour, not a packet defect. Verified by my own read of the runtime. |
| `sample-criteria.json` carries the exact five f_sample criteria, schema-valid, with verified line bounds | state records q_sample_* and q_style_match (rev 9, unchanged); `asset-plan.schema.json` | criteria unchanged; labels `proposal` x4 (wh actor), `requirement` x1 (wh user) | new file; no Q record changed | none | Consistent: byte-equal to the records (my comparison script); schema valid (my rerun); 18/18 bounds inside files and each cited text matches its claim. The single `authority` label per criterion is a kit schema limit; the mixed-authority split is in `basis`/`scope`, which I read. Adopted. |
| Brief component 3 (v1) labelled "controlled-evaluation sample confirmation" also carried "only dark value; no second outline tone, no selective outlining" | `controlled-evaluation-answers.md:5` (names only the treatment shown in reference.png); `reference-observations.md:40` (single flat colour, no ramp: observation); the rest is specialist wording | mixed authority under one label | **Finding 2 sent; corrected in v2**: 3a evaluation clause verbatim from `c_sample.li`; 3b observation citing lines 37-40; 3c specialist tightening labelled as such and added to `specialist_choices_in_this_brief`; "no drop shadow" attributed | none | Discrepancy found by me, corrected by the same child with an old-to-new table inside the v2 brief. No clause gained authority; `q_sample_outline` text unchanged. v1 retained as the pre-discovery identity (bound). Adopted. |
| Brief component 1 adds "no gradients, no dithering" under observed | `reference-observations.md:29` ("No anti-aliasing and no dithering in either file") | observation | v2 cites line 29 | none | Consistent; same authority class. |
| Reference roles: reference.png style (primary) + palette; reference-b.png style (secondary), conditionally included only if the live operation takes more than one style image with reference.png first | `pixellab-operations.md:33-47` (assign a role before selecting the operation); `brief.md:21-22` (both references are the style authority) | specialist choice, labelled | brief v1/v2 `references[]` | live schema (SQ2) | Consistent and explicit. A plausible alternative (always include both) would weaken the trial of the outlined treatment, which is the specialist's stated reason; reference-b.png remains the q_style_match comparison, so the owner's style authority is not dropped. Adopted as a scoped choice. |
| Hard constraints and their authority (canvas, alpha, single image, view, facing, sampling, palette, outline) | `controlled-evaluation-answers.md:6, 8`; `reference-observations.md:23, 24, 33-35, 37`; `brief.md:19, 23`; `method-research.md:41-55` | each labelled; nothing called confirmed | brief v1/v2 `hard_constraints` | none | Consistent. Sampling is correctly placed as a delivery rule, not a generation parameter. |
| Operation shortlist from `pixl_capabilities` decides nothing | `pixl_capabilities` (`live_discovery: false`, 2026-09-11); `pixellab-operations.md:15` ("discovery starting points, not a frozen callable catalog"); `readiness.md:101-102` | documentation | `operation-shortlist.json` with per-row discriminating questions | live declaration | Consistent; `no_tool_is_decided: true`; the only cached row with a required `style_images` field is noted as such without choosing it. |
| Local harness implements q_sample_canvas and q_sample_palette as worded; frame count kept outside both | Q texts (rev 9); harness lines 108-140 | tooling, not evidence | `work/sample-checks/*`; no X/E/V | none | Consistent: I read the evaluation code and reran it; it measures exactly width/height, fractional alpha and palette membership of alpha>0 pixels. Discriminating fixtures behave as expected. No verdict created. |
| v1 validation script overwrites the retained artifact when run as documented | `validate_criteria.py:9, 19, 60-62`; my own reproduction (hash 93643a34 -> 82d7df80) | reproducibility defect | **Finding 1 sent; corrected in v2**: `validate_criteria_v2.py` read-only, `--out` refuses to overwrite; v1 script and artifact retained unchanged; instruction recorded in the e note, the v2 packet and SESSION.md | none | Defect found by me (caused actual drift of a hash quoted in two bound files), reversed by me, fixed by the same child under a new name. Verified by my reruns. Adopted. |
| Revision 10/11 bind the packet files as S records; no I/C/F/Q/T/X/E/V/D change | `pixl_validate` record hashes; sorted diffs | structural | 5 + 4 new S/N records | none | Verified. The binding makes `validate` detect drift of the reviewed translation; v1 and v2 packets both stay bound, `s_sample_criteria` shared. |
| Decision table: every intake status unchanged; `job-prepare` needs capability inputs, not owner answers; `i_display_scale`/`i_backgrounds` gate visual review; production answers unchanged | `lifecycle.py:44-77` (sample gate accepts observed/proposed; unresolved/conflict block; production gates separate); `pixl_workflow` on rev 11 | runtime fact | none | live declaration, transport, authorization evidence | Verified by my own trace: t_sample -> f_sample.ct c_sample -> ch (none unresolved/conflict); production tasks keep prerequisite, contract and decision blockers. |
| Timestamps in retained JSON are UTC 2026-11-16 while `S.at` is 2026-11-15 | `state-authority.md:7-9` (observed provenance dates) | disclosure | disclosed in the d note | none | Observation, no action: the session date is 2026-11-15 and the files carry their actual UTC clock readings. |

## Correction round

Two findings, both source-grounded, sent to the same native child with evidence; one revision
received (revision 11). Finding 1 was a defect I detected by reproducing the specialist's own
instruction; finding 2 was a mixed-authority clause. Both corrections preserve the historical
artifacts (v1 brief, v1 packet, v1 script, 93643a34 artifact, d note) byte-for-byte and add
successors under new names with explicit old-to-new tables. No second revision was needed.

## Adoption finding

Revision 11 (720a1a1ecc59f210654485f4e279b1cb58dd881629ece37ef2db323c1ecec443), the
continuation notes d and e, the v2 request-review packet (`request-review-v2.json`
a596f02a..., `sample-creative-brief-v2.json` f84b2628..., unchanged `sample-criteria.json`
14c979ea...) and the local harness are consistent with the brief, the retained sources and the
installed runtime. No intake status moved; no acceptance, candidate, verdict, evidence, decision
or job was created; the controlled-evaluation answers remain sample-scoped. I adopt the revision
11 head, the v2 packet as the current pre-discovery translation of `c_sample`, and the next
operation as stated: `pixl_job_prepare` for `t_sample` / `f_sample`, blocked on the host's live
PixelLab tool declarations and connection, image transport for reference.png, and authorization
evidence, not on an owner answer. Consistency here is contract consistency; it is not provider
execution or asset acceptance.
