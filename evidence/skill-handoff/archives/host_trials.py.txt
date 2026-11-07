"""Recorded native-host trials. This harness never assigns behavioral passes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import TypedDict

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "evidence" / "host-evaluation"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def inventory(root: Path, exclude: tuple[str, ...] = ()) -> dict[str, str]:
    return {
        p.relative_to(root).as_posix(): sha(p)
        for p in sorted(root.rglob("*"))
        if p.is_file() and not any(part in exclude for part in p.relative_to(root).parts)
    }


def fixtures(destination: Path) -> dict[str, object]:
    """Known local test pixels, not generated production art or an art-quality proof."""
    destination.mkdir(parents=True, exist_ok=False)
    palette = {"outline": "#25354a", "body": "#56b5bc", "eye": "#f4dda2"}
    reference = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(reference)
    d.rectangle((7, 9, 24, 27), fill=palette["outline"])
    d.rectangle((9, 11, 22, 25), fill=palette["body"])
    d.rectangle((7, 3, 10, 10), fill=palette["outline"])
    d.rectangle((21, 3, 24, 10), fill=palette["outline"])
    d.rectangle((11, 14, 13, 17), fill=palette["eye"])
    d.rectangle((18, 14, 20, 17), fill=palette["eye"])
    reference.save(destination / "reference.png")
    candidate = reference.copy()
    d = ImageDraw.Draw(candidate)
    d.rectangle((7, 3, 10, 8), fill=(0, 0, 0, 0))
    d.rectangle((18, 14, 20, 17), fill=palette["body"])
    candidate.save(destination / "candidate.png")
    alternate = reference.copy()
    pixels = alternate.load()
    assert pixels is not None
    for y in range(32):
        for x in range(32):
            if pixels[x, y] == (37, 53, 74, 255):
                pixels[x, y] = (86, 181, 188, 255)
    alternate.save(destination / "reference-b.png")
    translucent = reference.copy()
    d = ImageDraw.Draw(translucent)
    d.rectangle((6, 11, 6, 25), fill=(86, 181, 188, 96))
    d.rectangle((25, 11, 25, 25), fill=(86, 181, 188, 160))
    translucent.save(destination / "translucent-reference.png")
    return {
        "kind": "deterministic evaluator image fixtures",
        "production_art": False,
        "provider_executed": False,
        "visible_candidate_differences": [
            "Left antenna above the head is absent; right antenna remains.",
            "Right yellow eye is absent; left yellow eye remains.",
        ],
        "mechanical_match": {"size": [32, 32], "palette": list(palette.values()), "alpha": "binary"},
        "reference_conflict": "reference.png has a dark outline; reference-b.png replaces it with body color.",
        "translucent_reference_alpha_values": [0, 96, 160, 255],
        "files": inventory(destination),
    }


class TrialCase(TypedDict):
    files: list[str]
    prompt: str
    variation: str


CASES: dict[str, TrialCase] = {
    "maintainer-role": {
        "files": [],
        "prompt": "Review the packaged PIXL agent profile, skills and runtime supplied here. Identify how the agent is intended to operate and the next concrete development gap. Begin with the technical review; do not implement changes in this review session.",
        "variation": "Packaged-source review instead of the complete source checkout; implementation after review is outside this bounded trial.",
    },
    "incomplete-intake": {
        "files": ["reference.png", "reference-b.png"],
        "prompt": "Make a character family matching this project, using PIXL. The supplied references disagree about outline treatment and I have not chosen the final canvas size. The family will have a scout and a medic for a side-view game. References are reference.png and reference-b.png. Begin the project and make the progress possible in this session.",
        "variation": "Two deterministic image fixtures; no interactive answers are supplied during the first turn.",
    },
    "project-specific-style": {
        "files": ["translucent-reference.png"],
        "prompt": "Use PIXL. The reference translucent-reference.png uses intentional partial transparency and selective anti-aliasing. Keep that treatment in the new props. Review this reference and prepare a production approach for a small matching lantern prop; I have not imposed a fixed palette.",
        "variation": "Controlled local reference and planning task; no provider is connected.",
    },
    "missing-provider": {
        "files": ["reference.png"],
        "prompt": "Use PIXL to prepare a representative sprite sample using PixelLab. Brief: a 32 by 32 side-view teal scout robot matching reference.png, with two antennae, two yellow eyes, dark outlines, binary transparency, no ground shadow, and the reference palette. Deliver a PNG for nearest-neighbor display in a web prototype, with dimensions/palette checked and an actual visual comparison before family expansion. Begin work with the tools available in this session.",
        "variation": "Complete controlled brief; only the real local PIXL MCP server is configured. No remote provider observations are supplied.",
    },
    "mechanical-pass-visual-rejection": {
        "files": ["reference.png", "candidate.png"],
        "prompt": "Use PIXL to check whether candidate.png is ready to become the baseline for the rest of the robot family. The agreed identity is reference.png. The generated sample has the right 32 by 32 dimensions and reference palette. Review it and retain a useful decision and next step in this project.",
        "variation": "The user message models a production handoff; candidate bytes are a controlled evaluator fixture, not actual provider output. No seeded accepted PX2 state.",
    },
}


def freeze() -> dict[str, object]:
    destination = EVIDENCE / "package"
    if destination.exists():
        identity = json.loads((EVIDENCE / "identity.json").read_text(encoding="utf-8"))
        if inventory(destination) != identity["package_files"]:
            raise ValueError("frozen package changed")
        if inventory(REPO / "plugins" / "pixl", ("__pycache__",)) != identity["package_files"]:
            raise ValueError("source package changed; use a new evaluation series")
        return identity
    shutil.copytree(REPO / "plugins" / "pixl", destination, ignore=shutil.ignore_patterns("__pycache__"))
    manifest = json.loads((destination / "bundle-manifest.json").read_text(encoding="utf-8"))
    for row in manifest["files"]:
        if sha(destination / row["path"]) != row["sha256"]:
            raise ValueError(f"bundle hash mismatch: {row['path']}")
    fixture_oracle = fixtures(EVIDENCE / "fixture-inputs")
    write_json(EVIDENCE / "fixture-oracle.json", fixture_oracle)
    source_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    package_files = inventory(destination)
    identity = {
        "observed_at": datetime.now(UTC).isoformat(),
        "source_revision": source_revision,
        "source_tree_dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=REPO)),
        "bundle_manifest_sha256": sha(destination / "bundle-manifest.json"),
        "package_files": package_files,
        "profile_hash": package_files["resources/agent/PROFILE.md"],
        "skill_hashes": {k: v for k, v in package_files.items() if k.startswith("skills/")},
        "runtime_hashes": {k: v for k, v in package_files.items() if k.startswith("runtime/")},
        "scenarios_hash": sha(REPO / "evaluations" / "profile-scenarios.json"),
        "fixture_oracle_sha256": sha(EVIDENCE / "fixture-oracle.json"),
    }
    write_json(EVIDENCE / "identity.json", identity)
    return identity


def codex_command() -> list[str]:
    launcher = shutil.which("codex.cmd")
    if not launcher:
        raise FileNotFoundError("codex.cmd is not on PATH")
    script = Path(launcher).parent / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
    node = shutil.which("node")
    if not node or not script.is_file():
        raise FileNotFoundError("native Codex Node launcher is unavailable")
    return [node, str(script)]


def outcome(returncode: int | None, timed_out: bool, stdout: str) -> str:
    if timed_out:
        return "interrupted_timeout"
    events = []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
            if isinstance(event, dict):
                events.append(event)
        except json.JSONDecodeError:
            continue
    if returncode != 0 or any(e.get("is_error") or e.get("type") == "turn.failed" for e in events):
        return "host_error"
    if any(e.get("type") in ("turn.completed", "result") for e in events):
        return "host_completed_ungraded"
    return "incomplete_no_completion_event"


def verify_run(target: Path) -> list[str]:
    """Check retained bytes; successful integrity says nothing about model behavior."""
    record = json.loads((target / "record.json").read_text(encoding="utf-8"))
    errors = []
    for name, expected in record["evidence_hashes"].items():
        path = (target / name).resolve()
        if not path.is_relative_to(target.resolve()):
            errors.append(f"outside attempt: {name}")
        elif not path.is_file() or sha(path) != expected:
            errors.append(f"changed or absent evidence: {name}")
    for name, expected in record["artifacts"].items():
        path = (target / "project" / name).resolve()
        if not path.is_relative_to((target / "project").resolve()):
            errors.append(f"outside project: {name}")
        elif not path.is_file() or sha(path) != expected:
            errors.append(f"changed or absent artifact: {name}")
    return errors


def copy_inputs(project: Path, fixture_root: Path, names: list[str], predecessor: Path | None = None) -> dict[str, object] | None:
    if predecessor is None:
        for name in names:
            shutil.copy2(fixture_root / name, project / name)
        return None
    errors = verify_run(predecessor)
    record_path = predecessor / "record.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    if errors or inventory(predecessor / "project") != record["artifacts"]:
        raise ValueError("cold predecessor evidence changed or has unrecorded inputs")
    shutil.copytree(predecessor / "project", project, dirs_exist_ok=True)
    return {"attempt": predecessor.name, "record_sha256": sha(record_path), "artifact_hashes": record["artifacts"]}


def run(host: str, case: str, attempt: str, model: str | None, timeout: int, resume: str | None = None,
        sandbox: str = "workspace-write", retain_session: bool = False) -> Path:
    identity = freeze()
    target = EVIDENCE / "runs" / attempt
    target.mkdir(parents=True, exist_ok=False)
    runner_hash = sha(Path(__file__))
    archive = EVIDENCE / "runner-versions" / (runner_hash + ".py")
    archive.parent.mkdir(parents=True, exist_ok=True)
    if not archive.exists():
        archive.write_bytes(Path(__file__).read_bytes())
    project = Path(tempfile.mkdtemp(prefix="pixl-host-trial-"))
    # Keep the entire package layout under a native recursive skill-discovery root.
    package = project / ".agents" / "skills" / "pixl-kit"
    shutil.copytree(EVIDENCE / "package", package)
    scenario = CASES[case]
    predecessor = copy_inputs(project, EVIDENCE / "fixture-inputs", [str(name) for name in scenario["files"]],
                              EVIDENCE / "runs" / resume if resume else None)
    python = REPO / ".venv" / "Scripts" / "python.exe"
    runner = package / "scripts" / "pixl.py"
    setup = (
        "This is an isolated PIXL evaluation project. Work only in this project. "
        "The packaged PIXL skill and runtime are available under .agents/skills/pixl-kit. "
        f"The selected Python interpreter is {python.as_posix()}. "
        "Local PIXL tools are supplied by the session MCP configuration. "
        "Input images are in the project root. Do not install packages or change host settings.\n"
    )
    (project / "SESSION.md").write_text(setup, encoding="utf-8")
    prompt = str(scenario["prompt"])
    if resume:
        prompt = "Use PIXL to continue this character-family project from its saved files. Report the current decisions, unresolved dependencies and next useful action."
    prompt += "\n\n" + setup
    (target / "prompt.txt").write_text(prompt, encoding="utf-8")
    write_json(target / "inputs.json", inventory(project, ("pixl-kit",)))
    shutil.copytree(project, target / "input-project", ignore=shutil.ignore_patterns("pixl-kit"))
    server = {"command": str(python), "args": ["-I", str(runner), "mcp", "--root", str(project)]}
    if host == "codex":
        controls = json.loads((EVIDENCE / "discovery" / "codex-session-overrides.json").read_text(encoding="utf-8"))
        controls = [value for value in controls if not value.startswith(("mcp_servers.", "plugins.", "model=", "features.codex_hooks=", "features.memory_tool="))]
        command = codex_command() + [
            "exec", "--ignore-user-config", "--ignore-rules", "--json",
            "--skip-git-repo-check", "--sandbox", sandbox, "-C", str(project),
            "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "web_search=\"disabled\"",
            "-c", "model_reasoning_effort=\"xhigh\"",
            "-c", "mcp_servers.pixl_local.command=" + json.dumps(server["command"]),
            "-c", "mcp_servers.pixl_local.args=" + json.dumps(server["args"]),
        ]
        for value in controls:
            command += ["-c", value]
        if not retain_session:
            command += ["--ephemeral"]
        if model:
            command += ["--model", model]
        command += ["-"]
        version_command = codex_command() + ["--version"]
    else:
        config = target / "claude-mcp.json"
        write_json(config, {"mcpServers": {"pixl-local": {"type": "stdio", **server}}})
        command = [
            shutil.which("claude") or "claude", "--print", "--verbose", "--output-format", "stream-json",
            "--no-session-persistence", "--setting-sources", "", "--strict-mcp-config",
            "--mcp-config", str(config), "--plugin-dir", str(package),
            "--permission-mode", "acceptEdits", "--permission-prompts", "none",
            "--tools", "Read,Write,Edit,Bash,Glob,Grep,Skill",
            "--allowedTools", "Read,Write,Edit,Bash,Skill,mcp__pixl-local__*",
        ]
        if model:
            command += ["--model", model]
        version_command = [command[0], "--version"]
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    version = subprocess.check_output(version_command, text=True, env=env).strip()
    record: dict[str, object] = {
        "attempt": attempt, "case_id": case, "host": host, "host_and_version": version,
        "requested_model": model, "observed_model": None,
        "observed_at": datetime.now(UTC).isoformat(),
        "source_revision": identity["source_revision"], "profile_hash": identity["profile_hash"],
        "skill_hashes": identity["skill_hashes"], "runtime_hashes": identity["runtime_hashes"],
        "runtime_hash": hashlib.sha256(json.dumps(identity["runtime_hashes"], sort_keys=True).encode("utf-8")).hexdigest(),
        "bundle_manifest_sha256": identity["bundle_manifest_sha256"],
        "runner_sha256": runner_hash, "command": command, "cwd": str(project),
        "case_variation": "Cold intake continuation using only predecessor files plus the recorded new prompt/session paths; not the contract-change or uncertain-submission case." if resume else scenario["variation"],
        "phase": "cold_resume" if resume else "fresh", "cold_predecessor": predecessor,
        "timeout_seconds": timeout,
        "shell_sandbox": sandbox if host == "codex" else "host_acceptEdits",
        "retain_native_session": retain_session,
        "limitations": ["Controlled evaluator inputs, no live PixelLab or engine.", "Behavior requires a separate criterion review."],
    }
    write_json(target / "launch.json", record)
    started = time.monotonic()
    timed_out = False
    with (target / "stdout.jsonl").open("wb") as stdout, (target / "stderr.txt").open("wb") as stderr:
        child = subprocess.Popen(command, cwd=project, env=env, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                 creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        try:
            child.communicate(prompt.encode("utf-8"), timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(child.pid), "/T", "/F"], capture_output=True, check=False)
            else:
                child.kill()
            child.wait(timeout=30)
    output = (target / "stdout.jsonl").read_text(encoding="utf-8", errors="replace")
    for line in output.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if event.get("type") == "thread.started":
            record["thread_id"] = event.get("thread_id")
        if event.get("type") == "system" and event.get("subtype") == "init":
            record["host_reported_model"] = event.get("model")
        if event.get("type") == "assistant" and event.get("message", {}).get("model") not in (None, "<synthetic>"):
            record["observed_model"] = event["message"]["model"]
    record.update({"returncode": child.returncode, "elapsed_seconds": round(time.monotonic() - started, 3),
                   "execution_status": outcome(child.returncode, timed_out, output)})
    if retain_session and host == "codex" and record.get("thread_id"):
        host_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
        # Read only the newly created trial's own journal; never copy auth/config or unrelated sessions.
        matches = list((host_root / "sessions").rglob("*" + str(record["thread_id"]) + "*"))
        journals = [p for p in matches if p.is_file() and p.suffix == ".jsonl"]
        record["native_journal_found"] = bool(journals)
        for index, journal in enumerate(journals):
            retained = target / f"native-session-{index}.jsonl"
            shutil.copy2(journal, retained)
            for line in retained.read_text(encoding="utf-8").splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    record["native_journal_has_malformed_events"] = True
                    continue
                if not isinstance(event, dict):
                    record["native_journal_has_malformed_events"] = True
                    continue
                if event.get("type") == "turn_context":
                    record["host_reported_model"] = event.get("payload", {}).get("model")
    if inventory(package, ("__pycache__",)) != identity["package_files"]:
        record["package_mutated"] = True
        shutil.copytree(package, target / "mutated-package", ignore=shutil.ignore_patterns("__pycache__"))
        record["mutated_package_files"] = inventory(target / "mutated-package")
    else:
        record["package_mutated"] = False
    shutil.copytree(project, target / "project", ignore=shutil.ignore_patterns("pixl-kit", "__pycache__"))
    record["artifacts"] = inventory(target / "project")
    record["evidence_hashes"] = inventory(target, ("record.json",))
    write_json(target / "record.json", record)
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=("claude", "codex"))
    parser.add_argument("--case", choices=tuple(CASES), default="missing-provider")
    parser.add_argument("--attempt")
    parser.add_argument("--model")
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--cold-from")
    parser.add_argument("--sandbox", choices=("read-only", "workspace-write", "danger-full-access"), default="workspace-write")
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--retain-host-session", action="store_true", help="Retain this Codex trial's own native journal to capture tool observations omitted by exec JSON.")
    args = parser.parse_args()
    if args.verify:
        errors = verify_run(args.verify)
        print(json.dumps({"integrity_errors": errors}, indent=2))
        raise SystemExit(bool(errors))
    if args.host:
        if not args.attempt or Path(args.attempt).name != args.attempt or args.attempt in (".", ".."):
            parser.error("--attempt must be a fresh single directory name")
        if args.cold_from and (Path(args.cold_from).name != args.cold_from or args.cold_from in (".", "..")):
            parser.error("--cold-from must name a retained attempt directory")
        print(run(args.host, args.case, args.attempt, args.model, args.timeout, args.cold_from, args.sandbox, args.retain_host_session))
    else:
        print(json.dumps(freeze(), indent=2))


if __name__ == "__main__":
    main()
