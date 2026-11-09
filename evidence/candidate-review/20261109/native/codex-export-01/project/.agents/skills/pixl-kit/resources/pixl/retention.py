"""Explicit retention of project-bound library source revisions."""

import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

from . import codec, graph, store

CACHE = ".pixl/library-sources"


def _managed(root, relative):
    path = graph.confined(root, relative)
    if path != Path(root).resolve() / relative:
        raise codec.PixlError("library_snapshot_path", relative)
    return path


def _key(uri, digest):
    return hashlib.sha256((uri + "\0" + digest).encode("utf-8")).hexdigest()


def _entry_path(root, uri, digest):
    return _managed(root, f"{CACHE}/refs/{_key(uri, digest)}.json")


def _object_path(root, digest):
    if not isinstance(digest, str) or graph.SHA.fullmatch(digest) is None:
        raise codec.PixlError("library_snapshot_corrupt", "invalid object identity")
    return _managed(root, f"{CACHE}/objects/{digest}")


def _retained(root, uri, digest):
    entry_path = _entry_path(root, uri, digest)
    if not entry_path.exists():
        return None
    try:
        entry = json.loads(entry_path.read_text("utf-8"))
        required = {
            "version",
            "uri",
            "sha256",
            "bytes",
            "kit",
            "resource",
            "manifest_sha256",
        }
        if (
            not isinstance(entry, dict)
            or set(entry) != required
            or type(entry["version"]) is not int
            or entry["version"] != 1
            or entry["uri"] != uri
            or entry["sha256"] != digest
            or type(entry["bytes"]) is not int
            or entry["bytes"] < 0
            or not isinstance(entry["kit"], str)
            or not isinstance(entry["resource"], str)
        ):
            raise ValueError("entry does not match the requested source")
        path = _object_path(root, digest)
        if path.stat().st_size != entry["bytes"] or graph.file_hash(path) != digest:
            raise ValueError("retained source bytes changed")
        manifest_path = _object_path(root, entry["manifest_sha256"])
        if graph.file_hash(manifest_path) != entry["manifest_sha256"]:
            raise ValueError("retained bundle manifest changed")
        manifest = json.loads(manifest_path.read_text("utf-8"))
        rows = [row for row in manifest["files"] if row["path"] == entry["resource"]]
        if len(rows) != 1 or rows[0]["sha256"] != digest:
            raise ValueError("source is not identified by its retained bundle")
        graph.confined(root, entry["kit"])
        if not entry["resource"].startswith("resources/"):
            raise ValueError("not a kit resource")
        graph.confined(root, entry["resource"])
        declared = graph.confined(
            root, (Path(entry["kit"]) / entry["resource"]).as_posix()
        )
        if declared != graph.confined(root, uri):
            raise ValueError("retained resource does not match its declared locator")
        return path, entry
    except (OSError, ValueError, KeyError, TypeError) as error:
        raise codec.PixlError("library_snapshot_corrupt", f"{uri}: {error}") from error


def resolve(root, uri, expected):
    """Resolve only an explicitly retained revision; never alter the requested hash."""
    original = graph.confined(root, uri)
    if original.is_file() and graph.file_hash(original) == expected:
        return original
    retained = _retained(root, uri, expected)
    return retained[0] if retained else original


def report(doc, root):
    if root is None:
        return []
    result = []
    for record in doc.records.values():
        if record.kind != "S" or urlsplit(record.fields["ur"]).scheme in (
            "http",
            "https",
        ):
            continue
        uri, expected = record.fields["ur"], record.fields["dg"]
        original = graph.confined(root, uri)
        actual = graph.file_hash(original) if original.is_file() else None
        if actual == expected:
            continue
        retained = _retained(root, uri, expected)
        row = {
            "source": record.id,
            "uri": uri,
            "expected_sha256": expected,
            "current_sha256": actual,
            "location_status": "missing" if actual is None else "changed",
            "retained_path": str(retained[0]) if retained else None,
            "status": "retained_revision" if retained else "unavailable",
        }
        if retained:
            row["kit_manifest_sha256"] = retained[1]["manifest_sha256"]
        result.append(row)
    return result


def _publish(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise codec.PixlError("library_snapshot_corrupt", str(path))
    else:
        store._atomic(path, data)


def retain(folder, expected, library, root=None, from_library=None):
    """Pin sources without rewriting project state or its existing proof bindings."""
    folder = Path(folder).resolve()
    root = Path(root).resolve() if root is not None else folder.parent
    if not folder.is_relative_to(root):
        raise codec.PixlError("path_escape", str(folder))
    kit = graph.confined(root, library)
    donor = graph.confined(root, from_library or library)
    with store.lock(folder):
        doc = store.load(folder)
        graph.validate(doc)
        if codec.digest(doc) != expected:
            raise codec.PixlError(
                "stale_write", "reload the project before retaining sources"
            )
        manifest_path = graph.confined(donor, "bundle-manifest.json")
        try:
            manifest_data = manifest_path.read_bytes()
            manifest = json.loads(manifest_data)
            rows = manifest["files"]
            inventory = {row["path"]: row for row in rows}
            if len(inventory) != len(rows):
                raise ValueError("duplicate bundle paths")
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise codec.PixlError("library_manifest", str(manifest_path)) from error
        manifest_hash = hashlib.sha256(manifest_data).hexdigest()
        pending = {}
        selected = []
        for record in doc.records.values():
            if record.kind != "S" or urlsplit(record.fields["ur"]).scheme in (
                "http",
                "https",
            ):
                continue
            uri, digest = record.fields["ur"], record.fields["dg"]
            location = graph.confined(root, uri)
            if not location.is_relative_to(kit / "resources"):
                continue
            selected.append(record.id)
            if _retained(root, uri, digest):
                continue
            resource = location.relative_to(kit).as_posix()
            row = inventory.get(resource)
            source = graph.confined(donor, resource)
            try:
                data = source.read_bytes()
            except OSError as error:
                raise codec.PixlError(
                    "library_source_missing",
                    f"{record.id}: need original bytes {digest} for {uri}",
                ) from error
            if (
                row is None
                or row.get("sha256") != digest
                or hashlib.sha256(data).hexdigest() != digest
            ):
                raise codec.PixlError(
                    "library_source_hash",
                    f"{record.id}: need original bytes {digest}; supply the matching original kit",
                )
            if record.fields["ln"]:
                try:
                    lines = len(data.decode("utf-8").splitlines())
                except UnicodeError as error:
                    raise codec.PixlError("source_encoding", record.id) from error
                if record.fields["ln"][1] > lines:
                    raise codec.PixlError("source_range", record.id)
            entry = {
                "version": 1,
                "uri": uri,
                "sha256": digest,
                "bytes": len(data),
                "kit": library,
                "resource": resource,
                "manifest_sha256": manifest_hash,
            }
            pending[uri, digest] = (data, entry)
        if not selected:
            raise codec.PixlError(
                "library_sources", "no project S records reference this kit's resources"
            )
        # All selected source bytes were checked before publishing any new entry.
        _publish(_object_path(root, manifest_hash), manifest_data)
        for (uri, digest), (data, entry) in pending.items():
            _publish(_object_path(root, digest), data)
            encoded = (json.dumps(entry, sort_keys=True, indent=2) + "\n").encode(
                "utf-8"
            )
            _publish(_entry_path(root, uri, digest), encoded)
        return {
            "hash": expected,
            "revision": doc.revision,
            "state_changed": False,
            "sources": sorted(selected),
            "new_snapshots": len(pending),
            "retained_sources": report(doc, root),
            "scope": "Exact declared library-source revisions; no new proof, verdict, or provider action.",
        }
