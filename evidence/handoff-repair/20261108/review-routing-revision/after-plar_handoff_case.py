"""Cold specialist/caller correction of a retained consumer contract and handoff."""

import shutil
from pathlib import Path

GUIDANCE = """This is an isolated native PIXL consumer continuation. Work only inside this
consumer using its installed PLAR/PIXL profile, knowledge, skills and available tools.
PHASE.md is the current assignment; older OWNER/STAGE files describe retained stages.
The retained provider evidence and image are controlled fixtures, not upstream art.
The completed production and original contracts/reviews remain historical evidence.
No new generation, credentials, package installs or global settings are assigned.
The caller owns the independent comparison and final consumption.
Native messages are limited to the agents created for this assignment, not other sessions.
"""
PROMPT = """You are the calling agent continuing PHASE.md. Delegate the retained consumer to
one native PIXL specialist, explicitly supplying its assignment and installed skill.
Use PIXL's existing pixel-art knowledge and available tools to assess the art direction,
original requirements, saved criteria and current delivery. Independently compare its
returned contract and handoff with the source and current production state. Resolve
any discrepancies with the same specialist, preserving earlier artifacts. Save
HANDOFF-RESULT.json linking the final exact handoff and your independent comparison,
with actual completed scope and unresolved obligations. Do not rewrite historical
acceptance or manufacture another generation merely to repair the contract.
"""


def setup(project, destination, python, resume):
    if resume is None or not (project / "DELIVERY-RESULT.json").is_file():
        raise ValueError("Handoff correction requires retained completed delivery")
    shutil.copyfile(resume / "provider-state.json", destination / "provider-state.json")
    shutil.copyfile(Path(__file__), destination / "plar_handoff_case.py.txt")
    (project / "PHASE.md").write_text("""# Review the retained asset contract and hand it back
The Ready sample has already been delivered. Reassess its retained request/criteria
and result against the actual brief and consumer sources, using PIXL's specialist
knowledge and useful harness tools. Correct discovered contract or citation defects
in new artifacts and retain an independent caller comparison. Preserve the old
arguments, plans, candidate, verdicts, source bytes and completed provider history.
A corrected future contract does not retroactively replace the one used for delivery.
Explain the applicable pixel-art reasoning and which decisions are expert choices.
Return an exact resumable handoff with current state and remaining obligations.
The existing source-consumer integration can be rechecked; style/family approval and
graphical renderer acceptance remain separate work. No new generation is assigned.
""", encoding="utf-8")
