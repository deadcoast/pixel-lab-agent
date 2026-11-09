"""Build the PIXL specialist corrected proposal for the authoring-01 criteria review.

Read-only on the store/PLAR/jobs. Writes only:
  work/criteria-review-01/specialist-proposal.json
  work/criteria-review-01/specialist-report.json
Every criterion's original text/hash is copied verbatim from the retained
request-review.json; every cited source line range is verified to contain the
wording relied on; every historical record hash is re-measured from disk.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\github\pixel-lab-agent\evidence\criteria-handoff\20261109\native\claude-01\project")
OUT_DIR = ROOT / "work" / "criteria-review-01"
REPORT_PATH = OUT_DIR / "request-review.json"
PROPOSAL_PATH = OUT_DIR / "specialist-proposal.json"
SUMMARY_PATH = OUT_DIR / "specialist-report.json"

EXPECTED_REPORT_SHA = "5563d65e834448a88974f984817bc4d6c1ac91ea7b254624fb15b01740fb5068"
EXPECTED_RAW_SHA = "f0bb3c5c08ff3f5b7f4bdda09d56a7383209f3828b2074943856414ed3e80cc4"
EXPECTED_SCOPE_SHA = "aa2c114f0d722d6b8678adce97e1adaae7093d47d5acedd2a818f349dcfb72f0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


_lines_cache: dict[str, list[str]] = {}


def file_lines(rel: str) -> list[str]:
    if rel not in _lines_cache:
        text = (ROOT / rel).read_text(encoding="utf-8")
        _lines_cache[rel] = text.splitlines()
    return _lines_cache[rel]


verified_citations: list[dict] = []
citation_failures: list[str] = []
_sha_cache: dict[str, str] = {}


def S(rel: str, lines: list[int], expect: str) -> dict:
    """Return a verified source pointer with one-based inclusive file-local bounds."""
    first, last = lines
    content = file_lines(rel)
    if not (1 <= first <= last <= len(content)):
        raise SystemExit(f"bounds out of range: {rel} {lines} (file has {len(content)} lines)")
    segment = "\n".join(content[first - 1 : last])
    if expect not in segment:
        citation_failures.append(f"citation not verified: {rel} {lines} does not contain {expect!r}")
    if rel not in _sha_cache:
        _sha_cache[rel] = sha256(ROOT / rel)
    pointer = {"path": rel, "sha256": _sha_cache[rel], "lines": [first, last]}
    verified_citations.append({**pointer, "verified_wording": expect})
    return pointer


# ---------------------------------------------------------------- report ----
if sha256(REPORT_PATH) != EXPECTED_REPORT_SHA:
    raise SystemExit("request-review.json hash changed; refusing to build against a different report")
if sha256(OUT_DIR / "request-review-raw.txt") != EXPECTED_RAW_SHA:
    raise SystemExit("request-review-raw.txt hash changed")
report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
if report["review_scope_sha256"] != EXPECTED_SCOPE_SHA:
    raise SystemExit("review_scope_sha256 mismatch")
criteria_by_id = {c["id"]: c for c in report["criteria"]}
if list(criteria_by_id) != report["criterion_ids"] or len(criteria_by_id) != 20:
    raise SystemExit("criterion id list mismatch")
for c in report["criteria"]:
    if c["record_sha256"] != c["current_record_sha256"] or c["record_status"] != "current":
        raise SystemExit(f"record not current: {c['id']}")

# ------------------------------------------------------- source pointers ----
BRIEF_MAIN = S("BRIEF.md", [3, 3], "Working uses four horizontal frames with a 100 ms frame duration")
BRIEF_PATHS = S("BRIEF.md", [5, 5], "Assets belong at the paths already used by the view")
BRIEF_PAUSED = S("BRIEF.md", [7, 7], "distinguishable from activity, completion and retry without relying on color alone")
BRIEF_READY = S("BRIEF.md", [9, 9], "check mark with asymmetrical arms")

QV_IDLE = S("src/queue-view.ts", [3, 3], 'idle: { label: "Start", path: "assets/start.svg", frames: 1 }')
QV_RUNNING = S("src/queue-view.ts", [4, 4], 'running: { label: "Working", path: "assets/working.png", frames: 4 }')
QV_PAUSED = S("src/queue-view.ts", [5, 5], 'paused: { label: "Paused", path: "assets/paused.png", frames: 1 }')
QV_FAILED = S("src/queue-view.ts", [7, 7], 'failed: { label: "Retry", path: "assets/error-retry.png", frames: 1 }')
QV_DISPLAY = S("src/queue-view.ts", [9, 9], 'display = { cell: [16, 16], scale: 3, filter: "nearest", frameMs: 100, background: "#172336" }')
QV_CONSUMERS = S("src/queue-view.ts", [10, 11], "export function compactStatus(state: QueueState) { return statusVisuals[state]; }")
QV_ALL = S("src/queue-view.ts", [2, 11], "statusVisuals")

QS_STATE = S("src/queue.ts", [1, 1], '"idle" | "running" | "succeeded" | "failed" | "paused"')
QS_AFTER = S("src/queue.ts", [2, 3], 'started: "running", ok: "succeeded", error: "failed", pause: "paused"')

VM_PANELVAR = S("renderer/view.mjs", [4, 5], "const panel = display.background")
VM_EVENTS = S("renderer/view.mjs", [9, 9], "['idle', 'started', 'pause', 'ok', 'error']")
VM_FETCH = S("renderer/view.mjs", [18, 18], "fetch(`/${path}`)")
VM_PAINT = S("renderer/view.mjs", [30, 41], "function paint(canvas, asset, frames, scale, elapsed)")
VM_FRAME = S("renderer/view.mjs", [32, 32], "Math.floor(Math.max(elapsed, 0) / display.frameMs) % frames")
VM_SMOOTH = S("renderer/view.mjs", [34, 34], "imageSmoothingEnabled = display.filter !== 'nearest'")
VM_PANELFILL = S("renderer/view.mjs", [35, 36], "context.fillStyle = panel")
VM_GEOM = S("renderer/view.mjs", [37, 38], "asset.width === width * frames && asset.height === height")
VM_LABEL = S("renderer/view.mjs", [49, 49], "label.textContent = descriptor.label")
VM_FIRSTPAINT = S("renderer/view.mjs", [56, 56], "info.frame = paint(canvas, asset, descriptor.frames, scale, elapsed)")
VM_GEOMMATCH = S("renderer/view.mjs", [57, 59], "Wrong sheet size")
VM_MATRIX = S("renderer/view.mjs", [71, 74], "for (const scale of [1, display.scale])")
VM_SELECT = S("renderer/view.mjs", [81, 88], "const state = event === 'idle' ? 'idle' : stateAfter(event)")
VM_LIVESCALE = S("renderer/view.mjs", [83, 83], "makeCell(consumer, state, display.scale, 0, false)")
VM_ANIMATE = S("renderer/view.mjs", [91, 97], "if (cell.canvas && cell.descriptor.frames > 1)")
VM_TIMELINE = S("renderer/view.mjs", [107, 116], "[i * display.frameMs, (i + 1) * display.frameMs - 1]")
VM_TIMELINE_STATIC = S("renderer/view.mjs", [110, 110], "if (descriptor.frames <= 1) continue")
VM_VIEWS = S("renderer/view.mjs", [117, 122], "getBoundingClientRect")
VM_SCOPE = S("renderer/view.mjs", [123, 124], "Image provenance and visual/style acceptance are separate")

IH_PIXELATED = S("renderer/index.html", [21, 21], "image-rendering: pixelated")
IH_MEDIA = S("renderer/index.html", [27, 27], "@media(max-width: 800px)")

CP_BOUNDS = S("renderer/check.py", [67, 74], "screenshot matches canvas pixels")
CP_TIMELINE = S("renderer/check.py", [87, 93], 'frame_index = (sample["elapsed"] // report["display"]["frameMs"]) % descriptor["frames"]')
CP_SCOPE = S("renderer/check.py", [101, 101], "sampled frame boundaries are not a review of animation quality")

AP = "authoring-plar.txt"
AP_W_PURPOSE = S(AP, [422, 422], "the reduced-motion mode must use a stationary Working symbol distinguishable from Ready and Paused")
AP_W_CONSUMERS = S(AP, [424, 445], '"symbol": "compactStatus"')
AP_W_CELL = S(AP, [453, 465], '"property": "cell_size_px"')
AP_W_BG = S(AP, [466, 474], "it does not restrict alpha to binary values")
AP_W_READ = S(AP, [475, 484], '"property": "pixel_art_readability"')
AP_W_PANEL = S(AP, [485, 493], '"value": "#172336"')
AP_W_COLOR = S(AP, [494, 502], "Use the existing cool blue UI accent; no fixed palette is required.")
AP_W_ACCENT = S(AP, [503, 511], '"value": "#70b9ed"')
AP_W_STYLE = S(AP, [512, 528], "this is a new adopted project choice,not an original brief requirement")
AP_W_GEOM = S(AP, [529, 545], "Four horizontal frames in 16 by 16 cells imply a 64 by 16 image strip.")
AP_W_ANIM = S(AP, [546, 559], '"frame_duration_ms": 100')
AP_W_MEANING = S(AP, [560, 570], "Show activity, avoiding completion/success silhouettes or a success-like terminal pose.")
AP_W_MOTIF = S(AP, [571, 577], "A four-phase rotating or pulsing activity mark is a proposal")
AP_W_RENDER = S(AP, [578, 595], '"source_rectangle": "frame*16,0,16,16"')
AP_W_PAUSEDIST = S(AP, [596, 604], "Paused must be distinguishable from activity, completion and retry without relying on color alone.")
AP_W_CHECKS = S(AP, [606, 619], "Play the loop at 100 ms per frame and inspect the fourth-to-first transition")
AP_R_PURPOSE = S(AP, [679, 679], "Show failed work and the Retry action")
AP_R_BG = S(AP, [723, 731], "it does not restrict alpha to binary values")
AP_R_STYLE = S(AP, [769, 785], '"property": "approved_style_reference"')
AP_R_GEOM = S(AP, [786, 799], "Retry is static and occupies one 16 by 16 logical cell.")
AP_R_MEANING = S(AP, [800, 810], "Signal failed work / retry and remain distinguishable from the other statuses without color alone.")
AP_R_MOTIF = S(AP, [811, 817], "A return/retry arrow with a distinct silhouette is a proposal")
AP_R_DEST = S(AP, [827, 836], "The current failure visual destination is assets/error-retry.png")
AP_R_CHECKS = S(AP, [838, 851], "grayscale comparison with Start, Ready and all Working frames")
AP_START_CHECKS = S(AP, [990, 996], "Keep the original SVG byte hash unchanged.")
AP_P_PURPOSE = S(AP, [1005, 1005], "Show paused work in both full and compact status cells")
AP_P_BG = S(AP, [1054, 1062], "it does not restrict alpha to binary values")
AP_P_STYLE = S(AP, [1100, 1116], '"property": "approved_style_reference"')
AP_P_GEOM = S(AP, [1117, 1130], "The updated Paused descriptor uses one frame in the existing 16 by 16 logical cell.")
AP_P_DIST = S(AP, [1131, 1139], "Paused must be distinguishable from activity, completion and retry without relying on color alone.")
AP_P_MOTIF = S(AP, [1140, 1146], "A pair of pause bars is a proposed starting point")
AP_P_CHECKS = S(AP, [1158, 1167], "including grayscale/non-color comparison; require a clearly distinct silhouette")

SP = ".pixl/assets/queue.ready/state.px"
SP_CT_PAUSED = S(SP, [47, 47], "@family.paused.contract:C{al=full")
SP_CT_RETRY = S(SP, [56, 56], "@family.retry.contract:C{al=full")
SP_CT_WORKING = S(SP, [62, 62], "Review every frame and actual loop,loop boundary,anchor and volume stability")
SP_V_PAUSED02 = S(SP, [183, 183], "Opaque magenta intermediate fails final transparent-exterior criterion")
SP_CT_SEED = S(SP, [223, 223], "proposed orbiting separated blocks")
SP_V_ANIM01 = S(SP, [258, 258], "contains193 opaque #808080 pixels in its background")
SP_V_REPAIR = S(SP, [320, 320], "Segments morph and near-hold across phases2/3, then jump atwrap")
SP_DEC_DEST = S(SP, [386, 386], "Accept available-member destination checks for exact Ready baseline")
SP_CH_DEST = S(SP, [391, 391], "Supplied browser fixture executing actual queue modules")
SP_CH_STYLE = S(SP, [392, 392], "deliberate coherent clusters and stepped edges")
SP_DEC_STYLE = S(SP, [393, 393], "Adopt exact ready.retained as representative status-family style baseline")

CC = "work/family-render-review/caller-comparison-final.json"
CC_SCOPE = S(CC, [113, 113], "controlled fixture, no PixelLab-generated quality claim")
CC_CARRY = S(CC, [114, 119], "Coherent deliberate pixel clusters and stepped edge treatment")
CC_NOTP = S(CC, [120, 125], "Exact stroke weight, margin or footprint")
CC_RATIONALE = S(CC, [126, 126], "no matte/fringe or resampling blur")
CC_ABSENT = S(CC, [180, 185], "Absent Working gives no playback-quality evidence")

SA = "work/family-render-review/specialist-assessment.json"
SA_CRAFT = S(SA, [166, 171], "Selective antialiasing remains permitted by the full-alpha contract")
SA_STYLE = S(SA, [201, 204], "do not carry completion check motif")
SA_START = S(SA, [205, 210], "Flat right-pointing cool-blue triangle, visually distinct from Ready")
SA_INV_W = S(SA, [235, 240], "activity never success; review actual timed loop and boundaries")
SA_INV_R = S(SA, [241, 246], "no invented motif requirement")
SA_INV_P = S(SA, [247, 252], "distinct from activity/completion/retry without color")
SA_FUTURE = S(SA, [255, 259], "actual side-by-side/grayscale family views")

RS_AUTH = S("RENDER-STAGE.md", [5, 6], "authorized to make the scoped caller style decision")
RS_RENDER = S("RENDER-STAGE.md", [10, 16], "renderer/check.py --project . --capture DIRECTORY")
RS_FAMILY = S("RENDER-STAGE.md", [26, 33], "distinguish absent members from rejected ones")

FJ = "work/pixl-render-recheck-01/findings.json"
FJ_SOURCES = S(FJ, [74, 81], '"renderer/view.mjs"')
FJ_OUTCOME = S(FJ, [83, 83], "integer placement/screenshot correspondence")
FJ_LIMITS = S(FJ, [84, 89], "Working actual 100ms playback and full family destination remain unperformed")

AS_QUAL = S("AUTHORING-STAGE.md", [11, 14], "not turn the reference's measured colors, alpha or cluster count into new owner")
AS_OP = S("AUTHORING-STAGE.md", [26, 30], "official-discovery.json")
AS_ASSEMBLY = S("AUTHORING-STAGE.md", [31, 32], "retain the\nexact intended frame-selection/assembly policy and its separate review obligations")

AU_REQ = S("AUTHORING-UPDATE.md", [2, 4], "a stationary Working\nsymbol distinct from Ready and Paused")
AU_SCOPE = S("AUTHORING-UPDATE.md", [5, 10], "Do not remove or rewrite the prepared request")

AR = "AUTHORING-RESULT.json"
AR_POLICY = S(AR, [84, 84], '"frame_selection_assembly_policy"')
AR_UPDATE = S(AR, [89, 89], '"previous_requirements_hash": "e0614bd962a53a19003707f3d73326be436891e198eb1e4a262f12412fbfb027"')
AR_IDENT = S(AR, [93, 93], '"bound_in_plan_and_request": "e0614bd962a53a19003707f3d73326be436891e198eb1e4a262f12412fbfb027", "current": "2901c7107d4f162e98653140ea8061dfe213821b22a5e1338d9d2d6de5b4ad0c"')
AR_ROTATION = S(AR, [120, 121], "160 patches")
AR_CONSUMER = S(AR, [124, 124], "no reduced-motion key, path, state or preference check")
AR_TRANSRGB = S(AR, [130, 130], "210 fully transparent pixels carry RGB 128,128,128")
AR_NEXT = S(AR, [151, 156], "decide how reduced motion maps in src/queue-view.ts")

RP = "work/authoring-01/working-rotation-policy.json"
RP_DEST = S(RP, [6, 38], '"frame_index": "floor(elapsed/100) mod 4')
RP_STEP1 = S(RP, [39, 45], "no gutters, padding, scaling or recolor")
RP_STEP2 = S(RP, [46, 52], "dst(x,y)=src(y,15-x) per 90 degrees")
RP_TRANS = S(RP, [52, 52], "#00000000 (all 224 transparent seed pixels are RGBA 0,0,0,0)")
RP_PLAY = S(RP, [1016, 1016], "angular velocity is uniform and the loop boundary is not a special case")
RP_OBLIG = S(RP, [1017, 1023], "pixel-exact: each delivered cell equals cw^k(seed) (local check)")

RR = "work/criteria-review-01/request-review.json"
RR_REQUEST = S(RR, [814, 918], '"id": "authoring-01.working.join-01"')
RR_NOTES = S(RR, [837, 837], "step 1 of a two-step deterministic official construction")
RR_MODE = S(RR, [836, 836], '"mode": "low"')
RR_SELECTION = S(RR, [1136, 1138], '"current_requirements_hash": "2901c7107d4f162e98653140ea8061dfe213821b22a5e1338d9d2d6de5b4ad0c"')

OD_WB = S("official-discovery.json", [14, 15], "join <image> <image>")

JOB = ".pixl/assets/queue.ready/jobs/d9badc9cf64c04f7adc812f2e245d4af8caf38bb63f102e4304c4e83bed1290d.json"
PACKET = ".pixl/assets/queue.ready/stage-requests/84dcf243f2cd22b69fa7ac906bfc33e7abd55bf113c2cc6db7566cb87bd4b1f8.json"
PLAN = ".pixl/assets/queue.ready/production-plans/b025e867d863f5ad28b47127d3384ea5f191d459573394521504243abd95d826.json"
JOB_PTR = S(JOB, [1, 1], '"authoring-01.working.join-01"')
PACKET_PTR = S(PACKET, [1, 1], '"--columns","4"')

SEED_ART = ".pixl/assets/queue.ready/artifacts/21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png"
MOTION_ART = ".pixl/assets/queue.ready/artifacts/cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc.png"

# ----------------------------------------------------------- measurements ----
measurements = [
    {
        "path": SEED_ART,
        "sha256": sha256(ROOT / SEED_ART),
        "method": "pixl_asset_check(alpha=full), 4-connectivity on nonzero alpha; zero-based coordinates",
        "result": {"width": 16, "height": 16, "visible_pixels": 32, "visible_colors": 9, "fractional_alpha_pixels": 0, "opaque_components": 3, "visible_bbox": [3, 3, 14, 14]},
        "use": "Supports scoping 'stable cluster count' to the seed-rotation construction: the seed has three 4-connected components and a quarter-turn permutation preserves that count and the visible-pixel volume.",
    },
    {
        "path": MOTION_ART,
        "sha256": sha256(ROOT / MOTION_ART),
        "method": "pixl_asset_check(alpha=full) on the accepted original-production motion strip live.working-animation-motion-01.candidate",
        "result": {"width": 64, "height": 16, "visible_pixels": 128, "visible_colors": 9, "fractional_alpha_pixels": 0, "opaque_components": 12, "visible_bbox": [3, 2, 62, 14]},
        "use": "12 components = 3 per cell and 128 visible = 32 per cell: consistent with cw^k(seed) per cell as the policy claims. Not a visual verdict.",
    },
]
seed_sha = measurements[0]["sha256"]
if seed_sha != "21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629":
    raise SystemExit("seed artifact hash changed")

# ------------------------------------------------------------------ helpers --
def clause(text, authority, basis, scope, sources):
    return {"text": text, "authority": authority, "basis": basis, "scope": scope, "source": sources}


ROUTE_FIXTURE = (
    "'the actual consumer renderer' means the supplied browser fixture renderer/view.mjs executing the actual "
    "src/queue.ts and src/queue-view.ts modules (render.choice.destination engine; RENDER-STAGE.md). src/queue-view.ts "
    "itself only returns the descriptor and display constants; slicing, sampling, compositing and frame advance are "
    "implemented in the fixture."
)
SCALE_FACT = (
    "In the fixture, stateAfter transitions render the two live cells at display.scale (3) only (view.mjs line 83); "
    "the 1x and 3x cells come from the state matrix keyed by state name (lines 71-74). Both routes call the same "
    "statusCell/compactStatus functions, which are identical bodies returning statusVisuals[state]."
)
TIMING_FACT = (
    "The fixture does not measure wall-clock frame duration. Its evidence for frame advance is (a) the capture timeline, "
    "which paints statusCell at elapsed 0,99,100,199,200,299,300,399 and 400 ms and records the frame index "
    "(floor(elapsed/100) mod frames; 400 ms wraps to frame 0), checked by renderer/check.py lines 87-93, and (b) the "
    "running requestAnimationFrame loop for descriptors with frames > 1, which a reviewer observes visually. check.py "
    "line 101 states that sampled frame boundaries are not a review of animation quality."
)

STYLE_CLAUSES = lambda plural: [  # noqa: E731
    clause(
        "Readable compact silhouette" + ("s" if plural else ""),
        "requirement",
        "BRIEF line 3 requires readable silhouettes at 1x and 3x on the dark panel; 'compact' comes from the adopted scoped style decision (render.choice.style carry list), a caller decision authorized by RENDER-STAGE.md, not the original brief.",
        "whole asset; 'compact' scoped to this consumer status family",
        [BRIEF_MAIN, SP_CH_STYLE, RS_AUTH, AP_W_READ],
    ),
    clause(
        "deliberate coherent clusters and stepped edges",
        "requirement",
        "Adopted scoped caller style decision render.choice.style / render.decision.style (carry: 'deliberate coherent clusters and stepped edges'), recorded in authoring-plar approved_style_reference as a new adopted project choice. Literal 'stepped edges' must not be read to forbid selective intentional anti-aliasing, which the full-alpha contract and the specialist assessment explicitly permit; it forbids accidental resampling blur and stray noise.",
        "this consumer status family (scoped adoption)",
        [SP_CH_STYLE, SP_DEC_STYLE, CC_CARRY, SA_CRAFT, AP_W_STYLE],
    ),
    clause(
        "a perceptible cool-blue accent related to the Ready baseline and the preserved Start accent",
        "requirement",
        "BRIEF line 3: 'the existing UI's cool blue accent; a fixed palette is not required'. The relation to Start's #70b9ed is an observation (authoring-plar existing_accent), not an exact-colour rule.",
        "whole asset",
        [BRIEF_MAIN, AP_W_COLOR, AP_W_ACCENT, SA_START],
    ),
    clause(
        "judged qualitatively at 1x and 3x on #172336",
        "requirement",
        "BRIEF line 3 inspection conditions; #172336 is display.background (observation from src/queue-view.ts line 9).",
        "whole asset",
        [BRIEF_MAIN, QV_DISPLAY, AP_W_PANEL],
    ),
    clause(
        "no exact hex, palette count, binary alpha, stroke width or margin rule",
        "observation",
        "Explicit non-restriction mirroring render.choice.style not_fixed and AUTHORING-STAGE.md lines 11-14 (do not turn measured colours/alpha/cluster count into owner requirements). It removes nothing required; keep.",
        "whole asset",
        [SP_CH_STYLE, CC_NOTP, AS_QUAL],
    ),
]

STYLE_PROPOSED = lambda plural: (  # noqa: E731
    f"Readable compact silhouette{'s' if plural else ''}, deliberate coherent clusters and stepped edges consistent with the exact Ready baseline "
    "(selective, intentional anti-aliasing is permitted under the full-alpha contract; accidental resampling blur or stray noise is not), "
    "and a perceptible cool-blue accent related to the Ready baseline and the preserved Start accent, judged qualitatively at 1x and 3x on #172336; "
    "no exact hex, palette count, binary alpha, stroke width or margin rule."
)
STYLE_ALT = (
    "A mark whose diagonal strokes carry one intermediate-alpha pixel per step as selective anti-aliasing: readable, coherent with Ready, cool-blue, "
    "transparent exterior, explicitly allowed by the al=full contract and the specialist assessment. A literal reading of 'stepped edges' could reject it; "
    "the clarified wording does not. (Tests the 'stepped edges' clause.)"
)

TRANSPARENT_ALT = (
    "A mark drawn on a small deliberate dark-blue badge (e.g. 10x10 rounded plate) with transparent cell edges and corners: BRIEF's 'transparent backgrounds' "
    "holds, yet the literal 'no ... plate' clause rejects it. A second alternative: a candidate whose alpha-0 pixels carry RGB 128,128,128 (as the accepted "
    "motion strip cell 0 does per AUTHORING-RESULT.json line 130) satisfies 'alpha 0' and must not be rejected on RGB of transparent pixels. "
    "(Tests the 'plate' clause and the review route.)"
)


def transparent_entry(stage_word, marks_word, example_clause, example_sources, extra_sources):
    text_marks = marks_word
    clauses = [
        clause(
            f"all pixels outside the {text_marks} have alpha 0",
            "requirement",
            "BRIEF line 3 'transparent backgrounds'; authoring-plar background requirement (transparent; binary alpha not required). Which opaque pixels are 'the mark' is a visual judgment, except under the seed-rotation construction where the exterior is exactly the alpha-0 set of cw^k(seed) and is mechanically decidable.",
            "whole asset (outcome); mechanical form only under the seed-rotation construction",
            [BRIEF_MAIN] + extra_sources,
        ),
        clause(
            "no opaque matte, plate" + (", grey tile" if stage_word == "working" else "") + " or fringe",
            "requirement",
            "Unintended canvas matte / grey tile / fringe violates the transparent-background requirement (historical verdict evidence). 'Plate' as a blanket prohibition is an expert construction preference: the PIXL profile distinguishes an unintended canvas matte from a deliberate plate/badge/backing with transparent exterior, which the brief does not forbid.",
            "matte/tile/fringe: whole asset (requirement); 'no deliberate plate': expert proposal, scoped to this authoring branch's construction",
            [BRIEF_MAIN, CC_RATIONALE] + example_sources,
        ),
    ]
    if example_clause:
        clauses.append(
            clause(
                example_clause,
                "observation",
                "Historical failure evidence retained in the store; it illustrates the failure class and does not define the rule.",
                "example only",
                example_sources,
            )
        )
    clauses.append(
        clause(
            "Partial alpha on mark pixels is permitted; binary alpha is not required.",
            "observation",
            "Contract al=full; authoring-plar background requirement reason; caller style decision not_prescribed 'Binary alpha'. Non-restriction; keep.",
            "whole asset",
            [AP_W_BG if stage_word == "working" else (AP_R_BG if stage_word == "retry" else AP_P_BG), CC_NOTP],
        )
    )
    return clauses


# ------------------------------------------------------------ the 20 rows ----
analysis: dict[str, dict] = {}

analysis["authoring-01.working.q.geometry"] = {
    "clauses": [
        clause(
            "Decode the delivered PNG as exactly 64x16",
            "requirement",
            "BRIEF line 3 (16x16 cells, four horizontal frames) with src/queue-view.ts running frames 4 and display.cell [16,16]; the renderer fixture draws nothing unless width == 16*frames and height == 16 and marks 'Wrong sheet size' otherwise (consumer code behavior).",
            "whole Working asset",
            [BRIEF_MAIN, QV_RUNNING, QV_DISPLAY, VM_GEOM, VM_GEOMMATCH, AP_W_GEOM],
        ),
        clause(
            "four horizontal 16x16 cells at x=0,16,32,48",
            "requirement",
            "Consumer code behavior: the fixture slices drawImage(frame*16, 0, 16, 16) (renderer/view.mjs line 38); authoring-plar image_geometry.",
            "whole Working asset",
            [VM_GEOM, AP_W_GEOM, AP_W_RENDER],
        ),
        clause(
            "with no gutters, padding or extra canvas",
            "requirement",
            "Gutters or extra canvas change the 64x16 geometry or shift cell content under frame*16 slicing (consumer code). 'Padding' is ambiguous: transparent margin inside a 16x16 cell is normal pixel-art composition and is not prohibited by any source; the join-result expectation 'no gutters, padding' in the rotation policy refers to added canvas between/around cells.",
            "whole Working asset; wording clarified",
            [VM_GEOM, RP_STEP1, BRIEF_MAIN],
        ),
        clause(
            "the consumer slices frame*16,0,16,16 for frames=4 and advances at display.frameMs 100 ms per frame",
            "observation",
            "Correct facts, wrong attribution: slicing and frame advance are implemented in the supplied renderer fixture renderer/view.mjs paint() (lines 30-41: floor(max(elapsed,0)/frameMs) % frames); src/queue-view.ts supplies frames 4 and frameMs 100 only. render.choice.destination records the engine as 'Supplied browser fixture executing actual queue modules'.",
            "consumer behavior observation",
            [VM_PAINT, VM_FRAME, QV_DISPLAY, SP_CH_DEST, AP_W_RENDER],
        ),
        clause(
            "(nominal 400 ms cycle)",
            "observation",
            "Arithmetic from BRIEF 4 frames x 100 ms; authoring-plar animation requirement nominal_cycle_ms 400.",
            "observation",
            [AP_W_ANIM],
        ),
    ],
    "proposed_check": (
        "Decode the delivered PNG as exactly 64x16: four horizontal 16x16 cells at x=0,16,32,48 with no gutters or added canvas between or around the cells "
        "(transparent margin inside a cell is composition, not padding). Basis: src/queue-view.ts declares running frames 4, display.cell [16,16] and frameMs 100; "
        "the supplied renderer fixture renderer/view.mjs draws only when width == 16*frames and height == 16, slices frame*16,0,16,16 and advances "
        "floor(elapsed/100) mod 4 (nominal 400 ms cycle)."
    ),
    "proposed_domain": "mechanical",
    "proposed_mode": "local",
    "change": "clarify",
    "change_explanation": (
        "Old: 'no gutters, padding or extra canvas' and 'the consumer slices ...'. New: 'padding' defined as added canvas between/around cells so transparent "
        "in-cell margins are not rejected; slicing/advance attributed to the renderer fixture (renderer/view.mjs) with src/queue-view.ts supplying frames and frameMs. "
        "Geometry requirement unchanged."
    ),
    "discriminating_alternative": (
        "(1) A 68x16 sheet with 1-px transparent gutters (cells at x=0,17,34,51) still holds four 16x16 frames at 100 ms as the brief's prose says, but the fixture "
        "refuses it ('Wrong sheet size'): the literal check rejects it and the rejection is source-supported by consumer code. (2) A 64x16 sheet whose marks occupy "
        "10x10 of each cell with 3-px transparent margins is brief-conforming; the original word 'padding' could be read to reject it, the clarified text cannot."
    ),
}

analysis["authoring-01.working.q.transparent-exterior"] = {
    "clauses": transparent_entry(
        "working",
        "activity marks (in every cell)",
        "(the rejected generated frame whose background held 193 opaque #808080 pixels is this failure class)",
        [SP_V_ANIM01],
        [AP_W_BG, RP_TRANS],
    ),
    "proposed_check": (
        "Split into a measured part and a visual part. Measured (mechanical/local): retain every cell's alpha histogram and exact RGBA component boxes; no cell may contain "
        "an alpha>0 region that reaches all four cell edges or fills the cell (canvas matte / grey tile). Under the seed-rotation construction, each cell's alpha channel must "
        "equal that of cw^k(seed) (224 alpha-0 pixels per cell), which decides the exterior mechanically; RGB values of alpha-0 pixels are not significant. "
        "Visual (visual/visual): viewed at 1x and 3x on #172336, the exterior of every frame shows the panel with no unintended matte, tile, halo or fringe; a deliberate "
        "opaque backing shape is acceptable only when it is part of the mark's recorded design and the exterior stays transparent. The rejected frame with 193 opaque "
        "#808080 background pixels (live.working-animation-01.review.verdict.1) is the failure class. Partial alpha on mark pixels is permitted; binary alpha is not required."
    ),
    "proposed_domain": "visual (if kept as one record); otherwise mechanical for the measured record and visual for the visual record",
    "proposed_mode": "visual (if kept as one record); otherwise local + visual",
    "change": "correct",
    "change_explanation": (
        "Old: one mechanical/local check that asks which pixels are 'outside the activity marks' and whether a 'plate' is present. New: the exterior decision is made "
        "mechanical only where it actually is (seed-rotation construction: alpha channel equals cw^k(seed)); otherwise the matte/plate/fringe judgment is routed to a "
        "visual review with saved native/enlarged views. 'No plate' is narrowed to unintended matte/tile; a deliberate recorded backing shape is not rejected. "
        "Transparent-RGB values are declared insignificant (AUTHORING-RESULT.json line 130 evidence)."
    ),
    "discriminating_alternative": TRANSPARENT_ALT,
}

analysis["authoring-01.working.q.frame-assembly"] = {
    "clauses": [
        clause(
            "When the provider result is not already the exact 64x16 four-cell sheet (more frames than four, another layout, gutters or padding)",
            "observation",
            "Condition. For the prepared join route the expected result is already the destination geometry (rotation policy step_1), so the clause is conditional and may be vacuous for step 1; the step-2 edit still transforms cells and is covered by the construction-scoped clause below.",
            "this authoring branch",
            [RP_STEP1, RR_NOTES, OD_WB],
        ),
        clause(
            "the retained assembly record names the exact source frames or cell rectangles in play order",
            "requirement",
            "AUTHORING-STAGE.md lines 31-32 (caller assignment): if assembly is needed, retain the exact intended frame-selection/assembly policy and its separate review obligations. Process requirement of the assignment, not an owner art requirement.",
            "this authoring branch",
            [AS_ASSEMBLY, AR_POLICY, RP_STEP1],
        ),
        clause(
            "every delivered cell is a lossless copy: no resize, resample, recolor, duplication or silent frame drop",
            "requirement",
            "Assignment process requirement (exact assembly policy) plus expert practice. Two words need bounds: 'lossless copy' means identical alpha everywhere and identical RGBA where alpha>0 (RGB of alpha-0 pixels is not significant; the accepted motion strip carries RGB 128,128,128 on transparent pixels); 'duplication' means undocumented substitution of a copied frame for a missing one, not a deliberately repeated phase recorded in the assembly record (the brief fixes four frames, not four distinct frames).",
            "this authoring branch; wording clarified",
            [AS_ASSEMBLY, AR_TRANSRGB, RP_TRANS, BRIEF_MAIN, AP_W_MOTIF],
        ),
        clause(
            "all raw provider frames are retained beside the assembled strip",
            "requirement",
            "Evidence/process requirement from the assignment (retain the policy and its review obligations) and PIXL evidence discipline; the store's historical practice preserved raw candidates (verdict 258 'Preserve raw candidate').",
            "this authoring branch",
            [AS_ASSEMBLY, SP_V_ANIM01],
        ),
        clause(
            "[proposed addition, construction-scoped] under the seed-rotation construction, delivered cell k equals cw^k(seed) (dst(x,y)=src(y,15-x) per quarter-turn) on every pixel with alpha>0 and has identical alpha everywhere; the step-2 patch list, its measured transparent expected value and the workbench step ids are the assembly record",
            "proposal",
            "Expert method choice from the rotation policy and the prepared request notes; the caller independently recomputed the 160-patch set and the clockwise direction (AUTHORING-RESULT.json lines 120-121). This check is listed in the policy's separate review obligations but no Q record carries it; it is construction-scoped, not an owner requirement.",
            "seed rotation construction only",
            [RP_STEP2, RP_OBLIG, AR_ROTATION, RR_NOTES],
        ),
    ],
    "proposed_check": (
        "When the provider result is not already the exact 64x16 four-cell sheet (more frames than four, another layout, gutters or added canvas), the retained assembly "
        "record names the exact source frames or cell rectangles in play order and every delivered cell is a lossless copy: identical alpha everywhere and identical RGBA "
        "where alpha>0 (RGB of alpha-0 pixels is not significant); no resize, resample or recolor; no undocumented duplication or silent frame drop (a deliberately repeated "
        "phase is allowed when the record says so); all raw provider outputs are retained beside the assembled strip. Construction-scoped (seed-rotation construction only, "
        "expert choice): delivered cell k must equal cw^k(seed) under dst(x,y)=src(y,15-x) per quarter-turn, and the step-2 patch list, the measured transparent expected "
        "value and the workbench step ids form the assembly record."
    ),
    "proposed_domain": "mechanical",
    "proposed_mode": "local",
    "change": "clarify",
    "change_explanation": (
        "Old: 'lossless copy ... no ... duplication' unbounded. New: 'lossless' bounded to alpha + visible RGBA (transparent RGB insignificant); 'duplication' bounded to "
        "undocumented substitution so a recorded repeated phase is not rejected. Added an explicitly construction-scoped pixel-exact rotation clause that the policy lists "
        "as a review obligation but no Q record carries; it is a proposal, not an owner rule."
    ),
    "discriminating_alternative": (
        "(1) A pulsing Working motif whose frames 2 and 4 are identical by design and recorded as such: brief-conforming (four frames at 100 ms), but the literal "
        "'no ... duplication' rejects it. (2) A join result whose alpha-0 pixels carry RGB 128,128,128: visually identical to the seed, yet a byte-equality reading of "
        "'lossless copy' rejects it. Both are accepted by the clarified text; the construction-scoped rotation clause would reject a strip whose cell 2 is rotated "
        "counter-clockwise (58 visible-pixel differences per AUTHORING-RESULT.json line 120), which is the intended discrimination for that construction only."
    ),
}

analysis["authoring-01.working.q.activity-not-success"] = {
    "clauses": [
        clause(
            "Viewed at 1x and 3x nearest on #172336",
            "requirement",
            "BRIEF line 3 inspection conditions; #172336 is display.background.",
            "whole Working asset",
            [BRIEF_MAIN, QV_DISPLAY],
        ),
        clause(
            "beside the exact Ready baseline",
            "proposal",
            "Comparison method chosen by the specialist/caller style adoption (exact ready.retained as baseline). Useful, not an owner requirement.",
            "method",
            [SP_CH_STYLE, CC_SCOPE],
        ),
        clause(
            "each frame and the running loop read as ongoing activity",
            "requirement",
            "BRIEF line 3: 'The working loop must communicate activity without looking like success' (loop). Reading each individual frame is an expert extension: frames are shown singly for 100 ms, frame 0 is painted at elapsed 0 when the cell is created (view.mjs line 56), and a stalled animation shows one frame. Kept as requirement for the loop; per-frame reading retained as expert quality clause with that rationale.",
            "loop: whole asset (requirement); per-frame: expert clause, whole asset",
            [BRIEF_MAIN, AP_W_MEANING, VM_FIRSTPAINT],
        ),
        clause(
            "no frame forms a check mark",
            "requirement",
            "Derived: BRIEF line 9 makes the Ready completion symbol a check mark; a frame forming a check would look like success (BRIEF line 3).",
            "whole Working asset",
            [BRIEF_MAIN, BRIEF_READY],
        ),
        clause(
            "an arrowhead, pause bars",
            "proposal",
            "Expert guidance derived from the preserved Start triangle (BRIEF line 3; assessment 'right-pointing triangle') and from the PROPOSED Retry arrow and Paused pause-bar motifs in authoring-plar (authority: proposal). The binding outcome is distinction from the delivered Retry/Paused marks and the preserved Start, which authoring-01.delivery.q.distinction judges against the actual members.",
            "expert guidance; this authoring branch",
            [AP_R_MOTIF, AP_P_MOTIF, SA_START, BRIEF_PAUSED],
        ),
        clause(
            "or a success-like terminal pose",
            "requirement",
            "authoring-plar state_meaning requirement: 'avoiding completion/success silhouettes or a success-like terminal pose'.",
            "whole Working asset",
            [AP_W_MEANING, BRIEF_MAIN],
        ),
    ],
    "proposed_check": (
        "Viewed at 1x and 3x nearest on #172336 (beside the exact Ready baseline as the comparison method), the running loop and each individual frame read as ongoing "
        "activity and not as completion: no frame forms a check mark or another success-like terminal pose. Expert guidance, scoped to this branch: avoid frames that read as "
        "the static symbol of another member (for example the preserved Start arrowhead or paired pause bars); the binding distinction against the delivered Retry and Paused "
        "marks is judged in authoring-01.delivery.q.distinction."
    ),
    "proposed_domain": "visual",
    "proposed_mode": "visual",
    "change": "clarify",
    "change_explanation": (
        "Old: 'no frame forms a check mark, an arrowhead, pause bars or a success-like terminal pose' as one rule. New: check mark / terminal pose stay required (success "
        "confusion, BRIEF lines 3 and 9); 'arrowhead' and 'pause bars' become scoped expert guidance because they derive from proposed motifs of other members; the binding "
        "distinction is delegated to the delivery distinction criterion. Visual route unchanged."
    ),
    "discriminating_alternative": (
        "A two-segment spinner whose horizontal phase briefly resembles two parallel bars: the loop reads as activity and a delivered Paused mark of another shape (e.g. a "
        "boxed square) remains distinct, satisfying BRIEF lines 3 and 7; the literal 'no frame forms ... pause bars' rejects it. (Tests the 'pause bars' clause.)"
    ),
}

analysis["authoring-01.working.q.motion-continuity"] = {
    "clauses": [
        clause(
            "Play the actual four frames at 100 ms per frame including the fourth-to-first wrap",
            "requirement",
            "BRIEF line 3 (four frames, 100 ms); authoring-plar animation requirement loop:true and delivery check 'inspect the fourth-to-first transition'; family.working.contract review obligation 'actual loop, loop boundary'; the fixture wraps via mod frames.",
            "whole Working asset",
            [BRIEF_MAIN, AP_W_ANIM, AP_W_CHECKS, SP_CT_WORKING, VM_FRAME],
        ),
        clause(
            "stable center and anchor",
            "proposal",
            "Expert quality clause carried by the adopted stage contract family.working.contract ('anchor and volume stability'), which binds this stage; not in the brief. Rationale: both consumers draw into a fixed 16x16 cell, so drift reads as jitter.",
            "whole Working asset under family.working.contract",
            [SP_CT_WORKING, QV_DISPLAY],
        ),
        clause(
            "stable cluster count and volume in every phase",
            "proposal",
            "'Volume' stability: contract clause (expert, binding for this stage). 'Cluster count' stability: construction-scoped expert clause; the seed measures three 4-connected components and a quarter-turn permutation preserves count and volume (measured), but a brief-conforming pulsing design may legitimately change its cluster count. AUTHORING-STAGE.md lines 11-14 forbid turning the reference's cluster count into an owner requirement.",
            "volume: whole asset under contract; cluster count: seed rotation construction only",
            [SP_CT_WORKING, AS_QUAL, RP_OBLIG, SP_CT_SEED],
        ),
        clause(
            "deliberate stepped phases with no morphing",
            "proposal",
            "Construction-scoped expert clause (quarter-turn phases). The required outcome behind it is temporally coherent motion; the rejected AI animation failed because its morphing was incoherent (verdict 320), not because change of shape is forbidden.",
            "seed rotation construction only",
            [RP_PLAY, SP_V_REPAIR, AP_W_MOTIF],
        ),
        clause(
            "near-hold or wrap jump (the rejected AI-animation failure class)",
            "proposal",
            "'Wrap jump': required outcome derived from loop:true and the contract's loop-boundary review (requirement). 'Near-hold': expert even-spacing clause (at 4 x 100 ms a held pair reads as a stutter), scoped as expert quality judgment. The parenthetical is an observation of live.working-animation-repair-01.review.verdict.1.",
            "wrap jump: whole asset (requirement); near-hold: expert clause; parenthetical: example",
            [SP_V_REPAIR, AP_W_ANIM, SP_CT_WORKING],
        ),
    ],
    "proposed_check": (
        "Play the actual four frames at 100 ms per frame including the fourth-to-first wrap, at 1x and 3x on #172336: the loop must read as one continuous, evenly paced "
        "activity cycle with no visible jump at the wrap (required outcome: BRIEF four-frame 100 ms loop; contract loop-boundary review). Expert quality clauses binding "
        "through family.working.contract for this Working asset: stable centre/anchor and stable visual volume across phases. Construction-scoped clauses for the "
        "seed-rotation construction only: stable cluster count (three components per cell) and stepped quarter-turn phases with no morphing or near-hold. The rejected AI "
        "animation (live.working-animation-repair-01.review.verdict.1: morph/near-hold across phases 2/3, jump at wrap) is the failure class, not the definition of the rule."
    ),
    "proposed_domain": "visual",
    "proposed_mode": "visual",
    "change": "clarify",
    "change_explanation": (
        "Old: one undifferentiated rule. New: the required outcome (continuous, evenly paced loop, seamless wrap) is stated first; anchor/volume stability are labelled "
        "expert clauses bound through the adopted contract; cluster-count stability and 'no morphing/near-hold' are explicitly scoped to the seed-rotation construction so a "
        "brief-conforming alternative construction is judged on coherence, not on this recipe. No clause deleted; nothing promoted to owner authority."
    ),
    "discriminating_alternative": (
        "A four-frame pulse in which a dot grows into a ring and back (cluster count and visible volume vary; frames 2 and 4 similar by design) that plays as one coherent "
        "activity loop with a seamless wrap: satisfies BRIEF line 3; the literal 'stable cluster count and volume ... no morphing' rejects it. (Tests the construction-scoped clauses.)"
    ),
}

analysis["authoring-01.working.q.style-coherence"] = {
    "clauses": STYLE_CLAUSES(True),
    "proposed_check": STYLE_PROPOSED(True),
    "proposed_domain": "visual",
    "proposed_mode": "visual",
    "change": "clarify",
    "change_explanation": "Old: 'deliberate coherent clusters and stepped edges' unqualified. New: same outcome, with the explicit note that selective intentional anti-aliasing is permitted (al=full contract; specialist assessment) and accidental blur/noise is not. Other clauses unchanged.",
    "discriminating_alternative": STYLE_ALT,
}

analysis["authoring-01.working.q.consumers"] = {
    "clauses": [
        clause(
            "Exercise started -> running through stateAfter",
            "requirement",
            "src/queue.ts stateAfter maps started to running; authoring-plar consumers rows.",
            "whole Working asset (integration)",
            [QS_AFTER, AP_W_CONSUMERS, VM_SELECT],
        ),
        clause(
            "and both statusCell and compactStatus with assets/working.png in the actual consumer renderer",
            "requirement",
            "Both consumers return the same descriptor (src/queue-view.ts lines 10-11); path from statusVisuals.running. " + ROUTE_FIXTURE,
            "whole Working asset (integration); route clarified",
            [QV_CONSUMERS, QV_RUNNING, SP_CH_DEST, RS_RENDER, VM_FETCH],
        ),
        clause(
            "label Working, frames 4",
            "requirement",
            "statusVisuals.running (consumer code); the fixture writes descriptor.label into the cell.",
            "whole Working asset",
            [QV_RUNNING, VM_LABEL],
        ),
        clause(
            "nearest sampling at scale 1 and 3",
            "requirement",
            "display.filter nearest and scale 3 (consumer code); BRIEF 1x/3x; fixture imageSmoothingEnabled false and image-rendering pixelated. " + SCALE_FACT,
            "whole Working asset; evidence route clarified",
            [QV_DISPLAY, BRIEF_MAIN, VM_SMOOTH, IH_PIXELATED, VM_MATRIX, VM_LIVESCALE],
        ),
        clause(
            "alpha compositing on #172336",
            "requirement",
            "display.background #172336 (consumer code); fixture fills the panel colour then draws the PNG (view.mjs lines 35-36).",
            "whole Working asset",
            [QV_DISPLAY, VM_PANELFILL, VM_PANELVAR],
        ),
        clause(
            "and observed live 100 ms frame advance including the wrap",
            "requirement",
            "100 ms comes from display.frameMs (consumer code) and the advance is frame = floor(elapsed/frameMs) % frames. The literal 'observed live 100 ms frame advance' overstates what the fixture can establish. " + TIMING_FACT,
            "whole Working asset; evidence claim corrected",
            [QV_DISPLAY, VM_FRAME, VM_ANIMATE, VM_TIMELINE, CP_TIMELINE, CP_SCOPE],
        ),
    ],
    "proposed_check": (
        "In the supplied browser fixture (renderer/view.mjs executing the actual src/queue.ts and src/queue-view.ts), exercise started -> running through stateAfter: both "
        "statusCell and compactStatus resolve the same descriptor {label Working, path assets/working.png, frames 4}; the live cells (scale 3) and the state-matrix cells "
        "(scale 1 and 3) render assets/working.png with imageSmoothingEnabled false / image-rendering pixelated, composited over #172336, geometryMatches true. Frame advance "
        "evidence: the capture timeline must report frame indices 0,0,1,1,2,2,3,3,0 at elapsed 0,99,100,199,200,299,300,399,400 ms (floor(elapsed/100) mod 4; wrap at 400 ms) "
        "and the live requestAnimationFrame loop must be observed cycling through all four frames; wall-clock frame duration is not measured by this fixture and is not claimed."
    ),
    "proposed_domain": "engine",
    "proposed_mode": "live",
    "change": "clarify",
    "change_explanation": (
        "Old: 'observed live 100 ms frame advance including the wrap' and 'nearest sampling at scale 1 and 3' under stateAfter. New: states what the fixture actually "
        "evidences (deterministic timeline frame indices incl. the 400 ms wrap, plus visually observed cycling) and that live stateAfter cells are 3x while 1x/3x come from "
        "the state matrix; 'actual consumer renderer' named as the fixture. No behavior asserted that the code lacks."
    ),
    "discriminating_alternative": (
        "An evidence alternative rather than an art alternative: a run that captures only the live 3x cells after clicking Start and never renders the 1x matrix would pass a "
        "loose reading of the old text; the clarified text requires both routes. A correct 64x16 strip of poor art passes this criterion in either form, confirming it "
        "establishes mapping/behavior only, not quality."
    ),
}

analysis["authoring-01.retry.q.geometry"] = {
    "clauses": [
        clause(
            "Decode the delivered PNG as exactly one static 16x16 frame",
            "requirement",
            "BRIEF line 3: status cells 16x16, 'Ready and Retry are static images'; statusVisuals.failed frames 1; fixture draws only a 16x16 image for frames 1.",
            "whole Retry asset",
            [BRIEF_MAIN, QV_FAILED, VM_GEOM, AP_R_GEOM],
        ),
        clause(
            "no strip, animation or extra canvas",
            "requirement",
            "Same sources; a strip or extra canvas fails the fixture geometry condition ('Wrong sheet size'); animation contradicts 'static'.",
            "whole Retry asset",
            [BRIEF_MAIN, VM_GEOMMATCH],
        ),
    ],
    "proposed_check": criteria_by_id["authoring-01.retry.q.geometry"]["check"],
    "proposed_domain": "mechanical",
    "proposed_mode": "local",
    "change": "keep",
    "change_explanation": "No change: every clause is an owner/consumer requirement with a mechanical route.",
    "discriminating_alternative": "A 32x16 two-frame 'blink' Retry: rejected by the literal check and by the sources (brief: Retry is static; consumer frames 1; fixture refuses the sheet size). No brief-conforming alternative is excluded.",
}

analysis["authoring-01.retry.q.transparent-exterior"] = {
    "clauses": transparent_entry("retry", "mark", None, [], [AP_R_BG]),
    "proposed_check": (
        "Split into a measured part and a visual part. Measured (mechanical/local): retain the alpha histogram and exact RGBA component boxes; no alpha>0 region may reach all "
        "four cell edges or fill the cell (canvas matte); RGB of alpha-0 pixels is not significant. Visual (visual/visual): at 1x and 3x on #172336 the exterior shows the panel "
        "with no unintended matte, halo or fringe; a deliberate opaque backing shape is acceptable only when it is part of the mark's recorded design and the exterior stays "
        "transparent. Partial alpha on mark pixels is permitted; binary alpha is not required."
    ),
    "proposed_domain": "visual (if kept as one record); otherwise mechanical + visual",
    "proposed_mode": "visual (if kept as one record); otherwise local + visual",
    "change": "correct",
    "change_explanation": "Old: mechanical/local rule deciding what is 'outside the mark' and prohibiting any 'plate'. New: measurement kept mechanical, mark/matte/plate judgment routed to visual review; blanket 'no plate' narrowed to unintended matte so a deliberate recorded backing is not rejected.",
    "discriminating_alternative": TRANSPARENT_ALT,
}

analysis["authoring-01.retry.q.retry-meaning-without-color"] = {
    "clauses": [
        clause("Viewed at 1x and 3x nearest on #172336", "requirement", "BRIEF line 3 inspection conditions.", "whole Retry asset", [BRIEF_MAIN, QV_DISPLAY]),
        clause(
            "in color and in grayscale",
            "proposal",
            "Grayscale conversion is the specialist's chosen method for testing 'without color alone' (authoring-plar delivery checks and assessment future_work are specialist-authored). Any equivalent non-colour comparison (e.g. binarized silhouettes) satisfies the brief.",
            "method",
            [AP_R_CHECKS, SA_FUTURE, BRIEF_MAIN],
        ),
        clause(
            "the mark reads as failed work / retry",
            "requirement",
            "BRIEF line 3 'Error/retry'; BRIEF line 7 'its purpose is unchanged'; statusVisuals.failed label 'Retry'; authoring-plar purpose and state_meaning.",
            "whole Retry asset",
            [BRIEF_MAIN, BRIEF_PAUSED, QV_FAILED, AP_R_PURPOSE, AP_R_MEANING],
        ),
        clause(
            "and is identifiable by shape alone against Ready, every Working frame, Paused and the preserved Start triangle",
            "requirement",
            "BRIEF line 3 'distinguishable without color alone'; BRIEF line 7 Paused distinct from retry (mutual); BRIEF line 3 preserved Start control.",
            "whole Retry asset",
            [BRIEF_MAIN, BRIEF_PAUSED, SA_START],
        ),
        clause(
            "it must not be confusable with the Working activity loop",
            "observation",
            "Restates the previous clause for one member; its origin is the retry_motif PROPOSAL ('avoid a shape that could be confused with the Working activity loop'). It adds no new restriction beyond 'identifiable by shape alone against every Working frame'; kept as emphasis.",
            "whole Retry asset (redundant emphasis)",
            [AP_R_MOTIF],
        ),
    ],
    "proposed_check": (
        "Viewed at 1x and 3x nearest on #172336 in colour and in a non-colour comparison (grayscale or binarized silhouettes), the mark reads as failed work with a retry "
        "action and is identifiable by shape alone against Ready, every Working frame, Paused and the preserved Start triangle; in particular it must not be confusable with "
        "the Working activity loop. No specific retry motif (such as an arrow) is required."
    ),
    "proposed_domain": "visual",
    "proposed_mode": "visual",
    "change": "clarify",
    "change_explanation": "Old: 'in color and in grayscale' as the sole method. New: grayscale named as one acceptable non-colour comparison; the required outcomes are unchanged; an explicit note that no arrow motif is required (the motif is a PLAR proposal).",
    "discriminating_alternative": (
        "An exclamation mark inside an open circle, with no arrow: distinguishable without colour from the check, the orbiting segments, pause bars and the Start triangle, so "
        "BRIEF lines 3 and 7 hold; the criterion accepts it, confirming it does not impose the proposed arrow. Method alternative: judging by binarized silhouette overlay "
        "instead of grayscale conversion satisfies the brief; the literal 'in grayscale' is a method, which the clarified text makes explicit."
    ),
}

analysis["authoring-01.retry.q.style-coherence"] = {
    "clauses": STYLE_CLAUSES(False),
    "proposed_check": STYLE_PROPOSED(False),
    "proposed_domain": "visual",
    "proposed_mode": "visual",
    "change": "clarify",
    "change_explanation": "Same clarification as the Working style criterion: selective intentional anti-aliasing permitted under al=full; otherwise unchanged.",
    "discriminating_alternative": STYLE_ALT,
}

analysis["authoring-01.retry.q.consumers"] = {
    "clauses": [
        clause("Exercise error -> failed through stateAfter", "requirement", "src/queue.ts stateAfter maps error to failed.", "integration", [QS_AFTER, VM_SELECT]),
        clause(
            "and both statusCell and compactStatus in the actual consumer renderer",
            "requirement",
            "Both consumers return the same descriptor. " + ROUTE_FIXTURE,
            "integration; route clarified",
            [QV_CONSUMERS, SP_CH_DEST, RS_RENDER],
        ),
        clause(
            "label Retry, frames 1, path assets/error-retry.png (not the superseded assets/retry.png)",
            "requirement",
            "statusVisuals.failed (consumer code); BRIEF line 7 'The failure visual moved to the path in the updated view'; authoring-plar destination_update observation and delivery check.",
            "whole Retry asset",
            [QV_FAILED, BRIEF_PAUSED, AP_R_DEST, AP_R_CHECKS],
        ),
        clause(
            "nearest sampling at scale 1 and 3, alpha compositing on #172336",
            "requirement",
            "display constants (consumer code); fixture smoothing/pixelated and panel fill. " + SCALE_FACT,
            "integration; evidence route clarified",
            [QV_DISPLAY, VM_SMOOTH, IH_PIXELATED, VM_PANELFILL, VM_MATRIX, VM_LIVESCALE],
        ),
        clause(
            "static behavior",
            "requirement",
            "frames 1: the fixture's animate loop only repaints descriptors with frames > 1 (view.mjs line 92) and the timeline skips frames <= 1 (line 110); static behavior is established by code and by a single painted frame.",
            "whole Retry asset",
            [VM_ANIMATE, VM_TIMELINE_STATIC, QV_FAILED],
        ),
    ],
    "proposed_check": (
        "In the supplied browser fixture (renderer/view.mjs executing the actual src/queue.ts and src/queue-view.ts), exercise error -> failed through stateAfter: both "
        "statusCell and compactStatus resolve {label Retry, path assets/error-retry.png (not the superseded assets/retry.png), frames 1}; the live cells (scale 3) and the "
        "state-matrix cells (scale 1 and 3) render the PNG with imageSmoothingEnabled false / image-rendering pixelated over #172336, geometryMatches true, and no animation "
        "loop runs for the descriptor (frames 1)."
    ),
    "proposed_domain": "engine",
    "proposed_mode": "live",
    "change": "clarify",
    "change_explanation": "Old: 'actual consumer renderer', 'scale 1 and 3' under stateAfter. New: fixture named; live-cells-at-3x vs matrix-at-1x/3x stated; 'static behavior' tied to the fixture's frames>1 gate. Requirements unchanged.",
    "discriminating_alternative": "A correct Retry PNG delivered to assets/retry.png: fails because statusVisuals.failed resolves assets/error-retry.png (queue-view.ts line 7; BRIEF line 7) - source-supported rejection. The old path alternative is exactly what the clause is meant to exclude.",
}

analysis["authoring-01.paused.q.geometry"] = {
    "clauses": [
        clause(
            "Decode the delivered PNG as exactly one static 16x16 frame",
            "requirement",
            "BRIEF line 7 (paused status image; keep existing display requirements) with line 3 16x16 cells; statusVisuals.paused frames 1; fixture geometry gate.",
            "whole Paused asset",
            [BRIEF_PAUSED, BRIEF_MAIN, QV_PAUSED, VM_GEOM, AP_P_GEOM],
        ),
        clause("no strip, animation or extra canvas", "requirement", "Same sources; fixture refuses other sizes ('Wrong sheet size').", "whole Paused asset", [VM_GEOMMATCH, QV_PAUSED]),
    ],
    "proposed_check": criteria_by_id["authoring-01.paused.q.geometry"]["check"],
    "proposed_domain": "mechanical",
    "proposed_mode": "local",
    "change": "keep",
    "change_explanation": "No change: owner/consumer requirement with a mechanical route.",
    "discriminating_alternative": "A 32x16 two-frame blinking Paused icon: rejected by the literal check and by the consumer descriptor (frames 1); no brief-conforming alternative is excluded.",
}

analysis["authoring-01.paused.q.transparent-exterior"] = {
    "clauses": transparent_entry(
        "paused",
        "mark",
        "(the rejected opaque magenta intermediate is this failure class)",
        [SP_V_PAUSED02],
        [AP_P_BG],
    ),
    "proposed_check": (
        "Split into a measured part and a visual part. Measured (mechanical/local): retain the alpha histogram and exact RGBA component boxes; no alpha>0 region may reach all "
        "four cell edges or fill the cell (canvas matte); RGB of alpha-0 pixels is not significant. Visual (visual/visual): at 1x and 3x on #172336 the exterior shows the panel "
        "with no unintended matte, halo or fringe; a deliberate opaque backing shape is acceptable only when it is part of the mark's recorded design and the exterior stays "
        "transparent. The rejected opaque magenta intermediate (live.paused-02.review.verdict.1) is the failure class. Partial alpha on mark pixels is permitted; binary alpha is not required."
    ),
    "proposed_domain": "visual (if kept as one record); otherwise mechanical + visual",
    "proposed_mode": "visual (if kept as one record); otherwise local + visual",
    "change": "correct",
    "change_explanation": "Same correction as the Working/Retry transparent-exterior criteria: measurement stays mechanical, matte/plate judgment routed to visual review, 'no plate' narrowed to unintended matte; failure example retained as an example.",
    "discriminating_alternative": TRANSPARENT_ALT,
}

analysis["authoring-01.paused.q.pause-meaning-without-color"] = {
    "clauses": [
        clause("Viewed at 1x and 3x nearest on #172336", "requirement", "BRIEF line 3 inspection conditions (kept by line 7).", "whole Paused asset", [BRIEF_MAIN, BRIEF_PAUSED]),
        clause(
            "in color and in grayscale",
            "proposal",
            "Specialist method for 'without relying on color alone'; equivalent non-colour comparisons satisfy the brief.",
            "method",
            [AP_P_CHECKS, SA_FUTURE],
        ),
        clause(
            "the mark reads as paused work",
            "requirement",
            "BRIEF line 7 paused state status image; statusVisuals.paused label 'Paused'; authoring-plar purpose.",
            "whole Paused asset",
            [BRIEF_PAUSED, QV_PAUSED, AP_P_PURPOSE],
        ),
        clause(
            "and is identifiable by shape alone against Ready (completion), every Working frame (activity), Retry and the preserved Start triangle",
            "requirement",
            "BRIEF line 7: distinguishable from activity, completion and retry without relying on color alone; Start preserved (line 3). No pause-bar motif is required (authoring-plar paused_motif is a proposal).",
            "whole Paused asset",
            [BRIEF_PAUSED, BRIEF_MAIN, AP_P_DIST, AP_P_MOTIF],
        ),
    ],
    "proposed_check": (
        "Viewed at 1x and 3x nearest on #172336 in colour and in a non-colour comparison (grayscale or binarized silhouettes), the mark reads as paused work and is "
        "identifiable by shape alone against Ready (completion), every Working frame (activity), Retry and the preserved Start triangle. No specific pause motif (such as "
        "paired bars) is required."
    ),
    "proposed_domain": "visual",
    "proposed_mode": "visual",
    "change": "clarify",
    "change_explanation": "Old: grayscale as the sole method. New: grayscale named as one acceptable non-colour comparison; explicit note that the pause-bar motif is a proposal. Required outcomes unchanged.",
    "discriminating_alternative": "A Paused mark drawn as a single square inside a thin ring (no bars): distinct from check, orbit segments, retry mark and triangle without colour, satisfying BRIEF line 7; the criterion accepts it, confirming it does not impose the proposed pause bars.",
}

analysis["authoring-01.paused.q.style-coherence"] = {
    "clauses": STYLE_CLAUSES(False),
    "proposed_check": STYLE_PROPOSED(False),
    "proposed_domain": "visual",
    "proposed_mode": "visual",
    "change": "clarify",
    "change_explanation": "Same clarification as the Working style criterion: selective intentional anti-aliasing permitted under al=full; otherwise unchanged.",
    "discriminating_alternative": STYLE_ALT,
}

analysis["authoring-01.paused.q.consumers"] = {
    "clauses": [
        clause("Exercise pause -> paused through stateAfter", "requirement", "src/queue.ts stateAfter maps pause to paused; QueueState includes paused.", "integration", [QS_AFTER, QS_STATE, VM_SELECT]),
        clause(
            "and both statusCell and compactStatus in the actual consumer renderer",
            "requirement",
            "Both consumers return the same descriptor. " + ROUTE_FIXTURE,
            "integration; route clarified",
            [QV_CONSUMERS, SP_CH_DEST, RS_RENDER],
        ),
        clause("label Paused, frames 1, path assets/paused.png", "requirement", "statusVisuals.paused (consumer code); BRIEF line 5 paths already used by the view.", "whole Paused asset", [QV_PAUSED, BRIEF_PATHS]),
        clause(
            "nearest sampling at scale 1 and 3, alpha compositing on #172336",
            "requirement",
            "display constants; fixture smoothing/pixelated and panel fill. " + SCALE_FACT,
            "integration; evidence route clarified",
            [QV_DISPLAY, VM_SMOOTH, IH_PIXELATED, VM_PANELFILL, VM_MATRIX, VM_LIVESCALE],
        ),
        clause("static behavior", "requirement", "frames 1: the fixture animates only frames > 1 and the timeline skips frames <= 1.", "whole Paused asset", [VM_ANIMATE, VM_TIMELINE_STATIC, QV_PAUSED]),
    ],
    "proposed_check": (
        "In the supplied browser fixture (renderer/view.mjs executing the actual src/queue.ts and src/queue-view.ts), exercise pause -> paused through stateAfter: both "
        "statusCell and compactStatus resolve {label Paused, path assets/paused.png, frames 1}; the live cells (scale 3) and the state-matrix cells (scale 1 and 3) render the "
        "PNG with imageSmoothingEnabled false / image-rendering pixelated over #172336, geometryMatches true, and no animation loop runs for the descriptor (frames 1)."
    ),
    "proposed_domain": "engine",
    "proposed_mode": "live",
    "change": "clarify",
    "change_explanation": "Same clarification as the Retry consumers criterion: fixture named, scale routes stated, static behavior tied to the frames>1 gate. Requirements unchanged.",
    "discriminating_alternative": "A Paused PNG placed at assets/pause.png: fails because statusVisuals.paused resolves assets/paused.png - source-supported rejection; a correct file of poor art passes, confirming this criterion establishes mapping only.",
}

analysis["authoring-01.delivery.q.continuity"] = {
    "clauses": [
        clause(
            "Compare all four actual members together at 1x and 3x nearest on #172336 against the exact Ready baseline",
            "requirement",
            "BRIEF line 3 'coherent pixel-art status assets' and inspection conditions; adopted scoped baseline render.decision.style / render.choice.style; RENDER-STAGE family review guidance.",
            "collective delivery (Ready, Working, Retry, Paused)",
            [BRIEF_MAIN, SP_DEC_STYLE, SP_CH_STYLE, RS_FAMILY],
        ),
        clause(
            "coherent deliberate pixel treatment, readable visual weight, perceptible cool-blue accent and transparent exteriors",
            "requirement",
            "BRIEF line 3 (coherent, readable, cool-blue accent, transparent); adopted style carry list. 'Readable visual weight' is ambiguous: it means comparable, not identical, weight; stroke width is explicitly not fixed.",
            "collective delivery; wording clarified",
            [BRIEF_MAIN, CC_CARRY, CC_NOTP],
        ),
        clause(
            "including Working's four frames and its actual 100 ms playback with the wrap",
            "requirement",
            "BRIEF line 3 four frames / 100 ms; the caller comparison notes that absent Working gave no playback evidence, so the collective review must include it.",
            "collective delivery",
            [BRIEF_MAIN, CC_ABSENT, FJ_LIMITS],
        ),
        clause(
            "no exact palette, alpha, stroke, margin or copied completion-motif requirement",
            "observation",
            "Explicit non-restriction (render.choice.style not_fixed; assessment 'do not carry completion check motif'; AUTHORING-STAGE lines 11-14).",
            "collective delivery",
            [SP_CH_STYLE, SA_STYLE, AS_QUAL],
        ),
    ],
    "proposed_check": (
        "Compare all four actual members together at 1x and 3x nearest on #172336 against the exact Ready baseline: coherent deliberate pixel treatment, comparable (not "
        "identical) visual weight, perceptible cool-blue accent and transparent exteriors, including Working's four frames and its actual 100 ms playback with the wrap; no "
        "exact palette, alpha, stroke, margin or copied completion-motif requirement."
    ),
    "proposed_domain": "continuity",
    "proposed_mode": "visual",
    "change": "clarify",
    "change_explanation": "Old: 'readable visual weight'. New: 'comparable (not identical) visual weight' so equal stroke width is not implied (stroke is explicitly not fixed). Otherwise unchanged.",
    "discriminating_alternative": "A Retry mark drawn with 1-px strokes beside Ready's 2-px-reading strokes but equally readable at 1x/3x: coherent and brief-conforming; 'readable visual weight' could be read as requiring equal weight and reject it; the clarified wording asks for comparable weight judged visually.",
}

analysis["authoring-01.delivery.q.distinction"] = {
    "clauses": [
        clause(
            "View Ready, every Working frame and the running loop, Retry and Paused together at 1x and 3x",
            "requirement",
            "BRIEF lines 3 and 7 distinction requirements with the 1x/3x inspection conditions; RENDER-STAGE family review.",
            "collective delivery",
            [BRIEF_MAIN, BRIEF_PAUSED, RS_FAMILY],
        ),
        clause(
            "including a grayscale/non-color comparison",
            "proposal",
            "Method for 'without color alone'; already phrased as 'grayscale/non-color', so equivalent methods are admitted. Keep.",
            "method",
            [AP_W_CHECKS, SA_FUTURE],
        ),
        clause(
            "Working never reads as success",
            "requirement",
            "BRIEF line 3.",
            "collective delivery",
            [BRIEF_MAIN],
        ),
        clause(
            "and Retry and Paused are each distinct from activity, completion and from each other by shape or structure alone",
            "requirement",
            "BRIEF line 3 (error/retry without color alone) and line 7 (paused distinct from activity, completion and retry).",
            "collective delivery",
            [BRIEF_MAIN, BRIEF_PAUSED],
        ),
        clause(
            "the preserved Start triangle remains separately identifiable",
            "requirement",
            "BRIEF line 3 preserve the existing vector Start control; statusVisuals.idle; assessment of Start as a distinct triangle.",
            "collective delivery",
            [BRIEF_MAIN, QV_IDLE, SA_START],
        ),
    ],
    "proposed_check": criteria_by_id["authoring-01.delivery.q.distinction"]["check"],
    "proposed_domain": "continuity",
    "proposed_mode": "visual",
    "change": "keep",
    "change_explanation": "No change: every clause is an owner requirement and the method clause already admits any non-colour comparison; visual route is correct.",
    "discriminating_alternative": "Retry and Paused marks that differ only in hue (same silhouette): satisfies colour-based readability but fails 'by shape or structure alone' - rejection supported by BRIEF lines 3 and 7. No brief-conforming alternative is excluded.",
}

analysis["authoring-01.delivery.q.destination"] = {
    "clauses": [
        clause(
            "Exercise all backend transitions (started, ok, error, pause, plus idle) through both statusCell and compactStatus",
            "requirement",
            "src/queue.ts stateAfter results; fixture event list; both consumers (consumer code).",
            "collective delivery (integration)",
            [QS_AFTER, VM_EVENTS, QV_CONSUMERS],
        ),
        clause(
            "with the exact retained package files at the confirmed destination paths",
            "requirement",
            "BRIEF line 5 'Assets belong at the paths already used by the view'; statusVisuals paths; render.choice.destination paths.",
            "collective delivery",
            [BRIEF_PATHS, QV_ALL, SP_CH_DEST],
        ),
        clause(
            "labels, frame counts, horizontal slicing, 100 ms timing, nearest sampling at scale 1 and 3, alpha compositing on #172336",
            "requirement",
            "Consumer code (statusVisuals, display) and fixture behavior. " + ROUTE_FIXTURE + " " + TIMING_FACT,
            "collective delivery; evidence route clarified",
            [QV_ALL, QV_DISPLAY, VM_PAINT, VM_FRAME, VM_SMOOTH, VM_PANELFILL, CP_TIMELINE, CP_SCOPE],
        ),
        clause(
            "and recorded integer placement against the screenshot",
            "proposal",
            "Adopted destination-check method from the recheck stage (recheck.decision.destination; findings 'integer placement/screenshot correspondence'; check.py bounds/pixel comparison). It tests the capture environment and compositing, not the art; scoped as the established method for destination acceptance.",
            "method adopted for destination acceptance in this consumer",
            [SP_DEC_DEST, FJ_OUTCOME, CP_BOUNDS, VM_VIEWS],
        ),
        clause(
            "assets/start.svg byte hash unchanged",
            "requirement",
            "BRIEF line 3 'Preserve the existing vector Start control'; authoring-plar queue.start delivery check.",
            "collective delivery",
            [BRIEF_MAIN, AP_START_CHECKS],
        ),
    ],
    "proposed_check": (
        "In the supplied browser fixture (renderer/view.mjs executing the actual src/queue.ts and src/queue-view.ts), exercise all backend transitions (started, ok, error, "
        "pause, plus idle) through both statusCell and compactStatus with the exact retained package files at the confirmed destination paths: labels, frame counts, horizontal "
        "slicing, frame index floor(elapsed/100) mod frames at the timeline sample points including the 400 ms wrap (wall-clock duration not measured), nearest sampling at scale "
        "1 (state matrix) and 3 (state matrix and live cells), alpha compositing on #172336, and - as the adopted destination-check method - recorded integer canvas placement "
        "matching the screenshot pixels; assets/start.svg byte hash unchanged."
    ),
    "proposed_domain": "engine",
    "proposed_mode": "live",
    "change": "clarify",
    "change_explanation": "Old: '100 ms timing' and 'nearest sampling at scale 1 and 3' without evidence route; placement check unlabelled. New: fixture named, timing evidence bounded to timeline frame indices, scale routes stated, integer-placement labelled as the adopted method. Requirements unchanged.",
    "discriminating_alternative": "A capture run in a zoomed page producing fractional canvas bounds: the art and mapping are identical, yet the integer-placement clause fails it - which shows that clause tests the capture method/environment, hence its 'method' scope. A package with Retry at the superseded assets/retry.png fails on paths with source support (queue-view.ts line 7).",
}

if citation_failures:
    raise SystemExit("\n".join(citation_failures))
if set(analysis) != set(criteria_by_id):
    raise SystemExit("analysis does not cover exactly the 20 report criteria")

# ------------------------------------------------------ assemble criteria ----
criteria_out = []
for cid in report["criterion_ids"]:
    rep = criteria_by_id[cid]
    a = analysis[cid]
    for cl in a["clauses"]:
        for key in ("text", "authority", "basis", "scope", "source"):
            if key not in cl:
                raise SystemExit(f"clause missing {key} in {cid}")
        if cl["authority"] not in {"requirement", "proposal", "observation", "unknown"}:
            raise SystemExit(f"bad authority in {cid}")
        if not cl["source"]:
            raise SystemExit(f"clause without source in {cid}")
    if a["change"] == "keep" and a["proposed_check"] != rep["check"]:
        raise SystemExit(f"keep with changed text: {cid}")
    criteria_out.append(
        {
            "criterion": cid,
            "record_sha256": rep["record_sha256"],
            "stage": rep["stage"],
            "output": rep["output"],
            "original_check": rep["check"],
            "original_domain": rep["domain"],
            "original_mode": rep["mode"],
            "original_sources": rep["sources"],
            "clauses": a["clauses"],
            "proposed_check": a["proposed_check"],
            "proposed_domain": a["proposed_domain"],
            "proposed_mode": a["proposed_mode"],
            "change": a["change"],
            "change_explanation": a["change_explanation"],
            "discriminating_alternative": a["discriminating_alternative"],
        }
    )

# -------------------------------------------------------------- sources ----
def src(rel, role):
    return {"path": rel, "sha256": sha256(ROOT / rel), "role": role}


sources = [
    src("BRIEF.md", "owner brief (render.source.brief); lines 3, 5, 7, 9"),
    src("src/queue-view.ts", "consumer descriptors and display constants (render.source.view)"),
    src("src/queue.ts", "backend transitions stateAfter (retained copy is r.22e90a2a03fe453a.source.4, same hash)"),
    src("renderer/view.mjs", "supplied browser fixture: slicing, sampling, compositing, frame advance, capture timeline"),
    src("renderer/index.html", "fixture page: image-rendering pixelated; no reduced-motion media query"),
    src("renderer/check.py", "fixture checker: bounds/pixel comparison and timeline frame-index check; scope statement"),
    src("authoring-plar.txt", "current PLAR for the authoring branch: queue.working (lines 420-675), queue.retry (676-907), queue.start (908-1001), queue.paused (1003-1224) with authority labels"),
    src("plar.txt", "original accepted-production PLAR (unchanged; historical)"),
    src("AUTHORING-STAGE.md", "authoring assignment: qualitative-preservation and assembly-policy obligations"),
    src("AUTHORING-UPDATE.md", "caller reduced-motion update (scoped to the authoring branch)"),
    src("AUTHORING-REVIEW.md", "this review-repair assignment"),
    src("AUTHORING-RESULT.json", "historical caller result: identities, consumer comparison, transparent-RGB note, rotation recomputation"),
    src("RENDER-STAGE.md", "render.source.assignment: style-decision authorization and renderer instructions"),
    src("work/family-render-review/caller-comparison-final.json", "render.source.caller: adopted style decision, carry/not-prescribed lists"),
    src("work/family-render-review/specialist-assessment.json", "render.source.assessment: corrected criteria review, Start control, family inventory"),
    src("work/pixl-render-recheck-01/findings.json", "recheck.source.findings: destination check outcome and limitations"),
    src(".pixl/assets/queue.ready/state.px", "store revision 88: contracts (lines 47, 56, 62, 223), verdicts (183, 258, 320), choices (391, 392), decisions (386, 393), Q records (lines 4-6, 9-13, 18-22, 27-33)"),
    src("work/authoring-01/working-rotation-policy.json", "specialist frame-selection/assembly policy for the two-step construction"),
    src("work/authoring-01/specialist-report.json", "prior specialist report for the authoring stage (historical)"),
    src("official-discovery.json", "retained official PixelLab workbench declaration (join/edit/patch_pixels)"),
    src(JOB, "durable job authoring-01.working.join-01 (historical, unchanged)"),
    src(PACKET, "retained stage-request packet (historical, unchanged)"),
    src(PLAN, "retained connected-plan snapshot authoring-01 (historical, unchanged)"),
    src("work/criteria-review-01/request-review.json", "caller's retained pixl_request_review report; the 20 criterion identities and texts were copied from it verbatim"),
    src("work/criteria-review-01/request-review-raw.txt", "raw tool bytes of the same report"),
    src(SEED_ART, "accepted Working seed live.working-seed.candidate (measured)"),
    src(MOTION_ART, "accepted original-production motion strip (measured; provenance for the rotation direction)"),
    src("assets/start.svg", "preserved Start control (byte hash must stay unchanged)"),
    src("assets/ready-confirmed.png", "exact Ready baseline ready.retained"),
]

# -------------------------------------------------------------- choices ----
choices = [
    {
        "id": "seed-rotation-two-step-construction",
        "choice": "Working strip built deterministically from the accepted seed: workbench `join` of four exact seed copies into a 64x16 sheet (job authoring-01.working.join-01), then a separate guarded `patch_pixels` edit rotating cells 2-4 by 90/180/270 degrees clockwise about (7.5,7.5) via dst(x,y)=src(y,15-x).",
        "appears_in": [RR_REQUEST, RR_NOTES, RP_STEP1, RP_STEP2, JOB_PTR, PACKET_PTR],
        "reason": "Reproduces the accepted motion (visible-pixel diff 0 per cell; counter-clockwise differs), guarantees anchor/volume stability and uniform angular velocity by construction, uses no paid generation, and carries fresh seed bytes as data URLs. It is an expert construction choice, not an owner requirement; the brief leaves the activity motif open (authoring-plar motion_motif is a proposal).",
        "scope": "authoring-01.working stage; revisable without changing the brief",
    },
    {
        "id": "failure-classes-as-examples",
        "choice": "Citing retained failures inside criteria: 193 opaque #808080 background pixels (live.working-animation-01.review.verdict.1), morph/near-hold/wrap jump (live.working-animation-repair-01.review.verdict.1), opaque magenta intermediate (live.paused-02.review.verdict.1).",
        "appears_in": [SP_V_ANIM01, SP_V_REPAIR, SP_V_PAUSED02],
        "reason": "Concrete anchors for reviewers. They are observations illustrating the failure class, not the definition of the rule; the proposal labels them as examples.",
        "scope": "examples only",
    },
    {
        "id": "no-gutters-padding-expectation",
        "choice": "Expectation that the join result is exactly 64x16 with cells at x=0,16,32,48 and no gutters/padding.",
        "appears_in": [RP_STEP1, RR_NOTES],
        "reason": "The fixture draws only when width == 16*frames; the requirement is consumer-code-derived. 'Padding' is clarified to mean added canvas, not in-cell transparent margin.",
        "scope": "mechanical geometry; whole Working asset",
    },
    {
        "id": "grayscale-comparison-method",
        "choice": "Grayscale conversion as the method for judging 'without color alone'.",
        "appears_in": [AP_R_CHECKS, AP_P_CHECKS, AP_W_CHECKS, SA_FUTURE],
        "reason": "Simple, reproducible proxy for colour-blind/non-colour reading. Equivalent non-colour comparisons (binarized silhouettes, side-by-side masks) satisfy the brief; the proposal names grayscale as one acceptable method.",
        "scope": "method",
    },
    {
        "id": "ready-baseline-comparison-context",
        "choice": "Reviewing every member beside the exact Ready baseline at 1x and 3x on #172336.",
        "appears_in": [SP_CH_STYLE, SP_DEC_STYLE, CC_SCOPE],
        "reason": "The adopted scoped style decision (caller, authorized by RENDER-STAGE) makes ready.retained the family baseline; 1x/3x on the panel is the brief's inspection condition. The baseline comparison is the method; coherence is the required outcome.",
        "scope": "this consumer status family",
    },
    {
        "id": "per-frame-activity-reading",
        "choice": "Requiring each Working frame, not only the loop, to read as activity.",
        "appears_in": [AP_W_MEANING],
        "reason": "Frames display singly for 100 ms, frame 0 is painted at creation (view.mjs line 56) and a stalled animation shows one frame; a frame that forms a check would read as success. Expert extension of BRIEF line 3, kept with rationale.",
        "scope": "whole Working asset (expert clause)",
    },
    {
        "id": "anchor-volume-cluster-stability",
        "choice": "Stable centre/anchor, stable volume (contract clauses) and stable cluster count / stepped quarter-turn phases (construction clauses).",
        "appears_in": [SP_CT_WORKING, RP_OBLIG, RP_PLAY],
        "reason": "Anchor/volume stability are expert quality clauses bound through the adopted family.working.contract; cluster-count stability and 'no morphing/near-hold' follow from the rotation construction (seed measured at 3 components). The proposal scopes the latter to the construction so other coherent constructions are judged on coherence.",
        "scope": "contract clauses: Working asset; construction clauses: seed rotation only",
    },
    {
        "id": "working-needs-seed-only",
        "choice": "Working stage input `needs` is only live.seed.output; Ready baseline bound at task level.",
        "appears_in": [RR_NOTES],
        "reason": "The chosen operation consumes only seed bytes (prior specialist report needs_rationale). A different construction (e.g. new generation styled on Ready) would need the Ready bytes as an explicit input.",
        "scope": "authoring-01 plan",
    },
    {
        "id": "transparent-expected-value-assumption",
        "choice": "Step-2 patch list assumes transparent pixels read as #00000000 after join; to be confirmed with `measure` before step 2.",
        "appears_in": [RP_TRANS, AR_TRANSRGB],
        "reason": "The accepted motion strip shows transparent pixels normalized to RGB 128,128,128, so the workbench may report #80808000; the proposal makes transparent RGB insignificant for 'lossless copy' checks.",
        "scope": "seed rotation construction, step 2",
    },
    {
        "id": "workbench-mode-low",
        "choice": "mode 'low' for the workbench join call.",
        "appears_in": [RR_MODE],
        "reason": "A deterministic join needs no planning narrative; fewer tokens. Revisable.",
        "scope": "prepared request",
    },
    {
        "id": "retain-raw-provider-frames",
        "choice": "Retaining all raw provider outputs beside the assembled strip.",
        "appears_in": [AS_ASSEMBLY, SP_V_ANIM01],
        "reason": "Assignment process requirement and PIXL evidence discipline; lets the caller verify lossless assembly.",
        "scope": "this authoring branch",
    },
]

# ------------------------------------------------------- reduced motion ----
reduced_motion = {
    "note": "Separate from the corrections above. The 20 criteria and job authoring-01.working.join-01 are bound to queue.working requirements_hash e0614bd962a53a19003707f3d73326be436891e198eb1e4a262f12412fbfb027 (normal-motion contract). The current selection hash is 2901c7107d4f162e98653140ea8061dfe213821b22a5e1338d9d2d6de5b4ad0c. This section does not adopt the old request as current and does not declare it dead; it states both identities and the impact.",
    "identities": {
        "bound_in_plan_and_job": "e0614bd962a53a19003707f3d73326be436891e198eb1e4a262f12412fbfb027",
        "current_authoring_plar_selection": "2901c7107d4f162e98653140ea8061dfe213821b22a5e1338d9d2d6de5b4ad0c",
        "job": {"id": "authoring-01.working.join-01", "state": "prepared", "remote_id": None, "next_action": "resolve_context", "blockers": report["request"]["blockers"]},
        "sources": [AR_IDENT, AR_UPDATE, RR_SELECTION, AU_SCOPE],
    },
    "a_current_requirement": {
        "text": "authoring-plar.txt queue.working purpose (line 422): '... the reduced-motion mode must use a stationary Working symbol distinguishable from Ready and Paused. Confirm its consumer mapping before any further generation.' AUTHORING-UPDATE.md lines 2-4 add: 'a stationary Working symbol distinct from Ready and Paused. Its consumer mapping needs comparison with the existing source before a revised request.'",
        "requires": [
            "A stationary (single, non-animated) Working symbol exists for a reduced-motion mode.",
            "It is distinguishable from Ready and from Paused (named explicitly).",
            "Its consumer mapping is confirmed against the existing source before any further generation for queue.working.",
            "The update is additive to this authoring branch: the four-frame 100 ms Working loop of BRIEF line 3 is not withdrawn (AUTHORING-UPDATE.md lines 5-10 say the older plan/request remains retained and must not be removed or rewritten).",
        ],
        "leaves_open": [
            "What 'reduced-motion mode' is: an OS/browser preference (prefers-reduced-motion), an application setting, or a queue state; the source has no such concept.",
            "Where the symbol lives: a separate file (e.g. assets/working-static.png), a designated cell of the existing 64x16 strip held stationary by the renderer, or a separate descriptor key.",
            "Whether distinction from Retry and the preserved Start is also required (the brief's general 'distinguishable without color alone' language suggests yes, but the update names only Ready and Paused).",
            "Whether the symbol must itself read as 'working' when static, or only as 'not ready / not paused'.",
            "Whether both consumers (statusCell, compactStatus) consult the preference identically (the brief's 'both full and compact status cells' purpose implies yes).",
            "Canvas, transparency and review conditions: the update says nothing; BRIEF 16x16 / transparent / 1x-3x conditions would apply by 'Keep the existing style and display requirements' (line 7) if the caller confirms.",
        ],
        "sources": [AP_W_PURPOSE, AU_REQ, AU_SCOPE, BRIEF_MAIN, BRIEF_PAUSED],
    },
    "b_consumer_mapping_facts": {
        "verified": [
            "src/queue-view.ts line 4: a single `running` descriptor {label Working, path assets/working.png, frames 4}; line 9: display has cell, scale, filter, frameMs, background and no motion-preference key; lines 10-11: statusCell and compactStatus take only the state and return statusVisuals[state].",
            "src/queue.ts lines 1-3: QueueState has idle/running/succeeded/failed/paused and stateAfter maps started/ok/error/pause; there is no reduced-motion state, result or preference.",
            "renderer/view.mjs: no matchMedia or prefers-reduced-motion check anywhere (grep over src/*.ts, renderer/*.mjs, renderer/index.html, renderer/check.py for 'reduced', 'prefers-reduced', 'motion' returned no matches); animate() (lines 91-97) always repaints descriptors with frames > 1; the only media query in renderer/index.html (line 27) is a max-width layout rule.",
            "Conclusion: there is no reduced-motion path in the consumer or the fixture today; the requirement currently has no consumer anchor. This confirms AUTHORING-RESULT.json line 124.",
        ],
        "sources": [QV_RUNNING, QV_DISPLAY, QV_CONSUMERS, QS_STATE, QS_AFTER, VM_ANIMATE, IH_MEDIA, AR_CONSUMER],
    },
    "c_impact_on_the_20_criteria": {
        "statement": "None of the 20 criteria is rewritten here; they remain the normal-motion contract bound to e0614bd9. No existing criterion covers the stationary symbol, so the current requirement is uncovered rather than contradicted.",
        "if_mapping_is_renderer_holds_a_strip_cell": [
            "authoring-01.working.q.activity-not-success: its per-frame clause already requires each frame to read as activity; it would additionally need 'the designated stationary cell reads as Working and is distinguishable from Ready and Paused when shown alone' (new clause or new criterion).",
            "authoring-01.working.q.consumers and authoring-01.delivery.q.destination: would need a reduced-motion branch (preference consulted by both consumers; no animate loop; designated cell painted) - behavior the fixture does not have today, so it cannot be checked until the consumer changes.",
            "authoring-01.delivery.q.distinction: would need the stationary symbol added to the compared set.",
            "geometry / frame-assembly / motion-continuity / transparent-exterior / style-coherence: unchanged for the strip.",
        ],
        "if_mapping_is_a_separate_static_file_or_descriptor": [
            "A new output (e.g. queue.working-static) with its own geometry (16x16, 1 frame), transparent-exterior, meaning-without-color (vs Ready and Paused at least), style-coherence and consumers criteria; the delivery collective would gain a member. This requires a new plan id or the explicit revision path (AUTHORING-RESULT.json lines 151-156) - not performed here.",
            "The 20 existing criteria remain as they are for the animated strip.",
        ],
        "job_identity": "authoring-01.working.join-01 stays prepared, undispatched, bound to e0614bd9; its resolution (retain as historical intent, or re-bind if the strip remains required alongside the stationary symbol) is a caller decision under the provider-recovery operation and is not made by this proposal.",
        "sources": [AR_NEXT, AR_IDENT, RR_REQUEST],
    },
    "d_expert_proposals": {
        "label": "PROPOSALS by the specialist, not owner requirements",
        "symbol_options": [
            {
                "option": "P1 - designated stationary cell of the rotation strip (cell 0 = the seed: three separated cool-blue segments orbiting an empty centre; measured 3 components, 32 visible pixels, bbox [3,3,14,14])",
                "assessment": "Reads as the familiar static 'spinner/loading' idiom; clearly distinct from the Ready check and from paired pause bars by structure (ring of separated segments vs two bars vs check). Risk: a static spinner can read as 'stalled' rather than 'working'; the brief's 'activity' is weaker when frozen. Lowest cost: no new art, one renderer rule.",
            },
            {
                "option": "P2 - dedicated static symbol: three horizontal dots (ellipsis) in the family's cool blue, stepped clusters, transparent exterior",
                "assessment": "Conventional 'in progress' static glyph; distinct from check, bars and triangle by count and axis (three small squares in a row vs two tall bars). Needs a new 16x16 asset and either a new descriptor or renderer mapping. Risk: at 1x three 2x2 dots may read as a dashed line; verify at 1x on #172336.",
            },
            {
                "option": "P3 - dedicated static symbol: closed ring with a single gap (a 'C'-like arc) in cool blue",
                "assessment": "Reads as 'in progress / incomplete' and is distinct from check and bars; risk of resembling a retry arrow without its head - must be compared against the delivered Retry mark.",
            },
        ],
        "recommended_default": "P1 if the caller accepts 'static spinner' semantics for reduced motion, because it adds no asset, keeps one source of truth and keeps the consumers' shared descriptor; otherwise P2.",
        "consumer_mapping_options": [
            "M1 - renderer rule: when the preference is active, paint a designated frame (default 0) and skip the animate loop; statusVisuals unchanged (frames stays 4 for geometry gating). Both consumers share it automatically because they return the same descriptor.",
            "M2 - descriptor extension: statusVisuals.running gains a reduced variant {path: 'assets/working-static.png', frames: 1} or a `stationaryFrame` index; statusCell/compactStatus (or the renderer) select it when the preference is active.",
            "M3 - separate state is NOT recommended: reduced motion is a display preference, not a queue state; adding it to QueueState would couple backend transitions to presentation.",
        ],
        "open_decisions_for_owner_caller": [
            "Definition and source of the reduced-motion preference (OS media query vs app setting) and which module consults it.",
            "Symbol option (P1/P2/P3 or other) and whether it must read as 'working' when static.",
            "Mapping option (M1/M2) and the destination path if a new file is chosen; whether frames stays 4 for the strip.",
            "Whether distinction from Retry and Start is also required for the stationary symbol.",
            "Whether the animated strip remains required (default yes per BRIEF line 3 and AUTHORING-UPDATE.md 'remains retained') and therefore whether authoring-01.working.join-01 is kept as the strip's pending intent.",
        ],
        "sources": [SP_CT_SEED, QV_RUNNING, QV_CONSUMERS, VM_ANIMATE, BRIEF_MAIN, BRIEF_PAUSED],
        "measurement_basis": measurements[0],
    },
}

# ------------------------------------------------- historical preservation ----
expected_preserved = {
    PLAN: "b025e867d863f5ad28b47127d3384ea5f191d459573394521504243abd95d826",
    JOB: "d9badc9cf64c04f7adc812f2e245d4af8caf38bb63f102e4304c4e83bed1290d",
    PACKET: "84dcf243f2cd22b69fa7ac906bfc33e7abd55bf113c2cc6db7566cb87bd4b1f8",
    "AUTHORING-RESULT.json": "3724bfa77c0a9af49bbcec6389b3f3b2d3879a49954e3148bdba8321537bdad7",
    "plar.txt": "a462ecf3b6b45c0382d3483b0f4f6912a9d0bd1d68e75253143faa1423837344",
    "authoring-plar.txt": "7c6c54fb55f0cb46fb8f5707468b3776438bd62ab102beafb49c2e91e50e3b41",
    ".pixl/assets/queue.ready/state.px": "3484cf385c91c8c28fa04316fb2c7c5b52c740178b505ccbd88631f57c893c9b",
    "work/criteria-review-01/request-review.json": EXPECTED_REPORT_SHA,
    "work/criteria-review-01/request-review-raw.txt": EXPECTED_RAW_SHA,
    "work/authoring-01/working-rotation-policy.json": "ba4cfb88742bce0c14d3af0534c92f010c19d930267db6959a3ebde96f3e3af2",
    "work/authoring-01/specialist-report.json": "0262c4540b262b09cb30076fd1a8bbd7335944addc3dea835677015eb2fe5686",
    "work/authoring-01/stage-packet.json": "892a94d7e2f7d214c9189e0f8c0ba7bd87b9196a1b1b0418b400874b1b84eeba",
    "work/authoring-01/plan.json": "ede3e0b4d0ddcf183b46ea34524cd37cc2faf8624f4eb9104138df1d292887fb",
    "assets/start.svg": "ee2ba2fe20bd09a2c9a9c96d889f766e8af80fcdf704e8172934135e2b7e12d3",
    "assets/ready-confirmed.png": "fc5e43ae9db53c12cdb419794b36ef09a8ae8cf2be996954ae7390396a268ac5",
}
preserved_files = []
for rel, expected in expected_preserved.items():
    actual = sha256(ROOT / rel)
    if actual != expected:
        raise SystemExit(f"historical file changed: {rel} {actual} != {expected}")
    preserved_files.append({"path": rel, "sha256": actual, "observed": "unchanged (re-hashed at build time; equals the value observed before this review)"})

historical_preservation = {
    "statement": "No existing file was modified. The store (state.px revision 88), PLAR files, plan snapshot, stage-request packet, job and all Q records are untouched; this proposal is a separate artifact beside them.",
    "state": {"path": ".pixl/assets/queue.ready/state.px", "revision": report["state"]["revision"], "sha256": report["state"]["sha256"]},
    "plan": report["plan"],
    "job": {
        "id": report["request"]["id"],
        "file": {"path": JOB, "sha256": expected_preserved[JOB]},
        "intent_sha256": report["request"]["request"]["intent_sha256"] if "intent_sha256" in report["request"]["request"] else report["request"]["intent_sha256"],
        "request_sha256": report["request"]["request"]["request_sha256"],
        "schema_sha256": report["request"]["request"]["schema_sha256"],
        "state": report["request"]["state"],
        "remote_id": report["request"]["remote_id"],
    },
    "stage_request_packet": {"path": PACKET, "sha256": expected_preserved[PACKET]},
    "q_records": [{"id": c["id"], "record_sha256": c["record_sha256"], "state_px_line": line} for c, line in zip(
        report["criteria"],
        [30, 33, 29, 27, 31, 32, 28, 19, 22, 20, 21, 18, 10, 13, 11, 12, 9, 4, 6, 5],
    )],
    "files": preserved_files,
    "tools_not_called": [
        "pixl_production_plan", "pixl_stage_prepare", "pixl_plar_save", "pixl_plar_prepare", "pixl_plar_handoff", "pixl_commit",
        "pixl_job_dispatch", "pixl_job_prepare", "pixl_job_observe", "pixl_job_import", "pixl_task_complete", "pixl_family_snapshot",
        "pixl_inspection_prepare", "pixl_inspection_review", "pixl_init", "pixl_intake", "pixl_retain_library", "any PixelLab remote tool",
    ],
    "tools_called": ["pixl_asset_check (two retained artifacts, read-only)", "file reads, grep, Python -I hashing"],
}

# verify the Q-record line mapping against state.px
for row in historical_preservation["q_records"]:
    line = file_lines(SP)[row["state_px_line"] - 1]
    if not line.startswith("@" + row["id"] + ":Q{"):
        raise SystemExit(f"Q record line mismatch for {row['id']} at line {row['state_px_line']}")

# ----------------------------------------------------------------- write ----
counts = {"criteria_covered": len(criteria_out), "keep": 0, "clarify": 0, "correct": 0}
for row in criteria_out:
    counts[row["change"]] += 1

proposal = {
    "version": 1,
    "kind": "specialist_corrected_proposal",
    "role": "PIXL specialist (pixl-kit profile), review repair of the authoring-01 connected plan; no generation, no provider request, no state writes",
    "assignment": {"path": "AUTHORING-REVIEW.md", "sha256": sha256(ROOT / "AUTHORING-REVIEW.md")},
    "reviewed_report": {
        "path": "work/criteria-review-01/request-review.json",
        "sha256": EXPECTED_REPORT_SHA,
        "raw_path": "work/criteria-review-01/request-review-raw.txt",
        "raw_sha256": EXPECTED_RAW_SHA,
        "review_scope_sha256": EXPECTED_SCOPE_SHA,
        "plan": report["plan"],
        "job": report["request"]["id"],
        "state": report["state"],
    },
    "conventions": {
        "lines": "one-based inclusive file-local bounds; each cited range was opened and verified at build time to contain the wording relied on (see verification in specialist-report.json)",
        "authority": "PLAR labels requirement / proposal / observation / unknown, asserted by the specialist for the caller to compare; 'requirement' includes consumer-code behavior and adopted caller decisions where the basis says so",
        "scope": "whole asset/stage, 'seed rotation construction', 'this authoring branch', 'method', or 'example'",
        "images": "zero-based pixel coordinates; component boxes from pixl_asset_check are measurements, not verdicts",
    },
    "summary_of_substantive_corrections": [
        "transparent-exterior (working, retry, paused): review route corrected - deciding which pixels are 'the mark' and whether a plate/matte is unwanted is visual judgment; mechanical measurement kept only where it is decidable (seed-rotation alpha equality); blanket 'no plate' narrowed to unintended matte/tile.",
        "working.q.frame-assembly: 'lossless copy' bounded to alpha + visible RGBA (transparent RGB insignificant); 'duplication' bounded to undocumented substitution; construction-scoped pixel-exact rotation clause added as a proposal (listed in the policy but carried by no Q record).",
        "working.q.motion-continuity: required outcome (continuous, evenly paced loop, seamless wrap) separated from contract-bound expert clauses (anchor/volume) and construction-scoped clauses (cluster count, stepped phases, no morphing/near-hold).",
        "working.q.activity-not-success: 'arrowhead' and 'pause bars' re-scoped as expert guidance derived from proposed motifs of other members; check mark / terminal pose remain required.",
        "consumers (working, retry, paused) and delivery.q.destination: 'actual consumer renderer' named as the fixture; 'observed live 100 ms frame advance' corrected to what the fixture evidences (timeline frame indices incl. the 400 ms wrap plus observed cycling; wall-clock not measured); 1x/3x routes stated.",
        "working.q.geometry: 'padding' defined as added canvas so in-cell transparent margins are not rejected; slicing attributed to renderer/view.mjs.",
    ],
    "criteria": criteria_out,
    "sources": sources,
    "measurements": measurements,
    "choices": choices,
    "reduced_motion": reduced_motion,
    "historical_preservation": historical_preservation,
    "not_claimed": ["acceptance of any candidate", "adoption of this proposal (caller decision)", "dispatch or provider execution", "that the old request is current", "that the old request is dead"],
}

PROPOSAL_PATH.write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
proposal_sha = sha256(PROPOSAL_PATH)

summary = {
    "version": 1,
    "kind": "specialist_report",
    "status": "delivered",
    "status_scope": "AUTHORING-REVIEW.md specialist deliverable: separate corrected proposal covering all 20 criteria with clause-level authority/basis/scope/source, choices, reduced-motion section and preservation record. The caller's independent comparison, coverage check and CRITERIA-RESULT.json remain the caller's work. No generation, request, dispatch or state write occurred.",
    "proposal": {"path": "work/criteria-review-01/specialist-proposal.json", "sha256": proposal_sha},
    "reviewed_report": proposal["reviewed_report"],
    "counts": counts,
    "substantive_corrections": proposal["summary_of_substantive_corrections"],
    "verification": {
        "criteria_copied_verbatim_from_report": True,
        "citations_verified": len(verified_citations),
        "citation_method": "each cited [first,last] range opened from disk and checked to contain the relied-on wording; build aborts on any failure",
        "historical_hashes_rechecked": len(preserved_files),
        "q_record_lines_checked_in_state_px": True,
        "measurements": [{"path": m["path"], "sha256": m["sha256"]} for m in measurements],
    },
    "reduced_motion_summary": {
        "bound_requirements_hash": "e0614bd962a53a19003707f3d73326be436891e198eb1e4a262f12412fbfb027",
        "current_requirements_hash": "2901c7107d4f162e98653140ea8061dfe213821b22a5e1338d9d2d6de5b4ad0c",
        "consumer_mapping": "none exists today in src/queue-view.ts, src/queue.ts or renderer/view.mjs (confirmed)",
        "criteria_affected_if_adopted": "none rewritten; stationary symbol uncovered by all 20; impacts listed per mapping option in the proposal",
        "job": "authoring-01.working.join-01 remains prepared/undispatched, bound to e0614bd9; resolution is a caller decision",
    },
    "questions_for_caller": [
        "Reduced motion: which mapping (renderer rule holding a designated strip cell vs separate static file/descriptor) and which preference source; is distinction from Retry/Start also required; does the animated strip remain required alongside it?",
        "Transparent-exterior route: adopt the split (measured + visual records) or keep one record with mode visual? Either preserves the requirement; the choice affects how many Q records a future plan carries.",
    ],
    "verified_citations": verified_citations,
}
SUMMARY_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(json.dumps({
    "proposal": {"path": str(PROPOSAL_PATH), "sha256": proposal_sha},
    "report": {"path": str(SUMMARY_PATH), "sha256": sha256(SUMMARY_PATH)},
    "counts": counts,
    "citations_verified": len(verified_citations),
}, indent=2))
