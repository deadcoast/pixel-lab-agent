"""Hash every project file (optionally excluding prefixes) into a JSON map. Run with -I."""
import hashlib, json, os, sys
root, out = sys.argv[1], sys.argv[2]
exclude = tuple(sys.argv[3:])
files = {}
for dp, dn, fn in os.walk(root):
    for f in fn:
        p = os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
        if any(p.startswith(e) for e in exclude):
            continue
        with open(os.path.join(root, p), "rb") as h:
            files[p] = hashlib.sha256(h.read()).hexdigest()
json.dump({"root": os.path.abspath(root), "excluded_prefixes": list(exclude), "count": len(files), "files": files}, open(out, "w", encoding="utf-8"), indent=1, sort_keys=True)
print(out, len(files))
