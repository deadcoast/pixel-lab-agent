# Native caller/specialist cold review, 2026-11-15

**Status: partial progress; PX-SKILL-001 / PX-EVAL-005 remains open.** The revised
Claude workflow produced an independent caller finding, a correction by the same
registered PIXL child, and subsequent caller verification. It still accepted
unsupported answer effects and inherited acceptance rules. This is not a passing
cold-authority qualification. [Exact result](RESULT.json).

## What was exercised

Both trials start from the exact 41-file [cold-04 revision-6 archive](../qualification-20261114/cold-04/project.zip),
including its faulty continuation. The seed and semantic rubric stay the same.
Neither native input includes a maintainer defect list, semantic grade, corrected
continuation or invented owner answer. Each is a fresh caller session and an actual
registered `pixl:pixl` child in an external consumer. The old interrupted native
parent is not resumed.

| Trial | Observed outcome | Retained evidence |
| --- | --- | --- |
| `native-01`, original kit `00adedec…` | Caller falsely accepts the returned authority claims without correction. Child omits the cold procedure. Three erroneous commit attempts recover using the store folder; final revision 7 is real, but not a semantic pass. | [Semantic review](semantic-review-01.md), [corrected mechanical review](mechanical-02.json), [scope notes](mechanical-review-notes-01.json), [input/output preservation](native-01/preservation.json) |
| `native-02`, revised kit `903e6c29…` | Caller independently identifies a contract-intent field mismatch and sends a source-cited finding to the same child. The child checks it, corrects the proposal and publishes revision 8. Caller verifies that revision, but still accepts unsupported authority claims. | [Semantic review](semantic-review-02.md), [mechanical review](mechanical-04.json), [caller comparison](native-02/project/review/caller-comparison-2026-11-15-v2.md), [input/output preservation](native-02/preservation.json) |

Observed host/model: Claude Code **2.1.318**, **claude-fable-5-1**. There are two
completed native workflows, not two behavioral passes. The first retains 49 output
files and the second 54; no seed file was removed and neither copied kit changed.
Raw streams, full native journals, original inputs, all output bytes and ZIPs are
retained in each attempt. A waiting response/result record is distinguished from
the actual final after child completion.

## Actual correction and remaining failure

In `native-02`, caller `0cb10d0f-c176-4369-bc7b-cc4864e78d6d` continued child
`a7f9957f93675cbf8` through native `SendMessage`. Its own source review found that a
new lighting observation keyed `li` would constrain the whole contract's lighting
and aesthetic-intent field to a lighting-only string. The same child verified the
cited code, changed the observation key to `lighting`, and saved an amended note
with an explicit old-to-new account. Final state is revision **8**, canonical hash
`ac9150f4e8ee656761811370867538130faaa111759d61065153df358ef14225`.
The earlier note and revision remain retained. No owner-choice status or acceptance
was changed by that correction.

That real correction does not resolve the original authority problem. The adopted
amendment carries forward outline-to-palette confirmation claims. The original note
acknowledges palette exclusivity as a derived rule, yet still treats confirmation as
adopting it. Its sample-criterion repair is conditional on a delegated-trial path;
the explicit outline/canvas-answer path leaves criteria requiring unasked confirmed
palette/alpha policy. The caller's comparison accepts the inherited rule as support
for the advice. Current finals, notes, criteria and next-operation claims are graded
together; valid state and preserved hashes do not override these defects.

The [second semantic review](semantic-review-02.json) records actor-specific final
question behavior, every C/O/CR judgment and the successful correction separately.
Post-revision caller checks include validation, readiness, hashes, a state diff and
the amended note. There is no claimed post-revision full `workflow` endpoint call.

## Changed implementation and prospective controls

- [Reusable isolated runner](../../../evaluations/cold_caller_review.py): exact seed
  and package verification, neutral assignment extraction, native registered-role
  tools, immutable source/launch guards, no default timeout, and complete failure
  retention. [Seven focused tests](../../../tests/test_cold_caller_review.py) cover
  preparation, exclusion, provenance guards and interrupted-output retention.
- [General caller procedure](../../../plugins/pixl/skills/pixl/references/delegation.md#caller-review-a-cold-continuation):
  compare literal inherited criteria and every claimed answer effect with sources,
  current status, authorized change and actual prerequisites; preserve scoped expert
  proposals; use the same child for real findings; recheck the final version.
  [Rationale and before/after identity](guidance-change-01.json).
- [Frozen revision](revision-01/RESULT.json): only the delegation reference and
  bundle manifest change. Profile, Python runtime, PX1/PX2 semantics and fixture
  inputs stay unchanged.

The [original protocol](protocol.json) and [reporting appendix](protocol-amendment-01.json)
were frozen before the first inference. The [second protocol](protocol-revision-02.json)
and [reporting appendix](protocol-amendment-02.json) preserve the rubric, task core
and seed while clarifying the head-file/store-folder locator and result self-hash
reporting. [Actual preparation checks](preparation-02.json) bind the exact prompt.
No findings from the first trial are supplied to the second caller. Guidance,
setup wording and reporting instructions change together; differing behavior is not
an isolated causal or general reliability result.

## Verification and preserved failures

- [Local checks](local-02/RESULT.json): **40 tests pass**—seven new runner tests,
  ten existing handoff tests and 23 recorder tests—plus scoped Ruff. The initial
  [two-finding lint failure](local-01/RESULT.json) remains retained.
- [Packaging](package-check-01/RESULT.json): **four packaging tests pass** on the
  revised kit; all package bytes remain unchanged through those checks. These
  include local copied-package and synthetic probes, not remote generation.
- [Revised-trial mechanics](mechanical-04.json): **42/42** for native identities,
  delivered instructions, final state, caller consumption and preservation. This
  does not pass the separate failed semantic review.
- [Seed preflight](seed-preflight/RESULT.json): **11/11**, exact revision 6 and
  unchanged source bytes/mtimes. [Initial preparation](preparation-01.json) and
  [revised preparation](preparation-02.json) bind the actual native inputs.
- Initial mechanical checker failures remain in [mechanical-01](mechanical-01.json)
  and [mechanical-03](mechanical-03.json). Numbered Read payloads and XML-escaped
  native completion text required additive parser corrections. Missing procedure
  retrieval in native-01 remains a real failure. An absent literal endpoint call
  is distinguished from observed current readiness/state checks.
- [Documentation audit](documentation-01.json), [read-only evidence integrity](integrity-01/RESULT.json)
  and [scoped final file check](final-worktree-check-01.json) retain their exact
  counts and limits. No full verifier is newly run or claimed.

The [earlier qualification](../qualification-20261114/README.md), all unaided
direct-profile failures and the separately maintainer-guided correction are
unchanged. No provider generation, new art acceptance, engine outcome or human
acceptance is established here. M1/M2 and broader M3/M4/M5 remain open.

## A–E review

- **A — Improvement:** byte checks and one genuine correction do not substitute for
  an answer-to-authority audit. The unresolved next operation should be tested against
  explicit, clearly labeled controlled evaluation answers, with unchanged unasked choices and
  applicable sample criteria checked independently.
- **B — Hosts:** this increment observes Claude's actual registered child and one
  same-child correction. It does not add a Codex run, resume the original parent,
  or establish general native reliability.
- **C — Context and quality:** the caller resolves one source-defined contract
  mismatch but misses inherited authority errors. Reference measurements and a
  valid store are distinct from source-faithful art decisions and artistic quality.
- **D — Another repository:** both consumers are outside repository ancestry, with
  explicit kit/runtime paths and exact retained inputs. Invocation isolation is not
  an operating-system sandbox or proof of universal discovery.
- **E — Responsibilities:** the profile owns expert judgment, the shared skill owns
  the review procedure, and local runtime tools preserve identities/state and check
  declared contracts. They do not decide whether an unasked policy was authorized.
  Official provider execution and human acceptance remain separate.

## Next work

Continue **PX-SKILL-001 / PX-EVAL-005 [M1, linked CF-02]** from the retained
revision-8 handoff: qualify the claimed answer-to-state operation with explicitly
labeled controlled answers, while preserving unasked authority and checking the
actual sample criteria. These answers stay scoped to the copied evaluation consumer and do not establish real owner preferences or human acceptance. Keep direct-question fidelity and all failed predecessors
open; do not substitute the successful intent-field correction for this exit.

The [store-locator finding](store-locator-finding-01.json) is a narrow supporting
**TM-04 / TM-03** follow-up: explain directory versus head-file arguments in the
immediate MCP/CLI surface and reject a file-valued write-store argument with precise
invalid-input recovery. It is identified, not implemented. The existing IDENTIFY
cycle and all 50 finding IDs continue; human acceptance is not a development gate.

To repeat the recorded revised-kit workflow, use a **new** attempt directory with
the runner's `prepare` command, the `seed-preflight/seed` and manifest, and
`protocol-revision-02.json` plus `protocol-amendment-02.json`; then use `run` on that
prepared directory. Preparation probes the host/runtime only. `run` invokes the
native model and retains outputs even on interruption. Replaying this prompt does
not acquire authority to provide owner answers or to execute a generation provider.
