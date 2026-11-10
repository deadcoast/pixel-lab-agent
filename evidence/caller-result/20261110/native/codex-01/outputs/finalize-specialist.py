import json,hashlib
from pathlib import Path
r=Path.cwd()
def read(p): return json.loads((r/p).read_text(encoding='utf-8-sig'))
def ref(p): return {'path':p,'sha256':hashlib.sha256((r/p).read_bytes()).hexdigest()}
c=read('work/compact-caller/compact.json'); q=read('work/compact-caller/receipt.json')
assert c['path']==q['path'] and c['sha256']==q['sha256']
d=read('work/compact-caller/details.json')
assert d['retained_specialist_observations']==read('work/artistic-revision/SPECIALIST-RESULT.json')
v={'native_child':{'agent_type':'pixl','canonical_task':'/root/compact_specialist','fork_turns':'none'},'status':'partial','compact':ref('work/compact-caller/compact.json'),'receipt':ref('work/compact-caller/receipt.json'),'detailed_report':ref('work/compact-caller/SPECIALIST-REPORT.json'),'details':ref('work/compact-caller/details.json'),'handoff':{'path':c['path'],'sha256':c['sha256']},'same_snapshot':True,'production_next':c['next'],'limits':['Retained evidence only; no fresh renderer run or new acceptance.','Separate fictional member.job remains unknown; no remote observation or retry.','No production state, original artifact, job or review edits.'],'unchanged_retained_observations':True}
(r/'work/compact-caller/SPECIALIST-RESULT.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
print(json.dumps(v))
