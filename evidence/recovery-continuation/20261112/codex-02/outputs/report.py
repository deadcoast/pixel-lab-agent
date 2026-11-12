import json, hashlib
from pathlib import Path
p=Path('work/provider-recovery/phase-2')
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
before=json.loads((p/'jobs-before.json').read_text())
after=json.loads((p/'jobs-after.json').read_text())
job=next(j for j in after['jobs'] if j['id']=='recoverable-job')
unresolved=next(j for j in after['jobs'] if j['id']=='unresolved-job')
assert unresolved==next(j for j in before['jobs'] if j['id']=='unresolved-job')
c=job['recovery']['imported'][0]
assert digest(c['path'])==c['sha256']==digest(p/'retrieved.png')
old=json.loads(Path('work/provider-recovery/phase-1/SPECIALIST-RESULT.json').read_text())
for ref in old['evidence_refs']:
    assert digest(ref['path'])==ref['sha256'], ref['path']
refs=[str(p/n).replace('\\','/') for n in ['ASSIGNMENT.md','jobs-before.json','jobs-after.json','provider-result.json','retrieved.png','verification.json','import-evidence.json','import-result.json','verify.py','report.py']]
r=dict(phase=2,status='recovered',provider_simulated=True,provider='pixellab-recovery-test',job='recoverable-job',remote_id=job['remote_id'],unresolved_job='unresolved-job',unresolved_state=unresolved['state'],candidate=dict(id=c['candidate_id'],output=c['output_id'],path=c['path'],sha256=c['sha256']),state=dict(path='.pixl/recovery/state.px',sha256=digest('.pixl/recovery/state.px'),canonical_hash=after['hash'],revision=after['revision']),evidence_refs=[dict(path=x,sha256=digest(x)) for x in refs],checks=dict(retrieval='177 complete bytes; SHA-256, PNG verification and full RGBA decoding match fresh originating response; retained candidate has equal bytes.',phase1_preservation='All prior specialist evidence references retain their exact SHA-256.',integration='not_performed',visual_acceptance='unperformed',artistic_acceptance='unperformed',engine_acceptance='unperformed',human_acceptance='unperformed'),limitations=['Controlled simulated fixture only; no live PixelLab evidence.','Candidate imported without acceptance, nomination or task completion.','unresolved-job remains unknown; insufficient observations cannot prove non-acceptance.','M1/M2 and broader M3/M4 remain open.'],next_action='Caller independently reads this report and current full jobs, hashes and opens the retained candidate, verifies src/avatar.ts mapping, copies exact candidate bytes to assets/robot.png and writes CALLER-RESULT.json. Phase 3 cold-consumes the same retained candidate without another dispatch or import.')
(p/'SPECIALIST-RESULT.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(report=str(p/'SPECIALIST-RESULT.json'),sha256=digest(p/'SPECIALIST-RESULT.json'),candidate=r['candidate'],state=r['state'])))
