# Baseline review: decision and next step

Reviewed 2026-09-11 against `reference.png`, the agreed robot identity.

## Decision

**`candidate.png` is rejected as the robot family baseline.** It passes every
mechanical check and fails identity.

The supplied facts were accurate and are recorded as passing: the sprite is
32x32, uses only the three confirmed palette colours (`#25354A`, `#56B5BC`,
`#F4DDA2`), has zero fractional-alpha pixels and one connected opaque component.

Looking at it beside the reference at 12x tells a different story. The candidate
drops two features the reference has:

| Feature | Reference | Candidate | Pixels |
|---|---|---|---|
| Left head antenna | `#25354A` outline at x7-10, y3-8 | fully transparent | 24 lost |
| Right eye | `#F4DDA2` accent at x18-20, y14-17 | repainted body teal `#56B5BC` | 12 lost |

Only 36 of 1024 pixels differ, and the candidate adds no pixel anywhere. That is
precisely why the mechanical gate stayed green: removing pixels and recolouring
within the palette cannot change dimensions, palette membership, alpha or
connectivity. The reference robot is symmetric about the sprite centre in both
head and face; the candidate is a one-antenna, one-eyed robot.

A baseline propagates. Every sibling derived from this sprite would inherit the
missing antenna and missing eye, and after a few family members the defect starts
to look like the family's intended identity. That makes this a cheap fix now and
an expensive one later.

## Next step

1. Revise the sample: restore the left antenna (24 `#25354A` pixels at x7-10,
   y3-8) and the right eye (12 `#F4DDA2` pixels at x18-20, y14-17), so the head
   and face match the reference's bilateral symmetry. The remaining 988 pixels
   already match the reference exactly and should not be touched. If the fix is
   regenerated rather than edited, expect other drift and re-check the whole
   sprite, not just these two regions.
2. Nominate the revision as a new candidate on `f-baseline` in `t-sample`. It
   cannot inherit `v-mech-1`; all three criteria are re-evaluated against the new
   candidate, including a fresh enlarged visual comparison.
3. Only once `t-sample` is done does family production open. `f-baseline` then
   becomes the `bs` baseline for the sibling outputs.

## Still unresolved

`i-destination` (`family_destination`) has no value. The target engine or import
destination for the robot family was never stated. It does not block this sample
review, but a delivery task cannot be activated or completed until it is
confirmed, and no engine-import acceptance has been checked or claimed here.

## What was and was not verified

- Verified locally: dimensions, palette membership, alpha, connectivity
  (`pixl-state/evidence/candidate-mechanical.json`).
- Verified visually: the enlarged three-panel comparison in
  `pixl-state/evidence/candidate-vs-reference.png` was inspected directly.
- Not verified: any engine or destination import behaviour; no PixelLab
  generation was performed in this session.
