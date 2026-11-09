"""Caller baseline inventory: sha256 of every file under the project, excluding the caller's own new directory."""
import hashlib, json, os, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
exclude = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else set()
files = {}
for p in sorted(root.rglob("*")):
    if not p.is_file():
        continue
    rel = p.relative_to(root).as_posix()
    if any(rel == e or rel.startswith(e + "/") for e in exclude):
        continue
    if "__pycache__" in rel:
        continue
    files[rel] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size}
print(json.dumps({"root": str(root), "count": len(files), "files": files}, indent=1))
