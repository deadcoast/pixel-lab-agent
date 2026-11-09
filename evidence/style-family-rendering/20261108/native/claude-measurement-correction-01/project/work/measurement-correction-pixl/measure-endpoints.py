"""Deterministic measurement of assets/ready-confirmed.png for the arm-axis correction.

Reads ONLY the PNG (path given as argv[1], default assets/ready-confirmed.png
relative to the consumer root two directories above this file). Prints one JSON
object to stdout. No other file is read or written.

Coordinate convention (identical to the quoted claims in
work/queue.ready-reassessment/art-assessment.json lines 21, 51-54):
  zero-based pixel indices, x increases to the right, y increases DOWNWARD
  (screen convention). A point (x, y) names the pixel in column x, row y.
  Boxes are [left, top, right, bottom] with exclusive right/bottom.
  Angles are measured from the +x (horizontal) axis; because y points down, a
  positive angle means the segment DESCENDS to the right on screen and a
  negative angle means it ASCENDS to the right.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
DEFAULT_PNG = os.path.join(ROOT, "assets", "ready-confirmed.png")

ACCENT = (112, 185, 237, 255)  # #70b9ed


def r(v: float, nd: int = 3) -> float:
    return round(v + 0.0, nd)


def seg(p: tuple[int, int], q: tuple[int, int]) -> dict:
    dx, dy = q[0] - p[0], q[1] - p[1]
    length = math.hypot(dx, dy)
    ang = math.degrees(math.atan2(dy, dx))
    return {
        "from": list(p),
        "to": list(q),
        "delta": [dx, dy],
        "length": r(length),
        "length_exact": f"sqrt({dx * dx + dy * dy})",
        "angle_from_horizontal_deg_screen": r(ang),
        "screen_direction": (
            "descends to the right" if dy > 0 and dx > 0 else
            "ascends to the right" if dy < 0 and dx > 0 else
            "descends to the left" if dy > 0 and dx < 0 else
            "ascends to the left" if dy < 0 and dx < 0 else
            "horizontal" if dy == 0 else "vertical"
        ),
        "is_exact_45_degree": abs(abs(dx) - abs(dy)) == 0 and dx != 0,
        "row_steps": abs(dy),
        "column_steps": abs(dx),
    }


def interior_angle(vertex, a, b) -> float:
    va = (a[0] - vertex[0], a[1] - vertex[1])
    vb = (b[0] - vertex[0], b[1] - vertex[1])
    dot = va[0] * vb[0] + va[1] * vb[1]
    na = math.hypot(*va)
    nb = math.hypot(*vb)
    return math.degrees(math.acos(dot / (na * nb)))


def runs_in_row(cols: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    for c in cols:
        if out and c == out[-1][1] + 1:
            out[-1][1] = c
        else:
            out.append([c, c])
    return out


def principal_axis(points: list[tuple[int, int]]) -> dict:
    """Least-squares (PCA) line through pixel centres; returns angle and extent."""
    n = len(points)
    mx = sum(p[0] for p in points) / n
    my = sum(p[1] for p in points) / n
    sxx = sum((p[0] - mx) ** 2 for p in points) / n
    syy = sum((p[1] - my) ** 2 for p in points) / n
    sxy = sum((p[0] - mx) * (p[1] - my) for p in points) / n
    # orientation of the major eigenvector
    theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
    ux, uy = math.cos(theta), math.sin(theta)
    proj = [(p[0] - mx) * ux + (p[1] - my) * uy for p in points]
    extent = max(proj) - min(proj)
    return {
        "pixel_count": n,
        "centroid_pixel_index": [r(mx), r(my)],
        "direction_unit_vector": [r(ux), r(uy)],
        "angle_from_horizontal_deg_screen": r(math.degrees(theta)),
        "angle_magnitude_deg": r(abs(math.degrees(theta))),
        "projected_extent_px": r(extent),
    }


def bbox(points: list[tuple[int, int]]) -> list[int]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return [min(xs), min(ys), max(xs) + 1, max(ys) + 1]


def main() -> None:
    png_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PNG
    with open(png_path, "rb") as fh:
        data = fh.read()
    sha = hashlib.sha256(data).hexdigest()
    im = Image.open(png_path).convert("RGBA")
    w, h = im.size
    px = im.load()

    opaque: list[tuple[int, int]] = []
    colours: dict[str, int] = {}
    alphas: set[int] = set()
    for y in range(h):
        for x in range(w):
            c = px[x, y]
            alphas.add(c[3])
            if c[3] != 0:
                opaque.append((x, y))
                key = "#%02x%02x%02x a%d" % c
                colours[key] = colours.get(key, 0) + 1
    opaque_set = set(opaque)

    pixel_map = [
        "".join("#" if (x, y) in opaque_set else "." for x in range(w)) for y in range(h)
    ]
    ruler = "".join(str(x % 10) for x in range(w))

    # 4-connected components
    seen: set[tuple[int, int]] = set()
    components = 0
    for p in opaque:
        if p in seen:
            continue
        components += 1
        stack = [p]
        seen.add(p)
        while stack:
            cx, cy = stack.pop()
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                q = (nx, ny)
                if q in opaque_set and q not in seen:
                    seen.add(q)
                    stack.append(q)

    rows: dict[int, list[int]] = {}
    for x, y in opaque:
        rows.setdefault(y, []).append(x)
    row_table = []
    for y in sorted(rows):
        cols = sorted(rows[y])
        rr = runs_in_row(cols)
        row_table.append({
            "row": y,
            "runs_inclusive": rr,
            "run_lengths": [b - a + 1 for a, b in rr],
            "run_centres_x": [r((a + b) / 2, 1) for a, b in rr],
            "left_edge": cols[0],
            "right_edge": cols[-1],
        })

    # What the quoted endpoints are
    quoted = {"left_tip": (4, 8), "vertex": (6, 12), "right_tip": (12, 4)}
    endpoint_identity = {}
    for name, (x, y) in quoted.items():
        cols = sorted(rows.get(y, []))
        rr = runs_in_row(cols)
        own_run = next((run for run in rr if run[0] <= x <= run[1]), None)
        below = sorted(rows.get(y + 1, []))
        above = sorted(rows.get(y - 1, []))
        endpoint_identity[name] = {
            "point_xy": [x, y],
            "opaque": (x, y) in opaque_set,
            "run_containing_point_inclusive": own_run,
            "run_length": (own_run[1] - own_run[0] + 1) if own_run else 0,
            "runs_in_row_above": runs_in_row(above),
            "runs_in_row_below": runs_in_row(below),
        }

    # Quoted polyline computations
    left_seg = seg(quoted["left_tip"], quoted["vertex"])
    right_seg = seg(quoted["vertex"], quoted["right_tip"])
    ratio = right_seg["length"] / left_seg["length"]
    quoted_polyline = {
        "left_arm_tip_to_vertex": left_seg,
        "vertex_to_right_arm_tip": right_seg,
        "length_ratio_right_over_left": r(ratio),
        "length_ratio_exact": "10 / sqrt(20) = sqrt(5)",
        "interior_angle_at_vertex_deg": r(interior_angle(quoted["vertex"], quoted["left_tip"], quoted["right_tip"])),
        "supports_exact_45_degree_axes": left_seg["is_exact_45_degree"] and right_seg["is_exact_45_degree"],
        "supports_4_to_8_steps_along_axes": False,
        "supports_about_1_to_2_length_ratio": abs(ratio - 2.0) < 0.1,
        "ratio_difference_from_2": r(ratio - 2.0),
    }

    # Partitions by column (the old 7 / 3 / 19 split)
    left_part = [p for p in opaque if p[0] <= 5]
    mid_part = [p for p in opaque if p[0] == 6]
    right_part = [p for p in opaque if p[0] >= 7]
    partition = {
        "rule": "x <= 5 | x == 6 | x >= 7 (column ranges only; not a geometric arm model)",
        "counts": [len(left_part), len(mid_part), len(right_part)],
        "left_bbox_exclusive": bbox(left_part),
        "left_bbox_size": [bbox(left_part)[2] - bbox(left_part)[0], bbox(left_part)[3] - bbox(left_part)[1]],
        "mid_pixels": sorted(mid_part, key=lambda p: p[1]),
        "right_bbox_exclusive": bbox(right_part),
        "right_bbox_size": [bbox(right_part)[2] - bbox(right_part)[0], bbox(right_part)[3] - bbox(right_part)[1]],
    }

    # Row/column extents measured tip to vertex (what '4 steps' and '8 steps' are)
    extents = {
        "left_arm_rows_tip_to_vertex": [8, 12],
        "left_arm_row_extent": 12 - 8,
        "left_arm_columns_tip_to_vertex": [4, 6],
        "left_arm_column_extent": 6 - 4,
        "right_arm_rows_tip_to_vertex": [4, 12],
        "right_arm_row_extent": 12 - 4,
        "right_arm_columns_tip_to_vertex": [12, 6],
        "right_arm_column_extent": 12 - 6,
        "row_extent_ratio": "4 : 8 = 1 : 2 (exact, but these are vertical row spans, not 45-degree axis lengths)",
        "column_extent_ratio": "2 : 6 = 1 : 3",
        "if_axes_were_45_degrees": "a 45-degree segment spanning 4 rows would also span 4 columns (length 4*sqrt(2) = 5.657) and one spanning 8 rows would span 8 columns (length 11.314); the quoted endpoints span 2 and 6 columns instead",
    }

    # Contour staircase checks (one column per row?)
    def edges(part_rows: list[int], side: str) -> list[int]:
        out = []
        for y in part_rows:
            cols = sorted(rows[y])
            out.append(cols[0] if side == "left" else cols[-1])
        return out

    def one_step_per_row(vals: list[int]) -> bool:
        return all(abs(b - a) == 1 for a, b in zip(vals, vals[1:]))

    def monotonic(vals: list[int]) -> bool:
        diffs = [b - a for a, b in zip(vals, vals[1:])]
        return all(d > 0 for d in diffs) or all(d < 0 for d in diffs)

    # outer contours: left arm's left edge rows 9..12, right arm's right edge rows 5..12
    left_outer = edges(list(range(9, 13)), "left")
    right_outer = edges(list(range(5, 13)), "right")
    left_outer_with_cap = edges(list(range(8, 13)), "left")
    right_outer_with_cap = edges(list(range(4, 13)), "right")
    # inner contours: right arm's left edge rows 5..9; left arm's right edge rows 9..9 (one row only)
    right_inner = [sorted(rows[y])[0] for y in range(5, 10)]  # left edge of right-arm run rows 5..9 (left arm absent in rows 5..7, present rows 8,9 -> take right-arm run)
    right_inner = [runs_in_row(sorted(rows[y]))[-1][0] for y in range(5, 10)]
    right_inner_with_cap = [runs_in_row(sorted(rows[y]))[-1][0] for y in range(4, 10)]
    contours = {
        "left_arm_left_edge_rows_8_to_12": left_outer_with_cap,
        "left_arm_left_edge_rows_9_to_12_one_step_per_row": one_step_per_row(left_outer),
        "left_arm_left_edge_rows_9_to_12_monotonic": monotonic(left_outer),
        "left_arm_left_edge_including_cap_row_8_one_step_per_row": one_step_per_row(left_outer_with_cap),
        "left_arm_left_edge_including_cap_row_8_monotonic": monotonic(left_outer_with_cap),
        "right_arm_right_edge_rows_4_to_12": right_outer_with_cap,
        "right_arm_right_edge_rows_5_to_12_one_step_per_row": one_step_per_row(right_outer),
        "right_arm_right_edge_rows_5_to_12_monotonic": monotonic(right_outer),
        "right_arm_right_edge_including_cap_row_4_one_step_per_row": one_step_per_row(right_outer_with_cap),
        "right_arm_right_edge_including_cap_row_4_monotonic": monotonic(right_outer_with_cap),
        "right_arm_left_edge_rows_4_to_9": right_inner_with_cap,
        "right_arm_left_edge_rows_4_to_9_one_step_per_row": one_step_per_row(right_inner_with_cap),
        "right_arm_left_edge_rows_4_to_9_monotonic": monotonic(right_inner_with_cap),
        "reading": "Between the single-pixel caps and the merge, the stroke contours advance exactly one column per row in one direction (monotonic), i.e. the 3-pixel-run staircases are built on 45-degree diagonals. At each cap the outer edge reverses direction by one column (left edge 4 -> 3 -> 4 ..., right edge 12 -> 13 -> 12 ...) because the cap sits directly above the centre of the adjacent 3-pixel run; a straight line through a cap and the vertex pixel is therefore NOT a 45-degree line.",
    }

    # Alternative centreline estimates (explicitly different measurements)
    def centre(y: int, which: int) -> tuple[float, float]:
        rr = runs_in_row(sorted(rows[y]))
        a, b = rr[which]
        return ((a + b) / 2, float(y))

    def fseg(p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        return {
            "from": [r(p[0], 1), r(p[1], 1)],
            "to": [r(q[0], 1), r(q[1], 1)],
            "delta": [r(dx, 1), r(dy, 1)],
            "length": r(math.hypot(dx, dy)),
            "angle_from_horizontal_deg_screen": r(math.degrees(math.atan2(dy, dx))),
        }

    # A: run centres of the 3-pixel runs, excluding the single-pixel caps and the merged rows
    left_a = fseg(centre(9, 0), centre(11, 0))          # (4,9) -> (6,11)
    right_a = fseg(centre(5, 0), centre(11, 0))         # (12,5) -> (6,11)
    alt_a = {
        "definition": "straight line through the centres of 3-pixel runs only: left arm row 9 run [3,5] centre (4,9) to row 11 run [5,7] centre (6,11); right arm row 5 run [11,13] centre (12,5) to the same row 11 centre (6,11). Excludes the single-pixel caps (4,8), (12,4) and (6,12) and the merged 5-pixel row 10.",
        "left": left_a,
        "right": right_a,
        "ratio_right_over_left": r(right_a["length"] / left_a["length"]),
    }
    # B: outer contours tip-of-staircase to vertex pixel
    left_b = seg((3, 9), (6, 12))
    right_b = seg((13, 5), (6, 12))
    alt_b = {
        "definition": "outer contour staircases: left arm's left edge from (3,9) to the vertex pixel (6,12); right arm's right edge from (13,5) to (6,12). Caps excluded.",
        "left": left_b,
        "right": right_b,
        "ratio_right_over_left": r(right_b["length"] / left_b["length"]),
    }
    # C: PCA axis through each column partition
    alt_c = {
        "definition": "least-squares principal axis through the pixel centres of each column partition (x<=5 and x>=7); the shared column 6 excluded. This is a statistical fit, not the quoted tip-to-tip line.",
        "left_partition": principal_axis(left_part),
        "right_partition": principal_axis(right_part),
    }
    alt_c["extent_ratio_right_over_left"] = r(
        alt_c["right_partition"]["projected_extent_px"] / alt_c["left_partition"]["projected_extent_px"]
    )

    # Stroke thickness: 3-pixel horizontal run on a 45-degree staircase -> 3/sqrt(2)
    stroke = {
        "interior_run_length_px": 3,
        "perpendicular_thickness_if_45_degree": r(3 / math.sqrt(2)),
        "reading": "about 2.1 px perpendicular, consistent with the retained 'about 2 px stroke' statement",
    }

    out = {
        "png": {"path": os.path.relpath(png_path, ROOT).replace("\\", "/"), "sha256": sha, "bytes": len(data), "size": [w, h], "mode_after_convert": "RGBA"},
        "coordinate_convention": "zero-based pixel indices; x right, y down (screen); (x,y) = column x, row y; boxes [left, top, right, bottom] exclusive right/bottom; angles from +x, positive = descending to the right on screen",
        "pixel_map": pixel_map,
        "pixel_map_column_ruler": ruler,
        "opaque_pixels": len(opaque),
        "transparent_pixels": w * h - len(opaque),
        "alpha_values": sorted(alphas),
        "opaque_colours": colours,
        "components_4_connected": components,
        "visible_bbox_exclusive": bbox(opaque),
        "bbox_size": [bbox(opaque)[2] - bbox(opaque)[0], bbox(opaque)[3] - bbox(opaque)[1]],
        "mass_centroid_edge_coords": [r(sum(p[0] for p in opaque) / len(opaque) + 0.5), r(sum(p[1] for p in opaque) / len(opaque) + 0.5)],
        "rows": row_table,
        "quoted_endpoint_identity": endpoint_identity,
        "quoted_polyline": quoted_polyline,
        "what_the_old_numbers_measured": extents,
        "column_partition": partition,
        "contours": contours,
        "alternative_centrelines": {"A_run_centres_excluding_caps": alt_a, "B_outer_contours": alt_b, "C_principal_axis_per_partition": alt_c},
        "stroke": stroke,
    }
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
