"""Produce the outline/display-scale comparison sheet and check it mechanically.

Only the supplied reference bytes are used. Enlargement is integer nearest-neighbour,
so no colour is invented and no content is resampled.
"""
import json
from PIL import Image, ImageDraw

ZOOMS = [1, 2, 3, 4, 6, 8]
BANDS = [
    ("light", (0xEC, 0xEF, 0xF2, 255)),
    ("dark", (0x12, 0x16, 0x1B, 255)),
    ("busy", None),  # checker, generated below
]
GAP, PAIR_GAP, MARGIN, LABEL_H = 22, 10, 16, 14
SRC = [("outlined  (reference.png)", "reference.png"),
       ("no outline  (reference-b.png)", "reference-b.png")]

imgs = {p: Image.open(p).convert("RGBA") for _, p in SRC}
W, H = imgs["reference.png"].size


def busy_tile(w, h):
    """A deliberately noisy background: 4px checker plus a mid-value stripe."""
    t = Image.new("RGBA", (w, h))
    px = t.load()
    for y in range(h):
        for x in range(w):
            c = 0x6B if ((x // 4) + (y // 4)) % 2 else 0x8A
            if (x + y) % 11 < 2:
                c = 0xA8
            px[x, y] = (c, c - 12, c + 14, 255)
    return t


# ---- layout ----
band_w = MARGIN
for z in ZOOMS:
    band_w += W * z * 2 + PAIR_GAP + GAP
band_w += MARGIN - GAP
band_h = H * max(ZOOMS) + LABEL_H + GAP
sheet_h = MARGIN + LABEL_H + len(BANDS) * band_h + MARGIN

sheet = Image.new("RGBA", (band_w, sheet_h), (0x20, 0x24, 0x2A, 255))
draw = ImageDraw.Draw(sheet)
draw.text((MARGIN, 4),
          "outline treatment x display scale  |  left = outlined, right = no outline  "
          "|  native pixels, nearest-neighbour integer zoom only",
          fill=(0xE8, 0xEC, 0xF0, 255))

placements = []  # (dest_x, dest_y, zoom, source_path) for the mechanical check
y = MARGIN + LABEL_H

for name, colour in BANDS:
    if colour is None:
        band = busy_tile(band_w, band_h)
    else:
        band = Image.new("RGBA", (band_w, band_h), colour)
    sheet.alpha_composite(band, (0, y))
    label_fill = (0x20, 0x24, 0x2A, 255) if name == "light" else (0xE8, 0xEC, 0xF0, 255)
    draw.text((MARGIN, y + 2), f"{name} background", fill=label_fill)

    x = MARGIN
    base = y + band_h - GAP // 2
    for z in ZOOMS:
        draw.text((x, y + LABEL_H + 2), f"{z}x", fill=label_fill)
        for _, path in SRC:
            big = imgs[path].resize((W * z, H * z), Image.NEAREST)
            dy = base - H * z
            sheet.alpha_composite(big, (x, dy))
            placements.append((x, dy, z, path))
            x += W * z + PAIR_GAP
        x += GAP - PAIR_GAP
    y += band_h

sheet.convert("RGB").save("deliverables/outline-scale-comparison.png")

# ---- mechanical check: q_aid_faithful ----
sp = sheet.load()
src_px = {p: imgs[p].load() for p in imgs}
uniform_fail = colour_fail = blocks = 0
src_colours = {p: {imgs[p].getpixel((a, b)) for a in range(W) for b in range(H)}
               for p in imgs}

for dx, dy, z, path in placements:
    s = src_px[path]
    for sy in range(H):
        for sx in range(W):
            expect = s[sx, sy]
            if expect[3] == 0:
                continue  # transparent source pixel: background shows through
            blocks += 1
            if expect not in src_colours[path]:
                colour_fail += 1
            for oy in range(z):
                for ox in range(z):
                    if sp[dx + sx * z + ox, dy + sy * z + oy] != expect:
                        uniform_fail += 1
                        break
                else:
                    continue
                break

result = {
    "criterion": "q_aid_faithful",
    "candidate": "x_aid",
    "candidate_path": "deliverables/outline-scale-comparison.png",
    "mode": "local",
    "zoom_levels": ZOOMS,
    "backgrounds": [b[0] for b in BANDS],
    "panels": len(placements),
    "opaque_source_pixels_checked": blocks,
    "non_uniform_blocks": uniform_fail,
    "blocks_with_colour_absent_from_source": colour_fail,
    "outcome": "pass" if uniform_fail == 0 and colour_fail == 0 else "fail",
    "note": "Verifies enlargement fidelity only. It says nothing about which outline "
            "treatment the project should adopt.",
}
json.dump(result, open("evidence/aid-faithfulness.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(result, indent=1))
