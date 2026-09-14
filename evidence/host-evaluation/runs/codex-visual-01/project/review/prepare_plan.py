"""Retain reference observations and prepare the PX2 review plan; no verdicts."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / '.agents/skills/pixl-kit/runtime'))
from pixl.codec import parse, to_data

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

def write(path, text):
    (ROOT / path).write_text(text, encoding='utf-8')

write('review/brief.txt', '''User instruction retained 2026-09-11:
Use PIXL to check whether candidate.png is ready to become the baseline for the rest of the robot family. The agreed identity is reference.png. The generated sample has the right 32 by 32 dimensions and reference palette. Review it and retain a useful decision and next step in this project.
Work only in this isolated project. Do not install packages or change host settings.
Scope: review this supplied static representative sample, retain decision and next step; no family generation requested. No target engine, game background, animation, or display scale beyond the 32 by 32 source canvas is supplied.
''')
write('review/reference-observations.md', '''Reference intake observations, before candidate evaluation

Inspected reference.png at native 32 by 32 and a 12x nearest-neighbor enlargement.
The agreed identity has a compact upright rectangular cyan face/body inside a thick dark blue frame, two straight dark antenna/prongs rising from its upper left and upper right, a wide open U-shaped gap between those prongs, and two separate pale upright rectangular eyes aligned horizontally. Its surfaces use broad flat color blocks and hard square corners; there is no directional shading ramp to preserve.
The source has 3 visible RGB colors: #25354a (frame/prongs), #56b5bc (face), #f4dda2 (eyes). PIXL measures binary alpha and a single 32x32 frame. These are observations; only reference identity, canvas dimensions, and reference palette are explicitly agreed by the user.
Inspection uses native source pixels and nearest-neighbor enlargement. This is a review setup, not an engine sampling or projection agreement. The PIXL contract uses ui to represent this flat front-facing image-plane review because its view enum has no front value; it does not choose the game's camera.
''')
write('review/method-applicability.md', '''Method: silhouette-readability (installed PIXL knowledge method).
Question: does the supplied candidate retain the robot identity well enough to seed its family?
Applicable: static character, known 32x32 source scale, landmarks from reference.png. Inspect flat masks for proportions/prongs/negative space, then colored views for eyes, frame and cyan fill. A silhouette alone cannot validate facial details.
Proof for this project: compare the two actual supplied sprites at native and 12x nearest zoom, plus flat masks and colored views on light, dark and a synthetic busy background. Identity landmarks and coherent broad clusters must survive; size and palette are independent mechanical criteria. Backgrounds are diagnostic surrogates only; the actual game background and intended display scale remain unknown.
Source retrieval and exact text are retained in research.json. PIXEL-ART-DEEP-RESEARCH.md lines 857-867 support protecting identifying features and deliberate clusters. Lines 1563-1573 concern temporal semantic differences; only their distinction between silhouette/shading/detail transfers to this static review, not a motion metric. PIXEL-ART-ASSETS.md lines 11-15 concern another project's UI and support context/cohesion only; their embedded UI directions are not this project's requirements.
The installed key-silhouette-landmarks receipt only checks specified geometric landmarks and generates native/4x views. It explicitly does not establish visual recognition, background readability, or artistic acceptance. That fixture is not reused as robot acceptance evidence. The actual robot comparison is the required project proof.
''')
state = parse((ROOT / '.pixl/state.px').read_bytes())
doc = {'format': 2, 'revision': state.revision + 1, 'records': [
    {'id':r.id,'kind':r.kind,'fields':to_data(r.fields)} for r in state.records.values()]}
R=lambda x:{'$ref':x}
Y=lambda x:{'$symbol':x}
def add(id,kind,**fields):
    doc['records'].append({'id':id,'kind':kind,'fields':fields})
def source(id,path,lines=[]):
    add(id,'S',ur=path,dg=sha(path),ln=lines,at='2026-09-11',au=Y('local'))
source('s.brief','review/brief.txt',[1,4])
source('s.reference','reference.png')
source('s.observations','review/reference-observations.md')
source('s.method','review/method-applicability.md')
source('s.research','review/research.json')
source('s.deep.features','.agents/skills/pixl-kit/resources/training/original-docs/PIXEL-ART-DEEP-RESEARCH.md',[857,867])
source('s.deep.semantic','.agents/skills/pixl-kit/resources/training/original-docs/PIXEL-ART-DEEP-RESEARCH.md',[1563,1573])
source('s.assets','.agents/skills/pixl-kit/resources/training/original-docs/PIXEL-ART-ASSETS.md',[11,15])
choices=[]
def choice(id,key,status,value,sources,why,owner='actor'):
    choices.append(R(id))
    add(id,'I',pr=R('project'),wh=R(owner),ky=key,st=Y(status),vl=value,so=[R(s) for s in sources],wy=why)
palette=json.loads((ROOT/'review/reference-palette.json').read_text())
choice('i.canvas','px','confirmed',[32,32],['s.brief'],'User specifies the canvas.','user')
choice('i.palette','pl','confirmed',palette,['s.brief','s.reference'],'User requires the reference palette; exact visible colors were extracted from the reference.','user')
choice('i.identity','identity','confirmed','reference.png is the agreed robot family identity',['s.brief','s.reference'],'Compare identity landmarks, silhouette and color roles to this exact image.','user')
choice('i.alpha','al','observed',Y('binary'),['s.observations','s.reference'],'Observed reference alpha; retained as sample interpretation, not a new user mandate.')
choice('i.sampling','sa','proposed',Y('nearest'),['s.observations'],'Use native pixels and integer nearest zoom for review; engine sampling remains unspecified.')
choice('i.view','vw','observed',Y('ui'),['s.observations'],'Flat front-facing image-plane inspection; ui is the available contract enum, not a game-camera decision.')
choice('i.light','li','observed','Flat broad color blocks; no directional shading ramp',['s.observations','s.reference'],'Preserve the reference color roles and edge treatment.')
choice('i.destination','destination','unresolved',None,['s.brief'],'Target engine, game backgrounds and final display scale are absent; this review determines baseline identity only.')
add('c.robot','C',nm='Reference-grounded robot sample review',px=[32,32],pl=palette,vw=Y('ui'),sa=Y('nearest'),al=Y('binary'),li='Flat broad color blocks; no directional shading ramp',ch=choices[:-1])
add('x.reference','X',nm='Agreed robot identity',ur='reference.png',dg=sha('reference.png'),kd=Y('reference'))
add('k.robot-review','K',nm='Project application of silhouette-readability',ap=[Y('characters')],rq=['Known reference identity and 32x32 canvas; actual game backgrounds unknown'],op=['Compare actual source masks and colored sprites at native scale and 12x nearest zoom.','Inspect prongs and their gap, body proportions, paired eyes, color roles and deliberate clusters.'],ck=['Reference identity landmarks remain distinct and coherent.','Mechanical passes are recorded separately from visual judgment.'],rk=['Surrogate backgrounds do not establish game-background acceptance.','Silhouette and component counts cannot establish facial identity or artistic quality.'],so=[R(s) for s in ['s.method','s.research','s.deep.features','s.deep.semantic','s.assets']])
for id,name,domain,mode,condition,sources in [
    ('q.size','32 by 32 canvas','mechanical','local','The supplied sample has exactly one 32x32 frame.',['s.brief']),
    ('q.palette','Reference palette','mechanical','local','Every visible pixel uses the reference RGB palette #25354a, #56b5bc, #f4dda2.',['s.brief','s.reference']),
    ('q.identity','Robot identity and silhouette','visual','visual','At native 32x32 and integer zoom, preserve the compact upright rectangular body, two straight top prongs with an open U-shaped gap, and two separated pale eyes at a common height inside the cyan face; retain relative proportions and placement recognizable as reference.png.',['s.brief','s.reference','s.observations','s.method']),
    ('q.clusters','Reference color roles and cluster readability','visual','visual','At native scale and integer zoom, retain a coherent cyan interior, dark enclosing frame/prongs, and pale eyes with broad flat deliberate color blocks; no scattered accents or competing detail that breaks facial readability or changes the reference character. Inspect color and mask views, with diagnostic backgrounds.',['s.brief','s.reference','s.observations','s.method'])]:
    add(id,'Q',nm=name,dm=Y(domain),md=Y(mode),ck=condition,wh=R('actor'),so=[R(s) for s in sources])
add('f.sample','F',tk=R('t.sample'),nm='Robot representative sample eligible for family baseline',kd=Y('sprite'),ct=R('c.robot'),rq=[R(q) for q in ['q.size','q.palette','q.identity','q.clusters']])
add('t.sample','T',nm='Review and qualify the robot representative sample',ow=R('actor'),pr=R('project'),dp=[],dc=[],kn=[R('k.robot-review')],st=Y('active'),ph=Y('sample'),ip=[R('x.reference')],op=[R('f.sample')],ca=[],vr=[])
for r in doc['records']:
    if r['id']=='project':
        r['fields'].update({'sc':[R('s.brief'),R('s.reference')],'in':choices,'ct':R('c.robot')})
write('review/plan.json',json.dumps(doc,indent=2)+'\n')
print('Prepared review/plan.json; candidate evaluation has not started.')
