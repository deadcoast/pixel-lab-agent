"""Revision 12 (2026-11-15f): bind the handoff-only continuation note and handoff_8.

Appends two records to the revision 11 head and changes nothing else:
  S s_continuation_7  deliverables/continuation-2026-11-15f.md
  N handoff_8         rv 12, nx [t_sample], bl [t_scout, t_medic, t_family]
No I status/value, C, F, Q, T, X, E, V, D, J or P change. No production change of any kind:
this increment relocated the consumer root and re-verified the retained state.
handoff_8.fo names the current and previous continuation, the v2 and v1 sample packet S records,
the shared criteria S record, the evaluation-answer source, c_sample, f_sample, every I record
whose status is not `confirmed` (in state order), and the two accepted research artifacts.
Encodes work/rev12.json -> work/rev12.px; the commit is performed separately against the
revision 11 hash.

Run from the consumer root with the selected interpreter:  python -I work/build_rev12.py
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
AT = "2026-11-15"
EXPECT_REV = 11
EXPECT_HASH = "720a1a1ecc59f210654485f4e279b1cb58dd881629ece37ef2db323c1ecec443"
NOTE = "deliverables/continuation-2026-11-15f.md"
OUT_JSON, OUT_PX = "work/rev12.json", "work/rev12.px"
EXPECTED_OPEN_I = ["i_alpha", "i_animation", "i_backgrounds", "i_canvas", "i_design_language",
                   "i_display_scale", "i_engine", "i_lighting", "i_outline", "i_palette",
                   "i_role_diff", "i_sampling"]


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


def main():
    cur = json.loads(subprocess.run([PY, RUNNER, "decode", "state.px/state.px"],
                                    capture_output=True, text=True, check=True,
                                    encoding="utf-8").stdout)
    assert cur["revision"] == EXPECT_REV, cur["revision"]
    assert sha("state.px/state.px") == EXPECT_HASH, "head bytes drifted"
    R = cur["records"]
    by_id = {r["id"]: r for r in R}
    for new_id in ("s_continuation_7", "handoff_8"):
        assert new_id not in by_id, new_id
    before = json.dumps(R, sort_keys=True)

    open_i = [r["id"] for r in R
              if r["kind"] == "I" and r["fields"]["st"] != sym("confirmed")]
    assert open_i == EXPECTED_OPEN_I, open_i

    assert lines(NOTE) >= 1, NOTE
    R.append({"id": "s_continuation_7", "kind": "S", "fields": {
        "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines(NOTE)], "at": AT, "au": sym("local")}})

    R.append({"id": "handoff_8", "kind": "N", "fields": {
        "wh": ref("actor"),
        "fo": refs("s_continuation_7", "s_continuation_6", "s_sample_brief_v2",
                   "s_sample_request_review_v2", "s_sample_criteria", "s_sample_brief",
                   "s_sample_request_review", "s_eval_answers", "c_sample", "f_sample",
                   *open_i, "x_aid", "x_study"),
        "nx": refs("t_sample"),
        "bl": refs("t_scout", "t_medic", "t_family"),
        "rv": 12}})

    assert json.dumps(R[: len(R) - 2], sort_keys=True) == before
    json.dump({"revision": 12, "records": R, "format": 2},
              open(OUT_JSON, "w", encoding="utf-8"), indent=1)
    subprocess.run([PY, RUNNER, "encode", OUT_JSON, "--out", OUT_PX], check=True)
    print("encoded", OUT_PX, "with", len(R), "records; note", sha(NOTE), lines(NOTE), "lines")


if __name__ == "__main__":
    main()
