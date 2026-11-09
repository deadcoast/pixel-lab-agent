from adopt import *
from datetime import datetime,timezone
sys.path.insert(0,str(ROOT/'.agents/skills/pixl-kit/runtime'))
from pixl import codec,graph
at=datetime.now(timezone.utc).isoformat()
d=decode(); idx={r['id']:r for r in d['records']}; parsed=codec.parse(Path(STATE).read_bytes())
enginefiles=['render-01/render.json','render-01/motion.json','pixel-check.json','motion-check.json','live-pixels-and-timing.json','caller-visual-observation.json','caller-comparison.json']
observation={'scope':'Fresh actual Chromium fixture execution of unchanged backend and versioned consumer; live timing and source-vs-painted pixels, not direct real-time human pacing or external engine acceptance.','reviewer':'PIXL native foreground specialist','observed_at':at,'evidence':[{'path':'work/successor-adoption/'+p,'sha256':sha(W/p)} for p in enginefiles],'criteria':{},'limitations':['Actual browser normal loop sampled all4 frames and wrap;100ms exact claim limited to boundary arithmetic, observed sampled intertransition gaps are quantized.','No new provider generation; exact reused source bytes.','Visual motion-continuity remains unavailable separately.']}
for key in ['working','retry','paused']:
 qid='successor-adoption-02.'+key+'.q.consumers';observation['criteria'][qid]='pass: Fresh renderer exercises real backend transitions and both shared consumers with matching label,path,frame count; all20 state/scale cells plus reduced state matrix/source hashes/alpha/nearest pixel checks passed. Working normal boundary phases and actual loop/source-vs-painted samples agree, reduced frame0 holds >800ms in both consumers, both live preference transitions repaint live/matrix and keep backend state; observed next-rAF route and single origin reset. Retry/Paused remain frames1 static.'
save('engine-observation.json',observation)
for key in ['working','retry','paused']:
 prefix='successor02.'+key; qid='successor-adoption-02.'+key+'.q.consumers';xid='successor-adoption-02.'+key+'.candidate';tid='successor-adoption-02.'+key+'.task';eid=prefix+'.engine.evidence';vid=prefix+'.engine.verdict'
 scope=graph.proof_scope(parsed,[xid,qid])
 d['records'].append({'id':eid,'kind':'E','fields':{'nm':'Fresh versioned browser consumer observation '+key,'ur':'work/successor-adoption/engine-observation.json','dg':sha(W/'engine-observation.json'),'rs':sym('pass'),'md':sym('live'),'at':at,'bs':[{'rf':ref(s),'dg':codec.record_hash(parsed.records[s])} for s in sorted(scope)]}})
 d['records'].append({'id':vid,'kind':'V','fields':{'tk':ref(tid),'rq':ref(qid),'xr':ref(xid),'st':sym('pass'),'wh':ref('actor'),'wy':observation['criteria'][qid],'at':at,'ev':[ref(eid)]}});idx[tid]['fields']['vr'].append(ref(vid))
qid='successor-adoption-02.working.q.motion-continuity';tid='successor-adoption-02.working.task';vid='successor02.working.motion.unavailable'
reason='Full qualitative temporal criterion unavailable: actual browser ran and sampled every source phase and wrap at nominal100ms; still-only image host cannot judge perceived pacing, near-hold or visible wrap continuity in real time at1x/3x. Stable center/volume and shape observations do not satisfy this full condition. View exact retained Working playback directly, then add a superseding scoped visual review.'
d['records'].append({'id':vid,'kind':'V','fields':{'tk':ref(tid),'rq':ref(qid),'xr':ref('successor-adoption-02.working.candidate'),'st':sym('unavailable'),'wh':ref('actor'),'wy':reason,'at':at,'ev':[]}});idx[tid]['fields']['vr'].append(ref(vid))
commit('engine-and-unavailable-commit',d)
for key in ['retry','paused']:
 cli(key+'-completion','task-complete',STORE,'successor-adoption-02.'+key+'.task','successor-adoption-02.'+key+'.candidate','--expect',sha(STATE),'--root',ROOT)
cli('family-after-member-review','family',STATE,'successor-adoption-02.delivery.output','--root',ROOT)
cli('workflow-after-member-review','workflow',STATE,'--root',ROOT)
cli('inspection-after-member-review','inspection',STATE,'--root',ROOT)
cli('validation-after-member-review','validate',STATE,'--root',ROOT)
print('Fresh engine passes all3, unavailable visual motion retained; Retry/Paused completed, Working/family remain incomplete.')
