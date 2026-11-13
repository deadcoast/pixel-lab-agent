"""Parent verification for revision-03: read the complete new caller result, new specialist result and new error,
verify every path/sha256 reference, the three-view snapshot identity, defect evidence and preservation.
Writes only revision-03/caller-verify-03c.json (fresh)."""
import hashlib, json, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
w = root / "work/compact-caller"
r3 = w / "revision-03"
report = {"checks": [], "failures": []}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


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


cr, n = verify_refs("work/compact-caller/revision-03/CALLER-RESULT.json")
check(n >= 25, "revision-03 CALLER-RESULT references verified: %d" % n)
check(len((r3 / "CALLER-RESULT.json").read_bytes()) < 8192, "revision-03 CALLER-RESULT.json < 8192 UTF-8 bytes")
prior = json.loads((w / "CALLER-RESULT.json").read_text("utf-8"))
for k in prior:
    check(k in cr, "carried forward field: " + k)
for k in ("receipt", "parent_receipt", "details_read", "resume_read", "refresh", "specialist_report", "details",
          "unknown_recovery", "stale_recovery", "missing_capability_protocol", "source_reads_protocol", "identities",
          "locator_reads", "production_delivery", "probes", "scope", "unresolved", "next_action"):
    check(cr[k] == prior[k] or k == "locator_reads", "retained unchanged from prior report: " + k)
for k in ("invalid_authoring", "stale_local_state", "uncertain_remote_result", "missing_capability"):
    check(cr["errors"][k] == prior["errors"][k], "retained error report: " + k)
check(cr["errors"]["unavailable_observation"]["path"] == "work/compact-caller/revision-03/errors/unavailable-observation.json", "unavailable_observation points to fresh capture")
check(cr["native_child"]["agent_id"] == "ab352c80d7f534aae" and cr["native_child"]["first_child"]["agent_id"] == "ac98550e535c93d5a", "native_child distinguishes first and latest child")
check(cr["compact"]["path"] == "work/compact-caller/revision-03/compact.json" and cr["specialist_result"]["path"] == "work/compact-caller/revision-03/SPECIALIST-RESULT.json", "compact and specialist_result point to revision-03 files")

sr, n = verify_refs("work/compact-caller/revision-03/SPECIALIST-RESULT.json")
check(n >= 10, "revision-03 SPECIALIST-RESULT references verified: %d" % n)
check(sr["native_child"]["agent_id"] == "ab352c80d7f534aae" and sr["native_child"]["publication_provenance"]["original_caller_view"]["published_by"].endswith("ac98550e535c93d5a"), "specialist result records provenance")
check(sr["status"] == "partial" and "reconciliation_note" in sr, "specialist result partial with reconciliation note")

compact = json.loads((r3 / "compact.json").read_text("utf-8"))
receipt = json.loads((w / "receipt.json").read_text("utf-8"))
parent = json.loads((w / "parent-receipt.json").read_text("utf-8"))
snap = root / compact["path"]
check(compact["sha256"] == receipt["sha256"] == parent["sha256"] == sha(snap) == cr["snapshot"]["sha256"], "three views name identical immutable snapshot bytes")
for k in ("asset_id", "requirements_hash", "state_hash", "next", "path"):
    check(compact[k] == receipt[k] == parent[k], "view field identical: " + k)
check(sha(r3 / "compact.json") == sha(w / "compact.json"), "revision-03 caller view byte-identical to first child's publication")
hand = json.loads(snap.read_text("utf-8"))
check(hand["details"] == json.loads((w / "details.json").read_text("utf-8")), "handoff /details equals details.json")
plar = json.loads((r3 / "specialist-plar-read-03.json").read_text("utf-8"))
check(plar["production"]["continuation"]["state_hash"] == compact["state_hash"] and plar["requirements_hash"] == compact["requirements_hash"] and plar["production"]["revision"] == 108, "fresh PLAR read identities current")

err = json.loads((r3 / "errors/unavailable-observation.json").read_text("utf-8"))
native = err["structuredContent"]
host = json.loads((r3 / "host-unavailable-return-02.json").read_text("utf-8"))
old = json.loads((w / "errors/unavailable-observation.json").read_text("utf-8"))["original_error"]
sep = chr(92)
check(err["isError"] is True and native["error"] == "operation" and native["category"] == "unavailable_observation", "fresh error retains native code and category")
check(host == native, "host MCP return equals frozen-kit native error exactly")
check(native["detail"].count(sep) == 20 and old["detail"].count(sep) == 10 and old != native, "prior report collapse defect demonstrated against native")
proto = [json.loads(l) for l in (r3 / "unavailable-protocol.jsonl").read_text("utf-8").splitlines() if l.strip()]
check(next(x for x in proto if x.get("id") == 2)["result"] == err, "raw protocol result equals saved error file")
check(not (w / "intentionally-missing.txt").exists(), "intentionally-missing.txt not created")
check(json.loads((r3 / "unknown-jobs-check.json").read_text("utf-8"))["jobs"][0]["state"] == "unknown", "fixture member.job still unknown (read only)")

preserved = {"CALLER-RESULT.json": prior and sha(w / "CALLER-RESULT.json"), "compact.json": "ff5c2289915ce12c26cc69073759f6254e154d341a631465d262ff8720900687",
             "details.json": "92682b133f09898b20e620fd0e9aea94f2aad3b5aae511f2ceec9defa87a3dc2", "SPECIALIST-REPORT.json": "7390a062f174405010b9472c952bb7948aa7748684220bb3682650e700c9f303",
             "SPECIALIST-RESULT.json": "ce38956d5f3ddf73e0a5e543385fa5fde5fdc6a67d54f0895220ce809e734236", "receipt.json": "6878691886ac3ab0221a5f03fd7efea96f12e6ce32f7ccfdf437f90cdd33e0e3",
             "errors/unavailable-observation.json": "a68d928eb73964c22457f1fdf475f5c175ba6db3e6e1a098ea5d2cc2f463f50e"}
for f, h in preserved.items():
    if f != "CALLER-RESULT.json":
        check(sha(w / f) == h, "prior file preserved: " + f)
check(cr["supersedes"]["sha256"] == sha(w / "CALLER-RESULT.json"), "prior CALLER-RESULT.json preserved and referenced")
for f, h in {"assets/working.png": "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc",
             "work/artistic-revision/SPECIALIST-RESULT.json": "e65ee7d76927a5ea1226d56565f860fae35fb24767d5a3e6c2034a13a4222a4c"}.items():
    check(sha(root / f) == h, "original file preserved: " + f)
check(len(list((root / ".pixl/handoffs").iterdir())) == 11, "handoff directory still 11 files")
check((r3 / "CALLER-RESULT-attempt-01-oversize.json").is_file() and cr["historical"]["first_attempt_caller_result"]["sha256"] == sha(r3 / "CALLER-RESULT-attempt-01-oversize.json"), "oversize first attempt retained and referenced")
check((r3 / "CALLER-RESULT-attempt-02-oversize.json").is_file() and cr["historical"]["second_attempt_caller_result"]["sha256"] == sha(r3 / "CALLER-RESULT-attempt-02-oversize.json"), "oversize second attempt retained and referenced")
check("locator_reads" in cr and cr["locator_reads"]["details_ref"] == prior["locator_reads"]["details_ref"] and cr["locator_reads"]["resume_ref"] == prior["locator_reads"]["resume_ref"], "locator reads carried forward")
report["summary"] = {"checks": len(report["checks"]), "failures": len(report["failures"])}
out = r3 / "caller-verify-03c.json"
if out.exists():
    raise SystemExit("exists")
out.write_text(json.dumps(report, indent=1), encoding="utf-8")
print(json.dumps(report["summary"]))
print("\n".join(report["failures"]) or "no failures")
