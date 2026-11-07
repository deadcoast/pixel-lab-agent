# Robot directional production plan

Planning deliverable completed on 2026-11-07 for `robot.directions`.
Requirements snapshot: `3bf04398cf4441a8c981b68a15c5f3dbadfd6294b80e22277fd4fa50819baf1b`.

This is an unexecuted production plan. No image was uploaded, no PixelLab operation was called, no generated candidate was obtained, and no delivery PNG was created. The approved identity is approval within the supplied example only; BRIEF.md explicitly describes the source as a retained fixture.

## Evidence and authority

Read BRIEF.md, src/robot.ts, README.md and the focused ../assignment.json packet, including the robot.base dependency and its identity reference. The three source hashes match that packet. See [source-inspection.json](source-inspection.json) for measurements, and [source-native-and-8x.png](source-native-and-8x.png) for the actual viewed inspection composite.

| Property | Authority | Application |
| --- | --- | --- |
| Same subject, proportions, palette and unchanged south sprite | Requirement: BRIEF.md:3 and robot.base dependency | Reference input, description and family review; south delivery uses unchanged local bytes. |
| Four views: south/east/north/west | Requirement: BRIEF.md:3 and src/robot.ts:1-5 | n_directions=4; label-based mapping to the four controller paths. |
| Separate 32×32 transparent PNGs under assets/robot/ | Requirement: BRIEF.md:3 | Output plan and mechanical checks; no size adaptation is assumed. |
| Nearest sampling | Requirement: src/robot.ts:6 and assignment packet | Engine import and rendering; not a PixelLab creation parameter. |
| Flat front-facing boxlike cyan/navy subject, two cream eyes, two upright prongs; no visible arms or legs | Visually observed at native size and 8× nearest zoom | Describe the supplied identity without redesigning it as a generic humanoid robot. |
| Three visible RGB colors: #25354A, #56B5BC, #F4DDA2; alpha values 0/255; occupied bounds [7,3,25,28) | Measured observations | Compare output palette and placement. Do not turn color count, exact occupied width, or binary alpha into new universal constraints for unseen directions. |
| Eye-level camera, provider view="side" | Proposed interpretation: no top plane or depth cue is visible | Explicitly labeled in the prepared request. Confirm against eventual camera context; do not silently adopt the provider's low-top-down default. |
| Hidden side/back surfaces and depth | Unspecified by front-only source | Infer minimally for the trial, then review continuity. No reference establishes exact rear design. |
| Pivot and runtime scale | Unknown: controller only declares cell/sampling | Inspect alignment in the 32×32 cells; final engine behavior remains unverified. |

Native and enlarged inspection showed a horizontally balanced, straight-on front, not a three-quarter sprite. This supports using the provider's south-reference convention. The image does not establish a perspective camera or a full three-dimensional design.

## Operation and input mapping

Use the discovered official host tool `mcp__pixellab__create_character` with `mode="v3"`, `n_directions=4`, and the actual PNG in `reference_image_base64`. The saved [request-v3-base64.json](request-v3-base64.json) contains the real 177-byte PNG as 236 base64 characters; decoding it reproduces source SHA-256 `d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7`. The local file path is provenance, not a provider image handle.

The current MCP documentation supports the four cardinal views with a v3 reference, uses reference dimensions when size is omitted, and treats that reference as south. Concept-image and style-only inputs have different roles. [Official MCP guide](https://api.pixellab.ai/mcp/docs)

The exact live declarations inspected in this session are retained in [provider-tool-declarations.json](provider-tool-declarations.json). The complete argument-to-requirement account, omitted controls, output mapping and upload alternative are in [provider-input-mapping.json](provider-input-mapping.json).

For this tiny native image, inline base64 is concrete and bounded. For an upload route in a later authorized run, call the discovered `get_upload_url({})`, follow its returned file-transfer instructions, record the actual returned `upload:<id>`/supported URL, and replace the base64 field with `reference_image_url`. No upload handle exists now. Do not send a Windows path, a fabricated upload ID, or both image fields.

Leave size omitted because the source is already 32×32. Leave direction_images omitted because no other approved directions exist; that schema has no south key. No new seed, no_background or palette-enforcement argument is invented. Palette/max_colors are documented as Pro-only on create_character, so the selected v3 path carries palette through the actual image and description and requires checking the result. No claim of exact palette preservation is made before that check.

The tool's default body type is humanoid. The proposed request avoids adding a body template and explicitly preserves the source's boxlike silhouette without added anatomy. Whether v3 follows this unusual form is a representative-trial uncertainty.

The editor's eight-view Pro workflow is a different surface and packaging contract. It does not justify requesting extra directions here. [Editor rotation documentation](https://www.pixellab.ai/docs/tools/create-8-rotations-pro)

## Future production sequence

1. Recheck source hashes and the focused requirements. Carry forward the next assignment's actual execution authorization and spending limits. This planning assignment supplies none.
2. Start the authorized PX2 task, output plans and saved criteria using the copied kit. Read its state-authority, provider-recovery and family-delivery references at that point; use the current state hash. This local JSON request is not a saved job-prepare or dispatch claim.
3. Resolve whether the proposed eye-level camera fits the intended renderer. Preserve the source front and evaluate the minimal inferred depth/rear treatment in the trial.
4. Prepare this exact source-conditioned request against its task/output plans; retain schema/discovery and authorization evidence. Use job-prepare and job-dispatch before one host call. If using upload transport, bind the actual handle to the same source hash before dispatch.
5. Treat the one four-view set as the smallest supported family trial. There is no one-direction cardinal request in this schema. Do not begin animation, diagonal variants or additional batches.
6. Retain the actual returned character/job identifiers. Inspect only observed status with get_character(character_id); follow reported polling guidance. Reconcile an unknown outcome before another paid submission.
7. Retrieve actual named rotation images or the returned download package. Preserve raw output and metadata under a candidate directory. Inspect the names; the documentation's listed order differs from the controller's display order, so never map by list position.
8. Deliver south by copying the approved local source bytes to assets/robot/south.png. For east/north/west, use the correspondingly named accepted candidates. If provider south differs, retain that mismatch as evidence while using the approved source for delivery.
9. Review mechanical and visual criteria below before any further production. Retain failed candidates. A palette or silhouette failure calls for a targeted correction of that observed candidate within the next authorized scope; it does not establish general provider failure. Do not automatically resize, mirror, or recolor outputs and declare acceptance.
10. When a runner exists, verify imports and exercise all four controller states. Record any unavailable or failed checks. Provider completion alone is not artistic or engine acceptance.

The rotation guide warns that successive rotations can accumulate errors and discusses targeted corrections; this plan keeps one fixed source identity for the first trial. [Official rotation guide](https://www.pixellab.ai/docs/guides/rotating-a-character)

## Predeclared acceptance for the future trial

| Evidence class | Check | Present status |
| --- | --- | --- |
| Mechanical | Exactly four named individual static PNGs, each 32×32, readable alpha channel and transparent background. Do not substitute a contact sheet. | Planned; no output candidates. |
| Mechanical | Delivered south SHA-256 equals the source hash above; the source itself remains untouched. | Planned; only the source has been measured. |
| Mechanical + visual | Compare visible RGB values with the source palette, record introduced colors and inspect whether they violate the requested palette preservation. No new numerical color-count cap is adopted. | Planned; v3 has no selected exact-palette control. |
| Visual | Native and enlarged comparison: same subject and proportions, appropriate occlusion of eyes/prongs, coherent volume and rear treatment, readable cardinal turns, no added humanoid anatomy or redesign. | Planned; no rotated candidate inspected. |
| Visual continuity | Review all four together on light/dark backgrounds; consistent canvas placement and apparent scale without clipping or directional jumps. Occupied width can legitimately change during rotation. | Planned; pivot not established by consumer. |
| Integration | Resolve every spriteFor facing to its named path; confirm nearest sampling, transparency, scale and facing selection in the real renderer. | Unavailable: no runner or engine project supplied. |

## Caller handoff

The assignment is **delivered for planning**. The exact local request is not submitted and contains one explicitly proposed camera setting. There are no remote IDs, charges, generated outputs, accepted rotation results or PX2 provider attempts to resume. Resume from this plan and mapping when a production assignment supplies execution scope. Questions are unnecessary to complete this plan; future production must resolve camera context and later test hidden geometry and renderer behavior.

Before handoff, the entire plan, request and mapping were reread together against the authority table. Observed color count/alpha/bounds remain observations, proposed camera/backside remain proposals, and the explicit palette, identity, frame and controller requirements remain in the prompt and review criteria.

