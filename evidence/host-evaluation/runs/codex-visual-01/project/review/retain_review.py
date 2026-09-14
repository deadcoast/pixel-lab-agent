"""Prepare a result revision with actual review evidence and a resumable next task."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'.agents/skills/pixl-kit/runtime'))
from pixl.codec import parse, Record, Ref, Symbol, encode, record_hash, to_data
from pixl.graph import proof_scope, validate

def sha(path): return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def write(path,text): (ROOT/path).write_text(text,encoding='utf-8')
def dump(path,value): write(path,json.dumps(value,indent=2)+'\n')

at=datetime.now(timezone.utc).isoformat()
(ROOT/'review/candidates').mkdir(exist_ok=True)
shutil.copyfile(ROOT/'candidate.png',ROOT/'review/candidates/candidate-v1.png')
assert sha('candidate.png')==sha('review/candidates/candidate-v1.png')
observations={
    'reviewer':'PIXL acting agent', 'at':at,
    'question':'Can candidate.png become the family baseline for the agreed reference.png identity?',
    'artifacts':{p:sha(p) for p in ['reference.png','candidate.png','review/candidates/candidate-v1.png','review/comparison.png','review/pixel-diff.json','review/pixel-observations.json']},
    'inspection':'Viewed both actual images at native 32x32, comparison board at original resolution with 12x nearest colored views and 8x alpha masks, and native sprites on light, dark and synthetic busy grounds.',
    'identity_verdict':'fail',
    'findings':[
        'Viewer-left antenna is absent: the reference dark block at inclusive x=7..10, y=3..8 is transparent in the candidate. The mask loses one of the two prongs and the bounded U-shaped top gap.',
        'Viewer-right eye is absent: the reference pale block at inclusive x=18..20, y=14..17 is cyan in the candidate. The face now has one pale eye instead of the agreed pair.',
        'The losses are apparent at native size and enlarged, across the diagnostic grounds. The candidate reads as a one-pronged, one-eyed variation; no such identity change was authorized.',
        'The surviving body proportions, dark enclosing frame, flat cyan interior and remaining pale eye are clean broad clusters. No scattered accent noise, extra shading colors or resampling blur is visible. Color-role and cluster-quality criterion passes; missing landmark completeness fails identity separately.',
        'The two sprites have the same visible bounding box and one opaque connected component. These measurements do not capture the missing landmarks.'
    ],
    'cluster_verdict':'pass',
    'coordinate_convention':'zero-based x,y; origin top-left; inclusive ranges',
    'decision':'Reject candidate-v1 as a family baseline; reference.png remains the identity authority.',
    'next_step':'Restore the left antenna and right eye in a separate candidate-v2.png using the reference placements and colors; register a new X for f.revised and run all four criteria again before any family production.',
    'limitations':['Diagnostic grounds are synthetic; actual game-background readability is unverified.','No engine, animation, direction family or final display route was supplied or tested. These are not additional gates for this static identity rejection.','The bundled key fixture is method context only, not this candidate visual evidence.']
}
dump('review/visual.json',observations)
write('REVIEW.md','''# Robot baseline review

**Decision: candidate.png is not ready to become the robot-family baseline.** The agreed identity remains reference.png.

| Check | Result | Evidence |
| --- | --- | --- |
| Canvas | Pass | One 32 × 32 frame |
| Reference palette | Pass | Three visible colors; no out-of-palette pixels |
| Identity and silhouette | **Fail** | Missing viewer-left antenna and viewer-right eye |
| Color roles and cluster quality | Pass | Remaining frame, cyan fill and pale eye retain clean flat blocks; missing landmark completeness is the identity failure above |

The reference has two top prongs and two pale eyes. The candidate has one of each. This changes both the silhouette and facial identity at native size. Equal dimensions, palette, bounding box and connected-component count do not make it a suitable family baseline.

[Open the native/enlarged comparison](review/comparison.png). Both actual images were inspected at native size and integer zoom, including alpha silhouettes and diagnostic light, dark and busy backgrounds.

**Next step:** create a separate `candidate-v2.png`, restoring the dark left antenna at x=7–10, y=3–8 and pale right eye at x=18–20, y=14–17 from the reference (zero-based coordinates, inclusive). Recheck all four criteria on the new candidate before extending the family. This review does not perform that edit.

PIXL state is [.pixl/state.px](.pixl/state.px). The original rejected candidate is retained byte-for-byte at [review/candidates/candidate-v1.png](review/candidates/candidate-v1.png). `d.baseline` retains the evidence-backed rejection; `t.sample` stays blocked by its visual failure; `t.revise` is the next open sample task, with planned output `f.revised`. No baseline has been approved for family production.

For resumption, run PIXL `workflow`, `family` and `jobs` on `.pixl/state.px`, then `context` focused on `t.revise`. Retain v1 and its verdicts, register v2 as a new candidate for `f.revised`, and evaluate it with its own evidence. Task completion requires all declared criteria to pass.

Detailed evidence: [mechanical measurements](review/mechanical.json), [visual observations](review/visual.json), [exact changed regions](review/pixel-diff.json), and [source applicability](review/method-applicability.md). Required criteria were published in revision 1 before this evaluation. Review results and the next task are retained in revision 2 using expected-hash publication.

Engine import, actual game backgrounds and final display scale were not supplied or tested. This is a static identity decision; it establishes no destination-engine acceptance. No generation request was made.
''')

doc=parse((ROOT/'.pixl/state.px').read_bytes()); doc.revision+=1
def add(id,kind,**fields): doc.records[id]=Record(id,kind,fields)
R=Ref; Y=Symbol
add('x.candidate-v1','X',nm='Rejected supplied robot candidate v1',ur='review/candidates/candidate-v1.png',dg=sha('review/candidates/candidate-v1.png'),kd=Y('sprite'),ct=R('c.robot'),of=R('f.sample'),mt={'origin':'User-supplied candidate.png; retained byte snapshot','original_sha256':sha('candidate.png'),'provider_job':'not supplied'})
add('x.comparison','X',nm='Inspected native and integer-zoom comparison',ur='review/comparison.png',dg=sha('review/comparison.png'),kd=Y('reference'))
add('x.diff','X',nm='Measured changed pixel regions',ur='review/pixel-diff.json',dg=sha('review/pixel-diff.json'),kd=Y('report'))
add('x.review','X',nm='Baseline decision and next-step handoff',ur='REVIEW.md',dg=sha('REVIEW.md'),kd=Y('report'))
add('d.baseline','D',wh=R('actor'),wt='Reject candidate-v1 as a robot-family baseline; preserve reference identity and revise the missing left antenna and right eye.',wr=[R(i) for i in ['x.candidate-v1','x.reference','x.comparison','x.diff','x.review','k.robot-review']],wy='Native and enlarged inspection shows a missing silhouette prong and a missing facial landmark. Size and palette pass but cannot establish identity. Save a new candidate and review it before family expansion.',rs=[R(s) for s in ['s.brief','s.reference','s.method','s.deep.features']],pc=[R('e.decision')])

for id,outcome,mode,path,seeds in [
    ('e.mechanical','pass','local','review/mechanical.json',['x.candidate-v1','q.size','q.palette']),
    ('e.identity','fail','visual','review/visual.json',['x.candidate-v1','x.reference','x.comparison','x.diff','q.identity']),
    ('e.clusters','pass','visual','review/visual.json',['x.candidate-v1','x.reference','x.comparison','q.clusters']),
    ('e.decision','fail','visual','review/visual.json',['d.baseline'])]:
    bindings=[{'rf':R(i),'dg':record_hash(doc.records[i])} for i in sorted(proof_scope(doc,seeds))]
    add(id,'E',nm=id,ur=path,dg=sha(path),rs=Y(outcome),md=Y(mode),at=at,bs=bindings)

verdicts=[]
for suffix,status,evidence,reason in [
    ('size','pass','e.mechanical','PIXL measured one 32x32 frame.'),
    ('palette','pass','e.mechanical','All visible pixels use the three reference colors; zero outside-palette pixels.'),
    ('identity','fail','e.identity','Missing viewer-left antenna at x7..10/y3..8 and viewer-right eye at x18..20/y14..17; native and enlarged views show a different silhouette and face.'),
    ('clusters','pass','e.clusters','Surviving dark frame/prong, cyan face and pale eye use clean broad flat clusters with no noise or blur. Missing landmark completeness fails q.identity separately.')]:
    id='v.'+suffix; verdicts.append(R(id))
    add(id,'V',tk=R('t.sample'),rq=R('q.'+suffix),xr=R('x.candidate-v1'),st=Y(status),wh=R('actor'),wy=reason,at=at,ev=[R(evidence)])
doc.records['t.sample'].fields.update(st=Y('blocked'),ca=[R('x.candidate-v1')],vr=verdicts)
add('f.revised','F',tk=R('t.revise'),nm='Revised robot with restored left antenna and right eye',kd=Y('sprite'),ct=R('c.robot'),rq=[R(q) for q in ['q.size','q.palette','q.identity','q.clusters']])
add('t.revise','T',nm='Restore both missing landmarks in candidate-v2 and re-review before family expansion',ow=R('actor'),pr=R('project'),dp=[],dc=[R('d.baseline')],kn=[R('k.robot-review')],st=Y('open'),ph=Y('sample'),ip=[R('x.reference'),R('x.candidate-v1'),R('x.review')],op=[R('f.revised')],ca=[],vr=[])
add('n.handoff','N',wh=R('actor'),fo=[R(i) for i in ['d.baseline','x.review','x.candidate-v1','v.identity','f.revised']],nx=[R('t.revise')],bl=[R('t.sample')],rv=doc.revision)
validate(doc,ROOT)
(ROOT/'review/result.px').write_bytes(encode(doc))
dump('review/result.json',{'format':doc.format,'revision':doc.revision,'records':[{'id':r.id,'kind':r.kind,'fields':to_data(r.fields)} for r in doc.records.values()]})
print('Result revision validated; ready for expected-hash commit.')
