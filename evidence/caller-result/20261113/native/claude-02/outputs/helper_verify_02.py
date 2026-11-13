"""Second-session verification of the existing work/compact-caller outputs.

Read-only: hashes cited files, checks the retained details/report/compact/handoff
against each other and against the fresh tool returns saved in this directory.
Run with: python -I -B helper_verify_02.py <consumer-root>
"""
import hashlib
import json
import os
import sys

ROOT = sys.argv[1]


def rd(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return f.read()


def sha(rel):
    return hashlib.sha256(rd(rel)).hexdigest()


def jl(rel):
    return json.loads(rd(rel).decode("utf-8"))


problems = []
checked = 0


def check(cond, msg):
    global checked
    checked += 1
    if not cond:
        problems.append(msg)


def walk_refs(obj, where):
    """Verify every {path, sha256} pair found anywhere in obj."""
    n = 0
    if isinstance(obj, dict):
        if "path" in obj and "sha256" in obj and isinstance(obj["path"], str) and isinstance(obj["sha256"], str):
            p = obj["path"]
            if not os.path.isabs(p) and os.path.exists(os.path.join(ROOT, p)):
                check(sha(p) == obj["sha256"], f"{where}: hash mismatch for {p}")
                n += 1
            elif not os.path.isabs(p):
                problems.append(f"{where}: cited file missing {p}")
        for k, v in obj.items():
            n += walk_refs(v, where + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            n += walk_refs(v, f"{where}[{i}]")
    return n


details = jl("work/compact-caller/details.json")
report = jl("work/compact-caller/SPECIALIST-REPORT.json")
compact = jl("work/compact-caller/compact.json")
prior_spec = jl("work/artistic-revision/SPECIALIST-RESULT.json")
plar = jl("work/compact-caller/specialist-plar-read.json")
unknown = jl("work/compact-caller/specialist-unknown-jobs.json")
rr02 = jl("work/artistic-revision/request-review-02.json")

print("refs verified in details.json:", walk_refs(details, "details"))
print("refs verified in SPECIALIST-REPORT.json:", walk_refs(report, "report"))
print("refs verified in compact.json:", walk_refs(compact, "compact"))

# details content rules
check(details["status"] == "partial", "details.status not partial")
check(details["retained_specialist_observations"] == prior_spec, "retained_specialist_observations != parsed SPECIALIST-RESULT.json")
caller = details["caller"]
cb = json.dumps(caller, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
print("caller block bytes:", len(cb), "summary chars:", len(caller["summary"]))
check(len(cb) <= 8192, "caller block > 8192 bytes")
check(len(caller["summary"]) <= 600, "summary > 600 chars")
check(len(caller["artifacts"]) <= 12 and len(caller["reports"]) <= 12 and len(caller["issues"]) <= 12, "caller list bounds")
cats = {"invalid_authoring", "stale_local_state", "missing_capability", "uncertain_remote_result", "unavailable_observation", "unfinished_work"}
for it in caller["issues"]:
    check(it["category"] in cats, f"bad issue category {it['category']}")
    check(len(it["summary"]) <= 600 and len(it.get("recovery", "")) <= 600, "issue text bound")
check(caller["integration"]["status"] in {"pass", "fail", "unavailable", "not_performed", "not_in_scope"}, "integration status")
for arr in (caller["artifacts"], caller["reports"], caller["integration"]["evidence"]):
    for ref in arr:
        check(set(ref.keys()) == {"path", "sha256", "role"}, f"ref keys {ref}")
        check("\\" not in ref["path"] and len(ref["role"]) <= 96, f"ref path/role {ref}")
check(details["detailed_report"]["sha256"] == sha("work/compact-caller/SPECIALIST-REPORT.json"), "details.detailed_report hash != current report")
check("caller_actions" in details and "future_work" in details, "caller_actions/future_work missing")
sep = details["separation"]
check(set(sep.keys()) == {"delivered_artistic_production", "partial_assignment", "historical_creation_acceptance", "stale_plan01", "controlled_unknown_job"}, "separation keys")

# compact.json vs handoff file
hp = compact["path"]
check(compact["sha256"] == sha(hp), "compact.sha256 != handoff file hash")
handoff = jl(hp)
print("handoff keys:", sorted(handoff.keys()))
check(handoff.get("details") == details, "handoff /details != details.json")
check(compact["view"] == "caller", "compact view")
check(compact["asset_id"] == "queue.working" and compact["requirements_hash"] == "ec61d688f752ac1280914d22ba75bdb4e8f7e31c42b18d7d62f7a14038eedea5" and compact["state_hash"] == "88d77c62b47eb8fef5d35015973f67b0f38731cb04e54430efa36aec4b898d64", "compact identities")
check(compact["details_ref"]["path"] == hp and compact["resume_ref"]["path"] == hp, "refs path")
check(compact["caller"]["present"] is True and compact["assignment"]["status"] == "partial", "compact caller/assignment")

# production facts from the fresh plar read
prod = plar["production"]
cont = prod["continuation"]
print("continuation:", json.dumps({k: cont[k] for k in cont if k not in ("delivery",)})[:900])
check(cont["action"] == "delivered" and cont["state_hash"] == compact["state_hash"] and cont["requirements_hash"] == plar["requirements_hash"], "continuation identity")
check(prod["revision"] == 108 and prod["task"] == "artistic-02.working.task" and prod["task_state"] == "done" and prod["store"] == ".pixl/assets/queue.ready", "production facts")
jobs = prod.get("jobs", [])
print("production.jobs:", json.dumps([{k: j.get(k) for k in ("id", "state", "remote_id", "next_action", "provider", "tool", "task")} for j in jobs]))
check(len(jobs) == 1 and jobs[0]["id"] == "authoring-01.working.join-01" and jobs[0]["state"] == "failed" and jobs[0]["next_action"] == "review_failure", "failed job facts")
check(prod.get("selection_current") is True or cont.get("selection_current") is True, "selection current")
check(plar["asset"]["id"] == "queue.working" and plar["path"] == "authoring-plar.txt", "plar identities")
d = cont["delivery"]
check(d["destination"] == "assets/working.png" and d["observed_sha256"] == "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc" and d["families"][0]["task"] == "artistic-02.delivery.task" and d["families"][0]["accepted"] is True and d["families"][0]["state"] == "done", "delivery facts")

# unknown fixture facts
uj = unknown["jobs"][0]
check(uj["id"] == "member.job" and uj["state"] == "unknown" and uj["remote_id"] is None and uj["next_action"] == "reconcile" and uj["request"]["provider"] == "fictional-fixture" and unknown["hash"] == "3ab0c1633edbf21977744bab59eb2a15b2cd8dc81424ea3cfe6c569d5f35e0a9" and unknown["revision"] == 9, "unknown job facts")

# stale plan diagnostic facts
print("rr02 plan:", rr02["plan"]["id"], "state:", json.dumps(rr02.get("state"))[:300])
check(rr02["plan"]["id"] == "artistic-01.plan", "rr02 plan id")
st = rr02.get("state") or {}
check(st.get("revision") == 92 and st.get("sha256") == report["stale_plan01"]["diagnostic_state"]["sha256"], "rr02 state rev/sha vs report")
check(os.path.exists(os.path.join(ROOT, rr02["plan"]["path"])) and sha(rr02["plan"]["path"]) == rr02["plan"]["sha256"], "plan01 file hash")

print("checks:", checked, "problems:", len(problems))
for p in problems:
    print("PROBLEM:", p)
