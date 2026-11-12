"""Independent pixel/timing checks for authored sprite animation consumers.

Exact painting and clock facts do not establish gait, contact, identity or art quality.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops

FILES = {"capture.mjs", "server.mjs", "view.mjs", "index.html", "check.py", "observation.py"}
LIMITATIONS = [
    "Controlled frame steps and actual RAF playback are separate observations.",
    "Timing and pivot coordinates are authored consumer requirements, not universal animation rules.",
    "Correct painting does not establish good motion, planted contacts, identity or artistic acceptance.",
    "This browser fixture does not qualify another target engine or human acceptance.",
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def confined(root, name):
    root = Path(root).resolve()
    if (not isinstance(name, str) or "\\" in name or ":" in name or Path(name).is_absolute()
            or any(part in ("", ".", "..") for part in name.split("/"))):
        raise ValueError("Reference must be a canonical relative path")
    cursor = root
    for part in name.split("/"):
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError("Reference symlink unsupported")
    path = (root / name).resolve()
    if path == root or not path.is_relative_to(root):
        raise ValueError("Reference escapes root")
    return path


def expected_frame(clip, elapsed):
    duration = sum(frame["duration_ms"] for frame in clip["frames"])
    at = max(elapsed, 0) % duration if clip["loop"] else min(max(elapsed, 0), duration)
    for index, frame in enumerate(clip["frames"]):
        if at < frame["duration_ms"]:
            return index
        at -= frame["duration_ms"]
    return len(clip["frames"]) - 1


def check(project, capture, renderer=None):
    project, capture = Path(project).resolve(), Path(capture).resolve()
    renderer = Path(renderer).resolve() if renderer else Path(__file__).resolve().parent
    facts = {"pixel_checks": 0, "source_checks": 0, "clock_checks": 0, "phases": {}}
    failures = []

    def expect(value, label):
        if not value:
            failures.append(label)

    def image(ref):
        path = confined(capture, ref["path"])
        expect(digest(path) == ref["sha256"], "retained image hash: " + ref["path"])
        with Image.open(path) as raw:
            expect(raw.format == "PNG", "actual PNG: " + ref["path"])
            return raw.convert("RGBA")

    def matches(a, b):
        return a.size == b.size and max(hi for lo, hi in ImageChops.difference(a, b).getextrema()) <= 1

    try:
        report = json.loads((capture / "capture.json").read_bytes())
        launch = json.loads((capture / "launch.json").read_bytes())
        execution = json.loads((capture / "execution.json").read_bytes())
        inputs = json.loads((capture / "inputs.json").read_bytes())
        config, animation = report["config"], report["animation"]
        expect(report["consumer"] == execution["consumer"] == config["profile"] == "sprite-animation-v1", "profile identity")
        expect(execution["status"] == "complete" and execution["renderer_executed"] is True and execution["cleanup"]["complete"] is True, "actual completed and cleaned renderer")
        expect(all(Path(x["project"]).resolve() == project for x in (report, launch, inputs, execution)), "same consumer root")
        expect(not report["errors"], "no browser errors")
        expect(config == launch["config"] == inputs["config"] and animation == launch["animation"], "captured source contract/config unchanged")
        config_ref = report["config_file"]
        expect(config_ref == inputs["config_file"] and digest(confined(project, config_ref["path"])) == config_ref["sha256"] == report["served_files"]["config"], "exact requested/served configuration")
        expect(report["inputs"] == report["final_inputs"] == inputs["files"], "unchanged input identities")
        current_sources = {p.relative_to(project).as_posix() for p in (project / "src").rglob("*") if p.is_file()}
        expect(set(inputs["files"]) == current_sources | set(config["destinations"].values()), "complete current source and destination closure")
        for name, expected in inputs["files"].items():
            expect(digest(confined(project, name)) == expected, "exact consumer input: " + name)
            facts["source_checks"] += 1
        expect(set(report["renderer_files"]) == FILES and report["renderer_files"] == launch["renderer_files"] == inputs["renderer_files"], "complete renderer closure")
        for name, expected in report["renderer_files"].items():
            expect(digest(confined(renderer, name)) == expected, "exact renderer source: " + name)
            facts["source_checks"] += 1
        for name, expected in report["served_files"].items():
            if name.startswith("consumer/"):
                expect(inputs["files"].get(name[9:]) == expected, "exact served consumer input: " + name)
            elif name.startswith("renderer/"):
                expect(report["renderer_files"].get(name[9:]) == expected, "exact served display input: " + name)
            else:
                expect(name == "config", "known served namespace")
        expect(report["served_files"].get("consumer/" + config["modules"]["animation"]) == inputs["files"][config["modules"]["animation"]], "actual animation module served")
        expect(set(config["scales"]) and len(set(config["scales"])) == len(config["scales"]), "unique scales")
        expect(animation["sampling"] == "nearest" and len(animation["viewport"]) == 2, "declared viewport and sampling")
        clips = {c["id"]: c for c in animation["clips"]}
        expect(len(clips) == len(animation["clips"]) and 1 <= len(clips) <= 4, "unique bounded clips")
        paths = {f["path"] for c in clips.values() for f in c["frames"]}
        expect(paths == set(config["destinations"].values()), "every destination used in the actual clip contract")
        sources = {}
        for path in paths:
            expect(report["served_files"].get("consumer/" + path) == inputs["files"][path], "actual served asset: " + path)
            with Image.open(confined(project, path)) as raw:
                expect(raw.format == "PNG", "source PNG: " + path)
                sources[path] = raw.convert("RGBA")
        for clip in clips.values():
            expect(type(clip["loop"]) is bool and 2 <= len(clip["frames"]) <= 16, "bounded clip policy: " + clip["id"])
            expect(len({f["id"] for f in clip["frames"]}) == len(clip["frames"]), "unique frame IDs")
            for f in clip["frames"]:
                expect(type(f["duration_ms"]) is int and f["duration_ms"] > 0, "positive authored frame duration")
                x, y, w, h = f["rect"]
                expect(all(type(n) is int for n in f["rect"]) and x >= 0 and y >= 0 and w > 0 and h > 0 and x + w <= sources[f["path"]].width and y + h <= sources[f["path"]].height, "valid source crop")
        viewport = report["viewport"]
        expect(viewport == {"width": launch["viewport"]["width"], "height": launch["viewport"]["height"], "device_scale_factor": 1}, "viewport binding")

        def painted(view, screenshot=False):
            clip, index, scale = clips[view["clip"]], view["frame"], view["scale"]
            f = clip["frames"][index]
            label = f"{clip['id']}@{scale}/{index}"
            expect(view["path"] == view["asset"]["path"] == f["path"] and view["asset"]["sha256"] == inputs["files"][f["path"]], "painted exact asset: " + label)
            expect(view["pivot"] == f["pivot"] and view["anchor"] == clip["anchor"] and view["source_rect"] == f["rect"] and view["frame_id"] == f["id"], "authored placement: " + label)
            expect(view["smoothing"] is False and view["imageRendering"] == "pixelated", "nearest paint: " + label)
            expect([view["asset"]["width"], view["asset"]["height"]] == list(sources[f["path"]].size), "decoded source geometry")
            background = tuple(int(animation["background"][i:i+2], 16) for i in (1, 3, 5)) + (255,)
            expected = Image.new("RGBA", tuple(animation["viewport"]), background)
            x, y, w, h = f["rect"]
            expected.alpha_composite(sources[f["path"]].crop((x, y, x+w, y+h)), (clip["anchor"][0]-f["pivot"][0], clip["anchor"][1]-f["pivot"][1]))
            expected = expected.resize((expected.width*scale, expected.height*scale), Image.Resampling.NEAREST)
            actual = image(view["image"])
            expect(matches(expected, actual), "actual crop/anchor/nearest pixels: " + label)
            facts["pixel_checks"] += 1
            if screenshot:
                shot = image(view["screenshot"])
                expect(shot.size == (viewport["width"], viewport["height"]), "screenshot dimensions")
                r = view["rect"]
                values = [r[k] for k in ("x", "y", "width", "height")]
                expect(all(type(v) in (int, float) and v == int(v) for v in values), "integer screenshot placement")
                xx, yy, ww, hh = map(int, values)
                expect((ww, hh) == actual.size and xx >= 0 and yy >= 0 and xx+ww <= shot.width and yy+hh <= shot.height, "visible canvas placement")
                expect(matches(actual, shot.crop((xx, yy, xx+ww, yy+hh))), "actual screenshot pixels: " + label)
                facts["pixel_checks"] += 1

        expected_views = {(c["id"], index, scale) for c in clips.values() for index in range(len(c["frames"])) for scale in config["scales"]}
        expect(len(report["views"]) == len(expected_views) and {(v["clip"], v["frame"], v["scale"]) for v in report["views"]} == expected_views, "complete controlled frame/scale inventory")
        for view in report["views"]:
            expect(view["kind"] == "controlled-step", "step evidence labeled separately")
            painted(view, True)
        expected_plays = {(c, s) for c in clips for s in config["scales"]}
        expect(len(report["playbacks"]) == len(expected_plays) and {(p["clip"], p["scale"]) for p in report["playbacks"]} == expected_plays, "complete real playback inventory")
        counts, total = {}, 0
        for playback in report["playbacks"]:
            clip, ticks, samples = clips[playback["clip"]], playback["ticks"], playback["samples"]
            expect(playback["status"] == "observed" and playback["loop"] is clip["loop"], "actual completed playback")
            last_time, last_frame = -1, None
            transitions = wraps = skips = 0
            changes, frames = [], set()
            for tick in ticks:
                elapsed, index = tick["elapsed_ms"], tick["frame"]
                expect(type(elapsed) in (int, float) and math.isfinite(elapsed) and elapsed > last_time, "strict actual RAF clock")
                expect(type(index) is int and index == expected_frame(clip, elapsed), "authored uneven-duration frameAt")
                if last_frame is None or index != last_frame:
                    changes.append((elapsed, index))
                    if last_frame is not None:
                        transitions += 1
                        wraps += int(index == 0 and last_frame == len(clip["frames"])-1)
                        skips += int(index != (last_frame+1) % len(clip["frames"]))
                    last_frame = index
                frames.add(index)
                last_time = elapsed
                facts["clock_checks"] += 1
            expect(bool(ticks) and ticks[0]["elapsed_ms"] == 0, "playback starts at its own actual RAF origin")
            expect([(s["elapsed_ms"], s["frame"]) for s in samples] == changes, "every observed transition retains actual painted PNG")
            expect(set(frames) == set(range(len(clip["frames"]))) and skips == 0, "every frame observed without skipped transitions")
            expect(playback["frames"] == sorted(frames) and playback["transitions"] == transitions and playback["wraps"] == wraps and playback["skips"] == skips, "measured playback counts")
            expect(wraps >= config["observed_wraps"] if clip["loop"] else last_time >= sum(f["duration_ms"] for f in clip["frames"]) and last_frame == len(clip["frames"])-1, "actual loop wraps or one-shot terminal hold")
            for sample in samples:
                expect(sample["clip"] == clip["id"] and sample["scale"] == playback["scale"], "playback sample identity")
                painted(sample)
            total += len(samples)
            counts[f"{clip['id']}@{playback['scale']}x"] = {"frames": sorted(frames), "transitions": transitions, "wraps": wraps, "skips": skips}
        facts["phases"]["playback"] = {"status": "observed", "sample_count": total, "counts": counts}
    except (OSError, ValueError, KeyError, TypeError, IndexError, ZeroDivisionError) as error:
        failures.append("Malformed or unavailable capture: " + str(error))
    return {"version": 1, "status": "fail" if failures else "pass", "pass": not failures,
            "facts": facts, "failures": failures, "limitations": LIMITATIONS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("project", "capture", "out"):
        parser.add_argument("--"+name, type=Path, required=True)
    args = parser.parse_args()
    result = check(args.project, args.capture)
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "pass": result["pass"], "path": str(args.out)}))
    return not result["pass"]


if __name__ == "__main__":
    raise SystemExit(main())
