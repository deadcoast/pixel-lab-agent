import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'work/integration-change'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n): return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def ref(n):
 p=OUT/n
 return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
specialist=load('SPECIALIST-RESULT.json')
refs=[r for r in specialist.values() if isinstance(r,dict) and set(r)=={'path','sha256'}]+specialist['helpers']
for r in refs: assert sha(ROOT/r['path'])==r['sha256'],r
checks=load('parent-byte-checks.json')
assert not checks['protected_file_changes'] and not checks['old_immutable_changes']
assert checks['asset_row_changes']==['queue.working']
assert set(checks['source_binding_changes'])=={'working-timing','timing-authority'}
assert all(r['pass'] for r in checks['exact_art'].values())
jobs=load('parent-jobs.json')['jobs']
assert all(r['remote_id'] is None and r['state']=='failed' for r in jobs)
old=next(r for r in jobs if r['id']=='first_request')
assert old['intent_sha256']=='c3a5945daca98b5ae465d3e3679185438e12e89ab7a62758485e82d3f1f96dbe'
context=load('delivery-context.json')
manifest=json.loads((ROOT/context['candidate_file']['path']).read_bytes())
capture=load('delivery-capture/render.json')
for member in manifest['files']:
 assert member['sha256']==sha(ROOT/'assets/working.png')==capture['served_files']['consumer/assets/working.png']
 assert sha(ROOT/context['candidate_file']['path'])==context['candidate_file']['sha256']
assert capture['display']['frameMs']==150 and capture['playback']['frameMs']==150
assert capture['playback']['status']=='observed'
assert load('renderer-check.json')['status']=='pass'
acceptance=load('parent-acceptance.json')
assert acceptance==load('acceptance.json')
family=acceptance['families'][0]
assert family['state']=='done'
handoff=load('handoff.json')
assert sha(ROOT/handoff['path'])==handoff['sha256']
result={
 'status':'delivered','native_child':{'canonical_path':'/root/pixl','agent_type':'pixl','fork_turns':'none'},
 'specialist_result':ref('SPECIALIST-RESULT.json'),'parent_refresh':ref('parent-refresh.json'),
 'parent_selections':ref('parent-selections.json'),'parent_acceptance':ref('parent-acceptance.json'),
 'handoff':ref('handoff.json'),'durable_handoff':{'path':handoff['path'],'sha256':handoff['sha256']},
 'independent_checks':{
  'bytes':ref('parent-byte-checks.json'),'jobs':ref('parent-jobs.json'),
  'specialist_references_hash_verified':True,'original_job_intent_preserved':True,
  'all_jobs_locally_abandoned_remote_ids_null':True,'only_working_row_changed':True,
  'package_member_equals_original_and_served_working':True,'current_frame_ms':150,'cycle_ms':600,
  'renderer_check':ref('renderer-check.json'),'capture':ref('delivery-capture/render.json'),
  'actual_parent_viewing':{'mode':'visual','files':[ref('delivery-capture/'+n) for n in ['destination.png','view-004.png','view-005.png','view-006.png','view-007.png','view-031.png','view-032.png','view-033.png','view-034.png','view-035.png','view-036.png']],
   'observations':'Opened destination screenshot and actual Working native/enlarged views from both consumers, plus retained live-painted phases. Cool-blue segmented ring remains readable against dark panel and differs in silhouette from check, pause bars and retry arrow. Both consumers show matching actual pixels. Timing judgment derives from retained real browser samples and passing byte/pixel check, not static image viewing.'},
  'public_acceptance_matches_specialist':True,
  'recovery':'Initial parent family read used directory rather than state.px; exact failure preserved as parent-acceptance-directory-failure.*. Correct public MCP family read saved parent-acceptance.json.'},
 'scope':'CF-07/NF-06 controlled exact-art Working timing integration at150ms only.',
 'limitations':['Native1x live playback unperformed;1x/3x stills and controlled1x frame boundaries retained separately.','Parent inspected retained live phase images and actual timing reports, not a continuous playback video.','No provider execution; this does not evaluate provider quality or host reliability.','M1/M2 and broader M3 remain open.'],
 'next_action':'Retain this controlled acceptance and handoff; address M1/M2 and broader M3 under separate authorized scope.',
 'evidence_helpers':[ref(n) for n in ['parent-verify.py','parent-finish.py','write-caller-result.py','finish-recovery.py']]}
target=OUT/'CALLER-RESULT.json'
assert not target.exists()
target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'path':target.relative_to(ROOT).as_posix(),'sha256':sha(target),'status':'delivered'}))
