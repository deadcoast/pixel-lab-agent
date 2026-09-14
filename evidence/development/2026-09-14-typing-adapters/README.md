# Typing and JSON input repair, 2026-09-14

The expanded Mypy check now passes, and CLI/MCP inputs reject duplicate JSON
object members before executing an operation. Before the repair, the decoder
silently kept the last value: CLI encoding could overwrite a saved file, and an
MCP request with two store paths could create the second store and report success.
PX1/PX2 wire syntax, version selection and valid saved-state behavior are unchanged.

The first branch convergence fast-forwarded `main` to
`fbca45c13124729cb1f7341ff5e04c6a48be4ca4`, preserving the earlier packaging repair.
Both GitHub branches were checked at that commit before this development began.
The pre-merge full-suite [log](branch-convergence-pre-merge-tests.log) records
383 tests: 382 passed and one Windows symlink-privilege skip. The changes described
below follow that preserved base.

## Changes and retained failures

- [Baseline typing](baseline-types.log): 24 diagnostics in nine files. Collection
  annotations and distinct local names correct inference conflicts. A narrow
  constructor protocol describes the installed referencing library's generated
  keyword argument without changing the explicit retrieval-denial callbacks.
  The RGBA pixel cast records the image mode already established by the fixture.
  No function-body checks or project coverage exclusions were disabled.
- [Failing boundary regressions](ambiguous-json-before.log): seven failing
  assertions/subtests across five tests; the valid PX1/PX2 round trip already
  passed. These execute real CLI and MCP subprocesses, not mocked service calls.
- [Passing boundary regressions](ambiguous-json-after.log): duplicate top-level,
  nested and escaped member names are rejected. Existing output remains byte
  identical, ambiguous MCP initialization creates no store, and the server handles
  the following valid request. Distinct objects may reuse the same member names.
  Nonfinite JSON values remain rejected.

The shared decoder in `pixl/service.py` serves file inputs and MCP stdio. CLI
file failures return `json_read`; MCP reports a parse error before dispatch. Error
messages do not echo supplied values. The tests cover these particular behaviors;
they do not establish that every adapter operation is complete.

## Final verification

The [full verifier](../../verification-runs/20260914T100937.559085Z/result.json)
records 388 discovered and executed tests: **387 passed, zero failures/errors,
one symlink-privilege skip**. It also records **39/39 reference checks**, 43 methods
and 93 source ranges. Its initial `runs:1, errors:1` stdout line belongs to the
deliberate recorder-rejection fixture; the complete suite result is separate.

- [Mypy](release-types.log): 36 maintained runtime/build/evaluation source files,
  with `--check-untyped-defs` and explicit package bases. Unannotated interfaces
  still exist, so this is not a claim that the entire runtime is statically typed.
- [Ruff](release-lint.log): maintained runtime, scripts, tests, evaluations,
  setup, both generated runtime copies and plugin launcher scripts passed.
- [Distribution](../../verification-runs/20260914T100937.559085Z/wheel-check.json):
  checkout → sdist → wheel → temporary installation passed, including five source
  document hashes and **33 installed CLI operations**. The isolated installation
  reuses existing dependencies. Separately, the exact [uv build](uv-build.log)
  command produced fresh local `dist/` artifacts.
- [Copied inspection](inspection/report.json): **11 operations**, 10 prepared
  views, using a controlled saved fixture and developer-supplied observations.
  The probe source is retained. Complete package/project copies (including store
  history otherwise ignored by Git) are in `inspection/snapshots.zip`, with a
  separately verified SHA-256 manifest. Extract into `inspection/` to restore the
  recorded relative layout.
- [Final identity check](summary.json): all 86 verifier input hashes and all 101
  bundle file hashes matched after the checks. Previous generated evidence is
  retained in the verifier run's `previous.zip` with its hash manifest.

Commands, exit codes, durations and input hashes accompany the logs as JSON.
Intermediate typing and lint failures remain alongside final results. The command
recorder source is retained in `command-recorder.py.txt`; it was executed from
`build/development_evidence.py`.

## Measured limits

[Coverage JSON](coverage.json) and the combined `coverage.sqlite` database retain
line and branch results from the full verifier and its subprocesses. The 20
checkout runtime modules measured **3858/4078 executable lines (94.61%)** and
**1428/1612 branches (88.59%)**. There remain **220 unexecuted lines and 184
unexecuted branch outcomes**. Combined coverage is 92.90%; `service.py` is 73.60%,
`cli.py` 85.22% and `platform.py` 88.15%.

Coverage's default ellipsis rule lists four physical lines around the new Protocol
method declaration as excluded (including adjacent blank/comment lines). No
project exclusion was added. Installed/copied runtime paths are not merged into
these checkout percentages. Coverage measures execution, not assertion strength,
all possible inputs or module completeness.

This work exercised local tools, package relocation and scripted workflow
mechanics. It did not run a fresh model/profile behavior evaluation, real PixelLab
generation, artistic acceptance, target-engine import or a clean-machine dependency
installation. Those outcomes remain separate work.
