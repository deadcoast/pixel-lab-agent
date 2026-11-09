from pathlib import Path
import json,hashlib,io,base64
from PIL import Image,ImageChops
root=Path.cwd();w=root/'work/successor-adoption';cap=w/'render-01'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
bg=(23,35,54,255)
checks=[]
def compare(actual,path,frame,scale):
 with Image.open(root/path) as im:
  tile=im.convert('RGBA').crop((frame*16,0,(frame+1)*16,16))
 expected=Image.alpha_composite(Image.new('RGBA',(16,16),bg),tile).resize((16*scale,16*scale),Image.Resampling.NEAREST)
 d=ImageChops.difference(expected,actual.convert('RGBA')).convert('RGB')
 assert max(x[1] for x in d.getextrema())<=1
 checks.append({'path':path,'frame':frame,'scale':scale,'max_rgb_error':max(x[1] for x in d.getextrema())})
motion=read(cap/'motion.json');transitions=[]
for phase in motion['phases']:
 for sample in phase['samples']:
  for c in sample['cells']:
   compare(Image.open(cap/c['image']['path']),c['path'],c['frame'],3)
  for c in sample['matrixWorking']:
   compare(Image.open(io.BytesIO(base64.b64decode(c['png'].split(',')[1]))),'renderer-successor/assets/working.png',c['frame'],c['scale'])
 seq=[]
 for sample in phase['samples']:
  f=sample['cells'][0]['frame']
  if not seq or f!=seq[-1]['frame']:seq.append({'frame':f,'observed_at_ms':sample['at']})
 if not phase['reduced']:
  assert all(b['frame']==(a['frame']+1)%4 for a,b in zip(seq,seq[1:]))
  assert any(a['frame']==3 and b['frame']==0 for a,b in zip(seq,seq[1:]))
 transitions.append({'phase':phase['name'],'transitions':seq,'sample_gap_max_ms':max(b['at']-a['at'] for a,b in zip(phase['samples'],phase['samples'][1:])),'observed_inter_transition_ms':[b['observed_at_ms']-a['observed_at_ms'] for a,b in zip(seq[1:],seq[2:])]})
r=read(cap/'reduced-render.raw.json')
for v in r['views']:
 actual=Image.open(io.BytesIO(base64.b64decode(v['png'].split(',')[1])))
 if v['descriptor']['path'].endswith('.png'):compare(actual,v['descriptor']['path'],0,v['scale'])
for t in r['timeline']:
 compare(Image.open(io.BytesIO(base64.b64decode(t['png'].split(',')[1]))),'renderer-successor/assets/working.png',0,1)
result={'status':'pass','source_pixel_comparisons':len(checks),'comparisons':checks,'live_transition_observations':transitions,'scope':'Actual sampled painted pixels compared against source crops/composites, tolerance one RGB level; normal sequential wrap observed, reduced stationary frame0. Nominal 100ms cadence is boundary arithmetic, wall-clock sampling quantizes observed transitions; no exact compositor scheduling or direct human real-time pacing claim.','inputs':{n:sha(cap/n) for n in ['render.json','motion.json','reduced-render.raw.json']}}
(w/'live-pixels-and-timing.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'source_pixel_comparisons':len(checks),'transitions':transitions}))
