# Decision card: side-view scout/medic family

Written by PIXL on 2026-11-14 in the isolated evaluation consumer. This is a
research/handoff report, not adopted production state. Production state is
`.pixl/assets/character-family/state.px` (revision 1); the queue is `plar.txt`.

## Question and current authority

| Property | Status | Authority | Source |
| --- | --- | --- | --- |
| View | confirmed: side | user instruction | BRIEF.md lines 5-10 |
| Members | confirmed: scout, medic | user instruction | BRIEF.md lines 5-10 |
| Canvas size | unresolved | user must choose | BRIEF.md line 7 |
| Edge treatment | conflict: continuous dark outline vs none | user must choose | BRIEF.md line 6; reference.png vs reference-b.png |
| Display scale / engine / backgrounds | unresolved | unknown | none |
| Palette roles (body #56B5BC, eyes #F4DDA2, outline #25354A) | observed | reference pixels | BRIEF.md lines 23-29 |
| Alpha binary | observed | reference pixels | BRIEF.md lines 23-29 |
| Identity landmarks (paired ears, light eye mark, tall teal body) | proposed | PIXL | BRIEF.md lines 30-31 |
| Representative sample = scout | proposed | PIXL | none |
| Role cues (scout lean/pack; medic upright/cross) | proposed | PIXL | none |
| Destination assets/characters/<member>.png | proposed | PIXL | none |

No fixed palette, alpha rule or canvas has been adopted. The measured 32x32
reference canvas is available as a proposal only.

## Reference inspection (measured and visually inspected)

- Both references are 32x32, binary alpha, 390 visible pixels, one opaque component,
  visible box x 7..25, y 3..28. Pixel maps were printed; enlargements are in
  `work/reference-x12.png` and `work/reference-b-x12.png`.
- reference.png: continuous 2px #25354A outline around body and both ears.
- reference-b.png: identical silhouette, no outline; the outline band is body color.
- Both are front-facing. A side-view game needs a profile pose, so the references
  supply style and identity, not pose.

## Selected knowledge

- `silhouette-readability` (saved at `work/research/knowledge-silhouette-readability.json`):
  evaluate identity landmarks at the intended scale on representative light, dark
  and busy backgrounds. Applicable: the family identity depends on a few landmarks
  (ear pair, eye mark, body mass) that must survive the profile turn.
- `edge-rhythm` (saved at `work/research/knowledge-edge-rhythm.json`): audit contour
  runs without imposing one contour style. Applicable to reviewing whichever outline
  choice is made; it does not decide between the two.
- The library's executed proofs cover their own fixtures (a 16x16 key, an 8x8
  staircase); they prove nothing about these characters.

## Local diagnostic: outline alternatives on three backgrounds

`work/research/outline-comparison-sheet.png` composites both references at 1x and
4x on a light (#ECECE4), dark (#1C1E28) and busy similar-hue checker background.
These backgrounds are PIXL's synthetic stand-ins because the game's backgrounds are
unknown. Observed:

- Outlined (reference.png): the figure separates from all three backgrounds at 1x and 4x.
- Outline-free (reference-b.png): clean on light and dark; on the busy teal checker
  the body edge dissolves and only the eyes remain clearly visible at 1x.

This is a diagnostic under those conditions, not a rule. If the game's backgrounds
are far from teal, the outline-free style remains viable.

## Recommendation (proposal)

1. Outline: if backgrounds are unknown or varied, prefer the continuous dark outline;
   it is the safer choice for a side-scroller where characters cross many surfaces.
   Alternative: authorize a two-variant scout trial (outlined and outline-free) and
   decide from the actual side-view sample.
2. Canvas: choose from the intended display scale. If the game shows sprites at
   3x or 4x on a 1080p-class screen, 32x32 (the reference canvas) keeps the ear pair
   and one profile eye readable. A 48x48 canvas gives room for role props (pack,
   satchel) and a 2px outline without crowding; 16x16 would lose the paired ears.
   This is a proposal; the owner chooses.
3. Sample order: scout first as the representative sample, then medic against the
   accepted scout baseline, then family review side by side.

## What the answers unlock

- Canvas + outline choice: a concrete raster contract (C) for `scout_sprite`, which
  removes the only blocker on `make_scout_sample`.
- A connected PixelLab tool: `pixl_plar_prepare` for `character.scout` with the
  packet (provider arguments + candidate plan) and discovered connection.
- Engine / display scale: an engine criterion for the delivery and a confirmed
  destination choice, which the delivery task needs to activate.

## Limits

- No provider is connected; nothing has been generated.
- No game code exists in this consumer; consumers and destinations are proposals.
- The comparison sheet uses synthetic backgrounds and front-facing references.
