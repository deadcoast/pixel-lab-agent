# Packaged PIXL Host Evaluation Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development for the bounded host discovery and evidence review tasks. Preserve the authorized development workspace and all earlier evidence.

**Goal:** Observe the packaged PIXL profile in both hosts and distinguish host execution, instruction following and actual production outcomes.

**Architecture:** A local evaluation runner freezes inputs, launches a native host in a separate project, retains structured events and copies resulting files into an immutable attempt directory. Criterion reviews cite those records and never infer behavioral passes from process completion.

**Tech Stack:** Existing uv environment, Python standard library and Pillow, installed Codex and Claude Code, packaged PIXL MCP.

**Spec:** `docs/superpowers/specs/2026-09-11-host-evaluation-design.md`

## Global constraints

- Do not activate PIXL in the maintainer session.
- Preserve the existing dirty tree and earlier evidence; do not rebuild the runtime bundle.
- Use native host skill loading and the exact copied package; record adapter limitations.
- Do not copy credentials, change global host configuration, or contact PixelLab.
- Keep authentication errors, incomplete trials and every applicable unverified criterion.
- A controlled image fixture is not a production result.

## Task 1: Native loading and input preparation

Files: `evaluations/host_trials.py`, `evaluations/fixtures/`, `evidence/host-evaluation/discovery/`.

- [x] Verify installed CLI configuration/discovery without reading secret values.
- [x] Create fixed image inputs and an evaluator-only expected-difference description.
- [x] Freeze bundle and scenario identities; copy inputs into an isolated project.
- [x] Retain exact native host arguments and session configuration.

## Task 2: Recorded trials

Files: `evaluations/host_trials.py`, `evidence/host-evaluation/runs/`.

- [x] Record native structured stdout, stderr, return status and all artifact hashes.
- [x] Run the supported initial cases and repeat selected prompts in fresh sessions.
- [x] Recheck Claude after the requested interactive login; record a concrete failed native attempt if it remains unavailable.
- [x] Run a cold continuation using persisted state when the prior trial provides it.
- [x] Validate evidence integrity and failure classification with focused tests.

## Task 3: Criterion review and next targets

Files: `evaluations/README.md`, `evaluations/TODO.spec.md`, `evidence/host-evaluation/report.json`, `docs/VERIFICATION.md`, `docs/AGENT-KIT.md`.

- [x] Review each attempted case's complete criteria, citing events and output files.
- [x] Check findings independently and retain disagreements or limitations.
- [x] Report coverage by host, loading, behavior and production outcomes.
- [x] Record the next actionable tasks in MIVIM `.spec` style, with inputs, operation, proof and stopping condition.
- [x] Run focused validation and verify the evaluated package still matches the frozen identity.

## Execution ledger

- The user explicitly selected this milestone and authorized continued development.
  Proceed without a redundant design approval pause. This is the governing ruling
  over generic brainstorming/plan handoff gates.
- Work remains on `develop/pixl-source-provenance`; a clean worktree would omit the
  accumulated authorized milestones. Only the host trial projects are isolated.
- Codex 0.154.0 reports an authenticated ChatGPT session. Claude Code 2.1.263 reports
  expired authentication. The user was asked to run `claude auth login` while
  independent work continues. No authentication result is a profile score.
- Task interfaces: discovery supplies native loading/configuration to the runner;
  the runner supplies immutable attempts to the reviewer; the reviewer supplies
  observed findings to the TODO. The runtime and packaged instructions are inputs
  shared by all tasks and remain unchanged during this evaluation.

## Initial baseline ledger (preserved)

- Seven actual Codex sessions completed across five catalog cases, one visual repeat and one supplementary cold intake. Claude native loading succeeded but expired OAuth blocked inference; the sanitized final auth recheck still reports logged out.
- Independent criterion review retained 16 pass and 6 unverified catalog criteria, plus 4 passing supplementary cold checks. Native image payloads in the repeated visual journal matched actual retained pixels; the first ephemeral visual trial remains unverified for that viewing criterion.
- All eight attempt inventories and six saved states replayed successfully (18 local operations). Seven focused recorder tests, Ruff and Mypy over all three evaluation scripts pass. No runtime, profile, bundled source, earlier receipt or production asset was changed.
- Recorder findings and failed probes were preserved before correction: verify-only predecessor copying; tolerate scalar JSON events; retain mutated package bytes. Later native journal retention addresses the exec stream observation gap.
- Next evaluation action is PX-EVAL-002 after Claude login. Next independently ready implementation is PX-OPS-001, candidate inspection with retained review evidence.

## Outstanding stage-5 acceptance

- [x] Complete the bounded matched Claude comparison after authentication is restored, retaining interrupted attempts and failed criteria.
- [ ] Execute the six remaining catalog scenarios and a separately specified real-production outcome.

The evaluation foundation is implemented. The bounded matched comparison is recorded
below; stage 5's broader scenario coverage and actual production acceptance remain open.

## Claude continuation after restored authentication

- The user restored Claude authentication. Sanitized status now reports logged in via claude.ai; old auth failures and the seven-file Codex baseline report set are preserved under `evidence/host-evaluation/previous/codex-baseline/`.
- Execute the unchanged five-case prompts, repeat the visual case, and cold-resume Claude's own intake using verified predecessor files. The package remains frozen; no new PixelLab or engine operation is authorized by these local evaluation prompts.
- Separate invalid model-authored state from corrupted evaluation evidence. A faithfully captured failed state operation is an observed outcome, not grounds to discard the trial. The compiler is being updated to derive host comparison status and outcomes from retained records and criterion reviews rather than the earlier blocked-Claude baseline.
- Ruling: repeat Codex missing-provider with the same prompt/package/model and working file access, retaining the native journal. The original constrained run could not publish typed local plans; comparing it directly to an unrestricted Claude trial would confuse host access with profile behavior. Retain both attempts and label their configuration difference.

## Authenticated comparison ledger

- Sixteen attempts are retained: eight completed Codex turns, four completed Claude
  turns, three Claude interruptions at 600 seconds and the original pre-inference
  authentication failure. Both hosts have observed behavior on five catalog cases;
  only maintainer routing and visual rejection have completed fresh turns in both.
- Independent review retains 33 passing, 2 failing and 9 unverified catalog criteria,
  plus eight passing supplementary cold checks. All original review entries remain
  unchanged. Claude's style plan overrides requested selective AA; other judgments
  add unsupported requirements. Those defects remain visible beside correct rejection.
- Cold Codex intake leaves its revision 2 unchanged. Cold Claude intake resumes the
  interrupted revision 1, completes its study review at revision 2 and asks consequential
  choices. It still repeats an unsupported outline/canvas threshold; recovery is not
  proof that inherited artistic reasoning is correct.
- All sixteen inventories and thirteen store heads pass replay: 39 local operations.
  Eighteen recorder/report tests, Ruff and Mypy pass. The compiler derives host-specific
  inference, completion, exact input pairing, usage and configuration differences.
- Independent checker review found that an unrecorded file could influence replay.
  The failing regression and prior checker are retained; exact project inventory
  equality now blocks replay. Independent re-review closed the finding. Actual trial
  inventories were intact both before and after correction.
- The frozen package's 92 files, profile/runtime sources and prior raw attempts remain
  unchanged. No provider generation, commissioned art or engine acceptance occurred.
- PX-EVAL-002 is complete for this bounded matrix. PX-OPS-001 is the next implementation
  target, with native/cropped viewing and truthful observation order. PX-SKILL-002 records
  the observed failures of project-specific artistic authority; the remaining six cases
  and real production outcomes remain in PX-EVAL-003.
