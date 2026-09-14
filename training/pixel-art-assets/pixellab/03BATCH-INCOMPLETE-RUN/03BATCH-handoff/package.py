"""package: manifest + sprite browser (single html) + zip."""
import os, json, base64, glob
from PIL import Image

OUT = "out"; DEST = "/mnt/user-data/outputs/pixellab"
GROUPS = [
 ("party", "The Postman and the party", ["postman", "tally", "merrow", "kell", "ada"]),
 ("farkeeper", "Farkeepers", ["spearman", "longbowman", "pugugly", "berserker", "rifle_rider", "recon_rider"]),
 ("reaper", "Reapers", ["conscript", "raider", "blackguard", "second", "admiral"]),
 ("smoke", "The Smoke", ["smoker", "torch", "gauger", "anointer"]),
 ("waylight", "Waylight", ["mail_worker", "hauler", "donkey"]),
 ("lamplighter", "Lamplighters", ["nomad"]),
 ("diefenbunker", "Diefenbunker Society", ["soldier", "salvager"]),
]
st = json.load(open("batch_state.json")); side = json.load(open("side_state.json")) if os.path.exists("side_state.json") else {}
ids = {k: v["id"] for k, v in st["chars"].items()}; ids.update({k: v["id"] for k, v in side.items()})


def b64(p): return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()


man = {"api": "https://api.pixellab.ai/v2", "frame": 64, "view": "low top-down", "directions": ["south", "south-west", "west", "north-west", "north", "north-east", "east", "south-east"], "groups": []}
data = []
for fac, title, names in GROUPS:
    g = {"id": fac, "title": title, "characters": []}
    for n in names:
        d = f"{OUT}/{fac}/{n}"
        rot = f"{d}/{n}_rotations.png"
        if not os.path.exists(rot): continue
        c = {"name": n, "id": ids.get(f"{fac}/{n}"), "rotations": f"{fac}/{n}/{n}_rotations.png", "animations": {}}
        entry = {"name": n, "rot": b64(rot), "anims": {}}
        for a in ("walk", "idle"):
            sheet = f"{d}/{a}/{n}_{a}_sheet.png"; meta = f"{d}/{a}/{n}_{a}.json"
            if os.path.exists(sheet):
                m = json.load(open(meta)); c["animations"][a] = {"sheet": f"{fac}/{n}/{a}/{n}_{a}_sheet.png", **m}
                entry["anims"][a] = {"sheet": b64(sheet), **m}
        g["characters"].append(c); data.append({"group": fac, **entry})
    man["groups"].append(g)
os.makedirs(DEST, exist_ok=True)
json.dump(man, open(f"{DEST}/manifest.json", "w"), indent=1)

HTML = r'''<title>Waylight Sprite Bench</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{--ink:#12141c;--slate:#1e2230;--slate-2:#2a2f40;--line:#3a4054;--parchment:#e7dcc4;--dim:#a9a08c;--brass:#d9b45c;--postal:#6f93b6;
--ff-display:"Cormorant Garamond",Georgia,serif;--ff-body:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif;--ff-mono:"IBM Plex Mono",Menlo,Consolas,monospace}
html,body{margin:0;background:var(--ink);color:var(--parchment);font-family:var(--ff-body);font-size:14px}
.wrap{max-width:1180px;margin:0 auto;padding:26px 22px 60px}
h1{font-family:var(--ff-display);font-weight:500;font-size:40px;margin:0;line-height:1}h1 em{color:var(--brass);font-style:italic}
.sub{font-family:var(--ff-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim)}
header{display:flex;justify-content:space-between;align-items:baseline;gap:20px;flex-wrap:wrap;margin-bottom:18px}
.ctl{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:12px 0 22px}
.ctl button,.ctl select{font-family:var(--ff-mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--parchment);background:var(--slate-2);border:1px solid var(--line);padding:7px 10px;cursor:pointer}
.ctl button.on{border-color:var(--brass);color:var(--brass)}
.ctl label{font-family:var(--ff-mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim)}
h2{font-family:var(--ff-display);font-weight:500;font-size:26px;margin:26px 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}
.card{background:var(--slate);border:1px solid var(--line);padding:10px;display:flex;flex-direction:column;gap:8px}
.card canvas{width:100%;height:auto;image-rendering:pixelated;background:var(--ink);cursor:pointer}
.card b{font-weight:500;font-size:14px}.card small{font-family:var(--ff-mono);font-size:10.5px;color:var(--dim);letter-spacing:.04em;display:block}
.dirs{display:flex;gap:2px}.dirs i{flex:1;height:4px;background:var(--line)}.dirs i.on{background:var(--brass)}
</style>
<div class="wrap">
<header><div><div class="sub">generated with PixelLab v3 · 64 px · low top-down · 8 directions</div><h1>Sprite <em>bench</em></h1></div><div class="sub" id="count"></div></header>
<div class="ctl"><label>show</label><button data-a="rot" class="on">rotations</button><button data-a="walk">walk</button><button data-a="idle">idle</button><label style="margin-left:14px">facing</label><select id="dir"><option value="-1">turntable</option><option>south</option><option>south-west</option><option>west</option><option>north-west</option><option>north</option><option>north-east</option><option>east</option><option>south-east</option></select><label style="margin-left:14px">zoom</label><button id="zoom">3×</button></div>
<div id="groups"></div>
</div>
<script>
const DATA=__DATA__; const GROUPS=__GROUPS__; const DIRS=["south","south-west","west","north-west","north","north-east","east","south-east"];
let mode="rot", dir=-1, zoom=3, tick=0; const imgs={};
function load(src){return new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.src=src;});}
(async()=>{
 for(const d of DATA){imgs[d.group+"/"+d.name]={rot:await load(d.rot)}; for(const a in d.anims) imgs[d.group+"/"+d.name][a]=await load(d.anims[a].sheet);}
 const root=document.getElementById("groups"); let n=0;
 for(const g of GROUPS){const h=document.createElement("h2");h.textContent=g.title;root.appendChild(h);const grid=document.createElement("div");grid.className="grid";root.appendChild(grid);
  for(const d of DATA.filter(x=>x.group===g.id)){n++;const c=document.createElement("div");c.className="card";
   c.innerHTML=`<canvas width="64" height="64"></canvas><div class="dirs">${DIRS.map(()=>"<i></i>").join("")}</div><b>${d.name.replace(/_/g," ")}</b><small>${Object.keys(d.anims).length? "walk "+(d.anims.walk?d.anims.walk.frames:"–")+"f · idle "+(d.anims.idle?d.anims.idle.frames:"–")+"f":"rotations only"}</small>`;
   c.querySelector("canvas").onclick=()=>{c.dataset.dir=((+(c.dataset.dir||-1))+2)%9-1};grid.appendChild(c);c.dataset.key=d.group+"/"+d.name;c.dataset.dir=-1;}}
 document.getElementById("count").textContent=n+" characters";
 document.querySelectorAll(".ctl button[data-a]").forEach(b=>b.onclick=()=>{mode=b.dataset.a;document.querySelectorAll(".ctl button[data-a]").forEach(x=>x.classList.toggle("on",x===b));});
 document.getElementById("dir").onchange=e=>{dir=e.target.value==="-1"?-1:DIRS.indexOf(e.target.value);};
 document.getElementById("zoom").onclick=function(){zoom=zoom===3?4:zoom===4?2:3;this.textContent=zoom+"×";document.querySelectorAll(".card canvas").forEach(cv=>cv.style.maxWidth=(64*zoom)+"px");};
 document.querySelectorAll(".card canvas").forEach(cv=>cv.style.maxWidth=(64*zoom)+"px");
 let last=0; function loop(ts){requestAnimationFrame(loop); if(ts-last<110) return; last=ts; tick++;
  for(const card of document.querySelectorAll(".card")){const key=card.dataset.key; const d=DATA.find(x=>x.group+"/"+x.name===key); const cv=card.querySelector("canvas"); const ctx=cv.getContext("2d"); ctx.imageSmoothingEnabled=false; ctx.clearRect(0,0,64,64);
   const cd=+card.dataset.dir; const di = cd>=0?cd : dir>=0?dir : Math.floor(tick/8)%8;
   card.querySelectorAll(".dirs i").forEach((el,i)=>el.classList.toggle("on",i===di));
   const set=imgs[key]; if(!set) continue;
   if(mode==="rot"||!set[mode]){ctx.drawImage(set.rot,di*64,0,64,64,0,0,64,64);} else {const a=d.anims[mode]; const row=a.directions.indexOf(DIRS[di]); if(row<0){ctx.drawImage(set.rot,di*64,0,64,64,0,0,64,64);continue;} const f=tick%a.frames; ctx.drawImage(set[mode],f*a.w,row*a.h,a.w,a.h,0,0,64,64);}
  }}
 requestAnimationFrame(loop);
})();
</script>'''
html = HTML.replace("__DATA__", json.dumps(data)).replace("__GROUPS__", json.dumps([{"id": g[0], "title": g[1]} for g in GROUPS]))
open(f"{DEST}/sprite_bench.html", "w").write(html)
open("/tmp/claude-0/-home-claude/635234b1-6687-5716-8ffe-c53919b32c9c/scratchpad/sprite_bench.html", "w").write(html)
# copy assets
import shutil
for fac, _, names in GROUPS:
    for n in names:
        src = f"{OUT}/{fac}/{n}"
        if os.path.isdir(src): shutil.copytree(src, f"{DEST}/{fac}/{n}", dirs_exist_ok=True)
for f in glob.glob(f"{OUT}/*_x3.png"): shutil.copy(f, DEST)
shutil.copy("plclient.py", DEST); shutil.copy("batch.py", DEST)
print("packaged", len(data), "characters;", os.path.getsize(f"{DEST}/sprite_bench.html") // 1024, "KB html")
