"""Validate rev2 artifacts and write work/queue.ready/rev2/request-review.json with actual hashes.

Usage: python -I build_request_review.py PROJECT_ROOT REQUIREMENTS_HASH
"""
import hashlib
import json
import os
import sys

import jsonschema

os.chdir(sys.argv[1])
RH = sys.argv[2]
R = "work/queue.ready/rev2/"


def H(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


args = json.load(open(R + "provider-arguments.json", encoding="utf-8"))
conn = json.load(open(R + "connection.json", encoding="utf-8"))
jsonschema.validate(args, conn["schema"])
plan = json.load(open(R + "candidate-plan.json", encoding="utf-8"))
jsonschema.validate(plan, json.load(open(".agents/skills/pixl-kit/runtime/pixl/asset-plan.schema.json", encoding="utf-8")))

doc = {
    "version": 1,
    "asset_id": "queue.ready",
    "generation": "rev2 (revision of the first-generation packet work/queue.ready/request-review.json)",
    "requirements_hash": RH,
    "plar": {
        "path": "plar.txt", "sha256": H("plar.txt"), "asset_id": "queue.ready", "requirements_hash": RH,
        "previous": {
            "sha256": "0abd74f7d50fc51e0ed48185a3fafa28686b1bf51758af85dd3cdea968038b33",
            "requirements_hash": "7170e02602daf79f77b8c039439182fdb6d6fcb5feab971c3d729d719e7f0302",
            "first_request_bound_requirements_hash": "79b08da5e8de765a407696cc8bb0da0414d538b953d82ae29e1c4117ffbe93f8"},
        "focused_read": {"path": R + "focused-read.json", "sha256": H(R + "focused-read.json")},
    },
    "sources": [
        {"path": "BRIEF.md", "sha256": H("BRIEF.md"),
         "role": "owner asset brief (current; previous bytes 5955da4d... retained under .pixl/assets/queue.ready/inputs/)",
         "locators": [
             "line 3: 16x16 cells, Ready static, transparent backgrounds, readable silhouettes, cool blue accent, no fixed palette, 1x/3x nearest on dark panel, working must not look like success, retry distinguishable without color",
             "line 5: destination paths from view, badges excluded, no approved style, representative sample first",
             "line 7: paused distinguishable from activity/completion/retry without color",
             "line 9 (new): Ready must visibly use a check mark with asymmetrical arms to convey successful completion; destination follows updated view; keep 16x16 canvas, static behavior, transparent background and review display conditions"]},
        {"path": "OWNER.md", "sha256": H("OWNER.md"), "role": "owner stage assignment and authorization (current)",
         "locators": [
             "lines 2-4: refresh PLAR against actual source, preserve existing IDs, other asset history and the Start control",
             "lines 4-5: continue queue.ready through one newly reviewed request and retain resumable state",
             "lines 5-6: original request belongs to pixellab-test; inspect its actual status before acting",
             "line 7: one further controlled request supported in this stage",
             "lines 7-8: preserve original attempts and contracts",
             "lines 8-11: deliverable ends at accepted revised request; no image/renderer, no approved style; integration and art acceptance future; no fabrication"]},
        {"path": "src/queue.ts", "sha256": H("src/queue.ts"), "role": "consumer state transitions (unchanged)",
         "locators": ["line 3: ok -> succeeded"]},
        {"path": "src/queue-view.ts", "sha256": H("src/queue-view.ts"),
         "role": "consumer visual mapping and display descriptor (current; previous bytes 01ee5376... retained under .pixl/assets/queue.ready/inputs/)",
         "locators": [
             "line 3: idle -> Start assets/start.svg",
             "line 6: succeeded -> Ready assets/ready-confirmed.png frames 1 (moved from assets/ready.png)",
             "line 9: display cell [16,16], scale 3, nearest, frameMs 100, background #172336",
             "lines 10-11: statusCell and compactStatus share statusVisuals"]},
        {"path": "assets/start.svg", "sha256": H("assets/start.svg"),
         "role": "preserved existing Start vector (unchanged); accent colour observation (#70b9ed) and idle-motif comparison; not an approved pixel-art style reference",
         "locators": ["line 1: fill #70b9ed, triangle path M4 2L14 8L4 14Z"]},
        {"path": "provider-schemas.json", "sha256": H("provider-schemas.json"),
         "role": "advertised pixellab-test schema (cross-check of host declaration; unchanged)", "locators": ["create_image_pro_flash"]},
        {"path": "provider-contract-origin.json", "sha256": H("provider-contract-origin.json"),
         "role": "controlled connection origin/scope note (unchanged)", "locators": ["scope"]},
        {"path": R + "original-status.json", "sha256": H(R + "original-status.json"),
         "role": "caller's actual pixellab-test list_jobs observation: first_request controlled-create-0001 failed, no image",
         "locators": ["response.jobs[0].status = failed; response.jobs[0].reason"]},
    ],
    "request": {
        "path": R + "provider-arguments.json", "sha256": H(R + "provider-arguments.json"),
        "kind": "provider_arguments", "provider": "pixellab-test", "tool": "create_image_pro_flash",
        "connection": {"path": R + "connection.json", "sha256": H(R + "connection.json")},
        "provider_simulated": True,
        "schema_validated": "Arguments validate against connection.json schema (equal to provider-schemas.json#create_image_pro_flash and the host declaration).",
        "changes_from_first_generation": {
            "previous": {"path": "work/queue.ready/provider-arguments.json", "sha256": H("work/queue.ready/provider-arguments.json")},
            "changed": "description now requires a check mark with clearly asymmetrical arms (short up-left arm, much longer up-right arm, classic tick) instead of an unspecified checkmark silhouette",
            "unchanged": "width 16, height 16, no_background true, seed omitted; colour, stroke, edge, panel, transparency, no-text/no-plate/no-shadow and static wording"},
        "not_expressible_by_schema": "Readability on #172336, 1x/3x nearest inspection, check-mark arm asymmetry, cool-blue relationship and non-colour silhouette are stated in description prose only; the schema has no palette, reference-image, alpha-mode or style controls. They are evaluated by the candidate-plan criteria once a real image exists.",
    },
    "criteria": {
        "path": R + "candidate-plan.json", "sha256": H(R + "candidate-plan.json"),
        "schema_validated": "Validates against runtime/pixl/asset-plan.schema.json.",
        "authority_summary": {
            "owner_or_consumer_requirement": ["geometry", "transparent-background", "ready-meaning", "asymmetric-check-mark", "readability-1x-3x", "cool-blue-accent"],
            "specialist_sample_choice": ["silhouette-without-color", "sample-pixel-craft"],
            "observations_used_as_reference_not_rules": ["#70b9ed (assets/start.svg fill)", "#172336 (src/queue-view.ts display.background, used as composite panel)"]},
        "changes_from_first_generation": {
            "previous": {"path": "work/queue.ready/candidate-plan.json", "sha256": H("work/queue.ready/candidate-plan.json")},
            "added": ["asymmetric-check-mark (owner requirement, BRIEF.md line 9)"],
            "revised": [
                "geometry, transparent-background, readability-1x-3x, ready-meaning: added BRIEF.md line 9 locators; queue-view line 6 cited at its current content",
                "contract.intent: destination assets/ready-confirmed.png; check mark now owner-required; tick orientation stated as specialist choice",
                "scope and output name: rev2 and moved destination"],
            "unchanged": ["cool-blue-accent", "silhouette-without-color", "sample-pixel-craft"]},
    },
    "choices": [
        {"id": "sample-asset", "choice": "Ready remains the representative family sample.",
         "authority": "PLAR proposal (family_sample) carried from the first generation; BRIEF line 5 requires a sample first without choosing the status",
         "where": "candidate-plan scope", "reason": "Static, single frame, no dependency on other statuses; the owner update keeps it the active asset."},
        {"id": "tick-orientation", "choice": "Short arm up-left from the bottom point, much longer arm up-right (classic tick).",
         "authority": "specialist choice implementing the owner asymmetrical-arms requirement",
         "where": "provider-arguments description; contract intent",
         "reason": "The conventional, most recognisable completion tick in left-to-right UIs. The asymmetric-check-mark criterion deliberately does not fix ratio or orientation, so a mirrored or differently proportioned asymmetric tick still passes."},
        {"id": "motif-details", "choice": "Chunky ~2px strokes, centered, no backing circle/badge plate, no drop shadow.",
         "authority": "specialist choice (PLAR sample_motif proposal)", "where": "provider-arguments description; contract intent",
         "reason": "Chunky strokes survive 1x at 16x16 and keep the arm-length difference legible; no plate keeps transparency simple and leaves room for family marks. Revisable at style review; not rejection rules."},
        {"id": "colour-treatment", "choice": "Cool sky blue close to #70b9ed plus one lighter highlight tone; no fixed palette.",
         "authority": "specialist choice implementing owner cool-blue-accent direction", "where": "provider-arguments description",
         "reason": "Relates to the observed Start fill without making the hex a rejection rule; a lighter tone keeps contrast against #172336."},
        {"id": "operation", "choice": "create_image_pro_flash, width 16, height 16, no_background true, seed omitted.",
         "authority": "specialist choice within the discovered schema", "where": "provider-arguments",
         "reason": "Only advertised generation tool; native 16x16 avoids downscaling (fixture default is 64x64, so width/height are explicit); no_background matches the transparent requirement; no seed is specified or needed (the failed first attempt produced no image to reproduce)."},
        {"id": "alpha", "choice": "Contract alpha 'full' and empty palette.", "authority": "derived from brief (transparent, no fixed palette)",
         "where": "candidate-plan contract", "reason": "Avoids manufacturing a binary-alpha or fixed-palette rule."},
        {"id": "extra-criteria", "choice": "silhouette-without-color and sample-pixel-craft remain specialist sample criteria.",
         "authority": "specialist choice", "where": "candidate-plan criteria",
         "reason": "Support the later owner non-colour and coherence obligations while judging only this sample; caller may demote or drop them."},
        {"id": "other-rows", "choice": "No requirement change to queue.working, queue.retry, queue.paused or queue.start.",
         "authority": "specialist PLAR refresh judgment", "where": "plar.txt",
         "reason": "The changed sources are file-level inputs to every row, but the actual changes (BRIEF line 9, queue-view line 6) concern only Ready. Their existing comparisons against the reviewed Ready sample already cover the new mark. Start remains byte-unchanged."},
    ],
    "deferred_obligations": [
        {"id": "family-working-not-success", "obligation": "Working 4-frame loop communicates activity without looking like Ready/success (now an asymmetrical check mark).",
         "source": "BRIEF.md lines 3, 9", "stage": "family expansion after Ready sample approval",
         "prerequisites": ["approved Ready sample", "Working candidate (queue.working)"]},
        {"id": "family-retry-non-color", "obligation": "Retry (assets/error-retry.png) distinguishable from Ready and others without colour alone.",
         "source": "BRIEF.md lines 3, 7", "stage": "family expansion/collective review", "prerequisites": ["approved Ready sample", "Retry candidate"]},
        {"id": "family-paused-non-color", "obligation": "Paused distinguishable from activity, completion and retry without colour alone, including grayscale comparison at 1x and 3x.",
         "source": "BRIEF.md line 7; PLAR queue.ready delivery checks", "stage": "family collective review",
         "prerequisites": ["approved Ready sample", "Working, Retry and Paused candidates"]},
        {"id": "style-decision", "obligation": "Record the representative-sample style decision and source-bind the approved visual reference before expanding the family.",
         "source": "BRIEF.md line 5; PLAR queue.ready next/questions", "stage": "after retrieval and inspection of a real Ready candidate",
         "prerequisites": ["retrieved candidate image (the controlled pixellab-test connection returns none)"]},
        {"id": "destination-delivery", "obligation": "Place the accepted Ready image at assets/ready-confirmed.png (not the superseded assets/ready.png); decode and confirm dimensions/frames/transparency there.",
         "source": "BRIEF.md lines 5, 9; src/queue-view.ts line 6", "stage": "delivery after art acceptance", "prerequisites": ["accepted candidate"]},
        {"id": "renderer-integration", "obligation": "Exercise statusCell and compactStatus in an actual renderer and confirm the Ready label and asset appear for the ok transition.",
         "source": "src/queue-view.ts lines 10-11; PLAR queue.ready delivery checks", "stage": "integration/live acceptance",
         "prerequisites": ["delivered asset", "a renderer or UI entry point (none supplied)"]},
    ],
    "resume": {
        "store": ".pixl/assets/queue.ready",
        "state_before_revision": {"hash": "47ef2326e8420a8db6369384c5eaf847cc07afd9474e37522a556c6689d71864", "revision": 4},
        "previous_generation": {
            "task": "task", "task_state": "open", "output": "output.ready", "candidate": None,
            "job": {"id": "first_request", "state": "failed", "remote_id": "controlled-create-0001", "provider": "pixellab-test",
                    "provider_simulated": True, "evidence": R + "original-status.json"},
            "packet": {"path": "work/queue.ready/request-review.json", "sha256": H("work/queue.ready/request-review.json")}},
        "revision_operation": "pixl_plar_prepare with revise: true and expect = state_before_revision.hash; the returned task/output/job IDs are the current ones",
    },
    "preserved": {
        "start_vector": {"path": "assets/start.svg", "sha256": H("assets/start.svg"), "note": "Unmodified; no Start production in scope."},
        "plar_ids": "No PLAR allocation IDs added, removed or renamed; only queue.ready requirements/destination/next/evidence, two source hashes and coverage changed.",
        "first_generation": "work/queue.ready/* first-generation files untouched; first_request job and its events untouched.",
    },
    "review_status": {
        "specialist_self_review": "Specialist validated arguments against the discovered schema and the plan against asset-plan.schema.json, and checked cited locators; this is self-review only.",
        "independent_caller_review": "not yet performed (caller owns it)"},
}
with open(R + "request-review.json", "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
print(H(R + "request-review.json"))
