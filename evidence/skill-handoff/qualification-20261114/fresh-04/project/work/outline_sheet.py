"""Local diagnostic: both references at native and 4x on light, dark and busy backgrounds.
No new art is authored; pixels are copied from the reference files unchanged."""
import sys
from PIL import Image, ImageDraw
root = sys.argv[1]
refs = [("reference.png", "A: continuous 2px outline"), ("reference-b.png", "B: no outline")]
bgs = [("light", (236, 232, 220, 255)), ("dark", (28, 30, 38, 255)), ("mid-teal", (70, 150, 160, 255)), ("busy", None)]
def busy(w, h):
    im = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            c = (120, 110, 90, 255) if ((x // 4 + y // 4) % 2 == 0) else (60, 80, 70, 255)
            d.rectangle([x, y, x + 3, y + 3], fill=c)
    return im
cell = 32; scale = 4; pad = 8
cols = len(bgs); rows = len(refs)
W = pad + cols * (cell * scale + pad); H = pad + rows * (cell * scale + cell + pad * 2)
sheet = Image.new("RGBA", (W, H), (255, 255, 255, 255))
for ri, (name, label) in enumerate(refs):
    src = Image.open(f"{root}/{name}").convert("RGBA")
    for ci, (bname, color) in enumerate(bgs):
        x0 = pad + ci * (cell * scale + pad); y0 = pad + ri * (cell * scale + cell + pad * 2)
        big_bg = busy(cell * scale, cell * scale) if color is None else Image.new("RGBA", (cell * scale, cell * scale), color)
        big_bg.alpha_composite(src.resize((cell * scale, cell * scale), Image.NEAREST))
        sheet.alpha_composite(big_bg, (x0, y0))
        nat_bg = busy(cell, cell) if color is None else Image.new("RGBA", (cell, cell), color)
        nat_bg.alpha_composite(src)
        sheet.alpha_composite(nat_bg, (x0, y0 + cell * scale + pad))
sheet.save(f"{root}/research/outline-comparison-sheet.png")
print("saved", sheet.size, "rows:", [l for _, l in refs], "cols:", [b for b, _ in bgs], "layout: 4x on top, native 1x below each")
