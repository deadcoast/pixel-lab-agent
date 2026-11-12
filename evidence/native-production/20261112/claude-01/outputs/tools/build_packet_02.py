"""Build packet-02 from packet-01 plus the caller's COMPARISON.json corrections.

packet-01 is left unchanged. Corrections applied:
1. provider-arguments: palette (the three source colours) + palette_name.
2. description: rectangular posts; three colours on transparency.
3. identity criteria per facing (east/west: visible post(s), rectangular; north: no teal panel required).
4. proportions_volume: visual requirement without numbers; numbers moved to a proposal criterion.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
P1 = ROOT / "work/native-production/packet-01"
P2 = ROOT / "work/native-production/packet-02"
P2.mkdir(parents=True, exist_ok=True)
COMPARISON_SHA = "503de778135f188c64f45eab170144e65fc3b3d375ef566be01b18083b1169a2"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(name):
    return json.loads((P1 / name).read_text(encoding="utf-8"))


def dump(name, obj):
    p = P2 / name
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


# 1 + 2: arguments
args = load("provider-arguments.json")
args["description"] = (
    "Small boxy robot sprite: a dark navy rectangular frame with two rectangular antenna posts rising "
    "from its top corners, a flat teal front panel, and two rectangular pale-yellow eyes. Flat eye-level "
    "pixel art in three colours (navy, teal, pale yellow) on a transparent background, no shading or "
    "outline gradients. Rotate this exact sprite; keep its height, width, colours, silhouette and simple "
    "box volume in every view."
)
args["palette"] = ["#25354a", "#56b5bc", "#f4dda2"]
args["palette_name"] = "robot-base source colours"
p_args = dump("provider-arguments.json", args)

# unchanged artifacts copied for a self-contained packet
for name in ("connection.json", "south-baseline-plan.json", "family-plan-draft.json", "discovery-01.json"):
    shutil.copyfile(P1 / name, P2 / name)
p_conn = P2 / "connection.json"

# 3 + 4: criteria
plan = load("candidate-plan.json")
IDENTITY = {
    "east": ("Viewed at 1x and 3x nearest, the sprite reads as the same robot as assets/robot-base.png turned to face east: "
             "the dark navy rectangular frame, the rectangular antenna post(s) as visible from that facing (one post may hide "
             "the other in profile) at the same post height, the teal body panel, and the pale-yellow eyes where the facing shows "
             "the front. No added limbs, wheels, extra faces, text or other features, and no redesign."),
    "west": ("Viewed at 1x and 3x nearest, the sprite reads as the same robot as assets/robot-base.png turned to face west: "
             "the dark navy rectangular frame, the rectangular antenna post(s) as visible from that facing (one post may hide "
             "the other in profile) at the same post height, the teal body panel, and the pale-yellow eyes where the facing shows "
             "the front. No added limbs, wheels, extra faces, text or other features, and no redesign."),
    "north": ("Viewed at 1x and 3x nearest, the sprite reads as the same robot as assets/robot-base.png seen from behind: "
              "the dark navy frame colour, both rectangular antenna posts (both visible from behind) at the same post height, "
              "no eyes. The teal front panel is not required on the back (the source never shows the back). No added limbs, "
              "wheels, faces, text or other features, and no redesign."),
}
for output in plan["outputs"]:
    d = output["id"]
    new = []
    for c in output["criteria"]:
        if c["id"] == "identity":
            c = {**c, "check": IDENTITY[d],
                 "basis": c["basis"] + " Clarified per caller COMPARISON.json (packet-01 identity rows)."}
        elif c["id"] == "proportions_volume":
            c = {**c,
                 "check": ("The sprite keeps the source's proportions and reads as the same simple box volume turned to the named facing: "
                           "same overall height, same post height, not stretched, shrunk, squashed or re-proportioned."),
                 "basis": ("Brief: preserve proportions; CF-10: inspect proportions and volume; PLAR delivery check 'identity, volume and "
                           "alignment together'. The specialist's measurement proxy (25 px tall, antenna tops row 3, base row 27, posts 4x6, "
                           "within 1 px) is recorded separately in height_measure, a proposal.")}
            new.append(c)
            new.append({
                "id": "height_measure", "domain": "mechanical", "mode": "local", "authority": "proposal",
                "check": ("Measured on the visible bounding box (zero-based, exclusive): top in [2,4] and bottom == 28, i.e. 24-26 px tall "
                          "(source: top 3, bottom 28, 25 px); each visible antenna post is 6 px tall within 1 px (source posts 4x6)."),
                "basis": "Specialist measurement proxy supporting proportions_volume; the numbers and tolerances are the specialist's, not an owner rule.",
                "scope": f"The {d} candidate file",
                "sources": [{"path": "assets/robot-base.png", "locator": "measured bbox [7,3,25,28), posts 4x6 at rows 3-8"},
                            {"path": "production-plar.txt", "locator": "robot.directions delivery checks", "lines": [164, 171]}],
            })
            continue
        new.append(c)
    output["criteria"] = new
plan["scope"] = plan["scope"] + " (packet-02: corrected per caller COMPARISON.json)"
p_plan = dump("candidate-plan.json", plan)

# packet
packet = load("request-review.json")
packet["packet_version"] = "02"
packet["supersedes"] = {"path": "work/native-production/packet-01/request-review.json", "sha256": sha(P1 / "request-review.json")}
packet["caller_comparison"] = {"path": "work/native-production/COMPARISON.json", "sha256": COMPARISON_SHA,
                               "result": "changes_requested; packet-02 applies corrections 1-4"}
packet["request"] = {
    "path": "work/native-production/packet-02/provider-arguments.json", "sha256": sha(p_args),
    "kind": "provider_arguments", "tool": "create_object_pro_flash", "provider": "pixellab-mcp",
    "connection": {"path": "work/native-production/packet-02/connection.json", "sha256": sha(p_conn)},
}
packet["criteria"] = {"path": "work/native-production/packet-02/candidate-plan.json", "sha256": sha(p_plan)}
packet["delivered_scope"]["family_delivery"] = "work/native-production/packet-02/family-plan-draft.json"
packet["delivered_scope"]["south_baseline"] = "work/native-production/packet-02/south-baseline-plan.json"
packet["choices"] = [c for c in packet["choices"] if c["id"] not in ("description_text", "palette_exact_set", "tolerances")] + [
    {"id": "palette_argument", "where": "provider-arguments.json palette/palette_name", "choice": "palette = the three source colours",
     "reason": "Caller correction 1: the declared schema says every drawn pixel is one of them and supplied pixels stay as they are, enforcing the owner palette requirement at generation. Deterministic palette/alpha correction remains a fallback, recorded as an 'edited' member distinct from raw provider bytes.", "authority": "caller-adopted correction of an owner requirement"},
    {"id": "description_text", "where": "provider-arguments.json description", "choice": "Literal description: rectangular posts, three colours on transparency; no new features",
     "reason": "Caller correction 2 (posts are 4x6, colour count excludes transparency).", "authority": "specialist choice, corrected"},
    {"id": "palette_exact_set", "where": "criterion palette_preserved", "choice": "'preserve palette' read as only the three source colours", "reason": "Kept by the caller (disposition keep); now also enforced by the palette argument.", "authority": "specialist interpretation accepted by the caller"},
    {"id": "tolerances", "where": "criteria height_measure, ground_line_measure", "choice": "±1 px height / centre / post tolerances", "reason": "Caller correction 4: numbers moved out of the requirement-authority visual check into proposal criteria.", "authority": "specialist choice (proposal)"},
    {"id": "identity_per_facing", "where": "criteria identity (east/west/north)", "choice": "Facing-specific identity wording", "reason": "Caller correction 3: profile may occlude a post; the back need not show the teal panel.", "authority": "caller clarification of the owner identity requirement"},
]
packet["budget"]["spent_so_far"] = 0
p_packet = dump("request-review.json", packet)
for p in sorted(P2.iterdir()):
    print(sha(p), p.relative_to(ROOT).as_posix())
