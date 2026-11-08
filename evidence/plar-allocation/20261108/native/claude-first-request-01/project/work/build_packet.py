"""Build the queue.ready first-request packet artifacts (local helper, no network)."""
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
REQUIREMENTS_HASH = "79b08da5e8de765a407696cc8bb0da0414d538b953d82ae29e1c4117ffbe93f8"
PLAR_HASH = "3901a2e7cea7eea6bc616715c64962f665e93a2b0804bcf9dfd45a51f1d0ac56"
TOOL = "create_image_pro_flash"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name: str, obj) -> Path:
    p = WORK / name
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return p


arguments = {
    "description": (
        "16x16 pixel art UI status icon meaning Ready / completed successfully: "
        "one bold checkmark silhouette, centered with a small margin, in a cool light-blue "
        "accent (around #70b9ed) with slightly lighter and deeper blue shading for form, "
        "high contrast against a dark navy UI panel (#172336). Clean hard-edged pixel "
        "clusters, simple readable shape at 1x, no text, no circle or badge behind the "
        "check, no spinner, arrows, cross or pause bars, transparent background."
    ),
    "width": 16,
    "height": 16,
    "no_background": True,
    "seed": 1108,
}

B = "BRIEF.md"
V = "src/queue-view.ts"
Q = "src/queue.ts"
S = "assets/start.svg"
P = "plar.txt"

criteria = {
    "version": 1,
    "scope": (
        "First representative Ready sample for queue.ready, for style review before "
        "Working/Retry/Paused family expansion. Candidate work only: no style is approved, "
        "and renderer integration of assets/ready.png is outside this sample's acceptance."
    ),
    "outputs": [{
        "id": "ready",
        "name": "Ready status sample (assets/ready.png candidate)",
        "kind": "sprite",
        "contract": {
            "size": [16, 16],
            "palette": [],
            "view": "ui",
            "sampling": "nearest",
            "alpha": "full",
            "intent": (
                "Owner requirements: static single-frame 16x16 Ready/success status image, "
                "transparent background, readable pixel-art silhouette at 1x and 3x nearest "
                "on the #172336 panel, existing cool-blue UI accent, no fixed palette (empty "
                "palette), alpha not restricted to binary. Observation: Start SVG accent "
                "#70b9ed (color cue, not an exact-color rule). Specialist sample choice: a "
                "bare checkmark motif without badge/circle, prompt-only (no style reference "
                "exists and the discovered tool has no image input)."
            ),
        },
        "criteria": [
            {
                "id": "geometry",
                "check": "Decoded candidate PNG is exactly 16x16 pixels and a single static frame.",
                "domain": "mechanical", "mode": "local",
                "basis": "Owner/consumer requirement: 16x16 logical cells; Ready is static; consumer declares frames: 1.",
                "scope": "This candidate file's decoded bytes.",
                "sources": [
                    {"path": B, "locator": "Status cells are 16 by 16 logical pixels; Ready and Retry are static images"},
                    {"path": V, "locator": "statusVisuals.succeeded frames: 1; display.cell [16, 16] (lines 10, 13)"},
                ],
            },
            {
                "id": "transparent_background",
                "check": "Background area is fully transparent with no opaque matte or filled backdrop; partial alpha is permitted (no binary-alpha rule).",
                "domain": "mechanical", "mode": "local",
                "basis": "Owner requirement: transparent backgrounds. Binary alpha is not required by any source.",
                "scope": "This candidate file's alpha channel outside the subject.",
                "sources": [{"path": B, "locator": "Use transparent backgrounds"}],
            },
            {
                "id": "readability",
                "check": "Viewed at 1x and 3x nearest-neighbor over #172336, the subject is a readable pixel-art silhouette with clean edges (not muddy, noisy or lost against the panel).",
                "domain": "visual", "mode": "visual",
                "basis": "Owner requirement: readable silhouettes inspected at 1x and 3x nearest on the actual dark panel; consumer display scale 3, filter nearest, background #172336.",
                "scope": "This candidate at the declared display conditions.",
                "sources": [
                    {"path": B, "locator": "readable silhouettes ... Inspect at 1x and 3x nearest display scale on the actual dark panel"},
                    {"path": V, "locator": "display scale: 3, filter: \"nearest\", background: \"#172336\" (line 13)"},
                ],
            },
            {
                "id": "success_meaning",
                "check": "The image reads as Ready / successful completion, not as activity/in-progress, failure/retry, or paused.",
                "domain": "visual", "mode": "visual",
                "basis": "Owner/consumer requirement: an ok result becomes succeeded, shown with label Ready; the working loop must not look like success; error/retry and paused must be distinguishable from completion.",
                "scope": "This candidate judged on its own; no other family member exists yet.",
                "sources": [
                    {"path": Q, "locator": "stateAfter: ok -> succeeded (line 3)"},
                    {"path": V, "locator": "statusVisuals.succeeded label Ready, path assets/ready.png (line 10)"},
                    {"path": B, "locator": "The working loop must communicate activity without looking like success; paused ... distinguishable from activity, completion and retry"},
                ],
            },
            {
                "id": "cool_blue_accent",
                "check": "The dominant color treatment uses the existing UI's cool-blue accent family; any exact hex, color count or shading ramp is not a rejection rule.",
                "domain": "visual", "mode": "visual",
                "basis": "Owner requirement: existing UI cool blue accent, no fixed palette. #70b9ed is an observation from the Start SVG used as a cue only.",
                "scope": "This candidate's color treatment.",
                "sources": [
                    {"path": B, "locator": "the existing UI's cool blue accent; a fixed palette is not required"},
                    {"path": S, "locator": "path fill=\"#70b9ed\""},
                ],
            },
            {
                "id": "family_sample_suitability",
                "check": "Silhouette, edge handling and color treatment are reviewed and recorded as a usable (or rejected) shared treatment for later Working/Retry/Paused members.",
                "domain": "visual", "mode": "visual",
                "basis": "Owner requirement to propose a representative status sample before expanding the family; Ready as the sample is a PLAR proposal (family_sample).",
                "scope": "This sample's suitability as a family reference; it does not approve a style or the family.",
                "sources": [
                    {"path": B, "locator": "No approved style reference exists yet: propose a representative status sample before expanding the family"},
                    {"path": P, "locator": "queue.ready requirements family_sample (proposal); questions[0]"},
                ],
            },
            {
                "id": "motif_checkmark",
                "check": "Subject is a single bare checkmark (no circle/badge, no text) whose shape still reads as a check in grayscale at 1x.",
                "domain": "visual", "mode": "visual",
                "basis": "Specialist sample choice (expert judgment), consistent with PLAR's sample_motif proposal. The grayscale check is a sample choice that keeps the future Paused/Retry non-color distinction feasible; it is not an owner requirement on Ready.",
                "scope": "This first sample only; a different success motif could satisfy the owner brief and would require revising this criterion, not the brief.",
                "sources": [{"path": P, "locator": "queue.ready requirements sample_motif (proposal, no sources)"}],
            },
            {
                "id": "preserve_existing",
                "check": "assets/start.svg bytes remain sha256 ee2ba2fe20bd09a2c9a9c96d889f766e8af80fcdf704e8172934135e2b7e12d3 and statusVisuals paths/labels and PLAR asset IDs are unchanged by this candidate work.",
                "domain": "other", "mode": "local",
                "basis": "Owner requirement: preserve the existing vector Start control and keep other allocation IDs; assets belong at the paths the view already uses.",
                "scope": "Project files touched during this candidate's production; process/preservation check, not an image property.",
                "sources": [
                    {"path": B, "locator": "Preserve the existing vector Start control; Assets belong at the paths already used by the view"},
                    {"path": S, "locator": "whole file"},
                    {"path": V, "locator": "statusVisuals (lines 6-12)"},
                ],
            },
        ],
    }],
}

args_path = write("queue-ready-arguments.json", arguments)
crit_path = write("queue-ready-criteria.json", criteria)

schema = json.loads((ROOT / "provider-schemas.json").read_text(encoding="utf-8"))[TOOL]
observed_at = datetime.now(UTC).isoformat(timespec="microseconds")
connection = {
    "provider": "pixellab-test",
    "schema": schema,
    "discovery": {
        "source": "Host MCP tool declaration mcp__pixellab-test__create_image_pro_flash, cross-checked against provider-schemas.json",
        "observed_at": observed_at,
        "evidence": {
            "connection": "pixellab-test",
            "tool": TOOL,
            "provider_simulated": True,
            "upstream_service": False,
            "declared_fields": ["description", "width", "height", "no_background", "seed"],
            "declaration_note": "Request-only fixture; default canvas 64x64, no_background true; returns simulated acceptance with no generated image.",
            "schema_file": {"path": "provider-schemas.json", "sha256": sha(ROOT / "provider-schemas.json")},
            "contract_origin": {"path": "provider-contract-origin.json", "sha256": sha(ROOT / "provider-contract-origin.json")},
        },
    },
    "authorization": {
        "scope": "One submission of this queue.ready first-candidate request to the controlled pixellab-test connection (provider_simulated=true); no other provider, retrieval-as-acceptance or integration.",
        "evidence": {
            "source": {"path": "OWNER.md", "sha256": sha(ROOT / "OWNER.md")},
            "quote": "One submission to the controlled pixellab-test connection is authorized.",
            "submissions_authorized": 1,
            "provider_simulated": True,
            "note": "Specialist prepares only; dispatch follows the caller's independent request/criteria comparison.",
        },
    },
}
conn_path = write("connection.json", connection)

src = lambda p, role, loc: {"path": p, "sha256": sha(ROOT / p), "role": role, "locators": loc}
packet = {
    "version": 1,
    "requirements_hash": REQUIREMENTS_HASH,
    "sources": [
        src(B, "brief", ["16 by 16 logical pixels", "Ready and Retry are static images", "transparent backgrounds, readable silhouettes and the existing UI's cool blue accent; a fixed palette is not required", "Inspect at 1x and 3x nearest display scale on the actual dark panel", "working loop ... without looking like success", "Preserve the existing vector Start control", "propose a representative status sample before expanding the family", "paused ... distinguishable from activity, completion and retry without relying on color alone"]),
        src(Q, "consumer_state", ["stateAfter ok -> succeeded (line 3)"]),
        src(V, "consumer_view", ["statusVisuals.succeeded {label Ready, path assets/ready.png, frames 1} (line 10)", "display {cell [16,16], scale 3, filter nearest, background #172336} (line 13)", "statusCell / compactStatus share statusVisuals (lines 14-15)"]),
        src(S, "existing_asset_preserved_and_color_observation", ["fill #70b9ed (observation, not a style reference)"]),
        {"path": P, "sha256": PLAR_HASH, "role": "plar_selection", "locators": ["queue.ready"]},
        {"path": "OWNER.md", "sha256": sha(ROOT / "OWNER.md"), "role": "assignment_authorization", "locators": ["One submission to the controlled pixellab-test connection is authorized"]},
        {"path": "provider-schemas.json", "sha256": sha(ROOT / "provider-schemas.json"), "role": "provider_schema", "locators": [TOOL]},
    ],
    "request": {"path": "work/queue-ready-arguments.json", "sha256": sha(args_path), "kind": "provider_arguments", "tool": TOOL, "provider": "pixellab-test"},
    "criteria": {"path": "work/queue-ready-criteria.json", "sha256": sha(crit_path)},
    "connection": {"path": "work/connection.json", "sha256": sha(conn_path)},
    "choices": [
        {"choice": "Operation create_image_pro_flash at native 16x16 (width/height 16) with no_background true", "where": "request.width/height/no_background", "reason": "Only discovered generation tool; 16 is within its 16-256 multipleOf-4 range so no resize from an oversized canvas is needed; no_background expresses the transparent-background requirement. The fixture's 64x64 default is overridden explicitly."},
        {"choice": "Bare checkmark motif, no circle/badge, no text", "where": "request.description; criteria motif_checkmark", "reason": "Expert choice: strongest single-shape success symbol at 16x16; avoids circular forms that could later collide with a Retry arrow and keeps a grayscale-distinct silhouette for the Paused/Retry non-color requirement. Scoped to this sample."},
        {"choice": "Color wording 'cool light-blue accent (around #70b9ed)' with lighter/deeper blue shading", "where": "request.description; criteria cool_blue_accent", "reason": "Carries the owner's cool-blue direction and the observed Start fill as a cue; shading is a prompt suggestion, not a palette rule."},
        {"choice": "Negative prompt cues (no spinner, arrows, cross, pause bars, text, badge)", "where": "request.description", "reason": "Supports the owner's success-vs-activity/retry/paused distinction; they are prompt cues, and success_meaning is the binding criterion."},
        {"choice": "Fixed seed 1108", "where": "request.seed", "reason": "Reproducibility for a later revision comparison; carries no aesthetic meaning."},
        {"choice": "Prompt-only conditioning; Start SVG not supplied as an image input", "where": "request", "reason": "No approved style reference exists and the discovered schema has no image/style field; Start is preserved and only its accent color is cited."},
        {"choice": "Renderer exercise of statusCell/compactStatus deferred", "where": "criteria scope", "reason": "No renderer/entry point was supplied and the assignment ends at the simulated queued response; the PLAR delivery check remains for integration."},
        {"unresolved": "Family distinction from Working/Retry/Paused side by side, including grayscale comparison", "where": "criteria success_meaning scope", "reason": "Those members do not exist yet; assessed at family review per PLAR delivery checks."},
    ],
}
packet_path = write("request-review.json", packet)

for p in (args_path, crit_path, conn_path, packet_path):
    print(p.relative_to(ROOT).as_posix(), sha(p))
print("observed_at", observed_at)
