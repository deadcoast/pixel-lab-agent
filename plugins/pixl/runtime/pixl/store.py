"""Local compare-and-swap snapshot store. No remote actions or implicit recovery."""

from contextlib import contextmanager
import json
import os
from pathlib import Path
import tempfile

from .codec import Document, PixlError, Record, Ref, Symbol, digest, encode, parse
from .graph import validate, closure, edges

TRANSITIONS = {"open": {"active", "blocked", "dropped"},
               "active": {"blocked", "done", "dropped"},
               "blocked": {"open", "active", "dropped"},
               "done": {"open"}, "dropped": {"open"}}
JOB_TRANSITIONS = {"prepared": {"submitted", "unknown", "failed"},
                   "submitted": {"running", "succeeded", "failed", "unknown"},
                   "running": {"succeeded", "failed", "unknown"},
                   "unknown": {"submitted", "running", "succeeded", "failed"},
                   "succeeded": set(), "failed": set()}


@contextmanager
def lock(folder):
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / ".lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise PixlError("store_locked", f"{path}; inspect owner PID and ensure no writer remains before removing a stale lock") from error
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid()}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        yield
    finally:
        path.unlink(missing_ok=True)


def _atomic(path, data):
    path = Path(path)
    fd, temp = tempfile.mkstemp(prefix=".pixl-write-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        Path(temp).unlink(missing_ok=True)


def _publish(folder, doc):
    data, hash_ = encode(doc), digest(doc)
    history = folder / "history"
    if history.is_symlink() or not history.resolve().is_relative_to(folder):
        raise PixlError("store_path", "history must remain inside the store")
    history.mkdir(exist_ok=True)
    snapshot = history / (hash_ + ".px")
    if snapshot.is_symlink() or not snapshot.resolve().is_relative_to(folder):
        raise PixlError("store_path", "snapshot must remain inside the store")
    if snapshot.exists():
        if snapshot.read_bytes() != data:
            raise PixlError("history_corrupt", str(snapshot))
    else:
        _atomic(snapshot, data)
    _atomic(folder / "state.px", data)
    return {"revision": doc.revision, "hash": hash_, "state": str(folder / "state.px")}


def empty_project(name="PIXL project"):
    actor = Record("actor", "A", {"nm": "PIXL", "rl": Symbol("agent")})
    contract = Record("contract", "C", {"nm": "unconfirmed-intake", "px": [32, 32], "pl": [],
                      "vw": Symbol("side"), "sa": Symbol("nearest"), "al": Symbol("binary"),
                      "li": "INTAKE DEFAULTS ONLY: replace with source-grounded project intent before generation"})
    project = Record("project", "P", {"nm": name, "ow": Ref("actor"), "ct": Ref("contract"), "sc": []})
    return Document(0, {r.id: r for r in (actor, contract, project)})


def initialize(folder, doc=None, root=None, name="PIXL project"):
    folder = Path(folder).resolve()
    doc = empty_project(name) if doc is None else doc
    with lock(folder):
        if (folder / "state.px").exists():
            raise PixlError("store_exists", str(folder))
        if doc.revision != 0:
            raise PixlError("revision", "initial state must be revision 0")
        validate(doc, root if root is not None else folder.parent)
        return _publish(folder, doc)


def load(folder):
    path = Path(folder) / "state.px"
    try:
        return parse(path.read_bytes())
    except OSError as error:
        raise PixlError("store_read", str(path)) from error


def _transitions(current, candidate):
    adjacency = edges(current)
    for id_, old in current.records.items():
        new = candidate.records.get(id_)
        if old.kind == "T" and old.fields["st"].value == "done" and new is not None and new.fields.get("st") == Symbol("done"):
            for dependency in closure(adjacency, [id_]):
                if current.records[dependency] != candidate.records.get(dependency):
                    raise PixlError("reopen_required", f"{id_}: dependency {dependency} changed")
    for id_, old in current.records.items():
        if id_ not in candidate.records:
            raise PixlError("record_removal", id_)
        new = candidate.records[id_]
        if old.kind != new.kind:
            raise PixlError("record_kind_change", id_)
        if old.kind == "E":
            old_fields = {k: v for k, v in old.fields.items() if k != "ob"}
            new_fields = {k: v for k, v in new.fields.items() if k != "ob"}
            if old_fields != new_fields or (old.fields.get("ob", False) and not new.fields.get("ob", False)):
                raise PixlError("evidence_immutable", f"{id_}: supersede with ob=+ and add a new receipt ID")
        if old.kind in ("T", "J"):
            field, transitions = ("st", TRANSITIONS) if old.kind == "T" else ("si", JOB_TRANSITIONS)
            before, after = old.fields[field], new.fields.get(field)
            if not isinstance(after, Symbol):
                raise PixlError("transition", f"{id_}: missing state")
            if before != after and after.value not in transitions[before.value]:
                raise PixlError("transition", f"{id_}: {before.value} -> {after.value}")
            if old.kind == "T" and before.value == "done" and after.value == "done" and old != new:
                raise PixlError("reopen_required", id_)
            if old.kind == "J":
                for key in ("tk", "tl", "ah"):
                    if old.fields[key] != new.fields.get(key):
                        raise PixlError("job_intent_change", f"{id_}.{key}")
                if old.fields["ri"] and old.fields["ri"] != new.fields.get("ri"):
                    raise PixlError("job_identity_change", id_)


def commit(folder, candidate, expected, root=None):
    folder = Path(folder).resolve()
    with lock(folder):
        current = load(folder)
        validate(current)  # Drift in files can be repaired by a correctly grounded candidate.
        if digest(current) != expected:
            raise PixlError("stale_write", "reload state and recompute the candidate from the current revision")
        if candidate.revision != current.revision + 1:
            raise PixlError("revision", f"expected {current.revision + 1}")
        _transitions(current, candidate)
        validate(candidate, root if root is not None else folder.parent)
        return _publish(folder, candidate)
