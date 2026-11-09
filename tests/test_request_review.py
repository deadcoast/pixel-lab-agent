"""Exact review evidence and provider-bound continuation across public surfaces."""

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
from pixl.request_review import report, source_evidence
from tests.test_plar_prepare import seed, write


class RequestReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "consumer"
        self.args, self.packet, self.plan, self.arguments = seed(self.root)

    def snapshot(self):
        return {
            p.relative_to(self.root).as_posix(): p.read_bytes()
            for p in self.root.rglob("*")
            if p.is_file()
        }

    def save_plan(self):
        self.packet["criteria"] = write(self.root, "work/criteria.json", self.plan)
        write(self.root, self.args["packet"], self.packet)

    def test_exact_excerpts_preserve_authority_without_claiming_consistency(self):
        for c in self.plan["outputs"][0]["criteria"]:
            c["sources"][0]["lines"] = [3, 3]
        self.plan["outputs"][0]["criteria"][0]["authority"] = "proposal"
        self.save_plan()
        before = self.snapshot()
        result = report(self.root, self.args["packet"], self.args["asset_id"])
        self.assertEqual(result["request"]["arguments"], self.arguments)
        self.assertEqual(
            result["source_evidence"][0]["excerpts"][0]["text"],
            (self.root / "BRIEF.md")
            .read_bytes()
            .decode("utf-8-sig")
            .splitlines(keepends=True)[2],
        )
        self.assertEqual(result["criteria"]["comparisons"][0]["authority"], "proposal")
        self.assertIsNone(result["consistent"])
        self.assertEqual(result["caller_comparison"], "unperformed")
        self.assertEqual(before, self.snapshot())

    def test_legacy_numbered_prose_reports_invalid_bounds_without_rewriting_packet(
        self,
    ):
        self.plan["outputs"][0]["criteria"][0]["sources"][0]["locator"] = (
            "line 999: claimed wording"
        )
        self.save_plan()
        before = self.snapshot()
        result = report(self.root, self.args["packet"])
        self.assertEqual(result["diagnostics"][0]["status"], "invalid_locator")
        self.assertEqual(before, self.snapshot())

    def test_explicit_invalid_lines_fail_new_preparation_before_writes(self):
        self.plan["outputs"][0]["criteria"][0]["sources"][0]["lines"] = [999, 999]
        self.save_plan()
        before = self.snapshot()
        with self.assertRaisesRegex(PixlError, "criterion source lines"):
            service.call("pixl_plar_prepare", self.args, self.root)
        self.assertEqual(before, self.snapshot())

    def test_changed_sources_and_unresolved_labels_are_visible(self):
        result = report(self.root, self.args["packet"])
        self.assertEqual(result["diagnostics"][0]["status"], "unresolved_locator")
        (self.root / "BRIEF.md").write_text("Changed", encoding="utf-8")
        result = report(self.root, self.args["packet"], self.args["asset_id"])
        self.assertEqual(result["diagnostics"][0]["status"], "changed")
        self.assertEqual(result["diagnostics"][-1]["status"], "changed_selection")

    def test_packet_source_locators_are_checked_even_outside_criteria(self):
        for citation in (
            {"locator": "lines 2-999: assignment"},
            {"locators": ["lines 2-999: assignment"]},
        ):
            with self.subTest(citation=citation):
                source = self.packet["sources"][0]
                source.pop("locator", None)
                source.pop("locators", None)
                source.update(citation)
                write(self.root, self.args["packet"], self.packet)
                result = report(self.root, self.args["packet"])
                self.assertTrue(
                    any(
                        d.get("packet_source") == source["path"]
                        and d["status"] == "invalid_locator"
                        for d in result["diagnostics"]
                    )
                )

    def test_repeated_source_roles_keep_every_citation_visible(self):
        source = dict(self.packet["sources"][0])
        self.packet["sources"] = [
            {**source, "role": "assignment", "locator": "line 999"},
            {**source, "role": "display", "locator": "line 3"},
        ]
        write(self.root, self.args["packet"], self.packet)
        before = self.snapshot()
        result = report(self.root, self.args["packet"])
        self.assertEqual(len(result["sources"]), 2)
        self.assertEqual(result["sources"][0]["role"], "assignment")
        self.assertEqual(result["sources"][1]["role"], "display")
        statuses = [
            result["source_evidence"][row["source_evidence"][0]]["status"]
            for row in result["sources"]
        ]
        self.assertEqual(statuses, ["invalid_locator", "resolved"])
        self.assertEqual(before, self.snapshot())

    def test_uncited_packet_reference_drift_is_reported(self):
        pointer = write(self.root, "work/reference-context.json", {"role": "palette"})
        self.packet["sources"].append({**pointer, "role": "reference context"})
        write(self.root, self.args["packet"], self.packet)
        write(self.root, pointer["path"], {"role": "different context"})
        result = report(self.root, self.args["packet"])
        self.assertEqual(result["sources"][-1]["binding"], "changed")
        self.assertTrue(
            any(d.get("source") == pointer["path"] for d in result["diagnostics"])
        )

    def test_tampered_criteria_and_escaping_sources_are_not_reviewed(self):
        (self.root / "work/criteria.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(PixlError, "changed artifact"):
            report(self.root, self.args["packet"])
        with self.assertRaises(PixlError):
            source_evidence(
                self.root, {"path": "../outside", "lines": [1, 1]}, "0" * 64
            )

    def test_binary_source_and_excessive_range_have_explicit_limits(self):
        image = self.root / "binary.png"
        image.write_bytes(b"\x89PNG\xff")
        row = source_evidence(
            self.root,
            {"path": image.name, "locator": "appearance"},
            sha256(image.read_bytes()).hexdigest(),
        )
        self.assertEqual(row["status"], "visual_source")
        brief = self.root / "BRIEF.md"
        row = source_evidence(
            self.root,
            {"path": brief.name, "lines": [1, 3]},
            sha256(brief.read_bytes()).hexdigest(),
            budget=1,
        )
        self.assertEqual(row["status"], "needs_narrower_range")
        self.assertNotIn("excerpts", row)

    def test_reviewed_connection_hash_and_provider_survive_preparation(self):
        self.packet["request"]["provider"] = self.args["connection"]["provider"]
        self.packet["request"]["connection"] = write(
            self.root, "work/reviewed-connection.json", self.args["connection"]
        )
        write(self.root, self.args["packet"], self.packet)
        resolved = report(self.root, self.args["packet"])
        self.assertEqual(
            resolved["request"]["connection"]["provider"],
            self.args["connection"]["provider"],
        )
        changed = dict(self.args["connection"], provider="different-provider")
        before = self.snapshot()
        with self.assertRaisesRegex(PixlError, "reviewed provider"):
            service.call(
                "pixl_plar_prepare", {**self.args, "connection": changed}, self.root
            )
        self.assertEqual(before, self.snapshot())
        write(self.root, "work/reviewed-connection.json", changed)
        before = self.snapshot()
        with self.assertRaisesRegex(PixlError, "changed artifact"):
            report(self.root, self.args["packet"])
        with self.assertRaises(PixlError):
            service.call(
                "pixl_plar_prepare", {**self.args, "connection": changed}, self.root
            )
        self.assertEqual(before, self.snapshot())

    def test_new_preparation_retains_exact_reviewed_connection_file(self):
        pointer = write(
            self.root, "work/reviewed-connection.json", self.args["connection"]
        )
        self.packet["request"]["connection"] = pointer
        write(self.root, self.args["packet"], self.packet)
        result = service.call("pixl_plar_prepare", self.args, self.root)
        markers = list((self.root / result["store"] / "plans").glob("*.json"))
        marker = json.loads(markers[0].read_bytes())
        retained = marker["sources"][pointer["path"]]
        self.assertEqual(
            (self.root / retained["path"]).read_bytes(),
            (self.root / pointer["path"]).read_bytes(),
        )

    def test_same_provider_with_unreviewed_connection_assertions_is_rejected(self):
        import copy

        self.packet["request"]["connection"] = write(
            self.root, "work/reviewed-connection.json", self.args["connection"]
        )
        write(self.root, self.args["packet"], self.packet)
        changed = copy.deepcopy(self.args["connection"])
        changed["authorization"]["scope"] = "Different supplied assertion"
        before = self.snapshot()
        with self.assertRaisesRegex(PixlError, "exact reviewed connection"):
            service.call(
                "pixl_plar_prepare", {**self.args, "connection": changed}, self.root
            )
        self.assertEqual(before, self.snapshot())

    def test_cli_and_mcp_return_same_readonly_evidence(self):
        arguments = {"packet": self.args["packet"], "asset_id": self.args["asset_id"]}
        result = dispatch(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "pixl_request_review", "arguments": arguments},
            },
            self.root,
        )
        response = subprocess.run(
            [
                sys.executable,
                "-B",
                "-m",
                "pixl",
                "request-review",
                self.args["packet"],
                "--asset",
                self.args["asset_id"],
                "--root",
                str(self.root),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(
            json.loads(response.stdout), result["result"]["structuredContent"]
        )
        listing = dispatch(
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, self.root
        )
        declaration = next(
            t for t in listing["result"]["tools"] if t["name"] == "pixl_request_review"
        )
        # Optional result_path makes this tool capable of a local file write.
        self.assertFalse(declaration["annotations"]["readOnlyHint"])

    def test_pending_handoff_and_success_follow_same_provider_generation(self):
        first = service.call("pixl_plar_prepare", self.args, self.root)
        folder = self.root / first["store"]
        claimed = jobs.dispatch(folder, first["hash"], first["job"]["id"], self.root)
        submitted = jobs.observe(
            folder,
            claimed["hash"],
            first["job"]["id"],
            "submitted",
            {"fixture": True},
            remote_id="retained-1",
            root=self.root,
        )
        continuation = plar.read(self.root, asset_id=self.args["asset_id"])[
            "production"
        ]["continuation"]
        self.assertEqual(continuation["action"], "observe")
        self.assertEqual(
            continuation["before_another_request"][0]["job"], first["job"]["id"]
        )
        self.assertEqual(
            continuation["jobs"][0]["provider"], self.args["connection"]["provider"]
        )
        self.assertEqual(continuation["jobs"][0]["remote_id"], "retained-1")
        self.assertEqual(
            continuation["jobs"][0]["discovery"], self.args["connection"]["discovery"]
        )
        jobs.observe(
            folder,
            submitted["hash"],
            first["job"]["id"],
            "succeeded",
            {"fixture": True},
            root=self.root,
        )
        production = plar.read(self.root, asset_id=self.args["asset_id"])["production"]
        self.assertEqual(production["continuation"]["action"], "retrieve_and_import")
        self.assertEqual(
            production["continuation"]["before_another_request"][0]["action"],
            "retrieve_and_import",
        )
        self.assertEqual(production["task"], first["task"])


if __name__ == "__main__":
    unittest.main()
