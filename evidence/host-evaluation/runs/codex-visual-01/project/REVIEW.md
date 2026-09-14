# Robot baseline review

**Decision: candidate.png is not ready to become the robot-family baseline.** The agreed identity remains reference.png.

| Check | Result | Evidence |
| --- | --- | --- |
| Canvas | Pass | One 32 × 32 frame |
| Reference palette | Pass | Three visible colors; no out-of-palette pixels |
| Identity and silhouette | **Fail** | Missing viewer-left antenna and viewer-right eye |
| Color roles and cluster quality | Pass | Remaining frame, cyan fill and pale eye retain clean flat blocks; missing landmark completeness is the identity failure above |

The reference has two top prongs and two pale eyes. The candidate has one of each. This changes both the silhouette and facial identity at native size. Equal dimensions, palette, bounding box and connected-component count do not make it a suitable family baseline.

[Open the native/enlarged comparison](review/comparison.png). Both actual images were inspected at native size and integer zoom, including alpha silhouettes and diagnostic light, dark and busy backgrounds.

**Next step:** create a separate `candidate-v2.png`, restoring the dark left antenna at x=7–10, y=3–8 and pale right eye at x=18–20, y=14–17 from the reference (zero-based coordinates, inclusive). Recheck all four criteria on the new candidate before extending the family. This review does not perform that edit.

PIXL state is [.pixl/state.px](.pixl/state.px). The original rejected candidate is retained byte-for-byte at [review/candidates/candidate-v1.png](review/candidates/candidate-v1.png). `d.baseline` retains the evidence-backed rejection; `t.sample` stays blocked by its visual failure; `t.revise` is the next open sample task, with planned output `f.revised`. No baseline has been approved for family production.

For resumption, run PIXL `workflow`, `family` and `jobs` on `.pixl/state.px`, then `context` focused on `t.revise`. Retain v1 and its verdicts, register v2 as a new candidate for `f.revised`, and evaluate it with its own evidence. Task completion requires all declared criteria to pass.

Detailed evidence: [mechanical measurements](review/mechanical.json), [visual observations](review/visual.json), [exact changed regions](review/pixel-diff.json), and [source applicability](review/method-applicability.md). Required criteria were published in revision 1 before this evaluation. Review results and the next task are retained in revision 2 using expected-hash publication.

Engine import, actual game backgrounds and final display scale were not supplied or tested. This is a static identity decision; it establishes no destination-engine acceptance. No generation request was made.
