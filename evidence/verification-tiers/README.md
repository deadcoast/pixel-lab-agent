# QOL-09 — verification tiers and side effects

**Bounded QOL-09 is complete.** This increment makes the [verification guide](../../docs/VERIFICATION.md) usable
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

The [fresh Codex CLI 0.167.2 reader](20261114/reader-01/project/NAVIGATION-RESULT.json)
completes four questions on inspection, focused tests, rebuilding and evidence
tiers. It discovers the guide from README and actually executes the documented
human-output integrity command, retaining the actual child exit **1**, exact
stdout and stderr. [Mechanical checks pass 42/42](20261114/reader-01/mechanical-01.json);
the [independent semantic/trace review passes all four answers and the route](20261114/semantic-review-01.json).
The reader's [separate preservation check](20261114/reader-01/preservation.json)
keeps all **85,651 tracked files** unchanged in bytes and mtimes. Its four frozen
guide inputs still match the source review and local command proof.

The reader first encounters `WinError 2` when launching a relative interpreter
from its external scratch process. It corrects the executable to the absolute
checkout interpreter and completes the read-only operation without post-launch
guidance. The initial failure remains in its [public trace](20261114/reader-01/stdout.jsonl)
and independent review. The successful wrapper exit is distinct from the actual
integrity command's exit 1. This is a maintenance-reader outcome, not PIXL
production qualification or a claim of error-free first-attempt execution.

A [supplemental recording note](20261114/reader-01/supplemental-source.json)
incorrectly inferred that the reader saw later local-test results in the working
ledger. The [trace-based correction](20261114/reader-01/supplemental-source-correction-01.json)
preserves that mistake and the actual rendered page: the reader saw the earlier
in-progress ledger and the already completed source review, not the later local
proof. No answer cites or depends on the later ledger version. The four guide
inputs stayed frozen; this linked working page was outside their protected set.
Its later snapshot is labeled as such, not substituted for the page actually read.

## Evidence limits and preservation

This increment does not run the full verifier, rebuild the kit, invoke the
official provider or review new art. The earlier NF-07 full verifier remains
[retained implementation evidence](../verification-runs/20261114T152255.619054Z/result.json):
1,393 passing tests, three Windows privilege skips, 39 reference checks and
distribution probes. Its [broad Ruff failure](../deliverable-index/20261114/maintenance-01/RESULT.json)
still contains nine findings in five unchanged files. A focused test does not
resolve those findings or extend native/artistic qualification.

The current evidence index and all registered claim lines remain unchanged.
The [final document audit](20261114/documentation-01.json) checks the unchanged
historical verification ledger, links, stable finding IDs, open milestones,
registered claim lines, retained snapshots and unchanged prior evidence/runtime
inputs. The [final read-only inspection](20261114/integrity-01/report.json)
retains the expected applicability/release gaps. These checks cover the final
living-document handoff separately from the frozen guide used by the trials.

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
