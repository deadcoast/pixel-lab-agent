# Candidate inspection artifact and operation contract, version 1

This operation operates on saved PX2 candidates using existing X/E/V records. It
adds no UDL syntax. The runtime prepares exact local inputs and verifies retained
records; callers supply actual observations and criterion judgments. Preparation,
measurement, declared review, host viewing evidence and engine execution are distinct.

## API and publication

`prepare(folder, expected, candidate_id, packet_id, options, root=None)` requires a
saved raster X with a matching F owner and C, saved owner task and required Q.
`folder` must be a project subdirectory; root defaults to its parent. `expected`
is the current canonical state hash. IDs must be valid PIXL identifiers, fresh,
and leave enough of the 96-character limit for generated suffixes.

Options are closed: required `references` (distinct local S/X IDs; `[]` is explicit),
`scale` (integer 2..16), `backgrounds` (nonempty distinct `#RRGGBB` or `checkerboard`);
optional `max_side` (64..2048, default 1024), `contexts` (default []). Contexts require
explicit `source_frame`. Options impose no universal artistic rules.

Each context is one of these closed objects, with a distinct nonempty name and a
source ID in the candidate plus explicit references:

```json
{"name":"walk","kind":"frames","source":"candidate","source_frame":0,
 "rects":[[0,0,16,16],[16,0,16,16]],"durations_ms":[100,null],
 "pivots":[[8,15],null]}
```

`source_frame` selects an existing zero-based decoded source frame, even for static
images. Rectangles are ordered `[x,y,width,height]`, with nonnegative integer origins,
positive dimensions and complete containment in that frame. `durations_ms` and
`pivots` have exactly the same length as `rects`; duration entries are positive
integer milliseconds or null, pivots are local in-bounds integer `[x,y]` or null.
Unknown values remain null. Individual frames and a comparison strip are retained.
The strip uses common-pivot alignment only if every pivot is known; otherwise it
uses top-left sequential placement. Timing observations do not create animation.

```json
{"name":"neighborhood","kind":"tiles","source":"candidate","source_frame":0,
 "tile_size":[16,16],"grid":[[0,1],[2,3]]}
```

Tile dimensions are positive integers and must divide the selected source exactly.
The nonempty rectangular grid is an array of top-to-bottom rows, with left-to-right
entries; each integer is a zero-based row-major source tile index. The declared
neighborhood is retained with exact RGBA placement. Every horizontal and vertical
neighbor pair reports differing adjacent RGBA edge-pixel counts, never an automatic
seam verdict. Boolean and fractional values are not valid integer fields.

Public adapters use the same request semantics:

```text
inspection-prepare STORE CANDIDATE PACKET OPTIONS_JSON --expect HASH --root ROOT
inspection-review STORE PACKET REVIEW_ID REVIEW_JSON --expect HASH --root ROOT
inspection STATE [PACKET] --root ROOT
```

CLI JSON arguments are local JSON file paths. MCP root is the configured project
root, and the closed tool envelopes are:

```json
{"tool":"pixl_inspection","arguments":{"path":".pixl/state.px","packet_id":"packet"}}
{"tool":"pixl_inspection_prepare","arguments":{"store":".pixl","expect":"HASH","candidate_id":"candidate","packet_id":"packet","options":{"references":[],"scale":8,"backgrounds":["#ffffff"]}}}
{"tool":"pixl_inspection_review","arguments":{"store":".pixl","expect":"HASH","packet_id":"packet","review_id":"review","observation":{}}}
```

`packet_id` is optional only for `pixl_inspection`; the other shown argument keys
are required. The review's observation placeholder must be replaced by the complete
closed review object described below.

Source bytes are captured once and checked against their saved hashes before rendering.
Every encoded input, decoded frame, native transparent view, native background view,
integer-nearest enlarged background view and requested context is retained. Large views
use complete logical crops before enlargement. Packet preparation creates auxiliary
X records of kind `reference` for inputs/views and a kind `report` X for its JSON.
It changes no nomination, task status, E or V. Publication uses ordinary store CAS;
failed publication may leave unreferenced immutable files, as with existing delivery.

The closed manifest keys are `version` (integer 1), `kind` (`packet`), `packet`,
`candidate`, `output`, `task`, `created_at` (timezone-aware timestamp),
`source_state_sha256`, `records`, `rendering`. Each original semantic record has
exactly `id`, `kind`, `fields` (lossless codec tagged JSON), `sha256` (record hash).
The original semantic proof scope includes the candidate, output, contract, required
criteria, explicit references and their semantic dependencies. Mutable task/project
workflow records are excluded by `graph.proof_scope`; task identity is retained.

`rendering` has exactly `inputs`, `views`, `measurements`, `options`,
`context_observations`. Inputs have `source`, `path`, `sha256`, `id`. Views add `id`
to the renderer's `path`, `source`, `frame`, `context`, `scale`, `background`, `crop`,
`width`, `height`, `sha256`. Paths inside the manifest are relative to its directory.
IDs are `PACKET.input.N` and `PACKET.view.N`, zero-based in deterministic render order.
Files live at `STORE/inspections/MANIFEST_SHA256/`; the report is `manifest.json`.
Views returned to a host have project-relative paths, ready for a root-confined viewer.

Packet X metadata is closed and typed: `inspection=packet` (Symbol), `version=1`,
`candidate` (Ref), `scope` (ordered original semantic Refs), `files` (ordered retained
input then view Refs). Auxiliary X metadata is `inspection=file` (Symbol), `source`
(Ref). The loader checks original bodies/hashes, ownership, semantic scope, typed
projection, canonical manifest bytes and every retained file. It deterministically
re-renders retained inputs to validate all nested rendering metadata and exact bytes.
This intentionally trades read cost for a complete closed rendering check.

Renderer ceilings apply equally to preparation and retained packet verification:
64 MiB/source, 256 MiB aggregate sources, 16,384 decoded pixels/axis, 16,777,216 pixels
per frame, 1,024 frames/source, 67,108,864 aggregate decoded pixels, 65,536 exact visible
colors/frame, 4,096 views, 2,048 delivered pixels/axis, 64 MiB/encoded view,
512 MiB aggregate returned files and 134,217,728 rendered pixels. The 65,537th visible
color rejects instead of truncating. Manifests additionally have the codec's 16 MiB
limit. Context-specific limits remain those documented by the renderer.

Prepare returns store `revision`, `hash`, `state`, plus `packet`, `manifest`, `views`,
`measurements`, `criteria`, `files_verified:true`. Criterion entries have `id`, `name`,
`check`, `domain`, `mode`, `status`, `verdict`. Missing verdicts are `unperformed`.

## Explicit review

`review(folder, expected, packet_id, review_id, observation, root=None)` requires
fresh IDs and current retained bindings. A done task must first be reopened. The
closed observation object requires `reviewer`, `observed_at`, `observations`,
`verdicts`, `next_action`, `limitations`. Reviewer names a saved A; observation time
must have an explicit UTC offset and lie between preparation and local recording.
This is caller-declared time, not an attestation that viewing happened.

Each observation has exactly `view`, `delivered_size`, `note`. View IDs must belong to
this packet and cannot repeat. Dimensions are two positive integers or null. Null
means the host has not established dimensions; never copy file dimensions into an
unknown host delivery. Notes and next action are nonempty text; limitations is a
list of nonempty strings, which may be empty.

Each verdict has exactly `criterion`, `status`, `reason`, `supersedes`. Criteria must
be distinct and required by this packet's original output. Reasons are nonempty.
Local criteria accept pass/fail; engine-domain or live-mode criteria accept only
unavailable, without E. Visual/continuity or visual-mode failures need at least one
observed candidate-source view; viewing only references cannot establish a candidate
failure. Visual/continuity or visual-mode passes require every prepared view, including reference and
context native/enlarged variants, observed at its prepared dimensions. Unknown or
resized deliveries cannot satisfy complete coverage. This verifies declaration
consistency; actual viewing transcripts remain separate evidence. Mechanical criteria
with local evidence mode do not require image-view coverage. Their verdicts still
require an explicit caller judgment against the saved criterion; measurements are
not automatically promoted to verdicts.

`supersedes` is null if no current V exists; otherwise it must name that exact current
V for this candidate/criterion. The operation marks that V obsolete and retains it.
It creates `REVIEW.verdict.N` for each declaration and `REVIEW.evidence.N` for each
performed criterion. E binds the exact original candidate/Q scope plus packet, review
and all retained files. It uses the criterion's required mode and declared outcome.
The saved-plan ordering and ordinary graph/store gates remain authoritative.
Omitted criteria stay unperformed unless they already have an existing current V.
A separate candidate inherits no V. Task nomination and status are unchanged.

Review JSON has exactly `version:1`, `kind:review`, `packet`, `review`, `recorded_at`,
`source_state_sha256`, `observation`, `coverage`. Its report X metadata is exactly
`inspection=review` (Symbol), `version=1`, `packet` (Ref). Coverage has `complete`,
`observed`, `missing`, `resized`, `unknown_size`; ID lists are sorted. Review returns
store commit fields plus `packet`, `review`, `verdicts` (new IDs), `coverage`,
`files_verified:true`. Retained next actions and limitations remain in observation.

## Cold reporting and history

`report(doc, root, packet_id=None)` returns `hash`, `files_verified:true`, `packets`.
Each packet has identity/ownership/time, views, measurements, context observations,
original criteria text with current candidate verdicts, `binding_drift` (changed
original semantic IDs), retained `reviews`, `files_verified:true`,
`visual_quality_verified:false`, `engine_import_verified:false`. Those final flags
state the runtime's limits; declared caller verdicts are represented separately.

Proper amendments remain readable with original criterion text; new reviews against
stale packets are rejected. Earlier E/V must be superseded under existing rules when
amending their dependencies. Reporting validates even obsolete inspection E against
its original retained closure and validates review V projections. Closed equivalence
preserves exact scalar types: booleans cannot stand in for integers and fractional
JSON representations cannot replace integer rendering metadata. Retained reads enforce
remaining aggregate source-byte limits before reading each input. Relocation is safe
when the project and its relative store layout are copied together.

These guarantees belong to the inspection APIs. Ordinary generic X records remain
mutable under existing semantics; arbitrary generic edits are not inspection
publication. The loader detects inconsistent retained files, bodies and projections;
it does not establish cryptographic authorship or guarantee discovery after arbitrary
coordinated generic rewriting. Historical receipts are never edited to imply new tests.
