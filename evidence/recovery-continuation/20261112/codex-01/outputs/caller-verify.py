import hashlib, json
from pathlib import Path

root = Path.cwd()
base = Path('work/provider-recovery/phase-1')
def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def ref(p):
    return {'path': str(p).replace('\\', '/'), 'sha256': hashlib.sha256(Path(p).read_bytes()).hexdigest()}
s = read(base/'SPECIALIST-RESULT.json')
before = read(base/'jobs-before.json')
after = read(base/'jobs-after.json')
current = read(base/'caller-jobs.json')
assert current == after
for evidence in s['evidence_refs']:
    assert ref(evidence['path']) == evidence
assert ref(s['state']['path'])['sha256'] == s['state']['sha256']
assert current['hash'] == s['state']['canonical_hash'] and current['revision'] == 8
jobs = {j['id']: j for j in current['jobs']}
old = {j['id']: j for j in before['jobs']}
assert jobs['unresolved-job'] == old['unresolved-job']
j = jobs['recoverable-job']
assert j['state'] == 'succeeded' and j['remote_id'] == s['remote_id']
assert [e['event'] for e in j['events']] == ['dispatch','unknown','running','succeeded']
assert j['candidates'] == [] and j['next_action'] == 'retrieve_outputs'
listed = read(base/'provider-list.json')['structuredContent']['jobs'][0]
assert listed['tool'] == j['request']['tool'] and listed['arguments'] == j['request']['arguments']
assert listed['source_sha256'] == ref('input.png')['sha256']
assert listed['arguments']['reference_image']['url'] == 'upload:controlled-' + ref('reference.png')['sha256']
err = read(base/'download-error.json')
part = (base/'download.part').read_bytes()
assert err['exit_code'] == 18 and err['attempts'] == 1 and len(part) == 59
assert err['partial']['sha256'] == hashlib.sha256(part).hexdigest()
assert (base/'download-stderr.bin').read_bytes().decode() == err['stderr']
assert len(part) < err['expected']['bytes'] == 177
assert 'assets/robot.png' in Path('src/avatar.ts').read_text()
assert not Path('assets/robot.png').exists()
result = {k: s[k] for k in ['phase','status','provider_simulated','provider','job','remote_id','unresolved_job','unresolved_state','candidate','state','limitations','next_action']}
result['native_child'] = {'id':'/root/pixl_phase1','agent_type':'pixl','fork_turns':'none','status':'completed'}
result['specialist_result'] = ref(base/'SPECIALIST-RESULT.json')
result['evidence_refs'] = s['evidence_refs'] + [ref(base/'caller-jobs.json'),ref('src/avatar.ts'),ref('input.png'),ref('reference.png'),ref(base/'caller-verify.py')]
result['checks'] = {'full_jobs_before_after_read':True,'independent_current_jobs_matches':True,'all_specialist_evidence_hashes_verified':True,'full_tool_arguments_input_identity_matches':True,'partial_bytes_and_exact_error_verified':True,'consumer_mapping':'assets/robot.png; 32x32; nearest; destination absent','candidate_imported':False,'human_acceptance':'unperformed','artistic_acceptance':'unperformed','engine_acceptance':'unperformed','milestones':'M1/M2 and broader M3/M4 remain open'}
out = base/'CALLER-RESULT.json'
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'result':ref(out),'checks':result['checks'],'partial_bytes':len(part),'state':result['state']}))
