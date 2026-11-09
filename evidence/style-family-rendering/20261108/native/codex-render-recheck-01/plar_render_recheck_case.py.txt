"""Explicit renderer-repair continuation; previous native findings remain unchanged."""

import shutil
from pathlib import Path

GUIDANCE = """This is an explicitly guided renderer-repair continuation of a retained
native family review, not a fresh blind trial. RENDER-RECHECK.md is the assignment.
Use the installed PIXL/PLAR skills, actual consumer and prior family result. The new
renderer-recheck helper is versioned separately; old renderer files/captures remain
historical evidence. Its browser uses an isolated temporary profile and loopback
server. No provider generation, global settings or new family artwork is assigned.
Native messages address only agents created for this assignment.
Required delegation is foreground work: ask the native agent to wait for PIXL's
report and finish the caller comparison before ending. A previous host may have
stopped its background child; preserved drafts are useful work, not a final result.
"""

PROMPT = """Continue RENDER-RECHECK.md as the calling agent. Delegate the focused renderer
recheck to PIXL, then independently open and verify its actual new screenshots,
pixel report, findings and current continuation. Preserve the preceding family/style
decision and earlier failures; update only what the new evidence justifies. Save
RENDER-RECHECK-RESULT.json linking the new evidence, caller comparison, available-
member destination outcome, remaining family work and exact current handoff.
"""


def setup(project, destination, python, resume):
    if resume is None or not (project / "RENDER-STAGE.md").is_file():
        raise ValueError("Renderer recheck requires a retained family assignment")
    interrupted = not (project / "FAMILY-RESULT.json").is_file()
    shutil.copyfile(resume / "provider-state.json", destination / "provider-state.json")
    shutil.copyfile(Path(__file__), destination / "plar_render_recheck_case.py.txt")
    source = Path(__file__).resolve().parents[1] / "examples/plar-project/renderer"
    shutil.copytree(source, project / "renderer-recheck", ignore=shutil.ignore_patterns("__pycache__"))
    (project / "RENDER-RECHECK.md").write_text(
        """# Continue the retained review with the corrected renderer
The original capture helper could observe the page before Chromium applied its
final screenshot viewport. Preserve that helper, its captures, failed checks and
the family/style findings in FAMILY-RESULT.json. A separate renderer-recheck/
version now sets device metrics before navigation and captures report/layout/image
in one isolated CDP page. This is a maintainer tool correction, not a new art request
or an automatic acceptance result. Verify the actual new output yourself.

Run node renderer-recheck/capture.mjs --out work/NEW_CAPTURE_DIRECTORY and the
selected Python with renderer-recheck/check.py --project . --capture DIRECTORY.
Open the actual screenshot and relevant native/enlarged views; compare both real
source consumers, current asset paths, source/image hashes and observed placement.
Retain an independent caller comparison. Do not alter the renderer to pass checks,
overwrite earlier results or re-create a family plan that is already retained.
Keep the existing style decision unless actual evidence requires a scoped revision.

If the new evidence resolves available-member destination checks, record that
precise outcome through the existing workflow and update PLAR evidence/next work.
It cannot pass a collective criterion requiring the still-absent members, their
animation, non-color distinction or full family continuity. Preserve meaningful
requirement changes and production-selection diagnostics; do not rebind old jobs
or transfer old verdicts to a different contract. Return a fresh exact handoff and
the actual next useful production action. This continuation is explicitly guided
by a renderer repair; do not relabel the original trial as an unassisted pass.
""" + ("""

## Interrupted original delivery
The previous caller ended while its background PIXL instance was still running;
the host stopped that child and FAMILY-RESULT.json was never delivered. This is a
cold restart from preserved artifacts, not the same native child conversation.
Finish the original RENDER-STAGE.md assignment as well as this renderer repair.
Read the actual saved caller and specialist notes/proposals, independently compare
them and choose the justified style outcome; drafts do not constitute adoption.
Reconcile numerical descriptions against the actual decoded images, including any
claims about the existing vector's edge pixels. Preserve drafts and old failed
captures. Complete the remaining scoped decision, family/state/PLAR updates, caller
comparison and exact handoff, then save FAMILY-RESULT.json and this continuation's
RENDER-RECHECK-RESULT.json. Do not recreate records that already exist. Do not end
while required delegated work is still running; use foreground delegation/wait.
""" if interrupted else ""),
        encoding="utf-8",
    )
