"""Reproducible checks for revision 11 (2026-11-15e). Read-only.

1. The head decodes as revision 11 with exactly the 76 revision 10 records unchanged (compared
   with work/rev10.json) plus s_sample_brief_v2, s_sample_request_review_v2, s_continuation_6,
   handoff_7.
2. Each new S digest/line range equals the current file bytes; the v1 packet files and the
   retained validation artifact still match the hashes quoted in revision 10.
3. handoff_7 has rv 11, nx [t_sample], bl [t_scout, t_medic, t_family].
4. The e note quotes the sha256 of every new file it lists.
5. Runner `workflow` on the head reports ready [t_sample], no jobs, files verified.
6. Running validate_criteria_v2.py (print-only) leaves criteria-schema-validation.json unchanged.

Run from the consumer root with the selected interpreter:
  python -I work/verify_rev11.py [path-to-state, default state.px/state.px]
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
STATE = sys.argv[1] if len(sys.argv) > 1 else "state.px/state.px"
NOTE = "deliverables/continuation-2026-11-15e.md"
NEW_SOURCES = {
    "s_sample_brief_v2": "deliverables/sample-request/sample-creative-brief-v2.json",
    "s_sample_request_review_v2": "deliverables/sample-request/request-review-v2.json",
    "s_continuation_6": NOTE,
}
RETAINED = {
    "deliverables/sample-request/sample-creative-brief.json": "cc21bf77519ed46e7a6f634718efcc79816a8f9895cc4ece4e89b007bf7380ce",
    "deliverables/sample-request/sample-criteria.json": "14c979ea9bbfb686f7a9c693d552facfac5a135c45c3184d969611116611834b",
    "deliverables/sample-request/request-review.json": "ffa933ede2b985eafd4c616e83b4a69d0b34a99002a731439704dcd0d781e78b",
    "deliverables/sample-request/criteria-schema-validation.json": "93643a34d32353b5471fd9943aed8bb3a0bf8cb48a94d8413c42635a1aaeb16a",
    "deliverables/sample-request/validate_criteria.py": "48f3d0f1274b9635284571eed78405955c0e9aa57fa0ee8e57ce2fa955adbe45",
    "deliverables/continuation-2026-11-15d.md": "826460e5ff96f7dae2bccff8b8df1278e5457614cfaadd3c0510e0f64feeb1dc",
}
LISTED_IN_NOTE = [
    "deliverables/sample-request/sample-creative-brief-v2.json",
    "deliverables/sample-request/request-review-v2.json",
    "deliverables/sample-request/request-review-v2-tool-refusal.json",
    "deliverables/sample-request/validate_criteria_v2.py",
    "work/sample-checks/criteria-validation-rerun-v2.json",
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(*args):
    return json.loads(subprocess.run([PY, RUNNER, *args], capture_output=True, text=True,
                                     check=True, encoding="utf-8").stdout)


problems = []
doc = run("decode", STATE)
by = {r["id"]: r for r in doc["records"]}
old = {r["id"]: r for r in json.load(open("work/rev10.json", encoding="utf-8"))["records"]}
if doc["revision"] != 11:
    problems.append(f"revision {doc['revision']} != 11")
if len(by) != 80:
    problems.append(f"{len(by)} records != 80")
for rid, rec in old.items():
    if by.get(rid) != rec:
        problems.append(f"{rid} changed but should be untouched")
for sid, path in NEW_SOURCES.items():
    f = by.get(sid, {}).get("fields")
    if not f:
        problems.append(f"missing {sid}")
        continue
    if f["ur"] != path or f["dg"] != sha(path):
        problems.append(f"{sid} digest/path mismatch")
    if f["ln"] != [1, open(path, "rb").read().count(b"\n")]:
        problems.append(f"{sid} line range mismatch")
for path, want in RETAINED.items():
    if sha(path) != want:
        problems.append(f"retained file drifted: {path}")
n = by.get("handoff_7", {}).get("fields")
if not n:
    problems.append("missing handoff_7")
elif n["rv"] != 11 or n["nx"] != [{"$ref": "t_sample"}] or \
        n["bl"] != [{"$ref": x} for x in ("t_scout", "t_medic", "t_family")]:
    problems.append("handoff_7 fields differ from the plan")

note = open(NOTE, encoding="utf-8").read()
for path in LISTED_IN_NOTE:
    if sha(path) not in note:
        problems.append(f"note lacks sha256 of {path}")

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
