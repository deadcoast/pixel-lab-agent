"""Parent scratch, third attempt: the second revision-03/CALLER-RESULT.json was 9628 bytes (> 8192). It is retained as
revision-03/CALLER-RESULT-attempt-02-oversize.json (rename only). This version keeps every required field and every
exact reference carried from the prior caller report, shortens agent prose, and relies on the linked
unavailable-comparison-02.json for the first-attempt unavailable-error file hashes."""
import hashlib, json, os, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
r3 = root / "work/compact-caller/revision-03"
cur = r3 / "CALLER-RESULT.json"
keep = r3 / "CALLER-RESULT-attempt-02-oversize.json"
if keep.exists():
    raise SystemExit("retained attempt already exists")
cur_bytes = cur.read_bytes()
cur_sha = hashlib.sha256(cur_bytes).hexdigest()
if len(cur_bytes) < 8192:
    raise SystemExit("current already within bound")
os.replace(cur, keep)
assert hashlib.sha256(keep.read_bytes()).hexdigest() == cur_sha
out = json.loads(cur_bytes.decode("utf-8"))
out["reviewer"] = "parent caller, session 0510b038-b18b-4fbc-aafe-c19b95d7dba6"
out["native_child"] = {
    "role": "pixl", "agent_type": "pixl:pixl", "agent_id": "ab352c80d7f534aae", "fork": "none",
    "first_child": {"agent_id": "ac98550e535c93d5a", "did": "2026-11-10: authored details/report, published original caller view and handoff 0f2d80cd...; interrupted (HTTP 429, host timeout)"},
    "latest_child": {"agent_id": "ab352c80d7f534aae", "did": "resumed via SendMessage: receipt view, prior result; revision-03 own caller-view call (same snapshot, byte-identical) and fresh result"},
    "correction": "Prior report credited the latest child with the first child's publication; corrected, history retained."}
out.pop("unavailable_host_return", None)
hist = out["historical"]
hist.pop("prior_compact", None)
hist.pop("first_attempt_host_copy", None)
hist.pop("first_attempt_comparison", None)
hist["second_attempt_caller_result"] = {"path": "work/compact-caller/revision-03/CALLER-RESULT-attempt-02-oversize.json", "sha256": cur_sha}
hist["note"] = "prior compact.json is byte-identical to revision-03/compact.json (same sha256); first-attempt unavailable host copy and comparison hashes are listed in unavailable-comparison-02.json"
out["defects"] = [
    "Provenance: prior caller/specialist results credited the latest child with the first child's caller-view publication. Corrected; same immutable snapshot.",
    "Exact error retention: prior errors/unavailable-observation.json collapsed doubled literal backslashes in detail (10 vs 20). Cause: Bash heredoc halves backslash runs; first revision-03 host copy and comparison repeated it (retained failures). Fresh error from maintainer helper raw protocol; host return saved via Write equals it exactly.",
    "Size: first two revision-03 caller results exceeded 8192 bytes; retained as attempt-01/02 files; this file has identical fields and references.",
]
out["retained_evidence"] = "receipt, parent receipt, details/resume reads, refresh, recoveries and the other four error reports retained from the prior continuation; not repeated."
out["preservation"]["existing_files_modified"] = "none; see revision-03/caller-verify-03c.json"
b = json.dumps(out, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
with cur.open("xb") as s:
    s.write(b)
print("bytes", len(b), "retained", keep.name, cur_sha)
