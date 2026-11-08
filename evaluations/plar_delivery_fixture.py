"""Resume an existing controlled request through actual fixture retrieval only."""

import argparse
import base64
import json
import sys
import threading
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from PIL import Image

try:
    from evaluations.pixellab_mcp_fixture import Provider
    from evaluations.plar_request_fixture import SCHEMAS as REQUEST_SCHEMAS
except ModuleNotFoundError:
    from pixellab_mcp_fixture import Provider  # type: ignore[import-not-found,no-redef]
    from plar_request_fixture import (  # type: ignore[import-not-found,no-redef]
        SCHEMAS as REQUEST_SCHEMAS,
    )

SCHEMAS = {
    **REQUEST_SCHEMAS,
    "get_image": {
        "type": "object",
        "properties": {
            "job_id": {"type": "string"},
            "index": {"type": ["integer", "null"]},
        },
        "required": ["job_id"],
        "additionalProperties": False,
    },
}
DESCRIPTIONS = {
    "list_jobs": "Observe the original controlled requests. No upstream service.",
    "get_image": "Retrieve the existing controlled image job. Returns actual fixture PNG inline and a loopback download URL, preserving the original job ID. No new generation or upstream service.",
    "create_image_pro_flash": "Retained schema for the originating request; this continuation supplies only retrieval of existing work, so new submissions are rejected.",
}


class DeliveryProvider(Provider):
    def __init__(self, folder):
        super().__init__(
            folder, folder / "provider-result.png", folder / "provider-result.png"
        )

    def _image(self, ident):
        job = next((j for j in self.state["jobs"] if j["job_id"] == ident), None)
        if not job or job["status"] != "completed":
            raise ValueError("Result is unavailable for this retained job")
        data = self.positive.read_bytes()
        if sha256(data).hexdigest() != job["result_sha256"]:
            raise ValueError("Retained fixture result changed")
        return data

    def call(self, name, arguments):
        with self.synchronized():
            Draft202012Validator(SCHEMAS[name]).validate(arguments)
            self.log({"tool": name, "arguments": arguments})
            if name == "create_image_pro_flash":
                raise ValueError(
                    "Resume the existing generation; this stage does not authorize another request"
                )
            if name == "list_jobs":
                return {"jobs": self.state["jobs"], "provider_simulated": True}, None
            job = next(
                (j for j in self.state["jobs"] if j["job_id"] == arguments["job_id"]),
                None,
            )
            if not job or job["status"] == "failed":
                raise ValueError("No result for this job")
            if arguments.get("index") not in (None, 0):
                raise ValueError("This retained result has only index 0")
            data = self.positive.read_bytes()
            self.valid_png(data)
            digest = sha256(data).hexdigest()
            if job.get("result_sha256", digest) != digest:
                raise ValueError("Retained fixture result changed")
            job.update(status="completed", result_sha256=digest)
            self.save()
            with Image.open(self.positive) as image:
                width, height = image.size
            return {
                "job_id": job["job_id"],
                "status": "completed",
                "provider_simulated": True,
                "images": [
                    {
                        "index": 0,
                        "width": width,
                        "height": height,
                        "format": "png",
                        "sha256": digest,
                        "download_url": self.base_url + "/" + job["job_id"] + ".png",
                    }
                ],
            }, data


def handle(provider, request):
    if "id" not in request:
        return None
    method = request.get("method")
    if method == "initialize":
        result = {
            "protocolVersion": request.get("params", {}).get(
                "protocolVersion", "2024-11-05"
            ),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "controlled-pixellab-retrieval", "version": "1"},
        }
    elif method == "tools/list":
        result = {
            "tools": [
                {"name": n, "description": DESCRIPTIONS[n], "inputSchema": s}
                for n, s in SCHEMAS.items()
            ]
        }
    elif method == "tools/call":
        try:
            params = request["params"]
            value, picture = provider.call(params["name"], params.get("arguments", {}))
            content = [{"type": "text", "text": json.dumps(value)}]
            if picture:
                content.append(
                    {
                        "type": "image",
                        "mimeType": "image/png",
                        "data": base64.b64encode(picture).decode(),
                    }
                )
            result = {"content": content, "structuredContent": value, "isError": False}
        except (ValueError, KeyError, OSError, ValidationError) as error:
            result = {
                "content": [{"type": "text", "text": str(error)}],
                "isError": True,
            }
    else:
        result = {}
    return {"jsonrpc": "2.0", "id": request["id"], "result": result}


def serve(folder):
    provider = DeliveryProvider(folder)

    class Download(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                if not self.path.endswith(".png") or self.path.count("/") != 1:
                    raise ValueError("Unknown download")
                data = provider.image(self.path[1:-4])
            except ValueError:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            provider.log({"download": self.path, "sha256": sha256(data).hexdigest()})

        def log_message(self, format, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Download)
    provider.base_url = f"http://127.0.0.1:{server.server_address[1]}"
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        for line in sys.stdin:
            response = handle(provider, json.loads(line))
            if response is not None:
                print(json.dumps(response), flush=True)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=Path, required=True)
    serve(parser.parse_args().folder)
