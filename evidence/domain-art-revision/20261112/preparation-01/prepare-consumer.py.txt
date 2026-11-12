"""Prepare CF-09's real-art inputs and destination without creating animation art.

The old four-direction handoff is immutable provenance. The repeated-East clip is
a static comparison adapter, not a failed animation or a new provider result.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

from evaluations.host_trials import inventory, sha, write_json
from evaluations.request_review_trials import ROOT

ARCHIVE = ROOT / "evidence/native-production/20261112/claude-01-resume-02/consumer-delta.zip"
ARCHIVE_SHA256 = "c8a763a8ec952bc9d447ff5b40212207264be4cd9290d455764c90c3f5f34f1d"
PROJECT = ROOT / "examples/delegation"
ASSIGNMENT = ROOT / "evidence/domain-art-revision/CF-09-ROBOT-IDLE.md"
RENDERER = ROOT / "examples/consumer-execution/sprite-animation"
RENDERER_FILES = ("capture.mjs", "server.mjs", "view.mjs", "index.html", "check.py", "observation.py")
SOURCE_HASHES = {
    "BRIEF.md": "e1202361a26c377aff4ace08166854beff4f2978b08f1f961ef8b775269aa0e1",
    "src/robot.ts": "d57b9a903dc4210944ad1d7ea83c83718cffd22b9b044932852ed6f1ba80c1d0",
    "assets/robot-base.png": "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7",
}
ASSET_HASHES = {
    "assets/robot/east.png": "71b35089965b6457f505d569f4fc89fbcc2521bf188aa43f836dc207c3771fb4",
    "assets/robot/north.png": "db516f78a836f89b618ba00cfac0d2373f260ae3923b6198f17c62ab957ba3f5",
    "assets/robot/south.png": "d997cadefc6b94c1c14f4ec17159deaf5ceb7ea9543b2522390ea1a577470aa7",
    "assets/robot/west.png": "ec96bf6379daf161ce8643894b72c50b4bb543e105f336cbc58f27293df655a0",
}
DURATIONS = (800, 120, 160, 120, 400)


def checked(data: bytes, expected: str, name: str) -> bytes:
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f"Retained source identity changed: {name}")
    return data


def configuration(*, baseline: bool) -> dict:
    return {
        "version": 1,
        "profile": "sprite-animation-v1",
        "modules": {"animation": "src/animation-baseline.ts" if baseline else "src/animation.ts"},
        "destinations": ({"robot.east.retained.output": "assets/robot/east.png"} if baseline else {
            f"robot.idle.frame{i}.output": f"assets/robot-idle/east-{i}.png" for i in range(5)
        }),
        "scales": [1, 3],
        "observed_wraps": 2,
        "phase_timeout_ms": 10000,
        "timeout_seconds": 90,
    }


def animation_module(*, baseline: bool) -> str:
    animation = {
        "viewport": [48, 40], "background": "#172336", "sampling": "nearest",
        "clips": [{
            "id": "east-idle",
            "label": "Static East comparison baseline" if baseline else "Planted panel idle",
            "loop": True, "anchor": [24, 34],
            "frames": [{
                "id": f"east-{i}",
                "path": "assets/robot/east.png" if baseline else f"assets/robot-idle/east-{i}.png",
                "rect": [0, 0, 32, 32], "duration_ms": duration, "pivot": [16, 28],
            } for i, duration in enumerate(DURATIONS)],
        }],
    }
    scope = ("Static comparison adapter: all five entries reuse the exact accepted East.\n"
             "// This is not a historical animation failure or newly generated animation."
             if baseline else
             "Prospective consumer contract: the five animation files do not exist yet.\n"
             "// Actual production and review must supply them; no placeholders are accepted.")
    return "// " + scope + "\nexport const animation = " + json.dumps(animation, indent=2) + """;

export function frameAt(clipId, elapsedMs) {
  const clip = animation.clips.find(value => value.id === clipId);
  if (!clip) throw new Error('Unknown clip');
  const duration = clip.frames.reduce((sum, frame) => sum + frame.duration_ms, 0);
  let at = clip.loop ? Math.max(elapsedMs, 0) % duration
                    : Math.min(Math.max(elapsedMs, 0), duration);
  for (let index = 0; index < clip.frames.length; index++) {
    if (at < clip.frames[index].duration_ms) return index;
    at -= clip.frames[index].duration_ms;
  }
  return clip.frames.length - 1;
}
"""


def prepare(destination: Path, *, archive: Path = ARCHIVE, project: Path = PROJECT,
            assignment: Path = ASSIGNMENT) -> Path:
    """Create a fresh attempt with a self-contained consumer and exact input ZIP.

    All supplied provenance is checked before writing. This neither reconstructs
    the old production store nor creates new candidates, jobs, verdicts or art.
    """
    destination = destination.absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError("Use a fresh CF-09 preparation directory; preserve prior attempts")
    archive_bytes = checked(archive.read_bytes(), ARCHIVE_SHA256, str(archive))
    payload = {name: checked((project / name).read_bytes(), digest, name)
               for name, digest in SOURCE_HASHES.items()}
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as retained:
        for name, digest in ASSET_HASHES.items():
            if retained.namelist().count(name) != 1:
                raise ValueError(f"Expected exactly one retained asset: {name}")
            payload[name] = checked(retained.read(name), digest, name)
    assignment_bytes = assignment.read_bytes()
    if not assignment_bytes.strip():
        raise ValueError("The explicit CF-09 assignment must not be empty")
    payload["CF-09-ROBOT-IDLE.md"] = assignment_bytes
    for name in RENDERER_FILES:
        payload[f"renderer/{name}"] = (RENDERER / name).read_bytes()
    payload["src/animation-baseline.ts"] = animation_module(baseline=True).encode("utf-8")
    payload["src/animation.ts"] = animation_module(baseline=False).encode("utf-8")
    for name, baseline in (("baseline-config.json", True), ("config.json", False)):
        payload[name] = (json.dumps(configuration(baseline=baseline), indent=2) + "\n").encode("utf-8")

    destination.mkdir(parents=True, exist_ok=False)
    root = destination / "consumer"
    for name, data in payload.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    inputs = inventory(root)
    input_zip = destination / "consumer-inputs.zip"
    with zipfile.ZipFile(input_zip, "w", compression=zipfile.ZIP_DEFLATED) as retained:
        for name in sorted(payload):
            retained.writestr(name, payload[name])
    provenance = {
        "scope": "CF-09 local preparation from actual retained art; no new animation output",
        "historical_archive": {"path": archive.resolve().as_posix(), "sha256": ARCHIVE_SHA256},
        "historical_provider": {
            "object_id": "2a3cb51a-6cf7-485d-8441-3c3db762cc9d",
            "job_id": "ea834364-0f7d-42eb-876b-bb26e21e1269",
            "new_provider_execution": False,
        },
        "original_sources": SOURCE_HASHES,
        "preserved_directions": [{
            "path": name, "sha256": digest,
            "origin": ("PixelLab-generated" if name.endswith(("east.png", "north.png")) else
                       "Retained evaluation fixture; not generated" if name.endswith("south.png") else
                       "Locally mirrored and edited East; not a direct provider result"),
        } for name, digest in ASSET_HASHES.items()],
        "assignment": {"path": "CF-09-ROBOT-IDLE.md", "sha256": inputs["CF-09-ROBOT-IDLE.md"]},
        "baseline": {
            "config": "baseline-config.json", "module": "src/animation-baseline.ts",
            "kind": "Static-baseline adapter for the new requirement; no original art defect claimed",
            "asset": "assets/robot/east.png", "sha256": ASSET_HASHES["assets/robot/east.png"],
        },
        "planned_animation": {
            "config": "config.json", "module": "src/animation.ts",
            "output_ids": "Provisional names; bind actual public plan output IDs before consumer-execute",
            "missing_files": list(configuration(baseline=False)["destinations"].values()),
            "durations_ms": list(DURATIONS), "viewport": [48, 40], "anchor": [24, 34],
            "pivot": [16, 28], "source_size": [32, 32], "scales": [1, 3],
            "scope": "Project-specific proposed animation contract, not universal pixel-art rules",
        },
        "consumer_inputs": inputs,
        "input_archive": {"path": input_zip.name, "sha256": sha(input_zip), "files": len(inputs)},
        "provider_calls": 0, "paid_calls": 0, "new_art_files": [],
        "production_state_created": False, "artistic_acceptance": False,
        "human_acceptance": False, "cf09_complete": False,
    }
    write_json(destination / "preparation.json", provenance)
    return root


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="Fresh attempt directory; consumer/ and input archive are created inside")
    args = parser.parse_args()
    print(prepare(args.destination).as_posix())


if __name__ == "__main__":
    main()
