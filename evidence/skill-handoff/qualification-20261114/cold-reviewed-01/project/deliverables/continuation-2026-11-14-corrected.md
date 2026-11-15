# Continuation note, 2026-11-14 (corrected successor)

Corrected continuation of the scout and medic family project by PIXL (agent) in an
isolated evaluation session, written in response to `CALLER-REVIEW.md`. The review is a
development-evaluation review of the preceding handoff; it supplies no owner answers and
no new permission. The predecessor's note `deliverables/continuation-2026-11-14.md` is
preserved unchanged as the record of that session; this note supersedes its claims where
stated below.

Resumed from `state.px/state.px` at revision 6 (canonical hash `b9a66bef…b5b7`), which
validated cleanly with every bound source, candidate and evidence file current. No
families, no provider jobs and no ready tasks. No generation provider is configured in
this session, so nothing was generated and no acceptance changed.

## Authority check of the review findings

Each finding was checked against the brief (`sources/brief.md`), the measured study
(`sources/reference-observations.md`), the saved intake records and criteria, and the
installed profile (intake-sample "Keep authority through derived rules", the artistic
authority reference, and the PX2 specification).

1. **Exclusive palette rule.** The saved criterion `q_palette` read "every visible pixel
   is a member of the confirmed project palette, with no colours outside it" and was
   attached to the sample, scout and medic outputs. The brief imposes no fixed palette; it
   asks for a family "matching this project" and names two references. The three hex
   values in `i_palette` are measured from reference pixels, so they are observations.
   The project's own study already states that an unoutlined treatment may need "a
   second teal value, or a cream accent" to keep the shoulder, base and stalk landmarks.
   That variation satisfies the brief yet would fail an exclusive membership check, so
   exclusivity is a derived proposal, not an entailed requirement. The profile is explicit:
   when no fixed palette is imposed, production checks omit exact palette membership.
   **Corrected:** `q_palette` is now a palette account, not an allowed-colour list. It
   requires a retained measurement that lists every visible colour with its role against
   the reference colours and names any colour not present in the references, so the
   visual style review can judge it. An exclusive allowed-colour rule stays available as
   a separate instruction the owner has not given.

2. **"Confirmed" prerequisites inside criteria.** `q_canvas` and `q_outline` referred to
   "the confirmed canvas size", "the confirmed alpha policy" and "the confirmed outline
   treatment". Under PX2, sample work can test proposed and observed choices; only
   production and delivery require every contract choice confirmed. As worded, the
   criteria made the sample unevaluable until every choice was confirmed, which was a
   stricter prerequisite than the owner or the specification set. **Corrected:** both now
   refer to the canvas size, alpha policy and outline treatment named in the candidate's
   contract, so each choice carries its own recorded status into the check.

3. **Palette, sampling and alpha "confirmed by" other answers.** The predecessor's outline
   row said the outline answer lets the palette move to confirmed, and its next-operation
   list wrote a sample contract with "confirmed palette, nearest sampling and binary
   alpha" after answers about outline, canvas and design language. None of those three
   rows was asked, and an answer adopts only the choices it explicitly supplies. The
   outline answer decides whether navy `#25354A` is a working colour; it does not make the
   colour list an owner-adopted palette. **Corrected** in the table and the next-operation
   list below: the sample contract carries palette and alpha as observed and sampling and
   design language as proposed. Those statuses are legitimate inputs for a sample trial
   and must be confirmed by the owner before scout or medic production.

4. **Design language marked "needed now".** The predecessor listed the proposed design
   language as blocking the sample contract. A proposed choice does not block a sample
   under PX2; the sample is the trial of that proposal. **Corrected:** it is needed before
   production, and the owner is still invited to disagree before the trial, but it does
   not block the trial.

The corrected `i_palette` rationale, the three reworded criteria and this note are the
only semantic changes. No done task, candidate, evidence or verdict is affected: the
amended records are referenced only by the open sample, scout and medic outputs, which
have no candidates.

## Decision table (corrected)

Authority column: who decides, and the saved status. "Needed now" means the next local
operation cannot proceed without it. An answer adopts only the row it names.

| Choice (record) | Authority / status | Needed now? | Effect of the answer |
|---|---|---|---|
| Outline treatment (`i_outline`) | Owner; **conflict** between the two references | **Yes.** A conflicting output choice blocks every phase, including the sample trial. | Names the treatment the sample trials and whether navy `#25354A` is a working colour. If "no outline", the shoulder bar, base bar and stalk interiors must be re-authored in another colour or dropped deliberately. It does not confirm the palette: the colour list stays observed until the owner adopts it, and no exclusive allowed-colour rule exists unless the owner asks for one. |
| Canvas size (`i_canvas`) | Owner; **unresolved**, final size explicitly not chosen | **Yes.** An unresolved output choice blocks every phase. | Either a final canvas (moves to confirmed) or an explicit go-ahead for a trial canvas for the sample only (moves to proposed; the agent proposes 32 x 32, the references' canvas). Either lets a concrete contract be saved for the sample output. |
| Design language (`i_design_language`) | Owner; **proposed** by the predecessor | No. The sample is the trial of this proposal. | Agreement is needed before scout/medic production. An objection now changes what the sample trials. |
| Game backgrounds (`i_backgrounds`) | Owner; **unresolved** | Helpful, not blocking | The comparison sheet showed the outline helps on busy mid-value backgrounds and hurts on dark ones. Knowing the typical level backgrounds informs the outline choice and makes the readability review representative. The light/dark/busy bands in `q_readability` are the agent's test set. |
| Display scale (`i_display_scale`) | Owner; **unresolved** | Before visual review, not before the contract | Sets the integer zoom for the readability and style reviews. At 1x the outline difference is not reliably visible; from 3x up it is. |
| Role differentiation (`i_role_diff`) | Owner; **unresolved** | Before scout/medic production, not before the sample | Chooses the device that makes a scout read as a scout and a medic as a medic. The sample is the scout, so an early answer lets the sample carry the device. |
| Palette (`i_palette`) | Owner; **observed** from the references | No for the sample; confirmed before production | The sample contract carries the measured colours as working colours (status observed). Owner adoption of a colour list is a separate step. The corrected `q_palette` accounts for colours; it does not reject colours outside the list. |
| Alpha (`i_alpha`) | Owner; **observed** binary | No for the sample; confirmed before production | The sample contract carries binary alpha as the observed working policy. Owner confirmation makes it the output policy. |
| Sampling (`i_sampling`) | Owner; **proposed** nearest | No for the sample; confirmed before production | Depends on the engine; nearest is the proposal that preserves the flat look. |
| Engine / importer (`i_engine`) | Owner; **unresolved** | Not now | Required only for the family delivery's engine import criterion. Without it that criterion stays unavailable, not failed. |
| Roster, side view (`i_roster`, `i_view`) | Owner; **confirmed** from the brief | Settled | None. |

## Recommendation, labelled as a proposal

Unchanged in substance from the predecessor. The decisions are coupled, and the
comparison sheet supports this proposal if the owner has no strong preference:

- Keep the 2 px dark outline and a 32 x 32 canvas for the sample. The outline carries the
  interior landmarks, and 32 x 32 leaves enough interior for the scout and medic to
  differ. This is the reversible option, because the sample is a proof and not a delivery.
- If the game's levels are predominantly dark, prefer no outline, and plan to re-author
  the shoulder, base and stalk landmarks as a second teal value or a cream accent. The
  corrected palette account allows that re-authoring to be judged visually rather than
  rejected mechanically.
- If the levels are busy or mid-value, keep the outline.

A trial sample under this proposal stays a proposal until the owner adopts it; it would
not confirm the canvas, outline, palette, alpha or sampling choice by itself.

## Next local operation and its prerequisites (corrected)

Needs only the outline and canvas answers:

1. Retain each answer verbatim as a local source. Move `i_outline` to the status the answer
   supports (confirmed, or proposed if the owner authorizes a trial without deciding), and
   `i_canvas` likewise. No other row changes status.
2. Add a C contract for the sample output linking, through `ch`: `i_canvas`, `i_outline`,
   `i_view` (confirmed), `i_palette` and `i_alpha` (observed), `i_sampling` and
   `i_design_language` (proposed). Set it as `f_sample.ct`. Commit with the expected hash.
   The sample task then shows as ready. This contract is a sample trial; it cannot be
   reused for scout or medic production until every linked choice is confirmed.
3. Preparing the sample's generation request needs the official PixelLab tool declarations
   from the host. This session has only the local PIXL server configured, so request
   preparation and dispatch remain unavailable here. That is a missing capability, not a
   failed attempt.
4. Before scout/medic production: owner confirmation of palette, alpha, sampling and design
   language, plus a role-differentiation choice. Before family delivery: the engine.

Nothing in this note changes any saved acceptance. The earlier handoff records are
preserved; a new handoff record points at this note and at the caller review.
