import json, hashlib, sys
ts = sys.argv[1]
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
V, L, X = "visual", "live", "local"
D = "work/native-review/destination-01/"
F = "work/native-review/family-views/"
obs = [
 # --- visual: collective views
 (0, "work/live-family/family-comparison.png", V, "540x552 sheet of actual consumer pixels: Start (preserved svg), Ready baseline, Retry, Paused and Working frames 0-3 each at color 1x/3x and grayscale 1x/3x on #172336. Viewed as the primary side-by-side comparison of all members."),
 (1, "work/focused-successor/specialist-grayscale.png", V, "500x180 grayscale comparison: Working four frames at 1x and 3x, Ready check, Retry ring-arrow, Paused bars; used for the non-color structure comparison."),
 (2, F+"family-succeeded-3x-color.png", V, "Ready baseline at 3x: single-tone light sky-blue check, two stepped strokes meeting at a low point, 2 px weight, transparent exterior."),
 (3, F+"family-running-3x-color.png", V, "Working frame 0 at 3x: three azure fragments (top bar, right vertical, lower-left curve) on an open ring, subtle in-shape ramp, transparent exterior."),
 (4, F+"family-failed-3x-color.png", V, "Retry at 3x: nearly closed 2 px blue ring with an arrowhead at the top; denser and continuous compared with Working's fragments."),
 (5, F+"family-paused-3x-color.png", V, "Paused at 3x: two solid 3 px-wide vertical blue bars with a light inner edge; heaviest member."),
 (6, F+"family-idle-3x-color.png", V, "Preserved Start svg exposure at 3x: solid right-pointing triangle in the same light sky blue as Ready."),
 (7, F+"family-succeeded-3x-gray.png", V, "Ready in grayscale 3x: check stroke still reads as a check by structure alone."),
 (8, F+"family-running-3x-gray.png", V, "Working frame 0 in grayscale 3x shown alone (the reduced-motion stationary presentation): three disjoint fragments around a ring; not a check, not paired bars, not a closed ring."),
 (9, F+"family-failed-3x-gray.png", V, "Retry in grayscale 3x: closed ring plus arrowhead remains distinct from Working's open fragments and from Paused."),
 (10, F+"family-paused-3x-gray.png", V, "Paused in grayscale 3x: two parallel full-height bars, distinct from every other member."),
 (11, F+"family-idle-3x-gray.png", V, "Start in grayscale 3x: solid triangle, separately identifiable."),
 (12, F+"family-succeeded-1x-color.png", V, "Ready at native 1x: check mark reads at 16x16."),
 (13, F+"family-running-1x-color.png", V, "Working frame 0 at native 1x: small open spinner, reads as activity at rest."),
 (14, F+"family-failed-1x-color.png", V, "Retry at native 1x: ring with arrow tip, denser than Working."),
 (15, F+"family-paused-1x-color.png", V, "Paused at native 1x: two bars."),
 (16, F+"family-idle-1x-color.png", V, "Start at native 1x: triangle."),
 (17, F+"family-running-1x-gray.png", V, "Working frame 0 in grayscale 1x: still three fragments, no check or bar pair."),
 (18, F+"family-paused-1x-gray.png", V, "Paused in grayscale 1x: two bars."),
 (19, F+"family-succeeded-1x-gray.png", V, "Ready in grayscale 1x: check."),
 (20, "work/native-review/frames/family-members-12x-color.png", V, "My own 12x nearest sheet from the exact package files: Ready, Working 0-3, Retry, Paused, Start exposure, on #172336; used to compare edge treatment, cluster construction and blue accents closely."),
 (21, "work/native-review/frames/family-members-12x-gray.png", V, "Same 12x sheet in grayscale; used for the structure-only distinction read."),
 # --- visual: Working playback and stationary presentation (continuity clause)
 (22, "work/acceptance-01/headless-review-03/playback.png", V, "Supplemental playback page screenshot: Working 1x/3x color/gray beside the other members and 17 recorded 100 ms transition exposures including four 3->0 wraps."),
 (23, "work/acceptance-01/headless-review-03/stationary.png", V, "Same page in its explicit stationary frame-zero view: Working frame 0 shown alone with its label beside Start, Paused, Ready and Retry at 1x and 3x, color and grayscale."),
 (24, "work/acceptance-01/observed-views/transition-03-3x-color.png", V, "Recorded 3x exposure of Working frame 3 immediately before the wrap."),
 (25, "work/acceptance-01/observed-views/transition-04-3x-color.png", V, "Recorded 3x exposure at the 3->0 wrap (412 ms): same quarter-turn increment as the other steps."),
 (26, "work/native-review/frames/working-strip-12x.png", V, "My 12x strip of the four Working cells: rigid quarter-turn rotation, same 32-pixel volume and ramp in every frame."),
 # --- live: destination run
 (27, D+"render.json", L, "Destination capture report (version 2, HeadlessChrome 156.0.8078.80, DPR 1, viewport 1280x1000, observed_at 2026-11-09T16:19:50Z): errors [] and missing []; transitions idle/started/pause/ok/error resolve identical descriptors on statusCell and compactStatus (Start svg ee2ba2fe..., Working cf101610... frames 4, Paused 80d2b823..., Ready fc5e43ae..., Retry 0fb0ab5e...); 20 views at scale 1 and 3 with geometryMatches true, smoothing false, integer bounds; timeline frames 0,0,1,1,2,2,3,3,0 at 0,99,100,199,200,299,300,399,400 ms with view-020..028 hashes equal to the recorded frame exposures; served_files hashes for the five renderer-successor/assets equal the manifest member hashes."),
 (28, D+"motion.json", L, "Live preference phases from the same page session: normal-before 40 samples over 1045 ms showing frames 0,1,2,3 on both live cells; reduced-live 40 samples over 1037 ms showing only frame 0 on both live cells and all four matrix Working cells; normal-after 40 samples over 1043 ms restarting at frame 0 through 1,2,3. preferenceChanges: reduce at 1322.6 ms and no-preference at 2473 ms, both via route animation-frame, exactly one entry per transition; statusCell and compactStatus report the same frame at every sample; every motion-NNN.png hash equals the exposure hash of its declared frame."),
 (29, D+"reduced-render.raw.json", L, "Raw report under prefers-reduced-motion: reduced true, timeline frame 0 at every sample point 0..400 ms, errors [] missing []."),
 (30, "work/native-review/destination-01-check.json", L, "renderer-successor/check.py over this capture: status pass, 233 observations, 0 failures, 20 available views, capture_sha256 84cb0c6e...; checks served bytes, retained image hashes, sheet geometry, nearest sampling, canvas dimensions, integer bounds and screenshot-vs-canvas pixel correspondence for every view."),
 (31, D+"destination.png", L, "1280x1000 destination screenshot at the end of the transition sequence (succeeded): live cells show Ready at 3x; the state matrix shows Start, Working frame 0, Paused, Ready, Retry at 1x and 3x for Full and Compact consumers, all composited on the panel colour."),
 (32, D+"normal-before.png", L, "Screenshot during normal-before: live Working cells mid-cycle (a frame other than 0) while the state matrix Working cells hold frame 0 as painted by the fixture; everything else identical."),
 (33, D+"reduced-live.png", L, "Screenshot during reduced-live: both live Working cells and all matrix Working cells show stationary frame 0; no other cell changed."),
 (34, D+"normal-after.png", L, "Screenshot during normal-after: live Working cells cycling again; the page was not reloaded and the queue state remained running."),
 (35, D+"motion-000.png", L, "48x48 live statusCell Working cell, normal-before first sample: frame 0 pixels equal the recorded frame 0 exposure."),
 (36, D+"motion-040.png", L, "48x48 live statusCell cell later in normal-before: frame 1."),
 (37, D+"motion-080.png", L, "48x48 live statusCell cell, reduced-live first sample: frame 0."),
 (38, D+"motion-160.png", L, "48x48 live statusCell cell, normal-after first sample: frame 0 (restart at origin)."),
 (39, D+"motion-200.png", L, "48x48 live statusCell cell later in normal-after: frame 1 (cycling resumed)."),
 (40, D+"view-022.png", L, "16x16 timeline crop at 100 ms: frame 1."),
 (41, D+"view-028.png", L, "16x16 timeline crop at 400 ms: frame 0, the wrap."),
 (42, D+"view-001.png", L, "48x48 state-matrix Start cell: the preserved svg rendered as a triangle at 3x."),
 (43, D+"view-013.png", L, "48x48 state-matrix Ready cell at 3x from the exact package bytes."),
 (44, D+"view-017.png", L, "48x48 state-matrix Retry cell at 3x."),
 (45, D+"view-009.png", L, "48x48 state-matrix Paused cell at 3x."),
 (46, D+"view-012.png", L, "16x16 state-matrix Ready cell at 1x."),
 # --- local
 (47, "work/native-review/old-consumer-hashes.txt", X, "SHA-256 of src/queue-view.ts (4d6ee92e...), src/queue.ts (de271234...), renderer/{capture,server,view}.mjs, renderer/index.html, renderer/check.py taken now; queue-view.ts 4d6ee92e..., renderer/view.mjs 5f64fc51... and renderer/index.html 05fbe0a3... equal the hashes recorded for those paths in work/successor-adoption/plar-final-document.json and work/acceptance-01/plar-update.json, and assets/*.png equal the manifest member hashes with assets/start.svg equal to renderer-successor/assets/start.svg."),
]
observations = []
for i, p, m, n in obs:
    assert i == len(observations), (i, p)
    observations.append({"path": p, "sha256": sha(p), "mode": m, "note": n})
cont = [0, 2, 3, 4, 5, 6, 12, 13, 14, 15, 16, 20, 22, 23, 24, 25, 26]
dist = [0, 1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 23]
dest = list(range(27, 47))
doc = {
 "version": 1,
 "binding_hash": "48752d9d65836801fde700b5f125e424cae21ee15c536628b5abde38740db443",
 "reviewer": "actor",
 "observed_at": ts,
 "observations": observations,
 "verdicts": [
  {"criterion": "provenance-correction.delivery.q.continuity", "status": "pass",
   "reason": "Compared the four package members together at 1x and 3x on #172336 against the exact Ready baseline. Pixel treatment is coherent and deliberate across all four: crisp stepped edges, compact clusters, binary alpha, no resampling blur or stray pixels; Ready is a flat single-tone stroke while Working, Retry and Paused carry subtle in-shape ramps, which reads as one hand-drawn family rather than a mismatch and is not restricted by the criterion (no palette or stroke rule). Visual weight is coherent with the baseline: Ready 29 opaque pixels at 2 px stroke, Working 32 per frame at 2 px, Retry 54 at 2 px ring, Paused 60 at 3 px bars; Paused is the heaviest and Ready the lightest but all read as mid-weight glyphs of the same size class at native scale, and identical footprint is not required. Each member shows a perceptible cool-blue accent (Ready and the preserved Start share a light sky blue; Working a more saturated azure; Retry and Paused a medium blue) and every exterior is the transparent panel with no matte, halo or fringe. Working's four frames keep the same volume and ramp; its recorded 100 ms playback with the 3->0 wrap is one continuous quarter-turn rotation (reviewed in native-review.working.motion), and its stationary frame zero shown alone under reduce reads as the same spinner at rest, coherent with the siblings.",
   "supersedes": None, "observations": cont},
  {"criterion": "provenance-correction.delivery.q.distinction", "status": "pass",
   "reason": "Viewed Ready, all four Working frames and the loop, Retry, Paused and the preserved Start together at 1x and 3x in colour and in grayscale. By structure alone: Ready is two diagonal strokes meeting at a low point (a check); every Working frame is three disjoint fragments on an open ring that never close into a check, a bar pair, a triangle or a solid shape, so Working never reads as success at any frame or in motion; Retry is a nearly closed continuous ring with an arrowhead, distinct from Working's open fragments by closure and density and from Paused by shape; Paused is two parallel full-height bars, unlike anything else in the set; Start is a solid triangle and remains separately identifiable. Stationary Working frame zero alone in the non-color 1x and 3x views (top bar, right vertical, lower-left curve) is clearly distinct from the Ready check and from Paused's twin bars, which is the required reduced-motion distinction; it is also distinguishable from Retry and Start. Retry and Working both use a circular motif; their structural difference (closed ring plus arrow versus three fragments) carries the distinction without a shared-silhouette rule.",
   "supersedes": None, "observations": dist},
  {"criterion": "provenance-correction.delivery.q.destination", "status": "pass",
   "reason": "Ran renderer-successor/capture.mjs against this project (HeadlessChrome 156, DPR 1) and check.py on the capture: no script errors, no missing assets, 233 checks pass. The fixture executed the actual src/queue.ts and src/queue-view-successor.ts through all backend transitions (idle, started, pause, ok, error); statusCell and compactStatus resolved identical descriptors with the exact package bytes served at renderer-successor/assets (served hashes equal the manifest members; start.svg ee2ba2fe... unchanged). All 20 views at scale 1 (matrix) and 3 (matrix and live) report geometryMatches, nearest sampling, integer bounds and screenshot pixels equal to canvas pixels; the Working timeline is 0,0,1,1,2,2,3,3,0 at 0..400 ms including the wrap, with crops equal to the recorded frame exposures. Live phases in one page session: normal cycling through all four frames; reduce applied via the animation-frame route at 1322.6 ms with both live cells and all matrix Working cells repainted to frame zero and held for 1037 ms; switch back at 2473 ms with cycling restarting at frame zero through 1,2,3; one preferenceChanges entry per transition, both consumers in the same frame at every sample, queue state still running, no reload. Matrix Working cells are painted once at elapsed 0 by the fixture design and only the live cells animate, consistent with the criterion. Old consumer files src/queue-view.ts, renderer/ and assets/ match the hashes recorded in the earlier successor-adoption documents and the manifest. Wall-clock frame duration is not measured, as the criterion states.",
   "supersedes": None, "observations": dest},
 ],
 "action": "complete",
 "next_action": "Hand the accepted package .pixl/assets/queue.ready/deliveries/ec59b8245619463446cb86b639e7b387e748917fb5c520a085984b85c89df5d0 to the caller for its independent verification; no further production is required for this family.",
 "limitations": [
  "Collective views were judged from recorded consumer exposures, the destination capture screenshots and my own nearest enlargements, not from a real-time display; playback continuity relies on the recorded 100 ms exposure sequence reviewed for the Working candidate.",
  "The destination run is the project's headless Chrome fixture on this machine; it does not establish behaviour in another browser, at other device pixel ratios, or wall-clock frame durations.",
  "Byte-unchanged status of old src/queue-view.ts, renderer/ and assets/ was verified against hashes recorded in earlier project evidence, not against version control, because this copied consumer is untracked.",
  "Scope is this exact manifest (ec59b824...) and its four member files on #172336 at 1x and 3x; no general art-quality or host-reliability claim."
 ]
}
json.dump(doc, open(sys.argv[2], 'w', encoding='utf-8'), indent=2)
print(json.dumps({"observed_at": ts, "n_obs": len(observations)}))
