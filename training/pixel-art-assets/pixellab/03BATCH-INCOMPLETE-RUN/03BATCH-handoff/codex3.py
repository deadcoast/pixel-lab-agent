"""Hearth and Road — the 03BATCH codex. Same page grammar as the Convergence codex: lore in the compendium's terms, then every
asset made for it. Sprites are found in out3 (this batch), out2 (02BATCH) or out (01BATCH); animations from any batch are shown."""
import os, json, base64, glob
from PIL import Image
import codex as c1
from content3 import OBJECTS, OBJECTS8, EMBLEMS, UI

DEST = "/mnt/user-data/outputs/03batch"; O3 = "out3"; O2 = "out2"; O1 = "out"
b64 = c1.b64; first = c1.first


def base_of(key):
    fac, name = key.split("/")
    for b in (f"{O3}/{fac}/{name}", f"{O2}/{fac}/{name}", f"{O1}/{fac}/{name}", f"{O1}/{name}"):
        if os.path.exists(f"{b}/{name}_rotations.png"): return b
    return None


def char_entry(key):
    fac, name = key.split("/"); base = base_of(key)
    if not base: return None
    e = {"key": key, "name": name.replace("_", " "), "rot": b64(f"{base}/{name}_rotations.png"), "anims": {}, "fw": 96 if key == "irongiant/working_frame" else 64}
    for b in {base, f"{O3}/{fac}/{name}"}:
        for d in sorted(glob.glob(f"{b}/*/")):
            a = os.path.basename(d.rstrip("/")); sheet = f"{d}/{name}_{a}_sheet.png"; meta = f"{d}/{name}_{a}.json"
            if os.path.exists(sheet) and os.path.exists(meta):
                m = json.load(open(meta)); e["anims"][a] = {"sheet": b64(sheet), **m, "new": b.startswith(O3)}
    p = first(f"{O3}/portraits/{name}/*.png") or first(f"{O2}/portraits/{name}/*.png")
    if p: e["portrait"] = b64(p)
    return e


def obj_entry(key):
    """8-direction object as a rotating card"""
    name = key.split("/")[-1]; rot = f"{O3}/objects8/{name}/{name}_rotations.png"
    if not os.path.exists(rot): return None
    im = Image.open(rot); fw = im.height
    return {"key": key, "name": name.replace("_", " "), "rot": b64(rot), "anims": {}, "fw": fw}


OBJ = {k.split("/")[1]: s for k, _, s in OBJECTS}

SECTIONS = [
 {"id": "farlands", "title": "The Farlands, at the Hearth", "sub": "Farkeepers at home · §6, UNITY-DESIGN",
  "lore": ["The Farkeepers carry the Republic's security and their architecture is engineering read as cathedral: a fire in the town hall that has never been allowed to go out, and tall sharp spires that are chimneys — smoke spools — with ducts down the spine that pull cool air in and whistle in wind. The famine is remembered in the shape of everything: the fire kept, the peat stacked, the bowl carried in both hands.",
           "This section draws the people who are not soldiers: the woman who keeps the Ever-flame, the wright who tends the spools, a grandmother who remembers, a child with kindling, a stonecutter, and the shield bearer who stands between them and the road.",
           "The buildings are map objects at 128 px so the spire silhouette survives at map scale; a dark-stone building kit lets the Farlands be laid out tile by tile."],
  "chars": ["farkeeper/flame_tender", "farkeeper/spool_wright", "farkeeper/matron", "farkeeper/child", "farkeeper/stonecutter", "farkeeper/shield_bearer"],
  "objects": ["smoke_spool", "everflame_hall", "farkeeper_longhouse", "lancet_ruin", "drystone_wall", "famine_field", "peat_stack", "standing_stone"],
  "icons": ["round_shield", "bearded_axe", "ever_coal", "peat_brick"], "tiles": ["heather_to_peat"], "kits": ["farkeeper_gothic"],
  "plates": ["11_the_ever_flame", "12_what_the_famine_left"], "backgrounds": ["farlands_village", "famine_field"]},
 {"id": "waylight", "title": "Waylight, at Home", "sub": "The mail society · §1–2, §4, WAYLIGHT-DESIGN",
  "lore": ["Within the cities, workers handle the local movement of mail; letters hold a place in the culture that money does not. The civic centre of a courier society is the letter wall beside the fountain, the sorting hall under the dome, the outfitters' rail of lit lanterns just inside the gate, and the couriers' hall with five identical doors.",
           "Here the lamplighter is a job, not a sentence. The trainee runs the north road in file. The postmaster stamps what goes out and the scribe writes for people who cannot.",
           "The civic stone comes as map objects — the Way Column, pillars, the statue column, pillared entrances, the clock tower — and as a pale-stone building kit with terracotta roofs."],
  "chars": ["waylight/postmaster", "waylight/scribe", "waylight/lamplighter", "waylight/outfitter", "waylight/trainee", "waylight/mail_worker", "waylight/hauler", "waylight/donkey"],
  "objects": ["sorting_hall", "courier_hall", "letter_wall", "way_column", "statue_column", "roman_pillar", "pillared_entrance", "clock_tower", "stone_house", "greenhouse", "allotment", "paper_mill_wheel", "lantern_rail", "lamp_post", "dark_lamp_post", "weigh_beam", "well", "notice_board"],
  "icons": ["wax_seal", "ink_and_quill", "ledger", "hand_stamp", "courier_badge", "lamp_oil", "paper_sheets"], "tiles": ["flagstone_to_cobble", "flagstone_roads"], "kits": ["waylight_stone"],
  "plates": ["13_the_sorting_hall", "14_the_lit_way"], "backgrounds": ["sorting_hall", "waylight_forum", "unity_plaza"]},
 {"id": "republic", "title": "The Republic Goes Out", "sub": "Envoys, the road, the party at a run · §3–5, §15, P07–P08",
  "lore": ["The Republic's offer travels as a written promise. An envoy carries it in a locked case; a registrar records the first reply that comes back, because the reply proves another person at the far end. Where the promise cannot be read, the armed stranger behind it is easier to understand.",
           "A courier game is played at a run. The party gets its running cycles here, and its hero beats: Ada reads a letter aloud, Merrow binds a wound, Tally levers the cut-down rifle and counts what is left, Kell unrolls the road.",
           "The road gets its furniture between settlements — bridges, a ford, signposts, a hitching rail, a hay shelter, a cairn on the ridge — and a covered caravan wagon rendered from eight angles."],
  "chars": ["republic/envoy", "republic/registrar", "party/postman", "party/tally", "party/merrow", "party/kell", "party/ada", "animals/draft_horse", "animals/light_horse", "farkeeper/rifle_rider"],
  "objects8": ["caravan_wagon"],
  "objects": ["stone_bridge", "timber_bridge", "ford_stones", "signpost", "settlement_sign", "hitching_rail", "water_trough", "hay_shelter", "timber_house", "cairn"],
  "icons": ["written_promise", "bedroll", "rope", "matches", "compass", "spyglass", "firewood", "horseshoe", "feed_bag", "shovel", "pickaxe", "hammer_and_nails", "bandage_roll", "dried_fish", "bread_loaf"],
  "tiles": ["grass_to_mud", "dirt_to_ash"], "kits": ["frontier_timber"],
  "plates": ["15_the_written_promise", "18_the_old_highway"], "backgrounds": ["river_crossing", "snow_pass", "burned_settlement"]},
 {"id": "oldworld", "title": "The Old World, Left Where It Fell", "sub": "Roads that remember · §5, WAYLIGHT-DESIGN layer 1",
  "lore": ["The old world is present as material, not as a functioning machine. Cars pushed to the shoulder with trees in their engine bays, pylons with the wires down, a cobra-head lamp post that never fell with a brass lantern hung from it now, a water tower repainted white, a turbine someone rebuilt from a book.",
           "The map's nature set is here too: pines and snow pines, dead trees, an oak, birches, boulders and outcrops, reeds, drifts — and the asphalt highway as an 18-configuration autotile, cracked, with grass in the lane paint."],
  "chars": [],
  "objects": ["wrecked_car", "wrecked_bus", "power_pylon", "power_pole", "highway_sign", "guardrail", "overpass_stub", "cobra_lamp", "water_tower", "wind_turbine", "solar_row", "shipping_container", "tyre_pile", "billboard", "gas_station_ruin", "phone_box",
              "pine_tree", "snow_pine", "dead_tree", "oak_tree", "birch_cluster", "bush", "tall_grass", "boulder", "rock_outcrop", "fallen_log", "stump", "reeds", "snowdrift"],
  "icons": [], "tiles": ["asphalt_roads"], "plates": [], "backgrounds": ["old_highway"]},
 {"id": "bunker", "title": "Beneath the Door", "sub": "The Diefenbunker Society, inside · §10–14",
  "lore": ["They lived hundreds of years underground with old books and records, passing down occupations, habits and an increasingly distant account of the world outside. The corridor, the bunks, the ration shelves mostly empty, the generator, the air filters, the terminal with its green phosphor: the inside of a continuity effort, generations on.",
           "The archivist carries what they know. The child sees daylight for the first time. Douglas Reed addresses the crowd — a custom animation for the voice of the record. The soldier and the salvager, made in the first batch, finally walk.",
           "Interior tiles — concrete to steel grate — and a riveted-steel building kit lay the bunker out; a stencil font sprays its signage."],
  "chars": ["diefenbunker/archivist", "diefenbunker/child", "diefenbunker/douglas_reed", "diefenbunker/soldier", "diefenbunker/salvager", "diefenbunker/enforcement_trooper"],
  "objects": ["bunker_door", "bunk_beds", "ration_shelves", "generator", "air_filter", "terminal_desk", "cistern", "records_cabinet", "map_table"],
  "icons": ["sbsn_card", "ration_can", "radio_handset", "flashlight", "gas_mask", "clipboard", "old_book", "rifle_cartridges"], "tiles": ["concrete_to_grate"], "kits": ["bunker_steel"],
  "plates": ["16_first_light_below"], "backgrounds": ["bunker_interior"]},
 {"id": "claims", "title": "The Claims, Their Ground", "sub": "Reapers, the hill people, the Smoke, the Lamplighters, Raiders, Rebels, Flame Keepers, Iron Giants · §3, §8, §15, P01–P06",
  "lore": ["Every claim on the road has ground under it. The Reapers' stockade: palisade, gate with a stop sign nailed above the ownership mark, a watchtower wearing a road sign, a cage. The hill community's huts of stitched hide and its drying racks. The Smoke's tank farm — pale tanks cut into dwellings, a flare that never goes out, and the only motor vehicle anyone will see, the bowser, rendered from eight angles.",
           "Raiders leave a caravan in the ditch and the lock cut. Rebels barricade a street with their own furniture. Flame Keepers chain the coal bunker and guard the hearth house door. Iron Giants run a gantry crane and a press. Lamplighters leave nothing but a blind among the rocks and a cache under a flat stone.",
           "Faces for dialogue: the Overseer, the Nomad Elder, the Hearth Keeper, the Speaker, the Gauger. Idles for the people who only had a walk."],
  "chars": ["smoke/driver", "reaper/overseer", "reaper/household_woman", "reaper/child", "cannibal/lookout", "lamplighter/nomad_elder", "lamplighter/marksman", "lamplighter/nomad", "rebel/speaker", "flamekeeper/stoker"],
  "objects8": ["smoke_bowser"],
  "objects": ["watchtower", "palisade_wall", "palisade_gate", "stockade_cage", "loot_heap", "marked_storehouse", "hide_hut", "drying_rack", "snare_line", "caravan_wreck", "loot_sacks", "furniture_barricade", "coal_bunker", "hearth_house", "gantry_crane", "scrap_press", "oil_drums", "flare_stack", "pipeline", "fuel_bowser", "storage_tank", "ridge_blind", "nomad_cache"],
  "icons": ["rifle_scope", "ghillie_net", "snare_wire", "bone_whistle", "ochre_pot", "jerrycan", "pressure_gauge", "bolt_cutters", "burlap_mask", "armband", "key_ring", "rivet_gun", "hydraulic_hose"], "tiles": [],
  "plates": ["17_the_farm", "19_the_stockade", "20_warmth_kept", "21_the_snow_pass", "22_the_scrap_yard"], "backgrounds": ["reaper_stockade", "hearth_hall", "scrap_yard", "tank_farm"]},
]


def tile_sheet(t):
    d = f"{O3}/tiles/{t}"
    fs = sorted(glob.glob(f"{d}/tile_*.png"), key=lambda p: int(os.path.basename(p)[5:-4]) if os.path.basename(p)[5:-4].isdigit() else 0)
    if not fs: fs = sorted(glob.glob(f"{d}/*.png"))
    fs = [f for f in fs if not f.endswith("_sheet.png")]
    if not fs: return None, 0
    ims = [Image.open(f).convert("RGBA") for f in fs]; n = len(ims); cols = min(n, 9); rows = (n + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 32, rows * 32), (0, 0, 0, 0))
    for i, im in enumerate(ims): sheet.paste(im.resize((32, 32)), ((i % cols) * 32, (i // cols) * 32))
    sp = f"{d}/{t}_sheet.png"; sheet.save(sp); return sp, n


def kit_sheet(k):
    d = f"{O3}/kits/{k}"; fs = sorted(f for f in glob.glob(f"{d}/*.png") if not f.endswith("_sheet.png"))
    if not fs: return None, 0
    ims = [Image.open(f).convert("RGBA") for f in fs]; n = len(ims); w = max(i.width for i in ims); h = max(i.height for i in ims); cols = min(n, 8); rows = (n + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * w, rows * h), (0, 0, 0, 0))
    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sp = f"{d}/{k}_sheet.png"; sheet.save(sp); return sp, n


def build():
    os.makedirs(DEST, exist_ok=True)
    data = {}; body = []; nav = []
    for s in SECTIONS:
        nav.append(f'<a href="#{s["id"]}">{s["title"]}</a>')
        h = [f'<section id="{s["id"]}"><div class="sub">{s["sub"]}</div><h2>{s["title"]}</h2><div class="lore">' + "".join(f"<p>{p}</p>" for p in s["lore"]) + "</div>"]
        plates = [p for p in s.get("plates", []) if os.path.exists(f"{O3}/story/{p}.png")]
        if plates:
            h.append('<h3>Story plates — generated background, generated sprites, composed 1:1</h3><div class="plates">')
            for p in plates: h.append(f'<figure class="plate" style="margin:0"><img src="{b64(f"{O3}/story/{p}.png")}"><figcaption>{p[3:].replace("_", " ")}</figcaption></figure>')
            h.append("</div>")
        cards = []
        for k in s["chars"]:
            e = char_entry(k)
            if not e: continue
            data[k] = e
            new = [a for a, v in e["anims"].items() if v.get("new")]; old = [a for a, v in e["anims"].items() if not v.get("new")]
            label = (", ".join(sorted(new)) + " <span style='color:#d9b45c'>new</span>" if new else "") + ((" · " if new else "") + ", ".join(sorted(old)) if old else "")
            por = f'<img class="p" src="{e["portrait"]}">' if e.get("portrait") else ""
            cards.append(f'<div class="card" data-key="{k}"><canvas width="{e["fw"]}" height="{e["fw"]}"></canvas>{por}<b>{e["name"]}</b><small>{label or "rotations"}</small></div>')
        for k in s.get("objects8", []):
            e = obj_entry("objects8/" + k)
            if not e: continue
            data[e["key"]] = e
            cards.append(f'<div class="card" data-key="{e["key"]}"><canvas width="{e["fw"]}" height="{e["fw"]}"></canvas><b>{e["name"]}</b><small>8 directions · object</small></div>')
        if cards: h.append('<h3>People and vehicles — click a sprite to step its facing</h3><div class="grid">' + "".join(cards) + "</div>")
        objs = [(o, f"{O3}/objects/{o}/{o}.png") for o in s.get("objects", []) if os.path.exists(f"{O3}/objects/{o}/{o}.png")]
        if objs: h.append('<h3>Map objects</h3><div class="objs">' + "".join(f'<figure style="width:{max(104, OBJ.get(o, 64) + 16)}px"><img src="{b64(p)}" style="width:{OBJ.get(o, 64) * (1 if OBJ.get(o, 64) >= 96 else 1.4):.0f}px;height:auto"><figcaption>{o.replace("_", " ")}</figcaption></figure>' for o, p in objs) + "</div>")
        icons = [(i, f"{O3}/icons/{i}/{i}.png") for i in s.get("icons", []) if os.path.exists(f"{O3}/icons/{i}/{i}.png")]
        if icons: h.append('<h3>Inventory icons</h3><div class="icons">' + "".join(f'<figure><img src="{b64(p)}"><figcaption>{i.replace("_", " ")}</figcaption></figure>' for i, p in icons) + "</div>")
        tiles = []
        for t in s.get("tiles", []):
            sp, n = tile_sheet(t)
            if sp:
                im = Image.open(sp); tiles.append(f'<figure><img src="{b64(sp)}" width="{im.width * 2}" height="{im.height * 2}"><figcaption>{t.replace("_", " ")} · {n} tiles</figcaption></figure>')
        for k in s.get("kits", []):
            sp, n = kit_sheet(k)
            if sp:
                im = Image.open(sp); tiles.append(f'<figure><img src="{b64(sp)}" width="{im.width * 2}" height="{im.height * 2}"><figcaption>building kit · {k.replace("_", " ")} · {n} pieces</figcaption></figure>')
        if tiles: h.append('<h3>Tiles and building kits</h3><div class="tiles">' + "".join(tiles) + "</div>")
        bgs = [(b, first(f"{O3}/plates/{b}/*.png")) for b in s.get("backgrounds", [])]; bgs = [(b, p) for b, p in bgs if p]
        if bgs: h.append('<h3>Backgrounds</h3><div class="plates">' + "".join(f'<figure class="plate" style="margin:0"><img src="{b64(p)}"><figcaption>{b.replace("_", " ")}</figcaption></figure>' for b, p in bgs) + "</div>")
        h.append("</section>"); body.append("".join(h))
    # interface
    em = [(k.split("/")[1], f"{O3}/emblems/{k.split('/')[1]}/{k.split('/')[1]}.png") for k in EMBLEMS]; em = [(k, p) for k, p in em if os.path.exists(p)]
    ui = []
    for k in UI:
        p = first(f"{O3}/{k}/*.png")
        if p: ui.append(f'<figure class="ui" style="margin:0"><img src="{b64(p)}"><figcaption class="sub" style="margin-top:6px">{k.split("/")[1].replace("_", " ")}</figcaption></figure>')
    fp = first(f"{O3}/ui/font_bunker/*.png")
    fh = f'<h3>Font — Diefenbunker Stencil (TTF in the package)</h3><figure class="font" style="margin:0"><img src="{b64(fp)}"></figure>' if fp else ""
    emh = '<h3>Faction emblems</h3><div class="icons">' + "".join(f'<figure><img src="{b64(p)}"><figcaption>{k.replace("_", " ")}</figcaption></figure>' for k, p in em) + "</div>" if em else ""
    if ui or fh or emh: body.append(f'<section id="ui"><div class="sub">Interface</div><h2>Emblems, panels and type</h2>{emh}<h3>Panels</h3><div class="uis">{"".join(ui)}</div>{fh}</section>'); nav.append('<a href="#ui">Interface</a>')
    head = c1.HTML_HEAD.replace("<title>The Convergence Codex</title>", "<title>Hearth and Road Codex</title>")
    head = head.replace('<div class="sub">The starting quadrant · where the histories meet</div><h1>The Convergence <em>codex</em></h1>', '<div class="sub">03BATCH · the world the cast stands in</div><h1>Hearth and Road <em>codex</em></h1>')
    head = head.replace('<p class="lede">Behind them stood UNITY. Beyond UNITY stood Waylight. Ahead lay a quadrant that would be written into the annals of history by people who would not agree about what had happened there. This is that quadrant\'s cast, in the compendium\'s words and in sprites made to its measure.</p>',
                        '<p class="lede">The first two batches drew the people. This one draws what they stand among: the old world left where it fell, the Republic\'s road furniture, the Farlands at the hearth, Waylight at home, the bunker inside — and the party at a run.</p>')
    html = head.replace("__NAV__", "".join(nav)).replace("__BODY__", "".join(body)).replace("__DATA__", json.dumps(data))
    open(f"{DEST}/hearth_and_road_codex.html", "w").write(html)
    open("/tmp/claude-0/-home-claude/635234b1-6687-5716-8ffe-c53919b32c9c/scratchpad/hearth_and_road_codex.html", "w").write(html)
    print("codex", len(data), "cards,", os.path.getsize(f"{DEST}/hearth_and_road_codex.html") // 1024, "KB")


if __name__ == "__main__":
    build()
