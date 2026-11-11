"""Write SPECIALIST-RESULT.json with exact path/sha256 references and verify protected files against the parent baseline."""
import hashlib
import json
import os

W = "work/integration-change/"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def ref(p, note=None):
    d = {"path": p, "sha256": sha(p)}
    if note:
        d["note"] = note
    return d


base = {}
for line in open(W + "parent/baseline-hashes.txt", encoding="utf-8"):
    line = line.strip()
    if not line or line.startswith("---"):
        continue
    h, p = line.split(" *", 1)
    base[p] = h
changed, missing = [], []
for p, h in base.items():
    if not os.path.exists(p):
        missing.append(p)
    elif sha(p) != h:
        changed.append(p)
expected_changed = ["integration-plar.txt", ".pixl/assets/queue.working/state.px"]
integrity = {
    "baseline_file": ref(W + "parent/baseline-hashes.txt"),
    "changed_vs_baseline": changed,
    "missing_vs_baseline": missing,
    "expected_changed_only": sorted(changed) == sorted(expected_changed),
    "note": "Only integration-plar.txt (public plar save/prepare/handoff) and state.px (public state operations) may differ from the parent baseline; all original art, sources, inputs, plar.txt, brief, amendment, history snapshots, old job journal and old plan bytes must be unchanged.",
}
handoff = json.load(open(W + "handoff.json", encoding="utf-8"))
result = {
    "version": 1,
    "specialist": "pixl:pixl (PIXL production profile; Claude agent)",
    "root": "C:/Users/ryanf/AppData/Local/Temp/pixl readiness claude clean j9gn621r/consumer",
    "status": "delivered",
    "steps_completed": [1, 2, 3, 4, 5, 6, 7],
    "initial_read": ref(W + "initial-read.json", "plar read --path integration-plar.txt (exit 0); file hash 8ddece43...; changes: timing-authority and working-timing changed; only queue.working affected"),
    "allocation_save": ref(W + "allocation-save.json", "plar save --expect 8ddece43... -> new file hash 28657e19...; refreshed only the two Working source hashes, its animation requirement (150 ms / 600 ms cycle) and its next action"),
    "final_document": ref(W + "final-document.json", "byte copy of integration-plar.txt immediately after the save (28657e19...); later public plar prepare/handoff advanced the row link; current file hash 481450298f..."),
    "current_selection": ref(W + "current-selection.json", "focused read after save: requirements_hash dc429242..., state 24a52f9d..., next_action resolve_prepared_intent, selection changed"),
    "obsolete_dispatch": ref(W + "obsolete-dispatch.json", "job-dispatch first_request --expect 24a52f9d...: exit 2, stdout empty, stderr JSON copied byte-for-byte: error job_blocked, detail plar_selection: queue.working is changed (selected=True); compare current requirements with the retained plan. No dispatch_request returned, no provider call, state hash unchanged (state-validate-after-refusals.json)"),
    "obsolete_completion": ref(W + "obsolete-completion.json", "task-complete task reference.0 --expect 24a52f9d...: exit 2, stdout empty, stderr JSON copied byte-for-byte: error plar_selection, detail task: current consumer requirements differ or are unavailable; retain the old review and compare a revised contract. Refusal cause is the stale PLAR selection guard, not a missing candidate; state hash unchanged"),
    "old_abandon": ref(W + "old-abandon.json", "job-observe first_request failed with LOCAL evidence (old-abandon-evidence.json: never dispatched, no provider contact, superseded by 150 ms amendment); revision 2, hash 979705c3..."),
    "old_abandon_evidence": ref(W + "old-abandon-evidence.json"),
    "revised_prepare": ref(W + "revised-prepare.json", "plar prepare --revise --expect 979705c3... with packet-150.json/connection-150.json: new generation r.5b1bc38638b68ed8.* (task/output/job), revision 4, hash a720d20c..., PLAR link advanced (481450...)"),
    "new_abandon": ref(W + "new-abandon.json", "job-observe r.5b1bc38638b68ed8.request failed with LOCAL evidence (new-abandon-evidence.json: exact art reuse, never dispatched, no provider contact); revision 5, hash 94b73a90..."),
    "new_abandon_evidence": ref(W + "new-abandon-evidence.json"),
    "candidate_commit": ref(W + "candidate-commit.json", "public commit (JSON document, --expect 94b73a90...) appending X r.5b1bc38638b68ed8.candidate.working.retained for assets/working.png cf101610... with historical-byte provenance; revision 6, hash d104f504..."),
    "candidate_commit_document": ref(W + "candidate-commit-document.json"),
    "sample_review_context": ref(W + "sample-review-context.json"),
    "sample_review": ref(W + "sample-review.json", "candidate-review sample-review-150 action complete: canvas(local)/activity(visual)/integration(live) pass; task r.5b1bc38638b68ed8.task done, candidate nominated; revisions 7-9, hash d56114f1..."),
    "sample_review_observation": ref(W + "sample-review-observation.json"),
    "decision_commit": ref(W + "decision-commit.json", "public commit (--expect d56114f1...) adding confirmed destination I r.5b1bc38638b68ed8.destination.working, decision D r.5b1bc38638b68ed8.decision.reuse150 and its live proof E bound to the decision semantic closure; revision 10, hash 4cda7487..."),
    "decision_commit_document": ref(W + "decision-commit-document.json"),
    "production_plan": ref(W + "production-plan-result.json", "production-plan delivery-150 with stages:[] (baseline candidate.working.retained, member output.working, destination destination.working, criteria bytes/continuity/destination); revision 11, hash ec989cbd..."),
    "production_plan_input": ref(W + "production-plan-150.json"),
    "plan_request_review": ref(W + "plan-request-review.json"),
    "family_pre_snapshot": ref(W + "family-pre-snapshot.json"),
    "delivery_build": ref(W + "delivery-build.json", "family-snapshot delivery-150.delivery.output delivery-150.package --expect ec989cbd...; manifest 873d6917...; revision 12, hash dd2970a4..."),
    "delivery_context": ref(W + "delivery-context.json", "review-context delivery-150.package: binding e9fce8bf..., state dd2970a4..., member files/0000.png == cf101610..."),
    "capture_report": ref(W + "capture-report.json", "exact stdout of: node renderer-integration/capture.mjs --project ROOT --out work/integration-change/capture-delivery (exit 0; errors [], missing []); raw capture in capture-delivery/render.json, screenshot capture-delivery/destination.png"),
    "capture_command": ref(W + "capture-delivery.command.txt"),
    "capture_stderr": ref(W + "capture-delivery.stderr.txt"),
    "capture_raw": ref(W + "capture-delivery/render.json"),
    "capture_screenshot": ref(W + "capture-delivery/destination.png"),
    "renderer_check": ref(W + "renderer-check.json", "check.py --project ROOT --capture capture-delivery: status pass, 0 failures, 406 observations, 20 views (exit 0)"),
    "renderer_check_command": ref(W + "renderer-check.command.txt"),
    "destination_report": ref(W + "destination-report.json", "observation.py bridge over capture-delivery + delivery-context.json + destinations-map.json"),
    "destinations_map": ref(W + "destinations-map.json"),
    "destination_import": ref(W + "destination-import.json", "destination-import delivery-150.package -> bundle work/integration-change/destination-bundle/8e7eb349....zip (98059 bytes), 56 previews; files_verified true, renderer_executed false, state_changed false, automatic_acceptance false"),
    "delivery_review": ref(W + "delivery-review.json", "candidate-review delivery-review-150 action complete: bytes(local)/continuity(visual)/destination(live) pass; delivery task done, package nominated; revisions 13-15, hash ad0cfa6d..."),
    "delivery_review_observation": ref(W + "delivery-review-observation.json"),
    "acceptance": ref(W + "acceptance.json", "family report after completion: delivery-150.delivery.task done, no blockers, no pending jobs, snapshot delivery-150.package"),
    "final_selection": ref(W + "final-selection.json", "focused read: next_action delivered, selection_current true, destination_matches true, family accepted true, state ad0cfa6d..."),
    "handoff": {**ref(W + "handoff.json"), "saved_handoff": {"path": handoff["path"], "sha256": handoff["sha256"]}, "note": "plar handoff --view caller; assignment status delivered (agent authored); next delivered"},
    "handoff_details": ref(W + "handoff-details.json"),
    "sample_capture": {"capture_report": ref(W + "capture-sample.stdout.txt"), "raw": ref(W + "capture-sample/render.json"), "screenshot": ref(W + "capture-sample/destination.png"), "renderer_check": ref(W + "renderer-check-sample.json"), "note": "first capture: live evidence for the sample review and the decision proof receipt"},
    "measurements": {"asset_check": ref(W + "working-asset-check.json"), "package_and_art_hashes": ref(W + "package-and-art-hashes.txt")},
    "inspection_views": ref(W + "views/index.json", "derived nearest-neighbour enlargements of existing art used for visual inspection (evidence only, not assets)"),
    "state_reports": {"workflow_initial": ref(W + "state-workflow-initial.json"), "jobs_initial": ref(W + "state-jobs-initial.json"), "validate_initial": ref(W + "state-validate-initial.json"), "validate_after_refusals": ref(W + "state-validate-after-refusals.json"), "workflow_after_sample": ref(W + "state-workflow-after-sample.json")},
    "command_log": ref(W + "command-log.txt"),
    "request_packet_150": {"packet": ref(W + "packet-150.json"), "arguments": ref(W + "arguments-150.json"), "criteria": ref(W + "criteria-150.json"), "connection": ref(W + "connection-150.json")},
    "ids": {
        "plar": "integration-plar.txt", "asset_id": "queue.working", "store": ".pixl/assets/queue.working",
        "old_task": "task", "old_output": "output.working", "old_job": "first_request (failed by local abandonment; never dispatched; remote_id null)",
        "revised_task": "r.5b1bc38638b68ed8.task", "revised_output": "r.5b1bc38638b68ed8.output.working", "revised_job": "r.5b1bc38638b68ed8.request (failed by local abandonment; never dispatched; remote_id null)",
        "candidate": "r.5b1bc38638b68ed8.candidate.working.retained", "destination_choice": "r.5b1bc38638b68ed8.destination.working", "decision": "r.5b1bc38638b68ed8.decision.reuse150", "proof": "r.5b1bc38638b68ed8.proof.reuse150",
        "plan": "delivery-150.plan", "delivery_task": "delivery-150.delivery.task", "delivery_output": "delivery-150.delivery.output", "delivery_candidate": "delivery-150.package",
        "manifest_sha256": "873d6917ed6e80f3302b282b4cb9a84686f3c8e9234497f8151b9997d17f1ead",
        "reviews": ["sample-review-150", "delivery-review-150"], "remote_ids": []},
    "hashes": {"plar_initial": "8ddece433eef4a42ac57db4ea77c46e1e99962d4de969c68b5ca55c9e65b04ad", "plar_after_save": "28657e190427c3033b4ed9c0e835da3ae012c249c9e75dca3e49c89ba7a88daa", "plar_final": sha("integration-plar.txt"),
               "requirements_old": "12cb410ef6f24ed585755beede2c470eb2d3b32574596b11457394c6c0a68eee", "requirements_new": "dc4292427296bdb382c9b5fcd6a8fc0c7678ad214126654fdf962942223b2968",
               "state_initial": "24a52f9ddc15e6149ec42c7bc12011c7675970806efd7261e725ed99f0b906f0", "state_final": "ad0cfa6d9b512a3a11ace7cdf99dd5613e6ffa5336e95cd436452d6b4785ebb6", "state_final_revision": 15,
               "working_png": sha("assets/working.png")},
    "integrity": integrity,
    "scope": "Controlled reused-art Working timing change (100 ms -> 150 ms) in the fresh prospective integration-plar.txt / .pixl/assets/queue.working state. Exact existing assets/working.png reused; no provider call of any kind, no new art, no edits to src/, assets/, renderer-integration/, plar.txt, BRIEF.md, WORKING-TIMING-AMENDMENT.md, work/integration-inputs/ or existing .pixl history/jobs/inputs bytes.",
    "limitations": [
        "Native 1x live playback remains unperformed; live loop playback was observed at the consumer 3x scale (13 samples, three wraps) with separate controlled 1x frame-boundary samples.",
        "Browser evidence is one local headless Chrome 157 run of the isolated renderer-integration fixture per capture; not acceptance by another engine or project.",
        "Acceptance is scoped to this controlled timing change; it is not PixelLab-generated quality evidence. Broader artistic production, host reliability, M1/M2 and broader M3 remain open.",
        "The historical task named task remains open with its plar_selection blocker and its failed (locally abandoned) first_request; its intent and journal bytes are unchanged.",
        "Both refusals (obsolete dispatch/completion) were returned on stderr with exit code 2; the named files are byte copies of that stderr JSON (stdout was empty).",
        "Working and Retry share a circular silhouette family; non-colour distinction rests on segmentation versus a continuous ring with arrowhead, plus Working motion.",
        "The decision proof receipt binds renderer-check-sample.json (first capture); the delivery acceptance rests on the second, fresh capture-delivery bundle.",
    ],
    "next_action": "Parent: consume handoff.json / final-selection.json (state ad0cfa6d..., next delivered); run plar read --since 8ddece43... and focused reads of all five assets; independently open capture-delivery/destination.png and the 1x/3x running cells. No further specialist action is pending for this controlled change.",
}
text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
open(W + "SPECIALIST-RESULT.json", "w", encoding="utf-8", newline="\n").write(text)
print(json.dumps(integrity, indent=1))
print("RESULT sha256", hashlib.sha256(text.encode("utf-8")).hexdigest())
