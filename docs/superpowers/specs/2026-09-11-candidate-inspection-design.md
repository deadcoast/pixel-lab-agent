# Candidate inspection with retained review evidence

Implements PX-OPS-001 in `evaluations/TODO.spec.md`. The maintainer develops this
operation; PIXL operates it only in a designated production or evaluation project.

## WHO, WHAT, WHERE, WHY

The project owner supplies requirements. PIXL selects applicable saved criteria,
inspects images through its host and supplies judgments. The runtime resolves saved
state, prepares exact inspection inputs, measures declared properties and retains
explicit reviews. Host viewing and target-engine execution remain separate evidence.

The native baseline found repeated ad hoc image/evidence publishers, missing native
view receipts, resized contact sheets and unsupported artistic rules. The operation
must make the useful work reusable without turning those rules into runtime policy.

Implementation belongs in `pixl/inspection.py` (state/publication),
`pixl/inspection_views.py` (bounded deterministic rendering), existing CLI/MCP/service
adapters, and a shared inspection skill reference. PX1 and PX2 schemas and existing
record semantics remain unchanged. Inspection JSON is a versioned retained artifact,
not new UDL syntax.

## Alternatives and decision

1. Extend path-only `asset-check`: small, but cannot recover saved criteria or bind a
   review to a candidate. Preserve this lower-level measurement operation.
2. Prepare and publish an inspection packet, then record an explicit review using
   existing X/E/V records: selected. Saved state and ordinary graph/file validation
   can verify every retained image and semantic dependency.
3. Add new UDL record kinds or a universal artistic judge: unnecessary for this
   operation and unsupported by the observed outcomes.

## Public operation

`inspection-prepare STORE CANDIDATE PACKET OPTIONS_JSON --expect HASH --root ROOT`
resolves an existing raster X with an F owner, its C, task and all required Q.
`OPTIONS_JSON` requires `references` (distinct local S/X IDs; empty is explicit),
integer `scale` (2..16), and nonempty distinct `backgrounds` (`#RRGGBB` or
`checkerboard`). Optional `max_side` defaults to 1024 (64..2048); optional `contexts`
defaults to empty. Defaults are rendering resource choices, not artistic contracts.

Each explicit context uses one captured source ID:

- Frames: `{name, kind:"frames", source, source_frame, rects, durations_ms, pivots}`. `source_frame` is an explicit zero-based decoded frame index. Rects are
  ordered `[x,y,width,height]`; durations are positive integers or null; pivots are
  local `[x,y]` coordinates or null. Arrays have equal lengths. Unknown timing or
  pivot data stays null. Prepare individual frames and a comparison strip; use
  common-pivot alignment only when all supplied pivots are known.
- Tiles: `{name, kind:"tiles", source, source_frame, tile_size:[w,h], grid}`. `source_frame` has the same explicit meaning. Grid is rectangular
  and contains zero-based row-major tile indices from the source. Require exact
  source divisibility and valid indices. Prepare the declared neighborhood; report
  differing adjacent edge-pixel counts as observations, never automatic seam failure.

Capture source bytes once and hash-check them against saved records before rendering.
Retain original encoded inputs, each decoded frame, native and integer-nearest views
on each selected background, and explicit frame/tile contexts. Crop large derived
views into complete logical-pixel regions before integer enlargement; record origin,
scale, source, frame/context and delivered file dimensions for every view. Never
silently omit frames, resample to a fractional scale or manufacture unknown context.
Limit encoded bytes, decoded pixels, view count and aggregate rendered pixels; fail
before publication when a request exceeds the documented limits.

Measure the candidate against C.px/C.pl/C.al using existing asset checks. Reference
properties are observations, not new restrictions. An empty palette stays unrestricted;
connectivity and timing measurements do not become artistic verdicts. The packet marks
visual and engine acceptance unperformed.

The manifest retains canonical tagged bodies and hashes of the original semantic
scope (including X/F/C/Q/I/S), not only references to current records. These bodies
preserve the exact acceptance conditions when current choices or criteria change.

Prepare publishes auxiliary X records for every retained input/view and one report X
for the manifest. Report metadata uses ordinary typed Ref values to link the original
candidate, criteria, references and retained files into the semantic graph. It does
not nominate a candidate, publish E/V, or advance a task. All paths stay inside the
project/store; writes retain immutable bytes and publication uses the expected hash.
As with existing delivery, a failed commit may leave unreferenced immutable files.

A closed inspection loader checks manifest identity, original record bodies/hashes,
typed metadata projection, source/input/view correspondence and every retained file.
The inspection API owns these checks and rejects reused packet IDs. Ordinary PX2
validation verifies file hashes and graph bindings but does not validate arbitrary
report formats or make generic X records immutable. Direct generic edits remain
possible under existing rules; they are not inspection publication and do not acquire
new guarantees. Packet reads distinguish corrupted retained data from current binding
drift, so proper amendments remain readable with their original criterion text.

`inspection-review STORE PACKET REVIEW_ID REVIEW_JSON --expect HASH --root ROOT`
requires a previously published packet and a fresh review ID. The closed review has:

```json
{
  "reviewer": "actor",
  "observed_at": "2026-09-11T22:00:00+00:00",
  "observations": [{"view": "packet.view.0", "delivered_size": [32,32], "note": "Actual viewing observation"}],
  "verdicts": [{"criterion": "q.identity", "status": "fail", "reason": "Observed missing feature", "supersedes": null}],
  "next_action": "Create a separately retained revision and review it again.",
  "limitations": []
}
```

The reviewer must be a saved A. Observation IDs must belong to this packet and cannot
repeat. Record positive delivered dimensions when known, or null when the host does
not establish them; do not substitute file dimensions for an unknown delivery size.
Report resizing or unknown delivery size honestly. Visual/continuity passes require complete native and enlarged
view coverage at the prepared dimensions; visual failures need an actual supplied
candidate-source view observation but may be established before exhaustive inspection.
A reference-only observation cannot establish inspection of the candidate. Missing/partial
coverage remains explicit. This validates the declaration's consistency, not whether
a person/model really looked. Actual host transcripts remain the viewing evidence.

Each supplied criterion must belong to the packet; omitted criteria remain unperformed.
Accept local mechanical and visual/continuity pass/fail observations. Engine/live
criteria can only be marked unavailable here, with an explicit reason and no receipt.
This operation does not manufacture external execution evidence. Preserve existing
V unless a replacement explicitly names that exact current V in `supersedes`.
Require timezone-aware observation time between packet preparation and local recording;
it is a caller-supplied observation time, not independently attested viewing order.

Review retains its JSON as a report X, creates E for each performed criterion with
the exact outcome/mode and complete X/Q/packet/review closure, adds V to T.vr, and uses
ordinary expected-hash commit and saved-plan ordering. It changes neither nomination
nor task status. A done task must first be reopened under the existing rules.

`inspection STATE [PACKET] --root ROOT` verifies retained packet/review files, lists
prepared views, reports declared coverage/resizing, current verdicts and binding drift,
and returns retained next actions. Historical packets remain inspectable after a
proper amendment; stale bindings block new review and require a fresh packet. A new
candidate never inherits a predecessor's verdict.

MCP equivalents: `pixl_inspection`, `pixl_inspection_prepare`,
`pixl_inspection_review`, with the same required inputs and closed envelopes.

## Verification and limits

Prove exact native/nearest pixels, alpha preservation, explicit backgrounds, complete
cropping, multi-frame durations, frame/pivot and tile contexts, resource rejection,
saved-plan/candidate/source binding, old failures, new unperformed candidates, stale
hashes, relocated cold reads, tampering, explicit supersession and honest unavailable
engine checks. Exercise real CLI/MCP and a copied plugin. Reuse the retained missing
antenna/eye fixture as a developer proof: mechanical pass plus explicitly supplied
visual rejection. This remains a controlled fixture, not commissioned production art.

Preserve the current runtime receipts before rebuilding. The completed host baseline
and its frozen package remain untouched and describe their original version. New
skill guidance gets its own bounded native operation trial and explicit limitations.

## Authorization and review

The user selected the next documented target and has authorized continued development.
Proceed through review, implementation and verification without a repeated approval
pause. This existing authorization governs generic skill handoff/commit gates. Preserve
the accumulated dirty development branch; do not commit, reset or remove its work.
