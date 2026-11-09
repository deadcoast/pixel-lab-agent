"""Caller's independent measurements of the actual art (not copied from the specialist).

Zero-based pixel indices; component boxes half-open [left, top, right, bottom]; 4-connectivity on alpha > 0.
Writes work/continuation/caller-measurements.json. Reads only; writes nothing else.
Usage: python -I work/continuation/caller_measure.py
"""
from __future__ import annotations

import hashlib
import json
import os

from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
OUT = "work/continuation/caller-measurements.json"


def sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def pixels(img):
    w, h = img.size
    px = img.load()
    return {(x, y): px[x, y] for y in range(h) for x in range(w)}


def components(img):
    w, h = img.size
    px = img.load()
    seen, out = set(), []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] > 0 and (x, y) not in seen:
                stack, pts = [(x, y)], []
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    pts.append((cx, cy))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and px[nx, ny][3] > 0:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                out.append({"pixels": len(pts), "box": [min(xs), min(ys), max(xs) + 1, max(ys) + 1],
                            "touches_all_four_edges": min(xs) == 0 and min(ys) == 0 and max(xs) == w - 1 and max(ys) == h - 1})
    return out


def alpha_histogram(img):
    hist = {}
    for p in pixels(img).values():
        hist[str(p[3])] = hist.get(str(p[3]), 0) + 1
    return dict(sorted(hist.items()))


def visible(img):
    return {k: v for k, v in pixels(img).items() if v[3] > 0}


def rotate_cw(img):
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    w, h = img.size
    for y in range(h):
        for x in range(w):
            out.putpixel((x, y), img.getpixel((y, h - 1 - x)))  # dst(x,y) = src(y, 15-x)
    return out


def centroid(img):
    vis = visible(img)
    n = len(vis)
    return [round(sum(x for x, _ in vis) / n + 0.5, 3), round(sum(y for _, y in vis) / n + 0.5, 3)]


result = {"convention": "zero-based pixel indices; boxes half-open [left,top,right,bottom]; centroids in pixel-edge coordinates (index centroid + 0.5); 4-connectivity on alpha>0"}
sheet_path = "assets/working.png"
sheet = Image.open(sheet_path).convert("RGBA")
cells = [sheet.crop((i * 16, 0, (i + 1) * 16, 16)) for i in range(4)]
rot = cells[0]
equal = []
for k in range(1, 4):
    rot = rotate_cw(rot)
    equal.append(visible(rot) == visible(cells[k]) and alpha_histogram(rot) == alpha_histogram(cells[k]) and [p[3] for p in pixels(rot).values()] == [p[3] for p in pixels(cells[k]).values()])
colors = {}
for p in visible(sheet).values():
    colors[p] = colors.get(p, 0) + 1
result["working"] = {
    "path": sheet_path, "sha256": sha(sheet_path), "size": list(sheet.size),
    "visible_pixels": len(visible(sheet)), "visible_colors": len(colors),
    "fractional_alpha_pixels": sum(1 for p in pixels(sheet).values() if 0 < p[3] < 255),
    "cells": [{"index": i, "alpha_histogram": alpha_histogram(c), "components": components(c), "centroid": centroid(c)} for i, c in enumerate(cells)],
    "cells_1_to_3_equal_cw_k_of_cell_0_on_alpha_and_visible_rgba": equal,
}
seed_path = ".pixl/assets/queue.ready/artifacts/21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png"
seed = Image.open(seed_path).convert("RGBA")
result["seed"] = {"path": seed_path, "sha256": sha(seed_path), "size": list(seed.size), "cell_0_equals_seed_on_alpha_and_visible_rgba": visible(seed) == visible(cells[0]) and alpha_histogram(seed) == alpha_histogram(cells[0])}
for name in ["ready-confirmed", "paused", "error-retry"]:
    path = f"assets/{name}.png"
    img = Image.open(path).convert("RGBA")
    result[name] = {"path": path, "sha256": sha(path), "size": list(img.size), "alpha_histogram": alpha_histogram(img), "components": components(img), "centroid": centroid(img),
                    "fractional_alpha_pixels": sum(1 for p in pixels(img).values() if 0 < p[3] < 255)}
result["start_svg"] = {"path": "assets/start.svg", "sha256": sha("assets/start.svg"), "note": "vector; rasterised by the browser in the fixture; not measured here"}
result["state_px_candidate_line_259_dg"] = "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc"
result["reuse_provenance_matches"] = result["working"]["sha256"] == result["state_px_candidate_line_259_dg"]
with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
    json.dump(result, handle, indent=1)
    handle.write("\n")
print(json.dumps({"out": OUT, "sha256": sha(OUT), "cells_equal": equal, "cell0_equals_seed": result["seed"]["cell_0_equals_seed_on_alpha_and_visible_rgba"], "provenance": result["reuse_provenance_matches"]}))
