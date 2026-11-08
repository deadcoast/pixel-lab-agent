"""Cold consumer/source update and reviewed plan continuation using retained work."""

import json
import shutil
from pathlib import Path

from evaluations.host_trials import write_json
from evaluations.plar_asset_case import GUIDANCE
from evaluations.plar_request_fixture import SCHEMAS

__all__ = ["GUIDANCE", "PROMPT", "setup"]

PROMPT = """You are the calling agent resuming the consumer in OWNER.md. Delegate to
PIXL through the installed PLAR/PIXL workflow, inspect its exact revised request and
criteria against the current sources, and complete the assigned request stage.
Retain COLD-RESULT.json with original and current state/job/PLAR links, your independent
review, the actual submitted arguments and remaining work. Preserve previous artifacts.
"""


def setup(project, destination, python, resume):
    if resume is None:
        raise ValueError("PLAR continuation requires a retained first-request attempt")
    source = project / "src/queue-view.ts"
    text = source.read_text(encoding="utf-8")
    assert 'assets/ready.png' in text
    source.write_text(text.replace('assets/ready.png', 'assets/ready-confirmed.png'), encoding="utf-8")
    brief = project / "BRIEF.md"
    brief.write_text(brief.read_text(encoding="utf-8") + "\nCurrent update: Ready must visibly use a check mark with asymmetrical arms to convey successful completion. The destination now follows the updated view. Keep the existing 16x16 canvas, static behavior, transparent background and review display conditions.\n", encoding="utf-8")
    (project / "OWNER.md").write_text("""# Continue the Ready request after the consumer update
The source brief and view changed since the retained first request. Refresh PLAR
against the actual source, preserving existing IDs, other asset history and the Start
control. Continue queue.ready through one newly reviewed request under this updated
contract and retain its resumable state. The original request belongs to the controlled
pixellab-test connection; inspect its actual current provider status before acting.
The connection supports one further controlled request in this stage. Preserve original
attempts and contracts. The assigned deliverable ends at the accepted revised request:
no image or renderer is supplied, no style is already approved, and integration and
art acceptance remain future work. Do not fabricate images, provider observations,
acceptance or a live-service identity. Work inside this consumer only.
""", encoding="utf-8")
    state = json.loads((resume / "provider-state.json").read_bytes())
    if len(state["jobs"]) != 1:
        raise ValueError("Expected exactly one retained source request")
    state["jobs"][0].update(status="failed", reason="Controlled continuation fixture: the original queued attempt has ended without an image.", provider_simulated=True)
    write_json(destination / "provider-state.json", state)
    write_json(project / "provider-schemas.json", SCHEMAS)
    for name in ("plar_request_fixture.py", "pixellab_mcp_fixture.py"):
        shutil.copyfile(Path(__file__).parent / name, destination / name)
    return {"command": str(python), "args": [str(destination / "plar_request_fixture.py"), "--folder", str(destination), "--continuation"]}
