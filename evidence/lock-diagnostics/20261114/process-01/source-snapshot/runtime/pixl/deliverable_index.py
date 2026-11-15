"""Consumer projection of verified family packages; no new publication or acceptance."""

from pathlib import Path
from urllib.parse import urlsplit

from . import codec, delivery, graph, lifecycle, plar, retention
from .codec import PixlError


def report(doc, root, output_id, state_path, candidate_id=None):
    """Read one selected package and its current review without hiding drift."""
    if not output_id:
        raise PixlError("deliverable_output", "consumer view requires an explicit family output")
    root = Path(root).resolve()
    state = Path(state_path).resolve()
    if not state.is_relative_to(root) or state == root:
        raise PixlError("path_escape", "consumer index state must be inside the project root")
    relative = state.relative_to(root).as_posix()
    family_report = delivery.report(doc, root, output_id)
    family = family_report["families"][0]
    selected = candidate_id if candidate_id is not None else family["candidate"]
    snapshot = next((row for row in family["snapshots"] if row["candidate"] == selected), None)
    if selected is not None and snapshot is None:
        raise PixlError("deliverable_candidate", "select a retained snapshot candidate belonging to this family output")
    workflow = lifecycle.report(doc)
    tasks = {row["id"]: row for row in workflow["tasks"]}
    outputs = {row["id"]: row for task in tasks.values() for row in task["outputs"]}
    unresolved = []

    def issue(code, subject, detail):
        row = {"code": code, "subject": subject, "detail": detail}
        if row not in unresolved:
            unresolved.append(row)

    def review(output, candidate):
        owner = doc.records[output].fields["tk"].id
        current = outputs[output]
        row = next((item for item in current["candidates"] if item["id"] == candidate), None)
        requirements = row["requirements"] if row else current["requirements"]
        for requirement in requirements:
            if requirement["status"] != "pass":
                issue("review_" + requirement["status"], candidate or output,
                      {key: requirement[key] for key in ("id", "check", "domain", "status", "reason", "verdict")})
        nominated = candidate is not None and current["candidate"] == candidate
        if not nominated:
            issue("not_nominated", candidate or output, "This package candidate is not the current nominee for its output.")
        if tasks[owner]["state"] != "done":
            issue("task_incomplete", owner, tasks[owner]["state"])
        return {"task": owner, "task_state": tasks[owner]["state"],
                "nominated": nominated, "current_candidate": current["candidate"],
                "requirements": requirements,
                "all_required_pass": bool(requirements) and all(q["status"] == "pass" for q in requirements)}

    selected_review = review(output_id, selected)
    for blocker in family["blockers"]:
        issue("family_blocker", output_id, blocker)
    for reason in family["baseline"]["reasons"]:
        issue("baseline_ineligible", family["baseline"]["candidate"], reason)
    for job in family["pending_jobs"]:
        issue("pending_job", job["id"], {"task": job["task"], "state": job["state"]})
    bindings = []
    # The accepted sample may intentionally retain a historical PLAR selection.
    selected_tasks = {family["task"], *(
        row["task"] for row in family["members"]
        if row["output"] != family["baseline"]["output"]
    )}
    for task_id in sorted(selected_tasks):
        for binding in plar.selection_bindings(doc, task_id, root, state.parent):
            row = {"task": task_id, **binding}
            bindings.append(row)
            if row["status"] != "current" or not row.get("selected_for_asset", True):
                issue("selection_not_current", task_id, row)

    assets = []
    package = None
    saved_bindings = {}
    choices = {item["id"]: {"family_destination"} for item in family["destinations"]}
    if snapshot is None:
        issue("package_unselected", output_id, "No family snapshot is nominated; select an explicit retained candidate to inspect unfinished work.")
    else:
        artifact = doc.records[selected]
        manifest = delivery._manifest(doc, artifact, root)
        saved_bindings = manifest["plan"]["bindings"]
        for choice in manifest["plan"]["destinations"]:
            choices.setdefault(choice, set()).add("snapshot_destination")
        directory = Path(snapshot["manifest"]).parent
        for reason in snapshot["stale"]:
            issue("package_stale", selected, reason)
        package = {"candidate": selected, "path": directory.as_posix(),
                   "manifest": snapshot["manifest"], "sha256": snapshot["sha256"],
                   "created_at": snapshot["created_at"],
                   "source_state_sha256": snapshot["source_state_sha256"],
                   "creation_acceptance": {"accepted": manifest["acceptance"]["accepted"],
                                           "source_status_pointer": "/acceptance/source_status"},
                   "stale": snapshot["stale"]}
        for member in snapshot["files"]:
            candidate = doc.records[member["candidate"]]
            output = doc.records[member["output"]]
            contract = None
            if reference := candidate.fields.get("ct"):
                record = doc.records[reference.id]
                current_hash = codec.record_hash(record)
                saved_hash = manifest["plan"]["bindings"].get(reference.id)
                contract = {"id": reference.id, "record_sha256": current_hash,
                            "saved_record_sha256": saved_hash, "current_binding": current_hash == saved_hash,
                            "declared": codec.to_data(record.fields)}
                for choice in record.fields.get("ch", []):
                    choices.setdefault(choice.id, set()).add("member_contract")
            metadata = candidate.fields.get("mt")
            assets.append({
                "output": output.id, "output_name": output.fields["nm"],
                "output_record_sha256": codec.record_hash(output),
                "saved_output_record_sha256": saved_bindings.get(output.id),
                "output_current_binding": codec.record_hash(output) == saved_bindings.get(output.id),
                "candidate": candidate.id, "name": candidate.fields["nm"],
                "kind": candidate.fields["kd"].value,
                "path": (directory / member["path"]).as_posix(),
                "package_path": member["path"], "source_path": member["source_path"],
                "sha256": member["sha256"], "bytes": member["bytes"],
                "record_sha256": member["record_sha256"],
                "contract": contract,
                "metadata": {"basis": "declared_opaque", "present": metadata is not None,
                             "value": codec.to_data(metadata),
                             "layout_status": "not_interpreted" if metadata is not None else "not_declared"},
                "review": review(output.id, candidate.id), "lineage": member["lineage"],
            })
    choice_rows, source_ids = [], set()
    for id_, roles in sorted(choices.items()):
        record = doc.records[id_]
        source_ids.update(reference.id for reference in record.fields["so"])
        choice_rows.append({"id": id_, "roles": sorted(roles),
                            **next(row for row in workflow["intake"] if row["id"] == id_),
                            "record_sha256": codec.record_hash(record),
                            "saved_record_sha256": saved_bindings.get(id_),
                            "current_binding": codec.record_hash(record) == saved_bindings.get(id_) if snapshot else None})
    source_rows = []
    for id_ in sorted(source_ids):
        record = doc.records[id_]
        fields = record.fields
        row = {"id": id_, "uri": fields["ur"], "sha256": fields["dg"],
               "lines": fields["ln"], "authority": fields["au"].value,
               "record_sha256": codec.record_hash(record),
               "saved_record_sha256": saved_bindings.get(id_),
               "current_binding": codec.record_hash(record) == saved_bindings.get(id_) if snapshot else None}
        if urlsplit(fields["ur"]).scheme in ("http", "https"):
            row.update(path=None, bytes=None, observed_sha256=None, status="remote_not_observed")
            issue("integration_source_unavailable", id_, "Remote source bytes were not observed; this local view performs no remote requests.")
        else:
            resolved = retention.resolve(root, fields["ur"], fields["dg"])
            observed = graph.file_hash(resolved)
            if observed != fields["dg"]:
                raise PixlError("file_hash", id_)
            row.update(path=resolved.relative_to(root).as_posix(), bytes=resolved.stat().st_size,
                       observed_sha256=observed,
                       status="declared_location" if resolved == graph.confined(root, fields["ur"]) else "retained_revision")
        source_rows.append(row)
    # Eligibility is a fresh local state observation, never a new verdict, delivery
    # assertion, or claim about undeclared target-engine/human acceptance.
    eligible = snapshot is not None and not unresolved
    refresh = {"path": relative, "output": output_id, "view": "consumer"}
    if candidate_id is not None:
        refresh["candidate"] = candidate_id
    return {
        "schema": "pixl.deliverable-index/1", "view": "consumer", "format": 2,
        "revision": doc.revision, "hash": codec.digest(doc), "state": relative,
        "family": {"output": output_id, "name": doc.records[output_id].fields["nm"],
                   "record_sha256": codec.record_hash(doc.records[output_id]),
                   "saved_record_sha256": saved_bindings.get(output_id),
                   "current_binding": codec.record_hash(doc.records[output_id]) == saved_bindings.get(output_id) if snapshot else None,
                   "selected_candidate": selected, **selected_review,
                   "current_eligible": eligible, "destinations": family["destinations"]},
        "package": package, "assets": assets, "unresolved": unresolved,
        "integration": {"choices": choice_rows, "sources": source_rows,
                        "scope": "Declared destination and selected member-contract choices with exact supporting source locators. Choice values may name consumer modules; the index does not infer a universal layout or execute those modules."},
        "pending_jobs": family["pending_jobs"], "selection_bindings": bindings,
        "files_verified": True,
        "history": {"state": relative, "manifest": package["manifest"] if package else None,
                    "operation": "pixl_family", "arguments": {"path": relative, "output": output_id}},
        "refresh": {"operation": "pixl_family", "arguments": refresh},
        "scope": {
            "paths": "All paths are project-relative except package_path, which is relative to the immutable package directory. source_path is the recorded source, not a verified destination import.",
            "metadata": "Contract values and X.mt are declared data. Opaque metadata has no universal frame/layout schema; missing or uninterpreted layout is not inferred from filenames, kind, dimensions or lineage.",
            "review": "Current criteria apply to the selected exact candidates. Package creation accepted=false remains historical; current_eligible requires current nomination, completed tasks, passing declared criteria, current bindings and no pending work or drift.",
            "acceptance": "This read creates no acceptance and does not observe destination bytes, authenticate remote execution, or establish undeclared engine or human acceptance. Refresh after changes; full history remains in the existing state and manifest.",
        },
    }
