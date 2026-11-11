from operations import *
p=read('work/integration-change/revised-prepare.json')
ev=save('new-abandon-evidence.json',{'scope':'LOCAL abandonment; no provider submission or remote failure','reason':'Exact retained art reuse requires no provider; request text also retained erroneous compact 100ms spelling, corrected in explicit successor','remote_executed':False})
op('new-abandon.json','job-observe',STORE,p['job']['id'],'failed',ev,'--expect',state(),'--root',ROOT)
args=read('work/integration-change/arguments-150.json');args['description']=args['description'].replace('100ms','150ms')
ap=save('arguments-150-corrected.json',args)
packet=read('work/integration-change/packet-150.json');packet['request'].update(path=ap,sha256=sha(ap))
pp=save('packet-150-corrected.json',packet)
p=op('corrected-prepare.json','plar','prepare','--root',ROOT,'--path','integration-plar.txt','--asset','queue.working','--requirements',p['requirements_hash'],'--packet',pp,'--connection','work/integration-inputs/connection.json','--revise','--expect',state())
ev=save('corrected-abandon-evidence.json',{'scope':'LOCAL abandonment of unsubmitted prepared intent; no provider execution or remote failure','reason':'Exact art reuse authorized; no generation necessary','remote_executed':False})
op('corrected-abandon.json','job-observe',STORE,p['job']['id'],'failed',ev,'--expect',state(),'--root',ROOT)
d=op('decoded-before-candidate.json','decode',STATE)
ref=lambda x:{'$ref':x}
sym=lambda x:{'$symbol':x}
output=p['outputs'][0]; contract=next(r for r in d['records'] if r['id']==output)['fields']['ct']
d['revision']+=1
d['records'].append({'id':'working.reused150','kind':'X','fields':{'nm':'Exact retained Working bytes freshly reviewed at150ms','ur':'assets/working.png','dg':sha('assets/working.png'),'kd':sym('animation'),'ct':contract,'of':ref(output),'mt':{'provenance':'Historical exact art reused; not generated under successor; no succeeded remote job'}}})
cp=save('candidate-commit-document.json',d)
op('candidate-commit.json','commit',STORE,cp,'--json','--expect',state(),'--root',ROOT)
op('sample-context.json','review-context',STATE,'working.reused150','--root',ROOT)
command=['node','renderer-integration/capture.mjs','--project',str(ROOT),'--out',str(OUT/'sample-capture')]
r=subprocess.run(command,cwd=ROOT,capture_output=True)
(OUT/'sample-capture.stdout').write_bytes(r.stdout);(OUT/'sample-capture.stderr').write_bytes(r.stderr)
save('sample-capture.execution.json',{'command':command,'exit_code':r.returncode,'helper_sha256':sha('work/integration-change/continue.py')})
print(r.stdout.decode(),r.stderr.decode())
