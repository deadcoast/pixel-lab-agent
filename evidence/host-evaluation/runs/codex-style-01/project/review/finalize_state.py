"""Retain the completed report review; leave the planned lantern unperformed."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
runner = root / ".agents/skills/pixl-kit/scripts/pixl.py"
def cli(*args):
    return subprocess.check_output([sys.executable, str(runner), *args], cwd=root, text=True, encoding="utf-8")
doc = json.loads(cli("decode", ".pixl/state.px"))
assert doc["revision"] == 1
doc["revision"] = 2
rows = doc["records"]
ref = lambda name: {"$ref": name}
sym = lambda value: {"$symbol": value}
def add(name, kind, **fields):
    rows.append({"id": name, "kind": kind, "fields": fields})
def digest(path):
    return sha256((root/path).read_bytes()).hexdigest()
def encode(name):
    adapter = root/f"review/{name}.adapter.json"
    adapter.write_text(json.dumps(doc,indent=2)+"\n",encoding="utf-8")
    cli("encode",str(adapter),"--out",f"review/{name}.candidate.px")

add("x.approach","X",nm="Completed lantern reference review and production approach",ur="lantern-production-approach.md",dg=digest("lantern-production-approach.md"),kd=sym("report"),of=ref("f.approach"))
task = next(row["fields"] for row in rows if row["id"]=="t.approach")
task["ca"]=[ref("x.approach")]
encode("report-unreviewed")
checked=json.loads(cli("validate","review/report-unreviewed.candidate.px","--root",str(root)))
assert checked["valid"]
hashes=checked["record_hashes"]

# The acting agent read the report against the saved q.approach requirement.
# This is a local document-completeness review, not lantern artistic acceptance.
now=datetime.now(timezone.utc).isoformat()
receipt={
    "observed_at":now,
    "reviewer":"PIXL acting agent",
    "criterion":"q.approach",
    "artifact":"lantern-production-approach.md",
    "artifact_sha256":digest("lantern-production-approach.md"),
    "mode":"local",
    "result":"pass",
    "observations":[
        "The report preserves the explicit full-alpha and selective-AA requirements and states no fixed palette.",
        "Measured source values match retained measurements: 32x32, 20x25 visible bounds, 30 fractional pixels, alpha 0/96/160/255, three RGB colors versus five visible RGBA combinations.",
        "The report uses the completed native/8x reference inspection and identifies dark-background contrast loss without claiming new lantern acceptance.",
        "Canvas, view, footprint, lantern design, anchor, alpha export and sampling are proposals; final engine, display scale and target backgrounds remain unknown.",
        "Method IDs, exact source ranges, conditional palette applicability, insufficient alpha citations and offline proof limitations are retained.",
        "One representative lantern is planned with separate mechanical, edit-locality, visual and future engine checks; no new sprite path or provider observation is invented."
    ],
    "limits":"Completes reference-review/approach scope only. No lantern candidate or project-specific method proof. No engine or remote generation acceptance."
}
receipt_path="review/approach-review-receipt.json"
(root/receipt_path).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
record_map={row["id"]:row for row in rows}
semantic={"A","S","R","C","K","D","X","I","F","Q"}
def walkrefs(value):
    if isinstance(value,dict):
        if "$ref" in value:
            yield value["$ref"]
        else:
            for v in value.values():
                yield from walkrefs(v)
    elif isinstance(value,list):
        for v in value:
            yield from walkrefs(v)
scope=set()
def visit(name):
    if name in scope or record_map[name]["kind"] not in semantic:
        return
    scope.add(name)
    for target in walkrefs(record_map[name]["fields"]):
        visit(target)
visit("x.approach")
visit("q.approach")
add("e.approach-review","E",nm="Report completeness review against saved approach criterion",ur=receipt_path,dg=digest(receipt_path),rs=sym("pass"),md=sym("local"),at=now,bs=[{"rf":ref(name),"dg":hashes[name]} for name in sorted(scope)])
add("v.approach-review","V",tk=ref("t.approach"),rq=ref("q.approach"),xr=ref("x.approach"),st=sym("pass"),wh=ref("actor"),wy="Document reviewed against the previously saved criterion; constraints, observed evidence, proposals, source limitations and next proof are explicit. This accepts the approach document only.",at=now,ev=[ref("e.approach-review")])
task["vr"]=[ref("v.approach-review")]
task["st"]=sym("done")
next(row["fields"] for row in rows if row["id"]=="handoff")["rv"]=2
encode("final")
print(json.dumps({"report_sha256":digest("lantern-production-approach.md"),"reviewed_scope":sorted(scope),"candidate":"review/final.candidate.px"},indent=2))
