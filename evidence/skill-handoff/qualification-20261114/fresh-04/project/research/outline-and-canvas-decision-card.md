# Decision card: outline treatment and canvas size for the scout/medic family

Written 2026-11-15 by PIXL (agent). This is a research report. Nothing here is an owner decision unless the owner adopts it.

## Question and current authority

The owner asked for a side-view character family (scout, medic) matching two references that disagree about outline treatment, with the canvas size still unchosen. Before a representative sample can be requested, two choices must be made: edge treatment and canvas size.

| Property | Value | Authority | Source | Applies to |
| --- | --- | --- | --- | --- |
| Game view | side view | requirement | BRIEF.md item 1 | all family members |
| Family members | scout, medic | requirement | BRIEF.md item 2 | family plan |
| Style reference | reference.png and reference-b.png | requirement (role: style) | BRIEF.md item 3 | all family members |
| Outline treatment | continuous dark outline OR no outline | conflict, unresolved | BRIEF.md item 4; measurements below | all family members |
| Canvas size | unknown | unresolved | BRIEF.md item 5 | all family members |
| Fill and eye colour roles | teal fill #56B5BC, cream eyes #F4DDA2 | observation | both references | proposal to carry as colour roles, not as an exclusive palette |
| Outline colour | dark navy #25354A | observation | reference.png only | depends on outline decision |
| Alpha | binary (no fractional alpha) | observation | both references | not adopted as a requirement |
| Reference facing | frontal, symmetrical face | observation | both references | the side-view construction is not shown by either reference |
| Delivery destination and engine | unknown | unresolved | not in brief | delivery stage |
| Generation provider | none assigned this session | requirement | BRIEF.md item 6 | this evaluation session |

## Measured facts (pixl_asset_check and a pixel dump; both files 32x32 PNG)

| File | sha256 | Visible pixels | Colours | Components | Subject bbox (x0,y0,x1,y1) |
| --- | --- | --- | --- | --- | --- |
| reference.png | d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7 | 390 | 3 | 1 | 7,3,25,28 |
| reference-b.png | e76b40ce38aeb436d0f5f0e433c4ac1eb4519bf93a7b29cd7a81a4609914a12a | 390 | 2 | 1 | 7,3,25,28 |

- The subject occupies 19 x 26 logical pixels inside the 32 x 32 canvas in both files.
- The two files share identical alpha coverage and identical eye pixels (two 3 x 4 cream blocks). They differ only in colour: reference.png replaces a 2-pixel-wide band around the whole subject with dark navy (180 pixels), reference-b.png keeps teal everywhere (366 teal pixels).
- In reference.png the two ears are 4 pixels wide, so the 2-pixel outline fills them completely: the ears are solid dark, with no teal interior.
- Neither file contains anti-aliasing, dithering, shading ramps or any side-facing feature. Both show a frontal symmetric face.

## Visual findings (viewed by the agent at 1x and 4x, research/outline-comparison-sheet.png)

The sheet places each reference, pixels unchanged, over light, dark, mid-teal and busy checker backgrounds.

- Outlined (reference.png): the silhouette stays closed on all four backgrounds, including the mid-teal background whose hue is close to the fill. At 1x the ears read as dark bars rather than teal ears because the 2 px line consumes them.
- No outline (reference-b.png): clean and bright on light and dark backgrounds; at 1x the ear notch is slightly clearer than in the outlined version. On the mid-teal background the body nearly disappears and only the eyes remain; on the busy background the edge is readable but softer.
- Both read as the same character; the outline does not change proportions or landmark positions.

These findings are scoped to these two 32 x 32 files on these four synthetic backgrounds. They do not establish a universal minimum canvas or a contrast threshold.

## Knowledge consulted (installed library, read-only)

- `silhouette-readability` (method index): curated diagnostic to compare the coloured asset on representative light, dark and busy backgrounds and to check that named landmarks remain visible. The sheet above follows that diagnostic. Cited text at PIXEL-ART-DEEP-RESEARCH.md lines 857-867 (cluster rejection constraints: do not destroy an identifying facial feature, do not add edge AA to an edge meant to stay hard) and lines 1402-1431 (cluster semantics list naming `silhouette`, `outline` and `eye` as clusters to declare). sha256 7efc4789ca70dfd9964abc2bc1100af318306236400e3496f7a0a5654f725e28. PIXEL-ART-ASSETS.md lines 11-15 (sha256 450a335ed6563a7f4a5cc380f2bbe72f98b70e532ac2c8d16a679bcc545d4900) is a UI brief about balance and consistency and does not bear on this choice.
- `edge-rhythm`: audit stair-step runs without imposing one contour style. Applicable later to the sample's diagonal edges; not relevant to the outline/no-outline decision itself.
- Applicability: the library supports treating the outline as a declared semantic cluster and supports the background comparison as a diagnostic. It does not prescribe outlined or outline-free characters. The choice remains an owner aesthetic decision informed by the game's actual backgrounds.

## Recommendation (proposal, not adopted)

1. Edge treatment: keep the continuous dark outline direction of reference.png, because the game's backgrounds are not known and the outlined version is the only one that survives a same-hue background. Propose line weight 1 px at the chosen canvas so the ears and thin side-view limbs keep teal interiors. A 1 px line is a scoped adaptation of reference.png, not a third reference; the owner may instead adopt reference.png's 2 px weight or reference-b.png's no-outline treatment.
2. Canvas: propose 32 x 32 per member, matching the references' grid so colour roles and proportions transfer without resampling, with the subject height kept near 26 px. If the owner needs visible role props on both characters (medic cross or satchel, scout scarf or goggles) at a display scale below 3x, propose 48 x 48 instead. Either value needs the owner's confirmation.
3. Side-view construction: neither reference shows a side view. The representative scout sample must establish facing direction, limb placement and ground contact; that is the first thing to review on the sample.

## What this does not establish

- No art has been generated. No provider was called. The comparison sheet reuses reference pixels only.
- The game's actual backgrounds, display scale, engine and delivery paths are unknown.
- The owner has not adopted any of the proposals above.

## Next action

Once the owner answers the two questions (outline treatment; canvas size), prepare the scout representative sample: translate the confirmed choices into a concrete contract on the sample output, save the request and criteria packet, and dispatch through a PixelLab connection when one is assigned. Until then the sample task stays blocked by the unresolved choices.
