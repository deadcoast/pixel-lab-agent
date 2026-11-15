# Creative brief: scout sample (not an executable provider request)

No PixelLab connection is assigned in this evaluation, so no tool schema was
discovered and no provider arguments exist. This brief is the translation of the
saved contract (`.pixl/characters`, task `scout_sample`, output `scout_sprite`) for
whoever prepares the real request once a connection is available. Discover the
actual tool declaration first; nothing below infers a parameter.

## Candidate operations to discover

- A freeform image tool (Pixflux / Pixen / Pro) with a style image input, generating
  one 32x32 image. Likely the best fit for a single static side-view sprite at native
  canvas; check whether the tool accepts 32x32 and a style-reference image.
- `create_character` if a reusable character identity with later states or
  animation is wanted. Check its native canvas and direction set; a side-view-only
  single pose may be more than it offers or less than it forces.

## Reference transport

- `reference.png` (sha256 d997cade…70aa7), role: style. Preserve: continuous dark
  outline (#25354a, 2 px in the reference), flat teal fill (#56b5bc), cream accents
  (#f4dda2), blocky cluster scale, no anti-aliasing.
- `reference-b.png` (sha256 e76b40ce…a12a), role: palette only.
- Optional: `candidates/scout-local-01.png`, role: pose/layout. A deterministic
  local construction (not generated) showing the proposed side-view layout:
  ears set back, eye and muzzle at the front, backpack on the back, feet on row 29.

Upload actual bytes through the tool's supported handle mechanism; a filename in
the prompt does not transmit the image.

## Prompt content (owner requirements first, then proposals)

Owner requirements: 32x32 canvas; side view; continuous dark outline like the
reference; teal body with cream accents; binary transparency (transparent
background, no semi-transparent pixels); intended for nearest-neighbor display.

PIXL proposals (confirm with the owner before production): flat fill with no
shading ramps; exact colors #56b5bc / #f4dda2 / #25354a; single standing pose facing
screen right; the scout is the same blocky two-eared creature as the reference seen
from the side, with a backpack on its back and a cream goggle strap running to its
eye.

## Acceptance after generation

The saved criteria on `scout_sprite` apply: canvas and binary alpha (local),
working-palette membership (local), continuous outline, side view, scout
readability and reference style match (all visual, native and 8x, light and dark
backgrounds). Provider output with anti-aliased edges or extra colors would need
`reduce_colors` / `correct_pixelart` style cleanup or a revised candidate; do not
relax the criteria to fit the output.
