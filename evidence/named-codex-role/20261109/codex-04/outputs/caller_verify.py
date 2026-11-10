import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'work/named-role'
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def check_named(obj, trail=''):
    checks=[]
    if isinstance(obj,dict):
        if isinstance(obj.get('path'),str) and isinstance(obj.get('sha256'),str):
            p=Path(obj['path'])
            if (ROOT/p).is_file():
                actual=sha(p); assert actual==obj['sha256'], (trail,str(p),actual,obj['sha256'])
                checks.append({'path':str(p),'sha256':actual})
        for k,v in obj.items(): checks.extend(check_named(v,trail+'/'+k))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): checks.extend(check_named(v,trail+'/'+str(i)))
    return checks
def baseline():
    rows=read('work/named-role/CALLER-BASELINE.json')
    for r in rows: assert sha(r['path'])==r['sha256'], r['path']
    return len(rows)
if __name__=='__main__':
    r=read('work/named-role/SPECIALIST-ROUND1.json')
    checks=check_named(r)
    s=read('work/named-role/CALLER-SELECTED-ROUND1.json')
    c=read('work/named-role/CALLER-CONTEXT-ROUND1.json')
    assert sha('work/named-role/round1-candidate-context.json')==sha('work/named-role/CALLER-CONTEXT-ROUND1.json')
    assert r['identities']['state_hash']==s['production']['continuation']['state_hash']==c['state_hash']
    assert r['identities']['requirements_hash']==s['requirements_hash']
    assert r['acceptance']['current']==c['current_acceptance']
    assert c['snapshot_acceptance']['accepted'] is False
    src=r['source']; lines=(ROOT/src['path']).read_bytes().decode('utf-8').splitlines(keepends=True)
    assert ''.join(lines[src['start']-1:src['end']])==src['literal_excerpt']
    assert sha(src['path'])==src['sha256']
    for m in c['members']:
        assert sha(m['retained_path'])==sha(m['source_path'])==m['sha256']
    a=read('work/named-role/round1-authoring.json')
    assert 'provenance-correction.plan' in json.dumps(a['plans'])
    report={'status':'verified','specialist':'/root/pixl_specialist','round1_report_sha256':sha('work/named-role/SPECIALIST-ROUND1.json'),'named_hash_checks':checks,'preexisting_files_verified':baseline(),'independent_exports':['work/named-role/CALLER-SELECTED-ROUND1.json','work/named-role/CALLER-CONTEXT-ROUND1.json'],'findings':['Selected authoring-plar.txt / queue.working generation, provenance-correction.plan and current canonical state agree.','Candidate context export is byte-identical to independent caller public export. All four retained/source member hashes verified.','BRIEF.md exact line 3 and source byte hash independently verified.','Current acceptance true and task done; immutable creation-time accepted false. Retained verdicts do not establish fresh visual or renderer observations.'],'corrections':[],'follow_up':'Replay unchanged work/export-review/identical-review.json for native.provenance.delivery.candidate.01 with review ID native.family.review.01, current canonical state guard, fresh result path; report actual reuse/publication and save public authoring-plar.txt / queue.working handoff. Carry retained-evidence limits and exact next action; no new acceptance or production publication.'}
    (OUT/'CALLER-REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'verified_hashes':len(checks),'baseline_files':report['preexisting_files_verified'],'review':'work/named-role/CALLER-REVIEW.json'}))
