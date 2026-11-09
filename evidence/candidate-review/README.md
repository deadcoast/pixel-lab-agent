# Ordinary candidate and family review

M1 findings **NF-01, NF-02 and CF-01** now have a shared public implementation:
[review-context and candidate-review](../../spec/candidate-review.md), exposed as
CLI commands and local MCP tools. The operation applies explicit specialist
judgments to existing candidates, retains exact observation files, derives E/V
bindings, and optionally nominates/completes through the existing lifecycle.
It supports both raster candidates and immutable family manifests.

## Implementation and local verification

The request has a closed versioned schema, exact semantic binding hash, current
canonical state hash, per-criterion reasons/supersession and observation file
hashes/modes. Record/nominate/complete are explicit actions. Partial, failed and
unavailable reviews remain representable. Prepared inspection-packet coverage
rules retain their prior meaning; this route accepts actual external observations
such as recorded playback and destination reports, not invented viewing claims.

Review and task completion share the extracted `completion.planned_steps` operation.
The whole sequence is checked before publication. If publication is interrupted,
repeating the identical review ID/payload with a current state hash reuses the
retained review and finishes remaining steps. Old verdicts remain, supersession
is explicit, and current acceptance is shown separately from the package's
immutable creation status. No provider action follows from review publication.

The [full verifier](../verification-runs/20261109T164301.724380Z/result.json) passes
**581 tests with one Windows symlink-privilege skip**, including 11 new review
regressions and five result-export regressions, 39 reference checks and clean
installed-wheel/copied-plugin review/export probes. The final focused
review/completion/export run passed 23 tests; the affected export/family/comparison
run passed 28 tests. These groups overlap and are not additional suite totals. Checks cover partial
and failed/unavailable results, current supersession, stale state/criteria, file
identity, evidence mode, path confinement, pending work, interruption after review
and activation, retained-file tampering, manifest immutability and CLI/MCP parity.

The [first full attempt](../verification-runs/20261109T161125.609112Z/result.json)
is preserved: 575 passed, one failure and one skip. The new distribution probe
imported its test fixture eagerly, causing the missing-source verifier fixture to
fail at import instead of reporting the missing source. Moving that fixture import
inside the probe fixed the failure; the [second full run](../verification-runs/20261109T161411.418370Z/result.json) passed 576 tests plus one skip before export was added.
The [first export-inclusive full run](../verification-runs/20261109T163818.273985Z/result.json)
passed 579, failed two and skipped one: existing family/request-review tests still
asserted unconditional read-only MCP annotations. Optional file export correctly
makes those tools capable of writes. Updating those assertions retained the
default query behavior; the final run passed all 581 executable tests. Early default
sandbox temp/cache attempts also hit filesystem permissions; project-local temp
paths and the authorized verifier execution resolved those environment failures.

## Exact file-output repair

MCP `result_path` and CLI `--result-path` provide a consistent export route for
context, request comparison, candidate/family review, family snapshots and PLAR
handoff. The tool serializes the full result and returns its path, SHA-256 and
byte count. A fresh root-confined path is checked before an operation; existing
files are preserved. If export fails after publication, the response preserves
the actual operation result so the caller can reconcile state safely. Default
output is unchanged, and full CLI wire context stays PX text.

[The final-kit follow-up](../../evaluations/candidate_review_export_case.py) copies
each completed native trial and retains both older kits. Native callers export
current context and the large family report, then replay the exact accepted
review into another result file. This separately verifies the export repair;
it does not rewrite the initial trial or claim another artistic review.

- **Claude:** [native result](20261109/native/claude-export-01/project/work/export-review/EXPORT-RESULT.json)
  and [13 independent checks](20261109/native/claude-export-01/independent-export-checks.json)
  pass. It used MCP for context and a 99,817-byte selected-family report, compared
  their exports byte-for-byte with CLI exports, and used CLI for the identical
  accepted-review retry. The malformed original and caller correction remain.
- **Codex:** [native result](20261109/native/codex-export-01/project/work/export-review/EXPORT-RESULT.json)
  and [13 independent checks](20261109/native/codex-export-01/independent-export-checks.json)
  pass. Its exported all-family report is 297,490 bytes; exact context and retry
  results parse and match returned identities. Both trials preserve accepted
  state and all prior inputs/kits, with zero new review publications.

Both report sizes exceed Windows' command-line length boundary; full JSON is
written by the runtime rather than embedded in a command. These are fresh native
caller export checks, not another delegated artistic assessment.

[Final package checks](20261109/verification/final-package-checks.json) verify all
168 bundled file hashes and no drift in the full verifier's checked inputs.
The frozen export kits have identical runtime/contract code to the final bundle;
the later full verifier regenerated four reference/proof/example resources, and
three skill references received trailing-whitespace cleanup. These differences
are retained explicitly rather than claiming byte-identical whole packages.
Ruff passes the affected modules, and configured Mypy passes 33 source files with
its existing untyped-body limitations. [Documentation checks](20261109/verification/documentation-checks.json)
keep all 50 finding IDs mapped once to SHELVED and validate the selected links.

## Native scenario and results

[The evaluation adapter](../../evaluations/candidate_review_case.py) copies the
existing successor and restores its retained revision-119 state, immediately
before Working motion acceptance. It keeps original assets, seven passing Working
criteria, the unavailable motion verdict, prior observations and historical state.
The current kit is installed alongside the original source-bound kit. Each caller
delegates review, completes Working, creates/reviews a fresh family snapshot,
executes both consumers through the existing isolated renderer, and tests an
identical retry. Native judgments concern retained actual assets; this scenario
does not commission new generation or qualify unfamiliar asset domains.

- **Codex 0.167.0:** completed through a generic native child applying the PIXL
  profile, with independent parent review. Named custom-role selection is not
  claimed. Its [result](20261109/native/codex-01/project/work/native-review/REVIEW-RESULT.json)
  completes Working and the collective family at state revision 126. The fresh
  renderer checker passes 233 assertions over both consumers; recorded normal,
  reduced and restored-motion behavior and exact package/consumer hashes were
  independently inspected by the caller. [Independent repository checks](20261109/native/codex-01/independent-checks.json)
  pass 15 checks for retention, lifecycle, exact files, the four new verdicts and
  retry without duplicate publication. The original unavailable verdict is
  retained/superseded; the manifest still records its initial `accepted:false`.
- **Claude 2.1.318:** completed through its registered `pixl` child, followed by
  independent parent checks and a CLI retry. Its [result](20261109/native/claude-01/project/work/native-review/REVIEW-RESULT.json)
  completes Working and the collective family at revision 126. The fresh renderer
  and caller recheck each report 233 passing assertions. [Independent checks](20261109/native/claude-01/independent-checks.json)
  pass the same 15 state/retention conditions. The [native trace review](20261109/native/claude-01/native-trace-review.json)
  retains registered-role delegation, 66 image-read calls and the saved-copy defect.
  Its parent detected invalid JSON in the specialist's hand-copied snapshot result,
  preserved it and wrote a separately identified correction. Accepted state and
  immutable manifests were valid throughout; this was a result-copying failure.

Codex retained its local member-hash/motion-check script mistakes and corrected
them within the native run. They were not erased or counted as passing attempts.
The new review operation required no maintainer state/evidence reconstruction.
The root developer additionally inspected both saved destination screenshots;
that corroborates the static comparison only, not playback by itself.

## Required A–E review

**A — Improvement.** The previously hand-written evidence/verdict/nomination steps
now use one explicit operation. Direct result-file export removes a copying failure observed in Claude. Remaining
M1 work includes narrower relevant-choice context and concise successor diffs.

**B — Host compatibility.** The implementation is the same CLI/MCP operation in
both harnesses. Native trials retain their actual host roles; a generic Codex
child is not reported as named-role qualification. Claude used its registered
`pixl` child and the same public review operation. Same-child continuation and the earlier interrupted criteria comparison
remain separate M2 work.

**C — Contextual/artistic quality.** Exact literal criteria and candidate/source
bindings preserve what is being judged. The specialist uses the host's pixel-art
knowledge, actual image access and renderer observations to supply judgments.
Retention/validation does not infer meaning, aesthetic quality or actual viewing.
This reused queue family does not establish broader generated quality.

**D — Consumer operation.** The scenario uses the existing consumer, actual assets
and isolated renderer without desktop takeover. Roots, semantic bindings, file
hashes and immutable/current status are explicit. Other consumers and cold
assignments remain broader qualification work.

**E — Responsibility placement.** The profile still supplies expertise and
authority; inspection/family skills explain when/how to review; the new adapter
and shared completion planner retain/check the declared result; the host supplies
image/execution tools; official PixelLab retains generation responsibility.
No second saved-state language or standalone model was introduced.

## Continuation

Actual native outcomes are linked in [TODO](../../TODO.md) and [SHELVED](../../SHELVED.md).
Next is SC-04 focused relevant-choice context and QOL-08 concise successor
comparison, followed by remaining hash labels and the everyday guide.
The [PLAN](../../PLAN.md) remains active. Completing this operation is an M1 slice,
not completion of M1's remaining usability exits or the overall product.
