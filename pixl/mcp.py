"""Small synchronous MCP stdio server for local PIXL operations only."""

import json
import sys

from jsonschema import Draft202012Validator, ValidationError

from .codec import PixlError
from .service import call


def schema(properties, required=()):
    return {"type": "object", "properties": properties, "required": list(required), "additionalProperties": False}


STR = {"type": "string", "minLength": 1}
INT = {"type": "integer", "minimum": 1}
OBJ = {"type": "object"}
TOOLS = [
    ("pixl_validate", "Validate PIXL state, record bindings and local file hashes.", schema({"path": STR}, ["path"])),
    ("pixl_context", "Retrieve complete task context; fail rather than truncate required byte budget.", schema({"path": STR, "focus": STR, "budget": INT}, ["path", "focus"])),
    ("pixl_ready", "List open tasks whose prerequisites are completed.", schema({"path": STR}, ["path"])),
    ("pixl_impact", "Find records transitively depending on a changed ID.", schema({"path": STR, "id": STR}, ["path", "id"])),
    ("pixl_init", "Initialize a local PIXL store with explicitly unconfirmed intake defaults.", schema({"store": STR, "name": STR}, ["store"])),
    ("pixl_commit", "Publish a local candidate after expected-hash, revision and evidence validation.", schema({"store": STR, "candidate": STR, "expect": STR}, ["store", "candidate", "expect"])),
    ("pixl_catalog", "Index local source sections without executing embedded content.", schema({"paths": {"type": "array", "items": STR}})),
    ("pixl_source", "Read exact hash-verified source lines within a byte budget.", schema({"path": STR, "expect": STR, "start": INT, "end": INT, "budget": INT}, ["path", "expect", "start", "end"])),
    ("pixl_asset_check", "Measure image dimensions, palette, alpha and components. Does not judge artistic quality.", schema({"path": STR, "width": INT, "height": INT, "palette": {"type": "array", "items": STR}, "alpha": {"enum": ["binary", "full"]}}, ["path"])),
    ("pixl_encode", "Compile lossless host records into canonical PIXL wire syntax, deriving UTF-8 lengths.", schema({"document": OBJ}, ["document"])),
    ("pixl_knowledge", "Read the pixel-art method index or one source-grounded method.", schema({"method": STR})),
    ("pixl_capabilities", "Read dated PixelLab documentation inventory; not live tool discovery.", schema({"name": STR})),
    ("pixl_prepare", "Validate supplied provider schema and prepare local intent. Never submits to PixelLab.", schema({"tool": STR, "arguments": OBJ, "schema": OBJ, "authorization": OBJ}, ["tool", "arguments", "schema"])),
    ("pixl_job", "Derive local journal state from supplied observations. Never polls or creates remote jobs.", schema({"job": OBJ, "event": STR, "remote_id": STR, "evidence": OBJ}, ["job", "event"]))
]


def dispatch(request, root):
    if not isinstance(request, dict) or request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
        return {"jsonrpc": "2.0", "id": request.get("id") if isinstance(request, dict) else None,
                "error": {"code": -32600, "message": "Invalid Request"}}
    if "id" not in request:
        return None
    id_, method, params = request["id"], request["method"], request.get("params", {})
    if isinstance(id_, (bool, list, dict)) or not isinstance(id_, (str, int, type(None))) or not isinstance(params, dict):
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}
    if method == "initialize":
        supported = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")
        requested = params.get("protocolVersion")
        result = {"protocolVersion": requested if requested in supported else supported[0],
                  "capabilities": {"tools": {"listChanged": False}},
                  "serverInfo": {"name": "pixl-local", "version": "1.0.0"},
                  "instructions": "All tools are local. PixelLab must be connected separately. Paths are relative to the configured project root."}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [{"name": n, "description": d, "inputSchema": s,
                             "annotations": {"readOnlyHint": n not in ("pixl_init", "pixl_commit"),
                                             "destructiveHint": False, "openWorldHint": False}}
                            for n, d, s in TOOLS]}
    elif method == "tools/call":
        try:
            name, args = params.get("name"), params.get("arguments", {})
            found = next((s for n, _, s in TOOLS if n == name), None)
            if found is None:
                raise PixlError("unknown_tool", str(name))
            Draft202012Validator(found).validate(args)
            output = call(name, args, root)
            result = {"content": [{"type": "text", "text": json.dumps(output, ensure_ascii=False, separators=(",", ":"))}],
                      "structuredContent": output, "isError": False}
        except ValidationError as error:
            result = {"content": [{"type": "text", "text": "arguments: " + error.message}], "isError": True}
        except (PixlError, OSError, ValueError, KeyError, TypeError, RecursionError) as error:
            result = {"content": [{"type": "text", "text": str(error)}], "isError": True}
    else:
        return {"jsonrpc": "2.0", "id": id_, "error": {"code": -32601, "message": "Method not found"}}
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
            response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Request exceeds 16 MiB"}}
        else:
            try:
                request = json.loads(line, parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
                response = dispatch(request, root)
            except (ValueError, UnicodeError, RecursionError):
                response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        if response is not None:
            data = json.dumps(response, ensure_ascii=True, separators=(",", ":")).encode("utf-8") + b"\n"
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()
