"""Revision 9 (2026-11-15c): apply sources/controlled-evaluation-answers.md to the sample.

Applies the retained recipe (deliverables/continuation-2026-11-15.md steps 1-5, step 3 as
amended by deliverables/continuation-2026-11-15b.md):
  1. S record for the new input (exact digest, line range; the file is not copied).
  2. Intake: i_outline conflict -> proposed, i_canvas unresolved -> proposed (sample-scoped
     controlled-evaluation confirmation, NOT owner confirmation); i_palette keeps observed,
     gains the new source and a current rationale. i_view / i_sampling / i_alpha keep their
     status, value word and sources; their wire type changes from string to symbol because
     lifecycle.py lines 133-138 pin a linked choice keyed by a contract field name to the
     contract field through encode_value, and C.vw / C.sa / C.al are symbol fields
     (codec.py 213-217 encodes a symbol as `side` and a string as `~4:side`).
  3. C c_sample with composed li; f_sample.ct = c_sample.
  4. Sample-specific Q records swapped into f_sample.rq (correction 4); original Q records
     untouched for f_scout / f_medic.
  5. handoff_5 (rv 9) and S record for the new continuation note.

Encodes work/rev9.json -> work/rev9.px. The commit is performed separately with the
expected revision-8 hash. No X, V, E, D or task-state change.

Run from the consumer root with the selected interpreter:
  python -I work/build_rev9.py                      # candidate (symbol-typed pinned values)
  python -I work/build_rev9.py --keep-string-values # diagnostic only: shows the pin failure
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
ANSWERS = "sources/controlled-evaluation-answers.md"
ANSWERS_SHA = "87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30"
NOTE = "deliverables/continuation-2026-11-15c.md"
AT = "2026-11-15"
EXPECT_REV = 8
EXPECT_HASH = "ac9150f4e8ee656761811370867538130faaa111759d61065153df358ef14225"
KEEP_STRINGS = "--keep-string-values" in sys.argv[1:]
OUT_JSON = "work/rev9-strings-diagnostic.json" if KEEP_STRINGS else "work/rev9.json"
OUT_PX = "work/rev9-strings-diagnostic.px" if KEEP_STRINGS else "work/rev9.px"


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


# ---- exact texts (also pasted verbatim into the continuation note; verify_rev9.py checks) ----

OUTLINE_ALT_A = ("reference.png: flat 2px dark outline #25354A fully enclosing the body, also "
                 "carrying the shoulder bar, base bar and solid top stalks")
OUTLINE_ALT_B = "reference-b.png: no outline, flat teal silhouette with cream eyes only"

OUTLINE_WY = (
    "Status moved conflict -> proposed in revision 9 on the authority of "
    "sources/controlled-evaluation-answers.md (s_eval_answers), which confirms the outlined "
    "treatment of reference.png for the representative sample only and states that it does "
    "not express a real owner preference, bind family or production policy, or provide human "
    "acceptance. `proposed` rather than `confirmed`: the project-level choice remains the "
    "owner's; a confirmed status would present a sample-scoped evaluation answer as an owner "
    "decision and would clear the production-phase unconfirmed gate once a production "
    "contract links this choice. The value is the first of the two alternatives retained "
    "while this choice was in conflict; the other alternative remains open for the family "
    "and for production: '" + OUTLINE_ALT_B + "'. Measured context unchanged: the two "
    "references differ in exactly 180 pixels, every one #25354A becoming #56B5BC; the "
    "outline is load-bearing rather than trim because it also carries the shoulder bar, base "
    "bar and stalk interiors; the bundled edge-rhythm method states contour style is "
    "authored intent and must not be resolved mechanically. The owner's own answer, informed "
    "by deliverables/outline-decision-brief.md, still decides the family treatment.")

CANVAS_WY = (
    "Status moved unresolved -> proposed in revision 9 on the authority of "
    "sources/controlled-evaluation-answers.md (s_eval_answers): 32 x 32 is confirmed for the "
    "representative sample only, with the stated limits that it is not a real owner "
    "preference, does not bind family or production policy and is not human acceptance. "
    "`proposed` rather than `confirmed` because the owner has explicitly not chosen the final "
    "canvas size (s_brief) and the input does not change that; a confirmed status would read "
    "as the project canvas and would clear the production-phase unconfirmed gate once a "
    "production contract links this choice. 32 x 32 is also the measured canvas of both "
    "references carrying an 18 x 25 figure (s_refobs), an observation that did not by itself "
    "adopt the value. Supplies C.px of the sample contract c_sample. The final canvas for "
    "scout/medic production remains the owner's decision.")

PALETTE_WY = (
    "Measured from the references: teal body #56B5BC and cream eyes #F4DDA2 in both, navy "
    "#25354A present only in reference.png. Observed, not agreed. Revision 9: the "
    "sample-scoped outlined-treatment answer in sources/controlled-evaluation-answers.md "
    "(s_eval_answers) brings #25354A into the sample's working palette, so all three "
    "measured colours supply C.pl of c_sample; the status stays observed because no owner "
    "instruction has adopted these exact values as the project palette and the answer binds "
    "the sample only. Confirmation for production remains coupled to the unresolved "
    "role-differentiation device (i_role_diff), which may need a reserved accent; the "
    "exclusive membership rule in q_palette is a derived rule, not a brief statement.")

C_NM = ("Representative sample: side-view scout, single idle pose, 32 x 32, outlined as "
        "reference.png; sample-scoped contract from the controlled-evaluation answers, not a "
        "family or production contract")

C_LI = (
    "[1 lighting; observed from reference.png and reference-b.png (i_lighting, s_refobs)] "
    "Flat colour: no directional light, no shading ramps. "
    "[2 design language; PIXL proposal awaiting owner agreement (i_design_language)] Carry "
    "the references' flat colour, absent anti-aliasing, binary alpha and blocky low-detail "
    "construction into a genuinely side-view figure; the references' front-facing symmetric "
    "shape is a style swatch, not the character design. "
    "[3 outline; controlled-evaluation sample confirmation (i_outline, "
    "sources/controlled-evaluation-answers.md): sample only, not an owner preference, not "
    "family or production policy] Outlined as reference.png: a flat #25354A contour at the "
    "weight shown there (2 logical px) fully enclosing the figure and also carrying the "
    "shoulder bar, base bar and solid top stalks, adapted to the side view; the no-outline "
    "treatment of reference-b.png stays open for the family. "
    "[4 identity landmarks for the readability criterion; PIXL construction proposal under "
    "component 2, not an owner requirement] (a) two top stalks separated by a notch, solid in "
    "the contour colour; (b) cream eye placement adapted to profile so the figure has an "
    "unambiguous facing direction; (c) the navy shoulder bar; (d) the navy base bar; (e) the "
    "enclosing navy contour separating the figure from the background. The single idle pose "
    "faces right, a scoped specialist choice for the sample that the engine can mirror.")

Q_SAMPLE_CANVAS = (
    "The candidate file is exactly 32 x 32 pixels, the canvas of the sample contract "
    "c_sample, and contains zero fractional-alpha pixels under that contract's binary alpha. "
    "Scope: the representative sample only; the canvas is a sample-scoped "
    "controlled-evaluation confirmation and the alpha policy an observation from the "
    "references, neither a confirmed project policy.")

Q_SAMPLE_PALETTE = (
    "Every visible pixel of the candidate is one of the three colours of the sample contract "
    "c_sample palette, #56B5BC, #F4DDA2 and #25354A, with no colours outside it. Scope: the "
    "representative sample only; these are the colours measured in the references, all three "
    "admitted by the sample-scoped outlined-treatment confirmation, and exclusivity is a "
    "sample working rule that a later role accent may reopen; this is not a confirmed "
    "project palette.")

Q_SAMPLE_OUTLINE = (
    "Inspected at native scale and at integer zoom, the candidate applies the outlined "
    "treatment of the sample contract c_sample, the treatment shown in reference.png: a flat "
    "#25354A contour at the weight shown there (2 logical px) fully enclosing the figure, "
    "applied consistently on every contour and also carrying the interior landmarks that "
    "treatment is responsible for (shoulder bar, base bar, solid top stalks) adapted to the "
    "side view. Scope: the representative sample only, under the sample-scoped "
    "controlled-evaluation confirmation; not a confirmed family treatment.")

Q_SAMPLE_READABILITY = (
    "At native scale and at the target integer zoom, on light, dark and busy test "
    "backgrounds, the figure reads as a side-view character with an unambiguous facing "
    "direction, and the identity landmarks named in the sample contract c_sample (two notched "
    "top stalks, cream eye placement, navy shoulder bar, navy base bar, enclosing navy "
    "contour) remain separable. The target integer zoom requires i_display_scale before "
    "review; the three test backgrounds are the specialist's test set until i_backgrounds is "
    "answered.")

TEXTS = {
    "c_sample.nm": C_NM, "c_sample.li": C_LI,
    "q_sample_canvas.ck": Q_SAMPLE_CANVAS, "q_sample_palette.ck": Q_SAMPLE_PALETTE,
    "q_sample_outline.ck": Q_SAMPLE_OUTLINE, "q_sample_readability.ck": Q_SAMPLE_READABILITY,
    "i_outline.wy": OUTLINE_WY, "i_canvas.wy": CANVAS_WY, "i_palette.wy": PALETTE_WY,
}


def main():
    assert sha(ANSWERS) == ANSWERS_SHA, "input digest drifted"
    cur = json.loads(subprocess.run([PY, RUNNER, "decode", "state.px/state.px"],
                                    capture_output=True, text=True, check=True).stdout)
    assert cur["revision"] == EXPECT_REV, cur["revision"]
    assert sha("state.px/state.px") == EXPECT_HASH, "head bytes drifted"
    R = cur["records"]
    by_id = {r["id"]: r for r in R}
    for new_id in ("s_eval_answers", "c_sample", "q_sample_canvas", "q_sample_palette",
                   "q_sample_outline", "q_sample_readability", "handoff_5", "s_continuation_4"):
        assert new_id not in by_id, new_id

    # ---- step 1: source record for the new input ----
    R.append({"id": "s_eval_answers", "kind": "S", "fields": {
        "ur": ANSWERS, "dg": ANSWERS_SHA, "ln": [1, lines(ANSWERS)], "at": AT,
        "au": sym("local")}})

    # ---- step 2: intake ----
    o = by_id["i_outline"]["fields"]
    assert o["st"] == sym("conflict") and o["vl"] == [OUTLINE_ALT_A, OUTLINE_ALT_B], o
    o["st"] = sym("proposed")
    o["vl"] = OUTLINE_ALT_A
    o["so"] = refs("s_brief", "s_refobs", "s_ref_a", "s_ref_b", "s_eval_answers")
    o["wy"] = OUTLINE_WY

    c = by_id["i_canvas"]["fields"]
    assert c["st"] == sym("unresolved") and c["vl"] is None, c
    c["st"] = sym("proposed")
    c["vl"] = [32, 32]
    c["so"] = refs("s_brief", "s_refobs", "s_eval_answers")
    c["wy"] = CANVAS_WY

    p = by_id["i_palette"]["fields"]
    assert p["st"] == sym("observed") and p["vl"] == ["#56B5BC", "#F4DDA2", "#25354A"], p
    p["so"] = refs("s_refobs", "s_ref_a", "s_ref_b", "s_eval_answers")
    p["wy"] = PALETTE_WY

    # Representation-only change forced by the contract pin (see module docstring).
    for cid, word in (("i_view", "side"), ("i_sampling", "nearest"), ("i_alpha", "binary")):
        f = by_id[cid]["fields"]
        assert f["vl"] == word, (cid, f["vl"])
        if not KEEP_STRINGS:
            f["vl"] = sym(word)

    # ---- step 3: contract ----
    R.append({"id": "c_sample", "kind": "C", "fields": {
        "nm": C_NM,
        "px": [32, 32],
        "pl": ["#56B5BC", "#F4DDA2", "#25354A"],
        "vw": sym("side"), "sa": sym("nearest"), "al": sym("binary"),
        "li": C_LI,
        "ch": refs("i_canvas", "i_palette", "i_view", "i_sampling", "i_alpha", "i_lighting",
                   "i_outline", "i_design_language")}})
    fs = by_id["f_sample"]["fields"]
    assert "ct" not in fs
    fs["ct"] = ref("c_sample")

    # ---- step 4: sample-specific criteria (originals untouched for f_scout / f_medic) ----
    def q(id_, nm, dm, md, ck, *so):
        R.append({"id": id_, "kind": "Q", "fields": {
            "nm": nm, "dm": sym(dm), "md": sym(md), "ck": ck, "wh": ref("actor"),
            "so": refs(*so)}})

    q("q_sample_canvas", "sample canvas and alpha", "mechanical", "local", Q_SAMPLE_CANVAS,
      "s_eval_answers", "s_refobs")
    q("q_sample_palette", "sample palette membership", "mechanical", "local", Q_SAMPLE_PALETTE,
      "s_refobs", "s_eval_answers")
    q("q_sample_outline", "sample outline treatment applied", "visual", "visual",
      Q_SAMPLE_OUTLINE, "s_eval_answers", "s_ref_a", "s_refobs")
    q("q_sample_readability", "sample side-view readability", "visual", "visual",
      Q_SAMPLE_READABILITY, "s_methods", "s_refobs", "s_continuation_2")
    assert fs["rq"] == refs("q_canvas", "q_palette", "q_outline", "q_readability",
                            "q_style_match"), fs["rq"]
    fs["rq"] = refs("q_sample_canvas", "q_sample_palette", "q_sample_outline",
                    "q_sample_readability", "q_style_match")
    for fid in ("f_scout", "f_medic"):
        assert by_id[fid]["fields"]["rq"][:5] == refs("q_canvas", "q_palette", "q_outline",
                                                        "q_readability", "q_style_match")

    # ---- step 5: handoff and continuation source ----
    R.append({"id": "s_continuation_4", "kind": "S", "fields": {
        "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines(NOTE)], "at": AT, "au": sym("local")}})
    R.append({"id": "handoff_5", "kind": "N", "fields": {
        "wh": ref("actor"),
        "fo": refs("s_continuation_4", "s_eval_answers", "c_sample", "i_outline", "i_canvas",
                   "i_palette", "i_backgrounds", "i_design_language", "i_lighting",
                   "i_animation", "i_display_scale", "i_role_diff", "i_engine",
                   "x_aid", "x_study"),
        "nx": refs("t_sample"),
        "bl": refs("t_scout", "t_medic", "t_family"),
        "rv": 9}})

    json.dump({"revision": 9, "records": R, "format": 2},
              open(OUT_JSON, "w", encoding="utf-8"), indent=1)
    json.dump(TEXTS, open("work/rev9-texts.json", "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    subprocess.run([PY, RUNNER, "encode", OUT_JSON, "--out", OUT_PX], check=True)
    print("encoded", OUT_PX, "with", len(R), "records; keep_strings =", KEEP_STRINGS)


if __name__ == "__main__":
    main()
