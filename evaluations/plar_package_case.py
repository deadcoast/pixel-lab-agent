"""Cold native consumption of the frozen, real-provider queue-family delivery."""

import shutil
from pathlib import Path

from evaluations.host_trials import inventory, write_json

GUIDANCE = """This is a cold native caller-consumption evaluation of retained actual
PixelLab production. PACKAGE-CONSUMPTION.md is the current assignment; older stage
prompts and result files are history. Use the installed PIXL/PLAR skills in
.agents/skills/pixl-kit. The identical frozen runtime is also at ../kit, preserving
CURRENT-HANDOFF.md's entrypoint. Work only in this copied consumer project. Preserve
all pre-existing production state, PLAR, sources, assets, reviews and evidence.
Write your new findings, captures and caller result at new paths. No generation or
asset revision is assigned: consume the delivered package. No host setting changes,
package installs or persistent memory writes. Use foreground native delegation and
wait for its result; the caller performs its own comparison before finishing.
"""

PROMPT = """You are the calling agent for PACKAGE-CONSUMPTION.md. Delegate the package
consumption check to a native PIXL specialist, then independently inspect its
return against the assignment and actual retained files. Resolve discrepancies
with the specialist if necessary. Finish the caller's PACKAGE-RESULT.json with
usable delivered-file paths and hashes, observed status, actual verification,
provenance and remaining limitations, and the exact current continuation. Do not
end while required delegated work is still running.
"""


def setup(project, destination, python, resume):
    if resume:
        raise ValueError("Package consumption starts cold from the frozen production")
    source = (
        Path(__file__).resolve().parents[1]
        / "evidence/pixellab-family-production/20261108"
    )
    original = source / "project"
    excluded = (".agents", ".codex", "__pycache__", "AGENTS.md", "SESSION.md")
    shutil.copytree(
        original, project, dirs_exist_ok=True, ignore=shutil.ignore_patterns(*excluded)
    )
    shutil.copytree(
        source / "kit",
        destination / "kit",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    write_json(
        destination / "origin.json",
        {
            "source": str(original),
            "files": inventory(original, excluded),
            "kit": inventory(source / "kit", ("__pycache__",)),
            "scope": "Fresh copy; production source and frozen kit remain unchanged",
        },
    )
    shutil.copyfile(Path(__file__), destination / "plar_package_case.py.txt")
    (project / "PACKAGE-CONSUMPTION.md").write_text(
        """# Consume the delivered queue family

Recover the production handoff starting at CURRENT-HANDOFF.md. Use the actual
package in this consumer repository to check the queue UI through both its full
and compact views. I need usable asset locations, slicing/timing information and
an honest statement of what is delivered and what remains open, without another
generation or a reconstruction of the earlier planning stage.

Verify the selected family, copied package members and integrated destination
bytes against current state and requirements. Run the retained renderer-live
capture/check helpers into a new work/cold-package directory and inspect the
actual output, including motion observations. Distinguish current acceptance from
historical creation-time flags and old failed attempts. Explain what was actually
generated, constructed or reused. Preserve historical requirement drift rather
than silently rebinding old evidence. Identify any mismatch that prevents honest
consumption; do not alter assets or evidence to make a check pass.

The caller must independently compare the specialist's evidence with the current
assignment, real files and both consumers, then save PACKAGE-RESULT.json linking
its comparison and exact current handoff. Use project-relative paths within this
copied consumer, with byte hashes for the selected files and cited handoff. Report
what your new checks establish separately from earlier reviews and broader quality
or host-reliability claims. Native child resumption, if needed, must be described
as observed; an artifact-based restart is not the same child conversation.
""",
        encoding="utf-8",
    )
