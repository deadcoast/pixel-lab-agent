"""Offline HTTP transport used by the REAL PixelLab adapter. No network fallback."""

from __future__ import annotations

import argparse
import base64
import copy
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch


class MockTransport:
    simulated = True

    def __init__(self, image: Path, *, mode: str = "success", log: Path | None = None):
        self.image = Path(image)
        self.mode = mode
        self.log = log
        self.calls: list[dict] = []
        self.submitted = False
        self.polls = 0
        self.remote_id = "test-pixellab-0001"

    def request(self, method: str, path: str, body: dict | None) -> dict:
        from pixl.pixellab_http import CREATE_PATH, ProviderError, validate_arguments

        entry = {
            "method": method,
            "path": path,
            "body": copy.deepcopy(body),
            "simulated": True,
        }
        self.calls.append(entry)
        if self.log:
            with self.log.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(entry) + "\n")
        if method == "POST" and path == CREATE_PATH:
            if not isinstance(body, dict):
                raise ProviderError("invalid_mock_request", definite_rejection=True)
            validate_arguments(body)
            if self.submitted:
                raise ProviderError(
                    "duplicate_mock_submission", definite_rejection=True
                )
            self.submitted = True
            if self.mode == "timeout":
                raise ProviderError("transport_outcome_unknown")
            if self.mode == "rejected":
                raise ProviderError("http_402", definite_rejection=True)
            return {"background_job_id": self.remote_id, "status": "processing"}
        if (
            method != "GET"
            or path != "/background-jobs/" + self.remote_id
            or not self.submitted
        ):
            raise ProviderError("unexpected_mock_request", definite_rejection=True)
        self.polls += 1
        status = (
            "processing"
            if self.polls == 1
            else "failed"
            if self.mode == "failed"
            else "completed"
        )
        result: dict = {
            "id": self.remote_id,
            "status": status,
            "created_at": "2026-11-05T00:00:00Z",
        }
        if status == "completed":
            result["last_response"] = {
                "image": {
                    "type": "base64",
                    "format": "png",
                    "base64": base64.b64encode(self.image.read_bytes()).decode(),
                }
            }
        elif status == "failed":
            result["last_response"] = {"error": "Controlled provider failure fixture"}
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--plugin", type=Path)
    parser.add_argument(
        "--mode",
        choices=("success", "timeout", "rejected", "failed"),
        default="success",
    )
    args = parser.parse_args()
    if args.plugin:
        sys.path.insert(0, str(args.plugin / "runtime"))
        os.environ["PIXL_PLUGIN_ROOT"] = str(args.plugin)
    else:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from pixl.pixellab_http import Workflow
    from pixl.pixellab_mcp import serve

    # Trap accidental HTTP calls even if production code is changed later.
    def forbidden(*args, **kwargs):
        raise RuntimeError("Network disabled in the PixelLab mock process")

    with patch("socket.socket", side_effect=forbidden):
        serve(
            Workflow(args.root, MockTransport(args.image, mode=args.mode, log=args.log))
        )


if __name__ == "__main__":
    main()
