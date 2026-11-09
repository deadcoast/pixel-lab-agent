# Style, family and consumer rendering — 2026-11-08

This increment continues the existing Ready consumer and corrected contract from
[handoff repair](../handoff-repair/README.md). It develops the specialist workflow;
the retained Ready image remains a controlled provider fixture. The native cases
ask PIXL and its caller to decide the sample's style role, review the actual family,
render both source consumers and preserve the exact continuation. They do not
provide an expected style decision or fabricate the three absent members.

**Current outcome:** scoped style review, available-member rendering and exact
continuation are verified in both hosts, with the original failures and explicit
guided corrections preserved. [Checks, version identities, grades and archives](checks.json)
bind the results. Full-family production and upstream generated quality remain open.

## Implementation and observed rendering

The [queue example renderer](../../examples/plar-project/README.md) imports the
actual backend and shared full/compact view modules. It uses their paths, cell size,
scale, panel color and frame timing. Missing artwork stays visibly missing. Its
capture retains browser identity, served module/image hashes, actual destination
pixels, per-view images, event transitions and frame-boundary observations.
The separate checker compares these images with the source PNG, alpha composition,
nearest-neighbor blocks and screenshot coordinates. It supplies no style verdict.
The original vector Start asset remains unchanged.

To open the reviewed consumer from the repository root, run:

```powershell
node examples/plar-project/renderer/server.mjs --project evidence/style-family-rendering/20261108/native/codex-render-recheck-01/project
```

Open the printed loopback URL. This uses the retained source and image files without
changing their production state. The [saved destination screenshot](20261108/native/codex-render-recheck-01/project/work/pixl-render-recheck-01/destination.png)
shows Ready and preserved Start in both views, with the three absent members visible.

Actual checking found two defects in the new renderer/capture implementation:

- Fractional layout coordinates prevented exact screenshot/pixel correspondence.
  Integer dimensions and text metrics corrected the layout. The [failed capture](20261108/renderer-alignment-failed/checks.json)
  and exact pre-change source remain available.
- Independent replay found an intermittent late viewport resize in Chromium's
  `--screenshot` route despite one [passing capture](20261108/renderer-viewport-corrected/checks.json).
  The corrected helper sets metrics before navigation, waits for the consumer and
  captures its report/layout/screenshot in one isolated CDP page. The [first corrected
  capture](20261108/renderer-cdp-corrected/checks.json) passes 104 checks. Independent
  replay and native outcomes remain separate evidence.

The [synthetic animation/alpha probe](20261108/renderer-probe/checks.json) passes
155 observations, including four distinct frame crops and the 400 ms loop boundary.
Its handmade test pixels are renderer test data, not family assets or art acceptance.
The original four-state consumer and later paused-state/renamed-destination consumer
both execute through the same renderer.

## Verification scope

The [final full verifier](../verification-runs/20261108T113550.638557Z/result.json)
passes **530 tests, one Windows symlink-privilege skip, 39 reference checks and clean
wheel/copied-plugin installations**. Six new regressions cover real-module serving,
changed-source/fractional-placement rejection, RGB screenshot corruption despite
opaque alpha/updated hashes, stage preservation and completed/interrupted recovery.
[Ruff, Mypy across 62 files and Node syntax checks](20261108/final-static-checks.json)
and [both skill format checks](20261108/final-skill-checks.json) pass. The earlier
[527-pass receipt](../verification-runs/20261108T095617.763912Z/result.json) predates
the CDP correction; the [529-pass receipt](../verification-runs/20261108T101958.581534Z/result.json)
predates the final caller-completion guidance and interrupted-stage recovery.
The [530-pass renderer/caller-repair receipt](../verification-runs/20261108T102334.684631Z/result.json)
precedes the final clarification to compare a numerical claim with its original
inputs. The [numerical-guidance receipt](../verification-runs/20261108T110546.668038Z/result.json)
includes that change; the final receipt also verifies the evaluation-only auto-memory
environment fix. Each reports 530 passing tests and the same one platform skip.

## Native outcomes and recovery

Both native01 cases started from the same retained Claude04 consumer. Their frozen
helper predates the CDP correction. Original results and exact helpers remain in
the [Claude archive](20261108/archives/claude-01.manifest.json) and
[Codex archive](20261108/archives/codex-01.manifest.json).

- **Codex01:** completed the scoped style/family review. It adopted exact Ready
  bytes for this family, retained three missing members and an open collective
  delivery plan, corrected earlier measurement descriptions and saved the exact
  current handoff. Its own capture failed viewport/position checks; it correctly
  withheld exact destination acceptance. Independent review found no model failure
  in that result. The failed check was not replaced by an offset-based pass.
- **Claude01:** incomplete parent delivery. It produced useful caller notes and
  specialist drafts, but the caller ended while its background specialist ran.
  The host later stopped that child. No required family result, final style decision,
  family commit, PLAR refresh or new handoff was delivered. Its original sources,
  state and PLAR stayed unchanged. Both captures failed the old helper's viewport
  checks. A caller note also counted each intermediate SVG edge tone as the total;
  that numerical description needs correction before adoption.

The shared delegation workflow now keeps required specialist completion, caller
comparison and handoff on the caller's critical path. Foreground/wait behavior is
documented by [Claude Code](https://code.claude.com/docs/en/sub-agents#run-subagents-in-foreground-or-background);
the repair changes no user-wide settings or model choice. Exit zero is not a
completion verdict. Background work remains useful while independent caller work
continues.

The explicit guided cold continuations use the separately copied corrected helper
and retain the original results/drafts. They are not fresh blind trials or resumed
native child conversations. The [Codex recovery passes independent review](independent-review/codex-render-recheck-01/REVIEW.json):
104 pixel/identity checks, 44 independent source/transition checks, all eight
available views at their recorded positions, and exact current handoff. It preserves
all 121 previous state records and appends four scoped destination records. The
three missing members and collective delivery stay open, and changed-contract
selection diagnostics remain explicit.

Claude's guided recovery delivers both required results, scoped caller adoption,
PLAR updates and the exact handoff. Its independent caller and specialist captures
pass 104 checks each; independent source/transition replays pass 44. It correctly
reconciles the vector's edge counts. Native child resumption fails with `No transcript
found`; the caller explicitly restarts from saved artifacts and waits for the new
specialist rather than claiming resumed memory. The original production state stays
unchanged; missing-member planning is retained in PLAR and collective acceptance is
not claimed. This raw assignment did not require identical state-record construction
in both hosts.

The recovery remains **partial for one descriptive finding**: it confirms the older
arm-axis explanation without checking the endpoints used by that explanation. Pixel
partitions and vertical extents do not verify those axis lengths and angles. The
shared review guidance now requires the original claim, input convention, calculation
and correction together. A focused guided numerical correction has returned a new
specialist calculation, independent caller calculation, PLAR evidence/next updates
and exact handoff. The [focused correction passes independent review](independent-review/claude-measurement-correction-01/REVIEW.json):
600 artifact identities, 27 result references, 24 nested references and 58 numerical/
state checks agree. All five requirement hashes, all 87 production records, art and
captures remain unchanged. PLAR gains the correction evidence and clearer next work.
The earlier partial grade stays preserved. No recapture was performed.

The [package version ledger](20261108/package-version-boundaries.json) distinguishes
the renderer/caller-recovery package from the final numerical-guidance package and
their refreshed proof receipts. The numerical correction is an explicitly guided
cold restart from Claude's completed recovery, not an unassisted fresh trial.

### Ambient host memory

The correction's public trace also records the caller updating Claude's project
auto-memory outside the consumer fixture. The [observation](independent-review/claude-measurement-correction-01/ambient-memory-observation.json)
is separate from the passing task proof; these runs do not establish clean host-memory
isolation or confinement of every write. The external note was not read or modified
by the maintainer/reviewer as part of this audit, and its host authorization is not
inferred from the public task trace.

Future evaluation subprocesses set and record `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`,
the [documented per-process override](https://code.claude.com/docs/en/memory#enable-or-disable-auto-memory).
This changes no production profile or persistent host configuration. The [propagation
probe](20261108/ambient-memory-environment-check.json) uses a controlled Python child
through the actual runner; it is not another native-model trial or filesystem sandbox.
The retained native attempts remain under their original conditions.

The [maintainer measurement check](20261108/measurement-description-check.json)
reconciles the old quoted endpoints and actual decoded pixels. The quoted vectors
do not establish the asserted 45-degree axes or 1:2 length ratio. This corrects a
description without rejecting the image or adding an owner-mandated shape recipe.
Native specialist/caller observations are evaluated independently.

## Required A–E review

**A — Improvement.** The ordinary path now has a concrete graphical consumer and a
retained pixel check, beyond source mapping alone. Shared family guidance separates
sample adoption, available members and unfinished collective review. Found capture
failures are retained and corrected before claiming reliable destination evidence.
The completed Codex operation also exposes manual family-plan assembly: its first
continuation adds 34 records through the existing state workflow. Preserve that
working representation, but evaluate a focused family-plan interface against actual
member production before adding more orchestration. Focused PLAR and exact handoff
already help continuity; the renderer and synthetic probes remain optional consumer
verification infrastructure, not installation prerequisites for every asset task.
Claude retains this review's missing-member continuation in PLAR without creating
a new PX2 family plan. That is sufficient for this scoped review; applicable member
and collective plans are still needed before their future production. A fixed amount
of state machinery is not the acceptance condition for every visual assignment.

**B — Host compatibility.** Shared skills supply workflow; the host supplies existing
knowledge, reasoning and available tools. Node/Chromium are tools for this consumer
fixture, not new PIXL runtime installation requirements. Both native host results
and their exact package/helper versions are evaluated separately.

**C — Contextual and artistic quality.** The sample decision must identify the actual
bytes and which properties guide later members. A glyph's treatment does not dictate
all siblings' shapes or prove unseen animation. Source measurements, rendered
observations and expert visual judgment remain distinct; a clean checker is not
evidence of upstream PixelLab quality or a complete family.
The hosts can legitimately adopt different scoped treatments. Claude explicitly
chooses a tighter stroke/fill/edge treatment under the caller's assigned authority;
Codex retains broader continuity properties. This difference is not a defect by
itself. Unreconciled factual claims remain defects even when the style choice is
valid and the image is readable.

**D — Consumer operability.** The entry point reads actual modules and mapped files
in the supplied consumer root. It follows renamed destinations and source states,
preserves the vector control, exposes missing members and exercises both shared
views. Its verified scope is this representative browser consumer, not another
application or engine.

**E — Responsibilities.** The profile owns specialist judgment, the intake/family
skills own scoped adoption and continuity, PLAR owns allocation/next work, and PX2
retains production history and acceptance. Local MCP operations preserve that state.
The browser helper observes the consumer; it is not a new asset producer or global
model. Official PixelLab operations remain the production generation interface.

## Remaining scope

Working, Retry and Paused have no delivered art in this retained consumer. Complete
family continuity and actual PixelLab-generated quality remain separate from the
available Ready asset's graphical integration. The [master TODO](../../TODO.md)
retains the wider production milestone and native same-child continuation qualification.
