from adopt import *
from datetime import datetime,timezone
cli('request-review-coverage','request-review',STATE,'--plan','successor-adoption-02.plan','--comparison',W/'caller-comparison.json','--root',ROOT)
reasons={
'geometry':'Decoded exact saved PNG and source copy: Working 64x16 four horizontal16x16 cells, Retry/Paused16x16. Transparent in-cell margins preserved; no extra canvas/gutters.',
'transparent-exterior.diagnostic':'Fresh alpha-diagnostics.json retains each cell histogram and component boxes; flags are diagnostic only, never an acceptance cutoff; alpha-zero RGB ignored.',
'transparent-exterior':'All actual fresh native/3x panel views inspected: panel shows through intended exterior, no opaque canvas matte or fringe. Selective AA/full alpha allowed. Transparent Paused source may show alpha-zero stored RGB in raw host handling; composited views and actual engine pixels show correct cool-blue bars without matte.',
'frame-assembly':'New candidate and renderer-successor/assets/working.png hash cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc equal exact original retained motion candidate. No new assembly/edit/provider execution.',
'activity-not-success':'All four disconnected stepped orbital segment poses read as activity, no check or terminal success pose. Native/3x frame0 with Working label is distinct from Ready check and Paused bars. Fresh phase samples exercise every frame; direct real-time pacing is separately unavailable.',
'motion-continuity':'Unavailable full qualitative temporal condition: browser actually ran four100ms phases and wrap and painted pixels match source; still-only host image access supports stable center/volume per pose but cannot establish real-time perceptual smoothness/even pacing or absence of visible wrap discontinuity. Need direct playback appraisal of this exact candidate under normal preference at1x/3x. No criterion relaxed.',
'style-coherence':'Fresh native/3x candidate and Ready reference views show deliberate compact stepped clusters, perceptible cool-blue accent and readable silhouettes. Paused tall bars, Retry curved arrow and Working spaced segments have appropriate different footprints; identical weight/palette/alpha not required.',
'retry-meaning-without-color':'Native/3x and grayscale show connected circular retry arrow for failed work, distinct from disconnected Working arcs, Ready check, Paused bars and preserved Start triangle; with Retry label its action is clear.',
'pause-meaning-without-color':'Native/3x and grayscale show two separated straight bars, distinct by shape from Ready check, disconnected rotating segments and connected Retry arrow; Start remains a triangle. No color-only distinction.'}
for key in ['working','retry','paused']:
 p=json.loads((W/(key+'-inspection-prepare.json')).read_text(encoding='utf-8'))
 obs={'reviewer':'actor','observed_at':datetime.now(timezone.utc).isoformat(),'observations':[{'view':v['id'],'delivered_size':[v['width'],v['height']],'note':'Actually viewed via pixl_inspection unresized image block at these payload dimensions; '+('candidate/reference native or3x with full visible extent' if v['scale'] in [1,3] else 'prepared view')} for v in p['views']],'verdicts':[],'next_action':'Bind fresh engine verdict separately; Working temporal review remains required before completion.' if key=='working' else 'Bind fresh engine verdict separately, then complete only with all required passes.','limitations':['Host access supplies still image blocks, no direct real-time playback appraisal. Mechanical browser phase/pixel checks are distinct from temporal visual judgment.','No new model generation or provider request; exact original bytes reused.']}
 for q in p['criteria']:
  suffix=q['id'].split('.q.',1)[1]
  if suffix=='consumers':continue
  obs['verdicts'].append({'criterion':q['id'],'status':'unavailable' if suffix=='motion-continuity' else 'pass','reason':reasons[suffix],'supersedes':None})
 save(key+'-review-observation.json',obs)
 r=cli(key+'-inspection-review','inspection-review',STORE,p['packet'],'successor02.'+key+'.review',W/(key+'-review-observation.json'),'--expect',sha(STATE),'--root',ROOT)
 print(key,r['coverage'])
