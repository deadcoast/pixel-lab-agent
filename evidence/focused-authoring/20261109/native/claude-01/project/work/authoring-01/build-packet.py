"""Build the exact stage packet and rotation policy for authoring-01.working.

Run from the project root with the selected Python (-I). The seed base64 is
computed from the retained artifact bytes and verified to round-trip to the
same sha256; nothing is hand-typed. No provider call is made.
"""
import base64
import datetime
import hashlib
import json

from PIL import Image

SEED = (
    ".pixl/assets/queue.ready/artifacts/"
    "21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png"
)
TOOL = "mcp__pixellab__pixelart_workbench"


def sha(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


raw = open(SEED, "rb").read()
seed_sha = hashlib.sha256(raw).hexdigest()
b64 = base64.b64encode(raw).decode("ascii")
assert hashlib.sha256(base64.b64decode(b64)).hexdigest() == seed_sha
data_url = "data:image/png;base64," + b64

discovery_doc = json.load(open("official-discovery.json", encoding="utf-8"))
declaration = next(t for t in discovery_doc["tools"] if t["name"] == TOOL)
now = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()

notes = (
    "Working queue status strip (queue.working -> authoring-01.working): step 1 of a "
    "two-step deterministic official construction from the accepted 16x16 seed "
    "live.working-seed.candidate (sha256 " + seed_sha + "). Join four copies of the exact "
    "seed bytes, supplied as data:image/png;base64 URLs, into one 64x16 horizontal sheet: "
    "4 columns x 1 row, no scaling, no redraw, no new pixels. Step 2 (a separate job on the "
    "same stage, prepared only after this result is reviewed) applies guarded patch_pixels "
    "to sheet cells 2, 3 and 4 so they hold the seed rotated 90, 180 and 270 degrees "
    "clockwise about canvas centre (7.5,7.5) via dst(x,y)=src(y,15-x) per quarter-turn; "
    "cell 1 remains the seed at 0 degrees. Why not animate_image: the retained AI animation "
    "of this same seed (job live.working-animation-01.job) returned five frames whose "
    "selected frames morphed and near-held across phases 2/3, jumped at the wrap, and one "
    "frame carried 193 opaque #808080 background pixels; the accepted motion "
    "live.working-animation-motion-01.candidate is exactly these clockwise quarter-turns, "
    "which this construction reproduces without a paid generation. Review obligations for "
    "this step's result (preparation is not acceptance): output exactly 64x16 with cells at "
    "x=0,16,32,48 and no gutters, padding or added canvas; every cell pixel-identical to the "
    "seed including an alpha-0 exterior; measure how the workbench represents transparent "
    "pixels before composing step 2 expected values. Later obligations: step-2 pixel-exact "
    "rotation check, native/3x frame review, live 100 ms playback with the 4->1 wrap, family "
    "distinction, and both statusCell/compactStatus consumers."
)

schema = {
    "type": "object",
    "properties": {
        "argv": {
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
                {"type": "null"},
            ]
        },
        "mode": {"type": "string", "enum": ["low", "high"]},
        "notes": {"type": ["string", "null"]},
    },
    "additionalProperties": False,
}

packet = {
    "version": 1,
    "inputs": {
        "live.seed.output": {"candidate": "live.working-seed.candidate", "sha256": seed_sha}
    },
    "request": {
        "provider": "pixellab-official-mcp",
        "tool": TOOL,
        "arguments": {
            "argv": [
                "join", data_url, data_url, data_url, data_url,
                "--as", "sheet", "--columns", "4",
            ],
            "mode": "low",
            "notes": notes,
        },
        "schema": schema,
        "discovery": {
            "source": (
                "Current connected official PixelLab MCP tool declaration retained in "
                "official-discovery.json (host-exposed declaration text; not a raw "
                "tools/list dump)"
            ),
            "observed_at": now,
            "evidence": {
                "declaration_path": "official-discovery.json",
                "declaration_sha256": sha("official-discovery.json"),
                "declaration_name": TOOL,
                "declaration_recorded_observation": discovery_doc["observed_at"],
                "declaration_text": declaration["description"],
                "schema_representation": (
                    "JSON Schema projection of the exposed TypeScript argument declaration: "
                    "argv string | string[] | null, mode 'low' | 'high', notes string | null; "
                    "additionalProperties false"
                ),
                "subject_transport": (
                    "Each argv subject is a data:image/png;base64 URL of the exact retained "
                    "seed bytes (declaration: a subject is an id or an image reference, "
                    "including a data URL, an https link or base64; never a file path). "
                    "Base64 computed from the artifact file and verified to round-trip to "
                    "the same sha256."
                ),
                "official_docs": discovery_doc["official_docs"],
            },
        },
        "authorization": {
            "scope": (
                "User-authorized useful official PixelLab operations for Working, Retry, "
                "Paused and collective family review in this retained consumer "
                "(PRODUCTION-STAGE.md), carried into the isolated authoring branch by "
                "AUTHORING-STAGE.md, which assigns request preparation and recovery only: "
                "no remote generation call and no dispatch claim in this continuation. The "
                "workbench pixel tools are declared free for subscribers; this step requests "
                "no paid generation."
            ),
            "evidence": {
                "source": "PRODUCTION-STAGE.md",
                "sha256": sha("PRODUCTION-STAGE.md"),
                "continuation": "AUTHORING-STAGE.md",
                "continuation_sha256": sha("AUTHORING-STAGE.md"),
                "user_request": (
                    "Choose and prepare Working's next executable official PixelLab "
                    "operation from the retained seed and current declarations in "
                    "official-discovery.json; include actual input image bytes via a "
                    "supported data/base64 input; do not call a remote generation tool."
                ),
            },
        },
    },
}

body = json.dumps(packet, indent=2, ensure_ascii=False) + "\n"
open("work/authoring-01/stage-packet.json", "w", encoding="utf-8").write(body)
canonical = json.dumps(
    packet, sort_keys=True, separators=(",", ":"), ensure_ascii=False
).encode("utf-8")

# Rotation policy and the exact step-2 patch list.
image = Image.open(SEED).convert("RGBA")
pixels = image.load()
src = {(x, y): pixels[x, y] for x in range(16) for y in range(16)}


def rotate_cw(frame):
    return {(x, y): frame[(y, 15 - x)] for x in range(16) for y in range(16)}


frames = [src]
for _ in range(3):
    frames.append(rotate_cw(frames[-1]))


def hex_rgba(color):
    return "#%02x%02x%02x%02x" % color


patches = []
for k in range(1, 4):
    for y in range(16):
        for x in range(16):
            if frames[k][(x, y)] != src[(x, y)]:
                patches.append([16 * k + x, y, hex_rgba(src[(x, y)]), hex_rgba(frames[k][(x, y)])])

accepted = Image.open("work/live-family/working-animation-motion-01.png").convert("RGBA")
accepted_px = accepted.load()
diffs = [
    sum(
        1
        for x in range(16)
        for y in range(16)
        if accepted_px[16 * k + x, y] != frames[k][(x, y)]
        and (accepted_px[16 * k + x, y][3] or frames[k][(x, y)][3])
    )
    for k in range(4)
]

policy = {
    "stage": "authoring-01.working",
    "output": "authoring-01.working.output",
    "seed_candidate": "live.working-seed.candidate",
    "seed_sha256": seed_sha,
    "destination": {
        "path": "assets/working.png",
        "width": 64,
        "height": 16,
        "cells": [[0, 0, 16, 16], [16, 0, 16, 16], [32, 0, 16, 16], [48, 0, 16, 16]],
        "frame_ms": 100,
        "frame_index": (
            "floor(elapsed/100) mod 4 (src/queue-view.ts display.frameMs with frames 4; "
            "renderer/view.mjs paint)"
        ),
    },
    "step_1": {
        "job": "authoring-01.working.join-01",
        "operation": "pixelart_workbench join <seed> <seed> <seed> <seed> --as sheet --columns 4",
        "expected_result": (
            "one 64x16 sheet of four identical seed cells; no gutters, padding, scaling or recolor"
        ),
        "frame_selection": (
            "no selection from a larger frame set is expected; the result is the destination "
            "geometry itself"
        ),
        "if_result_differs": (
            "retain the raw provider output; do not resize, crop-and-guess or silently drop or "
            "duplicate frames; either re-request join with corrected flags or perform a "
            "documented lossless cell extraction recording exact source rectangles in play "
            "order, each verified pixel-equal to the seed"
        ),
    },
    "step_2": {
        "job": "next distinct job id on the same stage, after step 1 is reviewed",
        "operation": (
            "pixelart_workbench edit <step-1 id> --changes [patch_pixels on layer image, frames [1]]"
        ),
        "rotation": (
            "clockwise quarter-turns about canvas centre (7.5,7.5): dst(x,y)=src(y,15-x) per "
            "90 degrees; cell k holds cw^k(seed) for k=0..3"
        ),
        "verified_against": (
            "work/live-family/working-animation-motion-01.png: visible-pixel differences per "
            "cell versus cw^k(seed) = " + json.dumps(diffs) + " (counter-clockwise differs, so "
            "the direction is pinned)"
        ),
        "patch_count": len(patches),
        "transparent_expected_assumption": (
            "#00000000 (all 224 transparent seed pixels are RGBA 0,0,0,0); if the workbench "
            "reports transparent pixels differently after join (for example #80808000 as in "
            "the earlier AI-output edit), regenerate only the expected column before step 2"
        ),
        "patches": patches,
    },
    "play_order": (
        "cell 0 -> 1 -> 2 -> 3 -> 0; every step including the wrap is a further 90 degree "
        "clockwise turn, so angular velocity is uniform and the loop boundary is not a special case"
    ),
    "separate_review_obligations": [
        "mechanical: 64x16, four cells, alpha-0 exterior, no gutters",
        "pixel-exact: each delivered cell equals cw^k(seed) (local check)",
        "visual: native and 3x on #172336, every frame and live 100 ms playback with wrap; "
        "activity never reads as success; cluster count and volume stable",
        "family: grayscale/non-color distinction against Ready, Retry, Paused and Start",
        "engine: started->running through stateAfter, both statusCell and compactStatus, "
        "nearest 1x/3x, observed frame advance",
    ],
    "not_claimed": ["acceptance", "dispatch", "remote execution"],
}
policy_body = json.dumps(policy, indent=2) + "\n"
open("work/authoring-01/working-rotation-policy.json", "w", encoding="utf-8").write(policy_body)

print("seed sha256", seed_sha)
print("base64 length", len(b64), "data url length", len(data_url))
print("observed_at", now)
print("packet file sha256", hashlib.sha256(body.encode("utf-8")).hexdigest())
print("packet canonical sha256", hashlib.sha256(canonical).hexdigest())
print("policy file sha256", hashlib.sha256(policy_body.encode("utf-8")).hexdigest())
print("step-2 patches", len(patches), "accepted-motion diffs", diffs)
