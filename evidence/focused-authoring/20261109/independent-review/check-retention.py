"""Check frozen native archives and the separate maintainer continuation."""
import hashlib
import json
import sys
from pathlib import Path

root = Path.cwd()
sys.path.insert(0, str(root))
from pixl import codec, graph, plar, store

base = root / "evidence/focused-authoring/20261109"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


archives = []
for path in sorted((base / "archives").glob("*-manifest.json")):
    manifest = read(path)
    attempt = root / manifest["attempt"]
    archive = path.parent / manifest["archive"]
    changes = [name for name, digest in manifest["files"].items()
               if not (attempt / name).is_file() or sha(attempt / name) != digest]
    assert not changes, changes
    assert sha(archive) == manifest["archive_sha256"]
    archives.append({"attempt": manifest["attempt"], "files": len(manifest["files"]), "archive_sha256": manifest["archive_sha256"], "unchanged": True})

source = base / "native/codex-provenance-01/project"
current = base / "current/project"
folder = ".pixl/assets/queue.ready"
before, after = store.load(source / folder), store.load(current / folder)
graph.validate(after, current)
task = "provenance-correction.working.task"
assert set(before.records) == set(after.records)
assert all(row == after.records[ident] for ident, row in before.records.items() if ident != task)
changed_fields = [key for key, value in before.records[task].fields.items() if after.records[task].fields[key] != value]
assert changed_fields == ["ca"]
changed_files = [path.relative_to(source).as_posix() for path in source.rglob("*")
                 if path.is_file() and "__pycache__" not in path.parts
                 and (not (current / path.relative_to(source)).is_file() or sha(path) != sha(current / path.relative_to(source)))]
assert changed_files == [folder + "/state.px"]
summary = read(base / "current/CURRENT-HANDOFF.json")
selected = plar.read(current, "authoring-plar.txt", "queue.working")
handoff_path = current / summary["handoff"]["path"]
handoff = read(handoff_path)
assert sha(handoff_path) == summary["handoff"]["sha256"]
assert summary["state_after"] == codec.digest(after) == handoff["resume"]["state_hash"]
assert handoff["resume"] == selected["production"]["continuation"]
result = {"archives": archives, "current_state": codec.digest(after), "changed_record": task,
          "changed_fields": changed_fields, "changed_original_files": changed_files,
          "handoff_current_and_exact": True, "graph_and_files_valid": True,
          "scope": "Retention, exact state and continuation; no change to visual verdicts or acceptance."}
(Path(__file__).with_name("retention-checks.json")).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
