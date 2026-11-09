"""Caller-authored REVIEW-RESULT.json for the native candidate/family review trial.

Reads only retained project files; publishes nothing to PIXL state.
"""

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
NR = ROOT / "work" / "native-review"


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


# Corrected copy of the specialist's malformed snapshot result (raw Windows path not JSON-escaped).
raw = (NR / "04-family-snapshot-result.json").read_text(encoding="utf-8")
try:
    json.loads(raw)
    snapshot_result_valid = True
except json.JSONDecodeError:
    snapshot_result_valid = False
    fixed = json.loads(raw.replace("\\", "\\\\"))
    fixed["_caller_note"] = "Corrected copy of 04-family-snapshot-result.json, whose original text left Windows path backslashes unescaped; the original is preserved unchanged."
    (NR / "04-family-snapshot-result.caller-corrected.json").write_text(json.dumps(fixed, indent=2) + "\n", encoding="utf-8")

working_req = load("work/native-review/02-working-review-request.json")
family_req = load("work/native-review/07-family-review-request.json")
working_res = load("work/native-review/02-working-review-result.json")
family_res = load("work/native-review/07-family-review-result.json")
replay_spec = load("work/native-review/10-family-replay-result.json")
replay_caller = load("work/native-review/12-caller-family-replay-result.json")
check_spec = load("work/native-review/destination-01-check.json")
check_caller = load("work/native-review/caller-destination-01-recheck.json")
render = load("work/native-review/destination-01/render.json")
motion = load("work/native-review/destination-01/motion.json")
reduced_raw = load("work/native-review/destination-01/reduced-render.raw.json")
manifest_rel = ".pixl/assets/queue.ready/deliveries/ec59b8245619463446cb86b639e7b387e748917fb5c520a085984b85c89df5d0/manifest.json"
manifest = load(manifest_rel)

member_checks = []
asset_paths = {
    "ready.retained": "renderer-successor/assets/ready-confirmed.png",
    "provenance-correction.working.candidate": "renderer-successor/assets/working.png",
    "provenance-correction.retry.candidate": "renderer-successor/assets/error-retry.png",
    "provenance-correction.paused.candidate": "renderer-successor/assets/paused.png",
}
for f in manifest["files"]:
    copied = sha(Path(manifest_rel).parent.as_posix() + "/" + f["path"])
    renderer_asset = sha(asset_paths[f["candidate"]])
    served = render["served_files"]["consumer/" + asset_paths[f["candidate"]]]
    member_checks.append({
        "member": f["candidate"],
        "manifest_sha256": f["sha256"],
        "copied_file_sha256_matches": copied == f["sha256"],
        "renderer_successor_asset_matches": renderer_asset == f["sha256"],
        "served_bytes_in_destination_run_match": served == f["sha256"],
    })

phases = {p["name"]: sorted({c["frame"] for s in p["samples"] for c in s["cells"]}) for p in motion["phases"]}
changes = motion["phases"][-1]["samples"][-1]["changes"]

result = {
    "trial": "candidate-review/20261109/native/claude-01",
    "assignment": "REVIEW-ASSIGNMENT.md",
    "written_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    "roles": {
        "caller": "Claude Code main session (claude-fable-5-1, Claude Code 2.1.318) acting as the caller; owns the independent checks below and authored this file.",
        "specialist": "Native Claude Code subagent spawned via the Agent tool with subagent_type \"pixl\" (declared in the harness --agents file as 'PixelLab visual asset specialist for this retained asset review'), running the PIXL profile from .agents/skills/review-kit. It is a generic host child carrying the PIXL role; no separately trained model or human reviewer is claimed. Its own statement is in work/native-review/SPECIALIST-REPORT.json.",
        "reviewer_actor_in_state": "actor",
    },
    "kit": {"current": ".agents/skills/review-kit", "historical_preserved": ".agents/skills/pixl-kit"},
    "state": {
        "path": ".pixl/assets/queue.ready/state.px",
        "store": ".pixl/assets/queue.ready",
        "start": {"revision": 119, "state_hash": "f2eb516254a10adf57d60153edfc9a3365868b6e23cc1be42d93ea80079d9300"},
        "current": {"revision": 126, "state_hash": "23718b6d027836af49f3548fcb38979bd4afca032e8113d7a9222c7c570c8c49", "valid": True, "records": 794, "files_verified": True},
        "publications": {
            "native-review.working.motion": [120, 121, 122],
            "family_snapshot": [123],
            "native-review.family.collective": [124, 125, 126],
        },
    },
    "reviewed": {
        "working": {
            "candidate": "provenance-correction.working.candidate",
            "candidate_sha256": "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc",
            "output": "provenance-correction.working.output",
            "task": "provenance-correction.working.task",
            "binding_hash": working_req["binding_hash"],
            "review_id": "native-review.working.motion",
            "review_sha256": working_res["review_sha256"],
            "review_report": working_res["review_path"],
            "observed_at": working_req["observed_at"],
            "action": working_req["action"],
            "verdicts": [{"criterion": v["criterion"], "status": v["status"], "supersedes": v["supersedes"], "new_verdict": "native-review.working.motion.verdict.0"} for v in working_req["verdicts"]],
            "task_status_after": "done",
            "all_required_pass_after": True,
            "request": "work/native-review/02-working-review-request.json",
            "result": "work/native-review/02-working-review-result.json",
            "context_before": "work/native-review/01-working-review-context.json",
            "context_after": "work/native-review/03-working-review-context-after.json",
        },
        "family": {
            "candidate": "native-review.family.candidate",
            "output": "provenance-correction.delivery.output",
            "task": "provenance-correction.delivery.task",
            "package": str(Path(manifest_rel).parent.as_posix()),
            "manifest": manifest_rel,
            "manifest_sha256": sha(manifest_rel),
            "manifest_created_at": manifest["created_at"],
            "snapshot_acceptance": {"accepted": False, "source_state_hash": "5c9c540938591271fd7ddf80ed9d591f3eb1b904c86f823776cb687317742a4a", "note": "Immutable manifest creation status; unchanged by review."},
            "current_acceptance": {"all_required_pass": True, "task_complete": True, "nominated": True},
            "binding_hash": family_req["binding_hash"],
            "review_id": "native-review.family.collective",
            "review_sha256": family_res["review_sha256"],
            "review_report": family_res["review_path"],
            "observed_at": family_req["observed_at"],
            "action": family_req["action"],
            "verdicts": [{"criterion": v["criterion"], "status": v["status"], "supersedes": v["supersedes"], "new_verdict": f"native-review.family.collective.verdict.{i}", "observation_count": len(v["observations"])} for i, v in enumerate(family_req["verdicts"])],
            "members": member_checks,
            "request": "work/native-review/07-family-review-request.json",
            "result": "work/native-review/07-family-review-result.json",
            "snapshot_result": "work/native-review/04-family-snapshot-result.json",
            "snapshot_result_valid_json": snapshot_result_valid,
            "snapshot_result_corrected_copy": None if snapshot_result_valid else "work/native-review/04-family-snapshot-result.caller-corrected.json",
            "family_report_before": "work/native-review/05-family-report.json",
            "family_report_after": "work/native-review/09-family-report-after.json",
            "context_before": "work/native-review/06-family-review-context.json",
            "context_after": "work/native-review/08-family-review-context-after.json",
        },
    },
    "replay": {
        "specialist": {"result": "work/native-review/10-family-replay-result.json", "reused_review": replay_spec["reused_review"], "publications": replay_spec["publications"], "revision": replay_spec["revision"], "state_hash": replay_spec["state_hash"]},
        "caller_via_kit_cli": {"result": "work/native-review/12-caller-family-replay-result.json", "command": "pixl.py candidate-review .pixl/assets/queue.ready native-review.family.candidate native-review.family.collective work/native-review/07-family-review-request.json --expect 23718b6d... --root <project>", "reused_review": replay_caller["reused_review"], "publications": replay_caller["publications"], "revision": replay_caller["revision"], "state_hash": replay_caller["state_hash"], "review_sha256": replay_caller["review_sha256"]},
        "conclusion": "Both identical replays returned reused_review true with no publications, unchanged revision 126 / state hash, the same review report sha and the same three verdict IDs.",
    },
    "renderer_evidence": {
        "runner": "renderer-successor/capture.mjs + renderer-successor/check.py (existing isolated fixture, headless Chrome via CDP)",
        "capture_dir": "work/native-review/destination-01",
        "render_json_sha256": sha("work/native-review/destination-01/render.json"),
        "motion_json_sha256": sha("work/native-review/destination-01/motion.json"),
        "destination_png_sha256": sha("work/native-review/destination-01/destination.png"),
        "browser": render["browser_version"].get("product"),
        "observed_at": render["observed_at"],
        "errors": render["errors"],
        "missing": render["missing"],
        "timeline_frames": [[s["elapsed"], s["frame"]] for s in render["timeline"]],
        "motion_phases_frames_observed": phases,
        "preference_transitions": changes,
        "specialist_check": {"path": "work/native-review/destination-01-check.json", "sha256": sha("work/native-review/destination-01-check.json"), "status": check_spec["status"], "observations": len(check_spec["observations"]), "failures": check_spec["failures"]},
        "caller_recheck": {"path": "work/native-review/caller-destination-01-recheck.json", "sha256": sha("work/native-review/caller-destination-01-recheck.json"), "status": check_caller["status"], "observations": len(check_caller["observations"]), "failures": check_caller["failures"], "identical_to_specialist_check": sha("work/native-review/caller-destination-01-recheck.json") == sha("work/native-review/destination-01-check.json")},
        "failed_captures": [],
    },
    "images_viewed": {
        "specialist": "Listed with sha256 in work/native-review/SPECIALIST-REPORT.json (images_viewed) and bound as observations in the two review requests: 16 visual observations for motion, 27 visual + 20 live for the family.",
        "caller": [
            {"path": "work/native-review/destination-01/destination.png", "sha256": sha("work/native-review/destination-01/destination.png"), "saw": "Succeeded live cells show Ready; state matrix shows Start/Working/Paused/Ready/Retry at 1x and 3x in both consumers; no missing markers."},
            {"path": "work/native-review/destination-01/reduced-live.png", "sha256": sha("work/native-review/destination-01/reduced-live.png"), "saw": "Running state under reduce: both live Working cells show stationary frame zero."},
            {"path": "work/native-review/frames/working-strip-12x.png", "sha256": sha("work/native-review/frames/working-strip-12x.png"), "saw": "Four Working frames enlarged; each is the previous rotated a quarter turn, same segment count and weight."},
            {"path": "work/native-review/frames/working-wrap-3-0-1-12x.png", "sha256": sha("work/native-review/frames/working-wrap-3-0-1-12x.png"), "saw": "Frames 3,0,1 side by side; the wrap step is the same increment as the other steps."},
            {"path": "work/native-review/frames/family-members-12x-color.png", "sha256": sha("work/native-review/frames/family-members-12x-color.png"), "saw": "Check, four Working frames, Retry ring-arrow, pause bars, Start triangle in cool blue on the panel colour."},
            {"path": "work/native-review/frames/family-members-12x-gray.png", "sha256": sha("work/native-review/frames/family-members-12x-gray.png"), "saw": "Same set in grayscale; each symbol remains identifiable by structure alone."},
            {"path": "work/acceptance-01/headless-review-03/playback.png", "sha256": sha("work/acceptance-01/headless-review-03/playback.png"), "saw": "Recorded playback page: color and grayscale family rows plus 17 captured transitions 0,1,2,3,0,... at ~100 ms steps."},
            {"path": "work/acceptance-01/observed-views/transition-03-3x-color.png", "sha256": sha("work/acceptance-01/observed-views/transition-03-3x-color.png"), "saw": "Recorded 3x exposure of frame 3."},
            {"path": "work/acceptance-01/observed-views/transition-04-3x-color.png", "sha256": sha("work/acceptance-01/observed-views/transition-04-3x-color.png"), "saw": "Recorded 3x exposure of frame 0 after the wrap."},
        ],
        "caller_note": "The caller viewed these to confirm the bound evidence is what the specialist describes; the artistic verdicts remain the specialist's.",
    },
    "caller_independent_verification": [
        "pixl_review_context on provenance-correction.working.candidate after the run: task done, nominated, all eight criteria pass, motion-continuity verdict is native-review.working.motion.verdict.0 (unavailable verdict superseded), binding_hash unchanged 835ff4ed..., state revision 126.",
        "pixl_review_context on native-review.family.candidate: task done, nominated, three collective criteria pass with verdicts native-review.family.collective.verdict.0/1/2; snapshot_acceptance.accepted stays false while current_acceptance is all_required_pass/task_complete true.",
        "pixl_validate: state valid, format 2, revision 126, hash 23718b6d..., 794 records, files_verified true; new records limited to native-review.* review/file/evidence/verdict records and the family candidate.",
        "Manifest ec59b824...: member order Ready, Working, Retry, Paused; each copied files/000N.png sha256 equals the manifest entry, the renderer-successor/assets file, the assets/ file and the served bytes recorded by the destination run.",
        "Re-ran renderer-successor/check.py on the specialist's capture: pass, 233 observations, zero failures, byte-identical output to the specialist's check file.",
        "Read render.json/motion.json/reduced-render.raw.json directly: no script errors, no missing assets, timeline 0,0,1,1,2,2,3,3,0 at 0..400 ms, phases normal {0,1,2,3} / reduced {0} / normal {0,1,2,3}, one preference transition each way via the animation-frame route (at ~1322.6 ms and 2473 ms).",
        "Both retained review reports hash to their directory names; all 18 and 48 retained observation files match their recorded sha256.",
        "Replayed the identical family review through the kit CLI with the current state hash: reused_review true, publications [], revision/state hash unchanged.",
        "Files modified during the session outside work/native-review are confined to the store: state.px, seven new history revisions (120-126), the new delivery package and the two review directories. No pre-existing file, source, artwork, requirements file or historical evidence was changed; assets/, renderer-successor/assets/ and start.svg hashes are unchanged.",
        "Viewed the key images listed above with the host image viewer.",
    ],
    "unresolved_issues": [
        "The specialist's saved copy work/native-review/04-family-snapshot-result.json is not valid JSON (Windows path backslashes unescaped). The original is preserved; a corrected copy was written alongside it. The snapshot itself is verified in state.",
        "The specialist hashed but did not open two decoded 1x grayscale family views (idle, failed); its Start/Retry grayscale judgments rest on the 3x gray views and composite sheets, which are bound as observations.",
        "The 'byte-unchanged old consumer' condition in q.destination was verified against hashes recorded in earlier project evidence, not version control, because this copied consumer directory is untracked.",
    ],
    "scope_and_limits": [
        "This trial evaluates the candidate-review/family-snapshot interface on retained PixelLab-derived assets through a native PIXL child; it does not establish general generated-art quality, destination behaviour beyond this headless Chrome 156 fixture at DPR 1, or host reliability in general.",
        "Motion and collective judgments were made from recorded exposures and enlargements viewed as ordered images, not real-time viewing; wall-clock frame duration is not measured by the fixture.",
        "No PixelLab remote call, generation, state.px hand-edit or generic commit was used; no global settings or memory were changed.",
    ],
    "key_files": {
        "specialist_report": {"path": "work/native-review/SPECIALIST-REPORT.json", "sha256": sha("work/native-review/SPECIALIST-REPORT.json")},
        "workflow_after": "work/native-review/11-workflow-after.json",
        "caller_script": "work/native-review/scripts/caller-review-result.py",
    },
}

out = json.dumps(result, indent=2) + "\n"
(ROOT / "REVIEW-RESULT.json").write_text(out, encoding="utf-8")
(NR / "REVIEW-RESULT.json").write_text(out, encoding="utf-8")
print(json.dumps({"written": ["REVIEW-RESULT.json", "work/native-review/REVIEW-RESULT.json"], "sha256": hashlib.sha256(out.encode()).hexdigest(), "snapshot_result_valid_json": snapshot_result_valid}))
