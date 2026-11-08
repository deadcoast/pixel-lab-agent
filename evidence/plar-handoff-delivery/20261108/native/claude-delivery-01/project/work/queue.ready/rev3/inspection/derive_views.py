"""Derived inspection evidence for the Ready candidate (NOT candidates, NOT deliverables).

Usage: python -I derive_views.py SOURCE_PNG OUT_DIR
Writes, read-only on the source:
  derived-desaturated-1x-on-172336.png   grayscale (luma) of candidate composited on #172336, 16x16
  derived-desaturated-3x-on-172336.png   same, nearest 3x, 48x48
  derived-structure-8x-on-172336.png     colour candidate on #172336, nearest 8x, 128x128 (structure aid)
  derived-start-vs-ready-3x.png          Start vector approximated? NO - omitted; the SVG is not rasterised here.
and derived-manifest.json with sha256 of each derived file.
"""
import hashlib
import json
import os
import sys

from PIL import Image

PANEL = (0x17, 0x23, 0x36, 255)


def composite(src: Image.Image, bg) -> Image.Image:
    base = Image.new("RGBA", src.size, bg)
    base.alpha_composite(src)
    return base


def main(src_path: str, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    src_bytes = open(src_path, "rb").read()
    src = Image.open(src_path).convert("RGBA")
    outputs = {}

    comp = composite(src, PANEL)
    gray = comp.convert("L").convert("RGBA")  # ITU-R 601 luma desaturation
    p1 = os.path.join(out_dir, "derived-desaturated-1x-on-172336.png")
    gray.save(p1)
    outputs["desaturated_1x"] = p1
    p3 = os.path.join(out_dir, "derived-desaturated-3x-on-172336.png")
    gray.resize((gray.width * 3, gray.height * 3), Image.NEAREST).save(p3)
    outputs["desaturated_3x"] = p3

    p8 = os.path.join(out_dir, "derived-structure-8x-on-172336.png")
    comp.resize((comp.width * 8, comp.height * 8), Image.NEAREST).save(p8)
    outputs["structure_8x"] = p8

    # Luma values of panel and mark, for the record
    panel_l = Image.new("RGBA", (1, 1), PANEL).convert("L").getpixel((0, 0))
    mark_rgba = next(((r, g, b, a) for (_, (r, g, b, a)) in src.getcolors(256) if a > 0), None)
    mark_l = Image.new("RGBA", (1, 1), mark_rgba).convert("L").getpixel((0, 0)) if mark_rgba else None

    manifest = {
        "kind": "derived inspection evidence (not a candidate, not a deliverable)",
        "source": {"path": src_path, "sha256": hashlib.sha256(src_bytes).hexdigest()},
        "method": "RGBA alpha-composite onto #172336, then Pillow convert('L') (ITU-R 601 luma) for desaturation; Image.NEAREST integer enlargement",
        "luma": {"panel_#172336": panel_l, "mark_rgba": list(mark_rgba) if mark_rgba else None, "mark_luma": mark_l,
                  "luma_difference": (mark_l - panel_l) if mark_l is not None else None},
        "files": {},
    }
    for key, p in outputs.items():
        b = open(p, "rb").read()
        im = Image.open(p)
        manifest["files"][key] = {"path": p.replace("\\", "/"), "sha256": hashlib.sha256(b).hexdigest(), "size": list(im.size)}
    mp = os.path.join(out_dir, "derived-manifest.json")
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    print(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
