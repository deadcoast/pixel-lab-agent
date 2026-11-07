# Production approach — small lantern prop matching translucent-reference.png

Companion to `analysis/reference-analysis.md`. Machine-readable contract:
`plan/lantern-treatment.contract.json`. Nothing here has been generated yet; PixelLab tools are not
exposed in this session (see "Blocker").

## 1. Style contract

| Field | Value | Status |
|---|---|---|
| Canvas | 32 x 32 | proposed (matches the reference exactly) |
| Alpha | full, straight (non-premultiplied) | confirmed — the user asked to keep the treatment |
| Alpha levels | 0, 96, 160, 255 only | proposed (measured from the reference) |
| Sampling | nearest, integer scale | proposed |
| View | flat frontal elevation, no ground contact | proposed — the reference has no perspective cue |
| Palette | 5 RGB values, listed below | proposed — no fixed palette was imposed |
| Edge treatment | hard silhouette, zero anti-aliasing on any contour | proposed (measured) |
| Translucency | alpha grading on the glass hue only; RGB never blended | proposed (measured) |
| Light bias | brighter to the right | observed in the reference |

Palette — three values are inherited byte-exact from the reference so the two assets read as one set;
two are new because a lantern has form the flat reference did not need:

| Role | RGB | Origin | Fractional alpha? |
|---|---|---|---|
| structure_dark | `#25354a` | reference, unchanged | no |
| structure_mid | `#3d7583` | **new** — lit metal, placed midway between the navy and the glass teal so it stays in one ramp | no |
| glass | `#56b5bc` | reference, unchanged | **yes — the only role that may** |
| flame_mid | `#d99a4e` | **new** — warm mid giving the flame a two-step ramp | no |
| flame_core | `#f4dda2` | reference accent, unchanged | no |

Going from 3 to 5 RGB values is the one real departure from the reference. It is a proposal, not a
confirmed choice: if the reference is finished art rather than a fixture, drop `structure_mid` and
`flame_mid` and keep the lantern as flat as the reference. That decision is cheap to reverse before
the first candidate and expensive after a family exists.

## 2. Geometry plan

Opaque body inside x 9..22, y 3..27; fringe columns land on x=8 (alpha 96) and x=23 (alpha 160), so
the whole prop occupies a 16 x 25 footprint against the reference's 20 x 25 — visibly the smaller
sibling, which is what "small matching prop" asks for.

Handle: inverted-U ring, 2px thick, y 3..7 — deliberately echoing the reference's two top prongs.
Cap: 2px bar, y 8..9. Housing: 2px posts at x 9..10 and x 21..22, glass x 11..20, y 10..24.
Flame: 4 x 6 cluster at x 14..17, y 15..20, cream core inside amber, matching the reference's habit
of 3-4 pixel wide warm blocks floating in glass. Base: 2px bar y 25..26 plus a foot row at y 27.

Every part is 2px thick because the reference has no 1px structure anywhere; a 1px lantern frame
would read as a different set.

## 3. Pipeline

The key decision: **do not ask the image generator for the transparency.** The fringe is a
deterministic rule — `evidence/fringe-rule-proof.json` shows that re-deriving it from a stripped
reference reproduces the original file byte-identically. A generator returning its own soft edges
would produce dozens of alpha levels and blended RGB, which is exactly the treatment the reference
avoids. So:

1. **Generate an opaque body only.** 32 x 32, transparent background, no soft edges, style-conditioned
   on `translucent-reference.png`.
2. **Palette-lock.** Map every visible pixel to the 5 approved RGB values by nearest ramp neighbour
   (local, deterministic). Reject rather than dither.
3. **Author the fringe.** `python tools/apply_glow_fringe.py plan/lantern-treatment.contract.json
   body.png lantern.png`. This is idempotent and can be re-run after any body edit.
4. **Gate mechanically.** `python tools/alpha_treatment_check.py plan/lantern-treatment.contract.json
   lantern.png` plus `pixl asset-check --width 32 --height 32 --alpha full --palette ...`.
5. **Inspect visually.** Native scale and 8x, composited over the same four backgrounds as the
   reference, side by side with the reference.
6. **Verify import** in the destination engine: nearest filtering, integer scale, straight-alpha
   blending, no atlas bleed into the 1px fringe.

Steps 2-4 are local and free. Only step 1 needs PixelLab, and if it stays unavailable the body can be
hand-authored against the geometry plan above at no loss of contract fidelity.

## 4. Proposed provider request (draft — not validated against a live schema)

Route: `create_1_direction_object`, which takes `style_images` and is the tool intended for matching
an existing reference. Poll with `get_object`.

```json
{
  "description": "small hanging lantern prop, front view, dark navy metal frame with a carrying ring on top, teal glass panes, small warm flame inside, flat single-value materials, hard pixel edges, no anti-aliasing, transparent background",
  "style_images": ["translucent-reference.png"],
  "size": 32
}
```

Caveats, all unresolved: the parameter names above come from a dated local capability index, not live
discovery; the actual encoding for `style_images` (path, base64, URL) is unknown; `size` may not be
the real field name. Discover the live schema before preparing the job, and save the discovered
schema with the request rather than this draft.

## 5. Acceptance criteria

| Domain | Condition | Evidence mode |
|---|---|---|
| mechanical | 32 x 32; alpha values only in {0,96,160,255}; every visible RGB in the 5-entry palette; fractional alpha only on `#56b5bc`; clear pixels are `(0,0,0,0)`; one 4-connected opaque body; every partial pixel adjacent to it | local — `tools/alpha_treatment_check.py` |
| visual | reads as a lantern at native size; the halo reads as light bleed on the project's actual backgrounds; hard silhouette preserved | visual inspection at 1x and 8x over the background set |
| continuity | sits beside `translucent-reference.png` as one set: same frame weight, same light bias to the right, same flatness | visual, both assets composited together |
| engine | nearest sampling, integer scale, straight-alpha blending, fringe survives atlas packing | live in the destination project |

Mechanical passes prove none of the other three.

## 6. Decisions needed from you

1. **Backgrounds.** A 37%-alpha cool halo is nearly invisible on light scenery (measured). If the game
   has bright environments, either raise the left level or make the halo warm.
2. **Side-on or top-down.** Top-down would want a symmetric halo and probably a ground shadow; the
   reference's left/right pair implies side-on.
3. **Detail level.** Keep the reference's flat 3-colour discipline, or accept the 5-colour proposal.
4. **Destination engine and display scale**, for the import check.

None of these block starting: the mechanical contract and the fringe rule are settled, and 1-3 change
values inside the same contract rather than the approach.

## 7. Blocker

No PixelLab tool is exposed in this session — the harness supplies only the local `pixl-local` MCP
server, so nothing can be submitted, polled or generated remotely. The local capability list is a
dated document, not live discovery. The missing capability is precisely: an authenticated PixelLab
MCP connection exposing `create_1_direction_object` / `get_object`. Until it exists, the honest
options are to hand-author the opaque body locally against section 2, or to hold.
