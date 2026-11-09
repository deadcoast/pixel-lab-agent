"""Public hash domains and relocated path examples protect actual publication guards."""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pixl import codec, graph, mcp, production_plan, production_review, service, store
from pixl.codec import PixlError
from tests.family_support import family
from tests.test_plar_prepare import seed
from tests.test_production_plan import plan


class PublicGuidanceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "consumer with spaces"
        self.root.mkdir()
        self.folder = self.root / ".pixl"
        family(self.root, self.folder)

    def cli(self, *args, cwd=None):
        # Source entry point avoids depending on a previously built bundle.
        code = "import runpy,sys; sys.path.insert(0,sys.argv.pop(1)); runpy.run_module('pixl',run_name='__main__')"
        return subprocess.run([sys.executable, "-c", code, str(Path(__file__).resolve().parents[1]), *map(str, args)], cwd=cwd, capture_output=True, check=False)

    def test_canonical_state_is_not_arbitrary_wire_file_sha256(self):
        doc = store.load(self.folder)
        lines = codec.encode(doc).splitlines()
        alternate = self.root / "alternate.px"
        alternate.write_bytes(b"\r\n".join([lines[0], *reversed(lines[1:])]) + b"\r\n")
        result = service.call("pixl_validate", {"path": "alternate.px"}, self.root)
        self.assertEqual(result["hash"], codec.digest(doc))
        self.assertNotEqual(result["hash"], hashlib.sha256(alternate.read_bytes()).hexdigest())
        self.assertEqual(result["hash_domains"]["hash"], "canonical_state_sha256")
        response = self.cli("validate", alternate, "--root", self.root, cwd=self.root.parent)
        self.assertEqual(response.returncode, 0, response.stderr)
        self.assertEqual(json.loads(response.stdout), result)

    def test_plar_file_requirements_and_state_domains_cannot_be_swapped(self):
        consumer = self.root / "allocated"
        args, _, _, _ = seed(consumer)
        service.call("pixl_plar_prepare", args, consumer)
        selected = service.call("pixl_plar_read", {"asset_id": args["asset_id"]}, consumer)
        self.assertEqual(selected["hash_domains"], {"hash": "file_sha256", "requirements_hash": "selected_requirements_sha256",
                         "production.continuation.state_hash": "canonical_state_sha256"})
        handoff = {"asset_id": args["asset_id"], "requirements_hash": selected["requirements_hash"],
                   "expect": selected["hash"], "details": {"status": "partial"}}
        before = {p: p.read_bytes() for p in consumer.rglob("*") if p.is_file()}
        with self.assertRaisesRegex(PixlError, "production.continuation.state_hash"):
            service.call("pixl_plar_handoff", handoff, consumer)
        self.assertEqual(before, {p: p.read_bytes() for p in consumer.rglob("*") if p.is_file()})
        handoff["expect"] = selected["production"]["continuation"]["state_hash"]
        result = service.call("pixl_plar_handoff", handoff, consumer)
        self.assertEqual(result["hash_domains"]["sha256"], "file_sha256")
        self.assertEqual(result["sha256"], graph.file_hash(consumer / result["path"]))
        self.assertEqual(result, service.call("pixl_plar_handoff", handoff, consumer))
        original = json.loads((consumer / "plar.txt").read_bytes())
        (consumer / "plar.txt").write_text(json.dumps(original, indent=4), encoding="utf-8")
        reformatted = service.call("pixl_plar_read", {"asset_id": args["asset_id"]}, consumer)
        self.assertNotEqual(selected["hash"], reformatted["hash"])
        self.assertEqual(selected["requirements_hash"], reformatted["requirements_hash"])

    def test_plan_review_identity_and_full_export_are_preserved(self):
        production_plan.author(self.folder, codec.digest(store.load(self.folder)), plan(), self.root)
        plain = production_review.report(self.root, ".pixl/state.px", "next.plan")
        args = {"packet": ".pixl/state.px", "plan": "next.plan"}
        result = service.call("pixl_request_review", args, self.root)
        self.assertEqual({k: v for k, v in result.items() if k != "hash_domains"}, plain)
        self.assertEqual(result["hash_domains"]["state.sha256"], "canonical_state_sha256")
        exported = service.call("pixl_request_review", {**args, "result_path": "work/review.json"}, self.root)
        self.assertEqual(json.loads((self.root / exported["result_path"]).read_bytes()), result)
        self.assertEqual(exported["hash_domains"], {"result_sha256": "file_sha256"})
        self.assertEqual(exported["result_sha256"], graph.file_hash(self.root / exported["result_path"]))

    def test_relocated_consumer_source_and_request_paths_agree(self):
        production_plan.author(self.folder, codec.digest(store.load(self.folder)), plan(), self.root)
        moved = self.root.parent / "relocated consumer"
        shutil.copytree(self.root, moved)
        arguments = {"packet": ".pixl/state.px", "plan": "next.plan"}
        expected = service.call("pixl_request_review", arguments, moved)
        output = self.cli("request-review", ".pixl/state.px", "--plan", "next.plan", "--root", moved, cwd=moved.parent)
        self.assertEqual(output.returncode, 0, output.stderr)
        self.assertEqual(json.loads(output.stdout), expected)
        (moved / "evidence.txt").write_bytes(b"first\nexact source\nlast\n")
        source_args = {"path": "evidence.txt", "expect": graph.file_hash(moved / "evidence.txt"), "start": 2, "end": 2}
        source = service.call("pixl_source", source_args, moved)
        output = self.cli("source", "evidence.txt", "--expect", source_args["expect"], "--start", 2, "--end", 2, "--root", moved, cwd=moved.parent)
        self.assertEqual(output.returncode, 0, output.stderr)
        self.assertEqual(json.loads(output.stdout), source)
        self.assertEqual(source["text"], "exact source\n")
        for bad in [str(moved / ".pixl/state.px"), "../outside.px", ".pixl\\state.px"]:
            with self.assertRaisesRegex(PixlError, "declared root") as caught:
                service.call("pixl_request_review", {**arguments, "packet": bad}, moved)
            self.assertEqual(caught.exception.code, "path_escape")

    def test_stale_publication_error_names_state_domain_in_both_surfaces(self):
        before = (self.folder / "state.px").read_bytes()
        args = {"store": ".pixl", "expect": "0" * 64, "output_id": "delivery.output", "candidate_id": "package"}
        response = mcp.dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "pixl_family_snapshot", "arguments": args}}, self.root)
        self.assertTrue(response["result"]["isError"])
        self.assertIn("canonical production state hash", json.dumps(response))
        output = self.cli("family-snapshot", self.folder, "delivery.output", "package", "--expect", "0" * 64, "--root", self.root)
        self.assertEqual(output.returncode, 2)
        self.assertEqual(json.loads(output.stderr)["error"], "stale_write")
        self.assertIn("canonical production state hash", json.loads(output.stderr)["detail"])
        self.assertEqual(json.loads(output.stderr)["detail"].count("stale_write"), 1)
        self.assertEqual(before, (self.folder / "state.px").read_bytes())


if __name__ == "__main__":
    unittest.main()
