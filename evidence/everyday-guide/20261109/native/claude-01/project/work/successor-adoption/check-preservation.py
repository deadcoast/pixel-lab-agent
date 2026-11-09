from pathlib import Path
import json,hashlib,subprocess
root=Path.cwd();w=root/'work/successor-adoption';py='C:/github/pixel-lab-agent/.venv/Scripts/python.exe';runner=root/'.agents/skills/pixl-kit/scripts/pixl.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,o):(w/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
before=json.loads((w/'preservation-before.json').read_text(encoding='utf-8'));changed=[p for p,h in before.items() if not Path(p).is_file() or sha(root/p)!=h]
initial=json.loads((w/'state-before-decoded.json').read_text(encoding='utf-8'))
final=json.loads(subprocess.check_output([py,str(runner),'decode','.pixl/assets/queue.ready/state.px']).decode('utf-8'));save('state-final-decoded.json',final)
i={r['id']:r for r in initial['records']};f={r['id']:r for r in final['records']}
protected=[id for id,r in i.items() if r['kind'] in ['C','I','Q','S','D','E','V','X','J']]
record_changes=[id for id in protected if f.get(id)!=i[id]]
res={'status':'pass' if not changed and not record_changes else 'fail','old_files_checked':len(before),'changed_or_missing_files':changed,'manifest':{'path':'work/successor-adoption/preservation-before.json','sha256':sha(w/'preservation-before.json')},'initial_state':{'revision':initial['revision'],'path':'.pixl/assets/queue.ready/history/022224962d44ec6ef1398056f278922f9e120ffcc97288fa997eff4922821daa.px','sha256':'022224962d44ec6ef1398056f278922f9e120ffcc97288fa997eff4922821daa'},'final_state':{'revision':final['revision'],'path':'.pixl/assets/queue.ready/state.px','sha256':sha(root/'.pixl/assets/queue.ready/state.px')},'old_semantic_candidate_job_records_checked':len(protected),'old_record_changes':record_changes,'protected_records':[{'id':id,'kind':i[id]['kind'],'canonical_json_sha256':hashlib.sha256(json.dumps(i[id],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()} for id in protected]}
save('preservation-final.json',res)
assert res['status']=='pass',res
print(json.dumps({k:v for k,v in res.items() if k!='protected_records'}))
