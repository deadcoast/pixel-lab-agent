"""Shared local operation surface used by CLI and MCP."""

import hashlib
import json
import os
from pathlib import Path

from . import assets, catalog, codec, graph, jobs, store
from .codec import PixlError

RESULT_EXPORT_TOOLS = {
    "pixl_context", "pixl_request_review", "pixl_review_context", "pixl_candidate_review",
    "pixl_family", "pixl_family_snapshot", "pixl_plar_handoff",
}


def describe_result(operation, result):
    """Add presentation-only hash domains; never alter stored bytes or identities."""
    if not isinstance(result, dict):
        return result
    operation = operation.removeprefix("pixl_").replace("-", "_")
    state_operations = {
        "validate", "context", "ready", "init", "intake", "commit", "workflow",
        "retain_library", "task_complete", "family", "family_snapshot", "jobs",
        "job_prepare", "job_dispatch", "job_observe", "job_import", "inspection",
        "inspection_prepare", "inspection_review", "production_plan", "stage_prepare",
        "plar_prepare", "review_context", "candidate_review",
    }
    fields = {}
    if operation in state_operations:
        fields["hash"] = "canonical_state_sha256"
    if operation in {"plar_read", "plar_save"}:
        fields.update({"hash": "file_sha256", "production.continuation.state_hash": "canonical_state_sha256"})
    if operation in {"plar_read", "plar_save", "plar_prepare", "plar_handoff"}:
        fields["requirements_hash"] = "selected_requirements_sha256"
    if operation in {"review_context", "candidate_review", "plar_handoff"}:
        fields["state_hash"] = "canonical_state_sha256"
    if operation in {"review_context", "candidate_review"}:
        fields.update({"binding_hash": "candidate_bindings_sha256", "review_sha256": "file_sha256",
                       "candidate_file.sha256": "file_sha256",
                       "snapshot_acceptance.source_state_hash": "canonical_state_sha256"})
    if operation == "request_review":
        fields.update({"state.sha256": "canonical_state_sha256", "plan.sha256": "file_sha256",
                       "review_scope_sha256": "review_scope_sha256", "comparison_sha256": "comparison_report_sha256",
                       "before.review_scope_sha256": "review_scope_sha256", "after.review_scope_sha256": "review_scope_sha256",
                       "before.plan.sha256": "file_sha256", "after.plan.sha256": "file_sha256",
                       "packet.sha256": "file_sha256", "request.sha256": "file_sha256",
                       "criteria.sha256": "file_sha256", "request.intent_sha256": "provider_intent_sha256"})
    if operation in {"source", "plar_handoff", "asset_check"}:
        fields["sha256"] = "file_sha256"
    labels = dict(result.get("hash_domains", {}))
    for field, domain in fields.items():
        value = result
        for part in field.split("."):
            value = value.get(part) if isinstance(value, dict) else None
        if value is not None:
            labels[field] = domain
    return {**result, "hash_domains": labels} if labels else result


def operation_error(operation, error):
    """Keep error codes stable while naming the expected publication identity."""
    if error.code != "stale_write":
        return error
    operation = operation.removeprefix("pixl_").replace("-", "_")
    hint = ("expect is the current PLAR file SHA-256 from plar read.hash (or new for first save)"
            if operation == "plar_save" else
            "expect is the current canonical production state hash from validate.hash or review-context.state_hash; not a PLAR, requirements, binding or exported-file hash")
    return error if hint in error.detail else PixlError(error.code, f"{error.detail}; {hint}")


def result_destination(root, relative):
    """Preflight a fresh project-relative output before a potentially mutating call."""
    if root is None:
        raise PixlError("result_path", "an explicit project root is required")
    path = graph.confined(root, relative)
    if path.exists():
        raise PixlError("result_exists", "choose a fresh result path; existing files are preserved")
    return path


def save_result(result, root, relative, data=None):
    """Save exact output without model transcription; retain operation results on I/O failure."""
    encoded = data if data is not None else (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    try:
        path = result_destination(root, relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
    except (OSError, PixlError) as error:
        return {"result_saved": False, "result_path": relative,
                "result_error": str(error), "operation_result": result,
                **({"wire_result": data.decode("utf-8")} if data is not None else {})}
    return {"result_saved": True, "result_path": relative,
            "result_sha256": hashlib.sha256(encoded).hexdigest(), "result_bytes": len(encoded),
            "media_type": "text/plain" if data is not None else "application/json",
            "hash_domains": {"result_sha256": "file_sha256", **({key: domain for key, domain in result.get("hash_domains", {}).items()
                            if key in ("hash", "state_hash")} if isinstance(result, dict) else {})},
            **({key: result[key] for key in ("state_hash", "hash", "revision", "review", "candidate", "task_status", "reused_review", "status", "pass")
                if key in result} if isinstance(result, dict) else {})}


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


def _with_retained_sources(result, doc, root):
    from .retention import report

    retained = report(doc, root)
    if retained:
        result["retained_sources"] = retained
    return result


def inspect_document(path, root=None):
    doc = load_document(path)
    graph.validate(doc, root)
    return _with_retained_sources(
        {
            "valid": True,
            "format": doc.format,
            "revision": doc.revision,
            "hash": codec.digest(doc),
            "records": len(doc.records),
            "files_verified": root is not None,
            "record_hashes": {
                id_: codec.record_hash(r) for id_, r in sorted(doc.records.items())
            },
        },
        doc,
        root,
    )


def workflow(path, root=None):
    from . import lifecycle

    doc = load_document(path)
    graph.validate(doc, root)
    if doc.format != 2:
        raise PixlError(
            "lifecycle_format",
            "workflow requires PX2; PX1 state retains its original rules",
        )
    report = lifecycle.report(doc)
    if root is not None:
        from .plar import selection_bindings
        from .plar_workflow import current_bindings

        for task in report["tasks"]:
            task["selection_bindings"] = selection_bindings(doc, task["id"], root, Path(path).resolve().parent)
            try:
                current_bindings(doc, task["id"], root, Path(path).resolve().parent)
            except PixlError as error:
                task["blockers"].append(str(error))
                if task["id"] in report["ready"]:
                    report["ready"].remove(task["id"])
    return _with_retained_sources(
        dict(
            report,
            format=2,
            revision=doc.revision,
            hash=codec.digest(doc),
            files_verified=root is not None,
        ),
        doc,
        root,
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
    doc = load_document(path)
    return _with_retained_sources(jobs.report(doc, root, Path(path).resolve().parent), doc, root)


def family_report(path, root, output_id=None):
    """Verify retained family files and describe the current saved selection."""
    from . import delivery

    doc = load_document(path)
    return _with_retained_sources(delivery.report(doc, root, output_id), doc, root)


def inspection_report(path, root, packet_id=None):
    """Verify retained inspection data and report original conditions and reviews."""
    from . import inspection

    doc = load_document(path)
    return _with_retained_sources(inspection.report(doc, root, packet_id), doc, root)


def call(name, args, root):
    if "result_path" in args:
        if name not in RESULT_EXPORT_TOOLS:
            raise PixlError("result_path", "this operation does not support result export")
        relative = args["result_path"]
        result_destination(root, relative)
        value = call(name, {key: value for key, value in args.items() if key != "result_path"}, root)
        return save_result(value, root, relative)
    try:
        return describe_result(name, _call(name, args, root))
    except PixlError as error:
        described = operation_error(name, error)
        if described is error:
            raise
        raise described from error


def _call(name, args, root):
    root = Path(root).resolve()

    def path(key):
        return graph.confined(root, args[key])

    if name == "pixl_validate":
        return inspect_document(path("path"), root)
    if name in ("pixl_context", "pixl_ready", "pixl_impact"):
        if name == "pixl_context":
            view = args.get("view", "complete")
            if view not in ("complete", "authoring"):
                raise PixlError("context_view", view)
            if view == "authoring":
                from .authoring_context import report

                if args.get("budget") is not None:
                    raise PixlError("context_budget", "budget applies only to complete wire context")
                return report(path("path"), args["focus"], root, args.get("plar_path"), args.get("asset_id"))
            if args.get("plar_path") is not None or args.get("asset_id") is not None:
                raise PixlError("context_view", "selection arguments require view=authoring")
        doc = load_document(path("path"))
        graph.validate(doc, root)
        if name == "pixl_ready":
            return {"ready": workflow(path("path"), root)["ready"] if doc.format == 2 else graph.ready(doc), "hash": codec.digest(doc)}
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
    if name == "pixl_task_complete":
        from .completion import complete

        return complete(
            path("store"), args["expect"], args["task_id"], args["candidates"], root
        )
    if name == "pixl_workflow":
        return workflow(path("path"), root)
    if name == "pixl_review_context":
        from . import candidate_review

        return candidate_review.context(load_document(path("path")), root, args["candidate_id"])
    if name == "pixl_candidate_review":
        from . import candidate_review

        return candidate_review.submit(path("store"), args["expect"], args["candidate_id"], args["review_id"], args["observation"], root)
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
    if name == "pixl_production_plan":
        from . import production_plan

        return production_plan.author(path("store"), args["expect"], args["plan"], root)
    if name == "pixl_stage_prepare":
        from . import production_plan

        return production_plan.prepare(path("store"), args["expect"], args["plan"], args["stage"], args["job"], args["packet"], root)
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
    if name == "pixl_retain_library":
        from .retention import retain

        return retain(
            path("store"),
            args["expect"],
            args["library"],
            root,
            args.get("from_library"),
        )
    if name == "pixl_plar_handoff":
        from .handoff import save

        return save(root, args["asset_id"], args["requirements_hash"], args["expect"], args["details"], args.get("path", "plar.txt"))
    if name == "pixl_request_review":
        from .request_review import report

        return report(root, args["packet"], args.get("asset_id"), args.get("path", "plar.txt"), args.get("plan"), args.get("job"), args.get("comparison"), args.get("view", "complete"), args.get("against_plan"))
    if name == "pixl_plar_prepare":
        from . import plar_prepare

        return plar_prepare.prepare(
            root,
            args["asset_id"],
            args["requirements_hash"],
            args["packet"],
            args["connection"],
            args.get("path", "plar.txt"),
            args.get("store"),
            args.get("revise", False),
            args.get("expect"),
        )
    if name in ("pixl_plar_read", "pixl_plar_save"):
        from . import plar

        if name == "pixl_plar_read":
            return plar.read(
                root,
                args.get("path", "plar.txt"),
                args.get("asset_id"),
                args.get("since"),
            )
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
        from .retention import resolve

        original = (
            graph.confined(resource_root(), args["path"])
            if scope == "library"
            else path("path")
        )
        source_path = (
            original
            if scope == "library"
            else resolve(root, args["path"], args["expect"])
        )
        result = source_slice(
            source_path,
            args["expect"],
            args["start"],
            args["end"],
            args.get("budget", 16384),
        )
        if source_path != original:
            result.update(
                retained_revision=True, uri=args["path"], resolved_path=str(source_path)
            )
        return result
    if name == "pixl_asset_check":
        return assets.inspect(
            path("path"),
            args.get("width"),
            args.get("height"),
            args.get("palette"),
            args.get("alpha", "binary"),
            args.get("regions"),
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
