"""Pre-fix probe: closed inspection equivalence must preserve JSON scalar types."""

import hashlib
import json
import shutil
import tempfile
from pathlib import Path

from pixl import codec, graph, inspection, store
from tests.inspection_support import options, project

results = []
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    project(root)
    folder = root / ".pixl"
    inspection.prepare(
        folder, codec.digest(store.load(folder)), "candidate", "packet", options(), root
    )
    doc = store.load(folder)
    doc.records["packet"].fields["mt"]["version"] = True
    graph.validate(doc, root)
    report = inspection.report(doc, root, "packet")
    results.append(
        {
            "mutation": "packet metadata version true instead of integer 1",
            "accepted": report["files_verified"],
        }
    )
    doc = store.load(folder)
    artifact = doc.records["packet"]
    old_path = root / artifact.fields["ur"]
    manifest = json.loads(old_path.read_bytes())
    manifest["rendering"]["views"][0]["width"] = float(
        manifest["rendering"]["views"][0]["width"]
    )
    data = inspection._bytes(manifest)
    sha = hashlib.sha256(data).hexdigest()
    new_dir = old_path.parent.parent / sha
    shutil.copytree(old_path.parent, new_dir)
    (new_dir / "manifest.json").write_bytes(data)
    old_prefix = old_path.parent.relative_to(root).as_posix() + "/"
    new_prefix = new_dir.relative_to(root).as_posix() + "/"
    for record in doc.records.values():
        if record.kind == "X" and record.fields["ur"].startswith(old_prefix):
            record.fields["ur"] = new_prefix + record.fields["ur"][len(old_prefix) :]
    artifact.fields["dg"] = sha
    graph.validate(doc, root)
    report = inspection.report(doc, root, "packet")
    results.append(
        {
            "mutation": "view width 32.0 instead of integer 32 in canonical rehashed manifest",
            "accepted": report["files_verified"],
            "returned_width": report["packets"][0]["views"][0]["width"],
        }
    )
print(
    json.dumps(
        {
            "source_sha256": hashlib.sha256(
                Path("pixl/inspection.py").read_bytes()
            ).hexdigest(),
            "results": results,
        },
        indent=2,
    )
)
