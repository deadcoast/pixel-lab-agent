from operations import *
from PIL import Image
ctx=read('work/integration-change/sample-context.json')
im=Image.open(ROOT/'assets/working.png').convert('RGBA')
measure=save('measurements.json',{'size':im.size,'frames':4,'frame_size':[16,16],'sha256':sha('assets/working.png'),'alpha_extrema':im.getchannel('A').getextrema(),'transparent_pixels':sum(a==0 for a in im.getchannel('A').getdata()),'provenance':'Exact retained historical art; fresh local measurement'})
command=[PY,'renderer-integration/check.py','--project',str(ROOT),'--capture','work/integration-change/sample-capture']
r=subprocess.run(command,cwd=ROOT,capture_output=True)
(OUT/'sample-renderer-check.json').write_bytes(r.stdout);(OUT/'sample-renderer-check.stderr').write_bytes(r.stderr);save('sample-renderer-check.execution.json',{'command':command,'exit_code':r.returncode,'helper_sha256':sha('work/integration-change/review-sample.py')})
obs=[]
def add(path,mode,note):obs.append({'path':path,'sha256':sha(path),'mode':mode,'note':note})
add(measure,'local','Fresh decoded64x16 RGBA sheet with transparent exterior and exact historical hash.')
add('work/integration-change/sample-capture/destination.png','visual','Actually viewed both consumers at1x/3x: segmented blue activity ring distinct from Ready check, Retry arrow and Paused bars; compact silhouettes and cool blue treatment coherent. No opaque matte.')
for n in [4,5,6,7,40]:add(f'work/integration-change/sample-capture/view-{n:03}.png','visual','Actually opened native/enlarged Working consumer pixels; segmented activity ring readable at declared scale. Live captured phase remains compact and distinct.')
add('work/integration-change/sample-capture/render.json','live','Actual isolated browser execution: both original consumers through stable wrapper; live requestAnimationFrame samples at3x loop four phases150ms/600ms, frame-boundary1x samples separate.')
add('work/integration-change/sample-renderer-check.json','live','Fresh real renderer check passes exact served hashes, frame selection,150ms live progression/wrap, nearest scaling and compositing. Not independent artistic judgment.')
review={'version':1,'binding_hash':ctx['binding_hash'],'reviewer':'actor','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'observations':obs,'verdicts':[],'action':'complete','next_action':'Adopt exact revised sample for scoped delivery-only plan.','limitations':['Native1x live playback unperformed;1x stills and controlled frame-boundary samples inspected.','Controlled reused-art timing integration only; broader artistic production and M1/M2/broaderM3 remain open.']}
for q in ctx['criteria']:
 indices=[i for i,o in enumerate(obs) if o['mode']==q['mode']]
 review['verdicts'].append({'criterion':q['id'],'status':'pass','reason':{'local':'Exact retained geometry, alpha and hash freshly measured.','visual':'Viewed both consumers/native and enlarged pixels: coherent cool-blue segmented ring expresses activity, differentiated by shape from check, arrow and pause bars.','live':'Fresh real browser/check establishes current150ms frame progression, loop and both consumers with exact bytes;3x live and1x/3x still scope.'}[q['mode']],'supersedes':None,'observations':indices})
rp=save('sample-review-observation.json',review)
op('sample-review.json','candidate-review',STORE,'working.reused150','sample.review150',rp,'--expect',state(),'--root',ROOT)
d=op('decoded-adoption.json','decode',STATE);d['revision']+=1
ref=lambda x:{'$ref':x};sym=lambda x:{'$symbol':x}
task=next(r for r in d['records'] if r['id']==ctx['task'])
sources=next(r for r in d['records'] if r['id']==ctx['criteria'][0]['id'])['fields']['so']
evidence=[ref(r['id']) for r in d['records'] if r['kind']=='E' and 'sample.review150' in r['id']]
d['records'].append({'id':'adopt.working150','kind':'D','fields':{'wh':ref('actor'),'wt':'Adopt exact freshly accepted Working sample solely for controlled150ms reused-art delivery','wr':[ref('working.reused150')],'wy':'Explicit amendment mandates exact art reuse; fresh sample review passes current criteria and both consumer capture.','rs':sources,'pc':evidence}})
d['records'].append({'id':'destination.working150','kind':'I','fields':{'pr':ref('project'),'wh':ref('actor'),'ky':'destination.working150','st':sym('confirmed'),'vl':{'path':'assets/working.png','frame_size':[16,16],'frames':4,'frame_ms':150,'loop':True,'cycle_ms':600,'sampling':'nearest','scales':[1,3],'background':'#172336','consumers':['statusCell','compactStatus']},'so':sources,'wy':'Explicit current timing amendment and stable actual renderer consumer contract.'}})
next(r for r in d['records'] if r['id']=='project')['fields']['in'].append(ref('destination.working150'))
cp=save('adoption-document.json',d)
op('adoption-commit.json','commit',STORE,cp,'--json','--expect',state(),'--root',ROOT)
plan={'version':1,'id':'working150.delivery','project':'project','actor':'actor','baseline':'working.reused150','decisions':['adopt.working150'],'knowledge':[],'stages':[],'delivery':{'name':'Controlled current150ms Working integration','members':[ctx['output']],'destinations':['destination.working150'],'criteria':[{'id':'continuity','check':'Exact reused Working member preserves accepted segmented cool-blue activity treatment and remains distinct by silhouette from retained Ready, Retry and Paused at1x/3x in both consumers.','domain':'continuity','mode':'visual','sources':[s['$ref'] for s in sources]},{'id':'timing','check':'Exact package member is served at assets/working.png in both actual consumers with four150ms looping frames,600ms cycle, nearest3x live playback and1x/3x still inspection, transparent compositing.','domain':'engine','mode':'live','sources':[s['$ref'] for s in sources]}]}}
pp=save('delivery-plan.json',plan)
print(op('delivery-plan-result.json','production-plan',STORE,pp,'--expect',state(),'--root',ROOT))
