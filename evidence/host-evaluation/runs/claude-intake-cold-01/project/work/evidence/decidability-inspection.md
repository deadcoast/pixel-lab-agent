# Visual inspection: is the edge study decidable?

Criterion: `q_study_decidable` (domain visual, mode visual).
Candidate: `x_study` — `work/study/edge-and-canvas-study.md`,
sha256 `724fb21920633a9aa5420fe2ac6bec2b94230a0c93fe90acd1ede76592018e23`.
Reviewer: PIXL (agent). Inspected 2026-09-11, this session.

## What was actually looked at

- `work/study/contact-sheet.png`, sha256
  `bd1eb7c86a695b176fd284307e53b827b7691842db0113855ddef98183274ad1`,
  2384x824, 8 visible colors, 0 fractional-alpha pixels.
- `work/inspect/dark-ground-1px-vs-2px.png` — the weakest-cell crop, 2px rim
  on the left against the 1px rim on the right, dark ground.

Both were opened and viewed as images by the reviewing agent in this session,
not inferred from the generator or from `measurement.json`.

## Layout observed in the contact sheet

Three rows, nine columns. Rows are the three outline treatments in the order
the report's §3 states: 2px as supplied, no outline as supplied, derived 1px.
Columns are three grounds (light, dark, busy checker), each shown at native
scale, x4 and x8. That is every treatment on every ground at native scale and
integer zoom, which is what the criterion asks for.

## Readings, on the image

- **Native scale (columns 1, 4, 7)**: the three rows are not distinguishable
  from one another at this size. The study's claim that the outline decision is
  only observable above 1x holds on the sheet.
- **2px rim, dark ground, x8**: confirmed as the weakest cell. The navy rim sits
  close in value to the near-black ground, the outer boundary stops reading, and
  the two upper prongs fill in solid navy — in the crop they read as dark
  negative space rather than as parts of the figure.
- **2px rim, light and busy grounds, x8**: the rim separates well, but the same
  prong fill-in is visible; the interior teal is visibly squeezed.
- **No outline, light and dark, x8**: clean; the flat teal holds its shape.
- **No outline, busy ground, x8**: the boundary softens against similar-value
  checker clutter. Weakest cell for this treatment, as stated.
- **1px rim, all three grounds, x8**: boundary reads on every ground and the
  prongs stay open teal shapes. The side-by-side crop shows this difference
  directly against the 2px row.

## Verdict reasoning

Pass. Every treatment is shown on every ground at native scale and at integer
zoom, the report names the weakest cell for each treatment in §3, and those
named cells are the ones that actually look weakest when the sheet is viewed.
An owner can settle `edge_treatment` by looking at this material.

## Limitations of this check

- The contact sheet carries no printed row or column labels. Row identity comes
  from §3 of the report, so the sheet is decidable *with* the report beside it,
  not on its own. Recorded as a usability limitation, not a failure of the
  stated criterion.
- This is the agent's inspection. It establishes that the study is decidable. It
  does not choose `edge_treatment`, which is the project owner's call, and it is
  not acceptance of any character art — none exists.
- The subjects are the supplied placeholder forms, not a scout or a medic, so
  nothing here proves how a real pose survives each treatment.
