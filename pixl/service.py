"""Shared local operation surface used by CLI and MCP."""

import hashlib
import json
import os
from pathlib import Path

from . import assets, catalog, codec, graph, jobs, store
from .codec import PixlError


def resource_root():
    if plugin := os.environ.get("PIXL_PLUGIN_ROOT"):
        return Path(plugin).resolve() / "resources"
    packaged = Path(__file__).with_name("resources")
    if packaged.is_dir():
        return packaged
    return Path(__file__).resolve().parent.parent


def source_slice(path, expected, start, end, budget=16384):
    data = Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise PixlError(
            "source_hash", "source changed; reindex and reassess dependent claims"
        )
    if any(type(n) is not int for n in (start, end, budget)) or budget < 1:
        raise PixlError(
            "source_range", "integer line bounds and positive byte budget required"
        )
    try:
        lines = data.decode("utf-8-sig").splitlines(keepends=True)
    except UnicodeError as error:
        raise PixlError("source_encoding", str(path)) from error
    if not 1 <= start <= end <= len(lines):
        raise PixlError("source_range", f"source contains {len(lines)} lines")
    text = "".join(lines[start - 1 : end])
    size = len(text.encode("utf-8"))
    if size > budget:
        raise PixlError(
            "source_budget", f"required={size}, budget={budget}; narrow the line range"
        )
    return {"text": text, "sha256": expected, "start": start, "end": end, "bytes": size}


def load_document(path):
    try:
        if Path(path).stat().st_size > codec.MAX_BYTES:
            raise PixlError("input_size", "document exceeds 16 MiB")
        return codec.parse(Path(path).read_bytes())
    except OSError as error:
        raise PixlError("file_read", str(path)) from error


def _reject_constant(value):
    raise PixlError("json", "nonfinite number")


def _unique_members(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            # Do not include supplied values (which may contain credentials).
            raise PixlError("json", "duplicate object member")
        result[key] = value
    return result


def parse_json(data):
    """Decode host input without silently discarding conflicting members."""
    return json.loads(
        data, parse_constant=_reject_constant, object_pairs_hook=_unique_members
    )


def read_json(path):
    try:
        return parse_json(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise PixlError("json_read", str(path)) from error


def knowledge(method=None):
    data = read_json(resource_root() / "knowledge" / "pixel-art.json")
    if method:
        if matches := [m for m in data["methods"] if m["id"] == method]:
            return matches[0]
        else:
            raise PixlError("unknown_method", method)
    return {
        "version": data["version"],
        "methods": [
            {"id": m["id"], "title": m["title"], "applies_to": m["applies_to"]}
            for m in data["methods"]
        ],
    }


def source_inventory(root=None):
    from .sources import load_inventory

    selected = resource_root() if root is None else Path(root).resolve()
    return dict(
        load_inventory(selected),
        root=str(selected),
        files_verified=True,
        authority="Declared source revisions; local byte identity verified, not external truth.",
    )


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
    if not isinstance(data, dict):
        raise PixlError("platform_catalog", "capability catalog must be an object")
    return {
        "version": data.get("version"),
        "retrieved_at": data.get("retrieved_at"),
        "source": data.get("source"),
        "live_discovery": False,
        "tools": [
            {
                k: row.get(k)
                for k in ("name", "category", "effect", "required", "poll_tool")
            }
            for row in data["tools"]
        ],
    }


def from_json(data):
    if (
        not isinstance(data, dict)
        or set(data) not in ({"revision", "records"}, {"format", "revision", "records"})
        or not isinstance(data["records"], list)
    ):
        raise PixlError(
            "document_shape", "expected {revision, records:[{id,kind,fields}]}"
        )
    doc = codec.Document(data["revision"], format=data.get("format", 1))
    for row in data["records"]:
        if not isinstance(row, dict) or set(row) != {"id", "kind", "fields"}:
            raise PixlError(
                "record_shape", "exact id/kind/fields required; duplicate IDs forbidden"
            )
        row_id = row["id"]
        row_kind = row["kind"]
        row_fields = row["fields"]
        if (
            not isinstance(row_id, str)
            or not isinstance(row_kind, str)
            or row_id in doc.records
        ):
            raise PixlError(
                "record_shape", "exact id/kind/fields required; duplicate IDs forbidden"
            )
        if not isinstance(row_fields, dict):
            raise PixlError("record_shape", "record fields must be a map")
        fields = from_data(row_fields)
        if not isinstance(fields, dict):
            raise PixlError("record_shape", "decoded record fields must be a map")
        doc.records[row_id] = codec.Record(row_id, row_kind, fields)
    graph.validate(doc)
    return doc


def inspect_document(path, root=None):
    doc = load_document(path)
    graph.validate(doc, root)
    return {
        "valid": True,
        "format": doc.format,
        "revision": doc.revision,
        "hash": codec.digest(doc),
        "records": len(doc.records),
        "files_verified": root is not None,
        "record_hashes": {
            id_: codec.record_hash(r) for id_, r in sorted(doc.records.items())
        },
    }


def workflow(path, root=None):
    from . import lifecycle

    doc = load_document(path)
    graph.validate(doc, root)
    if doc.format != 2:
        raise PixlError(
            "lifecycle_format",
            "workflow requires PX2; PX1 state retains its original rules",
        )
    return dict(
        lifecycle.report(doc),
        format=2,
        revision=doc.revision,
        hash=codec.digest(doc),
        files_verified=root is not None,
    )


JOB_REQUEST_FIELDS = (
    "provider",
    "tool",
    "arguments",
    "schema",
    "discovery",
    "authorization",
)


def job_prepare(folder, expected, job_id, task_id, outputs, request, root=None):
    """Validate the request envelope before publishing durable provider intent."""
    if not isinstance(request, dict) or set(request) != set(JOB_REQUEST_FIELDS):
        raise PixlError(
            "job_request",
            "request must contain exactly provider, tool, arguments, schema, discovery and authorization",
        )
    return jobs.prepare(
        folder,
        expected,
        job_id,
        task_id,
        outputs,
        **request,
        root=root,
    )


def job_report(path, root):
    return jobs.report(load_document(path), root)


def family_report(path, root, output_id=None):
    """Verify retained family files and describe the current saved selection."""
    from . import delivery

    return delivery.report(load_document(path), root, output_id)


def inspection_report(path, root, packet_id=None):
    """Verify retained inspection data and report original conditions and reviews."""
    from . import inspection

    return inspection.report(load_document(path), root, packet_id)


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
        return {
            "wire": wire.decode("utf-8"),
            "bytes": len(wire),
            "hash": codec.digest(doc),
            "revision": doc.revision,
        }
    if name == "pixl_init":
        return store.initialize(
            path("store"), root=root, name=args.get("name", "PIXL project")
        )
    if name == "pixl_intake":
        return store.initialize(
            path("store"),
            doc=store.intake_project(
                args.get("name", "PIXL project"), args.get("brief", "")
            ),
            root=root,
        )
    if name == "pixl_workflow":
        return workflow(path("path"), root)
    if name == "pixl_inspection":
        return inspection_report(path("path"), root, args.get("packet_id"))
    if name == "pixl_inspection_prepare":
        from . import inspection

        return inspection.prepare(
            path("store"),
            args["expect"],
            args["candidate_id"],
            args["packet_id"],
            args["options"],
            root,
        )
    if name == "pixl_inspection_review":
        from . import inspection

        return inspection.review(
            path("store"),
            args["expect"],
            args["packet_id"],
            args["review_id"],
            args["observation"],
            root,
        )
    if name == "pixl_family":
        return family_report(path("path"), root, args.get("output"))
    if name == "pixl_family_snapshot":
        from . import delivery

        return delivery.snapshot(
            path("store"),
            args["expect"],
            args["output_id"],
            args["candidate_id"],
            root,
        )
    if name == "pixl_job_prepare":
        return job_prepare(
            path("store"),
            args["expect"],
            args["job_id"],
            args["task_id"],
            args["outputs"],
            {key: args[key] for key in JOB_REQUEST_FIELDS},
            root,
        )
    if name == "pixl_job_dispatch":
        return jobs.dispatch(path("store"), args["expect"], args["job_id"], root)
    if name == "pixl_job_observe":
        return jobs.observe(
            path("store"),
            args["expect"],
            args["job_id"],
            args["event"],
            args["evidence"],
            remote_id=args.get("remote_id"),
            root=root,
        )
    if name == "pixl_job_import":
        return jobs.import_artifact(
            path("store"),
            args["expect"],
            args["job_id"],
            args["output_id"],
            args["candidate_id"],
            args["path"],
            args["evidence"],
            root,
        )
    if name == "pixl_jobs":
        return job_report(path("path"), root)
    if name == "pixl_commit":
        if ("candidate" in args) == ("document" in args):
            raise PixlError(
                "commit_input", "supply exactly one candidate path or document"
            )
        candidate = (
            from_json(args["document"])
            if "document" in args
            else load_document(path("candidate"))
        )
        return store.commit(path("store"), candidate, args["expect"], root=root)
    if name in ("pixl_plar_read", "pixl_plar_save"):
        from . import plar

        if name == "pixl_plar_read":
            return plar.read(root, args.get("path", "plar.txt"), args.get("asset_id"))
        return plar.save(
            root, args["document"], args["expect"], args.get("path", "plar.txt")
        )
    if name == "pixl_catalog":
        return catalog.build(root, args.get("paths"))
    if name == "pixl_sources":
        return source_inventory()
    if name == "pixl_source":
        scope = args.get("scope", "project")
        if scope not in ("project", "library"):
            raise PixlError("source_scope", scope)
        source_path = (
            graph.confined(resource_root(), args["path"])
            if scope == "library"
            else path("path")
        )
        return source_slice(
            source_path,
            args["expect"],
            args["start"],
            args["end"],
            args.get("budget", 16384),
        )
    if name == "pixl_asset_check":
        return assets.inspect(
            path("path"),
            args.get("width"),
            args.get("height"),
            args.get("palette"),
            args.get("alpha", "binary"),
        )
    if name == "pixl_encode":
        return {"wire": codec.encode(from_json(args["document"])).decode("utf-8")}
    if name == "pixl_knowledge":
        return knowledge(args.get("method"))
    if name in ("pixl_capabilities", "pixl_prepare", "pixl_job"):
        from . import platform

        if name == "pixl_capabilities":
            return capability_index(args.get("name"))
        if name == "pixl_prepare":
            return platform.prepare(
                args["tool"],
                args["arguments"],
                args["schema"],
                args.get("authorization"),
            )
        return platform.job_update(
            args["job"], args["event"], args.get("remote_id"), args.get("evidence")
        )
    raise PixlError("unknown_tool", name)
