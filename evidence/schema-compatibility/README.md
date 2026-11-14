# SC-06 — saved adapter/schema compatibility

This increment continues `IDENTIFY-2026-11-09-01` and qualifies the saved-format
contracts used by core production. [The compatibility policy](../../spec/adapter-compatibility.md)
separates authored JSON, review inputs and retained adapter metadata from the kit
version and the `PIXL/1` / `PIXL/2` wire headers. It introduces no format migration.
[The bounded outcome index](20261113/OUTCOME.json) binds the exact final receipts.

## Implementation and useful recovery

The connected-plan readers share one immutable snapshot check: supported binding,
wrapper version, artifact hash, authored schema and identity. An unsupported own
binding remains visible as a blocker. Caller comparisons retain their established
unversioned legacy form; an explicit unsupported version cannot count as a
complete comparison. Selected-asset metadata and preparation markers likewise
cannot silently disappear from their allocation/focus guards.

Supported numeric `1.0` inputs remain supported where older readers accepted
them. Existing strict integer formats stay strict. The runtime preserves saved
bytes instead of normalizing version spellings. Unsupported formats return
`adapter_version`, with `use_compatible_adapter` guidance in the public diagnostic
envelope: retain the original file and kit, then use a compatible reader or an
explicitly tested migration. No provider retry or acceptance is manufactured.

## Preserved failures and verification

- [Original plan/comparison probe](20261113/baseline-01/result.json): an unsupported
  own binding lost a changed-scope guard; an unsupported snapshot wrapper passed;
  an explicit version-2 comparison counted as complete. The original probe and
  source identities are retained.
- [Fresh execution of that same probe](20261113/after-01/result.json): unsupported
  inputs are rejected; supported numeric versions, legacy comparison and unrelated
  namespaces retain their earlier behavior.
- [Original preparation-focus probe](20261113/focus-baseline-01/receipt.json):
  boolean versions were treated as version 1, and unsupported/missing versions
  could fall through `task_store` as absent preparation.
- [Original selected-asset guard failure](20261113/selection-baseline-01/result.json):
  three unsupported own-namespace tokens disappeared from selection results. The
  failing log and original reader source remain beside the receipt.
- [Connected-plan focused checks](20261113/runtime-tests-01/result.json) cover
  preserved state/files, unsupported inputs and immutable snapshot readers. The
  earlier test-expectation failure remains separately recorded.
- [Final preparation-focus observations](20261113/focus-confirmation-02/receipt.json)
  preserve numeric compatibility and reject unsupported versions. The
  [focused verification history](20261113/focus-focused-verification.json) records
  overlapping test runs and the corrected interruption fixture; these counts are
  not added together as independent checks.
- [Final full verification](../verification-runs/20261114T032134.229415Z/result.json)
  passed **1,313 tests**, with **two existing Windows symlink-privilege skips**
  (1,315 run), all 39 reference checks and wheel/copied-kit distribution checks.
  [Sixteen test methods](20261113/new-regression-inventory.json) were added for
  SC-06; the suite total includes prior work. The run archives generated files
  before rebuilding them and binds its final source and package hashes.

## Actual installed-kit replacement

The final kit manifest is
`48120249c0a10672db9c773f0ad89d2e178022f4a93edd80a2d8c4e5f2442b79`.
Each proof physically replaces the installed kit at its original path in an
isolated copy of a retained consumer. The original kit remains available outside
that copy. These are local CLI replays of historical host-created projects, not
new native-host trials.

| Retained project | Observed result | Preservation and limits |
| --- | --- | --- |
| Connected successor plan | [Updated-kit request review](20261113/plan-upgrade-01/replacement-result.json) reads revision 126, the same authored plan/snapshot, exact criteria and all 23 current comparison mappings | All 3,032 non-kit files and the original 3,199-file consumer remain unchanged. [Report comparison](20261113/plan-upgrade-01/comparison-summary.json) retains `same_report: false`: only additive `hash_domains` labels differ. The two historical source-range diagnostics remain; semantic verdict stays `not_assessed`, consistency stays null |
| Codex-origin terrain and animation fixture | [Two public executions after replacement](20261113/consumer-upgrade-01/codex-01/upgrade-result.json) and independent artifact checks pass | All 216 preexisting non-kit files, including the old failed execution outputs, remain unchanged; saved review contexts are identical |
| Claude-origin terrain and animation fixture | [Two public executions after replacement](20261113/consumer-upgrade-01/claude-01/upgrade-result.json) and independent artifact checks pass | All 213 preexisting non-kit files, including the old failed execution outputs, remain unchanged; saved review contexts are identical |

[The combined execution receipt](20261113/consumer-upgrade-01/result.json) records
four successful updated-kit runs and unchanged kit identity. All four complete
their browser/server/profile cleanup. The original kits' four cleanup failures
remain in [the old-kit preparation result](20261113/consumer-upgrade-01/preparation.json),
with [separate cleanup evidence](20261113/consumer-upgrade-01/old-profile-cleanup.json).
The updated renderer behavior predates SC-06; this replay qualifies compatibility,
not a new cleanup repair.

The connected-plan fixture's initial `retain-library` attempt was inapplicable and
remains in [its failure receipt](20261113/plan-upgrade-01/retention-result.json).
An [audit of its 45 source records](20261113/plan-upgrade-01/source-dependencies.json)
found no kit-resource dependency requiring retention. The domain fixtures likewise
bind consumer-local sources. Existing library-retention qualification remains
separate; this increment does not claim to recover unavailable historical bytes.

[Final integrity qualification](20261113/integrity-audit-01.json) binds the current
source, archived previous generated files, exact package and replacement receipts.
[Documentation qualification](20261113/documentation-audit-01.json) checks links,
all 50 original finding IDs, the continuing cycle and open acceptance wording.
These checks do not establish new native model behavior, provider execution or
artistic quality. Human acceptance stays separate and unrecorded for this
increment. M1/M2 and broader M3/M4 remain open; bounded SC-06 completion does not
complete M5. The next eligible increment is **TM-05 — declared install/update
support matrix**.

## A–E review

**A — What improves?** A consumer can recover a saved project after updating the
kit without a version mismatch silently removing a production guard. The recovery
message identifies a local format limitation and preserves the data needed to act.

**B — Which hosts are qualified?** The local installed-kit Python/CLI route is
exercised with retained consumer inputs. This increment runs no new native Codex
or Claude specialist; historical host origins identify the fixtures only.

**C — What is artistic context?** Existing art, criteria and reviews supply saved
production context. Format readability, renderer execution and file preservation
do not establish that the art meets new requirements or deserves new acceptance.

**D — Can another repository use it?** The compatibility policy ships with the kit;
adapter versions are independent of checkout paths. Declared installation/update
coverage remains the separate TM-05 work, including environments outside the
bounded retained fixtures.

**E — Who is responsible?** Runtime guards check supported local contracts and
identity. The specialist and caller still review current requirements and actual
outcomes. A format change cannot transfer an old verdict or invent human approval.
