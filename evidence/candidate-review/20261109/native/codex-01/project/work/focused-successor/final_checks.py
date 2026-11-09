from pathlib import Path
from hashlib import sha256
import json

root=Path.cwd();work=root/'work/focused-successor'
def load(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def digest(p):return sha256((root/p).read_bytes()).hexdigest()
def write(n,d):(work/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
baseline=load('work/export-review-01/baseline-hashes.json')
preserved=[];allowed=[];failures=[];prior_baseline_drift=[]
for p,entry in baseline.items():
    if not (root/p).is_file():failures.append({'path':p,'error':'missing'});continue
    row={'path':p,'before':entry['sha256'],'after':digest(p)}
    if p in ['AGENTS.md','SESSION.md'] and row['before']!=row['after']:
        row['scope']='Prior EXPORT baseline differs from current assignment instructions. Neither file was written in this turn; no initial hash was measured this turn, so baseline continuity is not claimed.'
        prior_baseline_drift.append(row)
        continue
    if p in ['authoring-plar.txt','.pixl/assets/queue.ready/state.px']:
        allowed.append(row)
    else:
        row['unchanged']=row['before']==row['after'];preserved.append(row)
        if not row['unchanged']:failures.append(row)
assert not failures,failures
before=load('.pixl/plar-history/7c6c54fb55f0cb46fb8f5707468b3776438bd62ab102beafb49c2e91e50e3b41.json')
after=load('authoring-plar.txt')
assert before['sources']==after['sources']
for old,new in zip(before['assets'],after['assets']):
    assert old['id']==new['id']
    for key in ['purpose','kind','status','consumers','production','references','depends_on']:
        assert old.get(key)==new.get(key),(old['id'],key)
    assert old['delivery']['path']==new['delivery']['path']
    for a,b in zip(old['requirements'],new['requirements']):
        if a['property']=='renderer_frame_extraction':
            assert a['authority']==b['authority']=='observation'
            assert a['sources']==b['sources']
        else:assert a==b,(old['id'],a['property'])
write('preservation-check.json',{'status':'pass for evaluated historical art/source/evidence; instruction baseline caveat retained','prior_instruction_baseline_drift':prior_baseline_drift,'baseline':'work/export-review-01/baseline-hashes.json','files':preserved,'authorized_changes':allowed,'plar_source_bindings_unchanged':True,'plar_semantic_requirements_production_links_delivery_paths_unchanged':True,'old_plar_exact_bytes':{'path':'.pixl/plar-history/7c6c54fb55f0cb46fb8f5707468b3776438bd62ab102beafb49c2e91e50e3b41.json','sha256':digest('.pixl/plar-history/7c6c54fb55f0cb46fb8f5707468b3776438bd62ab102beafb49c2e91e50e3b41.json')}})
proposal=load('work/focused-successor/specialist-proposal-r4.json')
source_findings=[]
for s in proposal['source_index']:
    p=s['path'];actual=digest(p) if (root/p).is_file() else None
    row={'id':s['id'],'path':p,'expected':s['sha256'],'actual':actual,'current':actual==s['sha256']}
    if not row['current']:
        if p=='authoring-plar.txt':row['retained_at']='.pixl/plar-history/'+s['sha256']+'.json'
        elif p=='.pixl/assets/queue.ready/state.px':
            matches=[f for f in (root/'.pixl/assets/queue.ready/history').glob('*') if f.is_file() and sha256(f.read_bytes()).hexdigest()==s['sha256']]
            row['retained_at']=matches[0].relative_to(root).as_posix() if matches else None
        else:row['historical_reference']='Prior evidence/source revision remains in original historical artifact; not asserted current.'
    source_findings.append(row)
write('source-index-validation.json',{'sources':source_findings,'scope':'Current versus historical is explicit. Historical identities never rebound to changed bytes. Source location/meaning review is recorded separately in proposal and caller comparison.'})
write('retained-failures.json',{'render-01':'24samples/~600ms insufficient for proposed >=800ms window; preserved, superseded by render-02/03','render-02':'40samples prove visible freeze/resume but preference_changes remained empty; earlier motion-check-02 pass covered sampled frame/pixel conditions only and did not establish notification/phase reset. Preserved source revision under source-revisions/r1. Corrected render-03 asserts both transition records and matrix freeze.','initial_paused_concern':'Specialist raw hidden-magenta-RGB interpretation corrected after alpha/panel viewing; no opaque matte observed, no asset modified.','public_plan':'Exact public operation rejected existing production link. No unlink, renamed asset, manual immutable intent edit, invented request or acceptance transfer.'})
newfiles=[]
for folder in ['src/queue-view-successor.ts','renderer-successor','work/focused-successor']:
    p=root/folder
    paths=[p] if p.is_file() else sorted(p.rglob('*'))
    for f in paths:
        if f.is_file() and f.name!='artifact-manifest.json' and '__pycache__' not in f.parts:
            newfiles.append({'path':f.relative_to(root).as_posix(),'sha256':sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size})
write('artifact-manifest.json',{'files':newfiles,'scope':'Exact new source, copied-art and evidence bytes; excludes this manifest itself and later final result/handoff files.'})
print(json.dumps({'preserved':len(preserved),'authorized_changed':len(allowed),'new_files':len(newfiles),'historical_sources':len([s for s in source_findings if not s['current']])}))
