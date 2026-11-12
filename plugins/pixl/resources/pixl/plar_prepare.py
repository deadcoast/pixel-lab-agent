"""Prepare a selected PLAR candidate from reviewed artifacts, without provider I/O.

This adapter authors the existing sample-plan records and first durable intent.
It does not invent requirements, choose provider controls or publish acceptance.
"""

import copy
import json
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

from jsonschema import Draft202012Validator

from . import (
    codec,
    graph,
    jobs,
    lifecycle,
    plar,
    plar_workflow,
    platform,
    preparation_focus,
    store,
)
from .codec import PixlError, Record, Ref, Symbol

SCHEMA = json.loads(
    Path(__file__).with_name("asset-plan.schema.json").read_text("utf-8")
)


def _require(condition, detail):
    if not condition:
        raise PixlError("asset_prepare", detail)


def _json_file(root, path, expected=None):
    from .service import parse_json

    resolved = graph.confined(root, path)
    _require(resolved.is_file(), f"missing artifact: {path}")
    _require(
        resolved.stat().st_size <= plar.MAX_BYTES, f"artifact exceeds 4 MiB: {path}"
    )
    data = resolved.read_bytes()
    digest = sha256(data).hexdigest()
    _require(expected is None or digest == expected, f"changed artifact: {path}")
    try:
        value = parse_json(data.decode("utf-8-sig"))
    except UnicodeError as error:
        raise PixlError("asset_prepare", f"expected UTF-8 JSON: {path}") from error
    _require(isinstance(value, dict), f"expected an object: {path}")
    return value, digest, resolved.relative_to(root).as_posix()


def _artifact(root, value):
    _require(
        isinstance(value, dict) and {"path", "sha256"} <= value.keys(),
        "artifact needs path and sha256",
    )
    return _json_file(root, value["path"], value["sha256"])


def _inputs(root, path, asset_id, requirements_hash, packet_path, connection):
    selected = plar.read(root, path, asset_id)
    _require(
        selected["requirements_hash"] == requirements_hash,
        "selected requirements changed; reread PLAR and compare the contract",
    )
    _require(
        all(s["binding"] == "current" for s in selected["sources"]),
        "selected or dependent sources are changed, missing or unbound",
    )
    packet, packet_hash, packet_path = _json_file(root, packet_path)
    _require(
        type(packet.get("version")) is int
        and packet["version"] == 1
        and packet.get("requirements_hash") == requirements_hash,
        "packet must identify version 1 and the selected requirements_hash",
    )
    _require(isinstance(packet.get("sources"), list), "packet sources must be a list")
    sources = {}
    for source in packet["sources"]:
        _require(
            isinstance(source, dict) and {"path", "sha256", "role"} <= source.keys(),
            "each packet source needs path, sha256 and role",
        )
        local = graph.confined(root, source["path"])
        _require(
            local.is_file() and graph.file_hash(local) == source["sha256"],
            f"changed packet source: {source['path']}",
        )
        sources[local.relative_to(root).as_posix()] = source["sha256"]
    for source in selected["sources"]:
        local = graph.confined(root, source["path"]).relative_to(root).as_posix()
        _require(
            sources.get(local) == source["sha256"],
            f"packet omits the selected source identity: {source['path']}",
        )
    request_pointer = packet.get("request")
    _require(
        isinstance(request_pointer, dict)
        and request_pointer.get("kind") == "provider_arguments",
        "a creative brief is not an executable provider request",
    )
    arguments, arguments_hash, arguments_path = _artifact(root, request_pointer)
    plan, plan_hash, plan_path = _artifact(root, packet.get("criteria"))
    error = next(Draft202012Validator(SCHEMA).iter_errors(plan), None)
    _require(error is None, f"candidate plan: {error.message if error else ''}")
    output_ids = [o["id"] for o in plan["outputs"]]
    _require(len(set(output_ids)) == len(output_ids), "output IDs must be distinct")
    for output in plan["outputs"]:
        criterion_ids = [c["id"] for c in output["criteria"]]
        _require(
            len(set(criterion_ids)) == len(criterion_ids),
            "criterion IDs must be distinct within each output",
        )
        for criterion in output["criteria"]:
            for source in criterion["sources"]:
                local = (
                    graph.confined(root, source["path"]).relative_to(root).as_posix()
                )
                _require(
                    local in sources,
                    f"criterion source is absent from packet: {source['path']}",
                )
                if "lines" in source:
                    from .request_review import source_evidence

                    resolved = source_evidence(root, source, sources[local])
                    _require(resolved["status"] == "resolved", f"criterion source lines: {source['path']}: {resolved['status']}")

    _require(
        isinstance(connection, dict)
        and set(connection) == {"provider", "schema", "discovery", "authorization"},
        "connection needs provider, schema, discovery and authorization",
    )
    if "provider" in request_pointer:
        _require(request_pointer["provider"] == connection["provider"], "reviewed provider differs from the supplied connection")
    if "connection" in request_pointer:
        reviewed_connection, reviewed_hash, reviewed_path = _artifact(root, request_pointer["connection"])
        _require(reviewed_connection == connection, "supplied connection differs from the exact reviewed connection")
        sources[reviewed_path] = reviewed_hash
    request = {
        **connection,
        "tool": request_pointer.get("tool"),
        "arguments": arguments,
    }
    # Validate schema, authorization assertions and current observation time before writes.
    platform.prepare_discovered(**request)
    sources.update(
        {packet_path: packet_hash, arguments_path: arguments_hash, plan_path: plan_hash}
    )
    selection = {
        "project": selected["project"],
        "asset": plar._requirements(selected["asset"]),
        "dependencies": [
            plar._requirements({k: v for k, v in row.items() if k != "issues"})
            for row in selected["dependencies"]
        ],
        "sources": [
            {k: v for k, v in s.items() if k != "absolute_path"}
            for s in selected["sources"]
        ],
    }
    identity = {
        "version": 1,
        "plar_path": path,
        "asset_id": asset_id,
        "requirements_hash": requirements_hash,
        "packet": {"path": packet_path, "sha256": packet_hash},
        "request": request,
        "selection": selection,
    }
    return selected, plan, sources, identity


def _document(root, selected, plan, marker_path, marker, marker_hash, captured=None):
    records = [Record("actor", "A", {"nm": "PIXL", "rl": Symbol("agent")})]
    source_ids = {}
    retained = {row["path"]: row["sha256"] for row in marker["sources"].values()}
    for index, (path, digest) in enumerate(
        sorted({**retained, marker_path: marker_hash}.items())
    ):
        id_ = f"source.{index}"
        source_ids[path] = id_
        if path == marker_path:
            data = platform._json_bytes(marker) + b"\n"
        elif captured is not None:
            data = captured[path]
        else:
            data = graph.confined(root, path).read_bytes()
        try:
            count = len(data.decode("utf-8-sig").splitlines())
            lines = [1, count] if count else []
        except UnicodeError:
            lines = []
        records.append(
            Record(
                id_,
                "S",
                {
                    "ur": path,
                    "dg": digest,
                    "ln": lines,
                    "at": marker["created_at"],
                    "au": Symbol("local"),
                },
            )
        )
    source_refs = [Ref(id_) for id_ in source_ids.values()]
    binding = {
        "binding": "pixl.plar.selection/1",
        **{
            key: marker["input"][key]
            for key in ("plar_path", "asset_id", "requirements_hash")
        },
    }
    records.append(
        Record(
            "selection",
            "X",
            {
                "nm": "Retained PLAR selection and reviewed request",
                "ur": marker_path,
                "dg": marker_hash,
                "kd": Symbol("report"),
                "mt": binding,
            },
        )
    )
    inputs = [Ref("selection")]
    # Reference inputs retain actual bytes and declared roles, without pretending
    # they are a generated candidate or an adopted family baseline.
    for index, reference in enumerate(selected["visual_references"]):
        id_ = f"reference.{index}"
        path = graph.confined(root, reference["path"]).relative_to(root).as_posix()
        records.append(
            Record(
                id_,
                "X",
                {
                    "nm": reference["instructions"],
                    "ur": marker["sources"][path]["path"],
                    "dg": reference["sha256"],
                    "kd": Symbol("reference"),
                    "mt": {"role": reference["role"]},
                },
            )
        )
        inputs.append(Ref(id_))
    choices, outputs = [], []
    for output in plan["outputs"]:
        name = output["id"]
        choice_id, contract_id, output_id = (
            f"choice.{name}",
            f"contract.{name}",
            f"output.{name}",
        )
        contract = output["contract"]
        choices.append(Ref(choice_id))
        records.append(
            Record(
                choice_id,
                "I",
                {
                    "pr": Ref("project"),
                    "wh": Ref("actor"),
                    "ky": f"candidate.{name}",
                    "st": Symbol("proposed"),
                    "vl": contract,
                    "so": source_refs,
                    "wy": "Concrete candidate interpretation for the reviewed scope; source requirements retain their original authority in the selected PLAR and packet.",
                },
            )
        )
        records.append(
            Record(
                contract_id,
                "C",
                {
                    "nm": output["name"],
                    "px": contract["size"],
                    "pl": contract["palette"],
                    "vw": Symbol(contract["view"]),
                    "sa": Symbol(contract["sampling"]),
                    "al": Symbol(contract["alpha"]),
                    "li": contract["intent"],
                    "ch": [Ref(choice_id)],
                },
            )
        )
        criteria = []
        for criterion in output["criteria"]:
            id_ = f"criterion.{name}.{criterion['id']}"
            criteria.append(Ref(id_))
            records.append(
                Record(
                    id_,
                    "Q",
                    {
                        "nm": criterion["id"],
                        "ck": criterion["check"],
                        "dm": Symbol(criterion["domain"]),
                        "md": Symbol(criterion["mode"]),
                        "wh": Ref("actor"),
                        "so": source_refs,
                    },
                )
            )
        records.append(
            Record(
                output_id,
                "F",
                {
                    "tk": Ref("task"),
                    "nm": output["name"],
                    "kd": Symbol(output["kind"]),
                    "ct": Ref(contract_id),
                    "rq": criteria,
                },
            )
        )
        outputs.append(Ref(output_id))
    records.extend(
        [
            Record(
                "project",
                "P",
                {
                    "nm": selected["project"]["name"],
                    "ow": Ref("actor"),
                    "sc": source_refs,
                    "in": choices,
                    "br": selected["asset"]["purpose"] + "\n" + plan["scope"],
                },
            ),
            Record(
                "task",
                "T",
                {
                    "nm": plan["scope"],
                    "ow": Ref("actor"),
                    "pr": Ref("project"),
                    "dp": [],
                    "dc": [],
                    "kn": [],
                    "st": Symbol("open"),
                    "ph": Symbol("sample"),
                    "ip": inputs,
                    "op": outputs,
                    "ca": [],
                    "vr": [],
                },
            ),
        ]
    )
    document = codec.Document(0, {r.id: r for r in records}, format=2)
    prefix = marker.get("prefix", "")
    if prefix:
        names = {}
        for record in records:
            name = prefix + record.id
            if len(name) > 96:
                name = (
                    prefix
                    + record.id[:55]
                    + "."
                    + sha256(record.id.encode()).hexdigest()[:12]
                )
            names[record.id] = record.id if record.id in {"actor", "project"} else name

        def remap(value):
            if isinstance(value, Ref):
                return Ref(names.get(value.id, value.id))
            if isinstance(value, list):
                return [remap(item) for item in value]
            if isinstance(value, dict):
                return {key: remap(item) for key, item in value.items()}
            return value

        document.records = {
            names[r.id]: Record(names[r.id], r.kind, remap(r.fields)) for r in records
        }
    if prefix:
        for record in document.records.values():
            if record.kind == "I":
                record.fields["ky"] = prefix + record.fields["ky"]
    return document


def _canonical_identity(identity):
    """Source table order is presentation, just as in PLAR requirements identity."""
    result = copy.deepcopy(identity)
    selection = result.get("selection")
    if isinstance(selection, dict) and isinstance(selection.get("sources"), list):
        selection["sources"] = sorted(selection["sources"], key=platform._json_bytes)
    return result


def _retained_identity(current, root, folder, identity, linked):
    """Reuse a bound older snapshot without renaming or rewriting its identity."""
    canonical = _canonical_identity(identity)
    if current is None:
        return canonical
    owned = plar_workflow.owned_tasks(
        current, root, identity["plar_path"], identity["asset_id"]
    )
    owned.sort(key=lambda task: (not linked or task != linked["task"], task))
    seen = set()
    for task_id in owned:
        for reference in current.records[task_id].fields["ip"]:
            record = current.records[reference.id]
            if (
                reference.id in seen
                or record.fields.get("mt", {}).get("binding") != "pixl.plar.selection/1"
            ):
                continue
            seen.add(reference.id)
            location = graph.confined(root, record.fields["ur"])
            if (
                location.parent != folder / "plans"
                or location.suffix != ".json"
                or len(location.stem) != 64
                or any(c not in "0123456789abcdef" for c in location.stem)
            ):
                # Explicit selection metadata also supports ordinary report inputs.
                continue
            marker, _, relative = _json_file(
                root, record.fields["ur"], record.fields["dg"]
            )
            previous = marker.get("input")
            if (
                not isinstance(previous, dict)
                or _canonical_identity(previous) != canonical
            ):
                continue
            fingerprint = platform._sha(previous)
            _require(
                marker.get("input_sha256") == fingerprint
                and graph.confined(root, relative)
                == graph.confined(folder, "plans/" + fingerprint + ".json"),
                "retained preparation snapshot identity differs from its binding",
            )
            return previous
    return canonical


def prepare(
    root,
    asset_id,
    requirements_hash,
    packet,
    connection,
    path="plar.txt",
    folder=None,
    revise=False,
    expected=None,
):
    """Publish the exact candidate plan and prepare its first job; never dispatch."""
    root = Path(root).resolve()
    if isinstance(connection, str):
        connection, _, _ = _json_file(root, connection)
    selected, plan, sources, identity = _inputs(
        root, path, asset_id, requirements_hash, packet, connection
    )
    linked = selected["asset"].get("production")
    folder = graph.confined(
        root, folder or (linked["store"] if linked else f".pixl/assets/{asset_id}")
    )
    _require(folder != root, "use a consumer subdirectory for the asset store")
    if linked:
        _require(
            graph.confined(root, linked["store"]) == folder,
            "this asset already links another plan; resume that work",
        )
    current = store.load(folder) if (folder / "state.px").exists() else None
    if current is not None:
        graph.validate(current, root)
        if expected is not None and codec.digest(current) != expected:
            raise PixlError(
                "stale_write", "reread the production state before revising"
            )
    elif revise:
        _require(
            False,
            "revision requires existing production; omit revise for the first request",
        )
    identity = _retained_identity(current, root, folder, identity, linked)
    fingerprint = platform._sha(identity)
    marker_file = graph.confined(folder, "plans/" + fingerprint + ".json")
    with store.lock(folder):
        if current is not None and codec.digest(store.load(folder)) != codec.digest(
            current
        ):
            raise PixlError(
                "stale_write", "production changed before retaining the revised plan"
            )
        retained_marker = marker_file.exists()
        if retained_marker:
            marker, marker_hash, marker_path = _json_file(
                root, marker_file.relative_to(root).as_posix()
            )
            _require(
                marker.get("input_sha256") == fingerprint
                and marker.get("input") == identity,
                "asset preparation already exists with a different contract; preserve and revise the existing plan",
            )
            if len(plan["outputs"]) > 1 or (not linked and graph.confined(folder, preparation_focus.NAME).exists()):
                focus_task = marker.get("prefix", "") + "task"
                preparation_focus.check_switch(
                    current, root, folder, path, asset_id, focus_task, marker=marker,
                    revise=revise, expected=expected,
                    new_task=current is None or focus_task not in current.records,
                    retained_marker=True,
                )
        else:
            prefix = ""
            if current is not None:
                _require(
                    revise and expected is not None,
                    "existing state was not created by this preparation; review a revision and supply revise plus expect",
                )
                owned = plar_workflow.owned_tasks(current, root, path, asset_id)
                _require(
                    owned and (not linked or linked["task"] in owned),
                    "existing state has no matching asset selection; resume its explicit plan",
                )
                for task_id in owned:
                    jobs._pending(
                        current,
                        task_id,
                        [r.id for r in current.records[task_id].fields["op"]],
                    )
                prefix = "r." + fingerprint[:16] + "."
            captured, retained_sources = {}, {}
            for original, source_digest in sources.items():
                local = graph.confined(root, original)
                _require(
                    local.stat().st_size <= 64 * 1024 * 1024, "source exceeds 64 MiB"
                )
                source_data = local.read_bytes()
                _require(
                    sha256(source_data).hexdigest() == source_digest,
                    f"source changed while preparing: {original}",
                )
                suffix = local.suffix.lower()
                if len(suffix) > 16 or any(
                    not (c.isalnum() or c == ".") for c in suffix
                ):
                    suffix = ".bin"
                retained_path = (
                    folder.relative_to(root) / "inputs" / (source_digest + suffix)
                ).as_posix()
                captured[retained_path] = source_data
                retained_sources[original] = {
                    "path": retained_path,
                    "sha256": source_digest,
                }
            marker = {
                "version": 1,
                "input_sha256": fingerprint,
                "input": identity,
                "sources": retained_sources,
                "created_at": datetime.now(UTC).isoformat(),
                **({"prefix": prefix} if prefix else {}),
            }
            if len(plan["outputs"]) > 1:
                focus = preparation_focus.check_switch(
                    current, root, folder, path, asset_id, prefix + "task",
                    revise=revise, expected=expected, new_task=True,
                )
                marker["preparation_focus"] = {
                    "version": 1,
                    "previous_sha256": focus["sha256"] if focus else None,
                }
            data = platform._json_bytes(marker) + b"\n"
            marker_hash = sha256(data).hexdigest()
            marker_path = marker_file.relative_to(root).as_posix()
            preview = _document(
                root, selected, plan, marker_path, marker, marker_hash, captured
            )
            graph.validate(preview)
            _require(
                not lifecycle.blockers(preview, prefix + "task"),
                "candidate plan has unresolved activation prerequisites",
            )
            for relative, source_data in captured.items():
                destination = graph.confined(root, relative)
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists():
                    _require(
                        destination.read_bytes() == source_data,
                        "retained input bytes changed",
                    )
                else:
                    store._atomic(destination, source_data)
            marker_file.parent.mkdir(parents=True, exist_ok=True)
            store._atomic(marker_file, data)
    _require(
        marker.get("version") == 1 and isinstance(marker.get("sources"), dict),
        "unsupported preparation snapshot; inspect its retained version",
    )
    document = _document(root, selected, plan, marker_path, marker, marker_hash)
    task_id = marker.get("prefix", "") + "task"
    new_task = current is None or task_id not in current.records
    output_ids = [r.id for r in document.records[task_id].fields["op"]]
    job_id = (
        marker.get("prefix", "") + "request"
        if marker.get("prefix")
        else "first_request"
    )
    graph.validate(document, root)
    _require(
        not lifecycle.blockers(document, task_id),
        "candidate plan has unresolved activation prerequisites",
    )
    if current is None:
        store.initialize(folder, document, root)
    elif task_id not in current.records:
        _require(
            revise and expected is not None,
            "new plan generation requires explicit revise and expect",
        )
        # Preserve every original task, contract, candidate, verdict and job.
        candidate = copy.deepcopy(current)
        for id_, record in document.records.items():
            if id_ == "project":
                project = candidate.records[id_].fields
                for key in ("sc", "in"):
                    project[key].extend(
                        r for r in record.fields[key] if r not in project[key]
                    )
                project["br"] = record.fields["br"]
            elif id_ in candidate.records:
                _require(
                    candidate.records[id_] == record,
                    "revision record collides with existing work",
                )
            else:
                candidate.records[id_] = record
        candidate.revision += 1
        store.commit(folder, candidate, expected, root)
    elif (
        linked
        and linked["task"] != task_id
        and not (
            revise
            and expected is not None
            and (
                job_id not in current.records
                or current.records[job_id].fields["si"].value == "prepared"
            )
        )
    ):
        _require(
            False,
            "this is an earlier retained plan; resume the currently linked production instead",
        )
    current = store.load(folder)
    graph.validate(current, root)
    for id_, record in document.records.items():
        actual = current.records.get(id_)
        _require(
            actual is not None and actual.kind == record.kind,
            "prepared plan records changed; inspect the current workflow",
        )
        expected_fields, actual_fields = record.fields, actual.fields
        if id_ == "project":
            _require(
                all(
                    set(record.fields[k]) <= set(actual.fields[k]) for k in ("sc", "in")
                ),
                "prepared source/choice references changed; inspect the current project",
            )
            continue
        if id_ == task_id:
            expected_fields = {
                k: v for k, v in expected_fields.items() if k not in {"st", "ca", "vr"}
            }
            actual_fields = {
                k: v for k, v in actual_fields.items() if k not in {"st", "ca", "vr"}
            }
        _require(
            actual_fields == expected_fields,
            "prepared plan changed; inspect the current workflow",
        )
    job_id = (
        marker.get("prefix", "") + "request"
        if marker.get("prefix")
        else "first_request"
    )
    reused = job_id in current.records
    if not reused:
        # The same pending-asset check applies after interrupted plan publication.
        for owned in plar_workflow.owned_tasks(current, root, path, asset_id):
            jobs._pending(
                current, owned, [r.id for r in current.records[owned].fields["op"]]
            )
        jobs.prepare(
            folder,
            codec.digest(current),
            job_id,
            task_id,
            output_ids,
            root=root,
            **identity["request"],
        )
        current = store.load(folder)
    report = jobs.report(current, root, folder)
    job = next(row for row in report["jobs"] if row["id"] == job_id)
    retained_request = job.get("request", {})
    expected_context = jobs._context(current, task_id, output_ids)
    _require(
        job.get("context") == expected_context,
        "existing first request has different task/output bindings; inspect its actual journal",
    )
    _require(
        job.get("durable")
        and platform._sha(
            {key: retained_request.get(key) for key in identity["request"]}
        )
        == platform._sha(identity["request"]),
        "existing first request differs from the reviewed intent; inspect its actual journal before continuing",
    )
    focus_result = None
    if len(output_ids) > 1:
        try:
            focus_result = preparation_focus.publish(
                current, root, folder, path, selected, task_id, marker_path, marker_hash,
                revise=revise, expected=expected, new_task=new_task, retained_marker=retained_marker,
            )
        except (PixlError, OSError) as error:
            focus_result = {
                "status": "needs_reconciliation", "reason": str(error),
                "next": "The plan and job remain retained. Reread state and retry the exact current packet with revise/expect; do not create another request.",
            }
    allocation = plar_workflow.synchronize(
        root, selected, path, folder, task_id, output_ids, marker_path
    )
    job = next(
        row for row in jobs.report(current, root, folder)["jobs"] if row["id"] == job_id
    )
    return {
        "allocation": allocation,
        **({"preparation_focus": focus_result} if focus_result is not None else {}),
        "store": folder.relative_to(root).as_posix(),
        "state": str(folder / "state.px"),
        "hash": codec.digest(current),
        "revision": current.revision,
        "asset_id": asset_id,
        "requirements_hash": requirements_hash,
        "task": task_id,
        "outputs": output_ids,
        "job": job,
        "already_prepared": reused,
        "phase": "sample",
        "request_review": {
            **identity["packet"],
            "retained_path": marker["sources"][identity["packet"]["path"]]["path"],
        },
        "retained_inputs": marker["sources"],
        "remote_executed": False,
        "acceptance_created": False,
        "next": "Use the existing job operation named by job.next_action; reread selected requirements before dispatch. Inspect actual results before acceptance.",
    }
