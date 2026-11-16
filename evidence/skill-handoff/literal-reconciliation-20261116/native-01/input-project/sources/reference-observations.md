# Measured observations of the supplied references

Measured 2026-09-14 with the bundled asset check and direct pixel reads, then inspected
visually at native scale and at 12x nearest-neighbour enlargement
(`work/reference-views/`). Measurements are mechanical; the style judgements below are
labelled where they are inference rather than measurement.

## Identity

| | reference.png | reference-b.png |
|---|---|---|
| sha256 | d997cade…70aa7 | e76b40ce…14a12a |
| canvas | 32 x 32 | 32 x 32 |
| visible pixels | 390 | 390 |
| visible bbox | x 7..24, y 3..27 (18 x 25) | identical |
| visible colours | 3 | 2 |
| fractional-alpha pixels | 0 | 0 |
| opaque components (4-connectivity) | 1 | 1 |

## Shared, measured

- Identical alpha mask. Every visible pixel in one is visible in the other.
- Binary alpha in both files: zero fractional-alpha pixels.
- Body colour `#56B5BC` (teal) and detail colour `#F4DDA2` (cream) in both.
- Two cream clusters, each exactly 3 wide x 4 tall: x 11..13 and x 18..20, both y 14..17.
  They read as eyes and are mirror-symmetric about the figure's vertical axis.
- The figure is bilaterally symmetric and front-facing, with two vertical stalks at the
  top separated by a notch.
- No anti-aliasing and no dithering in either file.

## The outline disagreement, measured

The two files differ in exactly 180 pixels, and every one of those differences is the
same substitution: `#25354A` (dark navy) in reference.png becomes `#56B5BC` (teal) in
reference-b.png. There is no other difference.

- **reference.png**: a flat 2-logical-pixel navy outline fully enclosing the teal body.
  The two top stalks are 4 px wide and therefore rendered entirely in outline colour,
  with no teal interior. Two full-width navy bars at y 9..10 and y 26..27 read as a
  shoulder line and a base line. Outline is a single flat colour with no ramp.
- **reference-b.png**: no outline. Flat teal silhouette, cream eyes only. The shoulder
  and base bars and the stalk interiors disappear entirely, because they were drawn in
  the outline colour rather than as separate shapes.

**Inference, not measurement:** the outline in reference.png is not decorative trim. It
carries interior structure (the shoulder bar, the base bar, and the solidity of the
stalks). Dropping it, as reference-b.png does, removes readable landmarks, not just the
contour. A decision for the unoutlined treatment therefore has to re-author that
interior structure in some other way — a second teal value, or a cream accent — rather
than simply deleting the outline colour.

## Coupling between outline and canvas size, inference

A 2 px outline on an 18 x 25 figure spends roughly 46% of the visible pixels (180 of
390) on contour and bars. That ratio is a property of the figure's size, so the outline
decision and the canvas decision are not independent:

- On a canvas materially smaller than 32 x 32, a 2 px outline would leave very little
  interior for a scout/medic to differ in, and the two characters would be hard to tell
  apart.
- On a canvas materially larger than 32 x 32, a 2 px outline thins out visually and
  reads closer to a 1 px line at the reference's apparent weight.

## What the references do not establish

- **Projection.** Both figures are front-facing and symmetric. Neither shows a side
  view, which is the stated destination. The references establish colour, edge language,
  alpha behaviour and detail density; they do not establish the side-view silhouette,
  limb construction, or a facing direction.
- **Scout and medic differentiation.** Neither reference carries role-identifying
  equipment or a distinguishing accent colour.
- **Target display scale, engine, or importer.**
- **Animation poses, cycles, directions or timing.**
