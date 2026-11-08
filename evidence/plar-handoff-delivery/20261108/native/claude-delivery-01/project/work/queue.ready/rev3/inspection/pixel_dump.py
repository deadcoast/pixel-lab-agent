"""Exact pixel dump of the downloaded Ready candidate (read-only on the source).

Usage: python -I pixel_dump.py SOURCE_PNG OUT_JSON
Writes an RGBA grid, distinct colors, alpha histogram, alpha>0 bounding box,
connected components, and a per-arm geometry description of the check mark.
It never modifies the source and never writes an image.
"""
import hashlib
import json
import sys
from collections import Counter

from PIL import Image


def main(src: str, out: str) -> None:
    data = open(src, "rb").read()
    im = Image.open(src)
    fmt = im.format
    info = dict(im.info)
    n_frames = getattr(im, "n_frames", 1)
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    grid = [[list(px[x, y]) for x in range(w)] for y in range(h)]

    colors = Counter()
    alpha_hist = Counter()
    visible = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            alpha_hist[a] += 1
            if a > 0:
                colors[(r, g, b, a)] += 1
                visible.append((x, y))

    bbox = None
    if visible:
        xs = [p[0] for p in visible]
        ys = [p[1] for p in visible]
        bbox = {"x0": min(xs), "y0": min(ys), "x1": max(xs), "y1": max(ys),
                "width": max(xs) - min(xs) + 1, "height": max(ys) - min(ys) + 1}

    # 8-connected components of alpha>0 pixels
    vis = set(visible)
    seen = set()
    components = []
    for p in visible:
        if p in seen:
            continue
        stack = [p]
        comp = []
        seen.add(p)
        while stack:
            cx, cy = stack.pop()
            comp.append((cx, cy))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    q = (cx + dx, cy + dy)
                    if q in vis and q not in seen:
                        seen.add(q)
                        stack.append(q)
        components.append(sorted(comp))

    # Per-column and per-row occupancy of visible pixels
    col_rows = {x: sorted(y for (xx, y) in visible if xx == x) for x in range(w)}
    col_rows = {x: ys for x, ys in col_rows.items() if ys}
    row_cols = {y: sorted(x for (x, yy) in visible if yy == y) for y in range(h)}
    row_cols = {y: xs for y, xs in row_cols.items() if xs}

    # Vertex = lowest visible row (largest y); the check mark's two arms leave it
    vertex_y = max(y for (_, y) in visible) if visible else None
    vertex_cols = row_cols.get(vertex_y, []) if visible else []
    vertex_x_center = (min(vertex_cols) + max(vertex_cols)) / 2 if vertex_cols else None
    left_arm = [p for p in visible if p[0] < vertex_x_center] if vertex_x_center is not None else []
    right_arm = [p for p in visible if p[0] > vertex_x_center] if vertex_x_center is not None else []
    vertex_px = [p for p in visible if p[0] == vertex_x_center] if vertex_x_center is not None else []

    def arm_stats(arm):
        if not arm:
            return None
        xs = [p[0] for p in arm]
        ys = [p[1] for p in arm]
        return {"pixel_count": len(arm), "x_range": [min(xs), max(xs)], "y_range": [min(ys), max(ys)],
                "horizontal_extent": max(xs) - min(xs) + 1, "vertical_rise": max(ys) - min(ys) + 1}

    # Mirror-symmetry test about the vertex column (exact)
    mirror_symmetric = None
    if vertex_x_center is not None:
        mirrored = {(int(round(2 * vertex_x_center - x)), y) for (x, y) in visible}
        mirror_symmetric = mirrored == vis

    result = {
        "source": {"path": src, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                   "format": fmt, "n_frames": n_frames, "mode_after_convert": "RGBA",
                   "png_text": {k: v for k, v in info.items() if isinstance(v, str)}},
        "size": [w, h],
        "alpha_histogram": {str(k): v for k, v in sorted(alpha_hist.items())},
        "alpha_values_present": sorted(alpha_hist),
        "binary_alpha": set(alpha_hist) <= {0, 255},
        "visible_pixel_count": len(visible),
        "transparent_pixel_count": alpha_hist.get(0, 0),
        "distinct_visible_colors": [{"rgba": list(c), "hex": "#%02x%02x%02x" % c[:3], "count": n}
                                     for c, n in colors.most_common()],
        "bbox_alpha_gt0": bbox,
        "edge_rows_cols_fully_transparent": {
            "top_row": all(px[x, 0][3] == 0 for x in range(w)),
            "bottom_row": all(px[x, h - 1][3] == 0 for x in range(w)),
            "left_col": all(px[0, y][3] == 0 for y in range(h)),
            "right_col": all(px[w - 1, y][3] == 0 for y in range(h)),
        },
        "components_8connected": [{"pixel_count": len(c), "pixels": c} for c in components],
        "column_occupancy": {str(x): ys for x, ys in col_rows.items()},
        "row_occupancy": {str(y): xs for y, xs in row_cols.items()},
        "check_mark_geometry": {
            "vertex_row_y": vertex_y,
            "vertex_row_columns": vertex_cols,
            "vertex_x_center": vertex_x_center,
            "vertex_column_pixels": len(vertex_px),
            "left_arm": arm_stats(left_arm),
            "right_arm": arm_stats(right_arm),
            "exact_mirror_symmetric_about_vertex": mirror_symmetric,
        },
        "rgba_grid_rows": grid,
        "ascii_alpha_map": ["".join("#" if px[x, y][3] == 255 else ("+" if px[x, y][3] > 0 else ".") for x in range(w)) for y in range(h)],
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1)
    print(json.dumps({k: v for k, v in result.items() if k not in ("rgba_grid_rows", "components_8connected", "column_occupancy", "row_occupancy")}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
