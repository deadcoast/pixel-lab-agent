"""Revision 8 (2026-11-15 correction after caller review): rekey i_lighting from the
contract field name `li` to `lighting` so it no longer value-pins C.li (which the kit
defines as lighting AND aesthetic intent), rewrite its rationale accordingly, retain the
correction note as a source, and add a new handoff record. Value, status and sources of
i_lighting are unchanged; no other record changes. Encodes work/rev8.px; the commit is
performed separately with the expected hash.

Run from the consumer root with the selected interpreter:
  python -I work/build_rev8.py
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
NOTE = "deliverables/continuation-2026-11-15b.md"
AT = "2026-11-15"


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
assert cur["revision"] == 7, cur["revision"]
R = cur["records"]
by_id = {r["id"]: r for r in R}
for new_id in ("s_continuation_3", "handoff_4"):
    assert new_id not in by_id, new_id

light = by_id["i_lighting"]["fields"]
assert light["ky"] == "li", light["ky"]
assert light["st"] == sym("observed"), light["st"]
light["ky"] = "lighting"
light["wy"] = (
    "Measured from the references: three flat colours in reference.png and two in "
    "reference-b.png, each a single flat value with no ramp, no anti-aliasing and no "
    "directional shading. This observation supplies the lighting component of the sample "
    "contract's li field, which the kit defines as lighting and aesthetic intent; li is "
    "composed at contract time from this choice, the design-language proposal and the "
    "outline answer. Keyed `lighting` rather than `li` so linking it through C.ch does not "
    "pin the whole intent string to the lighting phrase (corrected from revision 7). "
    "Observed from the source art; not confirmed as this project's output policy.")

lines = open(NOTE, encoding="utf-8").read().count("\n")
R.append({"id": "s_continuation_3", "kind": "S", "fields": {
    "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines], "at": AT, "au": sym("local")}})

R.append({"id": "handoff_4", "kind": "N", "fields": {
    "wh": ref("actor"),
    "fo": refs("s_continuation_3", "s_continuation_2", "i_outline", "i_canvas",
               "i_backgrounds", "i_design_language", "i_lighting", "i_animation",
               "i_display_scale", "i_role_diff", "i_palette", "i_engine",
               "x_aid", "x_study"),
    "nx": refs("t_sample"),
    "bl": refs("t_sample", "t_scout", "t_medic", "t_family"),
    "rv": 8}})

json.dump({"revision": 8, "records": R, "format": 2},
          open("work/rev8.json", "w", encoding="utf-8"), indent=1)
subprocess.run([PY, RUNNER, "encode", "work/rev8.json", "--out", "work/rev8.px"], check=True)
print("encoded work/rev8.px with", len(R), "records; note lines:", lines)
