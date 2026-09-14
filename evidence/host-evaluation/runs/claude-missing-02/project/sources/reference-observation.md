# Observation of reference.png

Recorded 2026-09-11 by PIXL. File: `reference.png` in the project root.
SHA-256 of the file bytes: `d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7`.

## Measured (pixl_asset_check plus Pillow color census)

- Mode RGBA, single frame, 32 x 32 pixels.
- 390 pixels with nonzero alpha; 634 fully transparent pixels.
- 0 pixels with fractional alpha. Alpha values present are exactly 0 and 255.
- 3 distinct visible colors.
- 1 opaque connected component under 4-connectivity.
- Visible bounding box (x0, y0, x1, y1) = (7, 3, 25, 28); the art is inset from every edge.

### Exact palette with pixel counts

| Hex | RGBA | Visible pixels | Role read from the image |
| --- | --- | --- | --- |
| `#25354A` | (37, 53, 74, 255) | 180 | Dark outline and antennae |
| `#56B5BC` | (86, 181, 188, 255) | 186 | Teal body fill |
| `#F4DDA2` | (244, 221, 162, 255) | 24 | Pale-yellow eyes (two 2x3 blocks, 12 px each) |

There is no fourth color, so the reference offers no shading ramp and no separate
highlight or antenna color.

## Visually inspected at 12x nearest-neighbor enlargement (`work/reference_x12.png`)

The reference is a schematic color-and-feature key rather than a finished character:

- A single rectangular body with a uniform two-pixel dark outline on all sides, filled flat
  teal. No interior shading, no dithering, no anti-aliasing.
- Two straight vertical antennae rising from the top edge, drawn in the outline color only,
  one near each top corner, separated by a transparent gap.
- Two pale-yellow rectangular eyes on the upper body, evenly spaced, with no pupil and no
  outline of their own.
- No ground shadow, no ground contact cluster, and no detached pixels anywhere.
- The face reads frontally because both eyes sit on the same visible plane and the form is
  bilaterally symmetric. The reference does not itself demonstrate a side view.

## Consequences for the sample

- The palette constraint is exactly three opaque colors. This is the tightest constraint in
  the brief and the one most likely to be missed by a generator.
- Binary alpha and "no ground shadow" are both already true of the reference and are
  directly measurable on a candidate.
- "Side view" comes from the owner's text, not from this image; the image only supplies
  palette, feature inventory, outline weight and flat-fill treatment.
