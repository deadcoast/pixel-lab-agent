"""The Convergence — a field codex. One page: the starting quadrant's peoples, with the compendium's own words, and every
asset made for them: portraits, live sprites (rotations / walk / idle / extra), objects, icons, tiles, story plates."""
import os, json, base64, glob

OUT2 = "out2"; OUT = "out"; DEST = "/mnt/user-data/outputs/convergence"


def b64(p): return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()


def first(pattern):
    fs = sorted(glob.glob(pattern)); return fs[0] if fs else None


def char_entry(key):
    fac, name = key.split("/")
    base = f"{OUT2}/{fac}/{name}" if os.path.isdir(f"{OUT2}/{fac}/{name}") else (f"{OUT}/{fac}/{name}" if os.path.isdir(f"{OUT}/{fac}/{name}") else f"{OUT}/{name}")
    rot = f"{base}/{name}_rotations.png"
    if not os.path.exists(rot): return None
    e = {"key": key, "name": name.replace("_", " "), "rot": b64(rot), "anims": {}}
    for d in sorted(glob.glob(f"{base}/*/")):
        a = os.path.basename(d.rstrip("/")); sheet = f"{d}/{name}_{a}_sheet.png"; meta = f"{d}/{name}_{a}.json"
        if os.path.exists(sheet) and os.path.exists(meta):
            m = json.load(open(meta)); e["anims"][a] = {"sheet": b64(sheet), **m}
    p = first(f"{OUT2}/portraits/{name}/*.png")
    if p: e["portrait"] = b64(p)
    return e


SECTIONS = [
 {"id": "diefenbunker", "title": "The People Beneath the Door", "sub": "The Diefenbunker Society · §10–14",
  "lore": ["Descendants of a Canadian-origin population, including its old political class, who lived hundreds of years underground passing down occupations, habits and an increasingly distant account of the world outside. Highly educated, trained for survival, with mechanical expertise, administrative traditions and the arsenal of a great continuity effort.",
           "On New World Day the alarms sounded, pistons worked against centuries of rust, and a five-hundred-ton door scraped open. They came forward in work gear expecting to dig and salvage. What they found was people, conflict, Reapers, Cannibals. The outer seal had been built to open permanently; there was no going back below.",
           "The Society records people through inherited administrative language: SBSN, Social Bunker Security Number; SBCA, Social Bunker Career Assignment. Some leaders still wear the old pins. There is a red leaf engraved on a weapon's sight housing."],
  "chars": ["diefenbunker/douglas_reed", "diefenbunker/sarah_oconnel", "diefenbunker/jimmy_butler", "diefenbunker/enforcement_trooper", "diefenbunker/work_crew", "diefenbunker/soldier", "diefenbunker/salvager"],
  "objects": ["blast_door", "bunker_hatch", "bullion_crate_barricade", "comms_array", "decon_shower"],
  "icons": ["c8_carbine", "c7_rifle", "c22_pistol", "red_leaf_pin", "welding_torch"],
  "testimonies": [
    ("SBSN:DOUGLAS REED · SBCA: DIEFENBUNKER PRIME ADMINISTER · SAT AUG 10 · 13 DAYS POST UNSEAL", "douglas_reed", "THE SOCIETY, OUR PERFECT LITTLE BUBBLE. IT FINALLY SURFACED; THE ALARMS BLARED, THE PISTONS AND HYDRAULIST HISSED, THE RUST BROKE FREE OF THE SEALS AND THAT 500 TON DOOR FINALLY SCRAPED OPEN. NEW WORLD DAY WAS FINNALY HERE. WE WERE SURFACING IN OUR WORK GEAR; READY TO DIG; READY TO SALVAGE; READY TO TWIST THE METAL OF THE OLD WORLD STRAIGHT. BUT WE DIDNT FIND RUIN, WE DIDNT FIND CITIES OF OLD. WE FOUND DEATH. DEATH WE THOUGHT COULDNT EXIST."),
    ("SBSN: SARAH OCONNEL · SBCA: MECHANIC · SAT AUG 9 · 12 DAYS POST WHATEVER THE OPPOSITE OF HOPE IS", "sarah_oconnel", "THE YEAR FINALLY CAME; THEY CALLED IT NEW WORLD DAY. THE DAY THE ALL KNOWING GATES OPENED, THE DAY MATH TOLD US EARTH WAS READY TO REPOPULATE AND THE RADIOTION LEVELS HAD DROPPED ENOUGH WE COULD RE-CULTIVATE THE LAND; BUT WHEN WE SURFACED WHAT WE FOUND WASNT WHAT WE EXPECTED. SAVAGES, BARBARIANS, REAPERS, CANNIBALS; W A R. WE TRIED TO REASON WITH THEM, THERE WASNT ANY. WE WANTED TO START THE NEW WORLD; INSTEAD WE RETREATED BACK TO THE IRON WALLS OF OUR OLD ONE. BUT WE COULDNT SHUT THE DOORS. WE COULDNT RESEAL WHAT WAS DESIGNED TO UNSEAL PERMANENTLY. WE DIDNT HAVE THE TECHNOLOGY ANYMORE TO REBUILD WHAT SEALED US IN THE FIRST PLACE; HELL WE DIDNT EVEN HAVE THE FOOD OR SUPPLIES TO LAST ANOTHER CYCLE. THIS WAS OUR NEW HOME NOW, IN THE NEW WORLD, DOORS OPEN UNTILL WE GET THE WELDERS UP."),
    ("SBSN: JIMMY BUTLER · SBCA: DIEFENBUNKER ENFORCEMENT DEPARTMENT - LIEUTENANT · SAT AUG 13 · 16 DAYS POST NWD", "jimmy_butler", "AS THE RED ALERT FLICKERED TO LIFE AND THE ALARMS SCREAMED MOVEMENT AT THE BUNKER HATCHES; WE PREPARED FOR THE WORST. OUR SOLDIERS GRABBED THEIR PRE-BUNKER ERA ASSAULT RIFLES; THE ONES THAT READ C8 AND HAD THE READ LEAF ETCHED INTO THE SIGHTS. OUR LEADERS STILL WORE THEIR PINS; THE ONES OF THE OLD TIMES AND THE ANCIENT ONES. THE ONES WHO STILL BELIEVED WE CAME FROM A PLACE CALLED CANADA AND THIS BUNKER WAS ORIGINALLY THE LAST HAVEN OF THE FREE WORLD. SOMETHING ABOUT THE COLD, SOMETHING ABOUT THE WATER."),
  ],
  "plates": ["01_new_world_day", "02_movement_at_the_hatches"]},
 {"id": "lamplighter", "title": "The Cloaked Torch", "sub": "Lamplighters and the Nomads · §8–9, §13–14, P09",
  "lore": ["A Waylighter who chose violence against another loses his place among his people. Enough have been exiled to make a faction, the Lamplighter Nomads, dispersed far beyond the known Darklands; somewhere beyond those horizons they have already founded a city the nomads on these roads do not know about.",
           "They keep the Waylighter's mobility and hauling and add distance, patience and concealment: snipers, not brutes. The Diefenbunker Society took them in, and its precision rifles — the C14 Timberwolf, the C3A1, the C20 DMR — belong to the Lamplighter arsenal now.",
           "The light is still carried. It is no longer shown the same way."],
  "chars": ["lamplighter/sniper", "lamplighter/marksman", "lamplighter/nomad_hauler", "lamplighter/nomad_elder", "lamplighter/nomad"],
  "objects": ["cloaked_lantern", "nomad_tent"], "icons": ["cloaked_torch", "c14_timberwolf", "c3a1_rifle", "c20_dmr"], "plates": ["07_the_cloaked_torch"]},
 {"id": "reaper", "title": "The Right to Take", "sub": "Reaper territory · §3, §15, P01",
  "lore": ["The Reapers treat production as theirs when they have the force to seize it: a working field, a storehouse, a passing caravan, a captured courier. Their power is turning repeated taking into a permanent order, and their look is confiscated civic and military clothing made uniform through repeated marks of ownership.",
           "Inside their territory the news of the Light arrives as a warning about a foreign power. A household need know nothing of Waylight's prosperity to fear that prediction. A Reaper's child might remember the Republic as the people who killed a parent; someone released from the same stronghold might remember the same soldiers as the first people who ever came to help. Both would remember the uniforms.",
           "A Waylighter caught behind Reaper lines cannot rely on the promises that travel with the Republic."],
  "chars": ["reaper/overseer", "reaper/captive", "reaper/household_woman", "reaper/child", "waylight/haven_courier", "reaper/conscript", "reaper/raider", "reaper/blackguard", "reaper/second", "reaper/admiral"],
  "objects": ["reaper_marker"], "icons": [], "plates": ["03_behind_reaper_lines"]},
 {"id": "cannibal", "title": "Those Outside the Circle", "sub": "The communities the Republic calls Cannibals · §3, P04 (revised)",
  "lore": ["The name may gather communities whose inherited practices have become horrific to outsiders while remaining familiar within the lives that reproduce them. A community might preserve detailed practical knowledge and oral memory while having lost literacy and any contact with wider political systems. Its people would not thereby lack intelligence, affection, or a social order of their own.",
           "From such a viewpoint the Republic's offer could be incomprehensible before its force became unmistakable: polished weapons, unfamiliar speech, threatened living grounds. A promise written in an unfamiliar hand tells a person who cannot read it nothing. The armed stranger standing behind it is considerably easier to understand.",
           "Designed here as a people with learned local practices and lived material conditions: hides, ash and ochre, snare wire, a pipe spear, a cook pot, a marker post at the gathering place. No monster costume."],
  "chars": ["cannibal/hunter", "cannibal/hearth_keeper", "cannibal/lookout"], "objects": ["hill_totem", "campfire"], "icons": [], "plates": ["05_the_unread_promise"]},
 {"id": "roads", "title": "Roads That Remember", "sub": "The Republic's road crews and the road itself · §4–5, §6, P07–P08",
  "lore": ["People pass between two settlements and their traffic presses a line into the ground. In time a community or its Waylighters improve it with cobblestone, timber, or metal scrap. Masons provide the cobble, Forresters fell the timber, Path Pressers establish the routes by deliberate travel. The tree that supplied the timber is no longer standing.",
           "The network has stations, storage points, ladders, shelters and post boxes; a shelter must shelter, a defended place must protect, a donation must enter another life.",
           "Rifle Riders and Recon Riders need horses, and different animals bring different strengths in speed, toughness and travel. A proposed custom: a newly connected settlement gathers when the first reply comes back along the route, because the reply proves another person at the far end."],
  "chars": ["waylight/mason", "waylight/forrester", "waylight/path_presser", "farkeeper/captain", "animals/draft_horse", "animals/light_horse", "waylight/mail_worker", "waylight/hauler", "waylight/donkey"],
  "objects": ["station_shelter", "post_box", "milestone", "ladder", "cache_crate", "mail_cart", "road_roller", "cobble_pile", "timber_stack", "scrap_pile", "letter_bundle", "first_reply_table", "wire_fence_gate", "everflame_brazier"],
  "icons": ["letter_plain", "letter_sealed", "letter_brass", "cargo_crate", "cobblestone", "timber", "scrap_metal", "mail_satchel", "map_tube", "ration", "water_flask", "saddle", "longbow", "claymore", "spear", "tally_stick"],
  "tiles": ["grass_to_path", "cobble_roads", "timber_roads", "scrap_roads", "worn_path_roads", "dirt_to_cobble", "grass_to_snow", "gravel_to_water", "moss_to_rock"],
  "plates": ["04_the_road_station", "06_the_republic_sets_out", "08_the_first_reply"]},
 {"id": "claims", "title": "Six Claims Upon the Road", "sub": "Raiders, Rebels, Flame Keepers, Iron Giants · §15, P02–P06 (proposed)",
  "lore": ["Raiders are mobile groups whose unity lasts as long as a profitable undertaking; their gear is adapted for travel and theft, and the common word bandit need not name a single faction. Rebels are united, imperfectly, by resistance to the authority arriving alongside the letters — people of particular places, with settlement signs and practical regional dress, who might welcome a courier and fight the force that governs the destination.",
           "The Flame Keepers build authority around custodianship of ordinary heat: working furnaces, reliable hearths, and the fuel and skill to keep them going. Their claim is that warmth survives because someone limits access to it. The Iron Giants, in the proposed reading, are a salvage power organised around enormous human-operated armoured working frames — the name belongs to the machines and to the society whose authority depends on them.",
           "Part II of the compendium marks all of these as proposals, and so are the sprites: a first physical reading, to be kept or replaced."],
  "chars": ["raider/rover", "raider/bandit", "rebel/militiaman", "rebel/speaker", "flamekeeper/furnace_warden", "flamekeeper/stoker", "irongiant/frame_pilot", "irongiant/working_frame"],
  "objects": ["furnace", "salvage_frame_parked", "highleaf_bale"], "icons": ["highleaf", "coal_lantern"], "plates": ["09_warmth_under_guard", "10_the_weight_of_the_old_world"]},
]

HTML_HEAD = r'''<title>The Convergence Codex</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{--ink:#12141c;--slate:#1e2230;--slate-2:#2a2f40;--line:#3a4054;--parchment:#e7dcc4;--dim:#a9a08c;--brass:#d9b45c;--postal:#6f93b6;--red:#b8483a;--phos:#8fd39a;
--ff-display:"Cormorant Garamond",Georgia,serif;--ff-body:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif;--ff-mono:"IBM Plex Mono",Menlo,Consolas,monospace}
html,body{margin:0;background:var(--ink);color:var(--parchment);font-family:var(--ff-body);font-size:14.5px;line-height:1.5}
.wrap{max-width:1180px;margin:0 auto;padding:28px 22px 80px}
header{display:flex;justify-content:space-between;align-items:baseline;gap:20px;flex-wrap:wrap;margin-bottom:6px}
h1{font-family:var(--ff-display);font-weight:500;font-size:46px;margin:0;line-height:1}h1 em{color:var(--brass);font-style:italic}
.sub{font-family:var(--ff-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim)}
.lede{font-family:var(--ff-display);font-size:21px;line-height:1.35;max-width:66ch;margin:14px 0 26px}
nav{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 30px}nav a{font-family:var(--ff-mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--parchment);background:var(--slate-2);border:1px solid var(--line);padding:6px 10px;text-decoration:none}nav a:hover{border-color:var(--brass);color:var(--brass)}
section{margin:0 0 54px;padding-top:10px;border-top:1px solid var(--line)}
h2{font-family:var(--ff-display);font-weight:500;font-size:34px;margin:14px 0 2px;line-height:1.05}
.lore{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px;margin:16px 0 22px}.lore p{margin:0;max-width:64ch;color:var(--parchment)}
h3{font-family:var(--ff-mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);margin:22px 0 10px;font-weight:500}
.plates{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:14px}.plate img{width:100%;height:auto;image-rendering:pixelated;display:block;border:1px solid var(--line)}
.plate figcaption{font-family:var(--ff-mono);font-size:11px;letter-spacing:.05em;color:var(--dim);margin:6px 0 0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.card{background:var(--slate);border:1px solid var(--line);padding:8px;display:flex;flex-direction:column;gap:6px;position:relative}
.card canvas{width:100%;height:auto;image-rendering:pixelated;background:var(--ink);cursor:pointer}
.card b{font-weight:500;font-size:13px;text-transform:capitalize}.card small{font-family:var(--ff-mono);font-size:10px;color:var(--dim);letter-spacing:.04em;display:block}
.card .p{position:absolute;right:8px;top:8px;width:32px;height:32px;image-rendering:pixelated;border:1px solid var(--line);background:var(--ink)}
.objs{display:flex;gap:10px;flex-wrap:wrap}.objs figure{margin:0;background:var(--slate);border:1px solid var(--line);padding:8px;width:104px;text-align:center}.objs img{image-rendering:pixelated;width:88px;height:88px;object-fit:contain;display:block;margin:0 auto}
.objs figcaption{font-family:var(--ff-mono);font-size:10px;color:var(--dim);margin-top:4px;letter-spacing:.03em}
.icons{display:flex;gap:6px;flex-wrap:wrap}.icons figure{margin:0;background:var(--slate);border:1px solid var(--line);padding:6px;width:64px;text-align:center}.icons img{image-rendering:pixelated;width:48px;height:48px;display:block;margin:0 auto}.icons figcaption{font-family:var(--ff-mono);font-size:9px;color:var(--dim);margin-top:3px}
.tiles{display:flex;gap:12px;flex-wrap:wrap}.tiles figure{margin:0}.tiles img{image-rendering:pixelated;display:block;border:1px solid var(--line)}.tiles figcaption{font-family:var(--ff-mono);font-size:10px;color:var(--dim);margin-top:4px}
.testi{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px;margin:8px 0 6px}
.t{background:#0d1a12;border:1px solid #2a4a34;padding:12px 14px;font-family:var(--ff-mono);font-size:11.5px;line-height:1.55;color:var(--phos);display:grid;grid-template-columns:64px 1fr;gap:12px}
.t img{width:64px;height:64px;image-rendering:pixelated;border:1px solid #2a4a34;background:#0a1410}.t .h{color:#5f9a6d;font-size:10px;letter-spacing:.06em;margin-bottom:6px}
.ctl{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 8px}.ctl button{font-family:var(--ff-mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--parchment);background:var(--slate-2);border:1px solid var(--line);padding:6px 9px;cursor:pointer}.ctl button.on{border-color:var(--brass);color:var(--brass)}
.ui img{image-rendering:pixelated;max-width:100%;display:block;border:1px solid var(--line)}.uis{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:14px}
.font img{image-rendering:pixelated;max-width:100%;display:block}
</style>
<div class="wrap">
<header><div><div class="sub">The starting quadrant · where the histories meet</div><h1>The Convergence <em>codex</em></h1></div><div class="sub" id="count"></div></header>
<p class="lede">Behind them stood UNITY. Beyond UNITY stood Waylight. Ahead lay a quadrant that would be written into the annals of history by people who would not agree about what had happened there. This is that quadrant's cast, in the compendium's words and in sprites made to its measure.</p>
<nav>__NAV__</nav>
<div class="ctl"><span class="sub">sprites</span><button data-a="rot" class="on">rotations</button><button data-a="walk">walk</button><button data-a="idle">idle</button><button data-a="extra">extra</button><span class="sub" style="margin-left:10px">click a sprite to step its facing</span></div>
__BODY__
</div>
<script>
const DATA=__DATA__; const DIRS=["south","south-west","west","north-west","north","north-east","east","south-east"];
let mode="rot", tick=0; const imgs={};
function load(src){return new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=src;});}
(async()=>{
 for(const k in DATA){const d=DATA[k]; imgs[k]={rot:await load(d.rot)}; for(const a in d.anims) imgs[k][a]=await load(d.anims[a].sheet);}
 document.getElementById("count").textContent=Object.keys(DATA).length+" characters · "+document.querySelectorAll(".objs figure").length+" objects · "+document.querySelectorAll(".icons figure").length+" icons";
 document.querySelectorAll(".ctl button[data-a]").forEach(b=>b.onclick=()=>{mode=b.dataset.a;document.querySelectorAll(".ctl button[data-a]").forEach(x=>x.classList.toggle("on",x===b));});
 document.querySelectorAll(".card").forEach(c=>{c.dataset.dir=-1;c.querySelector("canvas").onclick=()=>{c.dataset.dir=((+(c.dataset.dir))+2)%9-1;};});
 let last=0; function loop(ts){requestAnimationFrame(loop); if(ts-last<110) return; last=ts; tick++;
  for(const card of document.querySelectorAll(".card")){const key=card.dataset.key; const d=DATA[key]; const set=imgs[key]; if(!d||!set) continue; const cv=card.querySelector("canvas"); const ctx=cv.getContext("2d"); ctx.imageSmoothingEnabled=false; const S=cv.width; ctx.clearRect(0,0,S,S);
   const cd=+card.dataset.dir; const di=cd>=0?cd:Math.floor(tick/8)%8;
   let a=null; if(mode==="walk") a=d.anims.walk; else if(mode==="idle") a=d.anims.idle; else if(mode==="extra"){const ks=Object.keys(d.anims).filter(x=>x!=="walk"&&x!=="idle"); if(ks.length) a=d.anims[ks[Math.floor(tick/48)%ks.length]];}
   if(!a){ctx.drawImage(set.rot,di*d.fw,0,d.fw,d.fw,0,0,S,S);continue;}
   const an=Object.keys(d.anims).find(x=>d.anims[x]===a); const row=a.directions.indexOf(DIRS[di]); const r=row<0?0:row; const f=tick%a.frames; ctx.drawImage(set[an],f*a.w,r*a.h,a.w,a.h,0,0,S,S);
  }}
 requestAnimationFrame(loop);
})();
</script>'''


def build():
    os.makedirs(DEST, exist_ok=True)
    data = {}; body = []; nav = []
    for s in SECTIONS:
        nav.append(f'<a href="#{s["id"]}">{s["title"]}</a>')
        h = [f'<section id="{s["id"]}"><div class="sub">{s["sub"]}</div><h2>{s["title"]}</h2><div class="lore">' + "".join(f"<p>{p}</p>" for p in s["lore"]) + "</div>"]
        if s.get("testimonies"):
            h.append('<h3>Three voices after the unsealing — verbatim from the record</h3><div class="testi">')
            for head, who, text in s["testimonies"]:
                p = first(f"{OUT2}/portraits/{who}/*.png"); img = f'<img src="{b64(p)}">' if p else "<div></div>"
                h.append(f'<div class="t">{img}<div><div class="h">{head}</div>{text}</div></div>')
            h.append("</div>")
        plates = [p for p in s.get("plates", []) if os.path.exists(f"{OUT2}/story/{p}.png")]
        if plates:
            h.append('<h3>Story plates — generated background, generated sprites, composed 1:1</h3><div class="plates">')
            for p in plates: h.append(f'<figure class="plate" style="margin:0"><img src="{b64(f"{OUT2}/story/{p}.png")}"><figcaption>{p[3:].replace("_", " ")}</figcaption></figure>')
            h.append("</div>")
        cards = []
        for k in s["chars"]:
            e = char_entry(k)
            if not e: continue
            e["fw"] = 96 if k == "irongiant/working_frame" else 64; data[k] = e
            anims = ", ".join(sorted(e["anims"].keys())) or "rotations"
            por = f'<img class="p" src="{e["portrait"]}">' if e.get("portrait") else ""
            cards.append(f'<div class="card" data-key="{k}"><canvas width="{e["fw"]}" height="{e["fw"]}"></canvas>{por}<b>{e["name"]}</b><small>{anims}</small></div>')
        if cards: h.append('<h3>People</h3><div class="grid">' + "".join(cards) + "</div>")
        objs = [(o, f"{OUT2}/objects/{o}/{o}.png") for o in s.get("objects", []) if os.path.exists(f"{OUT2}/objects/{o}/{o}.png")]
        if objs: h.append('<h3>Map objects</h3><div class="objs">' + "".join(f'<figure><img src="{b64(p)}"><figcaption>{o.replace("_", " ")}</figcaption></figure>' for o, p in objs) + "</div>")
        icons = [(i, f"{OUT2}/icons/{i}/{i}.png") for i in s.get("icons", []) if os.path.exists(f"{OUT2}/icons/{i}/{i}.png")]
        if icons: h.append('<h3>Inventory icons</h3><div class="icons">' + "".join(f'<figure><img src="{b64(p)}"><figcaption>{i.replace("_", " ")}</figcaption></figure>' for i, p in icons) + "</div>")
        tiles = []
        for t in s.get("tiles", []):
            fs = sorted(glob.glob(f"{OUT2}/tiles/{t}/tile_*.png"), key=lambda p: int(os.path.basename(p)[5:-4]) if os.path.basename(p)[5:-4].isdigit() else 0)
            if not fs: continue
            from PIL import Image
            ims = [Image.open(f).convert("RGBA") for f in fs]; n = len(ims); cols = min(n, 9); rows = (n + cols - 1) // cols
            sheet = Image.new("RGBA", (cols * 32, rows * 32), (0, 0, 0, 0))
            for i, im in enumerate(ims): sheet.paste(im.resize((32, 32)), ((i % cols) * 32, (i // cols) * 32))
            sp = f"{OUT2}/tiles/{t}/{t}_sheet.png"; sheet.save(sp)
            tiles.append(f'<figure><img src="{b64(sp)}" width="{cols * 64}" height="{rows * 64}"><figcaption>{t.replace("_", " ")} · {n} tiles</figcaption></figure>')
        if tiles: h.append('<h3>Tiles — the road materials of §5, as autotiles</h3><div class="tiles">' + "".join(tiles) + "</div>")
        h.append("</section>"); body.append("".join(h))
    # UI + font section
    ui = []
    for k in ("dialogue_panel", "bunker_panel"):
        p = first(f"{OUT2}/ui/{k}/*.png")
        if p: ui.append(f'<figure class="ui" style="margin:0"><img src="{b64(p)}"><figcaption class="sub" style="margin-top:6px">{k.replace("_", " ")}</figcaption></figure>')
    fp = first(f"{OUT2}/ui/font_postal/*.png")
    fh = f'<h3>Font — Waylight Postal (TTF in the package)</h3><figure class="font" style="margin:0"><img src="{b64(fp)}"></figure>' if fp else ""
    if ui or fh: body.append(f'<section id="ui"><div class="sub">Interface</div><h2>Panels and type</h2><h3>Dialogue panels</h3><div class="uis">{"".join(ui)}</div>{fh}</section>')
    nav.append('<a href="#ui">Interface</a>')
    html = HTML_HEAD.replace("__NAV__", "".join(nav)).replace("__BODY__", "".join(body)).replace("__DATA__", json.dumps(data))
    open(f"{DEST}/convergence_codex.html", "w").write(html)
    open("/tmp/claude-0/-home-claude/635234b1-6687-5716-8ffe-c53919b32c9c/scratchpad/convergence_codex.html", "w").write(html)
    print("codex", len(data), "characters,", os.path.getsize(f"{DEST}/convergence_codex.html") // 1024, "KB")


if __name__ == "__main__":
    build()
