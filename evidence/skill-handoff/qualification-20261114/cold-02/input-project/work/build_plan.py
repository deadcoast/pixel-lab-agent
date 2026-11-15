import hashlib, json

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def nlines(p):
    return len(open(p, "r", encoding="utf-8").read().splitlines())

AT = "2026-09-14"

def sym(s):
    return {"$symbol": s}

def ref(s):
    return {"$ref": s}

def refs(*a):
    return [ref(x) for x in a]

def S(ur, ln=None):
    return {"ur": ur, "dg": sha(ur), "ln": ln if ln is not None else [1, nlines(ur)],
            "at": AT, "au": sym("local")}

R = []

def rec(i, k, **f):
    R.append({"id": i, "kind": k, "fields": f})

# --- actors ---
rec("actor", "A", nm="PIXL", rl=sym("agent"))
rec("user", "A", nm="Project owner", rl=sym("user"))

# --- sources ---
rec("s_brief", "S", **S("sources/brief.md"))
rec("s_refobs", "S", **S("sources/reference-observations.md"))
rec("s_methods", "S", **S("sources/method-research.md"))
rec("s_ref_a", "S", ur="reference.png", dg=sha("reference.png"), ln=[], at=AT, au=sym("local"))
rec("s_ref_b", "S", ur="reference-b.png", dg=sha("reference-b.png"), ln=[], at=AT, au=sym("local"))

# --- intake choices ---
I = [
    ("i_outline", "edge_treatment", "conflict",
     ["reference.png: flat 2px dark outline #25354A fully enclosing the body, also carrying the shoulder bar, base bar and solid top stalks",
      "reference-b.png: no outline, flat teal silhouette with cream eyes only"],
     ["s_brief", "s_refobs", "s_ref_a", "s_ref_b"],
     "The user states the references disagree here. Measured: the two files differ in exactly 180 pixels and every difference is #25354A becoming #56B5BC. The outline is load-bearing rather than trim, because removing it also removes the shoulder bar, base bar and stalk interiors. Retained as a conflict; the bundled edge-rhythm method states contour style is authored intent and must not be resolved mechanically."),
    ("i_canvas", "px", "unresolved", None, ["s_brief", "s_refobs"],
     "The user has explicitly not chosen the final canvas size. Both references are 32x32 carrying an 18x25 figure, which is an observation about the source art and not an adopted project value. This choice blocks every raster output plan."),
    ("i_display_scale", "display_scale", "unresolved", None, ["s_methods"],
     "The target on-screen integer zoom is not stated. The bundled integer-presentation method requires a target viewport as an input, and the scale bounds how much interior detail survives, so it interacts with the canvas choice."),
    ("i_view", "vw", "confirmed", "side", ["s_brief"],
     "The brief states the destination is a side-view game."),
    ("i_roster", "roster", "confirmed", ["scout", "medic"], ["s_brief"],
     "The brief names exactly these two family members."),
    ("i_palette", "pl", "observed", ["#56B5BC", "#F4DDA2", "#25354A"], ["s_refobs", "s_ref_a", "s_ref_b"],
     "Measured from the references: teal body, cream eyes, and navy present only in reference.png. Observed, not agreed. Whether #25354A belongs to the output palette depends entirely on the unresolved outline decision, so this cannot be confirmed first."),
    ("i_alpha", "al", "observed", "binary", ["s_refobs"],
     "Both references contain zero fractional-alpha pixels. Observed from the source art; not yet confirmed as this project output policy."),
    ("i_sampling", "sa", "proposed", "nearest", ["s_methods"],
     "Proposal. Neither reference contains anti-aliasing or dithering, so nearest sampling preserves the supplied look. Proposed rather than confirmed because the display scale and engine are unknown."),
    ("i_design_language", "design_language", "proposed",
     "Carry the flat colour, absent anti-aliasing, binary alpha and blocky low-detail construction of the references into a genuinely side-view figure; treat the front-facing symmetric shape of the references as a style swatch rather than as the character design.",
     ["s_brief", "s_refobs"],
     "Proposal needing the agreement of the owner. Both references are front-facing and bilaterally symmetric while the stated destination is a side-view game, so the reference pose cannot be reproduced literally. This proposal states which parts of the references are being matched and which are not."),
    ("i_role_diff", "role_differentiation", "unresolved", None, ["s_brief", "s_refobs"],
     "How a scout reads as a scout and a medic as a medic is not stated, and neither reference carries role-identifying equipment or accent colour. At the detail density of the references this needs a deliberate device, such as a reserved accent hue or a silhouette attachment."),
    ("i_engine", "engine", "unresolved", None, ["s_brief"],
     "No destination engine or importer is named, so no engine import acceptance can be performed in this project yet."),
]
for i, k, st, vl, so, wy in I:
    rec(i, "I", pr=ref("project"), wh=ref("user"), ky=k, st=sym(st), vl=vl, so=refs(*so), wy=wy)

# --- acceptance criteria ---
Q = [
    ("q_study_complete", "reference study complete", "other", "local",
     "The retained study states both reference file identities by hash, the exact count and nature of the pixel differences between them, and names every choice it leaves unresolved.", "s_brief"),
    ("q_study_seen", "reference study matches what was viewed", "visual", "visual",
     "Both references were actually inspected at native scale and at integer enlargement, and the description in the study of the outline treatment and eye placement matches what was seen.", "s_refobs"),
    ("q_canvas", "canvas and alpha", "mechanical", "local",
     "The candidate file matches the confirmed canvas size exactly and contains zero fractional-alpha pixels under the confirmed alpha policy.", "s_brief"),
    ("q_palette", "palette membership", "mechanical", "local",
     "Every visible pixel of the candidate is a member of the confirmed project palette, with no colours outside it.", "s_refobs"),
    ("q_outline", "outline treatment applied", "visual", "visual",
     "The candidate applies the confirmed outline treatment consistently on every contour and on the interior landmarks that treatment is responsible for, inspected at native scale and at integer zoom.", "s_refobs"),
    ("q_readability", "side-view readability", "visual", "visual",
     "At native scale on light, dark and busy backgrounds the figure reads as a side-view character with an unambiguous facing direction and separable head, torso and limb landmarks.", "s_methods"),
    ("q_style_match", "reads as the same style", "visual", "visual",
     "Viewed beside reference.png and reference-b.png at equal integer zoom, the candidate reads as the same art style in colour, detail density and edge language.", "s_refobs"),
    ("q_role_read", "scout and medic are distinguishable", "visual", "visual",
     "At native scale a viewer can tell the scout from the medic by silhouette or accent alone, without text or a legend.", "s_brief"),
    ("q_family_continuity", "family continuity", "continuity", "visual",
     "Viewed together at equal zoom the family members share height, volume, eye-line, ground contact and anchor placement, and use one palette.", "s_brief"),
    ("q_engine_import", "destination engine import", "engine", "live",
     "The destination engine imports the sprites with the intended nearest sampling, integer scale, pivot placement and transparency, verified in the running engine.", "s_brief"),
]
for i, nm, dm, md, ck, so in Q:
    rec(i, "Q", nm=nm, dm=sym(dm), md=sym(md), ck=ck, wh=ref("user"), so=refs(so))

# --- planned outputs ---
rec("f_study", "F", tk=ref("t_study"), nm="Reference measurement and outline-conflict study",
    kd=sym("report"), rq=refs("q_study_complete", "q_study_seen"))
rec("f_sample", "F", tk=ref("t_sample"), nm="Representative side-view scout, single idle pose",
    kd=sym("sprite"), rq=refs("q_canvas", "q_palette", "q_outline", "q_readability", "q_style_match"))
rec("f_scout", "F", tk=ref("t_scout"), nm="Scout, side view",
    kd=sym("sprite"), rq=refs("q_canvas", "q_palette", "q_outline", "q_readability", "q_style_match", "q_role_read"))
rec("f_medic", "F", tk=ref("t_medic"), nm="Medic, side view",
    kd=sym("sprite"), rq=refs("q_canvas", "q_palette", "q_outline", "q_readability", "q_style_match", "q_role_read"))
rec("f_family", "F", tk=ref("t_family"), nm="Scout and medic family delivery manifest",
    kd=sym("report"), rq=refs("q_family_continuity", "q_engine_import"))

# --- the one materialized artifact this session ---
rec("x_study", "X", nm="Reference measurement and outline-conflict study",
    ur="sources/reference-observations.md", dg=sha("sources/reference-observations.md"),
    kd=sym("report"), of=ref("f_study"))

# --- tasks ---
rec("t_study", "T", nm="Measure the references and characterise the outline disagreement",
    ow=ref("actor"), pr=ref("project"), dp=[], dc=[], kn=[], st=sym("active"), ph=sym("research"),
    ip=[], op=refs("f_study"), ca=refs("x_study"), vr=[])
rec("t_sample", "T", nm="Prove one representative side-view figure before family production",
    ow=ref("actor"), pr=ref("project"), dp=refs("t_study"), dc=[], kn=[], st=sym("open"), ph=sym("sample"),
    ip=[], op=refs("f_sample"), ca=[], vr=[])
rec("t_scout", "T", nm="Produce the scout from the accepted sample",
    ow=ref("actor"), pr=ref("project"), dp=refs("t_sample"), dc=[], kn=[], st=sym("open"), ph=sym("production"),
    ip=[], op=refs("f_scout"), ca=[], vr=[])
rec("t_medic", "T", nm="Produce the medic from the accepted sample",
    ow=ref("actor"), pr=ref("project"), dp=refs("t_sample"), dc=[], kn=[], st=sym("open"), ph=sym("production"),
    ip=[], op=refs("f_medic"), ca=[], vr=[])
rec("t_family", "T", nm="Deliver the scout and medic as one family",
    ow=ref("actor"), pr=ref("project"), dp=refs("t_scout", "t_medic"), dc=[], kn=[], st=sym("open"),
    ph=sym("delivery"), ip=[], op=refs("f_family"), ca=[], vr=[])

# --- project ---
rec("project", "P", nm="Scout and Medic character family", ow=ref("user"),
    sc=refs("s_brief", "s_refobs", "s_methods", "s_ref_a", "s_ref_b"),
    **{"in": refs(*[x[0] for x in I])},
    br="Character family matching the supplied references for a side-view game: a scout and a medic. The two supplied references disagree about outline treatment, and the user has not chosen the final canvas size. Begin the project and make the progress possible in this session.")

json.dump({"revision": 1, "records": R, "format": 2},
          open("work/plan.json", "w", encoding="utf-8"), indent=1)
print("records:", len(R))
