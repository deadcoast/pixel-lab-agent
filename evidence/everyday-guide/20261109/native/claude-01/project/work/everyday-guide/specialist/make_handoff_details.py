"""Author 11-handoff-details.json from public read results with recomputed file hashes.

Run with the selected Python using -I from the consumer root. Reads only the
specialist result files and the delivered files; writes one fresh JSON file.
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


after = load(f"{W}/10-plar-read-after.json")
cont = after["production"]["continuation"]
rc = load(f"{W}/05-family-review-context.json")
rep = load(f"{W}/08-family-replay-result.json")
val = load(f"{W}/09-validate-after.json")
D = ".pixl/assets/queue.ready/deliveries/ec59b8245619463446cb86b639e7b387e748917fb5c520a085984b85c89df5d0"

assert cont["action"] == "delivered" and cont["delivery"]["destination_matches"] and cont["delivery"]["complete"]
fam = cont["delivery"]["families"][0]
assert fam["accepted"] is True and fam["state"] == "done" and fam["member_selection_current"] is True
assert rep["reused_review"] is True and rep["publications"] == [] and rep["remote_executed"] is False
assert rep["state_hash"] == cont["state_hash"] == val["hash"] == rc["state_hash"] and val["revision"] == 126
dest = fh("renderer-successor/assets/working.png")
assert dest["sha256"] == cont["delivery"]["expected_sha256"]
members = []
for m in rc["members"]:
    r = fh(m["retained_path"])
    assert r["sha256"] == m["sha256"]
    members.append({"candidate": m["candidate"], "output": m["output"], "retained_path": m["retained_path"],
                    "sha256": r["sha256"], "bytes": r["bytes"]})
dest_copies = [fh(p) for p in ["renderer-successor/assets/ready-confirmed.png", "renderer-successor/assets/error-retry.png",
                               "renderer-successor/assets/paused.png", "renderer-successor/assets/start.svg"]]
manifest = fh(D + "/manifest.json")
assert manifest["sha256"] == fam["manifest_sha256"]
review = fh(rep["review_path"])
assert review["sha256"] == rep["review_sha256"]
obs = fh("work/export-review/identical-review.json")

details = {
    "status": "delivered",
    "status_scope": "Assigned scope only: queue authoring-plar.txt, asset queue.working. The reviewed-reuse Working strip (provenance-correction.working.candidate) is nominated, its task provenance-correction.working.task is done, the nominated bytes are present at the declared destination, and the one containing family (native-review.family.candidate on provenance-correction.delivery.output) is currently accepted with its task done and member selection current. This is consumption/recovery of already accepted work; it is not a fresh art acceptance and no new verdict, snapshot, nomination, completion, provider call or generation occurred in this session.",
    "specialist": {
        "identity": "Native Claude Code subagent spawned by the caller through the Agent tool (subagent_type 'pixl' from the harness --agents file), running the PIXL profile from the installed kit .agents/skills/export-kit; the model is the host model (claude-fable-5-1), not a separately trained specialist.",
        "profile_and_skill_files_loaded": [
            ".agents/skills/export-kit/skills/pixl/SKILL.md",
            ".agents/skills/export-kit/resources/agent/PROFILE.md",
            ".agents/skills/export-kit/skills/pixl/references/everyday.md",
            ".agents/skills/export-kit/skills/pixl/references/identities-and-paths.md",
            ".agents/skills/export-kit/skills/pixl/references/delegation.md",
            ".agents/skills/export-kit/resources/spec/candidate-review.md",
        ],
    },
    "identities_used": {
        "selected_requirements_sha256": after["requirements_hash"],
        "canonical_state_sha256": cont["state_hash"],
        "state_revision": after["production"]["revision"],
        "plar_file_sha256_for_queue_saves_only": after["hash"],
        "candidate_bindings_sha256": rc["binding_hash"],
        "family_review_report_sha256": rep["review_sha256"],
        "store": cont["store"],
        "task": cont["task"],
        "note": "All taken from public read results (plar read, review-context, candidate-review, validate); no state hash was computed from a JSON export.",
    },
    "delivered_artifacts": {
        "destination": {
            "path": dest["path"], "sha256": dest["sha256"], "bytes": dest["bytes"],
            "candidate": cont["delivery"]["candidate"],
            "geometry": "64x16 PNG, four horizontal 16x16 cells per the passed mechanical verdict provenance.working.review.verdict.0; not re-decoded this session",
        },
        "destination_copies_of_other_members": dest_copies,
        "family_package": {"directory": D, "manifest": manifest, "members": members,
                           "candidate": fam["candidate"], "output": fam["output"], "task": fam["task"]},
        "family_review_report": review,
    },
    "family_acceptance": {
        "creation_time_snapshot_acceptance": rc["snapshot_acceptance"],
        "current_acceptance": rc["current_acceptance"],
        "continuation_family_accepted": fam["accepted"],
        "note": "snapshot_acceptance.accepted:false is the immutable creation-time record (source state 5c9c5409...); current acceptance is the three passing collective verdicts and the done delivery task. These are distinct facts.",
    },
    "checks_performed": [
        {"check": "Selected PLAR read before and after; file hash, requirements_hash and continuation state_hash unchanged across the session",
         "evidence": [f"{W}/01-plar-read.json", f"{W}/10-plar-read-after.json"]},
        {"check": "workflow and jobs reports: ready [], 11 jobs all terminal (8 succeeded, 3 failed), no pending or unknown job, remote_executed false",
         "evidence": [f"{W}/02-workflow.json", f"{W}/03-jobs.json"]},
        {"check": "Focused authoring context for provenance-correction.plan exported at the same state hash and revision",
         "evidence": [f"{W}/04-authoring-context.json"]},
        {"check": "Exact family review context and family report: binding_hash matches the unchanged observation file; three criteria pass with existing verdict IDs; task done; nominated",
         "evidence": [f"{W}/05-family-review-context.json", f"{W}/06-family-report.json"]},
        {"check": "Precise source retrieval src/queue-view-successor.ts lines 18-21 against the source file sha256 4ace984b...: the text defines motionQuery and statusFrame returning frame 0 for running under reduced motion, else floor(elapsed/frameMs) mod frames. It supports the current animation requirement (reduced: frame 0, stationary, source_frames 4), the renderer_frame_extraction observation, and the criteria provenance-correction.delivery.q.destination and provenance-correction.working.q.geometry",
         "evidence": [f"{W}/07-source-range.json"]},
        {"check": "Safe replay of review native-review.family.collective with the unchanged observation file: reused_review true, publications [], remote_executed false, review_sha256 59faea64..., state hash and revision 126 unchanged by the following validate",
         "evidence": [f"{W}/08-family-replay-result.json", f"{W}/09-validate-after.json", obs["path"]]},
        {"check": "Byte verification (sha256 recomputed in this session) of the destination PNG against the continuation expected_sha256, each retained member file against the review-context member sha256, the manifest against manifest_sha256 and the review report against review_sha256",
         "evidence": ["the sha256 values embedded in delivered_artifacts of this details object"]},
    ],
    "not_performed": [
        "No fresh native or enlarged viewing of the art, no playback viewing, no renderer execution and no PNG decoding; artistic and destination acceptance rest on the retained verdicts of the prior session.",
        "No PixelLab call, no generation, no job dispatch, observation or import.",
        "No new verdict, snapshot, nomination, completion, PLAR queue save or state record authoring.",
    ],
    "caller_actions": [
        {"action": "Supplied the assignment EVERYDAY-ASSIGNMENT.md and a delegation brief naming queue authoring-plar.txt, asset queue.working and the replay target",
         "evidence": [fh("EVERYDAY-ASSIGNMENT.md")]},
        {"action": "Supplied the unchanged observation file for the replay (reformatted copy of the original request carrying the same binding_hash 48752d9d...)",
         "evidence": [obs]},
        {"action": "Retained its own pre-delegation baseline reads under work/everyday-guide/caller/",
         "evidence": [fh("work/everyday-guide/caller/plar-read-before.json"), fh("work/everyday-guide/caller/baseline-hashes.json")]},
        {"action": "Earlier caller decisions remain as retained sources: exact Ready baseline adoption and the reviewed successor destination",
         "evidence": [fh("work/family-render-review/caller-comparison-final.json"), fh("SUCCESSOR-ADOPTION.md"), fh("RENDER-STAGE.md")]},
    ],
    "future_work": [
        "The overall product and broader host reliability remain open; this handoff covers only the Working asset and its four-member family at the declared destination.",
        "Queue row text: authoring-plar.txt still records queue.working status in_progress with next 'Isolated review-interface evaluation at retained pre-acceptance state' and a purpose sentence asking to confirm the reduced-motion consumer mapping, while the production continuation is delivered. Refreshing that row is a caller queue save (plar save guarded by the current PLAR file hash 88c27b3a...); it was deliberately not done here. A status/next edit would not change the selected requirements.",
        "Reduced-motion consumer mapping: per current reads it is confirmed for this consumer by the retained live verdict native-review.family.collective.verdict.2 (stationary frame zero in both statusCell and compactStatus, live switching both ways) and by src/queue-view-successor.ts lines 18-21; asset.questions is empty. No further generation is indicated. If a different consumer or browser is adopted, re-exercise the destination criterion there.",
        "Retained open tasks in the store outside this continuation (authoring-01.working.task, successor-adoption.working.task, successor-adoption-02.working.task) carry production_plan blockers from earlier generations; they are history, not blockers for queue.working delivery, and their reconciliation or closure is a separate caller decision.",
        "Three failed provider jobs (including authoring-01.working.join-01) are terminal and retained; no retry is required for the delivered scope.",
    ],
    "limits": [
        "The specialist did not re-view the art or run the renderer; findings are consumption of accepted work plus byte and identity verification.",
        "Original review limitations stand: headless Chrome fixture on one machine, recorded exposures rather than a real-time display, and byte-unchanged checks against earlier evidence rather than version control.",
    ],
}

p = f"{W}/11-handoff-details.json"
assert not os.path.exists(p)
with open(p, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(details, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"wrote": fh(p), "requirements_hash": after["requirements_hash"], "expect": cont["state_hash"]}, indent=2))
