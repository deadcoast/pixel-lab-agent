# Everyday production, hash domains and locators

M1 findings **QOL-03, QOL-04 and QOL-01**, active cycle `IDENTIFY-2026-11-09-01`.
This increment joins the public operations into a consumer-facing guide and
clarifies the identities/locations used to call them. It changes no PX field,
saved digest algorithm, prior receipt or artistic acceptance rule.

## Implementation

The [everyday guide](../../plugins/pixl/skills/pixl/references/everyday.md) is the
common skill's primary operational entry: assigned context → selected asset →
prepare/resume official PixelLab request → inspect/review → family/integration →
retained caller return. It keeps the host model's visual judgment central and
links detailed procedures only where needed. The running example uses the actual
queue successor and its `authoring-plar.txt`; the older queue remains distinct.

The [identity/path reference](../../plugins/pixl/skills/pixl/references/identities-and-paths.md)
distinguishes canonical state, file bytes, semantic requirements, candidate
bindings, comparison scope and current comparison reports. Public CLI and MCP
results share additive `hash_domains` labels without recalculating existing
identities. Exact exports label their own byte hashes separately. Stale-write and
handoff errors name the appropriate guard. Path rejection names the declared root
and required path form; confinement and error codes stay unchanged.

Examples distinguish installation, consumer and store locations; ordinary CLI
filesystem inputs, root-relative packet/export inputs and rooted MCP calls;
exact source file SHA-256, record identity and line/pointer locators. Existing
whole-file bindings are not rewritten to make their old evidence look narrower.

## Verification

Five new regression cases cover noncanonical wire-file bytes versus canonical
state, PLAR reformatting versus semantic requirements, wrong-domain handoff
rejection and unchanged retry, retained comparison identity/export bytes, relocation
with spaces and exact source text, and CLI/MCP stale-write errors. The focused
run passes 23 tests. Its first attempt hit Windows sandbox temporary-directory
permissions before useful execution; subsequent runs use a repository-local temp
root. The first retained focused log also catches a test fixture's Windows newline
assumption; writing explicit source bytes preserves the exact-text assertion.
Logs: [first](20261109/verification/focused-01.txt),
[passing](20261109/verification/focused-02.txt).

The [first full verifier](../verification-runs/20261109T191606.703842Z/result.json)
passes 595 tests plus one Windows symlink-privilege skip, 39 reference checks and
fresh wheel/copied-plugin probes. A final message-only refinement avoids repeating
the error-code prefix and adds an assertion. The [final full run](../verification-runs/20261109T191851.620905Z/result.json)
again passes **595 tests plus one skip**, 39 reference checks and distribution.
[Package checks](20261109/verification/package-checks.json) verify all 172 bundle
entries, zero tested-input drift, and native frozen packages identical to the final
bundle. Ruff and configured Mypy pass separately; Mypy's untyped-body coverage
remains limited. No result count here establishes model instruction following.

The [native scenario](../../evaluations/everyday_guide_case.py) reuses the completed
Claude and Codex consumers. It asks a cold caller to delegate guide-based
resumption, retrieve exact source/context, replay an unchanged accepted review,
save the selected successor's handoff and independently check the return. New
fixture-local optional role instructions replace stale assignment links; previous
trials and user host configuration remain untouched. Actual invocation is graded
from native traces rather than inferred from that file's presence.

## Native caller outcomes

Both trials finish the assigned consumption/recovery operation without maintainer
redirection. They use the final frozen package above and retain their own caller
verification. This assignment explicitly permits the generic Codex child route;
it does not qualify named-role discovery or arbitrary unassisted production.

| Host | Actual route | Result and independent evidence |
| --- | --- | --- |
| Claude Code 2.1.318 | Foreground `Agent`, `subagent_type:"pixl"`, registered by this harness's `--agents` file; child `a374e0c1528878c24` | Caller and child read the shipped guide/path reference. Child uses public CLI; caller independently uses local MCP and CLI. Its corrected verifier passes 26 checks. [Caller result](20261109/native/claude-01/project/work/everyday-guide/CALLER-RESULT.json), [independent checks](20261109/native/claude-01/independent-checks.json) |
| Codex CLI 0.167.0 | Generic native `/root/pixl_specialist`, not a selected named custom role | Caller reads the common skill/guide/path reference; child inherits that context and separately reads the profile and delegation procedure. Caller passes 16 checks. [Caller result](20261109/native/codex-01/project/work/everyday-guide/CALLER-RESULT.json), [independent checks](20261109/native/codex-01/independent-checks.json) |

Each independently passes 12 additional maintainer checks: unchanged valid
canonical state, every baseline consumer file and frozen kit file preserved, exact
authoring/review exports, creation-time snapshot versus current acceptance,
zero-publication identical replay, fresh selected-successor handoff, export-byte
identity and exact source text. These overlap with caller assertions; they are
separate checks of the same operation, not 24 different production successes.
The [checker](20261109/check_native.py) records its own identity and limits.

Both return `authoring-plar.txt` / `queue.working` with the unchanged selected
requirements hash `1ab9df77ca2b8e1c5c6c97fe69e428c4a0db7fedb3dd497847cc96732ea149a6`.
Their revision-126 states differ because they retain their own prior native
reviews. Each uses its own canonical state for handoff, the returned file hash
for byte checking, and the selected requirements hash for asset identity. Source
retrieval is exact: Claude reads `src/queue-view-successor.ts:18–21`, including
CRLF; Codex reads `SUCCESSOR-ADOPTION.md:44–52`. Existing broad bindings are retained.
No new verdict, asset acceptance or renderer observation is produced by replay.

**Retained corrections and limitations:**

- Claude's first caller verifier passes 21/25 assertions. Four failures assume
  incorrect manifest/handoff field layouts and normalize source newlines. The
  caller corrects its script against actual returned shapes and exact CRLF bytes;
  26/26 then pass. The [first result](20261109/native/claude-01/caller-verification-first.json)
  and [first script](20261109/native/claude-01/caller-verifier-first.py.txt) were
  copied outside the consumer before that autonomous correction; the native
  stream also retains the failures. No specialist output or production record
  needed repair. Caller and child each recover a shell heredoc quoting error.
- Claude's large direct PLAR read exceeds host display capacity; the host retains
  its full tool output, which the caller reads for verification. The compact
  caller-result finding QOL-10 remains useful follow-on work. The child also
  consults the packaged handoff implementation read-only for reserved detail keys;
  ordinary operation uses public interfaces and no low-level record construction.
- Codex corrects a read-only Python quoting error, replaces an oversized inventory
  printout with complete directory digests, and follows the returned handoff path
  after a guessed filename does not exist. The native journal retains those
  steps. No maintainer follow-up was supplied to this trial; the prior guided
  comparison remains separately graded in [its report](../choice-comparison/README.md).
- Claude's caller identifies stale descriptive queue progress beside a delivered
  derived continuation and leaves the assigned queue unchanged. This is explicit
  remaining queue-maintenance context, not grounds to regenerate accepted art.
  Neither this trial nor Codex's generic route closes same-child continuation,
  named Codex selection, the earlier interrupted Claude comparison or broader
  host reliability.

The [result ledger](20261109/RESULT.json) links host traces, exact result identities
and verification. The [final cohesion check](20261109/verification/cohesion-final.json)
checks the document chain, all finding dispositions, tested inputs and packages.

## Required A–E review

**A — Improvement.** Callers can start with one operation path and retrieve detail
at the needed phase. Labels/errors now distinguish the hashes and roots that caused
actual prior friction. Ordinary work uses public JSON operations instead of
internal record authoring.

**B — Host compatibility.** CLI and MCP preserve input shapes and existing result
fields while adding display metadata. The common skill ships the same workflow
to both hosts. The native harness's registered Claude agent and generic Codex
child consume that workflow; their actual roles and self-corrections are above.
These outcomes remain separate from discovery, typing and distribution checks;
named Codex role and continuation qualification stay within their explicit M2 scope.

**C — Contextual/artistic quality.** The guide preserves caller authority, scoped
expert choices, actual reference roles and existing accepted work. It requires
the applicable visual/temporal/destination observations without promoting fixture
geometry or mechanical measurements into aesthetic laws. This increment tests
usable operation, not new generated-art quality.

**D — Another repository.** The path reference and relocation tests use a consumer
root independent of the install and shell directory, including spaces. Both cold
native callers return the selected successor using exact source text and the
appropriate identity domains. Current queue selection determines its production
generation. General cross-project reliability still needs broader cases.

**E — Responsibilities.** Profile/model: specialist judgment. Skill: operation
sequence and authority. Local runtime/MCP: deterministic state/recovery/evidence.
Host: actual tools, delegation, observation and official provider calls. PixelLab:
production generation/editing through its official service. The official
[platform docs](https://www.pixellab.ai/docs) and [MCP overview](https://api.pixellab.ai/mcp/docs)
were consulted on 2026-11-09; they remain linked at the guide's provider step,
alongside the instruction to inspect the live declaration for the selected tool.

## Continuation

Record actual outcomes in [TODO](../../TODO.md) and dispositions in
[SHELVED](../../SHELVED.md); continue the active [PLAN](../../PLAN.md). M1 and broader
host reliability remain open. Next take M2 TM-06/CF-04: retain resumable native
attempt/session/child metadata and qualify Claude same-child continuation against
the earlier interrupted scenario, grading artifact-based restart separately.
Follow with CF-05 named Codex selection. Preserve the accepted consumer and all
earlier failures; no new IDENTIFY audit or conditional refactor is needed.
