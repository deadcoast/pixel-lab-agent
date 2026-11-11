"""Author the explicit delivery (family) candidate review from actually inspected files; hashes read from disk."""
import datetime
import hashlib
import json

W = "work/integration-change/"
ctx = json.load(open(W + "delivery-context.json", encoding="utf-8"))
imp = json.load(open(W + "destination-import.json", encoding="utf-8"))
Q = "delivery-150.delivery.q."


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


obs = [
    # local
    (W + "package-and-art-hashes.txt", "local",
     "sha256sum listing taken after the snapshot: package copy deliveries/873d6917.../files/0000.png == assets/working.png == cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc; start.svg ee2ba2fe..., ready-confirmed.png fc5e43ae..., error-retry.png 0fb0ab5e..., paused.png 80d2b823... all equal the fixture exact_art hashes; src/queue.ts, src/queue-view.ts, src/queue-view-integration.ts, BRIEF.md and plar.txt unchanged; src/working-timing.ts c42dd78d... and WORKING-TIMING-AMENDMENT.md 5b78962f... are the two controlled changes."),
    (W + "delivery-build.json", "local",
     "family-snapshot result: manifest 873d6917..., one member r.5b1bc38638b68ed8.output.working selected candidate r.5b1bc38638b68ed8.candidate.working.retained, created unaccepted (accepted:false, remote_executed:false)."),
    (W + "working-asset-check.json", "local",
     "Frozen-kit asset-check of assets/working.png: 64x16, 128 visible pixels, alpha only 0/255, sha256 cf101610..."),
    # visual
    (W + "capture-delivery/destination.png", "visual",
     "Fresh delivery capture screenshot 1280x1000 (Chrome/157): Current queue state panel (succeeded/Ready in both consumers) and the State comparison matrix. Running row: Full 1x, Full 3x, Compact 1x, Compact 3x all show the Working spinner with the Working label; idle/paused/succeeded/failed rows show Start/Paused/Ready/Retry. At 1x the spinner is a small cool-blue broken ring; at 3x it is crisp nearest blocks on the #172336 panel; no halo or matte."),
    (W + "capture-delivery/view-005.png", "visual", "statusCell running 3x (48x48), frame 0 painted by the real consumer on the dark panel."),
    (W + "capture-delivery/view-007.png", "visual", "compactStatus running 3x (48x48), frame 0: pixel-identical to the statusCell cell."),
    (W + "capture-delivery/view-004.png", "visual", "statusCell running 1x (16x16 native): small but legible blue spinner silhouette."),
    (W + "capture-delivery/view-006.png", "visual", "compactStatus running 1x (16x16 native): identical to the statusCell 1x cell."),
    (W + "capture-delivery/view-033.png", "visual", "Live sample t=304.8 ms statusCell 3x frame 2."),
    (W + "capture-delivery/view-040.png", "visual", "Live sample t=754.8 ms compactStatus 3x frame 1 (second loop)."),
    (W + "capture-delivery/view-051.png", "visual", "Live sample t=1654.8 ms statusCell 3x frame 3 (last phase of the third loop)."),
    (W + "capture-delivery/view-053.png", "visual", "Live sample t=1804.8 ms statusCell 3x frame 0 after the third last-to-first wrap; matches frame 0 of the sheet."),
    (W + "views/family-strip-8x-panel.png", "visual", "8x family strip on #172336: Ready, Retry, Paused, Working f0-f3 share the cool-blue stepped-cluster treatment; Working is the only segmented/rotating glyph."),
    (W + "views/family-strip-8x-grayscale.png", "visual", "Grayscale 8x family strip: Working (three separated arcs) remains distinct from Retry (continuous ring + arrowhead), Ready (check) and Paused (bars) without colour."),
    (W + "views/working-frames-12x-panel.png", "visual", "12x frames: four distinct rotation phases of the three-arc ring; no closed/success pose."),
    # live
    (imp["observation"]["path"], "live",
     "Destination import bundle (ZIP) for delivery-150.package: retains destination-report.json, canonical manifest, renderer-integration sources, served consumer sources and assets, all 55 capture PNGs and the screenshot; files_verified true, renderer_executed false, state_changed false, automatic_acceptance false. Supplied motion: statusCell and compactStatus requestAnimationFrame playback observed, 13 samples each at frame_ms 150, plus 9 controlled 1x boundary samples."),
    (W + "renderer-check.json", "live",
     "renderer-integration/check.py over capture-delivery: status pass, 0 failures, 406 observations, 20 views: served byte identities, nearest sampling, screenshot/canvas correspondence, PNG compositing, nearest blocks, frame-boundary crops, live playback at consumer frame duration 150 ms without skips in both consumers, wrap observed twice or more."),
    (W + "capture-delivery/render.json", "live",
     "Raw browser capture: display.frameMs 150 from src/queue-view-integration.ts + src/working-timing.ts; playback observed with 13 samples at 4.8, 154.9, 304.8 ... 1804.8 ms cycling frames 0-3 with wraps at 604.8, 1204.8 and 1804.8 ms in both statusCell and compactStatus at 3x; timeline 1x boundary samples 0/149/150/299/300/449/450/599/600 ms; served assets/working.png cf101610...; no errors, no missing assets."),
    (W + "destination-report.json", "live",
     "observation.py bridge report for candidate delivery-150.package / binding e9fce8bf...: destinations map r.5b1bc38638b68ed8.output.working -> assets/working.png verified against served bytes; renderer and consumer source identities; views and motion records."),
]
observations = [{"path": p, "sha256": sha(p), "mode": m, "note": n} for p, m, n in obs]
idx = {p: i for i, (p, _, _) in enumerate(obs)}
local = [i for i, (_, m, _) in enumerate(obs) if m == "local"]
visual = [i for i, (_, m, _) in enumerate(obs) if m == "visual"]
live = [i for i, (_, m, _) in enumerate(obs) if m == "live"]
review = {
    "version": 1,
    "binding_hash": ctx["binding_hash"],
    "reviewer": "actor",
    "observed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "observations": observations,
    "verdicts": [
        {"criterion": Q + "bytes", "status": "pass", "supersedes": None, "observations": local,
         "reason": "Package member files/0000.png, the served destination assets/working.png and the fixture exact_art hash are all cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc; the other four original art files hash unchanged."},
        {"criterion": Q + "continuity", "status": "pass", "supersedes": None, "observations": visual,
         "reason": "In the fresh destination screenshot and the 1x/3x cells of both consumers, the delivered Working sheet keeps the cool-blue stepped-cluster treatment of the adopted Ready baseline, reads as one coherent rotating activity sequence across the live samples (no success or terminal pose), and stays distinguishable from Ready, Retry and Paused in colour and in grayscale."},
        {"criterion": Q + "destination", "status": "pass", "supersedes": None, "observations": live,
         "reason": "Fresh renderer-integration browser capture: both statusCell and compactStatus painted the served assets/working.png with nearest filtering on #172336, looping frames 0-3 at display.frameMs 150 (600 ms cycle) with three last-to-first wraps at the consumer 3x scale; check.py passed with zero failures over the 1x/3x stills and live playback; the destination import verified every declared byte. 1x live playback was not performed and is not claimed."},
    ],
    "action": "complete",
    "next_action": "Reread the selected PLAR row and hand off; broader artistic production, host reliability, M1/M2 and broader M3 remain open outside this controlled timing change.",
    "limitations": [
        "Live loop playback observed only at the consumer 3x scale; native 1x live playback remains unperformed (1x boundary samples are a separate controlled observation).",
        "Browser evidence comes from one local Chrome 157 headless run of the isolated renderer-integration fixture; it is not acceptance by another engine or project.",
        "Acceptance is scoped to this controlled reused-art 150 ms timing change; it is not PixelLab-generated quality evidence and does not close M1/M2 or broader M3.",
        "Working and Retry share a circular silhouette family; their non-colour distinction rests on segmentation versus a continuous ring with arrowhead plus Working motion.",
    ],
}
text = json.dumps(review, indent=2, ensure_ascii=False) + "\n"
open(W + "delivery-review-observation.json", "w", encoding="utf-8", newline="\n").write(text)
print(json.dumps({"sha256": hashlib.sha256(text.encode()).hexdigest(), "observations": len(observations), "expect": ctx["state_hash"]}))
