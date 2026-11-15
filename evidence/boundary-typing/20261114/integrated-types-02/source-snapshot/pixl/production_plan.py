"""Author family/stage connections using existing PX2 records and durable jobs."""

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from . import adapter_versions, codec, graph, jobs, plar, platform, store
from .codec import PixlError, Record, Ref, Symbol


def _object(properties, required):
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False,
    }


STR = {"type": "string", "minLength": 1}
ID = {"type": "string", "pattern": "^[a-z][a-z0-9_.-]{0,47}$"}
REFS = {"type": "array", "items": STR, "uniqueItems": True}
CRITERIA = {
    "type": "array",
    "minItems": 1,
    "items": _object(
        {
            "id": ID,
            "check": STR,
            "domain": {
                "enum": ["mechanical", "visual", "continuity", "engine", "other"]
            },
            "mode": {"enum": ["local", "visual", "live"]},
            "sources": REFS,
        },
        ["id", "check", "domain", "mode", "sources"],
    ),
}
SELECTION = _object(
    {"path": STR, "asset": STR, "requirements_hash": STR,
     "replaces": _object({"store": STR, "task": STR, "output": STR}, ["store", "task", "output"])},
    ["path", "asset", "requirements_hash"],
)
SCHEMA = _object(
    {
        "version": {"const": 1, "type": "integer"},
        "id": ID,
        "project": STR,
        "actor": STR,
        "baseline": STR,
        "decisions": REFS,
        "knowledge": REFS,
        "stages": {
            "type": "array",
            "minItems": 0,
            "items": _object(
                {
                    "id": ID,
                    "name": STR,
                    "phase": {"enum": ["sample", "production"]},
                    "kind": {
                        "enum": [
                            "sprite",
                            "animation",
                            "tileset",
                            "atlas",
                            "normal",
                            "material",
                        ]
                    },
                    "contract": STR,
                    "needs": REFS,
                    "criteria": CRITERIA,
                    "selection": SELECTION,
                },
                ["id", "name", "phase", "kind", "contract", "needs", "criteria"],
            ),
        },
        "delivery": _object(
            {"name": STR, "members": REFS, "destinations": REFS, "criteria": CRITERIA},
            ["name", "members", "destinations", "criteria"],
        ),
    },
    [
        "version",
        "id",
        "project",
        "actor",
        "baseline",
        "decisions",
        "knowledge",
        "stages",
        "delivery",
    ],
)
REQUEST_SCHEMA = _object(
    {
        "version": {"const": 1, "type": "integer"},
        "inputs": {
            "type": "object",
            "additionalProperties": _object(
                {"candidate": STR, "sha256": STR}, ["candidate", "sha256"]
            ),
        },
        "request": {"type": "object"},
    },
    ["version", "inputs", "request"],
)


def _require(condition, message):
    if not condition:
        raise PixlError("production_plan", message)


def _validate(value, schema):
    adapter_versions.require_version(
        value, "connected production plan" if schema is SCHEMA else "stage request packet"
    )
    error = next(Draft202012Validator(schema).iter_errors(value), None)
    _require(error is None, error.message if error else "")
    plar._bytes(value)


def _record(doc, ident, kind):
    record = doc.records.get(ident)
    _require(record is not None and record.kind == kind, f"expected {kind}: {ident}")
    return record


def _ids(plan, stage):
    prefix = plan["id"] + "." + stage
    return prefix + ".task", prefix + ".output"


def _output(plan, ident):
    return _ids(plan, ident)[1] if ident in {s["id"] for s in plan["stages"]} else ident


def _selection(root, selection):
    current = plar.read(
        root, selection["path"], selection["asset"], include_production=False
    )
    _require(
        current["requirements_hash"] == selection["requirements_hash"],
        "PLAR requirements changed; compare before authoring",
    )
    _require(
        all(s["binding"] == "current" for s in current["sources"]),
        "PLAR source bytes changed or are unavailable",
    )
    return current


def _task_hash(record):
    return codec.record_hash(
        Record(
            record.id,
            "T",
            {
                k: v
                for k, v in record.fields.items()
                if k not in {"st", "ca", "vr", "ip"}
            },
        )
    )


def _current_plan(doc, marker):
    metadata = marker.fields["mt"]
    for ident, digest in metadata["scope"].items():
        _require(
            ident in doc.records and codec.record_hash(doc.records[ident]) == digest,
            f"authored plan scope changed: {ident}; review and append a new plan",
        )
    for ident, saved in metadata["tasks"].items():
        task = _record(doc, ident, "T")
        _require(
            _task_hash(task) == saved["sha256"]
            and set(saved["inputs"]) <= {r.id for r in task.fields["ip"]},
            f"authored task changed: {ident}; review and append a new plan",
        )


def _snapshot(root, marker):
    """Read one supported immutable plan without upgrading or rewriting it."""
    metadata = marker.fields.get("mt", {})
    adapter_versions.require_binding(metadata.get("binding"), "pixl.production.plan")
    _require(
        isinstance(metadata.get("scope"), dict)
        and all(isinstance(key, str) and isinstance(value, str) for key, value in metadata["scope"].items())
        and isinstance(metadata.get("tasks"), dict)
        and all(
            isinstance(key, str) and isinstance(value, dict)
            and isinstance(value.get("sha256"), str)
            and isinstance(value.get("inputs"), list)
            and all(isinstance(item, str) for item in value["inputs"])
            for key, value in metadata["tasks"].items()
        ),
        "invalid production plan metadata; preserve its saved scope and tasks",
    )
    path = graph.confined(root, marker.fields["ur"])
    _require(graph.file_hash(path) == marker.fields["dg"], "plan snapshot changed")
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    adapter_versions.require_version(snapshot, "production plan snapshot")
    _validate(snapshot.get("plan"), SCHEMA)
    _require(isinstance(snapshot.get("selections"), dict), "plan snapshot needs selections")
    _require(marker.id == snapshot["plan"]["id"] + ".plan", "plan identity mismatch")
    return snapshot


def blockers(doc, task_id, root, folder=None):
    """Check opt-in plan scope and only this stage's downstream allocations."""
    reasons = []
    task = doc.records[task_id]
    for reference in task.fields["ip"]:
        marker = doc.records[reference.id]
        if not adapter_versions.is_binding(marker.fields.get("mt", {}).get("binding"), "pixl.production.plan"):
            continue
        try:
            plan = _snapshot(root, marker)["plan"]
            _current_plan(doc, marker)
            delivery_task = _ids(plan, "delivery")[0]
            for stage in plan["stages"]:
                if "selection" not in stage:
                    continue
                selected_task, selected_output = _ids(plan, stage["id"])
                ancestors, pending = set(), [selected_task]
                while pending:
                    ident = pending.pop()
                    if ident not in ancestors:
                        ancestors.add(ident)
                        pending.extend(r.id for r in doc.records[ident].fields["dp"])
                if task_id != delivery_task and task_id not in ancestors:
                    continue
                selection = _selection(root, stage["selection"])
                link = selection["asset"].get("production")
                _require(
                    link is not None
                    and link["task"] == selected_task
                    and link["output"] == selected_output
                    and (
                        folder is None
                        or graph.confined(root, link["store"]) == Path(folder).resolve()
                    ),
                    "downstream PLAR link is missing or changed; reconcile the retained plan",
                )
        except (PixlError, OSError, ValueError, KeyError, TypeError) as error:
            reasons.append(f"production_plan: {task_id}: {error}")
    return reasons


def _replacement(doc, selection, selected, folder, root, target):
    """Explicit linked-generation CAS; never abandon or bypass a pending intent."""
    from .plar_workflow import owned_tasks

    old = selected["asset"].get("production")
    replacement = selection.get("replaces")
    if old is None:
        _require(replacement is None, "replacement link is no longer present; compare current allocation")
        return
    _require(replacement == old, "asset already has production; explicitly name its exact current production in selection.replaces")
    _require(graph.confined(root, old["store"]) == folder, "replacement belongs to another store")
    owned = owned_tasks(doc, root, selection["path"], selection["asset"])
    _require(old["task"] in owned, "replacement task does not own this PLAR selection")
    output = _record(doc, old["output"], "F")
    _require(output.fields["tk"].id == old["task"], "replacement output belongs to another task")
    for task in owned:
        if task != target:
            jobs._pending(doc, task, [r.id for r in doc.records[task].fields["op"]])


def _links(plan, folder, root, snapshot):
    # Recheck pending work under the same store lock used by job preparation.
    # PLAR keeps its own expected-hash publication and history snapshots.
    with store.lock(folder):
        return _publish_links(plan, folder, root, snapshot)


def _publish_links(plan, folder, root, snapshot):
    """Recoverable CAS links; no job or acceptance is implied by planning."""
    result = []
    for stage in plan["stages"]:
        if "selection" not in stage:
            continue
        selected = _selection(root, stage["selection"])
        task, output = _ids(plan, stage["id"])
        link = {
            "store": folder.relative_to(root).as_posix(),
            "task": task,
            "output": output,
        }
        old = selected["asset"].get("production")
        if old == link:
            result.append(
                {
                    "asset": stage["selection"]["asset"],
                    "status": "unchanged",
                    "production": link,
                }
            )
            continue
        _replacement(store.load(folder), stage["selection"], selected, folder, root, task)
        document, digest = plar._load(graph.confined(root, stage["selection"]["path"]))
        _require(
            digest == selected["hash"],
            "PLAR changed during linking; repeat the same plan",
        )
        asset = next(
            a for a in document["assets"] if a["id"] == stage["selection"]["asset"]
        )
        asset["production"] = link
        asset["status"] = "in_progress"
        asset["next"] = (
            "Read production prerequisites; select retained bytes for fresh review or prepare the selected stage when new provider work is needed."
        )
        asset["evidence"].append(
            {
                "path": snapshot,
                "note": "Retained successor stage plan; original production preserved, no provider execution or acceptance."
                if old else "Retained stage plan; no provider execution or acceptance.",
            }
        )
        plar.save(root, document, digest, stage["selection"]["path"])
        result.append({"asset": asset["id"], "status": "revised" if old else "linked", "production": link,
                       **({"previous_production": old} if old else {})})
    return result


def author(folder, expected, plan, root=None):
    """Append a graph from a compact plan; identical calls recover allocation links."""
    from .production_review import handoff

    _validate(plan, SCHEMA)
    folder, root, current = jobs._load(folder, expected, root)
    marker_id = plan["id"] + ".plan"
    existing = current.records.get(marker_id)
    if existing:
        _require(
            existing.kind == "X",
            "plan ID already belongs to another artifact",
        )
        retained = _snapshot(root, existing)
        _require(
            retained["plan"] == plan,
            "plan ID already exists with different content; append a new plan ID",
        )
        _current_plan(current, existing)
        snapshot = existing.fields["ur"]
        result = {
            "hash": expected,
            "revision": current.revision,
            "already_authored": True,
        }
    else:
        doc = copy.deepcopy(current)
        stages = plan["stages"]
        _require(len({s["id"] for s in stages}) == len(stages), "duplicate stage ID")
        _require("delivery" not in {s["id"] for s in stages}, "delivery is reserved")
        _record(doc, plan["project"], "P")
        _record(doc, plan["actor"], "A")
        baseline = _record(doc, plan["baseline"], "X")
        _require("of" in baseline.fields, "baseline must be a materialized sample")
        baseline_task = _record(doc, baseline.fields["of"].id, "F").fields["tk"].id
        selected_assets = set()
        selections = {}
        for stage in stages:
            if "selection" in stage:
                selection = stage["selection"]
                key = (selection["path"], selection["asset"])
                _require(
                    key not in selected_assets,
                    "bind each PLAR asset to one final stage",
                )
                selected_assets.add(key)
                selected = _selection(root, selection)
                _replacement(current, selection, selected, folder, root, _ids(plan, stage["id"])[0])
                selections[stage["id"]] = {
                    "project": selected["project"],
                    "asset": plar._requirements(selected["asset"]),
                    "dependencies": [
                        plar._requirements(row) for row in selected["dependencies"]
                    ],
                    "sources": [
                        {k: v for k, v in row.items() if k != "absolute_path"}
                        for row in selected["sources"]
                    ],
                }
        body = (
            platform._json_bytes({"version": 1, "plan": plan, "selections": selections})
            + b"\n"
        )
        snapshot, digest = jobs._blob(folder, root, "production-plans", body, ".json")

        def add(record):
            _require(
                record.id not in doc.records, f"record already exists: {record.id}"
            )
            doc.records[record.id] = record

        add(
            Record(
                marker_id,
                "X",
                {
                    "nm": "Production stages and family plan",
                    "ur": snapshot,
                    "dg": digest,
                    "kd": Symbol("report"),
                    "mt": {"binding": "pixl.production.plan/1"},
                },
            )
        )

        def criteria(prefix, rows):
            refs = []
            for row in rows:
                ident = prefix + ".q." + row["id"]
                add(
                    Record(
                        ident,
                        "Q",
                        {
                            "nm": row["id"],
                            "ck": row["check"],
                            "dm": Symbol(row["domain"]),
                            "md": Symbol(row["mode"]),
                            "wh": Ref(plan["actor"]),
                            "so": [Ref(s) for s in row["sources"]],
                        },
                    )
                )
                refs.append(Ref(ident))
            return refs

        for stage in stages:
            task_id, output_id = _ids(plan, stage["id"])
            inputs = [Ref(marker_id), Ref(plan["baseline"])]
            if "selection" in stage:
                selection = stage["selection"]
                selection_id = plan["id"] + "." + stage["id"] + ".selection"
                add(
                    Record(
                        selection_id,
                        "X",
                        {
                            "nm": "Current PLAR selection",
                            "ur": snapshot,
                            "dg": digest,
                            "kd": Symbol("report"),
                            "mt": {
                                "binding": "pixl.plar.selection/1",
                                "plar_path": selection["path"],
                                "asset_id": selection["asset"],
                                "requirements_hash": selection["requirements_hash"],
                            },
                        },
                    )
                )
                inputs.append(Ref(selection_id))
            add(
                Record(
                    task_id,
                    "T",
                    {
                        "nm": stage["name"],
                        "ow": Ref(plan["actor"]),
                        "pr": Ref(plan["project"]),
                        "dp": [Ref(baseline_task)],
                        "dc": [Ref(x) for x in plan["decisions"]],
                        "kn": [Ref(x) for x in plan["knowledge"]],
                        "st": Symbol("open"),
                        "ph": Symbol(stage["phase"]),
                        "ip": inputs,
                        "op": [Ref(output_id)],
                        "ca": [],
                        "vr": [],
                    },
                )
            )
            fields = {
                "tk": Ref(task_id),
                "nm": stage["name"],
                "kd": Symbol(stage["kind"]),
                "ct": Ref(stage["contract"]),
                "rq": criteria(plan["id"] + "." + stage["id"], stage["criteria"]),
            }
            if stage["phase"] == "production":
                fields["bs"] = Ref(plan["baseline"])
            add(Record(output_id, "F", fields))
        for stage in stages:
            task = doc.records[_ids(plan, stage["id"])[0]]
            for need in stage["needs"]:
                producer = _record(doc, _output(plan, need), "F").fields["tk"]
                _require(
                    doc.records[producer.id].fields["pr"].id == plan["project"],
                    "stage input belongs to another project",
                )
                if producer not in task.fields["dp"]:
                    task.fields["dp"].append(producer)
        task_id, output_id = _ids(plan, "delivery")
        delivery = plan["delivery"]
        members = [Ref(_output(plan, member)) for member in delivery["members"]]
        dependencies = list(
            dict.fromkeys(
                [baseline_task]
                + [_record(doc, m.id, "F").fields["tk"].id for m in members]
            )
        )
        add(
            Record(
                task_id,
                "T",
                {
                    "nm": delivery["name"],
                    "ow": Ref(plan["actor"]),
                    "pr": Ref(plan["project"]),
                    "dp": [Ref(x) for x in dependencies],
                    "dc": [Ref(x) for x in plan["decisions"]],
                    "kn": [Ref(x) for x in plan["knowledge"]],
                    "st": Symbol("open"),
                    "ph": Symbol("delivery"),
                    "ip": [Ref(marker_id), Ref(plan["baseline"])],
                    "op": [Ref(output_id)],
                    "ca": [],
                    "vr": [],
                },
            )
        )
        add(
            Record(
                output_id,
                "F",
                {
                    "tk": Ref(task_id),
                    "nm": delivery["name"],
                    "kd": Symbol("report"),
                    "bs": Ref(plan["baseline"]),
                    "mb": members,
                    "ds": [Ref(x) for x in delivery["destinations"]],
                    "rq": criteria(plan["id"] + ".delivery", delivery["criteria"]),
                },
            )
        )
        new_tasks = [_ids(plan, s["id"])[0] for s in stages] + [task_id]
        outputs = [_ids(plan, s["id"])[1] for s in stages] + [output_id]
        metadata = doc.records[marker_id].fields["mt"]
        metadata["scope"] = {
            ident: codec.record_hash(doc.records[ident])
            for ident in sorted(
                graph.proof_scope(doc, outputs + plan["decisions"] + plan["knowledge"])
            )
        }
        metadata["tasks"] = {
            ident: {
                "sha256": _task_hash(doc.records[ident]),
                "inputs": [r.id for r in doc.records[ident].fields["ip"]],
            }
            for ident in new_tasks
        }
        doc.revision += 1
        result = {
            **store.commit(folder, doc, expected, root),
            "already_authored": False,
        }
    try:
        allocation = _links(plan, folder, root, snapshot)
    except (PixlError, OSError) as error:
        allocation = [
            {
                "status": "needs_reconciliation",
                "reason": str(error),
                "next": "Plan retained; reread state and repeat the same plan to recover its links.",
            }
        ]
    return {
        **result,
        "plan": marker_id,
        "snapshot": snapshot,
        "stages": {
            s["id"]: dict(zip(("task", "output"), _ids(plan, s["id"])))
            for s in plan["stages"]
        },
        "delivery": dict(zip(("task", "output"), _ids(plan, "delivery"))),
        "allocation": allocation,
        "request_review": handoff(folder, root, marker_id),
        "remote_executed": False,
        "accepted": False,
    }


def prepare(folder, expected, plan_id, stage_id, job_id, packet, root=None):
    """Bind exact reviewed upstream candidates and prepare one existing durable job."""
    from .production_review import handoff

    _validate(packet, REQUEST_SCHEMA)
    folder, root, doc = jobs._load(folder, expected, root)
    marker = _record(doc, plan_id, "X")
    plan = _snapshot(root, marker)["plan"]
    _current_plan(doc, marker)
    stages = [s for s in plan["stages"] if s["id"] == stage_id]
    _require(len(stages) == 1, "unknown stage")
    stage = stages[0]
    task_id, output_id = _ids(plan, stage_id)
    needs = {_output(plan, n) for n in stage["needs"]}
    _require(
        set(packet["inputs"]) == needs,
        "inputs must name exactly the stage's prerequisite outputs",
    )
    request = packet["request"]
    _require(
        set(request)
        == {"provider", "tool", "arguments", "schema", "discovery", "authorization"},
        "request needs the exact discovered provider request fields",
    )
    normalized = platform.prepare_discovered(**request)
    task = doc.records[task_id]
    # Every declared input is the exact accepted nominee the caller reviewed.
    inputs = []
    for output, choice in packet["inputs"].items():
        producer = doc.records[_record(doc, output, "F").fields["tk"].id]
        candidate = _record(doc, choice["candidate"], "X")
        _require(
            producer.fields["st"] == Symbol("done")
            and Ref(candidate.id) in producer.fields["ca"],
            "upstream input is not the accepted nominee of a done task",
        )
        _require(
            candidate.fields.get("of") == Ref(output)
            and candidate.fields["dg"] == choice["sha256"],
            "upstream input identity differs from reviewed bytes",
        )
        inputs.append(Ref(candidate.id))
    if job_id in doc.records:
        prior = jobs._get(doc, job_id, root)
        normalized["prepared_at"] = prior["intent"]["request"]["prepared_at"]
        _require(
            prior["intent"]["request"] == normalized, "job ID has a different request"
        )
        _require(
            prior["intent"]["context"] == jobs._context(doc, task_id, [output_id]),
            "saved stage request context changed",
        )
        _require(
            all(i in task.fields["ip"] for i in inputs),
            "saved request has different inputs",
        )
        packet_digest = platform._sha(packet)
        _require(
            any(
                doc.records[i.id].fields.get("mt", {}).get("stage_packet_sha256")
                == packet_digest
                for i in task.fields["ip"]
            ),
            "saved request has a different reviewed packet",
        )
        return {
            "hash": expected,
            "revision": doc.revision,
            "already_prepared": True,
            "job": jobs._summary(doc, doc.records[job_id], prior, root, folder),
            "request_review": handoff(folder, root, plan_id, job_id),
            "remote_executed": False,
        }
    reasons = jobs._blockers(doc, task_id, root, folder=folder)
    _require(not reasons, "; ".join(reasons))
    jobs._pending(doc, task_id, [output_id], root=root)
    packet_path, digest = jobs._blob(
        folder, root, "stage-requests", platform._json_bytes(packet) + b"\n", ".json"
    )
    packet_id = "stage.request." + digest[:48]
    existing = doc.records.get(packet_id)
    if existing:
        _require(existing.fields.get("dg") == digest, "request identity collision")
    else:
        doc.records[packet_id] = Record(
            packet_id,
            "X",
            {
                "nm": "Reviewed stage inputs and executable request",
                "ur": packet_path,
                "dg": digest,
                "kd": Symbol("report"),
                "mt": {"stage_packet_sha256": platform._sha(packet)},
            },
        )
    changed = False
    for reference in inputs + [Ref(packet_id)]:
        if reference not in task.fields["ip"]:
            task.fields["ip"].append(reference)
            changed = True
    if changed:
        doc.revision += 1
        store.commit(folder, doc, expected, root)
        expected = codec.digest(doc)
    result = jobs.prepare(
        folder, expected, job_id, task_id, [output_id], root=root, **request
    )
    return {
        **result, "already_prepared": False, "remote_executed": False,
        "request_review": handoff(folder, root, plan_id, job_id),
    }
