"""Evaluation faults exercise real runtime publication, not simulated acceptance."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations.authoring_mcp import install
from pixl import codec, jobs, plar, production_plan, store
from tests.family_support import family
from tests.test_plar_prepare import seed
from tests.test_production_plan import packet, plan


class AuthoringEvaluationTests(unittest.TestCase):
    def test_interruption_then_requirement_update_preserves_original_and_blocks_dispatch(
        self,
    ):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            seed(root)
            original = (root / "plar.txt").read_bytes()
            (root / "authoring-plar.txt").write_bytes(original)
            folder = root / ".pixl/family"
            family(root, folder)
            value = plan()
            selection = plar.read(
                root, "authoring-plar.txt", "queue.working", include_production=False
            )
            value["stages"][0]["selection"] = {
                "path": "authoring-plar.txt",
                "asset": "queue.working",
                "requirements_hash": selection["requirements_hash"],
            }
            events = root / "events.jsonl"
            with patch.multiple(
                production_plan,
                _links=production_plan._links,
                prepare=production_plan.prepare,
            ):
                install(root, events, production_plan, plar)
                authored = production_plan.author(
                    folder, codec.digest(store.load(folder)), value, root
                )
                self.assertEqual(
                    authored["allocation"][0]["status"], "needs_reconciliation"
                )
                self.assertNotIn(
                    "production",
                    plar.read(root, "authoring-plar.txt", "queue.working")["asset"],
                )
                repeated = production_plan.author(folder, authored["hash"], value, root)
                self.assertTrue(repeated["already_authored"])
                self.assertEqual(repeated["hash"], authored["hash"])
                self.assertEqual(repeated["allocation"][0]["status"], "linked")
                request = packet(store.load(folder))
                prepared = production_plan.prepare(
                    folder,
                    repeated["hash"],
                    "next.plan",
                    "motion",
                    "next.job",
                    request,
                    root,
                )
                self.assertEqual(
                    prepared["evaluation_observation"]["kind"],
                    "caller_requirement_updated",
                )
                current = codec.digest(store.load(folder))
                with self.assertRaises(codec.PixlError):
                    jobs.dispatch(folder, current, "next.job", root)
                self.assertEqual(codec.digest(store.load(folder)), current)
                self.assertEqual(
                    store.load(folder).records["next.job"].fields["si"].value,
                    "prepared",
                )
                self.assertEqual((root / "plar.txt").read_bytes(), original)
                observed = [
                    json.loads(line) for line in events.read_text().splitlines()
                ]
                self.assertEqual(
                    [r["kind"] for r in observed],
                    ["allocation_write_interrupted", "caller_requirement_updated"],
                )
                self.assertNotEqual(
                    observed[1]["previous_requirements"],
                    observed[1]["current_requirements"],
                )
