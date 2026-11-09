"""Explicit supplied-source revisions; historical identities are never fallbacks."""

import hashlib
import json
import re
from pathlib import Path

from .codec import PixlError
from .graph import confined

INVENTORY_PATH = "training/source-inventory.json"


def _require(condition, detail):
    if not condition:
        raise PixlError("source_inventory", detail)


def _object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate field: {key}")
        result[key] = value
    return result


def _identity(row):
    return (
        isinstance(row.get("path"), str)
        and bool(row["path"])
        and isinstance(row.get("sha256"), str)
        and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None
        and type(row.get("lines")) is int
        and row["lines"] > 0
    )


def capture_inventory(root):
    """Return declared revisions and the exact verified inventory/source snapshots.

    The caller owns the inventory; these checks establish identity and freshness,
    not independent authentication of its provenance assertions.
    """
    root = Path(root).resolve()
    inventory = confined(root, INVENTORY_PATH)
    try:
        inventory_bytes = inventory.read_bytes()
        data = json.loads(inventory_bytes.decode("utf-8"), object_pairs_hook=_object)
    except (OSError, UnicodeError, ValueError) as error:
        raise PixlError("source_inventory", f"cannot read {INVENTORY_PATH}") from error
    _require(
        isinstance(data, dict) and set(data) == {"version", "documents"},
        "expected version and documents",
    )
    _require(
        type(data["version"]) is int and data["version"] == 1,
        "unsupported inventory version",
    )
    _require(
        isinstance(data["documents"], list) and bool(data["documents"]),
        "documents must be a nonempty list",
    )
    ids, paths = set(), set()
    snapshots = {INVENTORY_PATH: inventory_bytes}
    for row in data["documents"]:
        _require(
            isinstance(row, dict)
            and set(row) == {"id", "path", "sha256", "lines", "previous"},
            "invalid document fields",
        )
        _require(
            isinstance(row["id"], str)
            and re.fullmatch(r"[a-z][a-z0-9-]{0,95}", row["id"]),
            "invalid source ID",
        )
        _require(_identity(row), f"invalid identity: {row['id']}")
        path = confined(root, row["path"])
        _require(
            row["id"] not in ids and path not in paths, "duplicate source ID or path"
        )
        ids.add(row["id"])
        paths.add(path)
        previous = row["previous"]
        _require(
            previous is None
            or (
                isinstance(previous, dict)
                and set(previous) == {"path", "sha256", "lines"}
                and _identity(previous)
            ),
            "invalid previous identity",
        )
        try:
            snapshot = path.read_bytes()
        except OSError as error:
            raise PixlError("source_missing", row["path"]) from error
        if hashlib.sha256(snapshot).hexdigest() != row["sha256"]:
            raise PixlError(
                "source_hash",
                f"{row['path']}: review changed source before updating its inventory",
            )
        try:
            lines = snapshot.decode("utf-8-sig").splitlines()
        except UnicodeError as error:
            raise PixlError("source_encoding", row["path"]) from error
        if len(lines) != row["lines"]:
            raise PixlError("source_lines", row["path"])
        snapshots[row["path"]] = snapshot
    return data, snapshots


def load_inventory(root):
    """Discover supplied source revisions with local identity verification."""
    return capture_inventory(root)[0]
