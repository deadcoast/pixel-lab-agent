import json,subprocess,hashlib,copy
from pathlib import Path
from PIL import Image
O=Path('work/artistic-revision');PY='C:/github/pixel-lab-agent/.venv/Scripts/python.exe';RUN='.agents/skills/artistic-revision-kit/scripts/pixl.py';S='.pixl/assets/queue.ready'
def call(*a):
 p=subprocess.run([PY,RUN,*a],capture_output=True,text=True,encoding='utf-8');
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
 return json.loads(p.stdout)
d=call('decode',S+'/state.px');b={r['id']:r for r in d['records']}
for kind in ['working','retry','paused']:
 r=copy.deepcopy(b['artistic.'+kind+'.candidate']);r['id']='artistic2.'+kind+'.candidate';r['fields']['of']={'$ref':'artistic-02.'+kind+'.output'};d['records'].append(r)
d['revision']+=1;(O/'candidate-document-plan02.json').write_text(json.dumps(d,indent=2));a=call('commit',S,str(O/'candidate-document-plan02.json'),'--json','--expect',json.loads((O/'production-plan-02.json').read_text())['hash'],'--root',str(Path.cwd()));(O/'commit-candidates-plan02.json').write_text(json.dumps(a,indent=2))
# Retain actual temporally sampled exposures as a sequence montage, not synthetic playback.
r=json.loads((O/'capture-switch-04/render.json').read_text());items=[];observations=[]
for phase in r['phases']:
 samples=[x for x in phase['report']['playback'] if x['consumer']=='statusCell' and x['scale']==3]
 selected=[samples[0]]
 for row in samples[1:]:
  if row['frame']!=selected[-1]['frame']:selected.append(row)
 canvas=Image.new('RGB',(len(selected)*52,64),'#172336')
 for i,row in enumerate(selected):canvas.paste(Image.open(O/'capture-switch-04'/row['image']['path']).convert('RGB'),(i*52,8))
 p=O/('observed-sequence-'+phase['name']+'.png');canvas.save(p);observations.append({'phase':phase['name'],'path':str(p).replace('\\','/'),'rows':selected,'scope':'Actual ordered canvas exposures, includes measured paint and exposure timestamps; no synthetic reconstruction.'})
(O/'observed-sequences.json').write_text(json.dumps(observations,indent=2))
print(a['hash'])
