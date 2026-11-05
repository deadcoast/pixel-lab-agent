"""Closed-schema validation, evidence integrity and deterministic graph queries."""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

from .codec import Document, PixlError, Ref, Symbol, encode, record_hash

REGISTRY = json.loads(
    Path(__file__).with_name("registry.json").read_text(encoding="utf-8")
)
REGISTRIES = {
    1: REGISTRY,
    2: json.loads(
        Path(__file__).with_name("registry-v2.json").read_text(encoding="utf-8")
    ),
}
SHA = re.compile(r"[0-9a-f]{64}")


def refs(value):
    if isinstance(value, Ref):
        yield value.id
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)
    elif isinstance(value, dict):
        for child in value.values():
            yield from refs(child)


def edges(doc):
    return {id_: set(refs(record.fields)) for id_, record in doc.records.items()}


def closure(adjacency, seeds):
    pending = list(seeds)
    found = set()
    while pending:
        id_ = pending.pop()
        if id_ not in found:
            found.add(id_)
            pending.extend(adjacency.get(id_, ()))
    return found


def proof_scope(doc, seeds, adjacency=None):
    """Bind design/method/art semantics, excluding mutable workflow and proof nodes."""
    adjacency = edges(doc) if adjacency is None else adjacency
    semantic = {
        id_: targets
        for id_, targets in adjacency.items()
        if doc.records[id_].kind not in ("EPTJNV" if doc.format == 2 else "EPTJN")
    }
    return set(
        closure(
            {id_: targets & semantic.keys() for id_, targets in semantic.items()},
            set(seeds) & semantic.keys(),
        )
    )


def confined(root, name):
    root = Path(root).resolve()
    path = Path(name)
    if path.is_absolute() or not name or "\\" in name or ":" in name:
        raise PixlError("path_escape", name)
    path = (root / path).resolve()
    if not path.is_relative_to(root) or path == root:
        raise PixlError("path_escape", name)
    return path


def file_hash(path):
    hasher = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _type(value, type_, doc):
    if type_ == "str":
        return type(value) is str
    if type_ == "sha":
        return type(value) is str and bool(SHA.fullmatch(value))
    if type_ == "int":
        return type(value) is int
    if type_ == "bool":
        return type(value) is bool
    if type_ == "map":
        return type(value) is dict
    if type_ == "value":
        return True
    if type_ in ("strings", "ints", "symbols"):
        typ = {"strings": str, "ints": int, "symbols": Symbol}[type_]
        return isinstance(value, list) and all(type(v) is typ for v in value)
    if type_.startswith("sym:"):
        return isinstance(value, Symbol) and value.value in type_[4:].split("|")
    if type_.startswith("refs:"):
        return isinstance(value, list) and all(
            _type(v, f"ref:{type_[5:]}", doc) for v in value
        )
    if type_.startswith("ref:"):
        return (
            isinstance(value, Ref)
            and value.id in doc.records
            and (type_[4:] == "*" or doc.records[value.id].kind == type_[4:])
        )
    raise PixlError("registry_type", type_)


def _require(condition, code, detail):
    if not condition:
        raise PixlError(code, detail)


def _dag(doc):
    tasks = {
        id_: set(refs(r.fields["dp"]))
        for id_, r in doc.records.items()
        if r.kind == "T"
    }
    # Kahn traversal avoids recursion limits for deep, otherwise valid plans.
    dependents: dict[str, set[str]] = {id_: set() for id_ in tasks}
    for id_, needs in tasks.items():
        for needed in needs:
            dependents[needed].add(id_)
    pending = [id_ for id_, needs in tasks.items() if not needs]
    seen = 0
    while pending:
        id_ = pending.pop()
        seen += 1
        for other in dependents[id_]:
            tasks[other].remove(id_)
            if not tasks[other]:
                pending.append(other)
    _require(
        seen == len(tasks), "dependency_cycle", "task prerequisites must form a DAG"
    )


def validate(doc, root=None):
    encode(
        doc
    )  # Check wire-representable values and resource bounds, even for programmatic input.
    registry = REGISTRIES[doc.format]
    for id_, record in doc.records.items():
        _require(record.kind in registry["kinds"], "unknown_kind", record.kind)
        fields = dict(registry["common"], **registry["kinds"][record.kind]["fields"])
        for name in record.fields:
            _require(name in fields, "unknown_field", f"{id_}.{name}")
        for name, spec in fields.items():
            spec = {"type": spec} if isinstance(spec, str) else spec
            if name not in record.fields:
                _require(spec.get("optional", False), "missing_field", f"{id_}.{name}")
                continue
            _require(
                _type(record.fields[name], spec["type"], doc),
                "field_type",
                f"{id_}.{name}: {spec['type']}",
            )
        for target in refs(record.fields):
            _require(target in doc.records, "unresolved_ref", f"{id_} -> {target}")
    _dag(doc)
    adjacency = edges(doc)
    semantic = {
        id_
        for id_, record in doc.records.items()
        if record.kind not in ("EPTJNV" if doc.format == 2 else "EPTJN")
    }
    proof_edges = {
        id_: targets & semantic for id_, targets in adjacency.items() if id_ in semantic
    }
    scope_cache = {}

    def scope(id_):
        if id_ not in scope_cache:
            scope_cache[id_] = closure(proof_edges, [id_]) if id_ in semantic else set()
        return scope_cache[id_]

    def bound(evidence, passing=False):
        result = set()
        for reference in evidence:
            proof = doc.records[reference.id]
            if proof.fields.get("ob", False):
                continue
            if not passing or proof.fields["rs"].value == "pass":
                result.update(refs(proof.fields["bs"]))
        return result

    for id_, record in doc.records.items():
        f = record.fields
        if record.kind == "D":
            for key in ("wt", "wr", "wy", "rs", "pc"):
                _require(
                    bool(f[key])
                    and (not isinstance(f[key], str) or bool(f[key].strip())),
                    "decision_evidence",
                    f"{id_}.{key} is empty",
                )
            _require(
                scope(id_) <= bound(f["pc"]),
                "decision_proof",
                f"{id_}: proof must bind the decision, sources and semantic targets",
            )
        if record.kind == "K":
            for key in ("ap", "op", "ck", "so"):
                _require(bool(f[key]), "knowledge", f"{id_}.{key} is empty")
            if f.get("pc"):
                _require(
                    scope(id_) <= bound(f["pc"]),
                    "method_poc",
                    f"{id_}: proof must bind this method and its sources",
                )
        if record.kind == "R":
            _require(bool(f["so"]) and bool(f["vr"]), "runtime_source", id_)
        if record.kind == "C":
            _require(
                len(f["px"]) == 2 and all(0 < n <= 65536 for n in f["px"]),
                "dimensions",
                id_,
            )
            _require(
                all(
                    re.fullmatch(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?", c)
                    for c in f["pl"]
                ),
                "palette",
                id_,
            )
        if record.kind == "S":
            _require(
                len(f["ln"]) in {0, 2}
                and (not f["ln"] or 1 <= f["ln"][0] <= f["ln"][1]),
                "source_range",
                id_,
            )
            _require(bool(f["ur"]), "source_uri", id_)
        if record.kind in ("S", "E"):
            try:
                datetime.fromisoformat(f["at"])
            except ValueError as error:
                raise PixlError("date", id_) from error
        if record.kind == "E":
            _require(
                isinstance(f["bs"], list) and bool(f["bs"]), "evidence_binding", id_
            )
            targets = set()
            for binding in f["bs"]:
                _require(
                    isinstance(binding, dict) and set(binding) == {"rf", "dg"},
                    "evidence_binding",
                    id_,
                )
                _require(
                    _type(binding["rf"], "ref:*", doc)
                    and _type(binding["dg"], "sha", doc),
                    "evidence_binding",
                    id_,
                )
                target = binding["rf"].id
                _require(
                    target not in targets and doc.records[target].kind != "E",
                    "evidence_binding",
                    f"{id_}: duplicate or recursive proof",
                )
                targets.add(target)
                if not f.get("ob", False):
                    _require(
                        record_hash(doc.records[target]) == binding["dg"],
                        "stale_evidence",
                        f"{id_} binds outdated {target}",
                    )
            for target in targets:
                if doc.records[target].kind == "X" and not f.get("ob", False):
                    dependencies = scope(target)
                    _require(
                        dependencies <= targets,
                        "evidence_context",
                        f"{id_}: bind artifact {target} and its full contract/reference closure",
                    )
        if record.kind == "T" and doc.format == 1:
            _require(bool(f["dc"]), "task_decision", id_)
            if f["st"].value in ("active", "done"):
                for method in f["kn"]:
                    proofs = doc.records[method.id].fields.get("pc", [])
                    _require(
                        scope(method.id) <= bound(proofs, passing=True),
                        "method_poc",
                        method.id,
                    )
            if f["st"].value == "done":
                _require(
                    bool(f["io"])
                    and all(
                        doc.records[d.id].fields["st"].value == "done" for d in f["dp"]
                    ),
                    "completion",
                    f"{id_}: artifacts/prerequisites",
                )
                passing = [
                    doc.records[e.id]
                    for e in f["ev"]
                    if doc.records[e.id].fields["rs"].value == "pass"
                    and not doc.records[e.id].fields.get("ob", False)
                ]
                needed = set(refs(f["io"]))
                covered = (
                    set().union(*(set(refs(e.fields["bs"])) for e in passing))
                    if passing
                    else set()
                )
                _require(
                    needed <= covered,
                    "completion",
                    f"{id_}: evidence must bind all artifacts",
                )
        if record.kind == "J":
            if f["si"].value in ("submitted", "running", "succeeded"):
                _require(bool(f["ri"]), "job_identity", id_)
            if f["si"].value == "succeeded":
                _require(bool(f["ev"]), "job_evidence", id_)
        if record.kind == "N":
            _require(0 <= f["rv"] <= doc.revision, "handoff_revision", id_)
        if root is not None and record.kind in ("S", "X", "E"):
            if record.kind == "S" and urlsplit(f["ur"]).scheme in ("https", "http"):
                continue
            path = confined(root, f["ur"])
            _require(path.is_file(), "file_missing", f"{id_}: {f['ur']}")
            _require(file_hash(path) == f["dg"], "file_hash", f"{id_}: {f['ur']}")
            if record.kind == "S" and f["ln"]:
                try:
                    count = len(path.read_text(encoding="utf-8").splitlines())
                except UnicodeError as error:
                    raise PixlError("source_encoding", id_) from error
                _require(f["ln"][1] <= count, "source_range", id_)
    if doc.format == 2:
        from . import delivery, families, jobs, lifecycle

        families.validate(doc)
        lifecycle.validate(doc, scope, bound)
        jobs.validate(doc, root)
        delivery.validate(doc, root)
    return doc


def ready(doc):
    validate(doc)
    if doc.format == 2:
        from . import lifecycle

        return sorted(
            id_
            for id_, r in doc.records.items()
            if r.kind == "T"
            and r.fields["st"].value == "open"
            and not lifecycle.blockers(doc, id_)
        )
    return sorted(
        id_
        for id_, r in doc.records.items()
        if r.kind == "T"
        and r.fields["st"].value == "open"
        and all(doc.records[d.id].fields["st"].value == "done" for d in r.fields["dp"])
    )


def impact(doc, id_):
    validate(doc)
    _require(id_ in doc.records, "unknown_record", id_)
    reverse: dict[str, set[str]] = {key: set() for key in doc.records}
    for source, targets in edges(doc).items():
        for target in targets:
            reverse[target].add(source)
    return sorted(closure(reverse, [id_]))


def context(doc, focus, budget=None):
    validate(doc)
    _require(focus in doc.records, "unknown_record", focus)
    seeds = {focus} | {id_ for id_, r in doc.records.items() if r.kind == "P"}
    for id_, r in doc.records.items():
        if r.kind in ("J", "N") and focus in set(refs(r.fields)):
            seeds.add(id_)
    selected = closure(edges(doc), seeds)
    packet = Document(
        doc.revision,
        {id_: doc.records[id_] for id_ in sorted(selected)},
        format=doc.format,
    )
    required = len(encode(packet))
    if budget is not None:
        _require(
            type(budget) is int and budget > 0,
            "context_budget",
            "budget must be a positive byte count",
        )
        _require(
            required <= budget,
            "context_budget",
            f"required={required}, budget={budget}; required closure was not truncated",
        )
    return packet
