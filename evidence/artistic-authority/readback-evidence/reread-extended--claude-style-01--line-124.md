# Production approach — small translucent lantern prop

Scope: planning only. No PX2 state was created or amended, no art was generated, and no
provider was called. This document is the deliverable.

## 1. What was actually inspected

| Input | Identity |
| --- | --- |
| `translucent-reference.png` | sha256 `bda5c9b18e38b60a617877de6e9df6c5bf8e040410e9dfbe6bc85ca501b17132` |

Inspected at native scale and at 16× integer-nearest scale, over both a plain and a
checkerboard background. The two enlarged views (`_view_reference_16x.png`,
`_view_reference_16x_checker.png`) are throwaway inspection aids, not deliverables.

Measurements (`pixl asset-check`, plus a per-pixel dump):

- Canvas 32×32 RGBA, single frame. 420 visible pixels, visible bbox `[6,3,26,28]`
  (content 20 wide × 25 tall; margins 6 left, 6 right, 3 top, 4 bottom).
- 5 distinct RGBA values over 3 distinct hues: navy `#25354A`, teal `#56B5BC`,
  pale gold `#F4DDA2`.
- Alpha levels present: `0`, `96`, `160`, `255` — nothing else.
- 30 fractional-alpha pixels, all teal, all in exactly two single-pixel vertical
  columns: `x=6` at α=96 and `x=25` at α=160, each spanning rows 11–25.
- `opaque_components: 1` (4-connectivity over nonzero alpha).

Structure, as read from the pixel map: a hard-edged navy housing with a squared notch
open at the top (two prongs, rows 3–8), enclosing a teal field that carries two pale-gold
rectangles, with a soft teal column just outside each side wall.

Two observations that drive the whole plan:

1. **The soft edge is alpha, not a baked halo.** The fractional pixels keep full-strength
   teal RGB `(86,181,188)` at α=96/160. Premultiplied encoding would have scaled those
   channels to roughly `(32,68,71)`. So the file is straight (non-premultiplied) alpha,
   and the soft edge composites correctly over any background rather than only over the
   one it was authored against.
2. **The anti-aliasing is genuinely selective.** Every other boundary in the image is
   hard: the notch corners at row 9, the navy/teal interior seam, and the gold marks all
   have zero intermediate pixels. Softening is spent on two chosen columns and nowhere
   else.

The left column is fainter than the right (96 vs 160). *Interpretation, not a measured
fact about intent:* this reads as a directional bias, as if the light sits to the right.
It is equally consistent with a deliberately uneven hand-authored edge. I have not
resolved which, and the plan does not depend on resolving it.

## 2. Authority table

Every restriction later in this document traces to a row here. "Requirement" means it can
reject a candidate. "Observation" and "Proposal" cannot.

| Property / value | Status | Exact source | Applies to |
| --- | --- | --- | --- |
| Subject is a small lantern prop that matches the reference | **Requirement** | User brief: "a small matching lantern prop" | The new asset |
| Intentional partial transparency is retained | **Requirement** | User brief: "uses intentional partial transparency … Keep that treatment in the new props" | The new asset |
| Anti-aliasing is selective — softened edges are chosen, other edges stay hard | **Requirement** | User brief: "selective anti-aliasing … Keep that treatment" | The new asset |
| No fixed palette is imposed | **Requirement (a negative one)** | User brief: "I have not imposed a fixed palette" | All production checks |
| Deliverable is Markdown planning only; no PX2 writes, no art, no provider call | **Requirement** | Evaluation instruction | This session |
| Native canvas 32×32 | Observation of reference → **Proposal** for the new prop | Measured | Canvas choice, pending confirmation |
| Alpha levels `{0,96,160,255}` | **Observation** | Measured | Reference only |
| Hues navy `#25354A` / teal `#56B5BC` / gold `#F4DDA2` | **Observation** → **Proposal** to reuse | Measured | Style direction only; never a palette gate |
| Straight (non-premultiplied) alpha | **Observation** (RGB unscaled at α<255) → **Proposal** to adopt as project policy | Measured; method `alpha-contract` | Export, import, compositing |
| Softening lives in two 1px vertical side columns, 15px each | **Observation** | Measured | Reference only |
| Left α < right α (96 < 160) | **Observation**; "light from the right" is an **interpretation** | Measured | Reference only |
| `opaque_components == 1` | **Observation** | Measured | Reference only — see §5 |
| Content bbox 20×25 with 6/6/3/4 margins | **Observation** | Measured | Reference only |
| Authored AA belongs inside a declared edge mask; protected hard edges stay byte-identical | Method guidance, **adopted** because it is how the brief's "selective" is made checkable | `selective-edge-aa` (`PIXEL-ART-DEEP-RESEARCH.md` 590–632, 907–919) | Authoring and review of the soft edge |
| Alpha policy is kept separate from RGB palette membership | Method guidance, **adopted** | `alpha-contract` (`PIXEL-ART-DEEP-RESEARCH.md` 945–977, 1276–1291; `PIXEL-ART-ASSETS.md` 942–958) | Check design |
| PixelLab returns usable fractional alpha | **Untested expectation** | None | The POC in §4 |
| PixelLab style-image transfer reproduces this look | **Untested expectation** | None | The POC in §4 |

The two knowledge methods above carry bounded POC receipts — a numeric compositing fixture
and a 5×5 raster AA fixture. Those receipts establish the methods' own arithmetic. They say
nothing about what any generator will return for this sprite.

## 3. The prop and where the two treatments go

The reference's vocabulary maps onto a lantern without inventing new structure:

- The navy housing becomes the lantern's metal cage/body; hard-edged throughout.
- The top notch becomes the gap under the hanging bail or hook.
- The teal field becomes the glass pane.
- The gold marks become the flame or wick core inside the glass.

**Partial transparency is authored in two named places**, and both must survive to the
final file:

- *Glass body.* The pane itself carries sub-255 alpha so background reads through it —
  this is the "intentional partial transparency" the brief protects. (In the reference the
  pane is opaque and only the outer columns are translucent; making the pane itself
  translucent is a **proposal**, since a lantern's defining feature is that you see light
  through it. If you prefer the reference's literal arrangement — opaque pane, translucent
  outer columns only — say so and I will invert this.)
- *Outer soft columns.* A 1px translucent skirt of the glass hue just outside the cage
  walls, matching the reference's placement.

**Selective anti-aliasing is authored as a declared edge mask.** Softened: the outer glass
skirt, and optionally the bail's curve. Protected hard: the cage silhouette, the cage/glass
seam, and the flame marks. Nothing outside the mask changes. Per `selective-edge-aa`, the
intermediate steps come from the asset's own hue at reduced alpha rather than from colors
mixed against an assumed background — which is exactly why the reference survives on any
backdrop, and is the property worth preserving.

Straight alpha throughout, consistently across export, import and display.

## 4. Representative sample first, batch never before it

One sample lantern, then review, then anything else.

| Field | Content |
| --- | --- |
| Question | Can the generator return a lantern in this style **with fractional alpha intact and confined to selected edges**, or must the alpha pass be authored locally? |
| Method | Style-image-conditioned single-direction object generation, with the reference supplied as the style image; `alpha-contract` and `selective-edge-aa` govern the alpha pass either way |
| Smallest artifact | One 32×32 lantern, single frame, no animation |
| Acceptance | Stated in §5 before the candidate is looked at |
| Consequence | Pass → proceed to further props. Fail → §6 |

Proposed provider request. **Every value below is a proposal, not a confirmed
configuration**, and the argument names are unverified — see the blocker immediately after:

- Tool: `create_1_direction_object` (proposal; it is the documented tool taking both
  `description` and `style_images`, which is what carries the reference's look).
- `style_images`: `translucent-reference.png` (proposal).
- `description` (proposal): *"small hanging lantern, squared dark metal cage with an open
  notch at the top for its bail, translucent glass pane filling the cage, small pale flame
  core inside the glass, soft translucent halo one pixel outside each side wall, hard clean
  edges everywhere else, front view, transparent background"*.
- Canvas 32×32 (proposal, from the reference measurement).
- No palette argument, and no palette constraint of any kind — the user imposed none.

**Blocker: the provider surface is not connected in this session.** Only the local
`pixl-local` tools are present; no PixelLab tool is callable, so I cannot discover the real
argument schemas. `pixl capabilities` returned a *dated documentation inventory*
(`retrieved_at 2026-09-11`, `live_discovery: false`), which records that these tools exist
but does not establish their current availability or signatures. Before any real call, the
exact request must be re-derived from live schemas and saved with `job-prepare`, then
claimed with `job-dispatch`.

## 5. Review criteria — fixed before any candidate is seen

**Mechanical (rejects a candidate).** Run `pixl asset-check <file> --width 32 --height 32
--alpha full`, then read the returned fields:

1. `pass: true` at 32×32 with `--alpha full`.
2. `fractional_alpha_pixels > 0`. *This is a reported measurement, not a built-in gate —
   the check must read the field; `asset-check` will not fail the file for its absence.*
3. Fractional-alpha pixels all fall inside the declared edge mask from §3, and every
   protected hard edge contains no intermediate pixel. Verified from a per-pixel dump.
4. RGB channels are unscaled at α<255 (straight alpha, not premultiplied).
5. **No palette check.** No `--palette` argument, no hue thresholds, no color count limit.

> **Do not run `--alpha binary` on this family.** I confirmed this against the reference
> itself: `asset-check translucent-reference.png --alpha binary --width 32 --height 32`
> returns `pass: false, failures: ["alpha"]`. A binary-alpha gate anywhere in the pipeline
> would reject the exact treatment the brief asks to preserve. This is the single largest
> hazard here.

**Visual (rejects a candidate; requires me to actually look).** Enlarged integer-nearest
view over both light and dark backgrounds, plus native scale:

6. Reads as a lantern at 32×32.
7. Sits alongside the reference as the same family — qualitative judgement, no numeric
   color rule.
8. The translucency is legible as translucency and does not read as a dirty edge or a
   background-specific halo.

Mechanical measurements cannot satisfy 6–8, and I will not mark an unviewed file approved.

**Engine (currently unavailable).** No destination engine was named, so import sampling,
alpha blend mode and atlas padding stay **unverified**, recorded as unavailable rather
than as a pass. Straight-alpha assets darken at the edges if an importer premultiplies
them twice — worth checking once a target exists.

**Deliberately not rejection rules.** Each of these would fail a variation that still
satisfies the brief, so none of them gate a candidate:

- Component count. A lantern with a detached bail ring, a separate hook, or a floating
  spark is a legitimate design; `opaque_components == 1` is a reference measurement only.
- Exact alpha values. α=110 or α=200 satisfies "intentional partial transparency" as well
  as 96/160 does.
- Exact hues, hue count, or color count — no palette was imposed.
- The reference's specific gap rows, margins, bbox, or the 1px×15px column geometry.

## 6. If the first candidate fails

Scoped to that attempt. One failed candidate establishes that attempt's failure — it does
**not** establish that the provider cannot produce fractional alpha, and no fallback below
should be written up as if it had.

- *Alpha flattened to 0/255:* keep the returned silhouette and author the alpha pass
  locally as a second step — apply the §3 edge mask, drop the selected pixels to
  sub-255 alpha at the asset's own hue, leave protected edges byte-identical, re-run §5.
  This is the `selective-edge-aa` procedure and is fully within local capability.
- *Alpha present but smeared over the whole silhouette:* that is anti-aliasing without the
  "selective" half. Re-prompt with the protected hard edges named explicitly, or mask down
  to the selected edges locally.
- *Style match weak:* vary the description before concluding anything about style-image
  transfer, and record each attempt.

Retain every failed candidate and its review rather than overwriting it.

## 7. Open decisions

1. **Canvas size.** 32×32 is proposed from the reference's measurement, not adopted.
2. **Translucent pane, or reference-literal.** §3 proposes making the glass pane itself
   partly transparent. The reference keeps its pane opaque and softens only the outer
   columns. Both honor the brief; they look different.
3. **Destination engine.** Unnamed, so the import criteria stay unverified.
4. **Palette.** None imposed, so none is checked. Locking the reference's three hues later
   is available as an *optional* experiment; it is not part of the plan.
