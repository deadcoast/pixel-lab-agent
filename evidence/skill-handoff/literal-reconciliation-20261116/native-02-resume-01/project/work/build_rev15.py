"""Revision 15 (2026-11-16, b): bind the handoff-only continuation note written under the
249faf48 consumer root after the kit changed between evaluation roots a fourth time.

Appends two records to the revision 14 head and changes nothing else:
  S s_continuation_10  deliverables/continuation-2026-11-16b.md
  N handoff_11         rv 15, nx [t_sample], bl [t_scout, t_medic, t_family],
                       fo = [s_continuation_10] + handoff_10.fo (read from the head, asserted)
The 2026-11-16 note (s_continuation_9), the g note (s_continuation_8), the f note
(s_continuation_7) and every revision 14 record keep their bytes. No I status/value, C, F, Q, T,
X, E, V, D, J or P change; no production change of any kind. Encodes work/rev15.json ->
work/rev15.px; the commit is performed separately against the revision 14 hash.

Run from the consumer root with the selected interpreter:
  python -B -I work/build_rev15.py
Kit runner subprocesses are started with -B -I as well, so no bytecode cache is written into
the read-only kit regardless of the shell's PYTHONDONTWRITEBYTECODE setting.
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
AT = "2026-11-16"
EXPECT_REV = 14
EXPECT_HASH = "247b22ba715519ef2033fcea6de3dcabed45f288edcbcc5616b235e26e77e4af"
NOTE = "deliverables/continuation-2026-11-16b.md"
OUT_JSON, OUT_PX = "work/rev15.json", "work/rev15.px"
HANDOFF_8_FO = ["s_continuation_7", "s_continuation_6", "s_sample_brief_v2",
                "s_sample_request_review_v2", "s_sample_criteria", "s_sample_brief",
                "s_sample_request_review", "s_eval_answers", "c_sample", "f_sample", "i_alpha",
                "i_animation", "i_backgrounds", "i_canvas", "i_design_language", "i_display_scale",
                "i_engine", "i_lighting", "i_outline", "i_palette", "i_role_diff", "i_sampling",
                "x_aid", "x_study"]
HANDOFF_9_FO = ["s_continuation_8"] + HANDOFF_8_FO
HANDOFF_10_FO = ["s_continuation_9"] + HANDOFF_9_FO


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


def runner(*args):
    return subprocess.run([PY, "-B", "-I", RUNNER, *args], capture_output=True, text=True,
                          check=True, encoding="utf-8").stdout


def main():
    cur = json.loads(runner("decode", "state.px/state.px"))
    assert cur["revision"] == EXPECT_REV, cur["revision"]
    assert sha("state.px/state.px") == EXPECT_HASH, "head bytes drifted"
    R = cur["records"]
    assert len(R) == 86, len(R)
    by_id = {r["id"]: r for r in R}
    for new_id in ("s_continuation_10", "handoff_11"):
        assert new_id not in by_id, new_id
    before = json.dumps(R, sort_keys=True)

    fo_10 = [r["$ref"] for r in by_id["handoff_10"]["fields"]["fo"]]
    assert fo_10 == HANDOFF_10_FO, fo_10

    assert lines(NOTE) >= 1, NOTE
    R.append({"id": "s_continuation_10", "kind": "S", "fields": {
        "ur": NOTE, "dg": sha(NOTE), "ln": [1, lines(NOTE)], "at": AT, "au": sym("local")}})

    R.append({"id": "handoff_11", "kind": "N", "fields": {
        "wh": ref("actor"),
        "fo": refs("s_continuation_10", *fo_10),
        "nx": refs("t_sample"),
        "bl": refs("t_scout", "t_medic", "t_family"),
        "rv": 15}})

    assert json.dumps(R[: len(R) - 2], sort_keys=True) == before
    json.dump({"revision": 15, "records": R, "format": 2},
              open(OUT_JSON, "w", encoding="utf-8"), indent=1)
    runner("encode", OUT_JSON, "--out", OUT_PX)
    print("encoded", OUT_PX, "with", len(R), "records; note", sha(NOTE), lines(NOTE), "lines")


if __name__ == "__main__":
    main()
