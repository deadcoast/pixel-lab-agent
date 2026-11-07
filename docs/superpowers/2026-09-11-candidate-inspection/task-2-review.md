# Task 2 independent operation review

Status: PASS after corrections. No unresolved blocking findings in the reviewed operation/adapters.

Reviewed the accepted candidate-inspection design, current operation module and tests,
PX2 specification/registry, graph proof scope, store transition/CAS rules, retained
file publication helper, thin CLI/service/MCP adapters and their operation tests.
Read the project review and production profile as development artifacts. Renderer
implementation was independently reviewed elsewhere; this review covers its operation
integration. No source implementation, generated bundle, provider or model was changed
or executed by this reviewer.

## Validated findings

1. Important: a candidate visual failure could be published after declaring only a
   reference view. The observation validator required a nonempty observed-view set,
   without any candidate-source observation. A fixture review of reference-only
   packet.view.5 published failed candidate E/V. Require an observed candidate-source
   view for visual/continuity or visual-mode judgments; failures may still be partial.
   Evidence: `evidence/candidate-inspection/reference-only-review-probe.py` and
   `reference-only-review-pre-fix.json`. This tightens the design's overly broad
   phrase 'actual supplied view'; the final implementation/spec now makes candidate-source observation explicit.

2. Important: closed artifact equivalence used Python equality, which accepts
   `True == 1` and `32.0 == 32`. Both packet metadata version `true` and a canonical,
   rehashed manifest with view width `32.0` passed ordinary graph validation and
   the inspection loader with `files_verified:true`. The latter was returned as
   a float in the report. This concerns the promised closed typed artifact check,
   not cryptographic authorship or arbitrary generic rewriting. Compare canonical
   tagged bytes/record hashes wherever exact original fields, rendering, typed
   projections, coverage or semantic drift are verified. Evidence:
   `evidence/candidate-inspection/closed-type-equivalence-probe.py` and
   `closed-type-equivalence-pre-fix.json`. Both observations used operation source
   SHA256 `4176e0c8607b0d9cd90334a6f9486529db0dcf4c7e792de7867be3484df5027c`.

## Verified behavior and boundaries

- `uv run --no-sync python -m unittest tests.test_inspection tests.test_inspection_operations`
  initially passed 16 tests, including real subprocess CLI/MCP discovery, closed
  mutation envelopes, prepare/review round trips, cold reports, stale retries and
  root confinement.
- Independent probe `operation-review-probes.py`, retained result
  `operation-review-probes-01.json`, rejected future, pre-preparation and naive
  timestamps; unobserved visual failure; engine pass; and nonexistent supersession.
  Each rejection preserved the canonical saved state hash.
- That probe also created a failed visual review, properly obsoleted its E/V,
  amended Q and committed. Cold inspection preserved original criterion text and
  the retained failed review while reporting criterion binding drift. This covers
  amendment after review rather than only amendment before any verdict exists.
- Packet preparation retains original semantic X/F/C/Q/I/S closure as tagged bodies
  and record hashes, excluding mutable workflow T/P nodes while retaining task
  identity. No nomination/task status/E/V is changed by preparation.
- Review uses original saved criteria, rejects stale semantic bindings, requires
  fresh operation/generated IDs and exact current-V supersession, creates E only
  for performed local criteria, and appends V through the ordinary saved-plan and
  CAS commit. Done tasks must reopen. Separate candidates inherit no verdict.
- File capture is bounded and hashed before rendering. Publication uses confined,
  content-addressed, write-once files. A lost CAS may leave orphaned immutable files,
  as documented, without advancing state. Source and retained-path resolution is
  confined; retained publication paths reject redirected storage. Symlink races
  were reviewed statically, not stress-tested as hostile concurrent filesystem work.
- Loader reconstructs rendering from retained inputs and checks file bytes, original
  record closure and report projections. Final-source verification establishes strict scalar type equivalence as described below.
- Historical obsolete E is reconstructed against retained original semantic bodies;
  retained V fields are checked against the review JSON. Storage-based report
  discovery detects removed metadata tags. Coordinated arbitrary generic rewrites
  are explicitly outside authenticated inspection guarantees.
- Coverage, unknown/resized host delivery and retained next actions remain explicit.
  Complete visual passes require every prepared view at exact delivered dimensions.
  Review timing and viewing are caller declarations; no actual host viewing,
  artistic judgment or engine execution is established by these checks.

## Final gate

PASS on final operation source SHA256
`9d21b30f42d4c0a35eb8c47ce52a67fbc1f6c5ef4ceee63c1f2e6f499e7674d9`.
Read the final implementation report and source after the implementer's ready notice.

Both important findings are corrected:

- The visual observation gate now requires at least one candidate-source view.
  Complete pass coverage remains stricter; partial candidate failure is retained.
  Re-executing the original independent reference-only probe now rejects with
  `inspection_manifest: visual verdict needs observed candidate-source view`.
- Canonical tagged JSON bytes compare original fields, rendering, typed projections,
  coverage and retained E/V fields; retained X and semantic drift compare canonical
  record hashes. The boolean metadata probe now rejects with `typed packet
  projection differs`; an independent rerun of the preserved float-width mutation
  rejects with `rendering manifest differs from exact inputs`.
- The loader additionally validates source options and exact input count before
  capture, and enforces aggregate remaining encoded-byte limits on every retained
  input read. This bounds cold capture before renderer validation.

Final evidence under `evidence/candidate-inspection/`:

- `operation-review-final-tests.txt`: 19/19 inspection and real CLI/MCP operation
  tests pass, including all three finding regressions.
- `operation-review-probes-final.json`: the seven independent timing, observation,
  supersession and post-review-amendment probes pass on the source hash above.
- `reference-only-review-post-fix.txt`, `closed-type-equivalence-post-fix.txt`,
  `float-width-review-post-fix.txt`: preserved independent rejection traces for the
  formerly accepted declarations/artifacts. Nonzero exits are the expected outcome
  of these original success-path repro scripts after correction, not suite failures.

No additional blocking issue was found in publication/history or adapters. This gate
covers local operation behavior and retained integrity, plus discovery/format through
real adapters. It establishes neither production-profile behavior in model scenarios
nor artistic quality, actual host viewing, live provider execution or target-engine
acceptance. Plugin packaging and native task outcomes remain separate root-owned gates.

Additional final bound probe: `aggregate-cold-review-post-fix.json` confirms a 350-byte retained fixture with a patched 349-byte aggregate ceiling rejects during capture, before any renderer call. The source hash matches the final gate above. `float-width-review-post-fix-final.txt` reruns the standalone float-width probe with the same expected strict rejection. All reviewer probe scripts pass Ruff.
