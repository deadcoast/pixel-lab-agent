# Draft PixelLab request for f.sprite

Recorded 2026-09-11 by PIXL. **This is a draft, not saved provider intent.** No `J` record
exists in `.pixl/state.px`, because `job-prepare` requires the exact `inputSchema` observed
from a connected PixelLab server, and no such server is connected in this session
(see `pixellab-discovery.md`). Saving this text as a prepared request would fabricate a
discovery observation, which the provider operation forbids.

When a PixelLab MCP server is connected, the operator should re-run discovery, read the
actual tool list and `inputSchema`, adjust the argument names below to match what the
schema really accepts, and only then run `job-prepare` / `job-dispatch`.

## Tool selection (to be re-confirmed against the live schema)

The dated documentation snapshot lists several generation entry points. Ranked for this
task:

1. **`create_image_pixflux` / `create_image_pixen`** — documented as requiring
   `description`, polled with `get_image`. A direct single-image generator is the closest
   match for one 32x32 still at a fixed size.
2. **`create_character`** — documented as requiring `description`, polled with
   `get_character`. Preferable only if the later family expansion turns out to be
   animation or directional states, because a character resource carries those forward.
3. **`image_to_pixelart`** — only relevant if the operator would rather supply a
   higher-resolution source image than a text description.

`i.family_scope` is unresolved, so the choice between 1 and 2 cannot be settled yet. If the
owner's family is poses or directions of this same robot, option 2 avoids regenerating the
identity for every member.

## Description to send

> 32x32 pixel art sprite of a small teal scout robot, side view, standing upright.
> Rectangular boxy body, flat teal #56B5BC fill with no shading, gradients or dithering.
> Uniform dark navy #25354A outline around the whole silhouette. Two straight antennae
> rising from the top of the head, drawn in the same dark navy as the outline, with a gap
> between them. Two pale yellow #F4DDA2 rectangular eyes, both visible, no pupils, no eye
> outline. Exactly three colours total. Fully transparent background, hard edges, no
> anti-aliasing, no ground shadow, no drop shadow, no floor or contact shading, no
> background scenery.

## Parameters to set if the live schema exposes them

| Intent | Parameter to look for | Value |
| --- | --- | --- |
| Canvas | `image_size` / `width` + `height` | 32 x 32 |
| Style reference | `style_image` / `init_image` / `reference` | `reference.png` |
| Palette lock | `forced_palette` / `palette` / `color_palette` | `#25354A`, `#56B5BC`, `#F4DDA2` |
| Outline policy | `outline` | a single hard dark outline |
| Shading policy | `shading` / `detail` | flat, no shading |
| View | `view` / `camera` | side |
| Transparency | `transparent` / `no_background` | on |

## Requirements the tool may not be able to express

State these in the prepared request so the acceptance step knows what is untested at
submission time:

- **Exact three-colour palette.** If no palette parameter exists, the returned PNG will
  almost certainly carry extra anti-aliasing and shading colours. `q.palette` will fail and
  the candidate must be revised or quantised with a follow-up tool (the snapshot documents
  `reduce_colors` and `correct_pixelart` for this) rather than accepted.
- **Binary alpha.** Generators commonly return soft alpha at the silhouette edge.
  `q.alpha` will catch it.
- **Two eyes in a side view.** `i.eye_presentation` is only a proposal. A returned profile
  head with one eye fails `q.identity` and must be reported to the owner rather than
  silently accepted.
- **No ground shadow.** Frequently added by default; `q.identity` checks for it visually
  and the connected-component count in the harness receipt helps spot a detached blob.

## After a returned asset

1. Download into the project, then `job-import` to snapshot the bytes as a candidate of
   `f.sprite`.
2. `python tools/check_sprite.py <candidate> --out work/receipt.json --sheet work/sheet.png`
   for `q.canvas`, `q.palette`, `q.alpha` and `q.nearest`.
3. Actually look at `work/sheet.png` and record `q.identity` as pass or fail.
4. `q.webdisplay` stays unavailable until `i.web_prototype` is resolved.
