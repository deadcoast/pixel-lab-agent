"""Capture a read-only local MCP error without hand-copying its escaped detail."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
target = root / "work/compact-caller/revision-03"
paths = [target / "unavailable-protocol.jsonl", target / "unavailable-protocol.stderr.txt",
         target / "errors/unavailable-observation.json"]
if any(path.exists() for path in paths):
    raise ValueError("Preserve prior captures; this helper only creates fresh outputs")
arguments = {"path": "work/compact-caller/intentionally-missing.txt", "expect": "0" * 64,
             "start": 1, "end": 1}
requests = [{"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
             "params": {"name": "pixl_source", "arguments": arguments}}]
proc = subprocess.run([sys.executable, "-B", str(root / "installed pixl/scripts/pixl.py"),
                       "mcp", "--root", str(root)],
                      input="".join(json.dumps(row) + "\n" for row in requests).encode(), capture_output=True)
target.mkdir(parents=True, exist_ok=True)
for path, data in zip(paths[:2], (proc.stdout, proc.stderr)):
    with path.open("xb") as stream:
        stream.write(data)
responses = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
response = next(row for row in responses if row.get("id") == 2)
result = response["result"]
error = result["structuredContent"]
if proc.returncode or result["isError"] is not True or error["category"] != "unavailable_observation" or error["identity"]["path"] != arguments["path"]:
    raise ValueError("Expected exact rejected local missing-file read; inspect retained raw protocol")
paths[2].parent.mkdir(exist_ok=True)
with paths[2].open("x", encoding="utf-8", newline="\n") as stream:
    json.dump(result, stream, ensure_ascii=False, indent=2)
    stream.write("\n")
print(json.dumps({"scope": "Actual frozen-kit local MCP read; no provider or state mutation",
                  "arguments": arguments, "original_error": error,
                  "saved": [{"path": path.relative_to(root).as_posix(),
                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                            for path in paths]}, ensure_ascii=False))
