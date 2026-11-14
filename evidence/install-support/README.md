# TM-05 — declared install/update support

This increment continues `IDENTIFY-2026-11-09-01`. The
[consumer support matrix](../../docs/INSTALL-SUPPORT.md) distinguishes the package's
declared prerequisites, freshly executed local routes and native-host behavior.
The [setup guide](../../docs/AGENT-KIT.md#set-up-a-consumer-project) remains the
consumer entry point. No new runtime operation or saved-state migration is added.

## Qualification scope

The current production kit is the unchanged SC-06 payload, manifest
`48120249c0a10672db9c773f0ad89d2e178022f4a93edd80a2d8c4e5f2442b79`.
The last full production verifier remains
[the SC-06 run](../verification-runs/20261114T032134.229415Z/result.json): 1,313 passed,
two Windows privilege skips, 39 reference checks and distribution checks. Those
are retained results, not newly executed TM-05 tests. This increment adds a
maintainer evaluator, targeted evaluator tests and actual installation trials;
it does not regenerate historical proofs or the kit merely to update documentation.

[Five final local rows](20261114/local-01/FINAL.json) pass: Windows 11 x64 Python
3.11.14, 3.12.10, 3.13.12 and 3.14.3, and Ubuntu/WSL2 x86_64 Python 3.12.3.
The rows record 341 commands against the same final evaluator source. Each
qualifies copied-kit and installed-wheel use, actual kit replacement and cold
reads after moving the consumer. Windows Python 3.14.3 additionally qualifies
fresh locked-source installation/use, without a source-relocation claim.
Declared Python `>=3.11` metadata alone does not qualify other combinations.

Each copied-kit/wheel move preserves 56 consumer files and the same prepared
job, requirements and state. Each update preserves the old kit and all 3,032
nonkit files in the retained SC-06 consumer, with its 23 comparison mappings.
All 47 runtime Python/JSON payload files match the frozen kit. The final WSL
row runs on its Linux-native filesystem; the earlier Windows-mounted-filesystem
row also passed under its earlier evaluator source. The
[staging](20261114/local-01/wsl-native-staging-01/RESULT.json) and
[return manifest](20261114/local-01/wsl-native-staging-01/RETURNED.json) preserve
the exact inputs, execution locators and returned receipt bytes.

Local probes prepare useful PLAR work, preserve a pending request and reread it
from new processes after moving the kit and consumer. Controlled local dispatch
claims and synthetic job observations in those probes are not PixelLab requests.
Same-path kit replacement also rereads a genuinely retained connected plan.
Virtual environments stay at a fixed location or are recreated; moving a kit does
not repair absolute host configuration or console-entrypoint paths.

[Fresh native trials](20261114/native/RESULT.json) pass **Codex 19/19** and
**Claude 18/18**. They use the existing readiness clean scenario, the current kit,
a fresh minimal Python environment and isolated consumers. Codex 0.167.2 and
Claude Code 2.1.318 load the registered specialist, read its instructions,
execute source/library/readiness operations and consume the returned reports.
Their original inputs remain unchanged. These runs do not test native
continuation across relocated paths or updated packages. Local cold artifact
recovery and native same-session continuation remain distinct claims.

Fresh focused validation is **39 passing tests**: 12 for the installation
evaluator and 27 for the readiness grader, with Ruff passing for both changed
areas. Seventeen test methods are new. Four historical native traces also pass
fresh final-grader checks; these are regrades of retained executions.

## Failures and exact identities

Each new attempt uses a fresh directory, retaining commands, outputs, package and
consumer identities. An interrupted or failed cell stays in the record when a
corrected attempt is added. Earlier readiness, library-retention, SC-06 and native
failures remain unchanged.

The [development history](20261114/local-01/development-history.json) retains
three harness failures (interpreter path, inventory root and CLI argument),
earlier passes with narrower checks, and their original source identities. The
final index also retains the lint failure and all five pre-lint-cleanup passes.
The [first source-review mismatch](20261114/harness-review-01.json) remains
alongside its corrected review; it was review-source drift, not a runtime fault.
An actual Python 3.10.19 negative trial rejects the unsupported interpreter
without modifying the kit or empty consumer.

The native grader originally reported Codex 18/19 and a Claude reference-shape
error. Narrow grader corrections recognize the recorded tool enumeration and
one explicit file-reference wrapper while retaining hash, confinement and
paired-success checks. The original grades, unchanged native reports/traces,
correction receipts and negative tests remain in the
[native index](20261114/native/RESULT.json). Claude also corrected its own
relative-path mistake during the same recorded run. No external report edit or
manual continuation converted these failures into success.

The temporary wheel from the SC-06 full verifier is unavailable. The files later
present in `dist/` have different digests and cannot stand in for that receipt.
TM-05 builds and retains a fresh wheel from an isolated source snapshot and records
its own identity. A shared `1.0.0` version label is not evidence of identical bytes.
The [new distribution receipt](20261114/distribution-02/RESULT.json) binds wheel
SHA-256 `b1bfb390f9a45df4f9663ae62491883c12bec5f15af8a0a7d129fb72715e7846`.

## A–E review

**A — What improves?** Consumers can choose an observed install route and recover
saved production after an update or move. The guide explains the concrete path
and environment work needed instead of leaving users to infer portability from a
successful dependency install.

**B — Which hosts are qualified?** Local CLI/MCP operation, static registration,
native instruction loading and useful caller outcomes receive separate evidence.
The fresh Windows host trials and historical trials retain exact versions and
kit identities. WSL local-runtime results do not establish Linux-native hosts.

**C — What is artistic context?** Installation and retained-state reads make the
asset workflow reachable. They establish no new generated quality, source-specific
visual judgment or target-engine acceptance. Existing art and criteria keep their
original provenance and verdicts.

**D — Can another repository use it?** Fresh isolated consumers exercise copied
kits, runtime dependencies and installed wheels without the maintainer environment.
Relocation must preserve project state and explicitly rebind host paths. Only
the named route/OS/interpreter combinations receive qualification.

**E — Who is responsible?** The package supplies deterministic local operations;
host adapters load the profile and skills; the specialist and caller still own
current artistic decisions and outcome review. The official provider connection
retains its independent authorization and authentication requirements.

Human acceptance stays separate and unrecorded for this increment. M1/M2 and
broader M3/M4/M5 remain open. TM-05's bounded support declaration and
qualification are complete. The next PLAN-ordered development item is TM-10,
read-only evidence/release integrity; untested platforms and broader reliability
retain their open scope.
