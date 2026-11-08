# Drone production approach (planning only)

Status: a planning document. It does not initialize or change PX2 state, create art, call a provider, or accept anything for production.

## 1. Inputs reviewed

| Input | Identity | How it was used |
| --- | --- | --- |
| `small-separated.png` | sha256 `1c45c866f9d11ff57b055f4dacf1e47c8e71f2c99fd6b24f0cb4259ee40cbe5c` | Measured with `pixl_asset_check`, dumped per pixel, and viewed in the host |
| `old-assessment.md` | An earlier agent's diagnostic. Not approved by the owner. | Checked against the authority rules and the measurements below (§4) |
| PIXL skill references | `artistic-authority.md`, `intake-sample.md`, `pixellab-operations.md` | Method guidance only. These references don't establish a project style. |

### Reference measurements (observations, not rules)

```
................   y0
................   y1
.....AA..AA.....   y2   A = (37,53,74)    dark frame / antennae
.....AA..AA.....   y3   B = (86,181,188)  teal body
................   y4   C = (244,221,162) cream eyes
................   y5
...AAAAAAAAAA...   y6
...AAAAAAAAAA...   y7
...AABBBBBBAA...   y8
...AABCBBCBAA...   y9
...AABBBBBBAA...   y10
...AABBBBBBAA...   y11
...AAAAAAAAAA...   y12
...AAAAAAAAAA...   y13
................   y14
................   y15
```

- Canvas 16×16, one frame. 88 visible pixels, binary alpha (0 fractional-alpha pixels), visible bbox `[3,2,13,14]`.
- 3 opaque colors. 3 opaque components (4-connectivity): the body and two antenna islands.
- Body: a 10×8 block at x3–12, y6–13 with a 2-px dark frame on all sides. The teal interior is 6×4 (x5–10, y8–11).
- Eyes: single cream pixels at (6,9) and (9,9). Teal separates each eye from the frame on every side, so the eyes **do not touch the contour** in this drone.
- Antennae: two 2×2 dark islands at x5–6 and x9–10, y2–3. Each is separated from the body by a 2-row transparent gap (y4–5) and from the other by a 2-column gap (x7–8).
- The frame and antennae share color A. No separate outline color.
- Host view: the image reads as a small boxy teal drone with two eyes and floating antenna nodes. Its readability at 1× in-game size, against the game's actual backgrounds, has **not** been checked.

## 2. Authority table

| Property / value | Status | Source | Scope |
| --- | --- | --- | --- |
| Canvas 16×16 | **Requirement** | User: "a 16 by 16 canvas … Keep those choices" | Every drone deliverable in this approach |
| Thick 2-px dark frame around the teal body | **Requirement** | User: "a thick two-pixel dark frame around the teal body" | Body contour of the drone |
| Teal body | **Requirement** (qualitative hue family only) | User: "the teal body" | Body interior. No numeric hue threshold is adopted. |
| Two detached antenna islands | **Requirement** | User: "two detached antenna islands" | Antennae. This means exactly two antenna pieces, each not 4-connected to the body. It does **not** forbid other intentional detached details or fix their coordinates, size, or gap width. |
| Fixed palette | **Unresolved. Not approved.** | User: "I have not approved a fixed palette" | No palette-membership check in production. The 3 measured colors are observations. |
| Exact colors A/B/C | Observation | Reference pixels | Can serve as a starting suggestion or a labeled palette experiment |
| Total component count = 3 | Observation | Reference measurement | Not a rejection rule |
| Antenna size 2×2, gap 2 rows, positions | Observation | Reference measurement | Not a rejection rule |
| Eyes: two 1-px cream pixels on the teal | Observation | Reference pixels | Matching proposal. The face design is still open. |
| Binary alpha, no anti-aliasing | Observation | Reference measurement (0 fractional pixels) | Alpha policy is **not adopted**. Proposal: keep binary alpha to match the reference. The owner can confirm or change this. |
| Frame color = antenna color | Observation | Reference pixels | Proposal for consistency, not a rule |
| Universal 32-px minimum for thick outlines | **Rejected as a project rule** | `old-assessment.md` (unapproved, different robot) | Not applicable (see §4) |
| One connected component for all sprites | **Rejected. Contradicts a requirement.** | `old-assessment.md` | Not applicable (see §4) |
| Lock all props to the observed 3 colors | **Rejected as a rule** | `old-assessment.md`. Conflicts with "no fixed palette approved." | Optional palette experiment at most |

## 3. Production approach

### 3.1 Deliverable and operation

- One 16×16 drone sprite, a single frame, generated at **native 16×16**. Don't generate large and downscale. A nearest-neighbor resize is a different method and isn't equivalent pixel art (see §4).
- Operation: a small standalone sprite, so discover the connected PixelLab freeform image tools (e.g., Pixen / Pixflux / Pro or Pro Flash). Before choosing one, confirm from the live tool declaration that it supports a 16×16 output and accepts an image reference. If no connected tool offers a native 16×16 canvas, that is a verified tool limitation to report, and the next decision goes back to the owner. Don't silently change the canvas.
- Reference role: `small-separated.png` is the **style + identity** reference (frame thickness, body proportion, antenna treatment). Send it through the tool's real image input (upload handle / URL / encoded payload). A filename in the prompt text doesn't transmit an image. Record the local hash, the returned handle, and the request field.
- Request one output unless the owner wants a candidate grid.

### 3.2 Draft provider prompt (for when a provider call is authorized)

Requirements (from the user):
> 16×16 pixel-art drone. Teal body enclosed by a thick, two-pixel-wide dark frame on all sides. Two separate antenna pieces, each detached from the body with transparent pixels in between. Match the reference image's style.

Proposals (labeled, can be removed; the owner hasn't adopted any of them; these come from reference observations):
> *[proposal]* Front view, transparent background. *[proposal]* Boxy/rectangular body. *[proposal]* Antennae floating above the body. *[proposal]* Two small light eyes on the teal face. *[proposal]* Hard-edged pixels, no anti-aliasing / no semi-transparent pixels. *[proposal]* Antennae in the same dark color as the frame.

No palette lock and no hex colors in the production prompt. The colors come from the style reference. An exact-palette version is only the optional experiment in §3.4.

### 3.3 Acceptance checks for the representative sample

Mechanical (tool-measurable, e.g., `pixl_asset_check` with `width:16,height:16`):
1. The output is exactly 16×16, one frame. *(requirement: canvas)*
2. The body contour is 2 px thick and dark around the whole teal interior. Check by per-pixel inspection of every edge of the body: 2 dark pixels before the teal starts, with no 1-px thinning or gaps. *(requirement: frame)*
3. Exactly two antenna islands exist, and neither is 4-connected to the body. Check with component analysis plus visual identification of which components are the antennae. *(requirement: antennae)*. Other detached components are not an automatic failure. Flag them for visual review.

Visual (host viewing at native and integer-nearest zoom, e.g., 1× and 8×):
4. The body reads as teal (qualitative, judged by eye, no numeric threshold). *(requirement: teal)*
5. It reads as a drone and its features stay legible at 16 px. *(visual judgment. Reported as an opinion, not a measured pass.)*

Reported, not used for rejection: palette size and colors, alpha policy, total component count, eye design, antenna dimensions/gap, similarity to reference coordinates.

Not covered here: engine import and in-game background contrast. No destination engine was given, so these stay unverified.

### 3.4 Optional, separately labeled experiments

These are not production rules. Run them only if the owner wants them.

- **Palette experiment:** constrain to the observed A/B/C colors and compare with the unconstrained result. Its outcome informs a palette decision. It doesn't make that decision.
- **Alpha experiment:** confirm whether the owner wants strictly binary alpha (the reference is binary).

### 3.5 Fallbacks

- If a candidate fails check 2 or 3, retain it as a failed attempt. That shows only that this attempt failed, not that the provider can't do it. Next steps, in order: (a) edit/inpaint the failing region on that candidate with a mask, (b) retry with a stronger reference weighting, (c) as a last resort, hand-author or hand-repair at 16×16. The reference already shows that this design fits on the canvas.
- Keep every changed requirement for the owner to decide (e.g., if 16×16 proves unworkable in a tool, offer options rather than switching to 32).

## 4. Review of the earlier assessment (`old-assessment.md`)

That assessment came from a **different robot**, a **32-px source nearest-neighbor-resized to 16**, with no measurement of this drone and no owner adoption. Its conclusions apply only to that artifact and method.

| Old claim | Finding on this drone | Disposition |
| --- | --- | --- |
| A 2-px inset border consumed most of the interior, and the eyes met the contour | Here the teal interior is 6×4 and both eyes have teal between them and the frame. The design fits at native 16 px. | Doesn't apply. The failure belonged to a downscaled fixture. |
| Universal 32-px minimum for thick outlines | Contradicts the user's 16×16 requirement. One resized fixture can't establish a universal minimum. | Not adopted |
| One connected component for all sprites | Contradicts the required two detached antenna islands | Not adopted |
| Lock all props to the observed 3 colors | The user hasn't approved a fixed palette. Measured colors are observations. | Not adopted. At most the §3.4 palette experiment. |

The one transferable lesson: generate at native 16×16 rather than downscaling from 32.

## 5. Open decisions for the owner

1. **Palette**: leave it open (the default in this plan), or run or adopt the A/B/C palette experiment?
2. **Alpha policy**: confirm binary alpha / no anti-aliasing (proposed, matching the reference), or leave it open.
3. **Authorization to proceed**: when you're ready, authorize one native 16×16 representative sample through a connected PixelLab tool. That step would also start PX2 intake to record the requirements above. Neither was done in this session.

## 6. Whole-file audit (performed after saving)

- Prompt (§3.2): its requirement sentences map only to canvas, frame, teal, and two detached antennae. The first draft put "front view," "boxy," "transparent background," and antennae "above" the body under requirements. The audit moved them to labeled proposals because they're reference observations, not user choices. Eyes, hard edges, and antenna color are also labeled `[proposal]` at the prompt itself. No palette or hex lock.
- Rejection checks (§3.3): checks 1–4 each trace to a user requirement. Check 5 is reported as an opinion. Palette, alpha, component total, and gaps are explicitly excluded from rejection.
- Fallbacks (§3.5): they're scoped to the failed attempt. No universal provider or canvas claims.
- No "approved," "binding," or "must" language is attached to observed or proposed items. The old assessment's restrictions are all marked as not adopted.
- Unresolved: palette, alpha policy, engine/destination behavior, and provider tool availability for native 16×16 (not yet discovered this session).
