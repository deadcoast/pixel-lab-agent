"""Check exact directional-controller files and observed browser pixels.

These are mechanical observations. Directional identity, volume, alignment and
artistic suitability still need independent visual review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops

DIRECTIONS = ("south", "east", "north", "west")
MAPPING = {direction: f"assets/robot/{direction}.png" for direction in DIRECTIONS}
INPUTS = {"src/robot.ts", "assets/robot-base.png", *MAPPING.values()}
RENDERER_FILES = {"server.mjs", "capture.mjs", "view.mjs", "index.html", "check.py"}
LIMITATIONS = [
    "Browser pixels and mapping checks do not establish artistic acceptance or another engine's behavior.",
    "1x/3x on #172336 are this renderer's observation conditions, not newly imposed art requirements.",
    "Directional identity, volume, alignment and semantic facing need visual review; identical files can pass mechanical rendering.",
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def confined(root, name):
    root = Path(root).resolve()
    if not isinstance(name, str) or "\\" in name or ":" in name or Path(name).is_absolute() or any(part in ("", ".", "..") for part in name.split("/")):
        raise ValueError("Reference is not a canonical relative path")
    actual = (root / name).resolve()
    if actual == root or not actual.is_relative_to(root):
        raise ValueError("Reference escapes its root")
    return actual


def check(project, capture, renderer=None):
    project, capture = Path(project).resolve(), Path(capture).resolve()
    renderer = Path(renderer).resolve() if renderer else Path(__file__).resolve().parent
    report_path = capture / "capture.json"
    failures, facts = [], {"input_checks": 0, "renderer_checks": 0, "pixel_checks": 0, "screenshot_checks": 0}
    if not report_path.is_file():
        return {"version": 1, "status": "unavailable", "pass": False, "facts": facts,
                "failures": [], "limitations": ["No completed browser capture is available", *LIMITATIONS]}

    def expect(value, label):
        if not value:
            failures.append(label)

    def png(reference):
        path = confined(capture, reference["path"])
        expect(digest(path) == reference["sha256"], "retained image bytes: " + reference["path"])
        with Image.open(path) as image:
            expect(image.format == "PNG", "retained image format: " + reference["path"])
            return image.convert("RGBA")

    def matches(expected, actual):
        return expected.size == actual.size and max(high for low, high in ImageChops.difference(expected, actual).getextrema()) <= 1

    try:
        report = json.loads(report_path.read_bytes())
        execution = json.loads((capture / "execution.json").read_bytes())
        inputs = json.loads((capture / "inputs.json").read_bytes())
        launch = json.loads((capture / "launch.json").read_bytes())
        expect(report["version"] == 1 and report["consumer"] == "directional-robot-v1", "bounded consumer identity")
        expect(execution["consumer"] == report["consumer"] and execution["renderer_executed"] is True, "actual renderer execution")
        expect(execution["status"] == "complete", "completed execution")
        expect(execution["cleanup"]["complete"] is True, "owned browser/server/profile cleanup")
        expect(all(Path(value["project"]).resolve() == project for value in (report, execution, inputs, launch)), "same consumer root")
        expect(report["inputs"] == report["final_inputs"] == inputs["files"], "unchanged inputs across capture")
        expect(set(report["inputs"]) == INPUTS, "complete fixed input closure")
        for name in INPUTS:
            expect(digest(confined(project, name)) == report["inputs"].get(name) == report["served_files"].get("consumer/" + name), "exact served input: " + name)
            facts["input_checks"] += 1
        expect(set(report["renderer_files"]) == RENDERER_FILES, "complete renderer closure")
        expect(report["renderer_files"] == inputs["renderer_files"] == launch["renderer_files"], "same renderer identities")
        for name, expected in report["renderer_files"].items():
            expect(digest(confined(renderer, name)) == expected, "renderer bytes: " + name)
            facts["renderer_checks"] += 1
        expect(set(report["served_files"]) == {"consumer/" + name for name in INPUTS} | {"renderer/index.html", "renderer/view.mjs"}, "only required consumer and display resources served")
        for name in ("index.html", "view.mjs"):
            expect(report["served_files"].get("renderer/" + name) == report["renderer_files"][name], "exact served display: " + name)
        expect(not report["errors"], "no browser or contract errors")
        expect(report["directions"] == list(DIRECTIONS), "required direction order")
        expect(set(report["controller_inventory"]) == set(DIRECTIONS) and len(report["controller_inventory"]) == 4, "actual controller inventory")
        expect(report["controller_mapping"] == report["selected_mapping"] == MAPPING, "actual spriteFor and export mapping")
        expect(report["cell"] == {"width": 32, "height": 32, "sampling": "nearest"}, "actual controller cell")
        expect(report["scales"] == [1, 3] and report["background"] == "#172336", "recorded observation conditions")
        expect(report["viewport"] == {"width": 900, "height": 700, "device_scale_factor": 1}, "observed viewport")
        expect(launch["viewport"] == {"width": 900, "height": 700, "deviceScaleFactor": 1, "mobile": False}, "launched viewport")
        expect(bool(report["browser_version"]["product"]), "actual browser identity")
        base = confined(project, "assets/robot-base.png")
        expect(report["base"]["available"] is True and report["base"]["sha256"] == digest(base), "exact original identity loaded")
        expect(report["south_matches_base"] is True and digest(base) == digest(confined(project, MAPPING["south"])), "south preserves original file bytes")
        source_images = {}
        for direction, name in MAPPING.items():
            with Image.open(confined(project, name)) as source:
                expect(source.format == "PNG" and source.mode == "RGBA" and source.size == (32, 32), "32x32 RGBA PNG: " + direction)
                rgba = source.convert("RGBA")
                alpha = rgba.getchannel("A").getextrema()
                expect(alpha[0] == 0 and alpha[1] > 0, "visible image with transparent background: " + direction)
                source_images[direction] = rgba
        expect(report["screenshot"]["path"] == "destination.png", "single destination screenshot")
        screenshot = png(report["screenshot"])
        expect(screenshot.size == (900, 700), "screenshot viewport")
        expect(len(report["views"]) == 8 and {(view["direction"], view["scale"]) for view in report["views"]} == {(d, s) for d in DIRECTIONS for s in (1, 3)}, "all four directions at both scales")
        for view in report["views"]:
            direction, scale = view["direction"], view["scale"]
            label = f"{direction}@{scale}"
            name = MAPPING[direction]
            expect(view["path"] == view["asset"]["path"] == name, "selected asset: " + label)
            expect(view["asset"]["available"] is True and view["geometryMatches"] is True, "available geometry: " + label)
            expect(view["asset"]["sha256"] == report["inputs"][name], "browser decoded exact bytes: " + label)
            expect(view["asset"]["width"] == view["asset"]["height"] == 32, "browser natural dimensions: " + label)
            expect(view["smoothing"] is False and view["imageRendering"] == "pixelated", "nearest sampling: " + label)
            expect(view["image"]["path"] == f"{direction}-{scale}x.png", "distinct retained view: " + label)
            actual = png(view["image"])
            expected = Image.alpha_composite(Image.new("RGBA", (32, 32), (23, 35, 54, 255)), source_images[direction]).resize((32 * scale, 32 * scale), Image.Resampling.NEAREST)
            expect(matches(expected, actual), "source alpha/compositing/nearest pixels: " + label)
            facts["pixel_checks"] += 1
            rect = view["rect"]
            values = [rect[key] for key in ("x", "y", "width", "height")]
            expect(all(type(value) in (int, float) and int(value) == value for value in values), "integer placement: " + label)
            x, y, width, height = map(int, values)
            expect(width == height == 32 * scale and x >= 0 and y >= 0 and x + width <= 900 and y + height <= 700, "visible scaled canvas: " + label)
            expect(matches(actual, screenshot.crop((x, y, x + width, y + height))), "actual screenshot canvas pixels: " + label)
            facts["screenshot_checks"] += 1
    except (KeyError, TypeError, ValueError, OSError, IndexError) as error:
        failures.append("Malformed or unavailable retained input: " + str(error))
    return {"version": 1, "status": "fail" if failures else "pass", "pass": not failures,
            "capture_sha256": digest(report_path), "facts": facts, "failures": failures, "limitations": LIMITATIONS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--capture", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.project, args.capture)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "path": str(args.out), "pass": result["pass"]}))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
