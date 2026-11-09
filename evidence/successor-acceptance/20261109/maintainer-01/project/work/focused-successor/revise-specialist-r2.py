from pathlib import Path
import json,hashlib,shutil
p=Path('work/focused-successor/specialist-proposal.json'); r1=p.with_name('specialist-proposal-r1.json')
if not r1.exists():shutil.copyfile(p,r1)
d=json.loads(p.read_text(encoding='utf-8'))
changes=[]
for c in d['criteria']:
 for q in c['successor_checks']:
  text=q['check']
  if c['criterion'].endswith('working.q.geometry'):
   text=text.replace('and advances floor(elapsed/100) mod 4 (nominal 400 ms cycle).','and, under no-preference only, advances floor(elapsed/100) mod 4 (nominal 400 ms cycle). Under reduced motion it selects frame zero without changing the four-cell sheet geometry.')
  if c['criterion'].endswith('working.q.consumers'):
   text=text.replace('Frame advance evidence:', 'Normal-motion (no-preference) frame advance evidence:')
  if c['criterion'].endswith('delivery.q.continuity'):
   text=text.replace("including Working's four frames and its actual 100 ms playback with the wrap", "including Working's four frames, its actual 100 ms playback with the wrap under no-preference, and its stationary frame-zero presentation under reduce")
  if c['criterion'].endswith('delivery.q.destination'):
   text=text.replace('frame index floor(elapsed/100) mod frames at the timeline sample points including the 400 ms wrap','under no-preference only, frame index floor(elapsed/100) mod frames at the timeline sample points including the 400 ms wrap')
  if text!=q['check']:changes.append({'criterion':c['criterion'],'before':q['check'],'after':text})
  q['check']=text
# Preserve the original literal and r2 comparison criteria as history; only successor checks change.
d['revision']=2; d['supersedes']={'path':str(r1).replace('\\','/'),'sha256':hashlib.sha256(r1.read_bytes()).hexdigest(),'reason':'Caller found unqualified normal-motion frame-advance wording that could contradict frozen reduced-motion mode.'}; d['revision_changes']=changes
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('proposal',hashlib.sha256(p.read_bytes()).hexdigest(),'changes',len(changes))
m=json.loads(Path('work/focused-successor/render-01/motion.json').read_text(encoding='utf-8-sig'))
for phase in m['phases']:
 samples=phase['samples'];print(phase['name'],'samples',len(samples),'span_ms',samples[-1]['at']-samples[0]['at'],'frames', sorted({cell['frame'] for s in samples for cell in s['cells']}),'hashes',len({cell['image']['sha256'] for s in samples for cell in s['cells']}))
