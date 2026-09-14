# Intake and representative-sample implementation plan

> Use superpowers:subagent-driven-development for independent codec work and bounded reviews; integrate graph, store and operations locally. Continue within the user's development authorization.

**Goal:** PIXL can preserve incomplete intake, plan a representative sample before its file exists, and accept it only against its declared criteria.

**Architecture:** An explicit PX2 header and registry add I/F/Q/V lifecycle records. Shared graph/store primitives retain PX1 semantics; a lifecycle module validates new requirements and reports next work. CLI/MCP and an operational skill expose the complete path.

**Tech stack:** Existing Python 3.11+, unittest, stdio MCP, .px state, local file evidence.

**Spec:** `docs/superpowers/specs/2026-09-11-intake-sample-design.md`.

## Constraints

- Retain all working source-provenance changes and original supplied bytes.
- Keep PIXL/1 registry/spec/encoding semantics intact; reject store format changes.
- Use real files for X/E and preserve failed, superseded and unavailable observations.
- No remote submission or automatic production acceptance.
- Work in the current development branch; no reset, overwrite of earlier review, or global configuration.

## Tasks

### 1. Versioned codec

Files: `pixl/codec.py`, `tests/test_versions.py`.
Interface: `Document(revision, records, format=1)`; parse/encode PX1/PX2, reject other formats; unchanged record_hash.
- [x] Test `encode(parse(old_wire)) == old_canonical`, PX2 roundtrip, unknown format failure and preserved record hashes.
- [x] Implement explicit format handling; run version/language tests.

### 2. Typed lifecycle and persistence

Files: `pixl/registry-v2.json`, `pixl/lifecycle.py`, `pixl/graph.py`, `pixl/store.py`, `tests/test_lifecycle*.py`.
Interface: `lifecycle.validate(doc, scope, bound)`, `lifecycle.blockers(doc, task)`, `lifecycle.report(doc)` after generic graph validation; graph chooses registry by doc.format and delegates PX2-specific rules.
- [x] Add failing state tests for unknown/proposed/confirmed intake, plans without X, independent criterion verdicts, wrong bindings, completion, immutable V and drift/reopening.
- [x] Implement registry and lifecycle validation, adapt only versioned branches in graph/store, preserve PX1 behavior.
- [x] Exercise incomplete intake -> planned sample -> rejected candidate -> revised candidate -> partial acceptance -> full acceptance -> cold resume and changed contract.

### 3. Operations, skill, distribution and independent review

Files: `pixl/service.py`, `pixl/cli.py`, `pixl/mcp.py`, `spec/PIXL-2.md`, common skill and references, packaging checks, current docs/evidence.
Interfaces: CLI `intake`, `workflow`; MCP `pixl_intake`, `pixl_workflow`; version-preserving host adapter. New stores default PX2 only through intake; legacy init remains PX1.
- [x] Add failing adapter/CLI/MCP tests for intake, format preservation and persisted workflow reporting.
- [x] Implement operations and teach the exact sample procedure with a versioned example.
- [x] Archive prior evidence, regenerate library/examples/bundle, execute full suite, wheel, lint/type and instruction checks.
- [x] Independently review the complete operation and run a bounded skill scenario; correct concrete failures and document final evidence.

## Ledger

Ruling: PX2 is explicit and opt-in through intake; no automatic upgrade of old stores. Existing declarations do not tell us which defaults were agreed or which criteria were required, so automatic conversion would invent facts.

Ruling: retain the existing branch and uncommitted first-milestone work. A fresh checkout would lose the just-developed source operation; the user's request continues that development.

Codec task: eight new version tests plus five language tests pass. The former PX2 unsupported-header test now uses PX3, while PX1 canonical bytes and record hashes are pinned unchanged. No implicit conversion is introduced.

Lifecycle task: 41 new validation/report tests pass. Ruling: open production/delivery plans may lack an adopted D, but activation cannot; source inputs may intentionally have another project's style. Contract choices only gate their actual outputs. Keys remain unique within a project.

Ruling after cold-resume regression: retain a concrete C/X when its choice becomes unresolved/conflicting, then block dependent active/done work. Globally rejecting that C made it impossible to preserve new uncertainty. Three focused tests first exposed rejection/missing report detail, then passed after activation gating and actionable requirement reports were added.

Persistence task: six store tests and six operation tests pass. Two original failures showed missing prospective-plan checks at initialize/commit; those checks now run after structural/file validation. The CLI roundtrip test's empty-stdout mistake was corrected to inspect the `--out` file. Existing completed tasks require reopening for relevant changes, while unrelated project choices do not invalidate them.

Independent review: fixed the intake MCP read-only annotation and a newly superseded V loophole. The latter reproduced a new unsupported historical pass; new V must now be published valid before later supersession. The regression passed after the fix; a companion planning-order fixture was simplified because its invented superseded records were also correctly rejected. Scoped re-review confirmed rejection of new superseded pass/fail/unavailable V at initialization and commit, while genuine published history still supersedes. No remaining finding was reported. Invalid-reference probes return PixlError and preserve stored state.

Automated result: 202 tests, 201 passed, one Windows symlink-privilege skip; 39/39 reference POCs, 93/93 source ranges, five unchanged supplied source documents. Ten wheel operations pass on a 73-file temporary installation; the copied plugin contains 78 verified manifest files. Ruff and mypy pass. Three Codex skill checks, Codex plugin validation, three native Claude checks and 30 relative links pass. Historical source-milestone evidence is retained in `evidence/intake-sample/previous/`.

Bounded behavior result: an independent developer-agent completed two fictional scenarios against a fresh copied plugin, retaining 78 operations and 28 project files in `evidence/intake-sample/behavior-evaluation.json`. Unknown canvas and conflicting edge directions survived CLI/MCP cold starts without invented contracts, assets or adoption. A supplied visual failure blocked sample completion; missing adoption blocked production completion. Revision handoff retained the earlier X/E/V records and exposed the next ready task. No skill blocker was found. These scripted and inspected scenarios use synthetic verdicts and establish neither actual artistic acceptance nor engine integration.

Failed evaluation attempts remain in that report: the first copy failed manifest preflight while instructions were being edited; evaluation proceeded with a newly copied coherent bundle. Recorder syntax, stderr parsing and expected diagnostic-code mistakes are recorded separately from the correct runtime rejections. The evaluated snapshot retains its own manifest identity; later generated POC timestamps do not overwrite that history.

Next development target: durable provider intent, submission observations and recovery linked to project tasks, output plans and imported candidate artifacts. Current `prepare` and `job` remain local caller-supplied operations; actual provider execution and reconciliation require further development and evidence.
