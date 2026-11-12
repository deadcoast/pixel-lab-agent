from PIL import Image,ImageOps
from pathlib import Path
import json,hashlib
w=Path('work/native-production'); d=w/'render-01'; p=json.loads((d/'render.json').read_text())
files=[]
for v in p['views']:
 if v['state'] not in ['running','paused','succeeded','failed']:continue
 src=d/v['image']['path']; out=w/('gray-'+v['image']['path'])
 ImageOps.grayscale(Image.open(src).convert('RGB')).save(out)
 files.append({'source':src.as_posix(),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'path':out.as_posix(),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'consumer':v['consumer'],'state':v['state'],'scale':v['scale']})
ImageOps.grayscale(Image.open(d/'destination.png').convert('RGB')).save(w/'destination-gray-01.png')
(w/'grayscale-derivation-01.json').write_text(json.dumps({'method':'Pillow ImageOps.grayscale of exact actual renderer cell captures; no geometry or resampling changes','files':files},indent=2)+'\n')
print(json.dumps(files))
