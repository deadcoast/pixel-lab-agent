"""Reference-aware delegated edit scenario through a controlled PixelLab MCP surface."""
import shutil
from pathlib import Path

from evaluations.host_trials import write_json
from evaluations.pixellab_mcp_fixture import SCHEMAS

ROOT = Path(__file__).resolve().parents[1]
GUIDANCE = """This is a controlled native delegated PixelLab workflow evaluation.
Work only in this consumer project. Use .agents/skills/pixl-kit/skills/pixl/SKILL.md,
the delegation/request-review operation and the normal durable provider/inspection
operations. The pixellab-test MCP connection advertises the exact input schemas
saved in provider-schemas.json. Its operation names and argument forms are based
on the retained current official declarations; all responses and images are
controlled fixtures. No upstream provider is connected. Use this connection only.
Download from its returned loopback URL; never substitute or copy reference.png as
the delivered output. Inspect actual returned files. Keep provider_simulated=true.
The selected Python is supplied below; dependencies are already installed.
Do not read credentials, install packages, contact other services or change host settings.
The caller owns independent contract review and final consumption, not the specialist.
"""
PROMPT = """You are the calling agent. Complete OWNER.md by delegating to a native PIXL
specialist using the packaged workflow. Review its exact request/criteria packet
against the original brief before adoption, then continue it through the assigned
PixelLab edit, retrieval, inspection and delivery. If the candidate needs revision,
retain the failure and review the changed contract before continuing. Preserve
unknown submission outcomes and reconcile saved jobs before another call. Open the
final returned PNG yourself and verify the consumer mapping. Save PARENT-RESULT.json
with actual artifacts, your own review, state/provider identities and remaining
limitations. This evaluation requires completed delivery through the exposed
controlled MCP service; a contract-only plan is not the assigned outcome.
"""


def setup(project: Path, destination: Path, python: Path, resume: Path | None = None) -> dict:
    if resume is None:
        (project / "src").mkdir()
        (project / "assets").mkdir()
        (project / "OWNER.md").write_text("""# Restore the robot identity for this consumer
Use PixelLab to repair input.png to match the approved reference.png: restore the
two antennae and two yellow eyes. Preserve the front-facing teal body, dark outline,
32x32 canvas, the reference palette and binary transparency; no ground shadow.
Deliver one reviewed PNG at assets/robot.png, which src/avatar.ts already consumes.
The input and reference are controlled evaluation fixtures. Their geometry/palette
requirements apply only to this assignment. The first image is the content to edit;
reference.png is the approved identity reference, not just a text description.
The controlled MCP service is authorized for one edit and, if needed after review,
one corrective attempt. Real remote production is outside this evaluation.
The specialist should use durable job state and candidate inspection; the caller
must review the exact contract, then open and consume the delivered result.
Source/path integration is required. No runnable target engine is supplied, so
live engine rendering remains unverified rather than a prerequisite for this scope.
""", encoding="utf-8")
        (project / "src/avatar.ts").write_text('export const avatar = { path: "assets/robot.png", width: 32, height: 32, sampling: "nearest" };\n', encoding="utf-8")
        for source, name in (("candidate.png", "input.png"), ("reference.png", "reference.png")):
            shutil.copyfile(ROOT / "evidence/host-evaluation/fixture-inputs" / source, project / name)
    else:
        shutil.copyfile(resume / "provider-state.json", destination / "provider-state.json")
        if (resume / "uploads").exists():
            shutil.copytree(resume / "uploads", destination / "uploads")
    for source, name in (("candidate.png", "provider-negative.png"), ("reference.png", "provider-positive.png")):
        shutil.copyfile(ROOT / "evidence/host-evaluation/fixture-inputs" / source, destination / name)
    # Preserve the discovery artifact that existing request packets already bind.
    if not (project / "provider-schemas.json").exists():
        write_json(project / "provider-schemas.json", SCHEMAS)
    write_json(project / "current-provider-schemas.json", SCHEMAS)
    if not (project / "official-tool-declarations.json").exists():
        shutil.copyfile(ROOT / "evaluations/fixtures/pixellab-mcp-20261108.json", project / "official-tool-declarations.json")
    if not (project / "official-upload-declaration.json").exists():
        shutil.copyfile(ROOT / "evaluations/fixtures/pixellab-upload-20261108.json", project / "official-upload-declaration.json")
    script = destination / "pixellab_mcp_fixture.py"
    shutil.copyfile(ROOT / "evaluations/pixellab_mcp_fixture.py", script)
    return {"command": str(python), "args": [str(script), "--folder", str(destination),
            "--negative", str(destination / "provider-negative.png"),
            "--positive", str(destination / "provider-positive.png")]}
