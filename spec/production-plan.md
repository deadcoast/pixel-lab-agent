# Connected family plans and staged requests

These optional adapters author existing PX2 records. They add no wire fields or
acceptance rules. The specialist chooses the approach, uses applicable knowledge,
compares the caller's requirements, discovers official PixelLab tools and judges
the art. The adapters remove repeated graph wiring and input binding.

See [saved adapter compatibility](adapter-compatibility.md) for plan, snapshot,
request-packet and caller-comparison versions and unsupported-version recovery.

## Author the connected plan

First orient with `context STATE TASK_OR_OUTPUT_OR_PLAN --view authoring --root
ROOT`, or the existing `pixl_context` tool with `view: "authoring"`. This PX2 view
indexes the focused connected plan, enclosing family, current contract/criteria,
direct prerequisites, nominees, choices, sources and relevant jobs. Optional
`--plar PATH --asset ID` (`plar_path`, `asset_id`) adds current selected requirements
and dependency retrieval links. It is read-only, does not expand historical proof
or provider payloads, and reports source drift rather than granting validation or
acceptance. The default complete wire context and its byte-budget behavior are
unchanged. Authoring view rejects a byte budget rather than silently dropping rows.

The authoring view expands choices through declared semantic links from the
selected outputs/contracts, family destinations, inputs/nominees, decisions and
knowledge. It follows transitive authority links without traversing project
ownership or historical proof. Other project intake choices remain in the compact
`choice_scope.other_intake` index with exact complete-context retrieval arguments.
Project rows explicitly omit `in`; full choice values and their source material
are expanded only when linked. Unlinked does not mean irrelevant: inspect an
indexed choice if applicability is uncertain, and preserve caller instructions.
This selection uses no key/text heuristic and does not change saved I statuses.

```text
production-plan STORE PLAN_JSON --expect STATE_HASH --root ROOT
```

MCP: `pixl_production_plan(store, expect, plan)`. The JSON object has:

- `version: 1`, a new `id`, existing `project` P, `actor` A and exact `baseline` X
  from a sample; `decisions` D and `knowledge` K lists retain actual adoption/proof.
- `stages`: each has a distinct `id`, `name`, `phase` (`sample` or `production`),
  raster `kind`, existing `contract` C, `needs` and nonempty `criteria`.
- `needs`: existing F IDs or another stage's short ID. These become direct task
  prerequisites. They are planned outputs, not invented image candidates.
- Each criterion has `id`, exact `check`, `domain`, evidence `mode` and `sources`
  S IDs. Existing evidence-mode rules apply. Source/authority interpretation belongs
  in those retained sources; authoring does not create reviews or confirmations.
- Optional stage `selection`: `path`, `asset`, `requirements_hash` from a current
  PLAR read. Bind each asset once, to its final deliverable stage. The adapter
  retains its requirement/source snapshot, creates the explicit selection input
  and links the resulting task/output to the previously unlinked PLAR row.
- For a reviewed successor, selection may additionally carry `replaces` with the
  exact current `store`, `task` and `output` production link. Use a new plan ID and
  the current expected state hash. The prior link must belong to that asset in
  the same store; every earlier owned generation must have no pending job.
  Resolve an obsolete prepared request through its existing lifecycle first.
  This appends new tasks/criteria and saves the previous allocation in PLAR
  history; it neither rewrites an old intent nor transfers acceptance. Relinking
  rechecks pending work under the store lock and compares the PLAR hash. An
  interrupted publication can recover by repeating the identical plan, but cannot
  overwrite a different current link. Reused bytes may be reviewed as new
  candidates without inventing a provider request or observation.
- `delivery`: `name`, ordered `members` (existing F IDs or stage short IDs),
  `destinations` I IDs and separate collective `criteria`, including continuity.

`stages: []` authors delivery around existing outputs without creating a new
production stage or provider job. For example, deliver an accepted sample as the
family's only member using its existing X as `baseline` and its existing F as the
member:

```json
{
  "version": 1,
  "id": "sample-delivery",
  "project": "project",
  "actor": "artist",
  "baseline": "sample.accepted",
  "decisions": ["method.adopted"],
  "knowledge": ["method"],
  "stages": [],
  "delivery": {
    "name": "Deliver the accepted sample",
    "members": ["sample.output"],
    "destinations": ["destination"],
    "criteria": [{
      "id": "continuity",
      "check": "The delivered sample preserves the reviewed project treatment",
      "domain": "continuity",
      "mode": "visual",
      "sources": ["brief"]
    }]
  }
}
```

These IDs must refer to the project's actual existing records. Delivery still
requires a nonempty family, destination choices and collective criteria. Existing
members must satisfy the same baseline/project rules as a staged plan. The result
has an empty `stages` map and `allocation` list, and retains the plan marker, delivery
task/output and criteria. Identical retries reuse them. Open authoring still allows
an unaccepted baseline; activation, completion and `family-snapshot` retain their
existing eligibility and pending-work checks. Snapshotting an accepted sample as
the sole member records that exact X as both baseline and selected member and
leaves the delivery unaccepted until its separate collective review.

No dimensions, palette, alpha policy, adoption, provider controls or destination
confirmation are inferred. Establish those existing project records through the
normal reviewed operations. Open plans may have outstanding adoption or baseline
acceptance; lifecycle blockers prevent premature execution.

The return value maps stage names to task/output IDs. The adapter writes baseline
links, reciprocal task/output links, direct prerequisites, criteria, family
membership and destination references. It retains the authored plan and bound PLAR
snapshots in a report X and publishes only open work. Its marker binds authored
semantic records and fixed task structure. Later criterion, contract or structural
changes require review and a new plan ID.

State uses expected-hash publication. PLAR linking follows as a separate CAS;
an interruption returns `needs_reconciliation` with the retained plan. Reread state
and repeat the same plan to finish links without duplicate records. Changed plan
content cannot reuse its ID. Existing production links are not replaced: revised
generations retain the explicit revision workflow. Old contracts, jobs, candidates
and verdicts remain intact. Intermediate stages without a `selection` are local
production dependencies, not independently allocated PLAR assets.

Bound plan inputs also carry downstream selection checks through ordinary job
preparation/dispatch and new task activation/completion. A seed's final allocated
asset must still have the saved requirements and link. Unrelated member changes
do not block that seed merely because they share a plan; collective delivery checks
all allocated members. Already submitted jobs and historical acceptance remain
readable for reconciliation. These checks do not invent a second PLAR asset for
each intermediate or relabel a missing allocation link as permission to submit.

## Exact criteria handoff

Both adapters return `request_review`, an argument object for the existing
`pixl_request_review` tool. This adds no UDL fields and changes no saved-state
semantics. For an existing connected plan, use:

```text
request-review STORE/state.px --plan PLAN_X --root ROOT
request-review STORE/state.px --plan PLAN_X --job JOB_ID --root ROOT
request-review STORE/state.px --plan PLAN_X --job JOB_ID --comparison CALLER_JSON --root ROOT
```

The read-only report expands all authored member and collective criteria from the
exact plan snapshot, with Q IDs/hashes, literal conditions, source excerpts,
controls, decisions, actual inputs and the selected job request. Changed criteria,
source records/bytes and selections remain diagnostics. Historical review does not
make an obsolete request executable. Source records marked changed cannot stand
in for missing historical declarations.

`review_scope_sha256` binds the reported semantic scope, excluding absolute source
locations, unrelated state revisions and job lifecycle observations. Current job
state, remote ID and blockers remain visible in the report; progress alone does
not invalidate a comparison of the same intent and request. The optional caller comparison uses
`criterion_comparisons`, each with `criterion`, `record_sha256`, `source_obligation`,
`authority_basis`, `scope`, `literal_delta`, `discriminating_alternative` and
`disposition`. Its top-level `review_scope_sha256` must match. Coverage reports
missing/duplicate/unexpected/stale/incomplete entries; nonempty prose is not proof
of correct interpretation. The tool never sets `consistent:true` or grants
adoption. The shared request-review workflow supplies the independent judgment.

### Concise successor comparison

```text
request-review STORE/state.px --plan CURRENT_PLAN_X --against-plan PRIOR_PLAN_X --view changes --root ROOT --result-path work/changes.json
```

Use the same `pixl_request_review` MCP tool with `view:"changes"` and
`against_plan`. Both plan IDs must be explicit, distinct and in the same project;
the report does not infer direct succession from that choice. It checks immutable
snapshot identities, compares saved criteria/controls/selections and bound
contract/choice identities, shows source drift and retained choices, and lists
saved failures, obsolete verdicts and stale receipts. Output-level review
attention reports what lacks a current passing nominated review; it does not
transfer acceptance or certify artistic quality.

Criteria align only by exact stage ID and local criterion ID. Renames stay
added/removed. `fields` names the changed literal fields; the compact view never
paraphrases or truncates a criterion into a new rule. `criterion_index` preserves
every old/new ID and hash, and `before.retrieve` / `after.retrieve` fetch the exact
full reports with all literal checks and source excerpts. Read those checks before
semantic judgment. Retained plan paths expose original PLAR snapshots; changed
asset fields are reported separately from status/evidence prose. If a bound
historical choice/contract declaration no longer matches the current record, its
old fields remain unavailable, rather than being reconstructed from current text.

`comparison_sha256` identifies this complete current change report, including
state and observation status. It is not the stable `review_scope_sha256` used by
the existing caller-comparison protocol. Default `view:complete`, full report
identity and saved comparison coverage remain unchanged. The changes view and
its full retrievals support direct result-file export. This is an optional view
over existing PX2 semantics, not new wire syntax or an acceptance operation.

## Prepare the next executable stage

Once prerequisite outputs are accepted, review their actual selected bytes and
the next request. Upload or reference those bytes using the official tool's
supported mechanism. A saved X ID or filename in text is not provider input.
Keep provider controls and deterministic editing/assembly decisions explicit.

```text
stage-prepare STORE PLAN_X STAGE_ID JOB_ID PACKET_JSON --expect STATE_HASH --root ROOT
```

MCP: `pixl_stage_prepare(store, expect, plan, stage, job, packet)`.
The packet contains `version:1`, `inputs` and `request`. `inputs` maps each
prerequisite F ID to `{ "candidate": "ACTUAL_X_ID", "sha256": "EXACT_FILE_HASH" }`.
Use the generated or existing F IDs returned by the plan, exactly matching
`needs`. Each candidate must be the nominee of a done prerequisite task and match
its actual retained bytes. An empty map is valid for a stage with no `needs`.

`request` has the normal discovered-request fields: `provider`, `tool`,
`arguments`, `schema`, `discovery`, `authorization`. Use the actual official
connection/schema and the assignment's existing authority. The specialist/caller
still compare argument image handles with the reviewed bytes and reference roles;
these local tools cannot attest that a provider URL contains the claimed image.

Preparation verifies the authored plan is current and the stage can run, retains
the exact packet, attaches real candidate X inputs to the task, then uses the
durable job operation. A crash between those publications is recoverable by
repeating the same packet/job with the new state hash. A matching retry returns
its observed status without dispatch or another job. Unknown stays unknown; a
different pending attempt blocks work. Changed upstream nomination or plan context
requires reconciliation through existing job reports, preserving earlier intent.

Continue dispatch → official host tool → observe → import → inspect →
revise/complete. A new stage is not required for each retry of the same output;
use a distinct job ID after resolving the previous attempt. Retain generated
seed, generated animation, deterministic edits and assembled output with their
actual provenance. A successful request is still an unaccepted candidate.

Use `family` and `family-snapshot` for collective delivery. The manifest's initial
`accepted:false` remains a creation-time fact; current acceptance comes from the
selected candidate, current criteria/verdicts and completed delivery task. Neither
adapter generates art, grants acceptance, changes requirements or promises
exactly-once remote execution. Source, wheel and portable plugin share these APIs.
