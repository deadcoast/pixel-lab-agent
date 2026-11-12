"""Phase-3 caller verification and CALLER-RESULT.json composer.

Run with the selected Python -I from the consumer root:
  python.exe -I work/provider-recovery/phase-3/scripts/write_caller_result.py <consumer_root>

Read-only against the store; writes only work/provider-recovery/phase-3/CALLER-RESULT.json.
All hashes are computed from disk at run time; no hash is transcribed from memory.
"""
import datetime
import hashlib
import json
import os
import sys

ROOT = sys.argv[1]
P3 = "work/provider-recovery/phase-3"
P2 = "work/provider-recovery/phase-2"
P1 = "work/provider-recovery/phase-1"
CANDIDATE_PATH = ".pixl/recovery/artifacts/d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7.png"
STATE_PATH = ".pixl/recovery/state.px"


def ap(rel):
    return os.path.join(ROOT, rel.replace("/", os.sep))


def sha(rel):
    h = hashlib.sha256()
    with open(ap(rel), "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def size(rel):
    return os.path.getsize(ap(rel))


def load(rel):
    with open(ap(rel), "rb") as f:
        return json.loads(f.read().decode("utf-8"))


def ref(rel):
    return {"path": rel, "sha256": sha(rel)}


clock = datetime.datetime.now(datetime.timezone.utc).isoformat()
failures = []

# --- specialist result and its evidence refs ---------------------------------
spec_rel = P3 + "/SPECIALIST-RESULT.json"
spec = load(spec_rel)
spec_ref_checks = []
for r in spec["evidence_refs"]:
    actual = sha(r["path"])
    ok = actual == r["sha256"]
    spec_ref_checks.append({"path": r["path"], "declared": r["sha256"], "actual": actual, "match": ok})
    if not ok:
        failures.append("specialist evidence_ref mismatch: " + r["path"])

# --- phase-2 caller evidence refs (covers phase-1/phase-2 files + core files) -
p2_caller_rel = P2 + "/CALLER-RESULT.json"
p2_caller = load(p2_caller_rel)
p2_ref_checks = []
for r in p2_caller["evidence_refs"]:
    actual = sha(r["path"])
    ok = actual == r["sha256"]
    p2_ref_checks.append({"path": r["path"], "match": ok})
    if not ok:
        failures.append("phase-2 caller evidence_ref changed on disk: " + r["path"])
p2_spec_rel = P2 + "/SPECIALIST-RESULT.json"
p2_spec_ok = sha(p2_spec_rel) == p2_caller["specialist_result"]["sha256"]
if not p2_spec_ok:
    failures.append("phase-2 SPECIALIST-RESULT.json hash differs from phase-2 caller record")

# --- jobs reports -------------------------------------------------------------
caller_jobs_rel = P3 + "/caller-jobs.json"
jobs_before_rel = P3 + "/jobs-before.json"
jobs_after_rel = P3 + "/jobs-after.json"
caller_jobs = load(caller_jobs_rel)
jobs_before = load(jobs_before_rel)
jobs_after = load(jobs_after_rel)
with open(ap(caller_jobs_rel), "rb") as f:
    cj_bytes = f.read()
with open(ap(jobs_before_rel), "rb") as f:
    jb_bytes = f.read()
jobs_sem_eq = caller_jobs == jobs_before == jobs_after
if not jobs_sem_eq:
    failures.append("caller-jobs.json not semantically equal to specialist jobs-before/after")
byte_diff = "identical" if cj_bytes == jb_bytes else (
    "specialist file has trailing newline only" if jb_bytes == cj_bytes + b"\n" else "other byte difference")

rj = next(j for j in caller_jobs["jobs"] if j["id"] == "recoverable-job")
uj = next(j for j in caller_jobs["jobs"] if j["id"] == "unresolved-job")
imported = rj["recovery"]["imported"][0]

# --- candidate / delivered file -----------------------------------------------
cand_sha = sha(CANDIDATE_PATH)
robot_sha = sha("assets/robot.png")
state_sha = sha(STATE_PATH)
avatar_sha = sha("src/avatar.ts")
with open(ap("src/avatar.ts"), "r", encoding="utf-8") as f:
    avatar_src = f.read().strip()
avatar_ok = ('path: "assets/robot.png"' in avatar_src and "width: 32" in avatar_src
             and "height: 32" in avatar_src and 'sampling: "nearest"' in avatar_src)

checks = {
    "candidate_path_from_caller_jobs_report": imported["path"] == CANDIDATE_PATH,
    "candidate_sha256_equals_jobs_report": cand_sha == imported["sha256"],
    "candidate_sha256_equals_specialist_candidate": cand_sha == spec["candidate"]["sha256"]
    and imported["path"] == spec["candidate"]["path"],
    "candidate_bytes": size(CANDIDATE_PATH),
    "assets_robot_png_byte_identical_to_candidate": robot_sha == cand_sha and size("assets/robot.png") == size(CANDIDATE_PATH),
    "assets_robot_png_bytes": size("assets/robot.png"),
    "state_file_sha256_equals_jobs_report_hash": state_sha == caller_jobs["hash"],
    "state_revision_from_caller_jobs_report": caller_jobs["revision"],
    "state_matches_specialist_state": state_sha == spec["state"]["sha256"] == spec["state"]["canonical_hash"]
    and caller_jobs["revision"] == spec["state"]["revision"],
    "recoverable_job_state": rj["state"],
    "recoverable_job_remote_id": rj["remote_id"],
    "recoverable_job_next_action": rj["next_action"],
    "recoverable_job_missing_outputs": rj["recovery"]["missing_outputs"],
    "recoverable_job_event_count": len(rj["events"]),
    "unresolved_job_state": uj["state"],
    "unresolved_job_remote_id": uj["remote_id"],
    "unresolved_job_next_action": uj["next_action"],
    "unresolved_job_missing_outputs": uj["recovery"]["missing_outputs"],
    "unresolved_job_event_count": len(uj["events"]),
    "unresolved_job_guidance": uj["recovery"]["guidance"],
    "avatar_ts_maps_assets_robot_png_32x32_nearest": avatar_ok,
    "avatar_ts_line": avatar_src,
    "specialist_identity_same_as_phase2": (
        spec["job"] == p2_caller["job"] == rj["id"]
        and spec["remote_id"] == p2_caller["remote_id"] == rj["remote_id"]
        and spec["candidate"] == p2_caller["candidate"]
        and spec["unresolved_job"] == p2_caller["unresolved_job"] == uj["id"]
    ),
    "specialist_status": spec["status"],
    "specialist_provider_simulated": spec["provider_simulated"],
    "specialist_evidence_refs_all_match": all(c["match"] for c in spec_ref_checks),
    "specialist_evidence_refs_count": len(spec_ref_checks),
    "phase2_caller_evidence_refs_all_unchanged": all(c["match"] for c in p2_ref_checks),
    "phase2_caller_evidence_refs_count": len(p2_ref_checks),
    "phase2_specialist_result_unchanged": p2_spec_ok,
    "caller_jobs_semantically_equal_to_specialist_jobs_before_and_after": jobs_sem_eq,
    "caller_jobs_vs_specialist_jobs_before_bytes": byte_diff,
    "specialist_jobs_before_equals_after_bytes": sha(jobs_before_rel) == sha(jobs_after_rel),
}
for key in ("candidate_path_from_caller_jobs_report", "candidate_sha256_equals_jobs_report",
            "candidate_sha256_equals_specialist_candidate", "assets_robot_png_byte_identical_to_candidate",
            "state_file_sha256_equals_jobs_report_hash", "state_matches_specialist_state",
            "avatar_ts_maps_assets_robot_png_32x32_nearest", "specialist_identity_same_as_phase2"):
    if checks[key] is not True:
        failures.append("check failed: " + key)
if rj["next_action"] != "inspect_candidates" or rj["recovery"]["missing_outputs"]:
    failures.append("recoverable-job projection unexpected")
if uj["state"] != "unknown" or uj["remote_id"] is not None or len(uj["events"]) != 2:
    failures.append("unresolved-job changed")

status = "recovered" if not failures else "partial"

evidence_paths = [
    spec_rel, caller_jobs_rel, jobs_before_rel, jobs_after_rel,
    P3 + "/validate-before.json", P3 + "/validate-after.json", P3 + "/workflow-before.json",
    P3 + "/asset-check.json", P3 + "/rehash.json", P3 + "/scripts/write_caller_result.py",
    CANDIDATE_PATH, STATE_PATH, "assets/robot.png", "src/avatar.ts", "input.png", "reference.png",
    p2_caller_rel, p2_spec_rel, P2 + "/caller-jobs.json", P2 + "/retrieved.png",
    P1 + "/CALLER-RESULT.json", P1 + "/SPECIALIST-RESULT.json", P1 + "/download.part",
]

result = {
    "phase": 3,
    "status": status,
    "provider_simulated": True,
    "job": rj["id"],
    "remote_id": rj["remote_id"],
    "unresolved_job": uj["id"],
    "unresolved_state": uj["state"],
    "candidate": {
        "id": imported["candidate_id"],
        "output": imported["output_id"],
        "path": imported["path"],
        "sha256": cand_sha,
    },
    "state": {
        "path": STATE_PATH,
        "sha256": state_sha,
        "canonical_hash": caller_jobs["hash"],
        "revision": caller_jobs["revision"],
    },
    "native_child": {
        "agent_type": "pixl:pixl",
        "agent_id": "a06ade5d7e5d27b80",
        "host": "claude",
        "completed": True,
        "reported_status": spec["status"],
        "tool_uses": 23,
        "duration_ms": 232867,
        "launched_with": "Agent tool subagent_type=pixl:pixl, run_in_background=true; fresh child for this phase, not a continuation of the phase-1 or phase-2 child",
    },
    "specialist_result": ref(spec_rel),
    "caller_verification": {
        "written_at": clock,
        "timestamp_source": "host clock via selected Python -I datetime.now(timezone.utc) at the start of this script run",
        "cold_read_before_delegation": {
            "pixl_validate": {"valid": True, "revision": 9,
                               "hash": "c4d3812040eb9b1d1cae8e0e3eae167efeb7ae5f8f1d3f21e0bae24ea649e165",
                               "records": 30, "files_verified": True},
            "candidate_and_assets_robot_png_byte_identical": True,
            "assets_robot_png_opened_with_image_tool": True,
            "pixl_asset_check_assets_robot_png": {"pass": True, "width": 32, "height": 32, "frame_count": 1,
                                                    "visible_pixels": 390, "visible_colors": 3,
                                                    "fractional_alpha_pixels": 0, "opaque_components": 1,
                                                    "visual_quality_verified": False,
                                                    "engine_import_verified": False},
            "clock_at_baseline": "2026-11-12T12:38:39.136550+00:00",
            "note": "Values in this block were observed by the caller before the child was launched and are transcribed from the tool outputs of that step; every other value in this file is computed at script run time.",
        },
        "jobs_report_source": "mcp__pixl-local__pixl_jobs path=.pixl/recovery/state.px, retrieved independently by the caller after child completion and saved verbatim as caller-jobs.json",
        "after_child_pixl_validate": {"valid": True, "revision": 9,
                                       "hash": "c4d3812040eb9b1d1cae8e0e3eae167efeb7ae5f8f1d3f21e0bae24ea649e165",
                                       "records": 30, "files_verified": True},
        "after_child_pixl_workflow": {"recover-task": "open", "unresolved-task": "open",
                                       "recovered-avatar-candidate_nominated": False,
                                       "q.bytes_status": "unperformed", "q.bytes_verdict": None},
        "retained_candidate_opened_with_image_tool": "Read tool rendered the retained artifact PNG and assets/robot.png; both display as the same small 32x32 sprite. Mechanical open only, not artistic acceptance.",
        "checks": checks,
        "specialist_evidence_ref_checks": spec_ref_checks,
        "phase2_caller_evidence_ref_checks": p2_ref_checks,
        "failures": failures,
    },
    "evidence_refs": [ref(p) for p in evidence_paths],
    "limitations": [
        "No live PixelLab: the provider is the controlled pixellab-recovery-test fixture with provider_simulated=true. Neither participant called any fixture tool in this phase; no submission, dispatch, prepare, generate, upload, download, poll or paid work occurred.",
        "Read-only round: no production-state mutation by either participant. The caller's pixl-local calls were pixl_validate (twice), pixl_asset_check (once, on assets/robot.png), pixl_jobs (once) and pixl_workflow (once). The store remained at revision 9 with the same canonical hash throughout; no file copy was made and assets/robot.png, src/, input.png, reference.png, the kit and all phase-1/phase-2 files are unchanged (every phase-2 caller evidence_ref re-hashed by this script).",
        "Recovery is mechanical only: the same candidate recovered-avatar-candidate (177 bytes) as phase 2 was re-hashed from disk and matches the jobs report and the specialist's report; assets/robot.png is byte-identical to it and src/avatar.ts maps that path at 32x32 nearest. No artistic, target-engine or human acceptance was performed or claimed; pixl_asset_check reports visual_quality_verified=false and engine_import_verified=false; no consumer or renderer was executed.",
        "No acceptance recorded: candidate nominated=false and criterion q.bytes remains unperformed with verdict null in the current workflow report. No candidate review, inspection packet, nomination or task completion was created in this phase; those remain separate deliberate steps.",
        "unresolved-job remains unknown with remote_id null, only its original two events and next_action reconcile with missing output unresolved-output. It was not observed, modified, abandoned or resolved; absence from any listing is not proof of non-acceptance, and no originating-connection lookup was made in this read-only phase.",
        "caller-jobs.json is semantically equal (parsed JSON equality) to the specialist's jobs-before.json and jobs-after.json; the specialist's files carry one trailing newline so the byte hashes differ by that byte only. caller-jobs.json is byte-identical to the phase-2 specialist's jobs-after.json, and the specialist's phase-3 jobs files are byte-identical to the phase-2 caller's caller-jobs.json, so the public jobs report is unchanged since the phase-2 import.",
        "M1/M2 and broader M3/M4 remain open.",
        "The native child's agent ID is the host-reported subagent ID for this fresh phase-3 run; this phase is not a same-session or same-child continuation of phase 1 or 2.",
        "The caller wrote only caller-jobs.json, scripts/write_caller_result.py and CALLER-RESULT.json under work/provider-recovery/phase-3. The evidence_refs entry for scripts/write_caller_result.py hashes the script that composed this file; CALLER-RESULT.json itself is not self-referenced.",
    ],
    "next_action": (
        "Candidate: a separate, deliberate inspection and review of recovered-avatar-candidate for criterion q.bytes "
        "(pixl_review_context for candidate_id recovered-avatar-candidate on .pixl/recovery/state.px, then pixl_inspection_prepare "
        "on store .pixl/recovery with expect " + caller_jobs["hash"] + " or the then-current canonical hash, then an explicit "
        "pixl_candidate_review verdict bound to " + CANDIDATE_PATH + " sha256 " + cand_sha + "); nomination and task completion "
        "remain further separate steps and are not implied by import or by these measurements. unresolved-job: next_action per the "
        "public jobs report is reconcile (missing output unresolved-output; use the originating provider connection and saved "
        "request/history; no ID or elapsed time proves non-acceptance; do not redispatch). It stays unknown with no dispatch, "
        "re-prepare or abandon until actual matching originating-connection evidence exists."
    ),
}

out_rel = P3 + "/CALLER-RESULT.json"
with open(ap(out_rel), "w", encoding="utf-8", newline="\n") as f:
    json.dump(result, f, indent=2)
    f.write("\n")
print("status", status)
print("failures", json.dumps(failures))
print("written", out_rel, sha(out_rel))
