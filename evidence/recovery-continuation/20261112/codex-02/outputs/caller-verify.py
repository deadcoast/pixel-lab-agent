import json, hashlib, io
from pathlib import Path
from PIL import Image

root = Path.cwd().resolve()
base = Path('work/provider-recovery/phase-2')
def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ref(p):
    return {'path': str(p).replace('\\','/'), 'sha256': sha(p)}
specialist_path = base/'SPECIALIST-RESULT.json'
s = read(specialist_path)
assert s['status'] == 'recovered' and s['provider_simulated'] is True
for report in (s, read('work/provider-recovery/phase-1/SPECIALIST-RESULT.json'), read('work/provider-recovery/phase-1/CALLER-RESULT.json')):
    for r in report['evidence_refs']:
        assert sha(r['path']) == r['sha256'], r['path']
before, after, current = [read(base/name) for name in ('jobs-before.json','jobs-after.json','caller-jobs.json')]
assert current == after
jobs = {j['id']: j for j in current['jobs']}
assert jobs['unresolved-job']['state'] == 'unknown'
assert next(j for j in before['jobs'] if j['id']=='unresolved-job') == jobs['unresolved-job']
j = jobs['recoverable-job']
assert j['remote_id'] == s['remote_id'] == 'controlled-recovery-0001'
c = j['recovery']['imported'][0]
candidate = {'id':c['candidate_id'], 'output':c['output_id'], 'path':c['path'], 'sha256':c['sha256']}
assert candidate == s['candidate']
p = (root/c['path']).resolve()
assert p.is_relative_to(root)
data = p.read_bytes()
response = read(base/'provider-result.json')
expected = response['images'][0]
assert response['job_id']==j['remote_id'] and response['provider_simulated'] is True
assert len(data)==expected['bytes']==177
assert sha(p)==expected['sha256']==c['sha256']
assert data==(base/'retrieved.png').read_bytes()
im=Image.open(io.BytesIO(data)); im.verify()
im=Image.open(io.BytesIO(data)); im.load()
assert im.format=='PNG' and im.size==(expected['width'],expected['height'])==(32,32)
assert 'path: "assets/robot.png", width: 32, height: 32, sampling: "nearest"' in Path('src/avatar.ts').read_text()
assert read(base/'import-evidence.json') == j['events'][-1]['evidence']
imp=read(base/'import-result.json')
assert imp['hash']==current['hash'] and imp['revision']==current['revision']
assert sha('.pixl/recovery/state.px')==s['state']['sha256']
assert s['state']['canonical_hash']==current['hash']
destination=Path('assets/robot.png')
assert not destination.exists() or destination.read_bytes()==data
destination.write_bytes(data)
assert destination.read_bytes()==data
result={k:s[k] for k in ('phase','status','provider_simulated','provider','job','remote_id','unresolved_job','unresolved_state','state','limitations')}
result.update(candidate=candidate,
 native_child={'id':'/root/pixl','agent_type':'pixl','fork_turns':'none','status':'completed'},
 specialist_result=ref(specialist_path),
 evidence_refs=[ref(r['path']) for r in s['evidence_refs']]+[ref(base/'caller-jobs.json'),ref(p.relative_to(root)),ref(destination),ref('src/avatar.ts'),ref(base/'caller-verify.py')],
 checks={'full_jobs_before_after_and_independent_current_read':True,'specialist_evidence_hashes_verified':True,'phase1_evidence_hashes_unchanged':True,'candidate_bytes':len(data),'candidate_sha256':sha(p),'png_decode':'32x32 RGBA PNG','host_image_opened':True,'host_image_observation':'Native candidate opened with view_image; small cyan robot-like fixture with yellow eye pixels. Viewing establishes no artistic acceptance.','consumer_mapping':'assets/robot.png; 32x32; nearest','exact_bytes_copied':True,'visual_acceptance':'unperformed','artistic_acceptance':'unperformed','engine_acceptance':'unperformed','human_acceptance':'unperformed','milestones':'M1/M2 and broader M3/M4 remain open'},
 next_action='Phase 3: cold-consume the same retained candidate and current public state; no new dispatch or import. Preserve unresolved-job unknown absent matching originating evidence.')
(base/'CALLER-RESULT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'candidate':candidate,'destination':ref(destination),'caller_result':ref(base/'CALLER-RESULT.json')},indent=2))
