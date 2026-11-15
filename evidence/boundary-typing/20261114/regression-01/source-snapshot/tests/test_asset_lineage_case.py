"""Bounded lineage preparation, preservation and qualification refusal tests."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
import zipfile
from functools import cache
from pathlib import Path
from unittest.mock import patch

from evaluations import asset_lineage_case as case
from evaluations import asset_lineage_grade as grader
from evaluations.host_trials import inventory, sha, write_json
from pixl import asset_lineage, codec


@cache
def retained_files():
    return case.consumer_execution_case.retained_project()[0]


class AssetLineageCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reuse the durable restoration proof; no ignored live consumer is an input.
        cls.files = retained_files()
        cls.document = codec.parse(cls.files[case.STATE])
        cls.required = {case.STATE, case.PLAR, "BRIEF.md", *case.SOURCES.values(), *(
            cls.document.records[candidate].fields["ur"]
            for candidates in case.MEMBERS.values() for candidate in candidates)}

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="asset lineage fixture ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.consumer = self.root / "external consumer"
        self.attempt = self.root / "attempt"

    def fake_consumer_setup(self, destination, host, python, *, package, consumer):
        """Avoid native discovery and redundant full image-tree writes in unit tests.

        The reused consumer case separately verifies the complete historical
        closure. These preparation tests keep the actual state/member bytes.
        """
        destination.mkdir()
        consumer.mkdir()
        for name in self.required:
            target = consumer / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(self.files[name])
        write_json(consumer / case.consumer_execution_case.INPUTS / "restoration.json", {
            "scope": "Unit test subset of verified historical state/member bytes; native setup is mocked."})
        write_json(destination / "identity.json", {"inputs": inventory(consumer), "package_files": {}})
        write_json(destination / "launch.json", {"host": host, "cwd": str(consumer), "case": "consumer-execution"})
        (destination / "runner.py.txt").write_bytes(b"consumer setup runner\n")
        return consumer

    def prepare(self):
        with patch.object(case.consumer_execution_case, "prepare", side_effect=self.fake_consumer_setup) as setup, \
                patch.object(case, "run") as launch:
            root = case.prepare(self.attempt, "codex", Path(sys.executable), consumer=self.consumer)
        setup.assert_called_once_with(self.attempt, "codex", Path(sys.executable), package=None, consumer=self.consumer)
        launch.assert_not_called()
        return root

    def test_prepares_only_read_operations_over_exact_original_and_reused_members(self):
        self.prepare()
        identity = json.loads((self.attempt / "identity.json").read_bytes())
        fixture = json.loads((self.consumer / case.INPUTS / "fixture.json").read_bytes())
        self.assertEqual(fixture["families"], {"original": "live.family.candidate", "reused": "artistic2.delivery.candidate"})
        self.assertEqual(len(fixture["reads"]), 10)
        self.assertEqual({value["tool"] for value in fixture["reads"].values()},
                         {"pixl_review_context", "pixl_family", "pixl_plar_read", "pixl_source"})
        for role, pair in fixture["members"].items():
            self.assertEqual(tuple(item["candidate"] for item in pair), case.MEMBERS[role])
            self.assertEqual(pair[0]["sha256"], pair[1]["sha256"])
            for item in pair:
                self.assertEqual(sha(self.consumer / item["path"]), item["sha256"])
        for name in self.required:
            self.assertEqual((self.consumer / name).read_bytes(), self.files[name])
        self.assertEqual(identity["baseline_production"], inventory(self.consumer / ".pixl"))
        self.assertEqual(identity["inputs"], inventory(self.consumer))
        self.assertEqual(json.loads((self.attempt / "launch.json").read_bytes())["artifact_roots"], [case.WORK])
        self.assertEqual((self.attempt / "consumer-setup-runner.py.txt").read_bytes(), b"consumer setup runner\n")
        self.assertFalse((self.attempt / "stdout.jsonl").exists())

    def test_assignment_keeps_known_history_and_unknowns_separate_from_new_execution(self):
        self.prepare()
        assignment = (self.consumer / "ASSET-LINEAGE.md").read_text(encoding="utf-8")
        for term in ("Working's generated", "deterministic construction", "controlled fixture provenance",
                     "deterministic cutout", "Unknown or unsupported", "actual named", "inspected_sources",
                     "new_provider_execution=false", "acceptance_created=false", "M1/M2 and broader M3"):
            self.assertIn(term, assignment)
        self.assertIn("No provider calls", (self.consumer / "AGENTS.md").read_text(encoding="utf-8"))

    def test_tampered_member_fails_preparation_without_native_sampling(self):
        original = self.fake_consumer_setup
        def corrupted(*args, **kwargs):
            consumer = original(*args, **kwargs)
            name = self.document.records[case.MEMBERS["working"][0]].fields["ur"]
            (consumer / name).write_bytes(b"tampered historical art")
            return consumer
        with (patch.object(case.consumer_execution_case, "prepare", side_effect=corrupted),
              patch.object(case, "run") as launch,
              self.assertRaisesRegex(ValueError, "member bytes changed")):
            case.prepare(self.attempt, "codex", Path(sys.executable), consumer=self.consumer)
        launch.assert_not_called()
        self.assertFalse((self.consumer / case.WORK / "CALLER-RESULT.json").exists())

    def test_retention_copies_new_reports_without_duplicating_original_images_or_state(self):
        self.prepare()
        write_json(self.consumer / case.WORK / "CALLER-RESULT.json", {"status": "incomplete", "limitations": ["Missing source proof"]})
        case.retain(self.attempt)
        self.assertEqual(set(inventory(self.attempt / "outputs")), {"CALLER-RESULT.json"})
        self.assertFalse((self.attempt / "final-pixl").exists())
        self.assertFalse((self.attempt / "unexpected-delta.zip").exists())
        preservation = json.loads((self.attempt / "preservation.json").read_bytes())
        self.assertEqual(preservation["changed"], [])
        self.assertTrue(preservation["production_unchanged"])
        before = inventory(self.attempt)
        with self.assertRaisesRegex(ValueError, "Preserve prior retention"):
            case.retain(self.attempt)
        self.assertEqual(inventory(self.attempt), before)

    def test_continuation_retention_uses_original_baseline_without_rewriting_history(self):
        self.prepare()
        write_json(self.attempt / "continuation.json", {"session_id": "same-parent"})
        write_json(self.consumer / case.WORK / "original-read.json", {"retained": True})
        case.retain(self.attempt)
        before = inventory(self.attempt)
        resumed = self.root / "resumed"
        resumed.mkdir()
        launch = {"cwd": str(self.consumer), "predecessor": case.reference(self.attempt / "continuation.json")}
        write_json(resumed / "launch.json", launch)
        write_json(resumed / "identity.json", {"mode": "native_same_session"})
        write_json(self.consumer / case.WORK / "COMPARISON.json", {"scope": "new read-only report"})
        case.retain(resumed, baseline=self.attempt)
        self.assertEqual(inventory(self.attempt), before)
        self.assertEqual(inventory(resumed / "outputs"), inventory(self.consumer / case.WORK))
        self.assertTrue(json.loads((resumed / "preservation.json").read_bytes())["production_unchanged"])
        rejected = self.root / "wrong-resume"
        rejected.mkdir()
        launch["predecessor"]["sha256"] = "0" * 64
        write_json(rejected / "launch.json", launch)
        with self.assertRaisesRegex(ValueError, "exact original"):
            case.retain(rejected, baseline=self.attempt)
        self.assertFalse((rejected / "outputs").exists())

    def test_retention_records_unexpected_production_change_and_missing_input(self):
        self.prepare()
        (self.consumer / case.STATE).write_bytes(b"unexpected state mutation")
        (self.consumer / "BRIEF.md").unlink()
        case.retain(self.attempt)
        preservation = json.loads((self.attempt / "preservation.json").read_bytes())
        self.assertFalse(preservation["production_unchanged"])
        self.assertIn(case.STATE, preservation["changed"])
        self.assertIn("BRIEF.md", preservation["removed"])
        with zipfile.ZipFile(self.attempt / "unexpected-delta.zip") as archive:
            self.assertEqual(archive.read(case.STATE), b"unexpected state mutation")
            self.assertEqual(archive.namelist(), [case.STATE])


class AssetLineageGradeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="asset lineage grade ")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name).resolve()
        files = retained_files()
        cls.doc = codec.parse(files[case.STATE])
        names = {record.fields["ur"] for record in cls.doc.records.values() if record.kind == "X"}
        names.update(case.SOURCES.values())
        for name in names:
            path = cls.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(files[name])
        cls.lineages = {role: asset_lineage.describe(cls.doc, cls.root, pair[0]) for role, pair in case.MEMBERS.items()}
        cls.fixture = {"members": {role: [{"candidate": candidate, "sha256": cls.doc.records[candidate].fields["dg"]}
                                        for candidate in pair] for role, pair in case.MEMBERS.items()}}
        cls.comparison = {"families": case.FAMILIES, "key_claims": dict(case.KEY_CLAIMS), "limitations": ["Retained observations only"],
                          "members": {role: {"original_candidate": pair[0]["candidate"], "reused_candidate": pair[1]["candidate"],
                                             "original_sha256": pair[0]["sha256"], "reused_sha256": pair[1]["sha256"], "same_bytes": True,
                                             "findings": "Same hash; source record explains request intent, not remote authentication.",
                                             "limits": ["No parent inferred"], "evidence": [{"path": case.SOURCES["ready_fixture"],
                                                 "sha256": sha(cls.root / case.SOURCES["ready_fixture"])}]}
                                      for role, pair in cls.fixture["members"].items()}}

    def test_actual_retained_direct_importers_and_bounded_comparison_pass(self):
        for role, lineage in self.lineages.items():
            with self.subTest(role=role):
                self.assertEqual(grader.lineage_errors(self.doc, self.root, role, lineage), [])
        self.assertEqual(grader.comparison_errors(self.comparison, self.fixture, self.root), [])

    def test_each_inflated_or_missing_key_claim_is_rejected(self):
        for key, expected in case.KEY_CLAIMS.items():
            for value in (not expected, None, int(expected)):
                with self.subTest(key=key, value=value):
                    comparison = copy.deepcopy(self.comparison)
                    comparison["key_claims"][key] = value
                    self.assertTrue(grader.comparison_errors(comparison, self.fixture, self.root))

    def test_wrong_family_member_or_hash_fails_even_when_claims_are_true(self):
        for key in ("original_candidate", "reused_candidate", "original_sha256", "reused_sha256"):
            comparison = copy.deepcopy(self.comparison)
            comparison["members"]["working"][key] = "incorrect"
            self.assertTrue(grader.comparison_errors(comparison, self.fixture, self.root))
        comparison = copy.deepcopy(self.comparison)
        comparison["original"] = "wrong alias beside correct families"
        self.assertTrue(grader.comparison_errors(comparison, self.fixture, self.root))

    def test_ready_simulation_and_final_working_edit_cannot_be_inflated(self):
        for role, field, value in (("ready", "simulated", False), ("ready", "provider", "pixellab"),
                                   ("working", "operation", "animation_request")):
            lineage = copy.deepcopy(self.lineages[role])
            selected = next(job for job in lineage["jobs"] if job["id"] in lineage["artifact"]["jobs"])
            selected[field] = value
            self.assertTrue(grader.lineage_errors(self.doc, self.root, role, lineage))

    def test_workflow_context_cannot_replace_direct_importer_and_byte_identity(self):
        for field, value in (("candidate", "live.working-seed.candidate"), ("sha256", "0" * 64), ("remote_verified", True)):
            lineage = copy.deepcopy(self.lineages["working"])
            lineage[field] = value
            self.assertTrue(grader.lineage_errors(self.doc, self.root, "working", lineage))
        lineage = copy.deepcopy(self.lineages["working"])
        lineage["artifact"]["jobs"] = ["live.working-seed.job"]
        self.assertTrue(grader.lineage_errors(self.doc, self.root, "working", lineage))

    def test_ready_generation_cannot_substitute_for_paused_or_working_support(self):
        for role, id_ in (("paused", "live.paused-02.job"), ("working", "live.working-seed.job"),
                          ("working", "live.working-animation-repair-01.job")):
            lineage = copy.deepcopy(self.lineages[role])
            lineage["jobs"] = [job for job in lineage["jobs"] if job["id"] != id_]
            self.assertTrue(any(job["provider"] == "pixellab-test" and job["operation"] == "generation_request"
                                for job in lineage["jobs"]))
            self.assertTrue(grader.lineage_errors(self.doc, self.root, role, lineage))
        for role in ("paused", "working"):
            lineage = copy.deepcopy(self.lineages[role])
            direct = next(job for job in lineage["jobs"] if job["id"] in lineage["artifact"]["jobs"])
            direct["source_requests"][0]["matching_jobs"] = ["r.22e90a2a03fe453a.request"]
            self.assertTrue(grader.lineage_errors(self.doc, self.root, role, lineage))

    def test_positive_layout_does_not_hide_contradictory_provenance_or_acceptance(self):
        for field in ("remote_verified", "new_acceptance", "same_bytes_proves_parent", "same_bytes_proves_reuse_direction"):
            comparison = copy.deepcopy(self.comparison)
            comparison["members"]["working"][field] = True
            self.assertTrue(grader.comparison_errors(comparison, self.fixture, self.root))
        comparison = copy.deepcopy(self.comparison)
        comparison["remote_execution_authenticated"] = True
        self.assertTrue(grader.comparison_errors(comparison, self.fixture, self.root))
        self.assertFalse(grader.reported_unchanged({"unchanged": True, "state_changed_reported": True}, True))

    def test_evidence_reference_requires_exact_existing_bytes(self):
        comparison = copy.deepcopy(self.comparison)
        comparison["members"]["ready"]["evidence"][0]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            grader.comparison_errors(comparison, self.fixture, self.root)
        with self.assertRaises(ValueError):
            grader.ref({"path": "first.json", "sha256": "a", "reference": {"path": "other.json", "sha256": "a"}})

    def test_reports_alone_do_not_establish_native_read_or_operation(self):
        path = self.root / "authored-report.json"
        write_json(path, {"status": "complete", "claimed_native_call": True})
        item = {"path": path.name, "sha256": sha(path)}
        self.assertEqual(grader.viewed([], path), [])
        self.assertEqual(grader.operation_proof([], self.root, "pixl_review_context", item), [])
        self.assertEqual(grader.grade(self.root)["status"], "fail")


class AssetLineageNativeProofTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="lineage proof adapters ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.python = Path(sys.executable)
        runner = self.root / case.KIT / "scripts/pixl.py"
        runner.parent.mkdir(parents=True)
        runner.write_text("# Unit-test byte binding only; never executed.\n")
        self.fixture = {"reads": {key: {"tool": "pixl_source", "arguments": {"path": "retained.json", "expect": "0" * 64,
                                               "start": 1, "end": 1, "budget": 1000},
                                              "result_path": case.WORK + "/" + key.replace("_", "-") + ".json"}
                                  for key in ("working_construction", "ready_fixture")}}
        for key, spec in self.fixture["reads"].items():
            write_json(self.root / spec["result_path"], {"text": "synthetic native transcript fixture " + key})
        write_json(self.root / case.INPUTS / "fixture.json", self.fixture)
        self.identity = {"inputs": {case.INPUTS + "/fixture.json": sha(self.root / case.INPUTS / "fixture.json")},
                         "package_files": {"scripts/pixl.py": sha(runner)}}
        self.key = "working_construction"
        self.target = self.root / self.fixture["reads"][self.key]["result_path"]
        self.item = {"path": self.target.relative_to(self.root).as_posix(), "sha256": sha(self.target)}
        self.body = grader.INLINE_READER.replace("PYTHON", repr(self.python.as_posix())).rstrip()
        self.command = "@'\n" + self.body + "\n'@ | & '" + self.python.as_posix() + "' -"
        self.output = "\n".join(key + " " + str((self.root / spec["result_path"]).stat().st_size)
                                for key, spec in self.fixture["reads"].items())

    @staticmethod
    def row(command, output, code=0, line=10):
        return {"file": "synthetic-native.jsonl", "line": line, "item": {
            "type": "CommandExecution", "command": command, "aggregated_output": output, "exit_code": code}}

    def proof(self, rows):
        return grader.inline_fixture_proof([rows], self.root, self.fixture, self.identity, self.python, self.key, self.item)

    def test_exact_successful_inline_runner_and_byte_receipts_are_bound(self):
        self.assertTrue(self.proof([self.row(self.command, self.output)]))
        self.assertFalse(self.proof([{"file": "synthetic-native.jsonl", "line": 10,
                                     "message": {"content": self.command + self.output}}]))

    def test_inline_runner_rejects_modified_payload_args_target_or_execution(self):
        replacements = (("dest.write_bytes(r.stdout)", "dest.write_bytes(b'fabricated')"),
                        ("[py,runner]+args", "[py,runner]+['source','wrong.json']"),
                        ("dest=root/spec['result_path']", "dest=root/'wrong.json'"),
                        ("r=subprocess.run([py,runner]+args,capture_output=True)", "r=pretend_result"),
                        ("assert r.returncode==0,(key,r.stderr)", "assert True"))
        for old, new in replacements:
            with self.subTest(old=old):
                self.assertFalse(self.proof([self.row(self.command.replace(old, new), self.output)]))
        self.assertFalse(self.proof([self.row(self.command, self.output, code=1)]))
        self.assertFalse(self.proof([self.row(self.command, self.output.splitlines()[0])]))
        self.assertFalse(self.proof([self.row(self.command, self.output + "0")]))

    def test_inline_runner_rejects_fixture_kit_or_later_target_rewrites(self):
        initial = self.row(self.command, self.output)
        self.assertFalse(self.proof([initial, self.row("Set-Content " + self.item["path"] + " fabricated", "", line=11)]))
        rewrite = "@'\nfrom pathlib import Path\nPath('" + self.item["path"] + "').write_bytes(b'changed')\n'@ | & '" + self.python.as_posix() + "' -"
        self.assertFalse(self.proof([initial, self.row(rewrite, "", line=11)]))
        fixture_path = self.root / case.INPUTS / "fixture.json"
        original = fixture_path.read_bytes()
        fixture_path.write_bytes(original + b" ")
        self.assertFalse(self.proof([initial]))
        fixture_path.write_bytes(original)
        (self.root / case.KIT / "scripts/pixl.py").write_text("changed runner")
        self.assertFalse(self.proof([initial]))

    def bash_setup(self):
        reads = {key: {"tool": tool, "arguments": args, "result_path": case.WORK + "/" + key.replace("_", "-") + ".json"}
                 for key, (tool, args) in case.READS.items()}
        self.fixture["reads"] = {**reads, **self.fixture["reads"]}
        for key, spec in reads.items():
            write_json(self.root / spec["result_path"], {"synthetic": key})
        write_json(self.root / case.INPUTS / "fixture.json", self.fixture)
        self.identity["inputs"][case.INPUTS + "/fixture.json"] = sha(self.root / case.INPUTS / "fixture.json")
        self.key = "plar_ready"
        self.target = self.root / self.fixture["reads"][self.key]["result_path"]
        self.item = {"path": self.target.relative_to(self.root).as_posix(), "sha256": sha(self.target)}
        command = (grader.bash_prefix(self.root, self.python, self.fixture) + "\"$PY\" -I - <<'EOF'\n"
                   + grader.BASH_VALIDATOR.rstrip() + "\nEOF\nls -la work/asset-lineage")
        lines = ["ROOT=" + self.root.as_posix(), *["plar-" + role + " exit=0" for role in case.MEMBERS],
                 *[key.replace("_", "-") + " exit=0" for key in case.SOURCES], "=== validate JSON + sizes ==="]
        lines += [Path(spec["result_path"]).stem + " " + str((self.root / spec["result_path"]).stat().st_size)
                  + " " + sha(self.root / spec["result_path"]) + " json-ok keys=synthetic" for spec in self.fixture["reads"].values()]
        return command, "\n".join(lines)

    def bash_proof(self, rows):
        return grader.bash_fixture_proof([rows], self.root, self.fixture, self.identity, self.python, self.key, self.item)

    def test_exact_direct_bash_batch_and_read_only_hash_trailer_are_bound(self):
        command, output = self.bash_setup()
        self.assertTrue(self.bash_proof([self.row(command, output)]))
        self.assertFalse(self.bash_proof([{"file": "synthetic-native.jsonl", "line": 10,
                                          "message": {"content": command + output}}]))

    def test_bash_rejects_fake_commands_mutating_trailer_wrong_args_and_failures(self):
        command, output = self.bash_setup()
        for before, after in (('"$PY" -I "$R" plar read', 'echo "$PY" -I "$R" plar read'),
                              ('--asset "queue.$a"', '--asset "wrong.$a"'),
                              ('p.read_bytes()', "p.write_bytes(b'fabricated')"),
                              ('> "work/asset-lineage/plar-$a.json"', '> "wrong-$a.json"')):
            self.assertFalse(self.bash_proof([self.row(command.replace(before, after), output)]))
        self.assertFalse(self.bash_proof([self.row(command, output, code=1)]))
        self.assertFalse(self.bash_proof([self.row(command, output.replace("plar-ready exit=0", "plar-ready exit=1"))]))

    def test_bash_rejects_missing_or_wrong_hash_receipts_and_later_rewrites(self):
        command, output = self.bash_setup()
        self.assertFalse(self.bash_proof([self.row(command, output.replace(self.item["sha256"], "0" * 64))]))
        self.assertFalse(self.bash_proof([self.row(command, "\n".join(line for line in output.splitlines() if "plar-ready " not in line))]))
        self.assertFalse(self.bash_proof([self.row(command, output), self.row("Set-Content " + self.item["path"] + " fabricated", "", line=11)]))

    def test_complete_first_read_survives_only_distinct_later_missing_read(self):
        second = self.root / case.WORK / "not-yet-written.json"
        command = "Get-Content -Raw '" + self.item["path"] + "'; Get-Content -Raw '" + second.relative_to(self.root).as_posix() + "'"
        output = self.target.read_text() + "\nGet-Content: Cannot find path '" + str(second) + "' because it does not exist."
        self.assertTrue(grader.viewed([[self.row(command, output, code=1)]], self.target))
        for changed_command, changed_output in (
                (command, output.replace("synthetic", "altered", 1)),
                (command, output.split("Get-Content:")[0]),
                (command, output[10:]),
                (command.replace(self.item["path"], "wrong.json", 1), output),
                (command.replace(second.relative_to(self.root).as_posix(), self.item["path"]), output),
                ("Write-Output 'pretend'; " + command, output)):
            self.assertFalse(grader.viewed([[self.row(changed_command, changed_output, code=1)]], self.target))


class AssetLineageContinuationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="lineage same child ")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.root, self.attempt, self.resumed = (self.base / name for name in ("consumer", "attempt", "resumed"))
        for directory in (self.root / case.WORK, self.attempt / "native-transcripts", self.resumed / "native-transcripts"):
            directory.mkdir(parents=True)
        config = self.base / "config.json"
        write_json(config, {"host": "unchanged"})
        configuration = {"host": case.reference(config)}
        source = self.root / case.WORK / "original-read.json"
        write_json(source, {"original": True})
        (self.attempt / "outputs").mkdir()
        (self.attempt / "outputs/original-read.json").write_bytes(source.read_bytes())
        self.original_child = self.attempt / "native-transcripts/selected-child.jsonl"
        self.resumed_child = self.resumed / "native-transcripts/selected-child.jsonl"
        self.original_child.write_bytes(b'{"original_native_record":true}\n')
        self.resumed_child.write_bytes(self.original_child.read_bytes() + b'{"continued_native_record":true}\n')
        write_json(self.attempt / "launch.json", {"host": "claude", "cwd": str(self.root)})
        prior = {"host": "claude", "cwd": str(self.root), "session_id": "same-parent", "children": [{"id": "selected-child", "role": "pixl:pixl"}],
                 "calls": [], "inputs": {}, "configuration": configuration, "status": "finished", "returncode": 0,
                 "retained_transcripts": {"selected-child": case.reference(self.original_child)}, "artifacts": [case.reference(source)]}
        write_json(self.attempt / "continuation.json", prior)
        predecessor = case.reference(self.attempt / "continuation.json")
        launch = {"host": "claude", "cwd": str(self.root), "predecessor": predecessor, "continuation_mode": "native_same_session",
                  "expected_session_id": "same-parent", "expected_child_id": "selected-child"}
        write_json(self.resumed / "launch.json", launch)
        write_json(self.resumed / "identity.json", {"predecessor": predecessor, "original_consumer": str(self.root),
                                                   "session_id": "same-parent", "child_id": "selected-child"})
        self.current = {"host": "claude", "cwd": str(self.root), "predecessor": predecessor, "mode": "native_same_session",
                        "expected_session_id": "same-parent", "expected_child_id": "selected-child", "session_id": "same-parent",
                        "observed_expected_session": True, "children": [], "calls": [], "inputs": {}, "configuration": configuration,
                        "retained_transcripts": {"selected-child": case.reference(self.resumed_child)},
                        "status": "finished", "returncode": 0, "interruption_reason": None}
        write_json(self.resumed / "continuation.json", self.current)

    def check(self, child="selected-child"):
        return grader.continuation_checks(self.attempt, self.resumed, self.root, child)

    def test_same_identity_additive_child_prefix_and_original_reports_are_preserved(self):
        before = inventory(self.attempt)
        combined, checks = self.check()
        self.assertTrue(all(row["pass"] for row in checks))
        self.assertEqual(combined["children"], [{"id": "selected-child", "role": "pixl:pixl"}])
        self.assertEqual(inventory(self.attempt), before)
        # Identity aggregation never substitutes for an actual child completion.
        self.assertEqual(grader.claude_completion([], "selected-child"), [])

    def test_unrecorded_child_journal_cannot_contribute_native_proof(self):
        stray = self.resumed / "native-transcripts/agent-selected-child.jsonl"
        stray.write_bytes(b'{"unrecorded_extra_proof":true}\n')
        for directory in (self.attempt, self.resumed):
            (directory / "stdout.jsonl").write_bytes(b"")
        caller = {"native_child": {"agent_type": "pixl:pixl", "agent_id": "selected-child"}}
        with patch.object(grader, "claude_loading_proof", return_value={}):
            _, children, _, qualified, _, _ = grader.native_partitions(
                self.attempt, self.root, {"host": "claude"}, self.current, caller, self.resumed)
        self.assertEqual(len(children), 2)
        self.assertFalse(qualified)
        self.assertFalse(any("unrecorded_extra_proof" in row for journal in children for row in journal))
        self.resumed_child.write_bytes(b"tampered native snapshot")
        with patch.object(grader, "claude_loading_proof", return_value={}), self.assertRaisesRegex(ValueError, "exact retained"):
            grader.native_partitions(self.attempt, self.root, {"host": "claude"}, self.current, caller, self.resumed)

    def test_wrong_child_predecessor_root_or_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            self.check("different-child")
        for field, value in (("session_id", "different-parent"), ("cwd", str(self.base / "wrong-root")),
                             ("predecessor", {"path": "wrong", "sha256": "0" * 64}), ("configuration", {})):
            current = copy.deepcopy(self.current)
            current[field] = value
            write_json(self.resumed / "continuation.json", current)
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.check()
        write_json(self.resumed / "continuation.json", self.current)

    def test_overwritten_report_or_child_prefix_cannot_be_accepted(self):
        (self.root / case.WORK / "original-read.json").write_bytes(b"changed original output")
        _, checks = self.check()
        self.assertFalse(next(row["pass"] for row in checks if row["check"] == "all_predecessor_reports_preserved"))
        self.resumed_child.write_bytes(b'{"substituted_prefix":true}\n')
        self.current["retained_transcripts"]["selected-child"] = case.reference(self.resumed_child)
        write_json(self.resumed / "continuation.json", self.current)
        _, checks = self.check()
        self.assertFalse(next(row["pass"] for row in checks if row["check"] == "same_child_transcript_preserves_exact_prefix_and_adds_native_records"))
        (self.attempt / "outputs/original-read.json").write_bytes(b"rewritten retained history")
        with self.assertRaisesRegex(ValueError, "immutable native artifact"):
            self.check()


class AssetLineageReportProofTests(unittest.TestCase):
    def setUp(self):
        self.cache = "installed pixl/runtime/pixl/__pycache__/service.cpython-314.pyc"
        self.child = {"claim": True, "state_hash_at_every_read": "state", "revision_at_every_read": 108,
                      "validate_after_work": {"hash": "state", "revision": 108, "matches": True},
                      "files_modified_outside_work_asset_lineage_since_fixture": [self.cache]}
        self.caller = {"original_bytes_unchanged": True, "baseline_files": 10, "current_files": 11,
                       "changed": [], "removed": [], "added_other": [], "added_outside_work_asset_lineage": [self.cache],
                       "state_px_sha256_now": "state", "state_px_sha256_baseline": "state"}

    def accepted(self, value, independent=True):
        return grader.preservation_claim(value, independent, "state", 108)

    def test_observed_preservation_layouts_need_independent_bytes_and_exact_state(self):
        self.assertTrue(self.accepted(self.child))
        self.assertTrue(self.accepted(self.caller))
        for original in (self.child, self.caller):
            self.assertFalse(self.accepted(original, independent=False))
            for field, value in (("unchanged", False), ("state_changed_reported", True),
                                 ("canonical_state", {"state_hash": "wrong"}), ("results", {"file_set_drift": 1})):
                modified = copy.deepcopy(original)
                modified[field] = value
                self.assertFalse(self.accepted(modified))

    def test_false_claim_hash_revision_validation_or_noncache_mutation_is_rejected(self):
        for field, value in (("claim", False), ("state_hash_at_every_read", "wrong"), ("revision_at_every_read", 109),
                             ("validate_after_work", {"hash": "state", "revision": 108, "matches": False}),
                             ("validate_after_work", {"hash": "wrong", "revision": 108, "matches": True}),
                             ("validate_after_work", {"hash": "state", "revision": 109, "matches": True})):
            modified = copy.deepcopy(self.child)
            modified[field] = value
            self.assertFalse(self.accepted(modified))
        for field, value in (("original_bytes_unchanged", False), ("changed", ["source.py"]), ("removed", ["art.png"]),
                             ("added_other", ["state.px"]), ("state_px_sha256_now", "wrong"),
                             ("state_px_sha256_baseline", "wrong"), ("current_files", 12),
                             ("authoring_plar_sha256_now", "unverified")):
            modified = copy.deepcopy(self.caller)
            modified[field] = value
            self.assertFalse(self.accepted(modified))
        for path in ("installed pixl/runtime/pixl/service.py", "../installed pixl/runtime/pixl/__pycache__/x.pyc",
                     "installed pixl/runtime/pixl/__pycache__/../x.pyc", "C:/installed pixl/runtime/pixl/__pycache__/x.pyc",
                     "other/__pycache__/x.pyc"):
            for original, field in ((self.child, "files_modified_outside_work_asset_lineage_since_fixture"),
                                    (self.caller, "added_outside_work_asset_lineage")):
                modified = copy.deepcopy(original)
                modified[field] = [path]
                self.assertFalse(self.accepted(modified))

    def test_result_reference_wrapper_does_not_hide_conflicting_aliases(self):
        item = {"path": "actual.json", "sha256": "hash"}
        self.assertEqual(grader.ref({"tool": "pixl_review_context", "result": item}), item)
        with self.assertRaises(ValueError):
            grader.ref({"result": item, "reference": {"path": "other.json", "sha256": "hash"}})
        with self.assertRaises(ValueError):
            grader.ref({"result": item, "path": "other.json", "sha256": "hash"})

    def test_native_completion_requires_start_successful_revival_and_completed_notification(self):
        parent = [
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "resume-call", "name": "SendMessage", "input": {"to": "child"}}]}},
            {"type": "system", "subtype": "task_started", "session_id": "parent", "task_id": "child", "run_id": "run", "tool_use_id": "resume-call",
             "subagent_type": "pixl:pixl", "task_type": "local_agent"},
            {"type": "user", "tool_use_result": {"success": True, "resumedAgentId": "child", "revivedAgentId": "child"},
             "message": {"content": [{"type": "tool_result", "tool_use_id": "resume-call"}]}},
            {"type": "system", "subtype": "task_notification", "session_id": "parent", "task_id": "child", "run_id": "run", "tool_use_id": "resume-call", "status": "completed"},
        ]
        self.assertTrue(grader.resumed_completion(parent, "child", "parent"))
        for index in range(len(parent)):
            self.assertFalse(grader.resumed_completion(parent[:index] + parent[index + 1:], "child", "parent"))
        for index, field, value in ((3, "status", "stopped"), (3, "run_id", "other"), (3, "task_id", "other"),
                                    (3, "session_id", "other"), (3, "tool_use_id", "other"), (3, "type", "assistant"),
                                    (1, "subagent_type", "default")):
            changed = copy.deepcopy(parent)
            changed[index][field] = value
            self.assertFalse(grader.resumed_completion(changed, "child", "parent"))
        changed = copy.deepcopy(parent)
        changed[2]["tool_use_result"]["success"] = False
        self.assertFalse(grader.resumed_completion(changed, "child", "parent"))


if __name__ == "__main__":
    unittest.main()
