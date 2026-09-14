"""Retain one developer-agent knowledge-operation evaluation; never rebuild sources.

Run with the repository's selected .venv Python. This helper records actual copied
CLI/stdin-stdout MCP traffic; it does not generate art or invoke remote services.
The recorded applicability judgment is supplied by the evaluator, not this script.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = Path(__file__).with_suffix(".json")


def stamp():
    return datetime.now(UTC).isoformat()


def identity(path):
    raw = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def save(report):
    report["updated_at"] = stamp()
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def setup():
    if REPORT.exists():
        raise RuntimeError("Refusing to overwrite prior evaluation evidence")
    temp = Path(tempfile.mkdtemp(prefix="pixl knowledge evaluation "))
    plugin = temp / "kit" / "pixl"
    project = temp / "project"
    shutil.copytree(ROOT / "plugins/pixl", plugin, ignore=shutil.ignore_patterns("__pycache__"))
    project.mkdir()
    dependencies = [path for path in sys.path if path.endswith("site-packages")]
    launch = f"import sys,runpy;sys.path.extend({dependencies!r});p=sys.argv[1];sys.argv=sys.argv[1:];runpy.run_path(p,run_name='__main__')"
    instructions = ["AGENTS.md", "plugins/pixl/skills/pixl/SKILL.md", "plugins/pixl/skills/pixl/references/knowledge.md", "plugins/pixl/skills/pixl/references/runtime.md", "plugins/pixl/skills/pixl/references/production.md", "plugins/pixl/resources/agent/PROFILE.md", "plugins/pixl/resources/spec/PIXL-1.md", "plugins/pixl/runtime/pixl/registry.json", "tests/test_packaging.py"]
    report = {
        "schema": 1,
        "created_at": stamp(),
        "evaluation_kind": "single developer-agent behavior exercise with real copied local CLI and stdio MCP",
        "role_boundary": "Developer evaluator explicitly acts as PIXL only for the supplied production scenario; no permanent role activation.",
        "scenario": {
            "question": "Should ordered dithering be applied to a 32x32 top-down item family with a native-size readability concern?",
            "supplied_constraints": ["32x32 canvas", "top-down item family", "native-size readability concern", "ordered dithering is uncertain"],
            "observations": [],
            "missing_project_evidence": ["actual item sprites", "supplied style references", "item identities and gameplay roles", "palette/ramp restrictions", "background and display-scale context", "target-engine route"],
        },
        "environment": {
            "python": sys.executable,
            "python_version": sys.version,
            "dependency_site_directories": dependencies,
            "temp_root": str(temp),
            "plugin": str(plugin),
            "project": str(project),
            "resources": str(plugin / "resources"),
            "runner": [sys.executable, "-I", "-c", launch, str(plugin / "scripts/pixl.py")],
            "removed_environment_variables": ["PYTHONPATH", "PIXL_PLUGIN_ROOT"],
            "isolation": "Child processes use -I, only selected dependency site directories, copied runner/runtime, and a separate temporary project cwd.",
        },
        "instruction_identities": [identity(ROOT / path) for path in instructions],
        "bundle_manifest": identity(plugin / "bundle-manifest.json"),
        "steps": [],
        "result": {"status": "in_progress"},
        "limitations": ["Single developer-agent exercise, not a controlled model benchmark or proof across models.", "Local stdio MCP client exercise, not automatic harness discovery.", "No art generated or supplied for visual review; no remote calls or engine acceptance.", "Existing bundled reference receipts may be read but are not fresh project-specific proofs."],
    }
    save(report)
    print(json.dumps({"report": str(REPORT), "environment": report["environment"]}, indent=2))


def run(report, label, args, requests=None, command=None):
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.pop("PIXL_PLUGIN_ROOT", None)
    replacements = {"{resources}": report["environment"]["resources"], "{project}": report["environment"]["project"], "{plugin}": report["environment"]["plugin"]}
    actual = []
    for arg in args:
        for key, value in replacements.items():
            arg = arg.replace(key, value)
        actual.append(arg)
    argv = command if command is not None else report["environment"]["runner"] + actual
    incoming = None if requests is None else "".join(json.dumps(req) + "\n" for req in requests)
    result = subprocess.run(argv, cwd=report["environment"]["project"], env=env, input=incoming, encoding="utf-8", capture_output=True, check=False, timeout=30)
    step = {"sequence": len(report["steps"]) + 1, "at": stamp(), "label": label, "command": argv, "cwd": report["environment"]["project"], "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    if requests is not None:
        step["requests"] = requests
        step["responses"] = [json.loads(line) for line in result.stdout.splitlines()]
    else:
        try:
            step["response"] = json.loads(result.stdout)
        except json.JSONDecodeError:
            pass
    report["steps"].append(step)
    save(report)
    display = dict(step)
    if "response" in display or "responses" in display:
        display.pop("stdout")
    print(json.dumps(display, indent=2, ensure_ascii=False))


def mcp_prefix():
    return [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "pixl-knowledge-evaluator", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
    ]


def finalize(report):
    """Retain this evaluator's judgment and mechanically check its recorded inputs."""
    steps = report["steps"]
    if len(steps) != 20:
        raise RuntimeError("This judgment is tied to the original 20-step exercise")
    resources = Path(report["environment"]["resources"])
    plugin = Path(report["environment"]["plugin"])
    project = Path(report["environment"]["project"])
    inventory = steps[1]["response"]
    documents = {item["path"]: item for item in inventory["documents"]}
    assert inventory["files_verified"]
    assert steps[8]["responses"][-1]["result"]["structuredContent"] == inventory
    assert steps[7]["exit_code"] == 2
    assert json.loads(steps[7]["stderr"])["error"] == "source_hash"
    assert not steps[7]["stdout"]
    assert all(step["exit_code"] == 0 for step in steps if step["sequence"] != 8)
    retrieved = []
    for step in steps:
        if "responses" in step:
            for response in step["responses"]:
                assert not response.get("result", {}).get("isError", False)
            args = step.get("requests", [])[-1].get("params", {}).get("arguments", {})
            data = step["responses"][-1].get("result", {}).get("structuredContent", {})
            path = args.get("path")
        else:
            data = step.get("response", {})
            path = None
            if "text" in data and "--expect" in step["command"]:
                path = Path(step["command"][step["command"].index("source") + 1]).relative_to(resources).as_posix()
        if path is not None and "text" in data:
            actual = resources / path
            raw = actual.read_bytes()
            assert hashlib.sha256(raw).hexdigest() == data["sha256"]
            lines = raw.decode("utf-8").splitlines(keepends=True)
            assert "".join(lines[data["start"] - 1:data["end"]]) == data["text"]
            assert len(data["text"].encode("utf-8")) == data["bytes"]
            retrieved.append({"step": step["sequence"], "path": path, "sha256": data["sha256"], "start": data["start"], "end": data["end"], "bytes": data["bytes"], "inventory_id": documents.get(path, {}).get("id"), "authority": "supplied source" if path in documents else "context-linked local curation or receipt"})
    methods = [steps[3]["response"], steps[4]["response"]]
    for method in methods:
        for citation in method["sources"]:
            assert any(all(item[key] == citation[key] for key in ("path", "start", "end")) for item in retrieved)
    provenance = json.loads(steps[19]["stdout"].splitlines()[-1])
    assert Path(provenance["runtime_file"]).resolve() == (plugin / "runtime/pixl/__init__.py").resolve()
    assert Path(provenance["resource_root"]).resolve() == resources.resolve()
    manifest = json.loads((plugin / "bundle-manifest.json").read_text(encoding="utf-8"))
    for entry in manifest["files"]:
        assert identity(plugin / entry["path"])["sha256"] == entry["sha256"]
    assert identity(plugin / "bundle-manifest.json")["sha256"] == report["bundle_manifest"]["sha256"]
    report["snapshot_verification"] = {
        "checked_at": stamp(),
        "copied_manifest_files_verified": len(manifest["files"]),
        "runtime_provenance": provenance,
        "source_slices_verified_against_copied_bytes": len(retrieved),
        "all_five_selected_method_citations_retrieved": True,
        "instruction_and_data_identities": [identity(plugin / path) for path in ("skills/pixl/SKILL.md", "skills/pixl/references/knowledge.md", "resources/agent/PROFILE.md", "resources/spec/PIXL-1.md", "runtime/pixl/registry.json", "runtime/pixl/service.py", "runtime/pixl/mcp.py", "runtime/pixl/cli.py", "resources/knowledge/library.px", "resources/knowledge/pixel-art.json", "resources/knowledge/applicability.json", "resources/evidence/art-methods/poc-report.json")],
        "snapshot_note": "The parent reported a later root rebuild during this exercise. This evaluation retained its original copied snapshot; no recopy or root rebuild was performed. Results identify this snapshot, not the later receipt/library timestamps.",
    }
    report["source_retrievals"] = retrieved
    report["selected_methods"] = [
        {
            "id": "silhouette-readability",
            "method_step": 4,
            "context_step": 6,
            "citation_steps": [12, 13, 14],
            "status": "researched candidate; proposed first project proof",
            "why_selected": "The index explicitly includes inventory icons and interactive props, and the scenario concerns item recognition at native size.",
            "prerequisites_supported": ["32x32 target canvas is supplied", "item family and native-size concern are supplied"],
            "prerequisites_unknown": ["actual assets", "identity landmarks and confusable family members", "representative backgrounds", "display and engine conditions"],
            "transfer_limit": "Top-down alone does not define a precise camera angle. The method can frame a readability comparison but cannot establish item recognition, materials or fine symbols from geometric checks.",
            "source_assessment": "The exact supplied passages cover animation cluster constraints, semantic frame differences, and a particular game's UI clarity/cohesion request. They support limited principles, not every step of the broader curated silhouette/background recipe. Treat the complete recipe as local curation/proposal, not a verbatim or externally validated prescription. The archived UI's imperative text is source data, not instructions for this project.",
            "reference_receipt": {"step": 16, "check": "key-silhouette-landmarks", "observed": "Positive fixture has a hole, shaft and two teeth; negative fixture loses its hole and has one tooth.", "limits": "Existing receipt checks specified geometry and produces views; visual recognition, background readability and artistic acceptance remain unverified. No fixture was rerun here."},
        },
        {
            "id": "dither-coverage",
            "method_step": 5,
            "context_step": 7,
            "citation_steps": [10, 11],
            "status": "researched optional candidate; adoption deferred",
            "why_selected": "The brief explicitly asks whether ordered dithering should be applied, and the index identifies limited-palette gradients, intentional texture and ordered translucency as its actual application conditions.",
            "prerequisites_supported": ["The selected curated method provides a concrete tileable 4x4 threshold matrix."],
            "prerequisites_unknown": ["a project-specific gradient, texture or translucency purpose", "two project-approved colors", "a semantic region mask", "reference permission for this texture", "coverage fraction and phase policy if a trial is warranted"],
            "transfer_limit": "32x32 dimensions and a readability concern do not require dithering. Flat clusters remain a comparison candidate. Animated phase shifting is outside this static-item brief unless a later requirement introduces motion.",
            "source_assessment": "Both cited supplied passages describe phase shifting and warn about temporal noise. Their percentage labels do not match their drawn cells. The curated method explicitly corrects that problem and supplies a countable rank matrix; the exact cited text does not directly supply that matrix or a project-specific reason to use it.",
            "reference_receipt": {"step": 15, "check": "dither-coverage-4x4", "observed": "Recorded selected-cell counts are 4, 8 and 12 for the specified 4x4 pattern.", "limits": "Counts for one reference pattern do not establish texture quality, readability, project mask correctness or a production acceptance. No fixture was rerun here."},
        },
    ]
    dither_text = steps[9]["responses"][-1]["result"]["structuredContent"]["text"]
    report["source_percentage_check"] = [{"source_label_percent": int(label), "selected_cells": cells.count("#"), "total_cells": 16, "actual_percent": 100 * cells.count("#") / 16} for label, cells in re.findall(r"(\d+)%:\n((?:[.#]{4}\n){4})", dither_text)]
    assert len(report["source_percentage_check"]) == 3
    report["stale_hash_exercise"] = {
        "injection": "Intentionally supplied the inventory's historical deep-research SHA-256 with the current source path and current cited bounds; source bytes were not changed.",
        "failure_step": 8,
        "expected_hash": documents["training/original-docs/PIXEL-ART-DEEP-RESEARCH.md"]["previous"]["sha256"],
        "observed": "CLI exit 2, source_hash diagnostic, no source text returned.",
        "adoption_paused": True,
        "recovery_steps": [9, 10],
        "recovery": "Discovered actual local MCP schemas and refreshed installed inventory; files_verified remained true. Retrieved the same current citation with scope=library and the verified current hash. Inspected its content before assessing applicability; neither previous path nor old receipts were substituted.",
        "status": "expected failure preserved; current-revision retrieval recovered",
    }
    report["instruction_defects"] = [
        {"severity": "minor", "location": "skills/pixl/references/knowledge.md: Failures and recovery", "finding": "The changed-hash row conflates an unusable inventory/source installation with a stale caller-supplied expected hash. Here the installation verified successfully after rejecting a historical expected hash.", "suggestion": "Explicitly distinguish those cases: rediscover a verified current inventory and reassess current citations for a stale expectation; stop using the installation when its declared inventory does not match its own bytes.", "blocking": False},
    ]
    report["workflow_observations"] = [
        "The written operation led to source discovery, actual index-based method selection, complete contexts, exact hash-bound retrieval, applicability assessment, and a bounded next proof without an invented UDL draft operation.",
        "The reference receipt's dependency closure included unrelated fixture artifact records. They were retained as returned; their presence did not justify selecting unrelated methods or applying their contracts to this project.",
        "Context retrieval worked through the CLI using the installed resource root; MCP source retrieval used the discovered library scope while its configured project root stayed separate.",
        "The two supplied dither passages repeat the same example and are not independent corroboration.",
    ]
    report["evaluation_helper_events"] = [{"step": 19, "event": "The initial provenance probe exited normally with the CLI before printing post-run module identity. This was an evaluator-helper defect, not a plugin failure.", "recovery_step": 20, "recovery": "The helper catches only a successful SystemExit, then records the loaded module and resource paths. Both resolve inside the copied plugin. The initial output remains preserved."}]
    next_proof = {
        "status": "proposed; not executed or approved",
        "question": "Can the representative item preserve its required identity at native 32x32 size, and, if the actual style calls for it, does scoped ordered dithering improve a defined material/gradient cue without reducing that identity?",
        "missing_inputs": ["one representative item and its nearest confusable family neighbor", "style references", "named identity landmarks and required gaps", "actual gameplay or inventory backgrounds", "palette and material/texture intent"],
        "smallest_artifact": "First inspect the representative item's existing colored view and flat mask beside its nearest family neighbor on representative backgrounds. If a source-specific dither purpose exists, compare one flat version with one otherwise identical version using dithering only in an agreed semantic region.",
        "observable_acceptance": ["At native size, a reviewer can identify the intended item, distinguish its nearest family neighbor, and point to the required landmarks and open gaps on each target background.", "Any dither trial preserves the same outer silhouette and changes only the intended region using the project's approved colors; measure actual selected-cell coverage over that region.", "The visual comparison demonstrates the stated material/gradient purpose without obscuring a required landmark or reducing item/background separation; enlarged review checks cluster changes. Reviewer observations remain distinct from pixel counts."],
        "dependent_work": "Family-wide detailing, variations and any dither rollout remain pending this project-specific proof. Revise a failing baseline silhouette before testing decoration. Keep dithering unadopted if its purpose, prerequisites or visual result remain unresolved.",
        "retained_result_type": "Project-owned JSON evaluation/research notes, not invented PIXL syntax or an adopted D record.",
    }
    report["result"] = {
        "status": "knowledge_operation_complete_at_researched_candidate_and_next_proof_boundary",
        "production_status": "unproven; no asset or adopted production decision",
        "plain_language_response": "Begin with a native-size readability check of a representative item and its closest-looking family neighbor. Ordered dithering is optional: consider a masked comparison only if the actual references, palette limits or material goal call for it. The supplied examples warn about noise and contain incorrect percentage labels, so count coverage explicitly. Without sprites, references and backgrounds, I cannot determine whether dithering will help this family; the next step is the stated project-specific comparison.",
        "next_proof": next_proof,
        "verification_levels": {"discovery_format": "Actual copied CLI help and stdio MCP initialize/tools/list/source discovery exercised; no host auto-discovery test.", "recorded_behavior": "One developer-agent exercise with recorded tool traffic, judgment, and expected stale-hash recovery.", "actual_task_outcomes": "Source-grounded candidate research and next proof retained; no art generation, visual art evaluation, remote operation or engine acceptance."},
    }
    project_result = project / "knowledge-operation-result.json"
    project_payload = {key: report[key] for key in ("evaluation_kind", "role_boundary", "scenario", "bundle_manifest", "source_retrievals", "selected_methods", "stale_hash_exercise", "result", "limitations")}
    project_result.write_text(json.dumps(project_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report["project_owned_context"] = identity(project_result)
    report["project_owned_context"]["content"] = project_payload
    save(report)
    print(json.dumps({"report": str(REPORT), "status": report["result"]["status"], "steps": len(steps), "source_slices_verified": len(retrieved), "copied_manifest_files_verified": len(manifest["files"]), "project_context": str(project_result)}, indent=2))


def main():
    action, *args = sys.argv[1:]
    if action == "setup":
        setup()
        return
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    if action == "cli":
        run(report, "CLI " + " ".join(args), args)
    elif action == "mcp-discover":
        requests = mcp_prefix() + [{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "pixl_sources", "arguments": {}}}]
        run(report, "MCP initialize, tools/list and source discovery", ["mcp", "--root", "{project}"], requests)
    elif action == "mcp-call":
        name, arguments = args
        requests = mcp_prefix() + [{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": name, "arguments": json.loads(arguments)}}]
        run(report, "MCP " + name, ["mcp", "--root", "{project}"], requests)
    elif action == "probe":
        plugin = Path(report["environment"]["plugin"])
        dependencies = report["environment"]["dependency_site_directories"]
        code = (
            "import sys,runpy,os,json\n"
            f"sys.path.extend({dependencies!r})\n"
            f"p={str(plugin / 'scripts/pixl.py')!r}\n"
            "sys.argv=[p,'sources']\n"
            "try:\n    runpy.run_path(p,run_name='__main__')\n"
            "except SystemExit as stop:\n    if stop.code not in (None, 0): raise\n"
            "import pixl\nfrom pixl.service import resource_root\n"
            "print(json.dumps({'runtime_file':pixl.__file__,'resource_root':str(resource_root()),'sys_path':sys.path}))\n"
        )
        run(report, "Copied runner runtime provenance probe", [], command=[report["environment"]["python"], "-I", "-c", code])
    elif action == "finalize":
        finalize(report)
    elif action == "instruction-review":
        if "instruction_revision_review" in report:
            raise RuntimeError("Refusing to overwrite a prior instruction revision review")
        preserved_keys = ("steps", "snapshot_verification", "selected_methods", "stale_hash_exercise", "instruction_defects", "result", "project_owned_context")
        original_digest = hashlib.sha256(json.dumps({key: report[key] for key in preserved_keys}, sort_keys=True).encode("utf-8")).hexdigest()
        reference = ROOT / "plugins/pixl/skills/pixl/references/knowledge.md"
        lines = reference.read_text(encoding="utf-8").splitlines()
        table_start = lines.index("| Observation | Required response |")
        table_end = next(index for index in range(table_start, len(lines)) if not lines[index].startswith("|"))
        report["instruction_revision_review"] = {
            "reviewed_at": stamp(),
            "scope": "Read-only review of the revised Failures and recovery table; no repeated production scenario, copied runtime calls or bundle recopy.",
            "current_skill_identity": identity(ROOT / "plugins/pixl/skills/pixl/SKILL.md"),
            "current_knowledge_reference_identity": identity(reference),
            "reviewed_range": {"start": table_start + 1, "end": table_end, "text": "\n".join(lines[table_start:table_end]) + "\n"},
            "resolution": "resolved_by_instruction_review",
            "reason": "The table now distinguishes a failing inventory/source installation from a rejected stale expectation with fresh successful discovery. Recovery preserves the failure, re-reads the current method/context, and retrieves its current citation with the matching identity. It explicitly forbids carrying an old range into a new revision by only replacing the hash and falls back to the installation-conflict response when discovery fails.",
            "behavior_validation": "Not rerun. The revised wording was not part of the original copied-snapshot execution, and this review establishes only that it resolves the reported textual ambiguity.",
            "preserved_original_sections": list(preserved_keys),
            "preserved_original_sections_sha256": original_digest,
        }
        save(report)
        reread = json.loads(REPORT.read_text(encoding="utf-8"))
        assert hashlib.sha256(json.dumps({key: reread[key] for key in preserved_keys}, sort_keys=True).encode("utf-8")).hexdigest() == original_digest
        print(json.dumps(report["instruction_revision_review"], indent=2, ensure_ascii=False))
    else:
        raise ValueError(action)


if __name__ == "__main__":
    main()
