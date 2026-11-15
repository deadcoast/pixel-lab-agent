# Continuation note, 2026-11-14

Cold resume of the scout and medic family project by PIXL (agent) in an isolated
evaluation session. Resumed from `state.px/state.px` at revision 5 (canonical hash
`dc5029e4…57000`), which validated cleanly with every bound source, candidate and
evidence file current. No families, no provider jobs and no ready tasks were reported.
No generation provider is configured in this session, so nothing was generated.

## What the predecessor established

- Two research tasks are done with passing verdicts: the reference measurement study
  (`sources/reference-observations.md`) and the outline-by-scale comparison sheet
  (`deliverables/outline-scale-comparison.png`, read in this session as well).
- The sample, scout, medic and family tasks are all open. The sample task is blocked
  only by the missing raster contract, which in turn waits on the canvas choice and on
  the outline choice that decides the palette.
- The reference figures are front-facing and symmetric; the destination is side view.
  The predecessor proposed treating the references as a style swatch rather than as the
  character body. That proposal has not been agreed by the owner.

## Decision table

Authority column: who decides, and the current saved status. "Needed now" means the
next local operation cannot proceed without it.

| Choice (record) | Authority / status | Needed now? | Effect of the answer |
|---|---|---|---|
| Outline treatment (`i_outline`) | Owner; **conflict** between the two references | **Yes** | Decides whether `#25354A` navy is in the output palette, lets the palette move from observed to confirmed, and makes `q_outline` testable. If "no outline" is chosen, the shoulder bar, base bar and stalk interiors must be re-authored in another colour or dropped deliberately. |
| Canvas size (`i_canvas`) | Owner; **unresolved**, explicitly deferred by the owner | **Yes** | Lets a concrete contract be saved for the sample output, which clears the only blocker on the sample task. |
| Design language (`i_design_language`) | Owner; **proposed** by the predecessor | **Yes** | Settles whether the side-view figure carries the two-stalk blocky body of the references or only their colour, edge and detail density. The sample request cannot be written honestly without this. |
| Game backgrounds (`i_backgrounds`, added this session) | Owner; **unresolved** | Helpful, not blocking | The comparison sheet showed the outline helps on busy mid-value backgrounds and hurts on dark ones. Knowing the typical level backgrounds turns the outline choice from a guess into an informed one and makes the readability review backgrounds representative. The light/dark/busy bands in `q_readability` are the agent's test set, not the game's. |
| Display scale (`i_display_scale`) | Owner; **unresolved** | Before visual review, not before the contract | Sets the integer zoom at which readability and style match are judged. At 1x the outline difference is not reliably visible; from 3x up it is. |
| Role differentiation (`i_role_diff`) | Owner; **unresolved** | Before scout/medic production, not before the sample | Chooses the device that makes a scout read as a scout and a medic as a medic: a reserved accent hue, a silhouette attachment, or both. The sample is the scout, so an early answer lets the sample carry the device. |
| Palette (`i_palette`) | Owner; **observed** from the references | Follows the outline answer | Confirming it also adopts the exclusive palette rule in `q_palette`. That exclusivity is a derived rule, not something the brief states. |
| Alpha (`i_alpha`) | Owner; **observed** binary | Low stakes | Confirming binary alpha as output policy makes `q_canvas` fully specified. |
| Sampling (`i_sampling`) | Owner; **proposed** nearest | Not now | Depends on the engine; nearest is the proposal that preserves the flat look. |
| Engine / importer (`i_engine`) | Owner; **unresolved** | Not now | Required only for the family delivery's engine import criterion. Without it that criterion stays unavailable, not failed. |
| Roster, side view (`i_roster`, `i_view`) | Owner; **confirmed** from the brief | Settled | None. |

## Recommendation, labelled as a proposal

The decisions are coupled. The comparison sheet supports this proposal if the owner has
no strong preference:

- Keep the 2 px dark outline and a 32 x 32 canvas for the sample. The outline carries
  the interior landmarks, and 32 x 32 leaves enough interior for the scout and medic to
  differ. This is the reversible option, because the sample is a proof and not a
  delivery.
- If the game's levels are predominantly dark, prefer no outline, and plan to re-author
  the shoulder, base and stalk landmarks as a second teal value or a cream accent.
- If the levels are busy or mid-value, keep the outline.

A trial sample under this proposal would stay a proposal until the owner adopts it; it
would not confirm the canvas or outline choice by itself.

## Next local operation and its prerequisites

Once outline, canvas and design language are answered:

1. Add a visual contract record for the sample output with the confirmed canvas,
   palette, side view, nearest sampling and binary alpha, linking the confirmed choices,
   and set it as the sample output's contract. Move the answered choices to confirmed
   with the owner's answer retained as a source. Commit with the expected hash.
2. The sample task then shows as ready. Preparing its generation request needs the
   official PixelLab tool declarations from the host. This session has only the local
   PIXL server configured, so request preparation and dispatch remain unavailable here.
   That is a missing capability, not a failed attempt.

Nothing in this note changes any saved acceptance. The earlier handoff record is
preserved; a new handoff record points at this note.
