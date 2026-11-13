"""Retain exact host-spilled MCP bodies with their native call and file locators."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from evaluations.grade_named_codex_role import rows, strings
from evaluations.host_trials import write_json
from evaluations.native_trial_records import reference


def spill_locator(call, session):
    matches = []
    for text in strings(call.get("result")):
        match = re.match(r"^Error: result \(([\d,]+) characters\) exceeds maximum allowed tokens\. Output has been saved to (.+)\.\nFormat: JSON", text)
        if match:
            path = Path(match[2]).resolve()
            if (path.parent.name == "tool-results" and path.parent.parent.name == session
                    and re.fullmatch(r"mcp-" + re.escape(call["server"] + "-" + call["tool"]) + r"-\d+\.txt", path.name)):
                matches.append({"path": str(path), "characters": int(match[1].replace(",", ""))})
    return matches[0] if len(matches) == 1 else None


def binding(call):
    return {key: call[key] for key in ("call_id", "server", "tool", "arguments")}


def retain(attempt, destination):
    """Observe host files now; never substitute caller-authored copies or hashes."""
    from evaluations.grade_caller_result import mcp_calls
    attempt, destination = Path(attempt).resolve(), Path(destination).resolve()
    continuation = json.loads((attempt / "continuation.json").read_bytes())
    if continuation.get("status") != "finished" or destination.exists():
        raise ValueError("Retain from a finished attempt into a fresh directory")
    session = continuation["session_id"]
    journals = [rows(p) for p in sorted((attempt / "native-transcripts").glob("*.jsonl"))]
    entries, payloads = [], {}
    for call in mcp_calls(journals):
        locator = spill_locator(call, session)
        if not locator:
            continue
        source = Path(locator["path"])
        raw = source.read_bytes()
        text = raw.decode("utf-8")
        if len(text) != locator["characters"]:
            raise ValueError("Host-spilled result length differs from its native locator")
        json.loads(text)
        name = source.name
        if name in payloads and payloads[name] != raw:
            raise ValueError("Conflicting host-spilled result identities")
        payloads[name] = raw
        entries.append({"call": binding(call), "native_journal": reference(call["file"]), "call_line": call["line"],
                        "locator": locator, "source": reference(source), "archive_name": name})
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in payloads.items():
        with (destination / name).open("xb") as stream:
            stream.write(raw)
    for entry in entries:
        entry["archive"] = reference(destination / entry.pop("archive_name"))
    manifest = {"version": 1, "session_id": session, "attempt": reference(attempt / "continuation.json"),
                "scope": "Host-produced spill files observed and retained after completion; native locators provide path and character count, not a historical content hash.",
                "bindings": entries, "retention_source": reference(Path(__file__))}
    write_json(destination / "manifest.json", manifest)
    return manifest


def bind_retained(calls, session, directories):
    """Use only exact archived host bytes linked to matching actual native calls."""
    from evaluations.grade_caller_result import mcp_calls
    entries = []
    for directory in directories:
        directory = Path(directory).resolve()
        manifest_path = directory / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        if manifest.get("session_id") != session:
            raise ValueError("Host result archive belongs to a different session")
        checked_journals = {}
        for entry in manifest["bindings"]:
            archived = Path(entry["archive"]["path"]).resolve()
            journal = entry["native_journal"]
            if (not archived.is_relative_to(directory) or reference(archived) != entry["archive"]
                    or entry["archive"]["sha256"] != entry["source"]["sha256"]
                    or entry["archive"]["bytes"] != entry["source"]["bytes"]
                    or entry["source"]["path"] != entry["locator"]["path"]):
                raise ValueError("Retained host result bytes or source identity changed")
            if journal["path"] not in checked_journals:
                if reference(journal["path"]) != journal:
                    raise ValueError("Host result's original native journal changed")
                checked_journals[journal["path"]] = mcp_calls([rows(Path(journal["path"]))])
            if not any(binding(c) == entry["call"] and c["line"] == entry["call_line"]
                       and spill_locator(c, session) == entry["locator"] for c in checked_journals[journal["path"]]):
                raise ValueError("Retained host result has no matching original native call")
            raw = archived.read_bytes()
            if len(raw.decode("utf-8")) != entry["locator"]["characters"]:
                raise ValueError("Retained host result does not satisfy the native character count")
            entries.append({**entry, "manifest": reference(manifest_path), "body": json.loads(raw)})
    result = []
    for call in calls:
        locator = spill_locator(call, session)
        matching = [entry for entry in entries if entry["call"] == binding(call) and entry["locator"] == locator]
        if matching:
            if len({entry["archive"]["sha256"] for entry in matching}) != 1:
                raise ValueError("Conflicting retained bodies for the same native call")
            item = matching[0]
            call = {**call, "result": [item["body"], call["result"]],
                    "native_spill": {k: item[k] for k in ("manifest", "native_journal", "call_line", "locator", "source", "archive")}}
        result.append(call)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attempt", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    result = retain(args.attempt, args.destination)
    print(json.dumps({"bindings": len(result["bindings"]), "files": len({entry["source"]["sha256"] for entry in result["bindings"]})}))
