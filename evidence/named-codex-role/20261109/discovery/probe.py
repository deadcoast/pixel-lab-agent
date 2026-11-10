"""Reproduce role discovery without sampling a model or editing user settings.

Saved after the exploratory probes; PROBES.json identifies their exact commands.
Use a fresh destination. The temporary CODEX_HOME contains no copied credentials.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from evaluations.host_trials import codex_command  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--role", type=Path, required=True)
    parser.add_argument("--mode", choices=["explicit-role", "empty-config-trusted"], required=True)
    args = parser.parse_args()
    target = args.destination.resolve()
    target.mkdir(parents=True, exist_ok=False)
    consumer = target / "consumer"
    role = consumer / ".codex/agents/pixl.toml"
    role.parent.mkdir(parents=True)
    role.write_bytes(args.role.read_bytes())
    home = target / "codex-home"
    home.mkdir()
    env = dict(os.environ)
    env["CODEX_HOME"] = str(home)
    command = codex_command() + ["debug", "prompt-input", "-c", "features.apps=false",
        "-c", "features.plugins=false", "-c", "features.memories=false", "-c", "agents.enabled=true"]
    if args.mode == "explicit-role":
        command += ["-c", "agents.pixl.config_file=" + json.dumps(role.as_posix()),
                    "-c", 'agents.pixl.description="PIXL role discovery probe"']
    else:
        (consumer / ".codex/config.toml").write_text("", encoding="utf-8")
        for root in [ROOT, consumer]:
            command += ["-c", "projects." + json.dumps(root.as_posix()) + '.trust_level="trusted"']
    result = subprocess.run(command, cwd=consumer, env=env, capture_output=True, timeout=35)
    (target / "stdout.json").write_bytes(result.stdout)
    (target / "stderr.txt").write_bytes(result.stderr)
    record = {"command": command, "cwd": str(consumer), "CODEX_HOME": str(home),
              "returncode": result.returncode, "role_sha256": hashlib.sha256(role.read_bytes()).hexdigest(),
              "scope": "Prompt-input rendering only; no model sampling or user configuration edits"}
    (target / "result.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
