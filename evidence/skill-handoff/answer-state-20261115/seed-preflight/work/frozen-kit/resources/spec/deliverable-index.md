# Consumer deliverable index, version 1

The consumer view of `family` is a read-only projection over existing PX2 family
manifests, saved review and source records. It gives an integrating caller named
files and their declared use without requiring it to decode internal state.
It adds no UDL fields, ledger entries, provider execution or automatic acceptance.
The immutable [family manifest contract](family-delivery.md) remains version 1;
the index has its own `schema: "pixl.deliverable-index/1"`.

## Read and export one package

```text
family STATE OUTPUT --view consumer --root ROOT --result-path FRESH_INDEX_JSON
family STATE OUTPUT --view consumer --candidate CANDIDATE --root ROOT
```

MCP uses `pixl_family` with `path`, `output`, `view: "consumer"`, optional
`candidate`, and optional `result_path`. CLI `--result-path` and MCP `result_path`
use the existing exact JSON export to a fresh consumer-relative path. Open that
saved file before relying on its full contents. Exporting the result writes only
the requested result file; the family read changes no production state.

`output` is required for this view. Without an explicit candidate, selection is
the family's current nominee, never the most recent retained snapshot. No nominee
returns `package: null`, `assets: []`, `current_eligible: false` and unresolved
conditions. An explicit candidate must be a retained snapshot of this family;
its current nomination, review and drift are still reported. `candidate` is invalid
with the default `view: "complete"`; that complete family report keeps its existing
behavior, optional output filter and history.

The producer reads under its explicit project root and verifies retained package
and local source identities. Missing, redirected or changed required bytes fail
under the existing rooted checks. This does not check a separately installed
destination or make a network request.

## Index fields

| Field | Meaning |
| --- | --- |
| `schema`, `view`, `format` | `pixl.deliverable-index/1`, `consumer`, and the source document format `2`. |
| `revision`, `hash`, `state` | Observed source revision, canonical state hash and project-relative state locator. |
| `family` | Output ID/name, selected and current candidates, task/state, nomination, exact current requirements, destinations and `current_eligible`. |
| `package` | Selected manifest candidate, package directory and manifest paths, manifest SHA-256, creation time, preceding state hash, immutable `creation_acceptance` and current `stale` reasons; null when unselected. |
| `assets` | Ordered members from that exact manifest, with names, byte identities, contract, metadata, review and lineage as detailed below. |
| `integration` | Declared destination/member-contract choices and their directly cited source locators; no inferred layout or execution. |
| `unresolved` | Structured `code`, `subject`, `detail` entries for observed blocking conditions. |
| `pending_jobs`, `selection_bindings` | Current pending work and relevant retained PLAR selection bindings. |
| `files_verified` | Existing rooted file checks ran; it does not assert a destination import, remote-source retrieval or acceptance. |
| `history` | State/manifest locators and exact `pixl_family` arguments for the complete report. |
| `refresh` | Exact `pixl_family` arguments for a fresh consumer view, preserving an explicit candidate selection when supplied. |
| `scope` | Explicit path, metadata, review and acceptance boundaries. |

All paths are project-relative except each asset's `package_path`, which is
relative to the immutable package directory. An asset's `source_path` is its
recorded source location, not evidence that a destination import occurred.
The saved index is an observation at its state hash; it does not update itself.

## Named assets and declared integration

Each asset includes `output`, `output_name`, `candidate`, `name`, `kind`, retained
`path`, `package_path`, original `source_path`, `sha256`, `bytes` and the frozen
candidate `record_sha256`. It preserves manifest member order.

The output's current name is accompanied by `output_record_sha256`,
`saved_output_record_sha256` and `output_current_binding`. The family has the
corresponding `record_sha256`, `saved_record_sha256` and `current_binding` fields.
These identify current F declarations against the immutable snapshot; a renamed
or amended output is not presented as a reconstructed historical declaration.

`contract` is null when absent, otherwise it identifies the C record and its
`declared` fields. `record_sha256`, `saved_record_sha256` and `current_binding`
distinguish the current declaration from the snapshot's saved binding. This is not
an invented historical reconstruction of a changed contract.

`metadata` contains `basis: "declared_opaque"`, `present`, the saved X.mt `value`
and `layout_status`. Present metadata is `not_interpreted`; absent metadata is
`not_declared`. X.mt has no universal atlas/frame schema. Its presence does not
establish slicing, timing, frame order or pivot facts, and a missing fact is not
inferred from dimensions, kind, filenames or lineage.

`integration.choices` combines current family destinations, saved snapshot
destinations and selected member contracts' `ch` choices. Each row includes its
roles, ID, project, key, status, value, source IDs and rationale, plus current/saved
record hashes and `current_binding`. A current value with a changed binding is
reported as changed; it is not passed off as the frozen value.

`integration.sources` deduplicates the choices' direct S references. Each includes
its URI, declared SHA-256, line bounds, authority and current/saved record binding.
Locally available sources also include resolved project-relative `path`, `bytes`
and `observed_sha256`; status distinguishes `declared_location` from
`retained_revision`. A remote source has null path/bytes/observed digest and
`remote_not_observed` status, with an unresolved source condition. The view does
not fetch it. Source values may identify an authored consumer module containing
project-specific layout or timing; the index neither interprets nor runs it.

Each asset's `review` identifies current nomination, producer task state and exact
criterion statuses. `lineage` reuses the bounded existing projection of retained
imports, byte equivalence and workflow context. It does not authenticate remote
execution or turn task inputs into pixel ancestry. Follow the full history
locators when more evidence is needed.

## Creation, current review and unresolved work

`package.creation_acceptance.accepted` remains false because retaining a manifest
did not accept it. Its `source_status_pointer` points into the immutable manifest.
Subsequent verdicts, nominations and completion appear in the current review;
they never rewrite that creation status.

`family.current_eligible` requires a selected package and no observed unresolved
conditions: current nomination, completed relevant tasks, passing declared
criteria, current bindings and no pending work or reported drift. This is a
state-scoped eligibility observation. It creates no new judgment and does not
establish undeclared engine, broader artistic or human acceptance.

Unresolved conditions retain nonpassing criteria, missing nomination, incomplete
tasks, family/baseline blockers, pending jobs, stale packages or PLAR selections,
and unavailable cited source bytes. Undeclared layout facts remain explicitly
`not_declared` or opaque `not_interpreted` metadata; callers must resolve any
missing integration facts required by their actual task, even if its saved
criteria already pass.

## Package-only handoff and refresh

Export the full index, then transfer its manifest, retained asset files and every
cited source file needed to interpret the saved integration choices. A locator
alone does not transfer bytes. Preserve the exported relative layout or retain an
explicit copy mapping and verify each transferred file against its named SHA-256
and byte length. Include the exact referenced authored consumer module when its
source defines the requested behavior.

A cold caller can inspect names, files, contracts, choices, cited source content,
review and unresolved conditions from this handoff without opening internal state.
Use the actual declared target and these exact files for integration; do not infer
missing atlas, frame, timing or pivot metadata. Metadata/transfer checks and a
successful import are separate from rendered behavior or acceptance.

Keep the original exported index and package. If producer state changes, request a
new index through `refresh`; use `history` for the complete report and saved state.
An explicit historical candidate remains explicit on refresh. Preserve historical
failures and state the next unresolved action rather than replacing an old package
or interpreting read-time eligibility as new acceptance.
