# Library-source retention and recovery — PX-OPS-002

The current runtime reproduces the historical failure: an untouched project resumes with its original kit and fails after replacement because S source `s.fixture_receipt` still names the old proof report. The [before record](20261107/before.json) retains both outcomes.

The implemented operation keeps exact referenced library-source bytes in the consumer project. Normal validation and resumption can use those explicitly retained revisions after the kit changes; reports identify the old source actually used. State, record hashes, original receipt files/bindings and verdicts remain unchanged. The installed kit is not overwritten with old resources.

## Implemented interface and acceptance

- [Runtime](../../pixl/retention.py): immutable source objects and locator/digest entries, manifest-bound provenance, preflight, stale-write rejection and exact-byte recovery.
- [Agent workflow](../../plugins/pixl/skills/pixl/references/library-retention.md): call `retain-library` / `pixl_retain_library` after saving imported library S records; recover an already affected project with `from_library`.
- [Contract](../../spec/library-retention.md): explicit optional source resolution shared by PX1/PX2; no new record fields or rewritten evidence.
- Ordinary validation, workflow, jobs, family, inspection and project-scope source retrieval identify retained revisions. Current-library retrieval, live consumer sources, artifacts and receipt-file checks keep their original behavior.

The [eight-operation historical replay](20261107/reproduction-after.json) passed prevention, updated-kit validation/workflow/jobs/family, exact original source retrieval, and recovery after replacement using the original kit. Both original project-state files were byte-identical after the operations.

The [portable recovery record](20261107/portable-recovery.json) passes validation/workflow/jobs/family with the replaceable kit omitted and all seven required library S revisions available in project-owned retention. Its state SHA-256 remains `6cde256061704af7ca387b5a6abf55ec02c1ef088d7ee34f31b50bc684c219b2`.

The [retained project archive](20261107/retained-project.zip) contains all 50 files, including hidden state and snapshots. Every entry was checked against the [file manifest](20261107/retained-project-manifest.json); [archive identity](20261107/retained-project-archive.json) is retained separately. Extract it into an isolated directory, then run the current installed CLI against `retained-project/.pixl/state.px` with `--root retained-project`. The expanded working copy is ignored; the archive preserves the complete fixture for another checkout.

**PX-OPS-002 is complete for this source-retention/recovery contract.** Original bytes must exist in a retained snapshot or supplied original kit. Unavailable or corrupted original bytes remain an actionable failure; the operation never manufactures evidence. Old proof remains evidence about its original source revision, not the updated runtime or a new candidate.

## Verification

[Final full verification](../../evidence/verification-runs/20261108T002640.587065Z/result.json): **438 executed, 437 passed, one Windows symlink-privilege skip; 39/39 reference checks passed**. This increment adds **17 tests**, not 437 new tasks.

The source-distribution → wheel → temporary installation and copied-plugin relocation both execute `retain-library` and cold source/workflow retrieval through their isolated CLI. A local MCP protocol test invokes the new structured tool and resumes in a separate CLI process. These exercise the callable implementation; this increment is not a fresh Claude/Codex model trial.

Tests also verify unchanged receipt/state identities, exact line-range checking, idempotency, multiple source records sharing a file, complete preflight before publishing, stale callers, path confinement, damaged snapshots/manifests, project relocation, changed requested revisions, live consumer drift and separate current-library access. Ruff, Mypy and the shared skill validator passed. [Development checks](20261107/development-checks.json) retain corrected command/lint issues and the formatting-only verification rerun.

## Required A–E review

**A — Improvement:** one callable retention operation replaces manual reconstruction of changed library dependencies. It is conditional on importing library sources, so a simple direct asset request does not acquire a new mandatory setup process.

**B — Host compatibility:** the operation uses the existing CLI and structured local MCP protocol and is included in the same portable package. It requires no new host configuration or credentials. Installed/copied execution is verified; native specialist use within the updated complete asset workflow remains PX-EVAL-005.

**C — Contextual and artistic quality:** the original method/proof context survives an installation update, and the caller can see exactly which revision supports it. This does not correct the separate recorded artistic-authority failures or prove generated-art quality. Those acceptance items remain open.

**D — Another project's workflow:** source locators and retained objects are project-relative; reports return the actual resolved paths. Relocation, replacement, original-kit recovery and a project without the replaceable kit all work under the current runtime.

**E — Responsibility location:** the profile retains visual expertise; the knowledge skill routes to this recovery workflow; the CLI/MCP operation retains and retrieves exact bytes; versioned specifications preserve proof/acceptance meaning. Remote PixelLab generation remains in its official connection.

The [overall TODO](../../TODO.md) continues with artistic-authority correction, consumer allocation maintenance, native current-interface delivery, actual production, broader expertise/recovery coverage and installation dependency separation.
