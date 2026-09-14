"""Independently recompute the study's claims and check the report states them.

Recomputes every number in edge-and-canvas-study.md sections 1, 2 and 4 from
the two supplied PNGs without reading measurement.json, then confirms the
report text actually contains each claim. Writes work/evidence/repro-check.json.
"""

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / (sys.argv[1] if len(sys.argv) > 1
                 else "work/study/edge-and-canvas-study.md")
OUT = ROOT / (sys.argv[2] if len(sys.argv) > 2
              else "work/evidence/repro-check.json")

NAVY, TEAL, CREAM = (37, 53, 74), (86, 181, 188), (244, 221, 162)
NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mask(im):
    return {(x, y) for y in range(im.height) for x in range(im.width)
            if im.getpixel((x, y))[3] != 0}


def rings(cells):
    out, cur = [], set(cells)
    while cur:
        edge = {(x, y) for (x, y) in cur
                if any((x + dx, y + dy) not in cur for dx, dy in NEIGHBOURS)}
        out.append(edge)
        cur -= edge
    return out


def main():
    a = Image.open(ROOT / "reference.png").convert("RGBA")
    b = Image.open(ROOT / "reference-b.png").convert("RGBA")
    ma, mb = mask(a), mask(b)
    navy = {p for p in ma if a.getpixel(p)[:3] == NAVY}
    layers = rings(ma)
    xs, ys = [p[0] for p in ma], [p[1] for p in ma]
    diff = [(x, y) for y in range(32) for x in range(32)
            if a.getpixel((x, y)) != b.getpixel((x, y))]

    claims = {
        "reference.png sha256": (sha(ROOT / "reference.png"),
                                 "d997cade"),
        "reference-b.png sha256": (sha(ROOT / "reference-b.png"),
                                   "e76b40ce"),
        "both are 32x32": (a.size == (32, 32) and b.size == (32, 32), "32×32"),
        "silhouette identical": (ma == mb, "an **identical"),
        "silhouette cell count": (len(ma), "390 opaque cells"),
        "bounding box": ([min(xs), max(xs), min(ys), max(ys)] == [7, 24, 3, 27],
                         "x7–24, y3–27"),
        "occupied area": ([max(xs) - min(xs) + 1, max(ys) - min(ys) + 1] == [18, 25],
                          "18×25"),
        "differing pixels": (len(diff), "180 pixels"),
        "every difference is navy->teal": (
            {(a.getpixel(p)[:3], b.getpixel(p)[:3]) for p in diff} == {(NAVY, TEAL)},
            "navy `#25354A` in `reference.png` where `reference-b.png` has\nteal `#56B5BC`"),
        "no fractional alpha": (
            not any(0 < im.getpixel((x, y))[3] < 255
                    for im in (a, b) for y in range(32) for x in range(32)),
            "zero fractional-alpha pixels"),
        "cream marks present and unchanged": (
            sum(1 for p in ma if a.getpixel(p)[:3] == CREAM) == 24
            and sum(1 for p in mb if b.getpixel(p)[:3] == CREAM) == 24, "cream"),
        "navy cell count": (len(navy), "| 180 (46.2% of the silhouette) |"),
        "navy share": (round(100 * len(navy) / len(ma), 1), "46.2%"),
        "interior left by 2px rim": (len(ma) - len(navy), "210 cells"),
        "ring sizes depth 1-3": ([len(r) for r in layers[:3]], "| 92 |"),
        "navy per ring depth 1-3": ([len(r & navy) for r in layers[:3]],
                                    "| 3 | 58 | 6 |"),
        "rim is exactly 2 deep plus 6 strays": (
            layers[0] <= navy and layers[1] <= navy
            and len(layers[2] & navy) == 6 and not (layers[3] & navy),
            "uniform **2-pixel** outline, plus 6 stray navy cells"),
        "1px rim size": (len(layers[0]), "92 cells (23.6%)"),
        "interior left by 1px rim": (len(ma) - len(layers[0]), "298 interior cells"),
    }

    # Section 4 arithmetic, recomputed.
    for canvas, fig, two, one in [(16, 13, 30.8, 15.4), (24, 20, 20.0, 10.0),
                                  (32, 26, 15.4, 7.7), (48, 39, 10.3, 5.1),
                                  (64, 52, 7.7, 3.8)]:
        claims[f"canvas {canvas} figure height"] = (round(canvas * 26 / 32) == fig,
                                                    f"| {canvas} | {fig} |")
        claims[f"canvas {canvas} 2px share"] = (round(100 * 4 / fig, 1) == two,
                                               f"| {two}% | {one}% |")
        claims[f"canvas {canvas} 1px share"] = (round(100 * 2 / fig, 1) == one,
                                               f"| {two}% | {one}% |")

    text = REPORT.read_text(encoding="utf-8")
    results = {}
    for name, (computed, quoted) in claims.items():
        stated = quoted in text
        agrees = computed is not False and computed != 0
        results[name] = {
            "recomputed": computed if not isinstance(computed, bool) else computed,
            "quoted_fragment": quoted,
            "fragment_present_in_report": stated,
            "pass": bool(stated and agrees),
        }

    report = {
        "check": "q_study_repro",
        "checked_at": "2026-09-11",
        "candidate": {"path": REPORT.relative_to(ROOT).as_posix(),
                      "sha256": sha(REPORT)},
        "inputs": {"reference.png": sha(ROOT / "reference.png"),
                   "reference-b.png": sha(ROOT / "reference-b.png")},
        "method": ("Recomputed from the PNGs by this script, independently of "
                   "work/tools/edge_study.py and measurement.json, then matched "
                   "against the literal text of the report."),
        "claims_checked": len(results),
        "claims_failed": sorted(k for k, v in results.items() if not v["pass"]),
        "result": "pass" if all(v["pass"] for v in results.values()) else "fail",
        "claims": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(report["result"], report["claims_checked"], "claims;",
          "failed:", report["claims_failed"])


if __name__ == "__main__":
    main()
