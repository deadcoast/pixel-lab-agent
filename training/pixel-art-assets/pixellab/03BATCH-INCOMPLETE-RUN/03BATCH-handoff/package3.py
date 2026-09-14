"""Package 03BATCH: copy out3 into /mnt/user-data/outputs/03batch with previews, manifest, design doc, codex, pipeline; zip; key check."""
import os, json, glob, shutil, subprocess
from PIL import Image
import content3 as c

SRC = "out3"; DEST = "/mnt/user-data/outputs/03batch"; PREV = f"{DEST}/preview"


def contact(paths, cols, scale, out, pad=2, bg=(52, 50, 58, 255), label=None):
    ims = [Image.open(p).convert("RGBA") for p in paths if os.path.exists(p)]
    if not ims: return None
    w = max(i.width for i in ims) + pad; h = max(i.height for i in ims) + pad; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * w, rows * h), bg)
    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * w + pad // 2, (i // cols) * h + pad // 2), im)
    if scale != 1: sheet = sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST)
    sheet.save(out); return out


def main():
    if os.path.exists(DEST): shutil.rmtree(DEST)
    os.makedirs(PREV, exist_ok=True)
    manifest = {"batch": "03BATCH — Hearth and Road", "characters": {}, "objects": [], "objects8": [], "icons": [], "emblems": [], "tiles": [], "kits": [], "backgrounds": [], "story": [], "portraits": [], "ui": [], "fonts": [], "animations": {}, "partial": {}}
    st3 = json.load(open("pl3_state.json")) if os.path.exists("pl3_state.json") else {"jobs": {}}
    an = json.load(open("anim4_state.json")) if os.path.exists("anim4_state.json") else {"anims": {}}
    # characters: rotations + animations (any faction folder under out3 that is not a known asset class)
    classes = {"objects", "objects8", "icons", "emblems", "tiles", "kits", "plates", "story", "portraits", "ui"}
    for fac in sorted(os.listdir(SRC)):
        if fac in classes or not os.path.isdir(f"{SRC}/{fac}"): continue
        for name in sorted(os.listdir(f"{SRC}/{fac}")):
            d = f"{SRC}/{fac}/{name}"; key = f"{fac}/{name}"
            if not os.path.isdir(d): continue
            shutil.copytree(d, f"{DEST}/characters/{fac}/{name}")
            j = st3["jobs"].get(key, {})
            if os.path.exists(f"{d}/{name}_rotations.png"): manifest["characters"][key] = {"id": j.get("id"), "prompt": c.CHARS.get(key, ("", ""))[0], "template": c.CHARS.get(key, ("", "mannequin"))[1]}
            anims = [os.path.basename(a.rstrip("/")) for a in sorted(glob.glob(f"{d}/*/")) if os.path.exists(f"{a}/{name}_{os.path.basename(a.rstrip('/'))}_sheet.png")]
            if anims: manifest["animations"][key] = anims
    for ak, a in an["anims"].items():
        if a.get("partial"): manifest["partial"][ak] = a["partial"]
    for cls in ("objects", "objects8", "icons", "emblems", "tiles", "kits", "plates", "portraits", "ui"):
        if os.path.isdir(f"{SRC}/{cls}"):
            shutil.copytree(f"{SRC}/{cls}", f"{DEST}/{cls}", dirs_exist_ok=True)
            manifest["backgrounds" if cls == "plates" else cls] = sorted(os.listdir(f"{SRC}/{cls}"))
    if os.path.isdir(f"{SRC}/story"):
        os.makedirs(f"{DEST}/story", exist_ok=True)
        for p in sorted(glob.glob(f"{SRC}/story/*.png")): shutil.copy(p, f"{DEST}/story/"); manifest["story"].append(os.path.basename(p))
    manifest["fonts"] = [os.path.basename(p) for p in glob.glob(f"{DEST}/ui/*/*.ttf")]
    manifest["costs"] = st3.get("costs", {}); manifest["phase1"] = st3.get("phase1"); manifest["phase2_spent"] = an.get("spent")
    # prompts for reproducibility
    manifest["prompts"] = {"objects": {k: d for k, d, s in c.OBJECTS}, "objects8": {k: d for k, (d, s) in c.OBJECTS8.items()}, "icons": c.ICONS, "emblems": c.EMBLEMS, "tilesets": c.TILESETS, "roads": c.ROADS, "kits": c.BUILDINGS, "backgrounds": c.PLATES, "ui": {k: v["description"] for k, v in c.UI.items()}, "custom_animations": {f"{k}/{n}": a for k, n, a in c.CUSTOM}}
    json.dump(manifest, open(f"{DEST}/manifest.json", "w"), indent=1)
    # previews
    rots = [f"{SRC}/{k}/{k.split('/')[1]}_rotations.png" for k in c.CHARS]
    contact(rots, 1, 2, f"{PREV}/characters_rotations_x2.png")
    for size in (64, 96, 128):
        contact([f"{SRC}/objects/{k.split('/')[1]}/{k.split('/')[1]}.png" for k, _, s in c.OBJECTS if s == size], 8 if size < 128 else 6, 2, f"{PREV}/objects_{size}_x2.png")
    contact([f"{SRC}/icons/{k.split('/')[1]}/{k.split('/')[1]}.png" for k in c.ICONS], 12, 3, f"{PREV}/icons_x3.png")
    contact([f"{SRC}/emblems/{k.split('/')[1]}/{k.split('/')[1]}.png" for k in c.EMBLEMS], 12, 3, f"{PREV}/emblems_x3.png")
    contact(sorted(glob.glob(f"{SRC}/portraits/*/*.png")), 10, 3, f"{PREV}/portraits_x3.png")
    contact([f"{SRC}/objects8/{k.split('/')[1]}/{k.split('/')[1]}_rotations.png" for k in c.OBJECTS8], 1, 2, f"{PREV}/objects8_rotations_x2.png")
    # animation strips: the south row of every new sheet, x2
    strips = []
    for key, anims in manifest["animations"].items():
        fac, name = key.split("/")
        for a in anims:
            sheet = f"{SRC}/{fac}/{name}/{a}/{name}_{a}_sheet.png"; meta = f"{SRC}/{fac}/{name}/{a}/{name}_{a}.json"
            if not os.path.exists(meta): continue
            m = json.load(open(meta)); im = Image.open(sheet).convert("RGBA")
            row = m["directions"].index("south") if "south" in m["directions"] else 0
            strips.append((f"{name} · {a}", im.crop((0, row * m["h"], im.width, (row + 1) * m["h"]))))
    if strips:
        from PIL import ImageDraw
        w = max(s.width for _, s in strips); h = max(s.height for _, s in strips) + 12
        sheet = Image.new("RGBA", (w, h * len(strips)), (52, 50, 58, 255)); dr = ImageDraw.Draw(sheet)
        for i, (lab, s) in enumerate(strips): sheet.paste(s, (0, i * h + 12), s); dr.text((2, i * h), lab, fill=(230, 220, 200, 255))
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(f"{PREV}/animations_south_x2.png")
    # docs + pipeline + codex
    for f in ("03BATCH-DESIGN.md",):
        if os.path.exists(f): shutil.copy(f, DEST)
    os.makedirs(f"{DEST}/pipeline", exist_ok=True)
    for f in ("content3.py", "batch4.py", "anim4.py", "plates3.py", "codex3.py", "package3.py", "pl2.py", "plclient.py", "inventory.json"): shutil.copy(f, f"{DEST}/pipeline/")
    if os.path.exists(f"{DEST}/hearth_and_road_codex.html"): pass
    # key check, then zip
    key = open(".env").read().split("=")[1].strip()[:8]
    hits = subprocess.run(["grep", "-rl", key, DEST], capture_output=True, text=True).stdout.strip()
    if hits: raise SystemExit("KEY LEAK: " + hits)
    if os.path.exists("/mnt/user-data/outputs/03batch.zip"): os.remove("/mnt/user-data/outputs/03batch.zip")
    subprocess.run(["zip", "-qr", "/mnt/user-data/outputs/03batch.zip", "03batch"], cwd="/mnt/user-data/outputs")
    print("packaged", len(manifest["characters"]), "chars", len(manifest["objects"]), "objects", len(manifest["icons"]), "icons", sum(len(v) for v in manifest["animations"].values()), "anims;", os.path.getsize("/mnt/user-data/outputs/03batch.zip") // 1024 // 1024, "MB")


if __name__ == "__main__":
    main()
