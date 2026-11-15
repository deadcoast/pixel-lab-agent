"""Separate opt-in PixelLab HTTP MCP bridge, not the local state server."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, ValidationError

from . import service
from .codec import PixlError
from .mcp import OBJ, STR, schema
from .pixellab_http import HTTPS, Workflow, contract

COMMON = {"store": STR, "expect": STR, "job_id": STR}
TOOLS = [
    (
        "pixellab_contract",
        "Read the retained official HTTP image schema and adapter boundary.",
        schema({}),
    ),
    (
        "pixellab_prepare_image",
        "Save a schema-checked image request against a planned output; no HTTP call.",
        schema(
            {
                **COMMON,
                "task_id": STR,
                "output_id": STR,
                "arguments": OBJ,
                "authorization": OBJ,
            },
            [*COMMON, "task_id", "output_id", "arguments", "authorization"],
        ),
    ),
    (
        "pixellab_submit",
        "Claim the prepared job and make exactly one official image submission. Never retries an unknown job.",
        schema(COMMON, list(COMMON)),
    ),
    (
        "pixellab_poll",
        "Fetch the saved remote job ID once and retain the actual result; never submits.",
        schema(COMMON, list(COMMON)),
    ),
    (
        "pixellab_import_image",
        "Decode the completed response PNG into an unaccepted project candidate; no remote call or visual verdict.",
        schema(
            {**COMMON, "output_id": STR, "candidate_id": STR},
            [*COMMON, "output_id", "candidate_id"],
        ),
    ),
]


def call(workflow: Workflow, name: str, arguments: dict) -> dict:
    if name == "pixellab_contract":
        from .pixellab_http import CREATE_PATH, OPERATION, PROVIDER
        from .pixellab_http import schema as official_schema

        source = contract()
        return {
            "provider": PROVIDER,
            "operation": OPERATION,
            "method": "POST",
            "path": CREATE_PATH,
            "inputSchema": official_schema("CreateImagePixfluxRequest"),
            "source": source["source"],
            "retrieved_at": source["retrieved_at"],
            "source_sha256": source["source_sha256"],
            "simulated": workflow.transport.simulated,
            "poll_interval_seconds": 5 if not workflow.transport.simulated else 0,
            "boundary": "HTTP adapter; local PIXL tools remain local. Import does not accept art.",
        }
    args = dict(arguments)
    args["folder"] = args.pop("store")
    args["expected"] = args.pop("expect")
    methods: dict[str, Callable[..., dict]] = {
        "pixellab_prepare_image": workflow.prepare,
        "pixellab_submit": workflow.submit,
        "pixellab_poll": workflow.poll,
        "pixellab_import_image": workflow.import_image,
    }
    return methods[name](**args)


def dispatch(request, workflow: Workflow):
    if not isinstance(request, dict) or request.get("jsonrpc") != "2.0":
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32600, "message": "Invalid request"},
        }
    if "id" not in request:
        return None
    identifier = request["id"]
    method, params = request.get("method"), request.get("params", {})
    if not isinstance(params, dict):
        return {
            "jsonrpc": "2.0",
            "id": identifier,
            "error": {"code": -32602, "message": "Invalid parameters"},
        }
    result: dict[str, Any]
    if method == "initialize":
        result = {
            "protocolVersion": "2025-11-25",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "pixellab-http", "version": "1.0.0"},
            "instructions": "MOCK TRANSPORT: no provider calls or spend."
            if workflow.transport.simulated
            else "Official PixelLab HTTP adapter. Submission can consume credits. Honor established authorization.",
        }
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {
            "tools": [
                {
                    "name": n,
                    "description": d
                    + (
                        " TEST: transport is mocked."
                        if workflow.transport.simulated
                        else ""
                    ),
                    "inputSchema": s,
                }
                for n, d, s in TOOLS
            ]
        }
    elif method == "tools/call":
        try:
            name, args = params.get("name"), params.get("arguments", {})
            if not isinstance(name, str):
                raise PixlError("unknown_tool", "A tool name is required")
            tool_schema = next((s for n, _, s in TOOLS if n == name), None)
            if tool_schema is None:
                raise PixlError("unknown_tool", "Unknown PixelLab adapter operation")
            Draft202012Validator(tool_schema).validate(args)
            output = call(workflow, name, args)
            result = {
                "content": [{"type": "text", "text": json.dumps(output)}],
                "structuredContent": output,
                "isError": False,
            }
        except ValidationError as error:
            result = {
                "content": [
                    {
                        "type": "text",
                        "text": f"Invalid tool arguments ({error.validator})",
                    }
                ],
                "isError": True,
            }
        except (PixlError, OSError, ValueError, KeyError, TypeError) as error:
            result = {
                "content": [{"type": "text", "text": str(error)}],
                "isError": True,
            }
    else:
        return {
            "jsonrpc": "2.0",
            "id": identifier,
            "error": {"code": -32601, "message": "Unknown method"},
        }
    return {"jsonrpc": "2.0", "id": identifier, "result": result}


def serve(workflow: Workflow) -> None:
    for raw in sys.stdin.buffer:
        try:
            if len(raw) > 16 * 1024 * 1024:
                raise ValueError("request too large")
            response = dispatch(service.parse_json(raw), workflow)
        except (ValueError, PixlError):
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Invalid JSON"},
            }
        if response is not None:
            print(json.dumps(response), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    serve(Workflow(args.root, HTTPS(os.environ.get("PIXELLAB_API_KEY", ""))))


if __name__ == "__main__":
    main()
