"""Verify retained successor browser pixels/identities across preference phases; visual and family judgments are separate."""

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


def check(project, capture, baseline=None):
    project, capture = Path(project).resolve(), Path(capture).resolve()
    render = json.loads((capture / "render.json").read_text(encoding="utf-8"))
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

    here = Path(__file__).resolve().parent
    for name, expected in render.get("renderer_files", {}).items():
        expect(digest(confined(here, name)) == expected, "renderer implementation: " + name)
    for name, expected in render["served_files"].items():
        group, relative = name.split("/", 1)
        base = project if group == "consumer" else here
        expect(digest(confined(base, relative)) == expected, "served bytes: " + name)
    expect("consumer/src/queue-view-successor.ts" in render["served_files"], "fixture executed the successor consumer module")
    expect("consumer/src/queue-view.ts" not in render["served_files"], "fixture did not execute the retained original consumer module")
    if baseline:
        baseline_files = json.loads(Path(baseline).read_text(encoding="utf-8"))["files"]
        for name in ["src/queue-view.ts", "src/queue.ts", "renderer/view.mjs", "renderer/check.py", "renderer/capture.mjs", "renderer/server.mjs", "renderer/index.html", "assets/start.svg", "assets/working.png", "assets/ready-confirmed.png", "assets/paused.png", "assets/error-retry.png"]:
            expect(digest(confined(project, name)) == baseline_files.get(name), "retained file unchanged since baseline: " + name)

    sessions = {phase["report"]["sessionId"] for phase in render["phases"]}
    expect(len(sessions) == 1, "all phases observed in one open page session")
    phase_names = [phase["name"] for phase in render["phases"]]
    for phase in render["phases"]:
        report = phase["report"]
        label_prefix = f"[{phase['name']}] "
        motion = report["motion"]
        expect(not report["errors"], label_prefix + "browser reported no script errors")
        expect(report["devicePixelRatio"] == 1, label_prefix + "capture declares device pixel ratio one")
        expected_motion = {"normal-start": "normal", "reduced": "reduced", "normal-restored": "normal"}.get(phase["name"])
        if expected_motion:
            expect(motion == expected_motion and report["mediaMatches"] == (motion == "reduced"), label_prefix + f"preference resolved to {expected_motion}")
        screenshot = retained_image(phase["screenshot"])
        expect(screenshot.size == (report["viewport"]["width"], report["viewport"]["height"]), label_prefix + "screenshot and observed viewport dimensions")
        width, height = report["display"]["cell"]
        background = ImageColor.getrgb(report["display"]["background"])
        frame_ms = report["display"]["frameMs"]

        def expected_frame(descriptor, elapsed):
            if descriptor["animate"]:
                return (int(elapsed) // frame_ms) % descriptor["frames"]
            return descriptor["holdFrame"]

        def check_descriptor(descriptor, label):
            sheet_frames = descriptor["frames"]
            should_animate = motion == "normal" and sheet_frames > 1
            expect(descriptor["motion"] == motion, label + " descriptor carries the current preference")
            expect(descriptor["animate"] == should_animate, label + f" animate flag follows preference ({'animates' if should_animate else 'stationary'})")
            expect(descriptor["holdFrame"] == (None if should_animate else descriptor["still"]), label + " hold frame is the declared still cell when stationary")

        def check_view(view, label, screenshot_match=True):
            if not view["asset"]["available"]:
                expect("image" not in view, label + " missing asset has no invented view")
                return None
            actual = retained_image(view["image"])
            descriptor = view["descriptor"]
            scale = view["scale"]
            check_descriptor(descriptor, label)
            expect(view["geometryMatches"], label + " source sheet geometry")
            expect(view["smoothing"] is False and view["imageRendering"] == "pixelated", label + " nearest sampling settings")
            expect(actual.size == (width * scale, height * scale), label + " actual canvas dimensions")
            bounds = view["bounds"]
            expect(all(value == int(value) for value in bounds.values()), label + " integer destination bounds")
            if screenshot_match:
                x, y = int(bounds["x"]), int(bounds["y"])
                on_screen = screenshot.crop((x, y, x + actual.width, y + actual.height))
                expect(ImageChops.difference(on_screen, actual).convert("RGB").getbbox() is None, label + " screenshot matches canvas pixels")
            source = confined(project, descriptor["path"])
            expect(digest(source) == view["asset"]["sha256"], label + " actual asset identity")
            if source.suffix.lower() == ".png":
                with Image.open(source) as image:
                    expect(image.size == (width * descriptor["frames"], height), label + " independently decoded sheet size")
                    frame = image.convert("RGBA").crop((view["frame"] * width, 0, (view["frame"] + 1) * width, height))
                expected = Image.alpha_composite(Image.new("RGBA", frame.size, (*background, 255)), frame).resize(actual.size, Image.Resampling.NEAREST)
                expect(rgb_difference(expected, actual) <= 1, label + " source pixels and alpha compositing (rounding tolerance one)")
            return actual

        for view in report["views"]:
            label = label_prefix + f"{view['consumer']} {view['state']} {view['scale']}x"
            actual = check_view(view, label)
            if actual is None:
                continue
            expect(view["frame"] == (0 if view["descriptor"]["animate"] else view["descriptor"]["holdFrame"]), label + " matrix cell painted at elapsed 0 shows the expected cell")
            source = confined(project, view["descriptor"]["path"])
            if view["scale"] != 1 and source.suffix.lower() == ".png":
                base = next(v for v in report["views"] if v["consumer"] == view["consumer"] and v["state"] == view["state"] and v["scale"] == 1)
                native = retained_image(base["image"]).resize(actual.size, Image.Resampling.NEAREST)
                expect(ImageChops.difference(native, actual).convert("RGB").getbbox() is None, label + " nearest pixel blocks")
        labels = {view["state"]: view["descriptor"]["label"] for view in report["views"]}
        expect(labels == {"idle": "Start", "running": "Working", "paused": "Paused", "succeeded": "Ready", "failed": "Retry"}, label_prefix + "state labels through both consumers")
        running_views = [view for view in report["views"] if view["state"] == "running"]
        expect({view["consumer"] for view in running_views} == {"statusCell", "compactStatus"}, label_prefix + "running state rendered through both consumers")
        descriptors = {json.dumps({k: v for k, v in view["descriptor"].items()}, sort_keys=True) for view in running_views}
        expect(len(descriptors) == 1, label_prefix + "both consumers return the identical running descriptor under this preference")

        live_states = {cell["state"] for cell in report["live"]}
        expect(live_states == {"running"}, label_prefix + "live cells show the running state at capture time")
        for cell in report["live"]:
            label = label_prefix + f"live {cell['consumer']} {cell['state']} {cell['scale']}x"
            check_view(cell, label, screenshot_match=False)  # Live cells keep animating after the canvas snapshot in normal motion.
            if cell["asset"]["available"]:
                if cell["descriptor"]["animate"]:
                    expect(cell["frame"] == (int(cell["elapsed"]) // frame_ms) % cell["descriptor"]["frames"] or abs(cell["elapsed"] % frame_ms) < 40 or abs(cell["elapsed"] % frame_ms) > frame_ms - 40, label + " live frame agrees with elapsed time (frame-boundary tolerance)")
                else:
                    expect(cell["frame"] == cell["descriptor"]["holdFrame"], label + " live cell holds the still cell under reduced motion")
                    x, y = int(cell["bounds"]["x"]), int(cell["bounds"]["y"])
                    actual = retained_image(cell["image"])
                    on_screen = screenshot.crop((x, y, x + actual.width, y + actual.height))
                    expect(ImageChops.difference(on_screen, actual).convert("RGB").getbbox() is None, label + " stationary live cell matches the screenshot")

        for sample in report["timeline"]:
            label = label_prefix + f"timeline {sample['consumer']} {sample['state']} at {sample['elapsed']}ms"
            if not sample["available"]:
                expect(sample["frame"] is None and "image" not in sample, label + " missing animation is not a playback result")
                continue
            descriptor = sample["descriptor"]
            check_descriptor(descriptor, label)
            expect(sample["frame"] == expected_frame(descriptor, sample["elapsed"]), label + f" frame index {'advances' if descriptor['animate'] else 'holds'} as specified")
            actual = retained_image(sample["image"])
            with Image.open(confined(project, descriptor["path"])) as image:
                frame = image.convert("RGBA").crop((sample["frame"] * width, 0, (sample["frame"] + 1) * width, height))
            expected = Image.alpha_composite(Image.new("RGBA", frame.size, (*background, 255)), frame)
            expect(rgb_difference(expected, actual) <= 1, label + " decoded frame crop")
        working_timeline = [s for s in report["timeline"] if s["state"] == "running" and s["available"]]
        frames_seen = {s["frame"] for s in working_timeline}
        if motion == "normal":
            expect(frames_seen == {0, 1, 2, 3}, label_prefix + "normal motion cycles through all four cells including the wrap")
        else:
            expect(frames_seen == {0}, label_prefix + "reduced motion never leaves the held cell")
        for transition in report["transitions"]:
            expect(transition["motion"] == motion and all(c["descriptor"]["motion"] == motion for c in transition["consumers"]), label_prefix + f"transition {transition['event']} -> {transition['state']} consulted the current preference in both consumers")

    # Preference switch while open: the reduced phase must record the change event and in-place repaint.
    def phase(name):
        return next((p for p in render["phases"] if p["name"] == name), None)

    reduced, restored = phase("reduced"), phase("normal-restored")
    if reduced:
        events = [e for e in reduced["report"]["preferenceEvents"] if e["to"] == "reduced"]
        expect(len(events) >= 1, "[switch] change event observed when the preference became reduced")
        if events:
            repainted = events[-1]["repainted"]
            running = [r for r in repainted if r["state"] == "running"]
            expect({r["consumer"] for r in running} == {"statusCell", "compactStatus"}, "[switch] both consumers' Working cells repainted on the change event")
            expect(all(r["animate"] is False and r["frame"] == r["holdFrame"] for r in running), "[switch] every Working cell stopped on the held cell without reload")
            expect(any(r["live"] for r in running), "[switch] live Working cells were among the repainted cells")
            expect(events[-1]["sessionId"] == reduced["report"]["sessionId"], "[switch] change event belongs to the same page session")
    if restored:
        events = [e for e in restored["report"]["preferenceEvents"] if e["to"] == "normal"]
        expect(len(events) >= 1, "[switch] change event observed when the preference returned to normal")
        if events:
            running = [r for r in events[-1]["repainted"] if r["state"] == "running"]
            expect(all(r["animate"] is True and r["holdFrame"] is None for r in running), "[switch] Working cells resumed animation after the preference returned to normal")
    return {"version": 2, "status": "pass" if not failures else "fail", "capture_sha256": digest(capture / "render.json"), "phases": phase_names, "observations": observations, "failures": failures,
            "scope": "Identities, observed DOM/canvas dimensions, screenshot pixel correspondence, PNG alpha compositing, nearest blocks, frame-boundary crops, descriptor behaviour under each preference and the in-session preference switch. Not an artistic/style verdict; it does not judge whether the held cell reads as Working."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--capture", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, default=None, help="hash map of retained files that must be unchanged")
    args = parser.parse_args()
    result = check(args.project, args.capture, args.baseline)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "pass" else 1)
