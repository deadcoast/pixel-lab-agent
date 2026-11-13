"""TM-08 evidence confusion regressions; synthetic native traces do not qualify hosts."""

from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import domain_consumer_case as case
from evaluations import grade_domain_consumers as grader
from evaluations.host_trials import inventory, sha
from pixl import consumer_execution


def async_fixture():
    child, session, call_id, run_id = "selected-child", "parent-session", "agent-call", "background-run"
    text = "Bound final child result, not a parent-written completion claim."
    call = {"type": "tool_use", "name": "Agent", "id": call_id,
            "input": {"subagent_type": "pixl:pixl", "run_in_background": True}}
    result = {"type": "tool_result", "tool_use_id": call_id, "content": "Launched", "is_error": False}
    launch = {"status": "async_launched", "isAsync": True, "agentId": child}
    stdout = [
        {"type": "assistant", "message": {"content": [call]}},
        {"type": "system", "subtype": "task_started", "task_id": child, "tool_use_id": call_id,
         "run_id": run_id, "subagent_type": "pixl:pixl", "is_backgrounded": True},
        {"type": "user", "message": {"content": [result]}, "tool_use_result": launch},
        {"type": "system", "subtype": "task_updated", "task_id": child, "run_id": run_id, "patch": {"status": "completed"}},
        {"type": "system", "subtype": "task_notification", "task_id": child, "tool_use_id": call_id,
         "run_id": run_id, "status": "completed", "summary": text},
        {"type": "result", "subtype": "success", "terminal_reason": "completed", "is_error": False,
         "subagent_stats": {"completed": 1, "failed": 0}},
    ]
    parent = [
        {"type": "assistant", "message": {"content": [copy.deepcopy(call)]}},
        {"type": "user", "message": {"content": [copy.deepcopy(result)]}, "toolUseResult": copy.deepcopy(launch)},
        {"type": "user", "isSidechain": False, "promptSource": "system", "turnOrigin": "task_notification",
         "origin": {"kind": "task-notification", "producer": "session-task", "runId": run_id},
         "message": {"content": "<task-notification>\n" + f"<task-id>{child}</task-id>\n<tool-use-id>{call_id}</tool-use-id>\n"
                     + f"<status>completed</status>\n<result>{text}</result>\n</task-notification>"}},
    ]
    children = [[{"type": "assistant", "agentId": child, "sessionId": session, "isSidechain": True,
                  "message": {"stop_reason": "end_turn", "content": [{"type": "text", "text": text}]},
                  "file": "child.jsonl", "line": 1}]]
    for journal, key, name in ((stdout, "session_id", "stdout.jsonl"), (parent, "sessionId", "parent.jsonl")):
        for index, row in enumerate(journal, 1):
            row.update({key: session, "file": name, "line": index})
    return stdout, parent, children, child, session


class DomainConsumerGradeTests(unittest.TestCase):
    def test_exact_two_operation_references_are_required(self):
        valid = {"operations": {domain: {"path": domain + ".json", "sha256": "a" * 64} for domain in case.PROFILES}}
        self.assertEqual(grader.operations(valid), valid["operations"])
        wrapped = {"operations": {domain: {"result": ref, "status": "complete"} for domain, ref in valid["operations"].items()}}
        self.assertEqual(grader.operations(wrapped), valid["operations"])
        wrapped["operations"]["terrain"]["path"] = "different.json"
        with self.assertRaises(ValueError):
            grader.operations(wrapped)
        for operations in ({"terrain": valid["operations"]["terrain"]}, {**valid["operations"], "queue": {}},
                           {"terrain": "terrain.json", "animation": valid["operations"]["animation"]}):
            with self.subTest(operations=operations), self.assertRaises(ValueError):
                grader.operations({"operations": operations})

    def test_reported_child_identity_rejects_conflicting_aliases_and_roles(self):
        valid = {"agent_id": "child", "agent_type": "pixl:pixl"}
        self.assertEqual(grader.child_identity(valid, "claude"), "child")
        for extra in ({"canonical_task": "other"}, {"role": "default"}, {"child_id": "other"}):
            self.assertIsNone(grader.child_identity({**valid, **extra}, "claude"))
        codex = {"task_name": "/root/pixl-task", "agent_type": "pixl", "fork_turns": "none"}
        self.assertEqual(grader.child_identity(codex, "codex"), "/root/pixl-task")
        self.assertIsNone(grader.child_identity({**codex, "fork_turns": "all"}, "codex"))

    def test_observed_result_file_annotation_preserves_exact_reference_and_rejects_conflicts(self):
        refs = {domain: {"path": domain + ".json", "sha256": "a" * 64} for domain in case.PROFILES}
        actual = {"operations": {domain: {"result_file": ref, "returned_status": "complete"} for domain, ref in refs.items()}}
        self.assertEqual(grader.operations(actual), refs)
        for changes in ({"path": "different.json"}, {"sha256": "b" * 64},
                        {"result": {"path": "terrain.json", "sha256": "b" * 64}},
                        {"result_file": "terrain.json"}):
            modified = copy.deepcopy(actual)
            modified["operations"]["terrain"].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                grader.operations(modified)

    def test_async_completion_binds_named_call_launch_host_events_and_child_final(self):
        proof = grader.claude_async_completion(*async_fixture())
        self.assertEqual(len(proof), 1)
        self.assertEqual(proof[0]["mechanism"], "bound_async_host_completion")
        self.assertEqual(proof[0]["run_id"], "background-run")

    def test_unrelated_text_tool_results_do_not_hide_or_supply_async_completion(self):
        args = async_fixture()
        args[0].insert(3, {"type": "user", "session_id": args[4], "tool_use_result": "ordinary tool output"})
        args[1].insert(2, {"type": "user", "sessionId": args[4], "toolUseResult": "ordinary tool output"})
        self.assertTrue(grader.claude_async_completion(*args))
        args[0][2]["tool_use_result"] = "async_launched selected-child"
        self.assertEqual(grader.claude_async_completion(*args), [])

    def test_async_launch_without_actual_completion_never_qualifies(self):
        stdout, parent, children, child, session = async_fixture()
        for missing in (1, 2, 3, 4, 5):
            with self.subTest(missing=missing):
                self.assertEqual(grader.claude_async_completion([row for i, row in enumerate(stdout) if i != missing], parent, children, child, session), [])

    def test_async_wrong_identity_role_session_or_run_never_qualifies(self):
        cases = [("stdout", 0, "session_id", "other"), ("stdout", 1, "subagent_type", "general-purpose"),
                 ("stdout", 1, "task_id", "other"), ("stdout", 1, "tool_use_id", "other"),
                 ("stdout", 3, "run_id", "other"), ("stdout", 4, "task_id", "other"),
                 ("stdout", 4, "session_id", "other"), ("stdout", 4, "tool_use_id", "other"),
                 ("stdout", 4, "summary", "Parent-invented summary"), ("parent", 2, "promptSource", "user"),
                 ("parent", 2, "turnOrigin", "message"), ("parent", 2, "sessionId", "other"),
                 ("parent", 2, "isSidechain", True)]
        for journal, index, field, value in cases:
            args = async_fixture()
            args[0 if journal == "stdout" else 1][index][field] = value
            with self.subTest(journal=journal, field=field):
                self.assertEqual(grader.claude_async_completion(*args), [])
        for field, value in (("agentId", "other"), ("sessionId", "other"), ("isSidechain", False)):
            args = async_fixture()
            args[2][0][0][field] = value
            with self.subTest(field=field):
                self.assertEqual(grader.claude_async_completion(*args), [])

    def test_async_parent_prose_duplicate_tags_and_wrong_event_order_do_not_qualify(self):
        for mode in ("prose", "duplicate", "wrong-result", "order", "wrong-origin", "failed"):
            args = async_fixture()
            if mode == "prose":
                args[1][2].update(type="assistant", promptSource="assistant")
            elif mode == "duplicate":
                args[1][2]["message"]["content"] = args[1][2]["message"]["content"].replace("<status>", "<status>completed</status><status>")
            elif mode == "wrong-result":
                args[1][2]["message"]["content"] = args[1][2]["message"]["content"].replace("Bound final child result", "Invented")
            elif mode == "order":
                args[0][3], args[0][4] = args[0][4], args[0][3]
            elif mode == "wrong-origin":
                args[1][2]["origin"]["runId"] = "other"
            else:
                args[0][-1]["subagent_stats"]["failed"] = 1
            with self.subTest(mode=mode):
                self.assertEqual(grader.claude_async_completion(*args), [])

    def test_missing_attempt_evidence_is_failed_grade(self):
        with tempfile.TemporaryDirectory() as folder:
            result = grader.grade(folder)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["passed"], 0)

    def test_started_image_view_is_not_actual_completed_viewing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            image = root / "capture.png"
            image.write_bytes(b"fixture identity only")
            item = {"type": "ImageView", "id": "view-one", "path": str(image), "status": "in_progress"}
            journal = [{"type": "event_msg", "payload": {"type": "item_started", "item": item}}]
            self.assertEqual(grader.completed_image_views([journal], root), {})
            del item["status"]
            journal[0]["payload"]["type"] = "item_completed"
            self.assertIn(sha(image), grader.completed_image_views([journal], root))

    def test_failed_image_view_cannot_supply_viewing_even_with_completed_event(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            image = root / "capture.png"
            image.write_bytes(b"fixture identity only")
            for event in ("item_failed", "item_completed"):
                item = {"type": "ImageView", "id": "view-one", "path": str(image), "status": "failed"}
                journal = [{"type": "event_msg", "payload": {"type": event, "item": item}}]
                with self.subTest(event=event):
                    self.assertEqual(grader.completed_image_views([journal], root), {})

    def test_authored_contract_requires_literal_export_and_exact_function_boundary(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "src").mkdir()
            path = root / "src/terrain.ts"
            valid = 'export const terrain = {"neighborhoods": ["all", "island"]};\n\nexport function tileFor(corners) {}\n'
            path.write_text(valid, encoding="utf-8")
            self.assertEqual(grader.authored_contract(root, "terrain"), {"neighborhoods": ["all", "island"]})
            for source in (valid.replace("export const terrain", "const terrain"),
                           valid.replace(";\n\nexport function", "; sideEffect();\n\nexport function"),
                           valid.replace("tileFor", "otherFunction")):
                path.write_text(source, encoding="utf-8")
                with self.assertRaises(ValueError):
                    grader.authored_contract(root, "terrain")


class DomainConsumerArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        node = shutil.which("node")
        candidates = [Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
                      Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
                      Path("/usr/bin/chromium"), Path("/usr/bin/google-chrome")]
        browser = next((path for path in candidates if path.is_file()), None)
        if not node or not browser:
            raise unittest.SkipTest("Installed Node/Chromium unavailable")
        temporary = tempfile.TemporaryDirectory(prefix="tm08 frozen grader ")
        cls.addClassCleanup(temporary.cleanup)
        cls.root = Path(temporary.name).resolve()
        case.project(cls.root)
        resources = cls.root / case.KIT / "resources"
        source = Path(__file__).resolve().parents[1] / "examples/consumer-execution"
        for directory in grader.RESOURCES.values():
            location = resources / "examples/consumer-execution" / directory
            location.mkdir(parents=True)
            for filename in grader.PROFILE_FILES:
                shutil.copyfile(source / directory / filename, location / filename)
        cls.identity = {"package_files": inventory(cls.root / case.KIT)}
        cls.results, cls.captures = {}, {}
        with patch.object(consumer_execution.service, "resource_root", return_value=resources):
            for domain in case.PROFILES:
                result = consumer_execution.execute(cls.root / case.state(domain), cls.root, grader.CANDIDATE,
                    case.config(domain), f"{case.WORK}/{domain}-01", node=node, browser=str(browser))
                if result["status"] != "complete":
                    raise AssertionError(json.dumps(result))
                cls.results[domain] = result
                cls.captures[domain] = json.loads((cls.root / result["artifacts"]["capture/capture.json"]["path"]).read_bytes())

    def test_independent_frozen_checkers_reproduce_both_real_public_pipeline_archives(self):
        for domain, result in self.results.items():
            with self.subTest(domain=domain):
                checks, capture = grader.artifact_checks(self.root, self.identity, result, domain)
                self.assertTrue(all(row["pass"] for row in checks), [row for row in checks if not row["pass"]])
                self.assertEqual(capture, self.captures[domain])

    def test_frozen_profile_rejects_wrong_profile_and_changed_installed_or_copied_bytes(self):
        for domain, result in self.results.items():
            with self.subTest(domain=domain):
                other = "animation" if domain == "terrain" else "terrain"
                with self.assertRaises(ValueError):
                    grader.frozen_recheck(self.root, self.identity, result, other)
                provenance = json.loads((self.root / result["artifacts"]["renderer-sources.json"]["path"]).read_bytes())
                for key in ("resource", "copy"):
                    path = self.root / provenance[0][key]
                    original = path.read_bytes()
                    try:
                        path.write_bytes(original + b"\n// changed\n")
                        with self.assertRaises(ValueError):
                            grader.frozen_recheck(self.root, self.identity, result, domain)
                    finally:
                        path.write_bytes(original)

    def test_frozen_identity_must_match_all_six_files(self):
        identity = copy.deepcopy(self.identity)
        identity["package_files"]["resources/examples/consumer-execution/tile-neighborhood/server.mjs"] = "0" * 64
        with self.assertRaises(ValueError):
            grader.frozen_recheck(self.root, identity, self.results["terrain"], "terrain")

    def test_capture_cannot_delete_authored_map_or_clip_even_if_frozen_checker_passes(self):
        for domain, result in self.results.items():
            checked, capture, out = grader.frozen_recheck(self.root, self.identity, result, domain)
            capture[domain]["neighborhoods" if domain == "terrain" else "clips"].pop()
            with patch.object(grader, "frozen_recheck", return_value=(checked, capture, out)):
                checks, _ = grader.artifact_checks(self.root, self.identity, result, domain)
            guard = next(row for row in checks if row["check"] == domain + ":captured_contract_equals_exact_authored_source")
            self.assertFalse(guard["pass"])

    def test_missing_served_display_module_fails_independent_frozen_trial_guard(self):
        for domain, result in self.results.items():
            checked, capture, out = grader.frozen_recheck(self.root, self.identity, result, domain)
            del capture["served_files"]["renderer/view.mjs"]
            with patch.object(grader, "frozen_recheck", return_value=(checked, capture, out)):
                checks, _ = grader.artifact_checks(self.root, self.identity, result, domain)
            guard = next(row for row in checks if row["check"] == domain + ":actual_required_display_module_and_assets_served")
            self.assertFalse(guard["pass"])
            self.assertEqual(guard["evidence"]["missing"], ["renderer/view.mjs"])

    def test_complete_flag_cannot_hide_failed_browser_cleanup(self):
        for domain, original_result in self.results.items():
            result = copy.deepcopy(original_result)
            checked, capture, out = grader.frozen_recheck(self.root, self.identity, result, domain)
            reference = result["artifacts"]["capture/execution.json"]
            path = self.root / reference["path"]
            original = path.read_bytes()
            try:
                execution = json.loads(original)
                execution["cleanup"]["browser_closed"] = False
                path.write_text(json.dumps(execution), encoding="utf-8")
                reference["sha256"] = sha(path)
                # Simulate a permissive old checker and already-consistent archive
                # to isolate the independent cleanup guard under review.
                with patch.object(grader, "frozen_recheck", return_value=(checked, capture, out)), patch.object(grader, "bundle_errors", return_value=[]):
                    checks, _ = grader.artifact_checks(self.root, self.identity, result, domain)
                guard = next(row for row in checks if row["check"] == domain + ":actual_owned_browser_server_profile_cleanup")
                self.assertFalse(guard["pass"])
            finally:
                path.write_bytes(original)

    def test_every_context_and_scale_needs_actual_and_reported_image_views(self):
        for domain, capture in self.captures.items():
            images = {view["image"]["sha256"] for view in capture["views"]}
            screenshots = {view["screenshot"]["sha256"] for view in capture["views"]}
            self.assertTrue(grader.viewing_coverage(capture, domain, images, images)["pass"])
            self.assertTrue(grader.viewing_coverage(capture, domain, screenshots, screenshots)["pass"])
            self.assertFalse(grader.viewing_coverage(capture, domain, set(), images)["pass"])
            self.assertFalse(grader.viewing_coverage(capture, domain, images, set())["pass"])
            reduced = {view["image"]["sha256"] for view in capture["views"] if view["scale"] == 1}
            self.assertFalse(grader.viewing_coverage(capture, domain, reduced, reduced)["pass"])

    def test_incomplete_or_repeated_frozen_closure_refused_before_checker_execution(self):
        result = copy.deepcopy(self.results["terrain"])
        path = self.root / result["artifacts"]["renderer-sources.json"]["path"]
        original = path.read_bytes()
        provenance = json.loads(original)
        try:
            for value in (provenance[:-1], provenance[:-1] + [provenance[0]]):
                path.write_text(json.dumps(value), encoding="utf-8")
                result["artifacts"]["renderer-sources.json"]["sha256"] = sha(path)
                with self.assertRaisesRegex(ValueError, "Incomplete or duplicate"):
                    grader.frozen_recheck(self.root, self.identity, result, "terrain")
        finally:
            path.write_bytes(original)
