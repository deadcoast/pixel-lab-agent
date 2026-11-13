# Compact caller results and actionable recovery

Initial increment: **2026-11-10**; retained Claude continuation: **2026-11-13**,
active cycle `IDENTIFY-2026-11-09-01`,
**[M2 | QOL-10, SC-08 | PX-A2A-001, PX-EVAL-005]**. Local implementation and both
bounded caller outcomes are complete. Claude finishes through guided same-parent,
same-child continuation on the frozen November 10 kit. Its original rate-limit
failure, timeout and subsequent defects remain retained. Human acceptance stays
separate; M1/M2 and broader M3/M4 remain open. No new artwork, provider execution
or artistic acceptance is assigned here. The [original index](20261110/RESULT.json)
and [continuation index](20261113/OUTCOME.json) retain their distinct scopes.

## Implemented operation

The [caller-result contract](../../spec/caller-result.md) adds
`plar handoff --view caller` / `pixl_plar_handoff` with `view: "caller"` to the
existing immutable handoff operation. Default receipts and identical-input saved
bytes retain their existing meaning. The optional closed `details.caller` block
holds a bounded authored summary, file/report locators, issues and integration
findings. Existing detailed observations remain stored in full.

Assignment status and integration statements remain agent-authored. Production
facts and immediate continuation are derived from the captured selection. Declared
file hashes are checked before publication; a successful check does not certify
the assigned role, visual judgment or future file stability. The full handoff,
details and resume remain exactly retrievable. A resume larger than 4096 compact
UTF-8 JSON bytes is referenced as a whole rather than truncated. The returned
focused refresh read supports reconciliation before acting on an old snapshot.

[Shared diagnostics](../../pixl/diagnostics.py) retain the original error code and
detail, adding a category, safe identity context and an actionable recovery. Exact
recovery operations are existing reads when their arguments are known; otherwise
guidance stays in prose. Actual retained unknown-job context is required for an
uncertain-remote classification. Prepared or running work is not silently relabelled
unknown, and a dated catalog miss does not establish a missing live provider tool.
No recovery automatically retries a mutation or resubmits provider work. An export
failure after publication preserves the operation result and directs recovery to
the export rather than replaying the operation.

The canonical [delegation](../../plugins/pixl/skills/pixl/references/delegation.md),
[everyday](../../plugins/pixl/skills/pixl/references/everyday.md),
[runtime](../../plugins/pixl/skills/pixl/references/runtime.md) and
[identity/path](../../plugins/pixl/skills/pixl/references/identities-and-paths.md)
guides describe authored claims, derived facts and exact retrieval separately.
The shared profile is unchanged.

## Verification and package identity

The [prepared bundle receipt](20261110/preparation-01/bundle.json) verifies
183 listed entries (182 payload files plus requirements), manifest
`10895896cfc882c27e1fa99306426dc0def3cf59ce639e0ebbb9da8909cf9097`.
The complete [native kit archive and identity](20261110/native-kit-01/IDENTITY.json)
retain all 184 files including that manifest, independently of temporary consumers.
The full verifier regenerates four proof/example resources
(`evidence/art-methods/poc-report.json`, `examples/atelier/measurement.json`,
`examples/atelier/project.px` and `knowledge/library.px`), so its distribution
manifest changes. Native qualification does not claim whole-manifest identity
with the regenerated distribution. The [final parity check](20261110/bundle-parity-02/result.json)
finds 179/183 payload entries identical and exactly those four regenerated resources
changed; runtime, profile, skills, specifications and configuration match. The
final distribution manifest is
`b9959daa7a3b436c6ab2fc5db59936c0401d5eb6843707f26f0dfe5580a4ae11`.

The [first full verifier](../verification-runs/20261110T085441.240712Z/result.json)
retains 769 passes, one failure and one Windows privilege skip. Its sole failure
is an old MCP test expecting errors to omit `structuredContent`; SC-08 now
intentionally includes structured diagnostics. Runtime state and dispatch refusal
were unchanged. The assertion now checks the actual unknown job, read-only
recovery and absence of a dispatch request. The [final full verifier](../verification-runs/20261110T091628.456296Z/result.json)
passes **774 tests with one Windows symlink-privilege skip**, all 39 reference
checks, benchmark and fresh distribution checks. This is the complete suite
total, including existing tests. All 184 captured source inputs still match.
[Final Ruff](20261110/final-static-01/result.json) passes for 19 changed active
Python files; exact source-format restoration is covered by the final full run.

The [adapter verification](20261110/evaluator-adapter-01/result.json) passes 14
focused tests, Ruff and focused Mypy. These overlap the complete suite rather
than adding independent completion credit. The before-adapter sources and first
grades remain retained. The [grading index](20261110/native/GRADING-RECEIPT-02.json)
binds final grades, native records and exact evaluator snapshots. A later
[format identity check](20261110/format-verification-01/result.json) restores the
readiness grader/test files' original LF endings and reruns all four affected
native grades; their results exactly match the retained final grades.

## Native task outcomes

The assignment uses retained artistic-revision work: accepted `artistic-02.plan`,
its exact handoff and deliverables, and the unaccepted stale `artistic-01.plan`
diagnostic. Supporting controlled errors are identified as controlled; they do
not establish fresh provider execution. A size limit or specialist self-report
alone is not useful caller acceptance.

| Native case | Result | Independent evidence |
| --- | --- | --- |
| Codex, actual named `pixl` child | Completed compact result, full retrieval, current refresh, guarded handoff and five local error/recovery exercises | [28/28 pass](20261110/native/codex-01/independent-grade-03.json) |
| Claude, registered `pixl:pixl` children | Partial artifacts retained; no final caller result or complete retrieval/recovery evidence before timeout | [Required-evidence failure, 0/1](20261110/native/claude-01/independent-grade-01.json), [incomplete observation](20261110/native/claude-01/incomplete-observation-01.json) |
| Claude, first retained continuation | Same parent/latest child completes, but original caller-view authorship and exact error retention need correction | [23/31 original grade](20261113/native/claude-02/independent-grade-01.json), [29/31 after strict adapter fixes](20261113/claude-02-adapter-grade-02.json) |
| Claude, guided correction | Same child publishes caller view; parent retains exact error and consumes corrected reports | [31/31 final grade](20261113/claude-03-grade-03.json), [22/22 independent review](20261113/semantic-review-03.json) |

Codex's parent consumes exact details/resume ranges, refreshes selection and safely
repeats the unchanged handoff with returned guards. Assignment status stays partial
because the separate fictional `member.job` remains unknown; accepted artistic
production still reports delivered. All declared artifact/report hashes and prior
inputs are preserved. Integration statements cite retained renderer evidence;
there is no new provider execution, artistic acceptance or renderer review.

The [matched payload measurement](20261110/verification/payload-measurement-01.json)
uses the same immutable handoff and state: compact UTF-8 JSON is 7,963 bytes for
the caller view versus 17,937 bytes for the full handoff. The physical files are
9,664 and 22,165 bytes; the ordinary final caller report is 4,396 bytes. Full details
and continuation remain available. Older approximately 218 KB semantic audits
serve a different purpose and are not an equivalent size baseline.

The original Codex [19/28 grade](20261110/native/codex-01/independent-grade-01.json)
and [intermediate grade](20261110/native/codex-01/independent-grade-02.json) remain
preserved. Corrected adapters recognize the canonical child identity and failed
MCP items carrying structured errors. Codex's host log truncates the middle of the
focused PLAR response; refresh proof binds the completed call and its complete
`production.continuation`/`hash_domains` suffix. The full saved caller file is
separate evidence, not proof that the omitted native middle was observed. Final
grade 03 uses the final adapter source without changing the native attempt.

Claude's persisted parent is `0510b038-b18b-4fbc-aafe-c19b95d7dba6`. Its first
registered child, `ac98550e535c93d5a`, ended with HTTP 429 from the host account
rate limit. The parent started a **new** registered child, `ab352c80d7f534aae`,
without a resume argument; this is not same-child continuation. The 900-second
trial then timed out with exit 1. Compact output, full details and a specialist
report exist, but the receipt, specialist result, parent source reads/refresh and
final caller report do not. The 0/1 grade records missing required evidence, not a
failed artistic verdict. Original inputs and both production states remain
unchanged. At that original close, no continuation had been launched. The later
continuation below preserves those records. The separately passing [Claude readiness cases](../readiness/20261110/RESULT.json)
do not establish completion of this changed workflow.

## Retained Claude continuation — 2026-11-13

The [fresh preflight](20261113/preflight-01.json) verifies all 4,439 original
inputs, 16 partial artifacts, the frozen kit and exact persisted parent/child
journals. Both new processes use parent `0510b038-b18b-4fbc-aafe-c19b95d7dba6`
and latest child `ab352c80d7f534aae` through actual `SendMessage`, with native
completion events and additive journal prefixes. No replacement specialist is
credited. The kit remains manifest
`10895896cfc882c27e1fa99306426dc0def3cf59ce639e0ebbb9da8909cf9097`;
this does not qualify the newer production package.

The first continuation preserves all 4,456 preceding files and adds 29 outputs.
Its 23/31 grade has six adapter gaps and two real defects. The adapters now bind
the frozen host's queued completion notification, exact explicit child identity,
complete JSON lines in actual command output, labelled recovery wrappers and
native host-spilled result bodies. [Retained host results](20261113/native-tool-results-02/manifest.json)
come from actual native tool-result locators, not caller-authored copies. Those
fixes yield 29/31 while correctly retaining both real failures: the earlier child
had published the original caller view, and a manually copied diagnostic altered
literal backslashes in its original error detail. The [first semantic review](20261113/semantic-review-01.json)
and [attribution supplement](20261113/semantic-attribution-01.json) preserve them.

The guided correction supplies one explicitly identified
[read-only error-capture helper](20261113/correction-inputs-03/IDENTITY.json).
The same latest child makes its own public caller-view operation with identical
details and guards; the parent retains the exact native error without string
normalization. Fresh reports acknowledge original publication by the earlier
child. The [final caller report](20261113/native/claude-03/outputs/revision-03/CALLER-RESULT.json)
is **8,006 UTF-8 bytes**, names the same immutable handoff and delivered art,
leaves the fictional `member.job` unknown, and keeps assignment status partial
separate from delivered artistic production. All 4,486 pre-correction files remain
unchanged; 36 new files stay within `revision-03`.

Four oversized caller drafts (10,104, 9,628, 9,088 and 8,812 bytes), failed
comparisons, shell failures and the failed sibling redirection remain retained.
That redirection created no file. The [initial correction grade, 30/31](20261113/claude-03-grade-01.json)
also remains: its chronology adapter incorrectly let a later identical read-only
probe erase an earlier valid sequence. The final proof identifies one actual
ordered sequence of completed errors, stale recovery and guarded handoff; it
does not pretend the later probe preceded the earlier handoff. Final sources and
their exact snapshots are [retained separately](20261113/grading-sources-06/IDENTITY.json).

The [independent review](20261113/semantic-review-03.json) verifies complete
parent-visible specialist, caller and corrected-error reports. Fresh compact JSON
was parsed and compared with the original; complete model-visible review of every
saved JSON body is not claimed. The compressed caller history groups HTTP 429
and timeout in one phrase: the authoritative sequence remains first-child HTTP
429, then parent timeout while the latest child was unfinished. A report's
`fork: none` label is not proof of a separate Claude fork setting.

Reusable [case preparation and grading](../../evaluations/NATIVE-CONTINUATION.md)
now retain original and pre-resume baselines, reject changed partial outputs or
native history, verify transitive preservation and actual same-child completion,
and allow fresh correction report paths. The [focused final verification](20261113/verification-06/result.json)
passes **127 tests** covering evaluator, recorder, caller-contract and adjacent
native-proof regressions, with Ruff and whitespace checks. The [final Codex regression](20261113/codex-regression-03.json)
remains **28/28**; its [intermediate 26/28](20261113/codex-regression-02.json)
is retained with the narrow PowerShell-argument-vector adapter fix. The production
runtime, profile, skills and package are unchanged; the older full-suite result
above is not a new test run for this increment.

## Review questions A–E

**A — Improvement:** derive the ordinary result through the existing handoff so
callers receive useful artifacts, scoped findings and exact continuation without
manually rebuilding runtime identities. Both bounded caller outcomes support this
operation; Claude's result includes explicit guided corrections. Full detail remains available.

**B — Host compatibility:** CLI/MCP share the operation and structured diagnostics.
Codex's explicit named route completes the assigned caller work. Claude now
finishes the retained caller work through the same parent and latest child, on the
frozen kit. Earlier failures and guided recovery constrain that claim; broad host
reliability and current-kit qualification remain open.

**C — Contextual quality:** the concise view preserves unresolved requirements,
source authority and the difference between assignment status and acceptance.
No aesthetic verdict follows from serialization, file hashes or a successful export.

**D — Another repository:** the assignment and returned paths remain rooted in the
actual consumer. Fresh focused reads and exact retained-byte retrieval establish
which selection each caller consumed. Claude's exact correction reports and native
operations establish its completed result; partial artifacts alone did not.

**E — Responsibility:** the specialist authors scope, integration judgments and
issues; the local runtime derives saved-state facts and safe recovery context;
the host performs observations and separately authorized provider work. Neither
a recovery hint nor a cached catalog grants a new provider submission.

## Continuation

Follow [TODO](../../TODO.md), [PLAN](../../PLAN.md) and the
[ordered backlog](../../SHELVED.md). **SC-06 — saved adapter/schema compatibility**
is the next eligible increment; M5 enabling work can proceed alongside the open
earlier milestones. Human acceptance stays separate; M1/M2 and broader M3/M4
remain open. Continue the active IDENTIFY cycle without a new audit.
