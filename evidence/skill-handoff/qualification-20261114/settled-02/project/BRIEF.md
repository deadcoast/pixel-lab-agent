# Character family brief

Owner instruction recorded on 2026-11-15 (UTC) from the project owner's assignment.

## Assignment

Make a character family for a side-view game using PIXL. The family has two members: a scout and a medic.

## Owner-confirmed choices

1. Outline: the dark outline of `reference.png` (the reference that carries a dark outline; `reference-b.png` is the same figure without that outline).
2. Canvas: 32 by 32 pixels per character.
3. Palette: the agreed teal and cream palette.
4. Transparency: binary (alpha is fully transparent or fully opaque only).
5. View: side view.
6. Display: nearest-neighbor sampling.

## References

- `reference.png`: style reference with the chosen dark outline, teal body and cream details.
- `reference-b.png`: the same figure without the outline; shows the teal and cream fill without the edge treatment. Not the chosen outline treatment.

## Authorization

The owner authorized PIXL to proceed with the choices above. This evaluation project has only the local PIXL runtime configured; no remote generation provider is assigned, and the network, package installation and credential inspection are out of scope for this session.

## Observations (not owner requirements)

Measured from the reference files, recorded as observations only:

- Both references are 32 by 32 with 390 visible pixels, one opaque component, and only alpha 0 or 255.
- `reference.png` uses three opaque colors: dark `#25354A` (outline), teal `#56B5BC` (body), cream `#F4DDA2` (two eye blocks).
- `reference-b.png` uses two opaque colors: teal `#56B5BC` and cream `#F4DDA2`.
- The figure is a simple blocky body with two ear-like projections and two cream eye blocks; it is a style and palette anchor, not a scout or medic silhouette.

The exact hex values above are the measured reference colors. The owner's instruction names the palette by role (teal and cream, plus the dark outline). Whether those exact hex values are the only allowed opaque colors in the family is a specialist proposal for the first sample, not an owner rule.
