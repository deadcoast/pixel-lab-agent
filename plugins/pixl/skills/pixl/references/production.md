# Production procedure

Read this when creating, reviewing, or integrating assets. The [profile](../../../resources/agent/PROFILE.md) defines the full contract.

For incomplete intake, sample planning, criterion verdicts, revision and cold resumption, use the concrete [PX2 intake/sample operation](intake-sample.md). It defines the saved-state steps that support this production procedure. Keep existing PX1 projects in their declared version.

For an approved sample, multiple related members, collective continuity or delivery, use the [family and delivery operation](family-delivery.md). It defines saved baseline/member/destination plans, comparison in playback or neighborhoods, rejected revisions, retained copied files, and the exact unfinished destination checks a cold session must resume. A family snapshot creates a candidate; its acceptance remains a separate review.

## Intake to a useful proof

Inspect the user-provided references and existing assets, including their actual dimensions. State the asset's gameplay role and destination. Resolve only decisions that affect this task: native canvas size, projection, silhouette, color/ramp policy, edge treatment, lighting, transparency, directions, frame timing, anchors, tile boundaries, and renderer/import rules. Do not make a generic checklist into a mandatory style.

For each consequential choice retain WHO owns the constraint or result, WHAT will change, WHERE it is applied, and WHY the source or evidence supports it. A choice can come from the user, existing project material, observed visual references, documented tool limitations, or an explicitly identified proposal. Every recorded UDL decision must include research references and applicable executed proof receipts as defined by the specification. Researched knowledge can remain without executed proof until adoption. When sources conflict, identify the conflict and resolve it before dependent execution.

For unfamiliar methods or uncertain output quality, define a focused proof of concept:

| Field | Required meaning |
| --- | --- |
| Question | One uncertainty that affects the planned asset family |
| Method | The researched tool or technique and source that supports it |
| Smallest artifact | A representative pose, cycle, seam neighborhood, rig assembly, or import fixture |
| Acceptance | An observable test stated before interpreting results |
| Result | Artifact path/hash, measurements, visual observations, and pass/fail/uncertain |
| Consequence | Proceed, revise, or stop the dependent batch and why |

Examples: prove diagonal tile joins with a repeated neighborhood; prove a walk cycle's grounded contact and pivot stability before producing all directions; prove material-color response and occlusion separately before promising dynamic sprite lighting. A proof must exercise the disputed behavior. A prose plan alone is not a proof of concept.

## Remote operation

Use [PixelLab operation selection](pixellab-operations.md) to match the deliverable and each reference role to supported arguments. Carry actual image data/handles, not merely file names in text. Use [the delegation contract](delegation.md) for work received from and returned to another agent.

Read the tool schemas actually available in the session and the relevant current [PixelLab MCP documentation](https://api.pixellab.ai/mcp/docs). Record which surface is being used and the evidence date; cached examples do not establish current availability. Check prerequisites and map the selected UDL contract to supported tool arguments. Preserve references and values that the selected tool can express; report any constraint requiring later editing or inspection.

Follow the [provider submission and recovery operation](provider-recovery.md) for new PX2 work: save the exact request and plan, claim dispatch locally before one actual PixelLab call, retain returned identifiers and observations, and reconcile unknown outcomes before any new attempt. Import downloaded bytes as candidates, then evaluate them separately. Existing authorization and budget govern real calls. Do not synthesize progress or convert elapsed time into a completed state.

## Artifact acceptance

Retrieve the actual artifact before evaluating it. Record provenance, returned identifiers, local path, content hash, and contract version. Use `asset-check` for the dimensions and any palette constraint the project actually requires. Supplement it with appropriate format/frame/alpha checks; check `--help` and the current runtime output to establish its exact coverage.

Inspect native-scale readability and enlarged clusters. Evaluate identity and style across the asset family. Inspect animation in playback as well as individual frames, and tiles in repeated neighborhoods. Mechanical checks cannot measure all these properties. Keep the visual verdict separate from tool measurements and do not mark an unviewed artifact visually approved.

In the destination engine, validate applicable import sampling, pixel/display scale, alpha edges, atlas padding, pivots, frame slicing, timing, direction mapping, material and lighting behavior. If the engine is unavailable, deliver the artifact with an explicit unverified import requirement. Preserve any failed trial separately from the accepted revision and explain the change that resolved it.

Finish with the useful outcome, artifact links, source/contract identity, observed job state, concise verification evidence, known limitations, and next dependency. Update production state through the runtime so a later agent can resume without repeating remote generation or losing unresolved issues.
