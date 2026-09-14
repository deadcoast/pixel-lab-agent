"""Create a PX2 planning candidate through the bundled runtime's JSON adapter."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
runner = root / ".agents/skills/pixl-kit/scripts/pixl.py"
def cli(*args):
    return subprocess.check_output([sys.executable, str(runner), *args], cwd=root, text=True, encoding="utf-8")
doc = json.loads(cli("decode", ".pixl/state.px"))
assert doc["revision"] == 0
doc["revision"] += 1
rows = doc["records"]
ref = lambda name: {"$ref": name}
sym = lambda value: {"$symbol": value}
refs = lambda names: [ref(n) for n in names]
def add(name, kind, **fields):
    rows.append({"id": name, "kind": kind, "fields": fields})
def digest(path):
    return sha256((root/path).read_bytes()).hexdigest()
now = datetime.now(timezone.utc).isoformat()
def source(name, path, lines=None):
    add(name, "S", ur=path, dg=digest(path), ln=lines or [], at=now, au=sym("local"))
source("s.brief", "review/user-brief.txt", [1,3])
source("s.image", "translucent-reference.png")
source("s.measure", "review/reference-measurements.json")
source("s.visual", "review/reference-visual-review.md", [1,11])
source("s.research", "review/source-grounding.json")
deep = ".agents/skills/pixl-kit/resources/training/original-docs/PIXEL-ART-DEEP-RESEARCH.md"
source("s.edge-ramp", deep, [590,632])
source("s.sampling", deep, [907,919])
source("s.channels", deep, [945,977])
source("s.alignment", deep, [1276,1291])
source("s.archive", ".agents/skills/pixl-kit/resources/training/original-docs/PIXEL-ART-ASSETS.md", [942,958])
source("s.recipe", ".agents/skills/pixl-kit/resources/knowledge/pixel-art.json")
source("s.fixture", ".agents/skills/pixl-kit/resources/evidence/art-methods/poc-report.json")

choices = []
def choice(name, key, status, value, why, sources, owner="actor"):
    choices.append(name)
    add(name,"I",pr=ref("project"),wh=ref(owner),ky=key,st=sym(status),vl=value,so=refs(sources),wy=why)
choice("i.scope", "scope", "confirmed", "Reference review and lantern production approach", "Current assignment ends at the reviewed approach; sample creation is a retained next operation.", ["s.brief"], "user")
choice("i.alpha", "al", "confirmed", sym("full"), "User explicitly requires partial transparency; binary alpha would destroy that treatment.", ["s.brief"], "user")
choice("i.palette", "pl", "confirmed", [], "User has imposed no fixed palette. Empty list means no exact RGB membership restriction; final colors remain editable.", ["s.brief"], "user")
choice("i.edges", "edge_treatment", "confirmed", "Preserve selective authored anti-aliasing and partial transparency", "Carry the user's source aesthetic into new props.", ["s.brief"], "user")
choice("i.reference", "reference_metrics", "observed", {"px":[32,32],"bbox":[6,3,26,28],"rgb_count":3,"rgba_count":5,"fractional_pixels":30,"alpha_values":[0,96,160,255]}, "Reference measurements describe the source; they are not mandatory sprite color or pixel counts.", ["s.image","s.measure"])
choice("i.style", "reference_style", "observed", "Frontal block construction; opaque navy frame and teal fill; two warm cream blocks; partial-alpha side strips only", "Native and 8x inspection on light, dark and checker backgrounds; darkness reduces frame contrast.", ["s.image","s.visual"])
choice("i.canvas", "px", "proposed", [32,32], "Match the supplied reference's logical canvas for the first small sample.", ["s.measure"])
choice("i.view", "vw", "proposed", sym("ui"), "Frontal orthographic icon-like sample, matching the observed reference; ui is the raster contract convention and does not confirm the final gameplay use.", ["s.visual"])
choice("i.sampling", "sa", "proposed", sym("nearest"), "Nearest previews preserve authored alpha texels and hard clusters; final display scale remains unresolved.", ["s.sampling","s.research"])
light = "Flat navy structure and teal glass; one small warm cream light cluster; no inferred directional lighting"
choice("i.light", "li", "proposed", light, "Source uses flat areas; a warm lantern focal point makes its identity clear without adding a shading style.", ["s.visual"])
choice("i.shape", "lantern_shape", "proposed", "Compact loop handle, cap, two side rails, base and one central warm light; about 18-20 x 24-26 visible pixels", "Stay near the reference's 20 x 25 footprint while making the lantern recognizable.", ["s.visual","s.measure"])
choice("i.alpha-model", "export_alpha", "proposed", "RGBA PNG with straight alpha; verify preservation after save/reopen and check engine conversion once target is known", "The authored partial alpha is required; the actual import and blending route remains unproven.", ["s.research"])
choice("i.anchor", "anchor", "proposed", [16,28], "Initial bottom-center logical anchor at the reference ground line; keep untrimmed canvas. Final engine coordinates remain unresolved.", ["s.measure"])
choice("i.engine", "target_engine", "unresolved", None, "No engine or import project supplied. Blend state, atlas behavior and pivot convention need destination verification before game-ready delivery.", [])
choice("i.display", "target_display", "unresolved", None, "Final game backgrounds and display scale are unknown. Light/dark/checker previews are diagnostic substitutes.", [])

add("c.lantern-sample","C",nm="Proposed frontal lantern sample",px=[32,32],pl=[],vw=sym("ui"),sa=sym("nearest"),al=sym("full"),li=light,ch=refs(["i.canvas","i.view","i.sampling","i.alpha","i.palette","i.edges","i.light","i.shape","i.alpha-model","i.anchor"]))
add("x.reference","X",nm="Original translucent reference",ur="translucent-reference.png",dg=digest("translucent-reference.png"),kd=sym("reference"))
add("x.inspection","X",nm="Reference diagnostic composites at 1x and 8x",ur="review/reference-inspection.png",dg=digest("review/reference-inspection.png"),kd=sym("reference"))
add("k.alpha-research","K",nm="alpha-contract: candidate for lantern proof",ap=[sym("transparent_sprites")],op=["Keep alpha independent of RGB palette membership.","Retain full alpha and verify the chosen export/compositing route.","Review light/dark backgrounds and actual import before acceptance."],ck=["Selected translucent regions retain nonzero, nonopaque alpha.","Round-trip RGBA matches and chosen blend produces no matte fringe."],so=refs(["s.recipe","s.channels","s.alignment","s.archive","s.fixture","s.research"]),rq=["Chosen alpha model and destination renderer; project sample proof still needed."],rk=["The cited prose is about channels/alignment/CSS, not a complete compositing pipeline.","Bundled numeric POC proves no GPU/importer behavior."])
add("k.edge-research","K",nm="selective-edge-aa: candidate for lantern proof",ap=[sym("subpixel_edges")],op=["Define a selected edge mask and protect structural hard edges.","Choose coherent editable edge colors and partial alpha according to this user's full-alpha treatment.","Preview the actual sample on diagnostic and target backgrounds."],ck=["Edge edits stay inside the saved mask; protected pixels remain unchanged.","Selective soft edges preserve native readability and avoid a continuous halo."],so=refs(["s.recipe","s.edge-ramp","s.sampling","s.fixture","s.research","s.brief"]),rq=["Sample edge mask, chosen colors and representative backgrounds."],rk=["Do not transfer strict-palette quantization to this unrestricted-palette brief.","Offline edit-locality fixture does not prove perceptual quality."])

def criterion(name, title, domain, mode, condition, sources):
    add(name,"Q",nm=title,dm=sym(domain),md=sym(mode),ck=condition,wh=ref("actor"),so=refs(sources))
criterion("q.approach","Reference-grounded approach completeness","other","local","Written approach separates user constraints, measurements/visual observations, proposals and unknowns; explicitly preserves full alpha and selective AA without a fixed palette; cites actual method sources and limits; defines one representative sample and separate mechanical, visual and destination checks.",["s.brief","s.measure","s.visual","s.research"])
criterion("q.sample-mechanics","Sample raster and alpha preservation","mechanical","local","One 32x32 RGBA PNG with transparent exterior and intentionally fractional-alpha edge/material regions. Save/reopen preserves visible RGBA and alpha values. Exact RGB palette membership is unrestricted; no binary-alpha thresholding. Retain source, export, hash and alpha distribution.",["s.brief","s.measure","s.research"])
criterion("q.sample-style","Lantern identity and style","visual","visual","Inspect actual sample beside reference at 1x and 8x on light #F0E8D8, dark #18222E and checker. Handle, cap, base and warm light read as a lantern; navy structure, teal body and warm focal hierarchy retain the source's flat block style; partially transparent edges remain visible and controlled.",["s.visual","s.brief"])
criterion("q.sample-edge-mask","Selected edge mask and protected frame","mechanical","local","Retain a pre-AA raster and explicit mask for allowed AA/translucency edits. Pixel diff is confined to that mask and protected hard frame pixels remain byte-identical. Alpha/ramp values may change by authoring judgment; do not impose the source's exact counts.",["s.research","s.brief"])
criterion("q.sample-edges","Selective AA compositing appearance","visual","visual","Inspect actual post-export sample at 1x and 8x on all diagnostic backgrounds. Partial-alpha strips are localized, opaque structure remains crisp, the warm light remains distinct, and no opaque matte fringe or unplanned uniform soft outline appears. Record dark-background contrast concerns; engine rendering is separate.",["s.visual","s.research","s.brief"])
add("f.approach","F",tk=ref("t.approach"),nm="Lantern reference review and production approach",kd=sym("report"),rq=refs(["q.approach"]))
add("f.lantern","F",tk=ref("t.sample"),nm="First representative 32x32 RGBA lantern",kd=sym("sprite"),ct=ref("c.lantern-sample"),rq=refs(["q.sample-mechanics","q.sample-style","q.sample-edge-mask","q.sample-edges"]))
add("t.approach","T",nm="Review reference and prepare production approach",ow=ref("actor"),pr=ref("project"),dp=[],dc=[],kn=refs(["k.alpha-research","k.edge-research"]),st=sym("active"),ph=sym("research"),ip=refs(["x.reference","x.inspection"]),op=refs(["f.approach"]),ca=[],vr=[])
add("t.sample","T",nm="Prove proposed lantern treatment on one sample",ow=ref("actor"),pr=ref("project"),dp=refs(["t.approach"]),dc=[],kn=refs(["k.alpha-research","k.edge-research"]),st=sym("open"),ph=sym("sample"),ip=refs(["x.reference"]),op=refs(["f.lantern"]),ca=[],vr=[])
add("handoff","N",wh=ref("actor"),fo=refs(["t.approach","t.sample","i.scope","i.engine","i.display","s.research"]),nx=refs(["t.sample"]),bl=[],rv=1)
project = next(row["fields"] for row in rows if row["id"]=="project")
project["in"]=refs(choices)
project["sc"]=refs(["s.brief","s.image","s.measure","s.visual","s.research"])
adapter = root/"review/plan.adapter.json"
adapter.write_text(json.dumps(doc,indent=2)+"\n",encoding="utf-8")
print(cli("encode",str(adapter),"--out","review/plan.candidate.px"))
