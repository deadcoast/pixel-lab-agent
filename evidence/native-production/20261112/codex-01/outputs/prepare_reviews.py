import json,hashlib,datetime
from pathlib import Path
w=Path('work/native-production')
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,v):
 p=w/n;p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
b=json.loads((w/'caller-preservation-baseline.json').read_text())
pres=[]
for v in b:
 p=v['path']; actual=h(p);pres.append(dict(v,actual_sha256=actual,unchanged=actual==v['sha256']))
save('preservation-check-01.json',{'files':pres,'all_unchanged':all(x['unchanged'] for x in pres)})
raw=json.loads((w/'inspection-prepare-01.json').read_text());ins=raw.get('structuredContent') or json.loads(raw['content'][0]['text'])
seen=[]
for v in ins['views']:seen.append({'view':v['id'],'delivered_size':[v['width'],v['height']],'note':'Viewed unmodified PNG image block via pixl_inspection host forwarding at retained native/3x dimensions. Candidate: cyan asymmetric success tick on intentional white roundel and blue stepped border, transparent exterior. Reference: unbadged blue check. Same compact stepped cool-blue language; roundel is permitted variation.'})
reasons={'geometry':'PNG 16x16 one static frame; asset-check exact bytes passes.','transparency':'Viewed exterior clear on transparent and dark background; white circular interior is intentional success badge subject, not a canvas matte.','success':'Visible blue tick bends from shorter descending arm into ascending arm; asymmetrical relationship reads successful completion at both sizes.','readability':'Native symbol reads as success badge/check; 3x shows deliberate stepped border and tick clusters without blur.','style':'Cyan/blue stepped edges and modest shading cohere with reference and queue context; white subject backing increases completion emphasis without eliminating blue accent. No exact palette/footprint rule applied.'}
save('inspection-review-input-01.json',{'reviewer':'actor','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'observations':seen,'verdicts':[{'criterion':'criterion.ready.'+k,'status':'pass','reason':v,'supersedes':None} for k,v in reasons.items()],'next_action':'Retain external renderer/grayscale/lineage/preservation review, then complete and hand off.','limitations':['Physical screen DPI is not established; image payload dimensions were retained and forwarded unchanged.','Acceptance is scoped to this queue UI.']})
print(json.dumps({'preservation_all_unchanged':all(x['unchanged'] for x in pres),'inspection_views':len(seen)}))
