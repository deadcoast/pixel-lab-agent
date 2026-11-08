"""Request-only controlled MCP connection for selected-asset preparation trials.

Names and supported fields follow documented PixelLab controls. The connection
advertises its deliberately narrow schema; it produces no images or upstream I/O.
"""

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

try:
    from evaluations.pixellab_mcp_fixture import Provider
except ModuleNotFoundError:
    from pixellab_mcp_fixture import Provider  # type: ignore[import-not-found,no-redef]

SCHEMAS = {
    "create_image_pro_flash": {
        "type": "object",
        "properties": {
            "description": {"type": "string", "minLength": 1},
            "width": {
                "type": "integer",
                "minimum": 16,
                "maximum": 256,
                "multipleOf": 4,
            },
            "height": {
                "type": "integer",
                "minimum": 16,
                "maximum": 256,
                "multipleOf": 4,
            },
            "no_background": {"type": "boolean"},
            "seed": {"type": "integer", "minimum": 0},
        },
        "required": ["description"],
        "additionalProperties": False,
    },
    "list_jobs": {
        "type": "object",
        "properties": {"include_recent": {"type": "boolean"}},
        "additionalProperties": False,
    },
}
DESCRIPTIONS = {
    "create_image_pro_flash": "Controlled request-only fixture using documented PixelLab create_image_pro_flash fields. Queues one request; default canvas 64x64, no_background true. Return is a simulated acceptance, with no generated image or upstream provider. The assigned stage ends after retaining this job identity.",
    "list_jobs": "Read the existing controlled queued request; this fixture performs no generation.",
}


class RequestProvider(Provider):
    def __init__(self, folder):
        super().__init__(folder, folder / "unused-negative", folder / "unused-positive")

    def request(self, name, arguments):
        with self.synchronized():
            self.log({"tool": name, "arguments": arguments})
            Draft202012Validator(SCHEMAS[name]).validate(arguments)
            if name == "list_jobs":
                return {"jobs": self.state["jobs"], "provider_simulated": True}
            if self.state["jobs"]:
                raise ValueError(
                    "This stage permits one request; recover the existing job"
                )
            job = {
                "job_id": "controlled-create-0001",
                "status": "queued",
                "arguments": arguments,
                "tool": name,
                "provider_simulated": True,
            }
            self.state["jobs"].append(job)
            self.save()
            self.log({"accepted": job["job_id"]})
            return job


def serve(folder):
    provider = RequestProvider(folder)
    for line in sys.stdin:
        request = json.loads(line)
        if "id" not in request:
            continue
        method = request["method"]
        if method == "initialize":
            result = {
                "protocolVersion": request.get("params", {}).get(
                    "protocolVersion", "2024-11-05"
                ),
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "controlled-pixellab-request", "version": "1"},
            }
        elif method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": name,
                        "description": DESCRIPTIONS[name],
                        "inputSchema": schema,
                    }
                    for name, schema in SCHEMAS.items()
                ]
            }
        elif method == "tools/call":
            params = request["params"]
            try:
                value = provider.request(params["name"], params.get("arguments", {}))
                result = {
                    "content": [{"type": "text", "text": json.dumps(value)}],
                    "structuredContent": value,
                    "isError": False,
                }
            except (ValueError, KeyError, ValidationError) as error:
                result = {
                    "content": [{"type": "text", "text": str(error)}],
                    "isError": True,
                }
        else:
            result = {}
        print(
            json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}),
            flush=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=Path, required=True)
    serve(parser.parse_args().folder)
