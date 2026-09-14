# Outline treatment and canvas size: decision study

Reviewer: PIXL (agent). Date: 2026-09-11.
Inputs: `reference.png` (sha256 d997cade…), `reference-b.png` (sha256 e76b40ce…).
Artifacts: `work/study/measurement.json`, `work/study/contact-sheet.png`,
`work/study/variant-*.png`. Generator: `work/tools/edge_study.py`.

This study exists to let the project owner settle two intake choices that
currently block all character work: `edge_treatment` (conflict) and `px`
(unresolved). It does not settle them, and it produces no character art.

## 1. What the two references actually disagree about — measured

Both files are 32×32 with zero fractional-alpha pixels and an **identical
silhouette**: the same 390 opaque cells, bounding box x7–24, y3–27, an occupied
area of 18×25.

The files differ in exactly **180 pixels**, and every one of those is the same
substitution: navy `#25354A` in `reference.png` where `reference-b.png` has
teal `#56B5BC`. There is no other difference — not shape, not the cream
`#F4DDA2` marks, not alpha.

So the disagreement is purely outline treatment, exactly as stated:

| | `reference.png` | `reference-b.png` |
|---|---|---|
| Outline | continuous dark rim | none |
| Visible colors | 3 | 2 |
| Navy pixels | 180 (46.2% of the silhouette) | 0 |
| Interior fill left | 210 cells | 390 cells |

## 2. The dark rim is 2 cells deep

Peeling the silhouette boundary ring by ring:

| Depth from edge | Cells in ring | Navy cells |
|---|---|---|
| 1 | 92 | 92 |
| 2 | 82 | 82 |
| 3 | 58 | 6 |
| 4+ | 158 | 0 |

The rim is a uniform **2-pixel** outline, plus 6 stray navy cells at depth 3 in
the inner corners of the head notch. A 1-pixel rim on the same silhouette would
be 92 cells (23.6%) and would leave 298 interior cells instead of 210.

This matters more than it looks: a 2px outline on a figure this size spends
**46% of the character's pixels on its own edge**. Those are the pixels that
would otherwise carry the scout/medic distinction.

## 3. Visual comparison — contact sheet

`work/study/contact-sheet.png` shows three treatments (rows) on light, dark and
busy checkered grounds (columns), each at native scale, ×4 and ×8:

1. `variant-as_supplied_2px_outline.png` — `reference.png` unmodified
2. `variant-as_supplied_no_outline.png` — `reference-b.png` unmodified
3. `variant-derived_1px_outline.png` — **agent-derived study material**: the
   same silhouette with the navy reduced to the single outermost ring. This is
   a third option offered for the decision, not an approved project style.

Inspected at ×8 by the agent, on the three grounds:

- **2px outline, dark ground**: the navy rim is close in value to the dark
  ground and the outer edge stops reading as an edge. The figure loses its
  silhouette boundary and reads as a teal block sitting in a dark well. This is
  the weakest cell in the sheet.
- **2px outline, light and busy grounds**: strong separation; the rim does its
  job. But the teal interior is visibly squeezed — on the ears/horns the navy
  closes over the form entirely and they read as solid dark shapes rather than
  outlined ones.
- **No outline, dark and light grounds**: clean and confident; the flat teal
  holds its shape well at every scale.
- **No outline, busy ground**: still separates, but the boundary is soft
  against similar-value clutter. This is the weakest cell for this treatment.
- **1px outline, all three grounds**: reads on every ground, keeps the outer
  boundary crisp on the busy ground, and preserves 298 interior cells. At ×8
  the ears/horns stay open shapes instead of filling in.

At native scale (column 1 of each group) the three rows are nearly
indistinguishable on screen. **The outline decision is only observable at the
game's actual display scale**, which is itself unrecorded — see §5.

## 4. The two decisions are coupled, not independent

The outline cost scales inversely with canvas. Using the references' 26/32
vertical occupancy ratio, the share of figure height eaten by outline at top
and bottom:

| Canvas height | Figure height | 2px outline | 1px outline |
|---|---|---|---|
| 16 | 13 | 30.8% | 15.4% |
| 24 | 20 | 20.0% | 10.0% |
| 32 | 26 | 15.4% | 7.7% |
| 48 | 39 | 10.3% | 5.1% |
| 64 | 52 | 7.7% | 3.8% |

Read as a constraint rather than a ranking: **a 2px outline is not viable below
roughly 48px of canvas** for two characters that must be told apart, because
below that the rim plus a side-view head leaves too few interior cells for a
satchel, a cross marking, a scope or a pose difference. A 1px outline is
comfortable from 24px up. No outline imposes no floor at all.

## 5. What still has to come from the project owner

Ranked by how much they block work:

1. **`edge_treatment`** — conflict. Choose one of: 2px rim as in
   `reference.png`; no rim as in `reference-b.png`; or the 1px middle option in
   row 3. Everything raster is blocked on this.
2. **`px`** — unresolved. Both references are 32×32 with an 18×25 occupancy,
   which is evidence of intent but not a stated decision. If the 2px rim is
   chosen, §4 argues for 48×48.
3. **`display_scale`** — unresolved and not in the brief. §3 shows the outline
   decision is invisible at 1× and obvious at 8×. Knowing the intended on-screen
   scale would make choice 1 much easier to settle.
4. **`engine`** — unresolved and not in the brief. Engine acceptance for the
   family cannot be planned, let alone verified, until a destination exists.

## 6. Agent recommendation (not a decision)

**1px outline at 32×32**, on this evidence: it is the only treatment that reads
on all three grounds at every inspected scale (§3), it returns 88 interior
cells to the character compared with the supplied 2px rim (§2), and it keeps
the navy `#25354A` that `reference.png` introduces rather than discarding a
color the owner may have chosen deliberately. It is also the option that stays
viable if the canvas later moves down to 24px.

If the busy-ground case is not real for this game — flat or high-contrast
backgrounds only — then `reference-b.png`'s no-outline treatment is the better
answer and the simpler contract, and 32×32 still holds.

The 2px rim as supplied is the one option this study argues against at 32×32,
purely on the interior-budget arithmetic in §2 and §4. It becomes reasonable
again at 48×48.

## 7. Limits of this study

- Measurements in §1, §2 and §4 are computed from the actual supplied files and
  are reproducible with `work/tools/edge_study.py`.
- §3 is the agent's visual inspection of the contact sheet. It is not the
  project owner's judgment and does not settle a conflicting choice.
- The references are blocky placeholder forms, not characters. Conclusions
  about interior budget are arithmetic about cell counts; they are not
  validated against an actual scout or medic pose, because none exists yet.
- Nothing here was generated by PixelLab. No remote generation tool was
  available in this session.
