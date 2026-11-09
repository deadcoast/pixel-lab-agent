import hashlib, json, sys, io, os
from pathlib import Path
src = Path(sys.argv[1])
dst = Path('work/export-review-01/request-review-raw.txt')
b = src.read_bytes()
dst.write_bytes(b)
print('spilled bytes', len(b), 'sha256', hashlib.sha256(b).hexdigest(), 'copied sha256', hashlib.sha256(dst.read_bytes()).hexdigest())
print('first bytes', b[:60])
print('non-ascii bytes', sum(1 for x in b if x > 127), 'has BOM', b[:3]==b'\xef\xbb\xbf', 'CRLF count', b.count(b'\r\n'), 'LF count', b.count(b'\n'))
new = json.loads(b.decode('utf-8'))
old_raw_b = Path('work/criteria-review-01/request-review-raw.txt').read_bytes()
print('old raw bytes', len(old_raw_b), 'sha256', hashlib.sha256(old_raw_b).hexdigest(), 'non-ascii', sum(1 for x in old_raw_b if x>127))
old = json.loads(old_raw_b.decode('utf-8'))
print('top keys new', list(new.keys()))
print('top keys old', list(old.keys()))

def diff(a, b, path, out):
    if type(a) != type(b):
        out.append((path, 'type', repr(a)[:200], repr(b)[:200])); return
    if isinstance(a, dict):
        for k in sorted(set(a)|set(b)):
            if k not in a: out.append((path+'/'+k, 'added', None, repr(b[k])[:300]))
            elif k not in b: out.append((path+'/'+k, 'removed', repr(a[k])[:300], None))
            else: diff(a[k], b[k], path+'/'+k, out)
    elif isinstance(a, list):
        if len(a)!=len(b): out.append((path, 'len', len(a), len(b)))
        for i,(x,y) in enumerate(zip(a,b)): diff(x,y,path+'/%d'%i,out)
    else:
        if a!=b: out.append((path,'value',repr(a)[:300],repr(b)[:300]))
out=[]
diff(old,new,'',out)
print('DIFF count', len(out))
for d in out: print(d)
json.dump({'spilled_source': str(src), 'spilled_sha256': hashlib.sha256(b).hexdigest(), 'spilled_bytes': len(b), 'old_raw_sha256': hashlib.sha256(old_raw_b).hexdigest(), 'differences': [{'path':p,'kind':k,'old':o,'new':n} for p,k,o,n in out]}, io.open('work/export-review-01/raw-vs-prior-raw-diff.json','w',encoding='utf-8'), indent=1, ensure_ascii=False)
