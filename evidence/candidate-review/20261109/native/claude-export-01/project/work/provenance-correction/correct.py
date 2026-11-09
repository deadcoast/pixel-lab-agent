from pathlib import Path
import json, subprocess, hashlib, copy, sys
from datetime import datetime, timezone
ROOT=Path.cwd(); W=ROOT/'work/provenance-correction'; OLD=ROOT/'work/successor-adoption'
PY='C:/github/pixel-lab-agent/.venv/Scripts/python.exe'
RUN=str(ROOT/'.agents/skills/pixl-kit/scripts/pixl.py')
STORE='.pixl/assets/queue.ready'; STATE=STORE+'/state.px'
sys.path.insert(0,str(ROOT/'.agents/skills/pixl-kit/runtime'))
from pixl import codec, graph
PREFIX='provenance-correction'; PRIOR='successor-adoption-02'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def save(n,o):
 p=W/n; assert not p.exists(),p
 p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); return str(p)
def cli(n,*args):
 p=W/(n+'.json')
 with p.open('xb') as f: r=subprocess.run([PY,RUN,*map(str,args)],stdout=f,stderr=subprocess.PIPE)
 if r.returncode: raise RuntimeError(n+': '+r.stderr.decode('utf-8',errors='replace')+' '+p.read_text(encoding='utf-8'))
 return read(p)
def decode(): return json.loads(subprocess.check_output([PY,RUN,'decode',STATE]).decode('utf-8'))
def commit(n,d):
 d['revision']+=1
 return cli(n,'commit',STORE,save(n+'-document.json',d),'--json','--expect',sha(STATE),'--root',ROOT)
def ref(s): return {'$ref':s}
def sym(s): return {'$symbol':s}
def now(): return datetime.now(timezone.utc).isoformat()
def replace(o):
 if isinstance(o,str):
  return o.replace(PRIOR,PREFIX).replace('successor.source.','provenance.source.').replace('focused-successor.choice.destination','provenance.choice.destination').replace('successor.working.contract','provenance.working.contract').replace('successor.retry.contract','provenance.retry.contract').replace('successor.paused.contract','provenance.paused.contract')
 if isinstance(o,list): return [replace(v) for v in o]
 if isinstance(o,dict): return {k:replace(v) for k,v in o.items()}
 return o
def phase1():
 d=decode(); save('state-before.json',d)
 files={p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.rglob('*') if p.is_file() and not p.is_relative_to(W) and p.relative_to(ROOT).as_posix() not in [STATE,'authoring-plar.txt']}
 save('preservation-before.json',files)
 save('plar-before.json',read('authoring-plar.txt'))
 cli('context-before','context',STATE,PRIOR+'.plan','--view','authoring','--plar','authoring-plar.txt','--asset','queue.working','--root',ROOT)
 cli('workflow-before','workflow',STATE,'--root',ROOT); cli('jobs-before','jobs',STATE,'--root',ROOT)
 idx={r['id']:r for r in d['records']}; mapping=[]; at=now()
 for r in list(d['records']):
  if r['kind']=='S' and r['id'].startswith('successor.source.'):
   f=r['fields']; assert f['at']=='2026-11-09T20:00:00+00:00'
   assert sha(f['ur'])==f['dg']; assert f['ln']==[1,len(Path(f['ur']).read_text(encoding='utf-8').splitlines())]
   n=copy.deepcopy(r); n['id']=replace(r['id']); n['fields']['at']=at;d['records'].append(n)
   mapping.append({'old_id':r['id'],'new_id':n['id'],'unsupported_at':f['at'],'observed_at':at,'path':f['ur'],'sha256':f['dg'],'lines':f['ln'],'erratum':'The prior literal observation time was unsupported and future relative to the run. Retained without alteration; this new timestamp records current byte/line verification only, not original source creation, viewing or rendering.'})
 assert len(mapping)==8
 save('erratum.json',{'observed_at':at,'clock':'datetime.now(timezone.utc) on execution host; external clock tool also read during caller orientation','records':mapping,'old_attempt_preserved':True})
 choice=replace(copy.deepcopy(idx['focused-successor.choice.destination']));choice['fields']['ky']='family.destination.provenance_correction';d['records'].append(choice);idx['project']['fields']['in'].append(ref(choice['id']))
 for k in ['working','retry','paused']: d['records'].append(replace(copy.deepcopy(idx['successor.'+k+'.contract'])))
 commit('sources-contracts',d)
 p=read(OLD/'public-plan-02.json');p=replace(p);p['id']=PREFIX
 for s in p['stages']:
  k=s['id']; rd=cli('plar-'+k+'-before','plar','read','--asset','queue.'+k,'--path','authoring-plar.txt','--root',ROOT)
  assert rd['requirements_hash']==s['selection']['requirements_hash']
  s['selection']['replaces']={'store':STORE,'task':PRIOR+'.'+k+'.task','output':PRIOR+'.'+k+'.output'}
 save('public-plan.json',p)
 cli('production-plan','production-plan',STORE,W/'public-plan.json','--expect',sha(STATE),'--root',ROOT)
 cli('request-review','request-review',STATE,'--plan',PREFIX+'.plan','--root',ROOT)
 print('Phase 1: eight source corrections and explicit successor plan published.')
def compare():
 old=read(OLD/'request-review-02.json'); new=read(W/'request-review.json'); prior=read(OLD/'caller-comparison.json')
 assert len(old['criteria'])==len(new['criteria'])==23
 ni={q['id']:q for q in new['criteria']}; rows=[]
 for q in old['criteria']:
  n=ni[replace(q['id'])]
  for f in ['check','domain','mode','sources','stage','output']: assert replace(q[f])==n[f],(q['id'],f)
  assert n['record_status']=='current' and n['record_sha256']==n['current_record_sha256']
  pr=next(x for x in prior['criterion_comparisons'] if x['criterion']==q['id']); row=replace(copy.deepcopy(pr));row['record_sha256']=n['record_sha256'];row['disposition']='consistent: exact retained obligation; only provenance and necessary new-plan references change';rows.append(row)
 assert replace(old['controls'])==new['controls'] or all(replace(a['fields'])==b['fields'] and replace(a['contract'])==b['contract'] for a,b in zip(old['controls'],new['controls']))
 assert old['baseline']==new['baseline'] and old['request']==new['request']==None
 for s in new['selections']: assert s['requirements_hash']==s['current_requirements_hash']
 checks=[]
 for s in new['sources']:
  p=Path(s['path']); assert p.is_file() and sha(p)==s['sha256'],s['id']; checks.append({'id':s['id'],'path':s['path'],'sha256':s['sha256']})
 result={'reviewer_role':'Independent caller /root comparing exact public report against retained successor contract; no new specialist drafting or artistic judgment','status':'consistent','review_scope_sha256':new['review_scope_sha256'],'criterion_comparisons':rows,'original20_mapping':replace(prior['original20_mapping']),'retained_original20_mapping':prior['original20_mapping'],'controls_comparison':'Exact fields and contracts match after declared ID substitutions. Same baseline, destination, full alpha, geometry, reduced-motion obligations and no provider request.','source_identity_checks':checks,'allowed_substitutions':{'plan':[PRIOR,PREFIX],'source_prefix':['successor.source.','provenance.source.'],'destination_choice':['focused-successor.choice.destination','provenance.choice.destination'],'contract_prefix':['successor.<member>.contract','provenance.<member>.contract']},'diagnostic_visual_splits':3,'prior_comparison':{'path':str((OLD/'caller-comparison.json').relative_to(ROOT)).replace('\\','/'),'sha256':sha(OLD/'caller-comparison.json')},'exact_report':{'path':'work/provenance-correction/request-review.json','sha256':sha(W/'request-review.json')},'independent_judgment':'All23 literal checks independently compared, all20 original mappings retained plus3 transparency diagnostic/visual splits. No new restriction, weakened criterion, generation, render execution or viewing asserted.'}
 save('caller-comparison.json',result)
 cli('request-review-coverage','request-review',STATE,'--plan',PREFIX+'.plan','--comparison','work/provenance-correction/caller-comparison.json','--root',ROOT)
 print('Exact23 checks and unchanged controls compared; mapping retained.')
def candidates():
 d=decode();idx={r['id']:r for r in d['records']}
 for k in ['working','retry','paused']:
  old=idx[PRIOR+'.'+k+'.candidate'];n=replace(copy.deepcopy(old));n['fields']['mt']={'continuity_from_candidate':old['id'],'sha256':old['fields']['dg'],'new_generation':False,'new_visual_observation':False,'destination':'renderer-successor/assets/'+{'working':'working.png','retry':'error-retry.png','paused':'paused.png'}[k]}
  assert sha(n['fields']['ur'])==n['fields']['dg']==sha(n['fields']['mt']['destination']);d['records'].append(n)
 commit('candidate-commit',d)
 for k in ['working','retry','paused']:
  opt=replace(read(OLD/(k+'-inspection-options.json')));save(k+'-inspection-options.json',opt)
  cli(k+'-inspection-prepare','inspection-prepare',STORE,PREFIX+'.'+k+'.candidate','provenance.'+k+'.packet',W/(k+'-inspection-options.json'),'--expect',sha(STATE),'--root',ROOT)
 print('Exact-byte candidates retained with current inspection packets.')
def reviews():
 before=read(W/'state-before.json'); oldidx={r['id']:r for r in before['records']}; files=read(W/'preservation-before.json')
 assert all(sha(p)==h for p,h in files.items()),'Prior file drift'
 continuity={'verified_at':now(),'scope':'Metadata-only re-evaluation of retained observations against newly verified identical bytes and obligations. No new image viewing or renderer run. Prior measured/artistic/renderer limits persist.','comparison':{'path':'work/provenance-correction/caller-comparison.json','sha256':sha(W/'caller-comparison.json')},'members':{}}
 for k in ['working','retry','paused']:
  oldp=read(OLD/(k+'-inspection-prepare.json'));newp=read(W/(k+'-inspection-prepare.json')); oldobs=read(OLD/(k+'-review-observation-02.json'))
  assert len(oldp['views'])==len(newp['views'])
  vmap={}
  for a,b in zip(oldp['views'],newp['views']):
   assert sha(a['path'])==sha(b['path']);assert [a['width'],a['height']]==[b['width'],b['height']];vmap[a['id']]=b['id']
  continuity['members'][k]={'old_packet':oldp['packet'],'new_packet':newp['packet'],'view_id_map':vmap,'all_view_bytes_and_dimensions_equal':True,'prior_observation':{'path':'work/successor-adoption/'+k+'-review-observation-02.json','sha256':sha(OLD/(k+'-review-observation-02.json')),'observed_at':oldobs['observed_at']},'prior_engine_observation':{'path':'work/successor-adoption/engine-observation.json','sha256':sha(OLD/'engine-observation.json')},'old_verdicts':[r for r in before['records'] if r['kind']=='V' and r['fields']['tk']==ref(PRIOR+'.'+k+'.task')]}
 save('continuity.json',continuity)
 for k in ['working','retry','paused']:
  obs=read(OLD/(k+'-review-observation-02.json'));obs['observed_at']=now()
  for o in obs['observations']:
   o['view']=continuity['members'][k]['view_id_map'][o['view']];o['note']='Continuity verification only: exact bytes/dimensions equal the retained prior viewed image; prior host delivered_size retained. No new viewing. See work/provenance-correction/continuity.json. Prior observation: '+o['note']
  for v in obs['verdicts']:
   v['criterion']=replace(v['criterion']);v['reason']='Fresh corrected-scope verdict based on explicitly retained unchanged observation, not new viewing. See work/provenance-correction/continuity.json. '+v['reason']
  obs['limitations']+=['observed_at is current continuity re-evaluation time, not new visual observation time. Prior actual viewing timestamp is in continuity.json.','All original artistic/renderer limitations retained; Working temporal judgment remains unavailable.']
  save(k+'-review-observation.json',obs)
  cli(k+'-inspection-review','inspection-review',STORE,'provenance.'+k+'.packet','provenance.'+k+'.review',W/(k+'-review-observation.json'),'--expect',sha(STATE),'--root',ROOT)
 d=decode();idx={r['id']:r for r in d['records']};parsed=codec.parse(Path(STATE).read_bytes());at=now()
 for k in ['working','retry','paused']:
  q=PREFIX+'.'+k+'.q.consumers';x=PREFIX+'.'+k+'.candidate';t=PREFIX+'.'+k+'.task';e='provenance.'+k+'.engine.evidence';v='provenance.'+k+'.engine.verdict'
  scope=graph.proof_scope(parsed,[x,q]);assert not any(s.startswith('successor.source.') for s in scope)
  d['records'].append({'id':e,'kind':'E','fields':{'nm':'Corrected-scope continuity of retained actual renderer observation '+k,'ur':'work/provenance-correction/continuity.json','dg':sha(W/'continuity.json'),'rs':sym('pass'),'md':sym('live'),'at':at,'bs':[{'rf':ref(s),'dg':codec.record_hash(parsed.records[s])} for s in sorted(scope)]}})
  ov=oldidx['successor02.'+k+'.engine.verdict'];n=copy.deepcopy(ov);n['id']=v;n['fields'].update({'tk':ref(t),'rq':ref(q),'xr':ref(x),'at':at,'ev':[ref(e)],'wy':'Revalidated unchanged renderer/source/image bytes and exact criterion; retained actual engine observation reused, no new execution. See continuity.json. '+ov['fields']['wy']});d['records'].append(n);idx[t]['fields']['vr'].append(ref(v))
 ov=oldidx['successor02.working.motion.unavailable'];n=replace(copy.deepcopy(ov));n['id']='provenance.working.motion.unavailable';n['fields']['at']=at;d['records'].append(n);idx[PREFIX+'.working.task']['fields']['vr'].append(ref(n['id']))
 commit('engine-and-unavailable',d)
 for k in ['retry','paused']:cli(k+'-completion','task-complete',STORE,PREFIX+'.'+k+'.task',PREFIX+'.'+k+'.candidate','--expect',sha(STATE),'--root',ROOT)
 print('Fresh corrected-scope verdicts published from explicit continuity; Retry/Paused completed.')
def finish():
 def cli(n,*args):
  p=W/(n+'.json')
  if p.exists() and p.stat().st_size:return read(p)
  if p.exists():n+='-corrected'
  return globals()['cli'](n,*args)
 def save(n,o):
  p=W/n
  if p.exists():
   if read(p)==o:return str(p)
   n=p.stem+'-corrected'+p.suffix
  return globals()['save'](n,o)
 cli('family-final','family',STATE,PREFIX+'.delivery.output','--root',ROOT)
 j=read('authoring-plar.txt')
 for a in j['assets']:
  k=a['id'].removeprefix('queue.')
  if k in ['working','retry','paused']:
   a['status']='review' if k=='working' else 'integrated'
   a['next']='Working temporal review remains unavailable; directly appraise exact normal100ms playback at1x/3x including wrap, supersede unavailable verdict only on actual review, complete Working then snapshot and review collective family.' if k=='working' else 'Corrected-scope member accepted using verified unchanged observations. Preserve bytes; family delivery remains open pending Working motion and collective checks.'
   a['evidence'].append({'path':'work/provenance-correction/continuity.json','note':'Bounded provenance erratum and corrected-scope continuity; no new generation, viewing or renderer execution.'})
 cli('plar-save-final','plar','save',save('plar-final-document.json',j),'--expect',sha('authoring-plar.txt'),'--path','authoring-plar.txt','--root',ROOT)
 handoffs={};reqs={}
 for k in ['working','retry','paused']:
  rd=cli('plar-'+k+'-final','plar','read','--asset','queue.'+k,'--path','authoring-plar.txt','--root',ROOT);old=read(W/('plar-'+k+'-before.json'));assert rd['requirements_hash']==old['requirements_hash'];reqs[k]=rd['requirements_hash']
  details={'status':'partial' if k=='working' else 'member-complete-family-open','plan':PREFIX+'.plan','member_candidate':PREFIX+'.'+k+'.candidate','family_output':PREFIX+'.delivery.output','family_candidate':None,'erratum':'work/provenance-correction/erratum.json','continuity':'work/provenance-correction/continuity.json','comparison':'work/provenance-correction/caller-comparison.json','acceptance':{'retry':'complete','paused':'complete','working':'motion-continuity unavailable; other7 pass'},'unavailable_verdict':'provenance.working.motion.unavailable','caller_actions':['Directly appraise retained Working100ms playback at1x/3x including wrap; record superseding scoped visual verdict only if justified.','Complete Working only on all passes; then snapshot and independently inspect/review exact copied family and destination before collective acceptance.'],'future_work':['No new generation quality or general host reliability evidence.'],'no_new_viewing_or_render_execution':True}
  details['status']='partial'
  details_path=save(k+'-handoff-details.json',details)
  handoffs[k]=cli(k+'-handoff','plar','handoff',details_path,'--asset','queue.'+k,'--requirements',rd['requirements_hash'],'--expect',sha(STATE),'--path','authoring-plar.txt','--root',ROOT)
 cli('validation-final','validate',STATE,'--root',ROOT);cli('workflow-final','workflow',STATE,'--root',ROOT);cli('jobs-final','jobs',STATE,'--root',ROOT);cli('inspection-final','inspection',STATE,'--root',ROOT)
 d=decode();save('state-final.json',d);idx={r['id']:r for r in d['records']};parsed=codec.parse(Path(STATE).read_bytes())
 scopes={}
 for k in ['working','retry','paused','delivery']:
  seed=PREFIX+'.'+k+'.'+('output' if k=='delivery' else 'candidate');scope=graph.proof_scope(parsed,[seed]);ss=[{'id':s,**idx[s]['fields']} for s in sorted(scope) if idx[s]['kind']=='S'];assert not any(s['id'].startswith('successor.source.') or s['at']=='2026-11-09T20:00:00+00:00' for s in ss);scopes[k]={'seed':seed,'source_records':ss,'unsupported_future_sources':[]}
 save('source-closure.json',{'scope':'Current selected member candidate/output criterion scopes and new collective output scope; historical old records intentionally remain','checked_at':now(),'scopes':scopes})
 before=read(W/'state-before.json');changed=[r['id'] for r in before['records'] if idx[r['id']]!=r and r['id']!='project'];assert not changed,changed
 files=read(W/'preservation-before.json');drift=[p for p,h in files.items() if not Path(p).is_file() or sha(p)!=h];assert not drift,drift
 oldj=read(W/'plar-before.json');newj=read('authoring-plar.txt')
 def semantic(j):
  j=copy.deepcopy(j)
  for a in j['assets']:
   for f in ['production','status','next','evidence']:a.pop(f,None)
  return j
 assert semantic(oldj)==semantic(newj)
 preservation={'old_files_checked':len(files),'changed_old_files':drift,'old_records_checked':len(before['records']),'changed_old_records_except_project_intake_append':changed,'project_change':'Only appended new confirmed destination choice to project.in','plar_semantics_identical':True,'requirements_hashes':reqs,'public_operations_only':True,'no_global_settings_or_memory_writes':True}
 save('preservation-final.json',preservation)
 def artifact(p):
  if p=='work/provenance-correction/request-review-coverage.json':p='work/provenance-correction/request-review-coverage-corrected.json'
  return {'path':p,'sha256':sha(p)}
 result={'version':1,'status':'completed','scope':'Bounded caller provenance correction complete; art production remains partial. No new generated-art quality or general host reliability evidence.','assignment':artifact('PROVENANCE-CORRECTION.md'),'erratum':artifact('work/provenance-correction/erratum.json'),'actual_observed_time':read(W/'erratum.json')['observed_at'],'old_to_new_source_mapping':read(W/'erratum.json')['records'],'plan':{'id':PREFIX+'.plan','authored':artifact('work/provenance-correction/public-plan.json'),'publication':artifact('work/provenance-correction/production-plan.json'),'exact_request_review':artifact('work/provenance-correction/request-review.json'),'independent_comparison':artifact('work/provenance-correction/caller-comparison.json'),'coverage':artifact('work/provenance-correction/request-review-coverage.json')},'current_source_closure':artifact('work/provenance-correction/source-closure.json'),'continuity':artifact('work/provenance-correction/continuity.json'),'candidates':{k:{'id':PREFIX+'.'+k+'.candidate','fields':idx[PREFIX+'.'+k+'.candidate']['fields'],'task':idx[PREFIX+'.'+k+'.task'],'verdicts':[r for r in d['records'] if r['kind']=='V' and r['fields']['tk']==ref(PREFIX+'.'+k+'.task')]} for k in ['working','retry','paused']},'plar':{'path':'authoring-plar.txt','sha256':sha('authoring-plar.txt'),'requirements_hashes':reqs,'semantics_unchanged':True},'handoffs':handoffs,'state':{'path':STATE,'revision':d['revision'],'sha256':sha(STATE)},'preservation':artifact('work/provenance-correction/preservation-final.json'),'retained_prior_result':artifact('SUCCESSOR-RESULT.json'),'verification':{'validation':artifact('work/provenance-correction/validation-final.json'),'family':artifact('work/provenance-correction/family-final.json'),'workflow':artifact('work/provenance-correction/workflow-final.json'),'levels':'Public operation/schema/bindings and continuity of retained actual outcome evidence verified. No fresh model behavioral trial, image viewing, render execution or generation.'},'unchanged_acceptance_gap':{'working':'provenance.working.motion.unavailable: direct real-time qualitative playback/pacing/wrap review at1x/3x still unavailable','family':'Open; no candidate, snapshot or collective acceptance. All3 collective checks unperformed.','next_action':'Appraise exact Working normal100ms playback; record superseding scoped visual review if justified, complete Working, then snapshot and review collective copied family and destination.'}}
 save('PROVENANCE-RESULT.json',result);print(json.dumps({'result':'work/provenance-correction/PROVENANCE-RESULT.json','sha256':sha(W/'PROVENANCE-RESULT.json'),'revision':d['revision'],'preservation':preservation}))
if __name__=='__main__': globals()[sys.argv[1]]()
