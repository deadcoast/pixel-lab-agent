import json,hashlib,subprocess
from pathlib import Path
O=Path('work/artistic-revision');PY='C:/github/pixel-lab-agent/.venv/Scripts/python.exe';RUN='.agents/skills/artistic-revision-kit/scripts/pixl.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def identity(p):return {'path':p,'sha256':sha(p)}
def call(*a):
 p=subprocess.run([PY,RUN,*a],capture_output=True,text=True,encoding='utf-8')
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return json.loads(p.stdout)
resultpath=O/'SPECIALIST-RESULT.json';initial=O/'SPECIALIST-RESULT-initial.json'
if initial.exists():raise RuntimeError('Preservation target already exists')
initial.write_bytes(resultpath.read_bytes())
d=json.loads((O/'handoff-details.json').read_text());d['caller_actions']['coverage']=identity('work/artistic-revision/caller-request-review-coverage-final.json');d['caller_actions']['contract_comparison']=identity('work/artistic-revision/caller-criterion-comparisons.json');d['identity_correction']={'reason':'Current independent criterion comparison identity is covered by final public coverage report; initial report and earlier handoff retained unchanged.','prior_specialist_result':identity(str(initial).replace('\\','/')),'prior_handoff':json.loads(resultpath.read_text())['handoff'],'acceptance_change':False}
newdetails=O/'handoff-details-final.json';newdetails.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');s=call('plar','read','--path','authoring-plar.txt','--asset','queue.working','--root',str(Path.cwd()));(O/'plar-selected-handoff-final.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n');h=call('plar','handoff',str(newdetails),'--path','authoring-plar.txt','--asset','queue.working','--requirements',s['requirements_hash'],'--expect',s['production']['continuation']['state_hash'],'--root',str(Path.cwd()));(O/'handoff-result-final.json').write_text(json.dumps(h,indent=2,ensure_ascii=False)+'\n');r=json.loads(resultpath.read_text());r['caller_actions']=d['caller_actions'];r['handoff']=h;r['identity_correction']=d['identity_correction'];resultpath.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'specialist_result':identity(str(resultpath).replace('\\','/')),'handoff':h,'prior_result':identity(str(initial).replace('\\','/'))},indent=2))
