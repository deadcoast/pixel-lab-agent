"""Read-only CF-05 checks against retained native journals and actual output bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tomllib
import zipfile
from pathlib import Path

from evaluations.host_trials import inventory, sha, write_json
from pixl import candidate_review, codec, plar, store


def rows(path: Path) -> list[dict]:
    result = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict):
            result.append({**event, "line": number, "file": str(path)})
    return result


def normalized(text: str) -> str:
    # The Windows shell journal can expand CRLF to CRCRLF. Compare displayed
    # instruction/source text independently of the separately checked file bytes.
    return text.replace("\r\r\n", "\n").replace("\r\n", "\n").strip()


def own_rows(journal: list[dict], parent: str, *, cold: bool = False) -> list[dict]:
    meta = journal[0]["payload"]
    if meta.get("id") == parent:
        return journal[1:]
    if cold and not meta.get("forked_from_id") and meta.get("subagent_history_start_ordinal") is None:
        return journal[1:]
    start = meta.get("subagent_history_start_ordinal")
    return [r for r in journal[1:] if isinstance(start, int)
            and isinstance(r.get("ordinal"), int) and r["ordinal"] >= start]


def command_rows(journal: list[dict]) -> list[dict]:
    return [r for r in journal if r.get("payload", {}).get("type") == "item_completed"
            and r["payload"].get("item", {}).get("type") == "CommandExecution"]


def command_text(row: dict) -> str:
    return json.dumps(row["payload"]["item"].get("command", []), ensure_ascii=False)


def trace_facts(journals: list[list[dict]], parent: str, role_text: str) -> dict:
    """Keep raw tool exposure, requested roles and native selected roles distinct."""
    by_id = {j[0]["payload"].get("id"): j for j in journals if j and j[0].get("type") == "session_meta"}
    parent_rows = by_id.get(parent, [])
    children = []
    for ident, journal in by_id.items():
        if ident == parent:
            continue
        meta = journal[0]["payload"]
        source = meta.get("source", {})
        spawn = source.get("subagent", {}).get("thread_spawn", {}) if isinstance(source, dict) else {}
        if spawn.get("parent_thread_id") == parent and meta.get("session_id", ident) == parent:
            children.append({"id": ident, "role": spawn.get("agent_role"), "agent_path": spawn.get("agent_path"),
                             "cwd": meta.get("cwd"), "file": journal[0]["file"], "line": 1})
    schemas, calls = [], []
    for row in parent_rows:
        payload = row.get("payload", {})
        if payload.get("type") == "additional_tools":
            for namespace in payload.get("tools", []):
                if namespace.get("name") != "collaboration":
                    continue
                for tool in namespace.get("tools", []):
                    if tool.get("name") == "spawn_agent":
                        schemas.append({"file": row["file"], "line": row["line"],
                                        "parameters": sorted(tool.get("parameters", {}).get("properties", {})),
                                        "description": tool.get("description", "")})
        if payload.get("type") == "function_call" and payload.get("namespace") == "collaboration":
            try:
                args = json.loads(payload.get("arguments", "{}"))
            except (ValueError, TypeError):
                args = {}
            if isinstance(args, dict):
                calls.append({"tool": payload.get("name"), "id": payload.get("call_id"),
                              "requested_role": args.get("agent_type"), "to": args.get("target"),
                              "fork_turns": args.get("fork_turns"),
                              "file": row["file"], "line": row["line"], "timestamp": row.get("timestamp"),
                              "parent_turn": payload.get("internal_chat_message_metadata_passthrough", {}).get("turn_id")})
    for call in calls:
        for row in parent_rows:
            payload = row.get("payload", {})
            if payload.get("type") == "function_call_output" and payload.get("call_id") == call["id"]:
                call.update(result_line=row["line"], result_observed=True, result_error=payload.get("is_error", False))
            item = payload.get("item", {})
            if (payload.get("type") == "item_completed" and item.get("type") == "SubAgentActivity"
                    and item.get("id") == call["id"]):
                call.update(activity_line=row["line"], activity_kind=item.get("kind"),
                            child_id=item.get("agent_thread_id"), activity_timestamp=row.get("timestamp"))
    injected = []
    parent_developer = set()
    for row in parent_rows:
        p = row.get("payload", {})
        if p.get("type") == "message" and p.get("role") == "developer":
            parent_developer.update(normalized(c["text"]) for c in p.get("content", []) if isinstance(c.get("text"), str))
    for child in children:
        for row in by_id[child["id"]]:
            p = row.get("payload", {})
            if p.get("type") != "message" or p.get("role") != "developer":
                continue
            for c in p.get("content", []):
                text = c.get("text", "")
                if isinstance(text, str) and normalized(role_text) in normalized(text):
                    injected.append({"child": child["id"], "file": row["file"], "line": row["line"],
                                     "inherited_parent_text": normalized(text) in parent_developer,
                                     "text_sha256": hashlib.sha256(text.encode()).hexdigest()})
    selected = [c for c in children if c["role"] == "pixl"]
    cold_children = {c["child_id"] for c in calls if c["tool"] == "spawn_agent" and c.get("fork_turns") == "none"
                     and c.get("result_observed") and not c.get("result_error") and c.get("child_id") in by_id}
    continued = []
    for child in selected:
        targets = {child["id"], child["agent_path"], (child["agent_path"] or "").removeprefix("/root/")}
        for call in calls:
            if call["tool"] not in {"followup_task", "send_message"} or call["to"] not in targets:
                continue
            delivered = (call.get("result_observed") and not call.get("result_error")
                         and call.get("activity_kind") == "interacted" and call.get("child_id") == child["id"])
            after = [r for r in own_rows(by_id[child["id"]], parent, cold=child["id"] in cold_children)
                     if r.get("timestamp", "") > (call.get("activity_timestamp") or call["timestamp"] or "")]
            starts = [r for r in after if r.get("payload", {}).get("type") == "task_started"
                      and r["payload"].get("turn_attribution", {}).get("parent_turn_id") == call["parent_turn"]]
            turns = {r["payload"]["turn_id"] for r in starts}
            finals = [r for r in after if r.get("payload", {}).get("type") == "task_complete"
                      and r["payload"].get("turn_id") in turns]
            commands = [r for r in command_rows(after) if r["payload"].get("turn_id") in turns]
            round2 = [r for r in commands if "SPECIALIST-ROUND2.json" in json.dumps(r["payload"]["item"])]
            continued.append({"child": child["id"], "call": call,
                              "delivered_to_observed_child": bool(delivered), "new_turn_start_lines": [r["line"] for r in starts],
                              "later_final_lines": [r["line"] for r in finals],
                              "later_command_lines": [r["line"] for r in commands],
                              "round2_artifact_lines": [r["line"] for r in round2]})
    return {"schemas": schemas, "calls": calls, "children": children, "instruction_matches": injected,
            "continuations": continued, "cold_children": sorted(cold_children), "journals": by_id}


def named_route_checks(facts: dict) -> list[tuple[str, bool, object]]:
    selected = [c for c in facts["children"] if c["role"] == "pixl"]
    spawns = [c for c in facts["calls"] if c["tool"] == "spawn_agent"]
    return [
        ("native_tool_exposes_role_selection", any("agent_type" in s["parameters"] for s in facts["schemas"]), facts["schemas"]),
        ("one_explicit_pixl_spawn", len(spawns) == 1 and spawns[0]["requested_role"] == "pixl", spawns),
        ("one_actual_named_child", len(facts["children"]) == 1 and len(selected) == 1, facts["children"]),
        ("configured_role_instructions_loaded", any(not m["inherited_parent_text"] and m["child"] in {c["id"] for c in selected}
                                                   for m in facts["instruction_matches"]), facts["instruction_matches"]),
        ("same_child_completed_after_followup", any(c["call"]["tool"] == "followup_task"
                                                   and c["delivered_to_observed_child"] and c["new_turn_start_lines"]
                                                   and c["later_final_lines"] and c["round2_artifact_lines"]
                                                   for c in facts["continuations"]), facts["continuations"]),
    ]


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)


def public_mcp_proofs(journal: list[dict], operation: str, required: list[str],
                      result_path: str, result_sha256: str) -> list[dict]:
    tools = {"review-context": "pixl_review_context", "candidate-review": "pixl_candidate_review",
             "plar handoff": "pixl_plar_handoff"}
    proofs = []
    for row in journal:
        payload = row.get("payload", {})
        item = payload.get("item", {})
        result = item.get("result", {})
        if (payload.get("type") != "item_completed" or item.get("type") != "McpToolCall"
                or item.get("tool") != tools[operation] or item.get("server") != "pixl_local"
                or item.get("status") != "completed" or result.get("isError") is not False):
            continue
        args, summary = item.get("arguments", {}), result.get("structuredContent", {})
        if (args.get("result_path") == result_path and all(v in json.dumps(args) for v in required)
                and summary.get("result_path") == result_path and summary.get("result_sha256") == result_sha256):
            proofs.append({"route": "mcp", "file": row["file"], "line": row["line"], "tool": item["tool"],
                           "result_path": result_path, "result_sha256": result_sha256})
    return proofs


def public_cli_proofs(journal: list[dict], consumer: Path, operation: str, required: list[str],
                      result_path: str, result_sha256: str) -> list[dict]:
    """Correlate completed native CLI/script execution with the saved public result."""
    proofs = []
    for row in command_rows(journal):
        item = row["payload"]["item"]
        if item.get("exit_code") != 0:
            continue
        command = " ".join(item.get("command", []))
        output = item.get("aggregated_output", "")
        scripts = []
        # This evaluation permits small subprocess collectors. A script's source
        # and returned receipt must accompany its observed successful execution.
        if "python.exe" in command.lower() and "Get-Content" not in command:
            for name in re.findall(r"work/named-role/[A-Za-z0-9_-]+\.py", command):
                path = consumer / name
                if path.is_file():
                    text = path.read_text(encoding="utf-8")
                    if "subprocess.run" in text and "scripts/pixl.py" in text:
                        scripts.append((name, text))
        candidates = [(None, command)] if "scripts/pixl.py" in command and "Get-Content" not in command else []
        candidates += scripts
        for script, text in candidates:
            if not all(word in text for word in (operation, result_path, *required)):
                continue
            # A replay receipt exposes the exact saved hash. Export collectors may
            # save receipts to disk and print only result keys; retain that receipt.
            receipt_matches = result_sha256 in output and result_path in output
            receipt_paths = []
            if script:
                for path in (consumer / "work/named-role").glob("*.json"):
                    try:
                        receipt = json.loads(path.read_bytes())
                    except ValueError:
                        continue
                    if (isinstance(receipt, dict) and receipt.get("result_path") == result_path
                            and receipt.get("result_sha256") == result_sha256
                            and path.name in text):
                        receipt_paths.append({"path": path.relative_to(consumer).as_posix(), "sha256": sha(path)})
                receipt_matches = receipt_matches or bool(receipt_paths)
            if receipt_matches:
                proofs.append({"file": row["file"], "line": row["line"], "turn_id": row["payload"].get("turn_id"),
                               "script": script, "script_sha256": sha(consumer / script) if script else None,
                               "result_path": result_path, "result_sha256": result_sha256, "receipts": receipt_paths})
    return proofs


def public_operation_proofs(journal: list[dict], consumer: Path, operation: str, required: list[str],
                           result_path: str, result_sha256: str) -> list[dict]:
    return (public_cli_proofs(journal, consumer, operation, required, result_path, result_sha256)
            + public_mcp_proofs(journal, operation, required, result_path, result_sha256))


def grade(attempt: Path) -> dict:
    attempt = attempt.resolve()
    launch = json.loads((attempt / "launch.json").read_bytes())
    identity = json.loads((attempt / "identity.json").read_bytes())
    continuation = json.loads((attempt / "continuation.json").read_bytes())
    consumer = Path(launch["cwd"]).resolve()
    work = consumer / "work/named-role"
    checks = []

    def check(name, passed, evidence):
        checks.append({"check": name, "pass": bool(passed), "evidence": evidence})

    original_role = identity["original_role"]
    role_path = consumer / ".codex/agents/pixl.toml"
    role = tomllib.loads(role_path.read_text(encoding="utf-8"))
    check("unchanged_repository_role", sha(role_path) == original_role["sha256"], original_role)
    parent = continuation.get("session_id")
    journals = [rows(p) for p in sorted(attempt.glob("native-*.jsonl"))]
    facts = trace_facts(journals, parent, role["developer_instructions"])
    check("cold_parent_identity", launch.get("continuation_mode") == "new_session" and parent in facts["journals"]
          and not any(x in launch["command"] for x in ("resume", "fork")), parent)
    for name, passed, evidence in named_route_checks(facts):
        check(name, passed, evidence)
    check("native_roots_match_consumer", bool(facts["children"]) and all(Path(c["cwd"]).resolve() == consumer for c in facts["children"]), facts["children"])
    read_proofs = []
    specialist_rows = []
    for child in facts["children"]:
        child_rows = own_rows(facts["journals"][child["id"]], parent, cold=child["id"] in facts["cold_children"])
        specialist_rows.extend(child_rows)
        for row in command_rows(child_rows):
            item = row["payload"]["item"]
            for name in ("skills/pixl/SKILL.md", "resources/agent/PROFILE.md"):
                if name in command_text(row) and item.get("exit_code") == 0:
                    expected = normalized((consumer / ".agents/skills/role-kit" / name).read_text(encoding="utf-8"))
                    output = normalized(item.get("aggregated_output", ""))
                    read_proofs.append({"child": child["id"], "entrypoint": name, "file": row["file"], "line": row["line"],
                                        "full_text_observed": expected in output})
    check("child_read_current_shared_skill_and_profile", all(any(p["entrypoint"] == name and p["full_text_observed"] for p in read_proofs)
          for name in ("skills/pixl/SKILL.md", "resources/agent/PROFILE.md")), read_proofs)
    missing, changed = [], []
    for name, digest in identity["inputs"].items():
        path = consumer / name
        if not path.is_file():
            missing.append(name)
        elif sha(path) != digest:
            changed.append(name)
    check("all_original_inputs_unchanged", not missing and not changed,
          {"count": len(identity["inputs"]), "missing": missing, "changed": changed})
    current = inventory(consumer, ("__pycache__",))
    additions = sorted(set(current) - identity["inputs"].keys())
    unexpected = [p for p in additions if not p.startswith("work/named-role/") and not p.startswith(".pixl/handoffs/")]
    check("only_assigned_outputs_and_handoffs_added", not unexpected, {"additions": additions, "unexpected": unexpected})
    copied = attempt / "outputs"
    check("portable_output_copies_match_actual_files", copied.is_dir() and inventory(copied) == inventory(work),
          {"retained": str(copied), "actual": str(work)})
    delta_path = attempt / "consumer-delta.json"
    delta_evidence = {"manifest": str(delta_path)}
    delta_ok = False
    if delta_path.is_file():
        delta = json.loads(delta_path.read_bytes())
        archive = attempt / "consumer-delta.zip"
        expected_delta = {name: digest for name, digest in current.items()
                          if identity["inputs"].get(name) != digest and not name.startswith("work/named-role/")}
        with zipfile.ZipFile(archive) as saved:
            observed = {name: hashlib.sha256(saved.read(name)).hexdigest() for name in saved.namelist()}
        delta_ok = (sha(archive) == delta["archive"]["sha256"] and observed == delta["files"] == expected_delta
                    and sorted(delta["removed"]) == sorted(missing)
                    and sorted(delta["changed_existing"]) == sorted(p for p in changed if not p.startswith("work/named-role/")))
        delta_evidence.update(archive_sha256=sha(archive), entries=observed, removed=delta["removed"], changed_existing=delta["changed_existing"])
    check("portable_delta_preserves_handoffs_and_failed_changes", delta_ok, delta_evidence)
    document = store.load(consumer / ".pixl/assets/queue.ready")
    check("canonical_state_unchanged", codec.digest(document) == identity["baseline_state_hash"],
          {"expected": identity["baseline_state_hash"], "actual": codec.digest(document)})
    reports = {}
    for name in ("SPECIALIST-ROUND1.json", "CALLER-REVIEW.json", "SPECIALIST-ROUND2.json", "CALLER-RESULT.json"):
        path = work / name
        if path.is_file():
            try:
                value = json.loads(path.read_bytes())
                if isinstance(value, dict) and value:
                    reports[name] = value
            except ValueError:
                pass
    check("both_rounds_and_caller_reviews_returned", len(reports) == 4, sorted(reports))
    # A caller's pass assertions are observations, not the grader's evidence.
    # Exact file references are checked independently below.
    refs = []
    for report_name, report in reports.items():
        for obj in objects(report):
            # Family member `path` is relative to its manifest directory. The
            # public retained_path supplies its explicit consumer-root locator.
            path = obj.get("result_path", obj.get("retained_path", obj.get("path")))
            digest = obj.get("result_sha256", obj.get("sha256"))
            if not isinstance(path, str) or not isinstance(digest, str) or len(digest) != 64:
                continue
            target = (consumer / path).resolve()
            if not target.is_relative_to(consumer):
                refs.append({"report": report_name, "path": path, "expected": digest,
                             "match": False, "reason": "Reported path escapes assigned consumer"})
                continue
            refs.append({"report": report_name, "path": path, "expected": digest,
                         "match": target.is_file() and sha(target) == digest})
    check("reported_file_hashes_match_bytes", bool(refs) and all(r["match"] for r in refs), refs)
    output_json = []
    for path in work.glob("*.json"):
        try:
            value = json.loads(path.read_bytes())
        except ValueError:
            continue
        output_json.append((path, value))
    expected_context = candidate_review.context(document, consumer, identity["candidate"])
    contexts = [(p, value) for p, value in output_json if isinstance(value, dict)
                and value.get("candidate") == identity["candidate"] and "criteria" in value and "reused_review" not in value]
    check("exported_context_matches_current_saved_acceptance", bool(contexts) and any(
        all(value.get(key) == expected_context[key] for key in expected_context) for _, value in contexts),
        [{"path": str(p), "sha256": sha(p), "snapshot_acceptance": value.get("snapshot_acceptance"),
          "current_acceptance": value.get("current_acceptance")} for p, value in contexts])
    context_proofs = [proof for path, _ in contexts for proof in public_operation_proofs(
        specialist_rows, consumer, "review-context", [identity["candidate"]], path.relative_to(consumer).as_posix(), sha(path))]
    check("specialist_used_public_context_export", bool(context_proofs), context_proofs)
    source_proofs = []
    for path, value in output_json:
        if not isinstance(value, dict) or not isinstance(value.get("text"), str):
            continue
        start, end, digest = value.get("start"), value.get("end"), value.get("sha256")
        if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
            continue
        for name, original_digest in identity["inputs"].items():
            if digest != original_digest:
                continue
            try:
                lines = (consumer / name).read_text(encoding="utf-8").splitlines(keepends=True)
            except UnicodeError:
                continue
            source_proofs.append({"export": str(path), "source": name, "sha256": digest, "start": start, "end": end,
                                  "exact_text": normalized("".join(lines[start - 1:end])) == normalized(value["text"])})
    check("precise_source_excerpt_matches_retained_input", bool(source_proofs) and all(s["exact_text"] for s in source_proofs), source_proofs)
    replays = [{"path": str(p), "sha256": sha(p), "value": value} for p, value in output_json
               if isinstance(value, dict) and value.get("reused_review") is True
               and "publications" in value and "remote_executed" in value
               and value.get("candidate") == identity["candidate"] and value.get("review") == identity["review"]]
    check("actual_review_replay_reuses_original", bool(replays) and all(
        r["value"].get("state_hash") == identity["baseline_state_hash"]
        and r["value"].get("publications") == [] and r["value"].get("remote_executed") is False for r in replays), replays)
    replay_proofs = [proof for replay in replays for proof in public_operation_proofs(
        specialist_rows, consumer, "candidate-review", [identity["candidate"], identity["review"], "identical-review.json"],
        Path(replay["path"]).relative_to(consumer).as_posix(), replay["sha256"])]
    check("specialist_executed_public_review_replay", bool(replay_proofs), replay_proofs)
    handoffs = []
    for name in additions:
        if name.startswith(".pixl/handoffs/"):
            path = consumer / name
            value = json.loads(path.read_bytes())
            handoffs.append({"path": name, "sha256": sha(path), "value": value})
    check("immutable_handoff_returned", bool(handoffs) and all(Path(h["path"]).stem == h["sha256"] for h in handoffs), handoffs)
    handoff_refs = {(h["path"], h["sha256"]) for h in handoffs}
    handoff_exports = [p for p, value in output_json if isinstance(value, dict)
                       and (value.get("path"), value.get("sha256")) in handoff_refs]
    handoff_proofs = [proof for path in handoff_exports for proof in public_operation_proofs(
        specialist_rows, consumer, "plar handoff", ["queue.working", "authoring-plar.txt", identity["baseline_state_hash"]],
        path.relative_to(consumer).as_posix(), sha(path))]
    check("specialist_executed_public_handoff", bool(handoff_proofs), handoff_proofs)
    selected = plar.read(consumer, path="authoring-plar.txt", asset_id="queue.working")
    check("handoff_preserves_exact_current_selection_and_continuation", bool(handoffs) and all(
        h["value"].get("asset_id") == "queue.working" and h["value"].get("requirements_hash") == selected["requirements_hash"]
        and h["value"].get("resume") == selected["production"]["continuation"]
        and h["value"].get("next") == selected["production"]["continuation"]["action"]
        and h["value"].get("selection") == {"path": "authoring-plar.txt", "hash": selected["hash"],
                                             "current": selected["production"]["selection_current"]} for h in handoffs),
        {"requirements_hash": selected["requirements_hash"], "state_hash": selected["production"]["hash"],
         "next_action": selected["production"]["continuation"]["action"]})
    round_values = [set(strings(reports.get(f"SPECIALIST-ROUND{n}.json", {}))) for n in (1, 2)]
    expected_values = {"queue.working", "authoring-plar.txt", identity["baseline_state_hash"], selected["requirements_hash"]}
    check("rounds_preserve_selected_scope_and_root", all(expected_values <= values
          and consumer.as_posix().lower() in {v.replace("\\", "/").lower() for v in values} for values in round_values),
          {"required_values": sorted(expected_values), "consumer_root": str(consumer)})
    caller = reports.get("CALLER-RESULT.json", {})
    caller_review = reports.get("CALLER-REVIEW.json", {})
    caller_refs = [r for r in refs if r["report"] in {"CALLER-RESULT.json", "CALLER-REVIEW.json"}]
    caller_bundle = [caller, caller_review]
    for ref in caller_refs:
        path = (consumer / ref["path"]).resolve()
        if ref["match"] and path.suffix == ".json":
            caller_bundle.append(json.loads(path.read_bytes()))
    caller_values = set(strings(caller_bundle))
    child_identities = {value for c in facts["children"] for value in (c["id"], c["agent_path"])}
    caller_checks = []
    for row in command_rows(facts["journals"].get(parent, [])):
        item = row["payload"]["item"]
        if item.get("exit_code") != 0:
            continue
        text = command_text(row)
        for name in re.findall(r"work/named-role/[A-Za-z0-9_-]+\.py", text):
            if (consumer / name).is_file():
                text += "\n" + (consumer / name).read_text(encoding="utf-8")
        if "sha256" in text and "SPECIALIST-ROUND1.json" in text and "CALLER-REVIEW.json" in text:
            caller_checks.append({"file": row["file"], "line": row["line"]})
    check("caller_independently_verified_native_result", bool(child_identities & set(strings(caller)))
          and expected_values <= caller_values and bool(caller_refs) and all(r["match"] for r in caller_refs)
          and bool(caller_checks), {"native_verification": caller_checks, "verified_references": len(caller_refs),
                                    "child_identity_matches": sorted(child_identities & set(strings(caller)))})
    check("caller_returned_complete_assigned_outcome", caller.get("status") in {"delivered", "complete", "completed", "pass", "passed"}
          and bool(handoffs), {"status": caller.get("status"), "public_handoffs": [h["path"] for h in handoffs]})
    check("no_new_durable_jobs_or_state_publications", not missing and not changed and not any(p.startswith(".pixl/assets/") for p in additions),
          {"store_additions": [p for p in additions if p.startswith(".pixl/")],
           "limit": "Durable state/history identity; this alone does not audit unrecorded external activity."})
    return {"version": 1, "attempt": str(attempt), "grader_sha256": sha(Path(__file__)),
            "host_version": launch["host_version"], "parent_id": parent,
            "children": facts["children"], "passes": sum(c["pass"] for c in checks), "total": len(checks),
            "all_passed": all(c["pass"] for c in checks), "checks": checks,
            "scope": "Registered role loading, retained file/state operations and same-parent-process follow-up. No new art, renderer or cross-process continuation qualification."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attempt", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source = args.out.with_suffix(".py.txt")
    if args.out.exists() or source.exists():
        raise ValueError("Use a fresh output; preserve prior grading results")
    result = grade(args.attempt)
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_bytes(Path(__file__).read_bytes())
    result["grader_source"] = {"path": str(source.resolve()), "sha256": sha(source)}
    write_json(args.out, result)
    print(json.dumps({k: result[k] for k in ("passes", "total", "all_passed")}))
