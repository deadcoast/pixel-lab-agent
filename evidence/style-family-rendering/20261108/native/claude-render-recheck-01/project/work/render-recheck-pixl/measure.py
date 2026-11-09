"""Independent Pillow measurements of the renderer-recheck capture (read-only on inputs; writes diagnostics here)."""
import json
import sys
from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(sys.argv[1]).resolve()
CAP = ROOT / "work/render-recheck-pixl-01"
OLD = ROOT / "work/render-pixl-01"
CALLER = ROOT / "work/render-recheck-caller-01"
OUT = ROOT / "work/render-recheck-pixl"
digest = lambda p: sha256(Path(p).read_bytes()).hexdigest()
PANEL = (0x17, 0x23, 0x36)
ACCENT = (0x70, 0xB9, 0xED)

report = json.loads((CAP / "render.json").read_text(encoding="utf-8"))
shot = Image.open(CAP / "destination.png").convert("RGB")
out = {
    "capture": "work/render-recheck-pixl-01",
    "render_json_sha256": digest(CAP / "render.json"),
    "screenshot": {"path": "destination.png", "size": list(shot.size), "sha256": digest(CAP / "destination.png"), "mode_decoded": Image.open(CAP / "destination.png").mode},
    "reported_viewport": report["viewport"],
    "capture_layout": {k: report["capture_layout"][k] for k in ("layoutViewport", "visualViewport", "contentSize")},
    "capture_method": report["capture_method"],
    "browser_product": report["browser_version"]["product"],
    "devicePixelRatio": report["devicePixelRatio"],
    "errors": report["errors"],
    "missing": report["missing"],
    "screenshot_equals_viewport": list(shot.size) == [report["viewport"]["width"], report["viewport"]["height"]],
    "screenshot_equals_layout_viewport": list(shot.size) == [report["capture_layout"]["layoutViewport"]["clientWidth"], report["capture_layout"]["layoutViewport"]["clientHeight"]],
    "views": [],
}


def max_diff(a, b):
    return max(h for _, h in ImageChops.difference(a.convert("RGB"), b.convert("RGB")).getextrema())


def offset_search(view, x, y, radius=12):
    best = None
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            bx, by = x + dx, y + dy
            if bx < 0 or by < 0 or bx + view.width > shot.width or by + view.height > shot.height:
                continue
            d = max_diff(shot.crop((bx, by, bx + view.width, by + view.height)), view)
            if best is None or d < best[0] or (d == best[0] and abs(dx) + abs(dy) < abs(best[1]) + abs(best[2])):
                best = (d, dx, dy)
            if d == 0 and dx == 0 and dy == 0:
                return (0, 0, 0)
    return best


def label_metrics(x, y, w, h):
    # first non-panel column to the right of the canvas within the canvas row band (pure CSS gap on the panel)
    px = shot.load()
    gap = None
    for cx in range(x + w, min(shot.width, x + w + 60)):
        if any(px[cx, cy] != PANEL for cy in range(y, y + h)):
            gap = cx - (x + w)
            break
    rows = []
    if gap is not None:
        sx = x + w + gap
        for cy in range(y - 12, y + h + 12):
            if any(px[cx, cy] != PANEL for cx in range(sx, min(shot.width, sx + 70))):
                rows.append(cy)
    return gap, ([rows[0], rows[-1]] if rows else None)


fixture = Image.open(ROOT / "assets/ready-confirmed.png").convert("RGBA")
composite_cache = {}
for view in report["views"]:
    if not view["asset"]["available"]:
        out["views"].append({"view": f"{view['consumer']} {view['state']} {view['scale']}x", "available": False, "image": None, "label": view["descriptor"]["label"], "path": view["descriptor"]["path"]})
        continue
    img = Image.open(CAP / view["image"]["path"]).convert("RGB")
    b = view["bounds"]
    x, y, w, h = int(b["x"]), int(b["y"]), int(b["width"]), int(b["height"])
    colors = img.getcolors(img.width * img.height)
    distinct = len(colors)
    accent = sum(n for n, c in colors if c == ACCENT)
    panel = sum(n for n, c in colors if c == PANEL)
    entry = {
        "view": f"{view['consumer']} {view['state']} {view['scale']}x",
        "available": True,
        "image": view["image"]["path"],
        "sha256": view["image"]["sha256"],
        "sha256_recomputed": digest(CAP / view["image"]["path"]),
        "size": list(img.size),
        "reported_bounds": [x, y, w, h],
        "bounds_are_integers": all(float(v) == int(v) for v in b.values()),
        "max_channel_diff_at_reported_bounds": max_diff(shot.crop((x, y, x + w, y + h)), img),
        "best_match": dict(zip(("max_channel_diff", "dx", "dy"), offset_search(img, x, y))),
        "distinct_colors": distinct,
        "accent_pixels": accent,
        "panel_pixels": panel,
        "intermediate_pixels": img.width * img.height - accent - panel,
        "label": view["descriptor"]["label"],
        "asset_path": view["descriptor"]["path"],
        "asset_sha256_reported": view["asset"]["sha256"],
        "asset_sha256_on_disk": digest(ROOT / view["descriptor"]["path"]),
        "smoothing": view["smoothing"],
        "imageRendering": view["imageRendering"],
        "geometryMatches": view["geometryMatches"],
    }
    gap, rows = label_metrics(x, y, w, h)
    entry["label_gap_px"] = gap
    entry["label_text_rows"] = rows
    entry["canvas_centre_y"] = y + h / 2
    entry["label_centre_y"] = (rows[0] + rows[1] + 1) / 2 if rows else None
    if view["descriptor"]["path"].endswith(".png"):
        key = view["scale"]
        if key not in composite_cache:
            composite_cache[key] = Image.alpha_composite(Image.new("RGBA", fixture.size, (*PANEL, 255)), fixture).resize((16 * key, 16 * key), Image.Resampling.NEAREST).convert("RGB")
        entry["max_channel_diff_vs_pillow_composite_nearest"] = max_diff(composite_cache[key], img)
    if view["scale"] == 3:
        base = next(v for v in report["views"] if v["consumer"] == view["consumer"] and v["state"] == view["state"] and v["scale"] == 1)
        native = Image.open(CAP / base["image"]["path"]).convert("RGB").resize(img.size, Image.Resampling.NEAREST)
        entry["max_channel_diff_vs_nearest_upscaled_1x_view"] = max_diff(native, img)
    out["views"].append(entry)

# live panel: locate exact copies of the 3x Ready canvas in the live section (y < 320)
ready3 = Image.open(CAP / next(v for v in report["views"] if v["state"] == "succeeded" and v["scale"] == 3)["image"]["path"]).convert("RGB")
live = []
px = shot.load()
tl = ready3.getpixel((0, 0))
for yy in range(160, 320 - 48):
    for xx in range(100, 760 - 48):
        if px[xx, yy] == tl and px[xx + 47, yy + 47] == ready3.getpixel((47, 47)) and px[xx + 20, yy + 24] == ready3.getpixel((20, 24)):
            if max_diff(shot.crop((xx, yy, xx + 48, yy + 48)), ready3) == 0:
                gap, rows = label_metrics(xx, yy, 48, 48)
                live.append({"position": [xx, yy], "exact_match_view": "3x succeeded canvas", "label_gap_px": gap, "label_text_rows": rows})
# collapse overlapping hits (a match at (x,y) implies neighbours do not match exactly because of the accent pattern; keep unique)
out["live_panel_matches"] = live

# transitions
out["transitions"] = [{"event": t["event"], "state": t["state"], "consumers": [(c["consumer"], c["descriptor"]["label"], c["descriptor"]["path"], c["available"], c.get("sha256")) for c in t["consumers"]]} for t in report["transitions"]]
out["served_files"] = report["served_files"]
out["served_files_match_disk"] = {}
for name, expected in report["served_files"].items():
    group, rel = name.split("/", 1)
    base = ROOT if group == "consumer" else ROOT / "renderer-recheck"
    out["served_files_match_disk"][name] = digest(base / rel) == expected
out["renderer_files"] = report["renderer_files"]
out["renderer_files_match_disk"] = {name: digest(ROOT / "renderer-recheck" / name) == h for name, h in report["renderer_files"].items()}
out["renderer_vs_recheck_identity"] = {name: {"renderer": digest(ROOT / "renderer" / name), "renderer_recheck": digest(ROOT / "renderer-recheck" / name), "identical": digest(ROOT / "renderer" / name) == digest(ROOT / "renderer-recheck" / name)} for name in ("server.mjs", "capture.mjs", "index.html", "view.mjs", "check.py")}

# fixture geometry
fpx = fixture.load()
pixel_map = ["".join("#" if fpx[x, y][3] else "." for x in range(16)) for y in range(16)]
opaque = [(x, y) for y in range(16) for x in range(16) if fpx[x, y][3]]
alphas = sorted({fpx[x, y][3] for y in range(16) for x in range(16)})
xs, ys = [p[0] for p in opaque], [p[1] for p in opaque]
runs = []
for y in range(16):
    row = [x for x in range(16) if fpx[x, y][3]]
    if row:
        r, cur = [], 1
        for i in range(1, len(row)):
            if row[i] == row[i - 1] + 1:
                cur += 1
            else:
                r.append(cur); cur = 1
        r.append(cur)
        runs.append({"row": y, "runs": r})
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
lum = lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
def rel_lum(c):
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])
la, lp = rel_lum(ACCENT), rel_lum(PANEL)
out["ready_fixture"] = {
    "path": "assets/ready-confirmed.png",
    "sha256": digest(ROOT / "assets/ready-confirmed.png"),
    "size": list(fixture.size),
    "opaque_pixels": len(opaque),
    "transparent_pixels": 256 - len(opaque),
    "alpha_values": alphas,
    "opaque_rgba": sorted({fpx[x, y] for (x, y) in opaque}),
    "transparent_rgba": sorted({fpx[x, y] for y in range(16) for x in range(16) if not fpx[x, y][3]}),
    "components_4_connected": comps,
    "visible_bbox_exclusive": [min(xs), min(ys), max(xs) + 1, max(ys) + 1],
    "bbox_size": [max(xs) - min(xs) + 1, max(ys) - min(ys) + 1],
    "margins_lrtb": [min(xs), 15 - max(xs), min(ys), 15 - max(ys)],
    "mass_centroid": [round(sum(xs) / len(xs), 3), round(sum(ys) / len(ys), 3)],
    "pixel_map": pixel_map,
    "row_runs": runs,
    "lowest_pixel": min(opaque, key=lambda p: (-p[1], p[0])),
    "vertex_column_6_pixels": sum(1 for p in opaque if p[0] == 6),
    "left_arm_pixels_x_le_5": sum(1 for p in opaque if p[0] <= 5),
    "right_arm_pixels_x_ge_7": sum(1 for p in opaque if p[0] >= 7),
    "left_arm_columns": [min(p[0] for p in opaque if p[0] <= 5), 5],
    "left_arm_rows": [min(p[1] for p in opaque if p[0] <= 5), max(p[1] for p in opaque if p[0] <= 5)],
    "right_arm_columns": [7, max(p[0] for p in opaque if p[0] >= 7)],
    "right_arm_rows": [min(p[1] for p in opaque if p[0] >= 7), max(p[1] for p in opaque if p[0] >= 7)],
    "right_arm_left_edges_rows_4_9": [min(x for x in range(16) if fpx[x, y][3] and x >= 7) for y in range(4, 10)],
    "right_arm_right_edges_rows_4_9": [max(x for x in range(16) if fpx[x, y][3] and x >= 7) for y in range(4, 10)],
    "left_arm_left_edges_rows_8_12": [min(x for x in range(16) if fpx[x, y][3]) for y in range(8, 13)],
    "wcag_contrast_accent_on_panel": round((max(la, lp) + 0.05) / (min(la, lp) + 0.05), 2),
    "luma_601_accent": round(lum(ACCENT), 1),
    "luma_601_panel": round(lum(PANEL), 1),
}

# start vector raster
v0 = Image.open(CAP / "view-000.png").convert("RGB"); v1 = Image.open(CAP / "view-001.png").convert("RGB")
c0 = sorted("#%02x%02x%02x" % c for _, c in v0.getcolors(4096)); c1 = sorted("#%02x%02x%02x" % c for _, c in v1.getcolors(4096))
def bbox_nonpanel(im):
    bg = Image.new("RGB", im.size, PANEL)
    return list(ImageChops.difference(im, bg).getbbox())
out["start_vector_raster"] = {
    "source_sha256": digest(ROOT / "assets/start.svg"),
    "1x_colors": c0, "3x_colors": c1,
    "1x_distinct": len(c0), "3x_distinct": len(c1),
    "1x_intermediate_pixels": sum(n for n, c in v0.getcolors(4096) if c not in (PANEL, ACCENT)),
    "3x_intermediate_pixels": sum(n for n, c in v1.getcolors(4096) if c not in (PANEL, ACCENT)),
    "1x_accent_pixels": sum(n for n, c in v0.getcolors(4096) if c == ACCENT),
    "3x_accent_pixels": sum(n for n, c in v1.getcolors(4096) if c == ACCENT),
    "3x_vs_nearest_upscale_of_1x_max_diff": max_diff(v0.resize((48, 48), Image.Resampling.NEAREST), v1),
    "1x_triangle_bbox_nonpanel": bbox_nonpanel(v0), "3x_triangle_bbox_nonpanel": bbox_nonpanel(v1),
    "claim_check": {"caller_pre_specialist_note_said": "anti-aliased edge pixel count 4 -> 12, linear not 9x", "actual": "28 at 1x, 84 at 3x (3x linear)", "earlier_measurements_json_said": "28 / 84"},
}

# old vs new capture
oldrep = json.loads((OLD / "render.json").read_text(encoding="utf-8"))
oldshot = Image.open(OLD / "destination.png").convert("RGB")
diff = ImageChops.difference(oldshot, shot)
out["old_vs_new"] = {
    "old_capture": "work/render-pixl-01",
    "old_screenshot_sha256": digest(OLD / "destination.png"), "new_screenshot_sha256": digest(CAP / "destination.png"),
    "old_screenshot_size": list(oldshot.size), "new_screenshot_size": list(shot.size),
    "screenshot_diff_bbox": list(diff.getbbox()) if diff.getbbox() else None,
    "screenshot_max_channel_diff": max(h for _, h in diff.getextrema()),
    "screenshot_differing_pixels": sum(1 for p in diff.getdata() if p != (0, 0, 0)),
    "view_hashes_identical": all(digest(OLD / f"view-{i:03d}.png") == digest(CAP / f"view-{i:03d}.png") for i in range(8)),
    "old_reported_viewport": oldrep["viewport"], "new_reported_viewport": report["viewport"],
    "old_bounds_x": sorted({int(v["bounds"]["x"]) for v in oldrep["views"] if v.get("bounds")}),
    "new_bounds_x": sorted({int(v["bounds"]["x"]) for v in report["views"] if v.get("bounds")}),
    "bounds_y_identical": [v["bounds"]["y"] for v in oldrep["views"] if v.get("bounds")] == [v["bounds"]["y"] for v in report["views"] if v.get("bounds")],
    "caller_recheck_screenshot_sha256": digest(CALLER / "destination.png"),
    "caller_recheck_screenshot_identical_to_mine": digest(CALLER / "destination.png") == digest(CAP / "destination.png"),
    "caller_recheck_render_json_sha256": digest(CALLER / "render.json"),
    "caller_recheck_view_hashes_identical": all(digest(CALLER / f"view-{i:03d}.png") == digest(CAP / f"view-{i:03d}.png") for i in range(8)),
    "caller_recheck_bounds_identical": [v.get("bounds") for v in json.loads((CALLER / "render.json").read_text(encoding="utf-8"))["views"]] == [v.get("bounds") for v in report["views"]],
}

# derived nearest-neighbour crops of the NEW screenshot (diagnostics, not art)
crops = {
    "crop-full-1x-ready-cell-8x.png": ((243, 601, 333, 649), 8),
    "crop-compact-1x-ready-cell-8x.png": ((675, 601, 765, 649), 8),
    "crop-full-3x-ready-cell-4x.png": ((457, 593, 591, 657), 4),
    "crop-compact-3x-ready-cell-4x.png": ((889, 593, 1023, 657), 4),
    "crop-full-column-start-ready-1x-6x.png": ((243, 425, 333, 640), 6),
    "crop-full-column-start-ready-3x-3x.png": ((457, 405, 601, 660), 3),
    "crop-live-panel-2x.png": ((112, 160, 700, 300), 2),
    "crop-matrix-rows-2x.png": ((112, 370, 1168, 720), 2),
}
out["derived_crops"] = {}
for name, (box, scale) in crops.items():
    im = shot.crop(box).resize(((box[2] - box[0]) * scale, (box[3] - box[1]) * scale), Image.Resampling.NEAREST)
    im.save(OUT / name)
    out["derived_crops"][name] = {"source": "work/render-recheck-pixl-01/destination.png", "box": list(box), "nearest_scale": scale, "size": list(im.size), "sha256": digest(OUT / name), "role": "diagnostic crop of the actual screenshot; not art"}
gray = shot.crop((112, 590, 1168, 660)).convert("L").resize((2112, 140), Image.Resampling.NEAREST)
gray.save(OUT / "crop-succeeded-row-grayscale-2x.png")
out["derived_crops"]["crop-succeeded-row-grayscale-2x.png"] = {"source": "work/render-recheck-pixl-01/destination.png", "box": [112, 590, 1168, 660], "nearest_scale": 2, "size": list(gray.size), "sha256": digest(OUT / "crop-succeeded-row-grayscale-2x.png"), "role": "grayscale diagnostic of the succeeded row (non-colour reading of the Ready mark beside its label); not art"}

(OUT / "measurements.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: out[k] for k in ("screenshot_equals_viewport", "screenshot_equals_layout_viewport", "live_panel_matches", "old_vs_new")}, indent=1))
print(json.dumps([(v["view"], v.get("max_channel_diff_at_reported_bounds"), v.get("best_match"), v.get("label_gap_px"), v.get("label_text_rows"), v.get("distinct_colors"), v.get("intermediate_pixels"), v.get("max_channel_diff_vs_pillow_composite_nearest"), v.get("max_channel_diff_vs_nearest_upscaled_1x_view")) for v in out["views"] if v["available"]], indent=1))
print(json.dumps(out["start_vector_raster"], indent=1))
print(json.dumps({k: v for k, v in out["ready_fixture"].items() if k not in ("pixel_map", "row_runs")}, indent=1))
print("\n".join(out["ready_fixture"]["pixel_map"]))
