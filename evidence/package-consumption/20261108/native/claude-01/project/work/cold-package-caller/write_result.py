"""Caller: write caller-comparison.json and PACKAGE-RESULT.json from the caller's own measurements."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def h(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def ref(p):
    return {"path": p, "sha256": h(p), "bytes": (ROOT / p).stat().st_size}


def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


now = datetime.datetime.now(datetime.timezone.utc).isoformat()
hashes = load("work/cold-package-caller/hashes.json")
meas = load("work/cold-package-caller/asset-measurements.json")
pres = load("work/cold-package-caller/preservation-diff.json")
chk = load("work/cold-package-caller/check-rerun.json")
rs = load("work/cold-package-caller/render-summary.json")
after = load("work/cold-package-caller/plar-read-working-after.json")
spec = load("work/cold-package/specialist-result.json")
PKG = ".pixl/assets/queue.ready/deliveries/78d45b4dbeef06f376356e0bcbec8f8a8b09b034f999db7903369f22beaff0f7"
manifest = load(PKG + "/manifest.json")
start_preserved = load("work/live-family/package-integration.json")["start_preserved_sha256"]
HANDOFF = ".pixl/handoffs/4465bc2039e7647e305b286ea0b95b5b4d05268c6d9f156b0ff92b55cff7fc87.json"
NEW_HANDOFF = ".pixl/handoffs/d2d79e431ae1d7ac30ae15fdad33610b2173f403ea3b229d6e12a05020ac0e8e.json"
STATE_HASH = "ef6de040931d9ce9e6e9a09fe2c57d6cad1242db6fb6c9579ef1eac0fd70759d"

members = [
    ("assets/ready-confirmed.png", "succeeded", "Ready", 1, "ready.retained"),
    ("assets/working.png", "running", "Working", 4, "live.working-animation-motion-01.candidate"),
    ("assets/error-retry.png", "failed", "Retry", 1, "live.retry.candidate"),
    ("assets/paused.png", "paused", "Paused", 1, "live.paused-cutout-01.candidate"),
]
files = []
identity_ok = True
for i, (dest, state, label, frames, cand) in enumerate(members):
    m = manifest["files"][i]
    copy = f"{PKG}/files/000{i}.png"
    art = m["source_path"]
    hs = {"destination": h(dest), "package_copy": h(copy), "artifact_source": h(art), "manifest_declared": m["sha256"]}
    same = len(set(hs.values())) == 1 and m["candidate"] == cand
    identity_ok &= same
    mm = meas[dest]
    files.append({
        "state": state, "label": label, "destination": dest, "sha256": hs["destination"],
        "bytes": (ROOT / dest).stat().st_size, "package_copy": copy, "artifact_source": art,
        "candidate": cand, "manifest_candidate": m["candidate"], "identity_consistent": same,
        "width": mm["size"][0], "height": mm["size"][1], "frames": frames, "frame_size": [16, 16],
        "transparent_pixels": mm["transparent"], "opaque_pixels": mm["opaque"],
        "partial_alpha_pixels": mm["partial_alpha"], "visible_color_count": len(mm["visible_colors"]),
    })
start = {
    "state": "idle", "label": "Start", "destination": "assets/start.svg", "sha256": h("assets/start.svg"),
    "bytes": (ROOT / "assets/start.svg").stat().st_size,
    "role": "pre-existing vector, preserved, not a package member",
    "matches_package_integration_start_preserved_sha256": h("assets/start.svg") == start_preserved,
}
prod = after["production"]
frame_seq = [s[1][0] for s in rs["samples"]]
claims = [
    {"claim": "package copy = artifact source = destination = manifest sha256 for all four members; manifest candidates equal nominees",
     "caller_result": "confirmed" if identity_ok else "MISMATCH", "evidence": "work/cold-package-caller/hashes.json"},
    {"claim": "manifest.json sha256 equals its directory name 78d45b4d...",
     "caller_result": "confirmed" if hashes[PKG + "/manifest.json"] == "78d45b4dbeef06f376356e0bcbec8f8a8b09b034f999db7903369f22beaff0f7" else "MISMATCH"},
    {"claim": "renderer-live capture exit 0; check.py pass with 404 observations, 0 failures, 20 views",
     "caller_result": f"confirmed by caller re-run: exit 0, status {chk['status']}, {len(chk['observations'])} observations, failures {chk['failures']}, views {chk['available_views']}",
     "evidence": "work/cold-package-caller/check-rerun.json"},
    {"claim": "frames 1-3 are exact clockwise quarter-turns of frame 0; frame 0 equals seed visible pixels; three clusters 8/9/15 per frame; 32 visible px per frame",
     "caller_result": "confirmed by independent Pillow computation", "evidence": "work/cold-package-caller/asset-measurements.json"},
    {"claim": "live playback 13 samples, sequence 0,1,2,3 three times then 0, wraps at 403.3/803.3/1203.3 ms, both consumers",
     "caller_result": f"confirmed from render.json: {len(rs['samples'])} samples, wraps {rs['wraps_3_to_0']}, frames {frame_seq}",
     "evidence": "work/cold-package-caller/render-summary.json"},
    {"claim": "transitions idle/started/pause/ok/error map to Start/Working/Paused/Ready/Retry in both consumers, all available, no errors, no missing",
     "caller_result": "confirmed from render.json transitions; errors [] and missing []"},
    {"claim": "capture ran against this copied consumer, not the original production workspace",
     "caller_result": "confirmed: work/cold-package/render-01/launch.json project is this project root; served consumer bytes equal current src/ and assets/ hashes; browser-process.json code 0"},
    {"claim": "no pre-existing file modified; only the new handoff d2d79e43... was added",
     "caller_result": f"confirmed by caller inventory diff: {pres['baseline_count']} -> {pres['after_count']} files, added {pres['added']}, removed {pres['removed']}, changed {pres['changed']}",
     "evidence": "work/cold-package-caller/preservation-diff.json"},
    {"claim": "plar read queue.working still returns delivered with state ef6de040 revision 85 after the session",
     "caller_result": f"confirmed: next_action {prod['next_action']}, hash {prod['hash'][:8]}, revision {prod['revision']}, pending_jobs {prod['pending_jobs']}, selection_current {prod['selection_current']}",
     "evidence": "work/cold-package-caller/plar-read-working-after.json"},
    {"claim": "provider job IDs cited for seed, animation, repair, motion, retry and paused attempts",
     "caller_result": "all ten cited remote IDs, including controlled-create-0001/0002, found in work/cold-package/jobs.json; the three Working job IDs also appear in the current handoff resume.jobs"},
    {"claim": "acceptance occurred at revisions 84-85 after the revision-80 snapshot",
     "caller_result": "confirmed: work/live-family/family-completion.json publications revision 84 (8bc85500...) and 85 (ef6de040...); snapshot revision 80"},
    {"claim": "historical Ready drift: r.22e90a2a03fe453a.task and the open 'task' carry plar_selection blockers",
     "caller_result": "confirmed in work/cold-package/workflow.json task blockers; both are historical Ready-stage tasks; family and production member tasks have no blockers"},
    {"claim": "visual: full and compact views identical; Start triangle, Working three orbiting segments, Paused two bars, Ready asymmetric check, Retry circular arrow with head",
     "caller_result": "confirmed by the caller viewing destination.png and caller-built 8x and 4x sheets from the capture views; caller also notes visible blue-to-teal hue variation inside the Paused bars and mild shading inside Working and Retry clusters, all readable at 1x; Ready is a single colour",
     "evidence": ["work/cold-package/render-01/destination.png", "work/cold-package-caller/caller-matrix-8x.png", "work/cold-package-caller/caller-playback-4x.png"]},
    {"claim": "Working motion: rigid quarter-turn steps, no morphing, clean 3->0 wrap",
     "caller_result": "confirmed visually on caller-playback-4x.png: every 100 ms step including each wrap is the same quarter-turn of the same three shapes; both consumer rows identical"},
]
comparison = {
    "version": 1, "observed_at": now,
    "caller": "Claude Fable 5.1 native caller (Claude Code 2.1.318), PACKAGE-CONSUMPTION evaluation",
    "assignment": ref("PACKAGE-CONSUMPTION.md"),
    "specialist": {
        "agent_type": "pixl (agents.json profile, native Claude Code subagent)", "agent_id": "a5bc1206e811b8dfa",
        "mode": "foreground Agent call with run_in_background false; caller waited for completion",
        "reported_duration_ms": 520752, "reported_tool_uses": 54,
        "result": ref("work/cold-package/specialist-result.json"), "status_claimed": spec["status"],
        "mismatches_claimed": spec["mismatches"],
        "resumption": "No SendMessage follow-up was needed; the specialist completed in one conversation. No artifact-based restart occurred.",
    },
    "claims_checked": claims,
    "discrepancies": [
        {"severity": "none", "note": "The specialist wrote an optional new handoff record (" + NEW_HANDOFF + ") restating the unchanged continuation: next delivered, same state and requirements hashes. The caller permitted this only as a new file; the inventory diff confirms no pre-existing file changed. The authoritative current handoff remains 4465bc20..., cited by CURRENT-HANDOFF.md through work/live-family/HANDOFF-current.json."},
        {"severity": "none", "note": "The specialist did not save raw MCP tool outputs; it saved CLI equivalents under work/cold-package/. The caller re-derived the key facts (state hash, revision, task states, family acceptance) from its own plar read runs and those CLI files."},
        {"severity": "informational", "note": "Neither the specialist nor the caller regenerated a grayscale comparison; non-colour distinction was judged from silhouettes on enlarged colour sheets. The retained grayscale verdict (live.family.distinction.verdict) is historical evidence and was not re-established here."},
    ],
    "caller_independent_checks": {
        "preservation": pres, "hashes": "work/cold-package-caller/hashes.json",
        "check_rerun": {"command": "python -I renderer-live/check.py --project . --capture work/cold-package/render-01", "exit_code": 0, "status": chk["status"], "observations": len(chk["observations"]), "failures": chk["failures"], "available_views": chk["available_views"], "capture_sha256": chk["capture_sha256"]},
        "asset_measurements": "work/cold-package-caller/asset-measurements.json",
        "render_summary": "work/cold-package-caller/render-summary.json",
        "source_consumer_executor": {"command": "node verify-integration.mjs assets/ready-confirmed.png", "exit_code": 0, "result": "work/cold-package-caller/verify-integration-ready.json", "meaning": "statusCell and compactStatus both return assets/ready-confirmed.png with 1 frame for the succeeded state; PNG header 16x16; display filter nearest. Not a renderer."},
        "plar_read_before": "work/cold-package-caller/plar-read-working-before.json",
        "plar_read_after": "work/cold-package-caller/plar-read-working-after.json",
        "images_viewed_by_caller": ["work/cold-package/render-01/destination.png", "work/cold-package-caller/caller-matrix-8x.png", "work/cold-package-caller/caller-playback-4x.png"],
    },
    "verdict": "Specialist evidence agrees with the assignment, the real files and both consumers; no mismatch prevents honest consumption.",
}
(ROOT / "work/cold-package-caller/caller-comparison.json").write_text(json.dumps(comparison, indent=2), encoding="utf-8")
cmp_ref = ref("work/cold-package-caller/caller-comparison.json")

result = {
    "version": 1, "observed_at": now,
    "assignment": ref("PACKAGE-CONSUMPTION.md"),
    "status": "delivered",
    "status_scope": "Judged against the PACKAGE-CONSUMPTION.md consumption assignment: the delivered four-member queue family was recovered from the current handoff, verified byte-for-byte, rendered again through both actual consumers in this copied project and inspected. This is not a new art-quality verdict, human acceptance, another engine's acceptance or a host-reliability claim.",
    "current_handoff": {
        "entry": ref("CURRENT-HANDOFF.md"),
        "pointer": ref("work/live-family/HANDOFF-current.json"),
        "handoff": ref(HANDOFF),
        "asset_id": "queue.working", "requirements_hash": after["requirements_hash"],
        "store": ".pixl/assets/queue.ready", "state": ref(".pixl/assets/queue.ready/state.px"),
        "state_hash_in_handoff": STATE_HASH, "revision": prod["revision"],
        "plar": ref("plar.txt"), "selection_current": prod["selection_current"],
        "next": prod["next_action"],
        "reread_command": "C:/github/pixel-lab-agent/.venv/Scripts/python.exe ../kit/scripts/pixl.py plar read --root . --asset queue.working",
        "reread_results": {
            "before_delegation": ref("work/cold-package-caller/plar-read-working-before.json"),
            "after_delegation": ref("work/cold-package-caller/plar-read-working-after.json"),
            "both_return": "next_action delivered; task family.working.task done; delivery complete and destination matches; family.delivery.task done with live.family.candidate accepted and member_selection_current true; pending_jobs []",
        },
        "package": {
            "snapshot": ref("work/live-family/family-snapshot.json"), "manifest": ref(PKG + "/manifest.json"),
            "collective_review": ref("work/live-family/collective-review.json"),
            "package_integration": ref("work/live-family/package-integration.json"),
        },
        "specialist_restatement_handoff": {**ref(NEW_HANDOFF), "note": "Written by the specialist this session; same asset, requirements hash, state hash and next=delivered. Optional restatement, not a new acceptance; the handoff cited by CURRENT-HANDOFF.md above remains the entry."},
    },
    "delivered_files": files + [start],
    "slicing_and_timing": {
        "cell": [16, 16], "panel_background": "#172336",
        "sampling": "nearest (canvas imageSmoothingEnabled false; CSS image-rendering: pixelated)", "display_scales": [1, 3],
        "consumers": {"statusCell": "full view", "compactStatus": "compact view", "note": "both return the same statusVisuals descriptor per state (src/queue-view.ts), so one shared asset per state"},
        "state_map": {"idle": "assets/start.svg (1 frame)", "running": "assets/working.png (4 frames)", "paused": "assets/paused.png (1 frame)", "succeeded": "assets/ready-confirmed.png (1 frame)", "failed": "assets/error-retry.png (1 frame)"},
        "working": {"sheet": "64x16, four horizontal 16x16 frames, frame i at source rect (i*16, 0, 16, 16)", "frame_ms": 100, "loop_ms": 400, "frame_selection": "floor(max(elapsed,0)/100) mod 4", "wrap": "frame 3 -> frame 0", "motion": "frames 1-3 are exact clockwise quarter-turns of frame 0 about the canvas centre (7.5, 7.5); frame 0 equals the PixelLab-generated seed in every visible pixel"},
    },
    "observed_status": {
        "tasks": {"family.delivery.task": "done", "family.working.task": "done", "family.retry.task": "done", "family.paused.task": "done", "live.seed.task": "done", "r.22e90a2a03fe453a.task": "done (historical Ready sample; plar_selection drift blocker retained)", "task": "open (superseded historical Ready sample task; plar_selection drift blocker retained)"},
        "family": {"output": "family.delivery.output", "candidate": "live.family.candidate", "accepted": True, "member_selection_current": True, "collective_criteria": "continuity, distinction, engine: pass (retained verdicts)"},
        "pending_jobs": [], "ready_tasks": [],
        "source_bindings": "all PLAR sources current; observed sha256 equal declared for BRIEF.md, src/queue.ts, src/queue-view.ts, assets/start.svg, assets/ready-confirmed.png, renderer/*, RENDER-STAGE.md and the style files",
    },
    "caller_verification": {
        "scope": "New checks performed by the caller in this session, independent of the specialist and of earlier retained reviews.",
        "package_identity": {"result": "pass" if identity_ok else "fail", "detail": "For each manifest member, destination bytes = package copy = cited artifact = manifest sha256; manifest candidates equal the current nominees; assets/start.svg equals the preserved hash.", "evidence": "work/cold-package-caller/hashes.json"},
        "preservation": {"result": "pass" if not pres["changed"] and not pres["removed"] else "fail", "detail": f"Project inventory before vs after delegation: {pres['baseline_count']} -> {pres['after_count']} files; added {pres['added']}; removed {pres['removed']}; changed {pres['changed']}. Caller and specialist outputs live only in the new directories work/cold-package/ and work/cold-package-caller/ plus this file.", "evidence": ["work/cold-package-caller/baseline-inventory.json", "work/cold-package-caller/after-inventory.json", "work/cold-package-caller/preservation-diff.json"]},
        "renderer_live_check_rerun": {"result": chk["status"], "exit_code": 0, "observations": len(chk["observations"]), "failures": chk["failures"], "available_views": chk["available_views"], "capture": ref("work/cold-package/render-01/render.json"), "screenshot": ref("work/cold-package/render-01/destination.png"), "specialist_checks_file": ref("work/cold-package/render-01-checks.json"), "caller_rerun_file": ref("work/cold-package-caller/check-rerun.json"), "browser": rs["browser"], "viewport": rs["viewport"], "dpr": rs["dpr"], "project_in_launch": "this copied consumer root"},
        "mechanical_measurements": {"result": "pass", "detail": "All four PNGs decode at the PLAR geometry (16x16 statics, 64x16 Working); zero partial-alpha pixels; transparent exteriors; Working frames 1-3 are exact clockwise quarter-turns of frame 0; frame 0 equals work/live-family/working-seed-download.png in visible pixels; three 4-connected clusters of 8, 9 and 15 pixels in every frame.", "evidence": "work/cold-package-caller/asset-measurements.json"},
        "consumer_transitions": {"result": "pass", "detail": "render.json records idle->Start, started->running Working, pause->paused Paused, ok->succeeded Ready, error->failed Retry for both statusCell and compactStatus, all available; errors [] and missing []."},
        "live_playback": {"result": "pass", "samples": len(rs["samples"]), "frame_sequence": frame_seq, "elapsed_ms": [s[0] for s in rs["samples"]], "wraps_3_to_0": rs["wraps_3_to_0"], "both_consumers_each_sample": all(set(s[2]) == {"statusCell", "compactStatus"} and len(set(s[1])) == 1 for s in rs["samples"]), "boundary_timeline": rs["timeline"]},
        "source_consumer_executor": {"result": "pass", "command": "node verify-integration.mjs assets/ready-confirmed.png", "exit_code": 0, "evidence": "work/cold-package-caller/verify-integration-ready.json"},
        "caller_visual_observations": {
            "viewed": ["work/cold-package/render-01/destination.png", "work/cold-package-caller/caller-matrix-8x.png (caller-built 8x nearest sheet of view-000..019)", "work/cold-package-caller/caller-playback-4x.png (caller-built 4x sheet of the 13 live samples, both consumers)"],
            "full_and_compact": "Both consumers show identical imagery at 1x and 3x for every state; labels Start, Working, Paused, Ready and Retry present; the live panel shows the succeeded state with the Ready check in both consumers; the coverage line reports every mapped asset available; no Missing asset or Wrong sheet size markers.",
            "silhouettes": "Start is a filled triangle; Working is three separated segments (flat top bar, right vertical bar with a notch, lower-left L block) around an empty centre; Paused is two upright bars; Ready is a check with a short descending left arm and a long ascending right arm; Retry is an open circular arrow with an arrowhead at upper right. They are structurally distinct without relying on colour, and Working never forms a check or arrow.",
            "motion": "Across the 13 live samples each 100 ms step, including every 3->0 wrap, is the same clockwise quarter-turn of the same three rigid shapes; no morphing, size change or centre drift. Rotation is stepwise in four phases.",
            "craft_notes": "Crisp square pixels at 3x with no smoothing or fringe. Ready is a single colour; Working and Retry carry mild shading within clusters; the Paused bars show visible blue-to-teal hue variation within each bar. These are caller observations, not new criteria or verdicts.",
        },
    },
    "specialist_delegation": {
        "agent": "pixl (native Claude Code subagent, foreground)", "agent_id": "a5bc1206e811b8dfa",
        "result": ref("work/cold-package/specialist-result.json"), "status_claimed": spec["status"],
        "caller_comparison": cmp_ref, "comparison_verdict": comparison["verdict"], "discrepancies": comparison["discrepancies"],
        "child_resumption": "Not needed; the child finished in one foreground conversation and no SendMessage continuation or artifact-based restart was performed.",
    },
    "provenance": {
        "ready": "Controlled retrieval fixture (PNG text: Controlled retrieval fixture, not PixelLab-generated art); candidate ready.retained from controlled pixellab-test request controlled-create-0002 (simulated provider); adopted as the scoped family baseline under RENDER-STAGE. Not live PixelLab art.",
        "start": "Pre-existing vector assets/start.svg, unchanged (ee2ba2fe...).",
        "working": "Seed: PixelLab official MCP create_image_pro_flash job d2f044ef-a48f-4526-ad0b-f3c373ea16f4 (16x16, 32 visible px). AI animate_image job 7fb6c786-322c-4ebd-847e-74f978ddfffa produced the rejected live.working-animation-01.candidate (grey tile in frame 2); workbench background repair job 234cbedb-f890-4abb-af76-0032f18b46b5 produced the rejected live.working-animation-repair-01.candidate (morph and near-hold). Final: pixelart_workbench job e831a30a-a590-4874-b8c7-1ab04ab071dd applied patch pixels equal to exact quarter-turns of the seed (work/live-family/working-animation-motion-01-construction.json); candidate live.working-animation-motion-01.candidate accepted. Working is therefore a generated seed plus deterministic specialist construction executed through official PixelLab tools.",
        "retry": "Direct PixelLab official MCP create_image_pro_flash job 1eda2891-aaec-4170-b0c4-dcc7ec8fd422; downloaded bytes used unchanged (work/live-family/retry-download.png).",
        "paused": "First attempt job bc7df4a0-026f-464e-932d-163edcada4d3 failed at the provider (background removal erased the whole image; not charged). Generation on a magenta key, job 6bf20949-23a3-46aa-9aa6-a205287e0468, produced the rejected opaque live.paused-02.candidate. Final: pixelart_workbench guarded cutout job 0ac629b8-6d1b-4d64-9997-caf01a911c4a set 196 background pixels to alpha 0 and left the 60 glyph pixels unchanged; candidate live.paused-cutout-01.candidate accepted.",
        "evidence": ["work/cold-package/jobs.json", "work/live-family/*-request.json, *-review.json, *-completion.json", "work/live-family/paused-failed-response.json", "work/live-family/working-animation-motion-01-construction.json"],
        "caller_scope": "Job IDs and states are as saved in the retained state; this session made no provider call and observed no remote status.",
    },
    "history_vs_current": {
        "creation_time_flags": [
            "family-snapshot.json and manifest.json limits accepted=false, remote_executed=false, retention_only=true describe the revision-80 local snapshot operation; acceptance was published at revisions 84-85 (work/live-family/family-completion.json) and the current family report shows the family accepted with current member selection.",
            "render.choice.destination still carries placement_acceptance 'unresolved recorded-coordinate mismatch; no overall render-check pass' from RENDER-STAGE; the later live engine criteria passed. The record was not edited.",
            "snapshot.state and collective-review.snapshot.state are absolute paths into the original production workspace (evidence/pixellab-family-production/20261108/project); in this copied consumer the project-relative paths resolve and the hashes match.",
            "work/live-family/integration.json is pre-final (it cites working.png bee419d2... from the rejected repair); work/live-family/package-integration.json is the final integration record (cf101610...).",
        ],
        "failed_attempts_retained": [
            "live.working-animation-01.candidate (job 7fb6c786...): visual fail, 193 opaque #808080 background pixels in frame 2",
            "live.working-animation-repair-01.candidate (job 234cbedb...): visual fail, morph and near-hold, wrap jump",
            "live.paused-02.candidate (job 6bf20949...): visual fail, opaque magenta exterior",
            "live.paused.job (remote bc7df4a0...): provider failed, not charged",
            "controlled-create-0001 (pixellab-test): failed first Ready request",
        ],
        "requirement_drift_preserved": [
            "Historical Ready tasks r.22e90a2a03fe453a.task (done) and 'task' (open) keep plar_selection blockers because current queue.ready requirements (d28e9cc9...) differ from their bound selections (806a1f2d..., 79b08da5...). Neither was rebound or re-evaluated; the family baseline uses the accepted ready.retained candidate and current production links.",
        ],
    },
    "limitations": [
        "New checks establish byte identity, consumer mapping, slicing, timing, nearest compositing, placement and the caller's own visual observations in the supplied headless Chrome fixture (HeadlessChrome/156) on this machine. They do not establish broad generative quality, unaided native host reliability, human acceptance or another destination engine.",
        "Earlier retained reviews (member and collective verdicts, grayscale comparison) are cited as history and were not re-performed; the caller did not regenerate a grayscale comparison.",
        "Transparent-pixel RGB under alpha 0 is inconsistent across files (#808080 and #000000 in working.png, magenta residues in paused.png); invisible under alpha compositing and not a saved criterion, but a consumer that ignores alpha would show it.",
        "Ready remains a controlled fixture and Start the existing vector; only Working, Retry and Paused have real PixelLab provider provenance.",
        "MCP tool outputs from the specialist's calls were not saved verbatim; CLI equivalents in work/cold-package/ and the caller's own plar read runs carry the same revision 85 and state hash content.",
    ],
    "new_files": {
        "caller": ["PACKAGE-RESULT.json", "work/cold-package-caller/inventory.py", "work/cold-package-caller/write_result.py", "work/cold-package-caller/baseline-inventory.json", "work/cold-package-caller/after-inventory.json", "work/cold-package-caller/preservation-diff.json", "work/cold-package-caller/hashes.json", "work/cold-package-caller/check-rerun.json", "work/cold-package-caller/asset-measurements.json", "work/cold-package-caller/render-summary.json", "work/cold-package-caller/plar-read-working-before.json", "work/cold-package-caller/plar-read-working-after.json", "work/cold-package-caller/verify-integration-ready.json", "work/cold-package-caller/caller-matrix-8x.png", "work/cold-package-caller/caller-playback-4x.png", "work/cold-package-caller/caller-comparison.json"],
        "specialist": spec["new_files_written"],
    },
    "continuation": {
        "exact_current": "delivered",
        "entry": "CURRENT-HANDOFF.md -> work/live-family/HANDOFF-current.json -> " + HANDOFF,
        "state_hash": STATE_HASH, "revision": prod["revision"], "requirements_hash": after["requirements_hash"], "plar_hash": after["hash"],
        "pending_provider_work": "none",
        "do_not": "regenerate accepted assets merely to repeat a test; alter retained evidence; rebind historical Ready selections",
        "next_development": "Per CURRENT-HANDOFF.md: simplification of family-plan and staged-request authoring; broad quality, native reliability, human acceptance and other destination engines remain separate qualifications. Reread focused PLAR after any change to sources, selections or destination bytes.",
    },
}
(ROOT / "PACKAGE-RESULT.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps({"comparison": cmp_ref, "result": ref("PACKAGE-RESULT.json"), "identity_ok": identity_ok}, indent=1))
