"""Revision 4: retain the decision-aid candidate, its evidence, verdicts and a handoff."""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = ".agents/skills/pixl-kit/scripts/pixl.py"

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def sym(s):
    return {"$symbol": s}

def ref(s):
    return {"$ref": s}

def refs(*a):
    return [ref(x) for x in a]

cur = json.loads(subprocess.run([PY, RUNNER, "decode", "state.px/state.px"],
                                capture_output=True, text=True, check=True).stdout)
R = cur["records"]
by_id = {r["id"]: r for r in R}
AT = "2026-09-14"

R.append({"id": "x_aid", "kind": "X", "fields": {
    "nm": "Outline and display-scale comparison sheet",
    "ur": "deliverables/outline-scale-comparison.png",
    "dg": sha("deliverables/outline-scale-comparison.png"),
    "kd": sym("reference"), "of": ref("f_aid")}})

# Publish the candidate first so its record hash exists for the evidence bindings.
json.dump({"revision": 4, "records": R, "format": 2},
          open("work/rev4a.json", "w", encoding="utf-8"), indent=1)
subprocess.run([PY, RUNNER, "encode", "work/rev4a.json", "--out", "work/rev4a.px"], check=True)
val = json.loads(subprocess.run([PY, RUNNER, "validate", "state.px/state.px", "--root", "."],
                                capture_output=True, text=True, check=True).stdout)
subprocess.run([PY, RUNNER, "commit", "state.px", "work/rev4a.px",
                "--expect", val["hash"], "--root", "."], check=True)

# ---- revision 5: evidence, verdicts, completion, handoff ----
cur = json.loads(subprocess.run([PY, RUNNER, "decode", "state.px/state.px"],
                                capture_output=True, text=True, check=True).stdout)
R = cur["records"]
by_id = {r["id"]: r for r in R}
val = json.loads(subprocess.run([PY, RUNNER, "validate", "state.px/state.px", "--root", "."],
                                capture_output=True, text=True, check=True).stdout)
H = val["record_hashes"]

# Semantic closure of x_aid: X -> F -> Q -> A/S
scope_aid = ("x_aid", "f_aid", "q_aid_faithful", "q_aid_useful",
             "user", "s_methods", "s_refobs")

def bindings(*ids):
    return [{"rf": ref(i), "dg": H[i]} for i in ids]

R.append({"id": "e_aid_faithful", "kind": "E", "fields": {
    "nm": "Local nearest-neighbour fidelity check of the comparison sheet",
    "ur": "evidence/aid-faithfulness.json", "dg": sha("evidence/aid-faithfulness.json"),
    "rs": sym("pass"), "md": sym("local"), "at": AT, "bs": bindings(*scope_aid)}})

R.append({"id": "e_aid_useful", "kind": "E", "fields": {
    "nm": "Visual review of the comparison sheet and resulting decision brief",
    "ur": "deliverables/outline-decision-brief.md",
    "dg": sha("deliverables/outline-decision-brief.md"),
    "rs": sym("pass"), "md": sym("visual"), "at": AT, "bs": bindings(*scope_aid)}})

R.append({"id": "v_aid_faithful", "kind": "V", "fields": {
    "tk": ref("t_aid"), "rq": ref("q_aid_faithful"), "xr": ref("x_aid"),
    "st": sym("pass"), "wh": ref("actor"), "at": AT,
    "wy": "All 36 panels were checked block by block: 14,040 opaque source pixels each "
          "enlarge into a uniform z-by-z block of the identical colour, with zero "
          "non-uniform blocks and zero colours absent from the source files. This is "
          "enlargement fidelity only and carries no artistic weight.",
    "ev": refs("e_aid_faithful")}})

R.append({"id": "v_aid_useful", "kind": "V", "fields": {
    "tk": ref("t_aid"), "rq": ref("q_aid_useful"), "xr": ref("x_aid"),
    "st": sym("pass"), "wh": ref("actor"), "at": AT,
    "wy": "The sheet was viewed in this session. It shows both treatments at all six "
          "sampled scales over light, dark and busy backgrounds, and it surfaced a "
          "finding neither reference shows alone: the navy outline loses the figure "
          "against dark backgrounds but is what separates it against busy ones. Stated "
          "limit: at 1x the two treatments are not reliably distinguishable, so the "
          "sheet supports the decision from 3x upward.",
    "ev": refs("e_aid_useful")}})

t = by_id["t_aid"]["fields"]
t["st"] = sym("done")
t["ca"] = refs("x_aid")
t["vr"] = refs("v_aid_faithful", "v_aid_useful")

R.append({"id": "handoff", "kind": "N", "fields": {
    "wh": ref("actor"),
    "fo": refs("i_outline", "i_canvas", "i_display_scale", "i_role_diff", "i_engine",
               "i_design_language", "x_aid", "x_study"),
    "nx": refs("t_sample"),
    "bl": refs("t_sample", "t_scout", "t_medic", "t_family"),
    "rv": 5}})

json.dump({"revision": 5, "records": R, "format": 2},
          open("work/rev5.json", "w", encoding="utf-8"), indent=1)
subprocess.run([PY, RUNNER, "encode", "work/rev5.json", "--out", "work/rev5.px"], check=True)
subprocess.run([PY, RUNNER, "commit", "state.px", "work/rev5.px",
                "--expect", val["hash"], "--root", "."], check=True)
print("done")
