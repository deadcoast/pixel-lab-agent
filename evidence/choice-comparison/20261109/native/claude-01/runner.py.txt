"""Native caller use of focused choices and concise successor comparison."""

import argparse
from pathlib import Path

from evaluations.candidate_review_export_case import prepare as prepare_consumer
from evaluations.host_trials import inventory, sha, write_json
from evaluations.request_review_trials import run
from pixl import service

ASSIGNMENT = """# Focused choices and successor comparison

You are the caller in a bounded native evaluation using this existing consumer.
The completed successor remains delivered. This assignment reads/comparisons;
it does not change production state, existing sources, assets or prior evidence.
Write new work under work/choice-comparison. Use the current kit at
.agents/skills/export-kit (the directory name is inherited from the fixture).
Read its resources/spec/production-plan.md and skills/pixl/references/request-review.md.

1. Read the current authoring context for provenance-correction.plan with the
   public pixl_context / context command, view authoring. Use result_path /
   --result-path to save exact results. Read its relevant choices, including
   destination, caller style and transitive authority. Inspect the compact other
   intake index and follow at least one of its exact retrievals. Explain why being
   unlinked does not by itself make a choice irrelevant or grant a new restriction.
2. Read pixl_request_review / request-review with plan provenance-correction.plan,
   against_plan authoring-01.plan and view changes. Save the exact output. Follow
   both full-report locators and save those exact outputs too; read literal clauses
   programmatically as needed. The compact report is orientation, not a semantic
   verdict or an assertion that these plans are directly consecutive.
3. Delegate to native PIXL a focused semantic review of the actual source choices
   and old/new criteria. It should use its own pixel-art knowledge and the existing
   consumer/source evidence. Preserve every old/new criterion ID and hash in an
   explicit mapping. Explain the changed obligations: alpha diagnostic versus
   visual exterior judgment, geometry versus invented margins, fixed 100 ms versus
   perceived motion quality, family coherence versus identical weight, and reduced
   motion/live preference changes in the shared full and compact consumers. Name
   the authority for each interpretation. Read the actual linked source evidence,
   not only this assignment or the change counts. Do not infer all clauses are
   equivalent because their stage/local IDs align. Additional diagnostics must not
   erase the older failed/unavailable observations. Retain the actual native role
   and child identity; a generic Codex child is not named-role qualification.
4. As caller, independently check the specialist's result against the exact
   exports. Verify all 20 original and 23 successor criteria are accounted for,
   examine the actual changed text/source obligations, distinguish current accepted
   review from historical unavailable evidence, and correct any interpretation
   error in a separately retained follow-up. Do not manufacture approval or change
   old reviews. Saved completed acceptance already exists; it is not newly earned
   by reading this summary. This trial does not resolve the earlier interrupted
   Claude comparison or establish broad artistic/host reliability.
5. Return work/choice-comparison/CALLER-RESULT.json with export locators/hashes,
   selected and other choice IDs, actual specialist identity, mapping/review paths,
   independent caller conclusions, errors or corrections, and exact continuation.
   Keep the return concise; full literal evidence belongs in its exported files.

Use state .pixl/assets/queue.ready/state.px and the host's rooted local MCP or
current-kit CLI. All previous kits, source snapshots and result files stay intact.
No global settings or persistent-memory edits. The overall project remains active.
"""


def prepare(destination, host):
    import json

    prepare_consumer(destination, host)
    destination = destination.resolve()
    project = destination / "project"
    (project / "work/choice-comparison").mkdir()
    guidance = "This is the focused-choice/successor-comparison evaluation. Follow CHOICE-COMPARISON.md, not earlier assignments. Current kit: .agents/skills/export-kit. Preserve existing state/evidence. New work: work/choice-comparison. No global configuration or memory writes. Selected Python: C:/github/pixel-lab-agent/.venv/Scripts/python.exe."
    (project / "CHOICE-COMPARISON.md").write_text(ASSIGNMENT, encoding="utf-8")
    for name in ["AGENTS.md", "SESSION.md"]:
        (project / name).write_text(guidance, encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete the assignment through native PIXL delegation and independent caller review.\n", encoding="utf-8")
    launch = json.loads((destination / "launch.json").read_bytes())
    launch["case"] = "focused-choice-successor-comparison"
    write_json(destination / "launch.json", launch)
    if host == "claude":
        write_json(destination / "agents.json", {"pixl": {"description": "PIXL visual asset specialist for source-authority comparison", "prompt": "You are PIXL in an explicitly delegated comparison evaluation. " + guidance}})
    identity = json.loads((destination / "identity.json").read_bytes())
    identity.update(inputs=inventory(project, ("pixl-kit", "review-kit", "export-kit", "__pycache__")),
                    prompt_sha256=sha(destination / "prompt.txt"), runner_sha256=sha(Path(__file__)))
    write_json(destination / "identity.json", identity)
    (destination / "runner.py.txt").write_bytes(Path(__file__).read_bytes())
    for name, tool, arguments in [
        ("expected-context.json", "pixl_context", {"path": ".pixl/assets/queue.ready/state.px", "focus": "provenance-correction.plan", "view": "authoring"}),
        ("expected-changes.json", "pixl_request_review", {"packet": ".pixl/assets/queue.ready/state.px", "plan": "provenance-correction.plan", "against_plan": "authoring-01.plan", "view": "changes"}),
    ]:
        write_json(destination / name, service.call(tool, arguments, project))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", choices=["claude", "codex"])
    parser.add_argument("destination", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    prepare(args.destination, args.host)
    if not args.prepare_only:
        run(args.destination.resolve())
