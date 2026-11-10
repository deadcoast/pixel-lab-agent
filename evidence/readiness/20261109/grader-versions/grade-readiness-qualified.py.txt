"""Independent native loading, returned read-only operations and preservation checks."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path

from evaluations.grade_named_codex_role import (
    normalized,
    objects,
    rows,
    strings,
    trace_facts,
)
from evaluations.host_trials import inventory, sha, write_json
from evaluations.readiness_case import KIT, ROOT, WORK
from pixl.readiness import validate_observations


def read(path):
    return json.loads(Path(path).read_bytes())


def reference(root: Path, item: dict) -> Path:
    path = (root / item["path"]).resolve()
    if not path.is_relative_to(root.resolve()) or sha(path) != item["sha256"]:
        raise ValueError("Returned artifact escapes root or differs from declared bytes")
    return path


def expanded_objects(value):
    """Unwrap native MCP text blocks without interpreting arbitrary text as code."""
    yield from objects(value)
    for text in strings(value):
        if text.lstrip().startswith(("{", "[")):
            try:
                yield from objects(json.loads(text))
            except ValueError:
                pass


def native_calls(journals: list[list[dict]]) -> list[dict]:
    calls, uses = [], {}
    for journal in journals:
        for row in journal:
            payload = row.get("payload", {})
            item = payload.get("item", row.get("item", {}))
            if (item.get("type") in ("McpToolCall", "mcp_tool_call")
                    and item.get("server") in ("pixl_local", "pixl-local")
                    and item.get("status") in ("completed", "succeeded")):
                result = item.get("result", {})
                calls.append({"tool": item["tool"], "arguments": item.get("arguments", {}),
                    "result": result, "success": result.get("isError") is False,
                    "file": row.get("file"), "line": row.get("line")})
            message = row.get("message", {})
            content = message.get("content", []) if isinstance(message, dict) else []
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use" and re.fullmatch(r"mcp__pixl[-_]local__pixl_[a-z_]+", block.get("name", "")):
                    uses[block["id"]] = {"tool": block["name"].split("__")[-1], "arguments": block.get("input", {}),
                                         "file": row.get("file"), "line": row.get("line")}
                if block.get("type") == "tool_result" and block.get("tool_use_id") in uses:
                    call = {**uses[block["tool_use_id"]], "result": block.get("content"),
                            "success": not block.get("is_error", False)}
                    calls.append(call)
    return calls


def operation_proof(calls: list[dict], tool: str, item: dict, saved: dict) -> list[dict]:
    proofs = []
    for call in calls:
        if call["tool"] != tool or not call["success"]:
            continue
        returned = list(expanded_objects(call["result"]))
        exact_export = any(r.get("result_path") == item["path"] and r.get("result_sha256") == item["sha256"] for r in returned)
        direct_result = any(r == saved for r in returned)
        if exact_export or direct_result:
            proofs.append({k: call[k] for k in ("file", "line", "tool", "arguments")})
    return proofs


def semantic_result(saved: dict) -> dict:
    """Callers may preserve the complete MCP return or its result object."""
    if "structuredContent" in saved:
        if saved.get("isError") is not False or not isinstance(saved["structuredContent"], dict):
            raise ValueError("Saved MCP envelope is not a successful structured result")
        return saved["structuredContent"]
    return saved


def declared_tools(journals: list[list[dict]]) -> set[str]:
    names: set[str] = set()
    for journal in journals:
        catalog_calls = set()
        for row in journal:
            payload = row.get("payload", {})
            # ALL_TOOLS is native metadata. Accept its returned catalog only
            # from the paired exec enumeration, never from an authored report.
            if (payload.get("type") == "custom_tool_call" and payload.get("name") == "exec"
                    and re.search(r"text\(ALL_TOOLS\.filter\(\w+=>/pixl/i\.test\(\w+\.name\)\)\)", payload.get("input", ""))):
                catalog_calls.add(payload.get("call_id"))
            if (payload.get("type") == "custom_tool_call_output" and payload.get("call_id") in catalog_calls
                    and not payload.get("is_error")):
                for block in payload.get("output", []):
                    try:
                        catalog = json.loads(block.get("text", ""))
                    except (ValueError, AttributeError):
                        continue
                    if isinstance(catalog, list) and catalog and all(isinstance(t, dict) and isinstance(t.get("description"), str)
                            and re.fullmatch(r"mcp__pixl[-_]local__pixl_[a-z_]+", t.get("name", "")) for t in catalog):
                        names.update(t["name"].split("__")[-1] for t in catalog)
            # Only host declaration events establish static declarations.
            if payload.get("type") != "additional_tools" and not (row.get("type") == "system" and row.get("subtype") == "init"):
                continue
            for value in objects(row):
                name = value.get("name", "")
                if isinstance(name, str) and name.startswith("pixl_") and ("inputSchema" in value or "parameters" in value):
                    names.add(name)
                for tool in value.get("tools", []) if isinstance(value.get("tools"), list) else []:
                    if isinstance(tool, str) and re.fullmatch(r"mcp__pixl[-_]local__pixl_[a-z_]+", tool):
                        names.add(tool.split("__")[-1])
    return names


def completed_command_text(journal: list[dict]) -> str:
    """Read evidence belongs to the selected child's successful commands."""
    return "\n".join(r["payload"]["item"].get("aggregated_output", "") for r in journal
                     if r.get("payload", {}).get("type") == "item_completed"
                     and r["payload"].get("item", {}).get("type") == "CommandExecution"
                     and r["payload"]["item"].get("exit_code") == 0)


def codex_role_proof(journals: list[list[dict]], parent: str, selected: str | None, role_text: str) -> dict:
    facts = trace_facts(journals, parent, role_text or "__unconfigured_role__")
    parent_rows = facts["journals"].get(parent, [])
    bound = []
    for call in facts["calls"]:
        if call["tool"] != "spawn_agent" or call["requested_role"] != "pixl" or call["fork_turns"] != "none":
            continue
        for row in parent_rows:
            payload = row.get("payload", {})
            if payload.get("type") != "function_call_output" or payload.get("call_id") != call["id"] or payload.get("is_error"):
                continue
            try:
                returned = json.loads(payload.get("output", "{}"))
            except (ValueError, TypeError):
                continue
            path = returned.get("task_name") if isinstance(returned, dict) else None
            for child in facts["children"]:
                meta = facts["journals"][child["id"]][0]["payload"]
                consistent = all(meta.get(k, expected) == expected for k, expected in (
                    ("parent_thread_id", parent), ("agent_path", child["agent_path"]), ("agent_role", child["role"])))
                if consistent and child["role"] == "pixl" and path == child["agent_path"] and selected in (path, child["id"]):
                    bound.append({**child, "spawn_line": call["line"], "spawn_result_line": row["line"]})
    matches, completions, text = [], [], ""
    if len(bound) == 1:
        child = bound[0]
        journal = facts["journals"][child["id"]]
        for row in journal:
            payload = row.get("payload", {})
            if payload.get("type") == "message" and payload.get("role") == "developer":
                for block in payload.get("content", []):
                    # Exact instruction content, with newline representation only
                    # normalized. Do not accept a quotation or a parent read.
                    actual = block.get("text", "")
                    if role_text and actual.replace("\r\n", "\n") == role_text.replace("\r\n", "\n"):
                        matches.append({"file": row.get("file"), "line": row.get("line"), "child": child["id"]})
            if payload.get("type") == "task_complete":
                completions.append({"file": row.get("file"), "line": row.get("line")})
        text = completed_command_text(journal)
    return {"loaded": len(bound) == 1 and bool(matches), "completed": bool(completions), "child_text": text,
            "children": facts["children"], "selected_children": bound, "instruction_matches": matches,
            "completion_events": completions, "calls": facts["calls"]}


def claude_child_paths(attempt: Path, parent: str, child_ids: set[str]) -> list[Path]:
    return [p for p in sorted((attempt / "native-transcripts").glob("*.jsonl"))
            if p.stem not in {"parent", parent} and p.stem.removeprefix("agent-") in child_ids]


def startup_discovery(events: list[dict]) -> dict:
    inits = [r for r in events if r.get("type") == "system" and r.get("subtype") == "init"]
    terminals = [r for r in events if r.get("type") == "result"]
    return {"scope": "Host startup declarations only; no child loading or local-operation success inferred.",
            "initializations": [{"file": r.get("file"), "line": r.get("line"), "agents": r.get("agents", []),
                                 "plugins": r.get("plugins", []), "mcp_servers": r.get("mcp_servers", [])} for r in inits],
            "terminal_results": [{"file": r.get("file"), "line": r.get("line"), "is_error": r.get("is_error"),
                                  "message": r.get("result"), "usage": r.get("usage")} for r in terminals]}


def inventory_errors(observation: dict | None, declarations: set[str], used: set[str]) -> list[str]:
    if observation is None:
        return []
    names = set(observation["names"])
    if not names <= declarations | used:
        return ["Observed local tool names lack a native declaration or successful call"]
    if observation["complete_inventory"] and (not declarations or names != declarations):
        return ["Complete inventory claim does not match an observed complete declaration set"]
    return []


def generic_substitutions(role_evidence: dict, fallback_calls: list[dict]) -> dict:
    calls = role_evidence.get("calls", fallback_calls)
    return {"calls": [c for c in calls if c.get("tool") in ("Agent", "spawn_agent")
                      and c.get("role", c.get("requested_role")) not in ("pixl", "pixl:pixl")],
            "children": [c for c in role_evidence.get("children", []) if c.get("role") not in ("pixl", "pixl:pixl")]}


def _grade(attempt: Path) -> dict:
    attempt = attempt.resolve()
    launch, identity, continuation = (read(attempt / name) for name in ("launch.json", "identity.json", "continuation.json"))
    root = Path(launch["cwd"]).resolve()
    checks = []
    def check(name, passed, evidence=None):
        checks.append({"check": name, "pass": bool(passed), "evidence": evidence})
    current = inventory(root, ("__pycache__",))
    drift = [p for p, digest in identity["inputs"].items() if current.get(p) != digest]
    additions = [p for p in current if p not in identity["inputs"] and not p.startswith(WORK + "/")]
    check("fresh_external_consumer_inputs_preserved", not root.is_relative_to(ROOT) and not drift and not additions,
          {"root": str(root), "changed_or_missing": drift, "unexpected_additions": additions})
    check("complete_relocated_kit_unchanged", inventory(root / KIT, ("__pycache__",)) == identity["package_files"])
    environment = read(attempt / "runtime-environment.json")
    forbidden = {"ruff", "mypy", "coverage", "tiktoken", "sourcery", "types-jsonschema", "types-setuptools"}
    check("selected_runtime_has_no_maintainer_packages", not forbidden.intersection(environment["packages"]), environment)
    journals = [rows(p) for p in sorted(attempt.glob("native-*.jsonl"))]
    journals += [rows(p) for p in sorted((attempt / "native-transcripts").glob("*.jsonl"))]
    journals.append(rows(attempt / "stdout.jsonl"))
    discovery = startup_discovery(journals[-1])
    if (continuation.get("interruption_reason") == "authentication"
            and not (root / WORK / "CALLER-RESULT.json").exists()):
        return {"version": 2, "status": "blocked_authentication", "behavioral_status": "unverified",
                "host": launch["host"], "setup": launch["setup"], "passed": sum(c["pass"] for c in checks),
                "total": len(checks), "checks": checks, "startup_discovery": discovery,
                "observed_named_role_loaded": False, "native_process": {k: continuation.get(k) for k in
                    ("status", "returncode", "interruption_reason", "recording_status")},
                "unverified": ["actual named specialist loading", "child instruction and skill reads",
                               "native local source, library and readiness calls", "caller observation accuracy"],
                "scope": "Preparation preservation and startup discovery only. Authentication prevented the task from running."}
    caller = read(root / WORK / "CALLER-RESULT.json")
    values = {}
    for key in ("source", "library", "readiness", "observations_file"):
        values[key] = read(reference(root, caller[key]))
    source, library, report = (semantic_result(values[k]) for k in ("source", "library", "readiness"))
    observation = values["observations_file"]
    validate_observations(observation, launch["host"])
    brief = root / "BRIEF.md"
    check("actual_unique_project_source_returned", source.get("sha256") == sha(brief)
          and source.get("text") == "".join(brief.read_bytes().decode("utf-8-sig").splitlines(keepends=True)[:3])
          and source.get("start") == 1 and source.get("end") == 3, {"brief": sha(brief), "source": source})
    check("actual_installed_library_returned", library.get("files_verified") is True
          and Path(library.get("root", "")).resolve() == (root / KIT / "resources").resolve(),
          {"root": library.get("root"), "files_verified": library.get("files_verified")})
    check("readiness_binds_actual_root_kit_runtime", report.get("read_only") is True
          and Path(report["project"]["root"]).resolve() == root
          and Path(report["installation"]["root"]).resolve() == root / KIT
          and report["installation"]["bundle_manifest"].get("sha256") == sha(root / KIT / "bundle-manifest.json")
          and report["dependencies"]["status"] == "available"
          and Path(report["reporter"]["python_executable"]).resolve() == Path(environment["executable"]).resolve())
    check("report_keeps_assertions_separate_from_loading_and_authentication",
          report.get("caller_supplied_observations") == observation
          and report["specialist"]["instruction_loading"] == "not_verified"
          and report["official_pixellab"]["authentication"] == "not_verified"
          and report["official_pixellab"]["execution"] == "not_attempted"
          and report["official_pixellab"]["cached_catalog_is_live_discovery"] is False)
    calls = native_calls(journals)
    for field, tool in (("source", "pixl_source"), ("library", "pixl_sources"), ("readiness", "pixl_readiness")):
        proofs = operation_proof(calls, tool, caller[field], values[field])
        check("native_executed_" + tool, bool(proofs), proofs)
    used = {c["tool"] for c in calls if c["success"]}
    declarations = declared_tools(journals)
    errors = inventory_errors(observation.get("local_tools"), declarations, used)
    check("local_inventory_scope_supported_by_native_observations", not errors,
          {"errors": errors, "declared": sorted(declarations), "used": sorted(used)})
    official = observation.get("official_tools", {})
    check("no_official_generation_or_auth_claim", not official.get("names")
          and identity["isolation"]["official_provider_configured"] is False,
          {"scope": "This isolated invocation only; not the user's other sessions or provider account.", "observation": official})
    loaded = False
    role_evidence = {}
    child_text = ""
    if launch["host"] == "codex":
        role_path = root / ".codex/agents/pixl.toml"
        role_text = tomllib.loads(role_path.read_text(encoding="utf-8"))["developer_instructions"] if role_path.is_file() else ""
        proof = codex_role_proof(journals, continuation.get("session_id"), caller.get("native_child"), role_text)
        loaded, child_text = proof["loaded"], proof["child_text"]
        role_evidence = {k: v for k, v in proof.items() if k != "child_text"}
        if launch["setup"] == "clean":
            expected = (root / KIT / "config/codex-agent.example.toml").read_text(encoding="utf-8").replace("/ABSOLUTE/PLUGIN/pixl", (root / KIT).as_posix())
            check("exact_shipped_template_resolved_and_registered", role_path.read_text(encoding="utf-8") == expected
                  and "agents.pixl.config_file=" + json.dumps(role_path.as_posix()) in launch["command"])
            check("selected_native_child_completed", proof["completed"], proof["completion_events"])
        else:
            check("intended_codex_registration_omitted", not role_path.exists()
                  and not any(v.startswith("agents.pixl.config_file=") for v in launch["command"]))
    else:
        events = journals[-1]
        inits = [r for r in events if r.get("type") == "system" and r.get("subtype") == "init"]
        agents = [c for c in continuation.get("calls", []) if c.get("tool") == "Agent" and c.get("role") == "pixl:pixl"
                  and c.get("result_line") and not c.get("is_error")]
        actual_children = continuation.get("children", [])
        child_ids = {str(c.get("agent_id", c.get("id", ""))) for c in actual_children}
        selected = caller.get("native_child")
        selected_ids = {str(selected)} & child_ids
        loaded = bool(agents) and bool(selected_ids) and any("pixl" in json.dumps(r.get("plugins", [])) for r in inits)
        role_evidence = {"plugin_initialization": inits, "agent_calls": agents, "children": actual_children}
        child_paths = claude_child_paths(attempt, continuation.get("session_id"), selected_ids)
        child_text = "\n".join(text for p in child_paths for text in strings(rows(p)))
        check("actual_plugin_route_without_replacement_agent", "--agents" not in launch["command"]
              and (("--plugin-dir" in launch["command"]) == (launch["setup"] == "clean")))
    role_claim = observation.get("named_role", "not_observed")
    if launch["setup"] == "clean":
        check("actual_named_specialist_loaded", loaded and role_claim == "available", role_evidence)
        for path in ("skills/pixl/SKILL.md", "resources/agent/PROFILE.md"):
            expected = normalized((root / KIT / path).read_text(encoding="utf-8"))
            check("child_read_" + path, expected in normalized(child_text), {"expected_file": path, "sha256": sha(root / KIT / path)})
        check("specialist_result_returned", bool(caller.get("specialist_result")) and reference(root, caller["specialist_result"]).is_file())
    else:
        # The omitted route is a fixture fact. Another genuinely observed route
        # may still load a role; absence is not manufactured to make a test pass.
        check("incomplete_setup_observation_not_impersonated", role_claim in {"unavailable", "not_observed"} and not loaded
              or role_claim == "available" and loaded, role_evidence)
        non_target = generic_substitutions(role_evidence, continuation.get("calls", []))
        check("no_generic_specialist_substitution", not any(non_target.values()), non_target)
    check("native_process_completed_with_recorded_exit", continuation.get("status") == "finished"
          and continuation.get("returncode") == 0 and continuation.get("interruption_reason") is None,
          {k: continuation.get(k) for k in ("status", "returncode", "interruption_reason", "recording_status")})
    return {"version": 2, "status": "pass" if all(c["pass"] for c in checks) else "fail", "host": launch["host"],
            "setup": launch["setup"], "passed": sum(c["pass"] for c in checks), "total": len(checks), "checks": checks,
            "observed_named_role_loaded": loaded, "startup_discovery": discovery,
            "scope": "One isolated fresh consumer and observed native route; local read-only outcomes only. No provider authentication, generation, art, engine or general host-reliability claim."}


def grade(attempt: Path) -> dict:
    try:
        return _grade(attempt)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        return {"version": 2, "status": "fail", "passed": 0, "total": 1,
                "checks": [{"check": "required_evidence_readable", "pass": False, "evidence": f"{type(error).__name__}: {error}"}]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attempt", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Preserve previous grades; select a fresh output")
    result = grade(args.attempt)
    write_json(args.output, result)
    print(json.dumps({k: result[k] for k in ("status", "passed", "total")}))
    raise SystemExit(result["status"] != "pass")
