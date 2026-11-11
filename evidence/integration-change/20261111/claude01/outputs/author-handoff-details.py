"""Author the PLAR handoff details (caller view) from the fresh focused read and actual retained files."""
import hashlib
import json

W = "work/integration-change/"
sel = json.load(open(W + "final-selection.json", encoding="utf-8"))


def ref(path, role):
    return {"path": path, "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(), "role": role}


prod = sel["production"]
details = {
    "status": "delivered",
    "assignment": "CF-07/NF-06 controlled Working timing change: refresh integration-plar.txt for the 150 ms amendment, resolve the obsolete 100 ms prepared request locally, prepare and locally withdraw the revised intent, review the exact retained assets/working.png as a typed candidate, deliver it through a stages:[] family plan, and verify both consumers in the real renderer-integration browser capture. No provider execution, no new art, no source edits.",
    "caller": {
        "summary": "Delivered: exact assets/working.png (sha256 cf101610...) reviewed and accepted at the amended 150 ms timing in both statusCell and compactStatus via a fresh Chrome capture (check.py pass, 3x live loop with three wraps, 1x/3x stills). Sample task and delivery task are done; package delivery-150.package retained and destination-imported. No PixelLab call, no new art. 1x live playback unperformed; M1/M2 and broader M3 remain open.",
        "artifacts": [
            ref("assets/working.png", "delivered Working sheet (exact historical bytes, unchanged)"),
            ref(".pixl/assets/queue.working/deliveries/873d6917ed6e80f3302b282b4cb9a84686f3c8e9234497f8151b9997d17f1ead/manifest.json", "delivery package manifest (delivery-150.package)"),
            ref(W + "capture-delivery/destination.png", "fresh destination screenshot, both consumers, all states"),
            ref(W + "destination-bundle/8e7eb3490e30a47a8b7abe1ff439b155d7a62214c58eb9f6c5640ae874b391d0.zip", "NF-06 destination import bundle"),
            ref("integration-plar.txt", "refreshed allocation (Working sources/timing only)"),
        ],
        "reports": [
            ref(W + "sample-review.json", "sample candidate review (complete)"),
            ref(W + "delivery-review.json", "delivery candidate review (complete)"),
            ref(W + "renderer-check.json", "check.py over the delivery capture: pass"),
            ref(W + "destination-import.json", "destination import receipt"),
            ref(W + "obsolete-dispatch.json", "actual dispatch refusal for first_request (job_blocked: plar_selection changed)"),
            ref(W + "obsolete-completion.json", "actual completion refusal for old task (plar_selection: requirements differ)"),
            ref(W + "old-abandon.json", "local failed observation of never-dispatched first_request"),
            ref(W + "new-abandon.json", "local failed observation of never-dispatched r.5b1bc38638b68ed8.request"),
            ref(W + "acceptance.json", "family report after delivery completion"),
            ref(W + "command-log.txt", "exact CLI commands run"),
        ],
        "issues": [
            {"category": "unavailable_observation", "summary": "Native 1x live loop playback was not performed; live playback was observed at the consumer 3x scale only, with separate controlled 1x frame-boundary samples.", "recovery": "If 1x live playback evidence is required, extend the renderer-integration fixture to sample 1x cells during playback and re-capture; do not infer it from the 3x samples."},
            {"category": "unfinished_work", "summary": "Acceptance is scoped to the controlled reused-art 150 ms timing change. Broader artistic production, host reliability, M1/M2 and broader M3 remain open; historical task 'task' stays open with its plar_selection blocker and failed first_request preserved.", "recovery": "Treat this delivery as the Working baseline for later work; new generation needs its own reviewed request and authorization."},
        ],
        "integration": {
            "status": "pass",
            "summary": "Fresh renderer-integration capture: statusCell and compactStatus both paint the served assets/working.png with nearest filtering on #172336 at display.frameMs 150 (600 ms cycle), frames 0-3 without skips and three last-to-first wraps at 3x; 1x/3x stills match the sheet; check.py 0 failures; destination import verified all declared bytes.",
            "evidence": [ref(W + "renderer-check.json", "check.py result"), ref(W + "capture-delivery/render.json", "raw browser capture"), ref(W + "destination-import.json", "import receipt")],
        },
    },
    "findings": {
        "visual": "Four-frame three-arc broken ring in cool blue; distinct rotation phases; no success-like pose; clean transparent compositing; coherent with the Ready baseline; distinguishable from Ready/Retry/Paused in colour and grayscale (Working/Retry closest pair).",
        "mechanical": "64x16, four 16x16 frames, alpha 0/255 only, 9 visible colours, bytes cf101610... unchanged; package copy identical; four other original art files unchanged.",
        "timing": "Amendment 150 ms per frame, 4 frames, 600 ms cycle applied by src/queue-view-integration.ts from src/working-timing.ts; observed live in both consumers.",
    },
    "caller_actions": [
        {"action": "Refreshed only Working's two changed source hashes and its animation requirement (150/600) in integration-plar.txt", "evidence": W + "allocation-save.json"},
        {"action": "Abandoned first_request and r.5b1bc38638b68ed8.request locally (never dispatched; no provider contact)", "evidence": W + "old-abandon.json; " + W + "new-abandon.json"},
    ],
    "future_work": [
        "1x live playback observation if required by a later brief.",
        "Any new Working art or PixelLab generation needs its own reviewed request, discovery and authorization.",
    ],
    "scope": "Controlled reused-art timing change only; no provider execution, no new art, no source edits.",
    "limitations": [
        "1x live playback unperformed.",
        "Single local Chrome 157 headless fixture run; not another engine's acceptance.",
        "Not PixelLab-generated quality evidence; M1/M2 and broader M3 remain open.",
    ],
    "provider": {"remote_ids": [], "jobs": {"first_request": "failed (local abandonment, never dispatched)", "r.5b1bc38638b68ed8.request": "failed (local abandonment, never dispatched)"}, "remote_executed": False},
}
text = json.dumps(details, indent=2, ensure_ascii=False) + "\n"
open(W + "handoff-details.json", "w", encoding="utf-8", newline="\n").write(text)
print(json.dumps({"requirements_hash": sel["requirements_hash"], "expect": prod["continuation"]["state_hash"], "caller_bytes": len(json.dumps(details["caller"], separators=(",", ":")).encode())}))
