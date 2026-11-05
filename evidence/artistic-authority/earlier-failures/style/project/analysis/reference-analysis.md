# Reference review — translucent-reference.png

Subject: `translucent-reference.png`, sha256 `bda5c9b18e38b60a617877de6e9df6c5bf8e040410e9dfbe6bc85ca501b17132`.
Inspected at native scale, at 8x nearest-neighbour over four backgrounds, and as a per-pixel dump.
Measurements come from `pixl asset-check` and `tools/alpha_treatment_check.py`; the reading notes are visual.

## Measured facts

| Property | Value |
|---|---|
| Canvas | 32 x 32 RGBA, straight (non-premultiplied) alpha |
| Visible pixels | 420 of 1024; bbox x 6..25, y 3..27 (20 x 25) |
| Distinct visible colours | 5 RGBA entries over **3 RGB values** |
| Fractional-alpha pixels | 30 (7.1% of visible pixels) |
| Alpha levels present | 0, 96, 160, 255 — nothing else |
| Fully transparent pixels | all `(0,0,0,0)`; no colour left in the clear region |
| Opaque body | one 4-connected component |

RGB roles:

| Role | RGB | Pixels | Alpha behaviour |
|---|---|---|---|
| structure (frame) | `#25354a` | 180 | opaque only |
| glass / emissive | `#56b5bc` | 216 | opaque **and** the only role with fractional alpha (15 px at 96, 15 px at 160) |
| accent (warm) | `#f4dda2` | 24 | opaque only |

## What the treatment actually is

1. **Translucency is alpha grading on one hue, not colour blending.** The partial pixels carry the
   *identical* RGB as the opaque glass (`#56b5bc`); only alpha changes. No intermediate RGB was
   mixed against a background, so the file composites correctly on any backdrop. This differs from
   the classic pixel-art AA recipe of picking an approved intermediate *colour*
   (`PIXEL-ART-DEEP-RESEARCH.md` 590-632) and is the more portable of the two choices.
2. **Anti-aliasing is selective by role, not by edge.** Structure and accent are strictly binary
   alpha. The silhouette itself is hard: the frame corners and the outer contour have no softened
   pixels at all. Nothing here smooths a stair-step.
3. **The partial alpha is a glow fringe, not edge softening.** All 30 pixels sit in two 1-pixel
   vertical columns immediately outside the frame (x=6 and x=25), spanning exactly the rows that
   contain glass (y=11..25). The lamp/window bleeds light sideways past its frame.
4. **The fringe is directional.** Left column alpha 96 (37.6%), right column alpha 160 (62.7%).
   The right side is consistently brighter — the family has a light bias to the right.
5. **Exactly two fractional steps.** A 2-level ramp, not a smooth falloff.

## Reproducibility proof (executed)

`evidence/fringe-rule-proof.json`: stripping all 30 fractional pixels and re-deriving them with
`tools/apply_glow_fringe.py` (glass `#56b5bc`, left 96, right 160, one pixel outside the silhouette
on every glass row) reproduces the file **byte-identically** — same sha256. The treatment is a
deterministic post-process over an opaque body, not hand-placed texture. That is the single most
useful fact for production: the new prop should get its translucency from the same rule rather than
from a generator's own edge pixels.

`evidence/reference-treatment-check.json` and `evidence/mutant-check.json`: the contract gate passes
the reference and rejects a mutant that gives an accent pixel fractional alpha and introduces one
off-palette RGB.

## Visual reading (inspected, not measured)

- At native size the object reads as a chunky framed lamp/window: 2px frame everywhere, two 4px-wide
  prongs on top with a 10px gap, two 3x4 warm blocks in the glass. Very flat — no shading ramp on any
  role, a single value per material plus the accent.
- Over dark (`#18181c`) and mid-green (`#4a7c56`) backgrounds the fringe reads clearly as a soft
  light bleed. Over light grey (`#eeeeee`) the alpha-96 left column is effectively invisible and the
  alpha-160 right column is barely present.
- **Consequence for the lantern:** the encoding is background-independent, but the *effect* is not.
  A cool 37%-alpha halo carries almost no signal on light scenery. The set of backgrounds the game
  actually uses is an open question that changes the halo's alpha levels or hue.

## Open questions raised by the reference

- Projection and destination: the image is a flat frontal elevation with no ground contact, so it
  suits a side view or a UI slot. Whether the game is side-on or top-down changes whether the lantern
  needs a base shadow, and top-down would also make a symmetric halo more natural than this
  left/right pair.
- Backgrounds the asset must survive (see above).
- Display scale and filtering in the destination engine — a fractional halo one pixel wide is the
  first thing a non-integer scale or bilinear sampling destroys.
- Whether the reference is itself final art or a fixture: the geometry is perfectly rectangular and
  every material is a single flat value, which is unusually schematic for finished art. The rules
  above are safe to inherit either way, but "match the reference's level of detail" and "match the
  reference's treatment" are different instructions, and only the second one was given.
