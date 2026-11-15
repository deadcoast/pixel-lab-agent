# Selected asset to first candidate request

`plar prepare --root ROOT --asset ID --requirements HASH --packet PACKET_JSON --connection CONNECTION_JSON [--store STORE] [--path plar.txt] [--revise --expect STATE_HASH]`
and `pixl_plar_prepare` prepare the first candidate for a selected PLAR asset.
The normal output is an existing PX2 sample plan plus its first durable provider job.
The operation executes locally and returns the normal job state/next action. It
never calls PixelLab, invents a review, approves a style or marks an asset integrated.
The host submits through its authenticated official PixelLab connection using the
existing dispatch/observe operations and the assignment's existing authorization.

The [adapter compatibility policy](adapter-compatibility.md) records supported
packet, candidate-plan, preparation-marker and focus versions, including legacy
focus absence and explicit unsupported-version recovery.

## Inputs and interpretation

- `asset_id` and `requirements_hash` come from a current focused PLAR read. All
  selected/dependent source bindings must be current; unrelated queue progress
  does not alter the requirements identity.
- `packet` is a project-relative request-review JSON artifact, version 1, with a
  top-level `requirements_hash`. Its source entries include every selected source
  path/hash and role. Its `request` points to the exact `provider_arguments` JSON
  with path/hash/tool. Its `criteria` points to the candidate-plan JSON below.
  Existing choices and independent caller review remain part of the skill's
  handoff; this adapter validates bytes and structure, not the caller's judgment.
- `connection` is a JSON object or project-relative JSON file containing exactly
  `provider`, the actually discovered `schema`, `discovery` and `authorization`.
  These have the existing discovered-request meanings. Arguments and tool come
  from the reviewed packet, avoiding a second hand-authored copy of the payload.
  Credentials belong in the host connection, never these artifacts.
- `store` defaults to `.pixl/assets/ASSET_ID` under the consumer. Existing linked
  work defaults to its linked store. A revised contract requires explicit `revise`
  and the current production `expect` hash; ordinary calls cannot replace it.

Candidate-plan JSON follows [asset-plan.schema.json](../pixl/asset-plan.schema.json):
`version:1`, an explicit candidate `scope`, and `outputs`. Each output has a distinct
`id`, `name`, raster `kind`, concrete `contract`, and nonempty `criteria`.
Contract fields are `size`, `palette`, `view`, `sampling`, `alpha`, `intent`; every
value is explicitly authored from the assignment or a scoped expert choice. An
empty palette means no fixed palette; no dimensions, projection or alpha defaults
are inserted. Criteria have an ID, exact `check`, `domain`, required evidence `mode`,
`basis`, `scope` and source path/locator list. Expert-choice sources can be empty
when their basis is stated honestly. Criterion locators, authority and scope are
retained in the exact plan artifact, not discarded during record construction.
The optional authority and explicit source-line fields, deterministic evidence report
and consumer continuation are specified in [request-review.md](request-review.md).

The adapter creates A/P/S/I/C/T/F/Q records and actual reference X inputs, then
uses the existing durable-job preparation. It adds no registry fields. Contract
interpretations are explicitly proposed for the first candidate; they do not
promote an observation or expert choice into owner approval. The original PLAR
requirements keep their authority in the bound selection snapshot. Sample means
candidate work before artistic acceptance; it is not a provider spending policy.
Production adoption and family/delivery plans retain their existing operations.
The specialist still determines whether dependency work supports this action;
PLAR status labels are not proof of acceptance.

## Identity, publication and recovery

Exact source, reference, packet, argument and candidate-plan bytes are retained under
the asset store and bound into the plan, together with an immutable selection/
connection snapshot. The snapshot maps original paths/hashes to retained paths.
Later source edits cannot rewrite what the earlier request consumed. Snapshot identity excludes mutable
PLAR status, next action, evidence links, production links and absolute installation
paths. Updates to those queue fields, source-table reordering or relocation do not
invalidate the same plan. New snapshots canonicalize the source table; matching
older snapshots are reused through their explicit selection inputs without rewriting
retained identities, records or jobs.
Changing relevant requirements, sources, arguments or criteria requires a new
comparison and an explicit revision. The adapter never overwrites the old plan.

Validation of supplied schema/authorization assertions occurs before publication;
new discovery timestamps cannot be in the future. Invalid plan semantics are
checked before retaining a new plan snapshot. The plan is saved before the intent,
so a storage interruption may leave a valid plan with no job. An unchanged retry
prepares that missing intent, or returns the existing job without another revision.
Reuse requires both the exact request and the complete task/output bindings to match;
a same-named job with different arguments or output membership is rejected.
A dispatched unknown job remains unknown and requires reconciliation; retrying this
operation does not dispatch or create a second job. Normal writer locks and CAS
checks apply. This is not a cross-file all-or-nothing transaction; interruption can
leave unreferenced immutable plan files. Preserve them rather than fabricate progress.

The task includes a report-X input with explicit `mt.binding: pixl.plar.selection/1`
and `plar_path`, `asset_id`, `requirements_hash`. This opts that plan into current
selection checks; other X metadata and existing plans keep their previous semantics.
New job preparation and dispatch, including generic commit publication, compare the
current focused PLAR identity with that retained binding. Changed/missing/unreadable
selections prevent a new dispatch. Reports expose `selection_bindings` separately
from journal state. Already-submitted work can still be inspected, reconciled and
imported against its original saved plan; current-source changes do not erase remote
history or prove fitness for the changed consumer. Read and compare the new selection
before revising or adopting further work. No new PIXL record field is introduced.

Results include store/state/hash/revision, task/output IDs, current job, requirements
identity, packet identity, already_prepared and explicit absence of new acceptance
or remote execution. Link appropriate store/task/output IDs in PLAR and update its
status/next action against actual progress. Preparation is not completed production.
After submission continue the existing retrieval, candidate review, revision and
completion operations; failed candidates and unavailable required checks remain.

## Allocation and revised work

Focused PLAR reads return a compact `production` view: linked/discovered/missing
state, current selection, planned outputs and acceptance results, retained provider
identities, pending jobs and the next operation. This is derived from actual PX2
state, not the editable allocation status. Missing or corrupt production leaves
requirements readable with an explicit diagnostic. The default owned store can be
discovered after an interrupted allocation link; custom stores require their link
or the explicit store argument. Reports never search arbitrary directories. `new_request_allowed` is a local
selection/pending-work advisory, not authorization or a substitute for preparation
validation of the exact request and connection.

For one-output preparation, the operation CAS-links store/task/output, sets
`in_progress` and appends the immutable plan snapshot as evidence. Unrelated rows,
requirements, existing evidence and previous PLAR bytes remain unchanged. If a
concurrent allocation edit wins, the prepared job remains retained and the result
reports `allocation.status: needs_reconciliation`; reread and link it instead of
starting another request. Unchanged matching links are left byte-identical. A
multi-output plan returns `needs_output_link` for an explicit delivery-output choice.
It separately retains the explicitly prepared task in the asset store's versioned
`preparation-focus.json`. A focused read can resume that task before a collective
delivery output exists; it never substitutes an arbitrary member for delivery.
An existing explicit PLAR delivery link remains authoritative.
This linking step does not create a destination file or certify integration.

`revise: true` with `expect` appends a new candidate task/output/criteria/choice/input
generation in the **same store and project**, under IDs derived from the exact
reviewed input identity. Every old task, candidate, verdict and journal remains.
Project source/choice membership grows to include the new generation; no acceptance
is copied. The single-output allocation link advances only after its job is prepared.
A new plan can be retained before its job or allocation link; an unchanged explicit
retry with the current state hash resumes that generation, not another one.

Preparation focus is confined metadata, not a new PLAR field or PX2 record. It
binds the PLAR path, asset and retained requirements to the exact immutable
preparation marker (path, file hash and input fingerprint), its task and durable
job. Publication uses the store lock, a fresh state compare-and-swap and current
source requirements, after the job/context has been verified. Job observations
may advance state without invalidating an unchanged focus. Identical retries
leave focus bytes unchanged. A malformed or mismatched focus is an explicit
reconciliation diagnostic; no timestamp, lexical ID or old task status chooses
its replacement. A direct older preparation is not currently selected merely
because its source requirements match; existing dispatch/completion guards retain
that distinction. Connected family stages keep their separate selection semantics.

For an existing generation, repairing missing focus or deliberately selecting a
prepared generation requires explicit `revise` and the current `expect`, with the
exact target job still prepared and all other owned pending work resolved. This
also supports a legacy multi-output store after an interrupted publication. A
terminal historical retry cannot reclaim focus. An absent sidecar retains legacy
unique-task discovery; multiple unlinked tasks stay ambiguous until explicit
recovery. Older runtimes ignore this separate metadata and retain their original
ambiguity; PLAR version 1 and PX2 wire semantics are unchanged.

Before revision, resolve every pending attempt bound to this PLAR asset. A provider
change, new task ID or new output ID does not bypass that rule. Low-level prepare
and generic job publication enforce it too for tagged selections. Prepared work
may be explicitly withdrawn with the existing evidenced failed observation; unknown
or submitted work requires actual evidence from its originating connection. The
adapter never fabricates cancellation or retires a job merely to make a new plan fit.

Old inputs and outputs stay readable after consumer changes. New dispatch and
activation/completion require current selected requirements; completion also checks
that the task is still the allocation's selected generation. Historical done state
remains a statement about its original plan, not acceptance for the changed consumer.
Existing untagged PX2 work keeps its original semantics. No new registry or journal
fields are introduced.
