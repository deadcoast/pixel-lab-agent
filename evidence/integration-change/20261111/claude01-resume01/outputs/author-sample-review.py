"""Author the explicit sample candidate review JSON from actually inspected files (hashes read from disk)."""
import datetime
import hashlib
import json

W = "work/integration-change/"
ctx = json.load(open(W + "sample-review-context.json", encoding="utf-8"))
G = "r.5b1bc38638b68ed8."


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


obs = [
    (W + "working-asset-check.json", "local",
     "Frozen-kit asset-check of assets/working.png: pass, sha256 cf101610..., 64x16, 128 visible pixels, 9 visible colours, 0 fractional-alpha pixels (alpha only 0/255), bbox 3,2-62,14. Per-frame Pillow crop: each 16x16 frame has 32 opaque pixels, identical 9-colour cool-blue set; bytes equal the fixture exact_art hash."),
    (W + "views/working-frames-12x-panel.png", "visual",
     "Nearest 12x enlargement of the four frames side by side on #172336 (delivered 1008x288). Each frame is a broken ring of three short cool-blue arcs; the gap positions advance clockwise frame to frame, giving four distinct rotation phases. No check mark, no closed ring, no terminal/success pose. Clusters are deliberate 1-2 px stepped arcs with a slightly lighter highlight pixel per arc."),
    (W + "views/family-strip-8x-panel.png", "visual",
     "8x strip on #172336: Ready check, Retry circular arrow, Paused bars, then Working frames 0-3 (delivered 1152x192). All share the cool-blue accent and stepped-edge treatment of the adopted Ready baseline. Working reads as segmented activity; Retry is a near-complete ring with an arrowhead; Paused is two vertical bars; Ready is an asymmetric check."),
    (W + "views/family-strip-8x-grayscale.png", "visual",
     "Same 8x strip converted to grayscale. Without colour, Working (three separated arcs with gaps) remains distinguishable from Retry (continuous ring plus arrowhead), Ready (check) and Paused (bars). Working and Retry are the closest pair (both circular); the gaps/segmentation and the rotation keep them apart."),
    (W + "views/working-sheet-3x-panel.png", "visual",
     "3x nearest view of the whole 64x16 sheet on #172336 (delivered 204x60): four crisp frames, transparent background composites cleanly onto the panel with no matte or halo."),
    (W + "capture-sample/destination.png", "visual",
     "Actual browser destination screenshot 1280x1000 from the renderer-integration capture: Current queue state panel plus the State comparison matrix with Full 1x/3x and Compact 1x/3x columns for idle/running/paused/succeeded/failed. Running shows the Working spinner with the label Working in both consumers at both scales; 1x cells read as a small blue spinner, 3x cells as crisp pixel blocks on the dark panel."),
    (W + "capture-sample/view-005.png", "visual", "statusCell running 3x canvas (48x48) painted by the real consumer: frame 0 arcs, nearest blocks, panel background."),
    (W + "capture-sample/view-007.png", "visual", "compactStatus running 3x canvas (48x48): pixel-identical to the statusCell cell for the same frame."),
    (W + "capture-sample/view-004.png", "visual", "statusCell running 1x canvas (16x16) delivered at native 16x16: tiny but legible blue spinner silhouette on the panel."),
    (W + "capture-sample/view-031.png", "visual", "Live playback sample t=153.7 ms, statusCell 3x, frame 1: arcs rotated one phase from frame 0."),
    (W + "capture-sample/view-034.png", "visual", "Live playback sample t=303.8 ms, compactStatus 3x, frame 2: next rotation phase."),
    (W + "capture-sample/view-036.png", "visual", "Live playback sample t=453.7 ms, compactStatus 3x, frame 3: last phase before the wrap to frame 0 at t=603.8 ms."),
    (W + "capture-sample/render.json", "live",
     "Raw browser capture report (Chrome/157.0.8103.39, DPR 1, viewport 1280x1000): display.frameMs=150 via src/queue-view-integration.ts + src/working-timing.ts; playback status observed with 13 requestAnimationFrame samples at ~150 ms spacing covering frames 0-3 in both statusCell and compactStatus at 3x, with three last-to-first wraps (603.8, 1203.7, 1803.7 ms); controlled 1x elapsed-time boundary samples at 0/149/150/299/300/449/450/599/600 ms; served assets/working.png sha256 cf101610...; no script errors; no missing assets."),
    (W + "renderer-check-sample.json", "live",
     "renderer-integration/check.py over that capture: status pass, 0 failures, 406 observations, 20 available views: identities, nearest sampling settings, screenshot/canvas correspondence, PNG compositing within tolerance 1, nearest blocks, frame-boundary crops and live playback (consumer frame duration 150 ms, consecutive frames without skips, both consumers, two or more wraps)."),
]
observations = [{"path": p, "sha256": sha(p), "mode": m, "note": n} for p, m, n in obs]
review = {
    "version": 1,
    "binding_hash": ctx["binding_hash"],
    "reviewer": "actor",
    "observed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "observations": observations,
    "verdicts": [
        {"criterion": G + "criterion.working.canvas", "status": "pass", "supersedes": None, "observations": [0],
         "reason": "Fresh local measurement: exact retained 64x16 transparent sheet with four horizontal 16x16 frames, alpha only 0/255, bytes sha256 cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc unchanged."},
        {"criterion": G + "criterion.working.activity", "status": "pass", "supersedes": None, "observations": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
         "reason": "Fresh visual inspection at native 1x (browser cells and screenshot) and enlarged 3x/8x/12x nearest on #172336: cool-blue three-arc broken ring with four distinct rotation phases reads as ongoing activity, never as a check or terminal pose; transparent compositing is clean; the treatment (stepped clusters, cool-blue accent, slight highlight) is coherent with the adopted Ready baseline; in colour and in grayscale it stays distinct from Ready (check), Retry (solid ring + arrowhead) and Paused (bars)."},
        {"criterion": G + "criterion.working.integration", "status": "pass", "supersedes": None, "observations": [12, 13],
         "reason": "Actual renderer-integration browser execution of the real modules: both statusCell and compactStatus painted the exact served sheet with nearest filtering on the dark panel, looping frames 0-3 at the authorized 150 ms (600 ms cycle) observed live at 3x across three wraps, and 1x/3x stills verified; check.py passed with zero failures. 1x live playback was not performed (only 1x boundary samples)."},
    ],
    "action": "complete",
    "next_action": "Adopt this accepted revised sample as the family baseline for a stages:[] delivery plan, snapshot the package, then import the fresh destination capture and review the delivery candidate.",
    "limitations": [
        "Live loop playback was observed only at the consumer's 3x scale; native 1x live playback remains unperformed (controlled 1x frame-boundary samples are a separate observation).",
        "Host image delivery of the 16x16 1x cells is tiny; 1x readability was judged from the native-size destination screenshot and the 1x cell images together with the enlarged views.",
        "Working and Retry share a circular silhouette family; their non-colour distinction rests on segmentation (three gaps) versus a continuous ring with an arrowhead, plus Working's motion.",
        "assets/start.svg is a vector and was seen only inside the browser capture, not in the Pillow comparison strips.",
        "This acceptance is scoped to the controlled reused-art 150 ms timing change; it is not PixelLab-generated quality evidence and does not close M1/M2 or broader M3.",
    ],
}
text = json.dumps(review, indent=2, ensure_ascii=False) + "\n"
open(W + "sample-review-observation.json", "w", encoding="utf-8", newline="\n").write(text)
print(json.dumps({"sha256": hashlib.sha256(text.encode()).hexdigest(), "observations": len(observations), "expect": ctx["state_hash"]}))
