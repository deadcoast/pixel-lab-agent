# Lantern prop — production approach (planning only)

Status: bounded planning evaluation. No PX2 state was initialized or changed, no art was produced, and no provider was called. Nothing here is accepted production output.

## 1. Inputs reviewed

| Input | Identity |
|---|---|
| `translucent-reference.png` | sha256 `bda5c9b18e38b60a617877de6e9df6c5bf8e040410e9dfbe6bc85ca501b17132` |
| User brief | "The reference uses intentional partial transparency and selective anti-aliasing. Keep that treatment in the new props. … a small matching lantern prop; I have not imposed a fixed palette." |
| PIXL methods consulted | `selective-edge-aa`, `alpha-contract` (library.px). Their bounded POCs are raster/compositing fixtures. They do not show that a provider can reproduce this treatment. |

## 2. What the reference contains (measured observations)

These come from `pixl_asset_check` and a pixel dump. They are observations, not requirements.

- Canvas 32×32 RGBA, 1 frame. Visible bbox `[6,3,26,28]`. 420 visible pixels, 1 opaque 4-connected component.
- 3 RGB values: dark navy `#25354A` (outline, top lugs, top and bottom bars), teal `#56B5BC` (body fill), cream `#F4DDA2` (two 3×4 "eye" blocks).
- **Partial transparency / selective AA (30 pixels):** these are all teal RGB at reduced alpha. They sit in single columns outside the navy outline:
  - left edge x=6, rows 11–25: alpha 96 (~38%)
  - right edge x=25, rows 11–25: alpha 160 (~63%)
- Everything else is hard-edged: the top lugs, the top and bottom navy bars, and the corners have no fractional alpha and no blended intermediate colors. So the soft treatment is **selective**. It is placed on only the two vertical side edges.
- The side fringe is asymmetric (left fainter than right). That reads like a lighting direction, but this is my interpretation and unconfirmed.
- In this reference the "anti-aliasing" is done with alpha coverage (same RGB, lower alpha), not with blended in-between RGB colors.
- `pixl_asset_check` reported `failures: ["alpha"]` only because its default check expects binary alpha. Under this brief the fractional alpha is intended, so that flag is not a defect.
- Subject reading: a squat boxy body with two top lugs and two light "eyes". Whether it is a character, a jar or a container is uncertain, and the plan does not depend on it.

## 3. Authority table

| Property / value | Status | Source | Scope |
|---|---|---|---|
| Keep intentional partial transparency | **Requirement** | User brief | All new props, including the lantern |
| Keep selective anti-aliasing (on chosen edges only, not everywhere) | **Requirement** | User brief | All new props |
| Lantern prop, small, "matching" the reference | **Requirement** (matching is qualitative) | User brief | This asset |
| No fixed palette | **Requirement (absence of constraint)** | User brief | No exact palette-membership check in production |
| "Selective" AA = soft edges on some edges, hard edges on others | Reading of the brief word "selective", consistent with reference | Brief (+ reference observation) | Lantern review (R2) |
| Where partial transparency is placed (edges, glass, halo) | **Open**. The brief does not restrict it to edges. | — | User decision (§8) |
| AA done via alpha coverage of the adjacent fill colour (not blended RGB) | Observation | Reference pixels | Proposal for sample only. Colour-blend AA also satisfies the brief. |
| Transparent background around the prop | Proposal (usual for a prop sprite; not stated in the brief) | Inference | Sample default. Not a rejection rule until confirmed. |
| Interior details (flame, frame bars) kept crisp | Proposal | — | Sample experiment only |
| Alpha levels 96 and 160 | Observation | Reference pixels | Proposal for sample only. Other levels are allowed. |
| Asymmetric fringe (left fainter) = light from right | Interpretation | Reference | Proposal, not a rule |
| 32×32 canvas, dark navy outline, teal/cream colours | Observation | Reference | Proposal for sample. Not enforced (no fixed palette). |
| Straight (non-premultiplied) RGBA PNG | Proposal | `alpha-contract` method; PNG convention | Must be confirmed against the target engine |
| Single connected opaque component | Observation | Reference | **Not** a rule. A lantern may have a detached glow or flame. |

## 4. Where the treatments go on a lantern (proposal)

Both required treatments must be present. The placements below are proposals for the representative sample, with one decision left open (§8):

1. **Partial transparency** goes on the glass panes and/or a light halo:
   - Option A (natural for a lantern; a new placement not shown in the reference): the glass panes are translucent fill (warm light colour at partial alpha) between hard opaque frame bars. The background shows through the glass.
   - Option B: opaque glass, with a soft partial-alpha light fringe or halo outside the frame on selected sides. This mirrors the reference's outside-the-outline columns.
2. **Selective anti-aliasing** goes on chosen edges only. For example: the curved top cap or handle ring, and the frame's vertical sides. Do it with partial-alpha pixels of the adjacent colour, as the reference does. Keep the base, frame corners and handle attachment points hard-edged.
3. *[proposal]* Interior details (flame, frame bars) stay crisp in the first sample. This is an experiment, not a rejection rule.

## 5. Production steps

1. **Intake (later, when authorized):** create PX2 intake from this brief. Record the requirements above as confirmed. Record observations and proposals as proposed/unknown. Plan one output: `lantern` sample, RGBA PNG.
2. **Provider discovery:** look up the connected PixelLab tool list and schema at that time, and pick the operation that supports a reference/style image and transparent output. No tool or parameter is assumed here.
3. **Representative sample:** generate a single lantern conditioned on `translucent-reference.png` as the style reference.
   - Proposed prompt (choices marked *[proposal]* are not user requirements): "Small pixel-art lantern prop matching the reference style. *[proposal: transparent background]*. **Keep intentional partial transparency** *[proposal: on the glass panes / light halo]* and **selective anti-aliasing on only some edges** *[proposal: curved top cap and vertical sides, using semi-transparent edge pixels]*, with other edges hard. *[proposal: 32×32 canvas, dark outline, teal/cream-adjacent colours, light from the right]*."
   - Generated output may come back with binary alpha only, or with soft alpha everywhere. If so, author the selective alpha by hand or with a scripted edit inside an explicit edge mask (`selective-edge-aa`). Keep the provider candidate and the edited version as separate candidates.
4. **Inspection:** use `pixl_inspection_prepare` for native and integer-nearest views. Review them against light, dark and mid backgrounds (`alpha-contract`). Translucency only shows correctly when composited.
5. **Family extension:** only after the sample is accepted. R1, R2 and R4 carry over to the other "new props". R3 is replaced by each prop's own identity check.

## 6. Review criteria

**Production (rejection) checks: only from requirements**
- R1 Partial transparency present. At least some visible pixels have 0 < alpha < 255, placed intentionally (glass/halo/edges), not as uniform noise.
- R2 Anti-aliasing is selective. Soft edge pixels (partial-alpha or blended-colour) appear on chosen edges, and other edges remain hard. A sprite with no AA fails, and so does one softened uniformly on every edge.
- R3 Reads as a lantern at native size.
- R4 Visually matches the reference (qualitative human judgement covering outline weight, colour feel and simplicity).
- No exact palette-membership check, because no palette was imposed.
- R1 placement follows the §8 decision once it is made. Until then, translucency on glass, halo or edges all satisfies R1.

**Mechanical measurements (recorded, not verdicts):** dimensions, alpha histogram, fractional-alpha pixel locations, colour count, components. A binary-alpha warning from `pixl_asset_check` is expected and not a failure.

**Optional experiments (not rejection rules):** transparent background; crisp interior details; alpha-coverage AA instead of colour-blend AA; 32×32 size; reference alpha levels 96/160; reference RGB values; right-side light direction; single opaque component.

## 7. Risks and uncertainties

- Whether a generator honours *selective* partial alpha is untested here. Hand-authoring the mask may be needed. One failed candidate would show that attempt failed, not a general provider limit.
- Translucent pixels show differently on each background. Halos are possible if the colour was chosen for one background only (`selective-edge-aa` pitfall).
- Premultiplied versus straight alpha in the target engine is unknown. Engine import behaviour is unverified.
- "Matching" is a qualitative call, and only a human review can settle it.

## Revision note

Whole-file audit against §3. The prior draft is kept as `APPROACH.draft1.md`. Changes:
- Removed the implicit restriction of partial transparency to edges. Placement is now an open decision.
- Corrected the contradictory "Option A closest to the reference" label.
- Demoted these from production rules to labeled proposals: transparent background (was R5), crisp interior, alpha-only AA.
- Clarified that colour-blend AA also satisfies R2.
- Scoped the family carry-over so it does not apply the lantern-identity check to other props.

## 8. Decision needed from the user

**Where should the lantern's partial transparency live?**
- (A) translucent glass panes (background visible through glass), or
- (B) opaque glass with a soft partial-alpha light fringe or halo outside the frame (closest to the reference's side columns), or
- both.

Recommendation: start with (A), and soften the vertical sides selectively as the reference does. The glass is the lantern's natural translucent part, and the side softening keeps the reference's edge treatment. Also confirm the target engine's alpha mode (straight vs premultiplied) before acceptance.
