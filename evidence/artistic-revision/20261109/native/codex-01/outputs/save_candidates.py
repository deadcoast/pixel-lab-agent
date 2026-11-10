import json,subprocess,hashlib
from pathlib import Path
PY='C:/github/pixel-lab-agent/.venv/Scripts/python.exe';RUN='.agents/skills/artistic-revision-kit/scripts/pixl.py';O=Path('work/artistic-revision')
def call(*args):
 p=subprocess.run([PY,RUN,*args],capture_output=True,text=True,encoding='utf-8');print(p.stdout[:1000] if p.returncode else 'ok '+args[0]);
 if p.returncode:raise SystemExit(p.stdout+p.stderr)
 return json.loads(p.stdout)
d=call('decode','.pixl/assets/queue.ready/state.px');b={x['id']:x for x in d['records']};expect=json.loads((O/'production-plan.stdout.json').read_text())['hash']
for key,path in [('artistic-view','renderer-artistic/view.mjs'),('artistic-check','renderer-artistic/check.py')]:
 b['artistic.source.'+key]['fields']['dg']=hashlib.sha256(Path(path).read_bytes()).hexdigest();b['artistic.source.'+key]['fields']['ln']=[1,len(Path(path).read_text().splitlines())]
for kind,old in [('working','live.working-animation-motion-01.candidate'),('retry','live.retry.candidate'),('paused','live.paused-cutout-01.candidate')]:
 source=b[old];d['records'].append({'id':'artistic.'+kind+'.candidate','kind':'X','fields':{**source['fields'],'nm':'Exact reused accepted art under new artistic criteria; original '+old,'ct':{'$ref':'artistic.'+kind+'.contract'},'of':{'$ref':'artistic-01.'+kind+'.output'},'mt':{'reuse_provenance':{'source_candidate':old,'source_record_fields':source['fields'],'new_acceptance':False,'scope':'Existing bytes reused, no provider execution; previous acceptance not transferred.'}}}})
d['revision']+=1;(O/'candidate-document.json').write_text(json.dumps(d,indent=2));a=call('commit','.pixl/assets/queue.ready',str(O/'candidate-document.json'),'--json','--expect',expect,'--root',str(Path.cwd()));(O/'commit-candidates.json').write_text(json.dumps(a,indent=2))
