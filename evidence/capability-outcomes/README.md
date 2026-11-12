# NF-04 capability/outcome matrix

**Bounded complete, 2026-11-12.** The [task-first matrix](../../docs/CAPABILITY-OUTCOMES.md) makes the existing core features easier to select: setup, source allocation, requirement comparison, candidate/family review, changed-source integration, isolated consumer execution, lineage and caller continuation. It connects those routes to actual outcomes and separately covers production, advertised domains, hosts and renderers.

NF-04 was promoted from the active M4 queue in cycle `IDENTIFY-2026-11-09-01`. This increment changes development/consumer documentation and its evidence only. No runtime, packaged skill, saved-state semantics, provider job or historical receipt is changed. The matrix is a maintained qualification reference, not a new prerequisite in the production workflow or another runtime API.

## Scope and usefulness

- Each core task names the public route, result the caller can use, retained evidence, limiting condition and useful next action. The existing guide remains the operational entrypoint.
- Advertised asset classes and operation families are mapped to documented, locally checked, natively exercised or outcome-reviewed scope. Unsupported domains receive concrete next assignments. Catalog size never becomes an expertise claim.
- Exact historical package identities remain distinct from current source and later compatibility checks. CF-10's original and upgraded Claude kits remain separate. CF-03's recorder failure, QOL-10's incomplete Claude caller result and guided recoveries remain visible.
- README, host setup and evaluation entrypoints now lead to the matrix. Claude setup guidance now reflects the retained authenticated follow-ups, while preserving original login failures; the stale CF-06-next pointer is corrected.
- Human acceptance is **not recorded**, separate from development qualification. Native-agent or development-assistant review is not relabeled as human approval. That separate assessment does not halt authorized development or prevent closing this bounded documentation task.

## Verification

The [coverage inventory](20261112/coverage.json) records the reviewed public sources, explicit claim-to-row mapping, frozen receipt hashes and tested-identity bindings. The [fresh audit](20261112/audit-02.json) checks local paths/anchors, source/evidence identity, inventory coverage, the 50 existing finding/backlog IDs and preservation of prior evidence and runtime/package files. Its [retained script](20261112/audit.py.txt) reads these files and writes only a fresh requested report; it does not regenerate evidence or a bundle.

The [first audit](20261112/audit-01.json) retained one checker false failure: it treated a shell-example placeholder link inside a fenced code block as a real documentation target. The [original script](20261112/audit-source-01.py.txt) is preserved; the corrected checker excludes fenced examples and the fresh second audit verifies actual links.

Independent [claim/usability review](20261112/independent-review.json), [core factual review](20261112/core-review.json) and [domain factual review](20261112/domain-review.json) inspect actual receipt scopes. The core review identified ambiguous setup wording; the final matrix explicitly restricts named-child execution to clean setups and describes omitted-route cases separately. The review also checks all 28 cited native launch versions. Domain review checks all 25 named local reference IDs and retained production/recovery facts. This is fresh documentation qualification, not fresh artistic, native, provider or engine acceptance.

The preceding [full verifier](../verification-runs/20261112T093934.289828Z/result.json) remains **1,060 passes plus one skip**, with reference and distribution checks at its recorded source hashes. It was **not rerun** for this documentation-only increment; no new full-suite count is claimed. All prior evidence, runtime, shared profile/skills and bundle bytes remain unchanged. Later source or outcome changes require a new review and fresh audit receipt rather than rewriting this snapshot.

To check the retained scope without rebuilding anything, run from the repository root with a fresh output path:

```powershell
.venv/Scripts/python.exe evidence/capability-outcomes/20261112/audit.py.txt --out build/nf04-reference-recheck.json
```

The audit reports drift when a reviewed source changes; drift means review the matrix and append a new qualification snapshot, not that an old native outcome has become a failure. This bounded checker does not implement the broader TM-10 release-integrity proposal or independently infer the meaning of every sentence. The reviewed coverage inventory and manual outcome judgments remain explicit inputs.

## Required A–E review

| Question | Current answer and next consequence |
| --- | --- |
| **A — How to improve?** | Lead with core user tasks and usable returns, then expose exact scope and next action. Fix contradictory entry guidance. CF-08 next addresses the user's ability to finish interrupted work through existing operations. |
| **B — Claude/Codex compatibility?** | Both hosts have useful bounded routes; explicit Codex registration differs from automatic discovery, and Claude plugin loading differs from session selection. Record exact versions, partial runs and recoveries instead of implying interchangeable reliability. |
| **C — Contextual/artistic quality?** | Source authority, actual lineage, inspection and destination evidence constrain each result. Queue/robot success does not establish font, terrain, character, rig or general motion expertise. Human acceptance remains separately unrecorded. |
| **D — Work from another repository?** | The setup and everyday routes operate in the consumer project with its source map, brief and existing authorization. The matrix lets the caller choose a supported route and understand additional qualification needs without authoring low-level state or waiting for generic approval. |
| **E — Responsibility split?** | The profile supplies judgment through the host model; skills supply operational guidance; local CLI/MCP preserves state and observations; official PixelLab performs provider actions. This matrix reports what those combined routes have actually accomplished. It supplies no new execution or approval authority. |

## Next work

**CF-08 — unknown submission, known-job continuation and interrupted retrieval** is the next eligible TODO increment; use TM-03 support where the operation needs interruption/concurrency checks. Preserve provider identity, unresolved uncertainty, failed attempts and the no-duplicate-submission requirement. Existing controlled observations are starting evidence, not complete remaining qualification.

**M1/M2 and broader M3/M4 remain open**, including TM-08/domain quality, host reliability and the unrelated Claude QOL-10 caller-result continuation. Continue [PLAN](../../PLAN.md) through [SHELVED](../../SHELVED.md) and [TODO](../../TODO.md); no new full IDENTIFY cycle is started.
