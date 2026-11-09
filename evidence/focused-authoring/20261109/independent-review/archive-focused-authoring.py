"""Freeze one completed native attempt and verify every archived byte."""
import json
import sys
from hashlib import sha256
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

root = Path(__file__).resolve().parents[1]
base = root / "evidence/focused-authoring/20261109"
source = base / "native" / sys.argv[1]
record = json.loads((source / "record.json").read_text(encoding="utf-8"))
for name, expected in record["artifacts"].items():
    assert sha256((source / "project" / name).read_bytes()).hexdigest() == expected, name
target = base / "archives"
target.mkdir(exist_ok=True)
archive, manifest = target / (source.name + ".zip"), target / (source.name + "-manifest.json")
assert not archive.exists() and not manifest.exists()
files = {}
with ZipFile(archive, "x", compression=ZIP_DEFLATED, compresslevel=6) as output:
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            relative = path.relative_to(source).as_posix()
            files[relative] = sha256(path.read_bytes()).hexdigest()
            output.write(path, relative)
with ZipFile(archive) as retained:
    assert all(sha256(retained.read(name)).hexdigest() == digest for name, digest in files.items())
value = {"attempt": source.relative_to(root).as_posix(), "archive": archive.name,
         "archive_sha256": sha256(archive.read_bytes()).hexdigest(), "files": files,
         "verification": "Each original recorded artifact checked, then every archived file reread and matched."}
manifest.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"attempt": source.name, "files": len(files), "archive_sha256": value["archive_sha256"]}))
