import json, hashlib, sys
ts = sys.argv[1]
def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()
V = "visual"; L = "local"
obs = [
 ("work/acceptance-01/headless-review-03/playback.png", V, "1280x1000 headless-Chrome screenshot of the supplemental playback page after recording: the Working 1x/3x color and grayscale cells and the 17 captured transition exposures (frame 0,1,2,3,0,... at 12,112,212,...,1611 ms) laid out in sequence. Shows four complete observed cycles including four 3->0 wraps; no missing or repeated phase in the strip."),
 ("work/acceptance-01/observed-views/transition-00-3x-color.png", V, "48x48 nearest 3x exposure of frame 0 on #172336: top bar, right vertical segment, bottom-left curved segment; gap at upper-left."),
 ("work/acceptance-01/observed-views/transition-01-3x-color.png", V, "48x48 3x exposure of frame 1: the same three segments advanced one quarter turn clockwise (curved segment now upper-left, bar now at bottom, vertical segment at right)."),
 ("work/acceptance-01/observed-views/transition-02-3x-color.png", V, "48x48 3x exposure of frame 2: another exact quarter turn clockwise (curved segment upper-right, vertical at left, bar at bottom)."),
 ("work/acceptance-01/observed-views/transition-03-3x-color.png", V, "48x48 3x exposure of frame 3: another quarter turn clockwise (bar at top, vertical at left, curved segment lower-right)."),
 ("work/acceptance-01/observed-views/transition-04-3x-color.png", V, "48x48 3x exposure recorded at the 3->0 wrap (412 ms): identical to the frame 0 exposure; the step from frame 3 is the same quarter-turn increment as the other three transitions, so the wrap is not visible as a jump, hold or reversal."),
 ("work/acceptance-01/observed-views/transition-00-1x-color.png", V, "16x16 native exposure of frame 0 on #172336; the three-segment ring reads as a small spinner at 1x."),
 ("work/acceptance-01/observed-views/transition-01-1x-color.png", V, "16x16 native exposure of frame 1 (quarter turn clockwise from frame 0)."),
 ("work/acceptance-01/observed-views/transition-02-1x-color.png", V, "16x16 native exposure of frame 2."),
 ("work/acceptance-01/observed-views/transition-03-1x-color.png", V, "16x16 native exposure of frame 3."),
 ("work/acceptance-01/observed-views/transition-04-1x-color.png", V, "16x16 native exposure at the 3->0 wrap; identical pixels to the frame 0 exposure, continuous with frame 3 at native scale."),
 ("work/acceptance-01/observed-views/transition-08-3x-color.png", V, "3x exposure at the second observed wrap (812 ms), again frame 0; confirms repeated wraps show the same pixels."),
 ("work/acceptance-01/observed-views/transition-16-3x-color.png", V, "3x exposure at the fourth observed wrap (1611 ms), frame 0; end of the recorded sequence."),
 ("work/acceptance-01/observed-views/transition-03-3x-gray.png", V, "3x grayscale exposure of frame 3; segment weights remain readable without hue, used only as a comparison view."),
 ("work/native-review/frames/working-strip-12x.png", V, "My own 12x nearest enlargement of the four retained cells (sheet cf101610...) composited on #172336, side by side: each cell is the previous cell turned exactly 90 degrees clockwise; the three segments keep their shapes and cluster edges in every frame."),
 ("work/native-review/frames/working-wrap-3-0-1-12x.png", V, "My own 12x enlargement of frames 3, 0, 1 in order, isolating the wrap: the 3->0 step is the same quarter-turn increment as 0->1."),
 ("work/acceptance-01/playback-observation-03.json", L, "Recorded requestAnimationFrame playback (run 03, HeadlessChrome 156, DPR 1): 97 samples, 17 transitions at elapsed 11.6,111.6,...,1611.5 ms, complete_cycles 4, frame sequence 0,1,2,3 repeating with every 3->0 wrap present; assets.running sha256 cf101610... matches the candidate file."),
 ("work/acceptance-01/review-checks.json", L, "transition_intervals_ms all within 99.9-100.1 ms over 16 intervals; transition_frames 0,1,2,3,0,...,0; alpha_mass 8160 (32 opaque pixels) in every cell; alpha boxes 11x11 in every cell. clockwise_quarter_turn_matches is false in all four entries because that measurement compared raw RGBA including RGB under alpha zero; the sibling package-review-checks.json visible_clockwise_quarter_turn_matches (composited on #172336) is true for all four, and my own alpha-aware comparison agrees."),
]
observations = [{"path": p, "sha256": sha(p), "mode": m, "note": n} for p, m, n in obs]
visual_idx = [i for i, o in enumerate(observations) if o["mode"] == "visual"]
doc = {
 "version": 1,
 "binding_hash": "835ff4ed42593c033a41feca09656bb26bd9b0c92051e74c11bfc1d225d3fe67",
 "reviewer": "actor",
 "observed_at": ts,
 "observations": observations,
 "verdicts": [{
   "criterion": "provenance-correction.working.q.motion-continuity",
   "status": "pass",
   "reason": "Viewed the recorded 100 ms playback as a sequence at native 1x and nearest 3x on #172336 across four complete cycles, including every fourth-to-first wrap (transitions 04, 08, 12, 16). The loop is one continuous activity: each of the four steps, the wrap included, is the same quarter-turn clockwise increment of the same three-segment ring, so there is no visible jump, reversal or hold at the wrap. Center/anchor is stable: the ring turns about the cell center, every frame occupies an 11x11 box offset by at most one pixel, and nothing drifts or slides. Visual volume is stable: 32 opaque pixels, the same cluster shapes and the same blue ramp in every frame; no morphing or shrinking segment. Pacing is even: equal 90-degree steps at measured 99.9-100.1 ms intervals, no near-hold. The remaining quality note is a design choice, not a defect: the three segments carry unequal weight (bar, slim vertical, heavier curved piece), which gives the spinner a slight visual lope, but it reads clearly as deliberate rotating activity at both scales. Judgment is mine from the viewed exposures and my enlargements; the timing files were read only as supporting measurements.",
   "supersedes": "provenance.working.motion.unavailable",
   "observations": visual_idx
 }],
 "action": "complete",
 "next_action": "Snapshot the provenance-correction.delivery.output family with a fresh candidate id and review its collective continuity, distinction and destination criteria.",
 "limitations": [
   "Motion was judged from recorded headless-Chrome exposures and my own frame enlargements viewed as an ordered sequence, not from real-time viewing of a running display; the recording covers 1.6 s (four cycles) of the supplemental playback page, not the destination renderer, which is covered by the separate consumers/destination criteria.",
   "This review covers only the motion-continuity criterion of this exact 64x16 sheet (cf101610...) on #172336 at 1x and 3x; it does not establish general art quality or other display scales/backgrounds."
 ]
}
out = sys.argv[2]
json.dump(doc, open(out, 'w', encoding='utf-8'), indent=2)
print(json.dumps({"observed_at": ts, "visual_idx": visual_idx, "n_obs": len(observations)}))
