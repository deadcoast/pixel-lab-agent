# CF-08 recovery with TM-03 publication checks

**Bounded core recovery complete, 2026-11-12. Native instruction conformance remains partial.** This increment implements and demonstrates useful continuation of an uncertain submission, an identified job and interrupted artifact retrieval. It uses the existing public job/report/import workflow and an existing consumer. Controlled transport faults remain labeled; no paid production or new artistic acceptance is needed for this recovery qualification.

The selected work is **[M4 | CF-08, TM-03 | PX-EVAL-003]**, continuing cycle `IDENTIFY-2026-11-09-01`. M1/M2 and broader M3/M4 remain open. Human acceptance is a separate assessment, not a gate on this authorized development.

## Reviewed gaps and implemented operation

The prior [capability matrix](../../docs/CAPABILITY-OUTCOMES.md#remaining-scenario-coverage) and [controlled request-review outcomes](../request-review/review.md) establish useful earlier reconciliation. They do not close the remaining interrupted-retrieval and repeated cold-recovery conditions.

Source review found three concrete usability gaps:

1. A succeeded job reports `inspect_candidates` even when required outputs have not been imported; its candidate list lacks direct retained-file locators.
2. Retrying an import after publication succeeds but its reply is lost rejects the existing candidate ID and suggests a new ID, instead of recognizing identical completed work.
3. The optional HTTP import bridge writes a retained download directly; interruption can leave partial bytes at the expected digest filename and make every retry fail.

The implemented correction stays within existing commands and versioned state semantics: actionable read-only recovery information, exact same-import reconciliation, and atomic/recoverable local downloads with failed bytes preserved. No report grants another dispatch, provider success never grants artistic acceptance, and uncertain submission remains uncertain until originating-connection evidence supports a state change.

## Qualification scope

| Layer | Required observation |
| --- | --- |
| Local operation | Missing-output guidance, useful imported-file locators, unchanged exact import replay, mismatch/stale-write refusal, partial-download recovery without a new provider call |
| TM-03 | Real history-to-head and post-head lost-response boundaries; competing writers publish one valid journal/review/nomination; old history survives and no duplicate dispatch/import/verdict appears |
| Native controlled recovery | Named Codex and Claude specialists use the public operation in isolated existing consumers. One unresolved no-ID attempt remains unknown; another is reconciled, observed and retrieved through a controlled service that genuinely truncates its first HTTP response |
| First cold recovery | New caller/child, same consumer and frozen kit, saved remote identity reused with a fresh retrieval locator; complete candidate bytes imported and independently consumed by the caller |
| Second cold recovery | Another new caller/child recovers the same candidate, current state and useful next action without another dispatch/import; all earlier failures and identities remain retained |
| Package/implementation | Focused tests, source/profile discovery and appropriate full/distribution checks against exact tested versions; historical native kits remain distinct from later compatibility checks |

Native rounds are **artifact-based cold restarts**, not claims of same-parent/same-child cross-process continuation. A controlled provider's counters and on-wire download observations establish duplicate prevention and partial-byte behavior within this scenario. They do not establish live PixelLab failure behavior, remote exactly-once semantics or broad host reliability.

## Required A–E review

| Question | Current development answer |
| --- | --- |
| A — How to improve? | Let the caller recover through the ordinary report/import route: show missing outputs and retained paths, recognize already-published imports, and avoid a permanently poisoned download cache. |
| B — Claude/Codex compatibility? | Exercise the explicit named Codex role and Claude plugin child in separate cold processes; preserve their actual route, source package and observed results. |
| C — Contextual/artistic quality? | Preserve the original request, output context, source bytes and unperformed acceptance. Recovery correctness does not assess newly generated art or human satisfaction. |
| D — Another repository? | Reuse the isolated existing consumer with its selected runtime and complete kit; put mutable work in that consumer and return exact usable file/state locators. |
| E — Responsibilities? | The host performs actual provider lookup/download and supplies observations; the local runtime preserves identity, publication and import; skills explain the useful route. The controlled service is evaluation infrastructure. |

## Actual native results

All rounds use the exact [206-file frozen kit](20261112/native-kit-snapshot.json), manifest `60f2a7dd8cd3e4bb080bdb286eead4a9754cdff64d464d0461f837bc00e0ce6d`, archived [here](20261112/native-kit-60f2a7dd.zip). Codex **0.167.2** uses its explicit `pixl` role; Claude **2.1.318** uses the registered `pixl:pixl` plugin child. Their launch/identity records bind the actual host, selected isolated Python, copied provider fixture, prompts and external consumer. The actual Claude transcript identifies `claude-fable-5-1`; no model is inferred from earlier trials.

| Host / phase | Independent result | Observed outcome |
| --- | --- | --- |
| [Codex 1](20261112/codex-01/grade-final-01.json) | 30/30 | Matching originating lookup resolves one unknown; real processing/completed observations; 59-byte short response retained, with no import |
| [Codex 2](20261112/codex-02/grade-final-01.json) | 33/33 | Fresh parent/child obtains a fresh URL for the same remote ID, retrieves all 177 bytes, imports one candidate and independently consumes it |
| [Codex 3](20261112/codex-03/grade-final-01.json) | 31/31 | Another fresh parent/child consumes the same candidate; state and full provider-call log are unchanged |
| [Claude 1](20261112/claude-01/grade-final-01.json) | 30/30 | Matching originating listing supplies the actual processing observation; subsequent known-ID response completes; 59-byte short response retained |
| [Claude 2](20261112/claude-02/grade-final-01.json) | **32/33 overall — fail** | All recovery/import/caller outcomes pass; required common-profile loading is not observed. This is a retained native conformance finding, not a checker error |
| [Claude 3](20261112/claude-03/grade-final-01.json) | **30/31 retained grader**, plus [12/12 async-completion checks](20261112/claude-03/async-completion-proof.json) | All recovery, unchanged-state/log and common-profile checks pass. The existing grader recognizes synchronous completion only; actual asynchronous completion is independently bound to the same child/call/run/session |

Each host has **one original controlled accepted submission**, seeded before native execution. The native work performs no new preparation, dispatch or generation. A second saved attempt with no recoverable remote ID remains exactly `unknown`, with its original journal unchanged. The successful recovered image is SHA-256 `d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7`; the original short response is `c782e097dc9ebb50682becc305d82839e4ee73c38926dd9dd6495b75ed037c4f`. Both callers inspect the actual retained PNG and existing `src/avatar.ts` mapping; `assets/robot.png` is an exact byte copy. This verifies file consumption, not execution or acceptance of a target engine.

The provider returns the existing controlled reference pixels. It is a transport/recovery qualification, not a new artistic result. Tasks, artistic reviews and human acceptance remain unperformed. The independent grader uses retained native calls, role completion, actual returned reports, publication journals, changed-file archives and provider counters; a caller's success label alone cannot pass it.

## Implementation and TM-03 evidence

- The jobs report identifies missing outputs, the retained candidate paths and hashes, originating provider/tool/remote ID, and a usable next action. A succeeded job with missing output now directs retrieval. Reports grant no dispatch or acceptance authority.
- Repeating the exact completed import with the **current** expected state hash returns `reused_import: true` without another revision, artifact or journal event. Changed evidence, bytes, association or stale expectations refuse reconciliation. This is local published-work recognition, not a claim of remote exactly-once execution.
- The optional HTTP bridge validates complete bytes, atomically publishes its download, preserves an existing damaged cache entry, and uses a distinct content-bound recovery location. A changed recovery file is refused rather than overwritten. These are local controlled tests; the native scenarios use the ordinary host download and public import route.
- [TM-03 results](20261112/tm03-verification.json) retain the original failure and the real Windows path-spelling race: resolving a concurrently created file could yield an extended-length path while the root used the ordinary spelling. Normalizing only equivalent resolved drive/UNC spellings fixes the false escape; containment checks remain. Eight new publication tests cover actual history-to-head failure, post-head lost replies, competing imports/observations/reviews and single nomination. Six new confinement tests cover the path correction and escape refusal. Focused checks pass **39 plus one existing privilege skip**; the diagnostic concurrent-import loop passes 20/20 after the fix (repetitions, not 20 independent feature tests).

These cases qualify selected publication windows and ordinary CAS recovery. General process termination/lock cleanup, arbitrary filesystem faults and broad host reliability remain outside the claim.

## Preserved failures and proof corrections

The original checker grades remain: Codex 1 **21/30**, then **29/30**; Claude 1 **28/30**; Codex 2 **32/33**; Codex 3 **29/31**. They exposed checker limitations: the reported child-ID shape, a subprocess's genuine curl error despite the wrapper exiting zero, a processing observation correctly sourced from the matching listing, and literal public-CLI wrappers that directly save/print stdout. The corrected checker binds actual native role/calls, exact returned bytes, chronology and fully inspected wrapper source. Exact-source allowlists are specific proof adapters for these retained traces, not a general claim that arbitrary scripts are safe or trustworthy.

The [final grader source](20261112/grader-source-07.py.txt) and every prior grading source are retained. Two intermediate sources were reconstructed from adjacent snapshots and verified against the **exact SHA-256 already recorded in their original grades**; their filenames explicitly say so. No native outputs or old grade results were changed to manufacture a pass. **39 grader regressions** include altered/missing evidence, wrong resource identity, boolean/number substitution, orphan publication, changed helper source, missing diagnostics and modified CLI output.

Claude phase two has a separate **real native finding**: [profile loading was omitted](20261112/claude-02/profile-loading-finding.json). The child loaded the skill and recovery guide, but its parent softened the required profile read to “if useful,” and no full-profile read appears. Its overall **32/33 grade stays failed**. All core recovery outcome checks pass; that supports bounded CF-08 recovery outcome completion alongside the final cold-round evidence, not full instruction conformance. This gap remains under open M2 reliability; later reads cannot retroactively repair it. Repeating the successful import solely for a green score would add no missing recovery outcome.

Claude phase three has a different, **checker-only completion gap**. It uses a real asynchronous named child. Its retained host `task_started`, successful `async_launched` response, completed `task_notification`, child `end_turn` and exact completion text agree on child/call/run/session. The [separate immutable completion audit](20261112/claude-03/async-completion-proof.json), with [retained source](20261112/claude-03/async-completion-audit-source.py.txt), verifies 12 conditions against recorded hashes. The frozen grader's **30/31 remains unchanged**; this supplement supplies the missing completion proof without altering native data, broadening a runtime API or claiming another trial. It does not repair phase two's real profile omission.

An initial archive preflight used a relative kit path and failed its assertion; the absolute-path manifest check passed before the archive was created. Static-check preparation also retained an import-discovery failure and type-inference findings; the frozen native package is not silently relabeled as the later verified distribution.

## Verification and continuation

The [first complete verifier](../verification-runs/20261112T122953.825543Z/result.json) passes **1,138 tests plus one existing Windows privilege skip (1,139 run, 78 new)**, 39 reference checks and distribution probes. These totals include prior work. The [fresh final verifier](../verification-runs/20261112T123657.135315Z/result.json) repeats those passing totals and distribution probes after a standalone-fixture typing-comment placement correction; its complete checked-source hashes match the final implementation. [Final static checks](20261112/static-verification-02.json) pass repository Ruff and scoped Mypy over 44 sources; the [earlier static failure](20261112/static-verification.json) remains. Mypy does not check all untyped function bodies or certify all historical evaluation modules.

The frozen native kit remains unchanged. The later production runtime differs only by one local type annotation in `Workflow.import_image`; the [final-kit audit](20261112/final-kit-compatibility.json) passes **13/13**, checking that exact replacement and normalized syntax while checking all other production payload bytes exactly. The controlled fixture's later typing annotations/import comments are separately covered by local tests; native rounds continue using their exact frozen fixture copies. The final 206-file kit manifest is `8b2cabcd36b7c9d2e755af0daa027efed914e7cb455c4febab56fd6fc7480df6`. The four regenerated reference resources and manifest differ, as explicitly recorded. This is a local identity/compatibility proof, not another native execution or artistic outcome.

The [bounded outcome review](20261112/OUTCOME.json) binds all six original final grades, the separate asynchronous-completion proof and implementation verification. It closes the existing CF-08/TM-03 core recovery exits; **the native trial suite is not an unqualified all-pass**. Human acceptance remains unperformed, separate from this development decision. The [documentation audit](20261112/documentation-audit.json) binds current links, IDs, source hashes and preserved historical evidence, including the unchanged NF-04 snapshot.

**Next: TM-08 directional, animation and tile consumers, supporting CF-09 artistic revision**, selected in M4 PLAN order. Continue [TODO](../../TODO.md), [PLAN](../../PLAN.md) and [SHELVED](../../SHELVED.md) in the same audit cycle. **M1/M2 and broader M3/M4 remain open**, including native instruction conformance, broader domain quality/host reliability and unrelated Claude QOL-10 acceptance.
