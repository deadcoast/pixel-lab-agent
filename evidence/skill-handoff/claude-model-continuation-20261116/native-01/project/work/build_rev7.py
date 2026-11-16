"""Revision 7 (2026-11-15 continuation): retain the new continuation note as a local
source, add the lighting (observed) and animation (unresolved) intake choices that the
sources support, and add a new handoff record. Encodes work/rev7.px; the commit is
performed separately with the expected hash. No status change, no acceptance change.

Run from the consumer root with the selected interpreter:
  python -I work/build_rev7.py
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
NOTE = "deliverables/continuation-2026-11-15.md"
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
assert cur["revision"] == 6, cur["revision"]
R = cur["records"]
by_id = {r["id"]: r for r in R}
for new_id in ("s_continuation_2", "i_lighting", "i_animation", "handoff_3"):
    assert new_id not in by_id, new_id
lines = open(NOTE, encoding="utf-8").read().count("\n")

R.append({"id": "s_continuation_2", "kind": "S", "fields": {
    "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines], "at": AT, "au": sym("local")}})

R.append({"id": "i_lighting", "kind": "I", "fields": {
    "pr": ref("project"), "wh": ref("user"), "ky": "li",
    "st": sym("observed"),
    "vl": "flat (no directional light, no shading ramps)",
    "so": refs("s_refobs", "s_ref_a", "s_ref_b"),
    "wy": "Measured from the references: three flat colours in reference.png and two in "
          "reference-b.png, each a single flat value with no ramp, no anti-aliasing and no "
          "directional shading. Recorded because a concrete raster contract requires a "
          "lighting field (C.li) and no intake choice held it, so the sample contract could "
          "not be written. Observed from the source art; not confirmed as this project's "
          "output policy."}})

R.append({"id": "i_animation", "kind": "I", "fields": {
    "pr": ref("project"), "wh": ref("user"), "ky": "animation",
    "st": sym("unresolved"), "vl": None,
    "so": refs("s_brief", "s_refobs"),
    "wy": "The brief names a character family but states no poses, cycles, directions or "
          "timing, and neither reference shows motion; both retained sources name this gap. "
          "The saved plan treats the sample, scout and medic as single static side-view "
          "sprites. Not needed for the representative sample. Before scout/medic production "
          "it decides whether each output is one sprite or an animation set, which changes "
          "the planned output kinds and the PixelLab operation to use."}})

by_id["project"]["fields"]["in"].extend(refs("i_lighting", "i_animation"))

R.append({"id": "handoff_3", "kind": "N", "fields": {
    "wh": ref("actor"),
    "fo": refs("s_continuation_2", "i_outline", "i_canvas", "i_backgrounds",
               "i_design_language", "i_lighting", "i_animation", "i_display_scale",
               "i_role_diff", "i_palette", "i_engine", "x_aid", "x_study"),
    "nx": refs("t_sample"),
    "bl": refs("t_sample", "t_scout", "t_medic", "t_family"),
    "rv": 7}})

json.dump({"revision": 7, "records": R, "format": 2},
          open("work/rev7.json", "w", encoding="utf-8"), indent=1)
subprocess.run([PY, RUNNER, "encode", "work/rev7.json", "--out", "work/rev7.px"], check=True)
print("encoded work/rev7.px with", len(R), "records; note lines:", lines)
