# PIXL ordered development backlog

Cycle: **IDENTIFY-2026-11-09-01**. Updated: **2026-11-09**. Plan status: **active**.

This is the work-selection queue derived from [IDENTIFIED](docs/IDENTIFIED.md) and ordered by [PLAN](PLAN.md). “Shelved” means retained for execution in that order, not abandoned. [TODO](TODO.md) is the active execution/result ledger and keeps its existing `PX-*` IDs. Findings provide implementation detail; they do not replace existing acceptance requirements.

Every actionable finding has one row below. Its linked finding contains rationale, affected source and verification condition; its milestone supplies the outcome exit. **Active** means mapped to the existing next TODO slice, not implemented. **Queued** means planned after its dependencies. **Conditional** means evaluate the named trigger before implementing the proposed mechanism. P1/P2 indicate outcome urgency, not estimated duration. Within a milestone, take the first ready group; supporting P2 work can accompany its P1 operation when necessary.

## M1 — Reliable assignment, review and resumption

[M1 exits](PLAN.md#m1--reliable-assignment-review-and-resumption). Existing links: PX-OPS-004, PX-OPS-003, PX-OPS-002, PX-SKILL-001/002.

| Finding | Work | Priority | Disposition / dependency |
| --- | --- | --- | --- |
| [NF-01](docs/IDENTIFIED.md#new-features-and-additions) | Ordinary candidate review submission | P1 | Implemented; both native hosts complete Working through explicit observations and derived bindings; [actual results](evidence/candidate-review/README.md) |
| [NF-02](docs/IDENTIFIED.md#new-features-and-additions) | Collective family review submission | P1 | Implemented; both native hosts complete the retained family with fresh destination execution, 15 independent state checks and 233 renderer checks each; [actual results](evidence/candidate-review/README.md) |
| [CF-01](docs/IDENTIFIED.md#core-function-improvements) | Review, nomination and completion recovery | P1 | Implemented — preflighted sequence, retained supersession and identical-retry recovery; [actual results](evidence/candidate-review/README.md) |
| [SC-02](docs/IDENTIFIED.md#source-code-changes) | Typed request/result boundary | P1 | Implemented for ordinary review — closed shared schema and typed operation boundary; [contract](spec/candidate-review.md). Existing handoff refinements remain separate |
| [SC-05](docs/IDENTIFIED.md#source-code-changes) | Safe record construction | P1 | Implemented — ordinary review constructs records with named fields; retained original failure unchanged; [checks](evidence/candidate-review/README.md) |
| [SC-03](docs/IDENTIFIED.md#source-code-changes) | CLI/MCP/service parity checks | P1 | Implemented for the new review operation — shared schema/runtime and CLI/MCP plus distribution checks; [results](evidence/candidate-review/README.md) |
| [QOL-03](docs/IDENTIFIED.md#qol-enhancements) | Explicit hash-domain labels | P1 | Implemented — public CLI/MCP result labels and stale-write/handoff explanations distinguish canonical state, file, requirements, binding, scope and comparison hashes without changing saved identities. Five new regressions plus distribution checks; [actual results](evidence/everyday-guide/README.md) |
| [QOL-05](docs/IDENTIFIED.md#qol-enhancements) | Snapshot versus current acceptance | P1 | Implemented — context/result separates immutable snapshot_acceptance and current_acceptance; [family checks](evidence/candidate-review/README.md) |
| [SC-01](docs/IDENTIFIED.md#source-code-changes) | Shared operation helper boundary | P2 | Implemented for the active operation — completion.planned_steps shared by existing completion and new review, retaining lifecycle checks; [results](evidence/candidate-review/README.md) |
| [QOL-02](docs/IDENTIFIED.md#qol-enhancements) | File output for large reports | P1 | Implemented for context, request comparison, candidate/family review and PLAR handoff; both native export follow-ups pass 13 independent checks each, including large reports and unchanged retry state. No-clobber and post-publication export failure are locally tested; [actual results](evidence/candidate-review/README.md) |
| [SC-04](docs/IDENTIFIED.md#source-code-changes) | Relevant choices in focused context | P1 | Implemented; semantic links retain authority/destinations, other intake stays retrievable. Current consumer shrinks from six expanded choices/40 sources to four/24. Both hosts retrieve indexed choices; Codex completion is guided. Full suite/distribution pass; [results](evidence/choice-comparison/README.md) |
| [QOL-08](docs/IDENTIFIED.md#qol-enhancements) | Concise successor decision comparison | P1 | Implemented; CLI/MCP/export share exact retrieval and review attention. Claude completes registered-agent 20-to-23 comparison with retained caller corrections; Codex initial partial is preserved, guided generic-child completion retains citation/static-scope addendum. No new acceptance; [actual results](evidence/choice-comparison/README.md) |
| [QOL-04](docs/IDENTIFIED.md#qol-enhancements) | Root/path/locator examples | P1 | Implemented — shipped examples distinguish install/consumer/store roots, CLI filesystem versus root-relative arguments, exact file hashes and source ranges. Relocation with spaces, arbitrary working directory and rejection cases verified; historical bindings preserved. [Results](evidence/everyday-guide/README.md) |
| [QOL-01](docs/IDENTIFIED.md#qol-enhancements) | Everyday production guide | P1 | Implemented — common skill and onboarding link assignment/allocation through official production, review, integration and handoff. Cold native caller outcomes use the retained consumers; broader reliability remains open. [Guide and results](evidence/everyday-guide/README.md) |
| [SC-10](docs/IDENTIFIED.md#source-code-changes) | Current README/status accuracy | P1 | Identified stale claims corrected — README now links scoped real production, current review operation and actual tool declarations; historical reports preserved |
| [SC-07](docs/IDENTIFIED.md#source-code-changes) | Extract cohesive preparation phases | P2 | Conditional — only if the active operation reveals a useful extraction boundary |

## M2 — Dependable native agent-to-agent operation

[M2 exits](PLAN.md#m2--dependable-native-agent-to-agent-operation). Existing links: PX-EVAL-005, PX-SKILL-001/002, PX-A2A-001, PX-OPS-004 native operation.

| Finding | Work | Priority | Disposition / dependency |
| --- | --- | --- | --- |
| [TM-06](docs/IDENTIFIED.md#technical-module-enhancements) | Resumable native trial records | P1 | Next enabling group — retain attempt/session/child IDs, last usable artifact and explicit restart/continuation conditions; use the existing interrupted Claude scenario. Enables meaningful reruns while M1 remains open |
| [CF-04](docs/IDENTIFIED.md#core-function-improvements) | Claude same-child continuation | P1 | Next with TM-06 — inspect actual session-persistence conditions and test continuation versus artifact-based restart separately; no M1 dependency for diagnosis |
| [CF-05](docs/IDENTIFIED.md#core-function-improvements) | Named Codex role qualification | P1 | Queued — verify actual installed role selection. New everyday-trial fixture refreshes its optional role assignment; its successful generic-child route does not qualify named-role selection. Prior guided comparison and partial result remain separate |
| [CF-02](docs/IDENTIFIED.md#core-function-improvements) | Complete independent semantic comparison | P1 | Partial evidence — current M1 comparison completes in Claude and guided Codex, with independent caller checks and retained corrections; earlier interrupted Claude scenario and broader unassisted behavior remain open. [Scope](evidence/choice-comparison/README.md) |
| [CF-03](docs/IDENTIFIED.md#core-function-improvements) | Artistic authority through native revision | P1 | Queued — use exact caller choices and preserve prior failures |
| [TM-04](docs/IDENTIFIED.md#technical-module-enhancements) | Official tool-contract freshness | P1 | Queued — before affected live requests; schema checks need no generation |
| [NF-03](docs/IDENTIFIED.md#new-features-and-additions) | Host readiness report | P1 | Queued — use actual native discovery/configuration observations |
| [QOL-06](docs/IDENTIFIED.md#qol-enhancements) | Consumer versus maintainer setup | P1 | Queued — can proceed independently; verify fresh loading |
| [QOL-10](docs/IDENTIFIED.md#qol-enhancements) | Compact caller result and continuation | P1 | Queued — use M1 result fields and existing immutable handoff |
| [SC-08](docs/IDENTIFIED.md#source-code-changes) | Actionable error categories | P2 | Queued — use observed native recovery cases; avoid speculative error framework |

## M3 — Source allocation through useful consumer production

[M3 exits](PLAN.md#m3--source-allocation-through-useful-consumer-production). Existing links: PX-PLAR-002, PX-PROD-001, PX-EVAL-005.

| Finding | Work | Priority | Disposition / dependency |
| --- | --- | --- | --- |
| [CF-06](docs/IDENTIFIED.md#core-function-improvements) | Broader PLAR allocation/update coverage | P1 | Queued — existing consumers first; can advance alongside host work |
| [CF-07](docs/IDENTIFIED.md#core-function-improvements) | Changed requirement through integration | P1 | Queued — allocation coverage plus M1 review operation |
| [NF-06](docs/IDENTIFIED.md#new-features-and-additions) | Destination observation import | P1 | Queued — use existing renderer outputs and exact package identity |
| [TM-07](docs/IDENTIFIED.md#technical-module-enhancements) | Reusable isolated consumer execution | P2 | Queued — supports NF-06 and native production without desktop dependency |
| [NF-08](docs/IDENTIFIED.md#new-features-and-additions) | Asset lineage view | P1 | Queued — use retained generated/constructed/reused queue members |
| [CF-10](docs/IDENTIFIED.md#core-function-improvements) | Useful complete native production per host | P1 | Queued — applicable M1/M2 operations and renderer path ready |
| [NF-05](docs/IDENTIFIED.md#new-features-and-additions) | Consumer allocation adapters | P2 | Conditional — another consumer demonstrates recurring mapping friction |
| [NF-09](docs/IDENTIFIED.md#new-features-and-additions) | Provider usage observations | P2 | Conditional — official response exposes reliable usage fields |

## M4 — Demonstrated domain judgment and recovery

[M4 exits](PLAN.md#m4--demonstrated-domain-judgment-and-recovery). Existing links: PX-EVAL-003, PX-SKILL-002; unresolved domain coverage in TODO group 4.

| Finding | Work | Priority | Disposition / dependency |
| --- | --- | --- | --- |
| [NF-04](docs/IDENTIFIED.md#new-features-and-additions) | Capability/outcome matrix | P1 | Queued — seed from retained evidence; update as outcomes arrive |
| [CF-08](docs/IDENTIFIED.md#core-function-improvements) | Unknown submission/retrieval recovery | P1 | Queued — complete remaining native conditions using durable jobs |
| [TM-03](docs/IDENTIFIED.md#technical-module-enhancements) | Interruption and concurrent-publication checks | P1 | Queued — relevant M1 regressions run during M1; broader coverage here |
| [TM-08](docs/IDENTIFIED.md#technical-module-enhancements) | Directional, animation and tile consumers | P1 | Queued — contract-specific representative fixtures for claimed specialties |
| [CF-09](docs/IDENTIFIED.md#core-function-improvements) | Artistic revision across domains | P1 | Queued — actual generated artifacts and appropriate destination fixture |
| [TM-09](docs/IDENTIFIED.md#technical-module-enhancements) | Knowledge retrieval tied to decisions | P2 | Queued — assess alongside real domain work, preserving caller authority |
| [NF-10](docs/IDENTIFIED.md#new-features-and-additions) | Operation-specific reference recipes | P2 | Conditional — add only when a representative assignment requires the operation |

## M5 — Reusable delivery and supportable product claims

[M5 exits](PLAN.md#m5--reusable-delivery-and-supportable-product-claims). Existing links: PX-PKG-001, PX-OPS-002 and TODO group 5.

| Finding | Work | Priority | Disposition / dependency |
| --- | --- | --- | --- |
| [SC-06](docs/IDENTIFIED.md#source-code-changes) | Saved adapter/schema compatibility | P1 | Queued — define alongside changed payloads; qualify old projects here |
| [TM-05](docs/IDENTIFIED.md#technical-module-enhancements) | Declared install/update support matrix | P1 | Queued — qualify supported routes and retain old-kit recovery |
| [TM-10](docs/IDENTIFIED.md#technical-module-enhancements) | Read-only evidence/release integrity | P1 | Queued — link current claims to exact source/package receipts |
| [NF-07](docs/IDENTIFIED.md#new-features-and-additions) | Consumer deliverable index | P2 | Queued — build on accepted package/handoff semantics |
| [QOL-07](docs/IDENTIFIED.md#qol-enhancements) | Current evidence navigation | P2 | Queued — scoped capability matrix and retained historical failures |
| [QOL-09](docs/IDENTIFIED.md#qol-enhancements) | Verification tiers and side effects | P2 | Queued — document actual commands and validate read-only route |
| [SC-09](docs/IDENTIFIED.md#source-code-changes) | Lock diagnostics and recovery guidance | P2 | Queued — preserve exclusion; no automatic stale-lock deletion |
| [TM-01](docs/IDENTIFIED.md#technical-module-enhancements) | Incremental boundary typing | P2 | Queued — prioritize interfaces exercised by prior milestones |
| [TM-02](docs/IDENTIFIED.md#technical-module-enhancements) | Context/validation performance measurements | P2 | Conditional optimization — measure first; retain results even if no change is needed |

## Moving work into TODO

Keep the current TODO item until its acceptance is met; related finding rows describe one useful operation, not competing projects. Implementation status does not imply general native reliability; follow each row's result link for the observed scope. When the slice finishes, select the next ready group in the earliest unfinished PLAN milestone. Add a small tag such as `[M1 | NF-01, NF-02, CF-01 | PX-OPS-004]` beside the TODO item, its expected outcome and source links. Do not copy this entire backlog into TODO.

After implementation, update that row's disposition with the TODO/result link and the observed evidence tier. Mark a finding resolved only for what the evidence proves. If one change resolves several findings, link all of them to the same evidence without counting the run several times. Retain superseded/deferred proposals and the reason; do not quietly delete findings or relax milestone exits.

## Next steps

Execution proceeds in [TODO](TODO.md). QOL-03/QOL-04/QOL-01 now have scoped implementation and consumer-use evidence; M1 and broader host reliability remain open. The next ready enabling group is M2 TM-06/CF-04: resumable native trial records and Claude same-child qualification using the retained interrupted scenario. Follow with CF-05 named Codex selection. This advances known continuation gaps without declaring M1 closed or forcing conditional SC-07 extraction. Consult [PLAN](PLAN.md) for dependencies and [IDENTIFIED](docs/IDENTIFIED.md) for rationale and verification. Run another IDENTIFY cycle only after PLAN's required exits are complete.
