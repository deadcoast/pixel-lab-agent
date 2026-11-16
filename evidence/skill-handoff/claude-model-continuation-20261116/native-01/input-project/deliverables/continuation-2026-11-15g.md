# Continuation note, 2026-11-15 (g): corrections after the caller review of revision 12

Same session, same consumer root (`.../pixl caller review a97de5914a21428aad2fef3c65ecfcec/consumer`),
same kit, interpreter and isolation as `deliverables/continuation-2026-11-15f.md` (the f note,
sha256 `9e0df8a1d8d4bbfa6591d16fffe07406f53c639d32b797e320232b15177a135f`, bound as
`s_continuation_7`, retained unchanged). The caller reviewed revision 12 independently, verified
it consistent on every claim it checked (state identity, wire diff, protected files, verifier,
kit-reference and runtime line citations, evaluation-answer and brief citations), and returned
two findings plus an extension of the first. All are correct. This note records the
old-to-new correction for each and otherwise directs readers to the f note, which remains the
current full continuation (decision table, operation-effect check, kit identity, later needs).
This is still a **handoff-only increment**: no request packet, fixture, harness, generation,
provider, candidate, verdict, evidence, intake-status or task-state work; `c_sample`, the five
sample criteria, every I/T record and every retained file keep their bytes.

## State identity on entry / exit

| | Value |
|---|---|
| Entry | PX2 revision 12, 82 records, canonical hash `f6b2c25456d1abbc49bf4e6f6d1305749bf2e0b105738428f066f14b3070e632` (= head sha256 = history copy = `work/rev12.px`), ready `[t_sample]`, no jobs, head record `handoff_8` |
| Exit | revision 13, 84 records (82 + `s_continuation_8` + `handoff_9`), committed to the store folder `state.px` with expected hash `f6b2c254...e632`; ready `[t_sample]`, blockers unchanged, no jobs. The revision 13 hash is not written here (this note's digest is bound inside it); read it from `state.px/state.px`, `SESSION.md` or the caller return |

## Finding 1: wrong line locator for the side-view destination ("brief.md line 19")

**Fact.** `sources/brief.md` (sha256 `a78aca77135c5e533b8000272558b5b65e40ee421d1913cab961d7adc4cf5324`)
line 19 reads `- Family roster: a scout and a medic.`; line 20 reads `- Destination: a side-view
game.`; the verbatim brief also states "for a side-view game" at line 5.

**Old -> new.** Every locator that cites **line 19** for the side-view destination must read
**line 20** (optionally also line 5). Line 19 is the correct locator for the **roster**
(`i_roster`).

**Where the defect is (all retained unchanged; byte identity preserved):**

| File (sha256) | Line | Old text | New text |
|---|---|---|---|
| `deliverables/continuation-2026-11-15f.md` (`9e0df8a1...a135f`, `s_continuation_7`) | 137 (View row) | "Owner; confirmed `side` (`s_brief` line 19)" | "(`s_brief` line 20; verbatim line 5)" |
| same | 147 (Roster row) | no locator | "(`s_brief` line 19)" |
| `deliverables/sample-request/sample-criteria.json` (`14c979ea...1834b`, `s_sample_criteria`) | 74 (`q_sample_readability` sources) | `"locator": "line 19: destination is a side-view game", "lines": [19, 19]` | `"line 20: destination is a side-view game", "lines": [20, 20]` |
| `deliverables/sample-request/sample-creative-brief.json` (`cc21bf77...380ce`, `s_sample_brief`, v1) | 81 (`hard_constraints` view) | "owner, confirmed (i_view; sources/brief.md line 19)" | "... line 20" |
| `deliverables/sample-request/sample-creative-brief-v2.json` (`f84b2628...a5b80`, `s_sample_brief_v2`) | 110 (`hard_constraints` view) | same | same correction |
| `deliverables/sample-request/request-review.json` (`ffa933ed...1e78b`, `s_sample_request_review`, v1) | 9 (sources locators) | "line 19: side-view game" | "line 20: side-view game" |
| `deliverables/sample-request/request-review-v2.json` (`a596f02a...84d73`, `s_sample_request_review_v2`) | 19 (sources locators) | same | same correction |
| `review/caller-comparison-2026-11-15-v4.md` (`0c2f864e...7a58`, caller's file, not mine) | 53, 85 | states brief.md line 19 was opened and cites `brief.md:19` for the view constraint | the check looked at the roster line; the view authority is line 20 |

**Origin and why it was missed.** The locator was first written into the v1 packet (revision 10),
copied unchanged into the v2 packet (revision 11) and into the f note's decision table (this
session, inherited from `request-review-v2.json` line 19 rather than re-read from the brief).
`validate_criteria.py` / `validate_criteria_v2.py` check only that each `lines` range lies
inside the cited file (`all_line_bounds_inside_files true`, 18/18), not what the line says, so
`schema_valid true` could not catch a wrong-but-in-range pointer. The previous caller's
comparison recorded the range as opened but did not catch the mismatch either.

**What is not wrong.** The saved Q record `q_sample_readability` (`so [s_methods, s_refobs,
s_continuation_2]`, check text without a line number) and `i_view` (`so [s_brief]`, `wy` "The
brief states the destination is a side-view game", no line) carry no line locator, and
`s_brief` binds the whole file (`ln [1, 33]`). **No state record is wrong**; the authority of
`i_view` (owner, confirmed) is unchanged and still correct. The defect is a source-pointer error
in derived artifacts and in one note.

**Disposition (requested by the caller; adopted).** No v3 brief/criteria/packet is produced now,
because this increment is handoff-only and the packet becomes a successor anyway when the
provider arguments exist. The bound artifacts keep their bytes as the pre-discovery identities.
The correction is an **explicit required step of the next operation**:

> When the `provider_arguments` successor packet is built (the step before `job-prepare` for
> `t_sample` / `f_sample`), `sample-criteria.json` must be superseded by a **v2 criteria file**
> whose `q_sample_readability` source for `sources/brief.md` reads line 20 (`"lines": [20, 20]`,
> optionally also `[5, 5]`), with the brief and packet locators corrected the same way; it must
> be re-validated with `deliverables/sample-request/validate_criteria_v2.py --criteria <v2 file>
> --out <fresh path under work/>` (never `validate_criteria.py`), and bound as a **new S record
> beside the unchanged `s_sample_criteria`**. The five check texts themselves do not change.

Until then, readers of the v1/v2 packet should read "line 19" in those files as line 20.

## Finding 2: provenance misattribution in `SESSION.md`

**Old** (`SESSION.md` as written in the f increment, sha256 `f291ac6c9a90ce6eec6e130131c4df7a49c2bbf421f5f9e9ccab9ba54762f1f2`,
lines 5 and 7): the previous session at root `e3c7ebe1...` was credited with "revision 11 ...
note 2026-11-15e" only, and an "earlier session (2026-11-14 / 2026-11-15 a-d)" with "revisions 6
through 10 ... notes 2026-11-14 through 2026-11-15d". That wording was inherited from the
previous `SESSION.md` and is wrong about where revision 10 and the d note belong, and it
collapses three distinct earlier roots into one.

**Evidence (retained caller results and notes, all unchanged):**

| Root (consumer) | Caller result (lines) | Entry -> exit revisions | Notes |
|---|---|---|---|
| `e3c7ebe124824b69828309bf1645f322` | `CALLER-RESULT-PREREQUISITES.json` 6-7, 24-25 | 9 -> 10 -> 11 (`fdf4ebfe...` -> `23f4ee55...` -> `720a1a1e...`) | d, e (e note line 3: "Same session, same isolation and same paths as ... 15d.md"; d note lines 9-10 name this root) |
| `d31ffb17787d4358adda6c5e32024830` | `CALLER-RESULT-ANSWER-STATE.json` 6-7, 24 | 8 -> 9 (`ac9150f4...` -> `fdf4ebfe...`) | c (`continuation-2026-11-15c.md`) |
| `ca2b0073ba6c4da79a6c306380a10742` | `CALLER-RESULT.json` 6-7, 23-24 | 6 -> 7 -> 8 | 2026-11-15, 2026-11-15b |
| not recorded in a retained caller result | `continuation-2026-11-14.md` line 4 ("Resumed from ... revision 5") | 5 -> 6 | 2026-11-14 |
| predecessor, 2026-09-14 | `sources/brief.md` lines 11-15 (session constraints) | revisions 1-5 | kit at `.agents/skills/pixl-kit`, other interpreter |
| `a97de5914a21428aad2fef3c65ecfcec` (current) | this session | 11 -> 12 -> 13 | f, g |

**New** (`SESSION.md` rewritten in this correction round; hash in the caller return): the
provenance lines attribute revisions 10-11 and notes d-e to the `e3c7ebe1` session; revision 9
and note c to `d31ffb17`; revisions 7-8 and notes 2026-11-15 / 15b to `ca2b0073`; revision 6 and
the 2026-11-14 note to a 2026-11-14 session whose root is not recorded; revisions 1-5 to the
2026-09-14 predecessor. The current pointer names revision 13, the g note and the f note.

## Files added or edited in this correction round (consumer-relative, sha256)

| Path | sha256 | Role |
|---|---|---|
| `work/rev13-protected-snapshot.sha256` | `89652f5bedef53bd74cb1d601d55fb7e506bdb3caa9dfd10a9c86fe792f7ce32` | sha256 of all 388 files present before any write in this round; read by the verifier |
| `work/build_rev13.py` | `8df2ecee342011aeb98e443aa9f97457e743cdd03c221f3fc700312c8d4f9c7d` | revision 13 builder (decode head, append 2 records, encode) |
| `work/verify_rev13.py` | `270d6c4416c4792a1c2ebfdc33601d09ec98a83cc19203434ee0b35ccfbbd78b` | revision 13 verifier, read-only; checks the 82 revision 12 records against `work/rev12.json`, the g note binding, `handoff_9`, protected files via the snapshot, and that the v2 validator leaves the retained artifact unchanged |
| `work/rev13.json`, `work/rev13.px` | produced by the builder; `rev13.px` bytes equal the committed head | candidate document and wire |
| `deliverables/continuation-2026-11-15g.md` | bound by `s_continuation_8` | this note |
| `SESSION.md` | edited (finding 2); hash in the caller return | current-session pointer |

Nothing else was written; `validate_criteria.py` was not run.

## Records added in revision 13 (12 -> 13 delta)

| Record | Kind | Content |
|---|---|---|
| `s_continuation_8` | S (new) | `ur deliverables/continuation-2026-11-15g.md`, `dg` = this note's sha256, `ln [1, N]` with its actual line count, `at 2026-11-15`, `au local` |
| `handoff_9` | N (new) | `wh actor`; `rv 13`; `nx [t_sample]`; `bl [t_scout, t_medic, t_family]`; `fo` = `s_continuation_8` followed by `handoff_8`'s complete list (`s_continuation_7`, `s_continuation_6`, `s_sample_brief_v2`, `s_sample_request_review_v2`, `s_sample_criteria`, `s_sample_brief`, `s_sample_request_review`, `s_eval_answers`, `c_sample`, `f_sample`, the 12 non-confirmed I records in state order, `x_aid`, `x_study`) |

Header `PX2 12 -> PX2 13`. Nothing else: all 82 revision 12 records byte-identical (verified
against `work/rev12.json`). The finding-1 correction reaches the state only through this note's
binding; no Q, I, C or S record is edited or superseded, because none of them carries the wrong
locator.

## Effect on the current handoff

The f note's decision table, operation-effect check, kit-identity section and later-production
list stand unchanged except for the two locators above. The next operation is still `job-prepare`
for `t_sample` / `f_sample` against `c_sample`, blocked only on capability inputs (live PixelLab
declaration and schema, image transport handle for `reference.png`, discovery and authorization
evidence), with the criteria-v2 supersession above added as a required step of building the
`provider_arguments` successor packet. No owner answer is needed for the sample.
