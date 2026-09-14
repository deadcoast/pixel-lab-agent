"""Bind the completed local milestone to its retained evidence; never run proofs."""

import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pixl import codec, delivery, graph, service


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def identity(path):
    target = ROOT / path
    return {"path": str(path).replace("\\", "/"), "sha256": sha(path), "bytes": target.stat().st_size}


def main():
    tests = read("evidence/test-results.json")
    wheel = read("evidence/wheel-check.json")
    bundle = read("plugins/pixl/bundle-manifest.json")
    instructions = read("evidence/family-delivery/instruction-checks.json")
    review = read("evidence/family-delivery/review.json")
    scenario = read("evidence/family-delivery/plugin-scenario/record.json")
    base = Path("evidence/family-delivery/plugin-scenario")
    assert tests["status"] == wheel["status"] == instructions["status"] == "pass"
    assert scenario["passed"] is True and review["remaining_findings"] == []
    for name, expected in tests["runtime_hashes"].items():
        assert sha(Path("pixl") / name) == expected, name
    for item in bundle["files"]:
        assert (
            sha(item["source"])
            == sha(Path("plugins/pixl") / item["path"])
            == sha(base / "copied-kit" / item["path"])
            == item["sha256"]
        ), item["path"]
    for item in bundle["generated_files"]:
        assert sha(Path("plugins/pixl") / item["path"]) == item["sha256"]
    assert sha("plugins/pixl/bundle-manifest.json") == sha(base / "copied-kit/bundle-manifest.json") == scenario["bundle_manifest_sha256"]
    for name, expected in instructions["instruction_sha256"].items():
        assert sha(name) == expected, name
    for item in scenario["instructions"] + scenario["runtime"]:
        assert sha(base / "copied-kit" / item["path"]) == item["sha256"]
    assert sha("evidence/family-delivery/plugin-scenario.py") == sha(base / "executed-script.py") == scenario["script_sha256"]
    assert sha(base / "isolated-runner.py") == scenario["bootstrap_sha256"]
    assert sha("tests/family_support.py") == scenario["fixture_builder_sha256"]
    project = ROOT / base / "project"
    doc = service.load_document(project / ".pixl/state.px")
    graph.validate(doc, project)
    assert codec.digest(doc) == scenario["final_state"]["hash"] and doc.revision == scenario["final_state"]["revision"] == 17
    family = delivery.report(doc, project, "delivery.output")["families"][0]
    assert family == scenario["final_state"]["family"]
    assert family["state"] == "open"
    assert {x["id"]: x["status"] for x in family["requirements"]} == {
        "q.continuity": "unperformed", "q.delivery.engine": "unavailable",
    }
    for path, expected in scenario["old_snapshot_identities"].items():
        assert sha(Path(path)) == expected, path
    history = list((project / ".pixl/history").glob("*.px"))
    for path in history:
        data = path.read_bytes()
        parsed = codec.parse(data)
        assert codec.encode(parsed) == data and codec.digest(parsed) == path.stem
    project_files = [identity(p.relative_to(ROOT)) for p in sorted(project.rglob("*")) if p.is_file()]
    archive = read("evidence/family-delivery/previous/manifest.json")
    for item in archive["files"]:
        path = Path("evidence/family-delivery/previous") / item["path"]
        assert sha(path) == item["sha256"] and (ROOT / path).stat().st_size == item["bytes"]
    inventory = read("training/source-inventory.json")
    for item in inventory["documents"]:
        assert sha(item["path"]) == item["sha256"]
        assert subprocess.check_output(["git", "show", "HEAD:" + item["path"]], cwd=ROOT) == (ROOT / item["path"]).read_bytes()
    for name in ["spec/PIXL-1.md", "pixl/registry.json"]:
        assert subprocess.check_output(["git", "show", "HEAD:" + name], cwd=ROOT) == (ROOT / name).read_bytes()
    assert len(bundle["files"]) == 90 and len(archive["files"]) == 11
    assert tests["tests"]["run"] == 325 and tests["tests"]["passed"] == 324
    assert len(wheel["checks"]) == 33 and len(wheel["family_probe"]["checks"]) == 12
    mcp = sum("mcp" in event["command"] for event in scenario["events"])
    rejections = []
    for index, event in enumerate(scenario["events"]):
        assert event["exit"] in (0, 2), index
        if event["exit"] == 2:
            error = json.loads(event["stderr"])
            assert error["error"] == "delivery_blocked", error
            rejections.append({"event": index, "error": error["error"]})
    assert len(rejections) == 1

    paths = [
        "evidence/test-results.json", "evidence/test-log.txt", "evidence/art-methods/poc-report.json",
        "evidence/wheel-check.json", "evidence/representation-benchmark.json",
        "evidence/family-delivery/previous/manifest.json", "evidence/family-delivery/review.json",
        "evidence/family-delivery/semantic-task-report.md", "evidence/family-delivery/adapter-task-report.md",
        "evidence/family-delivery/instruction-checks.json", "evidence/family-delivery/portable-fixture.json",
        "evidence/family-delivery/plugin-scenario/record.json", "evidence/family-delivery/plugin-scenario/handoff.md",
        "evidence/family-delivery/plugin-scenario.py", "evidence/family-delivery/plugin-scenario/executed-script.py",
        "plugins/pixl/bundle-manifest.json", "pixl/registry-v2.json", "spec/PIXL-2.md", "spec/family-delivery.md",
        "docs/superpowers/specs/2026-09-11-family-delivery-design.md",
        "docs/superpowers/plans/2026-09-11-family-delivery.md", "docs/VERIFICATION.md",
        "training/source-inventory.json", "evidence/source-migration/range-review.json",
        "plugins/pixl/skills/pixl/references/family-delivery.md", "scripts/family_probe.py",
        "scripts/check_wheel.py", "tests/test_packaging.py", "tests/family_support.py",
        "tests/test_families.py", "tests/test_delivery.py", "tests/test_family_operations.py",
        "evidence/family-delivery/audit.py",
    ]
    summary = {
        "status": "complete", "observed_at": datetime.now(UTC).isoformat(),
        "scope": "Fourth local development milestone: exact approved sample dependencies, family membership/destination planning, collective acceptance and immutable local delivery through PIXL skills, CLI and MCP.",
        "branch": subprocess.check_output(["git", "branch", "--show-current"], text=True, cwd=ROOT).strip(),
        "starting_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, cwd=ROOT).strip(),
        "current_supplied_files_unchanged": 5, "px1_specification_and_registry_unchanged": True,
        "px2_registry_version": read("pixl/registry-v2.json")["version"],
        "family_extension": ["F.bs", "F.mb", "F.ds", "X.xs"], "automatic_legacy_conversion": False,
        "prior_milestone_files_preserved": 11, "verified_bundle_files": 90,
        "verified_generated_files": len(bundle["generated_files"]),
        "runtime_matches_test_receipt": True, "instructions_match_validation_receipt": True,
        "tests": tests["tests"],
        "new_tests": {"family_semantics": 23, "delivery": 21, "family_operations": 9, "total": 53},
        "reference_pocs": tests["art_pocs"], "verified_citations": 93,
        "wheel": {"status": wheel["status"], "files": wheel["wheel_files"], "operations": len(wheel["checks"]), "family_operations": 12, "scope": wheel["scope"]},
        "copied_plugin": {"operations": 32, "family_operations": 12, "scope": "Dependency-isolated public CLI from a retained synthetic preaccepted checkpoint; exact member copies and cold amended membership; no real visual/engine acceptance."},
        "additional_checks": {
            "ruff": "pass: pixl scripts tests setup.py",
            "mypy": "pass: pixl, 18 modules; default excludes some untyped function bodies",
            "git_diff_whitespace": "pass with CRLF recognized as a line ending",
            "codex_skill_checks": 3, "codex_plugin_errors": instructions["plugin_errors"],
            "native_claude_checks": 3, "relative_links": instructions["relative_links"],
        },
        "development_review": {
            "status": review["status"], "resolved_findings": [finding["id"] for finding in review["findings"]],
            "remaining_findings": [], "independent_final_review": review["independent_final_review"],
        },
        "behavior_evaluation": {
            "status": "completed_bounded_scripted_exercise", "scope": scenario["purpose"],
            "report_sha256": sha(base / "record.json"), "evaluated_manifest_sha256": scenario["bundle_manifest_sha256"],
            "script_sha256": scenario["script_sha256"], "verified_manifest_entries": 90,
            "processes": len(scenario["events"]), "cli_processes": len(scenario["events"]) - mcp, "mcp_processes": mcp,
            "separate_runtime_origin_check": True, "expected_rejections": rejections, "unexpected_process_errors": 0,
            "final_revision": doc.revision, "final_state_sha256": codec.digest(doc), "final_delivery_state": "open",
            "collective_continuity": "unperformed", "engine_acceptance": "unavailable",
            "retained_project_files": len(project_files), "canonical_history_snapshots_verified": len(history),
            "old_manifest_and_member_hashes_preserved": True,
            "parent_rechecked_final_report_and_all_manifest_source_plugin_copy_identities": True,
            "earlier_source_adapter_walkthrough": "Preserved separately in evidence/family-delivery/adapter-scenario; not treated as the copied-plugin evaluation or a behavioral baseline.",
            "limits": scenario["limits"],
        },
        "source_identity": [identity(item["path"]) for item in inventory["documents"]],
        "evidence": [identity(path) for path in paths], "retained_scenario_project": project_files,
        "remaining_work": [
            "Stage 5: evaluate exact packaged PIXL instructions across Claude and Codex with retained host/tool behavior and repeated task outcomes.",
            "Actual animation playback or tile-neighborhood artistic continuity for a project-selected asset family.",
            "Actual provider discovery, authorization, generation/reconciliation and returned artifact evidence.",
            "Actual target-engine import and integration acceptance of retained production assets.",
        ],
        "limitations": [
            "Completes the scoped local family/delivery operation, not the overall product or its artistic expertise.",
            "No real provider call, art generation, visual acceptance or engine execution was performed.",
            "Input checkpoint sample/member verdicts and job observations are explicitly synthetic claims.",
            "The single scripted and inspected copied-plugin exercise does not establish independent profile compliance, repeated reliability or cross-host model improvement.",
            "Unrooted graph validation cannot read frozen manifest bindings or copied bytes; family reports and publication require rooted checks.",
            "Retention can leave family criteria and destination/adoption unresolved; snapshot success creates no acceptance.",
            "Failed publication may leave unreferenced immutable files; state.px remains the authority.",
            "One existing Windows symlink test remains skipped without OS privilege; the new junction regression executed and passed.",
        ],
    }
    output = ROOT / "evidence/family-delivery/development-summary.json"
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], "summary": str(output.relative_to(ROOT)), "sha256": sha(output), "evidence_files": len(paths), "scenario_files": len(project_files), "history_snapshots": len(history), "processes": len(scenario["events"]), "mcp": mcp}))


if __name__ == "__main__":
    main()
