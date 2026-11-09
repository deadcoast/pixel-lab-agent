"""Exercise connected authoring through an isolated installed CLI, using fixture bytes."""

import json
from copy import deepcopy
from hashlib import sha256
from pathlib import Path


def run_production_plan_probe(invoke, project):
    project = Path(project)
    folder = str(project / ".pixl")
    state = str(project / ".pixl/state.px")
    root = str(project)
    before = invoke(["decode", state])
    records = {r["id"]: r for r in before["records"]}
    allocation = {
        "version": 1, "project": {"name": "Synthetic family", "brief": "Distribution mechanics only"},
        "coverage": {"included": ["Synthetic member output"], "excluded": ["Real consumer code"], "unresolved": []},
        "sources": [{"id": "fixture", "path": "source.txt", "sha256": sha256((project / "source.txt").read_bytes()).hexdigest()}],
        "assets": [{
            "id": "fixture.member", "kind": "sprite", "purpose": "Exercise retained synthetic member revision", "status": "todo",
            "consumers": [{"source": "fixture", "symbol": "member.output", "usage": "Synthetic graph fixture only"}],
            "existing": [], "requirements": [{"property": "raster_size", "value": [2, 2], "authority": "proposal", "sources": ["fixture"], "reason": "Developer fixture choice, not a real art requirement"}],
            "delivery": {"path": "fixture-successor.png", "checks": ["Synthetic fixture identity"]},
            "depends_on": [], "questions": [], "next": "Author fixture", "evidence": [],
        }],
    }
    (project / "plar.txt").write_text(json.dumps(allocation), encoding="utf-8")
    selected = invoke(["plar", "read", "--asset", "fixture.member", "--root", root])
    criteria = [
        {
            "id": "shape",
            "check": "Retain the synthetic fixture identity",
            "domain": "visual",
            "mode": "visual",
            "sources": ["source"],
        }
    ]
    plan = {
        "version": 1,
        "id": "authored",
        "actor": "actor",
        "project": "project",
        "baseline": "sample",
        "decisions": ["decision"],
        "knowledge": ["method"],
        "stages": [
            {
                "id": "motion",
                "name": "Fixture stage from accepted input",
                "phase": "production",
                "kind": "sprite",
                "contract": "contract",
                "needs": ["member.output"],
                "criteria": criteria,
                "selection": {"path": "plar.txt", "asset": "fixture.member", "requirements_hash": selected["requirements_hash"]},
            }
        ],
        "delivery": {
            "name": "Fixture delivery",
            "members": ["output", "motion"],
            "destinations": ["destination"],
            "criteria": [{**criteria[0], "domain": "continuity"}],
        },
    }
    packet = {
        "version": 1,
        "inputs": {
            "member.output": {
                "candidate": "member",
                "sha256": records["member"]["fields"]["dg"],
            }
        },
        "request": {
            "provider": "fictional-fixture",
            "tool": "animate_fixture",
            "arguments": {"description": "fixture"},
            "schema": {
                "type": "object",
                "properties": {"description": {"type": "string"}},
                "required": ["description"],
                "additionalProperties": False,
            },
            "discovery": {
                "source": "fixture tools/list",
                "observed_at": "2026-09-11T12:00:00+00:00",
                "evidence": {"fixture": True},
            },
            "authorization": {
                "scope": "Local distribution probe",
                "evidence": {"fixture": True},
            },
        },
    }
    plan_path = project / "authored-plan.json"
    packet_path = project / "authored-request.json"
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    packet_path.write_text(json.dumps(packet), encoding="utf-8")
    report = invoke(["family", state, "--root", root])
    authored = invoke(
        [
            "production-plan",
            folder,
            str(plan_path),
            "--expect",
            report["hash"],
            "--root",
            root,
        ]
    )
    prepared = invoke(
        [
            "stage-prepare",
            folder,
            "authored.plan",
            "motion",
            "authored.job",
            str(packet_path),
            "--expect",
            authored["hash"],
            "--root",
            root,
        ]
    )
    replay = invoke(
        [
            "stage-prepare",
            folder,
            "authored.plan",
            "motion",
            "authored.job",
            str(packet_path),
            "--expect",
            prepared["hash"],
            "--root",
            root,
        ]
    )
    review = invoke([
        "request-review", prepared["request_review"]["packet"],
        "--plan", prepared["request_review"]["plan"],
        "--job", prepared["request_review"]["job"], "--root", root,
    ])
    after = {r["id"]: r for r in invoke(["decode", state])["records"]}
    focused = invoke(["context", state, "authored.plan", "--view", "authoring", "--root", root])
    successor = deepcopy(plan)
    successor["id"] = "authored-successor"
    selected = invoke(["plar", "read", "--asset", "fixture.member", "--root", root])
    successor["stages"][0]["selection"]["replaces"] = selected["asset"]["production"]
    successor_path = project / "successor-plan.json"
    successor_path.write_text(json.dumps(successor), encoding="utf-8")
    rejected_pending = False
    try:
        invoke(["production-plan", folder, str(successor_path), "--expect", prepared["hash"], "--root", root])
    except RuntimeError as error:
        rejected_pending = "job_pending" in str(error)
    abandonment = project / "abandonment.json"
    abandonment.write_text(json.dumps({"reason": "Synthetic prepared-only abandonment, no provider failure or execution"}), encoding="utf-8")
    resolved = invoke(["job-observe", folder, "authored.job", "failed", str(abandonment), "--expect", prepared["hash"], "--root", root])
    predecessor_records = {r["id"]: r for r in invoke(["decode", state])["records"]}
    revised = invoke(["production-plan", folder, str(successor_path), "--expect", resolved["hash"], "--root", root])
    current_records = {r["id"]: r for r in invoke(["decode", state])["records"]}
    change_export = invoke(["request-review", ".pixl/state.px", "--plan", "authored-successor.plan",
                            "--against-plan", "authored.plan", "--view", "changes", "--root", root,
                            "--result-path", "successor-changes.json"])
    changes = json.loads((project / change_export["result_path"]).read_bytes())
    checks = {
        "historical_records_unchanged": all(after[k] == v for k, v in records.items()),
        "exact_input_bound": {"$ref": "member"}
        in after["authored.motion.task"]["fields"]["ip"],
        "prepared_only": after["authored.job"]["fields"]["si"]
        == {"$symbol": "prepared"},
        "no_acceptance": after["authored.motion.task"]["fields"]["ca"] == [],
        "same_job_reused": replay["already_prepared"]
        and replay["hash"] == prepared["hash"],
        "no_remote_execution": not authored["remote_executed"]
        and not prepared["remote_executed"],
        "exact_member_and_collective_handoff": review["criterion_ids"]
        == ["authored.motion.q.shape", "authored.delivery.q.shape"],
        "exact_request_for_caller": review["request"]["request"]["arguments"]
        == packet["request"]["arguments"],
        "review_does_not_grant_consistency": review["consistent"] is None,
        "focused_authoring_criteria": {r["id"] for r in focused["criteria"]}
        == {"authored.motion.q.shape", "authored.delivery.q.shape"},
        "focused_authoring_pending_job": focused["jobs"][0]["id"] == "authored.job"
        and "request" not in focused["jobs"][0],
        "focused_authoring_source_retrieval": focused["sources"][0]["retrieve"]["tool"] == "pixl_source",
        "successor_refused_pending_intent": rejected_pending,
        "successor_explicitly_relinked": revised["allocation"][0]["status"] == "revised"
        and revised["allocation"][0]["previous_production"] == selected["asset"]["production"],
        "successor_preserved_predecessor": all(current_records[k] == v for k, v in predecessor_records.items()),
        "successor_has_no_candidate_or_job": current_records["authored-successor.motion.task"]["fields"]["ca"] == []
        and len([r for r in current_records.values() if r["kind"] == "J"]) == 1,
        "focused_destination_choice": "destination" in {r["id"] for r in focused["choices"]},
        "focused_choice_discovery": "other_intake" in focused["choice_scope"],
        "successor_changes_exact_index": len(changes["criterion_index"]["before"]) == len(changes["criterion_index"]["after"]) == 2,
        "successor_changes_no_inherited_acceptance": changes["consistent"] is None
        and bool(changes["review_attention"]["after"]["outputs"][0]["requires_review"]),
        "production_hash_domain": prepared["hash_domains"]["hash"] == "canonical_state_sha256",
        "selected_queue_hash_domains": selected["hash_domains"]["hash"] == "file_sha256"
        and selected["hash_domains"]["requirements_hash"] == "selected_requirements_sha256",
        "comparison_hash_domains": changes["hash_domains"]["comparison_sha256"] == "comparison_report_sha256"
        and changes["hash_domains"]["after.review_scope_sha256"] == "review_scope_sha256",
        "export_hash_domain": change_export["hash_domains"]["result_sha256"] == "file_sha256",
    }
    if not all(checks.values()):
        raise RuntimeError(
            "production authoring distribution probe failed: " + str(checks)
        )
    return {
        "status": "pass",
        "checks": checks,
        "scope": "Connected authoring and same-request recovery on retained synthetic fixture; no provider or artistic outcome.",
    }
