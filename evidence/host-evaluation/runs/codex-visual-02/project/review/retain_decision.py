from pathlib import Path
from datetime import datetime, timezone
import sys, json, hashlib

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.agents/skills/pixl-kit/runtime'))
from pixl.codec import parse, Record, Ref, Symbol, encode, digest, record_hash
from pixl.graph import validate, proof_scope

def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

doc=parse((ROOT/'.pixl/state.px').read_bytes())
assert doc.revision==1
expected=digest(doc)
doc.revision+=1
at=datetime.now(timezone.utc).isoformat()

def rr(*ids):
    return [Ref(i) for i in ids]

def add(id,kind,**fields):
    assert id not in doc.records
    doc.records[id]=Record(id,kind,fields)

def artifact(id,name,path,kind='report',**fields):
    add(id,'X',nm=name,ur=path,dg=sha(path),kd=Symbol(kind),**fields)

artifact('x.candidate','Supplied candidate; retained rejected attempt','review/candidate-snapshot.png','sprite',ct=Ref('c.robot'),of=Ref('f.sample'),mt={'origin':'User-supplied candidate.png; byte-identical local snapshot; provider/job identity unspecified'})
artifact('x.reference-snapshot','Retained agreed reference bytes','review/reference-snapshot.png','reference')
artifact('x.comparison','Native and 6x diagnostic comparison','review/comparison.png','reference')
artifact('x.reference-zoom','Reference at 16x nearest-neighbor zoom','review/reference-16x.png','reference')
artifact('x.candidate-zoom','Candidate at 16x nearest-neighbor zoom','review/candidate-16x.png','reference')
artifact('x.difference','Exact landmark pixel differences','review/difference.json')
artifact('x.decision-report','Baseline decision and correction handoff','review/decision.md')

add('d.baseline','D',wh=Ref('actor'),wt='Reject candidate.png as the robot-family baseline; retain reference.png as the agreed identity and require one corrected sample before family expansion.',wr=rr('x.candidate','x.reference','x.reference-snapshot','x.comparison','x.reference-zoom','x.candidate-zoom','x.difference','x.decision-report','q.mechanical','q.silhouette','q.face','k.robot-identity'),wy='The measured 32x32/palette/alpha success does not preserve identity: visual inspection finds the left prong and right eye missing. The executed reference/candidate comparison fails the saved silhouette and face criteria.',rs=rr('s.brief','s.reference','s.observed','s.research','s.reject-features'),pc=rr('e.visual'))

def bindings(seeds):
    return [{'rf':Ref(id),'dg':record_hash(doc.records[id])} for id in sorted(proof_scope(doc,seeds))]

add('e.mechanical','E',nm='Executed PIXL image constraints: pass',ur='review/mechanical.json',dg=sha('review/mechanical.json'),rs=Symbol('pass'),md=Symbol('local'),at=at,bs=bindings(['x.candidate','q.mechanical']))

visual={
    'reviewer':'PIXL acting agent', 'observed_at':at,
    'method':'silhouette-readability applied to the actual supplied robot reference/candidate',
    'plan_revision':1,'plan_hash':expected,
    'inspected':[{ 'path':p,'sha256':sha(p)} for p in ['reference.png','candidate.png','review/reference-16x.png','review/candidate-16x.png','review/comparison.png']],
    'executed_proof':'Viewed both original 32x32 images, 16x nearest-neighbor enlargements, and a native/6x comparison sheet with light/dark/busy backgrounds and flat alpha masks.',
    'q.silhouette':{'result':'fail','observation':'The left upright prong is absent. The paired-prong silhouette and bounded upper gap from the reference are lost; only the right prong remains. This is visible at native size and in the masks.'},
    'q.face':{'result':'fail','observation':'The right cream eye is absent and replaced by teal. Only the left eye remains. The broad teal panel, dark frame and remaining flat regions are clean, but the paired-eye identity fails.'},
    'pixel_corroboration':json.loads((ROOT/'review/difference.json').read_text(encoding='utf-8')),
    'decision':'Reject baseline promotion; revise one sample to restore the missing left prong and right eye, then repeat all saved criteria before family expansion.',
    'limits':'Diagnostic backgrounds only; no target engine, live generation, animation or family-member continuity acceptance. Bundled key fixture evidence is not reused.',
    'bindings':[{'id':b['rf'].id,'sha256':b['dg']} for b in bindings(['d.baseline'])]
}
(ROOT/'review/visual.json').write_text(json.dumps(visual,indent=2)+'\n',encoding='utf-8')
add('e.visual','E',nm='Executed robot identity comparison: failed landmarks',ur='review/visual.json',dg=sha('review/visual.json'),rs=Symbol('fail'),md=Symbol('visual'),at=at,bs=bindings(['d.baseline']))

verdicts=[]
for suffix,status,evidence,why in [
    ('mechanical','pass','e.mechanical','PIXL asset-check confirms one 32x32 frame and zero out-of-palette visible colors; binary alpha passes as an additional measurement.'),
    ('silhouette','fail','e.visual','Missing left prong at x=7..10, y=3..8 changes the paired-prong reference silhouette to one prong.'),
    ('face','fail','e.visual','Missing right eye at x=18..20, y=14..17 leaves a one-eyed face instead of the reference paired eyes.')]:
    id='v.'+suffix
    add(id,'V',tk=Ref('t.sample'),rq=Ref('q.'+suffix),xr=Ref('x.candidate'),st=Symbol(status),wh=Ref('actor'),wy=why,at=at,ev=rr(evidence))
    verdicts.append(Ref(id))

doc.records['t.sample'].fields.update(st=Symbol('blocked'),ca=rr('x.candidate'),vr=verdicts,dc=rr('d.baseline'))
add('t.revise','T',nm='Restore the left prong and right eye in one new sample, then rerun baseline review',ow=Ref('actor'),pr=Ref('project'),dp=[],dc=rr('d.baseline'),kn=rr('k.robot-identity'),st=Symbol('open'),ph=Symbol('sample'),ip=rr('x.reference','x.candidate'),op=rr('f.revised'),ca=[],vr=[])
add('f.revised','F',tk=Ref('t.revise'),nm='One corrected robot sample, suggested filename candidate-v2.png',kd=Symbol('sprite'),rq=rr('q.mechanical','q.silhouette','q.face'),ct=Ref('c.robot'))
doc.records['n.handoff'].fields.update(fo=rr('d.baseline','t.sample','t.revise','x.decision-report'),nx=rr('t.revise'),bl=rr('t.sample'),rv=doc.revision)
validate(doc,ROOT)
(ROOT/'review/evaluated.px').write_bytes(encode(doc))
print(json.dumps({'expected':expected,'candidate':'review/evaluated.px','revision':doc.revision,'decision':'reject baseline','next':'t.revise'}))
