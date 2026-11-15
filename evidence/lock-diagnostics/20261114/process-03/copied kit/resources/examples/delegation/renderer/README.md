# Directional robot consumer observation

This bounded renderer loads the existing `src/robot.ts` controller, calls
`spriteFor` for south/east/north/west, and paints the actual destination PNGs at
1x and 3x nearest sampling on `#172336`. These scales and background are observation
conditions. They do not add an owner-approved palette or presentation requirement.
The original planning example stays unchanged; a production evaluation must supply
its own explicit assignment before generating the missing directions.

Run with Node supporting `node:module.stripTypeScriptTypes` and a locally installed
Chrome or Edge. No browser configuration or profile is shared with the user.
The checker uses the existing Python/Pillow environment.

```powershell
node examples/delegation/renderer/capture.mjs --project C:/ABS/CONSUMER --out C:/ABS/CONSUMER/work/robot-capture-01
.venv/Scripts/python.exe examples/delegation/renderer/check.py --project C:/ABS/CONSUMER --capture C:/ABS/CONSUMER/work/robot-capture-01 --out C:/ABS/CONSUMER/work/robot-check-01.json
```

An explicit `--browser C:/ABS/chrome.exe` may be supplied to capture. The output
directory and checker output must be new. Failures preserve their receipts; use a
new path after correction. For interactive inspection, run
`node examples/delegation/renderer/server.mjs --project C:/ABS/CONSUMER` and open
the printed loopback URL, then stop that server when finished.

Required inputs are `src/robot.ts`, `assets/robot-base.png`, and
`assets/robot/{south,east,north,west}.png`. The south file must preserve the exact
base bytes. Each directional output must be a visible transparent 32x32 RGBA PNG.
The actual controller export and `spriteFor` must map every direction to its
matching filename. Missing files, mapping changes, nontransparent images, wrong
dimensions, changed inputs, altered capture files, and mismatched screenshot
pixels fail the mechanical check.

`capture.json` retains observed mappings, source/output hashes, browser identity,
scaled canvas images and their screenshot positions. `inputs.json` binds the
pre-capture inputs and renderer sources; `execution.json` records completion and
owned browser/server/profile cleanup. The checker compares decoded source pixels,
alpha compositing, nearest scaling and screenshot crops independently with Pillow.

The report does **not** decide whether a direction looks correct, whether all views
preserve the robot's identity/volume, or whether the artwork is suitable. Inspect
the source and delivered images plus `destination.png`, then record the visual
review separately. Copying one sprite to every direction can pass the mechanical
checks and still fail that review. The synthetic test fixture does exactly that
to test rendering without claiming new art or directional acceptance.

This supports the existing example controller. It is not a new generic
`consumer-execute` profile or qualification of a separate game engine.
