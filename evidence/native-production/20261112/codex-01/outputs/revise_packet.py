import json,hashlib
from pathlib import Path
w=Path('work/native-production')
def save(n,v):
 p=w/n;p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');return {'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
p=json.loads((w/'request-review-01.json').read_text())
c=json.loads((w/'candidate-plan-01.json').read_text())
for q in c['outputs'][0]['criteria']:
 for s in q['sources']:
  if s['path']=='NATIVE-PRODUCTION.md' and s.get('lines')==[34,38]:s['lines']=[34,39];s['locator']='lines 34-39'
p['criteria']=save('candidate-plan-02.json',c)
print(save('request-review-02.json',p))
