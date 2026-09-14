"""Inspect retained Codex image deliveries; grade rows are explicit evaluator review."""

import base64
import hashlib
import io
import json
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from evaluations.host_trials import inventory, sha, verify_run


def pixels(raw):
    with Image.open(io.BytesIO(raw)) as image:
        return list(image.size), hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def run():
    base = Path(__file__).resolve().parent
    trial = base / "native-operation/runs/codex-inspection-01"
    project = trial / "project"
    record = json.loads((trial / "record.json").read_text(encoding="utf-8"))
    assert not verify_run(trial)
    assert inventory(project) == record["artifacts"]
    assert not record["package_mutated"]
    packet_path = next(path for path in project.glob(".pixl/inspections/*/manifest.json")
                       if json.loads(path.read_bytes())["kind"] == "packet")
    packet = json.loads(packet_path.read_bytes())
    review_path = next(path for path in project.glob(".pixl/inspections/*/manifest.json")
                       if json.loads(path.read_bytes())["kind"] == "review")
    review = json.loads(review_path.read_bytes())
    expected = {view["id"]: {"view": view, "pixels": pixels((packet_path.parent / view["path"]).read_bytes())}
                for view in packet["rendering"]["views"]}
    journal = trial / "native-session-0.jsonl"
    images, calls, final = [], [], None
    review_line = None
    for line, raw in enumerate(journal.read_text(encoding="utf-8").splitlines(), 1):
        event = json.loads(raw)
        if event.get("type") != "response_item":
            continue
        item = event["payload"]
        if item.get("type") == "custom_tool_call":
            code = item.get("input", "")
            calls.append({"line": line, "input": code})
            if "tools.mcp__pixl_local__pixl_inspection_review(" in code:
                review_line = line
        if item.get("type") == "message" and item.get("role") == "assistant":
            final = {"line": line, "text": "\n".join(block.get("text", "") for block in item["content"])}
        if item.get("type") != "custom_tool_call_output" or not isinstance(item.get("output"), list):
            continue
        label = None
        for block in item["output"]:
            if block.get("type") == "input_text":
                try:
                    value = json.loads(block["text"])
                    if isinstance(value, dict) and "view" in value:
                        label = value["view"]
                except ValueError:
                    pass
            if block.get("type") != "input_image":
                continue
            raw_image = base64.b64decode(block["image_url"].split(",", 1)[1], validate=True)
            actual = pixels(raw_image)
            assert label in expected and actual == expected[label]["pixels"]
            view = expected[label]["view"]
            images.append({"line": line, "view": label, "source": view["source"],
                           "scale": view["scale"], "delivered_size": actual[0],
                           "rgba_sha256": actual[1], "retained_pixel_match": True})
    assert {row["view"] for row in images} == set(expected)
    assert review_line and all(row["line"] < review_line for row in images)
    verdicts = {v["criterion"]: v["status"] for v in review["observation"]["verdicts"]}
    assert verdicts == {"q.mechanical": "pass", "q.visual": "fail", "q.engine": "unavailable"}
    assert review["coverage"]["complete"]
    assert all(obs["delivered_size"] == expected[obs["view"]]["pixels"][0]
               for obs in review["observation"]["observations"])
    result = {
        "purpose": "Explicit evaluator review with deterministic image identity checks; no statistical or production claim.",
        "attempt": trial.name, "execution_status": record["execution_status"],
        "bundle_manifest_sha256": record["bundle_manifest_sha256"],
        "bindings": {"record.json": sha(trial / "record.json"), journal.name: sha(journal),
                     "stdout.jsonl": sha(trial / "stdout.jsonl"),
                     "packet": sha(packet_path), "review": sha(review_path)},
        "analysis_source_sha256": sha(Path(__file__)), "images": images,
        "review_call_line": review_line, "retained_verdicts": verdicts,
        "declaration_matches_delivered_sizes": True, "final": final,
        "criteria": [
            {"check": "Load actual profile, shared inspection reference and implemented contract", "status": "pass", "lines": [13, 19, 29]},
            {"check": "Use packaged prepare/review instead of a project-specific evidence publisher", "status": "pass", "lines": [50, 77]},
            {"check": "Inspect exact retained native and enlarged pixels before review", "status": "pass", "lines": [55, 67, 77], "detail": "10 matching deliveries: six 32x32 native and four 256x256 enlarged views."},
            {"check": "Reject missing image-left antenna and image-right yellow eye, separate mechanical and engine results", "status": "pass", "lines": [72, 77, 91]},
            {"check": "Retain open task, original art and next action with cold readback", "status": "pass", "lines": [82, 91]},
        ],
        "limitations": [
            "One controlled saved-project attempt, not commissioned production art or a reliability estimate.",
            "MCP retains reviewer declarations; native journal independently establishes delivered image inputs.",
            "Model-requested and host-selected identities are recorded; no independent inference-model attestation.",
        ],
    }
    output = base / "codex-native-review.json"
    with output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"images": len(images), "verdicts": verdicts, "review": str(output)}))


if __name__ == "__main__":
    run()
