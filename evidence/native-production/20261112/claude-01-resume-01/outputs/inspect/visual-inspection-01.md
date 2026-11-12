# Visual inspection 01 — sample candidates (specialist pixl:pixl)

Viewed with the host image tool (Read) between 2026-11-12T08:31Z and 08:34Z.
Files viewed (all under work/native-production/inspect/): sheet-4dir-1x-dark.png,
sheet-4dir-3x-dark.png, sheet-4dir-8x-dark.png, sheet-4dir-3x-white.png, east-8x.png,
west-8x.png, north-8x.png, sheet-8dir-6x-dark.png, sheet-4dir-edited-1x-dark.png,
sheet-4dir-edited-3x-dark.png, sheet-4dir-edited-8x-dark.png. Sheets show
south | east | north | west in 32x32 cells (4 px gutters) on #172336 (and white),
scaled by nearest neighbour; delivered sizes as rendered by the host viewer are not
reported by the tool, so native 1x viewing is attested only by the 1x sheet file.
Mechanical numbers come from work/native-production/returned/measurements.json and
pixl_asset_check (inspect/asset-checks.json).

## south (reused, assets/robot/south.png = source bytes)
Unchanged approved identity. Baseline for all comparisons.

## east (candidate.east.raw, generated, sha256 71b35089…1fb4)
- 1x: a narrow navy slab, same height as south, with a bright 1-px teal line on its
  right edge and a post on top. Reads as the robot turned to the right.
- 3x/8x: body [11,22) x rows 9-27; post in profile 8 px wide (cols 12-19) rows 3-8,
  6 px tall as the source posts; teal front edge x=21 rows 11-25 (the source panel's
  row span 11-25 exactly); bottom frame rows 26-27 span [11,21) leaving a 1x2 notch
  under the teal edge at x=21 (minor, invisible at 1x, noted). No eyes (correct in
  strict profile), no added limbs or features; colours navy + teal only.
- Direction: front (teal) edge on the viewer's right = east. Pass.
- Identity/proportions: same height (rows 3-27), same ground line, box volume
  plausible (11 px deep). Pass.
- Alignment: bbox [11,22) centre 16.5 (source 16.0): within 1 px; bottom row 27. Pass.

## north (candidate.north.raw, generated, sha256 db516f78…a3f5)
- 1x/3x/8x: exactly the south silhouette (bbox [7,3,25,28), 390 px) filled with the
  frame navy; both posts; no eyes, no panel. Reads as the plain back of the box.
- Direction: back view, no front features. Pass. Identity: frame colour, both posts
  at the source positions/size, no added features. Pass. Alignment identical to
  south. Pass. (Observation: the back is featureless; the source never defined a
  back, so this is the minimal faithful reading.)

## west, raw (candidate.west.raw, generated, sha256 8209e5f6…f84c)
- 1x/3x/8x: the mirror silhouette of east (body [10,21), post cols 12-19) but
  navy only — no teal front edge. At 1x and 3x it reads as an anonymous navy slab;
  nothing marks the facing except a 1-px post offset that no viewer can read.
- Direction: FAIL (the front/eye panel is not shown turned toward the left edge;
  the facing is unreadable). Continuity with east: FAIL (not its mirror).
- Identity/proportions/alignment/palette/dims/alpha: pass mechanically and visually
  (same height, ground line, post, colours within palette).

## west, edited (candidate.west.edited, sha256 ec96bf63…55a0)
- Exact horizontal mirror of candidate.east.raw (PIL ImageOps.mirror), verified:
  mirror(edited) == east pixel-for-pixel. Differs from raw west in 17 px: the 15-px
  teal front edge at x=10 rows 11-25 (navy -> teal) and (10,26),(10,27) which become
  transparent (east's bottom notch mirrored). Receipt:
  work/native-production/edited/west-mirror-of-east.receipt.json.
- 1x/3x/8x in the 4-direction sheet: south front, east with teal edge right, north
  back, west with teal edge left — the box turns coherently S->E->N->W; equal
  height, ground line and post size throughout. Direction: pass. Identity,
  proportions, alignment: pass. Palette navy + teal only; alpha binary; 32x32.
- Provenance: edited (deterministic), not generated; the raw provider west is
  retained as a rejected candidate.

## Extra returned views (retained, not delivered)
south-east / south-west show the front with eyes at a 3/4 turn; north-east /
north-west are navy backs. Kept in work/native-production/returned/rotations/.
Provider south is byte-identical to the source (sha256 d997cade…70aa7).
