"""Write rev2 connection.json and request-review.json for queue.ready.

Run: python -I build-packet.py PROJECT_ROOT REQUIREMENTS_HASH
Validates provider-arguments.json against provider-schemas.json#create_image_pro_flash.
"""
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import jsonschema

root = Path(sys.argv[1])
req_hash = sys.argv[2]
rev = root / "work/queue.ready/rev2"


def sha(rel):
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


schemas = json.loads((root / "provider-schemas.json").read_text(encoding="utf-8"))
schema = schemas["create_image_pro_flash"]
args = json.loads((rev / "provider-arguments.json").read_text(encoding="utf-8"))
jsonschema.Draft202012Validator(schema).validate(args)
assert args["width"] == 16 and args["height"] == 16 and args["no_background"] is True

connection = {
    "provider": "pixellab-test",
    "schema": schema,
    "discovery": {
        "source": ("Host MCP tool declaration mcp__pixellab-test__create_image_pro_flash visible in this "
                   "specialist session, cross-checked field-for-field against provider-schemas.json#create_image_pro_flash"),
        "observed_at": datetime.now(UTC).isoformat(),
        "evidence": {
            "connection": "pixellab-test",
            "tool": "create_image_pro_flash",
            "schema_file": "provider-schemas.json",
            "schema_file_sha256": sha("provider-schemas.json"),
            "contract_origin_file": "provider-contract-origin.json",
            "contract_origin_sha256": sha("provider-contract-origin.json"),
            "host_declaration_note": ("Controlled request-only fixture; default canvas 64x64, no_background true; "
                                      "returns a simulated acceptance with no generated image or upstream provider."),
            "provider_simulated": True,
        },
    },
    "authorization": {
        "scope": ("Exactly one further submission, the revised queue.ready request, to the controlled pixellab-test "
                  "connection (create_image_pro_flash), dispatched by the caller after its independent comparison. "
                  "No other provider, credentials, installs or host changes."),
        "evidence": {
            "source": "OWNER.md",
            "source_sha256": sha("OWNER.md"),
            "locator": "line 7: 'The connection supports one further controlled request in this stage.'",
            "lines": [7, 7],
            "provider_simulated": True,
            "dispatch_owner": "caller, after its independent request/criteria comparison",
        },
    },
}
(rev / "connection.json").write_text(json.dumps(connection, indent=2) + "\n", encoding="utf-8")

packet = {
    "version": 1,
    "asset_id": "queue.ready",
    "requirements_hash": req_hash,
    "plar": {"path": "plar.txt", "sha256": sha("plar.txt"), "asset_id": "queue.ready", "requirements_hash": req_hash},
    "revision": {
        "kind": "revised contract (second generation)",
        "supersedes_packet": {"path": "work/queue.ready/request-review.json", "sha256": sha("work/queue.ready/request-review.json")},
        "changes": [
            "BRIEF.md line 9: check mark with asymmetrical arms is now an owner requirement (was specialist sample_motif proposal); new rejection criterion check-mark-asymmetrical-arms.",
            "src/queue-view.ts line 6: succeeded destination moved assets/ready.png -> assets/ready-confirmed.png (same Ready role); deferred delivery updated.",
            "Provider description adds the asymmetrical-arm construction and 3x readability; width/height/no_background unchanged; seed still omitted.",
        ],
    },
    "sources": [
        {"path": "BRIEF.md", "sha256": sha("BRIEF.md"), "role": "owner asset brief", "locators": [
            "line 3: 16x16 cells, Ready static, transparent backgrounds, readable silhouettes, cool blue accent, no fixed palette, 1x/3x nearest on dark panel, working must not look like success, retry distinguishable without color",
            "line 5: destination paths from view, badges excluded, no approved style, representative sample first",
            "line 7: paused distinguishable from activity/completion/retry without color",
            "line 9: Ready must visibly use a check mark with asymmetrical arms to convey successful completion; destination follows updated view; keep 16x16, static, transparent, review display conditions"]},
        {"path": "OWNER.md", "sha256": sha("OWNER.md"), "role": "owner stage assignment and authorization", "locators": [
            "lines 2-5: refresh PLAR, preserve IDs/history/Start, one newly reviewed request with resumable state",
            "lines 5-6: original request belongs to the controlled pixellab-test connection; inspect status",
            "line 7: one further controlled request in this stage; preserve original attempts and contracts",
            "lines 8-11: deliverable ends at accepted revised request; no image/renderer/approved style; no fabrication"]},
        {"path": "src/queue.ts", "sha256": sha("src/queue.ts"), "role": "consumer state transitions", "locators": ["line 3: ok -> succeeded"]},
        {"path": "src/queue-view.ts", "sha256": sha("src/queue-view.ts"), "role": "consumer visual mapping and display descriptor", "locators": [
            "line 3: idle -> Start assets/start.svg", "line 6: succeeded -> Ready assets/ready-confirmed.png frames 1",
            "line 9: display cell [16,16], scale 3, nearest, frameMs 100, background #172336",
            "lines 10-11: statusCell and compactStatus share statusVisuals"]},
        {"path": "assets/start.svg", "sha256": sha("assets/start.svg"), "role": "preserved existing Start vector (unchanged); accent colour observation #70b9ed and idle-motif comparison; not an approved pixel-art style reference", "locators": ["line 1: fill #70b9ed, triangle path M4 2L14 8L4 14Z"]},
        {"path": "provider-schemas.json", "sha256": sha("provider-schemas.json"), "role": "advertised pixellab-test schema (cross-check of host declaration)", "locators": ["create_image_pro_flash"]},
        {"path": "provider-contract-origin.json", "sha256": sha("provider-contract-origin.json"), "role": "controlled connection origin/scope note", "locators": ["scope"]},
        {"path": "work/queue.ready/provider-observation-failed.json", "sha256": sha("work/queue.ready/provider-observation-failed.json"), "role": "caller observation: first_request failed on its originating controlled connection", "locators": ["response.jobs[0].status failed"]},
    ],
    "request": {
        "path": "work/queue.ready/rev2/provider-arguments.json",
        "sha256": sha("work/queue.ready/rev2/provider-arguments.json"),
        "kind": "provider_arguments",
        "provider": "pixellab-test",
        "tool": "create_image_pro_flash",
        "connection": {"path": "work/queue.ready/rev2/connection.json", "sha256": sha("work/queue.ready/rev2/connection.json")},
        "provider_simulated": True,
        "schema_validation": "Arguments validated against provider-schemas.json#create_image_pro_flash (Draft 2020-12) by work/queue.ready/rev2/build-packet.py.",
        "not_expressible_by_schema": "The asymmetrical-arm check mark, readability on #172336 at 1x/3x nearest, cool-blue relationship and non-colour silhouette are stated in description prose only; the schema has no palette, reference-image, alpha-mode or style controls. They are evaluated by the candidate-plan criteria after retrieval.",
    },
    "criteria": {
        "path": "work/queue.ready/rev2/candidate-plan.json",
        "sha256": sha("work/queue.ready/rev2/candidate-plan.json"),
        "authority_summary": {
            "owner_or_consumer_requirement": ["geometry", "transparent-background", "check-mark-asymmetrical-arms", "ready-meaning", "readability-1x-3x", "cool-blue-accent"],
            "specialist_sample_choice": ["silhouette-without-color", "sample-pixel-craft"],
            "observations_used_as_reference_not_rules": ["#70b9ed (assets/start.svg fill)", "#172336 (src/queue-view.ts display.background, used as composite panel)"],
        },
    },
    "choices": [
        {"id": "sample-asset", "choice": "Ready remains the representative family sample.", "authority": "PLAR proposal (family_sample) under BRIEF line 5", "where": "candidate-plan scope", "reason": "Static, single frame, no dependency on other statuses."},
        {"id": "arm-orientation", "choice": "Short left arm meeting a longer right arm rising to the upper right.", "authority": "specialist choice", "where": "provider-arguments description; contract intent", "reason": "Conventional check-mark orientation that satisfies the owner's asymmetrical-arms requirement; the criterion does not require this orientation, so a mirrored asymmetric mark is not rejected."},
        {"id": "motif-construction", "choice": "Single centered check mark, chunky ~2px strokes, no backing circle/badge plate, no drop shadow.", "authority": "specialist choice", "where": "provider-arguments description; contract intent", "reason": "Chunky strokes survive 1x at 16x16 while leaving room for a visibly unequal arm length; no plate keeps transparency simple and leaves room for later family marks. Revisable at style review; not a rejection rule."},
        {"id": "colour-treatment", "choice": "Cool sky blue close to #70b9ed plus one lighter highlight tone; no fixed palette.", "authority": "specialist choice implementing owner 'cool blue accent' direction", "where": "provider-arguments description", "reason": "Relates to the observed Start fill without making the hex a rejection rule; a lighter tone keeps contrast on #172336."},
        {"id": "operation", "choice": "create_image_pro_flash, width 16, height 16, no_background true, seed omitted.", "authority": "specialist choice within the discovered schema", "where": "provider-arguments", "reason": "Only advertised generation tool; native 16x16 avoids downscaling (fixture default is 64x64, so explicit); no_background matches transparency; no seed specified or needed."},
        {"id": "alpha", "choice": "Contract alpha 'full' and empty palette.", "authority": "derived from brief (transparent, no fixed palette)", "where": "candidate-plan contract", "reason": "Avoids manufacturing a binary-alpha or fixed-palette rule."},
        {"id": "extra-criteria", "choice": "silhouette-without-color and sample-pixel-craft are specialist sample criteria (authority proposal).", "authority": "specialist choice", "where": "candidate-plan criteria", "reason": "Support later owner non-colour and coherence obligations while judging only this sample; caller may demote or drop them."},
        {"id": "output-id", "choice": "Plan output id 'ready' reused for the revised generation.", "authority": "specialist choice", "where": "candidate-plan outputs[0].id", "reason": "Same visual role; the runtime assigns the generation's task/output/job IDs, which are reported from the prepare result."},
    ],
    "deferred_obligations": [
        {"id": "family-working-not-success", "obligation": "Working 4-frame loop communicates activity without looking like Ready/success.", "source": "BRIEF.md line 3", "stage": "family expansion after Ready sample approval", "prerequisites": ["approved Ready sample", "Working candidate (queue.working)"]},
        {"id": "family-retry-non-color", "obligation": "Retry (assets/error-retry.png) distinguishable from Ready and others without colour alone.", "source": "BRIEF.md lines 3, 7", "stage": "family expansion/collective review", "prerequisites": ["approved Ready sample", "Retry candidate (queue.retry)"]},
        {"id": "family-paused-non-color", "obligation": "Paused distinguishable from activity, completion and retry without colour alone, including grayscale comparison at 1x and 3x.", "source": "BRIEF.md line 7; PLAR queue.ready delivery checks / paused_family_distinction", "stage": "family collective review", "prerequisites": ["approved Ready sample", "Working, Retry and Paused candidates"]},
        {"id": "style-decision", "obligation": "Record the representative-sample style decision and source-bind the approved visual reference before expanding the family.", "source": "BRIEF.md line 5; OWNER.md lines 8-10; PLAR queue.ready questions", "stage": "after retrieval and inspection of a real Ready candidate", "prerequisites": ["retrieved candidate image (the controlled pixellab-test connection returns none)"]},
        {"id": "destination-delivery", "obligation": "Place the accepted Ready image at assets/ready-confirmed.png; decode and confirm 16x16, 1 frame, transparency and the asymmetrical-arm check mark there.", "source": "BRIEF.md lines 5, 9; src/queue-view.ts line 6; PLAR queue.ready delivery", "stage": "delivery after art acceptance", "prerequisites": ["accepted candidate"]},
        {"id": "renderer-integration", "obligation": "Exercise statusCell and compactStatus in an actual renderer and confirm the Ready label and asset appear for the ok transition.", "source": "src/queue-view.ts lines 10-11; PLAR queue.ready delivery checks", "stage": "integration/live acceptance", "prerequisites": ["delivered asset", "a renderer or UI entry point (none supplied)"]},
    ],
    "resume": {
        "store": ".pixl/assets/queue.ready",
        "state_before_revision": {"revision": 4, "hash": "b9c3a2f7b4d93448cdb80a1a67dac4f4616f72a88ff085568b76a6ac76067d18"},
        "prior_generation": {"task": "task", "output": "output.ready", "task_state": "open"},
        "jobs": [{"id": "first_request", "task": "task", "provider": "pixellab-test", "tool": "create_image_pro_flash", "remote_id": "controlled-create-0001", "state": "failed", "next_action": "review_failure", "provider_simulated": True, "evidence": "work/queue.ready/provider-observation-failed.json", "note": "Terminal on its originating controlled connection with no image; retained, not reused."}],
        "preparation": "pixl_plar_prepare revise=true with expect = state hash above; the new task/output/job IDs are reported from its result, not assumed.",
    },
    "preserved": {
        "start_vector": {"path": "assets/start.svg", "sha256": sha("assets/start.svg"), "note": "Unmodified; no Start production in scope."},
        "prior_packet_artifacts": "work/queue.ready/*.json (first generation) left byte-identical.",
        "plar_ids": "No PLAR asset IDs added, removed or renamed.",
    },
    "review_status": {"specialist_self_review": "Specialist validated arguments against the discovered schema and resolved locators with pixl_request_review; self-review only.", "independent_caller_review": "not yet performed (caller owns it)"},
}
(rev / "request-review.json").write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
for f in ["provider-arguments.json", "candidate-plan.json", "connection.json", "request-review.json"]:
    print(f, sha(f"work/queue.ready/rev2/{f}"))
