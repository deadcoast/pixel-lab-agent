from adopt import *
d=decode(); idx={r['id']:r for r in d['records']}
srcs={'view':'src/queue-view-successor.ts','renderer':'renderer-successor/view.mjs','assignment':'SUCCESSOR-ADOPTION.md','proposal':'work/focused-successor/specialist-proposal-r4.json','comparison':'work/focused-successor/caller-comparison-final.json','backend':'src/queue.ts','server':'renderer-successor/server.mjs','capture':'renderer-successor/capture.mjs'}
for key,p in srcs.items():
 if not Path(p).exists(): continue
 d['records'].append({'id':'successor.source.'+key,'kind':'S','fields':{'ur':p,'dg':sha(p),'ln':[1,len(Path(p).read_text(encoding='utf-8').splitlines())],'at':'Successor adoption authority/actual consumer: '+key,'au':sym('local')}})
idx={r['id']:r for r in d['records']}
choice=copy.deepcopy(idx['render.choice.destination']); choice['id']='focused-successor.choice.destination'; f=choice['fields']; f['ky']='family.destination.successor_adoption'; f['so']=[ref('successor.source.'+x) for x in ['view','renderer','assignment','proposal','comparison']]; f['vl']['paths']={k:'renderer-successor/'+v for k,v in f['vl']['paths'].items()}; f['vl']['paths']['start']='renderer-successor/assets/start.svg'; f['vl']['engine']='Versioned supplied browser fixture executing src/queue.ts and src/queue-view-successor.ts'; f['vl']['placement_acceptance']='Requires fresh successor-scoped verdicts; old acceptance not transferred'; f['vl']['working_normal']='Four horizontal cells at nominal 100ms only under no-preference'; f['vl']['working_reduced']='Stationary frame zero while running; live preference switches reconcile once via change event or next-rAF matches'; f['wy']='Caller adopted local versioned destination in corrected retained comparison; SUCCESSOR-ADOPTION authorizes retention and fresh acceptance. Old destination preserved.'
d['records'].append(choice); idx['project']['fields']['in'].append(ref(choice['id']))
for key in ['working','retry','paused']:
 c=copy.deepcopy(idx['family.'+key+'.contract']); c['id']='successor.'+key+'.contract'; c['fields']['ch']=[ref('render.choice.style'),ref(choice['id'])]
 if key=='working': c['fields']['li']=c['fields']['li'].replace('at100ms/frame','at100ms/frame under normal motion only')+' Reduced motion displays stationary source frame zero with Working label; all four source cells remain unchanged. Live preference switching preserves backend state.'
 d['records'].append(c)
commit('source-contract-destination-commit',d)
p=json.loads(Path('work/focused-successor/retained-successor-proposal.json').read_text(encoding='utf-8'))['public_plan_shape']; p['id']='successor-adoption'; p['delivery']['name']='Reviewed versioned queue successor delivery with exact reused art'
for stage in p['stages']:
 key=stage['id']; rd=json.loads((W/('plar-'+key+'.json')).read_text(encoding='utf-8')); stage['contract']='successor.'+key+'.contract'; stage['selection']['requirements_hash']=rd['requirements_hash']; stage['selection']['replaces']={k:rd['production'][k] for k in ['store','task']}; stage['selection']['replaces']['output']='authoring-01.'+key+'.output'
 for q in stage['criteria']: q['sources']+=['successor.source.'+x for x in ['view','renderer','assignment','proposal','comparison','backend']]; q['check']=q['check'].replace('authoring-01.delivery.q.distinction','successor-adoption.delivery.q.distinction')
for q in p['delivery']['criteria']: q['sources']+=['successor.source.'+x for x in ['view','renderer','assignment','proposal','comparison','backend']]
save('public-plan.json',p)
r=cli('production-plan','production-plan',STORE,W/'public-plan.json','--expect',sha(STATE),'--root',ROOT)
print(json.dumps(r,indent=2)[:6000])
