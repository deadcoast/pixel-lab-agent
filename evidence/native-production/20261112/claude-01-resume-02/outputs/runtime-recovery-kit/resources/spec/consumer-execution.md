# Fixed consumer execution

`consumer-execute` / `pixl_consumer_execute` runs the shipped `queue-motion-v1`
profile against a current retained family candidate. It copies the renderer into
a fresh project-relative attempt, runs its headless capture and checks, then
imports a passing report through the existing [destination observation
contract](destination-observation.md). The result provides an observation ready
for a separate candidate review. It never writes production records, nominates a
candidate, records a verdict, or completes a task.

The profile uses a dedicated browser data directory, a loopback HTTP server and
owned subprocesses. This is process and profile isolation, **not an OS security
sandbox**. Run trusted consumer modules and installed profile resources. Desktop
control is unnecessary for this headless route; interactive inspection remains
available when a reviewer needs it.

## Operation inputs

The runtime API is:

```python
execute(state_path, root, candidate_id, config, out, *, node=None, browser=None)
```

`state_path` names the current production state; `root` is its consumer project.
`candidate_id` must identify a current family manifest candidate. `out` is a
canonical, fresh directory relative to `root`, outside `src` and the production
store. Existing attempts are never overwritten. Paths must remain within the
consumer project and must not resolve through symlinks or redirected parents.

`node` and `browser` optionally select one executable path or executable name.
They do not accept argument lists, shell text, environment overrides or a custom
runner. Windows batch scripts are unsupported. If `node` is absent, the operation
looks for `node` on the current process PATH. If `browser` is absent, the fixed
capture profile discovers its supported local Chromium executable. Nothing is
installed automatically.

Node must provide built-in `node:module.stripTypeScriptTypes`, `WebSocket`, and
`fetch`. A recorded capability probe checks those features before capture.
Unsupported or missing capabilities produce a retained `unavailable` result.
Python helpers use the same Python interpreter as the PIXL operation.

`CONFIG_SCHEMA` in `pixl/consumer_execution.py` is the closed version-1 schema.
Every field below is required; there are no omitted-field defaults:

```json
{
  "version": 1,
  "profile": "queue-motion-v1",
  "modules": {
    "state": "src/queue.ts",
    "view": "src/queue-view-artistic.ts"
  },
  "destinations": {
    "queue.working.output": "assets/working.png",
    "queue.ready.output": "assets/ready.png"
  },
  "scales": [1, 3],
  "observed_wraps": 2,
  "phase_timeout_ms": 10000,
  "hold_ms": 500,
  "timeout_seconds": 90
}
```

The example output IDs are illustrative; use the exact IDs from the candidate's
manifest. `destinations` must map every member output exactly once to its actual
served path under `assets/`. Each destination's bytes must equal the retained
manifest member before execution and after capture/import. Destination paths
must be unique. Mapping a different package member or stale candidate is a
preflight refusal, not a failed art review.

`modules.state` and `modules.view` are distinct canonical paths under `src/`,
with `.js`, `.mjs`, or `.ts` suffixes. Directory names contain ASCII letters,
digits, underscores or hyphens; filenames additionally allow dots. The operation
snapshots the entire confined `src` tree, including transitive inputs, with a
limit of 512 files and 64 MiB. It rejects additions, removals or byte changes
during the attempt. The fixed queue adapter expects `stateAfter` from the state
module, and `statusVisuals`, `statusCell`, `compactStatus`, `display`,
`reducedMotionQuery`, `motionPreference` and `frameAt` from the view module.
`display` supplies cell geometry, frame timing, nearest filtering and background;
consumer descriptors supply assets, frame counts, animation and held-frame
selection. The adapter validates those capabilities and does not infer arbitrary
framework entrypoints.

The queue profile drives `idle`, `started`, `pause`, `ok` and `error` events,
using `stateAfter` and the `statusVisuals` state inventory. Descriptors have
`path`, `label`, `frames`, `motion`, `animate` and, for held playback, `holdFrame`.
For normal animation this profile's checker expects
`floor(max(elapsed, 0) / display.frameMs) % frames`; reduced playback must use the
consumer-selected held frame. That sequence is this queue profile's contract,
not a universal animation or artistic rule.

| Field | Constraint |
| --- | --- |
| `scales` | One to four unique integers, each 1–16 |
| `observed_wraps` | Integer 1–10; counts observed transitions rather than guessed elapsed cycles |
| `phase_timeout_ms` | Integer 1,000–30,000 per playback phase |
| `hold_ms` | Integer 100–5,000 for reduced-motion hold observations |
| `timeout_seconds` | Integer 5–180 shared subprocess deadline |

Booleans and floating-point spellings are not accepted as integer values. Extra
configuration fields are rejected. The timeout bounds subprocess work, including
Node probes, capture, checker and report bridge; local preflight, retention and
bounded cleanup happen around that deadline. A requested phase sequence may need
more time than its deadline, in which case its partial evidence remains available.
The result explicitly reports `timeout_scope: "subprocesses"`; this is not a
whole-operation wall-clock bound on the NF-06 import or local retention work.

## Retained pipeline

Preflight verifies the current review context, frozen manifest, current family
bindings, exact served destinations and source closure. It then reserves `out`
and copies exactly these installed resource files into `out/renderer`:

`capture.mjs`, `server.mjs`, `view.mjs`, `index.html`, `check.py`, `observation.py`.

`service.resource_root()` selects those resources for source checkout, installed
wheel or plugin execution. Original resource paths and copied byte hashes are
retained in `renderer-sources.json`. Both original and copied identities are
rechecked; an edited installed profile or retained copy invalidates the attempt.

The operation writes `config.json`, `review-context.json`, `destinations.json`
(the plain output-to-path mapping) and `inputs.json`. Its fixed commands are:

```text
NODE --version
NODE -e FIXED_CAPABILITY_PROBE
NODE OUT/renderer/capture.mjs --project ROOT --out OUT/capture --config OUT/config.json [--browser BROWSER]
PYTHON OUT/renderer/check.py --project ROOT --capture OUT/capture --out OUT/check.json
PYTHON OUT/renderer/observation.py --project ROOT --capture OUT/capture --context OUT/review-context.json --renderer OUT/renderer --destinations OUT/destinations.json --out OUT/observation.json
```

The exact generated configuration, review context and destination mapping are
frozen from their requested serialized bytes. Their original hashes remain in
`requested_inputs` in the result, even if an external writer changes a retained
file. Confined paths and bytes are checked immediately before each process,
after each phase, before import and during finalization. A changed request stops
the pipeline and cannot silently lower the requested wraps or change bindings.

All subprocesses use argument arrays with `shell=False`. `execution/` contains
per-phase JSON receipts and separate stdout/stderr files. Receipts retain exact
argv, working directory, timestamps, elapsed seconds, PID, return code and owned
cleanup status. `executables.json` records the resolved Node executable/hash and
Python version; the Node version probe and renderer receipt retain runtime and
browser versions. Logs and raw frame payloads remain in files instead of growing
the operation response.

The capture retains raw `capture/capture.json`, PNGs and
`capture/execution.json`, including incomplete phases. The fixed checker covers
full and compact consumers at configured scales, exact delivered assets, actual
painted frames, observed wraps, normal playback, switching to reduced motion,
restoring normal playback and an initially reduced session. `check.json` retains
the checks and detailed observed counts. These are consumer mechanics and timing
facts, not an artistic judgment or a universal frame/scale prescription.

Only a successful capture with confirmed renderer cleanup and passing checks
proceeds to the observation bridge. After another current-binding/input check,
the NF-06 importer verifies and retains the report and its transitive source,
destination and output files under `out/import`. Its deterministic ZIP, preview
files and full import result remain available there. A final identity check
guards the ready observation returned to the caller.

## Result and failure semantics

`out/result.json` retains the bounded operation result. It includes the current
candidate/state/binding/manifest identities, status, phase receipt references,
hashed artifact references, cleanup evidence and limitations. A complete result
also contains `check_summary`, `bundle`, `import_result` and a ready
`observation`. The summary contains pixel/source/clock check totals and per-phase
sample counts with each consumer's distinct observed frame count, transitions,
wraps and skips; detailed samples remain in the referenced files.

| Status | Meaning |
| --- | --- |
| `complete` | Fixed capture/check/bridge and NF-06 import succeeded with unchanged verified inputs |
| `unavailable` | Required executable, installed profile or runtime/browser capability was unavailable |
| `failed` | A subprocess/check/import failed, or current inputs changed |
| `timeout` | The bounded subprocess deadline or renderer phase timed out |
| `interrupted` | Execution received an interruption and retained available evidence |
| `partial` | Available files remain, but cleanup or final evidence retention was not confirmed |

`process_started` distinguishes launching the capture subprocess from
`renderer_executed`, which is true only when the fixed renderer reports that a
browser page began executing. `files_verified` is true only after the complete
verification/import path. `state_written` and `automatic_acceptance` are always
false. `state_changed` reports a concurrent production-state change honestly;
the operation never restores or overwrites another writer's bytes.

Failures preserve useful partial files and do not create a ready review
observation. A checker failure is not an artistic rejection. Invalid config,
stale package binding, mismatched destination bytes and existing output paths
are refused before launch. A final result-write failure raises `consumer_export`
with the operation result in its error context; earlier files remain available.
Use a fresh `out` for retry and inspect the retained failure first. If requesting
an additional surface `result_path` export, choose a separate fresh path, not the
operation's own `out/result.json`.

On Windows, subprocesses are hidden and cleanup uses `taskkill /PID <owned PID>
/T /F`, never a global browser-name kill. On POSIX, a dedicated process group is
terminated with bounded escalation. The renderer cleans its own browser,
temporary profile and loopback server. The outer wrapper retains parent cleanup
uncertainty even if an earlier child receipt claims cleanup completed. Missing
renderer cleanup evidence remains unknown; an exited parent alone is not proof
that all descendants or profile files were cleaned.

Synthetic pipeline and owned-process tests establish orchestration, retention,
failure handling and cleanup mechanics. Real headless consumer runs and native
caller qualification are separate evidence. None of these closes M1, M2 or
broader M3, or substitutes for explicit visual/artistic and consumer acceptance.
