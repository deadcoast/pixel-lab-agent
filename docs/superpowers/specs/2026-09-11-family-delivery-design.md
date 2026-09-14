# Approved sample through family delivery

The next existing target is stage 4 in `docs/PROJECT-REVIEW.md`: an approved representative sample supports a coherent family and usable delivery. This design develops the local operation and the PIXL skill. The repository developer does not become PIXL. No project style, provider, engine or actual acceptance is invented.

## Source gap and chosen approach

Current PX2 has planned F, materialized X, candidate Q/V acceptance, task prerequisites and durable provider attempts. However, T.ip is excluded from semantic proof traversal. Merely placing a baseline or sibling in task inputs does not bind a continuity verdict to those actual records. There is also no explicit family membership, destination plan or retained delivery operation.

A prompt-only family procedure would leave that proof gap. A separate family/workspace framework would duplicate existing task/output/acceptance semantics. Extend F and X explicitly in registry 2.2.0 instead, preserving every PX1 and legacy PX2 document. Existing closed readers reject the new fields rather than misinterpreting them.

## Versioned fields and semantics

- Optional `F.bs: ref:X` is the exact representative sample candidate used as a production/delivery baseline. It participates in semantic proof. Its X must have an F owned by a same-project sample T. The consuming T must list that X in ip and the sample T directly in dp. Only production/delivery outputs use bs. A task cannot depend on its own sample. Planning can retain an unaccepted or subsequently superseded baseline; activation and completion require that candidate still nominated and its sample task done.
- Optional `F.mb: refs:F` and `F.ds: refs:I` together opt a report-kind F into the family delivery operation and require bs. mb is a nonempty, distinct, ordered list of actual planned family members. ds is a nonempty, distinct list of destination choices owned by the delivery task's project. The family output's task phase is delivery. Nested/self family membership is rejected. Every member belongs to that project and its producer must be a direct task prerequisite. The baseline's own sample output can be a member. Other members are production outputs with that same bs. At least one required Q has continuity domain; its mode and observable condition come from the actual project. Engine criteria are declared when applicable, not inferred from a target name.
- Optional `X.xs: refs:X` identifies a family manifest candidate's exact constituents: baseline first, followed by one selected candidate per member in saved mb order. The baseline can also appear as a delivered member. Only family report candidates use xs. Rooted validation verifies the retained manifest's frozen membership and this projection; it does not reinterpret historical snapshots as the current selection.

Destination unresolved/conflict/proposed/observed choices block delivery activation/completion until confirmed. They do not prevent retaining useful local files. Existing adoption decisions, confirmed output style, applicable proofs, Q/V requirements and expected-hash publication continue to apply. A copied bundle does not grant a task state change, nomination, criterion verdict or provider dispatch.

## Pure planning API

New `pixl/families.py` owns structural checks and selection/readiness interpretation, without file I/O or state mutation:

```python
validate(doc) -> None
blockers(doc, task_id) -> list[str]
plan(doc, output_id) -> dict
selection(doc, output_id) -> list[str | None]
snapshot_blockers(doc, output_id) -> list[str]
describe(doc, output_id) -> dict
```

`plan` returns exactly output/task/baseline/members/destinations/bindings, with IDs, ordered member/destination IDs and sorted record-hash bindings for the F's full semantic scope. `selection` returns the nominated X for each planned member, or null. `snapshot_blockers` requires the family task open/active, eligible baseline, all members nominated on done tasks, and no pending prepared/unknown/submitted/running J for baseline/member/family tasks. It intentionally does not require family verdicts, an adoption decision or confirmed destination: copying retained accepted member bytes is useful while delivery acceptance remains open. `describe` returns output, task, baseline eligibility/reasons, destinations, member candidates and their Q/V outcomes, current family nominee/requirements, blockers and pending job IDs/states. Reports are observations, never state transitions.

`families.validate` runs after shared schema checks and before lifecycle checks. Lifecycle activation adds `families.blockers` so direct commit, ready, workflow and provider dispatch enforce the same baseline/destination rules. Existing documents without these fields have identical interpretation.

## Retained delivery snapshot

New `pixl/delivery.py` supplies:

```python
snapshot(folder, expected, output_id, candidate_id, root=None) -> dict
report(doc, root, output_id=None) -> dict
validate(doc, root=None) -> None
transitions(current, candidate, root, folder) -> None
```

The snapshot reads a rooted valid saved plan, checks expected state and snapshot blockers, and captures each selected member's actual bytes (maximum 256 MiB per file, 512 MiB total, 1024 members). Each read must hash to its X. It writes a content-addressed directory `STORE/deliveries/<manifest-sha256>/` with canonical `manifest.json` and exact member copies under stable numbered paths. Original files remain untouched. A new X references the manifest and its typed constituents. Commit publishes one new candidate and no E/V/nomination/task changes. The result includes normal store publication fields, output/candidate, package path and explicit `accepted: false`, `remote_executed: false`.

Version-1 manifest is closed canonical UTF-8 JSON (sorted keys, compact separators, LF) with version, output, candidate, source_state_sha256, created_at, plan, baseline, files, acceptance, limits. Plan is the exact frozen planning API result. Baseline is its ID and canonical record hash. Each file has output, candidate, source_path, path, sha256, bytes and record_sha256. Paths are `files/0000<safe suffix>` in member order; unsupported suffixes use `.bin`. Acceptance snapshots the described baseline/member/destination/requirements state before creation and explicitly records that package retention is not acceptance. The schema validates bounded JSON, exact projections, hashes, unique numbered member paths and aware timestamps. Supplied acceptance annotations are retained descriptions, not new verdicts.

Rooted validation checks manifest bytes, frozen plan shape, X.xs, the source X's identity, all copied file identities and directory confinement. The manifest candidate and all of its baseline/member X records are immutable after publication. Generic publication enforces the same store content-addressed paths, saved unchanged plan, source revision, eligible current selection, new candidate ID and exact expected manifest content as the helper. Initialization cannot fabricate earlier snapshots. Existing family plans cannot shed bs/mb/ds and published manifest X cannot shed xs. Failed publication may leave unreferenced immutable blobs; only state.px publishes a candidate.

## Historical snapshots and current acceptance

Plan or member selection changes retain old X, files and frozen manifest. Reports list changed semantic bindings, baseline or member selection differences. Existing snapshot validation uses its saved membership rather than the current F.mb. A current pass/fail V for a family candidate requires its plan bindings and constituents still match current planning/selection; otherwise supersede that V and reopen affected work. An unavailable V remains an honest retained boundary. General immutable E/V and done-task change-impact rules still apply. Per-member evidence binds its baseline; family evidence binds the actual manifest, every selected member, baseline, destinations and criteria.

The current family report includes pending provider jobs for all member/baseline/delivery tasks, even though those jobs may not appear in a plain forward context packet. Unknown work directs the skill to the existing recovery operation. A cold session checks family report, workflow and retained job history before creating work or a fresh snapshot.

## Adapters and skill

CLI: `family STATE [OUTPUT] --root ROOT` is read-only. `family-snapshot STORE OUTPUT CANDIDATE --expect HASH [--root ROOT]` mutates local storage. MCP: `pixl_family {path, output?}` and `pixl_family_snapshot {store, output_id, candidate_id, expect}`; root is the server project root, the latter is not read-only, both have no open-world effects. No extra dependency.

The skill links approved sample evidence and applicable adoption, plans members without invented files, declares collective criteria before results, inspects animation playback/frame contacts or tile repeated/neighborhood contexts as the actual task requires, records continuity failures independently, snapshots accepted member bytes, and leaves unavailable destination checks with a concrete handoff. It distinguishes a useful package from a fully accepted delivery. Native-scale/zoom, direction mapping, pivot/timing and tile neighborhood are project-specific inspection questions, not new automatic artistic verdicts.

## Verification and limits

Before regeneration archive current provider milestone receipts, PX2 spec/registry and bundle manifest. Tests first demonstrate missing semantic baseline/family fields and missing snapshot operations. Exercise current versus rejected/replaced baselines, missing/foreign/nested members and destinations, exact collective proof, missing/unavailable engine checks, unchanged old snapshots after membership amendment, selection drift, stale writes, actual corrupted copies and generic commit bypasses. Actual CLI/MCP processes and relocated plugin/wheel operations exercise the same public path. Independently review the implementation and run one recorded fictional skill scenario with retained instructions, bytes, errors and cold resume.

No real provider, engine or production art is available by inference from this repository. Synthetic visual/live receipts test recording rules only. This milestone completes the local family/delivery operation; actual animation/tile artistic quality, engine readiness and repeated cross-host behavior require subsequent real evidence.
