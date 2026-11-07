# Matching lantern production approach

Prepared 2026-09-14. Deliverable: this Markdown plan only. The user explicitly excludes PX2 initialization or amendment, production art, and provider calls from this evaluation. Those production steps are future work, not prerequisites for completing this report.

Recommend a small lantern built from clear structural clusters, with intentional partial transparency and selectively authored anti-aliasing. A front-facing 32 × 32 trial with a dark frame, cool glass, and a warm light is a useful starting experiment. Its size, construction, and colors are proposals; successful matching remains untested.

## Reference review

Inspected `SESSION.md` and `translucent-reference.png`, using the packaged PIXL skill and local read-only tools. Viewed the original at native resolution and 12× nearest-neighbor enlargements composited in memory over dark RGB (24,24,32), light (240,240,240), and middle gray (128,128,128). No inspection images were saved. These backgrounds are diagnostic choices, not supplied game backgrounds.

The reference has a broad, flat teal interior within a dark navy structure, two upright upper extensions, and two pale warm rectangular accents. The largely frontal appearance and sparse shading suggest a compact, graphic construction. The image alone does not establish material identity, a light direction, or whether its pale accents emit light.

Measured reference facts, using zero-based pixel coordinates:

| Property | Observation |
| --- | --- |
| Canvas | 32 × 32, one frame |
| Occupancy | 420 pixels with nonzero alpha; bounding box x=6–25, y=3–27 inclusive |
| Transparent / opaque / partial | 604 / 390 / 30 pixels |
| Visible RGB colors | Navy `#25354A`, teal `#56B5BC`, pale warm `#F4DDA2` |
| Visible RGBA combinations | Five: the three opaque colors, plus teal at alpha 96 and 160 |
| Partial-alpha placement | Fifteen pixels at x=6, y=11–25, alpha 96; fifteen at x=25, y=11–25, alpha 160 |
| Connectivity | One component under the checker's four-neighbor, nonzero-alpha definition |

The softened side strips change appearance with the composite background; the core remains opaque. This supports preserving localized edge treatment. The reference does not demonstrate a rounded handle or a translucent glass interior. The user's description establishes intentional partial transparency and selective anti-aliasing regardless of whether a viewer interprets these strips as coverage, glow, or another effect. Neither treatment is replaced by a generic glow instruction.

Reference SHA-256: `bda5c9b18e38b60a617877de6e9df6c5bf8e040410e9dfbe6bc85ca501b17132`. PIXL `asset-check` ran with `alpha: "full"` and no palette or dimension restrictions. Its pass reports mechanical inspection only; it does not establish visual or engine acceptance.

## Authority and scope

| Property / value | Status and owner | Exact source | Applicable scope |
| --- | --- | --- | --- |
| Small matching lantern | User requirement | Brief: “prepare a production approach for a small matching lantern prop” | Planned asset identity and relationship to reference |
| Intentional partial transparency and selective anti-aliasing | User requirement | Brief: “uses intentional partial transparency and selective anti-aliasing. Keep that treatment in the new props.” | Sample instructions, authoring, review, export, and fallback |
| No fixed palette imposed | User-specified freedom | Brief: “I have not imposed a fixed palette.” | No exact palette membership or color-count rejection rule |
| Markdown only; no state, art, or provider action | User requirement | Evaluation instructions in this conversation; project scope in `SESSION.md` | Current execution |
| Dimensions, RGB/alpha values, counts, and locations above | Measured observations | Exact reference bytes identified above; local measurement | Reference description only |
| Graphic clusters, frontal appearance, cool body with warm accents | Visual observations / interpretation by PIXL | Native and enlarged reference views described above | Qualitative comparison, not an adopted projection or numeric color threshold |
| 32 × 32 front-facing sample; handle, cap, glass chamber, base; dark/cool/warm material roles | PIXL proposal | This report's recommendation, informed by reference review | Optional first experiment; no production rejection for choosing another matching design |
| Partial-alpha panes and selected edges; AA on handle/shoulders | PIXL proposal for fulfilling required treatments | Brief's treatment requirement plus `selective-edge-aa` research below | Proposed locations; reference coordinates and alpha levels are not prescribed |
| RGBA PNG master, straight-alpha working interpretation, point-sampled previews | PIXL technical proposal | `alpha-contract` and `selective-edge-aa`, with limits below | Future trial and export verification; engine behavior remains unknown |
| Final canvas, on-screen size, game backgrounds, renderer/import settings | Unresolved project choices | Not supplied in the inputs | Final production and destination-specific review |

## Proposed representative sample

After a separate production assignment, make one lantern study before extending the prop family. The question is whether a recognizable new lantern silhouette can retain both requested treatments at the intended display size.

1. **Construct the form.** Trial a front-facing 32 × 32 canvas with a compact handle, cap, glass chamber, and stable base. Use the reference's relative cluster density as a visual guide. The handle may be curved: lack of a curve in the reference is a reason to test it, not to prohibit it. Final canvas and occupied bounds remain open.
2. **Establish material relationships.** Trial a navy frame, teal glass, and pale amber light. Add or shift colors where they improve the match and readability. No extracted palette lock, maximum color count, numeric hue tolerance, or mandatory ramp length applies. A warm luminous center is a proposed lantern lighting intent, not a measured property of the reference.
3. **Author partial transparency.** Put intentional intermediate alpha in portions of the proposed glass and selected outer transitions, while retaining substantial structural clusters. Tune opacity by viewing composites; alpha 96 and 160 are reference evidence, not the only allowed values. A glow may be explored, but it does not substitute for deliberate transparency and selective AA.
4. **Author selective AA.** Place individual coverage or intermediate-color pixels along chosen handle curves and cap/shoulder transitions. Judge their relationship to the darker frame and glass. Compare with untreated edges to keep the effect selective. Use actual alpha for edges that meet changing backgrounds where appropriate, rather than baking in one diagnostic background color. Exact edge masks and protected pixels belong to this study, not the entire family.
5. **Review the combined result.** Compare the lantern and reference at native size and integer enlargement on the same backgrounds. Inspect readability, cluster hierarchy, glass/body separation, partial alpha, and localized AA together. Use the actual target size and game backgrounds once supplied. Revise this sample before making variants.

Suggested future artist/provider instruction, **an unsubmitted experimental prompt with proposed choices labeled here**:

> Create a small lantern prop matching translucent-reference.png. Preserve its intentional partial transparency and selective anti-aliasing as authored pixel treatments. Keep the lantern recognizable at its intended display size and compare its cluster structure and softened edges with the reference. There is no fixed palette. Proposed first experiment: a 32 × 32 front view with a compact handle, dark frame, cool glass, and pale warm light. Author partial transparency in selected glass regions and outer transitions, and selective anti-aliasing on the handle and cap/shoulder contours. These dimensions, hues, construction details, and treatment locations are trial choices, not mandatory reference rules; adjust them to improve the match while retaining both requested treatments.

This prose is not a discovered provider request schema. No provider was contacted or evaluated. If a provider is used later, discover its actual capabilities and determine which treatment needs local authoring before submission; do not assume the prompt guarantees faithful alpha or AA.

## Planned checks and response to a failed attempt

The following are future review instructions, not results or production acceptance in this evaluation.

| Review | Evidence and scope |
| --- | --- |
| Lantern identity and matching treatment | Visual comparison at intended size: recognizable lantern; coherent cluster scale and edge treatment relative to the reference. Record concrete discrepancies, not an invented numeric similarity threshold. |
| Partial transparency retained | Inspect RGBA values and corresponding visible regions. Confirm intentional pixels with 0 < alpha < 255 survive export and contribute to the intended appearance. Nonzero partial-alpha count alone does not prove artistic success. |
| Selective anti-aliasing retained | Identify authored transition pixels on the chosen contours at enlarged scale, then judge their effect at native size. A count of intermediate colors cannot establish AA quality. |
| Compositing diagnosis | Compare light, dark, and gray composites for distracting fringes, disappearing detail, and changes in material readability. Conclusions apply to that candidate on those backgrounds at those scales. Target-background suitability remains unverified until those backgrounds are supplied. |
| Mechanical report | Measure dimensions, alpha, colors, bounds, and components with full alpha allowed and no palette argument. Size checks become rejection rules only if a final size is adopted. Color count, reference opacity values, component count, and gaps remain diagnostics. |
| Future destination verification | Trial an RGBA PNG master and explicit straight-alpha interpretation, then verify the actual renderer's blend model, color-space handling, sampling, and export/import round trip. Point sampling is a proposed way to preserve authored texels, not a ban on authored AA. |

Failure to retain either requested treatment warrants revising that candidate. A new shade, alpha level, curved handle, different outline thickness, intentional detached detail, or different occupied bounds is not by itself a failure. These are examples of brief-compliant variations that prevent reference measurements from becoming extra restrictions.

If a candidate lacks intentional partial transparency or selective AA, retain it as an unsuccessful attempt and explicitly author the missing treatment in suitable regions. Opaque glass alone is not a failure if the required partial transparency is successfully expressed elsewhere; glass transparency is a proposed location. If composites show a fringe, first examine authored edge colors and alpha interpretation, then revise the affected pixels and repeat the relevant views. If a curve reads poorly, adjust its clustering or trial another handle shape while preserving both treatments. Do not infer a minimum canvas or a universal ban on curves from one failed design. A failed provider result establishes that attempt's failure, not general provider inability. Exact palette quantization and binary-alpha cleanup are not fallbacks for this brief.

## Research provenance and applicability limits

Local source discovery verified the installed inventory's byte identities. Retrieved both method entries and complete compiled contexts from `.agents/skills/pixl-kit/resources/knowledge/library.px`, without creating project state. Resources below are relative to `.agents/skills/pixl-kit/resources/`.

| Method | Exact source inspected | Transfer to this plan |
| --- | --- | --- |
| `selective-edge-aa` | `training/original-docs/PIXEL-ART-DEEP-RESEARCH.md`, lines 590–632 and 907–919 | Supports authored coverage cues and distinguishing them from runtime filtering. The strict-palette branch does not apply to this open-palette brief. Edge selections and representative game backgrounds are still to be established. Byte-identical protected edges and palette checks in its fixture are not imported as production requirements. |
| `alpha-contract` | Same document, lines 945–977 and 1276–1291; `training/original-docs/PIXEL-ART-ASSETS.md`, lines 942–958 | Curated recipe separates RGB palette from alpha and calls for consistent compositing. The cited passages discuss asset channels, companion alignment, and a CSS effect; they do not directly establish a complete straight/premultiplied-alpha pipeline. Treat the export choice as a proposal requiring an actual round trip. Its binary-alpha check is inapplicable here. |

Source identities: deep-research SHA-256 `7efc4789ca70dfd9964abc2bc1100af318306236400e3496f7a0a5654f725e28`; asset-archive SHA-256 `450a335ed6563a7f4a5cc380f2bbe72f98b70e532ac2c8d16a679bcc545d4900`. Historical external citation tokens in these documents were not independently verified and supply no claim about current engine or provider behavior.

Read the bundled receipt `evidence/art-methods/poc-report.json`, SHA-256 `5d27f3e14a7aba09860956d9ae100146e8e28f7d5dfc7542f51ed4f52538d680`. Its recorded `selective-aa-boundary` pass proves bounded edit locality and fixture palette compliance, not perceptual quality or arbitrary-background suitability. Its `alpha-compositing-contract` pass proves a linear numeric example and alpha-policy checks, not display transfer functions, GPU blend state, or an importer. These are existing offline fixture results, not newly executed lantern proofs. No production method or sample has been accepted here.

## Handoff

The planning deliverable is complete. The next production decision is the lantern's intended on-screen size and representative background or scene; that will guide final canvas choice and meaningful transparency/AA review. A 32 × 32 study on the diagnostic backgrounds is the proposed starting point if those choices remain open, with destination suitability explicitly unresolved. No palette decision is required to proceed with that future study.

Whole-file authority review covered the recommendation, experiment, prompt, checks, and fallbacks. It corrected one fallback sentence that could make the proposed glass-transparency location mandatory; the complete earlier draft is retained in the session's file readback. Artistic restrictions derive from the user's matching and treatment requirements; added design choices remain proposals, and measurements remain observations. No remaining conflict with the brief was found. The research citation limitation above remains unresolved for production adoption. This report provides a reviewable approach without claiming lantern quality, provider reliability, or engine acceptance.
