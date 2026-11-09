from adopt import *
j=json.loads(Path('authoring-plar.txt').read_text(encoding='utf-8'))
for a in j['assets']:
 for r in a['requirements']:
  if r['property']=='animation':
   r['value']={'normal':{'media':'prefers-reduced-motion: no-preference','frame_duration_ms':100,'loop':True,'nominal_cycle_ms':400},'reduced':{'media':'prefers-reduced-motion: reduce','frame':0,'stationary':True,'label':'Working','source_frames':4},'live_switch':'Repaint both consumers without backend state change; reset origin once per observed preference transition'}
   r['sources']+=['successor-assignment'];r['reason']='Normal motion retains original four-frame 100ms loop. Reviewed successor requires stationary Working frame zero under reduced motion, distinct from Ready and Paused; live preference switching preserves state/label/source geometry.'
  if r['property']=='renderer_frame_extraction':
   r['value']['implementation']='renderer-successor/view.mjs paint() and src/queue-view-successor.ts statusFrame()'; r['value']['frame_index']='normal: floor(max(elapsed,0)/display.frameMs) modulo frames; reduced:0';r['sources']=['successor-view','successor-renderer','successor-assignment'];r['reason']='Current versioned fixture uses unchanged backend; fresh scope is work/successor-adoption/render-01 plus pixel-check.json and motion-check.json. Old fixtures remain historical.'
  if r['property']=='motion_motif': r['value']='Exact reused four-phase rotating segments selected for this successor; stationary frame zero under reduce. This scoped expert choice does not turn the original open motif into a universal requirement.'
cli('plar-save-successor-02','plar','save',save('plar-proposal-02.json',j),'--expect',sha('authoring-plar.txt'),'--path','authoring-plar.txt','--root',ROOT)
p=json.loads((W/'public-plan.json').read_text(encoding='utf-8'));p['id']='successor-adoption-02'
for stage in p['stages']:
 key=stage['id'];rd=cli('plar-'+key+'-02','plar','read','--asset','queue.'+key,'--path','authoring-plar.txt','--root',ROOT); stage['selection']['requirements_hash']=rd['requirements_hash'];stage['selection']['replaces']={'store':STORE,'task':'successor-adoption.'+key+'.task','output':'successor-adoption.'+key+'.output'}
 for q in stage['criteria']:q['check']=q['check'].replace('successor-adoption.delivery.q.distinction','successor-adoption-02.delivery.q.distinction')
save('public-plan-02.json',p)
cli('production-plan-02','production-plan',STORE,W/'public-plan-02.json','--expect',sha(STATE),'--root',ROOT)
cli('request-review-02','request-review',STATE,'--plan','successor-adoption-02.plan','--root',ROOT)
print('Successor 02 retained and reviewed report ready')
