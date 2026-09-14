# Source-grounded knowledge operation implementation plan

> **For agentic workers:** Use superpowers:subagent-driven-development for the independent source migration and its review; execute tightly coupled runtime integration locally. Track completion here.

**Goal:** PIXL can discover the actual supplied sources, retrieve current method citations, and reproduce its knowledge in the checkout and a relocated distribution.

**Architecture:** One `training/source-inventory.json` identifies the supplied source revisions. A runtime reader validates this inventory and file identities; cataloging, verification, and packaging consume it. Curated citations migrate by reviewed line correspondence; historical receipts remain archived and new receipts come from re-execution.

**Tech Stack:** Existing Python 3.11+ package, unittest, Pillow, jsonschema, CLI and stdio MCP.

**Spec:** `docs/PROJECT-REVIEW.md`, R2, R6 and the source-reproduction milestone. This is the first prerequisite to the intake/sample lifecycle, not its complete implementation.

## Global constraints

- Preserve every current file in `training/original-docs/` byte-for-byte.
- Preserve PIXL/1 grammar, saved-state semantics, and evidence-binding rules.
- Do not replace missing source paths with obsolete bundled source bytes.
- Do not edit a historical receipt to imply that a new source revision was tested.
- Keep mutable project state outside installed plugin resources.
- Keep the developer role distinct from the PIXL production profile.

## Task 1: Explicit source identity and discovery

**Files:** create `training/source-inventory.json`, `pixl/sources.py`, `tests/test_sources.py`; modify `pixl/catalog.py`, `tests/test_catalog.py`.

**Interfaces:** `sources.load_inventory(root)` returns the validated inventory with documents `{id,path,sha256,lines,previous}`; verifies current bytes/line counts and rejects missing, changed, duplicate or escaping paths. `catalog.build(root)` uses this inventory when present. A source tree without its inventory fails clearly; arbitrary project Markdown cataloging still works when no supplied corpus exists.

- [x] Add and run failing tests for corpus discovery, missing inventory, missing/changed source, duplicate paths, path escape, and current source identity.
- [x] Implement the inventory reader and route catalog discovery through it.
- [x] Run the focused source/catalog tests; preserve red and green results.

Representative behavioral assertion:

```python
result = catalog.build(root)
self.assertEqual([row['path'] for row in result['documents']], ['training/original-docs/source.md'])
```

## Task 2: Reviewed citation migration

**Files:** `knowledge/pixel-art.json`, `knowledge/source-migration.json`, `docs/research/pixel-art-knowledge.md`; archive previous evidence under `evidence/source-migration/previous/`.

**Interfaces:** Existing `{path,start,end}` citation fields keep their meaning. Each migration row records old/new file identities and line ranges, and the reviewed correspondence. Do not change the method's prerequisites, procedures, checks, pitfalls, or applicability to make migration pass.

- [x] Compare old/current research documents and inspect every cited range affected by formatting changes.
- [x] Map citations into `training/original-docs/`, record old/new ranges and scope of changes, and correct current research tables/duplicate claims.
- [x] Verify migrated ranges retain the cited content and original methods retain all non-citation fields.

Acceptance is concrete: all 93 locators resolve to reviewed current text, with no invented source identity and no stale line-number assumption.

## Task 3: Reproduction, distribution and operational use

**Files:** `scripts/verify.py`, `scripts/build_plugin.py`, `setup.py`, `MANIFEST.in`, `scripts/check_wheel.py`, packaging tests, CLI/MCP/service source discovery routes, and the knowledge-operation skill reference.

**Interfaces:** CLI `sources` and MCP `pixl_sources` expose verified bundled/source inventory. An explicit CLI root selects a corpus. Packaging ships the same inventory and current source layout. Verification validates the inventory before executing proofs. The common skill provides a bounded source-to-method operation with failure and stopping conditions.

- [x] Test that failed source preflight cannot publish a partial bundle; test relocated source discovery and complete required resources.
- [x] Replace duplicated legacy file lists in verification and packaging with the inventory; safely prune only previously generated obsolete files whose bytes still match the old manifest.
- [x] Archive historical POC/library/test evidence before rebuilding; run current POCs, compile knowledge, build examples and bundle, and execute the suite.
- [x] Run wheel and relocated bundle checks, focused lint/type checks, and static skill validation.
- [x] Review the integrated diff and correct concrete findings; update current docs with fresh outcomes and limits.

## Execution ledger

Ruling: continue in the existing workspace on a dedicated local branch, preserving the preceding review edits. The user authorized development of this checkout; moving or resetting their current tree would obscure that work.

Preflight: Task 1 defines inventory fields consumed by Task 3. Task 2 changes only citation sources and current research documentation; Task 3 regenerates their derived evidence after completion. No task changes supplied source bytes or the UDL schema.

Completed on branch `develop/pixl-source-provenance`. Eighteen new source/distribution tests cover the operation; the focused source/catalog run passes 20 tests. Initial source tests exposed missing inventory behavior, and publication tests exposed a bundle write before source failure. Implementation followed those failing cases.

Independent review then reproduced three distribution faults: stale sources survived reused wheel output, malformed package metadata failed after bundle writes, and inventory/source reads could identify different byte snapshots. Each finding received a failing regression before its fix. A second snapshot probe used a valid `./` path alias; binding captured bytes to resolved bundle targets fixed that variant without banning valid aliases. Re-review confirmed all three findings resolved.

The source reviewer checked all 93 locators, including the one range that needed its new closing math fence included. The read-only audit passes with 25 byte-identical relocations and 68 formatting migrations, and a matching non-source digest across all 43 methods. All 15 archived files retain their recorded bytes.

Final integrated review found no remaining concrete issues in this operation. It independently exercised a copied bundle from an empty project: five-source discovery, method selection, exact citation retrieval, and an 8,218-byte closed context, with no project writes. All 70 bundle-manifest entries matched their source bytes.

Current automated validation is recorded in [test-results.json](../../../evidence/test-results.json), [wheel-check.json](../../../evidence/wheel-check.json), and [instruction-checks.json](../../../evidence/source-migration/instruction-checks.json): 140 passed tests, one Windows privilege skip, 39 reference POCs, seven wheel operations, three Codex skills plus plugin validation, and three native Claude component checks. Ruff and mypy pass. Whitespace verification uses Git's `cr-at-eol` setting to respect this repository's exact-byte CRLF artifacts.

Remaining product development is the intake and representative-sample lifecycle described in the review. This milestone changes neither PIXL/1 semantics nor the unimplemented draft-state, provider-submission persistence, visual-acceptance, and engine-acceptance operations.

The additional [knowledge-operation exercise](../../../evidence/source-migration/knowledge-operation-evaluation.json) retained real copied CLI/MCP traffic for a single developer-agent scenario: 20 commands, all five citations of two selected methods, nine independently verified slices, and a preserved stale-hash rejection followed by recovery. The result is an unadopted method candidate and a concrete next proof, with absent project evidence explicit. Its observed instruction ambiguity was corrected by separating discovery failure from a stale caller expectation. A separate wording review records that correction without relabeling the original run as a new scenario execution.
