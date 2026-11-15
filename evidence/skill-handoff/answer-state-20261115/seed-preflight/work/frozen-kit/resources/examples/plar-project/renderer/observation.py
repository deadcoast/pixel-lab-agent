"""Bridge a retained queue browser capture to the public destination report schema.

This reads observations and checks bytes. It never runs a browser, awards a verdict,
or infers missing destination mappings. The runtime importer validates the resulting
report against the current delivery candidate and retains its complete inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(project: Path, capture: Path, context: Path, renderer: Path,
          destinations: Path) -> dict:
    project = project.resolve()

    def confined(path: Path) -> Path:
        actual = path.resolve()
        if not actual.is_relative_to(project) or actual == project:
            raise ValueError("Observation input is outside the consumer root: " + str(path))
        return actual

    capture, renderer, context, destinations = map(confined, (capture, renderer, context, destinations))

    def ref(path: Path, expected: str | None = None) -> dict:
        path = confined(path)
        actual = digest(path)
        if expected is not None and actual != expected:
            raise ValueError("Captured bytes changed: " + str(path))
        return {"path": path.relative_to(project).as_posix(), "sha256": actual}

    observed = json.loads((capture / "render.json").read_bytes())
    launch = json.loads((capture / "launch.json").read_bytes())
    review = json.loads(context.read_bytes())
    mapping = json.loads(destinations.read_bytes())
    if not isinstance(mapping, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in mapping.items()):
        raise ValueError("Destination map must be an object from member output ID to served relative path")
    if Path(launch["project"]).resolve() != project:
        raise ValueError("Capture was produced for a different project")
    manifest_ref = ref(project / review["candidate_file"]["path"], review["candidate_file"]["sha256"])
    manifest = json.loads((project / manifest_ref["path"]).read_bytes())
    # Review context adds presentation fields; every immutable manifest field
    # (and any unrecognized extra) must still participate in the exact comparison.
    if manifest["candidate"] != review["candidate"] or manifest["files"] != [
        {k: v for k, v in row.items() if k not in {"retained_path", "lineage"}} for row in review["members"]
    ]:
        raise ValueError("Review context and exact candidate manifest disagree")
    members = {row["output"]: row for row in manifest["files"]}
    if set(mapping) != set(members):
        raise ValueError("Explicit destination map must cover exactly every package member")
    served = observed["served_files"]
    destination_rows = []
    for output, path in mapping.items():
        member = members[output]
        if served.get("consumer/" + path) != member["sha256"]:
            raise ValueError("Package member was not served at its explicit destination: " + output)
        destination_rows.append({"output": output, "candidate": member["candidate"], **ref(project / path, member["sha256"])})
    renderer_refs = [ref(renderer / name, expected) for name, expected in sorted(observed["renderer_files"].items())]
    for key, expected in served.items():
        if key.startswith("renderer/"):
            ref(renderer / key.removeprefix("renderer/"), expected)
    consumer_refs = [ref(project / key.removeprefix("consumer/"), expected)
                     for key, expected in sorted(served.items()) if key.startswith("consumer/")]
    if not consumer_refs:
        raise ValueError("No actual served consumer sources were recorded")
    files, file_ids = [], {}

    def add_file(path: Path, role: str, expected: str | None = None) -> str:
        item = ref(path, expected)
        if item["path"] in file_ids:
            return file_ids[item["path"]]
        ident = "capture." + str(len(files))
        files.append({"id": ident, **item, "role": role})
        file_ids[item["path"]] = ident
        return ident

    def image(item: dict) -> str:
        value = item["image"]
        path = confined(capture / value["path"])
        if not path.is_relative_to(capture):
            raise ValueError("Captured image escaped its capture directory")
        return add_file(path, "image", value["sha256"])

    views = []
    limitations = ["Bridge reads a supplied retained browser capture; it does not execute a renderer or grant review/acceptance.",
                   "View and motion observations describe this capture only; artistic judgment requires separate actual image inspection."]
    for view in observed["views"]:
        if "image" not in view:
            limitations.append(f"No captured view image: {view['consumer']} / {view['state']} / {view['scale']}")
            continue
        path = view["descriptor"]["path"]
        outputs = [output for output, target in mapping.items() if target == path]
        for output in outputs:
            if view["asset"]["sha256"] != members[output]["sha256"]:
                raise ValueError("Captured view does not show the package member bytes")
        views.append({"consumer": view["consumer"], "state": view["state"], "scale": view["scale"],
                      "output_id": image(view), "member_outputs": outputs})
    motion = []
    playback = observed.get("playback")
    if playback:
        for consumer in playback["transition"]["consumers"]:
            samples = []
            if playback["status"] == "observed":
                for sample in playback["samples"]:
                    cell = next((cell for cell in sample["cells"] if cell["consumer"] == consumer["consumer"]), None)
                    if cell is None or "image" not in cell:
                        raise ValueError("Observed playback lacks a consumer image sample")
                    samples.append({"elapsed_ms": sample["elapsed"], "frame": cell.get("frame"), "output_id": image(cell)})
            motion.append({"consumer": consumer["consumer"], "state": playback["transition"]["state"],
                           "mode": "requestAnimationFrame playback", "status": playback["status"],
                           "frame_count": playback.get("frameCount"), "frame_ms": playback.get("frameMs"),
                           "samples": samples, "limitation": playback.get("reason") or "No additional playback explanation supplied."})
            if playback["status"] != "observed":
                limitations.append("Playback unavailable; any partial raw samples remain only in the retained original capture.")
    else:
        limitations.append("Capture supplies no live playback observation.")
    for state in sorted({row["state"] for row in observed.get("timeline", [])}):
        rows = [row for row in observed["timeline"] if row["state"] == state and "image" in row]
        motion.append({"consumer": "statusCell", "state": state, "mode": "controlled elapsed-time boundary samples",
                       "status": "observed" if rows else "unavailable", "frame_count": None,
                       "frame_ms": observed["display"].get("frameMs"),
                       "samples": [{"elapsed_ms": row["elapsed"], "frame": row.get("frame"), "output_id": image(row)} for row in rows],
                       "limitation": "Renderer's explicit elapsed-time samples; this is separate from live callback playback."})
    add_file(capture / observed["screenshot"]["path"], "image", observed["screenshot"]["sha256"])
    # Retain raw reports, protocol, browser logs and all contextual/partial images.
    for path in sorted(p for p in capture.rglob("*") if p.is_file()):
        add_file(path, "image" if path.suffix.lower() == ".png" else "data")
    add_file(context, "data")
    add_file(destinations, "data")
    viewport = observed["viewport"]
    return {"version": 1, "candidate": review["candidate"], "binding_hash": review["binding_hash"],
            "manifest": manifest_ref, "observed_at": observed["observed_at"],
            "renderer": {"name": "Retained queue browser renderer", "command": [launch["browser"], *launch["args"]],
                         "runtime": {"name": "browser", "version": observed["browser_version"]["product"]}, "files": renderer_refs},
            "consumer_sources": consumer_refs, "destinations": destination_rows,
            "viewport": {"width": viewport["width"], "height": viewport["height"], "device_scale_factor": observed["devicePixelRatio"]},
            "views": views, "motion": motion, "files": files, "limitations": limitations}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--capture", type=Path, required=True, help="Fresh capture directory containing render.json and launch.json")
    parser.add_argument("--context", type=Path, required=True, help="Saved exact public delivery review-context JSON")
    parser.add_argument("--renderer", type=Path, required=True)
    parser.add_argument("--destinations", type=Path, required=True, help="JSON object mapping every package member output ID to its served path")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    target = args.out.resolve()
    if target.exists() or not target.is_relative_to(args.project.resolve()):
        raise ValueError("Report needs a fresh consumer-relative output path")
    report = build(args.project, args.capture, args.context, args.renderer, args.destinations)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"path": target.relative_to(args.project.resolve()).as_posix(), "sha256": digest(target),
                      "renderer_executed": False, "acceptance_created": False}))


if __name__ == "__main__":
    main()
