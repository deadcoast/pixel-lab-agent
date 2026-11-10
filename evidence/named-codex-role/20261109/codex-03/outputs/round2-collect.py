import json,subprocess,pathlib,hashlib
root=pathlib.Path.cwd(); out=root/'work/named-role'; py='C:/github/pixel-lab-agent/.venv/Scripts/python.exe'; runner=root/'.agents/skills/role-kit/scripts/pixl.py'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(name,args):
 p=subprocess.run([py,str(runner),*args,'--root',str(root)],capture_output=True,encoding='utf-8'); assert p.returncode==0,p.stdout+p.stderr
 (out/name).write_text(p.stdout,encoding='utf-8');return json.loads(p.stdout)
review=root/'work/export-review/identical-review.json'; before=h(review)
c=run('round2-pre-context-receipt.json',['review-context',str(root/'.pixl/assets/queue.ready/state.px'),'native.provenance.delivery.candidate.01','--result-path','work/named-role/round2-pre-context.json'])
context=json.loads((out/'round2-pre-context.json').read_text(encoding='utf-8'))
result=run('round2-replay-receipt.json',['candidate-review',str(root/'.pixl/assets/queue.ready'),'native.provenance.delivery.candidate.01','native.family.review.01',str(review),'--expect',context['state_hash'],'--result-path','work/named-role/round2-replay-result.json'])
s=run('selected-round2.json',['plar','read','--path','authoring-plar.txt','--asset','queue.working'])
print(json.dumps({'replay':result,'input_before':before,'input_after':h(review),'state_after':s['production']['continuation']['state_hash']},indent=2))
