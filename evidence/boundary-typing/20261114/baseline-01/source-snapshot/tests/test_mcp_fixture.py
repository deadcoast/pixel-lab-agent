"""Verify that the MCP fixture cannot silently resubmit an uncertain job."""

import base64
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import Request, urlopen

from evaluations.pixellab_mcp_fixture import Provider, handle

ROOT = Path(__file__).resolve().parents[1]
NEGATIVE = ROOT / "evidence/host-evaluation/fixture-inputs/candidate.png"
POSITIVE = ROOT / "evidence/host-evaluation/fixture-inputs/reference.png"


class McpFixtureTests(unittest.TestCase):
    def test_first_request_connection_retains_exact_arguments_across_clients(self):
        from evaluations.plar_request_fixture import RequestProvider

        with TemporaryDirectory() as temp:
            folder = Path(temp)
            caller, specialist = RequestProvider(folder), RequestProvider(folder)
            arguments = {
                "description": "A readable Ready indicator",
                "width": 16,
                "height": 16,
                "no_background": True,
            }
            result = specialist.request("create_image_pro_flash", arguments)
            current = caller.request("list_jobs", {})
            self.assertEqual(current["jobs"], [result])
            self.assertEqual(current["jobs"][0]["arguments"], arguments)
            self.assertTrue(result["provider_simulated"])
            with self.assertRaisesRegex(ValueError, "one request"):
                caller.request("create_image_pro_flash", arguments)

    def test_continuation_fixture_requires_terminal_original_and_accepts_only_one_new_job(self):
        from evaluations.plar_request_fixture import RequestProvider

        with TemporaryDirectory() as temp:
            folder = Path(temp)
            provider = RequestProvider(folder, continuation=True)
            original = provider.request("create_image_pro_flash", {"description": "Original"})
            with self.assertRaises(ValueError):
                provider.request("create_image_pro_flash", {"description": "New"})
            state = json.loads((folder / "provider-state.json").read_bytes())
            state["jobs"][0]["status"] = "failed"
            (folder / "provider-state.json").write_text(json.dumps(state), encoding="utf-8")
            self.assertEqual(provider.request("list_jobs", {})["jobs"][0]["status"], "failed")
            revised = provider.request("create_image_pro_flash", {"description": "New"})
            self.assertNotEqual(original["job_id"], revised["job_id"])
            with self.assertRaises(ValueError):
                provider.request("create_image_pro_flash", {"description": "Duplicate"})

    def arguments(self):
        return {
            "method": "reference",
            "description": "Restore the missing identity details.",
            "image_base64": base64.b64encode(NEGATIVE.read_bytes()).decode(),
            "reference_image": {
                "base64": base64.b64encode(POSITIVE.read_bytes()).decode()
            },
        }

    def test_uncertain_job_survives_restart_and_prevents_duplicate(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            first = Provider(folder, NEGATIVE, POSITIVE)
            result, error, _ = first.call("edit_image_pro_flash", self.arguments())
            self.assertTrue(error)
            self.assertNotIn("job_id", result)
            resumed = Provider(folder, NEGATIVE, POSITIVE)
            with self.assertRaisesRegex(ValueError, "reconcile"):
                resumed.call("edit_image_pro_flash", self.arguments())
            jobs, _, _ = resumed.call("list_jobs", {})
            ident = jobs["jobs"][0]["job_id"]
            _, error, image = resumed.call("get_image", {"job_id": ident})
            self.assertFalse(error)
            self.assertEqual(image, NEGATIVE.read_bytes())
            revised, error, _ = resumed.call("edit_image_pro_flash", self.arguments())
            self.assertFalse(error)
            _, _, image = resumed.call("get_image", {"job_id": revised["job_id"]})
            self.assertEqual(image, POSITIVE.read_bytes())
            self.assertNotEqual(image, NEGATIVE.read_bytes())
            with self.assertRaises(ValueError):
                resumed.call("edit_image_pro_flash", self.arguments())

    def test_separate_host_connections_share_current_jobs_and_uploads(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            caller = Provider(folder, NEGATIVE, POSITIVE)
            specialist = Provider(folder, NEGATIVE, POSITIVE)
            image = caller.upload(NEGATIVE.read_bytes())["ref"]
            reference = caller.upload(POSITIVE.read_bytes())["ref"]
            args = {
                "method": "reference",
                "image_url": image,
                "reference_image": {"url": reference},
            }
            specialist.call("edit_image_pro_flash", args)
            jobs, _, _ = caller.call("list_jobs", {})
            self.assertEqual(len(jobs["jobs"]), 1)
            with self.assertRaisesRegex(ValueError, "reconcile"):
                caller.call("edit_image_pro_flash", args)
            ident = jobs["jobs"][0]["job_id"]
            caller.call("get_image", {"job_id": ident})
            self.assertEqual(specialist.image(ident), NEGATIVE.read_bytes())
            second, _, _ = specialist.call("edit_image_pro_flash", args)
            _, _, downloaded = caller.call("get_image", {"job_id": second["job_id"]})
            self.assertEqual(downloaded, POSITIVE.read_bytes())

    def test_invalid_reference_does_not_create_job(self):
        with TemporaryDirectory() as temp:
            provider = Provider(Path(temp), NEGATIVE, POSITIVE)
            args = self.arguments()
            args["reference_image"]["base64"] = "not an image"
            response = handle(
                provider,
                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": "edit_image_pro_flash", "arguments": args},
                },
            )
            self.assertTrue(response["result"]["isError"])
            self.assertEqual(provider.state["jobs"], [])

    def test_corrupted_png_and_unknown_upload_do_not_create_jobs(self):
        with TemporaryDirectory() as temp:
            provider = Provider(Path(temp), NEGATIVE, POSITIVE)
            broken = bytearray(NEGATIVE.read_bytes())
            broken[71] ^= 2
            for kind in ("source", "reference", "unknown_upload"):
                args = self.arguments()
                if kind == "source":
                    args["image_base64"] = base64.b64encode(broken).decode()
                elif kind == "reference":
                    args["reference_image"]["base64"] = base64.b64encode(
                        broken
                    ).decode()
                else:
                    args.pop("image_base64")
                    args["image_url"] = "upload:unknown"
                with self.subTest(kind=kind), self.assertRaises(ValueError):
                    provider.call("edit_image_pro_flash", args)
                self.assertEqual(provider.state["jobs"], [])

    def test_uploaded_bytes_survive_restart_and_remain_bound(self):
        with TemporaryDirectory() as temp:
            folder = Path(temp)
            provider = Provider(folder, NEGATIVE, POSITIVE)
            uploaded = provider.upload(NEGATIVE.read_bytes())
            resumed = Provider(folder, NEGATIVE, POSITIVE)
            self.assertEqual(
                resumed.input_image(None, uploaded["ref"]), NEGATIVE.read_bytes()
            )
            entry = resumed.state["uploads"][uploaded["ref"]]
            (folder / entry["path"]).write_bytes(POSITIVE.read_bytes())
            with self.assertRaisesRegex(ValueError, "changed"):
                resumed.input_image(None, uploaded["ref"])

    def test_cold_setup_preserves_bound_discovery_and_uploaded_files(self):
        from evaluations.mcp_asset_case import setup

        with TemporaryDirectory() as temp:
            root = Path(temp)
            old, new = root / "old", root / "new"
            old.mkdir()
            (old / "project").mkdir()
            setup(old / "project", old, Path(sys.executable))
            provider = Provider(old, NEGATIVE, POSITIVE)
            uploaded = provider.upload(NEGATIVE.read_bytes())
            discovery = old / "project/provider-schemas.json"
            schemas = json.loads(discovery.read_text())
            schemas.pop("get_upload_url")
            discovery.write_text(json.dumps(schemas))
            original = discovery.read_bytes()
            shutil.copytree(old / "project", new / "project")
            setup(new / "project", new, Path(sys.executable), old)
            self.assertEqual(
                (new / "project/provider-schemas.json").read_bytes(), original
            )
            self.assertIn(
                "get_upload_url",
                json.loads((new / "project/current-provider-schemas.json").read_text()),
            )
            resumed = Provider(new, NEGATIVE, POSITIVE)
            self.assertEqual(
                resumed.input_image(None, uploaded["ref"]), NEGATIVE.read_bytes()
            )

    def test_stdio_discovery_and_actual_loopback_download(self):
        with TemporaryDirectory() as temp:
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-B",
                    "-m",
                    "evaluations.pixellab_mcp_fixture",
                    "--folder",
                    temp,
                    "--negative",
                    str(NEGATIVE),
                    "--positive",
                    str(POSITIVE),
                ],
                cwd=ROOT,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            try:

                def rpc(method, params=None):
                    request = {
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": method,
                        "params": params or {},
                    }
                    process.stdin.write(json.dumps(request) + "\n")
                    process.stdin.flush()
                    return json.loads(process.stdout.readline())["result"]

                self.assertEqual(len(rpc("tools/list")["tools"]), 4)
                upload = rpc("tools/call", {"name": "get_upload_url", "arguments": {}})[
                    "structuredContent"
                ]["upload_url"]

                def send_file(path):
                    body = (
                        b'--fixture-boundary\r\nContent-Disposition: form-data; name="file"; filename="sprite.png"\r\nContent-Type: image/png\r\n\r\n'
                        + path.read_bytes()
                        + b"\r\n--fixture-boundary--\r\n"
                    )
                    request = Request(
                        upload,
                        data=body,
                        headers={
                            "Content-Type": "multipart/form-data; boundary=fixture-boundary"
                        },
                    )
                    with urlopen(request, timeout=5) as response:
                        return json.load(response)["ref"]

                args = {
                    "method": "reference",
                    "description": "Repair identity",
                    "image_url": send_file(NEGATIVE),
                    "reference_image": {"url": send_file(POSITIVE)},
                }
                first = rpc(
                    "tools/call", {"name": "edit_image_pro_flash", "arguments": args}
                )
                self.assertTrue(first["isError"])
                jobs = rpc("tools/call", {"name": "list_jobs", "arguments": {}})[
                    "structuredContent"
                ]
                result = rpc(
                    "tools/call",
                    {
                        "name": "get_image",
                        "arguments": {"job_id": jobs["jobs"][0]["job_id"]},
                    },
                )
                link = result["structuredContent"]["images"][0]["download_url"]
                self.assertTrue(link.startswith("http://127.0.0.1:"))
                with urlopen(link, timeout=5) as response:
                    self.assertEqual(response.read(), NEGATIVE.read_bytes())
                self.assertEqual(
                    base64.b64decode(result["content"][1]["data"]),
                    NEGATIVE.read_bytes(),
                )
            finally:
                process.stdin.close()
                process.wait(timeout=10)
                process.stdout.close()
                errors = process.stderr.read()
                process.stderr.close()
            self.assertEqual(process.returncode, 0, errors)


if __name__ == "__main__":
    unittest.main()
