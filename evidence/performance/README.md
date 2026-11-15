# TM-02 — retained-history performance measurements

Measured 2026-11-14 (America/Vancouver), continuing `58af5359b0b29ae050a7b3938e7d8f66e5020d60`
within **IDENTIFY-2026-11-09-01**. **Human acceptance stays separate and unrecorded;
M1/M2 and broader M3/M4/M5 remain open.**

## Outcome and usability repairs

<a id="tm02-measurements"></a>The final local measurement passes all four retained histories and 39 operations, with 15 timed samples per operation, two warmups and three fresh-process authoring probes per history. All 5,207 frozen input files remain unchanged; all 36 previously successful operation results retain their exact hashes. Three previously crashing authoring reads now complete after a narrow whole-file source-binding repair. No performance optimization or cache was introduced.

The [measurement report](20261114/measurement-02/report.json) retains raw
nanoseconds, distributions, result sizes/hashes, dependency/platform versions,
source identities and complete input inventories. The [197/197 comparison](20261114/qualification-02.json)
checks successful output equality, fixed crashes, sampling and preservation.
The [earlier successful measurement](20261114/measurement-01/report.json) and [158/158 qualification](20261114/qualification-01.json) retain their pre-lock-correction source scope. All 39 successful outputs from that run match the final run. Its timings differ under uncontrolled machine load; this is not speedup evidence, and the corrected lock-observation helper is not called by these measured read paths.

The [wrapper receipt](20261114/measurement-02/RESULT.json) binds the exact archived
inputs and measured sources; its [source ZIP](20261114/measurement-02/sources.zip)
retains the implementation actually executed, including the replay driver.

Actual retained PNG sources legitimately have `ln=[]`. Authoring context formerly
indexed that empty list to construct a text-only `pixl_source` call, raising
`IndexError` on three histories. The repair exposes the exact complete `binding`
for these sources, preserving URI/digest/authority and current/changed/missing
observations. Ranged retrieval remains unchanged. No saved record, registry,
acceptance rule or source endpoint changes. This is a correctness repair found
by measurement, not a speedup. See the [authoring contract](../../spec/production-plan.md).

Full verification then exposed a separate Windows lock-read race. A contending
diagnostic reader's ordinary CRT handle denied deletion, so the actual writer
could publish successfully and then receive `WinError 32` during normal lock
release. [The deterministic original reproduction](20261114/lock-race-01/RESULT.json)
retains the failure and old source. The Windows metadata opener now shares read,
write and delete access, with `OPEN_EXISTING`, no-follow intent and a
noninheritable, read-only descriptor. It never requests delete-on-close; successful
descriptor conversion transfers ownership, and failed conversion closes the
native handle. Existing bounded reads, identity checks, exclusive acquisition and
release logic remain unchanged, with no automatic retry or unlocking.

This follows the [Windows sharing contract](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
and [Python descriptor conversion](https://docs.python.org/3/library/msvcrt.html#msvcrt.open_osfhandle).
The [35 focused lock tests](20261114/lock-race-03/RESULT.json) run with 33 passes
and two existing Windows privilege skips; scoped Ruff and the boundary gate pass
(five checks and 13 expected static refusals). Four new regressions exercise
held-reader release across threads and processes, descriptor properties and
conversion-failure cleanup. [Independent Windows review](20261114/lock-review-01/RESULT.json)
passes 17/17 checks, including actual handle closure and unchanged writer/guard
logic; its initial weak closure-test assertion is retained as corrected. The
portable branch retains its old flags, without a new POSIX runtime claim.

## Workloads and reproduction

These are real retained production histories, not synthetic scaling or new native
trials. Their original artistic/host results retain their original scope.

| Frozen case | Original outcome | Revision / records | State bytes | Retained state snapshots | Frozen files |
| --- | --- | ---: | ---: | ---: | ---: |
| queue-native | [CF-10 Codex Ready](../native-production/README.md) | 10 / 93 | 75,707 | 11 | 251 |
| robot-directions | [CF-10 guided Claude family](../native-production/README.md) | 43 / 354 | 391,967 | 44 | 328 |
| robot-idle | [CF-09 actual revision](../domain-art-revision/README.md) | 50 / 370 | 436,877 | 51 | 740 |
| queue-revision | [CF-03 retained successor](../artistic-revision/README.md) | 108 / 679 | 806,401 | 109 | 3,888 |

The [preparation receipt](20261114/input-preparation-01/RESULT.json) and four
[input archives/manifests](20261114/inputs) record each member's original archive
or exact historical-hash supplement. Native deltas omit unchanged consumer
sources; the older queue also needs its retained base archive. Supplements were
accepted only when their historical hashes matched, without rebinding state.
Installed kits/configuration/caches are explicitly excluded where present.
All original source/archive bytes and mtimes remain unchanged. The completed
input copies retain all 11/44/51/109 state snapshots respectively; the largest
delta alone contained only 20 snapshots and is not described as complete.

Run from the repository root using a **new** output directory:

```powershell
.venv/Scripts/python.exe -B evidence/performance/20261114/run-measurements.py.txt --out evidence/performance/20261114/measurement-NEW --profile
```

The [driver](20261114/run-measurements.py.txt) verifies ZIP/member identities,
extracts temporary consumer roots, writes a fresh manifest/source archive and
captures stdout, stderr and exit code. It removes its temporary roots after the
run. Reuse the driver, not a manifest pointing at a deleted temporary directory.
It measures the current checkout; earlier `sources.zip` files retain earlier
versions. The [maintainer guide](../../docs/PERFORMANCE.md) documents the reusable
stdout-only [harness](../../scripts/measure_performance.py), direct manifests,
flags, side effects and interpretation. No provider, host model or network
operation is part of measurement.

## Observed costs

Windows 11 AMD64, CPython 3.14.3, 16 logical CPUs, jsonschema 4.26.0 and Pillow
12.3.0. These measurements have warmed filesystem/runtime caches, no CPU affinity
or controlled machine load, and no cross-machine or latency-target claim.
The full verifier ran **after** measurement. Components overlap with public
operations and must not be summed to represent a caller workflow.
The selected task/output contexts omit the optional PLAR attachment. Concurrent
writers, optional attachment cost, provider latency and model latency were not
benchmarked.

Public operation wall time below is **median / nearest-rank p95, milliseconds**.
JSON serialization is timed separately in the raw report. With 15 samples this
p95 is the sample maximum, not an established production tail-latency estimate.

| Case | Authoring context | Complete context | Public validation report | Family report |
| --- | ---: | ---: | ---: | ---: |
| queue-native | 84.5 / 93.9 | 114.8 / 121.1 | 111.2 / 126.5 | Not applicable: single output |
| robot-directions | 104.7 / 121.1 | 375.9 / 400.3 | 325.1 / 337.7 | 445.4 / 470.5 |
| robot-idle | 135.8 / 146.5 | 379.4 / 405.0 | 329.0 / 351.4 | 418.1 / 428.4 |
| queue-revision | 289.9 / 397.8 | 673.3 / 763.2 | 818.5 / 909.6 | 757.2 / 902.2 |

Component medians, milliseconds:

| Case | Parse bytes | Store load | Canonical encode + hash | Raw state-file hash | Structural validation | File-backed validation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| queue-native | 4.628 | 4.436 | 2.550 | 0.400 | 10.022 | 90.037 |
| robot-directions | 21.521 | 19.995 | 8.134 | 0.550 | 51.335 | 271.124 |
| robot-idle | 18.333 | 20.044 | 9.588 | 0.492 | 60.600 | 259.796 |
| queue-revision | 35.493 | 30.242 | 18.028 | 0.665 | 92.758 | 684.036 |

Report sizes are actual pretty JSON UTF-8 bytes plus newline; complete wire is
also listed because the service wraps wire in JSON while the CLI emits raw wire.
Authoring is an orientation index with different semantics from complete context.
These are not equal-information compression ratios or token/model-quality scores.

| Case | Authoring JSON | Complete-context JSON | Raw complete wire | Family JSON | Fresh-process authoring median, ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| queue-native | 34,728 | 75,995 | 75,707 | N/A | 297.0 |
| robot-directions | 58,558 | 369,469 | 368,975 | 100,304 | 307.7 |
| robot-idle | 77,604 | 414,654 | 414,147 | 143,579 | 323.4 |
| queue-revision | 139,182 | 663,022 | 662,364 | 243,550 | 421.5 |

Fresh probes include process startup, imports, manifest reading, the actual
authoring operation and full-result serialization, but transport only compact
measurement JSON. They measure neither complete CLI output transport nor cold
disk access. Result identity agrees with the in-process operation in every case.
Large reports retain the existing file-output route; no information is dropped
to obtain these sizes.

## Optimization decision

**No performance optimization selected.** The bounded core authoring route now
works on all four histories. These runs establish costs, without an observed
caller stall or agreed latency requirement that justifies a cache or rewrite.
The largest full validation deliberately verifies retained history; raw SHA-256
alone is a small part of the measured operation.

Separate [authoring](20261114/measurement-02/authoring-profile.txt) and
[validation](20261114/measurement-02/validation-profile.txt) profiles on the
largest history identify structural validation/canonical record encoding and
historical journal/schema checks as candidates for a future targeted experiment.
Their instrumented durations are not baseline timings. The [profile receipt](20261114/measurement-02/profiles.json)
also confirms unchanged inputs. Any future optimization must repeat these
identities and successful/refused outcomes, retain changed-file and historical
receipt visibility, and demonstrate benefit to the caller. A faster failed
baseline cannot be compared with a repaired successful read as a speedup.

## Verification and preserved failures

- [First full verifier](../verification-runs/20261115T020512.610236Z/result.json)
  retains 1,429 passes, one error and four Windows privilege skips (1,434 run),
  plus 39 passing references. It stops before distribution at the reproduced
  diagnostic-reader sharing conflict. This is not dismissed as a flaky pass.
  [Lock-race-02](20261114/lock-race-02/RESULT.json) retains the intermediate lint
  finding; [lock-race-03](20261114/lock-race-03/RESULT.json) records its correction.
- [Prepared-input smoke](20261114/input-preparation-01/prepared-smoke.json)
  passes structural/file/complete-context checks on all four copies and retains
  the three authoring tracebacks. The earlier [archive-only smoke](20261114/input-preparation-01/archive-smoke.json)
  preserves the incomplete-delta missing-artifact result; the first
  [discovery](20261114/discovery-01) preserves a report-serialization failure.
- [Baseline-01](20261114/baseline-01/report.json) retains one warmup, three samples
  and one fresh probe per case, the three `IndexError` failures and an inapplicable
  single-output family-report refusal. Its source archive remains intact. The
  final driver selects only actual family outputs; that refusal is not relabeled
  as a runtime defect or erased.
- [Repair-02](20261114/repair-02/RESULT.json) passes 46 focused tests, including
  four new regressions, with no skips and scoped Ruff. They cover binary-source
  identity, changed/missing refusals, remote/ranged behavior, CLI/MCP parity and
  input preservation. [Repair-01](20261114/repair-01/CORRECTION.md) retains the
  initial 45/46 result caused by an incorrect test closure expectation.
- [Harness-04](20261114/harness-04/RESULT.json) passes 13 focused tests and scoped
  Ruff, including unexpected failures, expected-refusal mismatch, changed inputs,
  timing boundaries and exact child diagnostic retention. Earlier
  [harness-01](20261114/harness-01/RESULT.json) and
  [harness-03](20261114/harness-03/RESULT.json) lint failures remain.
- [Independent review-01](20261114/review-01/RESULT.json) retains 8/10 checks:
  malformed-child and timeout diagnostics were lost despite correctly failing.
  The correction retains exact captured stdout/stderr as labeled base64;
  [review-02](20261114/review-02/RESULT.json) passes the same ten checks, including
  exact invalid-UTF-8 timeout bytes.
- [Independent actual-report replay](20261114/review-03/RESULT.json) passes 36/36
  checks. Four freshly retrieved public authoring reports match the measured
  hashes and sizes. This replay precedes the lock correction; the final 197-check
  comparison confirms identical output bytes afterward. It checks 12 local whole-file and 103 ranged source bindings
  against actual saved fields and local bytes, preserving all 5,207 input files
  and their directory inventories. This review covers selected returned rows
  with current direct bindings; changed/missing cases are separately covered by
  the focused regressions. It does not independently certify its author's input
  preparation or establish native/visual outcomes.

## Final local and package verification

<a id="tm02-full-verification"></a>The final TM-02 verifier passes 1,434 tests with four existing Windows privilege skips (1,438 run), 39 reference checks and distribution checks. The 21 new unittest methods comprise four authoring regressions, 13 measurement-harness tests and four lock-reader regressions. This establishes local and package behavior against the recorded source identities, not native model behavior, provider performance, art quality or human acceptance.

The [final receipt](../verification-runs/20261115T023402.446790Z/result.json)
records tested source hashes, bundle identity and fresh installed/copied-package
checks. Its `previous.zip` preserves intermediate generated outputs, including
the failed first run's top-level results and log. The first attempt's archive
preserves the original generated bytes; the [257-file prior kit](20261114/prior-kit-01/manifest.json)
separately retains every tracked kit file at the starting commit. Neither the
failed full result nor the older native/artistic receipts are rewritten.

The [read-only registry inspection](20261114/integrity-01/RESULT.json) passes
12/12 checks across 23 claims and 68 receipts: two current TM-02 claims, eleven
historical and ten stale applicability claims. Earlier outcomes remain intact;
the expected `needs_review` exit reflects retained source/release gaps, not a
failed current measurement. The [final documentation audit](20261114/documentation-02.json)
checks links, all 50 finding IDs, open milestones, pinned claims, archived prior
outputs and final tested identities. The [worktree check](20261114/final-worktree-check-01.json)
records maintained-file whitespace and credential-shape scanning, including
nested new archives, within its stated scope.

<a id="ae-review"></a>
## A–E review and continuation

**A — Improvement:** measure actual read paths before optimizing; recover authoring context for valid whole-file sources and prevent a diagnostic reader from blocking its actual writer's normal release.
**B — Hosts:** shared service/CLI/MCP regression checks exercise the repair, but
no new Claude/Codex production behavior or general reliability follows.
**C — Quality:** exact bindings and full validation remain visible; byte count
and latency do not judge art or model reasoning.
**D — Other projects:** repeatable manifest-driven measurement works on isolated
retained consumers; current four-case coverage is not arbitrary-project support.
**E — Responsibility:** the maintainer harness measures local runtime costs;
profile/skills supply judgment and workflow, the provider supplies art operations,
and caller/human acceptance remain separate.

TM-02 is bounded complete as measurement and the discovered correctness repair;
optimization remains conditional. Next: **PX-SKILL-001 consequential-choice and
cold-handoff qualification [M1, linked CF-02 / PX-EVAL-005]**, the earliest
unfinished required behavior in the existing [TODO](../../TODO.md) and
[detailed specification](../../evaluations/TODO.spec.md). Preserve completed
literal-criteria comparisons and the separate CF-08 profile-loading failure.
Keep all 50 finding IDs and the active PLAN; no new IDENTIFY or milestone closure.
