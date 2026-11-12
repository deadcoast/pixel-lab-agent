import json, subprocess, hashlib
from pathlib import Path
from datetime import datetime, timezone
p = Path('work/provider-recovery/phase-1')
response = json.loads((p/'provider-status-2.json').read_text())['structuredContent']
url = response['images'][0]['download_url']
command = ['curl.exe', '--fail', '--show-error', '--output', str(p/'download.part'), url]
r = subprocess.run(command, capture_output=True)
(p/'download-stdout.bin').write_bytes(r.stdout)
(p/'download-stderr.bin').write_bytes(r.stderr)
diagnostic = {'command': command, 'exit_code': r.returncode, 'stdout': r.stdout.decode('utf-8', errors='replace'), 'stderr': r.stderr.decode('utf-8', errors='replace'), 'observed_at': datetime.now(timezone.utc).isoformat(), 'provider_simulated': True, 'attempts': 1, 'expected': response['images'][0]}
part = p/'download.part'
if part.exists():
    data = part.read_bytes()
    diagnostic['partial'] = {'path': part.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
(p/'download-error.json').write_text(json.dumps(diagnostic, indent=2)+'\n', encoding='utf-8')
print(json.dumps(diagnostic, indent=2))
if r.returncode == 0:
    raise RuntimeError('Expected controlled truncation did not occur; do not retry')
