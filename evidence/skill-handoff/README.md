# PX-SKILL-001: consequential choice at the handoff

The skill now carries a necessary unanswered choice into the final response and
routes cold resumes without an accepted sample through that guidance. This pace
changes two shared skill files; the production profile, Python runtime and PX1/PX2
semantics are unchanged.

## Observations and revisions

The unchanged native Codex fresh and cold controls saved useful local work but
omitted the necessary question from their final responses. Asking earlier in the
turn or recording an unresolved choice in a file did not satisfy the handoff.

The first revision changed only the intake reference. Its cold trial again
omitted the question: actual tool calls show that it never loaded the reference.
Both fresh trials of that revision reached the 600-second ceiling without a final
answer. Their partial work is retained; neither is a completed handoff.

The second revision also routes an unfinished cold intake to that reference. The
recorded Codex cold trial read it and ended with:

> What canvas size and edge experiment should the first scout trial use? That answer resolves the immediate planning dependency.

That response retained revision 2, saved a new resume report, kept the suggested
32x32 comparison provisional, and reported the missing generation capability.
The exact final response is extracted from the native journal's `final_answer`
event, not from progress messages or a process completion flag. It also quoted
skill implementation guidance unnecessarily; that verbosity remains an observed
limit of this response.

The second revision's Codex fresh start also completed with the direct question,
saved local plans and a provisional comparison recommendation. Claude's fresh
start reached the 600-second ceiling without a final response. The handoff is
verified in these two Codex cases; completed Claude behavior remains unverified.
The criterion review is in `review.md`; raw attempts and frozen packages are
preserved separately from that evaluator judgment.

## Controls and confounds

- A fresh-context unchanged-guidance micro-control did ask an outline question.
  The omission is therefore not universal. See `micro-control.md`.
- Paired handoff-only controls with all choices already supplied asked no
  unnecessary question and preserved existing authorization. See
  `settled-choice-micro-controls.md`. These use supplied state, not executed art.
- Initial native attempts encountered denied shell/image access, even with a
  project inside this repository. Working Codex controls and revisions use the
  same `danger-full-access` native sandbox setting, confined by the trial prompt
  to copied projects. These access-limited attempts are not clean skill controls.
- The historical cold seed validates with its original package but fails with
  the current package at `s.fixture_receipt`: it pins a proof receipt inside a
  mutable kit. `seed-compatibility/result.json` retains the exact comparison.
  This is the newly recorded PX-OPS-002 integration gap; hash rejection remains
  correct. Matched cold trials instead use the same valid, newly recorded seed.
- The unchanged Claude fresh response asked a question but asserted unsupported
  outline/canvas thresholds and that one answer would unblock everything.
  PX-SKILL-002 remains responsible for those artistic-authority errors.

## Identity and verification

Each series freezes its package, fixture bytes, controls and protocol before
inference. The shared native recorder is unchanged. Codex requested and reported
`gpt-6-astra`; Claude selected `claude-opus-5[1m]` and inference events reported
`claude-opus-5`. Model labels are recorded observations, not independent identity
attestation. Model nondeterminism and one attempt per cell limit causal claims.

`audit/20260914T123216Z/result.json` verifies matching brief, cold prompt, fixtures,
host controls and recorder. The first revision differs from the control only in
the intake reference and manifest; the second also changes the main skill.
The verifier subsequently regenerated proof/example resources, so the rebuilt
package has a different whole-package identity. Its entire skill, profile and
runtime content matches the second trial package exactly. Old receipts remain
in the frozen packages and verifier's `previous.zip`.

`verification/20260914T122241Z/` records the checks:

- Full discovery: 388 tests run, 387 passed, one Windows symlink-privilege skip;
  zero failures/errors. All 39 reference checks passed.
- Distribution: checkout to sdist to wheel to temporary installation passed;
  a separate default `uv build` also passed.
- Expanded Mypy passed all 36 source files in `pixl`, `scripts`, `evaluations` and
  `setup.py` with `--check-untyped-defs --explicit-package-bases`. The initial
  invocation without explicit package bases stopped at duplicate module discovery;
  both attempts remain under `expanded-typing*`. The earlier default check also
  passed, but did not check untyped bodies.
- Broad `ruff check .` failed with 479 diagnostics, including retained evaluation
  scripts and supplied training scripts. The unchanged receipts were preserved.
  A separate full maintained-source check passed for `pixl`, `scripts`, `tests`,
  `evaluations` and `setup.py`; its command/output are in the audit directory.
- The first replay retained 28 passing read-only validate/workflow/jobs/family
  operations across seven completed or interrupted states. A replay pass says
  those saved states load; it does not turn an interrupted host into a pass.
  The final Codex state passed four more checks. The Claude replay initially used
  an incorrect assumed `.pixl/state.px` path and failed four checks with `file_read`.
  Its recorded state is `state.px/state.px`; all four corrected checks passed.
  Both replay attempts are preserved. In total, 36 correctly addressed operations
  pass across nine states; the four harness-path failures remain recorded.

## Retained evidence

`archives/` contains five verified ZIP archives with 1,385 files and per-file SHA-256
manifests. They include all twelve native attempts, predecessor copies, frozen
packages, original streams/journals, project artifacts and hidden saved state.
Expanded copies remain locally available and ignored by Git; nothing was deleted
or normalized. Extract an archive into this directory to recover its original
series path. The exact unchanged shared recorder, per-series wrappers and response
extractor are retained. `responses/` gives readable final-answer extracts and
explicitly leaves behavioral judgment to this review.

`final-checks/result.json` verifies source identity against the complete verifier,
every current bundle entry, trial instruction/runtime identity and archive bytes.

Discovery and local mechanics, recorded model behavior, and actual production
outcomes remain separate. No PixelLab job, new character generation, production
visual acceptance or target-engine import was performed. This pace does not claim
that the ecosystem, every module path, or general profile reliability is complete.
