"""Parent scratch, second attempt: the first revision-03/CALLER-RESULT.json (built by helper_caller_result_03.py) was
10104 bytes, over the 8192-byte scenario bound. It is retained byte-for-byte as
revision-03/CALLER-RESULT-attempt-01-oversize.json (rename only), and a compact-separator version with shortened
prose but identical fields and references is created at revision-03/CALLER-RESULT.json (exclusive create)."""
import hashlib, json, os, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
r3 = root / "work/compact-caller/revision-03"
first = r3 / "CALLER-RESULT.json"
keep = r3 / "CALLER-RESULT-attempt-01-oversize.json"
if keep.exists():
    raise SystemExit("retained attempt already exists")
first_bytes = first.read_bytes()
first_sha = hashlib.sha256(first_bytes).hexdigest()
if len(first_bytes) < 8192:
    raise SystemExit("first attempt already within bound; nothing to do")
os.replace(first, keep)
assert hashlib.sha256(keep.read_bytes()).hexdigest() == first_sha
out = json.loads(first_bytes.decode("utf-8"))
out["native_child"]["first_child"]["did"] = "published original caller view compact.json and handoff 0f2d80cd... on 2026-11-10; authored details.json and SPECIALIST-REPORT.json; interrupted (HTTP 429, then host timeout)"
out["native_child"]["latest_child"]["did"] = "resumed via SendMessage; receipt view 2026-11-13; prior specialist result; revision-03 own actual caller-view call (same snapshot, byte-identical return) and fresh specialist result"
out["defects"] = [
    "Provenance: prior caller and specialist results credited the latest child with the first child's caller-view publication. Corrected; same immutable snapshot, no semantic change.",
    "Exact error retention: prior errors/unavailable-observation.json collapsed doubled literal backslashes in native detail (10 vs 20). Cause: Bash heredoc halves backslash runs; first revision-03 host copy and comparison repeated it and are retained as failures. Fresh error from maintainer helper raw protocol; host return saved via Write; exact equality confirmed.",
    "Size: first revision-03 caller result was 10104 bytes (> 8192); retained as CALLER-RESULT-attempt-01-oversize.json, replaced by this compact-separator file with identical fields and references.",
]
out["historical"]["first_attempt_caller_result"] = {"path": "work/compact-caller/revision-03/CALLER-RESULT-attempt-01-oversize.json", "sha256": first_sha}
out["retained_evidence"] = "receipt, parent receipt, details/resume reads, refresh, stale/unknown recoveries and the other four error reports are retained from the completed prior continuation; not repeated."
out["locator_reads"]["route"] = "host pixl_source then byte-exact capture through the frozen kit's local MCP stdio server (same inputs); see work/compact-caller/source-reads-summary.json"
out["preservation"]["existing_files_modified"] = "none; verified in revision-03/caller-verify-03b.json"
b = json.dumps(out, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
with first.open("xb") as s:
    s.write(b)
print("bytes", len(b), "retained_first_attempt", keep.name, first_sha)
