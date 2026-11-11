from operations import *
# Codec is used only to compute declared record identities; all state publication
# and production operations below use the frozen public CLI with retained returns.
sys.path.insert(0,str(ROOT/'installed pixl/runtime'))
from pixl.codec import Record, record_hash
from pixl.service import from_data
d=read('work/integration-change/adoption-document.json')
decision=next(r for r in d['records'] if r['id']=='adopt.working150')
decision['fields']['pc']=[{'$ref':'adoption.proof150'}]
bindings=[]
for row in d['records']:
 if row['kind'] not in 'EPTJNV':bindings.append({'rf':{'$ref':row['id']},'dg':record_hash(Record(row['id'],row['kind'],from_data(row['fields'])))})
proof=save('adoption-proof-observation.json',{'scope':'Scoped adoption following fresh accepted sample review','sample_review':{'path':'work/integration-change/sample-review.json','sha256':sha('work/integration-change/sample-review.json')},'sample':'working.reused150','decision':'adopt.working150','basis':'Exact art reuse mandated; fresh local/visual/live review passed current150ms criteria','limitations':['Controlled timing integration only; no new art or provider quality claim']})
d['records'].append({'id':'adoption.proof150','kind':'E','fields':{'nm':'Executed fresh sample review supporting scoped adoption','ur':proof,'dg':sha(proof),'rs':{'$symbol':'pass'},'md':{'$symbol':'local'},'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bs':bindings}})
cp=save('adoption-document-corrected.json',d)
op('adoption-commit-corrected.json','commit',STORE,cp,'--json','--expect',state(),'--root',ROOT)
ctx=read('work/integration-change/sample-context.json')
sources=next(r for r in d['records'] if r['id']==ctx['criteria'][0]['id'])['fields']['so']
plan={'version':1,'id':'working150.delivery','project':'project','actor':'actor','baseline':'working.reused150','decisions':['adopt.working150'],'knowledge':[],'stages':[],'delivery':{'name':'Controlled current150ms Working integration','members':[ctx['output']],'destinations':['destination.working150'],'criteria':[{'id':'continuity','check':'Exact reused Working member preserves accepted segmented cool-blue activity treatment and remains distinct by silhouette from retained Ready, Retry and Paused at1x/3x in both consumers.','domain':'continuity','mode':'visual','sources':[s['$ref'] for s in sources]},{'id':'timing','check':'Exact package member is served at assets/working.png in both actual consumers with four150ms looping frames,600ms cycle, nearest3x live playback and1x/3x still inspection, transparent compositing.','domain':'engine','mode':'live','sources':[s['$ref'] for s in sources]}]}}
pp=save('delivery-plan.json',plan)
result=op('delivery-plan-result.json','production-plan',STORE,pp,'--expect',state(),'--root',ROOT)
print(json.dumps(result,indent=2))
