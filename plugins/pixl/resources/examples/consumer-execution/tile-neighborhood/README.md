# Tile neighborhood execution

`tile-neighborhood-v1` is a reusable, fixed consumer renderer for an explicitly
chosen binary corner convention. It imports the consumer's `terrain` declaration
and calls its actual `tileFor(corners)` function for every rendered cell. It does
not generate tiles, infer a tile convention, score seams, or grant acceptance.

Use the public `pixl consumer-execute` workflow for retained candidate-family
observations. That workflow binds the package manifest, explicit destination map,
source closure, configuration and six renderer files to the observation. This
folder also supports direct isolated diagnostic capture:

```powershell
node examples/consumer-execution/tile-neighborhood/capture.mjs --project C:/project --config C:/project/tile-config.json --out C:/project/fresh-capture
.venv/Scripts/python.exe examples/consumer-execution/tile-neighborhood/check.py --project C:/project --capture C:/project/fresh-capture --out C:/project/fresh-check.json
```

The output directory and check output must be fresh. An installed Chromium
browser is required; `--browser PATH` selects one explicitly. Capture owns its
loopback server, browser process and temporary browser profile, and records their
cleanup. This isolation is not an operating-system sandbox. Failed attempts retain
available inputs, launch details, CDP commands, process logs and execution status.

## Configuration and source contract

The exact configuration fields are:

```json
{
  "version": 1,
  "profile": "tile-neighborhood-v1",
  "modules": {"terrain": "src/terrain.ts"},
  "destinations": {"terrain.tile0": "assets/terrain/tile-0.png"},
  "scales": [1, 3],
  "timeout_seconds": 90
}
```

Expand `destinations` to **sixteen** distinct output-to-PNG entries covering the
exact family. The one-entry excerpt above only illustrates the mapping syntax.
Scales are one to four distinct integers from 1 to 16; the subprocess deadline is
5 to 180 seconds. Source modules may be `.ts`, `.js` or `.mjs` under `src/`.
Imports may use other files under that same source closure. Every source file is
frozen and hashed, whether or not the browser imports it. Destination paths must
be canonical relative PNG paths under `assets/`; redirected paths are rejected.

The source exports `terrain` and `tileFor`:

```javascript
export const terrain = {
  tile_size: [16, 16],
  background: '#172336',
  sampling: 'nearest',
  corner_order: ['nw', 'ne', 'se', 'sw'],
  tiles: {
    '0': {path: 'assets/terrain/tile-0.png'},
    // Declare every ID through '15', exactly matching destination paths.
  },
  neighborhoods: [
    {id: 'island', label: 'Island corners', vertices: [
      [0, 0, 0, 0, 0],
      [0, 1, 1, 1, 0],
      [0, 1, 0, 1, 0],
      [0, 1, 1, 1, 0],
      [0, 0, 0, 0, 0]
    ]}
    // Include repeated uniform areas, straight boundaries, inner/outer
    // corners and diagonal contacts. Together the maps must exercise all 16 IDs.
  ]
};
export function tileFor(corners) {
  return String(corners.reduce((mask, value, bit) => mask + value * 2 ** bit, 0));
}
```

This profile's project convention is **NW=1, NE=2, SE=4, SW=8**, with binary
vertices. It is not a universal pixel-art rule. A cell reads its vertices in that
order and expects the corresponding string ID. A different convention needs an
explicit different profile or migration, not silently reinterpreted art.

The declaration is closed: no additional fields in terrain, tile entries or
neighborhoods. Tiles are 1 to 64 pixels per dimension and every PNG must have
that size. RGB and alpha-bearing PNGs are supported. Each neighborhood has a
unique lowercase identifier, a label of 1 to 120 characters, and a rectangular
binary grid of 2 to 17 vertices per dimension. One to sixteen neighborhoods may
be declared. Each scaled canvas is at most 2048 pixels per dimension and the
combined captures are at most 16 million pixels.

## Inspecting and retaining results

For an interactive local view:

```powershell
node examples/consumer-execution/tile-neighborhood/server.mjs --project C:/project --config C:/project/tile-config.json
```

Open the printed loopback URL and select the neighborhood and scale. The view
uses the same consumer module and actual mapping as the automated capture.

Capture writes one canvas PNG and one full viewport PNG for every neighborhood
and scale: `<id>-<scale>x.png` and `<id>-<scale>x-destination.png`. `capture.json`
records the declared grids, actual cell mappings, exact tile identities, canvas
bounds, sampling settings and screenshot identities. `inputs.json`, `launch.json`,
`execution.json`, `browser-process.json` and `capture-commands.json` preserve the
source, process and cleanup evidence. Existing output is never overwritten.

The independent Pillow checker rebuilds each neighborhood from the exact PNG
bytes and declared corner grids, applies alpha compositing and integer nearest
scaling, then compares both the canvas and screenshot crop. It rejects missing
patterns, incorrect actual mappings, changed sources/assets/configuration,
changed renderer files, missing views, altered retained images and incomplete
cleanup. Its static facts have `clock_checks: 0` and `phases: {}`.

`observation.py` converts retained evidence to the existing NF-06 report using
`--project --capture --context --renderer --destinations --out`. It binds the
exact family and mapped member bytes, retains all raw outputs and source
identities, and records `motion: []`. Views name the members actually used in
each neighborhood. It does not invent animation evidence or acceptance.

A successful mechanical check can still contain visibly wrong material, repeated
artifacts or a poor inner corner. Review the retained native and enlarged views
for those qualities separately. The tests use explicitly labeled synthetic
quadrant pixels; neither their passing results nor this renderer qualifies an
artist, the model, a production art family, or a target engine.
