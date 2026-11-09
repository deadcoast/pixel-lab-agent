import json,hashlib
from pathlib import Path
p=Path('work/focused-successor/specialist-proposal.json');d=json.loads(p.read_text(encoding='utf-8'))
for c in d['criteria']:
 for q in c['successor_checks']:
  q['check']=q['check'].replace('select stationaryFrame 0','select stationary frame zero via statusFrame(state, elapsed, reduced)')
d['request']['reduced']['selection_api']='src/queue-view-successor.ts statusFrame(state, elapsed, reduced), with reduced true selecting running frame 0; all other states static as before'
d['source_index'] = d['source_index']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(hashlib.sha256(p.read_bytes()).hexdigest())
for f in ['work/focused-successor/specialist-native-3x.png','work/focused-successor/specialist-grayscale.png']:
 print(f,hashlib.sha256(Path(f).read_bytes()).hexdigest())
