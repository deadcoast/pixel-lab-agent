# QOL-09 — verification tiers and side effects

This increment makes the [verification guide](../../docs/VERIFICATION.md) usable
before running a check. Its current command choices precede the unchanged dated
ledger: inspect existing evidence, exercise a focused core operation, evaluate
native behavior, review actual assets, or rebuild implementation evidence.
This continues `IDENTIFY-2026-11-09-01` from `90e1ff3`.

## What changed

The guide gives exact checkout commands, their prerequisites, outputs, evidence
tier and failure interpretation. The everyday read-only route remains
`scripts/check_integrity.py`; the focused example exercises consumer-index
semantics and CLI/MCP parity. README and the integrity guide link to these choices.

Source review established several consequential boundaries:

- Full unittest discovery can rebuild live bundle and knowledge outputs.
  The focused consumer-index module instead writes temporary fixtures and uses
  `-B` in its Python subprocesses. Parent `-B` is not a general no-write switch.
- Several direct builders and the full verifier do not parse arguments.
  Appending `--help` still runs their mutating operation.
- The full verifier archives known outputs, rebuilds and checks local work,
  then replaces current summaries. The archive is not a complete checkout backup
  or rollback; generated notice/build/cache locations have distinct coverage.
- A standalone wheel-check failure can leave an earlier successful receipt
  untouched. Retain the actual process status and logs in a fresh location.
- Native preparation, model execution, retained-result grading and official
  provider work have different effects. Outer runner success does not establish
  a passing native task. Integrity never replays a retained result.

The [source review](20261114/source-review-01.json) records exact sources and
preserved draft findings. No runtime, schema, production profile/skill, generated
bundle or integrity registry changed.

## Fresh qualification

Local command execution and the unfamiliar-reader exercise are recorded
separately. Their input manifests bind the tested guide and implementation.
New reports use fresh paths; historical evidence is not regenerated.

The [actual local command proof](20261114/local-01/RESULT.json) passes 19/19
qualification checks across four invocations:

| Invocation | Observed result | Evidence meaning |
| --- | --- | --- |
| [Human integrity output](20261114/local-01/integrity-human/execution.json) | Actual exit 1, `needs_review` | Expected qualification/release gaps remain visible; no tests are replayed. |
| [JSON integrity output](20261114/local-01/integrity-json/execution.json) | Actual exit 1; 17 claims and 57 receipts: two current, eleven historical, four stale | Exact identities and present applicability of the registered evidence. |
| [Selected NF-07 consumer claim](20261114/local-01/integrity-selected/execution.json) | Selected claim current; overall exit 1 | Claim filtering still checks retained releases; it does not hide their gaps. |
| [Focused consumer-index tests](20261114/local-01/focused-consumer-index/execution.json) | 16 existing tests pass, zero skips, exit 0 | Fresh local fixture/CLI/MCP coverage, not newly added tests or a full-suite/native/art outcome. |

Each invocation retains exact stdout, stderr, command and process status. The
[before/after preservation result](20261114/local-01/preservation.json) confirms
all **85,651 tracked files** preserve bytes and mtimes; **285,690 workspace path
entries** have no additions/removals. The path inventory includes ignored
bytecode outside `.git`, `.venv`, `node_modules` and this task's output tree.
It does not hash existing untracked bytes, environment contents, global caches
or external temporary fixtures, and does not prove an absence of transient
writes. The focused tests intentionally create and clean temporary state/art/exports.

The separate fresh-reader qualification is in progress. Its scope is command
selection, actual read-only execution and interpretation from the frozen guide.

## Evidence limits and preservation

This increment does not run the full verifier, rebuild the kit, invoke the
official provider or review new art. The earlier NF-07 full verifier remains
[retained implementation evidence](../verification-runs/20261114T152255.619054Z/result.json):
1,393 passing tests, three Windows privilege skips, 39 reference checks and
distribution probes. Its [broad Ruff failure](../deliverable-index/20261114/maintenance-01/RESULT.json)
still contains nine findings in five unchanged files. A focused test does not
resolve those findings or extend native/artistic qualification.

The current evidence index and all registered claim lines remain unchanged.
Post-qualification living-document handoffs will be checked separately from the
frozen guide used by the command and reader trials.

## A–E review

- **A — Improve the core operation:** choose the smallest check that answers the
  actual question. Consumer-index regression checks and existing-evidence
  inspection are directly usable without accidentally refreshing prior proofs.
- **B — Host compatibility:** the documented native lifecycle separates host
  execution, recorded status and independent review. A guide-reading evaluation
  is not new PIXL production qualification or broader host reliability.
- **C — Context and artistic quality:** local mechanics, observed rendering,
  visual review and human acceptance remain distinct. No command count confers
  an artistic verdict.
- **D — Another repository:** consumer installation/readiness stay separate from
  maintainer verification. These commands run in a selected checkout/environment;
  a consumer does not need to rebuild repository evidence to use delivered art.
- **E — Responsibilities:** maintainers select and retain appropriate proofs;
  scripts perform their declared local operations; native agents demonstrate
  behavior; specialist/caller reviews assess useful outcomes. Official provider
  execution occurs only in the corresponding production workflow.

Human acceptance stays separate; M1/M2 and broader M3/M4/M5 remain open.
The next eligible slice is **SC-09 — lock diagnostics and recovery guidance**.
