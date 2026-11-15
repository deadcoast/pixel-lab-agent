# TM-01 — incremental boundary typing

Reviewed 2026-11-14 within **IDENTIFY-2026-11-09-01**, continuing from
`0bf54b41e724703e9502a7175936bc1aab930459`. **Human acceptance stays separate and
unrecorded; M1/M2 and broader M3/M4/M5 remain open.**

## Core operation improvement

Publication, job observation, candidate review and handoff now expose checked
Python result shapes. Maintainers can detect a missing publication hash, a
mistyped review verdict or confusion between an observation receipt and a
dispatch request before shipping the change. Existing public JSON, saved records,
runtime validation and recovery routes retain their meanings.

| Boundary | Checked distinction |
| --- | --- |
| Publication | Required revision, canonical hash and state path from the actual publication producers |
| Jobs | Legacy versus durable summaries; observation/preparation, dispatch and import results have distinct required fields |
| Candidate review | Closed observation fields, verdict enums/indices, current review context, retained reports and publication results |
| Handoff | Default receipt versus caller view; absent versus present caller blocks; exact file/hash/line locators |

Raw review and caller inputs pass the existing schema and semantic checks before
being treated as validated shapes. Receipt mode continues to accept legacy expert
details, including a historical field called `caller`; the caller schema remains
opt-in. Provider payloads, journals, lineage/family extensions, continuations and
flexible UDL fields retain their separate validation and are not claimed to be
fully statically typed.

The [maintainer guide](../../docs/BOUNDARY-TYPES.md) gives the repeatable command:

```powershell
.venv/Scripts/python.exe -B scripts/check_boundary_types.py
```

The checker parses its examples without executing their operation calls. It uses
a temporary mypy cache; it neither runs production fixtures nor contacts a model
or provider. Ordinary `mypy pixl` now also applies the six selected module
overrides, including checks inside their otherwise unannotated helper bodies,
incomplete signatures and `Any` returns. Other modules keep their prior checking
scope. This is incremental checking, not a claim of strict typing everywhere.

## Fresh verification

<a id="tm01-boundary-types"></a>The [TM-01 static qualification](20261114/qualification-01/report.json) passes 5/5 checks, including real positive consumers and exactly 13 expected static refusals, with all 50 recorded source/configuration/fixture inputs unchanged; this establishes the declared local type-checking scope, not native behavior or artistic acceptance.

The negative examples exercise missing/wrong publication fields, observation
results used as dispatch results, legacy jobs read as durable jobs, invalid review
enums and observation indices, absent caller fields, invalid locator lines and
caller-only fields read from receipt mode. Positive examples consume the actual
operation return types and narrow their discriminated branches. Static `int`
still admits `bool`; exact JSON integer checks remain runtime responsibilities.

- [Focused runtime regression](20261114/regression-01/RESULT.json): **156 passed,
  two Windows privilege skips** (158 existing tests). Coverage includes valid and
  malformed requests, CLI/MCP results, unknown jobs, stale writes, retained review
  recovery, caller file integrity, exact handoff reuse and interrupted publication.
  These are existing behavior tests rerun against this change, not 158 new tests.
- [Independent review](20261114/review-independent-01.json): **46/46** checks,
  including executable-body comparisons after removing annotations, unchanged
  schemas/specifications and 13 baseline/current caller-validation comparisons.
  Its read-only inspection found no actionable regression. Dynamic extensions
  and optional-field presence correlations remain explicitly outside the claim.
- [Independent gate review](20261114/type-gate-review-01.json): **14/14** checks
  confirm real producer consumption, exact expected diagnostic matching, source
  identity and the non-executed fixture scope. This review does not add new
  runtime or model outcomes.
- [Integrated mypy](20261114/integrated-types-02/RESULT.json) passes all 45 runtime
  modules with the configured incremental scope. [Scoped Ruff](20261114/lint-01/RESULT.json)
  passes the eight changed/new runtime files; [final gate maintenance](20261114/type-gate-02/RESULT.json)
  covers the gate, static fixtures and guide separately.

<a id="tm01-full-verification"></a>TM-01 [full verification](../verification-runs/20261115T003322.792746Z/result.json) passes 1,413 tests with four Windows privilege skips (1,417 run), 39 reference checks and distribution checks; these are local implementation/package results, not native model behavior or artistic acceptance.

The full total consists of existing unit tests, rerun against the final sources;
the static examples are checked separately and never executed as unit tests.
The final built runtime includes the shared type module without adding a runtime
dependency on mypy. The retained full report binds the exact source/configuration
inputs and final bundle manifest.

## Failures and preserved evidence

The [baseline](20261114/baseline-01/typing.json) records default mypy passing with
untyped bodies excluded. The attempted global `--check-untyped-defs` run reports
**21 errors in seven files**, including imported modules. That wider run remains
failed evidence; this increment enables stronger checks on the selected operation
modules without claiming to resolve all unrelated typing gaps.

The first [integrated check](20261114/integrated-types-01/RESULT.json) reports
**eight errors in the HTTP adapter** after the job results become precise.
The adapter now narrows the legacy/durable branch explicitly before reading a
request, and its receipt decorator accepts a read-only mapping. Its existing
runtime rejection of legacy jobs and provider behavior remain unchanged.
The corrected integrated run is a fresh result. The candidate worker's earlier
[actual-configuration attempt](20261114/review-02/RESULT.json) also retains the
then-unfixed store timestamp-narrowing diagnostic.

[Type-gate attempt 01](20261114/type-gate-01/RESULT.json) passes its static probes
but retains two Ruff findings. [Attempt 02](20261114/type-gate-02/RESULT.json)
corrects the gate's import order and explicit subprocess-check style. Its original
source archive remains retained. The older [broad Ruff failure](../deliverable-index/20261114/maintenance-01/RESULT.json)
also remains unchanged; the scoped passes do not close that wider maintenance gap.

The [baseline complete kit](20261114/baseline-01/previous-kit.zip) preserves all
255 original files. Baseline and check-specific source snapshots retain the exact
inputs, while the full verifier archives outputs before rebuilding them. No old
dated receipt or pinned claim line is replaced with a new pass. Current source
applicability remains separate from each original native or artistic outcome.

The [read-only integrity inspection](20261114/integrity-01/RESULT.json) preserves
the selected inputs during inspection and distinguishes current applicability
from retained outcomes. The [documentation audit](20261114/documentation-01.json)
checks links, original finding IDs, open milestones, unchanged pinned claim lines
and archival of replaced generated bytes. It does not regrade native behavior.

## A–E review

- **A — Improve the core operation:** check the dictionaries that cross real
  publication, observation, review and continuation boundaries, so contract
  mistakes cannot silently pass through those maintained interfaces.
- **B — Host compatibility:** CLI/MCP behavior and opaque payload contracts
  remain unchanged; the local checks do not rerun Codex or Claude or establish
  broader instruction following.
- **C — Context and artistic quality:** a valid typed verdict still represents
  an authored judgment. Types confer no viewing evidence, acceptance or artistic
  authority, and unknown provider work stays unknown.
- **D — Another repository:** the shared result types ship with the runtime.
  Consumers do not need mypy or the maintainer test fixtures to use the kit.
  Package checks exercise installation separately from source-only static checks.
- **E — Responsibilities:** runtime validators enforce untrusted input and state
  semantics; type checking catches maintained-code contract mistakes; profiles
  and skills guide production judgment. Official provider execution remains a
  separate operation with its own observations.

Next: **TM-02 — measure context and validation cost**. Optimization remains
conditional on demonstrated need. Keep the active plan, its original 50 findings
and the broader milestone exits open.
