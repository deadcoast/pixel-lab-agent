# Exact connected-plan criteria handoff

Observed 2026-11-09. This increment repairs the missing connection between the
family/stage authoring interface and independent caller comparison. The original
[native authoring partial result](../native-authoring/README.md) remains historical
evidence; its graph, request and comparison are not rewritten.

## Implementation and deterministic verification

`pixl_production_plan` and `pixl_stage_prepare` return ready `request_review`
arguments. The existing `pixl_request_review` tool reads the bound plan and optional
job, including every member and collective criterion, exact source excerpts, current
controls and requirements, and retained request/blockers. It leaves authority for
the caller to classify. No new MCP tool or PX2 field was introduced.

The caller saves a comparison for each exact criterion identity: source obligation,
authority/basis, scope, literal additions/omissions, a discriminating alternative
and disposition. An optional coverage check detects missing, duplicate, changed or
incomplete entries. Its scope fingerprint survives relocation but changes with
review-relevant evidence. Structural coverage never grants semantic consistency,
adoption, execution or acceptance. Corrections remain separate from saved history.

See the [workflow](../../plugins/pixl/skills/pixl/references/request-review.md#connected-family-and-stage-handoff)
and [operation specification](../../spec/production-plan.md#exact-criteria-handoff).

The [final full verifier](../verification-runs/20261109T100432.749313Z/result.json) reports
**557 passes and one Windows symlink-privilege skip**, 39 reference checks and clean
wheel/copied-plugin probes. Ten new regressions cover complete member/collective
handoff, the prepared request and idempotent return, incomplete/stale comparisons,
changed criteria/source bytes, relocation, CLI/service parity and legacy-option
handling, plus actual local dispatch/submission progress without invalidating an
unchanged comparison. Current lifecycle state remains visible; its observations
do not change the semantic fingerprint. The installed probes exercise the exact
handoff as well as preparation.
Ruff passes; Mypy reports no issues across 67 maintained files under its configured
scope, which does not fully check untyped function bodies.

[Final parity](independent-review/final-parity.json) verifies all 139 recorded
code/spec inputs and 164 bundle entries without drift, including source-to-bundle
identity. All 222 local links checked across the nine affected documents resolve.

## Native comparison

The fresh [Claude attempt](20261109/native/claude-01/identity.json) is a targeted
repair of the retained partial comparison in a copied consumer, with the current
kit and ordinary local MCP. The assignment identifies the existing plan/job and
requires a complete comparison; it does not supply the desired interpretations of
individual clauses. It is not an unprompted replay of initial authoring, a new
provider request or another rendering acceptance.

The [independent review](independent-review/review.json) passes this targeted
comparison after native caller corrections. Claude Code 2.1.318 completed in
2625.738 seconds, returned [CRITERIA-RESULT.json](20261109/native/claude-01/project/CRITERIA-RESULT.json),
and passes [19 independent checks](independent-review/claude-checks.json). All 881
pre-run consumer files and the frozen kit remain unchanged; all 439 file/hash/line
pointers in the final proposal resolve. The archive contains 1,950 files, each
re-read against its [manifest](20261109/archives/claude-01-manifest.json).

The parent compared all **20 exact criteria**: 17 member checks and three
collective checks. It retained three unchanged, requested 14 clarifications and
three transparency/review-route corrections. It also caught four discrepancies in
the specialist's first proposal and obtained a separate revision:

- A component touching all four edges became a visual-review diagnostic, not a
  mechanical rejection of intentional foreground.
- Even motion pacing was attributed to expert judgment, separate from the required
  four-frame, 100 ms activity loop.
- Visual-weight wording retained coherence without inventing an equal/comparable
  stroke or footprint obligation.
- Distinction from Start was attributed to its shared consumer role as an explicit
  inference, not falsely quoted as the brief's wording.

The [caller comparison](20261109/native/claude-01/project/work/criteria-review-01/caller-comparison.json)
retains `changes_requested` for the historical contract. The
[corrected proposal](20261109/native/claude-01/project/work/criteria-review-01/specialist-proposal-r2.json)
is for future adoption; it is not a directly executable replacement PX2 plan.
The original graph/request is unchanged and Working remains prepared/blocked by
the changed requirements. No new provider, visual or renderer acceptance follows.

Two foreground registered PIXL calls were observed. `SendMessage` between them
failed with **No transcript found**; the parent used an explicit artifact-based
restart. This demonstrates saved-artifact recovery, not same-child reliability.
The `--no-session-persistence` evaluation setting remains a qualification question,
not a proven platform defect. Codex was not rerun for this repair.

## Current-kit continuity and diagnostic correction

The final runtime additionally excludes lifecycle observations from its fingerprint.
The native semantic-review run retains its original frozen runtime and fingerprint.
A [focused caller continuation](20261109/native/claude-export-01/identity.json) uses
the final kit, copies the current raw report as exact bytes, checks all actual
differences and retains the completed comparison without re-authoring its rows.
It returned [EXPORT-RESULT.json](20261109/native/claude-export-01/project/EXPORT-RESULT.json)
after 594.724 seconds and passes [16 independent checks](independent-review/export-checks.json).
All 20 comparison rows, discrepancy resolutions and historical files are unchanged;
fresh raw/formatted JSON values match exactly, and current-fingerprint coverage is
complete. The only report differences are the intended fingerprint change and
relocated absolute source paths. Its 1,990-file archive was re-read against its
[manifest](20261109/archives/claude-export-01-manifest.json). This is caller continuity
after completed semantic review, not a second independent artistic judgment.

An initial maintainer diagnostic used the Windows default decoder on UTF-8 JSON
and incorrectly reported a changed provider-description string. Explicit UTF-8
decoding proves the original raw and formatted native reports are identical. The
[correction](independent-review/encoding-correction.json) preserves the erroneous
diagnostics and explains that the follow-up prompt was launched with that mistaken
premise. The native follow-up independently verified the intact bytes. The shared
workflow now explicitly requires byte copying, UTF-8 parsing and parsed-value
equality for formatted reports; no native file was rewritten to hide the mistake.

## Required A–E review

**A — Improvement.** The caller receives exact authored clauses and their evidence
through the existing review operation instead of reconstructing them from grouped
summaries. Coverage makes omitted collective rules visible. The next usability
improvement is focused authoring context and compact shared source references
without broad history/runtime exploration. The native review worked but produced
large proposals and read substantial context; this does not establish an efficient
ordinary authoring workflow.

**B — Platform compatibility.** The trial uses the installed Claude native agent
route and a copied plugin through local MCP. Tool schemas expose optional arguments
without changing prior packet semantics. This qualifies a recorded installed route,
not future host behavior. Codex named-role selection remains open; Claude
same-child continuation failed again in this harness and requires separate work.

**C — Contextual/artistic quality.** Sources, expert choices and criteria stay
distinct. A model still must understand pixel art, retain qualitative outcomes and
judge alternatives; a complete table cannot prove good judgment or good art.
Preserving scoped construction choices avoids replacing expertise with blanket
permission or rejection rules.

**D — Another repository.** All pointers are consumer-relative and the review
identity survives consumer relocation. Existing source-retention resolution and
current-selection checks remain authoritative. Changed requirements are visible
beside the historical prepared request, preventing a corrected explanation from
silently reviving obsolete intent.

**E — Workflow location.** The profile owns specialist judgment; shared PIXL skill
references specify specialist-to-caller review and correction. The authoring adapter
and existing local review MCP/CLI provide evidence and structural checks. Official
PixelLab tools remain the production execution route. The native trial and byte
checker are development evidence, not production requirements.

## Continuation and limits

The useful successor in the existing consumer remains the scoped reduced-motion mapping, resolution of
obsolete prepared intent, and a reviewed family/request continuation through the
necessary production, review and rendering. Broader generated quality, host
reliability and the overall specialist ecosystem remain open.

The returned continuation uses “re-bind” informally. No in-place mutation of an
immutable job was implemented or verified. Successor work must use the actual
provider-recovery lifecycle, retain the old intent and separately bind revised
plans/requests; the root TODO makes that distinction explicit.
