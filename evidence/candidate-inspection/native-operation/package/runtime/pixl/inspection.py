"""Retained candidate inspection and explicit caller-declared review; PX2 only."""

import copy
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from . import codec, delivery, graph, inspection_views, platform, store
from .codec import Document, PixlError, Record, Ref, Symbol

PACKET_KEYS = {
    "version",
    "kind",
    "packet",
    "candidate",
    "output",
    "task",
    "created_at",
    "source_state_sha256",
    "records",
    "rendering",
}
REVIEW_KEYS = {
    "version",
    "kind",
    "packet",
    "review",
    "recorded_at",
    "source_state_sha256",
    "observation",
    "coverage",
}
OBS_KEYS = {
    "reviewer",
    "observed_at",
    "observations",
    "verdicts",
    "next_action",
    "limitations",
}


def _require(ok, detail, code="inspection_manifest"):
    if not ok:
        raise PixlError(code, detail)


def _closed(value, keys):
    _require(isinstance(value, dict) and set(value) == keys, "closed object required")


def _text(value):
    _require(isinstance(value, str) and bool(value.strip()), "nonempty text required")


def _bytes(value):
    return platform._json_bytes(value) + b"\n"


def _same(left, right):
    """JSON equality must not collapse bool/int or float/int scalar types."""
    return _bytes(codec.to_data(left)) == _bytes(codec.to_data(right))


def _tagged(value):
    if isinstance(value, list):
        return [_tagged(v) for v in value]
    if isinstance(value, dict):
        if set(value) == {"$ref"}:
            return Ref(value["$ref"])
        if set(value) == {"$symbol"}:
            return Symbol(value["$symbol"])
        return {k: _tagged(v) for k, v in value.items()}
    return value


def _scope(doc, candidate, references):
    return graph.proof_scope(doc, [candidate, *references])


def _contract(doc, candidate):
    f = doc.records[doc.records[candidate].fields["ct"].id].fields
    return {"px": f["px"], "pl": f["pl"], "al": f["al"].value}


def _projection(value):
    if value["kind"] == "packet":
        rendering = value["rendering"]
        return {
            "inspection": Symbol("packet"),
            "version": 1,
            "candidate": Ref(value["candidate"]),
            "scope": [Ref(r["id"]) for r in value["records"]],
            "files": [Ref(v["id"]) for v in rendering["inputs"] + rendering["views"]],
        }
    return {
        "inspection": Symbol("review"),
        "version": 1,
        "packet": Ref(value["packet"]),
    }


def _artifact(id_, path, data, metadata, kind="report"):
    return Record(
        id_,
        "X",
        {
            "nm": "Retained inspection " + id_,
            "ur": path,
            "dg": hashlib.sha256(data).hexdigest(),
            "kd": Symbol(kind),
            "mt": metadata,
        },
    )


def _write(folder, root, id_, value, files=None):
    data = _bytes(value)
    _require(len(data) <= codec.MAX_BYTES, "manifest exceeds 16 MiB")
    directory = folder / "inspections" / hashlib.sha256(data).hexdigest()
    relative = directory.relative_to(root).as_posix()
    _require(
        graph.confined(root, relative) == directory, "redirected inspection storage"
    )
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in (files or {}).items():
        target = graph.confined(directory, name)
        _require(target == directory / name, "redirected retained file")
        target.parent.mkdir(parents=True, exist_ok=True)
        delivery._write_once(target, content)
    delivery._write_once(directory / "manifest.json", data)
    return _artifact(
        id_, relative + "/manifest.json", data, _projection(value)
    ), directory


def _read(artifact, root):
    _require(
        artifact.kind == "X" and artifact.fields.get("kd") == Symbol("report"),
        "inspection report X required",
    )
    path = graph.confined(root, artifact.fields["ur"])
    _require(
        path == Path(root).resolve() / artifact.fields["ur"]
        and path.name == "manifest.json"
        and path.parent.name == artifact.fields["dg"],
        "invalid inspection storage",
    )
    try:
        with path.open("rb") as stream:
            data = stream.read(codec.MAX_BYTES + 1)
        _require(len(data) <= codec.MAX_BYTES, "manifest exceeds limit")
        value = json.loads(data)
        _require(
            _bytes(value) == data
            and hashlib.sha256(data).hexdigest() == artifact.fields["dg"],
            "manifest bytes differ",
        )
    except (OSError, ValueError, UnicodeError, RecursionError) as error:
        raise PixlError(
            "inspection_manifest", "unreadable retained manifest"
        ) from error
    return value, path.parent


def _rendering(rendered, packet):
    value = {k: copy.deepcopy(v) for k, v in rendered.items() if k != "files"}
    for key, part in [("inputs", "input"), ("views", "view")]:
        for index, item in enumerate(value[key]):
            item["id"] = f"{packet}.{part}.{index}"
    return value


def _load(doc, root, packet):
    _require(packet in doc.records, "unknown packet")
    value, directory = _read(doc.records[packet], root)
    _closed(value, PACKET_KEYS)
    _require(
        type(value["version"]) is int
        and value["version"] == 1
        and value["kind"] == "packet"
        and value["packet"] == packet,
        "packet identity differs",
    )
    platform._iso_timestamp(value["created_at"], "created_at", "inspection_manifest")
    _require(
        isinstance(value["source_state_sha256"], str)
        and graph.SHA.fullmatch(value["source_state_sha256"]),
        "invalid source hash",
    )
    frozen = Document(format=2)
    _require(
        isinstance(value["records"], list) and bool(value["records"]),
        "missing original records",
    )
    for item in value["records"]:
        _closed(item, {"id", "kind", "fields", "sha256"})
        record = Record(item["id"], item["kind"], _tagged(item["fields"]))
        _require(
            record.id not in frozen.records
            and codec.record_hash(record) == item["sha256"]
            and _same(codec.to_data(record.fields), item["fields"]),
            "original record body/hash differs",
        )
        frozen.records[record.id] = record
    try:
        candidate = frozen.records[value["candidate"]]
        output = frozen.records[value["output"]]
        _require(
            candidate.kind == "X"
            and candidate.fields["of"] == Ref(output.id)
            and output.kind == "F"
            and output.fields["tk"] == Ref(value["task"]),
            "original ownership differs",
        )
        rendering = value["rendering"]
        _closed(
            rendering,
            {"inputs", "views", "measurements", "options", "context_observations"},
        )
        canonical = inspection_views._validate_options(
            rendering["options"], value["candidate"]
        )
        source_ids = [value["candidate"], *canonical["references"]]
        _require(
            isinstance(rendering["inputs"], list)
            and len(rendering["inputs"]) == len(source_ids),
            "retained input count differs",
        )
        _require(
            set(frozen.records) == _scope(frozen, value["candidate"], source_ids[1:]),
            "original semantic scope differs",
        )
        snapshots = {}
        total = 0
        for index, item in enumerate(rendering["inputs"]):
            _closed(item, {"source", "path", "sha256", "id"})
            _require(
                index < len(source_ids)
                and item["source"] == source_ids[index]
                and item["id"] == f"{packet}.input.{index}",
                "input identity differs",
            )
            path = graph.confined(directory, item["path"])
            _require(path == directory / item["path"], "redirected input")
            with path.open("rb") as stream:
                data = stream.read(
                    min(
                        inspection_views.MAX_SOURCE_BYTES,
                        inspection_views.MAX_TOTAL_SOURCE_BYTES - total,
                    )
                    + 1
                )
            total += len(data)
            _require(
                len(data) <= inspection_views.MAX_SOURCE_BYTES
                and total <= inspection_views.MAX_TOTAL_SOURCE_BYTES,
                "retained source byte limits exceeded",
            )
            _require(
                hashlib.sha256(data).hexdigest()
                == item["sha256"]
                == frozen.records[item["source"]].fields["dg"],
                "input hash differs",
            )
            snapshots[item["source"]] = data
        rendered = inspection_views.render(
            snapshots,
            value["candidate"],
            _contract(frozen, value["candidate"]),
            rendering["options"],
        )
        _require(
            _same(rendering, _rendering(rendered, packet)),
            "rendering manifest differs from exact inputs",
        )
        for item in rendering["inputs"] + rendering["views"]:
            id_ = item["id"]
            path = directory / item["path"]
            data = rendered["files"][item["path"]]
            _require(
                graph.confined(directory, item["path"]) == path
                and path.is_file()
                and path.stat().st_size == len(data)
                and graph.file_hash(path) == item["sha256"],
                "retained file differs",
            )
            expected = _artifact(
                id_,
                path.relative_to(Path(root).resolve()).as_posix(),
                data,
                {"inspection": Symbol("file"), "source": Ref(item["source"])},
                "reference",
            )
            _require(
                id_ in doc.records
                and codec.record_hash(doc.records[id_]) == codec.record_hash(expected),
                "retained file X projection differs",
            )
        _require(
            _same(doc.records[packet].fields["mt"], _projection(value)),
            "typed packet projection differs",
        )
    except (KeyError, TypeError, IndexError, OSError) as error:
        raise PixlError(
            "inspection_manifest", "invalid retained packet structure"
        ) from error
    return value, frozen, directory


def _drift(doc, frozen):
    return sorted(
        id_
        for id_, record in frozen.records.items()
        if id_ not in doc.records
        or codec.record_hash(doc.records[id_]) != codec.record_hash(record)
    )


def _start(folder, expected, root):
    folder, root = delivery._locations(folder, root)
    doc = store.load(folder)
    _require(codec.digest(doc) == expected, "reload current state", "stale_write")
    _require(doc.format == 2, "inspection requires PX2")
    graph.validate(doc, root)
    return folder, root, doc


def _fresh(doc, ids):
    for id_ in ids:
        codec.identifier(id_)
        _require(
            id_ not in doc.records,
            "fresh operation and generated IDs required",
            "inspection_identity",
        )


def prepare(folder, expected, candidate_id, packet_id, options, root=None):
    folder, root, doc = _start(folder, expected, root)
    _fresh(doc, [packet_id])
    _require(candidate_id in doc.records, "unknown candidate")
    candidate = doc.records[candidate_id]
    _require(
        candidate.kind == "X"
        and "of" in candidate.fields
        and "ct" in candidate.fields
        and candidate.fields["kd"].value not in ("report", "reference", "code"),
        "saved raster candidate with F owner required",
    )
    canonical = inspection_views._validate_options(options, candidate_id)
    snapshots = {}
    total = 0
    for id_ in [candidate_id, *canonical["references"]]:
        _require(
            id_ in doc.records and doc.records[id_].kind in ("S", "X"),
            "local S/X source required",
        )
        source = doc.records[id_]
        with graph.confined(root, source.fields["ur"]).open("rb") as stream:
            data = stream.read(
                min(
                    inspection_views.MAX_SOURCE_BYTES,
                    inspection_views.MAX_TOTAL_SOURCE_BYTES - total,
                )
                + 1
            )
        total += len(data)
        _require(
            len(data) <= inspection_views.MAX_SOURCE_BYTES
            and total <= inspection_views.MAX_TOTAL_SOURCE_BYTES,
            "source byte limits exceeded",
        )
        _require(
            hashlib.sha256(data).hexdigest() == source.fields["dg"],
            "source changed",
            "file_hash",
        )
        snapshots[id_] = data
    rendered = inspection_views.render(
        snapshots, candidate_id, _contract(doc, candidate_id), canonical
    )
    rendering = _rendering(rendered, packet_id)
    _fresh(doc, [i["id"] for i in rendering["inputs"] + rendering["views"]])
    output = doc.records[candidate.fields["of"].id]
    value = {
        "version": 1,
        "kind": "packet",
        "packet": packet_id,
        "candidate": candidate_id,
        "output": output.id,
        "task": output.fields["tk"].id,
        "created_at": datetime.now(UTC).isoformat(),
        "source_state_sha256": expected,
        "records": [
            {
                "id": id_,
                "kind": doc.records[id_].kind,
                "fields": codec.to_data(doc.records[id_].fields),
                "sha256": codec.record_hash(doc.records[id_]),
            }
            for id_ in sorted(_scope(doc, candidate_id, canonical["references"]))
        ],
        "rendering": rendering,
    }
    artifact, directory = _write(folder, root, packet_id, value, rendered["files"])
    updated = copy.deepcopy(doc)
    updated.revision += 1
    updated.records[packet_id] = artifact
    for item in rendering["inputs"] + rendering["views"]:
        updated.records[item["id"]] = _artifact(
            item["id"],
            (directory / item["path"]).relative_to(root).as_posix(),
            rendered["files"][item["path"]],
            {"inspection": Symbol("file"), "source": Ref(item["source"])},
            "reference",
        )
    _load(updated, root, packet_id)
    result = store.commit(folder, updated, expected, root)
    packet = _packet_report(updated, root, packet_id)
    return {
        **result,
        "packet": packet_id,
        "manifest": artifact.fields["ur"],
        "views": packet["views"],
        "measurements": packet["measurements"],
        "criteria": packet["criteria"],
        "files_verified": True,
    }


def _observation(doc, packet, frozen, value, recorded_at):
    _closed(value, OBS_KEYS)
    _require(
        isinstance(value["reviewer"], str)
        and value["reviewer"] in doc.records
        and doc.records[value["reviewer"]].kind == "A",
        "saved reviewer A required",
    )
    observed = platform._iso_timestamp(
        value["observed_at"], "observed_at", "inspection_review"
    )
    _require(
        platform._iso_timestamp(packet["created_at"], "created_at")
        <= observed
        <= platform._iso_timestamp(recorded_at, "recorded_at"),
        "observation time must follow preparation and precede recording",
    )
    _text(value["next_action"])
    _require(isinstance(value["limitations"], list), "limitations list required")
    for limitation in value["limitations"]:
        _text(limitation)
    views = {v["id"]: v for v in packet["rendering"]["views"]}
    _require(isinstance(value["observations"], list), "observations list required")
    seen = set()
    exact = set()
    resized = []
    unknown = []
    for item in value["observations"]:
        _closed(item, {"view", "delivered_size", "note"})
        id_ = item["view"]
        _require(
            isinstance(id_, str) and id_ in views and id_ not in seen,
            "unique packet view required",
        )
        seen.add(id_)
        _text(item["note"])
        size = item["delivered_size"]
        if size is None:
            unknown.append(id_)
        else:
            _require(
                isinstance(size, list)
                and len(size) == 2
                and all(type(n) is int and n > 0 for n in size),
                "positive delivered dimensions or null required",
            )
            if size == [views[id_]["width"], views[id_]["height"]]:
                exact.add(id_)
            else:
                resized.append(id_)
    coverage = {
        "complete": exact == set(views),
        "observed": sorted(seen),
        "missing": sorted(set(views) - seen),
        "resized": sorted(resized),
        "unknown_size": sorted(unknown),
    }
    _require(
        isinstance(value["verdicts"], list) and bool(value["verdicts"]),
        "nonempty verdict list required",
    )
    criteria = {r.id for r in frozen.records[packet["output"]].fields["rq"]}
    seen_q = set()
    for verdict in value["verdicts"]:
        _closed(verdict, {"criterion", "status", "reason", "supersedes"})
        id_ = verdict["criterion"]
        _require(
            isinstance(id_, str) and id_ in criteria and id_ not in seen_q,
            "unique packet criterion required",
        )
        seen_q.add(id_)
        status = verdict["status"]
        _require(status in ("pass", "fail", "unavailable"), "invalid status")
        _text(verdict["reason"])
        if verdict["supersedes"] is not None:
            codec.identifier(verdict["supersedes"])
        criterion = frozen.records[id_].fields
        external = criterion["dm"].value == "engine" or criterion["md"].value == "live"
        _require(
            status == "unavailable" if external else status in ("pass", "fail"),
            "engine/live requires unavailable; local review requires pass/fail",
        )
        if not external and (
            criterion["dm"].value in ("visual", "continuity")
            or criterion["md"].value == "visual"
        ):
            _require(
                any(views[id_]["source"] == packet["candidate"] for id_ in seen),
                "visual verdict needs observed candidate-source view",
            )
            _require(
                status != "pass" or coverage["complete"],
                "visual pass requires every native/enlarged view at prepared dimensions",
            )
    return coverage


def review(folder, expected, packet_id, review_id, observation, root=None):
    folder, root, doc = _start(folder, expected, root)
    _fresh(doc, [review_id])
    packet, frozen, _ = _load(doc, root, packet_id)
    _require(
        not _drift(doc, frozen),
        "packet bindings changed; prepare a fresh packet",
        "inspection_stale",
    )
    _require(
        doc.records[packet["task"]].fields["st"] != Symbol("done"),
        "reopen done task before review",
        "reopen_required",
    )
    now = datetime.now(UTC).isoformat()
    coverage = _observation(doc, packet, frozen, observation, now)
    ids = [f"{review_id}.verdict.{i}" for i in range(len(observation["verdicts"]))]
    evidence_ids = [
        f"{review_id}.evidence.{i}"
        for i, v in enumerate(observation["verdicts"])
        if v["status"] != "unavailable"
    ]
    _fresh(doc, [*ids, *evidence_ids])
    updated = copy.deepcopy(doc)
    updated.revision += 1
    for verdict in observation["verdicts"]:
        current = [
            r
            for r in updated.records.values()
            if r.kind == "V"
            and not r.fields.get("ob", False)
            and r.fields["xr"] == Ref(packet["candidate"])
            and r.fields["rq"] == Ref(verdict["criterion"])
        ]
        _require(
            verdict["supersedes"] == (current[0].id if current else None),
            "supersedes must name exact current verdict",
            "inspection_supersession",
        )
        if current:
            current[0].fields["ob"] = True
    value = {
        "version": 1,
        "kind": "review",
        "packet": packet_id,
        "review": review_id,
        "recorded_at": now,
        "source_state_sha256": expected,
        "observation": copy.deepcopy(observation),
        "coverage": coverage,
    }
    artifact, _ = _write(folder, root, review_id, value)
    updated.records[review_id] = artifact
    for index, verdict in enumerate(observation["verdicts"]):
        ev = []
        if verdict["status"] != "unavailable":
            eid = f"{review_id}.evidence.{index}"
            scope = graph.proof_scope(
                updated, [packet_id, review_id, verdict["criterion"]]
            )
            updated.records[eid] = Record(
                eid,
                "E",
                {
                    "nm": "Explicit inspection observation",
                    "ur": artifact.fields["ur"],
                    "dg": artifact.fields["dg"],
                    "rs": Symbol(verdict["status"]),
                    "md": frozen.records[verdict["criterion"]].fields["md"],
                    "at": observation["observed_at"],
                    "bs": [
                        {"rf": Ref(id_), "dg": codec.record_hash(updated.records[id_])}
                        for id_ in sorted(scope)
                    ],
                },
            )
            ev = [Ref(eid)]
        updated.records[ids[index]] = Record(
            ids[index],
            "V",
            {
                "tk": Ref(packet["task"]),
                "rq": Ref(verdict["criterion"]),
                "xr": Ref(packet["candidate"]),
                "st": Symbol(verdict["status"]),
                "wh": Ref(observation["reviewer"]),
                "wy": verdict["reason"],
                "at": observation["observed_at"],
                "ev": ev,
            },
        )
        updated.records[packet["task"]].fields["vr"].append(Ref(ids[index]))
    return {
        **store.commit(folder, updated, expected, root),
        "packet": packet_id,
        "review": review_id,
        "verdicts": ids,
        "coverage": coverage,
        "files_verified": True,
    }


def _reports(doc, root):
    """Discover retained reports by storage as well as their mutable generic tag."""
    for id_, record in sorted(doc.records.items()):
        if record.kind != "X":
            continue
        path = Path(record.fields["ur"])
        marked = record.fields.get("mt", {}).get("inspection") in (
            Symbol("packet"),
            Symbol("review"),
        )
        if not marked and not (
            path.name == "manifest.json" and "inspections" in path.parts
        ):
            continue
        value, _ = _read(record, root)
        _require(
            isinstance(value, dict) and value.get("kind") in ("packet", "review"),
            "invalid retained report kind",
        )
        _closed(value, PACKET_KEYS if value["kind"] == "packet" else REVIEW_KEYS)
        _require(
            _same(record.fields.get("mt"), _projection(value)),
            "typed report projection differs",
        )
        yield id_, record, value


def _packet_report(doc, root, packet_id):
    packet, frozen, directory = _load(doc, root, packet_id)
    reviews = []
    for id_, record, value in _reports(doc, root):
        if value["kind"] != "review" or value["packet"] != packet_id:
            continue
        _closed(value, REVIEW_KEYS)
        _require(
            type(value["version"]) is int
            and value["version"] == 1
            and value["kind"] == "review"
            and value["packet"] == packet_id
            and value["review"] == id_,
            "review identity differs",
        )
        _require(
            _same(record.fields["mt"], _projection(value)),
            "typed review projection differs",
        )
        _require(
            isinstance(value["source_state_sha256"], str)
            and graph.SHA.fullmatch(value["source_state_sha256"]),
            "invalid review source hash",
        )
        _require(
            _same(
                value["coverage"],
                _observation(
                    doc, packet, frozen, value["observation"], value["recorded_at"]
                ),
            ),
            "review coverage differs",
        )
        for index, item in enumerate(value["observation"]["verdicts"]):
            verdict = doc.records.get(f"{id_}.verdict.{index}")
            _require(
                verdict is not None and verdict.kind == "V",
                "retained review verdict missing",
            )
            expected = {
                "tk": Ref(packet["task"]),
                "rq": Ref(item["criterion"]),
                "xr": Ref(packet["candidate"]),
                "st": Symbol(item["status"]),
                "wh": Ref(value["observation"]["reviewer"]),
                "wy": item["reason"],
                "at": value["observation"]["observed_at"],
                "ev": []
                if item["status"] == "unavailable"
                else [Ref(f"{id_}.evidence.{index}")],
            }
            _require(
                _same({k: v for k, v in verdict.fields.items() if k != "ob"}, expected),
                "retained review verdict differs",
            )
            if item["status"] != "unavailable":
                # Reconstruct the original proof against retained semantic bodies,
                # even after ordinary amendments have superseded the receipt.
                original = copy.deepcopy(frozen)
                for retained in [
                    packet_id,
                    id_,
                    *[
                        v["id"]
                        for v in packet["rendering"]["inputs"]
                        + packet["rendering"]["views"]
                    ],
                ]:
                    original.records[retained] = doc.records[retained]
                scope = graph.proof_scope(original, [packet_id, id_, item["criterion"]])
                receipt = doc.records.get(f"{id_}.evidence.{index}")
                expected_receipt = {
                    "nm": "Explicit inspection observation",
                    "ur": record.fields["ur"],
                    "dg": record.fields["dg"],
                    "rs": Symbol(item["status"]),
                    "md": frozen.records[item["criterion"]].fields["md"],
                    "at": value["observation"]["observed_at"],
                    "bs": [
                        {
                            "rf": Ref(target),
                            "dg": codec.record_hash(original.records[target]),
                        }
                        for target in sorted(scope)
                    ],
                }
                _require(
                    receipt is not None
                    and receipt.kind == "E"
                    and _same(
                        {k: v for k, v in receipt.fields.items() if k != "ob"},
                        expected_receipt,
                    ),
                    "retained review evidence differs",
                )
        reviews.append(value)
    criteria = []
    for ref in frozen.records[packet["output"]].fields["rq"]:
        q = frozen.records[ref.id].fields
        current = [
            r
            for r in doc.records.values()
            if r.kind == "V"
            and not r.fields.get("ob", False)
            and r.fields["xr"] == Ref(packet["candidate"])
            and r.fields["rq"] == ref
        ]
        criteria.append(
            {
                "id": ref.id,
                "name": q["nm"],
                "check": q["ck"],
                "domain": q["dm"].value,
                "mode": q["md"].value,
                "status": current[0].fields["st"].value if current else "unperformed",
                "verdict": current[0].id if current else None,
            }
        )
    views = [
        {
            **v,
            "path": (directory / v["path"])
            .relative_to(Path(root).resolve())
            .as_posix(),
        }
        for v in packet["rendering"]["views"]
    ]
    return {
        k: packet[k] for k in ("packet", "candidate", "output", "task", "created_at")
    } | {
        "views": views,
        "measurements": packet["rendering"]["measurements"],
        "context_observations": packet["rendering"]["context_observations"],
        "criteria": criteria,
        "binding_drift": _drift(doc, frozen),
        "reviews": reviews,
        "files_verified": True,
        "visual_quality_verified": False,
        "engine_import_verified": False,
    }


def report(doc, root, packet_id=None):
    graph.validate(doc, root)
    try:
        ids = (
            [packet_id]
            if packet_id is not None
            else [
                id_
                for id_, _, value in _reports(doc, root)
                if value["kind"] == "packet"
            ]
        )
        return {
            "hash": codec.digest(doc),
            "packets": [_packet_report(doc, root, id_) for id_ in ids],
            "files_verified": True,
        }
    except (KeyError, TypeError, IndexError, OSError) as error:
        raise PixlError(
            "inspection_manifest", "invalid retained inspection structure"
        ) from error
