# Saved adapter and schema compatibility

Saved JSON and adapter metadata have their own contracts. Their versions are
independent of the kit version, the PLAR format and the `PIXL/1` or `PIXL/2` wire
header. Installing a newer kit does not rewrite saved files, move acceptance to a
new candidate or turn an earlier receipt into evidence about the newer runtime.

This policy covers the authored plans, review inputs and persisted preparation
metadata used by the core production routes below. It is not a promise that every
historical kit, host or external tool is interchangeable. The current supported
contracts remain version 1; no format migration is introduced here.

## Supported inputs and retained metadata

The table distinguishes JSON Schema's integer semantics from formats with an
existing strict integer check. Where `1.0` is supported, its numeric value already
belongs to the version-1 contract. Booleans are not version numbers. Writers use
`1`; readers must not rewrite valid historical `1.0` bytes to normalize them.

| Format | Supported version and legacy behavior | Authority |
| --- | --- | --- |
| Connected production-plan JSON | Required numeric `1` or `1.0`; closed authored schema | [Production plan](production-plan.md), `production_plan.SCHEMA` |
| Connected stage-request packet | Required numeric `1` or `1.0`; closed schema with `inputs` and `request` | [Stage preparation](production-plan.md#prepare-the-next-executable-stage), `production_plan.REQUEST_SCHEMA` |
| Retained production-plan snapshot | Required numeric `1` or `1.0`; wrapper contains the authored `plan` and retained `selections`, which may be empty | [Production plan](production-plan.md), `production_plan` snapshot writer/reader |
| Connected-plan report-X binding | Exact `pixl.production.plan/1` token; its scope/task metadata retains the plan guard | [Production plan](production-plan.md), `production_plan` |
| Selected-asset report-X binding | Exact `pixl.plar.selection/1` token; requirements and allocation identity retain their existing meaning | [Asset preparation](asset-preparation.md), `plar.selection_bindings` |
| Candidate-plan JSON | Required numeric `1` or `1.0`; closed candidate-plan schema | [Candidate-plan schema](../pixl/asset-plan.schema.json), [request review](request-review.md) |
| Selected-asset request-review packet | Required integer `1`; `1.0`, booleans and missing version are unsupported | [Request review](request-review.md), `request_review` / `plar_prepare` |
| Connected-plan caller comparison | Absent version remains the legacy version-1 payload; an explicit numeric `1` or `1.0` is supported | [Exact criteria handoff](production-plan.md#exact-criteria-handoff), `production_review` |
| Candidate/family review observation | Required integer `1`; existing closed schema and strict integer check remain | [Candidate review](candidate-review.md), `candidate_review` |
| Retained selected-asset preparation marker | Required numeric `1` or `1.0`; missing version is not a legacy marker | [Asset preparation](asset-preparation.md), `plar_prepare` / `preparation_focus` |
| `preparation-focus.json` and explicit focus transition | A present object requires integer `1` and its existing closed fields; an absent whole focus file preserves legacy discovery | [Asset preparation](asset-preparation.md#allocation-and-revised-work), `preparation_focus` |
| Consumer execution config | Required integer `1`; existing closed schema and named profile constraints remain | [Consumer execution](consumer-execution.md), `consumer_execution.CONFIG_SCHEMA` |
| Destination observation report | Required integer `1`; existing closed schema, exact package identity and evidence checks remain | [Consumer execution](consumer-execution.md), `destination_observation.REPORT_SCHEMA` |

Version support does not waive any schema, source hash, semantic binding, path
confinement, state comparison or pending-job check. A missing optional field is
compatible only where that format already defines its absence. For example,
legacy request packets without optional connection/provider assertions retain
their documented preparation contract; a missing required marker version does
not acquire that exception. Candidate-plan authority/line-range additions remain
optional, and older closed-schema writers may reject these additions even when a
current reader can load the earlier plan.

## Unsupported versions and useful recovery

Known versioned metadata must not silently disappear from a production guard
because its version is unfamiliar. A reader checks the supported version before
interpreting the saved payload. An unsupported production-plan snapshot or caller
comparison cannot qualify as a valid current plan or complete comparison. An
unsupported preparation marker cannot be treated as absent legacy focus.

The shared version check reports `adapter_version` with the affected format,
observed value, supported version and recovery guidance. Existing operations may
surface that diagnostic as a blocker or nested production diagnostic rather than
abort an otherwise useful read. Other schema errors retain their own diagnostics;
the unchanged consumer and destination schemas continue to reject unsupported
versions through their existing errors. Version support alone never proves that
the rest of a file is valid.

The public error envelope classifies `adapter_version` as `missing_capability`
and returns recovery action `use_compatible_adapter`. This describes local format
support, not official-provider availability. An already unknown job retains its
more specific reconcile-existing-job guidance.

When a version is unsupported:

1. Preserve the exact file, its source kit and the diagnostic. Inspect the retained
   version and original operation instead of replacing it with a new empty plan.
2. Use a kit that explicitly supports that format, or restore the original kit
   alongside the current installation for the affected operation. Keep project
   state and retained evidence in the consumer project.
3. If a real semantic migration is necessary, use a documented, tested migration
   for that source and destination version. No such migration is supplied by this
   increment. Do not edit a version/header, recompute a digest to fit changed
   bytes, erase the marker or transfer an old verdict to bypass the diagnostic.
4. Reread current state and requirements before retrying the existing operation.
   Preserve submitted/unknown jobs and use their original provider connection for
   reconciliation; changing kit versions is not permission to dispatch again.

Missing historical library bytes are a separate problem. The
[retained-library operation](library-retention.md) preserves or recovers the exact
referenced source revision from an available original kit. It does not reconstruct
lost bytes, rewrite source identities or migrate adapter metadata.

## Changing a contract

Keep `PIXL/1`, `PIXL/2`, PLAR and each adapter's version independent. An adapter
change must identify the affected reader/writer contract and preserve the meaning
of already supported input. Optional additions must state which older writers
reject them. A changed interpretation of an existing field requires an explicit
version decision and saved-state compatibility evidence; a new kit label alone is
not that decision.

If a future change needs migration, specify the accepted source versions, target
version, exact semantic mapping, rejected cases and interruption/retry behavior.
Retain the original bytes and verify the new output separately. Any change to
state, sources or observations must keep the existing identity, provenance and
acceptance rules; migration cannot manufacture current review or remote results.

## Evidence and limits

Compatibility qualification combines format-specific positive/negative checks
with a retained consumer replay through the public installed-kit route. It must
show which old kit and saved files were used, which new kit actually executed,
whether source/art/state/acceptance remained unchanged, and what output was
produced. An original failure remains in the record when the corrected runtime is
retested. Tests against a synthetic future version establish rejection behavior,
not a successful migration from that version.

The development repository's `evidence/schema-compatibility/README.md` records the
actual qualification and its limits; historical trial files are not installed in
the kit. Local compatibility, rendering and file-identity
checks do not establish new native model behavior, provider execution, artistic
quality or human acceptance. Broader installation/update support remains separate
from these saved-format contracts.
