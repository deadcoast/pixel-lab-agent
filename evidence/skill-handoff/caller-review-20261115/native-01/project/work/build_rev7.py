"""Revision 7 (2026-11-15 continuation): retain the new continuation note as a local
source and add a new handoff record pointing at it. No choice, task, criterion or
verdict record is changed. Encodes work/rev7.px; the commit is performed separately
through pixl_commit with the expected revision-6 hash.

Run with: <interpreter> -I work/build_rev7.py  (cwd = consumer root)
"""
import hashlib
import json
import subprocess
import sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
NOTE = "deliverables/continuation-2026-11-15.md"
AT = "2026-11-15"
EXPECT_REVISION = 6
EXPECT_HASH = "b9a66beff93bcc2197a442d1de8ed6d7d9178aacf0c10606512a38e64d78b5b7"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sym(s):
    return {"$symbol": s}


def ref(s):
    return {"$ref": s}


def refs(*a):
    return [ref(x) for x in a]


assert sha("state.px/state.px") == EXPECT_HASH, "state.px/state.px is not the expected revision-6 bytes"
cur = json.loads(subprocess.run([PY, RUNNER, "decode", "state.px/state.px"],
                                capture_output=True, text=True, check=True).stdout)
assert cur["revision"] == EXPECT_REVISION, cur["revision"]
R = cur["records"]
ids = {r["id"] for r in R}
assert "s_continuation_2" not in ids and "handoff_3" not in ids
lines = open(NOTE, encoding="utf-8").read().count("\n")

R.append({"id": "s_continuation_2", "kind": "S", "fields": {
    "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines], "at": AT, "au": sym("local")}})

R.append({"id": "handoff_3", "kind": "N", "fields": {
    "wh": ref("actor"),
    "fo": refs("s_continuation_2", "s_continuation",
               "i_outline", "i_canvas", "i_backgrounds", "i_design_language",
               "i_display_scale", "i_role_diff", "i_palette", "i_engine",
               "x_aid", "x_study"),
    "nx": refs("t_sample"),
    "bl": refs("t_sample", "t_scout", "t_medic", "t_family"),
    "rv": 7}})

json.dump({"revision": 7, "records": R, "format": 2},
          open("work/rev7.json", "w", encoding="utf-8"), indent=1)
subprocess.run([PY, RUNNER, "encode", "work/rev7.json", "--out", "work/rev7.px"], check=True)
print("encoded work/rev7.px with", len(R), "records; note lines:", lines, "; note sha256:", sha(NOTE))
