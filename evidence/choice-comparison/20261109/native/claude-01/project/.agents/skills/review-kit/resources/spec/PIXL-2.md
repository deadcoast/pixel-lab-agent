# PIXL/2 normative specification

PIXL/2 adds explicit intake and candidate acceptance to the existing agent-operated language. Its header is `PX2 <revision>`; value framing, bounds, identifiers, canonical ordering and record hashing follow [PIXL/1](PIXL-1.md). The enclosing canonical document includes its own format header. Existing PX1 files and the [PX1 registry](../pixl/registry.json) retain their original semantics.

The complete PX2 field/type schema is [registry-v2.json](../pixl/registry-v2.json). Fields inherited unchanged from PX1 retain their defined meanings. Unknown kinds, fields and enum values fail. The JSON host adapter may include `format: 2`; absence means 1. The lifecycle commands never guess a format from fields. Library records can be copied with their complete dependency closure without changing record hashes; validate the destination document and its actual file paths.

PX2 shares PX1's optional [library-source retention](library-retention.md): source resolution preserves the declared revision and reports its retained identity, while choice authority, adoption, candidate and verdict semantics remain unchanged.

## Intake and concrete contracts

P owns a list `in` of I choices and can retain the brief in `br`. Its `ct` is optional. Initialization via `intake` creates no C, dimensions, projection, palette or alpha defaults. The user is a valid A role. Old `init` remains a PX1 initializer for compatibility.

I has an owning project `pr`, responsible actor `wh`, key `ky`, status `st`, value `vl`, source list `so` and rationale `wy`. Keys are unique within a project. Each I must appear in its P.in and cannot appear in another project's list. Status is one of:

| Status | Required meaning |
|---|---|
| unresolved | `vl=?`; retain the missing choice or question in `wy` |
| observed | Non-null value with source evidence; an observation does not establish agreement |
| proposed | Non-null candidate value and rationale; sources can be absent |
| confirmed | Non-null value and supporting source, including a retained user instruction where applicable |
| conflict | At least two alternatives in `vl`, with sources/rationale preserving the disagreement |

Confirmation is a recorded claim supported by sources, not authentication of the actor. A C is a concrete raster interpretation and can link its contributing choices through `ch`. When a linked choice is usable, a key naming an existing C field must have the same value as that field; custom aesthetic choices remain explicit semantic context. A previously concrete interpretation may remain recorded when its choice becomes unresolved/conflicting, but that contract cannot support active work until the conflict is resolved. This permits preserving old candidates and evidence while recording newly discovered uncertainty. Existing sources may intentionally use another contract.

## Planned work and materialized candidates

PX2 T has `ph` (research/sample/production/delivery), `ip` (existing X inputs), `op` (planned F outputs), `ca` (nominated X candidates) and `vr` (retained V verdicts), alongside `nm/ow/pr/dp/dc/kn/st`. PX1 task fields `io/ev` are not PX2 fields.

F names a planned output and its kind, owning task `tk`, applicable requirements `rq`, and optional contract `ct`. T.op and F.tk must agree. F contains no invented file identity; it can exist before work produces a file. Each F requires at least one Q. A candidate X uses `of` to identify its F and must match its kind and contract. X always names actual bytes. Report/code/reference X may omit C; raster kinds cannot.

Research and sample phases can investigate unproven K and can lack D. An open production/delivery task can plan before adoption; activation/completion requires an evidence-backed D and passing K scope coverage. D's research/proof requirements are unchanged. All active/done tasks require their prerequisites done. Raster output plans require a concrete C before activation, and unresolved/conflicting output choices block every phase. Sample work can test proposed/observed choices; production/delivery requires all choices in its output contracts confirmed. These choices must belong to the task's project. Input reference art can have another project's style and is not forced to adopt the output contract.

`ready` returns only open tasks with satisfied local blockers. It never establishes remote availability or acceptance. `workflow` reports unresolved intake, per-task blockers and each planned output's candidates and requirement outcomes. A report can distinguish an unperformed check, a failed check and an unavailable check without changing state.

## Required acceptance and retained verdicts

Q declares an observable condition `ck`, owner `wh`, sources `so`, domain `dm` and required evidence mode `md`. Domains are mechanical, visual, continuity, engine and other. Visual criteria require visual mode; engine criteria require live mode. Other domains choose their applicable mode explicitly. There is no universal requirement that every output use every domain. Requirements belong to the plan and are stated before observing the candidate's results.

V identifies a task, candidate X, required Q, reviewer, timestamp, rationale, status and supporting E receipts. Status is pass, fail or unavailable. Absence of a current V means unperformed. An unavailable verdict records the reason with no E and cannot accept anything. Only one non-superseded V may exist for a task/candidate/criterion combination; T.vr retains every V for that task.

Current pass/fail verdicts require non-superseded E of the matching outcome and Q's required mode. Their combined bindings cover the candidate's full semantic scope and Q's full semantic scope. Thus evidence is bound to the actual X/F/C/I/Q/source revisions, not just an artifact name or a generic fixture. Receipt mode is a caller assertion backed by a retained file; live mode does not authenticate a service or engine. A provider response or bundled method POC cannot be substituted for a visual or engine acceptance obligation by reusing its old bindings.

Semantic traversal in PX2 excludes P/E/T/J/N/V and includes I/F/Q as well as the original semantic kinds. Changing task states or superseding V therefore does not recursively change the evidence it summarizes. Changing a contract, applicable choice, plan or criterion invalidates live E bindings. Superseded V retains its old outcome and references but no longer requires current criterion membership or current E support. This permits an explicitly revised plan to retain historical rejected or obsolete requirements.

A done task needs all prerequisite tasks done, at least one F, exactly one nominated X per F, and a current passing V for every Q on every nominee. Mechanical success alone cannot satisfy visual or engine criteria. Older rejected candidates remain recorded and do not prevent selecting a later candidate, but no unreviewed replacement inherits their proof.

The optional [task completion operation](task-completion.md) nominates explicit already-reviewed candidates and publishes the existing active/done transitions. It retains all acceptance checks and creates no verdict or new UDL field.

## Publication, amendment and resumption

All PX1 concurrency, path confinement, immutable E and history publication guarantees remain. V fields are immutable after publication except one-way `ob=+`; correcting a verdict adds a new V ID. A newly introduced V cannot already be superseded: it must first pass current validation and be published, then a later revision may supersede it. Existing IDs cannot disappear. A store rejects format changes during commit. Existing PX1 stores are not automatically upgraded because old state does not identify confirmed choices or required acceptance. Start a new explicitly authored PX2 project when these operations are needed; preserve the old project as its own source/history.

For each newly published pass/fail V, the planned F and its complete semantic scope, including Q and C/choices, must already exist unchanged in the immediately preceding saved state. Save planning/criterion changes before collecting and publishing results. Initial PX2 publication cannot contain pass/fail V. Unavailable observations do not claim evaluation and are exempt from this ordering rule. This establishes recorded ordering between a plan and its verdict; it cannot independently attest when a person actually inspected an image.

A done task must reopen when it or its relevant dependency closure changes. PX2 closure does not traverse through P: an unrelated intake choice or project display name does not reopen an accepted sample. Link actual semantic dependencies through its input/output contracts, choices, criteria, sources and decisions. Changing one of those dependencies requires reopening and superseding stale E/V before new evaluation. History remains available for cold resumption.

The optional [selected-asset preparation adapter](asset-preparation.md) authors the
existing candidate/sample records from exact reviewed PLAR artifacts and retains
input bytes. Its explicit versioned report-X metadata binding also checks current
PLAR identity before new job preparation/dispatch; it does not add record fields or
relabel an expert candidate interpretation as owner-approved production.

## Operational boundaries

The optional [candidate/family review adapter](candidate-review.md) retains explicit
observations through existing X/E/V, derives exact evidence scope and connects
nomination/completion with recoverable publication. It adds no registry fields;
prepared inspection packets retain their existing coverage contract.

The optional [connected production-plan adapter](production-plan.md) authors
family/stage wiring from reviewed JSON and binds exact accepted upstream inputs
before preparing a staged request. It uses existing T/F/Q/X and PLAR metadata;
contracts, adoption, provider execution and acceptance keep their existing meaning.

Use `intake`, `decode`, `encode`, `validate`, `commit`, `workflow`, `ready`, `context` and `impact` through the selected runner; MCP adds `pixl_intake` and `pixl_workflow`. `context` retains PX2 format and complete references. Mutable state and evidence live in the art project, outside installed resources. Generic encode/commit can author the declared records; they do not perform inspection or grant approval.

This version supplies the local intake/sample lifecycle. The original platform prepare/job tools remain stateless local operations. Real PixelLab execution, actual visual judgments, destination-engine verification and model performance require their own observed evidence.

## Durable provider jobs (registry 2.1.0 extension)

J opts into durable history by supplying `jr` (current journal report X), `op` (nonempty distinct F outputs) and `xs` (all imported X candidates in event order, initially empty). J.xs preserves typed dependency closure for focused retrieval; these are not task nominations. Existing J without these fields retains its earlier semantics. A published legacy J cannot acquire this extension, and a durable J cannot shed it. Older PX2 readers reject these additional fields explicitly. PX1 schema and semantics are unchanged.

The retained journal uses the version-1 closed JSON contract in [provider-recovery.md](provider-recovery.md). J.tk/tl/ah/si/ri/op must exactly project its task/tool/intent hash/state/remote identity/outputs. J.ev retains ordered local E receipts for every snapshot, starting with prepared intent and adding one snapshot per event. Each non-superseded local passing E binds exactly its immutable journal X and shares its path/hash. The last receipt binds J.jr. Such a pass establishes retention and local consistency; it is not remote, mechanical, visual or engine acceptance.

Generic rooted validation replays the journal and every prefix, verifies local bytes and candidate bindings, and rejects invented projections. Publication requires a saved unchanged production plan before new prepared intent, one event per subsequent commit, immutable intent, immutable retained X/E, and unchanged imported candidates. No initial-state job can invent earlier submission history. Preparation and dispatch require satisfied task activation prerequisites and an open/active task. Another nonterminal durable attempt for an overlapping output, or an unjournaled nonterminal job for the task, blocks new preparation/dispatch.

The local dispatch claim publishes `unknown` before returning the request to its host. It does not contact a service. Unknown work must be reconciled rather than resubmitted. Caller-supplied observations retain the returned identity and evidence; accepted states require an ID, which cannot change once recorded. Failed and succeeded are terminal except that success may import new candidates. Completion never follows from provider success: imported candidates still require their declared V criteria.

Changed request context blocks dispatch but does not erase submitted history or prevent recording observations. Recovery reports list drift and next actions. Imports bind copied local bytes and the original output plan; a changed output plan must be reconciled before import. All operations use expected-hash publication. Unreferenced immutable blobs may remain after a failed commit; state.px is the sole publication authority. Local coordination cannot guarantee exactly-once remote execution or prevent a host from bypassing the procedure.

## Family production and delivery (registry 2.2.0 extension)

An optional F.bs names the exact X baseline for production or delivery. It is a semantic dependency, unlike the workflow-only T.ip. The baseline must belong to another sample task in the same project; its X is also listed in the consuming task's ip, and its task is a direct dp prerequisite. Open plans may preserve an unaccepted or replaced baseline. Activation/completion requires that exact sample still nominated and its task done. A sample's passing evidence does not automatically accept a family member.

F.mb and F.ds together opt a report-kind output of a delivery task into the family operation and require bs. mb is a nonempty distinct ordered list of planned F members; ds is a nonempty distinct list of same-project I destination choices. Members cannot be the family output itself or another family output. They are the baseline's sample output or same-project production outputs sharing that exact bs. All member tasks are direct delivery prerequisites. A family declares at least one continuity Q, with project-specific mode/conditions; engine Q is declared when applicable. All destination choices must be confirmed for delivery activation/completion. Missing/unavailable engine acceptance remains separately represented through Q/V.

A family manifest X has xs: baseline X first, then one selected X per member in the saved order (the baseline may also be a delivered member). xs belongs only to family report candidates and is required on every candidate of a family output. These references bind collective acceptance to the actual baseline, selected member identities, their plans/contracts and the destination/criteria scope. Merely listing siblings in T.ip does not supply this semantic proof.

The [family delivery manifest contract](family-delivery.md) governs immutable copied files, saved-plan publication, historical membership and current acceptance. Existing family F cannot shed bs/mb/ds, and existing X cannot acquire fabricated snapshot history. Once published, a manifest X and its baseline/member X records are immutable; revisions add new candidate IDs. Changes to underlying contracts/requirements still require the existing supersession/reopening procedure.

`family` / `pixl_family` reports baseline eligibility, member and collective acceptance, destination choices, pending provider attempts, saved snapshots and drift. `family-snapshot` / `pixl_family_snapshot` retains selected member bytes and publishes an unaccepted report candidate. It requires an open/active family task, the accepted baseline and all selected members on done tasks, no pending attempts for involved tasks, and the unchanged previously saved family plan. Snapshotting local files is allowed while destination/adoption/collective acceptance remains unresolved; it does not activate, nominate, evaluate or complete the delivery task. Actual artistic continuity and target-engine readiness require their own inspection and evidence.

PLAR-bound continuation uses the [allocation/revision contract](asset-preparation.md#allocation-and-revised-work). Pending attempts for the same explicitly tagged asset exclude new jobs even under different task/output IDs. New task activation/completion checks the current selection and selected generation; retained historical validation is unchanged.
