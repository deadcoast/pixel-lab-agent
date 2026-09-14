from pathlib import Path
from PIL import Image
import json

root=Path(__file__).resolve().parents[1]
ref=Image.open(root/'reference.png').convert('RGBA')
cand=Image.open(root/'candidate.png').convert('RGBA')
groups={}
for y in range(32):
    for x in range(32):
        a,b=ref.getpixel((x,y)),cand.getpixel((x,y))
        if a!=b:
            key=str(a)+' -> '+str(b)
            groups.setdefault(key,[]).append((x,y))
result=[]
for change,coords in groups.items():
    xs,ys=zip(*coords)
    result.append({'change':change,'count':len(coords),'bbox_inclusive':[min(xs),min(ys),max(xs),max(ys)],'pixels':coords})
out={'coordinate_convention':'zero-based x,y; bounding boxes inclusive','changed_pixels':sum(x['count'] for x in result),'changes':result,'scope':'Exact pixel comparison corroborates the visually observed missing landmarks; pixel difference alone is not an identity verdict.'}
(root/'review/difference.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({**out,'changes':[{k:v for k,v in x.items() if k!='pixels'} for x in result]}))
