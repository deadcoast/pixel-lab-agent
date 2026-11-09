"""PIXL round-1 preliminary views and measurements of the held Working cell versus Ready/Paused/Retry.
Writes only under work/continuation/round1-views. Measurements are facts; views are for the specialist's own viewing; nothing here is acceptance."""
import json, hashlib, sys
from pathlib import Path
from PIL import Image
root = Path(sys.argv[1]); out = root / 'work/continuation/round1-views'; out.mkdir(parents=True, exist_ok=True)
PANEL = (0x17, 0x23, 0x36, 255)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p): return Image.open(root / p).convert('RGBA')
sheet = load('assets/working.png'); ready = load('assets/ready-confirmed.png'); paused = load('assets/paused.png'); retry = load('assets/error-retry.png')
seed = load('.pixl/assets/queue.ready/artifacts/21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png')
cells = [sheet.crop((i*16, 0, (i+1)*16, 16)) for i in range(4)]
def comps(im):
    px = im.load(); w,h = im.size; seen=set(); res=[]
    for y in range(h):
        for x in range(w):
            if px[x,y][3]>0 and (x,y) not in seen:
                st=[(x,y)]; seen.add((x,y)); n=0; xs=[];ys=[]
                while st:
                    cx,cy=st.pop(); n+=1; xs.append(cx); ys.append(cy)
                    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                        nx,ny=cx+dx,cy+dy
                        if 0<=nx<w and 0<=ny<h and (nx,ny) not in seen and px[nx,ny][3]>0: seen.add((nx,ny)); st.append((nx,ny))
                res.append({'pixels':n,'box':[min(xs),min(ys),max(xs)+1,max(ys)+1]})
    return res
def hist(im):
    h={}
    for p in im.getdata(): h[str(p[3])]=h.get(str(p[3]),0)+1
    return h
def lum(rgb): return round(0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2],1)
def visible_lums(im):
    return sorted({lum(p[:3]) for p in im.getdata() if p[3]>0})
def cw(im):  # dst(x,y)=src(y,15-x)
    o=Image.new('RGBA',(16,16)); s=im.load(); d=o.load()
    for y in range(16):
        for x in range(16): d[x,y]=s[y,15-x]
    return o
def same_visible(a,b):
    pa,pb=a.load(),b.load()
    for y in range(16):
        for x in range(16):
            if pa[x,y][3]!=pb[x,y][3]: return False
            if pa[x,y][3]>0 and pa[x,y]!=pb[x,y]: return False
    return True
def centroid(im):
    px=im.load(); xs=0;ys=0;n=0
    for y in range(16):
        for x in range(16):
            if px[x,y][3]>0: xs+=x+0.5; ys+=y+0.5; n+=1
    return [round(xs/n,3), round(ys/n,3)]
def gaps(im):
    """rows/cols of the inner empty area: count fully transparent rows/cols inside the visible box"""
    px=im.load(); b=comps(im); xs=[c['box'][0] for c in b]+[c['box'][2] for c in b]; ys=[c['box'][1] for c in b]+[c['box'][3] for c in b]
    l,t,r,bt=min(xs),min(ys),max(xs),max(ys)
    empty_center = all(px[x,y][3]==0 for x in range(6,10) for y in range(6,10))
    return {'visible_box':[l,t,r,bt],'centre_4x4_transparent':empty_center}
meas = {'convention':'zero-based pixel indices; boxes half-open [left,top,right,bottom]; centroid in pixel-edge coordinates (index+0.5); 4-connectivity on alpha>0; luminance = Rec.709 of RGB on alpha>0 pixels; panel #172336 luminance %s' % lum(PANEL[:3]), 'images':{}}
meas['images']['assets/working.png']={'sha256':sha(root/'assets/working.png'),'size':sheet.size,'alpha_histogram':hist(sheet)}
for i,c in enumerate(cells):
    meas['images'][f'working cell {i}']={'components':comps(c),'alpha_histogram':hist(c),'centroid_edge':centroid(c),'visible_lums':visible_lums(c), **gaps(c)}
meas['cells_1_3_equal_cw_k_cell0_alpha_and_visible_rgba']=[same_visible(cells[k], (lambda im,k: [im:=cw(im) for _ in range(k)][-1] if k else im)(cells[0],k)) for k in range(1,4)]
meas['cell0_equals_seed_alpha_and_visible_rgba']=same_visible(cells[0],seed)
meas['seed_sha256']=sha(root/'.pixl/assets/queue.ready/artifacts/21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png')
for name,im,p in (('ready',ready,'assets/ready-confirmed.png'),('paused',paused,'assets/paused.png'),('retry',retry,'assets/error-retry.png')):
    meas['images'][p]={'sha256':sha(root/p),'size':im.size,'components':comps(im),'alpha_histogram':hist(im),'centroid_edge':centroid(im),'visible_lums':visible_lums(im), **gaps(im)}
# Retry inner structure: transparent pixels inside its bbox (ring openness)
rp=retry.load(); inner=[(x,y) for y in range(2,14) for x in range(3,13) if rp[x,y][3]==0]
meas['retry_transparent_pixels_inside_bbox']=len(inner)
# views: W0, Retry, Ready, Paused on panel, 1x and 3x, colour and grayscale; plus 12x grid of W0 and Retry
def on_panel(im): bg=Image.new('RGBA',im.size,PANEL); return Image.alpha_composite(bg,im)
def strip(ims, scale, gray=False, gap=4):
    w=16*scale; sheet=Image.new('RGBA',(len(ims)*w+(len(ims)+1)*gap, w+2*gap), PANEL)
    for i,im in enumerate(ims):
        t=on_panel(im).resize((w,w),Image.NEAREST)
        if gray: t=t.convert('L').convert('RGBA')
        sheet.paste(t,(gap+i*(w+gap),gap))
    return sheet
order=[cells[0],retry,ready,paused,cells[1],cells[2],cells[3]]
files={}
for scale in (1,3,12):
    for gray in (False,True):
        n=f"w0-retry-ready-paused-w1-w2-w3-{scale}x-{'gray' if gray else 'color'}.png"
        strip(order,scale,gray).save(out/n); files[n]=sha(out/n)
meas['views']={k:{'path':f'work/continuation/round1-views/{k}','sha256':v} for k,v in files.items()}
meas['view_order']='left to right: Working cell 0 (held), Retry, Ready, Paused, Working cells 1,2,3; each on #172336 with 4 px panel gutters; nearest-neighbour'
(out/'round1-measurements.json').write_text(json.dumps(meas,indent=1),encoding='utf-8')
print(json.dumps(meas,indent=1))
