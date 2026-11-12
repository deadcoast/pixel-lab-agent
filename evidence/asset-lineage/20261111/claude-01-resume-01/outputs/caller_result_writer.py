"""Assemble work/asset-lineage/CALLER-RESULT.json from final bytes on disk.

usage: python -I caller_result_writer.py <consumer_root>
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.abspath(sys.argv[1])
AL = "work/asset-lineage"


def p(rel):
    return os.path.join(ROOT, rel.replace("/", os.sep))


def sha(rel):
    h = hashlib.sha256()
    with open(p(rel), "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ref(rel, **extra):
    r = {"path": rel, "sha256": sha(rel)}
    r.update(extra)
    return r


def load(rel):
    with open(p(rel), encoding="utf-8") as fh:
        return json.load(fh)


fixture = load("work/asset-lineage-inputs/fixture.json")
spec = load(f"{AL}/SPECIALIST-RESULT.json")
comparison = load(f"{AL}/COMPARISON.json")
checks = load(f"{AL}/caller-independent-checks.json")
oc = load(f"{AL}/caller-original-context.json")
rc = load(f"{AL}/caller-reused-context.json")

operations = {}
for key, op in spec["operations"].items():
    operations[key] = {
        "tool": op["tool"],
        "route_reported_by_specialist": op.get("route"),
        "arguments": op.get("arguments"),
        "result": ref(op["result"]["path"]),
        "specialist_reported_sha256": op["result"]["sha256"],
        "caller_rehash_matches": sha(op["result"]["path"]) == op["result"]["sha256"],
    }
    if "mcp_attempt" in op:
        operations[key]["mcp_result_path_rejected"] = op["mcp_attempt"]["error"]

caller_operations = {}
for key, spec_read in fixture["caller_reads"].items():
    caller_operations[key] = {
        "tool": spec_read["tool"],
        "route": "mcp pixl-local with result_path (caller session, performed before the specialist's reports existed)",
        "arguments": {**spec_read["arguments"], "result_path": spec_read["result_path"]},
        "result": ref(spec_read["result_path"]),
        "byte_identical_to_specialist_read": sha(spec_read["result_path"]) == sha(fixture["reads"][key]["result_path"]),
    }
caller_operations["original_context"]["mcp_receipt"] = {
    "state_hash": "88d77c62b47eb8fef5d35015973f67b0f38731cb04e54430efa36aec4b898d64",
    "revision": 108,
    "candidate": "live.family.candidate",
    "task_status": "done",
    "result_bytes": 77319,
}
caller_operations["reused_context"]["mcp_receipt"] = {
    "state_hash": "88d77c62b47eb8fef5d35015973f67b0f38731cb04e54430efa36aec4b898d64",
    "revision": 108,
    "candidate": "artistic2.delivery.candidate",
    "task_status": "done",
    "result_bytes": 77440,
}

inspected_sources = [
    ref(f"{AL}/COMPARISON.json", note="read completely in the caller transcript"),
    ref(f"{AL}/SPECIALIST-RESULT.json", note="read completely in the caller transcript"),
    ref(f"{AL}/working-construction.json", note="saved pixl_source excerpt (lines 1-17); read completely; seed 21f5baca..., lossless quarter-turn permutation, patch_count 196"),
    ref(f"{AL}/ready-fixture.json", note="saved pixl_source excerpt (line 1); read completely; provider_simulated=true throughout, pixellab-test, controlled-create-0002, 127.0.0.1:4894"),
    ref(f"{AL}/caller-original-context.json", note="caller public read; members and lineage inspected programmatically"),
    ref(f"{AL}/caller-reused-context.json", note="caller public read; members and lineage inspected programmatically"),
    ref(f"{AL}/original-family.json", note="specialist read; snapshots.files and members inspected programmatically"),
    ref(f"{AL}/reused-family.json", note="specialist read; snapshots.files and members inspected programmatically"),
    ref(f"{AL}/plar-ready.json", note="specialist read (CLI stdout); production.link_status unlinked"),
    ref(f"{AL}/plar-working.json", note="specialist read (CLI stdout); continuation.delivery inspected"),
    ref(f"{AL}/plar-retry.json", note="specialist read (CLI stdout); continuation.delivery inspected"),
    ref(f"{AL}/plar-paused.json", note="specialist read (CLI stdout); continuation.delivery inspected"),
    ref("work/asset-lineage-inputs/fixture.json"),
    ref("work/live-family/working-animation-motion-01-construction.json", note="read completely (1206 lines); fixture source_evidence.working_construction"),
    ref(".pixl/assets/queue.ready/jobs/e7cc448003dc41409ef16591c3793a118859d4e9b4e5f44ff18be8ad07783922.json", note="Ready controlled-fixture journal; read completely"),
    ref(".pixl/assets/queue.ready/jobs/42e54029b82111da019824b279b53fdfb14619720362525d43bec2eb95f72389.json", note="live.working-animation-motion-01.job; argv edit source 234cbedb... = repair-01 remote_id; 196 patch_pixels"),
    ref(".pixl/assets/queue.ready/jobs/b982e1e81cc34ceef5944159c078afd4d45f7215bd93fc8452782d0f72a60226.json", note="live.working-animation-repair-01.job; edit of upload:a266e48d... (unresolved)"),
    ref(".pixl/assets/queue.ready/jobs/5ba42107ae11f29a06afd9761b418e02767f5734b477c5aa6030cf9c2887743c.json", note="live.working-seed.job; imported seed 21f5baca..."),
    ref(".pixl/assets/queue.ready/jobs/bfe185a1a7c1d8001374b117cb903da934ce8cf4820772fc2477d918c0df643a.json", note="live.working-animation-01.job (animate_image); imported 32615f3d...; not the delivered Working"),
    ref(".pixl/assets/queue.ready/jobs/f3c4ef548d11058f4103f75c5bed853ca532844892e04d5ed6c7c00dc914f339.json", note="live.retry.job; generation request; style_image upload:8be5bdc9... unresolved"),
    ref(".pixl/assets/queue.ready/jobs/4b5399fa7a514375970a792c8ef66a695058551084d087d6a88867fca963a877.json", note="live.paused-02.job; magenta-key generation; imported 16039251..."),
    ref(".pixl/assets/queue.ready/jobs/833f779f2523cb74bffb9aa6400b4176ea8e00a81ef87c4740fbd2268ef9e387.json", note="live.paused-cutout-01.job; deterministic cutout edit of job:6bf20949...; imported 80d2b823..."),
    ref(".pixl/assets/queue.ready/jobs/196ce9300b16516f1b60d362f50a83e0e1f24f841203f99f46ef4ed104d7abcd.json", note="live.paused.job; failed; no candidate"),
    ref(".pixl/assets/queue.ready/state.px", note="PX2 revision 108; file sha256 equals the canonical state_hash returned by every public read; artistic2.* X records carry mt.reuse_provenance"),
    ref(".pixl/assets/queue.ready/deliveries/78d45b4dbeef06f376356e0bcbec8f8a8b09b034f999db7903369f22beaff0f7/manifest.json", note="live.family.candidate manifest; created_at 2026-11-08T12:56:09Z"),
    ref(".pixl/assets/queue.ready/deliveries/1060114444f6c41150cb3914098f920790b29d47458af5c3ab33c43910b3c211/manifest.json", note="artistic2.delivery.candidate manifest; created_at 2026-11-10T02:57:58Z"),
    ref("work/live-family/working-strip-upload.json", note="declares upload:a266e48d... 64x16 single frame; no bytes or hash"),
    ref("work/live-family/working-animation-01-assembly.json", note="assembly of the rejected AI animation; raw frame 0 equals seed"),
    ref("work/live-family/anchor-upload.json", note="style upload 8be5bdc9... declared as assets/ready-confirmed.png fc5e43ae...; declaration only"),
    ref("work/live-family/paused-cutout-01-patches.json"),
    ref("work/artistic-revision/retained-failures.json"),
    ref("work/artistic-revision/candidate-document-plan02.json", note="artistic2.* reuse_provenance declarations as committed"),
    ref("work/live-family/working-animation-motion-01-succeeded-response.json", note="hash verified against journal citation"),
    ref("work/live-family/paused-cutout-01-succeeded-response.json", note="hash verified against journal citation"),
    ref("work/live-family/retry-submitted-response.json", note="hash verified against journal citation"),
    ref("work/live-family/retry-succeeded-response.json", note="hash verified against journal citation"),
    ref("work/live-family/working-seed-download.png", note="hash equals seed artifact 21f5baca..."),
    ref("work/live-family/working-animation-motion-01.png", note="hash equals delivered Working cf101610..."),
    ref("work/live-family/paused-cutout-01.png", note="hash equals delivered Paused 80d2b823..."),
    ref("work/live-family/retry-download.png", note="hash equals delivered Retry 0fb0ab5e..."),
    ref("work/live-family/paused-02-opaque.png", note="hash equals live.paused-02 artifact 16039251..."),
    ref("assets/ready-confirmed.png"),
    ref("assets/working.png"),
    ref("assets/error-retry.png"),
    ref("assets/paused.png"),
    ref("ASSET-LINEAGE.md"),
    ref("AGENTS.md"),
    ref("CURRENT-HANDOFF.md"),
]

check_index = {c["check"]: c for c in checks["checks"]}
prod = check_index["original_bytes_unchanged_outside_work_asset_lineage"]["detail"]
added = check_index["no_files_added_outside_work_asset_lineage"]["detail"]

doc = {
    "version": 1,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "assignment": "ASSET-LINEAGE.md caller section (NF-08 read-only retained asset-lineage evaluation)",
    "host": {"product": "Claude Code", "calling_role": "parent session", "session_id": "93202414-9a89-4779-8dce-8b28fd59da31"},
    "consumer_root": ROOT,
    "native_child": {
        "agent_type": "pixl:pixl",
        "agent_id": "ab752bfbbdae1c158",
        "same_child_across_recovery": True,
        "invocations": [
            {
                "kind": "Agent spawn",
                "outcome": "performed the ten reads and evidence inspection; the host stopped the child before COMPARISON.json and SPECIALIST-RESULT.json were written; the parent turn ended while waiting; exit code zero did not establish completion",
            },
            {
                "kind": "SendMessage resume of the same agent_id",
                "outcome": "child finished from its retained reads; wrote COMPARISON.json and SPECIALIST-RESULT.json; completion notification received by the parent",
                "child_reported_tool_uses_in_resumed_segment": 2,
                "child_reported_duration_ms": 279493,
            },
        ],
        "no_replacement_child": True,
    },
    "recovery": {
        "previous_parent_turn": "ended while waiting for the child; the ten public read exports and the two caller context exports already existed",
        "ten_reads_rerun": False,
        "caller_reads_rerun": False,
        "caller_reads_reused_because": "state.px file sha256 and the canonical state_hash at every read remain 88d77c62...; caller context files are byte-identical to the specialist's context files",
        "transient_files_disclosed_by_child": ["work/asset-lineage/_generate_reports.py (created and removed by the child; not present now)"],
        "transient_file_absent_now": not os.path.exists(p(f"{AL}/_generate_reports.py")),
    },
    "specialist_result": ref(f"{AL}/SPECIALIST-RESULT.json"),
    "comparison": ref(f"{AL}/COMPARISON.json"),
    "operations": operations,
    "caller_operations": caller_operations,
    "inspected_sources": inspected_sources,
    "independent_checks": {
        "report": ref(f"{AL}/caller-independent-checks.json"),
        "script": ref(f"{AL}/caller_verify.py"),
        "baseline": ref(f"{AL}/caller-baseline-hashes.json", note="sha256 of all 4440 files outside work/asset-lineage, taken before the child was spawned"),
        "baseline_script": ref(f"{AL}/caller_snapshot.py"),
        "summary": {c["check"]: c["status"] for c in checks["checks"]},
        "key_claims_agreement": check_index["key_claims_agree_with_caller_independent_evidence_reading"]["detail"],
        "cross_surface_identity_agreement": check_index["member_identities_and_hashes_agree_across_all_public_surfaces_and_comparison"]["detail"],
        "state_hashes": check_index["state_hash_agrees_across_public_surfaces_and_state_file"]["detail"],
        "working_chain": check_index["working_deterministic_construction_chain_consistent"]["detail"],
        "journal_import_evidence": check_index["job_journals_content_addressed_and_import_hashes_as_expected"]["detail"],
        "specialist_refs": {
            "specialist_result": check_index["specialist_result_file_refs_resolve_to_actual_bytes"]["detail"],
            "comparison": check_index["comparison_file_refs_resolve_to_actual_bytes"]["detail"],
        },
    },
    "caller_reading_of_key_claims": {
        "ready_is_controlled_fixture": True,
        "ready_is_authenticated_provider_generation": False,
        "working_has_retained_deterministic_construction_record": True,
        "working_final_is_provider_generated_animation": False,
        "paused_has_recorded_generation_and_deterministic_cutout": True,
        "retry_has_recorded_generation_request": True,
        "same_bytes_proves_reuse_direction": False,
        "remote_execution_authenticated": False,
        "basis": "Caller-read journals, construction record, state reuse_provenance declarations and manifests listed in inspected_sources; agrees with COMPARISON.key_claims on all eight.",
    },
    "production_unchanged": {
        "original_bytes_unchanged": not prod["changed"] and not prod["removed"],
        "baseline_files": prod["baseline_files"],
        "current_files": prod["current_files"],
        "changed": prod["changed"],
        "removed": prod["removed"],
        "added_outside_work_asset_lineage": added["added_python_bytecode_caches_under_installed_kit_runtime"],
        "added_other": added["added_other"],
        "state_px_sha256_now": sha(".pixl/assets/queue.ready/state.px"),
        "state_px_sha256_baseline": load(f"{AL}/caller-baseline-hashes.json")["files"][".pixl/assets/queue.ready/state.px"]["sha256"],
        "authoring_plar_sha256_now": sha("authoring-plar.txt"),
        "plar_txt_sha256_now": sha("plar.txt"),
        "assessment": "Art, source, state, PLAR files, history and kit source bytes are unchanged (0 changed, 0 removed of 4440 baseline files). 22 Python bytecode caches were created under installed pixl/runtime/pixl/__pycache__ by the interpreter when the child ran the kit CLI for the PLAR and source reads; they are regenerable interpreter artifacts, were disclosed by the child, and were left in place rather than deleted. Strictly, the installed kit directory is therefore not byte-identical to the baseline file set.",
    },
    "new_provider_execution": False,
    "acceptance_created": False,
    "scope": {
        "performed": "Read-only lineage qualification of live.family.candidate versus artistic2.delivery.candidate through public reads, cited journals and retained records; independent caller cross-check of identities, hashes and key claims.",
        "not_performed": "No provider call, generation, rendering, review, verdict, nomination, task completion, handoff, acceptance, package installation, settings or memory edit. No art or destination quality judgment.",
        "open": "M1/M2 and broader M3 remain open; CF-10 follows this bounded lineage increment.",
    },
    "limitations": [
        "Provider observations are caller-saved host response files; hashes match the journals, but no remote execution is authenticated and no provider was contacted.",
        "Unknown links remain unknown: style upload 8be5bdc9-da49-43b7-8ef3-307a81defeba (declared in anchor-upload.json as the Ready PNG, declaration only) and edit base upload a266e48d-e9e5-43ad-ba45-08a6685ebfd7 (declared 64x16 single frame, no retained bytes or hash). The exact pixel parent of the final Working edit is therefore declared, not byte-verified.",
        "Reuse direction live.* -> artistic2.* rests on retained revision order, manifest timestamps and declared reuse_provenance records; byte equality is symmetric and proves nothing about direction.",
        "The Ready baseline is a controlled pixellab-test fixture; how its 16x16 pixels were authored is not recorded anywhere in the retained lineage.",
        "Lineage projections are bounded (truncated=true); the family-level projection lists only the Ready job and member detail came from the family, PLAR and journal reads.",
        "pixl_plar_read does not advertise result_path in this session's MCP schema; the child captured those four reads as complete CLI stdout. pixl_source has no result_path; the child captured the two excerpts as CLI stdout and reported matching MCP returns. The caller did not repeat those CLI reads.",
        "The child's pixel measurements (quarter-turn equality on visible pixels; cutout RGB equality) were not independently re-executed by the caller; the caller verified the surrounding records, hashes and argv consistency instead.",
        "The first child attempt was stopped by the host; the resumed child reported that its first report write failed in the shell with ENAMETOOLONG before touching disk and that no reads were re-run. The caller verified the ten read files' hashes are unchanged since the first listing.",
        "22 Python bytecode cache files now exist under installed pixl/runtime/pixl/__pycache__ that were not in the baseline; see production_unchanged.",
        "This report interprets retained sources; it creates no provenance, acceptance or verdict.",
    ],
    "next_action": "No production action follows. Hand this bounded lineage report to CF-10. If a byte-identical kit directory is required, the 22 listed __pycache__ files may be removed by the owner; nothing else needs restoring. M1/M2 and broader M3 remain open.",
}

out = f"{AL}/CALLER-RESULT.json"
with open(p(out), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(doc, fh, indent=2)
print(json.dumps({"written": out, "sha256": sha(out), "all_checks": doc["independent_checks"]["summary"]}))
