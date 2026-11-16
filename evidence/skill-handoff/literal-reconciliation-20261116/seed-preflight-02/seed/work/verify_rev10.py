"""Reproducible checks for revision 10 (2026-11-15d). Read-only.

1. The head decodes as revision 10 with exactly the 71 revision 9 records unchanged
   (compared with work/rev9.json, which the caller verified identical to the revision 9 head)
   plus s_sample_brief, s_sample_criteria, s_sample_request_review, s_continuation_5, handoff_6.
2. Each new S digest/line range equals the current file bytes.
3. handoff_6 has rv 10, nx [t_sample], bl [t_scout, t_medic, t_family].
4. The continuation note quotes the sha256 of every packet file and harness file it lists.
5. Runner `workflow` on the head reports ready [t_sample], no jobs, files verified.

Run from the consumer root with the selected interpreter:
  python -I work/verify_rev10.py [path-to-state, default state.px/state.px]
"""
import hashlib, json, subprocess, sys

PY = sys.executable
RUNNER = "pixl-kit/scripts/pixl.py"
STATE = sys.argv[1] if len(sys.argv) > 1 else "state.px/state.px"
NOTE = "deliverables/continuation-2026-11-15d.md"
NEW_SOURCES = {
    "s_sample_brief": "deliverables/sample-request/sample-creative-brief.json",
    "s_sample_criteria": "deliverables/sample-request/sample-criteria.json",
    "s_sample_request_review": "deliverables/sample-request/request-review.json",
    "s_continuation_5": NOTE,
}
LISTED_IN_NOTE = [
    "deliverables/sample-request/sample-creative-brief.json",
    "deliverables/sample-request/sample-criteria.json",
    "deliverables/sample-request/request-review.json",
    "deliverables/sample-request/operation-shortlist.json",
    "deliverables/sample-request/criteria-schema-validation.json",
    "deliverables/sample-request/request-review-tool-refusal.json",
    "deliverables/sample-request/validate_criteria.py",
    "work/sample-checks/check_sample_mechanical.py",
    "work/sample-checks/make_fixtures.py",
    "work/sample-checks/aggregate_dry_run.py",
    "work/sample-checks/dry-run.json",
    "work/sample-checks/fixture-33x33.png",
    "work/sample-checks/fixture-offpalette.png",
    "work/sample-checks/fixture-fractional-alpha.png",
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(*args):
    return json.loads(subprocess.run([PY, RUNNER, *args], capture_output=True, text=True,
                                     check=True, encoding="utf-8").stdout)


problems = []
doc = run("decode", STATE)
by = {r["id"]: r for r in doc["records"]}
old = {r["id"]: r for r in json.load(open("work/rev9.json", encoding="utf-8"))["records"]}
if doc["revision"] != 10:
    problems.append(f"revision {doc['revision']} != 10")
if len(by) != 76:
    problems.append(f"{len(by)} records != 76")
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
n = by.get("handoff_6", {}).get("fields")
if not n:
    problems.append("missing handoff_6")
else:
    if n["rv"] != 10 or n["nx"] != [{"$ref": "t_sample"}] or \
            n["bl"] != [{"$ref": x} for x in ("t_scout", "t_medic", "t_family")]:
        problems.append("handoff_6 fields differ from the plan")
    for want in ("s_continuation_5", "s_sample_brief", "s_sample_criteria", "s_sample_request_review"):
        if {"$ref": want} not in n["fo"]:
            problems.append(f"handoff_6.fo lacks {want}")

note = open(NOTE, encoding="utf-8").read()
for path in LISTED_IN_NOTE:
    if sha(path) not in note:
        problems.append(f"note lacks sha256 of {path}")

wf = run("workflow", STATE, "--root", ".")
if wf.get("ready") != ["t_sample"]:
    problems.append(f"ready {wf.get('ready')}")
if not wf.get("files_verified"):
    problems.append("files not verified")
jobs = run("jobs", STATE, "--root", ".")
if jobs.get("jobs"):
    problems.append("unexpected jobs")

print(json.dumps({"state": STATE, "head_sha256": sha(STATE), "canonical_hash": wf.get("hash"),
                  "revision": doc["revision"], "records": len(by), "problems": problems}, indent=1))
sys.exit(1 if problems else 0)
