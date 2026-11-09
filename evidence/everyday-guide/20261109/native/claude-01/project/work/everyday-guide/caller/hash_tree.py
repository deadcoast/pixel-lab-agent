"""Caller helper: SHA-256 every file under a consumer root, excluding work/everyday-guide and .git."""
import hashlib
import json
import os
import sys

root = sys.argv[1]
out = sys.argv[2]
skip = {os.path.normpath(os.path.join(root, "work", "everyday-guide"))}
res = {}
for dp, dns, fns in os.walk(root):
    dns[:] = [d for d in dns if os.path.normpath(os.path.join(dp, d)) not in skip and d != ".git"]
    for fn in fns:
        p = os.path.join(dp, fn)
        rel = os.path.relpath(p, root).replace(os.sep, "/")
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        res[rel] = {"sha256": h.hexdigest(), "bytes": os.path.getsize(p)}
with open(out, "w", encoding="utf-8") as f:
    json.dump({"root": os.path.abspath(root), "excluded": ["work/everyday-guide", ".git"], "files": res}, f, indent=1, sort_keys=True)
print(len(res), "files hashed ->", out)
