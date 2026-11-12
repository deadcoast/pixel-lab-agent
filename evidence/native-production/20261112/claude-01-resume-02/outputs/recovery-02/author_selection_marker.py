"""Recovery-02: retain the current focused PLAR selection as an immutable store blob and
author the pixl.plar.selection/1 report-X input on the delivery task, reopening it.
Uses the corrected kit's own helpers; no provider action."""
import json, sys, hashlib
from datetime import datetime, UTC
from pathlib import Path
root = Path(sys.argv[1]); kit = Path(sys.argv[2]); out_wire = Path(sys.argv[3])
sys.path.insert(0, str(kit / "runtime"))
from pixl import codec, store, plar, platform, jobs, families
from pixl.codec import Ref, Symbol, Record
folder = root / ".pixl/assets/robot.directions"
doc = store.load(folder)
# (1) is the delivery task record part of the frozen manifest bindings?
planned = families.plan(doc, "robot-directions-family.delivery.output")
print("plan keys:", list(planned.keys()))
print("bindings include delivery task:", "robot-directions-family.delivery.task" in planned["bindings"], "| count", len(planned["bindings"]))
# (2) fresh focused read through the kit (identical to pixl_plar_read) and snapshot body mirroring production_plan's selection shape
selected = plar.read(root, "production-plar.txt", "robot.directions", include_production=False)
rh = selected["requirements_hash"]
assert rh == "e3918fbaa7fcedf4be73603cd83448c4bde6f043a58f45f16a39417372a142f7", rh
now = datetime.now(UTC).isoformat(timespec="microseconds")
body = platform._json_bytes({
    "version": 1,
    "binding": "pixl.plar.selection/1",
    "created_at": now,
    "input": {"plar_path": "production-plar.txt", "asset_id": "robot.directions", "requirements_hash": rh, "plar_file_sha256": selected["hash"],
              "task": "robot-directions-family.delivery.task", "reason": "recovery-02: delivery task lacked a tagged selection input; current focused selection retained after the delivery-time PLAR update (existing rows added)"},
    "selection": {
        "project": selected["project"],
        "asset": plar._requirements(selected["asset"]),
        "dependencies": [plar._requirements(row) for row in selected["dependencies"]],
        "sources": [{k: v for k, v in row.items() if k != "absolute_path"} for row in selected["sources"]],
        "visual_references": [{k: v for k, v in row.items() if k != "absolute_path"} for row in selected.get("visual_references", [])],
    },
}) + b"\n"
snapshot, digest = jobs._blob(folder, root, "selections", body, ".json")
print("snapshot:", snapshot, "sha256:", digest)
assert hashlib.sha256((root / snapshot).read_bytes()).hexdigest() == digest
# (3) candidate document: marker X + delivery task ip + reopen
mid = "robot-directions-family.delivery.selection"
assert mid not in doc.records
doc.records[mid] = Record(mid, "X", {
    "nm": "Current PLAR selection (recovery-02)", "ur": snapshot, "dg": digest, "kd": Symbol("report"),
    "mt": {"binding": "pixl.plar.selection/1", "plar_path": "production-plar.txt", "asset_id": "robot.directions", "requirements_hash": rh}})
task = doc.records["robot-directions-family.delivery.task"]
assert task.fields["st"] == Symbol("done")
task.fields["ip"] = task.fields["ip"] + [Ref(mid)]
task.fields["st"] = Symbol("open")
doc.revision += 1
out_wire.write_bytes(codec.encode(doc))
print("candidate revision", doc.revision, "written", out_wire)
json.dump({"snapshot": snapshot, "sha256": digest, "created_at": now, "marker": mid, "requirements_hash": rh, "plar_file_sha256": selected["hash"]},
          open(root / "work/native-production/recovery-02/selection-snapshot.receipt.json", "w", encoding="utf-8"), indent=1)
