from pathlib import Path
import json, subprocess, sys, hashlib, copy
ROOT=Path.cwd(); W=ROOT/'work/successor-adoption'; W.mkdir(exist_ok=True,parents=True)
PY='C:/github/pixel-lab-agent/.venv/Scripts/python.exe'; RUN=str(ROOT/'.agents/skills/pixl-kit/scripts/pixl.py'); STORE='.pixl/assets/queue.ready'; STATE=STORE+'/state.px'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,obj):
 p=W/name; p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); return str(p)
def cli(name,*args):
 p=W/(name+'.json')
 with p.open('xb') as f: r=subprocess.run([PY,RUN,*map(str,args)],stdout=f,stderr=subprocess.PIPE)
 if r.returncode: print(r.stderr.decode('utf-8',errors='replace')); print(p.read_text(encoding='utf-8')); raise RuntimeError(name)
 return json.loads(p.read_text(encoding='utf-8'))
def decode(): return json.loads(subprocess.check_output([PY,RUN,'decode',STATE]).decode('utf-8'))
def commit(name,d):
 d['revision']+=1
 return cli(name,'commit',STORE,save(name+'-document.json',d),'--json','--expect',sha(STATE),'--root',ROOT)
def ref(s): return {'$ref':s}
def sym(s): return {'$symbol':s}
if __name__=='__main__':
 cli('context-before','context',STATE,'authoring-01.plan','--view','authoring','--plar','authoring-plar.txt','--asset','queue.working','--root',ROOT)
 cli('workflow-before','workflow',STATE,'--root',ROOT); cli('family-before','family',STATE,'--root',ROOT); cli('jobs-before','jobs',STATE,'--root',ROOT)
 d=decode(); idx={r['id']:r for r in d['records']}
 save('selected-records-before.json',[idx[x] for x in ['project','family.working.contract','family.retry.contract','family.paused.contract','render.choice.destination','recheck.decision.destination','ready.retained','live.working.constructed'] if x in idx])
 j=json.loads(Path('authoring-plar.txt').read_text(encoding='utf-8'))
 paths={'successor-view':'src/queue-view-successor.ts','successor-renderer':'renderer-successor/view.mjs','successor-assignment':'SUCCESSOR-ADOPTION.md'}
 for id,p in paths.items(): j['sources'].append({'id':id,'path':p,'sha256':sha(p)})
 j['coverage']['included'].append('SUCCESSOR-ADOPTION: current queue consumer is versioned src/queue-view-successor.ts and renderer-successor/. Exact old Ready and Start bytes reused; original sources/renderer/assets preserved. accountBadge still resolves a server registry path and remains outside local replacement scope.')
 for a in j['assets']:
  for c in a['consumers']:
   if c['source']=='queue-view': c['source']='successor-view'; c['usage']=c['usage'].replace('assets/','renderer-successor/assets/')
  for r in a['requirements']:
   r['sources']=['successor-view' if x=='queue-view' else x for x in r['sources']]
  a['delivery']['path']='renderer-successor/'+a['delivery']['path']
  a['delivery']['checks']=[x.replace('assets/','renderer-successor/assets/').replace('Fresh local successor evidence is work/focused-successor/caller-comparison.json; retained-generation completion remains open.','Fresh acceptance is pending against this new connected successor; historical reviews do not transfer.') for x in a['delivery']['checks']]
  if a['id']=='queue.working':
   a['delivery']['checks']=[x.replace('Play the loop at 100 ms','Under no-preference only, play the loop at 100 ms') for x in a['delivery']['checks']]
   a['delivery']['checks'].append('Under reduced motion display stationary Working frame zero in both consumers and repaint live when preference changes both ways, keeping backend state and labels unchanged.')
  a['next']='Retain current successor plan, inspect exact reused bytes and fresh versioned renderer evidence, publish new scoped verdicts before completion; preserve all historical allocation/evidence.' if a['id'] not in ['queue.start','queue.ready'] else 'Preserve exact existing bytes; verify successor mapping alongside family; no replacement generation.'
  if a['id'] in ['queue.working','queue.retry','queue.paused']: a['status']='todo'
 plar_before=sha('authoring-plar.txt')
 cli('plar-save-successor','plar','save',save('plar-proposal.json',j),'--expect',plar_before,'--path','authoring-plar.txt','--root',ROOT)
 reads={}
 for a in ['working','retry','paused']: reads[a]=cli('plar-'+a,'plar','read','--asset','queue.'+a,'--path','authoring-plar.txt','--root',ROOT)
 save('plar-read-keys.json',{k:list(v) for k,v in reads.items()})
 print(json.dumps({k:{x:v[x] for x in v if 'hash' in x} for k,v in reads.items()}))
