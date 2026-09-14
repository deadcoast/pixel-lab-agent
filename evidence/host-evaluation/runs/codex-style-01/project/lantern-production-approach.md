The matching lantern should use a compact dark frame, a teal body and a small warm light, with deliberately placed translucent edge pixels. Preserve full RGBA and selective anti-aliasing. Keep colors editable: the reference supplies color relationships, and the brief imposes no fixed palette.

The reference has been inspected at native size and at 8x nearest enlargement on light, dark and checker backgrounds. [Open the inspection sheet](review/reference-inspection.png).

| Reference evidence | Finding | Production implication |
| --- | --- | --- |
| Measured canvas and footprint | 32 x 32; visible bounds `(6,3)-(26,28)`, with exclusive right/bottom bounds: 20 x 25 pixels | Propose a 32 x 32 first sample at comparable apparent scale. |
| Measured alpha | 604 transparent, 390 opaque and 30 partially transparent pixels; alpha values 0, 96, 160, 255 | Preserve fractional alpha. These counts and levels describe the reference, not mandatory new-asset quotas. |
| Measured edge placement | Fifteen pixels at x=6, y=11..25 use alpha 96; fifteen at x=25 use alpha 160 | Selective one-pixel side strips are the clearest treatment to carry over. Preserve useful asymmetry if it looks right in the sample. |
| Measured colors | Three RGB colors: navy `#25354A`, teal `#56B5BC`, cream `#F4DDA2`; five visible RGBA combinations | Start from these relationships; allow additional or adjusted colors when needed. RGB palette and alpha policy remain separate. |
| Visual construction | Flat frontal blocks, substantial navy frame, opaque teal interior and two small warm blocks | Match simple clusters, restrained detail and cool/warm contrast. The source does not establish a directional light. |
| Visual compositing | Soft strips remain localized; hard frame and fill remain crisp. The navy frame loses contrast on the dark test background. | Review the lantern on multiple backgrounds and adjust local contrast where necessary. |

PIXL's `visible_colors=5` measurement counts distinct visible RGBA combinations here. An independent RGB-only count is three. The reference's large teal interior is opaque; partial transparency is confined to the side strips. The user's description establishes the intentional treatment, while pixels alone do not distinguish material translucency from edge coverage.

The first sample proposal is one static, frontal lantern on a 32 x 32 transparent canvas. Aim for an approximately 18-20 x 24-26 pixel footprint: a small loop handle, short cap, two substantial side rails, a base and a single cream light cluster inside teal glass. Use a single light cluster to establish a lantern identity, with the reference's economical rectangular shapes. Propose bottom-center anchor `(16,28)` in the untrimmed canvas; final pivot conventions depend on the destination.

Keep the frame and most body clusters opaque. Begin selective AA with short, one-pixel translucent teal strips beside the glass/frame boundary, using the source's alpha 96 and 160 as starting swatches. Add coverage pixels at a handle corner only if the native silhouette benefits. Keep structural edges crisp, and judge color additions by their role in the image. The edge mask and chosen ramp are sample authoring choices; no fixed color count, exact palette membership or exact fractional-pixel count is required.

Production proceeds through one representative proof before related props:

1. Block in the handle, cap, rails, base and warm light at native resolution. Keep the source beside the sample and establish readable lantern identity before edge refinement. Retain this pre-AA version.
2. Save an explicit mask for permitted AA/translucency edits and mark protected hard frame pixels. Author partial alpha and any intermediate colors only where the mask allows them. No blanket smoothing or alpha thresholding is part of this approach.
3. Export one RGBA PNG, initially using straight alpha, then reopen it and compare visible RGBA and the full alpha channel with the authored raster. Retain both versions and the mask. Compare the pre/post-AA pixels to confirm that protected structure did not change.
4. Inspect the exported sample beside the reference at 1x and 8x nearest on light `#F0E8D8`, dark `#18222E` and a checker background. Confirm lantern identity, localized soft edges, a clear warm focal point and enough frame contrast. Retain failed revisions and revise the same sample before producing variants.
5. Once the target renderer and real backgrounds are known, verify actual imported appearance, blend convention, display scale, pivot and any atlas padding. Record destination acceptance separately. Nearest sampling is the initial preview proposal; it preserves authored fractional alpha while avoiding additional interpolation.

| Acceptance area | Observable requirement | Current status |
| --- | --- | --- |
| Mechanical | One 32 x 32 RGBA PNG; transparent exterior and intentional fractional-alpha regions; save/reopen preserves alpha and visible RGBA; no fixed palette validation | Criteria saved; lantern not created |
| Edit locality | AA pass changes only the saved mask; protected hard frame pixels remain byte-identical | Criteria saved; proof pending |
| Visual | Readable lantern at native size, matching flat clusters and color hierarchy; localized soft edges without a baked matte fringe or unplanned continuous halo | Criteria saved; sample inspection pending |
| Destination | Actual imported alpha, color, texture sampling, scale, anchor and atlas edges match the reviewed export on game backgrounds | Engine, display scale and game backgrounds unspecified |

The researched PIXL methods are `alpha-contract` and `selective-edge-aa`. Their applicability and exact source slices are retained in [source-grounding.json](review/source-grounding.json). In the bundled *PIXEL-ART-DEEP-RESEARCH.md*, lines 590-632 describe edge coverage and conditional strict-palette quantization; the coverage concept is relevant, while its fixed-palette restriction does not apply to this brief. Lines 907-919 distinguish authored edge cues from runtime filtering and support testing nearest previews.

The alpha method's cited deep-research ranges 945-977 and 1276-1291 address channel layout and alignment; its asset-archive range 942-958 is a CSS example. Those passages do not establish a complete alpha export/import pipeline. The method remains a candidate to prove on this project's sample. Its bundled numeric compositing fixture does not evaluate a display transfer function, GPU blend state or importer. The bundled selective-AA fixture proves edit locality and selected color membership, not perceptual quality against arbitrary backgrounds. Neither receipt is acceptance evidence for this lantern, and no source attribution with an unresolved historical citation is treated as current engine documentation.

The saved [PX2 state](.pixl/state.px) distinguishes confirmed user constraints, observed reference traits, proposed sample choices and unresolved destination settings. The planned lantern output has no fabricated file or acceptance verdict. Resume with the workflow report and `t.sample` context when sample creation is requested. The actual PixelLab provider is not exposed in this session; the local PIXL tools support planning and checks. A future PixelLab route requires discovering a real provider tool and its schema. No remote generation was attempted during this reference review.
