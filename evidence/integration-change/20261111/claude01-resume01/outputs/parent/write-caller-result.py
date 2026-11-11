"""Parent helper: assemble CALLER-RESULT.json from files already on disk.

Computes exact sha256 references; adds no observations beyond those the parent
recorded in the session. Run with: python -I write-caller-result.py (cwd = project root).
"""
import datetime
import hashlib
import json
import pathlib

root = pathlib.Path('.')


def sha(p):
    return hashlib.sha256((root / p).read_bytes()).hexdigest()


def ref(p, **kw):
    return {"path": p, "sha256": sha(p), **kw}


def load(p):
    return json.loads((root / p).read_text(encoding='utf-8'))


def hashmap(p):
    out = {}
    for line in (root / p).read_text(encoding='utf-8').splitlines():
        if ' *' in line:
            h, f = line.split(' *', 1)
            out[f] = h
    return out


spec = load('work/integration-change/SPECIALIST-RESULT.json')
base = hashmap('work/integration-change/parent/baseline-hashes.txt')
after = hashmap('work/integration-change/parent/after-hashes.txt')
changed = [k for k in base if k in after and base[k] != after[k]]
missing = [k for k in base if k not in after]
fixture = load('work/integration-inputs/fixture.json')
art = {p: {"fixture": h, "current": sha(p), "match": sha(p) == h} for p, h in fixture['exact_art'].items()}

OLD_JOB = '.pixl/assets/queue.working/jobs/ec1d22454640957119f527dcd5657edc79064f34d865783668963b3463f90571.json'
OLD_PLAN = '.pixl/assets/queue.working/plans/089b5e8f5fee113cf548c40eb13e123d9a1cfdd15c93b2cbc69c9e8a30e9593a.json'
PKG = '.pixl/assets/queue.working/deliveries/873d6917ed6e80f3302b282b4cb9a84686f3c8e9234497f8151b9997d17f1ead'
WORKING = 'cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc'
STATE_FINAL = 'ad0cfa6d9b512a3a11ace7cdf99dd5613e6ffa5336e95cd436452d6b4785ebb6'
REQ_OLD = '12cb410ef6f24ed585755beede2c470eb2d3b32574596b11457394c6c0a68eee'
REQ_NEW = 'dc4292427296bdb382c9b5fcd6a8fc0c7678ad214126654fdf962942223b2968'
PLAR_BASE = '8ddece433eef4a42ac57db4ea77c46e1e99962d4de969c68b5ca55c9e65b04ad'

first_attempt_files = [
    'work/integration-change/parent/parent-refresh.json',
    'work/integration-change/parent/parent-refresh.stderr.txt',
    'work/integration-change/parent/parent-refresh.command.txt',
    'work/integration-change/parent/parent-acceptance.stderr.txt',
    'work/integration-change/parent/parent-acceptance.command.txt',
    'work/integration-change/parent/parent-family.stderr.txt',
    'work/integration-change/parent/parent-jobs.stderr.txt',
    'work/integration-change/parent/parent-validate.stderr.txt',
    'work/integration-change/parent/parent-workflow.stderr.txt',
]

result = {
    "version": 1,
    "role": "parent (same CF-07/NF-06 parent session; continuation after harness time limit consuming an already completed child)",
    "written_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "root": "C:/Users/ryanf/AppData/Local/Temp/pixl readiness claude clean j9gn621r/consumer",
    "native_child": {
        "subagent_type": "pixl:pixl",
        "agent_id": "a9621eef304b33895",
        "canonical_path": "installed pixl/skills/pixl/SKILL.md",
        "skills_loaded": ["pixl:pixl", "pixl:plar"],
        "note": "One actual named pixl:pixl specialist completed the whole assignment in the original session; it was not re-spawned or resumed across processes.",
    },
    "specialist_result": ref('work/integration-change/SPECIALIST-RESULT.json', references_verified=59, reference_mismatches=0, status=spec['status'], steps_completed=spec['steps_completed']),
    "parent_refresh": ref('work/integration-change/parent/parent-refresh-r2.json', command_log='work/integration-change/parent/parent-commands-r2.txt', plar_hash='481450298f204ac146b2f4cd02565a947f8e23a006bae855affa2a477002c555', since=PLAR_BASE, changed_sources=["timing-authority", "working-timing"], affected_assets=["queue.working"], unaffected_assets=["queue.paused", "queue.ready", "queue.retry", "queue.start"]),
    "parent_selections": ref('work/integration-change/parent/parent-selections.json', assets=["queue.ready", "queue.working", "queue.retry", "queue.start", "queue.paused"], requirements_changed_only=["queue.working"]),
    "parent_acceptance": ref('work/integration-change/parent/parent-acceptance-r2.json', candidate="delivery-150.package", task="delivery-150.delivery.task", task_status="done", nominated=True, all_required_pass=True, task_complete=True, state_hash=STATE_FINAL, revision=15, criteria=[["delivery-150.delivery.q.bytes", "local", "pass"], ["delivery-150.delivery.q.continuity", "visual", "pass"], ["delivery-150.delivery.q.destination", "live", "pass"]]),
    "handoff": ref('work/integration-change/handoff.json', saved_handoff=ref('.pixl/handoffs/ce45854f3036f83239a9fb1e02375c59dab031e74eb6d3b60aa8e43c357aa238.json'), view="caller", next="delivered"),
    "additional_parent_reports": {
        "family": ref('work/integration-change/parent/parent-family-r2.json'),
        "jobs": ref('work/integration-change/parent/parent-jobs-r2.json', remote_executed=False, jobs=[{"id": "first_request", "state": "failed", "remote_id": None, "events": ["failed"]}, {"id": "r.5b1bc38638b68ed8.request", "state": "failed", "remote_id": None, "events": ["failed"]}]),
        "validate": ref('work/integration-change/parent/parent-validate-r2.json', hash=STATE_FINAL, revision=15),
        "workflow": ref('work/integration-change/parent/parent-workflow-r2.json', tasks={"delivery-150.delivery.task": "done", "r.5b1bc38638b68ed8.task": "done", "task": "open (blocker: plar_selection: current consumer requirements differ)"}),
        "commands": ref('work/integration-change/parent/parent-commands-r2.txt'),
        "baseline_hashes": ref('work/integration-change/parent/baseline-hashes.txt'),
        "after_hashes": ref('work/integration-change/parent/after-hashes.txt'),
        "helper": ref('work/integration-change/parent/write-caller-result.py'),
        "first_attempt_failed": {
            "note": "First parent CLI batch placed --root before the subcommand; argparse exit 2 with empty stdout. Files retained unchanged, retried under fresh -r2 names.",
            "files": [ref(p) for p in first_attempt_files],
        },
    },
    "independent_checks": {
        "five_original_art_hashes": {"all_match_fixture": all(v["match"] for v in art.values()), "detail": art},
        "unchanged_source_identities": {
            "src/queue.ts": sha('src/queue.ts') == "de271234087741c37ad6892a8802768ffcc38b440a0ae97ae66d8700ab0d1e08",
            "src/queue-view.ts": sha('src/queue-view.ts') == "4d6ee92e40374d4dd4c6a49a3a20a6caf34e7f2d61a32a230c8ecf54691b5c49",
            "src/queue-view-integration.ts": sha('src/queue-view-integration.ts') == "8058e2bca9cab1d0daaf0dd453ec288595357e54aed55aaa1d64da42677eca96",
            "BRIEF.md": sha('BRIEF.md') == "aebe00949f3a9510a44f6f554b8fc97e53476d7658a4bb29419db85b417f02ab",
            "SOURCE-MAP.md": sha('SOURCE-MAP.md') == "1ff4573dfb255c870171dad9ae09622e29b988200f144b0a88f7fcba430d2081",
            "plar.txt": sha('plar.txt') == "a462ecf3b6b45c0382d3483b0f4f6912a9d0bd1d68e75253143faa1423837344",
            "renderer-integration": {f"renderer-integration/{n}": sha(f'renderer-integration/{n}') for n in ("capture.mjs", "check.py", "index.html", "observation.py", "server.mjs", "view.mjs")},
            "controlled_changes_present": {"src/working-timing.ts": sha('src/working-timing.ts'), "WORKING-TIMING-AMENDMENT.md": sha('WORKING-TIMING-AMENDMENT.md')},
            "all_19_plar_sources_binding_current": True,
        },
        "baseline_vs_after_diff": {
            "changed_existing_files": changed,
            "missing_files": missing,
            "expected_changed_only": changed == ['integration-plar.txt', '.pixl/assets/queue.working/state.px'] and not missing,
            "note": "Every other pre-existing file (five art files, all src, plar.txt, brief, amendment, work/integration-inputs/*, old history .px snapshots, old job journal, old plan snapshot, retained inputs) is byte-identical; all other store additions are new files.",
        },
        "selected_identity_changed_only_for_working": {
            "result": True,
            "queue.working": {"old_prepared_requirements_hash": REQ_OLD, "current_requirements_hash": REQ_NEW},
            "other_four_requirements_hashes_identical_to_baseline_copy_read": True,
            "gap": "A focused read of the retained baseline PLAR byte copy now reports Working as fea38210..., not the fixture's 12cb410e..., because the two changed sources are already at 150 ms on disk and that read shows them as binding 'changed'. The original 12cb410e... digest is preserved in prepared-100.json and in the retained first_request selection_bindings (plan snapshot 089b5e8f..., unchanged bytes). The pre-change digest cannot be recomputed without restoring the 100 ms sources, which is out of scope.",
        },
        "original_prepared_intent_and_history_retained": {
            "old_job_journal_unchanged": after.get(OLD_JOB) == base.get(OLD_JOB),
            "old_plan_snapshot_unchanged": after.get(OLD_PLAN) == base.get(OLD_PLAN),
            "old_history_snapshots_unchanged": all(after.get(k) == base.get(k) for k in base if '/history/' in k),
            "old_task_still_open_with_plar_selection_blocker": True,
            "first_request_state": "failed by explicit local abandonment (old-abandon-evidence.json: never dispatched, provider_contact false, remote_id null)",
        },
        "no_remote_id_or_provider_execution": {
            "jobs_report_remote_executed": False,
            "remote_ids": [],
            "job_events": {"first_request": ["failed"], "r.5b1bc38638b68ed8.request": ["failed"]},
            "obsolete_dispatch_refusal": "job_blocked: plar_selection: queue.working is changed (selected=True); no dispatch_request returned",
            "obsolete_completion_refusal": "plar_selection: task: current consumer requirements differ or are unavailable; stale-selection guard, not a missing-candidate refusal",
            "destination_import": {"renderer_executed": False, "state_changed": False, "automatic_acceptance": False, "files_verified": True},
        },
        "package_member_vs_served_destination": {
            "package_member": ref(f'{PKG}/files/0000.png'),
            "served_destination": ref('assets/working.png'),
            "manifest": ref(f'{PKG}/manifest.json'),
            "bundle_destinations_0000_png_sha256": WORKING,
            "render_json_served_consumer_assets_working_png": WORKING,
            "destination_report_destination_sha256": WORKING,
            "all_equal": sha(f'{PKG}/files/0000.png') == sha('assets/working.png') == WORKING,
        },
        "current_150ms_report": {
            "render_json": ref('work/integration-change/capture-delivery/render.json'),
            "display": {"cell": [16, 16], "scale": 3, "filter": "nearest", "frameMs": 150, "background": "#172336"},
            "playback": {"frameMs": 150, "frameCount": 4, "durationMs": 1875, "samples": 13, "sampled_scales": [3], "sequence_statusCell": [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0], "compact_matches_statusCell": True, "elapsed_ms": [4.8, 154.9, 304.8, 454.9, 604.8, 754.8, 904.8, 1054.8, 1204.8, 1354.8, 1504.8, 1654.8, 1804.8], "wraps_3_to_0": 3, "browser": "HeadlessChrome/157.0.0.0"},
            "renderer_check": ref('work/integration-change/renderer-check.json', status="pass", failures=0, observations=406, views=20),
            "check_command": ref('work/integration-change/renderer-check.command.txt'),
            "capture_command": ref('work/integration-change/capture-delivery.command.txt'),
            "capture_stderr": ref('work/integration-change/capture-delivery.stderr.txt', note="only a Node ExperimentalWarning about stripTypeScriptTypes"),
        },
        "parent_visual_inspection": {
            "destination_screenshot": ref('work/integration-change/capture-delivery/destination.png', observed="Opened and viewed. Dark #172336 panel; state-comparison grid with Full 1x, Full 3x, Compact 1x, Compact 3x columns for idle/running/paused/succeeded/failed; running row shows the Working segmented ring in all four cells; footer reports every mapped status asset available; no missing-asset markers."),
            "statusCell_running_1x": ref('work/integration-change/capture-delivery/view-004.png', observed="16x16 crop: small cool-blue broken ring, transparent over the panel."),
            "statusCell_running_3x": ref('work/integration-change/capture-delivery/view-005.png', observed="48x48 nearest-scaled crop: segmented ring with three stepped clusters, crisp pixel blocks, no smoothing, transparent background."),
            "compactStatus_running_1x": ref('work/integration-change/capture-delivery/view-006.png', observed="Byte-identical to the statusCell 1x crop."),
            "compactStatus_running_3x": ref('work/integration-change/capture-delivery/view-007.png', observed="Byte-identical to the statusCell 3x crop."),
            "live_3x_sample_crops": "frames 0-3 map to four distinct crop hashes (ecc4d147, b6397ee4, 5e80286d, 96995db6) repeating across three wraps in both consumers; verified by hash, individual sample crops not each opened",
            "specialist_enlargements_viewed": [
                ref('work/integration-change/views/working-sheet-8x-panel.png', note="derived evidence, not an asset: four frames read as one rotating segmented ring"),
                ref('work/integration-change/views/family-strip-8x-panel.png', note="derived evidence: check, ring-with-arrowhead retry, pause bars and the four Working frames are distinguishable by shape, not colour alone"),
            ],
            "parent_measurement": {"tool": "pixl_asset_check assets/working.png", "sha256": WORKING, "width": 64, "height": 16, "visible_pixels": 128, "visible_colors": 9, "fractional_alpha_pixels": 0, "opaque_components": 12, "visible_bbox": [3, 2, 62, 14]},
            "parent_judgment": "Consistent with the specialist's visual and live verdicts for the scoped 150 ms reuse; the parent did not add or alter any public verdict.",
        },
        "minor_discrepancies": [
            {"item": "handoff.json lists command-log.txt as f7a66253...; the current file is eb860d26... because the specialist appended the final handoff line after the handoff was saved. The SPECIALIST-RESULT.json reference (eb860d26...) matches the current bytes."},
        ],
    },
    "ids": spec['ids'],
    "hashes": {"plar_baseline": PLAR_BASE, "plar_final": sha('integration-plar.txt'), "state_initial": "24a52f9ddc15e6149ec42c7bc12011c7675970806efd7261e725ed99f0b906f0", "state_final": sha('.pixl/assets/queue.working/state.px'), "requirements_old": REQ_OLD, "requirements_new": REQ_NEW, "working_png": sha('assets/working.png')},
    "scope": "Controlled reused-art Working timing change (100 ms -> 150 ms) over the fresh prospective integration-plar.txt / .pixl/assets/queue.working state, delivered by one named pixl:pixl specialist and independently verified by the parent. No provider execution, no new art, no source/config/memory edits.",
    "limitations": [
        "Native 1x live playback remains unperformed; live loop playback was sampled at the consumer 3x scale only (13 samples, three wraps). Controlled 1x evidence is still frames only. Continuous video viewing was not performed by the parent or child; the parent viewed the screenshot, the retained still crops and per-sample crop hashes.",
        "Browser evidence is a single local headless Chrome 157 run of the isolated renderer-integration fixture.",
        "The parent's first CLI batch failed on argument order (retained); the valid public reports are the -r2 files referenced above.",
        "The fixture's old requirements hash 12cb410e... cannot be recomputed from the retained baseline PLAR copy now that the sources are at 150 ms; it is preserved only in prepared-100.json and the retained first_request binding.",
        "Acceptance is scoped to this controlled timing change and is not PixelLab-generated quality evidence. M1/M2 and broader M3 remain open; historical task 'task' remains open with its plar_selection blocker and locally failed first_request.",
        "The parent did not spawn a new child, repeat production, rewrite receipts or change acceptance.",
    ],
    "next_action": "No further action for this controlled change. If 1x live playback evidence is required, extend the renderer-integration fixture to sample 1x cells during playback and re-capture under a new reviewed request. Any new Working art needs its own reviewed request and explicit provider authorization; M1/M2 and broader M3 stay open.",
}

out = root / 'work/integration-change/CALLER-RESULT.json'
out.write_text(json.dumps(result, indent=1), encoding='utf-8')
print("CALLER-RESULT.json sha256", sha('work/integration-change/CALLER-RESULT.json'))
ic = result["independent_checks"]
print("expected_changed_only", ic["baseline_vs_after_diff"]["expected_changed_only"])
print("art all match", ic["five_original_art_hashes"]["all_match_fixture"])
print("package==served", ic["package_member_vs_served_destination"]["all_equal"])
print("history retained", ic["original_prepared_intent_and_history_retained"])
print("sources", {k: v for k, v in ic["unchanged_source_identities"].items() if isinstance(v, bool)})
