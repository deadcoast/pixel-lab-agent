# Native trial records and Claude continuation

Development increment: **2026-11-09**, cycle `IDENTIFY-2026-11-09-01`,
**[M2 | TM-06, CF-04 | PX-EVAL-005, PX-OPS-004]**. M1 remains open.

**Result:** recording mechanics and one Claude same-parent/same-child continuation
across separate processes pass. The interrupted 20-to-29 comparison completes
through explicit artifact recovery, followed by native reconciliation. This does
not close M1 or broader host reliability. [Result and exact identities](20261109/RESULT.json).

## Implementation

The [common trial runner](../../evaluations/request_review_trials.py) now uses a
[durable attempt recorder](../../evaluations/native_trial_records.py). It saves
actual parent/child IDs, host version, launch/configuration hashes, observed output
files, raw stream locations, interruption reason and native transcript availability
while the process is running. Completed attempts retain transcript snapshots.
Every metadata record remains behaviorally ungraded until its outputs are reviewed.

New Claude trials preserve sessions. A separate invocation can resume the exact
parent and send the observed child a follow-up, using the same consumer, agent
definition, MCP configuration and frozen package. Preparation and execution both
check prior inputs and package payloads. Changed or missing inputs fail explicitly;
they do not silently create a replacement child. Old failed records remain intact.
The [maintainer guide](../../evaluations/NATIVE-CONTINUATION.md) documents the three
routes: new session, native continuation and restart from retained artifacts.

This is evaluation infrastructure. PIXL's shared profile, skills, domain knowledge,
official PixelLab connection and production state format retain their existing roles.
The consumer stays in ignored build storage across rounds; evidence retains new
outputs and exact transcript snapshots instead of another complete consumer copy.

The base consumer is `project/` in the retained
[focused Claude archive](../focused-authoring/20261109/archives/claude-01.zip).
The [new entrypoints](20261109/consumer-entrypoints.zip) contain only this
evaluation's AGENTS, SESSION and continuation assignment. Preparation copies the
frozen production kit into `.agents/skills/continuation-kit`; its manifest and
every payload hash are retained in phase 1's `identity.json`. Native transcripts
are evidence of the local run, not portable host-session installation files.

## Historical diagnosis

The earlier [focused Claude attempt](../focused-authoring/20261109/native/claude-01/record.json)
was launched with `--no-session-persistence`. It exhausted usage credits after
retaining its proposal/report and a partial renderer, before finishing the caller
comparison. Its original 20 mappings and **29** proposed criteria are distinct from
the later 20-to-23 comparison. The new
[historical observation](20261109/historical-focused-claude.json) records the actual
session/child, disabled persistence, usage interruption and absent resumable parent.
It does not change the original grade or invent a recovered native session.

Earlier `No transcript found` failures therefore occurred under a configuration
that explicitly suppressed resumable print sessions. This identifies a concrete
harness defect; it does not establish that every historical failure had that sole
cause. Current official [CLI](https://code.claude.com/docs/en/cli-reference) and
[subagent continuation](https://code.claude.com/docs/en/sub-agents#resume-subagents)
documentation were checked on 2026-11-09. Actual installed behavior is recorded
separately below.

The [historical Codex observation](20261109/historical-codex-record.json) preserves
the actual parent and generic child from the existing everyday-guide consumer. Its
native role metadata is null. Reading this journal is not a new Codex behavioral
trial, named-role qualification or Codex continuation result.

## Retained comparison recovery

[Phase 1](20261109/phase1-claude-01/record.json) completes in Claude Code 2.1.318,
using one registered `pixl` child. Parent session:
`a2057b27-4422-46ee-8eaf-8e12c438ffae`; child: `a740390f35e32deea`.
The [caller result](20261109/outputs/PHASE1-CALLER.json),
[independent caller review](20261109/outputs/CALLER-REVIEW-01.json) and
[specialist assessment](20261109/outputs/SPECIALIST-ROUND1.json) preserve the
original proposal and its exact 20-to-29 comparison. This is explicit recovery from
saved artifacts, not continuation of the old non-persistent child.

The [independent phase-1 checks](20261109/phase1-independent.json) confirm literal
criteria, mappings, 30 source identities, 68 cited excerpts and 991 unchanged
consumer inputs. The caller's own preservation check additionally covers both kits.
Twelve caller findings include a proposed stationary-frame recipe labelled as a
requirement, differing Retry/Start authority, an assembly-policy citation pointing
to reuse instructions, and actual-playback obligations unsupported by the sampled
renderer checks. Coverage is complete; agreement and adoption are separate.
The child contributes three findings the caller independently verifies and adopts;
two caller findings are explicitly sent back for reconciliation.

[Three temporary errors](20261109/phase1-tool-errors.json) remain in the raw trace:
two caller readouts assumed an optional `notes` field, and one specialist citation
assertion used an incorrect range. Claude corrects them within the attempt. The
specialist report is about 218 KB and the caller report about 160 KB: resumability
is improved, but compact authoring context and broader efficiency are not thereby
qualified. No production adoption or new renderer/art verdict is made here.

## Same-child continuation across processes

[Phase 2](20261109/phase2-claude-01/record.json) runs `--resume` against the exact
phase-1 parent, preserving the consumer, custom agent definition, local MCP config
and frozen kit. The raw stream records `SendMessage` at line 17 and its successful
result at line 20, with `resumedAgentId` identifying the original child. Subsequent
work and completion come from that child; no replacement Agent call occurs.
The retained child transcript preserves the entire phase-1 prefix and extends it.

The [round-2 reconciliation](20261109/outputs/SPECIALIST-ROUND2.json) addresses all
12 caller items: ten agreements and two narrowed interpretations. Its 29 rows keep
every original literal check, carry-over ID and original record identity. Eleven
check texts change, eleven other rows receive authority/scope/source/route changes,
and seven stay unchanged. This is an explicit addendum, not an adopted executable
production plan. The [parent result](20261109/outputs/PHASE2-CALLER.json) verifies
the response independently and accepts both narrowings from actual sources:
Retry's held-cell obligation combines the brief with the caller update; the fixture
has live playback only at 3x, while its 1x matrix is static.

[24 independent checks](20261109/independent-checks.json) pass, covering parent/child
identity, unchanged configuration and earlier outputs, transcript continuity,
literal comparison, all twelve caller findings, input/source hashes and 49 round-2
source excerpts. The [first grader result](20261109/independent-checks-01.json) had
one failure because the checker expected carry-over objects where the addendum
uses ID strings and retains hashes separately. The corrected checker verifies
both representations' IDs and all original hashes; native outputs were unchanged.
The [initial checker](20261109/grade-01.py.txt) remains alongside the final grader.

Phase 1 took 1667.935 seconds; phase 2 took 680.106 seconds. Both exited zero, but
completion is established by the reviewed returned files and trace, not exit code
alone. This single native continuation does not qualify repeated resumptions,
long gaps, other machines, named Codex roles or general model reliability. It also
does not determine whether child memory or re-reading retained files supplied a
particular fact. The interrupted predecessor remains unchanged and incomplete as
originally recorded; this separately identified recovery completes its comparison,
not its production/rendering assignment. Later accepted successor work remains
separately scoped.

## Local verification and exact versions

Nine new regressions cover partial streams, usage interruption, actual subprocess
timeout, scoped evaluation environment, immutable historical inspection, same-parent
preparation, configuration/package drift, and real-shape Codex identity metadata.
The [final full verifier](../verification-runs/20261109T201648.803400Z/result.json)
passes **604 tests with one Windows symlink-privilege skip**, 39 reference checks,
benchmark, and fresh installed-wheel/copied-plugin probes. Its 158 checked input
hashes match the final source. Ruff passes for the changed maintained Python files.

The [first broad run](../verification-runs/20261109T200845.317353Z/result.json)
retains two failures and three errors caused by restricted loopback, junction and
package-cache access. The successful rerun permits those operations and uses a
repository-local uv cache. The earlier [focused failure](20261109/verification/focused-01.txt)
exposed sandbox-hidden Windows process enumeration; termination now falls back to
the owned process handle and reports that tree termination was not confirmed.
It is not relabelled as a successful whole-tree termination.

Both native rounds use the frozen `ec66264` production package, manifest
`f4f46268a88208f3b754fae5f59fd2dacd50b58f8d7759a0b94974332f23e640`.
The full verifier regenerates four bundled proof/measurement resources and their
references, producing manifest
`c2d39b0b288cadac0c50aa2d4c9f9d59b7f3e185e84f6bf8671e7a06f7986ff9`.
All 172 final entries match their payloads. Runtime, profile, skills and scripts
are identical between the native and rebuilt packages; they are not described as
byte-identical packages. Each attempt retains the exact recorder source it ran.

## Required A–E understanding

- **A — Improvement:** retain useful partial work and exact native identities during
  execution; continue in the original consumer with new attempt logs. This makes
  interrupted comparisons recoverable without duplicating whole trial trees or
  treating process success as semantic acceptance.
- **B — Platform compatibility:** Claude persistence plus same-parent resume and
  `SendMessage` to a custom child follow the documented native model. Availability
  is observed from real transcripts, not assumed from configuration. Codex uses its
  actual journal metadata; named-role and native-resume qualification remain open.
- **C — Contextual/artistic quality:** literal criteria, owner authority, expert
  proposals, source locators and prior corrections survive recovery. The host model
  still supplies PIXL's visual judgment. This comparison does not establish new
  generated-art quality or destination acceptance.
- **D — Another-project use:** the same consumer and frozen kit are retained across
  process boundaries; the saved assignment names exact inputs, outputs, scope and
  follow-up. Native history is machine-specific; durable files enable an explicitly
  separate restart when that history is unavailable.
- **E — Responsibility placement:** production judgment belongs to the agent profile;
  workflow belongs to skills; deterministic state and provider operations belong to
  local tools and official PixelLab tools. Trial recording belongs in evaluations,
  with its own guide, rather than expanding the consumer's production interface.

Continue through [TODO](../../TODO.md), [SHELVED](../../SHELVED.md) and
[PLAN](../../PLAN.md). The current audit cycle remains active.
