"""Append the edited west candidate, a source record for the caller comparison, and
confirm the three reviewed candidate choices (caller COMPARISON.json adopted them).

Usage: python -I author_edited_west_and_confirm.py ROOT DECODED_JSON OUT_JSON
Then: pixl commit --json --expect HASH --root ROOT STORE OUT_JSON
"""
import json
import sys
from pathlib import Path

root, src, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
doc = json.loads(src.read_text(encoding="utf-8"))
G = "r.acf329804ba043b7."
REF = lambda i: {"$ref": i}
SYM = lambda v: {"$symbol": v}
by_id = {r["id"]: r for r in doc["records"]}

new = [
    {"id": "source.comparison", "kind": "S", "fields": {
        "ur": "work/native-production/COMPARISON.json",
        "dg": "503de778135f188c64f45eab170144e65fc3b3d375ef566be01b18083b1169a2",
        "ln": [1, 1019], "at": "2026-11-12", "au": SYM("local")}},
    {"id": "source.west_edit_receipt", "kind": "S", "fields": {
        "ur": "work/native-production/edited/west-mirror-of-east.receipt.json",
        "dg": __import__("hashlib").sha256((root / "work/native-production/edited/west-mirror-of-east.receipt.json").read_bytes()).hexdigest(),
        "ln": [], "at": "2026-11-12", "au": SYM("local")}},
    {"id": "candidate.west.edited", "kind": "X", "fields": {
        "nm": "West: deterministic horizontal mirror of the generated east frame (edited candidate)",
        "ur": "work/native-production/edited/west-mirror-of-east.png",
        "dg": "ec96bf6379daf161ce8643894b72c50b4bb543e105f336cbc58f27293df655a0",
        "ct": REF(G + "contract.west"), "kd": SYM("sprite"), "of": REF(G + "output.west"),
        "mt": {"provenance": "edited", "operation": "PIL ImageOps.mirror of candidate.east.raw (sha256 71b35089965b6457f505d569f4fc89fbcc2521bf188aa43f836dc207c3771fb4); no generation",
               "edited_from_provider_candidate": "candidate.east.raw",
               "replaces_raw": "candidate.west.raw (sha256 8209e5f6bc71d22eb76a6aa98b8bf08ffcfea46aafaf0bd056e649d64980f84c), which lacks the teal front edge",
               "pixel_diff_vs_raw_west": "17 px: x=10 rows 11-25 navy->teal (front edge), (10,26) and (10,27) navy->transparent (east's bottom-row notch mirrored)",
               "receipt": "work/native-production/edited/west-mirror-of-east.receipt.json",
               "object_id": "2a3cb51a-6cf7-485d-8441-3c3db762cc9d"},
        "tg": ["robot.directions", "west", "edited"]}},
]
for r in new:
    if r["id"] in by_id:
        raise SystemExit("exists: " + r["id"])
doc["records"].extend(new)
# confirm the three reviewed candidate choices; sources now include the caller comparison
for name in ("east", "north", "west"):
    rec = by_id[G + f"choice.{name}"]
    assert rec["fields"]["st"] == {"$symbol": "proposed"}, rec["fields"]["st"]
    rec["fields"]["st"] = SYM("confirmed")
    rec["fields"]["so"] = rec["fields"]["so"] + [REF("source.comparison")]
    rec["fields"]["wy"] = (rec["fields"]["wy"] + " Confirmed 2026-11-12 after the caller comparison (COMPARISON.json) accepted view=side, "
                           "binary alpha and the size/transparency/nearest requirements for this generation; the caller acts within the delegated assignment, not as a new owner approval.")
# the project must list new sources? P.sc lists sources; add the comparison source for retrieval
proj = by_id["project"]
proj["fields"]["sc"] = proj["fields"]["sc"] + [REF("source.comparison"), REF("source.west_edit_receipt")]
doc["revision"] = int(doc["revision"]) + 1
doc.setdefault("format", 2)
out.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
print("candidate written", out, "revision", doc["revision"])
