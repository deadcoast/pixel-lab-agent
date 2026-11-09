from adopt import *
d=decode(); idx={r['id']:r for r in d['records']}
original={'working':'live.working-animation-motion-01.candidate','retry':'live.retry.candidate','paused':'live.paused-cutout-01.candidate'}
for key,oldid in original.items():
 old=idx[oldid]; c=copy.deepcopy(old);c['id']='successor-adoption-02.'+key+'.candidate';c['fields']['ct']=ref('successor.'+key+'.contract');c['fields']['of']=ref('successor-adoption-02.'+key+'.output');c['fields']['nm']='Exact-byte reuse '+key+' under successor02, not new provider generation';c['fields']['mt']={'provenance_candidate':ref(oldid),'reuse_sha256':old['fields']['dg'],'provider_generated_under_successor':False,'destination':'renderer-successor/assets/'+{'working':'working.png','retry':'error-retry.png','paused':'paused.png'}[key]}; assert sha(c['fields']['mt']['destination'])==c['fields']['dg'];d['records'].append(c)
commit('candidate-commit',d)
for key in original:
 options={'references':['ready.retained'],'scale':3,'backgrounds':['#172336'],'contexts':[]}
 if key=='working':options['contexts']=[{'name':'normal-four-frame-loop','kind':'frames','source':'successor-adoption-02.working.candidate','source_frame':0,'rects':[[i*16,0,16,16] for i in range(4)],'durations_ms':[100]*4,'pivots':[None]*4}]
 save(key+'-inspection-options.json',options)
 r=cli(key+'-inspection-prepare','inspection-prepare',STORE,'successor-adoption-02.'+key+'.candidate','successor02.'+key+'.packet',W/(key+'-inspection-options.json'),'--expect',sha(STATE),'--root',ROOT)
 print(key,[(v['id'],v['path'],v['width'],v['height']) for v in r['views']])
