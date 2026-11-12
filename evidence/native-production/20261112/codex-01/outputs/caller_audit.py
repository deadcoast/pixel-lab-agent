from pathlib import Path
import json, hashlib, base64
from PIL import Image, ImageOps
root=Path.cwd()
def read(p): return json.loads((root/p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((root/p).read_bytes()).hexdigest()
def ref(p,role): return dict(path=p,sha256=sha(p),role=role)
s=read('work/native-production/SPECIALIST-RESULT.json')
h=read(s['handoff_ref']['full']['path'])
c=read('work/native-production/caller-handoff-01.json')
selraw=read('work/native-production/caller-final-selection.json')
sel=selraw.get('structuredContent') or json.loads(selraw['content'][0]['text'])
checks=[]
def check(name,ok,detail=None): checks.append(dict(check=name,passed=bool(ok),detail=detail))
def walk(x):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x and (root/x['path']).is_file(): check('file identity '+x['path'],sha(x['path'])==x['sha256'])
  for v in x.values(): walk(v)
 elif isinstance(x,list):
  for v in x: walk(v)
walk(s); walk(h); walk(c)
a=read('work/native-production/provider-arguments-01.json')
sub=read('work/native-production/provider-submit-01.json')
dispatch=read('work/native-production/dispatch-result-01.json')['structuredContent']
get=read('work/native-production/provider-get-01.json')
check('reviewed dispatch and actual submitted arguments equal',a==sub['arguments']==dispatch['dispatch_request']['arguments'])
preview=next(v for v in get['content'] if v['type']=='image')
check('provider returned image equals downloaded bytes',hashlib.sha256(base64.b64decode(preview['data'])).hexdigest()==sha('work/native-production/ready-generated-01.png'))
check('exact delivered bytes',sha('assets/ready-confirmed.png')==sha('work/native-production/ready-generated-01.png'))
check('fresh selected requirements and state match handoff',sel['requirements_hash']==c['requirements_hash']==h['requirements_hash'] and sel['production']['continuation']['state_hash']==c['state_hash']==h['resume']['state_hash'])
check('completed delivery with no pending jobs',sel['production']['delivery']['complete'] and not sel['production']['pending_jobs'] and c['production']['task_state']=='done' and c['production']['criteria']['by_status']=={'pass':9})
for x in read('work/native-production/caller-preservation-baseline.json'): check('protected '+x['path'],sha(x['path'])==x['sha256'])
for x in read('work/native-production-inputs/origin.json')['files'].items():
 if x[0]!='assets/ready-confirmed.png': check('origin closure '+x[0],sha(x[0])==x[1])
for x in read('work/native-production/grayscale-derivation-01.json')['files']:
 check('grayscale mapping '+x['path'],sha(x['source'])==x['source_sha256'] and sha(x['path'])==x['sha256'] and ImageOps.grayscale(Image.open(root/x['source'])).tobytes()==Image.open(root/x['path']).tobytes())
report=dict(status='pass' if all(x['passed'] for x in checks) else 'fail',checks=checks,failures=[x for x in checks if not x['passed']])
(root/'work/native-production/caller-identity-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(dict(status=report['status'],checks=len(checks),failures=report['failures'])))
