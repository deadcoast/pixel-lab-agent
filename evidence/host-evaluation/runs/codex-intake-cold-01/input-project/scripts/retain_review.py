"""Retain the actual review and complete only reference/research tasks."""
from begin_project import ROOT, STORE, cli, dump, digest, ref, refs, sym, publish
from datetime import datetime, timezone
import json

doc=json.loads(cli('decode',STORE/'state.px'))
assert doc['revision']==1, 'Review retention expects the saved plan at revision 1.'
doc['revision']=2
records=doc['records']
def add(id_,kind,**fields): records.append({'id':id_,'kind':kind,'fields':fields})
def get(id_): return next(r['fields'] for r in records if r['id']==id_)
def artifact(id_,name,path,kind,output=None,**metadata):
    fields=dict(nm=name,ur=path,dg=digest(path),kd=sym(kind),mt=metadata)
    if output: fields['of']=ref(output)
    add(id_,'X',**fields)
def source(id_,path): add(id_,'S',ur=path,dg=digest(path),ln=[],at='2026-09-11',au=sym('local'))

now=datetime.now(timezone.utc).isoformat()
source('s.measurements','evidence/reference-measurements.json')
source('s.visual_notes','docs/reference-analysis.md')
source('s.provider','evidence/provider-discovery.json')
new_choices=[
 ('i.observed_canvas','reference_canvas',[32,32],'Both supplied canvases were measured. This is not the output dimension choice.',('s.measurements',)),
 ('i.observed_alpha','reference_alpha','binary in both inputs','Both images have zero fractional-alpha pixels; output alpha remains unresolved.',('s.measurements',)),
 ('i.observed_palette','reference_colors',['#25354A','#56B5BC','#F4DDA2'],'A contains all three colors; B contains turquoise and pale gold only. No final palette limit is adopted.',('s.measurements',)),
 ('i.observed_forms','reference_forms','rectangular turquoise body, two upper projections and two pale rectangular face marks','Native and 8x visual inspection; the inputs do not establish a side-facing role sprite.',('s.visual_notes','s.reference_a','s.reference_b')),
 ('i.provider','provider_availability','local PIXL operations only; no PixelLab generation or polling tool exposed','Observed session tools; no request or job was created. Re-discover tools in the next session.',('s.provider',)),
]
for id_,key,value,why,sources in new_choices:
    add(id_,'I',pr=ref('project'),wh=ref('actor'),ky=key,st=sym('observed'),vl=value,so=refs(*sources),wy=why)
    get('project')['in'].append(ref(id_))

artifact('x.measurements','Source measurements','evidence/reference-measurements.json','report',inputs=refs('x.reference_a','x.reference_b'))
artifact('x.comparison','Native and 8x inspection board','evidence/reference-comparison.png','reference',inputs=refs('x.reference_a','x.reference_b'),origin='local reference inspection; no generated sprites')
artifact('x.viewer','Offline reference comparison viewer','reference-review.html','code',inputs=refs('x.reference_a','x.reference_b'),browser_interaction_verified=False)
artifact('x.slices','Exact retrieved method citations','evidence/research/exact-source-slices.json','report',sources=refs('s.clusters','s.motion','s.edges','s.archive'))
artifact('x.silhouette_context','Installed silhouette method context','evidence/research/silhouette-context.px','report',origin='Retrieved PX1 library context, not project state or project acceptance')
artifact('x.edge_context','Installed edge method context','evidence/research/edge-context.px','report',origin='Retrieved PX1 library context, not project state or project acceptance')
artifact('x.silhouette_method','Silhouette method description','evidence/research/silhouette-method.json','report')
artifact('x.edge_method','Edge method description','evidence/research/edge-method.json','report')
artifact('x.provider','Observed generation capability boundary','evidence/provider-discovery.json','report')
artifact('x.analysis','Completed reference inspection report','docs/reference-analysis.md','report','f.analysis',inputs=refs('x.reference_a','x.reference_b','x.measurements','x.comparison','x.viewer'))
artifact('x.research','Completed method applicability report','docs/method-research.md','report','f.research',sources=refs('x.slices','x.silhouette_context','x.edge_context','x.silhouette_method','x.edge_method','k.silhouette_candidate','k.edge_candidate','x.provider'))
artifact('x.handoff','Project continuation guide','START-HERE.md','report',origin='Human-readable handoff; state.px remains authority')
artifact('x.resume','Read-only resumption commands','scripts/resume.ps1','code')

get('t.inspect')['ca']=refs('x.analysis')
get('t.research')['ca']=refs('x.research')
get('n.handoff').update(fo=refs('x.handoff','x.analysis','x.research','x.provider','i.canvas','i.outline','i.engine','f.scout','f.medic','f.delivery'),nx=refs('t.style'),bl=refs('t.style','t.scout','t.medic','t.delivery'),rv=2)

# Use actual runtime-provided record hashes for semantic evidence bindings.
dump('.pixl/adapters/r2-review-unbound.json',doc)
unbound=ROOT/'.pixl/candidates/r2-review-unbound.px'
cli('encode',ROOT/'.pixl/adapters/r2-review-unbound.json','--out',unbound)
checked=json.loads(cli('validate',unbound,'--root',ROOT))
hashes=checked['record_hashes']
semantic={'A','S','R','C','K','D','X','I','F','Q'}
by_id={r['id']:r for r in records}
def referenced(value):
    if isinstance(value,dict):
        if '$ref' in value: yield value['$ref']
        else:
            for child in value.values(): yield from referenced(child)
    elif isinstance(value,list):
        for child in value: yield from referenced(child)
def bindings(*ids):
    seen=set()
    def walk(id_):
        if id_ in seen or by_id[id_]['kind'] not in semantic: return
        seen.add(id_)
        for child in referenced(by_id[id_]['fields']): walk(child)
    for id_ in ids: walk(id_)
    return [{'rf':ref(id_),'dg':hashes[id_]} for id_ in sorted(seen)]

reviews=[
 ('numbers','t.inspect','x.analysis','q.analysis_numbers','local','evidence/review-reference-mechanics.json',{
  'observation':'PIXL asset-check measured both original source snapshots; supplemental Pillow comparison measured identical alpha masks and 180 dark-to-turquoise replacements. The report agrees with the retained numerical output and keeps final output choices unresolved.',
  'files':['reference.png','reference-b.png','evidence/reference-measurements.json','docs/reference-analysis.md'],
  'limits':'A mechanical pass applies to reference analysis only. No final sprite properties, visual quality or engine import are certified.'}),
 ('visual','t.inspect','x.analysis','q.analysis_look','visual','evidence/review-reference-visual.json',{
  'observation':'The acting assistant opened both original 32x32 images via view_image, then opened the actual retained 800x416 comparison containing native and 8x nearest-neighbor images. Both have a rectangular body, two tall upper projections with a notch and two pale rectangular facial marks. A has dark side/bottom contours and dark upper projections; B has turquoise edges. Neither supplies equipment or a clearly side-facing scout/medic silhouette. The report separates these observations from proposed equipment designs.',
  'files':['reference.png','reference-b.png','evidence/reference-comparison.png','docs/reference-analysis.md'],
  'limits':'Only supplied references and the light-background board were visually inspected. Browser controls, game backgrounds, generated characters and engine import are unverified.'}),
 ('research','t.research','x.research','q.research','local','evidence/review-method-research.json',{
  'observation':'The acting assistant read actual method descriptions, both complete compiled context packets, four hash-verified source slices, and the two applicable bundled fixture limitations. The retained report names methods, source hashes/ranges, quotes, missing prerequisites, limited source transfer and a future scout proof. Source material does not select a winning outline.',
  'files':['docs/method-research.md','evidence/research/exact-source-slices.json','evidence/research/silhouette-context.px','evidence/research/edge-context.px'],
  'limits':'This passes source-grounded research completeness only. No project method proof, provider execution, outline adoption or character quality is claimed.'})
]
for suffix,task,candidate,criterion,mode,path,observation in reviews:
    observation.update(observed_at=now,outcome='pass',mode=mode,criterion=criterion,reviewer='PIXL acting assistant',file_sha256={p:digest(p) for p in observation['files']})
    dump(path,observation)
    eid='e.review_'+suffix
    vid='v.review_'+suffix
    add(eid,'E',nm='Retained '+suffix+' review',ur=path,dg=digest(path),rs=sym('pass'),md=sym(mode),at=now,bs=bindings(candidate,criterion))
    add(vid,'V',tk=ref(task),rq=ref(criterion),xr=ref(candidate),st=sym('pass'),wh=ref('actor'),wy=observation['observation'],at=now,ev=refs(eid))
    get(task)['vr'].append(ref(vid))
get('t.inspect')['st']=sym('done')
get('t.research')['st']=sym('done')
publish(doc,'r2-reviewed-intake')
