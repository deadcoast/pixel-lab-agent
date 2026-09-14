"""Acceptance harness for the teal scout robot sample.

Runs the locally decidable criteria declared in .pixl/state.px against a candidate PNG
and writes a JSON receipt plus a contact sheet for the visual criterion.

    python tools/check_sprite.py CANDIDATE.png --out work/receipt.json \
        --sheet work/contact-sheet.png

Criteria implemented here:
  q.canvas   mechanical  single 32x32 frame
  q.palette  mechanical  zero pixels outside #25354A / #56B5BC / #F4DDA2
  q.alpha    mechanical  zero fractional-alpha pixels
  q.nearest  other       8x nearest enlargement adds no colour and tiles uniformly

q.identity (visual) and q.webdisplay (engine) are NOT decided here. This script only
renders the contact sheet an agent or person must actually look at, and reports the
measurements that support -- but cannot replace -- that judgement.
"""
import argparse
import hashlib
import json
import pathlib
import sys
from collections import Counter

from PIL import Image

PALETTE = ["#25354A", "#56B5BC", "#F4DDA2"]
SIZE = (32, 32)
ZOOM = 8


def rgb(hex_color):
    value = hex_color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


# Palette membership is an RGB question. Alpha policy is checked separately by q.alpha,
# so a half-transparent body pixel must fail q.alpha alone and not also q.palette.
ALLOWED = {rgb(c) for c in PALETTE}


def load_frames(path):
    with Image.open(path) as image:
        count = getattr(image, "n_frames", 1)
        frames = []
        for index in range(count):
            image.seek(index)
            frames.append(image.convert("RGBA").copy())
    return frames


def visible(frame):
    return [p for p in frame.getdata() if p[3] != 0]


def check_canvas(frames):
    sizes = [f.size for f in frames]
    ok = len(frames) == 1 and sizes[0] == SIZE
    return ok, {"frame_count": len(frames), "sizes": [list(s) for s in sizes],
                "required": [list(SIZE), "single frame"]}


def check_palette(frame):
    counts = Counter(p[:3] for p in visible(frame))
    outside = sorted(c for c in counts if c not in ALLOWED)
    ok = not outside
    return ok, {
        "visible_colors": len(counts),
        "outside_palette_count": len(outside),
        "outside_palette_pixels": sum(counts[c] for c in outside),
        "outside_palette": ["#%02X%02X%02X" % c for c in outside[:16]],
        "counts": {"#%02X%02X%02X" % c: n for c, n in counts.most_common()},
    }


def check_alpha(frame):
    alphas = Counter(p[3] for p in frame.getdata())
    fractional = sum(n for a, n in alphas.items() if a not in (0, 255))
    return fractional == 0, {"fractional_alpha_pixels": fractional,
                             "alpha_levels": sorted(alphas)}


def check_nearest(frame, zoom=ZOOM):
    """Integer nearest enlargement must add no colour and tile uniformly."""
    big = frame.resize((frame.width * zoom, frame.height * zoom), Image.NEAREST)
    source_colors = set(frame.getdata())
    new_colors = sorted(set(big.getdata()) - source_colors)
    ragged = []
    for y in range(frame.height):
        for x in range(frame.width):
            block = big.crop((x * zoom, y * zoom, (x + 1) * zoom, (y + 1) * zoom))
            distinct = set(block.getdata())
            if len(distinct) != 1 or distinct.pop() != frame.getpixel((x, y)):
                ragged.append([x, y])
    ok = not new_colors and not ragged
    return ok, {"zoom": zoom, "new_colors": len(new_colors),
                "nonuniform_blocks": len(ragged), "first_nonuniform": ragged[:8]}


def checkerboard(size, cell=8):
    board = Image.new("RGBA", size, (255, 255, 255, 255))
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                board.paste((203, 203, 203, 255), (x, y, min(x + cell, size[0]),
                                                   min(y + cell, size[1])))
    return board


def contact_sheet(candidate, reference, path):
    """Reference and candidate at 8x over light, dark and checker backgrounds,
    plus both at native 32x32, in one image to be looked at."""
    pad, zoom = 8, ZOOM
    tile = 32 * zoom
    backgrounds = [("light", (245, 245, 245, 255)), ("dark", (18, 18, 18, 255)),
                   ("checker", None)]
    cols, rows = 2, len(backgrounds)
    width = pad + cols * (tile + pad)
    height = pad + rows * (tile + pad) + 32 + pad * 2
    sheet = Image.new("RGBA", (width, height), (128, 128, 128, 255))
    for row, (_, color) in enumerate(backgrounds):
        y = pad + row * (tile + pad)
        for col, image in enumerate((reference, candidate)):
            x = pad + col * (tile + pad)
            back = (checkerboard((tile, tile)) if color is None
                    else Image.new("RGBA", (tile, tile), color))
            back.alpha_composite(image.resize((tile, tile), Image.NEAREST))
            sheet.paste(back, (x, y))
    y = pad + rows * (tile + pad)
    for col, image in enumerate((reference, candidate)):
        back = Image.new("RGBA", (32, 32), (245, 245, 245, 255))
        back.alpha_composite(image)
        sheet.paste(back, (pad + col * (tile + pad), y))
    sheet.save(path)
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate")
    parser.add_argument("--reference", default="reference.png")
    parser.add_argument("--out")
    parser.add_argument("--sheet")
    args = parser.parse_args(argv)

    frames = load_frames(args.candidate)
    frame = frames[0]
    results = {}
    results["q.canvas"] = check_canvas(frames)
    results["q.palette"] = check_palette(frame)
    results["q.alpha"] = check_alpha(frame)
    results["q.nearest"] = check_nearest(frame)

    receipt = {
        "candidate": args.candidate,
        "sha256": hashlib.sha256(pathlib.Path(args.candidate).read_bytes()).hexdigest(),
        "contract": {"px": list(SIZE), "pl": PALETTE, "al": "binary", "sa": "nearest"},
        "criteria": {k: {"outcome": "pass" if ok else "fail", "measurements": data}
                     for k, (ok, data) in results.items()},
        "not_decided_here": {
            "q.identity": "visual criterion; requires actually viewing the contact sheet",
            "q.webdisplay": "engine criterion; requires the owner's web prototype",
        },
    }
    if args.sheet:
        reference = load_frames(args.reference)[0]
        receipt["contact_sheet"] = contact_sheet(frame, reference, args.sheet)
    text = json.dumps(receipt, indent=2, sort_keys=True)
    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8")
    print(text)
    return 0 if all(ok for ok, _ in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
