# Request and criteria handoff

Use for delegated asset work when a proposed production contract is ready to adopt, or when its consequential request/criteria change. The specialist prepares the contract; the calling agent independently compares its actual contents to the original assignment. This is an agent-to-agent review, not a new user-approval gate. Continue under established authorization when the contract is consistent.

## Specialist: return the exact proposed contract

Use the focused authoring context described in [family delivery](family-delivery.md)
to locate current records before exploring histories. Keep a proposal's shared
source index once and reference its entries from individual clauses; preserve each
clause's authority, scope and exact locator. Do not duplicate whole reports in
every criterion, abbreviate literal checks into a group summary, or treat the
index's source class as requirement authority. Read the original source text for
the comparison; retrieve a complete record/history only where it bears on the
decision. Exact connected review remains the handoff for adoption.

For a connected family/stage plan, use the adapter's returned `request_review`
arguments and retain that exact report as described in
[the connected handoff](#connected-family-and-stage-handoff). It supplies the saved
criteria and request evidence without manually rebuilding a candidate packet.

For other contracts, save a compact `request-review.json` in the consumer project. Point to existing artifacts instead of duplicating provider history or manufacturing PX2 state for a planning-only task. Its fields are:

- `version`: 1.
- `sources`: the brief and relevant consumer/reference sources, each with project-relative `path`, actual byte `sha256`, and `role`; include locators for the adopted decisions. Numbered locators refer to that individual file, never a concatenated multi-file terminal display. The caller verifies the cited content at those locators. Include the selected `requirements_hash` when PLAR supplied one.
- `request`: `path`, `sha256`, `kind` (`provider_arguments` or `creative_brief`) and the actual tool name when known. Provider arguments must be the complete exact JSON to dispatch, including real reference inputs. Use a creative brief when an operation/schema has not been discovered; do not label it executable.
- `criteria`: `path` and `sha256` for the exact criteria to use. Each criterion has an ID, check, authority/basis, applicable scope and source locator. Distinguish owner/consumer requirements, specialist sample choices, observations and diagnostics.
- `choices`: the consequential specialist choices or unresolved decisions, where each appears in the request/criteria, and its reason. A criterion scoped to a chosen sample can assess that sample; it does not establish a universal project requirement.
- `resume`: existing store/task/output/job links when applicable. Omit absent production state.

Return the packet's path and SHA-256 to the caller. For PX2 production, link the saved request and Q records or an exact exported view with their state/record identity. Do not silently rebuild the request after review. Before dispatch, compare the actual arguments to the reviewed request; reference bytes/handles and non-text controls matter as much as prompt wording.

Keep a required outcome separate from the recipe proposed to achieve it. A qualitative requirement such as matching a reference or conveying a state still needs an acceptance criterion when its palette, geometry, frame count or layout are open. When demoting an unsupported recipe to a sample choice, preserve the underlying required outcome; do not leave only mechanical checks binding. Consumer code establishes its actual data/rendering behavior, not an unmeasured aesthetic quality. Attribute expert quality criteria to expert judgment where that is their basis.

Creative decisions within the assignment need not all go back to the user. For example, choosing a static first sample or a construction method is expert judgment; attributing it to an owner who specified only canvas dimensions is incorrect. Keep the choice explicit and scoped so it can be revised without changing the owner's brief. Observations alone do not become rejection rules.

### Measured facts in creative requests

Do not estimate pixel coordinates by eye and then describe them as verified. When a numerical image fact materially guides a request or verdict, retain the measurement with its source-image hash, frame and coordinate convention. The existing `asset-check --regions COLOR...` / `pixl_asset_check(regions=[...])` measures exact RGBA component boxes; it does not identify the subject or make those colors mandatory. Boxes use zero-based coordinates with exclusive right/bottom edges. For other measurements, save the reproducible calculation. When exact coordinates are unnecessary, describe the visual relationship and supply the actual reference instead.

Keep centering calculations in one coordinate convention. For a half-open box
`[left, top, right, bottom]`, its centre in pixel-edge coordinates is
`((left + right) / 2, (top + bottom) / 2)` and the canvas centre is `(width / 2, height / 2)`.
A centroid computed from zero-based pixel indices needs `+0.5` per axis to use those
same edge coordinates. A margin imbalance, box-centre offset and mass-centroid offset
are different quantities; retain the actual calculation before calling an asset centred.

The caller independently verifies consequential measured claims against the original image and measurement, including the coordinate convention; repeating a specialist's pixel map is not independent verification. Correct unsupported numbers before dispatch while preserving the required visual outcome.

## Resolve source evidence for the comparison

For candidate plans used by selected-asset preparation, call `pixl_request_review`
with the packet path and selected `asset_id` (CLI `request-review PACKET --asset ID
--root PROJECT`). It reads the exact request/criteria identities, returns cited text
with file-local bounds, and includes the current production continuation. It reports
invalid/unresolved locators and changed sources. A resolved excerpt is evidence for
the caller to interpret, not a consistency verdict. Retain this report with the review.

Copy a host-spilled tool report as exact bytes before inspecting or formatting it.
These tool reports are UTF-8 JSON: use an explicit UTF-8 decoder (for example,
`Path.read_text(encoding="utf-8")`), not the Windows process default. If saving a
formatted copy, compare its parsed value with the raw report before returning its
path/hash. A new file hash alone cannot detect text changed by a wrong decoder.
Keep the raw report alongside any formatted copy.

When the connection is already discovered, bind `request.provider` and
`request.connection: {path, sha256}` to its exact artifact. Preparation compares that
reviewed connection with the supplied one; host credentials stay outside the artifact.

Use `lines: [first,last]` on a criterion's source pointer when citing text; retain
`locator` as a human-readable label. Preparation validates explicit bounds before
saving new work. Numbered prose in older plans remains readable and receives
locator diagnostics. For non-text references inspect the actual image/animation;
for named sections resolve the location through the existing source tool. Do not
mark a locator verified merely because its claimed wording appears elsewhere.

The optional criterion `authority` uses PLAR's requirement/proposal/observation/unknown
labels. Keep its basis and scope explicit. This label is an assertion to compare,
not an automatic grant of owner authority.

## Caller: inspect before adopting

### Connected family and stage handoff

`pixl_production_plan` and `pixl_stage_prepare` return `request_review` arguments
for this same review tool. Pass that object to `pixl_request_review`; `packet`
names the store's `state.px`, `plan` names its exact connected-plan X, and `job`
is present after preparation. Existing plans can use those IDs directly. The
report includes every authored member and collective criterion with its full Q
ID, record hash, literal check and source evidence. Authority starts unclassified:
source presence or a validator pass cannot assign it. Changed plan/source/PLAR
identities remain visible so historical interpretation can be reviewed without
making an obsolete request current.

The specialist returns this report's path/hash, explicit choices and any proposed
corrections. The caller reads the original evidence and records one
`criterion_comparisons` entry for **each** returned ID, including collective rules:

```json
{
  "review_scope_sha256": "REPORT_REVIEW_SCOPE_HASH",
  "criterion_comparisons": [{
    "criterion": "EXACT_Q_ID",
    "record_sha256": "Q_RECORD_HASH",
    "source_obligation": "What the cited source actually requires, with locator",
    "authority_basis": "Required outcome, scoped expert choice, observation, or mixed clauses",
    "scope": "The asset, stage or chosen construction this rule applies to",
    "literal_delta": "What the exact rule adds, drops or leaves unchanged",
    "discriminating_alternative": "A concrete alternative that tests that difference",
    "disposition": "Keep, clarify or correct, with the proposed artifact identity"
  }]
}
```

Split mixed-authority clauses in these explanations. A sound construction does
not make every clause an owner requirement; nor does an expert choice need to be
removed merely because other valid methods exist. Keep the required artistic
outcome and identify the chosen method's narrower scope. Do not substitute one
grouped style/geometry assertion for this comparison.

Call the same tool with `comparison` pointing to the saved caller file to check
coverage and identity. Missing, repeated, stale or incomplete rows are reported.
`complete:true` means structural coverage only; semantic judgment remains the
caller’s responsibility, and `consistent` stays null in the tool report. Record
the caller's own disposition separately. Save a corrected proposal beside the
old plan/request when necessary; do not rewrite historical criteria, transplant
acceptance or prepare another job merely to repair the review.

### Compare the original sources and exact contract

For either route, open the retained packet/report and verify its hashes. Read the original brief, relevant sources, complete request and complete criteria, not just the specialist's summary or self-audit. Check:

1. Every explicit requirement survives into the request and relevant checks, including qualitative identity/style/state outcomes, actual reference role/input and consumer mapping. Check for dropped or weakened outcomes as well as added restrictions.
2. Every consequential extra restriction has its true basis and scope. Test whether a brief-conforming alternative would be rejected only because an observation or proposal was promoted to an owner requirement.
3. The proposed operation's actual declaration supports the payload. Do not infer a provider parameter, frame/direction count, alpha policy or camera from prose alone.
4. Findings concern these exact artifacts. Mechanical/hash validity and a specialist's consistency claim do not prove semantic agreement or artistic quality.
5. Each rejection rule belongs to the current candidate/stage and has satisfiable prerequisites. A first sample cannot require completed dependent family assets before it may be accepted. Retain deferred family or destination obligations with an explicit later stage in the handoff/PLAR; verify they remain scheduled rather than dropping the required outcome.

For each rejection criterion, save one concise comparison using the following
sequence. A table or JSON is sufficient; this is the caller's actual reasoning about
the source, not a worksheet to have the specialist certify for itself.

1. **Source obligation.** Derive the minimum required outcome from the original source
   wording and locator before using the draft criterion as its paraphrase. State what
   the source leaves open. For an expert criterion, identify the actual expert choice
   and candidate scope instead of inventing owner authority.
2. **Literal condition and additions.** Compare the entire check with that obligation.
   Identify the exact added or omitted words/clauses, including extent, composition,
   exclusions, comparisons and numerical bounds. A supported noun does not establish
   support for its modifiers. Read the check itself, not just its basis or label.
3. **Discriminating alternative.** For each added restriction, describe a plausible
   asset that keeps the source obligation true while making that specific restriction
   false. Name the clause being tested and whether the literal check would reject it.
   Merely changing a value the check already permits does not test that restriction.
   If the source itself excludes the alternative, identify the exact source support.
4. **Disposition.** Keep the required outcome; remove an unsupported narrowing from
   that rule or split it into an explicitly scoped expert choice with its own rationale.
   An ambiguous condition that could reject a valid alternative needs clearer wording;
   do not approve it by silently giving it a more permissive interpretation. Verify the
   correction in the returned artifact before marking the contract consistent.

For example, a requirement for a readable silhouette does not itself require an
outlined silhouette. Comparing two outline colours leaves the added outline rule
untested; a readable outline-free construction tests it. The specialist may still
recommend an outline for this sample and explain its artistic value. The comparison
preserves that expertise while accurately describing who chose it and what it binds.

Cover every rejection rule; group only genuinely identical ones. Retain the source
quote/bounds, literal delta, tested alternative and disposition together. A general
"the brief permits flexibility" statement or a prompt-choice label elsewhere cannot
cancel a restriction still present in an owner-authority acceptance condition.

Check the **review route** as well as the wording. A local mechanical check can
establish measured dimensions, frame counts or alpha values. It cannot decide which
shape is intentional foreground, whether a matte is unwanted, whether a silhouette
reads as the requested symbol, or whether an accent serves its role. For a mixed
criterion, either split the measurement and required visual judgment or set its mode
to `visual` (normally domain `visual` too). The runtime requires saved native/enlarged
candidate views for visual-mode or visual/continuity-domain reviews; labelling such a
condition `mechanical`/`local` bypasses that evidence requirement. A planning-only
correction must still specify the route its future acceptance will actually need.
Do not call a corrected contract operable merely because its source locators resolve.

When reviewing a specialist's response to a discrepancy, re-open the literal check.
An added attribution or a claim that a conventional construction excludes no valid
alternatives does not remove an unchanged mandatory recipe. Retain the source's
qualitative outcome as required and place the expert construction in a scoped proposal;
judge actual recognizability without declaring one geometric recipe universal.

Resolve every evidence-report diagnostic before calling a locator verified. For a
text citation, open the actual source, use its file-local inclusive bounds and save
those bounds in the corrected packet; a nearby matching sentence does not repair a
wrong range. An unresolved named or visual reference needs actual inspection and a
recorded finding. A source hash alone never verifies the cited location or its meaning.

The [delegation boundary](delegation.md#caller--specialist) distinguishes unchanged
historical evidence from the editable corrected proposal. A caller must not freeze
prior criterion text or authority in the new proposal; reassess those interpretations
against the source. Use the profile's visual-role distinctions when translating colour,
subject construction and transparency intent, rather than adding a construction rule.

If a contract defect is found after delivery, preserve the original request, plan,
verdicts and candidate. Save a corrected proposal and independent comparison as a new
artifact, explicitly distinguishing it from the historical contract used for delivery.
Do not create another provider job merely to correct documentation, transplant old
verdicts to new criteria, or silently rewrite durable completed work. Carry both the
historical identity and the correction's adoption scope in the exact handoff details.

Keep process requirements, output requirements and diagnostic proxies distinct. A required production route is checked through actual calls and downloaded-byte provenance; a property of the resulting image is evidence only when it establishes that claim. Do not silently turn a process restriction into an extra output-difference test, or a diagnostic into a rejection rule. Independent review uses the original source, not another agent's assertion that the rule is sourced.

Save a concise `caller-review.json` (or equivalent named fields) with reviewer role, reviewed packet hash, `consistent` / `changes_requested` / `needs_input`, per-criterion comparisons and other findings tied to request locations and source evidence, and the next action. `consistent` means the planned contract matches this assignment; it is not provider execution or asset acceptance.

If changes are needed, send the specialist the precise discrepancy and relevant source; preserve the original artifacts, revise only the affected contract, and inspect the returned new packet. Reuse the existing specialist when the host supports it. Resolve supplied facts yourself; ask the user only a consequential decision genuinely missing from the available context. No token, secret header or credential belongs in either file.

If no independent caller/reviewer exists, retain the specialist's own review as self-review, proceed within existing authorization, and report the independent comparison as unperformed. Do not invent another agent or stop ordinary direct work solely to satisfy this procedure.

## Carry the comparison through production

Return `request_review` in the normal result, containing the packet and caller-review paths/hashes and unresolved findings. After preparing the durable provider job, verify its actual request still matches the reviewed arguments. A changed requirement, criterion or request needs a new comparison; polling progress and unrelated queue changes do not.

The final caller opens the delivered assets, checks the actual request and output against this contract, and records its own observations. Keep contract consistency, provider outcome, visual quality and destination acceptance separate. For a rejected candidate, retain the failure and the revised request/criteria; changing a checker merely to pass the candidate is a contract change, not an asset correction.

When an artistic explanation asserts a measurement, compare that assertion with
its actual data and coordinate convention. Reproducing a bounding box does not
verify a stated axis angle or arm-length ratio; approximate visual descriptions
should remain approximate. Correct an inconsistent explanation in a new observation
without converting its sample geometry into an additional rejection condition.
Reassess the original claim using its stated inputs. For quoted endpoints, retain
the coordinate convention and calculate their deltas, lengths and angles before
confirming an axis or ratio. Counts of occupied pixels, a bounding box and a newly
estimated centreline measure different things; they cannot confirm the original
endpoint claim. Save the old claim, calculation and corrected interpretation together
so the caller can reproduce the comparison without inheriting the earlier assertion.
