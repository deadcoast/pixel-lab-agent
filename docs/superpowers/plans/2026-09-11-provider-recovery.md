# Provider recovery implementation plan

> Use superpowers:subagent-driven-development for independent request/history helpers and bounded reviews; integrate the store operation locally. Continue the user's existing development authorization.

**Goal:** Persist provider intent before execution, recover uncertain submission and import candidates without inventing acceptance.

**Architecture:** An opt-in PX2 J extension binds immutable JSON journal snapshots to the existing compare-and-swap store. Pure request/history validation supports project-aware mutations and CLI/MCP/skill operations.

**Tech stack:** Existing Python, unittest, .px, JSON, local files and stdio MCP; no new dependency or external execution.

**Spec:** `docs/superpowers/specs/2026-09-11-provider-recovery-design.md`.

## Constraints

- Preserve supplied source bytes, PX1 rules, legacy PX2 J and previous milestone evidence.
- Keep the current development branch and its authorized uncommitted work; no reset/global install/push.
- Caller-supplied observations remain explicitly unverified; no paid call, automatic retry or acceptance.
- Use expected hashes for all mutations; state publication is the authority after failed writes.

## Task 1: Observed request preparation

Files: `pixl/platform.py`, `tests/test_discovered_requests.py`.
Interfaces: `prepare_discovered(provider, tool, arguments, schema, discovery, authorization) -> dict`, `validate_discovered(request) -> dict`, exact shape in design.

- [x] First test newly discovered tools and cache-conflicting arguments accepted under the exact supplied schema; schema-invalid/secret/unbounded inputs fail, provenance and authorization are retained, and mutations/hash drift fail replay.
- [x] Implement the explicit request route without changing legacy prepare; focused tests and Ruff pass.
- [x] Independently review the request boundary and correct concrete findings.

## Task 2: Immutable history reducer

Files: `pixl/job_history.py`, `tests/test_job_history.py`.
Interfaces: `new(job_id, request, context)`, `append(journal, event, evidence, remote_id=None, artifact=None)`, `validate(journal)` as specified.

- [x] First test dispatch before observed success, crash state unknown, repeated observations, immutable identity, terminal failure, import associations and full replay tampering rejection.
- [x] Implement finite closed JSON replay with complete retained intent and no I/O; focused tests and Ruff pass.
- [x] Independently review reducer requirements and correct concrete findings.

## Task 3: Project-aware durable operation

Files: `pixl/jobs.py`, `pixl/store.py`, `pixl/graph.py`, `pixl/registry-v2.json`, `spec/PIXL-2.md`, `tests/test_jobs.py`.
Interfaces: public prepare/dispatch/observe/import_artifact/report in the design; `jobs.validate(doc, root=None)` after generic validation; `jobs.transitions(current, candidate, root, folder)` after candidate validation during initialize/commit.

- [x] Archive current test/wheel/POC/library/instruction/spec/registry/bundle evidence and record hashes before regeneration.
- [x] First test full persisted uncertain-response recovery and direct-commit bypasses against actual files. Pin old compatibility.
- [x] Implement context hashing, immutable blobs and projections, saved-plan/append-only checks and publication ordering.
- [x] Verify concurrent/stale dispatch cannot yield executable arguments; failure retains prior state.

## Task 4: Operations, skills and portable verification

Files: CLI/service/MCP, common skill references and profile, packaging checks, verification/docs/evidence.

- [x] First test CLI/MCP mutations and cold report, then expose exact operations with correct mutability annotations.
- [x] Write the provider recovery skill with exact required context, commands, submission handoff and failure/resume procedure.
- [x] Rebuild the bundle; execute integrated suite, wheel, lint/type and instruction checks.
- [x] Independently review the integration and execute a bounded fictional recovery scenario from a copied plugin; preserve failed attempts and exact evaluated identities.
- [x] Record final outcomes and next development target; no claim of real provider/art/engine acceptance.

## Ledger

Ruling: the existing R5/stage-3 target is actionable, so the user's conditional request to create a new MIVIM .spec TODO is not triggered. No MIVIM format exists in this checkout; another project's doctrine is not imported.

Ruling: retain the current branch and prior uncommitted work, which is the user's continuing development context. A new checkout would omit it.

Ruling: extend PX2 through explicit optional J.jr/J.op/J.xs fields and registry 2.1.0, preserving all existing documents. Attaching the extension to a published legacy J is prohibited because it would invent durable history.

Ruling: save a dispatch claim as unknown before giving the host the request. This may require manual reconciliation even if the process dies before actually sending; that cost is preferable to treating an uncertain paid operation as safely repeatable.

Ruling after two integration regressions: durable J also requires `xs` with typed references to every imported candidate. JSON string IDs alone left the candidate out of a job context packet. Import now checks the complete output semantic scope, because an unchanged F can refer to a C whose actual contract changed. Both defects were reproduced before correction.

Initial store integration run: 15 errors because the new jobs module was absent. After implementation all 15 passed. Two added regressions then failed on incomplete context closure and changed-contract import, as recorded above. Request tests first had 14 missing-API failures; history tests had 22 missing-module assertion failures. These failed attempts remain distinct from later verification.

Independent core review found direct-commit storage bypass, backward event timestamps and credential defaults hidden through schema applicators/references. Four regression tests first produced seven failures; store-folder content addressing, monotonic aware timestamps and contextual local-reference inspection resolved them. Scoped re-review found a fractional precision gap; its failing regression is fixed by documented rejection beyond six fractional digits. Further adapter review found MCP schema errors echoed malformed credential values; a real stdio regression reproduced the leak, and keyword-only errors now pass. The reviewer confirmed all scoped fixes and reported no remaining finding. Generic publication protects storage as well as public helpers.

Adapter development: six initial tests exposed missing CLI/MCP operations; the first test helper tried decoding argparse text as JSON (three recorder errors), then its correction yielded only expected missing-operation assertions. Six operation tests passed after implementation, with one additional credential-error transport regression added during review.

Integrated verification: 272 tests run, 271 passed, no failures/errors, one Windows symlink-privilege skip. All 39 reference POCs and 93 citation ranges pass. A true competing-dispatch test grants exactly one request and returns stale/locked for the other writer. The portable wheel passes 21 commands on 78 installed files; copied-plugin verification executes 20 commands including the new eleven-step provider probe. All 84 plugin manifest entries match current source bytes. Ruff passes; default mypy reports no issues in 16 modules while explicitly excluding some untyped function bodies. Three Codex skill checks, Codex plugin validation, three native Claude checks and 40 relative links pass. Eleven prior-milestone evidence/contract files remain byte-identical in the archive. All five supplied source documents and PX1 specification/registry bytes remain unchanged.

Independent skill exercise: one fictional scenario against a separately copied plugin retained one dispatch across cold CLI/MCP sessions, reconciled a supplied remote identity and imported one actual local PNG. A changed-contract branch returned `job_stale` with the entire store inventory and source PNG unchanged. Later explicit nomination and dimensions/alpha verification left visual and engine requirements unperformed and the sample open; both branches retain concrete handoff records. The final audit checked 84 source/plugin/copy identities, 37 subprocess results, five MCP processes and 138 retained snapshot entries. Zero unexpected runtime errors occurred. Two recorder mistakes (an incorrect reference path and a rejected helper patch) remain separately recorded. This developer-agent scripted and inspected exercise uses synthetic provider observations; it is not a controlled benchmark, real provider operation or artistic/engine acceptance. See `evidence/provider-recovery/behavior-evaluation.json` and `evidence/provider-recovery/development-summary.json` for retained bytes, evaluated identities and claim limits.

Ruling: use the existing stage-4 target next: family-scale planning, continuity and delivery operations grounded in the approved sample and actual destination requirements. Real provider/art/engine outcome trials remain a separate evidence obligation; synthetic recovery fixtures do not discharge it.
