"""Revision 9 (2026-11-15 c): apply sources/controlled-evaluation-answers.md within its
stated scope (representative sample only; self-declared simulated, not owner preference).

- S s_eval_answers for the input; S s_continuation_4 for the new note; project.sc + input.
- i_outline conflict -> proposed (outlined as reference.png, alternatives kept in wy).
- i_canvas unresolved -> proposed [32,32].
- i_palette stays observed, same value; so + input; wy rewritten (correction 5 coupling).
- i_view / i_sampling / i_alpha: vl re-encoded as symbols (correction 6); nothing else.
- C c_sample; f_sample.ct = c_sample; f_sample.rq -> sample-scoped criteria (correction 4).
- Q q_sample_canvas / q_sample_palette / q_sample_outline / q_sample_readability.
- N handoff_5 rv 9.
No X, V, E or D record is created or changed. Encodes work/rev9.px; the commit is
performed separately with the expected revision-8 hash.

Run from the consumer root with the selected interpreter:
  python -I work/build_rev9.py
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
NOTE = "deliverables/continuation-2026-11-15c.md"
ANSWERS = "sources/controlled-evaluation-answers.md"
ANSWERS_SHA = "52f68a3242dd72ab0d2bd8315c605160f5e6b76b626164f28a949d1563f30f94"
AT = "2026-11-15"
PALETTE = ["#56B5BC", "#F4DDA2", "#25354A"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def lines(p):
    return open(p, "rb").read().count(b"\n")


def sym(s):
    return {"$symbol": s}


def ref(s):
    return {"$ref": s}


def refs(*a):
    return [ref(x) for x in a]


cur = json.loads(subprocess.run([PY, RUNNER, "decode", "state.px/state.px"],
                                capture_output=True, text=True, check=True).stdout)
assert cur["revision"] == 8, cur["revision"]
assert cur["format"] == 2
R = cur["records"]
by_id = {r["id"]: r for r in R}
assert len(R) == 63, len(R)
for new_id in ("s_eval_answers", "s_continuation_4", "c_sample", "q_sample_canvas",
               "q_sample_palette", "q_sample_outline", "q_sample_readability", "handoff_5"):
    assert new_id not in by_id, new_id
assert sha(ANSWERS) == ANSWERS_SHA, sha(ANSWERS)

# --- sources -------------------------------------------------------------------------
R.append({"id": "s_eval_answers", "kind": "S", "fields": {
    "ur": ANSWERS, "dg": ANSWERS_SHA, "ln": [1, lines(ANSWERS)], "at": AT, "au": sym("local")}})
R.append({"id": "s_continuation_4", "kind": "S", "fields": {
    "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines(NOTE)], "at": AT, "au": sym("local")}})

proj = by_id["project"]["fields"]
assert ref("s_eval_answers") not in proj["sc"]
proj["sc"].append(ref("s_eval_answers"))

# --- i_outline: conflict -> proposed (sample scope) ------------------------------------
o = by_id["i_outline"]["fields"]
assert o["st"] == sym("conflict") and o["ky"] == "edge_treatment"
old_alts = o["vl"]
assert isinstance(old_alts, list) and len(old_alts) == 2
o["st"] = sym("proposed")
o["vl"] = ("outlined as reference.png: flat #25354A contour of the references' weight "
           "(2 px measured) fully enclosing the body, with the same navy forming the "
           "shoulder bar, base bar and solid top stalks")
o["so"].append(ref("s_eval_answers"))
o["wy"] = (
    "Adopted for the representative sample only, from sources/controlled-evaluation-answers.md, "
    "which selects the outlined treatment of reference.png for the sample and declares itself a "
    "simulated answer for this isolated evaluation, not a real owner preference or human "
    "acceptance. Recorded as proposed, not confirmed: the runtime admits a proposed choice into "
    "a sample contract but requires confirmation plus a decision record before production or "
    "delivery, which is exactly the gate a non-owner answer must leave in place. The brief's "
    "statement that the references disagree still stands for the family. Alternatives "
    f"preserved: (a) {old_alts[0]} [adopted for the sample]; (b) {old_alts[1]} [not adopted; "
    "would make the palette two colours and require the shoulder, base and stalk landmarks "
    "that the navy carries to be re-authored in a named way or dropped deliberately]. "
    "Measured: the two files differ in exactly 180 pixels and every difference is #25354A "
    "becoming #56B5BC, so the outline is load-bearing rather than trim. The bundled "
    "edge-rhythm method states contour style is authored intent; the owner's confirmation of "
    "either treatment for the family is still needed.")

# --- i_canvas: unresolved -> proposed [32,32] (sample scope) ----------------------------
c = by_id["i_canvas"]["fields"]
assert c["st"] == sym("unresolved") and c["vl"] is None and c["ky"] == "px"
c["st"] = sym("proposed")
c["vl"] = [32, 32]
c["so"].append(ref("s_eval_answers"))
c["wy"] = (
    "Adopted for the representative sample only, from sources/controlled-evaluation-answers.md "
    "(32 x 32 for the sample; a self-declared simulated answer, not an owner preference). The "
    "brief explicitly states the final canvas size is not chosen, and the input does not claim "
    "to change that, so this is proposed, not confirmed: it lets C.px be written for the sample "
    "while production and delivery stay gated on the owner's confirmed final canvas. "
    "Observation retained: both references are 32x32 carrying an 18x25 figure. Alternative "
    "preserved: another owner-named size; the study notes that with a 2 px outline a materially "
    "smaller canvas leaves little interior for the scout and medic to differ in, and a "
    "materially larger one makes the 2 px contour read thinner than the references' weight.")

# --- i_palette: stays observed; sources + rationale only --------------------------------
p = by_id["i_palette"]["fields"]
assert p["st"] == sym("observed") and p["vl"] == PALETTE and p["ky"] == "pl"
p["so"].append(ref("s_eval_answers"))
p["wy"] = (
    "Measured from the references: teal body, cream eyes, and navy present only in "
    "reference.png. Status stays observed: the three colours are measurements, and the "
    "sample-scoped outline answer (sources/controlled-evaluation-answers.md) settles only that "
    "the navy is present in the sample, so the sample contract adopts exactly these three as "
    "C.pl without proposing or confirming a project palette. Not confirmed, deliberately: "
    "confirmation would adopt the exclusive membership rule for production, and the "
    "role-differentiation device (i_role_diff, unresolved) may need an accent hue. Confirm the "
    "palette only together with that device, or as a base palette with one reserved accent slot.")

# --- correction 6: symbol-valued choices pinned by the contract -------------------------
for cid, key, val in (("i_view", "vw", "side"), ("i_sampling", "sa", "nearest"),
                      ("i_alpha", "al", "binary")):
    f = by_id[cid]["fields"]
    assert f["ky"] == key and f["vl"] == val, (cid, f["vl"])
    f["vl"] = sym(val)

# --- contract -----------------------------------------------------------------------
LI = (
    "Lighting (observed from both references): flat colour, no directional light, no shading "
    "ramps. Design language (proposed, owner may override): no anti-aliasing, binary alpha and "
    "the blocky low-detail construction of the references carried into a genuinely side-view "
    "figure; the references' front-facing symmetric shape is a style swatch, not the character "
    "design. Outline (adopted for the sample from the controlled-evaluation answers, not an "
    "owner confirmation): outlined as reference.png, a flat #25354A contour of the references' "
    "weight (2 px measured) fully enclosing the body, with the same navy forming the shoulder "
    "bar, the base bar and the solid top stalks. Identity landmarks that the sample readability "
    "criterion names and that must stay separable in profile: the solid navy top-stalk "
    "silhouette (the references' two stalks adapted to side view), at least one cream eye, the "
    "navy shoulder bar and the navy base bar. Pose (scoped specialist choice for the sample): "
    "one idle pose facing right; the engine can mirror it.")
R.append({"id": "c_sample", "kind": "C", "fields": {
    "nm": ("Representative sample contract: side-view scout, single idle pose, 32 x 32, "
           "outlined as reference.png (sample-scoped; adopts proposed and observed choices, "
           "confirms none)"),
    "px": [32, 32], "pl": list(PALETTE), "vw": sym("side"), "sa": sym("nearest"),
    "al": sym("binary"), "li": LI,
    "ch": refs("i_canvas", "i_palette", "i_view", "i_sampling", "i_alpha", "i_lighting",
               "i_outline", "i_design_language")}})

# --- sample-scoped criteria (correction 4, delegated path) ----------------------------
def Q(id_, nm, dm, md, ck, *so):
    R.append({"id": id_, "kind": "Q", "fields": {
        "nm": nm, "dm": sym(dm), "md": sym(md), "ck": ck, "wh": ref("actor"), "so": refs(*so)}})

Q("q_sample_canvas", "sample canvas and alpha", "mechanical", "local",
  "The candidate file is exactly 32 x 32 pixels, the canvas of the sample contract c_sample "
  "(adopted for the sample from sources/controlled-evaluation-answers.md; not a confirmed "
  "final canvas), and contains zero fractional-alpha pixels under that contract's binary "
  "alpha policy.", "s_eval_answers", "s_refobs")
Q("q_sample_palette", "sample palette membership", "mechanical", "local",
  "Every visible pixel of the candidate is one of the three colours of the sample contract "
  "c_sample, #56B5BC, #F4DDA2 and #25354A (the measured reference palette, adopted for the "
  "sample because the sample outline treatment includes the navy), with no colours outside "
  "them. This exclusivity is a sample-scoped derived rule; it does not confirm the project "
  "palette, which stays coupled to the role-differentiation device.", "s_eval_answers", "s_refobs")
Q("q_sample_outline", "sample outline treatment applied", "visual", "visual",
  "The candidate applies the outlined treatment named in the sample contract c_sample, that of "
  "reference.png: a flat #25354A contour of the references' weight (2 px measured) fully "
  "encloses the body on every exterior contour, and the same navy forms the interior landmarks "
  "that treatment is responsible for (the shoulder bar, the base bar and the solid top stalks), "
  "inspected at native scale and at integer zoom.", "s_eval_answers", "s_refobs", "s_ref_a")
Q("q_sample_readability", "sample side-view readability", "visual", "visual",
  "At native scale and at the target integer zoom, on light, dark and busy test backgrounds, "
  "the figure reads as a side-view character with an unambiguous facing direction, and the "
  "identity landmarks named in the sample contract c_sample (the solid navy top-stalk "
  "silhouette, at least one cream eye, the navy shoulder bar and the navy base bar) remain "
  "separable. The target integer zoom comes from i_display_scale; until it is supplied, the "
  "review states the zooms actually used.", "s_methods", "s_refobs", "s_brief")

fs = by_id["f_sample"]["fields"]
assert "ct" not in fs
assert fs["rq"] == refs("q_canvas", "q_palette", "q_outline", "q_readability", "q_style_match")
fs["ct"] = ref("c_sample")
fs["rq"] = refs("q_sample_canvas", "q_sample_palette", "q_sample_outline",
                "q_sample_readability", "q_style_match")

# --- handoff -------------------------------------------------------------------------
R.append({"id": "handoff_5", "kind": "N", "fields": {
    "wh": ref("actor"),
    "fo": refs("s_continuation_4", "s_eval_answers", "c_sample", "f_sample", "i_outline",
               "i_canvas", "i_palette", "i_design_language", "i_lighting", "i_backgrounds",
               "i_display_scale", "i_role_diff", "i_animation", "i_engine", "x_aid", "x_study"),
    "nx": refs("t_sample"),
    "bl": refs("t_scout", "t_medic", "t_family"),
    "rv": 9}})

assert len(R) == 71, len(R)
json.dump({"revision": 9, "records": R, "format": 2},
          open("work/rev9.json", "w", encoding="utf-8"), indent=1)
subprocess.run([PY, RUNNER, "encode", "work/rev9.json", "--out", "work/rev9.px"], check=True)
print("encoded work/rev9.px with", len(R), "records; note lines:", lines(NOTE),
      "note sha:", sha(NOTE))
