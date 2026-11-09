from pathlib import Path
import json,hashlib
root=Path.cwd();w=root/'work/successor-adoption'
def read(p):return json.loads((root/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
def ref(p):return {'path':p,'sha256':sha(p)}
d=read('work/successor-adoption/state-final-decoded.json');old=read('work/successor-adoption/state-before-decoded.json');oldids={r['id'] for r in old['records']};validation=read('work/successor-adoption/validation-final.json');hashes=validation['record_hashes'];idx={r['id']:r for r in d['records']}
new=[r for r in d['records'] if r['id'] not in oldids]
ri=[]
for r in new:
 item={'id':r['id'],'kind':r['kind'],'record_sha256':hashes[r['id']]}
 if r['kind'] in ['Q','S','C','I','X','V']:item['fields']=r['fields']
 elif r['kind']=='E':item['fields']={k:v for k,v in r['fields'].items() if k!='bs'}
 if r['fields'].get('ur') and Path(r['fields']['ur']).is_file(): item['artifact']=ref(r['fields']['ur'])
 ri.append(item)
(w/'new-record-index.json').write_text(json.dumps(ri,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'new_records':len(ri),'verdicts':sum(x['kind']=='V' for x in ri),'criteria':sum(x['kind']=='Q' and x['id'].startswith('successor-adoption-02') for x in ri)}))
