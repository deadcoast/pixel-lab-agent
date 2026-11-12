# Visual inspection 02 — renderer capture render-01 and the delivered family

Viewed with the host image tool (Read) at 2026-11-12T08:48Z, after
`node renderer-native/capture.mjs --project . --out work/native-production/render-01`
(exit 0, status complete, browser/server/profile cleaned up) and
`renderer-native/check.py ... --out work/native-production/renderer-check-01.json`
(status pass, 6 input checks, 5 renderer checks, 8 pixel checks, 8 screenshot checks,
no failures). Capture sha256 0cd3eeab…25f24; check report sha256 be903fae…5d8e.

Files viewed (work/native-production/render-01/):
- destination.png (900x700 RGB page screenshot): heading "Directional robot consumer",
  a Facing / 1x / 3x table with south, east, north, west rows on #172336, footer
  "All four controller paths loaded. Identity and directional art quality require
  visual review." Each 1x cell shows the sprite at native size; each 3x cell shows it
  with hard nearest-neighbour blocks (no blur, no fringe), fully inside its cell.
- south-1x.png, east-1x.png, north-1x.png, west-1x.png (32x32 RGBA cells): south front
  with eyes; east narrow slab with the teal edge on the right; north plain navy back;
  west narrow slab with the teal edge on the left. Transparent around the robot
  (viewer shows the checker/none), same ground line in all four.
- south-3x.png, east-3x.png, north-3x.png, west-3x.png (96x96 RGBA cells): crisp 3x3
  blocks; the four facings share height, ground line, post height and colours; the
  box turns coherently south -> east (front edge right) -> north (back) -> west
  (front edge left). No cropping, misplacement or resampling softness.

Judgment for the family criteria:
- continuity: pass (same robot, same volume/height/ground line/colours; turn coherent).
- direction_mapping: pass (south.png front, east.png right, north.png back, west.png
  left at the controller paths spriteFor(facing)).
- renderer_mechanical: pass per renderer-check-01.json (live evidence of the actual
  consumer renderer run on the delivered bytes with the unchanged src/robot.ts).
- renderer_visual: pass (destination.png and all eight cells viewed as above).

Provenance reminder visible in the capture: east/north are the official provider
rotations; west is the specialist's deterministic mirror of the official east
(edited); south is the unchanged base bytes.
