import json
from pathlib import Path
w=Path('work/native-production'); d=json.loads((w/'handoff-details-01.json').read_text())
d['future_work']=[d.pop('next')]
f=json.loads((w/'failures-and-recovery-01.json').read_text());f.append({'kind':'handoff_details','status':'recovered_before_publication','error':'handoff_details: Derived fields belong to the snapshot; use caller_actions and future_work for commentary','detail':'First local handoff rejected reserved top-level next. Original details01 retained. Moved authored next instruction to future_work in details02; no state/provider mutation.'})
(w/'failures-and-recovery-02.json').write_text(json.dumps(f,indent=2)+'\n')
import hashlib
p=w/'failures-and-recovery-02.json';d['failures_and_recovery']={'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':'retained local failures and recovery'}
(w/'handoff-details-02.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
