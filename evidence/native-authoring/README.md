# Native connected authoring — 2026-11-09

This increment evaluates the connected `pixl_production_plan` and
`pixl_stage_prepare` operations through fresh native callers in copies of the
existing completed queue consumer. It does not replace the earlier
[actual production](../pixellab-family-production/README.md) or
[cold package consumption](../package-consumption/README.md) evidence.

## Conditions and evidence

Each caller receives the current frozen plugin, the actual consumer sources and
accepted assets, and an unlinked `authoring-plar.txt` planning branch. The original
allocation, assets, failed attempts, accepted state records and package remain
preserved. The assignment is to author Working/Retry/Paused and collective delivery,
bind Working to its accepted seed, prepare the next supported official request,
independently compare its exact criteria and arguments, and return a usable result.

Two declared events exercise recovery against the actual copied runtime:

1. The first allocation write fails after successful plan publication. Repeating
   the same plan must recover its links without a second graph.
2. After the first prepared request, a scoped caller update requires stationary
   reduced-motion Working behavior. The old request stays retained; current
   readiness must expose its obsolete requirements and the unmapped consumer route.

These are controlled, announced recovery conditions, not a blind production run or
new restrictions on normal paid PixelLab use. The wrapper delegates to the real
publication, preparation, PLAR and job implementations. The new regression checks
that actual dispatch rejects the changed selection without modifying the prepared
job or original allocation.

The [official discovery snapshot](20261109/official-discovery.json) retains current
host-exposed tool descriptions/declarations, their actual observation time, and an
official `pixelart_workbench describe animation` response. It is not raw tools/list
JSON. Provider JSON schemas projected from those declarations must say so. The
[official tool guide](https://api.pixellab.ai/mcp/docs) and
[PixelLab documentation](https://www.pixellab.ai/docs) remain the upstream references.
The native assignment ends at preparation/recovery; it adds no generated-art or
renderer acceptance.

## Native outcomes

The [independent behavioral review](independent-review/review.json) records a
**partial overall result**: both hosts use the adapter and recover correctly, but
Claude's caller-criteria comparison is incomplete. Each attempt retains its input copy,
frozen kit, prompt, launcher/version, event log, native transcript, caller result,
and exact output artifacts. No maintainer writes the evaluated caller's plan,
packet, comparison or result after launch.

| Host | Actual outcome | Remaining finding |
| --- | --- | --- |
| Codex CLI 0.166.0; 719.357 seconds | Native child authors three stages and collective delivery; interruption recovery keeps the same revision/hash; exact seed bytes enter an `animate_image` packet with explicit five-returned/four-selected frame policy. Caller compares all 13 criteria, catches a mixed authority label and obtains a separate correction. The changed requirement leaves the request prepared and blocked. | Initial specialist error remains preserved; named custom-role selection was not exercised. |
| Claude Code 2.1.318; 1686.081 seconds | Registered foreground PIXL agent authors the connected plan, recovers links, and prepares a documented four-seed workbench join. It retains a guarded rotation policy and blocks after the changed requirement. Parent independently checks sources, inputs, recipe, preservation and status. | Its final comparison groups 20 criteria and asserts agreement without establishing the authority/scope of stable cluster count, motif bans and lossless assembly restrictions. This review is partial. |

The stricter clauses can be valid choices for Claude's deterministic construction;
the missing evidence is the caller's explicit distinction between those choices
and the required artistic outcomes. The independent review does not declare the
recipe or artwork bad. Codex's caller makes this distinction for its no-resizing
finding and retains the original and corrective annotation separately.

Both [Claude](independent-review/claude-checks.json) and
[Codex](independent-review/codex-checks.json) pass 21 independent artifact/state
checks: all 376 original records, original assets/sources/allocation and frozen
kit bytes survive; exactly one new plan and one prepared job remain; three links
recover; the current Working requirement blocks dispatch; caller pointers resolve.
Claude's [proposed recipe check](independent-review/claude-recipe-check.json) finds
160 matching pixel guards and zero visible differences from retained Working.
This is local prediction checking, not provider execution or new acceptance.

Immutable [Claude](20261109/archives/claude-01-manifest.json) and
[Codex](20261109/archives/codex-01-manifest.json) archive manifests cover 1,914 and
1,924 files respectively; every archived file was re-read and compared with the
attempt. Native Codex journals retain some encrypted private payloads, so the
review claims only observable tool results, activity metadata and exact artifacts.

## Implementation verification

The [complete verifier](../verification-runs/20261109T082315.017109Z/result.json)
passes **547 tests plus one Windows symlink-privilege skip**, 39 reference checks,
and clean wheel/copied-plugin checks. This adds one evaluation regression to the
previous 546-pass source baseline. Ruff passes; Mypy reports no issues across 65
maintained files under its configured scope, which does not fully check untyped
function bodies. The runtime authoring implementation is unchanged by this increment.

The reusable case lives in `evaluations/plar_authoring_case.py`, its declared event
wrapper in `evaluations/authoring_mcp.py`, and dispatch-preservation regression in
`tests/test_authoring_evaluation.py`. Run new attempts through
`python -m evaluations.request_review_trials --host HOST --case plar-authoring --out FRESH_DIR --run`.
Never reuse an attempt directory or rewrite its original evidence.

## Required A–E review

**A — How can this improve?** The adapter removes manual task/output wiring and
recovers a real partial publication. First connect its exact authored criteria to
the existing request-review handoff so the caller assesses every member and
collective rule, including scoped construction choices. Then provide focused
authoring context: current source obligations, existing contract/baseline IDs and
the next input, without broad runtime-source exploration. A mechanically valid
contract can still misattribute a chosen production method to the owner.

**B — Host compatibility?** This checkpoint uses installed Claude Code 2.1.318 and
Codex CLI 0.166.0, native specialist delegation and the local MCP interface. That
qualifies the recorded route under these exact conditions, not every future host
version or general invocation reliability. Claude selects its registered `pixl`
agent. Codex spawns a generic native child named `pixl` and assigns specialist work
through task context and packaged skills; its journal records `agent_role:null`
and no `agent_type` argument. Named Codex custom-role selection is therefore not
qualified by this run. Official PixelLab execution remains in the host; local
tools retain state and check consistency. Claude same-child continuation remains
a separate open qualification.

**C — Contextual and artistic quality?** Real consumer contracts, exact accepted
seed bytes, prior rejected animation and actual family acceptance are available.
The model still chooses the method and evaluates its tradeoffs. Correct schemas,
hashes and assembly policies do not prove a better animation or final art quality.
Keep recipe constraints scoped and retain qualitative outcome criteria.

**D — Operation from another repository?** The copied consumer is the working root;
the installed kit is read-only support. The original production and prospective
branch have distinct allocations and identities. The returned result must name
the retained request, changed requirements and precise next consumer/contract work;
another agent should not reconstruct these from an informal summary.

**E — Where does the workflow live?** The shared profile owns expert judgment;
PIXL/PLAR skills route intake, allocation, production and independent review;
`spec/production-plan.md` defines the optional authoring adapter; local MCP/CLI
implement its deterministic publication/preparation and existing job lifecycle;
official PixelLab MCP/API performs production. The evaluation fault wrapper and
consumer renderer are verification infrastructure, not production dependencies.

## Remaining scope

Broader generated quality and native end-to-end reliability remain open. The
immediate repair is Claude's complete criteria/authority comparison through the
shared handoff, followed by fresh behavioral verification. The
reduced-motion change exists only in these evaluation branches; it is not silently
added to the accepted original commission. A subsequent useful continuation can
review that consumer mapping, resolve the obsolete prepared intent through its
existing lifecycle, and author a reviewed successor without losing family context.
This checkpoint does not declare the overall specialist ecosystem complete.
