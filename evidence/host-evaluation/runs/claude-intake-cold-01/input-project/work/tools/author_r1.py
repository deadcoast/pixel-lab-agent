"""Author PX2 revision 1: sources, intake choices, knowledge, plan, criteria.

Writes work/state/candidate-r1.json. Commits are a separate explicit step.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "work" / "state"
DATE = "2026-09-11"


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def lines(rel):
    return len((ROOT / rel).read_text(encoding="utf-8").splitlines())


def ref(i):
    return {"$ref": i}


def sym(s):
    return {"$symbol": s}


def rec(id_, kind, **fields):
    return {"id": id_, "kind": kind, "fields": fields}


def source(id_, rel, au, ranged):
    return rec(id_, "S", ur=rel, dg=sha(rel), ln=[1, lines(rel)] if ranged else [],
               at=DATE, au=sym(au))


records = [
    rec("actor", "A", nm="PIXL", rl=sym("agent")),
    rec("user", "A", nm="Project owner", rl=sym("user")),

    # --- sources -----------------------------------------------------------
    source("brief", "work/sources/brief.md", "local", True),
    source("ref_a", "reference.png", "local", False),
    source("ref_b", "reference-b.png", "local", False),
    source("measure", "work/study/measurement.json", "local", False),
    source("kmethods", "work/sources/knowledge-methods.json", "study", False),

    # --- knowledge retrieved for this decision -----------------------------
    rec("k_silhouette", "K",
        nm="Evaluate identity using silhouette and target backgrounds",
        ap=[sym("characters_25d939ff"), sym("inventory_icons_f7812ea4"),
            sym("interactive_props_25a44283")],
        op=["Render a flat opaque mask before detailing.",
            "Inspect major proportions, negative spaces and landmark separation at native logical scale.",
            "Compare the colored asset on representative light, dark and busy backgrounds."],
        ck=["Named identity landmarks remain visible at the target size.",
            "Required gaps stay open and interactive forms separate from their surroundings."],
        so=[ref("kmethods")]),
    rec("k_edge", "K",
        nm="Audit stair-step runs without imposing one contour style",
        ap=[sym("clean_linework_08dea3fe"), sym("small_curved_forms_e37a2e1c"),
            sym("hard_silhouettes_99485584")],
        op=["Trace boundary runs and highlight sudden run-length changes.",
            "Regularize only contours intended to read as smooth.",
            "Preserve corners, damage and organic asymmetry identified in the brief."],
        ck=["A supplied straight diagonal retains its declared repeating step pattern.",
            "No protected corner changes during cleanup."],
        so=[ref("kmethods")]),

    # --- intake choices ----------------------------------------------------
    rec("ch_roles", "I", pr=ref("project"), wh=ref("user"), ky="family_roles",
        st=sym("confirmed"), vl=["scout", "medic"], so=[ref("brief")],
        wy="The user named a scout and a medic as the two members of this family."),
    rec("ch_view", "I", pr=ref("project"), wh=ref("user"), ky="vw",
        st=sym("confirmed"), vl=sym("side"), so=[ref("brief")],
        wy="The user stated a side-view game. The references are front-facing and "
           "therefore do not establish the production view themselves."),
    rec("ch_edges", "I", pr=ref("project"), wh=ref("user"), ky="edge_treatment",
        st=sym("conflict"),
        vl=["continuous 2px dark outline in #25354A, as supplied in reference.png",
            "no outline; flat single-color silhouette, as supplied in reference-b.png"],
        so=[ref("brief"), ref("ref_a"), ref("ref_b"), ref("measure")],
        wy="The user named this disagreement explicitly. Measured: the two files share "
           "an identical 390-cell silhouette and differ in exactly 180 pixels, every one "
           "of them #25354A in reference.png against #56B5BC in reference-b.png. The rim "
           "is a uniform 2 cells deep and spends 46.2% of the character's pixels on its "
           "own edge. A third option, a 1px rim at 92 cells, is offered in the decision "
           "study but has not been put to the user. Unresolved until the user chooses."),
    rec("ch_canvas", "I", pr=ref("project"), wh=ref("user"), ky="px",
        st=sym("unresolved"), vl=None,
        so=[ref("brief"), ref("ref_a"), ref("ref_b")],
        wy="The user stated the final canvas size is not chosen. Both references are "
           "32x32 with an 18x25 occupied area, which is evidence of intent but not a "
           "decision. The choice is coupled to edge_treatment: a 2px rim is not viable "
           "below roughly 48px of canvas for two distinguishable characters."),
    rec("ch_palette", "I", pr=ref("project"), wh=ref("actor"), ky="pl",
        st=sym("observed"),
        vl=["#56B5BC", "#25354A", "#F4DDA2"],
        so=[ref("ref_a"), ref("ref_b"), ref("measure")],
        wy="Measured across both references: teal fill, navy rim, cream marks. "
           "Observation only. Whether these are the final character colors or "
           "placeholder colors has not been stated, and #25354A exists only in the "
           "outline treatment that is still in conflict."),
    rec("ch_alpha", "I", pr=ref("project"), wh=ref("actor"), ky="al",
        st=sym("observed"), vl=sym("binary"),
        so=[ref("ref_a"), ref("ref_b"), ref("measure")],
        wy="Measured: zero fractional-alpha pixels in either reference. Observation "
           "from two placeholder files, not a stated compositing policy."),
    rec("ch_sampling", "I", pr=ref("project"), wh=ref("actor"), ky="sa",
        st=sym("proposed"), vl=sym("nearest"), so=[],
        wy="Proposed for a side-view pixel game whose references are hard-edged and "
           "unantialiased. Not confirmed; it depends on the unresolved display_scale "
           "and engine choices."),
    rec("ch_scale", "I", pr=ref("project"), wh=ref("user"), ky="display_scale",
        st=sym("unresolved"), vl=None, so=[ref("brief")],
        wy="Not in the brief. The decision study shows the three outline treatments are "
           "nearly indistinguishable at 1x and clearly different at 8x, so this choice "
           "materially affects the edge_treatment decision."),
    rec("ch_engine", "I", pr=ref("project"), wh=ref("user"), ky="engine",
        st=sym("unresolved"), vl=None, so=[ref("brief")],
        wy="No target engine or import route was stated. Engine acceptance for the "
           "family cannot be planned concretely or verified until one exists."),
    rec("ch_light", "I", pr=ref("project"), wh=ref("user"), ky="li",
        st=sym("unresolved"), vl=None, so=[ref("ref_a"), ref("ref_b")],
        wy="Both references are flat fills with no shading, so they establish no light "
           "direction. Side-view characters normally need one stated."),

    # --- acceptance criteria ------------------------------------------------
    rec("q_study_repro", "Q", nm="study reproducible", dm=sym("mechanical"),
        md=sym("local"), wh=ref("actor"), so=[ref("brief"), ref("measure")],
        ck="Every measurement in the study is recomputed from reference.png and "
           "reference-b.png by work/tools/edge_study.py and matches the recorded "
           "sha256 digests, pixel counts and outline depth profile."),
    rec("q_study_decidable", "Q", nm="study decidable", dm=sym("visual"),
        md=sym("visual"), wh=ref("actor"), so=[ref("brief"), ref("kmethods")],
        ck="Each candidate outline treatment is shown at native scale and integer zoom "
           "on light, dark and busy grounds, and the study states which cells are "
           "weakest for each treatment, so the owner can settle edge_treatment by "
           "looking at it."),
    rec("q_sample_contract", "Q", nm="sample matches contract", dm=sym("mechanical"),
        md=sym("local"), wh=ref("user"), so=[ref("brief")],
        ck="The sprite file matches the confirmed canvas size, the approved palette and "
           "the confirmed alpha policy, with no colors outside the palette."),
    rec("q_sample_readable", "Q", nm="sample readable", dm=sym("visual"),
        md=sym("visual"), wh=ref("user"), so=[ref("brief"), ref("kmethods")],
        ck="At the intended display scale the scout reads as a side-view character: "
           "head, torso, leading leg and its role-identifying gear separate from each "
           "other and from light, dark and busy backgrounds."),
    rec("q_sample_import", "Q", nm="engine import", dm=sym("engine"), md=sym("live"),
        wh=ref("user"), so=[ref("brief")],
        ck="The destination engine displays the sprite at the intended sampling and "
           "scale, with the intended pivot and transparency, with no resampling "
           "artifacts or atlas bleed."),
    rec("q_family_continuity", "Q", nm="family continuity", dm=sym("continuity"),
        md=sym("visual"), wh=ref("user"), so=[ref("brief")],
        ck="Viewed side by side at the intended scale, scout and medic share body "
           "volume, head size, ground baseline, outline treatment and palette, so they "
           "read as two members of one family rather than two styles."),
    rec("q_member_distinct", "Q", nm="members distinct", dm=sym("visual"),
        md=sym("visual"), wh=ref("user"), so=[ref("brief")],
        ck="Each member's role is identifiable from its own silhouette and markings at "
           "the intended scale, with the other member absent."),

    # --- planned outputs -----------------------------------------------------
    rec("edge_study", "F", tk=ref("study_edges"),
        nm="Outline treatment and canvas size decision study", kd=sym("report"),
        rq=[ref("q_study_repro"), ref("q_study_decidable")]),
    rec("scout_sample", "F", tk=ref("sample_scout"),
        nm="Representative scout, side view, idle pose", kd=sym("sprite"),
        rq=[ref("q_sample_contract"), ref("q_sample_readable"),
            ref("q_sample_import")]),
    rec("medic_sprite", "F", tk=ref("make_medic"),
        nm="Medic, side view, idle pose, matching the accepted scout", kd=sym("sprite"),
        rq=[ref("q_sample_contract"), ref("q_sample_readable"),
            ref("q_sample_import"), ref("q_member_distinct"),
            ref("q_family_continuity")]),
    rec("family_pack", "F", tk=ref("deliver_family"),
        nm="Scout and medic family delivery package", kd=sym("report"),
        rq=[ref("q_family_continuity"), ref("q_member_distinct"),
            ref("q_sample_import")]),

    # --- candidate ----------------------------------------------------------
    rec("x_study", "X", nm="Outline and canvas decision study",
        ur="work/study/edge-and-canvas-study.md", dg=sha("work/study/edge-and-canvas-study.md"),
        kd=sym("report"), of=ref("edge_study")),

    # --- tasks ---------------------------------------------------------------
    rec("study_edges", "T",
        nm="Measure the reference disagreement and put the outline and canvas choices to the owner",
        ow=ref("actor"), pr=ref("project"), dp=[], dc=[],
        kn=[ref("k_silhouette"), ref("k_edge")], st=sym("active"), ph=sym("research"),
        ip=[], op=[ref("edge_study")], ca=[ref("x_study")], vr=[]),
    rec("sample_scout", "T",
        nm="Prove the style on one scout pose before producing the family",
        ow=ref("actor"), pr=ref("project"), dp=[ref("study_edges")], dc=[],
        kn=[ref("k_silhouette")], st=sym("open"), ph=sym("sample"),
        ip=[], op=[ref("scout_sample")], ca=[], vr=[]),
    rec("make_medic", "T",
        nm="Produce the medic against the accepted scout baseline",
        ow=ref("actor"), pr=ref("project"), dp=[ref("sample_scout")], dc=[],
        kn=[ref("k_silhouette")], st=sym("open"), ph=sym("production"),
        ip=[], op=[ref("medic_sprite")], ca=[], vr=[]),
    rec("deliver_family", "T",
        nm="Assemble and deliver the scout and medic family",
        ow=ref("actor"), pr=ref("project"),
        dp=[ref("sample_scout"), ref("make_medic")], dc=[], kn=[],
        st=sym("open"), ph=sym("delivery"),
        ip=[], op=[ref("family_pack")], ca=[], vr=[]),

    # --- project -------------------------------------------------------------
    rec("project", "P",
        nm="Scout and medic character family",
        ow=ref("user"),
        br="Side-view scout and medic character family matching the supplied "
           "references. Outline treatment disputed between references; final canvas "
           "size not chosen.",
        sc=[ref("brief"), ref("ref_a"), ref("ref_b"), ref("measure"), ref("kmethods")],
        in_=[]),
]

# `in` is a Python keyword; fix it up after construction.
for r in records:
    if r["kind"] == "P":
        r["fields"]["in"] = [ref(x["id"]) for x in records if x["kind"] == "I"]
        del r["fields"]["in_"]

doc = {"revision": 1, "format": 2, "records": records}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "candidate-r1.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
print("wrote", OUT / "candidate-r1.json", len(records), "records")
