# Build and verification audit

Started 2026-09-13; final verification 2026-09-14. Maintainer work in the existing
uv-managed Python 3.14.3 environment. [Machine-readable summary](summary.json).

## Reproduced faults and repairs

1. Commit `861d771` moved five source documents into `docs/research/`, while the
   inventory, curated citations, manifests and runtime still required
   `training/original-docs/`. Every relocated file matched its declared SHA-256
   and line count. The declared paths were restored by copying those exact bytes;
   the research-directory files, inventory identities and runtime semantics were
   preserved. Adding Python packages could not supply these project documents.
2. `scripts/check_wheel.py` used `uv build --wheel`, which skipped the sdist route.
   It now uses the default build route, verifies each source document in both
   archives and every runtime module/registry in both wheel runtime copies, then
   exercises the installed wheel from an unrelated directory.
3. Early verifier errors left an older passing `test-results.json` in place.
   Each attempt now archives prior generated outputs, publishes running/failure
   status, lists all discovered test IDs, checks for source changes during the
   run, and records unperformed stages. The full distribution check is part of
   the verifier. The two regression tests failed against the old implementation
   and passed after correction ([red](regression-red.log), [green](regression-green.log)).

## Executed results

| Check | Result | Evidence |
| --- | --- | --- |
| Baseline full unittest discovery | 381 run: 335 passed, 45 errors, one skip | [log](baseline-tests.log) |
| Baseline ordinary uv build | Failed with the reported `source_missing` | [log](baseline-build.log) |
| Final locked uv sync and ordinary uv build | Both exit 0; sdist and wheel produced | [sync](final-sync.log), [build](final-build.log) |
| Final full verifier, measured with coverage | 383 discovered/run: 382 passed, zero failures/errors, one Windows symlink-privilege skip | [run](../../verification-runs/20260914T094609.319493Z/result.json), [console](final-instrumented-verifier.log) |
| Reference fixtures | 39/39 passed, supporting 43 curated methods and 93 checked citation ranges | [run](../../verification-runs/20260914T094609.319493Z/result.json) |
| Installed wheel | 33 scripted CLI checks; source identities and import origin verified | [receipt](../../verification-runs/20260914T094609.319493Z/wheel-check.json) |
| Ruff, all maintained Python plus generated runtime copies | Passed | [log](final-lint-recheck.log) |
| Expanded Mypy, including untyped bodies | 24 diagnostics in nine files remain | [log](final-support-types.log) |

The console's `{"runs": 1, "errors": 1}` line comes from a deliberate
recorder-integrity rejection test; the complete unittest result is recorded
separately. Successful tests establish their asserted behaviors, not complete
module correctness. The runtime Python files and registries were unchanged by
this repair; regenerated knowledge, fixtures and plugin copies have fresh receipts.

## Measured runtime coverage

The final full verifier covered **94.49% of executable lines**
and **88.31% of branches** in the checkout's 20 runtime files.
The combined line/branch figure is **92.74%**. There are
**224 unexecuted lines and 188 unexecuted branches**;
no lines were excluded. [Exact missing lines/branches and per-function data](coverage-final.json),
[text report](coverage-final-report.log), [retained combined data](coverage-final-data).

| Runtime file | Combined coverage | Missing lines | Missing branches |
| --- | ---: | ---: | ---: |
| `pixl\__init__.py` | 100.0% | 0 | 0 |
| `pixl\__main__.py` | 100.0% | 0 | 0 |
| `pixl\assets.py` | 90.0% | 6 | 4 |
| `pixl\catalog.py` | 92.6% | 3 | 2 |
| `pixl\cli.py` | 84.9% | 23 | 21 |
| `pixl\codec.py` | 90.9% | 16 | 14 |
| `pixl\delivery.py` | 95.9% | 8 | 4 |
| `pixl\families.py` | 99.0% | 1 | 1 |
| `pixl\graph.py` | 96.7% | 8 | 4 |
| `pixl\inspection.py` | 98.9% | 4 | 0 |
| `pixl\inspection_views.py` | 95.5% | 12 | 8 |
| `pixl\job_history.py` | 98.9% | 1 | 1 |
| `pixl\jobs.py` | 94.7% | 10 | 8 |
| `pixl\lifecycle.py` | 99.7% | 0 | 1 |
| `pixl\mcp.py` | 87.4% | 6 | 5 |
| `pixl\platform.py` | 88.1% | 53 | 58 |
| `pixl\poc.py` | 97.2% | 12 | 9 |
| `pixl\service.py` | 70.3% | 49 | 37 |
| `pixl\sources.py` | 97.0% | 2 | 0 |
| `pixl\store.py` | 90.6% | 10 | 11 |

Coverage.py 7.16.1 was added with `uv add --dev coverage`. Branch measurement and
[subprocess instrumentation](https://coverage.readthedocs.io/en/latest/subprocess.html)
are configured in `pyproject.toml`. The measured source root is the checkout's
`pixl/`; separate relocated/installed runtime paths are not merged into that
percentage. Passing packaging operations remain their own evidence. The earlier
full-unittest-only measurement is retained in [coverage.json](coverage.json).
Execution coverage does not establish assertion quality, all input combinations,
instruction following or artistic outcomes.

## Remaining qualification

The [default Git whitespace check](whitespace-default.log) flags CRLF endings in
generated hash-bound receipts. The [CRLF-aware check](whitespace-crlf.log) passes;
receipt bytes were preserved. All 99 local links in the updated README,
verification guide and this audit resolved during the final documentation check.

The expanded Mypy command reports 22 diagnostics in runtime modules and two in
support scripts. Some concern local variable inference and some concern the
`referencing` dependency's generated constructors. They were not suppressed to
obtain a passing report. Default Mypy coverage of annotated bodies is a narrower
check. Existing dependency metadata also still mixes runtime and developer tools.

This pass exercised local runtime/CLI/MCP and packaging mechanics. It did not run
fresh native profile/skill behavior trials, real PixelLab production, visual
acceptance, target-engine import, or clean-machine/cross-version installation.
The ecosystem as a whole is not certified complete.

## Retained evidence

[before.zip](before.zip) and its [SHA-256 manifest](before-manifest.json) retain
1,861 files before the first baseline run, including earlier receipts and generated
copies. Failed baseline and regression logs are separate from final logs.
[user-dist-before-complete.zip](user-dist-before-complete.zip) preserves the user's
previous failed source archive; `user-dist-before.zip` is the partial archive from
the sandbox-denied first preservation attempt. Each verifier run additionally
retains `previous.zip`, its hash manifest, its own result and detailed logs.
