import json, pathlib, subprocess, hashlib, sys, datetime
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'work/integration-change'
PY='C:/github/pixel-lab-agent/build/readiness-setup-01/runtime/Scripts/python.exe'
RUN=ROOT/'installed pixl/scripts/pixl.py'
STORE='.pixl/assets/queue.working'
STATE=STORE+'/state.px'
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def save(n,v):
 p=OUT/n;p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');return p.relative_to(ROOT).as_posix()
def op(n,*args,ok=True):
 command=[PY,str(RUN),*map(str,args)]
 r=subprocess.run(command,cwd=ROOT,capture_output=True)
 (OUT/n).write_bytes(r.stdout)
 (OUT/(n+'.stderr')).write_bytes(r.stderr)
 save(n+'.execution.json',{'command':command,'exit_code':r.returncode,'stdout_sha256':sha('work/integration-change/'+n),'stderr_sha256':sha('work/integration-change/'+n+'.stderr'),'helper_sha256':sha('work/integration-change/operations.py')})
 if ok and r.returncode: raise RuntimeError(r.stderr.decode()+r.stdout.decode())
 try:return json.loads(r.stdout)
 except:return None
def state():return op('validate-'+str(len(list(OUT.glob('validate-*json'))))+'.json','validate',STATE,'--root',ROOT)['hash']
if __name__=='__main__':
 d=read('integration-plar.txt'); initial=read('work/integration-change/initial-read.json')
 for s in d['sources']:
  if s['id'] in ['working-timing','timing-authority']:s['sha256']=sha(s['path'])
 a=next(a for a in d['assets'] if a['id']=='queue.working')
 next(r for r in a['requirements'] if r['property']=='animation')['value'].update(frame_duration_ms=150,nominal_cycle_ms=600)
 final=save('final-document.json',d)
 op('allocation-save.json','plar','save',final,'--root',ROOT,'--path','integration-plar.txt','--expect',initial['hash'])
 sel=op('current-selection.json','plar','read','--path','integration-plar.txt','--asset','queue.working','--root',ROOT)
 op('obsolete-dispatch.json','job-dispatch',STORE,'first_request','--expect',state(),'--root',ROOT,ok=False)
 op('obsolete-completion.json','task-complete',STORE,'task','working.nonexistent','--expect',state(),'--root',ROOT,ok=False)
 ev=save('old-abandon-evidence.json',{'scope':'LOCAL abandonment of unsubmitted prepared intent; no provider execution or remote failure','reason':'150ms amendment supersedes original 100ms intent; exact art reuse required','remote_executed':False})
 op('old-abandon.json','job-observe',STORE,'first_request','failed',ev,'--expect',state(),'--root',ROOT)
 criteria=read('work/integration-inputs/criteria-100.json')
 criteria=json.loads(json.dumps(criteria).replace('100 ms','150 ms'))
 criteria['scope']='Controlled exact-art reuse under 150ms amendment; no provider execution'
 cp=save('criteria-150.json',criteria)
 args=read('work/integration-inputs/arguments-100.json');args=json.loads(json.dumps(args).replace('100 ms','150 ms'))
 ap=save('arguments-150.json',args)
 packet=read('work/integration-inputs/packet-100.json');packet['requirements_hash']=sel['requirements_hash']
 for s in packet['sources']:s['sha256']=sha(s['path'])
 packet['criteria']={'path':cp,'sha256':sha(cp)};packet['request'].update(path=ap,sha256=sha(ap))
 pp=save('packet-150.json',packet)
 prep=op('revised-prepare.json','plar','prepare','--root',ROOT,'--path','integration-plar.txt','--asset','queue.working','--requirements',sel['requirements_hash'],'--packet',pp,'--connection','work/integration-inputs/connection.json','--revise','--expect',state())
 print(json.dumps(prep,indent=2))
