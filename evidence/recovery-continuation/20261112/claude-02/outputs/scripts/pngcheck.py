"""Pure-Python PNG structural check (signature, chunks, CRCs, IHDR, IDAT inflate)."""
import hashlib
import json
import struct
import sys
import zlib
from datetime import datetime, timezone

path = sys.argv[1]
data = open(path, "rb").read()
out = {"path": sys.argv[2], "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
       "checked_at": datetime.now(timezone.utc).isoformat()}
sig = data[:8] == b"\x89PNG\r\n\x1a\n"
out["signature_ok"] = sig
chunks = []
pos = 8
crc_ok = True
idat = b""
ihdr = None
while pos + 8 <= len(data):
    length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
    body = data[pos + 8:pos + 8 + length]
    crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
    calc = zlib.crc32(ctype + body) & 0xFFFFFFFF
    ok = calc == crc and len(body) == length
    crc_ok = crc_ok and ok
    chunks.append({"type": ctype.decode("latin1"), "length": length, "crc_ok": ok})
    if ctype == b"IHDR":
        w, h, bd, ct, cm, fm, il = struct.unpack(">IIBBBBB", body)
        ihdr = {"width": w, "height": h, "bit_depth": bd, "color_type": ct,
                "compression": cm, "filter": fm, "interlace": il}
    if ctype == b"IDAT":
        idat += body
    pos += 12 + length
out["chunks"] = chunks
out["all_crc_ok"] = crc_ok
out["ends_with_iend"] = bool(chunks) and chunks[-1]["type"] == "IEND"
out["trailing_bytes"] = len(data) - pos
out["ihdr"] = ihdr
try:
    raw = zlib.decompress(idat)
    out["idat_inflate_ok"] = True
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ihdr["color_type"]]
    bpp = max(1, channels * ihdr["bit_depth"] // 8)
    rowlen = 1 + (ihdr["width"] * channels * ihdr["bit_depth"] + 7) // 8
    out["expected_raw_bytes"] = rowlen * ihdr["height"]
    out["actual_raw_bytes"] = len(raw)
    out["raw_length_ok"] = len(raw) == rowlen * ihdr["height"]
    out["filter_bytes_valid"] = all(raw[i] <= 4 for i in range(0, len(raw), rowlen))
except Exception as e:  # noqa: BLE001
    out["idat_inflate_ok"] = False
    out["idat_error"] = repr(e)
out["decodes_as_32x32_png"] = bool(sig and crc_ok and ihdr and ihdr["width"] == 32 and ihdr["height"] == 32
                                   and out.get("idat_inflate_ok") and out.get("raw_length_ok")
                                   and out["ends_with_iend"] and out["trailing_bytes"] == 0)
print(json.dumps(out, indent=2))
