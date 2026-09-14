"""03BATCH runner, phase 1 — creations. Resumable: every job lands in pl3_state.json; re-running skips finished keys.
Respects the 10-job cap by queueing in waves. Logs the balance after every wave so each asset class gets a measured cost."""
import os, sys, json, time, base64, traceback
import pl2, plclient as pl
from content3 import CHARS, OBJECTS, OBJECTS8, ICONS, EMBLEMS, TILESETS, ROADS, BUILDINGS, PLATES, UI, FONTS, PORTRAITS

pl2.OUT = "out3"; pl2.STATE = "pl3_state.json"
CAP = 10
INV = json.load(open("inventory.json"))


def active(st): return sum(1 for j in st["jobs"].values() if j["status"] == "processing")


def wave(st, items, fn, label):
    items = [(k, a) for k, a in items if k not in st["jobs"] or st["jobs"][k]["status"] == "failed"]
    if not items: return
    b0 = pl2.balance(); n = 0
    while items:
        pl2.refresh(st)
        while items and active(st) < CAP:
            key, args = items.pop(0)
            if key in st["jobs"] and st["jobs"][key]["status"] == "failed": del st["jobs"][key]
            try: fn(st, key, *args); n += 1
            except Exception as e: pl2.log("queue error", key, str(e)[:300])
        time.sleep(12)
    pl2.wait_all(st, limit=2400)
    b1 = pl2.balance(); pl2.log(f"WAVE {label}: {n} queued, spent {b0 - b1}, balance {b1}")
    st.setdefault("costs", {})[label] = {"n": n, "spent": b0 - b1}; pl2.save(st)


# --- extra queue functions -------------------------------------------------------------------------------------------
def q_object8(st, key, desc, size=96, view="high top-down", seed=7):
    if key in st["jobs"]: return
    r = pl2.post("/create-8-direction-object", {"description": desc, "size": size, "view": view, "seed": seed})
    st["jobs"][key] = {"type": "object8", "id": r.get("object_id"), "job": r.get("background_job_id"), "status": "processing"}; pl2.save(st); pl2.log("queued object8", key)


def q_building(st, key, wall, floor, roof, tile_type="square_topdown", tile_size=32, seed=7):
    if key in st["jobs"]: return
    body = {"description": f"{wall}, {floor}", "tile_type": tile_type, "tile_size": tile_size, "tile_view": "high top-down", "tile_feature": "building",
            "building_wall_description": wall, "building_floor_description": floor, "building_floor2_description": roof, "building_wall_tiles": 2, "seed": seed}
    r = pl2.post("/create-tiles-pro", body)
    tid = r.get("tile_id") or r.get("id")
    st["jobs"][key] = {"type": "tilespro", "id": tid, "status": "processing", "raw": r}; pl2.save(st); pl2.log("queued building kit", key, tid)


def refresh_extra(st):
    """object8 jobs are not handled by pl2.refresh — poll them here."""
    for key, j in st["jobs"].items():
        if j["status"] != "processing" or j["type"] != "object8": continue
        try:
            d = pl2.get(f"/objects/{j['id']}")
            s = d.get("status")
            if s == "completed" and d.get("rotation_urls"):
                name = key.split("/")[-1]; ims = {}
                for dname, u in d["rotation_urls"].items():
                    if u: ims[dname] = pl2.fetch(u); ims[dname].save(pl2.outpath(key, f"{name}_{dname}.png"))
                order = [x for x in pl.DIRS if x in ims]
                if order:
                    from PIL import Image
                    w = max(i.width for i in ims.values()); h = max(i.height for i in ims.values())
                    sheet = Image.new("RGBA", (w * len(order), h), (0, 0, 0, 0))
                    for i, dn in enumerate(order): sheet.paste(ims[dn], (i * w, 0), ims[dn])
                    sheet.save(pl2.outpath(key, f"{name}_rotations.png"))
                json.dump({k: v for k, v in d.items() if k not in ("rotation_urls", "storage_urls")}, open(pl2.outpath(key, "meta.json"), "w"), indent=1, default=str)
                j["status"] = "done"; pl2.log("object8 done", key, len(ims), "dirs")
            elif s == "failed": j["status"] = "failed"; pl2.log("object8 FAILED", key, str(d)[:200])
            elif s == "review": j["status"] = "failed"; pl2.log("object8 in review (unexpected)", key)
        except Exception as e: pl2.log("refresh error", key, str(e)[:200])
    pl2.save(st)


_refresh = pl2.refresh
def refresh_all(st): _refresh(st); refresh_extra(st)
pl2.refresh = refresh_all


def char_source(key, st):
    """south-facing sprite for a portrait: 03BATCH out3, 02BATCH out2, 01BATCH out/<fac>/<name> or out/<name>."""
    fac, name = key.split("/")
    for p in (f"out3/{fac}/{name}/{name}_south.png", f"out2/{fac}/{name}/{name}_south.png", f"out/{fac}/{name}/{name}_south.png", f"out/{name}/{name}_south.png"):
        if os.path.exists(p): return p
    return None


def main():
    st = pl2.load(); b0 = pl2.balance(); pl2.log("03BATCH phase 1 — balance", b0)
    # duplicate guard: refuse any key that 01/02BATCH already made
    dup = [k for k in list(CHARS) if k in INV["chars"]] + [k for k, _, _ in OBJECTS if k.split("/")[1] in INV["objects"]] + [k for k in ICONS if k.split("/")[1] in INV["icons"]] + [k for k in list(TILESETS) + list(ROADS) if k.split("/")[1] in INV["tiles"]] + [k for k in PLATES if k.split("/")[1] in INV["plates"]] + [k for k in PORTRAITS if k.split("/")[1] in INV["portraits"]]
    if dup: pl2.log("DUPLICATES refused:", dup); sys.exit(1)
    # 1. characters
    wave(st, [(k, (d, 64, t)) for k, (d, t) in CHARS.items()], lambda st, k, d, s, t: pl2.q_char(st, k, d, s, t), "characters")
    # 2. map objects, by size so a wave measures one cost
    for size in (64, 96, 128):
        wave(st, [(k, (d, size)) for k, d, s in OBJECTS if s == size], lambda st, k, d, s: pl2.q_object(st, k, d, s), f"objects_{size}")
    # 3. icons + emblems (sync pixen)
    b = pl2.balance()
    for k, d in list(ICONS.items()) + list(EMBLEMS.items()):
        if k in st["jobs"] and st["jobs"][k]["status"] == "done": continue
        try: pl2.pixen(st, k, d, 32, 32)
        except Exception as e: pl2.log("icon error", k, str(e)[:200])
    pl2.log("icons+emblems spent", b - pl2.balance())
    # 4. tilesets + roads
    wave(st, [(k, (lo, up, tr)) for k, (lo, up, tr) in TILESETS.items()], lambda st, k, lo, up, tr: pl2.q_tileset(st, k, lo, up, tr, 32, "standard"), "tilesets")
    wave(st, [(k, (d,)) for k, d in ROADS.items()], lambda st, k, d: pl2.q_tilespro(st, k, d, "square_topdown", 32, "roads"), "roads")
    # 5. building kit probe, then the rest if the price is sane
    kits = list(BUILDINGS.items())
    wave(st, [(kits[0][0], kits[0][1])], lambda st, k, w, f, r: q_building(st, k, w, f, r), "building_probe")
    probe = st.get("costs", {}).get("building_probe", {}).get("spent", 999)
    if probe <= 45 and st["jobs"].get(kits[0][0], {}).get("status") == "done" and pl2.balance() > 1100:
        wave(st, [(k, v) for k, v in kits[1:]], lambda st, k, w, f, r: q_building(st, k, w, f, r), "building_kits")
    else: pl2.log("building kits skipped after probe: spent", probe, "status", st["jobs"].get(kits[0][0], {}).get("status"))
    # 6. 8-direction objects
    wave(st, [(k, (d, s)) for k, (d, s) in OBJECTS8.items()], lambda st, k, d, s: q_object8(st, k, d, s), "objects8")
    # 7. plates
    wave(st, [(k, (d,)) for k, d in PLATES.items()], lambda st, k, d: pl2.q_bg(st, k, "/create-image-pixflux-background", {"description": d, "image_size": {"width": 400, "height": 224}, "seed": 7}, "plate"), "plates")
    # 8. UI + font
    wave(st, [(k, (b,)) for k, b in UI.items()], lambda st, k, b: pl2.q_bg(st, k, "/generate-ui-v2", b, "ui"), "ui")
    wave(st, [(k, (b,)) for k, b in FONTS.items()], lambda st, k, b: pl2.q_bg(st, k, "/generate-font-pro", b, "font"), "font")
    # 9. portraits
    items = []
    for key in PORTRAITS:
        pk = "portraits/" + key.split("/")[-1]
        src = char_source(key, st)
        if not src: pl2.log("portrait source missing", key); continue
        img = base64.b64encode(open(src, "rb").read()).decode()
        items.append((pk, ({"direction": "character_to_portrait", "image": {"type": "base64", "base64": img}, "view": "low top-down", "result_size": 64, "seed": 7},)))
    wave(st, items, lambda st, k, b: pl2.q_bg(st, k, "/portrait-character-pro", b, "portrait"), "portraits")
    b1 = pl2.balance(); pl2.log("PHASE 1 DONE — spent", b0 - b1, "balance", b1)
    st["phase1"] = {"spent": b0 - b1, "balance": b1}; pl2.save(st)


if __name__ == "__main__":
    try: main()
    except Exception: traceback.print_exc()
