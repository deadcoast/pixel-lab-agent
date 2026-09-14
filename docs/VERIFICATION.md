# Verification and limits

## Build and verification repair, 2026-09-14

The [ecosystem audit](../evidence/reviews/2026-09-13-ecosystem/README.md) retains the
failing build, the complete failing baseline suite, regression failures, and fresh
results. Earlier sections below describe historical runs. Their passing counts
do not certify the current checkout or complete modules.

Use the existing uv environment:

```powershell
uv sync --locked
uv run --no-sync python scripts/verify.py
uv build
```

The verifier discovers every test under `tests/`, regenerates reference proofs and
the portable plugin, and exercises `checkout -> sdist -> wheel -> temporary
installation`. The installation reuses the selected environment's dependencies;
it does not prove a clean dependency installation on another OS or Python version.

Each verification attempt archives the previous generated outputs before replacing
them, records its own logs under `evidence/verification-runs/`, and publishes a
current [result](../evidence/test-results.json). Import, source, test and build
errors produce failure records. Unreached stages remain `not_run`. A successful
file-hash comparison establishes byte identity, not coverage or correctness of
every function in that file.

Coverage is a separate measurement using the uv development dependency:

```powershell
uv run --no-sync python -m coverage run --data-file build/coverage-data scripts/verify.py
uv run --no-sync python -m coverage combine --data-file build/coverage-data
uv run --no-sync python -m coverage report --data-file build/coverage-data
uv run --no-sync python -m coverage json --data-file build/coverage-data -o build/coverage.json
```

Coverage includes branches and uses Coverage.py's [subprocess instrumentation](https://coverage.readthedocs.io/en/latest/subprocess.html).
The report measures the checkout's `pixl/` runtime. Copied and installed runtimes
are exercised by the packaging checks; their separate file paths are not merged
into the checkout's coverage percentages. Percentages measure executed code, not
assertion quality, complete input coverage, artistic judgment or production readiness.
Use a new data-file prefix to retain separate measurement attempts.

Static checks have their own scope and exit status:

```powershell
uv run --no-sync python -m ruff check pixl scripts tests evaluations setup.py plugins/pixl/runtime plugins/pixl/resources/pixl plugins/pixl/scripts
uv run --no-sync python -m mypy --check-untyped-defs pixl
uv run --no-sync python -m mypy --check-untyped-defs --explicit-package-bases scripts evaluations setup.py
```

The [follow-up development evidence](../evidence/development/2026-09-14-typing-adapters/README.md)
retains the original 24 Mypy diagnostics and the passing check of all 36 maintained
runtime, build and evaluation source files with `--check-untyped-defs`. These files
still contain unannotated interfaces: this is not a claim of complete static typing.
Historical training scripts and frozen evaluation packages are evidence inputs,
outside the maintained-code lint command above. This repair does not run new
agent-behavior trials, PixelLab generation, visual acceptance or target-engine acceptance.

Host JSON files and MCP input now reject repeated object member names, including
escaped spellings of the same name. Previously the decoder silently retained the
last value and could publish a different document or initialize a different store.
CLI input failures return `json_read` before writing output; MCP returns a parse
error before dispatch and continues reading subsequent requests. Repeated names
in different objects remain valid. PX1/PX2 wire syntax and saved-state semantics
are unchanged. Process-level regression failures and passing results are retained
in the follow-up evidence; they establish these input behaviors, not completeness
of the CLI, MCP or service modules.

## Candidate inspection operation, 2026-09-11

The current full verifier passed **380 tests, zero failures/errors and one Windows
symlink-privilege skip**, plus **39/39 reference checks**. The log is retained at
[`full-verifier-first.txt`](../evidence/candidate-inspection/full-verifier-first.txt).
Its initial `runs:1, errors:1` line comes from the deliberate recorder-integrity
rejection test; the full suite result has no errors. The previous implementation
and receipts are preserved in the [145-file archive](../evidence/candidate-inspection/legacy-docs/docs-01/manifest.json).

Independent reviews found and verified corrections for allocation ordering, high
measurement memory, transparent RGB preservation, reference-only candidate rejection
and scalar-type equivalence. The old failures remain alongside final probes.
Ruff passes across runtime/tests/scripts/evaluations. Default Mypy passes for the
20 runtime modules and explicit-package-base checks pass for the changed evaluation
and probe code; untyped function bodies retain Mypy's existing default limitation.
An overly broad initial Mypy invocation failed package discovery; its receipt is
retained separately from the corrected invocation.
The Windows CRLF-aware whitespace check also passes. The default Git check reports
carriage returns in generated JSON as trailing whitespace; that diagnostic is retained
without rewriting hash-bound receipts for cosmetic line-ending changes.

The [copied-package proof](../evidence/candidate-inspection/portable-operation/report.json)
passed 11 actual CLI/MCP operations with 10 prepared views, exact retained E/V,
mechanical pass / visual fail / engine unavailable, a separate unperformed candidate
and a relocated cold read of the old failure. Its judgments are explicitly supplied
developer fixture declarations. See [inspection evidence](../evidence/candidate-inspection/README.md)
for the separate native profile trials and their actual viewing evidence. Neither
fixture publication nor host completion establishes production art or engine acceptance.

All three new native attempts completed. Codex retained mechanical pass / visual fail /
engine unavailable after ten verified native/enlarged image deliveries. Claude's first
attempt preserved the visual rejection but incorrectly required viewing coverage for a
mechanical pass. The [original failure](../evidence/candidate-inspection/claude-native-review.json)
is retained. A two-sentence contract clarification, with unchanged runtime/profile/skill
hashes, led to a [successful fresh repeat](../evidence/candidate-inspection/claude-native-repeat-review.json)
with all three outcomes, exact image deliveries and saved-state readback. The
[12 isolated replay operations](../evidence/candidate-inspection/native-integrity.json)
have zero errors. Only the packaged contract and manifest changed after the full
runtime verifier; the new instruction identity received the targeted native repeat.

## Native profile evaluation, 2026-09-11

The [host evaluation](../evaluations/README.md) retains **sixteen native attempts**:
eight completed Codex model sessions, four completed Claude model sessions, three
Claude attempts interrupted at the shared 600-second limit, and the original Claude
authentication failure before inference. Both hosts have observed behavior on five
of eleven catalog cases, a visual repeat and a supplementary cold intake continuation.
Only maintainer routing and visual rejection have completed fresh turns in both hosts;
interrupted attempts still supply observable behavior and retained files.
The unchanged bundle manifest has 90 copied-file entries plus generated requirements;
its SHA-256 is `2c21250554a42804453ed3ea58810b08fd19b6b1fa08b5f0f3b886e14c3837d1`.

All four visual attempts identified the absent left antenna and right eye despite a
mechanical pass. Viewing completeness remains an independent requirement: the first
Codex exec stream omitted viewer observations, and Claude's repeat retained enlarged
inspection without native-scale viewing. Cold Codex intake recovered revision 2
unchanged; cold Claude intake continued an interrupted revision 1 and committed the
study's review at revision 2. Both preserved unresolved canvas and outline choices.

The [criterion review](../evidence/host-evaluation/criterion-review.json) retains
failures and unverified findings. Claude's style plan replaced requested selective
antialiasing with zero contour AA and an asserted approved palette; other attempts
introduced unsupported artistic requirements. Valid state and correct fixture
rejection did not establish correct project judgment. A Codex missing-provider rerun
with working file access completed local planning; the original denied-access attempt
remains unchanged. Claude assistant messages identify `claude-opus-5`, separately from
the init-selected `claude-opus-5[1m]`; Codex requested/selected `gpt-6-astra` without a
separate assistant model label. These are reported identities, not independent attestation.

[Evidence integrity and isolated state replay](../evidence/host-evaluation/integrity.json)
pass for all sixteen attempts and thirteen saved store heads: **39 local operations**.
All **18 focused recorder/report tests**, Ruff and Mypy pass. The checker discovers
stores in host-chosen directories, and the compiler separates interrupted inference,
completed turns, evidence corruption and model-authored state failures. A failed
cold-input test and independent recorder
probes are preserved; corrections prevent fixture reseeding on cold resume, retain
malformed-output attempts and archive mutated package bytes. An additional failing
regression is [retained](../evidence/host-evaluation/replay-inventory-before.txt): replay
now rejects unrecorded project files before they can influence validation. These checks validate
the recorder, not the model. The previous report, review and checks are
[preserved](../evidence/host-evaluation/previous-run/host-evaluation-01/codex-baseline/manifest.json).
Existing runtime, POC and family receipts below were not regenerated by this evaluation.

No live PixelLab generation, newly commissioned art, animation/tile continuity or
engine acceptance was exercised. The exact trial records, source versions and
limitations are retained separately from the [next task specifications](../evaluations/TODO.spec.md).

Run `python scripts/verify.py` from the checkout. It validates the declared supplied-source inventory and all curated line ranges, rebuilds the catalog/example/plugin, executes the full test suite and method POCs, measures representation size, and records runtime hashes. See [`evidence/test-results.json`](../evidence/test-results.json), [`test-log.txt`](../evidence/test-log.txt), [`art-methods/poc-report.json`](../evidence/art-methods/poc-report.json) and [`representation-benchmark.json`](../evidence/representation-benchmark.json) for actual results.

## Current family delivery operation, 2026-09-11

The integrated run executes **325 tests: 324 passed, zero failures/errors, and one existing Windows symlink-privilege skip**. All **39 reference POCs** and **93 source ranges** pass. The 53 new tests comprise 23 family semantic checks, 21 delivery checks and nine actual CLI/MCP operation checks. They exercise exact approved baselines, selected member/destination proof, pending jobs, historical packages after amendments, unavailable engine requirements, changed selection, immutable storage and generic publication ordering.

The [wheel probe](../evidence/wheel-check.json) passes **33 commands on an 83-file installation**. Copied-plugin verification passes 32 commands. Both include a twelve-command family operation beginning with a retained synthetic preaccepted checkpoint: snapshot real member bytes, leave collective checks unperformed, retain unavailable engine acceptance, amend membership and cold-read both old and new packages. The checkpoint's visual/live receipts are supplied test data, not actual artistic/engine evidence. All 90 bundle manifest entries match source and copied bytes. Exact current runtime identities and test counts are in [test-results.json](../evidence/test-results.json).

Ruff passes; default mypy reports no issues in 18 modules, with some untyped function bodies excluded. Three Codex skill checks, Codex plugin validation, three native Claude checks and 50 relative links in 16 instruction/spec files pass in [instruction-checks.json](../evidence/family-delivery/instruction-checks.json). These are discovery/format checks, distinct from agent behavior and real outcomes.

The [copied-plugin scenario](../evidence/family-delivery/plugin-scenario/record.json) records 49 isolated processes (43 CLI and six stdio MCP), with a separate import-origin check and all 90 source/plugin/copy identities verified. One fictional static-family workflow retained an unknown member attempt and rejected premature snapshotting, reconciled it through an explicitly supplied synthetic failure, preserved an earlier two-member package after saved membership amendment, and created a one-member package. The final delivery remains open: collective continuity is unperformed and engine acceptance unavailable. An N record and [concrete handoff](../evidence/family-delivery/plugin-scenario/handoff.md) identify the exact package and missing inspections. The earlier source-adapter walkthrough is retained separately. These scripted and inspected operations are not an independent profile-compliance benchmark, actual visual comparison or real provider/engine outcome.

Failed attempts remain separate in the [implementation ledger](superpowers/plans/2026-09-11-family-delivery.md) and [semantic review](../evidence/family-delivery/semantic-task-report.md). Seventeen delivery tests first failed on the absent operation, and the new family fields and public adapters were exposed by initial failures. Two later structural regressions reproduced family candidates omitting their constituents and family report plans carrying a raster contract. Independent review then found generic snapshot publication could activate its task and identified manifest redirection. Both new regressions failed before correction, including a real Windows junction. The reviewer confirmed all 23 scoped follow-up checks passed with no open finding. Unrooted graph validation cannot inspect frozen manifest bytes; the required rooted family report/store path does so.

The [previous milestone archive](../evidence/family-delivery/previous-run/family-delivery-01/manifest.json) preserves eleven exact provider-recovery files before regeneration. All five supplied source documents and PX1 specification/registry bytes remain unchanged. Registry 2.2.0 explicitly adds family fields; it does not silently upgrade old projects. The next development target is packaged-profile evaluation across hosts, with actual domain and destination outcomes still requiring their own observed evidence.

The [family development summary](../evidence/family-delivery/development-summary.json) binds the final runtime, review, instruction, distribution and scenario evidence by hash.

## Earlier provider recovery operation, 2026-09-11

The integrated run executes **272 tests: 271 passed, zero failures/errors, and one Windows symlink-privilege skip**. All **39 reference POCs** and **93 source ranges** pass. The 70 new tests cover discovered requests, closed history replay, project/store integration and actual CLI/MCP subprocesses. Local concurrent dispatch returns only one request; the other writer receives a stale/locked diagnostic. Saved plans, retained immutable bytes and acceptance remain checked on generic publication as well as high-level operations.

The [archived wheel probe](../evidence/family-delivery/previous-run/family-delivery-01/evidence/wheel-check.json) passes 21 command checks on a temporary 78-file installation. The copied-plugin test passes its original nine commands plus an eleven-command provider sequence. Both execute prepare, claim, cold unknown recovery, supplied success and local PNG import, then confirm all acceptance requirements remain unperformed. These tests use fictional discovery/authorization/provider observations; they do not call a live provider. The exact runtime identities are in the [archived test results](../evidence/family-delivery/previous-run/family-delivery-01/evidence/test-results.json). Standard Ruff and mypy checks pass; mypy's default does not check every untyped function body.

Three skill-format checks, Codex plugin validation, three native Claude checks and 40 relative links pass in [instruction-checks.json](../evidence/provider-recovery/instruction-checks.json). Profile behavior and actual production outcomes remain distinct verification levels.

The [independent recovery exercise](../evidence/provider-recovery/behavior-evaluation.json) follows the skill in one fictional scenario against a separately copied plugin. Restarted CLI/MCP sessions retained unknown state, reconciled a supplied remote identity without another dispatch, and imported one actual local PNG. A changed-contract branch rejected import with `job_stale` while retaining the store and downloaded file. Local dimensions/alpha measurement passed; visual and engine obligations remained unperformed, with concrete handoff records for both branches. This is one scripted and inspected developer-agent exercise with synthetic provider observations, not a controlled benchmark or actual provider/art/engine acceptance. Recorder mistakes are retained separately in its evidence.

Failed attempts remain separate. Initial missing-request/history/operation APIs were exposed before implementation. Further regressions reproduced an imported candidate missing from typed context, changed-contract import, generic commits referencing unretained working files, backward event dates, credential defaults hidden through schema applicators/references, timestamp precision truncation and an MCP schema diagnostic echoing a supplied credential value. Each was corrected and rechecked; the independent reviewer reported no remaining findings after scoped re-review. Adapter test helpers initially parsed argparse output as JSON; their correction is recorded separately from product failures. The [implementation ledger](superpowers/plans/2026-09-11-provider-recovery.md) retains the sequence and rulings.

The [previous milestone archive](../evidence/provider-recovery/previous-run/manifest.json) preserves eleven exact files before regeneration, including the earlier PX2 specification/registry and evidence. Existing PX1 specification and registry bytes and all five supplied domain documents remain unchanged. The new registry 2.1.0 fields explicitly opt into durable J semantics; no existing job is automatically upgraded.

The [provider recovery development summary](../evidence/family-delivery/previous-run/family-delivery-01/evidence/provider-recovery/development-summary.json) binds that milestone's implementation, review, instruction and scenario evidence by hash. Its next target was family-scale planning, continuity and delivery, implemented locally in the current milestone above.

## Earlier intake/sample lifecycle, 2026-09-11

The integrated run executes **202 tests: 201 passed, zero failures/errors, and one Windows symlink-privilege skip**. All **39 reference POCs** still pass. PX1 canonical-byte tests and the original regression suite remain in the run. PX2 checks cover empty intake, conflicting/proposed/confirmed choices, planned outputs without files, research before adoption, criterion-specific evidence, rejected and unavailable verdicts, immutable history, scoped reopening and saved-plan ordering.

The [archived wheel probe](../evidence/provider-recovery/previous-run/evidence/wheel-check.json) exercises ten operations from a temporary installation, including fresh PX2 intake, cold workflow inspection and the incomplete bundled example. The wheel contains 73 files. The copied-plugin tests exercise the same new operations separately. That milestone's runtime identities and exact counts are in [its archived test results](../evidence/provider-recovery/previous-run/evidence/test-results.json); the preceding source milestone remains preserved under [intake-sample/previous](../evidence/intake-sample/previous-run/manifest.json).

The new tests first exposed absent lifecycle/format operations. Two persistence regressions then demonstrated that freshly invented or amended criteria could be published with their passing verdicts; saved-plan checks at initialization and commit now reject that. Another regression demonstrated that globally rejecting unresolved choices in C prevented retaining an old candidate during a new conflict. Such state is now retained while dependent activation is blocked. A CLI test initially tried to parse stdout from `encode --out`; the test now checks the written file, matching the actual CLI contract.

No automatic PX1 migration, provider submission, visual-art acceptance or live engine result is supplied by the new state model. Fixture verdicts exercise local rules only. Profile behavior is evaluated separately from these tests.

Independent review found a new V could claim to be already superseded and skip current proof checks. The regression reproduced an unsupported historical pass, then verified its rejection. Store initialization and commit now reject every newly introduced superseded V; existing published verdicts still supersede one way. The earlier planning-order test had also used newly superseded fixture verdicts; it was simplified to isolate changed criteria under this stronger rule. The reviewer confirmed pass/fail/unavailable rejection in both publication routes and preserved state on failure.

The [recorded intake/sample exercise](../evidence/intake-sample/behavior-evaluation.json) covers two fictional scenarios performed by one independent developer-agent against a copied plugin: incomplete intake and rejected-sample revision. It retains 78 operations, 28 project files, cold CLI/MCP comparisons, completion rejections and the revision handoff. Both scenarios passed within that scope. The first copy's manifest mismatch and three recorder mistakes remain separate from the coherent evaluated snapshot and final outcomes. Supplied visual/engine verdicts are synthetic; these scripted and inspected scenarios are not a controlled benchmark or actual artistic acceptance. The broader 11 profile scenarios remain unexecuted. The [development summary](../evidence/intake-sample/development-summary.json) binds the final local evidence and lists remaining work.

## Earlier source operation milestone, 2026-09-11

That milestone's archived run executed **141 tests: 140 passed, zero failures/errors, and one Windows symlink-privilege skip**. All **39 bounded reference checks** passed for **43 methods**. All **93 source locators** resolved, and all **five supplied documents** matched their inventory identities. The two current research documents are distinct revisions; the earlier duplicate-file observation no longer applies.

Run `python evidence/source-migration/verify_ranges.py` to reproduce the migration audit against the archived prior sources. It checks 25 byte-identical relocations, 68 formatting-only citation migrations, complete historical research-line correspondence, and preservation of all non-source fields across 43 methods. The [migration manifest](../knowledge/source-migration.json) identifies each old/current slice and the exact permitted normalization; the [review report](../evidence/source-migration/range-review.json) binds those results. The archive and audit helper are checkout resources; the installed package ships the current sources, inventory, migration manifest and review report.

The [archived wheel check](../evidence/intake-sample/previous-run/evidence/wheel-check.json) built and temporarily installed a 66-file wheel, then exercised source discovery, knowledge, capabilities, initialization, project validation, installed-library validation, and all reference POCs from a separate project. Runtime dependencies were reused from the selected environment; nothing was installed globally. The full suite separately exercises a copied plugin and its own resource-package proofs.

Failed evidence remains separate. The [initial scaffold review](../evidence/reviews/2026-09-11-scaffold/summary.json) recorded 45 errors among 123 tests before migration. The [prior-source archive](../evidence/source-migration/previous-run/manifest.json) preserves the old sources, generated knowledge and receipts. Development regressions reproduced and corrected publication after invalid package metadata, stale sources retained in wheel build output, and divergence between validated source snapshots and packaged bytes (including aliased paths). Known preflight failures now leave existing bundle files untouched. This does not claim transaction rollback after a crash during publication.

A [separate developer-agent exercise](../evidence/source-migration/knowledge-operation-evaluation.json) followed the knowledge skill against a copied bundle from an empty project. It recorded 20 command executions, inspected both `silhouette-readability` and `dither-coverage`, retrieved all five method citations, verified nine source slices, and recovered from a deliberately stale hash through fresh inventory discovery. It retained a candidate and a specific proposed readability comparison, with missing references and assets explicit. It also identified the citations' limited support for broader curated procedures. One instruction ambiguity about stale expectations versus broken installations was clarified and reviewed separately; the report preserves the original evaluated snapshot. This single exercise is behavioral evidence for the bounded research operation, not a controlled model benchmark or production-art outcome. The broader scenarios in `evaluations/profile-scenarios.json` remain unexecuted.

The local engine is tested through real filesystem operations, image files, compiler round trips, competing writers, and stdio MCP subprocesses. PixelLab responses in unit tests are explicitly supplied fixtures. Those tests do not impersonate a live service.

## Evidence design

| WHO | WHAT | WHERE | WHY / research | Observable proof |
|---|---|---|---|---|
| Language evaluator | Preserve type distinctions and reject ambiguous encodings | `tests/test_language.py` | Proprietary notation must remain deterministic; density alone says nothing about inference. | UTF-8 byte framing, duplicate rejection, limits, canonical hashes. |
| State evaluator | Detect stale facts and rejected work | `tests/test_graph.py`, `tests/test_store.py` | Persistent agent context is useful only when its relationships remain current; [context-engineering research](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) motivates retrieval and note persistence. | Exact evidence/decision/method bindings, supersession, completion gates, stale/concurrent writers and reopening. |
| Art evaluator | Measure the actual file and reference algorithms | `tests/test_assets.py`, `tests/test_poc.py` | Research procedures in the knowledge registry require concrete tests with known results. | Real PNG/GIF/TIFF measurements, mutation injection, 512 oriented tile-neighbor pairs and independent numeric oracles. |
| Adapter evaluator | Keep provider arguments and observation history accurate | `tests/test_platform.py`, `tests/test_mcp.py` | Official PixelLab/MCP interfaces distinguish creation, observation and completion. | Exact supplied-schema validation, mode constraints, immutable remote identity, unknown outcomes and surviving malformed requests. |
| Distribution evaluator | Make the kit work outside this repository | `tests/test_packaging.py`, `docs/AGENT-KIT.md` | Installed plugins run from caches and other projects. | Relocated runner, copied-resource hashes, host discovery and real MCP handshake. |

## Failed attempts retained separately

These are pre-fix observations, not final verification results:

1. Initial parser/graph/store/catalog/assets test invocations failed because their modules were not implemented. The initial platform suite had 22 explicit missing-adapter failures; the POC suite had 15 explicit missing-runner failures. Implementation followed those baselines.
2. A new graph regression showed an asset receipt could omit its visual contract. Binding coverage was added and the regression passed.
3. Independent review reproduced a method borrowing an unrelated passing asset proof. Method and decision receipts now bind their own definitions and semantic sources; unrelated and stale proofs fail.
4. Independent review replaced a red image during inspection. The old code returned red measurements with the replacement blue file's hash. Inspection now hashes and measures one in-memory byte snapshot; the regression checks both the original receipt and a failing reinspection of the replacement.
5. A multi-frame TIFF bypassed limits using a tiny first frame and an oversized second frame. Every actual frame and cumulative pixel total are now checked before conversion. The first fix wrapped its own `image_limit` error; that exception handling was corrected and retested.
6. An escaped lone surrogate in an MCP tool name terminated the server before a subsequent ping. Escaped JSON response encoding preserves the structured error and the following request.
7. Evidence validation rebuilt adjacency for every asset binding. Independent review measured 1,000 X/E pairs at 2.316 seconds. Computing adjacency once reduced the same fixture to 0.0563 seconds in that review environment. These are local probe timings, not a cross-machine performance guarantee.
8. A completed task could remain completed after its contract and proof changed. Commits now require reopening on any change in the task's reference closure. Existing E receipt content cannot be rewritten; supersede it and add a new ID.
9. Exact source-slice testing initially expected LF while its Windows fixture wrote CRLF. The fixture now explicitly writes LF; the reader continues to preserve actual source newlines.
10. A strict POC run exposed deprecated Pillow `getdata` usage. It was replaced with a supported operation and verified with deprecation warnings treated as errors.
11. The root interpreter's `-I` mode hid user-site Pillow during bundle testing. The automated relocation harness now supplies only dependency site directories while excluding source/cwd paths. The independent agent exercise used a separate venv with dependencies and no PIXL installation, providing a second portability check.
12. The first wheel probe disabled build isolation on an interpreter without setuptools, so pip could not import the build backend. The probe now uses the project's declared isolated build dependencies. `python scripts/check_wheel.py` then built and installed the wheel in a temporary target and exercised knowledge, capabilities, initialization and validation without source imports. Results are in [`wheel-check.json`](../evidence/wheel-check.json).
13. Git's automatic newline conversion was observed normalizing several supplied CRLF sources in an intervening checkpoint. Their working bytes remained unchanged. `.gitattributes` now disables text conversion so subsequent commits/checkouts preserve exact source, snapshot and receipt bytes. Git can show those raw-byte restorations as changes even though the supplied working files were not edited.
14. Independent review changed cited research and corrupted generated PNGs after a POC run. The compiler formerly rebound current source hashes and ignored the artifact manifest. Compilation now requires the exact source and artifact bytes recorded by the run. Compiled receipts bind fixture X records and their contracts, so later context validation also rejects artifact drift.
15. Independent review altered a runner file after importing it. The loaded implementation formerly reported the hash of the changed, unexecuted file. A follow-up used an equal-size edit with an unchanged timestamp to make Python load stale bytecode. The runner now checks loaded module code against compilation of the captured source, binds its source identity at import, and rejects changes before or during execution. This guards accidental source/cache drift; it is not an attestation against hostile process manipulation.
16. The session crossed midnight. Generated receipts now record their actual UTC observation time, and compiled E records retain that time instead of a fixed development date. The repeated-run test initially compared timestamps as if they were deterministic fixture values; it now verifies UTC timestamps separately and still requires identical measurements, artifact hashes and other payload. That pre-fix failure is retained in [`timestamp-transition-failure.txt`](../evidence/timestamp-transition-failure.txt).
17. Workspace linting found that the packaged proof source imported a sibling module that had not been copied. The new resource-package regression first failed on its missing package initializer. Plugin and wheel builders now retain the complete source package, and the relocated package executes its own POCs. The portable launcher's minimum-version guard remains covered by a test; its local UP036 exception documents why an installer assumption does not apply to a copied launcher. Subprocess checks retain explicit return-code handling, and wheel verification uses the project's `uv` workflow.

The independent code reviewer re-ran all five original findings after their fixes and found them resolved. It also exercised method changes, source changes, receipt supersession, rejected receipt reactivation and preserved historical bindings. Subsequent exact runtime hashes are in the final test report; the narrative timings above describe the reviewed snapshot.

## What the results establish

The reference runner covers all 43 knowledge methods with 39 bounded checks. Reference proofs include deliberately damaged variants and independent expected values. Project-specific, provider, visual and engine acceptance still require their own evidence: connected masks do not establish appealing silhouettes; corner compatibility does not establish attractive joins; material conservation does not establish a production physics implementation. The [fixture visual review](../evidence/visual-fixture-review.json) records only the landmarks actually inspected in the key contact sheet.

`prepare` uses a caller-supplied input schema and never discovers or contacts a server. `job` records caller-supplied observations and never submits or polls. Receipts validate identity, freshness and local relationships; they are not remote attestations. PixelLab authentication, actual generation, account pricing, output quality and target-engine integration require real subsequent evidence.

The representation comparison uses the same records, values and explicit reference/symbol distinctions. It reports tuple, compact and pretty JSON baselines, two tokenizer encodings when available, the separate specification/registry bootstrap cost, and closed retrieval of one method from the complete PIXL knowledge library. It does not measure model accuracy, artistic output, end-to-end latency or long-horizon recovery success rates. A controlled multi-model experiment would need fixed task instances, identical evidence, multiple trials and outcome scoring; none was silently substituted with byte counts.

On this Windows machine the symlink-publication test is skipped when symlink creation privilege is unavailable. The report lists that skip explicitly. The ordinary path-confinement and writer tests still execute. All store guarantees assume local cooperative writers and a functioning filesystem; no distributed consensus, hostile filesystem protection or power-loss guarantee beyond the stated publication mechanism is claimed.

The final wheel probe also validates the installed PIXL knowledge library and executes its POCs from a separate project. The plugin relocation test does the same with copied runtime/resources and verifies the runner and source hashes. For Git whitespace review, CRLF must be recognized as a line ending: `git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff --check`. Supplied sources and historical archives preserve exact bytes, including any pre-existing whitespace. Plain `git diff --check` misidentifies CRLF endings in generated evidence as trailing whitespace because this repository disables checkout normalization.
