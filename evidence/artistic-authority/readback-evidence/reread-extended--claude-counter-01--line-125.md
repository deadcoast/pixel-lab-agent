# Drone production approach — matching `small-separated.png`

Date: 2026-09-14
Scope: bounded planning for one drone sprite family matching the supplied reference.
Status: **planning only.** No PX2 state was created or amended, no production art was
generated, and no provider was called. Nothing here is production acceptance.

---

## 1. Authority table

Every restriction later in this document must trace to a row here. "Requirement" means the
project owner established it this session. "Observation" means it was measured from the
supplied file. "Proposal" means this document suggests it and it is **not** binding.

| Property | Value | Standing | Exact source | Applicable scope |
|---|---|---|---|---|
| Canvas size | 16 × 16 logical pixels | **Requirement** | User brief, this session: "a 16 by 16 canvas" | All drone assets in this project |
| Body outline | Thick two-pixel dark frame around the teal body | **Requirement** | User brief: "a thick two-pixel dark frame around the teal body" | All drone assets |
| Body interior | Reads as teal | **Requirement** (qualitative) | User brief: "the teal body" | All drone assets |
| Antennae | Two detached antenna islands | **Requirement** | User brief: "two detached antenna islands" | All drone assets |
| Fixed palette | Not approved | **Unknown — explicitly withheld** | User brief: "I have not approved a fixed palette" | Blocks palette-membership checks project-wide |
| Frame colour | `#25354A` | Observation | Measured, `inspection/reference-measurements.json` | This reference file only |
| Body colour | `#56B5BC` | Observation | Measured, same file | This reference file only |
| Eye colour | `#F4DDA2` | Observation | Measured, same file | This reference file only |
| Visible colour count | 3 | Observation | `pixl_asset_check`, `visible_colors: 3` | This reference file only |
| Opaque components | 3 (body + 2 antenna blocks) | Observation | `pixl_asset_check`, `opaque_components: 3`, 4-connectivity | This reference file only |
| Body rectangle | 10 × 8 at `(3,6)`–`(12,13)` | Observation | Measured | This reference file only |
| Interior cavity | 6 × 4 = 24 px at `(5,8)`–`(10,11)` | Observation | Measured | This reference file only |
| Frame thickness | 2 px on left, right, top, bottom | Observation (confirms the requirement) | Measured `frame_thickness_LRTB: [2,2,2,2]` | This reference file only |
| Antenna blocks | Two 2 × 2 blocks at cols 5–6 and 9–10, rows 2–3 | Observation | Measured | This reference file only |
| Antenna → body gap | 2 empty rows (rows 4–5) | Observation | Measured | This reference file only |
| Eyes | One pixel each at `(6,9)` and `(9,9)` | Observation | Measured | This reference file only |
| Eye clearance to frame | 2 (Chebyshev) — eyes never touch the dark frame | Observation | Measured `eye_min_chebyshev_clearance_to_dark` | This reference file only |
| Alpha levels present | `{0, 255}` only; 0 fractional-alpha pixels | Observation | `pixl_asset_check`, `fractional_alpha_pixels: 0` | This reference file only |
| Alpha policy (straight/premultiplied, allowed levels) | Not established | **Unknown** | Absent from the brief; `k.alpha-contract` requires "RGBA interpretation, straight or premultiplied alpha, and allowed alpha levels" | Blocks any alpha-level rejection rule |
| Target engine / import path | Not named | **Unknown** | Absent from the brief | Blocks engine acceptance |
| Target viewport & integer scale | Not named | **Unknown** | Absent from the brief; `k.integer-presentation` requires "Logical resolution, camera convention and target viewport dimensions" | Blocks presentation acceptance |
| 32 px minimum for thick outlines | Rejected as a rule | Prior-agent proposal, unadopted | `old-assessment.md` | Not in force — see §4 |
| One connected component for all sprites | Rejected as a rule | Prior-agent proposal, unadopted | `old-assessment.md` | Not in force — contradicts the brief — see §4 |
| Lock all props to the three observed colours | Rejected as a rule | Prior-agent proposal, unadopted | `old-assessment.md` | Not in force — see §4 |
| PixelLab provider tools | Not present in this session | Observation | This session's harness exposes only `pixl-local` tools | Blocks dispatch — see §7 |

### Method receipts used

`k.semantic-clusters`, `k.silhouette-readability`, `k.palette-contract`, `k.alpha-contract`,
`k.integer-presentation`, `k.asset-provenance` were retrieved from the installed
`resources/knowledge/library.px`. Each carries a receipt marked `md=local`, `rs=pass`, built on
bounded local fixtures whose own limitation text reads "Bounded local test fixture; no production
aesthetic acceptance." These receipts establish that the local checks run — they do **not**
establish any PixelLab behaviour, engine behaviour, or artistic quality.

---

## 2. What was actually inspected

Supplied file: `small-separated.png`, sha256
`1c45c866f9d11ff57b055f4dacf1e47c8e71f2c99fd6b24f0cb4259ee40cbe5c`, 16 × 16, 88 visible pixels.

Performed this session:

- Mechanical measurement via `pixl_asset_check` and a direct pixel read.
- Exact pixel grid transcription (below).
- Visual viewing of a ×32 nearest-neighbour magnification (`inspection/reference-x32.png`).
- Visual viewing of the sprite composited over synthetic light `#EEEEEA`, near-black `#18181C`,
  and a two-tone "busy" fill, magnified ×20 (`inspection/reference-backgrounds-x20.png`).

Not performed, and therefore not claimed: viewing at native size in a real game context, viewing
against real project backgrounds, any engine import, any animation, any provider generation.

```
   0123456789012345
 0 ................
 1 ................
 2 .....11..11.....     1 = #25354A (dark frame, 64 px)
 3 .....11..11.....     2 = #56B5BC (teal body,   22 px)
 4 ................     3 = #F4DDA2 (eye,          2 px)
 5 ................     . = alpha 0              (168 px)
 6 ...1111111111...
 7 ...1111111111...
 8 ...1122222211...
 9 ...1123223211...
10 ...1122222211...
11 ...1122222211...
12 ...1111111111...
13 ...1111111111...
14 ................
15 ................
```

### Visual finding (diagnostic, within tested conditions)

Against the light and busy fills the silhouette reads cleanly: the two antenna islands separate
clearly from the body, and the teal cavity reads as a face/screen. Against the near-black
`#18181C` fill the dark frame `#25354A` nearly merges with the background — the antenna islands
lose most of their edge and the body's outer boundary becomes hard to locate; the teal cavity
carries the entire read.

Scope of that finding: one synthetic near-black fill, viewed at ×20 magnification. It does not
establish that the drone fails on the project's real dark backgrounds, because no project
background has been supplied. It is the main input to the open palette decision in §8.

---

## 3. The interior budget, stated plainly

This is the real design constraint and it should drive every drone in the family:

- 16 × 16 canvas, body 10 × 8, frame 2 px on all four sides → **6 × 4 = 24 interior pixels**
  for every feature the drone will ever show.
- The reference spends 2 of those 24 on eyes and leaves 22 as flat teal.

So a second interior feature (mouth, vent, status light, panel seam) is affordable, but roughly
three or four small features is the ceiling before the cavity stops reading as a body. Plan drone
variants around that number rather than around a colour count.

---

## 4. Disposition of `old-assessment.md`

`old-assessment.md` was written by an earlier agent about a **different robot**, derived from a
nearest-neighbour downscale of a 32 px source, and records no owner adoption, no measurement on
this drone, and no engine test. Its three proposals are not in force. Two of them are now also
contradicted by direct measurement of the supplied file:

1. **"32 px minimum for thick outlines."** Measured against this drone: false. At 16 px the 2 px
   frame leaves a 6 × 4 interior, and both eyes sit at Chebyshev distance 2 from the nearest dark
   pixel — they do not meet the contour. The prior failure was a property of downscaling a 32 px
   design, not of authoring at 16 px. Authoring natively at 16 × 16 is the approach here.

2. **"One connected component for all sprites."** This directly contradicts the owner's chosen
   aesthetic of two detached antenna islands, and it is unsupported: `k.semantic-clusters` records
   the risks "A semantic cluster need not be a single-color connected component" and "Automatically
   deleting every singleton destroys legitimate detail" — the latter would also delete this drone's
   one-pixel eyes. Not adopted.

3. **"Lock all props to the observed three colours."** The owner has explicitly not approved a
   fixed palette, so there is nothing to lock to. `k.palette-contract` records the risk "A fixed
   small palette is optional art direction, not a universal definition of pixel art" and requires
   "An approved RGBA palette, color-space choice and transparency policy" before its validation
   step applies. `k.asset-provenance` records the parallel risk that legacy project colour
   mandates "are project-specific, not universal art rules." Not adopted.

The file is kept as-is for provenance. Nothing in it becomes a rejection rule.

---

## 5. Production plan

Sample-first. One representative drone is authored and accepted before any batch.

**Step 1 — representative sample.** Produce a single 16 × 16 drone that is *not* a copy of the
reference: same aesthetic, different silhouette details (proposed: a wider 12 × 6 body with one
interior feature added beside the eyes, and antenna islands of a different shape). Producing a
deliberate variation rather than a clone is what tests whether the aesthetic generalises.

**Step 2 — mechanical check.** Run `pixl_asset_check` / the runner's `asset-check` on the
candidate. Record canvas, component count, alpha levels, colour count as *measurements*. Apply
only the rejection rules in §6.

**Step 3 — visual review.** Render the candidate at native size and at a declared integer scale,
and composite it over light, dark and busy backgrounds, as in §2. Inspect by eye. Mechanical
measurement supplies none of this verdict.

**Step 4 — owner decision on the open items in §8**, in particular the palette and the dark
background behaviour, before any batch.

**Step 5 — family extension.** Only after Steps 3 and 4 pass, extend to the remaining drone
variants using the accepted sample as baseline.

Provenance to carry with every produced asset (`k.asset-provenance`): source path
`small-separated.png`, its sha256 as above, adaptation scope "aesthetic reference only — canvas,
frame treatment and detached-antenna treatment reused; geometry and colours re-authored."

---

## 6. Production rejection rules

A candidate is rejected **only** for these. Each traces to a Requirement row in §1, and each has
been tested against a variation that still satisfies the brief.

| # | Rule | Traces to |
|---|---|---|
| R1 | Canvas is exactly 16 × 16 logical pixels. | Requirement: canvas |
| R2 | The body's dark frame is continuous and exactly 2 px thick on all four sides. | Requirement: two-pixel dark frame |
| R3 | The body interior reads as teal and is visually distinct from the frame, judged by eye at review. | Requirement: teal body |
| R4 | At least two opaque islands read as antennae, each disjoint (4-connectivity) from the body and from each other. | Requirement: two detached antenna islands |

R3 is deliberately qualitative. No numeric hue, saturation or contrast threshold is imposed,
because no such number has been approved and `k.silhouette-readability` records that "No contrast
ratio or component count proves aesthetic quality."

R4 says "at least two … read as antennae", not "exactly three components", because a drone with a
third intentional detached detail — a thruster spark, a dropped status pip — still satisfies the
owner's brief. An `opaque_components == 3` check would reject that legal variation, so component
count is a measurement to report, not a rule.

### Explicitly **not** rejection rules

Each of the following would reject a variation that still satisfies the brief, so each is a
measurement or an experiment, never grounds for rejection:

- Exact colours `#25354A` / `#56B5BC` / `#F4DDA2`, or any palette membership at all. No approved
  palette exists.
- Total visible colour count (3, or any other number).
- Exact component count.
- Body dimensions 10 × 8, or its position at `(3,6)`.
- Antenna block size 2 × 2, their columns, or the 2-row gap.
- Eye size, count, or position.
- Alpha levels. The reference happens to be binary-alpha, but no alpha policy has been
  established, so neither "binary alpha only" nor "no antialiasing" is enforceable here. If the
  owner later adopts an alpha policy, this becomes rule R5.
- Minimum canvas size. There is no 32 px floor.

---

## 7. Provider submission

**Blocked this session.** This harness exposes only the `pixl-local` tools. The precise missing
capability is a PixelLab generation tool (a text- or reference-conditioned sprite tool) discoverable
in the harness together with working credentials. No local tool submits, polls or generates.

When that capability is present, the flow is: discover the actual tool and its schema → save intent
with `job-prepare` against the sample's task and output plan → `job-dispatch` to claim once → host
executes → `job-observe` the real result → `job-import` the download as an unaccepted candidate.
None of that is done here.

### Proposed prompt for the representative sample

Every line marked **[proposal]** is this document's suggestion and carries no authority; the
unmarked lines carry the owner's requirements.

> A small robot drone sprite, front view, on a fully transparent background.
> Canvas: exactly 16 by 16 pixels, authored natively at that size.
> The drone's body is a rectangle enclosed by a thick dark outline exactly two pixels thick on
> all four sides. Inside that outline the body is teal.
> Above the body, two antenna shapes float as separate islands, not touching the body and not
> touching each other.
> **[proposal]** Body about 12 by 6 pixels, centred horizontally, leaving the antennae a gap of
> about two rows above it.
> **[proposal]** Inside the teal area, two small light eyes plus one additional small feature
> (a vent or status light), keeping every interior feature clear of the dark outline.
> **[proposal]** Dark outline near `#25354A`, teal body near `#56B5BC`, eyes near `#F4DDA2` —
> supplied as a colour *direction* matching the reference, not as a fixed palette. Deviation
> here is acceptable and will not be rejected.
> **[proposal]** Fully opaque pixels and fully transparent pixels only, no soft edges — offered
> as an experiment to compare against the reference's measured binary alpha, not as a rule.

The three colour hexes and the alpha line are proposals precisely because no palette and no alpha
policy have been approved. A returned candidate that ignores them is a candidate for discussion,
not a failure.

### If the first provider attempt fails

A failed attempt establishes that that attempt failed. It would not establish that the provider
cannot render a two-pixel frame at 16 px, cannot render detached islands, or cannot hit this
aesthetic — one candidate cannot support any of those conclusions.

Practical fallback, scoped to that attempt: hand-author the 16 × 16 sample locally. The whole
sprite is 88 visible pixels; the reference's own structure is fully transcribed in §2, so a
hand-authored sample is a few minutes of work and is subject to the identical rules in §6. This
keeps the sample-first plan moving without asserting any general provider limit.

---

## 8. Open decisions for the owner

1. **Palette (blocking for the batch, not for the sample).** No fixed palette is approved, so §6
   enforces none. Three ways forward: (a) leave it open and judge colour by eye per asset;
   (b) adopt the reference's three colours as the drone family's palette; (c) run a labelled
   palette experiment — generate the sample in two or three colour directions and pick one. Any of
   these is fine; until one is chosen, palette membership cannot be a rejection rule.

2. **Dark-background behaviour.** Against a near-black fill the `#25354A` frame nearly vanished
   (§2). If the drones will sit on dark backgrounds, the frame value likely needs lifting or a
   rim treatment — but that is a guess until real project backgrounds are supplied. Supplying one
   or two actual backgrounds would settle it and would sharpen decision 1 at the same time.

3. **Alpha policy.** Straight or premultiplied, and which alpha levels are allowed. Needed before
   any alpha rule can exist.

4. **Target engine and viewport/integer scale.** Needed before engine import or presentation can
   be verified. Neither is claimed here.

---

## 9. Residual uncertainty

- No artistic acceptance exists for anything in this document. The reference was inspected; no
  candidate has been produced, viewed or accepted.
- The dark-background finding is a diagnostic on synthetic fills at ×20, not a project conclusion.
- The knowledge receipts backing §4 and §6 are bounded local fixtures marked "no production
  aesthetic acceptance"; they support the reasoning, not the outcome.
- No engine import has been attempted or verified.
- No PixelLab call was made, and no claim is made about what PixelLab would return.
