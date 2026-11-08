# PLAR allocation, updates and first-request preparation

This increment follows the existing consumer fixture from raw source allocation through a source update and a selected asset's first executable request. It implements the PLAR update comparison and one preparation operation; it does not close the overall asset-production milestone. All dated runs below use UTC.

## What changed

- `plar read --since PRIOR_HASH` compares a retained allocation with the current work list, reports changed sources/declarations and transitive dependents, and distinguishes unaffected assets. Save returns the same comparison. This is conservative impact over tracked bindings, not a semantic scan for previously unknown consumers.
- `pixl_plar_prepare` / `plar prepare` consumes the selected requirements identity, exact request/review packet, ordinary-JSON candidate criteria and observed provider connection. It retains inputs, creates the existing PX2 first-candidate plan and prepares a durable job. The agent still chooses the art direction, operation and checks; the caller reviews their meaning.
- Unchanged preparation resumes the existing plan/job. Changed requirements prevent new preparation/dispatch; retained source/request bytes keep existing reports and observations recoverable. Exact request **and complete output/context** must agree before a job can be reused.
- The runtime does not create an image, adopt a style, approve art or rewrite a changed plan. Host execution uses the existing dispatch → actual provider call → observation/import workflow. Later family work and explicit plan amendments retain their existing operations.

[Preparation instructions](../../plugins/pixl/skills/plar/references/prepare.md) · [runtime contract](../../spec/asset-preparation.md) · [master TODO](../../TODO.md).

## Allocation and update coverage

An independent specialist received the existing queue consumer's raw TypeScript, brief, Start SVG and a source map, without the worked inventory. It allocated Ready/Working/Retry, preserved Start and explicitly recorded dynamic badge coverage and the unavailable renderer. Ready became the proposed representative sample; that was an expert choice, not a preapproved art direction.

The isolated source then changed: backend pause → paused, a new Paused visual mapping, Retry moved to `assets/error-retry.png`, and the brief requested a distinct Paused state. The specialist refreshed affected source bindings, kept existing IDs, added Paused, preserved the earlier work list in history and retained the original requirements, including full/compact consumers, animation mapping and 1x/3x nearest review. Independent review verified source identities and the actual old/new files.

The source change affected shared bindings, so this exercise does **not** establish selective unaffected behavior by itself. Its initial evidence/production fields were empty. A separate actual-CLI probe adds a real preparation receipt and production links, then changes only Retry's declaration and scoped source: Working's populated row and prepared state remain byte-identical. The same probe dispatches the exact reviewed arguments, changes source after submission claim, and records an explicitly synthetic observation while preserving the original source bytes.

- [Forward source and refreshed work list](20261108/forward/project/UPDATED-HANDOFF.md).
- [Complete forward archive and manifest](20261108/archives/forward.manifest.json): 37 files, including `.pixl` history otherwise ignored by Git.
- [Local probe result](20261108/local-probe-result.json): seven checks; [retained inputs/output](20261108/archives/local-probe.manifest.json).
- Fresh installed wheel and copied-plugin runs perform the same seven-check probe with production dependencies only.

## Native host observations

Both hosts use their native parent/specialist route, a copied frozen kit and the same updated consumer. The selected assignment is Ready's first request with independent caller review and resumable state. The controlled connection advertises only the exercised subset of `create_image_pro_flash`; it records actual MCP arguments and returns a simulated queued ID. It is not a complete upstream tool declaration or a generated-image service. Official operation semantics were checked against [PixelLab's MCP documentation](https://api.pixellab.ai/mcp/docs).

| Attempt | First-request mechanics | Independent review findings |
| --- | --- | --- |
| Claude 01 | One accepted call, exact reviewed arguments, linked PLAR and submitted job; caller revised a weak criterion before dispatch | Incorrect file-local locators and a misleading suggestion to retrieve the simulated ID from a real provider; final status also confuses completed stage with unfinished asset |
| Codex 01 | One accepted call, exact reviewed arguments, linked PLAR and submitted job | A required sample criterion depends on completing family members that themselves depend on the sample; caller missed the cycle |
| Claude 02 | Passed: one exact reviewed submission, current retained selection, seven source/choice-attributed checks and correct stage status | Locators and provider-ID scope corrected. Future same-output live preparation omits resolution of the retained pending simulated job; isolated replay returns `job_pending` with no writes |
| Codex 02 | Passed: one exact reviewed submission, current retained selection and correctly linked PLAR | Independent review passes the sample criteria and handoff; later family/destination obligations remain scheduled |

The failed first contracts/handoffs remain unchanged in the archives. Claude02 still needs a corrected **future continuation**: its actual proposed same-output reprepare is blocked by the retained submitted job. An isolated-copy probe confirms the rejection and unchanged copy/original state. Resolve the attempt through supported evidence or use a separate actual production assignment/context; do not turn the simulated ID into an upstream job or silently erase it. This finding does not undo its completed first-request stage. General guidance now keeps current-stage checks satisfiable, schedules rather than erases later family obligations, verifies locators within each individual file, and binds remote IDs to their originating provider. Results are judged from the actual packets, state, caller reviews and recorded calls, not process exit or a producer's self-report.

[Independent native review](20261108/native-review.json) · [archives](20261108/archives/) · [same-output continuation probe](20261108/review-findings/20261108T035455Z-results.json).

## Defects found and corrected

Independent review exercised the operation rather than just reading it. The preserved [development probes](20261108/review-findings/) found five issues: binary references used text line ranges; a different request could reuse a named job; edited consumer sources prevented recovery; a partial-output job could be reused; and generic state publication bypassed the new selection check. All five were corrected and re-exercised. The final independent preparation/job/history run passed 62 tests. Retained probes record their inputs/results; the development runtime was not frozen at every intermediate probe, so the archives do not claim that each failed implementation is independently replayable.

The first full verifier reached distribution and failed because the wheel omitted `asset-plan.schema.json`. Its [failed receipt](../verification-runs/20261108T033740.731893Z/result.json) is preserved. Package data now includes that schema; the [corrected full run](../verification-runs/20261108T034254.703857Z/result.json) passes **480 tests, one Windows symlink-privilege skip and 39 reference checks**, including clean wheel/copied-plugin use. This increment adds 21 regressions (3 allocation/update, 17 preparation, 1 request-fixture). Maintained source/generated Ruff and runtime/evaluation/script Mypy pass. Both skill validators pass.

[Checks and identities](checks.json) records the final distribution and archive verification. No fixture call, dimensions check or valid state establishes generated-art quality or consumer renderer acceptance.

## Required A–E review

**A — Improvement.** Allocation now exposes meaningful tracked change impact and a selected reviewed asset reaches a durable first request without handwritten PX2 setup. Independent review exposed real reuse/recovery defects and a stage-dependency planning error. Existing advanced operations remain useful for amendments, adoption, families and recovery. The next useful improvement is a contract-change continuation that preserves the old submission while making a newly reviewed plan actionable.

**B — Host compatibility.** Native Claude Code 2.1.318 and Codex CLI 0.166.0 load the shared skill through their native specialist routes and use local MCP plus the controlled provider connection. Exact frozen inputs and calls show bounded compatibility on these installed versions. The skills keep reasoning in the agent and deterministic operations in tools; the host owns authenticated PixelLab access. This does not establish every host version, installation mode or documented provider operation.

**C — Contextual and artistic quality.** Focused PLAR context includes transitive dependencies and exact reference/source identities. The caller compares actual arguments and every rejecting criterion against original sources. Required outcomes, scoped sample choices and later family checks remain distinct. Hashes and conservative impact protect identity, not artistic judgment; the native failures show why independent semantic review is still needed. Pixel-art quality requires actual generated candidates and their review.

**D — Understanding another project.** The independent raw-source allocation consumed a source map, traced backend transitions to two shared consumers, preserved existing art, and maintained the inventory after an actual source change. Installed/copy probes run from separate consumer roots. Dynamic registry data and a missing renderer remain explicit gaps. New/untracked consumers still require agent inspection; no file-hash operation claims exhaustive repository coverage.

**E — Responsibilities.** The canonical profile supplies visual expertise. PLAR's skill owns source interpretation, allocation and maintenance; PIXL's skill owns creative planning, request review, provider execution and acceptance. `plar.txt` is the consumer's work list. Local `pixl_plar_read/save/prepare` and existing job tools preserve validated state. The official PixelLab connection performs generation, and host/caller viewing plus the actual renderer establish the relevant quality/integration judgments. Optional proof and research infrastructure stay available behind the operations that need them.

## Reproduce the native request case

Build the current kit, then use a new output directory for each attempt:

```text
python scripts/build_plugin.py
python -m evaluations.request_review_trials --host claude --case plar-start --out NEW_CLAUDE_ATTEMPT --run
python -m evaluations.request_review_trials --host codex --case plar-start --out NEW_CODEX_ATTEMPT --run
```

The runner freezes instructions and raw inputs, exposes the controlled request connection, and retains actual native transcripts and artifacts. A completed process is explicitly ungraded until those outputs receive independent review. Never overwrite a retained attempt. The worked allocation/refresh input is preserved in this evidence tree and its archive.

## Next work and limits

This increment verifies allocation/update mechanisms and the selected first-request path on the existing fixtures. PX-PLAR-002 remains open for complete real-consumer coverage/integration; PX-EVAL-005 retains earlier full-delivery findings; PX-PROD-001 still requires useful real-provider art and destination acceptance. Continue with a changed-contract cold handoff on the existing submitted fixture, then carry selected work through retrieval, sample adoption, family review and destination use. Another user repository or commission is not a prerequisite for that development.
