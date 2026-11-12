"""Caller-side read-only snapshot: hash every file under the consumer root
except work/asset-lineage (the only directory this assignment may add to).

usage: python -I caller_snapshot.py <root> <out.json>
"""
import hashlib
import json
import os
import sys

root = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2])
skip = os.path.join(root, "work", "asset-lineage")

entries = {}
for dirpath, dirnames, filenames in os.walk(root):
    if os.path.abspath(dirpath).startswith(skip):
        dirnames[:] = []
        continue
    for name in filenames:
        full = os.path.join(dirpath, name)
        rel = os.path.relpath(full, root).replace(os.sep, "/")
        h = hashlib.sha256()
        with open(full, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        entries[rel] = {"sha256": h.hexdigest(), "bytes": os.path.getsize(full)}

doc = {
    "root": root,
    "excluded": "work/asset-lineage",
    "file_count": len(entries),
    "files": dict(sorted(entries.items())),
}
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(doc, fh, indent=2)
print(json.dumps({"file_count": len(entries), "out": out}))
