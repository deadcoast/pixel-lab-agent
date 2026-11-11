"""Author the revised 150 ms request packet from the current focused PLAR read (local files only)."""
import datetime
import hashlib
import json

W = "work/integration-change/"
sel = json.load(open(W + "current-selection.json", encoding="utf-8"))
now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="microseconds")
SHEET = "cf101610108f5a708987dfeb1a86ae9921525464d24c19953a889e20603176dc"

args = {
    "description": (
        "Controlled unsubmitted Working intent at the amended timing: four horizontal 16x16 activity frames, "
        "transparent background, cool blue accent, 150 ms per frame looping (600 ms cycle). Exact existing "
        "assets/working.png bytes are reused; this request is retained for lineage only and is not authorized for dispatch."
    ),
    "width": 64,
    "height": 16,
    "no_background": True,
}
srcs = [
    {"path": "BRIEF.md", "locator": "Asset brief and current updates"},
    {"path": "WORKING-TIMING-AMENDMENT.md", "locator": "Current Working timing authority: 150 ms per frame, four frames, looping, 600 ms cycle"},
    {"path": "src/working-timing.ts", "locator": "frameMs = 150"},
    {"path": "src/queue-view-integration.ts", "locator": "display = { ...originalDisplay, frameMs }"},
    {"path": "src/queue-view.ts", "locator": "statusVisuals, statusCell, compactStatus and display"},
]
crit = {
    "version": 1,
    "scope": "Revised 150 ms Working timing integration over the exact retained Working sheet; controlled local preparation only, no provider execution or acceptance.",
    "outputs": [{
        "id": "working",
        "name": "Working timing integration (150 ms)",
        "kind": "animation",
        "contract": {
            "size": [64, 16], "palette": [], "view": "ui", "sampling": "nearest", "alpha": "full",
            "intent": f"Reuse the exact four-frame Working sheet (sha256 {SHEET}); 150 ms per frame, looping, 600 ms cycle; activity distinct from success, retry and paused.",
        },
        "criteria": [
            {"id": "canvas", "domain": "mechanical", "mode": "local",
             "check": f"Exact retained transparent 64x16 sheet, four horizontal 16x16 frames; art bytes unchanged (sha256 {SHEET}).",
             "basis": "Preserved source-defined geometry/transparency constraints and the explicit Working timing amendment (no new art).",
             "scope": "This exact Working candidate in the retained queue consumer.", "sources": srcs},
            {"id": "activity", "domain": "visual", "mode": "visual",
             "check": "Readable cool-blue activity at 1x and 3x nearest on the #172336 dark panel; each frame and the sequence communicate ongoing work without a success-like pose; distinct from Ready, Retry and Paused without relying on color alone; scoped coherent treatment with the retained Ready reference.",
             "basis": "Preserved brief requirements (readability at 1x/3x, transparent background, cool blue accent, activity not success, non-color distinctions) and the adopted Ready style baseline.",
             "scope": "This exact Working candidate in the retained queue consumer.", "sources": srcs},
            {"id": "integration", "domain": "engine", "mode": "live",
             "check": "Observe the exact Working sheet in both actual consumers (statusCell and compactStatus) with four looping frames at the current authorized 150 ms each (600 ms cycle), nearest filtering and transparent compositing on the dark panel; live loop playback observed at the consumer's 3x scale, stills at 1x and 3x; 1x live playback remains unperformed.",
             "basis": "Explicit Working timing amendment and the stable integration wrapper driving both original consumers.",
             "scope": "This exact Working candidate in the retained queue consumer.", "sources": srcs},
        ],
    }],
}


def dump(name, obj):
    text = json.dumps(obj, indent=2, ensure_ascii=False) + "\n"
    with open(W + name, "w", encoding="utf-8", newline="\n") as stream:
        stream.write(text)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


ha = dump("arguments-150.json", args)
hc = dump("criteria-150.json", crit)
packet = {
    "version": 1,
    "requirements_hash": sel["requirements_hash"],
    "sources": [{"path": s["path"], "sha256": s["observed_sha256"], "role": "selected source requirement"} for s in sel["sources"]],
    "request": {"path": W + "arguments-150.json", "sha256": ha, "kind": "provider_arguments", "tool": "create_image_pro_flash"},
    "criteria": {"path": W + "criteria-150.json", "sha256": hc},
    "choices": [],
}
hp = dump("packet-150.json", packet)
conn = {
    "provider": "pixellab",
    "schema": {
        "type": "object",
        "properties": {
            "description": {"type": "string"},
            "width": {"type": "integer", "minimum": 16, "maximum": 256, "multipleOf": 4},
            "height": {"type": "integer", "minimum": 16, "maximum": 256, "multipleOf": 4},
            "no_background": {"type": "boolean"},
        },
        "required": ["description", "width", "height", "no_background"],
        "additionalProperties": False,
    },
    "discovery": {
        "source": "Controlled CF-07 local preparation schema carried forward from the retained first_request intent; not a live provider discovery",
        "observed_at": now,
        "evidence": {"controlled_fixture": True, "live_discovery": False, "carried_from_job": "first_request"},
    },
    "authorization": {
        "scope": "Local intent preparation only; no dispatch execution or provider call authorized; exact retained art reuse under WORKING-TIMING-AMENDMENT.md",
        "evidence": {"controlled_fixture": True, "amendment": "WORKING-TIMING-AMENDMENT.md", "new_art_authorized": False},
    },
}
hn = dump("connection-150.json", conn)
print(json.dumps({"arguments": ha, "criteria": hc, "packet": hp, "connection": hn,
                  "requirements_hash": sel["requirements_hash"],
                  "state_hash": sel["production"]["continuation"]["state_hash"]}))
