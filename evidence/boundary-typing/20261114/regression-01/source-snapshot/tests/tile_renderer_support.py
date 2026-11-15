"""Controlled synthetic tile pixels for renderer tests, never art acceptance."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def fixture(root):
    root = Path(root)
    (root / "src").mkdir(parents=True, exist_ok=True)
    (root / "assets/terrain").mkdir(parents=True, exist_ok=True)
    tiles, destinations = {}, {}
    for mask in range(16):
        path = f"assets/terrain/tile-{mask}.png"
        image = Image.new("RGBA", (16, 16))
        # Synthetic quadrant colors encode the declared corners, with partial
        # alpha to exercise real browser compositing independently in Pillow.
        for y in range(16):
            for x in range(16):
                bit = (0 if x < 8 else 1) if y < 8 else (3 if x < 8 else 2)
                image.putpixel((x, y), (62, 176, 110, 210) if mask & (1 << bit) else (24, 62, 106, 255))
        image.save(root / path)
        tiles[str(mask)] = {"path": path}
        destinations[f"terrain.tile{mask}"] = path
    # Separate non-overlapping 2x2 blocks cover every possible corner pattern.
    atlas = [[0] * 9 for _ in range(9)]
    for mask in range(16):
        y, x = mask // 4 * 2, mask % 4 * 2
        for bit, (dy, dx) in enumerate(((0, 0), (0, 1), (1, 1), (1, 0))):
            atlas[y + dy][x + dx] = (mask >> bit) & 1
    terrain = {"tile_size": [16, 16], "background": "#172336", "sampling": "nearest", "corner_order": ["nw", "ne", "se", "sw"], "tiles": tiles,
               "neighborhoods": [{"id": "all-patterns", "label": "Synthetic pattern coverage", "vertices": atlas},
                                 {"id": "island", "label": "Synthetic inner and outer corners", "vertices": [[0,0,0,0,0],[0,1,1,1,0],[0,1,0,1,0],[0,1,1,1,0],[0,0,0,0,0]]}]}
    module = "export const terrain = " + json.dumps(terrain, indent=2) + ";\nexport function tileFor(corners) { return String(corners.reduce((mask, value, bit) => mask + value * 2 ** bit, 0)); }\n"
    (root / "src/terrain.ts").write_text(module, encoding="utf-8")
    config = {"version": 1, "profile": "tile-neighborhood-v1", "modules": {"terrain": "src/terrain.ts"}, "destinations": destinations, "scales": [1, 3], "timeout_seconds": 90}
    write_json(root / "config.json", config)
    (root / "SYNTHETIC-TEST.md").write_text("Synthetic binary quadrant diagnostic pixels; no new art, seam quality or human acceptance is claimed.\n", encoding="utf-8")
    return config
