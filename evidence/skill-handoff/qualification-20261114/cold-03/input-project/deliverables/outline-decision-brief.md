# Outline and canvas decision brief

This is both the decision brief for the project owner and the retained visual
observation backing criterion `q_aid_useful` for candidate `x_aid`.

- **Sheet:** `deliverables/outline-scale-comparison.png`
- **Built from:** the supplied `reference.png` and `reference-b.png` bytes only, enlarged
  by integer nearest-neighbour at 1x, 2x, 3x, 4x, 6x and 8x over light, dark and busy
  backgrounds. No content was redrawn or resampled; the accompanying local check
  (`evidence/aid-faithfulness.json`) confirmed all 36 panels and 14,040 opaque source
  pixels enlarge into uniform blocks with no invented colour.
- **Reviewer:** PIXL (agent), viewed in this session, 2026-09-14.
- **Outcome for `q_aid_useful`:** pass, with one stated limit.

## What the sheet shows

**The outline decision is really a background decision.** This is the finding that
matters, and it is not visible in either reference on its own.

- On the **light** band both treatments read well. The unoutlined teal has ample
  contrast against a pale field and needs no help; the outline adds articulation but is
  not doing separation work.
- On the **dark** band the navy outline is close enough in value to the background that
  it partly disappears. The outlined figure reads as a *smaller* teal shape with a soft
  dark fringe, and the top stalks nearly vanish because they are entirely outline
  colour. The unoutlined figure reads more strongly and holds its full size.
- On the **busy** band the relationship inverts. The dark contour is what lifts the
  outlined figure off the noisy mid-value field, while the unoutlined teal begins to
  blend into it, particularly at the smaller scales.

So: if the game's levels are predominantly dark, the outline in `reference.png` actively
costs readability. If the levels are busy or mid-value, the outline is what makes the
character separable. Choosing the outline without knowing the backgrounds risks picking
the treatment that fails where the game actually is.

**The outline costs apparent size.** At 6x and 8x the teal interior of the outlined
figure is visibly smaller than the full teal body of the unoutlined one. The 2 px
contour consumes 180 of 390 visible pixels. On a canvas smaller than the references'
32 x 32, that cost grows proportionally and leaves very little interior in which a scout
and a medic could differ from one another.

**Legibility of the difference by scale.** At 1x the two treatments are not reliably
distinguishable — the figure is 18 x 25 device pixels and the outline reads as a general
darkening rather than as a contour. At 2x the eyes resolve. From 3x upward the outline
treatment is unambiguous. This is the stated limit on the pass: the sheet supports the
decision at 3x and above, and shows that at 1x the decision barely matters visually.

## What this does not decide

The sheet does not choose for you. Per the bundled `edge-rhythm` method, contour style is
authored intent and must not be resolved mechanically, and per `silhouette-readability`,
no contrast ratio or pixel count proves aesthetic quality. Both treatments are viable;
they serve different backgrounds.

## Bearing on the canvas choice

The two decisions are coupled, so it is worth taking them together:

- Keeping the 2 px outline argues for **32 x 32 or larger**, so that interior area
  remains for role differentiation between the scout and the medic.
- Dropping the outline makes a **smaller canvas** viable, because the full canvas is
  available to the figure — but then the shoulder bar, base bar and solid stalks that the
  navy currently carries have to be re-authored as a second teal value or a cream accent,
  or the characters lose those landmarks entirely.
