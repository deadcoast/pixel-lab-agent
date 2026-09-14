"""Build the outline-treatment and canvas-size decision study from the two
supplied references.

Reads only reference.png and reference-b.png from the project root. Writes a
measurement JSON and a contact sheet used to decide the two open intake
choices (edge_treatment, px). It generates no character art and calls no
remote service.
"""

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "work" / "study"

LIGHT = (232, 232, 226, 255)
DARK = (24, 22, 30, 255)
BUSY_A = (104, 96, 132, 255)
BUSY_B = (62, 58, 84, 255)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return Image.open(ROOT / name).convert("RGBA")


def opaque(im):
    return {(x, y) for y in range(im.height) for x in range(im.width)
            if im.getpixel((x, y))[3] != 0}


def color_counts(im):
    counts = {}
    for y in range(im.height):
        for x in range(im.width):
            p = im.getpixel((x, y))
            counts[p] = counts.get(p, 0) + 1
    return counts


def boundary(mask):
    """Opaque cells with at least one 4-neighbour outside the mask."""
    return {(x, y) for (x, y) in mask
            if any((x + dx, y + dy) not in mask
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}


def erode(mask):
    return mask - boundary(mask)


def bbox(mask):
    xs = [p[0] for p in mask]
    ys = [p[1] for p in mask]
    return [min(xs), min(ys), max(xs), max(ys)]


def make_variant(base, mask, outline_cells, outline_rgba, fill_rgba):
    """Repaint the shared silhouette with a chosen outline thickness."""
    im = base.copy()
    for (x, y) in mask:
        px = im.getpixel((x, y))
        if px[:3] in (OUTLINE_RGB, FILL_RGB):
            im.putpixel((x, y), outline_rgba if (x, y) in outline_cells else fill_rgba)
    return im


def checker(size, scale):
    im = Image.new("RGBA", size, BUSY_A)
    cell = max(1, 4 * scale)
    for y in range(size[1]):
        for x in range(size[0]):
            if ((x // cell) + (y // cell)) % 2:
                im.putpixel((x, y), BUSY_B)
    return im


def upscale(im, scale):
    return im.resize((im.width * scale, im.height * scale), Image.NEAREST)


def composite(sprite, bg_color, scale):
    s = upscale(sprite, scale)
    bg = checker(s.size, scale) if bg_color == "busy" else Image.new("RGBA", s.size, bg_color)
    bg.alpha_composite(s)
    return bg


def main():
    ref_a, ref_b = load("reference.png"), load("reference-b.png")
    mask_a, mask_b = opaque(ref_a), opaque(ref_b)

    counts_a = color_counts(ref_a)
    counts_b = color_counts(ref_b)
    outline_cells = {(x, y) for (x, y) in mask_a
                     if ref_a.getpixel((x, y))[:3] == OUTLINE_RGB}
    ring1 = boundary(mask_a)
    ring2 = ring1 | boundary(erode(mask_a))

    variants = {
        "as_supplied_2px_outline": ref_a,
        "as_supplied_no_outline": ref_b,
        "derived_1px_outline": make_variant(
            ref_a, mask_a, ring1, OUTLINE_RGBA, FILL_RGBA),
    }

    OUT.mkdir(parents=True, exist_ok=True)
    for name, im in variants.items():
        im.save(OUT / f"variant-{name}.png")

    # Contact sheet: rows = variants, columns = (native, x4, x8) on three grounds.
    scales = [1, 4, 8]
    grounds = [("light", LIGHT), ("dark", DARK), ("busy", "busy")]
    pad, cell_w = 8, 32 * 8
    row_h = cell_w + pad
    sheet_w = pad + len(grounds) * len(scales) * (cell_w + pad)
    sheet_h = pad + len(variants) * (row_h + pad)
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (255, 255, 255, 255))
    for r, (name, im) in enumerate(variants.items()):
        y0 = pad + r * (row_h + pad)
        c = 0
        for gname, gcolor in grounds:
            for scale in scales:
                tile = composite(im, gcolor, scale)
                x0 = pad + c * (cell_w + pad)
                # centre the smaller scales inside a fixed cell
                sheet.paste(tile, (x0 + (cell_w - tile.width) // 2,
                                   y0 + (cell_w - tile.height) // 2), tile)
                c += 1
    sheet.save(OUT / "contact-sheet.png")

    report = {
        "generated_from": {
            "reference.png": {"sha256": digest(ROOT / "reference.png"),
                              "size": list(ref_a.size)},
            "reference-b.png": {"sha256": digest(ROOT / "reference-b.png"),
                                "size": list(ref_b.size)},
        },
        "silhouette_identical": sorted(mask_a) == sorted(mask_b),
        "differing_pixels": sum(
            1 for y in range(32) for x in range(32)
            if ref_a.getpixel((x, y)) != ref_b.getpixel((x, y))),
        "visible_pixels": len(mask_a),
        "visible_bbox_xyxy": bbox(mask_a),
        "occupied_size": [bbox(mask_a)[2] - bbox(mask_a)[0] + 1,
                          bbox(mask_a)[3] - bbox(mask_a)[1] + 1],
        "fractional_alpha_pixels": sum(
            1 for y in range(32) for x in range(32)
            for im in (ref_a, ref_b) if 0 < im.getpixel((x, y))[3] < 255),
        "colors": {
            "reference.png": {str(k): v for k, v in sorted(
                counts_a.items(), key=lambda kv: -kv[1]) if k[3] != 0},
            "reference-b.png": {str(k): v for k, v in sorted(
                counts_b.items(), key=lambda kv: -kv[1]) if k[3] != 0},
        },
        "outline_accounting": {
            "outline_rgb": list(OUTLINE_RGB),
            "fill_rgb": list(FILL_RGB),
            "outline_pixels_in_reference_a": len(outline_cells),
            "outline_share_of_silhouette": round(len(outline_cells) / len(mask_a), 4),
            "outline_equals_two_boundary_rings": outline_cells == ring2,
            "one_ring_outline_pixels": len(ring1),
            "one_ring_share_of_silhouette": round(len(ring1) / len(mask_a), 4),
            "interior_pixels_left_by_2px_outline": len(mask_a) - len(outline_cells),
            "interior_pixels_left_by_1px_outline": len(mask_a) - len(ring1),
        },
        "canvas_cost": {
            "note": ("Share of a figure's height consumed by outline on the top "
                     "and bottom edge, for candidate canvas heights, assuming "
                     "the reference's 26/32 occupancy ratio."),
            "occupied_height_at": {
                str(n): round(n * 26 / 32) for n in (16, 24, 32, 48, 64)},
            "two_px_outline_height_share_at": {
                str(n): round(4 / max(1, round(n * 26 / 32)), 3)
                for n in (16, 24, 32, 48, 64)},
            "one_px_outline_height_share_at": {
                str(n): round(2 / max(1, round(n * 26 / 32)), 3)
                for n in (16, 24, 32, 48, 64)},
        },
    }
    (OUT / "measurement.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    json.dump(report, sys.stdout, indent=2)
    print()


OUTLINE_RGB = (37, 53, 74)
FILL_RGB = (86, 181, 188)
OUTLINE_RGBA = OUTLINE_RGB + (255,)
FILL_RGBA = FILL_RGB + (255,)

if __name__ == "__main__":
    main()
