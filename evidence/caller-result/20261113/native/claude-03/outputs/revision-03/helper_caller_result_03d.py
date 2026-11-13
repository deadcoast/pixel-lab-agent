"""Parent scratch, fourth attempt: the third revision-03/CALLER-RESULT.json was 9088 bytes (> 8192), retained as
revision-03/CALLER-RESULT-attempt-03-oversize.json (rename only). This version keeps every required field name and
every exact path/sha256 reference, and condenses only agent-authored prose (probes, scope, locator route, labels)."""
import hashlib, json, os, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
r3 = root / "work/compact-caller/revision-03"
cur = r3 / "CALLER-RESULT.json"
keep = r3 / "CALLER-RESULT-attempt-03-oversize.json"
if keep.exists():
    raise SystemExit("retained attempt already exists")
cur_bytes = cur.read_bytes()
cur_sha = hashlib.sha256(cur_bytes).hexdigest()
if len(cur_bytes) < 8192:
    raise SystemExit("current already within bound")
os.replace(cur, keep)
assert hashlib.sha256(keep.read_bytes()).hexdigest() == cur_sha
out = json.loads(cur_bytes.decode("utf-8"))
out["probes"] = {
    "invalid_authoring": "caller_result_input rejected; validated details caller block reused",
    "stale_local_state": "handoff_stale rejected; recovery read matched compact",
    "unavailable_observation": "operation error retained; file not created",
    "uncertain_remote_result": "job_history rejected duplicate dispatch; still unknown",
    "missing_capability": "unknown_tool from actual tools/list and tools/call"}
out["locator_reads"] = {"details_ref": out["locator_reads"]["details_ref"], "resume_ref": out["locator_reads"]["resume_ref"],
                        "route": "host pixl_source + frozen-kit stdio capture; see source-reads-summary.json"}
out["identities"]["compared"] = "returned refresh identities vs the three views; no recomputation"
out["scope"] = "QOL-10/SC-08 caller usability evaluation. Delivered artistic production (artistic-02.plan, CF-03/TM-04 reused-art successor) unchanged; combined reporting assignment partial; creation acceptance and artistic-01.plan are history; unknown job is a separate fixture. No provider call, dispatch, observation, acceptance, art edit, config or manual .px change."
out["historical"]["note"] = "prior compact.json byte-identical to revision-03/compact.json; first-attempt unavailable copy/comparison hashes in unavailable-comparison-02.json"
out["historical"]["third_attempt_caller_result"] = {"path": "work/compact-caller/revision-03/CALLER-RESULT-attempt-03-oversize.json", "sha256": cur_sha}
out["unknown_fixture"]["label"] = "controlled fictional fixture, not production; duplicate dispatch rejected; unchanged"
out["defects"] = [
    "Provenance: prior results credited the latest child with the first child's caller-view publication. Corrected; same immutable snapshot.",
    "Exact error retention: prior errors/unavailable-observation.json collapsed doubled literal backslashes (10 vs 20). Cause: Bash heredoc halves backslash runs; first revision-03 host copy/comparison repeated it (retained). Fresh error from maintainer helper raw protocol; Write-saved host return equals it exactly.",
    "Size: revision-03 caller result attempts 01-03 exceeded 8192 bytes; retained; this file keeps identical fields and references."]
out["unresolved"] = ["controlled-unknown member.job remains unknown (fixture; reconcile only on its originating connection)",
                     "no fresh renderer/integration run; integration is retained evidence", "M1/M2 and broader M3/M4 open", "human acceptance separate"]
out["next_action"] = "Production next is 'delivered'; reread focused PLAR before any operation; no remote retry; resolve the fixture job only in its own root."
out["preservation"]["existing_files_modified"] = "none; see revision-03/caller-verify-03d.json"
b = json.dumps(out, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
with cur.open("xb") as s:
    s.write(b)
print("bytes", len(b), "retained", keep.name, cur_sha)
