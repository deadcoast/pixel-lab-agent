"""Caller-authored comparison of packet-01 against the original sources (CF-10 robot.directions).
Run from the consumer root with the assignment Python using -I. Writes work/native-production/COMPARISON.json.
"""
import json, hashlib, datetime
from pathlib import Path

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

pk = 'work/native-production/packet-01/'
BRIEF = {"path": "BRIEF.md", "lines": [3, 3], "quote": "Preserve its subject, proportions, palette and front-facing south sprite; do not redesign it from a description. The controller needs four 32x32 directional views, south/east/north/west, as separate transparent PNGs under assets/robot/. Keep direction labels aligned with the controller."}
TS = {"path": "src/robot.ts", "lines": [1, 7]}
NP = {"path": "NATIVE-PRODUCTION.md", "lines": [21, 29]}
PL = lambda a, b: {"path": "production-plar.txt", "lines": [a, b]}
RD = {"path": "renderer-native/README.md", "lines": [25, 31]}
outs = ["east", "north", "west"]
rows = []
crit_sha = sha(pk + 'candidate-plan.json')

def row(cid, outputs, obligation, basis, scope, delta, alt, disp, sources):
    for o in outputs:
        rows.append({"output": o, "criterion": cid, "criteria_file_sha256": crit_sha,
                     "source_obligation": obligation, "authority_basis": basis, "scope": scope.format(o=o),
                     "literal_delta": delta, "discriminating_alternative": alt, "disposition": disp,
                     "source_evidence": sources})

row("dims", outs,
    "BRIEF.md:3 'four 32x32 directional views'; src/robot.ts:6 cell 32x32; production-plar.txt:106-118 dimensions [32,32]. Leaves nothing open about size.",
    "Required outcome (owner/consumer).", "The {o} candidate file",
    "Adds 'RGBA' and 'one frame'. README:27 names 'transparent 32x32 RGBA PNG'; one frame is implied by one sprite per controller path.",
    "A 32x32 indexed PNG with a tRNS chunk would be transparent but not literally RGBA; README:27 names RGBA, so the narrowing is supported and harmless.",
    "Keep.", [BRIEF, TS, PL(106, 118), RD])
row("alpha_transparent", outs,
    "BRIEF.md:3 'separate transparent PNGs'; production-plar.txt:134-143 alpha 'transparent background'.",
    "Required outcome (owner/consumer).", "The {o} candidate file",
    "Adds 'at least one opaque pixel' and 'no opaque matte, backdrop or canvas fill'; both restate a visible transparent-background sprite (README:27 'visible transparent').",
    "A fully transparent file satisfies a naive 'transparent' reading but README:27 'visible' excludes it. No valid alternative is rejected.",
    "Keep.", [BRIEF, PL(134, 143), RD])
row("alpha_binary", outs,
    "No source requires binary alpha. src/robot.ts:6 says sampling nearest; the source image has 0 fractional-alpha pixels (caller re-measured).",
    "Scoped specialist proposal; correctly labelled 'proposal'.", "The {o} candidate as delivered for this sample",
    "Adds a rule the brief does not state.",
    "A rotation with a 1-px semi-transparent fringe still meets the brief; the check flags it, but the basis says a fringe is a candidate for deterministic correction, not a design rejection.",
    "Keep as proposal. Its failure must not reject the candidate on its own; an alpha snap, if applied, is recorded as an 'edited' member.", [TS])
row("palette_preserved", outs,
    "BRIEF.md:3 'Preserve its ... palette'; production-plar.txt:62-73 identity 'Preserve the supplied subject, proportions, palette and south frame.' Measured source palette: #25354a (180 px), #56b5bc (186 px), #f4dda2 (24 px), nothing else. The brief does not say whether a turned view may add a shade.",
    "Mixed: 'no colour outside the source palette' is the owner outcome; reading 'preserve' as 'exactly this set, nothing added' is the specialist's interpretation, flagged in choices.palette_exact_set.",
    "The {o} candidate file",
    "Literal check: every opaque pixel is one of the three colours (strictest reading).",
    "An east view adding one darker teal for the side face while keeping the three colours; the check rejects it. In pixel art 'preserve its palette' ordinarily means keep the colour set, so the caller adopts the strict reading for this assignment and records it as a reading, not a quotation.",
    "Keep the strict check. CORRECT THE REQUEST: the discovered declaration (connection.json schema properties.palette / palette_name) accepts hex colours and states every drawn pixel is one of them while supplied pixels stay as they are. Add palette ['#25354a','#56b5bc','#f4dda2'] to provider-arguments so the requirement is met at generation rather than by post-correction. Keep deterministic palette correction as the fallback, recorded as an 'edited' member distinct from raw provider bytes.",
    [BRIEF, PL(62, 80)])
row("identity", ["east", "west"],
    "BRIEF.md:3 'Preserve its subject ... do not redesign'; production-plar.txt:74-80 'Keep this exact south-facing sprite and its subject identity when producing other directions.' The source shows two 4x6 posts at the frame's top corners (columns 7-10 and 21-24, rows 3-8), a teal panel and two 3x4 eyes.",
    "Required outcome (identity, no redesign); the feature list is the specialist's description of the measured source.",
    "The {o} candidate compared with the source at native and 3x",
    "Adds 'two square antenna posts on top' to the identity reading for every facing, plus 'eyes wherever the facing shows the front'.",
    "A correct east profile of a box whose two posts sit at the left and right ends of the front edge: from the side one post occludes the other, so one post (or one with the far one partly visible) is seen. Same robot, no redesign, yet the literal 'two ... posts' clause could reject it. The posts are also 4 wide by 6 tall, not square.",
    "CLARIFY: for east/west require 'the antenna post(s) as visible from that facing (one may hide the other in profile), same post height'; replace 'square' with 'rectangular (4x6 in the source)'. Keep the no-added-features clause.",
    [BRIEF, PL(62, 80), NP])
row("identity", ["north"],
    "Same sources as east/west. The back of the robot is not shown in the source.",
    "Required outcome; the back's appearance is open.",
    "The north candidate compared with the source at native and 3x",
    "Adds 'teal body panel' to the identity reading for a facing whose panel colour the source does not establish.",
    "A north view with the navy frame, both posts, no eyes and either a plain navy back or a teal back: both are consistent with the source; the check should accept either when nothing new is added.",
    "CLARIFY: for north do not require the teal panel; require the frame colour, both posts (both visible from behind), no eyes, no added features.",
    [BRIEF, PL(62, 80), NP])
row("proportions_volume", outs,
    "BRIEF.md:3 'Preserve its ... proportions'; NATIVE-PRODUCTION.md:27-28 inspect proportions and volume; production-plar.txt:168 'Inspect identity, volume and alignment together.' Measured source height rows 3-27 = 25 px.",
    "Mixed: same proportions / not stretched is the owner outcome; 'within 1 px' and 'antennae keep their post size' are the specialist's measurement proxies (choices.tolerances says so, but the criterion carries authority 'requirement').",
    "The {o} candidate compared with the source at native and 3x",
    "Adds a numeric 1-px height tolerance and a post-size clause inside a requirement-labelled criterion.",
    "A profile 2 px shorter that still reads as the same box is rejected by the numeric clause; the owner text alone would not reject it. A clearly squashed view is rejected by both.",
    "CLARIFY: keep the visual outcome as the requirement; move the 25 px / 1 px / post-size numbers into the basis as the specialist's proxy (or a proposal criterion), so the reviewer records visual judgment separately from the measurement.",
    [BRIEF, NP, PL(164, 171)])
row("direction", ["east"],
    "src/robot.ts:1-5 maps east to assets/robot/east.png; BRIEF.md:3 'Keep direction labels aligned with the controller'. The sources do not define what east looks like beyond the name.",
    "Required outcome (controller mapping); 'faces the viewer's right' is the ordinary screen convention and the specialist's reading.",
    "The east candidate",
    "Adds 'front/eye panel turned toward the right edge or seen in right profile' and 'not the south frame copied'.",
    "A mirrored convention (east = viewer's left) would be rejected; nothing in the sources supports it, and README:28 expects each file to match its facing.",
    "Keep.", [TS, BRIEF, PL(119, 133)])
row("direction", ["west"],
    "As east, mirrored: src/robot.ts:1-5 maps west to assets/robot/west.png.",
    "Required outcome; screen-left convention is the specialist's reading.", "The west candidate",
    "Adds 'turned toward the left edge or seen in left profile'.",
    "Same as east; no source-conforming alternative is rejected.", "Keep.", [TS, BRIEF, PL(119, 133)])
row("direction", ["north"],
    "src/robot.ts:1-5 maps north to assets/robot/north.png.",
    "Required outcome; 'seen from behind, no eyes' is the specialist's reading of north for a frontal south.", "The north candidate",
    "Adds 'back of the frame with both antenna posts, no eyes or front panel visible'.",
    "A north view with eyes visible would face the camera and not be north; rightly rejected. 'front panel' wording must not reject a plain back panel (see identity/north).",
    "Keep, with the identity/north clarification.", [TS, BRIEF, PL(119, 133)])
row("anchor_alignment", outs,
    "production-plar.txt:168 'Inspect identity, volume and alignment together.'; NATIVE-PRODUCTION.md:27-28 'anchor/alignment'; src/robot.ts:6 one fixed 32x32 cell.",
    "Required outcome (owner/consumer).", "The {o} candidate beside the south frame",
    "Adds 'same ground line' and 'centred like the source'; both follow from swapping files in one fixed cell without a jump.",
    "A sprite drawn 3 px higher floats when the controller swaps facings; rejecting it serves the consumer.",
    "Keep.", [PL(164, 171), NP, TS])
row("ground_line_measure", outs,
    "No source states numbers; the source's last opaque row is 27 and its box centre is 16.0 (caller re-measured: bbox [7,3,25,28), centre (7+25)/2 = 16).",
    "Scoped specialist proposal; correctly labelled.", "The {o} candidate file",
    "Adds bottom == 28 exclusive and |centre - 16| <= 1.",
    "A valid profile 1 px narrower has centre 16.5 and passes; a 2-px shift fails the proxy but might still look aligned. Proposal only.",
    "Keep as proposal; measured facts verified by the caller in the same zero-based exclusive-edge convention.", [PL(164, 171)])

choices = [
    {"id": "operation", "finding": "create_object_pro_flash declaration (connection.json schema) supports first_frame_url, first_frame_direction=south, n_directions 8, view enum, palette. Host tool text: reusing a first frame bills only the rotation part; capabilities quote image 5 + rotations 1 at 32x32, so 1 generation expected, provisional. Ranked fallbacks (create_character v3+reference 1 gen, pro rotate 10) fit the 20 limit.", "disposition": "Accept as specialist choice. Handle a non-32x32 returned canvas with a free deterministic step and keep raw bytes."},
    {"id": "view_side", "finding": "Source is strictly frontal with no top face (caller viewed 8x). No source names a camera.", "disposition": "Accept as scoped proposal."},
    {"id": "n_directions_8", "finding": "Schema enum [1,8]; E/N/W need 8.", "disposition": "Accept (tool constraint). Extra views retained under work/native-production only."},
    {"id": "description_text", "finding": "Two inaccuracies against the measured source: posts are 4 wide x 6 tall (rectangular), not 'square'; the sprite has three opaque colours plus transparency, and 'four colours' may invite a fourth opaque colour.", "disposition": "CORRECT: 'two rectangular antenna posts' and 'three colours (navy, teal, pale yellow) on a transparent background'."},
    {"id": "seed_0", "finding": "Default seed recorded explicitly.", "disposition": "Accept."},
    {"id": "alpha_binary", "finding": "Proposal, scoped.", "disposition": "Accept as proposal."},
    {"id": "palette_exact_set", "finding": "Caller adopts the strict reading for this assignment and notes the schema's palette argument enforces it at generation.", "disposition": "Accept the reading; CORRECT the request to pass palette."},
    {"id": "tolerances", "finding": "Numbers verified; they sit inside a requirement-labelled criterion (proportions_volume).", "disposition": "CLARIFY attribution as above."},
    {"id": "sample_then_family", "finding": "Process choice consistent with NATIVE-PRODUCTION.md:30-32 (family delivery output/link required).", "disposition": "Accept."},
    {"id": "deferred_family_checks", "finding": "Continuity, mapping and renderer checks scheduled at family level (family-plan-draft.json).", "disposition": "Accept; verify they remain scheduled in the authored plan."},
]

doc = {
    "version": 1,
    "reviewer": "caller (Claude Code main session, model claude-fable-5-1)",
    "reviewed_at": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    "native_child": "aeb8fdd3833c62981 (pixl:pixl)",
    "reviewed_packet": {"path": pk + "request-review.json", "sha256": sha(pk + "request-review.json")},
    "reviewed_request": {"path": pk + "provider-arguments.json", "sha256": sha(pk + "provider-arguments.json")},
    "reviewed_criteria": {"path": pk + "candidate-plan.json", "sha256": crit_sha},
    "reviewed_connection": {"path": pk + "connection.json", "sha256": sha(pk + "connection.json")},
    "evidence_report": {"path": pk + "request-review-report.json", "sha256": sha(pk + "request-review-report.json")},
    "other_reviewed": [{"path": pk + f, "sha256": sha(pk + f)} for f in ["review-context.md", "family-plan-draft.json", "south-baseline-plan.json", "discovery-01.json"]],
    "original_sources_read": [{"path": p, "sha256": sha(p)} for p in ["BRIEF.md", "src/robot.ts", "assets/robot-base.png", "production-plar.txt", "NATIVE-PRODUCTION.md", "renderer-native/README.md"]],
    "independent_measurement": {"tool": "Pillow 13 via the assignment Python with -I, caller script in this session", "image": "assets/robot-base.png d997cade...70aa7", "convention": "zero-based pixels, boxes [left,top,right,bottom) exclusive right/bottom", "visible_px": 390, "fractional_alpha_px": 0, "components_4": 1, "bbox": [7, 3, 25, 28], "colours": {"#25354a": 180, "#56b5bc": 186, "#f4dda2": 24}, "posts": "columns 7-10 and 21-24, rows 3-8 (4x6 each)", "body_box": [9, 11, 23, 26], "eyes": "[11,14,14,18) and [18,14,21,18)", "centre_x_edge_coords": 16.0, "agrees_with_specialist": True},
    "locator_checks": "All 14 text locators opened in the original files at the cited file-local line bounds; the quoted text matches. The image locator was inspected at 1x and 8x (work/native-production/inspect/robot-base-8x.png) and re-measured.",
    "schema_check": "connection.json schema compared with the host declaration of mcp__pixellab__create_object_pro_flash visible to the caller: first_frame_url, first_frame_direction const south, n_directions enum [1,8], view enum, palette/palette_name, seed, name all present; provider-arguments.json uses only declared fields. Host cost text: n_directions=8 total 6 for 16-88 px; 'Reusing a first frame bills only the rotation part'.",
    "provider_image_input_check": "upload-response.raw.json shows ref upload:57ceb659-b047-49e5-9250-58343f194c5f, 32x32, 1 frame; the packet binds it to the source hash. The signed URL is not retained. The caller did not re-upload.",
    "delivered_scope_check": "assets/robot/south.png exists and hashes d997cade...70aa7 (byte-identical). East/north/west destinations, the family delivery draft and retained extra views are all stated.",
    "criterion_comparisons": rows,
    "choice_comparisons": choices,
    "result": "changes_requested",
    "changes_requested": [
        "1. provider-arguments: add palette ['#25354a','#56b5bc','#f4dda2'] (palette_name optional) per the declared schema; this enforces palette_preserved at generation.",
        "2. provider-arguments description: 'two rectangular antenna posts' (not square); 'three colours on a transparent background' (not four colours).",
        "3. candidate-plan identity (east, west): allow one post to occlude the other in profile; say rectangular. identity (north): do not require the teal panel; require both posts, no eyes, no added features.",
        "4. candidate-plan proportions_volume: keep the visual requirement; attribute the 25 px / 1 px / post-size numbers to the specialist proxy (basis or a proposal criterion).",
        "5. Keep packet-01 unchanged; save packet-02 with the corrected files, re-run pixl_request_review on it, and bind the prepared job to the corrected request before dispatch (new state revision if the stored request changes)."
    ],
    "consistent_after_corrections": "Expected consistent once the five changes are visible in packet-02; the caller re-reads packet-02 before confirming.",
    "not_established": "Contract consistency is not provider execution, visual quality or destination acceptance. M1/M2 and broader M3 remain open.",
    "next_action": "Send these findings to agent aeb8fdd3833c62981; read packet-02; then authorize dispatch."
}
out = Path('work/native-production/COMPARISON.json')
out.write_text(json.dumps(doc, indent=2), encoding='utf-8')
print(sha(out), len(rows))
