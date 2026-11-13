"""Parent scratch: build work/compact-caller/revision-03/CALLER-RESULT.json from actual saved files.
Carries forward every field of the prior caller report (work/compact-caller/CALLER-RESULT.json, retained as history),
updating native_child, compact, specialist_result and errors.unavailable_observation to the same-child / fresh files."""
import hashlib, json, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
w = "work/compact-caller/"
r3 = w + "revision-03/"


def sha(rel):
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


def ref(rel):
    return {"path": rel, "sha256": sha(rel)}


def jl(rel):
    return json.loads((root / rel).read_text("utf-8"))


prior = jl(w + "CALLER-RESULT.json")
compact = jl(r3 + "compact.json")
receipt = jl(w + "receipt.json")
parent = jl(w + "parent-receipt.json")
spec = jl(r3 + "SPECIALIST-RESULT.json")
cmp2 = jl(r3 + "unavailable-comparison-02.json")
snap_path = compact["path"]
snap_sha = sha(snap_path)
same = (compact["path"] == receipt["path"] == parent["path"]
        and compact["sha256"] == receipt["sha256"] == parent["sha256"] == snap_sha
        and compact["state_hash"] == receipt["state_hash"] == parent["state_hash"]
        and compact["requirements_hash"] == receipt["requirements_hash"] == parent["requirements_hash"])
# retained references must still match their bytes
for k in ("receipt", "parent_receipt", "details_read", "resume_read", "refresh", "specialist_report", "details",
          "unknown_recovery", "stale_recovery", "missing_capability_protocol", "source_reads_protocol"):
    assert sha(prior[k]["path"]) == prior[k]["sha256"], k
for k, v in prior["errors"].items():
    assert sha(v["path"]) == v["sha256"], k
errors = dict(prior["errors"])
errors["unavailable_observation"] = ref(r3 + "errors/unavailable-observation.json")
out = {
    "version": 1, "kind": "caller_result", "revision": "03", "observed_at": "2026-11-13",
    "reviewer": "parent caller, persisted session 0510b038-b18b-4fbc-aafe-c19b95d7dba6",
    "supersedes": ref(w + "CALLER-RESULT.json"),
    "native_child": {
        "role": "pixl", "agent_type": "pixl:pixl", "agent_id": "ab352c80d7f534aae", "fork": "none",
        "first_child": {"agent_id": "ac98550e535c93d5a", "did": "published original caller view compact.json and handoff 0f2d80cd... on 2026-11-10; authored details.json and SPECIALIST-REPORT.json; interrupted (HTTP 429 earlier launch, then host timeout)"},
        "latest_child": {"agent_id": "ab352c80d7f534aae", "did": "resumed via SendMessage; receipt view 2026-11-13; prior specialist result; revision-03 own actual caller-view call (same snapshot, byte-identical return) and fresh specialist result"},
        "correction": "Prior caller report attributed the first child's caller-view publication to the latest child; corrected here, history retained."},
    "compact": ref(r3 + "compact.json"),
    "receipt": prior["receipt"], "parent_receipt": prior["parent_receipt"],
    "details_read": prior["details_read"], "resume_read": prior["resume_read"], "refresh": prior["refresh"],
    "specialist_result": ref(r3 + "SPECIALIST-RESULT.json"),
    "specialist_report": prior["specialist_report"], "details": prior["details"],
    "errors": errors,
    "unknown_recovery": prior["unknown_recovery"], "stale_recovery": prior["stale_recovery"],
    "missing_capability_protocol": prior["missing_capability_protocol"], "source_reads_protocol": prior["source_reads_protocol"],
    "unavailable_protocol": ref(r3 + "unavailable-protocol.jsonl"),
    "unavailable_host_return": ref(r3 + "host-unavailable-return-02.json"),
    "unavailable_comparison": ref(r3 + "unavailable-comparison-02.json"),
    "snapshot": {"path": snap_path, "sha256": snap_sha},
    "same_snapshot": same,
    "identities": prior["identities"],
    "locator_reads": prior["locator_reads"],
    "assignment_status": compact["assignment"]["status"],
    "production_next": compact["next"],
    "production_delivery": prior["production_delivery"],
    "unknown_job_id": "member.job", "unknown_job_state": jl(r3 + "unknown-jobs-check.json")["jobs"][0]["state"],
    "unknown_fixture": dict(prior["unknown_fixture"], recheck=ref(r3 + "unknown-jobs-check.json")),
    "probes": prior["probes"],
    "historical": {
        "prior_compact": prior["compact"], "prior_specialist_result": prior["specialist_result"],
        "prior_error_unavailable": prior["errors"]["unavailable_observation"],
        "first_attempt_host_copy": ref(r3 + "host-unavailable-return.json"),
        "first_attempt_comparison": ref(r3 + "unavailable-comparison.json")},
    "defects": [
        "Provenance: prior caller and specialist results credited the latest child with the first child's caller-view publication. Corrected; nothing semantic changed, same immutable snapshot.",
        "Exact error retention: prior errors/unavailable-observation.json collapsed doubled literal backslashes in native detail (%d vs %d). Cause reproduced: Bash heredoc halves backslash runs; first revision-03 host copy and comparison repeated it and are retained as failures. Fresh error captured by maintainer helper raw protocol and host return saved via Write; exact equality confirmed." % (cmp2["prior_report_detail_backslash_count"], cmp2["native_detail_backslash_count"])],
    "retained_evidence": "receipt, parent receipt, details/resume reads, refresh, stale and unknown recoveries and the other four error reports are retained from the completed prior continuation; those operations were not repeated.",
    "scope": prior["scope"],
    "preservation": {"handoff_files": len(list((root / ".pixl/handoffs").iterdir())), "new_handoff_files": 0,
                     "existing_files_modified": "none; verified in revision-03/caller-verify-03.json"},
    "unresolved": prior["unresolved"],
    "next_action": prior["next_action"],
}
b = json.dumps(out, indent=1, ensure_ascii=False).encode("utf-8")
target = root / r3 / "CALLER-RESULT.json"
if target.exists():
    raise SystemExit("exists")
target.write_bytes(b)
print("bytes", len(b), "same_snapshot", same)
