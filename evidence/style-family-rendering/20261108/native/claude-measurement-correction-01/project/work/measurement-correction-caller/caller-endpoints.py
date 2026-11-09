"""Caller-independent recomputation of the Ready arm geometry.

Written by the calling agent, separately from the specialist's
work/measurement-correction-pixl/measure-endpoints.py. Reads only the
retained PNG. Zero-based pixel indices, x right, y down (screen convention),
as in the quoted art-assessment points.
"""
import hashlib
import json
import math
import sys

from PIL import Image

PNG = sys.argv[1] if len(sys.argv) > 1 else "assets/ready-confirmed.png"

raw = open(PNG, "rb").read()
img = Image.open(PNG).convert("RGBA")
w, h = img.size
px = img.load()
opaque = [(x, y) for y in range(h) for x in range(w) if px[x, y][3] != 0]
colors = sorted({px[x, y] for (x, y) in opaque})
alphas = sorted({px[x, y][3] for y in range(h) for x in range(w)})
pixel_map = ["".join("#" if px[x, y][3] else "." for x in range(w)) for y in range(h)]

# row runs
runs = {}
for y in range(h):
    xs = [x for x in range(w) if px[x, y][3]]
    if not xs:
        continue
    row_runs, start, prev = [], xs[0], xs[0]
    for x in xs[1:]:
        if x != prev + 1:
            row_runs.append([start, prev])
            start = x
        prev = x
    row_runs.append([start, prev])
    runs[y] = row_runs


def vec(a, b):
    return (b[0] - a[0], b[1] - a[1])


def seg(a, b):
    d = vec(a, b)
    length = math.hypot(*d)
    # angle from horizontal in screen coords; positive dy = downward
    ang = math.degrees(math.atan2(abs(d[1]), abs(d[0])))
    direction = ("descending" if d[1] > 0 else "ascending") + (" right" if d[0] > 0 else " left")
    return {"from": list(a), "to": list(b), "delta": list(d), "length": round(length, 4),
            "angle_from_horizontal_deg": round(ang, 3), "direction": direction,
            "is_45_degree": abs(d[0]) == abs(d[1])}


def polyline(p0, v, p1):
    s1, s2 = seg(p0, v), seg(v, p1)
    u, t = vec(v, p0), vec(v, p1)
    cos = (u[0] * t[0] + u[1] * t[1]) / (math.hypot(*u) * math.hypot(*t))
    return {"left_segment": s1, "right_segment": s2,
            "length_ratio_right_over_left": round(s2["length"] / s1["length"], 4),
            "interior_angle_at_vertex_deg": round(math.degrees(math.acos(cos)), 3)}


quoted = polyline((4, 8), (6, 12), (12, 4))

# what the quoted points are
def describe(pt):
    x, y = pt
    rr = [r for r in runs.get(y, []) if r[0] <= x <= r[1]]
    return {"point": [x, y], "opaque": bool(px[x, y][3]), "row_run": rr[0] if rr else None,
            "single_pixel_run": bool(rr and rr[0][0] == rr[0][1])}

points = [describe(p) for p in [(4, 8), (6, 12), (12, 4)]]

# partition by column: x<=5 left arm, x==6 vertex column, x>=7 right arm
left = [p for p in opaque if p[0] <= 5]
mid = [p for p in opaque if p[0] == 6]
right = [p for p in opaque if p[0] >= 7]


def bbox(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return {"inclusive": [min(xs), min(ys), max(xs), max(ys)],
            "size": [max(xs) - min(xs) + 1, max(ys) - min(ys) + 1]}


# row spans measured tip-to-vertex as in the old 'axis_length_steps'
row_span_left = 12 - 8
row_span_right = 12 - 4
col_span_left = 6 - 4
col_span_right = 12 - 6

# run centres per row (3-pixel runs only, excluding single-pixel caps and merged rows)
centres = {y: [((r[0] + r[1]) / 2, r[1] - r[0] + 1) for r in rs] for y, rs in runs.items()}

# contour advance checks
left_edges_left_arm = [runs[y][0][0] for y in range(9, 13)]  # rows 9..12 leftmost run start
right_edges_right_arm = [runs[y][-1][1] for y in range(5, 13)]  # rows 5..12 rightmost run end
left_edges_right_arm = [runs[y][-1][0] for y in range(4, 10)]  # rows 4..9 rightmost run start


def monotone_one_step(seq, step):
    return all(b - a == step for a, b in zip(seq, seq[1:]))


# alternative centreline: run centres excluding caps
alt_centres = polyline((4, 9), (6, 11), (12, 5))
# alternative: outer contours
alt_outer = polyline((3, 9), (6, 12), (13, 5))

out = {
    "png": PNG,
    "sha256": hashlib.sha256(raw).hexdigest(),
    "size": [w, h],
    "coordinate_convention": "zero-based pixel indices; x increases rightward, y increases downward (screen)",
    "opaque_pixels": len(opaque),
    "transparent_pixels": w * h - len(opaque),
    "alpha_values": alphas,
    "opaque_colors": [list(c) for c in colors],
    "pixel_map": pixel_map,
    "row_runs": {str(y): rs for y, rs in runs.items()},
    "quoted_points": points,
    "quoted_polyline_(4,8)->(6,12)->(12,4)": quoted,
    "visible_bbox": bbox(opaque),
    "partition_counts_x<=5_x==6_x>=7": [len(left), len(mid), len(right)],
    "partition_bboxes": {"x<=5": bbox(left), "x==6": bbox(mid), "x>=7": bbox(right)},
    "tip_to_vertex_row_spans": {"left": row_span_left, "right": row_span_right, "ratio": row_span_right / row_span_left},
    "tip_to_vertex_col_spans": {"left": col_span_left, "right": col_span_right, "ratio": col_span_right / col_span_left},
    "run_centres_by_row": {str(y): c for y, c in centres.items()},
    "contours": {
        "left_arm_left_edge_rows_9_12": left_edges_left_arm,
        "left_arm_left_edge_advances_one_col_per_row": monotone_one_step(left_edges_left_arm, 1),
        "right_arm_right_edge_rows_5_12": right_edges_right_arm,
        "right_arm_right_edge_advances_one_col_per_row": monotone_one_step(right_edges_right_arm, -1),
        "right_arm_left_edge_rows_4_9": left_edges_right_arm,
        "right_arm_left_edge_advances_one_col_per_row": monotone_one_step(left_edges_right_arm, -1),
    },
    "alternative_centreline_run_centres_excluding_caps_(4,9)->(6,11)->(12,5)": alt_centres,
    "alternative_outer_contours_(3,9)->(6,12)->(13,5)": alt_outer,
    "perpendicular_thickness_of_3px_run_on_45deg": round(3 / math.sqrt(2), 3),
}
print(json.dumps(out, indent=1))
