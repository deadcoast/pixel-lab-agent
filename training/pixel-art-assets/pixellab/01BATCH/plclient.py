"""thin PixelLab v2 client for this pipeline: create characters, animate, poll, download, sheet."""
import os, sys, time, json, io, base64, requests
from PIL import Image

BASE = "https://api.pixellab.ai/v2"
KEY = os.environ.get("PIXELLAB_KEY") or open(os.path.join(os.path.dirname(__file__), ".env")).read().split("=", 1)[1].strip()
H = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
DIRS = ["south", "south-west", "west", "north-west", "north", "north-east", "east", "south-east"]


def post(path, body):
    r = requests.post(BASE + path, headers=H, json=body, timeout=120)
    if r.status_code >= 400: raise RuntimeError(f"{path} {r.status_code}: {r.text[:600]}")
    return r.json()


def get(path):
    r = requests.get(BASE + path, headers=H, timeout=60)
    if r.status_code >= 400: raise RuntimeError(f"{path} {r.status_code}: {r.text[:600]}")
    return r.json()


def balance(): return get("/balance")


def create_character(description, size=64, seed=None, view="low top-down", template="mannequin", outline="single color black outline", detail="medium detail", enhance=False, name=None):
    body = {"description": description, "image_size": {"width": size, "height": size}, "view": view, "template_id": template,
            "no_background": True, "outline": outline, "detail": detail, "enhance_prompt": enhance}
    if seed is not None: body["seed"] = seed
    if name: body["name"] = name
    return post("/create-character-v3", body)


def character(cid): return get(f"/characters/{cid}")


def wait_character(cid, every=8, limit=900):
    t0 = time.time()
    while time.time() - t0 < limit:
        c = character(cid)
        urls = c.get("rotation_urls") or {}
        st = c.get("status") or c.get("state")
        if urls and len(urls) >= 4 and all(urls.values()): return c
        print(f"  … {int(time.time() - t0)}s status={st} rotations={len(urls)}", flush=True)
        time.sleep(every)
    raise TimeoutError(cid)


def fetch_png(url):
    r = requests.get(url, timeout=60); r.raise_for_status()
    return Image.open(io.BytesIO(r.content)).convert("RGBA")


def save_rotations(c, out_dir, tag):
    os.makedirs(out_dir, exist_ok=True)
    frames = {}
    for d, u in c["rotation_urls"].items():
        im = fetch_png(u); im.save(os.path.join(out_dir, f"{tag}_{d}.png")); frames[d] = im
    order = [d for d in DIRS if d in frames]
    w, h = frames[order[0]].size
    sheet = Image.new("RGBA", (w * len(order), h), (0, 0, 0, 0))
    for i, d in enumerate(order): sheet.paste(frames[d], (i * w, 0))
    sheet.save(os.path.join(out_dir, f"{tag}_rotations.png"))
    prev = Image.new("RGB", (w * len(order) * 3, h * 3), (36, 34, 40)); prev.paste(sheet.resize((w * len(order) * 3, h * 3), Image.NEAREST), (0, 0), sheet.resize((w * len(order) * 3, h * 3), Image.NEAREST))
    prev.save(os.path.join(out_dir, f"{tag}_rotations_x3.png"))
    return order, sheet


def animate(cid, template_animation_id=None, action=None, directions=None, mode=None, frame_count=8, name=None):
    body = {"character_id": cid}
    if template_animation_id: body["template_animation_id"] = template_animation_id; body["mode"] = "template"
    if action: body["action_description"] = action
    if mode: body["mode"] = mode
    if directions: body["directions"] = directions
    if frame_count and (mode == "v3"): body["frame_count"] = frame_count
    if name: body["animation_name"] = name
    return post("/animate-character", body)


def animations(cid): return get(f"/characters/{cid}/animations") if True else None


if __name__ == "__main__":
    print(json.dumps(balance(), indent=1))
