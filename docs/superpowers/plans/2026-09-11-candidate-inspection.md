# Candidate Inspection Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development for the independent renderer, publication implementation and review tasks. Preserve this workspace and prior evidence; no commits or destructive cleanup.

**Goal:** Complete PX-OPS-001 through a reusable packaged inspection and explicit review operation.

**Architecture:** Bounded rendering produces exact view bytes and metadata. The publication layer captures saved dependencies and retains X/E/V through existing validation and commit. CLI/MCP and a skill expose the whole operation.

**Tech Stack:** Existing uv environment, Python standard library, Pillow, PX2, current local MCP.

**Spec:** `docs/superpowers/specs/2026-09-11-candidate-inspection-design.md`.

## Task 1: Exact inspection views

Files: new `pixl/inspection_views.py`, `tests/test_inspection_views.py`.

Interface:

```python
def render(snapshots: dict[str, bytes], candidate_id: str, contract: dict, options: dict) -> dict:
    # Returns files: {relative_path: bytes}, views: [metadata], measurements: dict,
    # inputs: [metadata], options: canonical rendering options, context_observations: list.
    # Each input: {source, path, sha256}; each view: {path, source, frame, context,
    # scale, background, crop:[x,y,w,h], width, height, sha256}.
    # Contract values are plain JSON: px:[w,h], pl:[...], al:"binary"|"full".
    ...
```

- [x] Write and run failing pixel tests for nearest/native, fractional alpha, full coverage crops, explicit frame timing/pivots and tile placement/seam observations.
- [x] Implement limits and deterministic rendering with no state mutation or artistic verdict.
- [x] Run `uv run --no-sync python -m unittest tests.test_inspection_views -v`; retain failures before fixes.
- [x] Review interface, pixels and boundary cases independently.

## Task 2: Saved packet and explicit review

Files: new `pixl/inspection.py`, `tests/test_inspection.py`,
`spec/candidate-inspection.md` (exact implemented artifact/request contract).

Interfaces:

```python
def prepare(folder, expected, candidate_id, packet_id, options, root=None): ...
def review(folder, expected, packet_id, review_id, observation, root=None): ...
def report(doc, root, packet_id=None): ...
```

- [x] Preserve previous changed-file/runtime receipts under `evidence/candidate-inspection/previous/` with hashes.
- [x] Write failing operation tests: prepare creates no verdict, stale state/source blocks, exact X file closure, review rejection with E/V, explicit supersession, partial/resized viewing, unavailable engine, cold relocation and candidate replacement.
- [x] Implement immutable capture and expected-hash publication, using `graph.proof_scope`, `codec.record_hash`, `store.commit` and the renderer interface.
- [x] Implement the design-review corrections: closed manifest/projection checks,
  original semantic record bodies, immutable per-operation packet IDs, readable
  historical drift, and stale-review rejection. Generic X semantics stay unchanged.
- [x] Require closed envelopes and precise IDs/dates; retain declared limitations and next action in review X.
- [x] Run `uv run --no-sync python -m unittest tests.test_inspection -v` and review state/retention boundaries independently.

## Task 3: Packaged operation and proof

Files: `pixl/cli.py`, `pixl/service.py`, `pixl/mcp.py`, new
`tests/test_inspection_operations.py`, shared skill references,
new `scripts/inspection_probe.py`, current development docs and TODO.

- [x] Wire `inspection`, `inspection-prepare`, `inspection-review` and the three MCP equivalents to Task 2; CLI reads closed JSON through `service.read_json`.
- [x] Add process-level CLI/MCP tests with actual temporary stores and saved evidence.
- [x] Document exact request/result contracts and the prepare/view/review/continue skill sequence; keep artistic authority and unavailable context explicit.
- [x] Run the missing-feature fixture through a relocated package, record mechanical success, explicit visual failure, new unperformed candidate and cold report.
- [x] Run a bounded native host trial against the new instruction identity; preserve the earlier host series untouched.
- [x] Run Ruff/Mypy and the source-aware full verifier after archiving prior receipts; inspect all skips/failures and preserve failed runs.
- [x] Perform final independent review, update the MIVIM status from observed proof, and leave the next target explicit.

## Execution ledger

- User authorization: continue the next specified development target; no additional design approval is needed.
- Workspace decision: keep the existing development branch because its accumulated uncommitted milestones are required inputs. Archive before replacing receipts and generated files.
- Design decision: reuse existing X/E/V and ordinary graph bindings; no new wire format or registry extension.
- Verification decision: a local fixture verdict tests retention/publication, while a separate native trial tests instruction use. Neither establishes real provider or engine acceptance.

### Interface preflight

| Tasks | Shared boundary | Check |
| --- | --- | --- |
| 1 / 2 | `render(snapshots, candidate_id, contract, options)` | Byte snapshots enter; relative file bytes, view/input metadata and observations leave. Publication owns IDs/paths/state. |
| 2 / 3 | `prepare`, `review`, `report` | CLI/MCP route the same values and use structured errors. |
| 1 | Rendering and pixel tests | No state, artistic policy or file publication; full/cropped native views retain exact logical pixels. |
| 2 | State/publication tests | Existing semantic closure and commit gates remain authoritative; independent design review checks immutable history. |
| 3 | Packaging and operation proof | Preserve baseline first; archived 145 files before any source/package replacement. |

- Renderer work can begin while the design reviewer finishes the independent
  publication/history checks; that review does not affect pixel transformations.
- Design review resolved: retain original tagged semantic record bodies; validate
  closed manifests and typed projections inside the inspection operation without
  changing generic X semantics; require explicit `source_frame` for contexts.
  Evidence bindings exclude mutable T records. Test amendments as readable drift,
  not corruption, and reject new reviews against stale packets.
- Review declaration clarification: delivered dimensions may be null when unknown.
  Unknown/resized delivery cannot satisfy complete native-scale coverage; an observed
  defect can still justify a failure. This prevents the schema from demanding invented
  host measurements.

### Shared reference verification

- [x] Retain the original native trial instructions and events as the baseline.
- [x] Identify the observed gap: project-specific publishers and incomplete/resized
  viewing receipts (`evidence/host-evaluation/criterion-review.json` and retained
  visual-trial projects). This is a reference/API addition, not a wording-only
  behavior experiment or a claim about causal profile improvement.
- [x] Add one linked inspection reference with entry, exact command forms, actual
  viewing declarations, explicit review publication, recovery and stopping condition.
  Existing skill discovery name/frontmatter remain unchanged.
- [x] Check the reference against the implemented contract and public help/schema.
- [x] Run the saved controlled candidate through the new packaged reference in
  native Claude and Codex sessions; inspect actual events and pixel deliveries.
- [x] Retain any failed trial and correct verified instruction gaps before claiming
  success. No commit/push is part of this authorized working-tree development task.

- First renderer review found four concrete issues despite 12 passing tests:
  aggregate decode checks and context-size checks after allocation, high-memory
  measurement structures, and transparent RGB loss in composed contexts. Corrections
  and their failing regression evidence are assigned to the renderer implementer;
  the same independent reviewer will recheck them before Task 2 integration.
- Renderer gate passed: 18 tests, all 65,536 binary 4x4 component patterns and 150
  seeded full measurement comparisons matched the prior measurement semantics.
  Limits now precede decode/context allocations; nonoverlapping context copies
  preserve hidden RGB. Measurements reject more than 65,536 exact visible colors
  per frame instead of growing an unbounded color set or truncating the count.
  The 512x512 probe's peak Python allocation changed from 86,286,643 to 2,364,562
  bytes; that probe is not a promise of total process memory at maximum input size.
- Task 3 adapter work is owned locally by the controller after Task 2's interface
  preflight. It touches no publication-owned files. Five real CLI/MCP process tests
  pass, including both cross-interface mutation directions, cold report equality,
  expected-hash retry rejection, closed mutation envelopes and path confinement.
  The initial absent-tool failure and the corrected `json_read` test expectation
  are retained separately. No second implementation subagent runs concurrently.
- Publication review clarified the visual-failure boundary: at least one observed
  candidate-source view is required. A reference-only declaration previously passed;
  its exact pre-fix probe is retained. Partial candidate viewing may still justify
  failure, including unknown delivery dimensions, without requiring exhaustive review.
- Final operation review passed strict scalar, candidate-view, aggregate capture,
  historical amendment and adapter checks. Full verification passed 380 tests with
  one privilege skip and 39/39 POCs. The copied package passed 11 operations.
- Native Codex passed the bounded operation. Claude's first attempt correctly rejected
  the image but omitted mechanical review because the contract's unqualified 'Passes'
  wording was ambiguous. Preserve that failure. Clarify only the contract, freeze a
  new package, and repeat Claude: all three outcome categories and actual native/8x
  image deliveries now verified. All 12 isolated replays pass. Native evidence review
  is retained separately; no statistical or production-art claim follows.
- PX-OPS-001 is complete at its defined scope. PX-SKILL-001 is the next target.
