"""Copy exact saved tool returns into work/compact-caller and probe key facts.

Usage: python -I -B helper_probe.py <consumer_root> <tool_results_dir>
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1])
tr = Path(sys.argv[2])
out = root / "work" / "compact-caller"
out.mkdir(parents=True, exist_ok=True)

copies = {
    "mcp-pixl-local-pixl_plar_read-1794301052512.txt": "specialist-plar-read.json",
    "mcp-pixl-local-pixl_workflow-1794301058934.txt": "specialist-workflow.json",
    "mcp-pixl-local-pixl_validate-1794301056421.txt": "specialist-validate.json",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


for src, dst in copies.items():
    s = tr / src
    d = out / dst
    if not d.exists():
        shutil.copyfile(s, d)
    print(dst, sha(d), d.stat().st_size)

plar = json.loads((out / "specialist-plar-read.json").read_text("utf-8"))
wf = json.loads((out / "specialist-workflow.json").read_text("utf-8"))
val = json.loads((out / "specialist-validate.json").read_text("utf-8"))

print("PLAR keys:", sorted(plar.keys()))
print("PLAR hash:", plar.get("hash"))
for k in ("requirements_hash", "project_root", "path"):
    print(k, plar.get(k))
asset = plar.get("asset", {})
print("asset keys:", sorted(asset.keys()))
print("asset id/status/kind:", asset.get("id"), asset.get("status"), asset.get("kind"))
prod = plar.get("production")
if prod is not None:
    print("production keys:", sorted(prod.keys()) if isinstance(prod, dict) else type(prod))
    print(json.dumps(prod, indent=1)[:6000])
for k in plar:
    if k not in ("sources", "queue", "asset", "production", "dependencies", "project", "coverage"):
        print("top", k, json.dumps(plar[k])[:1500])

print("WF keys:", sorted(wf.keys()), "rev", wf.get("revision"), "hash", wf.get("hash"), "files_verified", wf.get("files_verified"))
for t in wf.get("tasks", []):
    print("task", t.get("id"), t.get("status"), "keys", sorted(t.keys())[:20])
print("VAL", val.get("valid"), val.get("format"), val.get("revision"), val.get("hash"), val.get("records"), val.get("files_verified"))
