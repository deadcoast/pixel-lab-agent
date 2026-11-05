# Production approach — small lantern prop matching `translucent-reference.png`

**Status:** planning only. This document is the whole deliverable for this task. No PX2 project
was initialized or amended, no production art was generated, and no provider was called.

---

## 1. What was actually inspected

| Item | Value |
| --- | --- |
| Reference file | `translucent-reference.png` |
| sha256 | `bda5c9b18e38b60a617877de6e9df6c5bf8e040410e9dfbe6bc85ca501b17132` |
| Mechanical measurement | `pixl_asset_check` (`alpha: full`), single frame |
| Pixel dump | full 32×32 RGBA enumeration via Pillow (selected `.venv` interpreter) |
| Enlarged view | `inspection/reference-x12.png` (nearest, ×12) — viewed |
| Background views | `inspection/reference-backgrounds-x8.png` (white / near-black / magenta, ×8) — viewed |
| Knowledge consulted | `selective-edge-aa`, `alpha-contract`, `silhouette-readability`, `material-channel-budget` |
| Provider inventory | `pixl_capabilities`, retrieved `2026-09-11T05:58:46Z`, `live_discovery: false` |

The two `inspection/` files are viewing aids produced for this review. They are not candidate art.

---

## 2. Measured reference facts (observations)

```text
canvas            32 × 32 RGBA (straight alpha; PNG carries no premultiply flag)
visible bbox      x 6–25, y 3–27   (20 × 25 occupied)
visible pixels    420   → 390 fully opaque, 30 fractional alpha
opaque components 1 (4-connectivity)
visible colors    5
  (37, 53, 74, 255)    dark slate — posts, frame, base
  (86,181,188, 255)    teal       — body fill
  (244,221,162,255)    cream      — two inset windows
  (86,181,188,  96)    teal @ 38% — left wash column,  x=6,  y=11–25  (15 px)
  (86,181,188, 160)    teal @ 63% — right wash column, x=25, y=11–25  (15 px)
fully transparent RGB is zeroed: every α=0 pixel is (0,0,0,0)
opaque outer-boundary pixels: 92, all hard transitions except where they meet the two wash columns
```

Silhouette, from the pixel map: two upright slate posts (x 7–10 and 21–24, y 3–8) over a slate
frame enclosing a teal panel (x 9–22, y 11–25), with two cream windows inset symmetrically
(x 11–13 and x 18–20, y 14–17). Everything is axis-aligned; there is not a single diagonal or
curve in the image.

### How the translucency is actually built

The fractional-alpha pixels are **the body teal at reduced alpha**, not an intermediate color
blended toward a background. They sit in two straight 1-px columns, one immediately outside each
vertical side of the frame, spanning exactly the panel's rows. They are absent from the top edge,
the bottom edge, the posts, and the window insets.

Two consequences worth carrying into production:

- **It is background-agnostic.** Because the wash is the object's own hue at lowered alpha rather
  than a background-matched blend, it composites cleanly over light, dark and saturated
  backgrounds. I confirmed this on the three-background sheet: no foreign-hue halo appears on any
  of them. This directly avoids the `selective-edge-aa` pitfall *"background-specific intermediate
  colors can form halos on different backgrounds."*
- **The selectivity is the point.** 92 opaque boundary pixels exist; the soft treatment touches
  two edge runs and leaves the rest byte-hard. That is what makes it read as authored rather than
  as a filtered image.

### Where my reading differs from the brief — reported, not substituted

1. **Subject.** Enlarged, the form reads to me as a boxy housing or casing with two prongs and two
   lit windows. It does not read to me as a lantern. The brief names the *treatment* to carry
   over, not the subject, so I have planned "matching" as **treatment + material character + edge
   discipline**, not as silhouette copying. If you intended the reference itself to be a lantern
   and want the new prop to share its anatomy, say so and I will re-derive the silhouette plan.
2. **"Anti-aliasing".** What is present is constant-alpha translucency on selected edges, not
   coverage-graded contour AA (there are no diagonals for coverage AA to act on). I am keeping
   your terminology and your requirement intact; I am only flagging that the mechanism a
   generator or an artist would reproduce is *alpha reduction of an existing color on chosen
   edges*. This is an observation about how to hit the target, not a replacement for it.
3. **Left/right asymmetry.** α=96 left vs α=160 right. This *could* be a light-direction cue
   (stronger wash on the right) or simply uneven authoring. Untested — see §7.

---

## 3. Authority table

Every restriction in this document traces to a row here. Only **Requirement** rows may reject a
candidate.

| # | Property / value | Authority & status | Exact source | Scope |
| --- | --- | --- | --- | --- |
| A1 | Partial transparency is present and intentional | **Requirement** (user) | "uses intentional partial transparency … Keep that treatment in the new props" | Every new prop in this family |
| A2 | Anti-aliasing is *selective* — chosen edges soft, other edges hard | **Requirement** (user) | "selective anti-aliasing … Keep that treatment" | Every new prop in this family |
| A3 | Subject is a small lantern prop | **Requirement** (user) | "a small matching lantern prop" | This asset |
| A4 | No fixed palette is imposed → no palette-membership check | **Requirement** (user) | "I have not imposed a fixed palette" | This asset; production checks omit exact palette membership |
| A5 | Deliverable is this Markdown approach only | **Requirement** (user) | "save the production approach in APPROACH.md … do not initialize or amend PX2 state, create production art, or call a provider" | This task |
| B1 | 32 × 32 canvas | Observation (reference pixels) | `asset-check` frame 0 | Reference only |
| B2 | Colors `#253549`, `#56B5BC`, `#F4DDA2` | Observation (reference pixels) | full pixel enumeration | Reference only; **not** a palette rule (A4) |
| B3 | Fractional alpha levels {96, 160} | Observation (reference pixels) | full pixel enumeration | Reference only |
| B4 | Soft treatment on the two vertical panel edges, 1 px wide, absent elsewhere | Observation (reference pixels) | columns x=6, x=25, rows 11–25 | Reference only; A2 requires *some* selectivity, not this placement |
| B5 | 1 opaque 4-connected component | Observation (`asset-check`) | `opaque_components: 1` | Reference only; **not** a rule — a lantern with a detached handle ring or a floating spark still satisfies the brief |
| B6 | α=0 pixels have RGB (0,0,0) | Observation (reference pixels) | full pixel enumeration | Reference only |
| B7 | Wash hue = body hue at lowered alpha (background-agnostic) | Observation (pixels + 3-background composite) | see §2 | Reference only; informs method choice |
| B8 | Straight, non-premultiplied RGBA | Observation (PNG format) | `alpha-contract`, *"RGB ... straight or premultiplied alpha, and allowed alpha levels"* | Must be **declared** for the new asset (A1 depends on it); the specific choice is P6 |
| C1 | Prop canvas 32 × 32 | **Proposal** | matches B1, keeps the pair comparable at one scale | Trial only — open decision Q2 |
| C2 | Reuse `#253549` / `#56B5BC` / `#F4DDA2` as the starting hues | **Proposal** | matches B2, cheapest route to "matching" | Trial only — open decision Q1; never a rejection check (A4) |
| C3 | Wash 1 px wide, alpha in the 96–160 band | **Proposal** | matches B3/B4 | Trial only |
| C4 | Soft treatment placed on the lantern's glass/light-bearing edges and the cast-light side; hard everywhere else | **Proposal** | project-specific reading of A2 for a lantern subject | Trial only; A2 is satisfied by any deliberate selectivity |
| C5 | Zero the RGB of fully transparent pixels | **Proposal** | `alpha-contract` pitfall: *"Fully transparent RGB channels can differ without changing visible appearance"* | Trial/export hygiene; not an artistic gate |
| C6 | Lantern anatomy: housing frame, glass panel, top hanger, base | **Proposal** | project-specific reading of A3 | Trial only |
| D1 | Nearest/point sampling at import; no bilinear filtering | **Requirement, conditional on A2** | deep-research L907–919: *"sprite sampling = nearest / point … Otherwise the GPU's interpolation destroys the controlled decisions the artist made"* | Destination engine; **unverified** — no destination engine named or available |

---

## 4. Subject and role

A small lantern prop, matching the reference's treatment and material character. Gameplay role and
destination engine were not stated; both are left open and neither is invented here. Planned
review is therefore native-scale readability plus background compositing (§6), with engine import
recorded as **unavailable**, not as a pass.

Per `silhouette-readability`, identity landmarks are named before detailing so the visual review
has something concrete to check. Proposed landmarks (C6): **housing frame**, **glass panel**,
**top hanger**, **base**. These name what the review looks for; they do not forbid a different
lantern anatomy you prefer.

`material-channel-budget` is explicitly *not* being invoked: no emission channel, mask channel or
height map is planned. Its rule is that extra channels need a named consumer, and there is no
named engine consumer here. The lantern's light is authored into the diffuse RGBA only.

---

## 5. Alpha contract (the core of "keep that treatment")

Declared for the new prop, following `alpha-contract`'s requirement to state RGBA interpretation,
compositing model and allowed alpha levels, and to *"keep alpha policy separate from RGB palette
membership"* — which is exactly the split your brief asks for (A1/A2 binding, A4 open):

- **Interpretation:** straight (non-premultiplied) RGBA, PNG. (B8)
- **Allowed alpha levels:** 0, 255, and a *declared exception* for authored intermediate levels.
  `alpha-contract`'s check is *"binary-alpha assets contain only 0 and 255 unless an exception is
  declared"* — this asset declares that exception, because A1 requires it.
- **Where intermediate alpha is authored:** on selected edges only, as the adjacent region's own
  hue at reduced alpha (method from B7, which keeps the result background-agnostic). Proposed
  placement C4, proposed band C3.
- **Where alpha stays binary:** every edge not selected above. This is what makes A2 true and is
  the one thing most likely to be lost in generation.

Per `selective-edge-aa`, the changed pixels must stay inside the selected edge mask, protected
hard edges must remain untouched, and the result must be previewed against each allowed
background before acceptance. Its pitfall — *"this is authored color placement, not a permission
to enable bilinear texture filtering"* — is why D1 exists.

---

## 6. Production route

### 6.1 Provider

**No PixelLab tools are exposed in this session**; only the local `pixl-local` tools are present.
So provider execution cannot happen here, and nothing below is a live capability claim.

From the dated capabilities inventory (`2026-09-11`, `live_discovery: false`), the candidate
route is `create_1_direction_object` (`description` + `style_images`) — the only listed generate
tool that accepts style images, which suits "matching" a supplied reference. Alternatives if its
live schema differs: `create_map_object`, or `create_image_pixflux` / `create_image_pixen` /
`create_image_pro`.

**The production session must re-discover the actual tools and schemas before preparing a
request.** This inventory is a dated document, not live discovery. Whether any of these tools
returns authored partial alpha is an **untested expectation** — that is precisely what §6.3
exists to find out.

### 6.2 Proposed prompt (a labeled experiment, not an adopted contract)

Every bracketed item below is a **proposal** from §3, not a requirement:

> A small pixel-art lantern prop, front-facing, on a fully transparent background.
> `[proposal C6]` A dark slate metal housing frame with a lit glass panel, a hanger at the top and
> a solid base. `[proposal C2]` Dark slate metal, a cyan-teal glass body and a warm cream glow
> inside the panel. `[proposal C1]` 32×32. `[requirement A2]` Hard, crisp, unfiltered pixel edges
> on the metal housing and the base — no blur or softening there. `[requirement A1]` A soft
> semi-transparent halo of the glass color on the glass panel's side edges only.
> `[proposal C3]` One pixel wide. Flat color areas, no gradients, no dithering.

Note what is deliberately **absent**: no palette-membership instruction (A4), no component-count
or symmetry instruction (B5 is an observation), and no blanket "no antialiasing" directive — a
blanket ban would contradict A1/A2, which require authored soft pixels. The instruction is
*selective*: hard on the housing, soft on the named glass edges.

### 6.3 Representative sample / proof of concept

One candidate, before any batch.

| Field | Content |
| --- | --- |
| **Question** | Can the chosen tool return an asset with authored partial alpha confined to selected edges, or does it flatten alpha to binary / soften every edge uniformly? |
| **Method** | `create_1_direction_object` with `style_images: [translucent-reference.png]` and the §6.2 prompt, subject to live schema re-discovery. |
| **Smallest artifact** | One static lantern at the chosen canvas size. |
| **Acceptance** | The §6.4 rejection checks, stated here before any result is interpreted. |
| **Result** | Not run. No provider is reachable in this session. |
| **Consequence** | Pass → proceed to the prop family. Fail → §6.5 fallback. |

### 6.4 Rejection checks (entailed by the brief only)

| Check | Source | Evidence mode |
| --- | --- | --- |
| K1 — At least one pixel has 0 < α < 255; the asset is not flattened to binary alpha | A1 | mechanical (`asset-check --alpha full`) |
| K2 — Fractional-alpha pixels occupy identifiable authored regions, **and** hard α 0↔255 boundary transitions still exist elsewhere. Not every silhouette edge is soft | A2 | mechanical support + visual confirmation |
| K3 — The soft pixels read as deliberate placement on chosen edges, not as a filtered halo around the whole silhouette or a global opacity reduction | A2 | **visual**, enlarged and native scale |
| K4 — The prop reads as a lantern at native scale | A3 | **visual**, on light / dark / busy backgrounds |
| K5 — The soft edges produce no foreign-hue halo on any allowed background | A2 + `selective-edge-aa` preview step | **visual**, per-background composite |

No numeric threshold is set for K2. The measured 30-of-92 ratio in the reference is B4, an
observation about that image; inventing a percentage gate from it would turn an observation into a
rule. K2's mechanical part is a presence/absence test; the judgement is K3's and is visual.

**Not checks:** exact palette membership (A4 forbids it), component count (B5), exact alpha
values (B3), exact canvas (B1), left/right asymmetry, exact wash width or placement (B4).

### 6.5 Fallback if the sample fails

Author the partial-alpha regions locally as a post-pass over the returned opaque art, using the
reference's own mechanism (B7): select the edge mask, reduce the alpha of the adjacent body color
on that mask, leave every other pixel byte-identical. `selective-edge-aa`'s own check —
*"protected hard edges remain byte-identical"* — is directly verifiable on the before/after pair.
Re-run K1–K5 on the result.

**Scope limit:** if the sample fails, that establishes *that attempt's* failure with *that tool,
prompt and reference*. It does not establish that PixelLab cannot produce authored partial alpha,
and this document must not be read as concluding that.

---

## 7. Optional experiments (never rejection rules)

- **E1 — Palette.** Compare C2 (reuse the reference's three hues) against a newly authored
  lantern-appropriate set. A4 means neither can fail a production check; this is a preference
  trial only.
- **E2 — Wash asymmetry.** The reference's α=96 / α=160 split (B3) may encode a light direction.
  A trial pair — symmetric wash vs. stronger-on-one-side — would show whether the asymmetry is
  what makes the treatment read as intentional. Currently an interpretation with no evidence.
- **E3 — Curved forms.** The reference contains no diagonals or curves, so it says nothing about
  how the treatment behaves on a curved lantern hood or a ring hanger. If a curve is wanted, run a
  treatment-preserving trial on that shape. Uncertainty here is not grounds to ban curves.

---

## 8. Known limits of this document

- No candidate exists. Every statement about matching quality, lighting read, and provider
  behavior is an interpretation or an untested expectation. A plan cannot guarantee them.
- The provider tool list is dated `2026-09-11` with `live_discovery: false`; no PixelLab tool is
  reachable from this session.
- No destination engine was named and none is available, so D1 (nearest/point sampling) is an
  **unverified import requirement** to carry with the delivered asset, not a satisfied check.
- The reference's own visual quality was not accepted or rejected here; it was measured and read
  as a treatment source.
- `visual_quality_verified: false` and `engine_import_verified: false` in the `asset-check` output
  are correct and expected — that tool measures, it does not approve.

## 9. Open decisions (see §3 C1, C2 and §2 item 1)

1. **Palette** — reuse the reference's three hues, or author a new set for the lantern? The
   treatment (A1/A2) survives either answer; this only changes the prompt's color clause and E1.
2. **Canvas** — 32 × 32 to match the reference, or a different size for "small"?
3. **Silhouette** *(clarification, not blocking)* — is the reference itself meant to be a lantern?
   If yes, the new prop should inherit its anatomy and §4's landmarks get re-derived.
