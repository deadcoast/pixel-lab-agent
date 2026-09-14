# Intake and representative-sample lifecycle

This implements review R3/R4 for the PIXL production profile. The developer retains the maintainer role. User authorization is the instruction to continue the next development target; implementation proceeds with review and recorded tests.

## Design decision and compatibility

Use an explicit `PX2` document format with the existing wire values and hashing rules. `Document.format` is an integer, defaults to 1, and is encoded in the header. PX1 parsing, canonical bytes, record hashes, registry and validation remain unchanged. PX2 uses `registry-v2.json` and the additions below. A store cannot change formats during commit: existing PX1 projects remain usable, while new lifecycle projects start with `intake`. No automatic migration invents confirmation, task criteria or prior verdicts. Importing unchanged K/S/E records from a PX1 library into PX2 preserves record identities; the enclosing document has its own format/hash.

Rejected alternatives: modifying PX1 in place would silently reinterpret saved state; keeping lifecycle state in sidecar JSON would split the authoritative production graph. A new header and explicit registry keep the operational language authoritative without discarding the working runtime.

## Records and meaning

The existing A/S/R/C/K/D/E/J/N meanings continue. PX2 adds the actor role `user`. P fields are `nm:str`, `ow:ref:A`, `sc:refs:S`, `in:refs:I`, optional `ct:ref:C`, optional `rt:refs:R`, optional `br:str`. No style is invented at initialization. C retains its raster fields and optionally adds `ch:refs:I` for the choices it instantiates. I choices may also describe custom aesthetic concerns; for keys matching C fields, the choice value must equal the instantiated field.

| Kind | Required fields | Meaning |
|---|---|---|
| I | `pr:ref:P`, `wh:ref:A`, `ky:str`, `st:sym:unresolved|observed|proposed|confirmed|conflict`, `vl:value`, `so:refs:S`, `wy:str` | A project choice and its epistemic status. Unknown values are null, not scaffold defaults. Conflict values are a list of at least two alternatives. Observed and confirmed values require source records; a proposal requires a rationale and can lack sources. |
| F | `tk:ref:T`, `nm:str`, `kd` as X's artifact enum, `rq:refs:Q`; optional `ct:ref:C` | A planned output, before any file exists. At least one applicable requirement is declared. The owner T must list it in `op`. Raster outputs need a concrete contract before active work; report/code/reference outputs may omit one. |
| Q | `nm:str`, `dm:sym:mechanical|visual|continuity|engine|other`, `md:sym:local|live|visual`, `ck:str`, `wh:ref:A`, `so:refs:S` | An observable acceptance criterion declared on the plan. Visual requires visual mode; engine requires live mode. Other domains explicitly choose their evidence mode. Criteria are project-specific, not a mandatory universal art checklist. |
| V | `tk:ref:T`, `rq:ref:Q`, `xr:ref:X`, `st:sym:pass|fail|unavailable`, `wh:ref:A`, `wy:str`, `at:str`, `ev:refs:E`; optional `ob:bool` | A retained candidate verdict for a particular requirement. No verdict means unperformed. Unavailable is distinct from failure; it needs a reason and no passing claim. Non-superseded duplicate verdicts for the same task/candidate/criterion are rejected. |

PX2 T fields are `nm,ow,pr,dp,dc,kn,st` with existing types; `ph:sym:research|sample|production|delivery`, `ip:refs:X`, `op:refs:F`, `ca:refs:X`, `vr:refs:V`. `io` and `ev` are PX1-only task fields. Research/sample tasks may have no decision and may investigate an unproven method. Production/delivery require an evidence-backed D and passing method proofs before activation. D's existing proof requirement is preserved.

PX2 X retains its fields with optional `ct` and optional `of:ref:F`. Raster kinds still require a C. An X with `of` must match that F's kind and contract. Standalone source/reference X records remain valid inputs. X always describes actual local bytes; F never fabricates a path or hash.

## Readiness and acceptance

An intake I must be listed by its project P.in; keys are unique within that project. Choices referenced by a task's output contracts must belong to that task's project. A C may retain a previous concrete interpretation when a choice becomes unresolved/conflict, but such choices block all active/done tasks using that output contract. For usable values, matching C fields must equal the linked choice. Active sample tasks can investigate observed/proposed choices. Active production/delivery requires all linked choices confirmed. Research can continue without resolving unrelated art choices. Ready reports only open tasks whose prerequisites and applicable prerequisites above hold. Inputs may intentionally reference another project's art contract.

Each F belongs to exactly its named T; T.op must agree. Candidate T.ca entries belong to its planned outputs, with at most one nominated candidate per output. Older rejected candidates remain X/V records but need not remain nominated. Each V must concern a candidate of its task and a Q required by that candidate's F. T.vr lists its recorded verdicts, including superseded history.

A pass/fail V requires non-superseded E receipts of the matching outcome and the criterion's required mode. Together they must bind the exact candidate, its semantic scope and the criterion's semantic scope. That includes the planned output, its requirements, contract and linked intake choices. Library POCs cannot substitute for this evidence. An unavailable V has no E requirement and cannot accept an output. Live means a caller-reported execution with retained evidence; it is not remote attestation.

Task completion requires all dependencies done, at least one planned output, exactly one nominated candidate per output, and a current passing verdict for every required criterion on each nominated candidate. Mechanical success cannot satisfy a visual or engine criterion. A rejected candidate and unavailable engine inspection remain resumable state, never accepted delivery.

Semantic proof traversal excludes workflow kinds P/E/T/J/N/V; I/F/Q are semantic. This avoids task/verdict changes invalidating the evidence they summarize. V itself is immutable after publication, except one-way `ob=+`, like E; correcting a verdict adds a new V. Superseding V does not alter E. E keeps its existing immutability and supersession semantics. Superseded V may retain a Q no longer required by the current F, preserving explicitly revised acceptance history.

New pass/fail V publication requires F and its semantic scope to exist unchanged in the preceding stored revision. Initialization cannot contain pass/fail V. Unavailable V does not claim execution and is exempt. This enforces recorded planning order, not a human's actual observation time. Production/delivery tasks may remain open without an adopted D, with the adoption gate reported as a blocker until activation.

For PX2, reopening a done task is required when the task or its relevant dependency closure changes, excluding traversal through P. Explicit contract/choice/source/input/output/criterion links determine that closure. Changing an unrelated project choice or project name must not invalidate an accepted sample. Changing an applicable contract invalidates its live E bindings and requires supersession/new proof as well as reopening affected done tasks.

## Operations and profile integration

`intake STORE --name NAME --brief TEXT --root ROOT` creates PX2 revision zero with the PIXL actor, a user actor and a project with empty source/choice lists, no C and no invented dimensions. CLI/MCP encode/decode preserve format; the JSON adapter accepts optional `format` (absence means 1), and decode includes it for PX2. `workflow FILE --root ROOT` / `pixl_workflow` returns format, hash, intake states, task blockers, per-output candidate/criterion status and local ready tasks. It validates actual files when rooted. It is read-only and does not create evidence or submit work.

The generic checked encode/commit interface authors lifecycle records; a new intake/sample skill supplies exact entry conditions, record examples, operation order, failure/recovery and stop conditions. It keeps proposals, inspected observations and confirmations distinct; declares acceptance before evaluating a sample; uses actual inspection evidence; and resumes from persisted state. No paid provider operation or target engine is impersonated.

## Verification and delivery

Verify PX1 byte compatibility and regression suite; PX2 codec/adapter closure and format rejection; empty intake without style; unresolved/conflicting choice blocking; research/sample before adoption; planned outputs without files; wrong-candidate/criterion/mode/fixture proof rejection; mechanical pass with visual failure; unavailable engine; immutable verdict correction; contract drift and scoped reopening; copied plugin and wheel operations. Exercise an actual persisted local fixture workflow through fresh subprocesses, retaining rejected candidate/evidence and accurate inspection limits. A developer-agent scenario separately checks the skill's use and stopping behavior.

Preserve the previous source milestone receipts before regeneration. Supplied training bytes and PIXL/1 normative semantics remain unchanged. Package the PX2 registry, spec and skill, update current docs and retain explicit limits. Provider-journal integration and general profile benchmarking remain subsequent targets.
