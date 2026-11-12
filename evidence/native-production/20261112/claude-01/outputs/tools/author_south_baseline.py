"""Append the south-baseline sample task (reused exact bytes) to the decoded PX2 state.

Usage: python -I author_south_baseline.py ROOT DECODED_JSON OUT_JSON
Then commit OUT_JSON with: pixl commit --json --expect HASH --root ROOT STORE OUT_JSON
No provider action. Records follow registry-v2.json; nothing is accepted here.
"""
import json
import sys
from pathlib import Path

root, src, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
doc = json.loads(src.read_text(encoding="utf-8"))
G = "r.acf329804ba043b7."  # current reviewed generation's record prefix
S = lambda n: {"$ref": G + f"source.{n}"}
SYM = lambda v: {"$symbol": v}
REF = lambda i: {"$ref": i}
ROBOT_SHA = "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7"

# source map (this generation): 8=BRIEF.md, 6=src/robot.ts, 7=assets/robot-base.png,
# 3=NATIVE-PRODUCTION.md, 4=production-plar.txt, 5=renderer-native/README.md
records = [
    {"id": "contract.south", "kind": "C", "fields": {
        "nm": "Robot facing south (preserved)", "px": [32, 32], "pl": [], "vw": SYM("side"),
        "sa": SYM("nearest"), "al": SYM("binary"),
        "li": "Byte-identical copy of assets/robot-base.png at assets/robot/south.png; the approved identity baseline for the directional family. View 'side' and binary alpha describe the source as measured; no new art."}},
    {"id": "criterion.south.bytes_identical", "kind": "Q", "fields": {
        "nm": "bytes_identical", "dm": SYM("mechanical"), "md": SYM("local"),
        "ck": "assets/robot/south.png is byte-identical to assets/robot-base.png (sha256 " + ROBOT_SHA + ").",
        "wh": REF("actor"), "so": [S(3), S(5), S(7)]}},
    {"id": "criterion.south.identity", "kind": "Q", "fields": {
        "nm": "identity", "dm": SYM("visual"), "md": SYM("visual"),
        "ck": "Viewed at 1x and 3x nearest, the file shows the approved robot identity unchanged: navy frame with two rectangular antenna posts, teal front panel, two pale-yellow eyes, transparent background.",
        "wh": REF("actor"), "so": [S(8), S(4), S(7)]}},
    {"id": "output.south", "kind": "F", "fields": {
        "tk": REF("task.south"), "nm": "Robot facing south (preserved)", "kd": SYM("sprite"),
        "rq": [REF("criterion.south.bytes_identical"), REF("criterion.south.identity")],
        "ct": REF("contract.south")}},
    {"id": "candidate.south", "kind": "X", "fields": {
        "nm": "assets/robot/south.png: exact reuse of the approved identity bytes",
        "ur": "assets/robot/south.png", "dg": ROBOT_SHA, "ct": REF("contract.south"), "kd": SYM("sprite"),
        "of": REF("output.south"),
        "mt": {"provenance": "reused", "source_path": "assets/robot-base.png", "source_sha256": ROBOT_SHA,
               "operation": "byte copy (cp), verified with cmp; no PixelLab call, no edit",
               "copied_at": "2026-11-12T08:14:00+00:00"},
        "tg": ["robot.directions", "south", "reused"]}},
    {"id": "task.south", "kind": "T", "fields": {
        "nm": "South baseline: preserve the approved identity bytes as the family baseline",
        "ow": REF("actor"), "pr": REF("project"), "dp": [], "dc": [], "kn": [],
        "st": SYM("open"), "ph": SYM("sample"), "ip": [REF(G + "reference.0")],
        "op": [REF("output.south")], "ca": [], "vr": []}},
]
existing = {r["id"] for r in doc["records"]}
for r in records:
    if r["id"] in existing:
        raise SystemExit(f"record already exists: {r['id']}")
doc["records"].extend(records)
doc["revision"] = int(doc["revision"]) + 1
doc.setdefault("format", 2)
out.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
print("candidate written", out, "revision", doc["revision"], "format", doc.get("format"))
