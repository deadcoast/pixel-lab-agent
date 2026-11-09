# IDENTIFY development workflow

Use this workflow to audit the repository against its intended product, preserve actionable findings and maintain an execution chain across conversations. It is a maintainer workflow; it does not activate the PIXL production role or become part of a consumer's asset-generation instructions.

## Document responsibilities

| Document | Authority and use |
| --- | --- |
| [docs/IDENTIFIED.md](../IDENTIFIED.md) | Current audit cycle: intended/current comparison, strengths, weaknesses, source/evidence references, required A–E answers and five actionable finding lists |
| [PLAN.md](../../PLAN.md) | Ordered outcome milestones, dependencies, exit criteria and overall cycle status |
| [SHELVED.md](../../SHELVED.md) | Findings selected and ordered by PLAN, with stable IDs, priority, disposition, dependencies and result links |
| [TODO.md](../../TODO.md) | Existing active work, actual results and continuation; link/tag it with milestone/finding IDs without wholesale restructuring |

The flow is **[IDENTIFIED + PLAN] → [SHELVED] → [TODO]**. A consumer project's `plar.txt` remains its asset TODO; it is not replaced by this development workflow.

## Choose audit or continuation

1. Read the current user direction, AGENTS, TODO, PLAN and SHELVED before changing the work order. If `.codegraph/` exists, use CodeGraph first for code-location/understanding questions; otherwise use ordinary source exploration.
2. If there is no audit/plan yet, run the initial workflow below and create the missing documents. If PLAN is active, continue the existing work; a completed patch, trial or TODO slice does not trigger a new full audit.
3. Update narrow findings, evidence links and dispositions as work changes their facts. Preserve prior results and cycle identity. Do not claim that proposed work is implemented or that interrupted trials passed.
4. Run a new full IDENTIFY **only when the current PLAN's required exits are complete**, unless the user explicitly changes this workflow. Preserve the prior cycle's findings and dispositions before creating the next cycle. Do not treat missing optional proposal implementation as failure if it has an explicit justified disposition; do not use deferral to waive a required outcome.

## Run the initial or next full audit

1. Establish repository identity, working-tree state, intended design, source authorities and existing evidence. Preserve uncommitted work and historical failures. Read relevant specs/registries together before recommending saved-format changes.
2. Trace the important operation from caller intent to actual output. Inspect representative runtime paths, skills, host adapters, tests, packaging and failure/recovery mechanisms. Consult current official platform/provider documentation for changing compatibility assumptions.
3. Compare intended behavior with implementation, native behavior and actual outcomes separately. Identify strengths to retain and weaknesses with consequences. Label an observed defect, unverified outcome and design proposal distinctly. Verify mutable claims cheaply where possible; label retained test results with their original scope.
4. Write `docs/IDENTIFIED.md` with a dated cycle ID, source/evidence links, limitations and substantial actionable bullet lists for **NEW-FEATURES-AND-ADDITIONS**, **SOURCE-CODE-CHANGES**, **QOL-ENHANCEMENTS**, **CORE-FUNCTION-IMPROVEMENTS** and **TECHNICAL-MODULE-ENHANCEMENTS**. Give each finding a unique stable ID, affected operation/source, intended improvement, verification condition and milestone. Do not pad counts with duplicate work.
5. Answer A–E explicitly: how to improve; compatibility with Claude/Codex; contextual and artistic quality; operation from another repository; and division of responsibility among profile, skill, MCP/runtime and official provider. These are understanding questions, not generic permission gates.
6. Create or reconcile PLAN from the existing product requirements and work order. Define outcome exits and dependencies; recognize work already completed within its actual scope. A plan is not a clean-slate redesign or a reset of unfinished objectives.
7. Incorporate every actionable finding into SHELVED exactly once, grouped by PLAN milestone. Link the finding and its verification condition; assign priority/disposition and relevant existing task IDs. Conditional proposals name the evidence needed before implementation.
8. Make small contextual changes to TODO: workflow links, active milestone/finding tags and the next source of work. Preserve the existing structure, detailed results and outstanding acceptance. Correct a current factual contradiction when the audit establishes it, without rewriting old receipts.
9. End each document with contextual next steps: findings to PLAN/SHELVED; PLAN to ordered backlog/execution; SHELVED to TODO; TODO completion back to SHELVED. Only PLAN completion permits the next full IDENTIFY cycle.
10. Verify finding-to-backlog coverage, milestone references, document links and skill discovery format. Record what was freshly checked versus retained. Do not run evidence-mutating full verifiers merely to validate documentation. Create/update a durable reference for this workflow where authorized; project docs are the authority, not a memory-only copy.

## Continue execution

Use the active TODO slice and its linked SHELVED rows. Implement a complete useful operation, run verification appropriate to its behavior and record actual results. Update the affected A–E answers and backlog dispositions when evidence changes them. Keep unmet acceptance open and retain the continuation rather than substituting a smaller claim of completion.

When that slice completes, take the earliest ready group from SHELVED in the earliest unfinished PLAN milestone. Continue independent work when a specific external dependency is unavailable. A response boundary, temporary host limit or completed local test is not a reason to repeat the audit or abandon the overall objective.

## Next steps

For this repository's active cycle, read [PLAN](../../PLAN.md), select work from [SHELVED](../../SHELVED.md) and continue [TODO](../../TODO.md). Preserve the completed cycle and rerun this workflow after PLAN's required exits are satisfied.
