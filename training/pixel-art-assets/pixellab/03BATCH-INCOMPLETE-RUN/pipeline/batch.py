"""sheet writer for animations (extracted from the 01BATCH runner)."""
import os, json
import plclient as pl
from PIL import Image


def save_anim(anim, out_dir, name, aname):
    os.makedirs(out_dir, exist_ok=True)
    fb = {d["direction"]: [pl.fetch_png(u) for u in d["frames"]] for d in anim["directions"]}
    order = [d for d in pl.DIRS if d in fb]; n = min(len(v) for v in fb.values()); w, h = fb[order[0]][0].size
    sh = Image.new("RGBA", (w * n, h * len(order)), (0, 0, 0, 0))
    for r, d in enumerate(order):
        for k in range(n): sh.paste(fb[d][k], (k * w, r * h))
    sh.save(f"{out_dir}/{name}_{aname}_sheet.png")
    gifs = []
    for k in range(n):
        g = Image.new("RGB", (w * len(order) * 3, h * 3), (36, 34, 40))
        for i, d in enumerate(order):
            im = fb[d][k].resize((w * 3, h * 3), Image.NEAREST); g.paste(im, (i * w * 3, 0), im)
        gifs.append(g)
    gifs[0].save(f"{out_dir}/{name}_{aname}_x3.gif", save_all=True, append_images=gifs[1:], duration=110, loop=0)
    json.dump({"frames": n, "w": w, "h": h, "directions": order}, open(f"{out_dir}/{name}_{aname}.json", "w"))


