"""Focused orientation preserves identities without asserting art acceptance."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from pixl import codec, graph, jobs, mcp, production_plan, service, store
from pixl.codec import PixlError, Record, Ref, Symbol
from tests.family_support import family
from tests.test_production_plan import packet, plan


class AuthoringContextTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        family(self.root)
        self.folder = self.root / ".pixl"
        production_plan.author(self.folder, codec.digest(store.load(self.folder)), plan(), self.root)
        self.args = {"path": ".pixl/state.px", "focus": "next.plan", "view": "authoring"}

    def report(self, **extra):
        return service.call("pixl_context", self.args | extra, self.root)

    def test_exact_current_records_and_shared_sources_without_history(self):
        before = (self.folder / "state.px").read_bytes()
        report = self.report()
        self.assertEqual({r["id"] for r in report["criteria"]}, {"next.motion.q.shape", "next.delivery.q.shape"})
        self.assertEqual(report["criteria"][1]["fields"]["ck"], plan()["stages"][0]["criteria"][0]["check"])
        self.assertEqual(len(report["sources"]), 1)
        source = report["sources"][0]
        excerpt = service.call(source["retrieve"]["tool"], source["retrieve"]["arguments"], self.root)
        self.assertIn("Developer fixture brief", json.dumps(excerpt))
        self.assertEqual({r["id"] for r in report["plans"]}, {"next.plan"})
        self.assertNotIn("delivery.output", {r["id"] for r in report["outputs"]})
        self.assertIn("member", {r["id"] for r in report["artifacts"]})
        self.assertIn("contract", {r["id"] for r in report["contracts"]})
        self.assertTrue(all("vr" not in t["fields"] for t in report["tasks"]))
        self.assertIsNone(report["consistent"])
        self.assertEqual(before, (self.folder / "state.px").read_bytes())

    def test_pending_intent_is_visible_without_provider_payload_or_event_expansion(self):
        doc = store.load(self.folder)
        production_plan.prepare(self.folder, codec.digest(doc), "next.plan", "motion", "next.job", packet(doc), self.root)
        report = self.report()
        self.assertEqual(len(report["jobs"]), 1)
        job = report["jobs"][0]
        self.assertEqual((job["state"], job["next_action"]), ("prepared", "dispatch"))
        self.assertNotIn("request", job)
        self.assertNotIn("events", job)
        full = service.call(job["retrieve"]["tool"], job["retrieve"]["arguments"], self.root)
        self.assertEqual(full["jobs"][0]["intent_sha256"], job["intent_sha256"])
        self.assertEqual(report["plans"][0]["jobs"], ["next.job"])
        jobs.observe(self.folder, codec.digest(store.load(self.folder)), "next.job", "failed", {"reason": "Synthetic prepared-only abandonment; no provider call"}, root=self.root)
        self.assertEqual(self.report()["jobs"][0]["state"], "failed")

    def test_changed_source_remains_visible_and_full_context_still_rejects(self):
        (self.root / "source.txt").write_text("Changed consumer requirements\n", encoding="utf-8")
        self.assertEqual(self.report()["sources"][0]["file_status"], "changed")
        with self.assertRaises(PixlError):
            self.report(view="complete")

    def test_cli_and_mcp_match_and_complete_wire_default_is_unchanged(self):
        result = subprocess.run([sys.executable, "-m", "pixl", "context", str(self.folder / "state.px"), "next.plan", "--view", "authoring", "--root", str(self.root)], capture_output=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(result.stdout), self.report())
        default = service.call("pixl_context", {"path": ".pixl/state.px", "focus": "next.plan"}, self.root)
        self.assertEqual(default, self.report(view="complete"))
        self.assertTrue(default["wire"].startswith("PX2"))
        # The existing tool is extended; no separate overlapping MCP operation.
        schema = next(t[2] for t in mcp.TOOLS if t[0] == "pixl_context")
        self.assertIn("authoring", schema["properties"]["view"]["enum"])

    def test_scope_and_incompatible_options_are_rejected(self):
        for extra in ({"budget": 1000}, {"asset_id": "missing"}, {"focus": "source"}, {"view": "typo"}, {"view": "complete", "plar_path": "plar.txt"}):
            with self.subTest(extra=extra), self.assertRaises(PixlError):
                self.report(**extra)

    def test_unlinked_intake_stays_discoverable_without_expanding_selected_authority(self):
        baseline = self.report()
        doc = store.load(self.folder)
        doc.records["unlinked"] = Record(id="unlinked", kind="I", fields={
            "pr": Ref("project"), "wh": Ref("user"), "ky": "another.asset",
            "st": Symbol("proposed"), "vl": "Unrelated asset detail. " * 5000, "so": [], "wy": "Not linked to this assignment."})
        doc.records["project"].fields["in"].append(Ref("unlinked"))
        graph.validate(doc, self.root)
        (self.folder / "state.px").write_bytes(codec.encode(doc))
        report = self.report()
        self.assertEqual(baseline["choices"], report["choices"])
        self.assertEqual(baseline["sources"], report["sources"])
        self.assertNotIn("in", report["projects"][0]["fields"])
        other = next(r for r in report["choice_scope"]["other_intake"] if r["id"] == "unlinked")
        full = service.call(other["retrieve"]["tool"], other["retrieve"]["arguments"], self.root)
        self.assertIn("Unrelated asset detail.", full["wire"])
        self.assertNotIn("Unrelated asset detail.", json.dumps(report))

    def test_destinations_and_transitive_decision_choices_keep_authority_and_status(self):
        doc = store.load(self.folder)
        for key, value in [("caller.choice", Ref("caller.dependency")), ("caller.dependency", "Keep selective antialiasing")]:
            doc.records[key] = Record(id=key, kind="I", fields={"pr": Ref("project"), "wh": Ref("user"), "ky": key,
                "st": Symbol("observed"), "vl": value, "so": [Ref("source")], "wy": "Source observation, not confirmation."})
            doc.records["project"].fields["in"].append(Ref(key))
        doc.records["decision"].fields["wr"].append(Ref("caller.choice"))
        # Rebuild this synthetic fixture's bindings; no production receipt is amended.
        for record in doc.records.values():
            if record.kind == "E":
                for binding in record.fields["bs"]:
                    binding["dg"] = codec.record_hash(doc.records[binding["rf"].id])
        for ref in doc.records["decision"].fields["pc"]:
            receipt = doc.records[ref.id]
            existing = {b["rf"].id for b in receipt.fields["bs"]}
            for ident in sorted(graph.proof_scope(doc, ["decision"]) - existing):
                receipt.fields["bs"].append({"rf": Ref(ident), "dg": codec.record_hash(doc.records[ident])})
        (self.folder / "state.px").write_bytes(codec.encode(doc))
        report = self.report()
        choices = {r["id"]: r for r in report["choices"]}
        self.assertTrue({"destination", "caller.choice", "caller.dependency"} <= choices.keys())
        self.assertEqual(choices["caller.dependency"]["fields"]["st"], {"$symbol": "observed"})
        self.assertEqual(choices["caller.choice"]["fields"]["wh"], {"$ref": "user"})
