"""03BATCH story plates: 03BATCH backgrounds + sprites from any batch, composed 1:1 with drop shadows and depth sort."""
import os, glob
from PIL import Image, ImageDraw

DIRS = ["south", "south-west", "west", "north-west", "north", "north-east", "east", "south-east"]


def sprite(key, d="south"):
    fac, name = key.split("/")
    for base in (f"out3/{fac}/{name}", f"out2/{fac}/{name}", f"out/{fac}/{name}", f"out/{name}"):
        p = f"{base}/{name}_{d}.png"
        if os.path.exists(p): return Image.open(p).convert("RGBA")
    return None


def obj(name, d=None):
    for p in (f"out3/objects/{name}/{name}.png", f"out2/objects/{name}/{name}.png", f"out3/objects8/{name}/{name}_{d or 'south'}.png"):
        if os.path.exists(p): return Image.open(p).convert("RGBA")
    return None


def bg(name):
    fs = sorted(glob.glob(f"out3/plates/{name}/*.png")) or sorted(glob.glob(f"out2/plates/{name}/*.png"))
    return Image.open(fs[0]).convert("RGBA") if fs else None


def compose(name, background, items, size=(400, 224), tint=None):
    """items: (kind, key, x_foot, y_foot, direction, scale); kind c=character, o=object"""
    canvas = bg(background)
    if canvas is None: return None
    canvas = canvas.resize(size, Image.NEAREST) if canvas.size != size else canvas.copy()
    layer = Image.new("RGBA", size, (0, 0, 0, 0)); sh = Image.new("RGBA", size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    placed = []
    for kind, key, x, y, d, s in items:
        im = sprite(key, d) if kind == "c" else obj(key, d)
        if im is None: continue
        if s != 1: im = im.resize((int(im.width * s), int(im.height * s)), Image.NEAREST)
        bbox = im.getbbox()
        if not bbox: continue
        w, h = im.size; foot = bbox[3]
        px, py = int(x - w // 2), int(y - foot)
        placed.append((y, im, px, py, bbox))
    placed.sort(key=lambda t: t[0])
    for y, im, px, py, bbox in placed: sd.ellipse([px + bbox[0] - 2, y - 3, px + bbox[2] + 2, y + 3], fill=(0, 0, 0, 90))
    canvas.alpha_composite(sh)
    for y, im, px, py, bbox in placed: layer.paste(im, (px, py), im)
    canvas.alpha_composite(layer)
    if tint: canvas = Image.alpha_composite(canvas, Image.new("RGBA", size, tint))
    os.makedirs("out3/story", exist_ok=True)
    canvas.convert("RGB").save(f"out3/story/{name}.png")
    canvas.convert("RGB").resize((size[0] * 2, size[1] * 2), Image.NEAREST).save(f"out3/story/{name}_x2.png")
    return canvas


PLATES = [
 ("11_the_ever_flame", "farlands_village", [
   ("o", "everflame_brazier", 200, 170, None, 1), ("c", "farkeeper/flame_tender", 165, 205, "south-east", 1), ("c", "farkeeper/matron", 245, 208, "south-west", 1), ("c", "farkeeper/child", 215, 216, "south", 1),
   ("c", "farkeeper/stonecutter", 90, 200, "east", 1), ("c", "farkeeper/shield_bearer", 330, 205, "west", 1), ("c", "farkeeper/spool_wright", 60, 214, "south-east", 1)], (10, 10, 30, 50)),
 ("12_what_the_famine_left", "famine_field", [
   ("c", "farkeeper/matron", 150, 210, "south", 1), ("c", "farkeeper/child", 190, 214, "south-west", 1), ("c", "farkeeper/spearman", 300, 205, "west", 1), ("c", "farkeeper/spool_wright", 80, 200, "south-east", 1),
   ("o", "peat_stack", 340, 160, None, 1)], None),
 ("13_the_sorting_hall", "sorting_hall", [
   ("c", "waylight/postmaster", 200, 210, "south", 1), ("c", "waylight/scribe", 120, 205, "south-east", 1), ("c", "waylight/mail_worker", 290, 208, "south-west", 1), ("c", "waylight/hauler", 60, 214, "east", 1),
   ("c", "party/ada", 340, 200, "west", 1), ("o", "letter_bundle", 240, 190, None, 1)], None),
 ("14_the_lit_way", "waylight_forum", [
   ("o", "lantern_rail", 300, 165, None, 1), ("c", "waylight/lamplighter", 90, 205, "east", 1), ("c", "waylight/outfitter", 280, 208, "south-west", 1), ("c", "waylight/trainee", 180, 214, "south", 1),
   ("c", "party/postman", 220, 212, "south-east", 1), ("c", "waylight/donkey", 345, 216, "west", 1)], None),
 ("15_the_written_promise", "river_crossing", [
   ("c", "republic/envoy", 170, 210, "south-east", 1), ("c", "republic/registrar", 130, 214, "east", 1), ("c", "rebel/speaker", 260, 210, "west", 1), ("c", "rebel/militiaman", 310, 205, "south-west", 1),
   ("c", "waylight/haven_courier", 80, 200, "south-east", 1), ("c", "farkeeper/captain", 360, 195, "west", 1)], None),
 ("16_first_light_below", "bunker_interior", [
   ("o", "terminal_desk", 300, 170, None, 1), ("c", "diefenbunker/archivist", 120, 210, "south-east", 1), ("c", "diefenbunker/child", 180, 216, "south", 1), ("c", "diefenbunker/douglas_reed", 230, 208, "south-west", 1),
   ("c", "diefenbunker/salvager", 60, 200, "east", 1), ("c", "diefenbunker/soldier", 350, 212, "west", 1)], (0, 20, 10, 40)),
 ("17_the_farm", "tank_farm", [
   ("o", "smoke_bowser", 120, 190, "south-east", 1), ("c", "smoke/driver", 190, 212, "south", 1), ("c", "smoke/smoker", 260, 208, "south-west", 1), ("c", "smoke/gauger", 300, 200, "west", 1),
   ("c", "smoke/torch", 350, 214, "west", 1), ("o", "oil_drums", 40, 200, None, 1)], (30, 10, 0, 50)),
 ("18_the_old_highway", "old_highway", [
   ("o", "caravan_wagon", 300, 205, "west", 1), ("c", "waylight/donkey", 245, 214, "west", 1), ("c", "party/postman", 110, 212, "east", 1), ("c", "party/tally", 70, 204, "east", 1),
   ("c", "party/merrow", 150, 200, "south-east", 1), ("c", "party/kell", 40, 214, "east", 1), ("c", "party/ada", 190, 216, "south", 1)], None),
 ("19_the_stockade", "reaper_stockade", [
   ("o", "stockade_cage", 310, 165, None, 1), ("c", "reaper/overseer", 200, 210, "south", 1), ("c", "reaper/captive", 300, 214, "south-west", 1), ("c", "reaper/blackguard", 120, 205, "south-east", 1),
   ("c", "reaper/conscript", 60, 214, "east", 1), ("c", "reaper/household_woman", 360, 200, "west", 1)], None),
 ("20_warmth_kept", "hearth_hall", [
   ("c", "flamekeeper/furnace_warden", 180, 210, "south", 1), ("c", "flamekeeper/stoker", 260, 208, "south-west", 1), ("c", "raider/rover", 80, 214, "east", 1), ("c", "raider/bandit", 40, 200, "south-east", 1),
   ("c", "waylight/mail_worker", 340, 212, "west", 1)], (30, 15, 0, 40)),
 ("21_the_snow_pass", "snow_pass", [
   ("o", "cairn", 250, 170, None, 1), ("c", "lamplighter/sniper", 120, 210, "east", 1), ("c", "lamplighter/nomad_elder", 200, 214, "south", 1), ("c", "lamplighter/nomad_hauler", 60, 205, "south-east", 1),
   ("c", "lamplighter/nomad", 300, 208, "south-west", 1), ("c", "lamplighter/marksman", 350, 200, "west", 1)], (10, 10, 30, 40)),
 ("22_the_scrap_yard", "scrap_yard", [
   ("o", "scrap_press", 320, 170, None, 1), ("c", "irongiant/working_frame", 200, 212, "south", 1), ("c", "irongiant/frame_pilot", 120, 208, "south-east", 1), ("c", "diefenbunker/sarah_oconnel", 60, 214, "east", 1),
   ("c", "waylight/mason", 340, 214, "west", 1)], None),
]

if __name__ == "__main__":
    for name, background, items, tint in PLATES:
        r = compose(name, background, items, tint=tint); print("plate", name, "ok" if r else "no background")
