"""Proof of concept for the acceptance harness itself, before any candidate exists.

Question: do the locally decidable criteria (q.canvas, q.palette, q.alpha, q.nearest)
actually discriminate, or would they pass anything?

Method: run tools/check_sprite.py's checks on a positive control (reference.png, which
satisfies the mechanical half of the contract) and on four mutants, each breaking exactly
one criterion. Acceptance, stated before running: the control passes all four; each mutant
fails exactly its own criterion and no other.
"""
import json
import pathlib
import sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import check_sprite as cs  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "work" / "poc"
OUT.mkdir(parents=True, exist_ok=True)

base = cs.load_frames(ROOT / "reference.png")[0]


def mutate_palette(img):
    """One body pixel shifted by a single blue step: #56B5BC -> #56B5BD."""
    img = img.copy()
    for y in range(img.height):
        for x in range(img.width):
            if img.getpixel((x, y)) == (86, 181, 188, 255):
                img.putpixel((x, y), (86, 181, 189, 255))
                return img
    raise AssertionError("no body pixel found")


def mutate_alpha(img):
    """One body pixel given a half-transparent alpha."""
    img = img.copy()
    for y in range(img.height):
        for x in range(img.width):
            p = img.getpixel((x, y))
            if p == (86, 181, 188, 255):
                img.putpixel((x, y), (86, 181, 188, 128))
                return img
    raise AssertionError("no body pixel found")


def mutate_canvas(img):
    """Delivered one pixel too wide."""
    grown = Image.new("RGBA", (img.width + 1, img.height), (0, 0, 0, 0))
    grown.paste(img, (0, 0))
    return grown


CASES = [
    ("control", base, set()),
    ("mutant-palette", mutate_palette(base), {"q.palette"}),
    ("mutant-alpha", mutate_alpha(base), {"q.alpha"}),
    ("mutant-canvas", mutate_canvas(base), {"q.canvas"}),
]

report = {"question": __doc__.strip().splitlines()[2].strip(), "cases": []}
ok_overall = True

for name, image, expected_failures in CASES:
    path = OUT / f"{name}.png"
    image.save(path)
    frames = cs.load_frames(path)
    frame = frames[0]
    outcomes = {
        "q.canvas": cs.check_canvas(frames),
        "q.palette": cs.check_palette(frame),
        "q.alpha": cs.check_alpha(frame),
        "q.nearest": cs.check_nearest(frame),
    }
    failed = {k for k, (ok, _) in outcomes.items() if not ok}
    agrees = failed == expected_failures
    ok_overall &= agrees
    report["cases"].append({
        "name": name, "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "expected_failures": sorted(expected_failures),
        "actual_failures": sorted(failed),
        "as_predicted": agrees,
        "measurements": {k: data for k, (_, data) in outcomes.items()},
    })

# Negative control for the sampling mode itself: the same 32x32 art enlarged with a
# smoothing filter must fail the uniform-block condition that nearest enlargement passes.
big_bilinear = base.resize((base.width * cs.ZOOM, base.height * cs.ZOOM), Image.BILINEAR)
source_colors = set(base.getdata())
smeared_new_colors = len(set(big_bilinear.getdata()) - source_colors)
nonuniform = 0
for y in range(base.height):
    for x in range(base.width):
        block = big_bilinear.crop((x * cs.ZOOM, y * cs.ZOOM,
                                   (x + 1) * cs.ZOOM, (y + 1) * cs.ZOOM))
        distinct = set(block.getdata())
        if len(distinct) != 1 or distinct.pop() != base.getpixel((x, y)):
            nonuniform += 1
sampling_discriminates = smeared_new_colors > 0 and nonuniform > 0
ok_overall &= sampling_discriminates
report["sampling_negative_control"] = {
    "description": "Same art enlarged 8x with BILINEAR instead of NEAREST.",
    "new_colors_introduced": smeared_new_colors,
    "nonuniform_blocks": nonuniform,
    "discriminates": sampling_discriminates,
}

report["result"] = "pass" if ok_overall else "fail"
report["limits"] = [
    "This proves the checking code discriminates on controlled mutants.",
    "It is not a PixelLab generation, not a candidate for f.sprite, and not evidence "
    "about the artistic quality of any sprite.",
    "q.identity and q.webdisplay are untouched by this proof.",
]
path = ROOT / "work" / "poc" / "harness-proof.json"
path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
print(json.dumps({k: v for k, v in report.items() if k != "cases"}, indent=2))
for case in report["cases"]:
    print(case["name"], "expected", case["expected_failures"],
          "actual", case["actual_failures"], "->", case["as_predicted"])
sys.exit(0 if ok_overall else 1)
