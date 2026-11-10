import json,hashlib,collections
from pathlib import Path
from PIL import Image
O=Path('work/artistic-revision');data={};seed=Image.open('.pixl/assets/queue.ready/artifacts/21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png').convert('RGBA')
def measure(im):
 pix=im.load();remaining={(x,y) for y in range(im.height) for x in range(im.width) if pix[x,y][3]>0};allpixels=remaining.copy();components=[]
 while remaining:
  stack=[remaining.pop()];part=[]
  while stack:
   xy=stack.pop();part.append(xy);x,y=xy
   for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if q in remaining:remaining.remove(q);stack.append(q)
  xs,ys=zip(*part);components.append({'count':len(part),'box':[min(xs),min(ys),max(xs)+1,max(ys)+1]})
 rgba=[]
 for color,n in collections.Counter(im.getdata()).items():
  coords=[(x,y) for y in range(im.height) for x in range(im.width) if pix[x,y]==color];xs,ys=zip(*coords);rgba.append({'rgba':color,'pixels':n,'box':[min(xs),min(ys),max(xs)+1,max(ys)+1]})
 return {'alpha_histogram':dict(collections.Counter(im.getchannel('A').getdata())),'components_4connected':sorted(components,key=lambda a:a['box']),'rgba_boxes':rgba,'visible_pixels':len(allpixels),'mass_centroid_pixel_edges':[sum(x+.5 for x,y in allpixels)/len(allpixels),sum(y+.5 for x,y in allpixels)/len(allpixels)],'diagnostic_flags':[p for p in components if p['count']>128 or p['box']==[0,0,16,16]],'flag_is_rejection':False}
for kind,path in [('working','assets/working.png'),('retry','assets/error-retry.png'),('paused','assets/paused.png')]:
 im=Image.open(path).convert('RGBA');frames=[im.crop((i*16,0,(i+1)*16,16)) for i in range(im.width//16)];rows=[]
 for i,frame in enumerate(frames):
  row=measure(frame)
  if kind=='working':
   rot=seed.rotate(-90*i);row['seed_rotation_alpha_equal']=frame.getchannel('A').tobytes()==rot.getchannel('A').tobytes();row['seed_rotation_visible_rgba_equal']=all(a[3]==b[3] and (a[3]==0 or a==b) for a,b in zip(frame.getdata(),rot.getdata()))
  rows.append(row)
 data[kind]={'path':path,'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'size':im.size,'frames':rows,'assembly':'No assembly: exact retained accepted art reused with new unaccepted candidate; acceptance evaluated freshly.'}
(O/'fresh-measurements.json').write_text(json.dumps(data,indent=2));print({k:[r['visible_pixels'] for r in v['frames']] for k,v in data.items()})
