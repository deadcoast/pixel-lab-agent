"""Shared local operation surface used by CLI and MCP."""

import json
import hashlib
import os
from pathlib import Path

from . import assets, catalog, codec, graph, store
from .codec import PixlError


def resource_root():
    plugin = os.environ.get("PIXL_PLUGIN_ROOT")
    if plugin:
        return Path(plugin).resolve() / "resources"
    packaged = Path(__file__).with_name("resources")
    if packaged.is_dir():
        return packaged
    return Path(__file__).resolve().parent.parent


def source_slice(path, expected, start, end, budget=16384):
    data = Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise PixlError("source_hash", "source changed; reindex and reassess dependent claims")
    if any(type(n) is not int for n in (start, end, budget)) or budget < 1:
        raise PixlError("source_range", "integer line bounds and positive byte budget required")
    try:
        lines = data.decode("utf-8-sig").splitlines(keepends=True)
    except UnicodeError as error:
        raise PixlError("source_encoding", str(path)) from error
    if not 1 <= start <= end <= len(lines):
        raise PixlError("source_range", f"source contains {len(lines)} lines")
    text = "".join(lines[start - 1:end])
    size = len(text.encode("utf-8"))
    if size > budget:
        raise PixlError("source_budget", f"required={size}, budget={budget}; narrow the line range")
    return {"text": text, "sha256": expected, "start": start, "end": end, "bytes": size}


def load_document(path):
    try:
        if Path(path).stat().st_size > codec.MAX_BYTES:
            raise PixlError("input_size", "document exceeds 16 MiB")
        return codec.parse(Path(path).read_bytes())
    except OSError as error:
        raise PixlError("file_read", str(path)) from error


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"), parse_constant=lambda v: (_ for _ in ()).throw(PixlError("json", "nonfinite number")))
    except (OSError, ValueError) as error:
        raise PixlError("json_read", str(path)) from error


def knowledge(method=None):
    data = read_json(resource_root() / "knowledge" / "pixel-art.json")
    if method:
        matches = [m for m in data["methods"] if m["id"] == method]
        if not matches:
            raise PixlError("unknown_method", method)
        return matches[0]
    return {"version": data["version"], "methods": [{"id": m["id"], "title": m["title"],
                                                      "applies_to": m["applies_to"]} for m in data["methods"]]}


def from_data(value):
    if isinstance(value, list):
        return [from_data(v) for v in value]
    if isinstance(value, dict):
        if set(value) == {"$ref"}:
            return codec.Ref(value["$ref"])
        if set(value) == {"$symbol"}:
            return codec.Symbol(value["$symbol"])
        return {k: from_data(v) for k, v in value.items()}
    return value


def capability_index(name=None):
    from .platform import capabilities
    data = capabilities(name)
    if name is not None:
        return data
    return {"version": data.get("version"), "retrieved_at": data.get("retrieved_at"),
            "source": data.get("source"), "live_discovery": False,
            "tools": [{k: row.get(k) for k in ("name", "category", "effect", "required", "poll_tool")} for row in data["tools"]]}


def from_json(data):
    if not isinstance(data, dict) or set(data) != {"revision", "records"} or not isinstance(data["records"], list):
        raise PixlError("document_shape", "expected {revision, records:[{id,kind,fields}]}")
    doc = codec.Document(data["revision"])
    for row in data["records"]:
        if not isinstance(row, dict) or set(row) != {"id", "kind", "fields"} or row["id"] in doc.records:
            raise PixlError("record_shape", "exact id/kind/fields required; duplicate IDs forbidden")
        doc.records[row["id"]] = codec.Record(row["id"], row["kind"], from_data(row["fields"]))
    graph.validate(doc)
    return doc


def inspect_document(path, root=None):
    doc = load_document(path)
    graph.validate(doc, root)
    return {"valid": True, "revision": doc.revision, "hash": codec.digest(doc),
            "records": len(doc.records), "files_verified": root is not None,
            "record_hashes": {id_: codec.record_hash(r) for id_, r in sorted(doc.records.items())}}


def call(name, args, root):
    root = Path(root).resolve()
    def path(key):
        return graph.confined(root, args[key])
    if name == "pixl_validate":
        return inspect_document(path("path"), root)
    if name in ("pixl_context", "pixl_ready", "pixl_impact"):
        doc = load_document(path("path"))
        graph.validate(doc, root)
        if name == "pixl_ready":
            return {"ready": graph.ready(doc), "hash": codec.digest(doc)}
        if name == "pixl_impact":
            return {"affected": graph.impact(doc, args["id"])}
        packet = graph.context(doc, args["focus"], args.get("budget"))
        wire = codec.encode(packet)
        return {"wire": wire.decode("utf-8"), "bytes": len(wire), "hash": codec.digest(doc), "revision": doc.revision}
    if name == "pixl_init":
        return store.initialize(path("store"), root=root, name=args.get("name", "PIXL project"))
    if name == "pixl_commit":
        return store.commit(path("store"), load_document(path("candidate")), args["expect"], root=root)
    if name == "pixl_catalog":
        return catalog.build(root, args.get("paths"))
    if name == "pixl_source":
        return source_slice(path("path"), args["expect"], args["start"], args["end"], args.get("budget", 16384))
    if name == "pixl_asset_check":
        return assets.inspect(path("path"), args.get("width"), args.get("height"), args.get("palette"), args.get("alpha", "binary"))
    if name == "pixl_encode":
        return {"wire": codec.encode(from_json(args["document"])).decode("utf-8")}
    if name == "pixl_knowledge":
        return knowledge(args.get("method"))
    if name in ("pixl_capabilities", "pixl_prepare", "pixl_job"):
        from . import platform
        if name == "pixl_capabilities":
            return capability_index(args.get("name"))
        if name == "pixl_prepare":
            return platform.prepare(args["tool"], args["arguments"], args["schema"], args.get("authorization"))
        return platform.job_update(args["job"], args["event"], args.get("remote_id"), args.get("evidence"))
    raise PixlError("unknown_tool", name)
