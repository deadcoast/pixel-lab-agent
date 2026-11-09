# Connected family and staged-request authoring

**Subsequent native checkpoint, 2026-11-09:** [both callers use this interface](../native-authoring/README.md)
and pass artifact/recovery checks. Codex catches and corrects an authority error;
Claude's per-criterion comparison remains partial. The implementation evidence
below retains its original scope and receipts.

Implemented 2026-11-08: `production-plan` / `pixl_production_plan` and
`stage-prepare` / `pixl_stage_prepare` replace repeated family graph wiring and
manual upstream-candidate binding. [The contract](../../spec/production-plan.md)
documents the ordinary JSON inputs and recovery behavior. The profile remains the
visual expert; these local adapters support its authored decisions.

The new operation retains existing contracts, adoption/proof, baseline identity,
member criteria, collective criteria and destination choices. It creates open
T/F/Q/X records, establishes direct prerequisites, binds current PLAR selections
to final outputs and links previously unallocated rows. It creates no verdict,
nomination, provider result or automatic requirement confirmation.

Staged preparation verifies exact accepted upstream candidates, retains the
reviewed request/inputs and uses existing durable jobs. Interrupted input publication
or PLAR linking resumes without duplicate records/jobs. Different pending attempts,
changed authored scope, wrong input bytes and unaccepted prerequisites are rejected.
Bound seed stages also check the final asset's current PLAR requirements/link at
ordinary preparation, dispatch and new task activation/completion. Unrelated rows
retain their independent status. Historical observations and submitted jobs remain
recoverable.

## Observed checks

Ten new regression tests cover these operations, including lost-link recovery,
unknown-job reuse, invalid/cyclic plans, semantic drift, downstream changes and
unrelated-member independence. A development assertion initially selected Retry
as an independent row; the fixture correctly declares that it depends on Working.
The test now uses Start, the genuinely independent row. This preserved the existing
consumer dependency semantics rather than weakening the runtime to fit the test.

The full verifier checks source behavior and clean wheel/copied-plugin execution
through the public CLI. The distribution probe authors a connected plan, binds an
accepted fixture input, prepares a request, repeats it without a new revision and
confirms all historical records are unchanged. Synthetic fixture acceptance does
not establish art quality.

The [final verifier](../verification-runs/20261108T143610.530795Z/result.json) reports
**546 passed, one Windows privilege skip**, 39 reference checks and both distribution
probes passing. Ruff and the configured Mypy check pass (63 maintained files); the
PIXL skill format validator passes. Mypy does not fully inspect untyped bodies.

A [first rehearsal](20261108/checks.json) copies the actual completed consumer,
reuses its approved baseline/contracts/criteria and generated seed, authors three
production stages plus collective delivery, and prepares the retained Working
animation request without dispatch. The original PLAR, destination bytes and all
old records remain unchanged. It is local preparation with historical transport
references, not proof that those references are still available remotely. Its
frozen kit predates the subsequent downstream-selection guard; later verification
and rehearsal identities remain separate.

The [final rehearsal](20261108-final/checks.json) repeats that operation with the
guard included in its separately frozen kit. All six preservation/preparation
checks pass. Its [plan](20261108-final/project/work/authoring-rehearsal/plan.json)
and [request packet](20261108-final/project/work/authoring-rehearsal/request.json)
are concrete examples derived from the existing consumer's recorded criteria and
accepted input. They are rehearsal artifacts, not a new production assignment.

Existing linked generations keep their explicit revision route; these APIs do not
silently replace accepted production. Existing C/D/I authoring remains available for
specialist contract/adoption decisions. Official schema discovery, upload handles,
provider execution, visual comparison and target rendering remain host/profile work.

## Required A–E review

**A — Improvement.** The completed production exposed repeated dependency and
selection wiring. The adapters now derive that wiring from reviewed stages and
exact inputs, preserving failure history and local acceptance rules. Next verify
whether cold callers can author these JSON inputs without maintainer repair.

**B — Host compatibility.** The same profile/skills and CLI/MCP operations serve both
hosts. Current Claude 2.1.318 and Codex 0.166.0 completed the separate cold package
consumption assignment through native delegation. This establishes the observed
installed routes, not every host release or same-child resumption. The new adapter
has source/installation checks; native authoring remains to be exercised.

**C — Context and art quality.** Exact baseline, contract, source, requirement and
input identities remain explicit. Decisions about shape, palette, transparency,
motion and reference roles belong to the host specialist and scoped caller review.
The adapter's dependency checks cannot judge aesthetic fidelity or ensure that a
provider URL carries the reviewed image. Both require actual inspection.

**D — Another project's workflow.** Work stays under the consumer root; installed
and copied runtimes execute the same operations. A cold caller can recover the
actual delivery and compare it independently. New authoring returns task/output
IDs and recoverable allocation diagnostics, keeping low-level graph construction
out of the caller's assignment. Older historical observations remain visibly scoped.

**E — Responsibility location.** The shared profile supplies domain judgment and
authority. PIXL's family/provider references route connected production; PLAR owns
source allocation; CLI/local MCP retain plans, inputs, jobs and current-state
checks. Official PixelLab tools perform generation and edits. Browser fixtures and
reference proofs remain optional, scoped verification infrastructure.
