import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path.cwd().resolve()
phase = Path('work/provider-recovery/phase-3')
def read(path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))
def ref(path):
    p = (root / path).resolve()
    assert p.is_relative_to(root)
    return {'path': str(path).replace('\\', '/'), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

s_path = phase / 'SPECIALIST-RESULT.json'
s = read(s_path)
assert ref(s_path)['sha256'] == 'e48b21f48b1650023cdffb64acd7bbe45a514fecbac666e2ae005b0b87390c1f'
reports = [read(phase / name) for name in ['jobs-before.json', 'jobs-after.json', 'caller-jobs.json']]
assert reports[0] == reports[1] == reports[2]
j = reports[2]
jobs = {x['id']: x for x in j['jobs']}
r, u = jobs['recoverable-job'], jobs['unresolved-job']
assert r['state'] == 'succeeded' and r['remote_id'] == s['remote_id'] == 'controlled-recovery-0001'
assert u['state'] == 'unknown' and u['remote_id'] is None and u['next_action'] == 'reconcile'
c = s['candidate']
imp = r['recovery']['imported'][0]
assert (c['id'], c['output'], c['path'], c['sha256']) == (imp['candidate_id'], imp['output_id'], imp['path'], imp['sha256'])
for e in s['evidence_refs']:
    assert ref(e['path']) == e
for old in ['work/provider-recovery/phase-1/CALLER-RESULT.json', 'work/provider-recovery/phase-2/CALLER-RESULT.json']:
    for e in read(old)['evidence_refs']:
        assert ref(e['path']) == e
candidate = (root / c['path']).read_bytes()
delivered = (root / 'assets/robot.png').read_bytes()
assert candidate == delivered and len(candidate) == 177
assert ref(c['path'])['sha256'] == c['sha256']
for path in [c['path'], 'assets/robot.png']:
    with Image.open(root / path) as im:
        im.load()
        assert (im.format, im.size, im.mode) == ('PNG', (32, 32), 'RGBA')
mapping = (root / 'src/avatar.ts').read_text()
assert 'path: "assets/robot.png"' in mapping and 'width: 32' in mapping and 'height: 32' in mapping and 'sampling: "nearest"' in mapping
assert ref(s['state']['path'])['sha256'] == s['state']['sha256'] == j['hash']
assert s['state']['canonical_hash'] == j['hash'] and s['state']['revision'] == j['revision'] == 9
result = {key: s[key] for key in ['phase', 'status', 'provider_simulated', 'provider', 'job', 'remote_id', 'unresolved_job', 'unresolved_state', 'candidate', 'state', 'limitations']}
result['native_child'] = {'id': '/root/pixl_phase3', 'agent_type': 'pixl', 'fork_turns': 'none', 'status': 'completed'}
result['specialist_result'] = ref(s_path)
paths = [e['path'] for e in s['evidence_refs']] + [str(s_path), str(phase / 'caller-jobs.json'), str(phase / 'caller-verify.py'), s['state']['path']]
result['evidence_refs'] = [ref(p) for p in dict.fromkeys(paths)]
result['checks'] = {
    'full_jobs_before_after_and_independent_current_read': True,
    'full_reports_semantically_equal': True,
    'specialist_and_prior_evidence_hashes_verified': True,
    'candidate_and_delivery_independently_read_hashed_decoded': True,
    'candidate_bytes': len(candidate), 'delivered': ref('assets/robot.png'),
    'png_decode': '32x32 RGBA PNG', 'host_images_opened': [c['path'], 'assets/robot.png'],
    'host_image_observation': 'Both native PNGs show the same small cyan robot fixture with yellow eye pixels; no artistic judgment or acceptance.',
    'consumer_mapping': 'assets/robot.png; 32x32; nearest', 'consumer_paths_confined': True,
    'result_consumed': True, 'state_unchanged': True,
    'provider_calls': 0, 'production_mutations': False, 'file_copies': 0,
    'visual_acceptance': 'unperformed', 'artistic_acceptance': 'unperformed',
    'engine_acceptance': 'unperformed', 'human_acceptance': 'unperformed',
    'milestones': 'M1/M2 and broader M3/M4 remain open'
}
result['next_action'] = {
    'candidate': {'action': r['next_action'], 'guidance': r['recovery']['guidance'], 'inspection': 'Inspect retained candidate against original criteria and current review state in a separately assigned inspection round; no retrieval or generation is needed.'},
    'unresolved_job': u['recovery'],
    'scope': 'Read-only phase 3 completed. Preserve unresolved-job unknown absent exact matching originating-connection evidence. No reconciliation provider call was made in this round.'
}
(root / phase / 'CALLER-RESULT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'report': ref(phase / 'CALLER-RESULT.json'), 'candidate': c, 'delivered': ref('assets/robot.png'), 'state': result['state'], 'next_action': result['next_action']}, indent=2))
