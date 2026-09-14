"""Author the translucent side glow deterministically from an opaque sprite body.

The reference's partial transparency is a rule, not a painted texture: for every
row that contains glass, one pixel of glass colour is placed immediately outside
the opaque silhouette on each side, at a per-side alpha level. Generating the
fringe here (rather than asking an image model for it) is what keeps the alpha
levels exact and the RGB constant.

Usage:
    python tools/apply_glow_fringe.py CONTRACT.json IN.png OUT.png

Pixels already carrying fractional alpha in IN.png are cleared first, so the
script is idempotent and can re-derive the fringe after a body edit.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image


def parse_rgb(value: str) -> tuple[int, int, int]:
    text = value.lstrip("#")
    return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def apply_fringe(contract: dict, source: Image.Image) -> Image.Image:
    glow = contract["glow"]
    glass_rgb = parse_rgb(glow["rgb"])
    left_alpha = glow["left_alpha"]
    right_alpha = glow["right_alpha"]
    trigger_rgb = {parse_rgb(entry) for entry in glow["trigger_rgb"]}

    out = source.convert("RGBA").copy()
    width, height = out.size
    pixels = out.load()

    # Start from the opaque body only.
    for y in range(height):
        for x in range(width):
            if 0 < pixels[x, y][3] < 255:
                pixels[x, y] = (0, 0, 0, 0)

    for y in range(height):
        opaque_x = [x for x in range(width) if pixels[x, y][3] == 255]
        if not opaque_x:
            continue
        row_has_glass = any(pixels[x, y][:3] in trigger_rgb for x in opaque_x)
        if not row_has_glass:
            continue
        left = min(opaque_x) - 1
        right = max(opaque_x) + 1
        if left >= 0 and pixels[left, y][3] == 0:
            pixels[left, y] = (*glass_rgb, left_alpha)
        if right < width and pixels[right, y][3] == 0:
            pixels[right, y] = (*glass_rgb, right_alpha)
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__.strip())
        return 2
    contract = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    result = apply_fringe(contract, Image.open(argv[2]))
    result.save(argv[3])
    print(json.dumps({"input": argv[2], "output": argv[3], "contract": contract.get("name")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
