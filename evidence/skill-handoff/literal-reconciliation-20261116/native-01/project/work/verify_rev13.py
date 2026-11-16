"""Reproducible checks for revision 13 (2026-11-15g). Read-only.

1. The state decodes as revision 13 with exactly the 82 revision 12 records unchanged (compared
   with work/rev12.json) plus s_continuation_8 and handoff_9 (84 records).
2. s_continuation_8 digest/line range equals the current g note bytes; the f note still hashes
   as bound by s_continuation_7 (9e0df8a1...); the retained packet, criteria, validation artifact,
   source and reference files still match the hashes quoted in revisions 10-13.
3. handoff_9 has rv 13, nx [t_sample], bl [t_scout, t_medic, t_family] and fo = [s_continuation_8]
   + handoff_8.fo.
4. The g note quotes the sha256 of every new file it lists (except itself) and does not contain
   the revision 13 hash.
5. Every file recorded in work/rev13-protected-snapshot.sha256 (taken before any write in this
   correction round) still has the same bytes, except the two files edited on purpose
   (SESSION.md and the head state.px/state.px).
6. Runner `workflow` on the state reports ready [t_sample], no jobs, files verified.
7. Running validate_criteria_v2.py (print-only) leaves criteria-schema-validation.json unchanged.

Run from the consumer root with the selected interpreter:
  python -I work/verify_rev13.py [path-to-state, default state.px/state.px]
Pass work/rev13.px to check the encoded candidate before it is committed.
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
STATE = sys.argv[1] if len(sys.argv) > 1 else "state.px/state.px"
NOTE = "deliverables/continuation-2026-11-15g.md"
SNAPSHOT = "work/rev13-protected-snapshot.sha256"
EDITED_ON_PURPOSE = {"SESSION.md", "state.px/state.px"}
RETAINED = {
    "deliverables/continuation-2026-11-15f.md": "9e0df8a1d8d4bbfa6591d16fffe07406f53c639d32b797e320232b15177a135f",
    "deliverables/continuation-2026-11-15e.md": "f174f93971f3044b9731aae34e2704d5e090c5468761361063548d15056d597f",
    "deliverables/continuation-2026-11-15d.md": "826460e5ff96f7dae2bccff8b8df1278e5457614cfaadd3c0510e0f64feeb1dc",
    "deliverables/sample-request/request-review-v2.json": "a596f02addb73ba1c7732cfe05a8071b97b7c7236f26e349fdca5184e0684d73",
    "deliverables/sample-request/sample-creative-brief-v2.json": "f84b262818bbf044eb22716ab5d02eed1103cc65714360fcfc5d9efd019a5b80",
    "deliverables/sample-request/sample-criteria.json": "14c979ea9bbfb686f7a9c693d552facfac5a135c45c3184d969611116611834b",
    "deliverables/sample-request/sample-creative-brief.json": "cc21bf77519ed46e7a6f634718efcc79816a8f9895cc4ece4e89b007bf7380ce",
    "deliverables/sample-request/request-review.json": "ffa933ede2b985eafd4c616e83b4a69d0b34a99002a731439704dcd0d781e78b",
    "deliverables/sample-request/criteria-schema-validation.json": "93643a34d32353b5471fd9943aed8bb3a0bf8cb48a94d8413c42635a1aaeb16a",
    "deliverables/sample-request/validate_criteria.py": "48f3d0f1274b9635284571eed78405955c0e9aa57fa0ee8e57ce2fa955adbe45",
    "deliverables/sample-request/validate_criteria_v2.py": "b582f32737eb5733f6be883c3e08b0ce9423408bb7249caa3b7c32d12011719b",
    "sources/brief.md": "a78aca77135c5e533b8000272558b5b65e40ee421d1913cab961d7adc4cf5324",
    "sources/controlled-evaluation-answers.md": "87cf7eec2d97fdd994d338054b578c330b0c69253fdfe4b540bd45d3952f6e30",
    "sources/reference-observations.md": "d0862d144da0c4b315af96a8129846b32075fac99826b618ad51c62b6a960495",
    "reference.png": "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7",
    "reference-b.png": "e76b40ce38aeb436d0f5f0e433c4ac1eb4519bf93a7b29cd7a81a4609914a12a",
    "work/rev12.px": "f6b2c25456d1abbc49bf4e6f6d1305749bf2e0b105738428f066f14b3070e632",
}
LISTED_IN_NOTE = ["work/build_rev13.py", "work/verify_rev13.py", SNAPSHOT]
HANDOFF_8_FO = ["s_continuation_7", "s_continuation_6", "s_sample_brief_v2",
                "s_sample_request_review_v2", "s_sample_criteria", "s_sample_brief",
                "s_sample_request_review", "s_eval_answers", "c_sample", "f_sample", "i_alpha",
                "i_animation", "i_backgrounds", "i_canvas", "i_design_language", "i_display_scale",
                "i_engine", "i_lighting", "i_outline", "i_palette", "i_role_diff", "i_sampling",
                "x_aid", "x_study"]
FO = ["s_continuation_8"] + HANDOFF_8_FO


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(*args):
    return json.loads(subprocess.run([PY, RUNNER, *args], capture_output=True, text=True,
                                     check=True, encoding="utf-8").stdout)


problems = []
doc = run("decode", STATE)
by = {r["id"]: r for r in doc["records"]}
old = {r["id"]: r for r in json.load(open("work/rev12.json", encoding="utf-8"))["records"]}
if doc["revision"] != 13:
    problems.append(f"revision {doc['revision']} != 13")
if len(by) != 84:
    problems.append(f"{len(by)} records != 84")
if len(old) != 82:
    problems.append(f"work/rev12.json holds {len(old)} records != 82")
for rid, rec in old.items():
    if by.get(rid) != rec:
        problems.append(f"{rid} changed but should be untouched")
if set(by) - set(old) != {"s_continuation_8", "handoff_9"}:
    problems.append(f"unexpected new records: {sorted(set(by) - set(old))}")
if [r["$ref"] for r in old["handoff_8"]["fields"]["fo"]] != HANDOFF_8_FO:
    problems.append("handoff_8.fo in work/rev12.json differs from the recorded list")

f = by.get("s_continuation_8", {}).get("fields")
if not f:
    problems.append("missing s_continuation_8")
else:
    if f["ur"] != NOTE or f["dg"] != sha(NOTE):
        problems.append("s_continuation_8 digest/path mismatch")
    if f["ln"] != [1, open(NOTE, "rb").read().count(b"\n")]:
        problems.append("s_continuation_8 line range mismatch")
    if f["at"] != "2026-11-15" or f["au"] != {"$symbol": "local"}:
        problems.append("s_continuation_8 at/au differ from the plan")
for path, want in RETAINED.items():
    if sha(path) != want:
        problems.append(f"retained file drifted: {path}")
n = by.get("handoff_9", {}).get("fields")
if not n:
    problems.append("missing handoff_9")
elif n["rv"] != 13 or n["nx"] != [{"$ref": "t_sample"}] or \
        n["bl"] != [{"$ref": x} for x in ("t_scout", "t_medic", "t_family")] or \
        n["fo"] != [{"$ref": x} for x in FO] or n["wh"] != {"$ref": "actor"}:
    problems.append("handoff_9 fields differ from the plan")

note = open(NOTE, encoding="utf-8").read()
for path in LISTED_IN_NOTE:
    if sha(path) not in note:
        problems.append(f"note lacks sha256 of {path}")
if STATE == "state.px/state.px" and sha(STATE) in note:
    problems.append("note contains the revision 13 hash, which binds the note's own digest")

for line in open(SNAPSHOT, encoding="utf-8"):
    want, path = line.rstrip("\n").split("  ", 1)
    if path in EDITED_ON_PURPOSE:
        continue
    try:
        got = sha(path)
    except FileNotFoundError:
        problems.append(f"snapshot file missing: {path}")
        continue
    if got != want:
        problems.append(f"protected file drifted: {path}")

before = sha("deliverables/sample-request/criteria-schema-validation.json")
subprocess.run([PY, "-I", "deliverables/sample-request/validate_criteria_v2.py"],
               capture_output=True, text=True, check=True)
if sha("deliverables/sample-request/criteria-schema-validation.json") != before:
    problems.append("validate_criteria_v2.py modified the retained validation artifact")

wf = run("workflow", STATE, "--root", ".")
if wf.get("ready") != ["t_sample"]:
    problems.append(f"ready {wf.get('ready')}")
if not wf.get("files_verified"):
    problems.append("files not verified")
if run("jobs", STATE, "--root", ".").get("jobs"):
    problems.append("unexpected jobs")

print(json.dumps({"state": STATE, "head_sha256": sha(STATE), "canonical_hash": wf.get("hash"),
                  "revision": doc["revision"], "records": len(by), "problems": problems}, indent=1))
sys.exit(1 if problems else 0)
