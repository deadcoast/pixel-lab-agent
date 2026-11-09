"""Small synchronous MCP stdio server for local PIXL operations only."""

import json
import sys

from jsonschema import Draft202012Validator, ValidationError

from .codec import PixlError
from .service import call, parse_json


def schema(properties, required=()):
    return {
        "type": "object",
        "properties": properties,
        "required": list(required),
        "additionalProperties": False,
    }


STR = {"type": "string", "minLength": 1}
INT = {"type": "integer", "minimum": 1}
OBJ = {"type": "object"}
TOOLS = [
    (
        "pixl_production_plan",
        "Author connected sample/production stages and collective delivery from reviewed JSON using existing contracts, baseline and choices. Recover PLAR links on identical retries. No execution or acceptance.",
        schema({"store": STR, "expect": STR, "plan": OBJ}, ["store", "expect", "plan"]),
    ),
    (
        "pixl_stage_prepare",
        "Bind exact reviewed accepted upstream candidates to a planned stage and prepare its durable provider request. Identical retries recover saved intent; no dispatch or acceptance.",
        schema({"store": STR, "expect": STR, "plan": STR, "stage": STR, "job": STR, "packet": OBJ}, ["store", "expect", "plan", "stage", "job", "packet"]),
    ),
    (
        "pixl_plar_handoff",
        "Save an exact selected-production continuation with agent-authored details; returns immutable path/hash. Keep caller_actions and future_work in details; derived resume/next are preserved unchanged. No acceptance or provider action.",
        schema({"asset_id": STR, "requirements_hash": STR, "expect": STR, "details": OBJ, "path": STR}, ["asset_id", "requirements_hash", "expect", "details"]),
    ),
    (
        "pixl_request_review",
        "Read exact candidate or connected-plan criteria and source excerpts. For authoring, pass returned request_review arguments (packet is state.px, plan and optional job); includes every member/collective criterion. Optional comparison checks identity/coverage, never meaning or acceptance. Read only.",
        schema({"packet": STR, "asset_id": STR, "path": STR, "plan": STR, "job": STR, "comparison": STR}, ["packet"]),
    ),
    (
        "pixl_retain_library",
        "Retain exact library S-source bytes for a project before a kit update, or recover them from its original kit. Keeps state and receipts unchanged; no new proof or provider action.",
        schema(
            {"store": STR, "expect": STR, "library": STR, "from_library": STR},
            ["store", "expect", "library"],
        ),
    ),
    (
        "pixl_plar_read",
        "Read project asset requirements, source drift and update impact; select asset_id for current production links, pending jobs and next actions.",
        schema({"path": STR, "asset_id": STR, "since": STR}),
    ),
    (
        "pixl_plar_prepare",
        "Prepare a selected asset from reviewed request/criteria and discovered provider schema. Retains the candidate plan and durable job, links the allocation, and resumes identical calls. Explicit revise plus expect appends a reviewed generation after pending work is resolved. No dispatch or art acceptance.",
        schema({"path": STR, "asset_id": STR, "requirements_hash": STR, "packet": STR,
                "connection": {"anyOf": [OBJ, STR]}, "store": STR,
                "revise": {"type": "boolean"}, "expect": STR},
               ["asset_id", "requirements_hash", "packet", "connection"]),
    ),
    (
        "pixl_plar_save",
        "Save a PLAR requirements document with expected file hash (new to create); retain previous bytes and bind new source paths. No provider call.",
        schema({"path": STR, "document": OBJ, "expect": STR}, ["document", "expect"]),
    ),
    (
        "pixl_validate",
        "Validate PIXL state, record bindings and local file hashes.",
        schema({"path": STR}, ["path"]),
    ),
    (
        "pixl_context",
        "Retrieve complete task context; fail rather than truncate required byte budget.",
        schema({"path": STR, "focus": STR, "budget": INT}, ["path", "focus"]),
    ),
    (
        "pixl_ready",
        "List open tasks whose prerequisites are completed and whose tagged PLAR selections remain current.",
        schema({"path": STR}, ["path"]),
    ),
    (
        "pixl_impact",
        "Find records transitively depending on a changed ID.",
        schema({"path": STR, "id": STR}, ["path", "id"]),
    ),
    (
        "pixl_init",
        "Initialize a local PIXL store with explicitly unconfirmed intake defaults.",
        schema({"store": STR, "name": STR}, ["store"]),
    ),
    (
        "pixl_intake",
        "Initialize a PX2 project with a brief and no invented style or production decisions.",
        schema({"store": STR, "name": STR, "brief": STR}, ["store"]),
    ),
    (
        "pixl_task_complete",
        "Nominate explicit already-reviewed candidates and complete their PX2 task. Requires every saved criterion passed and provider attempts terminal; creates no acceptance evidence or remote action.",
        schema(
            {
                "store": STR,
                "expect": STR,
                "task_id": STR,
                "candidates": {
                    "type": "array",
                    "items": STR,
                    "minItems": 1,
                    "uniqueItems": True,
                },
            },
            ["store", "expect", "task_id", "candidates"],
        ),
    ),
    (
        "pixl_workflow",
        "Inspect PX2 intake, planned outputs, candidate verdicts, blockers and next ready tasks. No acceptance or remote side effect.",
        schema({"path": STR}, ["path"]),
    ),
    (
        "pixl_inspection",
        "Verify retained inspection and reviews. With packet_id and view_ids, deliver selected PNG image blocks with exact payload dimensions and hashes for viewing. Read-only; no artistic or engine acceptance.",
        {
            **schema(
                {
                    "path": STR,
                    "packet_id": STR,
                    "view_ids": {
                        "type": "array",
                        "items": STR,
                        "minItems": 1,
                        "maxItems": 8,
                        "uniqueItems": True,
                    },
                },
                ["path"],
            ),
            "dependentRequired": {"view_ids": ["packet_id"]},
        },
    ),
    (
        "pixl_inspection_prepare",
        "Retain saved candidate/reference bytes, native and integer-nearest views, and measurements using the expected state hash. No verdict, nomination, task completion or remote action.",
        schema(
            {
                "store": STR,
                "expect": STR,
                "candidate_id": STR,
                "packet_id": STR,
                "options": OBJ,
            },
            ["store", "expect", "candidate_id", "packet_id", "options"],
        ),
    ),
    (
        "pixl_inspection_review",
        "Retain explicit caller viewing observations and criterion verdicts against a prepared packet using the expected hash. Does not establish actual host viewing, nominate the candidate, complete the task or execute an engine.",
        schema(
            {
                "store": STR,
                "expect": STR,
                "packet_id": STR,
                "review_id": STR,
                "observation": OBJ,
            },
            ["store", "expect", "packet_id", "review_id", "observation"],
        ),
    ),
    (
        "pixl_family",
        "Verify retained family files and report baseline, member selection, destination requirements, pending jobs and drift. No acceptance or remote action.",
        schema({"path": STR, "output": STR}, ["path"]),
    ),
    (
        "pixl_family_snapshot",
        "Copy selected local family files into a retained delivery candidate using the expected state hash. Does not nominate or accept it, change task state, or execute remotely.",
        schema(
            {"store": STR, "output_id": STR, "candidate_id": STR, "expect": STR},
            ["store", "output_id", "candidate_id", "expect"],
        ),
    ),
    (
        "pixl_job_prepare",
        "Save exact caller-discovered provider intent and authorization in the local project. Never executes remotely.",
        schema(
            {
                "store": STR,
                "expect": STR,
                "job_id": STR,
                "task_id": STR,
                "outputs": {
                    "type": "array",
                    "items": STR,
                    "minItems": 1,
                    "uniqueItems": True,
                },
                "provider": STR,
                "tool": STR,
                "arguments": OBJ,
                "schema": OBJ,
                "discovery": OBJ,
                "authorization": OBJ,
            },
            [
                "store",
                "expect",
                "job_id",
                "task_id",
                "outputs",
                "provider",
                "tool",
                "arguments",
                "schema",
                "discovery",
                "authorization",
            ],
        ),
    ),
    (
        "pixl_job_dispatch",
        "Save a one-time dispatch claim as unknown before returning the exact request for host execution. Never submits remotely; reconcile after any uncertain result.",
        schema(
            {"store": STR, "expect": STR, "job_id": STR}, ["store", "expect", "job_id"]
        ),
    ),
    (
        "pixl_job_observe",
        "Save caller-supplied provider observations and remote identity. Never polls or attests provider success.",
        schema(
            {
                "store": STR,
                "expect": STR,
                "job_id": STR,
                "event": {
                    "enum": ["submitted", "running", "succeeded", "failed", "unknown"]
                },
                "evidence": OBJ,
                "remote_id": STR,
            },
            ["store", "expect", "job_id", "event", "evidence"],
        ),
    ),
    (
        "pixl_job_import",
        "Snapshot an already downloaded project file and link an unaccepted candidate to a succeeded job output. Never downloads or creates acceptance evidence.",
        schema(
            {
                "store": STR,
                "expect": STR,
                "job_id": STR,
                "output_id": STR,
                "candidate_id": STR,
                "path": STR,
                "evidence": OBJ,
            },
            [
                "store",
                "expect",
                "job_id",
                "output_id",
                "candidate_id",
                "path",
                "evidence",
            ],
        ),
    ),
    (
        "pixl_jobs",
        "Verify saved job files and report full requests, history, drift, candidates and recovery actions. Does not grant dispatch or contact a provider.",
        schema({"path": STR}, ["path"]),
    ),
    (
        "pixl_commit",
        "Commit a candidate file or inline JSON document after expected-hash, revision and evidence validation.",
        dict(
            schema(
                {"store": STR, "candidate": STR, "document": OBJ, "expect": STR},
                ["store", "expect"],
            ),
            oneOf=[{"required": ["candidate"]}, {"required": ["document"]}],
        ),
    ),
    (
        "pixl_catalog",
        "Index local source sections without executing embedded content.",
        schema({"paths": {"type": "array", "items": STR}}),
    ),
    (
        "pixl_sources",
        "Discover and verify the installed knowledge corpus source identities. Not remote research.",
        schema({}),
    ),
    (
        "pixl_source",
        "Read exact hash-verified source lines within a byte budget, from the project or installed library.",
        schema(
            {
                "path": STR,
                "expect": STR,
                "start": INT,
                "end": INT,
                "budget": INT,
                "scope": {"enum": ["project", "library"]},
            },
            ["path", "expect", "start", "end"],
        ),
    ),
    (
        "pixl_asset_check",
        "Measure image dimensions, palette, alpha and components. Optional regions selects exact RGBA colors for measured component boxes; no artistic judgment.",
        schema(
            {
                "path": STR,
                "width": INT,
                "height": INT,
                "palette": {"type": "array", "items": STR},
                "alpha": {"enum": ["binary", "full"]},
                "regions": {
                    "type": "array",
                    "items": STR,
                    "minItems": 1,
                    "maxItems": 16,
                },
            },
            ["path"],
        ),
    ),
    (
        "pixl_encode",
        "Compile lossless host records into canonical PIXL wire syntax, deriving UTF-8 lengths.",
        schema({"document": OBJ}, ["document"]),
    ),
    (
        "pixl_knowledge",
        "Read the pixel-art method index or one source-grounded method.",
        schema({"method": STR}),
    ),
    (
        "pixl_capabilities",
        "Read dated PixelLab documentation inventory; not live tool discovery.",
        schema({"name": STR}),
    ),
    (
        "pixl_prepare",
        "Legacy stateless request validation. Does not save project intent or submit to PixelLab.",
        schema(
            {"tool": STR, "arguments": OBJ, "schema": OBJ, "authorization": OBJ},
            ["tool", "arguments", "schema"],
        ),
    ),
    (
        "pixl_job",
        "Legacy stateless journal update from supplied observations. Does not publish project state, poll or create remote jobs.",
        schema(
            {"job": OBJ, "event": STR, "remote_id": STR, "evidence": OBJ},
            ["job", "event"],
        ),
    ),
]


def dispatch(request, root):
    if (
        not isinstance(request, dict)
        or request.get("jsonrpc") != "2.0"
        or not isinstance(request.get("method"), str)
    ):
        return {
            "jsonrpc": "2.0",
            "id": request.get("id") if isinstance(request, dict) else None,
            "error": {"code": -32600, "message": "Invalid Request"},
        }
    if "id" not in request:
        return None
    id_, method, params = request["id"], request["method"], request.get("params", {})
    if (
        isinstance(id_, (bool, list, dict))
        or not isinstance(id_, (str, int, type(None)))
        or not isinstance(params, dict)
    ):
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32600, "message": "Invalid Request"},
        }
    if method == "initialize":
        supported = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")
        requested = params.get("protocolVersion")
        result = {
            "protocolVersion": requested if requested in supported else supported[0],
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "pixl-local", "version": "1.0.0"},
            "instructions": "All tools are local. PixelLab must be connected separately. Paths are relative to the configured project root.",
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {
            "tools": [
                {
                    "name": n,
                    "description": d,
                    "inputSchema": s,
                    "annotations": {
                        "readOnlyHint": n
                        not in (
                            "pixl_init",
                            "pixl_intake",
                            "pixl_commit",
                            "pixl_plar_save",
                            "pixl_plar_prepare",
                            "pixl_production_plan",
                            "pixl_stage_prepare",
                            "pixl_plar_handoff",
                            "pixl_job_prepare",
                            "pixl_job_dispatch",
                            "pixl_job_observe",
                            "pixl_job_import",
                            "pixl_family_snapshot",
                            "pixl_inspection_prepare",
                            "pixl_inspection_review",
                            "pixl_task_complete",
                        ),
                        "destructiveHint": False,
                        "openWorldHint": False,
                    },
                }
                for n, d, s in TOOLS
            ]
        }
    elif method == "tools/call":
        try:
            name, args = params.get("name"), params.get("arguments", {})
            found = next((s for n, _, s in TOOLS if n == name), None)
            if found is None:
                raise PixlError("unknown_tool", str(name))
            Draft202012Validator(found).validate(args)
            output = call(name, args, root)
            images = []
            if name == "pixl_inspection" and "view_ids" in args:
                from .inspection import image_payloads

                output["image_payloads"], images = image_payloads(
                    output, root, args["view_ids"]
                )
            result = {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(
                            output, ensure_ascii=False, separators=(",", ":")
                        ),
                    }
                ]
                + images,
                "structuredContent": output,
                "isError": False,
            }
        except ValidationError as error:
            result = {
                "content": [
                    {
                        "type": "text",
                        "text": f"arguments violate inputSchema ({error.validator})",
                    }
                ],
                "isError": True,
            }
        except (
            PixlError,
            OSError,
            ValueError,
            KeyError,
            TypeError,
            RecursionError,
        ) as error:
            result = {
                "content": [{"type": "text", "text": str(error)}],
                "isError": True,
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": id_,
            "error": {"code": -32601, "message": "Method not found"},
        }
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def serve(root):
    stream = sys.stdin.buffer
    while True:
        line = stream.readline(16 * 1024 * 1024 + 2)
        if not line:
            return
        if len(line) > 16 * 1024 * 1024:
            while line and not line.endswith(b"\n"):
                line = stream.readline(16 * 1024 * 1024 + 2)
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32600, "message": "Request exceeds 16 MiB"},
            }
        else:
            try:
                request = parse_json(line)
                response = dispatch(request, root)
            except (ValueError, RecursionError):
                response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                }
        if response is not None:
            data = (
                json.dumps(response, ensure_ascii=True, separators=(",", ":")).encode(
                    "utf-8"
                )
                + b"\n"
            )
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
