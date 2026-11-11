"""Independent caller byte checks; public operation returns are retained verbatim."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'work/integration-change'
CLI = ROOT / 'installed pixl/scripts/pixl.py'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def public(name, args):
    target = OUT / name
    if target.exists():
        raise FileExistsError(target)
    command = [sys.executable, str(CLI), *args]
    run = subprocess.run(command, cwd=ROOT, capture_output=True)
    target.write_bytes(run.stdout)
    target.with_suffix('.stderr.txt').write_bytes(run.stderr)
    target.with_suffix('.command.json').write_text(json.dumps({'command':command,'exit_code':run.returncode},indent=2))
    if run.returncode:
        raise RuntimeError(name)
    return json.loads(run.stdout)

if __name__ == '__main__':
    baseline = json.loads((OUT/'parent-baseline.json').read_text(encoding='utf-8-sig'))
    prior = json.loads((OUT/'parent-initial-read.json').read_text(encoding='utf-8-sig'))
    refresh = public('parent-refresh.json',['plar','read','--root',str(ROOT),'--path','integration-plar.txt','--since',prior['hash']])
    selections = {}
    for asset in ['queue.ready','queue.working','queue.retry','queue.start','queue.paused']:
        selections[asset] = public('parent-selection-'+asset+'.json',['plar','read','--root',str(ROOT),'--path','integration-plar.txt','--asset',asset])
    (OUT/'parent-selections.json').write_text(json.dumps(selections,indent=2))
    public('parent-acceptance.json',['family',str(ROOT/'.pixl/assets/queue.working'),'--root',str(ROOT)])
    fixture = json.loads((ROOT/'work/integration-inputs/fixture.json').read_bytes())
    art = {p: {'expected':h,'actual':digest(ROOT/p),'pass':digest(ROOT/p)==h} for p,h in fixture['exact_art'].items()}
    protected = [r for r in baseline if r['path'] != 'integration-plar.txt' and not r['path'].startswith('.pixl/')]
    changed = [r['path'] for r in protected if not (ROOT/r['path']).exists() or digest(ROOT/r['path']) != r['sha256']]
    initial_sources = {r['id']:r for r in prior['sources']}
    source_changes = [r['id'] for r in refresh['sources'] if r['sha256'] != initial_sources[r['id']]['sha256']]
    unchanged_rows = {asset: selections[asset]['requirements_hash'] for asset in selections if asset != 'queue.working'}
    original = json.loads((ROOT/'.pixl/plar-history'/ (prior['hash']+'.json')).read_bytes())
    current = json.loads((ROOT/'integration-plar.txt').read_bytes())
    original_rows = {r['id']:r for r in original['assets']}
    row_changes = [r['id'] for r in current['assets'] if r != original_rows[r['id']]]
    old_immutable = [r for r in baseline if r['path'].startswith('.pixl/') and not r['path'].endswith(('state.px','.lock')) and '/plar-lock/' not in r['path']]
    immutable_changes = [r['path'] for r in old_immutable if not (ROOT/r['path']).exists() or digest(ROOT/r['path']) != r['sha256']]
    public('parent-jobs.json',['jobs',str(ROOT/'.pixl/assets/queue.working/state.px'),'--root',str(ROOT)])
    result = {'exact_art':art,'protected_file_changes':changed,'old_immutable_changes':immutable_changes,'asset_row_changes':row_changes,'source_binding_changes':source_changes,'unrelated_requirements_hashes':unchanged_rows,'changes':refresh['changes']}
    (OUT/'parent-byte-checks.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
