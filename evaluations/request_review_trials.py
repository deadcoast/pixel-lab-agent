"""Native caller/specialist request-review trials; remote production is a separate phase."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import uuid
import zipfile
from pathlib import Path

from evaluations.host_trials import codex_command, inventory, outcome, sha, write_json

ROOT = Path(__file__).resolve().parents[1]
GUIDANCE = """This is an isolated native agent-to-agent planning evaluation.
Work only inside this consumer project. Use the packaged PIXL skill at
.agents/skills/pixl-kit/skills/pixl/SKILL.md and its delegation/request-review operation.
Keep production scope from OWNER.md. Planning is the requested deliverable in this
evaluation; no remote generation, credentials, package installs or host setting changes.
Local PIXL MCP tools are available for source retrieval and file/image measurements.
The caller owns the independent caller-review; the specialist must not impersonate it.
Return actual files and exact byte hashes, not claims that a self-audit passed.
"""
PROMPT = """You are the calling agent for the asset assignment in OWNER.md. Read the
consumer context and delegate contract preparation to one native PIXL specialist.
Use the installed skill's request-and-criteria handoff. Independently inspect the
returned sources, request and criteria against the original assignment, retain your
caller-review, and resolve any discrepancies with the specialist before adopting the
contract. Keep earlier proposals and revisions available. End with PARENT-RESULT.json
linking the final packet and your own review, the actual scope completed and remaining
work. This assignment ends with a reviewable planned contract; no provider dispatch.
"""


def seed(project: Path, case: str) -> None:
    if case == "drone":
        archives = ROOT / "evidence/artistic-authority/archives"
        manifest = json.loads((archives / "20261107-current.manifest.json").read_text())
        archive = archives / manifest["archive"]
        if sha(archive) != manifest["sha256"]:
            raise ValueError("prior proposal archive changed")
        with zipfile.ZipFile(archive) as zf:
            def original(name: str) -> bytes:
                path = "20261107-current/" + name
                data = zf.read(path)
                if hashlib.sha256(data).hexdigest() != manifest["files"][path]:
                    raise ValueError("historical input changed: " + path)
                return data
            protocol = json.loads(original("protocol.json"))
            owner = protocol["cases"]["small-separated"]["prompt"].split("\nFor this evaluation")[0]
            (project / "OWNER.md").write_text(owner + "\n\nThe retained APPROACH.md is an unadopted earlier specialist proposal. Prepare the current request/criteria contract for my calling agent.\n", encoding="utf-8")
            for name in ("small-separated.png", "old-assessment.md"):
                (project / name).write_bytes(original("fixture-inputs/" + name))
            (project / "APPROACH.md").write_bytes(original("runs/claude-drone-01/project/APPROACH.md"))
    else:
        (project / "OWNER.md").write_text("""# Save indicator assignment
Plan the pixel-art assets consumed by src/save-indicator.ts. Use a 24x16 logical
frame with an amber visual emphasis. We need an idle state and an animated saving
state. Choose a useful sample frame count and timing; I have not specified them.
The error state already uses the existing shared badge and needs no new artwork.
Detached sparkle pixels are allowed. I have not imposed a fixed palette or an
all-connected silhouette. There is no approved reference image yet. The older
design-notes.md is a prototype suggestion, not an adopted style contract.
Return an actionable request and review criteria for the calling agent, grounded
in the actual consumer. Generation and engine acceptance are later work.
""", encoding="utf-8")
        (project / "src").mkdir()
        (project / "src/save-indicator.ts").write_text("""export type SaveState = "idle" | "saving" | "error";
export const frameSize = { width: 24, height: 16 };
export type SavingSheet = { path: string; frames: number; frameMs: number };
export function saveIndicator(state: SaveState, elapsedMs: number, saving: SavingSheet) {
  if (state === "error") return { sharedBadge: "error" };
  if (state === "idle") return { path: "assets/save-idle.png", frame: 0, ...frameSize };
  return { path: saving.path, frame: Math.floor(elapsedMs / saving.frameMs) % saving.frames, ...frameSize };
}
""", encoding="utf-8")
        (project / "design-notes.md").write_text("""# Earlier prototype suggestion, unadopted
Try one static blue disk icon on a 32x32 square, all pixels connected, four exact
colors. Reuse the same still image for idle and saving. These were sketch choices;
no renderer check or owner acceptance was recorded.
""", encoding="utf-8")


def prepare(destination: Path, host: str, case: str, resume: Path | None = None, complete_local: bool = False) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    project = destination / "project"
    if resume:
        previous = json.loads((resume / "record.json").read_text())
        for name, digest in previous["artifacts"].items():
            if sha(resume / "project" / name) != digest:
                raise ValueError("predecessor artifact changed: " + name)
        shutil.copytree(resume / "project", project, ignore=shutil.ignore_patterns("pixl-kit", "__pycache__"))
    else:
        project.mkdir()
        if case not in ("mcp-edit", "plar-start", "plar-resume", "plar-delivery", "plar-handoff", "plar-package", "plar-authoring"):
            seed(project, case)
    package = project / ".agents/skills/pixl-kit"
    package_source = (ROOT / "evidence/pixellab-family-production/20261108/kit"
                      if case == "plar-package" else ROOT / "plugins/pixl")
    shutil.copytree(package_source, package, ignore=shutil.ignore_patterns("__pycache__"))
    manifest = json.loads((package / "bundle-manifest.json").read_text())
    for row in manifest["files"] + manifest.get("generated_files", []):
        if sha(package / row["path"]) != row["sha256"]:
            raise ValueError("bundle changed: " + row["path"])
    python = ROOT / ".venv/Scripts/python.exe"
    extra_server = None
    guidance, prompt = GUIDANCE, PROMPT
    if case == "plar-authoring-review":
        from evaluations import plar_authoring_review_case
        extra_server = plar_authoring_review_case.setup(project, destination, python, resume)
        guidance, prompt = plar_authoring_review_case.GUIDANCE, plar_authoring_review_case.PROMPT
    elif case == "plar-authoring":
        from evaluations import plar_authoring_case
        extra_server = plar_authoring_case.setup(project, destination, python, resume)
        guidance, prompt = plar_authoring_case.GUIDANCE, plar_authoring_case.PROMPT
    elif case == "plar-package":
        from evaluations import plar_package_case
        extra_server = plar_package_case.setup(project, destination, python, resume)
        guidance, prompt = plar_package_case.GUIDANCE, plar_package_case.PROMPT
    elif case == "mcp-edit":
        from evaluations import mcp_asset_case
        extra_server = mcp_asset_case.setup(project, destination, python, resume)
        guidance, prompt = mcp_asset_case.GUIDANCE, mcp_asset_case.PROMPT
    elif case == "plar-start":
        from evaluations import plar_asset_case
        extra_server = plar_asset_case.setup(project, destination, python, resume)
        guidance, prompt = plar_asset_case.GUIDANCE, plar_asset_case.PROMPT
    elif case == "plar-resume":
        from evaluations import plar_resume_case
        extra_server = plar_resume_case.setup(project, destination, python, resume)
        guidance, prompt = plar_resume_case.GUIDANCE, plar_resume_case.PROMPT
    elif case == "plar-delivery":
        from evaluations import plar_delivery_case
        extra_server = plar_delivery_case.setup(project, destination, python, resume)
        guidance, prompt = plar_delivery_case.GUIDANCE, plar_delivery_case.PROMPT
    elif case == "plar-handoff":
        from evaluations import plar_handoff_case
        extra_server = plar_handoff_case.setup(project, destination, python, resume)
        guidance, prompt = plar_handoff_case.GUIDANCE, plar_handoff_case.PROMPT
    elif case == "plar-family":
        from evaluations import plar_family_case
        extra_server = plar_family_case.setup(project, destination, python, resume)
        guidance, prompt = plar_family_case.GUIDANCE, plar_family_case.PROMPT
    elif case == "plar-render-recheck":
        from evaluations import plar_render_recheck_case
        extra_server = plar_render_recheck_case.setup(project, destination, python, resume)
        guidance, prompt = plar_render_recheck_case.GUIDANCE, plar_render_recheck_case.PROMPT
    if resume and case not in ("plar-resume", "plar-delivery", "plar-handoff", "plar-family", "plar-render-recheck", "plar-authoring-review"):
        prompt = ("You are the calling agent resuming the saved consumer project. Delegate a cold status/recovery check to PIXL. "
                  "Inspect its saved contracts, jobs, candidate reviews and delivered file. Recover the next action without repeating "
                  "completed submissions. Save COLD-RESULT.json with actual observed state and evidence. "
                  "No new generation is assigned in this resumption check.\n")
    if complete_local:
        if resume is None:
            raise ValueError("Local completion requires an existing attempt")
        prompt = ("You are the calling agent resuming the delivery assigned in OWNER.md. Delegate to PIXL, "
                  "inspect its retained contracts, jobs, reviews and delivered file, and finish any outstanding "
                  "local integration, candidate selection or task completion supported by those saved reviews. "
                  "Preserve earlier results and unresolved limitations. No new generation is assigned. "
                  "Independently verify the completed local outcome and save COLD-RESULT.json with evidence.\n")
    guidance += "\nSelected Python: " + python.as_posix() + "\n"
    (project / "SESSION.md").write_text(guidance, encoding="utf-8")
    (project / "AGENTS.md").write_text(guidance, encoding="utf-8")
    (destination / "prompt.txt").write_text(prompt + "\n" + guidance, encoding="utf-8")
    local = {"command": str(python), "args": [str(package / "scripts/pixl.py"), "mcp", "--root", str(project)]}
    if case == "plar-authoring":
        local = plar_authoring_case.local_server(project, destination, python, package)
    specialist = "You are PIXL for the assigned asset task. " + guidance
    if host == "claude":
        servers = {"pixl-local": {"type": "stdio", **local}}
        if extra_server:
            servers["pixellab-test"] = {"type": "stdio", **extra_server}
        write_json(destination / "mcp.json", {"mcpServers": servers})
        write_json(destination / "agents.json", {"pixl": {"description": "Visual asset specialist for the assigned contract.", "prompt": specialist}})
        command = [shutil.which("claude") or "claude", "--print", "--verbose",
                   "--output-format", "stream-json", "--forward-subagent-text",
                   "--session-id", str(uuid.uuid4()), "--setting-sources", "", "--strict-mcp-config",
                   "--mcp-config", str(destination / "mcp.json"), "--agents", str(destination / "agents.json"),
                   "--plugin-dir", str(package), "--permission-mode", "acceptEdits",
                   "--permission-prompts", "none", "--tools", "Read,Write,Edit,Bash,Glob,Grep,Skill,Agent,SendMessage",
                   "--allowedTools", "Read,Write,Edit,Bash,Glob,Grep,Skill,Agent,SendMessage,mcp__pixl-local__*,mcp__pixellab-test__*"]
        version_command = [command[0], "--version"]
    else:
        agents = project / ".codex/agents"
        agents.mkdir(parents=True, exist_ok=True)
        (agents / "pixl.toml").write_text('name = "pixl"\ndescription = "PixelLab visual asset specialist."\ndeveloper_instructions = ' + json.dumps(specialist) + "\n", encoding="utf-8")
        command = codex_command() + ["exec", "--ignore-user-config", "--ignore-rules", "--json",
                   "--skip-git-repo-check", "--approve-for-me", "-C", str(project),
                   "-c", "agents.enabled=true", "-c", "agents.max_concurrent_threads_per_session=1",
                   "-c", "features.apps=false", "-c", "features.plugins=false", "-c", 'web_search="disabled"']
        servers = {"pixl_local": local}
        if extra_server:
            servers["pixellab_test"] = extra_server
        for name, server in servers.items():
            for key, value in server.items():
                command += ["-c", "mcp_servers." + name + "." + key + "=" + json.dumps(value)]
        command += ["-"]
        version_command = codex_command() + ["--version"]
    write_json(destination / "launch.json", {"host": host, "case": case, "cwd": str(project), "command": command,
                "host_version": subprocess.check_output(version_command, text=True).strip()})
    write_json(destination / "identity.json", {"source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "runner_sha256": sha(Path(__file__)), "package_files": inventory(package),
                "inputs": inventory(project, ("pixl-kit",)), "prompt_sha256": sha(destination / "prompt.txt"),
                "predecessor": str(resume) if resume else None,
                "scope": ("Cold consumption of retained real-provider production; no new provider work assigned."
                          if case == "plar-package" else "Targeted native repair of retained connected-plan criterion comparison; original partial result preserved."
                          if case == "plar-authoring-review" else "Native connected authoring/preparation with explicit allocation interruption and caller requirement change; original production preserved."
                          if case == "plar-authoring" else "Native delegation/contract review and, for provider cases, controlled provider execution; no upstream service.")})
    shutil.copyfile(Path(__file__), destination / "runner.py.txt")
    shutil.copytree(project, destination / "input-project", ignore=shutil.ignore_patterns("pixl-kit"))


def retain_journals(destination: Path, events: list[dict]) -> None:
    ids = {e["thread_id"] for e in events if e.get("type") == "thread.started"}
    found: set[str] = set()
    host_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "sessions"
    while ids - found:
        ident = (ids - found).pop()
        found.add(ident)
        for journal in host_root.rglob("*" + ident + "*.jsonl"):
            copy = destination / ("native-" + ident + ".jsonl")
            if not copy.exists():
                shutil.copyfile(journal, copy)
            for line in copy.read_text(encoding="utf-8").splitlines():
                event = json.loads(line)
                payload = event.get("payload", {})
                activity = payload.get("item", {})
                if activity.get("type") == "SubAgentActivity" and isinstance(activity.get("agent_thread_id"), str):
                    ids.add(activity["agent_thread_id"])
                if payload.get("type") == "function_call_output":
                    try:
                        result = json.loads(payload.get("output", "{}"))
                    except (ValueError, TypeError):
                        continue
                    if isinstance(result, dict) and isinstance(result.get("agent_id"), str) and re.fullmatch(r"[0-9a-f-]{36}", result["agent_id"]):
                        ids.add(result["agent_id"])


def run(destination: Path, *, timeout: float | None = None) -> None:
    from evaluations.native_trial_records import atomic_json, codex_journals, execute

    launch = json.loads((destination / "launch.json").read_text())
    if (destination / "stdout.jsonl").exists():
        raise ValueError("Use a fresh attempt")
    env = dict(os.environ)
    for key in list(env):
        if any(word in key.upper() for word in ("PIXELLAB", "PIXEL_LAB", "ANTHROPIC_API_KEY", "OPENAI_API_KEY")):
            del env[key]
    env.pop("PYTHONPATH", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    removed_history_override = False
    if launch["host"] == "claude" and "--no-session-persistence" not in launch["command"]:
        removed_history_override = env.pop("CLAUDE_CODE_SKIP_PROMPT_HISTORY", None) is not None
    # Local Claude sessions otherwise share repository auto-memory across fixtures.
    # Scope this documented override to the evaluation child, not user settings.
    overrides = {"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"} if launch["host"] == "claude" else {}
    env.update(overrides)
    write_json(destination / "execution-environment.json", {
        "scope": "Evaluation subprocess only; no persistent host configuration changed",
        "overrides": overrides,
        "removed_history_override": removed_history_override,
        "limit": "Disables the documented automatic-memory feature, not arbitrary filesystem access",
    })
    returncode, elapsed, events, continuation = execute(destination, launch, env, timeout)
    output = (destination / "stdout.jsonl").read_text(encoding="utf-8", errors="replace")
    if launch["host"] == "codex":
        retain_journals(destination, events)
        continuation = codex_journals(destination, continuation)
        atomic_json(destination / "continuation.json", continuation)
    write_json(destination / "record.json", {"host": launch["host"], "case": launch["case"],
        "returncode": returncode, "execution_status": outcome(returncode, continuation["interruption_reason"] == "timeout", output),
        "elapsed_seconds": elapsed, "behavioral_verdict": "ungraded",
        "continuation": {"path": "continuation.json", "sha256": sha(destination / "continuation.json"),
                         "interruption_reason": continuation["interruption_reason"]},
        "artifacts": inventory(Path(launch["cwd"]), ("pixl-kit", "__pycache__")),
        "recorded_files": inventory(destination, ("project", "input-project", "record.json"))})
    print(json.dumps({"attempt": str(destination), "returncode": returncode}))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=("claude", "codex"), required=True)
    parser.add_argument("--case", choices=("drone", "save-indicator", "mcp-edit", "plar-start", "plar-resume", "plar-delivery", "plar-handoff", "plar-family", "plar-render-recheck", "plar-package", "plar-authoring", "plar-authoring-review"), required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--complete-local", action="store_true")
    args = parser.parse_args()
    if args.complete_local and args.resume is None:
        parser.error("--complete-local requires --resume")
    destination = args.out.resolve()
    prepare(destination, args.host, args.case, args.resume.resolve() if args.resume else None, args.complete_local)
    if args.run:
        run(destination)


if __name__ == "__main__":
    main()
