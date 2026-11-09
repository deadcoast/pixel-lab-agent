"""Retained local family packages, separate from acceptance or engine execution."""

import copy
import hashlib
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path

from . import codec, families, graph, platform, store
from .codec import PixlError, Record, Ref, Symbol

MAX_FILE_BYTES = 256 * 1024 * 1024
MAX_TOTAL_BYTES = 512 * 1024 * 1024
MAX_MEMBERS = 1024
LIMITS = {
    "retention_only": True,
    "remote_executed": False,
    "automatic_acceptance": False,
}
MANIFEST_KEYS = {
    "version",
    "output",
    "candidate",
    "source_state_sha256",
    "created_at",
    "plan",
    "baseline",
    "files",
    "acceptance",
    "limits",
}
PLAN_KEYS = {"output", "task", "baseline", "members", "destinations", "bindings"}
FILE_KEYS = {
    "output",
    "candidate",
    "source_path",
    "path",
    "sha256",
    "bytes",
    "record_sha256",
}


def _require(condition, code, detail):
    if not condition:
        raise PixlError(code, detail)


def _closed(value, keys, detail):
    _require(
        isinstance(value, dict) and set(value) == keys, "delivery_manifest", detail
    )


def _sha(value):
    return isinstance(value, str) and graph.SHA.fullmatch(value) is not None


def _id(value):
    return (
        isinstance(value, str)
        and codec.IDENT.fullmatch(value.encode("utf-8")) is not None
    )


def _json(value):
    return platform._json_bytes(value) + b"\n"


def _locations(folder, root):
    folder = Path(folder).resolve()
    root = Path(root).resolve() if root is not None else folder.parent
    _require(
        folder != root and folder.is_relative_to(root),
        "store_path",
        "delivery store must be a project subdirectory",
    )
    return folder, root


def _file_name(index, source):
    suffix = Path(source).suffix
    if not re.fullmatch(r"\.[A-Za-z0-9]{1,16}", suffix):
        suffix = ".bin"
    return f"files/{index:04d}{suffix}"


def _entries(doc, output_id, root, capture=False):
    plan = families.plan(doc, output_id)
    selected = families.selection(doc, output_id)
    _require(
        0 < len(selected) <= MAX_MEMBERS and all(selected),
        "delivery_members",
        "each of at most 1024 members needs a selected candidate",
    )
    entries, snapshots, total = [], {}, 0
    for index, (output, candidate) in enumerate(
        zip(plan["members"], selected, strict=True)
    ):
        record = doc.records[candidate]
        source = graph.confined(root, record.fields["ur"])
        size = source.stat().st_size
        _require(
            size <= MAX_FILE_BYTES and total + size <= MAX_TOTAL_BYTES,
            "delivery_limit",
            "maximum 256 MiB per member and 512 MiB total",
        )
        target = _file_name(index, record.fields["ur"])
        if capture:
            with source.open("rb") as stream:
                data = stream.read(min(MAX_FILE_BYTES, MAX_TOTAL_BYTES - total) + 1)
            _require(
                len(data) <= MAX_FILE_BYTES and total + len(data) <= MAX_TOTAL_BYTES,
                "delivery_limit",
                "member changed beyond package limits",
            )
            _require(
                hashlib.sha256(data).hexdigest() == record.fields["dg"],
                "file_hash",
                candidate,
            )
            size = len(data)
            snapshots[target] = data
        total += size
        entries.append(
            {
                "output": output,
                "candidate": candidate,
                "source_path": record.fields["ur"],
                "path": target,
                "sha256": record.fields["dg"],
                "bytes": size,
                "record_sha256": codec.record_hash(record),
            }
        )
    return entries, snapshots


def _manifest_value(doc, output_id, candidate_id, created_at, entries):
    plan = families.plan(doc, output_id)
    return {
        "version": 1,
        "output": output_id,
        "candidate": candidate_id,
        "source_state_sha256": codec.digest(doc),
        "created_at": created_at,
        "plan": plan,
        "baseline": {
            "candidate": plan["baseline"],
            "record_sha256": codec.record_hash(doc.records[plan["baseline"]]),
        },
        "files": entries,
        "acceptance": {
            "accepted": False,
            "source_status": families.describe(doc, output_id),
        },
        "limits": dict(LIMITS),
    }


def _manifest(doc, artifact, root):
    """Verify the frozen projection and retained bytes, independent of current membership."""
    path = graph.confined(root, artifact.fields["ur"])
    _require(
        path == Path(root).resolve() / artifact.fields["ur"],
        "delivery_storage",
        "manifest directory was redirected",
    )
    _require(
        path.name == "manifest.json" and path.parent.name == artifact.fields["dg"],
        "delivery_storage",
        artifact.id,
    )
    try:
        with path.open("rb") as stream:
            data = stream.read(codec.MAX_BYTES + 1)
        _require(
            len(data) <= codec.MAX_BYTES, "delivery_manifest", "maximum 16 MiB manifest"
        )
        value = json.loads(data)
        _require(
            data == _json(value)
            and hashlib.sha256(data).hexdigest() == artifact.fields["dg"],
            "delivery_manifest",
            artifact.id,
        )
    except (OSError, ValueError, UnicodeError, RecursionError) as error:
        if isinstance(error, PixlError):
            raise
        raise PixlError(
            "delivery_manifest", f"{artifact.id}: unreadable canonical manifest"
        ) from error
    _closed(value, MANIFEST_KEYS, "closed version-1 manifest required")
    _require(
        type(value["version"]) is int and value["version"] == 1,
        "delivery_manifest",
        "unsupported manifest version",
    )
    _require(
        value["candidate"] == artifact.id
        and value["output"] == artifact.fields["of"].id,
        "delivery_manifest",
        "candidate/output projection differs",
    )
    _require(
        _sha(value["source_state_sha256"]),
        "delivery_manifest",
        "invalid source revision",
    )
    platform._iso_timestamp(value["created_at"], "created_at", "delivery_manifest")
    plan = value["plan"]
    _closed(plan, PLAN_KEYS, "closed saved family plan required")
    _require(
        plan["output"] == value["output"]
        and all(_id(plan[k]) for k in ["output", "task", "baseline"]),
        "delivery_manifest",
        "invalid saved plan identity",
    )
    for key, kind in [("members", "F"), ("destinations", "I")]:
        ids = plan[key]
        _require(
            isinstance(ids, list)
            and bool(ids)
            and all(_id(i) for i in ids)
            and len(set(ids)) == len(ids),
            "delivery_manifest",
            f"invalid saved {key}",
        )
        _require(
            all(i in doc.records and doc.records[i].kind == kind for i in ids),
            "delivery_manifest",
            f"missing saved {key}",
        )
    bindings = plan["bindings"]
    _require(
        isinstance(bindings, dict)
        and bool(bindings)
        and all(_id(k) and _sha(v) for k, v in bindings.items()),
        "delivery_manifest",
        "invalid saved plan bindings",
    )
    _require(
        {plan["output"], plan["baseline"], *plan["members"], *plan["destinations"]}
        <= bindings.keys(),
        "delivery_manifest",
        "saved plan omits required bindings",
    )
    _closed(
        value["baseline"], {"candidate", "record_sha256"}, "invalid baseline snapshot"
    )
    baseline = value["baseline"]
    _require(
        baseline["candidate"] == plan["baseline"] and _sha(baseline["record_sha256"]),
        "delivery_manifest",
        "baseline projection differs",
    )
    _require(
        plan["baseline"] in doc.records
        and doc.records[plan["baseline"]].kind == "X"
        and codec.record_hash(doc.records[plan["baseline"]])
        == baseline["record_sha256"],
        "delivery_manifest",
        "retained baseline identity changed",
    )
    _closed(
        value["acceptance"],
        {"accepted", "source_status"},
        "invalid pre-snapshot acceptance description",
    )
    _require(
        value["acceptance"]["accepted"] is False
        and isinstance(value["acceptance"]["source_status"], dict),
        "delivery_manifest",
        "retention cannot create acceptance",
    )
    _require(
        value["limits"] == LIMITS, "delivery_manifest", "retention boundaries differ"
    )
    files = value["files"]
    _require(
        isinstance(files, list)
        and len(files) == len(plan["members"])
        and 0 < len(files) <= MAX_MEMBERS,
        "delivery_manifest",
        "saved membership differs",
    )
    total, selected = 0, [plan["baseline"]]
    for index, item in enumerate(files):
        _closed(item, FILE_KEYS, "invalid member file")
        candidate_id = item["candidate"]
        _require(
            _id(candidate_id)
            and candidate_id in doc.records
            and doc.records[candidate_id].kind == "X",
            "delivery_manifest",
            "missing retained candidate",
        )
        candidate = doc.records[candidate_id]
        _require(
            item["output"] == plan["members"][index]
            and candidate.fields.get("of") == Ref(item["output"]),
            "delivery_manifest",
            "member output projection differs",
        )
        _require(
            item["record_sha256"] == codec.record_hash(candidate)
            and item["source_path"] == candidate.fields["ur"]
            and item["sha256"] == candidate.fields["dg"],
            "delivery_manifest",
            "retained member identity differs",
        )
        _require(
            item["path"] == _file_name(index, item["source_path"]),
            "delivery_manifest",
            "member path differs",
        )
        _require(
            type(item["bytes"]) is int and 0 <= item["bytes"] <= MAX_FILE_BYTES,
            "delivery_limit",
            "invalid retained member size",
        )
        total += item["bytes"]
        _require(total <= MAX_TOTAL_BYTES, "delivery_limit", "package exceeds 512 MiB")
        copied = graph.confined(path.parent, item["path"])
        _require(
            copied == path.parent / item["path"],
            "delivery_storage",
            "member path was redirected",
        )
        _require(
            copied.is_file()
            and copied.stat().st_size == item["bytes"]
            and graph.file_hash(copied) == item["sha256"],
            "delivery_file",
            f"{artifact.id}: {item['path']}",
        )
        selected.append(candidate_id)
    _require(
        artifact.fields["xs"] == [Ref(i) for i in selected],
        "delivery_manifest",
        "typed constituents differ from frozen manifest",
    )
    return value


def _stale(doc, artifact, manifest=None):
    output = artifact.fields["of"].id
    planned = families.plan(doc, output)
    constituents = [r.id for r in artifact.fields["xs"]]
    reasons = []
    if constituents != [planned["baseline"], *families.selection(doc, output)]:
        reasons.append("selected baseline or family members changed")
    if manifest is not None:
        saved = manifest["plan"]
        for key in ["task", "baseline", "members", "destinations"]:
            if saved[key] != planned[key]:
                reasons.append(f"plan {key} changed")
        for id_ in sorted(set(saved["bindings"]) | set(planned["bindings"])):
            if saved["bindings"].get(id_) != planned["bindings"].get(id_):
                reasons.append(id_)
    return reasons


def validate(doc, root=None):
    if doc.format != 2:
        return
    evaluated = {
        r.fields["xr"].id
        for r in doc.records.values()
        if r.kind == "V"
        and not r.fields.get("ob", False)
        and r.fields["st"].value in {"pass", "fail"}
    }
    for artifact in doc.records.values():
        if artifact.kind != "X" or "xs" not in artifact.fields:
            continue
        manifest = _manifest(doc, artifact, root) if root is not None else None
        if artifact.id in evaluated:
            _require(
                not _stale(doc, artifact, manifest),
                "family_stale",
                f"{artifact.id}: supersede current verdicts before changing family selection/plan",
            )


def _storage(artifact, folder, root):
    relative = (
        folder.relative_to(root)
        / "deliveries"
        / artifact.fields["dg"]
        / "manifest.json"
    ).as_posix()
    _require(
        artifact.fields["ur"] == relative
        and graph.confined(root, relative)
        == folder / "deliveries" / artifact.fields["dg"] / "manifest.json",
        "delivery_storage",
        "family snapshots must remain in this store's content-addressed deliveries",
    )


def transitions(current, candidate, root, folder):
    if candidate.format != 2:
        return
    if current is not None:
        for id_, old in current.records.items():
            new = candidate.records[id_]
            if old.kind == "F" and "mb" in old.fields:
                _require(
                    {"bs", "mb", "ds"} <= new.fields.keys(),
                    "delivery_history",
                    "family plans cannot shed their extension",
                )
            if old.kind == "X" and "xs" in old.fields:
                for retained in [id_, *[r.id for r in old.fields["xs"]]]:
                    _require(
                        candidate.records[retained] == current.records[retained],
                        "delivery_history",
                        f"{retained}: published manifest and constituent X records are immutable",
                    )
    for artifact in candidate.records.values():
        if artifact.kind != "X" or "xs" not in artifact.fields:
            continue
        folder, root = _locations(folder, root)
        _require(
            current is not None,
            "delivery_history",
            "save a family plan before publishing a snapshot",
        )
        _storage(artifact, folder, root)
        manifest = _manifest(candidate, artifact, root)
        old = current.records.get(artifact.id)
        if old is not None:
            _require(
                "xs" in old.fields,
                "delivery_history",
                "an existing artifact cannot acquire a fabricated snapshot history",
            )
            continue
        output = artifact.fields["of"].id
        _require(
            output in current.records and "mb" in current.records[output].fields,
            "delivery_plan",
            "save family planning before creating a snapshot",
        )
        _require(
            families.plan(current, output) == families.plan(candidate, output),
            "delivery_plan",
            "save unchanged family planning before a new snapshot",
        )
        _require(
            set(candidate.records) - set(current.records) == {artifact.id}
            and all(
                candidate.records[id_] == record
                for id_, record in current.records.items()
            ),
            "delivery_publication",
            "a new snapshot publication adds only its candidate; publish other changes separately",
        )
        _require(
            not families.snapshot_blockers(current, output)
            and not families.snapshot_blockers(candidate, output),
            "delivery_blocked",
            output,
        )
        entries, _ = _entries(current, output, root)
        expected = _manifest_value(
            current, output, artifact.id, manifest["created_at"], entries
        )
        _require(
            manifest == expected,
            "delivery_plan",
            "snapshot must describe the prior saved state and exact accepted member selection",
        )
        _require(
            not _stale(candidate, artifact, manifest),
            "family_stale",
            "new snapshot selection changed during publication",
        )
        task = candidate.records[manifest["plan"]["task"]]
        _require(
            Ref(artifact.id) not in task.fields["ca"]
            and not any(
                r.kind == "V" and r.fields["xr"] == Ref(artifact.id)
                for r in candidate.records.values()
            ),
            "delivery_acceptance",
            "publish a retained candidate before later nomination/evaluation",
        )


def _write_once(path, data):
    try:
        with path.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        _require(
            path.is_file() and not path.is_symlink() and path.read_bytes() == data,
            "delivery_storage",
            f"existing immutable bytes differ: {path.name}",
        )


def snapshot(folder, expected, output_id, candidate_id, root=None):
    folder, root = _locations(folder, root)
    doc = store.load(folder)
    _require(
        codec.digest(doc) == expected,
        "stale_write",
        "reload current state before creating a family snapshot",
    )
    _require(
        doc.format == 2, "family_format", "family delivery requires explicit PX2 state"
    )
    graph.validate(doc, root)
    _require(
        _id(candidate_id) and candidate_id not in doc.records,
        "delivery_candidate",
        "a new valid candidate ID is required",
    )
    reasons = families.snapshot_blockers(doc, output_id)
    _require(not reasons, "delivery_blocked", "; ".join(reasons))
    entries, snapshots = _entries(doc, output_id, root, capture=True)
    manifest = _manifest_value(
        doc, output_id, candidate_id, datetime.now(UTC).isoformat(), entries
    )
    data = _json(manifest)
    hash_ = hashlib.sha256(data).hexdigest()
    directory = folder / "deliveries" / hash_
    _require(
        graph.confined(root, directory.relative_to(root).as_posix()) == directory,
        "delivery_storage",
        "delivery directory was redirected",
    )
    for parent in [folder / "deliveries", directory, directory / "files"]:
        _require(
            not parent.is_symlink() and parent.resolve() == parent,
            "delivery_storage",
            "delivery directory was redirected",
        )
        parent.mkdir(exist_ok=True)
    for name, contents in snapshots.items():
        _write_once(directory / name, contents)
    _write_once(directory / "manifest.json", data)
    candidate = copy.deepcopy(doc)
    candidate.revision += 1
    relative = (directory / "manifest.json").relative_to(root).as_posix()
    candidate.records[candidate_id] = Record(
        candidate_id,
        "X",
        {
            "nm": doc.records[output_id].fields["nm"] + " retained snapshot",
            "ur": relative,
            "dg": hash_,
            "kd": Symbol("report"),
            "of": Ref(output_id),
            "xs": [
                Ref(manifest["plan"]["baseline"]),
                *[Ref(item["candidate"]) for item in entries],
            ],
        },
    )
    result = store.commit(folder, candidate, expected, root)
    return dict(
        result,
        output=output_id,
        candidate=candidate_id,
        package=directory.relative_to(root).as_posix(),
        manifest=relative,
        accepted=False,
        remote_executed=False,
    )


def report(doc, root, output_id=None):
    _require(
        doc.format == 2, "family_format", "family delivery requires explicit PX2 state"
    )
    _require(
        root is not None,
        "delivery_root",
        "a project root is required to verify retained files",
    )
    graph.validate(doc, root)
    outputs = (
        [output_id]
        if output_id is not None
        else sorted(
            r.id for r in doc.records.values() if r.kind == "F" and "mb" in r.fields
        )
    )
    result = []
    for output in outputs:
        row = families.describe(doc, output)
        snapshots = []
        for artifact in sorted(doc.records.values(), key=lambda r: r.id):
            if artifact.kind != "X" or artifact.fields.get("of") != Ref(output):
                continue
            manifest = _manifest(doc, artifact, root)
            snapshots.append(
                {
                    "candidate": artifact.id,
                    "manifest": artifact.fields["ur"],
                    "sha256": artifact.fields["dg"],
                    "created_at": manifest["created_at"],
                    "source_state_sha256": manifest["source_state_sha256"],
                    "stale": _stale(doc, artifact, manifest),
                    "files": manifest["files"],
                    "retention_is_acceptance": False,
                }
            )
        row["snapshots"] = snapshots
        result.append(row)
    return {
        "format": 2,
        "revision": doc.revision,
        "hash": codec.digest(doc),
        "files_verified": True,
        "families": result,
    }
