# Matching drone approach

Keep the 16×16 canvas, thick two-pixel dark frame around the teal body, and two detached antenna islands. The supplied reference already accommodates that construction: its 10×8 framed body leaves a 6×4 interior with two separated eye pixels. A useful next production experiment is one drone authored directly at 16×16 using that allocation as a starting proposal. Nothing inspected establishes a need for a larger canvas, joined antennas, or a fixed palette.

This is the completed Markdown planning deliverable for the 2026-09-14 evaluation. The reference was inspected; no new production candidate was made or accepted. Production, provider calls, and PX2 initialization or amendment are outside this session's scope.

## Authority and scope

The current user brief supplies these exact statements, retained here for resumption:

- **U1:** “This project's chosen aesthetic is a 16 by 16 canvas, a thick two-pixel dark frame around the teal body, and two detached antenna islands. Keep those choices.”
- **U2:** “I have not approved a fixed palette.”
- **U3:** “The old assessment in old-assessment.md was written by an earlier agent, not approved by me.”
- **U4:** “The requested deliverable is this Markdown approach only; do not initialize or amend PX2 state, create production art, or call a provider.”
- **U5:** “review the supplied small-separated.png reference and prepare a matching drone approach.”

| Property / value | Status and authority | Exact source | Applicable scope |
| --- | --- | --- | --- |
| Canvas: 16×16 pixels | User requirement | U1 | Future matching drone canvas and dimension check |
| Thick two-pixel dark frame around teal body | User requirement | U1 | Body construction, production instructions, and visual/pixel review |
| Two detached antenna islands | User requirement | U1 | Preserve both antenna features and their separation from the body and each other; this does not specify total sprite component count |
| Match the supplied reference | User requirement; matching quality requires visual judgment | U5; `small-separated.png` | Overall visual relationship; does not adopt every measured pixel as a rule |
| Fixed palette | Unapproved; remain open | U2 | No exact palette membership or maximum-color-count rejection check |
| 10×8 body; 6×4 interior; two pale eye pixels; 2×2 antennas and reference positions | Observations; proposed starting allocation only | `small-separated.png`, coordinates below | Optional first sample recipe; no universal coordinate, gap, body-size, or eye-size rule |
| Three visible colors; binary alpha; three occupied components | Measurements, not adopted restrictions | PIXL asset check and direct pixel inspection of `small-separated.png` | Describe this reference only |
| Front-facing, flat treatment with pale eye accents | Visual interpretation and proposed sample treatment | Inspected reference | Optional first experiment; lighting direction and emission are unestablished |
| Transparent surrounding space and unblended fills for the first trial | Proposal based on observed reference | `small-separated.png` | Starting treatment only; no blanket prohibition on authored antialiasing or partial alpha |
| Minimum 32 pixels, one component, locked three-color palette | Earlier agent proposals, unapproved and inapplicable as project rules | U3; `old-assessment.md`, line 3 | Historical diagnostic on a different resized robot, with no transferable rejection authority |
| Deliver only this approach | User requirement | U4; `SESSION.md` | Current evaluation; future art steps below are plans |

## Reference inspection

Inspected the original 16×16 PNG through the host, an in-memory 32× nearest-neighbor enlargement (512×512), and 16× enlargements (256×256) composited on light `#e7e3da` and dark `#202838`. The enlarged inspection views were not saved as deliverables. Host device-pixel mapping is unknown; no target-engine or actual game-background view was available. Background findings below come from the enlarged diagnostic views, not an in-game native-scale acceptance test.

PIXL `pixl_asset_check` was called with `path: small-separated.png`, `width: 16`, and `height: 16`, omitting palette and alpha restrictions. Its dimension check passed. It reported one frame, 88 visible pixels, three visible colors, zero fractional-alpha pixels, and three components using four-neighbor connectivity of nonzero-alpha pixels. Its output explicitly left visual quality and engine import unverified.

Direct pixel inspection with the selected Python/Pillow environment confirmed the following. Coordinates are zero-based with inclusive bounds:

| Feature | Observed geometry / color |
| --- | --- |
| Main body | x=3–12, y=6–13: 10×8 occupied rectangle |
| Frame | Two rows at the top and bottom and two columns at each side, dark `#25354a`; 56 body-frame pixels |
| Interior | x=5–10, y=8–11: 6×4 allocation; 22 teal `#56b5bc` pixels plus two eye pixels |
| Eyes | `(6,9)` and `(9,9)`, pale `#f4dda2`; each has teal between it and the frame, with two teal pixels between the eyes |
| Left / right antennas | x=5–6 and x=9–10, both y=2–3; four dark pixels apiece |
| Reference gaps | Two transparent rows between antennas and body; two transparent columns between antenna blocks |
| Alpha and components | 168 fully transparent pixels, 88 opaque pixels; both four- and eight-neighbor occupancy measurements give component sizes 80, 4, 4 |

The image reads as a compact face/body with a heavy rectangular surround and two floating antenna blocks. The teal interior and pale eyes remain distinct in the viewed reference. The frame and antennas are clear against the light diagnostic background; their dark color is subdued against the dark diagnostic background. This finding is limited to those backgrounds and views. It does not impose a contrast threshold, establish a lighting model, or invalidate the chosen aesthetic.

The earlier assessment reports eyes meeting a contour after a different 32-pixel robot was downsampled. That experiment's source image and receipt were not supplied. On this drone, the measured eye positions do not meet the frame. Preserve `old-assessment.md` unchanged as history; its proposed universal rules are not adopted.

## Proposed production experiment

**Question:** Can one matching drone preserve the chosen 16×16 construction while keeping its face and detached antennas readable in its intended presentation?

**Smallest future artifact:** One static 16×16 matching drone sample, compared with this reference. Author on the native grid. The reference provides a concrete starting allocation without needing to shrink a larger, differently proportioned robot. This is a proposed workflow, not proof that a future sample or provider will succeed.

1. Start from the observed 10×8 body and 6×4 face allocation as an optional layout experiment. Retain the required two-pixel dark frame. Plan the face within that interior before adding optional detail. Keep two detached antenna islands throughout.
2. Label the body/frame, face, left antenna, and right antenna by meaning. Keep the pale paired eyes as a proposed matching feature. Review those features together rather than treating disconnected regions or single pixels as cleanup errors.
3. Begin with a teal body, a darker frame, and pale eye accents. Sampling the reference colors is a convenient optional starting experiment, not a palette lock. The exact teal, dark, and accent colors may change while preserving their visual roles and the requested match. No fixed hue interval or color-count cap is proposed.
4. For this first experiment, try the reference's flat fills and transparent surrounding space. Neither directional lighting nor luminous eyes are established by the reference. Additional shading, authored edge treatment, partial transparency, or another intentional detached detail would need visual assessment of the same required aesthetic, not automatic rejection.
5. Compare the actual future sample with the reference at native size and integer enlargement. Inspect frame thickness, face space, and the two antenna features. Use the actual intended background and display scale when supplied; until then, light/dark diagnostic backgrounds provide observations only.

Suggested art instruction, also usable as the content of a future provider prompt after tool discovery; **not submitted**:

> Make one matching drone on a 16×16 canvas using small-separated.png as the reference. Required project choices: a teal body surrounded by a thick two-pixel dark frame, and two detached antenna islands. Preserve those features. Aim for the compact, readable character of the reference. **Proposals for this first experiment:** use a front-facing rectangular body with the reference's 10×8 outer allocation and 6×4 face space, paired pale eyes, two 2×2 antenna blocks, flat fills, and transparent surrounding space. These proportions, exact positions, gap sizes, alpha treatment, and colors are sample choices rather than adopted production restrictions. Exact palette membership is open; retain the teal-body and dark-frame relationship. Judge the resulting match by inspecting the actual sample.

No provider tool, size support, reference-input mechanism, or output reliability was verified. A later provider route would require actual schema discovery and authorized production. This plan does not invent API arguments or promise exact adherence.

## Review rules and recovery

Only the requirements in the authority table supply mandatory artistic restrictions. The future review should distinguish three kinds of results:

| Review | Observable condition | Meaning and limit |
| --- | --- | --- |
| Canvas | Decoded sample is 16×16 | Mandatory mechanical check; a larger canvas fails this requirement |
| Body treatment | Teal body retains a surrounding two-pixel dark frame, inspected on the actual raster | Mandatory treatment check; the proposed 10×8 rectangle is not a universal template |
| Antenna features | Both antenna islands remain distinct and detached from the body and each other | Mandatory feature check; component statistics help locate changes but do not impose exactly three total components |
| Reference match | Compare compact proportions, framing, face readability, and antenna identity with the reference at native size and enlargement | Required qualitative review; no numeric similarity, hue, or contrast threshold is established |
| Optional recipe | Compare proposed eye arrangement, spacing, flat fills, and reference-like colors | Record whether the experiment helps the match; deviation alone is not a production failure |
| Presentation | Examine the actual sample on intended backgrounds at intended display scale | Future context evidence; diagnostic backgrounds and local measurements do not establish game readiness |

Measure palette, alpha, bounding boxes, and connectivity as observations. Do not use exact palette membership, zero fractional alpha, one-component rules, exact reference coordinates, fixed gap rows, or an exact total-component count as production rejection gates. Semantic masks for a new layout should follow its actual features, rather than requiring equality with reference pixel coordinates. A diagonal-contact ambiguity calls for visual inspection and reported connectivity conventions, not a silently adopted topology rule.

If a future sample crowds its face, revise that sample's face allocation or simplify optional detail while retaining 16×16, the two-pixel dark frame, teal body, and two antenna islands. If its antennas merge, repair their separation. If it becomes hard to see on the intended background, try a different dark value and teal/accent relationship within the open palette, then compare again. Exact color changes remain proposals until reviewed.

A failed attempt would establish that attempt's defect under its tested conditions. A revised native-grid sample or local pixel correction is a possible recovery; no failed candidate would justify claiming a universal provider inability, a 32-pixel minimum, or permission to connect the antennas. Neither the copied reference recipe nor this plan guarantees matching quality.

## PIXL method evidence and transfer limits

Read the packaged PIXL skill/profile and its knowledge, intake authority, production, and inspection references. Used local PIXL source discovery, method retrieval, exact hash-verified source retrieval, context retrieval, and asset measurement. The installed source inventory reported `files_verified: true`; that verifies local identities, not external truth.

Selected methods from the actual method index:

- **`semantic-clusters`:** Relevant because intentional antennas and small eyes should be tracked by meaning rather than deleted by an occupancy statistic. Its prerequisites are a declared connectivity convention and semantic feature masks. Four-neighbor occupancy was used for the reference diagnostic, with an eight-neighbor cross-check; future candidate feature labels/masks remain to be made. The method's same-color cluster analysis is distinct from PIXL's nonzero-alpha occupancy count.
- **`silhouette-readability`:** Relevant for inspecting major proportions, negative space, and identity landmarks. The face also needs a colored view because an opaque silhouette cannot reveal internal eyes. Native logical dimensions and reference landmarks are known; intended game backgrounds and final display scale remain unknown. This is a proposed project review method, not an adopted production-quality verdict.

Exact cited source text was retrieved from `.agents/skills/pixl-kit/resources/`:

| Source identity | Inclusive lines | Applicable reading |
| --- | --- | --- |
| `training/original-docs/PIXEL-ART-DEEP-RESEARCH.md`, SHA-256 `7efc4789ca70dfd9964abc2bc1100af318306236400e3496f7a0a5654f725e28` | 1402–1445 | Connected or semantically related clusters; names features such as silhouette, outline, and eye |
| Same source and hash | 857–867 | Conditions distinguish intentional single pixels, approved ramps, and edges intended to remain hard. No approved ramp or general hard-edge policy exists here, so those conditional restrictions do not become project rules |
| Same source and hash | 1563–1573 | Change metrics depend on semantic class and action; animation discussion does not prove static drone readability or a minimum size |
| `training/original-docs/PIXEL-ART-ASSETS.md`, SHA-256 `450a335ed6563a7f4a5cc380f2bbe72f98b70e532ac2c8d16a679bcc545d4900` | 11–15 | Another project's interaction-key/UI guidance; contextual clarity advice, not this project's palette, drone layout, or acceptance authority |

Loaded `k.semantic-clusters` and `k.silhouette-readability` from the bundled `knowledge/library.px` with the selected interpreter and resource root. Initial MCP context attempts returned `file_missing: e.alpha-contract: evidence/art-methods/poc-report.json` under the configured project root. Read-only runner retrieval with the installed resources as `--root` succeeded for both methods; no files or receipts were repaired or substituted.

Their linked existing receipt is `evidence/art-methods/poc-report.json`, SHA-256 `5d27f3e14a7aba09860956d9ae100146e8e28f7d5dfc7542f51ed4f52538d680`, observed `2026-09-14T13:29:02.597896+00:00`, scope `offline_reference_fixtures`. The `cluster-connectivity` fixture reports four-neighbor sizes `[1,1,1,4]` and eight-neighbor sizes `[1,2,4]`; it explicitly does not establish semantic importance or authorize singleton removal. The `key-silhouette-landmarks` fixture distinguishes a key's hole/shaft/teeth from a mutant; its receipt explicitly leaves visual recognition, background readability, and final artistic acceptance to inspection. These existing fixture receipts were read, not rerun, and establish neither this drone's production acceptance nor provider/engine capability.

Reference SHA-256: `1c45c866f9d11ff57b055f4dacf1e47c8e71f2c99fd6b24f0cb4259ee40cbe5c`.

Unchanged historical assessment SHA-256: `4f7db791ae8d97869b169c76bcfce93c6101e5497b1b682d649730a695e70521`.

## Handoff

The planning question is answered: retain the chosen aesthetic and develop one matching sample directly at 16×16 when production is requested. The inspected reference demonstrates available face space and detached antenna structure; a new matching sample remains untested.

No additional aesthetic decision or fixed-palette approval is needed to use this approach. Before a later in-game readability verdict, identify the intended background and display scale; those determine the relevant presentation test. They do not block this Markdown evaluation.

For the final authority audit, read this entire file, including the suggested prompt, all review rules, and recovery conclusions. A still-matching variation with a different teal, shifted antenna positions, a different gap, or an additional intentional detached detail must not fail solely for that difference. Only an actual failure to retain a user requirement or the visually assessed reference match supports rejection. This prevents observations and optional sample choices from silently becoming production rules.
