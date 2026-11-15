import sys
from PIL import Image
from collections import Counter
root = sys.argv[1]
for name in ("reference.png", "reference-b.png"):
    im = Image.open(f"{root}/{name}").convert("RGBA")
    w, h = im.size
    px = im.load()
    print("==", name, im.size)
    colors = Counter(px[x, y] for y in range(h) for x in range(w) if px[x, y][3] > 0)
    print("colors:", colors.most_common())
    keys = {c: chr(ord('A') + i) for i, (c, _) in enumerate(colors.most_common())}
    for y in range(h):
        print("%2d " % y + "".join(keys[px[x, y]] if px[x, y][3] > 0 else "." for x in range(w)))
    big = im.resize((w * 8, h * 8), Image.NEAREST)
    big.save(f"{root}/work/{name[:-4]}-x8.png")
