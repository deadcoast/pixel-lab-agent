"""Independent read-only checks for the retained focused-authoring native attempts."""
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pixl import codec, store


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def review(host):
    attempt = ROOT / "evidence/focused-authoring/20261109/native" / (host + "-01")
    project, before = attempt / "project", attempt / "input-project"
    state = ".pixl/assets/queue.ready/state.px"
    original, current = store.load((before / state).parent), store.load((project / state).parent)
    changes = []
    for ident, record in original.records.items():
        after = current.records.get(ident)
        if after != record:
            changes.append({"id": ident, "kind": record.kind, "fields": [k for k in record.fields if after is None or record.fields[k] != after.fields.get(k)]})
    preserved = []
    for path in before.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(before)
        if rel.parts[0] in ("assets", "src", "renderer", "work") or rel.as_posix() in ("plar.txt", "BRIEF.md", "RENDER-STAGE.md"):
            if not (project / rel).is_file() or digest(path) != digest(project / rel):
                preserved.append(rel.as_posix())
    context_name = "context-authoring-raw.json" if host == "claude" else "context.raw.json"
    focused = load(project / "work/focused-successor" / context_name)
    wrapper_agrees = None
    if "structuredContent" in focused:
        wrapper_agrees = json.loads(focused["content"][0]["text"]) == focused["structuredContent"]
        focused = focused["structuredContent"]
    criteria = {r["id"]: r for r in focused["criteria"]}
    exact = all(r["record_sha256"] == codec.record_hash(original.records[ident]) and r["fields"] == codec.to_data(original.records[ident].fields) for ident, r in criteria.items())
    result = {
        "host": host, "state_before": codec.digest(original), "state_after": codec.digest(current),
        "focused_criteria": len(criteria), "focused_exact_criteria": exact,
        "focused_state_identity": focused["hash"] == codec.digest(original),
        "context_wrapper_agrees": wrapper_agrees,
        "changed_historical_records": changes, "changed_original_files": preserved,
        "old_job_state": current.records["authoring-01.working.join-01"].fields["si"].value,
        "old_job_remote_id": current.records["authoring-01.working.join-01"].fields["ri"],
        "new_records": len(set(current.records) - set(original.records)),
        "render_checks": [], "limitations": ["Checks identities and rendered pixels; semantic review and native role selection require independent reading."],
    }
    for directory in sorted((project / "work/focused-successor").glob("render-*")):
        motion_path = directory / "motion.json"
        if not motion_path.is_file():
            continue
        motion = load(motion_path)
        failures, phases = [], []
        for phase in motion["phases"]:
            frames = set()
            for index, sample in enumerate(phase["samples"]):
                for cell in sample["cells"]:
                    png = directory / cell["image"]["path"]
                    im = Image.open(png).convert("RGBA")
                    source = Image.open(project / cell["path"]).convert("RGBA")
                    frame = cell["frame"]
                    frames.add(frame)
                    crop = source.crop((frame * 16, 0, frame * 16 + 16, 16))
                    expected = Image.new("RGBA", (16, 16), "#172336")
                    expected.alpha_composite(crop)
                    expected = expected.resize(im.size, Image.Resampling.NEAREST)
                    checks = {
                        "hash": digest(png) == cell["image"]["sha256"],
                        "pixels": all(high == 0 for low, high in ImageChops.difference(im, expected).getextrema()),
                        "mode": sample["reduced"] == phase["reduced"],
                        "reduced_frame": not phase["reduced"] or frame == 0,
                        "geometry": im.size == (48, 48), "filter": cell["smoothing"] is False,
                    }
                    if not all(checks.values()):
                        failures.append({"phase": phase["name"], "sample": index, "consumer": cell["consumer"], "checks": checks})
            if frames != ({0} if phase["reduced"] else {0, 1, 2, 3}):
                failures.append({"phase": phase["name"], "reason": "observed frames do not cover the required motion mode", "frames": sorted(frames)})
            phases.append({"name": phase["name"], "reduced": phase["reduced"], "samples": len(phase["samples"]), "frames": sorted(frames), "elapsed_ms": phase["samples"][-1]["at"] - phase["samples"][0]["at"]})
        result["render_checks"].append({"directory": directory.relative_to(project).as_posix(), "phases": phases, "failures": failures})
    out = ROOT / "evidence/focused-authoring/20261109/independent-review"
    out.mkdir(parents=True, exist_ok=True)
    (out / (host + "-checks.json")).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "render_checks"}, indent=2))
    print("render summaries", [(r["directory"], len(r["failures"]), r["phases"]) for r in result["render_checks"]])


if __name__ == "__main__":
    review(sys.argv[1])
