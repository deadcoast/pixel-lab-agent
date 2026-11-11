"""Independent, bounded CF-06 source-allocation and preservation evidence checks."""

from __future__ import annotations

import argparse
import copy
import json
import re
import tomllib
from pathlib import Path

from evaluations.grade_caller_result import (
    bind_exports,
    child_identity,
    matching_calls,
    mcp_attempts,
)
from evaluations.grade_named_codex_role import normalized, own_rows, rows, strings
from evaluations.grade_readiness import (
    claude_loading_proof,
    codex_role_proof,
    expanded_objects,
    native_calls,
    reference,
    semantic_result,
)
from evaluations.host_trials import inventory, sha
from evaluations.native_trial_records import reference as file_reference
from evaluations.native_trial_records import verify_inputs
from evaluations.readiness_case import KIT
from pixl import plar, service

WORK = "work/plar-coverage"
STATES = {"idle": "queue.start", "running": "queue.working", "succeeded": "queue.ready", "failed": "queue.retry"}
TRANSITIONS = {"running": "started", "succeeded": "ok", "failed": "error"}
CHILD_SOURCES = ("SOURCE-MAP.md", "src/shortcut-entry.mjs", "src/start-shortcut.mjs", "src/queue-view.ts",
                 "src/queue.ts", "BRIEF.md", "assets/start.svg")
READ_TOOLS = {"pixl_catalog", "pixl_source", "pixl_sources", "pixl_plar_read", "pixl_readiness", "pixl_jobs",
              "pixl_workflow", "pixl_validate", "pixl_inspect", "pixl_plar_save"}


def read(path):
    return json.loads(Path(path).read_bytes())


def report_fields(value: dict) -> dict:
    """Accept the two declared reference layouts without changing retained bytes."""
    refs = value.get("refs", {})
    if not isinstance(refs, dict):
        raise TypeError("Report refs must be an object")
    for key, item in refs.items():
        if key in value and value[key] != item:
            raise ValueError("Contradictory top-level and refs values: " + key)
    names = {"coverage", "source_map", "initial_read", "update_save", "parent_refresh", "specialist_result", "final_document", "parent_selections"}
    return {**value, **{k: v for k, v in refs.items() if k in names}}


def selected_child(value, host: str) -> str | None:
    if host == "claude" and isinstance(value, dict):
        if value.get("agent_type") != "pixl:pixl":
            return None
        ident = value.get("agent_id", value.get("canonical_task"))
        return ident if isinstance(ident, str) and ident else None
    return child_identity(value)


def continuation_record(base: Path, resumed: Path, selected: str | None) -> tuple[dict, dict]:
    """Validate an additive same-parent continuation without rewriting its predecessor."""
    prior_path = base.resolve() / "continuation.json"
    prior, original = read(prior_path), read(base / "launch.json")
    launch, identity, current = (read(resumed / name) for name in ("launch.json", "identity.json", "continuation.json"))
    predecessor = file_reference(prior_path)
    if any(value.get("predecessor") != predecessor for value in (launch, identity, current)):
        raise ValueError("Continuation does not name the exact retained predecessor")
    session = prior["session_id"]
    if (original["host"] != "claude" or launch["host"] != original["host"] or current.get("host") != original["host"]
            or launch.get("continuation_mode") != "native_same_session" or current.get("mode") != "native_same_session"
            or any(Path(value["cwd"]).resolve() != Path(original["cwd"]).resolve() for value in (prior, launch, current))
            or Path(identity["original_consumer"]).resolve() != Path(original["cwd"]).resolve()):
        raise ValueError("Continuation changed host, mode or consumer root")
    if (not selected or selected not in {c["id"] for c in prior.get("children", [])}
            or any(value.get("expected_session_id") != session or value.get("expected_child_id") != selected for value in (launch, current))
            or identity.get("session_id") != session or identity.get("child_id") != selected
            or current.get("session_id") != session or current.get("observed_expected_session") is not True):
        raise ValueError("Continuation did not observe the same parent and selected child identity")
    if current.get("configuration") != prior.get("configuration"):
        raise ValueError("Continuation host/package configuration differs from predecessor")
    verify_inputs(prior)
    verify_inputs(current)
    children = {c["id"]: c for c in [*prior.get("children", []), *current.get("children", [])]}
    combined = {**current, "children": list(children.values()), "calls": [*prior.get("calls", []), *current.get("calls", [])]}
    return combined, {"predecessor": predecessor, "continuation": file_reference(resumed / "continuation.json"),
                      "session_id": session, "selected_child_id": selected, "observed_expected_session": True,
                      "scope": "Same parent resumed; original child evidence retained. No new child work is inferred."}


def confined(root: Path, name: str) -> Path:
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Evidence path escapes consumer")
    return path


def successful_calls(journals: list[list[dict]], root: Path) -> list[dict]:
    return bind_exports([{**c, "server": "pixl_local"} for c in native_calls(journals) if c["success"]], root)


def claude_completion(parent: list[dict], selected: str | None) -> list[dict]:
    calls, proof = {}, []
    for row in parent:
        blocks = row.get("message", {}).get("content", []) if isinstance(row.get("message"), dict) else []
        for block in blocks if isinstance(blocks, list) else []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("name") == "Agent" and block.get("input", {}).get("subagent_type") == "pixl:pixl":
                calls[block.get("id")] = row
            result = row.get("tool_use_result", {})
            if (block.get("type") == "tool_result" and not block.get("is_error") and block.get("tool_use_id") in calls
                    and result.get("status") == "completed" and result.get("agentId") == selected and selected):
                proof.append({"file": row.get("file"), "line": row.get("line"), "agent_id": selected, "call_id": block["tool_use_id"]})
    return proof


def bound_sources(document: dict, root: Path) -> dict:
    document = copy.deepcopy(document)
    for source in document.get("sources", []):
        if "sha256" not in source and confined(root, source["path"]).is_file():
            source["sha256"] = sha(root / source["path"])
    return document


def native_read_proof(journals: list[list[dict]], path: Path) -> list[dict]:
    """Accept complete numbered content from a successful path-bound host Read."""
    target = str(path.resolve()).replace("\\", "/").lower()
    expected = normalized(path.read_text(encoding="utf-8"))
    proof = []
    for journal in journals:
        calls = {}
        for row in journal:
            blocks = row.get("message", {}).get("content", []) if isinstance(row.get("message"), dict) else []
            for block in blocks if isinstance(blocks, list) else []:
                if not isinstance(block, dict):
                    continue
                if (row.get("type") == "assistant" and block.get("type") == "tool_use" and block.get("name") == "Read"
                        and str(block.get("input", {}).get("file_path", "")).replace("\\", "/").lower() == target):
                    calls[block.get("id")] = row
                if (row.get("type") != "user" or block.get("type") != "tool_result" or block.get("is_error")
                        or block.get("tool_use_id") not in calls):
                    continue
                for text in strings(block.get("content", [])):
                    displayed = text.replace("\r\r\n", "\n").replace("\r\n", "\n")
                    numbered = [re.fullmatch(r"\s*(\d+)\t(.*)", line) for line in displayed.splitlines()]
                    if (all(numbered) and [int(m[1]) for m in numbered if m] == list(range(1, len(numbered) + 1))
                            and normalized("\n".join(m[2] for m in numbered if m)) == expected):
                        proof.append({"file": row.get("file"), "line": row.get("line"), "method": "paired_Read_full_file", "sha256": sha(path)})
    return proof


def plar_skill_proof(journals: list[list[dict]], root: Path) -> list[dict]:
    """Bind the operational PLAR body to a selected child's successful host read."""
    path = root / KIT / "skills/plar/SKILL.md"
    expected = normalized(path.read_text(encoding="utf-8"))
    body = normalized(expected.split("\n---\n", 1)[1]) if expected.startswith("---\n") else expected
    target = str(path.resolve()).replace("\\", "/").lower()
    proof = []
    for journal in journals:
        calls, successes = {}, set()
        for row in journal:
            payload = row.get("payload", {})
            item = payload.get("item", row.get("item", {}))
            command = str(item.get("command", "")).replace("\\", "/").lower()
            if (item.get("type") in ("CommandExecution", "command_execution") and item.get("exit_code") == 0
                    and (target in command or "skills/plar/skill.md" in command)
                    and expected in normalized(str(item.get("aggregated_output", "")))):
                proof.append({"file": row.get("file"), "line": row.get("line"), "method": "successful_command_full_file"})
            blocks = row.get("message", {}).get("content", []) if isinstance(row.get("message"), dict) else []
            for block in blocks if isinstance(blocks, list) else []:
                if not isinstance(block, dict):
                    continue
                if row.get("type") == "assistant" and block.get("type") == "tool_use":
                    calls[block.get("id")] = block
                if row.get("type") != "user" or block.get("type") != "tool_result" or block.get("is_error"):
                    continue
                call = calls.get(block.get("tool_use_id"), {})
                args = call.get("input", {})
                if call.get("name") == "Skill" and args.get("skill") == "pixl:plar":
                    successes.add(block.get("tool_use_id"))
                if call.get("name") == "Read" and str(args.get("file_path", "")).replace("\\", "/").lower() == target:
                    for text in strings(block.get("content", [])):
                        lines = text.replace("\r\r\n", "\n").replace("\r\n", "\n").splitlines()
                        numbered = [re.fullmatch(r"\s*(\d+)\t(.*)", line) for line in lines]
                        if (all(numbered) and [int(m[1]) for m in numbered if m] == list(range(1, len(lines) + 1))
                                and normalized("\n".join(m[2] for m in numbered if m)) == expected):
                            proof.append({"file": row.get("file"), "line": row.get("line"), "method": "paired_Read_full_file"})
            if row.get("type") == "user" and row.get("isMeta") is True and row.get("sourceToolUseID") in successes:
                prefix = "Base directory for this skill: " + str(path.parent).replace("\\", "/")
                for text in strings(blocks):
                    actual = normalized(text)
                    first, _, remainder = actual.partition("\n")
                    if first.replace("\\", "/").lower() == prefix.lower() and normalized(remainder) == body:
                        proof.append({"file": row.get("file"), "line": row.get("line"), "method": "bound_Skill_operational_body", "frontmatter_returned": False})
    return proof


def source_proofs(calls: list[dict], root: Path, name: str) -> dict:
    """Require returned exact bytes covering the file, not a path or author claim."""
    path = confined(root, name)
    lines = path.read_bytes().decode("utf-8-sig").splitlines(keepends=True)
    digest, evidence = sha(path), []
    covered: set[int] = set()
    for call in calls:
        args = call["arguments"]
        if (call["tool"] != "pixl_source" or args.get("path") != name or args.get("expect") != digest
                or args.get("scope", "project") != "project"):
            continue
        start, end = args.get("start"), args.get("end")
        if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(lines):
            continue
        expected = {"text": "".join(lines[start - 1:end]), "sha256": digest, "start": start, "end": end}
        if any(all(value.get(k) == v for k, v in expected.items()) for value in expanded_objects(call["result"])):
            covered.update(range(start, end + 1))
            evidence.append({k: call[k] for k in ("file", "line", "tool", "arguments")})
    return {"complete": covered == set(range(1, len(lines) + 1)), "sha256": digest,
            "covered_lines": len(covered), "total_lines": len(lines), "native": evidence}


def allocation_errors(before: dict, after: dict, fixture: dict, root: Path) -> list[str]:
    errors = []
    plar.validate(after, root)
    old = {a["id"]: a for a in before["assets"]}
    new = {a["id"]: a for a in after["assets"]}
    if set(new) != set(old):
        errors.append("Stable asset IDs changed or a duplicate visual role was added")
        return errors
    if after["project"] != before["project"]:
        errors.append("Shared project meaning changed")
    for ident in fixture["unaffected_assets"]:
        if new[ident] != old[ident]:
            errors.append("Unrelated asset changed: " + ident)
    ident = fixture["changed_asset"]
    for key in ("kind", "purpose", "status", "delivery", "depends_on", "existing", "production", "evidence"):
        if new[ident].get(key) != old[ident].get(key):
            errors.append("Existing Start role/history changed: " + key)
    for key in ("requirements", "consumers", "references"):
        if any(row not in new[ident].get(key, []) for row in old[ident].get(key, [])):
            errors.append("Original Start declaration removed: " + key)
    old_sources = {s["id"]: s for s in before["sources"]}
    sources = {s["id"]: s for s in after["sources"]}
    if any(sources.get(k) != v for k, v in old_sources.items()):
        errors.append("Original source binding changed, including pre-existing drift")
    relevant = {c["source"] for c in new[ident]["consumers"]}
    relevant.update(s for r in new[ident]["requirements"] for s in r["sources"])
    relevant.update(r["source"] for r in new[ident].get("references", []))
    permitted_paths = {"SOURCE-MAP.md", fixture["existing_path"], *(c["path"] for c in fixture["new_consumers"])}
    for key in set(sources) - set(old_sources):
        s = sources[key]
        if key not in relevant or s["path"] not in permitted_paths or s.get("sha256") != sha(confined(root, s["path"])):
            errors.append("New source is unbound or unrelated to Start: " + key)
    for consumer in fixture["new_consumers"]:
        if not any(sources[c["source"]]["path"] == consumer["path"] and c["symbol"] == consumer["symbol"]
                   for c in new[ident]["consumers"]):
            errors.append("New actual consumer is not attached to Start: " + consumer["path"])
    observed_paths = permitted_paths | {"src/queue-view.ts", "src/queue.ts", "BRIEF.md"}
    added_paths = {c["path"] for c in fixture["new_consumers"]}
    for requirement in new[ident]["requirements"]:
        if requirement not in old[ident]["requirements"] and (requirement["authority"] != "observation"
                or not any(sources[s]["path"] in added_paths for s in requirement["sources"])
                or any(sources[s]["path"] not in observed_paths for s in requirement["sources"])):
            errors.append("Added Start requirement is not a source-backed scoped observation")
    return errors


def coverage_errors(report: dict, source_map: dict, fixture: dict, root: Path) -> list[str]:
    """Check this declared frontier; this is not general semantic coverage analysis."""
    errors = []
    cases = report["rows"]
    if {c.get("classification") for c in cases} != {"existing", "reused", "missing", "dynamic", "uninspected"}:
        errors.append("Five distinct coverage classes were not retained")
    if not report.get("limits") or not source_map.get("limits") or any(not c.get("limitation") for c in cases):
        errors.append("Coverage scope/limitations absent")
    for case in cases:
        name, classification = case.get("file", {}).get("path"), case.get("classification")
        if name in fixture["missing_paths"] and classification != "missing":
            errors.append("Contradictory classification for missing destination: " + name)
        if name in fixture["uninspected"] and (classification != "uninspected" or case.get("inspection") != "not_inspected"):
            errors.append("Contradictory classification for uninspected source: " + name)
        if classification in ("existing", "reused") and (not name or not confined(root, name).is_file()):
            errors.append("Existing/reused file is absent")
    for classification in ("existing", "reused"):
        matching = [c for c in cases if c.get("classification") == classification
                    and c.get("file", {}).get("path") == fixture["existing_path"]]
        if not matching or any(c.get("inspection") != "inspected" or c["file"].get("sha256") != sha(root / fixture["existing_path"])
                               for c in matching):
            errors.append("Existing/reused Start is not bound to inspected original bytes: " + classification)
    reused = [c for c in cases if c.get("classification") == "reused"]
    for target in fixture["new_consumers"]:
        if not any(any(c.get("path") == target["path"] and c.get("symbol") == target["symbol"]
                       for c in row.get("consumers", [])) for row in reused):
            errors.append("Reuse coverage omits actual new consumer: " + target["path"])
    for name in fixture["missing_paths"]:
        found = [c for c in cases if c.get("classification") == "missing" and c.get("file", {}).get("path") == name]
        if (root / name).exists() or not found or any(c["file"].get("sha256") for c in found):
            errors.append("Missing destination is invented or falsely present: " + name)
    if not any(c.get("classification") == "dynamic" and c.get("inspection") in ("inspected", "unavailable")
               and any(s.get("path") == "src/queue-view.ts" and s.get("symbol") == "accountBadge" for s in c.get("consumers", []))
               for c in cases):
        errors.append("Dynamic badge code and unavailable remote enumeration are not distinguished")
    files = {f["path"]: f for f in source_map["files"]}
    for name in fixture["uninspected"]:
        found = [c for c in cases if c.get("classification") == "uninspected" and c.get("file", {}).get("path") == name]
        if not (root / name).is_file() or not found or any(c.get("inspection") != "not_inspected" for c in found):
            errors.append("Present uninspected source misclassified: " + name)
        if files.get(name, {}).get("inspection") != "not_inspected":
            errors.append("Source map does not preserve the uninspected boundary: " + name)
    for f in source_map["files"]:
        if f.get("sha256") != sha(confined(root, f["path"])):
            errors.append("Source map hash differs: " + f["path"])
    for name in CHILD_SOURCES[1:]:
        if files.get(name, {}).get("inspection") != "inspected":
            errors.append("Inspected source missing from source map: " + name)
    mappings = {m["state"]: m for m in source_map["mappings"]}
    for state, asset in STATES.items():
        m = mappings.get(state, {})
        consumers = {(c.get("path"), c.get("symbol")) for c in m.get("consumers", [])}
        expected = {("src/queue-view.ts", s) for s in ("statusCell", "compactStatus")}
        if state == "idle":
            expected.update((c["path"], c["symbol"]) for c in fixture["new_consumers"])
        if m.get("asset_id") != asset or not expected <= consumers:
            errors.append("Incorrect state/function/asset mapping: " + state)
        if state in TRANSITIONS and m.get("transition") != {"path": "src/queue.ts", "symbol": "stateAfter", "input": TRANSITIONS[state]}:
            errors.append("Incorrect backend transition: " + state)
    return errors


def uninspected_reads(journals: list[list[dict]], root: Path, names: list[str]) -> list[dict]:
    """Audit explicit content tools/commands and returned full source, not arbitrary execution."""
    findings = []
    for journal in journals:
        for row in journal:
            payload = row.get("payload", {})
            item = payload.get("item", row.get("item", {}))
            blocks = row.get("message", {}).get("content", []) if isinstance(row.get("message"), dict) else []
            for name in names:
                leaf = Path(name).name.lower()
                direct = item.get("tool") == "pixl_source" and leaf in str(item.get("arguments", {}).get("path", "")).lower()
                commands = []
                returned_blocks = []
                for b in blocks if isinstance(blocks, list) else []:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") == "tool_use":
                        if b.get("name") in ("Read", "Grep", "view_image") or str(b.get("name", "")).endswith("__pixl_source"):
                            direct |= leaf in json.dumps(b.get("input", {})).lower()
                        if b.get("name") == "Bash":
                            commands.append(str(b.get("input", {}).get("command", "")))
                    if b.get("type") == "tool_result":
                        returned_blocks.append(b.get("content", []))
                if item.get("type") in ("CommandExecution", "command_execution"):
                    commands.append(str(item.get("command", "")))
                for command in commands:
                    # The assignment explicitly permits hashes without exposing
                    # contents. Remove only this literal hash-only expression;
                    # other reads and any returned full source remain auditable.
                    command = re.sub(r"(?:hashlib\.)?sha256\((?:Path|pathlib\.Path)\([^\n;]*?\)\.read_bytes\(\)\)\.hexdigest\(\)", "HASH_ONLY", command)
                    direct |= bool(re.search(r"(?:get-content|\bcat\b|\btype\b)[^\n;|]*" + re.escape(leaf), command, re.IGNORECASE))
                    direct |= bool(re.search(re.escape(leaf) + r"[^\n;]{0,80}\.(?:read_text|read_bytes)\s*\(", command, re.IGNORECASE))
                actual = normalized((root / name).read_text(encoding="utf-8"))
                returned = [item.get("aggregated_output", item.get("result", "")), *returned_blocks]
                direct |= bool(actual and len(actual) > 80 and any(actual in normalized(t) for t in strings(returned)))
                if direct:
                    findings.append({"file": row.get("file"), "line": row.get("line"), "path": name})
    return findings


def _grade(attempt: Path, continuation_attempt: Path | None = None) -> dict:
    attempt = attempt.resolve()
    launch, identity, continuation = (read(attempt / name) for name in ("launch.json", "identity.json", "continuation.json"))
    root = Path(launch["cwd"]).resolve()
    caller = report_fields(read(root / WORK / "CALLER-RESULT.json"))
    fixture, baseline = identity["fixture"], identity["baseline_document"]
    original_hash = identity["original_inputs"]["plar.txt"]
    checks = []
    def check(name, passed, evidence=None):
        checks.append({"check": name, "pass": bool(passed), "evidence": evidence})
    journals = [rows(p) for p in sorted(attempt.glob("native-*.jsonl"))]
    journals += [rows(p) for p in sorted((attempt / "native-transcripts").glob("*.jsonl"))]
    stdout = rows(attempt / "stdout.jsonl")
    selected = selected_child(caller.get("native_child"), launch["host"])
    if continuation_attempt is not None:
        continuation_attempt = continuation_attempt.resolve()
        continuation, evidence = continuation_record(attempt, continuation_attempt, selected)
        check("same_parent_continuation_identity_and_configuration_verified", True, evidence)
        journals += [rows(p) for p in sorted(continuation_attempt.glob("native-*.jsonl"))]
        journals += [rows(p) for p in sorted((continuation_attempt / "native-transcripts").glob("*.jsonl"))]
        stdout += rows(continuation_attempt / "stdout.jsonl")
    if launch["host"] == "codex":
        parent = next((j for j in journals if j and j[0].get("payload", {}).get("id") == continuation["session_id"]), [])
        role = tomllib.loads((root / ".codex/agents/pixl.toml").read_text(encoding="utf-8"))["developer_instructions"]
        proof = codex_role_proof(journals, continuation["session_id"], selected, role, require_isolated=False)
        ids = {c["id"] for c in proof["selected_children"]}
        children = [[j[0], *own_rows(j, continuation["session_id"], cold=True)]
                    for j in journals if j and j[0].get("payload", {}).get("id") in ids]
        check("actual_named_child_selected_and_completed", proof["loaded"] and proof["completed"], {k: v for k, v in proof.items() if k != "child_text"})
    else:
        parent = [r for r in stdout if not r.get("parent_tool_use_id") and not r.get("agent_id")]
        children = [j for j in journals if j and Path(j[0]["file"]).stem.removeprefix("agent-") == selected]
        loading = claude_loading_proof(children, root / KIT)
        completion = claude_completion(parent, selected)
        check("actual_named_child_selected_and_completed",
              any(c.get("id", c.get("agent_id")) == selected and c.get("role") == "pixl:pixl" for c in continuation.get("children", []))
              and bool(completion), {"common_production_loading": loading, "completion": completion,
                  "common_production_loading_required_for_allocation": False,
                  "scope": "Actual named role and selected child return; PLAR operational loading is separately required. Common production sources are reported only if observed."})
    child_calls, parent_calls = successful_calls(children, root), successful_calls([parent], root)
    plar_loading = plar_skill_proof(children, root)
    check("selected_child_loaded_operational_PLAR_skill", bool(plar_loading), plar_loading)
    values = {name: semantic_result(read(reference(root, caller[name]))) for name in
              ("coverage", "source_map", "initial_read", "update_save", "parent_refresh", "specialist_result")}
    final = read(root / "plar.txt")
    check("authored_final_document_is_actual_saved_allocation", bound_sources(read(root / WORK / "final-document.json"), root) == final)
    check("scope_and_action_are_explicit", bool(caller.get("scope")) and bool(caller.get("limits")) and bool(caller.get("next_action")))
    specialist = report_fields(values["specialist_result"])
    check("specialist_report_binds_returned_artifacts", all(specialist.get(k) == caller[k] for k in ("coverage", "source_map", "initial_read", "update_save"))
          and bound_sources(read(reference(root, specialist["final_document"])), root) == final)
    for name in CHILD_SOURCES:
        proof = source_proofs(child_calls, root, name)
        if name == "SOURCE-MAP.md" and not proof["complete"]:
            overview_reads = native_read_proof(children, root / name)
            proof.update(complete=bool(overview_reads), native=overview_reads,
                         mechanism="complete path-bound native Read for evaluation overview only")
        check("child_inspected_" + name, proof["complete"], proof)
    for name in ("src/start-shortcut.mjs", "src/shortcut-entry.mjs"):
        proof = source_proofs(parent_calls, root, name)
        check("parent_independently_inspected_" + name, proof["complete"], proof)
    initial = values["initial_read"]
    check("child_read_actual_baseline_queue", initial.get("hash") == original_hash and initial.get("changes") == identity["baseline_changes"]
          and bool(matching_calls(child_calls, "pixl_plar_read", initial)))
    save = values["update_save"]
    saves = matching_calls(child_calls, "pixl_plar_save", save, {"expect": original_hash})
    actual_saves = []
    for call in saves:
        document = bound_sources(call["arguments"].get("document", {}), root)
        if document == final and call["arguments"].get("path", "plar.txt") == "plar.txt":
            actual_saves.append(call)
    check("child_published_guarded_actual_allocation", bool(actual_saves) and save.get("hash") == sha(root / "plar.txt"), actual_saves)
    errors = allocation_errors(baseline, final, fixture, root)
    check("new_consumer_reuses_Start_without_changing_unrelated_rows", not errors, errors)
    errors = coverage_errors(values["coverage"], values["source_map"], fixture, root)
    check("source_state_function_mapping_and_five_coverage_boundaries", not errors, errors)
    entrypoint = read(attempt / "entrypoint-observation.json")
    check("fixture_entrypoint_observed_existing_Start_descriptor", entrypoint.get("returncode") == 0
          and json.loads(entrypoint["stdout"]) == {"label": "Start", "path": fixture["existing_path"], "frames": 1}
          and str(root / "src/shortcut-entry.mjs") in entrypoint["command"],
          {"scope": "Runner's local descriptor execution; not native viewing or rendered acceptance", "returncode": entrypoint.get("returncode")})
    refreshed = values["parent_refresh"]
    current = service.call("pixl_plar_read", {"since": original_hash}, root)
    check("parent_executed_exact_history_refresh", refreshed == current
          and bool(matching_calls(parent_calls, "pixl_plar_read", refreshed, {"since": original_hash})))
    changes = refreshed["changes"]
    check("preexisting_shared_source_drift_remains_explicit", all(s in changes["changed_sources"] for s in identity["baseline_changes"]["changed_sources"])
          and any(s.get("binding") == "changed" for s in refreshed["sources"]), {"before": identity["baseline_changes"], "after": changes})
    selections = caller["parent_selections"]
    for ident in STATES.values():
        result = semantic_result(read(reference(root, selections[ident])))
        actual = service.call("pixl_plar_read", {"asset_id": ident}, root)
        check("parent_observed_current_selection_" + ident, result == actual
              and bool(matching_calls(parent_calls, "pixl_plar_read", result, {"asset_id": ident})))
        before = identity["baseline_selections"][ident]
        equal = actual["requirements_hash"] == before["requirements_hash"]
        check("selected_requirements_identity_" + ident, equal == (ident in fixture["unaffected_assets"]),
              {"before": before["requirements_hash"], "after": actual["requirements_hash"]})
        if ident in fixture["unaffected_assets"]:
            check("retained_production_evidence_" + ident, actual["asset"] == before["asset"] and actual["production"] == before["production"])
    history = root / ".pixl/plar-history" / (original_hash + ".json")
    check("exact_original_allocation_retained_in_history", sha(history) == original_hash and read(history) == baseline)
    current_files = inventory(root, ("__pycache__",))
    drift = [p for p, digest in identity["inputs"].items() if p != "plar.txt" and current_files.get(p) != digest]
    additions = [p for p in current_files if p not in identity["inputs"] and not p.startswith((WORK + "/", ".pixl/plar-history/"))]
    bad_history = [p for p in current_files if p not in identity["inputs"] and p.startswith(".pixl/plar-history/")
                   and (Path(p).suffix != ".json" or Path(p).stem != current_files[p])]
    check("all_original_files_production_and_prior_history_preserved", not drift and not additions and not bad_history,
          {"changed": drift, "unexpected": additions, "invalid_new_history": bad_history})
    attempts = mcp_attempts(journals + [stdout])
    prohibited = [c for c in attempts if str(c["server"]).replace("-", "_") != "pixl_local" or c["tool"] not in READ_TOOLS]
    check("no_provider_production_art_or_acceptance_tool_attempts", not prohibited, prohibited)
    observed = uninspected_reads(journals + [stdout], root, fixture["uninspected"])
    check("no_observed_content_read_of_present_uninspected_file", not observed, observed)
    check("native_attempt_completed", continuation.get("status") == "finished" and continuation.get("returncode") == 0
          and continuation.get("interruption_reason") is None)
    return {"version": 1, "status": "pass" if all(c["pass"] for c in checks) else "fail", "checks": checks,
            "passed": sum(c["pass"] for c in checks), "total": len(checks),
            "scope": "Bounded native source allocation and parent verification on this declared frontier. No exhaustive semantic, provider, art or renderer acceptance claim. Uninspected-read audit covers explicit recorded tools/commands and returned full source, not every possible indirect program."}


def grade(attempt: Path, continuation: Path | None = None) -> dict:
    try:
        return _grade(attempt, continuation)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        return {"version": 1, "status": "fail", "passed": 0, "total": 1,
                "checks": [{"check": "required_evidence_readable", "pass": False, "evidence": f"{type(error).__name__}: {error}"}]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attempt", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--continuation", type=Path, help="Additive same-parent continuation attempt directory; preserve original attempt")
    args = parser.parse_args(argv)
    if args.output.exists():
        raise ValueError("Preserve prior grades; choose a fresh output")
    result = grade(args.attempt, args.continuation)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({k: result[k] for k in ("status", "passed", "total")}))
    return result["status"] != "pass"


if __name__ == "__main__":
    raise SystemExit(main())
