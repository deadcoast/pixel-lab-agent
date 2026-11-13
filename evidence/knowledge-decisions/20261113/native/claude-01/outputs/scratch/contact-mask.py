"""Read-only contact/silhouette measurement for the five delivered CF-09 frames.

Pure standard library PNG decode (8-bit RGBA/RGB, non-interlaced). Imports nothing
from the consumer. It measures the opaque alpha mask per frame, whether every
frame's mask is identical, the lowest opaque row and its column extent (the
lower contact edge), and the per-frame cyan column extent. Measurements only;
they are not artistic acceptance.
"""
import hashlib
import json
import struct
import sys
import zlib


def decode_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", path
    pos = 8
    idat = b""
    width = height = bit_depth = color_type = interlace = None
    palette = None
    trns = None
    while pos < len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if ctype == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif ctype == b"PLTE":
            palette = [tuple(body[i:i + 3]) for i in range(0, len(body), 3)]
        elif ctype == b"tRNS":
            trns = body
        elif ctype == b"IDAT":
            idat += body
        elif ctype == b"IEND":
            break
    assert bit_depth == 8 and interlace == 0, (path, bit_depth, interlace)
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color_type]
    raw = zlib.decompress(idat)
    stride = width * channels
    rows = []
    prev = bytearray(stride)
    i = 0
    for _ in range(height):
        ftype = raw[i]
        i += 1
        cur = bytearray(raw[i:i + stride])
        i += stride
        for x in range(stride):
            a = cur[x - channels] if x >= channels else 0
            b = prev[x]
            c = prev[x - channels] if x >= channels else 0
            if ftype == 1:
                cur[x] = (cur[x] + a) & 255
            elif ftype == 2:
                cur[x] = (cur[x] + b) & 255
            elif ftype == 3:
                cur[x] = (cur[x] + ((a + b) >> 1)) & 255
            elif ftype == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                cur[x] = (cur[x] + pred) & 255
        rows.append(bytes(cur))
        prev = cur
    pixels = []
    for row in rows:
        out = []
        for x in range(width):
            px = row[x * channels:(x + 1) * channels]
            if color_type == 6:
                out.append(tuple(px))
            elif color_type == 2:
                out.append((px[0], px[1], px[2], 255))
            elif color_type == 3:
                r, g, b = palette[px[0]]
                a = trns[px[0]] if trns and px[0] < len(trns) else 255
                out.append((r, g, b, a))
            elif color_type == 4:
                out.append((px[0], px[0], px[0], px[1]))
            else:
                out.append((px[0], px[0], px[0], 255))
        pixels.append(out)
    return width, height, pixels


def main(paths):
    report = {"frames": [], "all_masks_identical": None, "contact_rows_identical": None}
    masks = []
    contacts = []
    for path in paths:
        w, h, px = decode_png(path)
        mask = tuple(tuple(1 if p[3] > 0 else 0 for p in row) for row in px)
        masks.append(mask)
        opaque_rows = [y for y in range(h) if any(mask[y])]
        bottom = max(opaque_rows)
        bottom_cols = [x for x in range(w) if mask[bottom][x]]
        colors = {}
        for row in px:
            for p in row:
                if p[3] > 0:
                    colors[p] = colors.get(p, 0) + 1
        cyan_rows = [y for y in range(h) for x in range(w) if px[y][x][3] > 0 and px[y][x][2] > px[y][x][0] + 60 and px[y][x][1] > 120]
        cyan_cols = [x for y in range(h) for x in range(w) if px[y][x][3] > 0 and px[y][x][2] > px[y][x][0] + 60 and px[y][x][1] > 120]
        contact = (bottom, bottom_cols[0], bottom_cols[-1], len(bottom_cols))
        contacts.append(contact)
        report["frames"].append({
            "path": path,
            "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(),
            "size": [w, h],
            "opaque_pixels": sum(sum(r) for r in mask),
            "top_opaque_row": min(opaque_rows),
            "bottom_opaque_row": bottom,
            "bottom_row_cols": [bottom_cols[0], bottom_cols[-1]],
            "bottom_row_width": len(bottom_cols),
            "colors": {"#%02x%02x%02x%02x" % k: v for k, v in sorted(colors.items())},
            "cyan_rows": [min(cyan_rows), max(cyan_rows)] if cyan_rows else None,
            "cyan_cols": [min(cyan_cols), max(cyan_cols)] if cyan_cols else None,
            "cyan_height": (max(cyan_rows) - min(cyan_rows) + 1) if cyan_rows else 0,
        })
    report["all_masks_identical"] = all(m == masks[0] for m in masks)
    report["contact_rows_identical"] = all(c == contacts[0] for c in contacts)
    report["mask_diff_pixels_vs_frame0"] = [sum(1 for y in range(len(m)) for x in range(len(m[0])) if m[y][x] != masks[0][y][x]) for m in masks]
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
