"""Prepare isolated native caller/PIXL review without supplying evaluator findings."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path, PurePosixPath

from evaluations import skill_handoff_trials as handoff
from evaluations.host_trials import sha, write_json
from evaluations.native_trial_records import reference, validate_model
from evaluations.request_review_trials import ROOT
from evaluations.request_review_trials import run as run_native
from pixl.readiness import verify_manifest

KIT = handoff.KIT
DEFAULT_PYTHON = handoff.DEFAULT_PYTHON
ROLE = "pixl:pixl"
TOOLS = "Read,Write,Bash,Glob,Grep,Skill,Agent,SendMessage,TaskOutput"
SOURCE_FILES = (
    Path(__file__),
    ROOT / "evaluations/skill_handoff_trials.py",
    ROOT / "evaluations/host_trials.py",
    ROOT / "evaluations/request_review_trials.py",
    ROOT / "evaluations/native_trial_records.py",
    ROOT / "pixl/readiness.py",
)


def _assignment(protocol: Path, amendment: Path | None, consumer: Path, python: Path) -> str:
    """Only the preregistered assignment fields enter the model's input."""
    assignment = json.loads(protocol.read_bytes())["assignment"]
    core, setup = assignment["neutral_task_core"], assignment["setup_template"]
    if not isinstance(core, str) or not isinstance(setup, str):
        raise TypeError("Protocol assignment fields must contain text")
    prompt = core + "\n\n" + setup.format(CONSUMER_ROOT=consumer.as_posix(), PYTHON_EXE=python.as_posix())
    if amendment is not None:
        extra = json.loads(amendment.read_bytes())["assignment"]["appended_prompt_text"]
        if not isinstance(extra, str):
            raise TypeError("Protocol amendment appended_prompt_text must contain text")
        prompt += "\n\n" + extra
    return prompt + "\n"


def prepare(destination: Path, *, seed: Path, seed_manifest: Path | dict[str, str], protocol: Path,
            amendment: Path | None = None, python: Path = DEFAULT_PYTHON,
            package: Path | None = None, consumer: Path | None = None, model: str | None = None) -> Path:
    """Freeze inputs and an optional explicit model; run version/inventory probes only."""
    validate_model(model)
    destination, python, seed, protocol = (p.resolve() for p in (destination, python, seed, protocol))
    package = (package or ROOT / "plugins/pixl").resolve()
    amendment = amendment.resolve() if amendment else None
    if destination.exists():
        raise ValueError("Use a fresh attempt directory")
    if not python.is_file():
        raise ValueError("Selected runtime Python does not exist")
    if verify_manifest(package)["status"] != "verified" or not (package / "agents/pixl.md").is_file():
        raise ValueError("Freeze a complete verified plugin with its registered PIXL agent")
    if not seed.is_dir():
        raise ValueError("Seed directory does not exist")
    expected = handoff._manifest(seed_manifest)
    seed_files = handoff._files(seed)
    if not expected or seed_files != expected:
        raise ValueError("Seed files differ from the required supplied manifest")
    for name in seed_files:
        parts = PurePosixPath(name).parts
        if KIT in {part.casefold() for part in parts}:
            raise ValueError("Seed must omit the installed kit; it is frozen separately")
        if any(re.match(r"(?:caller[-_]review|semantic[-_]review|grader)(?:[-_.]|$)", part, re.IGNORECASE) for part in parts):
            raise ValueError("Seed must exclude evaluator or caller feedback")
    bindings = {"protocol": protocol}
    if amendment:
        bindings["amendment"] = amendment
    if isinstance(seed_manifest, Path):
        bindings["seed_manifest"] = seed_manifest.resolve()
    if any(path.is_relative_to(seed) for path in bindings.values()):
        raise ValueError("Keep evaluator protocol and manifests outside the project seed")
    if consumer is None:
        consumer = Path(tempfile.gettempdir()) / ("pixl caller review " + uuid.uuid4().hex) / "consumer"
    consumer = consumer.resolve()
    if consumer.exists() or consumer.is_relative_to(ROOT) or ROOT.is_relative_to(consumer):
        raise ValueError("Use a fresh consumer outside repository ancestry")
    trees = (destination, consumer, seed, package)
    if any(left.is_relative_to(right) or right.is_relative_to(left)
           for i, left in enumerate(trees) for right in trees[i + 1:]):
        raise ValueError("Keep evidence, consumer, package and seed trees separate")
    prompt = _assignment(protocol, amendment, consumer, python)
    package_files = handoff._files(package)
    binding_files = {name: reference(path) for name, path in bindings.items()}
    destination.mkdir(parents=True, exist_ok=False)
    consumer.mkdir(parents=True, exist_ok=False)
    kit = consumer / KIT
    shutil.copytree(package, kit, ignore=shutil.ignore_patterns("__pycache__"))
    if handoff._files(kit) != package_files:
        raise ValueError("Frozen package changed during preparation")
    handoff._copy(seed, consumer, seed_files)
    handoff._copy(consumer, destination / "input-project", seed_files)
    archive = handoff._archive(destination / "input-project", destination / "input-project.zip", seed_files)
    executable = shutil.which("claude") or "claude"
    host_version = subprocess.check_output([executable, "--version"], text=True).strip()
    runtime = subprocess.check_output([str(python), "-B", "-I", "-c",
        "import json,sys;from importlib.metadata import distributions;print(json.dumps({'executable':sys.executable,'version':sys.version.split()[0],'packages':sorted(d.metadata['Name'].lower() for d in distributions())}))"],
        text=True, cwd=consumer)
    write_json(destination / "runtime-environment.json", json.loads(runtime))
    (destination / "prompt.txt").write_text(prompt, encoding="utf-8")
    write_json(destination / "mcp.json", {"mcpServers": {"pixl-local": {"type": "stdio",
        "command": str(python), "args": ["-B", "-I", str(kit / "scripts/pixl.py"), "mcp", "--root", str(consumer)]}}})
    session = str(uuid.uuid4())
    command = [executable, "--print", "--verbose", "--output-format", "stream-json", "--forward-subagent-text",
        "--session-id", session, "--setting-sources", "", "--strict-mcp-config",
        "--mcp-config", str(destination / "mcp.json"), "--plugin-dir", str(kit),
        "--permission-mode", "acceptEdits", "--permission-prompts", "none",
        "--tools", TOOLS, "--allowedTools", TOOLS + ",mcp__pixl-local__*"]
    if model is not None:
        command += ["--model", model]
    write_json(destination / "launch.json", {"host": "claude", "case": "cold-caller-review",
        "cwd": str(consumer), "command": command, "host_version": host_version,
        "expected_session_id": session, "continuation_mode": "file_only_cold",
        "artifact_roots": [], "configuration_files": {"package": str(kit / "bundle-manifest.json"),
            "claude_plugin_agent": str(kit / "agents/pixl.md")}})
    source_files = []
    for source in SOURCE_FILES:
        target = destination / "runner-sources" / source.relative_to(ROOT).with_suffix(".py.txt")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        source_files.append({"source": reference(source), "snapshot": reference(target)})
    shutil.copyfile(__file__, destination / "runner.py.txt")
    write_json(destination / "identity.json", {"case": "cold-caller-review", "consumer": str(consumer),
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "package": reference(kit / "bundle-manifest.json"), "package_files": package_files,
        "registered_agent": reference(kit / "agents/pixl.md"), "target_role": ROLE,
        "inputs": seed_files, "input_archive": archive,
        "static_inputs": {name: digest for name, digest in seed_files.items()
            if handoff._static(name) or name.startswith(("sources/", "state.px/history/"))},
        "seed": {"path": str(seed), "files": seed_files, "supplied_manifest": True},
        "binding_files": binding_files,
        "launch": reference(destination / "launch.json"), "prompt": reference(destination / "prompt.txt"),
        "mcp": reference(destination / "mcp.json"), "runtime_environment": reference(destination / "runtime-environment.json"),
        "runner": reference(Path(__file__)), "source_files": source_files,
        "scope": "Fresh native caller and registered PIXL child from exact retained files; independent caller review. No evaluator findings supplied, provider execution or engine acceptance."})
    return consumer


def retain(destination: Path) -> dict:
    """Reuse full hidden-file snapshots and immutable-input/delta evidence retention."""
    return handoff.retain(destination)


def run(destination: Path, *, timeout: float | None = None) -> None:
    """Run once through the durable recorder; retain partial output even on failure."""
    destination = destination.resolve()
    launch, identity = (json.loads((destination / name).read_bytes()) for name in ("launch.json", "identity.json"))
    consumer = Path(launch["cwd"])
    if any((destination / name).exists() for name in ("stdout.jsonl", "stderr.txt", "continuation.json", "project", "preservation.json")):
        raise ValueError("Use a fresh prepared attempt; previous outcomes are retained")
    references = [identity[name] for name in ("launch", "prompt", "mcp", "runtime_environment")]
    references += list(identity["binding_files"].values())
    references += [item[key] for item in identity["source_files"] for key in ("source", "snapshot")]
    if (handoff._files(consumer, exclude_kit=True) != identity["inputs"]
            or handoff._files(destination / "input-project") != identity["inputs"]
            or handoff._files(consumer / KIT) != identity["package_files"]
            or any(reference(Path(item["path"])) != item for item in references)
            or sha(destination / "runner.py.txt") != identity["runner"]["sha256"]
            or sha(destination / "input-project.zip") != identity["input_archive"]["sha256"]):
        raise ValueError("Prepared evaluation inputs changed before execution")
    try:
        run_native(destination, timeout=timeout)
    finally:
        retain(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("destination", type=Path)
    for name in ("seed", "seed-manifest", "protocol"):
        prep.add_argument("--" + name, type=Path, required=True)
    prep.add_argument("--amendment", type=Path)
    prep.add_argument("--python", type=Path, default=DEFAULT_PYTHON)
    prep.add_argument("--package", type=Path)
    prep.add_argument("--consumer", type=Path)
    prep.add_argument("--model", help="Explicit native caller model; omission preserves the host default")
    execute = sub.add_parser("run")
    execute.add_argument("destination", type=Path)
    execute.add_argument("--timeout", type=float)
    saved = sub.add_parser("retain")
    saved.add_argument("destination", type=Path)
    args = parser.parse_args()
    if args.action == "prepare":
        consumer = prepare(args.destination, seed=args.seed, seed_manifest=args.seed_manifest,
            protocol=args.protocol, amendment=args.amendment, python=args.python, package=args.package,
            consumer=args.consumer, model=args.model)
        print(json.dumps({"attempt": str(args.destination.resolve()), "consumer": str(consumer), "launched": False}))
    elif args.action == "run":
        run(args.destination, timeout=args.timeout)
    else:
        print(json.dumps(retain(args.destination)))


if __name__ == "__main__":
    main()
