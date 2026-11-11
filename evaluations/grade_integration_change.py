"""Independent bounded CF-07/NF-06 native integration evidence checks."""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import re
import shlex
import tomllib
import zipfile
from itertools import pairwise
from pathlib import Path
from urllib.parse import unquote, urlparse

from evaluations.grade_caller_result import bind_exports, mcp_attempts
from evaluations.grade_named_codex_role import normalized, own_rows, rows, strings
from evaluations.grade_plar_coverage import (
    claude_completion,
    continuation_record,
    native_read_proof,
    plar_skill_proof,
    selected_child,
)
from evaluations.grade_readiness import (
    claude_loading_proof,
    codex_role_proof,
    expanded_objects,
    native_calls,
    reference,
    semantic_result,
)
from evaluations.host_trials import inventory, sha
from evaluations.integration_change_case import (
    ART,
    ASSETS,
    AUTHORITY,
    KIT,
    PLAR,
    RENDERER,
    TIMING,
    WORK,
)
from pixl import candidate_review, codec, graph, jobs, plar, service, store

REFS = ("initial_read", "allocation_save", "final_document", "current_selection",
        "obsolete_dispatch", "obsolete_completion", "old_abandon", "revised_prepare", "new_abandon",
        "sample_review", "delivery_build", "delivery_context", "capture_report", "renderer_check",
        "destination_report", "destination_import", "delivery_review", "acceptance", "final_selection", "handoff")


def read(path):
    return json.loads(Path(path).read_bytes())


def fields(value: dict) -> dict:
    refs = value.get("refs", {})
    if not isinstance(refs, dict) or any(k in value and value[k] != v for k, v in refs.items()):
        raise ValueError("Contradictory report reference layouts")
    return {**value, **refs}


def native_identity(value, host):
    if host == "claude" and isinstance(value, dict):
        roles = {value[k] for k in ("agent_type", "subagent_type") if k in value}
        if roles == {"pixl:pixl"}:
            return value.get("agent_id", value.get("canonical_task"))
    if isinstance(value, dict) and "canonical_path" in value:
        role = "pixl" if host == "codex" else "pixl:pixl"
        if value.get("agent_type") != role or any(value.get(k, value["canonical_path"]) != value["canonical_path"]
                                                 for k in ("canonical_task", "agent_id")):
            return None
        return value["canonical_path"]
    return selected_child(value, host)


def command_text(command):
    if isinstance(command, str):
        return command
    if not isinstance(command, list) or not all(isinstance(s, str) for s in command):
        return ""
    for flag in ("-Command", "-c", "/c"):
        if flag in command and command.index(flag) + 1 == len(command) - 1:
            return command[-1]
    # Preserve argv token boundaries for directly recorded Python executions.
    return " ".join(json.dumps(part) if any(c.isspace() for c in part) else part for part in command)


def leading_objects(output):
    """A host command may print a full JSON result followed by unrelated help."""
    yield from expanded_objects(output)
    for text in strings(output):
        remaining = text.lstrip()
        if remaining.startswith(("{", "[")):
            try:
                value, _ = json.JSONDecoder().raw_decode(remaining)
                yield from expanded_objects(value)
            except ValueError:
                pass


def apply_recorded_diff(before: str, patch: str) -> str:
    """Replay a retained native unified diff only when every old line agrees."""
    original = before.replace("\r\n", "\n").splitlines()
    lines = patch.replace("\r\n", "\n").splitlines()
    output, cursor, index = [], 0, 0
    while index < len(lines):
        header = re.fullmatch(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*", lines[index])
        if not header:
            raise ValueError("Unsupported recorded source patch header")
        start = int(header[1]) - (int(header[2] or "1") != 0)
        if start < cursor or start > len(original):
            raise ValueError("Recorded source patch overlaps or escapes old source")
        output.extend(original[cursor:start])
        cursor, old_count, new_count = start, 0, 0
        index += 1
        while index < len(lines) and not lines[index].startswith("@@"):
            line = lines[index]
            if not line or line[0] not in " +-":
                raise ValueError("Unsupported recorded source patch line")
            if line[0] in " -":
                if cursor >= len(original) or original[cursor] != line[1:]:
                    raise ValueError("Recorded source patch does not match old source")
                cursor += 1
                old_count += 1
            if line[0] in " +":
                output.append(line[1:])
                new_count += 1
            index += 1
        if old_count != int(header[2] or "1") or new_count != int(header[4] or "1"):
            raise ValueError("Recorded source patch line counts disagree")
    output.extend(original[cursor:])
    return "\n".join(output) + ("\n" if before.endswith("\n") else "")


def source_events(journals, root, path):
    """Replay successful native source writes before qualifying any later execution."""
    expected = normalized(path.read_text(encoding="utf-8"))
    result = []
    for journal in journals:
        content = None
        for row in journal:
            item = row.get("payload", {}).get("item", row.get("item", {}))
            if item.get("type") != "FileChange" or item.get("status") != "completed":
                continue
            for name, change in item.get("changes", {}).items():
                if (root / name).resolve() != path.resolve():
                    continue
                try:
                    if change.get("type") == "add":
                        content = change["content"]
                    elif change.get("type") == "update" and content is not None and not change.get("move_path"):
                        content = apply_recorded_diff(content, change["unified_diff"])
                    else:
                        content = None
                except (ValueError, KeyError):
                    content = None
                result.append({"file": row.get("file"), "line": row.get("line"),
                               "mechanism": "successful_FileChange_replayed_source", "matches": content is not None and normalized(content) == expected})
    for command in commands(journals):
        if command["exit_code"] != 0 or path.name not in command["command"]:
            continue
        if (expected in normalized("\n".join(strings(command["output"])))
                or expected in normalized(command["command"]) and any(w in command["command"] for w in ("Set-Content", "WriteAllText", "cat "))):
            result.append({"file": command["file"], "line": command["line"], "mechanism": "complete_native_source_read_or_write", "matches": True})
    return sorted(result, key=lambda r: (r["file"] or "", r["line"] or 0))


def commands(journals: list[list[dict]]) -> list[dict]:
    """Only completed host executions; prose and authored files are not executions."""
    result = []
    seen = set()
    for journal in journals:
        uses = {}
        for row in journal:
            payload = row.get("payload", {})
            item = payload.get("item", row.get("item", {}))
            if item.get("type") in ("CommandExecution", "command_execution") and item.get("exit_code") is not None and item.get("id", (row.get("file"), row.get("line"))) not in seen:
                seen.add(item.get("id", (row.get("file"), row.get("line"))))
                result.append({"command": command_text(item.get("command", "")), "output": item.get("aggregated_output", ""),
                               "exit_code": item["exit_code"], "file": row.get("file"), "line": row.get("line")})
            for block in row.get("message", {}).get("content", []) if isinstance(row.get("message"), dict) else []:
                if not isinstance(block, dict):
                    continue
                if row.get("type") == "assistant" and block.get("type") == "tool_use" and block.get("name") == "Bash":
                    uses[block["id"]] = block.get("input", {}).get("command", "")
                if row.get("type") == "user" and block.get("type") == "tool_result" and block.get("tool_use_id") in uses and block["tool_use_id"] not in seen:
                    seen.add(block["tool_use_id"])
                    result.append({"command": uses[block["tool_use_id"]], "output": block.get("content", ""),
                                   "exit_code": 1 if block.get("is_error") else 0,
                                   "file": row.get("file"), "line": row.get("line")})
    return result


def python_invocations(command: str) -> list[list[str]]:
    """Literal direct Python invocations; quoted prose is not executable evidence."""
    token = r'(?P<token>"[^"\r\n]+"|\'[^\'\r\n]+\'|[^\s;]+)'
    invocations = []
    for line in re.split(r"[;\r\n]", command):
        parts = [m.group("token").strip("\'\"") for m in re.finditer(token, line.strip())]
        if parts and parts[0] == "&":
            parts.pop(0)
        if len(parts) < 2 or not re.fullmatch(r".*(?:^|[/\\])python(?:\.exe)?", parts[0], re.IGNORECASE):
            continue
        if parts[1] == "-B":
            parts.pop(1)
        invocations.append(parts)
    return invocations


def direct_cli(command: str, operation: str) -> bool:
    for parts in python_invocations(command):
        expected = operation.split()
        if (len(parts) >= 3 and parts[1].replace("\\", "/").endswith("/scripts/pixl.py")
                and parts[2:2 + len(expected)] == expected):
            return True
    return False


# These two complete native helper sources were independently inspected: public
# subprocess stdout/stderr are written verbatim, never reconstructed from reports.
# A digest alone is insufficient: source loading/writing and actual execution must
# also be observed in the selected actor's journal before each accepted receipt.
AUDITED_HELPERS = {
    "2e55482508b6ae1468bc4151cec4f83d8afb11246a0c182eb37e8f2bbcbd8d2c": "operations.py",
    "8ddebc75d3fe88e3b6fc062d45b1fccefa2161d666b71745cde412fae19c9ccb": "parent-verify.py",
}


def audited_helper_proof(journals, root, operation, ref, success):
    output = reference(root, ref)
    base = Path(str(output).removesuffix(".stderr"))
    receipts = [Path(str(base) + ".execution.json"), base.with_suffix(".command.json")]
    observed = commands(journals)
    proofs = []
    for receipt in receipts:
        if not receipt.is_file():
            continue
        record = read(receipt)
        argv = record.get("command", [])
        expected = operation.split()
        if (len(argv) < 3 or Path(argv[1]).resolve() != (root / KIT / "scripts/pixl.py").resolve()
                or argv[2:2 + len(expected)] != expected or success != (record.get("exit_code") == 0)):
            continue
        stdout, stderr = base, Path(str(base) + ".stderr")
        if receipt.suffixes[-2:] == [".command", ".json"]:
            stderr = base.with_suffix(".stderr.txt")
        if not stdout.is_file() or not stderr.is_file():
            continue
        if "stdout_sha256" in record and (sha(stdout) != record["stdout_sha256"] or sha(stderr) != record["stderr_sha256"]):
            continue
        helper_name = AUDITED_HELPERS.get(record.get("helper_sha256"), "parent-verify.py" if ".command.json" in receipt.name else None)
        if not helper_name:
            continue
        helper = root / WORK / helper_name
        if not helper.is_file() or AUDITED_HELPERS.get(sha(helper)) != helper_name:
            continue
        helper_body = normalized(helper.read_text(encoding="utf-8"))
        for command in observed:
            command_text = str(command["command"]).replace("\\", "/")
            # An early operation may have completed before a later command in its
            # script failed; the individual receipt carries the operation's exit.
            candidates = [(root / argv[1]).resolve() for argv in python_invocations(command_text)
                          if len(argv) >= 2 and (root / argv[1]).resolve().parent == (root / WORK).resolve()
                          and (root / argv[1]).is_file()]
            for script in candidates:
                script_body = normalized(script.read_text(encoding="utf-8"))
                tree = ast.parse(script_body)
                imported = any(isinstance(n, ast.ImportFrom) and n.module == "operations" for n in tree.body)
                literal_call = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "op"
                                   and n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value == base.name
                                   for n in ast.walk(tree))
                if script != helper and not (helper_name == "operations.py" and imported and literal_call):
                    continue
                if script == helper and helper_name == "operations.py" and not literal_call:
                    continue
                if any(isinstance(n, (ast.FunctionDef, ast.Assign)) and
                       (getattr(n, "name", "") == "op" or any(isinstance(t, ast.Name) and t.id == "op" for t in getattr(n, "targets", [])))
                       for n in tree.body) and script != helper:
                    continue
                bound = []
                for name, body in ((helper.name, helper_body), (script.name, script_body)):
                    matching_sources = [c for c in source_events(journals, root, root / WORK / name)
                                        if c["file"] == command["file"] and (c["line"] or 0) < (command["line"] or 0)]
                    if matching_sources and matching_sources[-1]["matches"]:
                        bound.append({"source": name, "sha256": sha(root / WORK / name), **matching_sources[-1]})
                if len(bound) == 2:
                    proofs.append({"mechanism": "audited_verbatim_subprocess_helper", "file": command["file"], "line": command["line"],
                                   "receipt": receipt.relative_to(root).as_posix(), "receipt_sha256": sha(receipt), "sources": bound,
                                   "command": argv, "exit_code": record["exit_code"]})
    return proofs


def resolved_shell_segments(command):
    """Read literal Bash argv and bounded for lists; never evaluate shell code."""
    # Bash removes escaped newlines outside single quotes. Protect literal
    # dollars before shlex discards quote boundaries so they cannot turn into
    # variable substitutions or a claimed per-operation exit status.
    prepared, quote, index = [], None, 0
    while index < len(command):
        char = command[index]
        if char == "\\" and quote != "'":
            following = command[index + 1:]
            newline = 2 if following.startswith("\r\n") else 1 if following.startswith("\n") else 0
            if newline:
                index += 1 + newline
                continue
            if following.startswith("$"):
                prepared.append("\ue000")
                index += 2
                continue
            if following:
                prepared.extend((char, following[0]))
                index += 2
                continue
        if char in ("'", '"'):
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
        prepared.append("\ue000" if char == "$" and quote == "'" else char)
        index += 1
    command = "".join(prepared)
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    try:
        tokens = list(lexer)
    except ValueError:
        return []
    segments, segment = [], []
    for token in tokens:
        if token and all(c in ";&|\n" for c in token):
            if segment:
                segments.append(segment)
            segment = []
        else:
            segment.append(token)
    if segment:
        segments.append(segment)
    variables, resolved = {}, []
    def expand(value):
        return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)",
                      lambda m: variables.get(m[1] or m[2], m[0]), value)
    def consume(parts, inside_loop=False):
        index = 0
        while index < len(parts):
            segment = list(parts[index])
            if segment[0] == "for":
                if (inside_loop or len(segment) < 4 or segment[2] != "in"
                        or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", segment[1])):
                    return False
                end = next((i for i in range(index + 1, len(parts)) if parts[i] == ["done"]), None)
                if end is None or index + 1 == end or parts[index + 1][0] != "do":
                    return False
                values = [expand(value) for value in segment[3:]]
                if len(values) > 64 or any(any(c in value for c in "$`*?[]{}\ue000") for value in values):
                    return False
                body = [list(value) for value in parts[index + 1:end]]
                body[0] = body[0][1:]
                body = [value for value in body if value]
                for value in values:
                    variables[segment[1]] = value
                    if not consume(body, inside_loop=True):
                        return False
                index = end + 1
                continue
            if segment[0] in ("if", "then", "else", "fi", "while", "until", "case", "esac", "do", "done", "function"):
                return False
            while segment and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", segment[0], re.DOTALL):
                name, value = segment.pop(0).split("=", 1)
                if "$(" not in value and "`" not in value:
                    variables[name] = expand(value)
                else:
                    variables.pop(name, None)
            if segment:
                resolved.append([expand(v) for v in segment])
            index += 1
        return True
    if not consume(segments):
        return []
    return resolved


def shell_python_calls(command):
    segments = resolved_shell_segments(command)
    calls, echo_counts = [], {}
    echo_positions = {}
    for index, segment in enumerate(segments):
        if segment[0] == "echo" and len(segment) == 2 and segment[1].count("$?") == 1:
            pattern = "^" + re.escape(segment[1]).replace(re.escape("$?"), r"(\d+)") + "$"
            echo_positions[index] = (pattern, echo_counts.get(pattern, 0))
            echo_counts[pattern] = echo_counts.get(pattern, 0) + 1
    for position, segment in enumerate(segments):
        argv = list(segment)
        if not re.fullmatch(r"(?:.*[/\\])?python(?:\.exe)?", argv[0], re.IGNORECASE):
            continue
        while len(argv) > 1 and argv[1] in ("-I", "-B", "-E", "-s", "-u"):
            argv.pop(1)
        redirects = {}
        index = 0
        while index < len(argv):
            if argv[index] in (">", ">>") and index + 1 < len(argv):
                stream = "stderr" if index > 0 and argv[index - 1] == "2" else "stdout"
                redirects[stream] = argv[index + 1]
                start = index - (stream == "stderr")
                del argv[start:index + 2]
                index = start
            else:
                index += 1
        calls.append({"argv": argv, "position": position, "exit_echo": echo_positions.get(position + 1), **redirects})
    return calls


def explicit_exit(command, invocation):
    echo = invocation.get("exit_echo")
    if echo is None:
        return None
    output = "\n".join(strings(command["output"])).replace("\r\r\n", "\n").replace("\r\n", "\n")
    matches = re.findall(echo[0], output, re.MULTILINE)
    return int(matches[echo[1]]) if len(matches) > echo[1] else None


def literal_program_writes(source, target, root):
    """Recognize explicit Python target writes in recorded helper/inline source."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    def names(node):
        return [n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
    def same(value):
        return value == target.name or (root / value).resolve() == target.resolve()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if (isinstance(node.func, ast.Attribute) and node.func.attr in ("write_text", "write_bytes", "unlink", "replace", "rename")
                and any(same(v) for v in names(node.func.value))):
            return True
        if (isinstance(node.func, ast.Name) and node.func.id in ("op", "public") and node.args
                and any(same(v) for v in names(node.args[0]))):
            return True
        if isinstance(node.func, ast.Name) and node.func.id == "open" and node.args:
            mode = node.args[1] if len(node.args) > 1 else next((k.value for k in node.keywords if k.arg == "mode"), None)
            if (isinstance(mode, ast.Constant) and isinstance(mode.value, str) and any(c in mode.value for c in "wax+")
                    and any(same(v) for v in names(node.args[0]))):
                return True
    return False


def later_direct_rewrites(journals, root, target, command, invocation):
    """Audit later recorded target writes; this is not arbitrary-program attestation."""
    target = target.resolve()
    found = []
    def same(value):
        return isinstance(value, str) and "$" not in value and (root / value).resolve() == target
    observed = commands(journals)
    start = next((i for i, c in enumerate(observed) if c["file"] == command["file"] and c["line"] == command["line"]), None)
    if start is None:
        return [{"reason": "invocation not found"}]
    for index, later in enumerate(observed[start:], start):
        for position, segment in enumerate(resolved_shell_segments(later["command"])):
            if index == start and position <= invocation["position"]:
                continue
            paths = [segment[i + 1] for i, token in enumerate(segment[:-1]) if token in (">", ">>")]
            if segment[0] in ("cp", "mv", "tee"):
                paths.append(segment[-1])
            elif segment[0] in ("rm", "Remove-Item", "Set-Content", "Out-File"):
                paths.extend(segment[1:])
            for call in shell_python_calls(later["command"]):
                if call["position"] == position and "--result-path" in call["argv"]:
                    arg_index = call["argv"].index("--result-path") + 1
                    if arg_index < len(call["argv"]):
                        paths.append(call["argv"][arg_index])
            if any(same(p) for p in paths):
                found.append({"file": later["file"], "line": later["line"], "mechanism": "later_direct_target_write"})
            for call in shell_python_calls(later["command"]):
                if call["position"] != position or len(call["argv"]) < 2:
                    continue
                argv = call["argv"]
                source = None
                if argv[1] == "-c" and len(argv) > 2:
                    source = argv[2]
                elif argv[1].endswith(".py") and "$" not in argv[1]:
                    script = (root / argv[1]).resolve()
                    if script.is_relative_to(root.resolve()) and script.is_file():
                        source = script.read_text(encoding="utf-8")
                if source and literal_program_writes(source, target, root):
                    found.append({"file": later["file"], "line": later["line"], "mechanism": "later_explicit_helper_target_write"})
    for journal in journals:
        uses = {}
        for row in journal:
            if row.get("file") != command["file"] or (row.get("line") or 0) <= (command["line"] or 0):
                continue
            item = row.get("payload", {}).get("item", row.get("item", {}))
            if item.get("type") == "FileChange" and item.get("status") == "completed" and any(same(n) for n in item.get("changes", {})):
                found.append({"file": row["file"], "line": row["line"], "mechanism": "later_FileChange"})
            blocks = row.get("message", {}).get("content", []) if isinstance(row.get("message"), dict) else []
            for block in blocks if isinstance(blocks, list) else []:
                if not isinstance(block, dict):
                    continue
                if (row.get("type") == "assistant" and block.get("type") == "tool_use"
                        and block.get("name") in ("Write", "Edit") and same(block.get("input", {}).get("file_path"))):
                    uses[block["id"]] = row
                if row.get("type") == "user" and block.get("type") == "tool_result" and not block.get("is_error") and block.get("tool_use_id") in uses:
                    found.append({"file": row["file"], "line": row["line"], "mechanism": "later_native_Write_or_Edit"})
    return found


def streamed_objects(output):
    yield from leading_objects(output)
    for text in strings(output):
        index = 0
        while match := re.search(r"[\[{]", text[index:]):
            index += match.start()
            try:
                value, end = json.JSONDecoder().raw_decode(text[index:])
                yield from expanded_objects(value)
                index += end
            except ValueError:
                index += 1


def shell_file_proof(journals, root, operation, ref, success):
    """Bind direct CLI redirects/exports to actual native returns or full Reads."""
    saved = read(reference(root, ref))
    wanted = semantic_result(saved) if success else saved
    proof = []
    reads = native_read_proof(journals, reference(root, ref))
    for command in commands(journals):
        for invocation in shell_python_calls(command["command"]):
            argv = invocation["argv"]
            expected = operation.split()
            if (len(argv) < 3 or not argv[1].replace("\\", "/").endswith("/scripts/pixl.py")
                    or argv[2:2 + len(expected)] != expected):
                continue
            targets = [invocation.get("stdout" if success else "stderr")]
            if success and "--result-path" in argv and argv.index("--result-path") + 1 < len(argv):
                targets.append(argv[argv.index("--result-path") + 1])
            bound_targets = []
            for target in targets:
                if not target or "$" in target:
                    continue
                path = (root / target).resolve()
                if path.is_relative_to(root.resolve()) and path.is_file() and sha(path) == ref["sha256"]:
                    bound_targets.append(path.relative_to(root).as_posix())
            if not bound_targets:
                continue
            returned = list(streamed_objects(command["output"]))
            direct = any(v == saved or v == wanted for v in returned)
            exported = any(v.get("result_path") == ref["path"] and v.get("result_sha256") == ref["sha256"] for v in returned)
            later_reads = [r for r in reads if r["file"] == command["file"] and (r["line"] or 0) > (command["line"] or 0)]
            code = explicit_exit(command, invocation)
            dataflow = []
            if code is not None and (code == 0) == success and ("error" not in wanted) == success:
                for name in bound_targets:
                    rewrites = later_direct_rewrites(journals, root, root / name, command, invocation)
                    if not rewrites:
                        dataflow.append(name)
            if direct or exported or later_reads or dataflow:
                proof.append({"mechanism": "direct_shell_CLI_file_and_native_return_or_full_Read" if direct or exported or later_reads else "direct_shell_CLI_redirect_dataflow",
                              "file": command["file"], "line": command["line"], "argv": argv,
                              "bound_files": bound_targets, "sha256": ref["sha256"], "reads": later_reads,
                              "direct_result": direct, "exact_export": exported, "operation_exit": code, "dataflow_files": dataflow,
                              "native_byte_return_attestation": bool(direct or exported or later_reads),
                              "scope": "Actual frozen-kit CLI execution and explicit individual exit are separate from independently checked retained bytes. Direct redirect dataflow audits recorded target writes; it is not native-byte-return or arbitrary-program attestation."})
    return proof


def operation_proof(journals: list[list[dict]], root: Path, tool: str, ref: dict, *, success=True) -> list[dict]:
    """Bind a saved result to the real public call or its exact result export."""
    saved = read(reference(root, ref))
    result = []
    calls = bind_exports([{**c, "server": "pixl_local"} for c in native_calls(journals)], root)
    wanted = semantic_result(saved) if success else saved
    for call in calls:
        if call["tool"] != tool or call["success"] != success:
            continue
        values = list(expanded_objects(call["result"]))
        if any(v == wanted or v == saved for v in values):
            result.append({k: call[k] for k in ("file", "line", "tool", "arguments")})
    command_name = tool.removeprefix("pixl_").replace("_", "-")
    if command_name.startswith("plar-"):
        command_name = command_name.replace("plar-", "plar ", 1)
    for command in commands(journals):
        text = str(command["command"]).replace("\\", "/")
        if not direct_cli(text, command_name) or success != (command["exit_code"] == 0):
            continue
        values = list(expanded_objects(command["output"]))
        exact = any(v == wanted or v == saved for v in values)
        exported = any(v.get("result_path") == ref["path"] and v.get("result_sha256") == ref["sha256"]
                       for v in values) and ref["path"] in text and "--result-path" in text
        if exact or exported:
            result.append({k: command[k] for k in ("file", "line", "command", "exit_code")})
    if success:
        for command in commands(journals):
            for segment in command["command"].split(";"):
                pipeline = segment.split("|", 1)
                if len(pipeline) != 2 or not direct_cli(pipeline[0], command_name):
                    continue
                write = pipeline[1].strip()
                if not re.fullmatch(r"Set-Content\s+-Encoding\s+utf8\s+[\"']?" + re.escape(ref["path"]) + r"[\"']?", write, re.IGNORECASE):
                    continue
                readers = [c for c in commands(journals) if c["exit_code"] == 0 and c["file"] == command["file"]
                           and (c["line"] or 0) > (command["line"] or 0) and "Get-Content" in c["command"]
                           and ref["path"] in c["command"] and any(v == wanted for v in leading_objects(c["output"]))]
                if readers:
                    result.append({"mechanism": "direct_public_stdout_pipeline_and_later_full_native_read",
                                   "file": command["file"], "line": command["line"], "read_line": readers[0]["line"],
                                   "path": ref["path"], "sha256": ref["sha256"]})
    result.extend(shell_file_proof(journals, root, command_name, ref, success))
    result.extend(audited_helper_proof(journals, root, command_name, ref, success))
    return result


def complete_file_proof(journals: list[list[dict]], path: Path) -> list[dict]:
    expected = normalized(path.read_text(encoding="utf-8"))
    target = str(path.resolve()).replace("\\", "/").lower()
    result = []
    for command in commands(journals):
        if (command["exit_code"] == 0 and (target in command["command"].replace("\\", "/").lower()
                or path.name.lower() in command["command"].lower())
                and expected in normalized("\n".join(strings(command["output"])))):
            result.append({k: command[k] for k in ("file", "line")})
    return result


def image_views(journals: list[list[dict]], root: Path) -> dict[str, list[dict]]:
    """Actual image events and successful paired image Reads, never text path claims."""
    found: dict[str, list[dict]] = {}
    def add(name, row):
        if not isinstance(name, str):
            return
        if name.startswith("file:"):
            name = unquote(urlparse(name).path).lstrip("/")
        path = (root / name).resolve()
        if path.is_relative_to(root.resolve()) and path.is_file():
            found.setdefault(sha(path), []).append({"path": path.relative_to(root).as_posix(),
                                                   "file": row.get("file"), "line": row.get("line")})
    for journal in journals:
        uses = {}
        for row in journal:
            item = row.get("payload", {}).get("item", row.get("item", {}))
            if item.get("type") in ("ImageView", "image_view"):
                add(item.get("path"), row)
            for block in row.get("message", {}).get("content", []) if isinstance(row.get("message"), dict) else []:
                if not isinstance(block, dict):
                    continue
                if row.get("type") == "assistant" and block.get("type") == "tool_use" and block.get("name") in ("Read", "view_image"):
                    uses[block["id"]] = block.get("input", {}).get("file_path", block.get("input", {}).get("path"))
                if (row.get("type") == "user" and block.get("type") == "tool_result" and not block.get("is_error") and block.get("tool_use_id") in uses
                        and any(v.get("type") in ("image", "input_image") for v in expanded_objects(block.get("content", [])))):
                    add(uses[block["tool_use_id"]], row)
    return found


def allocation_errors(before: dict, after: dict, root: Path) -> list[str]:
    """The controlled timing amendment cannot erase unchanged artistic authority."""
    plar.validate(after, root)
    errors = []
    old = {a["id"]: a for a in before["assets"]}
    new = {a["id"]: a for a in after["assets"]}
    if set(old) != set(new) or after["project"] != before["project"]:
        return ["Project identity or stable asset IDs changed"]
    for ident in set(old) - {"queue.working"}:
        if old[ident] != new[ident]:
            errors.append("Unrelated allocation changed: " + ident)
    old_work, new_work = old["queue.working"], new["queue.working"]
    for key in ("id", "kind", "purpose", "consumers", "references", "delivery", "depends_on", "existing"):
        if old_work.get(key) != new_work.get(key):
            errors.append("Unchanged Working role/authority changed: " + key)
    old_requirements = {r["property"]: r for r in old_work["requirements"]}
    new_requirements = {r["property"]: r for r in new_work["requirements"]}
    if len(new_requirements) != len(new_work["requirements"]) or set(old_requirements) != set(new_requirements):
        errors.append("Working requirement inventory changed")
    for key, value in old_requirements.items():
        if key != "animation" and new_requirements.get(key) != value:
            errors.append("Non-timing Working requirement changed: " + key)
    timing = new_requirements.get("animation", {})
    if (timing.get("value") != {"frame_duration_ms": 150, "loop": True, "nominal_cycle_ms": 600}
            or timing.get("sources") != old_requirements["animation"]["sources"]
            or timing.get("authority") != old_requirements["animation"]["authority"]):
        errors.append("Timing amendment not carried as scoped authorized 150ms loop")
    sources = {s["id"]: s for s in after["sources"]}
    if set(sources) != {s["id"] for s in before["sources"]}:
        errors.append("Source inventory changed")
    for source in before["sources"]:
        expected = dict(source)
        if source["path"] in (TIMING, AUTHORITY):
            expected["sha256"] = sha(root / source["path"])
        if sources.get(source["id"]) != expected:
            errors.append("Unexpected source binding: " + source["id"])
    return errors


def bundle_errors(root: Path, report: dict, imported: dict, context: dict) -> list[str]:
    """Audit every transitive byte independently of the importer return flags."""
    errors = []
    if (imported.get("candidate") != context["candidate"] or report.get("candidate") != context["candidate"]
            or imported.get("binding_hash") != context["binding_hash"] or report.get("binding_hash") != context["binding_hash"]
            or report.get("manifest") != context["candidate_file"] or imported.get("manifest") != context["candidate_file"]):
        errors.append("Different candidate, manifest or current review bindings")
    if (imported.get("files_verified") is not True or any(imported.get(k) is not False
            for k in ("renderer_executed", "automatic_acceptance", "state_changed"))):
        errors.append("Import incorrectly implies execution or acceptance")
    manifest = read(reference(root, context["candidate_file"]))
    members = {r["output"]: r for r in manifest["files"]}
    destinations = report["destinations"]
    if len(destinations) != len(members) or {r["output"] for r in destinations} != set(members):
        errors.append("Destination map does not cover exact package")
    for row in destinations:
        expected = members.get(row["output"], {})
        if row.get("candidate") != expected.get("candidate") or row.get("sha256") != expected.get("sha256"):
            errors.append("Different destination member: " + row["output"])
    expected = {(group, row["path"]): row for group, group_rows in (
        ("renderer", report["renderer"]["files"]), ("consumer", report["consumer_sources"]),
        ("destinations", destinations), ("outputs", report["files"])) for row in group_rows}
    for row in expected.values():
        reference(root, row)
    bundle = reference(root, imported["bundle"])
    with zipfile.ZipFile(bundle) as archive:
        index = json.loads(archive.read("index.json"))
        retained = {(r["group"], r["original_path"]): r for r in index["files"]}
        if len(retained) != len(index["files"]) or set(retained) != set(expected):
            errors.append("Incomplete or duplicate transitive archive membership")
        if json.loads(archive.read("report.json")) != report or archive.read("package/manifest.json") != reference(root, context["candidate_file"]).read_bytes():
            errors.append("Archive report/manifest differs from observed package")
        if hashlib.sha256(archive.read("report.json")).hexdigest() != imported["report"]["sha256"]:
            errors.append("Archive report is not the imported original bytes")
        for key, wanted in expected.items():
            item = retained.get(key)
            if item is None:
                continue
            data = archive.read(item["archive_path"])
            if data != reference(root, wanted).read_bytes() or hashlib.sha256(data).hexdigest() != item["sha256"]:
                errors.append("Transitive retained bytes differ: " + wanted["path"])
    if imported.get("observation") != {"path": imported["bundle"]["path"], "sha256": imported["bundle"]["sha256"],
                                       "mode": "live", "note": imported.get("observation", {}).get("note")}:
        errors.append("Review observation is not bound to complete imported bundle")
    return errors


def motion_errors(report: dict) -> list[str]:
    errors = []
    views = {(r["consumer"], r["scale"]) for r in report["views"] if r["state"] == "running" and r["member_outputs"]}
    if not {(c, s) for c in ("statusCell", "compactStatus") for s in (1, 3)} <= views:
        errors.append("Working package missing actual full/compact native/enlarged views")
    for consumer in ("statusCell", "compactStatus"):
        motions = [m for m in report["motion"] if m["consumer"] == consumer and m["state"] == "running"
                   and m["mode"] == "requestAnimationFrame playback" and m["status"] == "observed"]
        if len(motions) != 1:
            errors.append("No unique actual callback playback: " + consumer)
            continue
        motion = motions[0]
        frames = [s["frame"] for s in motion["samples"]]
        changed = [f for i, f in enumerate(frames) if i == 0 or f != frames[i - 1]]
        if (motion["frame_ms"] != 150 or motion["frame_count"] != 4 or len(changed) < 9
                or any(b != (a + 1) % 4 for a, b in pairwise(changed))):
            errors.append("150ms live consecutive four-frame loops not observed: " + consumer)
    return errors


def capture_errors(root: Path, report: dict, capture: dict, capture_path: Path) -> list[str]:
    """Bind structured views and live samples to the exact raw renderer observations."""
    errors = []
    files = {row["id"]: row for row in report["files"]}
    captures = {row["path"]: row for row in report["files"]}
    raw_ref = captures.get(capture_path.relative_to(root).as_posix(), {})
    if raw_ref.get("sha256") != sha(capture_path) or report["observed_at"] != capture["observed_at"]:
        errors.append("Structured report is not bound to exact raw capture/time")
    launch = read(capture_path.parent / "launch.json")
    if (report["renderer"]["command"] != [launch["browser"], *launch["args"]]
            or report["renderer"]["runtime"] != {"name": "browser", "version": capture["browser_version"]["product"]}):
        errors.append("Declared renderer identity differs from actual capture")
    if report["viewport"] != {"width": capture["viewport"]["width"], "height": capture["viewport"]["height"],
                               "device_scale_factor": capture["devicePixelRatio"]}:
        errors.append("Declared viewport differs from capture")
    def output_matches(output_id, raw):
        row = files.get(output_id, {})
        expected_path = (capture_path.parent / raw["path"]).relative_to(root).as_posix()
        return row.get("path") == expected_path and row.get("sha256") == raw["sha256"] and row.get("role") == "image"
    expected_views = [v for v in capture["views"] if "image" in v]
    if len(report["views"]) != len(expected_views):
        errors.append("Structured view inventory differs from raw renderer")
    for view in expected_views:
        matches = [v for v in report["views"] if all(v[k] == view[k] for k in ("consumer", "state", "scale"))]
        if len(matches) != 1 or not output_matches(matches[0]["output_id"], view["image"]):
            errors.append("Structured view differs from raw renderer")
    playback = capture.get("playback", {})
    for motion in (m for m in report["motion"] if m["mode"] == "requestAnimationFrame playback"):
        if (motion["status"] != playback.get("status") or motion["frame_ms"] != playback.get("frameMs")
                or motion["frame_count"] != playback.get("frameCount")
                or len(motion["samples"]) != len(playback.get("samples", []))):
            errors.append("Structured live playback identity differs from raw renderer")
            continue
        for observed, raw in zip(motion["samples"], playback.get("samples", []), strict=True):
            cells = [c for c in raw["cells"] if c["consumer"] == motion["consumer"]]
            if (len(cells) != 1 or observed["elapsed_ms"] != raw["elapsed"] or observed["frame"] != cells[0]["frame"]
                    or not output_matches(observed["output_id"], cells[0]["image"])):
                errors.append("Structured live sample differs from actual painted frame")
                break
    declared_sources = {r["path"]: r["sha256"] for r in [*report["renderer"]["files"], *report["consumer_sources"]]}
    for name, digest in capture["served_files"].items():
        group, path = name.split("/", 1)
        relative = path if group == "consumer" else RENDERER + "/" + path
        if declared_sources.get(relative) != digest:
            errors.append("Actual served source omitted or changed: " + relative)
    for destination in report["destinations"]:
        if capture["served_files"].get("consumer/" + destination["path"]) != destination["sha256"]:
            errors.append("Package destination not served in actual capture")
    return errors


def _grade(attempt: Path, continuation_attempt: Path | None = None) -> dict:
    attempt = attempt.resolve()
    launch, identity, continuation = (read(attempt / n) for n in ("launch.json", "identity.json", "continuation.json"))
    root = Path(launch["cwd"]).resolve()
    caller = fields(read(root / WORK / "CALLER-RESULT.json"))
    specialist = fields(read(reference(root, caller["specialist_result"])))
    values = {k: read(reference(root, specialist[k])) for k in REFS}
    for key in set(REFS) - {"obsolete_dispatch", "obsolete_completion", "final_document", "destination_report", "capture_report", "renderer_check"}:
        values[key] = semantic_result(values[key])
    checks = []
    def check(name, passed, evidence=None):
        checks.append({"check": name, "pass": bool(passed), "evidence": evidence})
    journals = [rows(p) for p in sorted(attempt.glob("native-*.jsonl"))]
    journals += [rows(p) for p in sorted((attempt / "native-transcripts").glob("*.jsonl"))]
    stdout = rows(attempt / "stdout.jsonl")
    selected = native_identity(caller.get("native_child"), launch["host"])
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
        proof = codex_role_proof(journals, continuation["session_id"], selected, role)
        ids = {c["id"] for c in proof["selected_children"]}
        children = [[j[0], *own_rows(j, continuation["session_id"], cold=True)]
                    for j in journals if j and j[0].get("payload", {}).get("id") in ids]
        check("actual_isolated_named_child_completed", proof["loaded"] and proof["completed"], {k: v for k, v in proof.items() if k != "child_text"})
        loading = {name: {"loaded": bool(complete_file_proof(children, root / KIT / name)),
                          "evidence": complete_file_proof(children, root / KIT / name)}
                   for name in ("skills/pixl/SKILL.md", "resources/agent/PROFILE.md")}
    else:
        parent = [r for r in stdout if not r.get("parent_tool_use_id") and not r.get("agent_id")]
        children = [j for j in journals if j and Path(j[0]["file"]).stem.removeprefix("agent-") == selected]
        proof = claude_completion(parent, selected)
        check("actual_named_child_completed", bool(proof) and any(c.get("id", c.get("agent_id")) == selected
              and c.get("role") == "pixl:pixl" for c in continuation.get("children", [])), proof)
        loading = claude_loading_proof(children, root / KIT)
    check("selected_child_loaded_common_production_profile_and_skill", all(v["loaded"] for v in loading.values()), loading)
    proof = plar_skill_proof(children, root)
    check("selected_child_loaded_operational_PLAR_skill", bool(proof), proof)
    check("scope_limits_and_next_action_explicit", all(bool(v.get(k)) for v in (caller, specialist) for k in ("scope", "limitations", "next_action")))
    original = identity["inputs"]
    current_files = inventory(root, ("__pycache__",))
    mutable = {PLAR, identity["baseline_prepare"]["store"] + "/state.px",
               identity["baseline_prepare"]["store"] + "/HEAD"}
    drift = [p for p, digest in original.items() if current_files.get(p) != digest and p not in mutable]
    check("original_art_sources_kit_and_prior_evidence_preserved", not drift, drift)
    check("exact_five_art_hashes_preserved", all(sha(root / p) == identity["original_inputs"][p] for p in ART))
    before_files = read(attempt / "before-change-files.json")
    source_change = read(attempt / "source-change.json")
    changed_sources = {p for p, digest in before_files.items() if original.get(p) != digest and p not in {"AGENTS.md", "SESSION.md"}}
    check("controlled_change_is_only_timing_source_and_explicit_authority", changed_sources == {TIMING, AUTHORITY}
          and source_change["old_frame_ms"] == 100 and source_change["new_frame_ms"] == 150
          and source_change["before"] == {p: before_files[p] for p in changed_sources}
          and source_change["after"] == {p: original[p] for p in changed_sources}, source_change)
    final = read(root / PLAR)
    authored = copy.deepcopy(values["final_document"])
    final_assets = {a["id"]: a for a in final["assets"]}
    for asset in authored.get("assets", []):
        if asset["id"] == "queue.working":
            for key in ("production", "status", "evidence", "next"):
                if key in final_assets[asset["id"]]:
                    asset[key] = final_assets[asset["id"]][key]
                else:
                    asset.pop(key, None)
    check("authored_allocation_matches_final_requirements_before_lifecycle_advances", authored == final,
          "Public preparation/review can advance only Working's production link, status, evidence and next action after allocation save.")
    errors = allocation_errors(identity["baseline_document"], final, root)
    check("only_authorized_Working_timing_and_lifecycle_changed", not errors, errors)
    before = identity["baseline_prepare"]
    check("genuine_baseline_prepared_unsubmitted_intent", before["job"]["state"] == "prepared" and not before["job"]["events"]
          and not before["job"]["remote_id"] and before["remote_executed"] is False and before["acceptance_created"] is False)
    for key, tool in (("initial_read", "pixl_plar_read"), ("allocation_save", "pixl_plar_save"),
                      ("current_selection", "pixl_plar_read"), ("old_abandon", "pixl_job_observe"),
                      ("revised_prepare", "pixl_plar_prepare"), ("new_abandon", "pixl_job_observe"),
                      ("sample_review", "pixl_candidate_review"), ("delivery_build", "pixl_family_snapshot"),
                      ("delivery_context", "pixl_review_context"), ("destination_import", "pixl_destination_import"),
                      ("delivery_review", "pixl_candidate_review"), ("final_selection", "pixl_plar_read"), ("handoff", "pixl_plar_handoff")):
        proof = operation_proof(children, root, tool, specialist[key])
        check("child_actual_public_" + key, bool(proof), proof)
    for key, tool in (("obsolete_dispatch", "pixl_job_dispatch"), ("obsolete_completion", "pixl_task_complete")):
        proof = operation_proof(children, root, tool, specialist[key], success=False)
        errors = [v for v in expanded_objects(values[key]) if v.get("error") and v.get("recovery")]
        check("actual_obsolete_" + key + "_refusal", bool(proof) and bool(errors), {"calls": proof, "errors": errors,
              "scope": "The retained exact refusal code establishes its cause; missing prerequisites alone do not establish the stale-selection guard."})
    revised = values["revised_prepare"]
    selected_now = service.call("pixl_plar_read", {"path": PLAR, "asset_id": "queue.working"}, root)
    effective_task = selected_now["asset"]["production"]["task"]
    if revised["task"] != effective_task:
        for path in sorted((root / WORK).glob("*.json")):
            try:
                item = semantic_result(read(path))
            except (ValueError, TypeError):
                continue
            if isinstance(item, dict) and item.get("task") == effective_task and isinstance(item.get("job"), dict) and "outputs" in item:
                ref = {"path": path.relative_to(root).as_posix(), "sha256": sha(path)}
                proof = operation_proof(children, root, "pixl_plar_prepare", ref)
                if proof:
                    revised = item
                    check("additional_corrected_successor_has_actual_public_preparation", True, {"reference": ref, "calls": proof})
                    break
    check("explicit_successor_uses_current_requirements", revised["task"] == effective_task != before["task"]
          and revised["requirements_hash"] == selected_now["requirements_hash"] != before["requirements_hash"]
          and revised["job"]["id"] != before["job"]["id"] and revised["acceptance_created"] is False)
    folder = graph.confined(root, revised["store"])
    doc = store.load(folder)
    graph.validate(doc, root)
    job_rows = jobs.report(doc, root, folder)["jobs"]
    history_errors = []
    if not {before["job"]["id"], revised["job"]["id"]} <= {j["id"] for j in job_rows}:
        history_errors.append("Missing baseline or effective revised intent")
    for job in job_rows:
        baseline = before["job"] if job["id"] == before["job"]["id"] else revised["job"] if job["id"] == revised["job"]["id"] else job
        if (job["state"] != "failed" or job["remote_id"] or job["intent_sha256"] != baseline["intent_sha256"]
                or job["request"] != baseline["request"] or job["context"] != baseline["context"]
                or len(job["events"]) != 1 or job["events"][0]["event"] != "failed"
                or not job["events"][0].get("evidence")):
            history_errors.append("Intent/history is not explicit local abandonment: " + job["id"])
    check("all_retained_intents_locally_abandoned_without_remote_or_rewritten_history", not history_errors, history_errors)
    baseline_doc = store.load(attempt / "baseline-pixl" / Path(before["store"]).relative_to(".pixl"))
    changed = [ident for ident, record in baseline_doc.records.items() if ident not in doc.records
               or record.kind not in ("T", "J", "P") and record != doc.records[ident]]
    for ident, record in baseline_doc.records.items():
        if record.kind != "P":
            continue
        current = doc.records[ident].fields
        old = record.fields
        if (any(current[k] != old[k] for k in old if k not in ("br", "in", "sc"))
                or not current["br"].startswith(old["br"].split("\n", 1)[0])
                or any(current[k][:len(old[k])] != old[k] for k in ("in", "sc"))):
            changed.append(ident)
    check("prior_records_and_old_uncompleted_task_preserved", not changed and doc.records[before["task"]].fields["st"].value != "done", changed)
    sample_id = values["sample_review"]["candidate"]
    sample = candidate_review.context(doc, root, sample_id)
    check("fresh_exact_reused_candidate_passes_current_successor", sample["output"] in revised["outputs"]
          and sample["candidate_file"]["sha256"] == identity["original_inputs"]["assets/working.png"]
          and sample["current_acceptance"] == {"all_required_pass": True, "task_complete": True}
          and sample["nominated"] and sample_id not in baseline_doc.records)
    imported, report = values["destination_import"], values["destination_report"]
    context = candidate_review.context(doc, root, imported["candidate"])
    plans = [read(graph.confined(root, r.fields["ur"]))["plan"] for r in doc.records.values()
             if r.kind == "X" and r.fields.get("mt", {}).get("binding") == "pixl.production.plan/1"]
    check("delivery_only_plan_reuses_accepted_current_sample", any(p["stages"] == [] and p["baseline"] == sample_id for p in plans)
          and len(context.get("members", [])) == 1 and context["members"][0]["candidate"] == sample_id)
    errors = bundle_errors(root, report, imported, context)
    check("exact_current_NF06_bundle_retains_all_report_inputs_outputs", not errors, errors)
    errors = motion_errors(report)
    check("full_and_compact_current150ms_live_loops_and_views", not errors, errors)
    capture_path = reference(root, specialist["capture_report"])
    capture = values["capture_report"]
    if "capture" in capture and "views" not in capture:
        raw_path = Path(capture["capture"]).resolve()
        if not raw_path.is_relative_to(root):
            raise ValueError("Renderer stdout points outside consumer")
        retained = next((f for f in report["files"] if f["path"] == raw_path.relative_to(root).as_posix()), None)
        if retained is None:
            raise ValueError("Renderer stdout raw capture is not retained in NF06 report")
        capture_path = reference(root, retained)
        capture = read(capture_path)
    errors = capture_errors(root, report, capture, capture_path)
    check("structured_observations_match_actual_raw_capture", not errors, errors)
    checker = root / RENDERER / "check.py"
    if sha(checker) != original[checker.relative_to(root).as_posix()]:
        raise ValueError("Renderer checker changed")
    spec = importlib.util.spec_from_file_location("integration_retained_check", checker)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    measured = module.check(root, capture_path.parent)
    check("independent_retained_renderer_pixel_and_clock_checks", measured["status"] == "pass" and capture["display"]["frameMs"] == 150,
          {"status": measured["status"], "checks": len(measured["observations"]), "failures": measured["failures"]})
    authored_check = values["renderer_check"]
    check("native_checker_result_matches_independent_measurement", authored_check == measured)
    actual_commands = commands(children)
    check("child_executed_real_renderer_and_checker", any(c["exit_code"] == 0 and "capture.mjs" in c["command"] for c in actual_commands)
          and any(c["exit_code"] == 0 and "check.py" in c["command"] for c in actual_commands))
    expected_images = {capture["screenshot"]["sha256"]}
    expected_images.update(v["image"]["sha256"] for v in capture["views"] if v["state"] == "running" and v["scale"] in (1, 3))
    for actor, actor_journals in (("specialist", children), ("parent", [parent])):
        views = image_views(actor_journals, root)
        check(actor + "_viewed_exact_destination_and_both_Working_views", expected_images <= set(views),
              {"required_hashes": sorted(expected_images), "observed": views})
    check("explicit_current_delivery_review_acceptance", context["current_acceptance"] == {"all_required_pass": True, "task_complete": True}
          and context["nominated"] and context["snapshot_acceptance"]["accepted"] is False)
    check("review_retains_the_imported_live_bundle", any(r.kind == "X" and r.fields.get("dg") == imported["bundle"]["sha256"] for r in doc.records.values()))
    parent_refresh = semantic_result(read(reference(root, caller["parent_refresh"])))
    actual_refresh = service.call("pixl_plar_read", {"path": PLAR, "since": identity["baseline_hash"]}, root)
    proof = operation_proof([parent], root, "pixl_plar_read", caller["parent_refresh"])
    check("parent_independent_current_history_refresh", parent_refresh == actual_refresh and bool(proof), proof)
    selections = read(reference(root, caller["parent_selections"])) if "path" in caller["parent_selections"] else caller["parent_selections"]
    if "current" in selections and not any(ident in selections for ident in ASSETS):
        selections = selections["current"]
    for ident in ASSETS:
        item = selections[ident]
        value = semantic_result(read(reference(root, item))) if isinstance(item, dict) and {"path", "sha256"} <= set(item) else semantic_result(item)
        actual = service.call("pixl_plar_read", {"path": PLAR, "asset_id": ident}, root)
        changed = actual["requirements_hash"] != identity["baseline_selections"][ident]["requirements_hash"]
        proofs = []
        if isinstance(item, dict) and {"path", "sha256"} <= set(item):
            proofs = operation_proof([parent], root, "pixl_plar_read", item)
        else:
            for path in (root / WORK).glob("*.json"):
                try:
                    exact = semantic_result(read(path)) == value
                except (ValueError, TypeError):
                    continue
                if exact:
                    proofs += operation_proof([parent], root, "pixl_plar_read",
                                              {"path": path.relative_to(root).as_posix(), "sha256": sha(path)})
        check("parent_current_selection_" + ident, value == actual and changed == (ident == "queue.working") and bool(proofs), proofs)
    parent_acceptance = semantic_result(read(reference(root, caller["parent_acceptance"])))
    if "families" in parent_acceptance:
        proof = operation_proof([parent], root, "pixl_family", caller["parent_acceptance"])
        actual_acceptance = service.call("pixl_family", {"path": (folder / "state.px").relative_to(root).as_posix()}, root)
    else:
        proof = operation_proof([parent], root, "pixl_review_context", caller["parent_acceptance"])
        actual_acceptance = service.describe_result("review_context", context)
    check("parent_independent_current_package_acceptance", bool(proof) and parent_acceptance == actual_acceptance, proof)
    check("parent_consumed_exact_handoff", reference(root, caller["handoff"]).resolve() == reference(root, specialist["handoff"]).resolve()
          and bool(caller.get("independent_checks")))
    prohibited = [c for c in mcp_attempts(journals + [stdout]) if str(c["server"]).replace("-", "_") != "pixl_local"]
    check("no_recorded_external_provider_tool_attempt", not prohibited, prohibited)
    check("native_attempt_completed", continuation.get("status") == "finished" and continuation.get("returncode") == 0 and continuation.get("interruption_reason") is None)
    return {"version": 1, "status": "pass" if all(c["pass"] for c in checks) else "fail",
            "passed": sum(c["pass"] for c in checks), "total": len(checks), "checks": checks,
            "scope": "Controlled 100-to-150ms integration using exact retained art. Source/call/byte/pixel checks and recorded visual access do not independently judge artistic quality. No new provider art, general host reliability, or M1/M2/broader M3 closure."}


def grade(attempt: Path, continuation: Path | None = None) -> dict:
    try:
        return _grade(attempt, continuation)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, codec.PixlError, zipfile.BadZipFile) as error:
        return {"version": 1, "status": "fail", "passed": 0, "total": 1,
                "checks": [{"check": "required_evidence_readable", "pass": False, "evidence": f"{type(error).__name__}: {error}"}]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attempt", type=Path)
    parser.add_argument("--out", "--output", type=Path, required=True)
    parser.add_argument("--continuation", type=Path, help="Verified additive same-parent continuation; original attempt remains retained")
    args = parser.parse_args(argv)
    if args.out.exists():
        raise ValueError("Preserve earlier grades; choose a fresh output")
    result = grade(args.attempt, args.continuation)
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(json.dumps({k: result[k] for k in ("status", "passed", "total")}))
    return result["status"] != "pass"


if __name__ == "__main__":
    raise SystemExit(main())
