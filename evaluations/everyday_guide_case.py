"""Cold native use of the everyday guide on an already accepted consumer."""

import argparse
import json
from pathlib import Path

from evaluations.candidate_review_export_case import prepare as prepare_consumer
from evaluations.host_trials import inventory, sha, write_json
from evaluations.request_review_trials import run


def prepare(destination, host):
    prepare_consumer(destination, host)
    destination = destination.resolve()
    project = destination / "project"
    identity = json.loads((destination / "identity.json").read_bytes())
    guidance = (
        "This is the everyday-production-guide evaluation. Follow EVERYDAY-ASSIGNMENT.md, "
        "using current kit .agents/skills/export-kit. Older assignments/kits are retained history. "
        "New work belongs under work/everyday-guide. Preserve existing sources, production, "
        "assets and evidence. No global configuration or memory edits. "
        "Selected Python: C:/github/pixel-lab-agent/.venv/Scripts/python.exe."
    )
    assignment = f"""# Return the accepted queue successor through the everyday workflow

You are a cold caller using an existing asset project's completed successor. Use
the current kit's skills/pixl/references/everyday.md and identities-and-paths.md.
The assigned queue is authoring-plar.txt, asset queue.working; plar.txt is an older
generation. Determine the current useful return and continuation from actual saved
state. This is consumption/recovery of accepted work, not a fresh art acceptance.

Delegate this task to a native PIXL child using the host's available route. A
generic native child explicitly loading the current shared profile and skill is
supported when named-role selection is unavailable; report its actual identity.
The optional inherited role file is refreshed to this assignment; its mere presence
does not qualify named-role use.

The specialist should use public CLI/MCP operations to read the selected queue,
export focused authoring for provenance-correction.plan and exact candidate/family
review context for {identity['candidate']}, and retrieve a precise source range
supporting a current requirement. Resolve roots from this actual consumer, not a
maintainer checkout. Retain exact result files with fresh names.

Verify safe recovery by replaying the existing family review {identity['review']}
for {identity['candidate']} using the unchanged observation file
work/export-review/identical-review.json. This should reuse the review without a
state publication. It is not a newly observed review; preserve the original result.
Save an ordinary production handoff for the assigned queue/asset with truthful
expert findings, usable destination/package locators and actual remaining scope.
Obtain the correct requirements and production identities from current public reads;
do not calculate a store hash from a JSON export. Do not edit internal state records.

As caller, independently verify the exported files and retained handoff against
their returned hashes, the selected generation and unchanged prior acceptance.
Record how file, state, requirements, binding and report identities were used.
Keep creation-time family acceptance distinct from current acceptance. Confirm
the replay did not add publication or a provider action. Write the concise result
work/everyday-guide/CALLER-RESULT.json with actual specialist identity, artifact
locators, checks, any failures/corrections and the exact continuation. The overall
product and broader host reliability remain open.
"""
    (project / "work/everyday-guide").mkdir()
    (project / "EVERYDAY-ASSIGNMENT.md").write_text(assignment, encoding="utf-8")
    for name in ["AGENTS.md", "SESSION.md"]:
        (project / name).write_text(guidance, encoding="utf-8")
    # Only this new fixture's unused inherited adapter is refreshed. Prior trials
    # and user's installed role settings remain untouched.
    adapter = project / ".codex/agents/pixl.toml"
    if adapter.is_file():
        adapter.write_text('name = "pixl"\ndescription = "PIXL retained asset specialist"\ndeveloper_instructions = """' + guidance + '\nRead .agents/skills/export-kit/skills/pixl/SKILL.md and its shared profile for this evaluation.\n"""\n', encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete the assignment with native delegation and independent caller verification.\n", encoding="utf-8")
    launch = json.loads((destination / "launch.json").read_bytes())
    launch["case"] = "everyday-production-guide"
    write_json(destination / "launch.json", launch)
    if host == "claude":
        write_json(destination / "agents.json", {"pixl": {"description": "PIXL visual asset specialist for retained production", "prompt": "You are PIXL in this delegated evaluation. " + guidance}})
    identity.update(inputs=inventory(project, ("pixl-kit", "review-kit", "export-kit", "__pycache__")),
                    prompt_sha256=sha(destination / "prompt.txt"), runner_sha256=sha(Path(__file__)))
    write_json(destination / "identity.json", identity)
    (destination / "runner.py.txt").write_bytes(Path(__file__).read_bytes())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", choices=["claude", "codex"])
    parser.add_argument("destination", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    prepare(args.destination, args.host)
    if not args.prepare_only:
        run(args.destination.resolve())
