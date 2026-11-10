import json, subprocess, pathlib, hashlib
root=pathlib.Path.cwd()
out=root/'work/named-role'
python='C:/github/pixel-lab-agent/.venv/Scripts/python.exe'
runner=root/'.agents/skills/role-kit/scripts/pixl.py'
def run(name,args):
    p=subprocess.run([python,str(runner),*args,'--root',str(root)],capture_output=True,encoding='utf-8')
    if p.returncode: raise RuntimeError(p.stdout+p.stderr)
    data=json.loads(p.stdout)
    (out/name).write_text(p.stdout,encoding='utf-8')
    return data
selected=run('selected-round1.json',['plar','read','--path','authoring-plar.txt','--asset','queue.working'])
state=str(root/'.pixl/assets/queue.ready/state.px')
for name,args in [
 ('candidate-export-receipt.json',['review-context',state,'native.provenance.delivery.candidate.01','--result-path','work/named-role/candidate-context.json']),
 ('family-export-receipt.json',['family',state,'provenance-correction.delivery.output','--result-path','work/named-role/family-context.json']),
 ('authoring-export-receipt.json',['context',state,'provenance-correction.plan','--view','authoring','--result-path','work/named-role/authoring-context.json']),
 ('request-export-receipt.json',['request-review','.pixl/assets/queue.ready/state.px','--plan','provenance-correction.plan','--result-path','work/named-role/request-context.json']),
 ('workflow-round1.json',['workflow',state]),('jobs-round1.json',['jobs',state])]: run(name,args)
print(json.dumps({'selected_keys':list(selected),'candidate_keys':list(json.loads((out/'candidate-context.json').read_text(encoding='utf-8'))),'family_keys':list(json.loads((out/'family-context.json').read_text(encoding='utf-8')))},indent=2))
