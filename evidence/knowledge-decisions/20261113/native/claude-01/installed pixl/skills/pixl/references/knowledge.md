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
3. **Load the operational context.** Read the actual UDL specification/registry before interpreting or authoring `.px`. In a consumer-rooted MCP session, call `pixl_context` with `scope: "library"`, `path: "knowledge/library.px"` and `focus: "k.<method-id>"`. This resolves the installed resources even when they are outside the consumer. Optional `result_path: "research/method-context.json"` retains the complete result under the consumer root at a fresh path. CLI callers can use `context knowledge/library.px k.<method-id> --scope library --root <consumer-root>`; complete CLI context emits PIXL wire, while MCP returns a JSON envelope containing `wire`. Existing absolute-library-path CLI calls remain supported in default project scope. Add `--budget BYTES` when needed. Preserve the dependency closure and the **executed receipt's** limitations: the method's suggested POC recipe is not evidence that that recipe ran. A budget failure requires narrowing the operation or using enough context; it does not justify removing required evidence.
4. **Inspect the cited text.** Match the candidate's `{path,start,end}` citations to the discovered source identities. Use `source <absolute-source-path> --expect SHA256 --start N --end N` through the runner. Through MCP, use `pixl_source` with `scope: "library"`, the inventory's relative `path`, the expected hash and the cited line bounds. The default MCP scope remains `project` for the user's own project sources. Inspect any other context source using its actual S-record locator/hash; never infer that an uncataloged file belongs to the supplied corpus.
5. **Assess transfer to this project.** Compare the source conditions with the actual brief and artifacts. State which prerequisites hold, which remain unknown, where the method is unsuitable, and what the reference POC proves. A passing fixture demonstrates its stated reference properties; it does not establish the new asset's quality, current provider support, or engine behavior.
6. **Select the next operation.** If the question is answered by inspected sources, retain the supported conclusion and its limits. If the production use is uncertain, define the smallest representative proof, its observable acceptance criterion, and the affected dependent work. Use the [production procedure](production.md) for that proof and subsequent art work. Discover current remote tools before translating the proposal into a provider request.

The MCP operations `pixl_sources`, `pixl_knowledge`, `pixl_context` and
`pixl_source` accept an optional `result_path` under the consumer root. Use a fresh
path for each observation to retain the actual complete JSON and its returned
SHA-256. The export reply identifies the saved result; open that file to inspect
its full method, wire context or source text before drawing a conclusion. Export
does not convert a lookup into a design decision or artistic acceptance. CLI
retrieval keeps its existing output behavior; complete `context` emits PIXL wire.

## Result and stopping condition

Retain the selected method ID, exact source identities/ranges, the project question, applicability judgment, unresolved prerequisites, relevant receipt limitations, and next proof/action in project-owned context. Use declared PIXL record kinds and fields when updating production state; a proposed method must not be recorded as an adopted, proven decision before its requirements are met. The [PX2 intake/sample operation](intake-sample.md) retains choices, unproven research/sample tasks, planned outputs and acceptance requirements. For PX1 projects, preserve the existing format and do not invent equivalent fields.

This operation is complete when another session can identify the same method and source text, understand why it was selected or rejected, and identify the remaining production-specific proof. Explain the useful conclusion to the user in plain language. Keep hashes and tool details in the retained evidence unless they help the user assess a conflict or failure.

## Connect retrieval to a useful decision

Start with a concrete choice the caller needs to make: for example, whether a
proposed animation import preserves the accepted timing and planted contact.
Retrieve only methods that help answer it. Preserve the assignment's actual
requirements before considering a source example's numbers, geometry or effects.

Keep a short project-owned decision card with the following information. This is
an ordinary research/handoff report, not new PIXL syntax or automatic adoption:

| Information | What to retain |
| --- | --- |
| Question and current authority | The proposed action, actual brief/source/artifact identities and relevant requirements. Distinguish an original expert proposal from a later explicitly adopted assignment instruction. |
| Selected knowledge | Actual method IDs, saved complete contexts, exact source paths/hashes/ranges and executed proof identities. Keep the method's proposed POC separate from its current executed receipt. |
| Applicability | Which prerequisites hold, which remain unknown, and any adaptation or reason to reject the method for this assignment. |
| Decision and alternatives | The specific action to keep, change, reject or defer; the source support, actual observations and specialist judgment behind it. A source example does not set project values. |
| Proof and limits | Exact inspected artifacts or executed checks, what they establish, and what remains untested. An existing successful outcome does not establish that today's retrieval caused it. |
| Next action | A usable instruction or smallest necessary proof, including the affected destination. Preserve accepted work while an alternative remains unqualified. |

For an unequal-duration animation, a useful card can compare the proposed import
against the actual declared boundaries and loop length. A fixed-FPS preview, a
fixture with a stable mask, or valid pivot metadata alone does not prove that the
new destination preserves that animation. Inspect the relevant returned pixels
and destination observations; name the engine check still needed if its result
is unavailable. This example describes a question to investigate, not a rule that
all animations must use unequal durations, fixed bodies or a particular palette.

Keep successful and rejected retrievals and decisions when revising the card.
Reopen the saved card and compare its recommendations with the original brief,
retrieved conditions and actual proof limits before handing it back. A completed
research report does not reopen or rewrite accepted production state. If adopting
a design decision in that state is necessary, use the existing D/I/E semantics
and their real proof bindings through the state-authority operation.

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
| Installed method context is requested through project scope | Use `scope: "library"` with the relative installed resource path. Keep `result_path` in the consumer; do not copy a different library revision into the project as a workaround. |
| Library context is combined with authoring or PLAR selection | Retrieve the complete library context separately. Use project scope for consumer authoring and selected-asset state. |
| A result export path already exists | Read the retained result or choose a fresh path. Do not replace an earlier observation to make a new retrieval look historical. |

Source retrieval is read-only. It performs no generation, provider polling, installation, or project acceptance by itself.
