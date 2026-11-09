"""Caller script: write caller-review.json, FAMILY-RESULT.json and RENDER-RECHECK-RESULT.json from verified facts (run from the consumer root)."""
import datetime
import hashlib
import json
import re
from pathlib import Path

d = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
sz = lambda p: Path(p).stat().st_size
A = lambda p: {"path": p, "sha256": d(p), "bytes": sz(p)}
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
H = "ea4a61e117eba8f611f2bee1a43ac8e2f1a6296955dc57c9212142f662baeb67"
HP = f".pixl/handoffs/{H}.json"
OLD_PLAR = "71f493b9203f70afe77a4f25c27f4e524a5aa748604a94577bec47b4a97d10de"
OLD_REQ = "806a1f2d21914fe2ffa0b11cbe8556ea4d64fd5aeb1dc2aae52e60796cf2d673"
NEW_REQ = "29a330a3e5c378c80f59ed6d6d42c539ea99d7d0e5d88575d98aaca60ec0661e"
STATE = "7a97831f618ffe1c761c0f839525bf4d763eacb56c7fb05b26f15f9ad3da1a81"
READY = "fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5"
REQ_BY_ROW = {
    "queue.ready": NEW_REQ,
    "queue.working": "c6b5121c05396b2d21c68669dc9deffb8f71e9e44ddeb48ada7fec44d01126e5",
    "queue.retry": "c0404a1486c4a700a5342e3926de3abe363d8362a2ed11ef3a9756ede308bd4a",
    "queue.paused": "0bb25469522009a4ad8830b5d92b9e393da336d45d69179029bb82c7e5ecd935",
    "queue.start": "d25bb8982e69cb1f0a2fb448893bfa29432f21f498368312e58cbdba26250c42",
}
DIAG = {
    "task": "r.22e90a2a03fe453a.task (done)",
    "bound_requirements_hash": OLD_REQ,
    "current_requirements_hash": NEW_REQ,
    "selection_status": "changed",
    "derived_next_action": "review_contract",
    "handling": "preserved; the six historical verdicts remain valid for the historical contract only; old jobs not rebound, done task not reopened, verdicts not transferred; new Ready generation only under explicit new authorization against the corrected packet work/queue.ready-reassessment/request-review.json",
}
NOT_DONE = [
    "no new generation, provider call, job preparation or dispatch",
    "no edits to renderer/ or renderer-recheck/, historical contracts, verdicts, candidate, PX2 state, PLAR history or prior results",
    "no family plan, family snapshot or completed-family claim",
    "no relabelling of the historical renderer trial",
]
assert d(HP) == H, "handoff self-hash mismatch"
assert d(".pixl/assets/queue.ready/state.px") == STATE, "PX2 state changed"
assert d("assets/ready-confirmed.png") == READY

review = {
    "version": 1,
    "role": "calling agent independent comparison for RENDER-RECHECK.md (renderer recheck) and the interrupted RENDER-STAGE.md family/style review; recorded after both PIXL rounds",
    "recorded_at": now,
    "verdict": "consistent",
    "assignment": {"RENDER-RECHECK.md": d("RENDER-RECHECK.md"), "RENDER-STAGE.md": d("RENDER-STAGE.md"), "AGENTS.md": d("AGENTS.md")},
    "delegation": {
        "round_1": {"specialist": "native agent type 'pixl' (agents.json), Claude Code subagent a49b4d400a055050a, foreground (run_in_background false), 64 tool uses", "assigned": "fresh renderer-recheck capture + check, visual review, the never-written render-stage review, renderer-recheck review, PLAR proposal (not saved) with requirements_hash probes", "result": "delivered; plar.txt and PX2 untouched as instructed"},
        "round_2": {"specialist": "native agent type 'pixl', Claude Code subagent a1622a7acdc67cf12, foreground; ARTIFACT-BASED RESTART because SendMessage to a49b4d400a055050a failed ('No transcript found for agent ID'); the saved assignment, round-1 files, caller decision and exact state identities were passed explicitly", "assigned": "build and save the PLAR document per the caller's choices (adopt; drop U18; keep U11/U19; two caller evidence links), re-read, pixl_plar_handoff", "result": "delivered; save performed through the kit CLI 'plar save' (same deterministic operation as pixl_plar_save, same expect) because the specialist chose to pass the document file; first pixl_plar_handoff call rejected for a free-text status and re-issued with status 'delivered' (no side effect)"},
        "previous_host_interruption": "The RENDER-STAGE.md stage's background PIXL child was stopped by the host; its drafts in work/render-stage-pixl/ were preserved and read, and its render-review.json (cited by its own drafts) was written in round 1 by the new instance as an artifact-based restart. Drafts were treated as useful work, not adoption.",
    },
    "round_1_comparison": {
        "hashes": "Every sha256 reported by the specialist matched disk (capture files, check output, measurements, render-review, render-recheck-review, proposals, ledgers).",
        "capture_identity": "work/render-recheck-pixl-01/destination.png == work/render-recheck-caller-01/destination.png (a7f8ed81...); all eight view PNGs identical to each other's capture and to the historical work/render-caller-01 and work/render-pixl-01 views; render.json differs only in observed_at.",
        "checker": "Caller re-ran renderer-recheck/check.py on the specialist capture: pass, 104 observations, failures []; observation list identical to the specialist's saved stdout (work/render-recheck-review/caller-check-of-pixl-capture.json). Caller's own capture also 104/104 (work/render-recheck-caller-01-check.json).",
        "placement": "Caller confirmed every available canvas equals the screenshot crop at its reported integer bounds (zero difference) in the specialist capture; bounds x 247/463/679/895 equal the historical best-match positions (old reported x + 9).",
        "old_vs_new": "Caller measured old (1d13cde1...) vs new (a7f8ed81...) screenshots: bbox (112,293)-(114,324), 8 differing pixels, max channel difference 1. Matches the specialist's statement.",
        "label_gaps": "Caller re-measured first-ink gaps on the new screenshot: Ready 13 px (full) / 7 px (compact) at 1x and 3x; Start 12 / 6. Matches measurements.json.",
        "review_files": "render-review.json 'viewed' entries cite only existing files with correct hashes; render-recheck-review.json resolves/cannot-resolve lists agree with the checker scope and with RENDER-RECHECK.md's limits; the explicit statement that no scoped style revision is required is consistent with pixel-identical canvases.",
        "proposals": "Both proposal documents parse, keep version 1, the project block, the five asset IDs in order; all cited source/evidence paths exist; reference source IDs resolve. Hash probes used scratch copies; the live plar.txt was unchanged (71f493b9...) until round 2.",
        "numerical_reconciliation": "Caller independently decoded the Start views: 28 non-accent non-panel pixels at 1x, 84 at 3x, 9 distinct colours, max diff 132 vs nearest upscale. The earlier caller note's '4 -> 12' is wrong; the specialist's 28/84 is right; the qualitative re-rasterisation conclusion stands. Fixture pixel map, arm runs and 29/227 counts confirmed.",
        "visual": "Caller viewed destination.png (both captures), view-001/004/005 and the specialist's grayscale and 3x-column crops: check reads as completion beside 'Ready' in both consumers at 1x and 3x; panel shows through; 3x blocks uniform; Start is an anti-aliased vector beside it; absent members show 'Missing asset'. Agrees with the specialist's observations.",
        "discrepancies": [],
    },
    "caller_style_decision": {"path": "work/render-recheck-review/caller-style-decision.json", "sha256": d("work/render-recheck-review/caller-style-decision.json"), "decision": "ADOPT (scoped) the delivered Ready sample fc5e43ae... as the family style baseline", "choices_for_save": ["adopt variant", "drop U18 (queue.start requirements_hash kept stable)", "keep U11 and U19", "append caller decision artifact and caller capture to queue.ready evidence"]},
    "round_2_comparison": {
        "plar_file": {"old": OLD_PLAR, "new": d("plar.txt"), "retained_history": f".pixl/plar-history/{OLD_PLAR}.json (sha256 equals the old file hash: {d(f'.pixl/plar-history/{OLD_PLAR}.json') == OLD_PLAR})"},
        "saved_document": "plar.txt JSON == work/render-recheck-pixl/plar-update-saved.json JSON (caller check True). Diff vs the adopt proposal is exactly: queue.start existing[0].role restored to the live text, plus two queue.ready evidence entries (caller decision artifact, caller capture). No other field differs.",
        "cited_paths": "Every source and evidence path in the saved plar.txt exists (caller check: none missing).",
        "requirements_hash": {"queue.ready": f"{OLD_REQ[:8]}... -> {NEW_REQ}", "queue.working": "02a94ddf... -> " + REQ_BY_ROW["queue.working"], "queue.retry": "b864ea4e... -> " + REQ_BY_ROW["queue.retry"], "queue.paused": "1a18831f... -> " + REQ_BY_ROW["queue.paused"], "queue.start": "d25bb898... unchanged (caller focused read)", "matches_round_1_probes": True},
        "production_selection_diagnostic": "Caller fresh focused read and pixl_jobs/pixl_workflow: r.22e90a2a03fe453a.selection bound 806a1f2d..., current 29a330a3..., status 'changed'; selection_current false; derived next_action review_contract; new_request_allowed false; pending_jobs []; the done task now lists blocker 'plar_selection: current consumer requirements differ'. Preserved as the expected consequence of a deliberate requirements revision; no rebinding, no reopening, no verdict transfer.",
        "px2_state": "pixl_validate after save and handoff: valid, revision 14, hash 7a97831f..., 87 records, files_verified; file sha256 identical. pixl_jobs: both jobs unchanged (first_request failed; r.22e90a2a03fe453a.request succeeded, candidate ready.retained).",
        "handoff": {"path": HP, "sha256": d(HP), "self_hash_matches_filename": True, "resume_equals_fresh_focused_read": "store .pixl/assets/queue.ready, state_hash 7a97831f..., asset queue.ready, requirements_hash 29a330a3..., task r.22e90a2a03fe453a.task, action review_contract, job r.22e90a2a03fe453a.request/controlled-create-0002 succeeded: all equal to the caller's fresh pixl_plar_read continuation; selection.hash bb997899... equals the current plar.txt hash", "details_checked": "status delivered (specialist scope) with status_statement; restart_note present; artifact hashes match disk; caller_actions and future_work present; production_selection_diagnostic present"},
        "unchanged_files": "renderer/ and renderer-recheck/ (all five files each), assets/ready-confirmed.png, assets/start.svg, src/*.ts, preserved drafts in work/render-stage-pixl/ and work/render-stage-review/, historical captures work/render-caller-01 and work/render-pixl-01, prior results PARENT/COLD/DELIVERY/HANDOFF-RESULT.json: hashes unchanged versus work/render-recheck-review/caller-notes-pre-specialist.json.",
        "discrepancies": [],
        "non_blocking_observations": ["The specialist saved via the kit CLI rather than the pixl_plar_save MCP call; same operation, same expect token, result verified byte-for-byte, so accepted.", "plar-after-save.json predates the handoff and does not list it; the handoff lists plar-after-save.json."],
    },
    "not_done_by_design": ["no provider call or new generation", "no edit to renderer/ or renderer-recheck/", "no PX2 commit, family plan, rebinding or verdict transfer", "no new artwork; absent members remain absent", "no 'integrated' label (production-host display unverified)"],
}
Path("work/render-recheck-review/caller-review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")

family = {
    "version": 1,
    "role": "calling agent",
    "status": "delivered",
    "status_scope": "RENDER-STAGE.md stage completed in this explicitly guided continuation after the original caller was interrupted (its background PIXL child was stopped by the host; no FAMILY-RESULT.json existed). The representative Ready sample was reviewed in the actual rendered consumers, the caller made the scoped style decision (ADOPT), PLAR was updated with the source-bound baseline and renderer evidence, and an exact handoff was retained. The family remains unfinished: Working, Retry and Paused are absent (never produced, not rejected). No generation, provider call, credential, install, host-setting, renderer or PX2 change occurred. This is not an unassisted pass of the original trial: the renderer repair in RENDER-RECHECK.md supplied the capture correction, and the original renderer/ captures with their 9 failed checks remain the historical record.",
    "recorded_at": now,
    "assignment": {"RENDER-STAGE.md": A("RENDER-STAGE.md"), "continued_under": A("RENDER-RECHECK.md")},
    "workspace": str(Path.cwd()).replace("\\", "/"),
    "asset_id": "queue.ready",
    "requirements_hash": {"at_stage_start": OLD_REQ, "after_style_decision_save": NEW_REQ},
    "provider_simulated": True,
    "interrupted_original_delivery": {
        "what_was_preserved": "Caller pre-specialist notes (work/render-stage-review/caller-visual-notes-pre-specialist.json), caller capture work/render-caller-01 with renderer/check.py 95/104 and offset search; specialist capture work/render-pixl-01 with 95/104, measurements.json, assessment-crosscheck.json, adopt/no-adopt PLAR proposals and ledgers, hash probes and crops in work/render-stage-pixl/. The specialist's render-review.json was never written and no PLAR/PX2 save or handoff occurred.",
        "how_resolved": "A new PIXL instance wrote work/render-stage-pixl/render-review.json as an artifact-based restart from those drafts plus a fresh corrected capture; the caller independently compared the drafts, the new review and its own evidence before deciding.",
        "numerical_reconciliation": "Earlier caller note claimed Start vector anti-aliased edge pixels '4 -> 12'; decoded images show 28 at 1x and 84 at 3x (9 colours, linear 3x). The specialist's measurements were correct; all other preserved numbers (pixel map, arms 7/19 px, bbox 11x9, dx=+9, gaps 12/6, 29/261 accent px, triangle 10x12) confirmed.",
    },
    "style_decision": {
        "decision": f"ADOPT the delivered Ready sample assets/ready-confirmed.png (sha256 {READY}; PX2 candidate ready.retained, task r.22e90a2a03fe453a.task done) as the scoped family style baseline for queue.working, queue.retry and queue.paused.",
        "decided_by": "calling agent under RENDER-STAGE.md lines 4-6, using the specialist recommendation (work/render-stage-pixl/render-review.json) and the caller's independent review",
        "artifact": A("work/render-recheck-review/caller-style-decision.json"),
        "establishes": ["hard binary pixel edges, no anti-aliasing or outline", "about 2 px perpendicular stroke (3-px diagonal runs, 2-px orthogonals)", "flat single cool-blue primary fill (#70b9ed as rendered, equal to the Start fill); no fixed palette", "footprint about 9-12 px in a centred 12x12 safe area, mass comparable to 29 px", "transparent exterior, no plate; binary alpha in practice (full alpha still permitted by the contract)"],
        "does_not_establish": ["silhouettes of Working, Retry, Paused", "Working motion/timing or that it cannot read as success", "non-colour distinction among members", "Paused comparison and collective family continuity", "PixelLab-generated quality (controlled pixellab-test fixture)", "production-host display acceptance"],
        "separation_of_acceptances": {"sample_style_adoption": "done (this decision)", "available_member_destination": "Ready and Start exercised in the representative fixture renderer in both consumers at 1x/3x with 104/104 checks; production host unverified", "collective_family_acceptance": "not possible: members absent, no PX2 family plan", "pixellab_generated_quality": "not established (provider_simulated=true)"},
    },
    "renderer_evidence": {
        "historical_renderer": {"captures": ["work/render-caller-01", "work/render-pixl-01"], "checker": "renderer/check.py 95/104 (work/render-stage-review/check-render-caller-01.json, work/render-stage-pixl/check-render-pixl-01.json)", "failures": "'screenshot and observed viewport dimensions' + 8 'screenshot matches canvas pixels'; diagnosed then and confirmed now as a dx=+9 capture-layout bookkeeping offset (DOM measured at 1262x904, screenshot 1280x1000), not a rendering defect; preserved unchanged"},
        "corrected_renderer": {"captures": ["work/render-recheck-caller-01 (caller)", "work/render-recheck-pixl-01 (specialist)"], "screenshot_sha256": d("work/render-recheck-pixl-01/destination.png") + " (both captures byte-identical)", "checker": "renderer-recheck/check.py 104/104 on both captures; caller re-ran it on the specialist capture", "canvases": "all eight view PNGs byte-identical to the historical captures"},
        "observed": "ok -> succeeded -> label Ready with assets/ready-confirmed.png in statusCell and compactStatus at 1x and 3x; canvases are exact alpha composites on #172336 with nearest 3x3 blocks; idle -> Start renders the preserved anti-aliased SVG; running/paused/failed show 'Missing asset' with labels Working/Paused/Retry; no view invented for absent members.",
    },
    "family_state": {
        "available": [{"asset_id": "queue.ready", "path": "assets/ready-confirmed.png", "sha256": READY, "status": "in_progress; delivered sample, adopted scoped baseline; six historical verdicts pass; selection binding now 'changed' (see production_selection_diagnostic)"}, {"asset_id": "queue.start", "path": "assets/start.svg", "sha256": d("assets/start.svg"), "status": "deferred (preserved existing vector); rendered for idle in both consumers; requirements_hash unchanged d25bb898..."}],
        "absent_not_rejected": [{"asset_id": "queue.working", "path": "assets/working.png", "frames": 4, "status": "todo; references[style] and approved_style_reference now bound to ready-sample"}, {"asset_id": "queue.retry", "path": "assets/error-retry.png", "status": "todo; same bindings"}, {"asset_id": "queue.paused", "path": "assets/paused.png", "status": "todo; same bindings"}],
        "rejected": "none; failed job first_request (controlled-create-0001) produced no image and is retained provider history",
        "px2_family_plan": "none (pixl_family: families []); not manufactured",
    },
    "plar_update": {
        "old_hash": OLD_PLAR, "new_hash": d("plar.txt"),
        "saved_document": A("work/render-recheck-pixl/plar-update-saved.json"), "delta_vs_proposal": A("work/render-recheck-pixl/plar-saved-delta.json"), "change_ledger": A("work/render-recheck-pixl/plar-change-ledger.json"), "save_result": A("work/render-recheck-pixl/plar-save-result.json"), "after_save": A("work/render-recheck-pixl/plar-after-save.json"),
        "history_retained": f".pixl/plar-history/{OLD_PLAR}.json",
        "hash_covered_changes": ["sources +ready-sample, renderer-view (renderer-recheck/view.mjs), render-stage, render-recheck", "queue.ready existing role, delivery checks 4 and 5 refreshed (stale text from ledger C17)", "queue.ready approved_style_reference -> requirement (adopted baseline)", "queue.ready renderer_display_observation added (observation)", "queue.working/retry/paused references[style] + approved_style_reference -> requirement", "queue.working renderer_frame_extraction unknown -> observation"],
        "hash_safe_changes": ["coverage included/unresolved", "questions and next on all rows", "evidence links (+10 queue.ready, +1 each other row)"],
        "requirements_hash_by_row": REQ_BY_ROW,
        "status_labels": "queue.ready in_progress (unchanged; integrated would be a caller claim without production-host display); working/retry/paused todo; start deferred",
    },
    "production_selection_diagnostic": DIAG,
    "px2_state": {"path": ".pixl/assets/queue.ready/state.px", "sha256": STATE, "revision": 14, "changed_this_stage": False},
    "independent_comparison": A("work/render-recheck-review/caller-review.json") | {"verdict": "consistent"},
    "handoff": {"path": HP, "sha256": H, "bytes": sz(HP), "saved_by": "pixl_plar_handoff (specialist, round 2)", "state_hash": STATE, "requirements_hash": NEW_REQ, "derived_next": "review_contract", "selection_hash": d("plar.txt"), "caller_verification": "resume block equals the caller's fresh pixl_plar_read continuation"},
    "specialist_artifacts": [A(p) | {"role": r} for p, r in [("work/render-stage-pixl/render-review.json", "specialist render-stage review and style recommendation (adopt, scoped)"), ("work/render-recheck-pixl/render-recheck-review.json", "specialist renderer-recheck review"), ("work/render-recheck-pixl/measurements.json", "specialist Pillow measurements of the recheck capture"), ("work/render-recheck-pixl/check-render-recheck-pixl-01.json", "renderer-recheck/check.py 104/104"), ("work/render-recheck-pixl-01/render.json", "specialist recheck capture report"), ("work/render-recheck-pixl-01/destination.png", "specialist recheck screenshot")]],
    "caller_artifacts": [A(p) | {"role": r} for p, r in [("work/render-recheck-review/caller-notes-pre-specialist.json", "caller notes and baseline hashes before delegation"), ("work/render-recheck-caller-01/render.json", "caller recheck capture report"), ("work/render-recheck-caller-01/destination.png", "caller recheck screenshot"), ("work/render-recheck-caller-01-check.json", "renderer-recheck/check.py on the caller capture, 104/104"), ("work/render-recheck-review/caller-check-of-pixl-capture.json", "caller re-run of the checker on the specialist capture, 104/104"), ("work/render-recheck-review/caller-style-decision.json", "caller scoped style decision"), ("work/render-recheck-review/caller-review.json", "caller independent comparison"), ("work/render-recheck-review/write-results.py", "script that wrote caller-review.json, FAMILY-RESULT.json and RENDER-RECHECK-RESULT.json")]],
    "preserved_historical": [A(p) for p in ["work/render-stage-review/caller-visual-notes-pre-specialist.json", "work/render-stage-review/check-render-caller-01.json", "work/render-stage-review/screenshot-offset-search.json", "work/render-stage-pixl/check-render-pixl-01.json", "work/render-stage-pixl/measurements.json", "work/render-stage-pixl/assessment-crosscheck.json", "work/render-stage-pixl/plar-update-proposal.json", "work/render-stage-pixl/plar-change-ledger.json", "work/render-caller-01/destination.png", "work/render-pixl-01/destination.png", "HANDOFF-RESULT.json", "DELIVERY-RESULT.json", "COLD-RESULT.json", "PARENT-RESULT.json", ".pixl/handoffs/193d971414213cf407e19fa244b3f1f9f51f593c808f7236c7b41b2c8388427c.json"]],
    "unresolved_obligations": ["Working, Retry and Paused production under the adopted baseline: each needs a fresh caller-compared request/criteria packet, pixl_plar_prepare, explicit new provider authorization, renderer-recheck capture and check, grayscale non-colour comparison; Working additionally needs interactive playback review (node renderer-recheck/server.mjs).", "PX2 family plan (baseline ready.retained, members, destination choices, collective continuity criterion) before any collective acceptance.", "Production-host display verification before labelling queue.ready integrated.", "queue.ready selection binding 'changed' remains a visible diagnostic until a deliberate decision on the sample contract; any new Ready generation needs explicit new authorization."],
    "not_done_by_design": NOT_DONE,
    "next": f"Produce the absent members under the adopted baseline, one at a time, starting with queue.working (fresh caller-compared packet, pixl_plar_prepare, explicit new authorization), then capture each with renderer-recheck/ and compare the family in grayscale; resume from the handoff {H[:8]}... after rereading focused PLAR (plar {d('plar.txt')[:8]}..., state {STATE[:8]}...).",
}
Path("FAMILY-RESULT.json").write_text(json.dumps(family, indent=2) + "\n", encoding="utf-8")

recheck = {
    "version": 1,
    "role": "calling agent",
    "status": "delivered",
    "status_scope": "RENDER-RECHECK.md continuation complete: the focused renderer recheck was delegated to the native PIXL agent in the foreground, its actual new screenshots, pixel report, findings and continuation were independently opened and verified by the caller, the interrupted RENDER-STAGE.md family/style review was finished (FAMILY-RESULT.json), the style decision and renderer evidence were saved to PLAR through the existing operations, and a fresh exact handoff was retained. Explicitly guided by a maintainer renderer repair; the original trial's 95/104 result stays historical and is not relabelled. Family unfinished: Working, Retry, Paused absent. No generation, provider call, credential, install, host-setting, renderer or PX2 change.",
    "recorded_at": now,
    "assignment": A("RENDER-RECHECK.md"),
    "workspace": str(Path.cwd()).replace("\\", "/"),
    "asset_id": "queue.ready",
    "requirements_hash": {"before": OLD_REQ, "after": NEW_REQ},
    "provider_simulated": True,
    "delegation": {
        "round_1": {"specialist": "native agent type 'pixl' (agents.json), Claude Code subagent a49b4d400a055050a, foreground", "skills_supplied": "pixl:pixl (Skill invocation); .agents/skills/pixl-kit skills/pixl, skills/plar, PROFILE.md, delegation/family-delivery/inspection/format references", "assignment_supplied": "RENDER-RECHECK.md and RENDER-STAGE.md verbatim paths, AGENTS.md constraints, absolute consumer root, established hashes/state identity, preserved drafts inventory, caller capture results, required deliverables and prohibitions (no PLAR save/PX2 change/handoff in round 1)", "result": "delivered: work/render-recheck-pixl-01 capture, 104/104 check, measurements, render-review (never-written render-stage review), render-recheck-review, PLAR proposals + ledgers + hash probes"},
        "round_2": {"specialist": "native agent type 'pixl', Claude Code subagent a1622a7acdc67cf12, foreground", "restart": "artifact-based restart: SendMessage to a49b4d400a055050a failed with 'No transcript found for agent ID'; the caller passed the saved assignment, round-1 files, exact state identities and its decision explicitly; no resumed conversation is claimed", "result": "delivered: PLAR saved (expect 71f493b9... -> bb997899...), focused re-reads, pixl_plar_handoff ea4a61e1..."},
        "follow_up_messages": 0,
        "foreground": "both rounds run with run_in_background false; the caller waited for each report before comparing",
    },
    "new_evidence": {
        "renderer_recheck_helper": {name: d(f"renderer-recheck/{name}") for name in ["capture.mjs", "check.py", "view.mjs", "index.html", "server.mjs"]} | {"note": "only capture.mjs differs from renderer/ (CDP device metrics 1280x1000 before navigation; report, layout and screenshot in one page session); not edited by anyone this stage"},
        "specialist_capture": {"directory": "work/render-recheck-pixl-01", "render_json": A("work/render-recheck-pixl-01/render.json"), "screenshot": A("work/render-recheck-pixl-01/destination.png"), "views": {f"view-{i:03d}.png": d(f"work/render-recheck-pixl-01/view-{i:03d}.png") for i in range(8)}, "checker": A("work/render-recheck-pixl/check-render-recheck-pixl-01.json") | {"status": "pass", "observations": 104, "failures": []}, "measurements": A("work/render-recheck-pixl/measurements.json")},
        "caller_capture": {"directory": "work/render-recheck-caller-01", "render_json": A("work/render-recheck-caller-01/render.json"), "screenshot": A("work/render-recheck-caller-01/destination.png"), "checker": A("work/render-recheck-caller-01-check.json") | {"status": "pass", "observations": 104, "failures": []}},
        "caller_recheck_of_specialist_capture": A("work/render-recheck-review/caller-check-of-pixl-capture.json") | {"status": "pass", "observations": 104, "identical_observations_to_specialist_stdout": True},
        "findings": {"render_review": A("work/render-stage-pixl/render-review.json"), "render_recheck_review": A("work/render-recheck-pixl/render-recheck-review.json"), "style_revision_required_by_recheck": False},
        "what_changed_vs_historical": "viewport reported 1280x1000 (was 1262x904); canvas bounds x +9 (247/463/679/895); screenshot differs in 8 border pixels by at most 1 level; all eight canvases pixel-identical; checker 104/104 (was 95/104). The 9 historical failures are a capture-layout bookkeeping offset, not a rendering defect; they remain in the historical files.",
    },
    "caller_comparison": A("work/render-recheck-review/caller-review.json") | {"verdict": "consistent", "discrepancies": 0, "viewed_by_caller": ["work/render-recheck-caller-01/destination.png", "work/render-recheck-pixl-01/destination.png", "view-001/004/005 (caller capture)", "specialist crops: crop-succeeded-row-grayscale-2x.png, crop-full-column-start-ready-3x-3x.png"], "numerical_reconciliation": "earlier caller note '4 -> 12' Start edge pixels is wrong; 28/84 confirmed by the caller's own decode"},
    "available_member_destination_outcome": {
        "queue.ready": {"delivery_check_4": "Exercise both statusCell and compactStatus in an actual renderer: observed ok -> succeeded -> label Ready with assets/ready-confirmed.png in both consumers at 1x and 3x; screenshot/canvas correspondence 104/104 in the representative fixture renderer (recorded in plar.txt delivery.checks[3] status text, renderer_display_observation requirement and evidence links)", "delivery_check_3_display": "canvases equal straight-alpha composites on #172336 with nearest 3x3 blocks, zero difference", "scope": "representative headless Chrome 156 fixture at DPR 1 only; production-host display unverified; status stays in_progress"},
        "queue.start": {"delivery_check_2": "idle resolves to the preserved Start control (sha ee2ba2fe... unchanged) in both consumers at 1x and 3x; browser-rasterised with anti-aliasing (28/84 intermediate pixels); recorded in queue.start evidence and next (role text deliberately unchanged, requirements_hash stable)"},
        "recorded_through": "pixl_plar_save (kit CLI route, same operation and expect) and pixl_plar_handoff; no PX2 verdict was created because no saved criterion covers renderer display and the done task is not reopened",
        "cannot_pass": "any collective criterion requiring the absent members, their animation, non-colour distinction or full family continuity",
    },
    "style_decision": {"decision": "ADOPT (scoped) the delivered Ready sample fc5e43ae... as the family style baseline", "artifact": A("work/render-recheck-review/caller-style-decision.json"), "preserved_from_render_stage": "The decision was never saved before this continuation (interrupted); the preserved drafts leaned adopt (specialist) and lean-adopt (caller). The new evidence required no scoped revision; the decision was made and saved here. See FAMILY-RESULT.json."},
    "plar": {"old_hash": OLD_PLAR, "new_hash": d("plar.txt"), "saved_document": A("work/render-recheck-pixl/plar-update-saved.json"), "delta": A("work/render-recheck-pixl/plar-saved-delta.json"), "save_result": A("work/render-recheck-pixl/plar-save-result.json"), "after_save": A("work/render-recheck-pixl/plar-after-save.json"), "history_retained": f".pixl/plar-history/{OLD_PLAR}.json", "requirements_hash_by_row": REQ_BY_ROW, "production_selection_diagnostic": DIAG},
    "px2_state": {"path": ".pixl/assets/queue.ready/state.px", "sha256": STATE, "revision": 14, "changed": False, "pending_jobs": [], "families": []},
    "family_result": A("FAMILY-RESULT.json"),
    "remaining_family_work": [
        "queue.working (assets/working.png, 64x16 four-frame strip, 100 ms): fresh caller-compared request/criteria packet under the adopted baseline -> pixl_plar_prepare -> explicit new provider authorization -> renderer-recheck capture + check (expect timeline frames 0,0,1,1,2,2,3,3,0) -> interactive playback review via node renderer-recheck/server.mjs -> grayscale comparison with Ready/Start; must not read as success",
        "queue.retry (assets/error-retry.png): same path; non-colour distinction from Ready check and Working frames",
        "queue.paused (assets/paused.png): same path; non-colour distinction from activity, completion and retry",
        "PX2 family plan (baseline ready.retained, ordered members, destination choices, collective continuity criterion) saved before any collective acceptance; family snapshot only when every member has a nominee on a done task",
        "production-host display verification before an integrated label on queue.ready",
        "queue.ready: selection binding 'changed' stays visible; new Ready generation only under explicit new authorization against the corrected packet bef24027...",
    ],
    "handoff": {"path": HP, "sha256": H, "bytes": sz(HP), "state_hash": STATE, "state_revision": 14, "requirements_hash": NEW_REQ, "derived_next": "review_contract", "selection_hash": d("plar.txt"), "details_status": "delivered (specialist scope) with status_statement and restart_note", "caller_verification": "resume block equals the caller's fresh pixl_plar_read continuation after the save (store, state_hash, asset, requirements_hash, task, action, job); file self-hash matches its name"},
    "not_done_by_design": NOT_DONE,
    "next": f"Actual next useful production action: prepare queue.working under the adopted baseline (fresh caller-compared packet, pixl_plar_prepare, explicit new authorization), then capture it with renderer-recheck/ and review playback interactively. Resume from handoff {H[:8]}... after rereading focused PLAR (plar {d('plar.txt')[:8]}..., requirements_hash {NEW_REQ[:8]}..., state {STATE[:8]}...).",
}
Path("RENDER-RECHECK-RESULT.json").write_text(json.dumps(recheck, indent=2) + "\n", encoding="utf-8")

for p in ["work/render-recheck-review/caller-review.json", "FAMILY-RESULT.json", "RENDER-RECHECK-RESULT.json"]:
    print(p, d(p), sz(p))
missing = []
for f in ["FAMILY-RESULT.json", "RENDER-RECHECK-RESULT.json", "work/render-recheck-review/caller-review.json"]:
    for m in set(re.findall(r'"path": "([^"]+)"', Path(f).read_text(encoding="utf-8"))):
        if not Path(m).exists():
            missing.append((f, m))
print("missing cited paths:", missing)
