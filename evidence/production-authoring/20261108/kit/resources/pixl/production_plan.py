"""Author family/stage connections using existing PX2 records and durable jobs."""

import copy
import json

from jsonschema import Draft202012Validator

from . import codec, graph, jobs, plar, platform, store
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
    {"path": STR, "asset": STR, "requirements_hash": STR},
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
            "minItems": 1,
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


def _links(plan, folder, root, snapshot):
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
        # Replacing existing generations remains the explicit revision operation.
        _require(
            old is None,
            "asset already linked; preserve it and use explicit revision authoring",
        )
        document, digest = plar._load(graph.confined(root, stage["selection"]["path"]))
        _require(
            digest == selected["hash"],
            "PLAR changed during linking; repeat the same plan",
        )
        asset = next(
            a for a in document["assets"] if a["id"] == stage["selection"]["asset"]
        )
        asset["production"] = link
        asset["next"] = (
            "Read production prerequisites; prepare the selected stage when its inputs are accepted."
        )
        asset["evidence"].append(
            {
                "path": snapshot,
                "note": "Retained stage plan; no provider execution or acceptance.",
            }
        )
        plar.save(root, document, digest, stage["selection"]["path"])
        result.append({"asset": asset["id"], "status": "linked", "production": link})
    return result


def author(folder, expected, plan, root=None):
    """Append a graph from a compact plan; identical calls recover allocation links."""
    _validate(plan, SCHEMA)
    folder, root, current = jobs._load(folder, expected, root)
    marker_id = plan["id"] + ".plan"
    existing = current.records.get(marker_id)
    if existing:
        _require(
            existing.kind == "X"
            and existing.fields.get("mt", {}).get("binding")
            == "pixl.production.plan/1",
            "plan ID already belongs to another artifact",
        )
        retained = json.loads(
            graph.confined(root, existing.fields["ur"]).read_text(encoding="utf-8")
        )
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
                _require(
                    not selected["asset"].get("production"),
                    "asset already has production; do not replace its link",
                )
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
        "remote_executed": False,
        "accepted": False,
    }


def prepare(folder, expected, plan_id, stage_id, job_id, packet, root=None):
    """Bind exact reviewed upstream candidates and prepare one existing durable job."""
    _validate(packet, REQUEST_SCHEMA)
    folder, root, doc = jobs._load(folder, expected, root)
    marker = _record(doc, plan_id, "X")
    _require(
        marker.fields.get("mt", {}).get("binding") == "pixl.production.plan/1",
        "not a production plan",
    )
    _current_plan(doc, marker)
    plan = json.loads(
        graph.confined(root, marker.fields["ur"]).read_text(encoding="utf-8")
    )["plan"]
    _validate(plan, SCHEMA)
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
    return {**result, "already_prepared": False, "remote_executed": False}
