"""Read retained trial evidence; write only the independent reviewer receipt."""
import base64
import hashlib
import io
import json
import zipfile
from pathlib import Path

from PIL import Image

BASE = Path(__file__).resolve().parent
SERIES = BASE / "native-operation"
RUN = SERIES / "runs/claude-inspection-01"


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
receipt["behavior_grade"] = "partial: retained rejection succeeds; unsupported mechanical-viewing requirement remains"
receipt["criteria"] = [
    {"check": "New skill and inspection reference loaded", "status": "pass", "event_lines": [4, 6, 10, 11],
     "finding": "Native Skill invocation and full reference Read are retained. No separate PROFILE.md Read appears in the complete tool sequence."},
    {"check": "Packaged prepare and review", "status": "pass_with_recovery", "event_lines": [28, 29, 30, 31, 84, 85],
     "finding": "Initial store argument was a state-file path; rejected before publication, then corrected to .pixl."},
    {"check": "Native and enlarged viewing precedes review", "status": "pass", "event_lines": [37, 39, 44, 46, 48, 50, 59, 61, 63, 65, 84],
     "finding": "All ten actual image payloads have identical retained RGBA pixels: six 32x32 native and four 384x384 enlarged. Review honestly declares unknown delivery sizes; reviewer can independently recover exact dimensions from native payloads."},
    {"check": "Correct identity rejection", "status": "pass", "event_lines": [84, 85, 88, 95],
     "finding": "Missing top-left antenna and right yellow eye correctly identified and retained as q.visual fail. Independent reviewer visually inspected candidate/reference enlarged images and agrees."},
    {"check": "Engine unavailable, no art mutation or automatic task completion", "status": "pass", "event_lines": [84, 85, 88, 90, 95],
     "finding": "q.engine unavailable; task open and original candidate nominated. Source art/brief hashes unchanged; no provider or engine execution claimed."},
    {"check": "No unsupported requirements", "status": "fail", "event_lines": [68, 84, 95],
     "finding": "Claude leaves q.mechanical unperformed because it says mechanical pass requires known delivered dimensions and full viewing coverage. Runtime only applies this requirement to visual/continuity or visual-mode criteria. Valid measurements could support a caller-declared mechanical pass without known delivery sizes.",
     "source": "Frozen resources/spec/candidate-inspection.md:134-139 has ambiguous 'Passes require every prepared view' following visual-failure wording; frozen runtime/pixl/inspection.py:515-526 and shared inspection reference explicitly scope coverage to visual criteria.",
     "recommendation": "Clarify contract scope and mechanical independence, preserve this trial, then evaluate revised instructions in a new frozen series."},
    {"check": "Post-review readback", "status": "partial", "event_lines": [87, 88, 89, 90],
     "finding": "Workflow and validate read back saved review; inspection readback requested by the skill was omitted."},
]
(BASE / "claude-native-review.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"checks": checks, "images": len(images), "review_calls": len(reviews)}, indent=2))
