"""Controlled PixelLab MCP edit surface with loopback-only fixture downloads.

The advertised argument shapes follow the retained official tool declarations.
Responses, job IDs and images are evaluator fixtures, never upstream observations.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import threading
from contextlib import contextmanager
from datetime import UTC, datetime
from email import policy
from email.parser import BytesParser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError
from PIL import Image

NULLSTR = {"type": ["string", "null"]}
REFERENCE = {"type": ["object", "null"], "additionalProperties": False, "properties":
             {k: NULLSTR for k in ("base64", "url", "source_image_id", "usage_description")}}
SCHEMAS = {
    "get_upload_url": {"type": "object", "additionalProperties": False, "properties": {}},
    "edit_image_pro_flash": {"type": "object", "additionalProperties": False, "properties": {
        "description": NULLSTR, "image_base64": NULLSTR, "image_url": NULLSTR,
        "method": {"enum": ["text", "reference"]}, "no_background": {"type": ["boolean", "null"]},
        "project_id": NULLSTR, "reference_image": REFERENCE, "seed": {"type": "integer"},
        "source_image_id": NULLSTR, "use_color_palette_correction": {"type": "boolean"}}},
    "get_image": {"type": "object", "additionalProperties": False,
        "properties": {"job_id": {"type": "string"}, "index": {"type": ["integer", "null"]}},
        "required": ["job_id"]},
    "list_jobs": {"type": "object", "additionalProperties": False,
        "properties": {"include_recent": {"type": "boolean"}}},
}
DESCRIPTIONS = {
    "get_upload_url": "Controlled get_upload_url. Upload a local file with the returned multipart curl instructions, then pass the returned upload:<id> in image_url or reference_image.url. Avoids transcribing base64. Loopback fixture only; no upstream provider.",
    "edit_image_pro_flash": "Controlled test implementation of PixelLab edit_image_pro_flash. Edit the supplied image, preserving native canvas; method=reference uses reference_image. Queues one fixture job; get_image retrieves it. Use get_upload_url for local files and pass returned upload handles as image_url/reference_image.url; actual PNG base64 is also supported. This connection has no upstream provider.",
    "get_image": "Controlled get_image: observe a previously queued job; completed results include a loopback download URL and inline image. No upstream provider.",
    "list_jobs": "Controlled list_jobs: discover active jobs, or recently completed ones with include_recent=true. Use observed matching identity to reconcile an uncertain submission.",
}


class Provider:
    def __init__(self, folder: Path, negative: Path, positive: Path):
        self.folder = folder
        self.negative, self.positive = negative, positive
        self.state_path = folder / "provider-state.json"
        self.log_path = folder / "provider-calls.jsonl"
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {"jobs": []}
        self.base_url = ""
        self.lock = threading.RLock()

    @contextmanager
    def synchronized(self):
        # Parent and specialist may launch separate MCP processes against this service.
        with self.lock, (self.folder / "provider.lock").open("a+b") as lock:
            if lock.seek(0, 2) == 0:
                lock.write(b"0")
                lock.flush()
            lock.seek(0)
            if sys.platform == "win32":
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {"jobs": []}
                yield
            finally:
                lock.seek(0)
                if sys.platform == "win32":
                    msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(lock.fileno(), fcntl.LOCK_UN)

    def log(self, event: dict) -> None:
        with self.lock, self.log_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"at": datetime.now(UTC).isoformat(), "simulated": True, **event}) + "\n")

    def save(self) -> None:
        temporary = self.state_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.state, indent=2) + "\n", encoding="utf-8")
        temporary.replace(self.state_path)

    def image(self, ident: str) -> bytes:
        with self.synchronized():
            return self._image(ident)

    def _image(self, ident: str) -> bytes:
        job = next((x for x in self.state["jobs"] if x["job_id"] == ident), None)
        if not job or job["status"] != "completed":
            raise ValueError("Result is unavailable")
        return (self.negative if job["ordinal"] == 1 else self.positive).read_bytes()

    @staticmethod
    def valid_png(data: bytes) -> None:
        try:
            with Image.open(BytesIO(data)) as image:
                if image.format != "PNG":
                    raise ValueError("Expected PNG")
                if image.width * image.height > 16_777_216:
                    raise ValueError("Fixture image exceeds 16M pixels")
                image.verify()
            with Image.open(BytesIO(data)) as image:
                image.load()
        except (OSError, ValueError, SyntaxError, Image.DecompressionBombError) as error:
            raise ValueError("Image must be a fully decodable PNG") from error

    def upload(self, data: bytes) -> dict:
        with self.synchronized():
            return self._upload(data)

    def _upload(self, data: bytes) -> dict:
        self.valid_png(data)
        digest = hashlib.sha256(data).hexdigest()
        ref = "upload:controlled-" + digest
        folder = self.folder / "uploads"
        folder.mkdir(exist_ok=True)
        path = folder / (digest + ".png")
        path.write_bytes(data)
        item = {"ref": ref, "sha256": digest, "bytes": len(data), "path": path.relative_to(self.folder).as_posix()}
        with self.lock:
            self.state.setdefault("uploads", {})[ref] = item
            self.save()
        self.log({"upload": item})
        return {"ref": ref}

    def input_image(self, encoded: str | None, ref: str | None) -> bytes:
        if bool(encoded) == bool(ref):
            raise ValueError("Supply exactly one base64 image or uploaded image URL")
        if ref:
            item = self.state.get("uploads", {}).get(ref)
            if not item:
                raise ValueError("Unknown upload handle; use get_upload_url and upload the file")
            data = (self.folder / item["path"]).read_bytes()
            if hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise ValueError("Uploaded image bytes changed")
        else:
            data = base64.b64decode(encoded or "", validate=True)
        self.valid_png(data)
        return data

    def call(self, name: str, args: dict) -> tuple[dict, bool, bytes | None]:
        with self.synchronized():
            return self._call(name, args)

    def _call(self, name: str, args: dict) -> tuple[dict, bool, bytes | None]:
        Draft202012Validator(SCHEMAS[name]).validate(args)
        self.log({"tool": name, "arguments": args})
        if name == "get_upload_url":
            return {"upload_url": self.base_url + "/upload", "provider_simulated": True}, False, None
        if name == "edit_image_pro_flash":
            if len(self.state["jobs"]) >= 2 or any(j["status"] != "completed" for j in self.state["jobs"]):
                raise ValueError("Pending request or two-attempt test limit; reconcile existing jobs")
            data = self.input_image(args.get("image_base64"), args.get("image_url"))
            reference = args.get("reference_image") or {}
            if args.get("method", "text") == "reference":
                self.input_image(reference.get("base64"), reference.get("url"))
            elif not args.get("description"):
                raise ValueError("Text edit requires description")
            ordinal = len(self.state["jobs"]) + 1
            job = {"job_id": f"controlled-edit-{ordinal:04}", "ordinal": ordinal,
                   "status": "processing", "tool": name, "description": args.get("description"),
                   "source_sha256": hashlib.sha256(data).hexdigest(),
                   "created_at": datetime.now(UTC).isoformat()}
            self.state["jobs"].append(job)
            self.save()
            self.log({"accepted": job})
            if ordinal == 1:
                return {"error": "Transport response lost after sending; submission outcome is unknown."}, True, None
            return {"job_id": job["job_id"], "status": "processing", "provider_simulated": True}, False, None
        if name == "list_jobs":
            jobs = [j for j in self.state["jobs"] if args.get("include_recent") or j["status"] != "completed"]
            return {"jobs": jobs, "provider_simulated": True}, False, None
        found_job = next((j for j in self.state["jobs"] if j["job_id"] == args["job_id"]), None)
        if found_job is None:
            raise ValueError("Unknown job ID")
        found_job["status"] = "completed"
        self.save()
        data = self._image(found_job["job_id"])
        return {"job_id": found_job["job_id"], "status": "completed", "provider_simulated": True,
                "images": [{"index": 0, "width": 32, "height": 32, "format": "png",
                            "download_url": self.base_url + "/" + found_job["job_id"] + ".png"}]}, False, data


def handle(provider: Provider, request: dict) -> dict | None:
    if "id" not in request:
        return None
    method = request.get("method")
    if method == "initialize":
        result = {"protocolVersion": request.get("params", {}).get("protocolVersion", "2024-11-05"),
                  "capabilities": {"tools": {}}, "serverInfo": {"name": "controlled-pixellab", "version": "1"}}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [{"name": n, "description": DESCRIPTIONS[n], "inputSchema": s} for n, s in SCHEMAS.items()]}
    elif method == "tools/call":
        params = request.get("params", {})
        try:
            data, error, picture = provider.call(params["name"], params.get("arguments", {}))
            content = [{"type": "text", "text": json.dumps(data)}]
            if params["name"] == "get_upload_url":
                content = [{"type": "text", "text":
                    'Controlled upload URL: ' + data["upload_url"] + '\nSend a file with curl -sS -F "file=@sprite.png" "' + data["upload_url"] +
                    '". The JSON reply contains ref (upload:<id>); use it in image URL parameters. No upstream service.'}]

            if picture:
                content.append({"type": "image", "mimeType": "image/png", "data": base64.b64encode(picture).decode()})
            result = {"content": content, "structuredContent": data, "isError": error}
        except (ValueError, KeyError, OSError, ValidationError) as error:
            result = {"content": [{"type": "text", "text": str(error)}], "isError": True}
    else:
        return {"jsonrpc": "2.0", "id": request["id"], "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": request["id"], "result": result}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=Path, required=True)
    parser.add_argument("--negative", type=Path, required=True)
    parser.add_argument("--positive", type=Path, required=True)
    args = parser.parse_args()
    provider = Provider(args.folder, args.negative, args.positive)

    class Download(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
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
            provider.log({"download": self.path, "sha256": hashlib.sha256(data).hexdigest()})

        def do_POST(self) -> None:
            try:
                if self.path != "/upload":
                    raise ValueError("Unknown upload route")
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 8 * 1024 * 1024:
                    raise ValueError("Upload must be 1 byte to 8 MiB")
                message = BytesParser(policy=policy.default).parsebytes(
                    ("Content-Type: " + self.headers.get("Content-Type", "") + "\r\nMIME-Version: 1.0\r\n\r\n").encode()
                    + self.rfile.read(length))
                parts = list(message.iter_parts()) if message.is_multipart() else []
                if len(parts) != 1 or parts[0].get_param("name", header="content-disposition") != "file":
                    raise ValueError("Expected one multipart file field")
                payload = parts[0].get_payload(decode=True)
                if not isinstance(payload, bytes):
                    raise TypeError("Expected binary file payload")
                result = provider.upload(payload)
                data = json.dumps(result).encode()
            except (ValueError, TypeError, OSError) as error:
                self.send_error(400, str(error))
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, format: str, *args) -> None:
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
    main()
