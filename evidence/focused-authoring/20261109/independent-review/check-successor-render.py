"""Read-only pixel checks for the retained successor capture; run from repo root."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops

root = Path.cwd()
project = root / "evidence/focused-authoring/20261109/native/codex-successor-01/project"
capture = project / "work/successor-adoption/render-01"
motion = json.loads((capture / "motion.json").read_text(encoding="utf-8"))
result = {"capture": capture.relative_to(root).as_posix(), "cells_checked": 0, "phases": [], "failures": []}
for phase in motion["phases"]:
    frames, consumers = set(), set()
    for index, sample in enumerate(phase["samples"]):
        for cell in sample["cells"]:
            path = capture / cell["image"]["path"]
            actual = Image.open(path).convert("RGBA")
            sheet = Image.open(project / cell["path"]).convert("RGBA")
            frame = cell["frame"]
            expected = Image.new("RGBA", (16, 16), "#172336")
            expected.alpha_composite(sheet.crop((frame * 16, 0, frame * 16 + 16, 16)))
            expected = expected.resize(actual.size, Image.Resampling.NEAREST)
            checks = {
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest() == cell["image"]["sha256"],
                "pixels": all(high == 0 for _, high in ImageChops.difference(actual, expected).getextrema()),
                "mode": sample["reduced"] == phase["reduced"],
                "stationary_if_reduced": not phase["reduced"] or frame == 0,
                "geometry": actual.size == (48, 48),
                "nearest": cell["smoothing"] is False,
                "label": cell["label"] == "Working",
            }
            frames.add(frame)
            consumers.add(cell["consumer"])
            result["cells_checked"] += 1
            if not all(checks.values()):
                result["failures"].append({"phase": phase["name"], "sample": index, "consumer": cell["consumer"], "checks": checks})
    elapsed = phase["samples"][-1]["at"] - phase["samples"][0]["at"]
    correct_coverage = frames == ({0} if phase["reduced"] else {0, 1, 2, 3}) and len(consumers) == 2 and elapsed > 800
    result["phases"].append({"name": phase["name"], "samples": len(phase["samples"]), "frames": sorted(frames), "consumers": sorted(consumers), "elapsed_ms": elapsed, "coverage": correct_coverage})
    if not correct_coverage:
        result["failures"].append({"phase": phase["name"], "coverage": False})
result["passed"] = not result["failures"]
result["scope"] = "Exact retained browser pixels, frame selection and live mode switches; no fresh rendering, exact wall-clock cadence claim or aesthetic acceptance."
output = Path(__file__).with_name("successor-render-checks.json")
output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
assert result["passed"]
