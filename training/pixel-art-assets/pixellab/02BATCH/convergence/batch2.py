"""The Convergence batch, phase 1: characters, objects, icons, tiles, plates, font, UI, portraits.
Respects the 10-job cap by queueing in waves; pixen icons are synchronous and cheap."""
import os, sys, json, time, base64, traceback
import pl2, plclient as pl
from content2 import CHARS, OBJECTS, ICONS, TILESETS, ROADS, PLATES, PORTRAITS

CAP = 10


def active(st): return sum(1 for j in st["jobs"].values() if j["status"] == "processing")


def wave(st, items, fn):
    """queue items while under the cap; poll in between."""
    items = list(items)
    while items:
        pl2.refresh(st)
        while items and active(st) < CAP:
            key, args = items.pop(0)
            try: fn(st, key, *args)
            except Exception as e: pl2.log("queue error", key, str(e)[:200])
        time.sleep(12)


def main():
    st = pl2.load(); b0 = pl2.balance(); pl2.log("balance", b0)
    # 1. characters (62 gens) — waves of 10
    wave(st, [(k, (d, 64 if k != "irongiant/working_frame" else 96, t)) for k, (d, t) in CHARS.items()], lambda st, k, d, s, t: pl2.q_char(st, k, d, s, t))
    # 2. map objects (~1 gen, ~30 s each)
    wave(st, [(k, (d, 64)) for k, d in OBJECTS.items()], lambda st, k, d, s: pl2.q_object(st, k, d, s))
    # 3. icons (sync)
    for k, d in ICONS.items():
        try: pl2.pixen(st, k, d, 32, 32)
        except Exception as e: pl2.log("icon error", k, str(e)[:200])
    # 4. tilesets + roads
    wave(st, [(k, (lo, up, tr)) for k, (lo, up, tr) in TILESETS.items()], lambda st, k, lo, up, tr: pl2.q_tileset(st, k, lo, up, tr, 32, "standard"))
    wave(st, [(k, (d,)) for k, d in ROADS.items()], lambda st, k, d: pl2.q_tilespro(st, k, d, "square_topdown", 32, "roads"))
    # 5. story-plate backgrounds (pixflux background)
    wave(st, [(k, (d,)) for k, d in PLATES.items()], lambda st, k, d: pl2.q_bg(st, k, "/create-image-pixflux-background", {"description": d, "image_size": {"width": 400, "height": 224}, "seed": 7}, "plate"))
    # 6. font + UI
    wave(st, [("ui/font_postal", ()), ("ui/dialogue_panel", ()), ("ui/bunker_panel", ())], lambda st, k: (
        pl2.q_bg(st, k, "/generate-font-pro", {"description": "weathered stencilled postal service serif, slate blue and brass, slightly worn edges", "weight": "Bold", "glyph_px": 16, "seed": 7, "font_name": "Waylight Postal"}, "font") if k == "ui/font_postal" else
        pl2.q_bg(st, k, "/generate-ui-v2", {"description": "dialogue box panel of dark slate wood with a brass rivet border and a small brass post-horn emblem in the corner, pixel art RPG UI", "image_size": {"width": 512, "height": 160}, "seed": 7, "color_palette": "slate blue, dark wood brown and brass"}, "ui") if k == "ui/dialogue_panel" else
        pl2.q_bg(st, k, "/generate-ui-v2", {"description": "bunker terminal dialogue panel of grey riveted steel with a green phosphor screen inset and a small red maple leaf stencil, pixel art RPG UI", "image_size": {"width": 512, "height": 160}, "seed": 7, "color_palette": "gunmetal grey, phosphor green and one red"}, "ui")))
    # wait for everything so far
    pl2.wait_all(st, limit=2400)
    # 7. portraits from finished characters (25 each)
    for key in PORTRAITS:
        pk = "portraits/" + key.split("/")[-1]
        if pk in st["jobs"]: continue
        src = None
        if key.startswith("party/"): src = f"out/{key.split('/')[1]}/{key.split('/')[1]}_south.png"
        elif key in st["jobs"]: src = pl2.outpath(key, key.split("/")[-1] + "_south.png")
        else: src = f"out/{key}/{key.split('/')[-1]}_south.png"
        if not src or not os.path.exists(src): pl2.log("portrait source missing", key, src); continue
        img = base64.b64encode(open(src, "rb").read()).decode()
        try: pl2.q_bg(st, pk, "/portrait-character-pro", {"direction": "character_to_portrait", "image": {"type": "base64", "base64": img}, "view": "low top-down", "result_size": 64, "seed": 7}, "portrait")
        except Exception as e: pl2.log("portrait error", key, str(e)[:200])
        while active(st) >= CAP: pl2.refresh(st); time.sleep(10)
    pl2.wait_all(st, limit=1800)
    b1 = pl2.balance(); pl2.log("PHASE 1 DONE — spent", b0 - b1, "balance", b1)


if __name__ == "__main__":
    try: main()
    except Exception: traceback.print_exc()
