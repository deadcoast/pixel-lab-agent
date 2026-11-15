"""Reproducible checks for revision 9 (2026-11-15c). Read-only.

1. Every exact text in work/rev9-texts.json (contract nm/li, the four sample criteria, the
   three rewritten rationales) appears verbatim in deliverables/continuation-2026-11-15c.md.
2. The committed head decodes as revision 9 with the expected record IDs, f_sample links,
   intake statuses, and untouched original Q/X/V records (compared with work/rev8.json).
3. s_continuation_4 / s_eval_answers digests equal the current file bytes.

Run from the consumer root with the selected interpreter:
  python -I work/verify_rev9.py [path-to-state, default state.px/state.px]
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
STATE = sys.argv[1] if len(sys.argv) > 1 else "state.px/state.px"
NOTE = "deliverables/continuation-2026-11-15c.md"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def decode(p):
    return json.loads(subprocess.run([PY, RUNNER, "decode", p], capture_output=True,
                                     text=True, check=True).stdout)


problems = []
note = open(NOTE, encoding="utf-8").read()
texts = json.load(open("work/rev9-texts.json", encoding="utf-8"))
for key, text in texts.items():
    if text not in note:
        problems.append(f"note lacks verbatim {key}")

doc = decode(STATE)
by = {r["id"]: r for r in doc["records"]}
old = {r["id"]: r for r in json.load(open("work/rev8.json", encoding="utf-8"))["records"]}
if doc["revision"] != 9:
    problems.append(f"revision {doc['revision']} != 9")
if len(by) != 71:
    problems.append(f"{len(by)} records != 71")
for new in ("s_eval_answers", "c_sample", "q_sample_canvas", "q_sample_palette",
            "q_sample_outline", "q_sample_readability", "handoff_5", "s_continuation_4"):
    if new not in by:
        problems.append(f"missing {new}")

fs = by["f_sample"]["fields"]
if fs.get("ct") != {"$ref": "c_sample"}:
    problems.append("f_sample.ct is not c_sample")
want_rq = [{"$ref": x} for x in ("q_sample_canvas", "q_sample_palette", "q_sample_outline",
                                 "q_sample_readability", "q_style_match")]
if fs["rq"] != want_rq:
    problems.append(f"f_sample.rq {fs['rq']}")

for cid, st in (("i_outline", "proposed"), ("i_canvas", "proposed"), ("i_palette", "observed"),
                ("i_view", "confirmed"), ("i_sampling", "proposed"), ("i_alpha", "observed")):
    if by[cid]["fields"]["st"] != {"$symbol": st}:
        problems.append(f"{cid}.st != {st}")
for cid, word in (("i_view", "side"), ("i_sampling", "nearest"), ("i_alpha", "binary")):
    f, o = by[cid]["fields"], old[cid]["fields"]
    if f["vl"] != {"$symbol": word}:
        problems.append(f"{cid}.vl not symbol {word}")
    for k in ("ky", "pr", "so", "st", "wh", "wy"):
        if f[k] != o[k]:
            problems.append(f"{cid}.{k} changed")
if by["i_canvas"]["fields"]["vl"] != [32, 32]:
    problems.append("i_canvas.vl != [32, 32]")
c = by["c_sample"]["fields"]
if c["px"] != [32, 32] or c["pl"] != ["#56B5BC", "#F4DDA2", "#25354A"] or c["li"] != texts["c_sample.li"]:
    problems.append("c_sample fields differ from the published texts")

# untouched records: every X, V, E, T, original Q, other F, earlier S/N, actors, project
for rid, rec in old.items():
    if rid in ("i_outline", "i_canvas", "i_palette", "i_view", "i_sampling", "i_alpha", "f_sample"):
        continue
    if by.get(rid) != rec:
        problems.append(f"{rid} changed but should be untouched")

for sid, path in (("s_continuation_4", NOTE), ("s_eval_answers", "sources/controlled-evaluation-answers.md")):
    f = by[sid]["fields"]
    if f["ur"] != path or f["dg"] != sha(path):
        problems.append(f"{sid} digest/path mismatch")
    if f["ln"] != [1, open(path, "rb").read().count(b"\n")]:
        problems.append(f"{sid} line range mismatch")

print(json.dumps({"state": STATE, "head_sha256": sha(STATE), "revision": doc["revision"],
                  "records": len(by), "problems": problems}, indent=1))
sys.exit(1 if problems else 0)
