"""Recover the retained Claude comparison, then continue its persisted child."""

import argparse
import json
import shutil
import subprocess
import uuid
from pathlib import Path

from evaluations.host_trials import inventory, sha, write_json
from evaluations.native_trial_records import reference
from evaluations.request_review_trials import ROOT, run


def prepare(destination, consumer):
    destination, consumer = destination.resolve(), consumer.resolve()
    predecessor = ROOT / "evidence/focused-authoring/20261109/native/claude-01"
    record = json.loads((predecessor / "record.json").read_bytes())
    for name, digest in record["artifacts"].items():
        if sha(predecessor / "project" / name) != digest:
            raise ValueError(f"Retained consumer changed: {name}")
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copytree(predecessor / "project", consumer)
    kit = consumer / ".agents/skills/continuation-kit"
    shutil.copytree(ROOT / "plugins/pixl", kit)
    work = consumer / "work/continuation"
    work.mkdir()
    python = ROOT / ".venv/Scripts/python.exe"
    guidance = f"""This is the explicit native continuation evaluation, not a new art assignment.
Use CONTINUATION-ASSIGNMENT.md and the current kit at .agents/skills/continuation-kit.
Retain all old assignments, files and acceptance. New work belongs only under
work/continuation. Consumer root: {consumer.as_posix()}.
Selected Python: {python.as_posix()}. Do not edit global settings or memory.
PIXL is the host-model visual specialist using its shared profile/skill and actual
tools. The parent owns independent caller review. Native session persistence is
enabled; automated memory is disabled only for this evaluation subprocess.
"""
    assignment = """# Finish the retained interrupted caller comparison

The earlier focused-authoring Claude run stopped at a usage limit after its PIXL
child wrote work/focused-successor/specialist-proposal.json and specialist-report.json.
It was launched with session persistence disabled. This phase is an explicit
artifact-based restart of its unfinished comparison, not the old child resumed.
Preserve that attempt's grade and all its saved files.

The specific unfinished work here is the independent comparison of the original
20 criteria against that retained 29-criterion reduced-motion proposal. Do not
substitute the later 23-criterion package used by a different successor trial.
The broader original assignment also included production/rendering; those remain
separate and are not completed by this comparison. Do not adopt/rewrite production,
run a renderer, or create new art acceptance in this comparison assignment.

Read current shared profile and skill in .agents/skills/continuation-kit, then use
one native registered pixl child to review the retained proposal and its exact
sources. Use focused public context/request-review exports where useful. Read
large JSON programmatically and preserve literal checks, IDs and record hashes.
New files must be under work/continuation; the original proposal stays unchanged.

First ask the specialist for a concise assessment of the proposal and any concrete
source/authority defects, with exact locators and suggested corrections, in a new
SPECIALIST-ROUND1.json. Distinguish owner requirements, measured facts and scoped
expert choices. Preserve selective AA/full alpha, margins versus sheet padding,
perceptible color roles, expert pacing versus the owner's 100ms, shared-consumer
state distinction, and visual/temporal evidence obligations. Do not turn retained
unavailable viewing into a new pass. Retain the actual child ID for continuation.

Then independently compare all 20 original rows with the 29 proposed literal
criteria, using actual sources and the prior r2 corrections. Write CALLER-REVIEW-01.json:
- exact original proposal SHA-256 and original state/requirements identities;
- all 20 original IDs, record hashes, literal checks and mapped proposed IDs;
- each of the 29 proposed IDs and literal checks, supported disposition and any
  concrete authority/source concern; give corrections without rewriting originals;
- source locators and separation of mechanical, visual, temporal and destination
  evidence; limitations and remaining decisions.

Write PHASE1-CALLER.json with the native child ID, exact output paths/hashes, an
independent assessment of the specialist, and the precise follow-up for that same
child. End this phase after retaining the review. A separate invocation will
resume this same parent session and send that child the caller review to reconcile.
Do not replace this with another fresh child or claim already-tested same-child
continuation. M1 and broader host reliability remain open.
"""
    (consumer / "CONTINUATION-ASSIGNMENT.md").write_text(assignment, encoding="utf-8")
    for name in ("AGENTS.md", "SESSION.md"):
        # These are this disposable consumer's entrypoints; originals remain in the predecessor.
        (consumer / name).write_text(guidance, encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete phase 1 of CONTINUATION-ASSIGNMENT.md.\n", encoding="utf-8")
    write_json(destination / "agents.json", {"pixl": {"description": "PIXL specialist for retained criterion comparison and continuation",
               "prompt": "You are PIXL for this explicit evaluation. " + guidance}})
    write_json(destination / "mcp.json", {"mcpServers": {"pixl-local": {"type": "stdio", "command": str(python),
               "args": [str(kit / "scripts/pixl.py"), "mcp", "--root", str(consumer)]}}})
    executable = shutil.which("claude") or "claude"
    session = str(uuid.uuid4())
    command = [executable, "--print", "--verbose", "--output-format", "stream-json", "--forward-subagent-text",
               "--session-id", session, "--setting-sources", "", "--strict-mcp-config",
               "--mcp-config", str(destination / "mcp.json"), "--agents", str(destination / "agents.json"),
               "--plugin-dir", str(kit), "--permission-mode", "acceptEdits", "--permission-prompts", "none",
               "--tools", "Read,Write,Edit,Bash,Glob,Grep,Skill,Agent,SendMessage,TaskOutput",
               "--allowedTools", "Read,Write,Edit,Bash,Glob,Grep,Skill,Agent,SendMessage,TaskOutput,mcp__pixl-local__*"]
    write_json(destination / "launch.json", {"host": "claude", "case": "retained-comparison-continuation", "cwd": str(consumer),
               "command": command, "host_version": subprocess.check_output([executable, "--version"], text=True).strip(),
               "expected_session_id": session, "continuation_mode": "artifact_restart",
               "predecessor": reference(predecessor / "record.json"), "artifact_roots": ["work/continuation"]})
    write_json(destination / "identity.json", {"predecessor": reference(predecessor / "record.json"),
               "original_proposal": reference(predecessor / "project/work/focused-successor/specialist-proposal.json"),
               "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "inputs": inventory(consumer, ("pixl-kit", "continuation-kit", "__pycache__")),
               "current_package": reference(kit / "bundle-manifest.json"), "package_files": inventory(kit),
               "runner": reference(Path(__file__)), "scope": "Artifact recovery of interrupted comparison, followed by explicit same-parent same-child continuation."})
    shutil.copyfile(__file__, destination / "runner.py.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--consumer", type=Path, required=True)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    prepare(args.destination, args.consumer)
    if not args.prepare_only:
        run(args.destination.resolve())
