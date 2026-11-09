"""Style adoption, incomplete-family review and actual consumer rendering."""

import shutil
from pathlib import Path

GUIDANCE = """This is an isolated native PIXL continuation in an existing consumer.
RENDER-STAGE.md is the current assignment; earlier OWNER/STAGE/PHASE files retain
their original historical scopes. Use the installed shared PIXL/PLAR workflows and
your existing domain expertise. The caller owns independent review and its scoped
style decision. The retained image/provider records are controlled fixtures.
Work in this consumer; the supplied renderer uses its own temporary browser profile
and local loopback server, with no global settings or account changes. Preserve
earlier artifacts and use fresh capture directories. No new art generation is
assigned in this style/render review. Native messages address only this task's agents.
"""

PROMPT = """Continue RENDER-STAGE.md as the calling agent. Delegate the visual/style
assessment and family continuation to one native PIXL specialist using the installed
skill. Exercise the actual consumer, inspect the rendered images and independently
compare the returned findings and state. Resolve discrepancies with that specialist
and preserve earlier evidence. Make the scoped representative-style decision supported
by the results; do not ask the user to select another project. Save FAMILY-RESULT.json
linking the style decision, exact sample identity, family inventory/next work, actual
render evidence, caller comparison, current PLAR/state and exact resumable handoff.
"""


def setup(project, destination, python, resume):
    if resume is None or not (project / "HANDOFF-RESULT.json").is_file():
        raise ValueError("Style/render continuation requires the completed handoff")
    shutil.copyfile(resume / "provider-state.json", destination / "provider-state.json")
    shutil.copyfile(Path(__file__), destination / "plar_family_case.py.txt")
    source = Path(__file__).resolve().parents[1] / "examples/plar-project/renderer"
    shutil.copytree(source, project / "renderer", ignore=shutil.ignore_patterns("__pycache__"))
    (project / "RENDER-STAGE.md").write_text(
        """# Review the representative style and render the existing consumers
Continue the retained Ready delivery and corrected prospective contract. Inspect
the actual supplied art and the prior assessment, verify factual descriptions,
and decide whether this sample should guide the remaining status family under the
brief. You are authorized to make the scoped caller style decision for this
representative consumer using PIXL's recommendations and your independent review.
Preserve the historical request, contracts, verdicts, candidate and provider records;
any new review or acceptance must identify its own scope and evidence.

The consumer now has a runnable browser entry point in renderer/. It imports the
actual src/queue.ts and src/queue-view.ts and uses the mapped image files. Run
node renderer/capture.mjs --out work/NEW_CAPTURE_DIRECTORY
to retain browser observations, native/enlarged panel views and destination.png.
Use the selected Python with renderer/check.py --project . --capture DIRECTORY
to independently check retained identities, screenshot pixels and available PNG
compositing/scaling. That checker does not supply the visual/style decision.
Create the parent work directory if needed. The command detects an installed local
Chrome/Edge and uses a separate temporary profile. A new capture requires a new
output directory. Inspect the resulting images through the host's image tools;
the report alone supplies no visual verdict. Do not edit the renderer to obtain
a passing capture. Use its measured facts, actual source modules and observed
screen to assess sampling, alpha compositing, placement and backend-to-view mapping
in both consumers. This stage supplies a representative browser renderer; it does
not retroactively change earlier no-renderer observations.

Review the family as it actually exists. Preserve the existing Start vector and
all source requirements, distinguish absent members from rejected ones, and retain
an actionable continuation for remaining members. Do not manufacture replacement
images, a completed family, provider activity or reviews of nonexistent artwork.
Update the consumer's PLAR/workflow through the appropriate existing operations,
preserving history and meaningful requirements. Separate sample/style adoption,
available-member destination acceptance, collective family acceptance and actual
PixelLab-generated quality. The latter is not established by this controlled sample.
""",
        encoding="utf-8",
    )
