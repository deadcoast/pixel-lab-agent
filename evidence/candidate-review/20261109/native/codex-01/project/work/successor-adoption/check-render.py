"""Independent caller comparison and reproducible mechanical analysis; UTF-8 only."""
from pathlib import Path
import json, hashlib, importlib.util, base64
from collections import Counter, deque
from PIL import Image, ImageChops

root=Path.cwd(); work=root/'work/successor-adoption'
def read(p): return json.loads((root/p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256((root/p).read_bytes()).hexdigest()
def save(name,obj): (work/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
spec=importlib.util.spec_from_file_location('successor_checker',root/'renderer-successor/check.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
pixels=module.check(root,work/'render-01');save('pixel-check.json',pixels)
assert pixels['status']=='pass',pixels['failures']
render=read('work/successor-adoption/render-01/render.json')
motion=read('work/successor-adoption/render-01/motion.json')
motion_results=[]
for phase in motion['phases']:
    times=[s['at'] for s in phase['samples']]
    each=[]
    for consumer in ['statusCell','compactStatus']:
        cells=[next(c for c in s['cells'] if c['consumer']==consumer) for s in phase['samples']]
        frames=sorted({c['frame'] for c in cells});hashes=sorted({c['image']['sha256'] for c in cells})
        assert all(c['state']=='running' and c['label']=='Working' and c['smoothing'] is False and c['width']==48 and c['height']==48 for c in cells)
        for c in cells:
            p=work/'render-01'/c['image']['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==c['image']['sha256']
        assert frames==([0] if phase['reduced'] else [0,1,2,3])
        assert len(hashes)==(1 if phase['reduced'] else 4)
        each.append({'consumer':consumer,'frames':frames,'pixel_hashes':hashes,'samples':len(cells)})
    assert all(not x['errors'] for x in phase['samples'])
    assert len(phase['samples'][-1]['changes']) == {'normal-before':0,'reduced-live':1,'normal-after':2}[phase['name']]
    if phase['reduced']:
        assert all(c['frame']==0 for x in phase['samples'] for c in x['matrixWorking'])
    assert times[-1]-times[0]>=800
    assert all(s['reduced']==phase['reduced'] for s in phase['samples'])
    assert all(s['cells'][0]['frame']==s['cells'][1]['frame'] for s in phase['samples'])
    motion_results.append({'phase':phase['name'],'reduced':phase['reduced'],'span_ms':times[-1]-times[0],'consumers':each,'preference_changes':phase['samples'][-1]['changes']})
reduced=read('work/successor-adoption/render-01/reduced-render.raw.json')
assert reduced['reduced'] is True and not reduced['missing'] and not reduced['errors']
assert all(v['frame']==0 for v in reduced['views'])
assert all(s['frame']==0 for s in reduced['timeline'])
assert len(reduced['views'])==20
save('motion-check.json',{'status':'pass','phases':motion_results,'reduced_all_states_views':20,'reduced_timeline_all_frame_zero':True,'all_backend_transitions':[t['event'] for t in reduced['transitions']], 'limits':'Actual browser rAF samples and CDP media emulation in one page; exact compositor scheduling and human temporal playback are not measured. 100ms phase arithmetic is independently checked at boundaries. No global preference changed.'})

# Alpha measurements remain diagnostics. Occupancy is never an artistic verdict.
diagnostics=[]
for name in ['working.png','paused.png','error-retry.png','ready-confirmed.png']:
    image=Image.open(root/'renderer-successor/assets'/name).convert('RGBA')
    frames=[]
    for i in range(image.width//16):
        frame=image.crop((i*16,0,(i+1)*16,16));points={(x,y) for y in range(16) for x in range(16) if frame.getpixel((x,y))[3]}
        components=[]
        while points:
            todo=[points.pop()]; component=[]
            while todo:
                x,y=todo.pop();component.append((x,y))
                for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if n in points:points.remove(n);todo.append(n)
            xs,ys=zip(*component);box=[min(xs),min(ys),max(xs)+1,max(ys)+1]
            components.append({'pixels':len(component),'box_half_open':box,'review_flag_only':len(component)>128 or box==[0,0,16,16]})
        frames.append({'frame':i,'alpha_histogram':dict(Counter(frame.getchannel('A').getdata())),'components_4_connected':components})
    diagnostics.append({'path':f'renderer-successor/assets/{name}','sha256':sha(f'renderer-successor/assets/{name}'),'size':list(image.size),'frames':frames})
save('alpha-diagnostics.json',{'measurements':diagnostics,'scope':'Nonzero-alpha 4-connected components; alpha-zero RGB ignored. Flag alone never rejects a matte, backing, margin, AA or artwork. Visual review decides intended exterior.'})


print(json.dumps({'pixels':pixels['status'],'checks':len(pixels['observations']),'motion_phases':len(motion_results),'reduced_views':len(reduced['views'])}))
