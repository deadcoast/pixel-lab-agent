# TM-08 domain consumers supporting CF-09

**Bounded complete, 2026-11-12.** The [outcome ledger](OUTCOME.json) binds the final receipts. This increment adds reusable
`sprite-animation-v1` and `tile-neighborhood-v1` execution profiles. They expose
actual destination pixels, authored placement and timing, and corner-to-tile
mapping through the existing public `consumer-execute` / `pixl_consumer_execute`
operation. The existing queue profile and CF-10 robot renderer retain their own
contracts and evidence. CF-09 actual-art revision, human acceptance, M1/M2 and
broader M3/M4 remain open.

## Useful operation

The [profile selector](../../examples/consumer-execution/README.md) links each
closed contract. The [diagnostic project](../../examples/domain-consumer-project/README.md)
supplies runnable source/assets and project-specific intent. The shared workflow
selects a profile from actual consumer requirements and returns exact config,
source/destination/renderer snapshots, browser observations, independent checks,
NF-06 closure and cleanup. It creates no production records or acceptance.

- **Animation:** uneven per-frame duration, atlas crops, per-frame pivots and
  viewport anchor, looping and clamped one-shot playback, actual RAF frame/wrap
  samples and separately controlled stills. Interactive controls select clip,
  play/pause, frame, scale and anchor overlay. Correct painting does not judge
  contact continuity, readability or useful motion.
- **Terrain:** all sixteen explicitly declared binary corner IDs, actual
  `tileFor` calls for every neighborhood cell, independent mapping/compositing
  and screenshot checks at native/integer scale. NW/NE/SE/SW weights are this
  profile's explicit convention, not a universal terrain rule. Correct delivery
  does not judge material joins or artistic seams.
- **Preservation:** source closure and exact family members stay bound to the
  observation. Failures retain their evidence; retries need fresh directories.
  Owned browser/server/profile cleanup is recorded. Process isolation is not an
  operating-system security sandbox.

## Controlled qualification

The [preparation harness](../../evaluations/domain_consumer_case.py) copies an
authored project into fresh external consumers. PNG geometry and alpha are actually
measured; only those local member criteria are accepted. Both family snapshots
remain unreviewed, with no visual/destination verdict or human acceptance.

The native cases contain two deliberate pixel faults while preserving correct
module declarations: tile 6's northwest quadrant uses the wrong material, and
animation frame 2 is shifted down two source pixels. These are evaluator-authored
diagnostics, not provider failures. The mechanical operation should pass while the
specialist/caller inspect actual context and report the visual requirements still
unmet. Neither the defect nor its expected answer is placed in the assignment.
Original clean bytes and changed hashes are recorded in preparation identities.

The [frozen native kit](20261112/native-kit.json) retains every file and its exact
archive. Both trials use the existing local-only readiness launcher; there is no
paid provider call or production revision in this increment. Both callers finish naturally with unchanged source, pixels, kit and production
records. Final independent grades pass **49/49 each**:
[Codex](20261112/codex-01/grade-04.json) and
[Claude](20261112/claude-01/grade-02.json), with exact grader sources beside them.
The checks establish named-role loading, actual public execution, complete result
consumption, native image viewing, exact artifact/source closure and preservation.
They independently compare captures with the frozen authored source exports and
check cleanup subflags and required served files. This also covers the three
checker gaps discovered after the native kit was frozen, described below.

Both specialists and callers identify tile 6's wrong northwest material and the
third pose's two-pixel downward shift, separating those visible defects from
correct rendering. The [development-assistant still review](20261112/maintainer-observation-01.json)
corroborates the visible symptoms; the [report/byte comparison](20261112/maintainer-observation-02.json)
records identical selected Claude stills and the remaining wording limit. No pixels are revised and no artistic verdict
is recorded. Claude's proposed terrain correction includes an imprecise bounding-box
phrase; the required 64-pixel northwest correction and preservation scope are
clear, but this is not a blanket correctness or art-quality judgment.

Codex initially starts an inherited child, interrupts it before execution and
creates the required fresh named child; that history stays in its caller result
and journals. Claude recovers a caller shell-quoting error inside the assigned
work directory. Neither run requires a maintainer continuation or provider call.
Claude's original [0/1 grade](20261112/claude-01/grade-01.json) is retained: the grader
recognized flat references and Codex's `result` wrapper, but not Claude's lossless
`result_file` wrapper. The corrected adapter verifies the same exact path/hash
and rejects contradictory aliases. No native rerun or result rewriting was used.
All earlier Codex grades and their exact sources remain retained.

Exact initial consumer inputs are durable in the [Codex](20261112/codex-01/consumer-inputs.json)
and [Claude](20261112/claude-01/consumer-inputs.json) archive receipts: 340 and 337
files, including original production stores, brief, modules, pixels, configuration
and installed kit. The [retention script](20261112/retain-inputs.py.txt) checks the
native record's identity hash, then every current input against its preparation
hash before archiving and independently verifying the ZIP. This is post-run exact
byte retention, not reconstruction of missing state. When repeating this evaluation,
run that script for the completed attempt before disposing of its temporary consumer.

## Verification

Focused tests exercise real Chromium captures, incorrect mappings/timelines,
wrong pivot painting, missing assets/patterns, exact pixels/screenshots, changed
source/renderer/config, output collisions, unavailable browser and cleanup.
Public CLI tests cover both profiles through current-family validation and NF-06
import. Preparation checks keep mechanical acceptance separate from open art.
[Final scoped static checks](20261112/static-checks-02.json) pass. The first full
[verification attempt](../verification-runs/20261112T180945.296510Z/result.json)
runs 1,210 tests with 1,209 passes and the existing Windows privilege skip, then
correctly fails its source-stability guard because grader/tests changed during
that run. It is not a full verification pass. The final frozen-source
[verification](../verification-runs/20261112T181813.323111Z/result.json) passes
**1,212 tests plus one existing Windows privilege skip** (1,213 run; **74 new**
relative to CF-08), 39 reference checks and fresh distribution probes.

The separate [final-kit compatibility run](20261112/final-kit-compatibility-01/result.json)
passes **all four public operations**: both profiles in each actual native consumer.
Every run completes NF-06 import, exact-source checks, separate launch-contract
comparison and all cleanup flags. Per host, terrain retains four views; animation
retains sixteen controlled views and four actual playbacks with 26 transition
samples, two loop wraps and zero skips. All 554 Codex and 552 Claude preexisting
files, their directories, native receipts and original installed kits remain
unchanged. These are local replays, not new model, visual or artistic reviews.

The final 244-file kit manifest is
`853084baa638e47e77a281742dafeaa4e4807ba6268128bcf1103fe5541f3691`;
its complete archive, manifest and [native-to-final differences](20261112/final-kit-compatibility-01/kit-differences.json)
are retained beside the replay. Runtime/profile/skill sources match the native
kit. Executable renderer differences are the three corrected capture/check files;
two README fixes, four regenerated reference artifacts and the manifest account
for the remaining changes. The [compatibility guard probe](20261112/compatibility-probe-01/result.json)
separately checks recorded-receipt drift refusal and bounded mocked timeout cleanup.
The [final documentation audit](20261112/documentation-audit-03.json) checks links,
original finding IDs and historical-receipt preservation.

Cross-review found and fixed these bounded proof gaps:

- Animation checker: require each browser/server/profile cleanup flag and both
  served display resources, rather than trusting the aggregate cleanup flag or
  an incomplete served-file list.
- Tile checker: retain the initially imported terrain contract in `launch.json`
  and compare it with the capture before deriving coverage. Deleting a requested
  neighborhood and its views can no longer silently reduce the expected set.
  Animation already had this binding; a missing-clip regression now checks it.
- Native grader: only completed image-view events establish actual viewing;
  started and failed events are rejected. The observed native views completed.
- Documentation: the [first link audit](20261112/documentation-audit-01.json)
  finds a nonexistent queue README; the profile selector now links its actual
  specification. The failed audit remains retained. The [second audit](20261112/documentation-audit-02.json)
  incorrectly classifies the verifier-generated rolling wheel summary as historical
  evidence; its [original source](20261112/documentation-audit-source-02.py.txt)
  is preserved, and the corrected audit explicitly allows that generated summary.

The native [kit identity](20261112/native-kit.json) and archive remain unchanged.
The final-kit replays re-execute the corrected checker and capture sources;
independent native grading is not relabeled as execution of that newer kit.

## Required A–E review

| Question | Current answer and next consequence |
| --- | --- |
| **A — How to improve?** | Give the specialist one operation that exposes the relevant destination failure: planted contact over actual timing, or material joins in real neighborhoods. Keep arbitrary engine adapters outside these explicit contracts. |
| **B — Claude/Codex compatibility?** | Both hosts use the same frozen public operation from separate consumer roots. Qualification checks named role, complete instruction loading, actual calls, image viewing and independent caller consumption; no host reliability claim follows from one outcome. |
| **C — Contextual/artistic quality?** | Consumer declarations and BRIEF govern timing, pivots and corners. Mechanical pixel correctness remains distinct from visual continuity. The next real-art assignment must demonstrate a useful actual correction. |
| **D — Work from another repository?** | Fixed profiles ship with the kit and run against the caller's confined source/assets. The operation returns usable retained observations without bespoke renderer commands or caller-authored low-level state. Diagnostic state preparation is an evaluation helper only. |
| **E — Responsibility split?** | Runtime binds and records; renderers execute; independent checks measure; the profile/host judges actual art against caller intent; provider tools create authorized art; human acceptance remains separate. |

## Next work

[CF-09's concrete assignment](../../examples/domain-consumer-project/CF-09-ASSIGNMENT.md)
uses the appropriate consumer for a useful actual-art revision, preserving the
original failure and valid unrelated members. These controlled observations make
that comparison possible; they do not complete it. Continue the active PLAN cycle.
M1/M2, broader M3/M4, quality/reliability and unrelated Claude QOL-10 acceptance
remain open. Human acceptance does not halt authorized development.
