Current allocation/production continuity, cold host findings and A–E answers: [cohesion review](../evidence/plar-cohesion/README.md).

# PLA / PLAR critical review — 2026-11-07

Later allocation/update and selected-request implementation, current A–E answers and actual host findings: [2026-11-08 review](../evidence/plar-allocation/README.md). The review below retains its original dated scope.

The product is a callable specialist that understands a consumer project, creates its pixel-art UI/game assets through the official paid PixelLab API, inspects the result and delivers usable files. The repository has substantial production machinery, but its everyday interface previously began too far down at state records. PLAR supplies the missing project-to-asset requirements operation.

The reviewed behavioral source is [.agents/PROFILE.md](../.agents/PROFILE.md), with the shared [PIXL skill](../plugins/pixl/skills/pixl/SKILL.md), host adapters and runtime. No file named `MIVIM.spec` or profile titled `PIXEL ART ASSET SPECIALIST` exists in this checkout. [TODO.spec.md](../evaluations/TODO.spec.md) uses the MIVIM development-task framing; it is not another production profile.

## A — How can this be improved?

Make the ordinary path visible and callable: consumer project → PLAR → selected asset → PIXL/PixelLab → inspection → integration → updated work list. Preserve advanced evidence machinery, but load it only for the actual operation.

| Finding | Consequence | Implemented response |
| --- | --- | --- |
| No source-to-asset requirements operation | The agent must rediscover consumers and translate scattered context into low-level plans | PLAR skill, versioned ordinary-JSON `plar.txt`, source bindings, coverage boundaries and focused selection |
| Canonical profile moved to `.agents/PROFILE.md`, builders still copied `agent/` | Rebuilding could silently remove the portable profile; wheels could omit it | Explicit source-to-portable mapping, sdist inclusion and installed-byte verification |
| Commit required an encoded temporary file | The recorded Codex specialist could prepare a valid plan but could not save it through its available file tools | Existing commit accepts inline JSON through the same revision/evidence checks |
| Specific artistic failure cases occupied the common entrypoint | Every invocation paid their context cost, even when irrelevant | Preserve the full guidance in a linked artistic-authority reference; keep the general authority rule in the entrypoint |
| Provider boundary wording implied every local tool was state-only | The separately implemented HTTP bridge was obscured | Explicit distinction between local state MCP, authenticated PixelLab MCP and official HTTP bridge |
| Milestone status and missing evidence link were stale | A reader could not tell what either host had actually delivered | Retained trial review and updated task status; new evidence stays separate from previous attempts |

`plar.txt` uses ordinary JSON because the hosts and runtime already exchange it. A second bespoke wire language or a mandatory new orchestration server would add translation work. The source table avoids repeated locators; selecting an asset returns its complete requirements without the full queue. Semantic code understanding remains the host's job, not a regex pretending to discover every visual need.

## B — Is the spec compatible with current Claude and Codex?

Yes in architecture, with the adapter and packaging corrections above. Both platforms support reusable skills with references loaded as needed. Keep the shared skill portable and host-specific delegation/configuration in thin adapters. Codex discovers repository skills under `.agents/skills`; Claude uses its own skill/plugin locations. [Codex skill authoring](https://learn.chatgpt.com/docs/build-skills), [Claude skills](https://code.claude.com/docs/en/skills).

Claude's agent can inherit the parent model and tools; its optional `skills` list preloads whole skill bodies. Codex custom agents use `.codex/agents/*.toml` and inherit the host's tools and permission boundary. A shared Markdown agent file is therefore not a native agent definition for both hosts. This change adds a Codex repository adapter and a portable configuration example while retaining the Claude adapter. Pass the root, asset ID, constraints and reference paths explicitly when delegating. [Claude subagents](https://code.claude.com/docs/en/sub-agents), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

Installed CLIs inspected here: Codex 0.166.0 and Claude Code 2.1.318. The research establishes documented compatibility; actual native delivery is evaluated separately. No global settings or marketplace installation were changed.

## C — Does this best support consistent contextual quality?

It improves the conditions for quality: connect visual purpose to backend states and display size; preserve reference authority; select one coherent contract; inspect actual output before family expansion. It does not establish that this is an optimal architecture or guarantee exact generated art.

PLAR records which requirements are explicit, observed, proposed or unknown. It keeps the actual consumer path, frame geometry, import checks and relevant references in the selected handoff. The production agent must compare the submitted provider arguments with that handoff, then inspect the returned artifact in its use context. PixelLab documents reference-based style matching, but the generated result still needs review. [PixelLab style references](https://www.pixellab.ai/docs/tools/consistent-style).

The existing source corpus, pixel-craft knowledge, animation/tile inspection and rejection history remain useful. Source identity and mechanical validation protect traceability; neither measures silhouette quality, motion readability or style consistency. Broader artistic acceptance remains an empirical production question.

## D — Can the agent understand a supplied workflow and operate from another project?

The instruction path now states both roots explicitly. Installation resources are read relative to the skill; requirements, source bindings, jobs and output files belong to the consumer root. The complete plugin is the portable unit. A standalone copied SKILL.md would omit required runtime resources.

The host reads source/renderer entry points, follows backend-driven visual states, groups shared consumers, and records dynamic or unavailable surfaces as coverage gaps. It does not allocate an image to every function. Existing assets can remain in place; missing assets can be planned before files exist. The selected handoff includes requirements, sources, unresolved questions, dependencies and delivery checks.

[The external queue UI example](../examples/plar-project/README.md) exercises shared consumers, backend transitions, a frame strip, preserved vector art and a remote registry. Runtime tests also exercise drift, stale writes, relocation and installed use. The independent forward evaluation starts from raw source, not the worked inventory. These checks establish bounded operability, not exhaustive discovery on arbitrary repositories.

## E — Where are the pipeline and responsibilities represented?

| Responsibility | Owner and location |
| --- | --- |
| Interpret project intent, code consumers and visual requirements | [PLAR skill](../plugins/pixl/skills/plar/SKILL.md) |
| Work list and next actions | Consumer project's `plar.txt`; [format](../plugins/pixl/skills/plar/references/format.md) |
| Expert art decisions, production sequence, inspection and integration | [Profile](../.agents/PROFILE.md) and [PIXL operation skill](../plugins/pixl/skills/pixl/SKILL.md) |
| Validate requirements, bind sources, select context, retain edits | [PLAR runtime](../pixl/plar.py), CLI and two local MCP tools |
| Persist production jobs, artifacts and evidence | Existing PX2 store and runtime; inline commits simplify input |
| Generate assets | Official authenticated PixelLab API, via exposed MCP tools or the supported HTTP adapter |
| Delegate and supply project context/tools/authorization | Calling Claude or Codex host and its native adapter |
| Prove the asset works in the project | Actual renderer/engine import and host review |

MCP is the callable mechanism; the skill explains how and why to use it. Neither a skill nor an MCP manifest is a new autonomous service by itself. Keep semantic reasoning out of deterministic storage code and provider generation out of the local state server. PixelLab's official API and agent toolkit supply the remote generation surface; inspect current schemas instead of treating the dated capability snapshot as an exhaustive current inventory. [PixelLab API](https://www.pixellab.ai/pixellab-api), [PixelLab agent toolkit](https://www.pixellab.ai/mcp).

## Mechanisms to keep, simplify and leave optional

- **Production core:** intent/reference authority, actual PixelLab operation schemas, durable job identity/recovery, actual artifact import, visual review and destination checks.
- **Simpler front door:** PLAR selected-asset handoff and direct JSON commit. Full-repository allocation is useful for project planning; a precise one-asset brief can proceed directly.
- **Optional reference infrastructure:** representation benchmarks, broad research archives, method POCs irrelevant to the current asset, historical host trials and legacy PX1 compatibility. Keep them available without requiring every task to load or rerun them.

The repository's own [plar.txt](../plar.txt) scopes executable tooling and classifies its art as reference/evaluation material. It does not invent a game UI or queue production replacements for synthetic fixtures.

## Verification and remaining acceptance

See [current PLAR evidence](../evidence/plar-review/README.md), [historical delegated outcomes](../evidence/delegated-asset-request/README.md), and [the full verifier receipt](../evidence/test-results.json). The cross-host milestone is complete only when each parent receives and inspects its delegated asset. A successful process exit, valid plan or passing unit suite alone does not satisfy it.

The November 7 matched trials now satisfy that bounded milestone in both hosts. Codex used four inline JSON commits, and both parents actually viewed and consumed the delivered files. The audit also exposes a quality boundary: the selected requests translated reference features into text instead of sending a reference image. The controlled response cannot measure reference fidelity; choose the appropriate reference-capable PixelLab operation when production depends on visual matching and inspect the actual result.

The follow-on [agent-to-agent development review](AGENT-HANDOFF-REVIEW.md) records the implemented reference roles, complete dependency handoffs and official operation-selection guidance. Its independent planning exercise carries actual source PNG bytes into a reference-capable request; generated fidelity remains a separate production result.
