# CF-07 changed requirement through integration

Development increment: **2026-11-11**, active cycle `IDENTIFY-2026-11-09-01`,
**[M3 | CF-07, NF-06 | PX-PLAR-002, PX-PROD-001]**. Status: **bounded CF-07/NF-06 outcome complete**, with scoped native passes in
both hosts, full verification and separate final-kit compatibility replays. M1/M2 and broader
M3, generated quality and host reliability remain open.

## Bounded assignment

This follows the [CF-06 allocation/update outcome](../plar-coverage/README.md) in
the active plan. The scenario reuses the exact tracked historical queue source/art
closure and preserves the original `plar.txt` byte-for-byte. It creates a fresh
`integration-plar.txt` and a genuine public 100 ms prepared intent/store before
the controlled change to 150 ms. The ignored original producer state is neither
retained nor reconstructed, and old historical reviews supply no current
acceptance. Preservation covers the original tracked source/art and all history
of this fresh prospective intent and its successors, rather than an unavailable
historical producer store. The
[Codex identity](20261111/codex01/identity.json),
[baseline preparation](20261111/codex01/baseline-prepare.json) and
[source-change record](20261111/codex01/source-change.json) retain this boundary;
the [Claude identity](20261111/claude01/identity.json) and
[source-change record](20261111/claude01/source-change.json) describe the same
controlled setup.

The completed operation demonstrates these connected steps:

1. Prepare an undispatched request against the prior 100 ms selection, then change
   the actual consumer requirement and refresh the affected allocation.
2. Observe the stale request guard and explicitly abandon that obsolete local
   intent before authoring the successor. No remote request is inferred.
3. Reuse the exact existing Working sheet as a new candidate, with accurate
   provenance and fresh review against the 150 ms requirements. Existing art or
   historical acceptance does not accept the new requirement.
4. Author a delivery-only family around the accepted sample without a dummy
   production stage, retain the exact package, and execute both actual full and
   compact consumers at the revised timing.
5. Import structured, hash-bound NF-06 destination observations and retain their
   supporting files. Explicit collective review and parent handoff remain
   separate operations.

This assignment covers reused-art integration. It does not commission new paid
art or complete CF-10's useful official production outcome per host. The earlier
queue production and acceptance evidence retain their original scopes; they are
inputs to this increment, not new verification of the changed requirement.

## Implementation and verification status

The [production-plan adapter](../../spec/production-plan.md) now accepts an empty
`stages` list for delivery around existing outputs. Plan version 1 and PX2 wire
semantics are unchanged. Ordinary family validation still requires a nonempty
member set, valid baseline/project relationships, destinations and collective
criteria. Open plans may retain an unaccepted baseline; activation, completion
and snapshotting retain their existing eligibility and pending-work checks.

The local delivery-only enabler passed 17 production-plan tests and 21 delivery
tests, including four new regressions for direct sample delivery/retry, invalid
families, unaccepted baselines and pending jobs. Ruff and the scoped diff check
passed. These 38 tests include existing coverage and establish local adapter and
family behavior only. No provider/model call or bundle build was part of that
verification.

The [NF-06 importer](../../spec/destination-observation.md) is implemented through
shared `destination-import` / `pixl_destination_import` surfaces. It checks the
current candidate binding, canonical package, exact served members, declared
renderer/consumer source identities, view/motion references and all supplied
output hashes. A deterministic ZIP retains the complete declared report inputs
and outputs; separate exact PNG previews support inspection. Ordinary candidate
review can retain that ZIP so evidence survives removal of the working export.
The importer writes evidence files but does not run the renderer, change state,
create verdicts or grant acceptance. Its observation category does not attest
that the reported execution occurred.

The [example observation bridge](../../examples/plar-project/renderer/observation.py)
converts the existing capture output into the structured report, using explicit
member destinations. The [bounded scenario](../../evaluations/integration_change_case.py)
retains the prepared 100 ms intent, source change to 150 ms, exact-byte Working
reuse and explicit delivery/review route. The assigned capture scope separates
1×/3× static views, actual 3× live playback in both full and compact consumers,
and a controlled 1× timeline probe. **1× live playback remains unperformed**; the
controlled timeline is not a live observation at that scale.

Both native trials retain their original attempts. Their frozen package identities are in
[Codex identity](20261111/codex01/identity.json) and
[Claude identity](20261111/claude01/identity.json), each with bundle-manifest SHA-256
`198d62deabda79ddc559768c5d4178ac0185ef3e04169f7f51c9f00f4d7d619d` and per-file
identities. Those kits were frozen before the final CLI-only correction making
relative `STATE` resolve from the working directory within `ROOT`, plus its spec
clarification. The full verifier also legitimately rebuilt tracked reference
proofs (the art-method proof report, atelier measurements/project state and knowledge
library state) and corresponding bundle resources. Previous bytes are archived
in both the [first verifier](../verification-runs/20261111T213830.574343Z/previous.zip)
and [final verifier](../verification-runs/20261111T220620.742582Z/previous.zip)
archives, with their manifests alongside. The final bundle therefore differs
beyond the CLI/spec change. The actual profile and shared skill did not change
after native-kit freeze. The
[final-kit replay script](20261111/final-kit-replay.py.txt) has now run against
both actual consumer roots; its local proof remains distinct from native loading.

## Native results and retained corrections

Both native caller/specialist operations now have passing bounded grades:
[Codex grade 04](20261111/codex01/grade-04.json) is **50/50** and
[Claude recovery grade 04](20261111/claude01-resume01/grade-04.json) is **51/51**.
Each includes **406 nested actual-renderer pixel/clock assertions**, within its
outcome rather than added to the grade total. The earlier 233 figure described
preflight coverage; it is not the final renderer count. The actual capture scope
still has the 1× live-playback limit above and does not include continuous video
or new provider art.

Codex's original [grade 01](20261111/codex01/grade-01.json) failed 0/1 because its
plan-shape assumption raised `KeyError: 'stages'`. [Grade 02](20261111/codex01/grade-02.json)
reported 44/50 because the grader did not replay native file-change update events.
[Grade 03](20261111/codex01/grade-03.json) first passed 50/50; grade 04 preserves
that result with the final evidence reader. Exact
[grade-01 source](20261111/codex01/grading-sources/grade-01/grade_integration_change.py.txt),
[grade-02 source](20261111/codex01/grading-sources/grade-02/grade_integration_change.py.txt),
[grade-03 source](20261111/codex01/grading-sources/grade-03/grade_integration_change.py.txt)
and [grade-04 source](20261111/codex01/grading-sources/grade-04/grade_integration_change.py.txt)
remain alongside their grades. These grader defects remain separate from recorded
native corrections; no failed receipt is rewritten as a pass.

Claude's original specialist completed an accepted package and handoff, but the
outer harness reached its 1,200-second timeout before the final caller report.
The retained [original grade 01](20261111/claude01/grade-01.json) is **0/1**, for
missing caller evidence. It does not classify the specialist's art as failed.
Its [exact grading source](20261111/claude01/grading-sources/grade-01/grade_integration_change.py.txt)
remains retained with that original attempt.
The [original continuation](20261111/claude01/continuation.json) identifies parent
`9402a4fc-0e43-454b-8dfc-f8cdd660a071` and completed child `a9621eef304b33895`.
The [same-parent recovery](20261111/claude01-resume01/continuation.json) consumed
that completed child's result and completed caller verification. The child was
not resumed across processes; the extra check in the 51/51 grade establishes
actual parent-session continuity.

The resumed [grade 02](20261111/claude01-resume01/grade-02.json) failed 0/1 on an
incorrect raw-capture location assumption. [Grade 03](20261111/claude01-resume01/grade-03.json)
reported 44/51 because its reader did not handle the recorded finite Bash loop,
line continuations and reference-metadata equality correctly. The final reader
preserves individual operation exits and dataflow audits; its corrected result
is grade 04. The exact
[grade-02 source](20261111/claude01-resume01/grading-sources/grade-02/grade_integration_change.py.txt),
[grade-03 source](20261111/claude01-resume01/grading-sources/grade-03/grade_integration_change.py.txt)
and [grade-04 source](20261111/claude01-resume01/grading-sources/grade-04/grade_integration_change.py.txt)
remain retained with the failed grades and original attempt.

The proof distinguishes three observation routes:

- Direct native MCP/tool responses and returned bytes supply direct operation
  observations where recorded.
- Codex helper-based observations use audited helper source, reconstructed file
  writes and recorded patches alongside independent retained results/state.
- Claude's CLI observations identify the literal executable, operation and output,
  each individual operation's exit, no recorded later rewrite, and independent
  checks of retained state/results. Dynamic non-output arguments such as `$ROOT`,
  `$REQ` and `$EXP` are not evaluated by the reader. This limited transcript audit
  does not attest arbitrary shell execution or resolve every shell argument.

These routes do not substitute command text or model assertions for independent
artifact checks, and they do not independently judge artistic quality. Native
completion qualifies this controlled changed-requirement reuse assignment; M1/M2,
broader M3 and general host reliability remain open.

## Full verification and final-package status

The [first full verifier](../verification-runs/20261111T213830.574343Z/result.json)
failed with **842 passes, one failure and one Windows privilege skip** across
844 discovered tests. Its renderer expectation still listed five runner files;
adding `observation.py` made the actual set six. That expectation was corrected,
and the focused eight-test renderer retest passed. The failed receipt and its
previous-byte archive remain retained.

The [final full verifier](../verification-runs/20261111T220620.742582Z/result.json)
passes **848 tests plus one Windows symlink-privilege skip**: 849 tests discovered
and run, with no failures or errors. It also passes **39 reference checks** and
fresh wheel/copied-plugin checks, including destination import through both
installed routes. This is the full suite total, not newly added test coverage;
focused and nested checks are not added to it.

The final bundle-manifest SHA-256 is
`89d6144b34a20dfac85c8017b9cd20ace663cc8368d92f1190027ea9fbf61dab`, with **186
files verified**. Local final-kit replays pass **nine checks each** in the actual
[Codex consumer](20261111/codex01/final-kit-replay/consumer-output/replay-result.json)
and [Claude consumer](20261111/claude01/final-kit-replay/consumer-output/replay-result.json).
Each resolves the cwd-relative CLI state path, recreates the exact native
observation ZIP, and leaves every `.pixl` file and the native installed kit
unchanged. A deliberately altered served-member hash produces a real
`destination_binding` refusal, creates no output and preserves state. The
[Codex replay retention](20261111/codex01/final-kit-replay/retention.json) and
[Claude replay retention](20261111/claude01/final-kit-replay/retention.json) retain
all local replay files and identities.

These are local compatibility proofs against the final kit. They are not new
native/model loading, renderer execution, visual inspection or acceptance. The
native outcomes still name their frozen kit; regenerated reference resources do
not retroactively change which package those hosts loaded.

## Required A–E review

**A — How does this improve the operation?** The completed slice connects an ordinary
source change to guarded revision, useful reuse, destination evidence and caller
delivery. Delivery-only authoring removes unnecessary low-level family wiring;
NF-06 now retains a runner's exact declared observations for ordinary review.
Both hosts now supply scoped complete outcomes, with passing full verification
and separate final-bundle compatibility checks.

**B — What is qualified in Claude and Codex?** Existing
[readiness outcomes](../readiness/README.md) and
[CF-06 native outcomes](../plar-coverage/README.md) remain scoped to their recorded
assignments. Authenticated Claude readiness follow-ups passed after the historical
authentication failures; those old failures remain retained. This increment adds
scoped 50/50 Codex and 51/51 Claude outcomes. Claude's parent resumed across
processes to consume the already completed child; this does not qualify child
resumption across processes. The separate
[incomplete Claude caller-result trial](../caller-result/README.md) remains open.

**C — What does this establish about contextual or artistic quality?** Both native
records include fresh explicit review of the reused sheet and delivered package
under the revised requirements, with source authority and provenance retained.
The independent grades check source, calls, bytes, rendered pixels and clocks;
they do not independently judge artistic quality. Structured imports do not grant
acceptance, and no new generation quality is claimed.

**D — Does it work in another repository?** The assigned proof uses copies of the
existing real consumer project through public PLAR and review operations, then
both actual renderer variants. Local tests qualify the delivery adapter and
structured importer within their exercised scope. Both hosts now have
independently graded connected-consumer and parent-consumption evidence, with
Claude's original timeout and recovery preserved. Separate final-kit replays
qualify local compatibility in those same consumer roots. The fresh prospective
store boundary above remains part of the result; historical producer-state
recovery is not claimed.

**E — Where do responsibilities belong?** The caller owns the changed requirement
and handoff scope; the specialist traces sources, chooses reuse and makes explicit
reviews. Public runtime operations enforce identities, pending work and lifecycle
rules. The project runner supplies measured destination observations; NF-06
retains them without granting acceptance. Official PixelLab remains the provider
for newly authorized generation/editing, which this reuse assignment does not
require.

## Continuation

The bounded CF-07/NF-06 slice is complete. Continue with **TM-07 reusable isolated
consumer execution**, then NF-08 lineage and CF-10 in the existing backlog order.
The 1× live-playback and continuous-video gaps, broader PX-PLAR coverage, native
production/quality and M1/M2/broader M3 exits remain open. Preserve every failed
attempt, grade and verifier receipt with its exact source identity. Keep
[TODO](../../TODO.md), [SHELVED](../../SHELVED.md), [PLAN](../../PLAN.md) and the
[current audit context](../../docs/IDENTIFIED.md) aligned while continuing this
cycle without another full IDENTIFY.
