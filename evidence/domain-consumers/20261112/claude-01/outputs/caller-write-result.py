import json, os, hashlib, datetime
root = r"C:/Users/ryanf/AppData/Local/Temp/pixl readiness claude clean e69go7kd/consumer"

def sha(p):
    return hashlib.sha256(open(os.path.join(root, p), "rb").read()).hexdigest()

def ref(p, **extra):
    d = {"path": p, "sha256": sha(p)}
    d.update(extra)
    return d

T = "work/domain-consumers/terrain-01/capture/"
A = "work/domain-consumers/animation-01/capture/"
viewed = [
    ref(T + "coverage-1x.png", scale=1, what="Mixed shoreline canvas 128x128, 8x8 cells"),
    ref(T + "coverage-3x.png", scale=3, what="Mixed shoreline canvas 384x384 nearest 3x"),
    ref(T + "island-1x.png", scale=1, what="Island corners canvas 64x64, 4x4 cells"),
    ref(T + "island-3x.png", scale=3, what="Island corners canvas 192x192 nearest 3x; two green stubs visible on west shore"),
    ref(T + "coverage-1x-destination.png", scale=1, what="Full page screenshot, Mixed shoreline at 1x"),
    ref(T + "coverage-3x-destination.png", scale=3, what="Full page screenshot, Mixed shoreline at 3x"),
    ref(T + "island-1x-destination.png", scale=1, what="Full page screenshot, Island corners at 1x"),
    ref(T + "island-3x-destination.png", scale=3, what="Full page screenshot, Island corners at 3x"),
]
viewed += [ref(A + f"step-idle-1x-{i}.png", scale=1, what=f"Idle pose-{i} controlled step, 40x36 viewport; bytes identical to step-settle-1x-{i}.png") for i in range(4)]
viewed += [ref(A + f"step-idle-3x-{i}.png", scale=3, what=f"Idle pose-{i} controlled step, 120x108; bytes identical to step-settle-3x-{i}.png") for i in range(4)]
viewed += [
    ref(A + "screen-idle-1x-0.png", scale=1, what="Full page screenshot, Planted idle frame 1 of 4 at 1x (anchored context)"),
    ref(A + "screen-idle-3x-2.png", scale=3, what="Full page screenshot, Planted idle frame 3 of 4 (pose-2) at 3x; figure sits lower"),
    ref(A + "screen-settle-1x-2.png", scale=1, what="Full page screenshot, One-shot settle frame 3 of 4 (pose-2) at 1x"),
    ref(A + "screen-settle-3x-3.png", scale=3, what="Full page screenshot, One-shot settle terminal frame 4 of 4 at 3x"),
    ref(A + "live-idle-3x-4.png", scale=3, what="Live playback sample at first loop wrap (666.7 ms) back to pose-0; bytes identical to step-idle-3x-0.png"),
]
settle_identity = {
    f"step-settle-{s}x-{i}.png": sha(A + f"step-settle-{s}x-{i}.png") == sha(A + f"step-idle-{s}x-{i}.png")
    for s in (1, 3) for i in range(4)
}

def op(domain, profile, cfg_hash_note, check_extra, bundle_name, state_hash, binding):
    d = f"work/domain-consumers/{domain}-01"
    return {
        "profile": profile,
        "state_path": f".pixl/assets/{domain}/state.px",
        "candidate": "delivery.candidate",
        "config_input": ref(f"work/domain-consumer-inputs/{domain}-config.json"),
        "config_retained_by_tool": ref(f"{d}/config.json"),
        "config_semantically_identical": True,
        "out": d,
        "result_file": ref(f"work/domain-consumers/{domain}-result.json"),
        "internal_result": ref(f"{d}/result.json"),
        "result_file_vs_internal": "identical except the result_path copy adds a hash_domains key",
        "status": "complete",
        "phases_rc0": ["node-version", "node-capabilities", "capture", "check", "observation"],
        "check": dict({"file": ref(f"{d}/check.json"), "status": "pass", "failures": 0}, **check_extra),
        "cleanup": {"complete": True, "browser_closed": True, "server_closed": True, "profile_removed": True, "errors": 0},
        "nf06": {
            "bundle": ref(f"{d}/import/{bundle_name}.zip"),
            "bundle_sha_matches_filename": sha(f"{d}/import/{bundle_name}.zip") == bundle_name,
            "import_result": ref(f"{d}/import/result.json"),
            "observation_mode": "live",
            "renderer_executed_outer_receipt": True,
            "renderer_executed_import_layer": False,
            "files_verified": True,
            "automatic_acceptance": False,
            "state_changed": False,
        },
        "state_hash_reported": state_hash,
        "state_hash_caller_pixl_validate_after": state_hash,
        "state_file_sha256_before_delegation": state_hash,
        "state_file": ref(f".pixl/assets/{domain}/state.px"),
        "binding_hash": binding,
        "state_written": False,
    }

TERRAIN_HASH = "0190be0a8e2f9705218640911640e3ef25545521a33f1fea1c08ad80579996d9"
ANIM_HASH = "a3de687085f37f11ad962fc72219986a0f26e115f7ec0c39c5a79e470ad17a4c"

doc = {
    "report": "DOMAIN-CONSUMERS.md caller half (TM-08 consumer qualification)",
    "written_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "caller": {"host": "claude", "role": "calling agent", "model": "claude-fable-5-1"},
    "native_child": {
        "agent_type": "pixl:pixl",
        "agent_id": "afc36da3629147ad2",
        "route": "Claude Code Agent tool, subagent_type pixl:pixl, run_in_background false, waited for completion",
        "declared_identity_in_result": "pixl:pixl",
        "tool_uses_reported": 72,
        "duration_ms_reported": 472571,
    },
    "specialist_result": ref("work/domain-consumers/SPECIALIST-RESULT.json"),
    "operations": {
        "terrain": op("terrain", "tile-neighborhood-v1", None,
                      {"pixel_checks": 4, "source_checks": 43, "clock_checks": 0},
                      "e90910ec90f54c4f4db1da5c15e7d062c7e669ec8faef30ea398e50e726f89ae", TERRAIN_HASH,
                      "c28e03cccaf4d71d087cd53e53e5beb7f0668f6e9293dd3236cef70e65ca7b39"),
        "animation": op("animation", "sprite-animation-v1", None,
                        {"pixel_checks": 58, "source_checks": 12, "clock_checks": 244,
                         "playback": {"status": "observed", "sample_count": 26,
                                      "idle@1x": {"distinct_frames": 4, "transitions": 8, "wraps": 2, "skips": 0},
                                      "idle@3x": {"distinct_frames": 4, "transitions": 8, "wraps": 2, "skips": 0},
                                      "settle@1x": {"distinct_frames": 4, "transitions": 3, "wraps": 0, "skips": 0},
                                      "settle@3x": {"distinct_frames": 4, "transitions": 3, "wraps": 0, "skips": 0}}},
                        "8a968810a5fac924ca86c14d14608dcd81ed59bd34b70daba28998f8241334f5", ANIM_HASH,
                        "5395db34c175daca6cec8b22c8884ae1c25a7cde9b57d884561d19ebac016461"),
    },
    "viewed_images": viewed,
    "viewed_images_note": "All 21 images above were rendered with the Read image tool by the caller. The 8 step-settle captures were not opened separately because their bytes are identical to the corresponding step-idle captures (verified in step_settle_bytes_identical_to_step_idle); every frame of both clips at both scales is therefore covered by viewed bytes. Terrain: both neighborhoods at 1x and 3x plus all four page screenshots.",
    "step_settle_bytes_identical_to_step_idle": settle_identity,
    "independent_checks": [
        {"id": "C1", "check": "Production tree unchanged", "method": "SHA-256 manifest of every file outside work/domain-consumers (excluding installed pixl/runtime) taken before delegation and after; diff empty", "result": "pass", "files_compared": 292,
         "manifests": [ref("work/domain-consumers/caller-baseline-manifest.txt"), ref("work/domain-consumers/caller-after-manifest.txt")]},
        {"id": "C2", "check": "Installed kit unchanged", "method": "Every file listed in installed pixl/bundle-manifest.json re-hashed", "result": "pass", "ok": 244, "mismatch": 0, "missing": 0},
        {"id": "C3", "check": "State hashes unchanged", "method": "pixl_validate on both state.px after the specialist finished; hash equals the tool-reported state_hash and the file sha256 recorded before delegation", "result": "pass",
         "terrain": TERRAIN_HASH, "animation": ANIM_HASH, "revisions": {"terrain": 5, "animation": 5}},
        {"id": "C4", "check": "Result files written by the tool", "method": "terrain-result.json and animation-result.json parsed and compared with <domain>-01/result.json; identical apart from an added hash_domains key; status complete, all five phases returncode 0, state_changed false, state_written false, automatic_acceptance false, cleanup complete with no errors", "result": "pass"},
        {"id": "C5", "check": "Check receipts", "method": "check.json for both domains parsed: status pass, failures []; no failing entry anywhere in the document", "result": "pass"},
        {"id": "C6", "check": "NF-06 import receipts", "method": "import/result.json for both domains: files_verified true, automatic_acceptance false, state_changed false, renderer_executed false at the import layer (import validates a supplied report; the outer execute receipt records renderer_executed true); bundle sha256 equals zip filename", "result": "pass, with the layer distinction recorded"},
        {"id": "C7", "check": "Specialist hash references", "method": "all 50 {path, sha256} references in SPECIALIST-RESULT.json re-hashed", "result": "48 match, 2 mismatch",
         "detail": "operations.terrain.config_source and operations.animation.config_source carry the sha256 of the tool-retained copies (747c5977..., b1c39048...) instead of the original input files (b9dd6ad6..., 8c12dd55...). The parsed JSON contents are identical, so the execution used the right config; the claim that the retained copy has the same sha256 is wrong at byte level because the tool re-serialized the JSON. Reporting defect only."},
        {"id": "C8", "check": "Terrain source tiles vs corner contract", "method": "Caller-written PNG decoder; each 8x8 quadrant of all 16 tiles compared with NW=1/NE=2/SE=4/SW=8 expectation (green #72b36c land, navy #254767 water)",
         "result": "15 tiles correct; tile-6.png NW quadrant is green where navy is required; tile-6.png bytes equal tile-7.png (sha 6703a761...)",
         "tool_confirmation": "pixl_asset_check tile-6.png: green 192 px bbox [0,0,16,16], navy 64 px bbox [0,8,8,16]"},
        {"id": "C9", "check": "Rendered neighborhoods vs vertex grids", "method": "Vertex grids parsed from src/terrain.ts, cell ids derived, every quadrant of coverage-1x/3x and island-1x/3x captures compared with the vertex material",
         "result": "coverage: 5 mismatches at cells (r0,c3),(r2,c1),(r6,c5),(r7,c3),(r7,c5), all tile 6 NW, at both scales; island: 2 mismatches at (r1,c0),(r2,c0), tile 6 NW, at both scales; zero other mismatches. Mixed shoreline uses all 16 ids; island uses ids 1,2,3,4,6,7,8,9,11,12,13,14."},
        {"id": "C10", "check": "Animation source frames", "method": "Caller PNG decoder: opaque rows and feet-color (#9acdd0) rows per 16x16 frame",
         "result": "frame-0/1/3 opaque rows 2-13, feet rows 12-13; frame-2 opaque rows 4-15, feet rows 14-15 (whole figure +2 rows); frame-1 and frame-3 byte-identical (sha a4fd77b2...)"},
        {"id": "C11", "check": "Rendered ground contact", "method": "Feet-color rows in all 16 step captures plus pixl_asset_check on step-idle-1x-0 and step-idle-1x-2",
         "result": "poses 0,1,3: feet rows 26-27 at 1x / 78-83 at 3x in both clips; pose 2: feet rows 28-29 at 1x / 84-89 at 3x in both clips. pixl_asset_check feet boxes [16,26,19,28]+[21,26,24,28] (pose-0) vs [16,28,19,30]+[21,28,24,30] (pose-2). Rect, pivot [8,14] and anchor [20,28] identical for every view in capture.json, so the drop is in the authored pixels, not placement."},
        {"id": "C12", "check": "Observed playback timing", "method": "capture.json playbacks: frame index per sample and RAF ticks",
         "result": "idle transitions at 133.3, 300.0, 433.3, 666.6, 783.3, 966.6, 1083.2, 1333.2 ms (1x; 3x within 0.1 ms) against authored boundaries 120/300/420/660 ms, each on the first ~16.7 ms RAF tick at or after the boundary; 2 wraps; settle transitions at 133.3, 300.0, 433.3 ms then held frame 3 with 0 wraps. This is sampled observed playback, not continuous video and not subjective live viewing."},
    ],
    "findings": [
        {"id": "F1", "domain": "terrain", "severity": "visual continuity defect (mechanical pass)",
         "asset": "terrain delivery.candidate member.6 -> assets/terrain/tile-6.png", "member_file": ref("assets/terrain/tile-6.png"),
         "symptom": "NW quadrant painted land green; tile 6 must be NE+SE land only. Every placement shows an 8x8 green block protruding into water at a vertex whose other three quadrants are water.",
         "evidence": "C8, C9; visible in island-3x.png and island-3x-destination.png as two green stubs on the island west shore, and in coverage-3x.png at the five listed cells (clearest at row 0 col 3 beside the all-water tile 0).",
         "likely_correction": "Repaint x0-7,y0-7 of tile-6.png navy #254767 as a successor member for member.6.output.",
         "preservation_scope": "members 0-5 and 7-15, src/terrain.ts, both neighborhood grids and the destination config unchanged.",
         "caller_agrees_with_specialist": True},
        {"id": "F2", "domain": "animation", "severity": "visual continuity defect (mechanical pass)",
         "asset": "animation delivery.candidate member.2 -> assets/motion/frame-2.png (used by idle pose-2 and settle pose-2)", "member_file": ref("assets/motion/frame-2.png"),
         "symptom": "Entire figure drawn 2 px lower than frames 0/1/3, so with the constant pivot/anchor the rendered feet drop from viewport rows 26-27 to 28-29 for the 120 ms of pose-2 and snap back; the character visibly sinks and pops once per loop and once in the one-shot, contradicting the planted-floor intent.",
         "evidence": "C10, C11; visible in step-idle-3x-2.png and screen-idle-3x-2.png against the other poses; perceptible but subtle at 1x.",
         "likely_correction": "Shift frame-2 art up 2 rows inside its 16x16 canvas (feet back to rows 12-13) as a successor member for member.2.output; keep pivot [8,14] per the brief rather than editing src.",
         "preservation_scope": "members 0, 1, 3 and src/animation.ts unchanged; one successor repairs both clips.",
         "caller_agrees_with_specialist": True},
        {"id": "O1", "domain": "animation", "severity": "observation",
         "note": "frame-1 and frame-3 are byte-identical, so the cycle shows only three distinct images; a ping-pong structure, not a defect against the brief."},
        {"id": "O2", "domain": "specialist report", "severity": "reporting defect",
         "note": "Two config_source sha256 values in SPECIALIST-RESULT.json are the retained copies' hashes, not the input files' (see C7). Contents are semantically identical; the operations were run with the correct configs. The remaining 48 references verify."},
        {"id": "O3", "domain": "both", "severity": "observation",
         "note": "The NF-06 import layer records renderer_executed false while the outer execute receipt records true. The import step validates the supplied report and retains bytes; it does not itself run the renderer. Both receipts are consistent with one real headless Chrome execution per domain (Chrome 157.0.8103.39 headless, node v25.8.1, temporary user-data-dir removed on cleanup)."},
    ],
    "mechanical_vs_visual": "Mechanical: both fixed-profile executions completed, every pixel/source/clock check passed, bytes served matched the family members, mapping and pivot/anchor placement were correct, authored uneven durations drove observed transitions, the loop wrapped twice and the one-shot clamped. Visual: judged by the caller from the actual captured pixels and the source PNGs, the terrain fails the material-join intent at all seven tile-6 placements and the animation fails the planted-floor intent during pose-2. A mechanical pass coexists with two visual continuity defects. Timing samples establish observed playback only; no subjective live viewing is claimed by caller or specialist. No artistic, engine or human acceptance is asserted.",
    "production_unchanged": True,
    "acceptance_created": False,
    "scope": {
        "performed": [
            "Delegated to the actual named pixl:pixl specialist and waited for completion",
            "Read both complete tool-saved operation results, both internal result.json, check.json, import/result.json, observation.json and capture.json",
            "Compared hashes, status, phases, checks, cleanup and state hashes independently",
            "Viewed the returned images listed above at 1x and 3x",
            "Independent pixel audits of source tiles, source frames, rendered neighborhoods and rendered step captures",
            "Wrote only under work/domain-consumers",
        ],
        "not_performed": [
            "No re-execution of pixl_consumer_execute by the caller (specialist runs reused; a rerun would only duplicate observation)",
            "No pixel, metadata, src, .pixl state or kit edits",
            "No pixl_candidate_review, pixl_inspection_review, nomination, pixl_task_complete or commit",
            "No provider or remote call, installation, or global/memory change",
            "No CF-09 revision; no human acceptance",
        ],
        "open": [
            "CF-09 actual generated-art revision and observed destination outcome",
            "Human acceptance of either family",
            "q.continuity and q.destination remain unperformed in both state files",
            "M1/M2 and broader M3/M4",
        ],
    },
    "limitations": [
        "Visual judgments rest on captured stills at 1x and 3x plus sampled RAF timing; no continuous video and no human live viewing.",
        "The caller baseline manifest excluded installed pixl/runtime for speed; kit integrity was instead verified against bundle-manifest.json (244 of 244 files match).",
        "The quadrant and row audits are caller scripts plus pixl_asset_check color-component boxes; they locate the material and ground-contact breaks, not aesthetic quality.",
        "The island neighborhood does not exercise tile ids 0, 5, 10 and 15; those are covered only by the mixed shoreline.",
        "These families are authored diagnostic pixels; nothing here demonstrates real generated-art quality.",
        "The specialist identity is the Agent tool pixl:pixl route and its self-declaration; the caller compared its report against retained files rather than accepting the self-description.",
    ],
    "caller_helper_files": [
        "work/domain-consumers/caller-baseline-manifest.txt",
        "work/domain-consumers/caller-after-manifest.txt",
        "work/domain-consumers/caller-write-result.py",
    ],
    "next_action": "Keep CF-09 open: author successor members for terrain member.6 (tile-6 NW quadrant navy) and animation member.2 (frame-2 shifted up 2 px) through the authorized production workflow, preserving all other members and src; re-execute both profiles into fresh terrain-02/animation-02 directories; compare old/new pixels under the same contract; then an authorized reviewer records explicit pixl_candidate_review verdicts for q.continuity and q.destination. Human acceptance stays separately unrecorded until supplied.",
}

out = os.path.join(root, "work/domain-consumers/CALLER-RESULT.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(doc, fh, indent=2)
print("written", out, hashlib.sha256(open(out, "rb").read()).hexdigest(), os.path.getsize(out), "bytes")
print("settle identity all true:", all(settle_identity.values()))
print("nf06 bundle sha matches filename:", doc["operations"]["terrain"]["nf06"]["bundle_sha_matches_filename"], doc["operations"]["animation"]["nf06"]["bundle_sha_matches_filename"])
