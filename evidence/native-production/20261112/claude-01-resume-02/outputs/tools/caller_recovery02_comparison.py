"""Caller recovery-02: current-selection comparison and stale-handoff correction record.
Run from the consumer root with the assignment Python using -I; argv[1] = current UTC clock.
Writes work/native-production/recovery-02/CALLER-SELECTION-COMPARISON.json (new path).
"""
import json, hashlib, sys
from pathlib import Path

now = sys.argv[1]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def ref(p, role):
    return {"path": p, "sha256": sha(p), "role": role}

snap_path = '.pixl/assets/robot.directions/plans/acf329804ba043b77d690c7a84bd0c8900b79dabd811bba9a92e0fb2b2b91363.json'
snap = json.loads(Path(snap_path).read_text(encoding='utf-8'))
old_sel = snap['input']['selection']
cur = json.loads(Path('production-plar.txt').read_text(encoding='utf-8'))
cur_asset = [a for a in cur['assets'] if a['id'] == 'robot.directions'][0]
cur_dep = [a for a in cur['assets'] if a['id'] == 'robot.base'][0]
old_asset = old_sel['asset']
old_dep = old_sel['dependencies'][0]

identity_keys = ['id', 'kind', 'purpose', 'consumers', 'requirements', 'delivery', 'depends_on', 'questions', 'existing']
dep_identity_keys = ['id', 'kind', 'purpose', 'consumers', 'requirements', 'references', 'delivery', 'depends_on', 'questions', 'existing']
asset_delta = {k: {"old": old_asset.get(k), "current": cur_asset.get(k)} for k in identity_keys if old_asset.get(k) != cur_asset.get(k)}
dep_delta = {k: {"old": old_dep.get(k), "current": cur_dep.get(k)} for k in dep_identity_keys if old_dep.get(k) != cur_dep.get(k)}
src_equal = sorted((s['path'], s['sha256']) for s in old_sel['sources']) == sorted((s['path'], s['sha256']) for s in cur['sources'])
existing_file_check = [{"path": e['path'], "declared_role": e['role'], "actual_sha256": sha(e['path']), "role_hash_matches_file": sha(e['path']) in e['role']} for e in cur_asset['existing']]

doc = {
    "version": 1,
    "kind": "caller recovery-02 comparison: current focused PLAR selection versus the retained sample-generation selection snapshot, plus the stale-handoff acceptance error",
    "written_at_utc": now,
    "reviewer": "caller (Claude Code main session), persisted parent session 9d0f792b-9ac2-42e1-8131-5861ce4b1dc5",
    "native_child": "aeb8fdd3833c62981 (pixl:pixl), same child; no replacement",
    "runtime": {"note": "Explicit runtime upgrade: local MCP and plugin registration now point to the corrected kit copy; the original installed pixl package is untouched. pixl_readiness in this session reports the reporter module under work/native-production/runtime-recovery-kit (bundle manifest verified, 205 files, sha256 5dc8af04...).", "transition_record": ref("work/native-production/recovery-02/runtime-recovery.json", "source/kit transition record"), "kit_root": "work/native-production/runtime-recovery-kit", "old_kit_root": "installed pixl (unchanged)", "changed_files_per_transition_record": ["bundle-manifest.json", "resources/evidence/art-methods/poc-report.json", "resources/examples/atelier/measurement.json", "resources/examples/atelier/project.px", "resources/knowledge/library.px", "resources/pixl/plar_workflow.py", "resources/spec/family-delivery.md", "runtime/pixl/plar_workflow.py"]},
    "acceptance_error_acknowledged": {
        "what": "The earlier SPECIALIST-RESULT.json (b2b0f242...) and CALLER-RESULT.json (06000bb0...) both claimed status 'delivered' while the public handoff d864d860... and the focused PLAR read reported selection_current=false, next=review_contract, delivery_observed=false and delivery=null. The caller treated that as a harmless future-revision note. That was a reasoning error: the current public handoff had not accepted the delivery, so 'delivered' was not supported by the public state.",
        "prior_reports_preserved": [ref("work/native-production/recovery-02/prior-SPECIALIST-RESULT.json", "byte-for-byte copy of the prior specialist result"), ref("work/native-production/recovery-02/prior-CALLER-RESULT.json", "byte-for-byte copy of the prior caller result")],
        "prior_handoff_preserved": ref(".pixl/handoffs/d864d8602898fda7e93819b65f7160e77d6e6f594d4c852057ab232c368c7970.json", "prior public handoff, unchanged"),
        "not_rewritten": "The earlier conditional pre-dispatch decision (~08:25Z) and the post-dispatch packet-02 reread (~08:45Z) remain as recorded; this recovery does not relabel the reread as pre-dispatch. The timestamp-label defects remain disclosed in caller-clock-clarification-and-recovery.json."
    },
    "current_public_state_read_this_session": {"plar_file_sha256": sha('production-plar.txt'), "requirements_hash": "e3918fbaa7fcedf4be73603cd83448c4bde6f043a58f45f16a39417372a142f7", "state_hash": "ceb0b61ea85dc3c03f1548a66198e1c7c992271ce9e974665872c2b377f64cf7", "revision": 40, "selection_current": False, "selection_bindings": [], "next_action": "review_contract", "delivery": None, "pending_jobs": [], "task": "robot-directions-family.delivery.task", "task_state": "done"},
    "selection_snapshot_compared": ref(snap_path, "retained pixl.plar.selection/1 snapshot of the sample generation r.acf329804ba043b7 (requirements_hash de02...)"),
    "selection_delta": {
        "asset_identity_fields_compared": identity_keys,
        "asset_delta": asset_delta,
        "dependency_identity_fields_compared": dep_identity_keys,
        "dependency_delta": dep_delta,
        "source_digests_equal": src_equal,
        "project_equal": old_sel['project'] == cur['project'],
        "mutable_fields_excluded_by_snapshot": ["status", "next", "evidence", "production"],
        "caller_finding": "The only selected-identity change is existing: [] -> four delivered file entries. Requirements, delivery contract (assets/robot, three checks), consumers (spriteFor), purpose, depends_on, questions and all four source digests are unchanged. The dependency robot.base is unchanged in every identity field. This matches the stated input delta exactly."
    },
    "existing_rows_check": existing_file_check,
    "existing_rows_disposition": "Keep the four existing rows: each path exists, each actual sha256 appears in its role text, and the roles are truthful (reused / generated / generated / edited). Do not restore [] merely to make the old requirements_hash match; the current requirements_hash e3918fba... is the one a fresh selection binding must carry.",
    "gap_diagnosis": [
        "robot-directions-family.delivery.task has inputs [robot-directions-family.plan, candidate.south] and no report-X carrying mt.binding pixl.plar.selection/1, so the runtime cannot derive selection currency for the linked task; selection_bindings is [] and selection_current is false.",
        "The only tagged selections (r.acf329804ba043b7.selection, selection) belong to the sample tasks and were taken at requirements_hash de02..., which no longer matches e391... because existing changed.",
        "Because the linked task has no current selection, the derived continuation stays review_contract and delivery stays null/unobserved, even though the family manifest, members and destinations are intact."
    ],
    "correction_plan_for_the_child": [
        "1. Retain the actual current focused selection JSON (fresh pixl_plar_read of production-plar.txt / robot.directions, or the equivalent plar selection export) as an immutable file under the store, with its real sha256 as dg.",
        "2. Append a report-X whose ur is that retained file, dg its real sha256, kd report, mt {binding: 'pixl.plar.selection/1', plar_path: 'production-plar.txt', asset_id: 'robot.directions', requirements_hash: 'e3918fbaa7fcedf4be73603cd83448c4bde6f043a58f45f16a39417372a142f7'} (verify the exact field syntax against the existing @r.acf329804ba043b7.selection record and PIXL-2 registry; do not guess).",
        "3. Guarded pixl_commit (expect = current canonical state hash) that adds the Ref to robot-directions-family.delivery.task.ip and reopens that task in the same commit (st from done back to the public reopen state the spec allows); no other record changes; keep manifest.01 and its verdicts.",
        "4. Complete the task again through the public operation (pixl_task_complete with candidate robot-directions-family.delivery.manifest.01) if the existing verdicts are still current for that candidate; if the runtime says a current review is required, perform an honest review against the retained renderer evidence (render-01, unchanged source and pixels) and retain it; no new rendering is required solely for a count.",
        "5. Fresh pixl_plar_read and pixl_plar_handoff (view caller) must show selection_current=true, next=delivered, delivery observed and complete with four exact members under assets/robot, no pending jobs. If any remain false, diagnose the actual gap instead of declaring completion.",
        "6. Publish the corrected SPECIALIST-RESULT.json at the current alias only after the prior bytes are retained (already done at recovery-02/prior-SPECIALIST-RESULT.json). Keep all packets, views, handoffs, failed grades, raw west, jobs and timestamp clarifications."
    ],
    "forbidden": ["any paid or provider-mutating call", "regenerating or re-editing art", "editing or deleting earlier receipts, reviews, packets, handoffs", "forging a digest, verdict, job, acceptance or timestamp", "relabelling the edited west as generated"],
    "result": "comparison saved; correction authorized within the existing CF-10 scope (local state and PLAR operations only)",
    "next_action": "Send this comparison to child aeb8fdd3833c62981; wait for its corrected result; consume the new handoff; write corrected CALLER-RESULT.json."
}
out = Path('work/native-production/recovery-02/CALLER-SELECTION-COMPARISON.json')
out.write_text(json.dumps(doc, indent=2), encoding='utf-8')
print(sha(out))
print(json.dumps({"asset_delta_keys": list(asset_delta), "dep_delta_keys": list(dep_delta), "src_equal": src_equal}))
