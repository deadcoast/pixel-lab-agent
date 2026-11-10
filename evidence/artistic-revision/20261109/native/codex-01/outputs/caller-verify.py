"""Independent caller checks; reads specialist artifacts without modifying production."""
import json, hashlib, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'work/artistic-revision'
def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def save(name, value):
    (OUT/name).write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')
def decode(path):
    p = subprocess.run([sys.executable, str(ROOT/'.agents/skills/artistic-revision-kit/scripts/pixl.py'), 'decode', str(ROOT/path)], capture_output=True, text=True, check=True)
    return json.loads(p.stdout)

def verify():
    before=read('work/artistic-revision/caller-preservation-before.json')
    altered=[p for p,h in before.items() if not (ROOT/p).is_file() or digest(p)!=h]
    baseline=read('work/artistic-revision/caller-baseline-decoded.json')
    current=decode('.pixl/assets/queue.ready/state.px')
    old={r['id']:r for r in baseline['records']}
    new={r['id']:r for r in current['records']}
    changes=[]
    for id,r in old.items():
        if id not in new: changes.append({'id':id,'removed':True})
        elif new[id]!=r:
            fields={k:{'before':r['fields'].get(k),'after':new[id]['fields'].get(k)} for k in set(r['fields'])|set(new[id]['fields']) if r['fields'].get(k)!=new[id]['fields'].get(k)}
            changes.append({'id':id,'kind':r['kind'],'fields':fields})
    mapping=read('work/artistic-revision/adopted-criteria.json')
    originals=read('work/artistic-revision/caller-context-original.json')['criteria']
    expected_original={r['id']:r['record_sha256'] for r in originals}
    actual_original={r['id']:r['record_sha256'] for r in mapping['original_20']}
    corrected=read('work/continuation/SPECIALIST-ROUND2.json')['corrected_criteria']
    expected={r['id']:r for r in corrected}
    rows=[]
    for m in mapping['corrected_29']:
        r=expected[m['source_id']]
        text=r['original_check'] if r['corrected_check']=='(unchanged)' else r['corrected_check']
        relocated=text.replace('src/queue-view-successor.ts','src/queue-view-artistic.ts').replace('renderer-successor/','renderer-artistic/')
        q=new.get(m['record_id'])
        rows.append({'source_id':m['source_id'],'record_id':m['record_id'],
            'literal_matches_permitted_relocation':m['check']==relocated,
            'actual_Q_matches_mapping':bool(q and q['kind']=='Q' and q['fields']['ck']==m['check']),
            'companion_fields_present':all(k in m for k in ['authority_label_for_record','clauses','expert_clauses','carries','sources_added','evidence_route']),
            'literal_delta':None if m['check']==relocated else {'relocated_round2':relocated,'adopted':m['check']}})
    result={'immutable_files_checked':len(before),'immutable_files_changed_or_missing':altered,
        'baseline_revision':baseline['revision'],'current_revision':current['revision'],
        'original_records_removed':[x for x in changes if x.get('removed')],
        'original_record_changes':changes,'original_20_identities_match':expected_original==actual_original,
        'original_20_records_unchanged':all(old[id]==new.get(id) for id in expected_original),
        'corrected_29_unique_complete':len(rows)==29 and len({x['source_id'] for x in rows})==29 and set(expected)=={x['source_id'] for x in rows},
        'corrected_29_checks':rows}
    save('caller-independent-verification.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['original_record_changes','corrected_29_checks']},indent=2))
    print('changed original records',len(changes),'literal rederivations',sum(not x['literal_matches_permitted_relocation'] for x in rows))

if __name__=='__main__': verify()
