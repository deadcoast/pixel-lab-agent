"""Read-only final-guidance compatibility and integrity; no packaging tests rerun."""

from __future__ import annotations

import hashlib
import json
import runpy
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASE = OUT.parent
KIT = ROOT / "plugins/pixl"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def reference(path):
    return {"path": str(path.resolve()), "sha256": digest(path.read_bytes()), "bytes": path.stat().st_size}


def write(name, value):
    with (OUT / name).open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def inventory():
    return {p.relative_to(KIT).as_posix(): digest(p.read_bytes()) for p in sorted(KIT.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}


def archived(revision):
    path = BASE / revision / "frozen-kit.zip"
    with zipfile.ZipFile(path) as archive:
        files = {name: digest(archive.read(name)) for name in archive.namelist()}
    declared = json.loads((BASE / revision / "RESULT.json").read_bytes())["package_files"]
    if files != declared:
        raise ValueError("Frozen archive does not match its original receipt")
    return {"archive": reference(path), "receipt": reference(BASE / revision / "RESULT.json"), "files": files}


if __name__ == "__main__":
    if (OUT / "before.json").exists():
        raise ValueError("Use a fresh evidence directory")
    sys.path.insert(0, str(ROOT))
    from pixl.readiness import verify_manifest

    before = inventory()
    write("before.json", before)
    tested = archived("revision-03")
    current_archive = archived("revision-05")
    write("archive-identities.json", {"previously_tested": tested, "current": current_archive})
    previous_check = json.loads((BASE / "package-check-01/RESULT.json").read_bytes())
    changes = [name for name in sorted(set(tested["files"]) | set(before)) if tested["files"].get(name) != before.get(name)]
    expected_changes = {"bundle-manifest.json", "skills/pixl/references/intake-sample.md"}
    groups = {}
    for group, prefix in (("runtime", "runtime/"), ("launchers", "scripts/"), ("resources", "resources/")):
        names = sorted(name for name in set(tested["files"]) | set(before) if name.startswith(prefix))
        groups[group] = {"files": len(names), "unchanged": all(tested["files"].get(name) == before.get(name) for name in names)}
    readiness = verify_manifest(KIT)
    write("readiness.json", readiness)
    prior_checker = BASE / "package-check-01/runner.py"
    route_checker = runpy.run_path(str(prior_checker))
    routes = route_checker["skills"]()
    write("skill-routes.json", routes)
    procedure = KIT / "skills/pixl/references/intake-sample.md"
    with (OUT / "intake-sample.md.txt").open("xb") as stream:
        stream.write(procedure.read_bytes())
    lines = procedure.read_text(encoding="utf-8").splitlines()
    start = lines.index("## Cold intake handoff") + 1
    scope = {
        "status": "pass", "kind": "read-only semantic scope review by the development collaborator",
        "source": reference(procedure), "section_start_line": start,
        "checks": [
            {"finding": "No fixture values or expected answer", "basis": "The numbered procedure specifies source authority, a decision table, prerequisites and response components; it prescribes no canvas size, color, alpha choice, outline, character roster or answer text."},
            {"finding": "No blanket human approval gate", "basis": "The procedure preserves existing authorization, continues independent work, and directs already-supplied choices to the next operation without asking again."},
            {"finding": "Authority is preserved through the answer", "basis": "Owner decisions remain distinct from observations, proposals and diagnostic measurements; the answer adopts only choices it explicitly supplies, with unasked rows retaining status."},
            {"finding": "Local preparation and provider dependencies are separated", "basis": "Step 3 checks the actual tools and keeps decision, provider-schema, execution and engine prerequisites explicit; useful contract/output planning may precede real request preparation."},
            {"finding": "Cold final follows checked project state", "basis": "The sequence saves a short decision table, checks operation prerequisites, then derives saved progress, a direct question and its exact next local operation from that note."},
        ],
        "limit": "This is instruction-scope review, not proof that a model follows it or human acceptance of the product.",
    }
    write("scope-review.json", scope)
    after = inventory()
    write("after.json", after)
    result = {
        "status": "pass" if before == after == current_archive["files"] and set(changes) == expected_changes
            and all(item["unchanged"] for item in groups.values()) and readiness["status"] == "verified"
            and routes["status"] == "pass" and previous_check["status"] == "pass" else "fail",
        "verification_tier": "Read-only compatibility, discovery routes and local integrity; no fresh packaging test execution",
        "packaging_tests_executed_now": 0,
        "previous_packaging_evidence": {**reference(BASE / "package-check-01/RESULT.json"), "actual_passed_tests": previous_check["packaging_tests"],
                                      "tested_manifest_sha256": tested["files"]["bundle-manifest.json"]},
        "operations": ["pixl.readiness.verify_manifest(current kit)", "package-check-01 runner.skills() read-only route checks",
                       "SHA256 comparison of all current kit bytes before/after and against two receipt-verified ZIP archives",
                       "Read-only semantic review of the numbered cold-handoff procedure"],
        "current_kit_files": len(before), "current_manifest_sha256": before["bundle-manifest.json"],
        "current_archive_matches": before == current_archive["files"], "kit_before_after_identical": before == after,
        "changed_since_tested_revision": changes, "unchanged_since_tested_revision": len(before) - len(changes),
        "compatibility_groups": groups, "readiness": readiness, "discovery_entrypoints": routes["skill_count"],
        "scope_review": "pass", "changed_guidance": reference(procedure),
        "sources": {"runner": reference(Path(__file__)), "reused_route_checker": reference(prior_checker),
                    "readiness_implementation": reference(ROOT / "pixl/readiness.py")},
        "side_effects": "Only files under package-check-02 were written; no builder, test suite, model, remote provider or generated kit write.",
        "limit": "Existing packaging test results are linked with exact unchanged runtime, launcher and resource hashes; they are not relabeled as new tests or evidence of native behavior, art quality or human acceptance.",
    }
    write("RESULT.json", result)
    print(json.dumps(result, indent=2))
