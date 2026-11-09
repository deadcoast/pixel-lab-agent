"""Hash every file under the consumer root except work/continuation and __pycache__; print JSON {files:{relpath:sha256}}.

Usage: python -I work/continuation/hash_tree.py ROOT OUT.json
Used by the caller to prove that no retained file changed during the continuation phase.
"""
import hashlib
import json
import os
import sys

root = os.path.abspath(sys.argv[1])
out = sys.argv[2]
files = {}
for base, dirs, names in os.walk(root):
    rel_base = os.path.relpath(base, root).replace(os.sep, "/")
    dirs[:] = [d for d in dirs if d != "__pycache__" and not (rel_base == "work" and d == "continuation")]
    for name in sorted(names):
        path = os.path.join(base, name)
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        with open(path, "rb") as handle:
            files[rel] = hashlib.sha256(handle.read()).hexdigest()
with open(out, "w", encoding="utf-8", newline="\n") as handle:
    json.dump({"root": root, "count": len(files), "files": files}, handle, indent=1, sort_keys=True)
    handle.write("\n")
print(json.dumps({"out": out, "count": len(files)}))
