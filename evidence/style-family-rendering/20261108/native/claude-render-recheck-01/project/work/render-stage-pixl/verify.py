"""Cross-check prior assessment facts and earlier retained views against the new browser capture (read-only)."""
import json
import sys
from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "work/render-stage-pixl"
digest = lambda p: sha256(Path(p).read_bytes()).hexdigest()
prior = json.loads((ROOT / "work/queue.ready-reassessment/art-assessment.json").read_text(encoding="utf-8"))
mine = json.loads((OUT / "measurements.json").read_text(encoding="utf-8"))
fx = Image.open(ROOT / "assets/ready-confirmed.png").convert("RGBA")
px = fx.load()
out = {
    "prior_assessment_sha256": digest(ROOT / "work/queue.ready-reassessment/art-assessment.json"),
    "pixel_map_equal": prior["measured"]["pixel_map"] == mine["ready_fixture"]["pixel_map"],
    "transparent_pixel_rgba_values": sorted({px[x, y] for y in range(16) for x in range(16) if px[x, y][3] == 0}),
    "opaque_pixel_rgba_values": sorted({px[x, y] for y in range(16) for x in range(16) if px[x, y][3] != 0}),
    "contours": {},
    "prior_viewed_files": [],
    "diagnostics": {},
}
# per-row left/right edges for each arm (rows as in the fixture)
rows = {}
for y in range(16):
    xs = [x for x in range(16) if px[x, y][3]]
    if xs:
        rows[y] = xs
out["contours"]["right_arm_rows_4_to_9_left_edges"] = [min(x for x in rows[y] if x >= 7) for y in range(4, 10)]
out["contours"]["right_arm_rows_4_to_9_right_edges"] = [max(x for x in rows[y] if x >= 7) for y in range(4, 10)]
out["contours"]["left_arm_rows_8_to_12_left_edges"] = [min(rows[y]) for y in range(8, 13)]
out["contours"]["row_runs"] = mine["ready_fixture"]["row_runs"]
for v in prior["viewed"]:
    p = ROOT / v["path"]
    entry = {"path": v["path"], "claimed_sha256": v["sha256"], "exists": p.exists()}
    if p.exists():
        entry["actual_sha256"] = digest(p)
        entry["hash_matches"] = entry["actual_sha256"] == v["sha256"]
        with Image.open(p) as im:
            entry["size"] = list(im.size)
            entry["colors"] = sorted("#%02x%02x%02x a%d" % c for _, c in im.convert("RGBA").getcolors(65536))
    out["prior_viewed_files"].append(entry)
# do the earlier pixl inspection panel views equal the browser canvases?
cap = ROOT / "work/render-pixl-01"
insp = ROOT / ".pixl/assets/queue.ready/inspections/0126fe9615c7934b3e1ff0b197f769147de025c2a7064030dc2622199b90e38a/views"
for earlier, later in (("0001.png", "view-004.png"), ("0002.png", "view-005.png")):
    a = Image.open(insp / earlier).convert("RGB")
    b = Image.open(cap / later).convert("RGB")
    out["diagnostics"][f"{earlier}_vs_{later}"] = {"sizes": [list(a.size), list(b.size)], "max_channel_diff": max(h for _, h in ImageChops.difference(a, b).getextrema()) if a.size == b.size else None}
# caller capture equals mine?
caller = ROOT / "work/render-caller-01"
out["caller_capture_comparison"] = {name: {"caller": digest(caller / name), "mine": digest(cap / name), "equal": digest(caller / name) == digest(cap / name)} for name in ["destination.png"] + [f"view-{i:03d}.png" for i in range(8)]}
out["render_json_sha256"] = {"caller": digest(caller / "render.json"), "mine": digest(cap / "render.json")}
rj_c = json.loads((caller / "render.json").read_text(encoding="utf-8"))
rj_m = json.loads((cap / "render.json").read_text(encoding="utf-8"))
diff_keys = [k for k in rj_m if rj_m[k] != rj_c.get(k)]
out["render_json_differing_top_level_keys"] = diff_keys
(OUT / "assessment-crosscheck.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in out.items() if k != "prior_viewed_files"}, indent=1))
print(json.dumps([(e["path"].split("/")[-1], e.get("hash_matches"), e.get("colors")) for e in out["prior_viewed_files"]]))
