"""Exact production handoff identity and caller-authored judgment boundaries."""

import json
import subprocess
import sys
import unittest
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory

from pixl import jobs, plar, service
from pixl.codec import PixlError
from pixl.mcp import dispatch
from tests.test_plar_prepare import seed, write


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "consumer"
        self.args, _, _, _ = seed(self.root)
        self.prepared = service.call("pixl_plar_prepare", self.args, self.root)
        self.inputs = {
            "asset_id": self.args["asset_id"],
            "requirements_hash": self.args["requirements_hash"],
            "expect": self.prepared["hash"],
            "details": {"status": "partial", "future_work": ["Review the family after the current candidate"]},
        }

    def files(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def save(self, **changes):
        return service.call("pixl_plar_handoff", {**self.inputs, **changes}, self.root)

    def test_preserves_entire_continuation_without_mutating_production(self):
        before = self.files()
        selected = plar.read(self.root, asset_id=self.args["asset_id"])
        result = self.save()
        data = (self.root / result["path"]).read_bytes()
        document = json.loads(data)
        self.assertEqual(sha256(data).hexdigest(), result["sha256"])
        self.assertEqual(document["resume"], selected["production"]["continuation"])
        self.assertEqual(document["next"], document["resume"]["action"])
        self.assertEqual(document["details"], self.inputs["details"])
        self.assertEqual(document["selection"]["hash"], selected["hash"])
        self.assertEqual(before, {p: b for p, b in self.files().items() if p in before})
        self.assertEqual(set(self.files()) - set(before), {result["path"]})

    def test_retry_is_idempotent_and_corrupt_receipt_is_not_overwritten(self):
        result = self.save()
        before = self.files()
        self.assertEqual(self.save(), result)
        self.assertEqual(self.files(), before)
        (self.root / result["path"]).write_bytes(b"changed")
        with self.assertRaisesRegex(PixlError, "Retained snapshot bytes changed"):
            self.save()
        self.assertEqual((self.root / result["path"]).read_bytes(), b"changed")

    def test_observation_requires_fresh_state_and_preserves_old_handoff(self):
        old = self.save()
        folder = self.root / self.prepared["store"]
        claimed = jobs.dispatch(folder, self.prepared["hash"], self.prepared["job"]["id"], self.root)
        observed = jobs.observe(folder, claimed["hash"], self.prepared["job"]["id"], "submitted", {"fixture": True}, remote_id="same-job", root=self.root)
        before = self.files()
        with self.assertRaisesRegex(PixlError, "Production state changed"):
            self.save()
        self.assertEqual(self.files(), before)
        new = self.save(expect=observed["hash"])
        snapshot = json.loads((self.root / new["path"]).read_bytes())
        self.assertNotEqual(old["path"], new["path"])
        self.assertEqual(snapshot["next"], "observe")
        self.assertEqual(snapshot["resume"]["jobs"][0]["remote_id"], "same-job")
        self.assertEqual(snapshot["resume"]["jobs"][0]["discovery"], self.args["connection"]["discovery"])
        self.assertEqual(sha256((self.root / old["path"]).read_bytes()).hexdigest(), old["sha256"])

    def test_stale_requirements_and_missing_production_do_not_write(self):
        before = self.files()
        with self.assertRaisesRegex(PixlError, "Selected requirements changed"):
            self.save(requirements_hash="0" * 64)
        self.assertEqual(before, self.files())
        ready = plar.read(self.root, asset_id="queue.ready")
        with self.assertRaisesRegex(PixlError, "No production continuation"):
            self.save(asset_id="queue.ready", requirements_hash=ready["requirements_hash"])
        self.assertEqual(before, self.files())

    def test_agent_comments_cannot_replace_derived_fields(self):
        before = self.files()
        for key in ["resume", "next", "asset_id", "requirements_hash", "version"]:
            with self.subTest(key=key), self.assertRaises(PixlError):
                self.save(details={**self.inputs["details"], key: "rewritten"})
        with self.assertRaises(PixlError):
            self.save(details={"status": "automatically_accepted"})
        self.assertEqual(before, self.files())

    def test_cli_mcp_share_exact_artifact_and_mutation_annotation(self):
        write(self.root, "details.json", self.inputs["details"])
        response = subprocess.run([sys.executable, "-B", "-m", "pixl", "plar", "handoff", str(self.root / "details.json"), "--asset", self.inputs["asset_id"], "--requirements", self.inputs["requirements_hash"], "--expect", self.inputs["expect"], "--root", str(self.root)], capture_output=True, text=True, check=True)
        mcp = dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "pixl_plar_handoff", "arguments": self.inputs}}, self.root)
        self.assertEqual(json.loads(response.stdout), mcp["result"]["structuredContent"])
        listing = dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, self.root)
        tool = next(t for t in listing["result"]["tools"] if t["name"] == "pixl_plar_handoff")
        self.assertFalse(tool["annotations"]["readOnlyHint"])


if __name__ == "__main__":
    unittest.main()
