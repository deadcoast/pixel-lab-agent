# Character family brief

## Owner instructions (2026-11-14)

1. Make a character family for a side-view game.
2. The family contains two members: a scout and a medic.
3. Style references are `reference.png` and `reference-b.png`.
4. The supplied references disagree about outline treatment; the owner has not chosen between them.
5. The owner has not chosen the final canvas size.
6. This is an isolated PIXL evaluation project. No generation provider is assigned and no network access is allowed in this session; local planning, inspection and state are the authorized work.

## Reference observations (PIXL, measured 2026-11-14)

Both files are 32x32 PNG, fully opaque pixels on a transparent background (no fractional alpha), one connected visible shape, bounding box x 7..25, y 3..28. Both show the same mascot silhouette: a tall rounded-rectangle body with two short ear-like posts on top and two 3x4 cream eyes.

- `reference.png`: three colors. Body fill teal `#56B5BC`, continuous 2px dark navy outline `#25354A` around the whole silhouette, eyes cream `#F4DDA2`.
- `reference-b.png`: two colors. Same teal fill and cream eyes with no outline at all; the silhouette edge is the teal fill against transparency.

These are observations of the supplied images. The 32x32 canvas, the 2px outline width, the exact hex values and the mascot silhouette are not adopted project requirements unless the owner confirms them.

## Open decisions for the owner

- Outline treatment: continuous dark outline (as in `reference.png`), no outline (as in `reference-b.png`), or another treatment such as selective/partial outlines.
- Final canvas size for each character frame.

## Unknown until supplied

- Target engine or renderer, destination paths, display scale, pivots and any animation set. None of these were supplied in this session.
