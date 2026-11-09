# Intake through a reviewed representative sample

Use this operation for an incomplete brief, a consequential artistic uncertainty, or the first representative item/pose/cycle/neighborhood before producing a family. Follow the [production profile](../../../resources/agent/PROFILE.md). This reference governs PIXL operation; maintaining this repository remains a development task.

## Required context and entry

Read the actual [PX2 specification](../../../resources/spec/PIXL-2.md) and [registry](../../../runtime/pixl/registry-v2.json). New lifecycle projects use `intake STORE --name NAME --brief TEXT --root PROJECT_ROOT`, or `pixl_intake`. It creates a project and actors without a style contract. Existing PX1 state keeps its version; `workflow` deliberately rejects it. Do not relabel an old header, invent past confirmation, or discard old evidence to migrate it.

Inspect available references and artifacts at native scale and enlarged scale. Identify which choices affect this operation and which can remain unresolved. Preserve the user's actual instruction or relevant observation in project-owned source files, then record S identities/ranges. The profile supplies the judgment; dimensions, binary alpha and fixed palettes are not universal requirements.

## Keep authority through derived rules

Before deriving a style contract, acceptance criterion, checker rule or provider instruction, retain a compact account of each consequential restriction: property/value, authority and status, exact supporting instruction or adopted project choice, and where the restriction applies. Use the existing choice/source fields in PIXL state; this account adds no UDL fields. Carry its status through the entire approach, including prompts, checks and handoff.

The user's instruction and adopted project choices establish requirements. Reference pixels establish observations; matching a reference does not adopt every measured dimension, color, gap, alpha level or component count as a mandatory rule. For an unspecified property, explain a project-specific proposal and the trial it would test. A proposed trial can proceed within existing authorization while the final production choice remains open.

If your interpretation of an image differs from the brief's terminology, describe the observed pixels and the uncertainty while preserving the requested treatment. An alternative that contradicts that treatment is a change for the user to adopt, not a correction you can silently install in the contract. Neither a tool default nor a passing checker supplies that adoption.

Keep diagnostic conclusions attached to their tested artifact, method, scale and background. Failure of one resized fixture does not establish a minimum canvas for other designs; a measured component count or contrast ratio does not establish a universal rejection threshold. Label verified tool limitations separately from artistic choices.

Before saving the approach or a verdict, trace every enforced artistic restriction back to that account. Correct downstream claims such as “approved,” “binding,” or “must” when their source is still observed, proposed or unresolved. Preserve the earlier draft and its evidence when correcting it.

For a selected PLAR asset's first concrete candidate, use [PLAR preparation](../../plar/references/prepare.md) to save the reviewed output/criteria plan and first durable request in one operation. The record-level sequence below remains available for advanced plans and explicit amendments.

## Preserve intake and plan before execution

1. Load the current state and canonical hash. Decode it through the runner, keeping `format: 2` in the host adapter. Amend the relevant fields, increase the revision by one, encode a candidate, validate against the project root, and commit with the previously observed hash. A stale-write error means reload and reconcile.
2. Add each consequential choice as I with project, actor, key, status, value, sources and rationale; add it to P.in. Unknown values are null. Observations, proposals and confirmations remain different statuses. Preserve conflicting alternatives instead of selecting a scaffold default.
3. Research the uncertain technique through the [knowledge operation](knowledge.md). A K recipe or reference POC is useful context, not a proof for this asset. A research/sample T can use unproven K and have `dc=[]`; it does not need a fabricated D. Adoption into production/delivery needs the specified decision and applicable proofs.
4. Name the smallest useful sample as F, owned by its T. Separate T.ip inputs, T.op planned outputs and T.ca actual nominated candidates. Before a file exists, F is the output plan; do not create a false X path/hash. Instantiate a concrete C only from usable observed/proposed/confirmed choices. Link those choices through C.ch. An unresolved canvas can remain I while a raster F has no C and its sample task is blocked.
5. Declare Q criteria appropriate to the question and destination. Include explicit observable conditions, domain and required evidence mode. Mechanical properties, visual readability, temporal/neighbor continuity and engine behavior are separate where applicable. Do not add irrelevant gates to a report or impose a universal art style. Save this plan before interpreting candidate results: new pass/fail verdicts require the same plan and semantic scope in the prior saved revision.

The bundled [incomplete intake example](../../../resources/examples/intake/project.px) shows declared choices, a planned output and requirements without a fabricated artifact. It is a syntax example, not a project-approved style or a finished sample.

Host adapter example for one unresolved choice (add a real P reference and actor; this is one record, not a complete document):

```json
{"id":"canvas","kind":"I","fields":{"pr":{"$ref":"project"},"wh":{"$ref":"user"},"ky":"px","st":{"$symbol":"unresolved"},"vl":null,"so":[],"wy":"The final canvas size has not been chosen."}}
```

Use symbols and references as tagged values. Wire literal byte counts come from `encode`, not hand counting. A confirmed choice needs supporting S; a proposal can retain a rationale before evidence exists. Available record hashes come from `validate`, so E bindings use actual canonical identities rather than guessed digests.

## Produce, inspect and retain the candidate

Run `workflow STATE --root PROJECT_ROOT` or `pixl_workflow`. Resolve only the task's actual blockers. Sample work can investigate a proposed contract; production/delivery cannot treat that proposal as confirmed. Use the [production procedure](production.md) for authorized real tool execution. Missing tools leave the plan and local work useful; they do not supply a generated asset.

Retrieve the actual candidate and store it under a new project-owned path. Record X with its byte hash, matching contract/kind, and `of` pointing to F. Nominate it through T.ca. Preserve older candidates when revising. Run applicable measurements, visually inspect the actual file/reference comparison, and execute required engine checks when available. Record an unavailable engine check as unavailable, not a pass or an artistic failure.

For a saved raster candidate, use the [candidate inspection operation](inspection.md) to prepare exact native/enlarged views and retain an explicitly supplied review. It resolves the current plan and publishes the observation report with the required E/V bindings. The host still needs to view the actual images; preparation alone is unperformed review.

For evidence outside that operation, retain the actual observation file and create E with its hash, timestamp, outcome, mode and full semantic bindings for both X and Q. Those bindings include the plan, contract, linked choices and sources. Then add V naming the task/candidate/criterion, reviewer, status, reason and E references; retain it in T.vr. `workflow` shows any absent verdict as unperformed. A local size/palette measurement cannot satisfy a Q requiring visual or live evidence.

An unavailable V has `ev=[]` and a concrete reason. For example, a target project is absent, so its import behavior remains unknown. A failed V retains what was actually wrong. A current passing V is only the result for its exact candidate and criterion. Generic encoding cannot determine whether a claimed visual review truly occurred; the acting agent must inspect before making that claim.

## Revise, finish or leave a resumable boundary

- If a candidate fails, keep X/E/V, create the revised X and nominate it. Evaluate the new candidate against the saved criteria; it cannot borrow old bindings.
- If correcting a verdict, supersede the old V with `ob=true` and add a new V. Do not rewrite its previous outcome or reviewer. Supersede E only when its own observation is invalidated or replaced.
- If the plan, relevant choice or contract changes, preserve the change rationale/sources, reopen affected completed work, and supersede stale E/V. Commit the changed plan before publishing new evaluation. Do not merely recompute old receipt hashes.
- After all saved criteria pass, use `task-complete STORE TASK CANDIDATE... --expect HASH --root ROOT` or `pixl_task_complete` to nominate the explicit accepted candidates and finish the task. It validates existing acceptance, preserves every failed candidate/verdict, and publishes the legal state transitions; it does not supply a missing review. Read `workflow` afterward to confirm the durable result. [Operation contract](../../../resources/spec/task-completion.md).
- Mark T done only when all its nominated outputs satisfy every declared criterion and all prerequisite tasks are done. A mechanically valid but visually rejected sample stays unfinished. Deliver useful files while keeping an unavailable engine requirement explicit; do not label them fully accepted for that destination.
- Commit state and leave a handoff with the next task or unresolved requirement. A cold session starts with `workflow` and the focused `context`, inspecting retained observations before repeating work.

This operation ends with either a representative sample accepted against its actual requirements, or a concrete retained boundary: missing choice, failed candidate, unavailable inspection, or next proof. Explain that useful outcome plainly; keep hashes, record IDs and mechanical details in evidence unless they clarify a conflict.

If the next dependent step needs a consequential user choice, the final response must contain the useful progress saved, a direct concise question for the smallest set of necessary answers, and what those answers unlock. Carry a still-unanswered question into that final response even when it was asked earlier or saved in the handoff. Present genuine alternatives when helpful and keep suggested trials labeled as proposals. Reference dimensions remain observations until adopted for this project. Continue authorized work that is independent of the answer. When the necessary choices are already supplied, use them and report the next operation under the existing authorization.

When the representative sample is accepted and the assignment continues across a family, enter the [family and delivery operation](family-delivery.md). It records the exact nominated sample as the baseline, saves member and destination plans, and declares collective continuity before batch results. Replaced/rejected samples and unknown provider attempts must be reconciled before dependent production; an old artifact's existence is not baseline eligibility.
