"""Write SPECIALIST-REPORT.json with computed artifact hashes from the retained result files.

Run with the selected Python using -I from the consumer root (passed as argv[1]).
"""
import hashlib
import json
import os
import sys

ROOT = sys.argv[1]
os.chdir(ROOT)
W = "work/everyday-guide/specialist"


def fh(p):
    b = open(p, "rb").read()
    return {"path": p, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def load(p):
    return json.load(open(p, encoding="utf-8"))


before = load(f"{W}/01-plar-read.json")
after = load(f"{W}/10-plar-read-after.json")
rc = load(f"{W}/05-family-review-context.json")
rep = load(f"{W}/08-family-replay-result.json")
val_after = load(f"{W}/09-validate-after.json")
val_final = load(f"{W}/13-validate-final.json")
hand = load(f"{W}/12-handoff-result.json")
src = load(f"{W}/07-source-range.json")
ctx_sum = load(f"{W}/04-authoring-context.summary.json")
rc_sum = load(f"{W}/05-family-review-context.summary.json")
fam_sum = load(f"{W}/06-family-report.summary.json")
rep_sum = load(f"{W}/08-family-replay-result.summary.json")
hand_sum = load(f"{W}/12-handoff-result.summary.json")

cont = after["production"]["continuation"]
state_hash = cont["state_hash"]
assert state_hash == before["production"]["continuation"]["state_hash"] == rc["state_hash"] == rep["state_hash"]
assert state_hash == val_after["hash"] == val_final["hash"] == hand["state_hash"]
assert before["production"]["revision"] == val_after["revision"] == val_final["revision"] == rep["revision"] == 126
assert after["requirements_hash"] == before["requirements_hash"] == hand["requirements_hash"]
for summary, result in ((ctx_sum, f"{W}/04-authoring-context.json"), (rc_sum, f"{W}/05-family-review-context.json"),
                        (fam_sum, f"{W}/06-family-report.json"), (rep_sum, f"{W}/08-family-replay-result.json"),
                        (hand_sum, f"{W}/12-handoff-result.json")):
    assert fh(result)["sha256"] == summary["result_sha256"], result
handoff_file = fh(hand["path"])
assert handoff_file["sha256"] == hand["sha256"]

artifacts = []
for name in sorted(os.listdir(W)):
    if name == "SPECIALIST-REPORT.json":
        continue
    artifacts.append(fh(f"{W}/{name}"))
artifacts.append(handoff_file)

report = {
    "status": "delivered",
    "status_scope": "Delegated specialist half of EVERYDAY-ASSIGNMENT.md for queue authoring-plar.txt / asset queue.working: public reads, focused authoring and review-context exports, precise source retrieval, safe replay of the existing family review without publication, and one retained production handoff. Consumption/recovery of already accepted work; no fresh art acceptance, generation, provider action or state record authoring.",
    "specialist_identity": {
        "kind": "Native Claude Code subagent spawned via the Agent tool with subagent_type 'pixl' (declared in the harness --agents file), running the PIXL profile from the installed kit .agents/skills/export-kit. Host model claude-fable-5-1; not a separately trained model.",
        "kit": ".agents/skills/export-kit",
        "runner": ".agents/skills/export-kit/scripts/pixl.py via C:/github/pixel-lab-agent/.venv/Scripts/python.exe (public CLI only; MCP pixl-local not used)",
        "profile_and_skill_files_loaded": [
            ".agents/skills/export-kit/skills/pixl/SKILL.md",
            ".agents/skills/export-kit/resources/agent/PROFILE.md",
            ".agents/skills/export-kit/skills/pixl/references/everyday.md",
            ".agents/skills/export-kit/skills/pixl/references/identities-and-paths.md",
            ".agents/skills/export-kit/skills/pixl/references/delegation.md",
            ".agents/skills/export-kit/resources/spec/candidate-review.md",
        ],
        "runtime_file_consulted_read_only": ".agents/skills/export-kit/runtime/pixl/handoff.py (reserved details keys)",
    },
    "consumer_root": ROOT,
    "queue_path": "authoring-plar.txt",
    "asset_id": "queue.working",
    "requirements_hash": after["requirements_hash"],
    "state_hash": state_hash,
    "store": cont["store"],
    "revision": {"before": before["production"]["revision"], "after_replay": val_after["revision"], "after_handoff": val_final["revision"]},
    "identity_domains_used": {
        "file_sha256": "PLAR top-level hash 88c27b3a... (queue saves only, unused), every export result_sha256, source file sha256 4ace984b... for the source range, destination/member/manifest/handoff file sha256 values",
        "canonical_state_sha256": f"{state_hash} from plar read production.continuation.state_hash, context/family/workflow/jobs hash, review-context state_hash and validate hash; used as --expect for candidate-review and plar handoff",
        "selected_requirements_sha256": f"{after['requirements_hash']} from plar read requirements_hash; used as --requirements for plar handoff",
        "candidate_bindings_sha256": f"{rc['binding_hash']} from review-context binding_hash; carried unchanged inside work/export-review/identical-review.json",
        "review_report_sha256": f"{rep['review_sha256']} returned by the replay as review_sha256; identifies the retained review report file, not state",
        "not_used": "record_sha256 values; no hash was computed from any JSON export to form a state hash",
    },
    "replay": {
        "review": rep["review"],
        "candidate": rep["candidate"],
        "observation_file": fh("work/export-review/identical-review.json"),
        "reused_review": rep["reused_review"],
        "publications": rep["publications"],
        "remote_executed": rep["remote_executed"],
        "review_sha256": rep["review_sha256"],
        "review_path": rep["review_path"],
        "expected_review_sha256_from_caller": "59faea6482a769cc452444f1d94a5b85ff356ec7d0c558778738127861b81294",
        "review_sha256_matches_expected": rep["review_sha256"] == "59faea6482a769cc452444f1d94a5b85ff356ec7d0c558778738127861b81294",
        "state_hash_before": before["production"]["continuation"]["state_hash"],
        "state_hash_after": val_after["hash"],
        "revision_before": before["production"]["revision"],
        "revision_after": val_after["revision"],
    },
    "family_acceptance": {
        "candidate": rc["candidate"],
        "manifest": rc["candidate_file"],
        "creation_time_snapshot_acceptance": rc["snapshot_acceptance"],
        "current_acceptance": rc["current_acceptance"],
        "task_status": rc["task_status"],
        "nominated": rc["nominated"],
        "note": "Creation-time accepted:false is immutable and describes snapshot creation at source state 5c9c5409...; current acceptance (three passing verdicts, task done) is separate and is what the continuation reports as accepted:true.",
    },
    "delivery_confirmed_by_reads": {
        "continuation_action": cont["action"],
        "task": cont["task"],
        "task_state": after["production"]["task_state"],
        "destination": cont["delivery"]["destination"],
        "destination_sha256_expected": cont["delivery"]["expected_sha256"],
        "destination_sha256_on_disk": fh("renderer-successor/assets/working.png")["sha256"],
        "destination_matches": cont["delivery"]["destination_matches"],
        "delivery_complete": cont["delivery"]["complete"],
        "pending_jobs": after["production"]["pending_jobs"],
    },
    "source_range": {
        "path": "src/queue-view-successor.ts", "sha256": src["sha256"], "start": src["start"], "end": src["end"], "bytes": src["bytes"],
        "supports": "Current animation requirement (reduced: frame 0 stationary; normal: floor(elapsed/frameMs) mod frames) and criteria provenance-correction.delivery.q.destination / provenance-correction.working.q.geometry; locator derived from the authoring context source provenance.source.view (retrieve lines 1-22) narrowed to the reduced-motion clause.",
    },
    "handoff": {"path": hand["path"], "sha256": hand["sha256"], "bytes": handoff_file["bytes"], "next": hand["next"],
                "details_file": fh(f"{W}/11-handoff-details.json"), "result_file": fh(f"{W}/12-handoff-result.json")},
    "artifacts": artifacts,
    "errors_and_corrections": [
        "One shell heredoc attempt to author 11-handoff-details.json failed on bash quoting before writing anything; the details were then generated by the retained script make_handoff_details.py. No operation error, no handoff_stale, path_escape or result_exists occurred.",
        "08-family-replay-result.stderr.txt and 12-handoff-result.stderr.txt are empty captures retained for completeness.",
    ],
    "not_performed": [
        "No re-viewing of the art, playback or renderer execution; no PNG decoding.",
        "No PixelLab call, generation, dispatch, observation or import.",
        "No new verdict, snapshot, nomination, completion, PLAR queue save, state record authoring or edits to existing files.",
    ],
    "next": "Caller: open the listed files, verify result_sha256 values and the handoff bytes, compare the handoff resume block with a fresh focused plar read, and confirm the replay added no publication (revision 126, same hash). Then decide whether to refresh the queue.working row text in authoring-plar.txt (status/next) via a queue save guarded by the PLAR file hash; the overall product and broader host reliability remain open.",
}

p = f"{W}/SPECIALIST-REPORT.json"
assert not os.path.exists(p)
with open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"wrote": fh(p), "artifact_count": len(artifacts)}, indent=2))
