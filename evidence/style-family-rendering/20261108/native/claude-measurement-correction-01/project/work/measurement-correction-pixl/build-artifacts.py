"""Compose the measurement-correction artifacts (NEW files only).

Runs measure-endpoints.py (which reads only the PNG), then writes:
  measurement-correction.json   structured correction + claim table
  plar-update-proposal.json     FULL proposed PLAR document derived from plar.txt
  plar-change-ledger.json       old -> new ledger of every changed field

It never writes plar.txt, .pixl/, assets/, renderer*/ or any prior result/review file.
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir))
OUT_DIR = HERE
REL = "work/measurement-correction-pixl"

EXPECTED_PLAR_HASH = "bb9978992a90dd4ee07ad62d732579fc7a90b72643dc696d91f9f50c7ebd4169"
EXPECTED_REQ_HASH = "29a330a3e5c378c80f59ed6d6d42c539ea99d7d0e5d88575d98aaca60ec0661e"
EXPECTED_PNG_HASH = "fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5"


def sha(rel: str) -> str:
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def size(rel: str) -> int:
    return os.path.getsize(os.path.join(ROOT, rel))


def main() -> None:
    plar_rel = "plar.txt"
    plar_hash = sha(plar_rel)
    if plar_hash != EXPECTED_PLAR_HASH:
        sys.exit(f"plar.txt hash {plar_hash} != expected {EXPECTED_PLAR_HASH}; refusing to derive a proposal")

    measure_script = f"{REL}/measure-endpoints.py"
    proc = subprocess.run(
        [sys.executable, "-I", os.path.join(ROOT, measure_script), os.path.join(ROOT, "assets", "ready-confirmed.png")],
        capture_output=True, text=True, check=True,
    )
    m = json.loads(proc.stdout)
    if m["png"]["sha256"] != EXPECTED_PNG_HASH:
        sys.exit("PNG hash mismatch")

    qp = m["quoted_polyline"]
    left = qp["left_arm_tip_to_vertex"]
    right = qp["vertex_to_right_arm_tip"]

    sources_quoted = {
        "art_assessment": {"path": "work/queue.ready-reassessment/art-assessment.json", "sha256": sha("work/queue.ready-reassessment/art-assessment.json")},
        "render_review": {"path": "work/render-stage-pixl/render-review.json", "sha256": sha("work/render-stage-pixl/render-review.json")},
        "caller_style_decision": {"path": "work/render-recheck-review/caller-style-decision.json", "sha256": sha("work/render-recheck-review/caller-style-decision.json")},
    }

    claims = [
        {
            "id": "MC-01",
            "source": "work/queue.ready-reassessment/art-assessment.json",
            "lines": [52],
            "quoted": "left_arm ... \"direction\": \"descends right at 45 degrees from (4,8) to the vertex\", \"axis_length_steps\": 4",
            "status": "corrected",
            "finding": f"The segment (4,8)->(6,12) has delta {left['delta']}, length {left['length']} (sqrt(20)) and lies {left['angle_from_horizontal_deg_screen']} degrees below the horizontal (descending right). It is not a 45-degree line and its length is not 4 steps along a 45-degree axis. The number 4 is the vertical row extent rows 8..12 (12-8); the column extent is 2.",
            "retained_part": "'descends right' (direction) and the endpoints themselves are correct; (4,8) is the single-pixel cap of the left arm and (6,12) is the single-pixel bottom tip.",
        },
        {
            "id": "MC-02",
            "source": "work/queue.ready-reassessment/art-assessment.json",
            "lines": [53],
            "quoted": "right_arm ... \"direction\": \"ascends right at 45 degrees from the vertex to (12,4)\", \"axis_length_steps\": 8",
            "status": "corrected",
            "finding": f"The segment (6,12)->(12,4) has delta {right['delta']}, length {right['length']} and lies {abs(right['angle_from_horizontal_deg_screen'])} degrees above the horizontal (ascending right). Not a 45-degree line; 8 is the vertical row extent rows 4..12 (12-4), the column extent is 6.",
            "retained_part": "'ascends right' and the endpoint (12,4) (single-pixel cap of the right arm) are correct.",
        },
        {
            "id": "MC-03",
            "source": "work/queue.ready-reassessment/art-assessment.json",
            "lines": [54],
            "quoted": "\"arm_length_ratio\": \"about 1:2 (4 steps : 8 steps along the 45-degree axes)\"",
            "status": "corrected (explanation); approximate visual proportion retained as approximate",
            "finding": f"Along the quoted tip-to-tip lines the length ratio is 10/sqrt(20) = sqrt(5) = {qp['length_ratio_right_over_left']}, not 2. The 4:8 = 1:2 ratio is exact only as a ratio of vertical row extents. Other defensible centreline estimates give 3.0 (3-pixel run centres excluding caps), 2.33 (outer contours) and 2.76 (principal-axis extents). 'About 1:2' remains acceptable only as approximate visual-proportion language (long arm roughly twice the short arm by eye and by row span); it is not a measured ratio of 45-degree axis lengths.",
        },
        {
            "id": "MC-04",
            "source": "work/queue.ready-reassessment/art-assessment.json",
            "lines": [83],
            "quoted": "\"Both arms are exact 45-degree diagonals, so each contour steps one pixel per row with uniform run lengths\"",
            "status": "corrected in part; stroke-construction part supported",
            "finding": "The stroke contours between the caps and the merge DO step exactly one column per row in one direction (left-arm left edge rows 9..12 = 3,4,5,6; right-arm right edge rows 5..12 = 13..6; right-arm left edge rows 4..9 = 12..7), so the 3-pixel-run staircases are built on 45-degree diagonals and the edge-rhythm check holds for the strokes. But the arm AXES through the quoted endpoints are 63.4 and 53.1 degrees, because each single-pixel cap sits directly above the centre of its adjacent 3-pixel run (edge reverses by one column at the cap). 'Exact 45-degree diagonals' is true of the stroke staircases, false of the tip-to-tip axes.",
        },
        {
            "id": "MC-05",
            "source": "work/render-stage-pixl/render-review.json",
            "lines": [41],
            "quoted": "\"arm_axis_steps\": \"left about 4, right about 8 (ratio about 1:2)\"",
            "status": "corrected",
            "finding": "Repeats the row-extent figures under the name 'axis steps'. 4 and 8 are row extents rows 8..12 and 4..12; axis lengths through the quoted endpoints are sqrt(20) and 10 (ratio sqrt(5)).",
        },
        {
            "id": "MC-06",
            "source": "work/render-stage-pixl/render-review.json",
            "lines": [47],
            "quoted": "claims: \"stroke about 2.1 px perpendicular; arm ratio about 1:2; one-step-per-row staircases; ...\" verdict: \"Confirmed (...)\"",
            "status": "corrected (the 'arm ratio about 1:2' confirmation); other listed items supported",
            "finding": "The cross-check did not compute the quoted endpoint geometry; it reproduced counts, the bounding box and contour edges, which measure different things and cannot confirm the axis/ratio claim. Stroke 2.1 px (3/sqrt(2)=2.121), one-step-per-row staircases, one component, contrast 7.41:1 and the Start 10x12 figure remain confirmed.",
        },
        {
            "id": "MC-07",
            "source": "work/render-recheck-review/caller-style-decision.json",
            "lines": [51],
            "quoted": "\"All other preserved numerical claims (pixel map, arm geometry, dx=+9 offset, gaps, 29/261 accent pixels, triangle 10x12, check 11x9) were confirmed against the decoded images.\"",
            "status": "corrected (the words 'arm geometry'); the remaining items supported",
            "finding": "'arm geometry' as stated in art-assessment lines 52-54 (45-degree axes, 4:8 axis steps) was not reconciled; pixel map, dx=+9, gaps, 29/261, triangle 10x12 and check 11x9 reproduce.",
        },
        {"id": "MS-01", "claim": "29 opaque / 227 transparent pixels, alpha values {0,255}, single colour #70b9ed", "status": "supported", "value": [m["opaque_pixels"], m["transparent_pixels"], m["alpha_values"], list(m["opaque_colours"].keys())]},
        {"id": "MS-02", "claim": "visible bbox [3,4,14,13] exclusive, 11x9", "status": "supported", "value": [m["visible_bbox_exclusive"], m["bbox_size"]]},
        {"id": "MS-03", "claim": "one 4-connected component", "status": "supported", "value": m["components_4_connected"]},
        {"id": "MS-04", "claim": "7 / 3 / 19 occupied-pixel partition by columns x<=5 / x==6 / x>=7", "status": "supported (as a column partition, not an axis measurement)", "value": m["column_partition"]["counts"]},
        {"id": "MS-05", "claim": "contours advance one column per row between the caps and the merge (regular staircases)", "status": "supported", "value": {k: v for k, v in m["contours"].items() if k != "reading"}},
        {"id": "MS-06", "claim": "interior rows are 3-pixel runs; tips taper to 1 pixel at rows 4, 8 (left) and 12", "status": "supported", "value": [row["run_lengths"] for row in m["rows"]]},
        {"id": "MS-07", "claim": "vertex pixel [6,12]", "status": "supported as the single lowest tip pixel; the two strokes actually merge in rows 10-11 (runs [4,8] and [5,7]) above it", "value": m["quoted_endpoint_identity"]["vertex"]},
        {"id": "MS-08", "claim": "stroke roughly 2 px perpendicular (about 2.1)", "status": "supported", "value": m["stroke"]["perpendicular_thickness_if_45_degree"]},
        {"id": "MS-09", "claim": "mass centroid (8.5, 8.74) in pixel-edge coordinates", "status": "supported", "value": m["mass_centroid_edge_coords"]},
        {"id": "MS-10", "claim": "a legible asymmetric check (short descending left arm, long ascending right arm)", "status": "supported; the asymmetry is real (row extents 4 vs 8, column extents 2 vs 6, 7 vs 19 pixels) and is a visual judgement already recorded in verdicts; this correction changes none of it", "value": None},
    ]

    correction = {
        "version": 1,
        "role": "specialist measurement correction",
        "recorded_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "host": "claude-measurement-correction-01 (PIXL instance, image-free factual correction; artifact-based, not a resumed conversation)",
        "assignment": {
            "MEASUREMENT-CORRECTION.md": sha("MEASUREMENT-CORRECTION.md"),
            "MEASUREMENT-REVIEW-FEEDBACK.json": sha("MEASUREMENT-REVIEW-FEEDBACK.json"),
            "finding": "CLAUDE-RECHECK-NUMERIC-01",
            "advisory": "CLAUDE-RECHECK-CONTINUATION-01 (next-order wording; addressed in the PLAR proposal's next fields, not here)",
        },
        "scope": {
            "corrects": "only the numerical explanation of the Ready arm axes (angles, axis lengths, 'steps along the axes', the 1:2 axis ratio) and the reviews that repeated or confirmed it",
            "does_not_do": ["reject or re-grade the asset", "change assets/ready-confirmed.png or any capture", "change the caller's scoped style decision", "change PX2 state, verdicts, jobs or plar.txt", "add a geometric rejection criterion for future members"],
            "not_a_rejection_condition": True,
            "style_decision_stays": "The adopted scoped baseline (hard binary edges, about 2 px perpendicular stroke, flat single #70b9ed fill, footprint 9-12 px in the 12x12 safe area, transparent exterior with binary alpha in practice) rests on properties that this correction re-measures as true; the stroke staircases are 45-degree constructions even though the tip-to-tip arm axes are not.",
            "art_unchanged": {"path": "assets/ready-confirmed.png", "sha256": m["png"]["sha256"], "bytes": m["png"]["bytes"]},
        },
        "coordinate_convention": m["coordinate_convention"],
        "convention_note": "Identical to art-assessment.json line 21 and its pixel_map (lines 33-50): zero-based, x right, y down; the quoted points are (column, row). The same convention is used in render-review.json line 41. Angles below are measured from the horizontal; 'descends right' means +x,+y on screen and 'ascends right' means +x,-y.",
        "png": m["png"],
        "pixel_map": m["pixel_map"],
        "pixel_map_column_ruler": m["pixel_map_column_ruler"],
        "rows": m["rows"],
        "quoted_endpoint_identity": {
            "(4,8)": "opaque single-pixel cap of the left arm (row 8 run [4,4]); directly above the centre of the row-9 3-pixel run [3,5]. It is the top tip of the short arm, not a point on a 45-degree stroke contour.",
            "(6,12)": "opaque single-pixel bottom tip (row 12 run [6,6]); directly below the centre of the row-11 run [5,7]. The two strokes merge in rows 10 (run [4,8]) and 11 (run [5,7]); (6,12) is the lowest tip pixel of that merge.",
            "(12,4)": "opaque single-pixel cap of the right arm (row 4 run [12,12]); directly above the centre of the row-5 run [11,13].",
            "raw": m["quoted_endpoint_identity"],
        },
        "quoted_polyline_computation": {
            "polyline": "(4,8) -> (6,12) -> (12,4)",
            "left_arm_tip_to_vertex": left,
            "vertex_to_right_arm_tip": right,
            "length_ratio_right_over_left": qp["length_ratio_right_over_left"],
            "length_ratio_exact": qp["length_ratio_exact"],
            "interior_angle_at_vertex_deg": qp["interior_angle_at_vertex_deg"],
            "expected_check_values": {"deltas": [[2, 4], [6, -8]], "lengths": ["sqrt(20)=4.472", "10"], "ratio": "sqrt(5)=2.236", "angles_deg": [63.435, 53.130]},
            "all_expected_values_reproduced": (
                left["delta"] == [2, 4] and right["delta"] == [6, -8] and left["length"] == 4.472 and right["length"] == 10.0
                and qp["length_ratio_right_over_left"] == 2.236 and left["angle_from_horizontal_deg_screen"] == 63.435
                and right["angle_from_horizontal_deg_screen"] == -53.13
            ),
            "verdicts": {
                "supports_exact_45_degree_axes": False,
                "supports_4_steps_to_8_steps_along_45_degree_axes": False,
                "supports_about_1_to_2_as_measured_axis_ratio": False,
                "about_1_to_2_as_approximate_visual_proportion": "acceptable only when labelled approximate; the exact 1:2 belongs to the vertical row extents (4 rows vs 8 rows), and the measured axis ratio is 2.24",
            },
        },
        "what_the_old_numbers_measured": m["what_the_old_numbers_measured"],
        "column_partition": m["column_partition"],
        "contours": m["contours"],
        "alternative_centreline_estimates": m["alternative_centrelines"],
        "stroke": m["stroke"],
        "distinct_measurements_not_to_conflate": [
            {"kind": "quoted tip-to-tip lines", "values": "deltas (2,4)/(6,-8); lengths 4.472/10; angles 63.4 deg down-right / 53.1 deg up-right; ratio 2.236; interior angle 63.4 deg"},
            {"kind": "occupied-pixel partition by column", "values": "7 / 3 / 19 pixels for x<=5 / x==6 / x>=7; a count, not a length or angle"},
            {"kind": "bounding boxes / row and column spans", "values": "left partition bbox [3,8,6,12] 3x4, right partition bbox [7,4,14,12] 7x8; tip-to-vertex row extents 4 and 8 (ratio exactly 1:2), column extents 2 and 6 (ratio 1:3)"},
            {"kind": "stroke contour staircases", "values": "one column per row between caps and merge; 45-degree construction of the 3-pixel-run strokes; perpendicular thickness 3/sqrt(2) = 2.12 px"},
            {"kind": "alternative centrelines", "values": "A run-centres excluding caps: 45 deg both arms, lengths 2.83/8.49, ratio 3.0; B outer contours: 45 deg, lengths 4.24/9.90, ratio 2.33; C principal axes of the partitions: 59.0 deg / 46.5 deg, extents 3.09/8.52, ratio 2.76"},
            {"kind": "approximate visual proportion", "values": "'about 1:2' as seen; consistent with row extents and roughly with the pixel-count and outer-contour ratios, but not a measured 45-degree-axis ratio"},
        ],
        "claims": claims,
        "summary": {
            "corrected": ["art-assessment.json lines 52-54: 45-degree axes through (4,8)/(6,12)/(12,4) and '4 steps : 8 steps along the 45-degree axes'", "art-assessment.json line 83: 'Both arms are exact 45-degree diagonals' as a statement about the arm axes (true only of the stroke staircases)", "render-review.json line 41: arm_axis_steps 'about 4 / about 8 (ratio about 1:2)'", "render-review.json line 47: 'Confirmed' for 'arm ratio about 1:2' (not computed from the quoted endpoints)", "caller-style-decision.json line 51: 'arm geometry ... confirmed'"],
            "supported": ["29/227 pixels, two RGBA values", "bbox [3,4,14,13] 11x9", "one 4-connected component", "7/3/19 column partition", "one-column-per-row contours between caps and merge", "3-pixel interior runs, 1-pixel tapered tips", "vertex pixel (6,12)", "about 2.1 px perpendicular stroke", "centroid (8.5, 8.74)", "legible asymmetric check; asymmetry realised through length"],
            "effect_on_decisions": "none: no verdict, acceptance, style decision or requirement changes; nothing is rejected; the art is unchanged",
        },
        "knowledge_methods_consulted": [
            {"id": "edge-rhythm", "use": "its check 'a supplied straight diagonal retains its declared repeating step pattern' applies to the stroke contours (which do keep a one-column-per-row pattern); it is not a method for measuring an arm axis through tapered caps, so it could not have confirmed the 45-degree axis claim"}
        ],
        "script": {"path": measure_script, "sha256": sha(measure_script), "interpreter": sys.version.split()[0], "pillow": __import__("PIL").__version__, "reads": ["assets/ready-confirmed.png"]},
        "quoted_source_files_unchanged": sources_quoted,
        "measurements_raw": m,
    }

    corr_rel = f"{REL}/measurement-correction.json"
    with open(os.path.join(ROOT, corr_rel), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(correction, fh, indent=2)
        fh.write("\n")
    corr_hash = sha(corr_rel)

    # ---------------- PLAR proposal ----------------
    with open(os.path.join(ROOT, plar_rel), "r", encoding="utf-8") as fh:
        plar_text = fh.read()
    plar = json.loads(plar_text)
    proposal = copy.deepcopy(plar)
    ledger_changes = []

    def asset(doc, aid):
        return next(a for a in doc["assets"] if a["id"] == aid)

    ready = asset(proposal, "queue.ready")

    # (a) evidence link
    new_evidence = {
        "path": corr_rel,
        "note": (
            f"Specialist measurement correction (sha256 {corr_hash}; image-free; script {REL}/measure-endpoints.py) of the Ready arm-axis explanation: "
            "the quoted tip-to-tip polyline (4,8)->(6,12)->(12,4) has deltas (2,4) and (6,-8), lengths sqrt(20)=4.47 and 10 (ratio sqrt(5)=2.24) and angles 63.4 deg (descending right) and 53.1 deg (ascending right) from the horizontal, so it is not two exact 45-degree axes of 4 and 8 steps; the old 4/8 figures are vertical row extents (rows 8..12 and 4..12) and the 7/3/19 counts are a column partition. "
            "Corrects work/queue.ready-reassessment/art-assessment.json lines 52-54 and 83 (axis wording), work/render-stage-pixl/render-review.json line 41 (arm_axis_steps) and line 47 (the 'arm ratio about 1:2' confirmation), and work/render-recheck-review/caller-style-decision.json line 51 ('arm geometry' confirmed). "
            "Supported and unchanged: 29/227 px, bbox [3,4,14,13] 11x9, one component, 7/3/19 partition, 3-pixel runs stepping one column per row on 45-degree staircases between the caps, about 2.1 px stroke, vertex pixel (6,12), legible asymmetric check. "
            "Not an asset rejection: the art (fc5e43ae...), historical verdicts, PX2 state and the scoped style decision are unchanged; this is a corrected observation, not a new criterion."
        ),
    }
    old_evidence_len = len(ready["evidence"])
    ready["evidence"].append(new_evidence)
    ledger_changes.append({
        "id": "E01", "asset_id": "queue.ready", "path": f"assets[id=queue.ready].evidence[{old_evidence_len}]", "operation": "append",
        "old": None, "new": new_evidence, "hash_covered": False,
        "reason": "MEASUREMENT-REVIEW-FEEDBACK.json finding CLAUDE-RECHECK-NUMERIC-01 correction_scope: add an explicitly scoped correction without changing art, verdicts or style decision.",
    })

    # (b) queue.ready next
    old_ready_next = ready["next"]
    new_ready_next = (
        "render_recheck: corrected renderer-recheck capture work/render-recheck-pixl-01 (errors [], viewport 1280x1000 set via CDP before navigation, destination.png a7f8ed81... byte-identical to the caller's work/render-recheck-caller-01, eight views pixel-identical to the historical renderer/ captures) and renderer-recheck/check.py 104/104 retained; the historical renderer/ result (95/104, dx=+9 capture-layout offset, work/render-pixl-01) stays as evidence. Style decision saved in this row (approved_style_reference). "
        f"measurement_correction: the Ready arm-axis numerical explanation is corrected in {corr_rel} (the quoted tip-to-tip segments are 63.4/53.1 degrees with length ratio sqrt(5), not 45-degree axes of 4:8 steps; the old 4/8 are row extents); the art, the historical verdicts and the scoped style baseline are unchanged and nothing is rejected. "
        "Next, in this order: (1) review the current member requirements of queue.working, queue.retry and queue.paused against their sources and this row's approved_style_reference, and save the applicable member/collective plans (baseline, members, destinations, collective criteria) through the existing family-delivery operation BEFORE any member production; (2) only after those plans are saved, and under explicit new authorization, produce members. Working, Retry and Paused remain missing, not rejected; no family production and no collective acceptance is assigned now. "
        "Keep status in_progress until production-host display is verified or the owner labels integration; do not reopen the done sample task r.22e90a2a03fe453a.task; the current requirements revision (29a330a3...) flips its selection binding to 'changed' (preserve the diagnostic, do not rebind old jobs or transfer verdicts); new Ready generation only under explicit new authorization against the corrected packet (work/queue.ready-reassessment/request-review.json)."
    )
    ready["next"] = new_ready_next
    ledger_changes.append({
        "id": "N01", "asset_id": "queue.ready", "path": "assets[id=queue.ready].next", "operation": "replace",
        "old": old_ready_next, "new": new_ready_next, "hash_covered": False,
        "reason": "Record the correction and make the actionable order explicit (member requirement review and family-delivery plans before any member production; missing members stay missing; no production or collective acceptance assigned). Retains the in_progress, done-task, 'changed' selection diagnostic and explicit-authorization statements. Addresses advisory CLAUDE-RECHECK-CONTINUATION-01 (render-review.json line 106 wording must not become the dispatch order).",
    })

    # (c) member next fields
    member_preamble = (
        "Before any production: review this row's current requirements against its sources and the approved_style_reference, and save the applicable member/collective plan through the existing family-delivery operation (no PX2 family plan exists yet); this member remains missing, not rejected, and no production or collective acceptance is assigned now. "
        "Then, after that plan is saved and under explicit new authorization: "
    )
    for n, aid in (("N02", "queue.working"), ("N03", "queue.retry"), ("N04", "queue.paused")):
        a = asset(proposal, aid)
        old = a["next"]
        prefix = "After the style decision is saved: "
        if not old.startswith(prefix):
            sys.exit(f"unexpected next prefix for {aid}")
        new = member_preamble + old[len(prefix):]
        a["next"] = new
        ledger_changes.append({
            "id": n, "asset_id": aid, "path": f"assets[id={aid}].next", "operation": "replace",
            "old": old, "new": new, "hash_covered": False,
            "reason": "The style decision is now saved, so the old 'After the style decision is saved' trigger is stale; state the family-delivery plan-before-production order explicitly for this member. Requirements, references, delivery checks and dependencies untouched.",
        })

    prop_rel = f"{REL}/plar-update-proposal.json"
    with open(os.path.join(ROOT, prop_rel), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(proposal, fh, indent=2)
        fh.write("\n")

    # sanity: everything except the changed fields is identical
    check = copy.deepcopy(proposal)
    for aid in ("queue.ready", "queue.working", "queue.retry", "queue.paused"):
        asset(check, aid)["next"] = asset(plar, aid)["next"]
    asset(check, "queue.ready")["evidence"] = asset(plar, "queue.ready")["evidence"]
    if check != plar:
        sys.exit("proposal differs from plar.txt outside the ledgered fields")

    ledger = {
        "version": 1,
        "role": "specialist PLAR change ledger (proposal only; the caller performs pixl_plar_save)",
        "recorded_at": correction["recorded_at"],
        "base": {"path": plar_rel, "sha256": plar_hash, "queue_ready_requirements_hash": EXPECTED_REQ_HASH},
        "proposal": {"path": prop_rel, "sha256": sha(prop_rel)},
        "measurement_correction": {"path": corr_rel, "sha256": corr_hash},
        "changes": ledger_changes,
        "hash_covered_changes": [],
        "requirements_hash_expected_unchanged": True,
        "considered_and_left_unchanged": [
            {"path": "assets[id=queue.ready].requirements[property=approved_style_reference].value.scope", "text": "... about 2 px perpendicular stroke (3-pixel runs on 45-degree diagonals; 2-pixel orthogonal strokes) ...", "decision": "KEEP. This describes stroke construction, which the correction re-measures as true: the 3-pixel runs step one column per row on 45-degree staircases between the caps and the merge (perpendicular thickness 3/sqrt(2) = 2.12 px). It does not assert that the arm axes through the tapered tips are 45 degrees. Changing it would alter a requirements_hash-covered field without a factual defect."},
            {"path": "assets[id=queue.working|queue.retry|queue.paused].references[source=ready-sample].instructions", "text": "... about 2 px perpendicular strokes (3-pixel runs on 45-degree diagonals, 2-pixel orthogonals) ...", "decision": "KEEP for the same reason; hash-covered reference text describing stroke construction."},
            {"path": "assets[id=queue.ready].requirements[*]", "decision": "KEEP. No requirement text states the 45-degree axis or 4:8 axis-step claim; the defective explanation lives only in work/ review artifacts and is corrected by the new evidence link."},
            {"path": "assets[id=queue.ready].status", "decision": "KEEP in_progress (unchanged)."},
            {"path": "coverage, sources, delivery.checks, depends_on, questions, production", "decision": "KEEP (unchanged)."},
        ],
        "history_preserved": ["work/queue.ready-reassessment/art-assessment.json", "work/render-stage-pixl/render-review.json", "work/render-recheck-review/caller-style-decision.json", "FAMILY-RESULT.json", "RENDER-RECHECK-RESULT.json", ".pixl/ (state revision 14, hash 7a97831f...)", "plar.txt (bb997899...; the runtime retains the previous bytes on save)"],
    }
    ledger_rel = f"{REL}/plar-change-ledger.json"
    with open(os.path.join(ROOT, ledger_rel), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(ledger, fh, indent=2)
        fh.write("\n")

    report = {
        "artifacts": {
            rel: {"sha256": sha(rel), "bytes": size(rel)}
            for rel in (measure_script, f"{REL}/build-artifacts.py", corr_rel, prop_rel, ledger_rel)
        },
        "all_expected_values_reproduced": correction["quoted_polyline_computation"]["all_expected_values_reproduced"],
        "quoted_sources": sources_quoted,
    }
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
