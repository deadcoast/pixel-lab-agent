"""Native final-kit result export and retry, retaining completed review trials."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from evaluations.candidate_review_case import ROOT, STORE
from evaluations.host_trials import inventory, sha, write_json
from evaluations.request_review_trials import run
from pixl import codec, graph, store


def prepare(destination: Path, host: str) -> None:
    destination = destination.resolve()
    predecessor = ROOT / f"evidence/candidate-review/20261109/native/{host}-01"
    destination.mkdir(parents=True, exist_ok=False)
    project = destination / "project"
    shutil.copytree(predecessor / "project", project, ignore=shutil.ignore_patterns("__pycache__", "node_modules"))
    kit = project / ".agents/skills/export-kit"
    shutil.copytree(ROOT / "plugins/pixl", kit, ignore=shutil.ignore_patterns("__pycache__"))
    doc = store.load(project / STORE)
    graph.validate(doc, project)
    candidate = doc.records["provenance-correction.delivery.task"].fields["ca"][0].id
    review = next(r for r in doc.records.values() if r.kind == "X"
                  and r.fields.get("mt", {}).get("candidate_review") == 1
                  and r.fields["mt"]["candidate"].id == candidate)
    saved = json.loads((project / review.fields["ur"]).read_bytes())
    work = project / "work/export-review"
    work.mkdir()
    write_json(work / "identical-review.json", saved["observation"])
    guidance = (
        "This is a scoped final-kit export evaluation on an already completed review. "
        "Read EXPORT-ASSIGNMENT.md. Use .agents/skills/export-kit only for current operations; "
        "preserve the two older kits and all existing state/evidence. "
        "New work belongs under work/export-review. No global settings or memory edits. "
        f"Selected Python: {(ROOT / '.venv/Scripts/python.exe').as_posix()}."
    )
    for name in ["AGENTS.md", "SESSION.md"]:
        (project / name).write_text(guidance + "\n", encoding="utf-8")
    assignment = f"""# Verify exact result files through the final public interface

You are a native caller verifying a completed review's result handoff. This is a
bounded serialization/retry follow-up, not another art review or generation job.
The earlier native trial remains unchanged outside this isolated copy. Read the
current kit's resources/spec/candidate-review.md, especially Save results directly.

Use the actual local MCP/CLI, not imports of implementation internals or handwritten
copies of tool results. All result paths must be fresh under work/export-review.

1. Use pixl_review_context with result_path, or review-context --result-path, for
   {candidate}, state {STORE}/state.px. Read/parse the exact exported JSON.
2. Use pixl_family / family with result_path to export the current family report.
   Keep creation acceptance distinct from current acceptance.
3. Replay the exact saved request work/export-review/identical-review.json using
   candidate-review / pixl_candidate_review, candidate {candidate}, review ID
   {review.id}, store {STORE}, the current state_hash and a fresh result_path.
   Do not change the request. This must reuse the review with zero publications.
4. Independently check all exported JSON files parse, their bytes/SHA-256 match
   the returned summaries, state remains {codec.digest(doc)}, and acceptance
   remains complete. Retain the compact summaries from actual tool/CLI output.
   Use native execution to parse/hash files; do not transcribe complete JSON.
5. Write work/export-review/EXPORT-RESULT.json with actual calls, summary/file
   locators, verified identities, retry/publication result and any error. For
   Claude, preserve the prior malformed 04-family-snapshot-result.json and the
   caller-corrected copy. Link current exported family/context files as usable
   current results; do not rewrite or relabel the old creation receipt.

This verifies the final package's output path and a historical review's retry.
It does not establish broader art quality, named-role selection or new rendering.
"""
    (project / "EXPORT-ASSIGNMENT.md").write_text(assignment, encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete EXPORT-ASSIGNMENT.md and verify the saved files.\n", encoding="utf-8")
    launch = json.loads((predecessor / "launch.json").read_bytes())

    def relocate(value: str) -> str:
        return value.replace(str(predecessor).replace("\\", "\\\\"), str(destination).replace("\\", "\\\\")).replace(str(predecessor), str(destination)).replace("review-kit", "export-kit")

    launch["command"] = [relocate(arg) for arg in launch["command"]]
    if "configuration_files" in launch:
        launch["configuration_files"] = {name: relocate(path) for name, path in launch["configuration_files"].items()}
    launch.update(cwd=str(project), case="candidate-review-result-export")
    if host == "claude":
        config = relocate((predecessor / "mcp.json").read_text(encoding="utf-8"))
        (destination / "mcp.json").write_text(config, encoding="utf-8")
        write_json(destination / "agents.json", {"pixl": {"description": "PIXL retained asset specialist", "prompt": guidance}})
    write_json(destination / "launch.json", launch)
    write_json(destination / "identity.json", {
        "predecessor": str(predecessor), "baseline_state_hash": codec.digest(doc),
        "candidate": candidate, "review": review.id, "package_files": inventory(kit),
        "inputs": inventory(project, ("pixl-kit", "review-kit", "export-kit", "__pycache__")),
        "prompt_sha256": sha(destination / "prompt.txt"), "runner_sha256": sha(Path(__file__)),
    })
    shutil.copyfile(__file__, destination / "runner.py.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", choices=["claude", "codex"])
    parser.add_argument("destination", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    prepare(args.destination, args.host)
    if not args.prepare_only:
        run(args.destination.resolve())
