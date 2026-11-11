# TM-07 reusable isolated consumer execution

Development increment: **2026-11-11**, active cycle `IDENTIFY-2026-11-09-01`,
**[M3 | TM-07 | PX-PLAR-002, PX-PROD-001]**. Status: **bounded slice complete**:
public operation, both native outcomes, final full verification and separate
final-kit compatibility pass. M1/M2 and broader M3, allocation coverage, generated
quality, host reliability and the unrelated Claude caller-result continuation
remain open. **Next: NF-08 visible asset lineage, then CF-10.**

## Implemented operation and acceptance

The public `consumer-execute` / `pixl_consumer_execute` operation runs the shipped
`queue-motion-v1` profile against a current retained family candidate. See the
[contract](../../spec/consumer-execution.md) and
[caller procedure](../../plugins/pixl/skills/pixl/references/consumer-execution.md).
The operation copies six fixed resources into a fresh project-relative attempt:
`capture.mjs`, `server.mjs`, `view.mjs`, `index.html`, `check.py` and
`observation.py`. Its closed configuration names the consumer modules, exact
output-to-destination mapping, scales, observed wrap target and bounded timing.
There is no caller-supplied launch script or arbitrary runner.

Preflight checks current candidate/manifest bindings, exact delivered asset bytes
and the confined consumer source tree. Execution records Node capability checks,
fixed argument-array commands, subprocess receipts, stdout/stderr, raw capture,
PNGs, checked observations and cleanup. A passing capture/check/bridge reuses the
existing [NF-06 destination import](../../spec/destination-observation.md), retaining
the report and declared input/output closure. It returns an observation for a
separate candidate review; it does not write production state, nominate a
candidate, record a verdict or complete the task.

The operation uses a dedicated browser profile, loopback server and owned
processes. Desktop control is not required; interactive inspection remains
available when it adds evidence. This is process/profile isolation, not an OS
security sandbox. Missing prerequisites and failed, timed-out, interrupted or
partial attempts retain available evidence and require a fresh output path for
retry. The native outcomes below demonstrate scoped discovery and use of the
shipped route in both hosts.

The queue adapter reads the consumer's geometry, timing, descriptors and motion
contract. Its event/state interface and frame sequence are explicit profile
requirements, not universal pixel-art rules or arbitrary framework support. A
passing process, pixel check or import does not provide an artistic verdict.
Real playback, static views, controlled timeline samples and unavailable
observations remain distinct, including their actual scale and frame coverage.
No new provider generation is assigned by this increment.

## Promotion provenance

The [retained promotion record](20261111/renderer-01/provenance.json) identifies
`renderer-artistic/capture.mjs`, `view.mjs`, `check.py` and
`src/queue-view-artistic.ts` in the earlier
[CF-03 consumer archive](../artistic-revision/20261109/native/codex-01/consumer-delta.zip)
(SHA-256 `bdcc8feea6861bdf1c5b7f2c9b5567de4deb689dcd4aa9f890acba6d9159b6ad`).
It also hashes the retained successor consumer state module and five copied art
files. The richer motion contract is reused with a fresh configurable bounded
launcher and observer; the historical inputs and earlier local proof are not
rewritten. The fresh proof snapshots the current six-file renderer closure.

The [successor acceptance](../successor-acceptance/README.md) retains its own
maintainer headless execution, observed wrap counting, reduced-motion/live switch
evidence, failed initial recorder and interactive observations. The completed
[CF-07/NF-06 slice](../integration-change/README.md) retains its exact source/art
reuse, source-change guards, fresh review, both-host outcomes and final-kit
compatibility checks. Its Codex 50/50, continued Claude 51/51 and 848-pass/one-skip
full verifier retain their own source revisions and scopes. Its unperformed 1×
live playback and continuous video remain unperformed in those historical proofs;
TM-07's new 1× live evidence does not change them.

## Observed local results

| Proof | Observed result | Scope |
| --- | --- | --- |
| [Fresh renderer](20261111/renderer-01/check.json) | Pass: 136 PNG pixel, 15 source and 120 clock checks | Real headless consumer capture over the retained richer motion contract; no native model invocation |
| [Copied-kit public pipeline](20261111/pipeline-01/outputs/execution-result.json) | Complete: capture, check, bridge and NF-06 import; 172 PNG pixel, 15 source and 156 clock checks | Public CLI in a fresh external copied-kit consumer; no model launched |
| [Pipeline preservation](20261111/pipeline-01/preservation.json) | No changed or removed pre-existing files; production unchanged | New execution/import evidence retained without altering source, art, production records or earlier history |
| [Corrected copied-kit pipeline](20261111/pipeline-02/outputs/execution-result.json) | Complete: capture/check/bridge/NF-06 import; 168 PNG pixel, 15 source and 152 clock checks; cleanup confirmed | Fresh public invocation after the requested-input guard; initial requested hash references retained; no model launched |
| [Corrected pipeline preservation](20261111/pipeline-02/preservation.json) | No changed or removed pre-existing files; production unchanged | Exact existing consumer, art, production records and history preserved |

Each real capture observes `statusCell` and `compactStatus` at 1× and 3×. In
both normal-start and normal-restored phases, every consumer/scale observes all
four frames, eight transitions, two actual wraps and zero skips. The reduced and
initially-reduced phases hold frame 0 with no transitions. Live preference changes
and reconciliation are observed when entering reduced motion and restoring
normal playback. These are bounded facts about this supplied queue contract.
Sample counts and reduced-phase duration differ between the runs; the check
totals are separate, not an additive acceptance score.

The [renderer execution receipt](20261111/renderer-01/capture/execution.json)
and copied-kit result confirm browser/server closure and temporary-profile
removal. The copied-kit [public command](20261111/pipeline-01/public-command.json)
returns zero and [exports a complete result](20261111/pipeline-01/public-stdout.json)
with `renderer_executed` and `files_verified` true, and `state_changed`,
`state_written` and `automatic_acceptance` false. Its
[retained import result](20261111/pipeline-01/outputs/execution-01/import/result.json)
is a separate NF-06 consistency/retention result, not an independent claim that
NF-06 executed the consumer. The accompanying prepared `launch.json` is not proof
of a model run.

The idle SVG is decoded by the browser; the independent pixel comparator supports
PNG only. Continuous video, subjective artistic review, target-engine acceptance,
arbitrary consumer compatibility and broad host reliability are not established.

## Verification history and retained findings

Independent review identified a missing mutation guard for generated
`config.json`, `review-context.json` and `destinations.json`. The correction now
freezes their requested serialized bytes and retains initial hash references in
`requested_inputs`. It checks those controls before/after phases, import and final
return. The result also makes `timeout_scope: subprocesses` explicit. All 26
runtime tests and five surface tests pass, including five runtime cases added
after the pre-correction verifier. The `renderer-01` and `pipeline-01` proofs
predate this correction and retain their actual source snapshots. A fresh corrected-kit public replay
now passes in `pipeline-02`, retaining the exact requested control hashes,
unchanged inputs and confirmed cleanup. An older receipt does not test new source.

The [pre-correction full verifier](../verification-runs/20261111T224500.371261Z/result.json)
passes 905 tests plus one Windows symlink-privilege skip (906 run), 39 reference
checks and distribution checks. This receipt belongs to the revision before the
generated-input guard correction and remains retained. The
[guarded-runtime verifier](../verification-runs/20261111T225401.174513Z/result.json) passes
**913 tests plus one Windows symlink-privilege skip** (914 run), 39 reference
checks and fresh wheel/copied-plugin checks. This is 65 new tests relative to the
849-test CF-07 baseline, not 914 newly added tests. Installed consumer-execution
capability checks establish packaging and public surface availability; the real
headless pipeline is the separate evidence above.

That verified bundle manifest has 196 files and SHA-256
`e63db5543b20964090ad027d38d4f9c7ea8931d89fef80e48c6e26429b29c6b5`.
The [first grader-freeze verifier](../verification-runs/20261111T231133.390690Z/result.json)
passes 917 tests plus one Windows privilege skip (918 run), 39 reference checks
and distribution checks. It predates the preservation-contradiction hardening
below. The [post-hardening verifier](../verification-runs/20261111T231849.735943Z/result.json)
then passes 919 tests plus one Windows privilege skip (920 run), 39 reference
checks and distribution checks. That receipt predates the lint-only grader cleanup.
The final frozen-code result and separate compatibility replays are recorded
below. Keep discovery/format checks, synthetic orchestration/failure checks, real
browser execution, native model behavior and artistic/consumer acceptance
separate.

The [kit snapshot manifest](20261111/kit-snapshots/manifest.json) retains complete
[pre-request-guard](20261111/kit-snapshots/pre-request-guard.zip) and
[native guarded](20261111/kit-snapshots/native-guarded.zip) installed kits, 198
files each, bound to their original preparation identities. Archive hashes and
every member hash match the manifest; historical receipts were not rewritten.
These full snapshots preserve the actual executed kit bytes independently of
later generated bundle rebuilds. Their archive file counts are distinct from
entries counted by the bundle manifest.

## Final verification and compatibility

The [final frozen-code verifier](../verification-runs/20261111T232640.239355Z/result.json)
passes **919 tests plus one Windows symlink-privilege skip** (920 run), 39 reference
checks and fresh wheel/copied-plugin checks. The increment adds **71 tests** to
the 849-test CF-07 baseline; full-suite, focused, native and nested renderer totals
are separate evidence tiers. Earlier verifier receipts remain attached to their
actual source revisions. The checked source identities remain unchanged after
this final verification.

The final bundle manifest has **196 files**, SHA-256
`7f17cb4bbe15372050055d19f266176a97650d877c10a9dd28940d8b4311d48b`.
[Codex-consumer compatibility](20261111/codex-01-final-kit/receipt.json) and
[Claude-consumer compatibility](20261111/claude-01-final-kit/receipt.json) each
pass **13/13** separate local checks against that final copied kit.

Each replay first names a deliberately missing Node executable. The operation
retains an `unavailable` attempt and starts no renderer. A fresh output directory
then completes real capture/check/bridge/import, preserves the unavailable receipt,
verifies exact served/imported bytes, confirms owned cleanup and leaves all
original consumer inputs and production state unchanged. No acceptance is created.
This demonstrates a real unavailable-capability recovery route in both actual
consumers; it does not imply that every possible interruption or partial-capture
failure occurred in a native model trial.

The final kit's runtime, shared skills, renderer and specification are identical
to the frozen native kit. The four changed generated reference resources are
`poc-report.json`, the atelier `measurement.json` / `project.px`, and
`knowledge/library.px`; exact paths appear in both receipts. The old installed
kits remain archived. These replays prove final-kit public execution compatibility,
not another native model run, new image-viewing outcome or artistic acceptance.

## Native outcomes and retained failures

| Native trial | Independent result | Retained operation |
| --- | --- | --- |
| [Codex](20261111/codex-01/grade-05.json) | 28/28; natural process exit 0 | [168 PNG / 15 source / 152 clock checks](20261111/codex-01/outputs/execution-result.json); complete capture/check/import and renderer cleanup |
| [Claude](20261111/claude-01/grade-04.json) | 28/28; natural process exit 0 | [168 PNG / 15 source / 152 clock checks](20261111/claude-01/outputs/execution-result.json); complete capture/check/import and renderer cleanup |

Both actual named children load the common profile, skill and consumer-execution
reference, invoke the shipped `pixl_consumer_execute` public operation, inspect
retained images and produce an execution-only result. Their callers consume the
exact operation report and independently inspect images. The grader verifies
current candidate/binding identities, requested modules/scales/bounds, exact
source/destination/import bytes and unchanged production/history. It reruns the
frozen checker and reconciles compact counts to the retained samples. Both
consumers at 1×/3× show four distinct frames, two observed wraps and zero skips in
normal and restored phases, and same-page reduced-motion preference changes.
No recorded remote-provider tool attempt or new acceptance is reported.

Image-tool evidence establishes actual child and caller viewing of retained still
PNGs at both scales and the required phase screenshots. Motion/hold/wrap values
are sampled browser measurements from the operation; neither caller claims to
have watched live playback. Phase screenshot coverage uses frozen-renderer and
checked-canvas inventories, not an element-rectangle measurement. Normal-phase
screenshots may be byte-identical to each other, as may reduced-phase screenshots.
This does not establish subjective smoothness, every display refresh, continuous
video, new artistic review or target-engine acceptance. NF-06's nested import
still reports `renderer_executed: false` because import executes nothing; the
outer operation reports the actual headless capture.

The [first Codex grade](20261111/codex-01/grade-01.json) remains 21/28, with all 16
artifact/execution checks passing. Its seven grading failures arose from two
valid report shapes: `task_name` instead of `canonical_path` for the exact native
child caused five dependent failures, and structured `production_unchanged`
fields instead of one Boolean affected two report checks. Codex's intermediate
[grade-02](20261111/codex-01/grade-02.json) remains retained as well. The
[first Claude grade](20261111/claude-01/grade-01.json) remains 0/1 after a report
reference layout caused `KeyError: 'path'`. These are report-layout compatibility
defects in the grader, not failed consumer execution or artistic verdicts.

Narrow normalization of the exact observed report layouts first passed
[13 focused grader tests](20261111/grader-tests-03.json). Independent review then
identified a bypass: a positive unchanged alias could return before contradictory
recognized preservation fields were checked. The grader now validates every
supplied recognized flag, hash result and counter before accepting any positive
alias. [15 independent focused tests](20261111/grader-tests-04.json), including
22 mixed-contradiction cases, pass after this hardening.

The [hardening grader](20261111/grader-source-04.py.txt) and its original passing
grades remain retained. A later lint-only import-order cleanup and hash-verified
execution annotation change no grading semantics, runtime or native inputs.
[19 focused tests and evaluation-file Ruff checks](20261111/grader-tests-05.json)
pass: four fixture tests plus the same 15 independent grader tests.

The latest passing grades use the same [frozen grader](20261111/grader-source-05.py.txt),
SHA-256 `dd024848345d4eddcfebad4fa5dc4b0fce8f3f7d5fb0bf83917e8fd9e78e1944`,
with separate [Codex provenance](20261111/codex-01/grade-05-provenance.json) and
[Claude provenance](20261111/claude-01/grade-04-provenance.json). Earlier passing
and failed grades, their source snapshots and test receipts remain retained.
The native evidence was unchanged; no native rerun or continuation was needed
to obtain these fresh grades.

Claude's native record also retains recovered command errors: a broad Bash
cleanup was denied, then transient bytecode from CLI help was removed using
explicit paths; a report-write quoting error was corrected. Final preservation
checks pass. The child's native hash baseline excluded top-level assignment
files, while the caller separately compared the applicable restoration manifest
and the independent grader checks the exact initial input closure. These distinct
proofs must not be collapsed into a claim that every native hash list covered
every file. The errors and recoveries do not establish general host reliability.

## Required A–E review — current understanding

**A — Improve the operation.** The public fixed-profile operation consolidates
capture, checks, bridging and retention into one reusable invocation. It preserves
raw/partial evidence and uses a fresh attempt for retry. The generated-input guard
finding led to frozen requested controls and before/after identity checks, with
targeted regression coverage. Grader hardening also rejects mixed contradictory
preservation claims. Corrected public execution, both native outcomes, final full
verification and retained unavailable/fresh-retry compatibility checks pass.

**B — Host compatibility.** The copied-kit CLI completed without maintainer-only
launch code or desktop control. Public CLI/MCP discovery and the caller procedure
are implemented. Fresh Codex/Claude outcomes pass 28/28 each, with observed named
instruction loading, public invocation, exact caller consumption and image-tool
viewing. Both processes complete naturally. Final full verification and separate
13/13 final-kit replays per consumer pass; earlier grading failures remain retained.

**C — Context and quality.** Current bindings and exact delivered bytes anchor
capture. The new local observations cover both consumers at 1×/3×, actual frames
and wraps, reduced motion and live switching. SVG comparator limits remain
explicit. Both native callers and children inspect retained stills, while motion
counts remain sampled operation facts. These mechanics support separate specialist
judgment and do not confer artistic acceptance or alter earlier evidence scopes.

**D — Consumer operation.** A fresh external copied-kit consumer completed the
public capture/check/bridge/import path with unchanged production/art/history and
confirmed cleanup. Capability probing, bounded outcomes and
the corrected generated-control guard are implemented; targeted guard/surface
checks pass. Corrected public execution and both native outcomes preserve exact
source/art/history and demonstrate cleanup. Recovered Claude command errors and
grader-layout corrections remain in the ledger. Final verification and actual
unavailable-capability/fresh-retry replays pass; profile/platform scope stays
bounded to the tested queue consumer and environment.

**E — Responsibility location.** The profile owns judgment; the shared skill
explains procedure and limits; the local fixed execution route supplies
invocation, observations and retention. NF-06 validates and snapshots the supplied
report. Explicit candidate/family review retains acceptance; official PixelLab
remains the provider for separately authorized art production. No UDL migration
or new provider art is implied by this execution operation.

## Next steps

The bounded TM-07 slice is complete. Continue with **NF-08 visible asset lineage**:
show generated seed, provider edit, deterministic transform and reuse alongside
each delivered member, using existing job/artifact identities. Verify Working
construction, generated Retry/Paused and Ready's prior provenance in the retained
queue family without adding a new ledger. **CF-10 useful native production follows.**

[TODO](../../TODO.md), [PLAN](../../PLAN.md), [SHELVED](../../SHELVED.md) and the
active [findings](../../docs/IDENTIFIED.md) retain this order and the exact evidence
limits. M1/M2 and broader M3, quality, host reliability and the unrelated incomplete
Claude caller-result continuation remain open. Continue the existing audit cycle.
