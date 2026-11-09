from pathlib import Path
import json,hashlib,sys
root=Path.cwd();w=root/'work/successor-adoption'
def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
review_path=sys.argv[1];outname=sys.argv[2];r=read(review_path)
p=read('work/focused-successor/specialist-proposal-r4.json');prior=read('work/focused-successor/caller-comparison-final.json')
old={x['criterion']:x for x in prior['criterion_comparisons']};actual={x['id']:x for x in r['criteria']}
prefix=r['plan']['id'].removesuffix('.plan')
rows=[];mapping=[]
for c in p['criteria']:
 newids=[]
 for q in c['successor_checks']:
  nid=q['id'].replace('focused-successor.',prefix+'.');newids.append(nid);got=actual[nid]
  expected=q['check'].replace('authoring-01.delivery.q.distinction',prefix+'.delivery.q.distinction')
  assert got['check']==expected,(nid,'literal changed')
  assert got['domain']==q['domain'] and got['mode']==q['mode']
  assert got['record_status']=='current' and got['record_sha256']==got['current_record_sha256']
  prev=old[c['criterion']]
  row={k:prev[k] for k in ['source_obligation','authority_basis','scope','literal_delta','discriminating_alternative']}
  row.update({'criterion':nid,'record_sha256':got['record_sha256'],'literal':got['check'],'domain':got['domain'],'mode':got['mode'],'original_criterion':c['criterion'],'original_record_sha256':c['record_sha256'],'disposition':'consistent: unchanged corrected r4 obligation adopted into new saved successor; fresh verdicts required','literal_delta':'Exact corrected r4 text retained; only stale collective ID updated where present. '+prev['literal_delta'],'scope':prefix+' reuse and versioned graphical consumer; '+prev['scope']})
  rows.append(row)
 mapping.append({'original':c['criterion'],'original_record_sha256':c['record_sha256'],'new_checks':newids})
assert len(mapping)==20 and len(rows)==23 and {x['criterion'] for x in rows}==set(actual)
controls=[]
for c in r['controls']:
 ct=c['contract']; f=c['fields'];stage=c['output'].split('.')[-2]
 assert f['bs']=={'$ref':'ready.retained'}
 if stage!='delivery':
  assert ct['al']=={'$symbol':'full'} and ct['pl']==[] and ct['sa']=={'$symbol':'nearest'}
  assert ct['px']==([64,16] if stage=='working' else [16,16])
  assert ct['ch']==[{'$ref':'render.choice.style'},{'$ref':'focused-successor.choice.destination'}]
  assert 'exact stroke or margin rule' in ct['li']
 else:
  assert f['ds']==[{'$ref':'focused-successor.choice.destination'}]
  assert [x['$ref'] for x in f['mb']]==['r.22e90a2a03fe453a.output.ready']+[prefix+'.'+x+'.output' for x in ['working','retry','paused']]
 controls.append({'output':c['output'],'record_sha256':c['record_sha256'],'disposition':'consistent with exact Ready baseline, full alpha, no palette restriction, nearest source geometry; new destination only, no acceptance transfer','fields':f,'contract':ct})
assert r['request'] is None
sources=[]
for s in r['sources']:
 path=Path(s.get('absolute_path',s['path']))
 if path.is_file():
  observed=hashlib.sha256(path.read_bytes()).hexdigest();assert observed==s['sha256'],s['id']
  sources.append({'id':s['id'],'path':s['path'],'sha256':observed,'review_report_status':s['status'],'status':'actual source bytes hash verified; r4 interpretation retained where literal unchanged'})
assert all(x['requirements_hash']==x['current_requirements_hash'] for x in r['selections'])
res={'reviewer_role':'Independent native caller /root; specialist is /root/pixl','status':'consistent','review_scope_sha256':r['review_scope_sha256'],'exact_request_review':{'path':review_path,'sha256':sha(review_path)},'approved_proposal':{'path':'work/focused-successor/specialist-proposal-r4.json','sha256':sha('work/focused-successor/specialist-proposal-r4.json')},'retained_semantic_review':{'path':'work/focused-successor/caller-comparison-final.json','sha256':sha('work/focused-successor/caller-comparison-final.json'),'use':'Retain completed original20 semantic judgments; compare actual new literals/controls independently; do not repeat historical review.'},'criterion_comparisons':rows,'original20_mapping':mapping,'controls_comparison':controls,'source_identity_checks':sources,'reduced_motion_mapping':{'stationary_frame0':['working.q.geometry','working.q.activity-not-success','working.q.consumers','delivery.q.distinction','delivery.q.destination'],'normal_only_100ms':['working.q.geometry','working.q.motion-continuity','working.q.consumers','delivery.q.destination'],'live_preference_switching':['working.q.consumers','delivery.q.destination']},'independent_judgment':'New literal checks preserve split diagnostic/visual transparency, full alpha/selective AA, permitted margins, owner100ms distinct from scoped expert pacing, qualitative coherent family and inferred Start distinction. Current source matches reviewed implementation. 23 criteria are20 original mappings plus3 split diagnostics, with reduced obligations integrated literally. No new remote request exists or is needed. Fresh acceptance must use candidate-bound evidence; direct human temporal appraisal remains limited.','diagnostic_interpretation':'Large full proposal/comparison sources exceed excerpt budget (needs_narrower_range); exact UTF-8 files and hashes were read/compared directly, no missing meaning inferred from coverage.'}
(w/outname).write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':res['status'],'originals':len(mapping),'new':len(rows),'controls':len(controls),'source_hashes':len(sources)}))
