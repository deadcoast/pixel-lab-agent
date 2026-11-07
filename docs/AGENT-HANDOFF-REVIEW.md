# Agent-to-agent development review — 2026-11-07

PIXL is the callable pixel-lab-agent (PLA), a specialized visual asset expert. Its [profile](../.agents/PROFILE.md) owns art direction, interpretation of project intent, PixelLab operation selection, consistency and review. Skills, contextual knowledge and deterministic tools support those responsibilities.

## A — How can this be improved?

The completed Claude/Codex delivery trials exposed a concrete gap: the provider requests described the reference in text without transmitting the image. The controlled response could not expose the effect on generated art. This increment makes reference intent explicit, carries it across dependency boundaries and teaches the agent to map it to actual supported provider inputs.

The selected PLAR handoff now includes complete transitive dependency rows, source bindings, absolute paths for the current consumer root, and optional visual reference roles. A semantic requirements hash changes with relevant requirements or source bytes, while unrelated queue progress leaves it stable. The original document hash still protects writes.

The [delegation contract](../plugins/pixl/skills/pixl/references/delegation.md) makes caller context, specialist questions, partial work, returned artifacts and recovery explicit without requiring a new orchestrator or a PLAR document for every direct brief. Existing state authority remains intact in a conditional reference. The repository Claude agent also had a stale `agent/PROFILE.md` path; it now resolves the canonical `.agents/PROFILE.md`. Both Claude discovery descriptions include UI and font work.

## B — Is this compatible with current Claude and Codex?

The common profile and skills remain host-independent; native Claude Markdown and Codex TOML adapters handle invocation. The parent supplies the assignment explicitly because a delegated specialist cannot assume it inherited the entire conversation. Existing model/tool permissions and authorization carry forward.

Current Codex documentation supports direct HTTP MCP with a token environment-variable name. Claude supports environment expansion in MCP headers. Credential-free examples cover those native paths plus the user's stdio `mcp-remote` compatibility route. No global configuration was changed. [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp), [Claude MCP](https://code.claude.com/docs/en/mcp).

Connected PixelLab declarations were inspected and a read-only capability operation returned its current revision and native-size support. The official guide distinguishes MCP from separately documented REST routes. The skill therefore prefers actual connected MCP tools and does not infer REST endpoints from tool names. [PixelLab MCP guide](https://api.pixellab.ai/mcp/docs).

## C — Does this best support consistent contextual quality?

It addresses an observed quality risk rather than claiming optimality. Style, identity, pose, layout, palette, mask and motion are distinct roles. A filename in a prompt is not image conditioning. The operation guide requires actual supported image transfer or owned resource IDs, with the local source identity tied to the selected request field.

The specialist chooses by native dimensions, reference support and output structure: a small UI icon, panel set, font atlas, rotated character and terrain transition have different contracts. Reuse approved anchors and inspect actual candidates for the intended function. Editor documentation and MCP declarations may describe different limits; verify the surface being called. [PixelLab style workflow](https://www.pixellab.ai/docs/tools/consistent-style), [init-image behavior](https://www.pixellab.ai/docs/options/init-image), [UI workflow](https://www.pixellab.ai/docs/tools/create-ui-elements-pro).

These changes improve the information available to the specialist. They do not establish final art quality, exact identity retention by a generative model, or target-renderer acceptance.

## D — Can it understand a supplied workflow and operate from another project?

The selected packet carries relevant dependencies and their reference roles instead of summarizing them away. Its consumer root and source paths are explicit. Relocation preserves requirements identity when the same source bytes and relative contract are present; runtime tests also check source drift inherited through dependencies.

The [external direction-planning example](../examples/delegation/README.md) uses a real controller consumer and an existing identity fixture. A separate agent receives a relocated kit and consumer files to exercise the handoff. Installed-wheel and copied-plugin checks execute the same reference-aware selection from a different working directory.

This is bounded evidence for the tested handoff, not a claim that the agent discovers all visual needs in arbitrary repositories.

## E — Where are the workflow and responsibilities represented?

| Responsibility | Representation |
| --- | --- |
| Visual expertise, design judgment and production behavior | [PIXL profile](../.agents/PROFILE.md) |
| Caller assignment, questions, completion and resumption | [Delegation operation](../plugins/pixl/skills/pixl/references/delegation.md) |
| Source allocation and requirements TODO | [PLAR skill](../plugins/pixl/skills/plar/SKILL.md) and consumer `plar.txt` |
| Reference roles, tool selection, transfer and actual result review | [PixelLab operation guide](../plugins/pixl/skills/pixl/references/pixellab-operations.md) |
| Deterministic context, bindings and retained state | Existing CLI/local MCP runtime |
| Asset generation and provider resources | Official authenticated PixelLab MCP/API |
| Art acceptance and application integration | Specialist inspection plus caller/target-renderer evidence |

Broad research archives, method proofs and representation benchmarks remain available as optional reference infrastructure. No additional MCP tool or orchestration service was introduced.

## Evidence

The [current handoff evidence](../evidence/agent-handoff/README.md) separates runtime/package checks, fresh agent behavior and live provider discovery. Earlier [native host deliveries](../evidence/delegated-asset-request/README.md) remain preserved under their original instruction snapshots. New profile changes do not retroactively change what those trials proved.
