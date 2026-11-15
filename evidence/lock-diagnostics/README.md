# SC-09 — lock diagnostics and recovery guidance

Reviewed 2026-11-14 within **IDENTIFY-2026-11-09-01**. This increment makes
interrupted or competing local writes understandable without weakening exclusive
publication. **Human acceptance stays separate and unrecorded; M1/M2 and broader
M3/M4/M5 remain open.**

## Useful operation

A refused CLI or MCP operation keeps `store_locked` and now returns the lock path,
metadata status and recorded owner PID, host and UTC acquisition time when those
fields are readable. Owner liveness remains `unverified`. The caller receives
`unfinished_work` with `inspect_lock_owner`, without an executable retry or unlock
operation. Existing PID-only records remain readable; malformed, incomplete,
unavailable, changing, oversized and non-regular records remain distinct.

The shipped [recovery guide](../../plugins/pixl/skills/pixl/references/store-locking.md)
starts with the actual lock location. It covers store, PLAR and handoff locks,
quiescent writers, preservation of the leftover record, and rereading published
state before reconciling unfinished intent. A recorded PID or old timestamp is
not abandonment evidence. No process probe, automatic retry, age-based reclaim,
provider submission or saved-format migration was added.

## Fresh local verification

<a id="sc09-process-recovery"></a>SC-09's controlled source-runtime and copied-kit process proofs retain their exact local writer-lock diagnostic and recovery outcomes; input identities determine applicability, without native model, provider, artistic or human acceptance.

- [Source process proof](20261114/process-02/RESULT.json): **50/50** checks pass
  across graceful release, interruption before publication and interruption after
  the new head is published. Controlled workers terminate themselves through the
  Windows OS on their evaluator-owned input channel, bypassing normal cleanup;
  launcher and actual writer identities are retained separately. The evaluator
  never terminates a PID obtained from lock metadata.
- The live owner blocks a public CLI commit. Repeated calls and an artificially
  old lock timestamp still refuse publication. After verified writer exit,
  explicit recovery preserves exact lock bytes and validates the current state.
  The already-published case rejects the old expected hash and publishes the
  remaining reconciled change exactly once.
- [Final copied-kit process proof](20261114/process-03/RESULT.json): **50/50**
  checks pass using the same frozen evaluator and a copy of the final complete
  kit. Loaded module paths resolve inside that copied runtime, and public calls
  use its official `scripts/pixl.py`. Its recorded manifest matches the full
  verifier's final bundle. This is a scripted local consumer, not a model trial.
- [New lock tests and scoped Ruff](20261114/implementation-04/RESULT.json):
  **20 passed, one Windows symlink privilege skip** (21 run). Public CLI/MCP
  diagnostics, legacy records, unavailable metadata and exclusive acquisition
  are covered. [Independent review](20261114/review-01.json) passes eight checks;
  its separate test rerun has the same 20-pass/one-skip outcome.
- [Combined regression](20261114/regression-01/RESULT.json): **92 passed, two
  Windows privilege skips** (94 run), including existing store, jobs, completion,
  publication recovery, confinement and diagnostics tests. These overlap the
  focused tests and are not additional production outcomes.
- [Default mypy](20261114/typing-01/RESULT.json) passes 44 runtime modules, with
  the configured unchecked-untyped-body limit. The prior [broad Ruff failure](../deliverable-index/20261114/maintenance-01/RESULT.json)
  remains retained; this increment's scoped pass does not resolve it.

<a id="sc09-full-verification"></a>SC-09 [full verification](../verification-runs/20261114T235749.451894Z/result.json) passes 1,413 tests with four Windows privilege skips (1,417 run), 39 reference checks and distribution checks; this is local implementation/package evidence, not native behavior or artistic acceptance.

The total includes the existing suite and 21 new lock tests. The test log records
545.890 seconds. A retained [diagnostic stack sample](20261114/full-launch-01/stack-01.txt)
shows an existing retention fixture writing a local file during this longer run;
it does not establish the cause of the elapsed-time difference or a performance
qualification. No maintained source changed while verification ran.

## Preserved failures and corrections

The [baseline](20261114/baseline-01/RESULT.json) reproduces the old public gap:
contention excludes the write but provides neither structured owner metadata nor
lock-specific recovery. Its claim that killing the virtual-environment launcher
proved the writer was hard-terminated was too strong. The later process work
identified the Windows launcher/interpreter PID distinction; the baseline remains
unchanged, with an [additive correction](20261114/process-02/BASELINE-QUALIFICATION-CORRECTION.json). The corrected source proof above
supplies the interrupted-writer evidence.

[Implementation attempt 01](20261114/implementation-01/RESULT.json) fails with
16 assertion failures, two errors and one skip across 19 tests. Windows `lstat`
and `fstat` give different meanings to `ctime`, so the first observation code
misclassified unchanged files as changing. The implementation now compares shared
identity fields across those APIs and change times only within the same API.
The direct observation and all subsequent source snapshots remain retained.
Attempt 02 predates the final strict-JSON refinement. [Attempt 03](20261114/implementation-03/RESULT.json)
passes tests but retains four Ruff style findings; attempt 04 fixes those findings.

[Process attempt 01](20261114/process-01/RESULT.json) remains **40/50, failed**.
Its ten failures expose the evaluator's assumption that `Popen.pid` names the
actual Python writer on Windows. Wrapper-only termination did not establish that
writer exit. The corrected helper binds the worker's actual PID and parent to the
owned launcher and records its controlled self-termination and observed exit;
the [evaluator correction](20261114/process-02/EVALUATOR-CORRECTION.json) retains the distinction.
Neither a later missing PID nor a reused PID retroactively proves the old process
state. The subsequent result is a fresh attempt, not a regrade of the failure.

The [previous complete kit](20261114/baseline-01/previous-kit.zip) preserves all
254 original kit files. Full verification separately archives outputs it may
regenerate before running its builders and tests. Prior receipts and registered
claim lines remain unchanged; new results receive their own source bindings.

The [read-only integrity inspection](20261114/integrity-02/RESULT.json) records
the final registry applicability and preserves the selected input trees during
inspection. The [documentation audit](20261114/documentation-01.json) checks
links, the original 50 finding IDs, open milestones, pinned claim lines and exact
archival of replaced generated bytes. These audits do not replay prior native or
artistic results.

The first integrity inspection remains retained against an intermediate Markdown
newline change. A whitespace preflight omitted the repository's `cr-at-eol`
setting; the matrix's original CRLF convention was restored without changing
line content, and the final inspection uses a fresh output directory.

## Limits and next work

These are controlled local Windows process and package checks. They do not
qualify native profile instruction following, all filesystem races, hostile
filesystem replacement, every crash point or other operating systems. Normal
lock cleanup retains its existing path-based behavior; the guide's quiescence
requirement matters. No new provider execution, art, renderer or human acceptance
is claimed.

The next eligible slice is **TM-01 — incremental boundary typing**. TM-02 remains
conditional on measurement. Development continues within the same plan while
the broader milestone exits remain open.

## A–E review

- **A — Improve the core operation:** a blocked caller can locate the actual
  lock, distinguish readable identity from unavailable observation and recover
  unfinished local intent without blindly repeating publication.
- **B — Host compatibility:** CLI and MCP share the same bounded diagnostic
  contract, using the existing caller issue category. Local process and copied-kit
  checks do not substitute for Codex or Claude behavioral qualification.
- **C — Context and artistic quality:** reconciliation preserves published
  production state and uncertain provider jobs. It grants no artistic verdict or
  new acceptance to retained art.
- **D — Another repository:** the guide ships in the complete kit, and the copied
  runtime proof uses isolated consumer fixtures and the official kit launcher.
  Consumers do not need repository builders to inspect a contention result.
- **E — Responsibilities:** runtime enforces exclusive acquisition and reports
  observations; the skill guides investigation and explicit recovery; the caller
  establishes quiescence and reconciles current intent. Official provider work
  remains a separate production operation.
