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

For follow-up, use the host's continuation tool for the returned native agent ID
when available. Current [Claude Code](https://code.claude.com/docs/en/sub-agents#resume-subagents)
uses `SendMessage` to that ID/name; another `Agent` invocation starts another instance.
Codex supplies its own continuation/message tools. Do not infer instance memory merely
from the same PIXL profile name. If continuation is unavailable, pass the saved
assignment, current contract, previous findings and exact handoff to a new instance,
and describe that as an artifact-based restart. This preserves useful work without
claiming an unobserved resumed conversation.

When the caller's deliverable depends on PIXL's result, keep that delegation on the
critical path. Ask the host to run it in the foreground and wait when supported.
Background work is useful while the caller has independent work, but a progress
message saying that the specialist is still running does not deliver the assignment.
Wait for its completion notification, inspect the returned artifacts and finish the
caller comparison and handoff before ending. In a non-interactive host, do not assume
that background work will survive the parent's final response. If the host stops the
child, retain its saved work, report the interruption and continue from those files;
an exit code of zero alone does not establish task completion. Current [Claude Code
foreground/background behavior](https://code.claude.com/docs/en/sub-agents#run-subagents-in-foreground-or-background)
depends on the host mode; use its available wait/continuation mechanism rather than
changing the user's global configuration.

A direct brief can proceed without first manufacturing a PLAR document. Use PLAR when allocation, dependencies or ongoing project work benefit from it. The caller owns application-wide priorities; PIXL owns art direction, appropriate PixelLab operation selection, reference use and visual evaluation within the assignment.

## Specialist → caller while working

Read the actual reference and consumer context. Resolve facts from supplied files and tools before asking the caller. If one consequential choice remains, send a small question with the affected asset, alternatives and what it unlocks. The caller can answer from its context or relay to the user. Continue unaffected work, carrying existing authorization rather than re-requesting it.

Keep creative proposals explicit. Distinguish “the reference contains this” from “the user requires this.” Report a tool/input mismatch with the viable path, not an invented parameter or a silently changed asset size. Progress messages report actual saved plans, job IDs or inspected files.

Resume the same task/state where possible. Check retained provider attempts before another request. A failed or interrupted child is a handoff boundary; it is not permission for the parent to duplicate a potentially submitted generation.

Before adopting a proposed production contract, use the [request and criteria handoff](request-review.md). The specialist returns exact source/request/criteria artifacts; the caller reads them independently and records a source-grounded comparison. Preserve specialist choices as choices, and continue within existing authorization once discrepancies are resolved.

## Specialist → caller at completion

Return a compact structured result (JSON or equivalent named fields). For a
PLAR-bound assignment, use the [caller view](../../../resources/spec/caller-result.md)
of the existing handoff operation so production identities and continuation come
from saved state. Direct briefs and planning-only work can use the fields below
without manufacturing PLAR or production records:

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
use `pixl_plar_handoff` with its `asset_id`, `requirements_hash`,
`production.continuation.state_hash` as `expect`, and your `details` object. The
selected read's top-level `hash` identifies the PLAR file, not production state.
CLI: `plar handoff DETAILS_JSON --path QUEUE --asset ID
--requirements HASH --expect STATE_HASH --view caller --root PROJECT`. The operation saves the
complete derived continuation and immediate `next` unchanged in an immutable file.
Return the caller view and its exact handoff locator; the caller opens the retained
file and compares its state identity with fresh focused PLAR. Omitting `--view caller`
keeps the existing receipt response. The view does not add acceptance or alter the
saved handoff. Do not copy selected fields into a rewritten resume.
Older handoffs remain readable; their original bytes are not migrated or relabelled.
Before returning a reviewed open task, check its current nominee and workflow
requirements. Saved verdicts on an unselected candidate do not describe the
active output. Nominate the intended candidate through normal state authoring
when appropriate; preserve unavailable verdicts and leave the task open.

`details` contains your assignment status, delivered artifacts, request-review links,
expert reasoning, actual checks, unresolved issues and future work. Keep completed
caller actions with evidence in `details.caller_actions`, and subsequent goals in
`details.future_work`. A completed caller review can be reported there while the
runtime still derives `review_delivery`; it does not replace that derived action.
The snapshot records both facts without inventing a new acceptance event. The runtime
does not decide whether your artistic judgment or assignment-status claim is correct.

Use optional `details.caller` for the bounded ordinary return: summary, artifact
and report locators, issues and integration findings, following its closed
[contract](../../../resources/spec/caller-result.md). Retain complete observations
in the other details fields and referenced files. Each declared file reference
contains exactly `path`, `sha256` and `role`; the runtime verifies its current
confined file bytes before publishing. These checks do not verify the role or
judgment you supplied. The caller view distinguishes
these authored claims from derived task, acceptance and continuation facts.
A missing integration observation stays unreported; an accepted candidate does
not manufacture an assignment-status or integration claim. Without `details.caller`,
`caller.present` is false and the full details remain retrievable; legacy prose is
not automatically summarized.

For example, only when the assigned destination inspection remains unperformed:

```json
{
  "status": "partial",
  "caller": {
    "summary": "Candidate bytes are retained; required destination inspection remains unperformed.",
    "integration": {
      "status": "not_performed",
      "summary": "No destination observation has been made for this assignment."
    },
    "issues": [
      {
        "category": "unfinished_work",
        "summary": "The assigned destination check has not run.",
        "recovery": "Run the assigned destination check, retain its actual evidence and refresh the handoff."
      }
    ]
  }
}
```

Use actual findings and omit inapplicable fields. Summary/recovery text is bounded
to 600 characters; artifact, report, issue and integration-evidence arrays each
hold at most 12 entries, and the complete caller block at most 8192 compact UTF-8
JSON bytes. Move detail to linked files instead of truncating obligations.
Integration status is `pass`, `fail`, `unavailable`, `not_performed` or
`not_in_scope`; omission is not one of those observations.

Follow the returned full-handoff, details and resume locators for exact retrieval.
Read `resume_inline`: the unchanged `resume` is present up to 4096 compact UTF-8
JSON bytes; otherwise `resume_ref` retrieves it in full. It is never rewritten or
truncated. `details_ref` and `resume_ref` identify physical source ranges and JSON
pointers in the same immutable handoff. Use its `path`/`sha256` for the full file.
These facts describe the captured selection; use the returned `refresh` read
after source or state changes, and reconcile the current identities. Read that full resume before acting on its jobs or
recovery instructions. Keep routine responses useful without pasting the complete
criteria audit, request report or tool transcript into the return.

On a cold resume, read the saved handoff and current focused PLAR. Changed state or
requirements require a fresh snapshot; matching hashes preserve the original job and
its originating connection. Resolve pending work, then retrieve/import and review its
actual result before proposing another generation. The caller's normal response can
explain later work in prose while linking the exact resumable artifact.

Keep detailed receipts in project files so the caller receives useful art and decisions rather than an entire transcript or image encoded in text.
