# PIXL/2 normative specification

PIXL/2 adds explicit intake and candidate acceptance to the existing agent-operated language. Its header is `PX2 <revision>`; value framing, bounds, identifiers, canonical ordering and record hashing follow [PIXL/1](PIXL-1.md). The enclosing canonical document includes its own format header. Existing PX1 files and the [PX1 registry](../pixl/registry.json) retain their original semantics.

The complete PX2 field/type schema is [registry-v2.json](../pixl/registry-v2.json). Fields inherited unchanged from PX1 retain their defined meanings. Unknown kinds, fields and enum values fail. The JSON host adapter may include `format: 2`; absence means 1. The lifecycle commands never guess a format from fields. Library records can be copied with their complete dependency closure without changing record hashes; validate the destination document and its actual file paths.

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

## Publication, amendment and resumption

All PX1 concurrency, path confinement, immutable E and history publication guarantees remain. V fields are immutable after publication except one-way `ob=+`; correcting a verdict adds a new V ID. A newly introduced V cannot already be superseded: it must first pass current validation and be published, then a later revision may supersede it. Existing IDs cannot disappear. A store rejects format changes during commit. Existing PX1 stores are not automatically upgraded because old state does not identify confirmed choices or required acceptance. Start a new explicitly authored PX2 project when these operations are needed; preserve the old project as its own source/history.

For each newly published pass/fail V, the planned F and its complete semantic scope, including Q and C/choices, must already exist unchanged in the immediately preceding saved state. Save planning/criterion changes before collecting and publishing results. Initial PX2 publication cannot contain pass/fail V. Unavailable observations do not claim evaluation and are exempt from this ordering rule. This establishes recorded ordering between a plan and its verdict; it cannot independently attest when a person actually inspected an image.

A done task must reopen when it or its relevant dependency closure changes. PX2 closure does not traverse through P: an unrelated intake choice or project display name does not reopen an accepted sample. Link actual semantic dependencies through its input/output contracts, choices, criteria, sources and decisions. Changing one of those dependencies requires reopening and superseding stale E/V before new evaluation. History remains available for cold resumption.

## Operational boundaries

Use `intake`, `decode`, `encode`, `validate`, `commit`, `workflow`, `ready`, `context` and `impact` through the selected runner; MCP adds `pixl_intake` and `pixl_workflow`. `context` retains PX2 format and complete references. Mutable state and evidence live in the art project, outside installed resources. Generic encode/commit can author the declared records; they do not perform inspection or grant approval.

This version supplies the local intake/sample lifecycle. The platform prepare/job journal remains a separate local observation mechanism; J is not yet a durable provider-submission integration. Real PixelLab execution, actual visual judgments, destination-engine verification and model performance require their own observed evidence.
