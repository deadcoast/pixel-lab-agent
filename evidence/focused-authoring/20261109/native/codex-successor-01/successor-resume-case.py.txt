"""Continue an observed native successor after adding explicit linked revision."""

import argparse
import json
import shutil
from pathlib import Path

from evaluations.request_review_trials import (
    ROOT,
    inventory,
    prepare,
    run,
    sha,
    write_json,
)

GUIDANCE = """This is the caller continuing its completed focused successor work.
SUCCESSOR-ADOPTION.md is current; previous assignments/results remain history.
The current installed kit adds explicit successor links. Continue from retained
artifacts without repeating completed semantic review or changing old evidence.
Work under work/successor-adoption; preserve work/focused-successor and earlier
source/renderer/assets. State and authoring-plar.txt may advance via public tools.
No global settings or persistent-memory writes. Parse JSON as UTF-8.
"""

ASSIGNMENT = """# Adopt and complete the reviewed successor

Continue FOCUSED-RESULT.json and work/focused-successor, preserving that attempt.
The prior native run used focused context and implemented/reviewed a versioned
reduced-motion consumer. Its exact results, failures and any unperformed checks
remain authoritative. Do not assume a pass that the retained result does not show.

The current kit's production-plan adapter now supports optional selection.replaces:
{store, task, output}, exactly the current PLAR production link. New plan ID plus
current expected state hash append the successor, preserve the old plan/intent and
PLAR history, and refuse unresolved jobs across earlier owned generations. It
does not create a job or transfer acceptance. Read the current family-delivery and
production-plan documentation and discover the tool schemas. Default context and
the focused authoring view retain their meaning. Save large reports through the
CLI binary-stdout method in runtime.md instead of shell-embedding JSON.

1. Read the retained focused result, current focused context and exact corrected
   proposal/caller comparison. Have foreground PIXL address only the remaining
   adoption/acceptance questions; retain its native identity. Use its pixel-art
   judgment and actual image access. Do not re-author all historical comparisons
   where the literal obligations and evidence remain unchanged.
2. Ensure the successor PLAR branch describes the actual versioned consumer and
   destination. Update tracked sources/consumer bindings, delivery paths and any
   actual semantic requirement changes explicitly; preserve the original plar.txt
   and old source files. Keep preserved Ready/Start and the dynamic account badge
   coverage honest. Refresh obsolete status/next/evidence prose without inventing
   new constraints. Read fresh requirement hashes after any semantic update.
3. The previous public-plan-proposal.json, if present, is a draft. Compare it with
   the retained corrected proposal and actual successor code. Add new source,
   contract and destination records as needed through pixl_commit; preserve old
   C/I/Q/S/D/E/V records. Scope normal 100ms animation separately from stationary
   reduced-motion display. Keep the three split alpha diagnostics/visual decisions,
   full alpha/selective AA, in-cell margins, scoped expert pacing, qualitative
   coherence and inferred Start distinction. Retain an exact mapping from all 20
   original criteria to the new literal checks, plus reduced-motion requirements.
4. Author the new connected plan using explicit selection.replaces for the three
   linked member assets. Resolve any still-prepared obsolete intent through its
   evidenced local-abandonment lifecycle first; never assert a remote failure or
   rebind the old request. Check that the result's allocations are actually revised
   rather than merely that the graph was saved. Retain exact request_review output
   and independently compare its actual new criteria/controls to the approved
   successor proposal and original sources before accepting work. Coverage is not
   semantic judgment. Preserve the original intent and prior partial trial.
5. Reuse the exact existing PixelLab-produced assets if they satisfy the successor.
   Retain new candidate X.of identities and provenance to the original bytes for
   new outputs; do not claim a provider generated them under the new contract.
   Use current public commit/inspection/completion/family operations for fresh
   mechanical, visual and engine verdicts scoped to the new criteria. Preserve
   failed views/captures. Run the versioned renderer again for normal/reduced modes,
   both consumers, all states and live preference switching; verify actual pixels
   and timing claims at their measured scope. All outputs need their required
   verdicts before completion; then retain/review the family and refresh PLAR/handoff.
   If an actual new PixelLab operation is warranted, retain its exact request for
   the outer connected host rather than fabricating a provider result.
6. Return SUCCESSOR-RESULT.json with exact plan, criterion, source, candidate,
   job, verdict, renderer, allocation and handoff paths/hashes; demonstrate old
   evidence preservation and identify any unmet acceptance. Distinguish actual
   rendered/reviewed reuse from new model-generation quality. Overall quality,
   general host reliability and the wider product remain in development.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", choices=("claude", "codex"))
    parser.add_argument("predecessor", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.resolve()
    prepare(destination, args.host, "plar-authoring-review", args.predecessor.resolve())
    project = destination / "project"
    guidance = GUIDANCE + "\nSelected Python: " + (ROOT / ".venv/Scripts/python.exe").as_posix() + "\n"
    (project / "SUCCESSOR-ADOPTION.md").write_text(ASSIGNMENT, encoding="utf-8")
    for name in ("AGENTS.md", "SESSION.md"):
        (project / name).write_text(guidance, encoding="utf-8")
    (destination / "prompt.txt").write_text("Complete SUCCESSOR-ADOPTION.md and return SUCCESSOR-RESULT.json.\n" + guidance, encoding="utf-8")
    launch = json.loads((destination / "launch.json").read_text(encoding="utf-8"))
    launch["case"] = "focused-successor-adoption"
    write_json(destination / "launch.json", launch)
    specialist = "You are PIXL for the delegated successor acceptance work. " + guidance
    if args.host == "claude":
        write_json(destination / "agents.json", {"pixl": {"description": "Visual asset specialist for successor review and integration.", "prompt": specialist}})
    else:
        (project / ".codex/agents/pixl.toml").write_text('name = "pixl"\ndescription = "PixelLab visual asset specialist."\ndeveloper_instructions = ' + json.dumps(specialist) + "\n", encoding="utf-8")
    identity = json.loads((destination / "identity.json").read_text(encoding="utf-8"))
    identity.update(inputs=inventory(project, ("pixl-kit",)), prompt_sha256=sha(destination / "prompt.txt"), adapter_sha256=sha(Path(__file__)), scope="Native explicit successor allocation, fresh review of reused assets, rendering and completion; outcomes ungraded until independently checked.")
    write_json(destination / "identity.json", identity)
    for name in ("SUCCESSOR-ADOPTION.md", "AGENTS.md", "SESSION.md"):
        shutil.copyfile(project / name, destination / "input-project" / name)
    if args.host == "codex":
        shutil.copyfile(project / ".codex/agents/pixl.toml", destination / "input-project/.codex/agents/pixl.toml")
    shutil.copyfile(__file__, destination / "successor-resume-case.py.txt")
    run(destination)


if __name__ == "__main__":
    main()
