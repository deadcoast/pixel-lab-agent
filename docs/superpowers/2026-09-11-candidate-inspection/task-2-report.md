# Task 2 implementation and self-review report

Implemented `pixl/inspection.py`, `tests/test_inspection.py`, and
`spec/candidate-inspection.md`. No core schema, graph/store, adapter, renderer,
generated build or provider execution changes were made by this task.

## Concrete boundary

- `prepare(folder, expected, candidate_id, packet_id, options, root=None)` returns
  store commit fields plus packet ID, manifest path, project-relative views,
  measurements, original criteria and `files_verified:true`.
- View IDs are `PACKET.view.N`; input IDs are `PACKET.input.N`. Inputs/views are
  auxiliary X `kd=reference`; JSON artifacts are X `kd=report`.
- `review(folder, expected, packet_id, review_id, observation, root=None)` returns
  commit fields, packet/review IDs, created `REVIEW.verdict.N` IDs and coverage.
- `report(doc, root, packet_id=None)` returns current hash, verified packets and
  `files_verified:true`; packet reports retain original criteria, current verdicts,
  binding drift, views/measurements/context facts and exact review declarations.

## Retention and lifecycle

Original semantic record bodies use lossless tagged codec JSON and individual
canonical record hashes. The exact scope comes from `graph.proof_scope`, excluding
mutable T and P workflow records while retaining saved output/task identity.
Captured inputs are verified against source hashes before rendering. Manifest bytes
are canonical JSON, content-addressed under the store, written once, and published
through ordinary expected-hash commit. Generated IDs are checked before writes.

Packet reads reconstruct original semantic bodies and deterministically re-render
retained exact inputs to verify every nested rendering field and each retained
file. The full typed metadata projection is checked. This provides a closed loader
without changing generic X mutability; coordinated arbitrary generic rewrites are
not treated as authenticated inspection publications. Read cost includes rendering
and can be substantial at the documented renderer limits.

Review publication validates timezone-aware declared observation time, saved actor,
closed observations/verdicts, explicit null or actual delivered dimensions, complete
pass coverage, partial failure observations, unavailable live/engine criteria, and
exact current-V supersession. It creates E with full packet/review/candidate/Q/file
closure and V in existing task history; nomination/status do not advance. Done tasks
must first reopen. Existing saved-plan and CAS gates remain authoritative.

Historical amendments retain original Q text and report binding drift. Stale packets
cannot receive new review. Reporting verifies even superseded inspection E against
its original closure and matches retained V to review JSON. Generic tag removal is
also detected for reports retained in inspection storage. New candidates inherit no
verdicts.

## Test-first and self-review evidence

Initial tests failed before the implementation existed; preserved as
`evidence/candidate-inspection/task-2-red.txt`. The first implementation passed eight
operation tests (`task-2-first.txt`). Self-review added failing regressions for
malformed reviewer input and weakened obsolete E closure (`task-2-self-review-red.txt`),
then fixed structured validation and original-receipt reconstruction. A separate
failing tag-removal regression is preserved in `task-2-tag-red.txt` before its fix.

Current focused evidence:

- `task-2-final.txt`: 11/11 operation tests pass.
- `task-2-ruff.txt`: Ruff clean for the new module and tests.
- `task-2-mypy.txt`: Mypy succeeds for the new module; existing untyped-body note
  from job_history is informational.

Covered outcomes include no preparation verdict, relocated cold read, retained
visual failure, exact explicit supersession, partial/resized/unknown pass rejection,
complete coverage pass, engine unavailable without receipts, stale CAS/source/ID
rejection, original Q preservation after amendment, typed projection tampering,
new-candidate unperformed status, obsolete receipt integrity and malformed envelopes.

These are developer fixtures and local state/publication proofs. They do not prove
profile instruction following, actual visual observation, artistic correctness,
live PixelLab execution or target-engine acceptance. Independent operation review
and root-owned adapter/probe/package verification are separate gates.

## Independent review corrections

The reviewer and root identified two further concrete issues despite passing focused
tests: reference-only viewing could declare candidate failure, and Python equality
could accept bool/int or float/int substitutions in closed retained metadata. Their
original probes and outputs remain under evidence/candidate-inspection. Added failing
regressions are preserved in `task-2-independent-review-red.txt`.

The design was clarified to require a candidate-source view for a performed visual
or continuity verdict. Comparison now uses canonical tagged JSON bytes throughout
closed projections/rendering/coverage and hashes for original/current records, retaining
scalar distinctions. A canonical rehashed manifest with float width is rejected.
Root also identified the loader's aggregate input-read timing: reads now use the
remaining aggregate byte allowance and validate options/input counts beforehand.

Final focused run is now **14/14 tests passing**, with Ruff and Mypy still clean.
This supersedes the earlier 11-test count above; prior failing evidence remains intact.
Independent reviewer is rechecking these final corrections before declaring the gate.

## Post-native reference clarification

The first native trial exposed ambiguity in the normative reference: after describing
visual failures, the sentence "Passes require every prepared view" did not explicitly
limit that requirement to visual/continuity or visual-mode verdicts. Claude interpreted
it as applying to mechanical judgments and omitted a mechanical verdict despite available
measurements. The runtime, design and shared reference already scope that coverage gate.

Clarified only `spec/candidate-inspection.md`: visual/continuity or visual-mode passes
require complete prepared-view coverage; mechanical criteria with local evidence mode
do not require image-view coverage. Mechanical verdicts still require explicit judgment
against the saved criterion and are not automatically promoted measurements.

This is a reference wording clarification, with no runtime changes, new tests or bundle
rebuild performed by Task 2. Earlier reports and evidence remain intact. Root retains
the first trial and frozen package and will prepare a separately named repeat series;
this clarification alone does not establish improved native behavior.
