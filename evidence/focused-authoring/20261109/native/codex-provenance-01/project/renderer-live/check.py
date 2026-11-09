"""Verify retained browser pixels/identities; visual and family judgments are separate."""

import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import cast

from PIL import Image, ImageChops, ImageColor


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def rgb_difference(left, right):
    extrema = cast(tuple[tuple[float, float], ...], ImageChops.difference(left, right).convert("RGB").getextrema())
    return max(high for low, high in extrema)


def confined(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Capture resource escapes its root")
    return path


def check(project, capture):
    project, capture = Path(project).resolve(), Path(capture).resolve()
    report = json.loads((capture / "render.json").read_text(encoding="utf-8"))
    failures, observations = [], []

    def expect(condition, name):
        observations.append({"check": name, "pass": bool(condition)})
        if not condition:
            failures.append(name)

    def retained_image(reference):
        path = confined(capture, reference["path"])
        expect(digest(path) == reference["sha256"], "retained image hash: " + reference["path"])
        with Image.open(path) as image:
            return image.convert("RGBA")

    expect(not report["errors"], "browser reported no script errors")
    expect(report["devicePixelRatio"] == 1, "capture declares device pixel ratio one")
    for name, expected in report.get("renderer_files", {}).items():
        expect(digest(confined(Path(__file__).resolve().parent, name)) == expected, "renderer implementation: " + name)
    for name, expected in report["served_files"].items():
        group, relative = name.split("/", 1)
        base = project if group == "consumer" else Path(__file__).resolve().parent
        path = confined(base, relative)
        expect(digest(path) == expected, "served bytes: " + name)
    screenshot = retained_image(report["screenshot"])
    if "viewport" in report:
        expect(screenshot.size == (report["viewport"]["width"], report["viewport"]["height"]), "screenshot and observed viewport dimensions")
    width, height = report["display"]["cell"]
    background = ImageColor.getrgb(report["display"]["background"])
    available = []
    for view in report["views"]:
        if not view["asset"]["available"]:
            expect("image" not in view, "missing asset has no invented view: " + view["state"])
            continue
        actual = retained_image(view["image"])
        available.append(view)
        label = f"{view['consumer']} {view['state']} {view['scale']}x"
        scale = view["scale"]
        bounds = view["bounds"]
        expect(view["geometryMatches"], label + " source sheet geometry")
        expect(view["smoothing"] is False and view["imageRendering"] == "pixelated", label + " nearest sampling settings")
        expect(actual.size == (width * scale, height * scale), label + " actual canvas dimensions")
        expect(all(value == int(value) for value in bounds.values()), label + " integer destination bounds")
        x, y = int(bounds["x"]), int(bounds["y"])
        on_screen = screenshot.crop((x, y, x + actual.width, y + actual.height))
        expect(ImageChops.difference(on_screen, actual).convert("RGB").getbbox() is None, label + " screenshot matches canvas pixels")
        source = confined(project, view["descriptor"]["path"])
        expect(digest(source) == view["asset"]["sha256"], label + " actual asset identity")
        if source.suffix.lower() == ".png":
            with Image.open(source) as image:
                expect(image.size == (width * view["descriptor"]["frames"], height), label + " independently decoded sheet size")
                frame = image.convert("RGBA").crop((view["frame"] * width, 0, (view["frame"] + 1) * width, height))
            expected = Image.alpha_composite(Image.new("RGBA", frame.size, (*background, 255)), frame).resize(actual.size, Image.Resampling.NEAREST)
            expect(rgb_difference(expected, actual) <= 1, label + " source pixels and alpha compositing (rounding tolerance one)")
        if scale != 1 and source.suffix.lower() == ".png":
            base = next(v for v in report["views"] if v["consumer"] == view["consumer"] and v["state"] == view["state"] and v["scale"] == 1)
            native = retained_image(base["image"]).resize(actual.size, Image.Resampling.NEAREST)
            expect(ImageChops.difference(native, actual).convert("RGB").getbbox() is None, label + " nearest pixel blocks")
    for sample in report["timeline"]:
        if not sample["available"]:
            expect(sample["frame"] is None and "image" not in sample, "missing animation is not a playback result")
            continue
        descriptor = next(v["descriptor"] for v in report["views"] if v["state"] == sample["state"])
        frame_index = (sample["elapsed"] // report["display"]["frameMs"]) % descriptor["frames"]
        expect(sample["frame"] == frame_index, f"frame boundary at {sample['elapsed']}ms")
        actual = retained_image(sample["image"])
        with Image.open(confined(project, descriptor["path"])) as image:
            frame = image.convert("RGBA").crop((frame_index * width, 0, (frame_index + 1) * width, height))
        expected = Image.alpha_composite(Image.new("RGBA", frame.size, (*background, 255)), frame)
        expect(rgb_difference(expected, actual) <= 1, f"decoded frame crop at {sample['elapsed']}ms")
    playback = report.get("playback")
    if playback and playback["status"] == "observed":
        samples = playback["samples"]
        frame_ms, count = playback["frameMs"], playback["frameCount"]
        expect(frame_ms == report["display"]["frameMs"], "live playback uses consumer frame duration")
        expect(len(samples) >= count * 2 + 1, "live playback spans two complete loops")
        previous_time, previous_frame = -1, None
        wraps = 0
        for sample in samples:
            elapsed = sample["elapsed"]
            expect(elapsed > previous_time, "live playback clock advances")
            frame_index = int(elapsed // frame_ms) % count
            if previous_frame is not None:
                expect(frame_index == (previous_frame + 1) % count, "live playback observes consecutive frames without skips")
                if previous_frame == count - 1 and frame_index == 0:
                    wraps += 1
            expect({cell["consumer"] for cell in sample["cells"]} == {"statusCell", "compactStatus"}, "both live consumers observed")
            for cell in sample["cells"]:
                expect(cell["frame"] == frame_index, "live frame follows actual clock")
                source = confined(project, cell["descriptor"]["path"])
                expect(digest(source) == cell["sha256"], "live playback source identity")
                expect(cell["descriptor"]["frames"] == count, "live playback frame count matches consumer")
                with Image.open(source) as image:
                    frame = image.convert("RGBA").crop((frame_index * width, 0, (frame_index + 1) * width, height))
                expected = Image.alpha_composite(Image.new("RGBA", frame.size, (*background, 255)), frame)
                expected = expected.resize((width * cell["scale"], height * cell["scale"]), Image.Resampling.NEAREST)
                actual = retained_image(cell["image"])
                expect(actual.size == expected.size and rgb_difference(expected, actual) <= 1, "live painted frame matches source and nearest scale")
            previous_time, previous_frame = elapsed, frame_index
        expect(wraps >= 2, "live last-to-first boundary observed twice")
    elif playback:
        expect(playback["status"] == "unavailable" and bool(playback.get("reason")), "unavailable playback retains its reason")
        expect(not any(view["asset"]["available"] and view.get("geometryMatches") and view["descriptor"]["frames"] > 1 for view in report["views"]), "available animation requires observed live playback")
    return {"version": 1, "status": "pass" if not failures else "fail", "capture_sha256": digest(capture / "render.json"), "observations": observations, "failures": failures,
            "available_views": len(available), "missing": report["missing"],
            "scope": "Identities, observed DOM/canvas dimensions, screenshot correspondence, PNG compositing, nearest blocks, frame-boundary crops and live playback when retained. Not an artistic/style verdict or acceptance of absent members; clock/frame checks are not a judgment of motion quality."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--capture", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.project, args.capture)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
