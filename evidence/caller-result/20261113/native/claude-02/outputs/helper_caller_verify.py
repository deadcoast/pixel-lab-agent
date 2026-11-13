"""Parent caller verification: read every saved result completely, verify all path/sha256 references and the probe records.
Read-only except writing caller-verify-02.json (fresh)."""
import hashlib, json, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
w = root / "work/compact-caller"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


report = {"checks": [], "failures": []}


def check(ok, msg):
    report["checks"].append({"ok": bool(ok), "check": msg})
    if not ok:
        report["failures"].append(msg)


REF_KEYS = {"path", "sha256", "role", "start", "end", "bytes", "json_pointer"}


def walk(obj, where, acc):
    if isinstance(obj, dict):
        if {"path", "sha256"} <= set(obj) <= REF_KEYS and isinstance(obj.get("sha256"), str) and len(obj["sha256"]) == 64:
            acc.append((where, obj["path"], obj["sha256"]))
        for k, v in obj.items():
            walk(v, where + "/" + str(k), acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, where + "/" + str(i), acc)


def verify_refs(rel):
    doc = json.loads((root / rel).read_text("utf-8"))
    acc = []
    walk(doc, rel, acc)
    for where, p, h in acc:
        f = root / p
        check(f.is_file() and sha(f) == h, where + ": " + p + " sha256 matches")
    return doc, len(acc)


cr, n = verify_refs("work/compact-caller/CALLER-RESULT.json")
check(n >= 15, "CALLER-RESULT references verified: %d" % n)
check(len((w / "CALLER-RESULT.json").read_bytes()) <= 8192, "CALLER-RESULT.json <= 8192 UTF-8 bytes")
for k in ["native_child", "compact", "receipt", "parent_receipt", "details_read", "resume_read", "refresh", "specialist_result",
          "errors", "unknown_recovery", "stale_recovery", "same_snapshot", "assignment_status", "production_next",
          "unknown_job_id", "unknown_job_state", "scope", "unresolved", "next_action"]:
    check(k in cr, "CALLER-RESULT has field " + k)
check(set(cr["errors"]) == {"invalid_authoring", "stale_local_state", "unavailable_observation", "uncertain_remote_result", "missing_capability"},
      "five error categories present")
sr, n = verify_refs("work/compact-caller/SPECIALIST-RESULT.json")
check(n >= 6, "SPECIALIST-RESULT references verified: %d" % n)
check(sr["status"] == "partial" and sr["native_child"]["agent_id"] == "ab352c80d7f534aae", "specialist result partial, actual child id")

compact = json.loads((w / "compact.json").read_text("utf-8"))
receipt = json.loads((w / "receipt.json").read_text("utf-8"))
parent = json.loads((w / "parent-receipt.json").read_text("utf-8"))
snap = root / compact["path"]
check(compact["sha256"] == receipt["sha256"] == parent["sha256"] == sha(snap), "compact, receipt and parent receipt name the same snapshot bytes")
for k in ("asset_id", "requirements_hash", "state_hash", "next", "scope", "path"):
    check(compact[k] == receipt[k] == parent[k], "receipt field identical: " + k)
hand = json.loads(snap.read_text("utf-8"))
details = json.loads((w / "details.json").read_text("utf-8"))
check(hand["details"] == details, "handoff /details equals details.json")
lines = snap.read_text("utf-8").split("\n")
for name in ("details", "resume"):
    r = json.loads((w / (name + "-read.json")).read_text("utf-8"))
    ref = compact[name + "_ref"]
    phys = "\n".join(lines[ref["start"] - 1:ref["end"]]) + "\n"
    check(r["text"] == phys and len(r["text"].encode("utf-8")) == ref["bytes"] == r["bytes"] and r["sha256"] == ref["sha256"],
          name + "-read exact slice, bytes and hash match locator")
    check(r["text"].rstrip("\n").endswith(","), name + "-read trailing member comma preserved")
    member = json.loads("{" + r["text"].rstrip("\n").rstrip(",") + "}")
    check(member[name] == hand[name], name + "-read parses to handoff " + ref["json_pointer"])

refresh = json.loads((w / "refresh.json").read_text("utf-8"))
cont = refresh["production"]["continuation"]
check(cont["state_hash"] == compact["state_hash"] and refresh["requirements_hash"] == compact["requirements_hash"]
      and cont["store"] == compact["store"] and cont["action"] == compact["next"], "refresh identities equal compact identities")
check(refresh["production"]["pending_jobs"] == [] and refresh["production"]["revision"] == 108, "refresh: no pending jobs, revision 108")
stale = json.loads((w / "stale-recovery.json").read_text("utf-8"))
check(stale["production"]["continuation"]["state_hash"] == compact["state_hash"], "stale-recovery read matches compact state hash")

exp = {"invalid-authoring": ("caller_result_input", "invalid_authoring"), "stale-state": ("handoff_stale", "stale_local_state"),
       "unavailable-observation": ("operation", "unavailable_observation"), "uncertain-remote": ("job_history", "uncertain_remote_result"),
       "missing-capability": ("unknown_tool", "missing_capability")}
for name, (code, cat) in exp.items():
    e = json.loads((w / "errors" / (name + ".json")).read_text("utf-8"))
    check(e["original_error"]["error"] == code and e["original_error"]["category"] == cat and e["derived"]["category"] == cat,
          "errors/" + name + ".json retains original code " + code + " and category " + cat)
proto = [json.loads(l) for l in (w / "missing-capability-protocol.jsonl").read_text("utf-8").splitlines() if l.strip()]
check(proto[1]["result"]["isError"] is True and proto[1]["result"]["structuredContent"]["error"] == "unknown_tool",
      "missing-capability raw protocol retains isError unknown_tool")
check("pixl_missing_capability_probe" not in {t["name"] for t in proto[0]["result"]["tools"]}, "tools/list lacks the probed tool")
ur = json.loads((w / "unknown-recovery.json").read_text("utf-8"))
pre = json.loads((w / "unknown-jobs-precheck.json").read_text("utf-8"))
check(ur["result"] == pre and ur["result"]["jobs"][0]["state"] == "unknown"
      and ur["result"]["hash"] == "3ab0c1633edbf21977744bab59eb2a15b2cd8dc81424ea3cfe6c569d5f35e0a9" and len(ur["result"]["jobs"][0]["events"]) == 1,
      "unknown job unchanged before/after rejected duplicate dispatch")
check(not (w / "intentionally-missing.txt").exists(), "intentionally-missing.txt not created")

preserved = {"compact.json": "ff5c2289915ce12c26cc69073759f6254e154d341a631465d262ff8720900687",
             "details.json": "92682b133f09898b20e620fd0e9aea94f2aad3b5aae511f2ceec9defa87a3dc2",
             "SPECIALIST-REPORT.json": "7390a062f174405010b9472c952bb7948aa7748684220bb3682650e700c9f303",
             "specialist-plar-read.json": "3dccfd43851c41b036281bf4def05789a50791c91c28dd2b19c778d4b2ff34f2"}
for f, h in preserved.items():
    check(sha(w / f) == h, "session-1 file preserved: " + f)
prior = {"work/artistic-revision/SPECIALIST-RESULT.json": "e65ee7d76927a5ea1226d56565f860fae35fb24767d5a3e6c2034a13a4222a4c",
         "work/artistic-revision/CALLER-RESULT.json": "f5f13234e9c735256a890bd5023fa8b95a641181d6feb77b1381600d89e46821",
         "assets/working.png": "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc",
         ".pixl/handoffs/e560a32dcaf31134abbb81b661a0a2fc12824461a049c90b1c780cc01464273d.json": "e560a32dcaf31134abbb81b661a0a2fc12824461a049c90b1c780cc01464273d"}
for f, h in prior.items():
    check(sha(root / f) == h, "prior file preserved: " + f)
check(len(list((root / ".pixl/handoffs").iterdir())) == 11, "handoff directory still 11 files (no new snapshot this session)")

report["summary"] = {"checks": len(report["checks"]), "failures": len(report["failures"])}
out = w / "caller-verify-02.json"
if out.exists():
    raise SystemExit("caller-verify-02.json exists")
out.write_text(json.dumps(report, indent=1), encoding="utf-8")
print(json.dumps(report["summary"]))
print("\n".join(report["failures"]) or "no failures")
