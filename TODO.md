# Pixel Lab Agent — overall plan and TODO

**Overall status: in development; the requested specialist ecosystem is not complete.**
Updated 2026-11-08 UTC against commit `3a2f280` plus the retained working-tree implementation and evidence below.
**Current checkpoint: request/criteria handoff and controlled delegated delivery are verified in both hosts, with Claude scope/timestamp defects retained. Next: PLAR consumer allocation/update coverage and a simpler first-request entrypoint.**

This is the current product-level work list. [Detailed task specifications](evaluations/TODO.spec.md) retain their IDs, historical attempts and narrower acceptance criteria. [The scaffold review](docs/PROJECT-REVIEW.md) explains the original findings; its dated sequence is historical. A consumer project's `plar.txt` is its asset TODO, not this repository's development plan.

## Intended outcome

A calling Claude or Codex agent can use PLA from another repository as its visual asset expert. PLA understands the actual consumers and reference intent, resolves consequential unknowns with the caller, selects and uses the official PixelLab tools, creates coherent assets, reviews and revises them, integrates or hands them back as assigned, and preserves enough context to resume without losing decisions or repeating submissions.

The profile owns expertise and judgment; skills supply workflows; knowledge supplies applicable methods; MCP/API tools perform deterministic operations and provider actions. Production uses the paid official PixelLab service under the assignment's existing authorization. Development-trial conditions apply to those trials only.

## Request coverage and preservation

The reposted requests are the product requirements. Repeated audit findings about artistic authority describe the same PX-SKILL-002 issue; they are not separate completion credit.

| Requested outcome | Work tracking it | Acceptance still required |
| --- | --- | --- |
| Audit and preserve the existing specialist, pixel-art knowledge and supporting mechanisms | Historical audit; ongoing mechanism assessment in PX-EVAL-005 | Explain from the completed operation what helps production, what needs a simpler interface and what remains optional; remove nothing merely to simplify the audit |
| A complete delegated PixelLab asset request in Claude and Codex | PX-EVAL-004 controlled baseline; PX-EVAL-005 current native route; PX-PROD-001 real production | Each caller receives and consumes the assigned assets; identify the provider conditions and actual quality/import evidence |
| Profile first: specialized visual expert, supported by knowledge, workflows and skills | Canonical profile; PX-SKILL-002; steps 2–5 | Requested aesthetics survive interpretation, tool arguments, revision and final review |
| Research current Claude/Codex and PixelLab capabilities; keep A–E answered | Dated reviews; PX-PLAR-002; final acceptance | Verify consequential changing platform assumptions against current official sources and actual host/tool behavior |
| Discover consumer context through a source overview/index/MOC and trace UI to backend state | PX-PLAR-001 base; PX-PLAR-002 remaining work | Reuse an available source map or derive a focused overview; report dynamic and uninspected surfaces without claiming exhaustive coverage |
| Allocate reusable/existing/missing assets to actual code consumers; maintain actionable plar.txt | PX-PLAR-001 base; PX-PLAR-002; PX-PROD-001 | Preserve existing assets, match current integration, update the queue after source/asset changes and verify useful handoff in a real consumer |
| Direct operational path from ordinary request to executable production | PX-EVAL-005, including intake friction | The caller supplies the assignment and receives the result without authoring low-level state for the specialist |
| Communicate, extract and quantify the needed context from another repository | PX-A2A-001 base; PX-SKILL-001; PX-PLAR-002 | Resolve supplied facts, ask the caller only consequential missing decisions, preserve authorization, and return usable paths/metadata/findings |
| Lightweight runtime installation; development tools remain available to maintainers | **PX-PKG-001 — implemented and verified** | Clean wheel/plugin installation contains only production dependencies; maintainer tooling remains available. Other OS/Python combinations remain unverified |
| Official PixelLab platform as the production interface | Operation skill; host connection templates; PX-EVAL-005/PX-PROD-001 | Use current official tool declarations and actual image inputs; keep credentials in the host connection |

Official references: [PixelLab docs](https://www.pixellab.ai/docs), [complete MCP tool overview](https://api.pixellab.ai/mcp/docs). Native HTTP and the supplied mcp-remote compatibility route remain documented in [host setup](docs/AGENT-KIT.md#connect-official-pixellab). Credentials supplied in conversation are not TODO content.

The implementation can improve the proposed PLAR format/workflow when evidence supports a better operation. No deadline or response boundary changes the acceptance criteria. These requirements remain open until their actual outcomes are established.

## What the evidence establishes now

| Area | Current state | Still outstanding |
| --- | --- | --- |
| Profile, skills, adapters and local runtime | Implemented; local validation, portable-plugin and installed-wheel checks pass | Dependable use throughout real production |
| Source-to-asset allocation (PLAR) | Implemented; raw-source example and source-binding/relocation behavior checked | Representative real consumer coverage and integration |
| Parent → specialist → delivery in both native hosts | Controlled MCP upload/review/revision/delivery and cross-host completion demonstrated; earlier failures retained | Claude consumer-scope adherence and observation-time accuracy; actual production quality and broader coverage |
| Reference-aware handoff | Exact packets, independent per-criterion review, actual upload handles and returned-file inspection exercised in both hosts | Generated reference fidelity and live target use |
| Artistic requirement authority | Revised native planning and controlled delivery contracts preserve required outcomes and scoped choices; [current findings](evidence/request-review/review.md) retain failures | General reliability, additional art types and actual generated quality remain unproven |
| Kit-update recovery | Implemented and verified against the historical failure, source relocation, local MCP, copied plugin and installed wheel | Current cross-host continuation passes; lost original bytes cannot be reconstructed |
| Artistic/engine acceptance | Local fixtures and inspection mechanisms exist | Actual generated art, successful revision, family consistency and destination acceptance |

The latest complete verifier reports **459 passing tests plus one Windows symlink-privilege skip**, 39 reference checks and a clean runtime installation. This request/review increment adds **22 regression tests**, covering image measurements/delivery, controlled upload/recovery, accepted-task completion and observation-time validation; the earlier retention increment added 17. The final observation-time correction is covered by request/history and no-publication regressions; it has not received another native full run. These are mechanism checks. Native behavior and actual artifact outcomes are recorded separately in [request/review evidence](evidence/request-review/README.md), with failures preserved. [Recovery evidence](evidence/library-retention/README.md), [earlier runtime/planning evidence](evidence/agent-handoff/README.md), [earlier HTTP-adapter trials](evidence/delegated-asset-request/README.md).

## Ordered remaining work

### 1. Complete reliable assignment and resumption

- [x] **PX-OPS-002:** reproduced and repaired the historical source-retention failure; unchanged state/receipts resume after kit replacement, after recovery from the original kit and after relocation. Local MCP, copied-plugin and installed-wheel checks passed. [Evidence and limits](evidence/library-retention/README.md).
- [ ] **PX-PLAR-002:** finish the source-overview/allocation/update workflow in a representative consumer, including missing assets, existing assets, backend states, coverage gaps and selective reallocation after changes.
- [x] **PX-SKILL-002:** exact source/request/criteria packets and independent caller comparisons implemented and behaviorally verified in bounded native planning/delivery cases in both hosts. Required qualitative outcomes survive; proposals remain scoped. Failed original attempts and remaining broader quality limits are retained in [the evidence](evidence/request-review/README.md).
- [ ] **PX-SKILL-001:** finish the unresolved Claude consequential-question/cold-handoff comparison, retaining the user's already established choices and authorization.

**Completion:** a subsequent agent can recover the same project after a kit update, identify changed or unavailable evidence accurately, preserve requested aesthetics and ask only the decision actually needed. Both host observations and actual retained artifacts support the claim.

**Next execution:** advance PX-PLAR-002 using the repository-supplied consumer: trace UI/backend states, update allocation after a source change, then derive the first executable request from that selection. Reduce repeated low-level plan authoring without weakening source/criteria identity. Both hosts have completed the controlled full assignment and the same earlier unfinished handoff; the new task-complete interface preserves every prior verdict/job. Fresh Claude delivery now reaches done, but its out-of-project temporary write and unsupported observation timestamp remain explicit failures. Newly prepared future timestamps are rejected; native use of that final runtime correction remains unverified. Another user project or asset commission is not a development prerequisite.

### 2. Complete the current native agent-to-agent operation

- [ ] **PX-EVAL-005:** controlled full delivery and durable completion observed in both hosts; overall conformance remains open. Fresh Claude still writes outside the assigned consumer root and records a guessed discovery timestamp. Preserve these findings while improving ordinary operation; do not equate repeated trials with general reliability.
- [x] Preserve reference roles and actual image inputs through dispatch, retrieval, inspection and the parent result. Both hosts inspect/reject the first candidate, review the changed request and consume the corrective downloaded file.
- [x] Reconcile an unknown submission without duplication and resume retained work. Codex resumes its completed project; Claude and Codex both complete the same unfinished handoff with unchanged source/criteria/verdict identities and no new generation.
- [ ] Simplify remaining state-authoring friction exposed by the operation. Accepted-candidate finalization now has one operation; native specialists still construct low-level PX2 records/scripts before the first edit; evaluate a simpler contract-to-plan entrypoint while preserving exact requirements. The parent should continue to supply an ordinary assignment. Keep optional archives and irrelevant method proofs off the ordinary path.

**Completion:** both hosts complete the assigned operation through the primary interface with the same declared scenario conditions and retained call/artifact evidence. Controlled provider responses establish operation behavior only. This does not replace step 3.

### 3. Complete actual consumer-project production

- [ ] **PX-PROD-001:** use an actual consumer repository, its visible UI/backend states, intended asset family and reference art to define the assignment and acceptance.
- [ ] Have each supported host carry a useful scoped assignment through official PixelLab generation, actual artifact inspection and any needed revision. Assign useful production work rather than duplicating requests solely to accumulate tests.
- [ ] Verify the delivered files in their real consumers: dimensions, state/direction/frame mapping, sampling, transparency, placement and visual purpose as applicable.
- [ ] Preserve failed candidates, actual job identities, final reviews, integration evidence and the caller's usable result. Update the consumer's PLAR queue against that evidence.

**Completion:** the caller receives and uses the intended assets; actual visual and destination checks pass for the assignment. A provider success flag, a plan, or a reference-identical fixture cannot close this milestone.

**Development scope:** use and improve the repository's self-contained representative consumer projects for workflow verification. Do not ask the user to choose another repository or commission an asset as a prerequisite for developing PLA. When the finished agent is invoked in a consumer, it receives that root and derives asset scope, references and renderer context there. Real-provider/art-quality qualification remains distinct from controlled workflow evidence; it is not a user-input blocker on this development task.

### 4. Verify the claimed expertise and recovery coverage

- [ ] **PX-EVAL-003:** complete the six recorded gaps: language-development routing, production-review routing, uncertain submission recovery, animation/tile context, unavailable engine and contract-change cold resume.
- [ ] Review representative UI/state assets, directional sprites, animation and tile work against the actual domain requirements. Record which additional PixelLab capabilities, such as fonts and normal maps, have only documentation/instruction support.
- [ ] Demonstrate useful revision: detect an actual defect, select an appropriate correction, preserve identity/style and reassess the result.
- [ ] Repeat relevant native cases after consequential profile/workflow changes; keep contradictory and failed results visible.

**Completion:** a capability/outcome matrix states what was exercised, under which host and contract, with remaining failures explicit. Do not advertise every documented tool as a production-verified specialty or treat a single good result as general reliability.

### 5. Finish reusable delivery and product acceptance

- [x] **PX-PKG-001:** separated runtime/development dependencies, preserved maintainer tools and verified a fresh minimal wheel/plugin installation. [Evidence](evidence/runtime-dependencies/README.md).
- [ ] Verify the supported installation/loading routes in fresh consumer repositories for both hosts, including configuration, relocation, updates and cold resumption.
- [ ] Before any public plugin-directory submission, resolve license metadata and the listing icon. Current native loading/format validation passes; the directory validator reports missing license metadata and an icon warning. This does not block local development or operation.
- [ ] Keep the everyday interface centered on assignment → asset → review/integration. Retain advanced state and research mechanisms behind the relevant operations.
- [ ] Reconcile the profile, skills, examples, host setup and TODO against the final evaluated versions.
- [ ] Review the required A–E questions against actual outcomes, and close or explicitly resolve every acceptance item above before declaring the overall request complete.

**Completion:** a caller can follow the documented route, obtain and resume reviewed production work, and understand the supported capabilities and limits without maintainer improvisation. Marketplace publication is a separate distribution choice, not a hidden requirement.

## Work already completed within narrower scopes

- [x] Canonical profile/package repair, inline JSON commits and PLAR source allocation — [PX-PLAR-001](evaluations/TODO.spec.md#px-plar-001--source-linked-project-asset-requirements).
- [x] Local candidate inspection with retained reviews — [PX-OPS-001](evaluations/TODO.spec.md#px-ops-001--candidate-inspection-with-retained-review-evidence).
- [x] Recorded baseline and matched host observations — PX-EVAL-001/002. Completing the comparison did not turn its failed criteria into passes.
- [x] Native controlled delegated deliveries — [PX-EVAL-004](evaluations/TODO.spec.md#px-eval-004--delegated-pixellab-integration-in-both-hosts).
- [x] Reference roles, complete selected dependencies, caller result contract and one independent planning exercise — [PX-A2A-001](evaluations/TODO.spec.md#px-a2a-001--reference-aware-assignment-and-result).

These checks close their named increments only. They do not check off the ordered product outcomes above.

## Continuity and reporting

Keep this plan current across conversations. Before starting new work, identify the open item it advances and its completion criterion. An increment is a way to finish the overall request, not a replacement for that request.

After meaningful work, report: **what changed; what was actually verified; what remains open in the active item; the next concrete action; whether the overall outcome is complete.** If required work is unfinished, keep the item open and retain the continuation context. Avoid completion percentages without a defensible denominator.

The required A–E questions remain part of understanding and review, not generic workflow blockers: improvement, host compatibility, contextual/artistic quality, consumer-project operability, and where responsibilities live. Current answers: [request/review and native outcome review](evidence/request-review/README.md#required-ae-review), [PLAR review](docs/PLAR-REVIEW.md) and [agent-handoff review](docs/AGENT-HANDOFF-REVIEW.md). Revisit the affected answers when implementation or outcome evidence changes.
