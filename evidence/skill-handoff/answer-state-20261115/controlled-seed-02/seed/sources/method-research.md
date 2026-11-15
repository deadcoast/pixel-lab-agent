# Method research for the two open decisions

Retrieved 2026-09-14 from the bundled PIXL knowledge library via `pixl_knowledge`.
These are the library's own words and source locators, recorded so the reasoning behind
this project's criteria is traceable. **A bundled method and its bundled proof-of-concept
receipt are context for this project, not proof about this project's assets.**

## silhouette-readability

Title: "Evaluate identity using silhouette and target backgrounds".
Applies to: characters, inventory icons, interactive props.
Sources: `training/original-docs/PIXEL-ART-DEEP-RESEARCH.md` lines 857-867 and 1563-1573;
`training/original-docs/PIXEL-ART-ASSETS.md` lines 11-15.

Requires: "Intended viewing scale, representative backgrounds and identity landmarks".
Checks: "Named identity landmarks remain visible at the target size."
Pitfalls the library states explicitly: "Silhouette alone cannot validate faces,
materials or fine symbols." and "No contrast ratio or component count proves aesthetic
quality."

**Applicability here.** This is why the project's readability and role criteria are
declared with domain `visual` and mode `visual`, and why the scout/medic distinction is
stated as an observable landmark condition at native scale rather than as a pixel count.
It also means the outline question cannot be settled by measuring the references: the
library explicitly denies that component counts or contrast decide aesthetics.

## edge-rhythm

Title: "Audit stair-step runs without imposing one contour style".
Sources: `training/original-docs/PIXEL-ART-DEEP-RESEARCH.md` lines 1402-1431 and 857-867.

Pitfalls the library states explicitly: "Not every uneven run is a jaggy; shape can
require an abrupt change." and "Mechanical contour smoothing can erase style and
identity."

**Applicability here.** This is the direct reason the outline disagreement is retained
as a conflict for the user rather than resolved by the agent. The library's position is
that contour style is authored intent, so picking one reference over the other is a
style decision belonging to the project owner, not a cleanup the agent should perform.

## integer-presentation

Title: "Render at a declared logical grid and inspect device pixels".
Sources: `training/original-docs/PIXEL-ART-DEEP-RESEARCH.md` lines 907-919, 1293-1315,
1636-1638.

Requires: "Logical resolution, camera convention and target viewport dimensions".
Pitfalls: "Nearest filtering alone does not constrain lighting resolution." and
"Noninteger scaling, arbitrary rotation and browser zoom can change displayed pixel
widths."

**Applicability here.** The method requires a target viewport/display scale as an input.
This project has neither a canvas size nor a display scale, which is why the canvas
choice is recorded as unresolved together with a separate unresolved display-scale
choice, and why the engine criterion is declared but cannot be exercised.

## Consequence for this session

None of these methods supplies a value for the two open decisions. They establish that
the decisions are the owner's to make and that they are coupled, which is recorded in
`reference-observations.md`. No method was adopted into a design decision (`D`) this
session, and no proof was executed for one, because production has not been authorized
to start.
