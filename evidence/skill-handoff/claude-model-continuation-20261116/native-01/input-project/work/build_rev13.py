"""Revision 13 (2026-11-15g): bind the correction note after the caller review of revision 12.

Appends two records to the revision 12 head and changes nothing else:
  S s_continuation_8  deliverables/continuation-2026-11-15g.md
  N handoff_9         rv 13, nx [t_sample], bl [t_scout, t_medic, t_family],
                      fo = [s_continuation_8] + handoff_8.fo (read from the head, asserted)
The f note (s_continuation_7) and every revision 12 record keep their bytes; the g note records
the old-to-new correction of one locator in the f note and of the SESSION.md provenance lines.
No I status/value, C, F, Q, T, X, E, V, D, J or P change; no production change of any kind.
Encodes work/rev13.json -> work/rev13.px; the commit is performed separately against the
revision 12 hash.

Run from the consumer root with the selected interpreter:  python -I work/build_rev13.py
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
AT = "2026-11-15"
EXPECT_REV = 12
EXPECT_HASH = "f6b2c25456d1abbc49bf4e6f6d1305749bf2e0b105738428f066f14b3070e632"
NOTE = "deliverables/continuation-2026-11-15g.md"
OUT_JSON, OUT_PX = "work/rev13.json", "work/rev13.px"
HANDOFF_8_FO = ["s_continuation_7", "s_continuation_6", "s_sample_brief_v2",
                "s_sample_request_review_v2", "s_sample_criteria", "s_sample_brief",
                "s_sample_request_review", "s_eval_answers", "c_sample", "f_sample", "i_alpha",
                "i_animation", "i_backgrounds", "i_canvas", "i_design_language", "i_display_scale",
                "i_engine", "i_lighting", "i_outline", "i_palette", "i_role_diff", "i_sampling",
                "x_aid", "x_study"]


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
    for new_id in ("s_continuation_8", "handoff_9"):
        assert new_id not in by_id, new_id
    before = json.dumps(R, sort_keys=True)

    fo_8 = [r["$ref"] for r in by_id["handoff_8"]["fields"]["fo"]]
    assert fo_8 == HANDOFF_8_FO, fo_8

    assert lines(NOTE) >= 1, NOTE
    R.append({"id": "s_continuation_8", "kind": "S", "fields": {
        "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines(NOTE)], "at": AT, "au": sym("local")}})

    R.append({"id": "handoff_9", "kind": "N", "fields": {
        "wh": ref("actor"),
        "fo": refs("s_continuation_8", *fo_8),
        "nx": refs("t_sample"),
        "bl": refs("t_scout", "t_medic", "t_family"),
        "rv": 13}})

    assert json.dumps(R[: len(R) - 2], sort_keys=True) == before
    json.dump({"revision": 13, "records": R, "format": 2},
              open(OUT_JSON, "w", encoding="utf-8"), indent=1)
    subprocess.run([PY, RUNNER, "encode", OUT_JSON, "--out", OUT_PX], check=True)
    print("encoded", OUT_PX, "with", len(R), "records; note", sha(NOTE), lines(NOTE), "lines")


if __name__ == "__main__":
    main()
