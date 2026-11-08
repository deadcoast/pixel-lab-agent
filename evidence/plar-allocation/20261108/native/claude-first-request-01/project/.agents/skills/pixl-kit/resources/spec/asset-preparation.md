# Selected asset to first candidate request

`plar prepare --root ROOT --asset ID --requirements HASH --packet PACKET_JSON --connection CONNECTION_JSON [--store STORE] [--path plar.txt]`
and `pixl_plar_prepare` prepare the first candidate for a selected PLAR asset.
The normal output is an existing PX2 sample plan plus its first durable provider job.
The operation executes locally and returns the normal job state/next action. It
never calls PixelLab, invents a review, approves a style or marks an asset integrated.
The host submits through its authenticated official PixelLab connection using the
existing dispatch/observe operations and the assignment's existing authorization.

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
  work must be resumed in its own store. This is a first-plan adapter; it does not
  replace another plan or amend an existing candidate contract implicitly.

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
paths. Updates to those queue fields or relocation do not invalidate the same plan.
Changing relevant requirements, sources, arguments or criteria requires a new
comparison and explicit existing-plan revision; this adapter refuses to overwrite.

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
