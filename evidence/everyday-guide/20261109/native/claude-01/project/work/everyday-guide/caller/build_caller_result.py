"""Build work/everyday-guide/CALLER-RESULT.json from actual files; hashes are computed, not transcribed."""
import datetime
import hashlib
import json
import os
import sys

ROOT = os.path.abspath(sys.argv[1])


def p(rel):
    return os.path.join(ROOT, rel.replace("/", os.sep))


def sha(rel):
    h = hashlib.sha256()
    with open(p(rel), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return {"path": rel, "sha256": h.hexdigest(), "bytes": os.path.getsize(p(rel))}


def load(rel):
    with open(p(rel), "rb") as f:
        return json.loads(f.read().decode("utf-8"))


ver = load("work/everyday-guide/caller/verification.json")
spec = load("work/everyday-guide/specialist/SPECIALIST-REPORT.json")
plar = load("work/everyday-guide/caller/plar-read-mcp-after.json")
cont = plar["production"]["continuation"]
ctx = load("work/everyday-guide/caller/review-context-family-final.json")
replay_c = load("work/everyday-guide/caller/replay-result.json")
replay_s = load("work/everyday-guide/specialist/08-family-replay-result.json")
val_final = load("work/everyday-guide/caller/validate-final.json")
tree = load("work/everyday-guide/caller/tree-diff.json")
tree_final = load("work/everyday-guide/caller/tree-diff-final.json")
handoff_rel = spec["handoff"]["path"]
handoff = load(handoff_rel)

result = {
    "trial": "everyday-production-guide/20261109/native/claude-01",
    "assignment": sha("EVERYDAY-ASSIGNMENT.md"),
    "written_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "kit": {"current": ".agents/skills/export-kit", "bundle_manifest_version": load(".agents/skills/export-kit/bundle-manifest.json").get("version"), "historical_preserved": [".agents/skills/pixl-kit", ".agents/skills/review-kit"], "guidance_followed": ["skills/pixl/references/everyday.md", "skills/pixl/references/identities-and-paths.md", "skills/pixl/references/delegation.md", "resources/spec/candidate-review.md"]},
    "roles": {
        "caller": "Claude Code main session (claude-fable-5-1, Claude Code 2.1.318) acting as the cold caller; owns every check in caller_checks and authored this file through build_caller_result.py.",
        "specialist": {
            "actual_identity": "Native Claude Code subagent spawned by the caller with the Agent tool, subagent_type 'pixl' as declared in the harness --agents file (agents.json: 'PIXL visual asset specialist for retained production'). It is a generic host child carrying the PIXL role by loading the current kit's shared profile and skill; no separately trained model or named-role selection beyond that declaration is claimed. The inherited role file .codex/agents/pixl.toml was not used by this host.",
            "agent_id": "a374e0c1528878c24",
            "route": "Agent tool, foreground (run_in_background false); one instance, no SendMessage continuation needed",
            "profile_and_skill_files_it_reported_loading": spec["specialist_identity"]["profile_and_skill_files_loaded"],
            "interface_used": spec["specialist_identity"]["runner"],
            "self_report": sha("work/everyday-guide/specialist/SPECIALIST-REPORT.json"),
        },
        "reviewer_actor_in_state": "actor (unchanged; no new review recorded this session)",
    },
    "roots": {
        "consumer_root": ROOT,
        "mcp_root_configured": "same consumer root (../mcp.json passes --root to this project directory); pixl_plar_read project_root and CLI project_root both resolve to it",
        "production_store": cont["store"],
        "state": ".pixl/assets/queue.ready/state.px",
        "not_used": "maintainer checkout C:/github/pixel-lab-agent (only its .venv Python interpreter was used, as assigned)",
    },
    "selected_generation": {
        "queue": "authoring-plar.txt",
        "asset": "queue.working",
        "plar_file_hash_file_sha256": plar["hash"],
        "requirements_hash_selected_requirements_sha256": plar["requirements_hash"],
        "asset_row_status": plar["asset"]["status"],
        "asset_row_next": plar["asset"]["next"],
        "production": {k: plar["production"].get(k) for k in ("store", "link_status", "status", "task", "task_state", "revision", "hash")},
        "continuation": {"action": cont["action"], "state_hash_canonical_state_sha256": cont["state_hash"], "jobs": cont["jobs"], "before_another_request": cont["before_another_request"], "delivery": cont["delivery"]},
        "older_generation_untouched": {"path": "plar.txt", "unchanged": "plar.txt" not in tree_final["changed"]},
        "current_useful_return": "The assigned asset is delivered per the saved continuation: nominated bytes present at renderer-successor/assets/working.png, task done, and the one containing four-member family currently accepted with member selection current. The continuation is consumption of accepted work; the queue row text (status in_progress, stale next) lags the production state and is a caller queue-save decision, not a production gap.",
    },
    "state": {
        "start": {"revision": 126, "state_hash": "23718b6d027836af49f3548fcb38979bd4afca032e8113d7a9222c7c570c8c49", "source": "caller MCP pixl_validate before delegation"},
        "final": {"revision": val_final["revision"], "state_hash": val_final["hash"], "valid": val_final["valid"], "records": val_final["records"], "files_verified": val_final["files_verified"], "source": "caller CLI validate after specialist work and caller replay; MCP review_context final read agrees"},
        "mcp_final_read": {k: ctx.get(k) for k in ("state_hash", "revision", "task_status", "nominated", "binding_hash")},
        "publications_this_session": [],
        "provider_actions_this_session": [],
        "state_px_unchanged": ".pixl/assets/queue.ready/state.px" not in tree_final["changed"],
    },
    "specialist_artifacts": {
        "directory": "work/everyday-guide/specialist",
        "exports_verified_against_returned_summaries": {
            "authoring_context_provenance_correction_plan": sha("work/everyday-guide/specialist/04-authoring-context.json"),
            "family_review_context": sha("work/everyday-guide/specialist/05-family-review-context.json"),
            "family_report": sha("work/everyday-guide/specialist/06-family-report.json"),
            "family_replay_result": sha("work/everyday-guide/specialist/08-family-replay-result.json"),
            "handoff_result": sha("work/everyday-guide/specialist/12-handoff-result.json"),
        },
        "reads": {"plar_before": sha("work/everyday-guide/specialist/01-plar-read.json"), "plar_after": sha("work/everyday-guide/specialist/10-plar-read-after.json"), "workflow": sha("work/everyday-guide/specialist/02-workflow.json"), "jobs": sha("work/everyday-guide/specialist/03-jobs.json"), "validate_after_replay": sha("work/everyday-guide/specialist/09-validate-after.json"), "validate_final": sha("work/everyday-guide/specialist/13-validate-final.json")},
        "source_range": {"file": sha("work/everyday-guide/specialist/07-source-range.json"), "source": "src/queue-view-successor.ts", "source_sha256": spec["source_range"]["sha256"], "lines": [spec["source_range"]["start"], spec["source_range"]["end"]], "supports": spec["source_range"]["supports"]},
        "handoff_details": sha("work/everyday-guide/specialist/11-handoff-details.json"),
        "helper_scripts": [sha("work/everyday-guide/specialist/make_handoff_details.py"), sha("work/everyday-guide/specialist/make_specialist_report.py")],
        "all_listed_artifact_hashes_match_disk": next(c["ok"] for c in ver["checks"] if c["check"] == "specialist_report_artifact_hashes_match_disk"),
    },
    "handoff": {
        "retained": sha(handoff_rel),
        "next": handoff["next"],
        "asset_id": handoff["asset_id"],
        "requirements_hash": handoff["requirements_hash"],
        "selection": handoff["selection"],
        "resume_state_hash": handoff["resume"]["state_hash"],
        "resume_action": handoff["resume"]["action"],
        "details_status": handoff["details"]["status"],
        "details_caller_actions": len(handoff["details"]["caller_actions"]),
        "details_future_work": handoff["details"]["future_work"],
        "destination_and_package_locators": {"destination": handoff["details"]["delivered_artifacts"]["destination"], "family_package_directory": handoff["details"]["delivered_artifacts"]["family_package"]["directory"], "manifest": handoff["details"]["delivered_artifacts"]["family_package"]["manifest"], "members": handoff["details"]["delivered_artifacts"]["family_package"]["members"], "family_review_report": handoff["details"]["delivered_artifacts"]["family_review_report"]},
        "caller_assessment": "Status 'delivered' is warranted for the assigned scope: it agrees with the continuation action, the destination byte match and the current family acceptance; the details separate creation-time and current acceptance, state what was not performed (no re-viewing, no renderer run, no provider action) and name the remaining scope.",
    },
    "replay": {
        "review": "native-review.family.collective",
        "candidate": "native-review.family.candidate",
        "observation_file": sha("work/export-review/identical-review.json"),
        "observation_unchanged": sha("work/export-review/identical-review.json")["sha256"] == "fcb821d6ae755b7f471672a418050f233910e395d2bffd75463c733e263d878f",
        "observation_parses_equal_to_original_request": next(c["ok"] for c in ver["checks"] if c["check"] == "identical_review_equals_original_request_and_embedded_report_request"),
        "specialist": {"result": sha("work/everyday-guide/specialist/08-family-replay-result.json"), "reused_review": replay_s["reused_review"], "publications": replay_s["publications"], "remote_executed": replay_s["remote_executed"], "review_sha256": replay_s["review_sha256"], "state_hash": replay_s["state_hash"], "revision": replay_s["revision"]},
        "caller_via_kit_cli": {"result": sha("work/everyday-guide/caller/replay-result.json"), "summary": sha("work/everyday-guide/caller/replay-result.summary.json"), "reused_review": replay_c["reused_review"], "publications": replay_c["publications"], "remote_executed": replay_c["remote_executed"], "review_sha256": replay_c["review_sha256"], "state_hash": replay_c["state_hash"], "revision": replay_c["revision"], "byte_identical_to_specialist_result": sha("work/everyday-guide/caller/replay-result.json")["sha256"] == sha("work/everyday-guide/specialist/08-family-replay-result.json")["sha256"]},
        "original_review_preserved": {"report": sha(".pixl/assets/queue.ready/reviews/59faea6482a769cc452444f1d94a5b85ff356ec7d0c558778738127861b81294/review.json"), "verdicts": [(c["id"], c["status"], c["verdict"]) for c in replay_c["criteria"]], "observed_at_original": "2026-11-09T16:24:59+00:00 (from REVIEW-RESULT.json); this session added no new observation"},
        "conclusion": "Both replays reused the existing review with zero publications, no provider action, unchanged revision 126 and state hash; the retained report still hashes to its name. The replay is not a newly observed review.",
    },
    "acceptance_distinction": {
        "creation_time_snapshot_acceptance": ctx["snapshot_acceptance"],
        "current_acceptance": ctx["current_acceptance"],
        "task_status": ctx["task_status"],
        "nominated": ctx.get("nominated"),
        "note": "Manifest acceptance.accepted:false is the immutable creation receipt at source state 5c9c5409...; current acceptance comes from the three retained collective verdicts and the done task. Unchanged from the prior trial.",
    },
    "identity_domains_used": {
        "file_sha256": "every artifact/export result_sha256 verified against bytes on disk; PLAR top-level hash 88c27b3a... recorded only in the handoff's selection block (queue-save guard); source file sha256 4ace984b... for the exact range; manifest/member/destination/review-report file hashes",
        "canonical_state_sha256": "23718b6d... taken from validate.hash, workflow/context/family hash, review-context state_hash and plar production.continuation.state_hash; used as --expect for both replays and the handoff; never computed from a JSON export",
        "selected_requirements_sha256": "1ab9df77... from the fresh focused PLAR read; used as --requirements for the handoff and recorded in it",
        "candidate_bindings_sha256": "48752d9d... from review-context; equal to the binding_hash inside the unchanged observation file",
        "review_report_sha256": "59faea64... returned as review_sha256 by both replays; identifies the retained report file, not state or acceptance",
        "record_sha256": "not used for any decision",
    },
    "caller_checks": {"file": sha("work/everyday-guide/caller/verification.json"), "script": sha("work/everyday-guide/caller/verify.py"), "total": ver["checks_total"], "passed": ver["checks_ok"], "failed": ver["failed"], "names": [c["check"] for c in ver["checks"]]},
    "preservation": {
        "method": "sha256 of every file under the consumer (excluding work/everyday-guide and .git) before delegation and again at the end",
        "baseline": sha("work/everyday-guide/caller/baseline-hashes.json"),
        "after_specialist": sha("work/everyday-guide/caller/after-hashes.json"),
        "final": sha("work/everyday-guide/caller/final-hashes.json"),
        "diff_after_specialist": tree,
        "diff_final": tree_final,
        "conclusion": "The only addition outside work/everyday-guide is the retained handoff file; no source, asset, queue, state, kit, prior work or evidence file changed or was removed.",
    },
    "failures_and_corrections": [
        "Caller: the first version of verify.py assumed manifest key 'members', handoff-result 'result_saved' and LF line endings; four checks failed on those assumptions, not on the artifacts. The script was corrected to the actual public result shapes (manifest 'files' and 'acceptance.accepted', summary file for result_saved, exact CRLF comparison) and all 26 checks then passed. Nothing in the specialist's work or the state needed correction.",
        "Caller: a bash heredoc copy of hash_tree.py failed on backslash quoting before any file was written; the script was written with the editor tool instead.",
        "Specialist (self-reported): one bash heredoc attempt to author the handoff details failed on quoting before writing anything; it generated the file with a retained script. No operation error, handoff_stale, path_escape or result_exists occurred.",
        "Specialist report records path for 07-source-range.json but the export itself carries no path field; the caller verified the text against src/queue-view-successor.ts lines 18-21 byte-for-byte including CRLF.",
    ],
    "continuation": {
        "exact": "Reread authoring-plar.txt asset queue.working (pixl plar read / pixl_plar_read) and open the retained handoff " + handoff_rel + "; while its requirements_hash 1ab9df77... and resume.state_hash 23718b6d... still match the fresh focused read, the production side is delivered and nothing is pending.",
        "remaining_caller_decision": "Whether to refresh the queue.working row text in authoring-plar.txt (status in_progress, stale next, purpose sentence asking to confirm the reduced-motion mapping) via a PLAR save guarded by the current file hash 88c27b3a...; this changes queue progress, not the selected requirements.",
        "open_beyond_this_assignment": ["The overall product and broader host reliability remain open.", "Retained open tasks from earlier generations (authoring-01.working.task, successor-adoption*.working.task) and three terminal failed jobs are history, not blockers; their closure is a separate decision.", "Original review limits stand: headless Chrome fixture, recorded exposures, byte-unchanged checks against earlier evidence rather than version control."],
    },
    "scope_and_limits": [
        "This trial evaluates cold-caller consumption/recovery of an accepted successor through the everyday workflow with a native PIXL child; it does not establish generated-art quality, destination behaviour beyond the earlier fixture, or host reliability in general.",
        "No art was re-viewed, no renderer executed, no PixelLab call made, no new verdict, snapshot, nomination or completion recorded; no state.px hand-edit, generic commit, global setting or memory change.",
    ],
}

out = p("work/everyday-guide/CALLER-RESULT.json")
if os.path.exists(out):
    raise SystemExit("result exists; choose a fresh name")
with open(out, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print("wrote", out)
