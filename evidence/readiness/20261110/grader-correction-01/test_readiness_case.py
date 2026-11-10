"""Fresh native setup distinguishes template files, explicit loading and observations."""

from __future__ import annotations

import json
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

from evaluations import readiness_case as case
from evaluations.grade_readiness import (
    claude_child_paths,
    codex_role_proof,
    declared_tools,
    generic_substitutions,
    grade,
    inventory_errors,
    native_calls,
    operation_proof,
    semantic_result,
    startup_discovery,
)
from evaluations.host_trials import sha, write_json


class ReadinessNativeProofTests(unittest.TestCase):
    def test_raw_generic_child_is_not_hidden_by_empty_recorder_summary(self):
        proof = {"calls": [{"tool": "spawn_agent", "requested_role": "default"}], "children": [{"id": "other", "role": "default"}]}
        self.assertTrue(generic_substitutions(proof, [])["calls"])
        self.assertTrue(generic_substitutions({"calls": [], "children": proof["children"]}, [])["children"])

    def test_successful_saved_envelope_preserves_semantics_without_accepting_errors(self):
        saved = {"text": "source", "sha256": "a" * 64}
        self.assertEqual(semantic_result(saved), saved)
        self.assertEqual(semantic_result({"isError": False, "structuredContent": saved}), saved)
        with self.assertRaisesRegex(ValueError, "not a successful"):
            semantic_result({"isError": True, "structuredContent": saved})

    def codex_journals(self):
        def row(payload, line, kind="response_item", file="parent.jsonl"):
            return {"type": kind, "payload": payload, "line": line, "file": file}
        parent = [row({"id": "parent"}, 1, "session_meta"),
                  row({"type": "function_call", "namespace": "collaboration", "name": "spawn_agent", "call_id": "spawn",
                       "arguments": json.dumps({"agent_type": "pixl", "fork_turns": "none"})}, 2),
                  row({"type": "function_call_output", "call_id": "spawn", "output": '{"task_name":"/root/specialist"}'}, 3)]
        child = [row({"id": "child", "session_id": "parent", "source": {"subagent": {"thread_spawn": {
            "parent_thread_id": "parent", "agent_role": "pixl", "agent_path": "/root/specialist"}}}}, 1, "session_meta", "child.jsonl"),
            row({"type": "message", "role": "developer", "content": [{"text": "Read skill.\r\nRead profile.\r\n"}]}, 2, file="child.jsonl"),
            row({"type": "task_complete"}, 3, file="child.jsonl")]
        return parent, child

    def test_canonical_spawn_result_binds_exact_child_and_newline_normalized_instructions(self):
        parent, child = self.codex_journals()
        proof = codex_role_proof([parent, child], "parent", "/root/specialist", "Read skill.\nRead profile.\n")
        self.assertTrue(proof["loaded"])
        self.assertTrue(proof["completed"])
        self.assertEqual(proof["selected_children"][0]["id"], "child")
        self.assertFalse(codex_role_proof([parent, child], "parent", "/root/unrelated", "Read skill.\nRead profile.\n")["loaded"])
        child[0]["payload"]["source"]["subagent"]["thread_spawn"]["parent_thread_id"] = "other-parent"
        self.assertFalse(codex_role_proof([parent, child], "parent", "/root/specialist", "Read skill.\nRead profile.\n")["loaded"])

    def test_parent_only_reads_and_unselected_child_do_not_credit_selected_child(self):
        parent, child = self.codex_journals()
        parent.append({"payload": {"type": "item_completed", "item": {"type": "CommandExecution",
                       "exit_code": 0, "aggregated_output": "complete profile and skill"}}})
        proof = codex_role_proof([parent, child], "parent", "/root/specialist", "Read skill.\nRead profile.\n")
        self.assertEqual(proof["child_text"], "")
        child.append({"payload": {"type": "item_completed", "item": {"type": "CommandExecution",
                      "exit_code": 1, "aggregated_output": "complete profile and skill"}}})
        self.assertEqual(codex_role_proof([parent, child], "parent", "/root/specialist", "Read skill.\nRead profile.\n")["child_text"], "")
        child[-1]["payload"]["item"]["exit_code"] = 0
        self.assertIn("complete profile", codex_role_proof([parent, child], "parent", "/root/specialist", "Read skill.\nRead profile.\n")["child_text"])

    def test_claude_parent_transcript_is_never_child_read_proof(self):
        with tempfile.TemporaryDirectory() as directory:
            attempt = Path(directory)
            (attempt / "native-transcripts").mkdir()
            for name in ("parent", "session", "agent-selected", "agent-other"):
                (attempt / "native-transcripts" / (name + ".jsonl")).write_text("{}\n")
            self.assertEqual([p.stem for p in claude_child_paths(attempt, "session", {"selected", "parent"})], ["agent-selected"])

    def test_catalog_requires_paired_actual_enumeration_not_authored_inventory(self):
        catalog = [{"name": "mcp__pixl_local__pixl_source", "description": "Read source"}]
        output = {"payload": {"type": "custom_tool_call_output", "call_id": "catalog", "output": [
            {"type": "input_text", "text": json.dumps(catalog)}]}}
        call = {"payload": {"type": "custom_tool_call", "name": "exec", "call_id": "catalog",
                            "input": "text(ALL_TOOLS.filter(x=>/pixl/i.test(x.name)));"}}
        self.assertEqual(declared_tools([[call, output]]), {"pixl_source"})
        self.assertEqual(declared_tools([[output]]), set())
        self.assertEqual(declared_tools([[{"message": {"content": catalog}}]]), set())
        call["payload"]["input"] = 'text(JSON.parse(await read("tool-inventory.json")));'
        self.assertEqual(declared_tools([[call, output]]), set())

    def test_auth_startup_discovery_is_distinct_from_child_loading(self):
        result = startup_discovery([{"type": "system", "subtype": "init", "agents": ["pixl:pixl"],
            "mcp_servers": [{"name": "pixl-local", "status": "connected"}]}, {"type": "result", "is_error": True,
            "result": "Failed to authenticate", "usage": {"input_tokens": 0, "output_tokens": 0}}])
        self.assertEqual(result["initializations"][0]["agents"], ["pixl:pixl"])
        self.assertEqual(result["terminal_results"][0]["usage"]["input_tokens"], 0)
        self.assertNotIn("loaded", result)

    def test_report_only_does_not_prove_local_tool_execution(self):
        item = {"path": "work/readiness/source.json", "sha256": "a" * 64}
        saved = {"text": "actual source", "sha256": "b" * 64}
        journal = [{"message": {"content": [{"type": "text", "text": json.dumps(saved)}]}}]
        self.assertEqual(operation_proof(native_calls([journal]), "pixl_source", item, saved), [])

    def test_codex_completed_native_export_binds_path_and_actual_hash(self):
        item = {"path": "work/readiness/source.json", "sha256": "a" * 64}
        result = {"isError": False, "structuredContent": {"result_path": item["path"], "result_sha256": item["sha256"]}}
        journal = [{"file": "native.jsonl", "line": 8, "payload": {"type": "item_completed", "item": {
            "type": "McpToolCall", "server": "pixl_local", "tool": "pixl_source", "status": "completed",
            "arguments": {"path": "BRIEF.md"}, "result": result}}}]
        self.assertTrue(operation_proof(native_calls([journal]), "pixl_source", item, {}))
        result["isError"] = True
        self.assertFalse(operation_proof(native_calls([journal]), "pixl_source", item, {}))

    def test_claude_actual_tool_result_matches_returned_json(self):
        saved = {"text": "actual source", "sha256": "b" * 64}
        journal = [{"file": "claude.jsonl", "line": 3, "message": {"content": [{"type": "tool_use", "id": "call1",
            "name": "mcp__pixl-local__pixl_source", "input": {"path": "BRIEF.md"}}]}},
            {"file": "claude.jsonl", "line": 4, "message": {"content": [{"type": "tool_result", "tool_use_id": "call1",
            "content": [{"type": "text", "text": json.dumps(saved)}]}]}}]
        self.assertTrue(operation_proof(native_calls([journal]), "pixl_source", {"path": "a", "sha256": "c" * 64}, saved))
        self.assertFalse(operation_proof(native_calls([journal]), "pixl_source", {"path": "a", "sha256": "c" * 64}, {"text": "fabricated"}))

    def test_complete_inventory_is_not_inferred_from_successful_subset(self):
        observation = {"names": ["pixl_source"], "complete_inventory": True}
        self.assertTrue(inventory_errors(observation, {"pixl_source", "pixl_sources"}, {"pixl_source"}))
        observation["complete_inventory"] = False
        self.assertEqual(inventory_errors(observation, set(), {"pixl_source"}), [])
        observation["names"].append("pixl_invented")
        self.assertTrue(inventory_errors(observation, set(), {"pixl_source"}))


class ReadinessCaseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="readiness case tests ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.package = self.root / "source package"
        files = {"config/codex-agent.example.toml": 'name="pixl"\ndeveloper_instructions="Read /ABSOLUTE/PLUGIN/pixl/skills/pixl/SKILL.md"\n',
                 "agents/pixl.md": "---\nname: pixl\ndescription: Actual plugin role\n---\nRead the common skill.\n",
                 "skills/pixl/SKILL.md": "---\nname: pixl\ndescription: Common workflow\n---\n",
                 "skills/plar/SKILL.md": "---\nname: plar\ndescription: Allocation workflow\n---\n",
                 "scripts/pixl.py": "# fixture runner\n"}
        rows = []
        for name, text in files.items():
            path = self.package / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            rows.append({"path": name, "sha256": sha(path)})
        write_json(self.package / "bundle-manifest.json", {"files": rows})

    def prepare(self, host, setup):
        attempt = self.root / f"{host}-{setup}-attempt"
        consumer = self.root / f"{host}-{setup}-consumer"
        def output(command, **kwargs):
            if "--version" in command:
                return "0.167.0\n" if host == "codex" else "2.1.318 (Claude Code)\n"
            if command[0] == "git":
                return "fixture-source-revision\n"
            return json.dumps({"executable": sys.executable, "version": "3.11.0", "packages": ["pillow", "jsonschema", "referencing"]})
        with patch.object(case, "codex_command", return_value=["codex"]), patch.object(
                case.subprocess, "check_output", side_effect=output):
            case.prepare(attempt, host, setup, Path(sys.executable), consumer=consumer, package=self.package)
        return attempt, consumer, json.loads((attempt / "launch.json").read_bytes())

    def test_codex_clean_uses_resolved_shipped_template_and_explicit_session_registration(self):
        attempt, consumer, launch = self.prepare("codex", "clean")
        role = consumer / ".codex/agents/pixl.toml"
        expected = (self.package / "config/codex-agent.example.toml").read_text(encoding="utf-8").replace(
            "/ABSOLUTE/PLUGIN/pixl", (consumer / case.KIT).as_posix())
        self.assertEqual(role.read_text(encoding="utf-8"), expected)
        self.assertIn("agents.pixl.config_file=" + json.dumps(role.as_posix()), launch["command"])
        self.assertIn("agents.enabled=true", launch["command"])
        self.assertIn((consumer / case.KIT).as_posix(), tomllib.loads(expected)["developer_instructions"])
        self.assertFalse((attempt / "stdout.jsonl").exists())
        self.assertTrue((consumer / ".agents/skills/pixl/SKILL.md").is_file())

    def test_codex_incomplete_preserves_full_kit_and_runtime_but_omits_only_role_loading(self):
        _, consumer, launch = self.prepare("codex", "missing-registration")
        self.assertFalse((consumer / ".codex/agents/pixl.toml").exists())
        self.assertFalse(any(arg.startswith("agents.pixl.config_file=") for arg in launch["command"]))
        self.assertTrue(any(arg.startswith("mcp_servers.pixl_local.command=") for arg in launch["command"]))
        self.assertEqual(sha(consumer / case.KIT / "bundle-manifest.json"), sha(self.package / "bundle-manifest.json"))

    def test_claude_loads_actual_plugin_without_synthetic_agent_replacement(self):
        _, consumer, launch = self.prepare("claude", "clean")
        command = launch["command"]
        self.assertEqual(command[command.index("--plugin-dir") + 1], str(consumer / case.KIT))
        self.assertNotIn("--agents", command)
        self.assertNotIn("--agent", command)
        self.assertIn("pixl:pixl", (consumer / "READINESS-ASSIGNMENT.md").read_text(encoding="utf-8"))

    def test_claude_incomplete_omits_plugin_loading_not_local_runtime(self):
        attempt, consumer, launch = self.prepare("claude", "missing-registration")
        self.assertNotIn("--plugin-dir", launch["command"])
        server = json.loads((attempt / "mcp.json").read_bytes())["mcpServers"]
        self.assertEqual(set(server), {"pixl-local"})
        self.assertEqual(server["pixl-local"]["args"][0], "-B")
        self.assertTrue((consumer / case.KIT / "agents/pixl.md").is_file())
        self.assertFalse((consumer / ".claude/agents/pixl.md").exists())

    def test_repository_descendant_consumer_and_existing_attempt_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside repository ancestry"):
            case.prepare(self.root / "bad", "codex", "clean", Path(sys.executable),
                         consumer=case.ROOT / "build/readiness-forbidden", package=self.package)
        attempt, _, _ = self.prepare("codex", "clean")
        with self.assertRaisesRegex(ValueError, "fresh attempt"):
            case.prepare(attempt, "codex", "clean", Path(sys.executable), package=self.package)

    def test_retention_preserves_outputs_and_exposes_changed_original(self):
        attempt, consumer, _ = self.prepare("codex", "clean")
        write_json(consumer / case.WORK / "CALLER-RESULT.json", {"status": "partial"})
        (consumer / "BRIEF.md").write_text("changed original", encoding="utf-8")
        case.retain(attempt)
        saved = json.loads((attempt / "preservation.json").read_bytes())
        self.assertEqual(saved["changed"], ["BRIEF.md"])
        self.assertTrue((attempt / "outputs/CALLER-RESULT.json").is_file())

    def test_authentication_block_preserves_startup_facts_and_unverified_behavior(self):
        attempt, _, _ = self.prepare("claude", "clean")
        write_json(attempt / "continuation.json", {"status": "finished", "returncode": 1,
                   "interruption_reason": "authentication", "session_id": "parent"})
        events = [{"type": "system", "subtype": "init", "agents": ["pixl:pixl"],
                   "mcp_servers": [{"name": "pixl-local", "status": "connected"}]},
                  {"type": "result", "is_error": True, "result": "Failed to authenticate",
                   "usage": {"input_tokens": 0, "output_tokens": 0}}]
        (attempt / "stdout.jsonl").write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")
        result = grade(attempt)
        self.assertEqual(result["status"], "blocked_authentication")
        self.assertEqual(result["behavioral_status"], "unverified")
        self.assertFalse(result["observed_named_role_loaded"])
        self.assertEqual(result["startup_discovery"]["initializations"][0]["agents"], ["pixl:pixl"])


if __name__ == "__main__":
    unittest.main()
