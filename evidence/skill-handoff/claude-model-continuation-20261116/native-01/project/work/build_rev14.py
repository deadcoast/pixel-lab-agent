"""Revision 14 (2026-11-16): bind the handoff-only continuation note written under the
9f6e7c37 consumer root after the kit changed between evaluation roots again.

Appends two records to the revision 13 head and changes nothing else:
  S s_continuation_9  deliverables/continuation-2026-11-16.md
  N handoff_10        rv 14, nx [t_sample], bl [t_scout, t_medic, t_family],
                      fo = [s_continuation_9] + handoff_9.fo (read from the head, asserted)
The f note (s_continuation_7), the g note (s_continuation_8) and every revision 13 record keep
their bytes. No I status/value, C, F, Q, T, X, E, V, D, J or P change; no production change of
any kind. Encodes work/rev14.json -> work/rev14.px; the commit is performed separately against
the revision 13 hash.

Run from the consumer root with the selected interpreter:  python -I work/build_rev14.py
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
AT = "2026-11-16"
EXPECT_REV = 13
EXPECT_HASH = "42db4c758d328c521c1f73baae1873b56b14e8a4d4d1b580c1d720dcecd8acd2"
NOTE = "deliverables/continuation-2026-11-16.md"
OUT_JSON, OUT_PX = "work/rev14.json", "work/rev14.px"
HANDOFF_8_FO = ["s_continuation_7", "s_continuation_6", "s_sample_brief_v2",
                "s_sample_request_review_v2", "s_sample_criteria", "s_sample_brief",
                "s_sample_request_review", "s_eval_answers", "c_sample", "f_sample", "i_alpha",
                "i_animation", "i_backgrounds", "i_canvas", "i_design_language", "i_display_scale",
                "i_engine", "i_lighting", "i_outline", "i_palette", "i_role_diff", "i_sampling",
                "x_aid", "x_study"]
HANDOFF_9_FO = ["s_continuation_8"] + HANDOFF_8_FO


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
    assert len(R) == 84, len(R)
    by_id = {r["id"]: r for r in R}
    for new_id in ("s_continuation_9", "handoff_10"):
        assert new_id not in by_id, new_id
    before = json.dumps(R, sort_keys=True)

    fo_9 = [r["$ref"] for r in by_id["handoff_9"]["fields"]["fo"]]
    assert fo_9 == HANDOFF_9_FO, fo_9

    assert lines(NOTE) >= 1, NOTE
    R.append({"id": "s_continuation_9", "kind": "S", "fields": {
        "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines(NOTE)], "at": AT, "au": sym("local")}})

    R.append({"id": "handoff_10", "kind": "N", "fields": {
        "wh": ref("actor"),
        "fo": refs("s_continuation_9", *fo_9),
        "nx": refs("t_sample"),
        "bl": refs("t_scout", "t_medic", "t_family"),
        "rv": 14}})

    assert json.dumps(R[: len(R) - 2], sort_keys=True) == before
    json.dump({"revision": 14, "records": R, "format": 2},
              open(OUT_JSON, "w", encoding="utf-8"), indent=1)
    subprocess.run([PY, RUNNER, "encode", OUT_JSON, "--out", OUT_PX], check=True)
    print("encoded", OUT_PX, "with", len(R), "records; note", sha(NOTE), lines(NOTE), "lines")


if __name__ == "__main__":
    main()
