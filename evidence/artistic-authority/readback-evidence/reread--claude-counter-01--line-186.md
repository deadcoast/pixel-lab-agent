# Production approach — matching drone sprite

Session date: 2026-09-14. Bounded planning deliverable. No PX2 state was created or amended,
no art was generated, and no provider was called.

Reference inspected: `small-separated.png`
sha256 `1c45c866f9d11ff57b055f4dacf1e47c8e71f2c99fd6b24f0cb4259ee40cbe5c`

**Assumption stated for the user to correct:** the reference establishes the aesthetic, and the
work to plan is one new *matching* drone sprite as the representative sample. Extending to a family
of drones is deferred until that sample is accepted.

---

## 1. Authority table

Every restriction later in this document traces to a row here. "Requirement" = binding for
production. "Observation" = measured in the reference, not thereby adopted. "Proposal" = my
suggestion, to be tested, not enforced.

| Property | Value | Authority / status | Source | Applies to |
| --- | --- | --- | --- | --- |
| Canvas | 16 x 16 | **Requirement** | User instruction, this session | Every drone sprite |
| Frame | Thick two-pixel dark band around the teal body | **Requirement** | User instruction, this session | Every drone sprite |
| Antenna | Two antenna islands, detached from the body | **Requirement** | User instruction, this session | Every drone sprite |
| Body fill | Teal (qualitative, no hex fixed) | **Requirement** | User instruction, this session | Every drone sprite |
| Subject | Reads as a drone matching the reference | **Requirement** | User instruction, this session | Every drone sprite |
| Fixed palette | **Not approved** — exact palette membership is not a production check | **Requirement (negative)** | User instruction, this session ("I have not approved a fixed palette") | Every drone sprite |
| Visible colors | 3 | Observation | Measured, `small-separated.png` | Reference only |
| Frame color | `#25354A` (37, 53, 74) | Observation | Measured, `small-separated.png` | Reference only |
| Panel color | `#56B5BC` (86, 181, 188) | Observation | Measured, `small-separated.png` | Reference only |
| Eye color | `#F4DDA2` (244, 221, 162), 2 px total | Observation | Measured, `small-separated.png` | Reference only |
| Visible pixels | 88 of 256 | Observation | Measured, `small-separated.png` | Reference only |
| Components (4-conn.) | 3 | Observation | `pixl_asset_check` | Reference only |
| Visible bbox | x 3–12, y 2–13 (10 wide, 12 tall) | Observation | `pixl_asset_check` | Reference only |
| Body block | 10 x 8 at cols 3–12, rows 6–13 | Observation | Measured, `small-separated.png` | Reference only |
| Interior panel | 6 x 4 at cols 5–10, rows 8–11 | Observation | Measured, `small-separated.png` | Reference only |
| Antenna blocks | Two 2 x 2 squares, cols 5–6 and 9–10, rows 2–3 | Observation | Measured, `small-separated.png` | Reference only |
| Antenna gap | 2 fully empty rows (rows 4–5) | Observation | Measured, `small-separated.png` | Reference only |
| Alpha | Binary; 0 fractional-alpha pixels | Observation | `pixl_asset_check --alpha full` | Reference only |
| Alpha policy for new work | Binary alpha (0 / 255) | **Proposal** — not yet adopted | My suggestion; matches reference | Open decision #3 |
| Eye treatment | Two 1-px light eyes on the panel | **Proposal** — brief does not mention eyes | My suggestion; matches reference | Open decision (minor) |
| Provider route | `create_image_pixen` probe, then `create_1_direction_object` | **Proposal** — untested on this brief | Catalog snapshot 2026-09-11 | Open decision #2 |
| Destination engine | None named | **Unresolved** | No user instruction | Import check stays unavailable |

### Measured colour relationships (evidence only — no threshold is adopted)

WCAG relative-luminance ratios in the reference: frame-to-panel 5.18, panel-to-eye 1.80,
frame-to-eye 9.31. The eyes separate from the panel mostly by **hue**, not by value. This is
recorded so a later reviewer understands the reference; it is **not** converted into a numeric
contrast gate for new art.

---

## 2. Reference measurement

Exact pixel map (`A` = dark frame, `B` = teal panel, `C` = cream eye, `.` = alpha 0):

```
    0123456789012345
  0 ................
  1 ................
  2 .....AA..AA.....
  3 .....AA..AA.....
  4 ................
  5 ................
  6 ...AAAAAAAAAA...
  7 ...AAAAAAAAAA...
  8 ...AABBBBBBAA...
  9 ...AABCBBCBAA...
 10 ...AABBBBBBAA...
 11 ...AABBBBBBAA...
 12 ...AAAAAAAAAA...
 13 ...AAAAAAAAAA...
 14 ................
 15 ................
```

The layout the brief describes is directly confirmed in the pixels: the dark band is exactly 2 px
on all four sides of the body (rows 6–7 and 12–13; cols 3–4 and 11–12), the panel is the enclosed
6 x 4 teal region, and the two antenna blocks are separated from the body by two empty rows.

## 3. Visual inspection performed

I composited the reference over a dark (`#181818`) and a light (`#EBEBEB`) background, plus a flat
silhouette mask, upscaled 24x nearest-neighbour, and viewed all three.

- The sprite reads as a boxy hovering drone: chassis, face panel, two eye lights, two antenna stubs.
- **Identity is carried by the interior colour blocking, not by the silhouette.** The mask is a
  plain rectangle plus two small squares — it is not diagnostic. Consequence: silhouette review
  alone cannot accept a candidate here; the colour views must be reviewed.
- On the dark background the `#25354A` frame nearly merges with the backdrop and the teal panel
  carries the read. Scope: this is an observation about *this* reference on *these two* test
  backgrounds, not a general rule about the style or a reason to change the frame colour.
- The 2 px frame does **not** starve the interior at 16 px: it leaves a 6 x 4 panel that comfortably
  holds two separated eye pixels with a 1 px margin from the frame.

## 4. Disposition of `old-assessment.md`

That file was written by an earlier agent, was never approved, and its three proposals are either
refuted by the reference or contradict the brief. None of them enter this approach.

| Prior unapproved proposal | Disposition |
| --- | --- |
| 32-px minimum canvas for thick outlines | **Rejected.** It came from a resized 32-px source of a *different* robot. Measured here: a 2 px frame at 16 x 16 leaves a 6 x 4 panel and the eyes do not touch the contour. A failure of one resized fixture does not establish a canvas minimum for this design. |
| One connected component for all sprites | **Rejected.** It directly contradicts the user's requirement of two detached antenna islands. |
| Lock all props to the observed three colours | **Rejected as a rule.** The user has explicitly not approved a fixed palette. The three colours stay observations; a palette lock is available as optional experiment E1 if the user adopts it. |

## 5. Planned production

### 5.1 Layout intent (proposal — not a rejection rule)

Reuse the reference's proportions as a starting point because they are known to work at this size:
a 10 x 8 body centred horizontally, a 2 px frame, an enclosed teal panel, and two antenna islands
above with an empty gap. A different body footprint, a different antenna shape, or a 1-row gap all
still satisfy the brief and must not be auto-rejected.

### 5.2 Provider route

PixelLab tools are **not present in this session's tool list** (only `pixl-local` is configured), so
no dispatch is possible now. Before any real call, read the runtime `tools/list` `inputSchema` — the
bundled catalog (snapshot 2026-09-11, `https://api.pixellab.ai/mcp/docs`) states plainly that it
does not establish availability or current schemas.

Relevant documented constraints from that snapshot, to be re-verified against the live schema:

- `create_image_pixflux` — **cannot** produce 16 x 16: the per-axis floor is 16 but total area must
  be at least 1024 px. Documented tool constraint, not an artistic judgement.
- `create_image_pixen` — 16 x 16 is permitted (multiple of 4, square, and squareness is required
  below 32 px). Accepts no style or reference image; the aesthetic must ride entirely in the text.
  Cost 1 generation. Supports `seed`.
- `create_1_direction_object` — `style_images` is required; supplying the 16 x 16 reference sets the
  output size to 16 (size and non-empty `style_images` cannot coexist) and yields **64 candidates**
  in `review` status. Cost 20–40 generations.
- `create_image_pro` — accepts a style image, but its documented default and maxima are large and no
  16 px floor is stated; reaching 16 px would require downscaling, which resamples the pixel grid.
  Not selected.

**Step 1 — cheap probe (`create_image_pixen`, 1 generation).** Establishes whether the provider can
hold a 2 px frame *and* detached islands at 16 x 16 at all, before spending 20–40 generations.

**Step 2 — fidelity route (`create_1_direction_object`), if step 1's match is weak.** The 16 x 16
reference is passed as `style_images`, which both pins the output to 16 x 16 and carries the
aesthetic by image rather than by words. Inspect all 64 candidates, then `select_object_frames`.

**Step 3 — authored fallback.** At 16 x 16 with 88 visible pixels, authoring the sprite directly is
tractable and *guarantees* the three required treatments. This is the reliable path to a correct
asset if both provider attempts miss the brief.

Scope note on failure: if step 1 returns a candidate that misses the detached islands, that
establishes *that attempt* failed. It does not establish that PixelLab cannot render detached
islands at 16 px, and does not by itself authorise abandoning the treatment.

### 5.3 Draft request — step 1

Proposal. Every value below is my choice, not a user-adopted setting; `view`, `direction`,
`outline` and `detail` are documented as *weakly guiding*. Colours are described qualitatively
because no palette is approved — **do not put hex values in this prompt.**

```
tool: create_image_pixen
description:
  "16x16 pixel art hovering drone, facing the viewer. Boxy chassis drawn as a thick
   two-pixel dark outline frame that completely encloses a flat teal face panel. Two
   small light eye pixels on the teal panel. Two small antenna blocks floating
   separately above the chassis, clearly detached with empty space between them and
   the chassis. Flat colours, hard pixel edges, transparent background."
width: 16                       # requirement
height: 16                      # requirement
no_background: true             # proposal (sprite, not scene)
view: "side"                    # proposal, weakly guiding
direction: "south"              # proposal, weakly guiding
outline: "single color outline" # proposal, weakly guiding
detail: "low detail"            # proposal, weakly guiding
seed: <record the value used>   # proposal, for reproducibility
```

The three required treatments — 16 x 16, the two-pixel dark frame around the teal body, and the two
detached antenna islands — are each stated explicitly in the description, and are restated as
checks in §6.

### 5.4 State that would be saved once production is authorised

Not written this session. When authorised: a PX2 intake carrying the brief; `I` records for canvas,
frame, antenna islands and body colour as **confirmed**, and for palette, alpha and engine as
**unresolved**; an `F` output plan for the sample; the `Q` criteria of §6 saved *before* any
candidate is judged; then `job-prepare` / `job-dispatch` for the actual call.

## 6. Acceptance criteria

### 6.1 Production rejection rules — each traces to a requirement in §1

| # | Check | Evidence mode | Traces to |
| --- | --- | --- | --- |
| C1 | Canvas is exactly 16 x 16. | Mechanical (`pixl_asset_check`) | Canvas requirement |
| C2 | A dark band of a single colour, measuring exactly 2 px, lies between the teal interior and transparency in each cardinal direction from the interior, and fully encloses it. Corner chamfers or rounding are referred to visual review, not auto-rejected. | Mechanical + visual | Frame requirement |
| C3 | Exactly two antenna clusters sit above the body, each disjoint from the body cluster under 4-connectivity, each separated from it by at least one fully empty row. | Mechanical (semantic masks, not raw component count) | Antenna requirement |
| C4 | The enclosed interior reads as teal. | Visual | Body-fill requirement |
| C5 | At native 16 x 16 scale, on a light and a dark background, the sprite reads as a drone belonging to the same family as the reference. | Visual, host-viewed — a mechanical pass cannot satisfy this | Subject requirement |

C3 is written against *semantic masks* deliberately. "Two detached antenna islands" does not forbid
some other intentional detached detail and does not fix the total component count at 3, so a raw
`opaque_components == 3` gate would reject a legitimate variation and is not used.

### 6.2 Measured and recorded, but **not** grounds for rejection

Total visible pixels; visible colour count; `opaque_components`; the exact frame/panel/eye hex
values; fractional-alpha pixel count; body footprint, bbox and margins; antenna gap height.
These populate the evidence record and inform the open decisions. None of them is a pass/fail gate,
because none traces to an adopted requirement.

### 6.3 Optional labelled experiments — not production gates

- **E1 palette lock.** Run `reduce_colors` with the reference as `palette_image`, compare against
  the free-colour candidate, and let the user choose. Only becomes a check if the user adopts a
  palette (open decision #1).
- **E2 binary alpha.** Author at alpha 0/255 and record the fractional-alpha count. Until the user
  adopts an alpha policy this is reported, not enforced — so this document contains **no**
  "antialiasing forbidden" rule. If the user later wants selective edge antialiasing, the frame
  corners and antenna edges are where it would be authored and where it would be reviewed against
  both test backgrounds.
- **E3 eye treatment.** Two 1-px light eyes on the panel, as in the reference. The brief does not
  mention eyes, so their presence, count and colour are proposals.
- **E4 reference proportions.** Reproduce the 10 x 8 body and the 2-row gap exactly, versus letting
  the generator choose its own footprint within C1–C5.

### 6.4 Engine import

No destination engine was named, so import behaviour is **unavailable** — recorded as unknown, not
as a pass and not as an artistic failure.

## 7. Open decisions

1. **Palette.** Free colour choice within "dark frame / teal body", or lock to a fixed palette
   (the reference's three colours, or another you name)? A lock turns exact palette membership into
   a rejection rule and puts `reduce_colors` in the pipeline; leaving it free keeps §6.1 as written.
2. **Provider route and budget.** Approve the cheap `create_image_pixen` probe first (1 generation),
   or go straight to `create_1_direction_object` with the reference as a style image (20–40
   generations, 64 candidates, stronger aesthetic match)?
3. **Alpha policy.** Binary alpha, or selective edge antialiasing on the frame and antenna edges?

## 8. Uncertainties and limits of this document

- Nothing here is evidence that a provider *will* produce a matching drone. Every quality statement
  about steps 1 and 2 is an untested expectation.
- The catalog constraints in §5.2 come from a 2026-09-11 documentation snapshot, not from live tool
  discovery; the runtime `inputSchema` is the execution authority.
- The dark-background merging noted in §3 was observed on one background pair with this reference.
- The "matching drone" reading in the assumption at the top is mine; if you meant additional
  members of a drone family rather than a single sample, say so and §5.1 and §6 need a collective
  continuity criterion added.
