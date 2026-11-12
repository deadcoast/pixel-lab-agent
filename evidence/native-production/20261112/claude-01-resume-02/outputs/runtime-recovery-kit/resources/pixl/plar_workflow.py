"""Connect PLAR requirements to retained production without inventing acceptance."""

from . import codec, graph, jobs, lifecycle, store
from .codec import PixlError


def _family_destination(root, destination, members):
    """Observe only the manifest's exact consumer paths, never guessed filenames."""
    files, seen = [], set()
    for member in members:
        path = graph.confined(root, member["source_path"])
        within = path != destination and path.is_relative_to(destination)
        duplicate = path in seen
        seen.add(path)
        present = within and not duplicate and path.is_file()
        observed = graph.file_hash(path) if present else None
        size = path.stat().st_size if present else None
        files.append({
            "output": member["output"], "candidate": member["candidate"],
            "source_path": member["source_path"], "within_destination": within,
            "duplicate_destination": duplicate, "expected_sha256": member["sha256"],
            "observed_sha256": observed, "expected_bytes": member["bytes"],
            "observed_bytes": size,
            "destination_matches": present and observed == member["sha256"] and size == member["bytes"],
        })
    return files, destination.is_dir() and bool(files) and all(row["destination_matches"] for row in files)


def _delivery_status(document, root, folder, asset, output_id, outputs):
    """Report the exact nominated bytes and collective plans, without new verdicts."""
    from . import asset_lineage, delivery
    from .plar import selection_bindings

    output = next(row for row in outputs if row["id"] == output_id)
    candidate_id = output["candidate"]
    destination = graph.confined(root, asset["delivery"]["path"])
    expected = document.records[candidate_id].fields["dg"] if candidate_id else None
    observed = graph.file_hash(destination) if destination.is_file() else None
    matching = expected is not None and observed == expected
    related = {
        record.id
        for record in document.records.values()
        if record.kind == "F"
        and any(member.id == output_id for member in record.fields.get("mb", []))
    }
    linked_family = "mb" in document.records[output_id].fields
    if linked_family:
        related.add(output_id)
    families = []
    lineage = None
    destination_files = None
    if related:
        for row in delivery.report(document, root)["families"]:
            if row["output"] not in related:
                continue
            snapshot = next((s for s in row["snapshots"] if s["candidate"] == row["candidate"]), None)
            for member in row["members"]:
                if member["output"] == output_id and member["candidate"] == candidate_id:
                    lineage = member["lineage"]
            # The baseline may intentionally retain a historical sample contract.
            # Newly produced siblings must still match their explicit live selections.
            member_bindings = [
                binding
                for member in row["members"]
                if member["output"] != row["baseline"]["output"]
                for binding in selection_bindings(document, member["task"], root, folder)
            ]
            members_current = all(b["status"] == "current" and b.get("selected_for_asset", True) for b in member_bindings)
            accepted = (
                row["state"] == "done" and not row["pending_jobs"]
                and bool(snapshot) and not snapshot["stale"]
                and all(q["status"] == "pass" for q in row["requirements"])
                and members_current
            )
            families.append({"output": row["output"], "task": row["task"], "state": row["state"], "candidate": row["candidate"], "accepted": accepted,
                             "member_selection_current": members_current,
                             "manifest": snapshot["manifest"] if snapshot else None,
                             "manifest_sha256": snapshot["sha256"] if snapshot else None,
                             "members": [dict(member) for member in snapshot["files"]] if snapshot else []})
            if row["output"] == output_id and not destination.is_file():
                destination_files, matching = _family_destination(root, destination, snapshot["files"] if snapshot else [])
                # A directory has no single artifact digest. The family entry
                # separately identifies the verified manifest and each member.
                expected = observed = None
    if candidate_id is not None and lineage is None:
        lineage = asset_lineage.describe(document, root, candidate_id)
    result = {
        "destination": asset["delivery"]["path"], "candidate": candidate_id, "lineage": lineage,
        "expected_sha256": expected, "observed_sha256": observed,
        "destination_matches": matching, "families": families,
        "complete": matching and all(row["accepted"] for row in families),
        "scope": "Current nominated file bytes or exact manifest member paths beneath the declared directory, and acceptance of the linked/containing families; only the declared criteria are established.",
    }
    if destination_files is not None:
        result.update(destination_kind="directory", destination_files=destination_files)
    return result


def owned_tasks(document, root, path, asset_id):
    """Select explicit asset bindings; never infer ownership from a task name."""
    result = []
    for task in document.records.values():
        if task.kind != "T":
            continue
        for reference in task.fields["ip"]:
            metadata = document.records[reference.id].fields.get("mt", {})
            if (
                metadata.get("binding") == "pixl.plar.selection/1"
                and metadata.get("asset_id") == asset_id
                and isinstance(metadata.get("plar_path"), str)
                and graph.confined(root, metadata["plar_path"])
                == graph.confined(root, path)
            ):
                result.append(task.id)
                break
    return result


def current_bindings(document, task_id, root, folder=None):
    from .plar import selection_bindings
    from .production_plan import blockers as plan_blockers

    reasons = plan_blockers(document, task_id, root, folder)
    if reasons:
        raise PixlError("production_plan", "; ".join(reasons))

    bindings = selection_bindings(document, task_id, root, folder)
    changed = [
        b
        for b in bindings
        if b["status"] != "current" or not b.get("selected_for_asset", True)
    ]
    if changed:
        raise PixlError(
            "plar_selection",
            f"{task_id}: current consumer requirements differ or are unavailable; retain the old review and compare a revised contract",
        )
    return bindings


def report(root, selected, path):
    """Read one asset's production, including interrupted link publication."""
    asset = selected["asset"]
    link = asset.get("production")
    relative = link["store"] if link else f".pixl/assets/{asset['id']}"
    folder = graph.confined(root, relative)
    result = {"store": relative, "link_status": "linked" if link else "unlinked"}
    if not (folder / "state.px").is_file():
        return {
            **result,
            "status": "missing" if link else "not_started",
            "next_action": "restore_linked_state" if link else "prepare",
            "new_request_allowed": not bool(link),
        }
    try:
        document = store.load(folder)
        graph.validate(document, root)
        if document.format != 2:
            raise PixlError("plar_production", "linked production must be PX2")
        owned = owned_tasks(document, root, path, asset["id"])
        if link:
            task_id = link["task"]
            task = document.records.get(task_id)
            output = document.records.get(link["output"])
            if (
                task is None
                or task.kind != "T"
                or output is None
                or output.kind != "F"
                or output.fields["tk"].id != task_id
            ):
                raise PixlError(
                    "plar_production",
                    "linked task/output do not describe the same production work",
                )
            # Legacy authored projects may have no opt-in selection input.
            tagged = any(
                document.records[r.id].fields.get("mt", {}).get("binding")
                == "pixl.plar.selection/1"
                for r in task.fields["ip"]
            )
            if tagged and task_id not in owned:
                raise PixlError(
                    "plar_production", "linked task belongs to another asset selection"
                )
            owned = sorted(set(owned) | {task_id})
        elif len(owned) == 1:
            task_id = owned[0]
            result["link_status"] = "discovered"
        else:
            raise PixlError(
                "plar_production",
                "unlinked state has no unique owned task; inspect and explicitly link the retained work",
            )
        from .plar import selection_bindings

        task = document.records[task_id]
        bindings = selection_bindings(document, task_id, root, folder)
        current = bool(bindings) and all(
            b["status"] == "current" and b.get("selected_for_asset", True)
            for b in bindings
        )
        report_jobs = jobs.report(document, root, folder)["jobs"]
        relevant = [
            j for j in report_jobs if document.records[j["id"]].fields["tk"].id in owned
        ]
        pending = [j for j in relevant if j["state"] in jobs.PENDING]
        rows = []
        for job in relevant:
            request = job.get("request", {})
            rows.append(
                {
                    k: job[k]
                    for k in ("id", "state", "remote_id", "next_action", "durable")
                }
                | {
                    "task": document.records[job["id"]].fields["tk"].id,
                    "provider": request.get("provider"),
                    "tool": request.get("tool"),
                    "discovery": request.get("discovery"),
                    "stale": job.get("stale", []),
                    "blockers": job.get("blockers", []),
                    "candidates": job.get("candidates", []),
                }
            )
        action = "review_contract" if not current else "inspect_or_revise"
        active_jobs = [
            j for j in relevant if document.records[j["id"]].fields["tk"].id == task_id
        ]
        successful = [j for j in active_jobs if j["state"] == "succeeded"]
        if current and successful:
            action = (
                "review_candidates"
                if any(j.get("candidates") for j in successful)
                else "retrieve_and_import"
            )
        if task.fields["st"].value == "done" and current:
            action = "review_delivery"
        workflow = next(
            t for t in lifecycle.report(document)["tasks"] if t["id"] == task_id
        )
        delivered = None
        if task.fields["st"].value == "done" and current and link:
            delivered = _delivery_status(document, root, folder, asset, link["output"], workflow["outputs"])
            if delivered["complete"]:
                action = "delivered"
        if pending:
            action = (
                "reconcile"
                if any(j["state"] == "unknown" for j in pending)
                else "observe"
                if any(j["state"] in {"submitted", "running"} for j in pending)
                else "dispatch"
                if current and all(j["next_action"] == "dispatch" for j in pending)
                else "resolve_prepared_intent"
            )
        prerequisites = [
            {
                "job": j["id"],
                "action": j["next_action"],
                "requirement": "Resolve this retained attempt on its originating connection before preparing another request for this asset.",
            }
            for j in pending
        ]
        if not pending and successful and task.fields["st"].value != "done":
            prerequisites.extend(
                {
                    "job": j["id"],
                    "action": "review_candidates"
                    if j.get("candidates")
                    else "retrieve_and_import",
                    "requirement": "Inspect this retained result or record its actual unavailability before deciding whether a corrective request is needed.",
                }
                for j in successful
            )

        return {
            **result,
            "status": "available",
            "state": str(folder / "state.px"),
            "hash": codec.digest(document),
            "revision": document.revision,
            "task": task_id,
            "task_state": task.fields["st"].value,
            "outputs": workflow["outputs"],
            "delivery": delivered,
            "selection_bindings": bindings,
            "selection_current": current,
            "jobs": rows,
            "pending_jobs": [j["id"] for j in pending],
            "next_action": action,
            "continuation": {
                "store": relative,
                "state_hash": codec.digest(document),
                "asset_id": asset["id"],
                "requirements_hash": selected["requirements_hash"],
                "task": task_id,
                "action": action,
                "delivery": delivered,
                "jobs": [
                    {
                        k: row[k]
                        for k in (
                            "id",
                            "task",
                            "state",
                            "provider",
                            "remote_id",
                            "next_action",
                            "discovery",
                        )
                    }
                    for row in rows
                    if row["id"] in {j["id"] for j in pending} or row["task"] == task_id
                ],
                "before_another_request": prerequisites,
                "after_observation": {
                    "succeeded": "Retrieve the actual result and import it against this job's saved output plan; then review the candidate.",
                    "failed": "Retain the failure, compare the current contract and decide whether an explicit new request is needed.",
                    "pending_or_unknown": "Continue observation or reconciliation of the same attempt; retain its provider identity.",
                },
                "refresh": "Reread focused PLAR after any observation or state change before following the next operation.",
                "scope": "Derived local continuation, not a provider call, authorization or acceptance verdict.",
            },
            "link_action": "save_production_link" if not link else None,
            "new_request_allowed": current and not pending,
            "scope": "Observed local state and caller-supplied provider evidence; allocation status is not art or renderer acceptance.",
        }
    except (PixlError, OSError, ValueError) as error:
        return {
            **result,
            "status": "unavailable",
            "reason": str(error),
            "next_action": "inspect_retained_state",
            "new_request_allowed": False,
        }


def synchronize(root, selected, path, folder, task_id, outputs, marker_path):
    """CAS link one output after its job exists; preserve all unrelated allocation data."""
    from . import plar

    if len(outputs) != 1:
        return {
            "status": "needs_output_link",
            "reason": "Multiple outputs: explicitly choose the PLAR delivery output; all task outputs remain required.",
        }
    link = {
        "store": folder.relative_to(root).as_posix(),
        "task": task_id,
        "output": outputs[0],
    }
    if selected["asset"].get("production") == link:
        return {"status": "unchanged", "production": link}
    try:
        document, digest = plar._load(graph.confined(root, path))
        if digest != selected["hash"]:
            raise PixlError(
                "stale_write",
                "allocation changed during preparation; reread before linking the retained job",
            )
        asset = next(
            a for a in document["assets"] if a["id"] == selected["asset"]["id"]
        )
        asset.update(
            production=link,
            status="in_progress",
            next="Read this asset's production status; use its retained job action before another request.",
        )
        evidence = {
            "path": marker_path,
            "note": "Retained requirements, reviewed request and candidate plan; not asset acceptance.",
        }
        if evidence not in asset["evidence"]:
            asset["evidence"].append(evidence)
        saved = plar.save(root, document, digest, path)
        return {"status": "linked", "hash": saved["hash"], "production": link}
    except (PixlError, OSError) as error:
        return {
            "status": "needs_reconciliation",
            "production": link,
            "reason": str(error),
            "next": "The plan/job are retained. Reread PLAR and link this work; do not create another job.",
        }
