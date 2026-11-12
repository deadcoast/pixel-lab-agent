# Isolated consumer execution

Use `consumer-execute` / `pixl_consumer_execute` when the project's actual source
modules implement one of the shipped fixed profiles. The operation runs the
consumer in its own headless Chromium process and temporary browser profile,
checks the captures and imports exact-package evidence through NF-06. It needs
local Node and Chromium; it does not install prerequisites. Read the
[execution contract](../../../resources/spec/consumer-execution.md) for the source
API and supported paths. Another engine needs its own appropriate runner.

| Profile | Required source modules | Retained observations |
| --- | --- | --- |
| `queue-motion-v1` | `state`, `view` | Queue states, full/compact views, live normal and reduced-motion playback |
| `sprite-animation-v1` | `animation` | Authored clips, source rectangles, pivots, controlled frame views and separate live playback |
| `tile-neighborhood-v1` | `terrain` | Authored corner selection and rendered tile neighborhoods at requested scales |

Select the profile from the actual consumer source contract. Tile neighborhoods
need no motion fields. Sprite clips own their durations, anchors, pivots and loop
or one-shot behavior; they need no queue state or hold-frame settings. The fixed
tile corner ordering is an adapter contract, not a universal rule for tile art.

From the consumer directory, use the selected Python and installed runner from
[the everyday guide](everyday.md). Supply the current manifest candidate and a
JSON configuration with exact source module paths and every manifest member's
served destination path:

```powershell
pixl consumer-execute $StateFile $Candidate work/consumer-config.json --out work/consumer-01 --root $Project
```

The configuration explicitly names the profile, its exact module keys,
destinations, scales and overall timeout. Queue and sprite profiles additionally
require observed wraps and phase timeout; only queue requires a hold observation
window. Every applicable field is required, and fields from another profile are
rejected. Match the actual consumer contract; do not change its timing, held frame,
art or source to make a check pass. Module paths and served destinations are
relative to the consumer root. CLI STATE and CONFIG_JSON are ordinary filesystem
paths relative to the working directory; MCP state paths are root-relative.
Optional `--node` and `--browser` select existing executables. No desktop session
or hand-written launcher is required.

Use a fresh output directory for each attempt. Read its `result.json` and linked
checks, raw captures and process receipts. `complete` means the scoped execution,
checks and import finished with unchanged inputs and confirmed cleanup. Other
statuses preserve the failed, unavailable, timeout, interrupted or partial
attempt. Follow the recorded reason and use a new directory after correcting it;
do not overwrite a failed attempt. Optional `--result-path` saves a separate
bounded return value; choose a fresh path outside the attempt directory so it
cannot collide with internal receipts. If that export fails, recover the retained
operation result without replaying browser execution.

The queue profile captures normal playback, a live switch to reduced motion and a
switch back on the same page, plus a second page launched in reduced motion.
Normal completion requires actual consecutive frame observations and the requested
wrap count at each requested scale. Reduced-motion coverage records observed held
frames. The consumer owns animation timing and hold selection. Inspect raw
sampling gaps and limits: these are sampled browser observations, not a video or
proof of every intervening display refresh.

The sprite profile captures explicit stepped frames separately from actual
browser playback. The live `playback` phase records observed transitions and
wraps for looping clips, or arrival at the terminal frame for one-shot clips.
Check authored unequal durations and pivot placement against the source; stepped
views alone cannot establish live playback. The tile profile is static: it
retains source-linked neighborhood views with zero clock checks and no motion
phases. Passing pixel comparisons establish the checked placements and bytes,
not seamlessness or artistic quality by themselves.

Open the relevant actual images through the host's image tool and assess the
assigned criteria separately. Return observed counts, source/package hashes,
viewed files, limits and the full import-result locator to the caller. The outer
execution receipt records process execution; the nested NF-06 import truthfully
retains `renderer_executed:false` because import alone executes nothing. A matching
report and passing pixel checks do not establish that a specialist viewed it or
that its art satisfies the assignment.

No state publication, nomination or artistic acceptance occurs here. Explicit
[candidate review](../../../resources/spec/candidate-review.md) remains a separate
operation when assigned. Isolation owns the browser, profile and loopback server;
it is not an OS security sandbox for untrusted project code.
