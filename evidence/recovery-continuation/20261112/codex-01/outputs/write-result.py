import json, hashlib
from pathlib import Path
p=Path('work/provider-recovery/phase-1')
def ref(path):
    path=Path(path)
    return {'path': path.as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
jobs=json.loads((p/'jobs-after.json').read_text())
state=ref('.pixl/recovery/state.px')
state.update(canonical_hash=jobs['hash'],revision=jobs['revision'])
names=['ASSIGNMENT.md','jobs-before.json','jobs-after.json','workflow.json','provider-list.json','provider-status-1.json','provider-status-2.json','observe-running.json','observe-succeeded.json','download.part','download-error.json','download-stdout.bin','download-stderr.bin','download-once.py']
result={'phase':1,'status':'partial','provider_simulated':True,'provider':'pixellab-recovery-test','job':'recoverable-job','remote_id':'controlled-recovery-0001','unresolved_job':'unresolved-job','unresolved_state':'unknown','candidate':None,'state':state,'evidence_refs':[ref(p/n) for n in names],'checks':{'identity':'Full saved tool and arguments equal originating list entry. input.png and reference.png actual SHA-256 equal their saved upload handles; listed source_sha256 equals input.png. Exact ID returned processing then completed.','retrieval':'Exactly one curl invocation; exit 18, 59 of expected 177 bytes retained. No import or retry.','integration':'not_performed','human_acceptance':'unperformed','artistic_acceptance':'unperformed','engine_acceptance':'unperformed'},'limitations':['Controlled simulated fixture only; no live PixelLab evidence.','Partial retrieval is unusable as a complete candidate; no acceptance or nomination.','unresolved-job lacks matching evidence and remains unknown; listing absence does not prove non-acceptance.','M1/M2 and broader M3/M4 remain open.'],'next_action':{'phase':2,'operation':'Re-query mcp__pixellab_recovery__get_image on the same originating pixellab-recovery-test connection with job_id controlled-recovery-0001 for a fresh process-local URL. Download into a fresh phase-2 path, preserve phase-1 files, verify complete 177-byte 32x32 PNG SHA-256 d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7, read current jobs/hash, then public job-import for recoverable-job/recovered-avatar. Keep unresolved-job unknown. Do not prepare, dispatch, submit or upload.','expected_state_hash':jobs['hash'],'output':'recovered-avatar'}}
(p/'SPECIALIST-RESULT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(ref(p/'SPECIALIST-RESULT.json')))
print(json.dumps(state))
