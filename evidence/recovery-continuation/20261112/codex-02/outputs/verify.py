import json, hashlib
from pathlib import Path
from PIL import Image
p=Path('work/provider-recovery/phase-2')
r=json.loads((p/'provider-result.json').read_text())
b=(p/'retrieved.png').read_bytes()
i=r['images'][0]
assert len(b)==i['bytes']
assert hashlib.sha256(b).hexdigest()==i['sha256']
with Image.open(p/'retrieved.png') as im:
    assert im.format=='PNG'
    im.verify()
with Image.open(p/'retrieved.png') as im:
    im.load()
    assert im.size==(i['width'],i['height'])
    result=dict(provider_simulated=True,path=str(p/'retrieved.png').replace('\\','/'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),format=im.format,width=im.width,height=im.height,mode=im.mode,decode='pass')
(p/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
