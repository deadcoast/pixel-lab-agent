"""Check saved successor state, provenance, preservation and acceptance boundaries."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pixl import codec, graph, plar, service, store

name = sys.argv[1]
attempt = ROOT / "evidence/focused-authoring/20261109/native" / name
project, before = attempt / "project", attempt / "input-project"
folder = ".pixl/assets/queue.ready"
old, doc = store.load(before / folder), store.load(project / folder)
graph.validate(doc, project)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


old_changes = []
for ident, record in old.records.items():
    actual = doc.records.get(ident)
    if record != actual:
        old_changes.append({"id": ident, "kind": record.kind, "fields": [k for k in record.fields if actual is None or record.fields[k] != actual.fields.get(k)]})
file_changes = []
for p in before.rglob("*"):
    if not p.is_file() or any(part in ("pixl-kit", "__pycache__") for part in p.parts):
        continue
    rel = p.relative_to(before)
    if rel.parts[0] in ("src", "renderer", "renderer-successor", "assets", "work") or rel.name in ("FOCUSED-RESULT.json", "SUCCESSOR-RESULT.json", "plar.txt", "BRIEF.md"):
        if not (project / rel).exists() or sha(p) != sha(project / rel):
            file_changes.append(rel.as_posix())
workflow = service.workflow(project / folder / "state.px", project)
tasks = {t["id"]: t for t in workflow["tasks"]}
old_jobs = {r.id: r for r in old.records.values() if r.kind == "J"}
current_jobs = {r.id: r for r in doc.records.values() if r.kind == "J"}
result = {
    "attempt": name, "before": codec.digest(old), "after": codec.digest(doc),
    "graph_and_files_valid": True, "changed_old_records": old_changes,
    "changed_old_files": file_changes,
    "no_new_jobs": old_jobs == current_jobs,
    "members": [], "active_unsupported_future_sources": [],
}
active_outputs = []
for asset in ("queue.working", "queue.retry", "queue.paused"):
    selected = plar.read(project, "authoring-plar.txt", asset)
    link = selected["asset"]["production"]
    task = tasks[link["task"]]
    output = next(o for o in task["outputs"] if o["id"] == link["output"])
    active_outputs.append(link["output"])
    result["members"].append({"asset": asset, "status": selected["asset"]["status"], "requirements_hash": selected["requirements_hash"], "source_bindings": [s["binding"] for s in selected["sources"]], "task": task["id"], "task_state": task["state"], "candidate": output.get("candidate"), "criteria": [{k:q[k] for k in ("id", "status", "verdict")} for q in output["requirements"]]})
prefix = result["members"][0]["task"].removesuffix(".working.task")
family = tasks[prefix + ".delivery.task"]
active_outputs.append(prefix + ".delivery.output")
result["family"] = {"task": family["id"], "state": family["state"], "blockers": family["blockers"]}
scope = graph.proof_scope(doc, active_outputs)
for ident in sorted(scope):
    record = doc.records[ident]
    if record.kind == "S" and record.fields["at"] == "2026-11-09T20:00:00+00:00":
        result["active_unsupported_future_sources"].append(ident)
result["preservation_valid"] = not file_changes and all(r["kind"] == "P" and set(r["fields"]) <= {"in", "sc", "br"} for r in old_changes)
result["limits"] = "Validates local bindings and recorded outcomes. Does not infer artistic truth from receipts, authenticate host tool claims or close unavailable temporal review."
target = ROOT / "evidence/focused-authoring/20261109/independent-review"
target.mkdir(parents=True, exist_ok=True)
(target / (name + "-state-checks.json")).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k:v for k,v in result.items() if k not in ("members",)}, indent=2))
print([(m["asset"], m["task_state"], [(q["id"],q["status"]) for q in m["criteria"] if q["status"] != "pass"]) for m in result["members"]])
