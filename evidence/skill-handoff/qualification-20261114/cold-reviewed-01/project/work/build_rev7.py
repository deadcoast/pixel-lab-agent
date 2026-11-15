"""Revision 7 (2026-11-14 corrected continuation, after CALLER-REVIEW.md):
- retain the caller review and the corrected continuation note as local sources;
- reword q_palette from an exclusive allowed-colour rule into a palette account;
- reword q_canvas / q_outline to refer to the candidate's contract instead of
  "confirmed" choices (sample work may test proposed/observed choices);
- correct the i_palette rationale so exclusivity is not implied;
- add handoff_3 pointing at the corrected note.
Encodes work/rev7.px; the commit is performed separately with the expected hash.
Earlier records, notes and handoffs are preserved."""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
NOTE = "deliverables/continuation-2026-11-14-corrected.md"
REVIEW = "CALLER-REVIEW.md"
AT = "2026-11-14"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sym(s):
    return {"$symbol": s}


def ref(s):
    return {"$ref": s}


def refs(*a):
    return [ref(x) for x in a]


def nlines(p):
    return open(p, encoding="utf-8").read().count("\n")


cur = json.loads(subprocess.run([PY, RUNNER, "decode", "state.px/state.px"],
                                capture_output=True, text=True, check=True).stdout)
assert cur["revision"] == 6, cur["revision"]
R = cur["records"]
by_id = {r["id"]: r for r in R}

R.append({"id": "s_caller_review", "kind": "S", "fields": {
    "ur": REVIEW, "dg": sha(REVIEW), "ln": [1, nlines(REVIEW)], "at": AT, "au": sym("local")}})
R.append({"id": "s_continuation_2", "kind": "S", "fields": {
    "ur": NOTE, "dg": sha(NOTE), "ln": [1, nlines(NOTE)], "at": AT, "au": sym("local")}})

q = by_id["q_palette"]["fields"]
q["nm"] = "palette account"
q["ck"] = (
    "A retained local measurement lists every visible colour of the candidate with its "
    "pixel count and its role against the reference colours (teal body #56B5BC, cream "
    "detail #F4DDA2, navy outline #25354A), and names any colour not present in the "
    "references so the visual style review can judge it. This is an account, not an "
    "allowed-colour list: no fixed palette has been imposed by the owner, and a colour "
    "outside the reference set is reported, not failed.")
q["so"] = refs("s_refobs", "s_caller_review")

q = by_id["q_canvas"]["fields"]
q["ck"] = (
    "The candidate file matches the canvas size named in its contract exactly and, when "
    "that contract's alpha policy is binary, contains zero fractional-alpha pixels. The "
    "contract's linked choices carry their own recorded status (observed, proposed or "
    "confirmed); this check does not establish owner adoption.")
q["so"] = refs("s_brief", "s_caller_review")

q = by_id["q_outline"]["fields"]
q["ck"] = (
    "The candidate applies the outline treatment named in its contract consistently on "
    "every contour and on the interior landmarks that treatment is responsible for, "
    "inspected at native scale and at integer zoom.")
q["so"] = refs("s_refobs", "s_caller_review")

i = by_id["i_palette"]["fields"]
i["wy"] = (
    "Measured from the references: teal body, cream eyes, and navy present only in "
    "reference.png. Observed, not agreed: the brief imposes no fixed palette, so these are "
    "the working colours a sample trial may use, not an exclusive allowed-colour list. "
    "Whether #25354A belongs among the working colours follows the outline decision. Owner "
    "adoption of a colour list, and any exclusivity rule, are separate instructions the "
    "owner has not given; the outline answer does not supply them.")
i["so"] = refs("s_refobs", "s_ref_a", "s_ref_b", "s_caller_review")

R.append({"id": "handoff_3", "kind": "N", "fields": {
    "wh": ref("actor"),
    "fo": refs("s_caller_review", "s_continuation_2", "s_continuation",
               "q_palette", "q_canvas", "q_outline", "i_palette",
               "i_outline", "i_canvas", "i_design_language", "i_backgrounds",
               "i_display_scale", "i_role_diff", "i_alpha", "i_sampling", "i_engine",
               "x_aid", "x_study"),
    "nx": refs("t_sample"),
    "bl": refs("t_sample", "t_scout", "t_medic", "t_family"),
    "rv": 7}})

json.dump({"revision": 7, "records": R, "format": 2},
          open("work/rev7.json", "w", encoding="utf-8"), indent=1)
subprocess.run([PY, RUNNER, "encode", "work/rev7.json", "--out", "work/rev7.px"], check=True)
print("encoded work/rev7.px with", len(R), "records")
