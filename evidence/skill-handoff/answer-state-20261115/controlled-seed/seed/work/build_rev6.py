"""Revision 6 (2026-11-14 continuation): retain the continuation note as a local
source, surface the game-background intake question, and add a new handoff record.
Encodes work/rev6.px; the commit is performed separately with the expected hash."""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
NOTE = "deliverables/continuation-2026-11-14.md"
AT = "2026-11-14"


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
assert cur["revision"] == 5, cur["revision"]
R = cur["records"]
by_id = {r["id"]: r for r in R}
lines = open(NOTE, encoding="utf-8").read().count("\n")

R.append({"id": "s_continuation", "kind": "S", "fields": {
    "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines], "at": AT, "au": sym("local")}})

R.append({"id": "i_backgrounds", "kind": "I", "fields": {
    "pr": ref("project"), "wh": ref("user"), "ky": "target_backgrounds",
    "st": sym("unresolved"), "vl": None,
    "so": refs("s_continuation"),
    "wy": "The predominant level backgrounds of the side-view game are not stated. The "
          "retained comparison sheet showed the navy outline separates the figure on "
          "busy mid-value backgrounds but nearly disappears on dark ones, so the outline "
          "decision depends on this. The light, dark and busy bands used in the "
          "readability criterion are the agent's test set, not the game's backgrounds."}})

by_id["project"]["fields"]["in"].append(ref("i_backgrounds"))

R.append({"id": "handoff_2", "kind": "N", "fields": {
    "wh": ref("actor"),
    "fo": refs("s_continuation", "i_outline", "i_canvas", "i_design_language",
               "i_backgrounds", "i_display_scale", "i_role_diff", "i_engine",
               "x_aid", "x_study"),
    "nx": refs("t_sample"),
    "bl": refs("t_sample", "t_scout", "t_medic", "t_family"),
    "rv": 6}})

json.dump({"revision": 6, "records": R, "format": 2},
          open("work/rev6.json", "w", encoding="utf-8"), indent=1)
subprocess.run([PY, RUNNER, "encode", "work/rev6.json", "--out", "work/rev6.px"], check=True)
print("encoded work/rev6.px with", len(R), "records; note lines:", lines)
