# Teal and cream character family brief

## Assignment (owner instruction, 2026-11-14)
The owner asked for a character family for a side-view game, produced with PIXL in this consumer project.
The family has two members: a scout and a medic.
References are reference.png and reference-b.png.
The owner authorized proceeding with the choices below without further confirmation.

## Confirmed owner choices
Outline: use the reference's dark outline (the continuous dark outline seen in reference.png).
Canvas: 32 by 32 pixels per character.
Palette: the agreed teal and cream palette.
Transparency: binary (each pixel fully opaque or fully transparent).
View: side view.
Display: nearest-neighbor sampling.

## Reference observations (measured, not additional requirements)
reference.png (sha256 d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7): 32x32, binary alpha, three opaque colors: dark outline #25354a, teal #56b5bc, cream #f4dda2; one connected component; visible box x 7-24, y 3-27.
reference-b.png (sha256 e76b40ce38aeb436d0f5f0e433c4ac1eb4519bf93a7b29cd7a81a4609914a12a): 32x32, binary alpha, two opaque colors: teal #56b5bc, cream #f4dda2; no outline.
Both references are the same two-eared block figure with two cream eye blocks; they establish color roles and edge treatment, not a required silhouette for the scout or medic.
The exact hex values above are the measured teal, cream and dark values of the owner's references and are adopted as the concrete palette for this project; a different shade would be an owner change.

## Expert proposals (PIXL, open to owner revision)
Scout identity proposal: lighter build, forward lean, a hood or cap and a small pack, teal body with cream face and strap accents.
Medic identity proposal: sturdier stance, a satchel or armband carrying a cream cross or plus mark as the readable role landmark.
Both members share one ground line and head height so they read as one cast when placed side by side.
Destination proposal: assets/characters/scout.png and assets/characters/medic.png, separate PNGs at native 32x32.

## Unresolved
Target engine or runtime project: none named; engine import behavior cannot be verified until one is supplied.
Display scale: nearest-neighbor is confirmed, but the integer display multiple is not stated.
Facing direction within the side view: not stated; the sample will use a right-facing pose as a proposal.

## Session constraints
This evaluation session has only the local PIXL MCP tools. No generation provider is assigned, so no PixelLab request can be discovered, prepared with a real schema, or dispatched here. Planning, intake, criteria and handoff are the deliverables of this session.
