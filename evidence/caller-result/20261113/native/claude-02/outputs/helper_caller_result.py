"""Parent caller helper: build work/compact-caller/CALLER-RESULT.json from actual saved files (hashes computed from bytes)."""
import hashlib, json, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
w = "work/compact-caller/"
def sha(rel): return hashlib.sha256((root / rel).read_bytes()).hexdigest()
def ref(rel): return {"path": rel, "sha256": sha(rel)}
def jl(rel): return json.loads((root / rel).read_text("utf-8"))
compact = jl(w + "compact.json"); receipt = jl(w + "receipt.json"); parent = jl(w + "parent-receipt.json")
refresh = jl(w + "refresh.json"); cont = refresh["production"]["continuation"]
unknown = jl(w + "unknown-recovery.json")["result"]; job = unknown["jobs"][0]
spec = jl(w + "SPECIALIST-RESULT.json")
snap = compact["sha256"]
same = (compact["path"] == receipt["path"] == parent["path"] and snap == receipt["sha256"] == parent["sha256"] == sha(compact["path"])
        and compact["state_hash"] == receipt["state_hash"] == parent["state_hash"] == cont["state_hash"]
        and compact["requirements_hash"] == receipt["requirements_hash"] == parent["requirements_hash"] == refresh["requirements_hash"])
errors = {"invalid_authoring": ref(w + "errors/invalid-authoring.json"), "stale_local_state": ref(w + "errors/stale-state.json"),
          "unavailable_observation": ref(w + "errors/unavailable-observation.json"), "uncertain_remote_result": ref(w + "errors/uncertain-remote.json"),
          "missing_capability": ref(w + "errors/missing-capability.json")}
out = {
 "version": 1, "kind": "caller_result", "observed_at": "2026-11-13", "reviewer": "parent caller, persisted session 0510b038-b18b-4fbc-aafe-c19b95d7dba6",
 "native_child": {"role": "pixl", "agent_type": "pixl:pixl", "agent_id": spec["native_child"]["agent_id"], "fork": "none",
   "activation": "Named pixl:pixl specialist; first launch failed with HTTP 429, second launch interrupted by host timeout after compact.json; same child resumed via SendMessage and completed receipt and specialist result. Partial outputs retained."},
 "compact": ref(w + "compact.json"), "receipt": ref(w + "receipt.json"), "parent_receipt": ref(w + "parent-receipt.json"),
 "details_read": ref(w + "details-read.json"), "resume_read": ref(w + "resume-read.json"), "refresh": ref(w + "refresh.json"),
 "specialist_result": ref(w + "SPECIALIST-RESULT.json"), "specialist_report": ref(w + "SPECIALIST-REPORT.json"), "details": ref(w + "details.json"),
 "errors": errors, "unknown_recovery": ref(w + "unknown-recovery.json"), "stale_recovery": ref(w + "stale-recovery.json"),
 "missing_capability_protocol": ref(w + "missing-capability-protocol.jsonl"), "source_reads_protocol": ref(w + "source-reads-protocol.jsonl"),
 "snapshot": {"path": compact["path"], "sha256": snap},
 "same_snapshot": same,
 "identities": {"asset_id": compact["asset_id"], "plar_path": "authoring-plar.txt", "store": compact["store"], "state_hash": cont["state_hash"],
   "requirements_hash": refresh["requirements_hash"], "revision": refresh["production"]["revision"], "compared": "returned refresh identities vs compact/receipt/parent-receipt; no independent recomputation",
   "hash_domains": compact["hash_domains"]},
 "locator_reads": {"details_ref": {"start": compact["details_ref"]["start"], "end": compact["details_ref"]["end"], "bytes": compact["details_ref"]["bytes"], "exact": True, "trailing_comma": True},
   "resume_ref": {"start": compact["resume_ref"]["start"], "end": compact["resume_ref"]["end"], "bytes": compact["resume_ref"]["bytes"], "exact": True, "trailing_comma": True},
   "route": "host pixl_source then byte-exact capture through the frozen kit's local MCP stdio server (same inputs); summary in work/compact-caller/source-reads-summary.json"},
 "assignment_status": compact["assignment"]["status"],
 "production_next": cont["action"],
 "production_delivery": {"destination": cont["delivery"]["destination"], "observed_sha256": cont["delivery"]["observed_sha256"], "complete": cont["delivery"]["complete"], "task": cont["task"], "pending_jobs": refresh["production"]["pending_jobs"]},
 "unknown_job_id": job["id"], "unknown_job_state": job["state"],
 "unknown_fixture": {"root": "controlled-unknown", "store": ".pixl", "state_hash": unknown["hash"], "revision": unknown["revision"], "remote_id": job["remote_id"], "events": len(job["events"]), "label": "controlled fictional fixture; not production; duplicate dispatch rejected (job_history); unchanged"},
 "probes": {"invalid_authoring": "caller_result_input rejected; corrected block = validated details.json caller block; guarded receipt reused",
   "stale_local_state": "handoff_stale rejected; recovery pixl_plar_read matched compact identities",
   "unavailable_observation": "operation error retained; file not created",
   "uncertain_remote_result": "job_history rejected duplicate dispatch; recovery pixl_jobs shows unknown unchanged",
   "missing_capability": "unknown_tool from actual tools/list and tools/call; no replacement used"},
 "scope": "QOL-10/SC-08 compact-result caller usability evaluation. Delivered artistic production (artistic-02.plan, CF-03/TM-04 reused-art successor) unchanged; this combined reporting assignment is partial; historical creation acceptance and stale artistic-01.plan are history; the unknown job is a separate fixture. No provider call, dispatch claim accepted, observation, acceptance, art edit, configuration or manual .px change.",
 "preservation": {"handoff_files": len(list((root / ".pixl/handoffs").iterdir())), "new_handoff_files_this_session": 0, "existing_files_modified": "none intended; verified in caller-verify-02.json"},
 "unresolved": ["controlled-unknown member.job remains unknown (fixture; reconcile only on its originating connection)", "no fresh renderer or integration run; integration is retained evidence", "M1/M2 and broader M3/M4 remain open", "human acceptance remains separate"],
 "next_action": "Safe continuation: production next is 'delivered'; reread focused PLAR (refresh) before any further operation; do not retry remote work; resolve the fixture job only inside its own root."
}
b = json.dumps(out, indent=1, ensure_ascii=False).encode("utf-8")
target = root / w / "CALLER-RESULT.json"
if target.exists(): raise SystemExit("CALLER-RESULT.json exists")
target.write_bytes(b); print("bytes", len(b), "same_snapshot", same)
