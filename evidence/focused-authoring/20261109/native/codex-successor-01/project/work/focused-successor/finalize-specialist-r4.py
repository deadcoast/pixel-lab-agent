from pathlib import Path
import json,hashlib
p=Path('work/focused-successor/specialist-proposal-r3.json');d=json.loads(p.read_text(encoding='utf-8')); obsolete=[]; fresh=[]
for s in d['source_index']:
 if s['path']=='renderer-successor/view.mjs':
  obsolete.append(s['id']);s['role']='historical pre-preference-reconciliation successor renderer; prior bytes preserved under work/focused-successor/source-revisions/r1/renderer-successor/view.mjs'
for f in ['renderer-successor/view.mjs','work/focused-successor/render-03/motion.json']:
 sid='source.%03d'%len(d['source_index']);d['source_index'].append({'id':sid,'path':f,'sha256':hashlib.sha256(Path(f).read_bytes()).hexdigest(),'role':'final preference-reconciliation renderer or actual observation evidence'});fresh.append(sid)
changes=[]
for c in d['criteria']:
 for q in c['successor_checks']:
  q['source_refs']=[s for s in q['source_refs'] if s not in obsolete]+fresh[:1]
  old=q['check'];text=old
  text=text.replace('immediately paint frame zero on both live and matrix Working cells','paint frame zero on both live and matrix Working cells when the media change event is delivered or when the next animation frame observes changed matchMedia.matches; reconcile only once per observed preference transition')
  if c['criterion'].endswith('delivery.q.destination'):
   text+=' Preference changes may be applied through the media change event or by comparing matchMedia.matches on the next animation frame; record the observed route. No requirement that this browser dispatch a change event is inferred. Reset the animation origin once per observed preference transition and repaint both live and matrix Working cells.'
  q['check']=text
  if old!=text:changes.append({'criterion':c['criterion'],'before':old,'after':text})
d['request']['reduced']['listeners']='Media-query change event and animation-frame reconciliation of matchMedia.matches use the same transition handler; apply once per actual changed preference, repaint live and matrix, reset normal origin. Render-03 observed animation-frame route; no event firing claim.'
d['revision']=4;d['supersedes']={'path':str(p).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'reason':'Parent discovered host updates matchMedia.matches without delivering change event; reviewed explicit animation-frame preference reconciliation and reexecuted actual browser evidence.'};d['revision_changes']=changes
d['final_successor_sources']=[s for s in d['final_successor_sources'] if s not in obsolete]+fresh
m=json.loads(Path('work/focused-successor/render-03/motion.json').read_text(encoding='utf-8-sig'))
d['final_motion_observation']={'path':'work/focused-successor/render-03/motion.json','source_ref':fresh[1],'phases':[{'name':x['name'],'sample_count':len(x['samples']),'span_ms':x['samples'][-1]['at']-x['samples'][0]['at'],'observed_frames':sorted({c['frame'] for s in x['samples'] for c in s['cells']}),'pixel_hash_count':len({c['image']['sha256'] for s in x['samples'] for c in s['cells']}),'changes':x['samples'][-1].get('changes',[])} for x in m['phases']],'scope':'Parsed recorded actual browser samples; no new interactive browser session by specialist. Parent executed capture. No event dispatch claimed.'}
d['visual_observations']['additional_actual_views'].append('work/focused-successor/render-03/reduced-live.png');d['visual_observations']['final_screenshot_finding']='Actually viewed render-03/reduced-live.png: full and compact Working segmented-ring marks are readable with Working labels; matrix shows distinct Working, asymmetric Ready check, pause bars, Retry arrow and preserved Start at1x/3x. Transparent exterior and crisp nearest treatment remain visible.'
r=p.with_name('specialist-proposal-r4.json');r.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');p.with_name('specialist-proposal.json').write_bytes(r.read_bytes());print(hashlib.sha256(r.read_bytes()).hexdigest())
