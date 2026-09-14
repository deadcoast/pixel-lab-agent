"""Read-only host discovery: render Codex's context without an inference turn."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
HOME = Path.home()
CODEX = Path(
    "C:/nvm4w/nodejs/node_modules/@openai/codex/node_modules/@openai/"
    "codex-win32-x64/vendor/x86_64-pc-windows-msvc/bin/codex.exe"
)


def main() -> None:
    project = Path(tempfile.mkdtemp(prefix="pixl-codex-skill-probe-"))
    bundle = project / ".agents" / "skills" / "pixl-kit"
    shutil.copytree(ROOT / "plugins" / "pixl", bundle)
    skill = bundle / "skills" / "pixl" / "SKILL.md"
    config = tomllib.loads((HOME / ".codex" / "config.toml").read_text("utf-8"))
    disabled = sorted(
        str(path).replace("\\", "/")
        for base in (HOME / ".codex" / "skills", HOME / ".agents" / "skills")
        if base.is_dir()
        for path in base.rglob("SKILL.md")
    )
    overrides = [
        'model="gpt-6-astra"',
        'model_reasoning_effort="xhigh"',
        'developer_instructions=""',
        "project_doc_max_bytes=0",
        "notify=[]",
        "skills.bundled.enabled=false",
        "skills.config=[" + ",".join(
            "{path=" + json.dumps(path) + ",enabled=false}" for path in disabled
        ) + "]",
    ]
    for name in (
        "apps", "hooks", "codex_hooks", "plugin_hooks", "plugins", "memories",
        "memory_tool", "external_migration", "multi_agent", "multi_agent_v2",
        "goals", "recommended_plugins", "remote_plugin", "skill_mcp_dependency_install",
        "skill_env_var_dependency_prompt",
    ):
        overrides.append(f"features.{name}=false")
    for name in config.get("mcp_servers", {}):
        overrides.append("mcp_servers." + name + ".enabled=false")
    for name in config.get("plugins", {}):
        overrides.append("plugins." + name + ".enabled=false")
    command = [str(CODEX), "debug", "prompt-input"]
    for item in overrides:
        command += ["-c", item]
    prompt = "$pixl:pixl Review the project references and preserve unresolved production choices."
    command.append(prompt)
    completed = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=50)
    # Preserve raw diagnostic output only in the temporary project. Retained evidence
    # stores selected skill catalog entries, hashes and sanitized process diagnostics.
    (project / "prompt-input.json").write_text(completed.stdout, encoding="utf-8")
    text = completed.stdout
    messages = json.loads(text) if completed.returncode == 0 else []
    skill_instructions = [
        content["text"] for message in messages
        for content in message.get("content", [])
        if "<skills_instructions>" in content.get("text", "")
    ]
    skill_context = "\n".join(skill_instructions)
    catalog_lines = [
        line for line in text.replace("\\n", "\n").splitlines()
        if re.match(r"^- [a-zA-Z0-9_-]+:", line) and "SKILL.md" in line
    ]
    record = {
        "purpose": "Native Codex context construction; no turn/start or model inference.",
        "host_version": subprocess.check_output([str(CODEX), "--version"], text=True).strip(),
        "project": str(project),
        "skill_path": str(skill),
        "skill_sha256": hashlib.sha256(skill.read_bytes()).hexdigest(),
        "source_skill_sha256": hashlib.sha256((ROOT / "plugins/pixl/skills/pixl/SKILL.md").read_bytes()).hexdigest(),
        "exit_code": completed.returncode,
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "stdout_bytes": len(completed.stdout.encode()),
        "stderr": completed.stderr,
        "catalog_lines": catalog_lines,
        "skill_instructions": skill_instructions,
        "user_prompt": prompt,
        "common_skill_body_automatically_included": "For an assigned pixel-art production task, adopt" in text,
        "pixl_catalog_name_found": bool(re.search(r"- pixl:.*SKILL.md", text)),
        "copied_skill_path_found": (
            str(project / ".agents" / "skills").replace("\\", "/") in skill_context
            and "r0/pixl-kit/skills/pixl/SKILL.md" in skill_context
        ),
        "disabled_home_skill_count": len(disabled),
        "overrides": overrides,
        "command_kind": "codex debug prompt-input",
        "model_inference_executed": False,
        "bundle_manifest_sha256": hashlib.sha256((bundle / "bundle-manifest.json").read_bytes()).hexdigest(),
        "verified_bundle_manifest_entries": sum(
            hashlib.sha256((bundle / row["path"]).read_bytes()).hexdigest() == row["sha256"]
            for row in json.loads((bundle / "bundle-manifest.json").read_text())["files"]
        ),
        "limitations": [
            "debug prompt-input does not expose --ignore-user-config; all configured MCP and plugins were disabled with invocation-only overrides.",
            "Native discovery alone does not establish that a model reads or follows the skill.",
            "No native plugin installation or PixelLab execution is exercised.",
        ],
    }
    (HERE / "codex-loader-probe.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: record[key] for key in (
        "project", "exit_code", "stdout_bytes", "stderr", "catalog_lines",
        "pixl_catalog_name_found", "copied_skill_path_found", "disabled_home_skill_count",
    )}, indent=2))


if __name__ == "__main__":
    main()
