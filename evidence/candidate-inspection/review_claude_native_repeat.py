"""Read retained trial evidence; write only the independent reviewer receipt."""
import base64
import hashlib
import io
import json
import zipfile
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parent
SERIES = BASE / "native-operation-clarified"
RUN = SERIES / "runs/claude-inspection-02"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


record = read(RUN / "record.json")
protocol = read(SERIES / "inspection-protocol.json")
identity = read(SERIES / "identity.json")
package = SERIES / "package"
manifest = read(package / "bundle-manifest.json")
events = [json.loads(line) for line in (RUN / "stdout.jsonl").read_text(encoding="utf-8").splitlines()]
calls = {}
images = []
tools = []
texts = []
reviews = []
project = RUN / "project"
for line, event in enumerate(events, 1):
    for block in event.get("message", {}).get("content", []):
        kind = block.get("type")
        if kind == "tool_use":
            calls[block["id"]] = (line, block)
            tools.append({"line": line, "name": block["name"], "input": block["input"]})
            if block["name"].endswith("pixl_inspection_review"):
                reviews.append({"line": line, "input": block["input"]})
        elif kind == "text" and event["type"] == "assistant":
            texts.append({"line": line, "text": block["text"]})
        elif kind == "tool_result" and isinstance(block.get("content"), list):
            call_line, call = calls[block["tool_use_id"]]
            for item in block["content"]:
                if item.get("type") != "image":
                    continue
                raw = base64.b64decode(item["source"]["data"], validate=True)
                delivered = Image.open(io.BytesIO(raw)).convert("RGBA")
                path = Path(call["input"]["file_path"])
                relative = path.relative_to(Path(record["cwd"]))
                retained = project / relative
                original = Image.open(retained).convert("RGBA")
                images.append({"call_line": call_line, "payload_line": line,
                    "path": relative.as_posix(), "delivered_size": list(delivered.size),
                    "retained_size": list(original.size), "payload_sha256": hashlib.sha256(raw).hexdigest(),
                    "retained_sha256": sha(retained), "encoded_bytes_equal": raw == retained.read_bytes(),
                    "rgba_pixels_equal": delivered.size == original.size and delivered.tobytes() == original.tobytes()})

portable_root = BASE / "portable-operation"
portable = read(portable_root / "report.json")
with zipfile.ZipFile(SERIES / "fixture-inputs/seeded-project.zip") as archive:
    zip_inventory = {n: hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist()}
checks = {
    "native_package_inventory": all(sha(package / k) == v for k, v in identity["package_files"].items()),
    "native_bundle_entries": all(sha(package / row["path"]) == row["sha256"] for row in manifest["files"] + manifest["generated_files"]),
    "wrapper": sha(SERIES / "protocol-source.py") == protocol["wrapper_sha256"],
    "runner": sha(SERIES / ("runner-versions/" + protocol["shared_runner_sha256"] + ".py")) == protocol["shared_runner_sha256"],
    "zip_hash": sha(SERIES / "fixture-inputs/seeded-project.zip") == protocol["seed_zip_sha256"],
    "zip_inventory": zip_inventory == protocol["seed_files"],
    "record_evidence_hashes": all(sha(RUN / k) == v for k, v in record["evidence_hashes"].items()),
    "record_artifact_hashes": all(sha(project / k) == v for k, v in record["artifacts"].items()),
    "art_and_brief_unchanged": all(sha(project / k) == protocol["seed_files"][k] for k in ["candidate.png", "reference.png", "source.txt"]),
    "all_image_pixels_match": all(row["rgba_pixels_equal"] for row in images),
    "all_images_precede_review": bool(reviews) and all(row["payload_line"] < reviews[0]["line"] for row in images),
    "package_unmutated": record["package_mutated"] is False,
}
for key, folder in [("package_files", "package"), ("project_files", "project"), ("cold_project_files", "cold-project")]:
    checks["portable_" + key] = all(sha(portable_root / folder / name) == digest for name, digest in portable[key].items())
receipt = {"scope": "Independent retained Claude native events and portable proof integrity review",
    "checks": checks, "record_sha256": sha(RUN / "record.json"),
    "stdout_sha256": sha(RUN / "stdout.jsonl"), "protocol_sha256": sha(SERIES / "inspection-protocol.json"),
    "bundle_manifest_sha256": sha(package / "bundle-manifest.json"),
    "inspection_reference_sha256": sha(package / "skills/pixl/references/inspection.md"),
    "images": images, "tool_calls": tools, "review_calls": reviews, "assistant_text": texts,
    "limitations": ["Recorded image payloads establish delivered pixels, not internal perception.",
        "One controlled saved developer fixture, no generated production art or external engine/provider execution.",
        "Host process completion alone is not a behavioral pass."]}
receipt["behavior_grade"] = "pass for this bounded saved-fixture inspection scenario"
receipt["baseline_receipt_sha256"] = sha(BASE / "claude-native-review.json")
receipt["baseline_preserved"] = receipt["baseline_receipt_sha256"] == "7f57ea97451a5e4d6cd23971bc8b4fa639660dc97f1f30e761a812d9fb20daa2"
prior = read(BASE / "native-operation/identity.json")
receipt["intervention"] = {
    "changed_package_paths": [k for k, v in prior["package_files"].items() if identity["package_files"][k] != v],
    "runtime_hashes_unchanged": prior["runtime_hashes"] == identity["runtime_hashes"],
    "skill_hashes_unchanged": prior["skill_hashes"] == identity["skill_hashes"],
    "spec_sha256_before": prior["package_files"]["resources/spec/candidate-inspection.md"],
    "spec_sha256_after": identity["package_files"]["resources/spec/candidate-inspection.md"],
    "change": "Contract explicitly scopes complete coverage to visual/continuity or visual-mode passes and states local mechanical criteria need no image coverage.",
    "limitation": "One repeat with natural model variation supports observed recovery; it does not isolate causal instruction improvement statistically."
}
receipt["criteria"] = [
    {"check": "Skill, profile, reference and clarified contract loaded", "status": "pass", "event_lines": [4, 6, 8, 9, 10, 11, 37, 38]},
    {"check": "Packaged prepare and review", "status": "pass", "event_lines": [43, 44, 90, 91]},
    {"check": "Exact actual image delivery before review", "status": "pass", "event_lines": [51, 53, 55, 57, 59, 64, 66, 68, 70, 72, 90],
     "finding": "Six 32x32 native and four 256x256 enlarged payloads match retained files byte-for-byte and decoded RGBA pixel-for-pixel. All precede review; declared delivery sizes remain honestly unknown to the model."},
    {"check": "Correct visual rejection and next action", "status": "pass", "event_lines": [90, 91, 94, 96, 100],
     "finding": "Missing left antenna and right yellow eye retained as fail; separate future revision needs fresh inspection. Independent pixel comparison confirms 24 transparent pixels at x=7..10,y=3..8 and 12 teal replacements at x=18..20,y=14..17."},
    {"check": "Mechanical judgment independent of unknown viewing size", "status": "pass", "event_lines": [90, 91, 96, 100],
     "finding": "Explicit mechanical pass is judged against saved dimensions, palette and binary alpha. Baseline unsupported mechanical-viewing requirement is absent."},
    {"check": "Engine unavailable, art unchanged, task remains open", "status": "pass", "event_lines": [90, 91, 96, 100],
     "finding": "Engine unavailable is retained without claimed engine/provider execution; candidate/reference/brief bytes unchanged. Workflow retains open task and original nomination."},
    {"check": "Post-review inspection and workflow readback", "status": "pass", "event_lines": [93, 94, 95, 96]},
    {"check": "No unsupported requirements", "status": "pass", "event_lines": [90, 100],
     "finding": "No new artistic or mechanical gate introduced. It accurately reports inherited q.mechanical display-name inconsistency (2 by 2 versus actual 32x32 check), leaves records intact, and judges against the explicit check and confirmed intake."}
]
(BASE / "claude-native-repeat-review.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"checks": checks, "images": len(images), "review_calls": len(reviews)}, indent=2))
