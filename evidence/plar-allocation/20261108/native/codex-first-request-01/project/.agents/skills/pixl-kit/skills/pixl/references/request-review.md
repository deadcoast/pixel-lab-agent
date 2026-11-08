# Request and criteria handoff

Use for delegated asset work when a proposed production contract is ready to adopt, or when its consequential request/criteria change. The specialist prepares the contract; the calling agent independently compares its actual contents to the original assignment. This is an agent-to-agent review, not a new user-approval gate. Continue under established authorization when the contract is consistent.

## Specialist: return the exact proposed contract

Save a compact `request-review.json` in the consumer project. Point to existing artifacts instead of duplicating provider history or manufacturing PX2 state for a planning-only task. Its fields are:

- `version`: 1.
- `sources`: the brief and relevant consumer/reference sources, each with project-relative `path`, actual byte `sha256`, and `role`; include locators for the adopted decisions. Include the selected `requirements_hash` when PLAR supplied one.
- `request`: `path`, `sha256`, `kind` (`provider_arguments` or `creative_brief`) and the actual tool name when known. Provider arguments must be the complete exact JSON to dispatch, including real reference inputs. Use a creative brief when an operation/schema has not been discovered; do not label it executable.
- `criteria`: `path` and `sha256` for the exact criteria to use. Each criterion has an ID, check, authority/basis, applicable scope and source locator. Distinguish owner/consumer requirements, specialist sample choices, observations and diagnostics.
- `choices`: the consequential specialist choices or unresolved decisions, where each appears in the request/criteria, and its reason. A criterion scoped to a chosen sample can assess that sample; it does not establish a universal project requirement.
- `resume`: existing store/task/output/job links when applicable. Omit absent production state.

Return the packet's path and SHA-256 to the caller. For PX2 production, link the saved request and Q records or an exact exported view with their state/record identity. Do not silently rebuild the request after review. Before dispatch, compare the actual arguments to the reviewed request; reference bytes/handles and non-text controls matter as much as prompt wording.

Keep a required outcome separate from the recipe proposed to achieve it. A qualitative requirement such as matching a reference or conveying a state still needs an acceptance criterion when its palette, geometry, frame count or layout are open. When demoting an unsupported recipe to a sample choice, preserve the underlying required outcome; do not leave only mechanical checks binding. Consumer code establishes its actual data/rendering behavior, not an unmeasured aesthetic quality. Attribute expert quality criteria to expert judgment where that is their basis.

Creative decisions within the assignment need not all go back to the user. For example, choosing a static first sample or a construction method is expert judgment; attributing it to an owner who specified only canvas dimensions is incorrect. Keep the choice explicit and scoped so it can be revised without changing the owner's brief. Observations alone do not become rejection rules.

### Measured facts in creative requests

Do not estimate pixel coordinates by eye and then describe them as verified. When a numerical image fact materially guides a request or verdict, retain the measurement with its source-image hash, frame and coordinate convention. The existing `asset-check --regions COLOR...` / `pixl_asset_check(regions=[...])` measures exact RGBA component boxes; it does not identify the subject or make those colors mandatory. Boxes use zero-based coordinates with exclusive right/bottom edges. For other measurements, save the reproducible calculation. When exact coordinates are unnecessary, describe the visual relationship and supply the actual reference instead.

The caller independently verifies consequential measured claims against the original image and measurement, including the coordinate convention; repeating a specialist's pixel map is not independent verification. Correct unsupported numbers before dispatch while preserving the required visual outcome.

## Caller: inspect before adopting

Open the packet and verify its hashes. Read the original brief, relevant sources, complete request and complete criteria, not just the specialist's summary or self-audit. Check:

1. Every explicit requirement survives into the request and relevant checks, including qualitative identity/style/state outcomes, actual reference role/input and consumer mapping. Check for dropped or weakened outcomes as well as added restrictions.
2. Every consequential extra restriction has its true basis and scope. Test whether a brief-conforming alternative would be rejected only because an observation or proposal was promoted to an owner requirement.
3. The proposed operation's actual declaration supports the payload. Do not infer a provider parameter, frame/direction count, alpha policy or camera from prose alone.
4. Findings concern these exact artifacts. Mechanical/hash validity and a specialist's consistency claim do not prove semantic agreement or artistic quality.

For each criterion that can reject a candidate, retain a short caller-side comparison: criterion ID, the exact relevant source wording/locator (or explicit expert-choice basis), what the criterion adds or omits, and the finding. Group genuinely identical rules, but cover every rejection rule; a global "all restrictions come from the brief" claim is not this comparison. If a derived rule is stricter than the source, consider a source-conforming result it would reject before adopting it.

Keep process requirements, output requirements and diagnostic proxies distinct. A required production route is checked through actual calls and downloaded-byte provenance; a property of the resulting image is evidence only when it establishes that claim. Do not silently turn a process restriction into an extra output-difference test, or a diagnostic into a rejection rule. Independent review uses the original source, not another agent's assertion that the rule is sourced.

Save a concise `caller-review.json` (or equivalent named fields) with reviewer role, reviewed packet hash, `consistent` / `changes_requested` / `needs_input`, per-criterion comparisons and other findings tied to request locations and source evidence, and the next action. `consistent` means the planned contract matches this assignment; it is not provider execution or asset acceptance.

If changes are needed, send the specialist the precise discrepancy and relevant source; preserve the original artifacts, revise only the affected contract, and inspect the returned new packet. Reuse the existing specialist when the host supports it. Resolve supplied facts yourself; ask the user only a consequential decision genuinely missing from the available context. No token, secret header or credential belongs in either file.

If no independent caller/reviewer exists, retain the specialist's own review as self-review, proceed within existing authorization, and report the independent comparison as unperformed. Do not invent another agent or stop ordinary direct work solely to satisfy this procedure.

## Carry the comparison through production

Return `request_review` in the normal result, containing the packet and caller-review paths/hashes and unresolved findings. After preparing the durable provider job, verify its actual request still matches the reviewed arguments. A changed requirement, criterion or request needs a new comparison; polling progress and unrelated queue changes do not.

The final caller opens the delivered assets, checks the actual request and output against this contract, and records its own observations. Keep contract consistency, provider outcome, visual quality and destination acceptance separate. For a rejected candidate, retain the failure and the revised request/criteria; changing a checker merely to pass the candidate is a contract change, not an asset correction.
