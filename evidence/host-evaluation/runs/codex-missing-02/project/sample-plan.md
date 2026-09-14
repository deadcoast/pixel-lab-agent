The representative sample is planned in `.pixl/state.px`. Generation is blocked because this session exposes local PIXL tools but no callable PixelLab generation, polling, or artifact-retrieval tool. No provider request was submitted and no new sprite PNG exists.

Confirmed output: one 32x32 PNG, side-view teal scout robot matching `reference.png`, two antennae, two distinct yellow eyes, dark outlines, binary transparency, no ground shadow, and nearest-neighbor display in a web prototype. The visible palette is `#25354A` (outline), `#56B5BC` (body), and `#F4DDA2` (eyes). Transparent RGB bytes are unconstrained. Flat unshaded treatment is proposed from the reference. Left/right facing and final browser display scale remain unspecified.

The actual reference was inspected at native size and 8x zoom on light, dark, and checkerboard backgrounds. PIXL measured 32x32, one frame, three visible colors, 390 visible pixels, alpha values 0/255, and zero out-of-palette pixels. Its symmetric iconlike silhouette does not establish a facing direction. These findings apply to the input reference only.

Review material:

- [Reference inspection sheet](.pixl/evidence/reference-inspection.png)
- [Reference measurements](.pixl/evidence/reference-measurements.json)
- [Reference visual observations](.pixl/evidence/reference-visual-review.md)
- [Tool availability evidence](.pixl/evidence/tool-discovery.json)
- [Method applicability and proof limits](.pixl/research/applicability.md)

On resumption, read PIXL workflow and jobs for `.pixl/state.px`, then discover the actual connected PixelLab tool schema. Translate the saved contract into supported arguments with the supplied reference image. Save an exact request with `job-prepare`, claim it once with `job-dispatch`, execute through the discovered provider, and retain real observations and returned IDs. Import downloaded bytes as a candidate for `sample-png`; do not substitute the input reference as generated output.

Before sample acceptance, check the actual candidate's dimensions, PNG format, exact visible palette, and binary alpha. View candidate and reference together at native size and integer zoom on light/dark/checker backgrounds; verify silhouette, two separate antennae, two legible yellow eyes, outline character, and absence of a ground shadow. Save the actual comparison and criterion-specific verdicts. Browser inspection remains required and unperformed; use `image-rendering: pixelated` for an image, or `context.imageSmoothingEnabled = false` before canvas drawing, and verify the rendered result at the actual scale, zoom, and device-pixel ratio. Do not treat these suggested settings as a browser test.

Candidate mechanical checks, actual candidate/reference visual comparison, and browser display verification are all unperformed because no candidate exists. Family expansion must wait for the sample's required acceptance criteria. No packages were installed or host settings changed.
