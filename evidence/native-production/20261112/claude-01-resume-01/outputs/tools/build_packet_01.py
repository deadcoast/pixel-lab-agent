"""Build the packet-01 request/criteria artifacts for CF-10 robot.directions.

Writes exact JSON files under work/native-production/packet-01 and computes
their SHA-256 into request-review.json. No provider call, no credentials.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = ROOT / "work/native-production/packet-01"
OUT.mkdir(parents=True, exist_ok=True)

UPLOAD_REF = "upload:57ceb659-b047-49e5-9250-58343f194c5f"
ROBOT_SHA = "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7"
REQ_HASH = "de0268290f5cc14b5e6e1d9493f21e8767ca2a83ad231d5620b4086d5ddbddd0"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(name, obj):
    p = OUT / name
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


# ---------------------------------------------------------------- schema
# Transcribed from the mcp__pixellab__create_object_pro_flash declaration
# exposed by the host's PixelLab MCP connection in this session.
PALETTE_DESC = ("Target palette, 2 to 256 hex colours as a JSON array, e.g. [\"#081820\", \"#346856\", "
                "\"#88c070\", \"#e0f8d0\"] for Game Boy or [\"#000000\", \"#ffffff\"] for 1-bit. Every pixel "
                "the tool draws is one of them; pixels you supplied (a direction you drew) stay as they are.")
MAXC_DESC = ("At most this many colours (2-64). With a palette, they are picked from it. On the three tools "
             "that have a standard mode — create_character, create_topdown_tileset, animate_object — ANY "
             "palette setting needs mode='pro': standard refuses palette and max_colors, alone or together. "
             "Every other tool taking them has no standard mode and accepts them always.")
STYLE_DESC = ("Style anchor. Exactly ONE of its three sources: `url` also accepts an `upload:<id>` from "
              "get_upload_url or a data: URL, and `source_image_id` is an image you own (what a Pro Flash job "
              "returns). It must fit INSIDE the output canvas both ways — a larger one is refused, so crop it; "
              "resizing pixel art is never the answer. Reuse one anchor across calls to keep a set consistent.")
WIDTH_DESC = ("Defaults to 64 for text creation. Native sizes: 16x16 (experimental), 24x24, 32x32, 32x48, "
              "48x48, 64x64, 96x64, 96x96, 128x128. Custom size (Beta): integer width 16–256 and height 16–256. "
              "Both dimensions must be multiples of 4 pixels. Pixel-grid recovery uses image-to-pixel-art with "
              "fixer when needed. No native image resizing.")
SCHEMA = {
    "additionalProperties": False,
    "properties": {
        "description": {"maxLength": 2000, "minLength": 1, "type": "string"},
        "first_frame_base64": {"default": None, "type": ["string", "null"]},
        "first_frame_direction": {"const": "south", "default": "south", "type": "string"},
        "first_frame_url": {"default": None, "type": ["string", "null"]},
        "height": {"default": None, "maximum": 256, "minimum": 16, "multipleOf": 4, "type": ["integer", "null"]},
        "max_colors": {"default": None, "description": MAXC_DESC, "maximum": 64, "minimum": 2, "type": ["integer", "null"]},
        "n_directions": {"default": 8, "enum": [1, 8], "type": "integer"},
        "name": {"default": "", "type": "string"},
        "palette": {"default": None, "description": PALETTE_DESC, "items": {"type": "string"}, "type": ["array", "null"]},
        "palette_name": {"default": None, "description": "Optional name of the palette (e.g. 'Game Boy', 'PICO-8'); naming it helps the look. It only LABELS the colours you pass in palette rather than looking any up, so it cannot be sent on its own.", "maxLength": 100, "type": ["string", "null"]},
        "seed": {"default": 0, "minimum": 0, "type": "integer"},
        "source_image_id": {"default": None, "type": ["string", "null"]},
        "style_image": {
            "additionalProperties": False, "default": None, "description": STYLE_DESC,
            "properties": {
                "base64": {"default": None, "type": ["string", "null"]},
                "source_image_id": {"default": None, "type": ["string", "null"]},
                "url": {"default": None, "type": ["string", "null"]},
                "usage_description": {"default": None, "description": "How this reference should guide appearance.", "type": ["string", "null"]},
            },
            "type": ["object", "null"],
        },
        "style_options": {
            "additionalProperties": False, "default": None,
            "description": "Choose which visual traits to copy from the style image.",
            "properties": {
                "color_palette": {"default": True, "type": "boolean"},
                "detail": {"default": True, "type": "boolean"},
                "outline": {"default": True, "type": "boolean"},
                "shading": {"default": True, "type": "boolean"},
            },
            "type": ["object", "null"],
        },
        "view": {"default": "low top-down", "enum": ["low top-down", "high top-down", "side"], "type": "string"},
        "width": {"default": None, "description": WIDTH_DESC, "maximum": 256, "minimum": 16, "multipleOf": 4, "type": ["integer", "null"]},
    },
    "required": ["description"],
    "type": "object",
}

# ---------------------------------------------------------------- arguments
ARGUMENTS = {
    "description": (
        "Small boxy robot sprite: a dark navy rectangular frame with two square antenna posts rising "
        "from its top corners, a flat teal front panel, and two rectangular pale-yellow eyes. Flat "
        "eye-level pixel art, four colours, no shading or outline gradients. Rotate this exact sprite; "
        "keep its height, width, colours, silhouette and simple box volume in every view."
    ),
    "first_frame_url": UPLOAD_REF,
    "first_frame_direction": "south",
    "n_directions": 8,
    "view": "side",
    "name": "robot-directions CF-10",
    "seed": 0,
}

# ---------------------------------------------------------------- connection
CONNECTION = {
    "provider": "pixellab-mcp",
    "schema": SCHEMA,
    "discovery": {
        "source": "Host MCP connection 'pixellab' (https://api.pixellab.ai/mcp): tool declaration mcp__pixellab__create_object_pro_flash read in-session; search_help(tool='create_object_pro_flash'); get_pro_flash_capabilities(operation='object', width=32, height=32, n_directions=8); get_upload_url + POST of the exact source bytes",
        "observed_at": "2026-11-12T08:08:04+00:00",
        "evidence": {
            "declaration": "inputSchema transcribed verbatim from the host tool declaration (see schema)",
            "capabilities_quote": {
                "revision": "pro-flash-presets-48-128-2026-09-29",
                "operation": "object", "width": 32, "height": 32, "n_directions": 8,
                "cost": {"image": 5, "rotations": 1, "total": 6, "provisional": True},
                "note": "Reusing a first frame bills only the rotation part (tool description); expected charge for this call: 1 generation, provisional until the receipt.",
                "rotation_canvas": "Eight views use the square V3 canvas; one direction keeps the native size.",
                "supports_existing_source": True, "includes_first_direction": True,
            },
            "upload": {
                "ref": UPLOAD_REF, "source_path": "assets/robot-base.png", "source_sha256": ROBOT_SHA,
                "width": 32, "height": 32, "n_frames": 1, "expires_in_days": 3,
                "observed_at": "2026-11-12T08:09:03+00:00",
                "raw_response": "work/native-production/upload-response.raw.json",
                "note": "The temporary signed upload URL is deliberately not retained in any artifact; only the returned ref is used.",
            },
            "alternatives_considered": "work/native-production/packet-01/review-context.md#operation-choice",
            "discovery_report": "work/native-production/discovery-01.json",
        },
    },
    "authorization": {
        "scope": "NATIVE-PRODUCTION.md CF-10 useful production of robot.directions through the host's official PixelLab MCP connection; limit 20 subscription generations for the whole assignment including revisions; free upload/discovery/retrieval and deterministic corrections allowed; no deletion, publication or repeated calls for counts",
        "evidence": {
            "document": {"path": "NATIVE-PRODUCTION.md", "sha256": "8a60110ad8fb6fcc31a75b32860432400f1309a46ba7bfbe477a38f37c833b7b", "lines": [43, 60]},
            "balance_start": {"path": "work/native-production/balance-start.json", "generations_remaining": 4984, "observed_at": "2026-11-12T08:06:01+00:00", "assignment_limit_generations": 20},
            "caller": "Claude Code main session delegation message to the named pixl:pixl specialist (this session), 2026-11-12",
        },
    },
}

# ---------------------------------------------------------------- criteria
SRC_BRIEF = {"path": "BRIEF.md", "locator": "Identity, four 32x32 transparent views under assets/robot/, controller labels", "lines": [3, 3]}
SRC_TS_PATHS = {"path": "src/robot.ts", "locator": "robotSprites direction->path map", "lines": [1, 5]}
SRC_TS_CELL = {"path": "src/robot.ts", "locator": "cell 32x32 nearest", "lines": [6, 6]}
SRC_PLAR_DIM = {"path": "production-plar.txt", "locator": "robot.directions dimensions requirement", "lines": [106, 118]}
SRC_PLAR_DIR = {"path": "production-plar.txt", "locator": "robot.directions directions requirement", "lines": [119, 133]}
SRC_PLAR_ALPHA = {"path": "production-plar.txt", "locator": "robot.directions alpha requirement", "lines": [134, 143]}
SRC_PLAR_SAMPLING = {"path": "production-plar.txt", "locator": "robot.directions sampling requirement", "lines": [144, 153]}
SRC_PLAR_CHECKS = {"path": "production-plar.txt", "locator": "robot.directions delivery checks", "lines": [164, 171]}
SRC_PLAR_BASE = {"path": "production-plar.txt", "locator": "robot.base identity requirement and identity reference", "lines": [62, 80]}
SRC_CF10 = {"path": "NATIVE-PRODUCTION.md", "locator": "Useful assignment: preserve south, generate E/N/W, inspect identity/proportions/palette/volume/direction/anchor", "lines": [21, 29]}
SRC_IMG = {"path": "assets/robot-base.png", "locator": "whole 32x32 image; measured: 390 visible px, one 4-connected opaque component, bbox [7,3,25,28) zero-based exclusive, colours #25354a (frame, 180 px), #56b5bc (body, 186 px), #f4dda2 (eyes, 24 px, two 3x4 boxes), 0 fractional-alpha px"}

FACING = {
    "east": "faces the viewer's right (east): the front/eye panel is turned toward the right edge or seen in right profile",
    "north": "is seen from behind (north): the back of the frame with both antenna posts, no eyes or front panel visible",
    "west": "faces the viewer's left (west): the front/eye panel is turned toward the left edge or seen in left profile",
}


def criteria(direction):
    return [
        {"id": "dims", "domain": "mechanical", "mode": "local", "authority": "requirement",
         "check": "The file is a 32x32 RGBA PNG (one frame).",
         "basis": "Brief: four 32x32 views; controller cell 32x32; PLAR dimensions requirement.",
         "scope": f"The {direction} candidate file", "sources": [SRC_BRIEF, SRC_TS_CELL, SRC_PLAR_DIM]},
        {"id": "alpha_transparent", "domain": "mechanical", "mode": "local", "authority": "requirement",
         "check": "Every pixel outside the robot has alpha 0, the robot has at least one opaque pixel, and there is no opaque matte, backdrop or canvas fill behind it.",
         "basis": "Brief: separate transparent PNGs; PLAR alpha requirement 'transparent background'.",
         "scope": f"The {direction} candidate file", "sources": [SRC_BRIEF, SRC_PLAR_ALPHA]},
        {"id": "alpha_binary", "domain": "mechanical", "mode": "local", "authority": "proposal",
         "check": "No pixel has fractional alpha: every alpha value is 0 or 255.",
         "basis": "Specialist choice scoped to this candidate: the source has 0 fractional-alpha pixels and the consumer samples nearest, so a hard edge keeps the swapped facings consistent. Not an owner requirement; a fringe pixel is a candidate for deterministic correction, not a rejection of the design.",
         "scope": f"The {direction} candidate as delivered for this sample", "sources": [SRC_IMG, SRC_TS_CELL]},
        {"id": "palette_preserved", "domain": "mechanical", "mode": "local", "authority": "requirement",
         "check": "Every opaque pixel is one of the source's three colours #25354a, #56b5bc, #f4dda2; no new colours are introduced.",
         "basis": "Brief: 'Preserve its subject, proportions, palette'; robot.base identity requirement 'palette'. The exact-set reading (no added shade for a turned face) is the specialist's interpretation of 'preserve palette' and is flagged in choices for the caller.",
         "scope": f"The {direction} candidate file", "sources": [SRC_BRIEF, SRC_PLAR_BASE, SRC_IMG]},
        {"id": "identity", "domain": "visual", "mode": "visual", "authority": "requirement",
         "check": "Viewed at 1x and 3x nearest, the sprite reads as the same robot as assets/robot-base.png: a dark navy rectangular frame with two square antenna posts on top and a teal body panel, with the pale-yellow rectangular eyes wherever the facing shows the front. No added limbs, wheels, extra faces, text or other features, and no redesign.",
         "basis": "Brief: approved identity, do not redesign; robot.base 'Keep this exact south-facing sprite and its subject identity when producing other directions'; CF-10 identity inspection.",
         "scope": f"The {direction} candidate compared with the source at native and 3x", "sources": [SRC_BRIEF, SRC_PLAR_BASE, SRC_CF10, SRC_IMG]},
        {"id": "proportions_volume", "domain": "visual", "mode": "visual", "authority": "requirement",
         "check": "The sprite keeps the source's height (antenna tops about row 3, base about row 27, 25 px tall, within 1 px) and reads as the same simple box volume turned to the named facing; it is not stretched, shrunk, squashed or re-proportioned, and the antennae keep their post size.",
         "basis": "Brief: preserve proportions; CF-10: inspect proportions and volume; PLAR delivery check 'identity, volume and alignment together'.",
         "scope": f"The {direction} candidate compared with the source at native and 3x", "sources": [SRC_BRIEF, SRC_CF10, SRC_PLAR_CHECKS, SRC_IMG]},
        {"id": "direction", "domain": "visual", "mode": "visual", "authority": "requirement",
         "check": f"The sprite {FACING[direction]}. It is not the south frame copied, and it is not another facing mislabelled.",
         "basis": "Controller maps this filename to this facing; brief: keep direction labels aligned with the controller; CF-10: inspect direction.",
         "scope": f"The {direction} candidate", "sources": [SRC_TS_PATHS, SRC_BRIEF, SRC_PLAR_DIR, SRC_CF10]},
        {"id": "anchor_alignment", "domain": "visual", "mode": "visual", "authority": "requirement",
         "check": "Shown in the same 32x32 cell as the south frame (1x and 3x), the sprite stands on the same ground line and is centred like the source, so swapping facings in the controller does not visibly jump or float.",
         "basis": "PLAR delivery check 'alignment'; CF-10: inspect anchor/alignment; consumer swaps files in one fixed cell.",
         "scope": f"The {direction} candidate beside the south frame", "sources": [SRC_PLAR_CHECKS, SRC_CF10, SRC_TS_CELL]},
        {"id": "ground_line_measure", "domain": "mechanical", "mode": "local", "authority": "proposal",
         "check": "Measured on the visible bounding box (zero-based, exclusive bottom/right): bottom == 28 (last opaque row 27, as the source) and |(left + right) / 2 - 16| <= 1 (source box [7,25) has centre 16).",
         "basis": "Specialist measurement proxy supporting anchor_alignment; the 1 px tolerance is the specialist's choice, not an owner rule.",
         "scope": f"The {direction} candidate file", "sources": [SRC_IMG, SRC_PLAR_CHECKS]},
    ]


CANDIDATE_PLAN = {
    "version": 1,
    "scope": "Representative rotation sample for robot.directions: east, north and west candidates generated by one official reference-conditioned rotation of the exact approved south frame (south itself is preserved, not generated)",
    "outputs": [
        {"id": d, "name": f"Robot facing {d}", "kind": "sprite",
         "contract": {"size": [32, 32], "palette": [], "view": "side", "sampling": "nearest", "alpha": "binary",
                      "intent": f"Transparent 32x32 {d}-facing view of the approved robot, same identity, palette and volume as assets/robot-base.png, destined for assets/robot/{d}.png. 'side' view and binary alpha are scoped specialist choices (see request-review choices); size, transparency, nearest sampling and the direction set are owner/consumer requirements."},
         "criteria": criteria(d)}
        for d in ("east", "north", "west")
    ],
}

SOUTH_PLAN = {
    "version": 1,
    "scope": "South baseline: reuse of the exact approved identity bytes as assets/robot/south.png (sample task, no provider call). Authored after caller comparison as the family baseline.",
    "outputs": [{
        "id": "south", "name": "Robot facing south (preserved)", "kind": "sprite",
        "contract": {"size": [32, 32], "palette": [], "view": "side", "sampling": "nearest", "alpha": "binary",
                     "intent": "Byte-identical copy of assets/robot-base.png at assets/robot/south.png."},
        "criteria": [
            {"id": "bytes_identical", "domain": "mechanical", "mode": "local", "authority": "requirement",
             "check": "assets/robot/south.png is byte-identical to assets/robot-base.png (sha256 d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7).",
             "basis": "CF-10: preserve its exact south PNG bytes; renderer README requires the south file to preserve the exact base bytes.",
             "scope": "The delivered south file", "sources": [SRC_CF10, {"path": "renderer-native/README.md", "locator": "south must preserve the exact base bytes", "lines": [25, 27]}]},
            {"id": "identity", "domain": "visual", "mode": "visual", "authority": "requirement",
             "check": "Viewed at 1x and 3x the file shows the approved robot identity unchanged.",
             "basis": "Brief: approved identity; robot.base identity requirement.",
             "scope": "The delivered south file", "sources": [SRC_BRIEF, SRC_PLAR_BASE]},
        ],
    }],
}

FAMILY_DRAFT = {
    "version": 1,
    "status": "draft for pixl_production_plan after the sample is reviewed; not yet authored in state",
    "members_in_order": ["south (baseline sample output, reused bytes)", "east", "north", "west"],
    "destinations": {
        "paths": {"south": "assets/robot/south.png", "east": "assets/robot/east.png", "north": "assets/robot/north.png", "west": "assets/robot/west.png"},
        "sampling": "nearest", "cell": [32, 32],
        "source": "src/robot.ts lines 1-7 (requirement)",
    },
    "collective_criteria": [
        {"id": "continuity", "domain": "continuity", "mode": "visual", "authority": "requirement",
         "check": "Viewed together at 1x and 3x in one 32x32 cell each, the four facings share the same robot: equal height and ground line, the same navy frame/teal body/pale-yellow eye colours, consistent antenna posts, and a box volume that turns coherently S->E->N->W without a facing looking like a different object or size.",
         "basis": "Brief identity/proportions/palette; PLAR delivery check 'identity, volume and alignment together'."},
        {"id": "direction_mapping", "domain": "continuity", "mode": "visual", "authority": "requirement",
         "check": "Each file at the controller path spriteFor(facing) shows that facing: south front, east right, north back, west left.",
         "basis": "src/robot.ts mapping; brief 'Keep direction labels aligned with the controller'."},
        {"id": "renderer_mechanical", "domain": "engine", "mode": "live", "authority": "requirement",
         "check": "renderer-native/check.py reports pass for the capture made from the delivered files with the unchanged controller (all four facings mapped, 32x32 RGBA transparent, south bytes identical, screenshot pixels match).",
         "basis": "CF-10: run the copied renderer and save exact returned reports; renderer README contract."},
        {"id": "renderer_visual", "domain": "engine", "mode": "visual", "authority": "requirement",
         "check": "destination.png and every 1x/3x cell of the capture, viewed with the image tool, show the four facings rendered crisply (nearest), transparent over the observation background, without resampling blur, cropping or misplacement.",
         "basis": "CF-10: inspect destination.png and all actual 1x/3x cells; acceptance requires actual visual judgment."},
    ],
    "note": "Engine-domain criteria must be live mode in PX2; the visual renderer inspection will be authored as a visual-mode 'other'/'continuity' criterion if the validator refuses engine+visual, keeping the obligation.",
}

DISCOVERY = {
    "observed_clock_utc": {"session_start_read": "2026-11-12T08:07:36Z", "discovery": "2026-11-12T08:08:04Z", "upload": "2026-11-12T08:09:03Z"},
    "host_tools_observed": {"pixellab_mcp": True, "pixl_local_mcp": True},
    "candidate_operations": [
        {"tool": "create_object_pro_flash", "inputs": "first_frame_url=upload:<id> (exact source bytes), n_directions=8, view", "canvas": "32x32 square V3 canvas for eight views", "quoted_cost": "rotations 1 generation (provisional; image part not charged when a first frame is supplied)", "skeleton": "none (object)", "chosen": True},
        {"tool": "create_character (mode v3 + reference_image_url, n_directions 4)", "inputs": "reference_image_url=upload:<id>; south kept as drawn", "canvas": "reference's own 32x32", "cost": "ceil(32*32*8/65536) -> minimum 1 generation", "risk": "search_help reference: v3 assumes a standing humanoid/quadruped body and 'tends to add limbs' to other bodies; this robot has no limbs", "chosen": False, "fallback_rank": 1},
        {"tool": "create_character_pro_flash (first_frame_url)", "cost": "rotations ~1 generation at this size", "risk": "mannequin skeleton template on a limbless box", "chosen": False, "fallback_rank": 2},
        {"tool": "create_character (mode pro, reference_image_url) 'Pro rotate'", "cost": "10 generations", "note": "documented for bodies v3 gets wrong; Pro redraws all 8 directions; affordable once within the 20 limit", "chosen": False, "fallback_rank": 3},
        {"tool": "create_8_direction_object (reference_image_base64)", "cost": "10 generations", "risk": "canvas padded to 34x34 for 32 (per declaration) -> would need cropping to meet 32x32", "chosen": False},
    ],
    "upload": {"ref": UPLOAD_REF, "source_sha256": ROBOT_SHA, "width": 32, "height": 32, "n_frames": 1},
    "schema_source": "mcp__pixellab__create_object_pro_flash declaration (transcribed into packet-01/connection.json)",
}

p_args = dump("provider-arguments.json", ARGUMENTS)
p_conn = dump("connection.json", CONNECTION)
p_plan = dump("candidate-plan.json", CANDIDATE_PLAN)
p_south = dump("south-baseline-plan.json", SOUTH_PLAN)
p_family = dump("family-plan-draft.json", FAMILY_DRAFT)
p_disc = dump("discovery-01.json", DISCOVERY)

SOURCES = [
    {"path": "BRIEF.md", "sha256": sha(ROOT / "BRIEF.md"), "role": "brief (owner requirements: identity, 32x32, four directions, transparent, assets/robot/, controller labels)", "locator": "Request paragraph", "lines": [3, 3]},
    {"path": "src/robot.ts", "sha256": sha(ROOT / "src/robot.ts"), "role": "consumer (direction->path map, 32x32 cell, nearest sampling)", "locator": "whole file", "lines": [1, 7]},
    {"path": "assets/robot-base.png", "sha256": sha(ROOT / "assets/robot-base.png"), "role": "identity reference and preserved south; the exact bytes uploaded as " + UPLOAD_REF, "locator": SRC_IMG["locator"]},
    {"path": "NATIVE-PRODUCTION.md", "sha256": sha(ROOT / "NATIVE-PRODUCTION.md"), "role": "cf10-authority (scope, inspection list, spending limit)", "locator": "Useful assignment and scope/payment sections", "lines": [13, 60]},
    {"path": "production-plar.txt", "sha256": sha(ROOT / "production-plar.txt"), "role": "selected PLAR queue (robot.directions requirements, robot.base identity dependency, delivery checks)", "locator": "robot.base and robot.directions rows", "lines": [44, 178]},
    {"path": "renderer-native/README.md", "sha256": sha(ROOT / "renderer-native/README.md"), "role": "destination renderer contract (south exact bytes, 32x32 RGBA transparent, mapping)", "locator": "Required inputs paragraph", "lines": [25, 31]},
]

PACKET = {
    "version": 1,
    "requirements_hash": REQ_HASH,
    "asset_id": "robot.directions",
    "plar_path": "production-plar.txt",
    "sources": SOURCES,
    "request": {
        "path": "work/native-production/packet-01/provider-arguments.json", "sha256": sha(p_args),
        "kind": "provider_arguments", "tool": "create_object_pro_flash", "provider": "pixellab-mcp",
        "connection": {"path": "work/native-production/packet-01/connection.json", "sha256": sha(p_conn)},
    },
    "criteria": {"path": "work/native-production/packet-01/candidate-plan.json", "sha256": sha(p_plan)},
    "image_inputs": [{
        "role": "identity + south first frame", "local_path": "assets/robot-base.png", "sha256": ROBOT_SHA,
        "request_field": "first_frame_url", "handle": UPLOAD_REF, "handle_kind": "PixelLab upload ref (3-day temporary transport), obtained by POSTing the exact file bytes to get_upload_url at 2026-11-12T08:09:03Z; reply: width 32, height 32, n_frames 1",
        "raw_upload_reply": "work/native-production/upload-response.raw.json",
    }],
    "delivered_scope": {
        "preserved": [{"path": "assets/robot/south.png", "sha256": ROBOT_SHA, "role": "exact copy of assets/robot-base.png (already written, verified identical)"}],
        "generated": ["assets/robot/east.png", "assets/robot/north.png", "assets/robot/west.png"],
        "retained_not_delivered": "south-east, north-east, north-west, south-west views returned by n_directions=8 (kept under work/native-production, not delivered)",
        "family_delivery": "work/native-production/packet-01/family-plan-draft.json",
        "south_baseline": "work/native-production/packet-01/south-baseline-plan.json",
    },
    "choices": [
        {"id": "operation", "where": "request.tool / provider-arguments.json", "choice": "create_object_pro_flash with the exact source as first_frame_url and n_directions=8", "reason": "Cheapest discovered route (rotations only, quoted 1 generation) that takes the actual pixels as the south frame without a humanoid skeleton assumption; the robot is a limbless box, which create_character v3 documents as a body it 'tends to add limbs' to. Fallbacks ranked in discovery-01.json.", "authority": "specialist choice"},
        {"id": "view_side", "where": "provider-arguments.json view; contract.view 'side'", "choice": "view = 'side' (eye level)", "reason": "The source is drawn strictly frontal with no visible top face; an eye-level camera keeps the preserved south consistent with the generated views. 'low top-down' would invent a top surface the south frame does not have. Open to caller correction if the game camera is known to be top-down.", "authority": "specialist choice (proposal)"},
        {"id": "n_directions_8", "where": "provider-arguments.json n_directions", "choice": "8 (tool offers only 1 or 8)", "reason": "East/north/west are only available through the 8-view rotation; the four diagonals are retained but not delivered.", "authority": "tool constraint"},
        {"id": "description_text", "where": "provider-arguments.json description", "choice": "Literal description of the observed source pixels; no new features", "reason": "The tool documents description as guidance beside the first frame; it names only what the image already shows.", "authority": "specialist choice"},
        {"id": "seed_0", "where": "provider-arguments.json seed", "choice": "seed 0 recorded explicitly", "reason": "Reproducibility of the attempt record; a revision would use a different seed.", "authority": "specialist choice"},
        {"id": "alpha_binary", "where": "contract.alpha, criterion alpha_binary", "choice": "binary alpha", "reason": "Matches the source (0 fractional pixels) and nearest sampling; proposal, not an owner rule.", "authority": "specialist choice (proposal)"},
        {"id": "palette_exact_set", "where": "criterion palette_preserved", "choice": "'preserve palette' read as: only the three source colours", "reason": "Most literal reading of the brief; a turned face could arguably use one added shade while still 'preserving the palette' in spirit. The caller may relax this to 'no colours outside the source palette family' if it reads the brief differently.", "authority": "specialist interpretation of an owner requirement"},
        {"id": "tolerances", "where": "criteria proportions_volume, ground_line_measure", "choice": "±1 px height / centre tolerance; bottom row 27", "reason": "Measurement proxies for the owner's qualitative proportion/alignment requirements; the numbers are the specialist's.", "authority": "specialist choice (proposal)"},
        {"id": "sample_then_family", "where": "state plan (review-context.md)", "choice": "One sample-phase generation task (plar_prepare) proves the method; accepted bytes are then reused as production-stage members under a family delivery with the preserved south as baseline; no second paid call unless a revision is needed", "reason": "PX2 family members must be production outputs sharing a sample baseline; the representative sample supplies the adoption proof.", "authority": "specialist choice (process)"},
        {"id": "deferred_family_checks", "where": "family-plan-draft.json", "choice": "Continuity, direction mapping and renderer (engine) checks are family-level, reviewed after all four files exist", "reason": "They cannot pass on a single direction; deferral keeps the obligation scheduled rather than dropped.", "authority": "specialist choice (process)"},
    ],
    "budget": {"assignment_limit_generations": 20, "expected_this_call": 1, "provisional": True, "spent_so_far": 0},
}
p_packet = dump("request-review.json", PACKET)
for p in (p_args, p_conn, p_plan, p_south, p_family, p_disc, p_packet):
    print(sha(p), p.relative_to(ROOT).as_posix())
