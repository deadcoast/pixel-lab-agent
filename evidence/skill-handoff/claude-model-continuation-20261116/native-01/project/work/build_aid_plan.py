"""Revision 3: plan the outline/scale decision aid before producing it."""
import json, subprocess, sys

PY = sys.executable
RUNNER = ".agents/skills/pixl-kit/scripts/pixl.py"

def sym(s):
    return {"$symbol": s}

def ref(s):
    return {"$ref": s}

def refs(*a):
    return [ref(x) for x in a]

cur = json.loads(subprocess.run([PY, RUNNER, "decode", "state.px/state.px"],
                                capture_output=True, text=True, check=True).stdout)
R = cur["records"]

R.append({"id": "q_aid_faithful", "kind": "Q", "fields": {
    "nm": "decision aid is a faithful enlargement",
    "dm": sym("mechanical"), "md": sym("local"),
    "ck": "Every enlarged sprite panel in the sheet is an exact integer nearest-neighbour "
          "enlargement of the supplied reference bytes: each source pixel becomes a "
          "uniform z-by-z block of the identical colour, and no sprite pixel takes a "
          "colour absent from its source file.",
    "wh": ref("user"), "so": refs("s_methods")}})

R.append({"id": "q_aid_useful", "kind": "Q", "fields": {
    "nm": "decision aid supports the decision",
    "dm": sym("visual"), "md": sym("visual"),
    "ck": "Viewed as an image, the sheet shows both outline treatments together at every "
          "sampled display scale on light, dark and busy backgrounds, and the difference "
          "between them is visible well enough to choose between them.",
    "wh": ref("user"), "so": refs("s_refobs")}})

R.append({"id": "f_aid", "kind": "F", "fields": {
    "tk": ref("t_aid"),
    "nm": "Outline and display-scale comparison sheet for the owner decision",
    "kd": sym("reference"),
    "rq": refs("q_aid_faithful", "q_aid_useful")}})

R.append({"id": "t_aid", "kind": "T", "fields": {
    "nm": "Build a comparison sheet so the outline and canvas decisions can be made",
    "ow": ref("actor"), "pr": ref("project"), "dp": refs("t_study"), "dc": [], "kn": [],
    "st": sym("active"), "ph": sym("research"),
    "ip": [], "op": refs("f_aid"), "ca": [], "vr": []}})

json.dump({"revision": 3, "records": R, "format": 2},
          open("work/rev3.json", "w", encoding="utf-8"), indent=1)
val = json.loads(subprocess.run([PY, RUNNER, "validate", "state.px/state.px", "--root", "."],
                                capture_output=True, text=True, check=True).stdout)
print("records:", len(R), "| expect:", val["hash"])
