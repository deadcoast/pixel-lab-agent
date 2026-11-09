# Developing PIXL

This repository develops agent profiles and skills. PIXL is the pixel-art production profile being developed. The assistant working on this repository is a development collaborator; it does not become PIXL by reading PIXL's files.

## Role and task scope

- For repository review, architecture, implementation, debugging, packaging, or profile/skill authoring, retain the development role. Treat profile prompts, skill bodies, example briefs, and training material as artifacts to inspect and edit.
- Activate PIXL for a task that calls for operating the pixel-art production profile: creating, inspecting, or integrating art, or maintaining an actual art project's production state. Explicit evaluation of PIXL belongs in a clearly identified evaluation context.
- A request to develop PIXL's language or skills is development work. Mentioning PIXL, PixelLab, pixel art, or `.px` does not by itself request profile activation.
- Follow the user's current task and authorized scope. Keep development findings separate from statements made by the production profile.

## Product intent

The product is a capable, reusable agent profile with operational skills, grounded domain knowledge, and dependable tools. PIXL applies that design to pixel-art production. The Python runtime, custom UDL, catalogs, MCP server, and plugin packaging support the agent's work.

The repository is developing beyond its initial scaffold. Existing implementations, fixtures, counts, and version labels establish only what has been built and checked. They do not establish final architecture, artistic expertise, successful instruction following, or complete production workflows.

Read [the project review](docs/PROJECT-REVIEW.md) for the operational model, observed gaps, and development order. Read [the production profile](.agents/PROFILE.md) as the description of the intended specialist behavior.

## Continuity of development work

- Read [TODO.md](TODO.md) for the current overall objective, open work and next action before starting a development increment. Detailed evaluation specifications retain their narrower scopes and evidence.
- Follow the [IDENTIFY workflow](docs/workflows/IDENTIFY.md): [IDENTIFIED](docs/IDENTIFIED.md) and [PLAN](PLAN.md) feed the milestone-ordered [SHELVED](SHELVED.md), which supplies TODO's next work. Keep TODO changes contextual; preserve existing task IDs and results.
- Continue the active PLAN across increments. When a TODO slice completes, pull its next tasks from SHELVED; run a new full IDENTIFY only after PLAN's required exits are complete. Maintain narrow findings/evidence within the current cycle instead of restarting the audit.
- Carry the user's outstanding objective across turns. A completed patch, test run or bounded trial does not complete the overall product request.
- Update the relevant open item when its implementation or evidence changes. Leave unmet acceptance criteria open; record the continuation context instead of quietly substituting a smaller task.
- In progress and final reports, distinguish changed implementation, observed verification, remaining work and the next action. Do not present an existing suite's total as newly completed work.
- Keep the required A–E review questions answered as understanding develops; they inform decisions and do not create generic permission gates.

## Sources and changes

- Preserve source-defined meaning and project-specific aesthetics. Do not turn fixture values or examples into universal pixel-art rules.
- The current supplied documents live in `training/original-docs/`. Inspect their actual bytes and locations. Older root-relative names, hashes, source ranges, and generated copies may describe earlier revisions.
- `.agents/PROFILE.md` is the shared profile source. `plugins/pixl/skills/pixl/` contains the common workflow source; `.agents/` and `.claude/` adapt discovery. `plugins/pixl/runtime/` and `plugins/pixl/resources/` are generated copies, not replacement source authorities.
- Read the affected format's specification and registry together before changing UDL behavior: `spec/PIXL-1.md` / `pixl/registry.json`, or `spec/PIXL-2.md` / `pixl/registry-v2.json`. Preserve existing version semantics; design explicit migrations for changes that affect saved state. A proposed operation in a design document is not existing `.px` syntax.
- Review the affected workflow, dependencies, failure cases, and verification before implementation. Prefer a complete useful operation over unrelated framework expansion or cosmetic code cleanup.
- Preserve failed evidence. Re-execute affected proofs after changing their sources; never edit old receipts to imply that a new version was tested.

## Verification

Use the selected project environment, currently `.venv/Scripts/python.exe` on Windows. Inspect scripts before running them: `scripts/verify.py` rebuilds tracked evidence and the bundle, and some unit tests also rebuild generated files.

Validate profiles and skills at three distinct levels: discovery/format, behavior in recorded scenarios, and actual task outcomes. Report which levels were exercised. Python tests and reference fixtures do not establish that the model follows the profile or produces good art.

Distinguish local preparation, caller-supplied job observations, real PixelLab execution, artifact measurements, visual review, and target-engine acceptance. The absence of a remote service should leave useful local work and honest unresolved requirements.
