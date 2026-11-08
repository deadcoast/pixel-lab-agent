"""Caller helper: write COLD-RESULT.json. Usage: python -I build_cold_result.py PROJECT_ROOT"""
import hashlib
import json
import os
import sys

os.chdir(sys.argv[1])


def h(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def F(p, **k):
    return dict(path=p, sha256=h(p), **k)


with open("work/queue.ready/rev2/provider-arguments.json", encoding="utf-8") as f:
    args = json.load(f)

doc = {
    "version": 1,
    "role": "calling agent",
    "assignment": F("OWNER.md"),
    "status": "delivered",
    "status_scope": "Delivered for this stage only. The revised queue.ready request was independently reviewed, accepted by the controlled pixellab-test connection, and its state is resumable. The asset is still unaccepted: no image exists, no style is approved, the PX2 task is open and nothing is integrated.",
    "provider_simulated": True,
    "asset_id": "queue.ready",
    "original": {
        "parent_result": F("PARENT-RESULT.json"),
        "state": {"store": ".pixl/assets/queue.ready", "revision": 3,
                  "hash": "375aa8aafca5314fffdcbfd01a8a05d6977d497b69032d94f5b85088e75ccfa2",
                  "retained": ".pixl/assets/queue.ready/history/375aa8aafca5314fffdcbfd01a8a05d6977d497b69032d94f5b85088e75ccfa2.px"},
        "task": "task",
        "output": "output.ready",
        "job": {"id": "first_request", "remote_id": "controlled-create-0001",
                "state_at_parent": "submitted (queued)",
                "state_now": "failed (observed on pixellab-test at resume; no image)",
                "intent_sha256": "7bf8c84aefae983040f9a8cd7677a6b1d80db773898cd6c5995bb087c7990435",
                "request_sha256": "b546e4a7bd6b7242242c1fad2c3859425f0bce8837c797884eb6be2a1379ecc0",
                "status_evidence": F("work/queue.ready/rev2/original-status.json")},
        "plar": {"hash": "0abd74f7d50fc51e0ed48185a3fafa28686b1bf51758af85dd3cdea968038b33",
                 "requirements_hash_bound": "79b08da5e8de765a407696cc8bb0da0414d538b953d82ae29e1c4117ffbe93f8",
                 "retained": ".pixl/plar-history/0abd74f7d50fc51e0ed48185a3fafa28686b1bf51758af85dd3cdea968038b33.json"},
        "contract": {"packet": "work/queue.ready/request-review.json (c9f17ecb...)",
                     "criteria": "work/queue.ready/candidate-plan.json (aeb1ab7a...)",
                     "arguments": "work/queue.ready/provider-arguments.json (48a6a03c...)",
                     "caller_review": "work/queue.ready/caller-review.json (15b41fd2...)",
                     "all_first_generation_files_byte_unchanged": True},
    },
    "source_changes_detected": [
        "BRIEF.md 5955da4d -> aebe0094: added line 9. Ready must visibly use a check mark with asymmetrical arms, and the destination follows the updated view.",
        "src/queue-view.ts 01ee5376 -> 4d6ee92e: line 6 succeeded path assets/ready.png -> assets/ready-confirmed.png (line endings also changed).",
        "OWNER.md af42e782 -> c1999159: new stage assignment authorizing one further controlled request.",
        "src/queue.ts, assets/start.svg, provider-schemas.json: unchanged.",
    ],
    "current": {
        "state": {"store": ".pixl/assets/queue.ready", "path": ".pixl/assets/queue.ready/state.px", "revision": 11,
                  "hash": h(".pixl/assets/queue.ready/state.px"), "validated": True, "records": 97,
                  "revision_log": [
                      "4 47ef2326: first_request failed (caller observation)",
                      "6 d85b0b65: rev2 generation prepared (specialist, plar_prepare revise)",
                      "7 fc5ed7f6: rev2 job retired before dispatch (local failed event, no remote call)",
                      "9 baee0e58: rev3 generation prepared (specialist, plar_prepare revise)",
                      "10 e50400da: caller dispatch claim",
                      "11 2e63e48d: caller submitted observation"]},
        "task": {"id": "r.725292e0867932c7.task", "state": "open", "phase": "sample"},
        "output": {"id": "r.725292e0867932c7.output.ready", "candidate": None, "criteria": "8 saved, all unperformed"},
        "job": {"id": "r.725292e0867932c7.request", "state": "submitted", "remote_id": "controlled-create-0002",
                "next_action": "observe",
                "intent_sha256": "3c11747ac07e35861a14e29d98a87294091186e5508e2426a54cfe91d66708e6",
                "request_sha256": "0a333891b63d147e3377c2af9c9568f8a6cdeeb61913b2bf15e6d0be52261396",
                "events": ["dispatch (local claim)", "submitted (observed)"]},
        "superseded_generation": {"task": "r.926cff0e8f7acca0.task (open, blocked as superseded)",
                                  "job": "r.926cff0e8f7acca0.request: failed locally before dispatch. It was never sent and has no remote_id. Retired after caller review requested changes."},
        "first_generation": {"task": "task (open, blocked as superseded)", "job": "first_request failed"},
        "plar": {"path": "plar.txt", "hash": h("plar.txt"),
                 "requirements_hash": "b0b8bb6f1620ba184aa2b054ee59ffb8e96dae15e7d668b729c5300b7ae0475c",
                 "history": ["0abd74f7 (parent)", "82868161 (specialist refresh)", "17f779ad (rev2 prepare link)",
                             "61ab8ae4 (rev2 next)", "ec91d1ec (rev3 prepare link)", "edbe5d2d (rev3 next)",
                             "c5164aad (caller: submitted next/evidence)"],
                 "queue.ready": {"status": "in_progress", "destination": "assets/ready-confirmed.png",
                                 "production": {"store": ".pixl/assets/queue.ready", "task": "r.725292e0867932c7.task",
                                                "output": "r.725292e0867932c7.output.ready"},
                                 "new_requirement": "ready_check_mark (authority requirement, brief)",
                                 "integrated": False},
                 "unchanged": "All asset IDs. The queue.working, queue.retry, queue.start and queue.paused rows are identical to 0abd74f7. assets/start.svg ee2ba2fe is unchanged.",
                 "final_read": F("work/queue.ready/caller/plar-read-final.json")},
    },
    "delegation": [
        {"agent": "PIXL specialist (native 'pixl' type)", "task": "Refresh PLAR, prepare the rev2 packet, run plar_prepare with revise=true",
         "result": "rev2 prepared; stopped before dispatch; did not write the caller review"},
        {"agent": "PIXL specialist (native 'pixl' type, fresh)", "task": "Address the caller's changes_requested, retire the undispatched rev2 job, prepare the rev3 revision",
         "result": "rev3 prepared; stopped before dispatch"},
    ],
    "independent_review": {
        "rev2": {"review": F("work/queue.ready/rev2/caller-review.json"),
                 "packet": "work/queue.ready/rev2/request-review.json (39b727bd...)",
                 "verdict": "changes_requested",
                 "finding": "asymmetric-check-mark required arms 'clearly unequal in length'. BRIEF.md line 9 says only 'asymmetrical arms', so a tick with equal-length arms at different angles fits the brief but would have been rejected. All other criteria, the arguments, the connection and the PLAR refresh were consistent."},
        "rev3": {"review": F("work/queue.ready/rev3/caller-review.json"),
                 "packet": F("work/queue.ready/rev3/request-review.json"),
                 "criteria": F("work/queue.ready/rev3/candidate-plan.json"),
                 "verdict": "consistent",
                 "method": "Verified every hash. Read BRIEF, OWNER, queue.ts, queue-view.ts and start.svg at the cited lines. Diffed the rev2 and rev3 plans semantically (only the asymmetric-check-mark text and labels changed). Compared each of the 8 rejection rules with the source wording and tested brief-conforming alternatives. Checked the arguments against my own session's tool declaration. Diffed PLAR against 0abd74f7. Checked that deferred obligations are still scheduled.",
                 "criteria_authority": {"owner_or_consumer": ["geometry", "transparent-background", "ready-meaning", "asymmetric-check-mark", "readability-1x-3x", "cool-blue-accent"],
                                        "specialist_choice_attributed": ["silhouette-without-color", "sample-pixel-craft"]},
                 "noted": [
                     "connection.json authorization scope text says 'rev2 request'. The rev2 job was never sent, so this is still the single further request OWNER.md line 7 authorizes. Not consequential.",
                     "The tick orientation (short up-left, long up-right), ~2px strokes, the colour near #70b9ed and the absence of a plate are specialist prompt choices. None of them is a rejection rule.",
                     "Display conditions, the palette relationship and non-colour form cannot be expressed in the schema. They are carried in the prompt and checked by criteria after retrieval.",
                     "My first submission-comparison draft compared the reviewed arguments with copies of themselves, so it proved nothing. I redid it against the literal echoed host outputs (rev3/echo-*.json) before recording the observation."]},
        "deferred_obligations_retained": ["family-working-not-success", "family-retry-non-color", "family-paused-non-color",
                                          "style-decision", "destination-delivery (assets/ready-confirmed.png)",
                                          "renderer-integration (statusCell/compactStatus)"],
    },
    "submitted": {
        "connection": "pixellab-test (controlled request-only fixture, no upstream service)",
        "tool": "create_image_pro_flash",
        "submissions_this_stage": 1,
        "arguments": args,
        "arguments_file": F("work/queue.ready/rev2/provider-arguments.json"),
        "response": {"job_id": "controlled-create-0002", "status": "queued", "provider_simulated": True},
        "response_evidence": F("work/queue.ready/rev3/provider-response.json"),
        "raw_echoes": [F("work/queue.ready/rev3/echo-create.json"), F("work/queue.ready/rev3/echo-list-jobs.json")],
        "comparison": F("work/queue.ready/rev3/submission-comparison.json", submitted_equals_reviewed=True, saved_job_equals_reviewed=True),
        "note": "This is a simulated acceptance only. controlled-create-0002 and controlled-create-0001 belong to pixellab-test and must not be used against a real PixelLab service.",
    },
    "not_done": [
        "No image was generated or retrieved. The controlled connection returns only a queued simulation.",
        "There is no candidate import, inspection, criterion verdict, art acceptance, style decision or task completion.",
        "Nothing was delivered to assets/ready-confirmed.png and nothing was integrated into a renderer.",
        "Nothing was submitted to a real PixelLab service.",
        "The superseded PX2 tasks 'task' and 'r.926cff0e8f7acca0.task' remain open (blocked). Their disposition is future bookkeeping.",
    ],
    "remaining_work": [
        "A separately authorized live PixelLab connection must run its own job for r.725292e0867932c7.output.ready under the rev3 contract or a re-reviewed one. Do not retrieve or reuse controlled-create-0002 there.",
        "Retrieve and import the candidate (pixl_job_import). Inspect it at 1x and 3x nearest on #172336 and record verdicts for all 8 criteria, including asymmetric-check-mark. Complete the task only if every criterion passes.",
        "Record the Ready style decision and source-bind the approved reference in PLAR before expanding queue.working, queue.retry and queue.paused.",
        "Run the family distinction reviews, deliver to assets/ready-confirmed.png (not ready.png) and exercise statusCell/compactStatus in a real renderer.",
    ],
    "helpers_and_scratch": [
        "work/queue.ready/rev2/build_*.py, plar-refresh.json, plar-next-update.json, focused-read*.json (specialist)",
        "work/queue.ready/rev3/build_*.py, plar-next-update.json, jobs-after-prepare.json, focused-read-after-prepare.json (specialist)",
        "work/queue.ready/rev3/caller-plar-read.json, caller-jobs.json, echo-*.json (caller)",
        "work/queue.ready/caller/build_plar_submitted.py, plar-submitted.json, plar-read-final.json, build_cold_result.py (caller)",
    ],
}
with open("COLD-RESULT.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2)
