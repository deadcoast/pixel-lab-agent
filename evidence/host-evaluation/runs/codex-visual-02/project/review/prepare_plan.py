from pathlib import Path
import sys, json, hashlib
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.agents/skills/pixl-kit/runtime'))
from pixl.codec import parse, Record, Ref, Symbol, encode, digest
from pixl.graph import validate

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

doc = parse((ROOT / '.pixl/state.px').read_bytes())
assert doc.revision == 0
expected = digest(doc)
doc.revision += 1

def add(id, kind, **fields):
    doc.records[id] = Record(id, kind, fields)

def rr(*ids):
    return [Ref(i) for i in ids]

def source(id, path, lines=None):
    add(id, 'S', ur=path, dg=sha(path), ln=lines or [], at='2026-09-11', au=Symbol('local'))

source('s.brief', 'review/brief.txt', [1,3])
source('s.reference', 'reference.png')
source('s.observed', 'review/reference-observations.txt', [1,6])
source('s.research', 'review/research.json')
source('s.reject-features', '.agents/skills/pixl-kit/resources/training/original-docs/PIXEL-ART-DEEP-RESEARCH.md', [857,867])
source('s.semantic-change', '.agents/skills/pixl-kit/resources/training/original-docs/PIXEL-ART-DEEP-RESEARCH.md', [1563,1573])
source('s.archive-context', '.agents/skills/pixl-kit/resources/training/original-docs/PIXEL-ART-ASSETS.md', [11,15])

im = Image.open(ROOT / 'reference.png').convert('RGBA')
palette = sorted({'#%02X%02X%02X' % p[:3] for p in im.getdata() if p[3]})
(ROOT / 'review/reference-palette.json').write_text(json.dumps(palette, indent=2)+'\n', encoding='utf-8')

choices = []
def choice(id, key, status, value, sources, reason, actor='actor'):
    choices.append(Ref(id))
    add(id, 'I', pr=Ref('project'), wh=Ref(actor), ky=key, st=Symbol(status), vl=value, so=rr(*sources), wy=reason)

choice('i.canvas','px','confirmed',[32,32],['s.brief'],'The user explicitly identifies 32 by 32 as the correct dimensions.','user')
choice('i.palette','pl','confirmed',palette,['s.brief','s.reference'],'The reference palette is the user-supplied constraint; values are extracted from visible reference pixels.','user')
choice('i.identity','identity','confirmed','reference.png is the agreed robot-family identity',['s.brief','s.reference'],'The user names reference.png as the agreed identity.','user')
choice('i.landmarks','landmarks','observed','Tall rectangular frame; two separated upright prongs and open upper gap; teal panel; two distinct horizontally aligned cream eyes; flat clean color regions.',['s.reference','s.observed'],'Observed visual landmarks provide the baseline comparison criteria.')
choice('i.view','vw','proposed',Symbol('ui'),['s.observed'],'Straight-on review representation; no game camera has been agreed.')
choice('i.sampling','sa','proposed',Symbol('nearest'),['s.observed'],'Integer nearest-neighbor zoom preserves the actual pixels for inspection.')
choice('i.alpha','al','observed',Symbol('binary'),['s.reference'],'Reference alpha is binary; retain the observed reference edge behavior in the sample contract.')
choice('i.destination','destination','unresolved',None,[],'Game engine, display scale and actual backgrounds are not supplied; no engine-ready claim is part of this baseline review.')

add('c.robot','C',nm='Reference-derived robot sample review',px=[32,32],pl=palette,vw=Symbol('ui'),sa=Symbol('nearest'),al=Symbol('binary'),li='Flat color regions in reference; no directional lighting convention inferred.',ch=rr(*[r.id for r in choices if r.id != 'i.destination']))
doc.records['project'].fields.update({'in':choices,'sc':rr('s.brief','s.reference','s.observed','s.research'),'ct':Ref('c.robot')})
add('x.reference','X',nm='Agreed robot identity',ur='reference.png',dg=sha('reference.png'),kd=Symbol('reference'))
method = json.loads((ROOT/'review/research.json').read_text(encoding='utf-8'))['method']
add('k.robot-identity','K',nm='Project application of silhouette-readability',ap=[Symbol('robot_identity')],op=method['procedure'],ck=method['checks'],rq=method['requires'],rk=method['pitfalls'],so=rr('s.research','s.reject-features','s.semantic-change','s.archive-context'))

def criterion(id, name, domain, mode, condition):
    add(id,'Q',nm=name,dm=Symbol(domain),md=Symbol(mode),ck=condition,wh=Ref('actor'),so=rr('s.brief','s.reference','s.observed','s.reject-features'))

criterion('q.mechanical','32x32 and reference palette','mechanical','local','The still candidate is 32x32 and every visible RGB color belongs to the palette extracted from reference.png. Report alpha and connectivity measurements separately; neither proves identity.')
criterion('q.silhouette','Reference silhouette and proportions','visual','visual','At native 32x32 and integer zoom, retain the reference tall rectangular body/frame, two upright separated prongs, deep open upper gap and their relative proportions. Inspect flat alpha masks and colored views on diagnostic backgrounds. Reject a different body silhouette or collapsed identity gap.')
criterion('q.face','Reference face and clean color hierarchy','visual','visual','At native 32x32 and integer zoom, retain two distinct horizontally aligned cream eyes within the broad teal panel, with simple coherent flat regions and dark frame. Reject lost/merged facial landmarks or unmotivated speckling that replaces the reference hierarchy.')
add('t.sample','T',nm='Review supplied robot sample for baseline eligibility',ow=Ref('actor'),pr=Ref('project'),dp=[],dc=[],kn=rr('k.robot-identity'),st=Symbol('active'),ph=Symbol('sample'),ip=rr('x.reference'),op=rr('f.sample'),ca=[],vr=[])
add('f.sample','F',tk=Ref('t.sample'),nm='Robot family baseline sample',kd=Symbol('sprite'),rq=rr('q.mechanical','q.silhouette','q.face'),ct=Ref('c.robot'))
add('n.handoff','N',wh=Ref('actor'),fo=rr('t.sample'),nx=rr('t.sample'),bl=[],rv=doc.revision)
validate(doc, ROOT)
(ROOT/'review/plan.px').write_bytes(encode(doc))
print(json.dumps({'expected':expected,'candidate':'review/plan.px','palette':palette,'revision':doc.revision}))
