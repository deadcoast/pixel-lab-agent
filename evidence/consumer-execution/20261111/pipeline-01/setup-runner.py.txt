"""Prepare and record tiny fresh-consumer readiness trials in either native host."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
import tomllib
import uuid
from pathlib import Path

from evaluations.host_trials import codex_command, inventory, sha, write_json
from evaluations.native_trial_records import reference
from evaluations.request_review_trials import ROOT, run
from pixl.readiness import verify_manifest

WORK = "work/readiness"
KIT = "installed pixl"
SETUPS = ("clean", "missing-registration")
DEFAULT_PYTHON = ROOT / "build/readiness-setup-01/runtime/Scripts/python.exe"


def prepare(destination: Path, host: str, setup: str, python: Path,
            *, consumer: Path | None = None, package: Path | None = None) -> Path:
    """Prepare only; no native host sampling, provider call or user configuration edit."""
    if host not in ("codex", "claude") or setup not in SETUPS:
        raise ValueError("Choose codex/claude and clean/missing-registration")
    destination, python = destination.resolve(), python.resolve()
    package = (package or ROOT / "plugins/pixl").resolve()
    if destination.exists():
        raise ValueError("Use a fresh attempt directory")
    if not python.is_file():
        raise ValueError("Selected runtime Python does not exist")
    if verify_manifest(package)["status"] != "verified":
        raise ValueError("Freeze a complete verified plugin before preparation")
    if consumer is None:
        consumer = Path(tempfile.mkdtemp(prefix=f"pixl readiness {host} {setup} ")) / "consumer"
    consumer = consumer.resolve()
    if consumer.exists() or consumer.is_relative_to(ROOT) or ROOT.is_relative_to(consumer):
        raise ValueError("Use a fresh consumer outside repository ancestry")
    if destination.is_relative_to(consumer) or consumer.is_relative_to(destination):
        raise ValueError("Keep attempt evidence outside the consumer")
    consumer.mkdir(parents=True)
    destination.mkdir(parents=True)
    kit = consumer / KIT
    shutil.copytree(package, kit, ignore=shutil.ignore_patterns("__pycache__"))
    (consumer / WORK).mkdir(parents=True)
    marker = uuid.uuid4().hex
    brief = ("# Fresh consumer readiness probe\n"
             f"Consumer identity: {marker}.\n"
             "Read this source and the installed library; no art or provider operation is assigned.\n")
    (consumer / "BRIEF.md").write_text(brief, encoding="utf-8")
    configuration = {"package": str(kit / "bundle-manifest.json")}
    template = kit / "config/codex-agent.example.toml"
    role = consumer / ".codex/agents/pixl.toml"
    if host == "codex":
        for name in ("pixl", "plar"):
            wrapper = consumer / f".agents/skills/{name}/SKILL.md"
            wrapper.parent.mkdir(parents=True, exist_ok=True)
            wrapper.write_text(f"---\nname: {name}\ndescription: Load the installed {name.upper()} workflow.\n---\n\n"
                               f"Read `{(kit / 'skills' / name / 'SKILL.md').as_posix()}` and resolve its links from that file.\n",
                               encoding="utf-8")
            configuration[name + "_wrapper"] = str(wrapper)
        if setup == "clean":
            role.parent.mkdir(parents=True)
            text = template.read_text(encoding="utf-8").replace("/ABSOLUTE/PLUGIN/pixl", kit.as_posix())
            tomllib.loads(text)
            role.write_text(text, encoding="utf-8")
            configuration["codex_role"] = str(role)
    native = codex_command() if host == "codex" else [shutil.which("claude") or "claude"]
    host_version = subprocess.check_output(native + ["--version"], text=True).strip()
    runtime = subprocess.check_output([str(python), "-B", "-I", "-c",
        "import json,sys;from importlib.metadata import distributions;print(json.dumps({'executable':sys.executable,'version':sys.version.split()[0],'packages':sorted(d.metadata['Name'].lower() for d in distributions())}))"],
        text=True, cwd=consumer)
    write_json(destination / "runtime-environment.json", json.loads(runtime))
    target = "pixl" if host == "codex" else "pixl:pixl"
    guidance = f"""This is the explicit NF-03/QOL-06 fresh-consumer readiness evaluation.
Follow READINESS-ASSIGNMENT.md. Consumer root: {consumer.as_posix()}.
Complete installed kit: {kit.as_posix()}. Selected runtime Python: {python.as_posix()}.
Read the common readiness reference when useful. Keep original files unchanged;
new outputs belong only under {WORK}. Do not install packages, generate art, submit
provider work, edit global settings or persistent memory, or inspect credentials.
The evaluator configured only local PIXL MCP for this invocation. This describes
the isolated invocation, not the user's other sessions or provider account.
No artwork, production state, renderer or engine acceptance is assigned.
"""
    assignment = f"""# Observe actual fresh-consumer readiness

You are the calling agent in {host}; observed executable version is {host_version}.
Assess the actual available native specialist, installation, root, local runtime
and official-tool visibility. Do not treat files or supplied assertions as proof
of host loading, tool execution, authentication or successful production.

Inspect available native delegation declarations. If the configured `{target}`
specialist is actually selectable, invoke that exact role with this consumer root,
kit and assignment (Codex: agent_type="pixl", fork_turns="none"). Ask it to read
the actual common skill/profile and BRIEF.md, perform the read-only runtime checks
below, and return {WORK}/SPECIALIST-RESULT.json with their exact identities and
its useful readiness findings. Wait for completion and retain its actual child ID.
If that role is not available or cannot be observed, record the precise evidence
and distinguish unavailable from not_observed. Do not invent a specialist, use a
generic replacement, or change registration. A role may be exposed by a route
other than the evaluator's intended route; report what you actually observe.

Whether a specialist is available or not, obtain these actual local MCP results:
- pixl_source: BRIEF.md, exact SHA-256 {sha(consumer / 'BRIEF.md')}, lines1-3,
  scope project. Retain the full result under {WORK}/source.json.
- pixl_sources: inspect the installed source inventory; retain the full result
  under {WORK}/library.json. This is local library retrieval, not remote research.
- pixl_readiness: host={host}, installation={json.dumps(kit.as_posix())}, with
  observations derived from this session's actual declarations/results. Retain
  the full result under {WORK}/readiness.json. Use the tool's actual schema and
  result_path when available; do not forge returned data. Write the exact supplied
  observations to {WORK}/observations.json. Read the installed readiness reference
  for its schema. Its numeric host_version excludes product-name text. Inventory
  completeness must be justified; a subset of observed tools is not a complete list.
  Do not call a remote tool to probe availability or authentication. The local
  capabilities catalog is dated documentation, not current official tool discovery.

Independently compare returned source text/hash and root with the actual BRIEF.md,
and readiness installation identities with the copied kit. For a real specialist,
read its result and compare it rather than accepting its self-description as proof.
Write {WORK}/CALLER-RESULT.json with host, status, root, target_role,
role_observation (available/unavailable/not_observed), native_child (actual ID or
null), observations_file, readiness, source, library, specialist_result (or null),
role_evidence, checks, limitations and next_action. File references use
{{"path":"consumer-relative/path","sha256":"actual hash"}}. This report may
honestly complete while describing incomplete setup. Separate file presence,
advertised role/tools, actual role invocation, returned runtime observations and
provider authentication. No broad production-readiness or host-reliability pass.
"""
    for name in ("AGENTS.md", "SESSION.md"):
        (consumer / name).write_text(guidance, encoding="utf-8")
    (consumer / "READINESS-ASSIGNMENT.md").write_text(assignment, encoding="utf-8")
    (destination / "prompt.txt").write_text(guidance + "\nComplete READINESS-ASSIGNMENT.md.\n", encoding="utf-8")
    server = {"command": str(python), "args": ["-B", str(kit / "scripts/pixl.py"), "mcp", "--root", str(consumer)]}
    if host == "codex":
        command = native + ["exec", "--ignore-user-config", "--ignore-rules", "--json", "--skip-git-repo-check",
            "--sandbox", "danger-full-access", "-C", str(consumer), "-c", 'approval_policy="never"',
            "-c", "agents.enabled=true", "-c", "agents.max_concurrent_threads_per_session=1",
            "-c", "features.apps=false", "-c", "features.plugins=false", "-c", "features.memories=false",
            "-c", 'web_search="disabled"']
        if setup == "clean":
            command += ["-c", "agents.pixl.config_file=" + json.dumps(role.as_posix())]
        for key, value in server.items():
            command += ["-c", f"mcp_servers.pixl_local.{key}=" + json.dumps(value)]
        command.append("-")
    else:
        write_json(destination / "mcp.json", {"mcpServers": {"pixl-local": {"type": "stdio", **server}}})
        command = native + ["--print", "--verbose", "--output-format", "stream-json", "--forward-subagent-text",
            "--session-id", str(uuid.uuid4()), "--setting-sources", "", "--strict-mcp-config",
            "--mcp-config", str(destination / "mcp.json"), "--permission-mode", "acceptEdits", "--permission-prompts", "none",
            "--tools", "Read,Write,Bash,Glob,Grep,Skill,Agent,SendMessage,TaskOutput",
            "--allowedTools", "Read,Write,Bash,Glob,Grep,Skill,Agent,SendMessage,TaskOutput,mcp__pixl-local__*"]
        if setup == "clean":
            command += ["--plugin-dir", str(kit)]
            configuration["claude_plugin_agent"] = str(kit / "agents/pixl.md")
    write_json(destination / "launch.json", {"host": host, "case": "readiness-" + setup, "setup": setup,
        "cwd": str(consumer), "command": command, "host_version": host_version,
        "continuation_mode": "new_session", "artifact_roots": [WORK], "configuration_files": configuration})
    write_json(destination / "identity.json", {"host": host, "setup": setup, "consumer": str(consumer),
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "package": reference(kit / "bundle-manifest.json"), "package_files": inventory(kit),
        "inputs": inventory(consumer), "brief": reference(consumer / "BRIEF.md"),
        "template": reference(template), "configured_role": reference(role) if role.is_file() else None,
        "runtime_environment": reference(destination / "runtime-environment.json"),
        "runner": reference(Path(__file__)),
        "isolation": {"outside_repository_ancestry": True, "official_provider_configured": False,
                      "intended_role_loading": "explicit_codex_template" if host == "codex" and setup == "clean"
                      else "claude_plugin" if setup == "clean" else "omitted",
                      "absence_limit": "No claim about other user/session configuration; report actual host observations."}})
    shutil.copyfile(__file__, destination / "runner.py.txt")
    return consumer


def retain(destination: Path) -> None:
    """Retain small results plus a complete unchanged-input/delta inventory."""
    launch, identity = (json.loads((destination / name).read_bytes()) for name in ("launch.json", "identity.json"))
    consumer = Path(launch["cwd"])
    output = consumer / WORK
    if output.exists():
        shutil.copytree(output, destination / "outputs")
    current = inventory(consumer, ("__pycache__",))
    write_json(destination / "preservation.json", {
        "inputs": len(identity["inputs"]),
        "changed": [p for p, digest in identity["inputs"].items() if current.get(p) != digest],
        "new": {p: digest for p, digest in current.items() if p not in identity["inputs"]},
        "scope": "Report additions are allowed; missing or changed prior inputs are independently graded."})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("destination", type=Path)
    prep.add_argument("--host", choices=("codex", "claude"), required=True)
    prep.add_argument("--setup", choices=SETUPS, required=True)
    prep.add_argument("--python", type=Path, default=DEFAULT_PYTHON)
    prep.add_argument("--consumer", type=Path)
    prep.add_argument("--package", type=Path)
    execute = sub.add_parser("run")
    execute.add_argument("destination", type=Path)
    execute.add_argument("--timeout", type=float, default=600)
    args = parser.parse_args()
    if args.action == "prepare":
        consumer = prepare(args.destination, args.host, args.setup, args.python, consumer=args.consumer, package=args.package)
        print(json.dumps({"attempt": str(args.destination.resolve()), "consumer": str(consumer), "launched": False}))
    else:
        run(args.destination.resolve(), timeout=args.timeout)
        retain(args.destination.resolve())


if __name__ == "__main__":
    main()
