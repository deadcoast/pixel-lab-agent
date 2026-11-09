"""Independent verification of the work/export-review exports.

Usage: python -I verify-exports.py <project-root> <output-json>

Reads the compact summaries retained from actual tool/CLI output, re-reads the
exported files natively, recomputes bytes/SHA-256, parses them as UTF-8 JSON and
checks state/acceptance identities. Writes a verification JSON. Exit 1 on any
failed check. Does not call any publishing operation.
"""
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(sys.argv[1])
OUT = sys.argv[2]
PY = sys.executable
KIT = os.path.join(ROOT, ".agents", "skills", "export-kit", "scripts", "pixl.py")

EXPECTED_STATE_HASH = "23718b6d027836af49f3548fcb38979bd4afca032e8113d7a9222c7c570c8c49"
EXPECTED_REVISION = 126
EXPECTED_REVIEW_SHA = "59faea6482a769cc452444f1d94a5b85ff356ec7d0c558778738127861b81294"
EXPECTED_MANIFEST_SHA = "ec59b8245619463446cb86b639e7b387e748917fb5c520a085984b85c89df5d0"
EXPECTED_BINDING = "48752d9d65836801fde700b5f125e424cae21ee15c536628b5abde38740db443"
CREATION_SOURCE_STATE = "5c9c540938591271fd7ddf80ed9d591f3eb1b904c86f823776cb687317742a4a"
CREATION_RECEIPT_HASH = "a2134009ac25870515701eaaaaf61e23e20f1afe2024be66fe39cb8493a9d0b3"
# Hashes of the preserved prior files, as observed before any operation in this trial.
PRIOR = {
    "work/native-review/04-family-snapshot-result.json": "fed60d0be0d2a8e2aca13352cf9b41d8f93779ee058e09b64571dd61942c3e80",
    "work/native-review/04-family-snapshot-result.caller-corrected.json": "9fb2c38e9951160678088d9effca1975edbb2151bda470082b0e8005c1e30bcd",
    "work/export-review/identical-review.json": "fcb821d6ae755b7f471672a418050f233910e395d2bffd75463c733e263d878f",
    "work/native-review/07-family-review-request.json": "dba8d9abf0f5df615cb3f26912074275111e28b3d6b623b8ab532cf7d92bbf2b",
}

SUMMARIES = [
    ("mcp", "pixl_review_context", "work/export-review/01-family-review-context.mcp-summary.json"),
    ("mcp", "pixl_family", "work/export-review/02-family-report.mcp-summary.json"),
    ("cli", "candidate-review", "work/export-review/03-identical-review-cli-stdout.json"),
    ("cli", "review-context", "work/export-review/04-family-review-context-cli-stdout.json"),
    ("cli", "family", "work/export-review/05-family-report-cli-stdout.json"),
]

checks = []
report = {"root": ROOT, "python": PY, "exports": [], "checks": checks}


def rel(p):
    return os.path.join(ROOT, p.replace("/", os.sep))


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def read(p):
    with open(rel(p), "rb") as fh:
        return fh.read()


def check(name, ok, detail=None):
    checks.append({"check": name, "ok": bool(ok), "detail": detail})
    return ok


def load_json(p):
    return json.loads(read(p).decode("utf-8"))


# 1. Exported files match their returned summaries and parse as UTF-8 JSON.
parsed = {}
for interface, op, spath in SUMMARIES:
    summary = load_json(spath)
    target = summary["result_path"]
    data = read(target)
    entry = {
        "interface": interface,
        "operation": op,
        "summary_file": spath,
        "summary_sha256": sha_bytes(read(spath)),
        "result_path": target,
        "summary_sha256_claimed": summary["result_sha256"],
        "summary_bytes_claimed": summary["result_bytes"],
        "actual_sha256": sha_bytes(data),
        "actual_bytes": len(data),
        "result_saved": summary.get("result_saved"),
        "media_type": summary.get("media_type"),
    }
    try:
        parsed[target] = json.loads(data.decode("utf-8"))
        entry["parses_as_utf8_json"] = True
    except Exception as exc:  # noqa: BLE001
        entry["parses_as_utf8_json"] = False
        entry["parse_error"] = repr(exc)
    entry["sha256_matches"] = entry["actual_sha256"] == entry["summary_sha256_claimed"]
    entry["bytes_match"] = entry["actual_bytes"] == entry["summary_bytes_claimed"]
    report["exports"].append(entry)
    check(f"{target}: result_saved", summary.get("result_saved") is True)
    check(f"{target}: sha256 matches summary", entry["sha256_matches"], entry["actual_sha256"])
    check(f"{target}: bytes match summary", entry["bytes_match"], entry["actual_bytes"])
    check(f"{target}: parses as UTF-8 JSON", entry["parses_as_utf8_json"], entry.get("parse_error"))
    if "state_hash" in summary:
        check(f"{spath}: summary state_hash", summary["state_hash"] == EXPECTED_STATE_HASH, summary["state_hash"])
    if "hash" in summary:
        check(f"{spath}: summary hash", summary["hash"] == EXPECTED_STATE_HASH, summary["hash"])
    check(f"{spath}: summary revision", summary.get("revision") == EXPECTED_REVISION, summary.get("revision"))

ctx = parsed["work/export-review/01-family-review-context.json"]
ctx_cli = parsed["work/export-review/04-family-review-context-cli.json"]
fam = parsed["work/export-review/02-family-report.json"]
fam_cli = parsed["work/export-review/05-family-report-cli.json"]
replay = parsed["work/export-review/03-identical-review-result.json"]

check("MCP and CLI review-context exports are byte-identical",
      read("work/export-review/01-family-review-context.json") == read("work/export-review/04-family-review-context-cli.json"))
check("MCP and CLI family exports are byte-identical",
      read("work/export-review/02-family-report.json") == read("work/export-review/05-family-report-cli.json"))

# 2. Review context identities and acceptance.
report["review_context"] = {
    "state_hash": ctx.get("state_hash"),
    "revision": ctx.get("revision"),
    "binding_hash": ctx.get("binding_hash"),
    "candidate": ctx.get("candidate"),
    "candidate_file": ctx.get("candidate_file"),
    "output": ctx.get("output"),
    "task": ctx.get("task"),
    "task_status": ctx.get("task_status"),
    "nominated": ctx.get("nominated"),
    "current_acceptance": ctx.get("current_acceptance"),
    "snapshot_acceptance": ctx.get("snapshot_acceptance"),
    "criteria": [
        {k: c.get(k) for k in ("id", "status", "verdict", "mode", "required") if k in c}
        for c in ctx.get("criteria", [])
    ],
    "top_level_keys": sorted(ctx.keys()),
}
check("context: state_hash", ctx.get("state_hash") == EXPECTED_STATE_HASH, ctx.get("state_hash"))
check("context: revision", ctx.get("revision") == EXPECTED_REVISION, ctx.get("revision"))
check("context: binding_hash", ctx.get("binding_hash") == EXPECTED_BINDING, ctx.get("binding_hash"))
check("context: candidate manifest sha", (ctx.get("candidate_file") or {}).get("sha256") == EXPECTED_MANIFEST_SHA)
check("context: task done", ctx.get("task_status") == "done", ctx.get("task_status"))
check("context: nominated", ctx.get("nominated") is True, ctx.get("nominated"))
ca = ctx.get("current_acceptance") or {}
check("context: current_acceptance all_required_pass", ca.get("all_required_pass") is True, ca)
check("context: current_acceptance task_complete", ca.get("task_complete") is True, ca)
sa = ctx.get("snapshot_acceptance") or {}
check("context: snapshot_acceptance.accepted stays false (creation status)", sa.get("accepted") is False, sa)
check("context: snapshot source_state_hash is the creation-time state", sa.get("source_state_hash") == CREATION_SOURCE_STATE, sa)
crit = ctx.get("criteria", [])
check("context: three collective criteria", len(crit) == 3, len(crit))
check("context: all criteria pass", all(c.get("status") == "pass" for c in crit), [c.get("status") for c in crit])
check("context: verdict ids are native-review.family.collective.verdict.0/1/2",
      sorted(c.get("verdict") for c in crit) == [f"native-review.family.collective.verdict.{i}" for i in range(3)],
      [c.get("verdict") for c in crit])

# 3. Family report: creation vs current acceptance.
families = fam.get("families", [])
family = next((f for f in families if f.get("output") == "provenance-correction.delivery.output"), None)
check("family report: hash", fam.get("hash") == EXPECTED_STATE_HASH, fam.get("hash"))
check("family report: revision", fam.get("revision") == EXPECTED_REVISION, fam.get("revision"))
check("family report: files_verified", fam.get("files_verified") is True, fam.get("files_verified"))
check("family report: contains provenance-correction.delivery.output", family is not None)
if family:
    snaps = family.get("snapshots", [])
    cands = family.get("candidates", [])
    fam_summary = {
        "output": family.get("output"),
        "task": family.get("task"),
        "state": family.get("state"),
        "candidate": family.get("candidate"),
        "blockers": family.get("blockers"),
        "snapshot_blockers": family.get("snapshot_blockers"),
        "pending_jobs": family.get("pending_jobs"),
        "members": [
            {"output": m.get("output"), "candidate": m.get("candidate"), "state": m.get("state"), "accepted": m.get("accepted")}
            for m in family.get("members", [])
        ],
        "candidates": [
            {k: c.get(k) for k in c if k != "requirements"} | {
                "requirements": [{kk: r.get(kk) for kk in ("id", "status", "verdict")} for r in c.get("requirements", [])]
            }
            for c in cands
        ],
        "snapshots": snaps,
        "requirements": [{kk: r.get(kk) for kk in ("id", "status", "verdict")} for r in family.get("requirements", [])],
    }
    report["family"] = fam_summary
    check("family: task state done", family.get("state") == "done", family.get("state"))
    check("family: pending_jobs empty", not family.get("pending_jobs"), family.get("pending_jobs"))
    check("family: blockers empty", not family.get("blockers"), family.get("blockers"))
    check("family: all collective requirements pass",
          family.get("requirements") and all(r.get("status") == "pass" for r in family.get("requirements", [])),
          [r.get("status") for r in family.get("requirements", [])])
    check("family: all members accepted", all(m.get("accepted") is True for m in family.get("members", [])),
          [(m.get("candidate"), m.get("accepted")) for m in family.get("members", [])])
    snap = next((s for s in snaps if s.get("candidate") == "native-review.family.candidate"), None)
    check("family: native-review.family.candidate snapshot listed", snap is not None, snaps)
    if snap:
        check("family: snapshot retention_is_acceptance is false (creation status, not current acceptance)",
              snap.get("retention_is_acceptance") is False, snap.get("retention_is_acceptance"))
        check("family: snapshot source_state_sha256 is the creation-time state",
              snap.get("source_state_sha256") == CREATION_SOURCE_STATE, snap.get("source_state_sha256"))
        check("family: snapshot manifest sha", snap.get("sha256") == EXPECTED_MANIFEST_SHA, snap.get("sha256"))
        check("family: snapshot not stale", snap.get("stale") == [], snap.get("stale"))
        check("family: snapshot member hashes equal context members",
              [f.get("sha256") for f in snap.get("files", [])] == [m.get("sha256") for m in ctx.get("members", [])],
              [f.get("sha256") for f in snap.get("files", [])])
    cand = next((c for c in cands if c.get("id") == "native-review.family.candidate"), None)
    check("family: native-review.family.candidate listed as current candidate", cand is not None)
    if cand:
        check("family: current candidate nominated", cand.get("nominated") is True, cand.get("nominated"))

# 4. Replay result: reused review, zero publications, identities unchanged.
report["replay"] = {k: replay.get(k) for k in (
    "review", "review_sha256", "review_path", "reused_review", "publications", "remote_executed",
    "state_hash", "revision", "binding_hash", "candidate", "candidate_file", "output", "task",
    "task_status", "nominated", "current_acceptance", "snapshot_acceptance", "files_verified",
    "automatic_artistic_judgment")}
report["replay"]["criteria"] = [{k: c.get(k) for k in ("id", "status", "verdict")} for c in replay.get("criteria", [])]
check("replay: reused_review true", replay.get("reused_review") is True, replay.get("reused_review"))
check("replay: publications empty", replay.get("publications") == [], replay.get("publications"))
check("replay: remote_executed false", replay.get("remote_executed") is False, replay.get("remote_executed"))
check("replay: state_hash unchanged", replay.get("state_hash") == EXPECTED_STATE_HASH, replay.get("state_hash"))
check("replay: revision unchanged", replay.get("revision") == EXPECTED_REVISION, replay.get("revision"))
check("replay: review_sha256 is the original report", replay.get("review_sha256") == EXPECTED_REVIEW_SHA, replay.get("review_sha256"))
check("replay: binding_hash", replay.get("binding_hash") == EXPECTED_BINDING, replay.get("binding_hash"))
check("replay: task done / nominated", replay.get("task_status") == "done" and replay.get("nominated") is True)
check("replay: current_acceptance complete", (replay.get("current_acceptance") or {}).get("all_required_pass") is True
      and (replay.get("current_acceptance") or {}).get("task_complete") is True, replay.get("current_acceptance"))
check("replay: snapshot_acceptance.accepted stays false", (replay.get("snapshot_acceptance") or {}).get("accepted") is False)
check("replay: verdict ids unchanged",
      sorted(c.get("verdict") for c in replay.get("criteria", [])) == [f"native-review.family.collective.verdict.{i}" for i in range(3)],
      [c.get("verdict") for c in replay.get("criteria", [])])
prior_replay = load_json("work/native-review/12-caller-family-replay-result.json")
check("replay: parsed result equals prior CLI replay 12-caller-family-replay-result.json", replay == prior_replay)
report["replay"]["prior_cli_replay_sha256"] = sha_bytes(read("work/native-review/12-caller-family-replay-result.json"))
report["replay"]["prior_cli_replay_bytes_identical"] = read("work/native-review/12-caller-family-replay-result.json") == read(
    "work/export-review/03-identical-review-result.json")

# Retained review report hashes to its directory name.
review_rel = replay.get("review_path")
review_bytes = read(review_rel)
check("review report file sha256 equals directory name", sha_bytes(review_bytes) == EXPECTED_REVIEW_SHA, sha_bytes(review_bytes))
review_doc = json.loads(review_bytes.decode("utf-8"))
report["review_report"] = {"path": review_rel, "sha256": sha_bytes(review_bytes), "bytes": len(review_bytes),
                           "top_level_keys": sorted(review_doc.keys())}

# 5. State remains unchanged (export-kit validate, run natively).
proc = subprocess.run([PY, "-I", KIT, "validate", ".pixl/assets/queue.ready/state.px", "--root", ROOT],
                      cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
validate = json.loads(proc.stdout)
report["validate"] = {k: validate.get(k) for k in ("valid", "format", "revision", "hash", "records", "files_verified")}
report["validate"]["exit_code"] = proc.returncode
check("validate: exit 0", proc.returncode == 0, proc.stderr[-500:])
check("validate: valid", validate.get("valid") is True)
check("validate: hash unchanged", validate.get("hash") == EXPECTED_STATE_HASH, validate.get("hash"))
check("validate: revision 126", validate.get("revision") == EXPECTED_REVISION, validate.get("revision"))
check("validate: 794 records", validate.get("records") == 794, validate.get("records"))
check("validate: files_verified", validate.get("files_verified") is True)

state_bytes = read(".pixl/assets/queue.ready/state.px")
report["state_file"] = {"path": ".pixl/assets/queue.ready/state.px", "file_sha256": sha_bytes(state_bytes), "bytes": len(state_bytes),
                        "mtime": os.path.getmtime(rel(".pixl/assets/queue.ready/state.px"))}
assignment_mtime = os.path.getmtime(rel("EXPORT-ASSIGNMENT.md"))
newer = []
for dirpath, _dirs, files in os.walk(rel(".pixl")):
    for name in files:
        full = os.path.join(dirpath, name)
        if os.path.getmtime(full) > assignment_mtime:
            newer.append(os.path.relpath(full, ROOT).replace(os.sep, "/"))
report["store_files_modified_after_assignment"] = newer
check("store: no .pixl file modified after EXPORT-ASSIGNMENT.md", not newer, newer)
history_dir = rel(".pixl/assets/queue.ready/history")
report["history_file_count"] = len(os.listdir(history_dir))
check("history: creation receipt revision 123 hash exists as saved revision",
      os.path.exists(os.path.join(history_dir, CREATION_RECEIPT_HASH + ".px")))
check("history: current revision 126 hash exists as saved revision",
      os.path.exists(os.path.join(history_dir, EXPECTED_STATE_HASH + ".px")))

# 6. Identical request and preserved prior files.
prior_hashes = {}
for p, expected in PRIOR.items():
    actual = sha_bytes(read(p))
    prior_hashes[p] = {"sha256": actual, "bytes": len(read(p)), "unchanged": actual == expected}
    check(f"preserved unchanged: {p}", actual == expected, actual)
report["prior_files"] = prior_hashes
req = load_json("work/export-review/identical-review.json")
orig_req = load_json("work/native-review/07-family-review-request.json")
check("identical-review.json parses equal to 07-family-review-request.json", req == orig_req)
report["identical_request"] = {
    "path": "work/export-review/identical-review.json",
    "sha256": prior_hashes["work/export-review/identical-review.json"]["sha256"],
    "parsed_equal_to_original_request": req == orig_req,
    "byte_identical_to_original_request": read("work/export-review/identical-review.json") == read("work/native-review/07-family-review-request.json"),
    "crlf_line_endings": b"\r\n" in read("work/export-review/identical-review.json"),
    "original_crlf_line_endings": b"\r\n" in read("work/native-review/07-family-review-request.json"),
    "binding_hash": req.get("binding_hash"),
    "action": req.get("action"),
    "verdict_count": len(req.get("verdicts", [])),
    "observation_count": len(req.get("observations", [])),
}
check("identical request binding_hash matches context", req.get("binding_hash") == EXPECTED_BINDING)

# Malformed creation receipt and caller-corrected copy.
orig_receipt = read("work/native-review/04-family-snapshot-result.json")
try:
    json.loads(orig_receipt.decode("utf-8"))
    orig_parse = {"valid_json": True}
except json.JSONDecodeError as exc:
    orig_parse = {"valid_json": False, "error": str(exc)}
report["creation_receipt"] = {"path": "work/native-review/04-family-snapshot-result.json", **prior_hashes["work/native-review/04-family-snapshot-result.json"], **orig_parse}
check("prior 04-family-snapshot-result.json remains malformed JSON (preserved, not repaired)", orig_parse["valid_json"] is False, orig_parse.get("error"))
corrected = load_json("work/native-review/04-family-snapshot-result.caller-corrected.json")
report["creation_receipt_corrected"] = {"path": "work/native-review/04-family-snapshot-result.caller-corrected.json",
                                        **prior_hashes["work/native-review/04-family-snapshot-result.caller-corrected.json"],
                                        "revision": corrected.get("revision"), "hash": corrected.get("hash"),
                                        "accepted": corrected.get("accepted"), "candidate": corrected.get("candidate"),
                                        "manifest": corrected.get("manifest")}
check("corrected receipt: revision 123 / creation hash", corrected.get("revision") == 123 and corrected.get("hash") == CREATION_RECEIPT_HASH)
check("corrected receipt: accepted false (creation status)", corrected.get("accepted") is False)
check("corrected receipt: manifest path matches current context candidate file",
      corrected.get("manifest") == (ctx.get("candidate_file") or {}).get("path"), corrected.get("manifest"))
manifest_bytes = read(corrected["manifest"])
check("manifest.json sha256 equals package directory name", sha_bytes(manifest_bytes) == EXPECTED_MANIFEST_SHA, sha_bytes(manifest_bytes))

report["all_checks_passed"] = all(c["ok"] for c in checks)
report["failed_checks"] = [c for c in checks if not c["ok"]]
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(report, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print(json.dumps({"all_checks_passed": report["all_checks_passed"], "checks": len(checks),
                  "failed": [c["check"] for c in report["failed_checks"]], "output": OUT}, indent=2))
sys.exit(0 if report["all_checks_passed"] else 1)
