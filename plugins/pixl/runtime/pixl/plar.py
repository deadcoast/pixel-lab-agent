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
        references = _source_ids(asset)
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


def _source_ids(asset):
    ids = {row["source"] for row in asset["consumers"]}
    ids.update(source for row in asset["requirements"] for source in row["sources"])
    ids.update(row["source"] for row in asset.get("references", []))
    return ids


def _source_binding(root, row):
    path = graph.confined(root, row["path"])
    actual = graph.file_hash(path) if path.is_file() else None
    status = (
        "missing"
        if actual is None
        else "unbound"
        if "sha256" not in row
        else "current"
        if actual == row["sha256"]
        else "changed"
    )
    return dict(row, binding=status, observed_sha256=actual, absolute_path=str(path))


def _issues(root, asset, sources):
    issues = [
        f"source {key}: {sources[key]['binding']}"
        for key in sorted(_source_ids(asset))
        if sources[key]["binding"] != "current"
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
    return issues


def read(root, path="plar.txt", asset_id=None):
    """Return a queue or a complete source-bound delegation context for one asset."""
    root = Path(root).resolve()
    document, digest = _load(graph.confined(root, path))
    validate(document, root)
    assets = {row["id"]: row for row in document["assets"]}
    if asset_id is not None and asset_id not in assets:
        raise PixlError("plar_asset", asset_id)
    dependency_ids = (
        sorted(
            graph.closure(
                {key: set(row["depends_on"]) for key, row in assets.items()},
                assets[asset_id]["depends_on"],
            )
        )
        if asset_id is not None
        else []
    )
    selected = [assets[asset_id]] if asset_id is not None else list(assets.values())
    context_assets = selected + [assets[key] for key in dependency_ids]
    source_ids = set().union(*(_source_ids(asset) for asset in context_assets))
    if asset_id is None:
        source_ids = {row["id"] for row in document["sources"]}
    sources = {
        row["id"]: _source_binding(root, row)
        for row in document["sources"]
        if row["id"] in source_ids
    }
    issues = {row["id"]: _issues(root, row, sources) for row in context_assets}
    result = {
        "hash": digest,
        "project_root": str(root),
        "path": path,
        "project": document["project"],
        "coverage": document["coverage"],
        "sources": list(sources.values()),
        "queue": [
            {key: row[key] for key in ("id", "kind", "purpose", "status", "next")}
            | {"issues": issues[row["id"]], "questions": row["questions"]}
            for row in selected
        ],
    }
    if asset_id is not None:
        result["asset"] = assets[asset_id]
        result["dependencies"] = [
            dict(assets[key], issues=issues[key]) for key in dependency_ids
        ]
        result["visual_references"] = [
            {
                **reference,
                "asset_id": row["id"],
                "path": sources[reference["source"]]["path"],
                "absolute_path": sources[reference["source"]]["absolute_path"],
                "sha256": sources[reference["source"]].get("sha256"),
                "observed_sha256": sources[reference["source"]]["observed_sha256"],
                "binding": sources[reference["source"]]["binding"],
            }
            for row in context_assets
            for reference in row.get("references", [])
        ]
        # Requirements identity excludes queue progress and installation paths.
        # Source drift and transitive dependency requirements still change it.
        semantic = {
            "project": document["project"],
            "assets": [
                {
                    key: value
                    for key, value in row.items()
                    if key not in ("status", "next", "evidence", "production")
                }
                for row in sorted(context_assets, key=lambda row: row["id"])
            ],
            "sources": [
                {
                    key: value
                    for key, value in sources[id_].items()
                    if key != "absolute_path"
                }
                for id_ in sorted(sources)
            ],
        }
        result["requirements_hash"] = hashlib.sha256(
            json.dumps(
                semantic, sort_keys=True, ensure_ascii=False, allow_nan=False
            ).encode("utf-8")
        ).hexdigest()
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
