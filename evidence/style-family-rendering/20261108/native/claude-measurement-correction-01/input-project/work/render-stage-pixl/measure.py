"""Independent measurements of the render-pixl-01 capture (specialist diagnostics; not art, not acceptance)."""
import json
import sys
from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(sys.argv[1]).resolve()
CAP = ROOT / "work/render-pixl-01"
OUT = ROOT / "work/render-stage-pixl"
OUT.mkdir(exist_ok=True)
PANEL = (0x17, 0x23, 0x36)
ACCENT = (0x70, 0xB9, 0xED)


def digest(p):
    return sha256(Path(p).read_bytes()).hexdigest()


def max_diff(a, b):
    ext = ImageChops.difference(a.convert("RGB"), b.convert("RGB")).getextrema()
    return max(h for _, h in ext)


report = json.loads((CAP / "render.json").read_text(encoding="utf-8"))
shot = Image.open(CAP / "destination.png").convert("RGB")
result = {"capture": "work/render-pixl-01", "screenshot": {"size": list(shot.size), "sha256": digest(CAP / "destination.png")},
          "reported_viewport": report["viewport"], "views": [], "live_panel": [], "ready_fixture": {}, "start_vector_raster": {}, "derived_crops": {}}

# body is `max-width: 1120px; margin: auto` so a wider layout viewport re-centres content horizontally
result["layout_shift_prediction"] = {
    "body_max_width_px": 1120, "body_margin": "auto",
    "left_margin_at_reported_width": (report["viewport"]["width"] - 1120) // 2,
    "left_margin_at_screenshot_width": (shot.size[0] - 1120) // 2,
    "predicted_dx": (shot.size[0] - 1120) // 2 - (report["viewport"]["width"] - 1120) // 2,
    "predicted_dy": 0,
}

available = [v for v in report["views"] if v["asset"]["available"]]
for v in available:
    img = Image.open(CAP / v["image"]["path"]).convert("RGB")
    bx, by = int(v["bounds"]["x"]), int(v["bounds"]["y"])
    w, h = img.size
    at_reported = max_diff(shot.crop((bx, by, bx + w, by + h)), img)
    best = None
    for dy in range(-24, 25):
        for dx in range(-24, 25):
            x, y = bx + dx, by + dy
            if x < 0 or y < 0 or x + w > shot.size[0] or y + h > shot.size[1]:
                continue
            d = max_diff(shot.crop((x, y, x + w, y + h)), img)
            if best is None or d < best["max_channel_diff"] or (d == best["max_channel_diff"] and abs(dx) + abs(dy) < abs(best["dx"]) + abs(best["dy"])):
                best = {"max_channel_diff": d, "dx": dx, "dy": dy}
    sx, sy = bx + best["dx"], by + best["dy"]
    # label gap: scan right of the canvas along its full height for the first column with any non-panel pixel
    gap = None
    for col in range(sx + w, min(sx + w + 60, shot.size[0])):
        column = [shot.getpixel((col, yy)) for yy in range(sy, sy + h)]
        if any(p != PANEL for p in column):
            gap = col - (sx + w)
            break
    # label vertical extent (text pixels) within +-30 px of the canvas, in the 120 px to the right
    text_rows = []
    for yy in range(max(0, sy - 12), min(shot.size[1], sy + h + 12)):
        if any(shot.getpixel((xx, yy)) != PANEL for xx in range(sx + w + (gap or 0), min(shot.size[0], sx + w + (gap or 0) + 120))):
            text_rows.append(yy)
    colors = img.getcolors(maxcolors=4096)
    entry = {
        "view": f"{v['consumer']} {v['state']} {v['scale']}x", "image": v["image"]["path"], "sha256": v["image"]["sha256"],
        "sha256_recomputed": digest(CAP / v["image"]["path"]), "size": [w, h], "reported_bounds": [bx, by, w, h],
        "max_channel_diff_at_reported_bounds": at_reported, "best_match": best, "match_position": [sx, sy],
        "canvas_centre_y": sy + h / 2, "label_gap_px": gap, "label_text_rows": [min(text_rows), max(text_rows)] if text_rows else None,
        "label_centre_y": (min(text_rows) + max(text_rows) + 1) / 2 if text_rows else None,
        "distinct_colors": len(colors), "accent_pixels": sum(c for c, p in colors if p == ACCENT), "panel_pixels": sum(c for c, p in colors if p == PANEL),
        "other_pixels": sum(c for c, p in colors if p not in (ACCENT, PANEL)),
    }
    if v["descriptor"]["path"].endswith(".png"):
        src = Image.open(ROOT / v["descriptor"]["path"]).convert("RGBA")
        comp = Image.alpha_composite(Image.new("RGBA", src.size, (*PANEL, 255)), src).convert("RGB")
        expected = comp.resize(img.size, Image.Resampling.NEAREST) if v["scale"] != 1 else comp
        entry["max_channel_diff_vs_pillow_composite_nearest"] = max_diff(expected, img)
    result["views"].append(entry)

# Start vector: is the 3x canvas a nearest upscale of the 1x raster, or a re-rasterisation?
v1 = Image.open(CAP / "view-000.png").convert("RGB")
v3 = Image.open(CAP / "view-001.png").convert("RGB")
result["start_vector_raster"] = {
    "1x_colors": sorted("#%02x%02x%02x" % p for _, p in v1.getcolors(4096)),
    "3x_colors": sorted("#%02x%02x%02x" % p for _, p in v3.getcolors(4096)),
    "3x_equals_nearest_upscale_of_1x_max_diff": max_diff(v1.resize((48, 48), Image.Resampling.NEAREST), v3),
    "1x_intermediate_pixels": sum(c for c, p in v1.getcolors(4096) if p not in (ACCENT, PANEL)),
    "3x_intermediate_pixels": sum(c for c, p in v3.getcolors(4096) if p not in (ACCENT, PANEL)),
    "1x_triangle_bbox_nonpanel": ImageChops.difference(v1, Image.new("RGB", v1.size, PANEL)).getbbox(),
    "3x_triangle_bbox_nonpanel": ImageChops.difference(v3, Image.new("RGB", v3.size, PANEL)).getbbox(),
}

# Live panel: locate the two 3x Ready canvases in the top region by exact match against view-005
ready3 = Image.open(CAP / "view-005.png").convert("RGB")
for y in range(150, 300):
    for x in range(100, 600):
        if shot.getpixel((x, y)) == ACCENT and shot.getpixel((x - 1, y)) == PANEL and shot.getpixel((x, y - 1)) == PANEL:
            # topmost logical pixel of the check is (12,4); at 3x its block starts at (36,12) inside the 48x48 canvas
            cx, cy = x - 36, y - 12
            if cx >= 0 and cy >= 0 and max_diff(shot.crop((cx, cy, cx + 48, cy + 48)), ready3) == 0:
                gap = None
                for col in range(cx + 48, cx + 48 + 60):
                    if any(shot.getpixel((col, yy)) != PANEL for yy in range(cy, cy + 48)):
                        gap = col - (cx + 48)
                        break
                if not any(e["position"] == [cx, cy] for e in result["live_panel"]):
                    result["live_panel"].append({"position": [cx, cy], "exact_match_view": "view-005.png", "label_gap_px": gap})

# Ready fixture facts
fx = Image.open(ROOT / "assets/ready-confirmed.png").convert("RGBA")
px = fx.load()
opaque = [(x, y) for y in range(16) for x in range(16) if px[x, y][3] != 0]
rows = ["".join("#" if px[x, y][3] else "." for x in range(16)) for y in range(16)]
alphas = sorted({px[x, y][3] for y in range(16) for x in range(16)})
colors = sorted({px[x, y] for (x, y) in opaque})
xs, ys = [p[0] for p in opaque], [p[1] for p in opaque]
# 4-connected components
seen, comps = set(), 0
for p in opaque:
    if p in seen:
        continue
    comps += 1
    stack = [p]
    while stack:
        q = stack.pop()
        if q in seen:
            continue
        seen.add(q)
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (q[0] + d[0], q[1] + d[1])
            if n in opaque and n not in seen:
                stack.append(n)
runs = []
for y in range(16):
    run, cur = [], 0
    for x in range(16):
        if px[x, y][3]:
            cur += 1
        elif cur:
            run.append(cur); cur = 0
    if cur:
        run.append(cur)
    if run:
        runs.append({"row": y, "runs": run})


def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


la, lp = lum(ACCENT), lum(PANEL)
result["ready_fixture"] = {
    "sha256": digest(ROOT / "assets/ready-confirmed.png"), "size": list(fx.size), "opaque_pixels": len(opaque), "transparent_pixels": 256 - len(opaque),
    "alpha_values": alphas, "opaque_colors": ["#%02x%02x%02x alpha %d" % (c[0], c[1], c[2], c[3]) for c in colors],
    "components_4_connected": comps, "visible_bbox_exclusive": [min(xs), min(ys), max(xs) + 1, max(ys) + 1],
    "bbox_size": [max(xs) + 1 - min(xs), max(ys) + 1 - min(ys)], "bbox_centre": [(min(xs) + max(xs) + 1) / 2, (min(ys) + max(ys) + 1) / 2],
    "mass_centroid": [round(sum(xs) / len(xs) + 0.5, 3), round(sum(ys) / len(ys) + 0.5, 3)],
    "pixel_map": rows, "row_runs": runs,
    "lowest_pixel": max(opaque, key=lambda p: (p[1], -p[0])),
    "left_arm_pixels_x_le_5": sum(1 for p in opaque if p[0] <= 5), "right_arm_pixels_x_ge_7": sum(1 for p in opaque if p[0] >= 7), "vertex_column_6_pixels": sum(1 for p in opaque if p[0] == 6),
    "left_arm_columns": [min(p[0] for p in opaque if p[0] <= 5), max(p[0] for p in opaque if p[0] <= 5)], "left_arm_rows": [min(p[1] for p in opaque if p[0] <= 5), max(p[1] for p in opaque if p[0] <= 5)],
    "right_arm_columns": [min(p[0] for p in opaque if p[0] >= 7), max(p[0] for p in opaque if p[0] >= 7)], "right_arm_rows": [min(p[1] for p in opaque if p[0] >= 7), max(p[1] for p in opaque if p[0] >= 7)],
    "wcag_contrast_accent_on_panel": round((max(la, lp) + 0.05) / (min(la, lp) + 0.05), 2),
    "luma_601_accent": round(0.299 * ACCENT[0] + 0.587 * ACCENT[1] + 0.114 * ACCENT[2], 1), "luma_601_panel": round(0.299 * PANEL[0] + 0.587 * PANEL[1] + 0.114 * PANEL[2], 1),
}

# Derived crops (diagnostic enlargements of the actual screenshot; not art)
def crop(name, box, scale):
    im = shot.crop(box).resize(((box[2] - box[0]) * scale, (box[3] - box[1]) * scale), Image.Resampling.NEAREST)
    p = OUT / name
    im.save(p)
    result["derived_crops"][name] = {"source": "work/render-pixl-01/destination.png", "box": list(box), "nearest_scale": scale, "size": list(im.size), "sha256": digest(p)}


dx = result["layout_shift_prediction"]["predicted_dx"]
crop("crop-full-1x-ready-cell-8x.png", (238 + dx - 4, 617 - 16, 238 + dx + 16 + 70, 617 + 32), 8)
crop("crop-compact-1x-ready-cell-8x.png", (670 + dx - 4, 617 - 16, 670 + dx + 16 + 70, 617 + 32), 8)
crop("crop-full-3x-ready-cell-4x.png", (454 + dx - 6, 601 - 8, 454 + dx + 48 + 80, 601 + 56), 4)
crop("crop-compact-3x-ready-cell-4x.png", (886 + dx - 6, 601 - 8, 886 + dx + 48 + 80, 601 + 56), 4)
crop("crop-full-column-start-ready-1x-6x.png", (238 + dx - 4, 425, 238 + dx + 16 + 70, 640), 6)
crop("crop-full-column-start-ready-3x-3x.png", (454 + dx - 6, 405, 454 + dx + 48 + 90, 660), 3)
crop("crop-live-panel-2x.png", (112 + dx - 9, 160, 700, 300), 2)
crop("crop-matrix-rows-2x.png", (112 + dx - 9, 370, 1168 + dx - 9, 720), 2)

(OUT / "measurements.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"views": [(e["view"], e["max_channel_diff_at_reported_bounds"], e["best_match"], e["label_gap_px"], e["canvas_centre_y"], e["label_centre_y"], e.get("max_channel_diff_vs_pillow_composite_nearest")) for e in result["views"]],
                  "layout": result["layout_shift_prediction"], "live": result["live_panel"], "start": result["start_vector_raster"],
                  "fixture": {k: v for k, v in result["ready_fixture"].items() if k not in ("pixel_map", "row_runs")}}, indent=1))
