from pathlib import Path
import json,hashlib
p=Path('work/focused-successor/specialist-proposal-r2.json');d=json.loads(p.read_text(encoding='utf-8'));refs={}
for a in d['reuse_assets']:
 sid='source.%03d'%len(d['source_index']);d['source_index'].append({'id':sid,'path':a['source'],'sha256':a['sha256'],'role':'exact reused art source; destination '+a['destination']});refs[a['source'].split('/')[-1]]=sid
for c in d['criteria']:
 for q in c['successor_checks']:
  if c['stage']=='working':q['source_refs'].append(refs['working.png'])
  elif c['stage']=='retry':q['source_refs'].append(refs['error-retry.png'])
  elif c['stage']=='paused':q['source_refs'].append(refs['paused.png'])
  else:q['source_refs']+=list(refs.values())
  q['check']=q['check'].replace('with the exact retained package files at the confirmed destination paths','with the exact retained package files at the caller-reviewed proposed successor destination paths').replace('Successor destination is src/queue-view-successor.ts','Caller-reviewed proposed successor destination is src/queue-view-successor.ts')
d['revision']=3;d['supersedes']={'path':str(p).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'reason':'Caller requested reused art identities in shared source index and destination authority explicitly proposed until caller adoption.'}
r=p.with_name('specialist-proposal-r3.json');r.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');p.with_name('specialist-proposal.json').write_bytes(r.read_bytes());print(hashlib.sha256(r.read_bytes()).hexdigest())
