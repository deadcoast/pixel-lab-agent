"""Independent NF-08 native read, evidence-identity and preservation qualification."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import tomllib
from pathlib import Path

from evaluations.asset_lineage_case import (
    FAMILIES,
    KEY_CLAIMS,
    KIT,
    MEMBERS,
    PLAR,
    SOURCES,
    STATE,
    WORK,
)
from evaluations.consumer_execution_case import historical_target
from evaluations.grade_caller_result import mcp_attempts
from evaluations.grade_consumer_execution import (
    report_reference,
    reported_unchanged,
    selected_identity,
)
from evaluations.grade_integration_change import (
    commands,
    complete_file_proof,
    direct_cli,
    later_direct_rewrites,
    literal_program_writes,
    operation_proof,
)
from evaluations.grade_named_codex_role import normalized, own_rows, rows
from evaluations.grade_plar_coverage import (
    claude_completion,
    continuation_record,
    native_read_proof,
)
from evaluations.grade_readiness import (
    claude_loading_proof,
    codex_role_proof,
    native_calls,
    reference,
    semantic_result,
)
from evaluations.host_trials import inventory, sha
from evaluations.request_review_trials import ROOT
from pixl import codec, service, store


def read(path):
    return json.loads(Path(path).read_bytes())


def ref(value):
    wrapped = [report_reference(value, key) for key in ("reference", "result") if key in value]
    if not wrapped:
        return report_reference(value, "reference")
    if any((item["path"], item["sha256"]) != (wrapped[0]["path"], wrapped[0]["sha256"]) for item in wrapped):
        raise ValueError("Conflicting observed result reference wrappers")
    return wrapped[0]


def preservation_claim(value, independent, state_hash, revision, file_hashes=None):
    """Accept observed structured claims only against independently preserved state."""
    if isinstance(value, dict):
        if ("claim" in value and value["claim"] is not True
                or "original_bytes_unchanged" in value and value["original_bytes_unchanged"] is not True
                or "state_hash_at_every_read" in value and value["state_hash_at_every_read"] != state_hash
                or "revision_at_every_read" in value and (type(value["revision_at_every_read"]) is not int or value["revision_at_every_read"] != revision)):
            return False
        if (any(value[key] != state_hash for key in ("state_px_sha256_now", "state_px_sha256_baseline") if key in value)
                or any(value[key] != (file_hashes or {}).get(key) for key in ("authoring_plar_sha256_now", "plar_txt_sha256_now") if key in value)
                or any(value[key] != [] for key in ("removed", "added_other") if key in value)):
            return False
        validation = value.get("validate_after_work")
        if validation is not None and (not isinstance(validation, dict) or validation.get("matches") is not True
                or validation.get("hash") != state_hash or type(validation.get("revision")) is not int or validation["revision"] != revision):
            return False
        for field in ("files_modified_outside_work_asset_lineage_since_fixture", "added_outside_work_asset_lineage"):
            changes = value.get(field, [])
            if not isinstance(changes, list) or any(not isinstance(name, str) or Path(name).is_absolute()
                    or Path(name).drive or len(Path(name).parts) != 5
                    or Path(name).parts[:4] != (KIT, "runtime", "pixl", "__pycache__") or Path(name).suffix != ".pyc" for name in changes):
                return False
        if (("baseline_files" in value or "current_files" in value)
                and (any(type(value.get(key)) is not int or value[key] < 0 for key in ("baseline_files", "current_files"))
                     or value["current_files"] != value["baseline_files"] + len(set(value.get("added_outside_work_asset_lineage", []))))):
            return False
        if value.get("original_bytes_unchanged") is True:
            required = {"changed", "removed", "added_other", "added_outside_work_asset_lineage", "state_px_sha256_now",
                        "state_px_sha256_baseline", "baseline_files", "current_files"}
            if not required <= value.keys() or value["changed"] != []:
                return False
            value = {**value, "changed": False, "unchanged": value.get("unchanged", True)}
        if value.get("claim") is True:
            if not {"state_hash_at_every_read", "revision_at_every_read", "validate_after_work"} <= value.keys():
                return False
            value = {**value, "unchanged": value.get("unchanged", True)}
    return reported_unchanged(value, independent, state_hash)


def resumed_completion(parent, selected, session):
    """Bind a completed native task notification to the actual successful child revival."""
    if not isinstance(selected, str) or not selected or not isinstance(session, str) or not session:
        return []
    calls, starts, acknowledged, proof = {}, {}, set(), []
    for row in parent:
        blocks = row.get("message", {}).get("content", []) if isinstance(row.get("message"), dict) else []
        for block in blocks if isinstance(blocks, list) else []:
            if not isinstance(block, dict):
                continue
            if (row.get("type") == "assistant" and block.get("type") == "tool_use" and block.get("name") == "SendMessage"
                    and block.get("input", {}).get("to") == selected):
                calls[block["id"]] = row
            result = row.get("tool_use_result", {})
            if (row.get("type") == "user" and block.get("type") == "tool_result" and block.get("tool_use_id") in calls
                    and not block.get("is_error", False) and isinstance(result, dict) and result.get("success") is True
                    and result.get("resumedAgentId") == selected and result.get("revivedAgentId") == selected):
                acknowledged.add(block["tool_use_id"])
        if (row.get("type") != "system" or row.get("session_id") != session or row.get("task_id") != selected
                or row.get("tool_use_id") not in calls):
            continue
        if (row.get("subtype") == "task_started" and row.get("subagent_type") == "pixl:pixl"
                and row.get("task_type") == "local_agent" and row.get("run_id")):
            starts[row["run_id"]] = row
        if (row.get("subtype") == "task_notification" and row.get("status") == "completed"
                and row.get("tool_use_id") in acknowledged and row.get("run_id") in starts
                and starts[row["run_id"]]["tool_use_id"] == row["tool_use_id"]):
            proof.append({"file": row.get("file"), "line": row.get("line"), "agent_id": selected, "session_id": session,
                          "run_id": row["run_id"], "call_id": row["tool_use_id"], "started_line": starts[row["run_id"]].get("line"),
                          "mechanism": "native_completed_notification_bound_to_successful_same_child_revival"})
    return proof


def viewed(journals, path):
    proof = complete_file_proof(journals, path) or native_read_proof(journals, path)
    if proof:
        return proof
    if path.parent.parts[-2:] != Path(WORK).parts:
        return []
    # One observed two-read PowerShell batch returned the complete first file,
    # then failed on a distinct second path. Its batch exit is not the first read's exit.
    pattern = r'''Get-Content\s+-Raw\s+(['"])([^'"\r\n]+)\1\s*;\s*Get-Content\s+-Raw\s+(['"])([^'"\r\n]+)\3'''
    expected = normalized(path.read_text(encoding="utf-8"))
    for command in commands(journals):
        match = re.fullmatch(pattern, command["command"].strip())
        if not match or command["exit_code"] != 1:
            continue
        # The assigned report path supplies the consumer root for these literal reads.
        root = path.parents[len(Path(WORK).parts)]
        first, second = ((root / match[index]).resolve() for index in (2, 4))
        output = normalized(str(command["output"]))
        if (first == path.resolve() and second != first and output.startswith(expected + "\n")
                and "Cannot find path '" + str(second) + "' because it does not exist." in output[len(expected):]):
            proof.append({"file": command["file"], "line": command["line"], "sha256": sha(path),
                          "mechanism": "complete_first_literal_Get_Content_before_distinct_second_read_failure"})
    return proof


INLINE_READER = '''import json,subprocess,pathlib
root=pathlib.Path.cwd(); fixture=json.loads((root/'work/asset-lineage-inputs/fixture.json').read_text()); py=PYTHON; runner=str(root/'installed pixl/scripts/pixl.py')
for key,spec in fixture['reads'].items():
 if key in ('original_context','reused_context','original_family','reused_family'): continue
 a=spec['arguments']
 if spec['tool']=='pixl_plar_read': args=['plar','read','--root',str(root),'--path',a['path'],'--asset',a['asset_id']]
 else: args=['source',a['path'],'--root',str(root),'--expect',a['expect'],'--start',str(a['start']),'--end',str(a['end']),'--budget',str(a['budget'])]
 r=subprocess.run([py,runner]+args,capture_output=True); assert r.returncode==0,(key,r.stderr); dest=root/spec['result_path']; assert not dest.exists(),dest; dest.write_bytes(r.stdout); json.loads(r.stdout); print(key,len(r.stdout))
'''
INLINE_PIPE = re.compile(r"@'\r?\n(.*?)\r?\n'@\s*\|\s*&\s*'([^'\r\n]+)'\s+-\s*", re.DOTALL)


def inline_fixture_proof(journals, root, fixture, identity, python, key, item):
    """Audit the observed fixed stdin runner, never execute or generally interpret Python."""
    fixture_path = "work/asset-lineage-inputs/fixture.json"
    if (sha(root / fixture_path) != identity["inputs"].get(fixture_path)
            or read(root / fixture_path) != fixture
            or sha(root / KIT / "scripts/pixl.py") != identity["package_files"].get("scripts/pixl.py")):
        return []
    selected = {name: value for name, value in fixture["reads"].items()
                if name not in ("original_context", "reused_context", "original_family", "reused_family")}
    if (key not in selected or selected[key]["tool"] not in ("pixl_plar_read", "pixl_source")
            or reference(root, item) != root / selected[key]["result_path"]):
        return []
    expected_ast = ast.dump(ast.parse(INLINE_READER.replace("PYTHON", repr(python.as_posix()))))
    receipts = [name + " " + str((root / spec["result_path"]).stat().st_size) for name, spec in selected.items()]
    proof = []
    observed = commands(journals)
    for command in observed:
        match = INLINE_PIPE.fullmatch(command["command"].strip())
        if not match or command["exit_code"] != 0 or Path(match[2]).resolve() != python.resolve():
            continue
        try:
            actual_ast = ast.dump(ast.parse(match[1]))
        except SyntaxError:
            continue
        if actual_ast != expected_ast or normalized(str(command["output"])).splitlines() != receipts:
            continue
        target = reference(root, item)
        rewrites = later_direct_rewrites(journals, root, target, command, {"position": 10**6})
        for later in observed:
            if later["file"] != command["file"] or later["line"] <= command["line"]:
                continue
            source = INLINE_PIPE.fullmatch(later["command"].strip())
            if source and literal_program_writes(source[1], target, root):
                rewrites.append({"file": later["file"], "line": later["line"]})
        if not rewrites:
            proof.append({"file": command["file"], "line": command["line"], "path": item["path"], "sha256": item["sha256"],
                          "mechanism": "audited_exact_inline_fixture_CLI_stdout_dataflow",
                          "source_sha256": hashlib.sha256(match[1].encode()).hexdigest(),
                          "fixture_sha256": sha(root / fixture_path), "operation": selected[key],
                          "receipt": receipts[list(selected).index(key)],
                          "scope": "Exact observed runner, successful assertions, verbatim stdout write and recorded rewrite audit; no arbitrary-program attestation."})
    return proof


BASH_VALIDATOR = '''import json,hashlib,pathlib
d=pathlib.Path("work/asset-lineage")
for n in ["plar-ready","plar-working","plar-retry","plar-paused","working-construction","ready-fixture","original-context","reused-context","original-family","reused-family"]:
    p=d/(n+".json"); b=p.read_bytes()
    try:
        o=json.loads(b); ok="json-ok keys="+",".join(list(o)[:12])
    except Exception as e: ok="JSON-ERROR "+str(e)
    print(n, len(b), hashlib.sha256(b).hexdigest(), ok)
for n in ["working-construction","ready-fixture"]:
    o=json.loads((d/(n+".json")).read_bytes())
    print(n,"sha256=",o.get("sha256"),"bytes=",o.get("bytes"),"start/end=",o.get("start"),o.get("end"),"text_len=",len(o.get("text","")))
'''


def bash_prefix(root, python, fixture):
    def msys(path):
        value = path.as_posix()
        return "/" + value[0].lower() + value[2:] if path.drive else value
    prefix = (f'cd "{msys(root)}" && PY="{msys(python)}"; R="installed pixl/scripts/pixl.py"; '
              'ROOT="$(pwd -W 2>/dev/null || pwd)"; echo "ROOT=$ROOT"\n'
              'for a in ready working retry paused; do "$PY" -I "$R" plar read --root "$ROOT" --path authoring-plar.txt --asset "queue.$a" > "work/asset-lineage/plar-$a.json"; echo "plar-$a exit=$?"; done\n')
    for key in SOURCES:
        spec = fixture["reads"][key]
        args = spec["arguments"]
        prefix += (f'"$PY" -I "$R" source --root "$ROOT" --expect {args["expect"]} --start {args["start"]} '
                   f'--end {args["end"]} --budget {args["budget"]} {args["path"]} > {spec["result_path"]}; '
                   f'echo "{key.replace("_", "-")} exit=$?"\n')
    return prefix + 'echo "=== validate JSON + sizes ==="\n'


def bash_fixture_proof(journals, root, fixture, identity, python, key, item):
    """Recognize the observed direct Bash loop and its exact read-only hash trailer."""
    if key not in {"plar_" + role for role in MEMBERS}:
        return []
    if (sha(root / "work/asset-lineage-inputs/fixture.json") != identity["inputs"].get("work/asset-lineage-inputs/fixture.json")
            or read(root / "work/asset-lineage-inputs/fixture.json") != fixture
            or sha(root / KIT / "scripts/pixl.py") != identity["package_files"].get("scripts/pixl.py")):
        return []
    for role in MEMBERS:
        if fixture["reads"]["plar_" + role] != {"tool": "pixl_plar_read", "arguments": {"path": PLAR, "asset_id": "queue." + role},
                                               "result_path": f"{WORK}/plar-{role}.json"}:
            return []
    target = reference(root, item)
    if target != root / fixture["reads"][key]["result_path"]:
        return []
    expected = bash_prefix(root, python, fixture)
    marker = '"$PY" -I - <<\'EOF\'\n'
    trailer = '\nEOF\nls -la work/asset-lineage'
    proof = []
    for command in commands(journals):
        text = normalized(command["command"])
        if command["exit_code"] != 0 or not text.startswith(expected + marker) or not text.endswith(trailer):
            continue
        source = text[len(expected + marker):-len(trailer)]
        try:
            if ast.dump(ast.parse(source)) != ast.dump(ast.parse(BASH_VALIDATOR)):
                continue
        except SyntaxError:
            continue
        lines = normalized(str(command["output"])).splitlines()
        exits = ["plar-" + role + " exit=0" for role in MEMBERS]
        exits += [name.replace("_", "-") + " exit=0" for name in SOURCES]
        if lines[:8] != ["ROOT=" + root.as_posix(), *exits, "=== validate JSON + sizes ==="]:
            continue
        hashes_match = all(any(line.startswith(Path(spec["result_path"]).stem + " " +
                           str((root / spec["result_path"]).stat().st_size) + " " + sha(root / spec["result_path"]) + " json-ok keys=")
                           for line in lines) for spec in fixture["reads"].values())
        rewrites = later_direct_rewrites(journals, root, target, command, {"position": 10**6})
        if hashes_match and not rewrites:
            proof.append({"file": command["file"], "line": command["line"], "path": item["path"], "sha256": item["sha256"],
                          "mechanism": "audited_direct_Bash_loop_with_individual_exits_and_read_only_hash_trailer",
                          "command_sha256": hashlib.sha256(text.encode()).hexdigest(), "operation": fixture["reads"][key],
                          "scope": "Exact direct CLI arguments, redirects, individual zero exits and native returned file hashes. Earlier rejected MCP attempts remain separate."})
    return proof


def comparison_errors(comparison: dict, fixture: dict, root: Path) -> list[str]:
    """Check explicit evidence claims without grading prose or inferring a parent."""
    errors = []
    families = comparison.get("families", comparison)
    if any(families.get(key) != value or key in comparison and comparison[key] != value
           for key, value in FAMILIES.items()):
        errors.append("Wrong original/reused family identity")
    claims = comparison.get("key_claims", {})
    errors.extend("Unsupported or absent claim: " + key for key, value in KEY_CLAIMS.items()
                  if claims.get(key) is not value)
    errors.extend("Contradictory overall claim: " + key for key, value in KEY_CLAIMS.items()
                  if key in comparison and comparison[key] is not value)
    for role, pair in fixture["members"].items():
        member = comparison.get("members", {}).get(role, {})
        for key, expected in (("original_candidate", pair[0]["candidate"]), ("reused_candidate", pair[1]["candidate"]),
                              ("original_sha256", pair[0]["sha256"]), ("reused_sha256", pair[1]["sha256"])):
            if member.get(key) != expected:
                errors.append(role + ": wrong " + key)
        if member.get("same_bytes") is not True or not member.get("findings") or not member.get("limits"):
            errors.append(role + ": missing bounded byte-equivalence interpretation")
        evidence = member.get("evidence", [])
        if not isinstance(evidence, list) or not evidence:
            errors.append(role + ": no exact evidence references")
        else:
            for item in evidence:
                reference(root, ref(item))
        # Recognized contradictory assertions remain failures even beside correct claims.
        if any(member.get(key, False) is not False for key in
               ("remote_verified", "new_acceptance", "same_bytes_proves_parent", "same_bytes_proves_reuse_direction")):
            errors.append(role + ": inflated provenance or acceptance")
    if (not comparison.get("limitations") or comparison.get("remote_verified", False) is not False
            or comparison.get("acceptance_created", False) is not False):
        errors.append("Missing limits or inflated overall provenance/acceptance")
    return errors


def lineage_errors(doc, root: Path, role: str, lineage: dict) -> list[str]:
    """Check direct importers and journal intent independently of narrative claims."""
    errors = []
    candidate = MEMBERS[role][0]
    artifact = doc.records[candidate]
    if lineage.get("candidate") != candidate or lineage.get("sha256") != sha(root / artifact.fields["ur"]):
        errors.append("Wrong selected candidate bytes")
    expected_jobs = sorted(record.id for record in doc.records.values() if record.kind == "J"
                           and candidate in [item.id for item in record.fields.get("xs", [])])
    if lineage.get("artifact", {}).get("jobs") != expected_jobs:
        errors.append("Direct importer identity differs from retained state")
    if lineage.get("remote_verified") is not False or not lineage.get("limitations"):
        errors.append("Remote authentication inflated or limits missing")
    jobs = {item["id"]: item for item in lineage["jobs"]}
    for id_ in expected_jobs:
        item = jobs[id_]
        retained = doc.records[doc.records[id_].fields["jr"].id]
        journal_path = reference(root, {"path": item["journal"]["uri"], "sha256": item["journal"]["sha256"]})
        if item["journal"]["artifact"] != retained.id or journal_path != (root / retained.fields["ur"]).resolve():
            errors.append("Journal identity differs from retained importer")
        journal = read(journal_path)
        request = journal["intent"]["request"]
        if item["tool"] != request["tool"] or item["remote_id"] != journal["remote_id"]:
            errors.append("Job identity differs from exact journal")
        expected_operation = "deterministic_edit_request" if role in ("working", "paused") else "generation_request"
        if item["operation"] != expected_operation:
            errors.append("Wrong direct-import request operation")
        if role in ("working", "paused") and item.get("operation_details", {}).get("patch_count") != 196:
            errors.append("Wrong guarded deterministic patch count")
        if role in ("working", "paused"):
            argv = request["arguments"]["argv"]
            changes = json.loads(argv[argv.index("--changes") + 1])
            if (request["tool"] != "pixelart_workbench" or argv[0] != "edit"
                    or any(change["operation"] != "patch_pixels" for change in changes)
                    or sum(len(change["pixels"]) for change in changes) != 196):
                errors.append("Retained request does not contain the claimed deterministic patches")
        if role == "ready" and (item.get("simulated") is not True or item["provider"] != "pixellab-test"
                                or not any(claim["value"] is True for claim in item["simulation_claims"])):
            errors.append("Ready controlled fixture lost explicit simulation evidence")
    supporting = ({"live.paused-02.job": ("create_image_pro_flash", "generation_request")}
                  if role == "paused" else {"live.working-seed.job": ("create_image_pro_flash", "generation_request"),
                                           "live.working-animation-repair-01.job": ("pixelart_workbench", "deterministic_edit_request")}
                  if role == "working" else {})
    for id_, (tool, operation) in supporting.items():
        item = jobs.get(id_)
        retained = doc.records[doc.records[id_].fields["jr"].id]
        journal_path = root / retained.fields["ur"]
        journal = read(journal_path)
        if (item is None or item.get("tool") != tool or item.get("operation") != operation
                or item.get("remote_id") != journal["remote_id"] or journal["intent"]["request"]["tool"] != tool
                or item.get("journal") != {"artifact": retained.id, "uri": retained.fields["ur"], "sha256": sha(journal_path)}):
            errors.append("Missing or incorrect exact supporting request: " + id_)
    if role in ("working", "paused"):
        source_id = "live.paused-02.job" if role == "paused" else "live.working-animation-repair-01.job"
        source_candidate = source_id.removesuffix(".job") + ".candidate"
        source_remote = doc.records[source_id].fields["ri"]
        direct = jobs[expected_jobs[0]]
        journal = read(root / direct["journal"]["uri"])
        locator = journal["intent"]["request"]["arguments"]["argv"][1]
        if (locator.removeprefix("job:") != source_remote or
                not any(item.get("locator") == locator and item.get("matching_jobs") == [source_id]
                        and item.get("matching_candidates") == [source_candidate]
                        and item.get("journal_locator") == "/intent/request/arguments/argv/1"
                        and item.get("relationship") == "recorded_request_reference" and item.get("resolution") == "unique"
                        for item in direct["source_requests"])):
            errors.append("Exact deterministic edit source request is missing or misbound")
    if role == "working" and "live.working-seed.candidate" not in {item["candidate"] for item in lineage["workflow_inputs"]}:
        errors.append("Working generated seed workflow context absent")
    return errors


def preservation_checks(root: Path, identity: dict) -> list[dict]:
    current = inventory(root, ("__pycache__",))
    drift = [name for name, digest in identity["inputs"].items() if current.get(name) != digest]
    additions = [name for name in current if name not in identity["inputs"] and not name.startswith(WORK + "/")]
    historical = [name for name, digest in identity["restoration"]["files"].items()
                  if current.get(historical_target(name)) != digest]
    return [
        {"check": "exact_initial_inputs_and_assigned_additions", "pass": not drift and not additions,
         "evidence": {"changed_or_missing": drift, "unexpected_additions": additions}},
        {"check": "exact_historical_source_art_state_and_host_bytes", "pass": not historical, "evidence": historical},
        {"check": "all_production_records_unchanged", "pass": inventory(root / ".pixl") == identity["baseline_production"]},
        {"check": "frozen_installed_kit_unchanged", "pass": inventory(root / KIT, ("__pycache__",)) == identity["package_files"]},
    ]


def native_partitions(attempt, root, launch, continuation, caller, resumed=None):
    attempts = [attempt] + ([resumed] if resumed is not None else [])
    journals, stdout = [], []
    for directory in attempts:
        journals += [rows(path) for path in sorted(directory.glob("native-*.jsonl"))]
        journals += [rows(path) for path in sorted((directory / "native-transcripts").glob("*.jsonl"))]
        stdout += rows(directory / "stdout.jsonl")
    selected = selected_identity(caller.get("native_child"), launch["host"])
    if launch["host"] == "codex":
        parent = next((journal for journal in journals if journal and journal[0].get("payload", {}).get("id") == continuation["session_id"]), [])
        role = tomllib.loads((root / ".codex/agents/pixl.toml").read_text(encoding="utf-8"))["developer_instructions"]
        proof = codex_role_proof(journals, continuation["session_id"], selected, role)
        child_ids = {child["id"] for child in proof["selected_children"]}
        children = [[journal[0], *own_rows(journal, continuation["session_id"], cold=True)]
                    for journal in journals if journal and journal[0].get("payload", {}).get("id") in child_ids]
        qualified = proof["loaded"] and proof["completed"]
        loading = {name: {"loaded": bool(viewed(children, root / KIT / name))}
                   for name in ("skills/pixl/SKILL.md", "resources/agent/PROFILE.md")}
        proof = {key: value for key, value in proof.items() if key != "child_text"}
    else:
        parent = [row for row in stdout if not row.get("parent_tool_use_id") and not row.get("agent_id")]
        bound_children = set()
        for directory in attempts:
            record = read(directory / "continuation.json")
            item = record.get("retained_transcripts", {}).get(selected)
            if item is not None:
                path = Path(item["path"]).resolve()
                if not path.is_relative_to((directory / "native-transcripts").resolve()) or sha(path) != item["sha256"]:
                    raise ValueError("Selected child proof must use its exact retained native snapshot")
                bound_children.add(path)
        children = [journal for journal in journals if journal and Path(journal[0]["file"]).resolve() in bound_children]
        proof = claude_completion(parent, selected)
        if not proof and resumed is not None:
            proof = resumed_completion(parent, selected, continuation["session_id"])
        qualified = bool(proof) and any(child.get("id", child.get("agent_id")) == selected
                                       and child.get("role") == "pixl:pixl" for child in continuation.get("children", []))
        loading = claude_loading_proof(children, root / KIT)
    return parent, children, journals + [stdout], qualified, proof, loading


def continuation_checks(attempt, resumed, root, selected):
    combined, proof = continuation_record(attempt, resumed, selected)
    original = read(attempt / "continuation.json")
    current = read(resumed / "continuation.json")
    paths = []
    for directory, record in ((attempt, original), (resumed, current)):
        item = record["retained_transcripts"][selected]
        path = Path(item["path"]).resolve()
        if not path.is_relative_to((directory / "native-transcripts").resolve()) or sha(path) != item["sha256"]:
            raise ValueError("Selected child transcript differs from its exact retained record")
        paths.append(path)
    prefix = paths[0].read_bytes()
    continued = paths[1].read_bytes()
    original_outputs = {Path(item["path"]).relative_to(root / WORK).as_posix(): item["sha256"]
                        for item in original["artifacts"] if Path(item["path"]).is_relative_to(root / WORK)}
    if inventory(attempt / "outputs") != original_outputs:
        raise ValueError("Predecessor report copies differ from immutable native artifact hashes")
    final_outputs = inventory(root / WORK)
    drift = [name for name, digest in original_outputs.items() if final_outputs.get(name) != digest]
    return combined, [
        {"check": "same_parent_child_configuration_and_predecessor_verified", "pass": True, "evidence": proof},
        {"check": "same_child_transcript_preserves_exact_prefix_and_adds_native_records",
         "pass": len(continued) > len(prefix) and continued.startswith(prefix),
         "evidence": {"original": original["retained_transcripts"][selected], "continued": current["retained_transcripts"][selected]}},
        {"check": "all_predecessor_reports_preserved", "pass": not drift, "evidence": drift},
    ]


def _grade(attempt: Path, resumed: Path | None = None) -> dict:
    launch, identity, continuation = (read(attempt / name) for name in ("launch.json", "identity.json", "continuation.json"))
    root = Path(launch["cwd"]).resolve()
    fixture = identity["fixture"]
    runtime = attempt / "runtime-environment.json"
    if sha(runtime) != identity["runtime_environment"]["sha256"]:
        raise ValueError("Retained interpreter identity changed")
    python = Path(read(runtime)["executable"])
    caller = read(root / WORK / "CALLER-RESULT.json")
    specialist = read(reference(root, ref(caller["specialist_result"])))
    checks = preservation_checks(root, identity)
    preserved = all(item["pass"] for item in checks)
    def check(name, passed, evidence=None):
        checks.append({"check": name, "pass": bool(passed), "evidence": evidence})
    check("fresh_external_consumer", not root.is_relative_to(ROOT) and not ROOT.is_relative_to(root))
    retained = resumed if resumed is not None else attempt
    check("exact_new_reports_retained", inventory(root / WORK) == inventory(retained / "outputs"))
    # Read-only expectations must use the exact code shipped to the native agents.
    runtime_drift = [path.name for path in (ROOT / "pixl").glob("*.py")
                     if sha(path) != identity["package_files"].get("runtime/pixl/" + path.name)]
    check("grader_runtime_matches_frozen_native_kit", not runtime_drift, runtime_drift)
    if resumed is not None:
        continuation, additional = continuation_checks(attempt, resumed, root, selected_identity(caller.get("native_child"), launch["host"]))
        checks.extend(additional)
        preserved = preserved and all(item["pass"] for item in additional)
    parent, children, journals, qualified, proof, loading = native_partitions(attempt, root, launch, continuation, caller, resumed)
    check("actual_named_isolated_specialist_completed", qualified, proof)
    check("child_loaded_common_profile_and_skill", all(item["loaded"] for item in loading.values()), loading)
    workflow = root / KIT / "skills/pixl/references/family-delivery.md"
    check("child_loaded_lineage_workflow_reference", bool(viewed(children, workflow)))
    public_results = {}
    for actor, actor_journals, report, assigned in (("child", children, specialist, fixture["reads"]),
                                                  ("caller", [parent], caller, fixture["caller_reads"])):
        refs = report["operations" if actor == "child" else "caller_operations"]
        for key, operation in assigned.items():
            item = ref(refs[key])
            path = reference(root, item)
            expected = service.call(operation["tool"], operation["arguments"], root)
            saved = semantic_result(read(path))
            valid = path == root / operation["result_path"] and saved == expected
            call_proof = operation_proof(actor_journals, root, operation["tool"], item)
            if not call_proof and actor == "child":
                call_proof = inline_fixture_proof(actor_journals, root, fixture, identity, python, key, item)
                if not call_proof:
                    call_proof = bash_fixture_proof(actor_journals, root, fixture, identity, python, key, item)
            check(actor + "_public_read_" + key, valid and bool(call_proof), call_proof)
            if actor == "child":
                public_results[key] = saved
    doc = store.load(root / Path(STATE).parent)
    for role in MEMBERS:
        lineage = next(item["lineage"] for item in public_results["original_context"]["members"]
                       if item["candidate"] == MEMBERS[role][0])
        errors = lineage_errors(doc, root, role, lineage)
        check(role + "_retained_importer_intent_and_provenance_limits", not errors, errors)
    construction = read(root / SOURCES["working_construction"])
    seed = doc.records["live.working-seed.candidate"]
    check("construction_record_binds_generated_seed_and_deterministic_quarter_turns",
          construction["seed_sha256"] == seed.fields["dg"] == sha(root / seed.fields["ur"])
          and construction["clockwise_degrees"] == [0, 90, 180, 270] and construction["patch_count"] == 196)
    comparison_path = reference(root, ref(specialist["comparison"]))
    comparison = read(comparison_path)
    errors = comparison_errors(comparison, fixture, root)
    check("bounded_comparison_matches_exact_families_members_and_evidence", not errors, errors)
    for actor, actor_journals, report in (("child", children, specialist), ("caller", [parent], caller)):
        check(actor + "_names_same_exact_comparison", reference(root, ref(report["comparison"])) == comparison_path)
        named_sources = {reference(root, ref(item)) for item in report["inspected_sources"]}
        check(actor + "_names_exact_source_evidence", {root / path for path in SOURCES.values()} <= named_sources)
        for key in SOURCES:
            path = reference(root, ref(specialist["operations"][key]))
            check(actor + "_actually_consumed_source_excerpt_" + key, bool(viewed(actor_journals, path)))
        check(actor + "_reports_preservation_and_no_new_provenance_or_acceptance",
              preservation_claim(report.get("production_unchanged"), preserved, codec.digest(doc), doc.revision,
                                 {"authoring_plar_sha256_now": sha(root / PLAR), "plar_txt_sha256_now": sha(root / "plar.txt")})
              and report.get("new_provider_execution") is False and report.get("acceptance_created") is False
              and bool(report.get("limitations")) and bool(report.get("next_action")))
    check("caller_actually_consumed_exact_comparison_and_member_hashes", bool(viewed([parent], comparison_path)))
    check("caller_names_all_exact_child_results", all(reference(root, ref(caller["operations"][key])) ==
          reference(root, ref(specialist["operations"][key])) for key in fixture["reads"]))
    allowed = {"pixl_source", "pixl_sources", "pixl_review_context", "pixl_family", "pixl_plar_read",
               "pixl_readiness", "pixl_validate", "pixl_context", "pixl_knowledge", "pixl_capabilities"}
    prohibited = [call for call in mcp_attempts(journals) if
                  str(call["server"]).replace("-", "_") != "pixl_local" or call["tool"] not in allowed]
    mutation_commands = ("job-prepare", "job-dispatch", "job-observe", "job-import", "candidate-review", "family-snapshot",
                         "consumer-execute", "request-review", "production-plan", "stage-prepare", "task-complete",
                         "inspection-prepare", "inspection-review", "commit", "plar save", "plar prepare", "plar handoff")
    prohibited += [{"file": command["file"], "line": command["line"], "command": command["command"]}
                   for command in commands(journals) if any(direct_cli(command["command"], name) for name in mutation_commands)]
    check("no_recorded_remote_or_production_mutation_operation_attempt", not prohibited, prohibited)
    check("native_attempt_completed", continuation.get("status") == "finished" and continuation.get("returncode") == 0
          and continuation.get("interruption_reason") is None)
    return {"version": 1, "status": "pass" if all(item["pass"] for item in checks) else "fail",
            "passed": sum(item["pass"] for item in checks), "total": len(checks), "checks": checks,
            "recorded_rejected_read_attempts": [call for call in native_calls(journals)
                                                 if not call["success"] and call["tool"] in allowed],
            "scope": "Retained asset-lineage interpretation and native public read/preservation proofs only. No remote authentication, new art, artistic acceptance, or M1/M2/broader M3 closure."}


def grade(attempt: Path, continuation: Path | None = None) -> dict:
    try:
        return _grade(attempt.resolve(), continuation.resolve() if continuation is not None else None)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, StopIteration, codec.PixlError) as error:
        return {"version": 1, "status": "fail", "passed": 0, "total": 1,
                "checks": [{"check": "required_evidence_readable", "pass": False, "evidence": f"{type(error).__name__}: {error}"}]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attempt", type=Path)
    parser.add_argument("--continuation", type=Path)
    parser.add_argument("--out", "--output", type=Path, required=True)
    args = parser.parse_args()
    result = grade(args.attempt, args.continuation)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({key: result[key] for key in ("status", "passed", "total")}))
    return result["status"] != "pass"


if __name__ == "__main__":
    raise SystemExit(main())
