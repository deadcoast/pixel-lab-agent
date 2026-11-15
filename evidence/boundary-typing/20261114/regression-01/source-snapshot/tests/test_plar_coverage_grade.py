import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import grade_plar_coverage as grader
from evaluations.host_trials import inventory, sha, write_json
from pixl import service

ROOT = Path(__file__).resolve().parents[1]


def event(tool, arguments, result, *, status="completed", line=1, file="child", success=True):
    return {"file": file, "line": line, "payload": {"type": "item_completed", "item": {
        "id": f"call-{line}", "type": "McpToolCall", "server": "pixl_local", "tool": tool,
        "status": status, "arguments": arguments, "result": {"isError": not success, "structuredContent": result}}}}


class PLARCoverageGradeTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="plar coverage grade ")
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.root, self.attempt = self.base / "consumer", self.base / "attempt"
        shutil.copytree(ROOT / "evidence/plar-allocation/20261108/local-probe", self.root)
        self.attempt.mkdir()
        self.before = json.loads((self.root / "plar.txt").read_bytes())
        self.original = inventory(self.root)
        files = {
            "SOURCE-MAP.md": "Scoped overview: source inspection only; remote badges unavailable; renderer not inspected.\n",
            "src/start-shortcut.mjs": 'import { statusCell } from "./queue-view.ts";\nexport function startShortcut() { return statusCell("idle"); }\n',
            "src/shortcut-entry.mjs": 'import { startShortcut } from "./start-shortcut.mjs";\nexport function shortcutEntry() { return startShortcut(); }\nconsole.log(JSON.stringify(shortcutEntry()));\n',
            "uninspected/renderer-view.mjs": "// Present renderer kept outside this assignment's inspection boundary.\n" + "const present = true;\n" * 6,
        }
        for name, text in files.items():
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        self.fixture = {"changed_asset": "queue.start", "unaffected_assets": ["queue.working", "queue.ready", "queue.retry"],
            "new_consumers": [{"path": "src/start-shortcut.mjs", "symbol": "startShortcut", "state": "idle"},
                              {"path": "src/shortcut-entry.mjs", "symbol": "shortcutEntry", "state": "idle"}],
            "uninspected": ["uninspected/renderer-view.mjs"], "existing_path": "assets/start.svg",
            "missing_paths": ["assets/working.png", "assets/ready.png", "assets/retry.png"]}
        self.after = copy.deepcopy(self.before)
        start = next(a for a in self.after["assets"] if a["id"] == "queue.start")
        for index, consumer in enumerate(self.fixture["new_consumers"]):
            ident = f"shortcut{index}"
            self.after["sources"].append({"id": ident, "path": consumer["path"], "sha256": sha(self.root / consumer["path"])})
            start["consumers"].append({"source": ident, "symbol": consumer["symbol"], "usage": "Existing Start descriptor selected for idle; preserve vector"})

    def source_event(self, name, **kwargs):
        count = len((self.root / name).read_text(encoding="utf-8").splitlines())
        args = {"path": name, "expect": sha(self.root / name), "start": 1, "end": count}
        return event("pixl_source", args, service.call("pixl_source", args, self.root), **kwargs)

    def reports(self):
        cases = []
        for classification in ("existing", "reused"):
            cases.append({"id": classification, "classification": classification, "inspection": "inspected",
                "consumers": self.fixture["new_consumers"] if classification == "reused" else [{"path": "src/queue-view.ts", "symbol": "statusVisuals.idle"}],
                "file": {"path": "assets/start.svg", "sha256": sha(self.root / "assets/start.svg")}, "limitation": "Source/SVG inspection, not rendered acceptance"})
        for name in self.fixture["missing_paths"]:
            cases.append({"id": name, "classification": "missing", "inspection": "unavailable", "consumers": [],
                          "file": {"path": name}, "limitation": "Referenced destination is absent; no generation performed"})
        cases.extend([
            {"id": "badge", "classification": "dynamic", "inspection": "inspected", "consumers": [{"path": "src/queue-view.ts", "symbol": "accountBadge"}],
             "limitation": "Lookup code inspected; remote registry unavailable and not enumerated"},
            {"id": "renderer", "classification": "uninspected", "inspection": "not_inspected", "consumers": [],
             "file": {"path": self.fixture["uninspected"][0], "sha256": sha(self.root / self.fixture["uninspected"][0])},
             "limitation": "Present renderer remains outside inspection boundary"}])
        files = [{"path": p, "sha256": sha(self.root / p), "inspection": "inspected", "symbols": []} for p in grader.CHILD_SOURCES]
        files.append({"path": self.fixture["uninspected"][0], "sha256": sha(self.root / self.fixture["uninspected"][0]), "inspection": "not_inspected", "symbols": []})
        mappings = []
        for state, asset in grader.STATES.items():
            consumers = [{"path": "src/queue-view.ts", "symbol": s} for s in ("statusCell", "compactStatus")]
            if state == "idle":
                consumers += [{"path": c["path"], "symbol": c["symbol"]} for c in self.fixture["new_consumers"]]
            row = {"state": state, "asset_id": asset, "consumers": consumers}
            if state in grader.TRANSITIONS:
                row["transition"] = {"path": "src/queue.ts", "symbol": "stateAfter", "input": grader.TRANSITIONS[state]}
            mappings.append(row)
        return {"rows": cases, "limits": ["Scoped source frontier, retained shared-view drift, no render acceptance"]}, {
            "files": files, "mappings": mappings, "limits": ["No exhaustive semantic or remote-registry coverage"]}

    def test_guarded_reuse_preserves_populated_unrelated_rows_and_old_drift(self):
        self.assertEqual(grader.allocation_errors(self.before, self.after, self.fixture, self.root), [])
        changed = copy.deepcopy(self.after)
        changed["assets"][0]["evidence"] = []
        self.assertTrue(grader.allocation_errors(self.before, changed, self.fixture, self.root))
        changed = copy.deepcopy(self.after)
        changed["sources"][1]["sha256"] = sha(self.root / "src/queue-view.ts")
        self.assertTrue(grader.allocation_errors(self.before, changed, self.fixture, self.root))

    def test_duplicate_asset_or_unrelated_source_cannot_substitute_for_reuse(self):
        changed = copy.deepcopy(self.after)
        changed["assets"].append({**changed["assets"][-1], "id": "shortcut.new"})
        self.assertTrue(grader.allocation_errors(self.before, changed, self.fixture, self.root))
        changed = copy.deepcopy(self.after)
        start = next(a for a in changed["assets"] if a["id"] == "queue.start")
        start["requirements"].append({"property": "palette", "value": "red only", "authority": "requirement", "sources": ["shortcut0"], "reason": "Invented artistic constraint"})
        self.assertTrue(grader.allocation_errors(self.before, changed, self.fixture, self.root))
        start["requirements"][-1].update(property="reuse", value="Existing idle Start descriptor", authority="observation", reason="New consumer retains existing role")
        start["requirements"][-1]["sources"].append("view")
        self.assertEqual(grader.allocation_errors(self.before, changed, self.fixture, self.root), [])
        changed = copy.deepcopy(self.after)
        changed["sources"].append({"id": "unrelated", "path": self.fixture["uninspected"][0], "sha256": sha(self.root / self.fixture["uninspected"][0])})
        self.assertTrue(grader.allocation_errors(self.before, changed, self.fixture, self.root))

    def test_native_source_proof_requires_success_and_exact_complete_returned_bytes(self):
        name = "src/start-shortcut.mjs"
        good = self.source_event(name)
        self.assertTrue(grader.source_proofs(grader.successful_calls([[good]], self.root), self.root, name)["complete"])
        bad = copy.deepcopy(good)
        bad["payload"]["item"]["result"]["structuredContent"]["text"] = "self-authored claim"
        self.assertFalse(grader.source_proofs(grader.successful_calls([[bad]], self.root), self.root, name)["complete"])
        bad = self.source_event(name, status="failed", success=False)
        self.assertFalse(grader.source_proofs(grader.successful_calls([[bad]], self.root), self.root, name)["complete"])
        bad = copy.deepcopy(good)
        bad["payload"]["item"]["arguments"]["scope"] = "library"
        self.assertFalse(grader.source_proofs(grader.successful_calls([[bad]], self.root), self.root, name)["complete"])

    def test_split_reads_need_every_actual_line(self):
        name = "src/start-shortcut.mjs"
        args = {"path": name, "expect": sha(self.root / name), "start": 1, "end": 1}
        first = event("pixl_source", args, service.call("pixl_source", args, self.root))
        self.assertFalse(grader.source_proofs(grader.successful_calls([[first]], self.root), self.root, name)["complete"])
        args = {**args, "start": 2, "end": 2}
        second = event("pixl_source", args, service.call("pixl_source", args, self.root))
        self.assertTrue(grader.source_proofs(grader.successful_calls([[first, second]], self.root), self.root, name)["complete"])

    def test_mapping_and_present_uninspected_are_not_authored_pass_flags(self):
        coverage, source_map = self.reports()
        self.assertEqual(grader.coverage_errors(coverage, source_map, self.fixture, self.root), [])
        coverage["rows"][-2]["inspection"] = "unavailable"
        self.assertEqual(grader.coverage_errors(coverage, source_map, self.fixture, self.root), [])
        wrong = copy.deepcopy(source_map)
        wrong["mappings"][1]["transition"]["input"] = "ok"
        self.assertTrue(grader.coverage_errors(coverage, wrong, self.fixture, self.root))
        wrong = copy.deepcopy(coverage)
        wrong["rows"][-1]["inspection"] = "unavailable"
        self.assertTrue(grader.coverage_errors(wrong, source_map, self.fixture, self.root))
        contradictory = copy.deepcopy(coverage)
        contradictory["rows"].append({"id": "contradiction", "classification": "existing", "inspection": "inspected", "consumers": [],
                                      "file": {"path": "assets/ready.png"}, "limitation": "Claim"})
        self.assertTrue(grader.coverage_errors(contradictory, source_map, self.fixture, self.root))
        (self.root / "assets/ready.png").write_bytes(b"invented asset")
        self.assertTrue(grader.coverage_errors(coverage, source_map, self.fixture, self.root))

    def test_uninspected_audit_ignores_report_mentions_but_catches_content_tools(self):
        name = self.fixture["uninspected"][0]
        mention = {"file": "child", "line": 1, "payload": {"type": "message", "role": "assistant", "content": [{"text": name + " was not inspected"}]}}
        self.assertEqual(grader.uninspected_reads([[mention]], self.root, [name]), [])
        self.assertTrue(grader.uninspected_reads([[self.source_event(name)]], self.root, [name]))
        claude = {"file": "child", "line": 2, "message": {"content": [{"type": "tool_use", "name": "Read", "input": {"file_path": str(self.root / name)}}]}}
        self.assertTrue(grader.uninspected_reads([[claude]], self.root, [name]))
        for tool, args in (("Bash", {"command": "cat " + name}), ("Grep", {"path": name, "pattern": "present"})):
            claude["message"]["content"][0].update(name=tool, input=args)
            self.assertTrue(grader.uninspected_reads([[claude]], self.root, [name]))
        returned = {"message": {"content": [{"type": "tool_result", "content": (self.root / name).read_text(encoding="utf-8")}]}}
        self.assertTrue(grader.uninspected_reads([[returned]], self.root, [name]))
        hashed = {"message": {"content": [{"type": "tool_use", "name": "Bash", "input": {"command":
            "python -c \"import hashlib; from pathlib import Path; print(hashlib.sha256(Path('" + name + "').read_bytes()).hexdigest())\""}}]}}
        self.assertFalse(grader.uninspected_reads([[hashed]], self.root, [name]))
        hashed["message"]["content"][0]["input"]["command"] += "; cat " + name
        self.assertTrue(grader.uninspected_reads([[hashed]], self.root, [name]))

    def test_nonisolated_role_route_does_not_count_inherited_completion(self):
        parent = [{"type": "session_meta", "payload": {"id": "parent"}},
            {"line": 2, "file": "parent", "payload": {"type": "function_call", "namespace": "collaboration", "name": "spawn_agent",
                "call_id": "spawn", "arguments": json.dumps({"agent_type": "pixl", "fork_turns": "all"})}},
            {"line": 3, "file": "parent", "payload": {"type": "function_call_output", "call_id": "spawn", "output": '{"task_name":"/root/child"}'}}]
        child = [{"type": "session_meta", "file": "child", "payload": {"id": "child", "session_id": "parent", "parent_thread_id": "parent",
            "agent_role": "pixl", "agent_path": "/root/child", "forked_from_id": "parent", "subagent_history_start_ordinal": 10,
            "source": {"subagent": {"thread_spawn": {"parent_thread_id": "parent", "agent_role": "pixl", "agent_path": "/root/child"}}}}},
            {"line": 2, "file": "child", "ordinal": 2, "payload": {"type": "task_complete"}},
            {"line": 3, "file": "child", "ordinal": 9, "payload": {"type": "message", "role": "developer", "content": [{"text": "exact role"}]}}]
        self.assertFalse(grader.codex_role_proof([parent, child], "parent", "/root/child", "exact role")["loaded"])
        result = grader.codex_role_proof([parent, child], "parent", "/root/child", "exact role", require_isolated=False)
        self.assertTrue(result["loaded"])
        self.assertFalse(result["completed"])
        child.append({"line": 4, "file": "child", "ordinal": 11, "payload": {"type": "task_complete"}})
        self.assertTrue(grader.codex_role_proof([parent, child], "parent", "/root/child", "exact role", require_isolated=False)["completed"])
        self.assertFalse(grader.codex_role_proof([parent, child], "parent", "/root/wrong", "exact role", require_isolated=False)["loaded"])

    def test_claude_selected_child_cannot_borrow_another_child_completion(self):
        calls = [{"message": {"content": [{"type": "tool_use", "id": "b", "name": "Agent", "input": {"subagent_type": "pixl:pixl"}}]}},
                 {"tool_use_result": {"status": "completed", "agentId": "child-b"}, "message": {"content": [{"type": "tool_result", "tool_use_id": "b", "content": "done"}]}}]
        self.assertFalse(grader.claude_completion(calls, "child-a"))
        self.assertTrue(grader.claude_completion(calls, "child-b"))
        calls[-1]["message"]["content"][0]["is_error"] = True
        self.assertFalse(grader.claude_completion(calls, "child-b"))
        calls[-1]["message"]["content"][0].pop("is_error")
        calls[0]["message"]["content"][0]["input"]["subagent_type"] = "general-purpose"
        self.assertFalse(grader.claude_completion(calls, "child-b"))

    def test_report_refs_normalize_without_overwriting_contradictory_evidence(self):
        ref = {"path": "coverage.json", "sha256": "a" * 64}
        original = {"scope": "allocation", "refs": {"coverage": ref}}
        self.assertEqual(grader.report_fields(original)["coverage"], ref)
        self.assertNotIn("coverage", original)
        self.assertEqual(grader.report_fields({**original, "coverage": ref})["coverage"], ref)
        with self.assertRaisesRegex(ValueError, "Contradictory"):
            grader.report_fields({**original, "coverage": {**ref, "sha256": "b" * 64}})
        with self.assertRaisesRegex(TypeError, "object"):
            grader.report_fields({"refs": []})

    def test_actual_claude_agent_id_precedes_descriptive_task_but_role_is_required(self):
        value = {"agent_type": "pixl:pixl", "agent_id": "actual-child", "canonical_task": "Descriptive assignment prose"}
        self.assertEqual(grader.selected_child(value, "claude"), "actual-child")
        self.assertIsNone(grader.selected_child({**value, "agent_type": "general-purpose"}, "claude"))
        self.assertEqual(grader.selected_child({"agent_type": "pixl", "canonical_task": "/root/child", "fork_turns": "all"}, "codex"), "/root/child")

    def make_attempt(self):
        work = self.root / grader.WORK
        work.mkdir(parents=True)
        role = "Exact test portable specialist instructions"
        rolefile = self.root / ".codex/agents/pixl.toml"
        rolefile.parent.mkdir(parents=True)
        rolefile.write_text("developer_instructions = " + json.dumps(role), encoding="utf-8")
        skill = self.root / grader.KIT / "skills/plar/SKILL.md"
        skill.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "plugins/pixl/skills/plar/SKILL.md", skill)
        baseline = {ident: service.call("pixl_plar_read", {"asset_id": ident}, self.root) for ident in grader.STATES.values()}
        initial = service.call("pixl_plar_read", {}, self.root)
        inputs = inventory(self.root)
        saved = service.call("pixl_plar_save", {"document": self.after, "expect": initial["hash"]}, self.root)
        child = [self.source_event(name, line=i + 10) for i, name in enumerate(grader.CHILD_SOURCES)]
        child.append({"payload": {"type": "item_completed", "item": {"type": "CommandExecution", "exit_code": 0,
            "command": "Get-Content -LiteralPath '" + str(skill) + "'", "aggregated_output": skill.read_text(encoding="utf-8")}}})
        child += [event("pixl_plar_read", {}, initial, line=20), event("pixl_plar_save", {"document": self.after, "expect": initial["hash"]}, saved, line=21)]
        parent = [self.source_event(name, line=i + 10, file="parent") for i, name in enumerate(("src/start-shortcut.mjs", "src/shortcut-entry.mjs"))]
        refresh = service.call("pixl_plar_read", {"since": initial["hash"]}, self.root)
        parent.append(event("pixl_plar_read", {"since": initial["hash"]}, refresh, line=20, file="parent"))
        def output(name, value):
            path = work / name
            write_json(path, value)
            return {"path": path.relative_to(self.root).as_posix(), "sha256": sha(path)}
        coverage, source_map = self.reports()
        caller = {"native_child": "/root/specialist", "coverage": output("coverage.json", coverage), "source_map": output("source-map.json", source_map),
            "initial_read": output("initial-read.json", initial), "update_save": output("update-save.json", saved),
            "parent_refresh": output("parent-refresh.json", refresh), "scope": "Only declared source frontier", "limits": ["No art or runtime acceptance"],
            "next_action": "Continue other work; preserve controlled job", "parent_selections": {}}
        final_ref = output("final-document.json", self.after)
        specialist = {k: caller[k] for k in ("coverage", "source_map", "initial_read", "update_save")}
        specialist["final_document"] = final_ref
        caller["specialist_result"] = output("SPECIALIST-RESULT.json", specialist)
        for i, ident in enumerate(grader.STATES.values()):
            value = service.call("pixl_plar_read", {"asset_id": ident}, self.root)
            caller["parent_selections"][ident] = output(ident + ".json", value)
            parent.append(event("pixl_plar_read", {"asset_id": ident}, value, line=30 + i, file="parent"))
        output("CALLER-RESULT.json", caller)
        write_json(self.attempt / "identity.json", {"fixture": self.fixture, "baseline_document": self.before, "baseline_selections": baseline,
            "baseline_changes": initial["changes"], "inputs": inputs, "original_inputs": self.original})
        write_json(self.attempt / "launch.json", {"cwd": str(self.root), "host": "codex"})
        write_json(self.attempt / "entrypoint-observation.json", {"command": ["node", str(self.root / "src/shortcut-entry.mjs")],
            "returncode": 0, "stdout": json.dumps({"label": "Start", "path": "assets/start.svg", "frames": 1})})
        write_json(self.attempt / "continuation.json", {"session_id": "parent", "status": "finished", "returncode": 0, "interruption_reason": None})
        for name, values in (("native-parent.jsonl", [{"type": "session_meta", "payload": {"id": "parent"}}, *parent]),
                             ("native-child.jsonl", [{"type": "session_meta", "payload": {"id": "child"}}, *child]), ("stdout.jsonl", [])):
            (self.attempt / name).write_text("".join(json.dumps(v) + "\n" for v in values), encoding="utf-8")

    def grade_fixture(self):
        # Host activation itself has separate strict native regressions; here the
        # recorded MCP operations and actual filesystem remain independently checked.
        with patch.object(grader, "codex_role_proof", return_value={"loaded": True, "completed": True, "selected_children": [{"id": "child"}]}):
            return grader.grade(self.attempt)

    def test_complete_operation_and_missing_child_read_are_distinguished(self):
        self.make_attempt()
        result = self.grade_fixture()
        self.assertEqual(result["status"], "pass", [c for c in result["checks"] if not c["pass"]])
        journal = self.attempt / "native-child.jsonl"
        events = [json.loads(s) for s in journal.read_text(encoding="utf-8").splitlines()]
        events = [r for r in events if r.get("payload", {}).get("item", {}).get("arguments", {}).get("path") != "src/start-shortcut.mjs"]
        journal.write_text("".join(json.dumps(v) + "\n" for v in events), encoding="utf-8")
        result = self.grade_fixture()
        self.assertFalse(next(c["pass"] for c in result["checks"] if c["check"] == "child_inspected_src/start-shortcut.mjs"))

    def test_original_production_bytes_cannot_be_rewritten_after_pass(self):
        self.make_attempt()
        state = self.root / ".pixl/assets/queue.working/state.px"
        state.write_bytes(state.read_bytes() + b"\n")
        result = self.grade_fixture()
        self.assertEqual(result["status"], "fail")

    def test_named_role_and_source_reads_do_not_replace_actual_PLAR_loading(self):
        self.make_attempt()
        journal = self.attempt / "native-child.jsonl"
        events = [json.loads(s) for s in journal.read_text(encoding="utf-8").splitlines()]
        events = [r for r in events if r.get("payload", {}).get("item", {}).get("type") != "CommandExecution"]
        journal.write_text("".join(json.dumps(v) + "\n" for v in events), encoding="utf-8")
        result = self.grade_fixture()
        self.assertFalse(next(c["pass"] for c in result["checks"] if c["check"] == "selected_child_loaded_operational_PLAR_skill"))

    def test_plar_skill_requires_successful_bound_loading_not_assistant_quote(self):
        skill = self.root / grader.KIT / "skills/plar/SKILL.md"
        skill.parent.mkdir(parents=True)
        text = "---\nname: plar\n---\n\nRead actual consumers and preserve source boundaries.\n"
        skill.write_text(text, encoding="utf-8")
        quote = {"payload": {"type": "message", "role": "assistant", "content": [{"text": text}]}}
        self.assertFalse(grader.plar_skill_proof([[quote]], self.root))
        command = {"payload": {"type": "item_completed", "item": {"type": "CommandExecution", "exit_code": 0,
            "command": "Get-Content '" + str(skill) + "'", "aggregated_output": text}}}
        self.assertTrue(grader.plar_skill_proof([[command]], self.root))
        command["payload"]["item"]["exit_code"] = 1
        self.assertFalse(grader.plar_skill_proof([[command]], self.root))
        use = {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "skill-use", "name": "Skill", "input": {"skill": "pixl:plar"}}]}}
        returned = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "skill-use", "content": "Skill loaded"}]}}
        injected = {"type": "user", "isMeta": True, "sourceToolUseID": "skill-use", "message": {"content": [{"text":
            "Base directory for this skill: " + skill.parent.as_posix() + "\n\nRead actual consumers and preserve source boundaries."}]}}
        self.assertTrue(grader.plar_skill_proof([[use, returned, injected]], self.root))
        injected["sourceToolUseID"] = "unbound"
        self.assertFalse(grader.plar_skill_proof([[use, returned, injected]], self.root))

    def test_source_binding_added_by_public_save_does_not_invalidate_authored_document(self):
        unbound = copy.deepcopy(self.after)
        for source in unbound["sources"][-2:]:
            source.pop("sha256")
        self.assertEqual(grader.bound_sources(unbound, self.root), self.after)
        self.assertNotIn("sha256", unbound["sources"][-1])

    def test_overview_read_requires_complete_successful_path_bound_return(self):
        path = self.root / "SOURCE-MAP.md"
        path.write_text("First meaningful line\n\nLast meaningful line\n", encoding="utf-8")
        content = "\n".join(f"{i}\t{line}" for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1))
        use = {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "read", "name": "Read", "input": {"file_path": str(path)}}]}}
        result = {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "read", "content": content}]}}
        self.assertTrue(grader.native_read_proof([[use, result]], path))
        result["message"]["content"][0]["content"] = content + "\n4\t\n"
        self.assertTrue(grader.native_read_proof([[use, result]], path))
        result["message"]["content"][0]["content"] = "1\tFirst meaningful line\n2\t\n3\t\n"
        self.assertFalse(grader.native_read_proof([[use, result]], path))
        result["message"]["content"][0]["content"] = content
        result["message"]["content"][0]["is_error"] = True
        self.assertFalse(grader.native_read_proof([[use, result]], path))
        result["message"]["content"][0].pop("is_error")
        use["message"]["content"][0]["input"]["file_path"] = str(self.root / "BRIEF.md")
        self.assertFalse(grader.native_read_proof([[use, result]], path))

    def test_missing_evidence_fails_and_existing_grade_is_never_overwritten(self):
        self.assertEqual(grader.grade(self.attempt)["status"], "fail")
        output = self.attempt / "retained-grade.json"
        output.write_bytes(b"original failure")
        with self.assertRaisesRegex(ValueError, "Preserve"):
            grader.main([str(self.attempt), "--output", str(output)])
        self.assertEqual(output.read_bytes(), b"original failure")

    def continuation_fixture(self):
        resumed = self.base / "resumed"
        resumed.mkdir()
        config = self.base / "config.json"
        config.write_text("fixed configuration", encoding="utf-8")
        configuration = {"host": grader.file_reference(config)}
        write_json(self.attempt / "launch.json", {"host": "claude", "cwd": str(self.root)})
        prior = {"host": "claude", "cwd": str(self.root), "session_id": "same-parent", "children": [{"id": "selected-child", "role": "pixl:pixl"}],
                 "calls": [{"id": "original-call"}], "inputs": {}, "configuration": configuration, "status": "finished", "interruption_reason": "timeout"}
        write_json(self.attempt / "continuation.json", prior)
        predecessor = grader.file_reference(self.attempt / "continuation.json")
        launch = {"host": "claude", "cwd": str(self.root), "predecessor": predecessor, "continuation_mode": "native_same_session",
                  "expected_session_id": "same-parent", "expected_child_id": "selected-child"}
        identity = {"predecessor": predecessor, "original_consumer": str(self.root), "session_id": "same-parent", "child_id": "selected-child"}
        write_json(resumed / "launch.json", launch)
        write_json(resumed / "identity.json", identity)
        current = {"host": "claude", "cwd": str(self.root), "predecessor": predecessor, "mode": "native_same_session",
            "expected_session_id": "same-parent", "expected_child_id": "selected-child", "session_id": "same-parent", "observed_expected_session": True,
            "children": [], "calls": [], "inputs": {"launch": grader.file_reference(resumed / "launch.json")}, "configuration": configuration,
            "status": "finished", "returncode": 0, "interruption_reason": None}
        write_json(resumed / "continuation.json", current)
        return resumed, current

    def test_additive_continuation_preserves_original_child_without_inventing_work(self):
        resumed, current = self.continuation_fixture()
        original = (self.attempt / "continuation.json").read_bytes()
        merged, proof = grader.continuation_record(self.attempt, resumed, "selected-child")
        self.assertEqual(merged["children"], [{"id": "selected-child", "role": "pixl:pixl"}])
        self.assertEqual(merged["calls"], [{"id": "original-call"}])
        self.assertEqual(merged["status"], "finished")
        self.assertTrue(proof["observed_expected_session"])
        self.assertEqual((self.attempt / "continuation.json").read_bytes(), original)
        current["session_id"] = "different-parent"
        write_json(resumed / "continuation.json", current)
        with self.assertRaisesRegex(ValueError, "same parent"):
            grader.continuation_record(self.attempt, resumed, "selected-child")

    def test_continuation_rejects_wrong_child_predecessor_and_changed_configuration(self):
        resumed, current = self.continuation_fixture()
        with self.assertRaisesRegex(ValueError, "same parent"):
            grader.continuation_record(self.attempt, resumed, "another-child")
        altered = copy.deepcopy(current)
        altered["predecessor"]["sha256"] = "0" * 64
        write_json(resumed / "continuation.json", altered)
        with self.assertRaisesRegex(ValueError, "predecessor"):
            grader.continuation_record(self.attempt, resumed, "selected-child")
        write_json(resumed / "continuation.json", current)
        (self.base / "config.json").write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "configuration changed"):
            grader.continuation_record(self.attempt, resumed, "selected-child")


if __name__ == "__main__":
    unittest.main()
