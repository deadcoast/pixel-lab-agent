# Family delivery manifest contract, version 1

This is the local file contract for registry 2.2.0 family candidates in [PIXL/2](PIXL-2.md). It does not describe a remote service or an artistic judgment. Existing PX1/PX2 documents without the explicit family fields retain their prior interpretation.

## Canonical shape

The manifest is UTF-8 JSON with sorted keys, compact separators, unescaped Unicode and one final LF. Duplicate keys/noncanonical serialization are rejected through exact canonical byte comparison. Maximum encoded size is 16 MiB, JSON nesting 64, all numbers finite. Its SHA-256 is both the X.dg and containing directory name. Exact top-level keys:

| Field | Meaning |
| --- | --- |
| version | Integer 1 |
| output, candidate | Owning family F ID and this manifest X ID |
| source_state_sha256 | Canonical digest of the immediately preceding saved state |
| created_at | ISO timestamp with explicit UTC offset, at most six fractional digits |
| plan | Frozen planning identity and semantic bindings described below |
| baseline | Exact `candidate` ID and canonical `record_sha256` of the baseline X |
| files | Ordered frozen member entries described below |
| acceptance | Exactly `accepted: false` and `source_status`, the pre-snapshot family report |
| limits | Exactly `retention_only: true`, `remote_executed: false`, `automatic_acceptance: false` |

Plan has exactly output, task, baseline, members, destinations and bindings. The first three are record IDs. Members is the saved distinct ordered F list, destinations the saved distinct I list, and bindings maps each ID in the full semantic scope of the family F to its canonical record SHA-256. P/T/E/V/J/N are excluded under existing proof rules. The map includes baseline X, member F plans, destinations and their semantic dependencies. Current task states and actual V/E outcomes remain in source_status and the preceding state history, not in that hash closure.

Each files entry has exactly output, candidate, source_path, path, sha256, bytes and record_sha256. Output is the corresponding saved member F; candidate is its exact selected X. source_path is that X's project-relative path. path is `files/0000<suffix>` (zero-based member index, four digits). The original final suffix is retained when it matches a dot followed by 1–16 ASCII alphanumeric characters; otherwise use `.bin`. sha256 and bytes identify the exact copied bytes; record_sha256 binds the source X's full canonical fields. Maximum 1024 members, 256 MiB each, 512 MiB in total.

The family X is report kind with of=output and xs=[baseline, each files candidate in order]. It has no raster contract. The baseline may also occur in files. Candidate/record references are typed in X.xs and are checked against the manifest; JSON IDs alone do not supply graph context.

## Files and publication

The store is a proper subdirectory of the explicit project root. A snapshot resides at `STORE/deliveries/<manifest-sha256>/manifest.json`, with the numbered member files in its `files/` directory. Source files are not moved or rewritten. All resolved paths remain in their declared directories; redirected manifest/member locations and different existing immutable bytes fail. Every rooted validation checks actual retained copies and source identities.

Publication requires an existing saved PX2 family plan. The new manifest must exactly describe the immediately preceding canonical state, its current accepted baseline/member selection and report; its plan must remain unchanged in the candidate state. Both prior and candidate state must satisfy snapshot readiness. Generic commit enforces these requirements and store paths, just as the snapshot helper does. An initialized store cannot invent prior snapshot history. An existing X cannot acquire xs retroactively.

The snapshot helper and generic snapshot publication add only one new X, with existing records unchanged. No E/V, task state, nomination, approval or provider event is created. Retain the candidate first, then inspect and record the result separately; other intentional edits use another revision. All mutations use expected-hash compare-and-swap. Stale/failed publication never publishes a candidate; unreferenced immutable files may remain and are not an accepted delivery. state.px is the publication authority.

Published manifest X and every X named by its xs are immutable. A revision adds new X IDs, preserving original source and copied bytes. Existing family plans cannot shed bs/mb/ds, and old manifest candidates cannot shed xs. Intentional membership/destination/criteria changes are explicit plan revisions, with completed-task reopening and E/V supersession where applicable.

## Historical existence versus current acceptance

Old packages are checked against their saved members and typed constituents, so changing current F.mb does not erase or make old packages structurally invalid. Reports compare saved semantic bindings and selection to the current plan and report drift. A current pass/fail family V requires both current selection and saved semantic planning identity to match its candidate. Otherwise supersede that verdict, preserve the old candidate and reopen affected work. An unavailable V remains a retained account of why inspection was not performed.

Family reports require a project root and include pending jobs for baseline/member/delivery tasks. Unrooted graph validation can check typed structure and current selection, but cannot read frozen manifest bindings or copied bytes; it does not establish current package validity. Store publication and family reports require rooted checks. Pending prepared/submitted/running/unknown work prevents a fresh snapshot and is routed through the provider recovery skill. A family that lacks confirmed destination or applicable adoption may still retain useful local accepted-member bytes; it cannot use that retention to activate or complete delivery. Continuity inspection, engine execution and human artistic approval remain actual obligations supplied by the task's declared Q and real observations.

## Visible asset lineage

Rooted `family` reports derive `lineage` beside each currently selected member and
beside each historical snapshot file. `review-context` exposes the same projection
for its candidate and delivered members. PLAR delivery status carries nominated
candidate lineage and the nominated family snapshot's members into fresh handoffs.
When PLAR links the family output itself to a directory, delivery observation checks
every distinct manifest `source_path` beneath that directory against its retained
member size and SHA-256. It does not infer destination names, count unrelated files
as members, or treat the manifest digest as a directory digest. The nominated
snapshot must still match the current accepted family, its selections and pending
work; these read-time file checks create no acceptance or new saved-state fields.
These are read-time views of existing artifact and durable-job identities, not new
PX2 fields or changes to the immutable manifest contract above. Historical reports
and handoffs keep their original bytes; read current state for a fresh projection.

A retained import binds an exact candidate record to its journal event. The saved
request and caller-supplied observations describe what was requested or reported;
local hash and history validation does not authenticate remote execution. A tool
name, success state, provider ID, style baseline, task input or equal file hash alone
does not establish pixel ancestry. Family `X.xs` remains a constituent list. Where
an exact relationship is absent, ambiguous or unavailable, lineage must preserve
that limit rather than invent an origin. Equal bytes can support byte-equivalence
without establishing which copy was the source.

The derived view identifies its `candidate` and `sha256`. `artifact.jobs` names
its direct importing jobs; `jobs` contains bounded supporting job details and their
recorded `source_requests`. `same_bytes` lists equivalences; `workflow_inputs`
retains task context. `provenance_status` distinguishes a retained import, equality
to recorded imported bytes, and an unrecorded origin;
`remote_verified` stays false. Request operation labels describe saved intent,
not successful artistic outcomes. Explicit simulation evidence remains visible.
Nested source requests are bounded and unresolved references retain their locator.
The exact retained journal is the source for omitted details. Workflow inputs and
equal-byte candidates are context, not inferred directed ancestry.

Lineage is independent of acceptance. It creates no job, artifact, review, verdict,
nomination or completion. Derived relationships do not convert a controlled fixture
into real generation or a deterministic correction into a successful generative
animation. Larger caller results use the existing exact delivery/resume locators;
they must not silently omit lineage to fit the inline budget.
