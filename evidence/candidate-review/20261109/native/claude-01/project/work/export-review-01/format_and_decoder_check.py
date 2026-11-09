import hashlib, json, io, sys
from pathlib import Path
raw_b = Path('work/export-review-01/request-review-raw.txt').read_bytes()
new = json.loads(raw_b.decode('utf-8'))
# formatted copy: explicit UTF-8, sorted keys, LF, ensure_ascii False (same convention as prior request-review.json claimed)
fmt = json.dumps(new, indent=2, sort_keys=True, ensure_ascii=False) + '\n'
out = Path('work/export-review-01/request-review.json')
out.write_bytes(fmt.encode('utf-8'))
re = json.loads(out.read_bytes().decode('utf-8'))
print('formatted sha256', hashlib.sha256(out.read_bytes()).hexdigest(), 'bytes', out.stat().st_size, 'parsed_equal_to_raw', re == new)
# Earlier formatted copy vs earlier raw
old_raw = json.loads(Path('work/criteria-review-01/request-review-raw.txt').read_bytes().decode('utf-8'))
old_fmt_b = Path('work/criteria-review-01/request-review.json').read_bytes()
old_fmt = json.loads(old_fmt_b.decode('utf-8'))
def diff(a, b, path, out):
    if type(a) != type(b):
        out.append((path, 'type')); return
    if isinstance(a, dict):
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b: out.append((path+'/'+k, 'key'))
            else: diff(a[k], b[k], path+'/'+k, out)
    elif isinstance(a, list):
        if len(a)!=len(b): out.append((path,'len'))
        for i,(x,y) in enumerate(zip(a,b)): diff(x,y,path+'/%d'%i,out)
    else:
        if a!=b: out.append((path,'value',a,b))
d=[]; diff(old_raw, old_fmt, '', d)
print('old formatted vs old raw differences:', len(d))
report = []
for item in d:
    p = item[0]
    if item[1]=='value':
        a,b = item[2], item[3]
        if isinstance(a,str):
            # find differing chars
            import difflib
            sm = difflib.SequenceMatcher(None, a, b)
            ops = [(t, a[i1:i2], b[j1:j2]) for t,i1,i2,j1,j2 in sm.get_opcodes() if t!='equal']
            print(p, len(a), len(b), ops[:12])
            report.append({'path':p,'raw_len':len(a),'formatted_len':len(b),'ops':[{'op':t,'raw':x,'formatted':y, 'raw_codepoints':[hex(ord(c)) for c in x], 'formatted_codepoints':[hex(ord(c)) for c in y]} for t,x,y in ops]})
            # test hypothesis: cp1252 decode of utf-8 bytes
            print('  cp1252-mojibake-hypothesis matches:', a.encode('utf-8').decode('cp1252', errors='replace') == b)
        else:
            print(p, a, b); report.append({'path':p,'raw':a,'formatted':b})
    else:
        print(item); report.append({'path':p,'kind':item[1]})
# Where is declaration_text; show which non-ascii characters exist in raw
nonascii = sorted({c for c in raw_b.decode('utf-8') if ord(c)>127})
print('non-ascii chars in fresh raw:', [(c, hex(ord(c))) for c in nonascii])
json.dump({'fresh_formatted': {'path':'work/export-review-01/request-review.json','sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'parsed_equal_to_raw': re==new},
           'prior_formatted_vs_prior_raw': report, 'non_ascii_in_fresh_raw': [{'char':c,'codepoint':hex(ord(c))} for c in nonascii]},
          io.open('work/export-review-01/decoder-observation.json','w',encoding='utf-8'), indent=1, ensure_ascii=False)
