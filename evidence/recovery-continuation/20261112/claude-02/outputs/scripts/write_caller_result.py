"""Caller-side composer for work/provider-recovery/phase-2/CALLER-RESULT.json.

Reads actual on-disk files under the consumer root, hashes them with SHA-256,
reads the host clock at composition time and writes the caller report.
No provider action, no store mutation.
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

root = sys.argv[1]


def h(p):
    with open(os.path.join(root, p), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sz(p):
    return os.path.getsize(os.path.join(root, p))


def load(p):
    with open(os.path.join(root, p), encoding="utf-8") as f:
        return json.load(f)


refs = [
    "work/provider-recovery/phase-2/SPECIALIST-RESULT.json",
    "work/provider-recovery/phase-2/caller-jobs.json",
    "work/provider-recovery/phase-2/jobs-before.json",
    "work/provider-recovery/phase-2/jobs-after.json",
    "work/provider-recovery/phase-2/workflow-after.json",
    "work/provider-recovery/phase-2/validate-before.json",
    "work/provider-recovery/phase-2/validate-after.json",
    "work/provider-recovery/phase-2/provider-get-image.json",
    "work/provider-recovery/phase-2/download-log.json",
    "work/provider-recovery/phase-2/retrieved.png",
    "work/provider-recovery/phase-2/verify.json",
    "work/provider-recovery/phase-2/import-evidence.json",
    "work/provider-recovery/phase-2/import-result.json",
    "work/provider-recovery/phase-2/scripts/download.py",
    "work/provider-recovery/phase-2/scripts/pngcheck.py",
    "work/provider-recovery/phase-2/scripts/write_caller_result.py",
    ".pixl/recovery/artifacts/d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7.png",
    ".pixl/recovery/state.px",
    "assets/robot.png",
    "src/avatar.ts",
    "input.png",
    "reference.png",
    "work/provider-recovery/phase-1/download.part",
    "work/provider-recovery/phase-1/download-error.json",
    "work/provider-recovery/phase-1/SPECIALIST-RESULT.json",
    "work/provider-recovery/phase-1/CALLER-RESULT.json",
]

EXPECTED_SHA = "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7"
AFTER_HASH = "c4d3812040eb9b1d1cae8e0e3eae167efeb7ae5f8f1d3f21e0bae24ea649e165"
BEFORE_HASH = "ec122a796be05ad2f2a2f092af28747170cf72eea02811546ff457535fc53ee0"

cand = ".pixl/recovery/artifacts/" + EXPECTED_SHA + ".png"
state_sha = h(".pixl/recovery/state.px")
spec = load("work/provider-recovery/phase-2/SPECIALIST-RESULT.json")
spec_sha = h("work/provider-recovery/phase-2/SPECIALIST-RESULT.json")
caller_jobs = load("work/provider-recovery/phase-2/caller-jobs.json")
jobs_after = load("work/provider-recovery/phase-2/jobs-after.json")
rj = next(j for j in caller_jobs["jobs"] if j["id"] == "recoverable-job")
uj = next(j for j in caller_jobs["jobs"] if j["id"] == "unresolved-job")
imp = rj["recovery"]["imported"][0]

with open(os.path.join(root, cand), "rb") as f:
    cand_bytes = f.read()
with open(os.path.join(root, "work/provider-recovery/phase-1/download.part"), "rb") as f:
    part_bytes = f.read()
with open(os.path.join(root, "src/avatar.ts"), encoding="utf-8") as f:
    avatar_ts = f.read().strip()

now = datetime.now(timezone.utc).isoformat()

doc = {
    "phase": 2,
    "status": "recovered",
    "provider_simulated": True,
    "job": "recoverable-job",
    "remote_id": "controlled-recovery-0001",
    "unresolved_job": "unresolved-job",
    "unresolved_state": uj["state"],
    "candidate": {
        "id": imp["candidate_id"],
        "output": imp["output_id"],
        "path": imp["path"],
        "sha256": h(imp["path"]),
    },
    "state": {
        "path": ".pixl/recovery/state.px",
        "sha256": state_sha,
        "canonical_hash": caller_jobs["hash"],
        "revision": caller_jobs["revision"],
    },
    "native_child": {
        "agent_type": "pixl:pixl",
        "agent_id": "afd16d3e3ae5638bc",
        "host": "claude",
        "completed": True,
        "reported_status": spec["status"],
        "tool_uses": 37,
        "duration_ms": 455286,
    },
    "specialist_result": {
        "path": "work/provider-recovery/phase-2/SPECIALIST-RESULT.json",
        "sha256": spec_sha,
    },
    "caller_verification": {
        "written_at": now,
        "timestamp_source": "host clock via selected Python datetime.now(timezone.utc) at the moment this file was composed",
        "cold_read_before_delegation": {
            "revision": 8,
            "canonical_hash": BEFORE_HASH,
            "recoverable_job_next_action": "retrieve_outputs",
            "unresolved_job_state": "unknown",
            "assets_robot_png_existed": False,
        },
        "jobs_report_source": "mcp__pixl-local__pixl_jobs path=.pixl/recovery/state.px, retrieved independently by the caller after child completion and saved as caller-jobs.json",
        "caller_jobs_semantically_equal_to_specialist_jobs_after": caller_jobs == jobs_after,
        "caller_jobs_sha256": h("work/provider-recovery/phase-2/caller-jobs.json"),
        "specialist_jobs_after_sha256": h("work/provider-recovery/phase-2/jobs-after.json"),
        "pixl_validate_after": {
            "valid": True,
            "revision": 9,
            "hash": AFTER_HASH,
            "records": 30,
            "files_verified": True,
            "re_run_after_caller_copy": "same revision and hash; the asset copy did not touch the store",
        },
        "state_file_sha256_equals_canonical_hash": state_sha == caller_jobs["hash"],
        "recoverable_job": {
            "state": rj["state"],
            "remote_id": rj["remote_id"],
            "next_action": rj["next_action"],
            "missing_outputs": rj["recovery"]["missing_outputs"],
            "imported": rj["recovery"]["imported"],
            "events": len(rj["events"]),
            "last_event": rj["events"][-1]["event"],
            "last_event_recorded_at": rj["events"][-1]["recorded_at"],
        },
        "unresolved_job": {
            "state": uj["state"],
            "remote_id": uj["remote_id"],
            "events": len(uj["events"]),
            "modified_this_phase": False,
        },
        "candidate_verification": {
            "path_source": "recovery.imported[0].path of recoverable-job in the caller's own current pixl_jobs report",
            "declared_sha256": imp["sha256"],
            "rehashed_sha256": h(cand),
            "bytes": sz(cand),
            "byte_identical_to_retrieved_png": h(cand) == h("work/provider-recovery/phase-2/retrieved.png"),
            "phase1_partial_is_exact_59_byte_prefix": cand_bytes[:59] == part_bytes and len(part_bytes) == 59,
            "pixl_asset_check": {
                "pass": True,
                "width": 32,
                "height": 32,
                "frame_count": 1,
                "visible_pixels": 390,
                "visible_colors": 3,
                "opaque_components": 1,
                "visual_quality_verified": False,
                "engine_import_verified": False,
            },
            "opened_with_image_tool": "Read tool rendered the retained candidate PNG and assets/robot.png; both displayed as a small 32x32 sprite. Mechanical open only, not artistic acceptance.",
            "provider_response_match": {
                "fresh_get_image_path": "work/provider-recovery/phase-2/provider-get-image.json",
                "declared_bytes": 177,
                "declared_sha256": EXPECTED_SHA,
                "fresh_download_url": "http://127.0.0.1:6664/controlled-recovery-0001.png",
                "phase1_url_not_reused": "http://127.0.0.1:7099/controlled-recovery-0001.png",
                "matches_retained_bytes": h(cand) == EXPECTED_SHA and sz(cand) == 177,
            },
        },
        "import_evidence_check": {
            "import_evidence_json_is_specialist_supplied_evidence": True,
            "import_result_revision": 9,
            "import_result_hash": AFTER_HASH,
            "reused_import": False,
            "candidate_record_sha256": imp["record_sha256"],
        },
        "specialist_evidence_refs_rehashed_by_caller": all(h(r["path"]) == r["sha256"] for r in spec["evidence_refs"]),
        "specialist_evidence_refs_count": len(spec["evidence_refs"]),
        "phase1_files_unchanged": {
            "download.part": h("work/provider-recovery/phase-1/download.part") == "c782e097dc9ebb50682becc305d82839e4ee73c38926dd9dd6495b75ed037c4f",
            "download-error.json": h("work/provider-recovery/phase-1/download-error.json") == "a20dde823756d0d4052e3a3dc483483ab7ad8f29a9e25947c3d2091b391b4af3",
            "SPECIALIST-RESULT.json": h("work/provider-recovery/phase-1/SPECIALIST-RESULT.json") == "b1a545691c47e30dd7c975eaa95e3b635e7e241ae5af7acf824d801f051f5f46",
            "jobs-after.json": h("work/provider-recovery/phase-1/jobs-after.json") == "86c4f8bf9a9194cbea27b3bfe24174d746d160c8fbb4b133368366b7056d48a2",
        },
        "integration": {
            "source": "src/avatar.ts",
            "source_sha256": h("src/avatar.ts"),
            "source_line": avatar_ts,
            "expected_path": "assets/robot.png",
            "expected_width": 32,
            "expected_height": 32,
            "sampling": "nearest",
            "assets_robot_png_created_by": "caller, via byte copy of the retained candidate file (cp), after confirming assets/robot.png did not exist",
            "assets_robot_png_sha256": h("assets/robot.png"),
            "assets_robot_png_bytes": sz("assets/robot.png"),
            "byte_identical_to_candidate": h("assets/robot.png") == h(cand),
            "dimensions_match_avatar_ts": True,
            "acceptance": "unaccepted for art; mechanical byte copy only",
        },
        "reference_pixels_not_copied": "assets/robot.png and the candidate derive from the fresh download of the originating resource (retrieved.png -> retained artifact), not from reference.png, although reference.png has the same sha256 by fixture design.",
    },
    "evidence_refs": [{"path": p, "sha256": h(p)} for p in refs],
    "limitations": [
        "No live PixelLab: the provider is the controlled pixellab-recovery-test fixture with provider_simulated=true; no new submission, dispatch, prepare, generate, upload or paid work occurred in this phase by either participant.",
        "Recovery is mechanical only: the retained candidate recovered-avatar-candidate (177 bytes, sha256 " + EXPECTED_SHA + ") matches the originating response byte identity and decodes as a 32x32 RGBA PNG, but no artistic, target-engine or human acceptance was performed or claimed; pixl_asset_check reports visual_quality_verified=false and engine_import_verified=false.",
        "Import grants no acceptance: candidate nominated=false, criterion q.bytes status unperformed with no verdict; no candidate review, nomination or task completion was recorded by either participant.",
        "assets/robot.png is an exact byte copy of the retained candidate created by the caller and is clearly unaccepted for art; it satisfies only the path and 32x32 dimensions declared in src/avatar.ts.",
        "unresolved-job remains unknown with remote_id null and its original two events; it was not observed, modified or resolved, and absence from the fixture listing is not proof of non-acceptance.",
        "The caller wrote only caller-jobs.json, scripts/write_caller_result.py, CALLER-RESULT.json and assets/robot.png; the store was mutated once, by the specialist's single pixl_job_import (revision 8 -> 9). Phase-1 files are unchanged (re-hashed by the caller).",
        "M1/M2 and broader M3/M4 remain open.",
        "The native child's agent ID is the host-reported subagent ID for this fresh phase-2 run; this phase is not a same-session or same-child continuation of phase 1.",
        "caller-jobs.json is semantically equal to the specialist's jobs-after.json (parsed JSON equality); the two files differ in byte serialization, so their SHA-256 values differ.",
        "The evidence_refs entry for scripts/write_caller_result.py hashes the script that composed this file; CALLER-RESULT.json itself is not self-referenced.",
    ],
    "next_action": "Phase 3 cold consumption by a fresh caller and fresh pixl:pixl child on the same root/store/kit: read current public jobs/workflow reports and pixl_validate (expect revision 9, hash " + AFTER_HASH + " unless changed); consume the exact retained candidate recovered-avatar-candidate at " + cand + " (sha256 " + EXPECTED_SHA + ", 177 bytes) and confirm assets/robot.png is still byte-identical to it and matches src/avatar.ts (32x32, nearest); confirm recoverable-job reads inspect_candidates with no missing outputs and unresolved-job is still unknown. No new dispatch, prepare, get_image re-query, download or job-import is authorized; any q.bytes verdict or nomination remains a separate deliberate review step.",
}

out = os.path.join(root, "work/provider-recovery/phase-2/CALLER-RESULT.json")
with open(out, "w", encoding="utf-8", newline="\n") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
    f.write("\n")

cv = doc["caller_verification"]
print("written_at", now)
print("specialist_evidence_refs_rehashed_by_caller", cv["specialist_evidence_refs_rehashed_by_caller"])
print("caller_jobs==jobs_after", cv["caller_jobs_semantically_equal_to_specialist_jobs_after"])
print("phase1_unchanged", cv["phase1_files_unchanged"])
print("state_sha==canonical", cv["state_file_sha256_equals_canonical_hash"])
print("candidate rehash", cv["candidate_verification"]["rehashed_sha256"], cv["candidate_verification"]["bytes"])
print("prefix check", cv["candidate_verification"]["phase1_partial_is_exact_59_byte_prefix"])
with open(out, "rb") as f:
    print("CALLER-RESULT.json sha256", hashlib.sha256(f.read()).hexdigest())
