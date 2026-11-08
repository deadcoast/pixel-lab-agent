"""Selected updated consumer asset to an actual first controlled MCP request."""

import shutil
from pathlib import Path

from evaluations.host_trials import write_json
from evaluations.plar_request_fixture import SCHEMAS

ROOT = Path(__file__).resolve().parents[1]
GUIDANCE = """This is a native selected-asset operation evaluation. Work only inside this
consumer project. Use the packaged PLAR and PIXL skills under
.agents/skills/pixl-kit/skills/. Local PIXL operations and a controlled request-only
pixellab-test connection are available. Its current advertised schemas are also in
provider-schemas.json; it supports a subset of documented PixelLab fields and has
no upstream service. Keep provider_simulated=true. No credentials, package installs,
host changes or other external services are assigned. The caller owns its independent
request/criteria comparison; the specialist must not impersonate it. Keep all helpers
and evidence under this consumer root. The selected Python is supplied below.
"""
PROMPT = """You are the calling agent. Delegate OWNER.md to a native PIXL specialist
using the packaged PLAR/PIXL workflow. Inspect the returned exact request and criteria
against the original sources before adopting them, resolving any discrepancies with
the specialist. Continue through the first accepted request on the controlled MCP
connection and retain its actual identity in durable state. Independently compare
actual submitted arguments with the reviewed artifacts. Save PARENT-RESULT.json with
the actual completed scope, packet/caller review, PLAR/state/job links and remaining
work. No handwritten PX2 setup is required by the assignment; use the installed
workflow's ordinary operations where they help.
"""


def setup(project, destination, python, resume=None):
    if resume is not None:
        raise ValueError("This case starts a new selected-asset request")
    source = ROOT / "evidence/plar-allocation/20261108/forward/project"
    for name in ("BRIEF.md", "SOURCE-MAP.md", "plar.txt"):
        shutil.copyfile(source / name, project / name)
    for folder in ("src", "assets"):
        shutil.copytree(source / folder, project / folder)
    (project / "OWNER.md").write_text(
        """# First Ready candidate request
Use the selected queue.ready asset from plar.txt and the current consumer source.
Prepare a useful representative Ready candidate for this queue UI, preserving the
brief and current source requirements. A sample motif is expert judgment; no style
has already been approved. Keep the existing Start control and other allocation IDs.
The assigned outcome is the first accepted PixelLab request and its resumable local
state, with independent caller review of the exact request and acceptance criteria.
One submission to the controlled pixellab-test connection is authorized. Use the
actual discovered schema, retain the returned provider identity, and link the selected
asset's production state/next action in PLAR. Its simulated queued response ends this
stage: it does not deliver an image, and retrieval, art acceptance and live renderer
acceptance remain future work. Do not mark the asset integrated or fabricate a result.
""",
        encoding="utf-8",
    )
    write_json(project / "provider-schemas.json", SCHEMAS)
    write_json(
        project / "provider-contract-origin.json",
        {
            "source": "https://api.pixellab.ai/mcp/docs",
            "operation": "create_image_pro_flash",
            "scope": "Controlled connection advertises only description, width, height, no_background and seed from the documented operation. This file is not a complete upstream tools/list declaration.",
        },
    )
    for name in ("plar_request_fixture.py", "pixellab_mcp_fixture.py"):
        shutil.copyfile(ROOT / "evaluations" / name, destination / name)
    return {
        "command": str(python),
        "args": [
            str(destination / "plar_request_fixture.py"),
            "--folder",
            str(destination),
        ],
    }
