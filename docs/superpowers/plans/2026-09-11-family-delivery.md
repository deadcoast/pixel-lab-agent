# Family delivery implementation plan

> Use superpowers:subagent-driven-development for a bounded family semantic unit, adapters, independent review and fictional evaluation. Integrate snapshot storage locally. Continue the user's existing development authorization without an approval pause.

**Goal:** Carry an explicitly approved sample into planned family members, collective acceptance and a retained local delivery with honest unresolved destination checks.

**Architecture:** Optional PX2 F.bs/F.mb/F.ds and manifest X.xs extend existing lifecycle semantics. Pure family checks, immutable snapshot storage and CLI/MCP/skill adapters share the same checked publication path.

**Tech stack:** Existing Python, unittest, PIXL/2, canonical JSON, local files and stdio MCP; no new dependencies or external execution.

**Spec:** `docs/superpowers/specs/2026-09-11-family-delivery-design.md`.

## Global constraints

- Preserve supplied source bytes, PX1 rules, legacy PX2 semantics and prior milestone evidence.
- Keep the current development branch and its authorized uncommitted work; no reset, global install, merge or push.
- Complete one local operation. A fixture or retained package cannot create artistic/engine acceptance.
- Use expected hashes and saved plans on generic publication as well as public helpers.

## Task 1: Family planning and baseline semantics

Files: `pixl/families.py`, `pixl/registry-v2.json`, `pixl/lifecycle.py`, `tests/family_support.py`, `tests/test_families.py`. Parent wires graph and owns other files.

Interfaces: exact pure functions and return contract in design. `describe` may compose the existing lifecycle report, but must not invoke graph.validate recursively. `blockers` and snapshot blockers must not call lifecycle.blockers recursively.

- [x] Write failing tests for missing bs/mb/ds/xs semantics, baseline acceptance versus merely existing X, cross-project/nested membership, output ownership, destination blockers, scoped proof closure, pending jobs and preserved legacy behavior. Use actual lifecycle fixtures and retained receipt bytes, not mocked verdicts.
- [x] Implement registry 2.2.0 and pure validation/reporting. Add family blockers to lifecycle activation. Build a reusable fixture `family(root, folder=None)` that publishes a tiny synthetic sample and member through saved plans and returns a valid open delivery plan; record its exact IDs in the task report for consumers.
- [x] Run `python -m unittest tests.test_families -v` and focused lifecycle tests; review spec compliance and code quality.

## Task 2: Snapshot, publication and current family acceptance

Files: `pixl/delivery.py`, `pixl/graph.py`, `pixl/store.py`, `tests/test_delivery.py`, `spec/PIXL-2.md`, `spec/family-delivery.md`.

Interfaces: snapshot/report/validate/transitions in design; shared checks call families.validate before lifecycle.validate, then delivery.validate after jobs.validate. Store initialize/commit call delivery.transitions after candidate validation.

- [x] Archive eleven current milestone files before mutation/regeneration.
- [x] Write failing real-file tests: snapshot adds only candidate with exact bytes; collective proof includes baseline/members/destination; rejected/unaccepted members and pending jobs block; stale write/corrupt copies/storage bypass preserve state; membership amendment retains prior package; current verdict cannot bless an old selection; new snapshot requires a previously saved unchanged plan.
- [x] Implement canonical manifest, bounded capture, immutable directory paths, generic publication invariants and cold report. Reuse existing codec/graph/store primitives without changing their original contracts.
- [x] Run focused family/delivery/store/lifecycle/provider tests and correct concrete integration regressions.

## Task 3: Public operations and PIXL skill

Files: `pixl/cli.py`, `pixl/service.py`, `pixl/mcp.py`, `tests/test_family_operations.py`, shared skill references and `agent/PROFILE.md`.

Interfaces: CLI/MCP forms in design. Public `service.family_report(path, root, output_id=None)` wraps delivery.report; service route calls delivery.snapshot.

- [x] First run actual CLI/MCP tests exposing missing family report/snapshot, mutability and project confinement.
- [x] Expose the operations, then write the domain-specific family/continuity/delivery skill using exact saved-plan, comparison and recovery requirements. Update entrypoint links and runtime/profile operation routing.
- [x] Verify cold report, unknown member attempt, actual copied files and unavailable engine acceptance through restarted processes.

## Task 4: Portable verification, review and recorded outcome

Files: packaging probes/tests, documentation, `evidence/family-delivery/`.

- [x] Add one bounded public-operation probe to copied plugin and wheel verification, without importing checkout/runtime fixture helpers into the relocated process.
- [x] Independently review integration and fix reproduced defects. Record failed attempts separately.
- [x] Rebuild only after bundled source/instructions settle; run full suite, wheel, lint/type, static/native instruction and source-identity checks.
- [x] Run one fictional family skill exercise against the exact copied bundle, retaining actual bytes, cold-resume observations and unperformed artistic/engine obligations.
- [x] Bind final receipts and evaluated identities in a development summary, complete the ledger and identify the next existing task.

## Ledger

Ruling: existing stage 4 is actionable, so continue it rather than import another repository's MIVIM doctrine or invent a new TODO format. Source and runtime review identify the missing semantic family dependency and retained delivery operation.

Ruling: preserve the current branch and prior uncommitted work; it is the user's ongoing development context. User authorization already covers implementation and reversible review fixes.

Ruling: use explicit F/X extensions instead of a separate family kind. The operation reuses task prerequisites and Q/V acceptance; its cost is that family output plans are intentionally report-kind deliverables with typed member references.

Ruling: immutable manifests retain their saved membership. Current equality applies to a new snapshot or current acceptance, not to historical existence. This allows honest membership/destination amendments without erasing delivered evidence.

Prior evidence: eleven files archived byte-for-byte under `evidence/family-delivery/previous/manifest.json` before runtime, registry or bundle changes.

Failed attempts: seventeen delivery tests initially failed on the absent module; family tests first exposed the absent module/registry fields; four actual CLI/MCP assertions failed on missing operations. Two further family regressions reproduced candidates omitting xs and report plans carrying raster contracts. They are fixed. Independent storage review found generic snapshot publication could also activate its task, and identified possible manifest path redirection. Two new regressions failed as expected, including an actual Windows junction. Generic snapshot publication now adds exactly one X with every existing record unchanged, and rooted manifest reads reject lexical/resolved path differences. All 21 delivery tests and both structural regressions pass in the final scoped re-review, with no open finding. Unrooted validation's inability to read frozen manifest bytes is explicitly documented; rooted report/store validation supplies that boundary.

Ruling: generic snapshot publication is the same bounded operation as the helper: one new candidate only. Intentional unrelated changes use a separate saved revision. The local package can be retained while destination/adoption or collective acceptance remains unresolved, but cannot activate or complete delivery.

Portable probe: a retained synthetic preaccepted checkpoint supplies input data only; neither its test factory nor the source runtime is imported into the relocated process. Twelve public CLI operations verify real copied members, no automatic acceptance, unavailable engine, amended membership and both historical/current snapshots. This is operation verification, not new evidence that the checkpoint's synthetic visual/live claims happened.

Final integrated verification: 325 tests run, 324 passed, no failures/errors and one existing Windows symlink-privilege skip; 39/39 reference POCs and 93/93 source ranges pass. Wheel: 83 files and 33 public commands. Copied-plugin verification: 32 commands. All 90 bundle entries match current source and generated copies. Ruff passes; default mypy passes 18 modules with its untyped-body limitation. Three skill validators, Codex plugin validation, three native Claude validators and 50 relative links in 16 instruction/spec files pass. All eleven archived files, five supplied sources and PX1 specification/registry bytes remain unchanged.

Recorded exercise: final copied plugin manifest `2c21250554a42804453ed3ea58810b08fd19b6b1fa08b5f0f3b886e14c3837d1`; 49 isolated processes (43 CLI, six MCP) plus an origin check. Unknown member work blocked snapshot creation, supplied synthetic failure permitted reconciliation, and saved membership amendment retained the earlier two-member package while a new one-member snapshot was added. Final revision 17 keeps delivery open, collective continuity unperformed and engine unavailable, with N and a concrete handoff. The earlier source-adapter walkthrough and its synthetic outcomes remain distinct; no retrospective baseline or controlled behavior-improvement claim is made.

Next existing target: stage 5, evaluate exact packaged PIXL instructions across Claude and Codex with retained host/tool behavior and repeated task outcomes. Actual animation/tile continuity, provider execution and target-engine acceptance remain evidence obligations rather than conclusions from local fixtures.

Final evidence recorder correction: the summary builder first treated the scenario's saved `final_state.family` row as a top-level family report and raised `KeyError: families`. Correcting that recorder lookup permits comparison to the actual row; no runtime/source/scenario state changed and no verification run was replaced.
