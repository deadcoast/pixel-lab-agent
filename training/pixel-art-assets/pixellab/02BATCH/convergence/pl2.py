"""pl2 — generic PixelLab job framework: characters, map objects, pixen images, tilesets, tiles-pro, background jobs (font/ui/portrait/background).
State in a JSON file; every job records type, ids, status, cost delta when measurable. Concurrency cap respected via 429 retry."""
import os, sys, json, time, io, base64, traceback
import requests
from PIL import Image
import plclient as pl

BASE = pl.BASE; H = pl.H
OUT = "out2"; STATE = "pl2_state.json"


def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)


def load(): return json.load(open(STATE)) if os.path.exists(STATE) else {"jobs": {}}


def save(st): json.dump(st, open(STATE, "w"), indent=1)


def post(path, body):
    while True:
        r = requests.post(BASE + path, headers=H, json=body, timeout=180)
        if r.status_code == 429: time.sleep(20); continue
        if r.status_code >= 400: raise RuntimeError(f"{path} {r.status_code}: {r.text[:500]}")
        return r.json()


def get(path):
    r = requests.get(BASE + path, headers=H, timeout=90)
    if r.status_code >= 400: raise RuntimeError(f"{path} {r.status_code}: {r.text[:300]}")
    return r.json()


def b64png(s):
    if isinstance(s, dict): s = s.get("base64") or s.get("data") or ""
    if s.startswith("data:"): s = s.split(",", 1)[1]
    return Image.open(io.BytesIO(base64.b64decode(s))).convert("RGBA")


def fetch(url):
    r = requests.get(url, timeout=90); r.raise_for_status(); return Image.open(io.BytesIO(r.content)).convert("RGBA")


def balance(): return get("/balance")["subscription"]["generations"]


def outpath(key, *parts):
    p = os.path.join(OUT, *key.split("/")); os.makedirs(p, exist_ok=True)
    return os.path.join(p, *parts)


# ----------------------------------------------------------------- queue --
def q_char(st, key, desc, size=64, template="mannequin", seed=7, view="low top-down"):
    if key in st["jobs"]: return
    r = post("/create-character-v3", {"description": desc, "image_size": {"width": size, "height": size}, "view": view, "template_id": template, "no_background": True, "seed": seed, "name": key})
    st["jobs"][key] = {"type": "char", "id": r["character_id"], "status": "processing", "size": size}; save(st); log("queued char", key)


def q_object(st, key, desc, size=64, view="high top-down", seed=7):
    if key in st["jobs"]: return
    r = post("/map-objects", {"description": desc, "image_size": {"width": size, "height": size}, "view": view, "seed": seed})
    st["jobs"][key] = {"type": "object", "id": r["object_id"], "status": "processing"}; save(st); log("queued object", key)


def pixen(st, key, desc, w=32, h=32, view=None, seed=7, no_bg=True):
    if key in st["jobs"] and st["jobs"][key]["status"] == "done": return
    body = {"description": desc, "image_size": {"width": w, "height": h}, "no_background": no_bg, "seed": seed, "detail": "highly detailed"}
    if view: body["view"] = view
    r = post("/create-image-pixen", body)
    im = b64png(r["image"]); im.save(outpath(key, key.split("/")[-1] + ".png"))
    st["jobs"][key] = {"type": "pixen", "status": "done", "usage": r.get("usage")}; save(st); log("pixen done", key)


def q_tileset(st, key, lower, upper, transition="", tile=32, mode="standard", seed=7, view="high top-down"):
    if key in st["jobs"]: return
    body = {"lower_description": lower, "upper_description": upper, "transition_description": transition, "tile_size": {"width": tile, "height": tile}, "mode": mode, "seed": seed, "view": view}
    r = post("/create-tileset", body)
    tid = r.get("tileset_id") or r.get("id") or (r.get("tileset") or {}).get("id")
    st["jobs"][key] = {"type": "tileset", "id": tid, "status": "processing", "raw": {k: v for k, v in r.items() if k != "tileset"}}; save(st); log("queued tileset", key, tid)


def q_tilespro(st, key, desc, tile_type="square_topdown", tile_size=32, tile_feature=None, view="high top-down", seed=7):
    if key in st["jobs"]: return
    body = {"description": desc, "tile_type": tile_type, "tile_size": tile_size, "tile_view": view, "seed": seed}
    if tile_feature: body["tile_feature"] = tile_feature
    r = post("/create-tiles-pro", body)
    tid = r.get("tile_id") or r.get("id") or r.get("tiles_pro_id")
    st["jobs"][key] = {"type": "tilespro", "id": tid, "status": "processing", "raw": r}; save(st); log("queued tiles-pro", key, tid)


def q_bg(st, key, path, body, kind):
    if key in st["jobs"]: return
    r = post(path, body)
    jid = r.get("background_job_id") or r.get("job_id") or r.get("id")
    st["jobs"][key] = {"type": kind, "id": jid, "status": "processing", "raw": {k: v for k, v in r.items() if k not in ("image",)}}; save(st); log("queued", kind, key, jid)


# ----------------------------------------------------------------- poll ---
def save_any(key, obj, tag="result"):
    """dig images out of an arbitrary job response: base64 images, urls, ttf."""
    n = 0
    def walk(o, path):
        nonlocal n
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("base64", "image") and isinstance(v, (str, dict)):
                    try: im = b64png(v); im.save(outpath(key, f"{tag}_{n}.png")); n += 1
                    except Exception: pass
                elif k == "ttf_base64" and isinstance(v, str):
                    open(outpath(key, key.split("/")[-1] + ".ttf"), "wb").write(base64.b64decode(v)); n += 1
                elif isinstance(v, str) and v.startswith("http") and (".png" in v or "download" in v or "b2" in v or "backblaze" in v):
                    try: fetch(v).save(outpath(key, f"{tag}_{k}_{n}.png")); n += 1
                    except Exception: pass
                else: walk(v, path + [k])
        elif isinstance(o, list):
            for i, v in enumerate(o): walk(v, path + [i])
    walk(obj, [])
    return n


def refresh(st):
    for key, j in st["jobs"].items():
        if j["status"] != "processing": continue
        try:
            t = j["type"]
            if t == "char":
                d = pl.character(j["id"])
                if d.get("status") == "completed" and d.get("rotation_urls"):
                    pl.save_rotations(d, outpath(key), key.split("/")[-1]); j["status"] = "done"; log("char done", key)
                elif d.get("status") == "failed": j["status"] = "failed"; log("char FAILED", key)
            elif t == "object":
                d = get(f"/map-objects/{j['id']}")
                if d.get("status") == "completed" and d.get("download_url"):
                    fetch(d["download_url"]).save(outpath(key, key.split("/")[-1] + ".png")); j["status"] = "done"; log("object done", key)
                elif d.get("status") == "failed": j["status"] = "failed"; log("object FAILED", key, str(d)[:200])
            elif t == "tileset":
                d = get(f"/tilesets/{j['id']}")
                ts = d.get("tileset") or {}
                status = d.get("status") or ts.get("status") or (d.get("metadata") or {}).get("status")
                tiles = ts.get("tiles") or ts.get("images") or []
                if tiles or status == "completed":
                    n = save_any(key, d, "tile"); json.dump({k: v for k, v in d.items() if k != "tileset"} | {"tileset_keys": list(ts.keys())}, open(outpath(key, "meta.json"), "w"), indent=1, default=str)
                    j["status"] = "done"; log("tileset done", key, n, "images")
                elif status == "failed": j["status"] = "failed"; log("tileset FAILED", key)
            elif t == "tilespro":
                d = get(f"/tiles-pro/{j['id']}")
                if d.get("storage_urls"):
                    for k, u in d["storage_urls"].items(): fetch(u).save(outpath(key, f"{k}.png"))
                    json.dump({k: v for k, v in d.items() if k != "storage_urls"}, open(outpath(key, "meta.json"), "w"), indent=1, default=str)
                    j["status"] = "done"; log("tiles-pro done", key, len(d["storage_urls"]))
                elif d.get("status") == "failed": j["status"] = "failed"; log("tiles-pro FAILED", key)
            else:
                d = get(f"/background-jobs/{j['id']}")
                s = d.get("status")
                if s == "completed":
                    n = save_any(key, d.get("last_response") or d, "result"); json.dump(d, open(outpath(key, "job.json"), "w"), indent=1, default=str)
                    j["status"] = "done"; log(t, "done", key, n, "files")
                elif s == "failed": j["status"] = "failed"; log(t, "FAILED", key, str(d)[:300])
        except Exception as e:
            log("refresh error", key, str(e)[:200])
    save(st)


def wait_all(st, limit=3600):
    t0 = time.time()
    while time.time() - t0 < limit:
        refresh(st)
        pend = [k for k, j in st["jobs"].items() if j["status"] == "processing"]
        if not pend: return
        time.sleep(15)
