"""Independently check queue-motion-v1 source bytes, PNG pixels and observed clocks.

These checks establish a bounded queue fixture observation, never visual quality
or production acceptance. Partial captures and unavailable capabilities stay open.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageColor

PROFILE_FILES = {"capture.mjs", "server.mjs", "view.mjs", "index.html", "check.py", "observation.py"}
PHASES = ("normal-start", "reduced", "normal-restored", "initially-reduced")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def confined(root, name):
    root = Path(root).resolve()
    if not isinstance(name, str) or "\\" in name or Path(name).is_absolute() or any(p in ("", ".", "..") for p in name.split("/")):
        raise ValueError("Reference is not a canonical relative path")
    actual = (root / name).resolve()
    if actual == root or not actual.is_relative_to(root):
        raise ValueError("Reference escapes its root")
    return actual


def count_frames(frames, count):
    """Count real adjacent transitions only; duplicate paints add no wraps."""
    result = {"frames": [], "transitions": 0, "wraps": 0, "skips": 0, "last": None}
    for frame in frames:
        if not isinstance(frame, int) or isinstance(frame, bool) or not 0 <= frame < count:
            raise ValueError("Frame outside the source descriptor")
        if frame not in result["frames"]:
            result["frames"].append(frame)
        previous = result["last"]
        if previous is not None and frame != previous:
            result["transitions"] += 1
            if frame != (previous + 1) % count:
                result["skips"] += 1
            elif previous == count - 1 and frame == 0:
                result["wraps"] += 1
        result["last"] = frame
    return result


def check(project, capture, renderer=None):
    project, capture = Path(project).resolve(), Path(capture).resolve()
    renderer = Path(renderer).resolve() if renderer else Path(__file__).resolve().parent
    failures, limitations, facts = [], [], {"phases": {}, "pixel_checks": 0, "source_checks": 0, "clock_checks": 0}
    report_path = capture / "capture.json"
    if not report_path.is_file():
        return {"version": 1, "status": "unavailable", "pass": False, "facts": facts, "failures": [], "limitations": ["No browser capture was produced"]}

    def expect(value, label):
        if not value:
            failures.append(label)

    try:
        report = json.loads(report_path.read_bytes())
        launch = json.loads((capture / "launch.json").read_bytes())
        execution = json.loads((capture / "execution.json").read_bytes())
        expect(report["version"] == 1 and report["profile"] == "queue-motion-v1", "fixed profile identity")
        expect(Path(report["project"]).resolve() == project == Path(launch["project"]).resolve(), "same consumer project")
        config = report["config"]
        expect(config == launch["config"], "executed config identity")
        scales = config["scales"]
        expect(isinstance(scales, list) and 1 <= len(scales) <= 4 and len(set(scales)) == len(scales) and all(type(x) is int and 1 <= x <= 16 for x in scales), "bounded scales")
        for key, low, high in (("observed_wraps",1,10),("phase_timeout_ms",1000,30000),("hold_ms",100,5000),("timeout_seconds",5,180)):
            expect(type(config[key]) is int and low <= config[key] <= high, "bounded " + key)
        expect(set(report["renderer_files"]) == PROFILE_FILES, "complete executed renderer closure")
        expect(report["renderer_files"] == launch["renderer_files"], "launch renderer identities")
        for name, expected in report["renderer_files"].items():
            expect(digest(confined(renderer, name)) == expected, "renderer bytes: " + name)
            facts["source_checks"] += 1
        for key, expected in report["served_files"].items():
            group, name = key.split("/", 1)
            expect(group in ("consumer", "renderer"), "served source namespace")
            expect(digest(confined(project if group == "consumer" else renderer, name)) == expected, "served bytes: " + key)
            facts["source_checks"] += 1
        for module in config["modules"].values():
            expect("consumer/" + module in report["served_files"], "configured module actually served: " + module)
        expect(not report["errors"], "no browser script errors")
        expect(execution["cleanup"]["complete"], "owned browser/server/profile cleanup complete")
        width, height = report["display"]["cell"]
        background = ImageColor.getrgb(report["display"]["background"])
        if len(background) == 4:
            background = background[:3]
        expect(report["display"]["filter"] == "nearest", "consumer nearest sampling")
        expect(report["viewport"]["device_scale_factor"] == 1, "device scale factor one")

        def retained_image(reference):
            path = confined(capture, reference["path"])
            expect(digest(path) == reference["sha256"], "retained PNG bytes: " + reference["path"])
            with Image.open(path) as image:
                expect(image.format == "PNG", "retained image is PNG")
                return image.convert("RGBA")

        unavailable_inputs = False

        def cell_pixels(cell, label):
            nonlocal unavailable_inputs
            descriptor, asset = cell["descriptor"], cell["asset"]
            expect(descriptor["path"] == asset["path"], label + " descriptor asset identity")
            if not asset["available"] or not cell["geometryMatches"] or "image" not in cell:
                unavailable_inputs = True
                limitations.append(label + ": unavailable image or geometry")
                return False
            source = confined(project, descriptor["path"])
            expect(digest(source) == asset["sha256"] == report["served_files"].get("consumer/" + descriptor["path"]), label + " exact served asset")
            actual = retained_image(cell["image"])
            expect(actual.size == (width * cell["scale"], height * cell["scale"]), label + " canvas size")
            expect(cell["smoothing"] is False and cell["imageRendering"] == "pixelated", label + " literal sampling settings")
            if source.suffix.lower() == ".png":
                with Image.open(source) as image:
                    expect(image.size == (width * descriptor["frames"], height), label + " sheet geometry")
                    frame = image.convert("RGBA").crop((cell["frame"] * width, 0, (cell["frame"] + 1) * width, height))
                expected = Image.alpha_composite(Image.new("RGBA", frame.size, (*background, 255)), frame).resize(actual.size, Image.Resampling.NEAREST)
                difference = ImageChops.difference(expected, actual).getextrema()
                expect(max(high for low, high in difference) <= 1, label + " source pixels/alpha/nearest scale")
                facts["pixel_checks"] += 1
            else:
                limitations.append(label + ": source decoded in browser; independent pixel comparison supports PNG only")
            return True

        for reference in report["screenshots"]:
            image = retained_image(reference)
            expect(image.size == (report["viewport"]["width"], report["viewport"]["height"]), "actual screenshot viewport")
        expected_cells = {(consumer, scale) for consumer in ("statusCell", "compactStatus") for scale in scales}
        states = set(report["state_inventory"])
        expect({"idle","running","paused","succeeded","failed"}.issubset(states), "source inventory covers the fixed queue state contract")
        expect({(v["consumer"],v["state"],v["scale"]) for v in report["views"]} == {(c,s,k) for c,k in expected_cells for s in states}, "all state/consumer/scale still views")
        for cell in report["views"]:
            cell_pixels(cell, "view " + cell["consumer"] + "/" + cell["state"] + "/" + str(cell["scale"]))

        phases = report["phases"]
        expect([p["name"] for p in phases] == list(PHASES), "all fixed phases in required order")
        if len(phases) == 4:
            expect(phases[0]["sessionId"] == phases[1]["sessionId"] == phases[2]["sessionId"] != phases[3]["sessionId"], "same-page switches and separate startup page")
        for phase in phases:
            name, samples = phase["name"], phase["samples"]
            reduced = name in ("reduced", "initially-reduced")
            expect(phase["motion"] == ("reduced" if reduced else "normal"), name + " required preference")
            if name == "initially-reduced":
                expect(phase["initialMotion"] == "reduced" and not phase["preferenceEvents"], "initially reduced before page startup")
            elif name == "normal-start":
                expect(phase["initialMotion"] == "normal" and not phase["preferenceEvents"], "initially normal before page startup")
            if name in ("reduced", "normal-restored"):
                expected_switches = [("normal","reduced")] + ([("reduced","normal")] if name == "normal-restored" else [])
                expect([(e["from"],e["to"]) for e in phase["preferenceEvents"]] == expected_switches, name + " real media preference switches")
                expect(len(phase["reconciliations"]) == len(expected_switches), name + " source descriptor reconciliations")
                for r in phase["reconciliations"]:
                    expect(r["sessionId"] == phase["sessionId"], name + " reconciliation same page")
                    expect({(c["consumer"],c["scale"]) for c in r["repainted"] if c["live"]} == expected_cells, name + " reconciliation covers live consumers")
                    for c in r["repainted"]:
                        expect(c["descriptor"]["motion"] == r["to"], name + " reconciled descriptor preference")
                        if r["to"] == "reduced":
                            expect(c["descriptor"]["animate"] is False and c["frame"] == c["descriptor"]["holdFrame"], name + " source held-frame reconciliation")
            expect([t["event"] for t in phase["transitions"]] == ["idle","started","pause","ok","error"], name + " actual state event path")
            expect({t["state"] for t in phase["transitions"]} == {"idle","running","paused","succeeded","failed"}, name + " actual event path covers required queue states")
            expect(phase["frameMs"] == report["display"]["frameMs"] > 0, name + " source frame duration")
            expect(phase["endedAt"] - phase["startedAt"] <= config["phase_timeout_ms"] + 500, name + " bounded phase duration")
            expect(type(phase["rafCount"]) is int and phase["rafCount"] >= len(samples), name + " observed rAF callback count")
            by_cell = {key: [] for key in expected_cells}
            previous_at = previous_elapsed = -math.inf
            for sample in samples:
                expect(sample["at"] > previous_at and sample["elapsed"] > previous_elapsed, name + " capture clock strictly increases")
                expect({(c["consumer"], c["scale"]) for c in sample["cells"]} == expected_cells and len(sample["cells"]) == len(expected_cells), name + " every live consumer/scale sampled")
                for cell in sample["cells"]:
                    key=(cell["consumer"],cell["scale"])
                    if key not in by_cell:
                        continue
                    by_cell[key].append(cell)
                    d=cell["descriptor"]
                    expect(d["motion"] == phase["motion"] and d["frames"] == phase["frameCount"], name + " live source descriptor")
                    expect(0 <= cell["paintElapsed"] <= sample["elapsed"] + 1 and cell["paintAt"] <= sample["at"] + 1, name + " paint clock precedes capture clock")
                    if not reduced:
                        expect(abs((cell["paintAt"]-cell["paintElapsed"])-(sample["at"]-sample["elapsed"])) <= 1, name + " separate paint and capture clocks share origin")
                    expected_frame=d["holdFrame"] if reduced else int(max(cell["paintElapsed"],0)//phase["frameMs"]) % d["frames"]
                    expect(cell["frame"] == cell["expectedFrame"] == expected_frame, name + " painted frame uses paint clock/source contract")
                    expect(d["animate"] is (not reduced), name + " source animate decision")
                    facts["clock_checks"] += 1
                    cell_pixels(cell, name + " " + key[0] + "/" + str(key[1]))
                previous_at,previous_elapsed=sample["at"],sample["elapsed"]
            phase_counts={}
            for (consumer,scale), rows in by_cell.items():
                count=count_frames([c["frame"] for c in rows],phase["frameCount"])
                key=consumer+'@'+str(scale);phase_counts[key]=count
                expect(count == phase["counts"].get(key), name + " independently counted transitions/wraps " + key)
                if reduced:
                    expect(bool(rows) and count["transitions"] == 0 and count["wraps"] == 0, name + " source-held frame remains still " + key)
                else:
                    expect(count["skips"] == 0 and len(count["frames"]) == phase["frameCount"] and count["wraps"] >= config["observed_wraps"], name + " actual consecutive coverage and requested wraps " + key)
            if reduced:
                expect(len(samples) >= 2 and samples[-1]["at"] - samples[0]["at"] >= config["hold_ms"], name + " actually observed hold window")
            facts["phases"][name]={"status":phase["status"],"sample_count":len(samples),"raf_count":phase["rafCount"],"counts":phase_counts,"switches":len(phase["preferenceEvents"]),"reconciliations":len(phase["reconciliations"])}
            if phase["status"] != "observed":
                limitations.append(name + ": " + phase.get("reason", "incomplete phase"))
            expect(not phase["errors"], name + " no browser phase errors")
        unavailable = unavailable_inputs or execution["status"] != "complete" or any(p["status"] != "observed" for p in phases) or len(phases) != 4
        if unavailable:
            limitations.append("Execution incomplete; partial evidence does not establish consumer qualification")
    except (KeyError, TypeError, ValueError, OSError, IndexError, ZeroDivisionError) as error:
        failures.append("Malformed or unavailable retained input: " + str(error))
        unavailable = False
    status = "fail" if failures else "unavailable" if unavailable else "pass"
    return {"version":1,"status":status,"pass":status == "pass","capture_sha256":digest(report_path),"facts":facts,"failures":failures,"limitations":list(dict.fromkeys(limitations)) + ["PNG/source/clock observations are not artistic judgment or target-engine acceptance."]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project",type=Path,required=True)
    parser.add_argument("--capture",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    result=check(args.project,args.capture)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(result,stream,indent=2,allow_nan=False);stream.write("\n")
    print(json.dumps({"status":result["status"],"path":str(args.out),"pass":result["pass"]}))
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
