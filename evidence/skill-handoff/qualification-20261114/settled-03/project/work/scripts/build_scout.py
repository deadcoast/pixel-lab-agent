"""Deterministic local construction of the scout / medic sample candidates.

This is NOT provider-generated art. It builds a 32x32 side-view figure from
rectangles using the family's working palette so the contract, criteria and
review pipeline can be exercised in this session. Provenance is recorded on the
candidate's X record.

Usage: python -I build_scout.py OUT_PNG [PREVIEW_PNG] [--medic]
"""
import sys
from PIL import Image

TEAL = (0x56, 0xB5, 0xBC, 255)
CREAM = (0xF4, 0xDD, 0xA2, 255)
DARK = (0x25, 0x35, 0x4A, 255)
CLEAR = (0, 0, 0, 0)


def box(px, x0, y0, x1, y1, color):
    """Fill inclusive box [x0..x1] x [y0..y1]."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[x, y] = color


def outlined(px, x0, y0, x1, y1, fill=TEAL, w=2):
    box(px, x0, y0, x1, y1, DARK)
    if x1 - x0 + 1 > 2 * w and y1 - y0 + 1 > 2 * w:
        box(px, x0 + w, y0 + w, x1 - w, y1 - w, fill)


def base(px):
    """Shared family body: facing screen right, feet bottom on row 29."""
    box(px, 9, 3, 12, 10, DARK)    # back ear (solid dark post as in reference)
    box(px, 15, 3, 18, 10, DARK)   # front ear
    outlined(px, 6, 9, 23, 24)     # head/body block, interior x8..21 y11..22
    outlined(px, 22, 13, 27, 20)   # muzzle at the front
    box(px, 22, 15, 23, 18, TEAL)  # open the body wall into the muzzle
    box(px, 18, 13, 19, 16, CREAM)  # eye near the front of the face
    outlined(px, 8, 23, 13, 29)    # back leg
    outlined(px, 16, 23, 21, 29)   # front leg
    box(px, 10, 23, 11, 24, TEAL)  # join legs to body interior
    box(px, 18, 23, 19, 24, TEAL)


def scout(px):
    outlined(px, 2, 12, 7, 21)     # backpack on the back (screen left)
    box(px, 6, 14, 7, 19, TEAL)    # open wall into pack
    box(px, 4, 15, 5, 16, CREAM)   # buckle
    box(px, 8, 13, 17, 14, CREAM)  # goggle strap running to the eye


def medic(px):
    outlined(px, 2, 15, 7, 21)     # small satchel on the back
    box(px, 6, 17, 7, 19, TEAL)    # open wall into satchel
    box(px, 9, 16, 14, 17, CREAM)  # cross horizontal bar
    box(px, 11, 14, 12, 19, CREAM)  # cross vertical bar


def build(role="scout"):
    im = Image.new("RGBA", (32, 32), CLEAR)
    px = im.load()
    base(px)
    (medic if role == "medic" else scout)(px)
    return im


def main(argv):
    role = "medic" if "--medic" in argv else "scout"
    args = [a for a in argv if not a.startswith("--")]
    out = args[0]
    im = build(role)
    im.save(out)
    if len(args) > 1:
        im.resize((256, 256), Image.NEAREST).save(args[1])
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1:])
