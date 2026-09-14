"""story plates: a generated background + generated sprites composed at 1:1 with drop shadows and depth sort."""
import os, json, glob
from PIL import Image, ImageDraw

DIRS = ["south", "south-west", "west", "north-west", "north", "north-east", "east", "south-east"]


def sprite(key, d="south"):
    fac, name = key.split("/")
    for base in (f"out2/{fac}/{name}", f"out/{fac}/{name}", f"out/{name}"):
        p = f"{base}/{name}_{d}.png"
        if os.path.exists(p): return Image.open(p).convert("RGBA")
    return None


def obj(name):
    p = f"out2/objects/{name}/{name}.png"
    return Image.open(p).convert("RGBA") if os.path.exists(p) else None


def bg(name):
    fs = sorted(glob.glob(f"out2/plates/{name}/*.png"))
    return Image.open(fs[0]).convert("RGBA") if fs else None


def compose(name, background, items, size=(400, 224), tint=None):
    """items: list of (kind, key, x_foot, y_foot, direction, scale)"""
    canvas = bg(background)
    if canvas is None: canvas = Image.new("RGBA", size, (40, 38, 44, 255))
    canvas = canvas.resize(size, Image.NEAREST) if canvas.size != size else canvas.copy()
    layer = Image.new("RGBA", size, (0, 0, 0, 0)); sh = Image.new("RGBA", size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    placed = []
    for kind, key, x, y, d, s in items:
        im = sprite(key, d) if kind == "c" else obj(key)
        if im is None: continue
        if s != 1: im = im.resize((int(im.width * s), int(im.height * s)), Image.NEAREST)
        # trim transparent rows to find the feet
        bbox = im.getbbox()
        if not bbox: continue
        w, h = im.size; foot = bbox[3]
        px, py = int(x - w // 2), int(y - foot)
        placed.append((y, im, px, py, bbox))
    placed.sort(key=lambda t: t[0])
    for y, im, px, py, bbox in placed:
        bw = bbox[2] - bbox[0]
        sd.ellipse([px + bbox[0] - 2, y - 3, px + bbox[2] + 2, y + 3], fill=(0, 0, 0, 90))
    canvas.alpha_composite(sh)
    for y, im, px, py, bbox in placed: layer.alpha_composite(im, (px, py)) if 0 <= px and 0 <= py else layer.paste(im, (px, py), im)
    canvas.alpha_composite(layer)
    if tint: canvas = Image.alpha_composite(canvas, Image.new("RGBA", size, tint))
    os.makedirs("out2/story", exist_ok=True)
    canvas.convert("RGB").save(f"out2/story/{name}.png")
    canvas.convert("RGB").resize((size[0] * 2, size[1] * 2), Image.NEAREST).save(f"out2/story/{name}_x2.png")
    return canvas


PLATES = [
 ("01_new_world_day", "new_world_day", [
   ("c", "diefenbunker/work_crew", 150, 190, "south-east", 1), ("c", "diefenbunker/sarah_oconnel", 205, 205, "south", 1), ("c", "diefenbunker/douglas_reed", 255, 195, "south-west", 1),
   ("c", "diefenbunker/jimmy_butler", 100, 210, "east", 1), ("c", "diefenbunker/enforcement_trooper", 310, 212, "west", 1), ("c", "diefenbunker/salvager", 60, 180, "south-east", 1)], None),
 ("02_movement_at_the_hatches", "new_world_day", [
   ("c", "lamplighter/sniper", 60, 214, "east", 1), ("c", "lamplighter/nomad_elder", 105, 200, "east", 1), ("c", "lamplighter/nomad_hauler", 30, 195, "south-east", 1),
   ("c", "diefenbunker/jimmy_butler", 300, 205, "west", 1), ("c", "diefenbunker/soldier", 345, 215, "west", 1), ("c", "diefenbunker/enforcement_trooper", 270, 190, "south-west", 1)], (10, 10, 40, 90)),
 ("03_behind_reaper_lines", "reaper_town", [
   ("c", "reaper/overseer", 200, 205, "south", 1), ("c", "reaper/captive", 150, 212, "south-east", 1), ("c", "reaper/blackguard", 260, 200, "south-west", 1),
   ("c", "reaper/raider", 330, 210, "west", 1), ("c", "reaper/household_woman", 60, 195, "east", 1), ("c", "reaper/child", 90, 205, "south", 1), ("c", "waylight/haven_courier", 370, 190, "west", 1)], None),
 ("04_the_road_station", "road_station", [
   ("o", "post_box", 300, 170, None, 1), ("c", "party/postman", 190, 205, "south", 1), ("c", "party/tally", 140, 212, "south-east", 1), ("c", "party/ada", 240, 210, "south-west", 1),
   ("c", "party/merrow", 110, 195, "south", 1), ("c", "party/kell", 270, 196, "south", 1), ("c", "waylight/donkey", 345, 214, "west", 1)], None),
 ("05_the_unread_promise", "hill_camp", [
   ("c", "cannibal/hunter", 130, 205, "east", 1), ("c", "cannibal/hearth_keeper", 80, 195, "south-east", 1), ("c", "cannibal/lookout", 60, 215, "east", 1),
   ("c", "waylight/mail_worker", 260, 210, "west", 1), ("c", "farkeeper/spearman", 320, 205, "west", 1), ("o", "hill_totem", 180, 160, None, 1)], None),
 ("06_the_republic_sets_out", "unity_gate", [
   ("c", "farkeeper/captain", 200, 214, "south", 1), ("c", "farkeeper/spearman", 130, 205, "south", 1), ("c", "farkeeper/longbowman", 270, 205, "south", 1),
   ("c", "waylight/mason", 70, 195, "south-east", 1), ("c", "waylight/forrester", 330, 198, "south-west", 1), ("c", "waylight/path_presser", 365, 212, "south-west", 1), ("c", "waylight/hauler", 40, 214, "south-east", 1)], None),
 ("07_the_cloaked_torch", "nomad_ridge", [
   ("o", "cloaked_lantern", 230, 205, None, 1), ("c", "lamplighter/sniper", 190, 212, "south-east", 1)], None),
 ("08_the_first_reply", "road_station", [
   ("o", "first_reply_table", 200, 175, None, 1), ("c", "rebel/speaker", 130, 205, "east", 1), ("c", "rebel/militiaman", 300, 205, "west", 1), ("c", "party/ada", 200, 215, "south", 1),
   ("c", "reaper/child", 260, 212, "south-west", 1), ("c", "waylight/haven_courier", 80, 195, "east", 1), ("c", "farkeeper/rifle_rider", 350, 190, "west", 1)], None),
 ("09_warmth_under_guard", "hill_camp", [
   ("o", "furnace", 200, 165, None, 1), ("c", "flamekeeper/furnace_warden", 150, 205, "south-east", 1), ("c", "flamekeeper/stoker", 250, 205, "south-west", 1),
   ("c", "raider/rover", 60, 212, "east", 1), ("c", "raider/bandit", 340, 210, "west", 1)], (20, 10, 0, 60)),
 ("10_the_weight_of_the_old_world", "unity_gate", [
   ("c", "irongiant/working_frame", 200, 212, "south", 1), ("c", "irongiant/frame_pilot", 120, 205, "south-east", 1), ("o", "salvage_frame_parked", 320, 170, None, 1), ("o", "scrap_pile", 60, 165, None, 1)], None),
]

if __name__ == "__main__":
    for name, background, items, tint in PLATES:
        compose(name, background, items, tint=tint); print("plate", name)
