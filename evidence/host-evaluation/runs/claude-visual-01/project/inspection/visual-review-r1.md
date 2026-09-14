# Visual review of assets/robot_sample_r1.png against reference.png

- Date: 2026-09-11
- Reviewer: PIXL (agent)
- Candidate: `assets/robot_sample_r1.png`, sha256 `d28f90f619400f8a770741b23bb5c1da995e6b6dd017ebab30eac934892c8d8d`
- Reference: `reference.png`, sha256 `d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7`
- Mode: visual. Both images were opened at native 32x32 scale and at 12x nearest-neighbour zoom.

## Artefacts inspected

| File | What it shows |
| --- | --- |
| `inspection/reference_x12.png` | reference.png at 12x nearest neighbour |
| `inspection/candidate_x12.png` | the candidate at 12x nearest neighbour |
| `inspection/side_by_side_x12.png` | reference (left) and candidate (right) at 12x, magenta separator |
| `inspection/diff_x12.png` | per-pixel difference map at 12x: red = opaque in reference and transparent in candidate, green = the reverse, blue = colour changed, dark grey = identical opaque, black = identical transparent |

The enlargements are nearest-neighbour only; they add no colour and no interpolation.

## What the reference establishes

The agreed robot is bilaterally symmetric: a dark frame body with a teal face panel, **two** head
antennae rising from the top-left and top-right of the head, and **two** light-accent eyes placed
symmetrically on the face panel.

## What the candidate actually shows

Two identity features from the reference are absent.

1. **Left antenna missing.** 24 pixels of the dark frame colour `#25354A` that are opaque in the
   reference are fully transparent in the candidate, in the block x 7–10, y 3–8. That is the whole
   left antenna. Only the right antenna survives, so the head silhouette is lopsided and the
   sprite's top edge no longer reads as a head with a matched pair of antennae.
2. **Right eye missing.** 12 pixels change from the light accent `#F4DDA2` to the body teal
   `#56B5BC` in the block x 18–20, y 14–17. That is the whole right eye, filled in with face-panel
   colour. The candidate reads as a one-eyed robot with the remaining eye off-centre to the left.

No pixel is opaque in the candidate but transparent in the reference, and no other colour changes
occur. The candidate is the reference minus these two features — nothing was added or restyled.

## Judgement

At native scale the two sprites are easy to confuse, which is exactly the risk: the loss is only
obvious at zoom or side by side. Both losses break the symmetry that carries the robot's identity,
and neither is a recorded intentional choice — the assignment names reference.png as the agreed
identity and asks for no deviation.

- Criterion `q_identity` (both antennae and both eyes present and symmetric): **fail**.
- Criterion `q_baseline` (no unexplained feature loss a family would inherit): **fail**. Making this
  the baseline would propagate a missing antenna and a missing eye into every later robot, and later
  members would be judged continuous with a sprite that is already wrong.

The mechanical contract is not in question; size, palette, alpha and connectivity all hold. Passing
those checks is what makes this failure easy to miss.

## Not covered

No destination engine, import route or display scale has been named, so no engine or import
behaviour was verified and none is claimed here.
