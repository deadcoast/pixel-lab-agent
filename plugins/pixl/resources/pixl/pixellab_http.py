"""Optional official PixelLab HTTP adapter; transport is injectable for offline tests.

The local state server never calls this adapter. Submission is explicit and claims
the existing durable job before the single HTTP request; there are no retries.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import io
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Protocol

from jsonschema import Draft202012Validator, ValidationError
from PIL import Image

from . import codec, graph, jobs, service, store
from .codec import PixlError

BASE_URL = "https://api.pixellab.ai/v2"
CREATE_PATH = "/create-image-pixflux-background"
PROVIDER = "pixellab-http"
OPERATION = "create_image_pixflux_background"
MAX_RESPONSE = 12 * 1024 * 1024


class Transport(Protocol):
    simulated: bool

    def request(self, method: str, path: str, body: dict | None) -> dict: ...


class ProviderError(Exception):
    """Sanitized transport failure; never retain tokens or raw error bodies."""

    def __init__(self, code: str, *, definite_rejection: bool = False):
        self.code = code
        self.definite_rejection = definite_rejection
        super().__init__(code)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class HTTPS:
    simulated = False

    def __init__(self, token: str):
        if not token or any(c in token for c in "\r\n"):
            raise PixlError(
                "pixellab_auth", "Set PIXELLAB_API_KEY in the host environment"
            )
        self._token = token

    def request(self, method: str, path: str, body: dict | None) -> dict:
        allowed = (method == "POST" and path == CREATE_PATH) or (
            method == "GET" and re.fullmatch(r"/background-jobs/[A-Za-z0-9_-]+", path)
        )
        if not allowed:
            raise ProviderError("unsupported_endpoint", definite_rejection=True)
        data = None if body is None else json.dumps(body, allow_nan=False).encode()
        request = urllib.request.Request(
            BASE_URL + path,
            data=data,
            method=method,
            headers={
                "Authorization": "Bearer " + self._token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        # No redirect can forward credentials or repeat a generation request.
        opener = urllib.request.build_opener(_NoRedirect())
        try:
            with opener.open(request, timeout=30) as response:
                raw = response.read(MAX_RESPONSE + 1)
        except urllib.error.HTTPError as error:
            raise ProviderError(
                f"http_{error.code}", definite_rejection=400 <= error.code < 500
            ) from None
        except (OSError, TimeoutError):
            raise ProviderError("transport_outcome_unknown") from None
        if len(raw) > MAX_RESPONSE:
            raise ProviderError("response_too_large")
        try:
            result = service.parse_json(raw)
        except (ValueError, PixlError):
            raise ProviderError("invalid_json_response") from None
        if not isinstance(result, dict):
            raise ProviderError("invalid_response_object")
        return result


def contract() -> dict:
    return service.read_json(
        service.resource_root() / "knowledge/pixellab-http-image.json"
    )


def schema(name: str) -> dict:
    """Keep the official fields unchanged, resolving only local schema references."""
    source = contract()

    def resolve(value):
        if isinstance(value, list):
            return [resolve(child) for child in value]
        if not isinstance(value, dict):
            return value
        if "$ref" in value:
            reference = value["$ref"]
            if not reference.startswith("#/components/schemas/"):
                raise PixlError(
                    "pixellab_schema", "Only retained local references are supported"
                )
            return resolve(source["components"]["schemas"][reference.rsplit("/", 1)[1]])
        return {key: resolve(child) for key, child in value.items()}

    return resolve(source["components"]["schemas"][name])


def _validate(value: dict, name: str) -> None:
    try:
        Draft202012Validator(schema(name)).validate(value)
    except ValidationError as error:
        raise PixlError("pixellab_schema", f"{name}: {error.validator}") from None


def validate_arguments(arguments: dict) -> None:
    _validate(arguments, "CreateImagePixfluxRequest")
    width, height = (arguments["image_size"][key] for key in ("width", "height"))
    if not 1024 <= width * height <= 160000:
        raise PixlError("pixellab_arguments", "Pixflux requires 1024 to 160000 pixels")


def _job(folder: Path, expected: str, job_id: str, root: Path) -> dict:
    doc = store.load(folder)
    if codec.digest(doc) != expected:
        raise PixlError("stale_write", "Reload the current project before acting")
    rows = jobs.report(doc, root)["jobs"]
    row = next((row for row in rows if row["id"] == job_id), None)
    if row is None or not row.get("durable"):
        raise PixlError("pixellab_job", "Select a durable prepared PixelLab HTTP job")
    request = row["request"]
    if request["provider"] != PROVIDER or request["tool"] != OPERATION:
        raise PixlError(
            "pixellab_job", "This adapter handles only its declared image operation"
        )
    return row


class Workflow:
    """Connect official API observations to existing job/import semantics."""

    def __init__(self, root: Path, transport: Transport):
        self.root = Path(root).resolve()
        self.transport = transport

    def _folder(self, folder: str) -> Path:
        return graph.confined(self.root, folder)

    def _load_job(self, folder: Path, expected: str, job_id: str) -> dict:
        row = _job(folder, expected, job_id, self.root)
        simulated = row["request"]["discovery"]["evidence"].get("simulated_transport")
        if simulated is not self.transport.simulated:
            raise PixlError(
                "pixellab_transport",
                "Cannot switch a saved job between mock and live transport",
            )
        return row

    def _evidence(self, **values) -> dict:
        return {"adapter": PROVIDER, "simulated": self.transport.simulated, **values}

    def _result(self, result: dict) -> dict:
        return dict(result, provider_simulated=self.transport.simulated)

    def prepare(
        self,
        folder: str,
        expected: str,
        job_id: str,
        task_id: str,
        output_id: str,
        arguments: dict,
        authorization: dict,
    ) -> dict:
        validate_arguments(arguments)
        source = contract()
        return self._result(
            jobs.prepare(
                self._folder(folder),
                expected,
                job_id,
                task_id,
                [output_id],
                PROVIDER,
                OPERATION,
                arguments,
                schema("CreateImagePixfluxRequest"),
                {
                    "source": source["source"],
                    "observed_at": source["retrieved_at"],
                    "evidence": {
                        "openapi_sha256": source["source_sha256"],
                        "surface": "dated official HTTP contract, not live MCP discovery",
                        "simulated_transport": self.transport.simulated,
                    },
                },
                authorization,
                self.root,
            )
        )

    def submit(self, folder: str, expected: str, job_id: str) -> dict:
        directory = self._folder(folder)
        row = self._load_job(directory, expected, job_id)
        validate_arguments(row["request"]["arguments"])
        claimed = jobs.dispatch(directory, expected, job_id, self.root)
        expected = claimed["hash"]
        # The persisted unknown claim protects even a process crash during POST.
        try:
            response = self.transport.request(
                "POST",
                CREATE_PATH,
                copy.deepcopy(claimed["dispatch_request"]["arguments"]),
            )
            _validate(response, "CreateImagePixfluxBackgroundResponse")
            remote_id = response["background_job_id"]
            if not isinstance(remote_id, str) or not re.fullmatch(
                r"[A-Za-z0-9_-]+", remote_id
            ):
                raise ProviderError("invalid_job_identifier")
        except (ProviderError, PixlError) as error:
            failed = isinstance(error, ProviderError) and error.definite_rejection
            code = error.code
            return self._result(
                jobs.observe(
                    directory,
                    expected,
                    job_id,
                    "failed" if failed else "unknown",
                    self._evidence(operation="submit", error=code),
                    root=self.root,
                )
            )
        return self._result(
            jobs.observe(
                directory,
                expected,
                job_id,
                "submitted",
                self._evidence(operation="submit", response=response),
                remote_id,
                self.root,
            )
        )

    def poll(self, folder: str, expected: str, job_id: str) -> dict:
        directory = self._folder(folder)
        row = self._load_job(directory, expected, job_id)
        remote_id = row["remote_id"]
        if row["state"] not in {"submitted", "running", "unknown"} or not remote_id:
            raise PixlError(
                "pixellab_poll", "A nonterminal job with a known ID is required"
            )
        if not re.fullmatch(r"[A-Za-z0-9_-]+", remote_id):
            raise PixlError("pixellab_poll", "Invalid job ID")
        try:
            response = self.transport.request(
                "GET", "/background-jobs/" + remote_id, None
            )
            _validate(response, "BackgroundJobResponse")
            if response["id"] != remote_id:
                raise ProviderError("response_identity_mismatch")
            states = {
                "processing": "running",
                "completed": "succeeded",
                "failed": "failed",
            }
            if response["status"] not in states:
                raise ProviderError("unrecognized_job_status")
        except (ProviderError, PixlError) as error:
            return self._result(
                jobs.observe(
                    directory,
                    expected,
                    job_id,
                    "unknown",
                    self._evidence(operation="poll", error=error.code),
                    root=self.root,
                )
            )
        return self._result(
            jobs.observe(
                directory,
                expected,
                job_id,
                states[response["status"]],
                self._evidence(operation="poll", response=response),
                remote_id,
                self.root,
            )
        )

    def import_image(
        self, folder: str, expected: str, job_id: str, output_id: str, candidate_id: str
    ) -> dict:
        directory = self._folder(folder)
        row = self._load_job(directory, expected, job_id)
        if row["state"] != "succeeded":
            raise PixlError("pixellab_import", "Wait for an observed completed job")
        event = next(
            event for event in reversed(row["events"]) if event["event"] == "succeeded"
        )
        response = event["evidence"]["response"]
        image = (response.get("last_response") or {}).get("image")
        if not isinstance(image, dict):
            raise PixlError(
                "pixellab_import", "Completed response has no supported inline image"
            )
        _validate(image, "Base64Image")
        encoded = image["base64"]
        if encoded.startswith("data:image/png;base64,"):
            encoded = encoded.split(",", 1)[1]
        try:
            data = base64.b64decode(encoded, validate=True)
            if not data or len(data) > 8 * 1024 * 1024:
                raise ValueError("image size")
            with Image.open(io.BytesIO(data)) as decoded:
                if decoded.format != "PNG" or max(decoded.size) > 1024:
                    raise ValueError("unsupported image")
                decoded.verify()
        except (OSError, ValueError):
            raise PixlError(
                "pixellab_import", "Expected a valid bounded PNG response"
            ) from None
        digest = hashlib.sha256(data).hexdigest()
        relative = (
            directory.relative_to(self.root) / "downloads" / (digest + ".png")
        ).as_posix()
        recovered_from: dict | None = None
        # A failed download publication may leave unreferenced cache data, but
        # must not publish a partial hash-named file or destroy old evidence.
        with store.lock(directory):
            self._load_job(directory, expected, job_id)
            target = graph.confined(self.root, relative)
            if not target.is_relative_to(directory):
                raise PixlError("pixellab_import", "Download must remain inside the store")
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and (existing := target.read_bytes()) != data:
                recovered_from = {
                    "path": relative,
                    "sha256": hashlib.sha256(existing).hexdigest(),
                    "bytes": len(existing),
                }
                relative = (
                    directory.relative_to(self.root) / "downloads" / "recovery"
                    / (digest + "-from-" + recovered_from["sha256"] + ".png")
                ).as_posix()
                target = graph.confined(self.root, relative)
                if not target.is_relative_to(directory):
                    raise PixlError("pixellab_import", "Download must remain inside the store")
                target.parent.mkdir(parents=True, exist_ok=True)
            reused_download = target.exists()
            if reused_download:
                if target.read_bytes() != data:
                    raise PixlError(
                        "pixellab_import",
                        "Retained recovery download changed; preserve both files and reconcile their identities",
                    )
            else:
                store._atomic(target, data)
        result = self._result(
            jobs.import_artifact(
                directory,
                expected,
                job_id,
                output_id,
                candidate_id,
                relative,
                self._evidence(
                    operation="import", remote_id=row["remote_id"], sha256=digest
                ),
                self.root,
            )
        )
        result["download"] = {
            "path": relative,
            "sha256": digest,
            "bytes": len(data),
            "reused_download": reused_download,
            "recovered_from": recovered_from,
        }
        return result
