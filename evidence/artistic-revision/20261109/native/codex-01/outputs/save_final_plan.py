import json,hashlib,subprocess,datetime,copy
from pathlib import Path
O=Path('work/artistic-revision');PY='C:/github/pixel-lab-agent/.venv/Scripts/python.exe';RUN='.agents/skills/artistic-revision-kit/scripts/pixl.py';ROOT=str(Path.cwd());STORE='.pixl/assets/queue.ready'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def call(tag,*args):
 p=subprocess.run([PY,RUN,*args],capture_output=True,text=True,encoding='utf-8');Path(O/f'{tag}.json').write_text(p.stdout,encoding='utf-8')
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return json.loads(p.stdout)
# Refresh only source hashes, retaining historical documents via public save.
plar=json.loads(Path('authoring-plar.txt').read_text());old=sha('authoring-plar.txt')
for src in plar['sources']:
 if src['id'] in ['artistic-renderer-view','artistic-renderer-check']:src['sha256']=sha(src['path'])
save(O/'plar-final-sources.json',plar);call('plar-save-final','plar','save',str(O/'plar-final-sources.json'),'--path','authoring-plar.txt','--expect',old,'--root',ROOT)
doc=call('state-before-plan02','decode',STORE+'/state.px');expect=call('validate-before-plan02','validate',STORE+'/state.px','--root',ROOT)['hash'];now=datetime.datetime.now(datetime.timezone.utc).isoformat();ref=lambda x:{'$ref':x};sources={}
for key,path in [('view','renderer-artistic/view.mjs'),('check','renderer-artistic/check.py')]:
 lines=Path(path).read_text().splitlines()
 for n,start in enumerate(range(1,len(lines)+1,150)):
  sid=f'artistic2.source.{key}.{n}';sources[sid]=sid;doc['records'].append({'id':sid,'kind':'S','fields':{'ur':path,'dg':sha(path),'ln':[start,min(start+149,len(lines))],'au':{'$symbol':'local'},'at':now}})
r2=json.loads(Path('work/continuation/SPECIALIST-ROUND2.json').read_text());prop=json.loads(Path('work/focused-successor/specialist-proposal.json').read_text());byprop={x['id']:x for x in prop['criteria']};lines=Path('work/continuation/SPECIALIST-ROUND2.json').read_text().splitlines();round2ids={}
for row in r2['corrected_criteria']:
 occurrences=[i+1 for i,l in enumerate(lines) if '"id": "'+row['id']+'"' in l];start=occurrences[-1]-1;end=next((i for i in range(start+1,len(lines)) if lines[i].startswith('    },')),start+150)+1;sid='artistic2.source.round2.'+row['id'].split('.q.')[0].split('.')[-1]+'.'+row['id'].split('.q.')[1];round2ids[row['id']]=sid;doc['records'].append({'id':sid,'kind':'S','fields':{'ur':'work/continuation/SPECIALIST-ROUND2.json','dg':sha('work/continuation/SPECIALIST-ROUND2.json'),'ln':[start,min(end,start+199)],'au':{'$symbol':'local'},'at':now}})
# The old PLAR source is immutable retained bytes. Narrow each literal original locator independently.
plars={}
for row in prop['criteria']:
 for sr in row['sources']:
  if sr['id']=='plar':
   bounds=sr['lines'];sid='artistic2.source.plar.'+str(bounds[0])+'.'+str(bounds[1]);plars[tuple(bounds)]=sid
for (start,end),sid in plars.items():doc['records'].append({'id':sid,'kind':'S','fields':{'ur':'work/artistic-revision/authoring-plar-before.json','dg':sha(O/'authoring-plar-before.json'),'ln':[start,end],'au':{'$symbol':'local'},'at':now}})
doc['revision']+=1;save(O/'source-document-plan02.json',doc);a=call('commit-sources-plan02','commit',STORE,str(O/'source-document-plan02.json'),'--json','--expect',expect,'--root',ROOT)
plan=json.loads(Path(O/'production-plan.json').read_text());plan['id']='artistic-02'
for stage in plan['stages']:
 kind=stage['id'];sel=call('selected-final-'+kind,'plar','read','--path','authoring-plar.txt','--asset','queue.'+kind,'--root',ROOT);stage['selection']['requirements_hash']=sel['requirements_hash'];stage['selection']['replaces']=next(x for x in json.loads(Path('authoring-plar.txt').read_text())['assets'] if x['id']=='queue.'+kind)['production']
for target in plan['stages']+[plan['delivery']]:
 for criterion in target['criteria']:
  oldid='successor-01.'+('delivery' if target is plan['delivery'] else target['id'])+'.q.'+criterion['id'];old=byprop[oldid]
  filtered=[s for s in criterion['sources'] if s not in ['artistic.source.plar','artistic.source.round2','artistic.source.artistic-view','artistic.source.artistic-check','artistic.source.succ-view','artistic.source.succ-check']]
  criterion['sources']=list(dict.fromkeys(filtered+list(sources)+[round2ids[oldid]]+[plars[tuple(s['lines'])] for s in old['sources'] if s['id']=='plar']))
save(O/'production-plan-02.json',plan);result=call('production-plan-02','production-plan',STORE,str(O/'production-plan-02.json'),'--expect',a['hash'],'--root',ROOT)
m=json.loads(Path(O/'adopted-criteria.json').read_text());save(O/'adopted-criteria-plan01.json',m)
for row in m['corrected_29']:row['record_id']=row['record_id'].replace('artistic-01.','artistic-02.')
m['rederivation']['final_plan']='artistic-02.plan';m['rederivation']['retained_prior_attempt']='artistic-01.plan: source context drift after parent-requested paint timestamp correction; no verdicts transferred.';save(O/'adopted-criteria.json',m)
print(result['hash'],result['allocation'])
