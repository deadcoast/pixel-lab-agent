# Reference analysis

Inspected both supplied images at native 32×32 scale and the retained 8× nearest-neighbor comparison. The images share a geometric, roughly rectangular body, two tall upper projections separated by a notch, and two pale rectangular facial marks. Neither reference supplies a distinct scout/medic role, equipment, legs, or a clear side-facing pose. The side-view requirement comes from the user.

| Measured property | reference.png | reference-b.png |
|---|---|---|
| Canvas | 32×32 | 32×32 |
| Occupied bounds, right/bottom exclusive | (7,3)–(25,28) | (7,3)–(25,28) |
| Occupied width × height | 18×25 | 18×25 |
| Visible pixels | 390 | 390 |
| Nontransparent colors | 3 | 2 |
| Fractional alpha pixels | 0 | 0 |
| Connected opaque components, 4-neighbor | 1 | 1 |
| Dark blue #25354A | 180 pixels | 0 |
| Turquoise #56B5BC | 186 pixels | 366 pixels |
| Pale gold #F4DDA2 | 24 pixels | 24 pixels |

Their alpha masks are byte-identical. Exactly 180 RGBA pixels differ, all changing from dark blue to turquoise. The references therefore isolate a color/edge treatment disagreement without changing silhouette geometry.

Visually, A has a substantial dark contour, including approximately two-pixel side and bottom borders, with solid dark upper projections. B replaces all that dark area with the body color. Calling A a generic one-pixel outline or calling B a selectively outlined variant would misdescribe these files. Both retain sharp rectangular clusters and flat color fills; neither establishes a lighting direction.

The existing silhouette cannot distinguish scout from medic because both inputs have the same mask. Role differentiation must be demonstrated in actual future candidates. Proposed equipment landmarks are a compact hood/visor and slim pack for the scout, and a wider medical satchel with a pale band or badge for the medic. These proposals do not establish anatomy, clothing, iconography, or a final palette.

The final canvas remains unresolved. A 32×32 first trial is proposed because it matches the references, but there is no concrete output contract. The final outline remains a recorded conflict. Observed binary transparency and the three source colors are not automatically imposed on production. Display scale, gameplay backgrounds, animation scope, and destination engine remain unspecified.

The [interactive comparison](../reference-review.html) displays the original files without editing them. The [retained comparison image](../evidence/reference-comparison.png) contains native and 8× views on a diagnostic light background. The light-background image and native inputs were visually inspected; interactive dark/patterned controls have not been exercised in a browser or game engine. They are review aids, not evidence of gameplay acceptance.

Raw properties, exact input SHA-256 identities, and color transitions are retained in [reference-measurements.json](../evidence/reference-measurements.json). PIXL asset-check passed its implemented source measurements. That result does not judge attractiveness, approve the proposed characters, or verify engine import.
