"""Source-linked asset requirements and focused host handoffs.

Semantic discovery belongs to the PLAR skill. This module verifies stored claims
and local bindings; it never infers visual quality or invokes a provider.
"""

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from . import graph, store
from .codec import PixlError

MAX_BYTES = 4 * 1024 * 1024
SCHEMA = json.loads(Path(__file__).with_name("plar.schema.json").read_text("utf-8"))


def _bytes(document):
    try:
        data = (
            json.dumps(document, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as error:
        raise PixlError(
            "plar_json", "PLAR requires finite UTF-8 JSON values"
        ) from error
    if len(data) > MAX_BYTES:
        raise PixlError("plar_size", "PLAR exceeds 4 MiB; split by project scope")
    return data


def validate(document, root):
    """Check shape and references without treating missing assets as errors."""
    _bytes(document)
    error = next(Draft202012Validator(SCHEMA).iter_errors(document), None)
    if error:
        location = "/".join(str(part) for part in error.absolute_path)
        raise PixlError("plar_schema", f"{location}: {error.message}")
    sources = {row["id"]: row for row in document["sources"]}
    assets = {row["id"]: row for row in document["assets"]}
    if len(sources) != len(document["sources"]) or len(assets) != len(
        document["assets"]
    ):
        raise PixlError("plar_id", "duplicate source or asset ID")
    for source in sources.values():
        graph.confined(root, source["path"])
    for asset in assets.values():
        references = {row["source"] for row in asset["consumers"]}
        references.update(
            source for row in asset["requirements"] for source in row["sources"]
        )
        if references - sources.keys():
            raise PixlError("plar_source", f"{asset['id']}: unknown source IDs")
        for name in [
            asset["delivery"]["path"],
            *(row["path"] for row in asset["existing"]),
            *(row["path"] for row in asset["evidence"]),
        ]:
            graph.confined(root, name)
        if "production" in asset:
            graph.confined(root, asset["production"]["store"])
        if set(asset["depends_on"]) - assets.keys():
            raise PixlError("plar_dependency", f"{asset['id']}: unknown dependencies")
    # Iterative DFS also accepts long real project dependency chains.
    complete = set()
    for seed in assets:
        active: set[str] = set()
        pending = [(seed, False)]
        while pending:
            current, leaving = pending.pop()
            if leaving:
                active.remove(current)
                complete.add(current)
            elif current in active:
                raise PixlError("plar_dependency", "cyclic asset dependencies")
            elif current not in complete:
                active.add(current)
                pending.append((current, True))
                pending.extend((dep, False) for dep in assets[current]["depends_on"])
    return document


def _load(path):
    from .service import parse_json

    try:
        if path.stat().st_size > MAX_BYTES:
            raise PixlError("plar_size", "PLAR exceeds 4 MiB")
        data = path.read_bytes()
        return parse_json(data.decode("utf-8-sig")), hashlib.sha256(data).hexdigest()
    except (OSError, ValueError, UnicodeError) as error:
        raise PixlError("plar_read", str(path)) from error


def _source_status(root, row):
    path = graph.confined(root, row["path"])
    if not path.is_file():
        return "missing"
    if "sha256" not in row:
        return "unbound"
    return "current" if graph.file_hash(path) == row["sha256"] else "changed"


def read(root, path="plar.txt", asset_id=None):
    """Return queue summaries or one complete selected asset and its inputs."""
    root = Path(root).resolve()
    document, digest = _load(graph.confined(root, path))
    validate(document, root)
    assets = {row["id"]: row for row in document["assets"]}
    sources = {row["id"]: row for row in document["sources"]}
    selected = [assets[asset_id]] if asset_id in assets else []
    if asset_id is not None and not selected:
        raise PixlError("plar_asset", asset_id)
    if asset_id is None:
        selected = list(assets.values())
    source_ids = {row["source"] for asset in selected for row in asset["consumers"]}
    source_ids.update(
        source
        for asset in selected
        for row in asset["requirements"]
        for source in row["sources"]
    )
    if asset_id is None:
        source_ids = set(sources)
    bindings = {
        key: _source_status(root, row)
        for key, row in sources.items()
        if key in source_ids
    }
    result = {
        "hash": digest,
        "project": document["project"],
        "coverage": document["coverage"],
        "sources": [
            dict(row, binding=bindings[key])
            for key, row in sources.items()
            if key in source_ids
        ],
    }
    summaries = []
    for asset in selected:
        ids = {row["source"] for row in asset["consumers"]}
        ids.update(source for row in asset["requirements"] for source in row["sources"])
        issues = [
            f"source {key}: {bindings[key]}"
            for key in sorted(ids)
            if bindings[key] != "current"
        ]
        issues.extend(
            f"missing {row['role']}: {row['path']}"
            for row in asset["existing"]
            if not graph.confined(root, row["path"]).is_file()
        )
        issues.extend(
            f"missing evidence: {row['path']}"
            for row in asset["evidence"]
            if not graph.confined(root, row["path"]).is_file()
        )
        if (
            asset["status"] == "integrated"
            and not graph.confined(root, asset["delivery"]["path"]).exists()
        ):
            issues.append("integrated destination is missing")
        summaries.append(
            {key: asset[key] for key in ("id", "kind", "purpose", "status", "next")}
            | {"issues": issues, "questions": asset["questions"]}
        )
    result["queue"] = summaries
    if asset_id is not None:
        result["asset"] = assets[asset_id]
        result["dependencies"] = [
            {
                "id": dep,
                "status": assets[dep]["status"],
                "next": assets[dep]["next"],
                "delivery": assets[dep]["delivery"],
            }
            for dep in sorted(
                graph.closure(
                    {key: set(row["depends_on"]) for key, row in assets.items()},
                    assets[asset_id]["depends_on"],
                )
            )
        ]
    return result


def save(root, document, expected, path="plar.txt"):
    """CAS save with retained previous bytes; bind only previously unbound sources."""
    root = Path(root).resolve()
    destination = graph.confined(root, path)
    document = copy.deepcopy(document)
    validate(document, root)
    history = graph.confined(root, ".pixl/plar-history")
    lock_folder = graph.confined(root, ".pixl/plar-lock")
    with store.lock(lock_folder):
        previous = destination.read_bytes() if destination.exists() else None
        actual = hashlib.sha256(previous).hexdigest() if previous is not None else "new"
        if actual != expected:
            raise PixlError(
                "stale_write", "reload plar.txt and merge with the current requirements"
            )
        for row in document["sources"]:
            source = graph.confined(root, row["path"])
            if "sha256" not in row and source.is_file():
                row["sha256"] = graph.file_hash(source)
        data = _bytes(document)
        if previous is not None and previous != data:
            history.mkdir(parents=True, exist_ok=True)
            snapshot = graph.confined(history, actual + ".json")
            if snapshot.exists() and snapshot.read_bytes() != previous:
                raise PixlError("history_corrupt", str(snapshot))
            store._atomic(snapshot, previous)
        destination.parent.mkdir(parents=True, exist_ok=True)
        store._atomic(destination, data)
    return read(root, path)
