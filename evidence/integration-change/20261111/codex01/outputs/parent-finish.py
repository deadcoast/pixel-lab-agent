import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('parent_verify', HERE/'parent-verify.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
for name in ['baseline', 'prior', 'refresh', 'selections']:
    files = {'baseline':'parent-baseline.json','prior':'parent-initial-read.json','refresh':'parent-refresh.json','selections':'parent-selections.json'}
    setattr(v,name,json.loads((HERE/files[name]).read_text(encoding='utf-8-sig')))
tail = (HERE/'parent-verify.py').read_text().split('    fixture = ',1)[1]
tail = 'fixture = '+tail
tail = '\n'.join(line[4:] if line.startswith('    ') else line for line in tail.splitlines())
exec(compile(tail, str(HERE/'parent-verify.py')+' (remaining independent checks)', 'exec'),vars(v))
