"""Build SPECIALIST-REPORT.json and details.json for the compact caller handoff.

Usage: python -I -B helper_build.py <consumer_root>
All hashes are computed here from actual file bytes. No PIXL state is touched.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
out = root / "work" / "compact-caller"
NOW = datetime.now(timezone.utc).isoformat()

ASSET_ID = "queue.working"
PLAR_PATH = "authoring-plar.txt"
STORE = ".pixl/assets/queue.ready"
STATE_PATH = ".pixl/assets/queue.ready/state.px"
STATE_HASH = "88d77c62b47eb8fef5d35015973f67b0f38731cb04e54430efa36aec4b898d64"
REQ_HASH = "ec61d688f752ac1280914d22ba75bdb4e8f7e31c42b18d7d62f7a14038eedea5"
UNKNOWN_HASH = "3ab0c1633edbf21977744bab59eb2a15b2cd8dc81424ea3cfe6c569d5f35e0a9"


def sha(rel: str) -> str:
    p = root / rel
    if not p.is_file():
        raise SystemExit(f"missing cited file: {rel}")
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ref(rel: str, role: str | None = None) -> dict:
    r = {"path": rel, "sha256": sha(rel)}
    if role is not None:
        r["role"] = role
    return r


def load(rel: str):
    return json.loads((root / rel).read_text("utf-8"))


# ---- verify the facts we were told against our own saved tool returns ----
plar = load("work/compact-caller/specialist-plar-read.json")
wf = load("work/compact-caller/specialist-workflow.json")
val = load("work/compact-caller/specialist-validate.json")
ready = load("work/compact-caller/specialist-ready.json")
unk = load("work/compact-caller/specialist-unknown-jobs.json")
chk = load("work/compact-caller/specialist-asset-check.json")
rcw = load("work/compact-caller/specialist-review-context-working.json")
rcd = load("work/compact-caller/specialist-review-context-delivery.json")
rr02 = load("work/artistic-revision/request-review-02.json")
prod = plar["production"]
cont = prod["continuation"]
tasks = {t["id"]: t for t in wf["tasks"]}

checks = {
    "plar.requirements_hash": plar["requirements_hash"] == REQ_HASH,
    "plar.path": plar["path"] == PLAR_PATH,
    "plar.asset.id": plar["asset"]["id"] == ASSET_ID,
    "production.store": prod["store"] == STORE,
    "production.hash": prod["hash"] == STATE_HASH,
    "production.revision": prod["revision"] == 108,
    "production.task": prod["task"] == "artistic-02.working.task" and prod["task_state"] == "done",
    "continuation.action": cont["action"] == "delivered",
    "continuation.state_hash": cont["state_hash"] == STATE_HASH,
    "continuation.requirements_hash": cont["requirements_hash"] == REQ_HASH,
    "delivery.destination": cont["delivery"]["destination"] == "assets/working.png",
    "delivery.observed_sha256": cont["delivery"]["observed_sha256"] == "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc",
    "delivery.destination_matches_and_complete": cont["delivery"]["destination_matches"] is True and cont["delivery"]["complete"] is True,
    "delivery.family": (
        cont["delivery"]["families"][0]["task"] == "artistic-02.delivery.task"
        and cont["delivery"]["families"][0]["state"] == "done"
        and cont["delivery"]["families"][0]["accepted"] is True
    ),
    "jobs.single_failed": len(prod["jobs"]) == 1
    and prod["jobs"][0]["id"] == "authoring-01.working.join-01"
    and prod["jobs"][0]["state"] == "failed"
    and prod["jobs"][0]["next_action"] == "review_failure"
    and prod["jobs"][0]["remote_id"] is None,
    "pending_jobs.empty": prod["pending_jobs"] == [],
    "production.next_action": prod["next_action"] == "delivered",
    "selection_current": prod["selection_current"] is True,
    "workflow.hash_revision": wf["hash"] == STATE_HASH and wf["revision"] == 108 and wf["files_verified"] is True,
    "workflow.task.artistic-02.working.done": tasks["artistic-02.working.task"]["state"] == "done",
    "workflow.task.artistic-02.delivery.done": tasks["artistic-02.delivery.task"]["state"] == "done",
    "workflow.task.artistic-01.working.open_changed_plan": tasks["artistic-01.working.task"]["state"] == "open"
    and any("authored plan scope changed" in b for b in tasks["artistic-01.working.task"]["blockers"]),
    "validate.valid_hash_revision": val["valid"] is True and val["hash"] == STATE_HASH and val["revision"] == 108 and val["files_verified"] is True,
    "ready.empty_same_hash": ready["ready"] == [] and ready["hash"] == STATE_HASH,
    "review_context.working": rcw.get("state_hash") == STATE_HASH and rcw.get("revision") == 108,
    "review_context.delivery": rcd.get("state_hash") == STATE_HASH and rcd.get("revision") == 108,
    "asset_check.working_png": chk["sha256"] == "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc"
    and chk["frames"][0]["width"] == 64
    and chk["frames"][0]["height"] == 16
    and chk["frames"][0]["fractional_alpha_pixels"] == 0
    and chk["frames"][0]["visible_pixels"] == 128,
    "unknown.member_job": (
        unk["hash"] == UNKNOWN_HASH
        and unk["revision"] == 9
        and unk["jobs"][0]["id"] == "member.job"
        and unk["jobs"][0]["state"] == "unknown"
        and unk["jobs"][0]["remote_id"] is None
        and unk["jobs"][0]["request"]["provider"] == "fictional-fixture"
        and unk["jobs"][0]["next_action"] == "reconcile"
        and unk["remote_executed"] is False
    ),
    "rr02.plan01": rr02["plan"]["id"] == "artistic-01.plan"
    and rr02["state"]["revision"] == 92
    and any(d.get("status") == "changed_plan_context" for d in rr02["diagnostics"]),
}
failed = [k for k, v in checks.items() if not v]
if failed:
    raise SystemExit(f"verification failed: {failed}")
print("all", len(checks), "verification checks passed")

prior_specialist = load("work/artistic-revision/SPECIALIST-RESULT.json")
prior_caller = load("work/artistic-revision/CALLER-RESULT.json")

working_reqs = prod["outputs"][0]["requirements"]
working_pass = sum(1 for r in working_reqs if r["status"] == "pass")
delivery_task = tasks["artistic-02.delivery.task"]
delivery_reqs = delivery_task["outputs"][0]["requirements"]
delivery_pass = sum(1 for r in delivery_reqs if r["status"] == "pass")

# ---------------------------------------------------------------- report
report = {
    "version": 1,
    "kind": "specialist_detailed_report",
    "assignment": "QOL-10/SC-08 compact-result evaluation, SPECIALIST part: reporting/handoff only; no new art production, no provider call, no acceptance, no state commit.",
    "reviewer": "pixl:pixl specialist (native registered role, host model)",
    "observed_at": NOW,
    "project_root": str(root),
    "identities": {
        "asset_id": ASSET_ID,
        "plar_path": PLAR_PATH,
        "store": STORE,
        "state_path": STATE_PATH,
        "state_hash": STATE_HASH,
        "revision": 108,
        "requirements_hash": REQ_HASH,
        "plar_file_sha256": plar["hash"],
        "hash_domains": {
            "state_hash": "canonical_state_sha256",
            "requirements_hash": "selected_requirements_sha256",
            "plar_file_sha256": "file_sha256",
            "sha256": "file_sha256",
        },
    },
    "verification": {
        "method": "Every fact below was re-read through public local tools in this session and compared by helper_build.py; the exact tool returns are retained under work/compact-caller/.",
        "checks_passed": sorted(checks.keys()),
        "tool_returns": [
            ref("work/compact-caller/specialist-plar-read.json", "pixl_plar_read asset_id=queue.working path=authoring-plar.txt (exact return bytes)"),
            ref("work/compact-caller/specialist-workflow.json", "pixl_workflow .pixl/assets/queue.ready/state.px (exact return bytes)"),
            ref("work/compact-caller/specialist-validate.json", "pixl_validate .pixl/assets/queue.ready/state.px (exact return bytes)"),
            ref("work/compact-caller/specialist-ready.json", "pixl_ready .pixl/assets/queue.ready/state.px"),
            ref("work/compact-caller/specialist-review-context-working.json", "pixl_review_context artistic2.working.candidate (tool-saved result_path)"),
            ref("work/compact-caller/specialist-review-context-delivery.json", "pixl_review_context artistic2.delivery.candidate (tool-saved result_path)"),
            ref("work/compact-caller/specialist-review-context-receipts.json", "the two pixl_review_context receipts (result_sha256 as reported by the tool)"),
            ref("work/compact-caller/specialist-asset-check.json", "pixl_asset_check assets/working.png"),
            ref("work/compact-caller/specialist-unknown-jobs.json", "pixl-unknown pixl_jobs .pixl/state.px (controlled fictional fixture, read only)"),
        ],
        "helper_scripts": [
            ref("work/compact-caller/helper_probe.py", "copied saved returns and probed structure"),
            ref("work/compact-caller/helper_probe2.py", "probed production/task facts and hashed cited files"),
        ],
    },
    "delivered_artistic_production": {
        "scope": "CF-03/TM-04 exact reused-art successor: src/queue-view-artistic.ts module plus renderer-artistic/ browser fixture, consuming the existing accepted asset bytes. Acceptance is scoped to these exact bytes and the supplied local browser destination; it is not a general host-reliability, M1/M2 or generated-quality claim.",
        "plan_id": "artistic-02.plan",
        "scoped_caller_choice": prior_specialist["scoped_caller_choice"],
        "task": {"id": "artistic-02.working.task", "state": "done", "output": "artistic-02.working.output", "candidate": "artistic2.working.candidate", "nominated": True, "criteria_total": len(working_reqs), "criteria_pass": working_pass},
        "family": {"id": "artistic-02.delivery.task", "state": "done", "output": "artistic-02.delivery.output", "candidate": "artistic2.delivery.candidate", "accepted": True, "member_selection_current": True, "criteria_total": len(delivery_reqs), "criteria_pass": delivery_pass, "manifest": cont["delivery"]["families"][0]["manifest"], "manifest_sha256": cont["delivery"]["families"][0]["manifest_sha256"]},
        "continuation": {"action": cont["action"], "next_action": prod["next_action"], "selection_current": prod["selection_current"], "pending_jobs": prod["pending_jobs"], "new_request_allowed": prod["new_request_allowed"], "link_status": prod["link_status"]},
        "delivery": {"destination": cont["delivery"]["destination"], "expected_sha256": cont["delivery"]["expected_sha256"], "observed_sha256": cont["delivery"]["observed_sha256"], "destination_matches": cont["delivery"]["destination_matches"], "complete": cont["delivery"]["complete"], "scope": cont["delivery"]["scope"]},
        "mechanical_recheck_this_session": {"tool": "pixl_asset_check", "sha256": chk["sha256"], "width": chk["frames"][0]["width"], "height": chk["frames"][0]["height"], "visible_pixels": chk["frames"][0]["visible_pixels"], "fractional_alpha_pixels": chk["frames"][0]["fractional_alpha_pixels"], "opaque_components": chk["frames"][0]["opaque_components"], "note": "Measurement only: 64x16 strip, 128 visible pixels (4 cells x 32, consistent with the retained stationary-cell identity record), no fractional alpha. visual_quality_verified and engine_import_verified are false for this call by construction; artistic/engine acceptance rests on the retained artistic2 reviews, not on this measurement."},
        "artifacts": [
            ref("assets/working.png", "delivered Working strip 64x16, four 16x16 cells, 100 ms"),
            ref("assets/error-retry.png", "family member Retry 16x16"),
            ref("assets/paused.png", "family member Paused 16x16"),
            ref("assets/ready-confirmed.png", "family baseline Ready 16x16 (exact ready.retained)"),
            ref("src/queue-view-artistic.ts", "successor consumer module"),
            ref("renderer-artistic/view.mjs", "successor browser fixture"),
            ref("renderer-artistic/capture.mjs", "fixture capture driver"),
            ref("renderer-artistic/check.py", "fixture checker"),
        ],
        "retained_evidence": {
            "prior_specialist_result": ref("work/artistic-revision/SPECIALIST-RESULT.json"),
            "prior_caller_result": ref("work/artistic-revision/CALLER-RESULT.json"),
            "prior_caller_review": ref("work/artistic-revision/CALLER-REVIEW.json"),
            "adopted_criteria": ref("work/artistic-revision/adopted-criteria.json"),
            "current_plan_request_review": ref("work/artistic-revision/request-review-plan02.json"),
            "retained_failures": ref("work/artistic-revision/retained-failures.json"),
            "caller_independent_verification": ref("work/artistic-revision/caller-independent-verification.json"),
            "prior_handoff": ref(".pixl/handoffs/e560a32dcaf31134abbb81b661a0a2fc12824461a049c90b1c780cc01464273d.json"),
            "renderer_captures": [
                ref("work/artistic-revision/capture-switch-04/render.json", "specialist capture, preference switch"),
                ref("work/artistic-revision/capture-initial-reduced-03/render.json", "specialist capture, initial reduced"),
                ref("work/artistic-revision/caller-capture-switch-01/render.json", "caller independent capture, preference switch"),
                ref("work/artistic-revision/caller-capture-initial-reduced-01/render.json", "caller independent capture, initial reduced"),
            ],
            "note": "These renderer captures are retained evidence from the prior acceptance. No renderer was run in this assignment.",
        },
    },
    "historical_creation_acceptance": {
        "meaning": "The delivered bytes cf101610... were created and accepted earlier (byte-identical to live.working-animation-motion-01.candidate under the original 20 criteria). That earlier acceptance is history: artistic-02 re-reviewed the same bytes fresh under its own 29 criteria and did not transfer the old verdicts (frame-assembly verdict reason in the working review; SPECIALIST-RESULT 'Prior acceptance did not transfer').",
        "where": [ref("work/compact-caller/specialist-review-context-working.json", "current working-candidate criteria and verdict ids"), ref("work/artistic-revision/adopted-criteria.json", "original 20 and corrected 29 mapping")],
        "failed_durable_job": {"id": "authoring-01.working.join-01", "task": "authoring-01.working.task", "state": "failed", "remote_id": None, "provider": "pixellab-official-mcp", "tool": "mcp__pixellab__pixelart_workbench", "next_action": "review_failure", "note": "Retained local failed observation on the abandoned authoring branch; no invented remote ID. It is not pending and does not block the delivered artistic-02 continuation (pending_jobs is empty). Left untouched here."},
    },
    "stale_plan01": {
        "plan_id": "artistic-01.plan",
        "plan_file": ref(".pixl/assets/queue.ready/production-plans/9fa2988ddf8a9eae73258d5c3b5fa23dbfc08f6f3dc77b0402fd82855ccbf9a1.json"),
        "diagnostic": ref("work/artistic-revision/request-review-02.json", "production_plan_review of artistic-01.plan at state revision 92"),
        "diagnostic_state": rr02["state"],
        "diagnostics": rr02["diagnostics"],
        "what_it_is": "The first corrected-artistic plan (artistic-01.plan) authored at state revision 92 (state sha 07110fbe...). Its source scope changed (artistic.source.artistic-check and others), so the runtime flags changed_plan_context / changed_source_record / changed_selection; its tasks artistic-01.working/retry/paused/delivery remain open with 'authored plan scope changed' blockers and their selection bindings read status changed (requirements_hash 4ef95442... versus current ec61d688...).",
        "current_status": "History, not current. The current plan is artistic-02.plan whose selection binding is current and whose tasks are done. artistic-01 records were retained unchanged (no removal) per the prior caller verification; pixl_ready lists no ready task.",
        "current_workflow_blockers_artistic-01.working.task": tasks["artistic-01.working.task"]["blockers"],
    },
    "controlled_unknown_job": {
        "label": "CONTROLLED FICTIONAL FIXTURE. Not part of the artistic production and not attached to it.",
        "root": str(root / "controlled-unknown"),
        "store": ".pixl",
        "state_path": ".pixl/state.px",
        "state_hash": UNKNOWN_HASH,
        "revision": 9,
        "job": {"id": "member.job", "task": "member.task", "state": "unknown", "remote_id": None, "provider": "fictional-fixture", "tool": "generate_fixture", "durable": True, "next_action": "reconcile", "remote_executed": False, "intent_sha256": unk["jobs"][0]["intent_sha256"], "request_sha256": unk["jobs"][0]["request"]["request_sha256"], "events": unk["jobs"][0]["events"]},
        "observation": "Read once through mcp__pixl-unknown__pixl_jobs; no dispatch, observe, import or commit was performed; state hash and revision unchanged from the supplied facts. The job has a single local dispatch claim and no provider identity; its unknown outcome can only be resolved by an actual provider observation in its own fixture root. It is the reason this reporting assignment is 'partial'.",
        "evidence": ref("work/compact-caller/specialist-unknown-jobs.json"),
    },
    "inputs": [
        ref("work/compact-caller-inputs/fixtures.json", "assignment fixture identities"),
        ref("work/artistic-revision/CALLER-RESULT.json", "prior caller result"),
        ref("work/artistic-revision/SPECIALIST-RESULT.json", "prior specialist result"),
        ref("work/artistic-revision/request-review-02.json", "stale plan01 diagnostic"),
    ],
    "limits": [
        "No fresh renderer run; integration evidence is the retained prior captures.",
        "No provider observation; the official failed job and the fictional unknown job were only read.",
        "No acceptance, nomination, commit, PLAR save or configuration change.",
        "pixl_asset_check is a measurement; it does not re-establish visual or engine acceptance.",
    ],
}
(out / "SPECIALIST-REPORT.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", "utf-8")
print("SPECIALIST-REPORT.json", sha("work/compact-caller/SPECIALIST-REPORT.json"))

# ---------------------------------------------------------------- details
caller = {
    "summary": (
        "Reporting-only handoff. Artistic production for queue.working remains delivered: "
        "artistic-02.working.task and family artistic-02.delivery.task done, assets/working.png "
        "cf101610... matches, 14/14 working and all family criteria pass (retained reviews, re-read). "
        "Scope: CF-03/TM-04 reused-art successor (src/queue-view-artistic.ts, renderer-artistic/), "
        "exact bytes, local browser destination. Partial: a separately controlled fictional-fixture job "
        "(controlled-unknown member.job) stays unknown, read only. Stale artistic-01.plan is history. "
        "No provider call, renderer run or acceptance here."
    ),
    "artifacts": [
        ref("assets/working.png", "delivered Working strip 64x16"),
        ref("assets/error-retry.png", "family member Retry"),
        ref("assets/paused.png", "family member Paused"),
        ref("assets/ready-confirmed.png", "family baseline Ready"),
        ref("src/queue-view-artistic.ts", "successor consumer module"),
        ref("renderer-artistic/view.mjs", "successor browser fixture"),
        ref("renderer-artistic/check.py", "fixture checker"),
    ],
    "reports": [
        ref("work/compact-caller/SPECIALIST-REPORT.json", "detailed specialist report (this assignment)"),
        ref("work/artistic-revision/SPECIALIST-RESULT.json", "prior specialist result (delivered)"),
        ref("work/artistic-revision/CALLER-RESULT.json", "prior caller acceptance result"),
        ref("work/artistic-revision/request-review-02.json", "stale artistic-01.plan diagnostic (history)"),
        ref("work/compact-caller/specialist-plar-read.json", "focused pixl_plar_read return re-read this session"),
        ref("work/compact-caller/specialist-unknown-jobs.json", "controlled fictional-fixture pixl_jobs return"),
    ],
    "issues": [
        {
            "category": "uncertain_remote_result",
            "summary": "Controlled fictional fixture (not production): controlled-unknown/.pixl job member.job state unknown, remote_id null, provider fictional-fixture, next_action reconcile, state 3ab0c163... rev 9. Read only; untouched.",
            "recovery": "Reconcile inside its own fixture root with an actual provider observation (pixl_job_observe) before any import; never repeat generation on the strength of this report.",
        },
        {
            "category": "stale_local_state",
            "summary": "artistic-01.plan (state rev 92) is retained history: tasks open with 'authored plan scope changed' blockers and changed selection bindings. Current production is artistic-02.plan, selection current.",
            "recovery": "None required; keep as history. Do not reuse artistic-01 criteria or bindings for new work.",
        },
        {
            "category": "unfinished_work",
            "summary": "This assignment ran no renderer and made no provider observation. Failed durable job authoring-01.working.join-01 (next_action review_failure, no remote id) stays retained on the abandoned authoring branch; M1/M2, broader generated quality and general host reliability remain separately open.",
        },
    ],
    "integration": {
        "status": "not_performed",
        "summary": "RETAINED EVIDENCE ONLY, not a fresh renderer run: the prior accepted integration captures (caller independent captures of preference switch and initial reduced motion) are listed as evidence; no renderer was executed in this assignment.",
        "evidence": [
            ref("work/artistic-revision/caller-capture-switch-01/render.json", "retained prior caller capture, preference switch"),
            ref("work/artistic-revision/caller-capture-initial-reduced-01/render.json", "retained prior caller capture, initial reduced"),
        ],
    },
}
caller_bytes = len(json.dumps(caller, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
assert len(caller["summary"]) <= 600, len(caller["summary"])
for i in caller["issues"]:
    assert len(i["summary"]) <= 600 and len(i.get("recovery", "")) <= 600
assert len(caller["integration"]["summary"]) <= 600
assert caller_bytes <= 8192, caller_bytes
print("caller block compact bytes", caller_bytes)

details = {
    "status": "partial",
    "reason": "Combined reporting assignment: the artistic production for queue.working is delivered and unchanged, but the separately controlled remote observation (fictional fixture controlled-unknown member.job, state unknown) is left unresolved by design; no fresh renderer run or provider observation was made.",
    "assignment": "QOL-10/SC-08 compact-result evaluation, SPECIALIST part: reporting/handoff only; no art production, provider call, acceptance, commit, PLAR save or configuration change.",
    "observed_at": NOW,
    "identities": {"asset_id": ASSET_ID, "plar_path": PLAR_PATH, "store": STORE, "state_path": STATE_PATH, "state_hash": STATE_HASH, "revision": 108, "requirements_hash": REQ_HASH, "plar_file_sha256": plar["hash"]},
    "separation": {
        "delivered_artistic_production": {"status": "delivered", "plan_id": "artistic-02.plan", "task": "artistic-02.working.task", "task_state": "done", "candidate": "artistic2.working.candidate", "family_task": "artistic-02.delivery.task", "family_state": "done", "family_candidate": "artistic2.delivery.candidate", "family_accepted": True, "continuation_action": cont["action"], "destination": "assets/working.png", "destination_sha256": cont["delivery"]["observed_sha256"], "destination_matches": True, "scope": "CF-03/TM-04 exact reused-art successor at src/queue-view-artistic.ts and renderer-artistic/; exact bytes and supplied local browser destination only."},
        "partial_assignment": {"status": "partial", "what": "This reporting handoff only. It re-read state, retained a detailed report and published this handoff. It did not run the renderer, observe any provider, or change acceptance.", "why_partial": "A separately controlled remote observation (fictional fixture) remains unknown; the artistic production itself may remain delivered."},
        "historical_creation_acceptance": {"status": "history", "what": "Original creation/acceptance of the same bytes (live.working-animation-motion-01.candidate, original 20 criteria) plus the abandoned authoring branch with failed durable job authoring-01.working.join-01 (state failed, remote_id null, next_action review_failure). Not transferred to artistic-02; artistic-02 re-reviewed fresh."},
        "stale_plan01": {"status": "history_not_current", "plan_id": "artistic-01.plan", "diagnostic": ref("work/artistic-revision/request-review-02.json"), "diagnostic_state_revision": 92, "runtime_flags": [d.get("status") for d in rr02["diagnostics"]], "tasks": "artistic-01.working/retry/paused/delivery remain open with 'authored plan scope changed' blockers; selection binding status changed."},
        "controlled_unknown_job": {"label": "CONTROLLED FICTIONAL FIXTURE, NOT PRODUCTION", "root": "controlled-unknown", "store": ".pixl", "state_path": ".pixl/state.px", "state_hash": UNKNOWN_HASH, "revision": 9, "job_id": "member.job", "state": "unknown", "remote_id": None, "provider": "fictional-fixture", "next_action": "reconcile", "touched": False, "evidence": ref("work/compact-caller/specialist-unknown-jobs.json")},
    },
    "verification_this_session": {"checks_passed": sorted(checks.keys()), "tool_returns": report["verification"]["tool_returns"], "asset_check": chk},
    "detailed_report": ref("work/compact-caller/SPECIALIST-REPORT.json"),
    "retained_specialist_observations": prior_specialist,
    "prior_caller_result": ref("work/artistic-revision/CALLER-RESULT.json"),
    "caller_actions": [
        "Compare this handoff's asset_id/requirements_hash/state_hash with a fresh focused pixl_plar_read before acting.",
        "Treat integration as retained evidence; run renderer-artistic/ afresh if a current integration verdict is needed.",
        "Resolve the controlled-unknown member.job only inside its own fixture root with an actual observation; never attach it to queue.working.",
    ],
    "future_work": [
        "M1/M2 broader generated quality and general host reliability remain open.",
        "Consume the artistic module/renderer with the reused accepted files; acceptance is scoped to the current local browser destination and exact bytes.",
    ],
    "limits": report["limits"],
    "caller": caller,
}
(out / "details.json").write_text(json.dumps(details, indent=2, ensure_ascii=False) + "\n", "utf-8")
print("details.json", sha("work/compact-caller/details.json"), (out / "details.json").stat().st_size)
