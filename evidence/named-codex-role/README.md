# Named Codex role qualification

Development increment: **2026-11-09**, cycle `IDENTIFY-2026-11-09-01`,
**[M2 | CF-05, TM-06 | PX-EVAL-005]**. M1 and M2 remain open.

**Result:** the corrected cold trial passes **28 independent checks** for explicit
registered-role loading, useful retained-asset operations and completed same-child
follow-up. **30 focused infrastructure tests** pass. The two unavailable routes
and one scope-conflicted partial remain preserved. [Exact results](20261109/RESULT.json).

The assignment uses the existing accepted queue consumer. It tests a cold caller,
the registered `pixl` role, exact profile/skill loading, useful public-operation
results and a completed follow-up to the same child within one parent process.
It assigns no new provider work, art acceptance or renderer execution.

## Observed host routes

The installed host is **codex-cli 0.167.0**. The unchanged repository
[role](../../.codex/agents/pixl.toml) is copied into the consumer, whose discovery
wrappers lead to a frozen portable kit. The host model and its available tools
still provide execution and specialist reasoning.

- [Attempt 1](20261109/codex-01/outputs/CALLER-RESULT.json) exposes a spawn schema
  without `agent_type`. The caller records the unavailable route without spawning
  a generic substitute. No specialist assignment completes.
- [Attempt 2](20261109/codex-02/outputs/CALLER-RESULT.json) enables the installed
  `multi_agent_v2` feature for that invocation and observes the same omission.
  This is another retained qualification failure, not a semantic art failure.
- [Local discovery probes](20261109/discovery/PROBES.json) inspect actual rendered
  tool definitions without model sampling. Trust overrides and an empty project
  configuration do not expose role selection in those probes. An explicit
  session `agents.pixl.config_file` setting does expose it. Two failed probe
  preparations remain recorded separately from successful rendering.
- [Attempt 3](20261109/codex-03/outputs/CALLER-RESULT.json) uses explicit session
  registration and a cold `fork_turns="none"` child. Native metadata records
  `pixl` and the injected instructions. The child completes a same-child follow-up
  and unchanged-review replay, but the handoff remains blocked: the evaluation
  restricted new files to its report directory while assigning a public handoff
  that writes to `.pixl/handoffs`. This is a contradictory fixture restriction,
  not a failed production operation. The caller honestly returns a partial result.
- [Attempt 4](20261109/codex-04/outputs/CALLER-RESULT.json) reruns the cold assignment after explicitly permitting new immutable
  handoff files in that public operation's directory. Reports remain under
  `work/named-role`. The exact role, package and original production are unchanged.
  Its [28 independent checks](20261109/codex-04-independent-final.json) pass.

The probe reproducer is identified as written after the observations. Configuration
and raw tool-schema evidence support the tested route; a CLI version label or the
presence of a TOML file alone does not establish role loading. No global settings
were changed. File-only automatic discovery remains unqualified by this increment.

Current official [custom-agent documentation](https://developers.openai.com/codex/subagents)
describes standalone role files and inherited host capabilities. The
[configuration guide](https://learn.chatgpt.com/docs/config-file/config-basic)
describes session overrides and project trust. The upstream
[role loader](https://github.com/openai/codex/blob/main/codex-rs/agent-roles/src/loader.rs)
supports explicit role-file declarations; that mutable source explains a candidate
route, while the retained installed-host observations establish what ran here.

## Completed assignment and limits

The final parent is `01a1c2bd-ef78-7680-98c5-1c7544673c46`; its one child is
`01a1c2be-20a4-7541-9d8f-b635d58c3192`, native path `/root/pixl_specialist`.
The parent selects `agent_type="pixl"` with a fresh context. Child session metadata
records that actual role and the same consumer root; the developer message matches
the exact configured role instructions. Native source reads establish that it then
loads the shared skill, profile and applicable references. These are different
proofs from the child's self-description or a generic child's task name.

The specialist returns exact authoring, selected-asset and candidate/family context,
plus an original source excerpt. The caller separately reads public state, hashes
the returned files and checks the selected generation and acceptance. It then uses
`followup_task` on the same child, which completes a new attributed turn, reuses the
unchanged family review and saves the public handoff. Native execution and actual
returned bytes support the checks; report-shaped JSON alone is insufficient.

All **4,142** baseline files retain their original hashes. State remains revision
**126**, with canonical hash
`fea95799d4c0686e4e7b40e4ffdfaf9b8083363f98d76c33a0c22c1720cc492e`.
The review replay returns `reused_review: true`, no production publications and
`remote_executed: false`. The only new file outside the report directory is the
immutable [handoff](20261109/codex-04/handoff.json), also preserved in the
[consumer delta](20261109/codex-04/consumer-delta.json).
Its exact selected requirements, state, resume data and next action match a fresh
public read. Current acceptance remains complete; creation-time family acceptance
remains false. No historical receipt is rewritten to imply a later review.

The final attempt takes **243.26 seconds** and needs no maintainer intervention
after its corrected launch. This is one successful observed route with one
same-process follow-up. It does not qualify file-only automatic discovery,
cross-process Codex resume, repeated or long-gap continuation, other versions,
new generated quality or native end-to-end production. The original brief defect
and partial attempt remain relevant setup evidence.

## Implementation and evidence retention

The [scenario](../../evaluations/named_codex_role_case.py) registers the exact role
for the isolated invocation, supplies the scoped assignment and current consumer
paths, and keeps native outputs separate from historical files. The common trial
launcher uses the same explicit registration for subsequent Codex evaluations.
The production profile, shared skills, runtime and saved-state format are unchanged.

The [recorder](../../evaluations/native_trial_records.py) retains configuration
hashes, actual role metadata, tool declarations, collaboration calls and exact
instruction matches. Requested roles remain distinct from observed child roles.
Inherited history is not counted as new child work; a cold-child boundary requires
correlation with its actual parent spawn. These observations remain behaviorally
ungraded until checked against returned files and completed work.

The existing predecessor had 560 ignored `.pixl` files, including its current
state and reviews. The [baseline supplement](20261109/baseline-untracked.json)
and ZIP preserve those bytes alongside the predecessor files tracked at
`fc056f9049367f5ba8c1496c746be1013cc64903`. Preparation restores missing inputs into
the new consumer and verifies hashes; it never repairs or rewrites the predecessor.
The archive is evidence for this fixture, not another production dependency.
[Exact recovery checks](20261109/baseline-recovery-check.json) verify all 3,798
original recorded inputs against 3,238 committed Git blobs and 560 archived files.

Each attempt retains its entrypoints, exact executed scenario/recorder sources,
launch, input hashes, raw stream and native journals. New work outputs and a
consumer file delta preserve newly written immutable handoffs, including files
under ignored `.pixl`. Unexpected edits would be preserved and fail the scope
checks. A new handoff file is permitted; a new production-state publication is not.

## Fresh verification

[Focused verification](20261109/verification/focused-final.json) passes **30 tests**:
17 recorder/launcher tests (eight added to the prior nine), plus 13 scenario/grader
tests. They cover role registration, cloned-consumer configuration, cold versus
inherited instruction context, actual role versus requested role, missing/failed
follow-up, archive recovery/tamper, report rejection and ignored handoff retention.
[Ruff](20261109/verification/ruff-final.txt) passes for the changed maintained Python.
This is evaluation infrastructure; the evidence-mutating full verifier and package
rebuild were not rerun. The prior 604-pass/one-skip full result remains historical.

The independent checker binds native public calls to their successful results,
checks caller verification, source excerpts, file hashes, selected state, immutable
handoff content and retained bytes. The first attempt-3 checker also counted a
compact replay receipt as a full result, causing an extra false failure. Its
[original result and source](20261109/codex-03-independent-01.json) are preserved;
the corrected checker distinguishes the receipt from the full result. Native files
were unchanged. Final grading of every attempt uses separately retained exact
checker sources; earlier grades are not overwritten.

## Required A–E understanding

- **A — Improvement:** make the actual named role selectable in isolated native
  evaluations, retain the observed configuration, and make this accepted consumer
  reproducible from tracked evidence. Role selection and useful continuation have
  separate checks.
- **B — Platform compatibility:** the installed CLI needs explicit registration in
  this isolated setup. The earlier generic-child successes and the two unavailable
  routes remain distinct. Same-process follow-up does not establish cross-process
  Codex resume, repeated continuation or other host versions.
- **C — Contextual/artistic quality:** preserve the selected generation, source
  authority, current versus creation-time acceptance and prior evidence limits.
  Reusing an accepted family supplies no new generated-art quality judgment.
- **D — Another-project use:** consumer wrappers resolve a complete frozen kit;
  mutable outputs stay in the consumer. Exact role, package, state, source and
  result identities support a usable handoff and independent inspection.
- **E — Responsibility placement:** the profile supplies specialist judgment;
  shared skills supply the workflow; public tools manage deterministic production
  state. Role registration and trial grading belong to host setup/evaluations,
  not to new UDL syntax or caller-written production records.

Continue through [TODO](../../TODO.md), [SHELVED](../../SHELVED.md) and
[PLAN](../../PLAN.md). The next substantive group is **M2 CF-03**, artistic authority
through native revision, with **TM-04** tool-contract checks before affected live
requests. Preserve this active cycle and the broader unmet outcomes.
