import json
from pathlib import Path
from caller_verify import ROOT, OUT, read, sha, check_named, baseline
r1=read('work/named-role/SPECIALIST-ROUND1.json')
r2=read('work/named-role/SPECIALIST-ROUND2.json')
checks=check_named(r1)+check_named(r2)
assert r1['roots']==r2['roots']
assert r1['identities']==r2['identities']
c=read('work/named-role/CALLER-CONTEXT-ROUND2.json')
assert c==read('work/named-role/CALLER-CONTEXT-ROUND1.json')
s=read('work/named-role/CALLER-SELECTED-ROUND2.json')
assert s==read('work/named-role/CALLER-SELECTED-ROUND1.json')
replay=read('work/named-role/round2-review-replay.json')
assert replay['reused_review'] is True and replay['publications']==[] and replay['remote_executed'] is False
assert replay['state_hash']==c['state_hash'] and replay['revision']==126
assert sha(replay['review_path'])==replay['review_sha256']
hresult=read('work/named-role/round2-handoff-result.json')
h=read(hresult['path'])
assert sha(hresult['path'])==hresult['sha256']
assert h['resume']==s['production']['continuation']
assert h['requirements_hash']==s['requirements_hash'] and h['asset_id']=='queue.working'
assert h['next']==s['production']['next_action']=='delivered'
assert h['details']['checks']['fresh_visual_observation'] is False
assert h['details']['checks']['provider_calls']==0
n=baseline()
known={str(Path(x['path']).resolve()).lower() for x in read('work/named-role/CALLER-BASELINE.json')}
new=[]
for p in ROOT.rglob('*'):
    if not p.is_file() or '__pycache__' in p.parts or '.git' in p.parts: continue
    rel=p.relative_to(ROOT).as_posix()
    if str(p.resolve()).lower() not in known and not rel.startswith('work/named-role/'):
        new.append(rel)
assert new==[hresult['path']], new
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='CALLER-RESULT.json']
result={
 'status':'completed',
 'qualification':'Observed registered-role two-round retained-asset recovery and public handoff route only.',
 'child':{'actual_returned_identity':'/root/pixl_specialist','spawn_agent_type':'pixl','fork_turns':'none','spawn_result':{'task_name':'/root/pixl_specialist'},'host_role_rejection':None,'continuation_tool':'collaboration.followup_task','continuation_target':'/root/pixl_specialist','observed_completion':'Both round completion messages and saved reports received; same child returned round2 after caller review. No replacement spawned; child kept available.','proof_limit':'Native tool selected and accepted the registered role; reported skill/profile reads and byte hashes are separate observations, not internal host prompt-loading instrumentation.'},
 'rounds':[{'report':'work/named-role/SPECIALIST-ROUND1.json','sha256':sha('work/named-role/SPECIALIST-ROUND1.json'),'result':'Independent source excerpt, named file hashes, selected generation/plan, exact candidate context and member bytes verified.'},{'report':'work/named-role/SPECIALIST-ROUND2.json','sha256':sha('work/named-role/SPECIALIST-ROUND2.json'),'result':'Original unchanged review reused; public handoff and all named file hashes independently verified.'}],
 'caller_review':{'path':'work/named-role/CALLER-REVIEW.json','sha256':sha('work/named-role/CALLER-REVIEW.json')},
 'corrections':[],
 'identities':r2['identities'],
 'acceptance':{'current':c['current_acceptance'],'creation_time':c['snapshot_acceptance'],'fresh_visual_or_renderer_observation':False},
 'verification':{'named_hash_checks':checks,'baseline_files_unchanged':n,'baseline_exclusions':['work/named-role outputs','__pycache__ files','.git internals'],'new_files_outside_report_directory':new,'original_review_sha256':sha(replay['review_path']),'original_replay_input_sha256':sha('work/export-review/identical-review.json'),'reused_review':True,'production_publications':0,'provider_attempts':0,'state_revision_before_and_after':126,'evidence':'All baseline sources/assets/state/history/reviews and existing handoffs unchanged; no new production-store files; fresh caller public candidate and selected PLAR reads equal round1. Replay reports no publications or remote execution; no provider tools invoked by caller or specialist.'},
 'handoff':hresult,
 'report_files':files,
 'exact_next_action':'Use the immutable public handoff and existing accepted delivered bytes. Before future production, reread focused authoring-plar.txt / queue.working and compare canonical state and selected requirements; no further generation is assigned.',
 'remaining_open':['M1/M2','Broader reliability','Generated quality','Native end-to-end production']}
(OUT/'CALLER-RESULT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'completed','baseline_files_unchanged':n,'named_hash_checks':len(checks),'new_outside_reports':new,'result_sha256':sha('work/named-role/CALLER-RESULT.json')}))
