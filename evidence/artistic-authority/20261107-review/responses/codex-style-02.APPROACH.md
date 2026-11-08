# Matching lantern production approach

## Scope and conclusion

Plan one small lantern matching `translucent-reference.png`. Preserve intentional partial transparency and selective anti-aliasing as authored treatments. No fixed palette is required. This document is the sole deliverable: no PX2 state, production art, provider request or production acceptance is created here.

## Authority ledger

| Property / value | Authority | Exact source | Scope |
| --- | --- | --- | --- |
| Small matching lantern | Requirement | User brief, “small matching lantern prop” | Proposed prop |
| Preserve intentional partial transparency and selective anti-aliasing | Requirement | User brief, “Keep that treatment in the new props” | Authoring, request, review and fallback |
| No imposed fixed palette | Requirement / open choice | User brief, “I have not imposed a fixed palette” | No exact palette-membership rejection check |
| 32×32 RGBA; dark frame, teal body, pale warm marks | Measured / visually inspected observation | `translucent-reference.png`, whole image | Reference only; informs matching judgment |
| Teal side strips with alpha 96 and 160 | Measured observation | Reference x=6 and x=25, y=11–25, zero-based | Reference only; not a required alpha set or placement |
| Front-facing, static 32×32 canvas; dark frame, cool glass and warm light | Proposal | This approach | First representative experiment; not approved project convention |
| Rounded handle with selected softened edges; translucent glass | Proposal serving required treatments | This approach + user treatment requirement | First lantern sample; exact geometry remains adjustable |
| Intended display size, scene background and engine blend behavior | Unknown | Not supplied in project inputs | Resolve before production acceptance or engine-ready claims |

## Reference review

Inspected the original through the host image viewer and a temporary in-memory 16× nearest-neighbor enlargement composited over light gray. No preview files were saved. Pillow decoded the supplied PNG as 32×32 RGBA (1,024 pixels):

- 604 fully transparent pixels.
- 180 opaque dark pixels, RGB (37, 53, 74).
- 186 opaque teal pixels, RGB (86, 181, 188).
- 24 opaque warm pixels, RGB (244, 221, 162).
- 15 teal pixels at alpha 96 and 15 at alpha 160.

The image has a compact rectangular dark frame, two upper projections, a broad teal interior and two small warm rectangular accents. The partial-alpha strips run along the outside of the body frame; the interior teal is opaque. These are observations, not evidence that a lantern must copy the silhouette, pixel counts, symmetry, colors, outline width or strip arrangement. The user establishes selective anti-aliasing as intentional; measurements locate alpha but do not alone determine each pixel's artistic function. The visual read is deliberately simple, with dark structural contrast and restrained warm accents. Matching that hierarchy is an interpretation to test, not a guaranteed result.

Coverage limits: the original and light-gray enlargement were viewed; dark, colored and actual scene backgrounds were not reviewed. There is no lantern candidate or engine evidence.

## Proposed representative sample

Start with one static, front-facing lantern on a proposed 32×32 transparent canvas. Use a recognizable hanging handle, compact cap, glass chamber and stable base. Preserve enough negative space within the handle to read at small size. Use dark framing, cool glass and a small warm source as an initial color direction; allow hue and ramp adjustments rather than forcing the three opaque reference RGB values.

Author partial transparency in the glass chamber so a background can show through, with selective partial-alpha accents at the chamber edges. This extends the reference's treatment to a lantern material; it does not claim the reference interior is translucent. Keep a legible opaque structural frame and warm focal light in this experiment.

Author selective anti-aliasing along chosen handle curves and glass contours with purposeful intermediate coverage/color pixels. Keep other edges crisp where that supports the structure. A curved handle is a useful test of the treatment, not a reason to forbid curves. Do not apply a global blur or automatic smoothing pass. Conversely, do not impose a blanket ban on anti-aliasing, intermediate colors or partial alpha. An optional subtle glow may be explored later, but glow alone would not satisfy both required treatments.

## Future production procedure

1. Confirm the intended use and displayed size: inventory icon versus placed world prop can change silhouette, scale and anchor. The proposed front view and 32×32 canvas are a starting experiment, not settled requirements.
2. Before any paid operation, discover the actual authenticated PixelLab operation and current schema. Verify support for reference conditioning, dimensions, output transparency and reference input handles. The available local PIXL tools are not evidence of provider capability. Do not assume named parameters or reliable alpha generation.
3. Supply the actual reference bytes through a supported reference input, with its role explicitly described as style/treatment rather than identity or silhouette. A filename mentioned in prose is not reference conditioning. Keep all extra art choices labeled as proposals when preparing the real request.
4. Make one representative lantern before variants. Retain its RGBA source and inspect it before expanding the family. If a future provider output lacks the required alpha or selective AA, diagnose that candidate and locally author a corrected revision if suitable; do not flatten it or silently abandon the treatments. One failed attempt does not establish general provider inability.
5. Validate the corrected candidate again, then test its actual import and compositing in the target consumer before declaring it production-ready. Keep animation, emission maps and additional variants outside the first experiment unless requested.

### Proposed creative brief for that future sample

“Create a small lantern using the supplied image as a style and treatment reference. Preserve intentional partial transparency and selective anti-aliasing. Proposed first experiment: one static front view on a 32×32 RGBA canvas, compact dark frame, cool translucent glass, small warm light and a rounded hanging handle. Author selective AA on chosen curved/contoured edges and partial alpha in the glass and selected edge accents; retain clear structure at native scale. Colors may adapt to suit the lantern; no fixed palette or exact alpha set is imposed. Judge resemblance through simple clusters, contrast hierarchy and deliberate edge treatment, without copying the reference object's identity.”

This is a creative proposal, not an executable provider payload. Current capabilities, reference transport and output fidelity remain unverified.

## Review plan and decision rules

- **Required treatment:** verify actual pixels with 0 < alpha < 255 in meaningful authored regions, then visually inspect their compositing. Presence alone is insufficient: partial transparency must contribute intentionally rather than merely appear in stray pixels.
- **Required selective AA:** inspect chosen handle/glass contours enlarged and at native size. Confirm deliberate edge transitions and readable clusters. Do not require AA everywhere, forbid it everywhere, or mistake uniform resampling blur for selective authoring.
- **Required matching lantern:** assess whether the silhouette reads as a lantern at intended display size and whether structure, color relationships and detail density feel compatible beside the reference. Record the visual reasoning separately from pixel measurements.
- **Diagnostics, not automatic rejection:** report dimensions, alpha distribution, colors and connectivity. Do not reject a brief-compliant variation for different RGB values, more colors, different alpha levels, detached details, changed component counts or a different silhouette. Proposed dimensions/geometry become hard constraints only if adopted later.
- **Background test:** view native and nearest-neighbor enlarged candidates beside the reference over light, dark, saturated and actual scene backgrounds. Look for unintended matte fringes, glass disappearing, distracting edge bands or a blurred outline. Associate any failure with the tested candidate/background, not a universal aesthetic rule.
- **Consumer test:** verify actual texture alpha preservation and compatible straight/premultiplied blend handling, atlas bleed/padding and display sampling. Nearest-neighbor enlargement is a diagnostic here, not an imposed engine setting. No alpha clipping, quantization or flattening should erase the required authored treatment. Final import settings depend on the consumer.

## Next decision and audit

Before later production, establish intended use, display size and usual background; then confirm or revise the proposed front-facing 32×32 static sample. No palette decision is required now. A representative sample would test whether curved selective AA and translucent glass match this reference together; this plan cannot prove that outcome.

Whole-file audit: the creative brief, review rules and fallback retain both required treatments. Exact reference colors, alpha values, pixel counts and geometry remain observations; new geometry, size, materials and color direction remain proposals. No unsupported fixed palette, binary-alpha, zero-AA or exact component-count restriction is imposed. No unresolved conflict with the supplied brief was identified. This is a bounded reference review and production plan, not candidate or engine acceptance.
