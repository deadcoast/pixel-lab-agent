"""Check retained tile mapping and pixels; seam quality remains visual review."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageColor

PROFILE_FILES = {"capture.mjs", "server.mjs", "view.mjs", "index.html", "check.py", "observation.py"}
LIMITATIONS = [
    "Binary corner weights NW=1, NE=2, SE=4, SW=8 are this explicit consumer contract, not a universal tile convention.",
    "Exact mapping, compositing and screenshot pixels do not establish seam quality, material continuity, artistic acceptance or another engine's behavior.",
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def confined(root, name):
    root = Path(root).resolve()
    if not isinstance(name, str) or "\\" in name or ":" in name or Path(name).is_absolute() or any(p in ("", ".", "..") for p in name.split("/")):
        raise ValueError("Noncanonical relative reference")
    requested = root / name
    actual = requested.resolve()
    if actual == root or not actual.is_relative_to(root) or actual != requested:
        raise ValueError("Reference escapes or redirects its root")
    return actual


def configuration(config):
    if set(config) != {"version", "profile", "modules", "destinations", "scales", "timeout_seconds"} or config["version"] != 1 or config["profile"] != "tile-neighborhood-v1":
        raise ValueError("Invalid tile profile configuration")
    if set(config["modules"]) != {"terrain"} or not re.fullmatch(r"src/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_.-]+\.(?:js|mjs|ts)", config["modules"]["terrain"]):
        raise ValueError("One terrain module under src required")
    paths = list(config["destinations"].values())
    if len(paths) != 16 or len(set(paths)) != 16 or any(not p.startswith("assets/") or not p.endswith(".png") for p in paths):
        raise ValueError("Exactly 16 PNG destinations required")
    for path in paths:
        confined(Path.cwd(), path)
    scales = config["scales"]
    if not isinstance(scales, list) or not 1 <= len(scales) <= 4 or len(set(scales)) != len(scales) or any(type(v) is not int or not 1 <= v <= 16 for v in scales):
        raise ValueError("Invalid scales")
    if type(config["timeout_seconds"]) is not int or not 5 <= config["timeout_seconds"] <= 180:
        raise ValueError("Invalid timeout")


def check(project, capture, renderer=None):
    project, capture = Path(project).resolve(), Path(capture).resolve()
    renderer = Path(renderer).resolve() if renderer else Path(__file__).resolve().parent
    report_path = capture / "capture.json"
    failures, facts = [], {"pixel_checks": 0, "source_checks": 0, "screenshot_checks": 0, "clock_checks": 0, "phases": {}}
    if not report_path.is_file():
        return {"version": 1, "status": "unavailable", "pass": False, "facts": facts, "failures": [], "limitations": ["No browser capture available", *LIMITATIONS]}

    def expect(value, label):
        if not value:
            failures.append(label)

    def png(reference):
        path = confined(capture, reference["path"])
        expect(digest(path) == reference["sha256"], "retained image bytes: " + reference["path"])
        with Image.open(path) as image:
            expect(image.format == "PNG", "retained PNG format")
            return image.convert("RGBA")

    def matches(expected, actual):
        return expected.size == actual.size and max(high for _, high in ImageChops.difference(expected, actual).getextrema()) <= 1

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        execution, inputs, launch = [json.loads((capture / name).read_text(encoding="utf-8")) for name in ("execution.json", "inputs.json", "launch.json")]
        expect(report["version"] == 1 and report["consumer"] == "tile-neighborhood-v1", "fixed profile identity")
        expect(execution["consumer"] == report["consumer"] and execution["renderer_executed"] is True and execution["status"] == "complete", "actual complete renderer execution")
        expect(execution["cleanup"]["complete"] is True and all(execution["cleanup"][key] is True for key in ("browser_closed", "server_closed", "profile_removed")), "owned browser/server/profile cleanup")
        expect(all(Path(v["project"]).resolve() == project for v in (report, execution, inputs, launch)), "same project")
        config = report["config"]
        configuration(config)
        expect(config == launch["config"], "launch configuration identity")
        expect(report["config_ref"] == inputs["config"] == launch["config_ref"], "configuration byte binding")
        config_path = Path(report["config_ref"]["path"])
        expect(digest(config_path) == report["config_ref"]["sha256"] and json.loads(config_path.read_text(encoding="utf-8")) == config, "unchanged configuration")
        source_paths = sorted(p.relative_to(project).as_posix() for p in (project / "src").rglob("*") if p.is_file())
        expect(source_paths == report["source_files"] == inputs["source_files"], "complete source closure")
        expected_inputs = set(source_paths) | set(config["destinations"].values())
        expect(set(report["inputs"]) == expected_inputs, "complete input closure")
        expect(report["inputs"] == report["final_inputs"] == inputs["files"], "unchanged inputs across capture")
        for name in expected_inputs:
            expect(digest(confined(project, name)) == report["inputs"].get(name), "input bytes: " + name)
            facts["source_checks"] += 1
        expect(set(report["renderer_files"]) == PROFILE_FILES, "complete renderer closure")
        expect(report["renderer_files"] == inputs["renderer_files"] == launch["renderer_files"], "same renderer identities")
        for name, expected in report["renderer_files"].items():
            expect(digest(confined(renderer, name)) == expected, "renderer bytes: " + name)
            facts["source_checks"] += 1
        required_served = {"consumer/" + p for p in config["destinations"].values()} | {"consumer/" + config["modules"]["terrain"], "renderer/index.html", "renderer/view.mjs"}
        allowed_served = {"consumer/" + p for p in expected_inputs} | {"renderer/index.html", "renderer/view.mjs"}
        expect(required_served <= set(report["served_files"]) <= allowed_served, "required and confined served resources")
        for key, expected in report["served_files"].items():
            group, name = key.split("/", 1)
            expect(digest(confined(project if group == "consumer" else renderer, name)) == expected, "exact served bytes: " + key)
            facts["source_checks"] += 1
        expect(not report["errors"], "no browser errors")
        expect(bool(report["browser_version"]["product"]), "actual browser identity")
        terrain = report["terrain"]
        expect(set(terrain) == {"tile_size", "background", "sampling", "corner_order", "tiles", "neighborhoods"}, "closed terrain declaration")
        tw, th = terrain["tile_size"]
        if not all(type(v) is int and 1 <= v <= 64 for v in (tw, th)):
            raise ValueError("Invalid tile dimensions")
        expect(terrain["sampling"] == "nearest" and terrain["corner_order"] == ["nw", "ne", "se", "sw"], "declared sampling and corner convention")
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", terrain["background"]):
            raise ValueError("Invalid background")
        background = (*ImageColor.getrgb(terrain["background"]), 255)
        ids = {str(i) for i in range(16)}
        expect(set(terrain["tiles"]) == set(report["tile_assets"]) == ids, "all 16 tile patterns")
        expect({v["path"] for v in terrain["tiles"].values()} == set(config["destinations"].values()), "exact tile destination coverage")
        images = {}
        for ident in ids:
            declaration, asset = terrain["tiles"][ident], report["tile_assets"][ident]
            expect(set(declaration) == {"path"}, "one source tile path")
            name = declaration["path"]
            expect(asset["path"] == name and asset["sha256"] == report["inputs"][name] == report["served_files"].get("consumer/" + name), "exact tile bytes: " + ident)
            expect((asset["width"], asset["height"]) == (tw, th), "browser tile geometry: " + ident)
            with Image.open(confined(project, name)) as image:
                expect(image.format == "PNG" and image.size == (tw, th), "source tile geometry: " + ident)
                images[ident] = image.convert("RGBA")
        neighborhoods = terrain["neighborhoods"]
        if not isinstance(neighborhoods, list) or not 1 <= len(neighborhoods) <= 16:
            raise ValueError("Invalid neighborhood count")
        maps, pixels, patterns = {}, 0, set()
        for n in neighborhoods:
            if set(n) != {"id", "label", "vertices"} or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", n["id"]) or n["id"] in maps or not isinstance(n["label"], str) or not 1 <= len(n["label"]) <= 120:
                raise ValueError("Invalid neighborhood identity")
            vertices = n["vertices"]
            if not isinstance(vertices, list) or not 2 <= len(vertices) <= 17 or not isinstance(vertices[0], list) or not 2 <= len(vertices[0]) <= 17 or any(not isinstance(row, list) or len(row) != len(vertices[0]) or any(type(v) is not int or v not in (0, 1) for v in row) for row in vertices):
                raise ValueError("Invalid binary vertex grid")
            maps[n["id"]] = n
            for row in range(len(vertices) - 1):
                for col in range(len(vertices[0]) - 1):
                    corners = [vertices[row][col], vertices[row][col + 1], vertices[row + 1][col + 1], vertices[row + 1][col]]
                    patterns.add(sum(v * 2 ** bit for bit, v in enumerate(corners)))
            for scale in config["scales"]:
                w, h = (len(vertices[0]) - 1) * tw * scale, (len(vertices) - 1) * th * scale
                if w > 2048 or h > 2048:
                    raise ValueError("Scaled canvas exceeds bounds")
                pixels += w * h
        expect(patterns == set(range(16)), "neighborhoods exercise every binary corner pattern")
        if pixels > 16 * 1024 * 1024:
            raise ValueError("Capture exceeds pixel bound")
        wanted = {(ident, scale) for ident in maps for scale in config["scales"]}
        expect(len(report["views"]) == len(wanted) and {(v["neighborhood"], v["scale"]) for v in report["views"]} == wanted, "every neighborhood and scale exactly once")
        viewport = report["viewport"]
        expect(viewport["device_scale_factor"] == 1 and 900 <= viewport["width"] <= 2120 and 700 <= viewport["height"] <= 2348, "bounded viewport")
        for view in report["views"]:
            ident, scale = view["neighborhood"], view["scale"]
            n = maps[ident]
            vertices = n["vertices"]
            rows, columns = len(vertices) - 1, len(vertices[0]) - 1
            label = f"{ident}@{scale}"
            expect(view["label"] == n["label"] and (view["rows"], view["columns"]) == (rows, columns), "view geometry: " + label)
            expected = Image.new("RGBA", (columns * tw, rows * th), background)
            expected_cells = []
            for row in range(rows):
                for col in range(columns):
                    corners = [vertices[row][col], vertices[row][col + 1], vertices[row + 1][col + 1], vertices[row + 1][col]]
                    tile = str(sum(v * 2 ** bit for bit, v in enumerate(corners)))
                    name = terrain["tiles"][tile]["path"]
                    expected_cells.append({"row": row, "column": col, "corners": corners, "tile": tile, "path": name, "sha256": report["inputs"][name]})
                    expected.alpha_composite(images[tile], (col * tw, row * th))
            expect(view["cells"] == expected_cells, "actual tileFor mapping against declared corners: " + label)
            expect(view["smoothing"] is False and view["imageRendering"] == "pixelated", "nearest sampling: " + label)
            expect(view["image"]["path"] == f"{ident}-{scale}x.png" and view["screenshot"]["path"] == f"{ident}-{scale}x-destination.png", "distinct view outputs: " + label)
            expected = expected.resize((columns * tw * scale, rows * th * scale), Image.Resampling.NEAREST)
            actual, screenshot = png(view["image"]), png(view["screenshot"])
            expect(matches(expected, actual), "source compositing and nearest pixels: " + label)
            facts["pixel_checks"] += 1
            expect(screenshot.size == (viewport["width"], viewport["height"]), "screenshot viewport: " + label)
            values = [view["rect"][key] for key in ("x", "y", "width", "height")]
            expect(all(type(v) in (int, float) and int(v) == v for v in values), "integer canvas placement: " + label)
            x, y, w, h = map(int, values)
            expect((w, h) == actual.size and x >= 0 and y >= 0 and x + w <= viewport["width"] and y + h <= viewport["height"], "visible canvas: " + label)
            expect(matches(actual, screenshot.crop((x, y, x + w, y + h))), "actual screenshot canvas pixels: " + label)
            facts["screenshot_checks"] += 1
    except (KeyError, TypeError, ValueError, OSError, IndexError, AttributeError) as error:
        failures.append("Malformed or unavailable retained input: " + str(error))
    return {"version": 1, "status": "fail" if failures else "pass", "pass": not failures, "capture_sha256": digest(report_path), "facts": facts, "failures": failures, "limitations": LIMITATIONS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("project", "capture", "out"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    result = check(args.project, args.capture)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "pass": result["pass"], "path": str(args.out)}))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
