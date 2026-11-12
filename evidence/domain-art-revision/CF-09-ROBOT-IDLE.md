# CF-09 assignment: a planted panel idle for the retained robot

This is a new, bounded development production assignment selected under the
user's CF-09 request. It extends the accepted CF-10 robot with a useful idle
animation. It does not reinterpret the old static-direction brief as an
animation requirement or claim that its accepted art was defective.

## Source and scope

Use the exact accepted East PNG from CF-10 as the starting and finishing pose.
Its SHA-256 is
`71b35089965b6457f505d569f4fc89fbcc2521bf188aa43f836dc207c3771fb4`.
This is actual PixelLab-generated art from object
`2a3cb51a-6cf7-485d-8441-3c3db762cc9d`, retained in the
[CF-10 final consumer archive](../native-production/20261112/claude-01-resume-02/consumer-delta.zip).
The [CF-10 review](../native-production/20261112/claude-01-resume-02/maintainer-review-02.json)
already accepts this static family. Its previous West failure has an accepted
local mirror successor and must not be counted as a new repair.

The [original brief](../../examples/delegation/BRIEF.md) remains historical
authority for the robot identity and four static directions; its plan-only scope
does not authorize this new animation by itself. This addendum supplies the new
motion requirement and scoped official production work under the current
development request. Preserve the original brief, controller, reference and four
accepted static direction files unchanged. South is reused fixture art, East and
North are generated, and West is a local mirror/edit; preserve those distinctions.

The inspected East has a rigid navy body, top post and narrow cyan front edge.
It has no visible eyes, limbs or wheels. Do not invent a blink, walking motion,
body breathing, new anatomy or equipment.

## Intended motion and destination

Create one calm, planted `east-idle` loop. Keep the body's silhouette, post,
framing, proportions and lower contact edge steady. The existing cyan display
briefly contracts toward its vertical center and returns to its full height.
Replace the shortened cyan portions with the existing opaque navy so this
edge-display motion does not erode the body's silhouette or create alpha holes.
Preserve the minimal navy/cyan treatment and transparent exterior. Do not add a
ground shadow, camera movement or unrelated detail.

Use five full 32×32 PNG frames, beginning and ending in the supplied starting
pose. The intended official `animate_image` request asks for four generated
frames, with the supplied starting frame returned at index 0. Record index 0 as
reused input, not newly generated art. Inspect the actual response before assuming
its count, ordering, dimensions or transparency.

The authored consumer uses durations `[800, 120, 160, 120, 400]` milliseconds, a
constant pivot `[16, 28]`, viewport `[48, 40]`, anchor `[24, 34]`, background
`#172336` and nearest sampling. These are this new assignment's decisions, not
inherited values or universal pixel-art rules. The long resting pose and brief
display pulse should read as an occasional idle signal, without moving contact.
The 32×32 source lands at `[8, 6]` in the viewport.

Serve the five PNGs separately as `assets/robot-idle/east-0.png` through
`east-4.png`; use `sprite-animation-v1` at native 1× and nearest 3×, observing at
least two actual wraps at each scale. Inspect enlarged art on a light background
as well as the assigned dark destination; navy on dark alone can hide silhouette
problems. Additional inspection scales do not replace native-scale judgment.

## Review and revision criteria

| ID | Required outcome | Evidence |
| --- | --- | --- |
| R1 | The generated East identity and proportions remain recognizable; the rigid silhouette and post stay steady in position and shape throughout. | Actual original/returned pixels at 1× and contextual enlargement. |
| R2 | The cyan panel pulse is readable, calm and returns cleanly through the loop. | Actual frame sequence and playback under the declared unequal durations. |
| R3 | Lower contact remains planted without compensating pivot changes or camera movement. | Actual frames and destination placement against the unchanged anchor/pivot. |
| R4 | The four accepted static directions and historical source/controller are unchanged. | Exact original/current hashes. |
| R5 | PNGs are transparent 32×32 frames, mapped in their actual order with declared timing and nearest sampling. | File measurements, response identities and consumer checks. |
| R6 | The exact delivered animation works in its authored destination at 1×/3× with two observed wraps. | `sprite-animation-v1` capture/check and separate specialist review. |
| R7 | A useful correction addresses a genuinely observed artistic failure and improves the same criterion in the same destination. | Retained failed candidate, reason, exact successor and old/new comparison. |

Prepare the best intended first request. Do not seed a poor candidate or invent a
defect to satisfy R7. If the first result succeeds, retain that useful outcome
without claiming a demonstrated repair. Revise only the observed weakness and
preserve valid frames and unrelated assets. Keep rejected candidates, original
requests, actual returned identities, local-edit lineage and review history.

Use existing public preparation/job/import/review/family operations. One task
may own five frame outputs through `plar-prepare`; an atlas and new renderer are
unnecessary. A locally assembled or edited artifact must never be attributed to
a provider return. A provider access failure remains an access failure; listing
tools does not prove that generation or official editing is available.

## Baseline and acceptance boundaries

The local baseline adapter repeats the unchanged East image over the authored
timing. It exists to validate the consumer and show the previous static behavior.
It is not a historical generated animation, failed provider candidate, motion
quality pass or CF-09 revision outcome. Future frame paths must remain missing
until actual output is retrieved; do not populate them with placeholder copies.

Mechanical renderer success is separate from visual acceptance. Explicit
specialist/caller review is separate from human acceptance, which remains
unrecorded. CF-09 stays open until a useful actual-art correction and its actual
destination outcome are observed. M1/M2 and broader M3/M4 remain open.
