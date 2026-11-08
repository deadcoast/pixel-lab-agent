"""Caller helper: assemble COLD-RESULT.json from retained artifacts. Run from the consumer root."""
import hashlib
import json


def H(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


args = json.load(open("work/queue.ready/rev3/provider-arguments.json"))
STATE = ".pixl/assets/queue.ready/state.px"
RQ = "244f459131251b6de7f6c7e8b3afa109f3475f87772ab6f5473c158948fa8b0a"

res = {
    "version": 1,
    "role": "calling agent",
    "assignment": {"path": "OWNER.md", "sha256": H("OWNER.md")},
    "status": "delivered",
    "status_scope": (
        "Delivered for this stage only. The revised, independently reviewed queue.ready request was "
        "accepted (simulated queued) by the controlled pixellab-test connection, and its resumable local "
        "state is retained. No image exists, the asset is unaccepted, PX2 task r.028f320bf7292612.task "
        "remains open, and integration and art acceptance are future work."
    ),
    "provider_simulated": True,
    "asset_id": "queue.ready",
    "original": {
        "source": "PARENT-RESULT.json (unchanged)",
        "parent_result_sha256": H("PARENT-RESULT.json"),
        "assignment_sha256": "af42e78210c92389d30f8e7b18d74861c28b4bb6c91245198c85f797297f927a",
        "requirements_hash": "79b08da5e8de765a407696cc8bb0da0414d538b953d82ae29e1c4117ffbe93f8",
        "plar_hash": "0abd74f7d50fc51e0ed48185a3fafa28686b1bf51758af85dd3cdea968038b33",
        "state": {"revision": 3, "hash": "375aa8aafca5314fffdcbfd01a8a05d6977d497b69032d94f5b85088e75ccfa2"},
        "task": "task",
        "output": "output.ready",
        "job": {
            "id": "first_request",
            "remote_id": "controlled-create-0001",
            "state_at_parent": "submitted",
            "state_now": "failed",
            "next_action": "review_failure",
        },
        "packet": {
            "path": "work/queue.ready/request-review.json",
            "sha256": "c9f17ecb78e1346de3125e930467e611e31c7956e722e6b2bc3cfe45e7cf818a",
        },
        "first_generation_artifacts_verified_unchanged": True,
    },
    "provider_status_inspection": {
        "action": "Before acting, the caller called mcp__pixellab-test__list_jobs on the originating controlled connection.",
        "observed": (
            "controlled-create-0001 status failed: 'Controlled continuation fixture: the original queued attempt "
            "has ended without an image.' Echoed arguments equal the original reviewed provider-arguments.json."
        ),
        "evidence": {
            "path": "work/queue.ready/provider-observation-failed.json",
            "sha256": H("work/queue.ready/provider-observation-failed.json"),
        },
        "recorded": "pixl_job_observe failed on first_request -> state revision 4 (b9c3a2f7b4d93448cdb80a1a67dac4f4616f72a88ff085568b76a6ac76067d18)",
    },
    "plar_refresh": {
        "by": "PIXL specialist (native agent type 'pixl'), via the packaged plar save",
        "changes": [
            "BRIEF.md and src/queue-view.ts rebound to aebe0094... / 4d6ee92e...",
            "queue.ready destination/existing/delivery moved assets/ready.png -> assets/ready-confirmed.png (same ID and role)",
            "sample_motif proposal replaced by completion_mark requirement (BRIEF.md:9 check mark with asymmetrical arms)",
            "delivery check added for the asymmetrical-arm check mark",
        ],
        "preserved": (
            "IDs queue.paused, queue.retry, queue.start and queue.working are byte-equal to the retained prior version "
            "(caller-verified diff). assets/start.svg is unchanged (ee2ba2fe...). Prior PLAR versions are retained in "
            ".pixl/plar-history/."
        ),
        "requirements_hash": RQ,
        "plar_hash_history": [
            "0abd74f7... (parent)", "874f69c8... (refresh)", "1a2819cd... (rev2 link)", "99944719... (rev2 next)",
            "f43b994a... (rev3 link)", "e3a76273... (rev3 next)", "32e1590f... (caller: submitted)",
        ],
    },
    "independent_review": {
        "reviewer": "calling agent; the specialist did not write or perform it",
        "rev2": {
            "packet": {"path": "work/queue.ready/rev2/request-review.json", "sha256": H("work/queue.ready/rev2/request-review.json")},
            "caller_review": {"path": "work/queue.ready/rev2/caller-review.json", "sha256": H("work/queue.ready/rev2/caller-review.json")},
            "verdict": "changes_requested",
            "finding": (
                "check-mark-asymmetrical-arms required 'two arms of clearly unequal length', narrowing BRIEF.md:9 "
                "'asymmetrical arms'. A similar-length, different-angle check mark, which conforms to the brief, would "
                "have been rejected."
            ),
            "disposition": (
                "Undispatched rev2 job r.f9e2fa53f4fcac2a.request was withdrawn locally with an evidenced failed "
                "observation (no remote id; provider never contacted). The specialist was re-delegated to correct "
                "only that criterion."
            ),
            "withdrawal": {"path": "work/queue.ready/rev2/withdrawal.json", "sha256": H("work/queue.ready/rev2/withdrawal.json")},
        },
        "rev3": {
            "packet": {"path": "work/queue.ready/rev3/request-review.json", "sha256": H("work/queue.ready/rev3/request-review.json")},
            "criteria": {"path": "work/queue.ready/rev3/candidate-plan.json", "sha256": H("work/queue.ready/rev3/candidate-plan.json")},
            "locator_report": {
                "path": "work/queue.ready/rev3/request-review-report.json",
                "sha256": H("work/queue.ready/rev3/request-review-report.json"),
                "diagnostics": [],
            },
            "caller_review": {"path": "work/queue.ready/rev3/caller-review.json", "sha256": H("work/queue.ready/rev3/caller-review.json")},
            "verdict": "consistent",
            "summary": (
                "Programmatic diff against rev2 showed only the asymmetry criterion changed. Its condition, 'not "
                "mirror-symmetric about its vertex', is equivalent to the source. The 8 rejection criteria were each "
                "compared with source wording (6 owner/consumer requirements, 2 scoped specialist proposals). Family "
                "distinctions, style decision, delivery to assets/ready-confirmed.png and renderer integration stay "
                "deferred with a stage and prerequisites."
            ),
        },
        "unresolved_findings": [],
        "noted_non_blocking": [
            "The reason text for choices.motif-construction mentions 'visibly unequal arm length' (explanatory, not a rule).",
            "The prompt's short-left/long-right orientation is a specialist prompt choice, not a rejection rule.",
            "The description prose carries display conditions, palette relationship and non-colour form that the advertised schema cannot express.",
        ],
    },
    "submission": {
        "connection": "pixellab-test (controlled request-only fixture, no upstream service)",
        "tool": "create_image_pro_flash",
        "dispatch_claim": "pixl_job_dispatch r.028f320bf7292612.request at state 4152fa99... -> revision 10 (7513f614...)",
        "submitted_arguments": args,
        "reviewed_arguments": {"path": "work/queue.ready/rev3/provider-arguments.json", "sha256": H("work/queue.ready/rev3/provider-arguments.json")},
        "request_sha256": "7adba38229de8f11eee3b78aac2c5c251dbca6208b733b839a3bc0424101f400",
        "submissions_this_stage": 1,
        "response": {"job_id": "controlled-create-0002", "status": "queued", "provider_simulated": True},
        "response_evidence": {"path": "work/queue.ready/rev3/provider-response.json", "sha256": H("work/queue.ready/rev3/provider-response.json")},
        "comparison": {
            "path": "work/queue.ready/rev3/submission-comparison.json",
            "sha256": H("work/queue.ready/rev3/submission-comparison.json"),
            "submitted_equals_reviewed": True,
        },
        "note": "Simulated acceptance only. controlled-create-0002 belongs to pixellab-test and must not be retrieved from or reused on a real PixelLab service.",
    },
    "current": {
        "plar": {
            "path": "plar.txt",
            "hash": H("plar.txt"),
            "requirements_hash": RQ,
            "selection_current": True,
            "queue.ready": {
                "status": "in_progress",
                "production": {"store": ".pixl/assets/queue.ready", "task": "r.028f320bf7292612.task", "output": "r.028f320bf7292612.output.ready"},
                "integrated": False,
            },
        },
        "state": {"store": ".pixl/assets/queue.ready", "state_path": STATE, "revision": 11, "hash": H(STATE), "validated": True, "phase": "sample"},
        "tasks": [
            {"id": "r.028f320bf7292612.task", "state": "open", "current": True, "output": "r.028f320bf7292612.output.ready",
             "candidate": None, "criteria": "8 saved, all unperformed (no candidate image)"},
            {"id": "r.f9e2fa53f4fcac2a.task", "state": "open", "current": False,
             "note": "rev2 generation retained; plar_selection blocker; its job was withdrawn"},
            {"id": "task", "state": "open", "current": False,
             "note": "first generation retained; plar_selection blocker (requirements changed)"},
        ],
        "jobs": [
            {"id": "r.028f320bf7292612.request", "state": "submitted", "remote_id": "controlled-create-0002", "next_action": "observe",
             "intent_sha256": "77beced673e88a5ad8a5f8e1613347a587c41e9aa83b23c6fc0a4e9311695505",
             "events": ["dispatch (local claim)", "submitted (observed)"]},
            {"id": "r.f9e2fa53f4fcac2a.request", "state": "failed", "remote_id": None, "note": "withdrawn before dispatch; local evidence only"},
            {"id": "first_request", "state": "failed", "remote_id": "controlled-create-0001", "note": "observed failed on originating connection, no image"},
        ],
    },
    "resume": {
        "store": ".pixl/assets/queue.ready",
        "state_hash": H(STATE),
        "asset_id": "queue.ready",
        "requirements_hash": RQ,
        "task": "r.028f320bf7292612.task",
        "action": "observe",
        "jobs": [{"id": "r.028f320bf7292612.request", "provider": "pixellab-test", "remote_id": "controlled-create-0002",
                  "state": "submitted", "next_action": "observe"}],
        "before_another_request": [{"job": "r.028f320bf7292612.request", "action": "observe",
                                    "requirement": "Resolve this retained attempt on its originating connection before preparing another request for this asset."}],
    },
    "next": "Observe controlled-create-0002 on the controlled pixellab-test connection and record its actual outcome before any other request for queue.ready.",
    "not_done": [
        "No image was generated or retrieved; the controlled connection returned only a queued simulation.",
        "No candidate import, inspection, criterion verdicts, art acceptance, style decision, task completion, delivery to assets/ready-confirmed.png or renderer integration.",
        "No submission to any real PixelLab service. The connection's one further request for this stage is now used.",
    ],
    "remaining_work": [
        "Resolve controlled-create-0002 on its originating connection (observe; preserve queued/unknown outcomes).",
        "On success with bytes, retrieve and pixl_job_import against r.028f320bf7292612.output.ready, prepare inspection at 1x/3x nearest on #172336, record verdicts for the 8 rev3 criteria and complete the task only if all pass. On failure, retain it; any live production needs a separately authorized connection and a new job.",
        "Record the Ready style decision and source-bind the approved reference in PLAR before expanding queue.working, queue.retry and queue.paused.",
        "Run the family distinction reviews (Working not success; Retry and Paused distinguishable without colour), deliver to assets/ready-confirmed.png, and exercise statusCell/compactStatus in a real renderer.",
        "Earlier-generation tasks 'task' and r.f9e2fa53f4fcac2a.task remain open with plar_selection blockers. They are retained as history and were not closed in this stage.",
    ],
    "helpers_and_scratch": [
        "work/queue.ready/rev2/*.py, work/queue.ready/rev3/*.py (specialist helpers)",
        "work/queue.ready/rev2/plar-*.json, work/queue.ready/rev3/plar-*.json (specialist PLAR save inputs/reads)",
        "work/queue.ready/caller/plar-update-rev3-submitted.json, work/queue.ready/caller/write_cold_result.py (caller)",
    ],
    "previous_artifacts_preserved": "PARENT-RESULT.json and every first-generation work/queue.ready/*.json and rev2 file are unmodified (hash-verified).",
}
open("COLD-RESULT.json", "w").write(json.dumps(res, indent=2) + "\n")
print(H("COLD-RESULT.json"))
