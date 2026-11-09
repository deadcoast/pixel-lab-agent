# Agent-to-agent asset work

Use this operation when a calling Claude/Codex agent assigns visual work to PIXL. PIXL is the callable name of pixel-lab-agent (PLA). The profile supplies artistic judgment; this contract carries the assignment and result between agents.

## Caller → specialist

Supply the smallest complete assignment:

| Context | What the specialist needs |
| --- | --- |
| Outcome | Asset purpose, requested files and relevant success criteria |
| Workspace | Absolute consumer root; installed PIXL skill location |
| Requirements | Selected PLAR asset packet, or a complete direct brief |
| References | Addressable files/owned resource IDs, their roles and what to preserve |
| Authority | User decisions, proposals, unresolved choices and established authorization/limits |
| Resume | Existing store/task/output and pending provider IDs, when present |
| Integration | Destination, relevant consumers, and authorized code/import work |

Keep generated assets, request/review artifacts, helper scripts and scratch/previews inside the assigned consumer root unless the assignment names another authorized destination. Resolve paths against that root through each delegation and resumption; the shell's current directory or the kit's installation directory is not an implicit output destination. The caller checks returned paths against the agreed workspace as well as checking their bytes.

For PLAR, call `pixl_plar_read` with `asset_id`. Pass its selected row, transitive dependencies, source bindings, visual references and `requirements_hash`. Queue summaries alone omit production context. The reader supplies absolute paths for this filesystem; if the delegate uses another workspace, rebase paths and verify the same source bytes there.

The caller delegates to the native PIXL agent or a native specialist loading the shared PIXL skill. Keep the caller's model/tool/permission settings unless the assignment requires otherwise. Include the actual assignment in the delegation; naming a skill or saying “make the assets” does not transfer the parent's conversation. Credentials stay in the host's PixelLab connection.

When the assignment is to reassess or correct retained work, separate two scopes in
the delegation. **Historical evidence stays unchanged:** the original request, plan,
criteria, candidate, verdicts and provider history remain the record of what happened.
**The new proposal is editable:** PIXL may correct its check text, authority, basis,
scope, source pointers and proposed request wherever comparison reveals a defect.
Preserve the owner's actual requirements, not a prior agent's interpretation of them.
A prior accepted criterion is evidence of that earlier decision, not proof the source
requires it. Do not tell the specialist to keep all new criterion text identical while
also assigning contract correction; that prevents the requested work. Require an
explicit old-to-new change explanation and retain both artifact identities instead.
Corrections do not retroactively accept the old candidate or authorize resubmission.

A direct brief can proceed without first manufacturing a PLAR document. Use PLAR when allocation, dependencies or ongoing project work benefit from it. The caller owns application-wide priorities; PIXL owns art direction, appropriate PixelLab operation selection, reference use and visual evaluation within the assignment.

## Specialist → caller while working

Read the actual reference and consumer context. Resolve facts from supplied files and tools before asking the caller. If one consequential choice remains, send a small question with the affected asset, alternatives and what it unlocks. The caller can answer from its context or relay to the user. Continue unaffected work, carrying existing authorization rather than re-requesting it.

Keep creative proposals explicit. Distinguish “the reference contains this” from “the user requires this.” Report a tool/input mismatch with the viable path, not an invented parameter or a silently changed asset size. Progress messages report actual saved plans, job IDs or inspected files.

Resume the same task/state where possible. Check retained provider attempts before another request. A failed or interrupted child is a handoff boundary; it is not permission for the parent to duplicate a potentially submitted generation.

Before adopting a proposed production contract, use the [request and criteria handoff](request-review.md). The specialist returns exact source/request/criteria artifacts; the caller reads them independently and records a source-grounded comparison. Preserve specialist choices as choices, and continue within existing authorization once discrepancies are resolved.

## Specialist → caller at completion

Return a compact structured result (JSON or equivalent named fields):

- `status`: `delivered`, `partial`, `needs_input`, or `blocked`, judged against this assignment.
- `asset_id` and `requirements_hash` when PLAR supplied them; direct-brief tasks identify their brief.
- `artifacts`: project-relative paths, role, actual hashes and dimensions/frame metadata as relevant.
- `checks`: actual mechanical, visual and integration findings, with evidence paths and unavailable checks.
- `request_review`: packet and caller-review paths/hashes, with unresolved findings when applicable.
- `provider`: observed resource/job IDs and the production-state location needed to resume.
- `questions` or `next`: only outstanding decisions and the next concrete action.

When durable production state is in use, finish its accepted-candidate selection and task state through `task-complete` / `pixl_task_complete` after the saved required checks pass. The caller reads `workflow` to confirm the completed state agrees with the delivered files; an open task remains an explicit unfinished part of the operation. A planning-only assignment does not need manufactured production state.

Judge completion against the delegated scope. A planning-only assignment is delivered when its complete reviewed contract is returned; future generation remains outside that scope. An assignment ending at an accepted request is delivered when that request and its resumable state are returned, while the asset remains unaccepted and its production task open. State both facts explicitly. A full asset-production assignment is still partial at contract handoff. Retain the provider connection and simulated/live provenance with every job ID and next action; an ID cannot be resumed on a different service.

Include only applicable fields. A generation-only task can deliver a reviewed artifact while explicitly leaving engine import unverified. If the assignment requires integration, unavailable integration keeps that part unfinished. Never use a provider's completed status as artistic acceptance.

The caller opens the returned files and checks the relevant result against its original assignment. Compare a fresh selected PLAR packet if source context changed. `requirements_hash` tracks the selected requirements, reference bytes and dependency requirements; status/next-action changes alone do not change it. It is neither a spend authorization nor a readiness verdict. The existing file `hash` still governs PLAR writes.

For a PLAR-bound result, reread the selected asset after the last state change, then
use `pixl_plar_handoff` with its `asset_id`, `requirements_hash`, production `hash` as
`expect`, and your `details` object. CLI: `plar handoff DETAILS_JSON --asset ID
--requirements HASH --expect STATE_HASH --root PROJECT`. The operation saves the
complete derived continuation and immediate `next` unchanged in an immutable file.
Return that file's path/hash as `handoff`; the caller opens it and compares its state
identity with fresh focused PLAR. Do not copy selected fields into a rewritten resume.
Older handoffs remain readable; their original bytes are not migrated or relabelled.

`details` contains your assignment status, delivered artifacts, request-review links,
expert reasoning, actual checks, unresolved issues and future work. Keep completed
caller actions with evidence in `details.caller_actions`, and subsequent goals in
`details.future_work`. A completed caller review can be reported there while the
runtime still derives `review_delivery`; it does not replace that derived action.
The snapshot records both facts without inventing a new acceptance event. The runtime
does not decide whether your artistic judgment or assignment-status claim is correct.

On a cold resume, read the saved handoff and current focused PLAR. Changed state or
requirements require a fresh snapshot; matching hashes preserve the original job and
its originating connection. Resolve pending work, then retrieve/import and review its
actual result before proposing another generation. The caller's normal response can
explain later work in prose while linking the exact resumable artifact.

Keep detailed receipts in project files so the caller receives useful art and decisions rather than an entire transcript or image encoded in text.
