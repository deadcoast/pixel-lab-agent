# PixelLab operation and reference selection

Start with the [official documentation](https://www.pixellab.ai/docs) and [complete MCP tool guide](https://api.pixellab.ai/mcp/docs). Discover the actual connected tool declaration for the selected operation. Documentation across the web/editor/MCP/REST surfaces can describe different input limits and output packaging. Match the surface, not just the marketing name.

Prefer the connected official PixelLab MCP tools for agent production. Use the existing HTTP adapter when that explicitly selected route supports the task; its single image endpoint does not represent the full platform. A missing MCP tool does not justify guessing a REST endpoint or silently choosing a weaker operation.

## Choose by the deliverable

The names below are discovery starting points, not a frozen callable catalog.

| Need | Discover and evaluate |
| --- | --- |
| Small standalone sprite, item or UI icon | Freeform image tools, including Pixen, Pixflux and Pro/Pro Flash; compare exact canvas, image conditioning and output count |
| UI panel, frame or component set | UI asset tools; examine pieces/states, border geometry and current canvas limits |
| Pixel font | Font creation and retrieval; verify required glyphs, atlas/TTF delivery and actual text rendering |
| Character identity across directions | Character tools, existing-character state operations and supplied direction support |
| Object/environment prop across directions | Object tools and object-state variants |
| Motion | Character/object animation for an existing resource, or image animation for loose sprites; preserve timing, anchors and frame/direction expectations |
| Terrain | The matching top-down, sidescroller, isometric or tile tool; reuse connected base tiles and validate adjacency |
| Repair or variation | Edit/inpaint or state operations on the existing source; identify exactly what must remain unchanged |
| Material response or authored effects | Normal-map and pixel/VFX workbench tools when the assignment needs those outputs |

Do not choose a tool merely because “UI” or “character” appears in the task. For example, an icon's native canvas can be smaller than a UI panel operation accepts. Generate at the appropriate native scale or explain a proposed adaptation; resizing an oversized result is not automatically equivalent pixel art.

Inspect output cardinality before submission: a candidate grid, eight directions and one image are different deliverables. Do not order additional variants just because a mode returns them. Query capability/quote tools where available; preserve their provisional meaning and the user's current limits. No cached price or old tool inventory establishes the current charge or entitlement.

## Preserve reference meaning in actual arguments

Assign each visual input a role before selecting the operation:

| Role | Preserve |
| --- | --- |
| style | Art language: selected palette/ramp behavior, outlines, shading, detail and cluster scale |
| identity | The particular subject, costume, silhouette or already approved sprite |
| pose | Orientation, gesture, contact and anatomical placement |
| layout | Spatial arrangement, UI pieces, safe areas or composition |
| palette | Explicit color choices when adopted, rather than incidental reference measurements |
| mask | The actual region to change/preserve with the selected tool's mask semantics |
| motion | Timing/pose sequence or motion reference |

PLAR's optional `references` entries record `source`, `role` and `instructions`. Sources bind actual project files; selected context carries their current identities. A source citation or a filename written in a text prompt does **not** transmit an image to PixelLab.

Inspect the chosen tool's image inputs. For an image on disk, discover `get_upload_url` first when the operation accepts an image URL. Follow its returned upload instructions to send the file bytes directly (for example, multipart `curl -F file=@PATH`; `curl.exe` on Windows), parse the actual response, and use its returned `upload:<id>` in the corresponding image URL field. Bind that handle to the original local hash and role in the reviewed request. Keep the temporary upload URL out of delivery artifacts. This avoids model transcription of encoded image data; manually pasted base64 can corrupt even a small PNG.

Transfer the actual image via its supported upload URL/handle, owned source ID, URL or encoded payload. Use `get_upload_url` and its returned instructions for local images when available; prefer supported handles/URLs to large inline base64. Keep the local source hash, its role, the returned handle and the exact request field associated in production evidence. Upload handles are temporary transport references, not durable replacements for local source files.

Use the role-specific input: a style anchor is not necessarily a subject/pose source, and an init image can influence composition as well as appearance. Reusing an approved character or object ID can preserve identity more directly than describing it again. For Pro Flash, inspect current native sizes and style-image fit; the style anchor and content-reference count are distinct concepts. Reuse the chosen family anchor and relevant controls across members, then inspect the actual results.

If the chosen operation cannot express a required reference role, select a supported operation or propose a concrete staged workflow. A text-only fallback needs to be identified as an approximation; do not present it as equivalent reference conditioning. Avoid adding an unrelated exact-palette restriction merely because a style image has a small measured color set.

The [style-reference workflow](https://www.pixellab.ai/docs/tools/consistent-style) explains style consistency, while [init-image options](https://www.pixellab.ai/docs/options/init-image) explain image-guided generation. Their editor controls do not substitute for the live MCP input schema. The [UI workflow](https://www.pixellab.ai/docs/tools/create-ui-elements-pro) informs design intent; verify the actual MCP UI operation's limits independently.

## Run and review

Use [provider recovery](provider-recovery.md) for saved intent and actual calls. Capture returned IDs, use the matching retrieval tool, and use bounded `wait_for_jobs` when appropriate instead of blind repeated polling. Retrieve actual output files before inspection.

Review the asset's intended function at its display size: state readability for UI, identity and volume across directions, timing and contact in playback, adjacency in terrain, and alpha/material behavior in the target renderer. Keep source art and failed candidates. Prefer a targeted edit of a nearly correct result when it preserves the required identity; do not erase the original.

Return the [caller result](delegation.md) with files, checks, remaining questions and real provider/state identifiers. The platform creates candidates; the specialist supplies design judgment and evidence of fit.
