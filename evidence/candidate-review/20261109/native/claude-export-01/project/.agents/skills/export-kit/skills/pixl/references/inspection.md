# Candidate inspection and retained review

Use this operation to review an existing saved raster candidate. The project owns
the requirements; PIXL supplies the observation and judgment. The runtime prepares
exact inputs, reports measurements, and retains the review. Read the implemented
[inspection contract](../../../resources/spec/candidate-inspection.md) for closed
request schemas and result fields.

## Prepare from saved requirements

Read `workflow STATE --root ROOT` and `inspection STATE --root ROOT` before repeating
work. Resolve the candidate X, its output F, contract C and required Q. Save applicable
criteria before preparing views. If requirements or source bytes have changed, retain
the earlier result and prepare a fresh packet against the amended saved plan.

When forming or amending criteria, apply the [authority check](intake-sample.md#keep-authority-through-derived-rules).
Retain the supporting project requirement or proposal through the verdict; an observed
reference property or diagnostic threshold does not become an adopted rejection rule.

Choose actual reference S/X IDs, an integer enlargement and useful backgrounds.
An empty reference list is explicit. For animation or tiles, supply the known decoded
frame and actual rectangles/timing/pivots or tile neighborhood. Unknown timing and
pivots stay null. These options describe how to inspect this project, not a new style
contract. Example options for an existing reference ID:

```json
{"references":["reference"],"scale":8,"backgrounds":["#ffffff","#202838"],"max_side":1024,"contexts":[]}
```

Run `inspection-prepare STORE CANDIDATE PACKET OPTIONS_JSON --expect HASH --root ROOT`
or `pixl_inspection_prepare`. Use a fresh packet ID and the actual current state hash.
The packet retains original bytes, exact decoded frames, native views, nearest-neighbor
enlargements, explicit contexts, measurements and the original acceptance conditions.
Read its result to locate the prepared files and view IDs.

## View, then judge

When the host file viewer omits delivery metadata, use `pixl_inspection` with
`path`, `packet_id` and `view_ids` (1–8 prepared IDs per call). It returns the
actual selected PNG image blocks plus matching hashes and `payload_size` dimensions,
without resizing. View/forward the image blocks, not only their text metadata.
Those dimensions describe this transmitted image payload; record any later host
resizing separately, and keep delivery unknown if the host transforms it without
reporting the result. A tool result alone does not establish that anyone viewed it.

Open the retained candidate and reference views with the host's image viewer. Inspect
native readability and enlarged structure on the selected backgrounds. Use individual
views or complete crops for large inputs; a nominal 1x cell in a resized sheet is not
native-scale viewing. Read animation or tile contexts where the saved criteria require
them. A frame strip retains poses and declared timing; it does not establish playback
or target-engine behavior.

For a repository consumer, start with its existing isolated renderer or integration
runner. Retain actual rendered frames, timing and state transitions, then inspect
the saved native/enlarged pixels. A headless run can supply actual execution and
playback observations without taking control of the user's desktop. Use interactive
computer control only when it adds an observation the project runner cannot provide.

If one viewer or browser fails, use another suitable observation route before
declaring the check unavailable. Review recorded playback as a sequence, including
every required phase and the wrap; distinguish it from a synthetic frame strip.
Check for throttling or skipped phases in the recording. Judge the specific motion
condition from adequate visual and temporal evidence; do not invent a human-only
real-time viewing requirement. Measurements support the specialist's visual
judgment and do not create it automatically.

Record the view IDs actually seen, what each showed and the dimensions delivered by
the host when known. Use `delivered_size: null` when delivery dimensions are unknown;
file dimensions alone do not establish the viewer's delivered dimensions. Report any
resizing. Complete native and enlarged coverage at prepared dimensions is required
for a visual/continuity pass. An observed candidate defect can justify failure before
all views have been inspected; retain at least the actual candidate view and report
the partial coverage honestly. A reference-only observation does not inspect the candidate.

Interpret measurements against the saved criteria. A dimension/palette/alpha result
is mechanical evidence. Component counts, edge differences and reference colors are
observations whose artistic meaning depends on the project. Compare the actual
required features before a visual verdict. Omit unperformed criteria or explicitly
record an unavailable check with its concrete reason. This local operation can record
engine/live criteria only as unavailable; actual external acceptance uses its own
execution evidence.

## Retain and continue

For actual external observations (recorded motion, collective family views or
destination execution), use the [candidate/family review operation](../../../resources/spec/candidate-review.md).
Read `review-context STATE CANDIDATE --root ROOT` / `pixl_review_context` first.
It supplies exact literal criteria, current verdict IDs, semantic `binding_hash`
and canonical `state_hash`. Save explicit observation JSON, then call
`candidate-review STORE CANDIDATE REVIEW_ID REVIEW_JSON --expect STATE_HASH --root ROOT`
or `pixl_candidate_review`. It handles a raster or family manifest and derives
evidence records while retaining exact observation files. Use an existing reviewer
actor, actual observation time, explicit reasons and observations of the required
mode. Do not reuse prior review prose as a claim of new viewing.

Choose `action: "record"`, `"nominate"` or `"complete"` deliberately. Partial,
failed and unavailable checks remain useful records. Completion preserves all
prerequisite, selection, pending-job and acceptance checks. After interruption,
reload state and repeat the identical review ID/JSON; the retained review is reused
and outstanding publication finishes without duplicate verdicts. Do not construct
E/V records by hand for this ordinary operation. Prepared inspection-packet review
below retains its existing coverage rules; this external-observation route does
not certify that a packet was viewed completely.

Write the closed review object described in the contract: saved reviewer A,
timezone-aware `observed_at`, actual view observations, explicit per-criterion
verdicts/reasons, next action and limitations. Record the observation time after
viewing. Use `supersedes: null` for a first verdict; replacing a current verdict must
name that exact V. Use a fresh review ID and the latest state hash with
`inspection-review STORE PACKET REVIEW_ID REVIEW_JSON --expect HASH --root ROOT`
or `pixl_inspection_review`.

The operation retains its report and creates bound E/V for supplied performed checks.
It preserves failures and unavailable checks without nominating a candidate or marking
the task done. Read `inspection` and `workflow` again. Once all required checks and assigned integration are complete, use `task-complete` / `pixl_task_complete` with the accepted candidate IDs; then confirm the saved task is done. A revision is a new candidate;
it begins with unperformed criteria and cannot inherit the rejected candidate's pass.
If scope drift blocks review, amend the plan through the existing lifecycle rules and
prepare fresh views. Do not relabel the old observation as current evidence.

Finish with the actual result, the next useful action and any unresolved requirement.
Cold resumption uses the retained inspection report to recover the exact old inputs,
criterion text, declared viewing limits and next action. Continue through
[sample acceptance](intake-sample.md) or [family production](family-delivery.md) as
appropriate. Successful publication verifies retention, not whether a host truly
looked or an engine accepted the asset.

## Saving exact review results

For large context/review results, set MCP `result_path` or CLI `--result-path` to
a fresh consumer-relative file. The tool writes complete JSON and returns its
path/hash; read that file rather than reconstructing its contents. If export
fails, inspect `operation_result` and current state before repeating a mutation.

