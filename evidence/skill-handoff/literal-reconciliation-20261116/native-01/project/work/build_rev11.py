"""Revision 11 (2026-11-15e): bind the successor brief/packet (caller findings 1 and 2) and note.

Appends four records to the revision 10 head and changes nothing else:
  S s_sample_brief_v2           deliverables/sample-request/sample-creative-brief-v2.json
  S s_sample_request_review_v2  deliverables/sample-request/request-review-v2.json
  S s_continuation_6            deliverables/continuation-2026-11-15e.md
  N handoff_7                   rv 11, nx [t_sample], bl [t_scout, t_medic, t_family]
The v1 packet S records (s_sample_brief, s_sample_criteria, s_sample_request_review) stay as
the pre-discovery identity. No I status/value, C, F, Q, T, X, E, V, D or P change.
Encodes work/rev11.json -> work/rev11.px; the commit is performed separately against the
revision 10 hash.

Run from the consumer root with the selected interpreter:  python -I work/build_rev11.py
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
AT = "2026-11-15"
EXPECT_REV = 10
EXPECT_HASH = "23f4ee559508bab7b1966348589c1431604b848b804f7e6599940e48b06968c6"
NEW_SOURCES = {
    "s_sample_brief_v2": "deliverables/sample-request/sample-creative-brief-v2.json",
    "s_sample_request_review_v2": "deliverables/sample-request/request-review-v2.json",
    "s_continuation_6": "deliverables/continuation-2026-11-15e.md",
}
OUT_JSON, OUT_PX = "work/rev11.json", "work/rev11.px"


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
                                    capture_output=True, text=True, check=True).stdout)
    assert cur["revision"] == EXPECT_REV, cur["revision"]
    assert sha("state.px/state.px") == EXPECT_HASH, "head bytes drifted"
    R = cur["records"]
    by_id = {r["id"]: r for r in R}
    for new_id in (*NEW_SOURCES, "handoff_7"):
        assert new_id not in by_id, new_id
    before = json.dumps(R, sort_keys=True)

    for sid, path in NEW_SOURCES.items():
        assert lines(path) >= 1, path
        R.append({"id": sid, "kind": "S", "fields": {
            "ur": path, "dg": sha(path), "ln": [1, lines(path)], "at": AT, "au": sym("local")}})

    R.append({"id": "handoff_7", "kind": "N", "fields": {
        "wh": ref("actor"),
        "fo": refs("s_continuation_6", "s_sample_brief_v2", "s_sample_request_review_v2",
                   "s_sample_criteria", "s_sample_brief", "s_sample_request_review",
                   "s_continuation_5", "s_eval_answers", "c_sample", "f_sample",
                   "i_outline", "i_canvas", "i_palette", "i_design_language", "i_backgrounds",
                   "i_display_scale", "i_role_diff", "i_animation", "i_engine",
                   "x_aid", "x_study"),
        "nx": refs("t_sample"),
        "bl": refs("t_scout", "t_medic", "t_family"),
        "rv": 11}})

    assert json.dumps(R[: len(R) - 4], sort_keys=True) == before
    json.dump({"revision": 11, "records": R, "format": 2},
              open(OUT_JSON, "w", encoding="utf-8"), indent=1)
    subprocess.run([PY, RUNNER, "encode", OUT_JSON, "--out", OUT_PX], check=True)
    print("encoded", OUT_PX, "with", len(R), "records")


if __name__ == "__main__":
    main()
