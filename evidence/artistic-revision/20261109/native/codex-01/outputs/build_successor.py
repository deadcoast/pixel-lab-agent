import json,hashlib,subprocess,datetime,copy
from pathlib import Path
ROOT=Path.cwd(); OUT=Path('work/artistic-revision');PY='C:/github/pixel-lab-agent/.venv/Scripts/python.exe';RUN='.agents/skills/artistic-revision-kit/scripts/pixl.py';STORE='.pixl/assets/queue.ready'
def save(p,d): Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def call(tag,*args):
 p=subprocess.run([PY,RUN,*args],capture_output=True,text=True,encoding='utf-8');Path(OUT/f'{tag}.stdout.json').write_text(p.stdout,encoding='utf-8');Path(OUT/f'{tag}.stderr.txt').write_text(p.stderr,encoding='utf-8');
 if p.returncode: raise RuntimeError(tag+':'+p.stdout+p.stderr)
 return json.loads(p.stdout)
def ref(x):return {'$ref':x}
def sym(x):return {'$symbol':x}
doc=json.loads(Path(OUT/'state-after-abandonment.json').read_text());records=doc['records'];by={r['id']:r for r in records};now=datetime.datetime.now(datetime.timezone.utc).isoformat()
r2=json.loads(Path('work/continuation/SPECIALIST-ROUND2.json').read_text());prop=json.loads(Path('work/focused-successor/specialist-proposal.json').read_text());orig={x['id']:x for x in prop['criteria']};ctx=json.loads(Path(OUT/'context-initial.json').read_text())
# Preserve source PLAR bytes before moving current destination bindings.
# before snapshot already retained
sources={}
for key,source in prop['sources'].items():
 if key in ['state','plar'] or Path(source['path']).suffix.lower() in ['.png','.svg']: continue
 path=source['path'];sid='artistic.source.'+key;sources[key]=sid
 records.append({'id':sid,'kind':'S','fields':{'ur':path,'dg':sha(path),'au':sym('local'),'at':now,'ln':[1,max(1,len(Path(path).read_text(encoding='utf-8',errors='replace').splitlines()))]}})
for key,path in {'round2':'work/continuation/SPECIALIST-ROUND2.json','evaluation':'ARTISTIC-REVISION.md','artistic-module':'src/queue-view-artistic.ts','artistic-view':'renderer-artistic/view.mjs','artistic-check':'renderer-artistic/check.py','authoring-stage':'AUTHORING-STAGE.md','plar':'work/artistic-revision/authoring-plar-before.json'}.items():
 sid='artistic.source.'+key;sources[key]=sid;records.append({'id':sid,'kind':'S','fields':{'ur':path,'dg':sha(path),'au':sym('local'),'at':now,'ln':[1,max(1,len(Path(path).read_text(encoding='utf-8',errors='replace').splitlines()))]}})
choice=copy.deepcopy(by['render.choice.destination']);choice['id']='artistic.choice.destination';choice['fields']['ky']='family.destination.artistic';choice['fields']['so']=[ref(sources[k]) for k in ['evaluation','artistic-module','artistic-view']];choice['fields']['vl'].update({'module':'src/queue-view-artistic.ts','fixture':'renderer-artistic/','placement_acceptance':'fresh checker evidence required; historical acceptance not transferred','live_scales':[1,3]});choice['fields']['wy']='SCOPED EVALUATION CALLER CHOICE P1: hold existing Working frame zero using still descriptor; broad original adopted aesthetic. Fresh artistic destination; no historical owner requirement asserted.';records.append(choice)
by['project']['fields']['in'].append(ref('artistic.choice.destination'))
for kind in ['working','retry','paused']:
 c=copy.deepcopy(by['family.'+kind+'.contract']);c['id']='artistic.'+kind+'.contract';c['fields']['ch']=[ref('render.choice.style'),ref('artistic.choice.destination')];records.append(c)
doc['revision'] += 1
save(OUT/'planning-document.json',doc)
a=json.loads(Path(OUT/'commit-planning.stdout.json').read_text())
plan={'version':1,'id':'artistic-01','project':'project','actor':'actor','baseline':'ready.retained','decisions':['render.decision.style','recheck.decision.destination'],'knowledge':[],'stages':[],'delivery':{'name':'Corrected artistic reused-art family','members':['r.22e90a2a03fe453a.output.ready','working','retry','paused'],'destinations':['artistic.choice.destination'],'criteria':[]}}
mapping={'original_20':[{'id':x['id'],'record_sha256':x['record_sha256']} for x in ctx['criteria']], 'corrected_29':[],'scoped_caller_choice':'SCOPED EVALUATION CALLER CHOICE P1: existing Working frame zero held with still descriptor. Not historical owner requirement.', 'rederivation':{'permitted_path_changes':{'src/queue-view-successor.ts':'src/queue-view-artistic.ts','renderer-successor/':'renderer-artistic/'},'fixture_changes':'Actual live cells now 1x AND 3x in both consumers; playback rows sample actual requestAnimationFrame canvas exposure plus performance.now over >1 second; stateLive retains actual all-state live pixels. Existing synthetic timeline retained separately. Original corrected literal clauses retained with path substitutions only; additional evidence strengthens coverage without weakening outcomes.','sources':['src/queue-view-artistic.ts','renderer-artistic/view.mjs','renderer-artistic/check.py'],'caller_review':'pending independent caller review'}}
for kind in ['working','retry','paused']:
 selected=call('selected-'+kind,'plar','read','--path','authoring-plar.txt','--asset','queue.'+kind,'--root',str(ROOT));prod=selected['production'];print(kind,selected['requirements_hash'],prod.keys())
 link=selected['asset']['production'] if 'asset' in selected else next(x for x in json.loads(Path('authoring-plar.txt').read_text())['assets'] if x['id']=='queue.'+kind)['production']
 plan['stages'].append({'id':kind,'name':'Corrected artistic '+kind,'phase':'production','kind':'animation' if kind=='working' else 'sprite','contract':'artistic.'+kind+'.contract','needs':[],'criteria':[],'selection':{'path':'authoring-plar.txt','asset':'queue.'+kind,'requirements_hash':selected['requirements_hash'],'replaces':link}})
for row in r2['corrected_criteria']:
 check=row['original_check'] if row['corrected_check']=='(unchanged)' else row['corrected_check'];check=check.replace('src/queue-view-successor.ts','src/queue-view-artistic.ts').replace('renderer-successor/','renderer-artistic/')
 rid=row['id'].replace('successor-01.','artistic-01.');item={'source_id':row['id'],'record_id':rid,'check':check,**{k:row[k] for k in ['authority_label_for_record','clauses','expert_clauses','carries','sources_added','evidence_route']}};mapping['corrected_29'].append(item)
 srclist=list(dict.fromkeys([sources[x['id']] for x in orig[row['id']]['sources'] if x['id'] in sources]+[sources[x['id']] for x in row['sources_added'] if x['id'] in sources]+[sources['round2'],sources['evaluation'],sources['artistic-module'],sources['artistic-view'],sources['artistic-check']]))
 cr={'id':row['id'].split('.q.')[1],'check':check,'domain':row['domain'],'mode':row['mode'],'sources':srclist}
 target=plan['delivery'] if '.delivery.' in rid else next(x for x in plan['stages'] if '.'+x['id']+'.' in rid);target['criteria'].append(cr)
save(OUT/'adopted-criteria.json',mapping);save(OUT/'production-plan.json',plan)
result=call('production-plan','production-plan',STORE,str(OUT/'production-plan.json'),'--expect',a['hash'],'--root',str(ROOT));print('plan saved',result.keys())
