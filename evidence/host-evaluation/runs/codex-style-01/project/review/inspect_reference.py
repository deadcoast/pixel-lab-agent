"""Reference measurement and viewing aid; does not author or alter source art."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
source = root / "translucent-reference.png"
out = root / "review"
out.mkdir(exist_ok=True)
im = Image.open(source).convert("RGBA")
counts = Counter(im.getdata())
alpha = Counter(p[3] for p in im.getdata())
partial = [{"x": x, "y": y, "rgba": list(im.getpixel((x,y)))}
           for y in range(im.height) for x in range(im.width)
           if 0 < im.getpixel((x,y))[3] < 255]
stats = {
    "source": source.name, "sha256": sha256(source.read_bytes()).hexdigest(),
    "size": list(im.size), "mode": im.mode, "visible_bbox_exclusive": im.getbbox(),
    "visible_pixels": sum(n for p,n in counts.items() if p[3]),
    "visible_rgb_colors": len({p[:3] for p in counts if p[3]}),
    "alpha_histogram": dict(sorted(alpha.items())),
    "visible_rgba_counts": [{"rgba": list(p), "count": n} for p,n in sorted(counts.items()) if p[3]],
    "partial_alpha_pixels": partial,
    "notes": "Measurements of reference only; no artistic or engine acceptance. RGB colors and alpha levels are descriptive, not a required palette."
}
(out / "reference-measurements.json").write_text(json.dumps(stats, indent=2)+"\n", encoding="utf-8")

# A diagnostic contact sheet: source pixels composited, then enlarged with nearest.
sheet = Image.new("RGB", (840, 350), "#cccccc")
draw = ImageDraw.Draw(sheet)
for col, (label, color) in enumerate([("Light #F0E8D8", "#f0e8d8"), ("Dark #18222E", "#18222e"), ("Checker #809090 / #B0C0C0", None)]):
    bg = Image.new("RGBA", im.size, color or "#809090")
    if color is None:
        bdraw = ImageDraw.Draw(bg)
        for y in range(0, im.height, 4):
            for x in range(0, im.width, 4):
                if (x//4+y//4)%2:
                    bdraw.rectangle((x,y,x+3,y+3), fill="#b0c0c0")
    comp = Image.alpha_composite(bg, im).convert("RGB")
    left = col*280+12
    draw.text((left, 8), label, fill="black")
    sheet.paste(comp.resize((256,256), Image.Resampling.NEAREST), (left,30))
    sheet.paste(comp, (left,302))
    draw.text((left+40, 312), "1x source; above 8x", fill="black")
sheet.save(out / "reference-inspection.png")
print(json.dumps({k:v for k,v in stats.items() if k != "partial_alpha_pixels"}, indent=2))
print("Partial alpha rows:", dict(sorted(Counter(p["y"] for p in partial).items())))
