# Research a production method from supplied sources

Use this operation when a brief, artifact defect, or technical uncertainty requires selecting or checking a pixel-art method. Its result is a source-grounded candidate method and a specific next proof or production action. The [profile](../../../resources/agent/PROFILE.md) governs artistic judgment and authority.

PIXL already brings pixel-art judgment through the host model and this specialist
profile. The curated library extends and grounds that expertise; it is not the only
permitted source of reasoning, and this research operation is not a prerequisite for
every visual choice. Use available harness tools to test a consequential uncertainty.
Attribute familiar expert choices to your judgment and scope them to the candidate;
when you claim a supplied method supports a decision, retrieve its actual conditions.
Official provider documentation establishes tool capabilities, not the owner's style.

## Entry and required context

Identify the question the method must answer, the relevant project references or inspected artifact, and the applicable constraints. Keep the user's requirements, visual observations, proposals, and unresolved choices distinct. For example, a tile-corner defect calls for topology and neighborhood checks; it does not justify importing an unrelated palette policy.

Choose the source location deliberately. In a source checkout, use the current repository resources. For an installed plugin, resolve the bundled runner and resources from this skill's installation. A copied old bundle is a separate revision; do not use it to silently replace missing current source files.

## Procedure

1. **Discover the source revisions.** Run `sources` through the selected runner, or call the discovered local `pixl_sources` tool. In the checkout, `python -m pixl sources --root .` selects the current tree explicitly. The result contains the resource root and each supplied source's stable ID, path, SHA-256 and line count. `previous` is historical provenance, never a fallback location or permission to reuse an old receipt. `files_verified` means the local bytes match the declared inventory; it does not verify external claims.
2. **Select relevant knowledge.** Use `knowledge` to inspect the method index and `knowledge METHOD_ID` to inspect the candidate's applicability, prerequisites, procedure, checks, pitfalls and citations. Choose from the actual result rather than inventing a method ID. Leave unrelated methods out of the working context.
3. **Load the operational context.** Read the actual UDL specification/registry before interpreting or authoring `.px`. Run `context <resource-root>/knowledge/library.px k.<method-id> --root <resource-root>` through the selected runner. Add `--budget BYTES` when needed. Preserve the dependency closure and the proof receipt's limitations. A budget failure requires narrowing the operation or using enough context; it does not justify removing required evidence.
4. **Inspect the cited text.** Match the candidate's `{path,start,end}` citations to the discovered source identities. Use `source <absolute-source-path> --expect SHA256 --start N --end N` through the runner. Through MCP, use `pixl_source` with `scope: "library"`, the inventory's relative `path`, the expected hash and the cited line bounds. The default MCP scope remains `project` for the user's own project sources. Inspect any other context source using its actual S-record locator/hash; never infer that an uncataloged file belongs to the supplied corpus.
5. **Assess transfer to this project.** Compare the source conditions with the actual brief and artifacts. State which prerequisites hold, which remain unknown, where the method is unsuitable, and what the reference POC proves. A passing fixture demonstrates its stated reference properties; it does not establish the new asset's quality, current provider support, or engine behavior.
6. **Select the next operation.** If the question is answered by inspected sources, retain the supported conclusion and its limits. If the production use is uncertain, define the smallest representative proof, its observable acceptance criterion, and the affected dependent work. Use the [production procedure](production.md) for that proof and subsequent art work. Discover current remote tools before translating the proposal into a provider request.

## Result and stopping condition

Retain the selected method ID, exact source identities/ranges, the project question, applicability judgment, unresolved prerequisites, relevant receipt limitations, and next proof/action in project-owned context. Use declared PIXL record kinds and fields when updating production state; a proposed method must not be recorded as an adopted, proven decision before its requirements are met. The [PX2 intake/sample operation](intake-sample.md) retains choices, unproven research/sample tasks, planned outputs and acceptance requirements. For PX1 projects, preserve the existing format and do not invent equivalent fields.

This operation is complete when another session can identify the same method and source text, understand why it was selected or rejected, and identify the remaining production-specific proof. Explain the useful conclusion to the user in plain language. Keep hashes and tool details in the retained evidence unless they help the user assess a conflict or failure.

After saving imported library S records in the consumer project, use [library-source retention](library-retention.md) to preserve their exact bytes before replacing the kit. It leaves record and receipt identities unchanged. During a cold resume, inspect any reported retained revision before treating old proof as evidence for new work.

## Failures and recovery

| Observation | Required response |
| --- | --- |
| Discovery reports a missing inventory/source or an inventory hash/line-count mismatch | Preserve the diagnostic and stop dependent adoption. In a development task, repair provenance deliberately; in a production task, report the unusable installation/source and continue unrelated work. |
| Exact retrieval rejects a stale expected hash, but fresh source discovery validates the installed revision | Retain the rejected attempt. Re-read the current method and its context, then retrieve its current citation with the matching inventory identity. Never carry an old revision's line range into a new file merely by replacing the hash. If discovery also fails, use the installation-conflict response above. |
| Citation outside the declared source or range | Do not guess a replacement paragraph. Check the actual method/source revision and correct the citation through an explicit source review. |
| Source budget exceeded | Narrow to a meaningful cited section or increase the explicit budget; do not present a truncated result as the complete citation. |
| Stale compiled context or proof receipt | Do not recompute hashes on the old receipt. Re-execute applicable checks and compile updated evidence through the development workflow. |
| Local research contains historical citation tokens or unsupported attribution | Retain its stated status. Verify consequential external claims against retrievable primary sources before using them as current facts. |
| Method requires unavailable tooling or engine access | Keep the method as researched knowledge and name the missing proof. A fixture or prepared request cannot stand in for the unavailable operation. |

Source retrieval is read-only. It performs no generation, provider polling, installation, or project acceptance by itself.
