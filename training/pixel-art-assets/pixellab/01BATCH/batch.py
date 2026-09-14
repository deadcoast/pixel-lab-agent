"""batch runner: create characters (respecting the 10-job cap), then walk + idle animations, download, sheet."""
import os, sys, json, time, traceback
import plclient as pl
from PIL import Image

OUT = "out"
STATE = "batch_state.json"
CAP = 10

FACTIONS = {
 "reaper": {
  "conscript": "post-apocalyptic raider conscript, full bright orange hooded rain coverall sun-faded and stained, hood down, frayed rope belt, black rubber boots, no armour no webbing, brown cloth cap, gaunt stubbled face with hollow eyes, slouched, bright orange dominant with dust brown and black accents",
  "raider": "post-apocalyptic raider line trooper, mismatched scavenged gear, faded hi-vis orange rain jacket with buff leather panels riveted over the chest and shoulder, mustard knit cuffs, black webbing straps and buckles across the torso, belt pouches, soft brown cap with a stiff bill and goggles pushed up, black gloves, dark trousers, worn boots, rifle slung across the back, weathered stubbled face, rust orange mustard buff leather and black palette",
  "blackguard": "post-apocalyptic warband guard, plain black tunic and black trousers, black knit watch cap pulled low, black leather webbing straps and buckles across the chest, black belt gloves and boots, a single bright red neckerchief knotted at the throat, everything matches, no armour no insignia, lean bearded face, standing at attention, black and charcoal palette with the red scarf the only saturated colour",
  "second": "post-apocalyptic warband second-in-command, long black astrakhan curly lamb fur coat heavy and wide at the shoulders hanging to the knee, black kepi cap with a stiff bill and goggles pushed up, red-brown leather gauntlets with a round metal boss at the cuff, leather strap across the chest, curved sabre held low in one hand, older weathered face with grey stubble, black charcoal and red-brown palette",
  "admiral": "post-apocalyptic warlord, long oxblood leather double-breasted greatcoat to the knee, wide rust-red notched lapels, two rows of small pale pewter buttons down the chest, black leather belt with a plain buckle, rigid black leather collar standing up under the jaw, black gloves, dark trousers, tall boots, balding receding hair, short red-brown beard, flat pale stare, sabre held point-down, oxblood rust red black and cold pewter palette, no brass",
 },
 "smoke": {
  "smoker": "post-apocalyptic refinery raider, shaved head with raw sunburned red peeling scalp and face, lit cigarette at the mouth with a small ember, vest of overlapping cut pipe and oil-drum steel plates shingled and riveted, tar-blackened with a faint oily sheen, dark greasy work clothes, heavy gloves, steel-capped boots, square steel jerrycan slung on the back, tar black oily steel and raw sunburn red palette, boxy silhouette",
  "torch": "post-apocalyptic incendiary, large cylindrical pressure tank strapped to the back with a hose over the shoulder, long metal lance held forward with a small live flame at the tip, shaved sunburned head, both eyes milky white and scarred, heavy blackened leather apron and gauntlets scorched at the edges, shingled steel plate on one shoulder, hunched under the tank's weight, tar black scorched steel and sunburn red palette with one bright flame",
  "gauger": "post-apocalyptic refinery quartermaster woman, no armour, chest rack of salvaged round pressure dials and gauge faces strapped across the torso most of them cracked and dead, shaved sunburned head wrapped in an oiled rag, sharp watchful face, long greasy black coat with sleeves rolled, notched tally stick in the belt, brass key ring at the hip, arms folded, tar black dull steel and sunburn red palette with pale dial faces",
  "anointer": "post-apocalyptic oil-cult warlord, wide heat-warped refinery hard hat cut down into a scalloped drooping brim, dark and blistered, long coat of overlapping cut pipe and tank steel plates shingled like roof tiles, tar-black with a faint oily sheen, oxblood cloth underneath, round brass pressure gauge strapped over the left eye on a hide band, shaved sunburned scalp with a stitched scar, one pale eye, black gloves, oil-slick boots, chin up, tar black oxblood tarnished brass and sunburn red palette",
 },
 "farkeeper": {
  "spearman": "towering broad-chested mountain warrior, pale skin, thick powerful thighs, plain iron skull cap, layered hide and wool coat belted at the waist, dark green sash across the chest, wrapped leather bracers, fur-topped boots, long ash spear with an iron head held upright, stern bearded face, austere no ornament, hide brown iron grey and dark green palette",
  "longbowman": "towering broad-chested mountain archer, pale skin, iron skull cap, hide jerkin over a wool tunic, dark green sash, leather bracer on the bow arm, quiver of arrows at the hip, great yew longbow taller than a man held in one hand, fur-topped boots, lean bearded face, hide brown iron grey and dark green palette, no ornament",
  "pugugly": "immense bare-knuckled mountain brawler, far taller and broader than any man, pale skin, no helmet, shaved head with a thick beard, bare arms wrapped in leather straps at the wrists and fists, sleeveless hide vest, dark green sash at the waist, heavy wool trousers, fur boots, hunched shoulders, huge scarred hands, hide brown and dark green palette, no weapon",
  "berserker": "huge mountain swordsman, pale skin, broad chest, iron skull cap, hide and fur coat, dark green sash, an enormous two-handed claymore as long as a man carried across the back, a flintlock pistol in the belt, leather gauntlets, fur boots, fierce bearded face, hide brown iron grey dark green and dull steel palette, no ornament",
  "rifle_rider": "towering mountain warrior on horseback, pale skin, iron skull cap, hide and wool coat, dark green sash, long rifle held upright, sturdy dark bay horse with a plain leather saddle and a rolled blanket, fur boots in the stirrups, hide brown iron grey and dark green palette",
  "recon_rider": "lean mountain scout on horseback, pale skin, iron skull cap, light hide jerkin, dark green sash, a spyglass at the belt and a short bow across the back, fast grey horse with a light saddle, leaning forward, hide brown iron grey and dark green palette",
 },
}
TEMPLATE = {"rifle_rider": "horse", "recon_rider": "horse"}
ANIMS = [("walk", "walk"), ("idle", "breathing-idle")]


def load():
    return json.load(open(STATE)) if os.path.exists(STATE) else {"chars": {}, "anims": {}}


def save(st): json.dump(st, open(STATE, "w"), indent=1)


def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)


def active_jobs_guess(st):
    return sum(1 for c in st["chars"].values() if c.get("status") == "processing") + sum(8 for a in st["anims"].values() if a.get("status") == "processing")


def try_post(fn, *a, **k):
    while True:
        try: return fn(*a, **k)
        except RuntimeError as e:
            if "429" in str(e): time.sleep(20); continue
            raise


def refresh(st):
    for key, c in st["chars"].items():
        if c.get("status") != "processing": continue
        d = pl.character(c["id"])
        if d.get("status") == "completed" and d.get("rotation_urls"):
            fac, name = key.split("/")
            pl.save_rotations(d, f"{OUT}/{fac}/{name}", name); c["status"] = "done"; log("char done", key)
        elif d.get("status") == "failed": c["status"] = "failed"; log("char FAILED", key, d.get("error"))
    for key, a in st["anims"].items():
        if a.get("status") != "processing": continue
        ck, aname = key.rsplit("/", 1); c = st["chars"][ck]
        d = pl.character(c["id"])
        anims = [x for x in (d.get("animations") or []) if x.get("animation_type") == a["type"] or x.get("display_name") == aname]
        a.setdefault("t0", time.time()); age = time.time() - a["t0"]
        if anims and all(len(dd.get("frames", [])) > 0 for dd in anims[0]["directions"]) and len(anims[0]["directions"]) >= 8:
            fac, name = ck.split("/"); save_anim(anims[0], f"{OUT}/{fac}/{name}/{aname}", name, aname); a["status"] = "done"; log("anim done", key)
        elif anims and age > 600 and len(anims[0]["directions"]) >= 6:
            have = {dd["direction"] for dd in anims[0]["directions"]}; missing = [dd for dd in pl.DIRS if dd not in have]
            if missing and not a.get("retried"):
                try_post(pl.animate, c["id"], template_animation_id=a["type"], name=aname, directions=missing); a["retried"] = True; a["t0"] = time.time(); log("re-queued missing", key, missing)
            elif not missing or a.get("retried"):
                fac, name = ck.split("/"); save_anim(anims[0], f"{OUT}/{fac}/{name}/{aname}", name, aname); a["status"] = "done"; log("anim done (partial)", key, sorted(have))
    save(st)


def save_anim(anim, out_dir, name, aname):
    os.makedirs(out_dir, exist_ok=True)
    fb = {d["direction"]: [pl.fetch_png(u) for u in d["frames"]] for d in anim["directions"]}
    order = [d for d in pl.DIRS if d in fb]; n = min(len(v) for v in fb.values()); w, h = fb[order[0]][0].size
    sh = Image.new("RGBA", (w * n, h * len(order)), (0, 0, 0, 0))
    for r, d in enumerate(order):
        for k in range(n): sh.paste(fb[d][k], (k * w, r * h))
    sh.save(f"{out_dir}/{name}_{aname}_sheet.png")
    gifs = []
    for k in range(n):
        g = Image.new("RGB", (w * len(order) * 3, h * 3), (36, 34, 40))
        for i, d in enumerate(order):
            im = fb[d][k].resize((w * 3, h * 3), Image.NEAREST); g.paste(im, (i * w * 3, 0), im)
        gifs.append(g)
    gifs[0].save(f"{out_dir}/{name}_{aname}_x3.gif", save_all=True, append_images=gifs[1:], duration=110, loop=0)
    json.dump({"frames": n, "w": w, "h": h, "directions": order}, open(f"{out_dir}/{name}_{aname}.json", "w"))


def main():
    st = load()
    todo_chars = [f"{f}/{n}" for f, d in FACTIONS.items() for n in d]
    while True:
        refresh(st)
        active = active_jobs_guess(st)
        # queue characters first
        for key in todo_chars:
            if key in st["chars"] or active >= CAP: continue
            fac, name = key.split("/")
            r = try_post(pl.create_character, FACTIONS[fac][name], size=64, seed=7, template=TEMPLATE.get(name, "mannequin"), name=f"{fac}:{name}")
            st["chars"][key] = {"id": r["character_id"], "status": "processing"}; active += 1; log("queued char", key, r["character_id"]); save(st)
        # then animations for finished characters, one at a time (8 jobs each)
        for key, c in st["chars"].items():
            if c.get("status") != "done": continue
            for aname, tpl in ANIMS:
                ak = f"{key}/{aname}"
                if ak in st["anims"] or active + 8 > CAP: continue
                tpl_ = {"walk": "walk-6-frames", "breathing-idle": "rest-idle"}.get(tpl, tpl) if TEMPLATE.get(key.split("/")[1]) == "horse" else tpl
                r = try_post(pl.animate, c["id"], template_animation_id=tpl_, name=aname)
                st["anims"][ak] = {"status": "processing", "type": tpl_}; active += 8; log("queued anim", ak); save(st)
        pending = [k for k in todo_chars if st["chars"].get(k, {}).get("status") != "done" and st["chars"].get(k, {}).get("status") != "failed"]
        pending_a = [k for k, a in st["anims"].items() if a["status"] == "processing"]
        wanted_a = sum(2 for k, c in st["chars"].items() if c.get("status") == "done")
        have_a = sum(1 for k in st["anims"])
        if not pending and not pending_a and have_a >= wanted_a:
            log("ALL DONE"); log(pl.balance()); return
        time.sleep(25)


if __name__ == "__main__":
    try: main()
    except Exception: traceback.print_exc()
