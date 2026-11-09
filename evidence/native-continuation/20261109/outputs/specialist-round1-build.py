"""Build work/continuation/SPECIALIST-ROUND1.json (PIXL round-1 assessment of the retained 29-criterion proposal).

Every text citation below is opened and verified at build time (one-based inclusive file-local lines must contain
the listed wording); JSON-field citations are verified by path. Hashes are computed from the actual bytes.
Usage: python -I work/continuation/specialist-round1-build.py CONSUMER_ROOT
Writes only SPECIALIST-ROUND1.json; it reads (never modifies) every other file.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "work/continuation/SPECIALIST-ROUND1.json"


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def lines_of(rel):
    return (ROOT / rel).read_text(encoding="utf-8").splitlines()


# ---------------------------------------------------------------- shared source index
SOURCES = {
    "brief": ("BRIEF.md", "owner brief"),
    "update": ("AUTHORING-UPDATE.md", "caller reduced-motion update (authoring branch)"),
    "plar": ("authoring-plar.txt", "current authoring PLAR; queue.working row; line 422 carries the caller update"),
    "assignment": ("FOCUSED-SUCCESSOR.md", "assignment the proposal answered (step 2 lines 18-23); process requirements"),
    "authoring-stage": ("AUTHORING-STAGE.md", "earlier authoring assignment; lines 31-32 state the frame-selection/assembly process requirement (NOT in the proposal's source index)"),
    "continuation": ("CONTINUATION-ASSIGNMENT.md", "this phase's assignment"),
    "queue-ts": ("src/queue.ts", "backend state machine, shared by both consumers (original, unchanged)"),
    "view-ts": ("src/queue-view.ts", "original consumer module, unchanged (historical destination)"),
    "successor-ts": ("src/queue-view-successor.ts", "caller-proposed successor consumer module: a revisable design proposal, not owner authority"),
    "succ-view": ("renderer-successor/view.mjs", "successor browser fixture (evidence route); design proposal"),
    "succ-check": ("renderer-successor/check.py", "successor mechanical checker; never run on a completed capture"),
    "succ-index": ("renderer-successor/index.html", "successor fixture page"),
    "succ-capture": ("renderer-successor/capture.mjs", "successor capture driver"),
    "old-view": ("renderer/view.mjs", "original fixture, unchanged"),
    "working-png": ("assets/working.png", "existing Working sheet 64x16 (reuse candidate)"),
    "ready-png": ("assets/ready-confirmed.png", "exact Ready style baseline"),
    "paused-png": ("assets/paused.png", "delivered Paused member"),
    "retry-png": ("assets/error-retry.png", "delivered Retry member"),
    "start-svg": ("assets/start.svg", "preserved vector Start control"),
    "seed-png": (".pixl/assets/queue.ready/artifacts/21f5baca68958eaa30d89fe9ec216e2b8dfc9e4a941f80b8a19fa0e712939629.png", "accepted Working seed artifact"),
    "motion-artifact": (".pixl/assets/queue.ready/artifacts/cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc.png", "retained artifact of live.working-animation-motion-01.candidate (byte-identical to assets/working.png)"),
    "state": (".pixl/assets/queue.ready/state.px", "PX2 store revision 88 (read only)"),
    "context": ("work/focused-successor/context-authoring-raw.json", "focused authoring context: the 20 original Q ids, record hashes and literal checks"),
    "proposal": ("work/focused-successor/specialist-proposal.json", "OBJECT UNDER REVIEW: 29-criterion reduced-motion proposal"),
    "report": ("work/focused-successor/specialist-report.json", "its delegation result; verification = 79 citations"),
    "r2": ("work/criteria-review-01/specialist-proposal-r2.json", "prior corrected proposal r2 (D1-D4 settled)"),
    "caller-cmp": ("work/export-review-01/caller-comparison.json", "prior caller comparison (D1-D4 resolutions)"),
    "rr-export": ("work/continuation/request-review-authoring-01.json", "caller's retained pixl_request_review export for authoring-01.plan (used instead of a new call)"),
    "measurements-prop": ("work/focused-successor/specialist-views/specialist-measurements.json", "the proposal's measurements"),
    "views-pair": ("work/focused-successor/specialist-views/specialist-pair-w0-retry-ready-paused.png", "proposal's pair view (viewed by me)"),
    "render-01-launch": ("work/focused-successor/render-01/launch.json", "incomplete successor capture: launch record (no render.json exists)"),
    "render-01-process": ("work/focused-successor/render-01/browser-process.json", "incomplete successor capture: browser process record (exitCode null)"),
    "my-measurements": ("work/continuation/round1-views/round1-measurements.json", "my reproducible measurements and view hashes"),
    "my-views-build": ("work/continuation/round1-views-build.py", "script that produced my views/measurements"),
    "kit-request-review": (".agents/skills/continuation-kit/skills/pixl/references/request-review.md", "kit: request and criteria review"),
    "kit-profile": (".agents/skills/continuation-kit/resources/agent/PROFILE.md", "kit: PIXL profile"),
    "kit-intake": (".agents/skills/continuation-kit/skills/pixl/references/intake-sample.md", "kit: authority check"),
    "kit-authority": (".agents/skills/continuation-kit/skills/pixl/references/artistic-authority.md", "kit: artistic authority"),
    "kit-delegation": (".agents/skills/continuation-kit/skills/pixl/references/delegation.md", "kit: delegation contract"),
}
for key, (rel, _) in SOURCES.items():
    assert (ROOT / rel).is_file(), f"missing source {key}: {rel}"
SOURCE_INDEX = {k: {"path": rel, "sha256": sha(rel), "role": role} for k, (rel, role) in SOURCES.items()}

VERIFIED = []


def cite(src, first, last, must):
    """One-based inclusive lines of SOURCES[src] must contain `must` (joined with newlines)."""
    text = "\n".join(lines_of(SOURCES[src][0])[first - 1:last])
    if must not in text:
        raise SystemExit(f"CITATION FAILED {src} {first}-{last}: {must!r} not in {text[:200]!r}")
    VERIFIED.append([src, first, last, must])
    return {"source": src, "lines": [first, last], "contains": must}


def fcite(src, must):
    text = (ROOT / SOURCES[src][0]).read_text(encoding="utf-8")
    if must not in text:
        raise SystemExit(f"FILE CITATION FAILED {src}: {must!r}")
    VERIFIED.append([src, "file", "file", must])
    return {"source": src, "lines": None, "contains": must}


def jload(src):
    return json.loads((ROOT / SOURCES[src][0]).read_text(encoding="utf-8"))


def jcite(src, path, expect=None):
    """JSON-field citation: path like a.b[0].c must exist (and equal expect when given)."""
    node = jload(src)
    for part in path.replace("]", "").split("."):
        if "[" in part:
            name, idx = part.split("[")
            node = node[name] if name else node
            node = node[int(idx)]
        else:
            node = node[part]
    if expect is not None and node != expect:
        raise SystemExit(f"JSON CITATION FAILED {src} {path}: {node!r} != {expect!r}")
    VERIFIED.append([src, "json", path, expect if expect is not None else "(exists)"])
    return {"source": src, "field": path, "value": expect if expect is not None else (node if isinstance(node, (str, int, bool)) else "(exists)")}


# ---------------------------------------------------------------- identities
proposal = jload("proposal")
report = jload("report")
context = jload("context")
assert SOURCE_INDEX["proposal"]["sha256"] == "792d4b8f47211a0c646466793e54cc4c16e85c6556bd471f44de2562809b14b3"
assert SOURCE_INDEX["state"]["sha256"] == "3484cf385c91c8c28fa04316fb2c7c5b52c740178b505ccbd88631f57c893c9b"
assert context["revision"] == 88 and context["hash"] == SOURCE_INDEX["state"]["sha256"]

source_hash_check = []
for sid, s in proposal["sources"].items():
    actual = sha(s["path"])
    source_hash_check.append({"id": sid, "path": s["path"], "claimed": s["sha256"], "actual": actual, "match": actual == s["sha256"]})
assert all(x["match"] for x in source_hash_check), "proposal source hash mismatch"

# The 79 citations of the proposal's report, re-verified here from the actual files.
citation_recheck = []
for v in report["verification"]:
    text = "\n".join(lines_of(v["path"])[v["lines"][0] - 1:v["lines"][1]])
    citation_recheck.append({"cite": v["cite"], "path": v["path"], "lines": v["lines"], "verified_by_me": v["expected_wording"] in text})
assert all(c["verified_by_me"] for c in citation_recheck)

# Record hashes: pixl_validate(.pixl/assets/queue.ready/state.px) in this session returned hash 3484cf38... revision 88;
# the 20 Q record hashes below are copied from that tool result and compared with the context packet and the proposal.
VALIDATE_HASHES = {
    "authoring-01.delivery.q.continuity": "6df7e20ca123e5df9d02960a3c5413b8c3b0b4824ac14dcba5dba3e25b59a84b",
    "authoring-01.delivery.q.destination": "f9d04bde1905a8223494dc3c3ce1573a54b99c3e80e543367edb69055104c5a6",
    "authoring-01.delivery.q.distinction": "495b765b7d19e863bc8fa14ee344478d9b690552717be8c7dbe09cb735dd78a7",
    "authoring-01.paused.q.consumers": "cf34749f0a5f4696e02a2ca9c1b6ed5e924345c3a21581edf2321726d34e4aa1",
    "authoring-01.paused.q.geometry": "6ddf39c0e5ded6d3eb64e2324ee27de7fa7b2e718e033338ed9059088ae77bae",
    "authoring-01.paused.q.pause-meaning-without-color": "249bc83e1b2813fcfde4209acf1bcc34ac5a5580cd665d2bd639b5e9136bf777",
    "authoring-01.paused.q.style-coherence": "fb4d6d176c9029e2cee15bd8fca3681b1c3f080a6a67d621ee499ebf71530141",
    "authoring-01.paused.q.transparent-exterior": "3825694288a35fe5986e104f343e0a667ee8943a9f5b9c1062a7053e979a4e91",
    "authoring-01.retry.q.consumers": "63bb9a45e56d01026c98299c05c79c19cf0bd6ae4b2abb56242af3c543d4014f",
    "authoring-01.retry.q.geometry": "b9181108856b1221fe79ffbe6b773d347dfd2b1cab6cb6faaf8be1de7ad072dd",
    "authoring-01.retry.q.retry-meaning-without-color": "021696acc3bb3ec4ed48cc1465c685825830f0c63b5622862c3f2a689bec58c9",
    "authoring-01.retry.q.style-coherence": "ff724740ecd4df5840f310e12c8e22c59228f486e2d82ea979bfedf98865ec96",
    "authoring-01.retry.q.transparent-exterior": "f076bd55723bcb531f46bd21450bc11bf170b91c8b79d83d19153b29da02e4d4",
    "authoring-01.working.q.activity-not-success": "a5719b7cef8299db0608afec30c2b0e8ee2a732c482663b38fae283d1aac1e30",
    "authoring-01.working.q.consumers": "ed2091c5d4fcc40b51a4ac9deba9c35e60e93e9e070d04101c3beefd7bde8084",
    "authoring-01.working.q.frame-assembly": "f524a8f70a0cdf6b7c6b3888c87930cc0dfe0a73db4b35ca57fecc307233fca2",
    "authoring-01.working.q.geometry": "2ed1c002b7e74113a05691c6f1049a5d2687d9cd3d6edc72487c70b289f2b4e1",
    "authoring-01.working.q.motion-continuity": "3c047ce9c41259f17f2afeb2ca2dc4c62aa931cd7e61a99c14d62acdcff0ea54",
    "authoring-01.working.q.style-coherence": "066b5cffb06e93e2f3a4aad785a06ce9328b77547852b26059f115176a6b01db",
    "authoring-01.working.q.transparent-exterior": "a2a7a4b732d9f595aca9d557d1a16fbce9e9498d24a3d72a7a3e12a502374c83",
}
ctx_criteria = {c["id"]: c for c in context["criteria"]}
assert set(ctx_criteria) == set(VALIDATE_HASHES) and len(ctx_criteria) == 20
for cid, c in ctx_criteria.items():
    assert c["record_sha256"] == VALIDATE_HASHES[cid], cid
rr_export = jload("rr-export")
rr_ids = {c["id"]: c for c in rr_export["criteria"]}
assert set(rr_ids) == set(VALIDATE_HASHES)
for cid, c in rr_ids.items():
    assert c["record_sha256"] == VALIDATE_HASHES[cid] and c["check"] == ctx_criteria[cid]["fields"]["ck"], cid

# mapping checks
mapping = {m["original_id"]: m for m in proposal["mapping"]}
assert set(mapping) == set(VALIDATE_HASHES)
prop_criteria = {c["id"]: c for c in proposal["criteria"]}
assert len(prop_criteria) == 29
mapping_rows = []
carry_back = {}
for cid, m in mapping.items():
    row = {
        "original_id": cid,
        "record_sha256": m["record_sha256"],
        "hash_matches_context_and_validate": m["record_sha256"] == VALIDATE_HASHES[cid],
        "original_check_matches_context": m["original_check"] == ctx_criteria[cid]["fields"]["ck"],
        "carried_by": m["carried_by"],
        "carried_by_exist": all(x in prop_criteria for x in m["carried_by"]),
    }
    for x in m["carried_by"]:
        carries = [k["id"] for k in prop_criteria[x].get("carries", [])]
        carry_back.setdefault(x, []).append(cid in carries and any(k["record_sha256"] == VALIDATE_HASHES[cid] for k in prop_criteria[x]["carries"]))
    mapping_rows.append(row)
assert all(r["hash_matches_context_and_validate"] and r["original_check_matches_context"] and r["carried_by_exist"] for r in mapping_rows)
assert all(all(v) for v in carry_back.values())
new_ids = [c["id"] for c in proposal["criteria"] if not c.get("carries")]
assert sorted(new_ids) == sorted(proposal["criteria_summary"]["new_for_reduced_motion"]) and len(new_ids) == 6

my_meas = jload("my-measurements")
assert my_meas["images"]["assets/working.png"]["sha256"] == SOURCE_INDEX["working-png"]["sha256"]
assert SOURCE_INDEX["motion-artifact"]["sha256"] == SOURCE_INDEX["working-png"]["sha256"] == "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc"
assert my_meas["cell0_equals_seed_alpha_and_visible_rgba"] is True and my_meas["cells_1_3_equal_cw_k_cell0_alpha_and_visible_rgba"] == [True, True, True]
prop_cell0 = proposal["reduced_motion_design"]["measured_facts"]["cell0_frame0"]
assert prop_cell0["components"] == my_meas["images"]["working cell 0"]["components"]
assert prop_cell0["mass_centroid_edge_coords"] == my_meas["images"]["working cell 0"]["centroid_edge"]
assert prop_cell0["alpha_histogram"] == my_meas["images"]["working cell 0"]["alpha_histogram"]
assert not (ROOT / "work/focused-successor/render-01/render.json").exists()
ctx_contracts = {c["id"]: c for c in context["contracts"]}
working_contract_li = ctx_contracts["family.working.contract"]["fields"]["li"]
assert any(c["id"] == "recheck.decision.destination" for c in context["decisions"])

# ---------------------------------------------------------------- frequently used citations
B3_FRAMES = cite("brief", 3, 3, "Working uses four horizontal frames with a 100 ms frame duration")
B3_CELLS = cite("brief", 3, 3, "Status cells are 16 by 16 logical pixels")
B3_TRANSP = cite("brief", 3, 3, "Use transparent backgrounds")
B3_SILH = cite("brief", 3, 3, "readable silhouettes")
B3_BLUE = cite("brief", 3, 3, "the existing UI's cool blue accent")
B3_PALETTE = cite("brief", 3, 3, "a fixed palette is not required")
B3_INSPECT = cite("brief", 3, 3, "Inspect at 1x and 3x nearest display scale on the actual dark panel")
B3_ACTIVITY = cite("brief", 3, 3, "communicate activity without looking like success")
B3_RETRY = cite("brief", 3, 3, "Error/retry must be distinguishable without color alone")
B3_STATIC = cite("brief", 3, 3, "Ready and Retry are static images")
B3_START = cite("brief", 3, 3, "Preserve the existing vector Start control")
B3_COHERENT = cite("brief", 3, 3, "Create coherent pixel-art status assets")
B5_PATHS = cite("brief", 5, 5, "Assets belong at the paths already used by the view")
B7_PAUSED = cite("brief", 7, 7, "distinguishable from activity, completion and retry without relying on color alone")
B7_KEEP = cite("brief", 7, 7, "Keep the existing style and display requirements")
B7_PURPOSE = cite("brief", 7, 7, "its purpose is unchanged")
B9_CHECK = cite("brief", 9, 9, "check mark with asymmetrical arms")
U_REQ = cite("update", 2, 4, "symbol distinct from Ready and Paused")
U_RETAIN = cite("update", 5, 10, "remains retained")
P422 = cite("plar", 422, 422, "stationary Working symbol distinguishable from Ready and Paused")
P422_NOSUCCESS = cite("plar", 422, 422, "without implying success")
P422_MAPPING = cite("plar", 422, 422, "Confirm its consumer mapping before any further generation")
P_STYLE = cite("plar", 512, 528, "not an original brief requirement")
P_GEOM = cite("plar", 529, 545, '"frames": 4')
P_ANIM = cite("plar", 546, 559, '"frame_duration_ms": 100')
P_MEANING = cite("plar", 560, 570, "success-like terminal pose")
P_DELIV_WRAP = cite("plar", 606, 619, "Play the loop at 100 ms per frame and inspect the fourth-to-first transition")
A_STEP2 = cite("assignment", 18, 23, "not an owner-imposed motif, palette or frame choice")
A_STEP3_PACING = cite("assignment", 24, 31, "Expert pacing is not the")
A_STEP3_START = cite("assignment", 24, 31, "distinction is a shared-consumer inference")
A_STEP3_LIVE = cite("assignment", 24, 31, "Add explicit reduced-motion mapping and live preference-switch acceptance")
A_STEP4_PREF = cite("assignment", 32, 43, "respect prefers-reduced-motion and changes while open")
A_STEP4_FILES = cite("assignment", 32, 43, "implement the successor")
A_STEP4_OLD = cite("assignment", 32, 43, "keep old src/queue-view.ts and renderer/ untouched")
A_STEP4_REUSE = cite("assignment", 40, 43, "Reuse reviewed existing art when it satisfies the new criteria")
A_STEP4_BOTH = cite("assignment", 32, 43, "both statusCell and")
A_STEP6_SWITCH = cite("assignment", 52, 58, "switching the preference in the same session")
A_STEP6_NOTACC = cite("assignment", 52, 58, "A plan or code check is")
A_STEP6_SEP = cite("assignment", 52, 58, "distinguish mechanical,")
AS_ASSEMBLY = cite("authoring-stage", 31, 32, "frame-selection/assembly policy")
Q_STATE = cite("queue-ts", 1, 3, "stateAfter")
V_IDLE = cite("view-ts", 3, 3, 'idle: { label: "Start"')
V_RUNNING = cite("view-ts", 4, 4, "frames: 4")
V_PAUSED = cite("view-ts", 5, 5, '"Paused"')
V_RETRY = cite("view-ts", 7, 7, '"Retry"')
V_DISPLAY = cite("view-ts", 9, 9, "frameMs: 100")
V_CONSUMERS = cite("view-ts", 10, 11, "compactStatus")
S_QUERY = cite("successor-ts", 5, 5, "(prefers-reduced-motion: reduce)")
S_IDLE = cite("successor-ts", 7, 7, 'label: "Start"')
S_RUNNING = cite("successor-ts", 8, 8, "frames: 4, still: 0")
S_PAUSED = cite("successor-ts", 9, 9, '"Paused"')
S_RETRY = cite("successor-ts", 11, 11, '"Retry"')
S_PATHS = cite("successor-ts", 6, 12, "assets/error-retry.png")
S_DISPLAY = cite("successor-ts", 13, 13, "frameMs: 100")
S_STILL = cite("successor-ts", 14, 14, "`still` is the cell held when motion is reduced")
S_DESCRIPTOR = cite("successor-ts", 16, 16, "holdFrame: number | null")
S_MOTION = cite("successor-ts", 17, 19, "matchMedia")
S_DESCRIBE = cite("successor-ts", 20, 23, "holdFrame: animate ? null : visual.still")
S_GATE = cite("successor-ts", 21, 21, "visual.frames > 1")
S_FRAMEAT = cite("successor-ts", 24, 26, "descriptor.holdFrame ?? 0")
S_CONSUMERS = cite("successor-ts", 27, 28, "compactStatus")
F_SESSION = cite("succ-view", 8, 8, "proves no reload")
F_PAINT = cite("succ-view", 41, 52, "drawImage")
F_SMOOTH = cite("succ-view", 45, 45, "imageSmoothingEnabled")
F_GATE = cite("succ-view", 48, 48, "asset.width === width * descriptor.frames")
F_LABEL = cite("succ-view", 62, 62, "label.textContent = descriptor.label")
F_CREATE = cite("succ-view", 69, 69, "info.frame = paint(")
F_MATRIX = cite("succ-view", 95, 95, "for (const scale of [1, display.scale])")
F_LIVE = cite("succ-view", 105, 105, "makeCell(consumer, state, display.scale, 0, false)")
F_REFRESH = cite("succ-view", 80, 87, "repaint it in place")
F_CHANGE = cite("succ-view", 114, 121, "addEventListener('change'")
F_ANIMATE = cite("succ-view", 123, 130, "cell.descriptor.animate")
F_TIMELINE = cite("succ-view", 141, 149, "timeline.push")
F_TIMELINE_SYNTH = cite("succ-view", 146, 146, "makeCell(consumer, state, 1, elapsed, false)")
F_LIVE_SAMPLE = cite("succ-view", 157, 157, "elapsed: performance.now() - origin")
F_SCOPE = cite("succ-view", 158, 160, "visual/style acceptance are separate")
C_MODULES = cite("succ-check", 51, 52, "did not execute the retained original consumer module")
C_BASELINE = cite("succ-check", 53, 56, "retained file unchanged since baseline")
C_SESSION = cite("succ-check", 58, 59, "one open page session")
C_PHASES = cite("succ-check", 67, 69, '"normal-start": "normal", "reduced": "reduced", "normal-restored": "normal"')
C_DESCRIPTOR = cite("succ-check", 81, 86, "hold frame is the declared still cell")
C_COMPOSITE = cite("succ-check", 105, 112, "alpha compositing (rounding tolerance one)")
C_IDENTICAL = cite("succ-check", 126, 131, "identical running descriptor")
C_LIVE_ONE = cite("succ-check", 140, 140, "frame-boundary tolerance")
C_LIVE_HOLD = cite("succ-check", 133, 146, "live cell holds the still cell")
C_TIMELINE = cite("succ-check", 148, 166, "frame index")
C_CYCLE = cite("succ-check", 161, 164, "frames_seen == {0, 1, 2, 3}")
C_HOLD = cite("succ-check", 166, 166, "reduced motion never leaves the held cell")
C_SWITCH = cite("succ-check", 170, 190, "[switch]")
C_SWITCH_RUNNING = cite("succ-check", 180, 180, 'r["state"] == "running"')
C_RESUME = cite("succ-check", 190, 190, "resumed animation")
C_SCOPE = cite("succ-check", 191, 192, "it does not judge whether the held cell reads as Working")
I_PIXELATED = cite("succ-index", 21, 21, "image-rendering: pixelated")
CAP_PHASES = cite("succ-capture", 4, 5, "as-launched")
CAP_DEFAULT = cite("succ-capture", 20, 20, "'normal-start,reduced,normal-restored'")
CAP_RENDER = cite("succ-capture", 98, 99, "render.json")
K_RECIPE = cite("kit-request-review", 32, 32, "Keep a required outcome separate from the recipe")
K_CREATIVE = cite("kit-request-review", 34, 34, "Creative decisions within the assignment")
K_LABEL = cite("kit-request-review", 76, 78, "This label is an assertion to compare")
K_ROUTE = cite("kit-request-review", 172, 181, "review route")
K_PROCESS = cite("kit-request-review", 208, 208, "Keep process requirements, output requirements and diagnostic proxies distinct")
K_ROLE = cite("kit-profile", 55, 61, "Interpret a colour's role separately from its extent")
K_TRANSP = cite("kit-profile", 62, 67, "transparent exterior")
K_AA = cite("kit-profile", 77, 77, "Distinguish intentional anti-aliasing")
K_EVIDENCE = cite("kit-profile", 86, 86, "Label claims as measured")
K_BINARY = cite("kit-intake", 9, 9, "binary alpha and fixed palettes are not universal requirements")
K_REFERENCE = cite("kit-intake", 15, 15, "matching a reference does not adopt every measured dimension")
K_DIAG = cite("kit-intake", 19, 19, "Keep diagnostic conclusions attached to their tested artifact")
K_TEST = cite("kit-authority", 11, 11, "Test each derived restriction against a variation that still satisfies the brief")
K_RESTART = cite("kit-delegation", 25, 35, "Historical evidence stays unchanged")
START_HEX = fcite("start-svg", "#70b9ed")
CC_D1 = jcite("caller-cmp", "discrepancies_with_specialist[0].id", "D1")
CC_D2 = jcite("caller-cmp", "discrepancies_with_specialist[1].id", "D2")
CC_D3 = jcite("caller-cmp", "discrepancies_with_specialist[2].id", "D3")
CC_D4 = jcite("caller-cmp", "discrepancies_with_specialist[3].id", "D4")
R2_D2 = jcite("r2", "revision_changes[3].finding", "D2")
R2_D3 = jcite("r2", "revision_changes[4].finding", "D3")
CTX_CONTRACT = jcite("context", "contracts", None)
RL_PROJECT = jcite("render-01-launch", "project", None)
RP_EXIT = jcite("render-01-process", "exitCode", None)

# ---------------------------------------------------------------- authority classes
CLASSES = {
    "owner": "owner requirement: BRIEF.md with line",
    "caller_update": "caller requirement update: authoring-plar.txt line 422 / AUTHORING-UPDATE.md",
    "caller_adopted_decision": "adopted scoped caller decision (approved_style_reference, destination method); not an original brief line",
    "assignment_process": "assignment process requirement: FOCUSED-SUCCESSOR.md (or AUTHORING-STAGE.md where stated)",
    "consumer_fact_original": "consumer-code fact of the ORIGINAL module (src/queue.ts, src/queue-view.ts, unchanged)",
    "consumer_fact_successor_proposed": "consumer-code fact of the PROPOSED successor module src/queue-view-successor.ts (revisable design proposal)",
    "fixture_fact": "fact of the proposed successor fixture renderer-successor/view.mjs|index.html|capture.mjs (evidence route, revisable)",
    "checker_fact": "fact of renderer-successor/check.py (what it does or does not assert)",
    "measured": "measured fact with image hash and coordinate convention",
    "expert_choice": "scoped expert choice (whose, and what scope)",
    "inference": "inference from sources (reasonable reading), not an owner line",
    "method": "review/comparison method (how to look), not a restriction on the art",
    "non_restriction": "explicit statement of what is NOT required",
    "diagnostic": "diagnostic proxy that triggers review; not a rejection rule",
    "honest_limit": "statement of what is not claimed",
}


def crit(cid, clauses, expert_note=None):
    c = prop_criteria[cid]
    return {
        "id": cid,
        "check": c["check"],
        "domain": c["domain"],
        "mode": c["mode"],
        "labelled_authority": c["authority"],
        "carries": [k["id"] for k in c.get("carries", [])],
        "clauses": clauses,
        "expert_clauses_in_proposal": [e["text"] for e in c.get("expert_clauses", [])] or None,
        "note": expert_note,
    }


def cl(text, klass, basis, locators, scope, defect=None):
    assert klass in CLASSES
    return {"text": text, "class": klass, "basis": basis, "locator": locators if isinstance(locators, list) else [locators], "scope": scope, "defect": defect}


STYLE_CLAUSES = lambda asset: [
    cl("Readable compact silhouette(s)", "owner", "BRIEF line 3 readable silhouettes; 'compact' comes from the adopted baseline decision", [B3_SILH, P_STYLE], f"whole {asset}"),
    cl("deliberate coherent clusters and stepped edges consistent with the exact Ready baseline", "caller_adopted_decision", "authoring-plar.txt 512-528 approved_style_reference (reason: scoped caller decision, not an original brief requirement)", [P_STYLE], "this consumer status family"),
    cl("(selective, intentional anti-aliasing is permitted under the full-alpha contract; accidental resampling blur or stray noise is not)", "non_restriction", "full-alpha contract; profile pixel-craft distinction between intentional AA and resampling artifacts; no binary-alpha rule exists", [K_AA, K_BINARY], "all members"),
    cl("a perceptible cool-blue accent related to the Ready baseline and the preserved Start accent", "inference", "BRIEF line 3 names 'the existing UI's cool blue accent' (perceptibility, PROFILE visual roles); relating it to the Start fill #70b9ed is an inference that Start is the existing UI's accent exemplar; the role is about perceptibility, not extent", [B3_BLUE, START_HEX, K_ROLE], f"whole {asset}", "S9"),
    cl("judged qualitatively at 1x and 3x on #172336", "owner", "BRIEF line 3 inspection conditions; #172336 is display.background in both modules", [B3_INSPECT, V_DISPLAY, S_DISPLAY], "review conditions"),
    cl("no exact hex, palette count, binary alpha, stroke width or margin rule", "non_restriction", "BRIEF line 3 'a fixed palette is not required'; adopted decision not_fixed list", [B3_PALETTE, P_STYLE], "all members"),
]
MEASURED_CLAUSES = lambda member, construction: [
    cl("retain every cell's alpha histogram and exact RGBA component boxes (zero-based, half-open)", "method", "measurement route adopted by the caller in D1 for any future plan", [CC_D1], member),
    cl("FLAG for visual review any alpha>0 component touching all four cell edges, or ... more than half of the cell's 256 pixels ... NOT a rejection condition", "diagnostic", "D1: diagnostic proxy for a matte/grey tile; a corner-to-corner X legitimately touches four edges", [CC_D1, K_DIAG], member),
    cl("RGB values of alpha-0 pixels are not significant", "non_restriction", "measured: the sheet's transparent pixels carry (128,128,128,0) x817 and (0,0,0,0) x79 and composite identically", [jcite("measurements-prop", "source_sheet_sha256", "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc")], member),
] + ([
    cl("Mechanical REJECTION is decidable only under the seed-rotation construction: each cell's alpha channel must equal that of cw^k(seed) ... (224 alpha-0 and 32 alpha-255 pixels per cell)", "expert_choice", "specialist construction scope (seed rotation); measured True for cf101610... by the proposal and by me; the 224/32 figures are measured values of seed 21f5baca..., not part of the rule", [jcite("my-measurements", "cell0_equals_seed_alpha_and_visible_rgba", True), K_REFERENCE], "seed-rotation construction only", "S8"),
] if construction else [
    cl("No mechanical rejection rule is decidable for this static member", "honest_limit", "no construction fixes the alpha set; the visual record decides (D1)", [CC_D1], member),
])
VISUAL_TRANSP = lambda member, held: [
    cl("the exterior ... shows the panel with no unintended matte, tile, plate, halo or fringe" + (" (including the held cell when stationary)" if held else ""), "owner", "BRIEF line 3 'Use transparent backgrounds'; 'unintended' narrows the blanket 'no plate' (D1)" + ("; held cell added per the caller update" if held else ""), [B3_TRANSP] + ([P422] if held else []), member),
    cl("a deliberate opaque backing shape is acceptable only when it is part of the mark's recorded design and the exterior stays transparent", "inference", "profile transparency guidance: a transparency requirement does not prohibit every opaque backing; permissive clause", [K_TRANSP], member),
    cl("Partial alpha on mark pixels is permitted; binary alpha is not required", "non_restriction", "full-alpha contract; binary alpha is not a universal requirement", [K_BINARY], member),
    cl("viewed at 1x and 3x on #172336", "owner", "BRIEF line 3 inspection conditions", [B3_INSPECT], "review conditions"),
]
CONSUMER_ROUTE = cl("In the successor browser fixture renderer-successor/view.mjs executing the actual src/queue.ts and src/queue-view-successor.ts modules, checked by renderer-successor/check.py against the retained capture", "assignment_process", "FOCUSED-SUCCESSOR step 4 (successor files) and step 6 (exercise the successor renderer); check.py asserts the successor module was served and the original was not", [A_STEP4_FILES, A_STEP6_SWITCH, C_MODULES], "evidence route for every engine/live criterion")
RENDER_SETTINGS = cl("render ... with imageSmoothingEnabled false / image-rendering pixelated, composited over #172336, geometryMatches true", "consumer_fact_original", "display.filter nearest and background #172336 are declared identically in the original (line 9) and successor (line 13) modules; the fixture applies them; owner link: BRIEF line 3 nearest scale on the dark panel", [V_DISPLAY, S_DISPLAY, F_SMOOTH, I_PIXELATED, F_GATE, B3_INSPECT], "integration")
SCALES = cl("the live cells (scale 3) and the state-matrix cells (scale 1 and 3)", "fixture_fact", "fixture: matrix at 1 and display.scale, live at display.scale; owner link BRIEF line 3 1x and 3x", [F_MATRIX, F_LIVE, B3_INSPECT], "integration")
START_INFERENCE = lambda held: cl(("the held cell" if held else "the mark") + " ... distinguishable ... from the preserved Start triangle", "inference", "idle resolves to Start in the same status cells through both consumers in the original module (lines 3, 10-11) and the successor (lines 7, 27-28); 'distinguishable without colour alone' read over the view's status set; BRIEF line 3 'Preserve the existing vector Start control' only fixes the Start bytes (D4 settled); assignment step 3 calls it a shared-consumer inference", [V_IDLE, V_CONSUMERS, S_IDLE, S_CONSUMERS, A_STEP3_START, CC_D4], "view status set", "S11" if held else None)

criteria_classification = [
    crit("successor-01.working.q.geometry", [
        cl("Decode assets/working.png as exactly 64x16: four horizontal 16x16 cells at x=0,16,32,48", "owner", "BRIEF line 3 (16x16 cells, four horizontal frames); the original module already fixes frames 4 and cell [16,16], so this does not depend on adopting the successor module", [B3_CELLS, B3_FRAMES, V_RUNNING, V_DISPLAY, P_GEOM], "whole sheet, both preferences"),
        cl("with no gutters or added canvas between or around the cells (transparent margin inside a cell is composition, not padding)", "fixture_fact", "fixture geometry gate width == 16*frames; margins-versus-padding distinction preserved (r2); in-cell transparent margins are never rejected", [F_GATE], "whole sheet"),
        cl("Consumer basis: src/queue-view-successor.ts declares running frames 4 ..., display.cell [16,16] and frameMs 100", "consumer_fact_successor_proposed", "true of the proposed module; equally true of the unchanged original module (lines 4, 9), which is the independent basis", [S_RUNNING, S_DISPLAY, V_RUNNING, V_DISPLAY], "descriptive", "S7"),
        cl("the successor fixture draws only when width == 16*frames ..., slices frame*16,0,16,16 and derives the frame from frameAt() (floor(elapsed/100) mod 4 when animating; the held cell otherwise)", "fixture_fact", "descriptive of the proposed fixture and module; not a rejection clause on the art", [F_PAINT, S_FRAMEAT], "descriptive", "S7"),
    ]),
    crit("successor-01.working.q.transparent-exterior-measured", MEASURED_CLAUSES("every Working cell incl. the held cell", True)),
    crit("successor-01.working.q.transparent-exterior-visual", VISUAL_TRANSP("whole Working sheet", True) + [
        cl("The rejected generated frame whose background held 193 opaque #808080 pixels is the failure class, not the definition of the rule", "measured", "historical observation (live.working-animation-01.review.verdict.1) used as an example only", [CC_D1], "example"),
    ]),
    crit("successor-01.working.q.frame-assembly", [
        cl("For the successor the candidate sheet is the existing assets/working.png (sha256 cf101610...) ... no assembly step occurs and this clause is satisfied vacuously", "measured", "assets/working.png sha256 cf101610... equals the retained artifact of live.working-animation-motion-01.candidate (same hash); reuse authorised by assignment step 4 when the new criteria are satisfied", [A_STEP4_REUSE], "reuse case"),
        cl("the retained record must still name the exact candidate bytes and their provenance (byte-identical to accepted live.working-animation-motion-01.candidate; cells equal cw^k(seed) on alpha and visible RGBA)", "expert_choice", "PIXL evidence discipline (provenance record); the cw^k(seed) fact is measured True by the proposal and by me; the construction itself remains a scoped proposal", [K_EVIDENCE, jcite("my-measurements", "cells_1_3_equal_cw_k_cell0_alpha_and_visible_rgba", [True, True, True])], "reuse case; provenance only"),
        cl("If a future provider result is not already the exact 64x16 four-cell sheet, the retained assembly record names the exact source frames or cell rectangles in play order and every delivered cell is a lossless copy ...; all raw provider outputs are retained", "assignment_process", "actual source: AUTHORING-STAGE.md lines 31-32 ('retain the exact intended frame-selection/assembly policy and its separate review obligations'); the proposal cites FOCUSED-SUCCESSOR.md lines 40-43, which do not state this policy", [AS_ASSEMBLY, A_STEP4_REUSE], "conditional on any new assembly", "S3"),
        cl("(a deliberately repeated phase is allowed when the record says so) ... identical alpha everywhere and identical RGBA where alpha>0 (RGB of alpha-0 pixels is not significant)", "non_restriction", "r2 bounds on 'lossless' and 'duplication' (settled)", [CC_D1], "conditional"),
    ]),
    crit("successor-01.working.q.activity-not-success", [
        cl("the running loop ... read[s] as ongoing activity and not as completion", "owner", "BRIEF line 3; PLAR line 422 'without implying success'; PLAR 560-570 state_meaning", [B3_ACTIVITY, P422_NOSUCCESS, P_MEANING], "whole asset"),
        cl("and each individual frame read as ongoing activity and not as completion: no frame forms a check mark or another success-like terminal pose", "expert_choice", "per-frame reading of frames shown singly is the specialist's extension (basis admits it); for the held cell the single-frame reading is now caller-required (PLAR 422) and bound by stationary-meaning; for cells 1-3 it remains an expert clause yet sits inside a requirement-labelled check", [B3_ACTIVITY, P_MEANING, F_CREATE, K_RECIPE], "cells 1-3 singly: expert; held cell: caller update", "S4"),
        cl("(beside the exact Ready baseline as the comparison method)", "method", "adopted baseline decision; BRIEF line 9 fixes the success motif", [P_STYLE, B9_CHECK], "method"),
        cl("Viewed at 1x and 3x nearest on #172336", "owner", "BRIEF line 3", [B3_INSPECT], "review conditions"),
    ], "expert clause 'avoid frames that read as the Start arrowhead or paired pause bars' is correctly labelled proposal (r2 settled)"),
    crit("successor-01.working.q.motion-continuity", [
        cl("play the actual four frames at the consumer's 100 ms per frame including the fourth-to-first wrap, at 1x and 3x on #172336", "owner", "BRIEF line 3 (four frames, 100 ms); frameMs 100 in both modules; PLAR delivery check 'Play the loop at 100 ms per frame and inspect the fourth-to-first transition'", [B3_FRAMES, V_DISPLAY, S_DISPLAY, P_ANIM, P_DELIV_WRAP, B3_INSPECT], "whole sheet under normal motion"),
        cl("the strip plays as one continuous activity loop with no visible discontinuity at the fourth-to-first wrap", "owner", "BRIEF line 3 'loop ... communicate activity' by reasonable reading; D2 settled: this is the required outcome, pacing is expert", [B3_ACTIVITY, P_DELIV_WRAP, CC_D2, R2_D2], "whole sheet under normal motion"),
        cl("All four frames remain in the sheet and in play under normal motion; the reduced-motion hold does not remove or reorder them", "caller_update", "the update is additive: BRIEF line 3 four frames at 100 ms stays required; AUTHORING-UPDATE lines 5-10 retain the older plan; assignment step 2 keeps all four frames at 100 ms", [B3_FRAMES, U_RETAIN, A_STEP2], "both preferences"),
        cl("[evidence route] saved views / actual playback", "fixture_fact", "the fixture's timeline samples are synthetic frame-boundary stills built with makeCell(..., elapsed) and check.py only compares frame indices; no artefact of actual playback exists, so 'play the actual four frames' needs a named viewing route (live page under normal motion, or an assembled viewing aid labelled as such)", [F_TIMELINE_SYNTH, C_TIMELINE, C_SCOPE, K_ROUTE], "temporal evidence", "S5"),
    ], "expert clauses (stable centre/volume via family.working.contract li='%s'; even pacing/no near-hold = specialist; cluster count = construction) are labelled proposal; D2 faithfully applied" % working_contract_li.replace("\n", " ")[:160]),
    crit("successor-01.working.q.style-coherence", STYLE_CLAUSES("Working sheet incl. the held cell")),
    crit("successor-01.working.q.consumers-normal-motion", [
        CONSUMER_ROUTE,
        cl("with the preference resolving to normal, exercise started -> running through stateAfter", "consumer_fact_original", "src/queue.ts stateAfter('started') = 'running'", [Q_STATE], "integration"),
        cl("both statusCell and compactStatus return the identical descriptor {label Working, path assets/working.png, frames 4, still 0, motion normal, animate true, holdFrame null}", "consumer_fact_successor_proposed", "label/path/frames are facts of the unchanged original module (line 4); still/motion/animate/holdFrame are the PROPOSED module's descriptor shape (lines 16, 20-23); 'identical through both consumers' is the outcome the assignment requires (step 4: both consumers)", [V_RUNNING, S_RUNNING, S_DESCRIPTOR, S_DESCRIBE, A_STEP4_BOTH, C_IDENTICAL], "this successor implementation", "S6"),
        RENDER_SETTINGS, SCALES,
        cl("the capture timeline reports frame indices 0,0,1,1,2,2,3,3,0 at elapsed 0,99,100,199,200,299,300,399,400 ms (floor(elapsed/100) mod 4; wrap at 400 ms)", "checker_fact", "synthetic sampling: the timeline paints fresh cells at chosen elapsed values; check.py asserts frame == floor(elapsed/100) mod 4 and frames_seen == {0,1,2,3}; this is frame-index arithmetic, not playback", [F_TIMELINE_SYNTH, C_TIMELINE, C_CYCLE], "mechanical temporal evidence"),
        cl("and the live requestAnimationFrame loop is observed cycling through all four cells", "checker_fact", "NOT asserted by check.py: each live cell is sampled once (view.mjs line 157) and check.py line 140 checks that single frame against elapsed with a boundary tolerance; cycling through all four cells is asserted only on the synthetic timeline (line 164)", [F_LIVE_SAMPLE, C_LIVE_ONE, C_CYCLE], "temporal evidence", "S5"),
        cl("wall-clock frame duration is not measured and not claimed", "honest_limit", "correct; the owner's 100 ms is evidenced as the consumer constant plus frame-index arithmetic; actual cadence needs viewing", [S_DISPLAY], "temporal evidence"),
    ]),
    crit("successor-01.working.q.stationary-cell-identity", [
        cl("The stationary Working symbol is cell 0 of assets/working.png: the crop (0,0,16,16) ... the cell declared by statusVisuals.running.still = 0 and painted when animate is false", "expert_choice", "P1 is the specialist's proposal (assessing the assignment's suggested option, lines 18-23); still = 0 and the hold path are facts of the PROPOSED module", [A_STEP2, S_RUNNING, S_STILL, S_DESCRIBE, S_FRAMEAT], "the held cell under reduced motion"),
        cl("visible pixels 32, three 4-connected components with boxes [[5, 3, 10, 5], [12, 6, 14, 11], [3, 10, 8, 14]], visible box [3, 3, 14, 14], mass centroid [7.906, 9.0] ..., alpha histogram {'0': 224, '255': 32}; cell 0 equals the accepted seed", "measured", "reproduced independently by me on cf101610... frame 0 (zero-based, half-open boxes, centroid in pixel-edge coordinates): identical values; cell 0 == seed 21f5baca... on alpha and visible RGBA: True", [jcite("my-measurements", "images.working cell 0.centroid_edge", [7.906, 9.0]), jcite("my-measurements", "cell0_equals_seed_alpha_and_visible_rgba", True)], "cell 0 of cf101610..."),
        cl("if `still` changes, the identity record and those visual verdicts must be redone", "expert_choice", "evidence discipline: visual verdicts bind to the pixels actually painted", [K_EVIDENCE], "process"),
    ]),
    crit("successor-01.working.q.stationary-distinct-ready-paused", [
        cl("the held cell is distinguishable from the Ready mark ... and from the Paused mark", "caller_update", "authoring-plar.txt line 422; AUTHORING-UPDATE.md lines 2-4", [P422, U_REQ], "held cell vs Ready and Paused"),
        cl("by shape or structure alone ... in colour and in a non-colour comparison", "owner", "for Paused: BRIEF line 7 (Paused distinguishable from activity without colour alone; mutual). For Ready: not an owner line; a caller-adopted method already present in the original distinction criterion (grayscale comparison) and an inference from the line-7 pattern", [B7_PAUSED, B7_KEEP], "Paused pair: owner; Ready pair: inference/method", "S10"),
        cl("and does not read as completion or as pause", "owner", "BRIEF line 3 'without looking like success'; pause by reasonable reading of BRIEF line 7 (mutual)", [B3_ACTIVITY, B7_PAUSED], "held cell"),
        cl("Viewed stationary (no animation) at 1x and 3x nearest on #172336", "owner", "BRIEF line 3 inspection; stationary per the caller update", [B3_INSPECT, P422], "review conditions"),
        cl("Grayscale is the specialist's method; equivalent non-colour comparisons satisfy it", "method", "non-colour comparison method, correctly labelled", [], "method"),
    ]),
    crit("successor-01.working.q.stationary-distinct-retry-start", [
        cl("the held cell is distinguishable by shape or structure alone from the Retry mark ... and does not read as failure/retry", "inference", "BRIEF line 3 'Error/retry must be distinguishable without color alone' is stated for Retry; mutual distinction with the held cell (now a status cell) is a reasonable reading, not an owner line; basis says so, label says 'requirement'", [B3_RETRY, B7_PAUSED], "held cell vs Retry", "S11"),
        START_INFERENCE(True),
        cl("Viewed stationary at 1x and 3x nearest on #172336, in colour and in a non-colour comparison", "owner", "BRIEF line 3 inspection conditions", [B3_INSPECT], "review conditions"),
        cl("(assets/start.svg as rendered in the idle cell)", "honest_limit", "the proposal's Start comparison used a rasterised SVG as an aid; the fixture renders the SVG; browser rendering of Start has not been viewed for the successor", [F_SCOPE], "evidence limit"),
    ]),
    crit("successor-01.working.q.stationary-meaning", [
        cl("the held cell reads as the Working status's own symbol: it does not read as success (no check mark or terminal pose)", "owner", "BRIEF line 3 'without looking like success'; PLAR line 422 'without implying success'", [B3_ACTIVITY, P422_NOSUCCESS], "held cell"),
        cl("and does not read as pause", "caller_update", "PLAR line 422 distinct from Paused; BRIEF line 7 mutual", [P422, B7_PAUSED], "held cell"),
        cl("Viewed stationary at 1x and 3x on #172336 with its consumer label present", "method", "label rendering is a fixture/consumer fact (view.mjs line 62); judging only with the label present weakens the glyph reading BRIEF line 3 asks for ('readable silhouettes'); judge both with and without the label", [F_LABEL, B3_SILH], "method", "S2"),
        cl("it is recognisably one phase of the Working loop so that switching the preference while the page is open changes motion, not identity", "expert_choice", "this is the P1 design rationale (also listed in expert_clauses as a proposal) written into the required check; no owner or caller line requires the stationary symbol to be a loop phase; PLAR 422 requires only a stationary symbol distinguishable from Ready and Paused", [P422, A_STEP2, K_RECIPE, K_TEST], "P1 candidate only", "S1"),
        cl("[basis] a frozen spinner communicates 'in progress / busy' by UI idiom but can also read as 'stalled'", "honest_limit", "correct and necessary; see reduced_motion_assessment.stalled_reading_limit", [], "held cell"),
    ]),
    crit("successor-01.working.q.reduced-motion-consumer-mapping", [
        CONSUMER_ROUTE,
        cl("with the preference resolving to reduced ((prefers-reduced-motion: reduce) matches)", "assignment_process", "FOCUSED-SUCCESSOR step 4 'respect prefers-reduced-motion and changes while open' fixes the preference mechanism (the caller update itself left 'reduced-motion mode' open); the query string is the proposed module's constant", [A_STEP4_PREF, S_QUERY, S_MOTION], "successor"),
        cl("both statusCell and compactStatus return the identical descriptor {label Working, path assets/working.png, frames 4, still 0, motion reduced, animate false, holdFrame 0}; under normal both return {..., motion normal, animate true, holdFrame null}", "consumer_fact_successor_proposed", "outcome (one stationary symbol through both consumers; mapping confirmed) = PLAR 422 + assignment step 4; the descriptor field shape (still/motion/animate/holdFrame) is the proposed module's design (lines 16, 20-23), revisable", [P422_MAPPING, A_STEP4_BOTH, S_DESCRIPTOR, S_DESCRIBE, C_IDENTICAL], "this successor implementation", "S6"),
        cl("The sheet geometry stays 64x16 with frames 4 under both preferences (frames is the sheet's cell count, never changed by the preference)", "owner", "BRIEF line 3 four frames; original module frames 4; successor comment line 14", [B3_FRAMES, V_RUNNING, S_STILL], "both preferences"),
        cl("every Working cell (live 3x, matrix 1x and 3x) paints cell index holdFrame = still = 0 and the capture timeline reports frame 0 at every sample point (0..400 ms); no animation loop repaints Working cells", "checker_fact", "fixture animates only descriptors with animate true; check.py asserts the live cell holds the still cell and the timeline never leaves frame 0; outcome = caller update (stationary)", [F_ANIMATE, C_LIVE_HOLD, C_HOLD, P422], "integration under reduced"),
        cl("The static members (Start, Ready, Paused, Retry) resolve animate false / holdFrame 0 under both preferences with frames 1", "consumer_fact_successor_proposed", "describe(): animate = motion === 'normal' && frames > 1", [S_GATE, S_DESCRIBE], "descriptive"),
        cl("The default preference source is matchMedia('(prefers-reduced-motion: reduce)') consulted by both consumers through motionPreference(); an explicit motion argument overrides it identically for both", "consumer_fact_successor_proposed", "proposed module lines 17-19, 27-28", [S_MOTION, S_CONSUMERS], "descriptive"),
    ], "notes correctly say the mapping is the caller's proposal adopted by the specialist as the recommended mapping; M3 not recommended"),
    crit("successor-01.working.q.live-preference-switch", [
        cl("With the page open and Working shown ..., change the preference in the same page session: ... every Working cell in both consumers ... is re-derived from the same consumer under the new preference and repainted in place ... with no reload", "assignment_process", "FOCUSED-SUCCESSOR step 4 'changes while open', step 6 'switching the preference in the same session', step 3 'live preference-switch acceptance'", [A_STEP4_PREF, A_STEP6_SWITCH, A_STEP3_LIVE, F_REFRESH, F_CHANGE], "successor; same page session"),
        cl("to the held cell (animate false, frame == holdFrame == 0) when the preference becomes reduced, and back to cycling (animate true, holdFrame null, all four cells observed) when it returns to normal", "consumer_fact_successor_proposed", "descriptor-shape binding as in S6; 'all four cells observed' after restore is asserted only on the synthetic timeline of the normal-restored phase, not on the live loop", [S_DESCRIBE, C_SWITCH, C_RESUME, C_CYCLE], "this successor implementation", "S6"),
        cl("one sessionId across all phases, the change event recorded with from/to and the repainted cell list, and the live Working cells among the repainted cells", "checker_fact", "fixture sessionId and preferenceEvents; check.py [switch] assertions", [F_SESSION, C_SESSION, C_SWITCH], "evidence mechanism"),
        cl("Other states repaint unchanged", "checker_fact", "NOT asserted by check.py: the [switch] block filters repainted entries to state == 'running' only; the as-launched startup phase (--force-prefers-reduced-motion) also has no expected-motion assertion (lines 67-69)", [C_SWITCH_RUNNING, C_PHASES, CAP_PHASES], "evidence gap", "S12"),
    ]),
    crit("successor-01.retry.q.geometry", [
        cl("Decode assets/error-retry.png as exactly one static 16x16 frame", "owner", "BRIEF line 3 'Ready and Retry are static images', 16x16 cells; BRIEF line 7 'its purpose is unchanged'; original module frames 1", [B3_STATIC, B3_CELLS, B7_PURPOSE, V_RETRY, S_RETRY], "whole Retry asset"),
        cl("no strip, animation or extra canvas", "fixture_fact", "fixture geometry gate (also the original fixture); restates 'static' and frames 1", [F_GATE], "whole Retry asset"),
    ]),
    crit("successor-01.retry.q.transparent-exterior-measured", MEASURED_CLAUSES("Retry", False)),
    crit("successor-01.retry.q.transparent-exterior-visual", VISUAL_TRANSP("whole Retry asset", False)),
    crit("successor-01.retry.q.retry-meaning-without-color", [
        cl("the mark reads as failed work with a retry action", "owner", "BRIEF line 3 'Error/retry'; BRIEF line 7 'its purpose is unchanged'; consumer label Retry", [B3_RETRY, B7_PURPOSE, V_RETRY], "whole Retry asset"),
        cl("identifiable by shape alone against Ready, every Working frame including the held cell, Paused", "owner", "BRIEF line 3 'distinguishable without color alone'; 'including the held cell' is a reasonable reading because the successor shows it as a status cell (PLAR 422)", [B3_RETRY, P422], "whole Retry asset"),
        START_INFERENCE(False),
        cl("it must not be confusable with the Working activity loop or its held cell", "owner", "restates the shape-alone clause for the closest pair", [B3_RETRY], "whole Retry asset"),
        cl("No specific retry motif (such as an arrow) is required", "non_restriction", "the PLAR retry motif is a proposal (settled in r2)", [CC_D4], "whole Retry asset"),
        cl("in colour and in a non-colour comparison (grayscale or binarized silhouettes)", "method", "method, correctly labelled", [], "method"),
    ]),
    crit("successor-01.retry.q.style-coherence", STYLE_CLAUSES("Retry asset")),
    crit("successor-01.retry.q.consumers", [
        CONSUMER_ROUTE,
        cl("exercise error -> failed through stateAfter under both preferences", "consumer_fact_original", "src/queue.ts stateAfter('error') = 'failed'; both preferences per assignment step 4", [Q_STATE, A_STEP4_PREF], "integration"),
        cl("both statusCell and compactStatus resolve the identical descriptor {label Retry, path assets/error-retry.png, frames 1, still 0, animate false, holdFrame 0}", "consumer_fact_successor_proposed", "label/path/frames: original module line 7 (BRIEF line 7: failure visual moved to the path in the updated view); still/animate/holdFrame: proposed module shape", [V_RETRY, S_RETRY, S_DESCRIBE, B7_PURPOSE], "this successor implementation", "S6"),
        RENDER_SETTINGS, SCALES,
        cl("no animation loop runs (frames 1)", "consumer_fact_successor_proposed", "describe() frames > 1 gate; fixture animate() only when descriptor.animate", [S_GATE, F_ANIMATE], "integration"),
    ]),
    crit("successor-01.paused.q.geometry", [
        cl("Decode assets/paused.png as exactly one static 16x16 frame", "owner", "BRIEF line 7 (paused status image; keep display requirements) and line 3 (16x16 cells); original module frames 1", [B7_KEEP, B3_CELLS, V_PAUSED, S_PAUSED], "whole Paused asset"),
        cl("no strip, animation or extra canvas", "fixture_fact", "fixture geometry gate; restates frames 1", [F_GATE], "whole Paused asset"),
    ]),
    crit("successor-01.paused.q.transparent-exterior-measured", MEASURED_CLAUSES("Paused", False)),
    crit("successor-01.paused.q.transparent-exterior-visual", VISUAL_TRANSP("whole Paused asset", False) + [
        cl("The rejected opaque magenta intermediate is the failure class, not the definition of the rule", "measured", "historical observation (live.paused-02.review.verdict.1) as example only", [CC_D1], "example"),
    ]),
    crit("successor-01.paused.q.pause-meaning-without-color", [
        cl("the mark reads as paused work", "owner", "BRIEF line 7", [B7_PAUSED], "whole Paused asset"),
        cl("identifiable by shape alone against Ready (completion), every Working frame including the held cell (activity), Retry", "owner", "BRIEF line 7 names activity, completion and retry; the held cell is the stationary form of activity, so its inclusion is owner-grounded here", [B7_PAUSED, P422], "whole Paused asset"),
        START_INFERENCE(False),
        cl("No specific pause motif (such as paired bars) is required", "non_restriction", "the PLAR paused motif is a proposal (settled)", [CC_D4], "whole Paused asset"),
        cl("in colour and in a non-colour comparison (grayscale or binarized silhouettes)", "method", "method", [], "method"),
    ]),
    crit("successor-01.paused.q.style-coherence", STYLE_CLAUSES("Paused asset")),
    crit("successor-01.paused.q.consumers", [
        CONSUMER_ROUTE,
        cl("exercise pause -> paused through stateAfter under both preferences", "consumer_fact_original", "src/queue.ts stateAfter('pause') = 'paused'", [Q_STATE, A_STEP4_PREF], "integration"),
        cl("both statusCell and compactStatus resolve the identical descriptor {label Paused, path assets/paused.png, frames 1, still 0, animate false, holdFrame 0}", "consumer_fact_successor_proposed", "label/path/frames: original module line 5; still/animate/holdFrame: proposed module shape", [V_PAUSED, S_PAUSED, S_DESCRIBE], "this successor implementation", "S6"),
        RENDER_SETTINGS, SCALES,
        cl("no animation loop runs (frames 1)", "consumer_fact_successor_proposed", "describe() frames > 1 gate", [S_GATE, F_ANIMATE], "integration"),
    ]),
    crit("successor-01.delivery.q.continuity", [
        cl("Compare all four actual members together at 1x and 3x nearest on #172336 against the exact Ready baseline", "owner", "BRIEF line 3 'coherent pixel-art status assets' and inspection conditions; exact baseline = adopted caller decision", [B3_COHERENT, B3_INSPECT, P_STYLE], "collective delivery"),
        cl("coherent deliberate pixel treatment", "caller_adopted_decision", "approved_style_reference carry list", [P_STYLE], "family"),
        cl("readable visual weight coherent with the Ready baseline (identical stroke width or footprint is not required)", "owner", "BRIEF line 3 'coherent'; D3 applied verbatim from r2: coherence does not impose identical weight (assignment step 3)", [B3_COHERENT, CC_D3, R2_D3, A_STEP3_PACING], "family"),
        cl("perceptible cool-blue accent and transparent exteriors", "owner", "BRIEF line 3; role = perceptibility not extent", [B3_BLUE, B3_TRANSP, K_ROLE], "family"),
        cl("including Working's four frames, its actual 100 ms playback with the wrap under normal motion", "owner", "BRIEF line 3; temporal route must be named (S5)", [B3_FRAMES, P_DELIV_WRAP], "Working", "S5"),
        cl("and the held cell shown stationary under reduced motion", "caller_update", "PLAR line 422", [P422], "held cell"),
        cl("no exact palette, alpha, stroke, margin or copied completion-motif requirement", "non_restriction", "BRIEF line 3 no fixed palette; not_fixed list", [B3_PALETTE, P_STYLE], "family"),
    ], "notes report visible-pixel counts (W 32 / Ready 29 / Paused 60 / Retry 54) as observations, not a weight rule: correct"),
    crit("successor-01.delivery.q.distinction", [
        cl("Working (animated or held) never reads as success", "owner", "BRIEF line 3; PLAR 422", [B3_ACTIVITY, P422_NOSUCCESS], "collective"),
        cl("the held cell is distinct from Ready and from Paused by shape or structure alone", "caller_update", "PLAR 422 (distinguishable); 'shape or structure alone' for the Ready pair is method/inference (S10)", [P422, B7_PAUSED], "collective", "S10"),
        cl("Retry and Paused are each distinct from activity (including the held cell), completion and from each other by shape or structure alone", "owner", "BRIEF lines 3 and 7", [B3_RETRY, B7_PAUSED], "collective"),
        cl("the preserved Start triangle remains separately identifiable from every member including the held cell", "inference", "shared-consumer inference (D4 settled; caller disposition keep with corrected basis)", [V_IDLE, V_CONSUMERS, S_IDLE, S_CONSUMERS, CC_D4], "collective"),
        cl("including a grayscale/non-colour comparison", "method", "method already in the original criterion", [], "method"),
    ]),
    crit("successor-01.delivery.q.destination", [
        cl("Destination for the successor: src/queue-view-successor.ts + renderer-successor/ with the existing asset paths (...)", "assignment_process", "FOCUSED-SUCCESSOR step 4 names the successor files and 'explicitly identify the new destination'; BRIEF line 5 keeps the asset paths; the successor declares the same paths as the original", [A_STEP4_FILES, B5_PATHS, S_PATHS, V_RETRY], "successor destination"),
        cl("src/queue-view.ts, renderer/ and every existing asset byte remain unchanged (hashes compared against the retained baseline)", "assignment_process", "FOCUSED-SUCCESSOR step 4 'keep old src/queue-view.ts and renderer/ untouched'; check.py --baseline comparison", [A_STEP4_OLD, C_BASELINE], "successor destination"),
        cl("exercise all backend transitions (started, ok, error, pause, plus idle) through both statusCell and compactStatus under normal and reduced preferences", "consumer_fact_original", "src/queue.ts transitions; both consumers and both preferences per assignment step 4", [Q_STATE, A_STEP4_BOTH, A_STEP4_PREF], "integration"),
        cl("labels, frame counts (sheet geometry), horizontal slicing, frame index floor(elapsed/100) mod frames at the timeline sample points including the 400 ms wrap under normal and frame 0 at every sample under reduced (wall-clock duration not measured)", "checker_fact", "the original check said '100 ms timing'; the successor bounds it to frame-index arithmetic plus the consumer constant and states wall-clock is not measured (honest); the actual-playback leg belongs to motion-continuity and needs its route named (S5)", [C_TIMELINE, C_CYCLE, C_HOLD, S_DISPLAY], "temporal evidence", "S5"),
        cl("nearest sampling at scale 1 (state matrix) and 3 (state matrix and live cells), alpha compositing on #172336", "owner", "BRIEF line 3 1x/3x on the dark panel; display constants; check.py compositing tolerance one", [B3_INSPECT, S_DISPLAY, C_COMPOSITE], "integration"),
        cl("as the adopted destination-check method - recorded integer canvas placement matching the screenshot pixels", "method", "adopted method (recheck.decision.destination present in the context packet decisions); r2 labelled it method", [jcite("context", "decisions[0].id", "recheck.decision.destination")], "method"),
        cl("assets/start.svg byte hash unchanged", "owner", "BRIEF line 3 'Preserve the existing vector Start control' (this is the one place that sentence is the basis); check.py baseline list", [B3_START, C_BASELINE], "Start"),
        cl("the fixture executed the successor module and not the retained original", "checker_fact", "check.py lines 51-52", [C_MODULES], "evidence"),
    ]),
]
assert len(criteria_classification) == 29 and {c["id"] for c in criteria_classification} == set(prop_criteria)

# ---------------------------------------------------------------- defects
defects = [
    {"id": "S1", "severity": "blocking", "criterion_ids": ["successor-01.working.q.stationary-meaning"], "field": "check (last clause) / authority",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.stationary-meaning].check", "quote": "it is recognisably one phase of the Working loop so that switching the preference while the page is open changes motion, not identity"},
     "finding": "The P1 design rationale (hold a phase of the existing loop) is written into a requirement-labelled check. No owner or caller line requires the stationary symbol to be a loop phase: PLAR line 422 requires a stationary Working symbol distinguishable from Ready and Paused and a confirmed consumer mapping; FOCUSED-SUCCESSOR lines 18-23 call the hold-frame-zero option a proposed implementation, not an owner-imposed choice. The same sentence already appears in expert_clauses as a proposal, so the check duplicates a proposal as a requirement.",
     "discriminating_alternative": "P2 (a new static 16x16 'in progress' glyph, e.g. three dots, cool-blue, transparent exterior, clearly not a check and not bars) satisfies PLAR 422 and BRIEF line 3, yet the literal check rejects it because it is not 'one phase of the Working loop'.",
     "suggested_correction": "Either (a) scope the criterion explicitly to the P1 candidate ('for a held-cell candidate: ...') or (b) remove the clause from the check and keep it only in expert_clauses (proposal, scope 'P1 design'). Keep the required outcome: reads as Working's own symbol, not success, not pause. Do not rewrite the original proposal file; write the correction in a successor proposal artifact beside it.",
     "sources": [P422, A_STEP2, K_RECIPE, K_TEST]},
    {"id": "S2", "severity": "clarify", "criterion_ids": ["successor-01.working.q.stationary-meaning"], "field": "check (viewing condition)",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.stationary-meaning].check", "quote": "with its consumer label present"},
     "finding": "Evaluating the held cell's meaning only with the text label present makes the label do the semantic work; BRIEF line 3 asks for readable silhouettes and the compact consumer may show the glyph where the label is less prominent. The label is a fixture/consumer fact (view.mjs line 62), not a licence for the glyph.",
     "discriminating_alternative": "A held cell that reads as 'stalled' or ambiguous without the label but acceptable beside the word 'Working' passes the literal check; a reviewer judging the glyph alone would flag it.",
     "suggested_correction": "Judge the held cell both alone and beside its label at 1x and 3x; record both readings; the label is context, not a substitute. Keep the frozen-spinner limit explicit.",
     "sources": [F_LABEL, B3_SILH]},
    {"id": "S3", "severity": "clarify", "criterion_ids": ["successor-01.working.q.frame-assembly"], "field": "sources / basis",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.frame-assembly].sources[0]", "quote": "assignment lines 40-43 (assign-step4-reuse)"},
     "finding": "The assembly-record process requirement is cited to FOCUSED-SUCCESSOR.md lines 40-43, which say to reuse reviewed art and not to invent provider observations; they do not state a frame-selection/assembly policy. The actual source is AUTHORING-STAGE.md lines 31-32 ('retain the exact intended frame-selection/assembly policy and its separate review obligations'), which is absent from the proposal's 33-entry source index.",
     "discriminating_alternative": "Not an art alternative: a locator defect. A reviewer following the cited lines cannot verify the obligation.",
     "suggested_correction": "Add AUTHORING-STAGE.md (sha256 %s) to the source index and cite lines 31-32 for the assembly clause; keep FOCUSED-SUCCESSOR 40-43 for the reuse authorisation only." % SOURCE_INDEX["authoring-stage"]["sha256"],
     "sources": [AS_ASSEMBLY, A_STEP4_REUSE]},
    {"id": "S4", "severity": "clarify", "criterion_ids": ["successor-01.working.q.activity-not-success"], "field": "check / authority split",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.activity-not-success].check", "quote": "the running loop and each individual frame read as ongoing activity and not as completion: no frame forms a check mark or another success-like terminal pose"},
     "finding": "The basis and scope fields say the per-frame reading is an expert extension, but the literal check binds every individual frame under authority 'requirement'. Under the successor the per-frame reading is genuinely required for the held cell (PLAR 422, bound by stationary-meaning) but remains expert for cells 1-3, which are shown singly only for 100 ms.",
     "discriminating_alternative": "A four-frame loop whose cell 2, frozen alone, resembles a short tick stroke while the loop and the held cell 0 clearly read as activity: brief-conforming under normal motion (BRIEF line 3 binds the loop), rejected by the literal per-frame clause.",
     "suggested_correction": "Split: loop clause = owner requirement; held-cell single-frame reading = caller update (point to stationary-meaning); cells 1-3 singly = expert clause with its rationale (frame 0 painted at creation; 100 ms exposure). Mixed-authority clauses must be split per the kit's review guidance.",
     "sources": [B3_ACTIVITY, P_MEANING, F_CREATE, K_RECIPE]},
    {"id": "S5", "severity": "clarify", "criterion_ids": ["successor-01.working.q.consumers-normal-motion", "successor-01.working.q.motion-continuity", "successor-01.delivery.q.continuity", "successor-01.delivery.q.destination", "successor-01.working.q.live-preference-switch"], "field": "evidence_route / check (temporal evidence)",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.consumers-normal-motion].check", "quote": "the live requestAnimationFrame loop is observed cycling through all four cells"},
     "finding": "Temporal evidence is overclaimed in one place and unnamed in another. (a) check.py samples each live cell once (view.mjs line 157) and checks that one frame against elapsed with a boundary tolerance (line 140); 'cycling through all four cells' is asserted only for the synthetic timeline built by makeCell(..., elapsed) (view.mjs line 146; check.py line 164). (b) motion-continuity and delivery.continuity require playing 'the actual four frames at 100 ms' and judging the wrap, but no artefact of actual playback exists (the timeline PNGs are frame-boundary stills) and no viewing route is named; check.py's own scope says it does not judge animation quality. (c) destination/consumers correctly say wall-clock is not measured. The three legs (consumer constant frameMs 100 = mechanical; frame-index arithmetic = mechanical; actual playback = visual/temporal) must stay separate and each be routed; the r2 correction 'observed cycling' therefore has no checker support yet.",
     "discriminating_alternative": "A successor whose rAF loop stalls after the first paint while the synthetic timeline is still correct would pass every check.py assertion; the live single sample could even match by tolerance. The literal 'observed cycling' claim would be false yet the evidence route reports pass.",
     "suggested_correction": "Reword consumers-normal-motion to what check.py asserts (synthetic timeline cycles 0..3 with the 400 ms wrap; one live sample agrees with elapsed). Name the actual-playback route for motion-continuity/continuity: human viewing of the live fixture page under normal motion at 1x and 3x (recorded as a visual observation), optionally aided by an assembled 4-frame 100 ms preview labelled 'viewing aid, not fixture evidence'; or add a multi-sample live observation to the fixture/checker. Keep 'wall-clock not measured'.",
     "sources": [F_LIVE_SAMPLE, C_LIVE_ONE, F_TIMELINE_SYNTH, C_CYCLE, C_SCOPE, K_ROUTE, P_DELIV_WRAP]},
    {"id": "S6", "severity": "clarify", "criterion_ids": ["successor-01.working.q.consumers-normal-motion", "successor-01.working.q.reduced-motion-consumer-mapping", "successor-01.working.q.live-preference-switch", "successor-01.retry.q.consumers", "successor-01.paused.q.consumers"], "field": "check (descriptor equality) / authority",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.reduced-motion-consumer-mapping].check", "quote": "{label Working, path assets/working.png, frames 4, still 0, motion reduced, animate false, holdFrame 0}"},
     "finding": "Exact descriptor shapes (still, motion, animate, holdFrame) are bound under authority 'requirement'. label/path/frames are facts of the unchanged original module and BRIEF; still/motion/animate/holdFrame are the proposed successor module's design (lines 16, 20-23), which the assignment and the proposal's own source role call a revisable design proposal. The required outcomes are: both consumers resolve the same Working visual; under reduced motion it is stationary on the designated cell; under normal it cycles; static members stay static.",
     "discriminating_alternative": "A successor module that implements the hold as {frames: 4, hold: true} or exposes stillFrame instead of holdFrame, with identical rendering through both consumers and the same fixture behaviour: assignment- and brief-conforming, rejected by the literal descriptor equality.",
     "suggested_correction": "Keep the outcome clauses as requirements (PLAR 422, assignment step 4) and label the field-level descriptor equality as 'consumer-code fact of the proposed successor module; scope: this implementation; re-derive if the module changes'. check.py may keep asserting the exact shape as the implementation's own test.",
     "sources": [S_DESCRIPTOR, S_DESCRIBE, A_STEP4_BOTH, P422_MAPPING, K_LABEL]},
    {"id": "S7", "severity": "clarify", "criterion_ids": [c["id"] for c in proposal["criteria"] if c["authority"] == "requirement"], "field": "conventions.authority / per-criterion authority label",
     "locator": {"proposal_field": "conventions.authority", "quote": "'requirement' includes consumer-code behaviour, the caller's PLAR update and assignment process requirements where the basis says so"},
     "finding": "One label 'requirement' covers owner lines, the caller update, assignment process requirements, original-module facts and proposed-successor-module/fixture/checker facts. The basis strings often disambiguate, but the label is what a future plan carries into Q records; the kit says the label is an assertion to compare and that process, output and diagnostic clauses must stay distinct. For this successor the distinction between the unchanged original module and the revisable proposed module is consequential (S6).",
     "discriminating_alternative": "Not an art alternative; a labelling defect that hides S6-type promotions.",
     "suggested_correction": "Carry a per-clause class (as in this file's criteria_classification: owner / caller_update / assignment_process / consumer_fact_original / consumer_fact_successor_proposed / fixture_fact / checker_fact / measured / expert_choice / inference / method / non_restriction) in the successor proposal, keeping the PLAR label for the record and the class in the basis.",
     "sources": [K_LABEL, K_PROCESS]},
    {"id": "S8", "severity": "note", "criterion_ids": ["successor-01.working.q.transparent-exterior-measured"], "field": "check (construction clause)",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.transparent-exterior-measured].check", "quote": "(224 alpha-0 and 32 alpha-255 pixels per cell)"},
     "finding": "The counts are measured values of seed 21f5baca... (and of cf101610... cells), not part of the rule; written inside the rejection form they read as a fixed alpha census. Reference pixels establish observations, not mandatory counts.",
     "discriminating_alternative": "A future regenerated seed with 30 opaque pixels under the same rotation construction would satisfy 'alpha equals cw^k(seed)' yet contradict the parenthetical.",
     "suggested_correction": "Write '(for the current seed 21f5baca...: measured 224 alpha-0 / 32 alpha-255 per cell)'.",
     "sources": [K_REFERENCE, jcite("my-measurements", "images.working cell 0.alpha_histogram", {"0": 224, "255": 32})]},
    {"id": "S9", "severity": "note", "criterion_ids": ["successor-01.working.q.style-coherence", "successor-01.retry.q.style-coherence", "successor-01.paused.q.style-coherence"], "field": "check (accent relation)",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.style-coherence].check", "quote": "related to the Ready baseline and the preserved Start accent"},
     "finding": "BRIEF line 3 names 'the existing UI's cool blue accent'; relating it to the Start fill #70b9ed is an inference that Start is that accent's exemplar (the only colour source in this checkout). The role is perceptibility, not extent or exact hue; the check already says 'perceptible' and 'no exact hex', which is right.",
     "discriminating_alternative": "A member whose cool blue is perceptibly cool-blue and coherent with Ready but not visibly 'related' to #70b9ed (e.g. a steel-blue ramp) would pass the brief and arguably the check; the clause is loose enough not to reject it, hence note only.",
     "suggested_correction": "Label the Start-accent relation as an inference (basis: assets/start.svg fill #70b9ed observed) in the basis text.",
     "sources": [B3_BLUE, START_HEX, K_ROLE]},
    {"id": "S10", "severity": "note", "criterion_ids": ["successor-01.working.q.stationary-distinct-ready-paused", "successor-01.delivery.q.distinction"], "field": "check ('by shape or structure alone' for the Ready pair)",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.stationary-distinct-ready-paused].basis", "quote": "'By shape or structure alone' follows BRIEF line 7"},
     "finding": "BRIEF line 7's 'without relying on color alone' is stated for Paused (hence mutual for held-vs-Paused). For the held-vs-Ready pair the non-colour requirement is an inference from that pattern plus the caller-adopted grayscale method already in the original distinction criterion; the caller update (PLAR 422) says only 'distinguishable'.",
     "discriminating_alternative": "A held cell distinct from Ready only by hue with a check-like silhouette: it would already fail 'without looking like success', so no brief-conforming alternative is excluded in practice.",
     "suggested_correction": "State in the basis that the non-colour condition for the Ready pair is an inference/adopted method; no check change needed.",
     "sources": [B7_PAUSED, P422]},
    {"id": "S11", "severity": "note", "criterion_ids": ["successor-01.working.q.stationary-distinct-retry-start"], "field": "authority vs basis",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.stationary-distinct-retry-start].authority", "quote": "requirement (basis: 'Inference, not an owner line')"},
     "finding": "The label is 'requirement' while the basis says inference. This follows the settled D4 convention ('requirement by reasonable reading'), so it is not re-litigated; but the Retry direction and the Start inclusion for the stationary symbol are new, and the proposal itself asks the caller whether to adopt them (report.questions[1]).",
     "discriminating_alternative": "None needed for the Retry pair (distinguishability is symmetric). For Start: a held cell shaped like a filled right-pointing triangle would also fail the Working-not-Start identity by common sense; the risk is attribution, not rejection.",
     "suggested_correction": "Carry 'requirement by reasonable reading (inference over the view's status set)' into the check or Q basis so the bare label never stands alone; the caller answers the open question.",
     "sources": [A_STEP3_START, CC_D4, B3_RETRY]},
    {"id": "S12", "severity": "note", "criterion_ids": ["successor-01.working.q.live-preference-switch", "successor-01.working.q.reduced-motion-consumer-mapping"], "field": "check vs checker support",
     "locator": {"proposal_field": "criteria[id=successor-01.working.q.live-preference-switch].check", "quote": "Other states repaint unchanged"},
     "finding": "check.py's [switch] block inspects only repainted entries with state == 'running' (line 180); 'other states repaint unchanged' is not asserted. The evidence_route's as-launched run (--force-prefers-reduced-motion) has no expected-motion assertion in check.py (lines 67-69 map only the three default phases), so the startup-preference path would be unasserted.",
     "discriminating_alternative": "A regression that repaints Ready as frame 0 of a wrong sheet on the change event, or a startup path that ignores the launch preference, passes check.py.",
     "suggested_correction": "Either add the two assertions to check.py (static states keep animate false/holdFrame 0 on the change event; as-launched phase motion == reduced when forced) or label those clauses as caller visual observations on the reduced-phase screenshot.",
     "sources": [C_SWITCH_RUNNING, C_PHASES, CAP_PHASES]},
]
severity_counts = {s: sum(1 for d in defects if d["severity"] == s) for s in ("blocking", "clarify", "note")}
for d in defects:
    for cid in d["criterion_ids"]:
        assert cid in prop_criteria, cid

# ---------------------------------------------------------------- mapping check
mapping_check = {
    "all_20_present": True,
    "record_hashes_match": {"context_packet": True, "pixl_validate_this_session": True, "caller_request_review_export": True, "note": "pixl_validate on .pixl/assets/queue.ready/state.px returned valid, format 2, revision 88, hash 3484cf38...; its 20 Q record hashes equal the context packet, the caller's request-review export (sha256 %s) and every mapping row." % SOURCE_INDEX["rr-export"]["sha256"]},
    "original_checks_match_context": True,
    "carried_by_consistent": {"every_carried_by_exists": True, "every_carrier_carries_back_with_hash": True, "splits": {"authoring-01.working.q.transparent-exterior": 2, "authoring-01.retry.q.transparent-exterior": 2, "authoring-01.paused.q.transparent-exterior": 2}, "new_criteria_without_carries": new_ids, "count": "20 originals -> 23 carriers + 6 new = 29"},
    "rows": mapping_rows,
    "r2_applied": {
        "D1": "Faithful. Each transparent-exterior row is split into a measured record (authority observation; four-edge / >half-cell component = FLAG for visual review, 'NOT a rejection condition'; construction-scoped cw^k(seed) alpha equality as the only mechanical rejection form, Working only; 'No mechanical rejection rule is decidable for this static member' for Retry/Paused) and a visual deciding record ('no unintended matte, tile, plate, halo or fringe'; deliberate backing acceptable when recorded; partial alpha permitted). Text matches r2 revision_changes[0..2]. Minor: S8 (seed counts written as if part of the rule).",
        "D2": "Faithful. motion-continuity required outcome = 'one continuous activity loop with no visible discontinuity at the fourth-to-first wrap' at the consumer's 100 ms; 'evenly paced ... no near-hold' and 'stable cluster count / stepped quarter-turn phases' sit in expert_clauses labelled proposal with scopes 'specialist quality clause' and 'seed-rotation construction only'; stable centre/volume is labelled contract-bound expert clause. Expert pacing is not presented as the owner's 100 ms requirement.",
        "D3": "Faithful. delivery.continuity reads 'readable visual weight coherent with the Ready baseline (identical stroke width or footprint is not required)' exactly as r2 revision_changes[4]; the notes keep the pixel counts (32/29/60/54) as observations.",
        "D4": "Faithful. Every Start clause (retry-meaning, pause-meaning, delivery.distinction, and the new stationary-distinct-retry-start) rests on idle -> Start in the same status cells through both consumers, citing both the unchanged original module (lines 3, 10-11) and the successor (lines 7, 27-28), and explicitly denies 'Preserve the existing vector Start control' as the basis. Residual: the PLAR label stays 'requirement' with the inference in the basis (S11, consistent with the settled convention).",
    },
    "dropped_or_weakened_outcomes": [
        {"original_id": "authoring-01.working.q.consumers", "original_wording": "observed live 100 ms frame advance including the wrap", "successor_wording": "timeline frame indices ... and the live requestAnimationFrame loop is observed cycling through all four cells; wall-clock frame duration is not measured", "finding": "Not dropped, but the 'observed cycling' leg has no checker support (S5); the owner's 100 ms survives as consumer constant + frame-index arithmetic + a still-unnamed viewing route. Settled as a route change in r2; the route must now actually be named.", "defect": "S5"},
        {"original_id": "authoring-01.delivery.q.destination", "original_wording": "100 ms timing", "successor_wording": "frame index floor(elapsed/100) mod frames at the timeline sample points ... (wall-clock duration not measured)", "finding": "Same temporal bounding; honest; see S5.", "defect": "S5"},
    ],
    "owner_outcomes_checked_present": ["16x16 cells", "four horizontal frames at 100 ms (normal motion)", "Ready/Retry static", "transparent backgrounds (visual deciding + measured diagnostic)", "readable silhouettes", "cool blue accent (perceptible)", "no fixed palette imposed", "1x/3x on the dark panel", "activity not success (loop and held cell)", "Error/retry distinguishable without colour alone", "Paused distinguishable from activity/completion/retry without colour alone", "assets at the view's paths", "Start preserved (byte hash)", "coherent family", "caller update: stationary Working symbol distinct from Ready and Paused with confirmed consumer mapping"],
}

# ---------------------------------------------------------------- reduced-motion assessment (my own viewing; preliminary; not acceptance)
views = my_meas["views"]
reduced_motion_assessment = {
    "option": "P1: hold cell 0 (crop (0,0,16,16), zero-based half-open) of the existing assets/working.png sha256 cf101610... under reduced motion; all four cells at 100 ms under normal motion. Assessed as the assignment's suggested option (FOCUSED-SUCCESSOR lines 18-23), a proposed implementation, not an owner motif/frame choice.",
    "viewed": [{"image": v["path"], "sha256": v["sha256"], "scale": int(k.split("-")[-2].rstrip("x")), "mode": "grayscale" if k.endswith("gray.png") else "colour", "viewer": "PIXL (this child) via the host image display of the file; preliminary; not acceptance"} for k, v in views.items()]
              + [{"image": SOURCES["views-pair"][0], "sha256": SOURCE_INDEX["views-pair"]["sha256"], "scale": "1x/3x/12x composite", "mode": "colour+grayscale", "viewer": "PIXL (this child) viewed the prior specialist's pair view for comparison; preliminary"}],
    "view_layout": my_meas["view_order"],
    "measurements": {
        "file": SOURCES["my-measurements"][0], "sha256": SOURCE_INDEX["my-measurements"]["sha256"], "convention": my_meas["convention"],
        "held_cell_0": my_meas["images"]["working cell 0"],
        "ready": {k: my_meas["images"]["assets/ready-confirmed.png"][k] for k in ("sha256", "components", "alpha_histogram", "centroid_edge")},
        "paused": {k: my_meas["images"]["assets/paused.png"][k] for k in ("sha256", "components", "alpha_histogram", "centroid_edge")},
        "retry": {k: my_meas["images"]["assets/error-retry.png"][k] for k in ("sha256", "components", "alpha_histogram", "centroid_edge")},
        "retry_transparent_pixels_inside_bbox": my_meas["retry_transparent_pixels_inside_bbox"],
        "cells_1_3_equal_cw_k_cell0": my_meas["cells_1_3_equal_cw_k_cell0_alpha_and_visible_rgba"],
        "cell0_equals_seed": my_meas["cell0_equals_seed_alpha_and_visible_rgba"],
        "agreement_with_proposal": "component boxes, centroid [7.906, 9.0], alpha histogram {0:224, 255:32}, 12 components / 128 visible pixels for the sheet, 0 fractional-alpha pixels (pixl_asset_check alpha=full on all four files) all agree with specialist-measurements.json and the proposal's reduced_motion_design.measured_facts.",
    },
    "readability_findings_preliminary": {
        "label": "PIXL's own viewing of the files listed above; preliminary; not acceptance; not fixture captures",
        "held_cell_1x": "Reads as a small broken ring of three fragments (top 5x2 cluster, right 2x5 cluster, bottom-left 5x4 cluster) around a fully transparent 4x4 centre; the 2-3 px gaps survive at 1x; luminance 135-161 on the panel's 34 gives ample contrast. It is legible as the static 'spinner / loading' idiom. The mass sits bottom-left of centre (centroid 7.9, 9.0 vs 8, 8), which reads as a snapshot of rotation rather than a designed static emblem.",
        "held_cell_3x": "Unambiguous: three arcs of a ring; two-tone shading per fragment is visible and deliberate (selective, intentional shading consistent with the family's full-alpha contract; no resampling blur; 0 fractional-alpha pixels).",
        "held_cell_12x": "Cluster construction is clean and stepped; no stray pixels; the fragments are unequal (9/8/15 px), which is what makes the rotation legible across phases and also what makes any single phase asymmetric.",
        "vs_ready": "Distinct at 1x and 3x in colour and grayscale: a single diagonal stroke with asymmetric arms (29 px, one component, luminance 173) versus ring fragments (32 px, three components). Similar mass, different structure; weight coherent with the baseline.",
        "vs_paused": "Distinct at both scales: two solid 3x10 bars (60 px, two components) versus a gappy ring; Paused is the heaviest member; identical weight is not required (D3).",
        "closest_pair": "held cell versus Retry (see held_vs_retry).",
        "selective_aa_note": "No anti-aliasing is present in any member (all alpha 0/255), so nothing here tests the selective-AA permission; the permission stays in the criteria and is not contradicted by the art.",
    },
    "held_vs_retry": {
        "structure": "Retry: one 54-px component, a heavier near-closed ring with an arrowhead at the top-right and a notch; 66 transparent pixels inside its 10x12 bounding box (open centre). Held cell: 32 px in three components with 2-3 px gaps and a wide empty centre, no arrowhead, about 60% of Retry's mass.",
        "1x_colour": "Distinguishable: Retry is visibly denser and closed with a point; the held cell is sparse and gapped. Both are round, so this is the pair a reviewer must look at.",
        "1x_grayscale": "Still distinguishable by density and gaps, but subtle; I concur with the proposal that this is the closest pair and that the caller's own viewing of actual fixture captures at 1x grayscale should target it specifically.",
        "3x": "Unambiguous.",
        "concurrence": "I agree with the proposal's preliminary PASS-with-caveat; this is my own viewing of my own composites and of the prior pair view, not a verdict on fixture output.",
    },
    "stalled_reading_limit": "Honest limit, correctly recorded by the proposal and confirmed here: frozen, the held cell carries no motion cue; its off-centre mass reads as 'caught mid-turn', which is a weak activity cue and equally a 'stuck' cue. Beside the word 'Working' (both consumers render the label) it reads as busy; alone it can read as stalled or as a generic loading mark. No source requires the stationary symbol to convey motion; the owner requirements that bind are non-success, non-pause and distinction from Ready/Paused. Whether frozen-spinner semantics are acceptable is an owner/caller decision, not a criterion outcome.",
    "alternatives": [
        {"option": "another cell (1-3)", "view": "Equivalent by construction (quarter-turns of cell 0; verified cells 1-3 == cw^k(cell 0)); cell 0 has the cleanest provenance (== accepted seed) and matches the proposed still: 0. Agree."},
        {"option": "P2 new static 'in progress' glyph (e.g. three dots)", "view": "Stronger static semantics than a frozen spinner (an ellipsis conventionally means 'pending/in progress'), clearly distinct from check/bars/ring/triangle; costs one generation, a new descriptor path or key, and breaks the identity between animated and stationary forms (the preference switch would swap symbols). At 1x three 2x2 dots risk reading as a dashed line. Viable fallback if the owner rejects frozen-spinner semantics; the criteria must not exclude it (S1)."},
        {"option": "P3 new static gapped ring", "view": "Too close to the delivered Retry ring; would weaken the Retry distinction. Agree: not recommended."},
        {"option": "M3 reduced-motion queue state", "view": "Wrong layer: motion preference is presentation; src/queue.ts stays unchanged. Agree: not recommended."},
    ],
    "recommendation": {"label": "SPECIALIST PROPOSAL (round-1 concurrence; adoption is the caller's decision; no acceptance implied)", "text": "P1 remains the reasonable choice: no new art, one source of truth, both consumers share the mapping, the switch changes motion not identity. Conditions: (1) the owner/caller accepts frozen-spinner semantics (stalled-reading limit recorded); (2) the stationary-meaning criterion is corrected so it does not exclude P2 (S1) and is judged with and without the label (S2); (3) the caller views actual fixture reduced-phase captures of the held cell beside Retry at 1x grayscale before any acceptance; (4) the temporal evidence route for normal motion is named (S5)."},
    "owner_decisions_open": ["accept frozen-spinner semantics for the stationary Working symbol (or choose P2 with one generation)", "adopt distinction from Retry and Start for the stationary symbol as an inference-based requirement (proposal's open question)", "whether meaning is judged with the label present only, or also alone (S2)"],
    "fixed_by_assignment_not_owner": ["reduced-motion mode = prefers-reduced-motion media query and live switching (FOCUSED-SUCCESSOR step 4/6)", "successor destination files (step 4)"],
}

# ---------------------------------------------------------------- unavailable / not claimed
unavailable_or_not_claimed = [
    "Successor fixture capture: work/focused-successor/render-01 holds launch.json, browser-process.json (exitCode null) and view-*.png but no render.json; capture.mjs writes render.json last (line 99), so the capture never completed and renderer-successor/check.py has never run; launch.json records project '%s' (the earlier consumer root). Every engine/live criterion therefore has no retained evidence; nothing here turns that into a pass." % jload("render-01-launch")["project"].replace("\\", "/"),
    "No pixl_inspection packet or views exist for the successor; my composites and the prior specialist views are preliminary viewing aids, not saved candidate views for a visual-mode review.",
    "Actual playback of the four frames at 100 ms was not viewed (no live page run; no playback artefact); wall-clock cadence not measured (S5).",
    "Browser rendering of assets/start.svg was not viewed; the Start comparison relies on the prior rasterisation aid.",
    "No acceptance of any candidate, no adoption of the proposal or of successor-01.* ids, no verdict transferred from the original family or the seed, no state/PLAR/job change; job authoring-01.working.join-01 (prepared, undispatched, remote_id null) untouched; the 20 Q records unchanged; the original proposal file unchanged (sha256 792d4b8f... re-verified).",
    "No PixelLab tool call; no pixl_request_review/pixl_context call (the caller's retained exports work/continuation/request-review-authoring-01.json and work/focused-successor/context-authoring-raw.json were used and their identities cross-checked against pixl_validate).",
]

doc = {
    "version": 1,
    "kind": "specialist-round1-assessment",
    "role": "PIXL specialist (native registered pixl child, host model Claude Fable 5.1), artifact-based restart for the retained-contract comparison; round 1; caller review to be reconciled in a later message to this same child",
    "assignment": {"path": "CONTINUATION-ASSIGNMENT.md", "sha256": SOURCE_INDEX["continuation"]["sha256"], "delegation": "caller's round-1 instruction (tasks 1-5) in the launching message"},
    "reviewed_proposal": {"path": SOURCES["proposal"][0], "sha256": SOURCE_INDEX["proposal"]["sha256"], "report": {"path": SOURCES["report"][0], "sha256": SOURCE_INDEX["report"]["sha256"]}, "criteria_count": 29, "mapping_rows": 20, "sources_count": len(proposal["sources"])},
    "state": {"path": SOURCES["state"][0], "revision": 88, "sha256": SOURCE_INDEX["state"]["sha256"], "validated": "pixl_validate: valid, format 2, 412 records, files_verified true", "requirements_hash_current": proposal["requirements_hash"], "requirements_hash_bound_in_plan_and_job": proposal["old_requirements_hash_bound_in_plan_and_job"], "job": {"id": "authoring-01.working.join-01", "state": "prepared", "remote_id": None, "touched": False}},
    "conventions": {
        "lines": "one-based inclusive file-local lines; every `locator` in this file was opened at build time by specialist-round1-build.py and verified to contain its `contains` wording; JSON-field locators were verified by path",
        "authority_classes": CLASSES,
        "image_coordinates": "zero-based pixel indices; component boxes half-open [left, top, right, bottom]; centroids in pixel-edge coordinates (index + 0.5); 4-connectivity on alpha > 0; luminance Rec.709 on alpha > 0 pixels composited over #172336 (luminance 33.8)",
        "visual_statements": "every visual statement is labelled as my own viewing of a named image file and is preliminary; nothing here is acceptance or a pass on an unavailable check",
    },
    "sources": SOURCE_INDEX,
    "identity_verification": {
        "proposal_sha256_matches_expected": True,
        "proposal_sources_hash_check": {"count": len(source_hash_check), "all_match": True},
        "report_verification_citations_rechecked": {"count": len(citation_recheck), "all_verified_by_me": True},
        "original_20_ids_and_hashes": "context packet == pixl_validate == caller request-review export == proposal mapping (see mapping_check)",
        "my_citations_verified_at_build": len(VERIFIED),
    },
    "assessment": {
        "sound": "The proposal is a careful, well-sourced successor contract. All 33 source hashes and all 79 of its citations verify; all 20 original ids/record hashes are present, mapped and hash-consistent with the store; the three D1 splits, D2 pacing demotion, D3 weight wording and D4 Start basis are applied faithfully; selective AA / full alpha, margins-versus-padding, the perceptibility-not-extent accent role, expert pacing versus the owner's 100 ms, and the shared-consumer Start inference are all preserved; the P1 measurements are exact and reproduce; the frozen-spinner limit is stated honestly; nothing is claimed about fixture or inspection evidence that does not exist.",
        "needs_correction": "One promotion of a design proposal into a requirement-labelled check (S1: 'recognisably one phase of the Working loop' would reject a brief-conforming P2), one weakened viewing condition (S2: label present), one wrong process-requirement locator (S3: the assembly policy lives in AUTHORING-STAGE.md 31-32, not FOCUSED-SUCCESSOR 40-43), one mixed-authority check (S4: per-frame reading), one overclaimed/unnamed temporal evidence route (S5: 'live loop observed cycling' is not what check.py asserts; actual playback viewing has no route), and implementation-shape binding labelled as requirement across the five engine criteria (S6, with S7 as the labelling root cause). Notes S8-S12 are wording or checker-support refinements.",
        "open": "No engine/live or visual criterion has retained evidence: the render-01 capture is incomplete (no render.json), check.py has never run, no inspection views exist, and actual playback has not been viewed. Owner decisions on frozen-spinner semantics and on the Retry/Start inference remain open. Corrections belong in a successor proposal artifact beside the original, never by rewriting it.",
        "distinctions_preserved": {
            "selective_aa_full_alpha": "preserved in all three style criteria and the visual transparent-exterior records; no binary-alpha rule anywhere (verified by reading every check)",
            "margins_vs_padding": "preserved in working.q.geometry ('transparent margin inside a cell is composition, not padding')",
            "colour_role_perceptibility": "preserved ('perceptible cool-blue accent', 'no exact hex'); Start-accent relation is an inference (S9)",
            "expert_pacing_vs_owner_100ms": "preserved (D2 faithfully applied; even pacing is an expert clause)",
            "start_distinction_shared_consumer_inference": "preserved in every Start clause (D4); label convention note S11",
            "visual_temporal_destination_separate": "visual (saved views) and destination (fixture + check.py + baseline hashes) routes are named; the temporal route is split into consumer constant / frame-index arithmetic / actual playback and the last leg is not yet routed (S5)",
        },
    },
    "criteria_classification": criteria_classification,
    "defects": defects,
    "defect_counts_by_severity": severity_counts,
    "mapping_check": mapping_check,
    "reduced_motion_assessment": reduced_motion_assessment,
    "unavailable_or_not_claimed": unavailable_or_not_claimed,
    "questions_for_caller": [
        "Is the successor criteria set meant to bind only the P1 held-cell candidate, or to be the successor's universal Working contract? This decides whether S1 is fixed by scoping the stationary-meaning criterion to P1 or by removing the loop-phase clause (and S6 by scoping the descriptor-shape clauses to this implementation).",
        "Do you adopt distinction of the stationary symbol from Retry and from Start as an inference-based requirement (the proposal's own open question), or keep only the explicit Ready/Paused requirement from PLAR line 422?",
    ],
    "next": "Caller: write CALLER-REVIEW-01.json independently against the original sources (this file is my assessment, not your comparison), then send it to this child to reconcile; the reconciled corrections (S1-S7 at least) go into a new successor proposal artifact under work/continuation beside the unchanged original. Before any adoption or acceptance: complete the renderer-successor capture (phases normal-start, reduced, normal-restored; plus an as-launched forced-reduced run) into a fresh directory, run check.py with the baseline hash map, view the reduced-phase captures natively and enlarged with the held cell beside Retry at 1x grayscale, and view actual normal-motion playback; resolve job authoring-01.working.join-01 through its existing failed-observation route (caller decision).",
    "files_created": [
        "work/continuation/SPECIALIST-ROUND1.json",
        "work/continuation/specialist-round1-build.py",
        "work/continuation/round1-views-build.py",
        "work/continuation/round1-views/round1-measurements.json",
        "work/continuation/round1-views/after-round1-hashes.json (hash_tree.py output after this round; 1332 retained files, none changed/removed/added versus work/continuation/baseline-hashes.json)",
    ] + [v["path"] for v in views.values()],
    "files_modified": [],
    "tools_used": ["Read (files and image viewing)", "Grep", "Bash: C:/github/pixel-lab-agent/.venv/Scripts/python.exe -I (json, hashlib, Pillow)", "pixl_validate (.pixl/assets/queue.ready/state.px)", "pixl_asset_check alpha=full (assets/working.png 64x16, error-retry.png, ready-confirmed.png, paused.png)"],
    "tools_not_called": ["pixl_commit", "pixl_job_prepare/dispatch/observe/import", "pixl_plar_save", "pixl_plar_prepare", "pixl_production_plan", "pixl_stage_prepare", "pixl_inspection_prepare", "pixl_inspection_review", "pixl_task_complete", "pixl_plar_handoff", "pixl_family_snapshot", "pixl_request_review (caller's retained export used)", "pixl_context (retained raw packet used)", "any PixelLab tool", "renderer-successor capture (not run)"],
    "build_verification": {"verified_citations": VERIFIED},
}

OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps({"path": str(OUT.relative_to(ROOT)).replace("\\", "/"), "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(), "bytes": OUT.stat().st_size, "defects": severity_counts, "criteria": len(criteria_classification), "citations_verified": len(VERIFIED), "report_citations_rechecked": len(citation_recheck)}))
