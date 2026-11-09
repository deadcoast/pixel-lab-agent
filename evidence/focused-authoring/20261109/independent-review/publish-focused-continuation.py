"""Nominate the reviewed open candidate without altering native trial evidence."""
import json
import shutil
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from pixl import codec, graph, plar, service, store

repo = Path.cwd()
base = repo / "evidence/focused-authoring/20261109"
source = base / "native/codex-provenance-01/project"
root = base / "current/project"
if not root.exists():
    shutil.copytree(source, root, ignore=shutil.ignore_patterns("__pycache__"))
work = root / "work/current-handoff"
work.mkdir(parents=True, exist_ok=True)
folder = ".pixl/assets/queue.ready"
before = store.load(source / folder)
old_hash = codec.digest(before)
doc = deepcopy(before)
task_id = "provenance-correction.working.task"
candidate = "provenance-correction.working.candidate"
assert doc.records[task_id].fields["ca"] == []
assert doc.records[candidate].fields["of"].id == "provenance-correction.working.output"
assert doc.records["provenance.working.motion.unavailable"].fields["st"].value == "unavailable"
doc.records[task_id].fields["ca"] = [codec.Ref(candidate)]
doc.revision += 1
payload = {"format": doc.format, "revision": doc.revision,
           "records": [{"id": r.id, "kind": r.kind, "fields": codec.to_data(r.fields)} for r in doc.records.values()]}


def save(name, value):
    path = work / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"path": path.relative_to(root).as_posix(), "sha256": sha256(path.read_bytes()).hexdigest()}


save("nomination-document.json", payload)
if not (work / "commit.json").exists():
    result = service.call("pixl_commit", {"store": folder, "expect": old_hash, "document": payload}, root)
    save("commit.json", result)
after = store.load(root / folder)
assert codec.digest(after) == codec.digest(doc)
assert all(record == after.records[ident] for ident, record in before.records.items() if ident != task_id)
assert after.records[task_id].fields["st"].value == "open"
flow = service.workflow(root / folder / "state.px", root)
working = next(t for t in flow["tasks"] if t["id"] == task_id)
statuses = [q["status"] for q in working["outputs"][0]["requirements"]]
assert statuses.count("pass") == 7 and statuses.count("unavailable") == 1, statuses
save("workflow.json", flow)
details = json.loads((root / "work/provenance-correction/working-handoff-details.json").read_text(encoding="utf-8"))
details["nomination"] = {"candidate": candidate, "by": "maintainer continuation", "reason": "Expose the already reviewed candidate and its unavailable motion criterion in the active workflow; nomination is not acceptance."}
details["caller_actions"][0] = "Assess the retained playback/frame evidence with a suitable visual review route for the exact motion-continuity criterion; retain a superseding verdict only when supported. No universal human-only requirement is introduced."
selected = plar.read(root, "authoring-plar.txt", "queue.working")
handoff = service.call("pixl_plar_handoff", {"path": "authoring-plar.txt", "asset_id": "queue.working", "requirements_hash": selected["requirements_hash"], "expect": selected["production"]["continuation"]["state_hash"], "details": details}, root)
save("handoff.json", handoff)
graph.validate(after, root)
summary = {
    "observed_at": datetime.now(timezone.utc).isoformat(),
    "source_attempt": "native/codex-provenance-01", "state_before": old_hash,
    "state_after": codec.digest(after), "revision": after.revision,
    "only_record_changed": task_id, "only_field_changed": "ca",
    "working": {"candidate": candidate, "state": "open", "passes": 7, "unavailable": 1},
    "retry_paused": "done under corrected source bindings", "family": "open; depends on Working",
    "handoff": handoff, "limits": "Maintainer nomination repair, not an unassisted native completion. No verdict, source, image, request or acceptance changed.",
}
save("CURRENT-HANDOFF.json", summary)
(base / "current/CURRENT-HANDOFF.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
