from pathlib import Path
import json,hashlib
p=Path('work/focused-successor/specialist-proposal.json');d=json.loads(p.read_text(encoding='utf-8')); ids=[]
for f in ['src/queue-view-successor.ts','renderer-successor/view.mjs','renderer-successor/capture.mjs','renderer-successor/index.html','renderer-successor/server.mjs','work/focused-successor/render-02/motion.json']:
 q=Path(f)
 if not q.exists():continue
 sid='source.%03d'%len(d['source_index']);d['source_index'].append({'id':sid,'path':f,'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'role':'final successor source or actual rendered evidence; not historical source replacement'});ids.append(sid)
for c in d['criteria']:
 for q in c['successor_checks']:
  q['source_refs']+=ids[:2]
d['final_successor_sources']=ids
d['visual_observations']['additional_actual_views']=['work/focused-successor/render-01/destination.png','work/focused-successor/render-01/reduced-live.png']
d['visual_observations']['additional_findings']='Actually viewed destination screenshot and reduced-live screenshot. Both full and compact consumers show crisp blue segmented Working frame zero with Working labels in reduced-live; matrix displays distinct check, pause bars, Retry arrow and Start triangle at native/3x. No opaque matte in destination. Parsed actual render-01 sample observations: normal-before and normal-after each include all four frame indices and four pixel hashes; reduced-live has only frame0 and one hash over626.5ms, which alone did not reach the proposed800ms evidence window. Parent extended capture as render-02; reported separately.'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');r=p.with_name('specialist-proposal-r2.json');r.write_bytes(p.read_bytes());print(str(r),hashlib.sha256(r.read_bytes()).hexdigest())
