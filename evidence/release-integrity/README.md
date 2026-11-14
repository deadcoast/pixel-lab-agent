# TM-10 — read-only evidence/release integrity

This increment continues `IDENTIFY-2026-11-09-01`. The
[maintainer command](../../docs/EVIDENCE-INTEGRITY.md) checks whether a declared
capability's retained evidence is intact and whether its tested inputs still
match the current checkout. It prints diagnostics and next actions without
rebuilding packages, rerunning native/art trials or changing production state.

## Implementation and declared scope

`scripts/check_integrity.py` reads an explicit version-1 registry containing
15 claims and 54 pinned receipts. It covers all ten current core-task table
anchors, separates local installation from native setup, and keeps actual-art,
historical full-suite, dated claim-review and preserved-failure scopes distinct.
Each anchored claim line has its own byte identity. Current bindings derive from
hashes in pinned receipts, rather than treating today's untested bytes as tested.

The command separates receipt integrity, recorded outcome, source/package
applicability and claim wording. It validates exact JSON-pointer assertions,
closed declaration shapes, duplicate keys/IDs and confined paths. It follows
registered retained references; external Windows temporary paths and Linux
`/tmp` execution locators remain historical context. A failed or partial trial
retains its actual outcome even when a declaration incorrectly expects a pass.

The shared pure bundle plan in `scripts/build_plugin.py` feeds both the existing
builder and the new release inspector. Inspection checks the complete expected
bundle mapping, canonical bytes, generated requirements and supplied-source
identity. Exact retained wheel/sdist archives are inspected without extraction
or installation. The builder's writing phase remains an explicit separate call.
No production runtime, UDL semantics, common skill or live bundle was changed.

## Fresh verification

- [Checker tests](20261114/checker-tests-02/RESULT.json): 27 passed and one
  Windows symlink-privilege skip, 28 run; Ruff passed.
- [Release tests](20261114/package-01/checks-02/RESULT.json): 38 passed,
  including 20 new release tests and 18 existing source/builder tests; Ruff passed.
- [Actual package/parity proof](20261114/package-01/RESULT.json): 3,344
  original files retain identical bytes and mtimes. Old and refactored builders
  produce the same 251 portable files from 203 exact source files in isolated
  roots. The live kit remains unchanged at manifest
  `48120249c0a10672db9c773f0ad89d2e178022f4a93edd80a2d8c4e5f2442b79`.
- [Independent source/registry review](20261114/review-01.json) checks exact
  final sources, claim bindings and preserved scope. It is assistant review,
  separate from the executed tests and CLI outcomes.
- [Actual CLI qualification](20261114/integration-01/RESULT.json) passes all
  ten cases. The live checkout check preserves 85,043 inspected source/evidence
  files with identical bytes and mtimes. A relocated 685-file checkout supports
  the same inspection. Isolated source/payload/claim changes, a missing receipt
  and a newly added module produce the required diagnostics without repair.
  A selected historical failure remains `fail`; human-readable output and an
  unknown-claim refusal are exercised separately. Every case preserves its
  inspected file set, bytes and mtimes.

These are **65 passing focused tests and one skip**, not a fresh full production
suite. The older SC-06 suite retains its original 1,313 passing tests and two
skips. No new model invocation, provider request, generated art or destination
acceptance is credited to TM-10.

## Current findings are preserved

The [final checkout report](20261114/final-check-01/stdout.json) is expected to
need review. The prior full-suite
receipt is intact, but subsequent changes and new source/test files mean it
does not cover the entire current checkout. The dated NF-04 review also has
changed document/source inputs. Both original passing outcomes remain intact;
these findings do not prove a runtime regression.

The current bundle and the tested wheel still match their checked canonical
payloads. The retained sdist's exact digest is intact, while its README differs
from today's README. This source-applicability finding remains visible. No
archive was rebuilt or relabeled to clear it. The new command is not a release
approval gate and does not close broader M5 qualification.

The [registry correction](20261114/registry-01/RESULT.json) preserves its first
authored version with invalid terminal-slash prefixes and the corrected version.
CORE-EXECUTE now binds the distinct TM-07 and both TM-08 host kit identities.
The first checker test's help-wrapping assertion failure remains in
[checker-tests-01](20261114/checker-tests-01/RESULT.json); the assertion now
compares normalized help text. The package proof retains a rejected absolute
artifact locator before the explicit repository-relative locator was supplied.
Earlier product, native and grading failures remain unchanged.

## A–E review

**A — What improves?** Maintainers can inspect a core capability or a proposed
release without starting a rebuilding verifier. Exact changed paths and scoped
actions distinguish a missing receipt, a stale package and an old qualification.

**B — Which hosts are qualified?** This is a local maintainer inspection command.
It reads prior Claude/Codex outcomes and preserves their host versions and
package boundaries. It performs no new native-host qualification.

**C — What is artistic context?** The registry retains actual-art and reused-art
scope, partial/failed observations and separate acceptance. Hash equality cannot
add aesthetic judgment or transfer a prior verdict to new requirements.

**D — Can another repository use it?** The inspector can target another checkout
through an explicit root and registry. Consumer readiness and production remain
their existing operations. A copied runtime alone is not a maintainer evidence
checkout and is not silently treated as one.

**E — Who is responsible?** The checker verifies declared identities and current
applicability. Maintainers review claim scope and choose new qualification;
specialists/callers still judge actual work, and official provider execution
retains its own authorization and observations.

Human acceptance stays separate and unrecorded. M1/M2 and broader M3/M4/M5
remain open. TM-10's bounded integrity operation is complete. The next
PLAN-ordered development item is NF-07, the consumer deliverable index. Broader
release qualification and human acceptance are not inferred from these checks.
