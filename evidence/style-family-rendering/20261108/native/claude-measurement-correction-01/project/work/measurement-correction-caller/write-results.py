"""Calling-agent result writer for the measurement-correction continuation.

Usage (from the consumer root, selected Python):
  write-results.py comparison
  write-results.py result <handoff-path> <handoff-read-json>

`comparison` writes work/measurement-correction-caller/caller-comparison.json from
fresh hashes, the caller's own recomputation, the specialist's correction and the
three quoted historical files (verified by substring, never edited).
`result` writes REVIEW-CORRECTION-RESULT.json after the handoff exists.
"""
import datetime
import hashlib
import json
import math
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir))
CALLER_DIR = "work/measurement-correction-caller"
PIXL_DIR = "work/measurement-correction-pixl"


def p(rel):
    return os.path.join(ROOT, rel)


def sha(rel):
    return hashlib.sha256(open(p(rel), "rb").read()).hexdigest()


def size(rel):
    return os.path.getsize(p(rel))


def ref(rel, role=None):
    d = {"path": rel, "sha256": sha(rel), "bytes": size(rel)}
    if role:
        d["role"] = role
    return d


def load(rel):
    return json.load(open(p(rel), encoding="utf-8"))


def lines(rel):
    return open(p(rel), encoding="utf-8").read().splitlines()


def now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


EXPECTED = {
    "left_delta": [2, 4], "right_delta": [6, -8],
    "left_length": round(math.sqrt(20), 3), "right_length": 10.0,
    "ratio": round(math.sqrt(5), 3), "left_angle": 63.435, "right_angle": 53.13,
    "interior_angle": 63.435,
}

OLD_PLAR_HASH = "bb9978992a90dd4ee07ad62d732579fc7a90b72643dc696d91f9f50c7ebd4169"
NEW_PLAR_HASH = "2bb4a4834ff24c79d2945ac92cb904f68ac5cf09cb05ae536e53ef7b25ee4273"
STATE_HASH = "7a97831f618ffe1c761c0f839525bf4d763eacb56c7fb05b26f15f9ad3da1a81"
REQ_HASH = {
    "queue.ready": "29a330a3e5c378c80f59ed6d6d42c539ea99d7d0e5d88575d98aaca60ec0661e",
    "queue.working": "c6b5121c05396b2d21c68669dc9deffb8f71e9e44ddeb48ada7fec44d01126e5",
    "queue.retry": "c0404a1486c4a700a5342e3926de3abe363d8362a2ed11ef3a9756ede308bd4a",
    "queue.paused": "0bb25469522009a4ad8830b5d92b9e393da336d45d69179029bb82c7e5ecd935",
    "queue.start": "d25bb8982e69cb1f0a2fb448893bfa29432f21f498368312e58cbdba26250c42",
}
OLD_HANDOFF = ".pixl/handoffs/ea4a61e117eba8f611f2bee1a43ac8e2f1a6296955dc57c9212142f662baeb67.json"
PNG = "assets/ready-confirmed.png"
PNG_SHA = "fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5"

QUOTED = [
    ("work/queue.ready-reassessment/art-assessment.json", 52, "descends right at 45 degrees from (4,8) to the vertex", "axis_length_steps\": 4"),
    ("work/queue.ready-reassessment/art-assessment.json", 53, "ascends right at 45 degrees from the vertex to (12,4)", "axis_length_steps\": 8"),
    ("work/queue.ready-reassessment/art-assessment.json", 54, "about 1:2 (4 steps : 8 steps along the 45-degree axes)", None),
    ("work/queue.ready-reassessment/art-assessment.json", 83, "Both arms are exact 45-degree diagonals", None),
    ("work/render-stage-pixl/render-review.json", 41, "\"arm_axis_steps\": \"left about 4, right about 8 (ratio about 1:2)\"", None),
    ("work/render-stage-pixl/render-review.json", 47, "arm ratio about 1:2", "Confirmed"),
    ("work/render-recheck-review/caller-style-decision.json", 51, "arm geometry", "were confirmed against the decoded images"),
    ("work/render-stage-pixl/render-review.json", 106, "member production comes first", None),
]


def verify_quotes():
    out = []
    for rel, ln, s1, s2 in QUOTED:
        text = lines(rel)[ln - 1]
        out.append({"path": rel, "line": ln, "contains": [s1] + ([s2] if s2 else []),
                    "present": (s1 in text) and (s2 is None or s2 in text), "file_sha256": sha(rel)})
    return out


def caller_numbers():
    o = load(f"{CALLER_DIR}/caller-endpoints-output.json")
    q = o["quoted_polyline_(4,8)->(6,12)->(12,4)"]
    return o, {
        "left_delta": q["left_segment"]["delta"], "right_delta": q["right_segment"]["delta"],
        "left_length": round(q["left_segment"]["length"], 3), "right_length": round(q["right_segment"]["length"], 3),
        "ratio": round(q["length_ratio_right_over_left"], 3),
        "left_angle": q["left_segment"]["angle_from_horizontal_deg"], "right_angle": q["right_segment"]["angle_from_horizontal_deg"],
        "interior_angle": q["interior_angle_at_vertex_deg"],
    }


def specialist_numbers():
    m = load(f"{PIXL_DIR}/measurement-correction.json")
    q = m["quoted_polyline_computation"]
    return m, {
        "left_delta": q["left_arm_tip_to_vertex"]["delta"], "right_delta": q["vertex_to_right_arm_tip"]["delta"],
        "left_length": round(q["left_arm_tip_to_vertex"]["length"], 3), "right_length": round(q["vertex_to_right_arm_tip"]["length"], 3),
        "ratio": round(q["length_ratio_right_over_left"], 3),
        "left_angle": q["left_arm_tip_to_vertex"]["angle_from_horizontal_deg_screen"],
        "right_angle": abs(q["vertex_to_right_arm_tip"]["angle_from_horizontal_deg_screen"]),
        "interior_angle": q["interior_angle_at_vertex_deg"],
    }


def write_comparison():
    o, cn = caller_numbers()
    m, sn = specialist_numbers()
    agree = {k: (cn[k] == sn[k] == EXPECTED[k]) for k in EXPECTED}
    rerun_equal = load(f"{CALLER_DIR}/pixl-script-rerun.json") == m["measurements_raw"]
    mc = m["column_partition"]
    alt_a = o["alternative_centreline_run_centres_excluding_caps_(4,9)->(6,11)->(12,5)"]
    alt_b = o["alternative_outer_contours_(3,9)->(6,12)->(13,5)"]
    secondary = {
        "visible_bbox_11x9": o["visible_bbox"]["size"] == [11, 9] == m["measurements_raw"]["bbox_size"],
        "partition_7_3_19": o["partition_counts_x<=5_x==6_x>=7"] == [7, 3, 19] == mc["counts"],
        "partition_bbox_sizes_3x4_7x8": [o["partition_bboxes"]["x<=5"]["size"], o["partition_bboxes"]["x>=7"]["size"]] == [[3, 4], [7, 8]] == [mc["left_bbox_size"], mc["right_bbox_size"]],
        "row_spans_4_8_ratio_2": [o["tip_to_vertex_row_spans"]["left"], o["tip_to_vertex_row_spans"]["right"]] == [4, 8] == [m["what_the_old_numbers_measured"]["left_arm_row_extent"], m["what_the_old_numbers_measured"]["right_arm_row_extent"]],
        "col_spans_2_6": [o["tip_to_vertex_col_spans"]["left"], o["tip_to_vertex_col_spans"]["right"]] == [2, 6] == [m["what_the_old_numbers_measured"]["left_arm_column_extent"], m["what_the_old_numbers_measured"]["right_arm_column_extent"]],
        "contours_one_col_per_row": all(o["contours"][k] for k in o["contours"] if k.endswith("per_row")) and m["contours"]["left_arm_left_edge_rows_9_to_12_monotonic"] and m["contours"]["right_arm_right_edge_rows_5_to_12_monotonic"] and m["contours"]["right_arm_left_edge_rows_4_to_9_monotonic"],
        "alt_A_45deg_ratio_3": alt_a["left_segment"]["is_45_degree"] and alt_a["right_segment"]["is_45_degree"] and round(alt_a["length_ratio_right_over_left"], 2) == 3.0 == round(m["alternative_centreline_estimates"]["A_run_centres_excluding_caps"]["ratio_right_over_left"], 2),
        "alt_B_45deg_ratio_2.33": alt_b["left_segment"]["is_45_degree"] and alt_b["right_segment"]["is_45_degree"] and round(alt_b["length_ratio_right_over_left"], 2) == 2.33 == round(m["alternative_centreline_estimates"]["B_outer_contours"]["ratio_right_over_left"], 2),
        "stroke_thickness_2.121": o["perpendicular_thickness_of_3px_run_on_45deg"] == 2.121 == m["stroke"]["perpendicular_thickness_if_45_degree"],
        "quoted_points_are_single_pixel_caps": all(pt["single_pixel_run"] and pt["opaque"] for pt in o["quoted_points"]),
        "pixel_map_identical": o["pixel_map"] == m["pixel_map"],
        "png_sha256": o["sha256"] == PNG_SHA == m["png"]["sha256"] == sha(PNG),
    }
    history_rel = f".pixl/plar-history/{OLD_PLAR_HASH}.json"
    doc = {
        "version": 1,
        "role": "calling agent independent comparison (reviewer-guided measurement correction)",
        "recorded_at": now(),
        "assignment": {
            "MEASUREMENT-CORRECTION.md": ref("MEASUREMENT-CORRECTION.md"),
            "MEASUREMENT-REVIEW-FEEDBACK.json": ref("MEASUREMENT-REVIEW-FEEDBACK.json"),
            "finding": "CLAUDE-RECHECK-NUMERIC-01",
            "advisory": "CLAUDE-RECHECK-CONTINUATION-01",
        },
        "delegation": {
            "specialist": "native agent type 'pixl', Claude Code subagent a631f401ad654a1a4, single foreground round (run_in_background false); the caller waited for its report before verifying",
            "restart_note": "artifact-based cold continuation after the completed renderer recovery; not a resumed native child conversation; no SendMessage follow-up was needed",
            "scope_given": "image-free numerical correction and PLAR proposal only; no save, handoff, PX2, provider, art or capture change",
        },
        "specialist_artifacts": [
            ref(f"{PIXL_DIR}/measure-endpoints.py", "deterministic measurement script (reads only the PNG)"),
            ref(f"{PIXL_DIR}/build-artifacts.py", "helper that composed the three JSON files"),
            ref(f"{PIXL_DIR}/measurement-correction.json", "NEW specialist measurement correction"),
            ref(f"{PIXL_DIR}/plar-update-proposal.json", "full proposed PLAR document (saved unchanged by the caller)"),
            ref(f"{PIXL_DIR}/plar-change-ledger.json", "old-to-new ledger E01, N01-N04"),
        ],
        "caller_recomputation": {
            "script": ref(f"{CALLER_DIR}/caller-endpoints.py", "caller-written script, independent of the specialist's"),
            "output": ref(f"{CALLER_DIR}/caller-endpoints-output.json"),
            "specialist_script_rerun": ref(f"{CALLER_DIR}/pixl-script-rerun.json", "python -I rerun of the specialist script"),
            "specialist_script_rerun_equals_embedded_measurements_raw": rerun_equal,
            "coordinate_convention": o["coordinate_convention"],
            "png_viewed_by_caller": "host Read image viewer on assets/ready-confirmed.png: a single light-blue check mark, short descending left arm, long ascending right arm; and the decoded 16x16 pixel map below",
            "pixel_map": o["pixel_map"],
            "quoted_polyline": o["quoted_polyline_(4,8)->(6,12)->(12,4)"],
            "what_the_quoted_points_are": "each of (4,8), (6,12), (12,4) is an opaque single-pixel run (tapered cap); (4,8) sits directly above the centre of the row-9 run [3,5], (12,4) directly above the centre of the row-5 run [11,13], (6,12) directly below the centre of the row-11 run [5,7]; the strokes merge in rows 10-11",
            "row_spans_tip_to_vertex": o["tip_to_vertex_row_spans"],
            "col_spans_tip_to_vertex": o["tip_to_vertex_col_spans"],
            "partition_counts_x<=5_x==6_x>=7": o["partition_counts_x<=5_x==6_x>=7"],
            "partition_bboxes": o["partition_bboxes"],
            "contours": o["contours"],
            "alternative_centreline_run_centres_excluding_caps": alt_a,
            "alternative_outer_contours": alt_b,
            "perpendicular_thickness_of_3px_run_on_45deg": o["perpendicular_thickness_of_3px_run_on_45deg"],
        },
        "comparison_with_specialist": {
            "primary_quantities": {k: {"caller": cn[k], "specialist": sn[k], "expected_from_feedback": EXPECTED[k], "agree": agree[k]} for k in EXPECTED},
            "all_primary_agree": all(agree.values()),
            "secondary_checks": secondary,
            "all_secondary_agree": all(secondary.values()),
            "convention_note": "The specialist reports the right-arm angle as -53.13 deg (signed, y-down screen convention: negative = ascending right); the caller reports its magnitude 53.13 deg with the direction 'ascending right'. Same quantity, different sign convention; not a discrepancy.",
        },
        "quoted_claims_verified_present_in_unchanged_files": verify_quotes(),
        "caller_judgement_on_claims": {
            "corrected": [
                "art-assessment.json lines 52-54: lines through (4,8)->(6,12) and (6,12)->(12,4) are 63.435 and 53.130 degrees from the horizontal, lengths sqrt(20) and 10, ratio sqrt(5)=2.236; they are not 45-degree axes and '4 steps : 8 steps along the 45-degree axes' is not a measurement of them. 4 and 8 are the vertical row spans (rows 8..12, 4..12); the column spans are 2 and 6.",
                "art-assessment.json line 83: 'Both arms are exact 45-degree diagonals' is true of the 3-pixel-run stroke staircases between the caps (contours advance one column per row) and false of the tip-to-tip arm axes.",
                "render-review.json line 41 arm_axis_steps 'about 4 / about 8 (ratio about 1:2)' repeats row spans under the name 'axis steps'.",
                "render-review.json line 47 'Confirmed' for 'arm ratio about 1:2': the cross-check reproduced counts, bbox and contours, which do not verify the axis/ratio claim.",
                "caller-style-decision.json line 51 'arm geometry ... confirmed': the arm-axis explanation had not been reconciled; the other items in that sentence (pixel map, dx=+9, gaps, 29/261, triangle 10x12, check 11x9) do reproduce.",
            ],
            "supported": [
                "29 opaque / 227 transparent pixels, alpha {0,255}, one colour #70b9ed",
                "visible bbox 11x9 ([3,4,14,13] exclusive = [3,4,13,12] inclusive)",
                "one 4-connected component",
                "7 / 3 / 19 occupied-pixel partition by column (x<=5, x==6, x>=7): a count, not an axis length",
                "contours advance one column per row between the caps and the merge (regular 45-degree staircases); 3-pixel interior runs, 1-pixel tapered tips; about 2.12 px perpendicular stroke",
                "vertex pixel (6,12) as the lowest tip pixel; the strokes merge in rows 10-11",
                "legible asymmetric check; asymmetry realised through length (row spans 4 vs 8, column spans 2 vs 6, 7 vs 19 pixels)",
            ],
            "about_1_to_2": "acceptable only as approximate visual-proportion language; exact as a ratio of row spans (4:8); measured tip-to-tip axis ratio is 2.24, run-centre ratio 3.0, outer-contour ratio 2.33",
            "distinct_measurements": [
                "lines through the quoted tip pixels (deltas, lengths, angles, sqrt(5) ratio)",
                "occupied-pixel partition counts (7/3/19)",
                "bounding boxes and row/column spans (3x4 and 7x8; 4/8 rows; 2/6 columns)",
                "stroke contour staircases (one column per row; 45-degree construction; 2.12 px thickness)",
                "alternative centrelines (run centres excluding caps: 45 deg, ratio 3.0; outer contours: 45 deg, ratio 2.33; principal axes: 59.0/46.5 deg, ratio 2.76)",
            ],
        },
        "adoption_scope": {
            "style_decision": "unchanged: ADOPT (scoped) the delivered Ready sample fc5e43ae... as the family style baseline (hard binary edges, about 2 px perpendicular stroke built from 3-pixel runs on 45-degree staircases, flat single #70b9ed fill, footprint 9-12 px in the 12x12 safe area, transparent exterior, binary alpha in practice). These properties are re-measured as true; the corrected axis explanation does not touch them.",
            "not_a_rejection": True,
            "no_other_host_style_imposed": True,
            "art_unchanged": {"path": PNG, "sha256": sha(PNG)},
            "verdicts_unchanged": "six historical verdicts ready.delivery.review.verdict.0-5 remain bound to the historical contract 806a1f2d...",
        },
        "plar_save_by_caller": {
            "operation": "kit CLI `pixl.py plar save` (same operation as pixl_plar_save) with --expect " + OLD_PLAR_HASH,
            "document_saved": ref(f"{PIXL_DIR}/plar-update-proposal.json"),
            "save_result": ref(f"{CALLER_DIR}/plar-save-result.json"),
            "old_hash": OLD_PLAR_HASH,
            "new_hash": sha("plar.txt"),
            "new_hash_expected": NEW_PLAR_HASH,
            "history_retained": {"path": history_rel, "sha256": sha(history_rel), "matches_name": sha(history_rel) == OLD_PLAR_HASH},
            "diff_regions_vs_old": ["queue.ready next (N01)", "queue.ready evidence append (E01)", "queue.working next (N02)", "queue.retry next (N03)", "queue.paused next (N04)"],
            "hash_covered_changes": [],
            "requirements_hash_by_row_after_save_fresh_reads": REQ_HASH,
            "requirements_hash_changed": False,
            "save_result_changes": load(f"{CALLER_DIR}/plar-save-result.json")["changes"],
            "considered_and_kept": "approved_style_reference.scope and the member references[].instructions ('3-pixel runs on 45-degree diagonals') describe stroke construction, which is re-measured as true; no requirement text states the axis or 4:8 axis-step claim",
        },
        "px2_state": {"path": ".pixl/assets/queue.ready/state.px", "sha256": sha(".pixl/assets/queue.ready/state.px"), "expected": STATE_HASH, "revision": 14, "changed": sha(".pixl/assets/queue.ready/state.px") != STATE_HASH, "families": [], "pending_jobs": []},
        "historical_unchanged": [
            ref("work/queue.ready-reassessment/art-assessment.json"),
            ref("work/render-stage-pixl/render-review.json"),
            ref("work/render-recheck-review/caller-style-decision.json"),
            ref("FAMILY-RESULT.json"),
            ref("RENDER-RECHECK-RESULT.json"),
            ref(OLD_HANDOFF),
            ref(PNG),
        ],
        "next_order_clarified": "Review the current member requirements of queue.working, queue.retry and queue.paused against their sources and the approved_style_reference; save the applicable member/collective plans through the existing family-delivery operation BEFORE any member production; then produce members only under explicit new authorization. Working, Retry and Paused remain missing, not rejected; no family production or collective acceptance is assigned here. render-review.json line 106 ('member production comes first') is superseded as a dispatch order by this PLAR next wording.",
        "discrepancies": [],
        "verdict": "consistent" if (all(agree.values()) and all(secondary.values()) and rerun_equal) else "inconsistent",
    }
    out = f"{CALLER_DIR}/caller-comparison.json"
    with open(p(out), "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({"written": out, "sha256": sha(out), "bytes": size(out), "verdict": doc["verdict"]}))


def write_result(handoff_rel, handoff_read_rel):
    comp = load(f"{CALLER_DIR}/caller-comparison.json")
    handoff = load(handoff_rel)
    fresh = load(handoff_read_rel)
    history_rel = f".pixl/plar-history/{OLD_PLAR_HASH}.json"
    h_resume = handoff.get("resume", {})
    f_cont = fresh.get("production", {}).get("continuation", {})
    resume_match = {k: (h_resume.get(k) == f_cont.get(k)) for k in ("store", "state_hash", "asset_id", "requirements_hash", "task", "action")}
    doc = {
        "version": 1,
        "host": "claude-measurement-correction-01",
        "role": "calling agent",
        "status": "delivered",
        "status_scope": "MEASUREMENT-CORRECTION.md continuation complete: one focused foreground PIXL instance corrected the Ready arm-axis numerical explanation image-free; the caller independently recomputed the quoted geometry from the retained PNG with its own script, verified the quoted lines in the unchanged historical files, saved the proposed hash-safe PLAR wording/evidence through the existing save operation (history retained, requirements_hash unchanged on every row, 'changed' selection diagnostic preserved), saved a NEW exact handoff and compared it with fresh runtime output. The corrected explanation is not an asset rejection; the scoped style decision, the art, the captures, the verdicts and PX2 state are unchanged. Family unfinished: Working, Retry, Paused absent (missing, not rejected); no family production, family plan or collective acceptance was performed. No recapture, generation, provider call, credential, install, host-setting or renderer change.",
        "recorded_at": now(),
        "assignment": {
            "MEASUREMENT-CORRECTION.md": ref("MEASUREMENT-CORRECTION.md"),
            "MEASUREMENT-REVIEW-FEEDBACK.json": ref("MEASUREMENT-REVIEW-FEEDBACK.json"),
            "SESSION.md": ref("SESSION.md"),
            "finding_addressed": "CLAUDE-RECHECK-NUMERIC-01",
            "advisory_addressed": "CLAUDE-RECHECK-CONTINUATION-01 (next-order wording in PLAR next fields)",
        },
        "workspace": ROOT.replace("\\", "/"),
        "asset_id": "queue.ready",
        "requirements_hash": {"before": REQ_HASH["queue.ready"], "after": fresh["requirements_hash"], "changed": fresh["requirements_hash"] != REQ_HASH["queue.ready"]},
        "provider_simulated": True,
        "delegation": comp["delegation"],
        "findings": {
            "coordinate_convention": comp["caller_recomputation"]["coordinate_convention"],
            "quoted_points": comp["caller_recomputation"]["what_the_quoted_points_are"],
            "quoted_polyline": comp["caller_recomputation"]["quoted_polyline"],
            "row_spans": comp["caller_recomputation"]["row_spans_tip_to_vertex"],
            "col_spans": comp["caller_recomputation"]["col_spans_tip_to_vertex"],
            "partition_counts": comp["caller_recomputation"]["partition_counts_x<=5_x==6_x>=7"],
            "alternative_centrelines": {
                "run_centres_excluding_caps": comp["caller_recomputation"]["alternative_centreline_run_centres_excluding_caps"],
                "outer_contours": comp["caller_recomputation"]["alternative_outer_contours"],
            },
            "corrected_claims": comp["caller_judgement_on_claims"]["corrected"],
            "supported_claims": comp["caller_judgement_on_claims"]["supported"],
            "about_1_to_2": comp["caller_judgement_on_claims"]["about_1_to_2"],
            "distinct_measurements": comp["caller_judgement_on_claims"]["distinct_measurements"],
            "specialist_and_caller_agree": comp["comparison_with_specialist"]["all_primary_agree"] and comp["comparison_with_specialist"]["all_secondary_agree"],
        },
        "old_artifacts_preserved": comp["historical_unchanged"] + [
            {"path": history_rel, "sha256": sha(history_rel), "bytes": size(history_rel), "role": "previous plar.txt bytes (bb997899...) retained by the save"},
        ],
        "old_plar_hash": OLD_PLAR_HASH,
        "new_artifacts": {
            "specialist": comp["specialist_artifacts"],
            "caller": [
                ref(f"{CALLER_DIR}/caller-endpoints.py", "caller recomputation script"),
                ref(f"{CALLER_DIR}/caller-endpoints-output.json", "caller recomputation output"),
                ref(f"{CALLER_DIR}/pixl-script-rerun.json", "caller rerun of the specialist script"),
                ref(f"{CALLER_DIR}/plar-save-result.json", "kit CLI plar save stdout"),
                ref(f"{CALLER_DIR}/caller-comparison.json", "NEW independent caller comparison"),
                ref(handoff_read_rel, "fresh focused pixl_plar_read after the handoff"),
                ref(f"{CALLER_DIR}/write-results.py", "this writer"),
            ],
        },
        "adoption_scope": comp["adoption_scope"],
        "plar": {
            "old_hash": OLD_PLAR_HASH,
            "new_hash": sha("plar.txt"),
            "history_retained": history_rel,
            "changes": comp["plar_save_by_caller"]["diff_regions_vs_old"],
            "hash_covered_changes": [],
            "requirements_hash_by_row": REQ_HASH,
            "production_selection_diagnostic": {
                "task": "r.22e90a2a03fe453a.task (done)",
                "bound_requirements_hash": "806a1f2d21914fe2ffa0b11cbe8556ea4d64fd5aeb1dc2aae52e60796cf2d673",
                "current_requirements_hash": fresh["requirements_hash"],
                "selection_status": fresh["production"]["selection_bindings"][0]["status"],
                "derived_next_action": fresh["production"]["next_action"],
                "handling": "preserved; not rebound, verdicts not transferred, done task not reopened",
            },
        },
        "px2_state": comp["px2_state"],
        "handoff": {
            "path": handoff_rel,
            "sha256": sha(handoff_rel),
            "bytes": size(handoff_rel),
            "self_hash_matches_name": os.path.basename(handoff_rel).split(".")[0] == sha(handoff_rel),
            "saved_by": "calling agent via pixl_plar_handoff",
            "state_hash": h_resume.get("state_hash"),
            "requirements_hash": h_resume.get("requirements_hash"),
            "derived_next": h_resume.get("action"),
            "selection_hash": handoff.get("selection", {}).get("hash") if isinstance(handoff.get("selection"), dict) else handoff.get("selection_hash"),
            "previous_handoff": ref(OLD_HANDOFF, "historical render-recheck handoff; unchanged"),
            "caller_verification": {"resume_fields_equal_fresh_continuation": resume_match, "all_equal": all(resume_match.values()), "fresh_plar_hash": fresh["hash"], "fresh_state_hash": f_cont.get("state_hash")},
        },
        "remaining_family_work": [
            "FIRST: review the current member requirements of queue.working, queue.retry and queue.paused against their sources and the approved_style_reference, and save the applicable member/collective plans (baseline ready.retained, ordered members, destination choices, collective continuity criterion) through the existing family-delivery operation; no PX2 family plan exists yet (pixl_family: families []).",
            "THEN, only under explicit new authorization: queue.working (assets/working.png, 64x16 four-frame strip, 100 ms) fresh caller-compared packet -> pixl_plar_prepare -> renderer-recheck capture + check (frames 0,0,1,1,2,2,3,3,0) -> interactive playback via node renderer-recheck/server.mjs -> grayscale comparison; must not read as success.",
            "queue.retry (assets/error-retry.png) and queue.paused (assets/paused.png): same path; non-colour distinction from Ready and from each other.",
            "family snapshot only when every member has a nominee on a done task; collective acceptance not possible now.",
            "production-host display verification before an integrated label on queue.ready; selection binding 'changed' stays visible; new Ready generation only under explicit new authorization against the corrected packet bef24027....",
        ],
        "not_done_by_design": [
            "no recapture, generation, provider call, job preparation or dispatch",
            "no edits to assets/, renderer/, renderer-recheck/, historical contracts, verdicts, candidate, PX2 state, prior results or prior reviews",
            "no family plan, family snapshot or completed-family claim; no other host's style choice imposed",
            "no relabelling of any old confirmation as having performed this calculation; the correction is a NEW artifact",
        ],
        "next": "Resume from the handoff " + os.path.basename(handoff_rel).split(".")[0][:8] + "... after rereading focused PLAR (plar " + sha("plar.txt")[:8] + "..., requirements_hash " + fresh["requirements_hash"][:8] + "..., state " + STATE_HASH[:8] + "...). First action: member requirement review and family-delivery plans, then production under explicit new authorization.",
    }
    out = "REVIEW-CORRECTION-RESULT.json"
    with open(p(out), "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({"written": out, "sha256": sha(out), "bytes": size(out), "resume_match": resume_match, "self_hash_ok": doc["handoff"]["self_hash_matches_name"]}))


if __name__ == "__main__":
    if sys.argv[1] == "comparison":
        write_comparison()
    elif sys.argv[1] == "result":
        write_result(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit("usage: comparison | result HANDOFF_REL READ_REL")
