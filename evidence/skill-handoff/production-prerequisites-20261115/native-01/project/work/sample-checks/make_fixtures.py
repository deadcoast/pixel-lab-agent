"""Synthetic failing fixtures for the sample mechanical harness (2026-11-15d).

Each fixture is derived from reference.png bytes so that exactly one condition is broken:
  fixture-33x33.png            canvas 33 x 33 (figure unchanged, one transparent row/col added)
  fixture-offpalette.png       32 x 32, one body pixel recoloured to #FF00FF
  fixture-fractional-alpha.png 32 x 32, one body pixel given alpha 128
These are test fixtures for the tooling only. They are not candidates, references or evidence.

Usage (consumer root, selected interpreter):
  python -I work/sample-checks/make_fixtures.py
"""
import hashlib
import json

from PIL import Image

SOURCE = "reference.png"
SOURCE_SHA = "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7"
OUT = "work/sample-checks/"


def sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def first_body_pixel(img):
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if px[x, y][:3] == (0x56, 0xB5, 0xBC) and px[x, y][3] == 255:
                return x, y
    raise SystemExit("no teal body pixel found")


def main():
    assert sha(SOURCE) == SOURCE_SHA, "reference.png bytes drifted; fixtures not built"
    base = Image.open(SOURCE).convert("RGBA")
    made = {}

    big = Image.new("RGBA", (33, 33), (0, 0, 0, 0))
    big.paste(base, (0, 0))
    p = OUT + "fixture-33x33.png"
    big.save(p)
    made[p] = {"breaks": "q_sample_canvas (size)", "sha256": sha(p)}

    off = base.copy()
    x, y = first_body_pixel(off)
    off.putpixel((x, y), (0xFF, 0x00, 0xFF, 255))
    p = OUT + "fixture-offpalette.png"
    off.save(p)
    made[p] = {"breaks": "q_sample_palette (one #FF00FF pixel)", "pixel": [x, y], "sha256": sha(p)}

    frac = base.copy()
    x, y = first_body_pixel(frac)
    frac.putpixel((x, y), (0x56, 0xB5, 0xBC, 128))
    p = OUT + "fixture-fractional-alpha.png"
    frac.save(p)
    made[p] = {"breaks": "q_sample_canvas (one alpha-128 pixel)", "pixel": [x, y], "sha256": sha(p)}

    with open(OUT + "fixtures.json", "w", encoding="utf-8", newline="\n") as handle:
        json.dump({"source": SOURCE, "source_sha256": SOURCE_SHA, "fixtures": made}, handle, indent=1)
        handle.write("\n")
    print(json.dumps(made, indent=1))


if __name__ == "__main__":
    main()
