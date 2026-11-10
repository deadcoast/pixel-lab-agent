"""Verify predecessor recovery from Git blobs plus retained ignored files."""

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / "baseline-untracked.json").read_bytes())
predecessor = ROOT / manifest["base"]
expected = json.loads((predecessor.parent / "record.json").read_bytes())["artifacts"]
revision = manifest["source_revision"]
archive = HERE / manifest["archive"]
assert hashlib.sha256(archive.read_bytes()).hexdigest() == manifest["sha256"]
tracked = {}
for row in subprocess.check_output(["git", "ls-tree", "-rz", revision, "--", manifest["base"]], cwd=ROOT).split(b"\0"):
    if row:
        meta, path = row.split(b"\t", 1)
        tracked[path.decode().removeprefix(manifest["base"] + "/")] = meta.split()[2].decode()
selected = {name: tracked[name] for name in expected if name in tracked}
batch = subprocess.run(["git", "cat-file", "--batch"], input=("\n".join(selected.values()) + "\n").encode(),
                       stdout=subprocess.PIPE, check=True, cwd=ROOT).stdout
cursor, failures = 0, []
for name in selected:
    end = batch.index(b"\n", cursor)
    header = batch[cursor:end].split()
    size = int(header[2])
    data = batch[end + 1:end + 1 + size]
    cursor = end + 2 + size
    if hashlib.sha256(data).hexdigest() != expected[name]:
        failures.append(name)
missing = set(expected) - set(selected)
with zipfile.ZipFile(archive) as saved:
    for name in missing:
        if name not in manifest["files"] or hashlib.sha256(saved.read(name)).hexdigest() != expected[name]:
            failures.append(name)
result = {"status": "pass" if not failures else "fail", "source_revision": revision,
          "original_inputs": len(expected), "git_blob_inputs": len(selected), "archive_inputs": len(missing),
          "failures": failures, "scope": "Exact original record inputs recover from committed blobs and retained ZIP; no original files modified."}
target = HERE / "baseline-recovery-check.json"
with target.open("x", encoding="utf-8") as stream:
    json.dump(result, stream, indent=2)
    stream.write("\n")
print(json.dumps(result))
raise SystemExit(bool(failures))
