"""Native use of ordinary review authoring on the retained queue successor."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from evaluations.host_trials import codex_command, inventory, sha, write_json
from evaluations.request_review_trials import run
from pixl import codec, graph, plar, store

ROOT = Path(__file__).resolve().parents[1]
PREDECESSOR = ROOT / "evidence/successor-acceptance/20261109/maintainer-01/project"
STORE = ".pixl/assets/queue.ready"
BASELINE = "f2eb516254a10adf57d60153edfc9a3365868b6e23cc1be42d93ea80079d9300"

ASSIGNMENT = """# Complete the successor through ordinary review authoring

This is an isolated native evaluation of PIXL's candidate/family review interface.
You are the caller. Delegate the asset review to the registered PIXL specialist,
then independently check its saved result. Retain the actual native child identity
and role. Do not claim a named role if the host only provides a generic child.

The project is copied from the completed queue successor. Its working state was
restored to saved revision 119, immediately before motion/family acceptance. All
old files/history remain; original production and other candidate criteria are
already reviewed. This trial evaluates using a new interface on retained actual
PixelLab-derived assets, not new generation quality or an unfamiliar assignment.

Read the new kit's resources/agent/PROFILE.md and skills/pixl/SKILL.md, then its
inspection/family-delivery references and resources/spec/candidate-review.md.
Use the local MCP or this kit's CLI. Work only inside this copied consumer.
The caller owns final independent checks; the specialist supplies artistic judgment.
Do not hand-author X/E/V records or directly edit state.px for ordinary review.

1. Read review-context for provenance-correction.working.candidate in
   .pixl/assets/queue.ready/state.px. Seven Working criteria already pass; motion
   has a retained unavailable verdict. Inspect the actual recorded exposures in
   work/acceptance-01/headless-review-03/playback.png and stationary.png, the
   observed-views/transition-* native/3x images as relevant, and the actual timing
   in playback-observation-03.json and review-checks.json. Judge the literal
   motion criterion independently, naming actual viewed/executed evidence.
2. Use candidate-review to retain that judgment, explicitly superseding the
   current unavailable V. Use existing actor "actor"; take an actual timestamp.
   Choose record/nominate/complete based on the actual result. If it passes,
   nominate and complete Working through this operation. Save the request JSON
   and result under work/native-review. On an input mistake, retain the error and
   correct it using the documented interface; do not bypass with generic commits.
3. Once ready, create a fresh family snapshot of provenance-correction.delivery.output
   with a fresh candidate ID. Inspect its exact member hashes and collective
   continuity/distinction criteria. Existing family views include grayscale and
   the unchanged Start reference. Review them, preserving differences appropriate
   to each symbol rather than inventing a shared silhouette or palette rule.
4. Run the existing isolated renderer-successor/capture.mjs against this project,
   with --out work/native-review/destination-01, and its check.py on that capture.
   It executes both actual consumers, normal/reduced motion and live preference
   switches. Review saved destination pixels. Use the exact manifest member bytes;
   verify their hashes match the assets/successor files this renderer consumes.
   Desktop control is unnecessary for this runner. Preserve any failed capture.
5. Use candidate-review on the fresh family manifest for the three actual
   collective/destination criteria. Supply per-criterion observations/reasons of
   the required modes, and complete only if justified. The immutable manifest's
   initial accepted:false remains unchanged; report current acceptance separately.
6. Repeat one successful identical review request with the current state_hash and
   show it reuses the review without new verdicts/publications. Return
   REVIEW-RESULT.json with reviewed candidate/family IDs, request/result paths,
   actual images viewed and renderer evidence, current state_hash, unresolved
   issues, and what the caller independently verified. Preserve existing source,
   artwork, requirements and historical evidence. Record this trial's scope; it
   does not establish broader quality or all host reliability.

The task is review/integration of existing assets. No replacement asset generation
is needed for this assignment; do not alter the product's normal paid PixelLab
production workflow or ask the user for a new asset/repository.
"""


def prepare(destination: Path, host: str) -> None:
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=False)
    project = destination / "project"
    shutil.copytree(PREDECESSOR, project, ignore=shutil.ignore_patterns("__pycache__", "node_modules"))
    folder = project / STORE
    original = folder / "history" / (BASELINE + ".px")
    assert codec.digest(codec.parse(original.read_bytes())) == BASELINE
    (folder / "state.px").write_bytes(original.read_bytes())
    graph.validate(store.load(folder), project)
    queue = json.loads((project / "authoring-plar.txt").read_text(encoding="utf-8"))
    for asset in queue["assets"]:
        if asset["id"] in {"queue.working", "queue.retry", "queue.paused", "queue.ready"}:
            asset["status"] = "in_progress"
            asset["next"] = "Isolated review-interface evaluation at retained pre-acceptance state; inspect current production."
    plar.save(project, queue, sha(project / "authoring-plar.txt"), "authoring-plar.txt")
    kit = project / ".agents/skills/review-kit"
    shutil.copytree(ROOT / "plugins/pixl", kit, ignore=shutil.ignore_patterns("__pycache__"))
    python = ROOT / ".venv/Scripts/python.exe"
    guidance = ("This consumer is an isolated native candidate/family review evaluation. "
                "Read REVIEW-ASSIGNMENT.md. The current kit is .agents/skills/review-kit; preserve the old pixl-kit as historical source. "
                "Use all available local execution/image tools, preserve original files, and write new work under work/native-review. "
                "No global settings or persistent memory edits. Selected Python: " + python.as_posix() + ".")
    for name in ["AGENTS.md", "SESSION.md"]:
        (project / name).write_text(guidance + "\n", encoding="utf-8")
    (project / "REVIEW-ASSIGNMENT.md").write_text(ASSIGNMENT, encoding="utf-8")
    (project / "work/native-review").mkdir()
    prompt = "Complete REVIEW-ASSIGNMENT.md through a native PIXL specialist and verify the actual saved result.\n" + guidance
    (destination / "prompt.txt").write_text(prompt, encoding="utf-8")
    specialist = "You are PIXL for this explicitly delegated production review. " + guidance
    local = {"command": str(python), "args": [str(kit / "scripts/pixl.py"), "mcp", "--root", str(project)]}
    if host == "claude":
        write_json(destination / "mcp.json", {"mcpServers": {"pixl-local": {"type": "stdio", **local}}})
        write_json(destination / "agents.json", {"pixl": {"description": "PixelLab visual asset specialist for this retained asset review.", "prompt": specialist}})
        command = [shutil.which("claude") or "claude", "--print", "--verbose", "--output-format", "stream-json",
                   "--forward-subagent-text", "--setting-sources", "", "--strict-mcp-config",
                   "--mcp-config", str(destination / "mcp.json"), "--agents", str(destination / "agents.json"),
                   "--plugin-dir", str(kit), "--permission-mode", "acceptEdits", "--permission-prompts", "none",
                   "--tools", "Read,Write,Edit,Bash,Glob,Grep,Skill,Agent,SendMessage",
                   "--allowedTools", "Read,Write,Edit,Bash,Glob,Grep,Skill,Agent,SendMessage,mcp__pixl-local__*"]
        version = subprocess.check_output([command[0], "--version"], text=True).strip()
    else:
        agent_dir = project / ".codex/agents"
        agent_dir.mkdir(parents=True, exist_ok=True)
        (agent_dir / "pixl.toml").write_text('name = "pixl"\ndescription = "PixelLab visual asset specialist."\ndeveloper_instructions = ' + json.dumps(specialist) + "\n", encoding="utf-8")
        command = codex_command() + ["exec", "--ignore-user-config", "--ignore-rules", "--json", "--skip-git-repo-check",
                   "--approve-for-me", "-C", str(project), "-c", "agents.enabled=true",
                   "-c", "agents.max_concurrent_threads_per_session=1", "-c", "features.apps=false", "-c", "features.plugins=false",
                   "-c", 'web_search="disabled"']
        for key, value in local.items():
            command += ["-c", "mcp_servers.pixl_local." + key + "=" + json.dumps(value)]
        command += ["-"]
        version = subprocess.check_output(codex_command() + ["--version"], text=True).strip()
    write_json(destination / "launch.json", {"host": host, "case": "candidate-family-review", "cwd": str(project), "command": command, "host_version": version})
    write_json(destination / "identity.json", {"predecessor": str(PREDECESSOR), "baseline_state_hash": BASELINE,
               "package_files": inventory(kit), "inputs": inventory(project, ("pixl-kit", "review-kit", "__pycache__")),
               "prompt_sha256": sha(destination / "prompt.txt"), "runner_sha256": sha(Path(__file__)),
               "scope": "Native review/nomination/completion of retained actual successor assets. No new generation; native outcome remains ungraded until checked."})
    shutil.copyfile(__file__, destination / "runner.py.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", choices=["claude", "codex"])
    parser.add_argument("destination", type=Path)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    prepare(args.destination, args.host)
    if not args.prepare_only:
        run(args.destination.resolve())
