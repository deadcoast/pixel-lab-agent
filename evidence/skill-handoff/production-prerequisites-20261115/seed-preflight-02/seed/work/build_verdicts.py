"""Revision 2: retain evidence receipts and verdicts for the research task."""
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
val = json.loads(subprocess.run([PY, RUNNER, "validate", "state.px/state.px", "--root", "."],
                                capture_output=True, text=True, check=True).stdout)
H = val["record_hashes"]
R = cur["records"]
by_id = {r["id"]: r for r in R}

AT = "2026-09-14"

# Bindings cover the candidate's semantic closure (X -> F -> Q -> A/S) and the
# criterion's own closure. Hashes come from validate, not from guesswork.
def bindings(*ids):
    return [{"rf": ref(i), "dg": H[i]} for i in ids]

scope_common = ("x_study", "f_study", "q_study_complete", "q_study_seen",
                "user", "s_brief", "s_refobs")

R.append({"id": "e_study_complete", "kind": "E", "fields": {
    "nm": "Local completeness check of the reference study",
    "ur": "evidence/study-completeness.json",
    "dg": sha("evidence/study-completeness.json"),
    "rs": sym("pass"), "md": sym("local"), "at": AT,
    "bs": bindings(*scope_common),
}})

R.append({"id": "e_study_seen", "kind": "E", "fields": {
    "nm": "Visual inspection of both references at native and 12x integer scale",
    "ur": "evidence/reference-visual-inspection.md",
    "dg": sha("evidence/reference-visual-inspection.md"),
    "rs": sym("pass"), "md": sym("visual"), "at": AT,
    "bs": bindings(*scope_common),
}})

R.append({"id": "v_study_complete", "kind": "V", "fields": {
    "tk": ref("t_study"), "rq": ref("q_study_complete"), "xr": ref("x_study"),
    "st": sym("pass"), "wh": ref("actor"), "at": AT,
    "wy": "Every declared completeness check passed when run against the retained study: "
          "both reference hashes, the exact 180-pixel difference and its single "
          "colour-substitution nature, and the unresolved projection, role, scale and "
          "animation questions are all stated. This is a textual check and carries no "
          "artistic weight.",
    "ev": refs("e_study_complete"),
}})

R.append({"id": "v_study_seen", "kind": "V", "fields": {
    "tk": ref("t_study"), "rq": ref("q_study_seen"), "xr": ref("x_study"),
    "st": sym("pass"), "wh": ref("actor"), "at": AT,
    "wy": "Both references were opened at native 32x32 and at 12x nearest-neighbour "
          "enlargement in this session. At native scale the outline difference was not "
          "reliably judgeable; the enlargement is what made it legible. What was seen "
          "matches the study, including that the navy in reference.png also carries the "
          "shoulder bar, base bar and solid stalks, so the unoutlined variant loses "
          "those landmarks and not merely the contour.",
    "ev": refs("e_study_seen"),
}})

t = by_id["t_study"]["fields"]
t["st"] = sym("done")
t["vr"] = refs("v_study_complete", "v_study_seen")

json.dump({"revision": 2, "records": R, "format": 2},
          open("work/rev2.json", "w", encoding="utf-8"), indent=1)
print("records:", len(R), "| expect hash:", val["hash"])
