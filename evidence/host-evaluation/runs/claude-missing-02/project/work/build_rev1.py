"""Author PX2 revision 1: intake choices, contract, sample plan and criteria."""
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(r"C:\Users\ryanf\AppData\Local\Temp\pixl-host-trial-bio7mnzk")
DATE = "2026-09-11"
KB = ".agents/skills/pixl-kit/resources/training/original-docs"
DEEP = f"{KB}/PIXEL-ART-DEEP-RESEARCH.md"
ASSETS = f"{KB}/PIXEL-ART-ASSETS.md"


def digest(relpath):
    return hashlib.sha256((ROOT / relpath).read_bytes()).hexdigest()


def sym(name):
    return {"$symbol": name}


def ref(name):
    return {"$ref": name}


def refs(*names):
    return [ref(n) for n in names]


PALETTE = ["#25354A", "#56B5BC", "#F4DDA2"]
LIGHTING = (
    "Flat unlit fill with no interior ramp or dithering. Form is described by the dark "
    "#25354A outline alone, because reference.png contains no fourth colour and therefore "
    "supplies no shading ramp."
)

records = []


def add(id_, kind, fields):
    records.append({"id": id_, "kind": kind, "fields": fields})


def source(id_, uri, authority, lines=None, at=DATE):
    add(id_, "S", {
        "ur": uri, "dg": digest(uri), "ln": lines or [], "at": at,
        "au": sym(authority),
    })


# --- actors -----------------------------------------------------------------
add("actor", "A", {"nm": "PIXL", "rl": sym("agent")})
add("user", "A", {"nm": "Project owner", "rl": sym("user")})

# --- sources ----------------------------------------------------------------
source("s.brief", "sources/brief.md", "local")
source("s.refobs", "sources/reference-observation.md", "local")
source("s.refpng", "reference.png", "local")
source("s.discovery", "sources/pixellab-discovery.md", "local")
source("s.caps", "sources/pixellab-capabilities-snapshot.json", "local",
       at="2026-09-11T05:58:46.820240+00:00")
source("s.kb.palette", DEEP, "study", [767, 804])
source("s.kb.palette.assets", ASSETS, "study", [2677, 2683])
source("s.kb.alpha", DEEP, "study", [945, 977])
source("s.kb.integer", DEEP, "study", [1293, 1315])
source("s.kb.silhouette", DEEP, "study", [857, 867])

# --- knowledge methods (researched; no executed proof for this asset) -------
add("k.palette", "K", {
    "nm": "Declare and validate a scoped palette",
    "ap": [sym("indexed_sprites_40eaa310"), sym("limited_palette_styles_c8701d42"),
           sym("material_ramps_1ca01010")],
    "op": ["Assign stable palette indices and reserve any transparent entry explicitly.",
           "Validate opaque pixels against the palette; keep lighting-output exemptions "
           "separately declared.",
           "Apply colour replacements by semantic ramp rather than unrestricted RGB "
           "interpolation."],
    "ck": ["Every checked pixel maps to an allowed index.",
           "Palette changes retain stable semantic meaning and transparency."],
    "so": refs("s.kb.palette", "s.kb.palette.assets"),
    "rq": ["An approved RGBA palette, colour-space choice and transparency policy"],
    "rk": ["A fixed small palette is optional art direction, not a universal definition of "
           "pixel art.",
           "RGBA data can be palette-constrained without using an indexed file format."],
    "tg": ["palette-contract"],
})
add("k.alpha", "K", {
    "nm": "Declare alpha and compositing behavior",
    "ap": [sym("transparent_sprites_75353d50"), sym("glows_19e4066b"),
           sym("sprite_atlases_07b42f1f")],
    "op": ["Keep alpha policy separate from RGB palette membership.",
           "Use the chosen compositing equation consistently through export, import and "
           "display.",
           "Inspect edges against light and dark backgrounds after round-trip import."],
    "ck": ["Binary-alpha assets contain only 0 and 255 unless an exception is declared.",
           "Composited fixtures agree with the declared alpha model."],
    "so": refs("s.kb.alpha"),
    "rq": ["RGBA interpretation, straight or premultiplied alpha, and allowed alpha levels"],
    "rk": ["Fully transparent RGB channels can differ without changing visible appearance."],
    "tg": ["alpha-contract"],
})
add("k.integer", "K", {
    "nm": "Render at a declared logical grid and inspect device pixels",
    "ap": [sym("strict_grid_games_a7cd2a47"), sym("pixel_previews_014b1177"),
           sym("sprite_delivery_638f99a7")],
    "op": ["Render or sample at the logical grid, then use a declared integer scale where "
           "required.",
           "Apply nearest sampling to image scaling and account for browser device pixel "
           "ratio.",
           "Inspect the final output, not only a CSS property or import setting."],
    "ck": ["A logical pixel expands into a uniform scale-by-scale block in the fixture.",
           "No new colours appear during opaque nearest-neighbour enlargement."],
    "so": refs("s.kb.integer"),
    "rq": ["Logical resolution, camera convention and target viewport dimensions"],
    "rk": ["Noninteger scaling, arbitrary rotation and browser zoom can change displayed "
           "pixel widths."],
    "tg": ["integer-presentation"],
})
add("k.silhouette", "K", {
    "nm": "Evaluate identity using silhouette and target backgrounds",
    "ap": [sym("characters_25d939ff"), sym("inventory_icons_f7812ea4"),
           sym("interactive_props_25a44283")],
    "op": ["Render a flat opaque mask before detailing.",
           "Inspect major proportions, negative spaces and landmark separation at native "
           "logical scale.",
           "Compare the coloured asset on representative light, dark and busy backgrounds."],
    "ck": ["Named identity landmarks remain visible at the target size.",
           "Required gaps stay open and interactive forms separate from their surroundings."],
    "so": refs("s.kb.silhouette"),
    "rq": ["Intended viewing scale, representative backgrounds and identity landmarks"],
    "rk": ["Silhouette alone cannot validate faces, materials or fine symbols.",
           "No contrast ratio or component count proves aesthetic quality."],
    "tg": ["silhouette-readability"],
})

# --- intake choices ---------------------------------------------------------
CHOICES = [
    ("i.px", "user", "px", "confirmed", [32, 32], ("s.brief", "s.refpng"),
     "The owner states 32 by 32; reference.png measures exactly 32x32 with the art inset "
     "from every edge (bbox 7,3-25,28)."),
    ("i.pl", "user", "pl", "confirmed", PALETTE, ("s.brief", "s.refobs", "s.refpng"),
     "The owner requires 'the reference palette'. A colour census of reference.png returns "
     "exactly three opaque colours: #25354A outline/antennae (180 px), #56B5BC body "
     "(186 px), #F4DDA2 eyes (24 px). No fourth colour exists, so this list is complete."),
    ("i.vw", "user", "vw", "confirmed", sym("side"), ("s.brief",),
     "The owner states side view. reference.png does not itself demonstrate a view; it is "
     "bilaterally symmetric and supplies palette, features and edge treatment only."),
    ("i.al", "user", "al", "confirmed", sym("binary"), ("s.brief", "s.refobs"),
     "The owner requires binary transparency. reference.png already measures 0 "
     "fractional-alpha pixels, so the reference is consistent with this policy."),
    ("i.sa", "user", "sa", "confirmed", sym("nearest"), ("s.brief",),
     "The owner will display the PNG with nearest-neighbour sampling in a web prototype."),
    ("i.li", "actor", "li", "proposed", LIGHTING, (),
     "Not stated by the owner. Proposed because a three-colour palette leaves no value "
     "ramp, and reference.png shows a completely flat teal fill with zero interior "
     "shading. Adopting any shading would require a fourth colour and would break the "
     "confirmed palette. The sample exists to test this proposal, not to assume it."),
    ("i.outline", "user", "outline", "confirmed", "#25354A", ("s.brief", "s.refobs"),
     "The owner requires dark outlines. The only dark colour in the reference palette is "
     "#25354A, used in the reference as a uniform two-pixel border enclosing the body and "
     "as the antennae."),
    ("i.ground_shadow", "user", "ground_shadow", "confirmed",
     "No ground shadow, contact shadow or ground-contact cluster is drawn into the sprite; "
     "the silhouette must remain one connected opaque component.", ("s.brief", "s.refobs"),
     "The owner requires no ground shadow. reference.png measures exactly 1 opaque "
     "connected component, confirming the reference carries none either."),
    ("i.features", "user", "features", "confirmed",
     {"antennae": 2, "eyes": 2, "eye_color": "#F4DDA2", "body_color": "#56B5BC",
      "subject": "scout robot"}, ("s.brief", "s.refobs"),
     "Feature inventory required by the owner and corroborated by the reference: two "
     "antennae rising from the top of the head in the outline colour, and two pale-yellow "
     "eyes as separate clusters on the upper body."),
    ("i.eye_presentation", "actor", "eye_presentation", "proposed",
     "Both eyes remain visible on the facing plane of a side-facing body.", (),
     "Not stated by the owner, and the brief's two requirements pull apart: a strict "
     "profile head shows one eye, but the owner requires two eyes and the reference shows "
     "two. Proposed resolution is the common 2D convention of a side-facing body with a "
     "frontally-read face. This is the main artistic risk the representative sample must "
     "settle before any family expansion; a returned profile head with one eye fails "
     "q.identity."),
    ("i.delivery_target", "user", "delivery_target", "confirmed",
     "A single PNG file displayed in a web prototype at an integer scale with "
     "nearest-neighbour sampling.", ("s.brief",),
     "Stated delivery destination. It sets the integer-presentation requirement and the "
     "engine-domain criterion q.webdisplay."),
    ("i.web_prototype", "user", "web_prototype", "unresolved", None, (),
     "The owner has not identified the web prototype's repository, framework, page or asset "
     "path. Until it is named, the engine-domain criterion q.webdisplay cannot be executed "
     "and must be recorded unavailable rather than passed."),
    ("i.provider", "actor", "provider", "observed",
     "PixelLab is the owner's named generator, but no PixelLab tool is callable in this "
     "session and no PixelLab credential is present.", ("s.brief", "s.discovery", "s.caps"),
     "The owner named PixelLab. Discovery of the actual session tool surface found only the "
     "local pixl-local MCP server, whose own instructions state PixelLab must be connected "
     "separately. pixl_capabilities is a dated documentation inventory that reports "
     "live_discovery false, so it cannot supply the observed schema that job-prepare "
     "requires. This blocks generation, not planning or evaluation."),
    ("i.family_scope", "user", "family_scope", "unresolved", None, (),
     "The owner defers family expansion until this sample is reviewed and has not named the "
     "members (poses, directions, states or variants). Required before the family and "
     "delivery operation can record members and a baseline."),
]
for id_, who, key, status, value, sources, why in CHOICES:
    add(id_, "I", {
        "pr": ref("project"), "wh": ref(who), "ky": key, "st": sym(status),
        "vl": value, "so": refs(*sources), "wy": why,
    })

# --- visual contract --------------------------------------------------------
add("c.sprite", "C", {
    "nm": "Teal scout robot 32x32 side-view sample sprite",
    "px": [32, 32],
    "pl": PALETTE,
    "vw": sym("side"),
    "sa": sym("nearest"),
    "al": sym("binary"),
    "li": LIGHTING,
    "ch": refs("i.px", "i.pl", "i.vw", "i.sa", "i.al", "i.li"),
})

# --- acceptance criteria ----------------------------------------------------
CRITERIA = [
    ("q.canvas", "Canvas is exactly 32x32", "mechanical", "local",
     "asset-check on the delivered PNG reports frame_count 1 with width 32 and height 32, "
     "and no dimension failure.", ("s.brief",)),
    ("q.palette", "Only the three reference colours appear", "mechanical", "local",
     "asset-check with palette #25354A #56B5BC #F4DDA2 reports outside_palette_count 0 and "
     "visible_colors no greater than 3; every listed colour that appears is one of the "
     "three.", ("s.brief", "s.refobs")),
    ("q.alpha", "Transparency is binary", "mechanical", "local",
     "asset-check with alpha binary reports fractional_alpha_pixels 0 and no alpha failure, "
     "so every pixel's alpha is exactly 0 or 255.", ("s.brief", "s.kb.alpha")),
    ("q.nearest", "Integer nearest-neighbour enlargement is clean", "other", "local",
     "An 8x nearest-neighbour enlargement of the delivered PNG contains exactly the same "
     "set of visible colours as the 32x32 source, and every logical pixel maps to a uniform "
     "8x8 block of a single RGBA value.", ("s.kb.integer",)),
    ("q.identity", "Reads as the referenced teal scout robot", "visual", "visual",
     "Viewed by the agent at native 32x32 and at integer zoom, side by side with "
     "reference.png in one contact sheet: the sprite reads as a side-facing teal scout "
     "robot; exactly two antennae are visible above the head; exactly two yellow eyes are "
     "visible; a dark #25354A outline encloses the silhouette; the teal body fill is flat; "
     "and no shadow cluster, ground contact smear or stray detached pixel appears below or "
     "around the body.", ("s.brief", "s.refobs", "s.kb.silhouette")),
    ("q.webdisplay", "Displays correctly in the owner's web prototype", "engine", "live",
     "Loaded in the owner's actual web prototype at an integer scale with nearest sampling "
     "(for example image-rendering: pixelated), the sprite shows hard unblended pixel "
     "edges, introduces no colours outside the three-colour palette, and its transparent "
     "edges composite cleanly with no halo over both a light and a dark page background.",
     ("s.brief",)),
]
for id_, name, domain, mode, check, sources in CRITERIA:
    add(id_, "Q", {
        "nm": name, "dm": sym(domain), "md": sym(mode), "ck": check,
        "wh": ref("actor"), "so": refs(*sources),
    })

# --- input artifact ---------------------------------------------------------
add("x.reference", "X", {
    "nm": "Owner-supplied style reference",
    "ur": "reference.png",
    "dg": digest("reference.png"),
    "kd": sym("reference"),
    "mt": {"visible_colors": 3, "visible_pixels": 390, "opaque_components": 1,
           "fractional_alpha_pixels": 0},
    "tg": ["reference"],
})

# --- planned output and task ------------------------------------------------
add("f.sprite", "F", {
    "tk": ref("t.sample"),
    "nm": "Teal scout robot representative sprite PNG (32x32)",
    "kd": sym("sprite"),
    "rq": refs("q.canvas", "q.palette", "q.alpha", "q.nearest", "q.identity",
               "q.webdisplay"),
    "ct": ref("c.sprite"),
})
add("t.sample", "T", {
    "nm": "Produce and review the representative teal scout robot sprite",
    "ow": ref("actor"), "pr": ref("project"),
    "dp": [], "dc": [], "kn": refs("k.palette", "k.alpha", "k.integer", "k.silhouette"),
    "st": sym("open"), "ph": sym("sample"),
    "ip": refs("x.reference"), "op": refs("f.sprite"), "ca": [], "vr": [],
})

# --- project ----------------------------------------------------------------
add("project", "P", {
    "nm": "Teal Scout Robot Sample",
    "ow": ref("user"),
    "sc": refs("s.brief", "s.refobs", "s.refpng", "s.discovery", "s.caps"),
    "in": refs(*[c[0] for c in CHOICES]),
    "ct": ref("c.sprite"),
    "br": json.loads((ROOT / ".pixl" / "brief.json").read_text())
    if (ROOT / ".pixl" / "brief.json").exists() else None,
})

# keep the brief exactly as intake stored it
BRIEF = (
    "Produce a representative 32x32 side-view teal scout robot sprite with PixelLab, "
    "matching reference.png: two antennae, two yellow eyes, dark outlines, binary "
    "transparency, no ground shadow, and the reference palette. Deliver a PNG for "
    "nearest-neighbor display in a web prototype. Verify dimensions and palette "
    "mechanically and compare visually against the reference before expanding to a family."
)
records[-1]["fields"]["br"] = BRIEF

document = {"revision": 1, "format": 2, "records": records}
out = ROOT / "work" / "candidate-rev1.json"
out.write_text(json.dumps(document, indent=2), encoding="utf-8")
print("wrote", out, "records:", len(records))
