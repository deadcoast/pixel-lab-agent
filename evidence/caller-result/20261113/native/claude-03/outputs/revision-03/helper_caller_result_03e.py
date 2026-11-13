"""Parent scratch, fifth attempt: the fourth revision-03/CALLER-RESULT.json was 8812 bytes (> 8192) and had dropped the
prior compact.json reference. It is retained as CALLER-RESULT-attempt-04-oversize.json (rename only). This version
restores every exact reference of the prior caller report, moves the oversize-attempt references into
revision-03/oversize-attempts.json (referenced once), and condenses agent prose further."""
import hashlib, json, os, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
r3 = root / "work/compact-caller/revision-03"
cur = r3 / "CALLER-RESULT.json"
keep = r3 / "CALLER-RESULT-attempt-04-oversize.json"
if keep.exists() or (r3 / "oversize-attempts.json").exists():
    raise SystemExit("retained outputs already exist")
cur_bytes = cur.read_bytes()
cur_sha = hashlib.sha256(cur_bytes).hexdigest()
if len(cur_bytes) < 8192:
    raise SystemExit("current already within bound")
os.replace(cur, keep)
assert hashlib.sha256(keep.read_bytes()).hexdigest() == cur_sha


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


attempts = {"scope": "revision-03 caller result attempts that exceeded the 8192-byte scenario bound; retained unchanged",
            "attempts": [{"path": "work/compact-caller/revision-03/" + n, "sha256": sha(r3 / n), "bytes": len((r3 / n).read_bytes())}
                         for n in ("CALLER-RESULT-attempt-01-oversize.json", "CALLER-RESULT-attempt-02-oversize.json",
                                   "CALLER-RESULT-attempt-03-oversize.json", "CALLER-RESULT-attempt-04-oversize.json")]}
(r3 / "oversize-attempts.json").write_text(json.dumps(attempts, indent=1), encoding="utf-8")
out = json.loads(cur_bytes.decode("utf-8"))
prior = json.loads((root / "work/compact-caller/CALLER-RESULT.json").read_text("utf-8"))
out["reviewer"] = "parent caller, session 0510b038"
out["native_child"]["first_child"]["did"] = "2026-11-10: authored details/report, published original caller view + handoff 0f2d80cd...; interrupted (HTTP 429, timeout)"
out["native_child"]["latest_child"]["did"] = "resumed via SendMessage: receipt view, prior result; revision-03 own caller-view call (same snapshot, byte-identical), fresh result"
out["native_child"]["correction"] = "Prior report credited latest child with first child's publication; corrected, history retained."
out.pop("unavailable_protocol", None)
out["locator_reads"].pop("route", None)
out["historical"] = {"prior_compact": prior["compact"], "prior_specialist_result": prior["specialist_result"],
                     "prior_error_unavailable": prior["errors"]["unavailable_observation"],
                     "oversize_attempts": {"path": "work/compact-caller/revision-03/oversize-attempts.json", "sha256": sha(r3 / "oversize-attempts.json")}}
out["probes"] = {"invalid_authoring": "caller_result_input rejected", "stale_local_state": "handoff_stale rejected; recovery read matched",
                 "unavailable_observation": "operation error retained; no file created", "uncertain_remote_result": "job_history rejected duplicate; still unknown",
                 "missing_capability": "unknown_tool via actual tools/list+call"}
out["defects"] = [
    "Provenance: prior results credited the latest child with the first child's caller-view publication; corrected, same immutable snapshot.",
    "Exact error retention: prior errors/unavailable-observation.json collapsed doubled literal backslashes (10 vs 20); cause: Bash heredoc halves backslash runs; first revision-03 host copy/comparison repeated it (retained, hashes in unavailable-comparison-02.json). Fresh error = maintainer helper raw protocol; Write-saved host return equals it exactly.",
    "Size: four revision-03 attempts exceeded 8192 bytes; retained via oversize-attempts.json."]
out["retained_evidence"] = "receipt, parent receipt, source reads, refresh, recoveries and four error reports retained from the prior continuation; not repeated."
out["preservation"]["existing_files_modified"] = "none; see revision-03/caller-verify-03e.json"
b = json.dumps(out, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
with cur.open("xb") as s:
    s.write(b)
print("bytes", len(b), "retained", keep.name, cur_sha)
