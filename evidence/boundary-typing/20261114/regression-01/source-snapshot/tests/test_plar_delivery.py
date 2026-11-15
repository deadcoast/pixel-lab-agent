"""Controlled retrieval of a retained generation and actual consumer-module mapping."""

import json
import shutil
import subprocess
import sys
import unittest
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from evaluations.plar_delivery_case import INTEGRATION, fixture_png
from evaluations.plar_delivery_fixture import DeliveryProvider

ROOT = Path(__file__).resolve().parents[1]


class PLARDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        fixture_png(self.folder / "provider-result.png")
        (self.folder / "provider-state.json").write_text(
            json.dumps(
                {
                    "jobs": [
                        {
                            "job_id": "original",
                            "status": "failed",
                            "arguments": {"description": "Old"},
                        },
                        {
                            "job_id": "selected",
                            "status": "queued",
                            "arguments": {"description": "Retained"},
                        },
                    ]
                }
            ),
            encoding="utf-8",
        )

    def test_retrieves_same_job_across_clients_without_new_submission(self):
        first = DeliveryProvider(self.folder)
        result, data = first.call("get_image", {"job_id": "selected"})
        self.assertEqual(data, (self.folder / "provider-result.png").read_bytes())
        self.assertEqual(result["images"][0]["sha256"], sha256(data).hexdigest())
        second = DeliveryProvider(self.folder)
        observed, _ = second.call("list_jobs", {})
        self.assertEqual(len(observed["jobs"]), 2)
        self.assertEqual(observed["jobs"][1]["arguments"], {"description": "Retained"})
        self.assertEqual(second.image("selected"), data)
        with self.assertRaises(ValueError):
            second.call("create_image_pro_flash", {"description": "Duplicate"})
        with self.assertRaises(ValueError):
            second.call("get_image", {"job_id": "original"})
        (self.folder / "provider-result.png").write_bytes(b"changed")
        with self.assertRaises(ValueError):
            second.image("selected")

    def test_stdio_mcp_returns_inline_and_downloaded_identical_bytes(self):
        process = subprocess.Popen(
            [
                sys.executable,
                "-B",
                "-m",
                "evaluations.plar_delivery_fixture",
                "--folder",
                str(self.folder),
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            process.stdin.write(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "tools/call",
                        "params": {
                            "name": "get_image",
                            "arguments": {"job_id": "selected"},
                        },
                    }
                )
                + "\n"
            )
            process.stdin.flush()
            response = json.loads(process.stdout.readline())["result"]
            self.assertFalse(response["isError"])
            self.assertEqual(response["content"][1]["type"], "image")
            url = response["structuredContent"]["images"][0]["download_url"]
            with urlopen(url, timeout=5) as download:
                self.assertEqual(
                    download.read(), (self.folder / "provider-result.png").read_bytes()
                )
        finally:
            process.communicate(timeout=10)
        events = [
            json.loads(line)
            for line in (self.folder / "provider-calls.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        self.assertTrue(any(e.get("download") == "/selected.png" for e in events))
        self.assertFalse(any(e.get("tool") == "create_image_pro_flash" for e in events))

    def test_real_consumer_modules_accept_mapping_and_reject_wrong_backend_state(self):
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node is unavailable for actual TypeScript module execution")
        shutil.copytree(ROOT / "examples/plar-project/src", self.folder / "src")
        (self.folder / "assets").mkdir()
        shutil.copyfile(
            self.folder / "provider-result.png", self.folder / "assets/ready.png"
        )
        (self.folder / "verify-integration.mjs").write_text(
            INTEGRATION, encoding="utf-8"
        )
        command = [node, "verify-integration.mjs", "assets/ready.png"]
        result = subprocess.run(
            command, cwd=self.folder, capture_output=True, text=True, check=True
        )
        self.assertEqual(json.loads(result.stdout)["state"], "succeeded")
        backend = self.folder / "src/queue.ts"
        backend.write_text(
            backend.read_text(encoding="utf-8").replace(
                'ok: "succeeded"', 'ok: "failed"'
            ),
            encoding="utf-8",
        )
        rejected = subprocess.run(
            command, cwd=self.folder, capture_output=True, text=True, check=False
        )
        self.assertNotEqual(rejected.returncode, 0)


if __name__ == "__main__":
    unittest.main()
