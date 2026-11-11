import json, hashlib
from pathlib import Path
root = Path.cwd()
out = root / 'work/plar-coverage'
def read(name):
    return json.loads((out / name).read_text(encoding='utf-8-sig'))
def payload(name):
    r = read(name)
    return r.get('structuredContent') or json.loads(r['content'][0]['text'])
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
initial = payload('initial-read.json')['hash']
history = [p for p in (root/'.pixl/plar-history').rglob('*') if p.is_file() and digest(p)==initial]
assert history, 'Original PLAR bytes absent from history'
old = json.loads(history[0].read_text(encoding='utf-8-sig'))
new = json.loads((root/'plar.txt').read_text(encoding='utf-8-sig'))
assert new['project']==old['project']
assert new['sources'][:len(old['sources'])]==old['sources']
checks=[]
for id in ['queue.start','queue.working','queue.ready','queue.retry']:
    b=payload('parent-before-'+id+'.json')
    a=payload('parent-selection-'+id+'.json')
    assert b['production']==a['production']
    if id!='queue.start':
        assert b['asset']==a['asset'] and b['requirements_hash']==a['requirements_hash']
    else:
        assert b['requirements_hash']!=a['requirements_hash']
        for key in b['asset']:
            if key not in ['consumers','requirements']:
                assert b['asset'][key]==a['asset'][key], key
        for key in ['consumers','requirements']:
            assert a['asset'][key][:len(b['asset'][key])]==b['asset'][key]
    checks.append({'id':id,'prior_requirements_hash':b['requirements_hash'],'current_requirements_hash':a['requirements_hash'],'row_unchanged':b['asset']==a['asset'],'production_unchanged':True})
baseline=read('parent-preservation-baseline.json')
for row in baseline:
    assert digest(root/row['path'])==row['sha256'], row['path']
report={'checks':checks,'original_history':{'path':history[0].relative_to(root).as_posix(),'sha256':initial},'preserved_file_count':len(baseline),'original_source_bindings_unchanged':True,'limits':['Preservation snapshot was captured during this evaluation before allocation save; no rendered or runtime acceptance asserted.']}
(out/'parent-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
specialist=read('SPECIALIST-RESULT.json')
for key in ['initial_read','update_save','final_document','coverage','source_map']:
    ref=specialist[key]
    assert digest(root/ref['path'])==ref['sha256'], key
assert (root/'plar.txt').read_bytes()==(out/'final-document.json').read_bytes()
def ref(name):
    p=out/name
    return {'path':p.relative_to(root).as_posix(),'sha256':digest(p)}
caller={
    'native_child':{'agent_type':'pixl','canonical_task':'/root/allocation','fork_turns':'all'},
    **{key:specialist[key] for key in ['coverage','source_map','initial_read','update_save']},
    'parent_refresh':ref('parent-refresh.json'),
    'specialist_result':ref('SPECIALIST-RESULT.json'),
    'parent_selections':{id:ref('parent-selection-'+id+'.json') for id in ['queue.start','queue.working','queue.ready','queue.retry']},
    'verification':ref('parent-verification.json'),
    'independent_source_reads':[ref('parent-source-0.json'),ref('parent-source-1.json')],
    'scope':'Completed CF-06 allocation/update with one native PIXL specialist. Independently inspected both added modules and consumed all specialist reports. Only queue.start selected requirements identity changed; unrelated rows and selected identities, all production/evidence, original source hashes and original PLAR history bytes preserved.',
    'limits':specialist['limits']+['Conservative shared-file drift affects all four roles in the public impact report; this is separate from the added-consumer declaration and does not order regeneration.','No source allocation establishes rendered/artistic acceptance.'],
    'next_action':'Allocation evaluation complete. Preserve Start and retained historical production. No production handoff, regeneration or job action required by this assignment.'
}
(out/'CALLER-RESULT.json').write_text(json.dumps(caller,indent=2)+'\n',encoding='utf-8')
