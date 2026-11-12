"""Caller: write work/native-production/CALLER-RESULT.json from actual on-disk evidence.
Run from the consumer root with the assignment Python using -I; argv[1] = current UTC clock.
"""
import json, hashlib, sys
from pathlib import Path

now = sys.argv[1]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def ref(p, role):
    return {"path": p, "sha256": sha(p), "role": role}

cap = json.loads(Path('work/native-production/render-01/capture.json').read_text(encoding='utf-8'))
chk = json.loads(Path('work/native-production/renderer-check-01.json').read_text(encoding='utf-8'))
spec = json.loads(Path('work/native-production/SPECIALIST-RESULT.json').read_text(encoding='utf-8'))
hand = json.loads(Path('work/native-production/handoff/handoff-caller-view.json').read_text(encoding='utf-8'))

doc = {
    "version": 1,
    "written_at_utc": now,
    "caller": {"role": "calling agent", "host": "Claude Code (claude), persisted parent session 9d0f792b-9ac2-42e1-8131-5861ce4b1dc5", "model": "claude-fable-5-1"},
    "assignment": ref("NATIVE-PRODUCTION.md", "CF-10 native production assignment (authority)"),
    "status": "delivered",
    "status_basis": "The whole assigned scope was performed by the named pixl:pixl child and independently consumed by the caller: south preserved byte-identically; east and north are official PixelLab rotations of the uploaded source; west is an EDITED deterministic mirror of the official east (disclosed everywhere; the official raw west is retained and recorded as failed); family delivery task done with every saved criterion passing; the bounded consumer renderer capture and check pass and were independently re-verified; PLAR linked and integrated; compact handoff consumed; 1 of 20 generations spent. 'delivered' is judged against this assignment and the saved criteria, not as general artistic or host-reliability qualification.",
    "native_child": {
        "agent_type": "pixl:pixl (named specialist, Agent tool subagent_type)",
        "agent_id": "aeb8fdd3833c62981",
        "launch": "Agent tool, run_in_background false, 2026-11-12 ~08:07Z; returned packet-01 without spending",
        "continuations": [
            "SendMessage ~08:25Z: caller comparison with five corrections, conditional dispatch authorization",
            "SendMessage ~08:46Z (this persisted session): resume after host interruption; finish reviews, renderer, family, PLAR, handoff",
            "completion notification received 2026-11-12T08:59Z (task-id aeb8fdd3833c62981, status completed)"
        ],
        "same_child_throughout": True,
        "replacement_spawned": False
    },
    "interrupted_host_outcome": {
        "disclosure": "The original parent Claude Code process ended while waiting for the child after the ~08:25Z resume. A host task notification later reported the background agent 'stopped' with no completion record. At that point the child had completed the paid call, download, import, deterministic west edit and visual inspection, but SPECIALIST-RESULT.json and CALLER-RESULT.json did not exist.",
        "recovery": "Explicit same-parent/same-child recovery: this persisted parent session 9d0f792b-9ac2-42e1-8131-5861ce4b1dc5 re-read all on-disk state (store revision 12, hash df1ae9c7...), wrote the packet-02 completion review and the clock/interruption note, then resumed the SAME child aeb8fdd3833c62981 with SendMessage. No replacement child, no repeated paid request, no overwritten evidence.",
        "record": ref("work/native-production/caller-clock-clarification-and-recovery.json", "append-only clock clarification and interruption record")
    },
    "specialist_result": ref("work/native-production/SPECIALIST-RESULT.json", "specialist result (status delivered, all requested fields present)"),
    "comparison_ref": [
        ref("work/native-production/COMPARISON.json", "caller comparison of packet-01: changes_requested, 27 criterion rows, 10 choice rows (written ~08:24Z, before dispatch)"),
        ref("work/native-production/COMPARISON-packet-02-completion-review.json", "caller completion review of packet-02 written AFTER dispatch (~08:45Z): consistent; not a pre-dispatch reread"),
        ref("work/native-production/caller-coverage-check-receipt.json", "pixl_request_review comparison-coverage attempt: refused (candidate packets are not connected plans); label '08:35Z approx' corrected in the clock note to ~08:25Z")
    ],
    "comparison_chronology": "The caller's ~08:25Z SendMessage conditionally authorized five specified corrections before paid dispatch. The child applied corrections 1-4 in packet-02, withdrew the packet-01 job (0 generations), prepared and dispatch-claimed a new job with the corrected arguments, and made the paid call (dispatch claim 08:26:36.062Z; native call start 08:26:46.369Z, return 08:26:46.712Z). There was no parent reread of packet-02 before that paid call; the parent's packet-02 review happened only during this recovery and is labelled as such.",
    "request_packets": {
        "packet_01": ref("work/native-production/packet-01/request-review.json", "superseded packet, unchanged"),
        "packet_02": ref("work/native-production/packet-02/request-review.json", "dispatched packet, unchanged"),
        "packet_02_arguments": ref("work/native-production/packet-02/provider-arguments.json", "exact dispatched provider arguments (palette added, description corrected)")
    },
    "provider_operations": [
        {"tool": "mcp__pixellab__get_balance", "by": "caller", "observed_at": "2026-11-12T08:06:01Z", "result": {"generations_remaining": 4984, "generations_used": 16}, "receipt": ref("work/native-production/balance-start.json", "starting balance")},
        {"tool": "mcp__pixellab__get_upload_url + POST of assets/robot-base.png", "by": "specialist", "actual_id": "upload:57ceb659-b047-49e5-9250-58343f194c5f", "observed_at": "2026-11-12T08:09:03Z", "usage": "free", "receipt": ref("work/native-production/upload-response.raw.json", "raw upload reply (ref, 32x32, 1 frame)")},
        {"tool": "(local only) job first_request", "by": "specialist", "actual_id": None, "outcome": "withdrawn before dispatch after the caller comparison; never sent to PixelLab; 0 generations"},
        {"tool": "mcp__pixellab__create_object_pro_flash", "by": "specialist", "actual_id": {"object_id": "2a3cb51a-6cf7-485d-8441-3c3db762cc9d", "background_job_id": "ea834364-0f7d-42eb-876b-bb26e21e1269", "group": "fd1b84c0-1fed-43b2-8232-a59776bb0edd"}, "job": "r.acf329804ba043b7.request (durable; dispatch claim 08:26:36.062Z; native call 08:26:46.369Z-08:26:46.712Z; submitted event 08:26:57.597Z; succeeded 08:30:51.263Z)", "arguments_ref": ref("work/native-production/packet-02/provider-arguments.json", "dispatched arguments"), "response_ref": [ref("work/native-production/provider/create_object_pro_flash-response.json", "raw submit response"), ref("work/native-production/provider/get_object-response.json", "get_object completed response"), ref("work/native-production/returned/zip/object-2a3cb51a.zip", "downloaded ZIP of all 8 rotations")], "observed_usage": {"estimated_generations_in_response": 1, "balance_before": {"generations_remaining": 4979, "generations_used": 21, "observed_at": "2026-11-12T08:26:37Z"}, "balance_after": {"generations_remaining": 4978, "generations_used": 22, "observed_at": "2026-11-12T08:30:30Z"}, "consumed": 1}},
        {"tool": "mcp__pixellab__get_balance", "by": "caller (final, independent)", "observed_at": "2026-11-12T09:00Z", "result": {"generations_remaining": 4978, "generations_used": 22, "generations_today": 14, "subscription": "active (Tier 2: Pixel Artisan)"}, "note": "Matches the specialist's 08:53:51Z final reading. Assignment consumption: 1 of the 20-generation limit. The 5 generations used between 08:06 and 08:26 were not spent by this session (no paid call existed then) and are not attributed to this assignment."}
    ],
    "delivered_files": [
        ref("assets/robot/south.png", "reused: byte-identical copy of assets/robot-base.png (caller verified sha256 equal)"),
        ref("assets/robot/east.png", "generated: official PixelLab rotation east, unedited (caller verified equal to returned/rotations/east.png and the ZIP entry hash)"),
        ref("assets/robot/north.png", "generated: official PixelLab rotation north, unedited (caller verified equal to returned/rotations/north.png)"),
        ref("assets/robot/west.png", "edited: deterministic horizontal mirror of the official east (caller verified mirror(east)==file byte-for-byte on decoded RGBA); NOT an official generated west")
    ],
    "retained_not_delivered": [
        ref("work/native-production/returned/rotations/west.png", "official raw west: rejected (identity fail, direction fail in review.west.raw.01); retained"),
        ref("work/native-production/returned/rotations/south.png", "official south rotation, byte-identical to the source; lineage evidence only"),
        ref("work/native-production/returned/rotations/south-east.png", "extra view, retained"),
        ref("work/native-production/returned/rotations/south-west.png", "extra view, retained"),
        ref("work/native-production/returned/rotations/north-east.png", "extra view, retained"),
        ref("work/native-production/returned/rotations/north-west.png", "extra view, retained")
    ],
    "viewed_images": [
        ref("assets/robot-base.png", "source, 1x via Read"),
        ref("work/native-production/inspect/robot-base-8x.png", "source 8x"),
        ref("work/native-production/returned/rotations/east.png", "official east, 1x via Read"),
        ref("work/native-production/returned/rotations/north.png", "official north, 1x via Read"),
        ref("work/native-production/returned/rotations/west.png", "official raw west, 1x via Read"),
        ref("work/native-production/edited/west-mirror-of-east.png", "edited west, 1x via Read"),
        ref("work/native-production/inspect/east-3x.png", "east 3x"),
        ref("work/native-production/inspect/north-3x.png", "north 3x"),
        ref("work/native-production/inspect/west-3x.png", "raw west 3x"),
        ref("work/native-production/inspect/west-edited-3x.png", "edited west 3x"),
        ref("work/native-production/inspect/sheet-4dir-8x-dark.png", "S|E|N|W(raw) 8x sheet"),
        ref("work/native-production/inspect/sheet-4dir-edited-8x-dark.png", "S|E|N|W(edited) 8x sheet"),
        ref("work/native-production/inspect/sheet-4dir-edited-1x-dark.png", "S|E|N|W(edited) native 1x sheet"),
        ref("work/native-production/inspect/sheet-8dir-6x-dark.png", "all 8 official rotations 6x"),
        ref("work/native-production/render-01/destination.png", "renderer page screenshot 900x700 (viewed)"),
        ref("work/native-production/render-01/south-1x.png", "renderer cell south 1x (viewed)"),
        ref("work/native-production/render-01/east-1x.png", "renderer cell east 1x (viewed)"),
        ref("work/native-production/render-01/north-1x.png", "renderer cell north 1x (viewed)"),
        ref("work/native-production/render-01/west-1x.png", "renderer cell west 1x (viewed)"),
        ref("work/native-production/render-01/south-3x.png", "renderer cell south 3x (viewed)"),
        ref("work/native-production/render-01/east-3x.png", "renderer cell east 3x (viewed)"),
        ref("work/native-production/render-01/north-3x.png", "renderer cell north 3x (viewed)"),
        ref("work/native-production/render-01/west-3x.png", "renderer cell west 3x (viewed)")
    ],
    "caller_visual_judgment": {
        "source_mapping": "The delivered south is the source. East and north are the official rotations of the uploaded source bytes (upload ref bound to sha256 d997cade...). West is the mirror of the official east. Identity (navy frame, posts, teal panel, three colours) is preserved in every facing; no features were added; palette stays within the three source colours; alpha is binary; all four stand on rows 3-27 in one 32x32 cell.",
        "destination_render": "destination.png shows the renderer page with the four controller rows: south front with eyes, east narrow slab with the teal front edge on the right, north plain back, west narrow slab with the teal edge on the left, at 1x and crisp 3x nearest on #172336. The 1x cells equal the delivered files composited on the background and the 3x cells equal their nearest 3x enlargement (Pillow, byte-for-byte). The turn S->E->N->W is coherent.",
        "concerns_recorded_not_blocking": ["East (and the mirrored west) has a 1x2 transparent notch under the front edge at rows 26-27; invisible at 1x, minor at 3x.", "The north back is featureless navy; the source never defined a back.", "The official raw west was unusable (no front edge); the delivered west is therefore an edited derivative, labelled as such in state, PLAR, handoff and reports."]
    },
    "renderer_report_ref": {"capture": ref("work/native-production/render-01/capture.json", "capture metadata"), "inputs": ref("work/native-production/render-01/inputs.json", "pre-capture input hashes (match the delivered files and unchanged renderer sources)"), "execution": ref("work/native-production/render-01/execution.json", "completion and cleanup"), "stdout": ref("work/native-production/render-01-capture.stdout.txt", "capture stdout: status complete, cleanup complete"), "facts": {"browser": cap.get("browser_version", {}).get("product"), "node": cap.get("node"), "observed_at": cap.get("observed_at"), "south_matches_base": cap.get("south_matches_base"), "controller_mapping": cap.get("controller_mapping"), "selected_mapping": cap.get("selected_mapping"), "errors": cap.get("errors")}},
    "renderer_check_ref": {"report": ref("work/native-production/renderer-check-01.json", "check.py report"), "stdout": ref("work/native-production/renderer-check-01.stdout.txt", "check stdout"), "status": chk.get("status"), "facts": chk.get("facts"), "failures": chk.get("failures"), "command_run_by": "specialist, from the consumer root, exactly as NATIVE-PRODUCTION.md specifies (render-01 / renderer-check-01.json)"},
    "handoff_ref": {"handoff_file": ref(".pixl/handoffs/d864d8602898fda7e93819b65f7160e77d6e6f594d4c852057ab232c368c7970.json", "immutable pixl_plar_handoff (caller view)"), "caller_view": ref("work/native-production/handoff/handoff-caller-view.json", "saved caller-view result"), "asset_id": hand.get("asset_id"), "requirements_hash": hand.get("requirements_hash"), "state_hash": hand.get("state_hash"), "derived_next": hand.get("next"), "assignment_status_authored": hand.get("assignment", {}).get("status"), "integration_authored": hand.get("caller", {}).get("integration", {}).get("status"), "production": {"task": hand.get("production", {}).get("task"), "task_state": hand.get("production", {}).get("task_state"), "criteria": hand.get("production", {}).get("criteria"), "jobs": hand.get("production", {}).get("jobs"), "selection_current": hand.get("production", {}).get("selection_current")}, "consumed": "Caller opened the caller view, verified the immutable handoff file hash on disk, verified every declared artifact hash against the files, and re-ran the refresh read (pixl_plar_read production-plar.txt robot.directions)."},
    "independent_checks": [
        {"check": "packet-02 corrections 1-4 applied and dispatched job bound to the corrected arguments", "method": "diff packet-01 vs packet-02; pixl_jobs request arguments; request_sha256 ca743f1d...", "result": "pass"},
        {"check": "source files unchanged", "method": "sha256 of BRIEF.md, src/robot.ts, assets/robot-base.png, plar.txt equal their original hashes; installed kit and renderer-native sources unchanged (inputs.json hashes equal the caller's 08:06Z hashes)", "result": "pass"},
        {"check": "delivered bytes identity", "method": "sha256: south == base; east == returned east == ZIP entry; north == returned north; west == edited mirror; Pillow mirror(east)==west; raw west differs in 17 px", "result": "pass"},
        {"check": "delivered file properties", "method": "Pillow: all four 32x32 RGBA, 0 fractional alpha, colours within {#25354a,#56b5bc,#f4dda2}, bbox top 3 bottom 28, centre 16.0/16.5/16.0/15.5", "result": "pass"},
        {"check": "renderer cells", "method": "Pillow: each 1x cell == delivered file alpha-composited on #172336; each 3x cell == NEAREST 3x of the 1x; destination.png 900x700 viewed", "result": "pass"},
        {"check": "renderer check report", "method": "renderer-check-01.json status pass, failures [], capture sha256 matches capture.json on disk", "result": "pass"},
        {"check": "durable state", "method": "pixl_validate: valid, revision 40, hash ceb0b61e..., 353 records, files_verified; delivery task done, 4/4 criteria pass; raw west review recorded identity/direction fail; jobs: first_request failed/withdrawn, r.acf329804ba043b7.request succeeded remote 2a3cb51a...", "result": "pass"},
        {"check": "PLAR", "method": "pixl_plar_read: status integrated, production linked to robot-directions-family.delivery.task/output, requirements_hash e3918fba..., existing roles label west as EDITED; plar.txt untouched", "result": "pass"},
        {"check": "handoff identities", "method": "handoff file sha256 on disk equals its name and the caller view; state_hash and requirements_hash equal the fresh pixl_plar_read continuation", "result": "pass"},
        {"check": "spend", "method": "caller get_balance 09:00Z: 4978 remaining / 22 used, equal to the specialist's final; delta across the single paid call 4979 -> 4978", "result": "pass (1 of 20)"},
        {"check": "caller comparison structural coverage via pixl_request_review", "method": "attempted on packet-01", "result": "unavailable (tool requires a connected plan); the comparison stands on its own file"}
    ],
    "preservation": {
        "unchanged": ["plar.txt f26344e1...", "BRIEF.md e1202361...", "src/robot.ts d57b9a90...", "assets/robot-base.png d997cade...", "installed pixl/ (not modified)", "renderer-native/ (not modified; inputs.json hashes equal the caller's start hashes)"],
        "never_rewritten": ["packet-01 and packet-02 files", "COMPARISON.json 503de778...", "caller-coverage-check-receipt.json (its wrong 08:35Z label is clarified, not edited)", "provider responses (the 08:26:37Z pre-call clock label is clarified, not edited)", "returned rotations and ZIP", "edited west and its receipt", "all review results including the refused review.member.west.01", "state history snapshots"],
        "changed_outside_work_and_store": ["assets/robot/south.png, east.png, north.png, west.png (assigned destinations)", "production-plar.txt b6d6509a... -> 01b60be1... (assigned queue update)"],
        "paid_request_repeated": False,
        "credentials": "No token, auth configuration, secret environment variable or credential file was read by the caller or (per its result) the child; the signed upload URL was not retained."
    },
    "guided_recovery": [
        {"when": "~08:25Z", "what": "Caller comparison found four contract defects and one process step; sent to the same child; child applied them in packet-02 and dispatched under the conditional authorization without a parent packet-02 reread (disclosed above)."},
        {"when": "~08:43Z-08:46Z", "what": "Host interruption recovery in this persisted session: state re-read, packet-02 completion review and clock/interruption note written, same child resumed with explicit no-repeat, no-overwrite, no-relabel rules."},
        {"when": "08:47Z-08:56Z", "what": "Child completed reviews (raw west failed honestly), family plan/delivery, renderer capture+check, PLAR update, handoff and SPECIALIST-RESULT.json; one review attempt (review.member.west.01) was refused by the runtime and retained; no paid work."},
        {"when": "08:59Z-09:0xZ", "what": "Caller independent consumption and this result."}
    ],
    "limitations": [
        "West is an edited local derivative (Pillow horizontal mirror of the official east), not an official generated west. The assignment's 'deterministic PixelLab corrections' wording was met in effect (an exact flip is deterministic and identical however produced) but the route was local Pillow, not a PixelLab tool; recorded as a route deviation, not hidden.",
        "The parent did not reread packet-02 before the paid call; the conditional authorization and the child's faithful application are the only pre-dispatch controls. The post-dispatch completion review found no defect.",
        "The bounded renderer pass is not game-engine qualification; M1/M2 and broader M3 remain open; general artistic quality and host reliability are not closed by this run.",
        "Runtime lineage marks remote_verified false; provider execution rests on the host's actual call, returned IDs (object 2a3cb51a..., background job ea834364...) and downloaded bytes, retrievable on the account for independent checking.",
        "The derived PLAR continuation reports selection_current false / review_contract because the delivery-time PLAR update changed the requirements_hash; no pending or new request exists. Any further generation needs a fresh caller comparison and pixl_plar_prepare revise against requirements_hash e3918fbaa7fcedf4be73603cd83448c4bde6f043a58f45f16a39417372a142f7 and the remaining original budget (19 of 20).",
        "The host image tool does not report delivered pixel dimensions; 1x viewing is attested by the 32x32 files and the Pillow measurements.",
        "Two early timestamp labels (caller '08:35Z approx', child pre-call '08:26:37Z') are imprecise; they are clarified append-only in caller-clock-clarification-and-recovery.json using the preserved native chronology."
    ],
    "next_action": "None pending for this assignment. If an unedited official west is ever required, start a new revision with a fresh caller comparison (e.g. a different seed or the Pro rotate fallback) within the remaining 19 generations; otherwise the delivered family stands as reviewed. M1/M2 and broader M3 remain open."
}
out = Path('work/native-production/CALLER-RESULT.json')
out.write_text(json.dumps(doc, indent=2), encoding='utf-8')
print(sha(out))
