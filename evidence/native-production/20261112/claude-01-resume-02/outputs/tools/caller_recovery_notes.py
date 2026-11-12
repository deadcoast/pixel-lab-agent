"""Caller: packet-02 completion review (post-dispatch) and append-only clock/interruption note.
Run from the consumer root with the assignment Python using -I; pass the current UTC clock as argv[1].
"""
import json, hashlib, sys
from pathlib import Path

now = sys.argv[1]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

p2 = 'work/native-production/packet-02/'
doc = {
    "version": 1,
    "kind": "caller completion review of packet-02 (post-dispatch)",
    "reviewer": "caller (Claude Code main session, model claude-fable-5-1), persisted parent session 9d0f792b-9ac2-42e1-8131-5861ce4b1dc5",
    "reviewed_at": now,
    "native_child": "aeb8fdd3833c62981 (pixl:pixl), same child continued after host interruption",
    "chronology_disclosure": "The earlier parent SendMessage (around 08:25Z) conditionally authorized five specified corrections before paid dispatch. The child applied corrections 1-4 in packet-02 and dispatched create_object_pro_flash (dispatch claim recorded 08:26:36Z; native call start 08:26:46.369Z, return 08:26:46.712Z per the preserved raw native chronology). There was NO parent reread of packet-02 before that paid call. This file is the current completion review, written after the fact; it is not a pre-dispatch reread and does not retroactively create one.",
    "reviewed_files": {f: {"path": p2 + f, "sha256": sha(p2 + f)} for f in ["request-review.json", "provider-arguments.json", "candidate-plan.json", "connection.json", "family-plan-draft.json", "south-baseline-plan.json", "request-review-report.json", "discovery-01.json"]},
    "unchanged_from_packet_01": ["connection.json", "discovery-01.json", "family-plan-draft.json", "south-baseline-plan.json"],
    "packet_01_preserved": {"path": "work/native-production/packet-01/request-review.json", "sha256": sha("work/native-production/packet-01/request-review.json")},
    "comparison_preserved": {"path": "work/native-production/COMPARISON.json", "sha256": sha("work/native-production/COMPARISON.json")},
    "correction_checks": [
        {"n": 1, "requested": "palette argument with the three source colours", "observed": "provider-arguments.json has palette ['#25354a','#56b5bc','#f4dda2'] and palette_name 'robot-base source colours'; the dispatched job record (r.acf329804ba043b7.request, request_sha256 ca743f1d...) carries the same arguments.", "status": "applied"},
        {"n": 2, "requested": "description: rectangular posts; three colours on transparency", "observed": "description now reads 'two rectangular antenna posts' and 'in three colours (navy, teal, pale yellow) on a transparent background'.", "status": "applied"},
        {"n": 3, "requested": "identity per facing (profile may occlude a post; north need not show the teal panel)", "observed": "candidate-plan identity checks for east/west say 'the rectangular antenna post(s) as visible from that facing (one post may hide the other in profile) at the same post height'; north says 'both rectangular antenna posts ... no eyes. The teal front panel is not required on the back'.", "status": "applied"},
        {"n": 4, "requested": "move numeric tolerances out of requirement-authority proportions_volume", "observed": "proportions_volume is now qualitative; a new proposal criterion height_measure holds top in [2,4], bottom == 28, posts 6 px within 1 px.", "status": "applied"},
        {"n": 5, "requested": "re-run pixl_request_review on packet-02 and bind the prepared job to the corrected request before dispatch", "observed": "packet-02/request-review-report.json exists; the first prepared job 'first_request' was withdrawn (failed, withdrawn_before_dispatch, 0 generations) and a new job r.acf329804ba043b7.request was prepared at 08:26:26Z with the corrected arguments, dispatch-claimed 08:26:36Z, then called. Binding is correct. The parent's own reread happened only now.", "status": "applied by the child; parent verification is this file"}
    ],
    "residual_observations": [
        "Choice east/north/west contract.palette is still [] while palette_preserved and the request list the three colours; a harmless inconsistency in the PX2 contract value, noted, not a contract defect for acceptance.",
        "The identity check for east/west names 'the teal body panel' among what reads as the same robot; the generated east shows the panel as a 1-px teal front edge in strict profile. The caller reads that as the panel seen edge-on, consistent with the clause; the reviewer should say so explicitly in the verdict reason.",
        "The raw provider west (sha256 8209e5f6...) lacks the teal edge and is not the mirror of east; the child's deterministic mirror (sha256 ec96bf63...) is an EDITED candidate derived from the official east, not an official generated west. Any acceptance must label it so; the official raw west stays retained as a rejected candidate."
    ],
    "result": "consistent (packet-02 matches the COMPARISON.json dispositions and the dispatched request)",
    "not_established": "Consistency is not provider execution, visual acceptance or destination acceptance; those follow from the child's reviews, the renderer evidence and the caller's final independent inspection.",
    "next_action": "Resume child aeb8fdd3833c62981 to finish reviews, renderer capture/check, family delivery, PLAR update and handoff; then caller final inspection and CALLER-RESULT.json."
}
Path('work/native-production/COMPARISON-packet-02-completion-review.json').write_text(json.dumps(doc, indent=2), encoding='utf-8')

note = {
    "version": 1,
    "kind": "append-only clock clarification and interruption record",
    "written_at_utc_actual": now,
    "author": "caller (Claude Code main session), persisted parent session 9d0f792b-9ac2-42e1-8131-5861ce4b1dc5",
    "clarifications": [
        {"file": "work/native-production/caller-coverage-check-receipt.json", "sha256": sha("work/native-production/caller-coverage-check-receipt.json"), "original_label": "observed_at_utc '2026-11-12T08:35Z (approx, ...)'", "correction": "That label was an estimate typed by the caller. The file's own modification time is 2026-11-12T08:25:00Z and COMPARISON.json was written at 08:24:28Z, so the pixl_request_review coverage attempt was emitted around native 08:25Z, not 08:35Z. The old receipt is left unedited."},
        {"file": "work/native-production/provider/create_object_pro_flash-response.json", "sha256": sha("work/native-production/provider/create_object_pro_flash-response.json"), "original_label": "observed_at '2026-11-12T08:26:37Z'", "correction": "08:26:37Z is the pre-call clock the child read (same instant as its balance_before_call). The preserved raw native chronology gives the actual create_object_pro_flash call start 2026-11-12T08:26:46.369Z and return 08:26:46.712Z. The dispatch claim was recorded 08:26:36.062Z and the submitted event 08:26:57.597Z. The old receipt is left unedited."}
    ],
    "interruption_record": {
        "what_happened": "The original parent Claude Code process ended while waiting for child aeb8fdd3833c62981 after resuming it with the five corrections. The child had completed the paid call, download, import, deterministic west edit and visual inspection, but SPECIALIST-RESULT.json and CALLER-RESULT.json did not exist. A host task notification later reported the background agent 'stopped' with no completion record.",
        "recovery": "Same persisted parent session 9d0f792b-9ac2-42e1-8131-5861ce4b1dc5 and the SAME native child aeb8fdd3833c62981 are continued with SendMessage; no replacement child is spawned, the successful paid request (object 2a3cb51a-6cf7-485d-8441-3c3db762cc9d, background job ea834364-0f7d-42eb-876b-bb26e21e1269) is not repeated, and no earlier evidence is overwritten.",
        "state_at_recovery": {"store": ".pixl/assets/robot.directions", "revision": 12, "state_hash": "df1ae9c75fb918c827e2c0e2a6150d0b5c27f4b83479a1db5f552ceb960e7ddc", "jobs": "first_request failed/withdrawn_before_dispatch (0 gens); r.acf329804ba043b7.request succeeded, remote_id 2a3cb51a-6cf7-485d-8441-3c3db762cc9d, 1 generation", "candidates": "candidate.east.raw, candidate.north.raw, candidate.west.raw (official), candidate.west.edited (local mirror of official east), candidate.south (preserved bytes)", "criteria": "all unperformed", "families": "none", "plar_link": "unlinked", "destinations": "assets/robot/south.png only (byte-identical); east/north/west not yet written", "balance": "4978 remaining at 08:30:30Z; 1 generation consumed by this assignment"}
    }
}
Path('work/native-production/caller-clock-clarification-and-recovery.json').write_text(json.dumps(note, indent=2), encoding='utf-8')
for f in ['work/native-production/COMPARISON-packet-02-completion-review.json', 'work/native-production/caller-clock-clarification-and-recovery.json']:
    print(sha(f), f)
