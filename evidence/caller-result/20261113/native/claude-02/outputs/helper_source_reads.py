"""Parent caller helper: retrieve details_ref and resume_ref byte-exactly through the frozen kit's
local MCP server (stdio JSON-RPC, same route as missing_capability_probe.py). Read-only.
Writes only fresh files under work/compact-caller. Locators are taken from compact.json, not retyped."""
import hashlib, json, pathlib, subprocess, sys
root = pathlib.Path(__file__).resolve().parents[2]
out = root / "work/compact-caller"
compact = json.loads((out / "compact.json").read_text("utf-8"))
reqs = []
for i, (name, ref, budget) in enumerate((("details", compact["details_ref"], 65536), ("resume", compact["resume_ref"], 8192)), start=1):
    reqs.append({"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": "pixl_source", "arguments": {
        "path": ref["path"], "expect": ref["sha256"], "start": ref["start"], "end": ref["end"], "budget": budget, "scope": "project"}}})
proto = out / "source-reads-protocol.jsonl"
if proto.exists(): raise SystemExit("protocol output exists; use a fresh name")
p = subprocess.run([sys.executable, "-B", str(root / "installed pixl/scripts/pixl.py"), "mcp", "--root", str(root)],
                   input="".join(json.dumps(r) + "\n" for r in reqs).encode("utf-8"), capture_output=True)
with proto.open("xb") as s: s.write(p.stdout)
with proto.with_suffix(".stderr.txt").open("xb") as s: s.write(p.stderr)
responses = {r["id"]: r for r in (json.loads(l) for l in p.stdout.splitlines() if l.strip())}
lines = (root / compact["details_ref"]["path"]).read_text("utf-8").split("\n")
summary = {"returncode": p.returncode, "reads": {}}
for i, name in ((1, "details"), (2, "resume")):
    res = responses[i]["result"]
    text = res["content"][0]["text"]
    target = out / f"{name}-read.json"
    if target.exists(): raise SystemExit(f"{target} exists")
    target.write_bytes(text.encode("utf-8"))
    obj = json.loads(text)
    ref = compact[f"{name}_ref"]
    physical = "\n".join(lines[ref["start"] - 1: ref["end"]]) + "\n"
    summary["reads"][name] = {
        "saved": f"work/compact-caller/{name}-read.json",
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "isError": res.get("isError", False),
        "returned": {k: obj[k] for k in ("sha256", "start", "end", "bytes")},
        "locator": ref,
        "text_utf8_bytes": len(obj["text"].encode("utf-8")),
        "bytes_match_locator": len(obj["text"].encode("utf-8")) == ref["bytes"],
        "text_equals_physical_lines": obj["text"] == physical,
        "trailing_member_comma_preserved": obj["text"].rstrip("\n").endswith(","),
        "json_pointer": ref["json_pointer"],
    }
print(json.dumps(summary, indent=1))
