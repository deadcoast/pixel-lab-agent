"""Exercise the production HTTP/job/import path while prohibiting real sockets."""

import base64
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from evaluations.pixellab_mock import MockTransport
from pixl import codec, service, store
from pixl.codec import PixlError
from pixl.pixellab_http import (
    HTTPS,
    ProviderError,
    Workflow,
    schema,
    validate_arguments,
)
from pixl.pixellab_mcp import dispatch
from tests.lifecycle_support import sample


class PixelLabHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.folder = self.root / ".pixl"
        doc = sample(self.root)
        doc.records["choice"].fields["vl"] = [32, 32]
        doc.records["contract"].fields["px"] = [32, 32]
        store.initialize(self.folder, doc, self.root)
        self.image = self.root / "fixture.png"
        Image.new("RGBA", (32, 32), "teal").save(self.image)
        self.transport = MockTransport(self.image)
        self.workflow = Workflow(self.root, self.transport)
        self.arguments = {
            "description": "A teal robot",
            "image_size": {"width": 32, "height": 32},
            "no_background": True,
        }
        self.socket_guard = patch(
            "socket.socket", side_effect=AssertionError("Unexpected network call")
        )
        self.socket_guard.start()
        self.addCleanup(self.socket_guard.stop)

    def expected(self):
        return codec.digest(store.load(self.folder))

    def prepare(self):
        return self.workflow.prepare(
            ".pixl",
            self.expected(),
            "job",
            "task",
            "output",
            self.arguments,
            {
                "scope": "Mocked generation only; zero provider calls",
                "evidence": {"test": True},
            },
        )

    def submit(self):
        self.prepare()
        return self.workflow.submit(".pixl", self.expected(), "job")

    def complete(self):
        self.submit()
        self.workflow.poll(".pixl", self.expected(), "job")
        return self.workflow.poll(".pixl", self.expected(), "job")

    def test_complete_official_request_poll_import_does_not_accept_art(self):
        self.assertEqual(self.complete()["job"]["state"], "succeeded")
        result = self.workflow.import_image(
            ".pixl", self.expected(), "job", "output", "candidate"
        )
        self.assertTrue(result["provider_simulated"])
        self.assertEqual(
            [c["method"] for c in self.transport.calls], ["POST", "GET", "GET"]
        )
        self.assertEqual(self.transport.calls[0]["body"], self.arguments)
        doc = store.load(self.folder)
        self.assertEqual(
            (self.root / doc.records["candidate"].fields["ur"]).read_bytes(),
            self.image.read_bytes(),
        )
        self.assertEqual(doc.records["task"].fields["ca"], [])
        self.assertEqual(doc.records["task"].fields["vr"], [])
        report = service.workflow(self.folder / "state.px", self.root)
        self.assertEqual(report["tasks"][0]["state"], "open")

    def test_post_timeout_is_saved_unknown_and_cold_retry_is_blocked(self):
        self.transport.mode = "timeout"
        self.assertEqual(self.submit()["job"]["state"], "unknown")
        restarted = Workflow(self.root, self.transport)
        with self.assertRaises(PixlError):
            restarted.submit(".pixl", self.expected(), "job")
        self.assertEqual(len(self.transport.calls), 1)

    def test_explicit_http_rejection_is_saved_failed(self):
        self.transport.mode = "rejected"
        result = self.submit()
        self.assertEqual(result["job"]["state"], "failed")
        self.assertEqual(result["job"]["events"][-1]["evidence"]["error"], "http_402")

    def test_provider_failure_is_not_importable(self):
        self.transport.mode = "failed"
        self.assertEqual(self.complete()["job"]["state"], "failed")
        with self.assertRaisesRegex(PixlError, "pixellab_import"):
            self.workflow.import_image(
                ".pixl", self.expected(), "job", "output", "candidate"
            )
        self.assertNotIn("candidate", store.load(self.folder).records)

    def test_invalid_arguments_fail_before_publication_or_transport(self):
        before = self.expected()
        for changes in (
            {"image_size": {"width": 16, "height": 16}},
            {"made_up": True},
            {"image_size": {"width": True, "height": 32}},
        ):
            with self.subTest(changes=changes):
                original = self.arguments
                self.arguments = dict(original, **changes)
                with self.assertRaises(PixlError):
                    self.prepare()
                self.arguments = original
        self.assertEqual(self.expected(), before)
        self.assertEqual(self.transport.calls, [])

    def test_stale_submission_never_reaches_transport(self):
        before = self.expected()
        self.prepare()
        with self.assertRaisesRegex(PixlError, "stale_write"):
            self.workflow.submit(".pixl", before, "job")
        self.assertEqual(self.transport.calls, [])

    def test_wrong_remote_identity_is_unknown_without_rebinding(self):
        self.submit()
        with patch.object(
            self.transport,
            "request",
            return_value={
                "id": "wrong",
                "status": "completed",
                "created_at": "2026-11-05",
            },
        ):
            result = self.workflow.poll(".pixl", self.expected(), "job")
        self.assertEqual(result["job"]["state"], "unknown")
        self.assertEqual(result["job"]["remote_id"], self.transport.remote_id)

    def test_invalid_submission_response_remains_unknown(self):
        self.prepare()
        with patch.object(
            self.transport, "request", return_value={"status": "processing"}
        ):
            result = self.workflow.submit(".pixl", self.expected(), "job")
        self.assertEqual(result["job"]["state"], "unknown")

    def test_malformed_image_does_not_create_candidate(self):
        self.submit()
        body = {
            "id": self.transport.remote_id,
            "created_at": "2026-11-05",
            "status": "completed",
            "last_response": {
                "image": {"base64": base64.b64encode(b"not png").decode()}
            },
        }
        with patch.object(self.transport, "request", return_value=body):
            self.workflow.poll(".pixl", self.expected(), "job")
        before = self.expected()
        with self.assertRaisesRegex(PixlError, "valid bounded PNG"):
            self.workflow.import_image(".pixl", before, "job", "output", "candidate")
        self.assertEqual(self.expected(), before)

    def test_mcp_discovers_real_adapter_and_rejects_bad_arguments(self):
        response = dispatch(
            {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, self.workflow
        )
        self.assertEqual(len(response["result"]["tools"]), 5)
        response = dispatch(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "pixellab_submit", "arguments": {}},
            },
            self.workflow,
        )
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(self.transport.calls, [])

    def test_official_schema_preserves_http_names_and_closed_properties(self):
        self.assertIn("image_size", schema("CreateImagePixfluxRequest")["properties"])
        self.assertFalse(schema("CreateImagePixfluxRequest")["additionalProperties"])
        validate_arguments(self.arguments)

    def test_http_transport_uses_fixed_official_url_and_never_retries(self):
        token = "fictional-test-token"
        transport = HTTPS(token)
        with patch("urllib.request.build_opener") as opener:
            opener.return_value.open.side_effect = TimeoutError(
                "Do not retain token " + token
            )
            with self.assertRaises(ProviderError) as caught:
                transport.request(
                    "POST", "/create-image-pixflux-background", self.arguments
                )
            self.assertEqual(opener.return_value.open.call_count, 1)
            request = opener.return_value.open.call_args.args[0]
            self.assertEqual(
                request.full_url,
                "https://api.pixellab.ai/v2/create-image-pixflux-background",
            )
            self.assertEqual(json.loads(request.data), self.arguments)
            self.assertNotIn(token, str(caught.exception))

    def test_missing_credentials_and_unexpected_endpoint_fail_closed(self):
        with self.assertRaisesRegex(PixlError, "pixellab_auth"):
            HTTPS("")
        with self.assertRaises(ProviderError):
            HTTPS("fictional").request("POST", "https://elsewhere.test", {})

    def test_saved_mock_job_cannot_be_submitted_with_live_transport(self):
        self.prepare()
        live = HTTPS("fictional")
        with patch.object(live, "request") as request:
            with self.assertRaisesRegex(PixlError, "pixellab_transport"):
                Workflow(self.root, live).submit(".pixl", self.expected(), "job")
            request.assert_not_called()

    def test_mock_stdio_server_exposes_production_adapter(self):
        runner = Path(__file__).resolve().parents[1] / "evaluations/pixellab_mock.py"
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "pixellab_contract", "arguments": {}},
            },
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": None},
        ]
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(runner),
                "--root",
                str(self.root),
                "--image",
                str(self.image),
                "--log",
                str(self.root / "calls.jsonl"),
            ],
            input="".join(json.dumps(message) + "\n" for message in messages),
            text=True,
            capture_output=True,
            check=False,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertIn("MOCK TRANSPORT", rows[0]["result"]["instructions"])
        contract = rows[1]["result"]["structuredContent"]
        self.assertTrue(contract["simulated"])
        self.assertEqual(contract["path"], "/create-image-pixflux-background")
        self.assertEqual(rows[2]["error"]["code"], -32602)
        self.assertFalse((self.root / "calls.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
